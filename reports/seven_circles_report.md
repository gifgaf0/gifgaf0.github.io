# Seven Circles Probe — Cross-Ratio Distribution

**Date:** 2026-05-14
**Status:** T1 — exact enumeration, no statistical sampling
**Reproduces:** `tools/_seven_circles_source/scratch_seven_circles_experiment.md`
       (with one corrected count — see §2 and §5)
**Code:** `tools/seven_circles_probe.py`
**Tests:** `tools/test_seven_circles.py` (10/10 passing)
**Cited from:** `borromean_circumscription_derivation.md §5.2`,
       `paper/X1_cos18_address.md`

---

## §1 — Construction

**Torus parameters.** Canonical R = 3, r = 1.

**The seven natural torus circles** (verbatim from
`tools/_seven_circles_source/seven_circles_experiment.py`):

| Idx | Label        | Centre   | Radius                           | Value (R=3, r=1) |
|---:|---|---|---|---:|
| 1 | `1_outer`     | (0, 0)   | R + r                             | 4.000000 |
| 2 | `2_hole`      | (0, 0)   | R − r                             | 2.000000 |
| 3 | `3_spine`     | (0, 0)   | R                                 | 3.000000 |
| 4 | `4_tube_R`    | (R, 0)   | r                                 | 1.000000 |
| 5 | `5_geo_mean`  | (0, 0)   | √(R² − r²)                        | 2.828427 |
| 6 | `6_hept_in`   | (0, 0)   | (R − r)·cos(π/7)                  | 1.801938 |
| 7 | `7_wingtip`   | (0, y₀)  | \|y₀ + (R − r)\| with y₀ = Rr/(R−2r) | 5.000000 |

The wing-tip circle is the unique circle through (R, −r), (−R, −r),
(0, −(R−r)) — the closed form follows from setting the three radial
distances equal; undefined at R = 2r.

**The 40 chord positions.** A horizontal line at perpendicular
distance d from the origin (θ = 0), d sampled uniformly over
[0.1, 3.8] in 40 steps (`numpy.linspace(0.1, 3.8, 40)`). Each chord
intersects the seven circles in up to 14 points (2 per circle when
the chord cuts the disc). At each chord position the probe enumerates
**all 4-subsets** of the intersection points and computes the
projective cross-ratio along the chord parameter.

**What CR_tube measures.** For the §3 crystallographic-exclusion
check the construction restricts to two circles (spine and tube) and
computes two cross-ratios per chord: `CR_line` (chord-parameter
projective frame) and `CR_tube` (angular cross-ratio from the tube
centre via the tangent-half-angle projective parameter
`tan(α/2)`). Same definitions as `three_perspectives.py`.

**Matching.** Each cross-ratio (and its reciprocal) is compared to
each entry of the 23-constant curated library
`CURATED_CONSTANTS`, taken verbatim from
`tools/_seven_circles_source/seven_circles_tight.py`. A match is
recorded when the relative error is below **5 × 10⁻⁴ (0.05%)**.

**Counting convention.** A constant is credited with a "chord-position
hit" whenever at least one of that chord's 4-point cross-ratios
matches it. The headline figure for a constant `C` is therefore
`hits(C) / 40` — the fraction of chord positions where `C` appears.

---

## §2 — Main Result

```
cos 18° hits:  14 / 40   (35.00%)
```

Tied with √5/2 at 14/40; cos(π/7) at 13/40 just below.

Full distribution at the canonical parameters (R = 3, r = 1, 40 chord
positions, 0.05% tolerance), constants ranked by chord-position hits:

| Hits | Constant            | Value     | Description |
|---:|---|---:|---|
| 14 / 40 | `sqrt5/2`           | 1.118034 | t parameter |
| 14 / 40 | `cos(18deg)`        | 0.951057 | cos 18° = √(2+φ)/2 |
| 13 / 40 | `cos(pi/7)`         | 0.900969 | Klein triangle |
|  6 / 40 | `cos(2pi/7)`        | 0.623490 | 7-fold |
|  5 / 40 | `phi/2`             | 0.809017 | cos 36° |
|  4 / 40 | `arctan(1/sqrt2)`   | 0.615480 | Prop P.α |
|  4 / 40 | `void`              | 0.712840 | 1 − gap |
|  3 / 40 | `sin(36deg)`        | 0.587785 | sin 36° |
|  2 / 40 | `phi^-1`            | 0.618034 | 1/φ |
|  2 / 40 | `eps_3/eps_2`       | 2.787526 | Hales ratio |
|  2 / 40 | `pulsation`         | 0.094800 | pulsation amplitude |
|  2 / 40 | `gap`               | 0.287160 | 84 − cascade ratio |
|  1 / 40 | `phi^-2`            | 0.381966 | 1/φ² |
|  1 / 40 | `8/21`              | 0.380952 | Cheeger constant |

Aggregate counts at the canonical run:
- 11 495 cross-ratios computed
- 123 cross-ratio matches at 0.05%
- 14 distinct constants appearing at ≥ 1 chord position

