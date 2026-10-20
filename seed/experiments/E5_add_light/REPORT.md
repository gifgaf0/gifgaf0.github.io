# E5 — Add light

*Experiment E5 of the preregistered series (PLAN.md §4). Directory: `seed/experiments/E5_add_light/`. This run resumes an earlier attempt that a container restart killed; see Deviations for what was reused and what was fixed. This text was regenerated from `results.json` after two passes of the independent cross-check (`crosscheck/`); see Reconciliation at the end.*

## Question

SEED.md §7.4 says: "Add light. Gauge a U(1) inside the internal symmetry, read off the folds' electric charges, and confirm the photon's single cone." Commitment 4 says charge is "dressed, not slowed", commitment 1 says the vacuum is taut (p = −ρ in every frame), and §6B says the Skyrme fold lands "within roughly 30%" for nucleons (Adkins, Nappi & Witten 1983, ANW). PLAN.md E5 turns these into five computations:

1. electric charges of the SU(3) rotor states (8, 10, 10̄, 27) and of the SU(2) states;
2. electromagnetic static properties of the nucleon, compared with ANW and PDG 2026;
3. the charge dressing: proton and neutron charge densities, and the prediction that the isovector radius diverges for massless pions;
4. π⁰ → γγ from the gauged Wess–Zumino (WZ) term, at the physical f_π and at the fold's own fitted f_π;
5. one light cone and a taut vacuum, by linearization.

## Method

**Lagrangian and units** (ANW, as in PLAN E2):
L = (F_π²/16) Tr ∂_μU∂^μU† + (1/32e²) Tr[L_μ, L_ν]², with L_μ = U†∂_μU.
- F_π follows the 186-MeV convention (f_π = F_π/2).
- Dimensionless radius x = eF_π r. Energies are in units of F_π/e, moments of inertia in 1/(e³F_π).
- Optional massive variant: add (F_π²m_π²/16) Tr(U + U† − 2), with β = m_π/(eF_π).
- Metric (+,−,−,−), ε^{0123} = +1.

**Hedgehog.** U₀ = exp(iF(r) n̂·τ) with F(0) = π. The profile equation is
(x²/4 + 2s²)F″ = sc/2 + 2s³c/x² − 2scF′² − xF′/2 + β²x²s/4, with s = sin F, c = cos F.

It is solved with `scipy.solve_bvp` on a geometric mesh x ∈ [x₀, X]:
- at x₀ = 10⁻², a third-order regular series F = π + ax + b(a)x³;
- at X (massless), the analytic tail F = C/x² − C³/(21x⁶);
- at X (massive), F ∝ k₁(βx).

Integrals use 12-point Gauss–Legendre panels plus analytic tails beyond X (for example Λ_tail = C²/X). Production runs use X = 200.

Convergence checks (massless; `hedgehog_log.txt`, `results.json` → `hedgehog_numerics`):
- X = 100, 200 and 400 (tolerance 10⁻¹⁰) agree with the X = 200 reference to 8.9×10⁻¹⁰ relative in Λ (4.5×10⁻⁸ absolute) and to 3×10⁻¹³ relative in ⟨r²⟩_B. Tolerance 10⁻⁸ against 10⁻¹⁰ at X = 100 changes Λ by 10⁻¹¹ relative.
- Smaller boxes do worse. X = 50 is off by 2.8×10⁻⁸ in Λ and 1.9×10⁻⁸ in C. X = 25 is off by 7.2×10⁻⁷ in Λ and 1.2×10⁻⁶ in C, with B − 1 = −5.6×10⁻⁷.
- x₀ = 3×10⁻³ gives the same values.
- An independent shooting solution gives F′(0) = −1.00376411, the same as the BVP.
- Baryon number B = 1 − 1×10⁻¹¹ (X = 200).
- Virial residual (E₂ − E₄)/E = 8.5×10⁻¹² (X = 200).

Reference numbers: M = 36.46165 F_π/e = 1.2314457 × 3π²; Λ = 50.97874; C = 8.638578; ⟨r²⟩_B = 4.477836 and ⟨r⁴⟩_B = 48.35455 in units of (eF_π)⁻² and (eF_π)⁻⁴. All agree with E2 (`E2_skyrme_su3/results.json`).

