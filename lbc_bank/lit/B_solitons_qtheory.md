# B — Solitons, emergent light cones, and prior-address map (citation-verified sweep)

Sweep date: 2026-10-03. Scope: Part 1 (12 items to verify and summarise), Part 2 (a)–(d), the prior-address map for the program's "survivors".

## Method and limits (read first)

- Direct `curl` to arxiv.org, export.arxiv.org, inspirehep.net, crossref, APS, Springer and similar hosts is **blocked by the egress policy** in this session. Everything here was fetched with WebFetch from these sources: INSPIRE record JSON (`inspirehep.net/api/arxiv/<id>` or `/api/doi/<doi>`) for metadata; arXiv abstract pages; ar5iv HTML full text (`ar5iv.labs.arxiv.org/html/<id>`); and publisher landing pages (ScienceDirect, nature.com, Springer, cambridge.org, OUP, mdpi.com, zenodo.org) where they loaded.
- WebFetch returns text through a small model with a quote cap of about 125 characters. Quotes below are **as the tool rendered them**. Math symbols may be transliterated, for example `Q₁` or `e_i^k`. Each quote is at most 30 words. When the tool inserted an ellipsis or paraphrased, I left the quote out.
- ar5iv pages are often **truncated** for long papers. When a statement was not found, that only means it was not found in the part the tool returned. It does not prove the statement is absent.
- Tags: **VERIFIED** means the page was fetched and all metadata matched. **PARTIAL** means the metadata was verified but the claimed content was only partly supported, or a secondary source or metadata-only source was used. **NOT FOUND / NOT FETCHED** is self-explanatory.
- Pages that could not be read: `zenodo.org/records/21046966` (HTTP 429; the proxy said not to retry), `researchgate.net/publication/402541387` (HTTP 429), `royalsocietypublishing.org` (403), `journals.aps.org` (403), `pnas.org` (403), `pubmed` (captcha), `europepmc` and `export.arxiv.org/api` (blocked by robots.txt).

---

# PART 1 — verification and content

### 1. Barceló, Liberati, Visser — "Analogue gravity" (Living Rev. Relativ. 14, 3, 2011)

[VERIFIED] C. Barceló, S. Liberati, M. Visser, "Analogue Gravity," Living Rev. Relativ. **14**, 3 (2011); arXiv:gr-qc/0505065 (v3 = 2011 update); DOI 10.12942/lrr-2011-3. The 2005 original is Living Rev. Relativ. 8, 12 (2005), DOI 10.12942/lrr-2005-12. Note: the arXiv journal-ref field still shows the 2005 version, while INSPIRE lists both.
Fetched: https://link.springer.com/article/10.12942/lrr-2011-3 ; https://inspirehep.net/api/arxiv/gr-qc/0505065 ; https://arxiv.org/abs/gr-qc/0505065 ; https://arxiv.org/pdf/gr-qc/0505065v3 ; https://ar5iv.labs.arxiv.org/html/gr-qc/0505065

- Multiple metrics: "in superfluids there will be multiple acoustic metrics – and multiple acoustic horizons – corresponding to first and second sound" (early section; from the v3 PDF).
- Multiple metrics: "In simple physical situations the causal structure resembles that of the acoustic metric, though in more general situations one might encounter bi-refringence or even multi-refringence." (ar5iv)
- Table of contents (ar5iv) includes the subsections "Possible Lorentz violations" and "Multiple effective metrics and multi-refringence".
- **Low-energy-only Lorentz invariance: PARTIAL.** The relevant later sections (BEC, Lorentz violation) were truncated in every rendering I could fetch, so I could not quote the review itself on this. The same authors state it explicitly elsewhere:
  - [VERIFIED] C. Barceló, S. Liberati, M. Visser, "Analog gravity from Bose-Einstein condensates," Class. Quantum Grav. **18**, 1137–1152 (2001); arXiv:gr-qc/0011026; DOI 10.1088/0264-9381/18/6/312. Fetched: https://inspirehep.net/api/arxiv/gr-qc/0011026. Quotes: "At low momenta linearized excitations of the phase of the condensate wavefunction obey a (3+1)-dimensional d'Alembertian equation coupling to a (3+1)-dimensional Lorentzian-signature 'effective metric'" and "recover non-relativistic Newtonian physics at high momenta".
  - See also item 2 (Liberati–Visser–Weinfurtner, CQG 2006, Introduction).

Relevance: the canonical review. In analogue systems the light cone is an IR (hydrodynamic) property, and systems with several mode types generically produce several metrics.

### 2. Liberati, Visser, Weinfurtner — two-component BEC

[VERIFIED] S. Liberati, M. Visser, S. Weinfurtner, "Naturalness in emergent spacetime," Phys. Rev. Lett. **96**, 151301 (2006); arXiv:gr-qc/0512139; DOI 10.1103/PhysRevLett.96.151301. Fetched: https://inspirehep.net/api/arxiv/gr-qc/0512139
- "we consider the class of two-component BECs subject to laser-induced transitions"
- "this is the essence of the naturalness problem"
- "ensuring that small Lorentz violations remain small"

[VERIFIED] S. Liberati, M. Visser, S. Weinfurtner, "Analogue quantum gravity phenomenology from a two-component Bose-Einstein condensate," Class. Quantum Grav. **23**, 3129–3154 (2006); arXiv:gr-qc/0510125; DOI 10.1088/0264-9381/23/9/023. Fetched: https://inspirehep.net/api/arxiv/gr-qc/0510125 ; https://ar5iv.labs.arxiv.org/html/gr-qc/0510125
- Abstract: "two phonon modes (one massive, one massless) which share the same limiting speed"
- Abstract: "investigate the physical interpretation of the relevant fine-tuning conditions"
- §1: "We study the conditions required for these two phonon modes to share the same 'special relativity' metric in the hydrodynamic limit"
- §1, on earlier models: "no mono-metricity"
- §1: "provides a simple and explicit example of the high-energy breakdown of 'Lorentz invariance' which interpolates between a low-energy 'massless' relativistic regime"

