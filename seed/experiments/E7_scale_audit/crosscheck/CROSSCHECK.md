# E7 cross-check: scale and coupling audit (SEED.md §8)

**Verdict: CONFIRMED WITH CORRECTIONS.** E7's conclusions and all nine seed verdicts hold. Two headline numbers are wrong and have to be corrected:

- **Demidov–Levkov (DL) exponent.** At high energy F is 3.845, not 3.93.
- **Hopfion energy-rms radius.** It is 2.061, not 2.144. This shifts the hopfion c₀ and the coupling it implies for an electron.

Two CALIBRATED labels are not earned. I compared 90 quantities with my own code: 79 agree, most to 10⁻⁹ or better, and all 11 disagreements trace back to these two errors.

Everything is in `crosscheck/`. The new second pass is the `x2_*` files. A first cross-check pass (`cc_*`, now in `cc_crosscheck.json`) was already in the folder; I re-ran it from scratch and it reproduced exactly. `crosscheck.json` combines both passes.

## 1. What I did, independently

Before the comparison I read only PLAN.md, the report and `results.json`, not E7's scripts. I wrote the second pass without the first-pass code. Methods:

**Hedgehog (`x2_hedgehog.py`): my own shooting solver.**
- Integration: DOP853 at rtol 10⁻¹³, with bisection on F′(0) down to 2 × 10⁻¹⁶.
- Euler–Lagrange equation: derived by hand and checked by finite-difference variation.
- Tails: analytic beyond the matching radius X. Massless: F = C/x² − C³/(21x⁶), with the correction term derived here. With a pion mass: Yukawa k₁ tail.
- Convergence: X = 30–60 changes Λ by 4 × 10⁻⁸. Derrick's identity holds to 10⁻¹¹.
- The first pass used Ritz-spectral minimisation instead; E7 itself used collocation.

**Hopfion (`x2_hopfion.py`): direct 3D evaluation.**
- I evaluated the Ward-normalised Faddeev–Skyrme energy of n = U e₃ U† straight from its definition: 4th-order finite differences of the explicit field, spherical Gauss quadrature, no reduced formula.
- Profile: f(r) = F_Skyrme(√2 r). I verified it rather than assuming it: E₂ = E₄, and random smooth perturbations change the energy only at second order.
- Radii: energy-rms radius, and the ring radius from minimising n₃ on the equator.
- A tail-sensitivity test, described in §3.

**DL (`x2_dl.py`).**
- Model: arXiv:1103.0013 Eq. (9), read in the source. v at δρ = 0 and 2g²M_S by quadrature.
- Figures: Fig. 3b of 1103.0013v2 and Fig. 7b of 1103.2133v2, rendered at 600 dpi.
- Axes calibrated on the tick marks on the frame, not on the label text.
- Check: the left edge of Fig. 3b reads g²E = 6.240, which equals 2g²M_S = 6.236.

**Everything else (`x2_audit.py`), by deliberately different routes.**
- Rotor and mass computed in MeV at each (e, F_π), not from the closed formula 9e⁴/(16πΛa₁).
- Semiclassical floors by root-finding, checked at two values of F_π.
- ρ_Λ from SI units: Ω_Λ · 3H₀²/(8πG) · c² · (ħc)³.
- Breit–Wheeler peak by bounded maximisation.
- E1e combination from `E1_phi4/results.json`.

**Sources read.**
- LEP (arXiv:1302.3415) Eq. (3.9): r_e < 1.1 × 10⁻¹⁹ m. The bound assumes the VV contact model with positive interference and electromagnetic coupling strength.
- Planck 2018 (arXiv:1807.06209) Eqs. (14)–(15) and Table 2: H₀ = 67.36 ± 0.54, Ω_Λ = 0.6847 ± 0.0073, Ω_Λh² = 0.3107 ± 0.0082, Λ = 4.24 × 10⁻⁶⁶ eV² = 2.846 × 10⁻¹²² m_Pl².

## 2. Agreement table (key quantities; the full table of 90 is in `crosscheck.json`)

