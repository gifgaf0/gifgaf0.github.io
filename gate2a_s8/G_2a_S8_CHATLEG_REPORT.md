# G-2a-S8 CHAT-LEG EXECUTION REPORT
## The spinorial structure of the flat crystallographic home

**Executed:** July 10, 2026, chat-side, same session as registration lock.
**Pre-registration:** `G_2a_S8_EXECUTION_PREREGISTRATION.md` (locked verbatim before compute).
**Script:** `g_2a_s8_chatleg.py` (md5 `273f4d35b661a6a101694488301af76d`), exact arithmetic
(Fractions; ℚ(√2) quaternions), 47/47 assertions, deterministic, no numeric targets.
**Base:** SQT_Master_Ledger_v4_56_CANONICAL.md (md5 `1b1dc6b8824daf5c9c06c521d97065db`).

---

## 1. Registered claims vs. outcomes

| Registered item | Outcome | Grade |
|---|---|---|
| **H-A** — extension 1 → ℤ/2 → Γ̃ → Γ → 1 non-split | **CONFIRMED.** All 8 generator sign-assignments fail (every lift of every deck π-rotation squares to the central (−1, 0), both lifts, verified in the full unquotiented Spin(3)⋉ℝ³). Positive control: the same solver finds all 8 sections over the torus subgroup — the negative is a property of Γ, not the solver. | R1, falsifier live, did not fire |
| **B1** — ambient-2π meridian sign, all structures | **FORCED(−1).** 24/24: for every strand f and all 8 twists χ ∈ Hom(Γ, ℤ/2), monodromy(μ_f) = (χ_f q_f)² = −1. Structure set realized concretely: all 8 Ũ_χ verified as genuine homomorphisms on Γ̃₂ (16×16) with Ũ_χ(z) = −Id. | R1 |
| **B2** — turn-over sign system | **GRADED (the registered (c2)+(c3) decomposition):** (i) every lift of every turn-over e_f is an **involution** in Q̃ — square = +Id, never −Id — in sharp contrast with the deck π-rotations (order 4, square = z); (ii) S₄-equivariance **collapses** the three per-strand turn-over signs to **one global ℤ/2** = χ(t₍₁,₁,₁₎), the body-diagonal antiperiodicity bit; (iii) Hom(Q, 𝔽₂) enumerated exhaustively: **exactly 4 homomorphisms** = {admissible χ ∈ {(+,+,+), (−,−,−)}} × {sgn-twist of S₄}, with turn-over values uniform per hom and equal to χ₁χ₂χ₃. | R1 |
| **Verdict class** | **SPLIT** (pre-declared class): B1-FORCED + B2-CHOICE, with the choice located as a **single boundary-condition bit**. | R2 (H-D grading below) |

Supporting R1 facts established en route: Γ^ab ⊗ 𝔽₂ ≅ (ℤ/2)³ on r̄₁, r̄₂, r̄₃ with [Γ,Γ] = 2ℤ³ exactly (commutators supply ⊇; abelian exponent-2 quotient of order 8 supplies ⊆); t₍₁,₁,₁₎ attained as the word r₁r₂r₁r₃r₁ with class r̄₁+r̄₂+r̄₃; the N⁺-conjugation action on Γ^ab ⊗ 𝔽₂ is the **bare permutation representation** (no t₁₁₁-correction — machine columns: c₃ the 3-cycle, g₄ the (23)-transposition, e₁ trivial), so the invariant characters are exactly the diagonal {0, (1,1,1)} — and the admissible-restriction set matches it exactly.

## 2. The two channels, separated

The gate's sharpest yield is a clean separation that S7's R3 bank had left adjacent:

- **The meridian channel carries the −1.** A full ambient 2π rotation about any strand acts on every orbifold-native spinorial structure as −Id — forced, twist-independent, because the tangent holonomy of the cone loop is the π-rotation whose *both* spin lifts square to −1. This is the exact FR-relevant object G-2a-S4/S5 located as the single shared import.
- **The turn-over channel does NOT carry the −1.** Every lift of every turn-over translation is an involution; the −1 never appears in its square. What the turn-over system carries is at most **one** global ℤ/2 — the spin boundary condition along the body diagonal, χ(t₁₁₁) — and full N⁺-equivariance forces strand-uniformity: either all three turn-overs act with +, or all three with − (the two admissible diagonal structures). The canonical (pure argument-shift) lifts compose as T₁T₂T₃ = χ(t₁₁₁)·Id.

