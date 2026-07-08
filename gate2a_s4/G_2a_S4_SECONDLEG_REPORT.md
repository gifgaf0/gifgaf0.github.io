# G-2a-S4 SECOND-LEG REPORT (CC, independent)

**Date:** 2026-07-08 · **Pre-registration:** `G_2a_S4_EXECUTION_PREREGISTRATION.md` (archived here) ·
**First leg:** `g_2a_s4_firstleg.py` + `G_2a_S4_FIRSTLEG_REPORT.md` (archived here) ·
**Second-leg scripts:** `gate2a_s4_secondleg.py` (P1 characters + P2 branch a/b),
`gate2a_s4_secondleg_branchC.py` (P2 branch c, SnapPy) · **Base:** V4.52 CANONICAL.

## Zero-shared-machinery contract (honored)
The first leg computed P1 by building the 8-dim operators of `(ℂ²)^⊗3` in numpy and taking
explicit isotypic **projectors**, and P2 by calling `snappy.Manifold("6^3_2").symmetry_group()`.
This second leg touches neither:
- **P1 — pure character theory.** No 8-dim operator is ever constructed. The S₃ decomposition
  comes from the class function χ(σ) = 2^{c(σ)} against the three S₃ irreducible characters; the
  SU(2) decomposition comes from peeling highest weights out of the torus character (x+x⁻¹)³.
  All arithmetic is exact (`fractions.Fraction`), so there is no float roundoff to trust.
- **P2 — independent finite-group construction.** The strand motion group is built from scratch
  as **signed 3×3 permutation matrices**; orientation-preservation is `det = +1`, the parity law
  is checked elementwise over all 48, and the group is identified as O ≅ S₄ by order + element-order
  spectrum + closure. No manifold and no SnapPy are used.

## P1 — Schur–Weyl by characters (MATCHES first leg)
| quantity | first leg (tensors/projectors) | second leg (characters) |
|---|---|---|
| S₃ isotypic dims (sym, alt, mixed) | 4, 0, 4 | **4, 0, 4** (⟨χ,triv⟩=4, ⟨χ,sign⟩=0, ⟨χ,std⟩=2·2) |
| sym block SU(2) content | irreducible (commutant dim 1) | **spin-3/2, multiplicity 1 → unique SU(2)-irreducible isotypic** |
| mixed block | reducible, 2×spin-1/2 | **2 × spin-1/2** (from (x+1/x)³ = χ_{3/2} + 2χ_{1/2}) |
| alt block | 0 (Alt³ℂ²=0) | **0** (no 3 antisymmetric slots in a 2-dim space) |
| Casimir on sym block | 15/4 | **15/4** (= j(j+1) at j=3/2, exact rational) |
| doubling incompatibility | sym {15/4×4} ≠ ℂ²⊕ℂ² {3/4×4} | **15/4 ≠ 3/4 → INCOMPATIBLE** (ternary object; no single CD/Clifford doubling yields Sym³) |

The symmetric channel is the **unique** SU(2)-irreducible S₃-isotypic component, confirmed by an
entirely different route (highest-weight multiplicity = 1, not a commutant SVD). **H-P1: PASS, R1.**

## P2 — exchange realizability & motion group, independent of SnapPy (MATCHES first leg)
- All 48 signed permutations enumerate the full symmetry order; the **det = +1** locus has order
  **24 = |Isom⁺|**.
- **Parity law sgn(σ) = ε₁ε₂ε₃ ⇔ det = +1** verified over all 48 (not a sampled subset).
- Each of the 6 cusp permutations occurs with exactly 4 admissible sign patterns → 6×4 = 24;
  the peripheral-action map is a bijection.
- **Image of Isom⁺ in S₃ = ALL of S₃**, all three transpositions realized orientation-preservingly →
  strand exchange is an orientation-preserving motion. **H-P2: PASS, R1.**
- The det=+1 signed-permutation group is closed, order 24, nonabelian, element orders {1,2,3,4}
  (the order-4 element rules out A₄) → **motion group = octahedral rotation group O ≅ S₄** in its
  standard signed-permutation representation. Reproduces the first leg's principal yield.

