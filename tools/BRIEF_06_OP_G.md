# Brief 06 — Singer A matrix rank restoration (OP-G)

> *T1 = measured fact (script reproducible from
> `hybrid_kem/kem_slwe/slwe_toy.py` + `tools/gs_profile.py` +
> `tools/singer_rank_demo.py`).
> T2 = structural argument used to interpret the measurement.
> No prediction or extrapolation is labelled T1.*

## Headline

**Path A passes** all three checks at `(k = 32, p = 8191)`. The wrapper
now uses `singer_a_randomized` for production keygen. **Test suite is
70 passing, 0 xfailed** (was 69; +1 from the randomised-rank test
added in Task C1).

| Check | Path A result |
|---|---|
| F_p-rank of `A_F` at δ=1, k=32 | **512** (full) [T1] |
| Singer column period after randomisation | **broken** (no period < 512) [T1] |
| Sedenion homomorphism-failure rate at k=4 | **100%** [T1] |
| Sedenion homomorphism-failure rate at k=32 | **100%** [T1] |
| DFR over 1000 trials at p=911, k=4, randomised A | **0/1000** [T1] |

## Path A summary

`hybrid_kem/kem_slwe/slwe_toy.singer_a_randomized(k, p, seed, delta)`
constructs `A` as `SingerBase + δ · UniformPerturbation`
sedenion-componentwise. With `δ = 1` the resulting `A_F` is full
F_p-rank at `k = 32`, the column-period of pure Singer (= 112)
disappears, and the wrapper's downstream DFR test stays at 0/1000.
The wrapper's production keygen (`_keygen_small_sr`) was updated to
call `singer_a_randomized` instead of the original
`singer_orbit`-only construction.

## Honesty caveat (T2)

Over `F_p` there is no notion of "small δ": any nonzero δ multiplied
by a uniform random matrix is itself a uniform random matrix, up to
a fixed offset that — when the offset is itself random — is also
uniform. Therefore at `δ = 1`, the resulting `A` is
distributionally indistinguishable from a uniformly random sedenion
matrix.

What this means in plain terms:

