# E2 cross-check: the fold in SU(2) and SU(3)

*Independent second computation and adversarial audit of experiment E2 (PLAN.md §4). Done October 19, 2026. Code and data are in `crosscheck/`; this file is the report.*

## Verdict

**Confirmed, with minor corrections.**

- Every headline number in `results.json` was recomputed by a different method, and every one agrees, mostly to 1e-12 or better.
- Every calibration in the preregistered table passes with my own numbers.
- Every seed-claim verdict is supported by the evidence.
- No issue is blocking or major.
- The corrections concern verdict wording, the provenance of the targets, one PDG number, one multiplet label, and a few small rounding slips.

## Independence and procedure

1. **Before comparing.** I read PLAN.md, SEED.md, the report and `results.json`, and recomputed everything with my own code. Until that step was done, I looked only at the original's outputs (`results.json`, `out/*.json`, `profile.json`), never its scripts.
2. **Reuse of an earlier attempt.** The directory held an interrupted earlier cross-check of mine (`xc_derive.py`, `xc_hedgehog.py`). I reused both after review, and found and fixed a bug in my own J₂ (see "A bug on my side").
3. **After comparing.** Only then did I read the original scripts, to audit how verdicts are assigned. I also reran the original pipeline in a scratch copy, which wrote nothing to its directory.
4. **Literature.** For the citation audit I read the arXiv texts of DPP (hep-ph/9703373), Praszalowicz (hep-ph/0308114), Acus et al. (hep-ph/9605435), Kopeliovich (hep-th/9707067) and Schechter–Weigel (hep-ph/9907554).

### Methods, chosen to differ from the original

| quantity | original | this cross-check |
|---|---|---|
| hedgehog profile | Chebyshev collocation on the mapped half line, Newton | two-sided shooting (DOP853, rtol 1e-13). Outward from the origin series F = π + ax + c₃x³ + c₅x⁵; inward from a 6-term large-x series (to x⁻¹⁴, derived in sympy). Matched at x_m, with a 2-unknown Newton solve. Run in 4 geometries |
| integrals M, Λ, J₂, D, ⟨r²⟩ | Gauss/Clenshaw–Curtis on the spectral solution | quadrature carried along the ODE, plus [0, x₀] from the origin series and [X, ∞) from the asymptotic series (quad in y = 1/x) |
| energy and inertia densities, I₂ formula | analytic L_μ with explicit SU(3) matrices | the PLAN Lagrangian evaluated as written. The matrix field U₀(r) is differentiated by 6th-order finite differences in Cartesian coordinates, with dU/dt = i[Ω·λ/2, U₀]. Angular product quadrature; an arbitrary non-solution test profile |
| stress tensor | Noether T_ij | T_μν = 2∂L/∂g^μν − g_μν L |
| allowed SU(3) multiplets | explicit tensor-power irreps, lowering operators | Gelfand–Tsetlin patterns, checked against the Weyl dimension formula and the index sum rule Σ I₃² = Σ (3/4)Y² = C₂·d/8 |
| D-function matrix elements | Clebsch–Gordan intertwiners from null spaces | exact Haar integrals ⟨Rν,s\|D_ab\|Rν,s⟩ = d_R ∫\|D^R_νs\|² D_ab, done with Weingarten calculus on U(3) (equal to SU(3) for balanced polynomials) |
| g_A, factor 3/2 | Fourier transform of the Noether current | (a) numerical Noether current from the Lagrangian, integrated over a ball; (b) far-field derivation (below); (c) symbolic proof that D = −2C |

**Far-field derivation of g_A.** In the chiral limit, a static source with axial coupling g_A has the pion field

    π^a = (g_A/(8π f_π)) ⟨σ_i τ_a⟩ n_i / r².

The hedgehog has π^a = f_π F n^a, with F = C/(eF_π r)². After collective quantisation, ⟨N|D_ai|N⟩ = −(1/3)⟨σ_i τ_a⟩. Matching the two (with f_π = F_π/2) gives

    g_A = 2πC/(3e²).

This is identical to ANW's −(π/(3e²))D, because D = −2C. That identity holds because x² × [ANW bracket] = d/dx[x³F′(1 + 8 sin²F/x²)] on solutions, shown symbolically.

## Agreement table

Relative deviation unless marked "abs". All entries agree. The full list (45 quantities) is in `crosscheck.json`.

