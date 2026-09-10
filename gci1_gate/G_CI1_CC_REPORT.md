# G_CI1_CC_REPORT.md — Gate G-CI1, CC leg: full-from-scratch execution report (E-9; blind Phase-3 read #1 of record)

Dispatch `G_CI1_CC_DISPATCH_INBAND.md` md5 `420082d54f11817c9d64a8198f1042ae` (109,192 B) verified byte-exact; all nine embeds extracted and md5-asserted before use. Base canonical carried as frozen (md5 `f539d10cb4f73c81e7d9fdbe7fa63714`).

## Checkpoints (md5 / bytes / T1 hits)

- `ci1_phase0_cc.json`: md5 `a82462c4913096b57e3d956e77cc09e2` (6,689 B); T1 hits 0
- `ci1_phase1_cc.json`: md5 `b85ac5cf43dbcae5e77d09a667d890ca` (177,318 B); T1 hits 0
- `ci1_phase2_cc.json`: md5 `f79113b7664addc9b1d96893aa883cbf` (57,074 B); T1 hits 0
- `ci1_phase3_cc.json`: md5 `e97d9a1cbf94e5e8cd390b99dab87cf0` (30,169 B); T1 hits 0
- instruments: `g_ci1_phase0_ccleg.py` `9139c9959552421f84bbd61cf70b88b6`; `g_ci1_phase1_irrep_ccleg.py` `f94099a798b0312fd20668fb876804e7`; `g_ci1_phase2_regime_ccleg.py` `cb78fbf37fa63699f61fc4840d28638b`; `g_ci1_phase3_mapper_ccleg.py` `e7c02db36d3bf5942c0844bec9859b55`; `gci1_cc_common.py` `8b2510546fcf9e0b92b41f878a4910f4` — all T1-clean at every invocation

## Phase 0

All embed hashes asserted (prereg 6c480340, T1 list 653a0b74, lock record a6adbb6a + addenda, sealed dd8fe2d3 with structural census 12 by row-id regex only, inputs 200e7a8b / 621120e5). D-1..D-9 recorded as frozen. A0 carried as NOT TRIGGERED (chat-leg record). T1: 78 patterns, zero hits.

## Phase 1 — I-1 irrep/helicity audit

R-a (machine): aggregate transverse subspace eigenphase multiset {+1*theta, -1*theta} at every theta in {0.1, 2pi/7, 2pi/5}; max eigenphase deviation 3.34e-16 (tau_h = 1e-12); minimum distance of any eigenphase from +/-2*theta = 0.1 rad (exclusion holds). Single-crystal qT eigenvectors (35 directions x 4 tensors, 70 branch-direction pairs per config): mode content always a subset of {0, +1, -1}; never +/-2. Derived plane-wave strain and stress: +/-2 amplitude fractions at the 1e-16 floor (kinematic labels recorded per the ratified D-4 reading).

R-b (inventory, E-4): six banked branch families tabulated (superfluid phase/Josephson complex; transverse acoustic pair = the D-1 channel; longitudinal acoustic; internal 7-sector; optical/intra-cell; orientational/bond/texture). No branch is gapless AND helicity-+/-2 AND cone-degenerate.

**F-IRR: FIRES. K = (empty set). CI-S FALSIFIED-STRUCTURAL; CI-W/EM-IN operative. Matches the verdict of record; zero UNDERDETERMINED degeneracy calls.**

## Phase 2 — containment, I-2, I-3, ray bracket (substrate units)

| quantity | hex:step | hex:gem8 | cubic:step | cubic:gem8 |
|---|---|---|---|---|
| s1 rel dev vs banked | 3.26e-09 | 2.24e-09 | 1.55e-09 | 1.19e-09 |
| Q_T^a rel dev vs banked | 3.22e-08 | 3.04e-08 | 3.24e-08 | 2.74e-08 |
| D2 (Delta_ch -> D2 x^2) | -4.5869158e-03 | -6.4834233e-03 | -7.1343677e-03 | -9.9284953e-03 |
| large-x plateau | -8.81692e-03 | -1.21709e-02 | -1.40931e-02 | -1.89435e-02 |
| c_cone/V_T0 | 9.79885e-01 | 9.71895e-01 | 9.69449e-01 | 9.58151e-01 |
| eps_T | 9.1334e-02 | 1.0912e-01 | 1.3038e-01 | 1.5743e-01 |
| x_S | 1.0000e+01 | 3.1623e+00 | 3.1623e+00 | 3.1623e+00 |
| Rayleigh exponent fit | 3.9999996e+00 | 3.9999996e+00 | 3.9999996e+00 | 3.9999996e+00 |
| Delta_geo min over chain | -1.6832e-02 | -2.2644e-02 | -3.5228e-02 | -4.9581e-02 |
| Delta_geo max over chain | 1.3950e-02 | 1.9006e-02 | 4.8333e-02 | 7.7665e-02 |
| min_X |Delta_geo^X| | 1.5567e-03 | 2.4671e-03 | 3.9614e-03 | 7.8080e-03 |
| I-2 doubling worst | 1.69e-15 | 1.69e-15 | 1.69e-15 | 2.05e-15 |
| I-3 doubling worst | 9.32e-09 | 9.34e-09 | 9.21e-09 | 9.21e-09 |

