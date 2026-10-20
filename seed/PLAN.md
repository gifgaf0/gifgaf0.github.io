# Seed experiments: preregistration

*Written October 18, 2026, before any experiment below was run. The git commit that adds this file is the timestamp. Experiments, calibration targets and pass rules are fixed here; anything changed afterwards is reported as a deviation in that experiment's report.*

## 1. What this series can and cannot show

No set of simulations can prove a theory of everything, and this series doesn't try to. SEED.md is a set of commitments plus three starter models drawn from known physics. What experiments can do is:

1. **Calibrate.** Reproduce the published answers of the known models (φ⁴ kinks, Skyrme baryons, Faddeev–Hopf knots, gravitating skyrmions). Until the tools pass these checks, nothing built on them means anything.
2. **Test the seed's own claims.** SEED.md makes definite statements in §2–§5 and §7: the group facts of §3, folds being fermions or bosons depending on the internal space, the octet and decuplet, a ragged pair threshold, Q = 7 being a trefoil. Each can come out true or false.
3. **Measure the gaps.** §8 lists where a theory of everything has to reach. Some of those can be turned into numbers: how far a fold is from being as small and light as an electron, how many quanta a weakly coupled pair needs, and the size of the vacuum-energy mismatch.

Verdict words used in the reports:
- **CALIBRATED**: reproduces the literature target within the stated tolerance.
- **CONFIRMED**: a seed claim holds in the experiment.
- **AMENDED**: a seed claim holds only with a correction (stated).
- **REFUTED**: a seed claim fails.
- **QUANTIFIED**: a §8 gap measured, with no pass/fail.
- **OPEN**: not settled by this run (reason stated).

## 2. Method rules

- **Targets before compute.** Every number in §4 below was written down before the experiment that tests it was run.
- **Twice, independently.** Every headline number is computed by two agents with separate code. The second agent reads this plan and the first agent's report, but not its code, until both computations are done. Disagreements are diagnosed and reported, never averaged away.
- **No tuning to targets.** Parameters fitted to data are named as inputs. A miss is reported as a miss.
- **Provenance of targets.** The literature check (`prior_address/research_raw.json`) could not open publisher sites; the sandbox's proxy blocks them. Targets marked **[read]** were read in the source text, from the public arXiv mirror on Google Cloud Storage or the PDG 2026 database (the `pdg` Python package). Targets marked **[summary]** come from search-engine extracts or from several agreeing secondary sources. Their tolerances are looser.
- **Reproducible.** Python 3.13 with numpy 2.5.3, scipy 1.18.1, sympy 1.14, numba 0.68 and matplotlib 3.11 (`requirements.txt`). Scripts are standalone, deterministic (fixed seeds) and print their own checks.
- **Layout.** Each experiment lives in `experiments/E<n>_<name>/`: scripts, `results.json`, `REPORT.md`, figures, and a `crosscheck/` folder holding the independent second computation (`CROSSCHECK.md`, `crosscheck.json`). `RESULTS.md` collects the verdicts.

## 3. What the literature check found in SEED.md

Four agents checked the 27 references in §9 and 36 factual claims in §2–§8 against the literature (search extracts; some full texts from the arXiv mirror). **No reference is fabricated or wrong, and every volume and page matches.** Corrections to carry into the next revision of the seed:

1. **§4, §9: the 3/4 power.** The optimality of E ∝ Q^{3/4} was proved by Lin & Yang (2004, *Commun. Math. Phys.* 249, 273), who gave the matching upper bound. Sutcliffe 2007 is numerical; its energies agree with Ward's conjectured bound E ≥ Q^{3/4}. **[read: Sutcliffe 2007 §2 cites the optimality to its ref. 10]**
2. **§5: Weinberg 1964** proves universal coupling (gravitational mass = inertial mass) from the S-matrix. The derivation of Einstein's equations is Weinberg 1965, *Phys. Rev.* 138, B988, and Deser 1970.
3. **§8: the electron size bound** is conservative. LEP gives r_e < 1.1 × 10⁻⁴ fm (Schael et al., *Phys. Rept.* 532, 119 (2013)), so the electron misses the classical-fold condition by at least 3.5 × 10⁶, not 10⁵.
4. **§2: knot folds and spin.** π₄(S²) = ℤ₂ holds, but the rotation loop is non-contractible only for odd Hopf charge (Krusch & Speight, *Commun. Math. Phys.* 264, 391 (2006)). Hopf solitons can be fermions when Q is odd, not every knot fold.
5. **§2: the G₂ argument** needs H⁵(G₂; ℝ) = 0 for the absence of a Wess–Zumino term, as well as π₄ = π₅ = 0. Both hold (rational cohomology in degrees 3 and 11), and Auckly & Speight's classification agrees.
6. **§9: dates and details.** Albayrak & Vachaspati, *Phys. Rev. D* 109, 036001 appeared in 2024 (preprint 2023). DESI DR2 II is now *Phys. Rev. D* 112, 083515 (2025); a DES-Dovekie recalibration lowers its 4.2σ figure to about 3.2σ. Vakulenko & Kapitanskii's original is *Dokl. Akad. Nauk SSSR* 246, 840.
7. **§2: STAR 2021** is real (6085 exclusive pairs in ultra-peripheral Au+Au), but the photons are quasi-real, and whether that counts as Breit–Wheeler is debated. It was not the first observation of γγ → e⁺e⁻ in heavy-ion collisions.
8. **§8: Weinberg–Witten** forbids charged massless states with |h| > 1/2 (given a Lorentz-covariant conserved current) and any massless |h| > 1 state (given a Lorentz-covariant conserved T_μν). It forbids a composite graviton in such theories, not a neutral composite photon.

Not confirmed (full text unreachable): the exact axes and the "gaps even at high energy" wording attributed to Albayrak & Vachaspati 2026. Its abstract says production is fractured, "with holes and isolated regions".

## 4. The experiments

Nine experiments. E1, E6 and E8 are numerical PDE or ODE work; the rest are algebra, ODEs and quadrature.

### E0. The hexagon facts, recomputed exactly (§3)

**Question.** Do the §3 claims survive an independent computation in exact arithmetic?
**Method.** Redo every check of `hexagon_check.py` without floating point (sympy over ℚ(ζ₇), or exact permutation and integer-lattice arithmetic): the torus labeling, K₇, the 14 triangles and two Fano families, the octonion lines, ⟨D, 120° turn⟩ of order 21 in SU(3), both copies of PSL(2,7) of order 168 in SU(3), the quartics, maximality of the order-21 group, the uniqueness of the two cyclic Fano planes, and the Weyl-group action of SU(3) and G₂. Add:
- the character values that make PSL(2,7)'s and F₂₁'s triplets complex (b₇ = (−1 + i√7)/2) and A₅'s triplets real ((1 ± √5)/2);
- that G₂'s affine Weyl group is the wallpaper group p6m (point group of order 12 with 60° turns, translations forming the hexagonal lattice).

**Pass.** Every claim reproduces exactly. Any failure is a §3 correction.

### E1. A fold in one dimension (Model A; §4, §7.1, §8 coupling)

Conventions: V = ¼(φ² − 1)², so m = √2 and M_kink = 2√2/3 (the Dutta–Steer–Vachaspati convention). Velocities do not depend on the convention.

- **E1a, static kink.** Targets: M_kink = 2√2/3 and shape-mode frequency ω_s = (√3/2)m = √(3/2), both exact (relative 10⁻⁴).
- **E1b, kink–antikink collisions.**
  - Target: critical velocity v_c = 0.2598 **[summary, several sources agree]**, tolerance ±0.001.
  - Two-bounce resonance windows below v_c, the first near [0.1926, 0.2034] **[summary, one source]**, tolerance ±0.003. At least three windows, narrowing toward v_c.
  - Run a convergence check in dx and initial separation.
