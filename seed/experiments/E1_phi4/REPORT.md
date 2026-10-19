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
| DSV (ω, v) = (0.99, 0.43) | pair at T (appears at t ≈ 1160), still separating at 1.5T | pair | qualitative | [read] arXiv:0803.0670 | CALIBRATED |
| DSV trend | band moves from v ≈ 0.73–0.85 (ω = 0.90) to 0.41–0.43 (ω = 0.99); Spearman ρ(ω, median v) = −0.99 | lower v as ω rises | qualitative | [read] | CALIBRATED |
| DSV pass-through at high v | 0/10 produce at v = 0.90; 2/60 at v ≥ 0.85 | trains pass through | qualitative | [read] | CALIBRATED |
| DSV holes | (0.91, 0.81–0.82) empty between producing 0.80 and 0.83; 10 single-point holes elsewhere | holes, e.g. (0.91, 0.82) | qualitative | [read] | CALIBRATED |
| DSV, ω > 0.99 | 0 of 72 runs | none found | qualitative | [read] | CALIBRATED |
| E1d: production below 2M_kink | 0 of 19,526 Gaussian runs (pair and single, both φ_t forms, all resolutions) | 0 | exact | energy conservation | CALIBRATED |

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

Our v_c sits 2.6×10⁻⁴ above the [summary] target. That is inside the tolerance but larger than our estimated numerical uncertainty, and we have no diagnosis for it.

For context, Manton, Oleś, Romańczukiewicz & Wereszczyński 2021 (arXiv:2106.05153v2, read) quote the first window as 0.1920 < v < 0.2029. That is about 5×10⁻⁴ below both our edges and the target, so published values of these edges scatter at the 10⁻³ level.

**Windows 2–5** are [0.22414, 0.22896], [0.23723, 0.23974], [0.24407, 0.24556] and [0.24813, 0.24909]. They agree to 2×10⁻⁴ with a literature list of unverified provenance; this comparison was not preregistered. Windows narrower than 10⁻⁴ are not individually converged.

**Resonance check** (not preregistered): the time between the first two bounces grows by 5.30 per window, against one shape-mode period 2π/ω_s = 5.13. This is the Campbell–Schonfeld–Wingate mechanism. See `fig_e1b_collisions.png`.

### E1c compared with DSV Fig. 2

DSV values are our approximate reading of their figure, to about ±0.01.

| ω | DSV producing v | Ours (pair at T, v step 0.01) |
|---|---|---|
| 0.90 | ≈ 0.75–0.86 | 0.73, 0.76–0.79, 0.82–0.85 |
| 0.91 | 0.76–0.80, 0.83–0.85 | 0.76–0.77, 0.80, 0.83–0.85 |
| 0.92 | 0.74, 0.76–0.84 | 0.72–0.74, 0.76–0.77, 0.81–0.84 |
| 0.93 | 0.69–0.82 | 0.70–0.76, 0.78–0.81 |
| 0.94 | 0.67, 0.71–0.80 | 0.67, 0.69–0.79 |
| 0.95 | 0.64–0.77 | 0.62–0.65, 0.67–0.69, 0.71, 0.75, 0.77 |
| 0.96 | 0.59, 0.62, 0.65–0.72 | 0.59, 0.64–0.67, 0.69 |
| 0.97 | 0.58, 0.61–0.66 | 0.57–0.58, 0.60–0.64 |
| 0.98 | 0.49, 0.54–0.55 | 0.50–0.54, 0.56–0.58 |
| 0.99 | 0.43 | 0.41, 0.43 |

- 80 of 510 runs produce, and 72 of them still have the pair at 1.5T.
- The dx = 0.05 rerun agrees on 74 of 78 calls. The four disagreements are band-edge points.
- In the example (`fig_e1c_dsv.png`), a long-lived central oscillation follows the trains' passage. The pair appears at t ≈ 1160, which is 0.97T. On a lattice with T < 1160 the DSV-criterion call would flip, but the pair is real: it is still separating at 1.5T.

## Findings

### E1d, Gaussian packets

Figures: `fig_e1d_coarse.png`, `fig_e1d_slices.png`, `fig_e1d_example.png`, `fig_e1d_convergence.png`.

**1. Energy floor holds, and classical onset lies above it.** No run below 2M_kink produces, out of 19,526 Gaussian runs (pair and single, both φ_t forms, all resolutions). The lowest producing energies:

| Initial data | E/2M | Point | Resolution check | Collision needed? |
|---|---|---|---|---|
| Baseline, raw | 1.79 | A = 1.4, σ = 1, k = 0.25 | not reproduced at dx = 0.05 | — |
| Baseline | 1.86 | A = 0.8, σ = 2, k = 0.5 | reproduced at dx = 0.05 and 0.025 | yes |
| One-way φ_t | 2.70 | A = 0.6, σ = 4, k = 0.5 | reproduced at dx = 0.05 and 0.025 | yes |

The baseline point (A = 0.8, σ = 2, k = 0.5) carries E = 2.90 × 2M in one-way form and does not produce there. For broadband packets the φ_t prescription changes both the energy and the outcome.

