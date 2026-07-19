# G-TSH1 — CC-Leg Report (independent second leg: supersolid shear channel)

**Date:** 2026-07-19 · **Governing instruments (by reference):** `G_TSH1_EXECUTION_PREREGISTRATION.md`
lock md5 `c4b6c37b2abba7911329c6bebd6f5db7` + `G_TSH1_AMENDMENT_1.md` (author-authorized "Authorize A1",
Phase-0 ψ₆ criterion) · **Chat leg:** `g_tsh1_chatleg.py` / `G_TSH1_CHATLEG_REPORT.md` /
`g_tsh1_results.json` · **CC scripts:** `tsh1_cc_reduce.py` (analytic + raw re-reduction),
`tsh1_cc_bdg.py` + `tsh1_cc_polish.py` + `tsh1_cc_sweep.py` + `tsh1_cc_controls.py` (from-scratch GP+BdG).

> **Two-leg result: VERDICT-LEVEL AGREEMENT — Q1 = T-LINEAR; Q2 = PINNED(axis-i)/axis-ii
> UNDERDETERMINED. NO S9.** Independent from-scratch GP ground state + Bogoliubov spectrum reproduces
> every comparison item C1–C6 to **0.0–0.3%**, with **both mandatory controls (F9 Ward, C-NEG)
> satisfied** and the **H3 tiny-q Trotter instability independently reproduced and cured**.

## Lock / scope note (honest)
The locked pre-registration file itself was **not** in the CC hand-off — only its md5 `c4b6c37b…`,
cited identically in the chat script, Amendment 1, and the chat report. The lock is therefore
confirmed **by cross-reference, not byte-for-byte**. Amendment 1's authorization ("Authorize A1")
is on record in the amendment file. Substrate units (ħ=m=1) throughout; no physical-unit or KC
statement appears in any CC script (T1/T4 discipline held; independent forbidden-constant grep clean).

## Independence
Own primitive-cell grid **Nc=120** (chat 96), own dt schedule + finer polish stages, own reciprocal
truncation **n=28** (chat 32), own μ extraction, own polarization classifier, own slope reducer
(c=Σkω/Σk², p from log–log), own Ward + C-NEG controls, own tabulated γ6 Hankel transform. The BdG
operator (ω² f = L(L+2X)f, Hermitianized) is the correct supersolid Bogoliubov problem — physics, not
shared code. gz1-lineage reuse permitted (D3(a)).

## Results — comparison items C1–C6

| Item | Chat | CC (independent) | agree |
|---|---|---|---|
| **C1** Phase-0 anchors | a*=1.4575, μ=55.85, 3 gapless + optical 22.25 | a*=**1.4575**, μ=**55.857**, gapless {0,0,~0} + optical **22.25** | ✓ |
| **C2** branch set | {2nd-sound L, transverse, first-sound L} + gapped optical ω≈22.25 | same structure recovered | ✓ |
| **C3** Q1 arm | T-LINEAR (p≈1.00) | **T-LINEAR**, p_T=**0.998**, p_L=0.986 | ✓ |
| **C4** (c_T, c_L1, R_T) canonical | 5.7749, 11.0453, 0.52284 | **5.7796 (0.1%)**, **11.0472 (0.0%)**, **0.52317 (0.1%)** | ✓ (≤3%) |
| **C5** Q2 axis-(i) | PINNED, D_i=2.10% | **PINNED**, indep D_i=**2.08%** | ✓ |
| **C5** Q2 axis-(ii) | UNDERDETERMINED, D_ii=5.11% | **UNDERDETERMINED**, indep D_ii=**5.12%** | ✓ |
| **C6** Q3 ledger | 4 declaration items | item-set audited present/consistent (compute-free) | ✓ |

### Axis-(i) sweep — independent BdG at every soft-core point
| g | a* (CC) | c_T (CC) | c_L1 (CC) | R_T (CC) | R_T (chat) | Δ |
|---|---|---|---|---|---|---|
| 22 | 1.4575 | 5.7796 | 11.0472 | 0.52317 | 0.52284 | 0.1% |
| 28 | 1.4347 | 6.6289 | 12.5404 | 0.52861 | 0.52861 | 0.0% |
| 34 | 1.4166 | 7.4318 | 13.8972 | 0.53477 | 0.53476 | 0.0% |
| 44 | 1.3931 | 8.6700 | 15.9477 | 0.54365 | 0.54364 | 0.0% |

