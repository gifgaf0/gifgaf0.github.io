# ρ Derivation — Notes

**Brief:** CLAUDE_CODE_BRIEF_08_RHO_DERIVATION.md
**Code:** `tools/rho_derivation.py`
**Tests:** `tools/test_rho_derivation.py` — 13/13 passing on first run
**Citable output:** `reports/rho_derivation_output.txt`

## Computed values

| Quantity | Value |
|---|---|
| Triangle area | π/42 ≈ 0.074800 |
| Side opposite π/2 (a) | 0.620672 |
| sinh(R_hyp) = sinh(a)/2 | 0.330648 |
| R_hyp | **0.324902** |
| L / λ̄_p = 14 × (7/2) | **49** |
| φ = (1+√5)/2 | 1.618034 |
| cos(π/10) ≡ √(2+φ)/2 | 0.951057 (identity verified to 1e-12) |
| ζ = 1 − π/√12 | 0.093100 |
| 1 − cos 18° | 0.048943 |
| Void correction ζ(1−cos 18°) | 0.004557 |
| Factor 1 + correction | 1.004557 |
| **ρ_structural** = R_hyp × 49/4 | **3.980050** |
| **ρ_predicted** = ρ_structural × (1 + correction) | **3.998186** |
| **r_p (predicted)** = ρ_predicted × λ̄_p | **0.840854 fm** |
| ρ_muon (Pohl 2013) | 3.998261 |
| r_p_muon | 0.84087 fm |
| **Error vs muonic H** | **0.0019%** |
| Error vs α-matched | 0.276% |

## Vs Brief 08 expectations

- DoD: error vs muonic H < 0.01% — passed (0.0019%).
- Spec §3.3 quoted `ρ_predicted = 3.998185` and "0.002%" error; we
  compute 3.998186 and 0.0019% with no rounding (CODATA λ̄_p =
  0.21030892 fm, the value the brief specifies). Agreement at the
  6th significant figure / 4th decimal of the percentage.
- All 13 tests passed on first run.
- R/r = 168/42 evaluates to exactly 4.0 in IEEE 754 (verified by
  `test_r_over_r_is_4` using `==`, not `isclose`).
- The cos 18° identity `√(2+φ)/2 == cos(π/10)` is verified to
  abs_tol = 1e-12.

## Constants — sources

| Constant | Source |
|---|---|
| λ̄_p = 0.21030892 fm | CODATA 2018 (specified in Brief 08) |
| r_p muonic = 0.84087 fm | Pohl et al. 2013, *Nature* (Brief 08) |
| r_p α-matched = 0.83854 fm | Brief 08 |
| 168, 42, 14, 7 | Group theory: |PSL(2,7)|, 42 = 168/4, 14 Császár faces, 7 Singer period |
| π, √5, √12 | `math` module — no hardcoded floats |

No lookup beyond the values listed in Brief 08 itself.

## What this does NOT establish

Per the brief and the parent document
`borromean_circumscription_derivation.md §5`:

- The void correction ζ(1−cos 18°) was identified from the "5 is always
  a void connection" principle. The closed-form derivation of this
  factor from the H² → ℝ³ embedding map is **still open**. The script
  computes the formula; it does not derive the formula. Tier remains T2.
- The factor 49 (= 14·(7/2)) is justified structurally via
  Cayley-Dickson orientation doubling on Z₇; T2.
- The R/r = 4 ratio is T1 from |PSL(2,7)| = 168 and area = π/42.

If the formula's analytic derivation from the embedding map ever
appears, the tier of the prediction can be promoted from T2 to T1
without changing this script.

## Notes

- Script runs under the standard library (no NumPy / SciPy). Pure
  `math`. Deterministic.
- `python tools/rho_derivation.py` prints to stdout and writes
  `reports/rho_derivation_output.txt` for paper-appendix inclusion.
- No fitting, no optimisation, no interpolation, no free parameters
  (`test_no_free_parameters` enforces by re-running and comparing).
