# Cox, *The Cosserat Supersolid* (v4): what the body says about second sound, drag and Cherenkov radiation

**Plain-language summary.**
- **What we did.** We read all 945 pages of version 4 of the one published proposal that treats empty space as a supersolid. We were looking for anything on a second, slower sound, on drag on moving particles, and on Cherenkov-type radiation. Until now our paper had quoted only the abstract's claim that matter moves through without drag.
- **What it says.** It never mentions second sound, the Landau speed limit or Cherenkov radiation.
  - The no-drag claim is stated, not derived.
  - Where the book does discuss friction, it means friction from the crystal's bumpy periodic potential, which it says quantum smearing removes.
  - It never asks whether a fast particle sheds sound.
- **How it handles compression.** It keeps one compression wave and makes it about 10²⁰ times faster than light, by making the vacuum almost incompressible. That is Green's choice in the nineteenth-century elastic-ether debate. Our draft had placed the proposal in MacCullagh's lineage instead. That was wrong and is now corrected.
- **What our own equations say about it.** The book counts the superfluid's own sound mode once, but folds it into its single compression wave, so a second branch never appears. Our hydrodynamics supplies it.
  - With the book's own numbers (80 % superfluid, almost incompressible), the missing second sound comes out faster than light, at 1.03 to 1.55 times c. Two independent computations agree.
  - So our sonic-boom argument does not catch the proposal's particles. They are crystal defects, chiefly dislocations, and their speed limit is the light speed.
  - It would catch a version that is less than 75 % superfluid, through defects that couple to second sound, such as edge dislocations, which strain the lattice.
- **Correction (October 4, later).** Two statements here about vortex matter did not survive the vortex-coupling derivation (paper Sec. 6, derived twice): that the argument would catch any version whose matter is vortex knots, and that such matter could outrun light. A vortex couples to shear through the normal fraction, so in this corner its drag-free range also ends at the shear speed. Both statements are corrected below, and the modulus written M_µ is now M̃, so that µ means only the shear modulus.
- **For our paper.**
  - Its novelty claim stands: nobody, this proposal included, has computed how matter couples to second sound in a supersolid vacuum.
  - But the paper no longer claims to refute the proposal. Sections 1, 5, 9 and 10 now describe it accurately.

## 1. Source and method

| Item | Value |
|---|---|
| Work | M. A. Cox, "The Cosserat Supersolid: Deriving the Constants of Nature from Vacuum Lattice Mechanics", v4.0, 15 June 2026, Zenodo doi:10.5281/zenodo.20705475. This is Ref. [28] of the paper |
| Text read | The author supplied the pdftotext extraction of `cosseratSupersolidv4.pdf` on 4 Oct 2026: 63,302 lines, 945 printed pages, md5 `f4091750ae4d9da9815d01991299a828`. It is not committed here because it is Cox's monograph. To reproduce, fetch the PDF from Zenodo |
| Full read | Nine readers each read one block of the text in full and answered the same six questions with verbatim quotes and line numbers. The blocks were: front matter and Chs. 1–3; Ch. 4; Chs. 5–6; Chs. 7–9; Chs. 10–15; Chs. 16–21; Chs. 22–24; Chs. 25–28; Chs. 29–33 and Apps. A–H |
| Keyword sweep | `cox_v4_read/sweep.py`, run over the whole text; counts are in `cox_v4_read/sweep_counts.txt` |
| Quote check | Every quote below was re-read chat-side at its line number with `cox_v4_read/cite.py`. Quotes are verbatim, except that mathematics broken by the extraction (superscripts, root signs) is restored in standard notation. Section numbers are the book's; "L" numbers are line numbers in the extraction |
| Check of the paper's wording | A separate reader checked every statement the revised paper makes about the book against the text, looking for counter-evidence. All held in substance. Its wording corrections are applied: wrong section pointers, "chiefly dislocations", "compression branch", the MacCullagh comparison, the emission of compression waves, and the four-dimensional variant |

