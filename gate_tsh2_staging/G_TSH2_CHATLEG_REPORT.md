# G-TSH2 — CHAT-LEG EXECUTION REPORT
**Date:** July 19, 2026 · **Lock:** G_TSH2_PREREGISTRATION_LOCKED.md, md5 `99eb26a5d8ff1e32c54d5cff40386098` · **Base:** V4.68 CANONICAL · **Leg:** chat, from scratch (`g_tsh2_chatleg.py`, md5 `04c2b32f`) · **Order of operations §13 followed:** lock → CC packet staged in-band (`CC_HANDOFF_G_TSH2.md`, md5 `131825d1`) → P0 → P1 → P2 → P3 → P4 → this report. Thresholds appeared in an executed path for the first time at P4 (`arm_mapper.py`, md5 `2bf1f449`, T1-clean).

## P0 controls — both PASS
C-NEG (step g=8 uniform): pipeline ω matches analytic Bogoliubov to <10⁻⁶; exactly 1 gapless branch; 0 odd-parity gapless. C-POS (classical NN springs): c_L/c_T = √3 recovered to 2.8×10⁻⁸; polarization classifier labels T correctly.

## P1/P2 results (n=32; conv at n=40; ρ₀=1; substrate units)

| K | kernel | g\* | a\* | μ | GP resid | Ward (x,y) | c₂ | c_T | c_L1 | R_T | f_T | iso T/L1 % | conv | W-μ ratio | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K3 | γ=4 | 70 | 1.56245 | 341.83 | 3.1e-07 | 2.4e-09 | 5.50 | 5.3255 | 18.278† | 0.29136† | 1.000 | 0.90 / 2.60 | 1e-09 | 0.592 | **F-LIN, F-ISO → EXCLUDED** |
| K4 | γ=8 | 20 | 1.58888 | 66.898 | 4.4e-08 | 2.2e-09 | 4.135 | 4.6708 | 9.7733 | **0.47791** | 1.000 | 0.28 / — | 3e-09 | 0.520 | — |
| K5 | γ=12 | 20 | 1.53766 | 58.686 | 1.2e-06 | 3.7e-08 | 2.656 | 5.1887 | 10.6192 | **0.48861** | 1.000 | 0.29 / — | 5e-06 | 0.794 | — (H-1) |
| K6 | cap | 90 | 1.18287 | 136.94 | 1.0e-07 | 2.5e-09 | 6.618 | 7.4310 | 14.3949 | **0.51622** | 1.000 | 0.08 / — | 1e-09 | 0.466 | W-MU-BAND |

† uncertified values, shown for the record only. Every kernel: tier-2 confirmed at g\* (3 random-init deep re-solves, E/A machine-identical ≤10⁻¹⁵ rel), deep fail at g\*−5; F9 Ward passes by ≥5 orders on all certified kernels; F-NEG never fired; symmetry residual of ψ₀ ≤5×10⁻¹⁶.

**First-passing extensions (declared §3 procedure, logged):** K3 85→70 (fail 65); K4 25→20 (fail 15); K5 20 (fail 15); K6 110→90 (fail 85). All first passages bracketed by deep fails.

## Exclusion — K3 (honesty entry)
F-LIN fired on L1 both directions (p_W2 = 0.769 GM / 0.632 GK) and F-ISO on L1 (2.60% > 2%). Mechanism (post-hoc description from frozen raw arrays, no re-measurement): the L1 branch saturates sublinearly across the locked window (GM increments 1.124 → 0.421) at K3's strong-coupling first-passing point (μ = 342) — the locked k-window extends past the L1 linear regime for this kernel. The T branch itself was clean (p ∈ [0.985, 1.008], iso 0.90%): the transverse speed was measurable, but a certified R_T requires a certified L1. No window motion, no re-tuning (T3). One exclusion — below the two-exclusion return-to-author trigger.

## P4 verdict (quarantined arm_mapper, A-2 semantics)
P_W (7 pts) = {0.5228, 0.5286, 0.5348, 0.5436, 0.4988, 0.47791, 0.48861}: **D_W = 6.947%** (mean 0.51359).
P_X (8 pts) = P_W + {0.51622}: **D_X = 7.007%** (mean 0.51392).
Map: D_W ∈ (θ₁, θ₂] → **UNDERDETERMINED-2**. Dead zone honored on both statistics; the honest exit is the verdict.

**Structural observations for the record (R2 annotations, not verdict inputs):** (1) The within-family spread is real: soft-shoulder members (γ=8, 12) sit at 0.478–0.489 vs the step band 0.523–0.544 under the uniform first-passing convention — ~7% motion, too large for DERIVED, too small for KNOB. (2) The cross-family cap point (0.51622) lands *inside* the γ-family span; the out-of-family probe produced no displacement (D_X ≈ D_W). (3) Cell-level CERT caveat: the rhombic cell forces p6m periodicity; competing global phases (square/stripe) were not tested — declared instrument scope, carried as an annotation.

## Honesty ledger items (chat leg)
- **S-1** (pre-lock, in §A of the lock): staged Gaussian probe was analytically Q+; caught at instrument drafting; A-1 authorized.
- **H-1**: K5 GP-residual floor 1.20×10⁻⁶, marginally above the 10⁻⁶ target; the locked §4 cure (Ward re-check before use) was performed: Ward = 3.7×10⁻⁸, clean. State used.
- **H-2** (process note): `arm_mapper.py` was created after the main script's last T1 invocation and ran standalone; an explicit T1 grep over the mapper was run immediately after (clean). Future legs: grep the mapper inside its own invocation. No contamination.
- **W-MU-BAND** (K6): witness ratio 0.466 < 0.5, flagged per §8, non-falsifying. Noted: all four W-μ ratios sit below 1 (0.47–0.79) — the static shear modulus is consistently below ρ·c_T², directionally consistent with a partial normal-fraction participation picture; open Rakic–Ho–Lee territory; no theory relation locked.

## Consequence routing (per §12, UNDERDETERMINED-2 arm)
A kernel-set-extension successor is registered, unopened. No KC evaluated; no observable; the transverse scale import stays named and unexercised; nothing prior modified; Paper IIA §3–§4, T1–T5, §2.91.H estate, §2.90, μ_n, gauge §7.4 firewall untouched. §2.52 Open 3: frozen, untouched.

## Status
Chat leg COMPLETE. Awaiting CC full-from-scratch leg (E5(a)) against the in-band lock, then C1–C6 verdict-level comparison (S9 on any breach), then author fold authorization → V4.69 candidate.

## Artifact seals (md5)
lock `99eb26a5d8ff1e32c54d5cff40386098` · CC packet `131825d1eb2fa522f3324b32a8fc90c4` · chat-leg script `04c2b32ff47fa2f9db7f07b20ad9c43e` · results JSON `9d73e1aea61b2db9b6205e29a5b1ff74` · arm_mapper `2bf1f44937628fe657d5ee70d2433568` · arm verdict JSON `5fd459845296f0723aee71f1c5713c90` · feasibility diagnostic `49b157ba92676f26a5ab7c73bdb24374` · staging memo `09c9cc3805a33d0f51011deca2eeb3e9` · draft instrument `8f53c0e3fc7228b0e55806881ea0cb1e`
