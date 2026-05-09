# Brief 02 — Summary (post parameter-fix attempt)

## Test suite state

```
59 tests, 58 passing, 1 xfailed.
```

The xfailed test pins DFR < 0.01 at the toy parameters. Both the
parameter sweeps below were attempted in the parameter-fix follow-up
brief; neither moved the DFR off the noise-only ceiling. The xfail
therefore remains in place with an updated reason string.

## Brief 02 parameter-fix tasks

### Task 1 — mod-455 prime sieve

`tools/_mod455_sieve.py` enumerates primes `p ≡ 1 (mod 455)` in
[2000, 50000]. Output written to `tools/mod455_primes.txt`. 14 primes
found:

```
  2731    p-1 = 2 * 3 * 5 * 7 * 13
  8191    p-1 = 2 * 3^2 * 5 * 7 * 13
 11831    p-1 = 2 * 5 * 7 * 13^2
 14561    p-1 = 2^5 * 5 * 7 * 13
 16381    p-1 = 2^2 * 3^2 * 5 * 7 * 13
 17291    p-1 = 2 * 5 * 7 * 13 * 19
 20021    p-1 = 2^2 * 5 * 7 * 11 * 13
 21841    p-1 = 2^4 * 3 * 5 * 7 * 13
 22751    p-1 = 2 * 5^4 * 7 * 13
 24571    p-1 = 2 * 3^2 * 5 * 7 * 13 * 17
 (… see tools/mod455_primes.txt for the full list …)
```

Smallest mod-455 prime above 5000: **8191** (this is the prime the
brief's fallback path uses).

### Task 2 — η sweep at the toy

#### 2a. Patch `tools/sqt_slwe.py` to accept `eta`

Minimal edit to `rand_small()`:

```python
def rand_small(eta=1):
    if eta == 1:
        return [random.choices([-1, 0, 0, 1])[0] % p for _ in range(DIM)]
    if eta == 2:
        return [random.choices([-2,-1,0,1,2], weights=[1,4,6,4,1])[0] % p
                for _ in range(DIM)]
    raise ValueError(...)
```

Default flipped from a custom 7-tuple weighted distribution
(probabilities (1, 3, 6, 6, 6, 3, 1) / 26 over {-2..2}, range ±2) to
the textbook CBD₁ over {-1, 0, 1}. The caller surface
(`keygen / encaps` calling `rand_small()` with no args) is unchanged.

#### 2b. 5000-trial DFR at (p = 911, k = 4, η = 1)

```
failures = 2487 / 5000      DFR = 0.4974      elapsed = 14.3 s
```

DFR is at the noise-only ceiling. Brief's first conditional
("DFR < 0.01" → unmark xfail) does not fire.

#### 2c. Fallback: 5000-trial DFR at (p = 8191, k = 4, η = 2)

Switching p from 911 to 8191 (smallest mod-455 prime above 5000) and
widening η back to 2:

```
failures = 2503 / 5000      DFR = 0.5006      elapsed = 14.2 s
```

Still at the noise-only ceiling. Brief's parameter-fix escalation
path therefore exits without resolution.

## Why the parameter sweep doesn't move DFR

Decryption recovers `v = c2 − <s, c1>_norm = m·⌊p/2⌋ + ε  mod p`,
where the noise is

```
ε = <e, r>_norm  −  <s, e1>_norm  +  e2     (mod p)
```

In a standard LWE scheme **both** `e` (error) and `r` (encryption
randomness) are *small*. In the supplied SQT-SLWE source `r` is
sampled by `rand_nonzd()` — uniform over F_p^16 with the only filter
being "not a known zero divisor pair." So:

- `e` is small (a 16-vector with entries in {-1, 0, 1} for η=1, or
  {-2, …, 2} for η=2);
- `r` has entries uniform in [0, p);
- `<e, r>_norm = Σᵢ Re(conj(eᵢ)·rᵢ)` is a sum of 16 products, each
  product a small × O(p) = O(p), summed across 16 dims and across
  k ranks: O(k · DIM · p).

For (k=4, DIM=16, p=911) that's O(58 000) ≫ p, so the term wraps
modulo p and is uniform. The signal `m·⌊p/2⌋` is drowned and `v` is
indistinguishable from random — exactly the DFR ≈ 0.5 we observe.

Increasing η (more noise width on `e`) makes this strictly worse.
Increasing p alone is roughly neutral: the noise grows linearly in
p alongside the signal threshold (`p/4`), so the SNR doesn't change.

The fix is not a parameter tweak. The encryption randomness `r` has
to come from a small distribution. That is a **scheme change**, not
a parameter sweep:

- redefine `rand_nonzd()` to sample small (e.g. CBD η=2 over the
  16-vector, then reject if the result lies in a ZD pair), **or**
- restructure the protocol so `<e, r>_norm` is bounded by something
  much smaller than p. Both options live above the parameter-fix
  brief's scope.

Recorded as a raw finding; M. Gifford to interpret.

## Brief 02 final state, by section

| Section | Status |
|---|---|
| §1 toy SLWE wrapper wired | done |
| §1 keygen/encaps/decaps roundtrip test | passes structurally |
| §1 DFR < 0.01 | **fails**; xfail-marked with structural-cause reason |
| §2 lattice-estimator run | still blocked on Sage |
| §2 lattice-estimator script | ready |
| §3 DFR scaling, k axis | runs end-to-end; saturated at 0.5 (same root cause as §1) |
| §3 DFR scaling, q axis | requires source parametrisation (would not unblock §1) |
| Parameter-fix §1 (mod-455 prime sieve) | done; 14 primes in [2000, 50000] |
| Parameter-fix §2 (η=1 retry) | done; DFR = 0.497 |
| Parameter-fix §2 (η=2 at p=8191) | done; DFR = 0.501 |

## Files of record

- `tools/sqt_slwe.py` — source with `eta` parameter (default 1).
- `tools/mod455_primes.txt` — sieve output, 14 primes.
- `tools/_mod455_sieve.py` — sieve script.
- `tools/dfr_scaling_results.md` — 10 000-trial sweep over k.
- `hybrid_kem/kem_slwe/slwe_toy.py` — wrapper adapter.
- `hybrid_kem/tests/test_slwe_toy.py` — six structural tests + one
  xfail-marked DFR test.
- `tools/QUESTIONS.md` — open questions (now updated to point at the
  structural `r` issue rather than parameters).

## Recommendations (no code unilaterally written)

1. **Decision needed:** sample `r` from a small distribution. This
   changes the scheme's hardness assumption (small-secret +
   small-randomness LWE rather than small-secret-only); flag if you
   want the specific construction discussed first.
2. **Or** redefine the inner product. If `<·, ·>_norm` is replaced
   with one that's bounded by something other than p, the noise
   analysis changes and a small-r requirement may not be needed.
3. **Lattice-estimator** still blocked on Sage; nothing in the
   parameter-fix brief unblocks it.

Brief 03 not started, per the parameter-fix brief's last line.
