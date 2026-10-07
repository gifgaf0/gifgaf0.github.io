# SQT Ledger V4.88: Audit Findings

**Date:** October 6, 2026
**Scope:** the whole of `SQT_Master_Ledger_v4_88_CANONICAL.md` (4,630 lines, 1.77 MB), read by eight AI reviewers, one section each. Each reviewer was told to skip five items that had already been found:
- V4.67 scope
- Bjerknes binding
- §2.90 vs. Λ
- the Oct 3 second-sound result
- M.CW

Line numbers refer to that file, counting from 1.

**How to read this:** the section reports are leads, not verdicts. The table below lists the items that were re-checked in the main session, against the ledger text and against outside sources where relevant. Verify everything else before acting on it.

## Checked headline items

| # | Finding | Ledger evidence | Outside check |
|---|---|---|---|
| 1 | The transverse line's gravitational-wave channel has helicity 0/±1 (vector or scalar) strain, not tensor. No polarization test was ever run; GW170817 was used only as a speed check. | L1642: "a propagating plane wave's strain carries helicity 0/±1, never pure ±2"; L3: "NO gapless internal helicity-±2 branch". There are zero hits for any polarization test. | LIGO–Virgo, GW170817 tests of GR (arXiv:1811.00364): pure tensor is favored over pure vector at log₁₀ Bayes factor +20.81 ± 0.08. |
| 2 | The 16-component substrate's internal sector is gapless, but its dispersion and Landau speed were never examined. Under GP dynamics with density-only forces these modes should be quadratic, which makes the critical velocity zero. | L1522: "the two-body internal sector is gapless — a theorem (L_⊥ψ₀ = 0 …)". There are zero hits for type-B or quadratic dispersion. | Standard spinor-condensate physics (an inference, not computed): with SU(N)-symmetric interactions the non-condensed components move as free particles in the condensate's potential. |
| 3 | The proton ropelength test is mis-specified. 58.006 is the length of the presumed-minimal tight Borromean configuration, so the ideal ropelength cannot exceed it. The prediction 60.194 ± 0.3 therefore fails, unless the units differ. | L643: "L_B = 60.194 fm (within Ashton bounds [58.006, 62.0])"; L649 is the ±0.3 check. | Cantarella–Fu–Kusner–Sullivan–Wrinkle (arXiv:math/0402212) calls it a "ropelength-critical configuration (and presumed minimizer)". One reviewer reproduced the ledger's units. |
| 4 | Vortex reconnection is never discussed, yet "Borromean linking = baryon number" depends on the cores never crossing. | Zero hits for "reconnect". | Kleckner, Kauffman & Irvine, Nature Physics 12, 650 (2016): vortex knots in superfluids untie. The proton lifetime is above 10³⁴ yr. |
| 5 | §2.89 claims locally flat equals no response. §2.90 gets 1/r² from static tension, against Eshelby. The equivalence principle (MICROSCOPE) is never confronted, even though electrons have their own ε_e. | L1551 and L135 ("locally flat at the particle's scale"); zero hits for Eshelby or MICROSCOPE; L79 ("its own ε_e"). | Eshelby: point defects do not interact in an isotropic linear elastic medium, and fall off as 1/r³ in an anisotropic one. MICROSCOPE bounds η at about 10⁻¹⁵. |
| 6 | The gauge paper is cited for "PSL(2,7) as Császár automorphism group", but §2.86 found AGL(1,7), of order 42. | L2235 against L3157 ("Aut(14-face set) = AGL(1,7), order 42"). | Two reviewers confirmed order 42 by brute force. The text of paper v6.3 itself has **not** been checked. |
| 7 | The PSL(2,7) Zenodo note lacks the June prior art. As quoted in the ledger, its Open Problem 4.4 counts 104 elements with circle fixed sets and leaves out the 42 order-4 elements. | L32 ("3A/7A/7B→S¹ codim 6, 104 elts"); L125 (V4.45 prior art). | From the character table: χ₈(4A) = 0 and χ₈(2A) = 0 force eigenvalues {1,1,−1,−1,i,i,−i,−i}, so the fixed space has dimension 2 and the fixed set is S¹. The correct total is 56 + 42 + 48 = 146. Check the paper's own wording. |
| 8 | The "Zero Free Parameters" wording in Paper VII §9.1 and the calculators has been queued for correction since V4.46. | L4440, L3850, L3879. | m₀φ²⁷ = 82.13 GeV, against a measured m_W = 80.369 GeV (2.2% high). |
| 9 | The alpha-decay paper has no ledger row. | Zero hits. | — |
| 10 | The η / Flach row is still "Open", but its purpose (the spin sign coming from internal geometry) closed at V4.84. | L4516 ("Open … the Flach-correspondence computation"); V4.84: "π₁(Orbit) = 0 — the 2π loop contractible in the orbit, no spin sign". | If the problem was posed on the two-dimensional orbifold ℙ¹(2,3,7), the chirality-graded Dirac η-invariant there vanishes identically. The three-dimensional version is Σ(2,3,7). |
| 11 | The Singer-orbit SLWE rank collapse does not depend on k (rank ≤ 112 for every module rank), yet the related rows were scoped to k = 32 only. | L3761: "period-7 in its columns … rank ≤ 7×16 = 112, measured rank 76". | Linear algebra: the period-7 column structure holds for any k. The "~20 bits at spec" figure is one reviewer's rough estimate and has not been checked. |
| 12 | The ζ-tax per-vertex amplitude redshift belongs to the tired-light class. Gate 3 has been open since V4.4. | L4324 and L119 (welding lemma "flagged, not adjudicated"); L4539. | DES SN (arXiv:2406.05050): b = 1.003 ± 0.005 (stat) ± 0.010 (sys), "ruling out any non-time-dilating cosmological models". |
| 13 | Polycrystal grains would have to be only 5–20 lattice cells across. | L1640: W^EM_∪ = (0, 3.764e-33] m; L3: a_phys ∈ [1.899, 7.588]×10⁻³⁴ m. | Arithmetic: 3.764e-33 / 7.588e-34 = 4.96 and 3.764e-33 / 1.899e-34 = 19.8. |
| 14 | H₀ quantization in steps of 1/336 does not appear in V4.88, and as stated it cannot fail. | Zero hits for "1/336" or "0.2006". | The step of 0.2 km/s/Mpc is smaller than current H₀ error bars (≥ 0.4). |