The six questions:
1. the longitudinal sector and its speed;
2. how the superfluid component is modelled;
3. moving defects, drag, and any argument that there is no drag;
4. Lorentz invariance and the speeds of different modes;
5. how defects couple to compression;
6. anything else bearing on our claim.

**Keyword sweep, whole text.**
- **No hits** for "second sound", "two-fluid", "Landau critical / criterion / velocity", "critical velocity", "Mach", "supersonic", "transonic" or "intersonic".
- **One hit for Cherenkov:** the name of the Cherenkov Telescope Array (Sec. 9.4).
- **No supersolid-acoustics citations.** None of Poli et al.; Kunimi and Kato; Martone and Shlyapnikov; Astrakharchik and Pitaevskii; Son; or Josserand, Pomeau and Rica is cited.
- **Coleman–Glashow:** the only reference is their 1961 paper on the electromagnetic properties of baryons ([183]), not their work on Lorentz violation.

## 2. Findings

### 2.1 The no-drag claim

**Where it is stated:**
- **Abstract:** "The superfluid lets matter drift through without drag, so there is no aether wind for an interferometer to catch." (L16–17)
- **Sec. 2.1:** "The superfluid component lets matter drift through the medium without dragging on it, so there is no aether wind for an interferometer to catch [10]. The vacuum is stiff to fast oscillations, near 10¹⁵ Hz for optical light, and fluid to slow drifts, like the Earth's 30 km/s march around the Sun. A bowl of cornflour and water behaves the same way: it resists a fast punch and yields to a slow hand." (L2570–2574; [10] is Michelson–Morley.) The opening summary of Ch. 2 repeats the point (L2465–2468).
- **App. A:** the vacuum is "rigid enough to support waves at the speed of light, yet frictionless to steady motion, resolving the century-old Michelson–Morley objection that the Earth does not drag through any medium" (L57313–57315), and "the supersolid background lets the defect glide anywhere without resistance" (L57723–57724).

**What friction the book actually evaluates:**
- **Sec. 9.6:** "The Peierls stress τ_P, the threshold stress required to move a dislocation from one lattice valley to the next, is proportional to the amplitude of the periodic potential barrier … In the extreme quantum limit where e^(−2W) ∼ 10⁻²⁸ at the bootstrap f_s = 4/5, the Peierls stress is negligible: dislocations glide essentially without lattice friction." (L16986–16991) The same section says that the form factor and the Debye–Waller factor "suppress the friction of the background against propagating waves (Umklapp processes, Lorentz violation)" (L16975–16976). It then applies this to "a high-energy electron at the LHC" (L16978).
- **Sec. 20.2, on neutrinos:** "Second, lattice friction. An ordinary dislocation in a metal is slowed by Peierls friction. The vacuum lattice removes both pieces of that friction for the edge. … The neutrino is a frictionless relativistic dislocation with a small rest mass; its speed is set by its kinetic energy alone, with no lattice drag." (L29715–29725)

**What is absent everywhere:**
- a Landau criterion;
- drag from the emission of sound;
- a Cherenkov threshold.

The book does say that defects radiate into the compression channel, but it treats that radiation as its pilot wave or as background noise, never as a loss:
- "A defect radiates a longitudinal pressure wave and is then steered by the gradient of its own radiated field." (Sec. 1.4, L1703–1704)
- "each particle is a defect that continuously radiates into the compression channel as it moves" (Sec. 5.12.6, L11183–11184)
- "Each defect radiates compression waves that scatter off other defects, producing a stochastic background of lattice vibrations." (Sec. 5.7, L9589–9590) The same emission is invoked for decoherence in Secs. 31.2.5–31.2.6 (L54640–54643, L54683–54684).

No energy loss is computed. The nearest thing to wave drag is an analogy in Sec. 22.10: a ship's bow wave, where "the object drags its own field along with it, and the drag shows up as a renormalisation of the mass" (L35810–35814).

