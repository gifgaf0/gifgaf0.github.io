# E8 cross-check: Faddeev–Skyrme Hopf solitons (Model C)

**Verdict: CONFIRMED WITH (MINOR) CORRECTIONS.**

Every headline number I could recompute agrees with the original within its stated tolerance, and most agree to better than 0.1%. I reproduced all seven configuration types and all Hopf charges with my own tools. I found no blocking or major issues.

## What I computed, and how it differs from the original

I wrote my own code in `crosscheck/` and read none of the original scripts until the comparison below was complete.

**1. Spectral axial code (`xc_axial_spectral.py`).** This is a different method from both of the original's codes.
- **Ansatz:** φ = R₃(nθ)ψ(ρ, z).
- **Representation:** ψ = u/|u|, where u is a Chebyshev–Lobatto interpolant.
- **Domains:**
  - a compactified radius r = L(1+x)/(1−x), which covers all of ℝ³, i.e. true infinite volume with no box;
  - fixed-boundary cylinders ρ ≤ R, |z| ≤ R with R = 7.5, 12 and 25.
- **Numerics:** Gauss–Legendre over-integration, an exact hand-coded gradient and L-BFGS, with the z ↔ −z reflection symmetry imposed.
- **Checks:**
  - the gradient matches finite differences to 3 × 10⁻⁸;
  - the energy of an analytic field converges spectrally (1.3206057367480 at N = 48 and at N = 96);
  - results do not depend on the map scale (L = 1.1, 1.6, 2.6 agree to 10⁻⁹);
  - the infinite-volume virial E₂ = E₄ holds to 10⁻⁶.

**2. 3D tools (`xc_lib3d.py`, tested in `xc_tests3d.py`).**
- **Energies:**
  - my own implementation of the link/plaquette energy as REPORT.md describes it;
  - a second-order centred-difference energy;
  - a fourth-order centred-difference energy;
  - a fourth-order Richardson link energy, R4 = (4E_lp(h) − E_lp(2h))/3, with an exact gradient.
- **Accuracy on an analytic test field at h = 0.1:**

  | energy | relative error |
  |---|---|
  | link/plaquette | −0.32% |
  | second-order centred | −3.27% |
  | fourth-order centred | −0.083% |
  | R4 | +0.064% |

- **Gradients** match finite differences to 2 × 10⁻⁸, 2 × 10⁻⁸ and 6 × 10⁻⁷.
- **Hopf charge** is a Whitehead integral with B from fourth-order differences and A from the free-space Green function. It uses zero padding, so there are no periodic images.
- **Curves:** a preimage-curve tracer, exact polygon linking numbers, and Alexander polynomials from projections. On test curves it gives the trefoil t² − t + 1, the figure-eight t² − 3t + 1, the unknot 1, and a Hopf link with linking number ±1.

**3. Re-evaluation of the original fields** (`xc_eval_fields.py`, `xc_eval_R4.py`). I evaluated all 28 relaxed checkpoints and the 2 box runs with the tools above.

**4. My own 3D relaxation (`xc_relax3d.py`).**
- **Method:** L-BFGS with the R4 energy in the box [−7.5, 7.5]³ with fixed boundary.
- **Spacings:** h = 0.1875 and h = 0.15625, neither of which the original used.
- **Start:** my axial solution.
- **Charges:** Q = 1 only. The Q = 2 run was stopped for the compute budget and is not used.
- **What did not work:** a fourth-order *centred* functional cannot be relaxed, because its grid-scale modes cost nothing. It unwound a relaxed Q = 1 soliton at h = 0.1875 within 300 L-BFGS steps (`xc_relax3d_c4_unwinding_test.log`).

## Agreement table

