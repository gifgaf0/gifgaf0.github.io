# Sedenion Module-LWE & Φ-Modular Prime Project
## Master Reference Document — v2.0 | May 10, 2026
### Matthew Gifford | Independent Researcher, Ridgemark CA

---

> **Document discipline.** This is the single authoritative reference for the
> crypto/prime subproject. It supersedes `SLWE_Prime_Master_v1.md` (May 8, 2026).
> Sources consolidated: `phi_modular_prime_finder_spec__1_.md`,
> `ledger_entry_v3_4_sedenion_Fp_computation.md`,
> `rosetta_stone_draft_v1.md`, `rosetta_stone_arxiv_v1.md`,
> and all session outputs from May 8–10, 2026.
>
> **Append-only for §§1–4 (audit sections). §5 (open problems) and
> §6 (implementation) are overwriteable as work advances.**

---

## §0 — Epistemic Tiers & Standing Rules

| Tier | Label | Meaning |
|------|-------|---------|
| T1 | VERIFIED | Independently reproducible; no free parameters |
| T2 | STRUCTURAL | Derived from established algebra; not yet independently checked |
| T3 | CONJECTURE | Plausible structural observation; no derivation yet |
| T4 | SPECULATION | Pattern-match or narrative; flagged, not promoted |

**Prior Address Standard (PAS).** Every security claim must cite a specific
reduction or measurement. Analogies are not prior addresses.

**Hardness Posture (non-negotiable).** This is NOT a proven PQC scheme.
No hardness assumption for any sedenion-based problem is established in
the literature. Highly symmetric algebraic objects have historically been
broken faster than expected. For production use, deploy NIST-standardized
schemes: ML-KEM (FIPS 203), ML-DSA (FIPS 204), SLH-DSA (FIPS 205).

**Eddington Maneuver flag.** Any instance of vocabulary substitution —
renaming a known tractable problem in algebraic language to imply hardness —
must be flagged and demoted. This standard applies to every security claim
in this document.

---

## §1 — Algebraic Foundations (T1/T2)

### §1.1 The Cayley-Dickson Sedenion Algebra

The sedenion algebra 𝕊 is the 16-dimensional Cayley-Dickson double of the
octonions. Basis: {e₀, e₁, ..., e₁₅} with e₀ as real unit. The CD
construction gives multiplication rule:

    (a,b)(c,d) = (ac − d̄b, da + bc̄)

**T1 — Verified properties:**
- All imaginary units satisfy eᵢ² = −e₀ for i = 1..15
- π(1000) = 168 (verified to match PSL(2,7) order; sanity check)
- 𝕊 is non-commutative, non-associative, admits zero-divisors
- lmm(a)ᵀ = lmm(conj(a)) exactly — zero violations over 100 random elements
  (this is the adjoint identity enabling correct decryption)

**T1 — Universal −2 scalar anchor offset:**

| CD Level | Algebra | Dim | Observable (Dim−2) | Landmark |
|----------|---------|-----|---------------------|----------|
| 2 | ℍ | 4 | 2 | H+He |
| 3 | 𝕆 | 8 | 6 | Carbon (Z=6) |
| 4 | 𝕊 | 16 | 14 | Silicon (Z=14) |
| 5 | CD₅ | 32 | 30 | Zinc (Z=30) |
| 6 | CD₆ | 64 | 62 | Samarium (Z=62) |
| 7 | Cl(7) | 128 | 126 | Last nuclear magic number |

The −2 offset is universal. Physical/nuclear interpretations are Register 2.

### §1.2 The 84 Zero-Divisor Pairs and K₇,₇ Interface

**T1 — Computational (sedenion_Fp.py, sedenion_audit.py, May 2026):**

- Exactly 84 unordered zero-divisor pairs in 𝕊 over F_p, confirmed for
  p ∈ {911, 2731, 907, 919} (two mod-455, two non-mod-455)
- Identical 84 index quadruples across all tested primes
- All 42 active index pairs cross between {e₁..e₇} and {e₉..e₁₅}
- None involve e₈ (CD doubling unit); none lie within a single octonion copy
- Structure is prime-independent: a property of the CD multiplication table

**T1 — Zero-divisor graph:**
- 14 active nodes, 42 edges
- Graph = K₇,₇ minus the perfect matching {(eᵢ, eᵢ₊₈) : i=1..7}
- 6-regular bipartite; vertex-transitive and edge-transitive
- The 7 missing edges are the CD-conjugate pairs (eᵢ · e₈ = eᵢ₊₈)
- Automorphism group contains S₇ ≀ ℤ₂

