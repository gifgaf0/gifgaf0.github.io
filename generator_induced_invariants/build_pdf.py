#!/usr/bin/env python3
"""Build generator_induced_invariants_v1.pdf from its LaTeX source, reproducibly. Nothing here is deposited.

Plain-language summary: the note generalizes the SLWE rank collapse into a reusable result and ships the diagnostic it
describes. This build refuses to produce a PDF that disagrees with the tool it cites:
  1. the SHA-256 printed in the note's Section 7 must equal the checksum of diagnostics/design_matrix_rank.py;
  2. the tool's --self-test, which reproduces Table 1, rank N = 76, the note's other computed facts and the
     verdicts on the case study, the controls and the designs built to fail, must pass;
  3. the LaTeX log must show no errors, no undefined references or citations, and no overfull or underfull boxes;
  4. the PDF's extracted text must contain the file path, the checksum and the self-test command exactly, so that
     what a reader copies is what the note prints (skipped if pdftotext is not installed).
The PDF is built with latexmk/pdflatex and a fixed SOURCE_DATE_EPOCH, as in the SLWE note's build, so it rebuilds
byte-identical. The script prints the md5 (the checksum Zenodo shows) and SHA-256 of both files to be deposited.
"""
import hashlib, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "generator_induced_invariants_v1"
TEX = os.path.join(HERE, BASE + ".tex")
PDF = os.path.join(HERE, BASE + ".pdf")
TOOL = os.path.join(HERE, "diagnostics", "design_matrix_rank.py")
EPOCH = "1792076400"  # 2026-10-15 15:00 UTC
AUX = (".aux", ".fls", ".fdb_latexmk", ".out", ".log")


def digest(path, algo):
    with open(path, "rb") as f:
        return hashlib.new(algo, f.read()).hexdigest()


def fail(msg):
    sys.exit("build_pdf: FAIL: " + msg)


def clean(exts):
    for ext in exts:
        p = os.path.join(HERE, BASE + ext)
        if os.path.exists(p):
            os.remove(p)


# 1. The checksum the note prints must be the tool's actual checksum.
cited = re.findall(r"\b[0-9a-f]{64}\b", open(TEX, encoding="utf-8").read())
if len(cited) != 1:
    fail(f"expected exactly one SHA-256 in {BASE}.tex, found {len(cited)}")
tool_sha = digest(TOOL, "sha256")
if cited[0] != tool_sha:
    fail(f"the note cites SHA-256 {cited[0]} but design_matrix_rank.py is {tool_sha}; update Section 7")
print(f"[1] tool SHA-256 matches the note: {tool_sha}")

# 2. The tool's self-test must reproduce the published values.
r = subprocess.run([sys.executable, "-I", TOOL, "--self-test"], capture_output=True, text=True)
if r.returncode != 0:
    fail("design_matrix_rank.py --self-test failed:\n" + r.stdout + r.stderr)
print("[2] tool self-test: PASS (Table 1 columns k <= 8, rank N = 76 over Q and four primes, the note's other "
      "facts, and the verdicts)")

# 3. Build from scratch, reproducibly, and check the log.
clean(AUX + (".pdf",))
env = dict(os.environ, SOURCE_DATE_EPOCH=EPOCH, FORCE_SOURCE_DATE="1")
subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-quiet", BASE + ".tex"],
               cwd=HERE, check=True, stdout=subprocess.DEVNULL, env=env)
log = open(os.path.join(HERE, BASE + ".log"), encoding="latin-1").read()
problems = [ln for ln in log.splitlines()
            if ln.startswith("!") or re.search(r"undefined|overfull|underfull", ln, re.I)]
if problems:
    fail("LaTeX log problems:\n  " + "\n  ".join(problems[:20]))
print("[3] LaTeX: no errors, no undefined references or citations, no overfull or underfull boxes")

# 4. What a reader copies is what the note prints.
if shutil.which("pdftotext"):
    text = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True, text=True, check=True).stdout
    for needle in ("generator_induced_invariants/diagnostics/design_matrix_rank.py", tool_sha,
                   "python3 design_matrix_rank.py --self-test"):
        if needle not in text:
            fail(f"the PDF's extracted text lacks {needle!r}: copy-paste would not match the print")
    print("[4] copy-paste: path, checksum and self-test command extract exactly")
else:
    print("[4] copy-paste: skipped (pdftotext not installed)")

# 5. Clean up and report the files to deposit.
clean(AUX)
print("[5] files to deposit:")
for p in (PDF, TOOL):
    print(f"    {os.path.relpath(p, HERE):<38} md5 {digest(p, 'md5')}  sha256 {digest(p, 'sha256')}")