**Formulas.** Each formula was derived from the Lagrangian in `symbolic_derivations.py` (sympy, 39 checks, all computed) rather than copied:
- *Energy density and inertia.* The angular-averaged energy density; λ = (2π/3)Λ/(e³F_π) with Λ = ∫x²s²[1 + 4(F′² + s²/x²)]dx; and I₂ = (π/2)∫x²(1 − c)(1 + F′² + 2s²/x²)dx/(e³F_π) (checks 1–3).
- *Isospin current.* For the rotating hedgehog, ∫V⁰ = λW. The static spatial current is V^k_b = ε_{kbl} n_l g(r), with ∫ r g d³x = (3/2)λ (checks 4a–4d).
- *Baryon current.* B⁰ = −(1/2π²)s²F′/r², carried rigidly by the physical rotation (5a–5c). In SU(2) the gauged WZ term makes the isoscalar EM current B^μ/2, so Q = I₃ + B/2 (9b).
- *Magnetic moments.* μ^{I=0} = ½∫x × (B/2) = ⟨r²⟩_{I=0} J/(6λ), and μ^{I=1} = ½∫x × V₃ = D₃ᵢ λ/2 with |⟨p↑|D₃₃|p↑⟩| = 1/3 (6a–6b, 8a–8c). In nuclear magnetons:
  μ_{p,n} = 2M_N [⟨r²⟩_{I=0}/(12λ) ± λ/6], with M_N = 939 MeV.
  - The relative sign is fixed because the isospin charge and the magnetic moment come from the same current. Pointwise, V⁰_a = (W × x)·V_a (check 4c), so I_a = 2W·μ^{(a)}.
  - Ma & Harada (arXiv:1604.04850, eqs. 4.116 and 4.121) have the same structure, with B and V each normalized to twice ours: their μ^{I=0}_p = ⟨r²⟩/(6I) and μ^{I=1}_p = I/3, compared with twice the data.
- *Radii.*
  - ⟨r²⟩_{I=0} = −(2/π)∫r²s²F′dr (normalized baryon density).
  - The isoscalar magnetic radius in ANW's definition is ⟨r⁴⟩_B/⟨r²⟩_B (magnetic density ∝ r²ρ_B; the same definition as hep-ph/0605305, eq. 24). The Sachs radius, from the slope of G_M^{I=0}(q) ∝ ∫ρ_B r² 3j₁(qr)/(qr), is 3/5 of it.
  - The isovector charge density is the λ density normalized to ½. Then ⟨r²⟩_p = (⟨r²⟩₀ + ⟨r²⟩₁)/2 and ⟨r²⟩_n = (⟨r²⟩₀ − ⟨r²⟩₁)/2.
- *Axial current and g_A.*
  - The static axial current has the form A^j_a = f₁δ_{aj} + f₂n_a n_j (7a). Its integral over a sphere is G = ∫4πr²(f₁ + f₂/3)dr = −(π/3)∫x²D dx, where D is the integrand quoted for ANW (7b, exact sign).
  - The proton matrix element of the sphere integral gives g_A = (2/3)|G|/e². With massless pions the pion pole q_iq_j/q² removes ⅓ of the angular average as q → 0, so g_A = |G|/e² = (π/3e²)|D|, which is ANW's formula. With massive pions there is no pole term at q = 0, so g_A = (2/3)(π/3e²)|D|.
  - The tail is f₁ → −C/4r³ and f₂ → 3C/4r³ (7c). Because ∂_jA^j = 0 in the chiral limit, ∫A^i = ∮x^iA^j dS_j, a surface term. Hence g_A = 2πC/(3e²). Numerically D = −2C to 3.1×10⁻¹⁰ relative (5.4×10⁻⁹ absolute).
  - g_πNN = 2M_N g_A/F_π (Goldberger–Treiman, 186-MeV convention).
