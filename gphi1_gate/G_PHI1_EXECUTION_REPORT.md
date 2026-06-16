# Gate G-Φ1 — Execution Report

**Date executed:** 2026-06-16 · **Pre-registration:** `G_PHI1_PREREGISTRATION.md`
(filed June 15 2026, ledger V4.39 CANONICAL) · **Class:** gate execution (Part V
result; not promoted to body) · **Instrument:** the rebuilt MV-G1 soft-disk GP
solver (`gz1_core.py`, the same instrument as G-ζ1 Phase 1–2). numpy/scipy only.

**Eddington guard honoured:** Φ = 2π − φ²/(8π²) = 6.25003 appears in exactly one
file, `compare.py` (Step 6), run after Steps 1–5 were computed and frozen to
`gphi1_measurements.json`.

## VERDICT: **INCONCLUSIVE — registered premise falsified.** No arm (A/B/C) assigned.

The pre-registration's structural premise — that the MV-G1 single-vortex profile is
tanh-like, healing to a ρ₀ bulk with an interior inflection near r = 0.931ξ at
ρ/ρ₀ ≈ 1/3 — is contradicted by the actual ground state. The registered
inflection-point rate probe is therefore ill-posed for this system, and the
mechanical Step-6 arm rests on a window-boundary artifact (see below). Recorded per
auditor decision of 2026-06-16.

## Measurement (Steps 1–5, Φ-free)

| step | quantity | result | note |
|---|---|---|---|
| 1 | μ (rectangular 2×2 supercell, 224×388, dx=0.013, PBC) | 55.946 | matches R1/G-ζ1 exactly |
| 1 | GP residual | 2.3e-3 | a* locked at 1.4576 by commensurate box |
| 2 | void centre | (0.000, 0.842) | triangle-centre min-density point |
| 2 | ρ_void | 0.0081 | ≈ 0 ✓ (good vortex core) |
| — | ρ_max | 8.01 | strongly-modulated **droplet crystal** |
| 3 | radial profile | recorded 0→3ξ step ξ/20, 24 angular bins | extended to 5.5ξ for the premise check |
| 4 | max\|dρ/dr\| in registered [0,3ξ] | r = 3.000ξ (**window boundary**) | profile convex throughout — no interior inflection |
| 5 | rate_actual = −ln(ρ(3ξ)/ρ₀)·(2ξ/a*) | 0.2013 | = density at the 3ξ cutoff, **not** an inflection |

**Convention (logged, HARD-RULE choice):** ξ = 1/√(2g) = 0.150756, the GP healing
length that makes the pre-registered tanh result exact (rate_tanh = ln3·(2ξ/a*) =
0.227, r_inflect_tanh = 0.931ξ = 0.141R). 2ξ/a* = 0.206855. Not tuned to any
outcome.

## Two-leg verification (required before reporting)
- **Leg (a)** analytic 2nd-derivative root of a smoothing-spline fit: r_inflect =
  3.000ξ (agrees with finite-difference to <0.1%).
- **Leg (b)** independent oblique primitive-cell GP solver (different discretisation,
  n=160): r_inflect = 3.000ξ, ρ_void = 0.0081.
- **|rect − cell|/rect = 0.00%** (≪ 5% requirement). ✓ Both legs agree — and both
  hit the window boundary, confirming the artifact is physical, not numerical.

## Why the premise is falsified (the decisive evidence)
| probe | tanh prediction | measured | factor |
|---|---|---|---|
| ρ/ρ₀ at r = 0.931ξ | 0.333 | **0.0154** | ~22× emptier |
| location of true inflection | 0.931ξ | **4.15ξ** | 4.5× farther out |
| ρ/ρ₀ at the true inflection | 0.333 | **1.34** (>1) | overshoots ρ₀ |

The soft-disk vortex core is far wider and emptier than tanh (the finite range R=1
≫ ξ=0.15 sets the core scale, not ξ). The density rises monotonically from
ρ_void≈0 straight past ρ₀ to the droplet peak (ρ_max=8) — there is **no ρ₀
plateau**, so a "single vortex in uniform bulk" picture does not apply. The genuine
inflection lies on the approach to the droplet peak at ρ>ρ₀, where the registered
−ln(ρ_inflect/ρ₀) rate is negative (formula breaks down).

## Eddington step (Step 6, mechanical — superseded)
Φ = 6.25003, 1/Φ = 0.16000, rate_tanh = 0.227. Feeding the literal Step-5 value
(0.2013, the 3ξ-cutoff density) gives gap_to_tanh = 0.113, gap_to_target = 0.258,
fraction_closed = 0.38 → mechanical **ARM C**. This is **superseded**: it is the
density at an arbitrary window cutoff, not a compounding rate at an inflection, so
it carries no physical meaning here.

## What this settles / does not settle
- **Settles:** the tanh single-vortex approximation is *qualitatively* wrong for the
  MV-G1 droplet crystal (not "accurate near the core" — ARM B is firmly rejected).
  The soft-disk correction is large, not perturbative.
- **Does not settle:** whether the MV-G1 GP structure closes the 28% gap to 1/Φ.
  The registered inflection-rate probe cannot answer this for a droplet-crystal
  ground state. A corrected probe is needed.
- The multiplicative-vs-additive compounding determination (R1, prior session) is
  untouched, as the pre-registration notes.

## Recommended follow-on (re-pre-registration)
Define a compounding-rate probe that is well-posed for a droplet crystal — e.g. the
density at a *fixed geometric fraction* of the void-to-peak separation, or a
log-slope integrated across one tube-diameter, rather than the tanh inflection
point. Re-register before recomputing. M.BRIDGE remains the open structural channel.

## Proposed Master Ledger Part V row (for auditor fold-in; **ledger not edited here**
— canonical V4.39 is not in this repo)
> **G-Φ1** | 2026-06-16 | *Inconclusive — premise falsified* | MV-G1 vortex profile
> is a droplet-crystal core (ρ_void≈0, ρ_max=8), not a tanh vortex healing to ρ₀;
> ρ(0.931ξ)/ρ₀ = 0.015 vs tanh 0.333; no interior inflection in [0,3ξ]; registered
> rate probe ill-posed. ARM B rejected; gap-to-1/Φ undetermined by this probe.
> Two-leg agree 0.00%. Cites `G_PHI1_PREREGISTRATION.md` (2026-06-15). | not folded
> to body.

*Files: `measure.py` (Steps 1–5 + two-leg, Φ-free), `compare.py` (Step 6,
Eddington), `gphi1_measurements.json`, `gphi1_verdict.json`, `gz1_core.py`
(instrument). MANIFEST.md5 + tarball alongside.*
