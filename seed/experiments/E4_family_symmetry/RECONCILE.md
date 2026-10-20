# E4 reconciliation

*Reconciliation of E4 (the order-21 group on three generations) after its independent cross-check (`crosscheck/crosscheck.json`, verdict "confirmed_with_corrections").*

The cross-check reproduced every calibration and all 161 texture verdicts (with N_eff), using different methods. It raised **1 major and 6 minor issues**. Each one was settled by reading both codes and, where needed, by a decisive extra computation. Every issue is resolved, and none is left OPEN.

The pre-reconciliation outputs are kept for comparison:
- `out/fits_v1_deltawrap.jsonl` and `out/fits_v1_deltawrap.log`
- `out/yukawa_v1_deltawrap.json`
- `out/robustness_v1_deltawrap.json`
- `out/results_v1_prereconcile.json`

## Issues

| # | Severity | Issue | Who was right | Action | Resolved |
|---|---|---|---|---|---|
| 1 | major | Texture-survey headline ("0 predictive survivors; no class both fits and predicts") depends on an unstated choice: complex α, β in the "min" variant | Both computations are correct for their conventions. The original's headline was overstated | Real-coupling variants added to `e4_fits.py` and fitted (144 classes); `e4_realcoupling.py` works out what the survivors predict; report and results.json state the convention and give both | yes |
| 2 | minor | δ pull wrapped into [−3°, 357°), inconsistent with NuFIT's 96°–422° range | Cross-check | `data_targets.pull_delta` and `e4_fits.lepton_pulls` fixed; e4_yukawa, e4_fits (all classes), e4_structure and e4_robustness rerun | yes |
| 3 | minor | "23 classes relabelled structural, χ² 5×10³–10⁴, rounding noise" | Cross-check | Count and breakdown now computed in `collect_results.py`; report text corrected | yes |
| 4 | minor | "Three distinct masses need 1+1′+1″ together" | Cross-check | `e4_reconcile_checks.py` (a): any two singlet vevs suffice; text corrected | yes |
| 5 | minor | "10 / 97 distinct mixing patterns" | Cross-check (definition) | `e4_reconcile_checks.py` (b): these are (sector, G_ℓ, G_ν, \|U\|²) combinations; 3 / 26 distinct \|U\|² structures; both quoted | yes |
| 6 | minor | "Haze sign is an input chosen to match LNR" | Cross-check (wording) | The code already used LNR's printed U₋₁; note and text reworded | yes |
| 7 | minor | "Leptonic patterns that fit come from PSL(2,7)'s ℤ₂ elements (shared with S₄)" | Cross-check | `e4_reconcile_checks.py` (c): ⟨ℤ₇, t⟩ = PSL(2,7) (168), TM1 ⟨ℤ₃, t⟩ = S₄ (24), TM2 ⟨ℤ₃, t⟩ = A₄ (12); text restricted to TM1/TM2 | yes |

## Issue 1 (major): coupling convention in the texture survey

**What the cross-check said.** In the "min" (LNR leading-order) variant, `e4_fits.coupl` and `e4_fits.lepton_obs` take β and α complex (2 real parameters each). LNR use real α = β = −1. With real α and β, the classes φ₁₀ = G, (φ₅, φ₁) = (ℤ₃, P), (P, ℤ₃), (P, P) have N_eff = 6 and dof = 1, and they fit NuFIT 6.0. So the headline "0 predictive survivors" depends on an unstated convention.

**Diagnosis.**
- Reading both codes: the original's complex-coupling computation is correct, and the cross-check reproduced it class by class (161/161 verdicts and N_eff).
- The cross-check's real-coupling computation is also correct: the original pipeline, extended here, reproduces it.
- Both conventions are legitimate:
  - complex couplings are the generic effective theory;
  - real couplings impose CP, violated only by vev phases. That is LNR's own convention: they neglect "invariants capable of setting their phases" (0706.2341v2 §3.2), take α = β = −1, and scan α on the real axis.
- The original's fault was presentational. It did not state the convention, and it drew a framework-wide conclusion ("no alignment class in this framework both fits the data and predicts anything") that holds only for complex couplings. The cross-check is right.

**Decisive computation.**
- `e4_fits.py` gained variants "min-real" and "gen-real": every coupling real, with the same classes, observables, fit procedure and survival rule. That is 64 + 64 lepton and 16 quark classes (the quark "min" variant has no couplings).
- All 144 were fitted (`out/fits.jsonl`, 711 s), and `e4_structure.py` scanned them.
- Result: leptons 92 dead, 4 excluded, 29 accommodate, **3 survive**; quarks 13 dead, 3 accommodate.
- The three survivors are exactly the cross-check's classes. Survey multistart χ² = 0.90, 0.40, 0.021 (p = 0.34, 0.53, 0.89).
- `e4_realcoupling.py` polished from every δ branch, lowering the first two to 0.140 (p = 0.71). The cross-check found 0.140, 0.021, 0.140. Taking the lower value of the two computations: 0.14, 0.021, 0.021. All pass p > 0.01 with dof = 1.
- N_eff = 6 is the maximum rank over 30 random points (values 5 and 6 occur).
- gen-real has no survivor.

