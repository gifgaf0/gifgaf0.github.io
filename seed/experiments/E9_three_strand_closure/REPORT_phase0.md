# E9 option 4, Phase 0 (straight-string feasibility): report

October 31, 2026. Label: Exploration. The model, grid, checks, verdict rule and selection rule are those fixed in `PREREG_option4.md` §1, §2.1–§2.3, §5 and §6. The ψ sector is unchanged: κ = 2 (e = 1/√12), η = 0.1, and the §2.1 grid is used exactly (12 points, no others). The radial grid is the one in `option4_design.py`: dr = 0.04, rmax = 24. No loop was built or run. There is no Phase 1, no `axial_vorton.py` and no 3D.

**Units.** Model units only (`gl3.py` coordinates, ξ = 1/√2). ℰ is the line energy per unit coordinate length above the ψ vacuum. k is the σ winding density, and q is the σ charge per unit length. No particle identification is made, and n and Q are not to be read as spin or electric charge (§6).

## Summary

| | Result |
|---|---|
| C3 (global vacuum) | PASS at all 12 points. None dropped. |
| Existence windows | Non-empty at all 12 points. At 11 of 12 the q scan reached the safety cap q = 100 while still inside the window (deviation 3). Only b1_d1 closed naturally, at q ≈ 52 (by ω → m_vac and the tail test). |
| Verdicts (§2.3) | **WINDOW:** b1_d0.5, b2_d0.5, b2_d1, b3_d0.5, b3_d1, b5_d1 (each "q capped at 100"). **NONE:** b1_d1 (window closed). **NONE up to q = 100 (truncated):** b1_d0.25, b2_d0.25, b3_d0.25, b5_d0.25, b5_d0.5. |
| **P0 (§5)** | **Holds: at least one WINDOW (6 of 12).** |
| Selected point (§2.3 rule) | **b5_d1:** β = 5, δ = 1, μ² = 6.397, λ = 14.09, m_vac = 3.179. Equilibrium at k* = 0.7314, q* = 97.0, ω*/m_vac = 0.464, d²E/dR² = +66.9. |
| §3.2 labels it would give (Phase 1 not run) | n = 6, R_eq = 8.20, Q = 5.00 × 10³ |

**Read the following before the summary.**
- **Every equilibrium sits at large charge (q* ≳ 35).** The selected one sits at the q = 100 cap edge.
- **The selection is set by the truncation.** Within a point, ω*/m_vac falls as q* grows. The smallest stable ω*/m_vac is therefore always the last q* at which the R-interpolant still fits under the cap (q* = 97). A larger cap would move the selected (k*, q*), and possibly the selected point (§5.1).
- **The "string" at these equilibria is not a thin core with a condensate.** It is a fat σ-phase tube: the σ half-radius r_σ ≈ 4.3, and the ψ core is pushed out to r_ψ ≈ 5.0. R_eq / r_σ = 1.9 at the selected point, so the author's thin-ring reliability flag fires (§5.2). R_eq ≈ 8 is fixed by the n = round(8k*) rule, not by the physics.

## 1. Commands run

```
cd seed/experiments/E9_three_strand_closure
pip install scipy                                   # not present in the container (deviation 1)
nohup python3 option4_phase0.py > log_phase0.txt 2>&1 &     # first run, aborted after ~45 min (deviation 2)
# (option4_phase0.py extended with descriptive diagnostics, author's note; minimisation unchanged)
nohup python3 option4_phase0.py > log_phase0.txt 2>&1 &     # official run, 35 021 s
python3 phase0_tables.py                            # read-only tables for this report
```

The first run's console output is kept as `log_phase0_aborted_run1.txt`. Every k row it completed (8 rows over 4 points) is reproduced line for line by the official run, as expected from a deterministic L-BFGS-B.

## 2. Software, hardware, checks

- Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1 (installed with pip). Linux container, 4 cores (Intel Xeon 2.8 GHz), 15 GB RAM. One worker per point, 4 in parallel.
- **Gradient check** of the full functional ℰ = T_static(k) + q²/(4I). The definition is the same as `gl3.check_grad`: 40 random coordinates across f, a and s, central FD step 10⁻⁶, error |fd − g|/(|fd| + 10⁻⁸). Random state, k = 0.3, q = 1.7, β = 2, μ² = 3.6, λ = 4. **Worst relative error 2.5 × 10⁻⁶** (expected ≲ 10⁻⁵). A second check at k = 0, q = 0.5 gave 3.2 × 10⁻⁷.
- **Consistency with `option4_design.py`.** At q = 0, on a random state, ℰ and its gradient equal `option4_design.solve()`'s functional with q2 = k² exactly (difference 0.0).
- **Bare string.** T₀ = 27.798, core radius 1.168. ε₀(β) for β = 1, 2, 3, 5 is 2.047, 3.163, 4.025, 5.397, which reproduces §1.3.
- **Solver.** L-BFGS-B with `option4_design.solve()`'s options (gtol 10⁻¹⁰, ftol 10⁻¹⁶, maxiter 50 000). 64 668 grid solves in total, plus 3 315 ray cross-check solves (3 per sign change).
- **𝒯 cross-checks** (not used in the verdict).
  - Envelope theorem: ∂_kℰ = 2kI and ∂_qℰ = ω.
  - Continuum virial, 2D Derrick scaling at fixed (k, q), derived here: 𝒯 = G + 2B − 2k²I. Here G is the scale-invariant (gradient and winding) energy and B is the magnetic energy. A corollary is that **𝒯 > 0 identically at k = 0, at any q**, so a thin-ring equilibrium needs k²I > G/2 + B.
  - Over every in-window point with central differences in both directions, the finite-difference 𝒯 agrees with the envelope value to ≤ 4.9 × 10⁻⁴ ℰ and with the virial value to ≤ 6.4 × 10⁻⁴ ℰ.
  - At the selected equilibrium's bracketing points: 𝒯_fd = 2.754 / −1.626 and 𝒯_virial = 2.732 / −1.648.