| Quantity | Original | Cross-check | Agree |
|---|---|---|---|
| a₁ = M_cl/(F_π/e) | 36.46164562536 | 36.46164562525 (first pass: …524) | yes, 3e-12; passes the PLAN target within 0.2 % |
| Λ | 50.97874 | 50.97874 | yes, 4e-10 |
| a₂ (baryon rms, magnetic, energy rms, half-baryon) | 2.11609, 3.28613, 2.91443, 1.75263 | same | yes, ≤ 1e-9 |
| c₀ (baryon, half, energy, magnetic) | 77.156, 63.904, 106.265, 119.818 | same | yes |
| Extra radius definitions | — | mean baryon radius 69.0; 90 %-energy radius 143.4 | new |
| R_B, R_M at ANW parameters | 0.59393, 0.92233 fm | same | yes; both pass ANW's 0.59 and 0.92 ± 0.01 fm |
| M_cl, M_N, M_Δ at ANW parameters | 863.04, 936.38, 1229.76 MeV | same | yes |
| Own fit to (938.9, 1232) MeV | F_π = 129.260 MeV, e = 5.44465 | same | yes |
| Proton M R/ħc: 939 MeV × R_B, classical c₀/e², data | 2.8263, 2.5976, 3.9977 | same | yes |
| E_rot/M at ANW; floor for E_rot ≤ M; floor for E_rot ≤ 0.1 M | 0.08498; 0.75726; 2.39466 | same | yes |
| λ_C/R: LEP, SEED | 3.5105e6, 3.8616e5 | same | yes |
| e needed (LEP, baryon radius; range over radius definitions) | 16458; 14978–20509 | same | yes |
| F_π, E_rot/M, e²/16π² at the electron fold (LEP) | 230.65 MeV, 7.067e12, 1.715e6 | same | yes |
| c₀_B with a pion mass, β = 0.5 … 16 | 65.182 … 52.1447 | same | yes, ≤ 1e-10 |
| c₀_half with a pion mass, β = 16 | 47.295 (results.json only) | 47.295 | yes |
| Hopfion E_W (ansatz) | 1.2314457 | 1.2314457 (= a₁/3π²) | yes |
| Hopfion R_ring | 1.23930 | 1.23930 | yes |
| **Hopfion R_rms** | **2.1441** | **2.0608** | **no (−3.9 %)** |
| **Hopfion c₀ (rms)**; c₀ (ring) | **589.7**; 340.8 | **566.7**; 340.8 | **no**; yes |
| **Electron g² = 1/κ₄ (LEP, rms)**; √κ₂ | **2.07e9**; 84.5 MeV | **1.99e9**; 82.9 MeV | **no** |
| DL 2g²M_S; v | 6.235754; 0.745078 | same | yes |
| DL F at threshold | 4.45 ± 0.05 | 4.48 | yes |
| **DL F, high-energy plateau** | **3.93 ± 0.05** | **3.845** (first pass: 3.846) | **no (−0.085)** |
| DL g²N_min at high energy | 3.98 | 3.977 | yes |
| κ = F/N_pair | 0.630–0.714 | 0.617–0.718 | no (inherits F) |
| g² for P = 0.1, 1/e, 0.5 | 1.71, 3.93, 5.67 | 1.67, 3.84, 5.55 | no (inherits F) |
| Breit–Wheeler peak | 0.6817 πr_e² = 170.06 mb at 1.40 × 2m_e | same | yes |
| log₁₀ e^(−F/α) | −233.9 | −228.8 (−18.2 if g² = 4πα) | no (inherits F) |
| ρ_Λ; ρ_Λ^¼; Λ/m_Pl² | 2.51518e-47 GeV⁴; 2.23946 meV; 2.8445e-122 | same | yes |
| scale⁴/ρ_Λ: f_π, v, Higgs depth, reduced M_Pl, unreduced M_Pl | 2.856e42, 1.461e56, 4.718e54, 1.398e120, 8.834e122 | same (f_π ratio differs by 2e-4: 92.065 vs 92.07 MeV) | yes |
| E1e combination (PLAN-specified; not available to E7) | — | g²N_min(φ⁴) ≤ 3.38 = 2.53 N_pair; N = 2 quanta needs g² ≥ 1.69 | new; consistent with DL |

