# A1 — Prior-art sweep: supersolid vacuum, light = shear sound, matter = defect cores, second-sound Cherenkov limit

Sweep date: 2026-10-03. Tools: WebSearch and WebFetch only.

## How this was checked

- **Quotes.** The WebFetch summarizer will only return verbatim quotes of 125 characters or less. Longer passages therefore appear as consecutive verbatim pieces. Every quote below is 30 words or fewer and comes from the page listed with it. Where math appears, it is transcribed as the tool returned it.
- **arXiv metadata.** A WebFetch of an `arxiv.org/abs/...` page returns only the abstract, not the Journal-ref or DOI fields. Journal metadata were therefore checked against one of: the INSPIRE API (`inspirehep.net/api/arxiv/<id>` or `/api/doi/<doi>`), the CrossRef API (`api.crossref.org/works/<doi>`), or the journal's landing page.
- **Blocked sites.** These sites blocked fetches or returned 403/405/429: APS journals, ADS, Wiley, PubMed/PMC, IOP, De Gruyter, World Scientific, ResearchGate, GitHub and OSTI.
- **Whittaker (1910).** Read from the Wikisource page-scan transcriptions. PDF page N is printed page N−20; this offset was checked on printed pp. 150, 151, 153, 154 and 159.
- **Status labels.**
  - **VERIFIED**: I fetched a page on which authors, title, journal, volume, page and year all match.
  - **PARTIAL**: some fields were confirmed and others were not. Each PARTIAL entry says which.
  - **NOT FOUND**: I could not confirm the item.

---

## 0. Bottom line

**(a) Is the thesis already published?**

- **The general statement is published. Cite it; do not claim it as new.** The statement is: in emergent/analogue media, different excitations generically have different limiting speeds; matter that outruns a slower mode it couples to radiates (Cherenkov); and a shared light cone needs fine tuning or a very long RG flow. The closest prior statements are:
  - Barceló–Liberati–Visser 2002: multi-metricity is generic; a unique metric must be enforced.
  - Visser–Weinfurtner 2005 and Liberati–Visser–Weinfurtner 2006: two phonon modes are generically bi-metric, and equal speeds require tuning.
  - Comer, as reported in Living Rev. Relativ. 2011: first and second sound give multiple acoustic metrics.
  - Collins et al. 2004: "unnaturally strongly fine-tuned".
  - Anber–Donoghue 2011: different limiting speeds are generic; c_e > c gives Cherenkov emission; equalisation is only logarithmic.
  - Coleman–Glashow 1997/1999: species-dependent maximal attainable velocities; vacuum Čerenkov radiation.
  - Moore–Nelson 2001 and Elliott–Moore–Stoica 2005: matter faster than a slower gravitational or aether mode it couples to emits Cherenkov radiation, so the mode speed is bounded below.
  - Chadha–Nielsen 1983 is the counter-position: Lorentz invariance as an IR attractor.
- **The specific supersolid computation was not found in the peer-reviewed literature.** No published work found does both of the following:
  - (i) identifies light with the shear sound of a supersolid vacuum and matter with defect cores that carry a density deficit; and
  - (ii) computes how the cores couple to second sound, deriving the Landau–Cherenkov limit (matter speed limit c₂ below the shear speed c_T).
- **Closest overlap (not peer-reviewed).** One Zenodo monograph (M. A. Cox, "The Cosserat Supersolid", v2–v4, March–June 2026) proposes:
  - the vacuum as a supersolid;
  - light as the transverse shear wave;
  - particles as dislocations.

  But its record description asserts the opposite of the thesis: *"The superfluid lets matter drift through without drag, so there is no aether wind for an interferometer to catch."* Its 6.7 MB PDF could not be parsed with WebFetch, so whether the body discusses second sound is **unverified**. Check the PDF by hand before asserting novelty.
- **The condensed-matter ingredients do exist, separately:**
  - In the soft-core 2D Gross–Pitaevskii supersolid, the ordering is c₂ < c_T < c₁, and second sound carries weak but nonzero density weight (Poli et al., PRA 2024).
  - Drag and critical-velocity calculations exist for supersolids (Martone–Shlyapnikov 2018; Kunimi–Kato 2012).
  - Defects in an elastic medium move with "Lorentz" kinematics whose limiting speed is the shear speed (Frank 1949; Eshelby 1949).
  - The Kleinert–Zaanen world crystal explicitly has "an extra longitudinal sound wave with a different velocity than the shear waves."

**(b)** Verified citations for all requested items follow, with corrections where your metadata was off (summarised in §6).

---

## 1. Superfluid-vacuum programs

### 1.1 Volovik

**[VERIFIED]** G. E. Volovik, *The Universe in a Helium Droplet*
- Publisher: Oxford University Press (Clarendon Press), International Series of Monographs on Physics.
- Published 15 May 2003; ISBN 9780198507826. Page count: 530 pp. per OUP; 509 pp. per the Aalto research portal.
- The series number 117 is not shown on the OUP page; it appears only on retailer listings.
- Fetched: https://global.oup.com/academic/product/the-universe-in-a-helium-droplet-9780198507826 ; https://research.aalto.fi/en/publications/the-universe-in-a-helium-droplet-the-international-series-of-mono
- Quote (OUP description): "The text presents a general overview of analogies between phenomena in condensed matter physics on one hand and quantum field theory and elementary particle physics on the other."
- Relevance: the canonical superfluid-vacuum monograph.

**[VERIFIED]** G. E. Volovik, "Superfluid analogies of cosmological phenomena"
- Phys. Rep. 351, 195–348 (2001); arXiv:gr-qc/0005091; DOI 10.1016/S0370-1573(00)00139-3.
- Fetched: https://inspirehep.net/api/arxiv/gr-qc/0005091 ; https://arxiv.org/abs/gr-qc/0005091 ; https://ar5iv.arxiv.org/html/gr-qc/0005091
- Quote (abstract): "Superfluid 3He-A gives example of how chirality, Weyl fermions, gauge fields and gravity appear in low energy corner together with corresponding symmetries, including Lorentz symmetry and local SU(N)."
- Quote (text): "the chiral fermions as well as gauge bosons and gravity field arise as fermionic and bosonic collective modes of the system."
- The table of contents includes "XIII.2 Landau critical velocity and ergoregion".

**[VERIFIED]** G. E. Volovik, "Reentrant violation of special relativity in the low-energy corner"
- JETP Lett. 73, 162–165 (2001) [Pisma ZhETF 73, 182]; arXiv:hep-ph/0101286; DOI 10.1134/1.1368706.
- Fetched: https://inspirehep.net/api/arxiv/hep-ph/0101286 ; https://arxiv.org/abs/hep-ph/0101286
- Quote: "the energy region, where the special relativity holds, can be sandwiched from both the high and low energies sides by domains where the special relativity is violated."
- Relevance: emergent special relativity is approximate even in the IR.