- **E1c, Dutta–Steer–Vachaspati breather trains** **[read: arXiv:0803.0670]**.
  - Setup, exactly as published:
    - sine-Gordon breathers f = −1 + Σ (4/π) arctan[η sin(ωT_n)/cosh(ηωX_n)], with η = √(1 − ω²)/ω;
    - N_b = int[2/√(1 − ω²)] + 1 breathers per train;
    - half-separation a = 10/√(1 − ω²), spacing d = 2/√(1 − ω²);
    - evolve for one light-crossing time with absorbing boundaries.
  - Targets, qualitative:
    - (ω = 0.99, v = 0.43) produces a kink–antikink pair;
    - over ω ∈ [0.90, 0.99] and v ∈ [0.4, 0.9], the producing region trends to lower v as ω rises;
    - trains pass through at high v;
    - there are holes, e.g. near (0.91, 0.82);
    - no production found for ω > 0.99.
- **E1d, colliding Gaussian packets (new; the seed's Model A as written).**
  - Initial condition: φ = −1 + Σ_± A exp(−(x ∓ x₀)²/2σ²) cos(k(x ∓ x₀)), with φ_t from the linear dispersion ω_k = √(k² + m²) so the packets move toward each other.
  - Scan amplitude A, width σ and carrier k (group velocity k/ω_k). Record production (a persistent pair of zeros with φ ≈ +1 between them at the end of the run) against total energy in units of 2M_kink.
  - Predictions:
    - no production below E = 2M_kink (energy conservation; a sanity check);
    - above it, the boundary is ragged rather than one threshold (§4, §7.1);
    - production favors low speed and wide packets, by analogy with DSV 2008 and Albayrak–Vachaspati 2024.
  - Report the fraction of producing runs against E/2M and the number of disconnected producing regions.
- **E1e, number of quanta (§8).** Classical φ⁴ dynamics doesn't depend on the overall field scale φ₀ (λ scales out), so the number of quanta in a producing initial state is N = E/m ∝ φ₀² ∝ 1/λ. From E1c and E1d, compute N_min·λ, the smallest producing quanta count in units of 1/λ.
  - Prediction: pair production needs N ~ 1/λ quanta, so making a pair from a few quanta is exponentially rare at weak coupling. This is the §8 claim, and agrees with Demidov & Levkov 2011 **[summary]**.

### E2. The fold in SU(2) and SU(3) (Model B; §2, §6B)

Conventions: L = (F_π²/16) Tr ∂U∂U† + (1/32e²) Tr[L_μ, L_ν]², with F_π = 186 MeV experimentally (the 93 MeV convention is f_π = F_π/2), and dimensionless radius x = eF_π r.

- **Hedgehog.** Targets **[read: Schechter–Weigel hep-ph/9907554, Praszalowicz hep-ph/0308114; ANW numbers via secondary sources]**:
  - M_cl = 36.5 F_π/e, i.e. 1.2315 × 3π² F_π/e (tolerance 0.2%);
  - I₁ = (2π/3)Λ/(e³F_π) with Λ = 50.9 (tolerance 0.5%);
  - the ANW fit to M_N = 939 and M_Δ = 1232 MeV gives F_π = 129 MeV and e = 5.45 (1%);
  - g_A = 0.61 (±0.01).
- **Strange moment of inertia.** I₂ = (π/2)(1/(e³F_π)) ∫x²(1 − cos F)(1 + F′² + 2 sin²F/x²) dx **[read: Kopeliovich hep-th/9707067]**. The arctan ansatz gives I₂ ≈ 40.5/(e³F_π) **[read: Praszalowicz]**; the exact profile should land within 1.5% of it.
- **SU(3) rotor.**
  - E = M + C₂(p,q)/(2I₂) + (1/2I₁ − 1/2I₂)J(J+1) − N_c²/(24 I₂), with the Wess–Zumino constraint Y_R = N_c B/3 **[read: Diakonov–Petrov–Polyakov hep-ph/9703373]**.
  - Targets, exact: the allowed lowest irreps are 8 (J = ½), 10 (J = 3/2), 10̄ (J = ½), then 27; E(10) − E(8) = 3/(2I₁); E(10̄) − E(8) = 3/(2I₂).
  - With exact SU(3), every member of a multiplet has one mass (§6B).
- **Predictions written now** (from the targets above; numbers are expectations, not literature):
  - At ANW's parameters the SU(3) octet sits about 385 MeV above the SU(2) nucleon. The SU(3) rotor adds 3/(4I₂) ≈ 385 MeV.
  - A refit of (F_π, e) to the octet and decuplet centers (1151 and 1382 MeV, from PDG 2026 masses) gives roughly F_π ≈ 114 MeV and e ≈ 5.25, and puts the antidecuplet near 1760 MeV.
- **Fermion iff N_c odd** (§2, Witten 1983). For N_c = 1…7 with B = 1, list the allowed irreps and their spins. Prediction: J is half-integer exactly when N_c is odd.
- **Derrick and virial.**
  - The stretching and stiffness energies are equal at the minimum (E₂ = E₄ to 10⁻⁴).
  - Without the Skyrme term, shrinking the fold always lowers its energy (§4, Derrick 1964).
  - Von Laue: the fold's pressure integrates to zero.

### E3. Swap the internal space (§7.2)

- **G₂ (new; no published G₂ skyrmion found).**
  - Embeddings and decompositions:
    - from explicit 7 × 7 generators, compute the Dynkin indices of the SU(2) subgroups. Expected: long-root SU(2) index 1, short-root 3, plus 4 and 28 **[read: Mayanskiy arXiv:1611.04070]**. So the B = 1 fold is the long-root hedgehog, which is the SU(3) hedgehog sitting inside G₂;
    - branching under SU(2)_long × SU(2)_short: 14 = (3,1) + (1,3) + (2,4) **[read]** and 7 = (2,2) + (1,3) (expected).
  - Inertia: with the E2 profile, compute the inertia tensor on all 14 directions of g₂. Expected: I₁ (×3), I₂ (×8, equal to the SU(3) value), and 0 (×3, the short SU(2)).
  - Rotor spectrum:
    - allowed states are G₂ irreps R whose right-acting part is a singlet of SU(2)_short (there is no Wess–Zumino term to change that), and the spin J comes from the SU(2)_long content;
    - expected energies: E = M + J(J+1)/(2I₁) + [C₂(R) − J(J+1)]/(2I₂), with C₂(7) = 2 and C₂(14) = 4 in long-root normalization.
    - Seed prediction (§2): every allowed J is an integer, so G₂ folds are bosons. Expected lowest states: 1 (J = 0), then 14 (J = 1). The 7 is not allowed.
  - Report the first several multiplets with their energies at the E2 parameters. Stability of the embedded hedgehog in G₂ is checked if feasible; otherwise reported as OPEN.
- **The flag space SU(3)/T².**
  - Moment map: sample the orbit U diag(a)U† and project to the diagonal. Expected: the convex hull of the six permutations of a, a hexagon with 120° angles and alternating sides (Schur–Horn). It becomes a triangle when two eigenvalues coincide (CP²).
  - Charges: build explicit maps S² → SU(3)/T² and compute their two π₂ charges numerically; expected integers, independent, spanning ℤ².
  - Hopf-type charge: compute π₃ = ℤ for one explicit configuration through its SU(3) lift **[read: Affleck, Bykov & Wamer arXiv:2101.11638]**.

### E4. The order-21 group on three generations (§3, §7.3)

- **Groups and products.** Build F₂₁ = ⟨D, C⟩ and the seed's PSL(2,7) = ⟨D, C, R_flip⟩. Compute character tables and Kronecker products, and check them against Luhn–Nasri–Ramond **[read: arXiv:0709.1447, 0706.2341]**: F₂₁ 3 ⊗ 3 = 3 + 3̄ + 3̄, 3 ⊗ 3̄ = 1 + 1′ + 1″ + 3 + 3̄; PSL(2,7) 3 ⊗ 3 = 3̄ + 6, 3 ⊗ 3̄ = 1 + 8.
- **Allowed couplings.** For each assignment of left-handed fermions, right-handed fermions and Higgs or flavon fields to irreps, find the invariant Yukawa tensors and the general mass matrix, before and after vacuum alignments that leave subgroups unbroken (ℤ₃ by (1,1,1), ℤ₇ by D-eigenvectors).
- **Seed-relevant predictions.**
  - With F₂₁ unbroken, three generations in one irreducible triplet cannot have three different masses (Schur's lemma). The group has to be broken to make a hierarchy.
  - Mixing comes from misalignment between the subgroups left unbroken in different sectors.
  - Reproduce the LNR seesaw example (α = β = −1): θ₁₃ ≈ 2.8° and Δm²₃₁/Δm²₂₁ = 80/3 **[read]**, which data exclude (NuFIT 6.0: sin²θ₁₃ ≈ 0.022, ratio 33.8 ± 0.9).
- **Comparison data.** For each texture class, report whether it can fit NuFIT 6.0 and CKM data (UTfit 2022), and count free parameters against observables.
- **Pass.** Kronecker products and LNR outputs reproduce exactly. The fit status of each texture class is reported either way.

### E5. Add light (§7.4; commitment 4)

- **Charges.** Q = I₃ + Y/2 on the E2 rotor states, octet through 27. Check integrality and the SU(2) form Q = I₃ + B/2.
- **Electromagnetic static properties.** Targets **[ANW via secondary sources; formulas read in Ma–Harada and Rakhimov]**:
  - isoscalar charge radius 0.59 fm and isoscalar magnetic radius 0.92 fm;
  - μ_p = 1.87 and μ_n = −1.31 nuclear magnetons, so μ_p/μ_n = −1.43 (data: −1.4599);
  - g_πNN = 8.9.
  - Tolerance ±0.02 on the moments and ±0.01 fm on the radii. Test the seed's "within roughly 30%" against PDG 2026.
- **Charge is dressed.** Compute the proton and neutron charge densities. Prediction: with massless pions the isovector radius diverges, because the dressing cloud has no edge. Report what a pion mass changes, with no target.
- **π⁰ → γγ from the gauged Wess–Zumino term.**
  - Derive the amplitude. Γ = α²m³N_c²/(576π³f_π²) = 7.76 eV at f_π = 92.21 MeV **[read: Bernstein–Holstein arXiv:1112.4809]**.
  - Data: PrimEx-II 7.802 ± 0.117 eV; PDG 2026 7.72 ± 0.12 eV **[read]**. Pass: the leading-order value lies within 2σ of PrimEx-II, and N_c = 1 (0.86 eV) is excluded.
  - Internal-consistency prediction: at the Skyrme fold's own fitted f_π (64.5 MeV from ANW, about 57 MeV from the SU(3) refit) the width comes out 2 to 2.6 times too large (about 15.9 and 20 eV). The fold sector and the anomaly prefer different f_π.
- **One cone, taut vacuum.**
  - Linearize the gauged Skyrme and Maxwell fields around the vacuum and confirm a single light cone (photon ω = k; pion ω² = k² + m²).
  - Confirm T_μν = −V₀ g_μν for the vacuum, so p = −ρ in every frame (commitment 1).
  - Both are expected by construction; reported as checks.

### E6. A fold with gravity (§5, §7.5)

- **Setup.** Hedgehog Einstein–Skyrme equations with ds² = −σ²N dt² + dr²/N + r²dΩ² and coupling α = 4πG f², f = F_π(ANW)/2 **[convention per Bizon–Chmaj 1992; Kleihaus–Kunz–Sood]**.
- **Calibration.**
  - Solutions cease at α_crit = 0.040378 **[summary: Zajac 2009; also reproduced in a scratch check during the literature pass]**. Tolerance ±0.0002 for CALIBRATED; matching all digits is reported.
  - Two branches merge there, the lower one connecting to the flat skyrmion.
- **Equivalence-principle check.** Prediction: as α → 0, the ADM mass equals the flat-space energy plus the Newtonian binding energy −½∫ρΦ, to better than 1% in the O(α) coefficient. The fold's gravitational mass is its total energy, gradient and stiffness energy included (commitment 5).
- **Physical scale.** At the physical coupling α ≈ 3.5 × 10⁻⁴⁰ (f = 64.5 MeV), the metric deviation at the fold's core is of order 10⁻³⁹. Report numbers.

### E7. Scale and coupling audit (§8)

- **Size against Compton wavelength.**
  - In the Skyrme family, M ∝ F_π/e and R ∝ 1/(eF_π), so M·R/ħc = c₀/e². Compute c₀ from the E2 profile.
  - Proton at ANW parameters: M·R/ħc ≈ 2.8 (classical fold, as §8 says).
  - Find the e needed for an electron-mass fold no larger than the LEP bound, and the size of rotational and loop corrections there.
  - Prediction: the semiclassical fold fails by a factor ≥ 3.5 × 10⁶. The same holds for any soliton whose classical action scales as 1/g², so an electron-like fold needs g² ≫ 1, confirming §8's "strongly coupled fold sector" quantitatively.
- **Pairs.** Combine E1e's N_min ∝ 1/λ with the exponential suppression to state at what coupling few-quanta pair production stops being rare.
- **Vacuum tension.**
  - Observed ρ_Λ ≈ 2.5 × 10⁻⁴⁷ GeV⁴, i.e. (2.24 meV)⁴ (Planck 2018 H₀ and Ω_Λ).
  - Ratios to natural scales: f_π⁴ about 3 × 10⁴², electroweak about 10⁵⁶, Planck about 10¹²³. The seed lists this as open; reported as QUANTIFIED.
- **Can the cone be built from the field?** State what Weinberg–Witten allows for composite photons and gravitons under commitments 1 and 5.

### E8. Knots (Model C; §4, §6C)

- **Setup.** Energy E = (1/(32√2 π²)) ∫ [∂ᵢφ·∂ᵢφ + ½ (∂ᵢφ × ∂ⱼφ)·(∂ᵢφ × ∂ⱼφ)] d³x, so Ward's conjectured bound is E ≥ Q^{3/4}. The proven bound is c = (3/16)^{3/8} ≈ 0.534.
- **Targets** **[read: Sutcliffe 2007, Table 2; Δx = 0.1 on 151³ with fixed boundary; absolute energies about 1% low, relative ones about 0.1%]**:

  | Q | type | E | E/Q^{3/4} |
  |---|---|---|---|
  | 1 | A₁,₁ | 1.204 | 1.204 |
  | 2 | A₂,₁ | 1.967 | 1.170 |
  | 3 | Ã₃,₁ | 2.754 | 1.208 |
  | 4 | A₂,₂ | 3.445 | 1.218 |
  | 5 | L¹'¹₁,₂ | 4.095 | 1.225 |
  | 6 | L¹'¹₂,₂ | 4.650 | 1.213 |
  | 7 | K₃,₂ (trefoil) | 5.242 | 1.218 |

  More accurate Q = 1 values in the literature are 1.21–1.22.
- **Plan.** Q = 1–4 are required. Q = 5–7 are attempted within the compute budget (4 shared cores), with the trefoil started from the rational map W = Z₁²Z₀/(Z₁³ + Z₀²). Measure the Hopf charge from the Whitehead integral, and the knot type from the position curve φ = −e₃.
- **Pass.**
  - E_Q within 2% of the table for Q = 1–4, and ratios E_Q/E₁ within 1%;
  - the configuration types match;
  - the measured Q is within 0.05 of an integer.
- **Seed claims tested:**
  - E/Q^{3/4} stays near 1.2, so energy per unit charge falls and bigger folds store charge more cheaply (§4);
  - E₂ < 2E₁, so a charge-2 fold doesn't split;
  - Q = 7 is a trefoil, if reached.

## 5. Which seed claims each experiment tests

| SEED.md | Claim | Experiment |
|---|---|---|
| §2 | spin ½ from SU(3) iff N_c odd; G₂ folds only bosons | E2, E3 |
| §2 | one speed, no vacuum dispersion, taut vacuum frame-free | E5 (by construction), E7 |
| §2, §5 | equivalence principle from one metric | E6 |
| §3 | torus, Fano, F₂₁, PSL(2,7), G₂/p6m facts | E0 |
| §4, §7.1 | packets fold into pairs; ragged boundary | E1 |
| §4 | Derrick: something must push back | E2 |
| §4, §6C | E ∝ Q^{3/4}; Q = 7 trefoil | E8 |
| §6B | octet and decuplet from the fold; within about 30% for nucleons | E2, E5 |
| §7.2 | G₂ and flag-space folds | E3 |
| §7.3 | order-21 group on three generations | E4 |
| §7.4 | charges from a gauged U(1); one cone | E5 |
| §7.5 | self-gravitating skyrmion | E6 |
| §8 | size, coupling, vacuum tension, emergent cone | E7, E1e |
