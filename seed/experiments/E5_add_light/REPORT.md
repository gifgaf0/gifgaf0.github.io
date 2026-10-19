# E5 — Add light

*Experiment E5 of the preregistered series (PLAN.md §4). Directory: `seed/experiments/E5_add_light/`. This run resumes an earlier attempt that a container restart killed; see Deviations for what was reused and what was fixed. The independent cross-check in `crosscheck/` is not part of this report.*

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

Integrals use 12-point Gauss–Legendre panels plus analytic tails beyond X (for example Λ_tail = C²/X).

Convergence checks (massless; `hedgehog_log.txt`):
- X = 25, 50, 100, 200, 400 and tolerance 10⁻⁸ vs 10⁻¹⁰ agree to within 5×10⁻⁸ relative in Λ and better than 10⁻¹¹ in ⟨r²⟩_B;
- x₀ = 3×10⁻³ gives the same values;
- an independent shooting solution gives F′(0) = −1.00376411, the same as the BVP;
- baryon number B = 1 − 10⁻¹¹;
- virial residual (E₂ − E₄)/E = 8×10⁻¹².

Reference numbers: M = 36.46165 F_π/e = 1.2314457 × 3π²; Λ = 50.97874; C = 8.638578; ⟨r²⟩_B = 4.477836 and ⟨r⁴⟩_B = 48.35455 in units of (eF_π)^-2 and (eF_π)^-4. All agree with E2 (`E2_skyrme_su3/results.json`).

**Formulas.** Each formula was derived from the Lagrangian in `symbolic_derivations.py` (sympy, 38 checks) rather than copied:
- *Energy density and inertia.* The angular-averaged energy density, λ = (2π/3)Λ/(e³F_π) with Λ = ∫x²s²[1 + 4(F′² + s²/x²)]dx, and I₂ = (π/2)∫x²(1 − c)(1 + F′² + 2s²/x²)dx/(e³F_π) (checks 1–3).
- *Isospin current.* For the rotating hedgehog, ∫V⁰ = λW. The static spatial current is V^k_b = ε_{kbl} n_l g(r), with ∫ r g d³x = (3/2)λ (checks 4a–4d).
- *Baryon current.* B⁰ = −(1/2π²)s²F′/r², carried rigidly by the physical rotation (5a–5b). In SU(2) the gauged WZ term makes the isoscalar EM current B^μ/2, so Q = I₃ + B/2 (9b).
- *Magnetic moments.* μ^{I=0} = ½∫x × (B/2) = ⟨r²⟩_{I=0} J/(6λ), and μ^{I=1} = ½∫x × V₃ = D₃ᵢ λ/2 with ⟨p↑|D₃₃|p↑⟩ = 1/3 in magnitude (6a–6b, 8a–8c). In nuclear magnetons:
  μ_{p,n} = 2M_N [⟨r²⟩_{I=0}/(12λ) ± λ/6], with M_N = 939 MeV.
  - The sign is fixed because the isospin charge and the magnetic moment come from the same current. Pointwise, V⁰_a = (W × x)·V_a (check 4c), so I_a = 2W·μ^{(a)}.
  - Ma & Harada (arXiv:1604.04850, eqs. 4.116 and 4.121) have the same structure, with B and V each normalized to twice ours: their μ^{I=0}_p = ⟨r²⟩/(6I) and μ^{I=1}_p = I/3, compared with twice the data.
- *Radii.*
  - ⟨r²⟩_{I=0} = −(2/π)∫r²s²F′dr (normalized baryon density).
  - The isoscalar magnetic radius in ANW's definition is ⟨r⁴⟩_B/⟨r²⟩_B (magnetic density ∝ r²ρ_B; the same definition is used in hep-ph/0605305, eq. 24). The Sachs radius, from the slope of G_M^{I=0}(q) ∝ ∫ρ_B r² 3j₁(qr)/(qr), is 3/5 of it.
  - The isovector charge density is the λ density normalized to ½. Then ⟨r²⟩_p = (⟨r²⟩₀ + ⟨r²⟩₁)/2 and ⟨r²⟩_n = (⟨r²⟩₀ − ⟨r²⟩₁)/2.
