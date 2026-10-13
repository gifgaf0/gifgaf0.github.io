# Fluid Lattice Topology: Bridging PSL(2,7) Vacuum Geometry and Non-Associative Post-Quantum Cryptography

**Matthew Gifford** — Independent Researcher, Ridgemark, CA
**Version 2** (corrected) — May 2026

> *Suggested alternative title, more aligned with the corrected claims:*
> *"Sedenion Module-LWE and a Geometric Conjecture for the Proton Radius." Author's call; not load-bearing.*

---

## Version note (v2)

This version corrects a **material error in the cryptographic security claim** of v1 and tightens the framing of the physics section. The errors are stated plainly here rather than silently revised.

**Cryptography.** v1 claimed NIST Category 5 quantum security at N = 512, q ≈ 2³², β ≈ 247. **This was wrong.** A primal-uSVP attack on the flat 512-dimensional lattice at those parameters succeeds at block size β ≈ 80–110 — roughly 2³³ classical Core-SVP cost / 2⁶² classical gates — which is **below NIST Category 1**. The β ≈ 247 figure corresponds to a ≈ 2¹⁶ modulus, not the 2³² of the printed parameters; at fixed noise, a *larger* modulus lowers the noise rate σ/q and *reduces* lattice security. v2 corrects the parameters (k = 64, q = 911) and the methodology (primal-uSVP via the CN11 BKZ simulator, calibrated against ML-KEM), and restates the role of non-associativity as *removing the ideal-lattice attack class* (reduction to generic lattice hardness) rather than as additional quantified hardness.

**Physics.** v2 removes the claim that the order-7 cone bound "establishes a hard geometric lower bound on rₚ" (the bound 0.091 fm is exceeded by the measured radius by a factor of ~9 and constrains nothing near the physical value), updates the motivation to reflect the now largely resolved status of the proton-radius discrepancy, and states clearly that the boundary term and the 4λ̄ₚ relationship remain **contingent on the unproven bound R = 4r**. Several quantities in the fc relationship require an explicit convention that is not yet supplied; these are flagged in §III.A and the associated table is relabeled a *contingent illustration*, not a verification.

---

## Abstract

We study a single mathematical object — the 16-dimensional sedenion algebra **S** governed by the PSL(2,7) symmetry of the Fano plane and embedded in the hyperbolic P¹(2,3,7) orbifold — and examine how its structure bears on two unrelated problems, stating results at explicit epistemic tiers and isolating the load-bearing open problem in each.

In **physics**, modeling the proton as a Borromean configuration resolving the P¹(2,3,7) cone singularity yields a structural relationship between the fine-structure constant and the proton radius, fc = 1 + 2rₚ²φ⁻⁴/16π, in which the constants other than rₚ admit candidate geometric addresses. Among a scan of 17 zero-parameter geometric formulas, 4λ̄ₚ = 0.84124 fm lies within 0.043% of the muonic-hydrogen radius. Both the boundary term and the 4λ̄ₚ relationship are contingent on the Euclidean Borromean bound R = 4r, which we do not prove and state as the load-bearing open problem. We claim no independent derivation of either constant.

In **cryptography**, we propose Sedenion Module-LWE (Module-SLWE), a lattice-based KEM over Sᵩ. Correctness rests on the conjugate-norm inner product, whose adjoint property follows from the verified identity lmm(a)ᵀ = lmm(ā). PSL(2,7) non-associativity produces generic left-multiplication homomorphism failure (L_{a·b} ≠ L_a L_b), which removes the ideal-lattice dimension-folding attack class and reduces security to that of a generic module lattice — a structural guarantee, not additional quantified hardness. Security therefore equals the generic lattice estimate at the chosen parameters. At k = 64, q = 911 (effective dimension 1024), a primal-uSVP estimate calibrated against ML-KEM indicates NIST Category 5 (β ≈ 940), and the decryption-failure rate is ≤ 2⁻²⁹⁵ (verified); dual and hybrid confirmation via the full lattice-estimator is pending.

We do not claim a unified theory. We claim that one algebraic object carries structural properties independently useful in both domains.

---

## I. Introduction

### A. Dual motivation

Two fields share a structural shape: both require reasoning about algebraic objects whose symmetry groups outpace the frameworks used to analyze them.

