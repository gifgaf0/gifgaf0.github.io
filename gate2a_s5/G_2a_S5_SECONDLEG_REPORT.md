# G-2a-S5 SECOND-LEG REPORT (CC, independent)

**Date:** 2026-07-09 · **Pre-registration:** `G_2a_S5_EXECUTION_PREREGISTRATION.md` (archived here) ·
**Scripts:** `gate2a_s5_secondleg_HA_HC.py` (H-A + H-C), `gate2a_s5_secondleg_HB.py` (H-B) ·
**Base:** V4.53 candidate (G-2a-S4 folded).

> **Status:** This is the CC independent leg, run from the pre-registration. I did **not**
> receive the chat-side first-leg report; the results below stand on their own independent
> machinery and are ready to cross-check for two-leg agreement when the first leg lands. Every
> falsifiable claim is decidable finite-group / finite-algebra computation, reproduced here.

## §6 Literature-Search-First (MANDATED, done before computation)
Searched for any published identification linking the Borromean symmetry/motion group to
PGL(3,2)/Fano-plane line stabilizers (the knot-theory ↔ finite-geometry cross-dialect bridge this
gate proposes). **Result: none found.** The pieces exist separately in the literature — Fano plane
↔ Aut = PGL(3,2)=PSL(3,2), order 168; Borromean rings ↔ pyritohedral point group (order 24, ≅ ±A₄)
/ two ideal regular octahedra / order-48 tessellation symmetry — but no source bridges the
*group-level* motion-S₄ ↔ line-stabilizer-S₄ identification. The framework-internal content
(U(L), the ZD kernels, §2.73's forced base) has no external collision surface, as the pre-reg
anticipated; the proposed bridge is not pre-empted by prior art. *(Sources listed at end.)*

## Zero-shared-machinery contract (honored)
The first leg is specified to build Stab(L) as explicit matrices in a chosen basis + reuse §2.85's
kernel scripts. This leg instead:
- specifies L by the **dual/functional** description L = ker(φ), φ = top-bit read-off, and verifies
  the functional and setwise stabilizer descriptions agree;
- builds transvections **intrinsically** as t_d = I + d·φᵀ over 𝔽₂;
- does H-A(iii) existence/uniqueness by **abstract cocycle** computation (H¹/H² of S₃ on the 𝔽₂
  std-module) *in addition to* an explicit Φ, per the second-leg spec;
- builds the **sedenions from scratch** (Cayley–Dickson R→C→H→O→S) for H-B, independent of §2.85;
- does H-C via the **binary octahedral group as unit quaternions** + character sums, no numpy
  tensor Sym³.

## H-A — the identification (PASS, R1)
| clause | result |
|---|---|
| **H-A(i)** | \|Stab(L)\|=24; pointwise stabilizer ker(Stab(L)→Sym(L)) has order 4, elementary abelian; its 3 nontrivial elements are exactly the transvections t_d with axis L, indexed by direction d ∈ L. |
| **H-A(ii)** — *decisive falsifier* | Over all 72 (g,d) pairs, **g·t_d·g⁻¹ = t_{g(d)}**: conjugation sends the transvection at point d to the transvection at point g(d). The direction-indexing **intertwines** the §2.73-identified S₃ action — **no outer twist**. The decisive falsifier is **NOT triggered.** |
| **H-A(iii)** | Explicit Φ: motion-S₄ → Stab(L) covering id_{S₃} and matching the kernel indexing (motion "un-flipped strand i" ↦ transvection t_i) exists. Motion kernel V₄^mot = {+++, +−−, −+−, −−+}, each nontrivial element indexed by its single un-flipped strand = a point of L — the declared complement convention. |
| **H-A(iii) abstract** | The extension 1→V₄→S₄→S₃→1 is **split** (4 complements exist ⇒ [H²]=0) with **\|H¹(S₃,V₄)\|=1** (all complements V₄-conjugate) — the cocycle route confirms split + unique-up-to-conjugacy independently of the explicit Φ. |
| **H-A(iv)** — uniqueness | Exactly **4** isomorphisms Φ cover id_{S₃} and match the kernel indexing — i.e. Φ is unique **up to the 4 inner automorphisms by V₄**, matching the pre-reg's expectation exactly (Aut(S₄)=Inn(S₄); the 4 conjugations by V₄ fix both the S₃-quotient and the kernel indexing, and are the only ones that do). |

**H-A verdict:** the motion-S₄ and the Fano line-stabilizer S₄ are **canonically identifiable over
the §2.73-forced S₃**, not merely abstractly isomorphic. The convergence is a genuine
identification, R1.

## H-C — the convergence collapse (PASS, R1)
Built 2O as 48 unit quaternions; computed the spin-3/2 character χ_{3/2}(q) = Σ_{k=0}^{3} cos((3−2k)ψ),
cos ψ = Re(q), which is exact on the double cover (distinguishes q from −q).
- ⟨χ_{3/2}, χ_{3/2}⟩_{2O} = **1** → irreducible; χ(1)=**4** (dim 4); χ(−1)=**−4** → **−1 ↦ −Id**,
  genuinely spinorial.
- So Sym³(ℂ²) restricted to 2O **is** the unique genuine 4-dim irrep (G-2a-S1's D1=1). The two
  V4.53 convergent routes' 4-dim modules coincide as 2O-reps under Φ's lift. **H-C: PASS, R1.**
- Caveat per pre-reg §3: **the §2.50 import is NOT supplied by this gate** — identifying the group
  downstairs does not produce −1 ↦ −Id as a *physical* per-strand phase; it collapses "one import
  feeding two routes" to "one import feeding one structure." M.BRIDGE untouched.

## H-B — module dictionary (PARTIAL: module type reproduced; within-doublet action flagged)
Independent sedenion build reproduces the ZD structure: **7 six-assessor box-kites**; each box-kite's
6 assessors split into **3 strut-opposite pairs = 3 points of a line L**; the six-ZD S₃-module type
is **2·triv ⊕ 2·std₃** (two copies of the natural 3-point permutation rep), matching §2.85's U(L).
- **Rigorous:** the V₄ kernel = ker(Stab(L)→S₃) acts **trivially on the point content**, so each
  transvection **preserves each ZD kernel as a summand** — §2.85's "preserves each kernel
  individually," reproduced at the S₃-module level.
- **Flagged, NOT claimed:** the precise *within-doublet* action of each transvection needs the
  canonical §2.85 map Stab(L) → Aut(ZD-structure), which lives in the framework project and I did
  **not** reconstruct. I make **no** claim about which assessor maps where inside a doublet; the
  natural "single reflection in the point-i doublet, trivial elsewhere" is stated only as an **R2
  structural expectation**, to be confirmed chat-side against §2.85. Honest boundary, not laundered.

## Register ceilings / discipline
M.CW: the identification (H-A) and the module iso (H-C) are R1 finite-group facts; all physical
readings (H-B dictionary, the "turn-over ↔ transvection" reading) are R2. No observable bridge, no
μ_n, no dynamical claim; the §2.50 per-strand spinor phase remains the open import (unchanged).
§2.52 Open 3 untouched. **Distinct-S₄ (spatial-O):** explicitly OUT OF SCOPE — the spatial-rotation
O is a third S₄-class object; no claim made, its distinct-S₄ flag retained.

## Verdict (second leg)
- **H-A: PASS (R1)** — canonical identification over §2.73; decisive falsifier H-A(ii) not
  triggered; Φ unique up to the 4 V₄-inner autos; split extension, \|H¹\|=1 (independent cocycle).
- **H-C: PASS (R1)** — both 4-dim modules = the unique genuine 4-dim 2O-irrep; convergence collapses
  to one structure; §2.50 import still not supplied.
- **H-B: module type reproduced (R1 for the 2·triv⊕2·std S₃-content); exact transvection
  dictionary flagged** as needing the canonical §2.85 map (SQT-audited boundary, R2 expectation).
- **Two-leg agreement:** H-A and H-C are complete independent legs ready to match the first-leg
  report; H-B agrees at module-type level, with the within-doublet action left to chat-side.

**Sources (mandated search):** Fano plane / PGL(3,2): en.wikipedia.org/wiki/Fano_plane ,
finitegeometry.org/sc/8/plane.html . Borromean symmetry / geometry: mathunion.org/outreach/logos/borromean-rings ,
en.wikipedia.org/wiki/Borromean_rings , arXiv:math/0402212 (CKS). No source bridges the group-level
motion-S₄ ↔ line-stabilizer-S₄ identification.
