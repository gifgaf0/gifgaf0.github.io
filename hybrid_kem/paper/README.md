# What the Proofs Caught (paper draft)

LaTeX sources of a paper on the machine-checked CryptoVerif analysis of
HYBRID-AKE (`../analysis/cryptoverif/`), organised around what mechanization,
mutation tests and an independent review caught. Intended for IACR ePrint.

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
| 9 models, 17 queries, ~12 s | `../analysis/cryptoverif/Makefile`, `RESULTS.txt` |
| 16 mutation tests | `../analysis/cryptoverif/mutations.py` (`make mutations`) |
| Findings and their history | `../docs/HYBRID_AKE_COMPUTATIONAL.md` §7, §7.1; `../analysis/cryptoverif/README.md` (Review history) |
| Low-order points: 63 tests, 335 in the suite | `../tests/test_xwing_low_order.py`; `pytest hybrid_kem/tests` |
| Artifact commit | `67cc5f6` (models, tests and fix as analysed) |

## Before submitting

- [ ] Author name and affiliation in `main.tex` (currently `Matt [Surname]`).
- [ ] Confirm the AI-assistance statement (Introduction, "How this work was
      done", and the Acknowledgements) matches how you want to describe it.
- [ ] References verified against primary sources (see `refs.bib` comments).
- [ ] Re-run `make` and `make mutations` in `../analysis/cryptoverif/` and
      `pytest hybrid_kem/tests` at the commit cited as the artifact; update
      the commit in `refs.bib` (`Artifact`) and Appendix C if it changes.
- [ ] Choose ePrint keywords and a licence.