In theoretical physics, the geometric relationship between the proton's internal structure and the electromagnetic boundary condition is not fully understood, and the fine-structure constant α lacks a derivation from geometric first principles. Historically, the discrepancy between electronic and muonic hydrogen measurements of rₚ drew renewed scrutiny to this boundary condition. Subsequent electronic-hydrogen and scattering measurements have largely converged on the smaller (muonic) value (CODATA 2018: 0.8414(19) fm), and the discrepancy is now generally regarded as resolved. **We do not rely on an open puzzle**; we treat the measured radius as a fixed input and ask whether its value carries a geometric address.

In post-quantum cryptography, NIST-standardized lattice schemes (ML-KEM, ML-DSA) are built on Module-LWE over commutative polynomial rings, chosen specifically to limit the algebraic structure available to an attacker. Certain ring/ideal structures admit algebraic shortcuts in specific regimes. We explore whether non-associative (sedenion) structure can remove that attack surface *while reducing to generic lattice hardness* — i.e., whether the construction is at least as hard as a generic module lattice of the same dimension. This is a hardness exploration and a KEM candidate with stated open problems, **not a security proof and not a claim of hardness beyond generic LWE**.

### B. Epistemic conventions

| Tier | Meaning |
|------|---------|
| **T1** | Proven from stated axioms, or exhaustively verified by computation |
| **T2** | Formal claim following structurally from T1; full proof open |
| **T3** | Motivated and numerically consistent; formal proof pending |
| **T4** | Speculative; requires formalization before analysis |
| **Open Problem** | Precisely stated; resolution advances or refutes a specific claim |

Narrative framing is illustration only and is never cited as mechanism.

---

## II. Algebraic and geometric foundations

### A. The Cayley–Dickson ladder (T1)

The Cayley–Dickson doubling (a,b)(c,d) = (ac − d̄b, da + bc̄) produces **S** at the fourth step: 16-dimensional, non-commutative, non-associative, and possessing zero-divisors. The scalar units {e₀, e₈} are excluded from the imaginary traversal — a universal −2 offset appearing in both the physical boundary term (§III.A) and the cryptographic decryption path (§IV).

### B. The K₇,₇ zero-divisor interface (T1; Moreno 1998 + computational verification)

**S** over Fᵨ contains exactly 84 zero-divisor pairs for all valid primes. The 42 active index pairs cross strictly between the two octonion copies {e₁,…,e₇} and {e₉,…,e₁₅}; none lie within a single copy or involve {e₀, e₈}. These form a K₇,₇ bipartite graph (complete bipartite on 7+7, minus a perfect matching) — the **zero-divisor interface**. Prime-independent; confirmed over p ∈ {911, 2731, 907, 919}.

### C. The P¹(2,3,7) orbifold (T1)

Quotient of H² by the (2,3,7) triangle group: angles π/2, π/3, π/7; Euler characteristic −1/42; hyperbolic area π/42. The order-7 cone point is stabilized by the Z₇ subgroup of PSL(2,7) and carries the binding geometric constraint in both contexts.

Key (2,3,7) triangle measurements (exact, from the hyperbolic law of cosines): side a (opp. π/2) 0.620672; side b (opp. π/3) 0.545275; side c (opp. π/7) 0.283128; inradius 0.060452; circumradius 0.324902; area π/42.

---

## III. Physics: the proton configuration space

### A. The fine-structure boundary term (contingent illustration — T3)

The proton is modeled as a Borromean link of three flux tubes resolving the P¹(2,3,7) cone singularity. The proposed boundary correction:

> fc = 1 + 2rₚ²φ⁻⁴ / 16π

**Three items must be supplied before this is more than a contingent illustration** (flagged honestly; not resolved in v2):

