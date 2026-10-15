<!--
  Working titles (pick one for submission):
   1. Generator-Induced Invariants in Lattice Public Keys: A Pre-Standardization Rank Diagnostic
   2. When the Structure You Added Is the Structure That Breaks You
   3. Design-Matrix Rank Ceilings in Seed-Generated Public Keys
  First draft — October 2026. Math at paper-body rigour; reference list is leads to verify.
-->

# Generator-Induced Invariants in Lattice Public Keys
## A pre-standardization rank diagnostic, with a worked case study

**Matthew Gifford** — Independent Researcher, Hollister, California, USA
*First draft, October 2026*

---

### Abstract

A public-key construction that builds its public object by applying a fixed family of
linear maps to random seeds — for key compression, for an inherited symmetry, or to
support a reduction — produces an object that is the image of a single **fixed design
matrix**. Every invariant of that matrix, its rank first of all, is then imposed on the
public object *independently of the seeds*. When the rank of the design matrix is below
the ambient dimension, the public key is distinguishable from random by exact linear
algebra and key recovery collapses to a problem of the design matrix's rank, not the
ambient dimension. We state this as a one-line theorem (the rank of a product is bounded
by the rank of either factor), draw out its consequences for distinguishing and recovery,
and isolate the reason the weakness is easy to miss: it is **generically invisible below
the generator's saturation size**, so a rank check run on a small instance returns a clean
result even for a broken scheme. We make the point concrete with a fully reproducible case
study — a recently withdrawn sedenion Module-LWE proposal whose Singer-orbit public matrix
has rank at most 76 at every module rank, and whose own security check missed this because
it was run one instance size too small. We package the lesson as a cheap, exact diagnostic
(a design-matrix rank test run above saturation, against a uniform control) with a runnable
implementation, and we place the mechanism in a line of historical breaks in which structure
introduced for a benefit became the attack surface. The diagnostic is necessary, not
sufficient; it is strictly cheaper than the lattice-estimator step it should precede.

---

### Epistemic conventions

Claims are tagged by tier, following the author's other work.

| Tier | Meaning |
|---|---|
| **T1** | Proven from stated definitions, or exhaustively verified by exact computation. |
| **T2** | Follows structurally from T1; full proof sketched, not written in full. |
| **T3** | Motivated and numerically consistent; formal statement pending. |

The central mechanism (§2) and the case study (§3) are **T1**. The taxonomy (§5) is
retrospective reporting of published results; where it draws an analogy beyond the T1
theorem, it says so explicitly.

---

## 1. Introduction

Uniformly random public keys are large, and designers routinely replace them with a
*generated* object that is cheaper to store or transmit: the cyclic and negacyclic
structure of Ring- and Module-LWE, the quasi-cyclic and dyadic codes of compact
code-based schemes, group-action images, and orbit constructions of various kinds. The
generator is always introduced for a reason — a smaller key, a symmetry the designer
believes is benign or even helpful, or a structural argument that the construction reduces
to a well-studied problem.

The thesis of this note is that such a generator is a fixed linear gadget, and that
feeding random seeds through a fixed linear gadget cannot produce anything outside that
gadget's image. If the gadget carries an invariant — a rank ceiling, a fixed invariant
subspace, a common annihilator — the public object inherits that invariant no matter how
much entropy the seeds carry. When the invariant is a rank ceiling below the ambient
dimension, the consequences are immediate and severe: the public key is distinguishable
from uniform, and key recovery drops to the rank of the design matrix rather than the
ambient dimension.

None of the linear algebra here is deep; that is precisely the point. The mechanism is
elementary, the diagnostic that catches it is a few seconds of exact arithmetic, and yet
the weakness is easy to ship, because it is **generically invisible at small instance
sizes**. Below the point at which the generator's images are exhausted, the generated
object is full rank and statistically indistinguishable from a uniform control. A rank
check run there — exactly the diligent thing to do — returns a clean result. The pathology
only separates from the control once the instance is large enough to saturate the
generator. A scheme can therefore pass its own structural self-test and still carry a fatal
rank ceiling, if the self-test was run one size too small.

