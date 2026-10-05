# A2 literature check: vacuum Cherenkov / analogue gravity / supersolids / impurity drag

Checked 2026-10-03. Tools used: WebFetch and WebSearch only. Bash egress to arxiv.org, export.arxiv.org and inspirehep.net was blocked by the proxy, so every fetch below went through WebFetch.

**How metadata was checked.** Journal metadata came from Crossref (`api.crossref.org/works/<DOI>`) or OpenAlex (`api.openalex.org/works/doi:<DOI>`). arXiv IDs came from arXiv abstract, PDF or HTML pages, or from the INSPIRE `api/arxiv/<id>` record, or from the arXiv location that OpenAlex lists.

**How quotes were checked.** Quotes come from arXiv abstract pages or full text (PDF, arxiv.org/html, ar5iv). WebFetch passes each page through a small model and caps every quote at about 125 characters. Treat quotes as verbatim unless marked [rendered math] or [reconstructed].
- [rendered math]: the tool rendered the symbols. The words are verbatim, but the symbols may differ typographically from the PDF.
- [reconstructed]: rebuilt from OpenAlex's `abstract_inverted_index`, which stores each word's position in the abstract. The word order should be exact, but this is not a publisher page.

**Pages that could not be read:**
- Crossref returned HTTP 429 (rate limited) for `works/10.1103/PhysRevA.88.033618`, `works/10.1103/PhysRevLett.98.195301` and `works/10.1103/PhysRevX.8.031042`. Per the proxy instruction these were not retried. All three papers were verified through other sources instead.
- APS journal pages returned 403. IOP pages showed a CAPTCHA, and so did PubMed.
- jetp.ras.ru is HTTP-only. WebFetch upgrades to HTTPS and the server redirects back, so the page loops and never loads.
- ADS and export.arxiv.org are disallowed by robots.txt. Semantic Scholar returned 429.

---

## A. Vacuum Cherenkov / preferred frame / maximal attainable velocity (MAV)

**1. [VERIFIED]** T. Jacobson & D. Mattingly, "Gravity with a dynamical preferred frame," Phys. Rev. D 64, 024028 (2001)
- arXiv: gr-qc/0007031
- DOI: 10.1103/PhysRevD.64.024028
- Fetched: https://arxiv.org/abs/gr-qc/0007031 ; https://ar5iv.arxiv.org/html/gr-qc/0007031
- Quote (abstract): "We study a generally covariant model in which local Lorentz invariance is broken by a dynamical unit timelike vector field"
- Relevance: the original Einstein-aether (dynamical preferred-frame) model.

**2. [VERIFIED]** T. Jacobson & D. Mattingly, "Einstein-aether waves," Phys. Rev. D 70, 024003 (2004)
- arXiv: gr-qc/0402005
- DOI: 10.1103/PhysRevD.70.024003
- Fetched: https://arxiv.org/abs/gr-qc/0402005
- Quotes (abstract): "find the speeds and polarizations of all the wave modes in terms of the four constants appearing in the most general action at second order in derivatives" … "in addition to the usual two transverse traceless metric modes, there are three coupled aether-metric modes."
- Relevance: gives the mode speeds that the Cherenkov bounds constrain.

**3. [VERIFIED]** J. W. Elliott, G. D. Moore & H. Stoica, "Constraining the new aether: gravitational Cherenkov radiation," JHEP 08 (2005) 066
- arXiv title: "Constraining the New Aether: Gravitational Cherenkov Radiation"
- arXiv: hep-ph/0505211
- DOI: 10.1088/1126-6708/2005/08/066
- Fetched: https://arxiv.org/abs/hep-ph/0505211 ; https://arxiv.org/pdf/hep-ph/0505211
- Quotes:
  - Abstract: "the observation of ultra-high energy cosmic rays (which implies the absence of energy loss via various Cherenkov type processes) places constraints on the parameters of this theory, which are much stronger than those previously found"
  - Conclusion: "Cherenkov processes rule out the New Aether theory unless … all three propagating modes (graviton and two S field) are light-like to extremely high precision". The other escape routes are a VEV v < 3×10⁻⁸ m_pl, or Eq. (2.11) being incorrect.
  - Graviton bound, Eq. (3.13), from a cosmic ray of energy ~3×10¹¹ GeV travelling 10 kpc [rendered math]: "ε ≡ (−c₁ − c₃)/2 < 5 × 10⁻¹⁶".
  - Spin-1 bound [rendered math]: "(c₁+c₃)²(c₁²+2c₁c₃+c₃²−2c₄)/(2c₁²) < 7 × 10⁻³²"
  - Spin-0 bound [rendered math]: "(c₃ − c₄)²/|c₁ + c₄| < 1 × 10⁻³⁰"
  - The paper separately assumes "propagation speeds not be superluminal". Together with the Cherenkov bounds, this forces every mode to be luminal.