1. **Dimensional convention.** As written, rₚ² (length²) cannot be added to 1. The expression is only well-defined if rₚ is dimensionless (e.g. the ratio ρ = rₚ/λ̄ₚ) or an explicit length² normalization is stated. **[AUTHOR TO SUPPLY: the exact convention.]**
2. **The fc → α⁻¹ map.** The displayed formula gives fc ≈ 1.004 at rₚ = 0.839 fm, but the v1 table reported α⁻¹ = 137.036. The explicit map α⁻¹ = g(fc) and its normalization constant are not stated. Reverse-engineering requires an unaddressed base ≈ 136.48 and still does not reproduce the table to the stated precision. **[AUTHOR TO SUPPLY: the explicit map and any base constant, with prior addresses.]**
3. **Table ↔ formula consistency.** The v1 prior-address table lists 84 and arctan(1/√2) ≈ 0.6155, neither of which appears in the displayed formula. **[AUTHOR TO SUPPLY: reconcile, or remove the unused constants.]**

Until (1)–(3) are supplied, the "numerical verification" table from v1 is **relabeled a contingent illustration**, not a verification.

Prior-address candidates (each a candidate, not a derivation): 84 = S zero-divisor pair count; 2 = scalar anchor count / CD-ladder −2 offset; 16π = two-sedenion spinor solid angle (2 × 8π); φ⁻⁴ ≈ 0.1459 = bulk modulus from vacuum geometry; rₚ = physical input.

### B. Geometric constraints on rₚ

**Geometric consistency check (not a prediction).** The order-7 cone point gives a kinematic lower bound

> rₚ ≥ sin(π/7) · λ̄ₚ = 0.09125 fm   (using λ̄ₚ = 0.2103089 fm).

The measured radius exceeds this by a factor of ~9, so the bound is *consistent with*, but does not constrain, the physical value. It is **not** presented as a prediction or a "hard lower bound."

**Degrees of freedom (heuristic).** A Borromean configuration in R³ has on the order of ~9 configurational degrees of freedom; the P¹(2,3,7) orbifold imposes cone-point holonomy and a Gauss–Bonnet closure condition that reduce this. This accounting is **heuristic** pending an explicit statement of the holonomy constraints. **[AUTHOR TO SUPPLY: explicit constraint count, or retain as heuristic.]**

**The 4λ̄ₚ observation (T3, contingent).** A scan of **17** zero-parameter geometric formulas finds that

> 4λ̄ₚ = 0.84124 fm

lies within 0.043% of the muonic-hydrogen measurement. Because this is the best match among 17 candidates, it is reported as a **selected** match, not a clean prediction; its significance is conditional on a look-elsewhere correction. The factor 4 is the conjectured Euclidean Borromean circumscription bound R = 4r, which is **not proven**.

> **Open Problem (Physics).** Derive ρ = rₚ/λ̄ₚ ≈ 3.99 from P¹(2,3,7) orbifold geometry without experimental input. The gating claim is the Euclidean Borromean bound **R = 4r**. *Caveat:* an internal group-order/area identity (168 × (π/42)/π = 4) is **not** a valid derivation — it equates a circumradius/inradius length ratio with a tiling-area ratio that happen to share the value 4, with no geometric bridge between them. R = 4r remains open.

---

## IV. Cryptography: Sedenion Module-LWE

### A. Parameters and construction

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Module rank | **k = 64** | k × 16 = **1024** effective dimension; Category 5 requires an ≈1024-dim lattice (N = 512 reaches only Category 1). |
| Modulus | **q = 911** (= 455·2 + 1), prime, ≈ 2⁹·⁸ | Smallest prime ≡ 1 (mod 455) for full PSL(2,7) Singer-orbit closure. **Small q maximizes hardness**; a large q lowers the noise rate σ/q and weakens security (q = 2³² collapses primal-uSVP to β ≈ 80). Correctness is unaffected because the sparse secret makes decryption noise dimension-independent (§IV.C). |
| Secret / randomness | **sparse ternary, Hamming weight h = 64** | β ≈ 940 → Category 5 at this q. A dense (CBD2) secret would raise the decryption-failure rate to ≈ 2⁻²¹ at q = 911 and is **not viable** without raising q (which surrenders the security margin). |
| Error | **CBD2 (η = 2)** | Standard LWE error bounds. |

The public matrix A is a k × k sedenion matrix over Fᵩ, compressed via synchronized Z₇ Singer orbits that preserve all 42 cross-interface zero-divisor pairs. The condition q ≡ 1 (mod 455), 455 = 5·7·13, ensures Fᵩˣ contains the subgroups required for the Singer action. *(Open: the roles of the factors 5 and 13, which do not correspond to element orders in PSL(2,7), should be justified or the condition tightened.)*

