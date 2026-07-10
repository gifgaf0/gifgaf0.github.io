# G-2a-S7 SECOND-LEG REPORT (CC, independent)

**Date:** 2026-07-09 · **Pre-registration:** `G_2a_S7_EXECUTION_PREREGISTRATION.md` (archived here) ·
**Script:** `gate2a_s7_secondleg.py` (exact ℚ, stdlib) · **Base:** V4.55 · **Chat leg audited:**
`g_2a_s7_chatleg.py` + `G_2a_S7_CHATLEG_REPORT.md`.

Gate: compute **N(Γ)/Γ = Isom(flat Borromean orbifold)** for the cube-folding crystallographic
group Γ (§2.87.E's R3 bank). Decisive bits: **B1** (is the odd axis-permutation coset realized in
N?) and **B2** (do lattice translations realize the turn-over classes, strand-aligned?).

## Independence — honest disclosure of the route taken
The handoff permits two routes: (a) the **Γ presentation** (point cosets, vector system, L), or
(b) *preferred* — the **ITA cell-1 standard setting** of #24. **I attempted (b) and abandoned it
deliberately:** a body-centered cell-1 all-screw translation set with three pairwise-skew axes does
**not** drop out of a naive choice — my computational search over the ¼-grid returned **zero** valid
skew screw-sets, and my skew *test* even flags the chat's own verified cell-2 setup as "intersecting"
(the crystallographic axis-geometry is delicate). Getting the *setting* wrong would corrupt the
decisive bits, so I used route **(a)**, the sanctioned Γ presentation, with:
- **fully independent code**, and a **different method** for the normalizer — **direct conjugation of
  the generators + a Γ-membership test**, where the chat solved the conjugation *congruences*
  algebraically on a grid;
- my own closure/generation/orbit checks and my own Φ_flat axis-tracking.

The **#24 / Borromean-orbifold identification is adopted from CHK Ex. 2.32** (prior art) by *both*
legs — not independently re-derived. So this leg independently confirms the **computational** claims
(B1, B2, |N/Γ|, Φ_flat structure), not the orbifold-type attribution, which is a shared adoption.

## Euclidean-normalizer table cross-check (delegated to CC) — reported honestly
I searched for the Fischer–Koch Euclidean normalizer of #24 (I2₁2₁2₁) at the cubic point (Bilbao /
ITA ch. 3.5/15). The **source is confirmed** (Fischer & Koch 1983; ITA Vol. A Part 15, hosted on
Bilbao), but the **specific #24 cubic-metric entry is not openly retrievable** through this
environment's network — the same blocker the chat hit. So the table lookup remains **unresolved by
open sources**; the identification rests on the **two independent computations** (chat congruence-solve
+ this direct-conjugation method), which now agree in full. Not laundered as a table confirmation.

## H-A — Γ is the right group (PASS, R1 computational; orbifold-type adopted)
- **Closure** via membership test (own): every r_i r_j ∈ Γ; words in r₁,r₂,r₃ reach all four point
  cosets and **generate L** (2e₁,2e₂,2e₃,(1,1,1) all attained).
- **Base axes pairwise skew:** ℓ₁={(t,0,½)}, ℓ₂={(½,t,0)}, ℓ₃={(0,½,t)} — the shared fixed
  coordinate differs for each pair (clean 3-line check).
- **Transitivity:** one Γ-orbit per family (all 4 offset-classes mod 2 reached) ⇒ **the singular
  locus is exactly 3 circles**.