- Caveat: the exact phrase "each mode must be at least as fast as light" was not found. The logic is that a subluminal mode can be Cherenkov-radiated: "these modes carry more momentum than energy, and it is kinematically allowed to emit one."
- Relevance: the standard result that ultra-high-energy cosmic rays forbid any subluminal mode, to about 10⁻¹⁵.

**4. [VERIFIED]** G. D. Moore & A. E. Nelson, "Lower bound on the propagation speed of gravity from gravitational Cherenkov radiation," JHEP 09 (2001) 023
- arXiv: hep-ph/0106220
- DOI: 10.1088/1126-6708/2001/09/023 (Crossref: published 14 Sep 2001)
- Fetched: https://api.crossref.org/works/10.1088/1126-6708/2001/09/023 ; https://ar5iv.labs.arxiv.org/html/hep-ph/0106220
- Quotes (abstract):
  - "the case c_g<c is very tightly constrained by the observation of the highest energy cosmic rays."
  - "Assuming a galactic origin for the cosmic rays gives a conservative bound of c-c_g<2×10^-15c; if the cosmic rays have an extragalactic origin the bound is … of order c-c_g<2×10^-19c."
- Body text: "The highest energy cosmic ray which has been observed was probably a proton, of energy ∼ 3×10^11GeV."
- Relevance: the canonical quantitative gravitational-Cherenkov bound.

**5a. [VERIFIED]** S. Coleman & S. L. Glashow, "High-energy tests of Lorentz invariance," Phys. Rev. D 59, 116008 (1999)
- arXiv: hep-ph/9812418
- DOI: 10.1103/PhysRevD.59.116008
- Fetched: https://api.crossref.org/works/10.1103/PhysRevD.59.116008 ; https://arxiv.org/pdf/hep-ph/9812418
- Quotes:
  - "To each particle species we assign a maximal attainable velocity $c_a$."
  - Abstract: "They define the energy-momentum eigenstates and their maximal attainable velocities in the high-energy limit."
  - Vacuum Cherenkov: "In this case a charged particle traveling faster than light rapidly radiates photons until it is no longer superluminal."
  - Bound, as transcribed by the tool (check the exponent against the PDF): "Because primary protons with energies up to $10^{20}$ eV are seen, we set the bound $1-c^2 < 10^{-23}$."
- Relevance: introduces species-dependent MAVs and the vacuum-Cherenkov kinematic argument.

**5b. [VERIFIED]** S. Coleman & S. L. Glashow, "Cosmic ray and neutrino tests of special relativity," Phys. Lett. B 405, 249–252 (1997)
- arXiv: hep-ph/9703240
- DOI: 10.1016/S0370-2693(97)00638-2
- Fetched: https://inspirehep.net/api/arxiv/hep-ph/9703240 ; https://arxiv.org/pdf/hep-ph/9703240
- Quotes:
  - "if the maximum attainable speed of a particle depends on its identity, then neutrinos, even if massless, may exhibit flavor oscillations."
  - "A charged particle traveling faster than light loses energy rapidly via vacuum Cerenkov radiation."
  - Bound, tool transcription: "1 − c < 5 × 10−23".
- Relevance: the earliest MAV and vacuum-Cherenkov statement.

**6. [VERIFIED]** T. Jacobson, S. Liberati & D. Mattingly, "Lorentz violation at high energy: concepts, phenomena and astrophysical constraints," Ann. Phys. 321, 150–196 (2006)
- arXiv: astro-ph/0505267
- DOI: 10.1016/j.aop.2005.06.004
- Fetched: https://api.crossref.org/works/10.1016/j.aop.2005.06.004 ; https://inspirehep.net/api/arxiv/astro-ph/0505267 ; https://arxiv.org/abs/astro-ph/0505267
- Quote: "We review the effective field theory approach to describing LV, the issue of naturalness, and many phenomena characteristic of LV."
- Relevance: a standard review of vacuum Cherenkov and other high-energy Lorentz-violation constraints.

