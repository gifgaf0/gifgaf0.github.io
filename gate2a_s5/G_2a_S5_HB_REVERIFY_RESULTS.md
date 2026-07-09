# G-2a-S5 — H-B RE-VERIFICATION (CC second leg on the errata-class correction)

**Date:** 2026-07-09 · **Script:** `gate2a_s5_secondleg_HB_reverify.py` · **Base:** V4.54 CANONICAL
(`74a34bdd5b64346389d3c77ffb9c3dc7`) · **Chat leg audited:** `g_2a_s5_chatleg.py` +
`G_2a_S5_CHATLEG_REPORT.md`.

## What this closes
V4.54 folded an **errata-class canon correction**: §2.85 Part C's mechanism sentence *"the V₄
kernel preserves each kernel individually"* is **false at the kernel level** — V₄ fixes each ZD
*element* but **permutes** the six distinct line kernels. A canon sentence declared false warrants a
genuine second leg; the chat filed a re-verification spec (framework data only, zero shared code).
This is that leg — and it **independently confirms the correction in full.**

## Independence (zero shared code; different arithmetic)
- The chat leg computed kernels over the prime field **𝔽₉₁₁**. This leg uses **exact rationals
  (ℚ, `fractions.Fraction`)** — a different field, so agreement cannot be a modular artifact.
- All linear algebra (RREF, rank, nullspace, subspace equality/membership, restriction,
  eigenspaces) is written from scratch here.
- Shared only as **framework data** (not code, per the spec): the CD convention
  (a,b)(c,d)=(ac−conj(d)b, da+b·conj(c)), the line L={1,2,3}, the twelve ZD labels e_a ± e_{b+8},
  and the doubled transvection action fixing e₀, e₈.

## Results — every filed target reproduced exactly over ℚ
| # | claim | CC/ℚ result |
|---|---|---|
| 1 | each of the 12 labels e_a ± e_{b+8} has a dim-4 left-kernel | **CONFIRMED** (all 12) |
| 2 | exactly **6 distinct** kernels, 2 labels each, with the stated ± pairing | **CONFIRMED** — K0=ker(e₁+e₁₀)=ker(e₂−e₉), …, K5=ker(e₂−e₁₁)=ker(e₃+e₁₀), all six identifications hold over ℚ |
| 3 | V₄ fixes each ZD *element* but **permutes** the six kernels: t₁:(K0 K1)(K4 K5) fix K2,K3; t₂:(K2 K3)(K4 K5) fix K0,K1; t₃:(K0 K1)(K2 K3) fix K4,K5 | **CONFIRMED exactly** — every ZD element fixed (indices 1,2,3,9,10,11), induced kernel permutation matches the spec element-for-element |
| 4 | pattern: t_d fixes the pair {a,b} with a⊕b = m(d), m=(1→2→3→1) | **CONFIRMED** — m = {1:2, 2:3, 3:1} |
| 5 | headline R1 survives: all **24** Stab(L) elements preserve U(L) (dim 8) | **CONFIRMED** — U(L) is 8-dim; all 24 preserve it as a subspace (built the full GL(3,2)→Stab(L) independently) |
| 6 | each t_d is an involution on U(L), eigdims (+1:4, −1:4); pairwise +1-meet = 2 (the 2·triv) | **CONFIRMED** — involution, (4,4) eigdims, all three pairwise +1-intersections = 2 |

## Verdict
- **The errata-class correction is now TWO-LEG confirmed.** §2.85 Part C's "preserves each kernel
  individually" is false; the correct mechanism is that V₄ **permutes** the six line kernels
  (t_d fixing the pair with a⊕b = m(d)), so U(L)-invariance holds **without** Stab(L) ⊂ Aut(𝕊) —
  exactly as the additive annotation folded into V4.54 states.
- **The headline R1 survives, re-confirmed on a second leg:** all 24 Stab(L) elements preserve U(L).
- **The module dictionary is two-leg:** each strand-d turn-over acts on U(L) = 2·triv ⊕ 2·std₃ as an
  involution fixing 2·triv ⊕ the χ_d line in each std₃ copy and negating the other two (eigdims
  (4,4); pairwise +1-meet = the 2·triv).
- **m-cycle (1→2→3→1):** reproduced; provenance left uninterpreted (R3), per canon.

This retires the "CC H-B re-verification queued" open item from the V4.54 fold. My earlier
`gate2a_s5_secondleg_HB.py` reached module-type only and correctly flagged the within-kernel action
as needing the canonical map; that flag is now discharged by this exact-ℚ computation from the filed
framework data.

## Fold audit (V4.54, output-faithfulness — byte-splice is SQT-verified, not second-legged)
Audited the uploaded `SQT_Master_Ledger_v4_54_CANONICAL.md` in place (not copied into this repo, per
standing no-duplication rule):
- md5 = `74a34bdd5b64346389d3c77ffb9c3dc7` — matches the fold's claimed output hash.
- §2.85 Part C original mechanism sentence retained **byte-verbatim**; the correction is an
  **additive** parenthetical annotation appended to it — faithful to "body verbatim, additive only."
- §2.87.D (Gate G-2a-S5) present; one Part VI G-2a-S5 row present; CC commit `7cd0d5a` cited.
- §2.52 **Open 3** table rows present (8 rows) — untouched, per standing instruction.
- The fold script's discipline (anchor-uniqueness asserts, md5 before/after, reverse-splice
  reconstruction to the exact V4.53 md5, Open 3 byte-check) is sound on read.
- **Boundary:** V4.53 source is not in this code repo, so I confirm **output faithfulness**, not the
  byte-additivity reconstruction — that remains the SQT's verification (canonical lives in the
  framework project; not duplicated here).

*Register: R1 (the kernel-permutation mechanism, U(L)-invariance, module dictionary — now two-leg).
R3 (m-cycle provenance). M.CW/M.BRIDGE intact; no μ_n; §2.50 remains the single open import;
spatial-O leg of the distinct-S₄ flag remains open; §2.52 Open 3 untouched.*