**How Volovik's program represents light and matter.**
- Matter is fermionic quasiparticles (Weyl fermions at Fermi points in ³He-A).
- "Photons" (effective gauge fields) and gravity (effective metric) are bosonic collective modes of the same vacuum.
- In ⁴He, the phonons see the acoustic metric, and the effective "speed of light" is the sound speed.
- Landau critical velocity and ergoregions are treated (Phys. Rep. §XIII.2).
- In the fetched text I found no analysis of multiple longitudinal sound branches, and no Cherenkov drag of matter by a slower mode.

### 1.2 Kerson Huang

**[VERIFIED]** K. Huang, *A Superfluid Universe*
- World Scientific, published 4 July 2016; DOI 10.1142/10249; ISBN 9789813148451 (print), 9789813148475 (electronic).
- Fetched: https://api.crossref.org/works/10.1142/10249 ; https://books.google.com/books/about/A_Superfluid_Universe.html?id=tY34DAAAQBAJ
- Quote (Google Books description): "theory describing the universe as a quantum superfluid, and how dark energy and dark matter arise"

**[VERIFIED]** K. Huang, "Dark Energy and Dark Matter in a Superfluid Universe"
- Int. J. Mod. Phys. A 28, 1330049 (2013); arXiv:1309.5707; DOI 10.1142/S0217751X13300494. Also reprinted in a proceedings volume, DOI 10.1142/9789814590112_0002.
- Fetched: https://inspirehep.net/api/arxiv/1309.5707 ; https://arxiv.org/abs/1309.5707
- Quotes: "The vacuum is filled with complex scalar fields, such as the Higgs field." / "Quantum turbulence (chaotic vorticity) in the early universe was able to create all the matter in the universe"

**How Huang's program represents light and matter.**
- The vacuum superfluid is a complex scalar (Higgs-type) order parameter.
- Matter was created by quantum turbulence (vortices); dark matter is superfluid-density halos.
- Photons are not modelled as excitations of the superfluid.
- No Cherenkov or multiple-sound discussion was found in the fetched abstracts.

### 1.3 Zloshchastiev ("superfluid vacuum theory", logarithmic BEC)

**[VERIFIED]** K. G. Zloshchastiev, "Logarithmic nonlinearity in theories of quantum gravity: Origin of time and observational consequences"
- Grav. Cosmol. 16, 288–297 (2010); arXiv:0906.4282; DOI 10.1134/S0202289310040067.
- Fetched: https://inspirehep.net/api/arxiv/0906.4282 ; https://arxiv.org/abs/0906.4282
- Quotes: "Similar thing happens to the Lorentz invariance - in the resulting theory it becomes an asymptotic low-energy phenomenon." / "transluminal phenomena in the physical vacuum such as the Cherenkov-type shock waves."

**[VERIFIED]** K. G. Zloshchastiev, "Spontaneous symmetry breaking and mass generation as built-in phenomena in logarithmic nonlinear quantum theory"
- Acta Phys. Polon. B 42, 261–292 (2011); arXiv:0912.4139; DOI 10.5506/APhysPolB.42.261.
- Fetched: https://inspirehep.net/api/arxiv/0912.4139 ; https://arxiv.org/abs/0912.4139
- Quote: "we view the physical vacuum as a kind of the fundamental Bose-Einstein condensate embedded into the fictitious Euclidean space."

**[VERIFIED]** K. G. Zloshchastiev, "Vacuum Cherenkov effect in logarithmic nonlinear quantum theory"
- Phys. Lett. A 375, 2305–2308 (2011); arXiv:1003.0657; DOI 10.1016/j.physleta.2011.05.012.
- Fetched: https://inspirehep.net/api/arxiv/1003.0657 ; https://arxiv.org/abs/1003.0657 ; https://ar5iv.arxiv.org/html/1003.0657
- Quote: "some of the obtained results must be valid for any Lorentz-invariance-violating theory describing the vacuum by (effectively) continuous medium in the long-wavelength approximation."
- Quote (text): "A particle moving with speed v, c_n≤v≤c, momentum p and energy E emits at some point the photon with energy E_γ, momentum p_γ and velocity c_n."

**[VERIFIED]** K. G. Zloshchastiev, "Superfluid vacuum theory and deformed dispersion relations"
- Int. J. Mod. Phys. A 35, 2040032 (2020); arXiv:2011.11897; DOI 10.1142/S0217751X20400321.
- Fetched: https://inspirehep.net/api/arxiv/2011.11897 ; https://arxiv.org/abs/2011.11897
- Quote: "Using the logarithmic superfluid model of physical vacuum, one can formulate a quantum theory, which successfully recovers Einstein's theory of relativity in low-momenta limit"
- Also from the abstract: "a photon acquires effective mass".

**How Zloshchastiev's program represents light and matter.**
- The vacuum is a scalar BEC with logarithmic nonlinearity.
- Light is the low-momentum (phonon-like) excitation of that single condensate, with a deformed, roton-like dispersion at high momentum.
- His "vacuum Cherenkov" effect is a particle emitting photons because it outruns the photon's momentum-dependent speed (a vacuum refractive index). It is not emission into a second, slower longitudinal branch.
- No supersolid, shear or two-longitudinal-branch analysis was found.

### 1.4 Sbitnev

**[VERIFIED]** V. I. Sbitnev, "Hydrodynamics of the Physical Vacuum: I. Scalar Quantum Sector"
- Found. Phys. 46, 606–619 (2016), published online 8 Jan 2016; DOI 10.1007/s10701-015-9980-8.
- The search listing gives arXiv:1504.07497; I did not fetch the arXiv page.
- Fetched: https://link.springer.com/article/10.1007/s10701-015-9980-8
- Quote: "Physical vacuum is a special superfluid medium."

**[VERIFIED]** V. I. Sbitnev, "Hydrodynamics of the Physical Vacuum: II. Vorticity Dynamics"
- Found. Phys. 46, 1238–1252 (2016); DOI 10.1007/s10701-015-9985-3.
- Fetched: https://link.springer.com/article/10.1007/s10701-015-9985-3
- Quote: "The vortex ball resulting from topological transformation of the vortex ring is considered as a model of a particle with spin."

**How Sbitnev's program represents light and matter.**
- The vacuum is a superfluid of virtual pairs, described by a modified Navier–Stokes equation that reduces to the Schrödinger equation.
- A particle is a vortex ball (vortex topology). This is the closest of these programs to "matter = vortex knots".
- Light is not modelled in these two papers, and there is no Cherenkov or multiple-sound discussion.

