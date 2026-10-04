# XCHECK3D: independent 3D cross-check of this leg's 3D instrument

Files: `xcheck3d.py` (code, written from scratch), `xcheck3d_results.json` (all numbers, repr precision).
Blindness: `cc3d.py`, `qb_results.json`, `QB_NOTES.md`, `cc_loss.py` and `qd_results.json` were not opened until
my own numbers were saved. The results file had md5 `765b0c9bc0f7bc6eb99286ddc24ac39f` (written 17:10)
before I opened `qb_results.json`. The only later change to the file is one extra key,
`comparison_with_qb_results_post_save`. I checked that every other key is identical to the pre-comparison
copy. I never opened `cc3d.py`, because no difference needed a diagnosis.

## Model and setup
- Units ħ = m = R = 1, mean density 1. Kernel Û(k) = 4π(sin k − k cos k)/k³.
- Λ_c = 21.713734623865665 at k* = 5.44861331461245. The value comes from brentq on the stationarity condition
  5(sin k − k cos k) = k² sin k. Two checks: bounded minimisation gives 21.713734623865676, and a dense scan of
  k ∈ (0, 60] gives 21.713734629612205. Λ = 2Λ_c = 43.42746924773133.
- Cell: the ORTHORHOMBIC 4-site cell (a, √3a, c) as dispatched, with a = 1.3859646002819213 and
  c = 2.2595969088482843. Volume = N_cell = 7.517888… (see JSON).

## Method (chosen to differ from the main instrument)
1. **Ground state.** Pseudo-spectral real grid with exact Fourier-space convolution.
   - Solver: Newton–Krylov. The bordered Newton system for (ψ, μ) is solved by GMRES with an exact
     Hessian action (FFT) and a kinetic preconditioner, plus backtracking. No imaginary time and no L-BFGS.
   - Start: Gaussian droplets with σ chosen variationally (σ = 0.19938905727729953).
   - Symmetry: ψ is symmetrised under mirror x, mirror z, the c-glide (y → 2/3·√3a − y, z → z + c/2) and
     centering (½,½,0).
   - Convergence: 4 Newton steps to |F| = 3.3e-13 on the 24×42×40 grid. The 32×54×52 grid (seeded by spectral
     interpolation) needed 1 step.
   - E/N = 68.34274926596238 on both grids (difference 0). μ = 117.79955618037532.
   - ψ0 > 0 everywhere (min 1.15e-3), so L ≥ 0. The Fourier tail at the grid edge is 1.0e-14.
2. **BdG basis.** BOX cut |n_x| ≤ M_x, |n_y| ≤ M_y, |n_z| ≤ M_z on the orthorhombic reciprocal lattice. The
   main instrument used a sphere cut on the primitive cell. The basis is reduced to exact symmetry sectors:
   - centering parity (the even block contains e^{iq·r}ψ0);
   - for q ∥ x: (mirror z) × (c-glide);
   - for q ∥ z: (mirror x) × (c-glide with the e^{−iq_z c/2} phase removed).

   Check: the unsplit centering-even spectrum equals the union of the sector spectra to 1.6e-11. Off-(+,+)
   density weights are ≤ 1e-29.
3. **Exchange-like term.** X_{GG'} = Λ Σ_K ψ_{G−K} Û(|q+K|) ψ_{K−G'} is built as an explicit product W D W†.
   K runs over an alias-free set: the dilation of the box by the ψ support at 1e-14 relative. No FFT enters the
   BdG matrices. Φ_G = ΛÛ(G) n_G comes from an alias-free doubled grid.
4. **Algebra.** Cholesky of L instead of A: L = D D†, then the Hermitian problem D†AD y = ω² y with
   f₊ = D y/√ω, solved by full-spectrum eigh. Checks:
   - the full 2N×2N non-Hermitian eig at cut (7,12,11) reproduces the low spectrum to 1.35e-9 absolute
     (max |Im| = 3.6e-11);
   - χ_static = 2⟨s|A⁻¹|s⟩ by a direct dense Cholesky solve.