### B. Correctness: the conjugate-norm inner product (T1)

The conjugate-norm inner product projects onto the real scalar nucleus after the sedenion product: ⟨x, y⟩_norm = Σᵢ Re(x̄ᵢ · yᵢ). It is the standard Euclidean inner product on the coordinate vector; the sedenion structure enters the *hardness*, not the noise growth.

**Lemma (T1, computationally verified over F₉₁₁).** For any a ∈ Sᵩ, lmm(a)ᵀ = lmm(ā). This follows from Re(ū·v) = Re(v̄·u) and the definition of left multiplication.

**Theorem (Adjoint property, T1).** ⟨A ·ₛ s, r⟩_norm = ⟨s, Aᴴ ·ₛ r⟩_norm, with Aᴴᵢⱼ = Āⱼᵢ. *Proof.* Re((as)·r) = Re(s̄·(ār)) by the reversal property xy = ȳx̄; the matrix form follows from the Lemma after real projection, and the module case by summing over k. ∎

### C. Decryption-failure rate (T1 analytic + Monte-Carlo validated)

The decryption noise is N = ⟨e, r⟩_norm − ⟨s, e₁⟩_norm + e₂. For a sparse secret/randomness of **fixed** weight h, an inner product against a weight-h vector selects h distinct iid error coordinates, so

> **N is distributed as a sum of (2h + 1) = 129 iid CBD2 variables — independent of the module rank k.**

Hence Var(N) = (η/2)(hₛ + hᵣ + 1) = 129 and σ(N) ≈ 11.36 at **every** k.

Results (η = 2, h = 64), validated against an 8-million-trial vectorized Monte Carlo (empirical σ = 11.360 vs analytic 11.358; the Gaussian estimate is ~1% conservative on the tail, the safe direction, since |N| ≤ 258 has bounded support):

| Quantity | Value |
|----------|-------|
| q_min for DFR ≤ 2⁻¹²⁸ | **≈ 600, at every k** (512, 1024, 2048) |
| **DFR at q = 911** | **≤ 2⁻²⁹⁵** (≈ 167 bits below target) |
| DFR at q = 911 with a *dense* CBD2 secret (for contrast) | ≈ 2⁻²¹ — **not viable** |

The sparse-secret and small-q choices are **coupled**: small q maximizes lattice hardness, and the fixed-weight sparse secret is precisely what keeps the decryption noise low enough for small q to remain correct. A dense secret would force a larger q and surrender the security gain.

### D. Shield I — generic homomorphism failure (T1)

**Proposition (T1, computational).** For generic a, b ∈ Sᵩ, L_{a·b} ≠ L_a L_b. Over 100 independently sampled pairs, failure held in 100/100 cases; the mean Frobenius residual ‖L_{ab} − L_a L_b‖_F ≈ 39,000 against a random-matrix norm ≈ 13,000, indicating a structural effect, not small noise.

**Consequence (correctly scoped).** This eliminates the ideal-lattice dimension-folding attack class: an attacker cannot factor A through a predictable left-multiplication homomorphism. It is a guarantee that the construction **does not underperform** generic Module-LWE — **not** a claim of additional quantified hardness.

> **Open Problem (Algebra).** Prove that the locus {(a,b) ∈ Sᵩ² : L_{a·b} = L_a L_b} has measure zero over Fᵩ¹⁶ × Fᵩ¹⁶.

### E. Shield II — geometric lattice profile (T2, toy scale only)

A five-test GSO diagnostic on a 64 × 64 proxy lattice (k = 4, q = 911) found that PSL(2,7) Singer structure produces no rank deficiency, no anomalous short vectors, and no invariant sublattice relative to a uniformly random A. **This is a toy-scale negative result and does not establish anything at production dimension.**

### F. Core-SVP / lattice baseline

Hardness is estimated by primal-uSVP on the flat 1024-dimensional lattice using the **CN11 BKZ simulator** under the Core-SVP and classical-gate cost models, **calibrated against ML-KEM** (recovering Kyber-512 → β ≈ 417 ≈ Category 1, Kyber-768 → β ≈ 623 ≈ Category 3, Kyber-1024 → β ≈ 900 ≈ Category 5; the driver runs ~3% conservative relative to the canonical estimator).

