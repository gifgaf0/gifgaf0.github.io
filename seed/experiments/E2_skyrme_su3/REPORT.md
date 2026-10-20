# E2: the fold in SU(2) and SU(3)

*Experiment E2 of the preregistered series (PLAN.md §4). It tests three claims in SEED.md: §2 (spin from the Wess–Zumino term), §4 (Derrick) and §6B (octet and decuplet from the Skyrme hedgehog). Computed October 18–19, 2026. The independent second computation is in `crosscheck/`. It agreed with every number here and raised eight minor issues. All eight were reconciled on October 19, 2026: the corrections are folded into the text below and listed in the Reconciliation section at the end.*

## Question

1. Does the Skyrme model, the seed's Model B, reproduce the published numbers for the B = 1 hedgehog? These are the classical mass, the moments of inertia, the Adkins–Nappi–Witten (ANW) fit and g_A.
2. Quantised as an SU(3) rigid rotor with the Wess–Zumino constraint, are its lowest states the octet and the decuplet?
3. Are its folds fermions exactly when N_c is odd?
4. Does it satisfy Derrick's theorem, the virial theorem and the von Laue condition?

## Method

### Conventions

PLAN.md E2 conventions are used throughout:

    L = (F_π²/16) Tr ∂_μU ∂^μU† + (1/(32e²)) Tr [L_μ, L_ν]²,   L_μ = U†∂_μU,

- F_π is in the 186 MeV convention (f_π = F_π/2).
- Pions are massless.
- The dimensionless radius is x = eF_π r.

The B = 1 hedgehog is U₀ = exp(iτ·r̂ F(r)), with F(0) = π and F → C/x² at large x. For SU(3) it is embedded in the upper-left 2×2 block.

### Static equations

- Classical mass:

        M = 4π (F_π/e) ∫dx x² [ (1/8)(F′² + 2s²/x²) + (1/2)(s²/x²)(s²/x² + 2F′²) ],   s = sin F

- Euler–Lagrange equation:

        (x² + 8s²) F″ + 2x F′ + 4 sin2F F′² − sin2F − 4 sin2F s²/x² = 0

- Moments of inertia:

        I₁ = (2π/3) Λ/(e³F_π),   Λ  = ∫ x² s² [1 + 4(F′² + s²/x²)] dx
        I₂ = (π/2)  J₂/(e³F_π),  J₂ = ∫ x² (1 − cos F)[1 + F′² + 2s²/x²] dx   (Kopeliovich hep-th/9707067 eq. 22c)

- Axial coupling. This is ANW's expression; we read it in Acus et al. hep-ph/9605435 eqs. 4.9–4.10, with x = 2r̃:

        g_A = −(π/(3e²)) D,   D = ∫ x² [F′ + sin2F/x + 4(sin2F F′²/x + 2s²F′/x² + s² sin2F/x³)] dx

### Large-x asymptotics

Derived and checked numerically:

    F = C/x² − C³/(21x⁶) − (4/3)C³/x⁸ + O(x⁻¹⁰)

The x⁻⁶ term comes from the sigma-model nonlinearity and the x⁻⁸ term from the Skyrme term.

Fit to the solved profile, as relative deviations at x = 10, 20 and 40:

| form | x = 10 | x = 20 | x = 40 |
|---|---|---|---|
| three-term series | 6.0e-7 | 1.4e-9 | 4.3e-12 |
| C/x² alone | 4.5e-4 | 2.4e-5 | 1.4e-6 |

C itself is read off at x = 100 with the same series. The x = 40 figure is therefore a consistency check of the series, not a fully independent one.

This expansion supplies the analytic tails. Λ and J₂ converge only like C²/X.

### Deriving the densities (verify_densities.py)

The energy density, the full 8×8 inertia-tensor density, the axial Noether current and the stress tensor were all computed from explicit 3×3 matrices:

- U = A U₀ A†, with A ∈ SU(3) and A†Ȧ = (i/2)λ_aΩ_a.
- Then L₀ = A(U₀†wU₀ − w)A† and L_i = AU₀†∂_iU₀A†.
- The rotational Lagrangian is −(1/16)Tr L₀² − (1/16)Σ_i Tr[L₀, L_i]² = ½ i_ab Ω_a Ω_b.

These were evaluated at 12 random (x, F, F′) points and averaged with exact angular quadrature (12 Gauss–Legendre × 16 trapezoid points). They were then compared with the radial formulas above. Results:

- The energy density and the i_aa agree with the radial formulas to ≤ 5e-15 relative. The i_aa for a = 1–3 give I₁ and those for a = 4–7 give I₂. This derives Kopeliovich's I₂ expression rather than trusting it.
- i₈₈ and all off-diagonal i_ab vanish.
- The stress tensor agrees with T_rr and T_θθ as used in the von Laue check, to 1e-12.
- The integrated 8×8 inertia tensor of the solved profile is diagonal: (I₁ ×3, I₂ ×4, 0).

