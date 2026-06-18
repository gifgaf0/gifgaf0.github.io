# Proof sketch — the Cayley-Dickson ZD bridge realizes PG(n−1,2) at every doubling

**Status: PROVED unconditionally for n = 4…8** (the five computed doublings — every link
proved or exhaustively finitely verified), and **proved for all n ≥ 4 modulo one
classical input** (the nucleus of A_n is the base field, used only for "top-bit"
reduction pairs in the existence half). The former identity gap — G = associator
(Lemma 3) — is now closed symbolically: it reduces to *basis left-alternativity*
[eₓ,eₓ,e_w]=0, proved for all n by induction on the doubling with an elementary base
(n=1, ℂ), citing nothing external. The completeness property turned out to *be the
algebra's associator*: the bridge realizes PG(n−1,2) precisely because every
Cayley–Dickson algebra past the quaternions is non-associative. Machine certificates:
`verify_reduction.py`, `verify_associator.py`, `verify_alternative.py`,
`verify_induction.py`, `verify_existence.py`.

Throughout: field of characteristic ≠ 2; `^` is bitwise XOR; results reported as
found (no target consulted).

---

## 0. Setup and notation

The Cayley-Dickson algebra A_n (dim 2ⁿ) is the twisted group algebra of (ℤ/2)ⁿ:
for basis units i, j ≥ 0,
  e_i · e_j = σ_n(i,j) · e_{i^j},  σ_n(i,j) ∈ {+1,−1},
with σ_n(i,i) = −1 for i ≥ 1 (units square to −1) and σ_n(0,·)=σ_n(·,0)=1. The
"XOR property" e_i e_j = ±e_{i^j} is verified to hold in the project's build_cd_table
at every dimension used.

A **canonical two-term element** is x = s_a e_a + s_b e_b, a≠b, both ≥1, signs ±1.
A pair (x,y) is a **two-term canonical zero divisor (ZD)** if xy = 0.

**Doubling.** A_{n+1} = A_n ⊕ A_n ℓ, ℓ = e_D, D = 2ⁿ. Lower indices 0..D−1 are the
A_n subalgebra; upper indices are e_{D+k} = e_k ℓ (k = 0..D−1); call k the
**reduction** of D+k. From the CD product (a+bℓ)(c+dℓ) = (ac − d̄b) + (da + bc̄)ℓ and
τ(k) := (+1 if k=0 else −1), one gets the **cocycle recursion** (each line verified
against the table):

| product | σ_{n+1} | result index |
|---|---|---|
| lower·lower | σ_{n+1}(a,c) = σ_n(a,c) | a^c |
| lower·upper | σ_{n+1}(a, D+d) = σ_n(d,a) | D+(a^d) |
| upper·lower | σ_{n+1}(D+b, c) = τ(c) σ_n(b,c) | D+(b^c) |
| upper·upper | σ_{n+1}(D+b, D+d) = −τ(d) σ_n(d,b) | b^d  (lower) |

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

**Free-bit witness lemma (elementary, no nucleus theorem cited).** If a,b are distinct
nonzero with a,b < 2ᵏ (k ≤ n−1), then A(a,b,2ᵏ) = −1. *Proof:* all four index-pairs
in A(a,b,2ᵏ) lie in the subalgebra A_{k+1}, so we may use the cocycle recursion at the
doubling A_k → A_{k+1} (D=2ᵏ, generator e_D): σ(a⊕b,D)=σ_<(0,a⊕b)=1, σ(b,D)=1,
σ(a,b⊕D)=σ_<(b,a), σ(a,b)=σ_<(a,b); hence
A(a,b,2ᵏ) = σ_<(a,b)·1·1·σ_<(b,a) = σ_<(a,b)σ_<(b,a) = −1 by anticommutativity. ∎
(Verified, as predicate (W), in `verify_existence.py`.) Taking k=n−1, this **proves
(P_n′) outright for every pair whose two reductions are < 2ⁿ⁻¹** — the explicit
witness is the top generator e_{2ⁿ⁻¹}.

**Remaining pairs (a reduction uses the top bit).** Here no generator sits above both
units and there is no single closed-form witness (the associator has two regimes;
checked). (P_n′) still holds — it is exactly the standard fact that the nucleus of A_n
is the base field for n ≥ 3 (Schafer, *Intro. to Nonassociative Algebras*), so no
imaginary unit lies in a common associative subalgebra with everything. We have not
reduced this residual to a one-line elementary argument; it is **verified exhaustively
for n = 4…8**, where the witness count is exactly 2ⁿ⁻¹ > 0 for every pair (values
{2ⁿ⁻¹, 2ⁿ−4}, `verify_associator.py`). This is the single non-elementary input for
general n; everything else is proved for all n from scratch.

**Reading.** *The projective geometry of the bridge is the associator structure of
the algebra.* A PG(n−1,2) line {q₁,q₂,δ} is realized by the 64→128-style bridge **iff**
the corresponding imaginary units fail to associate with some third unit — which, by
non-associativity of every CD algebra past the quaternions, always holds. PG(2,2)
(Fano) for the octonions is the n=3 instance of the very same statement.

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
| (P_n′): ∃ non-associating p — pairs with both reductions < 2ⁿ⁻¹ | **proved all n** (free-bit lemma, elementary) |
| (P_n′): ∃ non-associating p — top-bit pairs | **proved n≤8** (exhaustive); general n = nucleus thm (Schafer), not re-derived |

**Bottom line.** Two scopes:

> **Theorem (unconditional, n = 4…8).** For each of the five computed doublings, the
> two-term canonical zero divisors split as two intact copies of A_n plus a bridge that
> realizes **exactly** PG(n−1,2) on the 2ⁿ−1 nonzero upper reductions — every line
> witnessed, none spurious, generator excluded — field-independently. Every link is
> proved or exhaustively finitely verified.

> **Theorem (general n ≥ 4, modulo one classical input).** The same holds at *every*
> Cayley–Dickson doubling, with a single non-elementary dependency: that for top-bit
> reduction pairs a non-associating unit exists — i.e. the nucleus of A_n is the base
> field (Schafer). All other ingredients — Lemma 1, Prop 2, soundness, point set,
> decomposition, Lemma 3 (G = associator) via basis left-alternativity, and the
> free-bit half of (P_n′) — are proved from scratch for all n.

The five computed levels PG(3,2)…PG(7,2) are unconditional instances. **Conceptual
content:** the bridge realizes PG(n−1,2) because, and exactly to the extent that, the
Cayley–Dickson algebra is non-associative — and the realization is *driven* by basis
left-alternativity, the last vestige of alternativity that survives past the octonions.
PG(2,2) (Fano, octonions) is the n=3 instance of the same statement.

*Companions: `verify_reduction.py` (Prop 2 vs brute; (P_n) on σ_n), `verify_associator.py`
(Lemma 3 + witness counts), `verify_alternative.py` (G=A ⇔ basis left-alt, n=4…8),
`verify_induction.py` (induction ingredients + L(n), n=1…9), `verify_existence.py`
(free-bit witness lemma (W)), `explore_Pn.py` (discovery). Other scripts per
VERIFICATION_REPORT.md.*