At **k = 64, q = 911, sparse-ternary secret (h = 64), CBD2 error**:

> β ≈ **942** → classical sieve gate-count ≈ **2³⁰⁵** → **NIST Category 5** (≈ 33 bits above the 2²⁷² threshold; ≈ 25 bits after the calibration margin).

A CBD2 secret would give β ≈ 1062 but is ruled out by correctness at q = 911 (§IV.C). The contrast with v1: at the printed v1 parameters (N = 512, q = 2³²) the same method gives β ≈ 80–110 → ≈ 2⁶² gates → below Category 1. Each doubling of the modulus at fixed σ costs ~13 bits of classical security.

> **This is a primal/Core-SVP estimate.** Dual, BDD, and hybrid costs **must be confirmed** with the full lattice-estimator (`LWE.estimate`) before the Category 5 claim is asserted. The non-associative structure contributes no hardness beyond this estimate; its role is to remove the ideal-lattice route so that security reduces to the generic lattice problem. Security is governed by the effective dimension and the noise rate σ/q; the modulus is kept small for this reason.

---

## V. Synthesis and open problems

### A. Shared structure

A single algebraic object carries properties independently useful in both domains. We do **not** claim a physical origin for the cryptographic hardness, nor a cryptographic validation of the physics. The shared elements (84 zero-divisor pairs; Z₇ Singer orbits; scalar anchors {e₀, e₈}; non-associativity; the K₇,₇ graph) play *structurally distinct* roles in each domain; the connection is shared notation and a shared object, not a mechanism.

### B. Summary of open problems

1. **OP-Physics (gating).** Prove or refute the Euclidean Borromean bound R = 4r. If true, rₚ = 4λ̄ₚ addresses the muonic radius to 0.043%. The group-order/area identity is not a valid derivation (§III.B).
2. **OP-Physics-fc.** Supply the dimensional convention, the explicit fc → α⁻¹ map, and the table/formula reconciliation (§III.A).
3. **OP-B (critical, crypto).** Is sedenion zero-divisor membership decidable in polynomial time via Moreno's classification? **If so, the construction cannot rest on it, and the hardness basis must be re-grounded.** This is the question that could undercut the premise.
4. **OP-Algebra.** Measure-zero of the homomorphism locus (§IV.D).
5. **OP-E.** Hardness reduction to a standard lattice problem, or a Shor-impossibility argument on the Moufang-loop structure.
6. **OP-Crypto (estimator).** Confirm dual / BDD / hybrid costs at k = 64, q = 911 via the full lattice-estimator; confirm no Category drop below the primal β ≈ 942.
7. **OP-(q, η).** Joint optimization of modulus, noise, and secret weight against public-key size.

### C. Positioning

SQT is presented not as a closed unified theory but as a mathematically grounded framework that makes falsifiable predictions and states precise open problems whose resolution would advance or refute it. The cryptographic component is a **KEM candidate plus stated open problems**, not a proven scheme; for production PQC, reference the NIST standards (ML-KEM, ML-DSA, SLH-DSA).

---

## Data availability

Computational results are reproducible from the archived scripts (software DOI 10.5281/zenodo.20078013): `sedenion_Fp.py` (algebra over Fᵨ), `sedenion_audit.py` (zero-divisor enumeration), `sqt_slwe.py` (Module-SLWE trials), `sqt_cryptanalysis.py` (homomorphism-failure analysis), `op_c_dfr_analysis.py` (DFR scaling), and the five-test GSO diagnostic. The DFR and Core-SVP figures in §IV were produced with the CN11 BKZ simulator (`fpylll`) and the op_c noise model; the canonical `LWE.estimate` confirmation (OP-Crypto) remains to be run.

---

*v2 changelog: corrected the cryptographic security claim (Cat 5 → broken at the v1 parameters; corrected to k = 64, q = 911 with a verified Cat-5 primal estimate and DFR ≤ 2⁻²⁹⁵); reframed non-associativity as removing an attack class rather than adding hardness; promoted OP-B to a headline open problem; tightened the physics motivation, demoted the "hard lower bound," flagged the fc convention/map gaps, and marked R = 4r as the gating open problem with the group-order identity explicitly disqualified as a derivation.*
