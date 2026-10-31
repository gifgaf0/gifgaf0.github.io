# E9 control run (P1): the untwisted ring collapses

October 30, 2026. Grid 49³, h = 0.5, box 24 (in units where the potential is ½(|ψ|²−1)²; ξ = 1/√2, λ = √2, κ = 2), η = 0.1. Script `gl3.py` (gradient checked against finite differences, worst relative error 2×10⁻⁷), `control_N0.py`, `pinned_N0.py`. Outputs: `control_N0_N49_R6.json`, `pinned_N0_R*.json`.

**Free relaxation from R = 6.** The composite ring shrinks and vanishes within about 50 iterations; the final energy equals the vacuum energy to 4×10⁻⁷. **P1 holds.**

**Pinned ring, E(R) above vacuum:**

| R | 2 | 3 | 4.5 | 6 | 8 |
|---|---|---|---|---|---|
| E | 131 | 214 | 298 | 1014 | 1381 |
| pinned sites | 96 | 168 | 216 | 324 | 432 |

Monotone, so **P1 holds**, but the step between 4.5 and 6 follows the pin density (sites per unit length 7.6 → 8.6), not the physics. The pinned curve is contaminated by the pin's own cost and is a control only. The N = 1 verdict uses free relaxation, as Amendment A states.

**Instrument notes, for the record.**
- Two fixes were made during the control and before any N = 1 run: the vacuum reference now uses the true vacuum |ψ|² = 1 + η (the first run showed a −207 offset that was exactly this), and the grid is centred on a site plane (odd N) so that a ring in the z = 0 plane can be pinned by a connected chain of sites.
- Cost at 49³: 0.08 s per energy evaluation, about 0.25 s per L-BFGS iteration.
- At R = 8 the ring is 4 units (2.8 λ) from the box edge; boxes of 65³ are needed for R ≳ 8.
