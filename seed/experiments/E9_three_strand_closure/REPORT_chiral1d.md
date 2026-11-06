# E9 chiral term, 1D calculations (γ_c and screening): report

November 1, 2026. Label: Exploration. Scope: `NOTE_chiral_term.md` §8 items 1 and 2 only. The model, method and predictions are those of `PREREG_chiral1d.md`, which was committed (dbaa172) before any calculation code. No loop, no 3D and no loop pre-registration were done. κ = 2 (e = 1/√12). η ∈ {0.1, 0}. n̂ ∈ {z = (0,0,1), diag = (1,1,1)/√3, perp = (1,−1,0)/√2}.

**Units.** Model units only (`gl3.py` coordinates, ξ = 1/√2). "gain" means E/P − e_vac, the energy per unit length above the uniform vacuum. It is per unit area of the plane perpendicular to n̂. No particle identification is made.

## Summary

| | Result |
|---|---|
| γ_c, A free (η = 0.1) | z: **0.3746**, diag: **0.3535**, perp: **0.3875**. Each matches the linear-instability threshold of the vacuum to within the bisection tolerance (continuous transition). |
| γ_c, A free (η = 0) | **Consistent with 0.** The search stops at the tolerance floor (bracket [0.0006, 0.0013]). The instability is a uniform (q = 0) state with gain = −0.75 γ² (analytic and numeric). |
| γ_c, A ≡ 0 | η = 0.1: z 0.4801, diag 0.7754, perp 0.3963. η = 0: 0.0789 for all n̂. That is 2π/80, the smallest wavenumber the largest cell allows. |
| Ratio γ_c(A free)/γ_c(A ≡ 0) | 0.780, 0.456, 0.978 (η = 0.1); 0.016 (η = 0). **The gauge field lowers γ_c. It enhances the chiral gain; it does not screen it.** |
| Optimal texture just above γ_c | **Not director-type.** It is a relative-phase texture with S ≠ 0: ⟨\|S\|/\|ψ\|²⟩ = 0.54–0.55 (A free, η = 0.1) and ≈ 0.99 (p + ip-like, η = 0). The director stays on the vacuum axis (1,1,1) and turns by less than 1° per cell. |
| Director (real-ψ) sector alone | Linear threshold γ ≈ 3.0 (η = 0.1) and 2.83 = 2√2 (η = 0). That is about 8× above the phase-sector γ_c. |
| P1 | **Holds.** |
| P2 | (no prior) γ_c = 0 with A free. With A ≡ 0 the value is limited by the cell size. |
| P3 | **Fails.** |
| P4 | **Fails** (5 of 6 cases outside 1 ± 0.05; only perp, η = 0.1 is inside). |
| P5 | **Not met as written.** The unrelaxed chiral energy is exactly 0, which holds. At η = 0 the winding survives and chiral/gradient = 2 × 10⁻⁵, which holds. At η = 0.1 the winding unwinds through a near-zero of \|ψ₁\| to the vacuum, and the "< 1 %" test then compares round-off numbers and fails literally (§6). |

## 1. Commands run

```
cd seed/experiments/E9_three_strand_closure
pip install scipy                                         # not present in the container (deviation 1)
OMP_NUM_THREADS=1 nohup python3 chiral1d.py > run_stdout.txt 2>&1 &   # writes log_chiral1d.txt, chiral1d_results.json; 12 579 s
python3 tables_chiral1d.py > tables_chiral1d_output.txt   # read-only tables for this report
python3 p5_trace_chiral1d.py | tee log_p5_trace.txt        # P5 relaxation trace (deviation 5)
python3 director_lin_chiral1d.py | tee log_director_lin.txt  # director-sector linear threshold (descriptive, deviation 5)
```

## 2. Software, discretization, checks

- Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1 (pip). 4 cores, 4 workers.
- **Lattice.** M = round(P/0.05) sites, h = P/M, periodic.
  - ψ_k sits on sites. A_∥ = n̂·A sits on links (U_s = e^{−ieh A_∥}). A_⊥ (2 components, in a basis perpendicular to n̂) sits on sites.
  - Σ_jk|D_jψ_k|² = Σ_k|D_sψ_k|² + e²|A_⊥|²|ψ|² holds exactly, using the covariant forward difference.
  - Magnetic term: ½|A_⊥'|², by forward difference.
  - **Chiral term:** the covariant central difference h Σ ψ*·(n̂×[U_sψ(s+1) − U*_{s−1}ψ(s−1)])/(2h), plus h Σ (−ie)ψ*·(A_⊥×ψ). Its complex value is real identically. The code evaluates the equal form Σ Re[ψ*(s)·(n̂×U_sψ(s+1))] + h Σ Re(−ieψ*·(A_⊥×ψ)), keeping Re explicit.