- *Axial current and g_A.*
  - The static axial current has the form A^j_a = f₁δ_{aj} + f₂n_a n_j (7a). Its integral over a sphere is G = ∫4πr²(f₁ + f₂/3)dr = −(π/3)∫x²D dx, where D is the integrand quoted for ANW (7b).
  - The proton matrix element gives g_A = (2/3)|G|/e² for the sphere integral. With massless pions the pion pole q_iq_j/q² removes ⅓ of the angular average as q → 0, so g_A = |G|/e² = (π/3e²)|D|, which is ANW's formula. With massive pions there is no pole term at q = 0, so g_A = (2/3)(π/3e²)|D|.
  - The tail is f₁ → −C/4r³ and f₂ → 3C/4r³ (7c). Because ∂_jA^j = 0 in the chiral limit, ∫A^i = ∮x^iA^j dS_j, a surface term. Hence g_A = 2πC/(3e²). Numerically D = −2C to 3×10⁻¹⁰ relative.
  - g_πNN = 2M_N g_A/F_π (Goldberger–Treiman, 186-MeV convention).
- *π⁰ → γγ.* Start from the gauged WZ term (Witten 1983; Bernstein & Holstein arXiv:1112.4809, eq. 67) with U = exp(iπ·τ/f) and f = 92 MeV convention.
  - Its part linear in the pion is L = (N_c e²/48π²f) ε^{μναβ}∂_μA_ν A_α ∂_β π⁰. Charged pions do not couple, because Tr Q²τ_{1,2} = 0.
  - The amplitude is A = N_c e²/(12π²f) and the width Γ = α²m³N_c²/(576π³f²) (checks 9a–9e). At N_c = 3 this is Bernstein–Holstein's (m/4π)³(α/f)², eq. 71. Their eq. 69, second line, uses a factor-2 different F̃ normalization (check 9e).
- *Charges.* Gauging Q = diag(2/3, −1/3, −1/3) from the left makes the collective charge Q = L₃ + L₈/√3 = I₃ + Y/2.
  - The allowed irreps are those containing Y_R = N_c/3 (WZ constraint), with J equal to the isospin of those states.
  - State content was computed two ways (branching rule, and weight multisets peeled into isomultiplets), with exact rationals (`rotor_charges.py`).
- *One cone and taut vacuum.*
  - Expand the gauged Skyrme, mass, WZ and Maxwell terms to second order around U = 1 (checks 10a–10g).
  - Compute T_μν = 2∂L/∂g^{μν} − g_μν L at the vacuum with a general symmetric metric (11a–11c).

**PDG 2026** values come from the `pdg` package (S016MM, S017MM, S016CR, S017MCR, S016MCR, S017MRD, S017AV and the π⁰ lifetime and branching ratio). The octet and decuplet centers (1151.19 and 1382.11 MeV) are used for the SU(3) refit.

## Calibration

| Quantity | Ours | Target | Tolerance | Source | Verdict |
|---|---|---|---|---|---|
| isoscalar charge radius, ANW params | 0.5939 fm | 0.59 fm | ±0.01 fm | PLAN E5 (ANW, secondary) | CALIBRATED |
| isoscalar magnetic radius, ANW def. √(⟨r⁴⟩/⟨r²⟩)_B | 0.9223 fm | 0.92 fm | ±0.01 fm | PLAN E5 | CALIBRATED |
| μ_p | 1.8776 | 1.87 | ±0.02 | PLAN E5 | CALIBRATED |
| μ_n | −1.3230 | −1.31 | ±0.02 | PLAN E5 | CALIBRATED |
| μ_p/μ_n | −1.4192 | −1.43 | ±0.02* | PLAN E5 | CALIBRATED |
| g_πNN (Goldberger–Treiman) | 8.868 | 8.9 | ±0.05* | PLAN E5 | CALIBRATED |
| g_A (consistency with E2) | 0.6091 | 0.61 | ±0.01 | PLAN E2 | CALIBRATED |
| Γ(π⁰→γγ), N_c = 3, f = 92.21 MeV | 7.761 eV | PrimEx-II 7.802 ± 0.117 eV (prereg. 7.76) | within 2σ | PLAN E5 [read: Bernstein–Holstein] | CALIBRATED (−0.35σ; +0.33σ vs PDG 2026, 7.720 ± 0.123) |
| Γ(π⁰→γγ), N_c = 1 | 0.862 eV | 0.86 eV, excluded | > 5σ | PLAN E5 | CALIBRATED (59σ) |
| charges of 8, 10, 10̄, 27 integral; SU(2) Q = I₃ + B/2 | yes | yes | exact | PLAN E5 | CALIBRATED |
| symbolic derivations, one cone, taut vacuum | 38/38 | all pass | exact | PLAN E5 | CALIBRATED |