## 3. C3 (vacuum) and σ-phase metastability

V(ρ, S) = 3·½(ρ − 1)² − 3ηρ − μ²S + ½λS² + 3βρS on ρ, S ≥ 0. The candidates were enumerated analytically (corners, both edges, and the interior stationary point) and cross-checked by a 601² grid plus a bounded L-BFGS-B polish. At all 12 points the global minimum is the ψ vacuum, ρ = 1 + η, S = 0, and the polish returns ρ = 1.100000, S = 0. The σ-only vacuum lies 0.363 above it at every point (= 0.2 D, by the choice of λ). **C3 passes everywhere and no point is dropped.**

**Author's note, item 1, verified.** At ψ = 0, S = μ²/λ, ∂V/∂S = 0 and ∂²V/∂S² = λ > 0. Also ∂V/∂ρ = −3(1 + η) + 3βS. Since V is linear in ρ = |ψ|², ψ = 0 is a local minimum iff βS > 1 + η. With S = μ²/λ = 1.6D/μ²:

| point | b1_d0.25 | b1_d0.5 | b1_d1 | b2_* | b3_* | b5_* |
|---|---|---|---|---|---|---|
| βS − (1 + η) | +0.164 | +0.040 | **−0.147** | +0.602 / +0.486 / +0.295 | +0.938 / +0.825 / +0.634 | +1.471 / +1.362 / +1.170 |

- The σ phase is metastable at 11 of 12 points, and not at b1_d1. The Hessian determinant 3λ − 9β² is < 0 at those 11 points, so the interior stationary point is a saddle. At b1_d1 the determinant is > 0 and the interior point is infeasible.
- This matches the scan exactly. b1_d1 is the only point whose window closed in q, and the other 11 reached the cap.
- The profiles show the mechanism. With growing q, ψ is expelled from a widening σ-filled core. At b5_d1, k = 0:

  | q | r_σ | r_ψ | I |
  |---|---|---|---|
  | 0 | 0.60 | 1.23 | 0.30 |
  | 25 | 2.07 | 2.72 | 8.5 |
  | 100 | 4.76 | 5.44 | 40.0 |

  Here r_σ is where s² = ½s(0)², and r_ψ is where f² = ½(1 + η).