---

## 2. Crystal / elastic vacua

**[VERIFIED (metadata); quote via secondary source]** H. Kleinert, "Gravity as a Theory of Defects in a Crystal with Only Second Gradient Elasticity"
- Ann. Phys. (Leipzig) 499 [7. Folge Bd. 44], no. 2, 117–119 (1987); DOI 10.1002/andp.19874990206.
- Fetched: https://api.crossref.org/works/10.1002/andp.19874990206 (the Wiley page returned 403).
- Quote, from Kleinert & Zaanen 2004 (https://ar5iv.arxiv.org/html/gr-qc/0307033): "The simple 1987 model had the somewhat unaesthetic feature that the crystal possessed only second-gradient elasticity to deliver the correct forces between the sources of curvature"
- Representation: a model of gravity only. Curvature sources are crystal defects. Light is not modelled. An ordinary first-gradient elastic sector is absent by construction.

**[VERIFIED — title differs from yours]** H. Kleinert & J. Zaanen, "Nematic world crystal model of gravity explaining absence of torsion in spacetime"
- Phys. Lett. A 324(5–6), 361–365 (2004); arXiv:gr-qc/0307033; DOI 10.1016/j.physleta.2004.03.048.
- The arXiv title is "World nematic crystal model of gravity explaining the absence of torsion".
- Fetched: https://api.crossref.org/works/10.1016/j.physleta.2004.03.048 ; https://www.sciencedirect.com/science/article/abs/pii/S0375960104004001 ; https://inspirehep.net/api/arxiv/gr-qc/0307033 ; https://ar5iv.arxiv.org/html/gr-qc/0307033
- Quote (abstract): "the world being a crystal which has undergone a quantum phase transition to a nematic phase by a condensation of dislocations"
- Quote (text): "Note that so far the crystal has an extra longitudinal sound wave with a different velocity than the shear waves."
- Representation:
  - Gravity is attributed to a dislocation-condensed (nematic) world crystal, and curvature sources are defects.
  - Light is not identified with shear.
  - The longitudinal mode is explicitly acknowledged. The visible text moves straight on to defects without saying how that mode is disposed of.

**[VERIFIED]** M. Danielewski, "The Planck–Kleinert Crystal"
- Z. Naturforsch. A 62(10–11), 564–568 (2007); DOI 10.1515/zna-2007-10-1102.
- Fetched: https://api.crossref.org/works/10.1515/zna-2007-10-1102 (the De Gruyter page returned 405).
- Quotes (abstract in the CrossRef record): "The transverse wave is the electromagnetic wave, and its velocity equals the velocity of light." / "The diffusing interstitial Planck particles create a gravity field, and the computed value of G is within the accuracy of experimental data."
- Note: Wikipedia's "World crystal" page mis-cites this paper as 62(1–2):56.
- Representation:
  - Light is the transverse wave of an fcc Planck-particle crystal.
  - Matter is "collective mass movement"; interstitials source gravity.
  - The longitudinal mode is not addressed in the abstract.

**[VERIFIED]** M. Danielewski & L. Sapa, "Foundations of the Quaternion Quantum Mechanics"
- Entropy 22(12), 1424 (2020); DOI 10.3390/e22121424.
- Fetched: https://www.mdpi.com/1099-4300/22/12/1424 ; full text at https://inspirehep.net/files/df79dfec93eb0b1bbd3923ac2e6cb9a8
- Quote: "The wave, i.e., the collective movement of the constituents forming the elastic Navier–Cauchy continuum, is considered equivalent to the particle."
- Longitudinal mode: present and kept. The full text gives `∂²(div u₀)/∂t² = 3c²Δ(div u₀)` versus `∂²(rot u)/∂t² = c²Δ(rot u)` for Poisson ratio 0.25, i.e. c_L = √3·c, faster than light.

**[VERIFIED — authors and title supplied]** M. Danielewski, L. Sapa, C. Roth, "Quaternion Quantum Mechanics II: Resolving the Problems of Gravity and Imaginary Numbers"
- Symmetry 15(9), 1672 (2023); DOI 10.3390/sym15091672.
- Fetched: https://www.mdpi.com/2073-8994/15/9/1672
- Quotes: "Elementary particles would have to be standing or soliton-like waves." / "Tension induced by the compression and twisting of the elastic medium would increase energy density, and as a result, generate gravity forcing and affect the wave speed."
- Representation: particles are standing or soliton waves of a Cauchy elastic vacuum. Compression enters as the origin of gravity, described through a refractive index.

**[VERIFIED]** S. Bernadotte & F. R. Klinkhamer, "Bounds on length scales of classical spacetime foam models"
- Phys. Rev. D 75, 024028 (2007); arXiv:hep-ph/0610216; DOI 10.1103/PhysRevD.75.024028.
- Fetched: https://inspirehep.net/api/arxiv/hep-ph/0610216 ; https://arxiv.org/abs/hep-ph/0610216
- Quote: "Simple models of a classical spacetime foam are considered, which consist of identical static defects embedded in Minkowski spacetime."
- Representation:
  - Light is the ordinary vacuum Maxwell field.
  - The defects are static holes in spacetime with boundary conditions. There is no elastic medium and no compressional mode.
  - Result: a modified photon dispersion, bounded by gamma-ray-burst and ultra-high-energy cosmic-ray data ("Spacetime foam models with a single length scale are excluded").

---

## 3. Supersolid or elastic-solid vacua with light = transverse phonon and matter = defects

### 3.1 Requested items

**[VERIFIED — venue confirmed]** J. Zaanen, Z. Nussinov, S. I. Mukhin, "Duality in 2+1D quantum elasticity: superconductivity and quantum nematic order"
- Ann. Phys. (N.Y.) 310(1), 181–260 (March 2004); arXiv:cond-mat/0309397; DOI 10.1016/j.aop.2003.10.003.
- Fetched: https://api.crossref.org/works/10.1016/j.aop.2003.10.003 ; https://api.semanticscholar.org/graph/v1/paper/arXiv:cond-mat/0309397 ; https://arxiv.org/abs/cond-mat/0309397 ; https://ar5iv.labs.arxiv.org/html/cond-mat/0309397
- Quotes: "The defects act like sources in electromagnetism, exerting long range forces on each other by the exchange of 'photons'" / "This theory remembers its origin in the physics of non-relativistic particles with the consequence that Lorentz invariance is badly broken" / "fluids are characterized by an isolated massless compression mode and are therefore superfluids"
- Relevance: phonons, both shear and compression (c_T ≠ c_L), are rewritten as "stress photons" in 2+1D, with defects as their sources. This is condensed-matter duality, not a vacuum model.

**[VERIFIED]** A. J. Beekman, J. Nissinen, K. Wu, K. Liu, R.-J. Slager, Z. Nussinov, V. Cvetkovic, J. Zaanen, "Dual gauge field theory of quantum liquid crystals in two dimensions"
- Phys. Rep. 683, 1–110 (2017); arXiv:1603.04254; DOI 10.1016/j.physrep.2017.03.004.
- Fetched: https://inspirehep.net/api/arxiv/1603.04254 ; https://arxiv.org/abs/1603.04254
- Quotes: "It is based on an Abelian-Higgs-type duality mapping of phonons onto gauge bosons" / "For the liquid crystal phases, the shear sector of the gauge bosons becomes massive"

**[VERIFIED]** M. Pretko & L. Radzihovsky, "Fracton-Elasticity Duality"
- Phys. Rev. Lett. 120, 195301 (2018); arXiv:1711.11044; DOI 10.1103/PhysRevLett.120.195301.
- Fetched: https://inspirehep.net/api/arxiv/1711.11044 ; https://arxiv.org/abs/1711.11044
- Quote: "The transverse and longitudinal phonons of crystals map onto the two gapless gauge modes of the gauge theory."

**[VERIFIED — found during the sweep]** M. Pretko & L. Radzihovsky, "Symmetry-Enriched Fracton Phases from Supersolid Duality"
- Phys. Rev. Lett. 121, 235301 (2018); arXiv:1808.05616; DOI 10.1103/PhysRevLett.121.235301.
- Fetched: https://inspirehep.net/api/arxiv/1808.05616 ; https://arxiv.org/abs/1808.05616
- Quote: "We thereby derive a hybrid vector-tensor gauge dual of a supersolid, which features both crystalline and superfluid order."
- Relevance: the closest peer-reviewed construction that maps a supersolid onto a gauge theory. It is condensed matter, not a vacuum model, and contains no defect-drag or Cherenkov analysis.

**[VERIFIED]** M. Levin & X.-G. Wen, "Colloquium: Photons and electrons as emergent phenomena"
- Rev. Mod. Phys. 77, 871–879 (2005); arXiv:cond-mat/0407140; DOI 10.1103/RevModPhys.77.871.
- Fetched: https://inspirehep.net/api/arxiv/cond-mat/0407140 ; https://arxiv.org/abs/cond-mat/0407140
- Quote: "photons, electrons, and other elementary particles may have a unified origin -- string-net condensation in our vacuum."
- Representation: the photon is the emergent U(1) gauge boson of a string-net liquid, not a phonon of a solid. There is no elastic longitudinal mode, and no speed or fine-tuning discussion was found in the fetched text.

### 3.2 Vacuum-as-supersolid proposals found (none peer-reviewed in a mainstream journal)

**[VERIFIED as a preprint record]** M. A. Cox (University of the Witwatersrand), "The Cosserat Supersolid: Deriving the Constants of Nature from Vacuum Lattice Mechanics"
- Zenodo preprint/monograph, three versions:
  - v2: 21 Mar 2026, DOI 10.5281/zenodo.19145609
  - v3: 13 Apr 2026, DOI 10.5281/zenodo.19535533
  - v4: 15 Jun 2026, DOI 10.5281/zenodo.20705475
- Fetched: https://zenodo.org/records/19145609 ; https://zenodo.org/records/19535533 ; https://zenodo.org/records/20705475
- Quotes (v4): "The crystal carries a transverse shear wave, which is light." / "A screw dislocation is an electron, a partial dislocation is a quark … an edge dislocation is a neutrino" / "The superfluid lets matter drift through without drag, so there is no aether wind for an interferometer to catch."
- Quote (v2): "a medium that is crystalline (rigid to shear, supporting transverse waves at c) yet simultaneously superfluid (frictionless to translation, undetectable by inertial motion)"
- Against the two tests in item 3:
  - **(i) Yes**, at preprint level: vacuum as supersolid, light as shear, matter as defects.
  - **(ii) Not found.** None of the three record descriptions mentions longitudinal or second sound, Landau velocity or Cherenkov radiation, and the record asserts zero drag. The body is unchecked: the PDF (`cosseratSupersolidv4.pdf`, 6.7 MB) came back as binary through WebFetch, and the GitHub repository is blocked by robots.txt.

**Other supersolid-vacuum items (peripheral).**
- **[VERIFIED preprint]** H. H. Chien (ed.), "Elastic Membrane Cosmology 12.3: The Supersolid Vacuum, Spacetime Phase Transitions, and the Hydrodynamic Unification of the Dark Sector," Zenodo v29 (6 Feb 2026), DOI 10.5281/zenodo.18503038.
  - Quote: "supporting transverse gravitational waves via lattice rigidity while permitting frictionless cosmic expansion via superfluidity"
  - Here the shear waves are gravitational waves, not light.
- **[VERIFIED]** M. Cavedon, "Supersolid Dark Matter and the Fabric of Spacetime," IPI Letters 3(2), O81–O85 (2025), DOI 10.59973/ipil.197. Fetched: https://ipipublishing.org/index.php/ipil/article/view/197
  - Quote: "supersolid dark matter is the fabric of spacetime - whose state of displacement gives rise to gravitational phenomena"
- **[PARTIAL — preprint only]** S. Roy & M. Roy, "Dark Matter and Supersolidity," arXiv:0801.2024 (physics.gen-ph, 2008). INSPIRE shows no journal reference.
  - Quote (with the original's typos): "we propose that the vacuum is composed of supersolid like matter which can be thgouht of as collisonalless cold dark matter"
  - The idea is not developed: there is no light, sound or defect content.

### 3.3 Modern elastic-ether revivals (light = transverse wave of a continuum)

- **[VERIFIED]** C. I. Christov, "On the nonlinear continuum mechanics of space and the notion of luminiferous medium"
  - Nonlinear Anal. TMA 71(12), e2028–e2044 (2009); arXiv:0804.4253; DOI 10.1016/j.na.2009.03.023.
  - Fetched: https://www.sciencedirect.com/science/article/abs/pii/S0362546X09004453
  - Quote: "We prove that, when linearized, the governing equations of an incompressible elastic continuum yield Maxwell's equations as corollaries."
  - This is Green's incompressible choice, revived.
- **[VERIFIED as a preprint]** K.-X. Jiang, "Isomorphic Emergence of Lorentz and Gauge Symmetries—A Constructive Interpretation Based on Continuum Mechanics," arXiv:2608.06244 (7 Aug 2026).
  - Fetched: https://arxiv.org/html/2608.06244
  - Quote: "Taking the transverse wave speed of a homogeneous, isotropic SM as the benchmark under a conventionalist synchronization scheme, Minkowski-type spacetime arises isomorphically"
  - Matter is wave packets, not defects. No longitudinal-mode treatment was found in the fetched text.
- **[NOT FOUND / not verifiable]** P. A. Millette, "Elastodynamics of the Spacetime Continuum" (STCED). Only search snippets were reachable; ResearchGate and FreeLibrary were blocked. The claimed mapping (transverse ↔ electromagnetism, longitudinal ↔ mass) is not verified.

### 3.4 Defect "relativity" in elastic media (defects move with the shear speed as their limiting speed)

- **[VERIFIED (metadata via CrossRef)]** F. C. Frank, "On the Equations of Motion of Crystal Dislocations," Proc. Phys. Soc. A 62(2), 131–134 (1949); DOI 10.1088/0370-1298/62/2/307.
- **[VERIFIED (metadata via CrossRef)]** J. D. Eshelby, "Uniformly Moving Dislocations," Proc. Phys. Soc. A 62(5), 307–314 (1949); DOI 10.1088/0370-1298/62/5/307.
  - Fetched: https://api.crossref.org/works/10.1088/0370-1298/62/2/307 ; https://api.crossref.org/works/10.1088/0370-1298/62/5/307 (the IOP pages are blocked by robots.txt).
- **[VERIFIED]** Supporting secondary source: C. J. Ruestes et al., "Probing the character of ultra-fast dislocations," Sci. Rep. 5, 16892 (2015), DOI 10.1038/srep16892.
  - Fetched: https://www.nature.com/articles/srep16892
  - Quotes: "linear elasticity theory predicts the need of an infinite energy to move at such velocity" [the shear speed] / "the Lorentz contraction of the dislocation strain field"
- Relevance: this is the standard precedent for the thesis's kinematics. In ordinary solids c_T < c_L, so shear is the slowest sound. What the thesis adds is the supersolid ordering c₂ < c_T.

### 3.5 Supersolid physics that supports the thesis's premises (cite these, not as prior art)

- **[VERIFIED (CrossRef)]** Y. Pomeau & S. Rica, "Dynamics of a model of supersolid," Phys. Rev. Lett. 72, 2426–2429 (1994); DOI 10.1103/PhysRevLett.72.2426. The CrossRef record has no abstract; the title is the quote.
- **[VERIFIED (CrossRef)]** C. Josserand, Y. Pomeau, S. Rica, "Coexistence of Ordinary Elasticity and Superfluidity in a Model of a Defect-Free Supersolid," Phys. Rev. Lett. 98, 195301 (2007); DOI 10.1103/PhysRevLett.98.195301. Title only.
- **[VERIFIED]** E. Poli, D. Baillie, F. Ferlaino, P. B. Blakie, "Excitations of a two-dimensional supersolid," Phys. Rev. A 110, 053301 (2024); arXiv:2407.01072; DOI 10.1103/PhysRevA.110.053301.
  - Fetched: https://api.crossref.org/works/10.1103/PhysRevA.110.053301 ; https://arxiv.org/abs/2407.01072 ; https://arxiv.org/html/2407.01072v1
  - Quote: "Two of these branches are related to longitudinal sound waves, similar to those in one-dimensional supersolids."
  - Quote (soft-core case): "the order of the three branches is preserved while varying Λ, with the gapless transverse branch always sandwiched in between the second sound mode and the first sound mode."
  - Quote: "the second sound or phase mode, which has a weak density contribution"
  - Relevance: this establishes the premise c₂ < c_T < c₁, with nonzero density weight in second sound, for the soft-core Gross–Pitaevskii supersolid.
- **[VERIFIED]** M. Kunimi & Y. Kato, "Mean-field and stability analyses of two-dimensional flowing soft-core bosons modeling a supersolid," Phys. Rev. B 86, 060510 (2012); arXiv:1205.2126; DOI 10.1103/PhysRevB.86.060510.
  - Quote: "we present a stability phase diagram that shows the region of the metastable superflow states for each phase."
- **[VERIFIED]** G. I. Martone & G. V. Shlyapnikov, "Drag Force and Superfluidity in the Supersolid Stripe Phase of a Spin–Orbit-Coupled Bose–Einstein Condensate," JETP 127, 865–876 (2018); arXiv:1805.12552; DOI 10.1134/S1063776118110146.
  - Fetched: https://link.springer.com/article/10.1134/S1063776118110146
  - Quote: "the Landau critical velocity vanishes if the motion is not strictly parallel to the stripes, and energy dissipation takes place at any speed"

### 3.6 Answer to item 3

**(i) Has anyone proposed the vacuum as a supersolid with light = shear and matter = defects?**
- Yes, but only in non-peer-reviewed form: Cox's 2026 Zenodo monograph.
- In peer-reviewed work, the nearest are:
  - crystal (not superfluid) vacua with light as the transverse wave: Danielewski 2007/2020/2023, Christov 2009;
  - supersolid ↔ gauge dualities in condensed matter: Pretko–Radzihovsky 2018;
  - phonons as dual "photons" with defects as their sources: Zaanen–Nussinov–Mukhin 2004, Beekman et al. 2017.

**(ii) Has anyone computed how defects couple to second sound, or the resulting Cherenkov constraint, in such a vacuum?**
- Not found.
- The nearest related work is condensed matter only: impurity drag in a stripe supersolid (Martone–Shlyapnikov) and superflow critical velocities in a soft-core supersolid (Kunimi–Kato).
- Cox explicitly claims there is no drag.

---

## 4. Elastic-ether history

**Primary secondary source: [VERIFIED (text)]** E. T. Whittaker, *A History of the Theories of Aether and Electricity from the Age of Descartes to the Close of the Nineteenth Century* (Longmans, Green, 1910), ch. V "The Aether as an Elastic Solid."
- Publisher confirmed from https://en.wikipedia.org/wiki/A_History_of_the_Theories_of_Aether_and_Electricity
- Fetched page scans: `https://en.wikisource.org/wiki/Page:A_history_of_the_theories_of_aether_and_electricity._Whittacker_E.T._(1910).pdf/NNN`, for NNN = 170, 171, 173, 174, 175, 176, 177, 179, 180, 181, 186. Page 178 came via `en.m.wikisource.org`.

### (a) Green — "longitudinal speed indefinitely great or indefinitely small"

- Printed p. 150: Green's paper was "read to the Cambridge Philosophical Society in December, 1837." The footnote reads "Trans. Camb. Phil. Soc., 1838; Green's Math. Papers, p. 245."
- Printed p. 153: "Green avoided this difficulty by adopting Fresnel's suggestion that the resistance of the aether to compression may be very large in comparison with the resistance to distortion"
- Printed p. 158: "a remark of Green's, that the longitudinal wave might be avoided in either of two ways—namely, by supposing its velocity to be indefinitely great or indefinitely small."
- Printed p. 158 (continued): "Green curtly dismissed the latter alternative and adopted the former, on the ground that the equilibrium of the medium would be unstable if its compressibility were negative"
- **Metadata [PARTIAL]:** G. Green, "On the laws of the reflexion and refraction of light at the common surface of two non-crystallized media," Trans. Camb. Phil. Soc. 7, 1–24.
  - Vol. 7, pp. 1–24 (1838) comes from the reference list of A. J. M. Spencer, J. Eng. Math. 95, 5 (2015), DOI 10.1007/s10665-015-9791-0 (fetched https://link.springer.com/article/10.1007/s10665-015-9791-0).
  - "Read 11 Dec 1837" comes from Darrigol 2010 (below).
  - Your "published 1842" date was **not** confirmed by any fetched page.

### (b) Cauchy's third (contractile/labile) ether, and Kelvin's revival

- Printed p. 158: "Cauchy, without attempting to meet Green's objection, took up the study of a medium …"
- Printed p. 158: "It is generally known as the contractile or labile aether"
- Cauchy footnote, p. 158: "Comptes Rendus, ix, p. 676 (25 Nov., 1839), and p. 726 (2 Dec., 1839)."
- Printed p. 159: "It may be defined as an elastic medium of (negative) compressibility such as to make the velocity of the longitudinal wave zero"
- Printed p. 159: "Cauchy, as we have seen, did not attempt to refute Green's objection that such a medium would be unstable"
- Printed p. 159: "Thomson (Lord Kelvin), who discussed it long afterwards." Footnote: "Phil. Mag. xxvi (1888), p. 414."
- Kelvin's stability reply, p. 159: "the equilibrium must be stable, provided the medium either extends through boundless space or has a fixed containing vessel as its boundary." The condition stated just before it is that both wave speeds are real.
- Printed p. 160: "This condition is in any case necessary for stability, as was shown by R. T. Glazebrook: cf. Thomson, Phil. Mag. xxvi, p. 500."
- Printed p. 161: "Thomson assumed that in space void of ponderable matter the aether is practically incompressible by the forces concerned in light-waves"
- **[VERIFIED]** W. Thomson, "On the reflexion and refraction of light," Phil. Mag. 26, 414–425 and 500–501 (1888). Sources: the Whittaker footnote, plus the Darrigol 2010 reference list.

### (c) MacCullagh, the torque objection, Kelvin's gyrostats, FitzGerald

- Printed p. 154: "He had, in fact, concluded from Green's results that it was impossible to explain optical phenomena satisfactorily by comparing the aether to an elastic solid of the ordinary type". Footnote: "Trans. Roy. Irish Acad. xxi.: MacCullagh's Coll. Works, p. 145."
- Printed p. 155: "For MacCullagh's new medium, on the other hand, the potential energy depends only on the rotation of the volume-elements."
- Printed p. 155: "we shall suppose this to be the case, so that no longitudinal waves exist at any time in the medium". The "case" is that div e is initially zero, and therefore always zero.
  - Note for the paper: in MacCullagh's medium the longitudinal sector has zero restoring force. It is excluded by initial conditions, not given a large speed.
- Printed p. 156, footnote (the mapping FitzGerald later exploited): "e corresponds to the magnetic force, μ curl e to the electric force, and curl e to the electric displacement"
- Printed p. 157, Kelvin's gyrostatic model: "a bar thus equipped will require a couple to hold it at rest in any position inclined to its original position"
- Printed p. 157: "the structure as a whole will possess that kind of quasi-elasticity which was first imagined by MacCullagh."
- Printed p. 157, footnotes: "Comptes Rendus, Sept. 16, 1889: Kelvin's Math. and Phys. Papers, iii, p. 466." and "Proc. Roy. Soc. Edinb., Mar. 17, 1890: Kelvin's Math. and Phys. Papers, iii, p. 468."
  - So the gyrostatic aether was first announced in 1889 (Comptes Rendus); the Proceedings of the Royal Society of Edinburgh paper is 1890.
- Printed p. 157: "The hesitation which was felt in accepting the rotationally elastic aether arose mainly from the want of any readily conceived example of a body endowed with such a property."
- Printed p. 157: "can scarcely be said to have been properly appreciated until FitzGerald drew attention to it forty years afterwards."

**Stokes's torque objection.** This was not in the Whittaker pages I fetched (pp. 154–157).
- **[VERIFIED]** D. F. Moyer, "MacCullagh, James," Complete Dictionary of Scientific Biography. Fetched: https://www.encyclopedia.com/science/dictionaries-thesauruses-pictures-and-press-releases/maccullagh-james
  - Quote: "Stokes in 1862 led the way in preferring Green's linear displacement potential to MacCullagh's rotational potential, since the latter involved unbalanced couples."
- **[PARTIAL]** Talk slides at https://www.maths.tcd.ie/~hmi/events/MacCullagh_talk.pdf (authorship unclear) quote Stokes: "[MacCullagh's ether] leads to consequences absolutely at variance with dynamical principles."
- **[PARTIAL]** Stokes, "Report on double refraction," Rep. Brit. Assoc. (1862). The Darrigol reference list as extracted reads "353-282", evidently a typo for 253–282; that page range is unconfirmed.

**MacCullagh metadata [PARTIAL].** J. MacCullagh, "An essay towards a dynamical theory of crystalline reflexion and refraction," Trans. R. Irish Acad. 21, 17–50, read 9 Dec 1839.
- Volume and pages come from the Darrigol 2010 reference list; Whittaker gives "xxi".
- The year 1848 is **not** confirmed: the extracted Darrigol entry printed "1885", apparently an extraction error.

**FitzGerald [VERIFIED].** G. F. FitzGerald, "On the electromagnetic theory of the reflection and refraction of light," Phil. Trans. R. Soc. Lond. 171, 691–711 (1880); DOI 10.1098/rstl.1880.0019.
- Fetched: https://api.crossref.org/works/10.1098/rstl.1880.0019
- Quote (Dictionary of Scientific Biography): "In 1880 FitzGerald showed (in 'On the Electromagnetic Theory of Reflection and Refraction of Light') that MacCullagh's formulation could be translated into an electromagnetic one"
- MacTutor says the paper was sent to the Royal Society in October 1878.

**Other secondary sources.**
- **[VERIFIED]** K. F. Schaffner, *Nineteenth-Century Aether Theories* (Pergamon, 1972), ISBN 978-0-08-015674-3. Fetched: https://www.sciencedirect.com/book/monograph/9780080156743/nineteenth-century-aether-theories
  - Quote: "the elastic solid aether. Concerns include Green's aether theory, MacCullagh's aether theory, and Kelvin's aether theory."
- **[VERIFIED]** O. Darrigol, "James MacCullagh's ether: An optical route to Maxwell's equations?," Eur. Phys. J. H 35, 133–172 (2010); DOI 10.1140/epjh/e2010-00009-3. Fetched: https://link.springer.com/article/10.1140/epjh/e2010-00009-3
  - Quote: "By renouncing mechanical modeling in favor of a more abstract dynamical method, he unveiled the structure which optics came to share with Maxwell's electrodynamics."

---

## 5. Is the thesis already published? Candidate statements

- **[VERIFIED]** S. Liberati, M. Visser, S. Weinfurtner, "Naturalness in an emergent analogue spacetime," Phys. Rev. Lett. 96, 151301 (2006); arXiv:gr-qc/0512139; DOI 10.1103/PhysRevLett.96.151301.
  - INSPIRE also lists a variant title, "Naturalness in emergent spacetime".
  - Fetched: https://inspirehep.net/api/arxiv/gr-qc/0512139 ; https://ar5iv.arxiv.org/html/gr-qc/0512139 ; https://arxiv.org/abs/gr-qc/0512139
  - Quotes: "our model explicitly avoids the 'naturalness problem', and makes specific suggestions regarding how to construct a physically reasonable quantum gravity phenomenology" / text: "They both 'experience' the same space-time if the sound speeds are equal,"
- **[VERIFIED]** S. Liberati, M. Visser, S. Weinfurtner, "Analogue quantum gravity phenomenology from a two-component Bose–Einstein condensate," Class. Quantum Grav. 23, 3129–3154 (2006); arXiv:gr-qc/0510125; DOI 10.1088/0264-9381/23/9/023.
  - Quotes: "This system can be tuned to have two 'phonon' modes (one massive, one massless) which share the same limiting speed in the hydrodynamic approximation" / "We investigate the physical interpretation of the relevant fine-tuning conditions"
- **[VERIFIED]** M. Visser & S. Weinfurtner, "Massive Klein-Gordon equation from a BEC-based analogue spacetime," Phys. Rev. D 72, 044020 (2005); arXiv:gr-qc/0506029; DOI 10.1103/PhysRevD.72.044020.
  - Quotes: "Once decoupled, the two distinct phonons generically couple to distinct effective spacetimes, representing a bi-metric model, with one of the modes acquiring a mass." / "it is possible to tune the system so that both modes can be arranged to travel at the same speed"
- **[VERIFIED]** C. Barceló, S. Liberati, M. Visser, "Refringence, field theory, and normal modes," Class. Quantum Grav. 19, 2961–2982 (2002); arXiv:gr-qc/0111059; DOI 10.1088/0264-9381/19/11/314.
  - Quotes: "more complicated situations lead to bi-metric and multi-metric theories" / "either by enforcing a unique effective metric or at the worst by arranging things so that there are multiple metrics that are all 'close' to each other"
- **[VERIFIED]** M. Visser, C. Barceló, S. Liberati, "Bi-refringence versus bi-metricity," in *Inquiring the Universe* (Frontier Group, 2003), pp. 397–429; arXiv:gr-qc/0204017. Metadata from INSPIRE.
  - Quote: "bi-metricity (where the two photon polarizations ``see'' two distinct metrics)."
- **[VERIFIED]** C. Barceló, S. Liberati, M. Visser, "Analogue Gravity," Living Rev. Relativ. 14, 3 (2011); DOI 10.12942/lrr-2011-3. Fetched: https://link.springer.com/article/10.12942/lrr-2011-3
  - Quote (§2.7.3, reporting Comer): "in superfluids there will be multiple acoustic metrics — and multiple acoustic horizons — corresponding to first and second sound."
  - The 2026 update, Living Rev. Relativ. 29, 2 (2026), was fetched only up to §2.11; nothing relevant appeared in that part.
- **[VERIFIED]** J. Collins, A. Perez, D. Sudarsky, L. Urrutia, H. Vucetich, "Lorentz invariance and quantum gravity: an additional fine-tuning problem?," Phys. Rev. Lett. 93, 191301 (2004); arXiv:gr-qc/0403053; DOI 10.1103/PhysRevLett.93.191301.
  - Quote: "gives rise to Lorentz violation at the percent level, some 20 orders of magnitude higher than earlier estimates, unless the bare parameters of the theory are unnaturally strongly fine-tuned."
- **[VERIFIED]** S. Chadha & H. B. Nielsen, "Lorentz invariance as a low energy phenomenon," Nucl. Phys. B 217, 125–144 (1983); DOI 10.1016/0550-3213(83)90081-0.
  - Fetched: https://api.crossref.org/works/10.1016/0550-3213(83)90081-0 ; https://inspirehep.net/api/doi/10.1016/0550-3213(83)90081-0
  - Quote: "this model simulates Lorentz invariance better and better as the energy scale is progressively lowered."
  - This is the counter-position (Lorentz invariance as an IR attractor).
- **[VERIFIED — found during the sweep]** M. M. Anber & J. F. Donoghue, "The emergence of a universal limiting speed," Phys. Rev. D 83, 105027 (2011); arXiv:1102.0789; DOI 10.1103/PhysRevD.83.105027.
  - Quotes: "we might expect that particles would display different limiting speeds" / "The differences normally vanish only logarithmically, so that an exponentially large energy trajectory is required" / "For c_e > c, energetic electrons traveling faster than the speed of light will radiate Cherenkov light"
- **[VERIFIED]** S. Coleman & S. L. Glashow, "Cosmic ray and neutrino tests of special relativity," Phys. Lett. B 405, 249–252 (1997); arXiv:hep-ph/9703240; DOI 10.1016/S0370-2693(97)00638-2.
  - Quotes: "If the maximum attainable speed of a particle depends on its identity, then neutrinos may exhibit flavor oscillations." / "A charged particle traveling faster than light loses energy rapidly via vacuum Čerenkov radiation."
- **[VERIFIED]** S. Coleman & S. L. Glashow, "High-energy tests of Lorentz invariance," Phys. Rev. D 59, 116008 (1999); arXiv:hep-ph/9812418; DOI 10.1103/PhysRevD.59.116008.
  - Quote: "They define the energy-momentum eigenstates and their maximal attainable velocities in the high-energy limit."
- **[VERIFIED]** G. D. Moore & A. E. Nelson, "Lower bound on the propagation speed of gravity from gravitational Cherenkov radiation," JHEP 09 (2001) 023; arXiv:hep-ph/0106220; DOI 10.1088/1126-6708/2001/09/023.
  - Quote: "We show that the case c_g < c is very tightly constrained by the observation of the highest energy cosmic rays."
- **[VERIFIED]** J. W. Elliott, G. D. Moore, H. Stoica, "Constraining the new aether: gravitational Cherenkov radiation," JHEP 08 (2005) 066; arXiv:hep-ph/0505211; DOI 10.1088/1126-6708/2005/08/066.
  - Quote: "the observation of ultra-high energy cosmic rays (which implies the absence of energy loss via various Cherenkov type processes) places constraints on the parameters of this theory"
- **[PARTIAL]** Volovik on species-dependent "speeds of light". No explicit passage was located. The closest verified statements are:
  - Phys. Rep. 351 (ar5iv): "the speed of 'light' c(n) – depends on the physics of the higher energy hierarchy rank" / "it is quite possible that even such symmetries as Lorentz symmetry and gauge invariance are not fundamental, but gradually appear"
  - JETP Lett. 73 (2001): "accompanied by the redistribution of the momentum-space topological charges between the fermionic flavors"
  - G. E. Volovik, "Emergent physics: Fermi point scenario," Phil. Trans. R. Soc. A 366, 2935 (2008), arXiv:0801.0724. Metadata from Anber–Donoghue ref. [10]; text via ar5iv. Quote: "the relative value of the Lorentz violating terms in Maxwell equation is smaller than 10^{-18}"

**Supersolid or crystal analogue spacetimes with second sound / two longitudinal modes / bimetricity.**
- Superfluid case: published. First and second sound give multiple acoustic metrics (Comer, via the Living Review).
- Two-mode BEC case: published. Generically bi-metric; equal speeds require tuning (Visser–Weinfurtner 2005; Liberati–Visser–Weinfurtner 2006).
- Crystal case: the extra longitudinal sound is noted (Kleinert–Zaanen 2004).
- Supersolid analogue-spacetime paper treating the second-sound/shear bimetricity: **none found**.

**Judgement.**
- **The general statement is published.** Different excitations of an emergent medium have different limiting speeds; matter faster than a slower mode it couples to radiates; a common cone needs tuning or a long RG flow. The best citations are Collins et al. 2004, Barceló–Liberati–Visser 2002, Visser–Weinfurtner 2005, Liberati–Visser–Weinfurtner 2006, Anber–Donoghue 2011, Coleman–Glashow 1997, Moore–Nelson 2001 and Elliott–Moore–Stoica 2005, with Chadha–Nielsen 1983 as the counterpoint.
- **The specific supersolid computation is not published (not found).** That is: light = shear speed; cores coupling to density hence to both longitudinal branches; c₂ < c_T with nonzero density weight; Landau–Cherenkov drag setting the matter speed limit.
  - The closest overlap is Cox's 2026 Zenodo monograph, which asserts the opposite (no drag) and whose body is unverified.
  - The condensed-matter premise (c₂ < c_T < c₁ in soft-core supersolids) is published by Poli et al. 2024.
- **Historical framing.** Green's dilemma (longitudinal speed indefinitely great or indefinitely small) is the classical precursor. The thesis amounts to the observation that in a supersolid the extra longitudinal branch cannot be pushed out of the way. Second sound is generically slower than shear, as in the soft-core case, and carries density weight.

---

## 6. Metadata corrections and notes against your list

1. **Kleinert & Zaanen.** The published title is "Nematic world crystal model of gravity explaining absence of torsion in spacetime" (CrossRef and ScienceDirect), not "World nematic …". The arXiv title is "World nematic crystal model of gravity explaining the absence of torsion". Pages 361–365.
2. **Danielewski 2007.** Issue 10–11, pp. 564–568, DOI 10.1515/zna-2007-10-1102. Your citation is correct; Wikipedia's 62(1–2):56 is wrong.
3. **Danielewski & Sapa 2020.** Title: "Foundations of the Quaternion Quantum Mechanics".
4. **Danielewski et al. 2023.** Authors: Danielewski, Sapa, Roth. Title: "Quaternion Quantum Mechanics II: Resolving the Problems of Gravity and Imaginary Numbers". Symmetry 15(9), 1672.
5. **Zaanen–Nussinov–Mukhin.** The venue is confirmed as Ann. Phys. (N.Y.) 310(1), 181–260 (2004), DOI 10.1016/j.aop.2003.10.003.
6. **Page ranges.**
   - Volovik, Phys. Rep. 351: 195–348.
   - Chadha–Nielsen: 125–144.
   - Sbitnev: 606–619.
   - Zloshchastiev: Grav. Cosmol. 288–297; Acta Phys. Polon. B 261–292.
   - Beekman et al.: 1–110.
   - Levin–Wen: 871–879.
   - FitzGerald: 691–711.
   - Kelvin 1888: 414–425 and 500–501.
7. **Kelvin's gyrostatic aether.** First announced in Comptes Rendus, 16 Sept 1889; the Proc. R. Soc. Edinb. paper is 17 Mar 1890 (Math. Phys. Papers iii, 466–472).
8. **MacCullagh.** Trans. R. Irish Acad. 21, 17–50, read 9 Dec 1839. Your year 1848 is unconfirmed.
9. **Green.** Trans. Camb. Phil. Soc. 7, 1–24, read 11 Dec 1837, dated "1838" by Whittaker and Spencer. Your "published 1842" is unconfirmed.
10. **Green's alternatives.** Whittaker's wording is "indefinitely great or indefinitely small". On p. 153 he also says that Green adopted Fresnel's suggestion of very large resistance to compression, not strict incompressibility.
11. **Stokes's objection.** The Dictionary of Scientific Biography phrases it as MacCullagh's potential "involved unbalanced couples". The original is Stokes's 1862 British Association "Report on double refraction"; its pages are unconfirmed.

## 7. Not verified / open

- The body of Cox's *Cosserat Supersolid* PDF (v4, `cosseratSupersolidv4.pdf`, 6.7 MB). Check by hand for any treatment of second sound or longitudinal sound, Landau velocity or Cherenkov radiation before claiming novelty.
- An explicit Volovik passage on species-dependent light cones.
- Millette's STCED claims.
- Comer's original first/second-sound paper (only the Living Review's report of it was fetched).
- The page range of Stokes's 1862 report.
- The 1842 date (Green) and the 1848 date (MacCullagh).