### SU(2) and SU(3) rotors

- SU(2) rotor (ANW): E = M + J(J+1)/(2I₁), with N at J = ½ and Δ at J = 3/2.
- SU(3) rotor (Diakonov–Petrov–Polyakov hep-ph/9703373):

        E(p,q,J) = M + C₂(p,q)/(2I₂) + (1/(2I₁) − 1/(2I₂)) J(J+1) − N_c²/(24I₂),   C₂ = (p² + q² + pq + 3(p+q))/3

- Wess–Zumino constraint: Y_R = N_c B/3. An irrep is allowed if it contains states with hypercharge N_c/3, and the isospin of those states is the spin J.
- The constraint is taken from the literature (Witten 1983; DPP). This experiment does not derive it from the WZ term.

How the rotor results were computed:

- Irreps up to dimension 64 were built explicitly (tensor powers, highest-weight vector, lowering operators). For each one we checked the Casimirs, the commutators [T_a, T_b] = i f_abc T_c and the Gelfand–Tsetlin content.
- The rotor Hamiltonian was built from these generators. It agrees with the closed formula on every Y = 1 state.
- Level differences are computed in exact rational arithmetic.
- The order of the lowest six levels is asserted by a check (added in reconciliation; before, it was printed but not tested).
- D^(8) matrix elements come from Clebsch–Gordan intertwiners obtained as null spaces. They reproduce Praszalowicz hep-ph/0308114 eqs. 17–19: all 12 diagonal elements and all 28 second-order coefficients.
- The same intertwiners give ⟨p↑|D₃₃|p↑⟩ = −1/3 for SU(2) and −7/30 for the SU(3) octet.

Irrep naming: (p, q) with p < q is the barred irrep, for example 24 = (3,1) and 24̄ = (1,3).

### Fits

1. **ANW fit.** The SU(2) rotor is fitted to M_N = 939 and M_Δ = 1232 MeV.
2. **SU(3) refit.** The SU(3) rotor is fitted to the octet and decuplet centres, with the ratio I₁/I₂ fixed by the profile.
   - The centres are state-weighted averages over isospin multiplets: (2N + Λ + 3Σ + 2Ξ)/8 and (4Δ + 3Σ* + 2Ξ* + Ω)/10.
   - The masses are from PDG 2026 (`pdg` package, 2026.0 sqlite). The isospin-averaged values used, in MeV:

| N | Λ | Σ | Ξ | Δ | Σ* | Ξ* | Ω |
|---|---|---|---|---|---|---|---|
| 938.919 | 1115.683 | 1193.154 | 1318.286 | 1232 | 1384.610 | 1533.387 | 1672.452 |

For Δ we used the PDG Breit–Wigner value for mixed charges, 1230–1234 MeV. The resulting centres are 1151.194 and 1382.106 MeV.

The comparison value for g_A is also from the `pdg` package (PDG 2026 S017AV): λ = g_A/g_V = −1.2753 ± 0.0013.

### Discretization and convergence (skyrme_hedgehog.py)

Chebyshev collocation with Newton iteration was run in three setups, plus an independent cross-check:

- **(B) Whole half line**, x = L(1+t)/(1−t). F is analytic in t because the asymptotic series is in 1/x² with no logarithms, so no truncation or tail is needed. This is the reference used for the headline numbers.
- **(A) Box [0, X]** with the Robin condition F′ + 2F/x = 0 at X plus analytic tails, as the experiment notes instruct. A variant with two more asymptotic orders in the Robin condition was also run.
- **(C) Box with Dirichlet F(X) = 0 and no tails**, run to show the bias.
- **Cross-check:** scipy `solve_bvp` on [10⁻³, 40] with the Robin condition and the same tails, integrated with adaptive quadrature.

| run | M/(F_π/e) | Λ | J₂ | D |
|---|---|---|---|---|
| (B) N = 40 | 36.461645627693 | 50.97871622 | 25.89677817 | −17.277273 |
| (B) N = 80 | 36.461645625237 | 50.97873911 | 25.89678962 | −17.2771564 |
| (B) N = 160 (reference) | 36.461645625237 | 50.97873911 | 25.89678962 | −17.27715644 |
| (B) N = 160, L = 1 and L = 4 | same to 1e-15 | same to 7e-13 | same to 8e-13 | same to 6e-13 |
| (A) X = 10, tails | 36.461645710 | 50.96235 (−3.2e-4) | 25.88832 | −17.28222 |
| (A) X = 40, tails | 36.461645625 | 50.97873 (−2.1e-7) | 25.89678 | −17.27717 |
| (A) X = 80, tails | 36.461645625 | 50.978739 (−7e-9) | 25.896789 | −17.277157 |
| (A) X = 40, no tails | — | 49.113 (−3.7%) | 24.964 (−3.6%) | — |
| (A) X = 20, improved Robin | 36.461645625 | 50.97873913 | 25.89678963 | −17.277157 |
| (C) Dirichlet X = 20 / 40 | +0.120% / +0.015% | −13.5% / −6.6% | −13.5% / −6.6% | −25.71 / −25.89 |
| solve_bvp, X = 40 | 36.461645607 | 50.9787232 | 25.8967816 | — |

