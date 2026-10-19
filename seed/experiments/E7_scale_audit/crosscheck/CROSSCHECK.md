# E7 cross-check: scale and coupling audit (SEED.md §8)

**Verdict: CONFIRMED WITH CORRECTIONS.** I recomputed every headline number with my own code, using a different method wherever one exists:

- 61 of 70 compared quantities agree, most to 1e-9 or better.
- The other 9 come from two errors: a figure misreading (Demidov–Levkov exponent) and a radius error in the hopfion code.
- Neither error changes a conclusion or a seed verdict.
- Two CALIBRATED labels are not earned.

All files are in `crosscheck/`.

## 1. What I did, independently

I read PLAN.md §4 E7, the report and `results.json`, but not the original scripts, until the comparison below was done.

**1. Hedgehog (`cc_hedgehog.py`).** Ritz spectral energy minimisation, not the original's collocation or shooting.
- Coordinate: x = L t/(1−t).
- Trial profile: F = (1−t)²[π + t Σ c_k T_k(2t−1)]. This builds in F(0) = π and the C/x² tail.
- Solver: Newton on the exact gradient and Hessian of the Gauss–Legendre energy.
- Convergence: over N = 20…80 and L = 1.5…3, the spread is ≤ 3 × 10⁻⁸ (Λ, the most sensitive quantity).
- Extra radius definitions: mean baryon radius gives c₀ = 69.0; the 90 %-energy radius gives c₀ = 143.4.
- Pion-mass family: recomputed at β = 0…16.

**2. Hopfion (`cc_hopfion.py`).** I derived an exact identity for the hedgehog-Hopf ansatz n = Uτ₃U†:
- MMᵀ = f′²P + (s²/r²)(1−P), which gives E_W = (1/(3√2π)) ∫dr [r²f′² + 2 sin²f + 4 sin²f f′² + 2 sin⁴f/r²].
- With r = y/√2 this is exactly (1/(3π²)) × the ANW hedgehog functional.
- Hence E_W = a₁/(3π²) = 1.2314457, R_rms = x_E/√2 and R_ring = x_half/√2.
- Numerical check: I built n explicitly from SU(2) matrices and integrated the 3D central-difference energy density. Result: E_W = 1.23144567, R_rms = 2.06082. The energy is independent of φ, stationary under Derrick scaling, and gives E₂/E₄ = 1.

**3. Demidov–Levkov (DL).**
- Own quadrature of M_S at δρ = 0.
- Pixel digitisation (`cc_digitize_dl.py`) of Fig. 3b of arXiv:1103.0013v2 and Fig. 7b of arXiv:1103.2133v2.
- Axes calibrated on tick-label centres. Check: the "1.2" label of Fig. 3b sits exactly on the panel-break line, and the left edge of Fig. 3b falls at g²E = 6.240, which equals 2g²M_S.

**4. Everything else (`cc_audit.py`).**
- Electron-fold numbers from I₁ and F_π in MeV, not from the closed formula 9e⁴/(16πΛa₁).
- One-loop proxies: ħ/(MR) = e²/c₀, e²/16π², and additionally e²/a₁.
- Semiclassical floor, also with a pion mass.
- Breit–Wheeler peak by my own maximisation.
- ρ_Λ from SI constants: 3H₀²/(8πG) · c² · (ħc)³.

**5. Literature, verified in the source texts.**
- DL Eq. (9): V = ½(φ+1)²[1 − vW((φ−1)/a)], a = 0.4, with v tuned to δρ.
- LEP (arXiv:1302.3415), Eq. (3.9): r_e < 1.1 × 10⁻¹⁹ m.
- Planck 2018 (arXiv:1807.06209), Eqs. (14)–(15): H₀ = 67.36 ± 0.54, Ω_Λ = 0.6847 ± 0.0073, Ω_Λh² = 0.3107 ± 0.0082, Λ = 4.24 × 10⁻⁶⁶ eV² = 2.846 × 10⁻¹²² m_Pl².

**6. E1e combination.** E7 could not do this step because `E1_phi4` finished after it ran. I did it with E1's `e1e_results.json`.

## 2. Agreement table

