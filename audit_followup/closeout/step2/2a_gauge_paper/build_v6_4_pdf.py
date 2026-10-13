#!/usr/bin/env python3
"""build_v6_4_pdf.py — builds the PDF of the gauge paper v6.4 from Gifford_Csaszar_Gauge_Group_v6_4_2026_FINAL.md.

Toolchain: pandoc 3.1 → XeLaTeX, FreeSerif 11 pt on US Letter, with pdf_filter.lua (layout only). The template
variable fontfamily=fontspec keeps pandoc's template from loading lmodern, which this TeX installation lacks. The
Markdown is read without fancy lists, superscripts, subscripts, TeX math or raw TeX, so "(i)", "(−1)^(N+1)" and the
like are set exactly as written. The file's first five paragraphs (title, author, affiliation, date) become a centered
title block; everything after them is converted as it stands. SOURCE_DATE_EPOCH fixes the dates. The script builds
twice in separate directories and requires the two PDFs to be identical, and it fails on any missing glyph, overfull
line, undefined reference or font-shape substitution.

Output: Gifford_Csaszar_Gauge_Group_v6_4_2026.pdf and build_pdf_output.txt, next to this script.
"""
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import unicodedata
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Gifford_Csaszar_Gauge_Group_v6_4_2026_FINAL.md")
SRC_MD5 = "f24dcc37690a7d2083fba3eb590bba8a"
FILTER = os.path.join(HERE, "pdf_filter.lua")
OUT = os.path.join(HERE, "Gifford_Csaszar_Gauge_Group_v6_4_2026.pdf")
EPOCH = int(datetime(2026, 10, 13, tzinfo=timezone.utc).timestamp())

md = open(SRC, encoding="utf-8").read()
assert hashlib.md5(md.encode("utf-8")).hexdigest() == SRC_MD5, "FINAL.md md5 mismatch"
lines = md.split("\n")
head = lines[:10]
assert head[1::2] == [""] * 5, head
t1, t2, author, affil, date = head[0::2]
assert t1.startswith("**") and t1.endswith("**") and t2.startswith("**") and t2.endswith("**")
assert affil.startswith("*") and affil.endswith("*") and not affil.startswith("**")
assert author == "Matthew Gifford" and date == "October 2026 — v6.4 (Revised)"
t1, t2, affil = t1[2:-2], t2[2:-2], affil[1:-1]
for x in (t1, t2, author, affil, date):
    assert not re.search(r"[\\{}$&#^_%~]", x), x          # nothing that would need escaping in the raw title block
body = "\n".join(lines[10:])
assert "\\" not in body                                      # raw TeX is off; check there is none to lose

TITLE = ("```{=latex}\n\\begin{center}\n"
         f"{{\\LARGE\\bfseries {t1}\\\\[3pt] {t2}\\par}}\n\\vspace{{1.2em}}\n"
         f"{{\\large {author}\\par}}\n\\vspace{{0.3em}}\n{{\\itshape {affil}\\par}}\n\\vspace{{0.6em}}\n"
         f"{date}\n\\end{{center}}\n\\vspace{{0.8em}}\n```\n\n")

HEADER = r"""\newfontfamily\dsfont{FreeSerif}[BoldFont=FreeSerif,ItalicFont=FreeSerif,BoldItalicFont=FreeSerif]
\usepackage{microtype}
"""


