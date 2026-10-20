# E8 reconciliation: Faddeev–Skyrme Hopf solitons

**Outcome.** The run agent's results stand, and no discrepancy is left open. The cross-check (crosscheck/CROSSCHECK.md) found no blocking or major issue and raised seven minor ones. All seven are resolved in its favour by reading both codes and, for issues 2 and 6, by short extra computations. No relaxed soliton or dx = 0.1 energy changed. What changed: the comparison conventions are now explicit, the infinite-volume and box-tail numbers are corrected, and the verdict wording is tighter.

**State found.** An earlier reconciliation attempt had been interrupted. It had only added stencil_relax.py, which was committed in 7f523ac and never run. REPORT.md and results.json were still exactly as the run agent left them, so nothing had to be undone.

## Issues and resolutions

**1. The absolute-energy CALIBRATED verdicts depend on the convention (minor).**
- *Check:* our same-box continuum energies against the cross-check's 4th-order energies of the same fields agree to −0.02%/+0.07%.
- *Finding:* the cross-check is right. At the same grid (dx = 0.1) our energies are +1.25% to +1.80% above the table: pass. Against the same-box continuum the table is −2.1, −1.8, −1.7, −2.2, −2.1, −2.0 and −2.1% low, so Q = 1, 4, 5 and 7 miss 2%. Against the infinite-volume continuum it is −1.7% for Q = 1 and 2. PLAN fixed the table and the tolerance but not the convention.
- *Change:*
  - The verdict on each E_Q row is now "CALIBRATED (same-grid comparison at dx = 0.1)".
  - Each results.json headline row carries the continuum value, the cross-check's c4 value, the deviation, and whether the 2% holds against the continuum.
  - REPORT.md adds a continuum table and states that the convention-independent calibration is the ratios (≤ 0.3% at dx = 0.1, ≤ 0.45% in the continuum) and the types.