- **Pre-registration gap (author's, recorded here, not a deviation).** C3 as written checks only the global minimum. It does not test metastability of the σ phase, which is what lets large charge be stored in a growing σ-phase tube.

## 4. Per-point results

Window extent is k from 0 to k_max. For each in-window k the q scan ran to the first out-of-window point, or to the cap q = 100. (k*, q*, ω*/m_vac) and d²E/dR² are given for the stable equilibrium with the smallest ω*/m_vac at that point. d²E/dR² is from the ℰ interpolant (relative step 0.03); the value in brackets is from direct solves on the ray.

| point | β | δ | μ² | λ | m_vac | βS−(1+η) | C3 | window: k_max; q range | 𝒯 sign change | (k*, q*, ω*/m_vac) | d²E/dR² | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| b1_d0.25 | 1 | 0.25 | 2.297 | 1.816 | 1.002 | +0.164 | PASS | 0.45; to 100 (capped, 10 rows) | y (8, all at k = 0.45 edge) | (0.4495, 98.50, 0.825)† | undefined (interp.); [+45.5] | **NONE up to q = 100 (truncated)** |
| b1_d0.5 | 1 | 0.5 | 2.547 | 2.233 | 0.868 | +0.040 | PASS | 0.70; to 100 (k ≤ 0.55), 45.75 / 29.75 / 21.25 at k = 0.60 / 0.65 / 0.70 | y (153; 141 stable) | (0.4089, 97.00, 0.900) | +45.4 [+48.8] | **WINDOW** (q capped, 12 rows) |
| b1_d1 | 1 | 1 | 3.047 | 3.196 | 0.503 | −0.147 | PASS | 0.95; 52.25 at k = 0 falling to 1.5 at k = 0.95 (closed) | n | — | — | **NONE** |
| b2_d0.25 | 2 | 0.25 | 3.413 | 4.010 | 1.785 | +0.602 | PASS | 0.45; to 100 (capped, 10 rows) | n | — | — | **NONE up to q = 100 (truncated)** |
| b2_d0.5 | 2 | 0.5 | 3.663 | 4.619 | 1.714 | +0.486 | PASS | 0.70; to 100 (capped, 15 rows) | y (157; 132 stable) | (0.5535, 97.00, 0.637) | +61.4 [+61.3] | **WINDOW** (q capped, 15 rows) |
| b2_d1 | 2 | 1 | 4.163 | 5.967 | 1.561 | +0.295 | PASS | 0.95; to 100 (capped, 20 rows) | y (270; 252 stable) | (0.5227, 97.00, 0.692) | +53.8 [+52.9] | **WINDOW** (q capped, 20 rows) |
| b3_d0.25 | 3 | 0.25 | 4.275 | 6.293 | 2.372 | +0.938 | PASS | 0.45; to 100 (capped, 10 rows) | n | — | — | **NONE up to q = 100 (truncated)** |
| b3_d0.5 | 3 | 0.5 | 4.525 | 7.051 | 2.318 | +0.825 | PASS | 0.70; to 100 (capped, 15 rows) | y (84; 52 stable) | (0.6350, 97.00, 0.541) | +66.7 [+63.6] | **WINDOW** (q capped, 15 rows) |
| b3_d1 | 3 | 1 | 5.025 | 8.695 | 2.208 | +0.634 | PASS | 0.95; to 100 (capped, 20 rows) | y (242; 222 stable) | (0.6192, 97.00, 0.571) | +59.5 [+58.8] | **WINDOW** (q capped, 20 rows) |
| b5_d0.25 | 5 | 0.25 | 5.647 | 10.982 | 3.294 | +1.471 | PASS | 0.45; to 100 (capped, 10 rows) | n | — | — | **NONE up to q = 100 (truncated)** |
| b5_d0.5 | 5 | 0.5 | 5.897 | 11.976 | 3.256 | +1.362 | PASS | 0.65; to 100 (capped, 14 rows) | n | — | — | **NONE up to q = 100 (truncated)** |
| b5_d1 | 5 | 1 | 6.397 | 14.093 | 3.179 | +1.170 | PASS | 0.95; to 100 (capped, 20 rows) | y (191; 166 stable) | **(0.7314, 97.00, 0.464)** | **+66.9** [+68.3] | **WINDOW** (q capped, 20 rows) |

† Not a stable equilibrium under the rule. See §5.3.

**Minimum 𝒯/ℰ over the window**, with its location (k, q):

| point | min 𝒯/ℰ | at (k, q) |
|---|---|---|
| b1_d0.25 | −0.0035 | (0.45, 100) |
| b1_d0.5 | −0.124 | (0.55, 100) |
| b1_d1 | +0.377 | (0.15, 52.75) |
| b2_d0.25 | +0.079 | (0.45, 100) |
| b2_d0.5 | −0.096 | (0.70, 100) |
| b2_d1 | −0.268 | (0.95, 100) |
| b3_d0.25 | +0.111 | (0.45, 100) |
| b3_d0.5 | −0.037 | (0.70, 100) |
| b3_d1 | −0.185 | (0.95, 100) |
| b5_d0.25 | +0.140 | (0.45, 100) |
| b5_d0.5 | +0.044 | (0.65, 100) |
| b5_d1 | −0.108 | (0.95, 100) |

At every capped point the minimum lies at the corner (k_max, q = 100). 𝒯/ℰ is still falling there, so the truncated NONEs are not evidence of absence.

**Sign changes, all points together.** There are 1105 crossings of the 𝒯 = 0 contour with grid lines. The full list is in `phase0_results.json` under `points[].summary.sign_changes`.
- They span q* from 34.8 to 100 and k* from 0.40 to 0.95.
- Every d²E/dR² that could be evaluated from the interpolant is positive: 0 negative, and 140 undefined because the ray leaves the convex hull of the window at q > 100 or k > k_max.
- All 1105 direct-solve checks are positive. No interpolant/direct sign disagreements.

**Window tests.**
- The tail fraction (I beyond r = 16) stayed below 2 × 10⁻⁶ everywhere except b1_d1. There it reached the 1 % limit and ended the k = 0, 0.05 and 0.10 rows, at q = 52.5–53.75; ω ≥ m_vac ended the other 17 rows.
- The largest r_σ in any window is 4.76, so **no (k, q) is box-affected** (r_σ > 12; author's item 4).
- Every k scan ended because the q = 0 point at the next k had σ(0) < 0.05: the σ condensate is not supported at q = 0 once k² ≳ δ.

## 5. Selection and what it derives

### 5.1 Selection

Under the §2.3 rule, the smallest ω*/m_vac among WINDOW equilibria is **b5_d1**, with ω*/m_vac = 0.4636. The equilibrium lies between grid points (0.70, 97) and (0.75, 97). Both solves, and all six neighbours used in their central differences, converged normally and are unflagged.

| quantity | value |
|---|---|
| k*, q* | 0.7314, 97.00 |
| ω* | 1.474 (m_vac = 3.179) |
| ℰ* | 178.2 (= 6.4 T₀) |
| r_σ* | 4.30 |
| r_ψ* | 4.97 |
| d²E/dR² | +66.9 (interpolant), +68.3 (direct solves) |
| §3.2 labels | n = max(1, round(8 × 0.7314)) = **6**, R_eq = n/k* = **8.20**, Q = 2πR_eq q* = **5.00 × 10³** |
| R_eq / r_σ* | **1.91 < 3: thin-ring proxy unreliable** (author's item 3) |
| R_eq / r_ψ* | 1.65 |
| Thin-ring energy 2πR_eq ℰ* | 9.18 × 10³, against m_vac·Q = 1.59 × 10⁴ (ratio 0.58) |

The last row compares with P2's "E < m_vac·Q" criterion. It is descriptive only: P2 is a Phase 1 criterion and is not applied here.

The ranking among points is close:

| point | min ω*/m_vac |
|---|---|
| b5_d1 | 0.464 |
| b3_d0.5 | 0.541 |
| b3_d1 | 0.571 |
| b2_d0.5 | 0.637 |
| b2_d1 | 0.692 |
| b1_d0.5 | 0.900 |

At every WINDOW point the minimizing equilibrium is at q* = 97.0. That is the largest q* at which the R ± 3 % interpolation stencil stays under q = 100. Along each point's 𝒯 = 0 contour, ω*/m_vac decreases with q*, so **the selected (k*, q*) is determined by the q cap, not by an interior optimum**. Whether a larger cap would change the selected point is not established.

### 5.2 Thin-ring reliability (descriptive, author's item 3)

- Only 154 of the 1105 sign changes have R_eq / r_σ ≥ 3, and 132 of those are stable equilibria. The stable ones are at b2_d1 (88; best ω*/m_vac = 0.765, at k* = 0.688, q* = 56.75, n = 6) and b3_d1 (44; best 0.646, at k* = 0.814, q* = 53.50, n = 7). None is at the selected point.
- **Caution for the author.** Because n = round(8k*), R_eq = n/k* ≈ 8 at every equilibrium. So R_eq / r_σ is fixed mainly by the §3.2 n rule, not by the solution. A larger n at the same (k*, q*) scales R_eq and Q up together and would pass the ratio test. The thin-ring proxy is then better justified, at the cost of a proportionally larger Q.

### 5.3 b1_d0.25 (flag)

- All 8 of its sign changes lie on its window's k-edge (k = 0.45, q = 98.4–100). They use one-sided k differences.
- Their d²E/dR² cannot be evaluated from the interpolant: the R − 3 % side of the ray needs k > 0.45, outside the window.
- The direct-solve check gives +45.4 to +45.5 at all 8.
- Under the most literal reading ("evaluated … by interpolating the ℰ grid") these are not established equilibria with d²E/dR² > 0, so the verdict is NONE up to q = 100 (truncated). Flagged for the author. It does not affect the selection (ω*/m_vac ≈ 0.82 there).

## 6. Crude §1.3 estimate against the exact calculation (descriptive)

Crude test: T/I_c ≤ (μ² − ε₀) + 2m²_vac, with T and I_c from the exact (k, q) = (0, 0) solve. Per grid point it uses 𝒯_crude = T − (k² + ω_c²)I_c, where ω_c = q/(2I_c).

| point | T(0,0) | I_c | T/I_c | limit | crude feasible | exact verdict | 𝒯 sign agreement (in-window points) |
|---|---|---|---|---|---|---|---|
| b1_d0.25 | 27.537 | 2.310 | 11.92 | 2.26 | n | NONE (trunc.) | 647 / 4010 |
| b1_d0.5 | 26.879 | 4.536 | 5.93 | 2.01 | n | WINDOW | 1653 / 5202 |
| b1_d1 | 24.416 | 11.418 | 2.14 | 1.51 | n | NONE | 1341 / 1684 |
| b2_d0.25 | 27.738 | 0.506 | 54.86 | 6.63 | n | NONE (trunc.) | 300 / 4010 |
| b2_d0.5 | 27.584 | 0.942 | 29.28 | 6.38 | n | WINDOW | 973 / 6015 |
| b2_d1 | 27.090 | 1.706 | 15.88 | 5.88 | n | WINDOW | 2758 / 8020 |
| b3_d0.25 | 27.771 | 0.228 | 121.8 | 11.50 | n | NONE (trunc.) | 210 / 4010 |
| b3_d0.5 | 27.698 | 0.426 | 64.96 | 11.25 | n | WINDOW | 536 / 6015 |
| b3_d1 | 27.462 | 0.763 | 36.00 | 10.75 | n | WINDOW | 1892 / 8020 |
| b5_d0.25 | 27.787 | 0.088 | 314.3 | 21.96 | n | NONE (trunc.) | 130 / 4010 |
| b5_d0.5 | 27.758 | 0.167 | 165.9 | 21.71 | n | NONE (trunc.) | 252 / 5614 |
| b5_d1 | 27.659 | 0.302 | 91.5 | 21.21 | n | WINDOW | 1091 / 8020 |

- The crude estimate says "no thin ring" at all 12 points. It agrees with the exact verdict only at the six NONE points (five of them truncated), and disagrees at all six WINDOW points.
- Point by point the sign agreement is poor. The crude 𝒯 goes negative at modest q because it freezes I = I_c. The exact solutions instead grow I by a factor of 10 to 100 with q (the σ-phase tube of §3). That keeps ω small, and makes the k²I term large enough for 𝒯 < 0 (virial form, §2).
- **Conclusion:** the §1.3 obstacle was an artefact of the frozen profile in this sense. The exact equilibria exist only in a regime the estimate did not model.

## 7. Deviations, collected

1. **SciPy installed with pip.** It was not present in the container.
2. **Run restarted once.** The first run was stopped after about 45 minutes to add the descriptive diagnostics requested in the author's note: r_σ, r_ψ, the box flag, the metastability column, and the G/B virial pieces. These are observables only. The functional, grid, step sizes, stop rules, warm starts and solver options are unchanged. Every row the aborted run completed is reproduced exactly (`log_phase0_aborted_run1.txt`).
3. **q safety cap at q = 100 (400 steps of 0.25).** It was added to the script by me, not by the pre-registration. §2.2 and the task say "q from 0 upward" until out of window. The cap was hit at 11 of 12 points (156 k rows), and per the author's note it was kept and not extended. Consequences:
   - The five NONEs at δ = 0.25 and at b5_d0.5 are labelled "NONE up to q = 100 (truncated)".
   - The six WINDOW verdicts stand, but the location of every selected equilibrium is set by the cap (§5.1).
   - PREREG §8's cost estimate (~150 solves per point) was exceeded by 10–50×: 64 668 solves, 9.7 h of wall time.
4. **Non-converged solves are kept, not dropped.** 128 of 64 668 solves (0.2 %) did not return L-BFGS-B success.
   - 125 ended with `ABNORMAL` line-search termination at max|∇ℰ| ≤ 3.9 × 10⁻⁵, the floating-point floor at ftol = 10⁻¹⁶. All 125 were inside the window and were used as computed.
   - 3 hit the 50 000-iteration limit. Each is a q = 0 point at the k just past the window edge: σ(0) = 0.019, 0.0073 and 0.0073 at b1_d0.25 (k = 0.5), b2_d0.25 (k = 0.5) and b2_d1 (k = 1.0). In each, σ is slowly decaying to zero (max|∇| ≤ 1.5 × 10⁻⁴).
   - **These solves ended the k scan at three points.** A converged solve would have σ(0) even smaller, so the stop decision would not change, but it rests on non-converged solves. Full list in the appendix.
   - No solver tolerance or step was changed.
5. **𝒯 at the grid edges.** At k = 0 the k∂_kℰ term is set to 0, and at q = 0 the q∂_qℰ term is set to 0 (exact, by symmetry). Elsewhere a neighbour outside the window gives a one-sided difference, flagged per sign change in the JSON. 172 of the 1105 sign changes use a one-sided difference. The selected one does not.
6. **d²E/dR² method.**
   - Primary: a Clough–Tocher (C¹ piecewise-cubic) interpolant of ℰ over the in-window grid, in index coordinates. A central difference along the fixed-(n, Q) ray with relative step h = 0.03, using the §3.2 n.
   - Also recorded: h = 0.06, and a direct-solve cross-check (3 extra solves per sign change, warm-started from the nearest grid point; not used in the verdict).
   - The choice of interpolant and step is mine. The pre-registration says only "interpolating the ℰ grid".
7. **"Nearest solved neighbour" for warm starts** is taken as Euclidean distance in (k, q). In practice this is (k − 0.05, q) whenever that point was solved, otherwise (k, q − 0.25).
8. **`phase0_results.json` is written compactly** (no indentation; 45 MB) to stay under GitHub's file-size warning. The first official write used indent = 1 (60 MB). The file was re-serialized without any change of content, and the script now writes the compact form.
9. **An extra file, `phase0_tables.py`** (read-only post-processing of the JSON into the tables above), is committed.

**Ambiguities flagged for the author.** Each was resolved by the most literal reading.

- **(a) The stop rule ends the k scan when the q = 0 point fails.**
  - At q = 0 the σ condensate disappears once k² ≳ δ, so every scan ended at k_max ≈ 0.45, 0.70, 0.95 for δ = 0.25, 0.5, 1.
  - Charged (q > 0) solutions at larger k were never tried, although the q direction stays in-window up to the cap at all k ≤ k_max at most points.
  - At the truncated-NONE points min 𝒯/ℰ falls towards that k edge (for example, b5_d0.5 reaches +0.044 at k = 0.65). So the k truncation, not only the q cap, may hide equilibria.
- **(b) ω < m_vac is the localization test as written.** For k > 0 the far-field σ decay rate is √(m²_vac + k² − ω²), so the actual localization condition is the weaker ω² < m²_vac + k². The pre-registered (stricter) test was used. At the capped points it never bound.
- **(c) §2.3 for edge sign changes** whose ray leaves the window (b1_d0.25, §5.3).
- **(d) The §3.2 n = round(8k*) rule fixes R_eq ≈ 8,** and with it R_eq / r_σ (§5.2).
- **(e) Pre-registration gap: C3 does not test σ-phase metastability** (§3).
- **(f) The selection rule picks the cap edge** (§5.1).

No parameter outside the §2.1 grid was used, and the ψ sector was not touched. `PREREG_option4.md`, `PREREG.md`, `gl3.py` and `option4_design.py` are unmodified.

## 8. What is and is not established

**Established, within the stated truncations:**
- On the E9 three-strand host string with the §1 σ field, C3 holds at all 12 grid points.
- The straight-string fixed-charge functional ℰ(k, q) has thin-ring equilibria (𝒯 = 0 with d²E/dR² > 0) at 6 of 12 points: b1_d0.5, b2_d0.5, b2_d1, b3_d0.5, b3_d1, b5_d1. All of them have ω*/m_vac < 1. **P0 holds.**
- These equilibria occur only at large charge per length (q* ≳ 35, I ≈ 14–62 at the bracketing grid points). At those charges the σ field forms a σ-phase tube of radius 4–5 that pushes the ψ core out to a similar radius. This is possible because the σ phase is metastable (βS > 1 + η) at 11 of the 12 points.

**Not established:**
- **No loop exists or was computed.** Phase 0 is a straight-string, thin-ring proxy. A WINDOW does not establish a vorton, and a NONE does not exclude a thick one.
- **The thin-ring proxy is doubtful at the selected equilibrium:** R_eq / r_σ = 1.9 and R_eq / r_ψ = 1.65 with n = 6.
- **The selected (k*, q*) and n, R_eq, Q are not stable to the q cap.** The five truncated NONEs are not NONEs on the full window. Neither the cap nor the k stop rule was relaxed here.
- Phase 1 has not been run, so P1 to P5 are not addressed. Whether Phase 1 should proceed with the selected labels (n = 6, R_eq = 8.20, Q ≈ 5.0 × 10³ at b5_d1), with a larger n, or after a revised Phase 0 is the author's decision.

## 9. Files committed

- `option4_phase0.py`: the Phase 0 script, which imports `option4_design.py`.
- `phase0_results.json`: every (k, q) solve with its observables, per-point summaries (including all sign changes), C3 results, the selection, and checks.
- `log_phase0.txt`: console output of the official run. `log_phase0_aborted_run1.txt`: the aborted first run.
- `phase0_tables.py`: read-only table generator.
- `REPORT_phase0.md`: this file.

No field profiles are saved. They are reproducible by re-running the script, which is deterministic.

## Appendix: non-converged solves (all 128)

```
- b1_d0.25 k=0.10 q=0.25: ABNORMAL: , nit=4146, max|grad|=3.3e-06, in_window=True, sigma0=0.669
- b1_d0.25 k=0.10 q=5.50: ABNORMAL: , nit=2672, max|grad|=9.3e-06, in_window=True, sigma0=0.917
- b1_d0.25 k=0.10 q=22.75: ABNORMAL: , nit=2924, max|grad|=7.4e-06, in_window=True, sigma0=1.13
- b1_d0.25 k=0.20 q=4.75: ABNORMAL: , nit=2989, max|grad|=6.6e-06, in_window=True, sigma0=0.883
- b1_d0.25 k=0.20 q=5.50: ABNORMAL: , nit=2984, max|grad|=3.1e-06, in_window=True, sigma0=0.906
- b1_d0.25 k=0.20 q=35.50: ABNORMAL: , nit=3445, max|grad|=1.6e-05, in_window=True, sigma0=1.17
- b1_d0.25 k=0.35 q=6.75: ABNORMAL: , nit=3304, max|grad|=6.0e-06, in_window=True, sigma0=0.916
- b1_d0.25 k=0.45 q=3.00: ABNORMAL: , nit=3346, max|grad|=9.3e-06, in_window=True, sigma0=0.743
- b1_d0.25 k=0.45 q=57.50: ABNORMAL: , nit=3796, max|grad|=2.3e-05, in_window=True, sigma0=1.2
- b1_d0.25 k=0.50 q=0.00: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT, nit=50000, max|grad|=3.8e-05, in_window=False, sigma0=0.0193
- b1_d0.5 k=0.05 q=10.50: ABNORMAL: , nit=2352, max|grad|=2.2e-06, in_window=True, sigma0=0.988
- b1_d0.5 k=0.10 q=29.75: ABNORMAL: , nit=3096, max|grad|=1.4e-05, in_window=True, sigma0=1.09
- b1_d0.5 k=0.25 q=3.50: ABNORMAL: , nit=3247, max|grad|=9.1e-06, in_window=True, sigma0=0.853
- b1_d0.5 k=0.25 q=11.75: ABNORMAL: , nit=3341, max|grad|=8.9e-06, in_window=True, sigma0=0.988
- b1_d0.5 k=0.35 q=5.00: ABNORMAL: , nit=3418, max|grad|=6.4e-06, in_window=True, sigma0=0.869
- b1_d0.5 k=0.55 q=1.75: ABNORMAL: , nit=3302, max|grad|=5.4e-06, in_window=True, sigma0=0.669
- b1_d0.5 k=0.55 q=23.25: ABNORMAL: , nit=3597, max|grad|=2.1e-05, in_window=True, sigma0=1.04
- b1_d1 k=0.00 q=1.75: ABNORMAL: , nit=2747, max|grad|=3.8e-06, in_window=True, sigma0=0.888
- b1_d1 k=0.00 q=9.75: ABNORMAL: , nit=3179, max|grad|=6.0e-06, in_window=True, sigma0=0.921
- b1_d1 k=0.05 q=9.00: ABNORMAL: , nit=2784, max|grad|=1.8e-05, in_window=True, sigma0=0.917
- b1_d1 k=0.05 q=45.25: ABNORMAL: , nit=2805, max|grad|=1.7e-05, in_window=True, sigma0=0.976
- b1_d1 k=0.10 q=19.25: ABNORMAL: , nit=3316, max|grad|=3.0e-06, in_window=True, sigma0=0.947
- b1_d1 k=0.35 q=14.25: ABNORMAL: , nit=3794, max|grad|=5.0e-06, in_window=True, sigma0=0.917
- b1_d1 k=0.35 q=16.00: ABNORMAL: , nit=3837, max|grad|=6.2e-06, in_window=True, sigma0=0.924
- b1_d1 k=0.85 q=0.75: ABNORMAL: , nit=3493, max|grad|=4.5e-06, in_window=True, sigma0=0.535
- b2_d0.25 k=0.00 q=24.25: ABNORMAL: , nit=3062, max|grad|=7.2e-06, in_window=True, sigma0=1.02
- b2_d0.25 k=0.00 q=78.50: ABNORMAL: , nit=3038, max|grad|=4.7e-06, in_window=True, sigma0=1.03
- b2_d0.25 k=0.10 q=23.75: ABNORMAL: , nit=2573, max|grad|=1.2e-05, in_window=True, sigma0=1.01
- b2_d0.25 k=0.15 q=94.00: ABNORMAL: , nit=3587, max|grad|=7.0e-06, in_window=True, sigma0=1.03
- b2_d0.25 k=0.30 q=85.75: ABNORMAL: , nit=3772, max|grad|=1.6e-05, in_window=True, sigma0=1.03
- b2_d0.25 k=0.45 q=0.75: ABNORMAL: , nit=2705, max|grad|=1.6e-05, in_window=True, sigma0=0.507
- b2_d0.25 k=0.50 q=0.00: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT, nit=50000, max|grad|=1.5e-04, in_window=False, sigma0=0.00735
- b2_d0.5 k=0.10 q=2.75: ABNORMAL: , nit=2088, max|grad|=1.5e-05, in_window=True, sigma0=0.741
- b2_d0.5 k=0.15 q=3.25: ABNORMAL: , nit=2361, max|grad|=4.2e-06, in_window=True, sigma0=0.76
- b2_d0.5 k=0.15 q=97.50: ABNORMAL: , nit=3555, max|grad|=2.5e-05, in_window=True, sigma0=0.989
- b2_d0.5 k=0.20 q=29.25: ABNORMAL: , nit=3183, max|grad|=3.5e-06, in_window=True, sigma0=0.983
- b2_d0.5 k=0.25 q=12.00: ABNORMAL: , nit=2924, max|grad|=2.1e-05, in_window=True, sigma0=0.918
- b2_d0.5 k=0.25 q=19.50: ABNORMAL: , nit=2963, max|grad|=1.7e-05, in_window=True, sigma0=0.96
- b2_d0.5 k=0.40 q=4.25: ABNORMAL: , nit=2963, max|grad|=9.2e-06, in_window=True, sigma0=0.779
- b2_d0.5 k=0.60 q=0.25: ABNORMAL: , nit=3271, max|grad|=2.5e-06, in_window=True, sigma0=0.392
- b2_d0.5 k=0.60 q=32.50: ABNORMAL: , nit=3561, max|grad|=9.8e-06, in_window=True, sigma0=0.982
- b2_d0.5 k=0.65 q=77.25: ABNORMAL: , nit=3849, max|grad|=1.7e-05, in_window=True, sigma0=0.994
- b2_d1 k=0.10 q=18.75: ABNORMAL: , nit=2570, max|grad|=5.1e-06, in_window=True, sigma0=0.89
- b2_d1 k=0.10 q=35.25: ABNORMAL: , nit=2825, max|grad|=8.8e-06, in_window=True, sigma0=0.915
- b2_d1 k=0.10 q=41.50: ABNORMAL: , nit=2918, max|grad|=1.0e-05, in_window=True, sigma0=0.918
- b2_d1 k=0.15 q=2.25: ABNORMAL: , nit=2537, max|grad|=1.5e-05, in_window=True, sigma0=0.718
- b2_d1 k=0.15 q=29.00: ABNORMAL: , nit=3100, max|grad|=2.7e-06, in_window=True, sigma0=0.909
- b2_d1 k=0.25 q=9.50: ABNORMAL: , nit=2897, max|grad|=5.7e-06, in_window=True, sigma0=0.84
- b2_d1 k=0.25 q=29.25: ABNORMAL: , nit=3146, max|grad|=1.3e-05, in_window=True, sigma0=0.909
- b2_d1 k=0.30 q=95.00: ABNORMAL: , nit=3677, max|grad|=1.9e-05, in_window=True, sigma0=0.919
- b2_d1 k=0.40 q=86.75: ABNORMAL: , nit=3985, max|grad|=7.4e-06, in_window=True, sigma0=0.92
- b2_d1 k=0.55 q=28.00: ABNORMAL: , nit=3531, max|grad|=5.8e-06, in_window=True, sigma0=0.903
- b2_d1 k=0.60 q=3.00: ABNORMAL: , nit=3043, max|grad|=2.0e-06, in_window=True, sigma0=0.699
- b2_d1 k=0.65 q=49.75: ABNORMAL: , nit=3801, max|grad|=1.1e-05, in_window=True, sigma0=0.918
- b2_d1 k=0.75 q=49.75: ABNORMAL: , nit=3764, max|grad|=2.8e-05, in_window=True, sigma0=0.917
- b2_d1 k=0.80 q=1.75: ABNORMAL: , nit=2854, max|grad|=6.3e-06, in_window=True, sigma0=0.603
- b2_d1 k=0.90 q=0.25: ABNORMAL: , nit=3271, max|grad|=4.9e-06, in_window=True, sigma0=0.373
- b2_d1 k=1.00 q=0.00: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT, nit=50000, max|grad|=3.2e-05, in_window=False, sigma0=0.00728
- b3_d0.25 k=0.10 q=19.00: ABNORMAL: , nit=2418, max|grad|=3.1e-06, in_window=True, sigma0=0.928
- b3_d0.25 k=0.10 q=33.75: ABNORMAL: , nit=2674, max|grad|=1.2e-05, in_window=True, sigma0=0.942
- b3_d0.25 k=0.40 q=0.00: ABNORMAL: , nit=6189, max|grad|=9.1e-06, in_window=True, sigma0=0.208
- b3_d0.25 k=0.45 q=23.50: ABNORMAL: , nit=3128, max|grad|=1.3e-05, in_window=True, sigma0=0.934
- b3_d0.5 k=0.00 q=12.75: ABNORMAL: , nit=3196, max|grad|=1.2e-05, in_window=True, sigma0=0.876
- b3_d0.5 k=0.00 q=24.50: ABNORMAL: , nit=3194, max|grad|=1.0e-05, in_window=True, sigma0=0.907
- b3_d0.5 k=0.00 q=80.50: ABNORMAL: , nit=3120, max|grad|=3.9e-05, in_window=True, sigma0=0.899
- b3_d0.5 k=0.05 q=64.50: ABNORMAL: , nit=2455, max|grad|=7.7e-06, in_window=True, sigma0=0.904
- b3_d0.5 k=0.55 q=19.25: ABNORMAL: , nit=3182, max|grad|=8.0e-06, in_window=True, sigma0=0.895
- b3_d0.5 k=0.60 q=23.25: ABNORMAL: , nit=3397, max|grad|=6.0e-06, in_window=True, sigma0=0.902
- b3_d0.5 k=0.60 q=67.50: ABNORMAL: , nit=3774, max|grad|=2.0e-05, in_window=True, sigma0=0.905
- b3_d0.5 k=0.65 q=60.75: ABNORMAL: , nit=3716, max|grad|=7.9e-06, in_window=True, sigma0=0.907
- b3_d0.5 k=0.70 q=2.50: ABNORMAL: , nit=2690, max|grad|=1.3e-05, in_window=True, sigma0=0.655
- b3_d1 k=0.05 q=84.75: ABNORMAL: , nit=2620, max|grad|=3.6e-06, in_window=True, sigma0=0.846
- b3_d1 k=0.10 q=5.00: ABNORMAL: , nit=2175, max|grad|=1.3e-05, in_window=True, sigma0=0.75
- b3_d1 k=0.10 q=54.50: ABNORMAL: , nit=2939, max|grad|=2.8e-05, in_window=True, sigma0=0.853
- b3_d1 k=0.20 q=23.00: ABNORMAL: , nit=2815, max|grad|=1.5e-05, in_window=True, sigma0=0.85
- b3_d1 k=0.25 q=2.25: ABNORMAL: , nit=2426, max|grad|=1.2e-05, in_window=True, sigma0=0.667
- b3_d1 k=0.30 q=3.00: ABNORMAL: , nit=2583, max|grad|=3.0e-06, in_window=True, sigma0=0.694
- b3_d1 k=0.30 q=24.25: ABNORMAL: , nit=3181, max|grad|=1.1e-05, in_window=True, sigma0=0.851
- b3_d1 k=0.35 q=39.50: ABNORMAL: , nit=3485, max|grad|=4.3e-06, in_window=True, sigma0=0.856
- b3_d1 k=0.40 q=26.25: ABNORMAL: , nit=3202, max|grad|=1.5e-05, in_window=True, sigma0=0.852
- b3_d1 k=0.45 q=93.25: ABNORMAL: , nit=3792, max|grad|=4.7e-06, in_window=True, sigma0=0.846
- b3_d1 k=0.50 q=17.50: ABNORMAL: , nit=3164, max|grad|=4.7e-06, in_window=True, sigma0=0.838
- b3_d1 k=0.55 q=2.75: ABNORMAL: , nit=2778, max|grad|=3.1e-06, in_window=True, sigma0=0.67
- b3_d1 k=0.55 q=3.25: ABNORMAL: , nit=2712, max|grad|=1.3e-05, in_window=True, sigma0=0.689
- b3_d1 k=0.65 q=3.75: ABNORMAL: , nit=2884, max|grad|=9.3e-06, in_window=True, sigma0=0.698
- b3_d1 k=0.70 q=19.00: ABNORMAL: , nit=3162, max|grad|=2.1e-05, in_window=True, sigma0=0.839
- b3_d1 k=0.75 q=3.00: ABNORMAL: , nit=2837, max|grad|=1.5e-05, in_window=True, sigma0=0.664
- b3_d1 k=0.75 q=16.25: ABNORMAL: , nit=3250, max|grad|=1.2e-05, in_window=True, sigma0=0.83
- b3_d1 k=0.80 q=0.50: ABNORMAL: , nit=2834, max|grad|=2.1e-06, in_window=True, sigma0=0.452
- b3_d1 k=0.95 q=16.50: ABNORMAL: , nit=3165, max|grad|=1.6e-05, in_window=True, sigma0=0.826
- b5_d0.25 k=0.05 q=59.00: ABNORMAL: , nit=2293, max|grad|=9.0e-06, in_window=True, sigma0=0.818
- b5_d0.25 k=0.05 q=73.25: ABNORMAL: , nit=2316, max|grad|=7.1e-06, in_window=True, sigma0=0.813
- b5_d0.25 k=0.10 q=11.25: ABNORMAL: , nit=2194, max|grad|=4.2e-06, in_window=True, sigma0=0.818
- b5_d0.25 k=0.25 q=19.00: ABNORMAL: , nit=2801, max|grad|=6.9e-06, in_window=True, sigma0=0.834
- b5_d0.25 k=0.25 q=23.50: ABNORMAL: , nit=2934, max|grad|=5.6e-06, in_window=True, sigma0=0.835
- b5_d0.25 k=0.30 q=23.25: ABNORMAL: , nit=3078, max|grad|=2.1e-06, in_window=True, sigma0=0.835
- b5_d0.25 k=0.35 q=3.00: ABNORMAL: , nit=2412, max|grad|=5.3e-06, in_window=True, sigma0=0.685
- b5_d0.25 k=0.35 q=18.00: ABNORMAL: , nit=2909, max|grad|=2.6e-05, in_window=True, sigma0=0.833
- b5_d0.25 k=0.40 q=14.25: ABNORMAL: , nit=2790, max|grad|=5.0e-06, in_window=True, sigma0=0.827
- b5_d0.25 k=0.40 q=21.00: ABNORMAL: , nit=3081, max|grad|=5.4e-06, in_window=True, sigma0=0.835
- b5_d0.25 k=0.40 q=21.75: ABNORMAL: , nit=3018, max|grad|=4.8e-06, in_window=True, sigma0=0.835
- b5_d0.5 k=0.05 q=1.00: ABNORMAL: , nit=1232, max|grad|=4.0e-06, in_window=True, sigma0=0.548
- b5_d0.5 k=0.20 q=25.50: ABNORMAL: , nit=2873, max|grad|=1.1e-05, in_window=True, sigma0=0.814
- b5_d0.5 k=0.35 q=6.00: ABNORMAL: , nit=2406, max|grad|=5.3e-06, in_window=True, sigma0=0.751
- b5_d0.5 k=0.40 q=0.00: ABNORMAL: , nit=3519, max|grad|=1.9e-05, in_window=True, sigma0=0.283
- b5_d0.5 k=0.45 q=66.25: ABNORMAL: , nit=3819, max|grad|=1.5e-05, in_window=True, sigma0=0.797
- b5_d0.5 k=0.45 q=97.75: ABNORMAL: , nit=3738, max|grad|=9.7e-06, in_window=True, sigma0=0.788
- b5_d0.5 k=0.50 q=21.25: ABNORMAL: , nit=3121, max|grad|=7.3e-06, in_window=True, sigma0=0.814
- b5_d0.5 k=0.55 q=84.50: ABNORMAL: , nit=3911, max|grad|=4.6e-06, in_window=True, sigma0=0.792
- b5_d0.5 k=0.60 q=66.25: ABNORMAL: , nit=3699, max|grad|=1.6e-05, in_window=True, sigma0=0.798
- b5_d1 k=0.00 q=25.75: ABNORMAL: , nit=3369, max|grad|=1.0e-05, in_window=True, sigma0=0.776
- b5_d1 k=0.00 q=26.00: ABNORMAL: , nit=3342, max|grad|=9.6e-06, in_window=True, sigma0=0.776
- b5_d1 k=0.00 q=52.25: ABNORMAL: , nit=3018, max|grad|=1.8e-05, in_window=True, sigma0=0.765
- b5_d1 k=0.05 q=14.75: ABNORMAL: , nit=1830, max|grad|=1.1e-05, in_window=True, sigma0=0.771
- b5_d1 k=0.10 q=2.25: ABNORMAL: , nit=1892, max|grad|=8.8e-06, in_window=True, sigma0=0.632
- b5_d1 k=0.25 q=15.75: ABNORMAL: , nit=2720, max|grad|=1.1e-05, in_window=True, sigma0=0.773
- b5_d1 k=0.30 q=68.50: ABNORMAL: , nit=3610, max|grad|=1.3e-05, in_window=True, sigma0=0.76
- b5_d1 k=0.45 q=20.00: ABNORMAL: , nit=3156, max|grad|=3.4e-06, in_window=True, sigma0=0.776
- b5_d1 k=0.45 q=20.25: ABNORMAL: , nit=3103, max|grad|=8.5e-06, in_window=True, sigma0=0.776
- b5_d1 k=0.50 q=40.25: ABNORMAL: , nit=3384, max|grad|=1.5e-05, in_window=True, sigma0=0.771
- b5_d1 k=0.55 q=14.00: ABNORMAL: , nit=2936, max|grad|=7.2e-06, in_window=True, sigma0=0.768
- b5_d1 k=0.55 q=22.00: ABNORMAL: , nit=3107, max|grad|=8.6e-06, in_window=True, sigma0=0.776
- b5_d1 k=0.60 q=31.75: ABNORMAL: , nit=3427, max|grad|=6.6e-06, in_window=True, sigma0=0.775
- b5_d1 k=0.65 q=10.00: ABNORMAL: , nit=2982, max|grad|=7.3e-06, in_window=True, sigma0=0.752
- b5_d1 k=0.70 q=21.25: ABNORMAL: , nit=3371, max|grad|=9.7e-06, in_window=True, sigma0=0.776
- b5_d1 k=0.85 q=10.75: ABNORMAL: , nit=2959, max|grad|=7.0e-06, in_window=True, sigma0=0.753
- b5_d1 k=0.85 q=50.00: ABNORMAL: , nit=3579, max|grad|=1.1e-05, in_window=True, sigma0=0.769
- b5_d1 k=0.90 q=60.50: ABNORMAL: , nit=3675, max|grad|=1.0e-05, in_window=True, sigma0=0.766
```
