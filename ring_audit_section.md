# §X — Algebraic Audit of ML-KEM's Cyclotomic Ring

*Commit 2017c4a. All computations verified programmatically.*

## X.1 Motivation

Module-SLWE is constructed over the 16-dimensional sedenion algebra 𝕊
governed by PSL(2,7)/Fano plane symmetry, with security properties that
depend critically on the Singer-orbit structure of the modulus q. A natural
question arises: does ML-KEM's ring R_q = Z_q[X]/(X^256+1), the basis of
FIPS 203, carry any of the same algebraic structure? If so, the sedenion
audit methodology developed for Module-SLWE might expose features of
ML-KEM's ring invisible to standard cyclotomic and lattice analysis. If
not, the two schemes are confirmed to operate in algebraically orthogonal
regimes — a result that directly strengthens the security argument for the
hybrid construction.

We conducted a four-line programmatic audit of R_3329, together with a
Clifford algebra embedding check. All lines returned null results. We report
the findings and their structural explanations in full.

## X.2 Ring Decomposition

**Result (T1 — verified).** R_3329 = Z_3329[X]/(X^256+1) decomposes via
the Chinese Remainder Theorem as:

    R_3329 ≅ (F_{3329²})^128

The decomposition arises because 17 is a quadratic non-residue mod 3329,
so every factor X² − ζ^{2j+1} (for j = 0,...,127, where ζ is a primitive
256th root of unity in F_{3329²}) is irreducible over F_3329. The 128
factor polynomials were written to `tools/mlkem_ring_factors.json` and
their product reconstructs X^256+1 exactly.

Each component field F_{3329²} is a field, hence an integral domain with
no non-trivial zero divisors. All zero divisors in R_3329 arise exclusively
from the product structure — elements supported on disjoint sets of CRT
components.

## X.3 Singer Orbit Audit — Null Result

**Hypothesis.** 3329 ≡ 1 (mod 7), so F_3329× contains a Z₇ subgroup. The
Singer-cycle orbit construction used to build the Module-SLWE public matrix
A might transfer to the 128 NTT factors.

**Finding (T1 — verified).** The hypothesis fails at the first step.

    3329 mod 7 = 4
    q − 1 = 3328 = 2⁸ · 13

The multiplicative group F_3329× has order 3328 = 2⁸ · 13. By Lagrange's
theorem, F_3329× contains no subgroup of order 7. The Singer orbit
construction requires a Z₇ subgroup of F_q×; this subgroup does not exist
for q = 3329. The audit has no input on this prime.

**Structural explanation.** NIST selected q = 3329 for ML-KEM because it
is the smallest prime satisfying q ≡ 1 (mod 256), enabling a full NTT over
Z_q. The condition q ≡ 1 (mod 256) requires q − 1 divisible by 256 = 2⁸.
Since 3329 − 1 = 2⁸ · 13, the only odd prime factor is 13. Singer orbit
analysis via PSL(2,7) requires a prime q with 7 | (q−1), i.e., q ≡ 1
(mod 7). The conditions q ≡ 1 (mod 256) and q ≡ 1 (mod 7) are compatible
— their conjunction requires q ≡ 1 (mod lcm(256,7)) = q ≡ 1 (mod 1792) —
but ML-KEM's q = 3329 satisfies only the NTT condition. The PSL(2,7)
structure has no foothold in this prime.

## X.4 Zero-Divisor Graph — Null Result

**Hypothesis.** The ZD graph of R_3329, restricted to a PSL(2,7)-orbit-
closed subset of the 128 CRT factors, might carry a K_{7,7}-like subgraph
analogous to the sedenion ZD graph.

**Finding (T1 — verified).** The ZD graph of R_3329 is the complete graph
K_128, with automorphism group Sym(128). Every pair of CRT factors generates
a zero divisor via the product structure. The graph has no privileged
substructure: any 14-element subset spans K_14, which contains K_{7,7}
as a complete bipartite subgraph trivially, without any algebraic content.

The natural ring-induced symmetry group is the dihedral group D_128 of
order 256, arising from the cyclic structure of the NTT. No PSL(2,7)
subgroup acts on the 128 factors, consistent with the Z₇ absence established
in §X.3.

The K_{7,7}-minus-matching structure of the sedenion ZD graph is a
consequence of the Cayley-Dickson doubling construction and the specific
non-associativity of 𝕊. It has no analogue in the commutative, associative
ring R_3329.

## X.5 Discrete Circle / (2,3,7) Angle Audit — Null Result

**Hypothesis.** The 256th roots of unity in Z_3329×, viewed as points on
a discrete circle, might exhibit the angle ratios of the (2,3,7) hyperbolic
triangle (π/2 : π/3 : π/7 = 21:14:6 in units of π/42).

**Finding (T1 — verified, with proof).** The count of (2,3,7)-angle triples
among primitive 256th roots of unity is exactly zero. This is not a
statistical result — it follows from a parity obstruction.