| quantity | original | cross-check | deviation |
|---|---|---|---|
| M_cl [F_π/e] | 36.46164562524 | 36.46164562522 | 4e-13 |
| M_cl/(3π² F_π/e) | 1.2314457 | 1.2314457 | 4e-13 |
| Λ | 50.97873911434 | 50.97873911434 | 5e-15 |
| J₂ | 25.89678962 | 25.89678962 | 9e-14 |
| I₂ coefficient (π/2)J₂ | 40.678582 | 40.678582 | 9e-14 |
| I₁/I₂ | 2.6247135 | 2.6247135 | 9e-14 |
| C | 8.638578214 | 8.638578218 | 4.5e-10 (the original's C is the less precise one) |
| F′(0) | −1.0037641114 | −1.0037641114 | 4e-12 |
| D | −17.27715644 | −17.27715644 | 2e-10 |
| ⟨r²⟩_B (eF_π)² | 4.477835953 | 4.477835953 | 1e-13 |
| E₂ = E₄ [F_π/e] | 18.2308228126 | 18.2308228126 | 5e-13 |
| virial E₂/E₄ − 1 | −4.4e-13 | +3.3e-13 | numerical zero |
| ∫x²p dx | −2.7e-13 | −1.6e-13 | numerical zero |
| p(0) | 0.38159 | 0.38163 (exact −a²/8 + a⁴/2 = 0.381628) | 9e-5 |
| pressure node | 2.1522 (grid-interval midpoint) | 2.15237 (root) | 1.6e-4 abs |
| Derrick, max \|μE₂(μ)/E₂ − 1\| | 1.7e-15 | 1.2e-15 | — |
| arctan-ansatz I₂ coefficient | 40.5435 | 40.54354 | 9e-7 |
| ANW fit F_π [MeV] | 129.26269 | 129.26269 | 3e-13 |
| ANW fit e | 5.4439855 | 5.4439855 | 1e-13 |
| g_A at the ANW fit | 0.6104737 | 0.6104737 | 2e-10 |
| ball-integral g_A | 0.40698 | 0.40697 (R = 24) | 3e-5 |
| 1/I₂ (ANW set) [MeV] | 512.6940 | 512.6940 | 9e-14 |
| E(8) − E_SU(2)(N) [MeV] | 384.5205 | 384.5205 | 9e-14 |
| r_B at the ANW fit [fm] | 0.593377 | 0.593377 | 1e-13 |
| E(8), E(10), E(10̄), ANW set [MeV] | 1323.52, 1616.52, 2092.56 | 1323.52, 1616.52, 2092.56 | 5e-14 |
| PDG 2026 centres [MeV] | 1151.1942, 1382.1056 | 1151.1942, 1382.1056 | 0 |
| SU(3) refit F_π [MeV], e | 113.75489, 5.247397 | 113.75489, 5.247397 | 3e-13 |
| SU(3) refit M_cl [MeV], E(10̄) [MeV] | 790.428, 1757.270 | 790.428, 1757.270 | 4e-14 |
| SU(3) refit E(27, J = 3/2) [MeV] | 1786 | 1786.16 | rounding |
| refit g_A, SU(2) form / × 7/10 | 0.65707 / 0.45995 | 0.65707 / 0.45995 | 2e-10 |
| \|⟨p↑\|D₃₃\|p↑⟩\|, SU(2) / SU(3) octet | 1/3, 7/30 | 1/3, 7/30 (exact) | 3e-16 |
| optional fit α, β, rms [MeV] | 371.756, −99.594, 3.984 | 371.756, −99.594, 3.984 | 5e-15 |
| Guadagnini LHS − RHS, PDG 2026 [MeV] | +8.507 | +8.507 | 3e-13 |
| Dirichlet box Λ, X = 10/20/40 | 37.09 / 44.11 / 47.59 | 37.091 / 44.108 / 47.594 | rounding |
| Dirichlet box D, X = 20/40 | −25.71 / −25.89 | −25.710 / −25.888 (D → −3C) | rounding |

### Exact results reproduced

- **Lowest Y_R = 1 multiplets:** 8(½), 10(3/2), 10̄(½), 27(3/2), 35(5/2), 27(½), 64(5/2), then 35̄(3/2) and 35(3/2) degenerate. The ANW-set and refit energies match the report's spectrum table.
- **Level differences** (sympy):
  - E(10) − E(8) = 3/(2I₁)
  - E(10̄) − E(8) = 3/(2I₂)
  - E(8) − E_SU(2)(N) = 3/(4I₂)
  - E(27, 3/2) − E(10̄) = 3/(2I₁) − 1/(2I₂)
- **N_c parity:** 2J ≡ N_c (mod 2) for every allowed state with N_c = 1–15 (p + q ≤ 30). Every allowed irrep has triality p − q ≡ N_c (mod 3). The lowest-four tables for N_c = 1–7 coincide with the report's, apart from one naming slip (issue 7).
- **⟨D₈₈⟩:** octet (N, Λ, Σ, Ξ) = (3, 1, −1, −2)/10; decuplet = Y/8.
- **Densities.** The PLAN Lagrangian reproduces the report's ε, ⟨i₁₁⟩ = (1/6)s²[1 + 4(F′² + s²/x²)] and ⟨i₄₄⟩ = (1/8)(1 − cos F)(1 + F′² + 2s²/x²), with i₈₈ = 0, no off-diagonal terms, and the report's T_rr and T_θθ. Maximum relative deviation 1.8e-10, the finite-difference floor. This independently confirms I₂ = (π/2)J₂/(e³F_π), i.e. Kopeliovich eq. 22c.
- **Large-x series:** F = C/x² − C³/(21x⁶) − (4/3)C³/x⁸ + 2C⁵/(385x¹⁰) + …, derived in sympy. The report's two correction terms are right. Its residuals at x = 10, 20, 40 are relative values; see issue 8.

### Calibration verdicts with my numbers

| quantity | mine | target, tolerance | result |
|---|---|---|---|
| M_cl | 36.46165 | 36.463 (also 36.5, and SW's 36.44), 0.2% | −0.004% / −0.11% / +0.05%: passes |
| Λ | 50.97874 | 50.9, 0.5% | +0.155%: passes |
| F_π | 129.263 MeV | 129 MeV, 1% | +0.20%: passes |
| e | 5.4440 | 5.45, 1% | −0.11%: passes |
| g_A | 0.6105 | 0.61 ± 0.01 | passes |
| I₂ coefficient | 40.679 | arctan value 40.54, 1.5% | +0.33%: passes |

Spectrum, level differences, virial, von Laue and Derrick all pass.

## A bug on my side

My first, interrupted attempt gave J₂ = 25.89558, which is 4.7e-5 below the original. Diagnosis:

- The integrand used 1 − cos F. In double precision this rounds to exactly 0 once F < ~1.5e-8, that is for x > ~2×10⁴.
- The analytic tail ∫(C²/2)dy over that last stretch of y = 1/x (about 1.2e-3) was therefore silently dropped.
- The giveaway was a geometry-dependent spread of 1.3e-6 in J₂, compared with 1e-10 for everything else.

Writing 1 − cos F as 2 sin²(F/2) removes the problem. My J₂ now agrees with the original to 9e-14. The original is correct; the error was mine.

## Reproducibility of the original

I reran `run_all.sh` in a scratch copy (single thread, 48 s wall):

- `results.json`, `profile.json` and the three figures are byte-identical to the committed ones.
- `out/*.json` differ only in their `runtime_s` fields.
- The figures exist (52–72 KB each) and match the numbers.

The report's reproducibility claim holds.

## Literature checks

- **DPP hep-ph/9703373.** Eq. 6 (Y′ = N_cB/3), eq. 8 (the rotor formula) and eqs. 9–13 (the lowest multiplets and both splittings) are exactly as the report uses them.
- **Praszalowicz hep-ph/0308114.**
  - Eqs. 26–28 give the arctan-ansatz M_cl, I₁ and I₂, with x₀ = √(15/4).
  - My recomputation of eq. 28 gives the coefficient 40.5435, matching the report.
  - The paper does not contain "36.5" or "1.2315" (see issue 3).
- **Acus et al. hep-ph/9605435.**
  - Eqs. 4.9–4.10, converted with x = 2r̃, are the report's g_A bracket.
  - The ANW column of Table 1 reads f_π = 64.5 MeV (F_π = 129), e = 5.45, g_A = 0.61, r₀ = 0.59 fm, μ_p = 1.87, μ_n = −1.31.
- **Schechter–Weigel hep-ph/9907554.**
  - E = 23.2π f_π/e, which is 36.44 F_π/e.
  - α² = 53.3/(e³f_π), which is equivalent to Λ = 50.90.
- **PDG 2026** (pdg 2026.0): λ = g_A/g_V = −1.2753 ± 0.0013. The baryon masses match `results.json` exactly.

## Seed-claim audit

| SEED claim | report | assessment |
|---|---|---|
| §2: fermion iff N_c odd (WZ term) | CONFIRMED | **Supported, conditionally.** It rests on the imported rule Y_R = N_cB/3; the report says so. E2 tests the group theory that follows from the rule, not the WZ mechanism. Reproduced with GT patterns. The proof is right: 2I₃ + 3Y is even on every weight. |
| §4: Derrick, something must push back | CONFIRMED | **Supported.** E₂(μ) = E₂/μ is an exact identity. The sigma-model ODE in t = ln x is damped motion between the two equal maxima of V = cos(2F)/2, so it ends at π/2 and never reaches F = 0. With the Skyrme term, E₂ = E₄ and ∫p d³x = 0. |
| §6B: octet and decuplet lowest | CONFIRMED | **Supported.** The exotic 10̄(½) and 27(3/2) that follow are correctly reported. The order depends only on I₁/I₂, so "at both parameter sets" is automatic. |
| §6B: exact SU(3) gives degenerate multiplets; splittings need extra parameters | CONFIRMED | **Supported.** Degeneracy holds by construction (the rotor H depends only on Casimirs). The optional 2-parameter fit is reproduced exactly. |
| §6B: e is the only pure number | CONFIRMED | **Supported**, but true by construction (dimensional analysis, massless pions, fixed N_c). It is not an empirical test. |
| §6B: within roughly 30% for nucleons | AMENDED | **Supported for g_A** (0.6105 vs 1.2753: −52%). The proposed corrected wording, "most static properties within about 30%", is not shown in E2: F_π is a fit parameter, and radii and moments belong to E5. Mark it provisional. |

## Issues

All are **minor**. None changes a headline number or a seed verdict.

1. **Verdict vocabulary.**
   - The headline tables label N_c parity, Derrick, virial and von Laue CALIBRATED. PLAN reserves CALIBRATED for reproducing a literature target.
   - N_c parity is a preregistered seed prediction and should be CONFIRMED (given the imported WZ rule), as in the report's own seed section.
   - The exact level differences, the "same ordering at both parameter sets" and "e is the only pure number" are identities or dimensional analysis.
2. **The 30% claim.** The AMENDED verdict is earned by g_A. The "corrected statement" that most static properties lie within 30% has no E2 evidence behind it; mark it provisional until E5.
3. **Target provenance.**
   - The plan and report cite "36.5 F_π/e = 1.2315 × 3π²" as [read] in Schechter–Weigel and Praszalowicz, but neither text contains those numbers. SW gives 23.2π f_π/e = 36.44 F_π/e and α² = 53.3/(e³f_π), equivalent to Λ = 50.90. Praszalowicz has only the arctan-ansatz formulas. The 36.5 is ANW's own number.
   - The calibration passes against every version of the target.
   - ANW's F_π, e and g_A can be upgraded from "secondary sources" to [read: Acus et al. Table 1].
4. **Weak I₂ calibration.** The I₂ target is a variational arctan-ansatz value, not a published exact-profile I₂, so the 1.5% test only rules out large formula slips. The I₂ density formula itself is verified independently on both sides.
5. **Hard-coded verdicts.** `collect_results.py` writes CALIBRATED unconditionally for the multiplet ordering, the exact level differences, Derrick and N_c parity. The ordering of the lowest multiplets is printed by `su3_rotor.py` but never asserted. The values are right (reproduced here), but a regression would not change these verdicts.
6. **PDG value.** PDG 2026 g_A/g_V is −1.2753 ± 0.0013; the report quotes 1.2754, the 2024 value. The conclusion (−52%) is unchanged.
7. **Multiplet label.** In the N_c table, (1,3) is written "24" at N_c = 4 and N_c = 7. By the report's own convention (6̄ = (0,2), 15̄ = (1,2)) it is 24̄. `results.json` correctly writes "24=(1,3)".
8. **Cosmetic numeric slips.**
   - The pressure node in `results.json` (2.1522) is a grid-interval midpoint; the root is 2.15237. The report's 2.152 is fine.
   - The asymptotic residuals "6e-7, 2e-9, 5e-10" are relative, which the report does not say. The x = 40 value is solver noise; the series remainder there is about 5e-12.
   - E₂ = E₄ is quoted as "to 6e-13" in one place and "to 4e-13" in another.
   - The report's "−2C = −17.2771564357" does not match the C in its own `results.json`, which gives −2C = −17.2771564286. That C is good only to 4.5e-10.

## Files (crosscheck/)

| file | content |
|---|---|
| `xc_derive.py` | symbolic EL equation, origin and large-x series, D = −2C as a total derivative |
| `xc_hedgehog.py` | two-sided shooting, integrals, virial, von Laue, pressure, Derrick, arctan ansatz, ANW fit; writes `xc_profile.npz` |
| `xc_densities.py` | densities from the PLAN Lagrangian by 3D finite differences |
| `xc_rotor.py` | GT patterns, allowed multiplets, N_c parity, exact level differences, PDG 2026 masses, fits, Weingarten D-function integrals, optional breaking fit |
| `xc_axial.py` | numerical Noether axial current and ball integral, asymptotic residuals, Dirichlet-box biases |
| `xc_collect.py` | comparison with the original's outputs; writes `crosscheck.json` |
| `run_xc.sh` | runs everything (about 40 s, one thread); each script prints its own checks |

Every check passes, and every comparison agrees.
