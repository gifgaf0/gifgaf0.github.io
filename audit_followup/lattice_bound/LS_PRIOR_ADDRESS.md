# Lattice-spacing bound: Prior Address (October 7, 2026)

**Plain-language summary.** Before computing anything, this file records what the literature already says on the four questions the brief named.
- **How many lattice cells a grain needs.** The polycrystal theories the ledger uses (Stanke & Kino; Ranganathan & Ostoja-Starzewski) treat each grain as a smooth crystal. They say how many *grains* an averaging volume needs, not how many *cells* a grain needs. Atomistic work on nanocrystalline copper answers the second question: grains of about 9–37 cells are 15–27 % too soft, because 30–50 % of their atoms sit in grain boundaries. Grains of about 55 cells or more (20 nm in copper) are within a few percent of bulk.
- **LHAASO's highest-energy Galactic photons.** The Crab Nebula has an event at 1.12 ± 0.09 PeV, about 1.9 kpc away. The Cygnus region has a 1.4 PeV photon, and the Cygnus "bubble" has 8 events above 1 PeV against 0.75 expected background, about 1.4 kpc away.
- **Distant sources.** GRB 221009A (z = 0.151) has photons up to about 13 TeV. Among distant TeV sources, the strongest documented case by the brief's own measure (E⁴ × distance) is Mrk 501 (z = 0.034), whose 1997 HEGRA spectrum reaches the 19–24 TeV bin.
- **Vacuum birefringence.** Gamma-ray-burst polarization limits the velocity split between the two light polarizations to about 2 × 10⁻³⁷ along the burst sightlines (Kostelecký & Mewes 2006). Spectropolarimetry of distant galaxies limits it to about 10⁻³² (their earlier work).
- **LHAASO's quadratic Lorentz-violation bound.** It is E_QG,2 > 6 × 10⁻⁸ E_Pl, or 6.9 × 10¹¹ GeV for slower-than-light photons, using LHAASO's stated velocity convention.

Nothing below is computed. The arms, readings and thresholds built on it are fixed in `LS_PREREG.md`.

## 1. Homogenization and the representative volume element

**Already cited in the ledger** (V4.73 record and the Part V VRH row): Stanke & Kino, JASA 75, 665 (1984); Weaver, JMPS 38, 55 (1990); Ranganathan & Ostoja-Starzewski, PRL 101, 055504 (2008) (the universal anisotropy index A^U). The V4.73 record states the falsifier surface in the brief's words: "Rayleigh-regime grain scattering α ∝ k⁴d³⟨(δC/C)²⟩ (Stanke–Kino 1984; Weaver 1990) with the fluctuation factor now FIXED by the G-TSH4 measurements".

**What these works address.**
- **Stanke & Kino.** Their unified theory, and the FOSA/SK–Weaver operator class pinned by G-POLY1 (with He, arXiv:1710.03828, as the cross-source), treats each grain as a homogeneous anisotropic continuum. It gives the Rayleigh law α ∝ k⁴d³ for kd ≪ 1. It is the machinery behind W^EM_∪.
- **Ranganathan & Ostoja-Starzewski.** In the 2008 dissertation (Ranganathan, "Scale-Dependent Homogenization and Scaling Laws in Random Polycrystals", UIUC; summary page read) and the companion JMPS paper, the representative volume element is reached through a scaling function of "a mesoscale (scale of observation relative to grain size)" and the anisotropy index A^U. A material-selection diagram then gives "the size of RVE for a whole range of polycrystals". The numerical RVE sizes are in the restricted full text and were not retrieved. This is the **grain → aggregate** level: how many grains an averaging volume needs.
- **What follows for this brief.** In the Rayleigh regime a wave averages over (λ/d)³ grains per wavelength cube. At the arms' energies and grain sizes that is far more than any RVE criterion asks; LS_PREREG §3 records the check. Neither work addresses the **cell → grain** level: how many lattice cells a grain needs before it behaves as a bulk crystal with the single-crystal tensor that G-POLY1 consumed.

**The cell → grain level: atomistic nanocrystals.**
- **Schiøtz, Di Tolla & Jacobsen, Nature 391, 561 (1998)** (author summary page, "Softening of nanocrystalline metals at very small grain sizes"):
  - "Each sample contains 8 to 64 grains in a 10.6nm cube of material, resulting in grain sizes from 3.3 to 6.6 nm."
  - "a Young's Modulus around 90-105GPa (increasing with increasing grain size)", against "124 GPa in macrocrystalline Cu";
  - "a significant fraction (30-50%) of the atoms are in the grain boundaries".
