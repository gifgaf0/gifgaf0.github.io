# E10 / Route B, B2 (straight-string calibration) and B3 (fixed-charge feasibility): report

*November 3, 2026. Label: Exploration. Run under `PREREG_B2B3.md`, which was committed before any code (da45134). The model, normalisations and calibration targets are those of `prior_address_routeB.md` (B1). Only λ ∈ {0.8, 1.0, 1.2} and G = diag(0, 1, 0) were used. No loop was built (no B4).*

**Units.** Model units only (PREREG §1): energies per unit length in v², lengths in 1/(gv). q is the SU(3)_{C+F} charge per unit length under G, which is not electric charge. k is the twist rate along the string. No particle identification is made.

## Summary

| | Result |
|---|---|
| B2, C1–C4 | **PASS at all three λ.** C1/C2 within 2.4–4.4 × 10⁻⁴ (tolerance 10⁻³); C3 within 6 × 10⁻¹⁰; C4 within 4 × 10⁻¹¹. |
| B2, C5 (λ = 1) | **PASS:** I = 0.9993 (2D lattice) and 1.0001 (radial); prediction 1 ± 2 %. No normalisation finding. |
| B2, C6 | I = 1.1094 (λ = 0.8), 0.9331 (λ = 1.2). |
| B3 λ = 0.8 | **NONE up to q = 30 (truncated).** No 𝒯 sign change. The q cap (30) bound in rows k ≤ 0.25. min 𝒯/ℰ = +0.014, at the cap corner (k, q) = (0.25, 30). |
| B3 λ = 1.0 | **WINDOW.** 116 sign changes of 𝒯 inside the window, 107 with d²E/dR² > 0 from the interpolant. All 116 have d²E/dR² > 0 from direct solves. They form one band, k* = 0.25–0.45, q* = 15–30, **ω*/m_bulk = 0.977–0.999**. |
| B3 λ = 1.2 | **NONE.** Every q row closed naturally (no cap); 𝒯 > 0 throughout (min 𝒯/ℰ = +0.096). |
| P1 (k = 0 NONE) | **Holds** at all λ (at λ = 0.8 and 1.0 only up to the cap q = 30). The predicted mechanism holds only at λ = 1.2; at λ ≤ 1 the window had not closed by q = 30. |
| P2 | I grows with ω, much more than predicted (×5 at λ = 1 by q = 30). ω/m saturates near 0.94 at λ ≤ 1. 𝒯 stays positive at k = 0. |
| P3 | First part **holds:** no sign change anywhere with k, ω < 0.5. Second part (**NONE anywhere in the scanned window**) **fails at λ = 1**. |
| P4 | **Holds:** α = π/4 at k = 0, q > 0; α → 0 (or π, equivalently) at k > 0, q = 0. |
| Overall | **B3 finds a WINDOW (at λ = 1).** Prior was about 10 %. |
| PREREG §4 | **WINDOW somewhere:** B4 needs its own pre-registration (selection rule written first; passenger control = cheapest charged bulk lump). B4 was not run. |

**Read the following before the summary.**
- **The λ = 1 window sits at the very edge of the leak threshold.** ω*/m_bulk is 0.977–0.999, on fat strings (charge rms radius ≈ 3–3.7, I ≈ 7–15, i.e. 2.4–5 × the static I).
- **102 of the 116 sign changes use a one-sided k difference,** because the next k row's window closed at lower q. 14 use central differences in both directions (k* ≈ 0.29–0.30, q* ≈ 23.5–24.8, ω*/m ≈ 0.981). All 14 are stable, by interpolant and by direct solve.
- **The band touches the q cap.** It starts at (0.25, 30) on the cap edge. At λ = 0.8, 𝒯 at the cap corner is still falling (+0.38 at (0.25, 30)), so the λ = 0.8 NONE is not evidence of absence.
- **The thin-ring reading is doubtful here.** With the PREREG's free n, R_eq = n/k* ≈ 3.4n, against a charge rms radius ≈ 3.4. So R_eq/r_q ≈ n, and the proxy needs n ≳ 3 with Q = 2πR_eq·q* ≈ 500n.
- **This is a straight-string result only.** No loop exists or was computed.

## 1. Commands run

```
cd seed/experiments/E10_u3_vortices
pip install scipy                                     # not in the container (deviation 1)
python3 checks_lattice.py > log_checks_lattice.txt    # 2D gradient, gauge and global checks
nohup python3 b2_run.py > log_b2.txt &                # B2 (2D lattice + radial cross-check)
nohup python3 b3_scan.py > log_b3.txt &               # B3 run 1 (stopped, deviation 2) -> log_b3_run1.txt
python3 b3_pipeline.py import 0.8                     # keep run-1 rows k <= 0.10 at lam = 0.8
python3 b3_pipeline.py run >> log_b3_run2.txt         # B3 run 2 (resumed after two container restarts)
python3 b2_run.py convergence >> log_b2.txt           # B2 lam = 1 convergence entries (after the restarts)
python3 b3_compare2d.py > log_b3_compare2d.txt        # radial reduction vs full 2D at one (lam, k, q)
python3 b3_perturb2d.py > log_b3_perturb2d.txt        # symmetry-breaking perturbation of that 2D solution
python3 b3_analyse_par.py > log_b3_analysis.txt       # analysis -> b3_results.json (deviation 6)
python3 b2b3_tables.py > log_tables.txt               # read-only tables
```

