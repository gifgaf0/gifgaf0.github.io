# E10 / Route B, B4: the axisymmetric charged, twisted loop at sign change #66 (n = 3, 5): report

*November 4, 2026. **Label: Exploration.** Run under `PREREG_B4.md`, committed at 8a77cdc before any loop code (head at start: 34df93e). Scope: exactly PREREG_B4 §3–§5. Axisymmetric (ρ, z) only. No 3D run, and Phase 3 was not started. `PREREG_B4.md`, `PREREG_B2B3.md`, `REPORT_B2B3.md`, `REPORT_verify.md`, `README.md`, every existing script and data file, and all E9 files are unmodified. The new code imports the existing modules.*

**Units.** Model units only (PREREG_B2B3 §1, λ = 1): energies in v²/(gv), lengths in 1/(gv). Q is the SU(3)_{C+F} Noether charge under G = diag(0, 1, 0). It is not electric charge, n is not spin, and no particle identification is made.

## Summary

| | Result |
|---|---|
| **n = 3 verdict (M3a, M3b)** | **METASTABLE, "string not required".** Both starts reach R_f = 10.25, with identical E = 1734.5049 (to 5 × 10⁻¹⁰). R_f/r_q = 2.92, τ = 1.000, ω/m = 0.9816, leak 3.3 × 10⁻⁵. The h = 0.125 check __FINE3__. E/(m_bulk Q) = **1.0664**; E/E_disp = **1.0909**. |
| **n = 5 verdict (M5a, M5b)** | **METASTABLE, "string not required".** Both starts reach R_f = 17.25, with identical E = 2888.6388 (to 3 × 10⁻¹¹). R_f/r_q = 5.00, τ = 1.000, ω/m = 0.9810, leak 3.2 × 10⁻⁵. The h = 0.125 check __FINE5__. E/(m_bulk Q) = **1.0656**; E/E_disp = **1.1019**. |
| n-dependence | **None:** the same verdict at n = 3 and n = 5. The n = 5 verdict carries forward: METASTABLE, "string not required". |
| **Passenger control (C-d, C-d5)** | **A bound bulk lump exists.** With no vortex, the seeded charge relaxes to a localized lump, not to box modes. E_disp = 1589.911 at Q₃ (0.9775 m_bulk Q) and 2621.459 at Q₅ (0.9670 m_bulk Q). Leak 1.6 × 10⁻⁴ and 2.5 × 10⁻⁴; 99.4 % and 99.0 % of the charge lies within r < 15; ω/m = 0.955 and 0.948. **E_lump < E_main at both Q**, so both main verdicts carry "string not required". |
| Phase 3 | **Not triggered.** PREREG_B4 §5 writes Phase 3 only after STABLE or METASTABLE *without* the "string not required" qualifier. It was not started. |
| P1 (C-a collapses) | **Holds.** It collapses to the vacuum (E = 3 × 10⁻⁸). |
| P2 (C-b: τ → 0, then collapse; C-c: collapse; 85 %) | **Fails as stated.** C-b collapses, but τ stays at 1.0000 until the core reaches the axis: plain shrinkage, with no unwinding first. C-c collapses (R_f/r_q → 0.70) into the same charged lump as C-d. |
| P3 (C-d disperses, E_disp ≥ m_bulk Q, no bound lump; 75 %) | **Fails.** A bound lump forms with E_disp/(m_bulk Q) = 0.977 and 0.967. |
| P4 (non-collapsing main runs stop within 15 % of R_eq; 70 %) | **Holds.** R_f/R_eq = 0.982 (n = 3) and 0.992 (n = 5), at plaquette resolution 0.25. |
| P5 (verdicts) | METASTABLE at both n (priors: n = 5 ≈ 35 %, n = 3 ≈ 25 %). STABLE (absolute) was < 5 % and did not occur. The author's "overall ≈ 40 % for METASTABLE or STABLE at n = 5" is realised, but with the "string not required" qualifier, which P5 did not foresee. |
| Instrument | Gradient: 5-point FD, worst absolute error 1.2 × 10⁻⁶ (FD round-off floor at E ~ 4 × 10⁴). Gauge invariance: 4 × 10⁻¹⁶. Vacuum: E = 0 exactly. **Regression** (straight segment, flat-weight mode of the same code): ℰ_lattice = 26.414103 against B3 ℰ* = 26.414527, **−1.6 × 10⁻⁵** relative (tolerance 2 × 10⁻³). |

