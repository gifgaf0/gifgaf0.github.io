# Lattice-spacing bound: pre-registration (October 7, 2026)

**Plain-language summary.** Light in this model is a shear wave in a polycrystalline vacuum. Grains scatter it, and the loss grows as the fourth power of the photon energy and the cube of the grain size. Photons that reach us therefore cap the grain size. This file fixes, before any number is computed:
- which photons are used;
- how much loss counts as "excluded";
- which birefringence limit is used;
- how the results are combined.

From the grain-size cap d_max, the largest lattice spacing that still fits N cells in a grain is a_max(N) = d_max/N. The comparison with the Planck length and with the ledger's declared lattice band is done last, by a separate script.

**What this is.** A bound ("the data require a ≤ …"), computed on base V4.94 (md5 708df4cf8f4703088c89b4fad96584bd) under the author's brief of October 7, 2026. It is not a verdict on anything already decided. No scale (ξ, a or d) is pinned, re-pinned or elected here. The Planck length ℓ_P is used as a unit and as a reference line only.

## 1. Inputs (md5-asserted at every run)

| Input | File | md5 | What is read |
|---|---|---|---|
| Anchor of record | `gci1_gate/embeds/anchors_G_CI1_SEALED.md` | dd8fe2d364624750201ad9c9ffef575c | TR-4 row (E_ref, E_alt, z, τ_r, R2/R3) |
| Fluctuation factor | `gci1_gate/ci1_phase2_cc.json` | f79113b7664addc9b1d96893aa883cbf | Q_T_a, Q_T_a_banked, eps_T per configuration |
| Lattice dispersion | `gs2c1_gate/cc_phase4.json` | 4ebd0db2e2a494db3e66d35f90df7422 | a₂ (Γ–K, Γ–M) and CIs |
| Texture birefringence | `gmscs2_gate/g_mscs2_chatleg_checkpoint.json` | 1c5b6b59829d2a6b9ae2b1a7a016832d | biref_b1_VRH per key |

**Values.** These are restated here, so that a second leg can compute from this file alone:
- **Q_T^a** (G-CI1 Phase 2; banked values in brackets):
  - hex:step 0.035190738866 [0.03519074];
  - hex:gem8 0.050020548479 [0.05002055];
  - cubic:step 0.054077628247 [0.05407763];
  - cubic:gem8 0.075494302071 [0.0754943].
- **ε_T**: 0.091333902531, 0.10912048635, 0.1303772679 and 0.15743361577, in the same order.
- **a₂** (G-S2C1 Phase 4, per (ka)², a = the p6m lattice constant):
  - Γ–K −0.0132447218611613 (CI 3.21×10⁻⁵);
  - Γ–M −0.020633674570357804 (CI 3.55×10⁻⁵).
- **b₁** (G-MSCS2, per unit t₄):
  - hex_step|a 0.01624085410723511;
  - hex_step|b 0.016241797577228063;
  - hex_gem8|a 0.01817488251117739;
  - hex_gem8|b 0.018174297109340813;
  - cubic_step −0.03789870339598654;
  - cubic_gem8 −0.04548125222774924 (|001 and |111 are identical).

**Constants.**
- ħ = 1.054571817×10⁻³⁴ J s; c = 299 792 458 m/s; e = 1.602176634×10⁻¹⁹ C; k(E) = E·e/(ħc).
- pc = 3.0856775814913673×10¹⁶ m.
- ℓ_P = 1.616255×10⁻³⁵ m and E_Pl = 1.220890×10¹⁹ GeV (CODATA 2018).
- h = 2πħ, used for λ = hc/E.

