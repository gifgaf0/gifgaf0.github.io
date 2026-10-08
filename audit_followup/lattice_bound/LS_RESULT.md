# Lattice-spacing bound: result (October 7, 2026)

**Plain-language summary.**
- **The grains must be at most about the Planck length.** The light reaching us from the highest-energy sources caps the grain size of a polycrystalline vacuum at 2.1 × 10⁻³⁵ m, which is 1.28 Planck lengths. The cap comes from LHAASO's PeV photons from the Cygnus region and the Crab Nebula, which agree to 1.3 %. It is 181 times tighter than the old window, which used a sub-TeV source.
- **So the cells must be finer than the Planck length.** A grain of N lattice cells needs a lattice spacing a ≤ 2.1 × 10⁻³⁵ m / N:

  | Cells per grain, N | Largest lattice spacing a | In Planck lengths |
  |---|---|---|
  | 20 | 1.0 × 10⁻³⁶ m | 0.064 ℓ_P |
  | 100 | 2.1 × 10⁻³⁷ m | 0.013 ℓ_P |
  | 1,000 | 2.1 × 10⁻³⁸ m | 0.0013 ℓ_P |

  At a Planck-length lattice, a grain could hold one cell. Even allowing ten times more scattering loss than the threshold, it could hold two.
- **The ledger's declared lattice does not fit.** That lattice (12–47 Planck lengths per cell) is 9 times larger than the largest allowed grain.
- **Grain alignment.** Any net alignment of the grains (texture) must be below about 10⁻³⁵ along the gamma-ray-burst sightlines, or 10⁻³⁰ in any direction. Randomly oriented grains satisfy this with more than 30 orders of magnitude to spare, so the bound only constrains a coherent, large-scale alignment.
- **Dispersion.** The lattice's own dispersion gives only a ≲ 10⁸ Planck lengths, so it never binds.
- **Checks.** Two independent computations agree to 5 × 10⁻¹⁵.

This is a bound ("the data require …"), not a prediction and not a verdict on anything already decided. No scale was pinned or re-pinned. Choosing the minimum cells per grain, N, stays with the author.

## The bound by arm

The rules were fixed in `LS_PREREG.md` (locked at `65404f5`) before anything was computed:
- an arm excludes a grain diameter d when the amplitude optical depth α·D exceeds 1 under every reading of that arm;
- the attenuation is α = (Q_T^a/8)·k⁴d³;
- each arm's bound of record is its most permissive reading (the lower energy, the shorter distance, the observed wavenumber), on the most permissive configuration (hex:step).

| Arm | Source (reading of record) | d_max (m) | d_max (ℓ_P) | a_max, N = 20 | a_max, N = 100 | a_max, N = 1,000 |
|---|---|---|---|---|---|---|
| A0 anchor | 1ES 1101-232, 0.733 TeV, z = 0.186 (725.5 Mpc) | 3.764 × 10⁻³³ | 232.9 | 1.88 × 10⁻³⁴ m (11.6 ℓ_P) | 3.76 × 10⁻³⁵ m (2.33 ℓ_P) | 3.76 × 10⁻³⁶ m (0.233 ℓ_P) |
| A1 Crab | LHAASO, 0.94 PeV (1.12 PeV − 2σ), 1.54 kpc | 2.102 × 10⁻³⁵ | 1.301 | 1.05 × 10⁻³⁶ m (0.0650 ℓ_P) | 2.10 × 10⁻³⁷ m (0.0130 ℓ_P) | 2.10 × 10⁻³⁸ m (0.00130 ℓ_P) |
| **A2 Cygnus** (decisive) | LHAASO, ≥ 1 PeV (8 events vs 0.75 background), 1.25 kpc | **2.075 × 10⁻³⁵** | **1.284** | **1.04 × 10⁻³⁶ m (0.0642 ℓ_P)** | **2.08 × 10⁻³⁷ m (0.0128 ℓ_P)** | **2.08 × 10⁻³⁸ m (0.00128 ℓ_P)** |
| A3 GRB 221009A | LHAASO KM2A, 7.7 TeV (12.5 − 2σ), z = 0.151 (603.2 Mpc) | 1.740 × 10⁻³⁴ | 10.77 | 8.70 × 10⁻³⁶ m (0.538 ℓ_P) | 1.74 × 10⁻³⁶ m (0.108 ℓ_P) | 1.74 × 10⁻³⁷ m (0.0108 ℓ_P) |
| A4 Mrk 501 | HEGRA 1997, 16 TeV, z = 0.034 (147.5 Mpc) | 1.049 × 10⁻³⁴ | 6.492 | 5.25 × 10⁻³⁶ m (0.325 ℓ_P) | 1.05 × 10⁻³⁶ m (0.0649 ℓ_P) | 1.05 × 10⁻³⁷ m (0.00649 ℓ_P) |
| **Combined** (minimum) | A2 | **2.075 × 10⁻³⁵** | **1.284** | **1.04 × 10⁻³⁶ m (0.0642 ℓ_P)** | **2.08 × 10⁻³⁷ m (0.0128 ℓ_P)** | **2.08 × 10⁻³⁸ m (0.00128 ℓ_P)** |
| Combined, τ × 10 (robust) | A2 | 4.471 × 10⁻³⁵ | 2.766 | 2.24 × 10⁻³⁶ m (0.138 ℓ_P) | 4.47 × 10⁻³⁷ m (0.0277 ℓ_P) | 4.47 × 10⁻³⁸ m (0.00277 ℓ_P) |