The S7 bank's "turn-over = half-lattice translation, adjacent to §2.50 thinking" is thereby **bounded precisely**: the adjacency is real but the turn-over is not where the spinor phase lives.

## 3. H-D verdict [R2; M.REL per-axis]

**Scale** — none anywhere. **Metric** — flat, inherited (unchanged from S6/S7 grading). **Sign** — B1 forced; B2 residual = one located ℤ/2 import (the body-diagonal antiperiodicity bit; the classical T³ spin-structure datum surviving into the normalizer — the positive control's 8 torus sections are exactly those structures, and the flat home's equivariance whittles the three independent torus bits down to their diagonal combination). **Ontology** — everything conditional on (i) the cone-π singular scaffolding (S7's undeclared physical import, R3) and (ii) the carrier identification (framework per-strand ℂ² ↔ orbifold spinor), **NOT made by this gate**, quarantined throughout.

**Relocation statement (the honest ceiling):** conditional on the two ontology imports, the *sign content* of the §2.50 per-strand spinor phase costs nothing further — the flat home forces −1 ↦ −Id (H-A) and forces the 2π meridian to realize it (B1). The §2.50 import therefore RELOCATES from "an unexplained sign" to "the ontological commitment that the physical strand carrier is the orbifold spinor of the flat home," plus one boundary-condition bit in the turn-over sector. **This is a sharpened LOCATED-IMPORT, explicitly NOT a §2.50 closure.** μ_n untouched; no observable; M.CW/M.BRIDGE intact.

## 4. Scope refinement recorded honestly (adjacent context, R2, not machine-verified)

The B1 forcing is a property of **orbifold-native** structures (those extending over the singular locus): upstairs is simply connected, so the only twists are Hom(Γ, ℤ/2), all meridian-even. On the **punctured** smooth part alone — deleting the singular circles and forgetting the orbifold extension — meridian classes are nonzero in H₁ (standard for complements), so spin structures exist there whose μ_f-holonomy is +1. The −1 forcing is therefore *precisely* the cone-π scaffolding doing work: requiring the spinorial structure to extend over the strand is what pins the sign. This sharpens, and does not weaken, the import accounting of §3 — the scaffolding import was already declared; this locates what it buys.

## 5. Banked R3 (uninterpreted, per registration)

The cone loop m_f carries ±q_f — order 4, sign twist-dependent: a **ℤ/4 refinement** of the ℤ/2 phase native to the cone-π geometry (half-meridian ↦ ±i-type element). Logged only.

## 6. Eddington attestation

No numeric targets anywhere; μ_n sealed. The −1 = −1 identification trap held: the gate's statements are about orbifold spinors; no identification with the framework carrier was made or used. The loop dictionary (m_f vs μ_f, 2π-C) was applied exactly as registered; no 2π substitution occurred. Both B2-admissibility branches were genuinely live — the (−,−,−) admissibility was decided by the machine (it IS admissible), not assumed. Registration-time hand-sketches (q² = −1; the triple relation) disclosed in the pre-registration and superseded by the machine legs. The conjugation matrices and the g₄/c₃ grid solves **re-derive** two S7 H-B slices (odd-coset (½,½,½) shift class; even-coset integrality) — flagged as re-derivations serving as cross-checks, not imports.

## 7. Two-leg status

Chat leg complete (this report). **CC leg pending** — handoff spec in `G_2a_S8_CC_HANDOFF.md`. Shared-presentation caveat expected per the S4/S7 precedent: the Γ presentation is the both-legs-verified S7 object; CC independence is required at the code+method level (different representation encouraged — SU(2) complex matrices over ℚ(i, √2), or a cohomological extension-class route — plus CC's own generator solves and its own word search for t₁₁₁).

## 8. What this gate does NOT claim (restated from registration)

No §2.50 closure. No spinor physics for the actual K₇ tube. No μ_n, no observable. No Pin/orientation-reversing content — the amphichiral involution's spinorial behavior (Pin⁺ vs Pin⁻ fork) stays the S9 candidate bank. The §2.52 Open 3 row untouched.

## 9. Fold-in staging (awaiting CC leg + author authorization)

Proposed shape on two-leg completion: §2.87.G (after §2.87.F, before Cluster G) + one Part VI row + one additive discharge-style annotation on §2.87.F's R3-bank item (a) (the turn-over dictionary — now bounded by this gate) + the KF partial-discharge annotation (separate sibling item, separately authorized). Append-only; no §3.x; no register change to anything prior; the §2.52 Open 3 row untouched.
