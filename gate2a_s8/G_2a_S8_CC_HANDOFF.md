# G-2a-S8 — CC SECOND-LEG HANDOFF

**Pre-registration (locked):** `G_2a_S8_EXECUTION_PREREGISTRATION.md`
**Chat leg:** `g_2a_s8_chatleg.py` (md5 `273f4d35b661a6a101694488301af76d`) + `G_2a_S8_CHATLEG_REPORT.md`
**Rule:** reproduce every target below with YOUR OWN implementation and, where specified, a different method. Do not read the chat-leg script before your first run; use only this spec + the pre-registration. Cite your commit hash. Log every deviation verbatim before resolving it.

## Independence requirements
1. **Different representation of Spin(3):** use SU(2) complex 2×2 matrices over exact ℚ(i, √2) (or a Clifford-algebra build) instead of quaternions. If you use quaternions anyway, flag it.
2. **Own generator solves:** re-derive the normalizer elements (the 3-cycle c₃ and a 4-fold g₄) by your own affine solve over your own grid; do not copy translation parts from this spec.
3. **Own word search** for t₍₁,₁,₁₎ as a word in r₁, r₂, r₃ (any valid word; report it).
4. **Method variation encouraged** for H-A and the Hom enumeration: e.g., compute the extension class / H²(Γ₂; ℤ/2)-style obstruction or use a presentation-based section solver, rather than brute sign sweeps.
5. **Shared-presentation caveat (expected, flag it):** the Γ presentation (r₁ = (diag(1,−1,−1) | (0,0,1)), r₂ = (diag(−1,1,−1) | (1,0,0)), r₃ = (diag(−1,−1,1) | (0,1,0)); L = {all-even or all-odd integer vectors}) is the both-legs-verified S7 object. Independence is at the code+method level over this shared base, per the G-2a-S4/S7 precedent.

## Objects
Γ, L as above. N⁺ = orientation-preserving Euclidean normalizer part; T_N = ℤ³; turn-overs e_f = unit translations. Q̃ = preimage of N⁺ in Spin(3)⋉ℝ³ modulo the spin-trivial translations {(1, t) : t ∈ 2ℤ³}. z = the central (−1, 0).

## Target table (all must be reproduced exactly)

| # | Target | Value |
|---|---|---|
| T1 | r_f² = e; commutators (r_i r_j)² = pure translations giving {±2e_k} | 3 involutions; {2e-set} |
| T2 | [Γ,Γ] = 2ℤ³; Γ^ab ⊗ 𝔽₂ ≅ (ℤ/2)³ on r̄₁,r̄₂,r̄₃ | order-8 abelian exponent-2 quotient |
| T3 | class of t₍₁,₁,₁₎ in Γ^ab ⊗ 𝔽₂ | r̄₁ + r̄₂ + r̄₃ |
| T4 | **H-A:** no section Γ → Spin(3)⋉ℝ³; every lift of every deck π-rotation squares to (−1, 0), both lifts | non-split; 6/6 |
| T5 | **Positive control:** sections over T_N/2ℤ³ exist | exactly 8 (the T³ spin structures) |
| T6 | **B1:** (χ_f q_f)² for all χ ∈ Hom(Γ, ℤ/2), all f | −1, 24/24; cone-loop element order 4 |
| T7 | Structure realizations Ũ_χ on Γ̃₂ (order 16): homomorphism, Ũ_χ(z) = −Id | 8/8 |
| T8 | c₃ affine solve: translation solutions all integral; b = 0 valid | re-derives S7 even-coset slice |
| T9 | g₄ affine solve: all solutions have fractional parts (½,½,½) | re-derives S7 odd-coset shift class |
| T10 | |2O| = 48; exactly two lifts each for c₃, g₄ rotations | 48; 2; 2 |
| T11 | |Q̃| = 384; |Q| = 192; z central | 384; 192 |
| T12 | **Hom(Q, 𝔽₂):** exhaustive count | **exactly 4** |
| T13 | Restrictions to Γ (admissible structure twists) | **{(+,+,+), (−,−,−)} only** |
| T14 | Turn-over values per hom: w(E₁) = w(E₂) = w(E₃) = w(t₁₁₁) = χ₁χ₂χ₃; the two homs per χ differ only in the sgn-factor (e.g., on g₄; c₃ always +1) | table match |
| T15 | Conjugation action of N⁺ on Γ^ab ⊗ 𝔽₂ = bare permutation rep (no t₁₁₁ correction); invariant characters | {0, (1,1,1)} |
| T16 | **B2 contrast:** both lifts of every e_f are involutions in Q̃ (square = id, never z); both lifts of every deck π-rotation have square = z | 6/6 and 6/6 |
| T17 | E₁E₂E₃ = the (+1)-lift of t₍₁,₁,₁₎; per-structure composite = χ₁χ₂χ₃ · Id | 8-row table match |

## Decisive-bit branch mapping (do not re-litigate; verify)
B1 → FORCED(−1). B2 → GRADED: involution channel FORCED(+Id-square) + one global ℤ/2 choice = χ(t₁₁₁). Verdict class SPLIT. If ANY target deviates, stop, log, and report before interpretation.

## Out of scope (do not compute)
Pin/orientation-reversing sector; any μ_n or observable quantity; any identification of orbifold spinors with the framework per-strand carrier; §2.52 Open 3.