## B. Analogue gravity: bi-metricity, mono-metricity and naturalness

**7. [VERIFIED]** C. Barceló, S. Liberati & M. Visser, "Analogue gravity," Living Rev. Relativ. 8, 12 (2005), with the update Living Rev. Relativ. 14, 3 (2011)
- arXiv: gr-qc/0505065. Version v3 is the "Major update as of 10 May 2011". Version v4 is a further "Major update as of 29 Nov 2024", so the current arXiv text is neither the 2005 nor the 2011 edition.
- DOIs: 10.12942/lrr-2005-12 ; 10.12942/lrr-2011-3 (Crossref: published 11 May 2011)
- Fetched: https://arxiv.org/abs/gr-qc/0505065 ; https://api.crossref.org/works/10.12942/lrr-2005-12 ; https://api.crossref.org/works/10.12942/lrr-2011-3 ; https://link.springer.com/article/10.12942/lrr-2011-3
- Quote (2011 edition, Sect. 2.7.3): "in superfluids there will be multiple acoustic metrics — and multiple acoustic horizons — corresponding to first and second sound." The authors credit this point to Comer.
- Caveat: Sect. 2.9 lists a topic "Normal modes in generic systems", but the full text of that section was cut off in the fetch. No mono-metricity sentence was retrieved from either edition.
- Relevance: multiple sound modes mean multiple effective metrics.

**8. [VERIFIED]** C. Barceló, S. Liberati & M. Visser, "Refringence, field theory, and normal modes," Class. Quantum Grav. 19, 2961–2982 (2002)
- arXiv: gr-qc/0111059
- DOI: 10.1088/0264-9381/19/11/314
- Fetched: https://inspirehep.net/api/arxiv/gr-qc/0111059 ; https://arxiv.org/pdf/gr-qc/0111059
- Quotes:
  - Abstract: "In the simple (single scalar field) situation … there is a single unique effective metric; more complicated situations can lead to bi-metric and multi-metric theories."
  - Condition for one metric [rendered math]: "there must be some choice of field variables so that all the new $\bar{\phi}_1^A$ see the same metric, that is: $\bar{f}^{\mu\nu}{}_{AB} = \delta_{AB} f^{\mu\nu}$". The paper also gives a commutation condition for simultaneous diagonalizability: $f^{\mu\nu}{}_{AB} f^{\alpha\beta}{}_{BC} = f^{\alpha\beta}{}_{AB} f^{\mu\nu}{}_{BC}$.
- Relevance: the formal condition for mono-metricity in multi-field systems.

**9. [VERIFIED; venue from INSPIRE]** M. Visser, C. Barceló & S. Liberati, "Bi-refringence versus bi-metricity"
- arXiv: gr-qc/0204017
- Venue: book chapter in J. M. Salim et al. (eds.), *Inquiring the Universe: Essays to Celebrate Professor Mario Novello Jubilee* (Frontier Group, 2003), pp. 397–429, ISBN 978-2-914601-08-5. The PDF says: "Contribution to the Festschrift in honour of Professor Mário Novello." This is not a journal article. INSPIRE also lists "Santa Barbara" as the place, which looks odd, so check the place before using it.
- Fetched: https://inspirehep.net/api/arxiv/gr-qc/0204017 ; https://arxiv.org/pdf/gr-qc/0204017
- Quotes:
  - "the quartic factorizes into two quadratics thus providing a bi-metric theory. Sometimes the quartic is a perfect square, implying a single unique effective metric."
  - "these notions are logically distinct"
- Relevance: separates birefringence from bi-metricity from mono-metricity.

**10a. [VERIFIED]** S. Liberati, M. Visser & S. Weinfurtner, "Naturalness in an emergent analogue spacetime," Phys. Rev. Lett. 96, 151301 (2006)
- arXiv: gr-qc/0512139. INSPIRE also lists the shorter title "Naturalness in emergent spacetime".
- DOI: 10.1103/PhysRevLett.96.151301
- Fetched: https://api.crossref.org/works/10.1103/PhysRevLett.96.151301 ; https://arxiv.org/pdf/gr-qc/0512139
- Quotes:
  - "They both "experience" the same space-time if the sound speeds are equal, which requires tr[C₀²]² − 4det[C₀²] = 0" [rendered math]
  - Abstract: "our model explicitly avoids the "naturalness problem""
  - "there is no natural suppression of the low-order modifications in these models."