The report's worry that `solve_bvp` reached only 10⁻⁷ does not matter: two unrelated methods reproduce every hedgehog number to ≤ 10⁻⁹.

## 3. Diagnosis of the disagreements

I diagnosed both after the comparison, by reading E7's code.

**DL exponent.**
- `e7_audit.py` hard-codes `F2 = 3.93`, an eye reading.
- In Fig. 3b at 600 dpi, the tick marks 4.4, 4.2 and 4.0 sit at rows 88, 199 and 310, i.e. 555 px per unit.
- The g²N = 0 curve flattens at rows 396–397, which is F = 3.844–3.845 for g²E = 10.5–11.5.
- F = 3.93 is where the curve sits at g²E ≈ 8.4, not on the plateau.

**Hopfion R_rms.**
- `e7_hopfion.py` represents f by a 24-node not-a-knot cubic spline in t = r/(1+r), with f(1) = 0 but no condition on df/dt(1).
- A nonzero end slope means f ≈ a/r at large r. Then ε ~ r⁻⁴, and ∫r²ε d³r grows linearly until the last Gauss node.
- Energy and ring radius are insensitive to the tail; that is why they agree.
- Reproduced in `x2_hopfion.py`: adding an a/r tail with a = 2 × 10⁻³ to the exact profile moves R_rms to 2.10–2.13, depending on the radial map, while E_W changes by less than 10⁻⁶.
- The exact profile gives 2.060816 at four resolutions and two radial maps.
- The first pass's `cc_diag_hopfion_rms.py` found the same mechanism.

## 4. Issues

Two issues are **major**: headline numbers outside their stated accuracy. Neither changes a conclusion or a seed verdict.

**1. (major) DL plateau F = 3.85, not 3.93.**
- The error is outside the stated ±0.05.
- Downstream: κ = 0.62–0.72; g² for P = 0.1, 1/e, 0.5 becomes 1.67, 3.84, 5.55; M_S/m at P = 0.1 becomes 1.87; the illustrative suppression becomes 10⁻²²⁹.
- Fix: `e7_audit.py`, `results.json`, the pairs panel of `fig_vacuum_pairs.png`, REPORT.md and the summary.

**2. (major) Hopfion R_rms = 2.061, not 2.144.**
- Corrected: c₀ʰ = 341–567; an electron needs g² = 1/κ₄ ≥ 1.2–2.0 × 10⁹; √κ₂ = 82.9 MeV.
- Fix: impose f ~ C/r² in the spline, or use f(r) = F_Skyrme(√2 r).

The rest are **minor**.

**3. Hopfion "CALIBRATED" is not a calibration.**
- For this ansatz the angle-averaged energy maps exactly (r = x/√2) onto the ANW functional, so E_W = a₁/(3π²) identically: the Skyrme number again.
- The "≤ 5 % above 1.204" tolerance was set by the original agent. PLAN has no E7 hopfion target, and E8's preregistered 2 % would not pass (the excess is 2.3 %).
- Fix: relabel as "variational upper bound, consistent with 1.204–1.22".

**4. Proton M R/ħc "CALIBRATED".**
- "≈ 2.8" is a PLAN expectation, not a literature target, and the ±0.05 tolerance was set by the original agent.
- PLAN's own formula, c₀/e², gives 2.598, which is outside that tolerance. The pass relies on using M_N = 939 MeV.
- The model radius is isoscalar, while the data value uses the proton charge radius, which diverges in the massless-pion model. The comparison is indicative only.
- Fix: report 2.60 and 2.83 as CONFIRMED (the expectation "classical fold" holds).

**5. The 10⁻²³⁴ QED illustration depends on a convention.**
- It takes DL's g² to be α. With QED's loop-counting coupling g² = e² = 4πα it is 10⁻¹⁸·⁶.
- The code computes that value and the figure marks 4πα, but the text quotes only 10⁻²³⁴.
- The conclusion (QED pair creation is perturbative, σ ∝ α²) is unaffected.

