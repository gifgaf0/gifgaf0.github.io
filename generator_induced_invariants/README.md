# Generator-Induced Invariants in Lattice Public Keys

A methodological note and a runnable diagnostic, generalizing the rank collapse found in the sedenion Module-LWE
("SLWE") negative result (`audit_followup/closeout/step3/3b_slwe_eprint/`; Zenodo doi:10.5281/zenodo.23352161).

## The claim, in one line

A public key built by applying a **fixed family of linear maps to random seeds** is the image of a single fixed
*design matrix* `D`: it factors as `M = R·D`, so `rank M ≤ rank D` for every instance size and every seed draw. If
`rank D` is below the ambient dimension, the key is distinguishable from uniform and noise recovery drops to dimension
at most `rank D`. The weakness hides because **a rank check on a realized instance of dimension n certifies only
rank D ≥ n**: SLWE's own check, run at module rank 4 (n = 64), could not see its ceiling of 76.

## Contents

| File | What it is |
|---|---|
| `generator_induced_invariants_v1.tex` | The note's source (canonical), in the same house style as the SLWE note. |
| `generator_induced_invariants_v1.pdf` | The note, 9 pages, built by `build_pdf.py`. |
| `build_pdf.py` | Reproducible build (fixed `SOURCE_DATE_EPOCH`; rebuilds byte-identical). It refuses to build if the SHA-256 printed in §7 does not match the tool, if the tool's self-test fails, if the LaTeX log shows any error, undefined reference or over/underfull box, or if the printed path, checksum or command would not copy and paste exactly. |
| `diagnostics/design_matrix_rank.py` | The §4 diagnostic. Pure Python 3.8+, no dependencies. |
| `ZENODO_DRAFT.md`, `ZENODO_DESCRIPTION.txt` | What to deposit, the record settings, and the description to paste (one line per paragraph). Nothing is deposited. |

The first draft, `generator_induced_invariants_DRAFT_v1.md`, is superseded by the `.tex` and remains in git history.

## Build

```bash
python3 build_pdf.py    # needs latexmk/pdflatex; pdftotext for the copy-paste check
```

## The diagnostic

```bash
cd diagnostics
python3 -I design_matrix_rank.py --self-test   # Table 1 columns k <= 8, rank N = 76 over four characteristics
python3 -I design_matrix_rank.py               # full report: SLWE (FAIL, ceiling 76) and a uniform control (PASS)
```

The self-test exits non-zero on any mismatch, so it doubles as a CI check pinned to the published result. To diagnose
another construction, implement the `GeneratorScheme` interface (`design_matrix()`, `realize()`, `ambient_rank()`,
`random_seeds()`) and pass it to `diagnose(...)`.

## Changes from the first draft

- **Proposition 2 restated.** The draft said a generated object is "generically full rank" below the generator's
  saturation size. As stated that is false (SLWE is already deficient at k = 5, with 80 of a possible 112 columns), and
  the threshold is the ceiling ρ, not the number of generator images. The note now proves the exact statement: a
  full-rank check at dimension n certifies only ρ ≥ n, and a deficiency must show once n > ρ. The tool's docstring had
  the same error and is corrected.
- **Corollaries made exact.** The distinguisher is a fixed common kernel (`ker D ⊆ ker M`; a uniform matrix passes the
  test with probability q^−a), and the recovery corollary counts samples by the rows of `M` and gives dimension at most
  `rank D`.
- **§5 tiering.** The draft tagged the McEliece, NTRU and principal-ideal entries T2, but nothing there follows from
  Proposition 1. The note now cites those breaks as established results and calls the classification interpretive.
- **Self-references pinned** from the repository's deposit records: the SLWE note, version 2 (10.5281/zenodo.23352161;
  all versions 10.5281/zenodo.23270248), and *Fluid Lattice Topology*, version 3 (10.5281/zenodo.23351706).
- **The tool's report** no longer prints a ceiling line for the uniform control, whose realized matrix is not of the
  form `R·D` with a fixed 16×16 `D`.

## Scope

Defensive and methodological. The case study is the author's own withdrawn proposal; the NIST standards appear only as
correctly designed controls. The tool analyses the structure of a construction you hand it; it is not an attack on any
deployed system. The design-matrix rank test is **necessary, not sufficient**: SLWE, with the structure removed, still
failed on its modulus-to-noise ratio, which this tool does not judge.