**2. No energy threshold; amplitude matters.** On the coarse grid the producing fraction rises slowly and saturates below 1:

| E/2M | < 1.5 | 1.5–2 | 2–3 | 3–4 | 4–6 | 6–8 | 8–12 | 12–24 | 24–64 | > 64 |
|---|---|---|---|---|---|---|---|---|---|---|
| Baseline | 0/307 | 3% | 8% | 11% | 18% | 45% | 53% | 59–60% | 69–70% | 75% |
| One-way φ_t | 0/267 | 0% | 3% | 7% | 22% | 48% | 54% | 53–58% | 66–69% | 74% |

- The one-way variant changes the total only slightly (572 producing against 564) but changes 23% of individual calls. That is the same order as the effect of halving dx.
- Small-amplitude packets pass through at any energy reached: no coarse run with A ≤ 0.3 produces in either form, up to E ≈ 15 × 2M.
- In the slices, production starts at A ≈ 0.35 (σ = 16) and A ≈ 0.45 (k = 1).

**3. Single packets fold on their own.** A single packet with A ≳ 0.4 folds into kink–antikink pairs without any collision, usually within tens of time units.

- Minimum A among self-folding slice points: 0.375–0.425.
- Lowest single-packet energy that self-folds: 2.21 × 2M.
- This holds for 366/564 producing coarse collisions (one-way: 363/572), for 1531/1996 producing points of the σ = 16 slice, and for 723/1162 of the k = 1 slice (728/1193 at dx = 0.05).
- The call and the time the pair forms are unchanged from dx = 0.1 to 0.025 and from dt = 0.04 to 0.005 for the packets tested (A = 0.5 and 0.925 fold; A = 0.3 does not).
- At A close to 1 the initial packet already nearly reaches the barrier top φ = 0. At A ≈ 0.4–0.5 the fold develops dynamically.

Collision-needed production is 3–31% of runs per energy band (one-way: 3–27%). It peaks at 12–16 × 2M and falls to about 10% above 64 × 2M, where self-folding dominates.

**4. The boundary is fractured at the grid scale.** The operational test was fixed before the slices were inspected:

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

**5. Speed and width at matched energy** (coarse grid; Spearman ρ of producing fraction in E/2M bands [2,4), [4,8), [8,16)):

| Test | Baseline ρ (p) | One-way ρ (p) | Result |
|---|---|---|---|
| Speed, all production | −0.82 (0.007), −0.87 (0.003), −0.88 (0.002) | −0.78 (0.013), −0.86 (0.003), −0.88 (0.002) | slower produces more: CONFIRMED in both |
| Speed, collision-needed | −0.82 (0.007), −0.68 (0.043), −0.13 (0.73) | −0.78 (0.013), −0.66 (0.053), −0.03 (0.93) | CONFIRMED in baseline, borderline in one-way |
| Width, all production | −0.28 (0.40), −0.28 (0.40), −0.21 (0.53) | 0.00 (1.0), −0.41 (0.20), +0.26 (0.45) | not supported |
| Width, collision-needed | −0.28 (0.40), −0.01 (0.97), +0.20 (0.56) | 0.00 (1.0), −0.77 (0.006), −0.17 (0.61) | not supported (one band favours narrow) |

- In the [2, 4) band only v_g ≤ 0.47 produces at all.
- Only the narrowest packets (σ ≤ 1.5) are clearly disfavoured.
- In raw counts wider packets produce more (6/135 at σ = 1, 86/135 at σ = 16), but only because they carry more energy at a given A.

### E1e, number of quanta

All values are N·λ/m². Energy conservation alone gives N·λ/m² ≥ 2/3.

| Initial state | E/2M | N = E/m | N_lin | Resolution-checked? |
|---|---|---|---|---|
| Gaussian, baseline φ_t: A = 0.8, σ = 2, k = 0.5 (v_g = 0.33); collision needed | 1.86 | **1.24** | **1.69** | yes (dx 0.05, 0.025) |
| Gaussian, one-way φ_t: A = 0.6, σ = 4, k = 0.5; collision needed | 2.70 | **1.80** | **1.96** | yes (dx 0.05, 0.025) |
| Gaussian, raw lowest E: A = 1.4, σ = 1, k = 0.25 | 1.79 | 1.19 | 2.72 | no |
| Gaussian, raw lowest N_lin: A = 0.275, σ = 16, k = 0.2 | 2.26 | 1.51 | 1.53 | no (isolated: 1/121 local neighbours, 1/8 phases) |
| DSV, (0.95, 0.62) | 7.17 | 4.78 | 3.93 | yes (dx 0.05) |
| DSV, raw lowest E: (0.90, 0.73) | 6.98 | 4.65 | 3.39 | no |

- N_lin can exceed E/m for strongly nonlinear data, because the cubic term makes the quadratic energy larger than the true energy.
- The classical minimum found is N_min ≈ (1.2–2) m²/λ. It is an upper bound from the scanned families.
- At λ/m² = 0.01, classical pair-making therefore needs about 120–200 quanta.
- N ≈ 2 would need λ/m² ≈ 0.6–1, which is strong coupling, where the classical description itself fails.

