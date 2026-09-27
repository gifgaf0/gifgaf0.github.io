# G-MSCS2 — CHAT-LEG PHASE 0 EXECUTION REPORT (pins and controls)

**Date:** September 26, 2026 (run at 14:33 UTC; 4 m 00 s). **Base:** V4.84 `f36bbdb0`. **Memo lock:** v2 `efdcabdcd937cda4acb64f941dc4bb2b` (46,053 B). **Lock record:** `49232d4c` (Addendum A-2.1–A-2.10). **Schema v1.0** `66f586d7` + **comparator v1.0** `80d3b907` (18/18 suites) — FROZEN before this emission. **T1 gate list** `be921b8c` (36 patterns; scanner `6b862900`). **Instrument:** `g_mscs2_chatleg.py` `f277580ddf0b4da9734d11edb009c54b` (7/7 selftest suites). **Checkpoint (Phase 0, partial by directive):** `g_mscs2_chatleg_phase0_checkpoint.json` `9e5a6e8ba0804bda778e4be52fbe2fde` (7,747 B); run log `72d64aeb`. T1: instrument, memo and checkpoint CLEAN (halt-on-hit; no override path); one numeric formatting collision logged in the log file under the contextual rule (0 hits).

**Scope of this run (the author's directive of September 26, 2026):** Phase 0 only. Phases 2–3 are implemented in the instrument and were **not executed**; the verdict class is NOT ASSEMBLED. Guards held: memo md5+bytes, T1 list md5, scanner md5, X-1 `200e7a8b` (md5+bytes), X-6 chat `c04c0b8e` and cc `249e11dd`.

## 1. Result: all 13 pins and controls PASS

| Item | Threshold | Value | Reading |
|---|---|---|---|
| **PIN-XTAL** — r_xtal (both arms), ⟨λ_L⟩, max λ_L on the 8 keys vs X-6 | worst rel ≤ 10⁻⁸ | **0** (bit-identical) | the inherited single-crystal machinery reproduces G-MSCS1 exactly |
| **PIN-VRH0** — v_T(t = 0) Voigt / Reuss / Hill on the 8 keys vs X-6 | ≤ 10⁻⁸ | **0** | idem |
| **PIN-HS0** — v_T(HS lo/hi), G_HS bounds and the optimized references vs X-6 | ≤ 10⁻⁶ | **0** | the A-2.3 reference optimization reproduced (references listed in the checkpoint witness) |
| **PIN-K2** — the l = 2 family re-run with this gate's ODF machinery: κ₂(S2-E₂, Hill) on the 4 hex keys vs X-6; cubic null | hex rel ≤ 10⁻⁴; cubic abs ≤ 10⁻¹² | **1.39×10⁻¹²** / **2.16×10⁻¹⁵** | −1.439461769 / −1.438702719 / −1.895648483 / −1.896137467 ×10⁻³ reproduced to 12 digits; the cubic l = 2 null reproduced (|κ₂| ≤ 2.2×10⁻¹⁵) — **the continuity pin that makes κ₄₄ comparable to G-MSCS1's κ₂** |
| **F-CTRL-ISO** — isotropic tensor: r_xtal, λ_max, r_agg(t₄) both families | ≤ 10⁻¹⁰ | 4.4×10⁻¹⁶ | texture on an isotropic grain does nothing |
| **F-CTRL-SO3** — ODF-averaged E₂ fraction = 2/5 for every mode at t = 0; r_agg(0) | ≤ 10⁻¹⁰; ≤ 10⁻⁶ | 5.0×10⁻¹⁶; 0 | the SO(3) identity |
| **F-CTRL-POS** — min ODF weight over the SO(3) grid, every family/grid used (incl. the exhaustion probes) | ≥ 0 | 0.395 | all ODFs positive |
| **F-CTRL-L2NULL** — cubic: l = 2 at t = 1, and P₂ added to the K̃₄ family, leave ⟨C⟩_V, ⟨S⟩_R, C_HS and r_agg unchanged | ≤ 10⁻¹² | 5.8×10⁻¹⁴ | the cubic l = 2 null holds jointly with l = 4 (κ₂₂ = κ₂₄ = 0 on cubic is an identity) |
| **F-CTRL-L4EXHAUST** — an l = 6 term (t₆ = 0.3; hex P₆ / cubic K̃₆) on top of t₄ = 0.3 changes tensors and r_agg | ≤ 10⁻¹² | tensors 4.3×10⁻¹⁴; r_agg 4.4×10⁻¹⁶ | **elasticity and the descriptor pair see the ODF only through l ≤ 4 — the (t₂, t₄) family is the general axisymmetric weak texture for this gate** |
| **F-CTRL-C4** — ⟨C⟩_V(t₄) − ⟨C⟩_V(0) = t₄·(H/3)·𝒯⁴(ẑ) (Voigt entries 3, 3, 8 / 1 / −4, −4 / −4, −4 / 1 over 105, H = C₁₁ − C₁₂ − 2C₄₄); Reuss likewise with H_S; affinity at 0.6 vs 2×0.3; H = 0 tensor | ≤ 10⁻¹² | closed form 2.5×10⁻¹⁴; affine 4.1×10⁻¹⁴; H = 0: 2.3×10⁻¹⁴ | **the textured cubic aggregate is exactly the isotropic aggregate plus t₄·(H/3)·𝒯⁴ — a five-constant transversely isotropic medium whose entire l = 4 response is the Zener combination** |
| **F-CTRL-MARG** — SO(3)-direct ODF average of the per-grain E₂ weight vs the S²-marginal form 1 + c·t₄·P₄ (c_⟨001⟩ = 1, c_⟨111⟩ = −2/3), both cubic configurations, both descriptor axes, every mode | ≤ 10⁻¹² | 8.3×10⁻¹⁶ | the marginal coefficients of A-2.5 are exact |
| **F-CTRL-TEX4** — synthetic cubic tensor (H = 120) at t₄ = 1, ⟨001⟩, Hill | \|r_agg\| > 10⁻⁶ | 4.12×10⁻⁴ | the instrument can see an l = 4 descriptor split |
| **F-CTRL-QUAD** — k̂-sphere doubling (128 × 256) on r_agg at t₄ = 0.25; SO(3) doubling (32, 20, 32) on ⟨C⟩_V at t₄ = 0.3 | ≤ 10⁻¹⁰ | 2.2×10⁻¹⁶; 2.3×10⁻¹⁴ | both quadratures exact at the working degrees |

## 2. What Phase 0 establishes (R1-machine, chat leg; the CC leg re-derives all of it blind)

1. **Continuity.** This gate's texture machinery *is* G-MSCS1's on the l = 2 family — the banked κ₂ curve, the single-crystal splits, the t = 0 speeds and the HS references reproduce to 12 digits or exactly. Whatever κ₄₄ Phase 2 returns is on the same footing as the banked κ₂.
2. **The two identities that define the gate hold to machine precision on the banked tensors:** l ≥ 6 texture is invisible to every observable (exhaustion), and on the fcc branch the l = 2 term is null jointly with l = 4, so the fcc texture response is the l = 4 term alone (cubic-effective). Both are controls, never results; both are now witnessed on the substrate's own tensors, not only on the synthetic pre-draft check.
3. **The exact closed form of the cubic l = 4 response is confirmed on both fcc configurations:** the whole texture dependence of the Voigt/Reuss aggregate is t₄·(H/3)·𝒯⁴(ẑ) with H the Zener combination — so the fcc branch's texture response is one number per configuration times a fixed rational tensor. (Phase 2's κ₄₄ is then the descriptor pair's second-order reading of this one-parameter deformation; the O(t₄) qSH/qSV birefringence along k̂ ⊥ ẑ is exactly Ht₄/21 on the Voigt tensor, A-2.6.)
4. **The marginal reduction of the descriptor average is exact** — c_⟨001⟩ = 1, c_⟨111⟩ = −2/3 — which is what makes the ⟨111⟩ descriptor's l = 4 response the negative two-thirds of the ⟨001⟩ descriptor's at the weight level; whether the sign flip of r_xtal carries into κ₄₄ (HYP-MS2-2) is a Phase-2 question.

## 3. Honesty items (chat side, this run)

- **H-MS2-1 (pre-lock, disclosed):** the closed forms of A-2.2/A-2.6 and the marginal coefficients were derived chat-side (sympy) before the lock and verified numerically on a generic synthetic tensor before the memo v2 was written; they entered the lock record as operationalizations to be asserted, not as results; the Phase-0 run asserts them on the banked tensors.
- **H-MS2-2 (build):** the instrument's selftest S2 initially failed on the test's own rotation matrix (the body-diagonal test used the transpose of the intended rotation); the test was corrected (no instrument code path changed) before any run; the instrument md5 above is the final one.
- **H-MS2-3 (housekeeping, recorded not resolved):** the author's lock directive states the HK-1 PRs merged with placeholder numbers; the live remote at lock (14:10 UTC) shows `main` = `d0a0e31`, no `gmscs1_gate/estate/` on any branch, the V4.79 canonical at the root (memo §10, A-2.4).
- **D-MS2-1 (none):** no deviation from the locked order of operations; Phases 2–3 not run by directive.
- **Scan hygiene (recorded for the next lock):** two forbidden numeric renderings were caught by the T1 scanner in drafting — a machine-precision residual in the draft memo and a synthetic selftest value in the comparator — both reworded before freezing; they were coincidences with digit strings on the stratum, not references.

## 4. Next steps (per the locked order of operations; on the author's word)

Phase 2 (the K̃₄ / P₄ sweeps, the fits, the birefringence coefficient, the hex quadratic form) → Phase 3 (verdict, last) → execution report → P-4/P-4.c dispatch with the T1 lists in-band → CC leg blind from scratch (method variation: a different SO(3) quadrature or the analytic generalized-spherical-harmonic route) → two-leg comparison (v1.0) → S9 on misses → fold authorization → V4.85.
