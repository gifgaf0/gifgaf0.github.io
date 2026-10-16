# Generator-Induced Invariants in Lattice Public Keys

A methodological note and a runnable diagnostic, generalizing the rank collapse found in the sedenion Module-LWE
("SLWE") negative result (`audit_followup/closeout/step3/3b_slwe_eprint/`; Zenodo doi:10.5281/zenodo.23352161).

## The claim, in one line

A public key built by applying a **fixed family of linear maps to random seeds** is the image of a single fixed
*design matrix* `D`: it factors as `M = R·D`, so `rank M ≤ rank D` for every instance size and every seed draw. If
`rank D` is below the ambient dimension at the deployed size, every key is rank-deficient: distinguishable from the
uniform matrix a security reduction assumes, with noise recovery reduced to dimension at most `rank D`. The weakness
hides because **a rank check on a realized instance of dimension n certifies only rank D ≥ n**: SLWE's own check, run
at module rank 4 (n = 64), could not see its ceiling of 76.

## Contents

| File | What it is |
|---|---|
| `generator_induced_invariants_v1.tex` | The note's source (canonical), in the same house style as the SLWE note. |
| `generator_induced_invariants_v1.pdf` | The note, 11 pages, built by `build_pdf.py`. |
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
python3 -I design_matrix_rank.py --self-test   # Table 1 (k <= 8), rank N = 76 over Q and four primes, the note's
                                               # other computed facts, and the verdicts below
python3 -I design_matrix_rank.py               # full report: SLWE (FAIL, ceiling 76) and two structured,
                                               # sound controls (PASS)
python3 -I design_matrix_rank.py --plugin my_scheme.py:MyScheme   # your own construction
```

The self-test exits non-zero on any mismatch, so it doubles as a CI check pinned to the published result. Otherwise the
exit status is 0 if every verdict is PASS, 1 if any is FAIL, and 2 on an ERROR (a design that does not factor its
realization).

To diagnose another construction, subclass `GeneratorScheme` in a file of your own (`from design_matrix_rank import
GeneratorScheme` works there even under `-I`) and run it with `--plugin`. Implement `design_matrix(k)` (the fixed
design at size k; any matrix with the same row space will do), `realize(k, seeds, p)`, `ambient_rank(k)` and
`random_seeds(k, p, rng)`, and set `parameter_sets = [(label, deployed k, working modulus q), ...]`: the verdict is
taken at each deployed size. Optional: `full_design()` (every generator image, which bounds every size),
`reference_realize(k, p, rng)` (a sample of the distribution your security argument assumes; default uniform over
F_p) and `shape(k)` for non-square maps. The built-in controls are a sedenion module with independent uniform entries
and an ML-KEM-shaped module over Z_3329[X]/(X^256+1) at k = 2, 3, 4.

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

## Changes after review (October 15, 2026)

A review of the PDF found two claims that were wrong as written and a verdict bug in the tool. All are fixed, and the
self-test now checks each corrected claim.

- **Remark 2 contradicted Table 1.** It said the realized rank is exactly min(n(k), ρ); at k = 5 and 6 that is 76, but
  the table shows 72 and 74. The realized rank equals rank N_k, the design restricted to the powers in use, so
  Proposition 1 is tight. The conclusions (first visible at k = 5; k = 4 uninformative) stand.
- **Remark 1 and step 5 overclaimed.** They said any fixed subspace that D "preserves or annihilates" transfers to M.
  Only the kernel transfers through M = R·D, and that is the rank ceiling again. Every multiplication map of ML-KEM's
  ring preserves the same 128 two-dimensional subspaces (the NTT slots), and ML-DSA's share 256 eigenvectors, so the
  old step 5 would have flagged the note's own controls. The remark now states the missing condition (the projection
  must keep the noise short) and cites the weak Ring-LWE literature. Step 5 flags the rank ceiling only.
- **The tool could print PASS on a collapsing design.** It reported a ceiling only when rank D was below D's own
  smaller dimension, not the ambient dimension at the deployed size. Two examples printed PASS: SLWE's shape with a
  generic full-rank 256×112 design (rank 112 of 128 at k = 8), and a row-seeded design (rank 256 of 320 at k = 20).
  The old uniform control passed only through the same comparison: its 16×16 identity "design" did not factor its
  16k×16k realization. Changes:
  - `design_matrix(k)` and `parameter_sets`, with the verdict taken at each deployed size;
  - a step-0 count bound;
  - exact rank over Q by fraction-free elimination;
  - an ERROR verdict when a realized rank exceeds rank D_k;
  - controls that are real factorizations: a sedenion module and an ML-KEM-shaped module;
  - designs built to fail, as regression tests.
- **Distinguisher made precise.** Every structured matrix, ML-KEM's included, is distinguishable from a uniform matrix
  over F_q. Corollary 1 now also covers the distribution a module reduction assumes (independent uniform entries). For
  SLWE the kernel test separates the Singer-orbit keys from that distribution, and the self-test checks this.
- **"Necessary, not sufficient" scoped.** Passing is necessary for any argument that assumes a full-rank uniform
  matrix. A ceiling reduces recovery to dimension ρ, which is fatal here (ρ = 76) but not in general.
- **Added:**
  - the hypothesis Proposition 2 uses (col(D_k) ⊆ col(D));
  - the two counting bounds (seed length × block rows; distinct generator images);
  - the observation that rank over Q bounds every modulus;
  - σ and the Cayley–Dickson convention, stated explicitly (the other common convention gives the same ranks);
  - 76 = 16 + 6·10;
  - σ is not even a Fano collineation in the product's labelling;
  - the step from noise recovery to decryption;
  - a definition of "seed" (the coefficients the generator consumes, after any XOF);
  - §5 entries for Rainbow and for weak Ring-LWE instances, and the McEliece dimension tests.
  - Notation: `rank M` (not `rank A`); D ∈ F^{g×b} (the row count no longer shares the name N).
- **PDF:** list bullets now come from a Type 1 font. The text-companion bullet had been embedded as a bitmap.

## Scope

Defensive and methodological. The case study is the author's own withdrawn proposal; the ML-KEM design appears only as
a correctly designed control, which the tool passes. The tool analyses the structure of a construction you hand it; it
is not an attack on any deployed system. Passing the design-matrix rank test is **necessary for a uniform-matrix
security argument, not sufficient**: SLWE, with the structure removed, still failed on its modulus-to-noise ratio,
which this tool does not judge.
