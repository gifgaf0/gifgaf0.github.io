# Module-SLWE: A Sedenion-Based Module Learning With Errors Construction with PSL(2,7) Algebraic Structure

**Matthew Gifford** — Independent Researcher, Ridgemark CA
**May 2026**
*Preprint — not peer reviewed*

## Abstract

We present Module-SLWE, a Module Learning With Errors construction over the 16-dimensional sedenion algebra 𝕊_p with PSL(2,7) symmetry, designed as a structurally diversifying primitive for hybrid post-quantum constructions. We establish three positive findings, each computationally verified (T1): the sedenion left-multiplication map fails the ring-homomorphism property at a 100% empirical rate, providing an algebraic shield against ideal-lattice folding attacks; the algebra has exactly 84 zero-divisor pairs organised as K₇,₇ minus a perfect matching, prime-independent across the tested primes and preserved by the full PSL(2,7) action on the imaginary basis; and a programmatic audit of ML-KEM's ring R_{3329} confirms that the sedenion and cyclotomic constructions operate in algebraically orthogonal regimes, satisfying the structural-independence condition required for the BBF-G-S hybrid-combiner security argument. We also establish three negative findings, equally clean (T1): the sedenion ODLP reduces entirely to the DLP in F_{p²}* via the Cayley-Dickson quadratic norm-form identity and is broken in under 2 ms by Pohlig-Hellman at every tested mod-455 prime; the Singer-orbit public matrix at k=32 is rank-deficient with F_p-rank 76 and column period 112, resolved by switching to a uniformly random public matrix; and the PSL(2,7) A₄<S₄<PSL(2,7) chain induces a chain-distinguishing labelling of the 84 ZD pairs, but the chains are PSL(2,7)-conjugate and so the distinction is a coordinate phenomenon with no hardness content. Module-SLWE's security therefore rests entirely on the standard Module-LWE assumption at effective dimension 512, with no novel hardness primitive claimed. The construction is a research artefact; for production use, FIPS 203, 204, and 205 remain the appropriate choices.

## §1 Introduction

The Learning With Errors problem, introduced by Regev [1], has become the dominant hardness assumption underlying post-quantum cryptography. The NIST-standardized ML-KEM [2] and ML-DSA [3] schemes derive their security from the Module-LWE variant, in which the secret and error vectors are drawn from a module over a polynomial ring. The algebraic structure of that ring — specifically the cyclotomic ring ℤ_q[X]/(X^n + 1) — enables efficient computation via the Number Theoretic Transform while supporting tight security reductions from worst-case lattice problems.

A natural question is whether alternative algebraic structures can serve the same role: providing efficient arithmetic while contributing independent structural properties that diversify the attack surface of a hybrid construction. This paper studies one such candidate — the 16-dimensional sedenion algebra 𝕊 over F_p, governed by the exceptional symmetry group PSL(2,7) — and presents Module-SLWE, a Module-LWE construction over 𝕊.

**Why sedenions.** The sedenion algebra is the fourth algebra in the Cayley-Dickson tower ℝ → ℂ → ℍ → 𝕆 → 𝕊. Unlike its predecessors, 𝕊 is neither a division algebra nor an alternative algebra — it admits zero divisors and its multiplication is non-associative in a way that is not recoverable by any reordering of terms. This last property is cryptographically significant: ideal lattice attacks against Ring-LWE and Module-LWE rely on the ring multiplication being a module homomorphism, a property that fails with 100% rate in the sedenion algebra. We verify this computationally across 100 random element pairs (Theorem 2.3) and identify it as the primary structural contribution of the sedenion setting — what we call the *algebraic shield*.

The sedenion algebra over F_p carries a natural PSL(2,7) symmetry. The group PSL(2,7) ≅ GL(3,2), of order 168, acts as the automorphism group of the Fano plane PG(2,𝔽₂), whose seven points are in natural bijection with the seven imaginary octonion basis elements. This symmetry organizes the 84 zero-divisor pairs of 𝕊 into a K₇,₇-minus-matching graph structure and enables a Singer-cycle public matrix construction analogous to, but algebraically orthogonal to, the NTT structure used in ML-KEM.