**Reading.**
- The no-drag claim is an assertion supported by an analogy. The cornflour analogy describes shear thickening, not the Landau criterion.
- Sec. 2.1's own example is a slow drift (30 km/s), and for a slow drift a Landau argument would indeed give no drag.
- The claim is also applied to relativistic particles: LHC electrons in Sec. 9.6 and neutrinos in Sec. 20.2. For these the only support is the suppression of Peierls and Bragg friction.

### 2.2 The longitudinal sector: Green's route

- **Sec. 5.1:** "The vacuum lattice supports two independent wave modes (Chapter 2). The first is the transverse shear wave, which propagates at c … The second is the longitudinal compression wave, which propagates at v_p ≫ c and is the nearly instantaneous pressure mode discussed in Sec. 6.6.1: this is bulk sound." (L8396–8398)
- **Sec. 6.6.1:**
  - "shear and compression come from two distinct broken symmetries of the supersolid. The crystalline symmetry gives the shear modulus µ = ρc²; the superfluid symmetry gives the bulk modulus K_sf" (L11943–11947).
  - Eq. 6.19 gives K_sf/µ ≈ 3.0 × 10⁴⁰.
  - "The Poisson ratio is therefore very close to ν = 1/2: the vacuum is effectively incompressible. The associated longitudinal pressure mode propagates at v_p = c√(K_sf/µ) ≈ 1.7 × 10²⁰ c" (L11960–11964).
- **Two causal cones, accepted:**
  - Sec. 1.4: "Relativity constrains only the shear sector, and that sector carries electromagnetism and particle kinematics." (L1715–1716)
  - Sec. 5.11: "The two light cones differ by twenty orders of magnitude, but each is a legitimate causal cone within its sector." (L10844–10845)
- **Identification:** the mode is the de Broglie–Bohm pilot wave (Secs. 1.4 and 5.1; branch 3 of Table 10.1).
- **The speed is not stated uniformly.** Sec. 9.3.1's zero-point sum uses "1 LA at c_L = 1.245 c" (L16271), and Sec. 25.12 uses the Cauchy value ν = 1/4 (L46189–46190). None of the values given is below c.
- **Other longitudinal branches.** The longitudinal microrotation (branch 9) "is predicted to exist with a comparable propagation speed" (Sec. 10.6.5, L18057–18059). A compact-direction mode runs at "∼ c … far below the compression speed" (Sec. 8.7.1, L14551). Neither is slower than c, and neither is the condensate's phase mode.

**Reading.** This is Green's choice: a longitudinal speed "indefinitely great", reached here through a superfluid bulk modulus. It is not MacCullagh's rotational medium, which has no longitudinal restoring force at all. In the book the Cosserat rotations are extra degrees of freedom, and compression is kept and made stiffer.

### 2.3 The superfluid component

- **Superfluid fraction:** f_s = 4/5 (Sec. 5.7.4, Eq. 5.41), defined as "the share of the medium's mass that flows without resistance" (L9881–9882). The stated range is 0.49 ≲ f_s ≲ 0.98 (L9903). It is used for the Debye–Waller and NCRI suppression of Bragg scattering (Sec. 9.3) and for the derivation of ħ (Ch. 5).
- **Inertia:** "the crystalline density that supplies both inertia and stiffness is ρ_n = (1 − f_s)ρ", and "the transverse speed stays c_s = √(µ_n/ρ_n) = c" (Sec. 9.3.2, L16356–16357 and L16388–16390). So the light speed is a normal-fraction shear speed, as in supersolid hydrodynamics.
- **The phase mode is counted once.** Sec. 25.9: "U(1) gauge symmetry → superfluid. … Breaking this symmetry generates one additional Goldstone mode (the superfluid phase mode), whose stiffness against compression of the condensate number density defines the superfluid bulk modulus K_sf." (L44577–44581)
- **Laboratory supersolids:** Sec. 9.3 notes that they "sustain both transverse (crystalline) and longitudinal (superfluid) Goldstone modes" (L16163–16164).
- **The branch catalogue has no phase-mode branch.** Table 10.1 (Sec. 10.6.5) lists twelve branches, built from the displacement u and the microrotation φ on a two-site cell (L18003–18025). Sec. 20.10 states:
  - "There are no additional modes." (Sec. 20.10.5, L31977)
  - "the symmetry-breaking pattern of the FCC supersolid (T × U(1) → FCC × 1) is fully accounted for, and all Goldstone modes have been identified" (L31993–31994)
  - "the only Goldstone modes are the acoustic phonons (photons and gravitons)" (Sec. 20.10.8, L32060–32061)
