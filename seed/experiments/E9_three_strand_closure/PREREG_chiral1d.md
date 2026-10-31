# Pre-registration: 1D chiral-term calculations (γ_c and screening), E9

*October 31, 2026. Label: Exploration. Committed before any calculation code was written. Scope: `NOTE_chiral_term.md` §8 items 1 and 2 only. No loop, no 3D, no loop pre-registration. Model units only (`gl3.py` coordinates, ξ = 1/√2). No particle identification is made or implied.*

## Predictions (verbatim from the task)

- P1: at η = 0.1, γ_c > 0 (finite) for every direction n̂ tested.
- P2: at η = 0 the relative phases are gapless, so γ_c may be 0. No prior; report what is found.
- P3: just above γ_c, the optimal helix is director-type: |S|/|ψ|² < 0.05 averaged over the cell, where S = iψ×ψ*. Prior about 60 %.
- P4 (screening): γ_c with A free, divided by γ_c with A ≡ 0, lies within 1 ± 0.05 at every (n̂, η). That would mean the gauge field does not screen the chiral gain for the optimal texture. Prior about 65 %.
- P5: a pure relative-phase winding, seeded as ψ = √(1+η)·(e^{2πi s/P}, 1, 1), gets no first-order chiral gain. At fixed equal amplitudes the chiral density averages to zero over the cell (analytic). After relaxation, the chiral energy per length is < 1 % of the gradient energy per length. Prior about 70 %.

## Model (NOTE §1–§2, strands locked to space, assumptions A5 and A6)

- ψ = (ψ₁, ψ₂, ψ₃) is a complex 3-vector. Everything depends on s = n̂·x only.
- Derivatives: ∂_j → n_j d/ds. Covariant derivative D_jψ_k = n_j ψ_k' − ieA_jψ_k, with A(s) a full 3-vector.
- Energy per unit area, over one periodic cell s ∈ [0, P):
  ∫ ds [ Σ_jk |D_jψ_k|² + ½ Σ_k (|ψ_k|² − 1)² − η Σ_{i<j} Re(ψ_iψ_j*) + ½ |n̂ × A'|² + γ Re( ψ*·(n̂ × ψ') − ie ψ*·(A × ψ) ) ]
  - The chiral term is the 1D reduction of γ ψ*·(D×ψ).
  - Keep "Re" explicit even though the integral is real.
- Parameters: κ = 2 (e = 1/√12, as in E9); η ∈ {0.1, 0}.
- Directions: n̂ ∈ { (0,0,1) (a locked cube axis), (1,1,1)/√3 (the body diagonal), (1,−1,0)/√2 (perpendicular to the diagonal) }.

## Method

- Discretize. Lattice spacing h ≤ 0.05; take M = round(P/h) points, periodic. Choose central or spectral differences. The chiral term's discretization must stay real and gauge-covariant: verify both numerically on random states (imaginary part / real part < 1e-12; gauge-transformation invariance to round-off).
- Gradient check the full functional (analytic gradient against a 5-point finite-difference stencil). Expect ≲ 1e-6.
- Vacuum reference e_vac: the uniform E9 vacuum, |ψ_k|² = 1 + η with equal phases, A = 0. Check that the code returns it as a minimum at γ = 0, and that its energy per length matches gl3.py's vacuum density.
- Cell periods: P on a fixed geometric grid of 24 values from 1.5 to 80. Each cell holds one free relaxation; multiple turns per cell are allowed.
- Seeds at each (γ, P): (i) vacuum plus a small right-handed helical perturbation of wavenumber 2π/P about n̂; (ii) the left-handed version; (iii) vacuum plus random noise of amplitude 0.05 (fixed seed). Keep the lowest-energy result.
- Minimizer: L-BFGS-B. Record convergence for every solve; keep non-converged solves listed, don't silently drop them.
- γ_c(n̂, η): the smallest γ > 0 for which min over P of (E/P − e_vac) < −1e-8. Find it by bisection to an absolute tolerance of 1e-3, after bracketing on γ ∈ {0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5}. If no bracket is found by γ = 5, report "γ_c > 5". Check the mirror symmetry: γ → −γ must give the same |γ_c| with opposite helix handedness.

## Calculations

1. (NOTE §8.1) γ_c with A free, for every (n̂, η): 6 cases. At γ = 1.1 γ_c: optimal P (q* = 2π/P*), handedness, energy split (gradient / potential / Josephson / magnetic / chiral), cell average of |S|/|ψ|², director cone angle to n̂, amplitude spread across strands. If γ_c = 0 at η = 0, how the instability shows up.
2. (NOTE §8.2, screening)
   (a) Calculation 1 with A ≡ 0 (frozen). Ratio γ_c(A free)/γ_c(A ≡ 0) per case (P4).
   (b) At γ = 0.5 γ_c and 1.5 γ_c (A-free values): A free vs A ≡ 0 for the optimal texture: energy gain, chiral energy, |S|, the A·S energy term (−eγ Re(i ψ*·(A×ψ))), magnetic energy.
   (c) P5: η = 0.1 and 0, n̂ = (0,0,1), P = 20, γ = γ_c(A free); seed √(1+η)·(e^{2πi s/P}, 1, 1). Chiral energy unrelaxed; then relax with A free and A ≡ 0; chiral and gradient energy per length; whether the winding survives and whether an amplitude zero occurred.

## Discipline

No parameters other than these; κ unchanged. Ambiguities resolved by the most literal reading, recorded and flagged. Deviations recorded. `gl3.py`, `NOTE_chiral_term.md`, `STATUS_step3.md` and existing scripts are not edited.