**6. Pairs: E1e is now available.**
- E1's smallest classical producer reproduced at dx = 0.05 has N_lin·λ/m² = 1.688. That gives g²N_min(φ⁴) ≤ 3.38, and N = 2 quanta needs λ/m² ≥ 0.84.
- This corroborates the DL estimate; deviation 1 should be marked superseded.
- The "unsuppressed for g² ≳ 1.7–5.7" thresholds extrapolate the leading exponent e^(−F/g²) to g² of order 1. They are indicative only.

**7. Inconsistencies.**
- The floor for E_rot ≤ 0.1 M is 2.3947, printed as 2.40 in the results.json note and 2.39 in the report.
- λ_C/R and the vacuum ratios are labelled QUANTIFIED in results.json but NO_TARGET in the summary.
- "c₀ ≥ 52 with any pion mass" holds only for the baryon-rms radius; the half-baryon radius gives 47.3 at β = 16.
- The floor of 0.757 is for the baryon-rms radius; it is 0.627 with the half-baryon radius.

**8. LEP bound qualifier missing.** The VV-contact-model assumption behind r_e < 1.1 × 10⁻⁴ fm is not stated.

**9. Unlisted deviation.** PLAN says "compute c₀ from the E2 profile", but E7 solved its own hedgehog. It agrees with E2 to ≤ 10⁻⁹, so the effect is nil.

**10. "Any soliton" wording.**
- The scaling theorem M R = c₀/(g²ħ) covers one-scale, one-coupling theories. With extra dimensionless parameters c₀ can move, and only two such families were tested.
- What is fully general is the semiclassical criterion: action per light-crossing time ≈ M R c ≫ ħ, i.e. R ≫ λ_C.
- The report's General statement is careful about this; the seed-claim sentence is broader.

## 5. Claim audit

| Claim | E7 verdict | Cross-check |
|---|---|---|
| §8 proton is a classical fold | CONFIRMED | Supported. Model 2.6–2.8, data 4.0. |
| §8 electron misses by ≥ 10⁵ | AMENDED (3.5 × 10⁶) | Supported; matches PLAN §3. LEP bound is model dependent. |
| Action ∝ 1/g² ⇒ an electron-like fold needs g² ≫ 1 | CONFIRMED | Supported. Skyrme numbers verified exactly; hopfion upper end corrected (g² ≥ 1.2–2.0 × 10⁹). |
| "Strongly coupled like QCD baryons" | AMENDED | Supported. |
| Few-quanta pair folding exponentially rare at weak coupling | CONFIRMED | Supported with the corrected F; E1e corroborates it for φ⁴. |
| "Electron pairs form readily ⇒ strongly coupled" | AMENDED | Supported. REFUTED for the inference alone would also be defensible, since the strong-coupling conclusion survives only through the size argument. |
| Vacuum tension | QUANTIFIED | Supported; all numbers reproduced. |
| Weinberg–Witten | AMENDED | Supported: no composite graviton when T^μν is covariant; a neutral composite photon is allowed. |
| §2 one cone | OPEN | Supported (not tested in E7). |
| Calibrations: a₁, Λ, ANW radii, own fit, ρ_Λ, DL 2g²M_S | CALIBRATED | Supported. |
| Calibrations: hopfion E_W, proton M R/ħc | CALIBRATED | Overstated (issues 3 and 4). |

`fig_scale.png` (100 KB) and `fig_vacuum_pairs.png` (74 KB) exist and match the text, except that the pairs panel still uses F = 3.93.

## 6. Reproduce

```
cd seed/experiments/E7_scale_audit/crosscheck
./run_crosscheck.sh
```

- Runtime is about 2 minutes on one core.
- The script runs the first pass (`cc_*`, writing `cc_crosscheck.json`) and then the second pass (`x2_*`), which ends by writing `crosscheck.json`.
- The DL digitisations need the arXiv PDFs in `$LITDIR` and `$LITDIR2`. Without them, the recorded readings are used.
- `cc_diag_hopfion_rms.py` imports the original `e7_hopfion.py` read-only, for diagnosis only.