- Relevance: equal sound speeds are a tuning condition, and the paper addresses naturalness.

**10b. [VERIFIED]** S. Liberati, M. Visser & S. Weinfurtner, "Analogue quantum gravity phenomenology from a two-component Bose–Einstein condensate," Class. Quantum Grav. 23, 3129–3154 (2006)
- arXiv: gr-qc/0510125
- DOI: 10.1088/0264-9381/23/9/023
- Fetched: https://inspirehep.net/api/arxiv/gr-qc/0510125 ; https://arxiv.org/pdf/gr-qc/0510125
- Quotes (abstract):
  - "This system can be tuned to have two "phonon" modes (one massive, one massless) which share the same limiting speed in the hydrodynamic approximation"
  - "We investigate the physical interpretation of the relevant fine-tuning conditions"
- Body [rendered math]: the condition is $C_0^2 = c_0^2\mathbf{I}$, which gives $\tilde U_{AB}=0$.
- Relevance: mono-metricity requires fine-tuning.

**11. [VERIFIED; title correction]** M. Visser & S. Weinfurtner, Phys. Rev. D 72, 044020 (2005)
- Published title (Crossref): "Massive Klein-Gordon equation from a Bose-Einstein-condensation-based analogue spacetime". The arXiv and INSPIRE title is the one you gave, "…from a BEC-based analogue spacetime".
- arXiv: gr-qc/0506029
- DOI: 10.1103/PhysRevD.72.044020
- Fetched: https://api.crossref.org/works/10.1103/PhysRevD.72.044020 ; https://inspirehep.net/api/arxiv/gr-qc/0506029 ; https://arxiv.org/pdf/gr-qc/0506029
- Quotes (abstract):
  - "the two distinct phonons generically couple to distinct effective spacetimes, representing a bi-metric model"
  - "it is possible to tune the system so that both modes can be to arranged travel at the same speed, in which case the two phonon excitations couple to the same effective metric." The garbled wording "can be to arranged" is in the original.
- Relevance: the clearest statement that bi-metricity is generic and mono-metricity is tuned.

## C. Supersolid hydrodynamics and density response

**12. [VERIFIED; your title is correct]** C.-D. Yoo & A. T. Dorsey, "Hydrodynamic theory of supersolids: Variational principle, effective Lagrangian, and density-density correlation function," Phys. Rev. B 81, 134518 (2010)
- arXiv: 1001.0621. The arXiv title is shorter: "Hydrodynamic theory of supersolids: Variational principle and effective Lagrangian".
- DOI: 10.1103/PhysRevB.81.134518
- Fetched: https://api.crossref.org/works/10.1103/PhysRevB.81.134518 ; https://arxiv.org/abs/1001.0621 ; https://arxiv.org/pdf/1001.0621
- Quotes:
  - Abstract: "we show that the onset of supersolidity produces peaks in the response function, corresponding to propagating second sound modes in the solid."
  - Eq. (51) [rendered math]: "$c_T = \sqrt{\tilde{\mu}/\rho_{n0}}$"
- Relevance: a verified source for c_t = √(shear modulus / normal density).

**13. [VERIFIED]** D. T. Son, "Effective Lagrangian and topological interactions in supersolids," Phys. Rev. Lett. 94, 175301 (2005)
- arXiv: cond-mat/0501658
- DOI: 10.1103/PhysRevLett.94.175301
- Fetched: https://api.crossref.org/works/10.1103/PhysRevLett.94.175301 ; https://api.openalex.org/works/doi:10.1103/PhysRevLett.94.175301 ; https://arxiv.org/abs/cond-mat/0501658
- Quote: "Galilean invariance imposes strict constraints on the form of the effective Lagrangian. We identify a topological term in the Lagrangian that couples superfluid and crystalline modes."
- Relevance: the low-energy effective field theory of a supersolid.

