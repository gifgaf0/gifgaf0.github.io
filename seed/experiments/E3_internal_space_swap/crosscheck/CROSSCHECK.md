# E3 cross-check — swapping the internal space: G2 and SU(3)/T²

**Verdict: CONFIRMED.**

Every headline number in E3 and every seed verdict reproduces under independent methods: 61 of 61 compared quantities agree, most to about 1e-10. The issues are all minor: wording, verdict labels, one mislabelled column in the stability table, citation precision, and how reproducibility is presented. None changes a number or a seed verdict.

All code is in this folder: `cc_g2.py`, `cc_skyrme.py`, `cc_flag.py`, `cc_stability.py` and `cc_summary.py`; `run_crosscheck.sh` runs them all. The comparison table is in `crosscheck.json`.

The original code was read only after all of my numbers were computed (procedure step 4). At that point the only disagreement left was the sign of the SO(3) π₃ map, which turned out to be a convention (see below).

## What I did differently

| item | original | this cross-check |
|---|---|---|
| g2 | Der(O), octonion lines {i, i+1, i+3} | stabiliser in so(7) of Bryant's 3-form φ = e123+e145+e167+e246−e257−e347−e356; roots from a numerically found Cartan subalgebra; su(2)s from root vectors; principal su(2) from ρ^∨, completed to an sl2 triple |
| irreps, branching | Freudenthal multiplicities + 2D difference formula; explicit tensor products | Weyl character formula by exact Laurent-polynomial division (integers); SU(2)_L×SU(2)_S content by peeling highest weights; G2→SU(3) by peeling SU(3) characters (Gelfand–Tsetlin) |
| hedgehog | two-sided shooting | `solve_bvp` collocation on [1e-5, X], Robin condition from F ≈ C/x² − C³/21x⁶, X = 60/120/240 |
| inertia tensor | 7×7 matrices, Gauss × uniform angular grid | 14-dim **adjoint** representation via structure constants, Lebedev 23/31, two mapped radial rules; repeated in the 7 |
| moment map | Haar sampling, hull area, Hausdorff distance | exact sympy geometry; Schur by Birkhoff (majorization of 2×10⁵ samples from a different sampler); Horn **constructively**: an explicit orthogonal U for 64 target points (vertices, edges, interior) |
| π₂ | lat-long continuum quadrature + lat-long lattice Berry phases | Berry curvature integrated over the stereographic **plane** with analytic derivatives; Berry phases on a 40 000-point **spherical Delaunay** mesh; a different non-holomorphic U(3) deformation |
| π₃ | spherical quadrature of the lift degree; projector-only CS + Γ route | lift degree on **Cartesian** grids (4th-order finite differences, 64³/96³/128³, Richardson); direct test that two lifts g and g·T(x) of the same flag configuration give the same degree |
| stability | linear-hat radial basis, l ≤ 3 | my own structure-constant Hessian; **cubic B-splines**, l ≤ 3 **and l ≤ 4**, Lebedev; validated against finite differences of the full nonlinear energy and against exact zero modes integrated over all space |

## Agreement table