Claim status for "mono-metricity requires tuning": **supported at abstract and introduction level.** The explicit tuning conditions (Section 4) fell in the truncated part of the page and were not quoted.

Relevance: the standard counterexample to a "free" shared light cone. With two components, one metric needs parameter conditions.

### 3. Volovik — Fermi-point scenario

[VERIFIED] G. E. Volovik, *The Universe in a Helium Droplet* (Oxford University Press, 2003), International Series of Monographs on Physics (vol. 117 per retailer listing; the OUP page does not show the number); ISBN 9780198507826; published 15 May 2003. Fetched: https://global.oup.com/academic/product/the-universe-in-a-helium-droplet-9780198507826. The page has a general description only, so no content quote was available.

[VERIFIED] G. E. Volovik, "Emergent physics: Fermi point scenario," Phil. Trans. R. Soc. A **366**, 2935–2951 (2008); arXiv:0801.0724; DOI 10.1098/rsta.2008.0070. **This is the correct paper-length statement.** Fetched: https://inspirehep.net/api/arxiv/0801.0724 ; https://ar5iv.labs.arxiv.org/html/0801.0724
- Abstract: "Fermi point is the topologically stable hedgehog in momentum space."
- Abstract: "emergent fermionic matter consists of massless Weyl fermions"
- Gauge fields, §2.2: "The vector field p_β^(0) in the expansion plays the role of the effective U(1) gauge field A_β acting on fermions."
- Gravity, §2.3: "The matrix field e_i^k acts on the quasiparticles as the field of vierbein, and thus describes the emergent dynamical gravity field."
- Species-sharing: not addressed in the fetched text.

[VERIFIED, different paper] G. E. Volovik, "Fermi-point scenario of emergent gravity," PoS (QG-Ph) 043 (2007); arXiv:0709.1258; no DOI listed. Fetched: https://inspirehep.net/api/arxiv/0709.1258 ; https://ar5iv.labs.arxiv.org/html/0709.1258
- "gravity is an emergent low-energy phenomenon arising from a topologically stable defect in momentum space -- the Fermi point"

**Species share one "speed of light" only through a symmetry.** This is the clearest statement found:
[VERIFIED] G. E. Volovik, "Reentrant violation of special relativity in the low-energy corner," JETP Lett. **73**, 162–165 (2001) [Pisma ZhETF 73, 182]; arXiv:hep-ph/0101286; DOI 10.1134/1.1368706. Fetched: https://inspirehep.net/api/arxiv/hep-ph/0101286 ; https://ar5iv.arxiv.org/html/hep-ph/0101286
- "all of them have the same 'speed of light' (i.e. the same maximum attainable speed)". The tool reported that this holds as a result of a "symmetry, which connects all the low-energy fermionic species".
- "the discrete symmetry between the fermions together with the momentum-space topology guarantee that massless fermions obey the special relativity"
- "the energy region, where the special relativity holds, can be sandwiched from both the high and low energies sides by domains where the special relativity is violated"

Related, not requested:
[VERIFIED] M. M. Anber, J. F. Donoghue, "The emergence of a universal limiting speed," Phys. Rev. D **83**, 105027 (2011); arXiv:1102.0789; DOI 10.1103/PhysRevD.83.105027. Fetched: https://inspirehep.net/api/arxiv/1102.0789
- "fields with different limiting velocities (the 'speed of light') at a high energy scale can nevertheless have a common limiting velocity at low energies due to the effects of interactions"
- "The differences normally vanish only logarithmically, so that an exponentially large energy trajectory is required in order to satisfy experimental constraints."

Relevance: in Volovik's scenario a shared light cone is not automatic. It needs a symmetry linking the species, or RG convergence (Anber–Donoghue), which is slow (logarithmic).

### 4. Klinkhamer & Volovik — vacuum variable q

[VERIFIED] F. R. Klinkhamer, G. E. Volovik, "Self-tuning vacuum variable and cosmological constant," Phys. Rev. D **77**, 085015 (2008); arXiv:0711.3170; DOI 10.1103/PhysRevD.77.085015. Fetched: https://inspirehep.net/api/arxiv/0711.3170 ; https://ar5iv.labs.arxiv.org/html/0711.3170
- Abstract (INSPIRE): "A spacetime independent variable is introduced which characterizes the Lorentz-invariant self-sustained quantum vacuum. The self-tuning of this variable nullifies the effective energy density of the perfect quantum vacuum."
- §II.1: "The most important property of the quantum vacuum is its Lorentz invariance."
- §II.1: "Having a zero value (or almost zero value) of the relevant vacuum energy density can be the property of a self-sustained medium"
- §II.2: "Under external pressure P, the relevant thermodynamic potential (Gibbs free energy) at zero temperature is given by"
- §II.2: "The Gibbs–Duhem equation in its simplest form, N dμ=V dP-S dT, relates an infinitesimal change dμ in the chemical potential"
- Eq. (10), equilibrium of the self-sustained vacuum with zero external pressure: "P=-ϵ(Ψ₀,q)+q·dϵ(Ψ₀,q)/dq=0"

[VERIFIED] F. R. Klinkhamer, G. E. Volovik, "Dynamic vacuum variable and equilibrium approach in cosmology," Phys. Rev. D **78**, 063528 (2008); arXiv:0806.2805; DOI 10.1103/PhysRevD.78.063528. Fetched: https://inspirehep.net/api/arxiv/0806.2805 ; https://ar5iv.labs.arxiv.org/html/0806.2805
- Introduction: "the effective cosmological constant Λ of a perfect quantum vacuum is strictly zero, which is consistent with the requirement of Lorentz invariance"
- Introduction: "the effective (coarse-grained) vacuum energy density is automatically nullified (without fine tuning) by the spontaneous adjustment"
- §II: "the effective vacuum energy density ε̃_vac(q)≡ε−q dε/dq, and it is this energy density that contributes to the effective gravitational field equations"