**Read before the summary.**
- **The ring is real at this level.** It is a classical, axisymmetric, charged and twisted loop of the elementary string. Two starts at different radii (R_eq and 1.5 R_eq) relax to the same state, to 10⁻⁹ in E. That state sits 1.8 % (n = 3) and 0.8 % (n = 5) inside the thin-ring radius, and 0.12 % / 0.044 % above the thin-ring energy E_thin = 2πR_eq ℰ*. The ratio of the two energy excesses, 2.7, is close to (5/3)² = 2.8, as expected for O((r_q/R)²) curvature corrections.
- **But it is not the cheapest object carrying this charge.** As PREREG_B4 §2 foresaw, it lies above m_bulk·Q (+6.6 %). It also lies **above a charged bulk lump** that needs no string: +9.1 % at n = 3 and +10.2 % at n = 5. In the language of PREREG_B4 §7, the string is a passenger; the charge binds on its own.
- **The bulk lump is the surprise.** P3 (75 %) expected dispersal to box modes. Instead, both C-d and C-d5 converge to a compact lump with ω < m_bulk and E < m_bulk·Q. Inside it, |det H| < 0.7 out to r ≈ 8 (H ≈ 1 − mm†). That is the same "unhiggsed orientation" structure as the string core, but without winding. C-c (vortex present, no twist) ends in **this same lump**, to 4 × 10⁻¹⁰ in E. Its leftover det-H winding at R_f = 3.5 sits inside the lump's |det H| ≈ 0 region and costs nothing.
- **Only one point, one model, classical, axisymmetric.** These are the λ = 1 BPS point, sign change #66, n ∈ {3, 5}, and h = 0.25 with an h = 0.125 check. The metastability statement concerns only axisymmetric deformations: non-axisymmetric modes (pinching; unwinding via π₁(CP²) = 0) are untested. "Metastable" here means a local minimum of E_Q under the axisymmetric ansatz, found by two starts. It does not mean a computed barrier.

## 1. Commands run

```
pip install scipy numba            # scipy 1.18.1, numba 0.68.1 (deviation 1)
python3 b4_straight.py  > log_b4_straight.txt   # #66 chain regenerated, straight string at (k*, q*) -> b4_straight.json
python3 b4_checks.py    > log_b4_checks.txt     # checks 1, 2, 4 (+ numba vs reference) -> b4_checks.json
python3 b4_run.py REG   > log_b4_REG.txt        # regression (check 3), before any loop run
./b4_chain.sh                                    # M3a M3b M5a M5b C-a C-b C-c C-d C-d5, 4 at a time -> log_b4_<run>.txt
python3 b4_run.py {M3a,M3b,M5a} fine             # h = 0.125 re-relaxations (started by hand, deviation 13)
./b4_chain2.sh                                   # M5b, C-d, C-d5 fine; then b4_analyse.py -> b4_verdicts.json
python3 b4_analyse.py   > log_b4_analyse.txt     # verdicts, PREREG_B4 §5 literally
python3 b4_tables.py    > log_b4_tables.txt      # tables of this report, lump size, b4_results.json
./b4_autocommit.sh                               # WIP commits every 20 min (container restarts); no restart occurred
```

Software: Python 3.13.18, numpy 2.5.3, scipy 1.18.1, numba 0.68.1. One thread per process, four processes on four cores.

## 2. Instrument, software, checks

### 2.1 Model, ansatz and lattice (`b4_axi.py`, kernels `b4_fast.py`, minimiser `b4_lbfgs.py`)

- **Model:** PREREG_B2B3 §1 at λ = 1, G = diag(0, 1, 0), m_bulk = 1.
- **Ansatz:** PREREG_B4 §3, H(ρ, φ, z, t) = U(nφ − ωt) H(ρ, z) U†, U(β) = exp(iβG). W_ρ and W_z are rotated the same way. W_φ and W_t are the dressings.
- **Lattice:** (ρ, z), spacing h.
  - Sites at ρ_i = (i + ½)h: no site sits on the axis, and no link crosses it, which is the natural axis condition.
  - z_j = −20 + jh.
  - H is Dirichlet (= 1) on the column ρ = 40 − h/2 and on the rows z = ±20.
  - Links U = exp(ihW) on ρ- and z-links, all free.
  - The twist field P = W̃_φ + nG and the Gauss-law field X = W̃_t − ωG sit on all sites, free.