Not re-checked, but plausible and worth handing over:
- **The μ_n premise.** The 4 in μ_n = (4μ_d − μ_u)/3 is a Clebsch–Gordan coefficient of the spin-½ nucleon; the spin-3/2 quartet is the Δ, and μ(Δ⁰) = 0.
- **G-VS1's symmetry group.** The invariants may have been counted under G₂×U(1)_global rather than the action's G₂×U(1)_ψ₀×ℤ₃.
- **OP-2.81.1/2.** These close by Moreno's zero-divisor criterion.
- **Fano/sedenion slips.** A batch of R1-labeled errors in those sections; see the section reports below.

---

## Section reports

### Line 3: recent fold summaries (V4.88 back)

1. **The ledger's gravitational-wave carrier has vector polarization, which GW170817 rules out.** Line 3, character 41815: "the instantiated substrate's excitation inventory carries NO gapless internal helicity-±2 branch; CI-S … FALSIFIED-STRUCTURAL". [E/H, medium-high]
   - §2.91.Q defines the gravitational-wave species (S2) as a descriptor of the transverse phonon's strain, sym(k̂⊗e⊥). That strain is helicity ±1 about the propagation direction, i.e. vector modes in standard polarization terms.
   - GW170817 favors pure tensor over pure vector at log₁₀ Bayes factor 20.81.
   - The ledger uses GW170817 only as a speed test (character 176394). That reading assumed tensor modes, and G-CI1's K = ∅ removed them.
   - **Action:** a polarization-content gate.
2. **κ = φ⁻⁴ contradicts the computed substrate, and the fluid lock was never amended.** Character 94884: "κ ≡ K/(ρ_s c²) = φ⁻⁴ … forcing the fluid-branch longitudinal speed c_s = φ⁻²c". [H/G, high]
   - Voigt–Reuss–Hill averaging of the ledger's own elastic constants (which reproduces c_T = 8.419 / 9.308) gives K/ρc_T² = 1.90–2.43, or 13–17× φ⁻⁴.
   - The same averaging gives ν = +0.28 / +0.32, against the recorded −0.543, and c_L/c_T = 1.80–1.94, against the recorded 1.2162.
   - With c defined as c_T, the longitudinal branch is superluminal, and the ledger never remarks on it.
   - KC3 was evaluated at c_s = 0.382c, a branch the substrate doesn't have.
   - **Action:** amend the I-CONST fork, and annotate the §2.64 row that lists κ as "SQT-derived".