**14. [PARTIAL]** A. F. Andreev & I. M. Lifshitz, "Quantum theory of defects in crystals," Sov. Phys. JETP 29(6), 1107–1113 (1969)
- arXiv: none
- Fetched: https://bibbase.org/network/publication/andreev-lifshitz-quantumtheoryofdefectsincrystals-1969 . That page gives the authors, title, volume 29, issue 6 and pp. 1107–1113. The DOI it lists (10.1103/PhysRevLett.23.778) is wrong and should be ignored.
- The JETP listing page (jetp.ras.ru/cgi-bin/e/index/e/29/6/p1107) appeared in search results under this title, but could not be loaded because of the HTTPS redirect loop.
- No quote was obtained. The Russian original (Zh. Eksp. Teor. Fiz. 56, 2057) was not verified.
- Relevance: the original proposal that zero-point defects make a crystal superfluid.

**15. [VERIFIED metadata; PARTIAL quote]** E. Poli, D. Baillie, F. Ferlaino & P. B. Blakie, "Excitations of a two-dimensional supersolid," Phys. Rev. A 110, 053301 (2024)
- Authors confirmed. The paper is not by Platt, Baillie & Blakie.
- arXiv: 2407.01072
- DOI: 10.1103/PhysRevA.110.053301 (Crossref: published 4 Nov 2024)
- Fetched: https://api.crossref.org/works/10.1103/PhysRevA.110.053301 ; https://arxiv.org/abs/2407.01072 ; https://arxiv.org/html/2407.01072v2 ; https://arxiv.org/html/2407.01072 ; https://arxiv.org/pdf/2407.01072
- Quotes:
  - "The next branch is the second sound or phase mode, which has a weak density contribution."
  - Abstract: "The third branch is a transverse wave arising from the non-zero shear modulus of the two-dimensional crystal."
- **Problem with Eq. (13).** Four fetches (HTML ×3, PDF ×1) all render it as "$mc_t^2 = \frac{\tilde{\mu}}{a}$". The text after it ("where we have defined") defines only a_Δ and b_Δ, never a plain a.
  - The paper's Lagrangian, Eq. (10), contains ½mρ_n(∂_t u − …)² and the elastic tensor C_ijkl = λ̃δδ + μ̃(δδ+δδ). These imply mc_t² = μ̃/ρ_n.
  - μ̃/a with a = lattice constant has the wrong dimensions. The "a" is probably a rendering artefact or a typo.
  - **Check the PRA PDF by eye before quoting Eq. (13).** Yoo & Dorsey Eq. (51) (item 12) is a safer source for c_t = √(μ/ρ_n).
- Densities defined in the paper: "the average superfluid density ρ_s = f_s ρ, and the average normal density ρ_n = (1 - f_s)ρ".

**16. [VERIFIED; now published]** L. M. Platt, D. Baillie & P. B. Blakie, "Supersolid spectroscopy," Phys. Rev. A 111, 053305 (2025)
- arXiv: 2412.15552
- DOI: 10.1103/PhysRevA.111.053305 (Crossref: published 7 May 2025)
- Fetched: https://api.crossref.org/works/10.1103/PhysRevA.111.053305 ; https://arxiv.org/pdf/2412.15552
- Note: the paper treats **one-dimensional** supersolids.
- Quotes:
  - Abstract: "determine its excitation frequencies and density response characteristics. This information can be used to estimate the superfluid fraction."
  - "Notably, the lowest band edge mode has a density fluctuation causing population exchange between adjacent sites."
  - "The hydrodynamic theory for Galilean invariant supersolids furnishes a relationship between the superfluid fraction and the speeds of sound". As transcribed: f_s = c₁²c₀²/[c_κ²(c₁²+c₀²−c_κ²)] [rendered math; check before use].
  - The paper extracts density-response weights χ^ρ_ν(k) for both lowest bands, ν = 0 and 1.
- Caveat: no single sentence saying "both gapless branches carry density weight" was found.

**17. [VERIFIED; your title is correct]** M. Kunimi & Y. Kato, "Mean-field and stability analyses of two-dimensional flowing soft-core bosons modeling a supersolid," Phys. Rev. B 86, 060510(R) (2012)
- arXiv: 1205.2126. The arXiv title says "analysis" (singular).
- DOI: 10.1103/PhysRevB.86.060510
- Fetched: https://api.crossref.org/works/10.1103/PhysRevB.86.060510 ; https://arxiv.org/html/1205.2126
- Quotes:
  - "We note that the lowest branch in the SS phase is the Bogoliubov mode, which causes instabilities in the SS phase as described later."
  - "Figure 4 (b) shows that the Bogoliubov mode that has a negative real part, which destabilizes the SS phase."
  - The paper uses LI (Landau instability) for the negative-real-part case and DI for the case with a nonzero imaginary part.