- **Discrete functional:**
  - static: Σ_links 2πρ_l |U H(x+μ) − H(x)|² + Σ_plaq 2πρ_p (2/h²) Re Tr(1 − U_plaq) + Σ_sites 2πρ h² (λ²/4)|1 − HH†|²;
  - twist: Σ_links (2π/ρ_l) |U P(x+μ) U† − P(x)|² + Σ_sites (2πh²/ρ) |PH − nHG|²;
  - Gauss law: K = Σ_links 2πρ_l |U X(x+μ) U† − X(x)|² + Σ_sites 2πρ h² [ρ⁻²|[P, X]|² + |XH + ωHG|²].
  - All terms are built like `u3lattice.Lattice2D`.
  - The discretisation is exactly invariant under lattice gauge transformations Ω(ρ, z).
- **E_Q = E_static + E_twist + Q²/(4I),** with I = min_X K/ω² and ω = Q/(2I).
- **Inner solve:**
  - X by preconditioned CG at every evaluation, warm-started.
  - Preconditioner: per component, the weighted lattice Laplacian plus the exact site diagonal, factorised by sparse LU.
  - Tolerance: relative residual 10⁻⁸ during the minimisation, 10⁻¹² for every recorded observable.
- **Gradient:** analytic. The Q²/(4I) term uses the envelope theorem, −ω²∂K_unit at X = X*. The link exponential uses Daleckii–Krein.
- **Minimiser:** plain L-BFGS (`b4_lbfgs.py`; memory 20, Armijo backtracking). Stop at the first of:
  - max|∇| ≤ 10⁻⁶;
  - relative decrease ≤ 10⁻¹⁴ on 5 consecutive iterations;
  - two consecutive line-search failures, the second after a memory reset;
  - 20 000 iterations.
  These options were fixed before any loop run (deviation 3).

### 2.2 Derivation used by the instrument (derived here; not in the PREREG)

__DERIV__

### 2.3 Observables (recorded every 50 iterations and at the end)

- **E:** E_Q above the vacuum, where the vacuum (H = 1, W = 0, W̃_φ = 0) has E = 0 exactly.
- **R_f:** the ρ of the plaquette carrying the gauge-invariant lattice winding of det H.
  - Per plaquette: n_p = (Σ_links arg(det H̄(x) · det U · det H(x+μ)) − arg det U_plaq)/2π.
  - For the elementary string only the first entry winds, so this is its winding (deviation 7). Plaquette resolution is 0.25.
  - Also recorded: the number of vortex plaquettes, and z_f.
- **Charge density:** the Gauss-law density of K at X*.
  - R_q = ⟨ρ⟩ (charge-weighted, 3D measure).
  - r_q = rms distance from the charge-weighted circle (R_q, z_q) (deviation 8).
- **I, ω, ω/m_bulk.**
- **Leak:** the charge fraction with ρ > 36 or |z| > 16, the axis excluded.
- **Twist retention τ:** the charge-weighted mean of 4p(1 − p), with M = 1 − H†H and p = M₂₂/Tr M, over sites with Tr M > 10⁻¹⁰.
  - p = sin²α for the string H = V diag(φe^{iχ}, 1, 1)V†.
  - τ is undefined once H ≈ vacuum (Tr M of indefinite sign): marked "undef.".
  - Q = 0 runs use the unit (ω = 1) Gauss-law density as weight (deviation 9).

### 2.4 Checks before any loop run (`b4_checks.json`, `log_b4_checks.txt`; `REG`)