Other properties of the reference solution:

- C = 8.6385782182 and F′(0) = −1.0037641114.
- C is read from F(100) through the asymptotic series. Before reconciliation it came from the spectral second derivative at the end point of the mapped grid, which is good only to 4.5e-10 and is now kept as a diagnostic.
- Baryon number B = 1 to 1e-14.

Two lessons for anyone redoing this:

1. Λ and J₂ need the 1/x² tail. Truncating the integral at X, or imposing F(X) = 0, biases them by several percent even at X = 40.
2. The Dirichlet box also biases g_A, by +50%. D for the true profile equals −2C (shown below). A Dirichlet box drops the C boundary term, giving D ≈ −3C.

The `solve_bvp` run stopped at its node limit (status 1) before reaching tol 1e-10. It still agrees with the spectral solution to 5e-10 in M and 3e-7 in Λ.

### g_A: what the formula means (verify_densities.py part iii)

The ANW bracket D can be compared with the axial Noether current of the static hedgehog, normalised so that ⟨0|A^a_μ|π^b⟩ = i f_π p_μ:

- The current is ⟨A^a_j⟩ = −(1/12) δ_aj × [ANW bracket].
- Its integral over a ball is a pure surface term, because ∂_iA_i = 0. It gives only 2/3 of ANW's g_A (0.407 at the ANW fit).
- We computed the Fourier transform of the current for q = 0.2 down to 0.01:
  - its longitudinal part vanishes (|A₃₃| < 1e-4);
  - its transverse part tends to exactly 3/2 of the ball integral (ratio 1.49995 at q = 0.01). This is the massless-pion-pole effect.
- So ANW's g_A = −(π/(3e²))D is the q → 0 transverse form factor.
- Current conservation also gives D = −2C: D = −17.2771564364 and −2C = −17.2771564364, equal to 1e-12. Hence g_A = 2πC/(3e²).

### Derrick, virial and von Laue (derrick_virial.py)

- E₂(μ) and E₄(μ) were computed for the dilated profile F(μx). Quadrature: 400-point Gauss–Legendre on the mapped half line, with N = 140 spectral interpolation.
- The radial sigma-model equation x²F″ + 2xF′ − sin2F = 0 was shot from F = π − ax for a = 0.1, 1 and 10, out to x = e⁴⁰.
- Stress tensor:

        T_rr = (1/8)(F′² − 2s²/x²) + (s²/(2x²))(2F′² − s²/x²),   T_θθ = −(1/8)F′² + s⁴/(2x⁴)

  with p = (T_rr + 2T_θθ)/3.
- The checks: ∫x²p dx = 0, and local equilibrium T_rr′ + 2(T_rr − T_θθ)/x = 0.
- The pressure node is located with a root finder (Brent). p(0) uses the exact small-x value −a²/8 + a⁴/2, with a = −F′(0).

## Calibration

### Literature targets (PLAN §4 E2)

| quantity | ours | target | tolerance | source | verdict |
|---|---|---|---|---|---|
| M_cl | 36.461646 F_π/e = 1.2314457 × 3π² F_π/e | 1.2315 × 3π² = 36.463 F_π/e (PLAN; written there as 36.5) | 0.2% | [read] Schechter–Weigel hep-ph/9907554 §2: E = 23.2π f_π/e = 36.44 F_π/e. 36.5 is ANW's value (secondary sources); 1.2315 × 3π² is the standard value (not read) | CALIBRATED (−0.004% vs 36.463; −0.11% vs 36.5; +0.05% vs 36.44) |
| Λ (I₁ = (2π/3)Λ/(e³F_π)) | 50.97874 | 50.9 (ANW) | 0.5% | [read] Schechter–Weigel: α² = 53.3/(e³f_π), i.e. Λ = 3 × 53.3/π = 50.90 | CALIBRATED (+0.155%) |
| ANW fit F_π | 129.26 MeV | 129 MeV | 1% | [read] Acus et al. hep-ph/9605435 Table 1, ANW column (f_π = 64.5 MeV) | CALIBRATED (+0.20%) |
| ANW fit e | 5.4440 | 5.45 | 1% | [read] Acus et al. Table 1 | CALIBRATED (−0.11%) |
| g_A at ANW fit | 0.6105 | 0.61 | ±0.01 | [read] Acus et al. Table 1; formula Acus et al. eqs. 4.9–4.10 | CALIBRATED |
| I₂ coefficient (π/2)J₂ | 40.6786 | ≈ 40.5 (arctan ansatz; recomputed here 40.5435) | exact within 1.5% of it | Praszalowicz eqs. 26–28 [read] (formulas; the number is computed from them); I₂ formula Kopeliovich 22c [read], derived here | CALIBRATED (+0.44% / +0.33%); a weak calibration, since the target is a variational value |
| lowest Y_R = 1 multiplets | 8 (½), 10 (3/2), 10̄ (½), 27 (3/2), 35 (5/2), 27 (½) | 8 (½), 10 (3/2), 10̄ (½), then 27 | exact | DPP hep-ph/9703373 [read] | CALIBRATED |
| E(10) − E(8) | 3/(2I₁) | 3/(2I₁) | exact | DPP [read] | CALIBRATED |
| E(10̄) − E(8) | 3/(2I₂) | 3/(2I₂) | exact | DPP [read] | CALIBRATED |

