# G-2a-S4 SECOND-LEG REPORT (CC, independent)

**Date:** 2026-07-08 · **Pre-registration:** `G_2a_S4_EXECUTION_PREREGISTRATION.md` (archived here) ·
**First leg:** `g_2a_s4_firstleg.py` + `G_2a_S4_FIRSTLEG_REPORT.md` (archived here) ·
**Second-leg script:** `gate2a_s4_secondleg.py` · **Base:** V4.52 CANONICAL.

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

## SnapPy-unavailability disclosure (honest scope)
`snappy` is **not installed** in this environment (`ModuleNotFoundError`). The second-leg spec
offered three P2 branches; branch (c) (independent SnapPy triangulation + `symmetry_group()`) is
therefore **not runnable here**. Branches (a)/(b) — the independent combinatorial/group construction
of the order-24 peripheral-action group and the parity law — are what this leg executes, and they
reproduce the order, the S₃ image, the parity law, and the O ≅ S₄ identification with **zero**
dependence on the first leg's machinery.

**What this does and does not second-leg:** it independently re-derives the *group-theoretic*
content (the exchange-statistics S₃, the det=+1 parity law, the motion group O ≅ S₄). It does **not**
independently recompute the *hyperbolic manifold* (volume 7.328, two ideal regular octahedra,
|Isom| = 48 flag-transitive) — that half rests on the first leg's SnapPy call plus the cited
**Thurston** prior art (Borromean complement = two ideal octahedra). So the topological-realizability
claim is **two-leg confirmed at the group/motion level, single-leg + literature-anchored at the
manifold level.** Flagged, not laundered.

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
- **Two-leg agreement:** achieved for all group/rep-theoretic content. Manifold-level realizability
  is literature-anchored (Thurston) + first-leg SnapPy, not independently recomputed (snappy absent).

*Second-leg deliverable. Scripts + report committed; first-leg files, first-leg report, and the
pre-registration archived in this directory.*
