# Steps 1–2: fractional flux and confinement in a three-component condensate
Pre-registration (exploration), October 30, 2026. Written before any run.

## Model (static energy; the same for the relativistic and non-relativistic versions)
Three complex fields ψ_k = √ρ_k e^{iθ_k} with equal charge e, one U(1) gauge field A, in 2D, London limit (fixed amplitudes):
E = Σ_k (ρ_k/2)(∇θ_k − eA)² + (1/2)B² − η Σ_{i<j} cos(θ_i − θ_j)
Lattice units (h = 1). ρ_k = 1. e = 1/(4√3), so the penetration depth is λ = 1/(e√Σρ) = 4. η = 0 or 0.02.
Vortices are fixed singular windings (θ_k = θ_k^sing + φ_k, with φ_k single-valued). The solver minimizes over φ_k and A.

## Configuration
A full composite (windings 1,1,1) at the origin. Component 1's vortex is pulled out to distance d; components 2 and 3 stay at the origin.

## Predictions (written now)
P1. Flux: the isolated component-1 vortex carries 1/3 of the flux quantum 2π/e, and the remaining pair carries 2/3.
P2. η = 0: E(d) − E(0) grows logarithmically. Neutral-mode coefficient 2π·|n_⊥|² with n_⊥ = (2/3, −1/3, −1/3), so the coefficient is 4π/3 ≈ 4.19 per unit ln d, at d ≫ λ.
P3. η = 0.02: E(d) grows linearly at large d. Slope ≈ sine-Gordon wall tension 8√(K V₀), with K = 2/3 and V₀ = 2η, giving ≈ 1.31 (approximate: it neglects coupling to the charged mode).
Fail conditions: no 1/3 flux; or no confinement growth; or slopes off by more than a factor of 2 from P2 and P3.