Notes on the table:

- **The I₂ row.** It compares the exact profile with an arctan-ansatz value, not with a published exact-profile I₂. It can only rule out formula slips larger than 1.5%. The I₂ density itself is verified independently on both sides: explicit SU(3) matrices here (5e-15), finite differences of the Lagrangian in the cross-check (7e-11).
- **The last three rows** are algebraic consequences of the DPP rotor formula and the WZ rule. They calibrate the irrep, Casimir and rotor code, not new physics. The order of the levels depends only on I₁/I₂, so "at both parameter sets" is one test. All three verdicts are derived from asserted checks in `su3_rotor.py`.

### Seed-claim tests and internal checks (PLAN §4 E2: "Fermion iff N_c odd", "Derrick and virial")

PLAN reserves CALIBRATED for literature targets. Here, PASS marks an internal consistency check with a preregistered tolerance; PASS is not one of PLAN's verdict words. In the first report these four rows were labelled CALIBRATED; see Reconciliation.

| quantity | ours | expectation | tolerance | verdict |
|---|---|---|---|---|
| virial E₂/E₄ − 1 | −4.4e-13 (independent quadrature +5.6e-13) | 0 | 1e-4 | PASS |
| von Laue ∫p d³x / ∫\|p\| d³x | −6.8e-13 | 0 | numerical zero | PASS |
| Derrick, no Skyrme term (SEED §4) | E₂(μ) = E₂/μ, strictly decreasing; sigma-model ODE ends at F = π/2 | no minimum | qualitative | CONFIRMED |
| N_c parity, B = 1 (SEED §2) | 2J ≡ N_c (mod 2) for all allowed states, N_c = 1–15 | J half-integer iff N_c odd | exact | CONFIRMED, given the imported WZ rule |

### Preregistered expectations

These have no tolerance; they are expectations, not literature values.

| quantity | ours | expectation | verdict |
|---|---|---|---|
| E(8) − E_SU(2)(N) at ANW parameters, = 3/(4I₂) | 384.5 MeV | ≈ 385 MeV | NO_TARGET, agrees |
| SU(3) refit: F_π | 113.75 MeV | ≈ 114 MeV | NO_TARGET, agrees |
| SU(3) refit: e | 5.2474 | ≈ 5.25 | NO_TARGET, agrees |
| SU(3) refit: E(10̄) | 1757.3 MeV | near 1760 MeV | NO_TARGET, agrees |

No calibration missed, so no miss needed diagnosing.

Two remarks:

- **The small excess of Λ over 50.9 (+0.16%).** It is in the direction a finite-box or truncated-tail computation would produce, since both bias Λ downward. We did not try to reconstruct how the original 50.9 was obtained.
- **The ANW (F_π, e) are rounded values.**
  - Using ANW's own M = 36.5 and Λ = 50.9 in our fit formulas gives F_π = 129.1 MeV and e = 5.443.
  - Using Schechter–Weigel's 23.2π f_π/e and 53.3/(e³f_π) gives F_π = 129.26 MeV and e = 5.441.

## Findings

### 1. The hedgehog

Dimensionless profile numbers:

- M = 36.461646 F_π/e.
- I₁ = 106.7696/(e³F_π) and I₂ = 40.6786/(e³F_π), so I₁/I₂ = 2.6247.
- C = 8.6385782.
- ⟨r²⟩_B (eF_π)² = 4.47784.

At the ANW fit (eF_π = 703.7 MeV, so ħc/(eF_π) = 0.2804 fm):