`resume_all.sh` relaunches the unfinished jobs after a container restart. It was used twice.

## 2. Instrument, software, checks

### 2.1 Discretisation

**2D lattice (`u3lattice.py`), the instrument of record for B2.**
- L × L sites, spacing h. The string axis sits at a plaquette centre.
- H is a complex 3 × 3 matrix on each site.
- Links are U_μ = exp(ih W_μ) with Hermitian W_μ (9 real parameters per link), as in `gl3.py`'s non-compact link variables, but exponentiated.
- Energy terms:
  - kinetic: Σ|U H(x+μ) − H|²;
  - magnetic: Wilson plaquette, (2/h²) Σ Re Tr(1 − P);
  - potential: h²(λ²/4) Σ|1 − HH†|².
- The discretisation is exactly gauge invariant.
- Boundary: H is Dirichlet on the outermost ring (vacuum with the string's winding); all links are free.
- The gradient is analytic. The exp derivative is Daleckii–Krein in the eigenbasis of hW.
- The Gauss-law problem is minimised by preconditioned CG.

**Radial reduction (`u3radial.py`), used for B3 for speed only.** Derived in §2.3d and validated in §2.4.
- Nodes r_j = j·dr; midpoint quadrature (as E9's `option4_design`).
- Radial gauge.
- The orientation α is one extra minimisation variable.
- The Gauss law is solved exactly by a sparse LU at every outer evaluation.
- Scan grid: dr = 0.1, r_max = 20 (half-width 20). h(r_max) = 1 is Dirichlet, matching the 2D box.

Solver: L-BFGS-B.
- 2D: gtol 10⁻⁸, ftol 10⁻¹⁵.
- B3 scan: gtol 10⁻⁹, ftol 10⁻¹², maxcor 20, maxiter 20 000.

### 2.2 Checks

- **Gradient (2D), 5-point FD**, step 10⁻⁴, 40 random active coordinates, L = 12, h = 0.5, random fields:
  - static T: worst relative error 9.8 × 10⁻⁹;
  - full B3 functional T + k²I + q²/(4I), with the inner CG solve and the envelope gradient (k = 0.3, q = 1.7): 1.8 × 10⁻⁷.
- **Gradient (radial, full outer functional including α), 5-point FD:**
  - λ = 1, k = 0.3, q = 1.7: 5.8 × 10⁻⁸;
  - λ = 0.8, k = 0, q = 2.5: 8.5 × 10⁻⁸.
  - This check was made before the scan.
- **Gauge invariance.** Smooth local U(3) transformation, |θ| ≤ 0.7, on random fields. T: 1982.257189740777 before and after, i.e. equal to the printed digits. I: relative change 1.3 × 10⁻¹⁶. As a control, transforming H alone changes T to 1988.02.
- **Global SU(3)_{C+F}.** H → VHV†, W → VWV†.
  - T unchanged to round-off for a generic V.
  - I unchanged to 2.6 × 10⁻¹⁶ for V commuting with G.
  - I unchanged to 1.2 × 10⁻¹⁵ for a generic V with G → VGV†.
  - With G held fixed, I changes, as it should (26.26 against 27.54).
- **CG.** Relative residual < 10⁻¹² in every Gauss-law solve reported.

### 2.3 Derivations used by the instrument (derived here; not in the PREREG)

**(a) Gauss law.** Put H(t) = UHU†, W_i(t) = UW_iU†, U = exp(−iωtG), and Ŵ = W_t − ωG. Then:
- f_{0i} = −D_iŴ (adjoint covariant derivative);
- D_0H = i(ŴH + ωHG).

So K = ∫Tr[(D_iŴ)² + |ŴH + ωHG|²], a convex quadratic in Ŵ with source ωHG. At frozen H the minimiser is linear in ω, so K_min = ω²·I(H) exactly.

**(b) Two normalisations of I.**
- C5 defines I through E_rot/ω² → πI.
- §3 uses I(H) = K_min/ω², with ω = q/(2I). P1's "ω² = T/I ≈ 2" requires I(0) ≈ π.
- **So I_§3 = π·I_C5.** B2 tables use I_C5; B3 tables use I_§3. Flagged as ambiguity (a).

**(c) J = I.** For the twist U(kz), with Ŵ_z = W_z + kG:
- f_{zi} = −D_iŴ_z and D_zH = i(Ŵ_zH − kHG);
- this is the same quadratic form with source −kHG, so J(H) = I(H) identically;
- f_{tz} = i[Ŵ_t, Ŵ_z] = 0 at the stationary point, since Ŵ_z = −(k/ω)Ŵ_t.

Hence ℰ(k, q) = min_H[T + k²I(H) + q²/(4I(H))], and ∂_Hℰ = ∂_HT + (k² − ω²)∂_HK_unit at the inner minimiser (envelope theorem).

**(d) Radial reduction.** Take g(θ) = exp(iθN), N = diag(1, 0, 0), and
- H = g h(r),
- W_θ = g a(r) g† − N,
- W_r = g a_r(r) g†,
- Ŵ = g ŵ(r) g†.

These are invariant under a rotation combined with the gauge transformation g. Then:
- D_θH = g(iah);
- f_{rθ} = g(a′ + i[a_r, a])g†;
- D_θŴ = g i[a, ŵ] g†;
- ŴH + ωHG = g(ŵh + ωhG).

Radial gauge a_r = 0 is reachable. The orientation n = (cos α, sin α, 0) enters only through G′ = V†GV = mm†, m = (sin α, cos α, 0). Every n with the same |n₂| is related by a symmetry of the ansatz.

**(e) Consequences** (used to read the results, not to decide them).
- At frozen diagonal h, I(α) = 4·I(π/4)·sin²α cos²α, so I = 0 at α = 0 and α = π/2.
- For k > 0, stationarity in α gives (k² − ω²)∂_αI = 0. Either ω = k ("chiral branch"), or α sits at the maximum of I (π/4).
- On the chiral branch h is the static string, I = q/(2k), ℰ = T₀ + kq and 𝒯 = T₀ − kq. It exists for q < 2kI₀.
- A sign change on that branch would need k² ≥ T₀/(2I₀). The measured T₀/(2I₀) is 0.822, 0.9998 and 1.155 at λ = 0.8, 1.0 and 1.2: above the largest in-window k² at every λ. So none can occur on the branch. None did.
- The numbers confirm the branch: median |ℰ − (T₀ + kq)|/ℰ ≤ 1.3 × 10⁻¹⁰, and median |ω − k| ≈ 4 × 10⁻⁷ (but see §6, deviation 5).

### 2.4 Radial reduction against the full 2D lattice (the 1e-3 requirement)

Point: λ = 1, k = 0.2, q = 3.0, ω ≈ 0.444, α fixed at π/4 in both (ambiguity (c)).
- The 2D minimisation is over all H and W, with the inner CG solve at every evaluation.
- The 2D fields are free to break the radial symmetry.

| | ℰ | T | I |
|---|---|---|---|
| radial dr = 0.1 (scan grid) | 7.105032 | 6.304122 | 3.379808 |
| radial dr = 0.05 | 7.104117 | 6.303058 | 3.378862 |
| 2D h = 0.25 (L = 160) | 7.096108 | 6.293789 | 3.370865 |
| 2D h = 0.125 (L = 320) | 7.101896 | 6.300489 | 3.376648 |
| 2D Richardson (h → 0) | 7.103825 | 6.302722 | 3.378576 |

| relative deviation | ℰ | T | I |
|---|---|---|---|
| scan grid vs 2D h = 0.125 | 4.4 × 10⁻⁴ | 5.8 × 10⁻⁴ | 9.4 × 10⁻⁴ |
| scan grid vs 2D Richardson | 1.7 × 10⁻⁴ | 2.2 × 10⁻⁴ | 3.6 × 10⁻⁴ |
| dr = 0.05 vs 2D Richardson | 4.1 × 10⁻⁵ | 5.3 × 10⁻⁵ | 8.5 × 10⁻⁵ |

**The reduction reproduces the 2D result to < 10⁻³ in ℰ, T and I.**

Symmetry of the 2D minimum.
- The minimum keeps the 90° symmetry: max|det H − rot90| is 3 × 10⁻⁹ at h = 0.25 and 6 × 10⁻¹⁰ at h = 0.125.
- Because the 2D run starts from the equivariant configuration, a symmetric *saddle* would not show up there. `b3_perturb2d.py` tests this. It adds random symmetry-breaking noise of amplitude 0.05 to every real component of the h = 0.25 solution (energy 8441) and re-minimises.
- **The energy returns to the same value, to 1.5 × 10⁻¹¹ relative.** The asymmetry decays from 0.50 to 2.4 × 10⁻³. The residual is in a nearly flat direction (consistent with the translation modulus).
- The equivariant solution is a local minimum at this point.
- The near-threshold fat strings of the λ = 1 window were not separately validated in 2D (§8).

## 3. B2: straight-string calibration (PREREG §2)

Primary lattice: half-width 20, h = 0.125 (L = 320).
- Starting profiles: the radial (abelian-Higgs, diagonal) solution at the same λ, in the stated entries.
- Every lattice solve ended either converged or with L-BFGS-B `ABNORMAL` line-search termination at max|∇T| ≤ 4.5 × 10⁻⁷ (the floating-point floor at ftol = 10⁻¹⁵).

| ID | λ | prediction | lattice (h = 0.125) | deviation | radial (dr = 0.05) | verdict |
|---|---|---|---|---|---|---|
| C1 | 0.8 | 0.91231 | 0.912041 | −2.9 × 10⁻⁴ | 0.912348 | **PASS** (1e-3) |
| C1 | 1.0 | 1.00000 | 0.999638 | −3.6 × 10⁻⁴ | 1.000058 | **PASS** |
| C1 | 1.2 | 1.07922 | 1.078750 | −4.4 × 10⁻⁴ | 1.079297 | **PASS** |
| C2 | 0.8 | 1.77407 | 1.773649 | −2.4 × 10⁻⁴ | 1.774132 | **PASS** |
| C2 | 1.0 | 2.00000 | 1.999411 | −2.9 × 10⁻⁴ | 2.000094 | **PASS** |
| C2 | 1.2 | 2.20944 | 2.208649 | −3.6 × 10⁻⁴ | 2.209563 | **PASS** |
| C3 | 0.8 / 1.0 / 1.2 | 1/3 | 0.3333333331 / 0.3333333336 / 0.3333333327 | ≤ 6.2 × 10⁻¹⁰ | exact | **PASS** (1e-6) |
| C4 | 0.8 / 1.0 / 1.2 | 1 | 1 + 3.5 / 3.7 / 3.2 × 10⁻¹¹ | ≤ 4 × 10⁻¹¹ | — | **PASS** (1e-4) |
| C5 | 1.0 | I = 1 (2 %) | **I = 0.99928** | −0.07 % | 1.00012 | **PASS** |
| C6 | 0.8 | — | **I = 1.10939** | — | 1.11023 | reported |
| C6 | 1.2 | — | **I = 0.93308** | — | 0.93392 | reported |

Notes:
- **Discretisation errors.** The lattice values sit 2.4–4.4 × 10⁻⁴ below the targets; the radial values sit 0.6–4.0 × 10⁻⁴ above. Both are discretisation errors, of opposite sign. Eto's Table 1 numbers lie between them at every λ.
- **C3 and C4 pass by construction.** The configurations stay diagonal under the minimisation: an off-diagonal gradient at a diagonal configuration is forbidden by the U(1)³ symmetry. The diagonal entries decouple exactly, in the continuum and on the lattice. So C3 checks only that the plaquette fluxes sum to the boundary winding, and C4 checks only the solver tolerance. Both are instrument checks, not physics checks, as the PREREG's 95 % prior implies.
- **C5: no normalisation finding.** I agrees with the worldsheet β = 2π/g² at BPS.
- **The moduli inertia I (C5/C6) is exactly ω-independent.** E_rot/ω² is identical at ω = 0.01, 0.02 and 0.05 to 7 digits:

  | λ | E_rot/ω² | I (2D) | CG iterations |
  |---|---|---|---|
  | 0.8 | 3.485239 | 1.109386 | 281 |
  | 1.0 | 3.139316 | 0.999275 | 282 |
  | 1.2 | 2.931345 | 0.933076 | 284 |

  With the profile frozen, as C5 specifies, the Gauss-law minimiser is linear in ω (§2.3a). The extrapolation to ω → 0 is therefore a constant (fitted slope in ω² ~ 10⁻¹⁶). The *back-reacted* I(q) is the B3 k = 0 row (§4).
- **Rotation check.** The string rotated to n = (1,1,0)/√2 has the same static energy to 5 × 10⁻¹⁰ relative (λ = 1: 6.2809099516 against 6.2809099487). This is larger than round-off (the random-field check of §2.2 gives 10⁻¹⁶) and is not explained. It is far below every tolerance.

### 3.1 Convergence (C1 at λ = 1)

| lattice | half-width | h | T/2π | I |
|---|---|---|---|---|
| L = 160 | 20 | 0.25 | 0.9985427 | 0.997074 |
| **L = 320 (primary)** | 20 | **0.125** | **0.9996379** | **0.999275** |
| L = 480 | 30 | 0.125 | 0.9996379 | 0.999275 |

- **Halving h** (0.25 → 0.125) cuts the deviation from 1.46 × 10⁻³ to 3.6 × 10⁻⁴, a factor 4.02, so the error is O(h²). The Richardson value is T/2π = 1.0000030.
- **h = 0.25 misses C1's 10⁻³ tolerance.** That is why h = 0.125 is primary (deviation 3).
- **Enlarging the box** (half-width 20 → 30) changes T/2π by < 10⁻⁷ and I by < 10⁻⁶.
- A second halving (h = 0.0625) was started and dropped (deviation 4).

### 3.2 Tail decay lengths (descriptive)

Fit of ln(|δ|√r). Windows: r ∈ [4, 9] on the lattice (x axis), r ∈ [5, 12] on the radial grid. δ = 1 − |det H| for the scalar tail; Tr B for the vector tail.

| λ | scalar mass, expected λ (lattice / radial) | vector mass, expected 1 (lattice / radial) |
|---|---|---|
| 0.8 | 0.793 / 0.797 | 0.987 / 0.996 |
| 1.0 | 0.994 / 0.998 | 0.993 / 0.998 |
| 1.2 | 1.193 / 1.198 | 0.995 / 0.998 |

The bulk masses λ and 1 are reproduced to ≤ 1 %. The residual is consistent with sub-leading corrections to K₀ inside the fit windows.

## 4. B3: fixed-charge straight string (PREREG §3)

### 4.1 Scan

- k = 0 (primary), then k = 0.05 … 1.0; q = 0, 0.1, … per row.
- Each row stops at the first out-of-window point: ω ≥ m_bulk, or a leak > 1 % (charge fraction at r > 16).
- Safety cap q = 30 (300 steps), set before the run (deviation 2).
- Warm start: nearest solved neighbour.
- 8313 grid solves, plus 348 direct solves on the R rays.

Per (k, q) the following are recorded in `b3_results.json` (`lambdas[].solves`): ℰ, T, J (= I), I, ω, ω/m_bulk, leak fraction, α, core radius (|det h|² = ½), charge radius (rms and half-charge), 𝒯 (finite differences with flags, and envelope value T − (k² + ω²)I), 𝒯_frozen, convergence data and warm-start source.

| λ | m_bulk | solves / in window | rows capped at q = 30 | how rows closed | min 𝒯/ℰ (at k, q) | 𝒯 sign changes | d²E/dR² > 0 (interp. / direct) | verdict |
|---|---|---|---|---|---|---|---|---|
| 0.8 | 0.8 | 2855 / 2840 | k = 0 … 0.25 | k = 0.30–0.75 by ω ≥ m (q_max 20.9 → 5.9); k ≥ 0.80 at q = 0.1 (ω = k ≥ m) | +0.014 (0.25, 30) | 0 | — | **NONE up to q = 30 (truncated)** |
| 1.0 | 1.0 | 3606 / 3592 | k = 0 … 0.30 | k = 0.35–0.95 by ω ≥ m (q_max 24.8 → 6.5); k = 1.0 at q = 0.2 | **−0.027 (0.35, 24.8)** | **116** | **107 (9 undefined) / 116** | **WINDOW** |
| 1.2 | 1.0 | 1852 / 1831 | none | k = 0, 0.05 by leak (1.0 %, 1.1 %) at ω/m = 0.996, 0.998; k = 0.10–0.95 by ω ≥ m (q_max 12.7 → 6.0); k = 1.0 at q = 0.2 | +0.096 (0.95, 6.0) | 0 | — | **NONE** |

**Rows of the λ = 1 table** (𝒯 from finite differences; I and α at the last in-window q):

| k | q_max in window | closed at (q, ω/m) | min 𝒯 in row (q) | I at q_max |
|---|---|---|---|---|
| 0.00 | 30.0 (cap) | (30.0, 0.945) | +1.90 (30) | 15.88 |
| 0.10 | 30.0 (cap) | (30.0, 0.950) | +1.59 (30) | 15.79 |
| 0.20 | 30.0 (cap) | (30.0, 0.965) | +0.68 (30) | 15.54 |
| 0.25 | 30.0 (cap) | (30.0, 0.977) | +0.010 (30) | 15.36 |
| 0.30 | 30.0 (cap) | (30.0, 0.990) | **−0.58 (30)** | 15.15 |
| 0.35 | 24.8 | (24.9, 1.0001) | **−0.73 (24.8)** | 12.40 |
| 0.40 | 18.3 | (18.4, 1.0003) | **−0.25 (18.3)** | 9.15 |
| 0.45 | 15.0 | (15.1, 1.0005) | **−0.028 (15.0)** | 7.50 |
| 0.50 | 12.9 | (13.0, 1.0009) | +0.105 (12.9) | 6.45 |
| 0.70 | 8.7 | (8.8, 1.0025) | +0.30 (8.7) | 4.36 |
| 0.95 | 6.5 | (6.6, 1.0028) | +0.22 (6.5) | 3.27 |

**The λ = 1 sign changes** (all listed in `b3_results.json`, `lambdas[1].summary.sign_changes`):

| item | value |
|---|---|
| range | k* 0.251–0.45, q* 14.9–30.0, ω*/m 0.977–0.999 (count per k row: 0.25: 29, 0.30: 55, 0.35: 18, 0.40: 11, 0.45: 3) |
| f″(1) from the Clough–Tocher interpolant | +0.94 to +13.9 at 107 sign changes; undefined at 9 (the ray leaves the window hull at q > 30, all at k* ≈ 0.25, q* ≈ 29.2–30) |
| f″(1) from direct solves | +6.3 to +9.6 at all 116 (all converged); no interpolant/direct sign disagreement where both exist |
| differences | 102 use a one-sided k difference (backward), flagged; 14 are central in both directions (k* = 0.287–0.300, q* = 23.5–24.8, ω*/m = 0.981–0.982), all stable |
| lowest ω*/m (stable) | k* = 0.258, q* = 29.1, ω*/m = 0.978, f″ = +5.4 (interp.), +6.4 (direct); one-sided k |
| a representative grid point inside the band | (k, q) = (0.30, 24.0): ℰ = 25.72, T = 12.83, I = 12.21, ω/m = 0.983, α = π/4, 𝒯_fd = −0.062, 𝒯_env = −0.065, core radius 2.79, charge rms radius 3.35, leak 3.8 × 10⁻⁵ |

Here f″(1) = R_eq·d²E/dR²/(2π), from f(u) = u·ℰ(k*/u, q*/u). Its sign is that of d²E/dR², independent of the free n and Q (ambiguity (b)).

**𝒯 cross-checks.**
- Away from the edges, the finite-difference 𝒯 agrees with the envelope value T − (k² + ω²)I to a median of 5 × 10⁻⁵ ℰ.
- The largest differences (≤ 2.2 × 10⁻² ℰ) sit only at the kink where α leaves the chiral branch (q ≈ 2kI₀). There ℰ has a discontinuous second derivative, so the stencil is inaccurate.
- At λ = 1, the envelope 𝒯 is negative at 145 in-window points against the FD's 116 crossings; the two disagree in sign at 20 of 3592 points.
- At λ = 0.8 and 1.2 the envelope 𝒯 is never negative.

**Frozen-profile 𝒯 (descriptive).** 𝒯_frozen = T₀ − (k² + ω_c²)I₀, with ω_c = q/(2I₀) and (T₀, I₀) the static string at α = π/4.
- It agrees in sign with the exact 𝒯 at 1314/2840, 1765/3592 and 1605/1830 in-window points (λ = 0.8, 1.0, 1.2).
- The frozen estimate turns negative at large q, because its ω_c exceeds m_bulk there. The exact solutions keep ω < m by growing I (k = 0, λ = 1: I = 3.11 → 15.9). This is the same failure of the frozen estimate as in E9 Phase 0 §6, in the opposite direction at k = 0.

### 4.2 P1–P4

**P1 (k = 0: NONE at every λ; window closes while 𝒯 > 0).**
- NONE holds at every λ.
- At λ = 1.2 the k = 0 row closes by leak at q = 12.9 (ω/m = 0.996) with 𝒯 ≥ +3.0, as predicted.
- At λ = 0.8 and 1.0 the k = 0 row reached the cap q = 30 still in window. ω/m had saturated at 0.944 / 0.945, and 𝒯 = +2.49 / +1.90, still decreasing slowly (λ = 0.8: −0.023 per unit q over q = 25–30).
- So **the NONE part holds; the "window closes" part is not observed at λ ≤ 1 within q ≤ 30.**

**P2 (I grows as ω → m_bulk, but not enough).** Confirmed in sign, but not in mechanism.
- At k = 0, I grows from 3.11 (π·0.99) to 15.9 (λ = 1, q = 30) and to 19.9 (λ = 0.8).
- It grows roughly linearly in q, so ω = q/(2I) saturates *below* m_bulk (0.94) instead of approaching it.
- The growth is carried by a **widening core**: at λ = 0.8, core radius 1.73 → 3.75 and charge rms radius 1.55 → 4.46. That is more than the dressing tail lengthening alone.
- At λ = 1.2 the growth is milder (I → 6.4, core radius 1.28 → 1.63) and the window does close.
- 𝒯 stays positive at k = 0 throughout.

**P3 (k > 0: NONE inside k, ω < 0.5; NONE anywhere in the scanned window).**
- No sign change has ω < 0.5 (all have ω/m > 0.97), and none has k < 0.25. **The first part holds.**
- **The second part fails at λ = 1:** a WINDOW with ω*/m = 0.977–0.999.
- It holds at λ = 0.8 (truncated) and λ = 1.2.

**P4 (α ≈ π/4 at k = 0, q > 0; α → 0 or π/2 at k > 0, q = 0).** **Holds.**
- At k = 0, q > 0: α ∈ [0.7847, 0.7872] at all λ.
- At k > 0, q = 0: α_mod π ∈ {0.0000, 0.0002, π}, i.e. n → e₁, the current switched off.
- The α → π/2 branch is degenerate with α → 0 on the chiral branch (§2.3e). The α → 0 side was selected by the initial α₀ = π/4 − 0.05 (ambiguity (d)).

### 4.3 Verdicts and PREREG §4

| λ | verdict |
|---|---|
| 0.8 | **NONE up to q = 30 (truncated)** |
| 1.0 | **WINDOW** |
| 1.2 | **NONE** |

**B3 finds a WINDOW somewhere** (at λ = 1). The literal PREREG §4 consequence is:

> **WINDOW somewhere.** B4 (axisymmetric loop) gets its own pre-registration, using the same selection discipline as E9 option 4 Amendment A. The selection rule is written before B4, and the passenger control is the cheapest charged bulk lump.

B4 was not run. Whether the window, as characterised in §5, warrants B4 is the author's decision.

## 5. What the window is (descriptive)

- It lies in a narrow band just inside the leak threshold: ω/m = 0.977–0.999 at λ = 1 (m_bulk = 1 = M_V = M_s, the BPS point).
- The strings there are fat: I ≈ 7–15 (2.4–5 × static), core radius 2.1–3.1, charge rms radius 2.5–3.7.
- The charge fraction beyond r = 16 is ≤ 8 × 10⁻⁵.
- The band runs from the cap edge (k* = 0.25, q* = 30) to (0.45, 15). At smaller k it presumably continues above q = 30, which was not scanned.
- At λ = 0.8 the same trend is cut off by the cap: min 𝒯 = +0.38 at (0.25, 30), falling.
- At λ = 1.2 the leak closes the rows first. With M_s = λ > M_V = 1, the bound is the vector mass, and the string fattens less.
- This resembles E9 option 4's rescue (charge stored in a widening core) more than B1's §3 expectation, which said no metastable phase means no rescue. Here there is no metastable phase, but the core still widens: the charged core region costs potential energy, yet less than ω per unit charge.
- **Thin-ring reliability.** R_eq = n/k* ≈ 3.4n against a charge rms radius ≈ 3.4. So the thin-ring proxy needs n ≳ 3–4 to have R_eq/r_q ≥ 3, with Q = 2πR_eq q* ≈ 500n. The PREREG fixes no n (ambiguity (b)).

## 6. Deviations, collected

1. **SciPy installed with pip** (not in the container).
2. **B3 run 1 stopped; run 2 resumed with a corrected q = 0 leak rule.**
   - Run 1 (`b3_scan.py`, `log_b3_run1.txt`) evaluated the leak fraction at q = 0 from the *unit* (ω = 1) kinetic density.
   - At k > 0, q = 0, I → 0 as α → 0, so that density is numerical noise. It gave a 14.6 % "leak" at λ = 0.8 from k = 0.15 on, closing every later row at q = 0.
   - With no charge the literal test (> 1 % of the charge density near the edge) cannot fail, so run 2 sets leak := 0 at q = 0. The unit-density value is kept as `leak_unit_density`.
   - No other change was made: same functional, grid, steps, tolerances, warm-start rule and cap.
   - λ = 0.8 rows k ≤ 0.10 were imported from run 1; their decisions are unchanged by the rule (checked on import).
   - λ = 1.0 and 1.2 were recomputed from k = 0. The recomputed rows reproduce run 1's rows (e.g. λ = 1.2: k = 0 closes at q = 12.9, k = 0.05 at 13.0, k = 0.10 at 12.8, as in run 1).
   - Run 2 (`b3_pipeline.py`) solves rows concurrently. A row waits for exactly the neighbour that sequential nearest-neighbour warm-starting would use, so the warm-start chain is unchanged.
   - **The safety cap q = 30 was my addition, set before run 1** (PREREG: "until the window closes"). It bound at λ = 0.8 (k ≤ 0.25) and λ = 1.0 (k ≤ 0.30). It was not raised.
3. **Primary 2D spacing h = 0.125, not 0.25.** h = 0.25 misses C1's 10⁻³ (deviation 1.46 × 10⁻³). The convergence study halves h from 0.25 to 0.125 and enlarges the box from 20 to 30 at h = 0.125.
4. **h = 0.0625 dropped.**
   - The L = 640 solve was started twice. It ran at about 5 L-BFGS iterations per 30 min under the B3 load, and was killed by container restarts. It was then dropped.
   - The λ = 1 convergence entries (h = 0.25, and half-width 30) were computed after the restarts, by `b2_run.py convergence`, with checkpointing.
5. **Saddle at α = π/4 on part of the chiral branch.**
   - At 60 / 73 / 68 points (λ = 0.8 / 1.0 / 1.2) with k > 0 and q < 2kI₀, the warm start carried α = π/4 exactly from row k − 0.05. That is a stationary point of I(α), and a saddle of ℰ once ω < k. L-BFGS stayed there.
   - Those ℰ are up to 0.026 (≤ 0.4 %) above the true minimum T₀ + kq.
   - All are at q ≤ 5.9, where 𝒯 ≥ +0.77. On the chiral branch 𝒯 = T₀ − kq > 0 analytically (§2.3e), so no sign change is created or hidden. They do contribute to the FD-vs-envelope mismatch at the branch kink.
   - Recorded, not corrected (the warm-start rule was not changed mid-run).
6. **Analysis run in parallel.** The serial analysis (`log_b3_analysis_serial_aborted.txt`) finished λ = 0.8 and 1.2 and was stopped during λ = 1's 348 direct solves. `b3_analyse_par.py` runs the same direct solves on 4 workers, caches them, and calls the unchanged `b3_scan.analyse`.
7. **Two container restarts** killed running jobs. All jobs resumed from saved per-point files or checkpoints (`resume_all.sh`). Per-point files live outside the repository (about 400 MB); `b3_results.json` contains every point's observables.
8. **Non-converged solves.**
   - 2 of 8313 B3 grid solves (λ = 0.8, k = 0.95 and 1.0, q = 0, out-of-window-irrelevant rows; `ABNORMAL` at nit = 0, max|∇| ≤ 5.8 × 10⁻⁵, already at the warm start's minimum).
   - No B3 solve hit the 20 000-iteration cap (maximum 2923).
   - 2D solves ended `ABNORMAL` at the gradient floors listed in §3 and §2.4. The 2D h = 0.125 comparison ended at max|∇| = 2.0 × 10⁻⁶.
9. **Extra files:** `b3_perturb2d.py` (symmetry-breaking check), `b3_analyse_par.py`, `resume_all.sh`, `b2b3_tables.py`, `b3_gradcheck.json`, `b3_raw_run1_lam0.8.json` (run-1 observables).

**Ambiguities flagged for the author** (each resolved by the most literal reading).
- **(a) Two normalisations of I** (§2.3b): I_§3 = π·I_C5. P1's "T/I ≈ 2" fixes the §3 one.
- **(b) n and Q are not fixed by the PREREG** for the R ray. The sign of d²E/dR² is independent of them (f″(1) reported); R_eq and Q are not (§5).
- **(c) The 2D/radial comparison fixes α = π/4**, because the 2D box's Dirichlet edge pins the orientation.
- **(d) ω at q = 0 for k > 0** is taken as 0 (q/(2I) is 0/0 there). The α → 0 vs α → π/2 branch was chosen by the initial α₀ = π/4 − 0.05; the branches are degenerate on the chiral branch.
- **(e) 𝒯_frozen** is read as T₀ − (k² + ω_c²)I₀ with ω_c = q/(2I₀), all frozen (as E9 Phase 0's crude 𝒯).
- **(f) The window test ω < m_bulk is used as written.** For k > 0 the physical localisation bound is the weaker ω² < m² + k² (E9 Phase 0 flag (b)). The stricter test still gives a WINDOW at λ = 1.
- **(g) At k = 1.0 and λ ≥ 1, q = 0.1 is "in window"** because ω = k = 1 − O(10⁻⁶) numerically on the chiral branch. This affects no sign change.

No parameter outside the PREREG was used. `PREREG_B2B3.md`, `prior_address_routeB.md`, `NOTE_route_B.md`, `README.md` and all E9 files are unmodified.

## 7. What is and is not established

**Established:**
- The 2D U(3) lattice instrument reproduces the published straight-string tensions (C1, C2) to ≤ 4.4 × 10⁻⁴ at λ = 0.8, 1.0 and 1.2.
- The 1/3 flux and the composite = 3 × elementary hold exactly (C3, C4).
- The moduli inertia at BPS is I = 0.9993 (C5, prediction 1). Off BPS, I = 1.109 at λ = 0.8 and 0.933 at λ = 1.2.
- The tail masses are λ and 1.
- The radial reduction used for B3 reproduces the full 2D functional to < 10⁻³ at one point, and that 2D solution is a minimum, not a symmetric saddle.
- On the straight string, the fixed-charge functional has 𝒯 sign changes with d²E/dR² > 0 inside the pre-registered window at **λ = 1** (WINDOW). It has none at λ = 1.2 (NONE), and none up to q = 30 at λ = 0.8 (NONE, truncated).
- No sign change exists in the moduli-valid region k, ω < 0.5. Charge-only (k = 0) strings have 𝒯 > 0 everywhere scanned.

**Not established:**
- **No loop exists or was computed.** A straight-string WINDOW is not a vorton. A NONE does not exclude a thick one.
- **The λ = 1 window is near-threshold and fat:** ω/m ≥ 0.977, with R_eq/r_q ≈ n. The thin-ring proxy is unreliable unless n ≳ 3–4.
- The radial reduction was not validated in 2D at the window points themselves (only at ω ≈ 0.44, and only with α fixed).
- **The λ = 0.8 NONE and the extent of the λ = 1 band are set by the q = 30 cap.** Whether λ = 0.8 also has a window above q = 30 is not known.
- 102 of 116 sign changes use one-sided k differences. The 14 central ones are the cleanest evidence.
- **Classical only.** The CP² worldsheet gap (B1 §2) is outside this test.
- Whether to write a B4 pre-registration, and with which (n, Q), is the author's decision (PREREG §4).

## 8. Files

- **Code:** `u3common.py`, `u3lattice.py` (2D instrument), `u3radial.py` (radial reduction), `checks_lattice.py`, `b2_run.py`, `b3_scan.py` (run 1, and the shared solve/analysis functions), `b3_pipeline.py` (run 2), `b3_analyse_par.py`, `b3_compare2d.py`, `b3_perturb2d.py`, `b2b3_tables.py`, `resume_all.sh`.
- **Results:** `b2_results.json`, `b3_results.json` (every B3 solve; per-λ summaries with all sign changes), `b3_compare2d.json`, `b3_perturb2d.json`, `checks_lattice.json`, `b3_gradcheck.json`, `b3_raw_run1_lam0.8.json`.
- **Logs:** `log_checks_lattice.txt`, `log_b2.txt`, `log_b3_run1.txt`, `log_b3_run2.txt`, `log_b3_analysis.txt`, `log_b3_analysis_serial_aborted.txt`, `log_b3_compare2d.txt`, `log_b3_perturb2d.txt`, `log_tables.txt`.
- No field profiles are committed. They are reproducible by re-running the scripts, which are deterministic.
