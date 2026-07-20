# CC HAND-OFF PACKET — Gate G-TSH2 (D5 protocol, first application)
**In-band locked artifact:** G_TSH2_PREREGISTRATION_LOCKED.md · **lock md5: 99eb26a5d8ff1e32c54d5cff40386098**
CC MUST verify byte-identity of the locked artifact against this md5 before Phase 1. Any mismatch: halt and report.

## CC leg requirements (E5(a): full-from-scratch)
- Own cell size, truncation, dt schedule, polish, classifier, and reducer. The gz1/tsh1 lineage may NOT be imported.
- Execute the locked instrument exactly: kernels K3 (gamma=4), K4 (gamma=8), K5 (gamma=12), K6 (parabolic cap), grids and CERT per section 3; estimators per section 7; F9/F-LIN/F-ISO/F-CONV/F-CLS per sections 5-7; C-NEG/C-POS per section 10; W-mu per section 8; T1 self-grep per section 10.
- Quarantine: thresholds (theta1, theta2) may appear only in the CC arm mapper, run after all measurements are frozen.
- Read-only anchors (never re-measured): step R_T {0.5228, 0.5286, 0.5348, 0.5436}; gamma6 R_T {0.4988}.

## Required output schema (JSON, one object per kernel)
g_star, deviations[], a_star, mu, gp_residual, ward_x, ward_y, cT_GM, cT_GK, cL1_GM, cL1_GK, c2_GM, c2_GK, p_T_W1, p_T_W2, p_L1_W1, p_L1_W2, f_T_min, iso_T_pct, iso_L1_pct, conv_dcT, conv_dcL1, R_T, mu_static, wmu_ratio, flags[]
Plus: controls {cneg: PASS/FAIL, cpos: PASS/FAIL}, and the CC arm-mapper verdict {D_W, D_X, arm}.

## Comparison (verdict-level; chat side runs the same)
C1 per-kernel g_star exact grid match; C2 a_star, mu <= 0.3%; C3 c_T, c_L1 <= 0.5%; C4 R_T <= 0.5%; C5 D_W, D_X within 0.3 pp and arm identity; C6 falsifier/control state identity. Any breach: S9 before any fold.
