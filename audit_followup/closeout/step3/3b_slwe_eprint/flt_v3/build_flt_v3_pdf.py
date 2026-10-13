#!/usr/bin/env python3
"""build_flt_v3_pdf.py — PDF of FLT_v3.md: pandoc 3.1 → XeLaTeX, FreeSerif 11 pt, US Letter.

The first heading, the author line and the version line become a centered title block; the notice is set in a frame
on the first page; everything else is converted as written (no fancy lists, super/subscripts, TeX math or raw TeX).
Two builds must be byte-identical (SOURCE_DATE_EPOCH), the log must show no missing glyph, overfull line or font
substitution, and the PDF's text must equal the Markdown's (markup, whitespace and hyphens removed; quotes, the
ellipsis and Unicode normalization made uniform).
"""
import hashlib, os, re, shutil, subprocess, sys, tempfile, unicodedata
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, "FLT_v3.md"), os.path.join(HERE, "Fluid_Lattice_Topology_v3.pdf")
md = open(SRC, encoding="utf-8").read()
lines = md.split("\n")
assert lines[0].startswith("# ") and lines[1] == "" and lines[4] == ""
assert lines[2].startswith("**Matthew Gifford** — ") and lines[3].startswith("**Version 3** — ")
title, author, version = lines[0][2:], lines[2], lines[3]
body = "\n".join(lines[5:])
assert "\\" not in md
EPOCH = int(datetime(2026, 10, 13, tzinfo=timezone.utc).timestamp())

TITLE = ("```{=latex}\n\\begin{center}\n{\\Large\\bfseries " + title + "\\par}\n\\vspace{1em}\n"
         "{\\large\\textbf{Matthew Gifford}" + author[len("**Matthew Gifford**"):] + "\\par}\n\\vspace{0.4em}\n"
         "\\textbf{Version 3}" + version[len("**Version 3**"):] + "\n\\end{center}\n```\n\n")
for x in (title, author, version):
    assert not re.search(r"[{}$&#^_%~]", x), x
FILTER = r'''
local seen = false
function BlockQuote(el)
  if not seen and pandoc.utils.stringify(el):match("^Notice %(October 2026%)") then
    seen = true
    local out = { pandoc.RawBlock("latex", "\\begin{framed}") }
    for _, b in ipairs(el.content) do out[#out + 1] = b end
    out[#out + 1] = pandoc.RawBlock("latex", "\\end{framed}")
    return out
  end
end

-- Keep each table on one page where it fits: reserve its estimated height (and its heading's, when a heading comes
-- right before it) with \\needspace. Lines per row = the longest cell's characters over its column's width, with
-- about 95 characters to the full text width.
local function rows_of(tbl)
  local rows = {}
  if tbl.head and tbl.head.rows then for _, r in ipairs(tbl.head.rows) do rows[#rows + 1] = r end end
  for _, b in ipairs(tbl.bodies) do for _, r in ipairs(b.body) do rows[#rows + 1] = r end end
  return rows
end
local function table_lines(tbl)
  local n, total = #tbl.colspecs, 0
  for _, row in ipairs(rows_of(tbl)) do
    local most = 1
    for i, cell in ipairs(row.cells) do
      local w = tbl.colspecs[i][2]
      if type(w) ~= "number" then w = 1 / n end
      local lines = math.ceil(utf8.len(pandoc.utils.stringify(cell.contents)) / math.max(8, 95 * w * 0.9))
      if lines > most then most = lines end
    end
    total = total + most
  end
  return total + 3
end
function Blocks(blocks)
  local out = {}
  for i, b in ipairs(blocks) do
    if b.t == "Table" then
      local need = table_lines(b)
      local heads = {}
      while #out > 0 and out[#out].t == "Header" do       -- the headings right before the table go with it
        table.insert(heads, 1, table.remove(out))
      end
      out[#out + 1] = pandoc.RawBlock("latex", "\\needspace{" .. (need + 3 * #heads) .. "\\baselineskip}")
      for _, h in ipairs(heads) do out[#out + 1] = h end
    end
    out[#out + 1] = b
  end
  return out
end
'''


