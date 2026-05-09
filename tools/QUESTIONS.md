# Brief 02 — Open Questions / Blockers (updated)

Tracking what was blocked, what unblocked, and what remains.

## 1. Toy SLWE wrapper (Brief 02 §1) — UNBLOCKED, BUT DFR TARGET NOT MET

**Unblock:** the user uploaded `tools/sqt_slwe.py`, `tools/sedenion_Fp.py`,
`tools/sedenion_audit.py`, and `tools/sqt_cryptanalysis.py` to complete
the brief. The wrapper now dispatches `mode="toy"` to the real SQT-SLWE
construction (sedenion algebra over F_911, PSL(2,7) Singer-orbit
public matrix, conjugate-norm inner product). Glue code lives in
`hybrid_kem/kem_slwe/slwe_toy.py`; tests in
`hybrid_kem/tests/test_slwe_toy.py`.

**What's wired up:**
- structural roundtrip: pk = 640 B, sk = 128 B, ct = 130 B, ss = 32 B.
- DRBG-driven Python `random` reseeding so the entropy layer flows
  through to keygen / encaps.
- single-bit per call; wrapper-level shared secret is
  `SHA256(m_bit || ct)` so both sides match iff `m_dec == m_bit`.

**What still fails:** The brief asks DFR < 0.01 over 1000 trials. The
supplied source's *own* self-test reports DFR ≈ 0.48 with the explicit
verdict *"FAIL — noise too large for this p"* and *"Noise exceeds
threshold p/4 = 227"*. We measure the same thing through the wrapper:

```
1000 trials at (p=911, k=4):  DFR ≈ 0.48 ± 0.03
1000 trials at (p=911, k=8):  DFR ≈ 0.50
1000 trials at (p=911, k=12): DFR ≈ 0.50
1000 trials at (p=911, k=16): DFR ≈ 0.49
```

i.e. saturated near the noise-only ceiling of 0.5. The
`test_toy_dfr_target_xfail` test is checked in marked `xfail` with the
above as the reason; if/when the source's noise budget is fixed it
will start passing strict.

**Sub-question still open:** the source's `__main__` block
recommends *"CBD parameter optimization: DFR target 2^-128"* and
*"Scale: k=32, p = large mod-455 prime (≥2^32)"* as next steps. Both
require touching the source. Choices to unblock < 0.01:

1. Tighten `rand_small()` to {-1, 0, 0, 0, 1} (current: ±2 with
   non-trivial weight) at the same p.
2. Increase p to a larger mod-455 prime (e.g. 39_551 = 87·455+1,
   or jump to ≥ 2^16). Requires modifying the module-level `p` in
   `tools/sqt_slwe.py` (and equivalently in `sedenion_audit`).
3. Both.

I have **not** touched the supplied source's noise distribution or
prime — the brief says don't paper over, and silently retuning these
without sign-off is exactly the kind of paper-over the brief warns
against. Flag preference and I'll do it.

## 2. Lattice-estimator integration (Brief 02 §2) — STILL BLOCKED

Sage is still not available on this host. `tools/lattice_estimate.py`
is wired and parameter-set-correct; it produces real numbers when run
under SageMath with the estimator on `sys.path`. No change since the
previous version of this file. The sub-question about literature-only
substitute numbers is still pending sign-off.

## 3. DFR scaling (Brief 02 §3) — UNBLOCKED, RESULT IS DEGENERATE

`tools/dfr_scaling.py` now runs end-to-end through the toy wrapper.
Output written to `tools/dfr_scaling_results.md` (10000 trials per
point, k ∈ {4, 8, 12, 16}, q = 911 throughout because the source
hardcodes p=911).

The result is that DFR sits at the noise-only ceiling of 0.5
across all four points. There is no usable slope to fit (slope ≈ 0,
intercept ≈ −1.0 bit). This is a direct consequence of §1's noise
budget overflow: the scheme is decoding noise, not signal, at every
k on offer. **Fixing §1 (lower DFR at k=4) is a prerequisite for §3
producing meaningful scaling data.**

The brief's text reads *"keep q ≈ 2^24 for upper sizes to keep
runtime bounded"*. Doing that requires the source to accept p as a
parameter. The supplied source has p as a module-level global with
the comment *"mod-455 prime: p ≡ 1 (mod 5,7,13) → full PSL(2,7)
symmetry"*; switching p without verifying the mod-455 condition would
silently break the PSL(2,7) structure that the scheme is built on.
Candidate primes that preserve mod-455 and reach ~2^24:

- ~2^16: 65_521, 65_447, ...
- ~2^24: 16_776_991, 16_777_141, ... (need to filter by `p ≡ 1 mod 455`).

Decision needed: do we want the source parametrised in p, or do we
keep the toy at 911 and accept that DFR scaling at this prime is
just degenerate?