| quantity | original | cross-check | agree |
|---|---|---|---|
| Dynkin index: long / short / diag(L×S) / SO(3)⊂SU(3) / principal | 1, 3, 4, 4, 28 | 1, 3, 4, 4, 28 (to 1e-14) | yes |
| 14 under SU(2)_L×SU(2)_S | (3,1)+(1,3)+(2,4) | same (matrices and characters) | yes |
| 7 under SU(2)_L×SU(2)_S | (2,2)+(1,3) | same | yes |
| 14 and 7 under principal SU(2) | spin 1 + spin 5; spin 3 | same | yes |
| C₂ of 7, 14, 27, 64, 77[0,2], 77′[3,0] | 2, 4, 14/3, 7, 10, 8 | same (exact) | yes |
| 13 G2 irreps up to dim 500 (branching, C₂, allowed J) | table | 13/13 identical | yes |
| jL + jS integer in every component | yes | yes; exp(2πT₃ᴸ) = exp(2πT₃ˢ) to 2.5e-15 (on 7 and 14) | yes |
| su(3) = stabiliser of e₁ | 8-dim, 7 = 3+3̄+1 | 8-dim, Casimir 4/3 (×6), 0 | yes |
| M_cl [F_π/e] | 36.46164562 | 36.46164563 (E2: 36.46164562524) | 6e-11 |
| Λ | 50.97873911 | 50.97873912 | 9e-11 |
| J₂ (I₂ = (π/2)J₂) | 25.89678962 | 25.89678962 | 5e-11 |
| F′(0), C | −1.00376411, 8.6385782 | −1.00376411, 8.6385783 | yes |
| virial (E₂ − E₄)/M | 4e-11 | −1e-13 | yes |
| I₁ (×3) [1/(e³F_π)] | 106.769622 | 106.7696215 | 1e-10 |
| I₂ (×8) | 40.678582 | 40.6785820 | 6e-11 |
| short block | < 7e-19 | < 2e-14 | yes |
| 7-dim vs adjoint inertia tensor | — | equal to 4e-10 | — |
| B and E of the short-root hedgehog | B = 3, E = 3M | 3.0000000000, 3.0000000000 | yes |
| ANW point: M, 1/I₁, 1/I₂ [MeV] | 863.04, 195.58, 513.35 | same | yes |
| E(14, J=1) − E(1, J=0) at ANW | 708.93 MeV | 708.93 MeV | yes |
| SU(3) refit: F_π, e, antidecuplet | 113.755 MeV, 5.24740, 1757.27 MeV | same (own PDG query: octet 1151.194, decuplet 1382.106) | yes |
| rotor ladder (E − M)·I₁, first 10 states | 0, 3.6247, 6.1243, 8.2494, 8.8741, 12.3738, 13.1236, 13.8741, 14.8112, 15.7483 | identical (≤ 4e-11) | yes |
| moment map, a = (1, 0.3, −1.3) | hexagon, 120°, sides 0.98995 / 2.26274 | exact: sides 7√2/10, 8√2/5 alternating; angles exactly 120° | yes |
| moment map, a = (1, 1, −2) | triangle, 60° | triangle, side 3√2, 60° | yes |
| Schur–Horn | 1.1e6 samples inside | 2e5 samples majorized; 64 targets attained (residual 1.4e-11) | yes |
| π₂ charges, maps A–G plus deformations | (1,0,−1), (0,1,−1), (1,1,−2), (2,−1,−1), (2,0,−2), (3,−2,−1), (−1,0,1) | same, to < 1e-6, both discretisations | yes |
| π₃ lift degrees C1–C5 | 1, 1, 2, 4, −1 | 1.0000000, 0.9999987, 1.9999993, −3.9999968 (+3.9999968 with opposite orientation), −1.0000000 | yes (see note) |
| π₃ independent of the lift | implied by C2 | deg g = 1.9999993, deg gT = 1.9999966, deg T = 0, projectors identical to 5e-16 | yes |
| any negative Hessian eigenvalue | none | none (min 7.5e-8) | yes |
| (1,3) lowest at R = 20 (exact (1/32)(π/20)² = 7.7106e-4) | 7.7156e-4 | 7.71063e-4 | yes |
| (3,1) continuum at R = 20 (×3, ×1) | 7.958e-4, 1.4359e-3 | 7.953e-4, 1.4358e-3 | yes |
| kaon continuum at R = 20 (×4, ×2) | 7.827e-4, 1.5995e-3 | 7.825e-4, 1.5993e-3 | yes |
| kaon zero-mode floor at R = 20 | 3.37e-5 (nr = 90, still falling) | 2.906e-5 (converged) | consistent |
| (2,4) spectrum vs kaon spectrum | doubled (1.6e-14) | doubled (1.3e-13) | yes |

**Note on the π₃ sign.** With my standard so(3) generators, (L_a)_bc = −ε_abc, the SO(3) hedgehog has degree −4 relative to my C1 = exp(i f n·σ). The original uses (L_a)_ij = +ε_aij, which is my C4′ and gives +4. The invariant is |deg| = 4, the Dynkin index of SO(3) ⊂ SU(3).

**Lift degrees.** They converge at fourth order: errors 2.4e-4, 4.8e-5 and 1.5e-5 at N = 64, 96, 128, ratios 5.0 and 3.2 against 5.06 and 3.16 expected. They are Richardson-extrapolated to within ≤ 3e-6 of the integers.

## Stability, in more detail

My quadratic form matches ½ d²E/dε² of the full nonlinear energy E[U₀e^{εφ}] to 1.3e-10, 8.6e-10 and 2.1e-10 in the three blocks. The quadratic kernel is block-diagonal **pointwise** to 6e-16, as SU(2)_short invariance requires.

Exact rotational zero modes integrated over all of space give Q = 1.9e-10, 8.5e-11 and 8.5e-11. On a ball of radius R they leave a −1/R³ surface term (ratio 7.9994 between R = 30 and R = 60). That is why a Dirichlet box lifts the zero modes to small positive values.

My cubic B-spline basis resolves the zero modes much better than linear hats:
- (3,1) block: 1.9e-6 (×3) and 3.7e-5 (×3) at R = 20, unchanged from nel = 30 to 60; 7.5e-8 and 4.1e-6 at R = 40. These are consistent with 1/R⁵ (translations, 1/r³ tails) and 1/R³ (iso-rotations, 1/r² tails).
- kaon / (2,4) block: 2.906e-5 at R = 20 and 3.29e-6 at R = 40.

The original's values (7.4e-5 / 3.5e-4 at R = 20, nr = 30) are higher, as Ritz upper bounds from a weaker basis must be, and its "falls with refinement" statement is correct.