3. **Polycrystal grains can be at most about 4–20 lattice cells across.** Character 42132: "W^EM_∪ = (0, 3.7641664288e-33]"; character 30509: "a_phys ∈ [1.899, 7.588]×10⁻³⁴ m". [G/A, medium-high]
   - These two numbers were never compared; their ratio puts the maximum grain size at 3.9–19.8 lattice spacings.
   - V4.40 uses a different lattice anchoring (cell side 2√3 ℓ_P, ξ_phys = 0.358 ℓ_P), which conflicts with ξ = ℓ_P.
   - The Voigt–Reuss–Hill, Hashin–Shtrikman and Born machinery assumes grains much larger than the lattice spacing.
   - V4.71 says "ξ = ℓ_P not licensed" (character 67109), yet V4.81's E-W-1(a) uses it.
   - **Action:** add a validity floor and pick one lattice anchoring.
4. **I6 may be computable rather than imported (order-by-disorder).** Character 221: "the real-unit split is symmetry-allowed at every order … the vacuum manifold of record is the origin of the allowed space". [F, medium]
   - A term that symmetry allows at every order is generically generated by fluctuations.
   - The zero-point Bogoliubov energy of each stratum can be computed with the existing G-ζ1 machinery (compare Turner et al., PRL 98, 190404).
   - **Action:** register this as a G-VS1 successor.
5. **The excitation inventory is single-component, but the substrate is 16-component.** Character 146015: "the two-body internal sector is gapless — a theorem". [H/B, medium]
   - G-CI1 and G-MSCS1 used elastic tensors from the single-component model.
   - The symmetry left unbroken on each stratum implies exact internal Goldstone modes, from 6 (G₂→SU(3)) up to 11 (G₂→SU(2)); at the vacuum of record there is instead an accidental gapless set.
   - These modes are helicity 0, so K = ∅ survives, but they are extra massless species subject to fifth-force and stellar-cooling limits.
   - V4.68's Q3 item (2), "polar-analog linear vs ferromagnetic-analog quadratic" (character 83078), is the only unresolved Q3 item.
   - **Action:** an inventory of internal modes for each stratum.
6. **The §2.52 Open 3 row is stale because it is frozen.** Character 152705: "closing that single I1–I3 import closes all three; none is independently closable above it". [C/G, high]
   - G-C1 found that shared chokepoint is a free knob. G-ζ1 found the pulsation channel gapless, and V4.67 retired the bridge.
   - The frozen row (L4339) still says "most structurally important".
   - **Action:** the author's decision on unfreezing.
7. **The SLWE leak doesn't depend on module rank k.** Character 38635: "rank ≤ 7×16 = 112"; character 41277: "no statement about … k ≤ 7". [A, high]
   - The bound is the same for every k, so every k ≥ 8 leaks by Gaussian elimination.
   - **Action:** rescope the finding to all k ≥ 8.
8. **The PSL(2,7) Zenodo deposit doesn't cite the prior art.** Character 155956: "the single-group note stays the Zenodo deposit (DOI 10.5281/zenodo.20532770), no fourth submission". [D, medium-high]
   - V4.45 found the result is classical (Faradžev–Ivanov 1990; Praeger–Saxl–Yokoyama 1987), but no corrected version followed.
   - **Action:** a new Zenodo version with the citations.
9. **G-κ1 sealed the mass-ratio test instead of bounding it.** Character 135641: "the ~3% ratio agreements become a boundable prediction". [A/B, medium]
   - The coupling was located but never bounded, while the screening came out topology-dependent at −41% to −53%.
   - F-QUANTA-3 needs the same binding energy and has been open since V4.82.
10. **Half-quantum vortex lines might supply the cone-π scaffolding import (I5).** Character 610. [B, low]
    - V4.88 recorded the half-quantum fact but registered no follow-up.

### Lines 4–72: status block and fold records V4.88 back to V4.69

1. **The tensor messenger has no helicity-±2 content, and GW170817's polarization test was never applied.** L53 and L55. [E/H]
   - The words "polarization test", "antenna" and "vector mode" appear nowhere in the file.
   - **Action:** a pre-registered gate covering GW170817, the later catalog polarization results, and pulsar-timing Hellings–Downs. This is probably a kill surface.
   - **Confidence:** high that it was missed; medium-high that the result goes against the framework.