**Closed: OP §2.23.1** (ZD localization to inter-octonion interface) —
confirmed computationally May 2026.

**T2 — Singer Z₇ symmetry of ZD graph:**
The synchronized Singer cycle (i → (i mod 7)+1 on both {1..7} and {9..15})
preserves all 42 cross-interface ZD pairs without exception.
OP §2.24.1 confirmed for the Z₇ subgroup of PSL(2,7).
Full PSL(2,7) action (all 168 elements) remains open.

**Open: OP §2.24.2** — Does the 42-pair set decompose as 2 × 21 respecting
Fano geometry?

**Open: OP §2.24.3** — Does the 84-pair count and K₇,₇-minus-matching
structure persist in characteristic 2?

**Open: OP §2.24.4** — Is zero-divisor membership polytime via Moreno's
explicit classification? (If yes, ZD membership cannot be a hardness
primitive; PQC direction must use orbit-level problems instead.)

### §1.3 Mod-455 Primes and PSL(2,7) Symmetry

455 = 5 · 7 · 13, φ(455) = 288.

Primes p ≡ 1 (mod 455) satisfy p ≡ 1 (mod 5), (mod 7), (mod 13) simultaneously,
giving F_p the full PSL(2,7)/octonion multiplication symmetry.

**T1 — Key finding (prime independence):**
The 84-pair ZD structure does NOT require mod-455 primes.
What mod-455 gives (Property B) is distinct from the ZD count (Property A):

- **Property A** (prime-independent): ZD count = 84, same quadruples, all p
- **Property B** (mod-455 specific): Full PSL(2,7) symmetry of the octonion
  multiplication table over F_p

For PQC, Property B is the relevant one for public matrix structure.
For the ZD-count claim, mod-455 is not required.

**First 5 mod-455 primes:** 911, 2731, 8191, 11831, 14561

### §1.4 Homomorphism Failure (T1)

**T1 — Verified over 100 random pairs:**
- L_{a·b} ≠ L_a × L_b: 100% failure rate (0/100 pairs satisfy equality)
- Average ||L_{ab} − L_a·L_b||_F ≈ 4657–8413 (Frobenius norm)
- Ratio vs random 16×16 matrix norm: ≈ 0.24
- Depth-512 accumulated error: ~4M >> q = 911

**Cryptographic consequence:** Ideal lattice unrolling attacks require
the ring multiplication to be a module homomorphism. The 100% failure
rate makes this a structural impossibility, not a probabilistic hardness
assumption. This is the **algebraic shield**.

---

## §2 — Prime Generation Infrastructure (T1)

### §2.1 sqt_prime_core.py — Verified Implementation

Three-layer pipeline: Wheel sieve (W=10920, φ(W)=2304, 78.9% elimination)
→ Miller-Rabin (40 rounds, deterministic below 3.3×10²⁴) → Strong Lucas (Baillie-PSW).

**T1 — Self-test results (27/27 checks pass):**
- φ(10920) = 2304 confirmed
- All eᵢ² = −e₀ for i=1..15 verified
- π(1000) = 168 confirmed
- All 5 Carmichael numbers (561, 1105, 1729, 8911, 29341) correctly rejected
- Lucas bug found and fixed: bit iteration off-by-one in UV computation
  (V component used updated U; corrected to simultaneous update)

**Performance:** 256-bit primes at 1.2–5.5ms per prime; 0 Lucas rejections
observed (MR catches all composites in practice; Lucas is the final guard).

**Prime families available:**
- `random_prime(bits)` — Baillie-PSW certified
- `safe_prime(bits)` — p and (p−1)/2 both prime
- `sophie_germain_prime(bits)` — p and 2p+1 both prime
- `mod455_prime(bits)` — p ≡ 1 (mod 455)
- `mod455_safe_prime(bits)` — both constraints

### §2.2 Mod-455 Residue Experiment (Phase A Complete, Phase B Pre-registered)

Phase A: 50,000 primes at 256-bit collected; columns: prime, bit_length,
r_mod_5, r_mod_7, r_mod_13, r_mod_455, discovery_time_ms.

Phase B: Pre-registered test of whether primes cluster non-uniformly in
residue classes mod 455. φ(455) = 288 coprime classes; Dirichlet predicts
uniform distribution. Phase B blocked pending resolution of the φ(455) = 288
correction (previously confused with E₈ root count 240; corrected in
ledger v3.1 §1.4).

**Note from §1.3:** The ZD structure does not require mod-455 primes.
Phase B tests a separate statistical claim about prime distribution, not
the sedenion structure.

---

## §3 — Honeypot Canary System (T1)