| check | setting | result |
|---|---|---|
| 1. Gradient vs 5-point FD (step 10⁻⁵) | ring mode, n = 3, Q = 7.3, h = 0.5, random fields; 8 random coordinates in each of H re, H im, W_ρ, W_z, W̃_φ; inner CG to 10⁻¹⁴ | worst relative error 3.0 × 10⁻⁷ (E = 2.2 × 10⁴); flat mode: worst absolute error 1.2 × 10⁻⁶, against the FD round-off floor E·ε/step ≈ 10⁻⁶ (E = 3.9 × 10⁴) |
| 2. Gauge invariance | smooth random Ω(ρ, z) = exp(iθ), \|θ_p\| ≤ 0.25 per component, random fields, n = 3 | E_static: 4.4 × 10⁻¹⁶; E_twist: 2.2 × 10⁻¹⁶; I: 2.2 × 10⁻¹⁶ (relative). Control, H transformed alone: E_static 53461.6 → 53579.8 |
| 2'. numba kernels vs numpy reference | n = 3, Q = 40, random fields | E: 1.1 × 10⁻¹⁵; gradient: 9 × 10⁻¹⁶ (relative) |
| 3. **Regression** | below | **passes, −1.6 × 10⁻⁵** (tolerance 2 × 10⁻³) |
| 4. Vacuum | H = 1, W = 0, W̃_φ = 0, at n = 0 and n = 3, Q = 0 | E = 0.0 and ∇E = 0.0 exactly |

**The straight string at (k*, q*).**
- The V1b fields were not kept (verify_common: under /tmp). `b4_straight.py` regenerated them by replaying the recorded warm-start chain:
  - original grid (dr 0.1, r_max 20): k = 0, q = 0 … 24.8 from the abelian-Higgs initial, then (k, 24.8) from (k − 0.05, 24.8) for k = 0.05 … 0.30;
  - V1b grid: (0.25, 24.8) and (0.30, 24.8), padded;
  - (k*, q*) = (0.2874021089, 24.8), from (0.30, 24.8), exactly as the V1b R-ray u = 1 solve.
- **Every regenerated energy is bit-identical to its record:** 249 + 6 originals, 2 V1b points, and ℰ* = 26.414526647654 (the V1b ray u = 1 value).
- At (k*, q*): I_q = 12.645587, ω = 0.980579, α = π/4, r_q = 3.40964.

**Regression (check 3): how it was done and why it is equivalent.**
- `Axi(mode='flat')` replaces only the two geometric weight functions:
  - the measure 2πρ → 2πR_L;
  - the φ metric ρ² → R_L².
  Every lattice term, the inner Gauss-law solve, the outer W̃_φ, the Dirichlet edge, the start map and the minimiser are the same code paths as the ring runs.
- With R_L = R_eq(3) = n/k*, n = 3 and Q = Q₃, this is exactly a straight string of length 2πR_L, with twist k = n/R_L = k* and charge per length Q/(2πR_L) = q*. Its energy is 2πR_L·ℰ_lattice(k*, q*).
- A literal large-R ring segment cannot reach 2 × 10⁻³ in this box. Curvature corrections are O((r_q/R)²), and R ≤ 40 − 20 leaves them at ~10⁻³–10⁻². The flat-weight mode isolates the discretisation and the functional, which is what the regression tests.
- The geometric weights themselves are tested by checks 1 and 2 (ring mode) and by the curvature scaling in §4.
- The core sits at (20, 0) in the [0, 40] × [−20, 20] box. The ρ = 0 side is a free (Neumann) edge 20 from the core.

| | ℰ | I_q (= I/2πR_L) | ω/m | r_q | τ | leak |
|---|---|---|---|---|---|---|
| B3 radial, V1b grid (b4_straight) | 26.414527 | 12.645587 | 0.980579 | 3.40964 | 1 (α = π/4) | 3 × 10⁻¹¹ (r_max 40) |
| B4 lattice, flat mode, h = 0.25 (REG, 191 its, ftol stop) | 26.414103 | 12.645034 | 0.980622 | 3.41036 | 1.000000 | 1.4 × 10⁻⁵ |
| relative difference | **−1.61 × 10⁻⁵** | | | | | |

The first REG run (179 iterations) ended on a single line-search failure at E = 1732.39543970. It was re-run after adding the memory-reset retry to `b4_lbfgs.py`: same E to 10⁻¹¹ (deviation 3).

## 3. Starts and runs

