# E1 — A fold in one dimension (φ⁴ in 1+1 D)

## Question

Does the seed's Model A behave as SEED.md §4, §7.1 and §8 say? Before that can be judged, the tools have to reproduce the known φ⁴ answers. The experiment has five parts, all preregistered in PLAN.md §4, E1:

- **E1a.** The static kink: its mass and its shape mode.
- **E1b.** Kink–antikink collisions: the critical velocity v_c and the two-bounce windows.
- **E1c.** The Dutta–Steer–Vachaspati (DSV 2008) breather-train map.
- **E1d.** Colliding Gaussian packets of the field itself (new). Is production bounded below by 2M_kink? Is the production boundary ragged? Does production favour slow, wide packets?
- **E1e.** How many quanta the smallest producing initial states carry, in units of 1/λ.

## Method

**Equations and conventions.** We use the DSV convention throughout:

- 𝓛 = ½φ_t² − ½φ_x² − ¼(φ² − 1)², with equation of motion φ_tt = φ_xx − φ(φ² − 1).
- Vacua φ = ±1, meson mass m = √2.
- Kink tanh(x/√2), with mass M_kink = 2√2/3 and kink width √2.
- Shape mode ω_s = √(3/2).
- Energies are quoted in units of 2M_kink = 4√2/3. Velocities do not depend on the convention.

**Discretization (phi4core.py).**

- Uniform grid with a node at x = 0.
- Fourth-order centred differences for φ_xx.
- Velocity-Verlet (leapfrog) time stepping with dt = 0.4 dx unless stated otherwise.
- Absorbing layers outside |x| < L_phys: a damping term −γ(x)φ_t, with γ rising quadratically from 0 to 1 over a width W, applied by exact exponential splitting.
- Field values beyond the array ends are fixed at −1.
- Energy uses a fourth-order φ_x.

**Pair test.** A "pair" at time t is a maximal interval with φ > 0 that is longer than 4 kink widths (5.66) and has φ > 0.5 on at least 80% of its points. The test searches the whole array, including the absorbing layers, where outgoing kinks are slowed and stopped. This test was fixed in phi4core.py before any E1c or E1d scan was run.

**E1a (e1a_static.py).**

- Newton solve of the discrete static equation, in the antisymmetric sector, at dx = 0.1, 0.05 and 0.025.
- Energy of the relaxed kink.
- Spectrum of the lattice fluctuation operator −∂² + 3φ_k² − 1 by sparse eigensolver.
- Time-domain check: excite the shape mode at amplitude 0.005–0.01 and count zero crossings.
- Moving-kink check: speed and γM at v = 0.3 and 0.6.

**E1b (e1b_kkbar.py, e1b_dtcheck.py).**

- Initial condition: φ = tanh(γ(x+x₀)/√2) − tanh(γ(x−x₀)/√2) − 1, with φ_t from the boost. Each kink moves at speed v toward the other.
- Box: L_phys = 40, W = 30. Half-separation x₀ = 12, about 8.5 kink widths. Run to t = x₀/v + 600.
- Bounces are counted as down-crossings of φ(0,t).
- Classification:
  - escape: φ(0) stays positive and the outermost zero recedes;
  - otherwise capture (bion).
  - The label is the bounce count for an escape, and 0 for capture.
- Scan: v from 0.15 to 0.30 in steps of 0.0001 (1501 runs), then bisection of every label change down to 2×10⁻⁵.
- Convergence checks:
  - dx ∈ {0.1, 0.05, 0.025} at dt = 0.4 dx;
  - x₀ ∈ {12, 20};
  - post-collision time 600 and 1500;
  - a time-step check that bisects v_c and the first-window edges to 10⁻⁵ for seven (dx, dt) pairs.

**E1c (e1c_dsv.py).**

- Initial data exactly as published (DSV eqs. 11–13):
  - sine-Gordon breathers f = −1 + Σ(4/π) arctan[η sin(ωT_n)/cosh(ηωX_n)], with η = √(1−ω²)/ω;
  - N_b = int[2/√(1−ω²)] + 1 breathers per train;
  - a = 10/√(1−ω²), d = 2/√(1−ω²).
