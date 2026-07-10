# G-2a-S6 SECOND-LEG REPORT (CC, independent)

**Date:** 2026-07-09 · **Pre-registration:** `G_2a_S6_EXECUTION_PREREGISTRATION.md` (archived here) ·
**Scripts:** `gate2a_s6_secondleg_HA_HB.py` (SnapPy-free: H-A core + H-B), `gate2a_s6_secondleg_HC2.py`
(H-C2 decisive + H-A peripheral yield) · **Base:** V4.54 CANONICAL (`74a34bdd…`) ·
**Chat leg audited:** `g_2a_s6_chatleg.py` + `G_2a_S6_CHATLEG_REPORT.md`.

## Zero-shared-machinery contract
Handoff spec §6 routes, in preference order, executed as:
- **H-B** — independent parametrization: exact **ℚ vertex-set equality** over the generic three-ellipse
  configuration (the chat used an axis-triple predicate; I test ellipse-set equality directly). SnapPy-free.
- **H-A core** — the axis representation, parity-law/properness, image O, faithfulness, and the
  N_{SO(3)}(O)=O uniqueness, all from the signed-permutation model. **SnapPy-free.**
- **H-C2 (decisive)** — the spec prefers a SnapPy-free hand-built two-octahedra gluing. I do **not**
  hold that face-pairing to a certainty that would make a hand build trustworthy for the *decisive*
  bit, so — rather than risk a wrong decisive result — I use SnapPy by an **independent construction
  path** (`Link('L6a4').exterior()`, confirmed isometric to `6^3_2`, **not** the census name the chat
  used) with **all downstream combinatorics written fresh** (own automorphism search, own vertex-link
  χ, own orientation/swap analysis). **Shared-solver caveat flagged** per the S4 precedent the spec
  explicitly permits.
- **H-A peripheral yield** — re-extracted independently from the 48 canonical isometries (own code).

## H-A — the axis representation is geometric, not conventional (PASS, R1)
**Core (SnapPy-free), from the signed-permutation model:**
- **Parity law ⟺ properness:** sgn(σ)=ε₁ε₂ε₃ ⟺ det(axis)=+1, verified over all 48 signed perms. So the
  parity law *is* the statement that motions act properly (image ⊂ SO(3)).
- Image = **O ⊂ SO(3)** (24 orthogonal det-+1 matrices); axis rep **faithful** on the motion group.
- **N_{SO(3)}(O)=O:** O is self-normalizing inside O_h (finite check: normalizer order 48, rotation
  part 24) and the standard axis argument (a rotation normalizing O permutes its three 4-fold axes ⇒
  monomial ⇒ in O) closes it ⇒ the spatial identification is **unique up to inner**.
- **Full-group model ℤ/2 × O:** the axis rep kills the central ℤ/2 ⇒ kernel = central ℤ/2, image = O
  (det=+1 for all 48, never O_h), every fiber size 2 (one or-preserving + one or-reversing).

**Peripheral yield (own SnapPy extraction, MATCHES chat):** over the 48 isometries — or-preserving
peripheral maps all **±Id**, or-reversing all **±diag(1,−1)**, **zero shear** (forms `{pmId:72,
diag_pm:72}`); **det(axis)=+1 for all 48**; faithful on the 24 motions; **axis-rep kernel = central
ℤ/2** (the amphichiral involution is *axis-invisible*); every (σ,ε) fiber size 2. The chat's
pre-reg-deviation note (the naive "parity ⟺ properness over all 48" biconditional is false; the true
statement is det=+1 for all 48) is reproduced and is an **upgrade yield**, not a failure.

## H-B — the flat rigid dichotomy (PASS, R1)
Exact ℚ computation over the generic three-ellipse embedding (ring i normal to axis i, cyclic
long/short semi-axes a≠b), via vertex-set equality:
- **O(3)-stabilizer = 24** (pyritohedral m3̄); **rotation part = 12 = T ≅ A₄**.
- The 12 rotations equal the **even-σ subgroup A₄ of the motion group element-for-element** (in the
  (σ,ε) bookkeeping); every odd motion element fails rigidity for this embedding.
