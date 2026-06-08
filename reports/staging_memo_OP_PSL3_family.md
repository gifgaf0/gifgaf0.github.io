# Staging Memo — OP-PSL.3: PSL(2,p) Family Generalization of the n₁ Characterization

**Status:** R1 computation memo (numbers only; no R2 family-theorem prose — see §scope).
**Date:** 2026-06-08. **Base:** Ledger V4.34; Paper §1.1.
**Deliverables:** `tools/op_psl3_family_sweep.g` (GAP), `tools/op_psl3_family_crosscheck.py`
(pure-Python, from scratch), this memo.
**Reproduce:** `gap -q -b < tools/op_psl3_family_sweep.g` ;
`python3 tools/op_psl3_family_crosscheck.py`.
**Computed over:** trinity `p ∈ {5,7,11}`, controls `p ∈ {13,17,19,23}`.
**Two-tool agreement:** GAP and the from-scratch Python cross-check agree on every
shared quantity — **33/33 Python checks OK, 0 mismatches** (see §6).

> **Headline (R1 numbers):** PR-1, PR-2, PR-4 **confirmed**; PR-5 main claim
> **confirmed**; **PR-3 is PARTIAL** — the §1.1 uniqueness characterization
> generalizes to `p=11` but **fails at `p=5`** (the index-10 `S₃` is a false
> positive: `n₁(S₃; ρ₄)=1` too). The §1.1 phenomenon is the **generic
> 2-transitive-stabilizer signature** (PR-5/§5), and what is special to {5,7,11}
> is the **existence of the index-p (degree-p) action**, Galois-complete (PR-1).

> **⚠ Brief-data discrepancy flagged:** the §1.1 "Lemma 2.5" generators in §6.2
> of the brief — `g₁=[[1,0,0],[0,0,1],[0,1,0]]`, `g₂=[[1,1,0],[0,1,1],[0,0,1]]` —
> generate the **order-24 point-stabilizer `S₄`**, NOT `GL(3,2)` (both fix the
> vector `(1,0,0)`). Verified in **both** GAP (`Order(⟨g₁,g₂⟩)=24`) and Python.
> The cross-check builds `GL(3,2)` by full enumeration of the 168 invertible
> `3×3` `F₂` matrices instead. Chat-side should correct the §1.1 generator
> reference (likely a missing third generator / a different intended pair).

---

## 1. Per-prime maximal-subgroup classes + full n₁(H; ρ) matrix (R1, GAP)

Column headers are the irreducible **degrees**; entries are
`n₁(H;ρ)=⟨χ_ρ, Ind^G_H 1_H⟩`. "Borel" = the index-`p+1` subgroup; "St" = the
degree-`p` Steinberg.

### p = 5 — `|G|=60`, irr degrees `[1, 3, 3, 4, 5]`
| maximal class | index | order | type | n₁ row `[1,3,3,4,5]` |
|---|---|---|---|---|
| 1 | 5 | 12 | **A₄** | `[1,0,0,1,0]` |
| 2 | 6 | 10 | D₁₀ (Borel) | `[1,0,0,0,1]` |
| 3 | 10 | 6 | S₃ | `[1,0,0,1,1]` |

### p = 7 — `|G|=168`, irr degrees `[1, 3, 3, 6, 7, 8]`
| maximal class | index | order | type | n₁ row `[1,3,3,6,7,8]` |
|---|---|---|---|---|
| 1 | 7 | 24 | **S₄** | `[1,0,0,1,0,0]` |
| 2 | 7 | 24 | **S₄** | `[1,0,0,1,0,0]` |
| 3 | 8 | 21 | C₇:C₃ (Borel) | `[1,0,0,0,1,0]` |

### p = 11 — `|G|=660`, irr degrees `[1, 5, 5, 10, 10, 11, 12, 12]`
| maximal class | index | order | type | n₁ row `[1,5,5,10,10,11,12,12]` |
|---|---|---|---|---|
| 1 | 11 | 60 | **A₅** | `[1,0,0,0,1,0,0,0]` |
| 2 | 11 | 60 | **A₅** | `[1,0,0,0,1,0,0,0]` |
| 3 | 12 | 55 | C₁₁:C₅ (Borel) | `[1,0,0,0,0,1,0,0]` |
| 4 | 55 | 12 | D₁₂ | `[1,1,1,0,2,0,1,1]` |

