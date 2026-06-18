# Longhand sign-derivations — referee-proof backbone

Purpose: discharge by hand, with **every ±1 tracked**, the compact steps in
`PROOF_SKETCH.md` whose sign-arithmetic was previously confirmed only by the machine
certificates. After this document, no step's *correctness* (not just logical structure)
relies on computation. For line-by-line review.

Conventions (fixed once):
- A_{m} = A_{m-1} ⊕ A_{m-1}ℓ, ℓ=e_{D'}, **D' = 2^{m-1}**. Element (u,v) := u + vℓ.
- **Doubling product:** (u₁,v₁)(u₂,v₂) = (u₁u₂ − v̄₂v₁, v₂u₁ + v₁ū₂).
- **Conjugation:** (u,v)‾ = (ū, −v); on basis ē_a = τ(a)e_a, τ(0)=+1, τ(a)=−1 (a≠0).
- e_i e_j = σ(i,j) e_{i⊕j}; lower index a is (e_a,0); upper index D'+s is (0,e_s),
  s the **reduction**. `^`=⊕=XOR.

---

## 0. Cocycle recursion — derived from the product (not a table lookup)

Evaluate each basis-pair product with the doubling formula.

**(R1) lower·lower:** (e_a,0)(e_c,0) = (e_a e_c − 0, 0) = (σ(a,c)e_{a⊕c}, 0).
⟹ σ_m(a,c)=σ_{m-1}(a,c), index a⊕c.

**(R2) lower·upper:** (e_a,0)(0,e_d): u₁=e_a,v₁=0,u₂=0,v₂=e_d.
= (e_a·0 − ē_d·0, e_d e_a + 0) = (0, e_d e_a) = (0, σ(d,a)e_{d⊕a}).
⟹ σ_m(a, D'+d) = σ_{m-1}(d,a), index D'+(a⊕d).

**(R3) upper·lower:** (0,e_b)(e_c,0): u₁=0,v₁=e_b,u₂=e_c,v₂=0.
= (0 − 0, 0 + e_b ē_c) = (0, e_b ē_c) = (0, τ(c)e_b e_c) = (0, τ(c)σ(b,c)e_{b⊕c}).
⟹ σ_m(D'+b, c) = τ(c)σ_{m-1}(b,c), index D'+(b⊕c).

**(R4) upper·upper:** (0,e_b)(0,e_d): u₁=0,v₁=e_b,u₂=0,v₂=e_d.
= (0 − ē_d e_b, 0) = (−τ(d)e_d e_b, 0) = (−τ(d)σ(d,b)e_{d⊕b}, 0).
⟹ σ_m(D'+b, D'+d) = −τ(d)σ_{m-1}(d,b), index (b⊕d) lower.

These four lines are exact; they hold for every m (the formula is general). The XOR
property (S0) is immediate: each case yields a single basis vector at the XOR index;
induction on m gives it for all dimensions.

---

## 1. Anticommutativity (S1): σ_m(i,j) = −σ_m(j,i), i≠j nonzero — by induction

Base: A_2=ℍ (quaternions, associative): i,j∈{1,2,3} distinct anticommute (direct).
Step, assume in A_{m-1}; take distinct nonzero i,j in F₂^m, split by top (D') bit:

- **both lower:** σ_m(i,j)=σ_{m-1}(i,j) = −σ_{m-1}(j,i) = −σ_m(j,i). ✓ [IH]
- **i lower (i≠0), j=D'+d upper:** σ_m(i,D'+d)=σ_{m-1}(d,i) by (R2);
  σ_m(D'+d,i)=τ(i)σ_{m-1}(d,i) by (R3). Since i≠0, τ(i)=−1, so the second is
  −σ_{m-1}(d,i) = −σ_m(i,D'+d). ✓ (Includes d=0, j=ℓ: σ_m(i,D')=σ_{m-1}(0,i)=1,
  σ_m(D',i)=τ(i)·1=−1.)
- **both upper, i=D'+b, j=D'+d (b≠d):** σ_m(i,j)=−τ(d)σ_{m-1}(d,b),
  σ_m(j,i)=−τ(b)σ_{m-1}(b,d), by (R4). If b,d both ≠0: σ_{m-1}(d,b)=−σ_{m-1}(b,d) [IH],
  τ(b)=τ(d)=−1, so σ_m(i,j)=−(−1)σ_{m-1}(d,b)=σ_{m-1}(d,b)=−σ_{m-1}(b,d), and
  −σ_m(j,i)=τ(b)σ_{m-1}(b,d)=−σ_{m-1}(b,d). Equal. ✓ If b=0 (i=ℓ), d≠0:
  σ_m(i,j)=−τ(d)σ_{m-1}(d,0)=−(−1)(1)=1; σ_m(j,i)=−τ(0)σ_{m-1}(0,d)=−(1)(1)=−1;
  1=−(−1). ✓ ∎

---

## 2. Flexibility (S2) on basis: σ(i,j)σ(i⊕j,i) = σ(j,i)σ(i,j⊕i) — from (S1) alone

(e_i e_j)e_i has sign σ(i,j)σ(i⊕j,i); e_i(e_j e_i) has sign σ(j,i)σ(i,j⊕i); both at
index j. By (S1): σ(i⊕j,i)=−σ(i,i⊕j) and σ(j,i)=−σ(i,j) (i,j distinct nonzero), so
RHS = (−σ(i,j))σ(i,j⊕i) = −σ(i,j)σ(i,i⊕j) = σ(i,j)(−σ(i,i⊕j)) = σ(i,j)σ(i⊕j,i) = LHS.
∎ (Degenerate i=j or 0: both sides equal trivially.)

---

## 3. Basis left-alternativity (Lemma 3a): e_E(e_E e_F) = −e_F (E≠0), all m

Write L(m) for this statement, R(m) for (e_F e_E)e_E = −e_F.

**R from L (same level):** F=E: (e_E e_E)e_E=(−1)e_E=−e_E. F=0: (1·e_E)e_E=−1=−e_F.
E,F distinct nonzero: (e_F e_E)e_E = (−e_E e_F)e_E [S1] = −(e_E e_F)e_E = −e_E(e_F e_E)
[S2] = −e_E(−e_E e_F) [S1] = e_E(e_E e_F) = −e_F [L(m)]. ∎

**Base L(1)=ℂ:** E=e₁ (only nonzero); F=e₀: e₁(e₁e₀)=e₁e₁=−1=−e₀. F=e₁:
e₁(e₁e₁)=e₁(−1)=−e₁. ✓

**Step L(m−1) ⟹ L(m).** D'=2^{m-1}. Four cases (g,h are reductions; verify each ±):

**(C1) E=(e_g,0), F=(e_h,0), g≠0.** e_E e_F=(e_g e_h,0). 
e_E(e_E e_F)=(e_g,0)(e_g e_h,0)=(e_g(e_g e_h),0)=(−e_h,0)=−e_F. [L(m−1)] ✓

**(C2) E=(e_g,0), F=(0,e_h), g≠0.** e_E e_F=(e_g,0)(0,e_h)=(0, e_h e_g) [as (R2)-shape].
e_E(e_E e_F)=(e_g,0)(0,e_h e_g)=(0, (e_h e_g)e_g)=(0,−e_h)=−e_F. [R(m−1)] ✓

**(C3) E=(0,e_g), F=(e_h,0).** e_E e_F=(0,e_g)(e_h,0)=(0, e_g ē_h).
e_E(e_E e_F)=(0,e_g)(0, e_g ē_h)=( −(e_g ē_h)‾ e_g, 0).
(e_g ē_h)‾ = (ē_h)‾(e_g)‾ = e_h ē_g [antiautomorphism; (ē_h)‾=e_h]. So first entry
= −(e_h ē_g)e_g = −τ(g)(e_h e_g)e_g = −τ(g)(−e_h) [R(m−1)] = τ(g)e_h.
g≠0 ⟹ τ(g)=−1 ⟹ = −e_h, giving (−e_h,0)=−e_F. ✓
g=0 (E=ℓ): e_E e_F=(0,ē_h)=(0,τ(h)e_h); e_E(e_E e_F)=(0,e₀)(0,τ(h)e_h)=(−τ(h)ē_h,0)
=(−τ(h)²e_h,0)=(−e_h,0)=−e_F. ✓

**(C4) E=(0,e_g), F=(0,e_h).** e_E e_F=(0,e_g)(0,e_h)=(−ē_h e_g, 0) =: (c,0), c=−ē_h e_g.
e_E(e_E e_F)=(0,e_g)(c,0)=(0, e_g c̄). c̄ = (−ē_h e_g)‾ = −(e_g)‾(ē_h)‾ = −ē_g e_h.
e_g c̄ = e_g(−ē_g e_h) = −τ(g)e_g(e_g e_h) = −τ(g)(−e_h) [L(m−1)] = τ(g)e_h.
g≠0 ⟹ = −e_h ⟹ (0,−e_h)=−e_F. ✓
g=0 (E=ℓ): e_E e_F=(−ē_h,0)=(−τ(h)e_h,0); e_E(e_E e_F)=(0,e₀)(−τ(h)e_h,0)
=(0, e₀·(−τ(h)e_h)‾)=(0,−τ(h)ē_h)=(0,−τ(h)²e_h)=(0,−e_h)=−e_F. ✓

All four (and g=0 subcases) give −e_F. L(m) holds. ∎ By induction, L(m) ∀ m≥1.

---

## 4. G = associator (Lemma 3): reduction to basis left-alternativity

G(p) := σ(q₂,p)σ(p,p⊕δ)σ(q₁,p⊕δ)σ(q₂,q₁), δ:=q₁⊕q₂;
A(q₁,q₂,p) := σ(q₁,q₂)σ(δ,p)σ(q₂,p)σ(q₁,q₂⊕p).
Claim G(p)=A(q₁,q₂,p). Both contain σ(q₂,p); cancel it. Remaining:
  σ(p,p⊕δ)σ(q₁,p⊕δ)σ(q₂,q₁) = σ(q₁,q₂)σ(δ,p)σ(q₁,q₂⊕p).
(S1): σ(q₂,q₁)=−σ(q₁,q₂); substitute and cancel σ(q₁,q₂) (=±1) from both sides:
  −σ(p,p⊕δ)σ(q₁,p⊕δ) = σ(δ,p)σ(q₁,q₂⊕p).
Put w:=p⊕δ (so δ=p⊕w, p⊕δ=w), a:=q₁; then q₂⊕p = (q₁⊕δ)⊕p = q₁⊕(δ⊕p) = a⊕w, and
δ=p⊕w. The equation becomes
  −σ(p,w)σ(a,w) = σ(p⊕w,p)σ(a,a⊕w).
(S1): σ(p⊕w,p) = −σ(p,p⊕w). So RHS = −σ(p,p⊕w)σ(a,a⊕w), and the equation is
  σ(p,w)σ(a,w) = σ(p,p⊕w)σ(a,a⊕w),  i.e.  **F(p)=F(a)**, F(x):=σ(x,w)σ(x,x⊕w).
Finally F(x) = −A(x,x,w):
A(x,x,w)=σ(x,x)σ(x⊕x,w)σ(x,w)σ(x,x⊕w)=(−1)(σ(0,w))σ(x,w)σ(x,x⊕w)=−σ(x,w)σ(x,x⊕w)=−F(x).
By §3, L(m): e_x(e_x e_w)=−e_w = (e_x e_x)e_w, i.e. the associator [e_x,e_x,e_w]=0, i.e.
A(x,x,w)=+1. Hence F(x)=−1 for every x, so F(p)=F(a)=−1, and G(p)=A(q₁,q₂,p). ∎

---

## 5. The three completeness witnesses (σ-collapse), every sign tracked

Work in A_m, t:=2^{m-1}, recursion A_{m-1}→A_m. Reductions/points in F₂^m. Each line of
PG(m−1,2) is witnessed by an explicit pair+p with A = −1.

**(W1) line with 0 upper points: pair (x,y) lower, p=t.** (x,y<t distinct nonzero.)
A(x,y,t) = σ(x,y)·σ(x⊕y,t)·σ(y,t)·σ(x,y⊕t).
- σ(x,y)=σ_{m-1}(x,y) [R1].
- σ(x⊕y,t)=σ(x⊕y, t+0)=σ_{m-1}(0,x⊕y)=1 [R2, d=0].
- σ(y,t)=σ_{m-1}(0,y)=1 [R2, d=0].
- σ(x,y⊕t)=σ(x, t+y)=σ_{m-1}(y,x) [R2, d=y; y⊕t=t+y as y<t].
⟹ A = σ_{m-1}(x,y)·1·1·σ_{m-1}(y,x) = σ_{m-1}(x,y)σ_{m-1}(y,x) = **−1** [S1, x≠y nonzero].

**(W2) line with 2 upper points, both reductions nonzero: pair (t+r₁,t+r₂), p=r₁.**
(r₁≠r₂, r₁,r₂≠0.) i=t+r₁, j=t+r₂, k=r₁; i⊕j=r₁⊕r₂, j⊕k=t+(r₂⊕r₁).
A = σ(i,j)·σ(i⊕j,k)·σ(j,k)·σ(i,j⊕k):
- σ(i,j)=σ(t+r₁,t+r₂) = −τ(r₂)σ_{m-1}(r₂,r₁) [R4].
- σ(i⊕j,k)=σ(r₁⊕r₂, r₁)=σ_{m-1}(r₁⊕r₂,r₁) [R1].
- σ(j,k)=σ(t+r₂, r₁)=τ(r₁)σ_{m-1}(r₂,r₁) [R3].
- σ(i,j⊕k)=σ(t+r₁, t+(r₂⊕r₁)) = −τ(r₂⊕r₁)σ_{m-1}(r₂⊕r₁,r₁) [R4].
Collect signs: (−τ(r₂))·(τ(r₁))·(−τ(r₂⊕r₁)) = τ(r₁)τ(r₂)τ(r₁⊕r₂) [two minuses cancel;
r₂⊕r₁=r₁⊕r₂]. Collect σ's: σ(r₂,r₁)·σ(r₁⊕r₂,r₁)·σ(r₂,r₁)·σ(r₂⊕r₁,r₁)
= σ(r₂,r₁)²·σ(r₁⊕r₂,r₁)² = 1·1 = 1. ⟹ A = τ(r₁)τ(r₂)τ(r₁⊕r₂) = (−1)(−1)(−1) = **−1**
[r₁,r₂,r₁⊕r₂ all nonzero].

**(W3) line through t (one reduction 0): pair (t+r₁, t), p any lower ∉{0,r₁}.** (r₁≠0.)
i=t+r₁, j=t (=t+0), k=p; i⊕j=r₁, j⊕k=t+p.
- σ(i,j)=σ(t+r₁,t+0) = −τ(0)σ_{m-1}(0,r₁) = −(1)(1) = −1 [R4].
- σ(i⊕j,k)=σ(r₁,p)=σ_{m-1}(r₁,p) [R1].
- σ(j,k)=σ(t,p)=σ(t+0,p)=τ(p)σ_{m-1}(0,p)=τ(p) [R3].
- σ(i,j⊕k)=σ(t+r₁,t+p) = −τ(p)σ_{m-1}(p,r₁) [R4].
⟹ A = (−1)·σ(r₁,p)·τ(p)·(−τ(p)σ(p,r₁)) = (−1)(−1)τ(p)²·σ(r₁,p)σ(p,r₁)
= σ_{m-1}(r₁,p)σ_{m-1}(p,r₁) = **−1** [S1, p≠r₁ nonzero].

Every line of PG(m−1,2) falls in exactly one of (W1)–(W3) (a line has 0 or 2 upper
points; if 2, either both reductions nonzero or one is 0), so every line is witnessed
with an explicitly **−1** associator. ∎

---

## Status after this document
Sections 0–5 discharge by hand every sign-bearing step that the certificates had
been confirming: the recursion (0), (S1)/(S2) (1–2), the four-case alternativity
induction (3), the G=A reduction (4), and the three completeness σ-collapses (5).
Combined with Lemma 1 (already longhand in PROOF_SKETCH §1), Prop 2's product
computation, soundness, and generator-exclusion, the chain is referee-checkable with no
appeal to the machine certificates. The certificates (n=3…9) now stand purely as an
independent cross-check.

*For the SQT agent: requesting line-by-line on §§0–5, especially the sign collections in
(W2)/(W3) and cases (C3)/(C4).*
