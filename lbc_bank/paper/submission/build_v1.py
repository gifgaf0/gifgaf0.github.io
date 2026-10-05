#!/usr/bin/env python3
"""Build the posting version (v1) of the paper the author approved on October 4, 2026.

Plain-language summary: this takes the approved draft, removes the cover note for the author (and nothing else), and
typesets the result as a PDF with pandoc and XeLaTeX. It also packs the supplementary material (the lbc_bank folder,
with the second computation from main) into one zip with a checksum list. Run it from lbc_bank/paper/submission/.

Steps
  1. Check the approved draft's md5; write second_sound_light_cone_v1.md = the draft minus the leading cover note,
     and assert that cover note + v1 reconstructs the draft byte for byte.
  2. Typesetting transform (in memory only; the v1 markdown is the text of record): title, author and abstract go to
     pandoc metadata; section headings move up one level; the reference list gets one paragraph per entry; Eq. (2)'s
     two formulas are stacked instead of set side by side, to fit the page. No wording, number or symbol changes.
  3. pandoc -> second_sound_light_cone_v1.tex; latexmk -xelatex -> second_sound_light_cone_v1.pdf.
  4. Supplementary zip (optional, --zip OUT): lbc_bank/ from this checkout plus lbc_bank/second_leg/ from origin/main,
     read from the committed tree (HEAD) and origin/main, fixed timestamps, sorted entries, with
     SUPPLEMENT_MD5.txt inside. The zip is not committed.
"""
import hashlib, os, re, subprocess, sys, zipfile, io

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFT = os.path.join(HERE, "..", "second_sound_light_cone_DRAFT.md")
APPROVED_MD5 = "a47080c26bb0a9c601912a5fa925a9f9"     # paper/second_sound_light_cone_DRAFT.md at commit 3664ed1
V1_MD = os.path.join(HERE, "second_sound_light_cone_v1.md")
V1_TEX = os.path.join(HERE, "second_sound_light_cone_v1.tex")

raw = open(DRAFT, "rb").read()
assert hashlib.md5(raw).hexdigest() == APPROVED_MD5, "the draft is not the approved version"
draft = raw.decode("utf-8")

# ---------------------------------------------------------------- 1. remove the cover note, nothing else
assert draft.startswith("<!--\nCOVER NOTE FOR THE AUTHOR")
end = draft.index("\n-->\n") + len("\n-->\n")
cover, v1 = draft[:end], draft[end:]
assert v1.startswith("\n# Second sound breaks the common light cone of a supersolid vacuum\n")
v1 = v1[1:]                                    # the blank line that followed the comment
assert cover + "\n" + v1 == draft
open(V1_MD, "w", encoding="utf-8", newline="\n").write(v1)

# ---------------------------------------------------------------- 2. typesetting transform (in memory)
t = v1
title = re.match(r"# (.+)\n", t).group(1)
t = t[t.index("\n") + 1:]
author_block = "\n**Matt Gifford**\nIndependent researcher, Hollister, California, USA\n"
assert t.startswith(author_block)
t = t[len(author_block):]
a0 = t.index("## Abstract\n\n") + len("## Abstract\n\n")
a1 = t.index("\n\n---\n\n", a0)
abstract = t[a0:a1]
assert "\n" not in abstract
t = t[a1 + len("\n\n---\n\n"):]
t = re.sub(r"^## ", "# ", t, flags=re.M)                       # sections
# Eq. (2): stack the point-defect and line formulas
eq2_old = "\\,dq ,\\qquad\nf_d^{(\\rm line)}"
assert t.count(eq2_old) == 1
t = t.replace("$$F_d^{(3D)}=", "$$\\begin{gathered}F_d^{(3D)}=", 1)
t = t.replace(eq2_old, "\\,dq ,\\\\\nf_d^{(\\rm line)}", 1)
eq2_tail = "\\,dq ,\\tag{2}$$"
assert t.count(eq2_tail) == 1
t = t.replace(eq2_tail, "\\,dq \\end{gathered}\\tag{2}$$", 1)
# references: a list with right-aligned [n] labels, small type
r0 = t.index("# References\n\n") + len("# References\n\n")
refs = [ln for ln in t[r0:].split("\n") if ln.strip()]
assert all(re.match(r"\[\d+\] ", ln) for ln in refs) and len(refs) == 62
LIST_OPEN = (r"\begingroup\small\begin{list}{}{\setlength{\leftmargin}{2.5em}\setlength{\labelwidth}{2.2em}"
             r"\setlength{\labelsep}{0.3em}\setlength{\itemsep}{1pt}\setlength{\parsep}{0pt}\setlength{\topsep}{2pt}}")
