# G-TSH4 — CC (blind) leg response to the C1–C6 opening memo

**Leg:** CC / Executor 2, branch `claude/new-session-17ziy6`. All items below are
**post-processing on the already-frozen CC measurement JSONs** — no new GP compute,
no re-optimization, no change to any frozen number. New file:
`tsh4_R2_christoffel.py` → `tsh4_R2_christoffel_output.json`.

## R-1 — CC optimal geometry table (for the C1 close)
Energies are per particle at each structure's **own** optimum; c/a shown for hex.

| kernel | AA (a,c) | AB (a,c) | ABC (a,c) | FCC (L) | BCC (L) |
|---|---|---|---|---|---|
| step | (1.2647, 1.3401) c/a 1.060 | (1.3860, 2.2596) c/a **1.630** | (1.3855, 3.3919) c/a **2.448** | 1.9569 | 1.5581 |
| gem8 | (1.2696, 1.3260) c/a 1.045 | (1.3744, 2.2417) c/a **1.631** | (1.3740, 3.3643) c/a **2.448** | 1.9421 | 1.5394 |

Notes for C1: AB sits at c/a ≈ 1.630 ≈ √(8/3)=1.633 (ideal hcp); ABC at c/a ≈ 2.448 ≈ √6
(FCC containment). These are the CC optima against which the chat leg's frozen
split-step geometries should be differenced. The memo's chat−CC energy pattern
(chat uniformly higher by +0.06…+0.12) is the expected sign if the chat geometries
sit ~1–2 % off these optima; **the geometry offset is the falsifiable prediction** —
if chat's frozen (a,c)/L match this table to ≲0.1 % while energies differ by
0.07–0.12, that is a functional-convention discrepancy → S9 (per R-1).

## R-2 — locked transverse A_3D from the frozen C_ij (conforming; C-POS)
**Nonconformance acknowledged (S9-lite convention finding, recorded):** the CC
Phase-1 report mapped an *axial-vs-basal compression* anisotropy under the non-arm
label "THREE-D-DISTINCT". The **locked** Q-C statistic is the max-from-mean spread
of the **transverse acoustic speeds** over the E4/A-1.4 direction set, mapped to
ISO-3D / UNDERDETERMINED-3D / ANISO-3D. Recomputed here from the CC leg's own frozen
C_ij via the Christoffel closed forms (ρ=1; this is simultaneously the **C-POS
control** — all speeds real, longitudinal purity ≈1.000, so C_ijkl is
positive-definite → C-POS PASS). C13 recovered from the hydrostatic closed form
A_iso = 2C11 + C33 + 2C12 + 4C13.

| kernel | structure | A_3D (max-from-mean of transverse speeds) | **arm** |
|---|---|---|---|
| step | AB | 0.1413 | **ANISO-3D** |
| step | FCC | 0.2233 | **ANISO-3D** |
| gem8 | AB | 0.1774 | **ANISO-3D** |
| gem8 | FCC | 0.2770 | **ANISO-3D** |

Basal isotropy is exact in the transverse speeds: Γ→K and Γ→M give identical
transverse pairs [7.7367, 8.0022] (step AB). The FCC [110] soft transverse
√((C11−C12)/2)=6.39 vs √C44=9.60 is the dominant cubic contribution (textbook).
**Result:** the conforming locked statistic gives **ANISO-3D on both structures,
both kernels** — the same arm the CC leg reached under the non-locked label, and
concordant with the chat leg's ANISO-3D. The convention slip did not change the arm.
Cubic Zener numeric: CC 2.256 / 2.763 vs chat 2.32 / 2.84 — agree to ≈3 %.

## R-3 — C66 measurement independence (resolves S9-F-ISO hypothesis (a))
C66 is measured by an **independent** strain mode, **not** derived from
(C11−C12)/2. In `run_routeS.py` / `tsh4_routeS.py`:
- `C66 = A_xy/4`, from the basal **shear** mode ε_xy=ε_yx=δ (its own 7-point sweep).
- `(C11−C12)/2 = A_dev/2`, from the **deviatoric** mode ε=diag(δ,−δ,0) (separate sweep).

| kernel | A_xy (shear) → C66 | A_dev (deviatoric) → (C11−C12)/2 | \|diff\|/C66 |
|---|---|---|---|
| step | 256.1391 → 64.03478 | 256.1395 → 64.03487 | 1.34e-6 |
| gem8 | 351.9922 → 87.99805 | 351.9927 → 87.99816 | 1.27e-6 |

The F-ISO residual therefore compares **two independent measurements** → it is
**evidential, not definitional**. **Hypothesis (a) (CC circularity) is falsified.**
The surviving explanation for the chat static F-ISO fire (3.25 % / 3.80 %) is
hypothesis (b) — frozen-geometry third-order (e‴·δg) contamination at a reference
displaced ~1–2 % from the optimum — which also reconciles the chat *dynamical*
F-ISO (0.65 %, basal-isotropic) and the CC clean 1.3e-6 at true optima. CC supports
the chat P-3 offer (true-optimum shear re-measurement) as the decisive test.

## R-4 — ground-state residual ledger (retroactive A-2 certification)
A-2 was not activated on the blind leg (no accompanying message; conditional block
requires the author's word in the dispatch — logged as the transmission-layer
defect). Nonetheless **every ground state used for any reported quantity** satisfies
the A-2 gate ‖Hψ−μψ‖/μ ≤ 1e-6 with large margin:

- Phase-0 reported (fine-grid) states: residuals **1e-12 … 9.2e-10** (all 10 states, both kernels).
- Route-S every strain point (max over each mode's 7-point sweep): **2.2e-11 … 9.7e-10** (all 18 mode-runs).

All ≤ 1e-6 by 3–5 orders of magnitude ⇒ **A-2 compliance certified retroactively.**
Full per-state numbers in `tsh4_phase0_measurements.json` (`fconv.res_fine`) and
`tsh4_routeS_measurements.json` (`*.res_max`).

## Author elections (not the blind leg's to make — surfaced for the author)
- **P-2 (Route-D path).** CC can attempt certification (option a) by moving the BdG
  off the truncated plane-wave basis onto a matrix-free full-grid operator seeded by
  the already-converged ground state (res ~3e-10) with a validity gate before trusting
  eigenvalues — the analogue of the chat mechanism. This is real additional compute,
  not pure post-processing; awaiting the author's election among (a) certify / (b)
  accept chat single-leg + logged deferral / (c) exclude Route-D from the fold candidate.
- **P-3 / P-4.** Chat-side action / process rule; CC concurs with both recommendations
  (P-3 yes: R-3 shows the true-optimum re-measurement is the decisive S9-F-ISO test;
  P-4 yes: every dispatch should embed its own activation flags — the A-2 gap here is
  the second transmission-layer defect).

## Net effect on C1–C6
- **C1:** R-1 table supplied → close pending the chat-side geometry diff.
- **C2:** unchanged — CLOSED, two-leg.
- **C3:** R-2 makes the CC Q-C statistic conforming → **ANISO-3D, two-leg concordant**;
  R-3 falsifies the F-ISO circularity hypothesis, leaving the testable (b).
- **C4:** unchanged — Route-D one-legged pending P-2.
- **C5:** R-4 certifies A-2 retroactively; F-ISO conflict now has one surviving hypothesis.
- **C6:** the R-2 conformance blocker is cleared; assembly still gated on S9-F-ISO (P-3).