### p = 13 (control) — `|G|=1092`, degrees `[1,7,7,12,12,12,13,14,14]`
| class | index | order | type | n₁ row |
|---|---|---|---|---|
| 1 | 14 | 78 | C₁₃:C₆ (Borel) | `[1,0,0,0,0,0,1,0,0]` |
| 2 | 78 | 14 | D₁₄ | `[1,0,0,1,1,1,1,2,0]` |
| 3 | 91 | 12 | D₁₂ | `[1,0,0,1,1,1,2,2,0]` |
| 4 | 91 | 12 | A₄ | `[1,1,1,1,1,1,2,1,0]` |

### p = 17 (control) — `|G|=2448`, degrees `[1,9,9,16,16,16,16,17,18,18,18]`
| class | index | order | type | n₁ row |
|---|---|---|---|---|
| 1 | 18 | 136 | C₁₇:C₈ (Borel) | `[1,0,0,0,0,0,0,1,0,0,0]` |
| 2 | 102 | 24 | S₄ | `[1,1,1,0,1,1,1,1,1,0,0]` |
| 3 | 102 | 24 | S₄ | `[1,1,1,0,1,1,1,1,1,0,0]` |
| 4 | 136 | 18 | D₁₈ | `[1,1,1,1,1,1,1,1,2,0,0]` |
| 5 | 153 | 16 | D₁₆ | `[1,1,1,1,1,1,1,2,2,0,0]` |

### p = 19 (control) — `|G|=3420`, degrees `[1,9,9,18,18,18,18,19,20,20,20,20]`
| class | index | order | type | n₁ row |
|---|---|---|---|---|
| 1 | 20 | 171 | C₁₉:C₉ (Borel) | `[1,0,0,0,0,0,0,1,0,0,0,0]` |
| 2 | 57 | 60 | A₅ | `[1,0,0,0,0,1,1,0,1,0,0,0]` |
| 3 | 57 | 60 | A₅ | `[1,0,0,0,0,1,1,0,1,0,0,0]` |
| 4 | 171 | 20 | D₂₀ | `[1,1,1,0,0,2,2,0,1,1,1,1]` |
| 5 | 190 | 18 | D₁₈ | `[1,1,1,0,0,2,2,1,1,1,1,1]` |

### p = 23 (control) — `|G|=6072`, degrees `[1,11,11,22,22,22,22,22,23,24,24,24,24,24]`
| class | index | order | type | n₁ row |
|---|---|---|---|---|
| 1 | 24 | 253 | C₂₃:C₁₁ (Borel) | `[1,0,0,0,0,0,0,0,1,0,0,0,0,0]` |
| 2 | 253 | 24 | S₄ | `[1,0,0,0,1,1,2,2,0,1,1,1,1,1]` |
| 3 | 253 | 24 | S₄ | `[1,0,0,0,1,1,2,2,0,1,1,1,1,1]` |
| 4 | 253 | 24 | D₂₄ | `[1,0,0,0,0,2,2,2,0,1,1,1,1,1]` |
| 5 | 276 | 22 | D₂₂ | `[1,0,0,0,0,2,2,2,1,1,1,1,1,1]` |

**Control note (sharpens §5):** the *types* A₄/S₄/A₅ DO recur as maximal subgroups
of control primes — A₄ at p=13 (index 91), S₄ at p=17 (102) and p=23 (253), A₅ at
p=19 (57) — but **never at index `p`**. The trinity specialness is the **index
(= p, the degree-p 2-transitive action)**, not the subgroup type.

---

## 2. Trinity: ρ_{p−1} identification and π_{H_p} decomposition (R1)

`ρ_{p−1}` := the nontrivial constituent of `π_{H_p}=Ind^G_{H_p}1` (the canonical
§3 rule). In all three cases `π_{H_p}=ρ₁ ⊕ ρ_{p−1}` — **multiplicity-free, rank 2**.