- DSV do not state their lattice size. We used L_phys = 600 (the span of their Fig. 1), absorbing layers of width 60, and dx = 0.1.
- Evolution for one light-crossing time, T = 2L_phys = 1200. The DSV call is "pair present at t = T".
- We also continued to 1.5T to check that the pair survives.
- Grids:
  - ω = 0.90, 0.91, …, 0.99 with v = 0.40–0.90 in steps of 0.01 (510 runs);
  - ω ∈ {0.992, 0.995} with v = 0.20–0.90 (72 runs);
  - a dx = 0.05 rerun of the columns ω = 0.91, 0.95, 0.99 (78 runs).

**E1d (e1d_gauss.py and follow-ups).**

- Initial condition: φ = −1 + Σ± A exp(−(x∓x₀)²/2σ²) cos(k(x∓x₀)), with φ_t = ±Aω_k G sin(·) and ω_k = √(k² + 2). This is the narrow-band form of "φ_t from the linear dispersion". The group velocity is v_g = k/ω_k.
- Fixed rules:
  - x₀ = 4σ + 10;
  - t_coll = x₀/v_g;
  - T = max(t_coll + 400, 1.25(t_coll + 100));
  - L_phys = x₀ + 4σ + 40, W = 50;
  - dx = 0.1, dt = 0.04.
- Production criterion: a pair present at each of 0.80T, 0.85T, 0.90T, 0.95T and T.
- Energy is computed from the discrete initial data.
- Coarse 3D grid (1485 runs):
  - A = 0.1–1.5 in steps of 0.1;
  - σ ∈ {1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 16};
  - k ∈ {0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3}, so v_g = 0.17–0.90.
- Two 59 × 57 slices, chosen by a rule fixed in choose_slices.py before the coarse scan finished (the coarse σ and k with the most producing runs):
  - (A, k) at σ = 16: A from 0.05 to 1.5 in steps of 0.025, k from 0.2 to 3.0 in steps of 0.05;
  - (A, σ) at k = 1: σ from 1 to 16, log-spaced.
- Controls:
  - **Single-packet runs.** The right-moving packet alone, run for every producing coarse and slice point.
  - **Collision phase.** 60 random boundary points of the σ = 16 slice, each with x₀ shifted over one carrier-phase period πk in 8 steps.
  - **Grid spacing.** dx = 0.05 reruns of 300 random coarse points with E > 2M.
  - **Smallest producers.** dx = 0.05 reruns of the five smallest-N and five smallest-E producers; an 11 × 11 local grid around the smallest-N producer; 8 phase shifts of it.

**E1e (e1e_quanta.py).** Write Φ = vφ and x → x/(√λ v). Then S = v²S̃, so the classical dynamics does not depend on φ₀ = v. With ħ = 1, the number of quanta is

- N = E/m = φ₀² Ẽ/√2, with φ₀² = m²/(2λ),
- so N·λ/m² = Ẽ/(2√2).

λ/m² is the dimensionless coupling in 1+1 D. We also report the free-field occupation number of the fluctuation about −1, N_lin = Σ_q(|π_q|² + ω_q²|δ_q|²)/(2ω_q), using the lattice dispersion of the stencil.

**Runs and threads.** Two worker processes with one thread each, on a shared 4-core machine.

## Calibration