- Relevance: exactly the claim you wanted.

**18. [VERIFIED]** F. Ancilotto, M. Rossi & F. Toigo, "Supersolid structure and excitation spectrum of soft-core bosons in three dimensions," Phys. Rev. A 88, 033618 (2013)
- arXiv: 1309.2769
- DOI: 10.1103/PhysRevA.88.033618
- Fetched: https://api.openalex.org/works/doi:10.1103/PhysRevA.88.033618 ; https://arxiv.org/abs/1309.2769
- Quote: "the excitation spectrum shows a soft mode related to the breaking of gauge symmetry" … "the superfluid fraction, which shows a first-order drop, from 1 to 0.4, at the liquid-supersolid transition"
- Relevance: the 3D soft-core supersolid spectrum.

**19. [VERIFIED]** S. Saccani, S. Moroni & M. Boninsegni, "Excitation spectrum of a supersolid," Phys. Rev. Lett. 108, 175301 (2012)
- arXiv: 1201.4784
- DOI: 10.1103/PhysRevLett.108.175301
- Fetched: https://api.crossref.org/works/10.1103/PhysRevLett.108.175301 ; https://api.openalex.org/works/doi:10.1103/PhysRevLett.108.175301 ; https://arxiv.org/abs/1201.4784
- Quote: "it features two distinct modes, namely a solid-like phonon and a softer collective excitation, related to broken translation and gauge symmetry respectively."

**20. [VERIFIED]** T. Macrì, F. Maucher, F. Cinti & T. Pohl, "Elementary excitations of ultracold soft-core bosons across the superfluid-supersolid phase transition," Phys. Rev. A 87, 061602(R) (2013)
- arXiv: 1212.6934
- DOI: 10.1103/PhysRevA.87.061602
- Fetched: https://api.crossref.org/works/10.1103/PhysRevA.87.061602 ; https://arxiv.org/pdf/1212.6934
- Quotes on the 2D transition order:
  - "density modulations become energetically favorable for α ≥ 12.65, marking a first order phase transition to a cluster supersolid state"
  - "One finds a first order phase transition at α ≈ 13.4, signaled by an abrupt drop of the superfluid fraction"
  - "roton softening occurs at α=14.74, preceded by the supersolid phase transition at α=12.7"
- Relevance: the 2D transition is first order and happens before the roton gap closes.

**21. [VERIFIED]** N. Henkel, R. Nath & T. Pohl, "Three-dimensional roton excitations and supersolid formation in Rydberg-excited Bose-Einstein condensates," Phys. Rev. Lett. 104, 195302 (2010)
- arXiv: 1001.3250
- DOI: 10.1103/PhysRevLett.104.195302
- Fetched: https://api.crossref.org/works/10.1103/PhysRevLett.104.195302 ; https://api.openalex.org/works/doi:10.1103/PhysRevLett.104.195302 ; https://arxiv.org/pdf/1001.3250
- Quotes:
  - "giving rise to a roton-maxon excitation spectrum and a transition to a super solid state in three-dimensional condensates."
  - "This first-order transition precedes the roton-instability."

**22a. [VERIFIED metadata; quote reconstructed]** Y. Pomeau & S. Rica, "Dynamics of a model of supersolid," Phys. Rev. Lett. 72, 2426–2429 (1994)
- arXiv: none found
- DOI: 10.1103/PhysRevLett.72.2426
- Fetched: https://api.crossref.org/works/10.1103/PhysRevLett.72.2426 ; https://api.openalex.org/works/doi:10.1103/PhysRevLett.72.2426
- Quote [reconstructed]: "Although uniform rotation occurs without dissipation, dissipationless flow around an obstacle is not possible."
- Relevance: directly relevant to drag on an obstacle in a supersolid. The sentence comes from an index-reconstructed abstract, so confirm it against the PRL before relying on it.