5. **Mode identification by symmetry sector, polarisation probes and q-scaling.**
   - q ∥ x: the (+,+) sector holds the two gapless density modes (2 = lower, 1 = upper). The glide-odd sector
     holds the y-polarised transverse mode; the mirror-z-odd sector holds the z-polarised transverse mode.
   - q ∥ z: the x-polarised transverse mode is mirror-x-odd and the y-polarised one is glide-odd.
   - **Pitfall found.** The glide-odd sector also contains a GAPPED mode, the relative-phase mode between
     the A and B layers. It sits at ω_Γ = 0.8416648620080364 and is almost flat: 0.84239 at q = 0.15 and
     0.84532 at q = 0.3. Below q ≈ 0.105 the y-transverse branch is the lowest mode of that sector; at q = 0.15
     and 0.3 it is the SECOND. I took the gapless branch, identified by the ratio ω(0.3)/ω(0.15) =
     2.0082195715029627 (the gapped mode gives 1.0035). Ordering by frequency would have given a spurious
     "c_T" ≈ 5.62.

## Results (primary: box cut M = (11,19,17), (+,+) sector Ns = 4041, N_K = 161293; q = 0.15 along x)

**Longitudinal (density-carrying) modes**

| quantity | value |
|---|---|
| c2 = ω2/q | 0.47055564690854 |
| c1 | 16.137178902945973 |
| F2 | 0.0016666207064723478 |
| F1 | 0.996681735526285 |
| Z21 = Z2/Z1 | 0.05734517702845586 |
| S2 (denominator Σ2Z/ω) | 0.6629041194625593 |
| S2 (denominator direct χ) | 0.6629038969095532 |
| c_κ = (vol/χ_direct)^½ | 9.384645864996887 |
| χ_direct | 0.08536111851946435 |

**Transverse speeds**

| direction | polarisation | value |
|---|---|---|
| along x | y | 8.040065316431589 |
| along x | z | 7.759918210458156 |
| along z | x | 7.7493459801429845 |
| along z | y | 7.749345985463413 |

- Range over x and z: c_T min = 7.7493459801429845, max = 8.040065316431589. c2 > c_T never occurs.
- Along z the lower and upper longitudinal speeds are 0.470578027070683 and 16.967018439481198, with
  F_lower = 0.0017385767900414044 and c_κ,z = 9.399832663460701.

**Sum rules at q = 0.15**
- f-sum residual: −1.5e-12.
- Spectral χ vs direct χ: −3.36e-7. This is eigh rounding on a graded spectrum, with ω² up to 1.35e7. The
  Rayleigh–Ritz refinement below reduces it to −4.1e-14.
- Σ F/c² over the two gapless modes = 0.011354253828574034, against 1/c_κ² = 0.011354400847348548.

**q = 0.3 (from cut (9,15,14))**
- c2 0.46907380973635504, c1 16.08614968804044, F2 0.0016573608455867637, Z21 0.05735130257258418,
  S2 0.6627861967017891, c_κ 9.38035723112268.
- Transverse speeds: 8.073108267719794 (y-polarised), 7.752967315109585 (z-polarised).
- LSQ slopes over q ∈ {0.15, 0.3}: c2 0.46937015589210657, c1 16.096355531271087.
- Gapless checks, ω(0.3)/ω(0.15): mode 2 1.9937, mode 1 1.9937, T_z 1.9982.

**Γ sector (cut 9)**
- Translation zero modes of A: 3.4e-11, 5.0e-11, 2.7e-11.
- Lowest eigenvalue of L in the (+,+) sector: 9.2e-14 (the phase mode).

**Extras**
- Dispersion along x at cut 7 for q = 0.05, 0.1, 0.15, 0.3: c2 = 0.47126 → 0.46908 and c_T,z = 7.7621 → 7.7530.
- Band-curvature estimate 2λ_min(L(q))/q² at q = 0.15: 0.0030745794849882965. This is not the same estimator
  as the twist f_s.

## Convergence (q = 0.15, the cut count is the box half-width)

