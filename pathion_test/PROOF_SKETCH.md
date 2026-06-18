# Proof sketch — the Cayley-Dickson ZD bridge realizes PG(n−1,2) at every doubling

**Status: PROVED unconditionally for all n ≥ 3** (the doubling target being the
sedenions or higher — the first algebras with two-term ZDs; see threshold below), modulo
only standard, citable Cayley–Dickson structural facts (S0)–(S2). The novel content is
deductive and the six machine certificates (n=3…9) are **confirmatory, not load-bearing**
(D2 = case i). (1) the identity G = associator (Lemma 3)
reduces to *basis left-alternativity* [eₓ,eₓ,e_w]=0, proved for all n by induction on the
doubling with an elementary base (n=1, ℂ); (2) the existence half (every line has a
non-associating witness) is proved by an **explicit per-line witness** (three cases,
each a τ-product or an anticommutator equal to −1), replacing the nucleus theorem. The
completeness property turned out to *be the algebra's associator*: the bridge realizes
PG(n−1,2) precisely because every Cayley–Dickson algebra past the quaternions is
non-associative. Machine certificates: `verify_reduction.py`, `verify_associator.py`,
`verify_alternative.py`, `verify_induction.py`, `verify_existence.py`,
`verify_witness_complete.py`.

Throughout: field of characteristic ≠ 2; `^` is bitwise XOR; results reported as
found (no target consulted).

---

## Theorem (precise statement)

Let the field have characteristic ≠ 2. Consider the Cayley–Dickson doubling
A_n → A_{n+1} = A_n ⊕ A_n ℓ (dim A_{n+1} = 2ⁿ⁺¹), with D = 2ⁿ, and index every basis
unit of A_{n+1} by F₂ⁿ⁺¹; "upper" units are e_{D+k}=e_k ℓ with **reduction** k ∈ F₂ⁿ.

**Scope (in the statement, not a footnote).** "ZD" means a **two-term, ±1-coefficient,
canonical** zero divisor x·y=0 with x=s_a e_a+s_b e_b, y=s_c e_c+s_d e_d (a,b,c,d≥1).
Higher-term ZDs (n-term kernels) and non-±1 / non-canonical ZDs are **outside scope**:
the theorem is silent on them. **Threshold:** such ZDs exist iff dim A_{n+1} ≥ 16, i.e.
**n ≥ 3** (Hurwitz: ℝ,ℂ,ℍ,𝕆 are the only composition algebras, so the first algebra
with zero divisors is the sedenions A_4 = 16D — see B2). At n=3 the bridge is the entire
sedenion ZD set; n=3 ↦ PG(2,2) is therefore a genuine ZD instance, not a Fano analogy.