**22b. [VERIFIED]** C. Josserand, Y. Pomeau & S. Rica, "Coexistence of ordinary elasticity and superfluidity in a model of a defect-free supersolid," Phys. Rev. Lett. 98, 195301 (2007)
- arXiv: cond-mat/0611402. The arXiv title is "Coexisting ordinary elasticity and superfluidity in a model of defect-free supersolid".
- DOI: 10.1103/PhysRevLett.98.195301
- Fetched: https://api.crossref.org/works?query.bibliographic=Coexistence+of+ordinary+elasticity… ; https://api.openalex.org/works/doi:10.1103/PhysRevLett.98.195301 ; https://arxiv.org/abs/cond-mat/0611402 ; https://arxiv.org/pdf/cond-mat/0611402
- Quotes:
  - "Our model displays a paradoxical behavior: the existence of a non classical rotational inertia fraction in the limit of small rotation speed and no superflow under small (but finite) stress"
  - "the shear waves are decoupled from the compression and phase (Bogoliubovlike) waves."

**23. [VERIFIED metadata; quote reconstructed]** A. J. Leggett, "Can a solid be 'superfluid'?," Phys. Rev. Lett. 25, 1543–1546 (1970)
- DOI: 10.1103/PhysRevLett.25.1543
- Fetched: https://api.crossref.org/works/10.1103/PhysRevLett.25.1543 ; https://api.openalex.org/works/doi:10.1103/PhysRevLett.25.1543
- Quotes [reconstructed]:
  - "It is suggested that the property of nonclassical rotational inertia possessed by superfluid liquid helium may be shared by some solids."
  - "the associated superfluid fraction is shown to be very small (probably ≲10⁻⁴) even at T=0"
- Caveat: the abstract gives no closed-form bound. The formula f_s ≤ 1/(⟨n⟩⟨1/n⟩) was not checked in this paper. It is often cited to Leggett, J. Stat. Phys. 93, 927 (1998), which was not verified here.

## D. Impurity drag and induced interaction

**24. [VERIFIED]** G. E. Astrakharchik & L. P. Pitaevskii, "Motion of a heavy impurity through a Bose-Einstein condensate," Phys. Rev. A 70, 013608 (2004)
- arXiv: cond-mat/0307247 (v2, 8 Oct 2004)
- DOI: 10.1103/PhysRevA.70.013608 (Crossref: published 20 Jul 2004)
- Fetched: https://api.crossref.org/works/10.1103/PhysRevA.70.013608 ; https://ar5iv.labs.arxiv.org/html/cond-mat/0307247 ; https://arxiv.org/pdf/cond-mat/0307247
- Conventions (verbatim):
  - "g = 4πħ²a/m and gi = 2πħ²b/m are particle-particle and particle-impurity coupling constants"
  - "μ = gn = mc²"
  - ħ and m are kept explicit throughout; neither is set to 1. m is the boson mass, b is the impurity–boson scattering length, and the impurity is infinitely heavy, so the reduced mass is m.
- Momentum cutoff, Eq. (11): "|k| ≤ kmax = 2m(V² − c²)^(1/2)/ħ"
- 3D drag force, Eq. (12): "Thus the energy dissipation takes place only if the impurity moves with a speed larger than the speed of sound. Integration with respect to k, taking into account restriction (11), finally gives"

  **F_V = 4π n b² m V² (1 − c²/V²)²**

  Followed by: "The energy dissipation, Ė = −F_V V, can be evaluated by measuring the heating of the gas. For large V the force is proportional to V²."
- **Check against your formula.** Substitute b = m g_i/(2πħ²):

  F_V = n g_i² m³ (V² − c²)² / (π ħ⁴ V²)

  With ħ = m = 1 this is F = n g²(v² − c²)²/(π v²). **Your formula agrees exactly.** The full-unit prefactor is m³/ħ⁴. Your g corresponds to their g_i = 2πħ²b/m, i.e. the static-impurity coupling.