### §3.1 Architecture (telemetry_server.py, canary_deploy.py)

Three-component system for monitoring cryptographic tripwires:

**Key ladder** (5 honeypot keys, gradient from trivial to non-trivial):
1. 512-bit sequential (Fermat-factorable, seconds) — url_token canary
2. 512-bit mod-455 (structural family, ECM/NFS) — url_token canary
3. 512-bit random (baseline) — url_token canary
4. 1024-bit mod-455 (medium structural) — credential canary
5. 1024-bit random (medium baseline) — credential canary

**Fire order interpretation:** If mod-455 fires before random at the same
bit size → adversary is exploiting PSL(2,7) algebraic structure.
This is the actual research signal: structural family = attack surface.

**Canary payload types:** URL token (fires on HTTP fetch), credential
(fires on API use), SSH key (fires on login attempt).

**OAEP fix (May 2026):** 512-bit keys require SHA-1 OAEP (SHA-256 needs
≥528 bits). Plaintext > max_plain is truncated via SHA-256 hash before
encryption. Round-trip verified correct.

**Self-test: 11/11 checks pass.**

### §3.2 Research Signal

The honeypot system operationalizes the PQC research question: does the
mod-455/PSL(2,7) structure create exploitable attack surface? If yes, the
canary fires early. If no, structural and random keys fall at the same rate.
This is empirical measurement, not theoretical argument.

---

## §4 — SQT-SLWE Scheme (T2/T3)

### §4.1 Architecture

**Scheme:** Module LWE over the sedenion algebra with PSL(2,7)-structured
public matrix and conjugate-norm inner product.

**Parameters (toy scale — current implementation):**

| Parameter | Toy | Production target |
|-----------|-----|-------------------|
| Module rank k | 4 | 32 |
| Sedenion dim | 16 | 16 |
| Effective dim N | 64 | 512 |
| Modulus q | 911 | ~3329 (mod-455 prime) |
| Secret | rand non-ZD | sparse ternary {-1,0,1} |
| Noise | CBD-like ±2 | CBD_η=2 |

**Key equations:**

    KeyGen:    b = A ⊛ s + e          (sedenion module left-mult)
    Encaps:    c₁ = A^H ⊛ r + e₁     (conjugate-transpose)
               c₂ = ⟨b, r⟩_norm + e₂ + m·⌊q/2⌋
    Decaps:    v = c₂ − ⟨s, c₁⟩_norm
               m = round(2v/q)

where ⟨u, v⟩_norm = Σᵢ Re(conj(uᵢ) · vᵢ) mod q.

### §4.2 Correctness (T1)

**T1 — Adjoint property verified:**
⟨A·s, r⟩_norm = ⟨s, A^H·r⟩_norm — holds exactly (0 violations over
all tested instances). This follows from lmm(a)ᵀ = lmm(conj(a)).

**Previous correctness failure (resolved):** The original Regev-style
decryption used standard sedenion inner product (left-multiply). The
transpose property ⟨A·s,r⟩ = ⟨s,A^T·r⟩ fails with 15/16 differing
components because sedenion is non-associative. The conjugate-norm inner
product resolves this.

**DFR at toy scale:** ~48% failure at k=4, q=911 with dense random secrets.
This is a **parameter problem, not an architecture problem**. The adjoint
holds; the noise accumulates beyond p/4 because q=911 is too small for
dense secrets over k=4 terms. Fix: sparse ternary secrets + larger q.

### §4.3 PSL(2,7) Singer Structure in A (T1/T2)

Each row of A is a Singer cycle orbit of a seed element:

    Row i = [seed_i, σ(seed_i), σ²(seed_i), ..., σ^{k-1}(seed_i)]

where σ: eᵢ → e_{(i mod 7)+1} for i=1..7, synchronized across both
octonion copies.

**T1 — Rank:** PSL(2,7)-structured A has full rank 64/64 at toy scale,
identical to random A. Zero rank cost from Singer structure.

**T1 — Singer orbit verification:** confirmed in code.

**T2 — Z₇ does NOT fold the effective dimension:**
- Ring-LWE: full n×n matrix determined by 1 seed → n-fold compression
- SQT-SLWE: k independent row seeds; Z₇ links blocks within a row only
- Different rows have independent seeds → k independent subproblems
- Effective attack dimension: k·16 = N (no reduction to N/7)

If Z₇ folded to N/7=73 (worst case, not demonstrated):
beta~40, quantum~40b → BROKEN.
Status: NOT demonstrated; rows are independent by construction.

### §4.4 Security Assessment (T2)