- M_cl = 865.75 MeV.
- 1/I₁ = 195.33 MeV and 1/I₂ = 512.69 MeV (I₁ = 1.010 fm, I₂ = 0.385 fm).
- The baryon rms radius is 0.593 fm.

`profile.json` stores F(x) and F′(x) on 0 ≤ x ≤ 100 for other experiments. Beyond x = 100, use the stored asymptotic series. Figure: `fig_profile.png`.

### 2. Stability balance

- E₂ = E₄ = 18.230823 F_π/e. E₂/E₄ − 1 = −4.4e-13 in the reference solution, and +5.6e-13 from the independent quadrature in `derrick_virial.py`.
- The dilation curve E(μ) = E₂/μ + μE₄ has its minimum at μ* = 1.0000000001.
- With only the stretching term, E(μ) = E₂/μ falls without bound as the fold shrinks (μ → ∞).
- The sigma-model radial equation has no B = 1 solution. Started at F(0) = π with any slope, it settles at F = π/2 (it is a damped pendulum in ln x).
- The pressure:
  - It is positive in the core: p(0) = −a²/8 + a⁴/2 = 0.38163 in units of (F_π/e)(eF_π)³.
  - It has a single node at x = 2.15237 (0.60 fm at ANW parameters) and is negative outside.
  - It integrates to zero to 7e-13.

Figures: `fig_derrick.png`, `fig_profile.png` (right panel).

### 3. SU(3) spectrum (exact SU(3), rigid rotor, N_c = 3)

The exact level formulas are:

- E(8) − M = 3/(8I₁) + 3/(4I₂)
- E(10) − E(8) = 3/(2I₁)
- E(10̄) − E(8) = 3/(2I₂)
- E(8) − E_SU(2)(N) = 3/(4I₂)

Lowest allowed levels, in MeV:

| multiplet (J) | ANW set (F_π = 129.26 MeV, e = 5.444) | SU(3) refit (F_π = 113.75 MeV, e = 5.247) |
|---|---|---|
| 8 (½) | 1323.5 | 1151.2 (fit input) |
| 10 (3/2) | 1616.5 | 1382.1 (fit input) |
| 10̄ (½) | 2092.6 | 1757.3 |
| 27 (3/2) | 2129 | 1786 |
| 35 (5/2) | 2361 | 1969 |
| 27 (½) | 2605 | 2161 |
| 64 (5/2) | 3130 | 2575 |
| 35 (3/2), 35̄ (3/2) | 3155 | 2594 |

At the ANW parameters:

- The SU(3) rotor puts the octet 384.5 MeV above the SU(2) nucleon. That is 15% above the PDG octet centre; the decuplet is 17% above its centre.
- The ANW-fitted I₁ gives E(10) − E(8) = 293 MeV, against 230.9 MeV between the PDG centres.

The SU(3) refit therefore wants smaller F_π and e. At the refit:

- M_cl = 790.4 MeV.
- 1/I₁ = 153.9 MeV and 1/I₂ = 404.1 MeV.

The exotic 10̄ (J = ½) and 27 (J = 3/2) lie close together. Their gap is 3/(2I₁) − 1/(2I₂): about 37 MeV at the ANW set and 29 MeV at the refit. PDG 2026 lists no established exotic multiplet. Figure: `fig_spectrum.png`.

With exact SU(3), all d_R(2J+1) states of each multiplet are degenerate. This was checked on the explicit 8, 10 and 10̄ matrices.

### 4. N_c parity

| N_c | lowest allowed multiplets (J) | spins |
|---|---|---|
| 1 | 3 (½), 6̄ (½), 15 (3/2), 15 (½) | all half-integer |
| 2 | 3̄ (0), 6 (1), 15̄ (1), 24 (2) | all integer |
| 3 | 8 (½), 10 (3/2), 10̄ (½), 27 (3/2) | all half-integer |
| 4 | 6̄ (0), 15 (1), 15′ (2), 24̄ (1) | all integer |
| 5 | 15̄ (½), 24 (3/2), 21 (5/2), 15̄′ (½) | all half-integer |
| 6 | 10̄ (0), 27 (1), 35 (2), 28 (3) | all integer |
| 7 | 24̄ (½), 42 (3/2), 48 (5/2), 21̄ (½) | all half-integer |

Coverage: all irreps with p + q ≤ 16 for N_c = 1–7, and with p + q ≤ 30 for N_c ≤ 15. Every allowed irrep has triality matching N_c.

The rule is exact. On every SU(3) weight, 2I₃ + 3Y is an even integer: it equals 2(p+q) at the highest weight and changes by −2 or −4 under the lowering operators. So Y = N_c/3 forces 2J ≡ N_c (mod 2).

### 5. Extras (not preregistered; labelled)