items = [re.sub(r"^\[(\d+)\] ", lambda m: "`\\item[{[" + m.group(1) + "]}]`{=latex} ", ln) for ln in refs]
t = (t[:r0] + "```{=latex}\n" + LIST_OPEN + "\n```\n\n" + "\n\n".join(items)
     + "\n\n```{=latex}\n" + r"\end{list}\endgroup" + "\n```\n")
# Table 2: a wider first column, so "35 (e^{-r^6})" stays on one line
sep2 = "|---|---|---|---|---|---|---|---|---|---|"
assert t.count(sep2) == 1
t = t.replace(sep2, "|------|----|-----|----|----|----|----|----|----|----|", 1)
# units stay on the line of their number
t = re.sub(r"\$ (m|fm|GeV)\b", "$ \\1", t)
assert t.count("(10 kpc)") == 1
t = t.replace("(10 kpc)", "(10 kpc)")
# the data-availability paragraph is full of unbreakable file names: set it ragged right
d0 = t.index("# Data and code availability\n\n") + len("# Data and code availability\n\n")
d1 = t.index("\n\n# References", d0)
t = (t[:d0] + "```{=latex}\n\\begingroup\\raggedright\n```\n\n" + t[d0:d1] + "\n\n```{=latex}\n\\par\\endgroup\n```"
     + t[d1:])
AUTHOR = ("`Matt Gifford\\\\[2pt]{\\normalsize Independent researcher, Hollister, California, USA}`{=latex}")
meta = {"title": title, "author": AUTHOR, "date": "4 October 2026", "abstract": abstract}
header = r"""
\usepackage[a4paper,margin=25mm]{geometry}
\usepackage{microtype}
\usepackage{amsmath}
\renewcommand{\arraystretch}{1.15}
\AtBeginEnvironment{longtable}{\small}
\setlength{\LTpre}{6pt}\setlength{\LTpost}{6pt}
\usepackage{titlesec}
\titleformat{\section}{\large\bfseries}{}{0pt}{}
\titlespacing*{\section}{0pt}{14pt}{6pt}
\usepackage[hidelinks]{hyperref}
\hypersetup{pdftitle={Second sound breaks the common light cone of a supersolid vacuum},pdfauthor={Matt Gifford}}
"""
open(os.path.join(HERE, "_header.tex"), "w").write(header)
md_for_pandoc = os.path.join(HERE, "_typeset.md")
yaml = "---\n" + "".join(f"{k}: |\n  {v}\n" for k, v in meta.items()) + "---\n\n"
open(md_for_pandoc, "w", encoding="utf-8").write(yaml + t)

# ---------------------------------------------------------------- 3. pandoc + XeLaTeX
subprocess.run(["pandoc", md_for_pandoc, "-f", "markdown+tex_math_dollars+raw_tex-implicit_figures",
                "-s", "-o", V1_TEX, "--pdf-engine=xelatex", "-H", os.path.join(HERE, "_header.tex"),
                "-V", "fontsize=11pt", "-V", "documentclass=article", "-V", "linestretch=1.08", "-V", "fontfamily=fontspec",
                "-V", "mainfont=Latin Modern Roman", "-V", "mathfont=Latin Modern Math"], check=True)