**The reference readings are tighter.** These are each arm's quoted energy and distance:

| Arm | Reference reading | d_max (m) | d_max (ℓ_P) |
|---|---|---|---|
| Cygnus | 2.5 PeV at 1.4 kpc | 5.89 × 10⁻³⁶ | 0.364 |
| Crab | 1.12 PeV at 1.90 kpc | 1.55 × 10⁻³⁵ | 0.960 |
| Mrk 501 | 21.45 TeV | 7.10 × 10⁻³⁵ | 4.39 |
| GRB 221009A | 12.5 TeV | 9.12 × 10⁻³⁵ | 5.64 |
| Anchor | 2.916 TeV | 5.97 × 10⁻³⁴ | 36.9 |

**Against the brief's expectation.**
- The PeV arms shrink the anchor's window by 179 (Crab) and 181 (Cygnus) on the readings of record, and by 38 and 101 on the reference readings. That is inside the expected 40–2,000 range, or at its edge.
- The shrink follows d_max ∝ (E⁴D)^(−1/3) exactly.

**Checks on every arm and configuration.** All 20 arm-and-configuration cells pass:
- Rayleigh regime: k·d_max ≤ 2.6 × 10⁻¹³, against the threshold of 10⁻⁴.
- Weak-fluctuation conditions: ε_T² ≤ 0.025, and ε_T·x and Q·x³ are negligible.
- Lattice continuum: k·a ≤ 1.3 × 10⁻¹⁴ at N = 20.
- Aggregate RVE: a wavelength cube holds at least 10⁴⁰ grains (1.4 × 10⁴⁰ at the shortest wavelength of any reading), so the grain-to-aggregate averaging of Ranganathan & Ostoja-Starzewski is met with vast margin.
- The anchor reproduces W^EM_∪ of record (3.7641664288 × 10⁻³³ m) to 8.2 × 10⁻¹⁰.

**The scattering condition, restated.**
- α = c_geo ε_T² k⁴ d³, with c_geo = Q_T^a/(8ε_T²) = 0.38–0.53. The fluctuation strength ε_T² = 0.0083–0.0248 is fixed by the G-TSH4-lineage single-crystal tensors.
- This is the brief's α ∝ k⁴d³⟨(δC/C)²⟩ with its prefactor computed.

## Where the Planck length falls

- **Under the combined bound**, the largest number of cells a grain can hold is:
  - N_P = d_max/ℓ_P = 1.28 at a = ℓ_P (2.77 under the robust variant);
  - N_D = 0.11 at the declared band's lower edge, a = 1.899 × 10⁻³⁴ m = 11.75 ℓ_P.
- **So for any N ≥ 2**, the light window needs cells finer than the Planck length. Under the declared chain, no grain holds even one cell: the band's lower edge is 9.2 times d_max.
- **The anchor arm alone** keeps 233 cells at a = ℓ_P and 19.8 at the band's edge. This matches V4.94's "4.96–19.82 cells".
- **The window is EMPTY for the combined bound at N = 20, 100 and 1,000**, in both senses:
  - a_max < ℓ_P;
  - a_max < 1.899 × 10⁻³⁴ m.

  This holds under the robust variant too.

## Texture bound (independent of the lattice spacing)

A textured aggregate is birefringent at first order, Δn = b₁·t₄. The bound is t₄ ≤ Δn_max/|b₁|:

| Birefringence limit | Δn_max | hex (b₁ = 0.0162–0.0182) | cubic (\|b₁\| = 0.0379–0.0455) |
|---|---|---|---|
| **R-T1, of record:** GRB polarization, σ < 10⁻³⁷ (Kostelecký & Mewes 2006), along the burst sightlines | 2 × 10⁻³⁷ | **t₄ ≤ 1.1–1.2 × 10⁻³⁵** | **t₄ ≤ 4.4–5.3 × 10⁻³⁶** |
| R-T2: cosmological spectropolarimetry, 2 × 10⁻³² (KM 2002), any orientation | 4 × 10⁻³² | t₄ ≤ 2.2–2.5 × 10⁻³⁰ | t₄ ≤ 0.9–1.1 × 10⁻³⁰ |
| R-T0, reported: GRB 021206 (polarization disputed) | 2 × 10⁻³⁸ | t₄ ≤ 1.1–1.2 × 10⁻³⁶ | t₄ ≤ 4.4–5.3 × 10⁻³⁷ |