**Contributions.**

1. A general statement (§2, T1): a seed-generated public object factors as `M = R·D` with
   `D` a fixed design matrix, and `rank M ≤ rank D` for every instance and every seed draw.
   The same factorization yields a fixed low-dimensional subspace containing the public
   object's rows — a distinguisher — and confines the LWE error to a subspace of dimension
   `rank D`, reducing recovery to that dimension.
2. The **saturation principle** (§2, T1/T2): the ceiling is observable only at instance
   sizes whose ambient dimension exceeds `rank D`; a check below that size is uninformative.
3. A fully reproducible case study (§3, T1): a withdrawn sedenion Module-LWE proposal in
   which exactly this mechanism gives a rank-76 ceiling at every module rank, together with
   a post-mortem of why the scheme's own geometric self-test (run at module rank 4) could
   not see it.
4. A cheap, exact **diagnostic** (§4) — compute the design matrix's rank over the real
   field, above saturation, against a uniform control — with a runnable implementation that
   reproduces the case study as a regression fixture.
5. A short taxonomy (§5) placing the mechanism among historical breaks of the same shape,
   and an honest account (§6) of what the T1 theorem does and does not cover.

**Scope.** This is a defensive, methodological note. The case study is the author's own
withdrawn proposal; the NIST standards appear only as correctly-designed controls. No
attack on any deployed or standardized system is given or implied.

---

## 2. The mechanism

### 2.1 Setup

Let `F` be a field. By a **seed-generated public object** we mean the following. A scheme
fixes a finite family of `F`-linear maps `T₀, …, T_{r-1} : F^d → F^d` (the *generator*),
draws independent random *seeds*, and assembles the public object by applying the generator
to the seeds and combining the results `F`-linearly. Flatten to coordinates the particular
`F`-linear map the scheme exposes to an adversary — for an LWE-type KEM, the map `s ↦ As`
whose matrix we call `M`. The assembly being linear in the seeds and linear in the fixed
generator images, `M` is **bilinear** in (seeds, generator), so it factors as

> **`M = R · D`**,

where `R` collects all and only the seed randomness (an `a × N` matrix whose entries are
`F`-linear in the seed coordinates), and `D` is an `N × b` matrix that is **fixed**:
its entries are determined by the generator family `{T_j}` and the combination rule, with
no dependence on the seeds. We call `D` the **design matrix**.

### 2.2 The rank ceiling

> **Proposition 1 (T1).** For every instance and every seed draw, `rank M ≤ rank D`.
>
> *Proof.* `M = R·D`, and the rank of a product is at most the rank of either factor
> (`col(R·D) ⊆ col(R)` and `row(R·D) ⊆ row(D)`). Hence `rank M ≤ rank D`. ∎

The content is entirely in the observation that `D` is fixed. Seed entropy moves `M`
*within* the image of `D`; it cannot enlarge the rank beyond `rank D`. If `rank D` is
below the ambient dimension `b`, then every public key the scheme can ever emit is
rank-deficient by the same amount, with probability one.

> **Corollary 1 (T1, distinguisher).** Every row of `M` lies in the fixed subspace
> `row(D)` of dimension `rank D`. Equivalently there are `b − rank D` fixed linear relations,
> computable from the design alone, satisfied by every public key. A uniform object of the
> same shape satisfies no such relation (with overwhelming probability), so an exact-rank or
> linear test distinguishes the two.

