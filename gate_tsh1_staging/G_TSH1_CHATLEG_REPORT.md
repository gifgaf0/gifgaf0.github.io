# G_TSH1_CHATLEG_REPORT — Gate G-TSH1 chat-leg execution record

**Date:** July 18, 2026. **Leg:** chat, from-scratch solver per election D3(a).
**Governing instruments:** `G_TSH1_EXECUTION_PREREGISTRATION.md` (lock md5 `c4b6c37b2abba7911329c6bebd6f5db7`, re-verified byte-identical at execution start) + `G_TSH1_AMENDMENT_1.md` (author-authorized, Phase-0 ψ₆ criterion). Corpus base V4.67 (`3cef6d98...`). Staging authority `f53401d7...`.
**Executable:** `g_tsh1_chatleg.py` (T1 forbidden-string self-grep clean at every invocation). **Raw record:** `g_tsh1_results.json`.

---

## 1. Headline (locked-threshold verdict, quarantined assembly)

**Q1 = T-LINEAR. Q2 = PINNED on axis (i); axis (ii) UNDERDETERMINED (dead-zone exit). Q3 ledger delivered (§6).**

The instantiated substrate **dynamically realizes a propagating linear transverse (shear) channel** — the symmetry-admitted shear invariant of Thm 2.1′ is realized, not merely admitted. Canonical point (g = 22, soft-core, a\* = 1.4575):

| branch | speed (substrate units) | exponent p (primary / robust window) |
|---|---|---|
| second sound (lower L) | c₂ = 1.7650 (secondary) | — |
| **transverse (shear)** | **c_T = 5.7749** | **1.0016 / 1.0136** |
| first sound (upper L) | c_L1 = 11.0453 | 0.9875 / 0.9979 |

R_T ≡ c_T/c_L1 = **0.52284**. Polarization f_T = 1.00 across the window; direction-pair isotropy 1.0% (< 3% log threshold; p6m-isotropic per Thm 2.1′). Convergence n = 32→40: δc_T ≈ 7×10⁻¹¹, δc_L1 ≈ 1×10⁻¹² (F2 ceiling 1%).

## 2. Phase 0 (under Amendment 1) — PASS

ψ₆ = 0.9730 (≥ 0.814 ✓, ψ₄ = 0.0282 ✓), 217 peaks vs ideal 217.4 (±10% ✓); a\* = 1.4575 (target 1.4576 ± 0.5% ✓); μ = 55.8536 ∈ [55.6, 56.2] ✓ (post-polish); three gapless branches at q_tiny with ω₄ = 22.25 ✓; **F9 Ward gate:** GP residual 1.89×10⁻³ (≤ 5×10⁻³ ✓), raw w²_min(kf = 0.005) = −0.029 (> −0.05 ✓).

## 3. Controls (Phase C) — both PASS

**C-NEG** (uniform fluid, g = 10, same functional/cell): contrast 1.0000, zero T-classified modes, exactly one gapless branch — the pipeline does not hallucinate shear. **C-POS** (classical triangular central-spring lattice, dispersion derived symbolically in-file): classifier recovers the transverse branch, T-LINEAR (p = 0.992/0.976), f_T ≥ 0.95, window fits within 1.1%/3.3% of the symbolic slope (5% tolerance for the exact-dispersion finite-window bias, H2).

## 4. Phase 2 sweep — R_T across the locked axes

| point | ψ₆ (anneal) | a\* | c_T | c_L1 | **R_T** | n32→40 δR_T |
|---|---|---|---|---|---|---|
| soft g=22 | 0.973 (τ40) | 1.4575 | 5.7749 | 11.0453 | **0.52284** | ~10⁻¹⁰ |
| soft g=28 | 0.973 (τ40) | 1.4347 | — | — | **0.52861** | 5×10⁻¹¹ |
| soft g=34 | 0.885 (τ40) | 1.4165 | — | — | **0.53476** | 5×10⁻¹¹ |
| soft g=44 | 0.970 (τ80, D3) | 1.3930 | 8.6718 | 15.9513 | **0.54364** | 5×10⁻¹¹ |
| γ6 g=35 | 0.765 (τ40, D4) | 1.4378 | 6.6184 | 13.2673 | **0.49885** | 1×10⁻¹¹ |

**Axis (i):** D = 2.10% ≤ 3% → **PINNED** — the ratio holds to ~2% while the individual speeds change by ~50% and a\* drifts 4.4%. **Axis (ii):** pooled max deviation D = 5.11% ∈ (3%, 10%) → **UNDERDETERMINED** per the locked dead zone (T3: no re-tuning; the exit is real). Everything consumed lies in-set {kernel form, g, ρ₀}: **zero new import delta** as a computational fact; the formal §6 sub-classification (DERIVED-RATIO vs DERIVED-OF-LOCATED-IMPORT) stays open pending an axis-(ii) resolution — successor-gate material, author-gated.

