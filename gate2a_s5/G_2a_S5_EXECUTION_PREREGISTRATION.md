# G-2a-S5 EXECUTION PRE-REGISTRATION
**Gate:** G-2a-S5 — the distinct-S₄ identification gate (motion-group S₄ vs Fano line-stabilizer S₄)
**Date registered:** July 8, 2026. **Base:** SQT Master Ledger V4.53 (candidate; G-2a-S4 folded). This registration promotes the R3 convergence note in §2.87.C's Eddington record ("distinct-S₄") to a registered gate. Part VI row to be added at the execution fold (G-2a-S1/S2 precedent).

## 0. The question
Is the **motion-group S₄** (V4.53 / §2.87.C: the orientation-preserving ambient symmetry group of the Borromean strands acting on (strand labels, strand orientations) — the det = +1 signed-permutation group, abstractly O ≅ S₄) **canonically identifiable** with the **Fano line-stabilizer S₄** (§2.85 Part C: Stab(L) ⊂ PSL(2,7) ≅ GL(3,2), order 24, preserving U(L))?

"Canonically" means: identifiable by an isomorphism covering the identity on the S₃ already identified by §2.73 (topological strand-permutation S₃ = geometric S₃ on the three points of L — forced), with naturally indexed kernels — NOT merely abstractly isomorphic.

## 1. Eddington guard (the trap this gate exists to avoid)
- **Abstract S₄ ≅ S₄ is content-free.** Any two groups of order 24 with the right presentation are isomorphic; that proves nothing. The gate passes ONLY on equivariant naturality over the §2.73-identified S₃, with the indexing conventions declared below.
- **Out of scope:** the spatial-rotation O (octahedral rotation group of ℝ³) is a THIRD S₄-class object and is NOT addressed by this gate; no claim about it is made or implied. The distinct-S₄ flag remains logged for that pair regardless of this gate's outcome.
- No numeric targets exist for this gate; the factor-of-4 remains quarantined by standing habit and is not consulted.

## 2. Structural setup (banked, load-bearing)
1. **§2.73 (forced):** the topological S₃ of Borromean strand permutation = the geometric S₃ ⊂ GL(3,2) acting as the full permutation group on the 3 points of the line L. This is the base identification every construction below must respect.
2. **Motion side (V4.53, R1):** the motion group is {(σ, ε) ∈ S₃ ⋉ (ℤ₂)³ : sgn(σ) = ε₁ε₂ε₃}. The forget-ε map is a surjection onto S₃ with kernel V₄^mot = {+++, +−−, −+−, −−+}: three nontrivial elements, each flipping exactly one PAIR of strands — equivalently (via the S₃-equivariant complement bijection on 3 objects) each indexed by the single UN-flipped strand = a point of L.
3. **Algebra side (§2.85 Part C, R1):** Stab(L) ≅ S₄ acts on U(L) = 2·triv ⊕ 2·std₃; the S₄ → S₃ quotient permutes the six ZDs and their kernels; the V₄ kernel preserves each kernel individually. The kernel of Stab(L) → Sym(points of L) is the pointwise stabilizer of L — hypothesized below to be the three transvections with axis L, indexed by their directions = the nonzero vectors = the points of L.

## 3. Hypotheses (pre-registered, falsifiable)
- **H-A (R1 target — the identification).**
  (i) ker(Stab(L) → S₃) has order 4, elementary abelian; its three nontrivial elements are the transvections with axis L, in natural bijection with the three points of L via transvection direction.
  (ii) This bijection intertwines the S₃-actions: conjugation by g ∈ Stab(L) sends the transvection at point p to the transvection at point σ_g(p), where σ_g is g's §2.73-identified permutation of line points.
  (iii) Both extensions 1 → V₄ → S₄ → S₃ → 1 are split and equivalent over id_{S₃}; construct an explicit isomorphism Φ: S₄^mot → Stab(L) covering id_{S₃} and matching the indexed kernels (motion flip-pair {j,k} ↦ transvection at the complementary point i — **declared convention:** the point/pair correspondence is the complement bijection; the alternative direct-pair indexing differs by a fixed S₃-equivariant relabeling and carries identical content — a convention, declared, not a freedom).
  (iv) Compute the uniqueness class of Φ: which automorphisms of the target fix the S₃-quotient (over §2.73) and the V₄ indexing. Expected: Φ is unique up to at most the inner automorphisms by V₄ itself; state exactly.
