# Brief 02 — Summary (updated post-source-upload)

## What landed (current state)

- `tools/sqt_slwe.py`, `tools/sedenion_Fp.py`, `tools/sedenion_audit.py`,
  `tools/sqt_cryptanalysis.py` — the SQT-SLWE source uploaded by
  M. Gifford. Imports patched (`/home/claude` → `os.path.dirname(__file__)`).
  `sedenion_audit.py` script body moved under `if __name__ == "__main__"`
  so importing the helpers no longer runs the audit at import time.
- `hybrid_kem/kem_slwe/slwe_toy.py` — adapter that exposes the
  source's `keygen / encaps / decaps` through the byte-oriented
  `SLWEWrapper` API. Byte layout: pk = 640 B, sk = 128 B,
  ct = 130 B, ss = 32 B. Reseeds Python's global `random` from the
  caller's DRBG before each call.
- `hybrid_kem/kem_slwe/slwe_wrapper.py` — toy branch now real, full
  branch still raises `NotImplementedError` (pending p-scaling).
- `hybrid_kem/tests/test_slwe_toy.py` — six structural tests (all pass)
  plus an `xfail`-marked DFR-target test (currently fails by design,
  see below).
- `tools/lattice_estimate.py` — Sage-callable runner; unchanged
  since the previous brief.
- `tools/dfr_scaling.py` — runs end-to-end through the wrapper now;
  `tools/dfr_scaling_results.md` is the latest output.

## Test suite

```
59 tests, 58 passing, 1 xfailed.
The xfailed test pins DFR < 0.01 at (p=911, k=4) per the brief; it
fails because the supplied source self-reports DFR ≈ 0.48 at that
configuration ("noise too large for this p"). When the noise budget
is fixed, the test will start passing strict.
```

## What's true and what's not (raw findings)

### §1 toy SLWE wrapper — wired up, DFR target unmet by source

The supplied source is structurally correct: the adjoint property
`<A·s, r>_norm = <s, Aᴴ·r>_norm` holds (the source verifies this at
`__main__` and our wrapper relies on it for decryption), the Singer
Z₇ orbit preserves the 42 cross-interface ZD pairs, and the Cayley-
Dickson-built sedenion algebra has the expected 84 ZD-quadruple
structure (sedenion_audit confirms).

What does **not** work as shipped is the noise budget at (p=911, k=4):
the cumulative noise routinely exceeds p/4 = 227, so decapsulation
fails with probability ≈ 0.48. That is a property of the chosen CBD
weights and small-prime size, not of our wrapper. Both my own DFR
measurement (0.464 at 1000 trials, 0.49 at 1000 trials in the scaling
sweep) and the source's own self-test (0.480) agree.

I deliberately did not retune the source. Two natural fixes are
listed in `tools/QUESTIONS.md`; both require explicit sign-off
because they change the scheme's parameters.

### §2 lattice-estimator — still blocked on Sage

No change. `tools/lattice_estimate.py` is ready for a Sage run; the
parameter sets and assumptions are documented inline. Until Sage is
available the script does not produce numbers.

### §3 DFR scaling — runs, result is degenerate

The k axis is exercised at k ∈ {4, 8, 12, 16}, q = 911 fixed (the
source hardcodes p=911). DFR is saturated near the 0.5 noise-only
ceiling for every k:

| k | failures | trials | DFR |
|---|---:|---:|---:|
| 4  | ~498 | 1000 | 0.498 |
| 8  | ~460 | 1000 | 0.460 |
| 12 | ~496 | 1000 | 0.496 |
| 16 | ~487 | 1000 | 0.487 |

Linear fit: log₂(DFR) ≈ 0.000·k − 1.05 — i.e. no slope. The 10000-
trial sweep is queued (~12 minutes wall clock); same qualitative
answer expected, narrower error bars only. **No useful scaling
information is extractable at this prime** because the per-trial
DFR is at the noise-only ceiling regardless of k. Lowering DFR at
k=4 (i.e. fixing §1) is a prerequisite.

### §3 q-axis is the deeper blocker

The brief specifies *"q ≈ 2^24 for upper sizes"*. The source has
`p = 911` as a module-level global with a comment that the mod-455
property (p ≡ 1 mod 5,7,13) is required for full PSL(2,7) symmetry.
Changing p without preserving that property would silently break the
scheme; preserving it requires picking a specific mod-455 prime in
the desired magnitude range. I have not done that; it's a scheme
change, not a wrapping change.

## What surprised me

- The source ships with self-acknowledged DFR ≈ 0.48. Its `__main__`
  prints the failure message verbatim and lists "CBD parameter
  optimization: DFR target 2^-128" as a follow-up. The brief was
  presumably written assuming the noise budget was fine — that
  assumption doesn't hold at the parameters in source.
- The Singer Z₇ orbit construction in `sqt_slwe.py` does work and is
  consistent with the audit in `sedenion_audit.py` (the same Z₇ ⊂
  PSL(2,7) acts as a symmetry on the 42 cross-interface ZD pairs).
  This part is solid; the DFR issue is downstream of it (it's about
  noise sizing, not algebraic structure).
- Brief 03 / Task 2 separately found that the *NTT prime* 3329 has
  no Z₇ subgroup (`7 ∤ 3328`). So the SQT-SLWE Z₇ structure (which
  lives over F_911 with `911 = 2·5·7·13 + 1` having Z_7) does not
  port directly to the ML-KEM ring. That's a separate story from
  Brief 02 but worth flagging for the next brief that wants both
  layers to talk to each other.

## Worth revisiting

- **Re-tune the toy.** Either tighten the CBD error to a narrower
  distribution or jump p to a larger mod-455 prime. Either gets DFR
  below 0.01 at k=4 and unblocks the §3 scaling.
- **Parameterise p in `sqt_slwe.py`.** Today p is a module global;
  exposing it as an argument lets the DFR-scaling tool sweep both
  axes the brief asks for.
- **Wire up `sqt_cryptanalysis.py`.** The uploaded file is not used
  by the wrapper or by Brief 02 directly. It looks like Brief 03 / 04
  territory, so I left it in place for later.
- **Lattice-estimator on a Sage box.** Drop `tools/lattice_estimate.py`
  on a Sage machine and commit `tools/lattice_estimate_results.md`.

## Definition of done — checklist

- [x] §1 toy wrapper wired
- [x] §1 keygen/encaps/decaps roundtrip test (passes structurally)
- [ ] §1 DFR < 0.01 over 1000 trials — **fails by design at supplied
      parameters; xfail-marked**
- [ ] §2 lattice-estimator run — still blocked on Sage
- [x] §2 results script written; awaits Sage
- [x] §3 DFR scaling — runs; result is "DFR ≈ 0.5 across k", no
      meaningful slope
- [x] `tools/QUESTIONS.md` — updated
- [x] `tools/BRIEF_02_SUMMARY.md` — this file