**What the survivors predict.**
- Fix m_e/m_μ, m_μ/m_τ, r, s₁₂², s₁₃² and s₂₃² at their central values. δ is then left on discrete branches. The script finds at least 20, 22 and 16 per class (300 starts per class); the list is completed by the exact conjugation symmetry δ → 360° − δ, which is verified on every branch solution.
- The union over the three classes is 25 values spread over the whole circle (15.5° … 344.5°). Each branch has a ±3° to ±16° spread from the 1σ errors of r and the angles.
- The nearest branches to NuFIT's best fit (177°) are 152.3° and 207.7°. Their pulls are −1.23σ and +1.61σ with the 1σ errors, and −0.91 and +0.38 in the 3σ-range convention.
- So these classes pass the preregistered rule formally, but the one constraint barely restricts δ at current precision.
- Each needs a hand-put generic φ₁₀ vev that carries the whole charged-lepton hierarchy. Imposing CP is an assumption beyond F₂₁.

**Action.**
- `e4_fits.py` docstring: complex α, β in "min", and the real variants.
- `collect_results.py`: `texture_survey_coupling_convention`, and the `texture_survey_real_couplings` block (summary, survivors, predictions, all classes). The findings entry and the seed-claim evidence for "F₂₁ does a job" are revised.
- `make_figs.py`: fig_texture_survey.png shows both conventions.
- REPORT.md: Method, Finding 6, "What it means", Deviations 10–11, Limitations.

**Verdict impact.** The "F₂₁ does a job" verdict word stays AMENDED. Its evidence now reads: 0 of 161 classes both fit and predict with complex couplings; 3 of 144 survive with real couplings, with a weak δ prediction and a hand-put φ₁₀ vev. **Resolved.**

## Issue 2: δ pull wrap

**Diagnosis.** The cross-check is right. `data_targets.pull_delta` and `e4_fits.lepton_pulls` wrapped δ into [bf − 180°, bf + 180°) = [−3°, 357°) before the one-sided pull. NuFIT's 3σ range for δ is 96°–422°, so δ = 0° = 360° is inside it with pull +2.24 (from 360°). The wrap gave it −6.56 (from 0°), and χ² jumped at δ = 357°.

**Action.**
- Both functions now use the representative δ + 360°k with the smallest |pull|. With σ = 81.7° and 27° the two branches cross at δ = 87.5°, inside NuFIT's excluded window of 62°–96°.
- The old convention is kept as `data_targets.pull_delta_wrap_v1`, used only to reproduce old numbers.
- Reran, via `reconcile_rerun.sh`:
  - e4_yukawa.py: residual patterns and ℤ₂-partial fits, 15/15 checks.
  - e4_fits.py: all 161 original classes refitted from scratch, plus the 144 new ones.
  - e4_structure.py: 3/3.
  - e4_robustness.py: 2/2.
- e4_groups.py and e4_lnr.py do not use the δ pull and were not rerun.

**Effect.**
- PSL(2,7) best full-residual lepton pattern (ℤ₃ × ℤ₇, Dirac ν, δ = 0°): χ² 200.05 → **162.09**, matching the cross-check's 162.1. Still excluded.
- Excluded ℤ₂-partial (0, ½, ½) classes: 400.75 → 362.80, matching the cross-check.
- The three ℤ₂-partial survivors are unchanged (2.133, 2.541, 7.628). The F₂₁ best lepton (2459.1) and the CKM patterns are unchanged.
- Texture survey: all 161 verdicts unchanged. The only N_eff change is the fit-level N_eff of one structurally dead class (lepton|gen|φ₁₀ = ℤ₇|φ₅ = ℤ₃|φ₁ = ℤ₃, 5 → 6). χ² changed only for dead classes, where it is a rounding artefact, and at the 10⁻⁸ level for accommodating ones. The 72.49 failures and the LNR exact point (1472.01) are unchanged.

**Resolved.**

## Issue 3: number of classes relabelled by the rank scan

**Diagnosis.** The cross-check is right. The pre-reconciliation results.json already listed 26 relabelled classes (22 lepton, 4 quark), with χ² from 1.5×10³ to 3.1×10⁶. The report's "23" and "χ² about 5×10³ to 10⁴" were slips. The rounding-noise explanation covers only the classes with a ℤ₇ familon, where M_e or M_d has rank 2. The others are dead for other reasons: exactly degenerate light neutrinos (r = 1), or a permutation CKM.