def floatify(tex, n, with_note):
    """Turn Table n (caption paragraph + longtable [+ the note paragraph after it]) into one table float, so the
    text flows around it instead of leaving half a page empty. Content is moved, not changed."""
    c0 = tex.index("\\emph{Table %d. " % n)
    l0 = tex.index("\\begin{longtable}[]{", c0)
    caption = tex[c0:l0].strip()
    l1 = tex.index("\\end{longtable}", l0) + len("\\end{longtable}")
    body = tex[l0:l1]
    assert body.count("\\endhead\n") == 1 and body.count("\\bottomrule\\noalign{}\n\\endlastfoot\n") == 1
    body = (body.replace("\\begin{longtable}[]{", "\\begin{tabular}{", 1)
                .replace("\\endhead\n", "", 1)
                .replace("\\bottomrule\\noalign{}\n\\endlastfoot\n", "", 1)
                .replace("\\end{longtable}", "\\bottomrule\\noalign{}\n\\end{tabular}", 1))
    end = l1
    note = ""
    if with_note:
        assert tex[l1:l1 + 2] == "\n\n"
        n1 = tex.index("\n\n", l1 + 2)
        note = tex[l1 + 2:n1]
        end = n1
    flt = ("\\begin{table}[tbp]\n\\noindent\\parbox{\\linewidth}{" + caption + "}\\par\\medskip\n{\\small\\centering\n"
           + body + "\\par}\n" + ("\\smallskip\\noindent\\parbox{\\linewidth}{\\footnotesize " + note + "}\n"
                                  if note else "") + "\\end{table}")
    return tex[:c0] + flt + tex[end:]


tex = open(V1_TEX, encoding="utf-8").read()
tex = floatify(tex, 1, False)
tex = floatify(tex, 2, True)
assert "longtable}[]" not in tex
open(V1_TEX, "w", encoding="utf-8").write(tex)
# fixed dates, so the PDF is byte-reproducible (approval time, 2026-10-04 18:08 PDT)
env = dict(os.environ, SOURCE_DATE_EPOCH="1791162480", FORCE_SOURCE_DATE="1")
subprocess.run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "-quiet",
                os.path.basename(V1_TEX)], cwd=HERE, check=True, stdout=subprocess.DEVNULL, env=env)
for ext in (".aux", ".fls", ".fdb_latexmk", ".out", ".xdv", ".log"):
    p = V1_TEX[:-4] + ext
    if os.path.exists(p):
        os.remove(p)
os.remove(md_for_pandoc); os.remove(os.path.join(HERE, "_header.tex"))
print("v1 markdown:", hashlib.md5(open(V1_MD, "rb").read()).hexdigest(), V1_MD)
print("v1 tex     :", hashlib.md5(open(V1_TEX, "rb").read()).hexdigest())
print("v1 pdf     :", hashlib.md5(open(V1_TEX[:-4] + ".pdf", "rb").read()).hexdigest(), os.path.getsize(V1_TEX[:-4] + ".pdf"), "bytes")

# ---------------------------------------------------------------- 4. supplementary zip
if "--zip" in sys.argv:
    out = sys.argv[sys.argv.index("--zip") + 1]
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True,
                          check=True).stdout.strip()
    files = {}
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True,
                          check=True).stdout.strip()
    tracked = subprocess.run(["git", "ls-tree", "-r", "--name-only", head, "lbc_bank"], cwd=root, capture_output=True,
                             text=True, check=True).stdout.split("\n")
    for f in tracked:                          # the committed state, not the working tree
        if f and not f.startswith("lbc_bank/second_leg/"):
            files[f] = subprocess.run(["git", "show", f"{head}:{f}"], cwd=root, capture_output=True,
                                      check=True).stdout
    main_files = subprocess.run(["git", "ls-tree", "-r", "--name-only", "origin/main", "lbc_bank/second_leg"],
                                cwd=root, capture_output=True, text=True, check=True).stdout.split("\n")
    for f in main_files:
        if f:
            files[f] = subprocess.run(["git", "show", f"origin/main:{f}"], cwd=root, capture_output=True,
                                      check=True).stdout
    lines = [f"{hashlib.md5(files[f]).hexdigest()}  {f}" for f in sorted(files)]
    files["lbc_bank/SUPPLEMENT_MD5.txt"] = ("\n".join(lines) + "\n").encode()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(files):
            zi = zipfile.ZipInfo(f, date_time=(2026, 10, 4, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, files[f])
    print("supplement zip from", head[:7], "+ origin/main second_leg:", out, len(files), "files,", os.path.getsize(out), "bytes, md5",
          hashlib.md5(open(out, "rb").read()).hexdigest())