- **Schiøtz, Vegge, Di Tolla & Jacobsen, Phys. Rev. B 60, 11971 (1999)** (arXiv:cond-mat/9902165):
  - grain sizes 3.28, 4.13, 5.21, 6.56 and 13.2 nm;
  - "The low value is due to the large volume fraction of the atoms being in the grain boundaries";
  - the reduction "will be difficult to detect experimentally due to the much lower volume fraction of atoms in the grain boundaries for typical grain sizes in high-quality samples (>∼ 20 nm)";
  - experiments on larger grains show "a reduction in Young's modulus of at most a few percent when correcting for the remaining porosity".
- **In lattice cells** (fcc Cu, a = 0.3615 nm): 3.3–13.2 nm is about 9–37 cells (15–27 % soft, 30–50 % of atoms in boundaries). 20 nm is about 55 cells (at most a few percent soft).
- **Scaling.** For boundaries of fixed thickness δ, the boundary volume fraction falls as about 3δ/d, that is as 1/N. Taking δ as one to three cells, it is about 3–9/N: 15–45 % at N = 20, 3–9 % at N = 100 and 0.3–0.9 % at N = 1000. This is an order-of-magnitude reading of the literature, used only to lay out the author's options.

**The ledger's own floor.** G-CI1 registered "Substrate floor | d ≥ N_cell·a with N_cell = 10 in substrate units; **not converted to SI** (§3.3)". Its reason was that "ξ = ℓ_P for the transverse sector" is not licensed.

**Supported floor.** Grains behave as bulk crystals to within a few percent from about **N ≈ 50–100** cells per grain. At N ≈ 10–40 the continuum-grain description is off by 15–30 %. The choice of N stays with the author.

## 2. LHAASO's PeV sources

- **Crab Nebula.** LHAASO, Science 373, 425 (2021): spectrum to 1.1 PeV. As quoted in LHAASO, arXiv:2204.02956: "The most energetic event of 1.12±0.09 PeV was registered", with |δE_γ,max| = 0.09 PeV. Distance: the VLBI parallax gives 1.90 (+0.22/−0.18) kpc (Lin et al., ApJ 2023, arXiv:2306.01617).
- **Twelve UHE sources.** LHAASO, Nature 594, 33 (2021), from the CAS release of May 17, 2021: "LHAASO also detected 12 stable gamma ray sources with energies up to about 1 PeV", "including one at 1.4 PeV", and "Photons with energies exceeding 1 PeV were detected in a very active star-forming region in the constellation Cygnus". No energy uncertainty is given there for the 1.4 PeV photon.
- **The Cygnus bubble.** LHAASO, Sci. Bull. 69, 449 (2024), arXiv:2310.10100:
  - "a γ-ray bubble spanning at least 100 deg2 in ultra high energy (UHE) up to a few PeV";
  - "There are 8 events with energy above 1 PeV, whileas the background is only 0.75";
  - the spectrum "gradually increases with energy at least up to 2 PeV without indicating a sharp cutoff";
  - Cygnus-X is "at a distance ≈1.4 kpc", and the 6° radius corresponds to "about 150 pc".
  The IHEP release on the published paper gives photons "with the highest energy reaching 2.5 PeV". The Gaia distance to Cyg OB2 is "1.6 kpc with a standard deviation of 0.1 kpc", with "A systematic error of ±0.1 kpc" (Berlanas et al., arXiv:1909.03809).
- **Not retrieved.** The first LHAASO catalogue (ApJS 271, 25 (2024)) was refused by the fetch tool in this session. As far as the session knows it lists significances above 100 TeV, not photon maxima. The source maxima above come from the papers named.
- **Ranking.** By the brief's scaling d_max ∝ (E⁴D)^(−1/3), the Cygnus region and the Crab are the candidates for the decisive Galactic arm. Both are pre-registered.

## 3. GRB 221009A

- **KM2A.** LHAASO, Sci. Adv. 9, eadj2778 (2023), arXiv:2310.08845: "the detection of gamma-rays up to 13 TeV"; "a measured redshift of z=0.151"; "KM2A covers the energy range from 3 TeV to 20 TeV".
- **The highest-energy event** depends on the spectral model:
  - "17.8 +7.4 −5.1 TeV" (log-parabola);
  - "12.2 +3.5 −2.4 TeV" (power law with exponential cutoff);
  - "12.5 +3.2 −2.4 TeV" (the EBL-attenuation model);
  - "eight events with reconstructed energy above 10 TeV".
- **WCDA** photons span 0.2–7 TeV (LHAASO, Science 380, 1390 (2023), as restated in the LIV paper below).
- **Not used.** Carpet-2's claimed 251 TeV event is not LHAASO and is unconfirmed.

## 4. The most constraining distant TeV source