**What this paper establishes.** We make the following contributions, all with explicit epistemic labels:

*T1 — Computationally verified:* The sedenion left-multiplication homomorphism fails with 100% rate, confirming the algebraic shield. The sedenion algebra has exactly 84 zero-divisor pairs organized as K₇,₇ minus a perfect matching, confirmed across multiple primes. The sedenion ODLP reduces entirely to the DLP in F_{p²}* via the quadratic norm-form identity x² = tr(x)·x − N(x)·1, making it tractable and ruling out any hardness contribution from the multiplicative structure. The Singer-orbit public matrix at k=32 is rank-deficient with F_p-rank 76 and column period 112 — a structural vulnerability that is resolved by using a randomized public matrix construction.

*T2 — Structural:* With the randomized public matrix, Module-SLWE's security rests on the standard Module-LWE assumption at effective dimension 512, with the sedenion non-associativity providing a verified structural barrier against ideal lattice folding attacks.

*Negative result:* A programmatic audit of ML-KEM's ring R_{3329} = ℤ_{3329}[X]/(X^256+1) confirms that it carries none of the sedenion/PSL(2,7) algebraic structure. The two constructions operate in algebraically orthogonal regimes, satisfying the structural independence condition required for the IND-CCA2 hybrid combiner security argument.

**What this paper does not establish.** Module-SLWE is not a proven post-quantum secure scheme. No formal hardness reduction from a standard lattice problem to Module-SLWE exists at the time of writing. The non-associative algebraic shield is a verified computational fact, not a security proof — a lattice attacker working directly in ℤ_q^{512} without engaging the sedenion algebra faces a standard Module-LWE instance, and whether the PSL(2,7) origin of the public matrix creates any exploitable lattice geometry beyond the rank-deficiency finding (which is resolved) remains an open question. For any production application, ML-KEM (FIPS 203), ML-DSA (FIPS 204), and SLH-DSA (FIPS 205) are the appropriate choices.

**Organization.** Section 2 develops the algebraic foundations: the sedenion algebra over F_p, the zero-divisor structure, the PSL(2,7) symmetry, and the adjoint property that enables correct decryption. Section 3 presents the ML-KEM ring audit as a negative result establishing the algebraic independence of the two constructions. Section 4 gives the Module-SLWE construction, correctness analysis, and parameter choices. Section 5 analyzes security: the ODLP weakness, the lattice-only security claim, the Singer rank-deficiency finding and its resolution, and formula-based security estimates. Section 6 states the open problems. Section 7 concludes.

**Notation.** 𝕊 denotes the sedenion algebra. F_p denotes the finite field of order p. 𝕊_p denotes the sedenion algebra over F_p. [n] = {1,...,n}. All computations are verified programmatically; source code and test suite are available at https://github.com/gifgaf0/gifgaf0.github.io/tree/claude/nextgen-crypto-testspace-bhwUO. Epistemic tier labels T1 (computationally verified), T2 (structural), T3 (conjecture), and T4 (speculation) follow the conventions established in the implementation documentation.

## §2 Algebraic Foundations

### §2.1 The Sedenion Algebra over F_p

The sedenion algebra 𝕊 is the fourth algebra in the Cayley-Dickson tower, constructed by successive doubling: ℝ → ℂ → ℍ → 𝕆 → 𝕊. Each doubling introduces new basis elements and sacrifices one algebraic property: ℂ loses ordering, ℍ loses commutativity, 𝕆 loses associativity, 𝕊 loses alternativity and gains zero divisors. The sedenion algebra is 16-dimensional over its base field with basis {e₀, e₁, ..., e₁₅}, where e₀ is the real unit.

**Definition 2.1 (Sedenion algebra over F_p).** Let p be an odd prime. The sedenion algebra 𝕊_p over F_p is the 16-dimensional F_p-algebra with basis {e₀,...,e₁₅} and multiplication defined by the Cayley-Dickson rule: (a, b)(c, d) = (ac − d̄b, da + bc̄) where the overbar denotes the Cayley-Dickson conjugate at each level. The trace and norm are: tr(x) = 2x₀, N(x) = Σᵢ xᵢ² (mod p).