**Model:** Core-SVP, calibrated to Kyber ground truth.
Formula: beta ≈ 0.4965·n − 6.25 (at q=3329, σ=1), q-corrected.
Calibration check: Kyber-512 formula gives beta=120 vs spec 118 — OK.

**Security table (no-folding assumption):**

| Scenario | n | q | beta | Classical | Quantum | Level |
|----------|---|---|------|-----------|---------|-------|
| Kyber-512 (ref) | 256 | 3329 | 120 | 166b | 120b | <L1 |
| Kyber-768 (ref) | 384 | 3329 | 184 | 254b | 184b | L1 ✓ |
| Kyber-1024 (ref) | 512 | 3329 | 247 | 341b | 247b | L3 |
| SQT-SLWE k=32 q=911 | 512 | 911 | 295 | 408b | 295b | L5 |
| SQT-SLWE k=32 q=3329 | 512 | 3329 | 247 | 341b | 247b | L3 |

**The IF:** All numbers above assume non-associativity prevents algebraic
dimension folding. This is computationally established (100% homomorphism
failure) but not formally proven as a security reduction. Until that proof
exists, treat these as upper bounds.

**Structural attack scenarios (k=32, n=512, q=3329):**

| Attack | beta | Quantum | Status |
|--------|------|---------|--------|
| No folding (non-assoc blocks) | 247 | 247b | Target |
| Z₇ folds n to 73 | 40 | 40b | BROKEN — NOT demonstrated |
| 16D blocks exploitable as Ring-LWE | 40 | 40b | BROKEN — PREVENTED by non-assoc |

### §4.5 Annihilator Attack Results (T1)

**T1 — Single-element scale:**
ZD-pair annihilator (z·A=0 exactly): residual ||z·(A·s)||² ≈ 916,442
vs noise ||z·e||² ≈ 44 → ratio ≈ 20,000×. Noise buried.

**T1 — Module scale (k=4):**
Norm inner product collapses attack to scalar channel (1D vs 16D).
z·(A·s) ≠ 0 via sedenion annihilator; scalar magnitude still differs
from z·e but by a smaller factor than the full sedenion case.

**Explanation of scalar collapse:** The norm inner product
⟨u,v⟩_norm = Re(conj(u)·v) is bilinear over F_p. Even if z·A_elem = 0
as a sedenion product, Re(conj(z)·(A·s)) is not forced to be 0 because
the real-part projection is not the same as the sedenion product.

---

## §5 — Geometric Lattice Analysis (T1/T2)

### §5.1 Five-Test Framework (sqt_lattice_geometry.py)

All tests at k=4, n=64, q=911 proxy lattice.

**Test 1 — Rank: PASS**
Both structured and random A: full rank 64/64.
Singer orbits create no linear dependencies.

**Test 2 — Row norms: PASS**
min norm ratio (structured/random) = 1.038.
No anomalously short basis vectors from PSL(2,7) structure.
Both matrices above Gaussian heuristic λ₁ ≈ 1585 (min observed: 1829).

**Test 3 — GSO log-profile: INVESTIGATE**
Structured profile range: 6.02 vs random: 3.13 (~2× variance).
Profile drops more steeply at indices 48–63 (tail end).
BKZ exploits declining GSO profiles; the tail deviation is the primary
open geometric question. At 64D this is not immediately exploitable;
at 512D a systematic bias would give BKZ measurable advantage.

**Test 4 — Row correlations: PASS**
Structured A: mean|corr| = 0.071. Random A: mean|corr| = 0.102.
Singer orbits produce LOWER correlation than random (counterintuitive).
No exploitable pairwise row dependencies.

**Test 5 — PSL(2,7) invariant sublattice: RESOLVED**
dim(ker(P−I)) = 16 for Singer P on Z_q^64.
Initial flag: potential weakness.
Resolution: the 16 kernel vectors are:
  - 4 fixed points e₀ per block (one per block)
  - 4 fixed points e₈ per block
  - 4 orbit-sum vectors (Σe₁..e₇) per block
  - 4 orbit-sum vectors (Σe₉..e₁₅) per block
Each Singer 7-cycle contributes exactly 1 kernel vector (the orbit sum).
4 blocks × 4 vectors = 16. This is structural and expected.

**Critical finding:** A does NOT preserve this subspace.
A·(invariant vector) is NOT invariant under Singer.
The 16D fixed-point subspace is a geometric artifact, NOT an A-stable
lattice ideal. BKZ cannot target it without knowing the Singer structure.

### §5.2 Open Geometric Question

