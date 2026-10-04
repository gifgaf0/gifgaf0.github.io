# Phase 2 report: what a shared light cone demands, and where the program's survivors stand

Exploration mode: no lock, no two-leg verification, no fold. Nothing here changes the ledger. Written 4 October 2026 (UTC), on base V4.89 plus the Phase 1 banking work.

## Plain-language summary

**The requirement.** Light and matter must share one speed limit, and no wave that matter touches may be slower than light. Otherwise fast matter leaks energy into the slow wave. That leak is the drag found in Phase 1.

**The screen.** I ran five candidate vacua through a five-question checklist. Only one passes without tuning: a vacuum whose stress looks the same in every frame (pressure equal to minus the energy density), with particles as relativistic solitons.
- The supersolid fails: its second sound is slower than its shear "light".
- A two-component superfluid passes only with tuned parameters, and it has no transverse light at all.
- A MacCullagh-type medium passes only for matter that couples to rotation alone. Matter with a density dip in its core feels drag at every speed.
- A Fermi-point vacuum passes only if a symmetry among the particle species is imposed.

**Prior address.** Each survivor checked against the literature:
- "Q = L" (Hopf charge equals linking number) is textbook.
- A baryon built as a vortex ring in one condensate threaded by a vortex of a second condensate, with baryon number equal to the linking of the two kinds of vortex line, is published (2001–2026).
- "Borromean linking = baryon number" is not in refereed work. Two 2026 Zenodo preprints claim it.
- The Z₃ vacuum form uses standard ingredients. Its three minima are one vacuum seen through an SU(3) centre rotation.

**The top question, and the cheap calculation.** Is "Borromean linking = baryon number" a conserved charge? I computed the topological charge (the S³ degree, which is the Skyrme baryon number) of a two-component field for seven explicit configurations. The results are integers to 10⁻⁹.
- The charge counts only links between the vortex lines of the two different components.
- Three Borromean rings in one component carry charge zero on their own.
- With one second-component loop threading one ring, the Borromean rings and the same rings pulled apart carry the same charge, 1.
- By Hopf's degree theorem, field configurations with equal charge can be deformed into one another. So the Borromean core can be unlinked continuously, and in an ordinary superfluid it is: simulated Borromean vortex rings reconnect into separate loops (2025).
- Protecting a Borromean link needs vortex charges that do not commute. A quaternion-coloured version is published (2022), and even that one can be undone by vortex splitting.
- The program's group PSL(2,7) contains the tetrahedral and octahedral groups but not the quaternion group.

**Ranked next questions.**
1. What, if anything, protects a Borromean baryon? The ledger's own vacuum record (vortex charges form ℤ, which is Abelian) suggests nothing topological does. The decisive test is a group computation. The observable is the proton lifetime: Super-Kamiokande's bound needs a decay exponent of about 150.
2. Can a vacuum "in perfect tension" carry light as a shear wave? I expect not, because such a vacuum has zero inertia. A one-page check settles it.
3. Can the mass clause ("energy = line tension × length") live on relativistic strings, which pass the screen? Compare published elastic-rod coefficients and hopfion energies with ideal ropelengths. The observable is the mass ratios.

I stop here. You pick the next question.

---

## 1. Rules as applied

- **Prior Address.** Literature first. Three sweeps were done before this report (`lit/A1_prior_art.md`, `lit/A2_cherenkov_supersolid.md`, `lit/B_solitons_qtheory.md`), plus five targeted checks today (§7). Every source below was fetched and matched. The few that were not are marked.
- **Eddington guard.** No numerology. The tetrahedral group of order 12 in the spin-2 condensate papers below is a coincidence of names with the program's |T| = 12 alpha-decay capacity. Nothing here connects them.
- **M.CW.** The degree calculation uses no physical inputs at all; it is pure topology. The proton-lifetime estimate in Q1 imports two external numbers, named where used: the Super-K bound and a hadronic attempt rate. It is an order-of-magnitude statement only.

---

## 2. The shared-light-cone screen

### 2.1 Checklist