**Comparison with randomly oriented grains.**
- **Sampling scatter.** A finite sample of M random grains has net texture √(c/M), with c = 21/4 (cubic) or 9 (hex).
- **At the scale of a polarimetry path.** Over the first Fresnel volume of a 1 Gpc path at 100 keV, the statistical texture is:
  - 7–9 × 10⁻⁶⁹ at the largest grain size on record (3.8 × 10⁻³³ m);
  - 3–4 × 10⁻⁷² at d_max.

  That is 33–36 orders of magnitude below the bound.
- **At small scales.** Random grains already average below the bound inside a cube about 1.5–2.2 nm across (or 8–12 pm at d_max).
- **What follows.** A random polycrystal is untouched by the birefringence data. The bound restricts only a coherent, cosmological-scale alignment of the grains, to below about 10⁻³⁵ (or 10⁻³⁰ in any direction).
- **Scope.**
  - b₁ is defined for sightlines perpendicular to the texture axis, and other sightlines carry an angular factor of order one.
  - The hex l = 2 texture t₂ has no banked first-order coefficient, so it is not bounded here.

## Dispersion

- **No term linear in energy (dimension 5).**
  - The light carrier is the shear phonon of a centrosymmetric crystal: p6m in 2D, and the AB/hcp stack, P6₃/mmc, in 3D.
  - With finite-range forces the dynamical matrix is analytic, and inversion makes ω² even in k. So ω/k − c starts at k².
  - Natural optical activity (linear birefringence) needs broken inversion.
  - A random aggregate of such grains inherits all this.
  - The record agrees: G-S2C1's verdict is A3 DISPERSIVE-O(k²).
  - LHAASO's linear bound (E_QG,1 > 10 E_Pl) therefore does not apply.
- **Quadratic.** The lattice has E = pc[1 + a₂(ka)²] with a₂ < 0, so it is subluminal. LHAASO's E² ≃ p²c²[1 − (E/E_QG,2)²] then gives a = ħc/(E_QG,2 √(2|a₂|)).
  - With E_QG,2 > 6.9 × 10¹¹ GeV (subluminal) and |a₂| = 0.0132 (Γ–K): **a ≤ 1.76 × 10⁻²⁷ m = 1.09 × 10⁸ ℓ_P**.
  - The other readings give 0.82–1.02 × 10⁸ ℓ_P.
  - This is about ten times looser than the brief's expectation of 10⁷ ℓ_P, because of the factor 1/√(2|a₂|) ≈ 5–6.
  - At N = 20 it is 1.7 × 10⁹ times looser than the attenuation bound, so it never binds.
  - The a₂ values are the 2D single-crystal ones; no 3D value is on record.

## Combined

**a_max(N) = min(attenuation, dispersion) = 2.08 × 10⁻³⁵ m / N at every N**, from the attenuation arms. The Planck length lies above a_max(N) for every N ≥ 2.

## What it touches, and what it does not

**Pointers in the V4.95 fold.**
- **The light-only transverse carrier** (§2.92.E). The one transverse carrier left now has a bound on its medium.
- **W^EM_∪** (§2.91.N and the G-CI1 Part VI row). The window of record stands as computed from its sealed anchor; the photon data as a whole bound grains 181 times tighter.
- **The polycrystal-floor row** (Part VI). The numbers it needs, with the options below.
- **The ANNEX-SC-1 / G-S2C1-W chain**: ANNEX-CDEF-1, §2.91.H and the G-S2C1-W row. Under the declared chain no grain holds a cell, and no scale is re-pinned.
- **The texture** (§2.91.S, where b₁ is banked; §2.91.T, whose first-order polarization-split successor E-SA-1(b) is unopened). There is now an observational bound on t₄. The successor stays unopened.

**What it does not touch.** The A1 polarization verdict, the A2 internal-mode friction, the second-sound drag and KC-EP do not depend on the grain size, the lattice spacing or the texture of the transverse aggregate, so they stand as recorded.

## The polycrystal floor: options for the author

