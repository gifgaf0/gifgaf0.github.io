# G-2a-L1 SECOND-LEG REPORT (CC, independent) — the spin–isospin locking assembly

**Date:** 2026-07-11 · **Locked pre-registration:** `G_2a_L1_EXECUTION_PREREGISTRATION.md`
(md5 `da9c25d19ff91f2c0809ac0027a7bebb`) · **Script:** `gate2a_L1_secondleg.py` (exact Cℓ(3)± over
ℚ(√2)) · **Base:** V4.62 · **Chat leg:** `g_2a_L1_chatleg.py`.

> **Two-leg status:** the locked pre-reg + chat leg were provided together; I ran this CC leg against
> the locked text (clean order honored — the L1 registration locked before I executed). The CC leg
> uses the pre-reg's **requested method variation** (the direct cohomological route for B1) and
> **reproduces the chat leg's verdict on every decisive bit.**

## Method (independent) + collision check
Own Cℓ(3)^q build (blade-integer, ℚ(√2)); the **cohomological route** for B1 (the induced-cover
question posed as: can any character carry the central z to the nontrivial ℤ/2 class?), plus a
Chebyshev character build for the Spin side. Only the S7 Γ/N presentation is shared (flagged).
**In-execution collision check:** no published derivation of soliton spin–isospin locking from
orbifold spin-structure data, nor of "which double cover a flat-orbifold spin structure induces" for
the #24/Hantzsche–Wendt family. **Novel-in-assembly**, as registered. *(Sources at end.)*

## B1 — which extension does the flat home induce on M = N/Γ ≅ ℤ/2×S₄?
**Verdict: NOT-INDUCED-BY-OBSTRUCTION** (a re-posed obstruction, matching the chat leg).
- **The obstruction (cohomological):** the central z (Spin's −1) is a **commutator in Γ̃**:
  **[q̃₁, q̃₂] = z** (the cone-loop lifts q̃_f = bivectors; [q̃₁,q̃₂] = q₁q₂q₁⁻¹q₂⁻¹ = −1),
  verified in **both Pin types**. Since every character χ: Γ̃→ℤ/2 has an abelian target, **χ(z) =
  χ([q̃₁,q̃₂]) = +1**. Confirmed exhaustively: Γ̃₂ (order 16) has **8 characters, all of which kill z**.
- Therefore the D1 pushforward κ_χ = χ∘c **can never carry z to the nontrivial ℤ/2 class** — the flat
  static home does **not** manufacture a non-split double cover of the motion group by this route.
- **D2 collapse (control, verified as a lemma):** |Ñ₂/Γ̃₂| = **48 = |M|** in both Pin types — the sign
  z is absorbed into the deck image (z ∈ Γ̃), so there is no residual ℤ/2.

**Consequence:** the spatial 2O of §2.87.A's postulate is **not** produced by the static flat home; the
2O locking substrate is **relocated to the loop/motion sector** (S4's FR route), where the π-rotation
lifts square to −1. (Regression anchors: |Ñ₂|=768, |Γ̃₂|=16, D2=48, both types.)

## F2 discriminator (control) — 2O vs GL(2,3)
Built 2O (order 48, from Clifford lifts) and GL(2,3) (order 48) independently. **2O has a unique
involution (−1 only)** — every order-2 element of O lifts to **order 4** (the binary-cover
fingerprint). **GL(2,3) has non-central involutions** (transpositions lift at order 2). The two
double covers of S₄ are **separated** by transposition-lift order, so the machine — not an assumption
— identifies the internal locking cover as **2O**, not GL(2,3). (Eddington two-covers trap held.)

## B2 — transport along Φ and module uniqueness
**Verdict: ASSEMBLED-RELOCATED** (matching the chat leg).
- **S1 regressions reproduced:** ⟨χ_{3/2}, χ_{3/2}⟩_{2O} = **1** (irreducible); **χ_{3/2}(z) = −4**
  (genuine, central −1 ↦ −Id).
- **Exactly 2 lifts over id_{S₄}** (a torsor over Hom(S₄,ℤ/2)), both fixing z.
- **The sgn-twist is invisible on the 4-dim module:** χ_{3/2} **vanishes on every sgn=−1 class**
  (verified against [O,O]=A₄, order 12), so the sgn-twist acts trivially on Sym³(ℂ²) → **module
  transport is UNIQUE.** The locking's structural content is derived-conditional, with the substrate
  on the loop sector (B1) and the full S8/S9 import list carried.

## B3 — admissibility lattice + Assignment disposition
FR-style (J,I) multiplicities via character inner products; **parity law verified**: every nonzero
multiplicity has **J+I integer** (half-integer isospin forced). Lattices (2J,2I)→m:
- **2O-locked (χ_FR=triv):** {(1,1):1, (3,3):1, (3,5):1, (5,3):1, (5,5):2, (7,1):1, (7,3):1, (7,5):2}
  — the nucleon channel **(2J,2I)=(1,1)** is present at m=1.
- **2O-locked (χ_FR=sgn):** {(1,5):1, (3,3):1, (3,5):1, (5,1):1, (5,3):1, (5,5):1, (7,1):1, (7,3):1, (7,5):2}.
- **2T-restricted (representative):** {(1,1):1, (1,5):1, (3,3):2, (3,5):2, (5,1):1, (5,3):2, (5,5):3, (7,1):2, (7,3):2, (7,5):4}.

**Assignment: NEUTRAL** — the sgn-twist being invisible on the 4 (B2) means the admissibility lattice
does not privilege Assignment I vs II. (Matches the chat leg.)

## Verdict (second leg) — full agreement with the chat leg
- **B1: NOT-INDUCED-BY-OBSTRUCTION** — z = [q̃₁,q̃₂] a commutator in Γ̃ (both Pin types); all 8
  characters kill z; D2 collapse |Ñ/Γ̃|=48. The static home does not manufacture 2O; the substrate is
  relocated to the loop sector. *(CC method: cohomological/obstruction framing; chat: cocycle-attempt
  exhibited as theorem — same conclusion, independent routes.)*
- **F2:** 2O vs GL(2,3) separated by transposition-lift order; internal cover = 2O.
- **B2: ASSEMBLED-RELOCATED** — 2 lifts, sgn-twist trivial on the 4, module transport unique;
  ⟨χ,χ⟩=1, χ(z)=−4.
- **B3:** parity law J+I integer; Assignment NEUTRAL; nucleon channel present.

**Scope (carried verbatim):** conditional **R2** — the S8 ontology axes + the Pin-type ℤ/2 + the
S2/V4.50 octahedral-vs-tetrahedral representative gap are the enumerated import list; **no Gate-2a
closure**; the **dynamical selection** stays open (M.CW wall); no μ_n, no observable; distinct-4 held;
no time-reversal; §2.52 Open 3 untouched.

## Boundaries
- **Shared presentation:** independence at the code + method level on the S7 Γ/N presentation; flagged.
- **B3 admissibility lattice** is exact rep theory (R1); the *physical* reading of any channel stays
  sealed (Eddington trap 1) — I did not consult nucleon (J,I) values; the (1,1) label is the machine
  channel, not a physics claim.

**Sources (collision check):** en.wikipedia.org/wiki/Binary_octahedral_group; arXiv:0904.1876 (finite
π₁ 3-manifold cohomology); ResearchGate "Spin, Statistics and CPT for Solitons". No source derives the
locking pairing map or the flat-orbifold induced-cover for #24.