| quantity | original | cross-check | agree |
|---|---|---|---|
| E_Q at dx = 0.1 (their scheme), Q = 1…7 | 1.2226, 1.9925, 2.7885, 3.5058, 4.1639, 4.7234, 5.3362 | identical to 10⁻¹² (my implementation on their fields) | yes (bookkeeping) |
| E_Q, same-box continuum | 1.2303, 2.0024, 2.8015, 3.5212, 4.1822, 4.7427, 5.3567 | fourth-order centred on their dx = 0.1 fields: 1.2302, 2.0022, 2.8013, 3.5205, 4.1815, 4.7419, 5.3559 | yes (−0.02% to +0.07%) |
| | | R4 on the same fields: 1.2305, 2.0027, 2.8019, 3.5236, 4.1842, 4.7448, 5.3596 | |
| E₁, same-box continuum, from **my own relaxation** | 1.2303 | 1.2304 (1.228802 at h = 0.1875 and 1.229641 at h = 0.15625, h⁴ extrapolation, ±0.0003) | yes |
| E_Q/E₁, same-box continuum | 1.6275, 2.2771, 2.8620, 3.3993, 3.8548, 4.3539 | 1.6276, 2.2772, 2.8618, 3.3992, 3.8547, 4.3538 | yes |
| E₁, continuum, infinite volume | 1.225 ± 0.001 | **1.2249321** (spectral) | yes |
| E₂, continuum, infinite volume | 2.000–2.001 | 2.0004701 | yes |
| E₂/E₁ and E₂/(2E₁), infinite volume | 1.633; 0.817 | 1.63313; 0.8166 | yes |
| E₁, E₂ in the cylinder R = 7.5, continuum | 1.23154, 2.00348 | 1.231564, 2.003450 | yes (2 × 10⁻⁵) |
| box shift, R 7.5 → 25, Q = 1 and Q = 2 | −0.49%, −0.14% (lattice, h = 0.1) | continuum −0.52%, −0.15%; to infinity −0.54%, −0.15% | yes |
| energy beyond R = 25, Q = 1 | "about 10⁻⁴" | 1.8 × 10⁻⁴ | approximately (minor) |
| \|Q\| at dx = 0.1 | 0.998 … 6.996 (solid angles) | 0.9982, 1.9976, 2.9969, 3.9946, 4.9944, 5.9941, 6.9930 (free-space) | yes |
| \|Q\| at dx = 0.2, worst case | 0.017 | 0.086 (Q = 7) with my estimator | depends on the estimator |
| Q from linking numbers | exact integers | exact integers | yes |
| types, Q = 1…7 | A₁,₁, A₂,₁, Ã₃,₁, A₂,₂, L^{1,1}_{1,2}, L^{1,1}_{2,2}, K₃,₂ | the same (details below) | yes |
| centred-difference energy of their dx = 0.1 fields | 1.2044, 1.9666, 2.7534, 3.4387, 4.0948, 4.6472, 5.2450 | 1.20441, 1.96666, 2.75343, 3.43874, 4.09489, 4.64727, 5.24519 | yes |
| E/Q^{3/4} (continuum); fitted exponent p | 1.19–1.25; 0.764 (dx = 0.1) | 1.1905–1.2506; 0.763 (continuum) | yes |
| axial A₃,₁, infinite volume (new) | – | 2.822876, which is above the bent Ã₃,₁ (2.8015 in the box) | supports "bent" |

What my curve tracer found, type by type:

| Q | what my curve tracer found | type |
|---|---|---|
| 1 | a planar circle of radius 1.19 | A₁,₁ |
| 2 | a planar circle of radius 1.74, twist 2 | A₂,₁ |
| 3 | one unknot, strongly non-planar (out-of-plane rms/radius 0.22), twist 3 | Ã₃,₁ |
| 4 | two coincident, unlinked planar circles of radius 1.81, twists 2 + 2, axial | A₂,₂ |
| 5 | two unknots linked once, twists 1 and 2 | L^{1,1}_{1,2} |
| 6 | two unknots linked once, twists 2 and 2 | L^{1,1}_{2,2} |
| 7 | one loop with Alexander polynomial t² − t + 1 in 3 projections, on both the dx = 0.15 and dx = 0.1 fields; Q_link = 7 | K₃,₂ |

What I could not cross-check:
- **A₂,₂ axial energy.** My spectral code did not hold the A₂,₂: the u/|u| representation let deg ψ unwind from 2 to 0, from two different starts. This is a limitation of my method, not a finding. The Q = 4 energy is therefore cross-checked only by re-evaluating their field.
- **Charges 3–7.** These were not independently minimised from scratch.

## Diagnosis