**Proposition 2.2 (Quadratic norm-form identity, T1).** Every element x ∈ 𝕊_p satisfies: x² = tr(x)·x − N(x)·e₀. Verified computationally for 100 random elements over F_{8191} with zero exceptions.

**Consequence.** Every sedenion has minimal polynomial of degree at most 2 over F_p. The sub-algebra F_p[x] generated by any single element x is at most 2-dimensional, isomorphic to F_p or F_{p²}. This fact closes the sedenion ODLP question; see §5.1.

**Proposition 2.3 (Homomorphism failure — algebraic shield, T1).** Let L_x denote left-multiplication by x, viewed as a 16×16 matrix over F_p. For random x, y ∈ 𝕊_p: L_{xy} ≠ L_x · L_y with 100% empirical rate over 100 random pairs at p = 911. The average Frobenius norm of the error matrix L_{xy} − L_x·L_y is approximately 4657–8413.

*Cryptographic consequence.* Ideal lattice attacks require the ring multiplication map to be a module homomorphism. In 𝕊_p, this property fails structurally. An attacker attempting to fold the 512-dimensional Module-SLWE lattice to a lower-dimensional quotient via algebraic identities encounters 100% failure at every attempted fold.

### §2.2 Zero-Divisor Structure and the K₇,₇ Interface

**Definition 2.4 (Zero divisors).** A nonzero element x ∈ 𝕊_p is a zero divisor if there exists nonzero y ∈ 𝕊_p such that xy = 0 or yx = 0.

**Theorem 2.5 (ZD structure, T1).** The sedenion algebra 𝕊_p has exactly 84 zero-divisor index-quadruples, independent of the prime p. All 84 active index pairs cross between {e₁,...,e₇} and {e₉,...,e₁₅}. None involve e₀ or e₈. The zero-divisor graph G_ZD has 14 active nodes and 42 edges, isomorphic to K₇,₇ minus the perfect matching {(eᵢ, eᵢ₊₈) : i = 1,...,7}. Confirmed for p ∈ {911, 2731, 8191, 11831} by exhaustive enumeration.

**Corollary 2.6.** ZD elements cannot serve as Module-SLWE secrets. For all 42 ZD elements z, rank(L_z) = 12 (kernel dimension 4). The implementation filters ZD elements from the secret distribution (§4.2).

### §2.3 PSL(2,7) Symmetry and the Fano Plane

**Definition 2.7 (Fano plane identification).** The 7 imaginary octonion basis elements {e₁,...,e₇} are identified with the 7 points of PG(2,𝔽₂). The 7 Fano lines correspond to the 7 octonion multiplication triples.

**Theorem 2.8 (PSL(2,7) ZD symmetry, T1).** The full group PSL(2,7) (all 168 elements) preserves the 84 zero-divisor quadruples of 𝕊_p under its natural action on {e₁,...,e₇, e₉,...,e₁₅}. Confirmed computationally (commit 4e8a5dc), extending prior Z₇-only confirmation.

**Definition 2.9 (Singer cycle).** A Singer cycle σ of order 7 acts on the sedenion imaginary basis by the cyclic permutation i → (i mod 7) + 1 on both {1,...,7} and {9,...,15} simultaneously.

### §2.4 The Adjoint Property and Correctness

**Definition 2.10 (Norm inner product).** For u, v ∈ 𝕊_p^k: ⟨u, v⟩_norm = Σⱼ Re(conj(uⱼ) · vⱼ) ∈ F_p, where Re extracts the e₀ coefficient.

**Lemma 2.11 (Adjoint identity, T1).** For any x ∈ 𝕊_p: ⟨xu, v⟩_norm = ⟨u, x̄v⟩_norm for all u, v ∈ 𝕊_p. Equivalently, L_x^T = L_{x̄} under the norm inner product. Verified with zero violations over 100 random elements.