2. **G-VS1 counted invariants under a U(1) the action of record doesn't have.** L47 and L39. [G/H, medium]
   - The 2/6 and 1/2 counts match G₂×U(1)_global. G₂×U(1)_ψ₀ gives 4/10 and 3/6 instead.
   - Under the action's actual symmetry, G₂×U(1)_ψ₀×ℤ₃, a degree-6 term Re(ψ·ψ)³ pins the 7-sector phase. The half-quantum windings on the polar strata then lose protection, and only ψ₀ windings survive.
   - **Action:** rerun the π₁ table under the actual symmetry.
3. **G-BKZ32 annotated only one open-problem row, but it actually kills the k = 32 spec.** L53. [A]
   - §2.58.B, §2.66.1, OP-2.58.2c and OP-2.58.5 still read as live.
   - Only k ≤ 7 (dimension ≤ 112) avoids rank collapse, far below 128-bit LWE sizes.
   - **Action:** annotate those entries and register a redesign-or-retire decision.
4. **The PSL(2,7) paper's Open Problem 4.4 leaves out the 4A class.** L32. [D/F]
   - χ₈(4A) = χ₈(2A) = 0 forces eigenvalues {1,1,−1,−1,±i,±i}.
   - An explicitly built ρ₈ gives fixed-space dimensions 4/2/2/2 for element orders 2/3/4/7, so the codimension-6 classes total 146 elements, not 104.
   - **Action:** check the paper's own text.
   - **Confidence:** high on the math, medium on the paper's wording.
5. **OP-2.81.1 and OP-2.81.2 follow from a classical criterion.** L4. [F, high]
   - A sedenion (a,b) is a zero divisor exactly when Re a = Re b = 0, |a| = |b| and a ⊥ b (cf. Moreno 1998).
   - So the even-parity result holds for every n. All 60,998 clean elements were checked.
   - 1764 = 1680 + 84, so the "84×21" factorization carries no structural meaning.
6. **"Gate 2b resolved structurally on Cℓ(6)" went stale after V4.84.** L32 against L47. [H, medium-high]
   - V4.84 never annotated the μ_n spinor-promotion row (around L4503).
7. **The "most structurally important" open row is frozen.** L39–L71. [C, high]
   - G-ζ1 came back INFORMATIVE-FAIL (3.87× off), and V4.80 then found G-ζ1's state wasn't stationary.
8. **The transverse-line gates ran on a single-component substrate.** L65 and L63. [H, medium]
   - The phonon numbers should carry over, but the gapless internal sector is missing from the species inventory.
   - Without an import, the vacuum is S¹⁵ and knots are not protected, which undercuts the polycrystal postulate's reliance on continuous knot generation.
9. **Minor:**
   - μ_s = ρc_T² is declared definitional (L67), but the identity needs ρ_n.
   - The I4 annotation was never attached (L65).
   - The A2 alpha-decay gate still lacks its source file (L36).

### Lines 73–164: fold records V4.68 back to V4.25

1. **Paper VII's ropelength prediction has already failed.** L105, L107 and L131. [E/F/G, high]
   - 58.006 is the conjectured minimum, not a lower bound.
   - §2.82's four-arc model computes 58.05 in the ledger's units; the units were verified by reproducing G-κ1's 93.8 and 71.1.
   - So the ±0.3 check fails by 2.2, and L = 58.0 gives m_p ≈ 760 MeV.
   - V4.40 banks a third proton length, 80.95.
   - **Action:** apply §2.15's own rule (L652).
2. **The equivalence principle is never confronted.** L141 and L79. [E/B, high]
   - Electrons get "their own ε_e", and binding energy is not a knot.
   - MICROSCOPE needs electron and nucleon response per unit mass to match to about 10⁻¹⁰, and binding energy to about 10⁻¹².
3. **The mass-clause error budget contradicts itself.** L107, L113, L131 and L105. [G/H, high]
   - V4.40 called the tube sub-cell (R1), while V4.48 called the 100φ scale "category-mismatched".
   - G-κ1 found 6–13% dispersion and −41% to −53% screening, above the 3% agreements.
4. **Vortex links can untie, and reconnection is never mentioned.** L107, L129 and L153. [F/H, medium-high]
   - Kleckner, Kauffman & Irvine (Nature Physics 2016). G-κ1's strands sit 2–4ξ apart.
   - §3.4-G2-knot has been on hold since V4.29.
