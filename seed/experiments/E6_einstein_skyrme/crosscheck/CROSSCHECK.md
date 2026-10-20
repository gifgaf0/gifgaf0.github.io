# E6 cross-check: a fold with gravity (hedgehog Einstein–Skyrme)

**Verdict: CONFIRMED WITH CORRECTIONS.** All of the following reproduce:
- every headline number, including α_crit to 10⁻¹⁴;
- the MISS of the preregistered Newtonian prediction, with its diagnosis;
- the radial stability result.

One small numerical slip: the location and value of the light-deflection maximum. The rest are wording and attribution problems. Nothing is blocking or major.

## 1. Scope and independence

- **What was read first.** I read PLAN.md §4 E6, the original REPORT and results.json. I compared against them before opening any original script.
- **Inherited code.** An earlier cross-check attempt in this directory was interrupted, and I reused its code: the derivation, the solver and the first-order scripts. I read it line by line and re-derived the key steps.
- **Changes I made:**
  - fixed its fold stage: the Moore–Spence solve hit a singular matrix, so it now uses branch bisection on τ_α;
  - finished the deflection check;
  - added the stability, extra and collection scripts;
  - reran the whole pipeline from scratch. Two runs gave byte-identical outputs.
- **Why it counts as independent.** The method differs from the original's in every component:

| | Original | Cross-check |
|---|---|---|
| Gauge | Schwarzschild-type, ds² = −σ²N dt² + dr²/N + r²dΩ² | **isotropic**, ds² = −A²dt² + ψ⁴(dx² + x²dΩ²) |
| Equations | m′, (ln σ)′, matter | Lichnerowicz ∇²ψ = −(α/2)ρψ⁵, (x²ψ²A′)′ = αx²ψ⁶A(ρ + p_r + 2p_t), matter from ∫Aψ⁶x²ρ (sympy-checked, including the Noether identity) |
| Solver | RK4 shooting in ln x, bisection; `solve_bvp` | **Chebyshev pseudo-spectral Newton** on the compactified radius x = Ls/(1 − s), Jacobians by complex step |
| Fold | max_b α(b) (Brent) | **pseudo-arclength continuation**, zero of the α-component of the branch tangent; quartic fits of α(arclength) and α(b) as second estimators |
| ADM mass | m(x≈2000) + tail | ∫x²ρψ⁵dx = ψ fall-off = Komar mass (all three agree to 10⁻¹⁰) |
| O(α) formula | −G∫(ρ + p_r)m/r dV; harmonic exchange | **isotropic-gauge expansion** m₁ = −½∫x²u(ρ₂ − 3ρ₄)dx, with ∇²u = ρ; also the Schwarzschild formula |
| Stability | own pulsation equation; finite differences in ln r; box | own pulsation derivation (sympy); **Chebyshev collocation** in the isotropic radius on isotropic-gauge backgrounds, converted pointwise to Schwarzschild variables |

The conventions follow PLAN.md:
- L = (f²/4)Tr ∂U∂U† + (1/32e²)Tr[L, L]², with f = F_π/2;
- x = efr and α = 4πGf²;
- masses are in units of 4πf/e.

## 2. Agreement table