**Cosmology** (the anchor's CONV convention):
- flat ΛCDM with H₀ = 67.4 km s⁻¹ Mpc⁻¹ and Ω_m = 0.315, radiation neglected;
- H(z) = H₀√(Ω_m(1+z)³ + 1 − Ω_m);
- the light-travel distance is D_lt(z) = c∫₀^z dz′/[(1+z′)H(z′)], integrated to ≤ 10⁻¹⁰ relative, with an independent quadrature as a cross-check.

## 2. The grain-scattering condition (restated)

- **Attenuation.** Amplitude attenuation α = Im k of the transverse (light) mode in the Rayleigh regime, from the G-POLY1 / G-CI1 machinery (Stanke–Kino / Weaver class, Voigt reference medium):
  - α·d = Q_T^d·(kd)⁴, with Q_T^d = Q_T^a/8 (erratum H-6; d = 2 × the correlation radius of the exponential two-point function);
  - so α = Q_T^d k⁴ d³.
- **Fluctuation factor.** It is the covariance ⟨C⊗C⟩ − ⟨C⟩⊗⟨C⟩ of the G-TSH4-lineage single-crystal tensors over orientations, contracted as in G-POLY1. Written through the scalar fluctuation strength, α = c_geo ε_T² k⁴ d³ with c_geo = Q_T^a/(8ε_T²). c_geo is reported as a restatement and not used.
- **Exclusion.** A grain diameter d is excluded on an arm when α·D > τ_r for every reading of that arm (§3), with **τ_r = 1** (the anchor's P-TRANS threshold, amplitude convention).
  - **R4 band:** τ_r × 10 and × 0.1, reported for the combined bound.
  - The intensity convention (2αD ≤ 1) lies inside that band.
- **Closed form.** d_max = [τ_r / (Q_T^d k⁴ D)]^(1/3).
- **Rayleigh and validity checks**, on every arm and configuration, at the arm's largest wavenumber and its bound of record:
  - x = k·d_max ≤ 10⁻⁴, the regime where the G-CI1 machinery's α_d = Q_T^d x⁴ holds exactly;
  - ε_T·x ≤ 1;
  - Q_T(x)·x³ ≤ 0.10;
  - ε_T² ≤ 0.10.
  A failed check marks that cell VOID and drops it from the minimum.
- **Lattice continuum check:** k·(d_max/N) ≪ 1 at every N, reported.
- **Aggregate RVE check:** (λ/d_max)³ grains per wavelength cube, reported.

## 3. Photon arms and readings

**Per-arm rule.** For each arm, d_max is computed for every combination of its readings:
- E ∈ {E_ref, E_alt};
- D ∈ {D_ref, D_alt};
- for z > 0, k ∈ {k_obs, (1+z)·k_obs}, the anchor's R2.

An arm excludes d only if every reading excludes it (the anchor's R3 logic). The arm's **bound of record** is therefore the largest d_max over its readings. By monotonicity this is (E_alt, D_alt, k_obs), and the code asserts that. The **reference reading** (E_ref, D_ref, k_obs) is reported beside it.

**Configurations.** Every arm is computed on all four configurations. The value of record is the union edge, i.e. the largest d_max over configurations (expected to be hex:step, the smallest Q_T^a; asserted). Per-configuration values are reported.

| Arm | Source | z | E_ref | E_alt (rule) | D_ref | D_alt (rule) |
|---|---|---|---|---|---|---|
| **A0** anchor (TR-4) | 1ES 1101-232, H.E.S.S. (Nature 440, 1018) | 0.186 | 2.916 TeV (highest bin mean, 1.6σ) | 0.733 TeV (highest bin ≥ 3σ; sealed row) | D_lt(0.186) | = D_ref |
| **A1** Crab | LHAASO KM2A: event 1.12 ± 0.09 PeV; VLBI 1.90 (+0.22/−0.18) kpc | 0 | 1.12 PeV | 0.94 PeV (E_ref − 2σ_E) | 1.90 kpc | 1.54 kpc (D_ref − 2σ_D,low) |
| **A2** Cygnus (catalogue check) | LHAASO Sci. Bull. 69, 449 (2024): 8 events > 1 PeV vs 0.75 background; up to 2.5 PeV; Cygnus-X ≈ 1.4 kpc; 6° ≈ 150 pc | 0 | 2.5 PeV | 1.0 PeV (the population threshold) | 1.40 kpc | 1.25 kpc (D_ref − 0.15 kpc, the bubble's near edge) |
| **A3** GRB 221009A | LHAASO KM2A (Sci. Adv. 9, eadj2778): highest event 12.5 +3.2/−2.4 TeV | 0.151 | 12.5 TeV | 7.7 TeV (E_ref − 2σ_E,low) | D_lt(0.151) | = D_ref |
| **A4** Mrk 501 (most constraining distant TeV source documented) | HEGRA 1997 (A&A 349, 11): highest bin 19–24 TeV, 40 excess on 13 background (3.7σ nominal); "highest recorded photon energies being 16 TeV or more" | 0.034 | 21.45 TeV (bin energy) | 16 TeV (the paper's own floor) | D_lt(0.034) | = D_ref |

**Readings reported only** (they never enter a minimum):
- A3 at 17.8 TeV (log-parabola) and 13 TeV (abstract);
- A2 at the Cyg OB2 Gaia distance of 1.6 kpc;
- A1 at the classic 2.0 kpc.

**Anchor reproduction (halt-on-fail).** A0's hex:step bound of record must reproduce W^EM_∪ = 3.7641664288×10⁻³³ m to ≤ 10⁻⁷ relative, with both the Phase-2 and the banked Q_T^a. Both deviations are reported.

**Combined bound.** d_comb is the minimum over arms A0–A4 of each arm's bound of record. The **decisive arm** is the arm attaining it. The R4 variants are d_comb × 10^(1/3) and × 10^(−1/3).

## 4. The table

a_max(N) = d_max/N, for N ∈ {20, 100, 1000}, on every arm (bound of record), in metres and in units of ℓ_P. Combined row: d_comb/N, plus its R4 ×10 (robust) variant.

## 5. Texture

**Birefringence limits.**

| Reading | Δn_max = |v₊ − v₋|/c | Source | Scope |
|---|---|---|---|
| **R-T1 (of record)** | 2×10⁻³⁷ | Kostelecký & Mewes 2006, σ < 10⁻³⁷ (GRB 930131, GRB 960924); Δv = 2σ | along the GRB sightlines |
| R-T2 (conservative) | 4×10⁻³² | KM 2002 level 2×10⁻³², read permissively as σ ≤ 2×10⁻³² | cosmological sources, any orientation at that level |
| R-T0 (reported) | 2×10⁻³⁸ | KM 2006, GRB 021206 (disputed polarization) | one sightline |

**Bound.** t_max = Δn_max/|b₁| for each b₁ key. The headline is the smallest |b₁| (the most permissive), with the cubic and hex values each reported. b₁ is defined for propagation perpendicular to the fiber axis. On other sightlines the split carries an angular factor of order one that vanishes along the axis. R-T1 therefore bounds a texture whose axis is not aligned with both GRB sightlines, while R-T2 holds for any orientation. The bound does not involve a. A bound on the hex l = 2 texture t₂ would need its first-order coefficient, which is not banked, so it is not computed.

**Statistical texture of randomly oriented grains.** A finite sample of M independent random grains has a net texture of standard deviation σ_t(M) = √(c/M), with c = 1/⟨K̃₄²⟩ = 21/4 (cubic) or 1/⟨P₄²⟩ = 9 (hex). Here M = V/d³. Reported:
- (i) M_min = c/t_max² (R-T1, per family), and the cube side L_min = d·M_min^(1/3) over which random grains average below t_max;
- (ii) σ_t over the first Fresnel volume V_F = πλD²/6 of a representative polarimetry path, with E = 100 keV (λ = hc/E) and D = 1 Gpc;
- (iii) the ratio t_max/σ_t.

Each is evaluated at d = 3.7641664288×10⁻³³ m (the largest grain size on record) and at d = d_comb.

## 6. Dispersion

**No dimension-5 term.**
- The light carrier is the shear phonon of a centrosymmetric crystal: p6m in 2D, and the AB/hcp stack (P6₃/mmc) in 3D.
- With finite-range interactions the dynamical matrix is analytic in k, and inversion makes ω² even in k. So ω/k − c starts at O(k²): no term linear in E, and no linear (natural optical-activity) birefringence, which needs broken inversion.
- A random aggregate of centrosymmetric grains inherits this.
- The record agrees: G-S2C1 fitted {(ka)², (ka)⁴} on ka ∈ [10⁻³, 0.3] with verdict A3 DISPERSIVE-O(k²).
- This is a symmetry statement. No new number decides it.

**Quadratic bound.** The lattice gives E = pc[1 + a₂(ka)²], so E² = p²c²[1 + 2a₂(ka)²]. LHAASO's E² ≃ p²c²[1 − s(E/E_QG,2)²] with s = +1 (subluminal, a₂ < 0) then gives (E/E_QG,2)² = 2|a₂|(ka)², with k = E/(ħc). Hence
- a_max^disp = ħc / (E_QG,2,min · √(2|a₂|)).

The group-velocity form, 3|a₂|(ka)² = (3/2)(E/E_QG,2)², gives the same relation.

| Choice | Reading of record (permissive) | Also reported |
|---|---|---|
| E_QG,2,min | 6.9×10¹¹ GeV (subluminal, LHAASO Summary) | 6×10⁻⁸ × 1.220890×10¹⁹ GeV (abstract) |
| \|a₂\| | 0.0132447218611613 (Γ–K) | 0.020633674570357804 (Γ–M) |

The a₂ values are the 2D single-crystal ones. No 3D-stack value is on record, and a_max^disp scales as |a₂|^(−1/2).

## 7. Combine

a_max(N) = min(d_comb/N, a_max^disp) for N ∈ {20, 100, 1000}. Steps 2–7 are computed by `ls_leg1.py` (one leg) and written to `ls_leg1.json` before the comparison script exists.

## 8. The comparison (last; separate script `ls_compare.py`)

Reading only `ls_leg1.json`, report, per arm and combined:
- **EMPTY_P(N)** ⇔ a_max(N) < ℓ_P (the window needs cells finer than the Planck length);
- **EMPTY_D(N)** ⇔ a_max(N) < 1.899×10⁻³⁴ m (the declared band's lower edge: the declared chain's cells do not fit);
- N_P = d/ℓ_P and N_D = d/(1.899×10⁻³⁴ m), the largest cells-per-grain at a = ℓ_P and at the band's lower edge;
- where ℓ_P and the declared band [1.899, 7.588]×10⁻³⁴ m fall relative to a_max(N);
- the same for the R4 ×10 variant.

## 9. Second leg

**Trigger.** The second leg runs if the combined bound is EMPTY_P or EMPTY_D at N = 20. Since a_max falls with N, that means at every N ≥ 20. This union of the two readings of "empty" contains the brief's literal condition ("empty for every N ≥ 20 on every arm").

**Protocol.**
- A blind subagent receives this file only, and no leg-1 code or numbers. It computes every arm's d_max at every reading and configuration, the combined bound and decisive arm, a_max^disp, and t_max, and returns them as JSON.
- The comparator `ls_twoleg_compare.py` is frozen (committed) before leg 2 returns.
- **PASS** requires:
  - relative deviation ≤ 10⁻⁶ on every d_max, a_max^disp and t_max;
  - the same decisive arm;
  - identical EMPTY_P/EMPTY_D flags at N = 20, 100 and 1000.
- A miss is reconciled and recorded before any fold.

## 10. Scope

- **This file decides nothing already decided.** The result is a bound recorded in one short fold. That fold carries pointers on:
  - the light-only transverse carrier (§2.92.A/E);
  - the polycrystal-floor Part VI row;
  - the ANNEX-SC-1 / G-S2C1-W chain (§2.91.H; the G-S2C1-W row);
  - W^EM_∪ (§2.91.N);
  - and, for the texture bound, the b₁ source (§2.91.S) and the unopened first-order polarization-split successor (§2.91.T, E-SA-1(b)).
- **It does not touch** the A1 polarization verdict, the A2 internal-mode friction, the second-sound drag or KC-EP.
- **N is not elected here.** The polycrystal-floor options go to the author.

## 11. Honesty register

- **H-LS-1.** Known before this file was written:
  - the brief's expectations (the Crab arm shrinks the window by about 40–2,000; a ≲ 10⁷ ℓ_P from dispersion);
  - V4.94's P2 facts (the anchor edge is 4.96–19.82 cells under the declared chain);
  - the LS-0 reproduction of W^EM_∪;
  - the Prior Address quotations.

  Candidate sources were ranked by E⁴·D, the brief's own scaling, using documented energies and redshifts only. No arm d_max, table entry, texture bound or dispersion bound was computed before this file was committed.
- **H-LS-2.** A2 (Cygnus) is a fifth arm added by the catalogue check that the brief asked for. It enters the minimum like the four named arms.
- **H-LS-3.** R-T2's factor-of-two ambiguity (a coefficient magnitude versus σ) is resolved permissively.
- **H-LS-4.** The D_alt and E_alt rules (2σ downward; the near edge of an extended source; a paper's own floor statement) are uniform choices made to keep the bound conservative. Each is stated in its row.