5. **The surviving static gravity picture has two classical problems.** L135 and L129. [E/F]
   - §2.89: locally flat does not mean zero gradient (COW, qBounce, ALPHA-g).
   - §2.90: point defects in isotropic linear elasticity do not interact (Eshelby 1956).
6. **The published gauge paper carries an unclosed audit item.** L91. [B/D/F, high]
   - Whether the J = L_{e₀} sign dressing is a reparametrization of Furey's choices remains open, yet it is part of the v6.3 novelty claim.
   - Against PDG 2024, only tan θ_C = 3/13 survives (0.2σ); sin θ_C = 3/13 is about 8σ off.
7. **CM-3, which sets the sign of attraction, was never validly tested.** L137 and L83. [H/C, medium]
   - T5 assumes a uniform drive, which is the drive V4.37 found knots don't respond to.
8. **The PSL(2,7) Zenodo note was never updated.** L125. [D, high]
9. **Calculator formulas.** L121. [E, medium]
   - m₀φ²⁷ = 82.13 GeV against 80.369 GeV measured.
   - sin²θ_W = φ⁻³ has no stated energy scale.
10. **The κ = φ⁻⁴ solid branch contradicts the computed substrate.** L83 against L73. [G/H, medium]

### Lines 165–1287: Preamble, Part I, Part II §A–F

1. **The μ_n program is aimed at the Δ, not the nucleon.** L1029, L1041 and L1114. [H/B, high]
   - In μ_p = (4μ_u−μ_d)/3, the 4 is a Clebsch–Gordan coefficient, not the size of a spin-3/2 quartet.
   - The symmetric quartet is the Δ, and μ(Δ⁰) = 0.
2. **L_B is the proton mass run backwards, and its one real test fails.** L643–652 and L946. [H/E, high]
   - Solving the §2.14 formula for m_p gives exactly 60.194.
   - A = 20 comes from (t−1)³; the standard Alexander polynomial gives 70.
3. **PSL(2,7) is not the symmetry group of the Császár polyhedron.** L520 and L525; the gauge-paper cross-references at L2159, L2226 and L2235. [H/D, high]
   - §2.86 found AGL(1,7), which has trivial Schur multiplier, so the polyhedron gives no spinor-type representations.
4. **The mass table is presented more strongly than it supports.** L371–386 and L219. [G/E, high]
   - W (+2.2%) and Z (+3.05%) break the 2% headline, and the table uses stale PDG values.
   - m₀ and 100φ are fitted, and look-elsewhere freedom is large.
   - The linear V4.51 mass rule clashes with the exponential formula.
   - The "order-9" stabilizer cannot exist, since 9 does not divide 168.
5. **§1.1's status line is out of date** ("Submitted to Journal of Algebra"). Theorem 2.1 still checks D₄, which is not maximal. [D/G, high]
6. **§2.73's four "invariant" vectors are not in U(L).** L887 against L809 and L830. [G, high]
7. **The "84" cascade near-miss outlives its own retirement record.** L448–458 against L4163. [A/C, medium-high]
8. **The same 0.003% α match is claimed from two starting values,** 240/√3 and 84/arctan(1/√2). L392 against L1337. [G/A, medium-high]
9. **The alpha-decay paper is not tracked, and a by-construction identity sits in Tier 1.** L337–347 and L396–398. [D/A, medium]
10. **Cluster D entries keep R2 labels despite refutation and factual errors.** L486–513. [A/G, high]
    - Tb, Dy, Ho, Er and Tm are f-block ferromagnets.
    - Pb-208 already has a positive alpha-decay energy (about +0.52 MeV).

### Lines 1288–1655: Part II §G–I (physics line, §2.87.J through §2.91)

1. **The transverse line has no tensor-polarized gravitational wave.** L1642 and L1646. [A/E/G, high that it was missed]
   - GW170814 favored tensor over pure vector by a Bayes factor above 200, and GW170817's localized analysis also favors tensor.
   - §2.88.E (L1536) and §2.91.H (L1616) still count GW170817 as passed.
   - **Action:** a gate on detector response and binary radiation rate, tested against LIGO–Virgo and Kramer 2021.
2. **Grain-orientation averaging probably can't hide the 3D transverse-speed split.** L1640 and L1652. [A/E/B/C, medium]
   - The EM window caps grains at 5–20 cells.
   - LHAASO's PeV Crab photons would shrink the window to ≲1.3×10⁻³⁴ m, below a_phys.
   - A textured aggregate is birefringent at first order, and photon polarimetry would force |t| ≲ 10⁻³⁰, against the delivered bound of 1.2×10⁻⁶.
