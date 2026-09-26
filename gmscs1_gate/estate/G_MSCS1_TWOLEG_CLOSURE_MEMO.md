# G-MSCS1 — TWO-LEG CLOSURE MEMO

**Date:** September 20, 2026. **Base:** V4.82 `d095a7003bb0d4c177e7451e1d14c4c6`. **Memo lock:** v2 `3f30262eaec461fb5fd3202835f7de37`. **Lock record:** `3dbe953b` (Addendum A-2). **Comparator v1.0** `22432b29` + **schema v1.0** `76a42db3` (frozen pre-emission). **Elections (T3):** E-MS-1(a) · E-MS-2(a) · E-MS-2b (a)+(b) · E-MS-2c ⟨001⟩+⟨111⟩ · E-MS-3(a) · E-MS-4(a) · E-MS-5(a) · E-MS-6(a); Amendment A-1 authorized.

## 1. Verification chain on the CC return (chat-side, bytes not prose)

1. **Retrieval.** PR #24 merged to `main` (merge `0378056`); `gmscs1_gate/G_MSCS1_CC_RETURN_INBAND.md` md5 `ae2c3fdb4af9cc6c8ac5248ec02627db` (148,781 B). The dispatch CC worked from is in the tree as `dispatch.md` = the staged `619395f7` byte-for-byte.
2. **Embeds.** Four sentinel blocks re-extracted with the dispatch's own extractor rule, each byte-exact against its declared md5 and against the in-tree copy: instrument `195a2b1baf1589675d4bf18983673a23` (41,561 B) · checkpoint `249e11dd53c4cb82f302b15d3c94c337` (24,415 B) · compare `35d0f762053dd1c48caabf8cad186b16` (1,829 B) · two-leg comparison `d4a5b2713d32443cb7d6dec6c7a3c73f` (69,284 B).
3. **Blindness ordering (git).** `5a4c425` (02:02) — pre-consultation checkpoint; message carries `249e11dd`; the blob at that commit hashes `249e11dd`; the dispatch blob = `619395f7`; **no G-MSCS1 chat artifact in the tree** (the only "chatleg"-named path is `inputs/chatleg_phase0bfull.json` — the X-5 G-POLY1 pin source, a plain embed). `a849af9` (02:02) — CC compare only. `b16d097` (02:04) — first appearance of the decoded chat instrument, checkpoint, compare, report, and the comparison. `945a53d` (02:06) — the return. Order verified.
4. **Comparator run of record (chat-side, frozen v1.0).** chat `c04c0b8e` vs CC `249e11dd` (+ both compare files): **415 checks, 406 PASS, 9 MISS** — the chat-side output is **byte-identical** to CC's own `g_mscs1_twoleg_comparison.json` (`d4a5b271` both sides; the (check, item, result) triples identical) — comparator determinism confirmed.
5. **Independence witness.** Instrument md5s differ; checkpoints not byte-identical; CC's instrument uses a different SO(3) grid (20,12,20), a different μ-moment route (degree-8 Chebyshev fit), the closed-form isotropic projection for the untextured averages, its own Mandel algebra, labelling and HS-reference optimizer (CC-DD-1..6).

## 2. Two-leg verdict: IDENTITY-DELIVERED — zero deviation on every verdict-bearing quantity

Every Phase-1 mean, r_xtal, λ statistic, share, covariance and branch label; every Phase-2 pin, r_agg(t) array (Hill and HS), S_t and κ₂; every born_t0 quantity; every control flag; both falsifier states; the verdict class; and all five hypothesis flags — identical within tolerance, most to the printed digit (r_xtal to 10⁻¹¹, κ₂ to 10⁻¹², D2 exactly). Both legs, without coordination, found the cubic l = 2 texture null and marked the same two hypothesis rows (H-MS-3, H-MS-5) non-concordant for it.

| Quantity (hex_step\|a / hex_gem8\|a) | chat | CC |
|---|---|---|
| r_xtal(S2-E₂) | −2.796720689×10⁻² / −3.933943770×10⁻² | −2.796720689×10⁻² / −3.933943770×10⁻² |
| r_xtal(S2-h) | −1.112878×10⁻³ / −1.314865×10⁻³ | −1.112878×10⁻³ / −1.314865×10⁻³ |
| S_t(E₂) | +1.63×10⁻¹³ / +4.89×10⁻¹³ | +1.61×10⁻¹³ / +4.89×10⁻¹³ |
| κ₂(E₂), Hill | −1.439461769×10⁻³ / −1.895648483×10⁻³ | −1.439461770×10⁻³ / −1.895648483×10⁻³ |
| cubic κ₂(E₂), all four keys | 10⁻¹⁵–10⁻¹⁶ | 10⁻¹⁵–10⁻¹⁶ |
| PIN-A2AGG worst | 6.3×10⁻¹⁴ | 4.4×10⁻¹⁵ |
| PIN-HS0 worst | 1.6×10⁻¹² | 4.6×10⁻¹² |
| doubling residual | 1.8×10⁻¹⁵ | 1.1×10⁻¹⁵ |