> **Corollary 2 (T1, recovery).** Write the public key as `t⃗ = M s⃗ + e⃗` (LWE form), with
> `V = col(M)`, `ρ = dim V = rank M ≤ rank D`, and ambient dimension `b` (the number of
> columns of `D`). Then `t⃗ − e⃗ ∈ V`, so the error satisfies `b − ρ` public linear
> constraints and is confined to the `ρ`-dimensional affine subspace `t⃗ − V`. Choosing `ρ`
> coordinates on which a basis of `V` is invertible expresses the remaining `b − ρ` error
> coordinates as fixed affine functions of those `ρ`, i.e. an LWE instance in `ρ` unknowns
> with `b − ρ` samples. Recovery is therefore a dimension-`ρ` problem, not a dimension-`b`
> one.

Rank is the cheapest invariant to read off, but it is not the only one: any fixed invariant
subspace of `D`, or any common left annihilator, transfers to `M` by the same argument and
gives the adversary a projection that shrinks the secret. The rank ceiling is simply the
most lethal and the easiest to test.

### 2.3 Saturation: why the ceiling hides

The design matrix is assembled from the generator images available at a given instance
size. Suppose the generator contributes `c` independent images in total (for a cyclic
generator of order `r` acting on a `d`-dimensional alphabet, `c ≤ r·d`, and the column
space of the design stops growing once the instance reaches `r` blocks, because the images
repeat). Let `ρ = rank D` be the eventual ceiling and let `ambient(k)` be the full rank a
uniform control would have at instance size `k`.

> **Proposition 2 (saturation, T2).** For instance sizes `k` with `ambient(k) ≤ ρ`, the
> generated object `M_k = R_k · D_k` is generically of full rank `ambient(k)`, exactly as a
> uniform control would be; the ceiling is invisible there. The deficiency `rank M_k < ambient(k)`
> appears only once `ambient(k) > ρ`.
>
> *Reasoning.* Below the ceiling, `D_k` has `ambient(k) ≤ ρ` columns and generically attains
> rank `ambient(k)`; a generic `R_k` preserves this, so `M_k` is generically full rank. Once
> `ambient(k) > ρ`, Proposition 1 caps `rank M_k` at `ρ < ambient(k)`. ∎

The practical corollary is the one that matters for evaluation: **a structural rank check
is only meaningful at an instance size whose ambient dimension exceeds the eventual
ceiling.** A check run below saturation cannot distinguish a broken generator from a sound
one. §3.3 is this proposition observed in the wild.

---

## 3. Worked example: a sedenion Module-LWE proposal

We instantiate the mechanism on a concrete, recently withdrawn scheme. All numerical
claims in this section are reproduced from the negative-result note that broke it
[Gifford 2026a], to which we refer for the full computations; our purpose is to exhibit
the general mechanism of §2, not to re-derive the break. The scheme and its break are the
author's own, which makes this the most self-critical possible vehicle for the lesson.

### 3.1 The construction and its intent

The scheme ("SLWE") is a Module-LWE KEM over the 16-dimensional sedenion algebra
`S_q = S ⊗ F_q` (the fourth Cayley–Dickson algebra over `F_q`). Its public matrix
`A ∈ S_q^{k×k}` is built by orbits of an order-7 coordinate permutation `σ` — a "Singer
cycle" inherited from the PSL(2,7) symmetry of the Fano plane — with `A_{ij} = σ^j(seed_i)`
for independent uniform seeds `seed_i ∈ S_q`. The orbit structure was deliberate: it
compresses the key (each row is generated from one seed) and was intended to preserve the
algebra's zero-divisor interface. Non-associativity was argued to *remove* an ideal-lattice
attack class, reducing security to that of a generic module lattice; two parameter sets
were published with a claim of NIST Category 5.

### 3.2 The factorization and the rank ceiling (T1)

Flatten `s ↦ A s` to the matrix `M ∈ F_q^{16k×16k}` with
`M_{16i+u,\,16j+c} =` coefficient `u` of `σ^j(seed_i)·e_c`. Because `σ` is linear and the
sedenion product is bilinear, this factors exactly as in §2.1:

> `M = (S ⊗ I_16) · N_k`,

