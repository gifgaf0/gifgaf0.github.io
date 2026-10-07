# A1 — Polarization gate: pre-registration (decision rule fixed before any derivation)

**Plain-language summary.** A gravitational wave in general relativity stretches and squeezes space in a "plus" or "cross" pattern (a *tensor* wave). Other theories can produce *vector* or *scalar* waves, which move detector mirrors in different patterns. The LIGO–Virgo detectors have tested which pattern real waves have, and the tensor pattern wins by a huge margin. The ledger says light and gravitational waves travel in the same transverse channel of the vacuum crystal. This file fixes, before any calculation, what that claim must pass: if the channel's wave has no tensor part, the claim fails the polarization test and the ledger's "GW170817 structural pass" is withdrawn.

**Lock.** This file is locked by its md5, recorded in `A1_LOCK.txt` and in the commit that adds it, before `a1_derivation.py` or any derivation text exists. Nothing below may be edited after that commit; corrections go in a dated addendum.

**Base.** `SQT_Master_Ledger_v4_91_CANONICAL.md`, md5 `ce9ca6873adb5686227f5d103b41e3cc` (1,778,302 B), read from the project store on 2026-10-06. Repository `main` at `3587eb3` (PR #37).

**Mode.** Proportionate discipline (author's brief of 2026-10-06): a pre-registered decision rule; a blind second leg only for the step that decides the verdict (the helicity-to-antenna mapping); everything else is annotation. No sealed anchors and no T1 list: the comparison numbers are public, quoted below, and enter only the verdict step.

---

## 1. Question (from the brief, verbatim)

> What polarization content does the transverse line's gravitational-wave channel (S2) present to a detector, and does it survive the LIGO–Virgo polarization tests?

## 2. What the ledger already records (read at V4.91, cited by section, not by line)

- §2.91.O (G-S2C1, V4.80), election E-P2-1(a): under full SO(3) grain averaging a propagating plane wave's strain "carries helicity 0/±1, never pure ±2"; the aggregate S2 channel "is the polarization-averaged shear cone itself".
- §2.91.N (G-CI1, V4.77): F-IRR fires, K = ∅. The instantiated substrate carries no gapless internal helicity-±2 branch; CI-S (the metric perturbation as a substrate ±2 mode) is falsified structurally; the operative branch is CI-W/EM-IN.
- §2.91.Q (G-MSCS1, V4.83): EM and S2 are "two descriptors of the one transverse phonon"; S2-E₂ is the m = ±2 fraction of the transverse-projected strain *about the crystal axis*; S2-h is "the helicity-±1 fraction of the full traceless strain about k̂"; Amendment A-1.1 carries E-P2-1(a) "as the kinematic statement it is (no plane wave carries pure helicity ±2)".
- The GW170817 speed check appears as a "structural pass" at §2.88.E (V4.35), §2.91.B (A-SHEAR, V4.63), §2.91.H (V4.67) and ANNEX-CDEF-1 (iv) (V4.71). The ledger contains no polarization test (zero hits for GW170814, Hellings, and any LVC polarization result).

## 3. Definitions fixed now

- **Helicity** is taken about the propagation direction k̂ of the wave at the detector, in the detector's rest frame (the substrate frame up to v/c ≈ 1.2×10⁻³).
- **Classification by spin weight.** Rotate the wave's polarization about k̂ by an angle ψ, keeping everything else fixed. The detector output R(ψ) of a linear detector is a trigonometric polynomial in ψ. Its terms in cos 2ψ, sin 2ψ are the **tensor** part (helicity ±2: plus, cross); its terms in cos ψ, sin ψ are the **vector** part (helicity ±1: x, y); its ψ-independent terms are the **scalar** part (helicity 0: breathing b, longitudinal l). This is the Eardley–Lee–Lightman–Wagoner–Will classification restated without assuming a metric theory.
- **Equivalent tensor statement.** For a wave described by a symmetric 3-tensor field T_ij (a strain, or a metric-equivalent perturbation built from the wave's fields), the tensor part is the transverse-traceless projection Λ(k̂)T = P T P − ½ P tr(PT), with P = 1 − k̂k̂.
- **Antenna patterns** for an L-shaped interferometer with unit arm vectors u, v: D = ½(u⊗u − v⊗v); the six standard patterns F_A = D:e_A with e_+, e_×, e_x, e_y, e_b, e_l in the conventions of Will, *Living Rev. Relativ.* 17, 4 (2014) and Isi & Weinstein (arXiv:1710.03794). Sign and normalization conventions are stated in the derivation and do not affect classification.
- **Tensor fraction** (reported only if nonzero): f_T = ⟨|R_T|²⟩ / ⟨|R|²⟩, averaged over sky position (uniform on S²) and ψ (uniform), for an L-shaped detector with the wave's amplitude normalized to unit strain-equivalent.

## 4. Decision rule (the author's, adopted verbatim)

> If the S2 response has no tensor component:
> - the reading "the spin-2 radiative sector shares the transverse channel" is FALSIFIED by GW170817's polarization test;
> - the GW170817 "structural pass" is withdrawn wherever it appears;
> - the transverse line keeps only the EM carrier.
>
> If there is a tensor component, report its fraction and run the comparison.

**Operational test for "no tensor component".** The S2 response has no tensor component if the tensor part defined in §3 vanishes identically at linear order in the wave amplitude, for every propagation direction and every polarization, in the substrate's untextured aggregate (the medium of record for the transverse line). A tensor part that is nonzero but bounded (for example by texture or by the detector's motion through the substrate) is reported as a fraction with its bound and is **not** "no tensor component"; in that case the comparison arm (§5) runs on the fraction.

**Comparison anchors (public; verified 2026-10-06; they enter only the verdict step):**
- GW170817, sky position fixed to NGC 4993, three detectors: log₁₀ Bayes factor of pure tensor over pure vector **+20.81 ± 0.08**, over pure scalar **+23.09 ± 0.08** (LVC, *Tests of General Relativity with GW170817*, PRL 123, 011102 (2019), arXiv:1811.00364). The vector and scalar hypotheses replace the antenna patterns and keep the GR phase model.
- GW170814 (first three-detector event): Bayes factors above 200 (vector) and 1000 (scalar) for pure tensor (LVC, PRL 119, 141101 (2017), arXiv:1709.09660).
- With waveforms whose inclination dependence matches vector or scalar radiation (not GR's): ln B(tensor/vector) = 21.078 and ln B(tensor/scalar) = 44.544 for GW170817, rising to 51.043 and 60.271 with the jet-inclination prior (Takeda, Morisaki & Nishizawa, PRD 103, 064037 (2021), arXiv:2010.14538; natural logarithms).
- GWTC-3: no evidence for non-tensor polarizations, pure or mixed (LVK, arXiv:2112.06861; summary arXiv:2204.00662).

## 5. Robustness items fixed now (they test the rule's scope; they cannot reverse it)

- **R-1, inventory.** Check every excitation of the 16-component substrate (lattice displacement branches and internal L_⊥ branches) for a helicity-±2 source at linear order.
- **R-2, admixture on the cone.** A vector+scalar mixture is not excluded by three detectors in full generality. Determine whether any scalar (helicity-0) branch of the substrate propagates at c_T. A branch off the c_T cone cannot accompany a signal that arrived within 1.7 s of its gamma-ray counterpart after ~40 Mpc; then the on-cone signal is pure vector and the pure-vector comparisons above apply as stated.
- **R-3, bounded admixtures.** Bound any tensor admixture from (a) texture of the aggregate, (b) the detector's motion relative to the substrate, (c) second order in the wave amplitude.

## 6. Secondary arms (structural only, no decision weight)

- **S-1, binary radiation.** Multipole structure of helicity-±1 radiation from a bound binary: when dipole terms appear, the quadrupole coefficient, and what the double pulsar (Kramer et al., PRX 11, 041050 (2021): GR quadrupole emission confirmed to 1.3×10⁻⁴, 95 %) can and cannot test.
- **S-2, pulsar timing.** Earth-term overlap reduction functions for the derived modes, against Hellings–Downs; NANOGrav 15-yr: HD correlations favoured over an uncorrelated common process with Bayes factor 200–1000, p = 5×10⁻⁵ to 1.9×10⁻⁴ (ApJL 951, L8 (2023)); its polarization search covered transverse modes only (HD vs scalar-transverse, Bayes factor ≈ 2; ApJL 964, L14 (2024)).

## 7. Second leg (blind)

An independent agent derives the helicity-to-antenna mapping without access to this leg's derivation: (i) the TT content of the strain of a plane displacement wave of arbitrary polarization; (ii) the response of an L-shaped interferometer to that strain, projected on the six standard patterns over the sky; (iii) the ψ-spin-weight of the response. **Agreement criterion:** identical classification, and numerical agreement of the projected coefficients to ≤ 10⁻¹⁰ on a common sky grid (or exact symbolic identity). A disagreement halts the verdict and is resolved by a third derivation before anything is folded.

## 8. Blast radius (pre-declared; extended by grep at verdict time)

Annotate, in the same fold, every entry that leans on the GW pass or on c_GW = c_EM by carrier identity: §2.88.E (GW170817 reframe), §2.91.B (A-SHEAR), §2.91.H (the "A-SHEAR/transverse statements ... the GW170817 structural pass ... continue" clause), §2.91.I Q3 item (1), ANNEX-CDEF-1 (iii)–(iv), and the A-SHEAR consonance; plus every further entry the verdict-time grep finds (GW170817, c_GW, carrier identity, spin-2, S2, tensor-vs-EM, GW-side windows).

## 9. What this pre-registration does not do

It does not evaluate any magnitude, fix any coupling, or touch §2.52 Open 3. It does not assume a metric theory. It does not decide anything about the EM carrier itself (CI-W/EM-IN), which the rule leaves standing.