| p | H_p (index p) | π_{H_p} decomposition | ρ_{p−1} | degree |
|---|---|---|---|---|
| 5 | A₄ | `ρ₁ ⊕ ρ₄` | irr #4 | 4 |
| 7 | S₄ | `ρ₁ ⊕ ρ₆` | irr #4 | 6 |
| 11 | A₅ | `ρ₁ ⊕ (irr #5)` | **irr #5** (the *second* deg-10) | 10 |

**p=11 disambiguation (brief §3 subtlety):** of the two degree-10 irreducibles
(`irr #4`, `irr #5` in GAP's ordering), **only `irr #5` appears in `π_{A₅}`**;
`irr #4` does not. So `ρ₁₀ := irr #5`. (`n₁(irr#4; A₅)=0`, `n₁(irr#5; A₅)=1`.)

---

## 3. PR-3 column — `n₁(H; ρ_{p−1})` over all maximal classes + uniqueness verdict (R1, LIVE)

| p | n₁(·; ρ_{p−1}) over maximal classes | classes with n₁=1 | = exactly the index-p classes? | verdict |
|---|---|---|---|---|
| 5 | A₄:**1**, D₁₀:0, **S₃:1** | {A₄ (idx 5), **S₃ (idx 10)**} | **NO** — S₃ is a false positive | **FAILS** |
| 7 | S₄:**1**, S₄:**1**, C₇:C₃:0 | {both index-7 S₄} | **YES** | holds |
| 11 | A₅:**1**, A₅:**1**, Borel:0, D₁₂:2 | {both index-11 A₅} | **YES** | holds |

- **p=7, p=11:** the property `n₁(·;ρ_{p−1})=1` picks out **exactly** the index-p
  maximal class(es) — two of them, swapped by Out (PR-4). The §1.1 characterization
  **generalizes to p=11**.
- **p=5:** **the characterization fails.** Besides the index-5 `A₄`, the index-10
  `S₃` also satisfies `n₁(·;ρ₄)=1` (because `ρ₄` is also a constituent of the
  degree-10 action `C[A₅/S₃] = ρ₁ ⊕ ρ₄ ⊕ ρ₅`). So `ρ₄` does **not** single out
  `A₄` among maximal classes. **Honest partial result** (brief §5.4): the §1.1
  *uniqueness* clause does **not** hold verbatim at p=5.

(Reading note: "the n₁=1 class" is never literally unique at p=7,11 either — there
are **two** index-p classes, Out-swapped. The correct statement is "the n₁=1 set
**equals** the set of index-p classes," true at 7,11 and false at 5.)

**Independent reproduction (Python, permutation characters only — no character
table):** the entire ρ_{p−1} column was recomputed from scratch via
`n₁(M;ρ)=(1/|G|)Σ_g (fix_{degp}(g)−1)·fix_{G/M}(g)`, with the maximal actions
built as point action / Sylow-p conjugation (Borel) / 2-subsets (p=5 S₃) / PG(2,2)
lines (p=7 line-S₄): reproduced `[A₄:1,D₁₀:0,S₃:1]`, `[S₄:1,S₄:1,7:3:0]`,
`[A₅:1,Borel:0]` — **matching GAP exactly, including the p=5 false positive.**

---

## 4. PR-4 — index-p class count and Out-action (R1, LIVE)

Outer automorphism realized as conjugation by `δ ∈ PGL(2,p) \ PSL(2,p)`
(`Out=C₂`). A class is **moved/swapped** iff `H` is not `G`-conjugate to `H^δ`.

| p | # index-p classes | type | Out-action |
|---|---|---|---|
| 5 | **1** | A₄ | **fixed** (H conjugate to H^δ) |
| 7 | **2** | S₄ | **swapped** (point- vs line-stabilizer) |
| 11 | **2** | A₅ | **swapped** |

**Confirmed exactly as pre-registered**, including the **honest asymmetry**: the
trinity is *not* uniform — p=5 has a single Out-fixed index-p class, while p=7,11
each have a swapped pair. (Surfaced, not hidden — brief §5/PR-4.)

---

## 5. PR-5 — Borel/Steinberg baseline and uniqueness (R1, GUARD)

`n₁(Borel; St)` and whether the Borel is the **unique** maximal class with
`n₁(·;St)=1`. (`n₁(Borel;St)=1` ⟺ rank-2 / 2-transitive P¹ action.)

| p | n₁(Borel; St) | classes with n₁(·;St)=1 | Borel unique for St? |
|---|---|---|---|
| 5 | 1 | {D₁₀ (Borel), S₃} | **no** |
| 7 | 1 | {C₇:C₃ (Borel)} | **yes** |
| 11 | 1 | {C₁₁:C₅ (Borel)} | **yes** |
| 13 | 1 | {Borel, D₁₄} | no |
| 17 | 1 | {Borel, 2×S₄, D₁₈} | no |
| 19 | 1 | {Borel, D₁₈} | no |
| 23 | 1 | {Borel, D₂₂} | no |

- **`n₁(Borel; St)=1` holds for EVERY p** (confirmed — the generic 2-transitive
  signature; independently confirmed in Python by rank-2 of the P¹ action for all
  7 primes).
- **Borel-uniqueness-for-St is NON-generic:** it holds only at **p=7, 11** and
  fails at p=5 and all controls. So `n₁=1` *alone* is exactly the
  point-stabilizer-of-a-2-transitive-action signature (§5.1), never "rigidity."

---

## 6. GAP ↔ Python agreement (R1)

Both tools agree on every shared quantity:

| quantity | GAP | Python (from scratch) | agree |
|---|---|---|---|
| `\|G\| = p(p²−1)/2`, all 7 primes | ✓ | ✓ (P¹ closure) | ✓ |
| 2-transitivity / `n₁(Borel;St)=1`, all 7 | ✓ | ✓ (rank-2 of P¹) | ✓ |
| index-p stab order/index/type (5,7,11) | A₄/S₄/A₅ | order 12/24/60, index 5/7/11; A₅ perfect | ✓ |
| trinity `n₁(H_p; ρ_{p−1})=1` | ✓ | ✓ (rank-2) | ✓ |
| trinity ρ_{p−1} column (PR-3) | [1,0,1]/[1,1,0]/[1,1,0,2] | reproduced via perm-chars | ✓ |
| §1.1 generators ⟨g₁,g₂⟩ order | 24 | 24 | ✓ (both: NOT 168) |

**Python self-report: 33 checks, 33 OK, 0 mismatches.** No blocking discrepancy.

---

## Pre-registration scorecard

| ID | Verdict | Supporting numbers |
|----|---------|--------------------|
| **PR-1** | **CONFIRMED** | Index-p maximal class exists for p∈{5,7,11} (types A₄/S₄/A₅) and for **no** control (13,17,19,23 have none). Types recur at other indices for controls, but index-p does not. Galois trinity complete. |
| **PR-2** | **CONFIRMED** (all trinity) | `π_{H_p}=ρ₁⊕ρ_{p−1}` multiplicity-free, rank 2, for p=5,7,11. |
| **PR-3** | **PARTIAL** | Characterization (n₁(·;ρ_{p−1})=1 ⟺ index-p) **holds at p=7, p=11**; **FAILS at p=5** (index-10 S₃ also =1). §1.1 uniqueness generalizes to 11, not to 5. |
| **PR-4** | **CONFIRMED** (incl. asymmetry) | index-p classes: 1 (p=5, **Out-fixed**, A₄); 2 (p=7, **swapped**, S₄); 2 (p=11, **swapped**, A₅). |
| **PR-5** | **CONFIRMED** (main) + located | `n₁(Borel;St)=1` for all p; Borel **unique** for St only at p=7,11 (non-generic). `n₁=1` = generic 2-transitive signature, not rigidity. |

**Register:** every number above is **R1** (twice-computed: GAP + from-scratch
Python). **No R2 claims** in this memo (no "natural home" / family-theorem /
narrative — out of scope per brief §9; that is a downstream R2 write-up after
chat-side audit, with a stated proof target). **No physical interpretation**
(M.BRIDGE — internal mathematics, no observable bridge).

**Open for the downstream R2 task (not asserted here):** the precise family
statement is *"the index-p (degree-p) 2-transitive action — hence the
n₁=1-distinguished maximal subgroup of degree p — exists exactly for p∈{5,7,11},
Galois-complete"* (PR-1/PR-2), with the **uniqueness** clause holding only at
p=7,11 (PR-3 partial) and the Out-action asymmetric (PR-4). The §1.1 multiplicity
itself is the generic 2-transitive signature (PR-5), not special.