where `S ∈ F_q^{k×16}` holds the seeds (this is `R`) and `N_k` is built from the columns of
a **fixed** integer matrix `N ∈ Z^{256×112}`, `N_{16m+u,\,16j+c} =` coefficient `u` of
`σ^j(e_m)·e_c` (this is `D`). Since `σ^7 = id`, the column blocks of `N_k` repeat with
period 7, so `col(N_k) = col(N)` and `rank N_k = rank N` for every `k`.

Exact computation gives `rank N = 76`, over `ℚ` and over every prime tested (the modulus
`q ≈ 2³²` of the first parameter set, `911` of the second, and others) — the ceiling is
characteristic-independent. By Proposition 1, `rank A ≤ 76` at **every** module rank `k`,
against `16k` for a uniform matrix of the same shape. Table 1 reproduces the exact ranks.

**Table 1.** Exact rank of the flattened public map at module rank `k`, Singer-orbit
versus uniform matrix (reproduced from [Gifford 2026a], and regenerated by the tool of §4).

| `k` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ambient `16k` | 16 | 32 | 48 | 64 | 80 | 96 | 112 | 128 | 256 | 512 | 1024 |
| Singer-orbit | 16 | 32 | 48 | 64 | **72** | **74** | **76** | 76 | 76 | 76 | 76 |
| uniform | 16 | 32 | 48 | 64 | 80 | 96 | 112 | 128 | 256 | 512 | 1024 |

By Corollary 2, recovering the noise is a dimension-76 LWE instance with `16k − 76` samples;
the lattice estimator places it near `2³⁹`–`2⁴⁰` operations at both published parameter
sets, with the block size at the model floor — reduction at the scale of LLL already
suffices [Gifford 2026a]. Distinguishing the public key from uniform is cheaper still:
Corollary 1 needs only Gaussian elimination.

### 3.3 Why it hid: a check run below saturation

The scheme was not shipped without a structural self-test. Its design included a
"geometric lattice profile" check — a five-test Gram–Schmidt diagnostic looking for exactly
the kind of anomaly at issue — and that check reported *no rank deficiency, no anomalous
short vectors, and no invariant sublattice* relative to a uniform matrix. The check was run
on a module rank `k = 4` proxy.

At `k = 4` the public map has `16·4 = 64` columns — **below the ceiling of 76.** By
Proposition 2 the generated object is generically full rank there, exactly like the uniform
control; the deficiency cannot appear until `16k > 76`, i.e. `k ≥ 5`, and is pinned at 76
once the generator saturates at `k ≥ 7`. The self-test returned a clean result not because
the scheme was sound but because it was evaluated one instance size too small. Table 1 makes
the trap visible at a glance: rows 1–4 are identical for the Singer-orbit and the uniform
matrix — there is genuinely nothing to see — and they separate only from `k = 5`. This is
the single most instructive feature of the case, and it motivates the "above saturation"
requirement of the diagnostic in §4.

### 3.4 Non-associativity was a red herring (T1)

The scheme's security narrative rested on the non-associativity of the sedenions and on the
`σ`-symmetry of `A`. Neither bears on the break. Once decryption uses the bilinear
conjugate-norm pairing (as the scheme does), every map the adversary needs is `F_q`-linear,
and the argument of §2 uses only linearity; the much-advertised non-associativity never
enters. The permutation `σ` is not an automorphism of the sedenion product — it is a
relabelling of coordinates — so the "symmetry" of `A` is not an algebraic symmetry at all.
The general lesson generalizes beyond this scheme: **advertised algebraic richness can be
entirely orthogonal to the property that actually carries security**, and a security
argument phrased in terms of the rich structure may be answering the wrong question.

### 3.5 The repair that wasn't (T1)

After the rank deficiency was found, the natural repair was to replace the Singer-orbit
matrix with a uniform one, which removes the ceiling. It does not rescue the security
claim: at the first parameter set the modulus-to-noise ratio alone leaves the cheapest
attack near `2⁵¹`, and at the second near `2¹⁶⁷`, some 95 bits below the `2²⁶²` the same
estimator assigns ML-KEM-1024 [Gifford 2026a]. This is a second, independent lesson, and a
caution about the diagnostic of §4: **clearing the structural flag you found does not clear
the parameter problem you did not.** The design-matrix rank test is necessary, never
sufficient.