- **g_A.** The ANW value is the q → 0 transverse form factor, 3/2 of the ball integral of the current, and D = −2C exactly (see Method).
  - In the SU(3)-symmetric rotor, the leading term carries ⟨p↑|D₃₃|p↑⟩ = −7/30 instead of −1/3, so g_A drops by the factor 7/10.
  - At the SU(3) refit, g_A = 0.657 with the SU(2) factor, or 0.460 with the SU(3) factor.
  - PDG 2026: g_A/g_V = −1.2753 ± 0.0013.
- **Optional symmetry breaking.** H′ = −α D⁽⁸⁾₈₈ + βY at first order, with the multiplet centres fixed. Two fitted inputs: α = 371.8 MeV, β = −99.6 MeV.
  - It reproduces the 8 PDG isospin multiplets with rms 4.0 MeV. The largest residual is Ξ, +6.9 MeV.
  - It implies the following relations identically. PDG 2026 values (LHS − RHS):
    - Guadagnini, 8(N + Ξ*) + 3Σ = 11Λ + 8Σ*: +8.5 MeV (+0.036%)
    - Gell-Mann–Okubo: −25.8 MeV (−0.57%)
    - decuplet equal spacing: +3.8 and +9.7 MeV
  - This is a fit, not a prediction of the masses.

## What it means for the seed

- **§2: "For SU(3) … the Wess–Zumino term supplies the sign … the fold is a fermion when N_c is odd." CONFIRMED,** given the WZ quantisation rule Y_R = N_c B/3. With that rule, every B = 1 rotor state has half-integer spin exactly when N_c is odd (checked for N_c = 1–15, with a one-line proof). The rule is taken from Witten and DPP. This experiment checks the group theory that follows from it, not the rule itself.
- **§4: "a static fold can't be held by gradient energy alone (Derrick 1964) … Something has to push back." CONFIRMED.**
  - Without the Skyrme term, the energy scales as 1/μ and has no minimum, and the radial equation has no B = 1 solution.
  - With the Skyrme term, the solution satisfies E₂ = E₄ and ∫p d³x = 0, both to about 1e-12.
- **§6B: "Quantize its rotations and the lowest states fill the octet … and the decuplet." CONFIRMED.**
  - These are the two lowest allowed multiplets, with the right spins. The order depends only on I₁/I₂, so it is the same at both parameter sets.
  - The seed should add that the same rotor next predicts exotic multiplets, 10̄ (J = ½) and 27 (J = 3/2). They sit about 600 MeV above the octet at the SU(3) refit and about 770 MeV above it at the ANW set. No established states match them.
- **§6B: "With exact SU(3) … every member of the octet has one mass … the splittings … need a symmetry-breaking term … which brings in more parameters." CONFIRMED.** The rotor states are exactly degenerate. At first order, two fitted parameters reproduce the splittings to 4 MeV rms and imply Guadagnini's relation.
- **§6B: "F sets the units and e is the only pure number, so every prediction is a ratio." CONFIRMED,** for massless pions and fixed N_c. This is true by construction (dimensional analysis). A pion mass would add m_π/(eF_π).
- **§6B: "For nucleons the model lands within roughly 30% (ANW 1983)." AMENDED.**
  - The masses are fit inputs.
  - The one non-fit nucleon static property E2 computes is g_A. At 0.61, against |g_A/g_V| = 1.2753(13), it is 52% low, outside 30%. The SU(3)-symmetric rotor lowers it further, to 0.46 at the refit.
  - Whether the radii and magnetic moments land within 30% is E5's test. E2 makes no claim about them.
  - Context only: the fitted F_π = 129 MeV is 30.5% below 186 MeV, if the masses are regarded as the inputs. The SU(3) octet and decuplet at ANW parameters are 15–17% high.

  The corrected statement, on E2's evidence: g_A misses by about a factor of two. The broader "most static properties within about 30%" reading of the first version of this report is withdrawn here, because E2 does not show it.

## Deviations from the plan

1. **Reference solution.** The headline numbers come from the whole-half-line Chebyshev solution, which needs no truncation. The box + Robin + analytic-tails method from the experiment notes was also run. It agrees to 2e-7 at X = 40 and 7e-9 at X = 80. No verdict depends on the choice.
2. **The M_cl and Λ targets.**
   - The plan writes "36.5 F_π/e, i.e. 1.2315 × 3π² F_π/e". These differ by 0.10%: 1.2315 × 3π² = 36.463. We compared to 36.463.
   - The plan marks both numbers [read: Schechter–Weigel, Praszalowicz]. Neither appears in those texts (checked in reconciliation by reading them).
     - Schechter–Weigel give E = 23.2π f_π/e = 36.44 F_π/e and α² = 53.3/(e³f_π), which is Λ = 50.90.
     - Praszalowicz gives only the arctan-ansatz formulas.
     - 36.5 and 50.9 are ANW's values.
   - Our M_cl is inside 0.2% of all three versions of the target, and Λ is inside 0.5% of both.