| cut | Ns(+,+) | c2 | F2 | Z21 | S2 | c_κ | c_T,x,y |
|---|---|---|---|---|---|---|---|
| (7,12,11) | 1122 | 0.4705852929506607 | 0.0016668315294936105 | 0.0573488151669753 | 0.6629042469789884 | 9.384645912749987 | 8.040074544867737 |
| (9,15,14) | 2217 | 0.4705555405151125 | 0.001666620741465662 | 0.057345191201168294 | 0.6629042252331365 | 9.384645865021486 | 8.040065321819203 |
| (11,19,17) | 4041 | 0.47055564690854 | 0.0016666207064723478 | 0.05734517702845586 | 0.6629041194625593 | 9.384645864996887 | 8.040065316431589 |

- Changes between cuts (9) and (11) are at most 2.5e-7 relative and come from eigh rounding, not truncation.
- The f-sum residual falls from 3.9e-7 to 6.2e-11 to 1.5e-12.
- Peak RSS was 2.19 GB at the largest cut.
- A smaller cut (4,7,6) is NOT converged (c2 = 2.35). f_s is about 3e-3, so the superfluid branch depends on the
  tunnelling tails of ψ0 and needs |G| ≳ 30.

## Comparison with `qb_results.json` (main instrument: primitive cell, sphere K = 50, A-Cholesky)
All 31 overlapping physics quantities pass the thresholds (speeds and c_κ 0.3%, F and Z21 2%, S 0.01 absolute).
The largest differences:

| quantity | xcheck3d | qb | relative diff |
|---|---|---|---|
| c2 | 0.47055564690854 | 0.470555527432646 | 2.54e-7 |
| Z21 | 0.05734517702845586 | 0.05734519151329853 | −2.53e-7 |
| S2 | 0.6629041194625593 | 0.6629042326549988 | −1.13e-7 (absolute) |

- S1 (the complement of S2, 1.1e-7 absolute) and the lower longitudinal speed along z (1.3e-7) are also at the
  1e-7 level, for the same reason. Everything else agrees to ≤ 1.3e-8. c_κ agrees to 1.9e-15, c1 to 4.5e-11,
  F2 to 1.3e-9, and the transverse speeds to ≤ 1.2e-9.
- Further agreements: E/N is identical, μ agrees to 1.2e-16, and Λ_c is identical. The Γ first nonzero
  eigenvalue of A agrees to 6.4e-12, and the glide-odd lowest eigenvalue of L to 3.0e-10. All q = 0.3 values,
  the LSQ slopes and the z-direction longitudinal values agree to ≤ 1.3e-7.
- **Diagnosis of the 1e-7-level residue: neither implementation is wrong.** The gap comes from rounding in my
  own eigh on the graded L-Cholesky matrix at the largest cut. Supporting evidence:
  - my normalisation error is 5.1e-7, and my spectral-vs-direct χ residual is 3.4e-7;
  - a post-comparison Rayleigh–Ritz refinement of the lowest 12 (+,+) modes on the well-conditioned pencil
    A f = ω² L⁻¹ f (normalisation error 9e-14, χ residual 4e-14) gives, against qb, c2 to 8.8e-10, F2 to 1.8e-9,
    Z21 to 9.1e-10 and S2 to 4.2e-12.

  The refinement is a labelled diagnostic and does not replace the saved primary values.
- Extrapolation convention (an extra, not a schema quantity). qb's two-point c_κ(q→0) = 9.386074974659767
  extrapolates c_κ² linearly in q²; recomputing that from qb's inputs gives 9.386074974171704. Mine,
  9.386075409654422, extrapolates c_κ linearly in q². qb's small-q fit gives 9.386022556462432.
- Two notes. First, the transverse-mode labels agree: qb also used the gapless glide-odd branch at q = 0.15,
  not the gapped 0.84 mode. Second, qb's c_T range covers x, y and z, while mine covers x and z; qb's
  y-direction values lie inside the range, so cT_min and cT_max coincide.

## Ambiguities and choices
- The dispatch defines S2 with the denominator Σ_μ 2Z_μ/ω_μ; I report that value as primary. The spec's
  denominator (direct χ) is reported alongside.
- Speeds are ω/q at q = 0.15. LSQ slopes over 0.15 and 0.3 are given as extras.
- Cut (11,19,17) was run at q = 0.15 only; the q = 0.3 and Γ values come from cut (9,15,14).