**25a. [PARTIAL]** A. Klein & M. Fleischhauer, "Interaction of impurity atoms in Bose-Einstein condensates," Phys. Rev. A 71, 033605 (2005)
- arXiv: cond-mat/0407809
- DOI: 10.1103/PhysRevA.71.033605
- Fetched: https://api.crossref.org/works/10.1103/PhysRevA.71.033605 ; https://ar5iv.labs.arxiv.org/html/cond-mat/0407809 ; https://arxiv.org/pdf/cond-mat/0407809
- Quote: "there is a conditional energy shift resulting from the exchange of phonons between the impurity atoms." Eq. (24) is a mode sum with the factor (ε⁰_k/E_k²) cos(k·Δr).
- Text: "For very small distances of the impurities Δ is negative" but "eventually changes its sign".
- **Why PARTIAL:** the word "Yukawa" does not occur in the fetched full text, and the paper reports a sign change in its trapped/box setup. Do not cite it for "Yukawa".

**25b. [VERIFIED]** A. Camacho-Guardian & G. M. Bruun, "Landau effective interaction between quasiparticles in a Bose-Einstein condensate," Phys. Rev. X 8, 031042 (2018)
- arXiv: 1712.06931
- DOI: 10.1103/PhysRevX.8.031042
- Fetched: https://arxiv.org/abs/1712.06931 (journal ref and DOI shown there) ; https://arxiv.org/pdf/1712.06931
- Quote: "There are no retardation effects for zero COM and (5) gives the well-known Yukawa interaction."
- Eq. (7) [rendered math; check prefactor]: f(r) = −(𝒯_v² n₀ m_B/π) e^{−√2 r/ξ}/r, with ξ = (8π a_B n_B)^{−1/2}.
- Relevance: an attractive Yukawa potential whose range is set by the coherence length.

**25c (extra). [VERIFIED]** P. Naidon, "Two impurities in a Bose–Einstein condensate: from Yukawa to Efimov attracted polarons," J. Phys. Soc. Jpn. 87, 043002 (2018)
- arXiv: 1607.04507
- DOI: 10.7566/JPSJ.87.043002
- Fetched: https://api.openalex.org/works/doi:10.7566/JPSJ.87.043002 ; https://arxiv.org/abs/1607.04507
- Quote: "the two impurities form two polarons that interact through a weak Yukawa attraction mediated by virtual excitations."

**26a. [VERIFIED]** P. Gravejat, "A non-existence result for supersonic travelling waves in the Gross–Pitaevskii equation," Commun. Math. Phys. 243, 93–103 (2003)
- arXiv: none found
- DOI: 10.1007/s00220-003-0961-y
- Fetched: https://link.springer.com/article/10.1007/s00220-003-0961-y ; https://api.openalex.org/works/doi:10.1007/s00220-003-0961-y
- Quote: "We prove the non-existence of non-constant travelling waves of finite energy and of speed c > √2 in the Gross-Pitaevskii equation in dimension N≥2." In Gravejat's units, √2 is the sound speed.

**26b. [VERIFIED metadata; quote reconstructed]** C. A. Jones & P. H. Roberts, "Motions in a Bose condensate. IV. Axisymmetric solitary waves," J. Phys. A 15, 2599–2619 (1982)
- Exact title has "condensate. IV." with a period.
- DOI: 10.1088/0305-4470/15/8/036
- Fetched: https://api.openalex.org/works/doi:10.1088/0305-4470/15/8/036 . The IOP page showed a CAPTCHA.
- Quote [reconstructed]: "Axisymmetric disturbances that preserve their form as they move through a Bose condensate are obtained numerically by the solution of appropriate nonlinear Schrodinger equation."
- Relevance: the subsonic family of vortex rings and rarefaction pulses.

---

## Metadata corrections to your list
- **#11:** the published PRD title is "…from a Bose-Einstein-condensation-based analogue spacetime".
- **#15:** the authors are Poli, Baillie, Ferlaino & Blakie (confirmed).
- **#16:** now published as PRA 111, 053305 (2025). It is about 1D supersolids.
- **#9:** a book chapter in the Novello Festschrift (2003, pp. 397–429), not a journal article.
- **#19:** the authors are Saccani, Moroni & Boninsegni.
- **#26b:** the title punctuation is "condensate. IV.".
- **#25:** use Camacho-Guardian & Bruun (or Naidon) for "Yukawa", not Klein & Fleischhauer.
- **Page ranges:** #6 is pp. 150–196, #5b is pp. 249–252, #8 is pp. 2961–2982, #10b is pp. 3129–3154.
- **#7:** the arXiv v4 (Nov 2024) is a newer edition. Cite LRR 8, 12 or LRR 14, 3 explicitly.