**PARTIAL on the exact wording "p = −ε, T_μν ∝ g_μν".** I did not get a verbatim sentence with that form in the fetched text. What is verified is the Gibbs–Duhem form P = −(ε − q dε/dq) = −ε̃. In equilibrium with no external pressure this gives P = 0, so ε̃ = 0 (self-tuning), together with the statement that the result is "consistent with the requirement of Lorentz invariance".

### 5. Coleman & Glashow — maximal attainable velocities

[VERIFIED] S. Coleman, S. L. Glashow, "Cosmic ray and neutrino tests of special relativity," Phys. Lett. B **405**, 249–252 (1997); arXiv:hep-ph/9703240; DOI 10.1016/S0370-2693(97)00638-2. Fetched: https://inspirehep.net/api/arxiv/hep-ph/9703240 ; https://ar5iv.labs.arxiv.org/html/hep-ph/9703240
- "if the maximum attainable speed of a particle depends on its identity, then neutrinos, even if massless, may exhibit flavor oscillations."
- "A charged particle traveling faster than light loses energy rapidly via vacuum Čerenkov radiation."
- "The threshold energy for p→p+γ is E₀'=M/√(1-c²), with M the particle mass."

[VERIFIED] S. Coleman, S. L. Glashow, "High-energy tests of Lorentz invariance," Phys. Rev. D **59**, 116008 (1999); arXiv:hep-ph/9812418; DOI 10.1103/PhysRevD.59.116008. Fetched: https://inspirehep.net/api/arxiv/hep-ph/9812418
- "They define the energy-momentum eigenstates and their maximal attainable velocities in the high-energy limit."

Relevance: the observational penalty for species whose light cones differ.

### 6. Skyrme

[VERIFIED — metadata only] T. H. R. Skyrme, "A non-linear field theory," Proc. R. Soc. Lond. A **260**, 127–138 (1961); DOI 10.1098/rspa.1961.0018. Fetched: https://inspirehep.net/api/doi/10.1098/rspa.1961.0018 ; https://api.semanticscholar.org/graph/v1/paper/DOI:10.1098/rspa.1961.0018 (the abstract is elided there; the publisher page returned 403). No quote available.

[VERIFIED] T. H. R. Skyrme, "A unified field theory of mesons and baryons," Nucl. Phys. **31**, 556–569 (1962); DOI 10.1016/0029-5582(62)90775-7. Fetched: https://www.sciencedirect.com/science/article/pii/0029558262907757 ; https://inspirehep.net/api/doi/10.1016/0029-5582(62)90775-7
- "The way in which a non-linear meson field theory of this type may contain its own sources, and how these may be idealised to point singularities"

### 7. Adkins–Nappi–Witten; Witten

[VERIFIED] G. S. Adkins, C. R. Nappi, E. Witten, "Static properties of nucleons in the Skyrme model," Nucl. Phys. B **228**, 552–566 (1983); DOI 10.1016/0550-3213(83)90559-X. Fetched: https://www.sciencedirect.com/science/article/pii/055032138390559X
- "We compute static properties of baryons in an SU(2) × SU(2) chiral theory (the Skyrme model)"
- "whose solitons can be interpreted as the baryons of QCD"
- "Our results are generally within about 30% of experimental values."