| Option | What the homogenization literature says | a_max | Robust (τ × 10) |
|---|---|---|---|
| **N = 10** (G-CI1's registered substrate floor, never exercised in SI) | Grains of 9–18 cells are 15–27 % soft, with 30–50 % of atoms in boundaries (atomistic Cu; Schiøtz et al. 1998, 1999) | 2.08 × 10⁻³⁶ m (0.128 ℓ_P) | 0.277 ℓ_P |
| **N = 20** | 37-cell grains are still about 15 % soft | 1.04 × 10⁻³⁶ m (0.064 ℓ_P) | 0.138 ℓ_P |
| **N = 50** (lower end of the supported floor) | Grains of ≳ 55 cells (≳ 20 nm in Cu) are at most a few percent soft (experiments, porosity-corrected) | 4.15 × 10⁻³⁷ m (0.026 ℓ_P) | 0.055 ℓ_P |
| **N = 100** (upper end of the supported floor) | Boundary fraction about 3–9 % | 2.08 × 10⁻³⁷ m (0.013 ℓ_P) | 0.028 ℓ_P |
| **N = 1,000** | Boundary fraction about 0.3–0.9 % | 2.08 × 10⁻³⁸ m (0.0013 ℓ_P) | 0.0028 ℓ_P |
| **No floor** | Grains could be single cells. Then the continuum theory behind W^EM_∪ (grains much larger than a cell) does not apply as stated | d ≤ 2.08 × 10⁻³⁵ m (1.28 ℓ_P), no statement on a | 2.77 ℓ_P |

The literature supports **N ≈ 50–100** as the floor at which a grain behaves as a bulk crystal to a few percent. Every option with N ≥ 2 puts the cells below the Planck length, and under the declared chain no option leaves a window. The choice is the author's.

## Process

- **Prior Address**: `LS_PRIOR_ADDRESS.md`.
- **Pre-registration**: `LS_PREREG.md`, md5 ea6651ce…, locked at `65404f5` before any computation.
- **Leg 1**: `ls_leg1.py`, committed at `a9e6091` before the comparison script existed.
- **The comparison**, run last: `ls_compare.py`, at `ebf150c`.
- **The second-leg trigger fired.** The combined bound is empty at N = 20 in both pre-registered senses. The brief's literal condition ("empty for every N ≥ 20 on every arm") holds under the declared-chain reading, since every arm is EMPTY_D at N = 20. It does not hold under the Planck reading, because the anchor arm alone keeps 11.6 ℓ_P at N = 20.
- **The comparator** `ls_twoleg_compare.py` was frozen at `824f7fd` before leg 2 was launched.
- **Leg 2** was a blind subagent given only `LS_PREREG.md`.
  - Its 13 tool calls are audited: it read that file, checked the input md5s, and wrote only to the scratchpad.
  - It used independent quadratures (tanh-sinh at 40 digits, QUADPACK, Gauss–Legendre and the closed-form flat-ΛCDM lookback) and a 40-digit mpmath d_max path.
  - **Result: 185/185 checks pass, worst relative deviation 4.8 × 10⁻¹⁵.** Same decisive arm; identical EMPTY flags. Committed at `4a4b7b0`.
  - Its eleven interpretive choices are listed in `leg2/REPORT.md`. None moves a number that decides anything.

## Honesty notes

- **H-LS-1 to H-LS-4** are in the pre-registration: what was known beforehand, the added Cygnus arm, the permissive reading of R-T2, and the conservative alternative-reading rules.
- **H-LS-5.** Cygnus beats the Crab by 1.3 %. The headline does not depend on which of the two decides.
- **H-LS-6.** The dispersion expectation (10⁷ ℓ_P) differs from the result (1.1 × 10⁸ ℓ_P) by 1/√(2|a₂|). No rule depended on it.
- **H-LS-7.** The first LHAASO catalogue was not retrieved. A catalogued source with larger E⁴D would only tighten the bound, since the combined bound is a minimum.
- **H-LS-8.** The bound assumes the LHAASO events are photons. Cygnus rests on a population (8 events against 0.75 background), the Crab on one event at 1.12 PeV less 2σ.
- **H-LS-9.** Like W^EM_∪, the bound is conditional on:
  - the G-CI1 scattering machinery (Voigt reference medium, Rayleigh regime);
  - the units election c_T ≡ c;
  - the anchor's conventions (amplitude τ, light-travel distance, observed wavenumber).

  The machinery itself presumes grains much larger than a cell, which is exactly the floor question.

## Files

All in `audit_followup/lattice_bound/` on branch `claude/audit-followup-oct6`:

| File | Contents |
|---|---|
| `LS_PRIOR_ADDRESS.md` | The literature pass |
| `LS_PREREG.md` | The pre-registration |
| `ls_leg1.py`, `.json`, `_output.txt` | Leg 1 |
| `ls_compare.py`, `.json`, `_output.txt` | The comparison |
| `ls_twoleg_compare.py`, `.json`, `_output.txt` | The two-leg check |
| `leg2/` | The blind leg's script, JSON, extras and verbatim report |
| `LS_RESULT.md` | This file |
