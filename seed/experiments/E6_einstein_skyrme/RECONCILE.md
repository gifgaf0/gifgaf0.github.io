# E6 reconciliation: original run vs independent cross-check

**Inputs.**
- The original report and code are in `seed/experiments/E6_einstein_skyrme/`.
- The cross-check is `crosscheck/crosscheck.json`, by another agent in an isotropic gauge with Chebyshev spectral Newton, pseudo-arclength continuation and its own pulsation operator.

**Cross-check outcome.**
- Overall: "confirmed_with_corrections". 45 of 48 compared quantities agree; all 12 fixed-α (b, m) pairs agree to every printed digit.
- α_crit agrees to 10⁻¹⁴: 0.0403785252871376 here against 0.04037852528715.
- Six minor issues; no blocking or major ones.

**Method of reconciliation.**
- Each issue was settled by reading both codes and, where a number was involved, by recomputing it in the original code.
- The original scripts were fixed where they were wrong, and the affected stages were rerun. After that, the whole pipeline was rerun from scratch with `run_all.sh` (4 min 28 s). The from-scratch run reproduces the incremental reruns exactly.
- Nothing under `crosscheck/` was modified.

## Issues

### 1. Deflection maximum limited by the grid (minor; cross-check issue 1)
- **Claim in the original.** Per unit α, the maximum deflection is 18.83 at b = 0.739/(ef). Physically, 6.6×10⁻³⁹ rad at 0.41 fm (f = 64.5 MeV) and 1.35×10⁻³⁸ rad at 0.29 fm (f = 92.2 MeV).
- **Diagnosis.** The cross-check is right. `stage_phys` took the largest value on a 60-point geometric grid in b (grid ratio 1.12).
  - A bounded maximisation inside the grid bracket gives 18.858554 at b = 0.77430/(ef).
  - Re-evaluating at that b with a 4× finer z grid and a 4× smaller difference step gives 18.858554 again.
  - The cross-check has 18.858554 (isotropic gauge) and 18.858531 (Schwarzschild gauge).
- **Action.** `minimize_scalar` refinement and a quadrature check were added to `stage_phys`. The grid value is kept in `results.json` (`deflection_max_grid`).
- **Corrected numbers.** 18.86 at b = 0.774/(ef); 6.614×10⁻³⁹ rad at 0.435 fm; 1.3515×10⁻³⁸ rad at 0.304 fm. The deflection at 1 fm and the large-b limit are unchanged; the large-b agreement is 1.9×10⁻⁶ at b = 50/(ef).
- **Resolved:** yes.

### 2. "39 orders of magnitude" (minor; cross-check issue 2)
- **Diagnosis.** The cross-check is right: α_crit/α_phys = 1.151×10³⁸ (log₁₀ = 38.06), i.e. 38 orders.
- **Action.** Report text corrected. The `results.json` note now quotes α_phys/α_crit = 8.69×10⁻³⁹, computed with our α_crit rather than the rounded target.
- **Resolved:** yes.

### 3. Commitment 5 verdict AMENDED (minor; cross-check issue 3)
- **Diagnosis.** The cross-check is right in substance.
  - SEED §5 says "A massless spin-2 field coupled consistently to all energy turns out to be general relativity … The cone bending under energy is GR." GR's source is the full T_μν, and this computation solves GR exactly.
  - The 22.4% failure is the failure of PLAN E6's preregistered Newtonian prediction −½∫ρΦ, which uses the energy density only. It is not a failure of the seed's physics.
  - The word "energy" in commitment 5 is loose for a stressed soliton, but correcting it is a wording change, not a physics amendment.
- **Action.** The verdict is now **CONFIRMED (by construction; wording clarified)**.
  - The evidence keeps the full result: the defect is 1.2885 × Newtonian and equals −G∫(ρ + p_r)m/r dV to 2×10⁻⁹. It also keeps the suggested wording "stress-energy bends it".
  - The MISS remains on the PLAN prediction in the headline.
- **Resolved:** yes.

### 4. Verdict words on identities that hold by construction (minor; cross-check issue 4)
- **Diagnosis.** The cross-check is right.
  - M_ADM(α → 0)/E_flat = 1 has no literature target and holds by minimal coupling.
  - The 4GM/b deflection is weak-field GR.