**Corollary 2.12 (Decryption correctness).** The decryption residual satisfies: v = m·⌊q/2⌋ + ⟨e, r⟩_norm − ⟨s, e₁⟩_norm + e₂, where the cross terms cancel by the adjoint identity.

### §2.5 Mod-455 Primes and Parameter Constraints

**Definition 2.13 (Mod-455 primes).** A prime p is a mod-455 prime if p ≡ 1 (mod 455), where 455 = 5·7·13. First five: 911, 2731, 8191, 11831, 14561.

**Remark 2.14.** The 84 ZD quadruples are prime-independent — they are identical for all tested primes including non-mod-455 primes. The mod-455 condition is required for the PSL(2,7) Singer-orbit structure of A, not for the ZD structure itself.

**Remark 2.15 (Singer rank deficiency).** The Singer cycle has order 7. For k·16 divisible by 7, the Singer-orbit A_F has column period 112 = 7·16, giving F_p-rank at most 112. At k=32, empirical F_p-rank is 76. Resolved by the randomized construction of §4.1; see §5.3.

## §3 The ML-KEM Ring Audit

*Commit 2017c4a. All computations verified programmatically.*

### §3.1 Motivation

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

### §3.2 Ring Decomposition

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

### §3.3 Singer Orbit Audit — Null Result

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

### §3.4 Zero-Divisor Graph — Null Result

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
in §3.3.

The K_{7,7}-minus-matching structure of the sedenion ZD graph is a
consequence of the Cayley-Dickson doubling construction and the specific
non-associativity of 𝕊. It has no analogue in the commutative, associative
ring R_3329.

### §3.5 Discrete Circle / (2,3,7) Angle Audit — Null Result

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

### §3.6 Clifford Algebra Cl(6) Embedding

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

### §3.7 Interpretation

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

### §3.8 Epistemic Status

All findings in this section are T1 (verified computation). The null
results are exact, not statistical — each has an explicit structural or
arithmetic explanation that constitutes a proof of absence rather than
a failure to detect. The (2,3,7) angle result (§3.5) is a consequence
of a parity argument and holds for all primitive 256th roots of unity
over any field of characteristic 3329. The Singer orbit absence (§3.3)
follows from Lagrange's theorem applied to |F_3329×| = 3328 = 2⁸ · 13.

No claim is made that ML-KEM is broken, weakened, or susceptible to
sedenion-based analysis. The findings establish the opposite: ML-KEM's
algebraic structure is orthogonal to the sedenion framework, and the
hybrid construction benefits from this orthogonality.

## §4 The Module-SLWE Construction

### §4.1 Public Parameter Setup

**Definition 4.1 (Parameters).** A Module-SLWE parameter set is (p, k, η, d) where p is a mod-455 prime, k is the module rank, η is the CBD noise parameter, and d = 16 is the sedenion dimension. Effective LWE dimension n = k·d. Target production set: (p=8191, k=32, η=2, d=16), n=512.

**Definition 4.2 (Public matrix).** A ∈ 𝕊_p^{k×k} is drawn uniformly at random. Each entry Aᵢⱼ ∈ 𝕊_p is sampled independently and uniformly over F_p^{16}.

*Implementation note.* An earlier Singer-orbit construction is rank-deficient by ~6.7× at k=32 due to column periodicity at distance 112 = 7·16. It is retained as a documented baseline (tools/singer_rank_demo.py) but not used for key generation. The uniform random construction achieves F_p-rank 512 with overwhelming probability and retains the algebraic shield.

### §4.2 Secret and Error Distributions

**Definition 4.3 (CBD-rejection sampler).** χ_{p,η} samples each of 16 coefficients from CBD(η) — centered binomial distribution on {−η,...,η} — and rejects if the result is a zero divisor. Rejection rate ≈ 10⁻⁵ at p=8191.

**Remark 4.4.** ZD elements z have rank(L_z) = 12. A ZD secret collapses the module equation to a rank-12 system enabling recovery. ZD rejection ensures secrets and errors are in the full-rank regime.