- **H-B (R1 computation / R2 reading — the dictionary).** Compute the precise module action of the three transvections Φ(ε-flips) on U(L) = 2·triv ⊕ 2·std₃ (refining §2.85's "preserves each kernel individually"): which summands are fixed, what each transvection does inside each ZD kernel. Dictionary candidate (R2): **strand turn-over ↔ transvection at the corresponding line point.** Any physical reading is R2 under the M.CW ceiling.
- **H-C (conditional consequence, R2 — the convergence collapse).** If H-A passes: the spinorial promotion is SINGLE — §2.50's lift of the motion group and §2.85 Part D's promotion S₄ → 2·S₄ are the same lift of the same group, so V4.53's two convergent routes (Schur–Weyl symmetric channel; motion-group → 2O) become one structure, and their 4-dim modules (Sym³(ℂ²) as a 2O-rep; the unique genuine 4-dim irrep χ_{3/2}) must be verified isomorphic as 2O-reps under Φ's lift (a character computation — expected from G-2a-S1's D1 = 1, but must be exhibited through Φ, not assumed). **The §2.50 import is NOT supplied by this gate:** identification of the group downstairs does not produce −1 ↦ −Id; the bottleneck count goes from "one import feeding two routes" to "one import feeding one structure." M.BRIDGE untouched.

## 4. Falsification conditions
- H-A(i) fails if the pointwise stabilizer has order ≠ 4 or is not generated by transvections as described.
- H-A(ii) fails — **the decisive falsifier** — if the transvection-direction indexing does NOT intertwine the §2.73-identified S₃ actions, i.e. if matching the kernels requires an outer twist relative to §2.73. Then no canonical identification exists over the forced base, the convergence stays coincidence-class, and the distinct-S₄ flag is CONFIRMED as a genuine distinctness — an informative negative, banked like G-ζ1.
- H-C fails if the two 4-dim modules are inequivalent as reps of the identified double cover — which would break the "one structure" collapse while leaving H-A standing; state separately if so.

## 5. Register ceilings and scope
M.CW: all physical readings R2; the identification itself, if it passes, is R1 finite group theory + R2 for its framework meaning. No observable bridge; no μ_n; no dynamical claim; the §2.50 per-strand spinor phase remains the open import. §2.52 Open 3 untouched.

## 6. Literature-Search-First
Ingredient-level prior art is textbook and is adopted, not claimed: transvection structure of hyperplane/subspace stabilizers in GL(n,2); split extensions V₄ ⋊ S₃ = S₄ and H²(S₃, V₄); the signed-permutation model of O. **One cross-dialect search item is MANDATED at execution start, before any computation:** any published identification linking the symmetry/motion group of the Borromean rings to PGL(3,2)/Fano-plane line stabilizers (knot-theory ↔ finite-geometry dialects — the V4.42/V4.45 vocabulary-gap pattern). The framework-internal content (U(L), the ZD kernels, §2.73's forced base) has no external collision surface, but the group-level bridge might.

## 7. Execution plan
- **First leg (chat-side):** explicit GL(3,2) computation over 𝔽₂ for the §2.85 line L — build Stab(L), compute the pointwise stabilizer, verify the transvection indexing and its S₃-equivariance against §2.73's identification; construct Φ explicitly; verify H-B's module action on U(L) with fresh code (conceptually parallel to but not sharing §2.85's kernel-level scripts); H-C character comparison through Φ's lift.
- **Second leg (CC):** zero shared machinery — different basis/line conventions, independent stabilizer construction (e.g. via the dual/functional description), independent sedenion kernel build for H-B, abstract extension-equivalence check for H-A(iii) by cocycle computation rather than explicit matrices.
- **Audit → fold:** chat-side audit of CC output; fold as §2.87.D + one Part VI row (registering + executing in one row if executed same arc, else the row registers at the next fold touching Part VI).

*Filed July 8, 2026, prior to any computation on this gate. No targets to quarantine beyond standing habit; the decisive falsifier is H-A(ii).*