- Point group 222, I-centered ⇒ **I2₁2₁2₁ (#24) = the Borromean orbifold** (CHK Ex. 2.32, adopted).

## H-B — the normalizer (PASS, R1; B1 confirmed)
By direct conjugation + Γ-membership over B ∈ O_h, b on the (½ℤ)³ grid mod L:
- **|N/Γ| = 48** (192 distinct (B,b mod L), ÷4).
- **P_N = O_h — the odd axis-permutation coset IS realized (decisive bit B1).** ✔
- The odd coset is **uniformly (½,½,½)-shifted mod T_N = ℤ³** and **genuinely nonsymmorphic**
  (no single global origin absorbs the shift for all odd point parts — verified by an exhaustive
  origin search, the correct simultaneous test).
- **T_N/L ≅ (ℤ/2)² = {0, e₁, e₂, e₃}**; **−I ∈ N, unshifted**.
- Index factorization |N/Γ| = 4 (T_N/L) · 2 (inversion) · 6 = 48. Structure matches the chat.

*(Two of my structural sub-tests initially read False against the chat — the uniform-shift and
nonsymmorphic tests — because I first measured them at the wrong resolution (mod L instead of mod
T_N=ℤ³) and per-element instead of with a single global origin. Fixed; both then confirm the chat.
Recorded for honesty.)*

## H-C — the realization map Φ_flat (PASS, R1; B2 confirmed)
- **Faithful:** 48 distinct (σ,ε,d) images. **Homomorphism:** 0 failures / 2304 products (own
  renormalize-and-compare).
- **Image = the parity-law 48-group** {Πε = sgn(σ)} × independent d ≅ **ℤ/2 × S₄**. The
  pre-registration's drafting-error formula (Πε = d·sgn σ) is *not* what holds — the correct
  constraint is **Πε = sgn(σ) for all 48 with d an independent ℤ/2**, exactly the §2.87.E hyperbolic
  structure (det=+1 on all 48; orientation carried separately). Reproduced independently; convergence,
  not rescue.
- **Size-2 (σ,ε)-fibers** with the **axis-invisible central class** (σ=id, ε=+++, d=−1) realized —
  the flat home mirrors the hyperbolic bookkeeping element-for-element.
- **Decisive bit B2 — EXACT and strand-aligned:** translation **e₁ ↦ (id; ε=(+,−,−); d=+1)**,
  **e₂ ↦ (id; (−,+,−); +1)**, **e₃ ↦ (id; (−,−,+); +1)**; identity ↦ 0. **Translation by e_f is
  the turn-over fixing strand f.** The (ℤ/2)² translation subgroup = {identity, three turn-overs} =
  the motion V₄, realized by **half-lattice translations**. ✔

## Verdict (second leg) and register
- **H-A: PASS** (computational; orbifold-type adopted from CHK by both legs).
- **H-B: PASS (R1)** — |N/Γ|=48; **B1: odd coset realized (P_N=O_h)**, half-shifted, nonsymmorphic;
  T_N/L=(ℤ/2)²; −I∈N. Independent method (conjugation+membership).
- **H-C: PASS (R1)** — Φ_flat faithful homomorphism; image ℤ/2 × S₄; **B2: translation e_f ↦
  turn-over fixing strand f**, strand-aligned.
- **H-D verdict:** the flat crystallographic home is **maximally symmetric — Isom(E³/Γ) ≅ ℤ/2 × S₄**,
  realizing every symmetry class of the Borromean rings statically, the odd coset included, at the
  cost of the orbifold import (the cone-π singular scaffolding, physically undeclared, R3). This
  sharpens S6: the odd coset is dynamical in flat **smooth** space but **static in the flat orbifold
  home**, carried by half-centering-shifted isometries. Cross-geometry table: smooth flat ℝ³ →
  proper ceiling A₄ (T_h impropers); **flat orbifold → full 48**; round S³ → full 48.
- **R3 bank:** *turn-over = half-lattice translation in the flat home* (strand-aligned; adjacent to
  §2.50 thinking, no import claimed). Logged, uninterpreted.

M.CW/M.BRIDGE intact; no observable, no μ_n; **§2.50 untouched** (single open import); **§2.52 Open 3
untouched.**

## Boundaries (honest)
1. **Route (b) not delivered:** I did not produce the independent ITA cell-1 screw setting — the
   axis-geometry defeated a quick correct build. Independence here is at the **code + method** level
   (direct conjugation vs congruence-solve) on the shared Γ presentation, not a distinct coordinate
   setting. Weaker than the preferred route; flagged, not hidden.
2. **Table cross-check unresolved** through open sources (the #24 normalizer entry is behind ITA);
   the result rests on two agreeing independent computations, not a tabulated value.
3. **Orbifold-type (#24 = Borromean)** is adopted from CHK by both legs, not second-legged.

*Two-leg agreement achieved for every decisive computational claim (B1, B2, |N/Γ|=48, Φ_flat faithful
homomorphism onto ℤ/2 × S₄), with the three boundaries above stated plainly.*