| Quantity | Ours | Target | Tolerance | Source | Verdict |
|---|---|---|---|---|---|
| M_kink | 0.9428090346 (dx = 0.025; rel. err. −7.4×10⁻⁹; dx = 0.05: −1.2×10⁻⁷) | 2√2/3 = 0.9428090416 | 10⁻⁴ relative | exact | CALIBRATED |
| ω_s | 1.2247448677 (lattice eigenvalue, −3.0×10⁻⁹); time-domain 1.224749 (+3.4×10⁻⁶) | √1.5 = 1.2247448714 | 10⁻⁴ relative | exact | CALIBRATED |
| v_c | **0.26006 ± 0.00003** (dt → 0); baseline dx = 0.05, dt = 0.02: 0.26016 | 0.2598 | ±0.001 | [summary] CSW 1983 / Anninos et al. 1991 | CALIBRATED |
| First two-bounce window | **[0.19257, 0.20344]** (dt = 0.005); baseline [0.19268, 0.20354] | [0.1926, 0.2034] | ±0.003 per edge | [summary, one source] | CALIBRATED |
| ≥ 3 windows, narrowing toward v_c | 20 windows; widths 0.0109, 0.0048, 0.0025, 0.0015, 0.00096, 0.00066, 0.00048, … | ≥ 3, narrowing | qualitative | [summary] | CALIBRATED |
| DSV (ω, v) = (0.99, 0.43) | pair at T, still separating at 1.5T | pair | qualitative | [read] arXiv:0803.0670 | CALIBRATED |
| DSV trend | producing band moves from v ≈ 0.73–0.85 (ω = 0.90) to 0.41–0.43 (ω = 0.99); Spearman ρ(ω, median v) = −0.99 | lower v as ω rises | qualitative | [read] | CALIBRATED |
| DSV pass-through at high v | 0/10 produce at v = 0.90; 2/60 at v ≥ 0.85 | trains pass through | qualitative | [read] | CALIBRATED |
| DSV holes | (0.91, 0.81–0.82) empty between producing 0.80 and 0.83; 10 single-point holes elsewhere | holes, e.g. (0.91, 0.82) | qualitative | [read] | CALIBRATED |
| DSV ω > 0.99 | 0 of 72 runs (ω = 0.992, 0.995; v = 0.20–0.90) | none found | qualitative | [read] | CALIBRATED |
| E1d: no production below 2M_kink | 0 runs; lowest producing E/2M = 1.79 | 0 | exact | energy conservation | CALIBRATED |

**E1b convergence.** All runs use x₀ = 12 and a post-collision time of 600 unless stated.

| Configuration | dx | dt | v_c | Window 1 |
|---|---|---|---|---|
| dx0.1 | 0.1 | 0.04 | 0.26044 | [0.19303, 0.20388] |
| base | 0.05 | 0.02 | 0.26016 | [0.19268, 0.20354] |
| dx0.025 | 0.025 | 0.01 | 0.26008 | [0.19259, 0.20346] |
| x₀ = 20 | 0.05 | 0.02 | 0.26016 | identical to base |
| post time 1500 | 0.05 | 0.02 | 0.26017 | identical to base |
| dt check | 0.1, 0.05, 0.025 | 0.01 | 0.260079 / 0.260079 / 0.260085 | [0.19259, 0.20346] |
| dt check | 0.05, 0.025 | 0.005 | 0.260065 / 0.260065 | [0.19257, 0.20344] |

At fixed dt the results do not depend on dx, to within 10⁻⁵. The whole drift is leapfrog time error of second order: Richardson extrapolation of the dx series gives order 1.94–2.0. Extrapolating dt → 0 gives v_c = 0.26006 and window 1 = [0.19256, 0.20343].

Windows 2–5 are [0.22414, 0.22896], [0.23723, 0.23974], [0.24407, 0.24556] and [0.24813, 0.24909]. They agree to 1.6×10⁻⁴ with a literature list whose provenance we could not verify; this comparison was not preregistered. The narrowest windows near v_c, below 10⁻⁴ wide, differ between configurations and are not individually converged.

Resonance check (not preregistered): the time between the first two bounces grows by 5.30 per window, against one shape-mode period 2π/ω_s = 5.13. This is the Campbell–Schonfeld–Wingate picture. See fig_e1b_collisions.png.

**E1c compared with DSV Fig. 2.** DSV values are our approximate reading of their figure, to about ±0.01.

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

- 80 of 510 runs produce; 72 of them still have the pair at 1.5T.
- Some pairs vanish after T. These are mostly multi-pair states, and in some cases fast kinks reach the end of the array.
- The dx = 0.05 rerun agrees on 74 of 78 calls. The four disagreements are band-edge points at ω = 0.91 and 0.95.
- In the (0.99, 0.43) example (fig_e1c_dsv.png, right panel), the trains have passed each other by t ≈ 660. A long-lived oscillating lump then sits at the centre, and the pair appears only at t ≈ 1150, separating at about 0.41c. With a lattice giving T < 1150, the DSV-criterion call would flip, but the pair is real: it is still present and separating at 1.5T.

## Findings

**E1d, Gaussian packets.** Figures: fig_e1d_coarse.png, fig_e1d_slices.png, fig_e1d_example.png.

