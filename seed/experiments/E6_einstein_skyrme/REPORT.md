# E6: A fold with gravity (hedgehog Einstein–Skyrme)

## Question

SEED §5 and §7.5 couple the fold to gravity: every field shares one metric, energy bends it, and §7.5 adds gravity to a single fold. The preregistration (PLAN.md §4, E6) asks four things:

1. **Calibration.** Do the hedgehog Einstein–Skyrme equations, in the Bizon–Chmaj convention, have solutions only up to α_crit = 0.040378? Do two branches meet there, with the lower one connecting to the flat skyrmion?
2. **Equivalence principle.** As α → 0, is the ADM mass the flat-space energy (gradient and stiffness energy included) plus the Newtonian binding energy, with the O(α) coefficient correct to better than 1%?
3. **Physical scale.** At the physical coupling α ≈ 3.5 × 10⁻⁴⁰, how large are the metric deviations, the light deflection and the Shapiro delay of one fold?
4. **Stability (literature only, unless computed).** Is the upper branch unstable?

## Method

**Model and conventions.**
- Lagrangian: L = (f²/4) Tr(∂_μU ∂^μU†) + (1/32e²) Tr[U†∂_μU, U†∂_νU]², in mostly-minus form. The static Lagrangian density is −ρ in either signature.
- f = F_π/2, so ANW's F_π = 129 MeV gives f = 64.5 MeV.
- Hedgehog: U = cos F(r) + i sin F(r) n̂·τ.
- Metric: ds² = −σ²N dt² + dr²/N + r²dΩ², with N = 1 − 2GM(r)/r.
- Dimensionless variables: x = e f r and α = 4πG f². Then N = 1 − 2α m(x)/x and M_ADM = 4π (f/e) m(∞).
- Using F_π instead of f would multiply α by 4. In F_π units the fold sits at 4α_crit = 0.161514.