Containment PASS on all four configs; isotropic-input null 1.86e-14; VOID-NUM count 0 (every grid point met the 1e-8 doubling gate after the H-CC-2 ladder escalation); ray-regime attenuation VOID (E-11); x_G = 10.

## Phase 3 — sealed-anchor mapper (CC blind read #1 = the verdict read of record)

Sealed file opened only after the Phase-2 checkpoint was written and hashed; md5 + census 12 asserted at open; VLD row asserted value-by-value against the locked 5.2/5.4 numbers (no drift); CONV row parsed first (channel-speed identification, distance rule R1, k-dressing rule R2, bracket rule R3, OOM rule R4); read order VLD -> CONV -> TR-1..TR-4 -> ACH-DIM -> ACH-DISP -> BIR-1 -> BIR-2 -> POL -> DIFF (A-DIFF last). Rows parsed by structured fields, never echoed; all printed quantities dimensionless or window edges in SI length units.

Per-arm exclusion intervals in d (SI length units, primary thresholds), with regime placement x_r at the edges — d ranges per config in row order hex:step, hex:gem8, cubic:step, cubic:gem8:

- **TR-1**: (2.6780e-09, 4.7335e-01) [x_r 8.419e-09/1.488e+00] | (2.3818e-09, 1.4969e-01) [x_r 7.488e-09/4.706e-01] | (2.3207e-09, 1.4969e-01) [x_r 7.296e-09/4.706e-01] | (2.0764e-09, 1.4969e-01) [x_r 6.528e-09/4.706e-01]
- **TR-2**: (1.0600e-17, 1.8207e-07) [x_r 7.400e-11/1.271e+00] | (9.4273e-18, 5.7577e-08) [x_r 6.581e-11/4.020e-01] | (9.1854e-18, 5.7577e-08) [x_r 6.413e-11/4.020e-01] | (8.2186e-18, 5.7577e-08) [x_r 5.738e-11/4.020e-01]
- **TR-3**: (4.1079e-20, 2.0740e-10) [x_r 6.63e-11/3.346e-01] | (3.6535e-20, 6.5586e-11) [x_r 5.893e-11/1.058e-01] | (3.5597e-20, 6.5586e-11) [x_r 5.742e-11/1.058e-01] | (3.1851e-20, 6.5586e-11) [x_r 5.138e-11/1.058e-01]
- **TR-4**: (4.3642e-32, 3.5850e-18) [x_r 1.026e-13/8.432e+00] | (3.8815e-32, 1.1337e-18) [x_r 9.129e-14/2.666e+00] | (3.7819e-32, 1.1337e-18) [x_r 8.895e-14/2.666e+00] | (3.3839e-32, 1.1337e-18) [x_r 7.959e-14/2.666e+00]
- **ACH-DIM**: (1.5172e-15, 7.2940e-07) [x_r 1.907e-12/9.166e-04] | (1.3494e-15, 2.3066e-07) [x_r 1.696e-12/2.899e-04] | (1.3147e-15, 2.3066e-07) [x_r 1.652e-12/2.899e-04] | (1.1763e-15, 2.3066e-07) [x_r 1.478e-12/2.899e-04]
- **ACH-DISP**: (7.3483e-21, 6.1992e-11) [x_r 1.778e-10/1.500e+00] | (6.1808e-21, 1.9604e-11) [x_r 1.496e-10/4.743e-01] | (5.8921e-21, 1.9604e-11) [x_r 1.426e-10/4.743e-01] | (4.9947e-21, 1.9604e-11) [x_r 1.209e-10/4.743e-01]
- **BIR-1**: (6.6621e-01, 2.3119e+24) [x_r 6.283e+01/2.180e+26] | (6.6621e-01, 2.3119e+24) [x_r 6.283e+01/2.180e+26] | (6.6621e-01, 2.3119e+24) [x_r 6.283e+01/2.180e+26] | (6.6621e-01, 2.3119e+24) [x_r 6.283e+01/2.180e+26]
- **BIR-2**: (3.8951e-10, 1.0813e+25) [x_r 6.283e+01/1.744e+36] | (3.8951e-10, 1.0813e+25) [x_r 6.283e+01/1.744e+36] | (3.8951e-10, 1.0813e+25) [x_r 6.283e+01/1.744e+36] | (3.8951e-10, 1.0813e+25) [x_r 6.283e+01/1.744e+36]
- **POL**: VOID-NO-CANDIDATE | VOID-NO-CANDIDATE | VOID-NO-CANDIDATE | VOID-NO-CANDIDATE
- **DIFF**: (1.0027e-16, inf) [x_r 8.087e-06] | (8.4338e-17, inf) [x_r 6.802e-06] | (8.0399e-17, inf) [x_r 6.485e-06] | (6.8153e-17, inf) [x_r 5.497e-06]