- **Sec. 4.5 describes the missing mode's restoring force, in a static setting only:** "The interfacial breathing is a rearrangement of the crystal skeleton at fixed condensate number, through which the superfluid component redistributes freely. Static rearrangements therefore cost only the contact stiffnesses, and the colossal bulk modulus K_sf … engages only when the condensate density itself must change." (L5423–5426)

**Reading.** The book has both ingredients of second sound: a superfluid fraction, and a lattice that can be strained at fixed condensate density. It gives the phase mode's stiffness K_sf to its single compression branch and never writes the two-fluid equations. In those equations the two hybridize into two branches, so the second branch never appears in the book.

### 2.4 Matter and its coupling to compression

- **Matter is crystal defects:**
  - screw dislocation: electron;
  - edge dislocation: neutrino;
  - partial dislocation: quark;
  - vacancy: dark matter;
  - node clusters: hadrons.
- **Limiting speed:** "Frank [143] and Eshelby [144] showed that the total energy of a screw dislocation moving at velocity v through a crystal is E(v) = E₀/√(1 − v²/c_s²), where c_s is the shear wave speed." (Sec. 6.7, L12089–12095) Sec. 20.2 extends this to "any dislocation, screw or edge" (L29705–29706).
- **Which defects source compression (Sec. 10.6.3):** "For a screw dislocation (electron), ∇·u = 0 everywhere (pure shear); screw dislocations do not source the scalar field. For an edge dislocation (neutrino), the Volterra cut creates a localised compression … For a vacancy (dark matter candidate), the volumetric strain is purely compressive" (L17915–17922).
- **Composite objects (Sec. 25.10):** "a spherical inclusion or cluster (such as the 13-node proton) has a large hydrostatic component", and "composite objects couple directly through their volumetric strain fields" (L45506–45515).

**Reading.** In the book's own terms, cosmic-ray protons couple to compression directly; electrons couple to it only at second order.

### 2.5 The Lorentz-violation literature

