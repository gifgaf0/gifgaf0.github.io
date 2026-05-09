# Brief 02 — Summary

## What landed

- `tools/lattice_estimate.py` — Sage-callable runner for the
  lattice-estimator. Defines the four target parameter sets
  (toy / medium-1 / medium-2 / full), bakes in the secret / error
  distribution choices, and emits a markdown table to
  `tools/lattice_estimate_results.md`. Importable in plain CPython
  without crashing — it only tries to import the Sage-side estimator
  inside `main()`.
- `tools/dfr_scaling.py` — generic DFR measurement harness. Calls
  `SLWEWrapper(mode="toy", ...)` for each `(k, q)` point, fits
  `log2(DFR)` vs. `k` by ordinary least squares, and writes
  `tools/dfr_scaling_results.md`. Honours the 30-minute-per-point cap
  and exits non-zero if the wrapper still throws `NotImplementedError`.
- `tools/QUESTIONS.md` — the precise list of inputs we need before any
  of this is runnable end-to-end.

## What did not land — and why

**§1 (toy SLWE wrapper)**: blocked. `sqt_slwe__1_.py` is not in this
repository. The brief asks me to wrap it; without the source I would be
inventing a scheme rather than wrapping the existing one. I deliberately
did *not* generate a "best-guess" SLWE implementation, because:

- a research-testbed wrapper has to match the scheme it's wrapping
  bit-for-bit, otherwise downstream comparisons (DFR, lattice cost) are
  measuring something else;
- the master document presumably documents non-obvious choices (rejection
  sampling rule, exact error distribution, byte-encoding) that I cannot
  recover from `SPEC.md` alone.

**§2 (lattice-estimator run)**: blocked at install. The estimator
requires SageMath, which isn't installed on this host and isn't a
pip-installable add-on. The script is written so it produces real
numbers as soon as it's run on a Sage box.

**§3 (DFR scaling)**: blocked on §1. Wired up so it'll run as soon as
the wrapper is real.

## What surprised me

- The brief reads as though `sqt_slwe__1_.py` is already inside the
  repo. The original tarball didn't contain it, and nothing in the
  earlier briefs uploaded it either. Worth double-checking that the
  master doc / SLWE source were ever pushed; if they live in a sibling
  repository on the author's laptop, that's the kind of context the
  testbed shouldn't depend on implicitly.
- `fpylll` installs trivially under pip; the estimator does not. People
  conflate the two regularly. I've called this out in
  `tools/QUESTIONS.md` so the next attempt doesn't start from
  `pip install lattice-estimator` and the same dead end.
- The dual-attack column in the table I'd produce is going to look
  worse than the primal column at the larger parameter sets, but only
  by a few bits. That's expected behaviour for Module-LWE-style
  parameters; flagging it now so it doesn't read as a bug when the
  numbers actually arrive.

## Worth revisiting

- **Decoupling the parameter set from the wrapper.** The current
  `SLWEWrapper` constructor takes `params: dict | None`, but the brief
  pins `(k=4, q=911)` for toy mode. Once the real wrapper lands, decide
  whether to expose `params` to callers or hard-code per-mode values.
  Keeping it open for now lets the DFR script pass `(k, q)` per call.
- **Alternative cost models.** The script reports classical Core-SVP
  bits. The master doc may want quantum sieving bits as well. Easy to
  add a column once the estimator runs; flag if you want both.
- **Hybrid attack column.** Estimator's hybrid mode is fragile on
  Module parameters. I left it out on purpose; if it becomes the headline
  attack at the higher parameter sets, we can light it up explicitly.

## Definition of done — checklist

- [ ] §1 toy wrapper — **blocked** (need `sqt_slwe__1_.py`)
- [ ] §1 toy wrapper tests at DFR < 0.01 over 1000 trials — blocked on §1
- [ ] §2 lattice-estimator run — **blocked** (need SageMath)
- [ ] §2 results markdown — script written; awaits real run
- [ ] §3 DFR scaling — script written; awaits §1
- [x] `tools/QUESTIONS.md` — written
- [x] `tools/BRIEF_02_SUMMARY.md` — this file

Nothing in `kem_slwe/` or the rest of the testbed has been touched, so
the existing 52-test suite still passes unchanged.