**Post-verdict R2 annotation (permitted by T2, claiming nothing):** the classical central-force spring-lattice ratio from the in-file symbolic control is 0.4330/0.75 ≈ 0.577; the measured soft-core band 0.523–0.544 sits 6–9% below it — the GP supersolid does **not** inherit the naive central-force value.

## 5. Deviations and honesty ledger (all pre-verdict, all logged open)

**D1** ψ₆ depth-dependence → Amendment 1 (authorized). **D2** (cosmetic) direction labels swapped vs true BZ families; both computed, isotropy 1.0%, no verdict impact. **D3** g=44 glassy at τ=40, crystallized at τ=80 (same protocol, deeper anneal). **D4** the D3 two-tier depth convention applied uniformly in the γ6 search; g=30 near-threshold, disordered at both depths, passed over; g=35 first-passing.
**H1** T1 self-grep initially tripped on its own concatenated list (check bug; file never contained a forbidden string). **H2** C-POS slope tolerance 5% for finite-window bias. **H3 (material):** the split-step Trotter-bias residual (6.3×10⁻²) broke the translation Ward identity, producing spurious ω² < 0 (to −1.03 at q→0) and a fake transverse soft onset — caught by the (L+2X)∇ψ₀ = 0 control **before any verdict**; fixed by dt-staged polish (residual → 1.9×10⁻³); permanent falsifier **F9** added; the contaminated first Phase-1 pass VOIDED and recomputed. **H4** the "phase" pick captured gapped optical modes; second sound rides the lower L branch (c₂ re-derived; secondary only).

## 6. Q3 — Declaration ledger (compute-free; always delivers; nothing adjudicated)

1. **EM-carrier declaration** (M.ONT-adjacent). A-SHEAR's one-carrier claim needs a declared answer to *which framework structure carries the EM wave* before "EM rides the transverse channel" has content. Register: absent. Successor: declaration memo + gate; the Danielewski differentiation obligation (transverse wave = Maxwell wave in the Planck–Kleinert cousin) attaches here.
2. **Envelope constitutive/phase class.** Polar-analog textures carry linear magnons; ferromagnetic-analog quadratic (LSF §6.4). This gate's result narrows the stakes: a **lattice** transverse carrier exists regardless, so the envelope class now governs only the texture-channel route. Register: undeclared. Successor: declaration.
3. **2D→3D stack structure** (§2.88.B transverse-isotropy caveat). Promotion of the in-plane shear branch to the full 3D transverse sector is unadjudicated. Register: open caveat. Successor: computation gate on a stacked/3D instantiation.
4. **c-definition move** (M.REL scale axis). Whether c_T ≡ c is a *definition* of c (content: EM and GW share one channel) or a *claim* (requiring the μ = ρ_s c² import). Register: undecided; kept fully unexercised here (T4 substrate-units discipline). Successor: author declaration.

## 7. Consequence surface

Per the locked §10: no CARRIER-ROUTE-CLOSED arm fired — the instantiated-substrate carrier route is **OPEN and delivered**. A-SHEAR remains an explicit assumption, but it now has a **live instantiated carrier candidate with a machine-verified linear shear branch**, its speed ratio g-pinned at 2% within the kernel class. The M.CW scale import (any physical c_T statement) stays named and unexercised. No KC evaluated; GW170817 numbers appeared in no computation; Paper IIA, T1–T5, the retired longitudinal estate, §2.90, μ_n, §2.52 Open 3 all untouched. Fold candidate on two-leg agreement + authorization: **§2.91.I** + one Part VI row. Register ceilings: numerics/arms R1-at-thresholds (pending two-leg); Q3 ledger R2.

## 8. Comparison items for the CC leg (locked §9; S9 on any verdict-level disagreement)

C1 Phase-0 PASS (under A1) · C2 three gapless branches {second sound L, transverse, first sound L} + gapped optical at ω ≈ 22.25 · C3 Q1 arm **T-LINEAR** · C4 canonical (c_T, c_L1, R_T) = (5.7749, 11.0453, 0.52284), cross-leg tolerance ≤ 3% · C5 Q2 arm **PINNED(axis-i)/axis-ii UNDERDETERMINED**, D_i = 2.10%, D_ii = 5.11%, all-in-set imports · C6 Q3 item-set = the four items of §6.
**CC-leg notes:** gz1-lineage reuse permitted (D3(a)); the locked artifact + this report's A1 travel together; **the F9 Ward control is mandatory** — an unpolished state reproduces the H3 spurious instability; C-NEG control mandatory; thresholds immutable per T3.