1. **Energy bound holds.** No run below 2M_kink produces, out of about 9,000 Gaussian runs. The lowest producing energy is 1.79 × 2M at A = 1.4, σ = 1, k = 0.25, but that call does not reproduce at dx = 0.05. The lowest producer that does reproduce is 1.86 × 2M at A = 0.8, σ = 2, k = 0.5, and it needs the collision.

2. **No energy threshold; amplitude matters.** On the coarse grid the producing fraction rises slowly and never reaches 1:

   | E/2M | < 1.5 | 1.5–2 | 2–3 | 3–4 | 4–6 | 6–8 | 8–12 | 12–24 | 24–64 | > 64 |
   |---|---|---|---|---|---|---|---|---|---|---|
   | Producing | 0/307 | 3% | 8% | 11% | 18% | 45% | 53% | 59–60% | 69–70% | 75% |

   Small-amplitude packets pass through at any energy: no coarse run with A ≤ 0.3 produces, even at E ≈ 15 × 2M. In the slices, production starts at A ≈ 0.35 (σ = 16) or A ≈ 0.45 (k = 1). That is roughly where the superposed excursion −1 + 2A of the two overlapping packets approaches the barrier top φ = 0; this is a heuristic, not a fitted rule.

3. **Single packets fold on their own.** A single packet with A ≳ 0.4 (the minimum A among self-folding slice points is 0.375–0.425) and enough energy (pair-run E ≳ 4.5 × 2M) folds into kink–antikink pairs without any collision, usually within a few tens of time units of its start. This holds for:
   - 366 of the 564 producing coarse collisions;
   - 1531 of 1996 producing points in the σ = 16 slice;
   - 723 of 1162 producing points in the k = 1 slice.

   Production that needs the collision makes up 3–31% of runs in each energy band. It peaks at about 30% around 12–16 × 2M and falls to 10% above 64 × 2M, where self-folding dominates.

4. **The boundary is ragged, fractured at the grid scale.** Operational test, fixed before the slices were inspected:
   - A clean threshold would mean one producing region, and production switching on once along each line of fixed k (or σ) as A rises.
   - CONFIRMED means at least 20% of producing lines switch more than once, or at least 3 producing regions of 3 or more points.

   Results:

   | Slice | Producing | Regions (single points) | Enclosed holes | Lines switching > once | Collision-needed: points / regions (single points) |
   |---|---|---|---|---|---|
   | σ = 16, (A, k) | 1996/3363 | 24 (15) | 267 | 57/57, mean 14.8 switches per line | 465 / 186 (134) |
   | k = 1, (A, σ) | 1162/3363 | 48 (26) | 141 | 48/53, mean 13.3 | 439 / 121 (73) |

   What sets the fine structure:
   - **Collision phase.** At 60 boundary points, shifting x₀ through one carrier period changes the outcome at 51; 8 always produce and 1 never does.
   - **Grid spacing.** Halving dx changes the call for 20% of 300 random coarse points. The aggregate does not move: 143 producing at dx = 0.1, 144 at dx = 0.05, and per-band fractions agree within 0.04–0.09.

   So the outcome at a single point is not converged, while the statistics are. This is sensitive dependence on initial data, the kind seen in multi-kink interactions (fig_e1d_example.png). The counts of regions and holes depend on resolution and should be read as evidence of fracture, not as converged numbers.

5. **Speed and width, at matched energy (coarse grid).**
   - **Slower packets produce more.** Spearman ρ between producing fraction and v_g is −0.82, −0.87 and −0.88 (p = 0.007, 0.003, 0.002) in the bands E/2M ∈ [2,4), [4,8), [8,16). In [2,4) only v_g ≤ 0.47 produces at all. For collision-needed production alone, ρ = −0.82 and −0.68 in the two lower bands; −0.13 in [8,16) is not significant.
   - **Width shows no trend.** ρ = −0.28, −0.28, −0.21 (p ≥ 0.40). Only the narrowest packets (σ ≤ 1.5) are clearly disfavoured.
   - In raw counts wider packets produce more (6/135 at σ = 1, 86/135 at σ = 16), but only because they carry more energy at a given A.

**E1e, number of quanta.** Energy conservation alone gives N·λ/m² ≥ 2/3. All values below are N·λ/m².