def build(workdir):
    open(os.path.join(workdir, "in.md"), "w", encoding="utf-8").write(TITLE + body)
    open(os.path.join(workdir, "header.tex"), "w", encoding="utf-8").write(HEADER)
    subprocess.run(["pandoc", "in.md", "-f", "markdown-fancy_lists-superscript-subscript-tex_math_dollars-raw_tex",
                    "-t", "latex", "-s", "-o", "paper.tex", "--lua-filter", FILTER, "-H", "header.tex",
                    "-V", "documentclass=article", "-V", "fontsize=11pt", "-V", "geometry:letterpaper,margin=1in",
                    "-V", "mainfont=FreeSerif", "-V", "fontfamily=fontspec", "-M", "lang=en-US",
                    "-M", f"title-meta={t1} {t2}", "-M", f"author-meta={author}"],
                   cwd=workdir, check=True)
    env = dict(os.environ, SOURCE_DATE_EPOCH=str(EPOCH), FORCE_SOURCE_DATE="1")
    for _ in range(2):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"], cwd=workdir,
                           env=env, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout[-3000:]
    log = open(os.path.join(workdir, "paper.log"), encoding="utf-8", errors="replace").read()
    problems = [ln for ln in log.split("\n") if re.search(
        r"Missing character|Overfull \\hbox|Overfull \\vbox|undefined|Font shape .* not available|"
        r"Some font shapes were not available", ln)]
    pdf = open(os.path.join(workdir, "paper.pdf"), "rb").read()
    return pdf, problems, log


tmp1, tmp2 = tempfile.mkdtemp(prefix="gauge_pdf_a_"), tempfile.mkdtemp(prefix="gauge_pdf_b_")
try:
    pdf1, probs1, log1 = build(tmp1)
    pdf2, probs2, _ = build(tmp2)
    assert not probs1, "\n".join(probs1)
    same = pdf1 == pdf2
    assert same, "the two builds differ"
    open(OUT, "wb").write(pdf1)
    info = subprocess.run(["pdfinfo", OUT], capture_output=True, text=True, check=True).stdout
    fonts = subprocess.run(["pdffonts", OUT], capture_output=True, text=True, check=True).stdout
    pages = re.search(r"^Pages:\s+(\d+)", info, flags=re.M).group(1)
    underfull = len(re.findall(r"Underfull \\hbox", log1))
    text = subprocess.run(["pdftotext", "-enc", "UTF-8", OUT, "-"], capture_output=True, text=True, check=True).stdout
finally:
    shutil.rmtree(tmp1, ignore_errors=True)
    shutil.rmtree(tmp2, ignore_errors=True)


# Fidelity: the PDF's text layer must equal the Markdown's text, once Markdown markup, page numbers, whitespace and
# hyphens (a hyphen at a line end cannot be told from LaTeX's hyphenation) are removed; once pandoc's typographic
# quotes and its ellipsis (it sets the "..." of {e₁, ..., e₇} as "…") are put back in plain form; and once both are in
# Unicode NFC (pdftotext writes accented letters such as the á of Császár decomposed).
def squash(s):
    for x, y in (("\u00a0", " "), ("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("…", "...")):
        s = s.replace(x, y)
    return unicodedata.normalize("NFC", re.sub(r"[\s\-‐]+", "", s))


md_text = re.sub(r"^#+ ", "", md, flags=re.M).replace("**", "").replace("*", "")
pdf_text = "\n".join(ln for ln in text.replace("\f", "\n").split("\n") if not re.fullmatch(r"\s*\d+\s*", ln))
fidelity = squash(md_text) == squash(pdf_text)
assert fidelity, "the PDF's text differs from the Markdown's"

report = [f"source: {os.path.basename(SRC)} md5 {SRC_MD5}",
          f"output: {os.path.basename(OUT)} md5 {hashlib.md5(pdf1).hexdigest()} | {len(pdf1)} bytes | {pages} pages",
          f"SOURCE_DATE_EPOCH={EPOCH} (2026-10-13T00:00:00Z) | two builds identical: {same}",
          "missing glyphs, overfull lines, undefined references, font substitutions: none",
          f"underfull lines (loose, not overfull): {underfull}",
          f"text layer equals the Markdown text ({len(squash(md_text))} characters, markup and whitespace removed): "
          f"{fidelity}",
          "fonts:", fonts.rstrip()]
print("\n".join(report))
open(os.path.join(HERE, "build_pdf_output.txt"), "w", encoding="utf-8").write("\n".join(report) + "\n")