3. **The gapless internal modes of the 16-component substrate are missing from every MV-G1 inventory.** L1522 and L1654. [H/F/D, medium-high]
   - First-order GP dynamics gives type-B branches with ω ≈ k²/2m* and zero Landau critical velocity.
   - Fano-line cores wind in internal directions, so a moving defect excites these modes at any speed.
   - **Action:** read m* off the existing MV-G1 data, and count Goldstone modes per stratum before electing I6.
4. **§2.50.A's 2π "topological trap" was never re-read after G-VS1.** L1373 and L1654. [H/C/G, high]
   - At the vacuum of record π₁ = 0, and on the polar strata the smallest winding is π.
   - r_eff(e) ≡ 1, the m₀ exponent 2π/Φ, and through them the mass table all rest on 2π.
5. **§2.89 and §2.90 contradict the universality of free fall.** L1551. [F/E/G, high]
   - The VC-B and I4 annotations owed to these entries were never attached.
6. **§2.45-NGA is stale.** It ties an electron-shell closure to a nuclear-decay boundary, the type error §2.45-PAIR later named. L1417. [H/G/D, medium]
7. **§2.25.3–6 misstates the α⁻¹ retrodiction.** 84/arctan(1/√2) = 136.479, which is below 137.036. L1337. [G, high]
- **Minor:** G-TSH4 found hcp lowest by about 10⁻⁴, while the published ground state is FCC.

### Lines 1656–3176: Part II §J–L (Fano / sedenion)

1. **The gauge paper is cited for "PSL(2,7) = Császár automorphism group",** but Aut(14-face set) = AGL(1,7), order 42. L2235, L2159, L2226 and §2.74 against L3157. [D/H]
   - PSL(2,7) fixes only one face Fano plane; only F₂₁ fixes both.
   - **Action:** search v6.3 for "automorphism" and "symmetry group".
2. **Signed vs. unsigned lifts.** 21 elements lift without signs, but all 168 lift with signs (8 sign choices each, order 1344). [G/H, high]
   - "PSL(2,7) does not act on 𝒴" and the O_POS/O_NEG chirality come from the basis convention.
   - Affected entries: L3161, L3165, §2.75 VI (L2299) and G-2a.3 (L1706).
3. **Moreno 1998 closes OP-2.81.1 and OP-2.81.2.** n = 6 gives 11,200. The §2.68.8.1 argument is flawed, and the "CLOSED" row for OP-2.67.1b(ii) (L4418) rests on it. [F/A, high]
4. **OP-2.74.1c.i has a one-line answer.** TS_O1 is exactly the twosets with e_a·e_b = −e_{a⊕b}. This also settles OP-2.74.1c.iii. [F, high]
5. **The §2.84A "LEAD" survivor is a labeling coincidence:** 7⊕a ≡ −a mod 7 in these labels. L3135. [A/G, high]
6. **Two Register-1 errors in the spin thread.** [G, high]
   - L2407: no element of SL(2,7) sends u to u³, so the involution is outer.
   - L2799: the order-4 elements generate all of SL(2,7), so their images span M₄(ℂ).
   - SL(2,7) has no order-24 element (L2803).
7. **"The 42 size-2 matchings" is false (K₇,₇−M has 651),** and de Marrais's box-kites go unattributed in §2.55, §2.68.4 and §2.41.B. L2006 and L2014. [G/D, high]
8. **Factual slips.** [F/G, high]
   - K₈ has six 1-factorizations, not two (L1728).
   - arctan(1/√2) = 35.26°, not 54.74° (L1896).
   - log(4π)/log 7 = 1.3007 (L1738).
   - The imaginaries column in §2.53 should read 3, 7, 15.
- **Firewall:** no §7.4 firewall text appears in this range. The Yang–Baxter material is not in paper v6.

### Lines 3177–4285: Part II §M–O, Part III, Part IV

1. **The rank collapse breaks SLWE at every module rank.** L3763 and L3761. [A/B, high]
   - The rank is at most 112 for any k, so the problem reduces to LWE in ≤ 112 dimensions (76 measured).
   - Part VI (L4386) still says "empirically robust".
   - **Action:** one fpylll run at p = 911, then close OP-2.58.2.