3. **Additions beyond the plan,** all labelled above as extras or optional: the g_A analysis, the D⁽⁸⁾ matrix elements, the SU(3) factor 7/10, the pressure profile, and the first-order symmetry-breaking fit with two named inputs.
4. **The scipy cross-check** stopped at its node limit (status 1), short of its requested tolerance. It is a secondary check, and it agrees to 3e-7.
5. **Process.**
   - This is a resumed attempt. The computations were done by a previous agent, which was interrupted by a container restart. The resumed run re-executed the whole pipeline and reproduced its outputs.
   - The reconciliation then changed five files: `skyrme_hedgehog.py`, `su3_rotor.py`, `derrick_virial.py`, `collect_results.py` and `run_all.sh`. It reran everything.
   - What changed in `results.json`, `profile.json` and `out/*.json`:
     - C and D, at the 1e-10 level;
     - the pressure node, at 1e-4;
     - verdict words and provenance notes.
   - The figures are byte-identical. `results.json` is identical on a second rerun.
   - This report is returned to the orchestrator rather than written to disk by the agent.
6. **Verdict words relabelled after the cross-check (no number changed).** N_c parity and Derrick are seed claims and now read CONFIRMED. Virial and von Laue are internal checks and now read PASS. All four had been labelled CALIBRATED.

## Limitations

- **Rigid-rotor semiclassics only.** There are no quantum loop or Casimir corrections, no breathing or vibrational modes, and no rotation-induced deformation. The expansion is in 1/N_c, and for the 10̄ and 27 the rigid rotor is least reliable. The 1757 MeV antidecuplet is a rigid-rotor, exact-SU(3), massless-pion number. It is not a prediction to compare with any claimed exotic state.
- **Massless pions.** I₁, I₂ and g_A are sensitive to the long pion tail. A physical pion mass would change them and adds a second pure number.
- **The Wess–Zumino constraint** Y_R = N_c B/3 is imported, not derived. The parity result rests on it.
- **The embedded hedgehog.** Only the SU(2) hedgehog embedded in SU(3) was used. Its stability against genuinely SU(3) deformations was not tested here, though the literature takes it as the B = 1 minimum.
- **Target provenance.**
  - M_cl and Λ are [read] in Schechter–Weigel, in the forms 23.2π f_π/e and 53.3/(e³f_π).
  - The ANW fit (F_π, e) and g_A are [read] in Acus et al. Table 1, ANW column.
  - The I₂ target is an arctan-ansatz value computed from Praszalowicz's formulas [read].
  - The spectrum targets were read in DPP.
  - ANW's own paper was not read.
- **The g_A definition.** g_A depends on the definition by a factor of 3/2: ball integral vs form factor. We report the ANW (form-factor) definition, which is the calibration target.

## How to reproduce

    cd seed/experiments/E2_skyrme_su3
    NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 sh run_all.sh

Requirements:

- Python 3.13, numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.
- The `pdg` package (PDG 2026 sqlite) for the baryon masses and g_A/g_V. If it is missing, `su3_rotor.py` falls back to an embedded table of the same values and says so.

The pipeline is deterministic and single-threaded. Each script prints its own PASS/FAIL checks, and the run ends with `all checks pass: True`.

Wall-clock times on one shared core (reconciliation rerun; total about 48 s):

| script | what it does | wall time |
|---|---|---|
| `skyrme_hedgehog.py` | profile, convergence studies, D = −2C check; writes `profile.json`, `out/hedgehog.json` | 8.1 s |
| `verify_densities.py` | explicit SU(3)-matrix derivation of the densities, I₂ formula, g_A factor 3/2, stress tensor; writes `out/verify.json` | 17.4 s |
| `su3_rotor.py` | irreps, rotor, asserted level ordering, fits, N_c parity, D⁽⁸⁾ elements, optional breaking, PDG g_A/g_V; writes `out/rotor.json` | 19.5 s |
| `derrick_virial.py` | scaling, sigma-model shooting, von Laue, pressure node (root); writes `out/derrick.json` | 1.6 s |
| `make_figures.py` | `fig_profile.png`, `fig_derrick.png`, `fig_spectrum.png` (each < 75 KB) | 1.6 s |
| `collect_results.py` | `results.json`: headline numbers with units, targets, tolerances, verdicts derived from asserted checks, PDG inputs, seed-claim verdicts, reconciliation list | 0.3 s |

The full log of this run is in `out/run_all.log`.

## Reconciliation

The independent cross-check (`crosscheck/`) recomputed every headline number with separate code: shooting instead of collocation, finite differences of the Lagrangian, Gelfand–Tsetlin patterns and Weingarten integrals. All numbers agreed, and its overall verdict was "confirmed with corrections". It raised eight issues, all minor; none was blocking or major. For each issue we read both codes and the cited literature and fixed the original where it was wrong. On every issue the cross-check was right. On one point (8b) its diagnosis is refined.

