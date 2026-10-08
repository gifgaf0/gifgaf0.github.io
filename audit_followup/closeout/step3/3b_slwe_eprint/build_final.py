#!/usr/bin/env python3
"""Step 3b: the SLWE negative-result note for IACR ePrint, final form for the author's approval. Not submitted.

Plain-language summary: this takes the Phase C draft and changes three things.
  - The byline and contact follow F5: "Matthew Gifford", independent researcher, Hollister, California, USA. The email
    placeholder is dropped, because the repository is public; ePrint's submission form asks for an email separately.
  - The acknowledgement becomes one sentence on AI assistance, for the author to approve.
  - The red DRAFT date line becomes "October 2026".
Everything else is the Phase C text, unchanged. The PDF is built with latexmk/pdflatex, as before.
"""
import hashlib, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../../../phase_c/C1/eprint_draft/slwe_negative_result.tex")
SRC_MD5 = "70ea6610a6df829894c3235e9f91c845"
t = open(SRC, encoding="utf-8").read()
assert hashlib.md5(t.encode()).hexdigest() == SRC_MD5
ACK = ("AI agents (Anthropic's Claude) drafted this note and wrote and ran all of its computations, including both "
       "independent rank implementations; the author directed the work, reviewed the text, and takes responsibility "
       "for it.")
E = [
    (r"\author{Matt Gifford\\ \small independent researcher \quad \textit{[contact email to be added by the author]}}",
     r"\author{Matthew Gifford\\ \small Independent researcher, Hollister, California, USA}"),
    (r"\date{\small \textcolor{red}{DRAFT, October 7, 2026 --- not submitted; for the author's review}}",
     r"\date{\small October 2026}"),
    ("\\paragraph{Acknowledgements.} The computations and both rank implementations were carried out by AI agents, not by\nhuman referees.",
     "\\paragraph{Acknowledgements.} " + ACK),
]
out = t
for old, new in E:
    assert t.count(old) == 1, old[:60]
    out = out.replace(old, new, 1)
rev = out
for old, new in reversed(E):
    rev = rev.replace(new, old, 1)
assert rev == t
assert "Matt Gifford" not in out and "DRAFT" not in out and "contact email" not in out
base = os.path.join(HERE, "slwe_negative_result_final")
open(base + ".tex", "w", encoding="utf-8").write(out)
env = dict(os.environ, SOURCE_DATE_EPOCH="1791212400", FORCE_SOURCE_DATE="1")
subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-quiet", os.path.basename(base) + ".tex"],
               cwd=HERE, check=True, stdout=subprocess.DEVNULL, env=env)
for ext in (".aux", ".fls", ".fdb_latexmk", ".out", ".log"):
    if os.path.exists(base + ext):
        os.remove(base + ext)
for ext in (".tex", ".pdf"):
    b = open(base + ext, "rb").read()
    print(f"final{ext}: md5 {hashlib.md5(b).hexdigest()} ({len(b)} B)")
print("three edits; reverse to the Phase C draft byte-identical — PASS")