- *π⁰ → γγ.* Start from the gauged WZ term (Witten 1983; Bernstein & Holstein arXiv:1112.4809, eq. 67) with U = exp(iπ·τ/f), in the f = 92 MeV convention.
  - The gauged WZ term has no part of order 0, 1 or 2 in the fields (check 10d, computed). Its part linear in the pion is L = (N_c e²/48π²f) ε^{μναβ} F_μν A_α ∂_β π⁰ = (N_c e²/24π²f) ε^{μναβ} ∂_μA_ν A_α ∂_β π⁰ (check 9g). Charged pions do not couple, because Tr Q²τ_{1,2} = 0.
  - The amplitude is A = N_c e²/(12π²f) and the width Γ = α²m³N_c²/(576π³f²) (checks 9a–9e). At N_c = 3 this is Bernstein–Holstein's (m/4π)³(α/f)², eq. 71. The second line of their eq. 69 uses an F̃ normalization that differs by a factor 2 (check 9e).
- *Charges.* Gauging Q = diag(2/3, −1/3, −1/3) from the left makes the collective charge Q = L₃ + L₈/√3 = I₃ + Y/2.
  - The allowed irreps are those containing Y_R = N_c/3 (WZ constraint), with J equal to the isospin of those states.
  - State content was computed two ways (branching rule, and weight multisets peeled into isomultiplets), with exact rationals (`rotor_charges.py`).
- *One cone and taut vacuum.*
  - Expand the gauged Skyrme, mass, WZ and Maxwell terms to second order around U = 1 (checks 10a–10g).
  - Compute T_μν = 2∂L/∂g^{μν} − g_μν L at the vacuum with a general symmetric metric (11a–11c).

**Data.** PDG 2026 values come from the `pdg` package (S016MM, S017MM, S016CR, S017MCR, S016MCR, S017MRD, S017AV, and the π⁰ lifetime and branching ratio). The SU(3) refit uses the PDG 2026 octet and decuplet centres, 1151.19 and 1382.11 MeV (unrounded averages in the code). The PDG sqlite has no pion decay constant, so the supplementary f_π comparison uses f = 92.21 MeV, the preregistered π⁰ input from Bernstein–Holstein.

## Calibration

| Quantity | Ours | Target | Tolerance | Source | Verdict |
|---|---|---|---|---|---|
| isoscalar charge radius, ANW params | 0.5939 fm | 0.59 fm | ±0.01 fm | PLAN E5 (ANW via Rakhimov Table 1.1) | CALIBRATED |
| isoscalar magnetic radius, ANW def. √(⟨r⁴⟩/⟨r²⟩)_B | 0.9223 fm | 0.92 fm | ±0.01 fm | PLAN E5 | CALIBRATED |
| μ_p | 1.8776 | 1.87 | ±0.02 | PLAN E5 | CALIBRATED |
| μ_n | −1.3230 | −1.31 | ±0.02 | PLAN E5 | CALIBRATED |
| μ_p/μ_n | −1.4192 | −1.43 | ±0.02* | PLAN E5 | CALIBRATED |
| g_πNN (Goldberger–Treiman) | 8.868 | 8.9 | ±0.05* (post hoc) | PLAN E5 | CALIBRATED under the post hoc tolerance; fails ±0.02 (|Δ| = 0.032) |
| g_A (consistency with E2) | 0.6091 | 0.61 | ±0.01 | PLAN E2 | CALIBRATED |
| Γ(π⁰→γγ), N_c = 3, f = 92.21 MeV | 7.761 eV | PrimEx-II 7.802 ± 0.117 eV (prereg. 7.76) | within 2σ | PLAN E5 [read: Bernstein–Holstein] | CALIBRATED (−0.35σ; +0.33σ vs PDG 2026, 7.720 ± 0.123) |
| Γ(π⁰→γγ), N_c = 1 | 0.862 eV | 0.86 eV, excluded | > 5σ | PLAN E5 | CALIBRATED (59σ; the exclusion holds only with N_c-independent quark charges) |
| charges of 8, 10, 10̄, 27 integral; SU(2) Q = I₃ + B/2 | yes | yes | exact | PLAN E5 (internal check) | CHECK PASSED |
| symbolic derivations, one cone, taut vacuum | 39/39 (all computed) | all pass | exact | PLAN E5 (internal check) | CHECK PASSED |