- **Checks** (random states, P = 3, all three n̂; `log_chiral1d.txt`, `checks` in the JSON):

| Check | Result |
|---|---|
| Reality: \|Im\|/\|Re\| of the complex central-difference chiral sum | 1.8 × 10⁻¹⁶ (z), 1.1 × 10⁻¹⁴ (diag), 8 × 10⁻¹⁷ (perp). Its real part equals the code's value to 1 × 10⁻¹⁴. |
| Gauge covariance: random lattice gauge function α_s ∈ (−π, π) | chiral term rel. change ≤ 3.2 × 10⁻¹⁴; total ≤ 1.2 × 10⁻¹⁶ |
| Mirror: s → −s, A → −A maps E_γ to E_{−γ} | ≤ 1.2 × 10⁻¹⁶ |
| Gradient check: analytic vs 5-point stencil (step 10⁻³), 60 random coordinates, error \|fd − g\|/(\|fd\| + 10⁻⁸) | worst 1.4 × 10⁻⁸ (A free), 9 × 10⁻¹⁰ (A ≡ 0) |
| Vacuum | e_vac = 3(½η² − η(1+η)) = −0.315 (η = 0.1) and 0 (η = 0). It equals `gl3.GL3.vacuum_energy()` per volume exactly. The code's E/P at the vacuum agrees to 1 × 10⁻¹⁶, with gradient 7 × 10⁻¹⁸. At γ = 0 a noise start relaxes back to it (gain 3 × 10⁻¹⁵, converged). The minimum curvature over 20 random directions is +58 > 0. |

- **Solver.** L-BFGS-B, gtol 10⁻¹⁰, ftol 10⁻¹⁶, maxcor 20, maxiter 40 000. Every solve is recorded in the JSON (gain, success, message, iterations, max|∇|).
- **Seeds**, at every (γ, P):
  - R and L: vacuum + 0.05(e₁ cos qs ± e₂ sin qs), with q = 2π/P and e₁ × e₂ = n̂. This is a real (director) helix (deviation 6).
  - Noise: vacuum + N(0, 0.05) on every free variable, `default_rng(0)`.
- **Linear-stability cross-check (descriptive, added).** The vacuum Hessian of the same lattice functional, block by Fourier block q = 2πm/P over the P grid (q ≤ 4). γ_lin is the smallest γ at which a block goes negative.

## 3. γ_c table (Calculations 1 and 2a)

Each γ_c is the smallest γ found unstable (gain < −10⁻⁸ for some P and seed). The bracket is the final bisection interval.

| n̂ | η | γ_c, A free [bracket] | γ_lin, A free (q) | γ_c, A ≡ 0 [bracket] | γ_lin, A ≡ 0 (q) | ratio A free / A ≡ 0 |
|---|---|---|---|---|---|---|
| z | 0.1 | **0.37461** [0.37402, 0.37461] | 0.37421 (0.093) | **0.48008** [0.47949, 0.48008] | 0.47931 (0.079) | **0.780** |
| diag | 0.1 | **0.35352** [0.35293, 0.35352] | 0.35297 (0.157) | **0.77539** [0.77441, 0.77539] | 0.77472 (0.393) | **0.456** |
| perp | 0.1 | **0.38750** [0.38691, 0.38750] | 0.38733 (0) | **0.39629** [0.39570, 0.39629] | 0.39520 (0.079) | **0.978** |
| z | 0 | 0.00125 [0.00063, 0.00125] (→ 0) | 0.00024 (0) (→ 0) | **0.07891** [0.07813, 0.07891] | 0.07855 (0.079) | 0.016 |
| diag | 0 | 0.00125 [0.00063, 0.00125] (→ 0) | 0.00024 (0) (→ 0) | **0.07891** [0.07813, 0.07891] | 0.07855 (0.079) | 0.016 |
| perp | 0 | 0.00125 [0.00063, 0.00125] (→ 0) | 0.00024 (0) (→ 0) | **0.07891** [0.07813, 0.07891] | 0.07855 (0.079) | 0.016 |

**Reading the table.**