- **Mrk 501, z = 0.034.** HEGRA, 1997 outburst: Aharonian et al., A&A 349, 11 (1999), astro-ph/9903386.
  - "From 500 GeV to 24 TeV the differential photon spectrum is well approximated by a power-law with an exponential cutoff";
  - "In the highest energy bin (19 TeV to 24 TeV) 40 excess events are found above a background of 13 events", a nominal 3.7σ, with the caveat "due to the steep spectrum in this energy range, a part of these events may represent a spill-over from lower energies";
  - "the highest recorded photon energies being 16 TeV or more";
  - energy resolution "15% to 20%". The table's bin energy is 21.45 TeV.
- **Ranking.** By E⁴·D, Mrk 501 at 16–21 TeV and 0.15 Gpc outranks GRB 221009A at 8–13 TeV and 0.6 Gpc, and both outrank the 0.73–2.9 TeV anchor at 0.73 Gpc. The candidate ranking used only documented energies and redshifts; no d_max was computed.
- **LHAASO's long-term Mrk 501 study** (ICRC2025, PoS 501, 883) gives a cutoff fit "E_cut = 9.51 ± 1.44 TeV" and no maximum photon energy.
- **Not retrieved:** HAWC's Mrk 421/501 spectra and 1LHAASO's KM2A blazar entries.

## 5. Vacuum birefringence

- **Kostelecký & Mewes, PRL 97, 140401 (2006)** (hep-ph/0607084):
  - GRB 930131 and GRB 960924 polarization "constrain certain types of relativity violations in photons to less than parts in 10^37";
  - per source, log₁₀ σ < −37, and log₁₀ σ < −38 for GRB 021206;
  - v±/c = 1 + ρ ± σ, so the velocity split is 2σ, and Δφ ≃ 2σ L_eff E;
  - the earlier level: "Their magnitudes are currently bounded at the level of 10^-32 by observations of polarized light" from galaxies at about 1 Gpc.
  - Each GRB constrains σ along its own sightline.
- **Kostelecký & Mewes, PRD 66, 056005 (2002)** (hep-ph/0205211): "The comparative spectral polarimetry of light from cosmologically distant sources yields stringent constraints of 2×10−32".
- **Kostelecký & Mewes, PRL 110, 201601 (2013)** (arXiv:1301.5367): GRB polarization constrains coefficients for d = 4–9, "improves existing sensitivities … by factors ranging from ten to a million", with Δv = 2E^(d−3)|ς^(d)a|. No d = 4 number was retrieved.
- **Caveat.** The GRB polarization detections behind 10⁻³⁷ and 10⁻³⁸ are marginal (BATSE) or disputed (RHESSI, GRB 021206).
- **Relevance.** A textured aggregate is a uniform anisotropic medium for the shear (light) mode. In the long-wavelength regime its birefringence does not depend on frequency, which is the dimension-4, CPT-even birefringent class these bounds constrain.

## 6. LHAASO's quadratic Lorentz-violation bound

- **The bound.** LHAASO, PRL 133, 071501 (2024), arXiv:2402.06009, from GRB 221009A: "E_QG,1 > 10 times of the Planck energy E_Pl for the linear" and "E_QG,2 > 6 × 10⁻⁸ E_Pl for the quadratic LIV effects". The Summary gives E_QG,2 > 6.9 × 10¹¹ GeV for the subluminal case and 7.0 × 10¹¹ GeV for the superluminal case.
- **Convention.** E² ≃ p²c²[1 − Σ s (E/E_QG,n)ⁿ] and v(E) ≈ c[1 − s (n+1)/2 (E/E_QG,n)ⁿ], with s = +1 subluminal. The photons are 0.2–7 TeV, and the CCF median energies run from 0.354 to 1.601 TeV.
- **Relevance.** The lattice's banked dispersion is subluminal (a₂ < 0, G-S2C1), so the subluminal bound applies. The linear bound needs a term odd in k, which a centrosymmetric lattice does not have (LS_PREREG §6).

## 7. The anchor of record

G-CI1 TR-4: 1ES 1101-232, z = 0.186 (H.E.S.S., Aharonian et al., Nature 440, 1018 (2006)). E_ref = 2.916 TeV is the mean of the highest bin (1.6σ); E_alt = 0.733 TeV is the mean of the highest bin at ≥ 3σ. "exclusion only if excluded under BOTH E readings (R3); k = E/(hbar*c); D_ref = D_lt(0.186); tau_r = 1.0". This was read from `gci1_gate/embeds/anchors_G_CI1_SEALED.md` (md5 dd8fe2d364624750201ad9c9ffef575c, census 12, asserted at open). These anchors were unsealed at each G-CI1 leg's Phase-3 mapper in August, so reading them now breaks no seal.

*Sources were fetched in this session, except the two marked "not retrieved". Quotations are as returned by the fetch tool.*
