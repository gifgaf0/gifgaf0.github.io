# SLWE Prime Master v1 — open-problems log

> **Stub created by Brief 06.** The original `SLWE_Prime_Master_v1.md`
> referenced by Briefs 02–06 was not present in this repository at any
> point during the work. This file is a placeholder so OP-G has a home;
> entries for OP-A through OP-F should be filled in from the canonical
> source if/when it lands.
>
> Cross-references in this branch:
> - OP-B (lattice-estimator on the toy parameters): `tools/QUESTIONS.md`,
>   `tools/lattice_estimate.py`, `tools/lattice_estimate_results.md`.
> - OP-C (DFR scaling): `tools/dfr_scaling.py`,
>   `tools/dfr_scaling_results.md`.
> - OP-D (sedenion ODLP): `tools/BRIEF_04_ODLP_REPORT.md` —
>   **closed**, security is lattice-only by the Cayley-Dickson
>   norm-form identity.
> - OP-F (Singer-orbit GS profile): `tools/BRIEF_05_GS_PROFILE.md` —
>   identified the rank deficit that this OP-G entry then closes.

## OP-G — Singer-orbit `A` matrix rank deficiency at `k = 32`

**Status (Brief 06): resolved by Path A (randomised Singer).**

### Problem statement

The Module-SLWE public matrix `A` was constructed in
`tools/sqt_slwe.py` as ``A[i] = singer_orbit(seed_i, k)`` —
each row is a length-``k`` Z₇ Singer-cycle orbit of an
independently sampled seed. Brief 05 (commit `0b07af7`) showed
that this construction is rank-deficient at `k = 32`:

- The Z₇ Singer cycle σ has order exactly 7.
- For `k = 32`, ``A_sed[:, j] = A_sed[:, j + 7]`` because
  ``σ^{j+7} = σ^j``.
- After flattening to the F_p left-multiplication embedding,
  the column equality lifts to ``A_F[:, c] = A_F[:, c + 112]``
  (verified directly as integer column equality).
- Hence `column rank(A_F) ≤ 7 · 16 = 112` against a nominal
  shape of `512 × 512`.
- Empirical F_p-rank at one sample: 76 (extra collinearities
  beyond the 112 ceiling).
- Effective primal-attack lattice dimension drops from 512 to
  ≤ 112; an attacker who notices `A_F[:, j] == A_F[:, j+112]`
  reduces the SLWE problem to a ≤ 112-dim quotient where BKZ
  work that would be infeasible at 512 is routine.

### Root cause

A single-row construction whose period (7) is shorter than
the module rank (32). Any time `k > L` (where `L` is the
Singer cycle's order), the construction repeats columns
`⌈k/L⌉` times.

### Fix (Path A: randomised Singer)

`hybrid_kem/kem_slwe/slwe_toy.singer_a_randomized(k, p,
seed, delta)` returns ``SingerBase + δ · UniformPerturbation``,
sedenion-componentwise mod `p`. At `δ = 1`:

- F_p-rank of the resulting `A_F` is 512 (full).
  ([T1, `test_singer_a_randomized_fp_rank_full`])
- Column period is broken — no `L < n` makes
  `A_F[:, j] == A_F[:, j + L]` for all `j`.
- Sedenion homomorphism-failure rate (the
  non-associative algebraic shield) remains at 100% at
  both `k = 4` and `k = 32` — the shield is a property of
  sedenion multiplication, not of `A`, so it is preserved
  trivially. ([T1])
- DFR over 1000 trials at `(p = 911, k = 4)` is 0/1000.
  ([T1])

The wrapper's production keygen (`_keygen_small_sr` in
`slwe_toy.py`) now calls `singer_a_randomized` instead of
the original `singer_orbit` construction.

### Honesty note about Path A

Over `F_p` there is no "small δ": any nonzero δ multiplied
by a uniform random matrix is itself a uniform random
matrix (up to a fixed offset, which is also uniform when
the offset is itself random). Therefore at δ = 1 the
resulting `A` is distributionally indistinguishable from
a uniformly random sedenion matrix.

What this means in practice:

- The PSL(2,7) symmetry that the original Singer construction
  put into `A` is gone.
- The "randomised Singer" naming is descriptive of the
  *implementation* (we construct SingerBase explicitly and
  add to it), not of the *distribution* (which is just
  uniform).

The non-associative algebraic shield — what
`tools/sqt_cryptanalysis.py` measures with the homomorphism
failure rate — does **not** depend on `A` at all. It is a
property of sedenion multiplication. So the shield is
preserved under any choice of `A`, including uniform
random. Path A therefore "preserves the shield" in a
trivial sense, and is operationally equivalent to Path B
(uniform-random `A` directly).

### Demonstrator

`tools/singer_rank_demo.py` is a parameter-driven script that
exhibits the rank-deficit pattern for arbitrary
`(orbit_length, field_dimension, k, p)` — no SLWE-specific
imports; readable by a lattice cryptographer with no SQT
context. Sample run at the SLWE parameters:

```
orbit length L            = 7
field dimension d         = 16
module rank k             = 32
prime p                   = 8191
column period             = 112
structural rank ceiling   = 112      (= L * d)
```

### CI tests pinning the result

- `test_singer_a_column_period_at_k32` — column period
  exactly 112 (vulnerability witness).
- `test_singer_pure_a_fp_rank_at_most_112` — pure Singer
  is rank-bounded (vulnerability witness).
- `test_singer_a_randomized_fp_rank_full` — Path A fix is
  full rank.
- `test_random_a_fp_rank_full_at_k32` — Path B baseline
  (uniform A) is full rank, useful as the "lower bound" of
  what Path A converges to at δ ≥ 1.

The vulnerability tests and the fix tests coexist by design;
the OP-G entry is a documented finding, not dead code.