- **Continuous transition.** At every η = 0.1 entry γ_c − γ_lin ≤ 1.1 × 10⁻³, about one bisection step. The vacuum goes unstable by a soft mode, not by a first-order jump, at least from these seeds.
- **Hand check (mine, not in the NOTE).** Take the quadratic fluctuations about the vacuum ψ₀ = √(1+η)(1,1,1).
  - The chiral form decouples real (a) and imaginary (b) perturbations: Re δψ*·(n̂×δψ') = a·(n̂×a') + b·(n̂×b').
  - Real (director/amplitude) modes have mass² ≈ 2 + O(η). Their threshold is ≈ 2√2 = 2.83 at η = 0, which `director_lin_chiral1d.py` confirms (§4.3).
  - Relative-phase modes b ⊥ (1,1,1) have mass² 1.5η.
  - With A free, a uniform A_⊥ ∥ S lowers the energy by −γ²|S|²/(4|ψ|²). For a small phase perturbation that gain is exactly −γ²|b|², independent of e and of n̂. So a **uniform** instability appears at γ = √(1.5η) = 0.3873. This is the perp value (q = 0). Finite-q helices lower it further for z and diag.
- **η = 0, A free.** The phase sector is gapless, so the uniform state is unstable at any γ > 0. Its gain is −0.75γ² + O(γ⁴), the p + ip state with ρ relaxed.
  - The numbers agree: −7.500 × 10⁻⁵ at γ = 0.01, −1.875 × 10⁻⁵ at 0.005, −4.687 × 10⁻⁶ at 0.0025.
  - The bisection stops at 0.00125 only because at γ = 0.000625 the solver relaxed slowly toward that state: gain −3 × 10⁻¹¹, against the analytic −2.9 × 10⁻⁷. That is above the −10⁻⁸ test.
  - **γ_c(η = 0, A free) = 0.** The listed 0.00125 is a threshold-and-convergence artefact.
- **η = 0, A ≡ 0.** γ_c = 0.0789 ≈ 2π/80 in all three directions: the smallest q the P grid allows. In an unbounded medium this would also go to 0. It is a cell-size limit, not a physical threshold.
- **Mirror check (γ → −γ).** |γ_c| is the same to the bisection tolerance in 11 of 12 cases: −γ_lo is stable and −γ_hi unstable.
  - **Exception: perp, η = 0.1, A ≡ 0.** −0.395703 is already unstable (gain −5.3 × 10⁻⁷), whereas +0.395703 was not. The functional is exactly mirror-symmetric (check above), so this is a seed and solver effect. The noise seed is not mirror-symmetric, and growth is slow near threshold.
  - So that γ_c is uncertain by one step: 0.3952 (linear) ≤ γ_c ≤ 0.3963. The ratio stays 0.978–0.980.
  - At ±1.1 γ_c the optimal gains agree to ≤ 1.4 × 10⁻⁹ and the handedness is opposite in every case (§4).
- **Non-converged solves**, kept (full lists in the JSON under `gamma_c.*.history`):
  - η = 0.1: 35–148 per case ended `ABNORMAL` (line search) at max|∇| ≤ 1.0 × 10⁻⁷, the floating-point floor.
  - η = 0, A free: 46–50 per case hit the 40 000-iteration limit (max|∇| ≤ 4.3 × 10⁻⁵). This is the slow gapless relaxation already noted in `STATUS_step3.md`.
  - η = 0, A ≡ 0: 0–10, all ABNORMAL at ≤ 2 × 10⁻⁸.
  - A non-converged solve with negative gain is still a valid upper bound, so instability decisions do not depend on convergence. Stability decisions near γ_c do; see η = 0 above.

## 4. Optimal-texture diagnostics (Calculation 1, and 2a for comparison)

At γ = 1.1 γ_c of each case, the lowest state over 24 P × 3 seeds. Energies are per unit length. q* is in units of 1/ξ (q*ξ = q*/√2).

- "Hand" is the sign of the γ-free chiral density: R if ∫ψ*·(D×ψ) < 0. This follows the NOTE convention: the helix (cos qz, sin qz, 0) with q > 0 is right-handed and gives −q.
- "Turn" is the director's signed rotation about n̂ over the cell. Positive is right-handed.
- The cone angle is the angle between the director (the top eigenvector of Re ψψ†) and n̂. For comparison, the vacuum director (1,1,1) sits at 54.74° to z, 0° to diag and 90° to perp.
- "chiral A·S" is the term −eγ Re(iψ*·(A×ψ)), evaluated in the axial gauge (A_∥ constant).

| case | γ | P* | q*·ξ | seed | hand | gain | gradient | potential | Josephson | magnetic | chiral (twist / A·S) | ⟨\|S\|/\|ψ\|²⟩ | cone mean [min, max] | turn/cell | amp spread |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| z, 0.1, A free | 0.4121 | 67.30 | 0.066 | noise | R | −4.20e−3 | 4.290e−2 | 1.550e−2 | −0.29033 | 4.2e−4 | −8.77e−2 (−3.36e−2 / −5.41e−2) | 0.543 | 54.71 [53.1, 56.6] | −0.35° | 0.0020 |
| diag, 0.1, A free | 0.3889 | 40.06 | 0.111 | noise | R | −4.27e−3 | 4.152e−2 | 1.567e−2 | −0.28934 | 1.5e−3 | −8.87e−2 (−1.64e−2 / −7.23e−2) | 0.550 | 1.62 [1.5, 1.7] | −0.57° | 0.0000 |
| perp, 0.1, A free | 0.4263 | 47.62 (uniform: P-degenerate) | (0) | noise | R | −4.14e−3 | 4.361e−2 | 1.540e−2 | −0.29093 | ~0 | −8.72e−2 (0 / −8.72e−2) | 0.539 | 90.00 | 0.00° | 0.0079 |
| z, 0, A free | 0.00138 | 20.06 (uniform: P-degenerate) | (0) | noise | R | −1.38e−6 | 1.38e−6 | 4e−13 | 0 | ~0 | −2.76e−6 (0 / −2.76e−6) | 0.987 | (ill-defined, p + ip) | 0 | 0 |
| diag, 0, A free | 0.00138 | as above | (0) | noise | R | −1.38e−6 | 1.38e−6 | 3e−13 | 0 | ~0 | −2.76e−6 (0 / −2.76e−6) | 0.986 | (ill-defined) | 0 | 0 |
| perp, 0, A free | 0.00138 | as above | (0) | noise | R | −1.38e−6 | 1.38e−6 | 5e−13 | 0 | ~0 | −2.76e−6 (0 / −2.76e−6) | 0.987 | (ill-defined) | 0 | 0 |
| z, 0.1, A ≡ 0 | 0.5281 | 80 (grid edge) | 0.056 | noise | R | −2.45e−3 | 2.732e−2 | 1.535e−2 | −0.30677 | 0 | −5.33e−2 (all twist) | 0.408 | 53.99 [53.7, 54.8] | −0.01° | 0.0148 |
| diag, 0.1, A ≡ 0 | 0.8529 | 47.62 | 0.093 | noise | R | −6.93e−3 | 7.065e−2 | 1.813e−2 | −0.26413 | 0 | −1.466e−1 | 0.679 | 2.00 [1.8, 2.2] | −2.54° | 0.0000 |
| perp, 0.1, A ≡ 0 | 0.4359 | 80 (grid edge) | 0.056 | noise | R | −3.30e−3 | 3.660e−2 | 1.536e−2 | −0.30000 | 0 | −7.03e−2 | 0.445 | 90.00 | 0.00° | 0.0070 |
| z / diag / perp, 0, A ≡ 0 | 0.0868 | 80 (grid edge) | 0.056 | noise | R | −6.6e−5 / −6.4e−5 / −8.8e−5 | 1.3e−3 / 1.2e−3 / 1.7e−3 | ~1e−6 | 0 | 0 | −1.35e−3 / −1.30e−3 / −1.80e−3 | 0.40 / 0.49 / 0.36 | 54.3 / 1.4 / 90.0 | ≤ 0.44° | 0 |

Further detail is in `tables_chiral1d_output.txt`: E/P against P, A_⊥ rms, biaxiality, amplitude minima and windings.

### 4.1 What the optimal texture is

- **It is a relative-phase texture, not a director helix.**
  - The director stays on the vacuum axis. The cone angle equals the vacuum value to within 2°, and it turns by less than 3° per cell in every case.
  - S is large (0.54 of its maximum |S| = |ψ|²). The amplitudes stay near √(1+η) (spread ≤ 1.5 %). No strand phase winds.
  - The chiral gain therefore comes from the relative phases. The softest chiral channel is the phase sector (mass² 1.5η), not the director sector.
- **With A free, most of the chiral energy is the A·S term** (62 %, 82 % and 100 % for z, diag and perp at η = 0.1).
  - It is carried by a nearly uniform A_⊥ (rms 0.31–0.40) aligned with S. A_∥ averages to ≤ 10⁻⁶. The magnetic energy is small (≤ 1.5 × 10⁻³).
  - perp, η = 0.1 is exactly uniform: gain −4.14 × 10⁻³ at every P (P* is a tie).
  - For z the uniform state gives −1.72 × 10⁻³ at P ≤ 34, and a finite-q phase helix beats it: −4.20 × 10⁻³ at P = 67.3. For diag the corresponding values are −7 × 10⁻⁶ and −4.27 × 10⁻³ at P = 40.
- **η = 0, A free.** The state is uniform and p + ip-like (⟨|S|/|ψ|²⟩ = 0.99, biaxial ratio 0.72), so the director cone angle is not well defined. The tabulated P* = 20.06 is not meaningful.
  - Most P solves had not finished relaxing at 40 000 iterations, so the E/P curve is ragged (10⁻¹¹ to 10⁻⁶). The analytic uniform gain −0.75γ² = −1.43 × 10⁻⁶ is reached to 4 %.
  - **How the instability shows up.** At the smallest bracket value tested, γ = 0.01, the gain is −7.500 × 10⁻⁵, equal to −0.75γ², with a noise seed at every P. That is a uniform p + ip relative-phase state with a uniform A_⊥, and no length scale.
- **With A ≡ 0** the texture is still phase-type (⟨|S|/|ψ|²⟩ = 0.41–0.68). For z, perp and η = 0 its optimum sits at the largest cell (P = 80, the smallest allowed q), so P* is a grid-edge value.
- **Handedness.** For γ > 0 every optimum has a negative γ-free chiral density (R). At −1.1 γ_c every optimum is L with the same gain, and the director turn reverses sign where it is non-zero. The mirror check passes on handedness.

### 4.2 Physical reading of the uniform A_⊥ (flag for the author)

In the 1D cell a constant A_⊥ is a legitimate degree of freedom: it has zero field strength and a non-trivial holonomy. In 3D it is gauge-equivalent to a uniform phase gradient ψ → ψ e^{ieA_⊥·x} **perpendicular to n̂**. The A-free optimum therefore contains a supercurrent-like phase modulation along a direction other than n̂, with the Lifshitz coupling γ S·(∇θ − eA) making the net current vanish.

This is the mechanism of the helical phases in noncentrosymmetric superconductors that NOTE §4 cites [memory: Kaur, Agterberg and Sigrist 2005]. Two consequences:

- "A free" thresholds are partly a minimum over modulation directions. This is why perp's A-free and A ≡ 0 values nearly coincide: there the uniform A-free state and the A ≡ 0 phase winding along n̂ are the same physics, up to the quantized q = 2π/P.
- The NOTE's question "does A screen the chiral gain?" has the opposite answer for the optimal texture. **A enhances it.**

### 4.3 Director sector on its own (descriptive)

Restricted to real perturbations of ψ (S = 0 at first order; A does not enter at second order), the vacuum's linear threshold is the following (`director_lin_chiral1d.py`, Fourier blocks over the same P grid, q ≤ 6):

| n̂ | η = 0.1 | η = 0 |
|---|---|---|
| z | 3.035 (q = 1.49) | 2.831 (q = 1.41) |
| diag | 3.069 (q = 1.57) | 2.831 |
| perp | 3.019 (q = 1.49) | 2.831 |

At η = 0 this matches the one-constant estimate 2m with m² = 2 (the amplitude/director mass), γ = 2√2. **The locked anisotropy pins the director about 8× more strongly than the Josephson term pins the relative phases.**

## 5. Calculation 2b: A free against A ≡ 0 at 0.5 γ_c and 1.5 γ_c (A-free γ_c)

Optimal texture over the full P sweep. In the A-free case "A·S" is −eγ Re(iψ*·(A×ψ)) in the axial gauge; it equals the A_⊥·S part because A_∥ averages to ≤ 2 × 10⁻³.

| n̂, η | γ | A | gain | P* | chiral | A·S term | ⟨\|S\|⟩ | ⟨\|S\|/\|ψ\|²⟩ | magnetic |
|---|---|---|---|---|---|---|---|---|---|
| z, 0.1 | 0.187 | free / ≡ 0 | vacuum (0) / vacuum | — | 0 | 0 | 0 | 0 | 0 |
| z, 0.1 | 0.562 | free | **−8.07e−2** | 47.6 | −0.431 | −0.260 | 2.93 | 0.870 | 4.0e−3 |
| z, 0.1 | 0.562 | ≡ 0 | −5.98e−3 | 56.6 | −0.086 | 0 | 1.63 | 0.492 | 0 |
| diag, 0.1 | 0.177 | both | vacuum | — | 0 | 0 | 0 | 0 | 0 |
| diag, 0.1 | 0.530 | free | **−8.10e−2** | 33.7 | −0.430 | −0.344 | 2.97 | 0.879 | 1.0e−2 |
| diag, 0.1 | 0.530 | ≡ 0 | vacuum (γ < γ_c(A ≡ 0) = 0.775) | — | 0 | 0 | 0 | 0 | 0 |
| perp, 0.1 | 0.194 | both | vacuum | — | 0 | 0 | 0 | 0 | 0 |
| perp, 0.1 | 0.581 | free | **−8.18e−2** | uniform | −0.438 | −0.438 | 2.96 | 0.876 | ~0 |
| perp, 0.1 | 0.581 | ≡ 0 | −6.18e−2 | 80 (edge) | −0.358 | 0 | 2.59 | 0.771 | 0 |
| any, 0 | 6.3e−4 | free | −3.0e−11 (incompletely relaxed; analytic −2.9e−7) | — | −6.1e−11 | −6.1e−11 | 0.03 | 0.01 | ~0 |
| any, 0 | 6.3e−4 | ≡ 0 | vacuum | — | 0 | 0 | 0 | 0 | 0 |
| z / diag / perp, 0 | 1.9e−3 | free | −2.60e−6 / −2.64e−6 / −2.64e−6 | — | −5.2e−6 / −5.3e−6 / −5.3e−6 | 100 % of chiral | 2.98–3.00 | 0.994–1.000 | ~0 |
| any, 0 | 1.9e−3 | ≡ 0 | vacuum (γ < 0.0789) | — | 0 | 0 | 0 | 0 | 0 |

At 1.5 γ_c the A-free gain is 13× (z) and 1.3× (perp) the A ≡ 0 gain. For diag, A ≡ 0 is still stable. In every case the A·S term supplies 60–100 % of the chiral energy, while the magnetic cost stays ≤ 1 × 10⁻². Below γ_c both are the vacuum, as required.

## 6. Calculation 2c (P5): the pure relative-phase winding

n̂ = z, P = 20, γ = γ_c(A free): 0.37461 at η = 0.1 and 0.00125 at η = 0 (see deviation 9). The seed is √(1+η)(e^{2πis/P}, 1, 1).

| η, A | chiral, unrelaxed | gradient, unrelaxed | chiral, relaxed | gradient, relaxed | chiral/gradient | winding (ψ₁, ψ₂, ψ₃), relaxed | min \|ψ₁\| along the path | final state |
|---|---|---|---|---|---|---|---|---|
| 0.1, free | **0 (exactly)** | 0.1086 | −5.3e−14 | 2.8e−14 | (−1.9; round-off / round-off) | (0, 0, 0) | **0.031** (iteration 89) | vacuum (gain 6e−15) |
| 0.1, ≡ 0 | **0 (exactly)** | 0.1086 | −5.0e−17 | 7.9e−16 | (−0.063; round-off) | (0, 0, 0) | **0.041** (iteration 37) | vacuum (gain 1e−15) |
| 0, free | **0 (exactly)** | 0.0987 | −1.40e−6 | 0.0636 | **−2.2e−5** | (1, 0, 0) | 0.937 | winding kept, gain +0.065, ⟨\|S\|/\|ψ\|²⟩ 0.60 |
| 0, ≡ 0 | **0 (exactly)** | 0.0987 | −1.47e−6 | 0.0890 | **−1.7e−5** | (1, 0, 0) | 0.949 | winding kept, gain +0.094 |

- **Unrelaxed.** The lattice chiral sum is Σ f² cos(2π(s+h)/P) over a full period, which is 0.0 in floating point. This confirms the analytic statement.
- **η = 0.1.** The winding does not survive. The Josephson term turns it into a sine-Gordon-type kink, and the kink unwinds.
  - The trace (`p5_trace_chiral1d.json`) shows the winding of ψ₁ changing at a single iteration. At that iteration |ψ₁| has dropped to 0.05 (A free) or 0.08 (A ≡ 0), against the vacuum value 1.049, and the largest nearest-neighbour phase step is 0.89 or 0.51 rad.
  - So it **unwinds through an amplitude near-zero of ψ₁** (minimum 0.031 / 0.041). On the lattice the slip completes before the amplitude reaches exactly 0.
  - The relaxed state is the uniform vacuum. At γ = γ_c the vacuum is marginal, and the relaxation did not leave it.
- **η = 0.** The winding survives (no Josephson restoring force). It relaxes with small amplitude adjustments. Its chiral energy is 2 × 10⁻⁵ of its gradient energy at this very small γ.

## 7. Verdicts (applied literally)

- **P1** (η = 0.1: γ_c > 0, finite, for every n̂): **HOLDS.** 0.3746, 0.3535, 0.3875 (A free), and also with A ≡ 0.
- **P2** (η = 0: γ_c may be 0; no prior): **Found γ_c = 0 with A free** (uniform p + ip-type instability, gain −0.75γ²). The bisection value 0.00125 is an artefact. With A ≡ 0, γ_c = 0.0789 = 2π/P_max, limited by the cell size.
- **P3** (just above γ_c the optimal helix is director-type, ⟨|S|/|ψ|²⟩ < 0.05): **FAILS.** 0.543, 0.550, 0.539 (A free, η = 0.1); 0.99 (η = 0); 0.41–0.68 (A ≡ 0).
- **P4** (ratio within 1 ± 0.05 at every (n̂, η)): **FAILS.** 0.780 (z), 0.456 (diag), 0.978 (perp) at η = 0.1; 0.016 (all n̂) at η = 0. Only perp, η = 0.1 is inside the band. The deviation runs the other way from screening: the free gauge field lowers γ_c.
- **P5** (no first-order gain; unrelaxed chiral zero; relaxed chiral < 1 % of gradient): **NOT MET as written.**
  - The unrelaxed chiral energy is exactly zero. This part holds.
  - At η = 0 the relaxed ratio is 2 × 10⁻⁵, which holds.
  - At η = 0.1 the winding unwinds through an amplitude near-zero to the vacuum. There both energies are round-off (10⁻¹⁴ to 10⁻¹⁶), and |chiral|/gradient = 1.9 (A free) and 0.063 (A ≡ 0), which is > 1 % literally. Substantively the test is undefined there, because no winding remains.

## 8. Deviations, collected

1. **SciPy installed with pip.**
2. **Branch.** This session's designated push branch is `claude/awesome-noether-8f5elm`. I created it from `origin/claude/seed-step3-first-closure` at 5d8de7c and pushed all commits there, not to `claude/seed-step3-first-closure`. A merge or fast-forward is needed to bring the commits onto the step-3 branch.
3. **h slightly above 0.05.** M = round(P/0.05) was used as written, which gives h = P/M ∈ [0.0495, 0.0505]. In 11 of the 24 cells h exceeds 0.05 by at most 0.94 %. The two requirements ("h ≤ 0.05" and "M = round(P/h)") conflict. I took the second literally.
4. **Handedness label in `chiral1d.py` is wrong. It is not used.** The script labels by the sign of the γ-weighted chiral energy, which is negative at any favourable state for either sign of γ, so the JSON field `handedness` reads "R" everywhere. `tables_chiral1d.py` recomputes handedness from the γ-free density. The values in this report are the recomputed ones. No energy or decision depends on the label.
5. **Extra files and analyses, all descriptive:**
   - the linear-stability cross-check (in `chiral1d.py`, `linear` in the JSON);
   - `director_lin_chiral1d.py` with its JSON and log;
   - `p5_trace_chiral1d.py` with its JSON and log. It re-runs the 2c relaxations deterministically (the same iteration counts, 2338 and 1276, as the main run) to see whether an amplitude zero occurred, which the main run did not record;
   - `tables_chiral1d.py` and its output.
6. **Seed forms (literal readings).** The R and L "helical perturbations" are real director helices of amplitude 0.05. The real subspace is exactly invariant under the A ≡ 0 or A = 0 dynamics, so the phase-sector instability was always found from the noise seed (every optimum's seed is "noise"). The noise is Gaussian with standard deviation 0.05 on every free variable (ψ and, when free, A), using rng seed 0 for every solve.
7. **The η = 0 "optimum at γ = 0.01" was not run as a separate sweep.** The script's guard required a bisection lower end of exactly 0, which was not the final bracket. The γ = 0.01 sweep from the bracketing stage (72 solves, in the JSON) is used instead (§4.1).
8. **Non-converged solves** are kept and counted (§3). In the optimum sweeps there are 0–14 of 72 per case. All are ABNORMAL at the round-off floor, except at η = 0 with A free, where they hit the iteration limit.
9. **2c at η = 0** uses γ = 0.00125, the bisection value, as instructed ("γ = γ_c(A free)"), although the true γ_c there is 0.
10. **Mirror exception** (perp, η = 0.1, A ≡ 0): recorded in §3, not re-run.
11. `run_stdout.txt` (console copy of the log) was committed during the run and is removed at the end. `log_chiral1d.txt` is the record.

**Ambiguities flagged for the author.** Each was resolved by the most literal reading.

- **(a)** The uniform A_⊥ mode (§4.2) is allowed by the 1D functional and dominates the A-free gain. Whether a "1D calculation along n̂" should admit it is a modelling choice. It makes the A-free γ_c partly direction-independent.
- **(b)** "Director-type" (P3) and the cone angle presuppose a director. For p + ip-like states (η = 0) it is ill-defined.
- **(c)** The γ_c rule's −10⁻⁸ test plus finite relaxation gives a non-zero value at η = 0. The cell-size cap P ≤ 80 sets the A ≡ 0 value at η = 0, and puts several A ≡ 0 optima at the P = 80 edge.
- **(d)** P5's "< 1 %" test is undefined when the winding does not survive (η = 0.1).
- **(e)** The "A·S energy term" is gauge-dependent through A_∥. It is reported in the axial gauge, where A_∥ is constant and averages to about 0. There the term equals the gauge-invariant A_⊥·S part.

`gl3.py`, `NOTE_chiral_term.md`, `STATUS_step3.md` and all pre-existing scripts are unmodified.

## 9. What is and is not established

**Established, in 1D, for the vacuum and simple periodic textures, at κ = 2:**

- The uniform locked vacuum is stable for |γ| < γ_c, with γ_c = 0.3535 (diag), 0.3746 (z), 0.3875 (perp) at η = 0.1 and A free. The transition is continuous, the γ_c equal the linear thresholds, and they are mirror-symmetric.
- At η = 0 there is no stable window with A free.
- The first instability is in the **relative-phase (S ≠ 0) sector**, not the director sector. The director sector alone is stable up to γ ≈ 3.0 (η = 0.1).
- The gauge field **does not screen** the chiral gain of the optimal texture. Through the A·S coupling, carried by a uniform A_⊥, it **enhances** the gain and lowers γ_c (ratios 0.46–0.98 at η = 0.1).
- A pure relative-phase winding has exactly zero chiral energy at fixed amplitudes. At η = 0.1 it is not metastable at P = 20: it unwinds through an amplitude near-zero.

**Not established:**

- **Anything about a twisted loop**: its stability, size, or the Derrick balance of NOTE §3.3. These results say nothing yet about whether a twisted loop is stable.
- 3D textures, other κ, other directions than the three tested, or cells longer than P = 80.
- Whether the uniform-A_⊥ state survives in a finite 3D geometry with boundaries (§4.2).
- Global optimality: only three seeds per (γ, P) were tried.

## 10. Recommendation for a loop pre-registration (a recommendation, not a decision)

- **η = 0.1, not η = 0.** At η = 0 there is no stable vacuum window with A free.
- **γ well inside the stable window**, below the smallest A-free γ_c over the tested directions: **γ ∈ (0, 0.35)**, set by n̂ = (1,1,1)/√3, γ_c = 0.3535. A margin such as γ ≤ 0.3 keeps the vacuum, and the loop's far field, away from the soft relative-phase mode. Use A free, since A ≡ 0 overstates the window (up to 0.775 on the diagonal).
- **Sector: be explicit that it is not "director, unscreened".**
  - In this window the chiral term acts most strongly on S ≠ 0 relative-phase textures, and there the gauge field enhances rather than screens.
  - A director-sector (S = 0) loop meets director stiffness about 8× larger (γ_lin ≈ 3), so at γ < 0.35 its chiral gain is weak.
  - So I recommend that the pre-registration choose between:
    - **(i) the relative-phase (S ≠ 0) sector**, where E9's twist N lives, at η = 0.1, γ ∈ (0, 0.35). It should include the ±N parity control and a check that the far field stays in the uniform vacuum.
    - **(ii) the director sector**, with the explicit expectation that NOTE §3.3's b² > 3ac condition may fail at γ < 0.35. If so, it is a test that could be negative by design.
  - Option (i) is the closer match to these results. NOTE §4's preference for the director sector, which was motivated by avoiding screening, is not supported: no screening was found to avoid.

## 11. Files committed

- `PREREG_chiral1d.md`: predictions, committed first (dbaa172).
- `chiral1d.py`: the model, the checks, the γ_c searches, Calculations 1, 2a, 2b and 2c, and the linear cross-check.
- `chiral1d_results.json`: every solve without fields, the checks, the γ_c histories, optima, mirror, 2b, 2c and linear thresholds.
- `log_chiral1d.txt`: console log of the run.
- `tables_chiral1d.py`, `tables_chiral1d_output.txt`: read-only tables.
- `p5_trace_chiral1d.py`, `p5_trace_chiral1d.json`, `log_p5_trace.txt`: the P5 relaxation trace.
- `director_lin_chiral1d.py`, `director_lin_chiral1d.json`, `log_director_lin.txt`: the director-sector threshold.
- `REPORT_chiral1d.md`: this file.

Everything is deterministic and reproducible by re-running the scripts. No particle identification is made or implied.