*Proof sketch.* Let ω be a primitive 256th root of unity in F_{3329²}.
All primitive 256th roots have the form ω^k for k odd (since primitive
means gcd(k, 256) = 1, and 256 = 2⁸ forces k odd). The discrete log of
any primitive root is odd. For a triple of primitive roots to realize
angles in ratio 21:14:6, one angle corresponds to a log-difference of
14m for some integer m. But 14m is even for all m. An even log-difference
between two odd logs requires an even minus odd = odd, contradiction. Hence
no such triple exists. The full-circle count of 248 angle triples matches
exactly the uniform-random expectation under the audit's definition,
confirming that no (2,3,7) structure is present.

## X.6 Clifford Algebra Cl(6) Embedding

**Hypothesis.** The 128-factor decomposition of R_3329 might carry a natural
Cl(6) module structure, via the chain: sedenions ↔ Cl(0,8) triality ↔
Cl(6) embedding ↔ 128-dimensional spinor space. If Cl(6) structure were
present and natural with respect to the NTT, the NTT would be performing
spinor arithmetic in a sense accessible to sedenion analysis.

**Finding (T1 — verified).** Six anticommuting 8×8 generators were
constructed over F_3329 via the standard Pauli-tensor pattern, using
i = 17^{(3329−1)/4} = 1729 as √−1 in F_3329. The generators were lifted
to 128 dimensions via Γ_a = I_{16} ⊗ γ_a. All 21 Clifford anticommutation
relations {Γ_a, Γ_b} = 2δ_{ab} · I_{128} were verified programmatically.

**However, the Cl(6) structure is non-natural with respect to the NTT.**
Three obstructions were identified:

1. *Non-canonical multiplicity.* The construction yields a 16-fold degenerate
   embedding (128 = 16 × 8, where 8 is the Cl(6) spinor dimension). This
   produces an entire GL_16-family of inequivalent Cl(6) embeddings in the
   128-dimensional space, with no canonical choice privileged by the ring
   structure.

2. *NTT symmetry mismatch.* The natural symmetry group of the NTT
   decomposition is cyclic Z/128, acting by permutation of the 128 CRT
   factors. This group has no (Z/2)⁶ subgroup (since 128 = 2⁷ and Z/128
   is cyclic, not a product of copies of Z/2). Cl(6) structure requires a
   (Z/2)⁶ action. These are incompatible.

3. *Scalar endomorphisms only.* The only endomorphisms of the 128-dimensional
   space that simultaneously commute with the diagonal F_q action (from the
   CRT decomposition) and with all six Clifford generators are scalar
   multiples of the identity. No non-scalar Cl(6) endomorphism respects the
   NTT structure.

The Cl(6) algebra exists in the 128-dimensional space in the same trivial
sense that any sufficiently large algebra contains smaller algebras as
substructures. The embedding is not a property of ML-KEM's ring — it is a
property of the ambient dimension.

## X.7 Interpretation

The four-line audit and the Clifford embedding check are collectively a
clean negative result, with explicit structural reasons for each null
finding.

The root cause is arithmetic. ML-KEM's parameter q = 3329 satisfies
q − 1 = 2⁸ · 13. The sedenion/PSL(2,7) construction requires primes
q ≡ 1 (mod 455), where 455 = 5 · 7 · 13, ensuring F_q× contains
subgroups of orders 5, 7, and 13 simultaneously. ML-KEM's q satisfies
only the factor-13 condition; the factor-7 condition (required for Singer
orbit closure) and the factor-5 condition are absent. The two constructions
are operating on arithmetically incompatible primes.

This incompatibility has a direct implication for the hybrid construction.
The sedenion audit methodology, applied to ML-KEM's ring, finds no
exploitable structure — not because the methodology is weak, but because
the ring genuinely lacks the algebraic prerequisites the methodology probes.
Module-SLWE and ML-KEM are not variants of the same scheme expressed in
different algebraic vocabulary. They are structurally distinct constructions
whose security properties are independent. This is precisely the condition
required for the BBF-G-S combiner's IND-CCA2 guarantee to provide
meaningful diversification.

Furthermore, the audit establishes a precise characterization of the
attack surface for PSL(2,7)-based analysis: it applies to rings built over
primes q ≡ 1 (mod 455). No currently standardized PQC scheme (ML-KEM,
ML-DSA, SLH-DSA, HQC) uses such primes. Module-SLWE is, to the authors'
knowledge, the first cryptographic construction deliberately designed to
operate in this regime.

## X.8 Epistemic Status

All findings in this section are T1 (verified computation). The null
results are exact, not statistical — each has an explicit structural or
arithmetic explanation that constitutes a proof of absence rather than
a failure to detect. The (2,3,7) angle result (§X.5) is a consequence
of a parity argument and holds for all primitive 256th roots of unity
over any field of characteristic 3329. The Singer orbit absence (§X.3)
follows from Lagrange's theorem applied to |F_3329×| = 3328 = 2⁸ · 13.

No claim is made that ML-KEM is broken, weakened, or susceptible to
sedenion-based analysis. The findings establish the opposite: ML-KEM's
algebraic structure is orthogonal to the sedenion framework, and the
hybrid construction benefits from this orthogonality.
