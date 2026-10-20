# E4 cross-check: the order-21 group on three generations

*Independent second computation and adversarial audit of `seed/experiments/E4_family_symmetry/` (SEED.md §3, §7.3; PLAN.md §4 E4).*

The work was done in two passes:
- **First pass.** An earlier cross-check session was interrupted by a container restart. It wrote `cc_*.py`.
- **Second pass.** This session inspected the first-pass code and re-ran it; the outputs reproduce byte for byte. It then added new methods (`cc2_*.py`), repaired a first-pass convention slip, and only then read the original code to diagnose the disagreements.

Neither pass imports or copies the original scripts. Both read PLAN.md, the original REPORT.md and `results.json`, and the literature: LNR 0709.1447 and 0706.2341, NuFIT 6.0 Table 1, UTfit 2022, and Huang & Zhou 2020. All data values used by the original were re-read in those PDFs and match.

## Verdict

**Confirmed, with corrections.**
- **What reproduces:**
  - all the group theory and all 17 calibrations;
  - the LNR seesaw example and its exclusion by NuFIT 6.0;
  - the F₂₁ Majorana residual obstruction;
  - the three PSL(2,7) ℤ₂-partial survivors;
  - all 161 texture-class verdicts.
- **One headline number is wrong:** the best PSL full-residual lepton pattern has χ² = 162, not 200. The cause is a δ-wrapping bug, and it changes no verdict.
- **One major overstatement:** "no alignment class both fits and predicts" holds only for complex α, β in LNR's minimal variant, and the report does not say it made that choice. With LNR's own real couplings, three classes survive the preregistered rule with dof = 1.

## Methods (where they differ from the original)

| Item | Original | Cross-check |
|---|---|---|
| Group closure | exact ℤ[ζ₇, 1/7] | own exact ℚ(ζ₇) class, plus exact PSL presentation a² = b³ = (ab)⁷ = [a,b]⁴ = 1 and F₂₁ relations |
| Character tables | explicit irreps | Burnside (class-algebra eigenvectors) and peeling of tensor powers of the 3; no irreps needed |
| Invariants / couplings | null spaces of generator equations | (a) characters and Reynolds projector (first pass); (b) **exact monomial counting** (second pass): D-weights mod 7 and C-orbits with phases in μ₄₂, no floating point |
| LNR mass matrices | derived from invariants | (a) LNR's displayed forms; (b) derived from the exact invariants and shown equal, structure by structure, to LNR's I₃, γ₁,₂, β₁,₂ |
| α windows / refit | numerical | exact roots of (320+3r)α² + (320+6r)α + 80 = 0 |
| Residual patterns, ℤ₂-partial fits | own code | independent code, δ treated within NuFIT's 3σ interval |
| Texture survey | numba least squares | independent re-implementation (all 161 classes); 'gen' lepton classes refitted with a consistent PMNS convention |

## Agreement table