\* The plan gives no tolerance for g_πNN; ±0.05 (half of ANW's last digit) was chosen afterwards. The ratio uses the moments' tolerance. ANW's −1.43 is itself the ratio of the rounded numbers 1.87/−1.31 = −1.427.

ANW's rounded parameters (129 MeV, 5.45) give M_N = 936.4 and M_Δ = 1229.8 MeV. My own exact SU(2) refit to 939/1232 gives F_π = 129.26 MeV and e = 5.444. At the refit: r_{I=0} = 0.5934 fm, r_M = 0.9215 fm, μ_p = 1.8788, μ_n = −1.3260, g_A = 0.6105, g_πNN = 8.869. Every quantity moves by at most 0.003, so all verdicts hold.

## Findings

**1. Charges.** With Y_R = 1 the lowest allowed irreps are 8 (J = ½), 10̄ (½), 10 (3/2) and 27 (½ and 3/2). The states carry:

| Irrep | Charges |
|---|---|
| 8 | −1, 0, +1 |
| 10 | −1, 0, +1, +2 (Δ⁺⁺) |
| 10̄ | −2, −1, 0, +1 (Θ⁺ with S = +1; Ξ⁻⁻ in the I = 3/2 quartet) |
| 27 | −2 … +2 |

- All charges are integers and obey Gell-Mann–Nishijima, Q = I₃ + (B + S)/2.
- In SU(2), Q = I₃ + B/2: I = J = ½ gives {1, 0}, 3/2 gives {2, 1, 0, −1}, 5/2 gives {3, …, −2}. The Y = 1 members of every SU(3) multiplet match this.
- The isoscalar half is the baryon current: part of a fold's charge is topological.
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

Three of the seven finite predictions lie within 30% of the data. μ_p, μ_n and g_πNN miss by 31–33%, and g_A by 52%. The two individual charge radii do not exist in the massless model.

Optional massive-pion variant, no target (m_π = 138 MeV; refit to M_N and M_Δ gives F_π = 108.26 MeV, e = 4.842, which verifies the quoted AN84 values 108 and 4.84). At F_π = 108 MeV, e = 4.84:
- r_{I=0} = 0.683 fm, r_{I=1} = 1.040 fm, r_p = 0.880 fm (+5% vs data), ⟨r²⟩_n = −0.308 fm² (2.7 × data);
- μ_p = 1.972, μ_n = −1.241;
- g_A = 0.649 (sphere integral, no pole factor);
- g_πNN = 11.29 (Goldberger–Treiman).

**3. Charge is dressed** (`fig_charge_densities.png`). The isovector density falls as r⁻⁴ (4πr²ρ_{I=1} ∝ C²/(Λx²)), so the isovector ⟨r²⟩ inside a cutoff R grows linearly. In units of (eF_π)^-2 it is 0.55, 5.39, 12.71, 27.34, 71.25, 144.4 and 290.8 for R = 2, 5, 10, 20, 50, 100 and 200 (x units), with asymptotic slope C²/Λ = 1.4638. At ANW parameters that is ⟨r²⟩_{I=1}(R) ≈ 0.411 fm × R, which diverges. The isovector charge outside R is 0.205 fm/R; the computed tail agrees with this to 10⁻⁶ at R = 10 fm.

Enclosed charge Q(<R):

| R (fm) | proton, massless | neutron, massless | proton, m_π = 138 MeV | neutron, m_π = 138 MeV |
|---|---|---|---|---|
| 0.5 | 0.341 | +0.172 | 0.263 | +0.118 |
| 1 | 0.764 | +0.185 | 0.798 | +0.103 |
| 2 | 0.897 | +0.102 | 0.980 | +0.019 |
| 5 | 0.959 | +0.041 | 1.000 | +0.000 |
| 10 | 0.980 | +0.021 | 1.000 | +0.000 |

The neutron has a positive core inside a negative cloud. With massless pions the cloud has no edge; a pion mass gives an exponential edge and finite radii. The effective charge depends on how closely you look, as commitment 4 says. The mechanism is the fold's own classical pion field.

**4. π⁰ → γγ.** At leading order Γ = 7.761 eV, 0.35σ below PrimEx-II and 0.33σ above PDG 2026; matching PrimEx-II's central value needs f = 91.97 MeV. N_c = 1 gives 0.862 eV, excluded at 59σ.

At the fold's own decay constant the width is too large:
- ANW, f = 64.5 MeV: 15.86 eV (2.03×);
- own SU(2) fit, f = 64.63 MeV: 15.80 eV;
- SU(3) refit (F_π = 113.755 MeV, e = 5.2474, the same as E2's), f = 56.877 MeV: 20.40 eV (2.61×).

The preregistered tension is confirmed. The fold sector, fitted to baryon masses, wants f_π a factor 1.43–1.62 below the value the anomaly needs.

Caveat: N_c² scaling assumes N_c-independent quark charges. With anomaly-consistent charges, N_c Tr(Q²τ₃) = 1 for every N_c (check 9f; Bär & Wiese hep-ph/0105258). So π⁰ → γγ alone does not count colours.

**5. One cone, taut vacuum.**
- The quadratic Lagrangian is ½∂π·∂π − ½m_π²π² − ¼F_μνF^μν, with no photon–pion mixing.
- The Skyrme commutator term starts at fourth order and the WZ term at third, so neither changes propagation around the vacuum. U = 1 commutes with Q, so the photon stays massless.
- Maxwell's kernel has rank 3 off the cone (the null vector is pure gauge) and rank 1 on it, leaving two transverse photons with ω = |k|. Pions have ω² = k² + m², with group velocity below 1, tending to 1.
- k² is boost invariant.
- The vacuum T_μν = V₀ g_μν (mostly-minus), so ρ = V₀, p = −V₀, and it is unchanged by boosts.

These results hold by construction for a Lorentz-invariant Lagrangian at tree level. The check confirms that nothing added (the Skyrme and WZ terms, the gauging, the mass term) breaks it.

## What it means for the seed

- **§7.4, charges from a gauged U(1): CONFIRMED.** Integer charges for every state of 8, 10, 10̄ and 27, and Q = I₃ + B/2 in SU(2). This requires the WZ constraint, and N_c = 3 with standard quark charges (or anomaly-consistent charges). The same gauging predicts exotic charges (Θ⁺, Ξ⁻⁻, Q = ±2 in the 27), which are not established experimentally.
- **§7.4 and §2, one cone, no vacuum dispersion: CONFIRMED (by construction).** The photon and the fold field share ω² = k² (+ m²), with no preferred frame. The check could not have failed for this Lagrangian. It says nothing about whether an as-yet-unspecified fundamental theory of the seed is Lorentz invariant.
- **Commitment 1, taut vacuum: CONFIRMED (by construction).** T_μν ∝ g_μν, so p = −ρ in every frame. The value of V₀ is a free constant.
- **Commitment 4, charge dressed, not slowed: CONFIRMED.** Charge densities are extended. With massless pions the isovector radius diverges (⟨r²⟩₁(R) ≈ 0.41 fm × R) and the enclosed charge approaches its total only as 1/R. A pion mass makes it finite. The photon's cone is untouched. The dressing shown is classical pion-cloud structure, not QED vacuum polarization.
- **§6B, "within roughly 30%": AMENDED.** Against PDG 2026, 3 of 7 finite predictions are within 30% (μ_p/μ_n, both isoscalar radii). μ_p, μ_n and g_πNN miss by 31–33%, g_A by 52%, and r_p and ⟨r²⟩_n are infinite without a pion mass. ANW's own table (as reproduced by Rakhimov) already excepted g_A. Suggested wording: "about 30–35% for magnetic moments and isoscalar radii, about 50% for g_A, better for ratios; the proton and neutron charge radii need a pion mass."
- **§6B, one parameter set for all predictions (anomaly sector included): QUANTIFIED.** At the fold's fitted f_π the gauged WZ term overpredicts Γ(π⁰→γγ) by 2.03× (ANW) or 2.61× (SU(3) refit). The physical f_π is 1.43–1.62× the fold's.
- **§2, the WZ term that makes the fold a fermion also gives π⁰ → γγ: CONFIRMED,** with the caveat that excluding N_c = 1 assumes N_c-independent quark charges.

## Deviations from the plan

1. **Resumed run.** An earlier attempt with the same instructions was killed by a container restart. Its scripts and results were checked, two defects were fixed, and the whole pipeline was rerun from scratch with `run_all.sh`.
   - `symbolic_derivations.py` swapped f₁ and f₂ when extracting the axial tensor, giving 3 FAIL lines (7a–7c). The numerics did not use that extraction. After the fix: 38/38.
   - The cutoff table in the old `hedgehog_log.txt` and the right panel of `fig_charge_densities.png` came from a version that always integrated up to x ≥ 5. The code had been fixed but not rerun. Full-range integrals were unaffected; both were regenerated.
2. **g_πNN tolerance.** The plan gives none; ±0.05 was chosen afterwards. For μ_p/μ_n the moments' ±0.02 was applied.
3. **Magnetic radius.** It is calibrated in ANW's definition (⟨r⁴⟩/⟨r²⟩ over the baryon density) and compared with data in the Sachs definition (factor √(3/5)). Both ratios are given.
4. **g_πNN data value.** 13.1 is a [summary] value (g²/4π ≈ 13.6–13.8; 2M_N g_A/F_π(phys) = 13.0); PDG does not list g_πNN.
5. **Massive variant.** Optional, with no target. The AN84 parameters were verified by refit; AN84's other numbers were not read in the source.
6. **Extras, not preregistered and labelled as such:** N_c-dependence of the charges, the enclosed-charge table, the identity D = −2C and its surface-term reason, and `fig_vs_pdg.png`.
7. **Cross-check.** The independent second computation (`crosscheck/`) belongs to another agent and is not reported here.

## Limitations

- **Leading order only.** Everything is classical soliton plus rigid-rotor quantization, leading order in 1/N_c. Known corrections at subleading order (rotational and meson-loop corrections, notably to g_A) are not included. The moments use SU(2) collective quantization; SU(3) magnetic moments (octet Clebsches, symmetry breaking) were not computed.
- **Massless pions in the calibrated model.** The proton and neutron charge radii are infinite there, so the only charge-radius comparison with data is the uncalibrated massive variant.
- **One-cone and vacuum checks** are tree level and hold by construction. Quantum corrections were not computed; with a Lorentz-invariant regulator they would not change this.
- **π⁰ width at leading order only.** Bernstein–Holstein quote higher-order chiral predictions of 8.10 eV (+4.5%), which lie 2.5σ above PrimEx-II. The leading-order agreement is therefore partly fortuitous, and the pass is a statement about the anomaly normalization, not a precision test.
- **Data values.** The isoscalar magnetic radius derived from PDG has a ±0.09 fm uncertainty, dominated by r_M^p. g_πNN is a [summary] value.
- **Targets.** ANW targets come through secondary sources (Rakhimov's Table 1.1 reproduces ANW: 0.59 fm, 0.92 fm, 1.87, −1.31, 0.61, 8.9).

## How to reproduce

```
cd seed/experiments/E5_add_light
./run_all.sh            # sets NUMBA/OMP/OPENBLAS/MKL threads to 1; total 2 min 59 s wall on one shared core
```

Individual steps, in order, each prefixed with `NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`:

| Command | Runtime | Output |
|---|---|---|
| `python3 symbolic_derivations.py` | 150–170 s | `symbolic_log.txt`, `symbolic_results.json`; 38 checks, prints PASS/FAIL |
| `python3 hedgehog_em.py` | 7 s | `hedgehog_results.json`, `hedgehog_log.txt`, `fig_charge_densities.png`; convergence table, shooting check, derived-density cross-checks |
| `python3 rotor_charges.py` | < 1 s | `charges_results.json` |
| `python3 pi0_gamma_gamma.py` | ~1 s | `pi0_results.json` |
| `python3 make_results.py` | ~2 s | `results.json`, `fig_vs_pdg.png`; prints the calibration verdicts and the PDG comparison |

Python 3.13, numpy 2.5.3, scipy 1.18.1, sympy 1.14, matplotlib 3.11 and the `pdg` package (PDG 2026); hard-coded PDG fallbacks exist. All scripts are deterministic.