---

## 4. The diagnostic

The mechanism of §2 yields a checklist any designer or evaluator can run before trusting a
compressed or structured public key, at a cost far below the lattice-estimator step it
should precede.

1. **Factor.** Rewrite the public-key construction as `M = R·D`, isolating the seed
   randomness `R` from the fixed generator gadget `D`. If no such factorization exists —
   the public object is genuinely uniform — there is nothing to check here.
2. **Locate saturation.** Count `c`, the number of independent generator images (columns of
   `D`). Note the smallest instance size `k*` with `ambient(k*) > rank D`. *Any check below
   `k*` is uninformative* (Proposition 2).
3. **Compute the ceiling exactly.** Compute `rank D` over the **real** field `F_q` — exact
   arithmetic, not floating point — at an instance size `≥ k*`, and over a second
   characteristic to confirm the ceiling is not an artifact of one prime.
4. **Control.** Compare against a uniform object of identical shape at the same size, over
   several seed sets.
5. **Flag.** Report a ceiling if `rank D < ambient`; report a projection weakness if `D`
   has any nontrivial common invariant subspace. Either gives a distinguisher (Corollary 1)
   and a dimension-reduced recovery (Corollary 2).

The test is exact linear algebra on a matrix of the design's size — seconds, no lattice
reduction, no estimator — and is strictly cheaper than the Core-SVP estimate a candidate
already runs. It belongs **before** that estimate, because a positive result makes the
estimate moot.

**Where to look.** The factorization of step 1 exists whenever the public object is
"generator applied to seeds": cyclic or orbit-generated matrices, group-action public keys,
structured-code substitutions, and any object described as "compressed", "symmetric", or
"inheriting" an algebraic structure. The absence of the factorization (a genuinely uniform
key) is itself the sound design.

**Implementation.** A standalone, dependency-free implementation accompanies this note
(`design_matrix_rank.py`). It exposes a `GeneratorScheme` interface — implement
`design_matrix()`, `realize()`, `ambient_rank()`, and `random_seeds()` for your
construction — and runs steps 2–5 with a verdict. It ships with the sedenion scheme of §3 as
a built-in case (verdict: **fail**, ceiling 76, characteristic-independent) and a uniform
control (verdict: **pass**), and a `--self-test` mode that reproduces Table 1 and the
rank-76 ceiling across three seed sets and four characteristics as a regression fixture. The
empirical saturation curve it prints is Table 1; the rows below `k = 5` are explicitly
flagged "collapse invisible", which is §3.3 in executable form.

---

## 5. The pattern recurs

The sedenion scheme is one instance of a recurring shape: **a structural feature introduced
for a benefit carries an invariant, or an auxiliary datum, that an attacker reads off.**
The T1 theorem of §2 covers the *linear-image* instances exactly; the others below are the
same meta-pattern and are offered as motivation for the general habit, not as corollaries of
the theorem. All are published, and all are breaks of proposed or withdrawn constructions.

- **Rank/image ceiling from a generator (T1).** The sedenion scheme of §3. *Benefit sought:*
  key compression and inherited symmetry. *Lever:* the design matrix's rank. This is the
  linear-image case the theorem governs directly.

- **Structured-code substitution — the McEliece family (T2).** Random binary Goppa codes
  give a sound McEliece instance; substituting a *structured* code to shrink the key has been
  broken repeatedly — generalized Reed–Solomon codes (Sidelnikov–Shestakov, 1992), compact
  quasi-cyclic and dyadic variants (Faugère–Otmani–Perret–Tillich, EUROCRYPT 2010), and
  algebraic-geometry codes (Couvreur–Márquez-Corbella–Pellikaan, 2014) — by structural attacks
  that recover the hidden code from the public generator matrix. The shape is identical to §3:
  structure added for size became the lever.

