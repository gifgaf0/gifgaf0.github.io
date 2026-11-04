# E10 / Route B, QB: where do bulk charged lumps (Q-balls) bind?

*November 4, 2026. Label: Exploration. Written after `REPORT_B4.md` (head 815033a) and before any QB run. It asks whether the bulk lump that made B4's ring a passenger tracks the straight-string window.*

## 0. The question

B4 found a vortex-free charged lump below m_bulk·Q at λ = 1. The straight-string window exists at λ ∈ {0.8, 0.9, 1.0} and not at λ ∈ {1.1, 1.2} (`REPORT_B2B3.md`, `REPORT_verify.md` V3). Over λ and Q, where does the lump bind?

- **If it binds exactly where the window exists,** the two share a mechanism, plausibly the attraction that lets an unhiggsed orientation region grow.
- **If it binds more widely,** Q-balls are generic in this model, and any charge-supported closure must beat them.

## 1. Model and instrument

- **Model:** PREREG_B2B3 §1, with G = diag(0, 1, 0).
- **Instrument:** B4's axisymmetric code (`b4_axi.py`, `b4_run.py`) with n = 0 and no vortex, unchanged. Use the same box (ρ ∈ [0, 40], z ∈ [−20, 20], Dirichlet vacuum edge), h = 0.25, the same minimizer and the same stopping rule.
- **Regression before any new run:** at λ = 1 and Q = 1626.5329, B4's C-d start must reproduce E = 1589.9110 to 1e-6 relative.

## 2. Grid (fixed now)

- λ ∈ {0.8, 0.9, 1.0, 1.1, 1.2}.
- Q ∈ {200, 400, 800, 1626.5329, 2710.9} (log-spaced, plus B4's two charges).
- **Two starts per point:**
  - S1: B4's ball start (`b4_axi.ball_start`, radius 4).
  - S2: the same with radius 8.

  The lower final E is the result for that point. Both are reported.

That is 5 × 5 × 2 = 50 runs.

**m_bulk = min(1, λ)** (PREREG_B2B3 §1).

## 3. Verdict per (λ, Q) (fixed now)

| verdict | conditions |
|---|---|
| **BOUND** | Leak < 1 % (charge within 4 of the box edge, excluding the axis), **E/(m_bulk Q) < 0.995**, ω/m_bulk < 1, and the 3D charge rms radius is less than 15. |
| **DISPERSED** | Leak ≥ 1 %, or E/(m_bulk Q) ≥ 1. |
| **MARGINAL** | Anything else. This includes 0.995 ≤ E/(m_bulk Q) < 1, which sits within the box's threshold shift. |

**Checks.**
- **Box check.** For each λ, take the largest-Q BOUND point and the smallest-Q BOUND point. Re-relax them in the box ρ ∈ [0, 60], z ∈ [−30, 30]. The verdict must not change, and E must move by < 1e-3 relative.
- **Resolution check.** For each λ with any BOUND point, re-relax one BOUND point at h = 0.125, with the same criterion.

**Binding threshold.** Q_min(λ) is the bracket between the largest DISPERSED Q and the smallest BOUND Q on the grid. It is reported as a bracket only; no refinement.

## 4. Classification against the window (fixed now)

Let W = {0.8, 0.9, 1.0}, the λ values with a straight-string window, and B = the λ values with at least one BOUND point.

| | condition |
|---|---|
| **TRACKS** | B = W |
| **BROADER** | B ⊋ W: lumps bind where there is no window |
| **NARROWER** | B ⊊ W |
| **MIXED** | otherwise |

## 5. Predictions (written now)

**A crude thin-wall estimate, made before any run.** Deep inside a large lump, one orientation direction is unhiggsed. That costs the potential energy λ²/4 per unit volume, and the charge rotates there. The thin-wall frequency is then ω₀² ≈ 2U/|φ|² ≈ λ²/2, so **ω₀/m_bulk ≈ 1/√2** for λ ≤ 1 and **≈ λ/√2** for λ > 1. Binding at large Q needs ω₀ < m_bulk, which gives **λ < √2 ≈ 1.41**.

So this estimate predicts large-Q lumps **at every λ on the grid, including 1.1 and 1.2,** where there is no window. It is crude: it ignores gradients, the W_t dressing and the gauge fields.

| ID | Prediction | Prior |
|---|---|---|
| QB-P1 | Regression reproduces B4's C-d. | must hold |
| QB-P2 | Classification **BROADER**: lumps bind at λ = 1.1 and 1.2 at the larger Q. | 55 % |
| QB-P2′ | Classification TRACKS. | 30 % |
| QB-P3 | At each λ with a BOUND point, E/(m_bulk Q) falls with Q (thin-wall approach), and Q_min(λ) rises with λ. | 70 % |
| QB-P4 | At λ = 1.2 and Q = 2710.9: BOUND, with E/(m_bulk Q) between 0.95 and 0.995. | 45 % |

## 6. What follows

- **BROADER.** Q-balls are generic in this model, beyond the window. A charge-supported closure of the U(3) string can win only where the ring's energy per charge (ℰ*/q*, 1.065 m_bulk at #66) falls below the lump's. Combined with the window, that is a single inequality to check. It closes the charge route in this model unless such a region appears.
- **TRACKS.** The window and the lump share a mechanism. The statement for the programme is then that the same attraction that lets a charged string hold its charge also lets the charge bind without it. That would be a structural reason why charge-supported closures are passengers in this class of models.
- **NARROWER or MIXED.** Report as found. If there is a λ with a window but no lump, it gets its own B4-style pre-registration there.

## 7. Eddington guard

- Fixed: the λ and Q grids, the starts, the verdict thresholds, the box rule and the classification.
- No refinement of Q or λ after seeing results; any refinement is a new pre-registration.
- Model units only. The SU(3)_{C+F} charge is not electric charge.