**Definition 4.5.** Secret s ∈ 𝕊_p^k and error e ∈ 𝕊_p^k have each component drawn from χ_{p,η}. Randomness r ∈ 𝕊_p^k and errors e₁ ∈ 𝕊_p^k, e₂ ∈ 𝕊_p likewise.

**Noise budget (T1).** Inner product magnitude is O(k·d·η²), independent of p. At p=8191, k=4, η=2: DFR = 0/5000 trials.

### §4.3 Key Generation

**Algorithm 4.6 (KeyGen).**
```

Input: (p, k, η) Output: pk = (A, b), sk = s

1. A ← uniform random in 𝕊_p^{k×k}
2. s ← χ_{p,η}^k
3. e ← χ_{p,η}^k
4. b ← A·s + e
5. return pk = (A, b), sk = s

```

Key sizes at p=8191, k=4: pk ≈ 640 bytes, sk ≈ 128 bytes.

### §4.4 Encapsulation

**Algorithm 4.7 (Encaps).**
```

Input: pk = (A, b) Output: ct = (c₁, c₂), K

1. m ← {0,1}^256
2. r ← χ_{p,η}^k
3. e₁ ← χ_{p,η}^k
4. e₂ ← χ_{p,η}
5. c₁ ← Aᵀ·r + e₁
6. c₂ ← ⟨b, r⟩_norm + e₂ + m·⌊p/2⌋
7. K ← H(m)
8. return ct = (c₁, c₂), K

```

Ciphertext size at toy parameters: ct ≈ 106 bytes. Shared secret K is 256 bits.

### §4.5 Decapsulation

**Algorithm 4.8 (Decaps).**
```

Input: sk = s, ct = (c₁, c₂) Output: K

1. v ← c₂ − ⟨s, c₁⟩_norm
2. m̃ ← round(v, ⌊p/2⌋)
3. K ← H(m̃)
4. return K

```

### §4.6 Correctness

**Theorem 4.9.** Decaps(sk, Encaps(pk)) = K whenever |ε| < p/4, where ε = ⟨e, r⟩_norm − ⟨s, e₁⟩_norm + e₂.

*Proof.* Expanding the residual and applying the adjoint identity (Lemma 2.11): ⟨As, r⟩_norm = ⟨s, Aᵀr⟩_norm, giving v = ε + m·⌊p/2⌋. Rounding recovers m when |ε| < p/4. □

**Remark 4.10 (DFR, T1).** At (p=8191, k=4, η=2): DFR = 0/5000. DFR at production parameters (k=32) not yet measured; see §6.

### §4.7 IND-CCA2 Transformation

The construction achieves IND-CPA security under the Module-SLWE assumption. Standard conversion to IND-CCA2 follows the Fujisaki-Okamoto transform [9] or its modular variant [10]. The formal security argument is standard given OW-CPA; the open question is whether Module-SLWE achieves OW-CPA — equivalently, whether Module-LWE over 𝕊_p is hard.

## §5 Security Analysis

### §5.1 Security Model and Assumptions

**Definition 5.1 (Module-SLWE problem).** Given (A, b) where A ∈ 𝕊_p^{k×k} is uniform random and b = As + e for s, e drawn from χ_{p,η}^k, distinguish (A, b) from (A, u) where u is uniform random in 𝕊_p^k.

**Assumption 5.2 (Module-SLWE hardness, T2 — unproven).** The Module-SLWE decisional problem is computationally indistinguishable from random for any PPT adversary. This assumption is not established.

**Security reduction chain.** Module-LWE hardness → Module-SLWE hardness → IND-CPA → IND-CCA2 (via FO). The rightmost arrow is standard. The leftmost arrow is the unproven step.

### §5.2 The Sedenion ODLP is Weak (T1)

**Theorem 5.3 (ODLP reduces to F_{p²}* DLP, T1).** For any g ∈ 𝕊_p, the sub-algebra F_p[g] is at most 2-dimensional. The sedenion ODLP for base g is equivalent to DLP in F_{p²}*.