- **Overstretched NTRU (T2).** A large modulus at fixed noise causes a **dense sublattice**
  to appear, broken by subfield / sublattice attacks (Albrecht–Bai–Ducas; Kirchner–Fouque),
  with the onset later pinned as the "fatigue point" (Ducas–van Woerden). Here the structural
  artifact is created by a parameter choice made for functionality rather than by an explicit
  generator, but the lever is again a fixed low-dimensional structure in the public object.

- **Principal-ideal lattices and short generators (T2).** Compact key constructions over
  principal ideals (e.g. Soliloquy) admit short-generator recovery (Campbell–Groves–Shepherd;
  Cramer–Ducas–Peikert–Regev): the ideal structure chosen for compactness is the recovery
  route.

- **SIDH/SIKE — auxiliary structure for functionality (analogy, not T1).** The torsion-point
  images `φ(P), φ(Q)` are published to let the key exchange complete; the 2022 attacks, all
  published at EUROCRYPT 2023 (Castryck–Decru; Maino–Martindale–Panny–Pope–Wesolowski; Robert,
  polynomial-time in full generality), via Kani's theorem embedding the secret isogeny into a
  higher-dimensional abelian variety, turn exactly that auxiliary structure into key recovery.
  This is *not* a rank ceiling and not an instance of the §2 theorem; it is the same meta-lesson
  — the structure published to make the scheme work was the attack surface — and we include it
  to mark the boundary of the linear-image argument.

The unifying question the taxonomy recommends asking of any structured proposal is simply:
*what did the structure I added give the attacker?* For the linear-image cases, §4 answers it
mechanically and cheaply; for the others, the question is a design discipline rather than a
single test.

---

## 6. Limitations and honest scope

- **The theorem is about linear-image generators only.** Proposition 1 is exact and general
  for objects bilinear in (seeds, fixed generator). Nonlinear generators, and the SIDH/SIKE
  case of §5, are outside it; there they are analogy, not consequence, and §5 says so at each
  point.
- **Necessary, not sufficient.** Passing the diagnostic — full-rank design matrix, no
  invariant subspace — establishes only that *this* class of weakness is absent. §3.5 is the
  cautionary coda: with the structure removed, the case-study scheme still failed on its
  modulus-to-noise ratio, which this test does not and should not judge.
- **Structure is not the enemy.** Module-LWE and binary-Goppa McEliece are structured and
  sound. The claim is narrow and testable: *generator-induced invariants must be computed, over
  the real field, above saturation, before a structured public object is trusted* — not that
  structure should be avoided.
- **Idealised adversary for the recovery corollary.** Corollary 2 states the dimension to
  which recovery reduces; the concrete cost is then a lattice-estimator question (and depends,
  as §3.5 shows, on parameters the rank test is silent about).