| Initial state | E/2M | N = E/m | N_lin | Reproduced at dx = 0.05? |
|---|---|---|---|---|
| Gaussian, A = 0.8, σ = 2, k = 0.5 (v_g = 0.33); collision needed | 1.86 | **1.24** | **1.69** | yes |
| Gaussian, raw lowest energy: A = 1.4, σ = 1, k = 0.25 | 1.79 | 1.19 | 2.72 | no |
| Gaussian, raw lowest N_lin: A = 0.275, σ = 16, k = 0.2 | 2.26 | 1.51 | 1.53 | no |
| DSV, (0.95, 0.62) | 7.17 | 4.78 | 3.93 | yes |
| DSV, raw lowest energy: (0.90, 0.73) | 6.98 | 4.65 | 3.39 | no |

- The raw lowest-N_lin Gaussian run is isolated: none of its 120 neighbours on a ΔA = 0.005, Δk = 0.01 grid produce, and only 1 of 8 phase shifts does.
- For strongly nonlinear initial data N_lin can exceed E/m, because the cubic term makes the quadratic energy larger than the true energy. Both counts are O(1)·m²/λ.
- The classical minimum we found is N_min ≈ (1.2–1.7) m²/λ. It is an upper bound from the scanned sets.
- At λ/m² = 0.01, classical pair-making therefore needs about 120–170 quanta. N ≈ 2 would require λ/m² ≈ 0.6–0.8, which is strong coupling, where the classical description itself fails.

## What it means for the seed

- **§2, "the threshold is twice the lightest fold's energy": AMENDED.** No production below 2M_kink, as required. In classical collisions, though, 2M is a lower bound and not the onset. Production first appears at about 1.8 × 2M for packets and about 7 × 2M for DSV trains, and stays rare (3–8% of runs) up to 3 × 2M. The kinematic threshold 2M belongs to the quantum process the seed cites (Breit–Wheeler); a classical field needs extra energy for radiation and kink kinetic energy.
- **§4, "a small, spread-out packet is linear and passes through": CONFIRMED.** No coarse run with A ≤ 0.3 produces, even at 15 × 2M. The only exception, one isolated point at A = 0.275, does not reproduce at dx = 0.05.
- **§4, "pile in enough energy … the packet can fold into a fold–antifold pair": AMENDED.** Packets do fold. Amplitude, not energy, controls it: at fixed E/2M the producing fraction runs from 0 to about 0.8, and no energy guarantees production. New: a single packet with A ≳ 0.4 and enough energy folds into pairs without any collision.
- **§4, "colliding trains of small pulses make kink–antikink pairs over a wide range of settings, most easily at low speed (DSV 2008)": CONFIRMED.** E1c reproduces DSV Fig. 2 band by band, together with the example point, the hole, high-v pass-through and nothing above ω = 0.99.
- **§4 / §7.1, "the boundary may be ragged rather than one clean threshold": CONFIRMED.** Both slices are fractured, including collision-needed production on its own. The outcome is sensitive to collision phase and to discretization, while the producing fractions are stable. This matches the character Albayrak & Vachaspati (2026) report in 2D, "fractured … with holes and isolated regions", here in the simplest model.
- **PLAN E1d, "production favours low speed and wide packets": AMENDED.** Low speed is CONFIRMED at matched energy. Width is not supported at matched energy; wide packets win only by carrying more energy.
- **§8, "a classical pair needs N ~ 1/λ quanta": QUANTIFIED.** N_min·λ/m² ≈ 1.2 (N = E/m) to 1.7 (N_lin) for Gaussian packets, and 4.8 / 3.9 for DSV trains. These are upper bounds from runs reproduced at dx = 0.05.
- **§8, "in weakly coupled theories, folding a few quanta into a pair is exponentially rare": OPEN.** The classical result shows that the classical route needs N ~ m²/λ, i.e. many quanta at weak coupling. The exponential suppression of few-quanta production needs a semiclassical computation (Demidov & Levkov 2011), which E1 does not do. Our numbers are consistent with that picture but do not establish it.

## Deviations from the plan