cos 18° is at the top of the table (joint-top with √5/2). The
appearance is not a single chord-position artefact — it occurs at
35% of the swept positions, ~10× the null expectation under random
log-uniform sampling against the same library.

---

## §3 — Crystallographic Exclusion Check

Three-perspective check on the two-circle (spine + tube)
construction, sweeping (d, θ) over a 100 × 100 grid. 2060 chord
configurations with exactly 4 intersection points.

| Perspective | cos 18° hits at 0.05% |
|---|---:|
| CR_line (external projective frame) | 3 |
| CR_tube (angular from tube centre)  | 10 |
| **CR_tube / CR_line**               | **3.33** |

The ratio exceeds the brief's 3× threshold; cos 18° concentrates in
the local-curvature (tube) frame and is suppressed in the external
projective frame. Consistent with crystallographic exclusion of
pentagon symmetry from the p6m bulk: the pentagon appears in the
boundary geometry, not in the projective bulk.

---

## §4 — Identity Verification

```
cos(18°) = cos(π/10) = √(2 + φ)/2,    φ = (1 + √5)/2
```

| Form | Value (15 sig figs) |
|---|---|
| `cos(π/10)` direct        | 0.951056516295154 |
| `√(2 + φ)/2`              | 0.951056516295154 |

Identity verified to float64 precision (1e-12 tolerance).
Algebraic check: `2 + φ = (5 + √5)/2`, so `√(2 + φ)/2 = √(5 + √5)/(2√2) = cos(π/10)`.

This identity is independently verified in `tools/rho_derivation.py`
(commit `4d6b612`) where it appears as a load-bearing step of the
proton-radius prediction.

---

## §5 — Discrepancy from the v1 scratch claim

Brief 07's Definition of Done expected `cos18_hits == 27`, citing the
v1 scratch note `scratch_seven_circles_experiment.md` §R2 table:

> | cos(18°) = √(2+φ)/2 | 27 | 5-fold | previously UNMAPPED |

This count **does not reproduce** under the construction recorded in
the source `.py` files (vendored at
`tools/_seven_circles_source/`). The reproducing count at the
documented 0.05% tolerance, with the 23-entry CURATED_CONSTANTS
library, on the 40-position sweep, is **14/40**. No parameter
adjustment to force the brief's expected number was made; the brief
explicitly requires reporting the verified count and updating the
paper cite. v5 of `borromean_circumscription_derivation.md` §5.2 had
already revised the expected count to 14/40 with the hole-boundary
attribution.

For the other top entries the v1 scratch note matches the verified
count: cos(π/7) at 26 in the scratch table differs from 13 here, and
√5/2 at 26 in the scratch table differs from 14 here. The
likely origin of the v1 over-counts: an earlier double-counting of
value-and-reciprocal as two separate hits (the v1 code path that
became `match_curated` in `seven_circles_tight.py` explicitly notes
"Reciprocal counted as ONE match, not two" as a v2 change). Under
that hypothesis, halving the scratch count gives 13.5 ≈ 13.5, which
matches the verified figures to within rounding for cos(π/7) and
√5/2 but not for cos 18°. The exact provenance of the 27 is not
recovered here; the verified count is what should be cited.

The brief's epistemic-discipline section anticipated exactly this:

> If the 27/40 count does NOT reproduce … document this explicitly as a
> discrepancy and write the correct count in the report. The paper cite
> will be updated to match the verified number. The principle (cos18°
> is the dominant value) matters more than the exact 27/40 fraction.

The principle holds: cos 18° is the joint-highest-frequency framework
constant in the seven-circles cross-ratio distribution at the
canonical parameters, with ~10× null enrichment.

---

## §6 — Epistemic Status

**What this establishes:**

- cos 18° has a prior geometric address in the seven-natural-circles
  construction on the torus: it is the joint-highest-frequency
  framework constant across a wide chord sweep at canonical
  parameters, with ~10× null enrichment.
- The pentagon content (cos 18°) concentrates in the local-curvature
  (tube) frame and is suppressed in the external projective frame —
  consistent with crystallographic exclusion of 5-fold symmetry from
  the p6m bulk.

**What this does NOT establish:**

- It does not derive the void correction ζ·(1 − cos 18°) in the
  proton-radius formula from first principles. The probe gives a
  prior geometric address; it does not derive the projection
  mechanism that produces the specific correction factor.
- It does not establish a unique combinatorial address. The specific
  4-circle quadruples that produce cos 18° at R/r = 3 do not in
  general produce cos 18° at other R/r values (see scratch note §R3);
  the register identity (5-fold trig) is stable across
  reparameterisation but the specific quadruple-to-constant map is not.
- It does not promote cos 18° beyond Register 2 in the framework's
  internal tiering: the bilateral fold from a 36° angular deficit to
  18° per side (the substrate-action step) remains an open
  derivation.

For the paper-section formulation see `paper/X1_cos18_address.md`.