Independent **D_axis_i = 2.08%** (< 3% → PINNED): the individual shear speed changes **~50%**
(5.78 → 8.67) while the ratio holds to 2% — the pinning is real, reproduced on a second solver.
**γ6-kernel axis-(ii):** R_T = **0.49888** (chat 0.49885, 0.0%); pooled D = **5.12%** in the locked
dead-zone (3%,10%) → UNDERDETERMINED, the second kernel genuinely moving the ratio.

## Mandatory controls
- **F9 Ward (translation identity).** Independently reproduced **H3**: the underpolished ground state
  (GP-res 6.3×10⁻³) gives raw w²min(kf=0.005) = **−0.088** (fails >−0.05) — a spurious tiny-q
  instability. Deep polish (GP-res **6.9×10⁻⁴**) flips it to **+0.0014** (F9 PASS). The shear speed is
  **robust across the cure** (c_T 5.7568 → 5.7796, 0.4%): the H3 contamination is a q→0 artifact that
  does not touch the finite-q fit window — a fully independent confirmation of the chat's H3 diagnosis
  and F9 fix.
- **C-NEG (null).** Uniform superfluid (g=10, below crystallization): contrast **1.0000**, **zero**
  T-classified modes, exactly **one** gapless branch → PASS. The classifier does not manufacture shear.

## Analytic / re-reduction layer (zero shared machinery)
- **C-POS** classical triangular central-force lattice re-derived symbolically from scratch:
  c_T=√3/4, c_L=3/4, **c_T/c_L=1/√3** (Cauchy relation λ=μ). Measured GP band 0.523–0.544 sits
  **5.8–9.4% below** this — the supersolid does not inherit the naive central-force ratio (chat's
  post-verdict R2 note, independently confirmed).
- **Independent re-reduction** of the chat's raw ω(k) arrays with my own reducer reproduces
  (c_T, c_L1, R_T) to **<0.3%**, isotropy |c_T(ΓK)−c_T(ΓM)|/c_T = **1.02%**, and D_i=2.10% / D_ii=5.11%
  — auditing the chat's fit/classification/verdict layer.
- **Amendment 1** monotonicity check: ψ₆(τ) = 0.427→0.525→0.662→0.862→0.973 is strictly increasing and
  the canonical 0.834 lies on the trajectory (τ≈22) — the amended criterion certifies the same object
  at equal-or-greater order; Eddington-adjacent depth-tuning correctly rejected.

## Scope held / honesty
Radial→in-plane shear only; the 2D→3D stack promotion (Q3 item 3) is unadjudicated. My leg confirms the
**cell-level** crystal (a*-energy minimum + localized droplet + 3 gapless branches) and all BdG physics;
I did **not** re-run the 160²-box ψ₆ quench — the Phase-0 object-level anchors (a*, μ, Goldstone count)
are what I independently reproduced, and the a*-minimum + droplet localization is the crystallization
witness. No KC evaluated; no GW170817/physical-c numbers in any computation; Paper IIA, T1–T5, the
retired longitudinal estate, §2.90, μ_n, and §2.52 Open 3 all untouched.

## Consequence (concur with chat routing)
No CARRIER-ROUTE-CLOSED arm fired — the instantiated-substrate shear carrier is **OPEN and delivered**,
now with a **machine-verified linear transverse branch on a second independent solver**, its speed ratio
g-pinned to 2% within the kernel class and kernel-class-sensitive across it. A-SHEAR remains an explicit
assumption but has a live instantiated carrier candidate. The M.CW scale import (any physical c_T
statement) stays named and unexercised. **Fold candidate §2.91.I + one Part VI row on two-leg agreement
+ explicit author authorization** — agreement now achieved; authorization is the author's to give.

---
*Filed 2026-07-19. Independent GP+BdG (Nc=120, n=28), both mandatory controls satisfied, H3/F9
reproduced. Verdict-level agreement across C1–C6; no S9.*
