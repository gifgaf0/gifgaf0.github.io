# What the Proofs Caught (paper draft)

LaTeX sources of a paper on the machine-checked CryptoVerif analysis of
HYBRID-AKE (`../analysis/cryptoverif/`), organised around what mechanization,
mutation tests and two AI-assisted reviews caught. Intended for IACR ePrint.

## Build

```bash
make            # latexmk -pdf main.tex; needs pdflatex, bibtex, latexmk and the lmodern fonts
make clean
```

Tested with TeX Live 2023 (Ubuntu 24.04 packages `texlive-latex-extra`,
`texlive-science`, `lmodern`).

## Where the numbers come from

| In the paper | Source |
|---|---|
| Bounds in Theorems 1–2 and Lemmas 1–2 | `../analysis/cryptoverif/RESULTS.txt` |
| 9 models, 17 queries | `../analysis/cryptoverif/Makefile`, `RESULTS.txt` |
| 22 mutation tests (12 freshness guards) | `../analysis/cryptoverif/mutations.py` (`make mutations`) |
| Findings and their history | `../docs/HYBRID_AKE_COMPUTATIONAL.md` §1, §3, §7, §7.1; `../analysis/cryptoverif/README.md` (Review history); git history |
| Low-order points: 63 tests, 9 mutants of the fix, 335 tests in the suite | `../tests/test_xwing_low_order.py`, `../tests/low_order_mutants.py`; `pytest hybrid_kem/tests` |
| Artifact commit | `74affcf` (models, tests, mutants and fix as described) |
| References | `refs.bib`; each entry names the page it was checked against |

## Before submitting

- [ ] Author name and affiliation in `main.tex` (currently `Matt [Surname]`).
- [ ] Read the whole paper and check it against the artifact. The IACR Board
      has proposed that human authors verify that they understand and endorse
      their entire submission, including AI-generated parts; the last
      sentence of the Acknowledgements (and the TODO above it in
      `sections/conclusion.tex`) depends on this.
- [ ] Confirm the AI-assistance statements (Introduction, "How this work was
      done"; Acknowledgements). They say, from the repository history, that
      the specification, implementation, Tamarin models and proof sketch were
      also written with an AI assistant. Correct them if that is wrong.
- [ ] Re-run `make` and `make mutations` in `../analysis/cryptoverif/`,
      `pytest hybrid_kem/tests` and `python3 hybrid_kem/tests/low_order_mutants.py`
      at the commit cited as the artifact. If PR #49 is merged first, cite the
      merge commit instead and update `refs.bib` (`Artifact`) and Appendix C.
- [ ] Choose ePrint keywords and a licence (ePrint requires one at submission;
      it cannot be changed afterwards).