| Quantity | Original | Cross-check | Agree |
|---|---|---|---|
| a₁ = M_cl/(F_π/e) | 36.46164562536 | 36.46164562524 | yes (3e-12) |
| Λ | 50.97874 | 50.97874 | yes (8e-10) |
| a₂: baryon rms, magnetic, energy rms, half-baryon | 2.11609, 3.28613, 2.91443, 1.75263 | same | yes (≤ 5e-10) |
| c₀: B, half, E, M | 77.156, 63.904, 106.265, 119.818 | same | yes |
| R_B, R_M at ANW | 0.59393, 0.92233 fm | same | yes; passes 0.59 and 0.92 ± 0.01 fm |
| M_cl, M_N, M_Δ at ANW (MeV) | 863.04, 936.38, 1229.76 | same | yes |
| Own fit to (938.9, 1232) | F_π = 129.260, e = 5.44465 | same (with 939: 129.263, 5.44399) | yes |
| Proton MR: 939 × R_B, classical c₀/e², data r_p/λ_C | 2.8263, 2.5976, 3.9977 | same | yes |
| E_rot/M at ANW | 0.08498 | 0.08498 | yes |
| Floor (MR)_min for E_rot ≤ M and ≤ 0.1 M | 0.7573, 2.3947 | same | yes |
| Floor with a pion mass (β = 1, 4, 16) | — | 0.90, 0.89, 0.88 | new |
| λ_C/R: LEP, SEED | 3.5105e6, 3.8616e5 | same | yes |
| e needed: LEP (B), LEP range, SEED (B) | 16458; 14978–20509; 5458 | same | yes |
| F_π needed (LEP) | 230.65 MeV | 230.65 MeV | yes |
| E_rot/M at electron fold: LEP, SEED | 7.067e12, 8.551e10 | same | yes |
| ħ/MR, e²/16π² (LEP) | 3.51e6, 1.715e6 | same; e²/a₁ = 7.4e6 | yes |
| Floor ÷ electron MR (LEP) | 2.658e6 | 2.658e6 | yes |
| c₀_B at β = 1, 4, 8, 16 | 60.142, 54.151, 52.846, 52.145 | 60.142, 54.151, 52.846, 52.152 | yes (β = 16 within my 4e-4 L-spread) |
| Hopfion E_W (ansatz) | 1.2314457 | 1.2314457 = a₁/(3π²) | yes |
| Hopfion R_ring | 1.2393 | 1.2393 | yes |
| **Hopfion R_rms** | **2.1441** | **2.0608** | **no (−3.9 %)** |
| **Hopfion c₀ (rms)**; c₀ (ring) | **589.7**; 340.8 | **566.7**; 340.8 | **no**; yes |
| **Hopfion g²_min (LEP, rms)**; ring | **2.07e9**; 1.20e9 | **1.99e9**; 1.20e9 | **no**; yes |
| DL 2g²M_S; v at δρ = 0 | 6.2358; 0.745078 | same | yes |
| DL F at threshold | 4.45 ± 0.05 | 4.48 | yes |
| **DL F at g²E = 11.5** | **3.93 ± 0.05** | **3.85** | **no (−0.08)** |
| DL g²N_min at high energy | 3.98 | 3.978 (near threshold 4.54) | yes |
| κ = F/N_pair; g² for P = 0.1, 1/e, 0.5 | 0.630; 1.71, 3.93, 5.67 | 0.617; 1.67, 3.85, 5.55 | no (inherits F) |
| Breit–Wheeler: σ_max/πr_e², σ_max, √s/2m_e | 0.68171, 170.06 mb, 1.4028 | same | yes |
| log₁₀ exp(−F/α) | −233.9 | −228.9 | no (inherits F) |
| ρ_Λ; ρ_Λ^¼; Λ/m_Pl² | 2.51518e-47 GeV⁴; 2.23946 meV; 2.8445e-122 | same | yes |
| scale⁴/ρ_Λ: f_π, v_EW, Higgs depth, reduced M_Pl, unreduced M_Pl | 2.856e42, 1.461e56, 4.718e54, 1.398e120, 8.834e122 | same | yes |
| E1e (φ⁴), PLAN-specified | not done | g²N_min ≤ 3.38 (2.5 N_pair); N ≤ 2 quanta needs g² ≥ 1.69 | new; consistent with DL |

The original's worry that solve_bvp reached only 10⁻⁷ is moot: an unrelated method reproduces every hedgehog number to ≤ 3 × 10⁻⁸.

## 3. Diagnosis of the disagreements

These were diagnosed after the comparison, by reading the original code.

**DL exponent.** `e7_audit.py` hard-codes `F2 = 3.93`, an eye reading of Fig. 3b.
- The figure's upper panel has tick labels 4.4, 4.2 and 4.0, each 111 px apart at 600 dpi.
- The g²N = 0 curve flattens 87 px below the "4.0" label, which is 3.84–3.85.
- The same figure appears in v1 and v2 of the paper.

**Hopfion R_rms.** `e7_hopfion.py` uses a 24-node not-a-knot cubic spline in t = r/(1+r) with f(1) = 0.
- That spline has df/dt(1) ≠ 0, which means a spurious f ≈ a/r tail.
- The energy-rms integral ∫r²ε d³r is then linearly sensitive to the tail all the way to the last Gauss node (r ≈ 2 × 10⁵).
- Feeding the exact profile through the original machinery (`cc_diag_hopfion_rms.py`) gives tail amplitudes a ≈ 5–6 × 10⁻³ and rms 2.67–2.74. The optimiser's own spline happened to give 2.14.
- The energy and the ring radius are insensitive to the tail; that is why they agree.