[VERIFIED metadata; PARTIAL for "baryon number = winding"] E. Witten, "Current algebra, baryons, and quark confinement," Nucl. Phys. B **223**, 433–444 (1983); DOI 10.1016/0550-3213(83)90064-0. Fetched: https://www.sciencedirect.com/science/article/pii/0550321383900640
- "It is shown that ordinary baryons can be understood as solitons in current algebra effective lagrangians."
- The winding-number identification is not in the abstract. Companion paper: Witten, "Global aspects of current algebra," Nucl. Phys. B 223, 422–432 (1983), DOI 10.1016/0550-3213(83)90063-9 (verified, fetched https://www.sciencedirect.com/science/article/pii/0550321383900639; its abstract covers the Wess–Zumino quantization law).
- Secondary statement, from unofficial student notes of N. S. Manton & D. Stuart's Cambridge Part III course, Easter 2017, notes by D. Chua (https://dec41.user.srcf.net/notes/III_E/classical_and_quantum_solitons.pdf): "This topological charge is then identified with what is known, physically, as the baryon number. This baryon number is conserved for topological reasons."
- Goldstone & Wilczek, PRL 47, 986 (1981), DOI 10.1103/PhysRevLett.47.986: metadata verified, but the abstract does not state the winding identification, so it is not usable for this claim.

### 8. Faddeev & Niemi

[VERIFIED] L. Faddeev, A. J. Niemi, "Stable knot-like structures in classical field theory," Nature **387**, 58–61 (1997); DOI 10.1038/387058a0; arXiv:hep-th/9610193 (the arXiv/INSPIRE title is **"Knots and particles"**). Fetched: https://www.nature.com/articles/387058a0 ; https://inspirehep.net/api/arxiv/hep-th/9610193
- "we have found indications that knotlike structures appear as stable finite energy solitons in a realistic 3+1 dimensional model." (arXiv abstract)
- "We have explicitly simulated the unknot and trefoil configurations, and our results suggest that all torus knots appear as solitons."

### 9. Battye & Sutcliffe

[VERIFIED] R. A. Battye, P. M. Sutcliffe, "Knots as stable soliton solutions in a three-dimensional classical field theory," Phys. Rev. Lett. **81**, 4798–4801 (1998); arXiv:hep-th/9808129; DOI 10.1103/PhysRevLett.81.4798. Fetched: https://inspirehep.net/api/arxiv/hep-th/9808129
- "For charges between one and eight, we find solutions which exhibit a rich and spectacular variety of phenomena, including stable toroidal solitons with twists, linked loops and also knots."

[VERIFIED] R. A. Battye, P. M. Sutcliffe, "Solitons, links and knots," Proc. R. Soc. Lond. A **455**, 4305–4331 (1999); arXiv:hep-th/9811077; DOI 10.1098/rspa.1999.0502. Fetched: https://inspirehep.net/api/arxiv/hep-th/9811077 ; https://ar5iv.labs.arxiv.org/html/hep-th/9811077
- **Whitehead / linking statement (§2):** "if a field has Hopf number Q then the two loops consisting of the preimages of any two distinct points on the target S² will be linked exactly Q times."
- §2: "the position of the soliton is the curve in space described by the preimage of the vector (0,0,-1)."

Original source: J. H. C. Whitehead, "An expression of Hopf's invariant as an integral," Proc. Natl. Acad. Sci. USA 33, 117–123 (1947). **[PARTIAL]**: the reference is from the nLab page https://ncatlab.org/nlab/show/Whitehead+integral+formula (JSTOR 87688). The publisher and PubMed pages could not be fetched.

### 10. Sutcliffe 2007

[VERIFIED] P. Sutcliffe, "Knots in the Skyrme–Faddeev model," Proc. R. Soc. A **463**, 3001–3020 (2007); arXiv:0705.1468; DOI 10.1098/rspa.2007.0038. Fetched: https://inspirehep.net/api/arxiv/0705.1468 ; https://ar5iv.labs.arxiv.org/html/0705.1468
- "Numerical simulations are performed to compute soliton solutions for Hopf charges up to sixteen"
- "Often these knots are only local energy minima, with the global minimum being a linked solution"
- "Two loops obtained as the preimages of any two distinct points on the target two-sphere are linked exactly Q times, where Q is the Hopf charge."
- Link notation: "the total charge is the sum of the subscripts plus superscripts"
- Energy bound quoted there: "E≥c​Q^{3/4}"
- No Borromean or three-component configuration appeared in the fetched text.

### 11. Near-BPS Skyrme models and the binding-energy problem

[VERIFIED] C. Adam, J. Sánchez-Guillén, A. Wereszczynski, "A Skyrme-type proposal for baryonic matter," Phys. Lett. B **691**, 105–110 (2010); arXiv:1001.4544; DOI 10.1016/j.physletb.2010.06.025. Fetched: https://inspirehep.net/api/arxiv/1001.4544 ; https://ar5iv.labs.arxiv.org/html/1001.4544
- "binding energies of physical nuclei, which are usually quite small (below the 1% level)"
- "a submodel within the Skyrme-type low-energy effective action which does have a Bogomolny bound and exact Bogomolny solutions"
- "at least at the classical level, reproduces the nuclear masses by construction"
- Fix: sextic plus potential (BPS) submodel, with zero classical binding.

[VERIFIED] P. Sutcliffe, "Skyrmions, instantons and holography," JHEP **08** (2010) 019; arXiv:1003.0023; DOI 10.1007/JHEP08(2010)019. Fetched: https://inspirehep.net/api/arxiv/1003.0023 ; https://ar5iv.labs.arxiv.org/html/1003.0023
- "Instanton holonomies produce exact solutions of a BPS Skyrme model, in which the Skyrme field is coupled to a tower of vector mesons."
- "A theory that is close to a BPS system is required to reproduce the experimental data on binding energies of nuclei."
- "Such binding energies are much greater than those observed experimentally in nuclei, where binding energies are typically less than 1%"
- Standard-model numbers: "the energy of the B=1 Skyrmion is 12π² × 1.23 and the energy of the B=2 Skyrmion is 24π² × 1.18"
- Fix: a tower of vector mesons, from instanton holonomy.

[VERIFIED] M. Gillard, D. Harland, M. Speight, "Skyrmions with low binding energies," Nucl. Phys. B **895**, 272–287 (2015); arXiv:1501.05455; DOI 10.1016/j.nuclphysb.2015.04.005. Fetched: https://inspirehep.net/api/arxiv/1501.05455 ; https://ar5iv.labs.arxiv.org/html/1501.05455
- "typically, these are too large by an order of magnitude." (standard Skyrme binding energies)
- "The second includes a potential that is quartic in the pion fields."
- "The binding energies obtained in both models are lower than those obtained from the standard Skyrme model, and those obtained in the second model are close to the experimental values."
- "A Skyrme model with only a sextic term and a potential term is BPS: energies are directly proportional to the baryon number, and hence binding energies are zero."
- Fix: a "lightly bound" model with a quartic potential.

**Correction to the brief:** the figure "~15%" was **not found verbatim**. The verified statements are: an order of magnitude too large; B=1 at 1.23 and B=2 at 1.18 in units of the bound; nuclei below 1%.

### 12. Manton & Sutcliffe — moving soliton as a Lorentz boost

[VERIFIED — metadata] N. Manton, P. Sutcliffe, *Topological Solitons* (Cambridge University Press, 2004), Cambridge Monographs on Mathematical Physics; ISBN 9780521838368; DOI 10.1017/CBO9780511617034. Fetched: https://cambridge.org/core/books/topological-solitons/0A9670253EB1C8254BDACA4EE30C3AA3. The page shows chapter titles only, with no boost quote.

[PARTIAL — authors' lecture notes] N. Manton, "Topological Solitons," XIII Saalburg Summer School (Sept 2007), notes by M. Schwarz. Fetched: https://saalburg.aei.mpg.de/wp-content/uploads/sites/25/2017/03/manton.pdf
- §5.1 exercise: "The Lorentz boosted kink satisfies the full field equation of the theory"

[PARTIAL — unofficial student notes] Cambridge Part III "Classical and Quantum Solitons," N. S. Manton & D. Stuart, Easter 2017, notes by D. Chua. Fetched: https://dec41.user.srcf.net/notes/III_E/classical_and_quantum_solitons.pdf
- "Since this is relativistic, we can do a Lorentz boost, and we obtain a moving soliton."
- "Our theory is Lorentz invariant, so we simply apply a Lorentz boost. Then we obtain a field φ(x,t) = tanh γ(x − vt)."
- "Then we obtain an energy-momentum relation of the form E² − P·P = M²."

---

# PART 2 — prior-address map

## (a) "Q = L" in the Faddeev–Hopf (S² target) model — **ALREADY HAS IT, with a caveat**

- If **L means the linking number of the preimages of two distinct target points**, this is Whitehead (1947). The soliton literature states it verbatim: Battye–Sutcliffe 1999 (item 9), Sutcliffe 2007 (item 10), and Kawaguchi–Nitta–Ueda 2008 (below): "If the 𝐧 field has Hopf charge Q, two loops corresponding to the preimages of any two distinct points on the target S² will be linked Q times."
- **Caveat.** If L instead means the linking number between the two components of the soliton's own core curve (the "position string"), the literature gives a **different formula**:
  [VERIFIED] D. Harland, M. Speight, P. Sutcliffe, "Hopf solitons and elastic rods," Phys. Rev. D **83**, 065008 (2011); arXiv:1010.3189; DOI 10.1103/PhysRevD.83.065008. Fetched: https://inspirehep.net/api/arxiv/1010.3189 ; https://ar5iv.labs.arxiv.org/html/1010.3189
  - "If one links once a ring of charge Q₁ and a ring of charge Q₂, the resulting configuration has total charge Q=Q₁+Q₂+2"
  - "Hopf charge can be accrued by the linking of distinct components of the position string (or by self-linking of a single component)."
  - Sutcliffe 2007's notation says the same: "the total charge is the sum of the subscripts plus superscripts".
  - So for a two-component soliton link, Q = Q₁ + Q₂ + 2·lk, not Q = lk.
- Spinor-BEC version: [VERIFIED] Y. Kawaguchi, M. Nitta, M. Ueda, "Knots in a spinor Bose-Einstein condensate," Phys. Rev. Lett. **100**, 180403 (2008); erratum PRL 101, 029902 (2008); arXiv:0802.1968; DOI 10.1103/PhysRevLett.100.180403. Fetched: https://inspirehep.net/api/arxiv/0802.1968 ; https://ar5iv.labs.arxiv.org/html/0802.1968. Quotes: "We show that knots of spin textures can be created in the polar phase of a spin-1 Bose-Einstein condensate" and "The order parameter manifold for the polar phase is therefore given by M={(U(1)×S²)/ℤ₂}".

## (b) Two-component baryon: linked vortex core plus texture/hopfion envelope, mass = ropelength — **PARTLY HAS IT**

**Already in the literature: a vortex ring in one component with its core filled by the other forms a 3D skyrmion, and its degree equals the linking number of the two components' vortex lines.**
- [VERIFIED] J. Ruostekoski, J. R. Anglin, "Creating vortex rings and three-dimensional skyrmions in Bose-Einstein condensates," Phys. Rev. Lett. **86**, 3934–3937 (2001); arXiv:cond-mat/0103310; DOI 10.1103/PhysRevLett.86.3934. Fetched: https://inspirehep.net/api/arxiv/cond-mat/0103310 ; https://arxiv.org/abs/cond-mat/0103310
  - "Some remnant population of atoms in a second internal state remains within the toroidal trap formed by the mean field repulsion of the vortex ring."
  - "If this flow has unit topological winding number, the entire structure formed by the two condensates is an example of a three-dimensional skyrmion texture."
- [VERIFIED] R. A. Battye, N. R. Cooper, P. M. Sutcliffe, "Stable Skyrmions in two-component Bose-Einstein condensates," Phys. Rev. Lett. **88**, 080401 (2002); arXiv:cond-mat/0109448; DOI 10.1103/PhysRevLett.88.080401. Fetched: https://inspirehep.net/api/arxiv/cond-mat/0109448 ; https://ar5iv.labs.arxiv.org/html/cond-mat/0109448
  - "stable Skyrmions exist in two-component atomic Bose-Einstein condensates, in the regime of phase separation"
  - "The configuration can be viewed as a quantised vortex ring in one component close to whose core is confined the second component carrying quantised circulation around the ring."
  - "topological classification of (non-singular) field configurations, in terms of the winding number for the map S³→S³"
- [VERIFIED] E. Babaev, L. D. Faddeev, A. J. Niemi, "Hidden symmetry and knot solitons in a charged two-condensate Bose system," Phys. Rev. B **65**, 100512 (2002); arXiv:cond-mat/0106152; DOI 10.1103/PhysRevB.65.100512. Fetched: https://inspirehep.net/api/arxiv/cond-mat/0106152
  - "This implies in particular that such a system possesses a hidden O(3) symmetry and allows for the formation of stable knotted solitons."
- [VERIFIED] D. S. Hall, M. W. Ray, K. Tiurev, E. Ruokokoski, A. H. Gheorghe, M. Möttönen, "Tying quantum knots," Nature Phys. **12**, 478–483 (2016); arXiv:1512.08981; DOI 10.1038/nphys3624. Fetched: https://www.nature.com/articles/nphys3624 ; https://arxiv.org/abs/1512.08981
  - "knot solitons in the order parameter of a spinor Bose–Einstein condensate"
  - "topologically nontrivial element of the third homotopy group and exhibits the celebrated Hopf fibration"
- **Key result: the core linking and the Hopf charge are the same invariant, and both equal the baryon number.**
  - [VERIFIED] S. B. Gudnason, M. Nitta, "Linking number of vortices as baryon number," Phys. Rev. D **101**, 065011 (2020); arXiv:2002.01762; DOI 10.1103/PhysRevD.101.065011. Fetched: https://inspirehep.net/api/doi/10.1103/PhysRevD.101.065011 ; https://ar5iv.labs.arxiv.org/html/2002.01762
    - "the topological degree of a Skyrmion field is the same as the Hopf charge of the field under the Hopf map and thus equals the linking number of the preimages"
    - "we would like to associate the zero lines of each complex scalar field with (deformed) vortex rings."
    - "we conjecture that the topological degree of a Skyrmion can be interpreted as the product of winding numbers of vortices corresponding to the zero lines, summing over clusters of vortices."
  - [VERIFIED] S. B. Gudnason, M. Nitta, "Linked vortices as baryons in the miscible BEC-Skyrme model," Phys. Rev. D **102**, 045022 (2020); arXiv:2006.04067; DOI 10.1103/PhysRevD.102.045022. Fetched: https://inspirehep.net/api/arxiv/2006.04067
    - "the vortices are linked exactly B times, due to a recently formulated theorem, with B being the baryon number of the solution"
  - [VERIFIED] Y. Hamada, M. Nitta, Z. Qiu, "Baryons as linked vortices in QCD matter with isospin asymmetry," JHEP **02** (2026) 200; arXiv:2509.20844; DOI 10.1007/JHEP02(2026)200. Fetched: https://link.springer.com/article/10.1007/JHEP02(2026)200
    - "The linking number has the physical meaning of the baryon number in view of the Wess-Zumino-Witten term."
    - "The charged pions constitute a local ANO-like vortex, while the neutral pion configures a global vortex which is further attached to a domain wall also known as the chiral soliton."

**Partly in the literature: two distinct invariants in one Skyrme-type system.**
- [VERIFIED] K. Fujii, S. Otsuki, F. Toyoda, "A Soliton Solution With Baryon Number B=0 and Skyrmion," Prog. Theor. Phys. **73**, 524–532 (1985); DOI 10.1143/PTP.73.524. Fetched: https://inspirehep.net/api/doi/10.1143/PTP.73.524
  - "a soliton solution with the Hopf index H=1"
  - "The Hopf soliton is interpreted as a kind of composite of a Skyrmion and an anti-Skyrmion."
  - Here B and H differ, but they are not split between a core and an envelope as in the survivor.

**Mass = ropelength.** Not found for the baryon (proton) mass in refereed work. The nearest cases:
- [VERIFIED] R. V. Buniy, T. W. Kephart, "A model of glueballs," Phys. Lett. B **576**, 127–134 (2003); arXiv:hep-ph/0209339; DOI 10.1016/j.physletb.2003.09.081. Fetched: https://inspirehep.net/api/arxiv/hep-ph/0209339 ; https://ar5iv.labs.arxiv.org/html/hep-ph/0209339
  - "We model the observed glueball mass spectrum in terms of energies for tightly knotted and linked QCD flux tubes."
  - "the energy is positive and proportional to l and thus the minimum of the energy is achieved by shortening l, i.e. tightening the knot."
  - The model covers glueballs only. In the fetched text it does not treat baryons and does not mention Borromean links.
- [VERIFIED] R. V. Buniy, T. W. Kephart, "Glueballs and the universal energy spectrum of tight knots and links," Int. J. Mod. Phys. A **20**, 1252–1259 (2005); arXiv:hep-ph/0408027; DOI 10.1142/S0217751X05024146. Fetched: https://inspirehep.net/api/arxiv/hep-ph/0408027
  - "Systems of tightly knotted, linked, or braided flux tubes will have a universal mass-energy spectrum if the flux is quantized."
- [VERIFIED; refereed, 2026] T. Riedel, "Nuclear Binding Energies from Composite-Knot Ropelength: A Topological Model That Mirrors Quantum-Mechanical Phenomenology," Particles **9**(2), 43 (2026); DOI 10.3390/particles9020043; received 23 Feb 2026, accepted 7 Apr 2026. Fetched: https://www.mdpi.com/2571-712X/9/2/43
  - "the ropelength of the composite knot—a purely geometric quantity requiring no quantum mechanics—tracks the experimental binding-energy curve"
  - "Chirality plays the role of isospin projection"
  - Nucleons are modelled as trefoil ("threefoil") knots. **This is direct prior art for "nuclear energetics from ropelength".**
  - The fetch summary also said the paper mentions a Borromean-ring model under separate development. That is the tool's summary, not a verified quote.
- [VERIFIED] Harland–Speight–Sutcliffe 2011 (above). In actual Skyrme–Faddeev field theory the string energy is an elastic-rod energy, not ropelength: "The general form of the elastic rod energy is derived from the field theory energy and is found to be an extension of the classical Kirchhoff rod energy."
- [PARTIAL; preprint, title differs by version] F. Lin, X. Wang, arXiv:2601.20274 (Jan 2026). The v1 HTML title is "Gluon knots as the dynamical core of baryons"; INSPIRE lists "Toward a Unified Picture of Confinement and Baryon Structure". No journal. Fetched: https://arxiv.org/html/2601.20274v1 ; https://inspirehep.net/api/arxiv/2601.20274
  - "A gluon knot, as a specific monopole condensate configuration, thus emerges as a candidate for the baryonic core."
  - "The quantity L_ij measures the mutual linking number between the i-th and j-th color-magnetic flux tubes; the case i = j corresponds to self-linking."
  - The fetched text does not mention ropelength or Borromean links.

**Verdict for (b).** The ingredients are prior art: a vortex ring plus filled core equals a skyrmion, and the core linking number equals the degree, the Hopf charge and the baryon number. What is new, or would need justifying, is placing the linking invariant and the Hopf charge in *different* components as *independent* invariants. In the standard two-component construction the Gudnason–Nitta theorem makes them one invariant. Also new: identifying the baryon *mass* with ideal-knot ropelength. The closest prior work covers glueballs (Buniy–Kephart) and nuclear binding curves (Riedel 2026).

## (c) "Borromean linking = baryon number" — **refereed literature does NOT have it; non-refereed preprints DO (2026)**

- **Hadron physics uses "Borromean" in a different sense.** It means three-body binding, not knot-theoretic linking.
  [VERIFIED] C. D. Roberts, J. Segovia, "Baryons and the Borromeo," Few-Body Syst. **57**, 1067–1076 (2016); arXiv:1603.02722; DOI 10.1007/s00601-016-1150-9. Fetched: https://inspirehep.net/api/arxiv/1603.02722 ; https://ar5iv.labs.arxiv.org/html/1603.02722
  - "a system constituted from three bodies, no two of which can combine to produce an independent, asymptotic two-body bound-state"
  - "all may be viewed as Borromean bound-states, and the Roper is at heart the nucleon's first radial excitation"
- **Borromean quantum-vortex rings** have been studied as decaying dynamical objects, not as particles.
  [VERIFIED] H. Guan, S. Zuccher, X. Liu, "Topological cascade of quantum Borromean rings," Phys. Fluids **37**, 024126 (2025); DOI 10.1063/5.0252708. Fetched: https://zucchers.github.io/downloads/GZL_POF2025.pdf (author-hosted; the AIP page returned 403).
  - "The evolution and the topological cascade of quantum vortices forming Borromean rings are studied for the first time."
- **The mathematical bridge exists.** Milnor's triple linking number corresponds to Pontryagin's invariant of a map from the 3-torus to S².
  [PARTIAL — arXiv only; journal refs not verified] D. DeTurck, H. Gluck, R. Komendarczyk, P. Melvin, C. Shonkwiler, D. S. Vela-Vick, "Triple linking numbers, ambiguous Hopf invariants and integral formulas for three-component links," arXiv:0901.1612. Fetched: https://ar5iv.labs.arxiv.org/html/0901.1612
  - "Twice Milnor's μ-invariant for L is equal to Pontryagin's ν-invariant for gL."
  Same authors, "Pontryagin invariants and integral formulas for Milnor's triple linking number," arXiv:1101.3374. Fetched: https://ar5iv.labs.arxiv.org/html/1101.3374
  - "For example, the Borromean rings shown here have p=q=r=0 and μ=±1, where the sign depends on the ordering and orientation"
- **Hopfion solutions with Borromean structure: none found.** None appeared in the fetched text of Sutcliffe 2007 (Q ≤ 16), Harland–Speight–Sutcliffe 2011, Battye–Sutcliffe 1999, Gudnason–Nitta 2020 or Buniy–Kephart. Targeted searches found none either. This is absence in the checked sources, not proof of absence.
- **Non-refereed overlaps (2026).** These are directly on point.
  - [VERIFIED as record; Zenodo "Presentation", not peer-reviewed] M. Aksman, "The Neutron as a Twisted Borromean Soliton," Zenodo (8 Jul 2026), DOI 10.5281/zenodo.21252830. Fetched: https://zenodo.org/records/21252830
    - "We model the baryon as three interlocked vorton rings in a Borromean link—mutually inseparable though no two are pairwise linked"
    - "Confinement is rigorously topological and gluon-free: a Borromean link cannot be separated into its component rings without disassembling"
  - [VERIFIED as record] M. Aksman, "A Discrete Gauge-Theoretic Framework for Baryonic Topological Solitons," Zenodo (29 Jul 2026), DOI 10.5281/zenodo.21689199. Fetched: https://zenodo.org/records/21689199
    - "Standard Model baryons as Borromean bound states of singular vorton attractors"
  - [NOT FETCHED] ResearchGate 402541387, "The Topological Architecture of the Proton: Borromean Rings, Solenoid Confinement, and the 37,137 Vorton Lattice" (title from search results only; HTTP 429).
  - [NOT FETCHED] Zenodo 21046966, "The Topological Origin of Baryon Asymmetry: Matter as the Borromean-Locked Survivor…" (title from search results only; HTTP 429).
- **Analysis note (mine, not from the literature; checkable).** For S²-valued fields, Q = lk(preimage of p, preimage of q). Suppose the preimage of p is a Borromean triple C₁∪C₂∪C₃ (pairwise unlinked) and the preimage of q consists of nearby push-offs Cᵢ'. Then Q = Σᵢ lk(Cᵢ,Cᵢ') + Σ_{i≠j} lk(Cᵢ,Cⱼ') = Σ framings + 0. The Hopf charge (π₃(S²)) therefore does not see Milnor's μ̄₁₂₃. A "Borromean = baryon number" claim needs an invariant beyond the Hopf/S³ degree, such as the T³→S² Pontryagin invariant above.

## (d) "Z₃ vacuum form": Φ in the symmetric 6 of SU(3), with −γ Re det Φ — **standard ingredients, but this specific form was not found**

**Group theory, verified by computation.** Script: `sym6_check.py` in this folder, using sympy. It solves for sl(3)-annihilated polynomials on the 6 with action δΦ = XΦ + ΦXᵀ.
- Holomorphic invariants: none of degree 1, none of degree 2, and **exactly one of degree 3, which equals det Φ**. This is the classical discriminant of a ternary quadratic form.
- The centre element ω·1 (ω = e^{2πi/3}) acts on the 6 as **ω²** (6 ⊂ 3⊗3 has triality 2).
- **Consequence.** The three minima of −γ|det Φ|cos3α at α = 0, 2π/3, 4π/3 are related by the SU(3) centre (U = ω²·1 gives UΦUᵀ = ωΦ). They therefore lie on one SU(3) orbit. They are **not physically distinct vacua**: no Z₃ domain walls, and π₀ of the vacuum manifold is trivial. The only exception is when the true symmetry is a subgroup that lacks the centre. The same holds for the 't Hooft term below, where the Z₃ remnant of U(1)_A sits inside the centre of SU(3)_L × SU(3)_R.
- Contrast with the Polyakov loop, where Z(3) vacua *are* distinct, because the adjoint action does not see the centre.

**Closest standard literature**
- [VERIFIED] J. T. Lenaghan, D. H. Rischke, J. Schaffner-Bielich, "Chiral symmetry restoration at nonzero temperature in the SU(3)_r × SU(3)_l linear sigma model," Phys. Rev. D **62**, 085008 (2000); arXiv:nucl-th/0004006; DOI 10.1103/PhysRevD.62.085008. Fetched: https://inspirehep.net/api/arxiv/nucl-th/0004006 ; https://ar5iv.labs.arxiv.org/html/nucl-th/0004006
  - "Φ → U_r Φ U_ℓ^†"
  - "The determinant terms correspond to the U(1)_A anomaly in the QCD vacuum. As shown by 't Hooft, they arise from instantons."
  - "These terms are invariant under SU(3)_r × SU(3)_ℓ ≅ SU(3)_V × SU(3)_A transformations, but break the U(1)_A symmetry explicitly."
  - "For N_f=3 massless flavors, the transition is always first order. In this case, the term which breaks the U(1)_A symmetry is a cubic invariant."
- [VERIFIED] R. D. Pisarski, F. Wilczek, "Remarks on the chiral phase transition in chromodynamics," Phys. Rev. D **29**, 338–341 (1984); DOI 10.1103/PhysRevD.29.338. Fetched: https://inspirehep.net/api/doi/10.1103/PhysRevD.29.338
  - "For three or more massless flavors, the perturbative ε expansion predicts the phase transition is of first order."
  - "At high temperatures, the UA(1) symmetry will also be effectively restored."
- [VERIFIED; title discrepancy] R. D. Pisarski, Phys. Rev. D **62**, 111501 (2000); arXiv:hep-ph/0006205; DOI 10.1103/PhysRevD.62.111501. INSPIRE title: "Quark gluon plasma as a condensate of SU(3) Wilson lines"; ar5iv title: "…Z(3) Wilson Lines". Fetched: https://inspirehep.net/api/arxiv/hep-ph/0006205 ; https://ar5iv.labs.arxiv.org/html/hep-ph/0006205
  - "For N=3, the simplest examples include det𝐋+c.c., (tr𝐋)³+c.c., tr𝐋(tr𝐋²)+c.c.."
  - "Different j are the usual N degenerate vacua of the broken Z(N) global symmetry."
  - "⟨𝐋⟩=exp(2πij/N)ℓ₀ 𝟏, j=0...(N-1)."
- [VERIFIED] T. Bhattacharya, A. Gocksch, C. Korthals Altes, R. D. Pisarski, "Interface tension in an SU(N) gauge theory at high temperature," Phys. Rev. Lett. **66**, 998–1000 (1991); DOI 10.1103/PhysRevLett.66.998. Fetched: https://inspirehep.net/api/doi/10.1103/PhysRevLett.66.998
  - "The interface tension between distinct Z(N) vacua is computed in weak coupling by semiclassical techniques."
- Sextet condensates (symmetric colour tensor). The known effective potentials are U(1)_B-invariant and contain no det term:
  - [VERIFIED] T. Brauner, J. Hošek, R. Sýkora, "Color superconductor with a color-sextet condensate," Phys. Rev. D **68**, 094004 (2003); arXiv:hep-ph/0303230; DOI 10.1103/PhysRevD.68.094004. Fetched: https://inspirehep.net/api/arxiv/hep-ph/0303230 ; https://ar5iv.arxiv.org/html/hep-ph/0303230
    - "V(Φ)=−a tr Φ†Φ+b tr(Φ†Φ)²+c(tr Φ†Φ)², where the minus sign at a suggests spontaneous symmetry breaking."
    - "The continuous SU(3)×U(1) symmetry is completely broken (only a discrete (Z₂)³ symmetry is left)."
    - Per the fetch, there is no cubic det term.
  - [VERIFIED as conference preprint] R. D. Pisarski, D. H. Rischke, "Why color-flavor locking is just like chiral symmetry breaking," arXiv:nucl-th/9907094 (Tel Aviv conf., Apr 1999; no DOI). Fetched: https://inspirehep.net/api/arxiv/nucl-th/9907094 ; https://ar5iv.labs.arxiv.org/html/nucl-th/9907094
    - "it also contains a piece which is symmetric, and so is a color sextet."
    - "multiplying by the operator det(φ)*; this is also invariant under SU(3)_c color and SU(3)_f flavor, but precisely soaks up the requisite factors for baryon number"
- [VERIFIED — metadata only] L.-F. Li, "Group theory of the spontaneously broken gauge symmetries," Phys. Rev. D **9**, 1723–1739 (1974); DOI 10.1103/PhysRevD.9.1723. Fetched: https://inspirehep.net/api/doi/10.1103/PhysRevD.9.1723
  - "investigated systematically in the general rotation groups and unitary groups, with Higgs scalars in the various representations up to second-rank tensors"
  - The treatment of the symmetric 6 itself was not verified.
- [VERIFIED as record; Research Square preprint, not peer-reviewed] M. Hannan, "The proton has no lifetime, only a cross-section: Triality-locked baryon number and vortex-catalyzed nucleon decay," DOI 10.21203/rs.3.rs-10504019/v1 (29 Jul 2026). Fetched: https://www.researchsquare.com/article/rs-10504019/v1
  - "It is realized instead inside the cores of the Z3 baryonic vortices that the breaking U(1)B →Z3 necessarily produces"

**Verdict for (d).** The structure "cubic det, U(1) broken to Z₃, cos 3α, three minima" is textbook in two settings: the 't Hooft determinant for (3,3̄) at N_f = 3, and Z(3) Wilson-line potentials. The specific form "symmetric 6 with Φ → UΦUᵀ plus Re det Φ" was not found as a standard construction. Sextet condensates preserve U(1)_B, which forbids it. Its three minima are SU(3)-equivalent, so it does not generate distinct Z₃ vacua by itself.

---

## Corrections to the metadata in the brief

1. The Volovik paper-length statement is Phil. Trans. R. Soc. A 366, 2935–2951 (2008) = arXiv:0801.0724. arXiv:0709.1258 is a separate PoS paper (QG-Ph 043, 2007). The clearest species-speed quote is from JETP Lett. 73, 162 (2001) [hep-ph/0101286].
2. Liberati–Visser–Weinfurtner titles: the PRL is "Naturalness in emergent spacetime"; the CQG is "Analogue quantum gravity phenomenology from a two-component Bose-Einstein condensate" (pp. 3129–3154).
3. Faddeev & Niemi: the Nature title is correct (pp. 58–61). The arXiv version is titled "Knots and particles".
4. Hall et al. 2016 is arXiv:1512.08981.
5. Pisarski (2000): the title differs between INSPIRE ("SU(3) Wilson lines") and ar5iv ("Z(3) Wilson Lines").
6. The "~15% binding" figure was not found verbatim (see item 11).
7. All other volumes, pages and years given in the brief matched.
