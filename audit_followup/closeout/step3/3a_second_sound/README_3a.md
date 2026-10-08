# Second-sound paper, posting version (Step 3a)

**Plain-language summary.** This is the paper you approved on October 4 (v1), ready for your last read before posting. One thing changed: the byline now reads **Matthew Gifford**, matching the Zenodo records. The affiliation already read "Independent researcher, Hollister, California, USA", as in your F5. The cover note was removed when v1 was built. Nothing is posted.

| File | md5 | What it is |
|---|---|---|
| `second_sound_light_cone_v1_posting.pdf` | `41404d8f679d625f6a968a245be7f5df` | 13 pages, A4, XeLaTeX, for your last read |
| `second_sound_light_cone_v1_posting.md` | `b2e9759df65894192f33fca07c41afb3` | Source text: v1 with the byline changed |
| `second_sound_light_cone_v1_posting.tex` | `56f832d1a478c62d4d400538c60db1d9` | The LaTeX the PDF is built from: v1's LaTeX with the byline changed in its two places, the author line and the PDF metadata |
| `build_posting.py` | | Builds all three from the committed v1 files (md5-checked) |

**Checks.**
- The markdown changes in exactly one place and the LaTeX in exactly two. Reversing those changes gives back v1 byte for byte.
- The PDF's extracted text differs from v1's PDF in one line only, the author's name.
- The PDF dates are fixed, so the build reproduces.

**Kept as approved:** the title, the acknowledgments ("every check was made by AI agents, not by human referees"), and every word, number and symbol. The supplementary zip is built by `lbc_bank/paper/submission/build_v1.py --zip OUT`, as recorded in `lbc_bank/paper/APPROVAL_V1.md`.
