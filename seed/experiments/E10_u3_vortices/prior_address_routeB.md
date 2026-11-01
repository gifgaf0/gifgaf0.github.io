# E10 / Route B, step B1: prior address

*November 1, 2026. Label: Exploration. Literature only; nothing computed numerically. Follows `NOTE_route_B.md` §5 (B1). Items are marked **[checked]** when confirmed against the source text or abstract on November 1, 2026, and **[derived]** when they follow from checked items by short algebra shown here. Anything still unverified is marked **[open]**.*

## 1. The model adopted for Route B (fixes NOTE §1's open normalizations)

Use the U(N) extension of the Abelian-Higgs model with a single gauge coupling (Auzzi, Eto and Vinci's "fine-tuned model"):

  L = Tr[ −(1/2g²) F_μν F^μν + D_μH (D^μH)† − (λ²g²/4)(v² 1_N − HH†)² ],  N = 3.

[checked: Auzzi, Eto and Vinci, "Static Interactions of non-Abelian Vortices", arXiv:0711.0116, eq. (2.1); the same form is in Eto, arXiv:0810.4895, eq. (1).]

- **One dimensionless parameter.** After H → vH, W → gvW, x → x/(gv) [checked, 0810.4895 eq. (5)], the vector masses are M_U(1) = M_SU(N) = 1 and the scalar masses are M_s = M_ad = λ, in units of gv [checked, eq. (6)]. So λ is the only free parameter. This is better for the Eddington guard than NOTE §1's four couplings.
- **BPS point: λ = 1.** There is no force between parallel static vortices at any distance [checked: 0711.0116 abstract].
- **Off BPS.** For λ < 1 (type I), vortices with the same orientation attract. For λ > 1 (type II) they repel. Vortices with opposite (orthogonal) CP^{N−1} orientations feel no force [checked: 0711.0116 text].

**Conventions.** With F = F^aT^a and Tr(T^aT^b) = ½δ^{ab}, Tr(F²)/(2g²) = F^aF^a/(4g²). That is the same normalization as Shifman–Yung's SU(N) sector [derived]. For comparison, Shifman–Yung's two-coupling SQCD has m_W = g₂√ξ and m_{U(1)} = g₁√(N/2)·√ξ [checked: Ievlev thesis, arXiv:2011.14121, eqs. (2.2.22)–(2.2.23)].

## 2. The elementary string

**Flux 1/3 [derived].** The elementary vortex winds one diagonal entry: H = diag(h(r)e^{iθ}, v, v), with its gauge field along diag(1, 0, 0). Since diag(1, 0, 0) = (1/3)·1 + diag(2/3, −1/3, −1/3), the string carries exactly 1/3 of the overall U(1) flux quantum, plus SU(3) flux along a Cartan generator. Consistent with this, the abelian (ANO) string is N times the elementary string's tension [checked: arXiv:0805.4378, "There are N species of such strings; they have degenerate tensions T = 2πξ. (The ANO string tension is N times larger.)"].

**Tension.**
- At BPS: T = 2πξ in SQCD normalization [checked: arXiv:0712.3512 eq. (11); Ievlev eq. (1.1.5)]. In the model of §1 this is T = 2πv² up to convention [open: confirm the factor in B2 numerically].
- Off BPS, elementary (k = 1) and coincident k = 2 masses, normalized so that λ = 1 gives 1 [checked: 0810.4895 Table 1]:

| λ | 0.8 | 0.9 | 1.0 | 1.1 | 1.2 |
|---|---|---|---|---|---|
| k = 1 | 0.91231 | 0.95737 | 1.00000 | 1.04053 | 1.07922 |
| k = 2 (parallel) | 1.77407 | 1.88936 | 2.00000 | 2.10655 | 2.20944 |

  In the single-coupling model the mass of a (k₁, k₂) vortex is the sum of the (k₁, 0) and (0, k₂) masses [checked: 0810.4895 text]. **These numbers are B2's calibration target.**

**Moduli and worldsheet theory.**
- The orientation lives in CP² = SU(3)_{C+F}/[SU(2) × U(1)] [checked: 0712.3512 eq. (12)].
- The worldsheet action is S = 2β∫dt dz [∂n̄·∂n + (n̄·∂n)²], with n ∈ C³ and |n| = 1 [checked: Ievlev eq. (2.4.3)].
- β = (2π/g₂²)·I [checked: Ievlev eq. (2.4.4)], with β = 2π/g₂² at the BPS point [checked: 0712.3512, "β = 2π/g²₂ at the scale √ξ"]. So I = 1 at BPS.
- The 2D CP² model is asymptotically free and gaps the moduli quantum mechanically, at a scale Λ ≪ √ξ [checked: 0712.3512 eq. (14) context]. Classical treatment only, as NOTE §3 says.

## 3. B-i, the intrinsic vorton: the crude estimate with the correct normalizations

**Moduli inertia.** Rotate the orientation in time inside a U(1) ⊂ SU(3)_{C+F}: n = (cos α, e^{iωt} sin α, 0). The worldsheet energy per unit length is 2β ω² sin²α cos²α [derived from the action above]. Its maximum, at α = π/4, gives a moduli inertia I_m = β/2 = π/g² (energy = I_m ω²).

**Thin-ring balance (NOTE §3).** With the profile frozen, as in option 4's §1.3: k² + ω² = T/I_m = 2πv² / (π/g²) = **2g²v² = 2 M_V²** [derived]. Here M_V = gv is the common vector mass, and the inertia is at its maximum, so this is the most favourable case.

**Leak threshold.** Charge stays on the string only if ω < m_bulk. The lightest bulk modes carrying SU(3)_{C+F} charge are the adjoint vectors (M_V) and adjoint scalars (λM_V). So m_bulk = min(1, λ)·M_V ≤ M_V.

**Consequences, at the crude level:**
- **Charge only (k = 0)** needs ω ≥ √2 M_V > m_bulk. **The charge leaks at every λ.** Charge-only thin vortons are excluded.
- **With current** we need k² > 2M_V² − m_bulk² ≥ M_V². That is a winding wavelength shorter than the core size 1/M_V, which is outside the moduli approximation, which needs k, ω ≪ M_V. The winding is also unprotected (π₁(CP²) = 0).

**Can the core deformation rescue it, as it did in option 4?**
- Option 4 was rescued by a **metastable σ phase**: the charge filled a widening tube of a locally stable phase, which made I grow by 10 to 100 times.
- Route B's analogue would be a widening region in which one diagonal entry of H vanishes. In the model of §1 that region is never a local minimum of the potential: it costs (λ²g²/4)v⁴ per unit volume above the vacuum [derived from the potential]. So the inertia cannot grow cheaply.
- **My expectation, not a result:** no rescue. B3 is still cheap enough to check this directly.

**Prior art.**
- Vortons with non-abelian moduli: the toy U(1) × SO(3) model only. Above a critical ω they decay into a spinning Q-ring [checked: Tallarita, Peterson, Bolognesi and Bedford, EPJC 80, 38 (2020)]. The colour-flavour-locked U(N) case is not treated.
- Two searches on November 1, 2026 found no U(N) colour-flavour-locked vorton construction after 2020. That is not proof none exists.
- For the gauged U(1) × U(1) model, stable vortons were found by gradient flow, stable against non-axial perturbations, in quantitative agreement with the thin-string approximation [checked: Battye et al., PRL 127, 241601 (2021), abstract]. **This supports trusting thin-string estimates when no metastable phase intervenes, so it weighs against B-i here.**

## 4. B-ii, braided and linked strings: protection

- **Reconnection.** At critical (BPS) coupling, local and semilocal strings in abelian and non-abelian gauge theories always reconnect classically when they collide [checked: Eto, Hashimoto, Marmorini, Nitta, Ohashi and Vinci, PRL 98, 091602 (2007), hep-th/0609214, abstract]. At low energies, mismatched orientations can reduce the reconnection probability [checked at abstract level: Hashimoto and Tong, JCAP 0509, 004 (2005), hep-th/0506022]. **So linking is not topologically protected. Only dynamics can keep linked loops from passing through each other.**
- **Forces.** These are as in §1: none at BPS, orientation-dependent off BPS. Off BPS, a bound state of two vortices at non-zero separation exists for some couplings [checked: 0711.0116 abstract]. The abstract does not say whether that happens in the single-λ model of §1 [open].
- **Global strings with orientational moduli** were simulated in head-on collisions, with an inter-vortex force phase diagram [checked: JHEP 03 (2021) 156, abstract]. Relevant to B-ii dynamics, not read in detail.

## 5. What B1 changes in the plan

1. **Model.** The model of §1, with λ as the only parameter. λ = 1 (BPS) is primary. λ ∈ {0.8, 1.2} are secondary, chosen now because they bracket type I and type II and have published calibration numbers.
2. **B2 (straight-string calibration) gets a sharp instrument check:** reproduce the k = 1 and k = 2 masses of the table above at λ = 0.8, 1.0 and 1.2. Also check:
   - the 1/3 flux (§2),
   - the moduli inertia β·I with I = 1 at BPS,
   - T = 2πv² (to fix §2's open convention factor).
3. **B3's prediction is written now, before any run:** no thin-ring equilibrium for charge only at any λ (from §3), and none with current inside the moduli-valid region k, ω < 0.5 M_V. B3 can still overturn the frozen-profile estimate, as Phase 0 did for option 4. My prior that B3 finds a window is about 10 %.
4. **B-ii is lower priority still.** Linking is unprotected (§4), and whether the single-λ model has a static bound state is open.

**Bottom line for the author.** Route B gives exact, free thirds with internal orientations, and its own built-in "σ". But on the crude estimate, the orientation charge cannot hold a ring open without leaking into the bulk, and Route B has no metastable phase to rescue it the way option 4 had. B2 and B3 are cheap (1D, minutes) and decide this properly.

## Sources checked

- Hanany and Tong, "Vortices, Instantons and Branes", hep-th/0306150.
- Auzzi, Eto and Vinci, "Static Interactions of non-Abelian Vortices", arXiv:0711.0116.
- Eto, "Static Interactions of U(N) non-Abelian Vortices", arXiv:0810.4895.
- Shifman and Yung, review, hep-th/0703267, and the related papers arXiv:0712.3512 and arXiv:0805.4378.
- Ievlev, PhD thesis (2020), arXiv:2011.14121.
- Tong, "Quantum Vortex Strings: A Review", arXiv:0809.5060.
- Eto et al., "Group Theory of Non-Abelian Vortices", JHEP 11 (2010) 042.
- Tallarita, Peterson, Bolognesi and Bedford, "Vortons with Abelian and non-Abelian currents and their stability", Eur. Phys. J. C 80, 38 (2020).
- Battye et al., "Stable Cosmic Vortons in Bosonic Field Theory", Phys. Rev. Lett. 127, 241601 (2021).
- Eto, Hashimoto, Marmorini, Nitta, Ohashi and Vinci, "Universal Reconnection of Non-Abelian Cosmic Strings", Phys. Rev. Lett. 98, 091602 (2007).
- Hashimoto and Tong, "Reconnection of Non-Abelian Cosmic Strings", JCAP 0509, 004 (2005).
- Forgács, Reuillon and Volkov, "Twisted Superconducting Semilocal Strings", hep-th/0602175.
- Garaud and Volkov, arXiv:0712.3589.
- "Dynamics of global and local vortices with orientational moduli", JHEP 03 (2021) 156.