- **Action.** Verdicts changed to words already used elsewhere in the series (E5):
  - M_ADM row: **CHECK PASSED (by construction)**, with source "PLAN E6 prediction; no literature target".
  - Equivalence-principle seed claim: **CONFIRMED (by construction)**.
  - SEED §5 light bending: **CONFIRMED (by construction)**, with the weak-field-GR caveat and "not preregistered".
- **Resolved:** yes.

### 5. Provenance of the questions (minor; cross-check issue 5)
- **Diagnosis.** The cross-check is right.
  - PLAN.md §4 E6 preregisters three things: calibration (α_crit and branches), the equivalence-principle check, and the metric deviation at f = 64.5 MeV.
  - It has no stability item and no "literature note".
  - Deflection, the Shapiro delay, f = 92.2 MeV and the Bartnik–McKinnon limit are extensions.
  - "Upper branch unstable" is not a seed claim. `results.json` never listed it as one, but the run summary did.
- **Action.**
  - The Question section is rewritten.
  - Each `results.json` headline entry carries `preregistered: true/false`, and the extension entries name "extension beyond PLAN.md E6" as their source.
  - Stability stays a NO_TARGET headline extension and is absent from the seed claims.
- **Resolved:** yes.

### 6. Stress–stress exchange cancellation presented as a finding (minor; cross-check issue 6)
- **Diagnosis.** The cross-check is right, and the identity was verified analytically here.
  - A spherically symmetric stress has p̃_ij(k) = A δ_ij + B k̂_i k̂_j. Conservation, k_i p̃_ij = 0, forces B = −A.
  - Then p̃_ij p̃_ij = 2A² = ½(2A)² = ½p̃² at every k, so ∫d³k (p̃_ij p̃_ij − ½p̃²)/k² = 0.
  - The numbers (−0.67647167 + 0.67647164 = −3×10⁻⁸) check the quadrature only.
- **Action.** The report's table shows the stress–stress terms as "0 (exact identity)", with the derivation. The gap is attributed entirely to the ρ × stress-trace cross term, −4.2051.
- **Resolved:** yes.

### 7. Omitted [0, x₀] pieces (noted in the cross-check comparisons)
- **Diagnosis.** The cross-check is right.
  - The first-order ∫(x² + 2 sin²F)F′²/x dx, used for d ln σ(0)/dα and 1 − σ(0), started at the first grid point x₀ ≈ 10⁻³. The missing piece b²(1 + 2b²)x₀²/2 = 1.812×10⁻⁵ accounts exactly for the difference: −9.747335 here against −9.747353 in the cross-check.
  - The ±1 fm chord delay also omitted [0, x₀], a −6×10⁻⁴ relative error.
  - Found while fixing this: the "full" σ slope used a degree-2 polynomial fit with a 10⁻⁶ truncation error. The fits give degree 2 −9.7473628, degree 3 −9.7473532, degree 4 −9.7473534.
- **Action.**
  - The series core piece was added in `stage_ep` and `stage_phys`, and the chord integral now starts at r = 0.
  - The σ-slope fit is now degree 4, with degrees 2–4 stored.
- **Corrected numbers.**
  - d ln σ(0)/dα: full −9.7473534 against first order −9.7473534, a relative difference of 2×10⁻¹⁰ (previously 2.8×10⁻⁶).
  - 1 − σ(0) = 9.747353 per α; 3.4187×10⁻³⁹ at f = 64.5 MeV and 6.9856×10⁻³⁹ at f = 92.2 MeV.
  - Shapiro delay 2.0138×10⁻⁶² s and 3.6246×10⁻⁶² s, identical to the cross-check to 4 digits.
- **Resolved:** yes.

### 8. Zero crossing of the radial ω² 3×10⁻⁶ below the fold (found during reconciliation)
- **Claims.** The original said the inner cut shifts the crossing by about 40·x_cut³ in b, about 3×10⁻⁶ at x_cut = 2.5×10⁻³. The cross-check accepted that attribution.
- **Diagnosis.** Neither side was right about the cause. 40·x_cut³ is 6×10⁻⁷ at 2.5×10⁻³, not 3×10⁻⁶. A decisive computation settled it:
  - **Method.** The crossing was located without the eigensolver, as the root in b of the end value of the ω² = 0 solution of the same FD operator (Jacobi criterion). This was done for h = 5×10⁻³, 2×10⁻³ and 10⁻³ and x_cut = 5×10⁻³, 2.5×10⁻³ and 1.25×10⁻³, at X = 400.
  - **Result.** The offset is c(x_cut) + k h², with k = −0.137 at every cut. At the production step h = 5×10⁻³ the O(h²) term is −3.4×10⁻⁶, which is the observed offset. The eigensolver's default tolerance, eps·‖T‖₁, adds a few 10⁻⁷ of noise.
  - **h → 0 limit.** The offsets are +5.7×10⁻⁶, +7.9×10⁻⁷ and +1.7×10⁻⁷ for x_cut = 5×10⁻³, 2.5×10⁻³ and 1.25×10⁻³. They are fitted by 8×10⁻⁸ + 45·x_cut³.
  - **Conclusion.** The converged zero mode sits at the fold to within 10⁻⁷, inside the 6×10⁻⁸ by which the two codes' b_crit differ. This is consistent with the cross-check's ω² = −4×10⁻¹³ at the fold point.