- **Genericity** confirmed: sizes (24,12) independent of the a≠b choice (tested 2:1 and 3:1).
- **Fix_flat(A₄) = {0, ∞}:** the common fixed subspace of the nontrivial rotations in ℝ³ is
  0-dimensional (only the origin; exact ℚ rank), plus the point at infinity ⇒ exactly **2 points,
  both in the complement**.

## H-C2 — the ℝ³-rigid ceiling (PASS, R1 — the decisive computation)
Independent construction path (`L6a4` diagram, isometric to `6^3_2`); own combinatorics on the
canonical retriangulation (24 tetrahedra): **5 vertex classes**, own link-χ gives **2 sphere links
(finite = octahedron centers) + 3 torus links (cusps)**; own gluing-propagation automorphism search
finds **48 automorphisms** (cross-checks `K.isomorphisms_to(K)`=48). Classification (orientation,
strand-parity, octahedron-center action):

| | fix both centers | swap centers |
|---|---|---|
| or-preserving even | **12** | 0 |
| or-preserving odd | 0 | **12** |
| or-reversing even | 12 | 0 |
| or-reversing odd | 0 | 12 |

**DECISIVE BIT (pre-registered, both branches equal weight): every orientation-preserving ODD element
SWAPS the two octahedron centers; every EVEN element FIXES both.** So stab_{Isom⁺}(center) = the
order-12 subgroup = **A₄**, and the center-swap character on Isom⁺=S₄ is the **sign** character
(the homomorphism S₄→ℤ/2 is sign, not trivial; the order-12 kernel is uniquely A₄).

**The pre-registered falsifier branch (an odd element fixing a center ⇒ a rigid full-O embedding in
ℝ³) did NOT fire.** Conclusion chain: Fix_M(A₄)=2 points (H-B, transported by equivariant Mostow) =
the two octahedron centers (A₄ fixes both); odd Isom⁺ elements swap them ⇒ **Fix_M(S₄)=∅** ⇒ **the
ℝ³-rigid ceiling is EXACTLY the pyritohedral A₄.** The full O is spatial only in round S³ (H-C1:
equivariant filling, orthogonal in O(4)) or dynamically as motions in flat space.

## H-C1 — the S³ ceiling (R1-adopt)
Adopted via the prior-art chain (all peripheral maps ±Id ⇒ equivariant Dehn filling; Dinkelbach–Leeb
⇒ orthogonal action ⊂ O(4)). The framework contribution — the ±Id verification — is reproduced in the
H-A peripheral yield above. Not independently re-derived beyond that; adopted as the chat states.

## Verdict (second leg) and register
- **H-A: PASS (R1)** — core fully SnapPy-free; peripheral yield reproduced independently.
- **H-B: PASS (R1)** — fully independent over exact ℚ.
- **H-C2: PASS (R1)** — decisive bit reproduced; **falsifier refuted**; ℝ³-rigid ceiling = pyritohedral
  A₄. (Shared-solver caveat: canonical retriangulation + peripheral maps from SnapPy, as chat;
  independence at construction-path + all analysis code.)
- **H-D graded verdict:** LOCATED-IMPORT, curvature/embedding-graded — import-free (parity law =
  properness; A-from-peripheral-data; inner-uniqueness), flat-embedding import (pyritohedral A₄),
  round-S³/curvature import (full O static-spatial); in flat space the odd coset is intrinsically
  **dynamical**. Two legs agree.
- **Flag disposition:** with S5 (motion↔stabilizer identified) and S6 (motion↔spatial graded), the
  **distinct-S₄ flag is fully dispositioned** — no un-analyzed pair remains.
- **R3 bank (cube-folding orbifold):** I did **not** pursue the crystallographic N(Γ)/Γ route (offered
  as an alternative); it remains logged/uninterpreted, as the chat has it. Not second-legged here.

M.CW/M.BRIDGE intact; no observable, no μ_n; **§2.50 untouched** (the per-strand spinor phase remains
the single open import); **§2.52 Open 3 untouched.**

*Two-leg agreement achieved for H-A/H-B/H-C2. The one honest boundary is the shared SnapPy solver for
the canonical retriangulation + peripheral maps in H-C2 and the H-A yield — flagged per S4 precedent,
with the group-theoretic core of H-A and all of H-B fully SnapPy-free, and the decisive combinatorics
written fresh on an independently-constructed manifold.*
