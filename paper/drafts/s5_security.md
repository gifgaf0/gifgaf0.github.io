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