**Inputs from the JSON** (V1b #66; b4_straight.json).
- k* = 0.2874021089373914, q* = 24.8, ℰ* = 26.414526647654, r_q* = 3.40947.
- **n = 3:** R_eq = 10.438337, Q₃ = 2π(3/k*)q* = 1626.532904, m_bulk·Q₃ = 1626.5329, E_thin = 1732.4233.
- **n = 5:** R_eq = 17.397228, Q₅ = 2710.888173, E_thin = 2887.3721.

**Ring starts** (`b4_axi.ring_start`).
- The straight string's radial profiles h(r), a(r), in the body frame with orientation V = rot12(α*), α* = π/4, are mapped onto the ring by d (distance to the core circle ρ = R₀, z = 0) and χ = atan2(z, ρ − R₀).
  - H = V g(χ)h(d)V†, with g = exp(iχ diag(1, 0, 0)): the first entry winds once in χ, at the start's orientation.
  - W_χ = V(g a(d) g† − diag(1, 0, 0))V† at the link midpoints, U = exp(ihW).
- A smooth lattice gauge transformation Ω = V exp(−iχ m(ρ, z) N)V† then moves the winding off the outer edges.
  - m is a smoothstep mask: 0 within 2 of the branch-cut segment {z = 0, 0 ≤ ρ ≤ R₀}, 1 beyond 8.
  - The winding then sits, gauge-equivalently, along the axis, where H is free.
  - H = 1 is imposed on the Dirichlet sites. The mismatch there is the string tail, ≤ 4 × 10⁻¹⁶.
- W̃_φ is initialised by minimising E_twist alone over it (a quadratic, same CG). Without this, the mapped start carries E_twist ≈ 6400 instead of ≈ 70.

**No-vortex starts (C-d, C-d5)** (`b4_axi.ball_start`).
- H = 1 − f(r) mm†, with:
  - r = √(ρ² + z²);
  - f = (1 − r²/16)² for r < 4, 0 outside;
  - m = (1, 1, 0)/√2, the main starts' orientation α = π/4.
- W = 0, W̃_φ = 0, n = 0.
- Under the ansatz it rotates as U(−ωt) H U†. Since [mm†, G] ≠ 0, I > 0 (I = 13.7 at the start), and the same Q is imposed through Q²/(4I). The start therefore has ω/m ≈ 59 (Q₃) and 99 (Q₅), far above threshold, and the charge is free to spread or to bind.

| run | n | Q | start | R₀ |
|---|---|---|---|---|
| REG | 3 | Q₃ | straight (flat mode) | core at ρ = 20 |
| M3a, M3b | 3 | Q₃ | ring | 10.438, 15.658 |
| M5a, M5b | 5 | Q₅ | ring | 17.397, 26.096 |
| C-a | 0 | 0 | ring | 10.438 |
| C-b | 3 | 0 | ring | 10.438 |
| C-c | 0 | Q₃ | ring | 10.438 |
| C-d | 0 | Q₃ | ball, radius 4 | — |
| C-d5 | 0 | Q₅ | ball, radius 4 | — |

## 4. Per-run histories and end states (h = 0.25)

Rows: every 500 iterations, plus the end (the last row). Full 50-iteration histories are in `b4_hist/<run>.json`.
- R_f: plaquette ρ of the det-H winding (resolution 0.25; z_f = −0.125 in every main run, because the core sits on the z = 0 site row).
- E/(m Q): E/(m_bulk Q).

__HIST__

**Main end states, side by side.**

| | M3a | M3b | M5a | M5b |
|---|---|---|---|---|
| E | 1734.504919 | 1734.504918 | 2888.638808 | 2888.638808 |
| E_static / E_twist / Q²/4I | 868.357 / 67.873 / 798.274 | (same) | 1445.035 / 113.865 / 1329.739 | (same) |
| E/(m_bulk Q) | 1.06638 | 1.06638 | 1.06557 | 1.06557 |
| E/E_disp | 1.09094 | 1.09094 | 1.10192 | 1.10192 |
| E − E_disp | +144.59 | +144.59 | +267.18 | +267.18 |
| E/E_thin − 1 | +1.20 × 10⁻³ | +1.20 × 10⁻³ | +4.39 × 10⁻⁴ | +4.39 × 10⁻⁴ |
| R_f (R_f/R_eq) | 10.25 (0.982) | 10.25 (0.982) | 17.25 (0.992) | 17.25 (0.992) |
| R_q, r_q, R_f/r_q | 11.291, 3.505, 2.92 | 11.291, 3.505, 2.92 | 17.924, 3.447, 5.00 | 17.925, 3.447, 5.00 |
| I, ω/m | 828.54, 0.98157 | 828.54, 0.98157 | 1381.65, 0.98104 | 1381.66, 0.98103 |
| τ | 1.000000 | 1.000000 | 1.000000 | 1.000000 |
| leak | 3.30 × 10⁻⁵ | 3.30 × 10⁻⁵ | 3.20 × 10⁻⁵ | 3.19 × 10⁻⁵ |
| min \|det H\| | 0.018 | 0.018 | 0.017 | 0.017 |
| iterations, stop | 2099, ftol | 3210, ftol | 2274, ftol | 5452, line search (after reset) |
| max\|∇\| at stop | 3.6 × 10⁻⁵ | 4.3 × 10⁻⁵ | 4.6 × 10⁻⁵ | __M5BG__ |

- **Curvature scaling (descriptive).** E/E_thin − 1 = 1.20 × 10⁻³ (n = 3) and 4.39 × 10⁻⁴ (n = 5): ratio 2.74, against (R₅/R₃)² = 2.78. The REG lattice offset (−1.6 × 10⁻⁵) is an order of magnitude smaller.
- **R_q > R_f** because the 2πρ weight puts more charge on the outer side of the core.
- **The b-starts contract monotonically onto the a-states.**
  - M3b: 15.75 → 12.0 (500 its) → 10.75 (1000) → 10.25 (≥ 2000).
  - M5b: 26.0 → 23.25 → 21.25 → 19.5 → 18.25 → 17.5 → 17.25 (≥ 3500).
  - Along the way ω/m rises from 0.654 to 0.981, and τ stays at 1.
- **Controls:**
  - **C-a:** shrinks and annihilates at the axis, with no vortex left by iteration 500. Ends at vacuum, E = 2.7 × 10⁻⁸.
  - **C-b:** shrinks steadily, R_f 10.5 → 4.0 (500) → 0.25 (1000), with τ = 1.0000 throughout. The core leaves through the axis between iterations 1000 and 1100. The end state is vacuum (E = 3 × 10⁻⁷).
  - **C-c:** shrinks fast (R_f = 1.125 with 4 vortex plaquettes at iteration 500). It ends in the charged lump of C-d: E = 1589.91105 against 1589.91105, I and r_q equal to 10⁻⁶. The surviving winding at R_f = 3.5 lies inside the lump's low-|det H| region (ρ < 7.9). R_f/r_q = 0.70 < 1: COLLAPSE.
  - **C-d, C-d5:** the charge spreads from radius 4 within ~500 iterations, then binds. The end states are below.

**Bulk lumps (C-d, C-d5 end states; `log_b4_tables.txt`).**

| | Q | E_disp | E_disp/(m_bulk Q) | ω/m | I | 3D rms radius | charge within r < 5 / 10 / 15 | leak | \|det H\| at origin; \|det H\| < 0.7 for |
|---|---|---|---|---|---|---|---|---|---|
| C-d | 1626.53 | 1589.9110 | 0.97748 | 0.95531 | 851.31 | 7.35 | 0.231 / 0.891 / 0.994 | 1.6 × 10⁻⁴ | 0.154; ρ ≤ 7.9 |
| C-d5 | 2710.89 | 2621.4591 | 0.96701 | 0.94815 | 1429.57 | 8.35 | 0.134 / 0.800 / 0.990 | 2.5 × 10⁻⁴ | 0.145; ρ ≤ 9.6 |

Both are localized (leak < 1 %, finite charge radius), so neither is a box-mode dispersal. E/Q falls with Q (0.977 → 0.967), the usual Q-ball trend.

## 5. h = 0.125 re-relaxations

Every non-collapsing end state (M3a, M3b, M5a, M5b, and the lumps C-d, C-d5) was re-relaxed at h = 0.125: 320 × 321 sites, 4.6 × 10⁶ unknowns. Each run starts from the h = 0.25 end state, interpolated (`b4_run.refine`: bilinear in H, W̃_φ and the link parameters), and uses the same options. The criterion is ΔR_f < 5 % and ΔE < 10⁻³ (relative). For the lumps, which have no R_f, only ΔE is reported.

__FINE__

R_f moves by one fine plaquette because the two staggered grids are not nested: plaquette centres at h = 0.25 are 10.25 and 17.25; at h = 0.125 the nearest are 10.375 and 17.375. That shift is within plaquette resolution.

## 6. Verdicts (PREREG_B4 §5, applied literally; `b4_analyse.py` → `b4_verdicts.json`)

__VERD__

## 7. Deviations, collected

1. **Software installs.** `pip install scipy` (1.18.1; not present in the container) and `numba` (0.68.1; speed only). `py-spy` was installed to diagnose one slow run; it was not used for results.
2. **V1b fields regenerated.** The V1b per-point fields were never committed (they lived under /tmp). "Warm-started from V1b's bracketing solutions" was done by regenerating them via the recorded chain. All regenerated energies are bit-identical (§2.4).
3. **Minimiser and stopping rule (not fixed by the PREREG).** A plain L-BFGS (`b4_lbfgs.py`) replaced scipy's L-BFGS-B, whose bound-constrained bookkeeping cost ~0.6 s per iteration at 1.1 × 10⁶ unknowns. Same energies on the provisional regression test (26.4141017 both).
   - The stop options (§2.1) were fixed before any loop run.
   - The memory-reset retry was added after the first REG run, which ended on one line-search failure. REG was re-run, and every loop run used the final version.
   - Two runs (C-d; M5b) stopped on "line search failed (after memory reset)" rather than ftol. At those points E changes below 10⁻¹³ relative and max|∇| ≤ 7 × 10⁻⁵, the same level as the ftol stops.
4. **W_φ is an outer variable** (interpretation of "dressings W_φ and W_t are solved for; W_t comes from the Gauss law (inner linear solve)"). On the ring the twist and Gauss-law dressings couple through [P, X], so W_φ cannot be eliminated by a separate quadratic solve the way B3's W_z could (§2.2). It is minimised with the other spatial fields. The inner linear solve is W_t only, as the PREREG says. The REG regression confirms the straight-string limit.
5. **Grid edges.** Staggered ρ sites put the Dirichlet column at ρ = 40 − h/2 (39.875 at h = 0.25, 39.9375 at h = 0.125). z edges are at ±20 exactly.
6. **Where the winding sits.** With H = 1 on the outer edges, the start's 2π winding is moved, by a smooth gauge transformation, onto the free axis (§3). This is gauge-equivalent to the standard ring configuration.
7. **"First-entry winding" is measured as the det-H winding.** It is gauge-invariant, and for the elementary string (one winding entry) it equals the first entry's winding. Resolution is one plaquette.
8. **r_q on the ring** is the rms distance of the charge from its charge-weighted circle (R_q, z_q), and R_q = ⟨ρ⟩_charge. For the lumps a 3D rms radius about the origin is added (descriptive).
9. **τ.**
   - The local definition is 4p(1 − p), p = (1 − H†H)₂₂/Tr(1 − H†H).
   - It is undefined in the vacuum: the C-a and C-b end values (e.g. −86) are artefacts of Tr M ≈ 0 with indefinite sign, and are marked "undef.".
   - At Q = 0 (C-a, C-b) the weight is the unit Gauss-law density.
   - Recorded τ is used only before collapse.
10. **Leak band:** ρ > 36 or |z| > 16 (within 4 of the Dirichlet edges, axis excluded).
11. **Reading of the verdict table** (`b4_analyse.py` docstring).
    - EXPANDS means R_f > 36.
    - COLLAPSE requires no vortex plaquette or R_f/r_q < 1. The mechanism is ordered by the first recorded iteration of τ < 0.1, of leak > 1 % / ω ≥ m, and of the collapse.
    - A pair is COLLAPSE / LEAK / EXPANDS only if both starts are. Mixed classes are MARGINAL.
    - E < min(m_bulk Q, E_disp) is required of both starts.
    - E_disp is the C-d (C-d5) end energy.
    None of these readings is decisive here: both pairs are clean.
12. **Mechanism = minimiser path.** L-BFGS is not real-time dynamics. "Unwinding first" against "plain shrinkage" (C-b) describes the order along the minimisation path, which is the only order available in this static instrument.
13. **Run scheduling.** The chain wrapper (`b4_chain.sh`) was stopped while M5b was still running, so that the h = 0.125 runs of M3a, M3b and M5a could start on idle cores. The remainder was run by `b4_chain2.sh`. Inputs and options are unchanged; the M5b process was not interrupted.
14. **C-d / C-d5 use n = 0** (no vortex, hence no twist). The ball profile is above.
15. **The fine check also covers C-d and C-d5** (E only). They are "non-collapsing end states" in the literal sense.
16. **Gradient-check tolerance.** In flat mode two coordinates have small derivatives (0.03, 0.15), and their 5-point FD carries round-off ~10⁻⁶ at E = 3.9 × 10⁴. The absolute error (1.2 × 10⁻⁶) is at that floor.
17. **File sizes.** No file exceeds 20 MB __SIZES__.

## 8. What is and is not established

**Established (classical, λ = 1, sign change #66, axisymmetric, lattice h = 0.25 with an h = 0.125 check):**
- **The thin-ring window of B3 survives closing the string, at n = 3 and at n = 5.**
  - A charged, twisted loop of the elementary string has a local minimum at R_f ≈ 0.98–0.99 R_eq.
  - It holds τ = 1 and ω/m = 0.981, with no leak (3 × 10⁻⁵).
  - Starts at R_eq and 1.5 R_eq reach it to 10⁻⁹ in E.
  - Its energy exceeds the thin-ring estimate only by the expected curvature correction.
- **It is not absolutely stable.** It lies 6.6 % above m_bulk·Q (as predicted in PREREG_B4 §2), and 9–10 % above a charged bulk lump at the same Q.
- **A localized, bound, non-topological charged lump exists in this model at λ = 1** (C-d, C-d5): E/(m_bulk Q) = 0.977 at Q₃ and 0.967 at Q₅, ω/m ≈ 0.95. C-c reaches the same lump from a collapsing vortex ring. The verdict therefore carries **"string not required"**: the cheaper object holding this charge has no string.
- **The controls behave as designed** for the instrument: C-a collapses. C-b collapses (with no twist unwinding along the minimiser path). C-c collapses (into the lump).

**Not established:**
- Any statement beyond axisymmetry: pinching, non-axisymmetric unwinding of the twist (π₁(CP²) = 0), and any barrier height. Phase 3 is not triggered by this result (§5 qualifier) and was not started.
- Any λ other than 1. V3 (REPORT_verify) found the window one-sided (present at λ = 0.9, absent at 1.1).
- Whether the lump is the global minimum at fixed Q. Only one lump start was tried per Q, at one orientation (α = π/4).
- Any quantum statement (the CP² moduli gap, B1 §2), and any particle identification.
- Box dependence of the lump at the level of 10⁻⁴: the leak is 1.6–2.5 × 10⁻⁴, and only one box was run.

## 9. Files

- **Code:** `b4_axi.py` (instrument), `b4_fast.py` (numba kernels), `b4_lbfgs.py`, `b4_straight.py`, `b4_checks.py`, `b4_run.py`, `b4_analyse.py`, `b4_finelist.py`, `b4_tables.py`, `b4_chain.sh`, `b4_chain2.sh`, `b4_autocommit.sh`.
- **Results:** `b4_results.json` (all histories, end states, fine checks, verdicts, checks, straight string), `b4_verdicts.json`, `b4_checks.json`, `b4_straight.json`, `b4_hist/<run>.json`.
- **Logs:** `log_b4_straight.txt`, `log_b4_checks.txt`, `log_b4_REG.txt`, `log_b4_<run>.txt`, `log_b4_<run>_fine.txt`, `log_b4_analyse.txt`, `log_b4_tables.txt`, `log_b4_chain.txt`.
- **Final fields:** `b4_fields/<run>.npz` and `b4_fields/<run>_fine.npz` (packed L-BFGS vector; unpack with `b4_run.make(run, h)[0].unpack(x)`). `b4_fields/straight/{star_0_0, V1b_5_248, V1b_6_248}.npz` hold the radial solutions.