## What it means for the seed

- **§2, "the threshold is twice the lightest fold's energy": AMENDED.** Nothing produces below 2M_kink in any run. In classical dynamics, though, 2M is a floor and not the onset. Production first appears at 1.86 × 2M (baseline packets), 2.70 × 2M (one-way packets) or 7.2 × 2M (DSV trains), and stays at 0–11% of runs per band below 4 × 2M. The exact 2M threshold belongs to the quantum process the seed cites (Breit–Wheeler); a classical field needs extra energy for radiation and kink motion.
- **§4, "a small, spread-out packet is linear and passes through": CONFIRMED.** No coarse run with A ≤ 0.3 produces, up to 15 × 2M, in either φ_t form. The only exception, one isolated slice point at A = 0.275, does not reproduce at dx = 0.05.
- **§4, "pile in enough energy … the packet can fold into a fold–antifold pair": AMENDED.** Packets do fold, and even a single packet with A ≳ 0.4 folds into pairs with no collision. But amplitude, not energy, controls it: at fixed E/2M the producing fraction runs from 0 to about 0.8, and no energy guarantees production (74–75% above 64 × 2M).
- **§4, colliding trains of small pulses make pairs over a wide range, most easily at low speed (DSV 2008): CONFIRMED.** E1c reproduces DSV Fig. 2 band by band, along with the example point, the hole, high-v pass-through and nothing above ω = 0.99.
- **§4 / §7.1, "the boundary may be ragged rather than one clean threshold": CONFIRMED.**
  - Both slices are fractured, including collision-needed production on its own, and the fracture persists at half the grid spacing and time step.
  - The outcome at a point is sensitive to collision phase and to discretization, down to dx = 0.0125; the producing fractions are stable.
  - This matches the character Albayrak & Vachaspati (2026) report in 2D, "fractured … with holes and isolated regions", here in the simplest single-field model.
- **PLAN E1d, "production favours low speed and wide packets": AMENDED.** Low speed holds at matched energy in both φ_t forms. Width does not; wide packets win only by carrying more energy.
- **§8 / PLAN E1e, "a classical pair needs N ~ 1/λ quanta": QUANTIFIED.** N_min·λ/m² ≈ 1.2–1.8 (N = E/m) or 1.7–2.0 (N_lin) for Gaussian packets, and 4.8 / 3.9 for DSV trains. These are upper bounds from resolution-checked runs.
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

## Limitations

- **Classical only.** No quantum suppression or quantum corrections are computed.
- **Pair test and finite time.**
  - The pair test is a heuristic.
  - Multi-pair states and kinks frozen in the absorbing layers count as production.
  - A finite T can miss late production or late annihilation; the DSV example forms its pair at 0.97T.
- **E1d is not converged point by point.** About 20% of coarse points are sensitive: their call changes under refinement and keeps changing down to dx = 0.0125. A change in the φ_t prescription changes 23% of calls. Only statistics (fractions, trends, the presence of fracture) are robust. Region and hole counts depend on resolution.
- **Finite scanned ranges.** A ≤ 1.5, σ ∈ [1, 16], k ∈ [0.2, 3], and two initial-velocity families. N_min is an upper bound, and the lowest producing energy depends on the family (1.86 vs 2.70 × 2M).
- **DSV lattice unknown.** DSV's lattice and boundary details are not stated, so our T and theirs may differ, and their figure is read only approximately.
- **Literature targets.** The E1b targets are [summary], from secondary sources. Our v_c lies 2.6×10⁻⁴ above 0.2598: inside the tolerance, not explained by any numerical parameter we varied (dx, dt, x₀, run length, box), and within the scatter of published edge values.
- **Mechanism not analysed.** We did not analyse why single packets fold. Focusing from the softer potential on the φ > −1 side (the cubic term) is a guess.

## How to reproduce

Run everything, using 2 worker processes with 1 thread each:

```
cd seed/experiments/E1_phi4
nohup ./run_all.sh > logs/run_all.log 2>&1 &
```

- The script is resumable: each stage is skipped if its output exists, and `e1d_extra.py` resumes from its .jsonl checkpoints.
- Total wall time is about 105 min on two shared cores.

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

Outputs:

- `results.json`: every headline number with units and conventions, target, tolerance and verdict, plus `seed_claims` (copied from `seed_claims.json`).
- Details: `e1a_results.json`, `e1b_analysis.json`, `e1c_analysis.json`, `e1d_analysis.json`, `e1e_results.json`, `e1_extra_analysis.json`, `e1d_oneway_min.json`.
- Figures: `fig_e1b_collisions.png`, `fig_e1c_dsv.png`, `fig_e1d_coarse.png`, `fig_e1d_slices.png`, `fig_e1d_example.png`, `fig_e1d_convergence.png`.
- Drivers: `run_remaining.sh` and `run_post.sh` (second attempt) and `run_extra*.sh` (this attempt) are the drivers actually used. The older `run_e1*.sh` scripts are kept from the first attempt.