- **Einstein-aether and khronometric theory** are named. GW170817 is handled this way: "The multimessenger bound |c_gw/c − 1| ≲ 10⁻¹⁵ from GW170817 [132] is satisfied identically, since the microrotation graviton speed is c by construction." (Sec. 5.12.4, L11110–11112)
- **Analogue gravity** (Barceló, Liberati and Visser, [35]) is cited twice:
  - for method (Sec. 1.5, L1895–1897);
  - in the opening of Ch. 9, for the statement that it "showed that emergent Lorentz symmetry is generic in media with linear long-wavelength dispersion" (L15683–15684).

  The mono-metricity problem that the same programme raises (several modes give several metrics, and one metric needs tuning; the paper's Refs. [1–5]) is not discussed.
- **Not cited or discussed:**
  - vacuum Cherenkov radiation;
  - Coleman and Glashow on maximal attainable velocities;
  - Moore and Nelson;
  - Elliott, Moore and Stoica.

## 3. The proposal's parameters in our hydrodynamics (two-leg)

The book never writes supersolid hydrodynamics. So we ask what the standard zero-temperature theory in the paper's Sec. 3 gives for its stated parameters.

**Green's limit (α → ∞).** First sound runs off, c₊ → ∞, and second sound settles at

  c₋²/c_T² → f_s M̃/µ,  with M̃ = lim (M − γ²/α).

Here:
- f_s = ρ_s/ρ is the superfluid fraction;
- c_T² = µ/ρ_n;
- M̃ is the lattice's uniaxial modulus at fixed chemical potential. M̃ = M if the density–strain coupling γ stays finite.

**The bound.** Take an isotropic lattice in d dimensions, with K the lattice bulk modulus at fixed density. Positive-definite energy requires µ > 0, α > 0 and αK > γ², and therefore M̃ ≥ 2(d−1)µ/d. In Green's limit this gives c₋ > c_T whenever f_s > d/[2(d−1)]:
- **three dimensions:** f_s > 3/4;
- **two dimensions:** never, since it would need f_s = 1;
- **four dimensions:** f_s > 2/3 (relevant because the book's lattice is four-dimensional, D4 with a compact direction).

**Mapping from the book's parameters:**
- K_sf ↔ ρ²α;
- f_s ↔ ρ_s/ρ;
- the book's crystalline-sector value K/µ = 5/3 (the Cauchy value, Sec. 25.3) ↔ the fixed-density lattice bulk modulus, so M = 3µ;
- light ↔ c_T;
- isotropy, which the book claims is exact for D4. The book concedes cubic anisotropy for the three-dimensional FCC slice; treating long-wavelength sound as isotropic is our idealization.

| f_s | c₋/c_T with γ finite: first leg / second leg | Stability floor √(4f_s/3): first leg / second leg |
|---|---|---|
| 4/5 (the book's value) | 1.549193 / 1.549193 | 1.032796 / 1.032796 |
| 0.49 (low end of its range) | 1.212436 / 1.212436 | 0.808290 / 0.808290 |
| 0.98 (high end of its range) | 1.714643 / 1.714643 | 1.143095 / 1.143095 |

- **Dimension.** If the lattice is taken as four-dimensional, the floor at f_s = 4/5 is √(1.2) = 1.0954 c_T and the threshold is 2/3. This is the general-d formula of both legs evaluated at d = 4 (`green_limit_check.out`, item 6b). So the conclusion is stronger, not weaker.
- **First sound:** both legs give c₊/c_T = 7.746 × 10¹⁹ at f_s = 4/5, reading K_sf/µ = 3.0 × 10⁴⁰ with µ = ρ_n c_T². With the book's own convention, µ = ρc², it is the book's 1.7 × 10²⁰ c, a factor √5 higher. Either way c₋ is unchanged.
- **Effect of finite K_sf:** it shifts c₋ by less than 10⁻²⁰.
- **First leg:** `../paper/green_limit_check.py`. It derives the result in sympy from the Lagrangian, takes the limits, checks stability, and evaluates the numbers in mpmath at 60 digits. Output is in `green_limit_check.out`; all checks pass.
- **Second leg:** `../paper/green_limit_second_leg/`, an independent derivation run blind to the first. It uses Euler–Lagrange and Hamiltonian routes and a full stability check of the vector problem in d = 2 and 3. It agrees on every formula and every number. Two of its notes are worth keeping:
  - The bound needs the full positive-definiteness condition (αK > γ²), not the weaker plane-wave condition (αM > γ²).
  - In double precision the textbook root formula returns c₋ = 0 here, because the cancellation spans 40 orders of magnitude.

**Consequence.**
- At the book's own f_s = 4/5, the omitted second sound is faster than light for every stable isotropic lattice, in three or four dimensions. If γ stays finite it is about 1.5 c.
- The book takes its matter to be limited to the shear speed, so the Landau–Cherenkov drag of the paper's Sec. 7 is closed to it.
- The drag opens only if f_s M̃/µ < 1, which requires f_s < 3/4 (2/3 in four dimensions). That lies inside the book's stated range (0.49–0.98), but not at its derived value.
- Vortex matter in the same medium is no exception: it couples to shear through the normal fraction (paper Sec. 6), so its drag-free range also ends at the shear speed. (An earlier version of this memo said it could outrun light; that is withdrawn.)

**Limits of this check.**
- It assumes the book's medium obeys standard supersolid hydrodynamics, which the book neither states nor contradicts.
- It covers only the two-fluid longitudinal sector. The Cosserat medium has further branches, for example the longitudinal microrotation, whose speed the text gives inconsistently. These are not assessed here.

## 4. What changed

**In `../paper/second_sound_light_cone_DRAFT.md`:**
- **Sec. 1.**
  - The proposal's particles are now called "defects, chiefly dislocations" (previously "topological defects").
  - One sentence notes that it has a single longitudinal compression branch, which is superluminal, and that it says nothing about second sound.
  - The thesis line now says that second sound's speed is not tied to the shear speed, and that in the standard model supersolid it is slower than shear. It previously read "a sound slower than shear".
  - "A direct test of the no-drag claim" now reads as a test made in the computed model, and the Green's-limit regime is added.
- **Sec. 5** (its paragraph on whether c₂ > c_T is possible). The Green's-limit result and the f_s > 3/4 threshold are added, with the two-leg check as supplementary S6.
- **Sec. 9.**
  - The Green's-limit paragraph now gives how F₋ falls off under both scalings of γ, and points to Sec. 5.
  - The proposal is moved from MacCullagh's lineage to Green's and described as above, including the four-dimensional variant (floor 1.10 c_T, threshold 2/3).
  - The paper's claim that "its no-drag claim holds only if second sound is tuned to the shear speed" is withdrawn. The conditional of §3 replaces it.
- **Sec. 10.**
  - "Refutes, within it, the claim that superfluidity lets matter move without drag" becomes a statement of what superfluidity does and does not do.
  - The c₂ > c_T paragraph gains the Green's-limit route, with its different consequences for matter limited by the shear speed (the book's defects) and for vortex matter.
- **Cover note.** "Always has a second, slower sound" is corrected, and a prior-art line is added.
- **Data and code availability.** S6 now lists the two Green's-limit checks.

**Elsewhere:**
- `PAPER_OUTLINE_AND_ABSTRACT.md`: summary, thesis, prior-art status, and the Sec. 9 line;
- `CITATION_LOG.md`: row 28;
- `VENUE_AND_SUBMISSION.md`: the item is marked done;
- `A1_prior_art.md`: the open item is resolved;
- `../README.md` and `../../STATUS.md`.

**Ledger.** No ledger line is affected. The ledger never mentions the proposal; the word "Cox" occurs in it only inside "Coxeter".

## 5. Files

| File | md5 | What |
|---|---|---|
| `cox_v4_read/sweep.py` | e51702fc | Keyword sweep of the extraction, with a page and section map |
| `cox_v4_read/sweep_counts.txt` | 271c6e07 | Sweep counts by term and section |
| `cox_v4_read/cite.py` | b0e82b2b | Prints a line range with its page and section, for checking quotes |
| `../paper/green_limit_check.py` → `green_limit_check.out` | c0f7c3a7 / 34efbae7 | First leg. Item 6b (the d = 2, 3, 4 evaluation) was added after the comparison; the version compared was 1ee13f4b / 48a49f13 |
| `../paper/green_limit_second_leg/derive.py` → `derive_output.txt` | f415f565 / b3e72acd | Second leg: formulas and the stability test |
| `../paper/green_limit_second_leg/q5_numbers.py` → `q5_numbers_output.txt` | e594bf08 / a3583d9a | Second leg: numbers |

The scripts in `cox_v4_read/` expect the extraction, saved as `cox_v4.txt`, in the working directory.
