# G-TSH3 Chat-Leg Execution Report
**Gate:** kernel-set-extension successor (ledger V4.69 §2.91.J registration)
**Date:** July 21, 2026 · **Leg:** chat, from-scratch · **Author elections:** E1(c) GEM-{3,4,8}+cap-p2 · E2 YES (quarantined witness) · E3 YES (W-μ) · E4 CC full-from-scratch
**Lock:** staging memo md5 `dab46b332b83997d34f9e4ca64c07a4d` (author word "Lock", July 21)
**Instrument lock:** AUTH-INST-1 (author word "Lock", July 21) — Δq = 0.02·(2π/a*), forced-origin, j = 2..6, Γ→K & Γ→M averaged; no per-kernel tuning (Eddington guard).

## Artifacts (md5)
- `g_tsh3_chatleg.py` — **f23aaca367b308dc50dd998b0eff798c** (final; lineage ee6ad7d3 → f1f80021 (H-2) → e91d40bd (H-3) → 0be61011 (D-2) → 5721332e (H-4) → 246a847e (H-5) → f23aaca3 (P3w conv bar + P3mu continuation))
- `gtsh3_results.json` — **91b671203c3ad4a70bc08833170095e0**
- `gtsh3_arm_mapper.py` (quarantined, θ's only appearance, own T1) — **6485f8391ddc565d9fcfdce24fc53d5c**
- `gtsh3_arm_verdict.json` — **cd15b0ee0fb0f5358129446be3b29e7d**
- `gtsh3_feasibility_diag.py` — 34d3fccfaafa692010d85d0b261aaf9d · `gtsh3_feasibility.json` — 0fe5e9f40fcbf94672e39b9ef0c6e15d
- `gtsh3_deviation_log.md`, `dq_sweep.{py,log,json}` (diagnostic, closed), `verify_d2.{py,json}`

## Controls (P0a)
C-NEG uniform Bogoliubov: 0.0 exact, zero odd-parity gapless. C-POS spring lattice: c_L/c_T = √3 to machine (1.732050807568877). T1 self-grep at every invocation, mapper included.

## Anchor reproduction (P0b) and ANCHOR-SYS
Static chain reproduces both eras: step@22 a* 1.45731/μ 55.8505 (rel ≤1.3e-4), γ8@20 μ 66.89905 (rel 1.7e-5); Ward/res ~1e-12 deep; n32→40 R_T agreement 2.4e-6. Speeds under the locked instrument deviate from frozen-anchor speeds in kernel-dependent directions (step R_T −0.77%, γ8 R_T +0.49%); no fit convention and no single Δq reconciles both (dq_sweep). Attributed to per-era window conventions in the archived TSH1/TSH2 legs (files not on disk). **Assigned cross-era systematic: ±1% speeds, ±0.8% R_T — cross-era comparison only; internal comparability of all new points unaffected (one instrument).** BOUNDARY rule: D_ext ∈ [9%, 11%] → return-to-author (did not fire: D_ext = 18.6%). **Pre-registered CC cross-check: CC's from-scratch leg at the locked convention should land near the chat values (step R_T ≈ 0.5188, γ8 ≈ 0.4803), not the frozen anchors.**

## P1 first passing (E2(a) two-tier, downward extension, deep-fail bracket g*−5)
| kernel | g_c (diag) | g* | a* | μ | contrast | tier-2 (e,μ) | seeds |
|---|---|---|---|---|---|---|---|
| gem8 | 22.02 | **20** | 1.46059 | 53.225 | 45.9 | 3.8e-14 | 2/3 cryst (unif: 3) |
| gem4 | 39.19 | **35** | 1.49352 | 93.372 | 60.5 | 4.5e-14 | 2/3 cryst (unif: 3) |
| gem3 | 71.87 | **70** | 1.51435 | 192.214 | 172.3 | 3.1e-12 | 3/3 cryst |
| cap_p2 | 451.24 | **410** | 0.98099 | 417.691 | 97.2 | 4.1e-12 | 2/3 cryst (unif: 3) |

All four first-pass below their spinodal g_c — first-order across the family. Every passage bracketed by a verified deep CERT fail at g*−5. Uniform landings logged per D-2, never dropped silently.

## P2 certification (n=32; F9 ≤5e-3, F-LIN [0.95,1.05] both windows both branches, F-ISO ≤2%, F-CONV n32→40 ≤5e-6, F-CLS f_T ≥0.95)
| kernel | status | R_T | c_T | c_L1 | f_T | Ward | iso T/L | conv |
|---|---|---|---|---|---|---|---|---|
| gem8 | **CERTIFIED** | 0.51767 | 5.0138 | 9.6853 | 0.988 | 3.8e-6 | 0.34/0.14% | 4.1e-6 |
| gem4 | **CERTIFIED** | 0.47401 | 5.7394 | 12.1081 | 0.985 | 8.8e-7 | 0.72/0.20% | 1.4e-6 |
| gem3 | **CERTIFIED** | 0.40780 | 6.8691 | 16.8445 | 0.984 | 6.4e-6 | 1.35/0.24% | 3.8e-6 |
| cap_p2 | **EXCLUDED** | (0.45092) | 11.6362 | 25.8054 | 0.983 | 1.2e-6 | 0.78/0.23% | 2.3e-6 |

**cap_p2 exclusion (F-LIN L1):** p_L1 = [0.986, 0.946, 0.987, 0.952] — the W2 exponents on both directions fall below 0.95; sublinear longitudinal saturation at the strong-coupling first-passing point (μ = 417.7, γ4-class; γ4 was μ = 342 with the same L1 mechanism). The T branch was clean everywhere. Mechanism annotation is post-hoc description from the frozen raw arrays; no re-measurement, no window motion (T3). One exclusion — below the two-exclusion return-to-author trigger. This is precisely the [D4] retention flag playing out: coupling-sourced, informative R2.

## P3w witness (E2, quarantined, non-verdict-carrying; g_w = 1.5·g_c; same falsifier bar incl. F-CONV)
step: REUSE (g_w = 22.1 within 0.5 of certified g = 22). All six measured points **DROPPED**: γ8@34.1 (F-LIN L1 [1.06, 0.923, 1.061, 0.928] + F-CONV 1.15e-5), gem8@33 (F-CONV 1.0e-5), gem4@58.8 (F-CONV 1.7e-5), gem3@107.8 (F-CONV 1.4e-5), cap_p1@158.2 (F-CONV 6.3e-5), cap_p2@676.9 (F-CONV 1.4e-5). Mechanism: at 1.5·g_c the density peaks sharpen and n=32→40 truncation convergence exceeds the 5e-6 gate. Drops logged, zero budget impact. **Witness sample collapsed to the reuse point → D_C degenerate → §8 guide uninformative → the §7 arm stands unqualified** (memo default). R2 side-note (raw, uncertified): the dropped-point R_T ordering at the uniform 1.5·g_c convention reproduces the first-passing ordering (gem3 lowest at 0.409 vs 0.408) — qualitatively shape-sourced, held at annotation only.

## P3mu W-μ static witness (E3, R2, non-falsifying; adiabatic continuation from the unsheared crystal)
gem8: μ_s = 17.90, μ_s/(ρc_T²) = 0.712 · gem4: 25.62, 0.778 · gem3: 46.86, **0.993** · no W-MU-BAND flags. Ratio → 1 monotonically as the kernel softens; gem3 sits at the elastic identity μ_s = ρc_T² to 0.7%.

## P4 mapper (quarantined; frozen-set self-check D_X = 7.006%/0.51392 vs ledger 7.007/0.51392)
P_ext (n = 11) = 8 frozen + {gem8 0.51767, gem4 0.47401, gem3 0.40780}. Mean 0.50098. **D_ext = 18.600%** > θ₂ = 10% (boundary window [9,11]% not entered). Farthest: gem3; departing family GEM; **D_F = 12.582%** > θ₁ = 3%. ncert_new = 3/4 [D3 met]; exclusions = 1.

## VERDICT: **KNOB**
R_T ≡ c_T/c_L1 on the p6m GP supersolid, under the uniform per-kernel first-passing convention, is a **kernel-shape knob**: the GEM family alone spans 12.6% internally and drives the pooled max-from-mean to 18.6%. The TSH1→TSH2 dead zone is resolved on the kernel-shape axis — R_T is neither DERIVED-RATIO nor KERNEL-CLASS-PINNED. Structural R2 annotation: R_T is monotone in GEM softness (n = 3 → 0.408, 4 → 0.474, 8 → 0.518, step-limit family 0.523–0.544); softer cores buy relatively more longitudinal stiffness than shear.

**Consequences (per memo §9, all arms):** no KC evaluated; no observable; nothing prior modified; transverse scale import named and unexercised (T1 grep clean, both files); Paper IIA §3–§4, T1–T5, §2.91.H retired estate, §2.90, μ_n, gauge-paper §7.4 firewall untouched; §2.52 Open 3 untouched. Downstream caveat HARDENS: any R_T use must name the kernel. V4.68 successor-surface items unconsumed. The E2 convention-resolution question (elevating a witness to verdict-carrying) remains registered material — this witness was uninformative, not adverse.

## Honesty / deviation ledger
H-0 (stale leg file removed, fresh build) · H-1 (C-POS finite-q → exact q→0 matrix) · **H-2** (Hankel-table quadrature defect, caught pre-use; Bessel-zero-subdivided GL fix, validated 8.9e-16) · **H-3** (forward-Euler polish unstable; Sobolev-preconditioned descent, Ward-safe) · **H-4** (tier-2 comparator included non-translation-invariant ρmax; 5.0e-3 spread on the identical state at (e,μ) 3.8e-14; assert moved to (e,μ), ρmax recorded) · **H-5** (leg F-CONV 1e-4 vs memo 5e-6; corrected pre-use — the corrected gate was decisive on all six witness drops and left gem8 P2 passing at 1.2× margin) · D-1 (Δq halved, anchor-calibrated pre-verdict) · **D-2** (init amp 0.4→3.0 + tier-2 acceptance rule; author-ratified; invariance verified on both anchors ≤7e-5) · **D-3** (memo tier-2 "≤1e-15 rel" operationalized at ≤1e-8 on translation-invariant (e,μ); observed ≤4.1e-12, residual-limited; accept/reject invariant across [1e-11, 1e-8]; TSH2's solver achieved 1e-15 with a different stopping design; author veto standing).

## Register tags
Per-kernel numerics, brackets, exclusion, D-statistics: **R1-at-thresholds (chat leg; two-leg pending)**. Arm verdict, structural annotations, witness collapse, W-μ: **R2**. Fold target §2.91.K + one Part VI row — **on author authorization only, after CC comparison C1–C6**.