## 4. Issues

All issues are **minor**: none changes a headline conclusion or a seed verdict.

1. **DL plateau F = 3.85, not 3.93.** The difference is outside the stated ±0.05.
   - Downstream: κ = 0.62–0.72; g² for P = 0.1, 1/e, 0.5 becomes 1.67, 3.85, 5.55; M_S/m at P = 0.1 becomes 1.87; the hypothetical QED fold suppression becomes 10⁻²²⁹.
   - Fix: change the value in `e7_audit.py`, the figure legend, `results.json`, REPORT.md and the summary.
2. **Hopfion R_rms = 2.061, not 2.144.** This gives c₀ʰ = 341–567 and g² ≥ 1.2–2.0 × 10⁹ for the electron.
   - Fix: build (1−t)² into the trial profile, or use the identity f(r) = F_Skyrme(√2 r).
3. **Hopfion "CALIBRATED" is not an independent calibration.** E_W(ansatz) is identically a₁/(3π²), i.e. the Skyrme number again.
   - The "≤ 5 % above 1.204" tolerance was self-chosen; E8's preregistered 2 % would fail.
   - Fix: relabel as "variational upper bound, consistent with 1.204–1.22".
4. **Proton M R/ħc "CALIBRATED".** 2.8 is a PLAN expectation, not a literature target, and the ±0.05 tolerance was self-set.
   - PLAN's own definition, c₀/e² with the classical mass, gives 2.598, which is outside the tolerance. The pass relies on using M = 939 MeV.
   - Fix: report 2.83 (with M_N) and 2.60 (classical) without CALIBRATED.
5. **Pairs evidence is literature plus scaling.** No computation in this run.
   - The PLAN-specified E1e combination can now be made. It gives g²N_min ≤ 3.38 for φ⁴, so production from ≤ 2 quanta needs g² ≥ 1.69 (λ/m² ≥ 0.84). This corroborates the DL-based estimate.
   - The thresholds "unsuppressed for g² ≳ 1.7–5.7" extrapolate the leading exponent exp(−F/g²) far outside its validity. They are indicative only, and so is the shaded band in `fig_vacuum_pairs.png`.
6. **Label and rounding mismatches.**
   - `results.json` labels λ_C/R and the vacuum ratios QUANTIFIED; the summary says NO_TARGET.
   - The floor (MR)_min at E_rot ≤ 0.1 M appears as 2.40 in one place and 2.39 elsewhere (the value is 2.3947).
7. **Unlisted deviation.** PLAN says "compute c₀ from the E2 profile"; E7 solved its own hedgehog. It agrees with E2 to 10⁻¹¹, so the effect is nil.
8. **LEP bound qualifier missing.** The bound is model-dependent: it assumes the VV contact model with positive interference and electromagnetic coupling strength. The report does not say so.

## 5. Seed-claim audit

| SEED claim | E7 verdict | Cross-check |
|---|---|---|
| §8 proton is a classical fold | CONFIRMED | Supported. r_p/λ_C = 3.998; model 2.6–2.8. |
| §8 electron misses by ≥ 10⁵ | AMENDED (3.5 × 10⁶) | Supported; consistent with PLAN §3. |
| Action ∝ 1/g² ⇒ electron fold needs g² ≫ 1 | CONFIRMED | Supported. Scaling verified; Skyrme and hopfion numbers verified, apart from the minor rms correction. The floor of 0.76 also holds with a pion mass (0.88–0.90). |
| "Strongly coupled like QCD baryons" | AMENDED | Supported. |
| Few-quanta pair folding exponentially rare at weak coupling | CONFIRMED | Supported by DL plus scaling; E1e now corroborates for φ⁴. F needs a small correction. |
| "Electron pairs form readily ⇒ strongly coupled" | AMENDED | Supported. σ_BW ∝ α² is perturbative, so the observation does not imply a strongly coupled fold sector. |
| Vacuum tension | QUANTIFIED | Supported. All numbers reproduced. |
| Weinberg–Witten: no composite graviton with covariant T^μν; neutral composite photon allowed | AMENDED | Supported. |
| §2 one cone | OPEN | Supported (not tested in E7). |

Figures `fig_scale.png` and `fig_vacuum_pairs.png` exist, are under 300 KB, and match the text, except that the pairs panel uses F = 3.93.

## 6. Reproduce

```
cd seed/experiments/E7_scale_audit/crosscheck
./run_crosscheck.sh
```

- Runtime is about 75 s on one core.
- The DL digitisation needs the two arXiv PDFs in `$LITDIR`; if they are absent it is skipped and the committed `cc_dl_digitized.json` is used.
- Output: `crosscheck.json`, which holds the comparison table, the issues and the extra independent values.
- `cc_diag_hopfion_rms.py` imports the original `e7_hopfion.py` read-only, for diagnosis only, with bytecode writing disabled.