| Quantity | Original | Cross-check | Agree |
|---|---|---|---|
| α_crit | 0.0403785252871376 | **0.04037852528715** (7 grids, N = 60–120, L = 0.4–1.2; spread 8×10⁻¹⁴) | yes (10⁻¹⁴); target 0.040378 ± 0.0002: CALIBRATED |
| b_crit; curvature of α(b) | 2.9302755; 0.014840 | 2.9302756; 0.014840 | yes |
| fold: m(∞), σ(0), min N | 4.9553901, 0.43502, 0.58260 at x = 0.660 | 4.9553901238, 0.43502274, 0.5826045 at R = 0.6604 | yes |
| flat: m₀, b_flat, E_flat | 5.803051134521, 2.007528222713, 72.92329125 f/e | 5.8030511345216, 2.0075282227, 72.92329125 f/e (E₂ − E₄ ≈ 10⁻¹²) | yes |
| fixed-α table, 12 (b, m) pairs | REPORT table | all reproduced to every printed digit (e.g. upper α = 0.001: b = 29.828334, m = 26.381753) | yes |
| M_ADM(α→0)/E_flat − 1 | −4.6×10⁻¹² | −4.5×10⁻¹² | yes (by construction) |
| m₁, full nonlinear solutions | −18.782439388 | −18.782439387 | yes |
| m₁, Newtonian ½∫ρΦ | −14.5773349 | −14.5773348 (two routes) | yes, so the **MISS (−22.4%) is confirmed** |
| m₁, GR first order | −18.7824394 | −18.7824394 (Schwarzschild formula and isotropic expansion) | yes |
| ρ × stress-trace cross term | −4.2051 | −4.2051046 (Newton + cross term = GR total, exactly) | yes |
| ∫p_r m/r ÷ ∫ρ m/r; p_r/ρ at the centre | 0.2885; 0.20 | 0.2884687; 0.20080 (p_r/ρ ≥ 0.2008 everywhere) | yes |
| d ln σ(0)/dα: full; first order | −9.74736; −9.74734 | −9.7473628; −9.7473534 | yes (the original's trapezoid omits ∫₀^{x₀}: 1.9×10⁻⁶) |
| ω², upper branch at α = 0.04, 0.035, 0.02 | −0.07841, −0.40907, −1.62158 | −0.0784058, −0.4090659, −1.6215725 (N = 80 and 120 agree to 10⁻¹⁰) | yes |
| negative modes, lower branch (α = 0, 0.02, 0.035, 0.04) | 0 | 0 | yes |
| zero crossing of the lowest ω² | b = 2.930273 (fold 2.930276) | ω² = −4.0×10⁻¹³ at the fold point itself | yes (the original's 3×10⁻⁶ offset is its inner-cut artefact) |
| √α·m(∞) → BM; b_BM | 0.82871 (linear); m_BM 0.828647; b_BM 0.4537163 | linear 0.828738; (1, α, α ln α) fit **0.828648**; (1, √α, α) 0.82847–0.82856; b²α/2 → 0.4535–0.4539 | yes (about 10⁻⁴, extrapolation-limited) |
| α_phys at f = 64.5 / 92.2 MeV | 3.5073e-40 / 7.1667e-40 | 3.507326e-40 / 7.166688e-40 | yes |
| per α: max(1 − N); 1 − σ(0) | 6.476 at x = 1.17; 9.747 | 6.47633 at 1.173; 9.74735 | yes |
| 1 − σ(0), max(1 − N), 1 − N(1 fm), 1 − σ(1 fm) at f = 64.5 | 3.42e-39, 2.27e-39 at 0.66 fm, 1.99e-39, 1.48e-40 | 3.4187e-39, 2.2715e-39 at 0.6585 fm, 1.9856e-39, 1.479e-40 | yes |
| the same at f = 92.2 | 6.99e-39, 4.64e-39 at 0.46 fm, 3.11e-39, 7.8e-41 | 6.9856e-39, 4.6414e-39 at 0.4606 fm, 3.1103e-39, 7.79e-41 | yes |
| **maximum deflection per α** | **18.8323 at b = 0.739/(ef)** | **18.8586 at b = 0.7743/(ef)** (isotropic and Schwarzschild gauges agree to 4×10⁻⁵) | **no** (minor) |
| **maximum deflection, physical** | 6.6e-39 rad at **0.41 fm**; 1.35e-38 at **0.29 fm** | 6.614e-39 rad at **0.435 fm**; 1.3515e-38 at **0.304 fm** | values yes; **locations no** (minor) |
| deflection at 1 fm (point-mass value) | 4.38e-39 (4.57e-39); 6.44e-39 (6.53e-39) | 4.3767e-39 (4.5701e-39); 6.4393e-39 (6.5327e-39) | yes |
| deflection(b = 50) ÷ 4M/b | 1 within 10⁻⁵ | 1 − 1.9×10⁻⁶ | yes |
| Shapiro delay, chord ±1 fm (Schwarzschild coordinates) | 2.0125e-62 s; 3.6228e-62 s | 2.0138e-62 s; 3.6246e-62 s | yes (the original omits [0, x₀]: −6×10⁻⁴). In isotropic coordinates the same chord gives 2.75e-62 s; it is coordinate-dependent, as the report says |
| GM/c³ | 3.811e-63 s | 3.811e-63 s | yes |

Diagnoses, from reading the original code after the comparison:
- **Deflection maximum.** `stage_phys` takes `argmax` over `np.geomspace(0.05, 50, 60)`. The grid point b = 0.739 gives 18.834, but the true maximum lies between grid points.
- **Two tiny differences**, in d ln σ(0)/dα (first order) and in the Shapiro delay. Both are the missing interval [0, x₀ = 10⁻³] in a trapezoid integral. They are negligible at the quoted precision.

## 3. Physics checks beyond reproduction

- **The equivalence-principle MISS is real.** The PLAN predicted that the O(α) coefficient would equal the Newtonian −½∫ρΦ within 1%. In isotropic gauge, M_ADM = ∫x²ρψ⁵dx, and the δF term vanishes because the flat profile is stationary. This gives m₁ = −½∫x²u(ρ₂ − 3ρ₄)dx. Using p_r + 2p_t = −ρ₂ + ρ₄, that equals ½∫x²ρu + ∫x²(p_r + 2p_t)u = −14.5773 − 4.2051 = −18.7824. My full nonlinear isotropic-gauge solutions reproduce this to 10⁻¹⁰. No reading of "Newtonian binding" rescues the 1% prediction: with Φ sourced by ρ + 3p one gets −16.68.
- **The p_ij p′_ij and −½pp′ rows cancel by an identity.** For a static, conserved, spherically symmetric stress, the Fourier transform is A(k)(δ_ij − k̂_ik̂_j). For such a tensor p_ij p_ij − ½p² = 2A² − 2A² = 0 identically. So the two rows (±0.6765) are not separate physical contributions.
- **The pulsation operator is validated independently.** At the fold, the derivative of the solution family with respect to b, taken at fixed α_crit, is a static perturbation. The lowest eigenvalue of my operator is −4×10⁻¹³ at that point. On the upper branch it then becomes negative, with slope −0.43 per unit b. Complex eigenvalues appear only at ω² ≳ 4×10³, as spurious high-frequency collocation modes.

## 4. Issues

| # | Severity | Issue | Suggested fix |
|---|---|---|---|
| 1 | minor | The deflection maximum is grid-limited. 18.83 at b = 0.739/(ef) should be 18.86 at 0.774/(ef). Physically: 6.61e-39 rad at 0.43 fm, not 0.41 fm; and 0.30 fm, not 0.29 fm, for f = 92.2 MeV. | Find the maximum with a bounded optimiser; update REPORT, headline and results.json. |
| 2 | minor | "The physical coupling is 39 orders of magnitude below α_crit": α_crit/α_phys = 1.15×10³⁸, which is 38 orders. | Say 38, or quote 8.7×10⁻³⁹. |
| 3 | minor | "Commitment 5 AMENDED" blames the seed for the PLAN's Newtonian expectation. SEED §5 already identifies "energy bends the cone" with GR, whose source is the full T_μν, and E6 solves GR by construction. Only the plain-language gloss can change, not the physics. | Keep the MISS on the PLAN prediction. Mark commitment 5 "CONFIRMED (GR by construction); wording: stress-energy, not energy density alone", or label the AMENDED as wording-only. |
| 4 | minor | By-construction identities carry verdict words. M_ADM(0)/E_flat = 1 is labelled CALIBRATED, which needs a literature target. "Light bends (4GM/b)" is labelled CONFIRMED with no by-construction caveat in seed_claims. | Label them as consistency checks. |
| 5 | minor | Provenance. The report says PLAN E6 "asks four things", including stability with a "literature note: the upper branch is unstable", light deflection, the Shapiro delay and an f = 92.2 MeV case. PLAN.md E6 contains only calibration, the EP check and the metric deviation at f = 64.5 MeV. "Upper branch unstable" is not a seed claim but is listed in seed_claims. | Label these as extensions; move the stability verdict out of seed_claims. |
| 6 | minor | The cancellation of the p_ij p′_ij and −½pp′ terms is presented as a numerical finding, but it is an exact identity. | State the identity; drop the two rows. |

## 5. Claim audit

**Supported:**
- α_crit is CALIBRATED.
- The branch structure, including the BM limit.
- E_flat.
- m₁ = −18.7824 and the 22.4% MISS of the Newtonian prediction.
- The GR first-order and exchange diagnosis: "stresses gravitate".
- Radial stability (0 and 1 negative modes; the zero mode at the fold).
- α_phys and all metric deviations.
- The deflection at 1 fm and its 4GM/b limit.
- The Shapiro delay, with its coordinate caveat.
- §7.5 "a self-gravitating fold exists": CONFIRMED.
- The equivalence principle: CONFIRMED, by construction, as the report says.

**Overstated:**
- "Commitment 5 AMENDED" (issue 3).
- "M_ADM(0)/E_flat CALIBRATED" (issue 4).

**Wrong (all minor):**
- The location and value of the deflection maximum (issue 1).
- "39 orders" (issue 2).
- "PLAN asks four things" (issue 5).

## 6. Convergence and reproducibility

- **α_crit.** Over 7 grids it ranges from 0.040378525287107 to 0.040378525287191. The τ_α = 0 estimator and the two polynomial-fit estimators agree within each grid to 3×10⁻¹⁴.
- **Flat mass.** Stable to 10⁻¹² for N ≥ 60.
- **Solutions.** The G^x_x equation, which is not imposed, holds to a residual of 10⁻⁸ or better at the fold.
- **Upper branch.** Every point was re-solved with N + 30 points and agrees to the printed digits.
- **Eigenvalues.** Bound-state eigenvalues are stable to 10⁻¹⁰ from N = 80 to 120.
- **Reproduction.** `bash crosscheck/xc_run_all.sh` runs the pipeline in about 5 minutes on one core. It is deterministic, and two runs gave identical outputs.

Files in `seed/experiments/E6_einstein_skyrme/crosscheck/`:
- `xc_derive.py`, `xc_pulsation_derive.py`: symbolic derivations;
- `xc_iso.py`, `xc_run.py`: solver and driver;
- `xc_firstorder.py`, `xc_defl_check.py`, `xc_extra.py`, `xc_stability.py`: the checks;
- `xc_collect.py`: writes `crosscheck.json`;
- `out/`, `logs/`: outputs and logs.
