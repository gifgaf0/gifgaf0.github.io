# Generator-Induced Invariants in Lattice Public Keys

A methodological note and a runnable diagnostic, generalizing the rank collapse found in
the sedenion Module-LWE ("SLWE") negative result
(`audit_followup/closeout/step3/3b_slwe_eprint/`).

## The claim, in one line

A public key built by applying a **fixed family of linear maps to random seeds** is the
image of a single fixed *design matrix* `D`; it factors as `M = R·D`, so `rank M ≤ rank D`
for every instance size and every seed draw. If `rank D` is below the ambient dimension,
the key is distinguishable from random and recovery drops to dimension `rank D`. The
weakness is **generically invisible below the generator's saturation size**, which is why a
rank check run on too small an instance returns a clean result on a broken scheme.

## Contents

- `generator_induced_invariants_DRAFT_v1.md` — the first-draft note.
  - §2 the mechanism (theorem + two corollaries + the saturation principle);
  - §3 the SLWE case study, including why the scheme's own `k = 4` self-test missed the
    `76` ceiling;
  - §4 the diagnostic; §5 a taxonomy of same-shape historical breaks; §6 honest scope.
  - Reference list is **leads to verify** against primary sources before external use.
- `diagnostics/design_matrix_rank.py` — the §4 diagnostic, pure Python, no dependencies.

## The diagnostic

```bash
cd diagnostics

# Regression fixture: reproduces the SLWE note's Table 1 and rank N = 76 over
# F_911, F_2731, F_(2^31-1), and the first parameter set's q, across three seed sets.
python3 -I design_matrix_rank.py --self-test

# Full report: diagnoses the built-in SLWE scheme (FAIL, ceiling 76) and a
# uniform control (PASS), with the empirical saturation curve.
python3 -I design_matrix_rank.py
```

The self-test exits non-zero on any mismatch, so it doubles as a CI check pinned to the
published result.

To diagnose another construction, implement the `GeneratorScheme` interface
(`design_matrix()`, `realize()`, `ambient_rank()`, `random_seeds()`) and pass it to
`diagnose(...)`.

## Scope

Defensive and methodological. The case study is the author's own withdrawn proposal; the
NIST standards appear only as correctly-designed controls. The tool analyses the structure
of a construction you hand it — it is not an attack on any deployed system. The design-matrix
rank test is **necessary, not sufficient**: clearing it means only that this class of
weakness is absent (SLWE, with the structure removed, still failed on its modulus-to-noise
ratio — a separate matter this tool does not judge).