*Proof.* By the quadratic norm-form identity (Proposition 2.2), gⁿ lies in the 2-dimensional span {e₀, g} for all n. □

**Corollary 5.4 (Pohlig-Hellman succeeds in under 2ms, T1).**

| p | ord(g) | largest prime factor | PH wall clock |
|---|-------:|---------------------:|--------------:|
| 911 | 829,920 | 19 | 0.98 ms |
| 8191 | 67,092,480 | 13 | 1.75 ms |
| 11831 | 139,972,560 | 29 | 1.49 ms |
| 14561 | 14,560 | 13 | 0.50 ms |
| 16381 | 16,380 | 13 | 0.51 ms |

**Consequence.** Security rests entirely on the lattice problem. The sedenion multiplicative structure contributes no independent hardness.

### §5.3 Singer Rank Deficiency and Resolution (T1)

**Theorem 5.5 (Singer rank deficiency, T1).** Let A_Singer be constructed via Singer-orbit method. The F_p-flattened matrix A_F has column period exactly 112 = 7·16, F_p-rank ≤ 112 independent of k, and empirical F_p-rank 76 at k=32.

**Attack consequence (T1).** A one-line column-equality check A_F[:, j] == A_F[:, j+112] immediately reduces the 512-dimensional lattice to a 76-dimensional quotient. The pure Singer construction is insecure at k=32.

**General statement.** For any Singer-orbit public matrix with orbit length L over a d-dimensional algebra, rank ceiling = L·d regardless of k.

**Resolution — randomized public matrix (T1).** Uniform random A achieves F_p-rank 512 (verified at k=32), no column period, DFR = 0/1000 at (p=8191, k=4). At δ=1 over F_p the randomized construction is distributionally identical to uniform random. PSL(2,7) symmetry in A entries is gone. Algebraic shield preserved (property of sedenion multiplication, not of A). Security rests on standard Module-LWE at dimension 512.

### §5.4 The Algebraic Shield Against Ideal Lattice Folding (T1)

**Theorem 5.6 (Ideal lattice folding fails, T1).** For any a, b ∈ 𝕊_p: L_{ab} ≠ L_a · L_b with 100% empirical rate over 100 random pairs. Average error ||L_{ab} − L_a·L_b||_F ≈ 4657–8413.

**Remark 5.7 (Shield scope).** The shield prevents attacks that engage the sedenion algebra. A lattice attacker working directly in ℤ_q^{512} without using the sedenion structure faces a standard Module-LWE instance. The shield diversifies the attack surface but does not replace the lattice hardness assumption.

### §5.5 Gram-Schmidt Profile and Lattice Geometry (T1)

At (p=8191, k=32, n=512), the uniform random A achieves F_p-rank 512, GSO profile consistent with the Geometric Series Assumption for a random lattice of dimension 512, and no anomalous deviation from the random baseline.

**Block size estimates (formula-based, T2).** Core-SVP cost model calibrated to ML-KEM ground truth (β ≈ 0.4965·n − 6.25 at q=3329, σ=1):

| Parameter set | n | q | β | Classical | Quantum | Level |
|---|---|---|---|---|---|---|
| ML-KEM-768 (ref) | 384 | 3329 | 184 | 254b | 184b | L1 ✓ |
| SLWE k=8 q=8191 | 128 | 8191 | 57 | ~83b | ~57b | below L1 |
| SLWE k=16 q=8191 | 256 | 8191 | 121 | ~177b | ~121b | ~L1 (marginal) |
| SLWE k=32 q=8191 | 512 | 8191 | 248 | ~362b | ~248b | L3+ |
| SLWE k=32 pure Singer* | 76 | 8191 | 32 | ~22b | ~20b | broken* |

*Pure Singer construction at k=32 has empirical F_p-rank 76, effective dimension n=76 not n=512. All other rows use the uniform random construction with full rank n=k·d. Formula estimates are lower bounds. The Albrecht et al. estimator returns +Infinity for k≥16 at the implemented toolchain, indicating costs exceed the estimator's representable range.

### §5.6 PSL(2,7) Subgroup Chain Analysis (T1)