| Quantity | Original | Cross-check | Agree |
|---|---|---|---|
| \|⟨D,C⟩\|, \|⟨D,C,R_f⟩\| | 21, 168 | 21, 168; ⟨D,R_f⟩ already 168 | yes |
| R_f = A^[3], R_f·D = B^[3] | exact | exact (also A·B = D) | yes |
| F₂₁ / PSL character tables, FS | LNR; FS(3) = 0 | same; FS 0 for 3, 3̄ and +1 for 6, 7, 8 | yes |
| F₂₁ 3⊗3, 3⊗3̄ | (3+3̄)_s + 3̄_a; 1+1′+1″+3+3̄ | same, from characters and from exact counting | yes |
| PSL Kronecker products (14), branchings, A^[8] | match; 3×10⁻¹⁶ | match; 4.4×10⁻¹⁶ | yes |
| F₂₁ invariants ψψ′ξξ′ | 5 (2 symmetric) | 5 (2); these are exactly LNR's five M_Dir structures | yes |
| Dirac / Majorana coupling tables, closed forms, Schur | as reported | identical (three methods) | yes |
| LNR M_ν(−1,−1); ratios; r | ½[[0,1,1],[1,−4,5],[1,5,−4]]; 1:−2:9; 80/3 | same (sign included); r(α) = 80(2α+1)²/(−3α(α+2)) | yes |
| α windows | (−1.143, −0.946), (−0.220, −0.154) | (−1.1435, −0.9462), (−0.2202, −0.1537) | yes |
| α refit (r = 33.83) | −1.0621, −0.1787 | −1.06209, −0.17870 | yes |
| θ₁₃ / θ₁₂ with haze (pole masses) | 2.819° / 32.45° | 2.8186° / 32.442° (unitary), 32.449° (linear) | yes |
| θ₁₃ with MS-bar masses | 2.792° | 2.7924° | yes |
| Pulls: s₁₃², r, s₁₂², s₂₃² | −34.1, −7.8, −1.8, −1.4/−4.1 | −34.07, −7.82, −1.80, −1.42/−4.15 | yes |
| LNR-exact class χ² | 1472.0 | 1472.01 (closed form) | yes |
| Stabiliser of LNR M_ν in PSL | identity | identity | yes |
| F₂₁ Majorana obstruction | ℤ₇ → 0, ℤ₃ degenerate | exact (sympy), all 7 ℤ₃ | yes |
| Subgroup counts | ℤ₇×8, ℤ₃×28, ℤ₂×21, ℤ₄×21, V₄×14 | same | yes |
| F₂₁ best lepton / CKM χ² | 2459 / 1.08×10⁵ | 2459.1 / 1.083×10⁵ | yes |
| **PSL best full-residual lepton χ²** | **200** | **162.1** (200.05 with the original's δ wrap) | **no** |
| PSL best Klein–Majorana / CKM | 692 / 7.7×10⁴ | 692.2 / 7.716×10⁴ | yes |
| ℤ₂-partial survivors | ℤ₇ 2.13, TM1 2.54, TM2 7.63; next 31.5 | 2.133, 2.541, 7.628; next 31.53 | yes |
| Texture survey (161 classes) | 90/5/34 (leptons), 29/0/3 (quarks), 0 survivors | identical; 161/161 class verdicts and N_eff | yes |
| Relabelled after the rank scan | "23", χ² ≈ 5×10³–10⁴ | 26 in results.json, χ² 1.5×10³–3.1×10⁶ | **no** (report text) |

Checks: 92 of 93 pass. The one failure is the PSL χ² = 200 target, diagnosed below.
- First pass: groups 32/32, LNR 18/18, Yukawa 11/11, residual 5/6.
- Second pass: exact invariants 11/11, LNR closed form 10/10, real-coupling verification 5/5.
- Convention-fixed refit of the 64 'gen' lepton classes: 0 disagreements.

## Disagreements, diagnosed after reading the original code

1. **PSL best lepton χ² 200 → 162 (bug in the original).**
   - `data_targets.pull_delta` and `e4_fits.lepton_pulls` wrap δ into [bf−180°, bf+180°) = [−3°, 357°) before applying the one-sided σ.
   - NuFIT's 3σ range is 96°→422°, so δ = 0 ≡ 360° is allowed. The wrap gives it pull −6.56 instead of +2.24.
   - Reproducing the wrap gives 200.05. Non-surviving ℤ₂-partial classes are inflated the same way, e.g. 400.75 vs 362.80.
   - No pass/fail changes: the survivors, the accommodating fits and the 72.49 classes all have δ inside 96°–357°.
2. **Real vs complex couplings (unstated choice in the original).**
   - In `e4_fits.py` the 'min' variant uses complex α and complex β (`coupl`, `lepton_obs`). The report calls 'min' "LNR's leading order", but LNR use real α = β = −1.
   - The first pass found, and `cc2_minreal_verify.py` confirms with independent code, that with real α, β three classes survive the preregistered rule (dof ≥ 1, p > 0.01). All have φ₁₀ = G:

     | (φ₅, φ₁) | N_eff | χ² | p | δ |
     |---|---|---|---|---|
     | (ℤ₃, P) | 6 | 0.14 | 0.71 | 207° |
     | (P, ℤ₃) | 6 | 0.02 | 0.89 | 188° |
     | (P, P) | 6 | ≤ 0.14 | 0.71 | |

   - With complex α, β the same classes have dof = 0, as the original found.
   - The "prediction" in the real case is weak: fitting the other six observables exactly leaves δ on discrete branches. For (ℤ₃, P) the first pass found δ ∈ {26, 84, 131, 152, 229, 299, 360}°.
3. **Relabelled count (report text).** `results.json` has 26 classes with verdict_fit = excluded and verdict_final = structural, not 23. Only the 19 ℤ₇ classes fit the "rounding noise on a zero singular value" explanation. The other 7 are dead through r = 1 degeneracies or a permutation CKM.
4. **First-pass slips, fixed here; not issues with the original.**
   - cc_texture mixed PMNS conventions (U_e from M_eM_e†, U_ν conjugated). This only matters for 'gen' classes with complex φ₅. A consistent-convention refit of all 64 'gen' lepton classes reproduces every original verdict and N_eff.
   - One 72.49 class stopped at 76.31 in the first pass. The original's minimum is the lower one.

## Issues

| Severity | Issue | Fix |
|---|---|---|
| **major** | "0 predictive survivors / none fits and predicts" holds only for complex α, β in 'min', which the report does not state. With LNR's real couplings, 3 classes survive at dof = 1 (p = 0.71–0.89). This is also part of the evidence for the AMENDED "F₂₁ does a job" verdict. | State the convention. Report the real-coupling variant and its δ branches. Qualify the claim. |
| minor | δ-wrap bug: PSL best lepton χ² is 162, not 200, and non-surviving ℤ₂-partial χ² values are inflated. No verdict changes. | Wrap within NuFIT's 3σ interval; correct 200 → 162. |
| minor | "23" relabelled classes, χ² 5×10³–10⁴, all rounding noise. Actually 26 classes, χ² 1.5×10³–3.1×10⁶, mixed causes. | Correct the text. |
| minor | "Three distinct masses need 1+1′+1″ together": any two singlet vevs suffice. | Reword. |
| minor | "10" / "97" distinct patterns count (sector, G_ℓ, G_ν, \|U\|²) tags. Distinct \|U\|² structures are 3 and 26. | Define the count. |
| minor | Haze sign called an "input chosen to match": LNR's printed U₋₁ fixes it (verified entry by entry to O(λ)). | Reword. |
| minor | "(shared with S₄)": true for TM1 (⟨ℤ₃,t⟩ = S₄) and TM2 (⟨ℤ₃,t⟩ = A₄); the ℤ₇ class generates all of PSL(2,7). | Restrict to TM1 and TM2. |

## Claim audit

- **Supported:**
  - §3 group facts, R_f = A^[3], complex triplets (uniqueness not tested, as stated);
  - all 17 calibrations;
  - the Schur claim;
  - the F₂₁ Majorana obstruction;
  - the F₂₁ and PSL residual-pattern verdicts, apart from the χ² value 200;
  - the ℤ₂-partial survivors;
  - the LNR exclusion and its accidental tri-bimaximal form;
  - the texture counts.
- **Supported, with a caveat:** "model-builders used both groups" is shown computationally for F₂₁. For PSL(2,7) it rests on the literature (LNR 0709.1447).
- **Overstated:**
  - "none fits and predicts" (real-coupling caveat);
  - "1+1′+1″ together";
  - the haze-sign wording;
  - "(shared with S₄)" applied to the ℤ₇ class.
- **Wrong (numbers only, no verdict effect):**
  - PSL best lepton χ² = 200;
  - "23 relabelled".
- **Seed verdict words:** they all stand (CONFIRMED ×4, AMENDED ×2, CONFIRMED for the LNR exclusion). The AMENDED "F₂₁ does a job" should carry the real-coupling caveat.
- **Report hygiene:**
  - the figures exist and are under 300 KB;
  - the PASS counts quoted (54/54, 15/15, 14/14) match the logs;
  - the deviations from PLAN are disclosed, except the coupling convention above.

## Files and how to reproduce

Directory: `seed/experiments/E4_family_symmetry/crosscheck/`. Run with one thread (`NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`).

First pass:
- `cc_groups.py` (2 s)
- `cc_lnr.py` (10 s)
- `cc_yukawa.py` (5 s)
- `cc_residual.py` (5 min)
- `cc_z2gen.py`
- `cc_texture.py` (9.5 min; `--minreal` for the real-coupling survey)

Second pass:
- `cc2_exact_invariants.py` (10 s)
- `cc2_lnr_closed.py` (20 s)
- `cc2_minreal_verify.py` (about 25 min, checkpointed in `out/minreal_verify_cc2.ckpt.jsonl`)
- `cc2_texture_convfix.py` (1 min)
- `cc2_collect.py`, which writes `crosscheck.json` and supersedes `cc_collect.py`

Logs are in `out/*.log`. All scripts are deterministic (fixed seeds). Re-running cc_groups, cc_lnr, cc_yukawa and cc_residual in this session reproduced the first-pass logs exactly.