## 3. The nine misses, classified (S9)

- **8 × `halving_dev_kappa2` on the four cubic keys, both legs — DEFINITIONAL, pre-declared** (H-MS-2 chat / H-CC-3 CC): κ₂ ≡ 0 on cubic under an l = 2 texture (§4), so the relative halving criterion is 0/0. Not verdict-bearing. Both legs left their checkpoints as computed. Fix: comparator v1.1 candidate `g_mscs1_compare_v1_1.py` `54b329889418a10f4471b90704e0cbcd` (19,261 B; 17/17 suites; T1 CLEAN) — one rule: the per-leg halving check is vacuous when both legs agree |κ₂| ≤ κ₂_abs_floor (10⁻⁶); nothing else changes. **Frozen only on the author's election.** Supplementary chat-side run of v1.1 on the two checkpoints of record: 415 checks, **1 miss** (`948852fe`).
- **1 × `F-CTRL-ADMIX.r_xtal_h_projected` — CHAT-SIDE, instrument + definition** (H-MS-3 chat; H-CC-1 CC): the chat control was coded as a tautology (0.0); CC implemented the memo wording literally and found the number is **not** zero — −0.97×10⁻³ (hex_step) to −1.97×10⁻³ (cubic_gem8). **Two-leg confirmation (diagnostic, not the checkpoint of record):** the chat machinery recomputing the literal projection reproduces CC's eight per-key numbers to ≤ 2.2×10⁻¹⁶. CC's number is the value of record for the control. The control's memo wording is an A-1.3-class defect that survived into v2: the partial projection (quasi-transverse branches only) leaves the quasi-longitudinal branch's EM-weight tail; the complete projection is a tautology. Disposition: the control is reclassified from a physics control to a code-level identity check (complete projection → 0, both legs: chat by construction, CC `x_r_complete_projection_worst = 0.0`); the substantive admixture content moves to §4.

Verdict-bearing quantities: zero deviation. S9 outcome to elect (§6).

## 4. Findings of record (R1-machine two-leg; readings R2)