2. **The spec parameters are weak even with a random public matrix.** L3434 and L3469. [F/G, high]
   - At fixed noise, a larger q makes lattice attacks easier, not harder.
   - A rough primal estimate gives about 20 bits for n = 512, η = 2, h = 64; the same script gives about 119 bits for Kyber-512.
   - The decryption failure rate is exactly zero (noise ≤ 258 ≪ q/4).
   - **Action:** run the OP-2.58.5 estimator.
3. **The §3.05 correction never reached §§2.59–2.61.** The sum-to-14 rule holds for only 6 of 21 pairs, and the co-line structure equals the Hamming(7,4) syndrome partition. L3278 against L4029. [A/H, high]
4. **G-C1 (§2.64.B) undercut §2.64.A:** ξ/a ≈ 0.06 is sub-cell. L3862 against L3897. [H/C, medium-high]
5. **The verify-then-widen couplings fail current data.** The two formulas also contradict each other at tree level. L3846. [E/D, high]
6. **The C.COSM.4 Plateau argument is wrong:** 120° junctions tile the plane as hexagons, not triangles. L4268 against L4276. [F/G, high]
7. **The §2.69 canary is vacuous:** the prime number theorem for arithmetic progressions already guarantees the uniformity. L3503. [F, high]
8. **The §4.7 blocker contradicts itself:** 7₁ is also chiral. L4185. [G/C/F, medium]
   - Amphichiral knots up to 8 crossings: 4₁, 6₃, 8₃, 8₉, 8₁₂, 8₁₇, 8₁₈.
9. **The cosmogony entries can't be falsified as stated,** and the sedenions are not a division algebra. L4218. [E/G, high]
10. **The §2.62.C stabilizer is D₄, not V₄×ℤ₂.** L3358. [G, high]

### Lines 4286–4630: Part V and Part VI (open tasks)

1. **The ζ-tax redshift can be decided with existing data.** Its four gates have been open since V4.4. L4310, L4324 and L4537–4540. [B/E/H, high]
   - DES measures b = 1.003 ± 0.005 ± 0.010.
2. **The k = 32 crypto break has not been carried into the related rows.** L4386–4392, L4398–4399 and L4479–4480. [A/G/H/C, high]
   - OP-2.58.2e (the Leftover Hash Lemma argument) cannot hold.
3. **The G-VS1 results were not carried back.** L4550, L4340, L4371, L4376 and L4328. [A/H/G, medium]
   - OP-2.14 is filed as closed but depends on an open §2.50 plus I6.
   - G-QUANTA's witness is unprotected.
4. **The η-invariant commission to Flach is probably moot, and possibly ill-posed.** L4516, L4514 and L4503. [A/F/G, medium]
   - Donnelly's η-defect is a finite sum that can be computed in-house.
   - The ledger names S⁷/PSL(2,7), not ℙ¹(2,3,7).
5. **The public "Zero Free Parameters" wording was never updated.** L4440. [C/D, high]
6. **One gate carries two statuses (§2.45-NGA and §2.53).** cos 18° still feeds the α⁻¹ / proton-radius relation. L4343–4344. [G/H, medium-high]
7. **Declarations made for the retired II-B line still shape the ontology** (Branch C, VC-B). L4349 and L4358–4360. [A/G, medium]
8. **§2.52 Open 3 is frozen, about 53 versions.** L4339, L4347 and L4455. [C/G, medium]
9. **The top-quark knot choice is cheap to settle with KnotInfo and the Ashton tables.** L4341, L4185 and L4507. [F/G/C, medium]
10. **The Hubble 1/336 quantization is not tracked and is unfalsifiable as stated.** L4324. [E/H, high]
11. **Gauge paper checks.** L4325 and L4486. [D/E, low-medium]
    - Which observable is 3/13?
    - OP-2.77-FB (Dirac/Weyl language) has been bypassed since V4.7.

## Sources
- LIGO–Virgo, Tests of General Relativity with GW170817: https://arxiv.org/abs/1811.00364
- Cantarella, Fu, Kusner, Sullivan, Wrinkle, Criticality for the Gehring link problem: https://arxiv.org/abs/math/0402212
- DES SN time dilation (White et al. 2024): https://arxiv.org/abs/2406.05050
- Kleckner, Kauffman, Irvine, How superfluid vortex knots untie, Nature Physics 12, 650 (2016)
- Turner et al., PRL 98, 190404: https://www.ma.imperial.ac.uk/~rlbarnet/PhysRevLett_98_190404.pdf