Going to l ≤ 4 adds the complete grand-spin channels K ≤ 3 for (3,1) and K ≤ 7/2 for (2,4). It changes no low eigenvalue. So the conclusion "linearly stable within the tested basis" stands and is slightly strengthened. Global minimality stays OPEN.

## Citations checked (arXiv mirror)

- **Mayanskiy 1611.04070, §4.** Table 2 lists A₁⁴ and A₁²⁸ with explicit embeddings. The list right after it reads "A₁ = A₁¹, Ã₁ = A₁³, A₁⁴, A₁²⁸". Prop. 4.1 gives (2,4) = D½⊗D3/2 for A₁+Ã₁ and D₅ for the principal SU(2). This matches the report, apart from the "Table 2" label for indices 1 and 3.
- **ABW 2101.11638, §1.4.** States H³(F) = 0 and π₃(Fₙ) ≅ ℤ. Matches.
- **Amari–Sawado 1805.10008, eq. (13).** The F₂ Hopf invariant ∫ε(A·F − Γ), with Γ in eq. (14). Matches.

## Issues (all minor)

1. **Verdict words.** Seed predictions and PLAN expectations are labelled CALIBRATED in the headline: the rotor ladder, integer J, the 7 branching, the C₂ values, the inertia blocks, the moment map, π₂ and π₃. PLAN §1 reserves CALIBRATED for literature targets, so these should read CONFIRMED, as they already do in `seed_claims`.
2. **Stability table, (3,1) at R = 40, nr = 40.** The entry 1.94e-4 (×3) is the first continuum level (mine: 1.937e-4). The iso-rotation zero-mode triplet is the 3.73e-4 entry, which is unresolved and lies above that continuum level. So "zero modes, then continuum" and "zero modes appear as the lowest eigenvalues" are wrong for that column. The conclusion is unaffected.
3. **"The centre element exp(2πT₃ᴸ)".** G2 has trivial centre. The element is the image of −1 ∈ SU(2)_L, which is central only in the SO(4) subgroup.
4. **The no-linear-term argument is incomplete as written.** "A character of the stabiliser's Lie algebra" alone does not exclude an SU(2)_short-invariant term along the (3,1) directions. Right SU(2)_L (spatial rotation) invariance does. The conclusion holds. Separately, AMENDED is used for a PLAN §3 literature note, not for a seed claim.
5. **Citation precision.** Mayanskiy's indices 1 and 3 come from the list after Table 2, not from Table 2 itself.
6. **"E2 parameters".** These are PLAN's rounded ANW values (129 MeV, 5.45). E2's own fit is (129.26, 5.444), which gives M = 865.75 MeV and a 14–1 gap of 708.0 MeV instead of 708.9. This is a declared deviation with an effect of at most 0.3%.
7. **Reproducibility presentation.** `logs/run_all.log` is a resumed run that did not execute `e3_stability_refine`; that step and `make_results` ran separately. The "27 minutes" is a sum of step times. Each step was run, but `run_all.sh` in its current form has not been run end to end.
8. **Seed row "the B = 1 fold is the long-root hedgehog: CONFIRMED".** What the evidence shows is that this hedgehog carries B = 1 (the generator of π₃) and is locally stable. That it is the minimal B = 1 fold in G2 is OPEN, as the report says elsewhere. The row should carry that qualifier.

## What I did not redo

I did not re-implement the projector-only (Coulomb-gauge CS + Γ) route for π₃. The CS and Γ values the original reports reproduce B arithmetically, B = −(3ΣCS + Γ)/24π². The equality of the π₃ charge with the lift degree, and its independence of the lift, I checked my own way.

## Seed verdicts after the cross-check

| claim | verdict |
|---|---|
| §2, G2 folds are bosons | CONFIRMED. Holds for all irreps, because exp(2πT₃ᴸ) = exp(2πT₃ˢ) and physical states are SU(2)_short singlets. |
| Lowest states 1 (J=0), then 14 (J=1); 7 not allowed | CONFIRMED |
| §3, SU(3) ⊂ G2 as the stabiliser of an imaginary octonion | CONFIRMED |
| §4, B = 1 generator is the long-root hedgehog | CONFIRMED; minimality OPEN |
| Inertia I₁ (×3), I₂ (×8), 0 (×3) | CONFIRMED |
| Local linear stability | CONFIRMED; global stability OPEN |
| §7.2, moment-map hexagon | CONFIRMED |
| §7.2, π₂ = ℤ² | CONFIRMED |
| §7.2, π₃ = ℤ through the lift | CONFIRMED |

## Reproduce

    cd seed/experiments/E3_internal_space_swap/crosscheck && ./run_crosscheck.sh

This runs single-threaded in about 12 minutes. Every script prints its own checks:

| script | checks passed |
|---|---|
| `cc_g2` | 54/54 |
| `cc_skyrme` | 18/18 |
| `cc_flag` | 13/13 |
| `cc_stability` | 9/9 |

`cc_summary` then compares against `../results.json` (61/61 agree) and writes `crosscheck.json`.