- **References verified.** The citations in §5 and below were checked against primary sources
  (IACR ePrint, the journal and conference records, DBLP, and authors' own pages) in October
  2026. The two self-references to the author's own Zenodo depositions still need their current
  version DOIs pinned.

---

## 7. Reproducibility

- `design_matrix_rank.py` (accompanying this note): the §4 diagnostic. `--self-test`
  reproduces Table 1 and `rank N = 76` over `F₉₁₁`, `F₂₇₃₁`, `F_{2³¹−1}`, and the first
  parameter set's `q`, across three seed sets. Pure Python, no dependencies; exact rank by
  Gaussian elimination over `F_p`.
- The full break of the case-study scheme, including both independent rank implementations
  (one written blind from a textual specification), the exact-rank computation with
  python-flint, and the lattice-estimator runs, is archived with [Gifford 2026a].

---

## Acknowledgements

AI agents (Anthropic's Claude) assisted in drafting this note, in generalizing the mechanism
from the case study, and in writing and running the accompanying diagnostic, including its
reproduction of the published rank table. The author directed the work, reviewed the text,
and takes responsibility for it.

---

## References

*Verified against primary sources (IACR ePrint, journal/conference records, DBLP, authors'
pages), October 2026. The two Gifford self-references need their current Zenodo version DOIs
pinned before external use.*

**Primitives and controls**
- O. Regev. *On lattices, learning with errors, random linear codes, and cryptography.*
  J. ACM 56(6), article 34, 2009.
- A. Langlois, D. Stehlé. *Worst-case to average-case reductions for module lattices.*
  Des. Codes Cryptogr. 75(3):565–599, 2015. (ePrint 2012/090.)
- M. R. Albrecht, R. Player, S. Scott. *On the concrete hardness of Learning with Errors.*
  J. Math. Cryptol. 9(3):169–203, 2015 (ePrint 2015/046); the lattice-estimator,
  `github.com/malb/lattice-estimator`.
- NIST. *FIPS 203* (ML-KEM), *FIPS 204* (ML-DSA), *FIPS 205* (SLH-DSA), August 2024
  — correctly-designed controls.

**Structure-induced breaks (the §5 taxonomy)**
- V. M. Sidelnikov, S. O. Shestakov. *On the insecurity of cryptosystems based on generalized
  Reed–Solomon codes.* Discrete Math. Appl. 2(4):439–444, 1992 (transl. of Diskretnaya
  Matematika 4(3), 1992).
- J.-C. Faugère, A. Otmani, L. Perret, J.-P. Tillich. *Algebraic Cryptanalysis of McEliece
  Variants with Compact Keys.* EUROCRYPT 2010, LNCS 6110, 279–298.
- A. Couvreur, I. Márquez-Corbella, R. Pellikaan. *A polynomial time attack against algebraic
  geometry code based public key cryptosystems.* ISIT 2014 (ePrint 2014/064).
- M. R. Albrecht, S. Bai, L. Ducas. *A subfield lattice attack on overstretched NTRU
  assumptions: cryptanalysis of some FHE and graded encoding schemes.* CRYPTO 2016
  (ePrint 2016/127).
- P. Kirchner, P.-A. Fouque. *Revisiting lattice attacks on overstretched NTRU parameters.*
  EUROCRYPT 2017.
- L. Ducas, W. van Woerden. *NTRU Fatigue: How Stretched is Overstretched?* ASIACRYPT 2021
  (ePrint 2021/999).
- P. Campbell, M. Groves, D. Shepherd. *Soliloquy: A Cautionary Tale.* ETSI 2nd Quantum-Safe
  Crypto Workshop, 2014.
- R. Cramer, L. Ducas, C. Peikert, O. Regev. *Recovering short generators of principal ideals
  in cyclotomic rings.* EUROCRYPT 2016 (ePrint 2015/313).
- W. Castryck, T. Decru. *An efficient key recovery attack on SIDH.* EUROCRYPT 2023
  (ePrint 2022/975).
- L. Maino, C. Martindale, L. Panny, G. Pope, B. Wesolowski. *A direct key recovery attack on
  SIDH.* EUROCRYPT 2023 (ePrint 2022/1026).
- D. Robert. *Breaking SIDH in polynomial time.* EUROCRYPT 2023 (ePrint 2022/1038).
- E. Kani. *The number of curves of genus two with elliptic differentials.* J. reine angew.
  Math. 485:93–121, 1997.

**Case study (author's own)**
- [Gifford 2026a] M. Gifford. *A rank collapse in a sedenion Module-LWE proposal, and why a
  uniform matrix does not repair it.* Zenodo, 2026. (Pin the current version DOI; v1 was
  10.5281/zenodo.23270249.)
- [Gifford 2026b] M. Gifford. *Fluid Lattice Topology: bridging PSL(2,7) vacuum geometry and
  non-associative post-quantum cryptography.* Zenodo, 2026 (v3 carries the withdrawal notice;
  10.5281/zenodo.20078312).
