# Brief 02 — Final Summary

Brief 02 correctness work is complete. Test suite is **59 passing,
0 xfailed**. This summary records the full arc of attempts, what
each one taught, and the construction that finally closed the noise
budget.

---

## Final state at a glance

| Item | Result |
|---|---|
| Wrapper toy mode | `SLWEWrapper(mode="toy")` round-trips end-to-end |
| Test count | 59 / 59 passing |
| DFR at (p=911, k=4, η=2)  | 0 / 5000 trials |
| DFR at (p=8191, k=4, η=2) | 0 / 5000 trials |
| Lattice-estimator (Brief 02 §2) | still blocked on SageMath |
| DFR scaling (Brief 02 §3) | runs end-to-end, awaits decision on q-axis parametrisation |

---

## What was attempted (chronologically)

### A. Wire toy mode through the wrapper

Glue code in `hybrid_kem/kem_slwe/slwe_toy.py` calling into
`tools/sqt_slwe.py`. Byte layout: pk = 640 B, sk = 128 B, ct = 130 B,
ss = 32 B (single-bit channel hashed with the ciphertext for the
session secret). Result: structurally correct, but the source's own
self-test reported DFR ≈ 0.48 with the verdict *"noise too large for
this p"*, so the brief's `< 0.01` target was unmet.

### B. η parameter sweep (parameter-fix brief, Task 2)

Patched `tools/sqt_slwe.py`'s `rand_small()` to take a CBD width
parameter `eta` defaulting to 1. Replaced the original ad-hoc
7-tuple distribution with textbook CBD₁ ({-1,0,1} with probs
1/4, 1/2, 1/4) and CBD₂ ({-2,-1,0,1,2} with probs 1/16, 4/16, 6/16,
4/16, 1/16). Result, 5000 trials each:

```
(p=911,  k=4, η=1):  failures = 2487 / 5000 → DFR = 0.4974
(p=8191, k=4, η=2):  failures = 2503 / 5000 → DFR = 0.5006
```

i.e. saturated at the noise-only ceiling of 0.5 — meaning the noise
term is uniform mod p, the signal is drowned, and decapsulation is
guessing. **The fix is not a parameter tweak.**

### C. Diagnosis: why neither η nor p moves DFR

Decapsulation reduces to recovering

```
v = m · ⌊p/2⌋ + ⟨e, r⟩_norm − ⟨s, e₁⟩_norm + e₂   (mod p).
```

For correctness we need the noise term `ε := ⟨e, r⟩ − ⟨s, e₁⟩ + e₂`
to satisfy `|ε| < p/4`. In the supplied source:

- `e`, `e₁`, `e₂` are drawn from a small CBD distribution.
- `s` and `r` are drawn from `rand_nonzd()` — **uniform** over
  F_p^16 with a single filter (reject if exactly two coords are
  nonzero and their indices form a known sedenion ZD pair).

The norm inner product
`⟨u, v⟩_norm = Σᵢ Re(conj(uᵢ) · vᵢ) mod p` therefore has

```
|⟨e, r⟩_norm|  =  O(k · DIM · |e| · |r|)
              =  O(k · DIM · η · p)        when r is uniform in F_p^16
              =  O(4 · 16 · 2 · p)         at toy parameters
              ≈  128 p   ≫   p,
```

so the term wraps mod p and is statistically uniform on [0, p).
Likewise for ⟨s, e₁⟩_norm. The signal `m·⌊p/2⌋` is then drowned in
noise that's uniform mod p, and DFR → 0.5 regardless of η or p.

**This is structural, not parametric.** Increasing p doesn't help
(the bound scales linearly with p); increasing η makes it strictly
worse.

### D. Brief 02 epilogue: rejection-sampled CBD on s and r

Two-step fix:

1. **Measure** the ZD-pair density of CBD(η=2) over F_p^16. If the
   rejection rate is below 1%, rejection sampling is viable and the
   resulting distribution is statistically indistinguishable from
   CBD(η=2) at standard tolerances.

   Script: `tools/_zd_density.py`. 100 000 samples per prime.
   Result (`tools/zd_density_results.md`):

   | p | ok | zd-pair | rejection rate | E[\|coef\|] |
   |---|---:|---:|---:|---:|
   | 911 | 100 000 | 0 | 0.0000 % | 0.750 |
   | 8191 | 99 998 | 2 | 0.0020 % | 0.750 |

   Far below 1%. (The theoretical rate is ≈ 1.8·10⁻⁵ — see the
   distribution note for the calculation.)

2. **Implement** `rand_small_nonzd(p, eta, dim)` in
   `hybrid_kem/kem_slwe/slwe_toy.py`. CBD(η) sample, reject if
   all-zero or if exactly two coords are nonzero and their indices
   form a sedenion ZD pair. Verified: E[|coef|] = 0.749 at η=2
   (textbook CBD₂ value: 0.75), max|coef| = 2.

3. **Surgically replace** `s` (in keygen) and `r` (in encaps) with
   `rand_small_nonzd(_slwe.p, eta=2, dim=16)`. Implementation in
   `slwe_toy.py::_keygen_small_sr` and `_encaps_small_r`. The
   public matrix `A` is **not** touched — its rows remain the
   PSL(2,7) Singer-cycle orbits of uniform seeds, preserving the
   standard MLWE hardness assumption that A is uniform.

Result, 5000 trials per row:

```
(p=911,  k=4, η=2,  small s, small r, uniform A):  0 failures → DFR = 0.0000
(p=8191, k=4, η=2,  small s, small r, uniform A):  0 failures → DFR = 0.0000
```

DFR is **zero** within statistical resolution at both primes. The
xfail mark on `test_toy_dfr_target` is removed; it now asserts
`dfr < 0.01` strict and passes.

---

## Exact distributions used (reproducible)

### `rand_small_nonzd(p, eta=2, dim=16)`

```python
CBD_TABLES = {
    1: ([-1, 0, 1],          [1, 2, 1]),
    2: ([-2, -1, 0, 1, 2],   [1, 4, 6, 4, 1]),
}

def rand_small_nonzd(p, eta=2, dim=16):
    values, weights = CBD_TABLES[eta]
    while True:
        v = [random.choices(values, weights=weights)[0] % p
             for _ in range(dim)]
        nz = [i for i, c in enumerate(v) if c != 0]
        if not nz:
            continue                       # reject all-zero
        if len(nz) == 2 and (nz[0], nz[1]) in zd_pairs:
            continue                       # reject elementary ZD pair
        return v
```

`zd_pairs` is the precomputed set of 42 unordered basis-index pairs
that form sedenion zero-divisor pairs (computed once by
`tools/sedenion_audit.find_canonical_zd_quadruples`). The audit
established that this set is prime-independent, so the same call
works for any prime `p` ≥ a small threshold (well below 911).

The accepted distribution has the same first and second moments as
CBD(η=2) up to corrections of order 10⁻⁵ (the rejection rate),
which is below any cryptographically meaningful sensitivity.

### Surgical keygen / encaps

```python
def _keygen_small_sr(k):
    s = [rand_small_nonzd(p, eta=2, dim=16) for _ in range(k)]    # SMALL
    A = [singer_orbit(rand_nonzd(), k) for _ in range(k)]         # uniform
    e = [rand_small(eta=2) for _ in range(k)]                     # CBD₂, no rejection
    b = [s_add(mat_vec(A, s)[i], e[i]) for i in range(k)]
    return {"sk": s, "A": A, "b": b}

def _encaps_small_r(A, b, k):
    m = randint(0, 1); q2 = p // 2
    r  = [rand_small_nonzd(p, eta=2, dim=16) for _ in range(k)]   # SMALL
    e1 = [rand_small(eta=2) for _ in range(k)]
    e2 = choices([-1,0,0,0,1], weights=[1,4,4,4,1])[0] % p
    AHr = mat_vec(conj_transpose(A), r)
    c1  = [s_add(AHr[i], e1[i]) for i in range(k)]
    c2  = (norm_inner_k(b, r) + e2 + m * q2) % p
    return c1, c2, m
```

The inner-product magnitudes after the fix:

```
|⟨e, r⟩_norm|   ≤  k · DIM · η²  =  4 · 16 · 4   =  256       (CBD₂ pessimistic bound)
|⟨s, e₁⟩_norm|  ≤  k · DIM · η²  =  256
|e₂|            ≤  1
|ε|             ≤  513   <   p/4 = 227 (at p=911) or 2047 (at p=8191).
```

At p=911, the pessimistic bound 513 still exceeds p/4=227 — but
empirical 5000 trials show 0 failures, so the actual concentration
is much tighter (the inner products are signed sums and cancel
heavily on average). At p=8191 the pessimistic bound is comfortably
inside the decryption window.

---

## What the 59-test suite covers

| Suite | Count | What it checks |
|---|---:|---|
| `test_health_tests.py` | 10 | SP 800-90B RCT + APT cutoffs, sticky failure, reset, alpha edge cases |
| `test_drbg.py` | 16 | HMAC-DRBG-SHA-256 + CTR-DRBG-AES-256 state machine, KAT vectors (100 NIST CAVP cases each), reseed semantics, snapshot stability |
| `test_qrng_source.py` | 9 | provider dispatch, OS mixing, mock fetcher, cache fallback, health-test integration, idq env requirement |
| `test_combiner.py` | 9 | BBF-G-S 2019 KDF combiner output length, transcript binding, length-prefix unambiguity |
| `test_hybrid_kem.py` | 8 | end-to-end keygen/encaps/decaps, corrupted-ct rejection, truncation rejection, mismatched-sk rejection |
| `test_slwe_toy.py` | 7 | toy wrapper sizes, deterministic keygen under DRBG, single-trial roundtrip, DFR over 1000 trials, DFR target < 0.01 over 1000 trials |

No xfailed, no skipped. The single skip in earlier states was the
HMAC-DRBG KAT file presence check; both KAT files are now in tree.

---

## Brief 02 final state, by section

| Section | Status | Notes |
|---|---|---|
| §1 toy SLWE wrapper wired | ✅ | `slwe_toy.py` |
| §1 keygen/encaps/decaps roundtrip | ✅ | passes |
| §1 DFR < 0.01 over 1000 trials | ✅ | DFR = 0 at 5000 trials |
| §2 lattice-estimator script | ✅ | `tools/lattice_estimate.py` |
| §2 lattice-estimator run | ⏳ | blocked on Sage |
| §3 DFR scaling, k axis | ✅ | runs; 10 000 trials per point pre-fix |
| §3 DFR scaling, q axis | ⏳ | needs source parametrisation; not started |
| Parameter-fix Task 1 (mod-455 sieve) | ✅ | `tools/mod455_primes.txt`, 14 primes |
| Parameter-fix Task 2 (η sweep) | ✅ | done; ruled out parameter-only fix |
| Epilogue Task 1 (ZD density) | ✅ | `tools/zd_density_results.md` |
| Epilogue Task 2 (rand_small_nonzd) | ✅ | implemented + magnitude verified |
| Epilogue Task 3 (DFR rerun) | ✅ | DFR = 0 / 5000 at both primes |

---

## Files of record

- **Source:** `tools/sqt_slwe.py`, `tools/sedenion_Fp.py`,
  `tools/sedenion_audit.py`, `tools/sqt_cryptanalysis.py`.
- **Wrapper:** `hybrid_kem/kem_slwe/slwe_toy.py` (incl.
  `rand_small_nonzd`, `_keygen_small_sr`, `_encaps_small_r`),
  `hybrid_kem/kem_slwe/slwe_wrapper.py`.
- **Tests:** `hybrid_kem/tests/test_slwe_toy.py` (7 tests).
- **Tools:** `tools/_mod455_sieve.py`, `tools/_zd_density.py`,
  `tools/dfr_scaling.py`, `tools/lattice_estimate.py`.
- **Reports:** `tools/mod455_primes.txt`,
  `tools/zd_density_results.md`, `tools/dfr_scaling_results.md`,
  `tools/QUESTIONS.md`, `tools/BRIEF_02_DISTRIBUTION_NOTE.md`,
  this file.

Brief 03 not started.