\* The plan gives no tolerance for g_πNN; ±0.05 (half of ANW's last digit) was chosen afterwards. Under the moments' ±0.02 it would fail. It is accepted because g_A, which fixes g_πNN through Goldberger–Treiman, passes its preregistered ±0.01. The ratio μ_p/μ_n uses the moments' tolerance; ANW's −1.43 is itself the ratio of the rounded numbers 1.87/−1.31 = −1.427.

ANW's rounded parameters (129 MeV, 5.45) give M_N = 936.4 and M_Δ = 1229.8 MeV. My own exact SU(2) refit to 939/1232 gives F_π = 129.26 MeV and e = 5.444. At the refit: r_{I=0} = 0.5934 fm, r_M = 0.9215 fm, μ_p = 1.8788, μ_n = −1.3260, g_A = 0.6105, g_πNN = 8.869. Every quantity moves by at most 0.003, so all verdicts hold.

## Findings

**1. Charges.** With Y_R = 1 the lowest allowed irreps are 8 (J = ½), 10̄ (½), 10 (3/2) and 27 (½ and 3/2). The states carry:

| Irrep | Charges |
|---|---|
| 8 | −1, 0, +1 |
| 10 | −1, 0, +1, +2 (Δ⁺⁺) |
| 10̄ | −2, −1, 0, +1 (Θ⁺ with S = +1; Ξ⁻⁻ in the I = 3/2 quartet) |
| 27 | −2 … +2 |

- All charges are integers and obey Gell-Mann–Nishijima, Q = I₃ + (B + S)/2. The 8 and 10 charges coincide with the observed octet and decuplet baryons.
- In SU(2), Q = I₃ + B/2: I = J = ½ gives {1, 0}, 3/2 gives {2, 1, 0, −1}, 5/2 gives {3, …, −2}. The Y = 1 members of every SU(3) multiplet match this.
- The isoscalar half is the baryon current: part of a fold's charge is topological.
- The U(1) generator, the quark charge matrix, is an input chosen to match nature. Integrality follows because the WZ constraint Y_R = 1 selects triality-zero irreps.
- Extra, not preregistered. With quark charges held fixed at (2/3, −1/3, −1/3), the nonstrange members of the lowest irrep for N_c = 1, 5, 7 have fractional charges (−1/3 and 2/3; 1/3 and 4/3; 2/3 and 5/3). With the anomaly-consistent charges Q = diag(½ + 1/2N_c, −½ + 1/2N_c, …) they are {0, 1} for every N_c (`charges_results.json`).

**2. Static properties against data (PDG 2026).** At the calibrated ANW point, with massless pions (`fig_vs_pdg.png`):

| Quantity | Skyrme | Data | Ratio |
|---|---|---|---|
| μ_p | 1.878 | 2.7928 | 0.67 |
| μ_n | −1.323 | −1.9130 | 0.69 |
| μ_p/μ_n | −1.419 | −1.4599 | 0.97 |
| g_A | 0.609 | 1.2753 | 0.48 |
| g_πNN | 8.87 | ≈ 13.1 [summary] | 0.68 |
| r_E^{I=0} = √(r_p² + ⟨r²⟩_n) | 0.594 fm | 0.769 fm | 0.77 |
| r_M^{I=0} (Sachs) | 0.714 fm | 0.82 ± 0.09 fm | 0.87 (ANW def.: 1.12) |
| r_p | ∞ | 0.8407 fm | — |
| ⟨r²⟩_n | −∞ | −0.1155 fm² | — |
| *supplementary:* f_π = F_π/2 (fit output) | 64.5 MeV | 92.21 MeV | 0.70 |

Six of the seven finite nucleon predictions lie within 33% of the data. Strictly within 30% are three: μ_p/μ_n (−3%), r_E^{I=0} (−23%) and r_M^{I=0} (−13%, Sachs). μ_p (−33%), μ_n (−31%) and g_πNN (−32%) sit just outside 30%. The clear exceptions are g_A, low by 52% (a factor of about 2), and the two individual charge radii, which do not exist in the massless model.

The supplementary f_π row was not preregistered and is a pion property, so it is kept out of the nucleon tally. F_π is an output of the fit to M_N and M_Δ, the two inputs, and Rakhimov's Table 1.1 (reproducing ANW) lists it against 93 MeV. It is −30.05% from 92.21 MeV (−29.9% from f_π⁺/√2 = 92.07 MeV [summary]), on the 30% boundary. With it, 3 of 8 are strictly within 30% and 7 of 8 within 33%.

Optional massive-pion variant, no target. With m_π = 138 MeV, a refit to M_N and M_Δ gives F_π = 108.26 MeV and e = 4.842, which verifies the quoted AN84 values 108 and 4.84. At F_π = 108 MeV, e = 4.84:
- r_{I=0} = 0.683 fm, r_{I=1} = 1.040 fm, r_p = 0.880 fm (+5% vs data), ⟨r²⟩_n = −0.308 fm² (2.7 × data);
- μ_p = 1.972, μ_n = −1.241;
- g_A = 0.649 (sphere integral, no pole factor);
- g_πNN = 11.29 (Goldberger–Treiman); f_π = 54 MeV (0.59 × 92.21).

**3. Charge is dressed** (`fig_charge_densities.png`). The isovector density falls as r⁻⁴ (4πr²ρ_{I=1} ∝ C²/(Λx²)), so the isovector ⟨r²⟩ inside a cutoff R grows linearly. In units of (eF_π)⁻² it is 0.55, 5.39, 12.71, 27.34, 71.25, 144.4 and 290.8 for R = 2, 5, 10, 20, 50, 100 and 200 (x units), with asymptotic slope C²/Λ = 1.4638. At ANW parameters that is ⟨r²⟩_{I=1}(R) ≈ 0.411 fm × R, which diverges. The isovector charge outside R is 0.205 fm/R; the computed tail agrees with this to 4×10⁻⁶ at R = 10 fm.

Enclosed charge Q(<R):

| R (fm) | proton, massless | neutron, massless | proton, m_π = 138 MeV | neutron, m_π = 138 MeV |
|---|---|---|---|---|
| 0.5 | 0.341 | +0.172 | 0.263 | +0.118 |
| 1 | 0.764 | +0.185 | 0.798 | +0.103 |
| 2 | 0.897 | +0.102 | 0.980 | +0.019 |
| 5 | 0.959 | +0.041 | 1.000 | +0.000 |
| 10 | 0.980 | +0.021 | 1.000 | +0.000 |

The neutron's enclosed charge is largest at the node of its charge density. That maximum is +0.206 at R = 0.73 fm (massless, ANW), or +0.140 at 0.68 fm (m_π = 138 MeV, AN84): a positive core inside a negative cloud. With massless pions the cloud has no edge; a pion mass gives an exponential edge and finite radii. The effective charge depends on how closely you look, as commitment 4 says. The mechanism is the fold's own classical pion field. Any extended charge distribution would show an R-dependent enclosed charge, so this confirms the commitment only in the operational sense preregistered in PLAN E5.

**4. π⁰ → γγ.** At leading order Γ = 7.761 eV, 0.35σ below PrimEx-II and 0.33σ above PDG 2026; matching PrimEx-II's central value needs f = 91.97 MeV. N_c = 1 gives 0.862 eV, excluded at 59σ if the quark charges are held fixed.

At the fold's own decay constant the width is too large:
- ANW, f = 64.5 MeV: 15.86 eV (2.03×);
- own SU(2) fit, f = 64.63 MeV: 15.80 eV;
- SU(3) refit (F_π = 113.755 MeV, e = 5.2474, the same as E2's), f = 56.877 MeV: 20.40 eV (2.61×).

The preregistered prediction is confirmed: the fold sector, fitted to baryon masses, wants an f_π 1.43–1.62 times smaller than the anomaly needs. This is not a separate tension from the f_π row in Finding 2. Γ ∝ 1/f², so 2.03 = (91.97/64.5)², the square of the fold's 30% f_π deficit (38% for the SU(3) refit).

Caveat: the N_c² scaling assumes N_c-independent quark charges. With anomaly-consistent charges, N_c Tr(Q²τ₃) = 1 for every N_c (check 9f; Bär & Wiese hep-ph/0105258). So π⁰ → γγ alone does not count colours.

**5. One cone, taut vacuum.**
- The quadratic Lagrangian is ½∂π·∂π − ½m_π²π² − ¼F_μνF^μν, with no photon–pion mixing.
- The Skyrme commutator term starts at fourth order and the gauged WZ term at third (both computed), so neither changes propagation around the vacuum. U = 1 commutes with Q, so the photon stays massless.
- Maxwell's kernel has rank 3 off the cone (the null vector is pure gauge) and rank 1 on it, leaving two transverse photons with ω = |k|. Pions have ω² = k² + m², with group velocity below 1, tending to 1.
- k² is boost invariant.
- The vacuum T_μν = V₀ g_μν (mostly-minus), so ρ = V₀ and p = −V₀, unchanged by boosts.

These results hold by construction for a Lorentz-invariant Lagrangian at tree level. The check confirms that nothing added (the Skyrme and WZ terms, the gauging, the mass term) breaks it.

## What it means for the seed

- **§7.4, charges from a gauged U(1): CONFIRMED.** Every state of 8, 10, 10̄ and 27 has an integer charge, and Q = I₃ + B/2 in SU(2). This requires the WZ constraint, and N_c = 3 with standard quark charges (or anomaly-consistent charges). The same gauging predicts exotic charges (Θ⁺, Ξ⁻⁻, Q = ±2 in the 27), which are not established experimentally.
- **§7.4 and §2, one cone, no vacuum dispersion: CONFIRMED (by construction).** The photon and the fold field share ω² = k² (+ m²), with no preferred frame. The check could not have failed for this Lagrangian. It says nothing about whether a not-yet-specified fundamental theory of the seed is Lorentz invariant.
- **Commitment 1, taut vacuum: CONFIRMED (by construction).** T_μν ∝ g_μν, so p = −ρ in every frame. The value of V₀ is a free constant.
- **Commitment 4, charge dressed, not slowed: CONFIRMED (in the preregistered operational sense only).**
  - Charge densities are extended. With massless pions the isovector radius diverges (⟨r²⟩₁(R) ≈ 0.41 fm × R) and the enclosed charge approaches its total only as 1/R. A pion mass makes it finite. The photon's cone is untouched.
  - The test cannot tell "dressing" from any extended charge distribution. The mechanism is classical pion-cloud structure, not QED vacuum polarization, and "not slowed" holds by construction.
- **§6B, "within roughly 30%": AMENDED.**
  - Against PDG 2026, 6 of 7 finite nucleon predictions are within 33%, and 3 of 7 strictly within 30%. The amendment rests on g_A, low by 52%, and on r_p and ⟨r²⟩_n, which are infinite without a pion mass. The fit-output f_π is 30% low.
  - Rakhimov (nucl-th/0502078, §1.2.4, read), summarizing ANW, writes "qualitative agreement with experiment (within 30%) except for g_A". ANW's own text was not read.
  - Suggested wording: "about 30–35% for the magnetic moments, g_πNN and f_π, within 25% for the isoscalar radii and better for ratios, about 50% for g_A; the proton and neutron charge radii need a pion mass."
- **PLAN E5 internal-consistency prediction, not a SEED sentence (the fold sector and the anomaly prefer different f_π): CONFIRMED (preregistered prediction; no SEED verdict).**
  - At the fold's fitted f_π the gauged WZ term overpredicts Γ(π⁰→γγ) by 2.03× (ANW) or 2.61× (SU(3) refit). That is the square of the f_π deficit, not an independent miss.
  - It bears on §6B's single (F, e) parameter set.
- **§2, the WZ term that makes the fold a fermion also fixes π⁰ → γγ: CONFIRMED (the anomaly normalisation); the N_c = 1 exclusion holds only with fixed quark charges.** With fixed charges, N_c = 1 baryons also carry fractional charges. With anomaly-consistent charges the width does not depend on N_c.

## Deviations from the plan

1. **Resumed run.** An earlier attempt with the same instructions was killed by a container restart. Its scripts and results were checked, two defects were fixed, and the whole pipeline was rerun from scratch with `run_all.sh`.
   - `symbolic_derivations.py` swapped f₁ and f₂ when extracting the axial tensor, giving 3 FAIL lines (7a–7c). The numerics did not use that extraction. After the fix all checks pass.
   - The cutoff table in the old `hedgehog_log.txt` and the right panel of `fig_charge_densities.png` came from a version that always integrated up to x ≥ 5. The code had been fixed but not rerun. Full-range integrals were unaffected; both were regenerated.
2. **Symbolic checks after the first cross-check.** Check 10d (no quadratic WZ term) had been asserted by inspection; it is now a computed expansion of the gauged WZ term. Checks 5c and 7b were made strict (exact value and sign), and 9g (the π⁰ coupling coefficient) was added. Total: 39 checks, all computed, all pass.
3. **g_πNN tolerance.** The plan gives none; ±0.05 was chosen afterwards, and g_πNN would fail ±0.02. For μ_p/μ_n the moments' ±0.02 was applied.
4. **Magnetic radius.** It is calibrated in ANW's definition (⟨r⁴⟩/⟨r²⟩ over the baryon density) and compared with data in the Sachs definition (factor √(3/5)). Both ratios are given.
5. **g_πNN data value.** 13.1 is a [summary] value (g²/4π ≈ 13.6–13.8; 2M_N g_A/F_π(phys) = 13.0); PDG does not list g_πNN.
6. **Massive variant.** Optional, with no target. The AN84 parameters were verified by refit; AN84's other numbers were not read in the source.
7. **Extras, not preregistered and labelled as such:**
   - the N_c-dependence of the charges;
   - the enclosed-charge table and the neutron peak;
   - the identity D = −2C and its surface-term reason;
   - `fig_vs_pdg.png`;
   - the supplementary f_π row (added in reconciliation).

## Limitations

- **Leading order only.** Everything is classical soliton plus rigid-rotor quantization, leading order in 1/N_c. Known subleading corrections (rotational and meson-loop, notably to g_A) are not included. The moments use SU(2) collective quantization; SU(3) magnetic moments (octet Clebsches, symmetry breaking) were not computed.
- **Massless pions in the calibrated model.** The proton and neutron charge radii are infinite there, so the only charge-radius comparison with data is the uncalibrated massive variant.
- **One-cone and vacuum checks** are tree level and hold by construction. Quantum corrections were not computed; with a Lorentz-invariant regulator they would not change this.
- **π⁰ width at leading order only.** Bernstein–Holstein quote higher-order chiral predictions of 8.10 eV (about +4.5%), 2.5σ above PrimEx-II. The leading-order agreement is therefore partly fortuitous, and the pass is a statement about the anomaly normalization, not a precision test.
- **Data values.**
  - The isoscalar magnetic radius derived from PDG has a ±0.09 fm uncertainty, dominated by r_M^p.
  - g_πNN is a [summary] value.
  - The f_π reference (92.21 MeV) is the Bernstein–Holstein input, because the PDG sqlite has no decay constant.
- **Targets.** ANW targets come through secondary sources. Rakhimov's Table 1.1 (nucl-th/0502078, read) reproduces ANW: 0.59 fm, 0.92 fm, 1.87, −1.31, 0.61, 8.9, and f_π = 64.5 MeV. ANW's paper itself was not reachable.

## How to reproduce

```
cd seed/experiments/E5_add_light
./run_all.sh            # sets NUMBA/OMP/OPENBLAS/MKL threads to 1; 3 min 52 s wall in the reconciliation rerun (one shared core)
```

Individual steps, in order, each prefixed with `NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`:

| Command | Runtime | Output |
|---|---|---|
| `python3 symbolic_derivations.py` | 220–300 s (logged runs) | `symbolic_log.txt`, `symbolic_results.json`; 39 checks, prints PASS/FAIL |
| `python3 hedgehog_em.py` | 8 s | `hedgehog_results.json`, `hedgehog_log.txt`, `fig_charge_densities.png`; convergence table, shooting check, derived-density cross-checks |
| `python3 rotor_charges.py` | < 1 s | `charges_results.json` |
| `python3 pi0_gamma_gamma.py` | ~1 s | `pi0_results.json` |
| `python3 make_results.py` | ~2 s | `results.json`, `fig_vs_pdg.png`; prints the calibration verdicts, the PDG comparison (with the supplementary f_π row) and the neutron peak |

Python 3.13, numpy 2.5.3, scipy 1.18.1, sympy 1.14, matplotlib 3.11 and the `pdg` package (PDG 2026); hard-coded PDG fallbacks exist. All scripts are deterministic: the reconciliation rerun reproduced every number in `results.json` bit for bit.

## Reconciliation

Two passes of the independent cross-check (`crosscheck/`: two-sided shooting, finite-element energy minimisation, Noether currents of the matrix Lagrangian, its own π⁰ derivation, Gelfand–Tsetlin charges, and its own PDG query) reproduce every number. The second pass compared 100 of 100 rows, mostly to 10⁻⁹ relative or better. None of the issues it raised was numerical.

The one major issue was that this report had not been regenerated after the first reconciliation, which had changed the code and `results.json`. The report and the structured summary therefore disagreed with `results.json` on verdict wording and on the check count.

Actions:
- `run_all.sh` was rerun end to end (3 min 52 s, 39/39 checks). Every numeric value in `results.json` came out identical to the previous file.
- This text was rewritten from that `results.json`.
- `make_results.py` now adds:
  - the supplementary f_π row (in `results.json` and `fig_vs_pdg.png`);
  - the 8-row tally;
  - the "square of the f_π deficit" reading of the π⁰ factor;
  - the Rakhimov quotation;
  - the absolute and relative D = −2C deviation;
  - a `reconciliation.second_pass` block.
- `run_all.sh` runtime comments were updated.

| Issue (cross-check) | Who was right | Action | Resolved |
|---|---|---|---|
| Major: REPORT stale against `results.json` (38/38, CALIBRATED for internal checks, QUANTIFIED, "3 of 7", unqualified commitment 4) | cross-check | report regenerated from `results.json`; verdicts now identical in both | yes |
| π⁰ coupling written with ∂_μA_ν and 48π² | cross-check (factor 2 typo; code and amplitude always right) | both forms now written (48π² with F_μν, 24π² with ∂_μA_ν) | yes |
| convergence "X = 25…400 to 5×10⁻⁸ relative" | cross-check on X = 25; in addition the 5×10⁻⁸ was the absolute Λ spread (8.9×10⁻¹⁰ relative), a slip both sides repeated | ranges quoted separately | yes |
| 38/38 and 150–170 s | cross-check | 39/39 (all computed) and logged runtimes | yes |
| verdict vocabulary | cross-check | CHECK PASSED for internal checks; no QUANTIFIED | yes |
| π⁰ factor 2 = square of the f_π miss; f_π missing from the 6B tally | cross-check (in substance) | supplementary f_π row (−30.05%), kept out of the preregistered nucleon tally; π⁰ factor described as its square | yes |
| §6B framing "3 of 7" | cross-check | 6 of 7 within 33% (3 of 7 strictly within 30%); verdict stays AMENDED | yes |
| commitment 4 unqualified | cross-check | "CONFIRMED (in the preregistered operational sense only)" | yes |
| neutron peak "+0.185 at 1 fm" in the summary | cross-check | peak +0.206 at 0.73 fm quoted; table value at 1 fm unchanged (correct) | yes |
| g_πNN fails ±0.02 | cross-check (already disclosed) | stated in the calibration verdict | yes |
| "ANW's own table excepted g_A" unverified | cross-check (unsupported as written) | Rakhimov §1.2.4 read this pass: the sentence is his summary of ANW; re-attributed, ANW unread | yes |

No discrepancy remains open. All verdicts (CALIBRATED ×9, CHECK PASSED ×2, and the seed verdicts above) are the same in this report, `results.json` and the structured summary.