**Statement (set equality, A2).** For n ≥ 3:
1. the canonical two-term ZD pairs of A_{n+1} partition as (lower copy of A_n's ZDs) ⊔
   (upper copy) ⊔ (bridge = pairs whose two assessors each cross lower/upper);
2. define, for a bridge ZD {(p₁,D+q₁),(p₂,D+q₂)}, its **witnessed triple**
   {q₁,q₂,q₁⊕q₂} ⊂ F₂ⁿ. Then
   **{ witnessed triples } = { lines of PG(n−1,2) }**
   under the identification (nonzero reduction k) ↔ (point k of F₂ⁿ∖{0}); i.e. every
   projective line is witnessed (completeness), and every witnessed triple is a line
   (soundness, "nothing spurious"); and the doubling generator ℓ (reduction 0) appears
   in no bridge ZD (so the point set is exactly the 2ⁿ−1 points of PG(n−1,2)).

**Field scope (A4).** The criterion for a canonical pair to be a ZD is a finite set of
sign equations in σ ∈ {±1} (Prop 2); no prime or characteristic enters beyond char≠2.
Hence the F_911 / field-class checks were only ever **evidence for the empirical claim**
and are irrelevant to this theorem — it holds over every field of char ≠ 2.

---

## 0. Setup and notation

**Standard Cayley–Dickson facts** (Schafer, *An Introduction to Nonassociative
Algebras* 1966; Baez, *The Octonions* 2002), used as cited foundations, each provable
by induction on the doubling from the recurrence (a+bℓ)(c+dℓ) = (ac − d̄b, da + bc̄),
ē=conjugate:

- **(S0) Twisted-group structure / XOR property.** A_n (dim 2ⁿ over a field, char ≠ 2)
  has a basis {e_i}_{i∈F₂ⁿ} with e_i·e_j = σ_n(i,j)·e_{i⊕j}, σ_n(i,j) ∈ {+1,−1}; and
  σ_n(i,i)=−1 (i≠0), σ_n(0,·)=σ_n(·,0)=1. *Proof for all n:* induction — each of the
  four product cases below yields exactly one basis vector whose index is the XOR. ∎
- **(S1) Anticommutativity.** σ_n(i,j) = −σ_n(j,i) for distinct nonzero i,j (distinct
  imaginary units anticommute; ē_i=−e_i and conjugation is an antiautomorphism).
- **(S2) Flexibility.** (xy)x = x(yx); on basis units σ(i,j)σ(i⊕j,i)=σ(j,i)σ(i,i⊕j).
  *(Derivable from (S1): see verify_induction.py.)*

**Cocycle recursion (derived, not assumed).** For A_{n+1} = A_n ⊕ A_n ℓ, ℓ = e_D,
D = 2ⁿ, with e_{D+k}=e_k ℓ (call k the **reduction**) and τ(k):=(+1 if k=0 else −1),
the doubling formula gives, **for all n** (each line is the basis-level evaluation of
(a+bℓ)(c+dℓ), not a table lookup):

| product | σ_{n+1} | result index |
|---|---|---|
| lower·lower | σ_{n+1}(a,c) = σ_n(a,c) | a^c |
| lower·upper | σ_{n+1}(a, D+d) = σ_n(d,a) | D+(a^d) |
| upper·lower | σ_{n+1}(D+b, c) = τ(c) σ_n(b,c) | D+(b^c) |
| upper·upper | σ_{n+1}(D+b, D+d) = −τ(d) σ_n(d,b) | b^d  (lower) |

The build_cd_table verification (`verify_induction.py`, n=1…9) **confirms** (S0)–(S2)
and the recursion; it is not relied upon by the deductive chain.

A **canonical two-term element** is x = s_a e_a + s_b e_b, a≠b, both ≥1, signs ±1.
A pair (x,y) is a **two-term canonical zero divisor (ZD)** if xy = 0.

**Doubling decomposition.** Lower indices 0..D−1 are the A_n subalgebra; upper indices
are the e_k ℓ.

---

## 1. The completeness lemma (which quadruples can be ZDs)

**Lemma 1.** If xy = 0 (x,y canonical two-term, indices a,b / c,d) then the index
sets are **disjoint** and **a^b^c^d = 0**.

*Proof.* xy = Σ s_·s_· σ(·,·) e_{·^·} over the four cross terms. If two indices
coincide (say a=c) then e_{a^c}=e_0=1 appears alone with coefficient −s_a s_c ≠ 0
(the case a=c, b=d is excluded as {a,b}={c,d}), so xy≠0 ⇒ indices disjoint. With
disjoint indices the four product-indices a^c, a^d, b^c, b^d are nonzero; two of them
coincide **iff** a^b^c^d = 0 (all other coincidences force a repeated index). If
a^b^c^d ≠ 0 the four terms are independent and xy ≠ 0. ∎

So every ZD has a well-defined difference δ := a^b = c^d, and the product collapses
to two terms whose vanishing is a pair of **sign equations** in the σ-values. This is
exactly why "every ZD quadruple has index-XOR = 0" at all five computed levels — it
is forced, not incidental.

---

## 2. The bridge, reduced to one cocycle condition (the core, machine-verified)

Take the doubling A_n → A_{n+1}. A **crossing (bridge) assessor** is (p, D+q),
p ∈ {1..D−1} lower, q a reduction. A bridge ZD pair is {(p₁,D+q₁),(p₂,D+q₂)}.
Computing the product with the recursion of §0:

- **Lower part** vanishes ⇒ difference-lock **p₁^p₂ = q₁^q₂ (=:δ)** and
  s_a s_c σ_n(p₁,p₂) + t_a t_c σ_n(q₂,q₁) = 0. … (L)
- **Upper part** vanishes ⇒ same δ and
  s_a t_c σ_n(q₂,p₁) − t_a s_c σ_n(q₁,p₂) = 0. … (U)

Eliminating the four signs (set s_a=1; solve (L) for s_c, substitute in (U)) gives a
single consistency condition, **independent of the signs and of the prime**:

> **(†)  σ_n(q₂,p₁) = − σ_n(p₁,p₂) · σ_n(q₂,q₁) · σ_n(q₁,p₂).**

**Proposition 2 (reduction).** For nonzero reductions, a bridge pair is a ZD **iff**
difference-lock holds **and** (†) holds. Every term in (†) is a value of the
**level-n** cocycle σ_n.

**Machine verification (`verify_reduction.py`, part B).** At the doubling A₄→A₅ (32D),
the set of bridge ZDs computed by honest brute force and the set computed by
"difference-lock ∧ (†)" are **identical: 924 = 924**. (Brute also shows the generator
e_D lies in **0** crossing ZDs — see §4.) The reduction's algebra is therefore
confirmed, not merely asserted.

---

## 3. Soundness — no spurious lines (fully proved)

A bridge ZD {(p₁,D+q₁),(p₂,D+q₂)} witnesses the triple {q₁, q₂, q₁^q₂}. By
construction its three entries are the two reductions and their XOR; with q₁≠q₂ both
nonzero, q₁^q₂ ≠ 0 and the three are distinct. Hence **every witnessed triple is, by
definition, an XOR-zero triple of nonzero F₂ⁿ vectors — a line of PG(n−1,2).** No
spurious triple can ever be produced. This alone explains "nothing spurious" at all
five levels with zero computation. ∎

---

## 4. The point set is exactly PG(n−1,2) — generator excluded (proved + verified)

Points are the nonzero reductions, i.e. F₂ⁿ \ {0} = the 2ⁿ−1 points of PG(n−1,2).
The generator e_D (reduction 0) is **excluded**: setting a reduction to 0 flips τ(0)=+1
in (L)/(U), which makes the two sign equations inconsistent, so **e_D belongs to no
crossing ZD.** Verified: at 32D the brute count of generator-involving crossing ZDs
is **0**, and across all five runs exactly 2ⁿ−1 of 2ⁿ reductions participate (15/16,
31/32, 63/64, 127/128, 255/256). ∎

---

## 5. Decomposition total(n+1) = 2·total(n) + bridge (proved)

- **Lower copy.** A_n ↪ A_{n+1} is a subalgebra (σ unchanged, §0), so its total(n)
  ZD pairs persist verbatim.
- **Upper copy.** From σ_{n+1}(D+b,D+d) = −τ(d) σ_n(d,b), two purely-upper units
  multiply to σ-mirror the lower product; the ZD sign-equations for purely-upper
  pairs are in bijection with the lower ones, giving the **same** count total(n).
- **Bridge.** everything else.

This reproduces the observed 84→1260→13020→117180→992124→8161020, each = 2×previous +
bridge (bridges 1092, 10500, 91140, 757764, 6176772). ∎

---

## 6. Completeness = the algebra's associator (the punchline)

What remains for "**all** lines witnessed" is existence of a witness per line:

> **(P_n).** For all distinct nonzero q₁,q₂ ∈ F₂ⁿ (δ=q₁^q₂), there exists nonzero
> p ∉ {0,δ} (p₁=p, p₂=p^δ) satisfying (†):
>   σ_n(q₂,p)·σ_n(p,p^δ)·σ_n(q₁,p^δ) = − σ_n(q₂,q₁),
> i.e. **G(p) := σ_n(q₂,p)σ_n(p,p^δ)σ_n(q₁,p^δ)σ_n(q₂,q₁) = −1.**

**Lemma 3 (the witness sign IS the associator).** For all distinct nonzero q₁,q₂ and
all valid p,
  **G(p) = A(q₁, q₂, p),**
the associator sign A(i,j,k) := σ(i,j)σ(i^j,k)σ(j,k)σ(i,j^k) defined by
(e_i e_j)e_k = A(i,j,k)· e_i(e_j e_k). **Proved for all n** (below); also verified
exhaustively (`verify_associator.py`) at n = 4…8.

*Proof.* Cancel the common factor σ(q₂,p) from G = A; apply anticommutativity
σ(q₂,q₁) = −σ(q₁,q₂); substitute w := p^δ and a := q₁ (so q₂^p = a^w, δ = p^w). Every
step is a sign identity over {±1}; the identity collapses (verified line-by-line in
`verify_alternative.py`) to
  **F(p) = F(a),  where F(x) := σ(x,w)·σ(x, x^w).**
Now F(x) = −A(x,x,w): indeed e_x(e_x e_w) = σ(x,w)σ(x,x^w) e_w = F(x) e_w while
(e_x e_x)e_w = −e_w, so A(x,x,w) = −e_w /(F(x)e_w) = −F(x). Hence

> **G = A  ⇔  A(x,x,w) is independent of x  ⇐  basis left-alternativity
> [eₓ,eₓ,e_w] = 0, i.e. e_x(e_x e_w) = −e_w.**

**Lemma 3a (basis left-alternativity, all n).** In every A_n, e_x(e_x e_w) = −e_w for
all basis units (x ≠ 0). *Note this is strictly weaker than alternativity, which fails
for n ≥ 4 — it holds only because both arguments are basis units.*

*Proof by induction on the doubling A_n → A_{n+1}* (D = 2ⁿ, e_{D+a} = e_a ℓ; write
η(a)=+1 if a=0 else −1, conjugate ē_a = η(a)e_a). **Base n = 1 (ℂ), direct** (no
alternativity cited): the only nonzero unit is e₁ with e₁²=−1; for w∈{0,1},
e₁(e₁e_w) = e₁·(e₁e_w) computes to −e_w in both cases. (One may equally base at n=2,3
where the algebra is associative/alternative.) Three facts, *all derivable from
anticommutativity on basis units alone* (checked in `verify_induction.py`):
(i) anticommutativity;
(ii) conjugation is an antiautomorphism, \overline{e_a e_b} = ē_b ē_a; (iii) flexibility
(e_g e_h)e_g = e_g(e_h e_g). From L(n)+(i)–(iii) one gets the right form
R(n): (e_h e_g)e_g = −e_h (via (e_h e_g)e_g = −(e_g e_h)e_g = −e_g(e_h e_g) =
e_g(e_g e_h) = −e_h). **Inductive step**, using (u,v)(u',v') = (uu' − v̄'v, v'u + v ū'):

- *E,F lower* — inside A_n, holds by L(n).
- *E=e_g lower, F=e_h ℓ:* e_E e_F = (e_h e_g)ℓ, so e_E(e_E e_F) = ((e_h e_g)e_g)ℓ =
  (−e_h)ℓ = −e_F by R(n).
- *E=e_g ℓ, F=e_h lower:* e_E e_F = (e_g ē_h)ℓ, then e_E(e_E e_F) =
  −\overline{(e_g ē_h)}e_g = −(e_h ē_g)e_g = (e_h e_g)e_g = −e_h = −e_F (antiauto. + R(n)).
- *E=e_g ℓ, F=e_h ℓ:* with c = −ē_h e_g, e_E e_F = (c,0) and e_E(e_E e_F) = (0, e_g c̄);
  c̄ = −ē_g e_h, so e_g c̄ = −η(g) e_g(e_g e_h) = η(g)e_h = −e_h (g≠0), giving −e_F.
  (g=0, E=ℓ, is direct.)

All four cases give e_E(e_E e_F) = −e_F, so L(n+1) holds. ∎ Therefore F(x) ≡ −1,
F(p)=F(a), and **G = A for all n.** ∎

With Lemma 3, **(P_n) becomes a pure non-associativity statement:**

> **(P_n′).** For every two distinct nonzero imaginary units e_{q₁}, e_{q₂} there is a
> unit e_p with which they **fail to associate** (A(q₁,q₂,p) = −1).

**(P_n′) is proved elementarily for all n** — by an explicit witness per line, with no
nucleus theorem and no residual. Completeness needs only that each *line* be witnessed
(a bridge ZD on any pair of its points realizes the whole triple), so for each line we
pick the most convenient pair. Set t := 2ⁿ⁻¹. Each line has 0 or 2 "upper" points
(reductions ≥ t), since the top bit of δ=q₁⊕q₂ is the XOR of the top bits of q₁,q₂.

- **0 upper points** (all three < t): take a lower pair (x,y), witness **p = t**. All
  four index-pairs of A(x,y,t) lie in A_n's subalgebra A_{(log t)+1}, where the cocycle
  recursion gives σ(x⊕y,t)=σ(t,y)=1 and σ(x,y⊕t)=σ(y,x); so
  **A(x,y,t) = σ(x,y)σ(y,x) = −1** (anticommutativity).
- **2 upper points** u₁=t+r₁, u₂=t+r₂ (r₁≠r₂): take the pair (u₁,u₂).
   - *both r₁,r₂ ≠ 0* — witness **p = r₁** (lower). The recursion collapses the σ-factors
     to 1 and leaves **A(u₁,u₂,r₁) = τ(r₁)τ(r₂)τ(r₁⊕r₂) = (−1)³ = −1** (all three
     nonzero), where τ(x)=−1 for x≠0.
   - *one reduction is 0* (the line passes through t; say u₂=t, r₁≠0) — witness **p =**
     any lower index in {1,…,t−1}\{r₁} (nonempty for t ≥ 3, i.e. n ≥ 3). The recursion
     gives **A(t+r₁, t, p) = σ(r₁,p)σ(p,r₁) = −1**.

These cases are exhaustive, so **every PG(n−1,2) line is witnessed, for all n ≥ 3.** The
three closed-form associator values are derived from the cocycle recursion and certified
against the multiplication table for n=3…8; the witness rule is certified to produce
A=−1 on all 7…43 435 lines for n=3…9 (`verify_witness_complete.py`). The earlier
free-bit lemma is the 0-upper case; the nucleus theorem is no longer needed.

**Reading.** *The projective geometry of the bridge is the associator structure of
the algebra.* A PG(n−1,2) line {q₁,q₂,δ} is realized by the 64→128-style bridge **iff**
the corresponding imaginary units fail to associate with some third unit — which, by
non-associativity of every CD algebra past the quaternions, always holds. PG(2,2)
(Fano) is the n=3 instance — realized by the 84 sedenion zero divisors (all of which
are bridge, since octonions have none), witnessing all 7 Fano lines (verified).

---

## 7. What is proved vs. open

| component | status |
|---|---|
| ZD ⇒ disjoint indices ∧ XOR=0 (Lemma 1) | **proved** (all n) |
| bridge ZD ⇔ difference-lock ∧ (†) (Prop 2) | **proved** (all n) + verified (924=924) |
| soundness: no spurious lines | **proved** (all n) |
| point set = PG(n−1,2); generator excluded | **proved** (all n) + verified |
| total(n+1) = 2·total(n) + bridge | **proved** (all n) |
| completeness ⇔ (P_n) | **proved** (reduction, all n) |
| Lemma 3: G(p) = associator A(q₁,q₂,p) | **proved** (all n, via Lemma 3a) + verified n=4…8 |
| Lemma 3a: basis left-alternativity | **proved all n** (induction, base n=1) + verified n=1…9 |
| (P_n′)/completeness: every line witnessed | **proved all n** (explicit per-line witness, 3 cases) + verified n=3…9 |

**Bottom line — unconditional theorem, all n, self-contained.** Every row is proved from
scratch for all n, citing nothing external (the former two dependencies — octonion
alternativity and the nucleus theorem — are both eliminated):

> **Theorem.** For every Cayley–Dickson doubling A_n → A_{n+1} (n ≥ 3) over a field of
> characteristic ≠ 2, the two-term ±1-canonical zero divisors split as two intact copies
> of A_n's ZDs plus a bridge, and the bridge realizes **exactly** PG(n−1,2) on the 2ⁿ−1
> nonzero upper reductions: every projective line is witnessed, no non-line is, and the
> doubling generator is excluded. The criterion is a sign condition, so the result is
> independent of the field (any characteristic ≠ 2).

The computed levels PG(2,2)…PG(7,2) (sedenions through 512D) are instances; the proof
covers them and every higher doubling at once.

**Conceptual content — two distinct facts at two distinct thresholds (B2).**
*(i) Why the object exists at all:* two-term ZDs require the loss of the composition
(normed-division) property, which by Hurwitz happens first at the **sedenions** (A_4,
the n=3 doubling). This is the **Hurwitz threshold**, and it — not non-associativity —
is why n=3 is the first level; for n<3 (the doubling target being ℍ, ℂ, ℝ) there are no
ZDs and the theorem is vacuously silent (A3).
*(ii) Why the ZDs are organized as PG(n−1,2):* the **associator**. Non-associativity
appears earlier, at the octonions (A_3), and is the *structuring* mechanism: soundness
is forced by basis left-alternativity (Lemma 3a — the vestige of alternativity that
*survives* past the octonions, making G=A; B1), and completeness by an explicit
non-associating witness on every line (§"existence"). These are independent of (i):
non-associativity organizes ZDs once they exist, but does not create them (octonions are
non-associative yet division). Both facts are load-bearing, neither is decoration.
PG(2,2) (Fano) at n=3 is a genuine ZD instance (the 84 sedenion ZDs, all bridge, witness
all 7 Fano lines — verified), not a Fano analogy.

*Companions: `verify_reduction.py` (Prop 2 vs brute; (P_n) on σ_n), `verify_associator.py`
(Lemma 3 + witness counts), `verify_alternative.py` (G=A ⇔ basis left-alt, n=4…8),
`verify_induction.py` (induction ingredients + L(n), n=1…9), `verify_existence.py`
(free-bit witness lemma), `verify_witness_complete.py` (complete per-line witness rule
+ closed-form associator values, n=3…9), `explore_Pn.py` (discovery). Other scripts per
VERIFICATION_REPORT.md.*