## P2 branch (c) — independent SnapPy recompute (RUN; MATCHES)
`snappy` was **not** in the base image but **pip-installs cleanly** here (SnapPy 3.3.2), so branch
(c) of the second-leg spec — "independent SnapPy install with `M.symmetry_group()` on an
independently built triangulation" — is now executed (`gate2a_s4_secondleg_branchC.py`).

Independence from the first leg is at the **construction path**: the first leg called
`snappy.Manifold("6^3_2")` (census lookup by name); this leg builds the manifold from a link
**diagram**, `Link('L6a4').exterior()`, and confirms it is the same manifold via
`is_isometric_to(6^3_2) = True` (identity established, not assumed). Recomputed results:
- Symmetry group `Z/2 × octahedral`, **order 48**; **24** orientation-preserving; all 24 have clean
  ±Id peripheral maps (no shear/mixing).
- **Image of Isom⁺ in S₃ = ALL of S₃**; the three transpositions realized orientation-preservingly.
- **Parity law sgn(σ)=ε₁ε₂ε₃** holds over all 24; each cusp permutation carries exactly 4 sign
  patterns (6×4=24).
- **Cross-check:** the recomputed set of (σ, ε) pairs is **byte-identical** to the machinery-free
  signed-permutation det=+1 group of branch (a)/(b) — `SETS IDENTICAL: True`.

**Honest independence caveat:** `symmetry_group()` itself is the *same SnapPy algorithm* the first
leg used — branch (c) is independent at the **triangulation-construction** level (diagram vs census
name), not at the symmetry-solver level. The solver-independent confirmation is supplied separately
by branch (a)/(b) (pure signed-permutation group theory, no SnapPy), whose (σ,ε) set matches exactly.
Together: the manifold identity and symmetry order are re-derived from an independent construction
path, and the group/parity content is re-derived with zero SnapPy dependence. So the
topological-realizability claim is now **two-leg confirmed at both the manifold level (independent
construction path, isometry-verified) and the group/motion level (SnapPy-free)** — an upgrade from
the group-only confirmation, with the shared-solver caveat stated plainly.

## Discipline flags carried
- **Distinct-48 (Eddington):** |Isom(BRC)| = 48 = |2O| — same integer, distinct provenance
  (hyperbolic isometry count / signed-perm order vs binary octahedral subgroup of SU(2)).
  **No identification made.** The motion group established here is **O ≅ S₄ (order 24), NOT 2O
  (order 48)**; the spinor lift O → 2O (−1 ↦ −Id) is precisely the still-open **§2.50** per-strand
  phase import, not closed by this gate.
- **Distinct-4 held:** sym block and ℂ²⊕ℂ² are both 4-dimensional; the incompatibility is module
  content (Casimir 15/4 vs 3/4), not dimension. No same-dimension identification.
- **Distinct-S₃ / distinct-S₄ noted:** the exchange S₃ (this gate) is grounded in the motion group
  via P2, not assumed equal to the topological/Fano S₃; the convergence of motion-S₄ with spatial O
  remains R3, per the first leg.
- **M.CW / M.BRIDGE:** everything structural (R1); no dimensionful constant, no observable, no μ_n
  number computed. The import is located (§2.50), not resolved. §2.52 Open 3 untouched.

## Verdict (second leg)
- **H-P1: PASS (R1)** — reproduced by characters, zero shared machinery.
- **H-P2: PASS (R1)** — reproduced by independent group construction; exchange realizable,
  orientation-preserving, full S₃.
- **Parity law + motion group O ≅ S₄: PASS (R1)** — reproduced independently over all 48 elements.
- **H-P3 chain:** the single shared bottleneck import (§2.50 per-strand spinor phase) feeding both
  the Sym³ route and the motion-group→2O route is confirmed as the *only* open link; not resolved here.
- **Two-leg agreement:** achieved for all group/rep-theoretic content AND, via branch (c), at the
  manifold level — an independently-constructed (diagram-built, isometry-verified) triangulation
  reproduces the order-48 symmetry group, the full-S₃ image, and the parity law, with the recomputed
  (σ,ε) set identical to the SnapPy-free branch (a)/(b) group. Shared-solver caveat noted: branch (c)
  is construction-path-independent, not symmetry-solver-independent; the solver-independent check is
  branch (a)/(b).

*Second-leg deliverable. Scripts + report committed; first-leg files, first-leg report, and the
pre-registration archived in this directory.*