**2. The Hopf-charge criterion depends on the estimator (minor).**
- *Check:* both estimators are correct discretisations of the Whitehead integral. The solid-angle B is exactly divergence-free on the lattice; the 4th-order finite-difference B is not.
- *Finding:* at dx = 0.1 both pass (≤ 0.004 ours, ≤ 0.007 the cross-check's). At dx = 0.2 the cross-check's estimator gives 0.068–0.086 for Q = 4–7. The new qlink_coarse.py (analysis only) computes the estimator-free linking-number charge on the dx = 0.2 and 0.15 fields: it is the exact integer for every charge, so every field at every spacing now has an exact Q_link.
- *Change:*
  - The integrality criterion is an internal check, so its verdict is now "CHECK PASSED (internal check; dx = 0.1, both estimators)" instead of CALIBRATED.
  - The solid-angle values, the cross-check's free-space values and Q_link are tabulated by dx in the report and in results.json.

**3. The E₁ literature discrepancy was called "not resolved" (minor).**
- *Finding:* the cross-check is right. Our corrected axial estimate is 1.2248 ± 0.0003 (issue 4); the cross-check's Chebyshev spectral value on all of ℝ³ is 1.2249321. They agree to 1.1 × 10⁻⁴.
- *Literature context,* checked in the arXiv texts:
  - PLAN's 1.21–1.22 is summary-grade context without a tolerance.
  - Sutcliffe 2007 writes "around 1.21", taken from several authors.
  - Ward 1999 (hep-th/9811176) quotes 1.25 K₀ from Gladikowski–Hellmund (axial) and 1.13 K₀ from Battye–Sutcliffe's 3D runs, which he calls a finite-volume underestimate. K₀ = 1 in these units.
- *Where I differ from the cross-check's wording:* with a fixed boundary the box *raises* the energy (+0.44% in the cube and +0.54% in the R = 7.5 cylinder, for Q = 1). Lattice values such as 1.204 are low because of discretisation; "finite-volume underestimate" is Ward's description of early runs only.
- *Change:* Finding 3 and the Limitations now say the question is resolved. The calibration row is CHECK PASSED (two codes agree; no preregistered tolerance).

**4. The energy beyond R = 25 and the box shifts (minor).**
- *Finding:* the cross-check is right, and the run agent's own axial data say so too.
  - A fit E(R) = E∞ + cR^{−p} to the Richardson continuum values at R = 12, 18 and 25 gives p = 3.00 for Q = 1. The energy beyond R = 25 is 1.82 × 10⁻⁴ (1.68 × 10⁻⁴ at h = 0.1), not "about 10⁻⁴".
  - The continuum shift for R 7.5 → 25 is −0.53%, and −0.55% to infinity; the cross-check has −0.52% and −0.54%.
  - For Q = 2: p = 5.02, 7 × 10⁻⁶ beyond R = 25, and a shift of −0.15% (cross-check −0.15%).
- *Side finding:* the original infinite-volume estimates 1.2243 and 1.2255 had compensating errors.
  - Both used the h = 0.1 shift, which is 0.0005 too small.
  - 1.2255 also omitted the tail.
  - 1.2243 applied the cylinder shift to the cube, which overcorrects because the cube's box effect is smaller.
  - The quoted 1.225 ± 0.001 still contains the true value.
- *Change:* make_results.py now computes the continuum shift, the tail and E∞ = E_cyl,7.5 + shift + tail with a stated uncertainty rule: E₁ = 1.2248 ± 0.0003, E₂ = 2.0004 ± 0.0001, E₂/E₁ = 1.6333, E₂/(2E₁) = 0.8166. The cube-based value (1.2236) is labelled a lower estimate. The pre-reconciliation numbers are kept in results.json.

**5. Virial attribution (minor).**
- *Finding:* the cross-check is right. Extrapolated to dx → 0 in the same box, (E₂−E₄)/E is −0.012 to −0.013 for Q = 1 (−0.026 at dx = 0.1) and −0.004 to −0.011 for Q = 2–7 (−0.015 to −0.020 at dx = 0.1). The cross-check's spectral R = 7.5 cylinder gives −0.016 (Q = 1) and −0.007 (Q = 2).
- *Change:* the report now says the sign is the boundary effect, while half or more of the dx = 0.1 magnitude is discretisation. results.json gains virial_continuum_est for every charge.

**6. The stencil explanation's wording (minor).**
- *Finding on the ratio:* the cross-check is right. The centred-to-link error ratio depends on the field: 7.5–8.2 on our Gaussian field, 7.3–10.6 on the cross-check's sharper field.
- *Decisive test of the null-mode caveat:* stencil_relax.py, single thread, about 5 minutes in total. It relaxes our Q = 1 dx = 0.1 field by arrested Newton flow, Sutcliffe's method, on the centred energies:
  - 2nd order with a 10⁻⁴ perturbation: the soliton is lost by t = 4. At t = 2, E_c is 0.60, there are 372 hedgehogs and E_link is 636.
  - 2nd order unperturbed: lost by t = 3.
  - 4th order: lost by t = 2.
  - The k = π modes are null in the gradient energy and get negative curvature from the unit-length constraint, so they grow under any descent flow.
- *What this means:* Sutcliffe's minimiser was not a descent on a pure centred energy. The Battye–Sutcliffe codes he cites discretise the field equations with 4th-order stencils, including direct second-derivative stencils that penalise grid modes (hep-th/9811077; hep-th/0103026 §2.3.2). A 4th-order energy of our fields gives 1.2302, not 1.204. The 2nd-order centred evaluation still matches all seven table values to ≤ 0.18%.
- *Change:* Finding 4b now says the ratio is field-dependent. A new Finding 4d explains that the stencil reading concerns how the energy was evaluated and remains an inference. stencil_relax.py gained `--pert` and `--log-every` options and an outcome note.

**7. Minimality caveat in the verdict words (minor).**
- *Finding:* the cross-check is right; there was one start per charge.
- *Change:* the verdicts now read "CONFIRMED as a reproduction of the literature minimum (… global minimality not re-searched: one start per charge …)" for the Q = 7 trefoil, and the same for "rings / definite knot or link". The E/Q^{3/4} claim reads "CONFIRMED (Q = 1–7)", with a note that the energies are upper bounds matching the survey.

## Final verdicts

| item | verdict |
|---|---|
| E₁…E₇ vs Sutcliffe Table 2 (2%) | CALIBRATED, same-grid comparison at dx = 0.1 (+1.25% to +1.80%); against the same-box continuum the table is 1.7–2.2% low |
| E_Q/E₁, Q = 2…7 (1%) | CALIBRATED (−0.29% to +0.25%; continuum −0.45% to +0.02%) |
| configuration types | CALIBRATED (all 7) |
| Hopf charge within 0.05 of an integer | CHECK PASSED (dx = 0.1, both estimators; Q_link exact everywhere) |
| E₁, E₂, E₂/E₁ in infinite volume | CHECK PASSED (1.2248 ± 0.0003, 2.0004 ± 0.0001, 1.6333; cross-check 1.22493, 2.00047, 1.63313) |
| seed: E/Q^{3/4} near 1.2, falling E/Q | CONFIRMED (Q = 1–7) |
| seed: E₂ < 2E₁ | CONFIRMED (0.8166 in infinite volume) |
| seed: Q = 7 is a trefoil | CONFIRMED as a reproduction of the literature minimum (one start per charge) |
| seed: 3/4 power, attribution | AMENDED |
| seed: rings, definite knots or links | CONFIRMED as a reproduction of the literature types (one start per charge) |

## Files changed or added

All in seed/experiments/E8_hopfions/:
- **Changed:** make_results.py and results.json (rerun), stencil_relax.py (options, outcome note).
- **Added:** qlink_coarse.py, qlink_coarse.json, stencil_relax.json, runs/stencil_relax_c2.log, runs/stencil_relax_c2_pert0.log, runs/stencil_relax_c4.log, runs/make_results_reconcile.out and runs/report_tables_reconcile.out.
- **REPORT.md:** corrected in place, with a Reconciliation section appended.
- **Figures:** regenerated byte-identical.
- Nothing outside the experiment folder was touched, and nothing was committed.

## Left open

No discrepancy is left open. Two limitations remain, and both are stated in the report:
- Sutcliffe's exact discretisation is unknown, so the stencil reading is an inference.
- The Q = 3–7 minima were relaxed by one code only. The cross-check re-evaluated them, but its axial A₂,₂ attempt failed.