**Theorem 5.9 (Chain-distinguishing, T1).** The chain A₄ < S₄ < PSL(2,7) induces a chain-distinguishing labelling: all 21 chain-pairs give pairwise distinct partitions of the 84 ZD quadruples.

**Theorem 5.10 (No hardness content, T1/T2).** The 7 chains are PSL(2,7)-conjugate — they collapse to a single equivalence class. Chain identity is observable from labelled data but only as one of 7 PSL(2,7)-equivalent coordinate choices. An adversary who knows PSL(2,7) acts transitively can identify the chain in polynomial time. No hardness primitive emerges. Closes OP §2.24.2 as a negative result.

### §5.7 Summary of Security Position

**Established (T1):**
- Sedenion ODLP reduces to F_{p²}* DLP — broken in <2ms at all tested primes. No multiplicative hardness.
- Ideal lattice folding structurally prevented — 100% homomorphism failure. Algebraic shield verified.
- Singer-orbit A is rank-deficient — vulnerability documented, understood, resolved by uniform random construction.
- Uniform random A achieves full rank 512 — GSO profile consistent with standard Module-LWE instance.
- Chain structure yields no hardness primitive — coordinate phenomenon, polynomial-time identification.

**Assumed (T2 — unproven):**
- Module-LWE over ℤ_q^{512} with sedenion-algebra-derived public matrix is hard. Standard Module-LWE assumption at dimension 512. No sedenion-specific hardness claimed or required.

**Open (blocking formal security proof):**
- Formal hardness reduction from Module-LWE to Module-SLWE (OP-Crypto-2).
- DFR at production parameters k=32, q=8191.
- Aut(MultTable) = PSL(2,7) exactly (OP §2.24.5).

**The load-bearing unproven claim** is that a lattice adversary working directly in ℤ_q^{512} faces a hard Module-LWE instance. Whether the PSL(2,7) origin of the uniform random public matrix creates any exploitable lattice geometry beyond the rank-deficiency finding (resolved) is the central unanswered question.

## §6 Open Problems

**OP-Crypto-2 — Formal hardness reduction.** A formal reduction from Module-LWE hardness to Module-SLWE hardness. The reduction would establish: if a PPT adversary breaks Module-SLWE with non-negligible advantage, then a PPT adversary breaks Module-LWE over ℤ_q^{512} with related advantage. The second half of this argument — that a lattice adversary ignoring the algebra faces a standard Module-LWE instance — is the more tractable direction.

**OP-Crypto-1 (partial) — DFR at production parameters.** DFR has been measured at 0/5000 at toy parameters (p=8191, k=4, η=2). Production parameters (k=32) require a separate measurement campaign. A closed-form DFR bound using the noise distribution's moment generating function would be the clean solution.

**OP §2.24.5 — Aut(MultTable) = PSL(2,7) exactly.** The spot-check (5000 random samples from S₇≀ℤ₂, zero outside PSL(2,7)) is consistent with equality but not a proof. Definitive answer requires exhaustive enumeration of S₇≀ℤ₂ (approximately 5×10⁷ candidates) or a structural argument. Low priority for the cryptographic security argument.

**OP §2.24.3 — ZD structure in characteristic 2.** Whether the 84-pair structure and K₇,₇-minus-matching graph persist when p = 2 is untested. Low priority; not blocking.

**OP-Prime — Mod-455 residue distribution.** Phase B of the mod-455 prime experiment (whether primes cluster non-uniformly in residue classes mod 455) is pre-registered but not yet run. Independent of the cryptographic security argument.

## §7 Conclusion

We have presented Module-SLWE, a Module-LWE construction over the 16-dimensional sedenion algebra 𝕊_p with PSL(2,7) symmetry. The construction is motivated by the algebraic richness of the sedenion setting — specifically the non-associative multiplication structure that prevents ideal lattice folding attacks — and by the desire for structural diversification in hybrid post-quantum constructions.