There are no disagreements to diagnose. After the comparison I read the original code; it implements what the report describes:
- the link/plaquette energy;
- arrested Newton flow with the stated safeguards;
- the Whitehead integral with solid-angle fluxes;
- the K32_Q5 map Z₁Z₀/(Z₁³ + Z₀²), which is Sutcliffe's K₃,₂ → L^{1,1}_{1,2} route from his Table 1.

The stop files and stage JSONs match the deviation table.

## Audit of the report

**Supported:**
- every number in the calibration and findings tables that I checked against results.json and against my own recomputations: the deviations from the table, the continuum ratios, the dx = 0.2 comparison, the box study, the splitting margins and the power law;
- the seed verdicts: E/Q^{3/4} is near 1.2 and E/Q falls (CONFIRMED); E₂ < 2E₁ (CONFIRMED; 0.8166 in infinite volume); Q = 7 is a trefoil-type minimum (CONFIRMED, with the global-minimality caveat stated); the 3/4 power is AMENDED to credit Lin & Yang, and Sutcliffe 2007 §2 does cite its ref. 10 for the optimality.
- the citations: Sutcliffe's "around 1.21", "about 1% low" and "relative energies about 0.1%" appear in the arXiv text, and so do his Table 1 routes (K₃,₂ → L^{1,1}_{2,2} at Q = 6; L^{1,1}_{2,3} → K₃,₂ at Q = 7).
- the four figures exist and are each under 80 KB.

**Issues (all minor):**

1. **The absolute-energy CALIBRATED verdicts depend on the convention.** They pass at the same grid (+1.25% to +1.80%). Against the same-box continuum, which my fourth-order energies confirm, Sutcliffe's table is 1.7–2.2% low, so Q = 1, 4, 5 and 7 would miss 2%. The report discloses this in Finding 4a. The headline rows should say so, and should note that the calibration rests robustly on the ratios (≤ 0.3%) and the types.
2. **The Hopf-charge deviation depends on the estimator.** The figure "max |Q − n| = 0.017" is for the solid-angle estimator. A finite-difference estimator gives up to 0.086 at dx = 0.2. The linking-number charge, which is an exact integer, is the estimator-free check and should be named in the verdict.
3. **The E₁ literature "discrepancy" is settled in the original's favour, not left open.** The infinite-volume continuum value is 1.2249321, which confirms 1.225 and E₁ ≥ 1.223. The 1.21–1.22 range is a summary-grade target that leaves out higher published values; Gladikowski–Hellmund's axial result is 1.25, as quoted by Ward 1999. The values near 1.21 are lattice and finite-box underestimates.
4. **The box tail is 1.8 × 10⁻⁴, not "about 10⁻⁴".** That is the Q = 1 energy beyond R = 25. The continuum box shift from 7.5 to 25 is −0.52% (−0.54% to infinity), against the −0.49% quoted at h = 0.1.
5. **The virial is mostly discretisation at dx = 0.1.** The sign, E₄ > E₂, is the boundary effect. But about half of the −0.026 at Q = 1 is lattice artefact: the same-box continuum value is about −0.012, and the R = 7.5 cylinder gives −0.016.
6. **The stencil inference needs softening.** The "≈ 8×" truncation-error ratio depends on the field; it is about 10× on my sharper test field. A purely centred functional also has grid-scale null modes, as the unwinding test shows. So Sutcliffe's exact scheme remains unknown. The report already labels this an inference.
7. **The "minimum" verdicts use one initial condition per charge.** "Q = 7 is a trefoil" and "each charge's minimum is a definite knot or link" are each CONFIRMED from one initial condition, so global minimality comes from Sutcliffe's survey. The report states this caveat; the verdict wording could carry it too.

## Files

All in `crosscheck/`. Field checkpoints are kept in the scratchpad, outside the repository.
- **Scripts:** `xc_axial_spectral.py`, `xc_axial_a22.py`, `xc_lib3d.py`, `xc_tests3d.py`, `xc_eval_fields.py`, `xc_eval_R4.py`, `xc_relax3d.py`, `xc_summary.py`.
- **Results:** `xc_axial.json`, `xc_axial_a22.json`, `xc_fields.json`, `xc_R4_fields.json`, `xc_relax3d.json`, `xc_tests3d.json`, and `crosscheck.json`, which holds the full comparison.
- **Logs:** the `*.log` files.
