# E1 — A fold in one dimension (φ⁴ in 1+1 D)

## Question

Does the seed's Model A behave the way SEED.md §2, §4, §7.1 and §8 say? Before that can be judged, the tools have to reproduce the known φ⁴ answers. PLAN.md §4 preregisters five parts:

- **E1a.** The static kink: its mass and shape-mode frequency.
- **E1b.** Kink–antikink collisions: the critical velocity v_c and the two-bounce resonance windows.
- **E1c.** The Dutta–Steer–Vachaspati (DSV 2008) breather-train production map.
- **E1d.** Colliding Gaussian packets of the field itself (new). Three questions:
  - Is production bounded below by 2M_kink?
  - Is the production boundary ragged?
  - Does production favour slow, wide packets?
- **E1e.** How many quanta the smallest producing initial states carry, in units of m²/λ.

## Method

### Equations and conventions

The DSV convention is used throughout:

- 𝓛 = ½φ_t² − ½φ_x² − ¼(φ² − 1)², so the equation of motion is φ_tt = φ_xx − φ(φ² − 1).
- Vacua φ = ±1; meson mass m = √2.
- Kink tanh(x/√2), kink width √2, M_kink = 2√2/3.
- Shape mode ω_s = √(3/2).
- Energies are quoted in units of 2M_kink = 4√2/3. Velocities do not depend on the convention.

### Discretization (`phi4core.py`)

- Uniform grid with a node at x = 0.
- Fourth-order centred differences for φ_xx.
- Velocity-Verlet (leapfrog) time stepping, dt = 0.4 dx unless stated.
- Absorbing layers outside |x| < L_phys: a damping term −γ(x)φ_t, with γ rising quadratically from 0 to 1 over a width W, applied by exact exponential splitting.
- Ghost values beyond the array ends are fixed at −1.
- Energy uses a fourth-order φ_x.

Energy conservation without absorbing layers (dx = 0.05, dt = 0.02, t = 300): the maximum relative drift is 5.6×10⁻⁵ for a Gaussian collision and 7.5×10⁻⁶ for a kink collision (`e1_verify.py`).

### Pair test (fixed in `phi4core.py` before any E1c or E1d scan)

A "pair" at time t is a maximal interval with φ > 0 that:

- is longer than 4 kink widths (5.66), and
- has φ > 0.5 on at least 80% of its points.

The whole array is searched, including the absorbing layers, where outgoing kinks slow down and stop.

### E1a (`e1a_static.py`)

- Newton solve of the discrete static equation at dx = 0.1, 0.05 and 0.025.
- Energy of the relaxed kink.
- Spectrum of the lattice operator −∂² + 3φ_k² − 1.
- Time-domain shape-mode check (zero-crossing count).

### E1b (`e1b_kkbar.py`, `e1b_dtcheck.py`, `e1b_boxcheck.py`)

Initial condition:

- φ = tanh(γ(x+x₀)/√2) − tanh(γ(x−x₀)/√2) − 1, with φ_t from the boost.
- Each kink moves at speed v toward the other.
- Box L_phys = 40, W = 30; x₀ = 12 (8.5 kink widths); run to t = x₀/v + 600.

Classification:

- Bounces are down-crossings of φ(0, t).
- Escape: φ(0) stays positive and the outermost zero recedes. Otherwise the run is a capture (bion).
- The label is the bounce count for an escape and 0 for a capture.

Scan:

- v = 0.15–0.30 in steps of 10⁻⁴ (1501 runs).
- Every label change is then bisected to 2×10⁻⁵.

Convergence checks:

- dx ∈ {0.1, 0.05, 0.025} at dt = 0.4 dx.
- x₀ ∈ {12, 20}.
- Post-collision time 600 and 1500.
- Time-step check: v_c and the window-1 edges bisected to 10⁻⁵ for seven (dx, dt) pairs.
- Box check (new): (L_phys, W) = (100, 60) and (200, 100).

### E1c (`e1c_dsv.py`)

Initial data exactly as published (DSV eqs. 11–13):

- f = −1 + Σ (4/π) arctan[η sin(ωT_n)/cosh(ηωX_n)], with η = √(1−ω²)/ω;
- N_b = int[2/√(1−ω²)] + 1 breathers per train;
- a = 10/√(1−ω²), d = 2/√(1−ω²).

Lattice and criterion:

- L_phys = 600 (our choice; the span of DSV's Fig. 1), absorbing layers of width 60, dx = 0.1.
- Evolution for one light-crossing time, T = 2L_phys = 1200. The DSV call is "pair present at t = T".
- We also continued to 1.5T.

Grids:

- ω = 0.90, 0.91, …, 0.99 × v = 0.40–0.90 in steps of 0.01 (510 runs).
- ω ∈ {0.992, 0.995} × v = 0.20–0.90 (72 runs).
- A dx = 0.05 rerun of the columns ω = 0.91, 0.95, 0.99 (78 runs).

### E1d (`e1d_gauss.py`, `e1d_extra.py` and follow-ups)

**Initial condition (baseline).**

- φ = −1 + Σ± A exp(−(x∓x₀)²/2σ²) cos(k(x∓x₀)).
- φ_t = ±A ω_k G sin(·), with ω_k = √(k² + 2) at the carrier. This is the PLAN wording "φ_t from the linear dispersion ω_k" taken literally.
- Group velocity v_g = k/ω_k.

**Variant (new).** Exact one-way packets: the same φ(x, 0), with every Fourier component given its own free-wave velocity toward the centre. For kσ ≳ 3 the two forms coincide to about 1%. For kσ ~ 1 the baseline also sends part of each packet outward.

**Fixed rules.**

- x₀ = 4σ + 10; t_coll = x₀/v_g.
- T = max(t_coll + 400, 1.25(t_coll + 100)).
- L_phys = x₀ + 4σ + 40, W = 50.
- dx = 0.1, dt = 0.04.

**Production criterion.** A pair present at each of 0.80T, 0.85T, 0.90T, 0.95T and T. Energy is computed from the discrete initial data.

**Coarse 3D grid (1485 runs).**

- A = 0.1–1.5 in steps of 0.1.
- σ ∈ {1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 16}.
- k ∈ {0.25, …, 3}, so v_g = 0.17–0.90.

**Two 59 × 57 slices.** The rule, fixed in `choose_slices.py` before the coarse scan finished, takes the coarse σ and the coarse k with the most producing runs:

- (A, k) at σ = 16;
- (A, σ) at k = 1, with σ from 1 to 16 log-spaced.

**Controls.**

- Single-packet runs: the right-moving packet alone, for every producing point. A producing point whose single packet makes no pair is "collision-needed".
- Collision phase: 60 boundary points with x₀ shifted over one carrier period.
- Grid spacing:
  - dx = 0.05 on 300 random coarse points;
  - the whole k = 1 slice at dx = 0.05, dt = 0.02 (new), with its single-packet controls;
  - a ladder to dx = 0.025 and 0.0125 at 32 points (new).
- Probes of the smallest producers (local grid, phase shifts, dx = 0.05 and 0.025) in both initial-velocity forms.

### E1e (`e1e_quanta.py`)

With Φ = vφ and x → x/(√λ v), the action is S = v²S̃. The classical dynamics therefore does not depend on φ₀ = v. With ħ = 1:

- N = E/m = φ₀² Ẽ/√2, with φ₀² = m²/(2λ);
- so N·λ/m² = Ẽ/(2√2), where λ/m² is the dimensionless coupling in 1+1 D.

We also report the free-field occupation of the fluctuation about −1, N_lin = Σ_q (|π_q|² + ω_q²|δ_q|²)/(2ω_q), using the lattice dispersion.

### Reconciliation methods (added after the cross-check; not preregistered)

- **Fourth-order time stepping for DSV trains** (`e1c_reconcile.py`, scheme "y4"). Yoshida's symmetric composition of the same velocity-Verlet step, with weights w₁ = 1/(2 − 2^{1/3}) and w₀ = −2^{1/3} w₁, and the exact damping split in every sub-step. Space, initial data, lattice, run length and pair test are those of `e1c_dsv.py`.
  - A call is "converged" when the two finest runs agree on it and their φ(0, t) agree to 0.1 until the pair has formed.
  - (dx, dt) ladders run down to (0.0125, 0.005).
- **Neighbourhood ensembles.** Initial data at v steps of 0.001 inside DSV's 0.01-wide cells at ω = 0.99.
- **Speed at fixed packet shape** (`e1d_speedtest.py`). The design is A ∈ {0.5, …, 1.0}, σ ∈ {2, 4, 8} and the nine coarse k values. Each point is run at 8 collision phases (x₀ shifted over one carrier-phase period), in both φ_t forms, with single-packet controls. The analysis is a logistic slope on v_g with one intercept per shape. The decision rule is in the script's docstring and was fixed before the run.
- **Time reversal** (`e1_timereversal.py`). A slow kink–antikink pair is evolved until the bound state stays below φ = 0. Then all velocities are reversed and the run continues, without absorbing layers.

### Runs and threads

Two worker processes with one thread each, on a shared 4-core machine.

## Calibration

| Quantity | Ours | Target | Tolerance | Source | Verdict |
|---|---|---|---|---|---|
| M_kink | 0.9428090346 (dx = 0.025; rel. err. −7.4×10⁻⁹; dx = 0.05: −1.2×10⁻⁷) | 2√2/3 = 0.9428090416 | 10⁻⁴ rel. | exact | CALIBRATED |
| ω_s | 1.2247448677 (lattice eigenvalue, −3.0×10⁻⁹); time domain within 2.2×10⁻⁵ | √1.5 = 1.2247448714 | 10⁻⁴ rel. | exact | CALIBRATED |
| v_c | **0.26006 ± 0.00003** (dt → 0); baseline (dx 0.05, dt 0.02) 0.26016 | 0.2598 | ±0.001 | [summary] CSW 1983, Anninos et al. 1991 | CALIBRATED |
| First two-bounce window | **[0.19256, 0.20343]** (dt → 0); baseline [0.19268, 0.20354] | [0.1926, 0.2034] | ±0.003 per edge | [summary, one source] | CALIBRATED |
| ≥ 3 windows, narrowing toward v_c | 20 windows; widths 0.0109, 0.0048, 0.0025, 0.0015, 0.00096, 0.00066, 0.00048, … | ≥ 3, narrowing | qualitative | [summary] | CALIBRATED |
| DSV (ω, v) = (0.99, 0.43) *(reconciled)* | resolution-sensitive: no pair at 4 of 5 fourth-order (dx, dt) settings; a pair from t = 870 at the finest, (0.0125, 0.005); the pair-or-not decision falls after the runs' trajectories separate (t ≈ 830). Inside DSV's 0.01-wide cell, 0 of 11 neighbouring initial data (v = 0.425–0.435) produce at one fourth-order setting. Converged DSV-like producer at (0.99, 0.41): pair from t = 590 at every setting | pair | qualitative | [read] arXiv:0803.0670 | OPEN |
| DSV trend | band moves from v ≈ 0.73–0.85 (ω = 0.90) to 0.41 (ω = 0.99, converged); Spearman ρ(ω, median v) = −0.99 (cross-check: −0.94) | lower v as ω rises | qualitative | [read] | CALIBRATED |
| DSV pass-through at high v | 0/10 produce at v = 0.90; 2/60 at v ≥ 0.85 (cross-check: 0/18 at v ≥ 0.86) | trains pass through | qualitative | [read] | CALIBRATED |
| DSV holes | (0.91, 0.82) makes no pair at every resolution tried (leapfrog dx 0.1 and 0.05; fourth-order dx 0.05 and 0.025), while (0.91, 0.80) produces at all of them and (0.91, 0.85) at the three where it was run; the hole's extent varies (0.81–0.82 or 0.82–0.83); 10 single-point holes elsewhere at dx 0.1 | holes, e.g. (0.91, 0.82) | qualitative | [read] | CALIBRATED |
| DSV, ω > 0.99 | 0 of 72 runs (cross-check: 0 of 6) | none found | qualitative | [read] | CALIBRATED |
| E1d: production below 2M_kink (sanity check, not a literature target) | 0 of 19,526 Gaussian runs (pair and single, both φ_t forms, all resolutions) | 0 | exact | energy conservation | CHECK PASSED |

### E1b convergence

All rows use x₀ = 12 and a post-collision time of 600 unless the configuration says otherwise.

| Configuration | dx | dt | v_c | Window 1 |
|---|---|---|---|---|
| dx0.1 | 0.1 | 0.04 | 0.26044 | [0.19303, 0.20388] |
| base | 0.05 | 0.02 | 0.26016 | [0.19268, 0.20354] |
| dx0.025 | 0.025 | 0.01 | 0.26008 | [0.19259, 0.20346] |
| x₀ = 20 | 0.05 | 0.02 | 0.26016 | identical to base |
| post time 1500 | 0.05 | 0.02 | 0.26017 | identical to base |
| dt check | 0.1 / 0.05 / 0.025 | 0.01 | 0.260079 / 0.260079 / 0.260085 | [0.19259, 0.20346] |
| dt check | 0.05 / 0.025 | 0.005 | 0.260065 / 0.260065 | [0.19257, 0.20344] |
| box (100, 60) and (200, 100) | 0.05 | 0.01 | 0.260079 (shift 0) | [0.19260, 0.20346] (shift 0) |

- At fixed dt the results do not depend on dx, to within 10⁻⁵.
- The whole drift is second-order leapfrog time error.
- Richardson extrapolation gives v_c = 0.26006 and window 1 = [0.19256, 0.20343].
- Neither the box size nor the width of the absorbing layer moves any transition at the 10⁻⁵ bisection resolution, so reflected radiation is not the source of the offset from 0.2598.

Our v_c sits 2.6×10⁻⁴ above the [summary] target. That is inside the tolerance but larger than our estimated numerical uncertainty. *(Corrected in reconciliation.)* The independent cross-check, a Fourier pseudo-spectral code with RK4, a different x₀ and a different box, gives v_c = 0.260066, within 10⁻⁵ of ours. The offset therefore lies in the [summary] target value, not in either computation.

For context, Manton, Oleś, Romańczukiewicz & Wereszczyński 2021 (arXiv:2106.05153v2, read) quote the first window as 0.1920 < v < 0.2029. That is about 5×10⁻⁴ below both our edges and the target, so published values of these edges scatter at the 10⁻³ level.

**Windows 2–5** are [0.22414, 0.22896], [0.23723, 0.23974], [0.24407, 0.24556] and [0.24813, 0.24909]. They agree to 2×10⁻⁴ with a literature list of unverified provenance; this comparison was not preregistered. Windows narrower than 10⁻⁴ are not individually converged.

**Resonance check** (not preregistered): the time between the first two bounces grows by 5.30 per window, against one shape-mode period 2π/ω_s = 5.13. This is the Campbell–Schonfeld–Wingate mechanism. See `fig_e1b_collisions.png`.

### E1c compared with DSV Fig. 2

*(Table and comparison corrected in reconciliation.)* The DSV column is DSV Fig. 2 digitised from the arXiv PDF on the v grid of step 0.01 (`dsv_fig2_reading.json`). The earlier version of this table gave an approximate reading that smoothed over the gaps in the figure (for example ω = 0.95 as 0.64–0.77). Our map is the original one, at dx = 0.1 and dt = 0.04.

| ω | DSV Fig. 2 (digitised) | Ours (pair at T) | Hits | Ours only | DSV only |
|---|---|---|---|---|---|
| 0.90 | 0.76–0.79, 0.81, 0.83–0.86 | 0.73, 0.76–0.79, 0.82–0.85 | 7 | 0.73, 0.82 | 0.81, 0.86 |
| 0.91 | 0.76–0.80, 0.83–0.85 | 0.76–0.77, 0.80, 0.83–0.85 | 6 | — | 0.78–0.79 |
| 0.92 | 0.74, 0.76–0.84 | 0.72–0.74, 0.76–0.77, 0.81–0.84 | 7 | 0.72–0.73 | 0.78–0.80 |
| 0.93 | 0.69–0.77, 0.79–0.82 | 0.70–0.76, 0.78–0.81 | 10 | 0.78 | 0.69, 0.77, 0.82 |
| 0.94 | 0.67, 0.71–0.80 | 0.67, 0.69–0.79 | 10 | 0.69–0.70 | 0.80 |
| 0.95 | 0.64–0.65, 0.67–0.70, 0.72–0.73, 0.75–0.77 | 0.62–0.65, 0.67–0.69, 0.71, 0.75, 0.77 | 7 | 0.62–0.63, 0.71 | 0.70, 0.72–0.73, 0.76 |
| 0.96 | 0.59, 0.62, 0.65–0.66, 0.69–0.72 | 0.59, 0.64–0.67, 0.69 | 4 | 0.64, 0.67 | 0.62, 0.70–0.72 |
| 0.97 | 0.58, 0.61–0.66 | 0.57–0.58, 0.60–0.64 | 5 | 0.57, 0.60 | 0.65–0.66 |
| 0.98 | 0.49, 0.54–0.55 | 0.50–0.54, 0.56–0.58 | 1 | 0.50–0.53, 0.56–0.58 | 0.49, 0.55 |
| 0.99 | 0.43 | 0.41, 0.43 (original); 0.41 converged, 0.40 and 0.43 resolution-sensitive (reconciliation) | 1 | 0.41 | — |

- 80 of 510 runs produce, and 72 of them still have the pair at 1.5T.
- **Bands agree; points often do not.** We hit 58 of DSV's 81 producing points, with 22 producers DSV do not have and 23 of theirs we miss; 71 of our 80 producers lie within 0.01 of a DSV point. The earlier wording "reproduces DSV Fig. 2 band by band" is withdrawn. At the point level the map is not converged in either code. Five of the 14 lowest-energy producers of our map are not reproduced with fourth-order time stepping (`e1c_reconcile.py`): four make no pair at dx = 0.05, and (0.95, 0.62) makes one at dx = 0.05 but not at 0.025.
- The dx = 0.05 rerun agrees on 74 of 78 calls, and the four disagreements are band-edge points. In the ω = 0.99 column that agreement is trivial: our producers there (0.41, 0.43) are not on the dx = 0.05 grid (step 0.02), which has no ω = 0.99 producer at all.
- **The example point (0.99, 0.43) is resolution-sensitive.** *(Corrected in reconciliation; the earlier text said "the pair is real: it is still separating at 1.5T", which generalised from one unconverged run.)* The trains leave a long-lived central oscillation. Whether it ends in a pair is decided at t ≈ 830–870, after the trajectories of any two affordable resolutions have separated. With fourth-order time stepping there is no pair at four (dx, dt) settings, and a pair from t = 870 at the finest, (0.0125, 0.005). The original leapfrog gives a pair at some settings, including (0.1, 0.04), where it forms at t = 1160, and none at others. Inside DSV's 0.01-wide cell, 0 of 11 neighbouring initial data (v = 0.425–0.435, step 0.001; fourth order, dx = 0.05) make a pair. At the finest resolution the pair sits at ±128 at T, close to the ±140 of DSV Fig. 1, so DSV may have caught this rare outcome; we cannot tell. See the Reconciliation section and `fig_e1c_example_y4.png`.
- **A converged DSV-like producer sits 0.02 lower, at (0.99, 0.41).** The pair forms at t = 590 at every fourth-order setting down to (0.0125, 0.005), in the cross-check's spectral code at three settings, and in the leapfrog as dt → 0. The pair is well separated at T (±190–207; DSV Fig. 1 shows about ±140). Its v-neighbours at ±0.005 make no pair, and in the 0.41 cell only 3 of 11 neighbouring initial data produce (v = 0.407, 0.41, 0.411). Production at ω = 0.99 is a sparse, fractured set near v ≈ 0.40–0.41 (v = 0.40 produces at 3 of 4 fourth-order settings).

## Findings

### E1d, Gaussian packets

Figures: `fig_e1d_coarse.png`, `fig_e1d_slices.png`, `fig_e1d_example.png`, `fig_e1d_convergence.png`.

**1. Energy floor holds; in the scanned families, onset lies above it.** No run below 2M_kink produces, out of 19,526 Gaussian runs (pair and single, both φ_t forms, all resolutions). The lowest producing energies, which are upper bounds on where production starts *within each family*:

| Initial data | E/2M | Point | Resolution check | Collision needed? |
|---|---|---|---|---|
| Baseline, raw | 1.79 | A = 1.4, σ = 1, k = 0.25 | not reproduced at dx = 0.05 | — |
| Baseline | 1.86 | A = 0.8, σ = 2, k = 0.5 | reproduced at dx = 0.05 and 0.025 | yes |
| One-way φ_t | 2.70 | A = 0.6, σ = 4, k = 0.5 | reproduced at dx = 0.05 and 0.025 | yes |

The baseline point (A = 0.8, σ = 2, k = 0.5) carries E = 2.90 × 2M in one-way form and does not produce there. For broadband packets the φ_t prescription changes both the energy and the outcome.

*(Added in reconciliation.)* These onsets belong to the families, not to classical fields in general. Over all initial data the classical infimum is 2M itself. The φ⁴ equation is time-reversal invariant. A slow kink–antikink pair (v < v_c, outside the resonance windows) is captured, and the bound state radiates until the field stays below φ = 0 everywhere. Reversing all velocities at that moment gives kink-free initial data with E = 2Mγ(v), which evolve into an outgoing pair. `e1_timereversal.py` demonstrates this on the lattice. At v = 0.05 the reversed data have φ < 0 everywhere and E = 1.0012 × 2M, and they make the pair again under the exact inverse of the forward map. DSV 2008 (p. 1) describe the same construction. Such data are extremely finely tuned: noise of amplitude 10⁻⁸, a halved time step, or truncating the far radiation each prevents the pair.

**2. No energy threshold; amplitude matters.** On the coarse grid the producing fraction rises slowly and saturates below 1:

| E/2M | < 1.5 | 1.5–2 | 2–3 | 3–4 | 4–6 | 6–8 | 8–12 | 12–24 | 24–64 | > 64 |
|---|---|---|---|---|---|---|---|---|---|---|
| Baseline | 0/307 | 3% | 8% | 11% | 18% | 45% | 53% | 59–60% | 69–70% | 75% |
| One-way φ_t | 0/267 | 0% | 3% | 7% | 22% | 48% | 54% | 53–58% | 66–69% | 74% |
| Baseline, collision-needed only *(row added in reconciliation)* | 0/307 | 3% | 8% | 11% | 11% | 22% | 19% | 31% (12–16), 25% (16–24) | 24% (24–32), 18% (32–64) | 10% |

- Below 4 × 2M every producing run is collision-needed. Above it, self-folding single packets (item 3) supply a growing share of the production: about half at 6–8 × 2M and most of it above 8 × 2M. So the all-production curve above 4 × 2M says more about single packets than about collisions.
- The one-way variant changes the total only slightly (572 producing against 564) but changes 23% of individual calls. That is the same order as the effect of halving dx.
- Small-amplitude packets pass through at any energy reached: no coarse run with A ≤ 0.3 produces in either form, up to E ≈ 15 × 2M.
- In the slices, production starts at A ≈ 0.35 (σ = 16) and A ≈ 0.45 (k = 1).

**3. Single packets fold on their own.** A single packet with A ≳ 0.4 folds into kink–antikink pairs without any collision, usually within tens of time units.

- Minimum A among self-folding slice points: 0.375–0.425.
- Lowest single-packet energy that self-folds: 2.21 × 2M.
- This holds for 366/564 producing coarse collisions (one-way: 363/572), for 1531/1996 producing points of the σ = 16 slice, and for 723/1162 of the k = 1 slice (728/1193 at dx = 0.05).
- The call and the time the pair forms are unchanged from dx = 0.1 to 0.025 and from dt = 0.04 to 0.005 for the packets tested (A = 0.5 and 0.925 fold; A = 0.3 does not).
- At A close to 1 the initial packet already nearly reaches the barrier top φ = 0. At A ≈ 0.4–0.5 the fold develops dynamically.
- *(Added in reconciliation.)* A one-line estimate gives the threshold. The packet's troughs sit at φ = −1 − A, where V = ¼(A(2 + A))². That exceeds the barrier V(0) = ¼ once A > √2 − 1 = 0.414, so a trough has enough potential energy to swing over the barrier on its own. The observed onset, A = 0.375–0.425, is a little lower because the packet also carries kinetic energy.

Collision-needed production is 3–31% of runs per energy band (one-way: 3–27%). It peaks at 12–16 × 2M and falls to about 10% above 64 × 2M, where self-folding dominates.

**4. The boundary is fractured at the grid scale.** *(Presentation corrected in reconciliation.)* The robust facts come first:

- Along almost every line of fixed k (σ = 16 slice) or fixed σ (k = 1 slice), production switches on and off more than once as A rises: 57 of 57 and 48 of 53 lines.
- The same holds for collision-needed production alone, at half the grid spacing and time step, and in the independent code (σ = 16, k = 1 and k = 2 lines: the same onset, A = 0.375; on the k = 2 line the same gap at A = 0.45–0.5).
- The production fractions are stable under refinement.

The region, hole and switch counts below are illustrative, not converged. They change with dx, and between codes: on the σ = 16, k = 2 line the independent code switches 9 times against our 17.

The operational test was fixed before the slices were inspected:

- A clean threshold would mean one producing region, with production switching on once along each line of fixed k (or σ) as A rises.
- The verdict is CONFIRMED if at least 20% of producing lines switch more than once, or there are at least 3 producing regions of 3 or more points.

| Slice | Producing | Regions (single points) | Enclosed holes | Lines switching > once (mean switches) | Collision-needed: points / regions (single points) |
|---|---|---|---|---|---|
| σ = 16, (A, k), dx 0.1 | 1996/3363 | 24 (15) | 267 | 57/57 (14.8) | 465 / 186 (134) |
| k = 1, (A, σ), dx 0.1 | 1162/3363 | 48 (26) | 141 | 48/53 (13.3) | 439 / 121 (73) |
| k = 1, (A, σ), dx 0.05, dt 0.02 | 1193/3363 | 40 (26) | 153 | 49/53 (12.8) | 465 / 110 (66) |

What is and is not converged:

- **Halving dx and dt keeps the fracture.** Switch density, hole count and regions are similar, and the verdict is CONFIRMED at both resolutions, for all production and for collision-needed production. 83% of individual calls agree; 4 × 4-block production fractions correlate at 0.95 (mean absolute difference 0.06).
- **Collision phase.** Shifting x₀ through one carrier period changes the outcome at 51 of 60 boundary points; 8 always produce and 1 never does. This is a physical parameter of the initial data, not a numerical one.
- **Point-level ladder.** Points whose call flipped between dx = 0.1 and 0.05 keep flipping under further refinement: 0.05 vs 0.025 agree at 15/24, and 0.025 vs 0.0125 at 15/24. Points that did not flip stay fixed (8/8 at every resolution). About 20% of coarse points with E > 2M are of the sensitive kind (dx = 0.05 rerun of 300 points: 80% agree, 143 vs 144 producing).

So the outcome depends sensitively on the initial data, as in multi-kink scattering (`fig_e1d_example.png`). The fine structure lies below any resolution we can afford. The production statistics and the location of the sensitive region are robust; individual point calls and region or hole counts are not converged. They should be read as evidence of fracture, not as numbers.

**5. Speed and width.** *(Rewritten in reconciliation. The earlier text read the matched-energy speed correlation as "slower produces more: CONFIRMED"; the cross-check showed it is confounded with amplitude, and a decisive test confirms that.)*

*Matched energy* (coarse grid; Spearman ρ of producing fraction in E/2M bands [2,4), [4,8), [8,16)):

| Test | Baseline ρ (p) | One-way ρ (p) |
|---|---|---|
| Speed, all production | −0.82 (0.007), −0.87 (0.003), −0.88 (0.002) | −0.78 (0.013), −0.86 (0.003), −0.88 (0.002) |
| Speed, collision-needed | −0.82 (0.007), −0.68 (0.043), −0.13 (0.73) | −0.78 (0.013), −0.66 (0.053), −0.03 (0.93) |
| Width, all production | −0.28 (0.40), −0.28 (0.40), −0.21 (0.53) | 0.00 (1.0), −0.41 (0.20), +0.26 (0.45) |
| Width, collision-needed | −0.28 (0.40), −0.01 (0.97), +0.20 (0.56) | 0.00 (1.0), −0.77 (0.006), −0.17 (0.61) |

- In the [2, 4) band only v_g ≤ 0.47 produces at all.
- **The speed correlation is an amplitude effect.** At matched energy a slow packet is taller: in the [2, 4) band mean A is 0.85–0.90 at v_g ≤ 0.33, against 0.36 at v_g = 0.90 (`e1d_confound.py`). Amplitude controls production.
- **Stored grid, amplitude held fixed.** With A fixed, or A and σ fixed, there is no slow preference. Logistic regression P ~ log A + log σ + v_g gives a v_g coefficient (z) of +0.56 (+1.9) baseline and +0.16 (+0.6) one-way; positive means faster produces more. For collision-needed production it gives −0.18 (−0.6) and −0.53 (−1.7), neither significant. At fixed A and E slower packets do produce more, but there a slower packet must be wider. The (A, σ, v_g) description fits better than (A, E, v_g), with the same number of parameters.
- **Decisive test, fixed packet shape** (`e1d_speedtest.py`, not preregistered; its decision rule was written into the script before it ran). The design is 6 amplitudes (0.5–1.0) × 3 widths (2, 4, 8) × 9 speeds (v_g 0.17–0.90) × 8 collision phases, in both φ_t forms, with a single-packet control for each point: 3,402 runs. A logistic slope on v_g is fitted with one intercept per shape (A, σ); 95% CI, positive = faster produces more:

| Production | Baseline φ_t | One-way φ_t | Baseline at dx 0.05 (σ = 4) |
|---|---|---|---|
| All | +1.36 [+0.80, +1.92] | +0.62 [+0.07, +1.16] | +1.35 [+0.44, +2.27] |
| Packets that do not fold on their own | +1.32 [+0.53, +2.10] | +0.71 [−0.24, +1.67] | +0.84 [−0.32, +2.00] |

  - A real slow preference of half the matched-energy size would give a coefficient of −1.19. Every interval excludes it, and three of the four dx = 0.1 intervals lie entirely above zero.
  - At fixed shape, faster packets produce as much or more, because a faster packet of the same shape carries more energy.
  - The phase-averaged probabilities agree between dx = 0.1 and 0.05: correlation 0.89, mean absolute difference 0.10.
- **Width.** At matched energy there is no width preference in either form or code. At fixed amplitude, wider packets produce more (log σ: z = 13.4 for all production, 2.4 for collision-needed), because they carry more energy. Only the narrowest packets (σ ≤ 1.5) are clearly disfavoured at matched energy. In raw counts wider packets produce more (6/135 at σ = 1, 86/135 at σ = 16).

### E1e, number of quanta

All values are N·λ/m². Energy conservation alone gives N·λ/m² ≥ 2/3.

| Initial state | E/2M | N = E/m | N_lin | Resolution-checked? |
|---|---|---|---|---|
| Gaussian, baseline φ_t: A = 0.8, σ = 2, k = 0.5 (v_g = 0.33); collision needed | 1.86 | **1.24** | **1.69** | yes (dx 0.05, 0.025) |
| Gaussian, one-way φ_t: A = 0.6, σ = 4, k = 0.5; collision needed | 2.70 | **1.80** | **1.96** | yes (dx 0.05, 0.025) |
| Gaussian, raw lowest E: A = 1.4, σ = 1, k = 0.25 | 1.79 | 1.19 | 2.72 | no |
| Gaussian, raw lowest N_lin: A = 0.275, σ = 16, k = 0.2 | 2.26 | 1.51 | 1.53 | no (isolated: 1/121 local neighbours, 1/8 phases) |
| DSV, (0.94, 0.67): lowest-energy converged producer *(reconciliation)* | 7.81 | **5.20** | **4.14** | yes (4th-order time stepping at dx 0.05 and 0.025; same pair time, φ(0, t) agree) |
| DSV, (0.95, 0.62) *(withdrawn in reconciliation)* | 7.17 | 4.78 | 3.93 | leapfrog at dx 0.05: yes; 4th-order time stepping: pair at dx 0.05, none at dx 0.025. Not converged |
| DSV, raw lowest E: (0.90, 0.73) | 6.98 | 4.65 | 3.39 | no (no pair with 4th-order time stepping at dx 0.05 or 0.025) |

- N_lin can exceed E/m for strongly nonlinear data, because the cubic term makes the quadratic energy larger than the true energy.
- The classical minimum found is N_min ≈ (1.2–2) m²/λ. It is an upper bound from the scanned families. Over all initial data the floor 2/3 is approached by the finely tuned time-reversed captures of Findings item 1.
- At λ/m² = 0.01, classical pair-making therefore needs about 120–200 quanta.
- N ≈ 2 would need λ/m² ≈ 0.6–1, which is strong coupling, where the classical description itself fails.

## What it means for the seed

*(Verdicts revised in reconciliation; the earlier verdicts and the reasons for each change are in the Reconciliation section.)*

- **§2, "a fold appears only with an antifold, so the threshold is twice the lightest fold's energy": CONFIRMED** *(was AMENDED)*.
  - The floor holds. Nothing produces below 2M_kink in any run, in our code or in the two independent ones, and every production event is a kink–antikink pair.
  - 2M is also the classical infimum over all initial data. Time-reversed slow captures are kink-free data that make a pair at E → 2M (lattice demonstration at 1.0012 × 2M). They are finely tuned beyond 10⁻⁸.
  - What is family-specific is the onset. Simple packets start producing well above 2M: at 1.86 × 2M (baseline packets), 2.70 × 2M (one-way packets) and 7.81 × 2M (DSV trains, lowest converged producer), and at 0–11% of runs per band below 4 × 2M. These are upper bounds on where production starts within each scanned family. The earlier rationale, that "a classical field needs extra energy for radiation and kink motion", is withdrawn as a general statement.
- **§4, "a small, spread-out packet is linear and passes through": CONFIRMED.** No coarse run with A ≤ 0.3 produces, up to 15 × 2M, in either φ_t form or in the independent codes. The only exception, one isolated slice point at A = 0.275, does not reproduce at dx = 0.05.
- **§4, "pile in enough energy … the packet can fold into a fold–antifold pair": AMENDED.** Packets do fold, and even a single packet with A ≳ 0.4 folds into pairs with no collision; the threshold matches the over-barrier estimate A > √2 − 1. But amplitude, not energy, controls it: at fixed E/2M the producing fraction runs from 0 to about 0.8, and no energy guarantees production (74–75% above 64 × 2M).
- **§4, colliding trains of small pulses make pairs "over a wide range of settings, most easily at low speed" (DSV 2008): AMENDED** *(was CONFIRMED)*.
  - The wide range holds. E1c reproduces DSV's producing band and its trend, high-v pass-through, the hole at (0.91, 0.82) and the null above ω = 0.99.
  - "Most easily at low speed" is neither what DSV report nor what E1c shows. At each ω, production is confined to a velocity band with nothing below it (ω = 0.90: nothing for v < 0.73).
  - The slower bands belong to weaker pulses and cost no less energy. The lowest-energy converged producers sit at v = 0.59–0.79 with E ≈ 7.8–8.2 × 2M; the converged ω = 0.99 producer at v = 0.41 carries 12.3 × 2M.
  - What holds is DSV's own statement: weaker pulses need lower speed, and trains that are too fast pass through.
  - DSV's example point itself is OPEN (resolution-sensitive). DSV-like production at ω = 0.99 is converged at v = 0.41.
- **§4 / §7.1, "the boundary may be ragged rather than one clean threshold": CONFIRMED.**
  - In both slices almost every line of fixed k or σ switches on and off more than once as A rises. This holds for collision-needed production on its own, at half the grid spacing and time step, and in the independent code.
  - The outcome at a point is sensitive to collision phase and to discretisation, down to dx = 0.0125; the producing fractions are stable.
  - Region and hole counts are illustrative, not converged.
  - This matches the character Albayrak & Vachaspati (2026) report in 2D, "fractured … with holes and isolated regions", here in the simplest single-field model.
- **PLAN E1d, "production favours low speed" (from §4 by analogy with DSV 2008 and Albayrak–Vachaspati 2024): REFUTED** *(was part of an AMENDED verdict that said "low speed holds")*.
  - At matched energy slower packets do produce more, in both φ_t forms and in the cross-check. But that is because a slow packet of the same energy is taller, or wider.
  - At fixed packet shape, averaged over collision phase, faster packets produce as much or more. Every 95% interval excludes a slow preference of half the matched-energy size, and three of four lie above zero.
  - Packets that need the collision to produce show the same.
  - Speed as such does not favour production in this model.
- **PLAN E1d, "production favours wide packets": AMENDED** *(was "not supported")*. At fixed amplitude, wider packets produce more (log σ coefficient z = 13.4 for all production, 2.4 for collision-needed). That is because they carry more energy, and more of the packet lies beyond the self-folding threshold. At matched energy there is no width preference in either code.
- **§8 / PLAN E1e, "a classical pair needs N ~ 1/λ quanta": QUANTIFIED.** For Gaussian packets N_min·λ/m² ≈ 1.2–1.8 (N = E/m) or 1.7–2.0 (N_lin). For DSV trains it is 5.20 / 4.14, from the lowest converged producer (0.94, 0.67). The earlier DSV value, 4.78 / 3.93, is withdrawn because that producer is not converged. These are upper bounds from resolution-checked runs; the floor over all initial data is 2/3.
- **§8, "in weakly coupled theories, folding a few quanta into a pair is exponentially rare": OPEN.** The classical route needs N ~ m²/λ, many quanta at weak coupling, which is consistent with the claim. The exponential suppression of few-quanta production is a semiclassical computation (Demidov & Levkov 2011) that E1 does not do.

## Deviations from the plan

1. **Resumed run, third attempt.** All outputs of the earlier attempts (E1a–E1e, figures, results.json) were found complete on disk. They were reused after a reproducibility check: 12 Gaussian and 6 collision runs rerun with identical calls and energies to 10⁻⁹. This attempt added the robustness checks marked "new" above.
2. **E1b headline values.** These are dt → 0 values from a time-step check that was not preregistered; the baseline values also pass. The box-size check was added. Windows 2–5 were compared with a list of unverified provenance.
3. **E1c setup.** L_phys = 600 is our choice; DSV do not state it. Our pair test stands in for their visual judgement. The 1.5T survival check and the dx = 0.05 rerun were added.
4. **E1d initial data.**
   - The baseline uses ω_k at the carrier for φ_t, the literal PLAN wording. For kσ ≲ 2 this sends part of each packet outward.
   - An exact one-way variant was added on the coarse grid and for the smallest producers.
   - The slice rule picked σ = 16, at the edge of the coarse σ range.
5. **E1d tests.** PLAN.md gives no numerical definition of "ragged". The operational test and the matched-energy speed and width tests were fixed after the coarse scan and before the slices were inspected.
6. **Added controls (not preregistered).**
   - Single-packet controls and the collision-phase scan.
   - dx = 0.05 reruns: 300 coarse points and the whole k = 1 slice.
   - The point-level ladder to dx = 0.0125.
   - Probes of the smallest producers.
   - Energy-conservation and reproducibility checks, and the illustrative figure.
7. **E1e definition.** We report N = E/m as preregistered and also N_lin. Headline values count only producers that survive a resolution check.
8. **Reconciliation after the independent cross-check (not preregistered).** Added: a fourth-order time integrator for the DSV runs, with a (dx, dt) ladder down to (0.0125, 0.005) at and near the example point and at the named hole; a neighbourhood ensemble inside DSV's 0.01-wide v cells at ω = 0.99; a lattice demonstration of the time-reversal argument; an amplitude-confound analysis of the stored coarse grid; and a phase-averaged speed test at fixed packet shape, whose decision rule was written into `e1d_speedtest.py` before it ran. DSV Fig. 2 was digitised for a point-by-point comparison. Every verdict change is listed in the Reconciliation section.

## Limitations

- **Classical only.** No quantum suppression or quantum corrections are computed.
- **Pair test and finite time.**
  - The pair test is a heuristic.
  - Multi-pair states and kinks frozen in the absorbing layers count as production.
  - A finite T can miss late production or late annihilation.
- **Chaotic DSV points.** *(Added in reconciliation.)* Some DSV trains leave a long-lived central oscillation whose fate is decided after any two affordable discretisations have separated. DSV's example point (0.99, 0.43) is one of them. For such points a single call means little, at any resolution; only neighbourhood frequencies do. Leapfrog calls on the dx = 0.1 map are not converged point by point.
- **E1d is not converged point by point.** About 20% of coarse points are sensitive: their call changes under refinement and keeps changing down to dx = 0.0125. A change in the φ_t prescription changes 23% of calls. Only statistics (fractions, trends, the presence of fracture) are robust. Region and hole counts depend on resolution.
- **Finite scanned ranges.** A ≤ 1.5, σ ∈ [1, 16], k ∈ [0.2, 3], and two initial-velocity families. N_min is an upper bound, and the lowest producing energy depends on the family (1.86 vs 2.70 × 2M).
- **DSV lattice unknown.** DSV's lattice and boundary details are not stated, so our T and theirs may differ. Their figure was digitised from the PDF to the 0.01 grid.
- **Literature targets.** The E1b targets are [summary], from secondary sources. Our v_c lies 2.6×10⁻⁴ above 0.2598. That is inside the tolerance, not explained by any numerical parameter we varied (dx, dt, x₀, run length, box), reproduced to 10⁻⁵ by an independent code, and within the scatter of published edge values.
- **Mechanism, only estimated.** *(Corrected in reconciliation.)* The self-folding threshold matches a local over-barrier estimate (Findings, item 3), but the dynamics of the fold were not analysed further.

## How to reproduce

Run everything, using 2 worker processes with 1 thread each:

```
cd seed/experiments/E1_phi4
nohup ./run_all.sh > logs/run_all.log 2>&1 &
```

- The script is resumable: each stage is skipped if its output exists, and `e1d_extra.py` resumes from its .jsonl checkpoints.
- Total wall time is about 105 min on two shared cores for the original stages, plus about 85 min for the reconciliation stages.

Measured stage times:

| Part | Command | Time |
|---|---|---|
| E1a | `e1a_static.py` | 3 s |
| E1b | `e1b_kkbar.py`: base / dx0.1 / x0_20 / tpost1500 / dx0.025 | 173 / 52 / 213 / 248 / 672 s |
| E1b | `e1b_dtcheck.py` / `e1b_boxcheck.py` | 109 / 56 s |
| E1c | `e1c_dsv.py`: example / grid / fine / high / dxcheck | 2 / 315 / 348 / 93 / 438 s |
| E1d | `e1d_gauss.py`: coarse / single / sliceAk 16.0 / sliceAs 1.0 / phase / dxcheck | 88 / 41 / 483 / 227 / 72 / 161 s |
| E1d | `e1d_single_slices.py`: σ = 16 slice / k = 1 slice | 350 / 91 s |
| E1d | `e1d_probe_min.py` / `e1d_example.py` | 52 / ~5 s |
| E1d (new) | `e1d_extra.py`: coarse_oneway / single_oneway / slice_dx05 / slice_dx05_single | 105 / 35 / 952 / 333 s |
| E1d (new) | `e1d_dxladder.py` / `e1d_oneway_min.py` | 253 / 16 s |
| Checks (new) | `e1_verify.py` | 26 s |
| Analysis | `analyze_e1b.py`, `analyze_e1c.py`, `analyze_e1d.py`, `e1e_quanta.py`, `analyze_extra.py`, `collect_results.py` | about 1 min |
| Reconciliation | `e1c_reconcile.py` (two passes; resumable) | about 62 min (the two runs at dx = 0.0125 take about 7 min each) |
| Reconciliation | `e1_timereversal.py` / `e1d_speedtest.py run` + `analyze` / `e1c_example_y4.py` | 880 s / 248 s / 47 s |
| Reconciliation | `e1d_confound.py`, `e1c_reconcile_analysis.py`, `reconcile_results.py` | about 2 min |

Outputs:

- `results.json`: every headline number with units and conventions, target, tolerance and verdict, plus `seed_claims` (copied from `seed_claims.json`).
- Details: `e1a_results.json`, `e1b_analysis.json`, `e1c_analysis.json`, `e1d_analysis.json`, `e1e_results.json`, `e1_extra_analysis.json`, `e1d_oneway_min.json`; from the reconciliation, `e1c_reconcile_analysis.json` (with the runs in `e1c_reconcile.jsonl` and `reconcile_data/`), `e1d_confound.json`, `e1d_speedtest.json` (runs in `e1d_speedtest.jsonl`), `e1_timereversal.json`, `dsv_fig2_reading.json`.
- Figures: `fig_e1b_collisions.png`, `fig_e1c_dsv.png` (its φ(x, t) panel is the unconverged leapfrog run of (0.99, 0.43)), `fig_e1d_coarse.png`, `fig_e1d_slices.png`, `fig_e1d_example.png`, `fig_e1d_convergence.png`; from the reconciliation, `fig_e1c_reconcile.png` and `fig_e1c_example_y4.png`.
- Drivers: `run_remaining.sh` and `run_post.sh` (second attempt) and `run_extra*.sh` (this attempt) are the drivers actually used. The older `run_e1*.sh` scripts are kept from the first attempt.

## Reconciliation

*Added after the independent cross-check (`crosscheck/CROSSCHECK.md`, verdict "confirmed with corrections"), which raised four major and five minor issues. An earlier reconciliation pass was interrupted. Its runs and scripts (`e1c_reconcile.py` passes 1–4, `e1_timereversal.py`, `e1d_confound.py`) were reviewed and kept, then extended. None of this was preregistered. It used about 85 min of compute on two cores. `reconcile_results.py` applies every change below to `results.json` and `seed_claims.json`; it is idempotent and is the last stage of `run_all.sh`.*

### Verdict changes

| Item | Before | After | Which side was right |
|---|---|---|---|
| DSV example point (0.99, 0.43) | CALIBRATED | **OPEN** | The cross-check, in part. The call was not demonstrated. But the point is not a clean non-producer either: the finest runs of both integrators make a pair. It is chaotic |
| DSV hole (0.91, 0.82) | CALIBRATED | CALIBRATED, now resolution-checked | — |
| DSV trend, pass-through, ω > 0.99 null | CALIBRATED | CALIBRATED (unchanged; both codes agree) | — |
| §4 DSV paraphrase, "most easily at low speed" | CONFIRMED | **AMENDED** | The cross-check |
| PLAN E1d, "production favours low speed" | part of AMENDED ("low speed holds") | **REFUTED** | The cross-check (amplitude confound), settled by a new decisive test |
| PLAN E1d, "production favours wide packets" | NOT SUPPORTED (not a PLAN verdict word) | **AMENDED** (holds at fixed amplitude only) | — |
| §2, "the threshold is twice the lightest fold's energy" | AMENDED | **CONFIRMED** | The cross-check |
| E1d, no production below 2M (sanity check) | CALIBRATED | **CHECK PASSED** | The cross-check (vocabulary) |
| E1d, k = 1 slice at dx = 0.05 (internal check) | CONFIRMED | **CHECK PASSED** | Vocabulary |
| E1e, DSV trains N_min·λ/m² | 4.78 / 3.93 at (0.95, 0.62) | **5.20 / 4.14** at (0.94, 0.67); old rows OPEN (withdrawn) | Found in this reconciliation |
| E1b, offset of v_c from 0.2598 | "no diagnosis" | lies in the [summary] target | The cross-check |

### Major issue 1: the DSV example point (0.99, 0.43)

The cross-check found that the original code produces at this point at only some (dx, dt) settings, and its two independent codes at none. We added a fourth-order time integrator to the original code: Yoshida's symmetric composition of the same velocity-Verlet step, with the absorbing layer split exactly in every sub-step (`e1c_reconcile.py`). Space, initial data, lattice, run length and pair test are unchanged. With it we ran a (dx, dt) ladder down to (0.0125, 0.005) at and near the point.

Pair calls by code and resolution ("xc" marks runs of the cross-check; "–" means not run):

| Code | dx | dt | (0.99, 0.43) | (0.99, 0.41) |
|---|---|---|---|---|
| original FD4 + leapfrog | 0.1 | 0.04 | pair from t = 1160 (±22.5 at T) | pair from 670 |
| | 0.1 | 0.02 | pair from 780 | none |
| | 0.1 | 0.01 | none (xc) | pair from 610 (xc) |
| | 0.05 | 0.02 | none | none |
| | 0.05 | 0.01 | none (xc) | none (xc) |
| | 0.05 | 0.005 | none (xc) | – |
| | 0.05 | 0.0025 | none | pair from 640 |
| | 0.025 | 0.01 | none (xc) | – |
| | 0.025 | 0.005 | pair from 840 | pair from 590 |
| | 0.025 | 0.0025 | none (xc) | – |
| | 0.0125 | 0.005 | pair from 840 (xc) | – |
| FD4 + 4th-order Yoshida (new) | 0.05 | 0.02 | none | pair from 590 |
| | 0.05 | 0.01 | none | pair from 590 |
| | 0.025 | 0.01 | none | pair from 590 |
| | 0.025 | 0.005 | none | pair from 590 |
| | 0.0125 | 0.005 | **pair from 870** (±128 at T) | pair from 590 |
| cross-check FD6 + RK4 | 0.08 | 0.032 | none | – |
| cross-check spectral, 4th-order splitting | 0.1 / 0.05 / 0.1 | 0.02 / 0.02 / 0.01 | none at all three | pair from 590 at all three |

- **(0.99, 0.41) is a converged producer.** The pair forms at t = 590 in all eight higher-order runs, and the leapfrog converges to that as dt → 0. φ(0, t) of the fourth-order runs agree to 0.1 until t ≥ 668, after the pair has formed. At T the pair is at ±190–207.
- **(0.99, 0.43) is chaotic.** The trains leave a long-lived central oscillation.
  - φ(0, t) of all fourth-order runs agree to 4 × 10⁻⁵ up to t = 500, and to 0.1 up to t = 757–831.
  - The difference between the two finest runs grows from 4 × 10⁻³ at t = 800 to order 1 by t = 850. The pair-or-not decision falls at t ≈ 830–870, after even the two finest runs have separated.
  - Pushing the convergence horizon past t ≈ 870 would need errors 10²–10³ times smaller than the finest run's. That means at least two more halvings of both dx and dt: 16 times its cost per run, about 2 h on one core, and two such runs to check agreement.
  - The finest fourth-order run makes a pair at ±128 at T, close to the ±140 the cross-check read off DSV Fig. 1. So DSV may well have seen this outcome. It is not reproducible at our resolutions: the leapfrog produces at 4 of 11 distinct settings, our fourth-order code at 1 of 5, the cross-check's higher-order codes at 0 of 4.
- **Neighbourhood ensemble** (fourth order, dx = 0.05, dt = 0.02). Inside DSV's 0.01-wide cell around 0.43 (v = 0.425–0.435, step 0.001), 0 of 11 initial data produce. Around 0.41, 3 of 11 do (v = 0.407, 0.41, 0.411). At 0.40 the pair appears at 3 of 4 fourth-order settings (t = 610–640). Production at ω = 0.99 is a sparse, fractured set near v ≈ 0.40–0.41 (`fig_e1c_reconcile.png`, `fig_e1c_example_y4.png`).
- **Verdict.** The original text, "the pair is real: it is still separating at 1.5T", generalised from one unconverged run, and is withdrawn. The cross-check's conclusion, that the call "is a property of the (0.1, 0.04) discretisation", is also too strong: the finest runs of both integrators produce. The example point is **OPEN**: neither "produces" nor "does not produce" can be demonstrated at affordable resolution.
- **What the DSV calibration honestly is.** Reproduced and CALIBRATED in both codes:
  - the producing band and its trend to lower v as ω rises;
  - pass-through at high v;
  - the hole at (0.91, 0.82), now resolution-checked: no pair at four discretisations, while (0.91, 0.80) produces at all four;
  - no production above ω = 0.99.

  Not reproduced point by point: our dx = 0.1 map hits 58 of DSV's 81 producing points, with 22 extra. The example point is chaotic, and DSV-like production in its column is converged 0.02 lower, at v = 0.41.

### Major issue 2: "most easily at low speed"

The cross-check is right. DSV themselves say that higher ω (weaker pulses) requires lower incoming velocity, and that trains that are too fast pass through. Neither DSV's map nor ours shows production that is easiest at low speed.

- At fixed ω there is no production below the velocity band (ω = 0.90: nothing for v < 0.73).
- The slow bands at high ω cost no less energy. The three lowest-energy converged producers are (0.94, 0.67), (0.96, 0.59) and (0.94, 0.79), at E = 7.8–8.2 × 2M. The converged ω = 0.99 producer at v = 0.41 carries 12.3 × 2M.

The §4 claim is **AMENDED**. Pairs form over a wide range, in an ω-dependent velocity band that moves to lower v as the pulses weaken.

### Major issue 3: the low-speed preference is an amplitude effect

The cross-check is right.

- **Stored grid** (`e1d_confound.py`). At matched energy slow packets are taller, and amplitude controls production. With A fixed, or A and σ fixed, there is no slow preference, for all production or for collision-needed production. The one nominally significant stratified result has faster packets producing more.
- **Decisive test** (`e1d_speedtest.py`, 3,402 runs). Packet shape (A, σ) is held fixed, speed is varied over v_g = 0.17–0.90, and the call is averaged over 8 collision phases, in both φ_t forms. The decision rule was fixed in the script before the run: a slow preference half the size of the matched-energy effect would give a logistic coefficient of −1.19.
  - Every 95% interval excludes it.
  - With all production, both forms show faster packets producing more: +1.36 [+0.80, +1.92] baseline, +0.62 [+0.07, +1.16] one-way.
  - Packets that cannot fold on their own give +1.32 [+0.53, +2.10] and +0.71 [−0.24, +1.67].
  - Halving dx (σ = 4 subset) gives +1.35 [+0.44, +2.27].

The PLAN prediction "production favours low speed" is **REFUTED** in this model. "Favours wide packets" is **AMENDED**: it holds at fixed amplitude, where wider packets carry more energy (log σ: z = 13.4), and not at matched energy.

### Major issue 4: the §2 threshold

The cross-check is right that the earlier rationale, "2M is a floor, not the onset; a classical field needs extra energy", holds only for the scanned families.

- The φ⁴ equation is time-reversal invariant, so reversing a slow captured kink–antikink pair gives kink-free initial data that make a pair at E = 2Mγ(v) → 2M.
- `e1_timereversal.py` demonstrates this on the lattice. At v = 0.05 the bound state decays until φ < 0 everywhere (t = 2186). The reversed data hold about 70% of their energy in the remnant bion and the rest in inward radiation, and they make the pair again at E = 1.0012 × 2M (also at v = 0.1: 1.0050 × 2M).
- The construction needs the exact inverse of the forward map. Noise of amplitude 10⁻⁸, a halved time step, or truncating the far radiation each prevents the pair. DSV 2008 (p. 1) describe the same construction and call such data very hard to arrange.

What is shown: the floor (no production below 2M), and that the infimum over all initial data is 2M, approached only by finely tuned data. What is not shown is a property of classical fields in general beyond that. The onsets 1.86, 2.70 and 7.81 × 2M are upper bounds for the Gaussian, one-way and DSV families. The claim is **CONFIRMED**.

### Minor issues

1. **Verdict word for the energy-floor sanity check.** Changed from CALIBRATED to CHECK PASSED; it has no literature target. The internal dx = 0.05 slice check is also CHECK PASSED. Informational rows carry NO_TARGET, which means no verdict.
2. **Slice counts.** Region, hole and switch counts are now labelled illustrative. Findings item 4 leads with the robust facts: almost every line switches more than once, with the same onset in both codes, and the fractions are stable.
3. **Self-folding threshold.** Added the over-barrier estimate A > √2 − 1 = 0.414 (observed 0.375–0.425). Collision-needed fractions per band were added next to all production. Below 4 × 2M every producing run needs the collision.
4. **DSV table.** Replaced by DSV Fig. 2 digitised from the PDF, with hit counts. "Band by band" was withdrawn.
5. **v_c offset.** The independent code agrees to 10⁻⁵, so the 2.6 × 10⁻⁴ offset is in the [summary] target. CALIBRATED stands.

### Found during reconciliation

- **E1e, DSV trains.** The DSV producer that set the E1e count, (0.95, 0.62), is not converged. With fourth-order time stepping it makes a pair at dx = 0.05 but not at 0.025, and φ(0, t) of the two runs separate at t = 168, before the pair forms.
  - We checked the 14 lowest-energy producers of the original map in order of energy. The lowest converged one is (0.94, 0.67), at E = 7.81 × 2M: the same pair time at both resolutions, and φ(0, t) agreeing to 0.1 throughout.
  - The DSV values become N_min·λ/m² = 5.20 (N = E/m) and 4.14 (N_lin). The Gaussian values, which set the headline, are unchanged.
- **Point-level DSV map.** Five of those 14 low-energy producers are not reproduced with fourth-order time stepping. Calls on the dx = 0.1 leapfrog map should be read as a band, not as points.

### Files

New or changed in the reconciliation:

- Code: `e1c_reconcile.py` (passes F and G added), `e1c_reconcile_analysis.py`, `e1c_example_y4.py`, `e1d_confound.py`, `e1d_speedtest.py`, `e1_timereversal.py`, `reconcile_results.py`, `run_all.sh`.
- Data: `e1c_reconcile.jsonl` and `reconcile_data/` (96 runs), `e1c_reconcile_analysis.json`, `e1c_example_y4.npz`, `e1d_confound.json`, `e1d_speedtest.jsonl` (3,402 runs), `e1d_speedtest.json`, `e1_timereversal.json`, `dsv_fig2_reading.json`.
- Figures: `fig_e1c_reconcile.png`, `fig_e1c_example_y4.png`.
- Updated outputs: `results.json` (with a `reconciliation` block) and `seed_claims.json`, where the PLAN E1d prediction is split into its speed and width parts.