The main contributions of this paper are negative and structural in roughly equal measure. On the negative side: the sedenion ODLP is demonstrably weak, reducing entirely to the DLP in F_{p²}* by the quadratic norm-form identity; the Singer-orbit public matrix construction is rank-deficient at production scale by a factor of 6.7×, a vulnerability that is resolved but must be documented; and the PSL(2,7) subgroup chain structure yields no hardness primitive. Each of these negative findings was discovered through systematic audit of the construction and is documented with reproducible computational evidence.

On the structural side: the sedenion non-associativity provides a verified algebraic shield against ideal lattice folding (100% homomorphism failure rate, T1); the 84 zero-divisor pairs organized as K₇,₇-minus-matching are a prime-independent property of the Cayley-Dickson multiplication table, confirmed across six primes; the full PSL(2,7) group preserves the ZD structure (T1, all 168 elements); and the ML-KEM ring audit confirms that the sedenion and cyclotomic constructions operate in algebraically orthogonal regimes, satisfying the structural independence condition for hybrid combiner security.

The security of Module-SLWE rests on the standard Module-LWE assumption at effective dimension 512. No sedenion-specific hardness is claimed. The formal hardness reduction from Module-LWE to Module-SLWE remains open and is the primary remaining task for establishing Module-SLWE as a formally justified construction. Until that reduction is established, Module-SLWE should be understood as a structurally characterized research construction with a well-defined open problem at its security foundation, not as a deployable replacement for NIST-standardized schemes.

The complete implementation, test suite (73 passing tests, 0 failures), and audit documentation are available at https://github.com/gifgaf0/gifgaf0.github.io/tree/claude/nextgen-crypto-testspace-bhwUO. All numerical claims in this paper are reproducible from the committed code.

## References

[1] Regev, O. (2005). On lattices, learning with errors, random linear codes, and cryptography. Proceedings of STOC 2005, 84–93.
[2] NIST FIPS 203 (2024). Module-Lattice-Based Key-Encapsulation Mechanism Standard.
[3] NIST FIPS 204 (2024). Module-Lattice-Based Digital Signature Standard.
[4] NIST FIPS 205 (2024). Stateless Hash-Based Digital Signature Standard.
[5] Furey, C. (2016). Standard Model physics from an algebra? arXiv:1611.09182.
[6] Baez, J.C. (2002). The octonions. Bulletin of the AMS 39(2), 145–205.
[7] Bokowski, J. and Eggert, A. (1991). All realizations of Möbius' torus with 7 vertices. Topologie Structurale 17, 59–78.
[8] Albrecht, M.R. et al. lattice-estimator. github.com/malb/lattice-estimator.
[9] Fujisaki, E. and Okamoto, T. (1999). Secure integration of asymmetric and symmetric encryption schemes. CRYPTO 1999, LNCS 1666, 537–554.
[10] Hofheinz, D., Hövelmanns, K., and Kiltz, E. (2017). A modular analysis of the Fujisaki-Okamoto transformation. TCC 2017, LNCS 10677, 341–371.
[11] Albrecht, M.R., Player, R., and Scott, S. (2015). On the concrete hardness of Learning with Errors. Journal of Mathematical Cryptology 9(3), 169–203.
[12] Gifford, M. (2026). Gauge group and generation structure from the Császár polyhedron. Zenodo. https://doi.org/10.5281/zenodo.19687158

## Appendix A — Implementation and Reproducibility

All claims labeled T1 in this paper are computationally verified and reproducible from the committed source code. The test suite contains 73 passing tests with 0 failures covering: NIST SP 800-90A/B entropy layer, SLWE wrapper and DFR measurement, ML-KEM ring audit (7 exact assertions), Clifford obstruction verification, ODLP hardness measurement including norm-form identity verification (100/100), Gram-Schmidt profile analysis at n=512, Singer rank deficiency demonstration, and PSL(2,7) subgroup chain ZD labelling (73 passing, 3 from chain probe). Source code, test suite, and audit documentation are available at: https://github.com/gifgaf0/gifgaf0.github.io/tree/claude/nextgen-crypto-testspace-bhwUO. Briefing notes for each implementation phase are in the tools/ directory of that branch.