| # | Question | Pass condition |
|---|---|---|
| 1 | What is light? | A transverse (two-polarization) wave at speed c |
| 2 | What is matter? | Named object: defect core, soliton, or quasiparticle |
| 3 | What is matter's limiting speed? | Equals c |
| 4 | What is the slowest wave matter couples to? | At least c |
| 5 | Does uniform motion relative to the vacuum cost energy? | No, for all speeds below c |

**Verdicts:**
- **PASS** means items 3–5 hold by a symmetry of the medium.
- **PASS-only-by-tuning** means they hold only for tuned parameters, an imposed coupling rule, or an imposed symmetry the medium does not supply.
- **FAIL** means they are violated structurally.

### 2.2 Table

| Medium | 1 Light | 2 Matter | 3 Matter's limit | 4 Slowest coupled wave | 5 Friction | Verdict |
|---|---|---|---|---|---|---|
| **Supersolid** (the program's soft-core model, MV-G1) | Shear wave, c_T = √(μ/ρ_n) | Knotted cores with a forced density deficit | The slowest longitudinal sound the cores couple to (Phase 1) | Second sound c₂: at most 0.78 c_T anywhere in the stable phase; 0.06 c_T in 3D. Density weight F₂ ≠ 0 unless ρ_s = 0 or M = ργ | Cherenkov drag ∝ F₂ for v > c₂. Loss length about 39 orders short | **FAIL** |
| **Two-component superfluid** | No shear rigidity, so no transverse wave. "Light" can only be one of the two sounds | Vortex rings and skyrmions, or the massive phonon | The speed of the slower sound it couples to | The slower of the two sounds; they are equal only after tuning [LVW 2006] | Landau/Cherenkov drag above the slower sound | **PASS-only-by-tuning**, and no transverse light |
| **MacCullagh rotational medium** (energy depends only on rotation) | Transverse waves. FitzGerald's map turns its equations into Maxwell's [Whittaker; FitzGerald 1880] | (i) Sources that couple only through rotation; (ii) defects whose cores compress the medium | (i) c, because the equations are Maxwell's; (ii) not fixed by anything | The longitudinal sector has zero restoring force, so its speed is zero and it holds all of the density weight [Whittaker p. 155] | (i) None. (ii) Drag at every speed (see note) | **PASS only for (i)**, which is gauge invariance imposed as a rule. **FAIL for (ii)** |
| **Fermi-point vacuum** (Volovik) | Emergent gauge field; its metric is induced by the fermions | Weyl-fermion quasiparticles (not knots) | Each species' own metric | The medium's own collective modes, whose speeds are material numbers | None at T = 0 below the slowest coupled mode | **PASS-only-by-tuning**, or by an imposed species symmetry [Volovik 2001; Anber–Donoghue 2011] |
| **Lorentz-invariant field vacuum** (T_μν ∝ g_μν, p = −ε; q-theory) | Massless gauge field at c | Relativistic solitons: Skyrmions, hopfions | c exactly: a moving soliton is a boosted static one [Manton–Sutcliffe] | All waves share one metric. Massive modes have phase speed above c, so there is no Cherenkov emission | None: T_μν is the same in every frame [Klinkhamer–Volovik 2008] | **PASS by symmetry**, and the only one |

**Note on the MacCullagh row.** Phase 1's drag formula gives a drag into each branch proportional to that branch's density weight, independent of its speed, once the source outruns it. A branch with zero speed and all of the weight therefore drags at every speed. Physically, a passing density dip leaves the medium moving behind it, as in dynamical friction in a cold, pressureless medium. Cauchy's "labile" ether, with longitudinal speed set to zero, is the historical version of this sector [Whittaker p. 159].

### 2.3 What the screen says

- The requirement holds by symmetry only when the vacuum's stress tensor is boost invariant, so that no frame is special.
- Every medium with a rest frame fails in one of two ways: it has a longitudinal wave slower than its transverse light, or it has no transverse light. Density-coupled matter then feels the slow wave.
- The escapes are always one of three things:
  - tuning (the two-component superfluid);
  - a coupling rule (MacCullagh, i.e. gauge invariance imposed by hand);
  - a species symmetry (the Fermi point).
- The program's discrete group could play the role of Volovik's species symmetry, but only within one irreducible multiplet. Schur's lemma equalizes speeds inside a multiplet, not between multiplets, and not with the medium's own sound. That route also gives up knots as matter.
- Any lattice selects a frame. So the only PASS row contains no lattice. Q2 and Q3 below test what that costs the program.

---

## 3. Prior-address map

| Survivor | Literature status | Key published sources | What is not in the literature | Catch |
|---|---|---|---|---|
| **Q = L** (Faddeev–Hopf: Hopf charge = linking number) | **Has it**; textbook since Whitehead 1947 | Battye–Sutcliffe 1999 ("linked exactly Q times"); Sutcliffe 2007; Kawaguchi–Nitta–Ueda 2008 | Nothing. The ledger already files it as "R1 standard, not an SQT result" | For two linked soliton rings, Q = Q₁ + Q₂ + 2·lk, not lk alone [Harland–Speight–Sutcliffe 2011] |
| **Two-component baryon** (vortex core inside a texture envelope) | **Partly has it** | Ruostekoski–Anglin 2001; Battye–Cooper–Sutcliffe 2002; Babaev–Faddeev–Niemi 2002; Gudnason–Nitta 2020 (×2: "linking number of vortices as baryon number"); Hamada–Nitta–Qiu 2026 | Core Borromean link and envelope Hopf charge as *independent* invariants; mass = ideal ropelength (closest: Buniy–Kephart glueballs; Riedel 2026 nuclear binding) | In the standard two-component class the single topological charge counts core–envelope links (Gudnason–Nitta; confirmed in §5). Field-theory string energy is a Kirchhoff rod energy, not ropelength [Harland–Speight–Sutcliffe] |
| **Borromean linking = baryon number** | **Not in refereed work**; 2026 Zenodo preprints claim it (Aksman ×2) | Adjacent published results: Borromean vortex rings in a Gross–Pitaevskii superfluid reconnect into "unknotted, unlinked loops" [Guan–Zuccher–Liu 2025]. Protection of vortex links needs non-commuting charges [Poénaru–Toulouse 1977; Kobayashi et al. 2009; Annala et al. 2022]. Milnor's μ̄ is a Pontryagin invariant of a T³ → S² map [DeTurck et al., arXiv] | A baryon whose number is a protected Borromean invariant | Not a conserved charge of a two-component field (§5). Conserved only if the three lines can never pass through one another |
| **Z₃ vacuum form** (Φ in the symmetric 6 of SU(3), −γ Re det Φ) | **Partly has it** | 't Hooft determinant for (3, 3̄) at N_f = 3 [Lenaghan–Rischke–Schaffner-Bielich 2000; Pisarski–Wilczek 1984]; Z(3) Wilson-line potentials [Pisarski 2000] | The symmetric-6 form with Re det Φ was not found as a standard construction | Its three minima lie on one SU(3) orbit (the centre acts as ω² on the 6; `lit/sym6_check.py`), so they are one vacuum and there are no Z₃ walls. The ledger already gives it "no assigned physical role" |

---

## 4. Ranked questions

### Q1 (top). What protects a Borromean baryon, and is the proton then stable enough?

**Why.** The two-component baryon on the ledger puts baryon number in the Borromean linking of the core. §5 shows that the field's topological charge cannot see that linking. The linking is therefore either protected by something else or not protected.

**Expectation for the next step.** Protection needs non-commuting vortex charges, i.e. a non-Abelian fundamental group of the vacuum manifold. With a U(1) core it fails outright. With non-Abelian charges it can hold against reconnection and strand crossing, but not against vortex splitting [Annala et al. 2022].

**Decisive test, in three cheap-to-moderate steps.**
1. **Bookkeeping.** Is the core one complex (U(1)) field? If yes, the claim is dead as topology. It survives only as energetic metastability, which needs a barrier.
   - This step may already be answered on the record. G-VS1 (§2.91.U, V4.88) found the protected vortex sector to be the U(1) winding: π₁ = ℤ on every stratum except ferro-7, with half-quantum vortices on the polar strata. That group is Abelian, so Poénaru–Toulouse's commutator obstruction to crossing is trivial.
   - If the core's lines are those vortices, nothing topological protects their Borromean linking. Only two options remain: a non-Abelian sector that is not yet on the record, or energetic metastability.
2. **Computation.** If the core has non-Abelian charges in some group G, enumerate the G-colourings of the Borromean rings. These are the homomorphisms from the link group, read off the closed braid (σ₁σ₂⁻¹)³, to G. Keep those whose three meridians pairwise do not commute. Then evaluate Annala et al.'s coloured-link invariant on each.
   - This is exactly the ledger's own candidate (b) under §2.70, "homomorphisms to non-abelian targets such as PSL(2,7)". The step gives it a physical meaning and a published criterion.
   - Side fact, computed today (`q1_group_check.py`): PSL(2,7) contains A₄ and S₄ but no Q₈. Its double cover SL(2,7) does contain Q₈. So the published Q₈ example does not transfer verbatim.
3. **Observable.** If protection holds only up to splitting, the proton decays through a barrier. Super-K gives τ/B(p → e⁺π⁰) > 2.4 × 10³⁴ yr (90% CL). With a hadronic attempt rate m_p c²/ħ ≈ 1.4 × 10²⁴ s⁻¹ (an import), the decay exponent must satisfy S ≳ ln(1.1 × 10⁶⁶) ≈ 152. Weaker channel bounds lower this only logarithmically.

**Cost.** Step 1 is reading. Step 2 is a few seconds of enumeration plus implementing one published invariant.

### Q2. Can a vacuum "in perfect tension" carry light as a shear wave?

**Why.** The screen's only symmetric pass has T_μν ∝ g_μν, i.e. p = −ε. This is the brief's lead (a), §2.90's tensioned ground state read as perfect tension, and Klinkhamer–Volovik's self-sustained vacuum.

**Expectation: no.**
- In a relativistic elastic medium, shear waves travel at v² = μ/(ε + p) [Battye–Moss 2009]. The enthalpy ε + p is the medium's inertia, and it is what a rest frame is made of.
- Perfect tension sets ε + p = 0. Then either μ = 0 (no shear light) or the shear speed is infinite.
- The program's light is c_T² = μ/ρ_n, which needs the inertia ρ_n > 0, so it needs a rest frame.
- Separately, a network of tensioned filaments or sheets has w = −1/3 or −2/3 [Bucher–Spergel 1999], never −1. So §2.90's lattice of tensioned threads is not a perfect-tension vacuum in any case. Note that w = −1/3 is exactly the line below which expansion accelerates (ä ∝ −(ε + 3p)).

**Decisive test.** A short analytic note:
1. Write the substrate's rest-frame stress tensor and identify the inertia carried by its shear waves.
2. Compute w for §2.90's network in its 3D embedding.

If the expectation holds, lead (a) and "light = shear wave of the substrate" are mutually exclusive. Adopting lead (a) would mean light is not a substrate wave.

**Observable.** A substrate rest frame shows up as Phase 1's matter drag and as Lorentz-violation signals. A filament-network vacuum energy cannot drive accelerated expansion.

**Cost.** Cheap.

### Q3. Can the mass clause survive on relativistic strings?

**Why.** In the only PASS vacuum, matter is relativistic: a moving object is a boosted static one and feels no drag. The ledger's mass clause, "filament energy = line tension × length", is the energy of a relativistic (Nambu–Goto) string at leading order. The clause is therefore not tied to the failing supersolid; only the filament's home is.

**Internal prior address.** The ledger already records that the filament reading (energy organized by ropelength) and the texture reading (energy ~|Q|^{3/4}, Vakulenko–Kapitanskii) are "connectable but not energy-identifiable". The two-component declaration put the ropelength mass on the core for that reason. What is new here is the screen's verdict: only the relativistic reading passes. So the question is whether a Lorentz-invariant field theory has knotted strings whose energy stays ropelength-organized.

**Expectation: no, not at the 2% level the dictionary needs.**
- Closed relativistic strings have no static knotted minima on tension alone; something must stabilize them.
- In the known field theory that does stabilize them (Skyrme–Faddeev), the string energy is a Kirchhoff elastic-rod energy with bending and twist terms [Harland–Speight–Sutcliffe 2011]. Ideal ropelength is only its tension-dominated limit, and tight knots have curvature radii comparable to their thickness.
- Energies obey E ≥ c Q^{3/4}, and the lowest state of a given Q is often a link, not a knot [Sutcliffe 2007].

**Decisive test.**
1. Evaluate the bending and twist share of the rod energy on the ideal (tight) shapes of the dictionary's knots, using Harland–Speight–Sutcliffe's coefficients. Cross-check against published hopfion energies where a knotted minimum exists (e.g. the trefoil). If the non-tension share exceeds the dictionary's agreement band, the clause and the relativistic route cannot both hold.
2. If the share is small, minimize the cable knots (muon, tau) in the field theory. That is a real project.

**Observable.** The fermion mass ratios.

**Cost.** Step 1 is cheap (published coefficients and tables). Step 2 is expensive.

---

## 5. Q1 first calculation: the topological charge of Borromean configurations

### 5.1 Expectation, filed before computing

- `Q1_EXPECTATION_pre_compute.md`: md5 8502c2337ceb1bd179ee3ff85b98621c, 05:00:45 UTC.
- `Q1_EXPECTATION_ADDENDUM_pre_compute.md`: md5 b09baecd88660e1b6f0191a55c1e8227, 05:10:41 UTC. The addendum adds the calibration a′, configuration f and the linking cross-check.
- The first full run started at 05:15:44 UTC. The recorded rerun at 05:32:44 UTC only adds two more projections to the link-type check; all numbers are identical.

The expectation was NO: the charge counts pairwise cross-component links and is blind to Borromean linking within one component.

### 5.2 Setup

- **Fields.** Two complex fields z₁, z₂ with n = (z₁, z₂)/|(z₁, z₂)| on S³. This is the standard class of a vortex core in one condensate inside a second condensate.
- **Boundary condition.** z₁ → 0 and z₂ → 1 at infinity. This is the program's declared envelope-dominated vacuum (ρ₁∞ = 0).
- **Charge.** B = (1/2π²)∫det[n, ∂ₓn, ∂ᵧn, ∂_z n] d³x, computed as det[Z, ∂Z]/|Z|⁴ with analytic derivatives. Midpoint rule on [−6.5, 6.5]³ at N = 128, 192 and 256.
- **Geometry.**
  - Borromean rings: three mutually perpendicular ellipses with semi-axes 2 and 1, z₁ = f_A f_B f_C (1+r²)⁻³ e^{−r²/6.25}.
  - z₂ loops: radius 0.5, z₂ = f_D/(1+r²) for one loop and f_D₁f_D₂f_D₃/(1+r²)³ for three. In (b), z₂ = (1 + r² + 2iz)/(1+r²), which never vanishes.
  - The amplitude of z₁ is set per configuration so the integrand is resolved. This is topologically irrelevant.

### 5.3 Results (N = 256; stable to < 4 × 10⁻⁵ already at N = 128)

| | Vortex lines of z₁ | Vortex lines of z₂ | Expected | **B** | Σ links (Gauss integrals) |
|---|---|---|---|---|---|
| a | z-axis (identity map) | unit circle | 1 minus the box tail (≥ 0.9941) | **0.99641** | — |
| a′ | ring A | loop D₁ through A | 1 | **1.000000** | 1 |
| b | Borromean A, B, C | none (z₂ never zero) | 0 | **0.000000** | 0 |
| c | Borromean A, B, C | D₁ through A only | 1 | **1.000000** | 1 |
| d | Borromean A, B, C | D′ linking none | 0 | **0.000000** | 0 |
| e | A, B, C pulled apart (unlinked) | D₁ through A only | 1 (= c) | **1.000000** | 1 |
| f | Borromean A, B, C | D₁, D₂, D₃, one through each ring | 3 | **3.000000** | 3 |

**Checks.**
- (a) The identity map's integrand equals 8/(1+r²)³ pointwise to 4 × 10⁻¹⁵.
- **Link type.** Pairwise Gauss linking numbers are 0 for both ring triples. A Kauffman-bracket state sum on a generic projection gives:
  - the Borromean triple: the Jones polynomial of the Borromean rings, −t³ + 3t² − 2t + 4 − 2t⁻¹ + 3t⁻² − t⁻³;
  - the pulled-apart triple: that of the 3-component unlink, t + 2 + t⁻¹.

  Both results hold in all three recorded projections (12, 8 and 12 crossings for the Borromean triple; 4, 6 and 0 for the pulled-apart triple).
- None of the expectation's falsifiers fired:
  - B(b) = 0;
  - B(d) = 0;
  - B(c) = B(e).

### 5.4 Why: an analytic argument the numbers confirm

- Take the target point (z₁, z₂) = (0, −1). Its preimages are the points on z₁'s vortex lines where z₂ is real and negative.
- Along ring i, the phase of z₂ winds lk(ring i, zero set of z₂) times. So the signed count of preimages, which is the degree, is Σᵢ lk(ring i, z₂'s lines).
- The point at infinity maps to (0, 1), not (0, −1), so it never contributes.
- The rings' linking among themselves never enters.
- By Hopf's degree theorem (standard), based maps S³ → S³ are classified up to homotopy by this number. Two consequences:
  - Configuration c (Borromean) can be deformed continuously into e (unlinked), with no singularity.
  - Configurations b and d can be deformed into the vacuum.

### 5.5 What it means

- **In the two-complex-field class, the conserved charge is the number of core–envelope links**, as in Gudnason–Nitta. That is case f: three rings each threaded once give B = 3.
- **With an envelope that never vanishes (cores filled, condensed outside), B = 0 whatever the core's link type.** That is case b.
- **The Borromean structure of the core lines is not conserved by topology in either case.** With a U(1) core, the lines can reconnect, and in Gross–Pitaevskii dynamics they do (Guan–Zuccher–Liu 2025).
- **Relation to the ledger.**
  - This sharpens the "Hopf-blindness becomes a prediction" clause of the two-component baryon declaration. The envelope's charge is blind to the core's Borromean linking, as declared. In addition, that linking is not a conserved charge of anything in this class.
  - If the program's envelope is a richer (quaternionic) field, it can carry its own Hopf charge. The core's Borromean link type is still not invariant under deformations of one U(1) core field.

### 5.6 What it does not mean

- **Energetics are not addressed.** Homotopic does not mean cheap: a tight configuration can sit behind an energy barrier. Q1's step 3 is where barriers enter.
- **The link-invariant work is untouched.** The ledger's link-invariant computations (Milnor μ̄ of the configuration) describe the link and are unaffected. The open issue is conservation, not the value.
- **Not a model of the declared object.** This is a calculation in a standard model class, not a model of the program's quaternionic envelope.

---

## 6. Limits and what was not done

- **The screen is qualitative** except for the supersolid row, which carries Phase 1's numbers.
- **The Fermi-point row** relies on Volovik's statements about species symmetry (verified quotes), not on a calculation.
- **Not computed:**
  - the PSL(2,7) colourings and Annala et al.'s invariant (Q1, step 2);
  - w for §2.90's network (Q2);
  - any hopfion energy (Q3).
- **Partial sources.** Some literature items are verified from abstracts or fetched excerpts only. The lit files mark which (e.g., the DeTurck et al. journal references; the Manton–Sutcliffe boost statement from lecture notes).
- **Phase 1 carry-over.** The Cox preprint body remains unread.

## 7. Files (in `lbc_bank/phase2/` on the repo branch)

- `PHASE2_REPORT.md`: this report.
- `Q1_EXPECTATION_pre_compute.md` and `Q1_EXPECTATION_ADDENDUM_pre_compute.md`: filed before computing.
- `q1_degree_check.py` (md5 3085e8c3b83b54c26d1a9de4ccf611fe) → `q1_degree_check.json` (8fb234d860aa98f620102634da5f2606) and `.log`. It covers the degree integrals, the Gauss linking integrals and the Kauffman bracket. Run with `python3 q1_degree_check.py 128 192 256` (about 2 minutes).
- `q1_group_check.py` (823f9c8a3dd9f06050b85187e1467b06) → `q1_group_check.json` (c023bae0b87c3a4684f1170645d2d951): the Q₈/A₄/S₄ content of PSL(2,7) and SL(2,7).
- `../lit/`: the three literature sweeps and `sym6_check.py`.

## Sources

**New checks for this report** (fetched 4 October 2026):
- T. Annala, R. Zamora-Zamora, M. Möttönen, "Topologically protected vortex knots and links," Commun. Phys. 5, 309 (2022). [nature.com](https://www.nature.com/articles/s42005-022-01071-2)
- M. Kobayashi, Y. Kawaguchi, M. Nitta, M. Ueda, "Collision dynamics and rung formation of non-Abelian vortices," PRL 103, 115301 (2009). [APS](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.103.115301), [ar5iv](https://ar5iv.labs.arxiv.org/html/0810.5441)
- V. Poénaru, G. Toulouse, "The crossing of defects in ordered media and the topology of 3-manifolds," J. Physique 38, 887 (1977). [journal page](https://jphys.journaldephysique.org/articles/jphys/abs/1977/08/jphys_1977__38_8_887_0/jphys_1977__38_8_887_0.html)
- H. Guan, S. Zuccher, X. Liu, "Topological cascade of quantum Borromean rings," Phys. Fluids 37, 024126 (2025). [author PDF](https://zucchers.github.io/downloads/GZL_POF2025.pdf)
- G. W. Semenoff, F. Zhou, "Discrete symmetries and 1/3-quantum vortices in condensates of F=2 cold atoms," PRL 98, 100401 (2007). [INSPIRE](https://inspirehep.net/api/arxiv/cond-mat/0610162). Background for Q1 only: the cyclic spin-2 phase has both non-Abelian charges and fractional vortices.
- Super-Kamiokande Collaboration, "Search for proton decay via p → e⁺π⁰ and p → μ⁺π⁰ with an enlarged fiducial volume in Super-Kamiokande I–IV," PRD 102, 112011 (2020). [arXiv:2010.16098](https://arxiv.org/abs/2010.16098)
- M. Bucher, D. N. Spergel, "Is the dark matter a solid?," PRD 60, 043505 (1999). [INSPIRE](https://inspirehep.net/api/arxiv/astro-ph/9812022)
- R. Battye, A. Moss, "Anisotropic dark energy and CMB anomalies," PRD 80, 023531 (2009). [arXiv:0905.3403](https://arxiv.org/html/0905.3403)

**From the earlier sweeps:** URLs, quotes and verification status are in `lit/B_solitons_qtheory.md` and `lit/A1_prior_art.md`. They include:
- Barceló–Liberati–Visser; Liberati–Visser–Weinfurtner (CQG 23, 3129 and PRL 96, 151301, 2006);
- Volovik (JETP Lett. 73, 162, 2001; Phil. Trans. A 366, 2935, 2008); Anber–Donoghue (PRD 83, 105027, 2011); Klinkhamer–Volovik (PRD 77, 085015 and 78, 063528, 2008);
- Whittaker (1910, ch. V); FitzGerald (Phil. Trans. 171, 691, 1880);
- Battye–Sutcliffe (PRL 81, 4798, 1998; Proc. R. Soc. A 455, 4305, 1999); Sutcliffe (Proc. R. Soc. A 463, 3001, 2007); Harland–Speight–Sutcliffe (PRD 83, 065008, 2011); Kawaguchi–Nitta–Ueda (PRL 100, 180403, 2008);
- Ruostekoski–Anglin (PRL 86, 3934, 2001); Battye–Cooper–Sutcliffe (PRL 88, 080401, 2002); Babaev–Faddeev–Niemi (PRB 65, 100512, 2002); Gudnason–Nitta (PRD 101, 065011 and 102, 045022, 2020); Hamada–Nitta–Qiu (JHEP 02 (2026) 200);
- Buniy–Kephart (PLB 576, 127, 2003); Riedel (Particles 9, 43, 2026); DeTurck et al. (arXiv:0901.1612, 1101.3374); Aksman (Zenodo 10.5281/zenodo.21252830 and .21689199);
- Lenaghan–Rischke–Schaffner-Bielich (PRD 62, 085008, 2000); Pisarski–Wilczek (PRD 29, 338, 1984); Pisarski (PRD 62, 111501, 2000);
- Manton–Sutcliffe (*Topological Solitons*, CUP 2004; boost statement from lecture notes).

**Standard results used without a specific source:**
- Hopf's degree theorem;
- Schur's lemma;
- the Friedmann acceleration equation;
- the Jones polynomials of the Borromean rings and of the unlink.