**Equations.** They were derived and checked symbolically in `derive_equations.py`:

    m'          = (N F'²/2)(x² + 2 sin²F) + sin²F (1 + sin²F/(2x²))
    (ln σ)'     = (α/x)(x² + 2 sin²F) F'²
    (σN(x² + 2 sin²F) F')' = σ sin 2F (1 + N F'² + sin²F/x²)

Boundary conditions:
- F(0) = π and m(0) = 0, imposed through a series at the centre.
- F → 0 at infinity, with F ~ C/x².
- σ(∞) = 1, by normalisation.

`derive_equations.py` runs these symbolic checks; all pass:
- **(A)** The reduced ρ(F, F′, N, r) equals the 2×2 matrix expression evaluated in the curved spatial metric, to a relative 10⁻³¹ at a test point.
- **(B)** The Einstein tensor of the metric gives m′ from G^t_t = 8πG T^t_t, and σ′/σ = 4πG r (ρ + p_r)/N from G^r_r − G^t_t.
- **(C)** The matter equation follows from the reduced action ∫ σ r² ρ dr.
- **(D)** The G^θ_θ equation then holds identically.
- **(E)** The dimensionless forms above are correct.
- **(F)** The series at the centre is F = π − bx + c₃x³ + c₅x⁵ and m = b²(1 + b²)x³/2 + m₅x⁵, with c₃, c₅ and m₅ derived exactly.

**Shooting.**
- Integration starts at x₀ = min(10⁻³, 2×10⁻³/b) from the series.
- Classical RK4 in t = ln x, with uniform steps h = 2×10⁻³, 10⁻³ and 5×10⁻⁴, out to x_max = 10⁶ (10⁵ and 10⁷ also checked).
- The step is split automatically on fast trajectories. Those are always non-solutions; converged solutions never trigger the split.
- Each trajectory is classified as an overshoot (F < 0), an undershoot (F′ > 0), or a horizon (N ≤ 0). If none of these happens by x_max, the sign of xF′ + 2F decides; it measures the growing mode A·x in F = Ax + C/x².

**Branch map and fold.**
- The branch parameter is b = −F′(0).
- At fixed b, α(b) is found by scanning α upward from 0 to the first change of class, then bisecting to a relative 4×10⁻¹⁶.
- α_crit = max_b α(b), from a bounded Brent maximisation (b tolerance 10⁻⁹). A quartic fit of α(b) around the maximum serves as a second estimate.
- Both branches were also solved at fixed α by bisection on b = −F′(0), at 9 values of α.
- Independent cross-check: `scipy.solve_bvp` collocation on [x₀, X] with X = 200 and 400. Here α is an unknown parameter and the outer condition is the asymptotic Robin condition xF′ + (2 + 2αm/x)F = 0. The result is again maximised over b.
- ADM mass: m at x ≈ 2000, plus the analytic tail C²/x³.

**Equivalence-principle check.**
- Ten lower-branch solutions were computed at α = 2×10⁻⁴ … 2×10⁻³. [m(α) − m₀]/α was fitted with polynomials of degree 2 to 4 to obtain m₁.
- Three expressions were evaluated on the flat profile (h = 5×10⁻⁴, Simpson rule in ln x) and compared with m₁:
  - **(i) Newtonian (the PLAN prediction).** Φ solves Poisson's equation ∇²Φ = 4πGρ_flat, via the radial Green's function; the residual of (x²Φ′)′ = x²ρ is 5×10⁻⁷. Then E_bind = ½∫ρΦ dV with Φ < 0, which is the PLAN's "−½∫ρΦ" written with Φ as a positive potential depth.
  - **(ii) GR first order, derived here.** M = ∫4πr² ρ(F, N) dr holds exactly. Expanding in G, the δF term vanishes because the flat profile F₀ extremises the flat energy. Further, ∂ρ/∂N = (ρ + p_r)/(2N) and δN = −2G m₀(r)/r. Hence **δM = −G ∫ (ρ + p_r) m₀(r)/r dV**, whereas the Newtonian formula is −G∫ρ m₀/r dV.
  - **(iii) Linearised gravity in harmonic gauge.** This is the one-graviton exchange between full stress tensors: δE = −G∬[½ρρ′ + ½(ρp′ + pρ′) + p_ij p′_ij − ½pp′]/|x − y|, with p = p_ii. It is reduced to radial integrals using the l = 0 and l = 2 Legendre terms of 1/|x − y|.
- Diagnostics: the radial and tangential stresses p_r and p_t, and the von Laue integral ∫(p_r + 2p_t) dV = 0, satisfied to 2.5×10⁻⁹.

**Physical scale.** Everything is linear in α, built on the flat profile:
- 1 − N = 2αm₀/x and −ln σ = α∫_x^∞ (y² + 2 sin²F)F′²/y dy.
- Full solutions at α = 10⁻⁶, 10⁻⁵ and 10⁻⁴ deviate from this linear prediction by 6α (relative), as expected.
- Weak-field light deflection: δ(b) = −½∫∂_b(δg₀₀ + δg_zz) dz. In Schwarzschild coordinates this gives 4GM/b for a point mass.
- Shapiro delay along a diameter: Δt = ½∫(δg₀₀ + δg_zz) dz over |z| ≤ 1 fm.
- Inputs: G = 6.70883×10⁻³⁹ GeV⁻²; e = 5.45 for both f = 64.5 MeV and f = 92.2 MeV; ħc = 197.327 MeV fm.

**Radial stability (an extension of the plan).** `derive_pulsation.py` perturbs F, m and σ in the time-dependent metric:
- G_tx gives δm = N(x² + 2 sin²F)F′ δF.
- G^x_x − G^t_t gives (δσ/σ)′. Only this derivative appears in the matter equation; this was checked symbolically.
- The result is −(pξ′)′ + qξ = ω²wξ with p = σN(x² + 2 sin²F) and w = (x² + 2 sin²F)/(σN). Self-adjointness was verified numerically to 2×10⁻⁷.
- ω is in units of e f and measured at infinity.

`e6_stability.py` solves this eigenproblem:
- Finite differences in ln x on [2.5×10⁻³, X], with Dirichlet conditions at both ends, X = 100 to 1600 and h = 5×10⁻³ and 10⁻².
- Independent count of negative modes: the number of nodes of the ω² = 0 solution (discrete Sturm criterion).
- The inner cut shifts the zero crossing by about 40·x_cut³ in b: about 4×10⁻⁵ at x_cut = 10⁻² and about 3×10⁻⁶ at 2.5×10⁻³ (the value used).

**Convergence summary.**
- α_crit = 0.040378525287189, …141 and …138 for h = 2×10⁻³, 10⁻³ and 5×10⁻⁴. The observed RK4 order is 4.03, and Richardson extrapolation gives 0.040378525287137.
- Changing x_max over 10⁵ to 10⁷ changes the result by less than 10⁻¹⁴.
- The flat-skyrmion mass is stable to 10⁻¹² across step sizes.

## Calibration

| Quantity | Ours | Target | Tolerance | Source | Verdict |
|---|---|---|---|---|---|
| α_crit, α = 4πG f², f = F_π/2 | 0.040378525287 | 0.040378 | ±0.0002 | PLAN E6 [summary: Zajac 2009; Bizon–Chmaj convention] | **CALIBRATED** |
| Branch structure | 2 branches meet at α_crit; lower → flat skyrmion | same | qualitative | PLAN E6 | **CALIBRATED** |
| Flat B = 1 energy | 72.92329125 f/e | 72.92329 f/e (E2); 1.2315 × 6π² = 72.9265 | 0.2% | E2 results.json; PLAN E2 | **CALIBRATED** (≈1e-9 vs E2; −4.4e-5 vs 1.2315 × 6π²) |
| M_ADM(α → 0)/E_flat | 1 − 4.6×10⁻¹² | 1 | 10⁻⁶ | PLAN E6 (commitment 5) | **CALIBRATED** (built in) |
| O(α) coefficient m₁, units 4πf/e: full vs Newtonian ½∫ρΦ | −18.782439 | −14.577335 | 1% | PLAN E6 prediction | **MISS** (−22.4%) |
| α_phys, f = 64.5 MeV | 3.5073×10⁻⁴⁰ | ≈ 3.5×10⁻⁴⁰ | rounding | PLAN E6 | **CALIBRATED** |
| Metric deviation at the core, f = 64.5 MeV | 1 − σ(0) = 3.4×10⁻³⁹; max(1 − N) = 2.3×10⁻³⁹ | "of order 10⁻³⁹" | order of magnitude | PLAN E6 | consistent (no formal target) |

**On the α_crit digits.** The offset from the target is +5.3×10⁻⁷, a relative 1.3×10⁻⁵. The target's six digits are our value truncated. Rounded to six digits, ours is 0.040379.

**The collocation cross-check.** `solve_bvp` gives α_crit = 0.0403785252871 for both X = 200 and X = 400, at b = 2.9302756. That agrees with shooting to 10⁻¹³.

## Findings

**1. The fold and the two branches** (`fig_branches.png`, `fig_profiles.png`).

At the fold:

| Quantity | Value |
|---|---|
| b_crit = −F′(0) | 2.9302755 |
| Curvature of α(b) at the top | α ≈ α_crit − 0.014840 (b − b_crit)² |
| m(∞) | 4.9553901 |
| M_ADM | 62.2713 f/e, 14.6% below the flat 72.9233 f/e |
| σ(0) | 0.43502 |
| min N | 0.58260, at x = 0.660 |

Solutions at fixed α. Masses are in units of 4πf/e; on both branches the recomputed α(b) agrees with α to 2×10⁻¹⁵.

| α | lower b | lower m(∞) | upper b | upper m(∞) |
|---|---|---|---|---|
| 0.001 | 2.013942 | 5.784245 | 29.8283 | 26.38175 |
| 0.01 | 2.079802 | 5.612567 | 8.85519 | 8.707867 |
| 0.02 | 2.178287 | 5.414919 | 5.83479 | 6.420543 |
| 0.03 | 2.332258 | 5.205174 | 4.35718 | 5.468599 |
| 0.04 | 2.781911 | 4.966346 | 3.10330 | 4.967786 |
| 0.04037 | 2.906579 | 4.955649 | 2.954524 | 4.955654 |

What the branches do:
- **Lower branch.** It starts at the flat skyrmion: b_flat = 2.007528222713 and m₀ = 5.803051134521.
- **Upper branch.** It is heavier than the lower branch at every α, so M(α) has a cusp at α_crit. As α → 0 it shrinks like √α.
- **Bartnik–McKinnon limit.** On the upper branch, √α·m(∞) → 0.82871 (linear extrapolation over α < 3×10⁻⁴; the smallest α computed, 2.3×10⁻⁵, gives 0.82883). The first Bartnik–McKinnon solution, computed here from the EYM equations, has b_BM = 0.4537163 and m_BM = 0.8286470. The two agree to about 10⁻⁴, limited by the extrapolation.

**2. Equivalence principle and binding** (`fig_ep.png`).
- **α⁰ order.** M_ADM(α → 0) equals the flat energy E₂ + E₄ (gradient plus Skyrme term) to 5×10⁻¹².
- **O(α) coefficient.** Fitted from the full solutions, m₁ = −18.782439. Fits of degree 2, 3 and 4 give −18.782442, −18.7824394 and −18.7824394, so m₁ is stable to 2×10⁻⁷.
- In words: M_ADM(α)/E_flat = 1 − 3.23665 α + O(α²).
- The three comparison expressions:

| Expression | Value | vs full m₁ |
|---|---|---|
| GR first order, −G∫(ρ + p_r)m/r dV | −18.7824394 | rel. 1.7×10⁻⁹ |
| Harmonic-gauge one-graviton exchange | −18.7824396 | rel. 9.5×10⁻⁹ |
| Newtonian, ½∫ρΦ with flat ρ | −14.5773349 | **22.39% too small in magnitude** |

**3. Why the Newtonian estimate misses.** The exchange energy splits into four terms:

| Term | Contribution to m₁ |
|---|---|
| ρρ′ (the Newtonian term) | −14.5773 |
| ρ × (stress trace) cross term | −4.2051 |
| p_ij p′_ij | −0.6765 |
| −½ p p′ | +0.6765 |

- The last two cancel to 5×10⁻⁸. The whole difference is therefore the coupling of the energy density to the stresses.
- In Schwarzschild gauge it appears as the radial stress p_r: p_r ≥ 0 everywhere, p_r = 0.20 ρ at the centre, and ∫p_r m/r dV = 0.2885 ∫ρ m/r dV.
- The fold is a relativistically stressed object, its stresses gravitate, and they add 28.8% to the Newtonian binding.
- This is not a numerical effect: three independent computations agree to 10⁻⁸.
- It is not a convention effect either: the sign and normalisation are fixed by M_ADM(0) = E_flat, and the Newtonian integral is reproduced in two ways (direct Poisson solution and −∫m x ρ dx) to 4×10⁻⁹.
- The O(α) dependence of σ(0) also matches first order: d ln σ(0)/dα = −9.74736 (full) against −9.74734 (first order).

**4. Radial stability** (`fig_stability.png`).
- **Lower branch, at α = 0, 0.02, 0.035 and 0.04 and in a scan up to b = 2.92.** There is no negative mode. The lowest eigenvalue is the box continuum of massless pions: 2.0×10⁻³, 5.1×10⁻⁴, 1.26×10⁻⁴ and 3.2×10⁻⁵ for X = 100, 200, 400 and 800, i.e. ∝ 1/X². The node count is 0.
- **Upper branch.** There is exactly one negative mode, independent of X to 10⁻⁶ and of h to 10⁻⁴: ω² = −0.07841, −0.40907 and −1.62158 (units (ef)²) at α = 0.04, 0.035 and 0.02. The node count is 1.
- **At the fold.** The lowest ω² crosses zero at b = 2.930272–2.930273 for X = 200 to 1600. The fold is at b_crit = 2.9302755, a difference of 3×10⁻⁶.
- **Conclusion.** The literature statement that the upper branch is unstable is reproduced here by computation, but only for spherically symmetric (radial) perturbations.

**5. The physical scale.** The ratios below are per unit α (dimensionless). Physical numbers use e = 5.45.

Per unit α:
- max(1 − N) = 6.476, at x = 1.17;
- 1 − σ(0) = 9.747;
- maximum deflection = 18.83, at impact parameter b = 0.74 (in units of 1/(ef)).

At the physical coupling:

| | f = 64.5 MeV | f = 92.2 MeV |
|---|---|---|
| α | 3.507×10⁻⁴⁰ (α/α_crit = 8.7×10⁻³⁹) | 7.167×10⁻⁴⁰ |
| M_cl | 0.863 GeV | 1.234 GeV |
| max(1 − N) | 2.27×10⁻³⁹ at 0.66 fm | 4.64×10⁻³⁹ at 0.46 fm |
| 1 − N at 1 fm | 1.99×10⁻³⁹ | 3.11×10⁻³⁹ |
| 1 − σ(0) | 3.42×10⁻³⁹ | 6.99×10⁻³⁹ |
| 1 − σ at 1 fm | 1.5×10⁻⁴⁰ | 7.8×10⁻⁴¹ |
| 1 − σ²N at the centre | 6.8×10⁻³⁹ | 1.4×10⁻³⁸ |
| maximum deflection | 6.6×10⁻³⁹ rad at b = 0.41 fm | 1.35×10⁻³⁸ rad at 0.29 fm |
| deflection at b = 1 fm (point mass) | 4.38×10⁻³⁹ (4.57×10⁻³⁹) rad | 6.44×10⁻³⁹ (6.53×10⁻³⁹) rad |
| GM/c³ | 3.8×10⁻⁶³ s | 5.4×10⁻⁶³ s |
| Shapiro delay, chord −1 fm → +1 fm | 2.0×10⁻⁶² s | 3.6×10⁻⁶² s |

Notes on the table:
- 1 − N vanishes at r = 0, because m ∝ r³ there. The "core" value is therefore the maximum of 1 − N, or the centre value of 1 − σ.
- At large impact parameter the deflection tends to the point-mass value 4GM_ADM/b; it agrees to 10⁻⁵ at b = 50/(ef).

## What it means for the seed

- **§7.5, a self-gravitating fold exists: CONFIRMED.** Regular, asymptotically flat B = 1 folds exist for 0 ≤ α ≤ 0.0403785, on two branches. Only the lower branch is radially stable. The physical coupling is 39 orders of magnitude below α_crit, so gravity cannot destabilise a single fold.
- **§2 and commitment 5, equivalence principle: CONFIRMED.** The fold's gravitational (ADM) mass at α → 0 is its total energy, gradient and stiffness terms included, to 5×10⁻¹². This follows from minimal coupling to one metric, so the computation checks consistency rather than testing the principle independently.
- **Commitment 5, "energy bends the cone": AMENDED.** The cone is bent by the whole stress-energy tensor, not by the energy density alone. PLAN E6's prediction of Newtonian binding −½∫ρΦ within 1% fails by 22.4%. The fold's O(α) mass defect is 1.2885 times the Newtonian value: it is −G∫(ρ + p_r)m/r dV, the one-graviton exchange between full stress tensors. For a soliton whose stresses are comparable to its energy density, "energy" in commitment 5 should read "stress-energy".
- **§5, light bends and is delayed: CONFIRMED** outside the fold, where the deflection is 4GM_ADM/b. Inside the core it is reduced. At the physical coupling the effects are of order 10⁻³⁸ rad and 10⁻⁶² s.
- **Scale gap: QUANTIFIED.** One fold perturbs the metric by about 10⁻³⁹ (f = 64.5 MeV). This is the expected G·M/R for a hadron, and it shows numerically why gravity plays no role in fold structure at physical parameters.

## Deviations from the plan

1. **The equivalence-principle prediction is a MISS (22.4% against a 1% tolerance).** It is reported as such, with a diagnosis rather than a correction. The sign convention was resolved as stated in Method; read literally with Φ < 0, the plan's formula would have the wrong sign as well.
2. **Added work not in the plan:**
   - radial linear stability, from a pulsation equation derived with sympy (the plan allowed a literature citation only);
   - the Bartnik–McKinnon limit of the upper branch, with BM computed here;
   - a collocation (`solve_bvp`) cross-check of α_crit;
   - two independent first-order mass formulas;
   - a check that the metric response is linear in α.
3. **e = 5.45 is used for both f values.** The notes give no e for f = 92.2 MeV. This choice affects only the conversions to fm and seconds, not the dimensionless results.
4. **The Shapiro delay is defined over a finite diametral chord (±1 fm).** For any mass the delay grows logarithmically with path length beyond the source.
5. **No independent second computation here.** PLAN §2 requires one; it is another agent's task, and `crosscheck/` was not touched.

## Limitations

- **Ansatz.** Only the spherically symmetric hedgehog, with massless pions, classical fields and no collective-coordinate quantisation. The physical-scale numbers use the classical fold.
- **Stability.** Only radial (l = 0) perturbations within the hedgehog ansatz. Non-radial and non-hedgehog modes were not examined.
- **Branches.** Only the fundamental family was mapped. The shooting classification shows further class changes at larger α (for example b ≳ 2.6 with α > α(b)), which point to other solution families. They were not followed.
- **Bartnik–McKinnon limit.** It is supported to about 10⁻⁴, limited by extrapolating the upper branch in α. The literature BM mass was not re-read; our own EYM computation is the comparison.
- **Target provenance.** α_crit = 0.040378 is a [summary] target. We did not read Zajac 2009, Bizon–Chmaj 1992 or Heusler–Droz–Straumann. The convention α = 4πG f² with f = F_π/2 is the one the notes and the plan specify.
- **Weak-field quantities.** Deflection and delay are computed to first order in α in Schwarzschild-type coordinates. The deflection at infinity is gauge-invariant; a finite-chord delay is coordinate-dependent at O(α).

## How to reproduce

From `seed/experiments/E6_einstein_skyrme/`:

    bash run_all.sh        # whole pipeline from scratch: 3 min 39 s wall on one shared core

The script sets NUMBA_NUM_THREADS=OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1 and runs these steps in order, writing logs to `logs/`:

| Step | Command | Wall time | Output |
|---|---|---|---|
| 1 | `python3 derive_equations.py` | 12 s | symbolic checks A–F, all PASS; `derived_equations.json` |
| 2 | `python3 derive_pulsation.py` | 66 s | radial pulsation coefficients; `pulsation_coeffs.json` |
| 3 | `python3 e6_solve.py` | 112 s | flat skyrmion, α_crit, branch map, fixed-α shooting, BVP check, equivalence principle, BM limit, physical scale; checkpoints in `out/stage_*.json` (resumable; delete `out/` to recompute) |
| 4 | `python3 e6_stability.py` | 27 s | `out/stage_stability.json` |
| 5 | `python3 collect_results.py` | <1 s | `results.json` (headline numbers, targets, tolerances, verdicts, details) |
| 6 | `python3 make_figures.py` | 2 s | `fig_branches.png`, `fig_profiles.png`, `fig_ep.png`, `fig_stability.png` |

The scripts are deterministic, with no random numbers. Two complete runs gave identical numbers. Requirements: Python 3.13, numpy 2.5.3, scipy 1.18.1, sympy 1.14, numba 0.68, matplotlib 3.11.
