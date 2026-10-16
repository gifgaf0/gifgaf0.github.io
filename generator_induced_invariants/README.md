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
| `generator_induced_invariants_v1.pdf` | The note, 12 pages, built by `build_pdf.py`. |
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
python3 -I design_matrix_rank.py               # full report: SLWE (FAIL, ceiling 76) and two structured
                                               # controls (PASS)
python3 -I design_matrix_rank.py --plugin my_scheme.py:MyScheme   # your own construction
```

The self-test exits non-zero on any mismatch, so it doubles as a CI check pinned to the published result. Otherwise
the exit status is 0 if every verdict is PASS, 1 if any is FAIL, and 2 on an ERROR: a design that does not describe
its construction, a composite modulus, or any crash.

To diagnose another construction, subclass `GeneratorScheme` in a file of your own (`from design_matrix_rank import
GeneratorScheme` works there even under `-I`) and run it with `--plugin`. Implement:

- `design_matrix(k)`: the *minimal* fixed design at size k. Its row space must equal the span of the rows of
  `realize()` at unit seeds. Repeated rows may be dropped.
- `realize(k, seeds, p)`: linear in the seeds.
- `ambient_rank(k)` and `random_seeds(k, p, rng)`.
- `parameter_sets = [(label, deployed k, working prime q), ...]`: the verdict is taken at each deployed size.

Optional:

- `shape(k)` for a non-square map.
- `full_design()`: every generator image, with the same rows as `design_matrix(k)`; it bounds every size.
- `reference_realize(k, p, rng)`: a sample of the distribution your security argument assumes; the default is uniform
  over F_p.

The tool checks the design against the realizations. A realized row outside row(D_k) is an ERROR. So is a design that
the realizations at unit seeds do not span: any design contains them, since R = M and D = I always factor, but only
the minimal one makes a PASS mean something. The minimality check runs at the sizes the tool can afford; at the
deployed sizes the verdict relies on `design_matrix(k)`. The built-in controls are a sedenion module with independent
uniform entries and an ML-KEM-shaped module over Z_3329[X]/(X^256+1) at k = 2, 3, 4.

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

Two reviews of the PDF, the second an independent referee pass over the first round of fixes, found claims that were
wrong as written and verdict bugs in the tool. All are fixed below, and the self-test checks each corrected claim.

**The note**

- **Remark 2 contradicted Table 1.** It said the realized rank is exactly min(n(k), ρ); at k = 5 and 6 that is 76, but
  the table shows 72 and 74. The realized rank equals rank N_k, the design restricted to the powers in use, so
  Proposition 1 is tight. The tool now confirms this from first principles: the realizations at unit seeds span
  exactly 16, 72 and 76 dimensions at k = 1, 5 and 8. The conclusions (first visible at k = 5; k = 4 uninformative)
  stand.
- **The design matrix was not unique.** R = M with D the identity always factors, so a full-rank D proved nothing.
  §2.1 now defines D as the minimal design, with row(D) = W, the span of the realizations at unit seeds. A ceiling
  found with any valid D is real; a pass needs the minimal one.
- **Remark 1 and step 5 overclaimed.** They said any fixed subspace that D "preserves or annihilates" transfers to M.
  Only the kernel transfers through M = R·D, and that is the rank ceiling again. Every multiplication map of ML-KEM's
  ring preserves the same 128 two-dimensional subspaces (the NTT slots), and ML-DSA's share 256 eigenvectors, so the
  old step 5 would have flagged the note's own controls. The remark now states the missing condition, that the
  projected noise be far from uniform (short, or confined to a small set), and cites the weak Ring-LWE literature.
  Step 5 flags only the rank invariants: a distinguisher when ρ < b, and a ceiling when ρ < min(a, b). They differ
  for wide maps.
- **Three statements were attributed to the negative-result note that it does not make.** The 144 failing basis
  products and 76 = 16 + 6·10 are now this note's own self-tested facts. The note derives message recovery but reports
  no executed run, and the text now says "derives".
- **§3.5 misattributed the second parameter set's failure.** The note it cites gives 2^167 from hybrid attacks on the
  weight-64 sparse secret, with primal uSVP at 2^254. Only the first set (2^51) fails on its modulus-to-noise ratio.
  The NTRU cross-reference, Limitations, this README and the tool docstring are corrected to match. This error was
  already in the first draft.
- **Scoped claims.**
  - "Necessary, not sufficient" now reads "necessary for a uniform-matrix argument".
  - A ceiling reduces recovery to dimension ρ, which is fatal here (ρ = 76) but not in general.
  - "Sound" is now "no attack is known".
  - "Indistinguishable" is now "by its rank".
  - Proposition 2's hypothesis is stated (col(D_k) ⊆ col(D), with D_k's rows independent of k).
  - Corollary 1 also covers matrices with independent uniform module entries, the distribution SLWE's reduction
    assumed.
  - q = 4 294 977 961 is labelled as the negative-result note's instantiation of version 1's q ≈ 2^32.
- **Added:**
  - the two counting bounds (seed length × rows per block, ℓd; at most rd distinct columns);
  - the observation that the rank over Q bounds every modulus;
  - σ and the Cayley–Dickson convention, stated explicitly; the other common convention is the opposite algebra and
    gives the same ranks;
  - σ is not even a Fano collineation in the product's labelling;
  - the step from noise recovery to decryption;
  - a definition of "seed";
  - §5 entries for Rainbow and for weak Ring-LWE instances, and the McEliece dimension tests;
  - notation: `rank M` (not `rank A`), and D ∈ F^{g×b}.

**The tool**

- **It could print PASS on a collapsing design.** It compared rank D with D's own smaller dimension instead of the
  number of columns at the deployed size. Two collapsing designs passed: SLWE's shape with a generic full-rank
  256×112 design, and a row-seeded design at rank 256 of 320. The old uniform control passed only through the same
  comparison.
- **It trusted the design.** It now:
  - checks that every realized row lies in row(D_k), not only the rank;
  - checks that realize() is linear in the seeds;
  - checks minimality (the realizations at unit seeds must span row(D_k)) at the sizes it can afford;
  - rejects a full design whose rows differ from D_k's, and prints the every-size bound only when Proposition 2's
    hypothesis holds.

  The identity "design" for SLWE is now an ERROR.
- **Other fixes:**
  - wide maps get the right verdict;
  - composite moduli are an ERROR instead of a crash;
  - every crash exits 2, never 1 (FAIL);
  - several seed sets that are all deficient block a PASS.
- **Self-test additions:** a non-trivial passing design and regressions for every input above. It passes on Python
  3.8 and 3.13.
- **PDF:** list bullets now come from a Type 1 font. The text-companion bullet had been embedded as a bitmap.

## Scope

Defensive and methodological. The case study is the author's own withdrawn proposal; the ML-KEM design appears only as
a correctly designed control, which the tool passes. The tool analyses the structure of a construction you hand it; it
is not an attack on any deployed system. Passing the design-matrix rank test is **necessary for a uniform-matrix
security argument, not sufficient**: SLWE, with the structure removed, still failed on its parameters (the
modulus-to-noise ratio at the first set, hybrid attacks on the sparse secret at the second), which this tool does not
judge.