The GSO profile steepness at tail indices (48–63) is the one unresolved
geometric concern. The specific test needed: at k=32, n=512, does the
Singer-structured A produce a systematically steeper GSO profile than
random A? If yes: BKZ gets a measurable advantage at production scale.
If no: the geometric shield holds at cryptographic dimension.

This requires full BKZ simulation at N=512 to close definitively.

---

## §6 — Implementation File Index

| File | Purpose | Status |
|------|---------|--------|
| `sqt_prime_core.py` | Prime generation, Baillie-PSW, mod-455, safe primes | T1, 27/27 tests pass |
| `telemetry_server.py` | Flask canary server, SQLite, dashboard | Functional |
| `canary_deploy.py` | Honeypot key gen, canary payloads, key ladder | 11/11 tests pass |
| `sedenion_Fp.py` | Sedenion algebra over F_p, Cayley-Dickson mult table | T1, verified |
| `sedenion_audit.py` | ZD pair enumeration, graph analysis | T1, 84 pairs confirmed |
| `sedenion_lwe_sandbox.py` | Three-part attacker/defender sandbox | Tests run |
| `sedenion_module_lwe.py` | Module LWE with PSL(2,7) A (broken — old scheme) | Superseded by sqt_slwe.py |
| `sqt_slwe.py` | Corrected SQT-SLWE with conjugate-norm inner product | T2, DFR issue at toy params |
| `sqt_cryptanalysis.py` | BKZ cost, structural vulnerability, non-assoc penalty | T2 analysis |
| `sqt_lattice_geometry.py` | Five geometric tests on structured vs random A | T1/T2 |
| `sedenion_lwe_check.py` | Left-mult injectivity audit | T1, ZD secrets ruled out |

**Key finding from sedenion_lwe_check.py:**
ZD elements as LWE secrets: rank(L_s) = 12 for ALL 42 ZD elements (ker dim=4).
SINGULAR — cannot be used as LWE secrets.
Random non-ZD elements: rank = 16 in 200/200 cases — safe.

---

## §7 — Open Problems Consolidated

| ID | Problem | Blocking | Priority |
|----|---------|----------|----------|
| OP §2.24.1 | Full PSL(2,7) (168 elements) acts as ZD graph symmetry | Nothing | Medium |
| OP §2.24.2 | 42 pairs decompose as 2×21 respecting Fano geometry | Nothing | Low |
| OP §2.24.3 | 84-pair structure in characteristic 2 | Nothing | Low |
| OP §2.24.4 | ZD membership polytime via Moreno classification | **Critical for PQC** | High |
| OP-Crypto-1 | Full BKZ simulation at N=512 for GSO profile | OP §2.24.4 should go first | High |
| OP-Crypto-2 | Formal hardness reduction for Module-SLWE | Requires OP-Crypto-1 | High |
| OP-Prime | Phase B mod-455 residue distribution test | φ(455)=288 correction done | Medium |

**Critical path for PQC credibility:**
1. Resolve OP §2.24.4 (membership polytime check) — if polytime, pivot to orbit problems
2. Run OP-Crypto-1 (BKZ at N=512) — closes the GSO profile concern
3. Attempt OP-Crypto-2 (hardness reduction) — this is the paper

---

## §8 — What This Is and Is Not

**What it is:**
- A structurally sound KEM construction with verified adjoint property
- A computationally established algebraic shield (100% homomorphism failure)
- A computationally verified geometric shield at reduced dimension (N=64)
- A prime generation library with production-quality Baillie-PSW certification
- A honeypot system for empirically measuring structural attack surface
- A precise set of open problems whose resolution would either confirm or
  refute the security claims

**What it is not:**
- A proven PQC scheme
- A formal hardness proof or security reduction
- A replacement for NIST-standardized schemes for any production use
- Evidence that the sedenion structure is hard for an adversary who knows it

**The load-bearing unproven claim:**
That 100% homomorphism failure rate translates to zero exploitable algebraic
shortcut for a lattice geometry adversary working directly in ℤ_q^512
without engaging the sedenion algebra. A lattice attacker doesn't need
to work in 𝕊 — they work in ℤ_q^512 geometrically. Whether the
PSL(2,7)/Singer origin of A creates any exploitable lattice geometry
is the central unanswered question.

---

## §9 — Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | May 8, 2026 | Initial consolidation from May 8 session |
| v2.0 | May 10, 2026 | Full update: corrected SQT-SLWE scheme (conjugate-norm inner product), five geometric tests, calibrated BKZ security table, annihilator attack at module scale, GSO profile analysis, invariant sublattice resolution, consolidated open problems |

---

*Append-only ledger discipline preserved in parallel SQT project.
No prior ledger content was modified in the preparation of this document.*
