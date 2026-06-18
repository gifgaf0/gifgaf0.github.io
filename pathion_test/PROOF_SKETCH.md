# Proof sketch — the Cayley-Dickson ZD bridge realizes PG(n−1,2) at every doubling

**Status:** soundness, structure, the generator-exclusion, and the *reduction* of
the whole theorem to a single cocycle property are **proved and machine-verified**
(`verify_reduction.py`). The one remaining link — property (P_n), the cocycle
non-degeneracy that gives completeness — is **proved in the principal inductive case
and confirmed computationally for n = 4…8** (the 32→512D runs); a fully general
proof of its boundary cases is the open completion. Honest bottom line: this turns
"5 computed levels" into "one clean lemma away from a theorem for all levels."

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

## 6. Completeness ⇔ property (P_n), with the inductive step

What remains for "**all** 2ⁿ⁻¹·(2ⁿ−1)/3 lines witnessed" is existence of a witness
for each line:

> **(P_n).** For all distinct nonzero q₁,q₂ ∈ F₂ⁿ (δ=q₁^q₂), there exists nonzero
> p ∉ {0,δ} (p₁=p, p₂=p^δ) satisfying (†):
>   σ_n(q₂,p)·σ_n(p,p^δ)·σ_n(q₁,p^δ) = − σ_n(q₂,q₁).

**Verified for n = 4,5,6,7 directly on σ_n** (`verify_reduction.py`, part C: 35/35,
155/155, 651/651, 2667/2667 lines witnessed via (†)), and for **n = 8** by the 512D
realization run. (P_n) is the exact and only remaining content.

**Inductive step — principal case (proved).** Assume (P_n). In (P_{n+1}) take q₁,q₂
both in the **lower copy** (q₁,q₂ < D); then δ < D, choose p < D, and by the
lower·lower line of the recursion **every σ_{n+1} in (†) equals σ_n**, so the
condition is literally (P_n) for the same q₁,q₂ — a witness exists by hypothesis. ∎
(case closed)

**Remaining cases.** When q₁,q₂ are both upper, or mixed, choosing p upper turns (†)
into an analogous **existence-of-witness condition at level n** (the τ-signs from the
recursion are even and cancel, e.g. the upper-upper case asks for r with
σ_n(r,b)σ_n(r^δ,r)σ_n(r^δ,a) = −σ_n(a,b)). These are the same *type* of cocycle
non-degeneracy as (P_n) but not literally (P_n); they hold for n=4…8 (the runs) and
are the open part of the induction. The CD recursion makes each a finite, decidable
σ_n-statement, which is why the computation can and does discharge them level by
level.

---

## 7. What is proved vs. open

| component | status |
|---|---|
| ZD ⇒ disjoint indices ∧ XOR=0 (Lemma 1) | **proved** |
| bridge ZD ⇔ difference-lock ∧ (†) (Prop 2) | **proved + machine-verified (924=924)** |
| soundness: no spurious lines | **proved** |
| point set = PG(n−1,2); generator excluded | **proved + verified (gen in 0 ZDs)** |
| total(n+1) = 2·total(n) + bridge | **proved** |
| completeness ⇔ (P_n) | **proved** (reduction) |
| (P_n) — lower-lower inductive case | **proved** |
| (P_n) — full, all cases, all n | **open**; verified n=4…8 |

**Reading.** The realization PG(2,2)→PG(3,2)→…→PG(7,2) is not a numerical
coincidence: it is forced by Lemma 1 (XOR law), is sound by construction (no spurious
lines, ever), and is complete iff the single cocycle property (P_n) holds — which is
proved in its principal case and reduces in all cases to finite σ_n-identities,
confirmed through n=8. A general proof of (P_n)'s boundary cases would upgrade the
five-level R1 result to a theorem valid at **every** Cayley-Dickson doubling.

*Companion: `verify_reduction.py` (validates Prop 2 against brute force and checks
(P_n) on σ_n for n=4…7). All other scripts as in VERIFICATION_REPORT.md.*