def build(d):
    open(os.path.join(d, "in.md"), "w", encoding="utf-8").write(TITLE + body)
    open(os.path.join(d, "f.lua"), "w", encoding="utf-8").write(FILTER)
    open(os.path.join(d, "h.tex"), "w", encoding="utf-8").write("\\usepackage{framed}\n\\usepackage{microtype}\n\\usepackage{needspace}\n\\hyphenation{zenodo}\n"
        "\\AtBeginDocument{\\setlength{\\emergencystretch}{8em}}\n")
    subprocess.run(["pandoc", "in.md", "-f", "markdown-fancy_lists-superscript-subscript-tex_math_dollars-raw_tex",
                    "-t", "latex", "-s", "-o", "p.tex", "--lua-filter", "f.lua", "-H", "h.tex",
                    "--shift-heading-level-by=-1", "-V", "documentclass=article", "-V", "fontsize=11pt",
                    "-V", "geometry:letterpaper,margin=1in", "-V", "mainfont=FreeSerif", "-V", "fontfamily=fontspec",
                    "-M", "lang=en-US", "-M", f"title-meta={title}", "-M", "author-meta=Matthew Gifford"],
                   cwd=d, check=True)
    env = dict(os.environ, SOURCE_DATE_EPOCH=str(EPOCH), FORCE_SOURCE_DATE="1")
    for _ in range(2):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "p.tex"], cwd=d, env=env,
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stdout[-3000:]
    log = open(os.path.join(d, "p.log"), encoding="utf-8", errors="replace").read()
    bad = [l for l in log.split("\n") if re.search(r"Missing character|Overfull \\[hv]box|undefined|"
                                                     r"Font shape .* not available", l)]
    return open(os.path.join(d, "p.pdf"), "rb").read(), bad, log


d1, d2 = tempfile.mkdtemp(), tempfile.mkdtemp()
try:
    p1, bad, log = build(d1)
    p2, _, _ = build(d2)
finally:
    shutil.rmtree(d1, ignore_errors=True); shutil.rmtree(d2, ignore_errors=True)
assert not bad, "\n".join(bad)
assert p1 == p2, "builds differ"
open(OUT, "wb").write(p1)
text = subprocess.run(["pdftotext", "-enc", "UTF-8", OUT, "-"], capture_output=True, text=True, check=True).stdout


def squash(s):
    for x, y in (("\u00a0", " "), ("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("…", "...")):
        s = s.replace(x, y)
    return unicodedata.normalize("NFC", re.sub(r"[\s\-‐]+", "", s))


def plain(t):
    """Markdown text with markup removed (headings, quotes, emphasis, code ticks, rules)."""
    t = re.sub(r"^#+ ", "", t, flags=re.M)
    t = re.sub(r"^> ?", "", t, flags=re.M).replace("**", "").replace("*", "").replace("`", "")
    return re.sub(r"^---$", "", t, flags=re.M)


# The markdown split into text runs and tables (a table is a block of lines starting with "|").
runs, tables, cur, in_table = [], [], [], False
for l in md.split("\n"):
    if l.startswith("|") != in_table:
        (tables if in_table else runs).append("\n".join(cur)); cur = []; in_table = not in_table
    cur.append(l)
(tables if in_table else runs).append("\n".join(cur))
table_text = "\n".join(re.sub(r"^\|[-| ]+\|$", "", t, flags=re.M).replace("|", " ") for t in tables)
# page numbers: on page k, the last non-empty line is "k"; only those lines are dropped
pages_txt = text.split("\f")
kept = []
for k, pg in enumerate(pages_txt, 1):
    ls = pg.split("\n")
    nz = [i for i, l in enumerate(ls) if l.strip()]
    if nz and ls[nz[-1]].strip() == str(k):
        del ls[nz[-1]]
    kept.append("\n".join(ls))
pdf_text = squash("\n".join(kept))
md_all_tmp = squash(plain("\n".join(runs)))
# longtable repeats a table's header row after a page break; drop the repeats
for t in tables:
    head = squash(plain(t.split("\n")[0].replace("|", " ")))
    while pdf_text.count(head) > 1 and pdf_text.count(head) > md_all_tmp.count(head) + 1:
        i = pdf_text.rindex(head)
        pdf_text = pdf_text[:i] + pdf_text[i + len(head):]
md_all = squash(plain("\n".join(runs) + "\n" + table_text))

# 1. the same characters, with the same multiplicities, as the whole markdown text
from collections import Counter
same_chars = Counter(md_all) == Counter(pdf_text)
# 2. outside the tables, the same order: each text run appears in the PDF text, in sequence (pdftotext reads wrapped
#    table cells column by column, so order is only checked outside the tables)
pos, in_order = 0, True
for r in runs:
    r = squash(plain(r))
    if not r:
        continue
    k = pdf_text.find(r, pos)
    if k < 0:
        in_order = False
        print("RUN NOT FOUND IN ORDER:", r[:80])
        break
    pos = k + len(r)
if not (same_chars and in_order):
    ca, cb = Counter(md_all), Counter(pdf_text)
    print("characters only in the markdown:", dict(ca - cb), "| only in the PDF:", dict(cb - ca))
    sys.exit("text check FAILED")
pages = re.search(r"^Pages:\s+(\d+)", subprocess.run(["pdfinfo", OUT], capture_output=True, text=True).stdout,
                  flags=re.M).group(1)
print(f"{os.path.basename(OUT)}: md5 {hashlib.md5(p1).hexdigest()} | {len(p1)} B | {pages} pages | builds identical "
      f"| no missing glyphs or overfull lines | underfull: {log.count('Underfull')} | text check: same "
      f"{len(md_all)} characters as FLT_v3.md, in order outside the {len(tables)} tables")