- **Action.** `zero_freq_end()` and a `zero_crossing_convergence` block were added to `e6_stability.py`. The earlier eigenvalues, scans and crossings are bit-identical and are labelled as not converged in h. The report's Method and Findings text is corrected.
- **Resolved:** yes.

### 9. Bartnik–McKinnon extrapolation (noted; both sides agree)
- **Diagnosis.** √α·m on the upper branch → m_BM is limited by the extrapolation. The original code now fits three bases over two ranges, α < 3×10⁻⁴ and α < 10⁻³:

  | Basis | α < 3×10⁻⁴ | α < 10⁻³ |
  |---|---|---|
  | (1, α) | 0.828710 | 0.828787 |
  | (1, √α, α) | 0.828587 | 0.828522 |
  | (1, α, α ln α) | 0.828647 | 0.828647 |

  m_BM = 0.828647 from our EYM shooting. Only the (1, α, α ln α) intercept is stable under the range change, but that form is not derived here.
- **Action.** The intercepts are stored in `results.json`. The report quotes the full spread and does not prefer a basis. The limit is supported at about 10⁻⁴.
- **Resolved:** yes (documented, not tuned).

## Files changed (all inside `seed/experiments/E6_einstein_skyrme/`)
- `e6_solve.py`:
  - `stage_ep`: series core piece in the first-order σ slope; degree-4 σ-slope fit, with degrees 2–4 stored.
  - `stage_bm`: intercepts by fit basis.
  - `stage_phys`: series core piece in 1 − σ(0); chord delay from r = 0; refined deflection maximum with a quadrature check.
- `e6_stability.py`: `zero_freq_end()`, the zero-crossing convergence study, and a corrected comment on the inner cut.
- `collect_results.py`:
  - verdict words (CHECK PASSED / CONFIRMED (by construction) / CONFIRMED (by construction; wording clarified));
  - `preregistered` flags and extension sources;
  - the converged zero crossing, BM basis spread and α_crit/α_phys in the notes;
  - a `reconciliation` record.
- Regenerated: `out/stage_*.json` (from scratch), `results.json`, `logs/*.log`, and the four figures (unchanged content, each under 75 KB).

## Final verdicts

| Item | Verdict |
|---|---|
| α_crit = 0.040378525287 (target 0.040378 ± 0.0002) | CALIBRATED |
| Branch structure | CALIBRATED |
| E_flat = 72.92329125 f/e | CALIBRATED |
| M_ADM(α → 0)/E_flat = 1 − 4.6×10⁻¹² | CHECK PASSED (by construction) |
| O(α) coefficient vs the PLAN's Newtonian −½∫ρΦ (−18.782439 vs −14.577335, 1% tolerance) | MISS (diagnosed: full slope = GR first order including stresses, to 1.7×10⁻⁹) |
| α_phys = 3.5073×10⁻⁴⁰ | CALIBRATED |
| Metric deviation, f = 64.5 MeV (1 − σ(0) = 3.42×10⁻³⁹, max(1 − N) = 2.27×10⁻³⁹) | NO_TARGET, consistent with "of order 10⁻³⁹" |
| Radial stability, deflection, Shapiro delay, f = 92.2 MeV, BM limit | NO_TARGET (extensions) |
| SEED §7.5: self-gravitating fold exists | CONFIRMED |
| SEED §2/§5: equivalence principle | CONFIRMED (by construction) |
| Commitment 5 / §5: energy bends the cone (GR) | CONFIRMED (by construction; wording clarified: stress-energy) |
| SEED §5: light bends and is delayed | CONFIRMED (by construction) |
| Scale gap | QUANTIFIED |

No discrepancy remains open.