1. **Species universality is an identity on the untextured aggregate and is protected to first order in an l = 2 fiber texture on every configuration** (|S_t| ≤ 4.9×10⁻¹³, both legs). The textured split is second order: r_agg(t) ≈ κ₂t².
2. **The delivered constraint curve (hex stacking branch): κ₂(S2-E₂) = −1.4395×10⁻³ (step) / −1.8956×10⁻³ (gem8)** under Hill; the Walpole-HS mean scheme within 0.8%; the tetragonal-form and symmetrized arms within 5×10⁻⁴. Sign matches r_xtal(S2-E₂). At full l = 2 texture the species split is 1.4–1.9×10⁻³.
3. **Cubic l = 2 texture null (structural):** a cubic grain carries no l = 2 texture coefficient (the l = 2 harmonic summed over the octahedral orbit of the grain axis vanishes — ⟨001⟩ and ⟨111⟩ alike); ⟨C⟩_t = ⟨C⟩_0 to 10⁻¹² and every species quantity is zero. On the fcc branch the identity is exact to all orders in this family; the first cubic texture effect is l = 4 (E-MS-5's registered successor arm). Refutes the cubic clauses of H-MS-3/H-MS-5 by symmetry — recorded as a refuted prediction, found independently on both legs.
4. **Single crystal:** the E₂ descriptor's speed sits 2.8% / 3.9% below the EM species' on hex, with 83% of its weight on the qSH branch; cubic 1.7–2.1% below on ⟨001⟩ and 1.2–1.4% **above** on ⟨111⟩ — on a cubic lattice the descriptor axis is a genuine choice, recorded, not resolved.
5. **The admixture structure, sharpened by H-CC-1/H-CC-2.** r_xtal(S2-h) (−1.1 to −1.8×10⁻³) has the sign of −Cov_EM(λ_L, v) but the first-order identity −Cov/(3⟨v⟩) is only a 28–34% estimate. Reason, read off the machine: the EM descriptor gives the **quasi-longitudinal branch a small but finite weight (0.5–0.9% of its total, share_EM[qL])** with λ_L ≈ 1 there — far outside the small-λ expansion — and that branch propagates at ~1.8–1.9 c_T; its contribution (−1.0 to −2.0×10⁻³, the literal-projection residual) is of the order of the whole. So the S2-h split is admixture-sourced, as claimed, but the dominant admixture is the *longitudinal-to-transverse leakage on the quasi-longitudinal branch*, not the transverse admixture λ_L on the quasi-transverse branches. This sharpens the Danielewski differentiator (memo §3): an isotropic continuum gives the EM descriptor zero weight on the L branch; the anisotropic substrate gives it ~10⁻² weight on a branch propagating near twice c_T — a single-crystal effect the untextured aggregate removes (λ_L = 10⁻³⁰ at t = 0) and an l = 2 texture restores only at O(t²) (10⁻⁵ at t = 1).
6. **Maxwell-admissibility maps:** ⟨λ_L⟩ = 4.8–9.3×10⁻³, max 3.4–4.3% on the qSV/qT2 branch, identical on both legs.

## 5. Honesty ledger (both legs)

Chat: H-MS-0 (T1 base-list hash discrepancy), H-MS-1 (v1 draft's kill set symmetry-forced; A-1), H-MS-2 (halving 0/0), H-MS-3 (ADMIX tautology), H-MS-4 (tetragonal-form self-test catch), **H-MS-5 (new, post-CC): the memo §4 F-CTRL-ADMIX wording and the §2.6 "O(λ_L²)" claim were both wrong for the same reason — the quasi-longitudinal EM-weight tail; the identity is a ~30% estimate, not a few-percent one. Chat-side definitional defects; CC caught both.** CC: H-CC-1 (ADMIX non-zero, mechanism identified), H-CC-2 (covariance identity 28–34%), H-CC-3 (halving confirmed; v1.1 seconded); CC-DD-1..6; no deviations. T1: CLEAN on every artifact, both legs (collisions logged under the contextual rule: chat 4+1, CC 5+0+6+11; 0 hits); the two list embeds the only scan exemptions in the dispatch; CC's return needed none.

## 6. S9 election requested

- **(a) Close on run 1 as classified** — 8 definitional + 1 chat-side, verdict-bearing quantities at zero deviation; freeze v1.1 as the supplementary run (415 / 1 miss) for the record; no re-emission. *Recommended:* nothing physical rides on either miss, and the ADMIX number is already two-leg confirmed by the diagnostic.
- **(b) Full cycle** — freeze v1.1; chat instrument v1.1 with the substantive ADMIX; S9 mini-dispatch; CC re-run; run 2 expected 415 / 0 (the diagnostic guarantees the ADMIX float agrees to 10⁻¹⁶).

Either way the closure memo's §4 findings and registers are unchanged.

## 7. Registers and non-claims (for the fold)

Every number R1-machine two-leg. The IDENTITY-DELIVERED reading R2, conditional on E-MS-1(a), the untextured import (G-POLY1 E3), K = ∅, the kernel election, and the A-2.3 HS operationalization; the polycrystal postulate remains R3. **§2.91.I Q3 item (1): the emergent species-universality burden is DISCHARGED-AS-IDENTITY on the untextured aggregate, with its corrections quantified and the texture constraint curve κ₂ delivered; the Danielewski differentiation obligation discharged as far as a gate can (attribution table + λ_L and the qL-tail differentiator).** No observable, no bridge, no SI value, no evaluation against any bound; no kill claimed or possible here (memo §5 names the kill surface: E-MS-1(b), the texture import's value, a sealed-anchor comparison).

## 8. Fold plan (V4.83) — awaiting the author's word

- Title/As-of bump; V4.83 fold-in record ahead of V4.82.
- **§2.91.Q** (G-MSCS1) as a bold-lettered paragraph after §2.91.P, before the Cluster J heading.
- One **Part VI** row (Gate G-MSCS1, after the G-QUANTA row).
- Additive brackets: on the §2.91.I Q3 item-(1) chain (the burden's disposition, → §2.91.Q); on the §2.91.O successor sentence (the multi-species question → executed); on §2.91.P and on the V4.82 fold-in record (the housekeeping bracket: PR #23 merged; `gquanta_gate/estate/`; CC's reverse-splice audit; "not yet in the repo" superseded).
- One changelog line. Append-only; reverse-splice to byte identity against `d095a700`. The T1 base list's pin location (`tools/t1/`) and H-MS-0 recorded in the record.

## 9. Estate

Chat: `outputs/gmscs1/` — memo v2 `3f30262e`; lock record `3dbe953b`; schema `76a42db3`; comparator v1.0 `22432b29` (+ v1.1 candidate `54b32988`); T1 `fef28271` / `6b862900` / `05302210`; instrument `db5f51dd`; checkpoint `c04c0b8e`; compare `7b933c08`; execution report `3cf78f51`; dispatch `619395f7`; this memo. CC: `gmscs1_gate/` on `main` (PR #24, head `945a53d`): return `ae2c3fdb`; instrument `195a2b1b`; checkpoint `249e11dd`; compare `35d0f762`; comparison `d4a5b271` (= chat-side run). Not yet in the repo: the chat-side closure memo, the v1.1 candidate, the execution report is (CC committed it from the armor).