1. **Resumed run.** We reused the interrupted agent's E1a, E1b scans and E1c example and grid after sanity checks. We added the E1b dt check, the rest of E1c, all of E1d and E1e.
2. **E1b headline values.** The headline v_c and window edges are dt → 0 values from a time-step check that was not preregistered. The baseline values are also within tolerance. Windows 2–5 were compared with a list of unverified provenance.
3. **E1c setup.** The lattice size L_phys = 600 is our choice; DSV do not give it. Our pair test (interval > 4 kink widths, φ > 0.5 on ≥ 80%) stands in for their visual judgement. We added the 1.5T survival check and the dx = 0.05 rerun.
4. **E1d initial data and slices.** The initial φ_t is the narrow-band form; the envelope-derivative term is dropped, which matters for σ ≈ 1. The slice rule picked σ = 16, which sits at the edge of the coarse σ range.
5. **E1d tests.** PLAN.md gives no numerical definition of "ragged". The operational test and the matched-energy speed and width tests were fixed during the run, after the coarse scan and before the slices were inspected.
6. **Added controls (not preregistered).** Single-packet controls (prompted by the coarse result), the collision-phase diagnostic, the dx = 0.05 reruns, the probe of the smallest producers, and the illustrative figure.
7. **E1e definition.** We report N = E/m as preregistered and also N_lin. The headline counts only producers that reproduce at dx = 0.05.

## Limitations

- **Classical only.** This is classical field theory. Quantum suppression and quantum corrections are not computed.
- **Pair test and finite time.**
  - The pair test is a heuristic.
  - Multi-pair states and kinks frozen in the absorbing layers count as production.
  - A finite T can miss late production or late annihilation; the DSV example forms its pair at 0.96T.
- **E1d is not converged point by point.** About 20% of calls change when dx is halved. Only statistics (fractions, trends) are robust. Region and hole counts depend on resolution.
- **Scanned ranges are finite.** A ≤ 1.5, σ ∈ [1, 16], k ∈ [0.2, 3]. N_min is an upper bound.
- **DSV lattice unknown.** DSV's lattice and boundary details are unknown, so our T and theirs may differ, and their figure is read only approximately.
- **Literature targets.** The E1b targets are [summary], from secondary sources. Our v_c lies 0.00026 above 0.2598, inside the tolerance.
- **Mechanism not analysed.** We did not analyse why single packets fold; modulational self-focusing, from the softer potential on the φ > −1 side, is a guess.

## How to reproduce

Run everything with:

```
cd seed/experiments/E1_phi4
nohup ./run_all.sh > logs/run_all.log 2>&1 &
```

The script is resumable: each stage is skipped if its output exists. It uses 2 worker processes with 1 thread each. Total wall time was about 71 min on two shared cores.

Measured stage times:

| Part | Command | Time |
|---|---|---|
| E1a | `e1a_static.py` | 3 s |
| E1b | `e1b_kkbar.py`: base / dx0.1 / x0_20 / tpost1500 / dx0.025 | 173 / 52 / 213 / 248 / 672 s |
| E1b | `e1b_dtcheck.py` | 109 s |
| E1c | `e1c_dsv.py`: example / grid / fine / high / dxcheck | 2 / 315 / 348 / 93 / 438 s |
| E1d | `e1d_gauss.py`: coarse / single / sliceAk 16.0 / sliceAs 1.0 / phase / dxcheck | 88 / 41 / 483 / 227 / 72 / 161 s |
| E1d | `e1d_single_slices.py`: σ = 16 slice / k = 1 slice | 350 / 91 s |
| E1d | `e1d_probe_min.py` | 52 s |
| E1d | `e1d_example.py` | about 5 s |
| Analysis | `analyze_e1b.py`, `analyze_e1c.py`, `analyze_e1d.py`, `e1e_quanta.py`, `collect_results.py` | about 1 min |

Outputs:

- `results.json` holds every headline number with units, conventions, target, tolerance and verdict.
- Details are in `e1a_results.json`, `e1b_analysis.json`, `e1c_analysis.json`, `e1d_analysis.json` and `e1e_results.json`.
- Figures: `fig_e1b_collisions.png`, `fig_e1c_dsv.png`, `fig_e1d_coarse.png`, `fig_e1d_slices.png`, `fig_e1d_example.png`.
- `run_remaining.sh` and `run_post.sh` are the drivers this resumed run actually used. The older `run_e1*.sh` scripts are kept from the interrupted attempt.