- **The PSL(2, 7) symmetry that the original construction put into
  `A` is gone** in Path A's output. The brief acknowledges this as
  an acceptable trade-off ("the PSL(2,7) symmetry in the matrix
  entries will not be preserved exactly").
- **Path A at δ = 1 is operationally equivalent to Path B**
  (uniform-random `A`). The naming "randomised Singer" describes
  the implementation (we explicitly construct SingerBase and then
  add to it), not the resulting distribution. A future caller who
  cared about the PSL(2, 7) structure would need a *structured*
  perturbation (e.g., perturb only the seed, not the orbit pattern)
  rather than a uniform one. The brief's Path A2 fallback ("if the
  shield holds at k=4 but fails at k=32, document this explicitly
  and proceed to Task A3 with a structured perturbation that adds
  randomness only to diagonal blocks") was not triggered, because
  the shield test outcome doesn't depend on `A` (see next note).

## On the homomorphism-failure test (T2)

The test in `tools/sqt_cryptanalysis.py` measures
`L_{a*b} ≠ L_a · L_b` over **uniformly random sedenions `a, b`**.
It is a property of the sedenion algebra's multiplication, not of
the public matrix `A`, so its outcome is invariant under any
choice of `A` or `k`. In particular:

- The brief's framing "the perturbation interaction may only
  manifest at the operational scale; the k=4 test alone is
  insufficient" assumes the test depends on `A`. It does not.
- Reporting the failure rate at "k=4" and "k=32" gives the same
  number both times (100%), as the script confirms; including both
  rows in the table is documentation-parity with the brief, not
  evidence that two distinct things were measured.

A test of the algebraic shield as it interacts with `A` would
need a different design (e.g., look at how `A` composes with the
left-multiplication structure on the secret space). That's not in
scope for Brief 06; flagged here so a future brief that wants
"shield ⊕ public-matrix interaction" doesn't reuse this test
expecting it to vary.

## §1. Path A details (T1)

### A1. Randomised Singer construction

```python
def singer_a_randomized(k, p, *, seed=None, delta=1):
    singer_part = [singer_orbit(rand_nonzd(), k) for _ in range(k)]
    A = []
    for i in range(k):
        row = []
        for j in range(k):
            perturb = [random.randrange(0, p) for _ in range(DIM)]
            entry = [(singer_part[i][j][c] + delta * perturb[c]) % p
                     for c in range(DIM)]
            row.append(entry)
        A.append(row)
    return A
```

At `δ = 1`, `(k = 32, p = 8191)`, single sample with seed `0xb06`:

```
F_p-rank      = 512   (full)
column period = None  (no period < 512 over F_p)
```

[T1] Both checks reproducible from `python3 -m pytest
hybrid_kem/tests/test_ring_audit.py
::test_singer_a_randomized_fp_rank_full`.

### A2. Algebraic-shield test

```
k= 4: hom-failure rate = 100% (avg differing entries: 209.9/256)
k=32: hom-failure rate = 100% (avg differing entries: 210.0/256)
```

[T1] Run with the inline replication of `sqt_cryptanalysis.py`'s
test in this brief. The same 100% rate would hold for any `A`
(see §"On the homomorphism-failure test").

### A3. DFR at k=4 with randomised A

```
1000 trials, p=911 (toy default), k=4, randomised A:
failures = 0 / 1000   →   DFR = 0.0000
```

[T1] Run via the wrapper which now uses `singer_a_randomized` in
its keygen. Same result as before the change (the original DFR
also went to 0 once `s` and `r` were drawn small in Brief 02
epilogue; randomising `A` does not affect that result because
`A`'s distribution wasn't the noise-budget bottleneck).

## §2. Tasks C1–C3

### C1. CI tests

- Renamed `test_singer_a_fp_rank_at_most_112` →
  `test_singer_pure_a_fp_rank_at_most_112`. The vulnerability is
  documented and pinned, not deleted.
- Added `test_singer_a_randomized_fp_rank_full` confirming the
  Path A fix.
- Kept `test_random_a_fp_rank_full_at_k32` (Path B baseline,
  also valid as the limit Path A converges to at δ ≥ 1).

The vulnerability test and the fix test now coexist:

```
hybrid_kem/tests/test_ring_audit.py::test_singer_pure_a_fp_rank_at_most_112  PASS
hybrid_kem/tests/test_ring_audit.py::test_singer_a_randomized_fp_rank_full    PASS
hybrid_kem/tests/test_ring_audit.py::test_random_a_fp_rank_full_at_k32        PASS
```

### C2. Master doc

Original `SLWE_Prime_Master_v1.md` is **not present in this repo**
and never has been across Briefs 02–06 — same blocker that's been
flagged before. I created a stub at `tools/SLWE_Prime_Master_v1.md`
with the OP-G entry per the brief; entries for OP-A through OP-F
should be filled in from the canonical source if/when it lands.

### C3. Demo

`tools/singer_rank_demo.py` is parameter-driven, pure CPython, and
contains no SLWE-specific imports. It illustrates the rank-deficit
pattern for any `(orbit_length, field_dimension, k, p)` and shows
that the column-period observation is a structural identity
independent of the algebra `A` is being interpreted in. Sample
output at the SLWE parameters:

```
$ python3 tools/singer_rank_demo.py --orbit 7 --dim 16 --k 32 --p 8191

orbit length L            = 7
field dimension d         = 16
module rank k             = 32
prime p                   = 8191
matrix shape (n x n)      = 512 x 512
column period             = 112
structural rank ceiling   = 112      (= L * d)
  ceiling matches period? = yes
empirical F_p-rank        = 16
empirical rank deficit    = 496 (out of 512)

The column period equals L*d = 112, so column rank ≤ 112 for any
embedding that respects A_sed[:, j] = A_sed[:, j+L].
```

(The empirical rank of 16 here is from the demo's deliberately
simple "one row of d-block per A-entry" embedding; under the
left-multiplication embedding used in `tools/sqt_slwe.py` the
empirical rank reaches 76 — see Brief 05 for the SQT-specific
case.)

## §3. CI-protected vs documentation-only

CI-protected (assertions in `hybrid_kem/tests/test_ring_audit.py`):
**(a)** Pure Singer column period is exactly 112 at k=32; **(b)**
pure Singer F_p-rank ≤ 112; **(c)** randomised Singer at δ=1 is
F_p full rank (= 512); **(d)** uniform random A is F_p full rank
(= 512).

Documentation-only (in this report and in `tools/BRIEF_05_GS_PROFILE.md`):
the empirical Singer F_p-rank value 76 (sample-specific, not
structural); the homomorphism-failure rate 100% (algebra-only,
inferred from Brief 06's run); the DFR 0/1000 with the new `A`
construction; the equivalence of Path A and Path B over F_p
(structural, T2). The cryptanalytic interpretation that
"effective attack dimension drops from 512 to 112" remains
documentation-only — no exploit script lives in this branch.

## §4. Stop conditions encountered

None. Path A succeeded on all three checks; Path B was not
activated. The 30-min limit was not approached (rank check ~12 s,
shield test ~30 s, DFR ~3 s).

## §5. Reproducibility

```bash
pip install numpy cysignals fpylll       # one-time
python3 tools/singer_rank_demo.py --orbit 7 --dim 16 --k 32 --p 8191
python3 tools/gs_profile.py --k 32 --p 8191        # ~25 s; OP-F context
pytest hybrid_kem/tests/test_ring_audit.py -v       # ~30 s; 11 assertions
pytest hybrid_kem/tests/ -q                          # full suite, ~25 s
```

Brief 07 not started.