| # | issue | diagnosis | action | resolved |
|---|---|---|---|---|
| 1 | Verdict vocabulary: N_c parity, Derrick, virial and von Laue labelled CALIBRATED | PLAN reserves CALIBRATED for literature targets. N_c parity and Derrick are seed claims; virial and von Laue are internal checks. The ordering and level differences are PLAN literature targets [read: DPP] but algebraic identities of the rotor formula | Relabelled: N_c parity and Derrick CONFIRMED; virial and von Laue PASS. Ordering and level differences stay CALIBRATED, with a note. No number changed | yes |
| 2 | The corrected 30% reading ("most static properties within about 30%") is not shown in E2 | Right: g_A is the only non-fit nucleon observable here; radii and moments are E5's test | AMENDED kept on the g_A evidence (−52%); the clause is withdrawn from E2's verdict | yes |
| 3 | Target provenance: "36.5 = 1.2315 × 3π²" not in the cited [read] texts | Right; checked by converting the PDFs. Schechter–Weigel §2: E = 23.2π f_π/e, α² = 53.3/(e³f_π). Praszalowicz: arctan formulas only (eqs. 25–28). Acus et al. Table 1, ANW column: f_π = 64.5 MeV, e = 5.45, g_A = 0.61 | Provenance corrected in `results.json` and here. M_cl passes against 36.463, 36.5 and 36.44; Λ passes against 50.90. ANW numbers upgraded to [read]. PLAN.md (outside this directory) keeps the overstated label; flagged for the series summary | yes |
| 4 | The I₂ target is an arctan-ansatz value | Right: a weak calibration | Stated in the table and in `results.json`; verdict unchanged | yes |
| 5 | `collect_results.py` hard-coded CALIBRATED; the multiplet ordering was not asserted | Right | New check in `su3_rotor.py` asserts the lowest six levels at both sets. Every exact or qualitative verdict is now derived from asserted checks | yes |
| 6 | PDG 2026 g_A quoted as 1.2754 | Right: pdg 2026.0 S017AV gives −1.275335 ± 0.001263, i.e. −1.2753(13); 1.2754 is the 2024 value | Read from the `pdg` package; quoted as 1.2753(13). The −52% is unchanged | yes |
| 7 | (1,3) written "24" at N_c = 4 and 7 | Right: by the report's own convention it is 24̄; `irrep_name` lacked (3,1) and (1,3) | Names added; table and notes corrected | yes |
| 8a | Pressure node 2.1522 was a grid midpoint | Right | Brent root: x = 2.1523729, agreeing with the cross-check to 1e-13. p(0) from the exact formula: 0.381628 | yes |
| 8b | Asymptotic residuals "6e-7, 2e-9, 5e-10": relative, and the x = 40 value called solver noise | Partly right. They are relative, but the 5e-10 at x = 40 was not solver noise: it was the 4.5e-10 error in C (see 8d) | With the corrected C: 6.0e-7, 1.4e-9 and 4.3e-12, matching the cross-check's remainder estimate (~5e-12) | yes |
| 8c | "E₂ = E₄ to 6e-13" vs "4e-13" | Both genuine: −4.4e-13 (reference solution) and +5.6e-13 (independent quadrature) | Both quoted | yes |
| 8d | The report's −2C = −17.2771564357 did not match the `results.json` C | C came from the spectral second derivative at the end point of the mapped grid. That estimate is good only to ~5e-10 and is noisy in N (7e-10 at N = 200). D = bulk + C inherited the error, and `verify_densities.py` printed a third value from its own N = 120 solve | C is now read from F(100) through the asymptotic series. A new check requires D/(−2C) − 1 < 1e-11 (it is −1.1e-12). C, D and g_A changed by 4.5e-10, 2.3e-10 and 2.3e-10 | yes |

After reconciliation, our numbers agree with the cross-check as follows:

| quantity | ours | relative difference from the cross-check |
|---|---|---|
| C | 8.63857821821941 | 6.6e-13 |
| D | −17.277156436420 | 1.6e-13 |
| g_A (ANW fit) | 0.6104737137667 | 6e-13 |
| pressure node | 2.1523728647 | 1e-13 |
| M_cl, Λ, J₂, I₁/I₂ | unchanged | ≤ 4e-13 |

No CALIBRATED verdict changed, no seed-claim verdict changed, and nothing is left OPEN. `results.json`, this report and the seed-claim verdicts are consistent.

One downstream note: E3's `make_results.py` compares its own profile with E2's `profile.json`. The stored C moved by 4.5e-10, which does not affect that comparison.
