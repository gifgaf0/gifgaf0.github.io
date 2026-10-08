#!/usr/bin/env python3
"""Step 3a: the second-sound paper's posting version = the approved v1 with the byline per F5, and nothing else changed.

Plain-language summary: this takes the v1 source and LaTeX exactly as built on October 4 and changes one thing, the
author's name ("Matt Gifford" → "Matthew Gifford", matching the Zenodo records; the affiliation already reads
"Independent researcher, Hollister, California, USA"). The cover note was already removed in v1. Then it typesets the PDF.

Inputs (lbc_bank/paper/submission/, as committed): second_sound_light_cone_v1.md (md5 0dc9b1ea…, the approved draft minus
the cover note) and second_sound_light_cone_v1.tex (md5 727a1ad4…, the LaTeX of the v1 PDF).
Outputs (this directory): second_sound_light_cone_v1_posting.md / .tex / .pdf.
Checks: exactly one byline change in the markdown, and exactly two in the LaTeX (the \\author line and the PDF metadata).
Removing them restores v1 byte for byte. The PDF dates are fixed, so the build reproduces.
"""
import hashlib, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
SUB = os.path.join(HERE, "../../../../lbc_bank/paper/submission")
MD, TEX = os.path.join(SUB, "second_sound_light_cone_v1.md"), os.path.join(SUB, "second_sound_light_cone_v1.tex")
md, tex = open(MD, encoding="utf-8").read(), open(TEX, encoding="utf-8").read()
assert hashlib.md5(md.encode()).hexdigest() == "0dc9b1ea59384bdca33e9980b6cbb8ef"
assert hashlib.md5(tex.encode()).hexdigest() == "727a1ad4cd7283305729583a4744860e"
OLD_MD, NEW_MD = "\n**Matt Gifford**\n", "\n**Matthew Gifford**\n"
OLD_T1, NEW_T1 = "\\author{Matt Gifford\\\\[2pt]", "\\author{Matthew Gifford\\\\[2pt]"
OLD_T2, NEW_T2 = "pdfauthor={Matt Gifford}", "pdfauthor={Matthew Gifford}"
assert md.count(OLD_MD) == 1 and md.count("Matt Gifford") == 1
assert tex.count(OLD_T1) == 1 and tex.count(OLD_T2) == 1 and tex.count("Matt Gifford") == 2
md2 = md.replace(OLD_MD, NEW_MD, 1)
tex2 = tex.replace(OLD_T1, NEW_T1, 1).replace(OLD_T2, NEW_T2, 1)
assert md2.replace(NEW_MD, OLD_MD, 1) == md and tex2.replace(NEW_T1, OLD_T1, 1).replace(NEW_T2, OLD_T2, 1) == tex
assert "COVER NOTE" not in md2 and "<!--" not in md2
base = os.path.join(HERE, "second_sound_light_cone_v1_posting")
open(base + ".md", "w", encoding="utf-8", newline="\n").write(md2)
open(base + ".tex", "w", encoding="utf-8", newline="\n").write(tex2)
env = dict(os.environ, SOURCE_DATE_EPOCH="1791162480", FORCE_SOURCE_DATE="1")    # v1's fixed date (Oct 4, 18:08 PDT)
subprocess.run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "-quiet",
                os.path.basename(base) + ".tex"], cwd=HERE, check=True, stdout=subprocess.DEVNULL, env=env)
for ext in (".aux", ".fls", ".fdb_latexmk", ".out", ".xdv", ".log"):
    if os.path.exists(base + ext):
        os.remove(base + ext)
for ext in (".md", ".tex", ".pdf"):
    b = open(base + ext, "rb").read()
    print(f"posting{ext}: md5 {hashlib.md5(b).hexdigest()} ({len(b)} B)")
print("byline changed in 1 + 2 places; reverse to v1: byte-identical — PASS")