**Action.** `collect_results.py` now computes the count, the χ² range and the causes (`texture_survey_relabelled_by_rank_scan`). After the δ-fixed refit: 26 relabelled (22 lepton, 4 quark): 19 with a ℤ₇ familon (M_e or M_d rank 2; a class that is also r = 1 is counted here), 4 with exactly degenerate light neutrinos (r = 1), and 3 minimal quark classes with a permutation CKM. χ² ranges from 1.9×10³ to 3.1×10⁶ (1.5×10³ to 3.1×10⁶ before the δ fix). The report now says so.

## Issue 4: singlet vevs and three distinct masses

**Diagnosis.** The cross-check is right. `e4_reconcile_checks.py` builds the F₂₁ invariant tensors for L = R = 3 with H ∈ {1, 1′, 1″} and tests 200 random couplings for each set of singlets.
- A single singlet gives three equal |masses| at every point.
- Each pair (1+1′, 1+1″, 1′+1″) gives three distinct masses at 200 of 200 points. The smallest relative gap is 7.6×10⁻⁴, which is generic and not a degeneracy.

The original's yukawa check ("1+1′+1″ together give three free diagonal entries") is true. The report's "need all three" was an overstatement.

**Action.** Report and results.json now say "at least two of 1, 1′, 1″ (F₂₁ broken to ℤ₇) or triplet vevs".

## Issue 5: counting mixing patterns

**Diagnosis.** The cross-check is right about the definition. The counts 10 (F₂₁) and 97 (PSL) are (sector, G_ℓ type, G_ν type, |U|²) combinations. The same matrix is counted once for quark use and once for Dirac-lepton use.
- F₂₁: 5 quark + 5 Dirac-lepton combinations, from 3 distinct |U|² structures.
- PSL(2,7): 43 quark + 43 Dirac-lepton + 11 Klein–Majorana combinations, from 26 distinct |U|² structures.

**Action.** Both numbers are quoted, with the definition (report §4; results.json findings; `reconcile_checks.pattern_counts`).

## Issue 6: haze sign

**Diagnosis.** The cross-check is right on wording. `e4_lnr.py` already uses LNR's printed U₋₁ = [[1, λ_e, 0], [−λ_e, 1, 0], [0, 0, 1]] (0706.2341v2 §4.2, re-read in this pass). So the sign was never tuned. The report only described it as an input.

**Action.** The calibration note in collect_results.py and the report text now say the sign is LNR's printed U₋₁, which reproduces their displayed U_MNSP. The opposite sign gives θ₁₂ = 38.09°.

## Issue 7: which group the ℤ₂-partial survivors use

**Diagnosis.** The cross-check is right. `e4_reconcile_checks.py` (c) finds every (g_ℓ, t) pair that reproduces each survivor's fixed column and computes the order of ⟨g_ℓ, t⟩ from PSL(2,7)'s multiplication table.
- ℤ₇ class: 168 (all of PSL(2,7)).
- TM1: 24 (S₄).
- TM2: 12 (A₄ ⊂ S₄).

**Action.** "(shared with S₄)" now applies only to TM1 and TM2. The ℤ₇ class is described as using a ℤ₂ that, together with ℤ₇, generates the whole PSL(2,7). It is still not available to F₂₁.

## Points checked that needed no change

- **PMNS convention.** The original extracts U = V_e†V_ν from the eigenvectors of M_eM_e† and M_νM_ν†. That is the "ē_L M_e e_R, ν̄_L M_ν ν_L^c" convention, used consistently in both sectors. It equals the complex conjugate of the holomorphic-convention PMNS (δ → −δ), and every class's parameter space is closed under complex conjugation, so the fits are equivalent. The convention slip the cross-check mentions was in its own first pass (`cc2_texture_convfix.py`), and refitting with the consistent convention gave 0/64 disagreements with the original.
- **The 72.49 classes.** The cross-check's first pass left one at 76.31. The original's lower minimum (72.49, and 300 starts find nothing lower) stands. Robustness after the δ fix: the six refits are identical to the new stored fits, and a 300-start rerun gives a minimum of 72.498 against the stored 72.490 (robustness 2/2).
- **"Model-builders used both groups".** For PSL(2,7) this rests on LNR 0709.1447 proposing it, which is a literature fact; only the F₂₁ model was computed. The report says so.

## Consistency

After the reruns, results.json, the report and the verdicts agree:
- All 17 calibrations are CALIBRATED.
- Every check passes: groups 54/54, yukawa 15/15, lnr 14/14, structure 3/3, robustness 2/2, realcoupling 4/4, reconcile_checks 4/4.
- Seed-claim verdicts are unchanged in their verdict words. The evidence for "F₂₁ does a job" (AMENDED) and for "mixing from misaligned residual subgroups" (AMENDED) is updated as described above.