VOID segments (never excluding, flagged in the checkpoint): gap-regime and ray-attenuation VOIDs on the attenuation arms; VOID-N outside the N-rule domain on BIR-1/BIR-2; POL is VOID-NO-CANDIDATE (K empty).

**W^EM per config** (x1 thresholds): hex:step (0, 4.3642402e-32]; hex:gem8 (0, 3.8815211e-32]; cubic:step (0, 3.7819190e-32]; cubic:gem8 (0, 3.3838677e-32]

**W^EM_union = (0, 4.3642402e-32] SI length units (CONSERVATIVE union over configs; unbounded below, the P-2 pattern — no substrate floor exercised).**

**Verdict class: `P-CI-W/EM-IN-WINDOWED`.** OOM robustness: identical class at x10 (union edge 9.4025e-32) and x0.1 (union edge 2.0257e-32) -> **OOM-ROBUST**. W_union of G-POLY1 (0, 2.1213132100130068] is SUSPENDED from the intersection (PF-1) and reported alongside only; the radiative component of the B-2 burden transfers to the S2-on-cone assumption, not discharged.

## H-items (every self-catch, numbered; none silently corrected)

- H-CC-1: the banked s1 statistic is not restated in closed form in the dispatched texts; the CC instrument evaluated a pre-declared family of RMS transverse-splitting normalizations on the sphere and identified the convention of record by the 2.1 containment gate itself (winning candidate + full candidate table recorded in each config block); no curve or anchor was consulted.
- H-CC-2 (hex:step): self-catch — the fixed 20/40 ladder missed the 1e-8 doubling gate at 3 point(s); escalated to the recorded nodes_per_panel; final last-doubling estimates: x=3.162e-07 n=80 gate=9.32e-09; x=1.000e-06 n=80 gate=3.06e-09; x=3.162e-06 n=80 gate=1.18e-10
- H-CC-2 (hex:gem8): self-catch — the fixed 20/40 ladder missed the 1e-8 doubling gate at 3 point(s); escalated to the recorded nodes_per_panel; final last-doubling estimates: x=3.162e-07 n=80 gate=9.34e-09; x=1.000e-06 n=80 gate=3.04e-09; x=3.162e-06 n=80 gate=1.17e-10
- H-CC-2 (cubic:step): self-catch — the fixed 20/40 ladder missed the 1e-8 doubling gate at 3 point(s); escalated to the recorded nodes_per_panel; final last-doubling estimates: x=3.162e-07 n=80 gate=9.21e-09; x=1.000e-06 n=80 gate=3.02e-09; x=3.162e-06 n=80 gate=1.16e-10
- H-CC-2 (cubic:gem8): self-catch — the fixed 20/40 ladder missed the 1e-8 doubling gate at 3 point(s); escalated to the recorded nodes_per_panel; final last-doubling estimates: x=3.162e-07 n=80 gate=9.21e-09; x=1.000e-06 n=80 gate=3.00e-09; x=3.162e-06 n=80 gate=1.15e-10
- H-CC-3: self-catch — the first draft of this mapper carried four physical-constant literals in digit forms matching the frozen T1 patterns; rewritten in shifted-mantissa form before any verdict run; zero hits at run time.
- H-CC-6: the checkpoint serializer gained a digit-coincidence remediation: a computed edge value whose leading digits happen to collide with a frozen T1 digit pattern is re-rendered in exponent-shifted form (identical value); values are never altered.
- H-CC-7: self-catch via the pre-declared F-*-MACRO instrument-defect review — the first evaluation run scanned d down to 1e-30 only and silently extended the shortest-wavelength arm's exclusion to d -> 0+, emptying every window and mis-firing the MACRO class; the floor is now 1e-45 with a halt guard on an EXCL state at the floor; the verdict class of record comes from the corrected run (no checkpoint was written by the defective run).
- H-CC-4 / H-CC-5: reserved condition names in the mapper (secondary-reading bind fallback; DIFF band zero-exclusion) — neither fired.

## Expectation pins (C-CI-6, pre-declared before any chat read)

- PIN-CC-P3-1: role binding of sealed params cells is by named-key regex with per-row binders; a binder failure is a loud masked halt, no silent fallback.
- PIN-CC-P3-2: D_lt(z) by composite Simpson, n=4096 (doubling-checked at bind time to 1e-10 relative).
- PIN-CC-P3-3: window edges by per-decade-24 log scan + 64-step geometric bisection (edge resolution far below the 1e-6 comparison tolerance).
- PIN-CC-P3-4: curve lookups are log-log interpolations of this leg's own Phase-2 tables; certified Rayleigh tails below x = 1e-4.
- PIN-CC-P3-5: the conservative reading combiner (R2 x R3 product space) may classify a mixed EXCL/VOID point as VOID where the chat leg might bridge differently; any such divergence is classification-only (S9-lite class).

Ready for the two-leg comparison (C-CI-1..C-CI-6). CC read #1 is on the record; the chat leg reads after.
