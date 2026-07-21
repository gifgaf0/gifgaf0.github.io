# CC HANDOFF — G-TSH3 (kernel-set extension), full-from-scratch per E4
**Date:** July 21, 2026 · **Chat leg complete; two-leg comparison pending.**

## Lock (D5 standard — travels in-band)
Staging memo md5 **`dab46b332b83997d34f9e4ca64c07a4d`** (`G_TSH3_STAGING_MEMO.md`, included in this delivery). Verify byte-identity BEFORE Phase 1. Instrument lock AUTH-INST-1 (in `gtsh3_deviation_log.md`, included): Δq = 0.02·(2π/a*), forced-origin ω-vs-q, j = 2..6, Γ→K & Γ→M averaged, no per-kernel tuning.

## Scope (locked)
Kernels: GEM-3, GEM-4, GEM-8 (U = exp(−(r)^n) class as specified in memo §4), cap-p2 = (1−r²)²·θ(1−r) (Û = 16πJ₃(k)/k³). Frozen read-only anchors: the 8-point P_X set of §2.91.I/J. Convention ħ = m = ρ₀ = 1; spinodal g_c = min_{Û<0} k²/(−4Û). First passing: E2(a) two-tier, grid step 5 from 5·ceil(g_c/5), downward extension, deep-fail bracket at g*−5. Falsifiers: F9 ≤5e-3, F-LIN [0.95,1.05] (W1 = j2-4, W2 = j4-6, both branches, both directions), F-ISO ≤2%, F-CONV(n→n′) ≤5e-6, F-CLS f_T ≥0.95, F-NEG. Controls C-NEG/C-POS mandatory. Witness g_w = 1.5·g_c, same bar, non-verdict. W-μ: 5 shears ε ∈ ±0.06, band [0.5, 2]. **Build everything from scratch: own cell, own solver, own tables, own classifier, own reducer, own mapper (θ₁ = 3%, θ₂ = 10% appear ONLY in your quarantined mapper, own T1 grep in-invocation).**

## Chat-leg values (comparison targets C1–C6; do NOT tune toward them)
P1: gem8 g*=20 (a* 1.46059, μ 53.225) · gem4 g*=35 (1.49352, 93.372) · gem3 g*=70 (1.51435, 192.214) · cap_p2 g*=410 (0.98099, 417.691). All below diagnostic g_c; every bracket deep-fail-verified; tier-2 (e,μ) spreads ≤4.1e-12, uniform landings {seed 3} at gem8/gem4/cap_p2.
P2: gem8 CERT R_T=0.51767 · gem4 CERT 0.47401 · gem3 CERT 0.40780 · **cap_p2 EXCLUDED, F-LIN L1 W2 = 0.946/0.952 (γ4-class strong coupling, μ = 418)**.
P3w: step REUSE; all six measured points DROP — five on F-CONV ~1e-5–6e-5, γ8 also F-LIN L1. Expect the same collapse class at your truncation pair; drops are non-verdict.
P3mu: gem8 0.712 · gem4 0.778 · gem3 0.993 — no flags.
P4: P_ext n=11, mean 0.50098, **D_ext = 18.600%**, farthest gem3, departing family GEM, **D_F = 12.582%**, ncert 3/4, exclusions 1, boundary False → **ARM = KNOB**.

## Pre-registered cross-era prediction (ANCHOR-SYS)
Your from-scratch leg at the locked instrument should land **near the chat values, not the frozen anchor speeds**: step@22 R_T ≈ 0.5188 (frozen 0.52284), γ8@20 ≈ 0.4803 (frozen 0.47791). Frozen anchors enter D_ext as recorded R_T data, not re-measurements. If your independent window/solver instead reproduces the frozen speeds exactly, that FALSIFIES the chat attribution (per-era window conventions) → S9.

## Deviations you must independently confirm or flag (full list in gtsh3_deviation_log.md)
D-2 (init amp 3.0 + tier-2 acceptance ≥2/3-identical, uniform landings logged) · H-4 (identity comparator on translation-invariant (e,μ); ρmax is registration-dependent on a grid) · D-3 (identity threshold 1e-8 operational; memo's 1e-15 unattainable at residual-target 1e-12 stopping; outcome-invariant [1e-11,1e-8]) · H-5 (F-CONV = 5e-6 per memo — this gate is decisive at witness points and tight (1.2×) at gem8 P2; use the memo value) · H-2/H-3 solver lessons (oscillatory Hankel quadrature; no Trotter splitting near the Ward identity).

## Comparison plan (C1–C6)
C1 controls · C2 g*/a*/μ per kernel (expect ≤0.02%) · C3 speeds/R_T (expect ≤0.3% given independent windows at the SAME locked Δq; the pre-registered anchor prediction above) · C4 exclusion mechanism (cap_p2 L1 sublinearity, independently) · C5 witness drop class + W-μ ratios · C6 mapper D_ext/D_F/arm (expect ≤0.06 pp, KNOB). Any disagreement → S9 counter-cross-check before anything else.

## Chat artifact md5s
leg f23aaca367b308dc50dd998b0eff798c · results 91b671203c3ad4a70bc08833170095e0 · mapper 6485f8391ddc565d9fcfdce24fc53d5c · verdict cd15b0ee0fb0f5358129446be3b29e7d · feasibility 34d3fccf/0fe5e9f4 · staging memo dab46b33.
Fold target §2.91.K + one Part VI row — author authorization only, after C1–C6.
