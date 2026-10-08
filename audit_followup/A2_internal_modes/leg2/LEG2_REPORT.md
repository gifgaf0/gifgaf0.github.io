# A2: blind second-leg report

**Summary.** I counted the allowed potential terms exactly by three independent methods, and all three agree on every number. The action's own symmetry group (c) allows one new sixth-order term, Re(S³) = Re((ψ·ψ)³), that the global-phase group (a) does not allow. Group (c) also forbids the fourth-order term Re(ψ₀²S̄) that (a) allows.

Once Re(S³) is switched on, the polar vacuum's phase circle shrinks to six points, so the vacuum splits into three separate 6-spheres. As a result π₁ = 0, and the half-quantum vortex loses its topological protection: it now terminates three domain walls. Windings of ψ₀ stay protected because U(1)_ψ₀ is an exact symmetry.

The internal (⊥) fluctuations carry no density or current at linear order, and they have no pairing term. Objects that couple only through density or lattice velocity therefore cannot create internal quanta at any order. An object that sources the gapless internal field linearly radiates at every speed, with drag ∝ v in 2D and ∝ v² in 3D. An internal bound state, by contrast, moves with its object without loss in a uniform medium; in a crystal it can emit only when ħG·v ≥ E_b.

**Blindness and inputs.** I verified `A2_PREREG.md` and its md5 is `fd2e95973de02d9a0e6d719cb579ccc0`, which matches. The only other file I read was `g_vs1_gate/staging_memo_G_VS1_v2.md`, and only for definitions: the Fano convention {i, i+1, i+3} mod 7 and the strata. No first-leg material was read, and nothing was committed. Everything is under `/home/claude/a2_leg2/`, and `./run_all.sh` reproduces all outputs in about 5 minutes. It needs sympy, numpy, scipy and python-flint.

---

## Setup: g₂ derived from the multiplication table (`octonion_g2.py`)

**Algebra checks.** I built the multiplication table from the lines {1,2,4},{2,3,5},{3,4,6},{4,5,7},{5,6,1},{6,7,2},{7,1,3}, with e_i e_{i+1} = e_{i+3}. The checks run exactly over the integers, on 200 random elements each:
- the algebra is alternative;
- the norm is multiplicative;
- the Moufang identity holds;
- φ is totally antisymmetric;
- it is non-associative.

**Der(𝕆).** I imposed D(e_i e_j) = D(e_i)e_j + e_i D(e_j) for all i, j: 512 equations in 64 unknowns, with an exact nullspace. The results:
- The solution space has **dimension 14**.
- Each derivation kills e₀, is antisymmetric, and the set is Lie-closed.
- The commutant is 1-dimensional on the 7 and 2-dimensional on 1⊕7.
- Every derivation preserves φ, and the φ-stabiliser inside so(7), computed independently, also has dimension 14.
- The orbit-map rank is 6 at one generic vector, 11 at a pair and 14 at a triple.

**Cartan subalgebra and roots.** The Cartan subalgebra is the 2-dimensional intersection of g₂ with the rotations of the planes that L_{e7} pairs: (1,3), (2,6), (4,5). Its centraliser is 2-dimensional. Over ℚ(i), the weight vectors are e_j ∓ i e_k and e₇:
- The weights of the 7 are 0 and the six short roots.
- There are 12 roots and |W| = 12; the Weyl group was generated from the reflections.
- The simple roots are (0,1) (short) and (1,−1) (long).
- After a diagonal rescaling, the simple-root vectors become 0/1 matrices, so all later linear algebra is over ℤ.

## Task 1: invariant counts (`task1_invariants.py`, `task1_output.txt`)

### Methods

**Method A (primary, exact).** This method does not reduce to known invariant generators.
- It uses complex coordinates z = ψ and w = ψ̄, with z and w independent and written in the rational weight basis.
- A polynomial is g₂-invariant exactly when it has weight 0 and is killed by the raising operators E_{α₁} and E_{α₂}. A weight-0 highest-weight vector generates the trivial module.
- U(1)_global and U(1)_ψ₀ are gradings on monomials, Z₃ is a congruence on the u(1)₇ charge, and T is the swap z ↔ w (orbit sums).
- Ranks are exact integer ranks computed with FLINT `fmpz_mat`.
- Cross-check: replacing the two simple-root operators by all 6 positive or all 12 root operators gives identical counts.

**Method B (Molien–Weyl, exact).** The dimension of the invariants in Sym^p 7 ⊗ Sym^q 7 is (1/|W|)·CT[h_p·h_q·∏_α(1 − t^α)], using the derived weights and roots. T-even counts come from the identity tr((g⊗g)∘swap) = tr(g²).
- Controls: trivial rep 1, Λ²7 → 0, Λ³7 → 1 (the 3-form φ), Sym²7 → 1, Sym³7 → 0.

**Method C (floating point, degrees 2 and 4).** This works in real coordinates (u, v), using the 14 derived real derivations plus the u(1) derivations. The invariants are the kernel of Σ DᵀD. Z₃ comes from the u(1)₇ spectrum on that kernel, and the T-even part from the trace of (−1)^{deg v}. The spectral gap is at least 1.

**Agreement.** A = B at every entry, both for the bigraded I(p,q) and for every group count. A = C at degrees 2 and 4.

### Result (all / T-even)

| space | group | d = 2 | d = 4 | d = 6 |
|---|---|---|---|---|
| ℝ¹⁴ | (a) G₂×U(1)_global | 1/1 | 2/2 | 2/2 |
| ℝ¹⁴ | (b) G₂×U(1)_ψ₀ (= G₂ on ℝ¹⁴) | 3/2 | 6/4 | 10/6 |
| ℝ¹⁴ | (c) G₂×U(1)_ψ₀×ℤ₃ | 1/1 | 2/2 | **4/3** |
| ℝ¹⁶ | (a) | 2/2 | 6/5 | 10/8 |
| ℝ¹⁶ | (b) | 4/3 | 10/7 | 20/13 |
| ℝ¹⁶ | (c) | 2/2 | **4/4** | **8/7** |

**Bigraded G₂ invariants.** I(p,q) = dim (Sym^p 7 ⊗ Sym^q 7)^{G₂}:
- I(p,q) = 1 at (0,0), (2,0), (1,1), (4,0), (3,1), (6,0), (5,1).
- I(p,q) = 2 at (2,2), (4,2), (3,3).
- I(p,q) = 0 whenever p + q is odd.
- I is symmetric in p and q.

The trace of T on I(p,p) is 1, 1, 2, 2 for p = 0, 1, 2, 3. This equals the generating function of the free algebra ℂ[S, N, S̄]. That is an outcome of the count, not an input.

**Where (c) differs from (a).**
- On ℝ¹⁴ they differ at degree 6, where (c) adds Re S³ (T-even) and Im S³ (T-odd).
- On ℝ¹⁶ they differ at degree 4. Group (a) contains Re(ψ₀²S̄) (T-even) and Im(ψ₀²S̄) (T-odd), and U(1)_ψ₀ forbids both.
- On ℝ¹⁶ they also differ at degree 6.

**Group (c) T-even inventory on ℝ¹⁶ (consistent with the counts):**
- d2: |ψ₀|², N
- d4: |ψ₀|⁴, |ψ₀|²N, N², |S|²
- d6: |ψ₀|⁶, |ψ₀|⁴N, |ψ₀|²N², |ψ₀|²|S|², N³, N|S|², Re S³

**Failed checks:** none.

**Assumptions:**
- Real invariants are counted through the complexification, which is standard for a compact group.
- T is componentwise conjugation and commutes with G₂, since the g₂ matrices are real.
- On ℝ¹⁴, group (b) is G₂ alone, because U(1)_ψ₀ acts trivially there.

**Side observation.** G-VS1 §2.2 states dim Sym⁶(ℝ¹⁴) = 11,628. The correct value is C(19,6) = 27,132; 11,628 is C(19,5). No count depends on this.

## Task 2: explicit T-even basis for group (c) on ℝ¹⁴

Write A = |u|² − |v|² and B = 2u·v, so that S = ψ·ψ = A + iB and N = |u|² + |v|².

| degree | basis | value on ψ₇ = e^{iθ}n |
|---|---|---|
| 2 | N | 1 |
| 4 | N², \|S\|² = A² + B² | 1, 1 |
| 6 | N³, N\|S\|², **Re S³ = A³ − 3AB²** | 1, 1, **cos 6θ** |

How the basis is checked:
- Each element is annihilated exactly by all 14 derived derivations, and each is Z₃-invariant and T-even.
- At each degree the elements are linearly independent (exact rank 1, 2, 3), and their number equals the machine dimension.
- Independently, I took the exact FLINT kernel for (c), T-even, degree 6, mapped it back to original coordinates and evaluated it on the polar orbit. The 3-dimensional kernel contains exactly **one θ-dependent direction, ∝ cos 6θ**, with residual below 10⁻¹⁸.

**So Re(S³) depends on the 7-sector phase on P7.** Its T-odd partner Im(S³) = sin 6θ is excluded by T.

## Task 3: π₀ and π₁ (`task3_topology.py`, `task3_output.txt`)

### Polar stratum P7

**Case (i): degree ≤ 4 only.** The vacuum manifold is V = (S¹_θ × S⁶)/ℤ₂, where the ℤ₂ acts freely by (θ, n) ↦ (θ + π, −n).
- **π₀ = 0** and **π₁ = ℤ**. This follows from the fibration S⁶ → V → S¹/ℤ₂ together with π₁(S⁶) = 0.
- The generator is the half-quantum loop (θ: 0 → π, n → −n). The ordinary 2π vortex is twice the generator.

**Case (ii): adding λ₆ Re S³ with λ₆ ≠ 0.** On P7 this term equals λ₆N³cos 6θ, so θ is pinned to six values θ* + kπ/3. Because e^{i(θ+π)}n = e^{iθ}(−n), these give V = three disjoint copies of S⁶.
- **π₀ = ℤ₃** (three components, cyclically permuted by ω), and **π₁ = 0**.
- **The half-quantum vortex is not topologically protected.** Its loop must cross three phase walls (Δθ = π/3 each), so it is the end-line of three domain walls; a 2π vortex ends six. Its protection survives only at degree ≤ 4, or if the coefficient is tuned to zero.

### Mixed stratum (ψ₀ ≠ 0, 7-sector polar), under group (c)

Group (c) has no ψ₀–ψ₇ phase-locking term at any degree ≤ 6: Re(ψ₀²S̄) is forbidden by U(1)_ψ₀.
- **Case (i):** V = S¹_{θ₀} × (S¹ × S⁶)/ℤ₂, so **π₁ = ℤ ⊕ ℤ**. The generators are the 2π winding of ψ₀ and the 7-sector half-quantum.
- **Case (ii):** V = S¹_{θ₀} × (3 copies of S⁶), so **π₀ = ℤ₃ and π₁ = ℤ**. Only the ψ₀ winding is protected.
- **Alternative reading, for comparison only.** If the (a)-allowed locking term Re(ψ₀²S̄) were present (it is forbidden under (c)), case (i) would give V ≅ S¹ × S⁶ with π₁ = ℤ: one common 2π winding, the MP of G-VS1.

### Numerical evidence

I minimised explicit potentials from 300 random starts each:
- **Case (i):** every minimum is polar, with |S|/N − 1 below 2·10⁻¹⁵, and θ fills [0, π).
- **Case (ii):** θ mod π falls into exactly 3 clusters spaced π/3 apart, for both signs of λ₆.
- **Barrier along the half-quantum loop:** about 3·10⁻¹⁶ in case (i), and 0.11417 = 2λ₆N*³ in case (ii).
- **Mixed (i):** θ₀ and θ₇ are both free.
- **Mixed (ii):** θ₇ falls into 3 clusters, while θ₀ and the relative phase stay free.
- **With the (a) locking term:** the relative phase is locked.

**Failed check:** in the first attempt, V with λ₆Re S³ was unbounded below and the minimiser diverged. I fixed this by adding g₆N³ with g₆ > |λ₆|. That term is θ-independent and leaves the topology unchanged.

**Assumption:** the potential favours the polar orbit (negative |S|² coefficient), and λ₆ is small enough that the minimum stays polar.

## Task 4: Watanabe–Murayama counting (`task4_wm.py`, `task4_output.txt`)

I used explicit anti-Hermitian 8×8 generators and random representatives of each vacuum. n_BG is the rank of the map T ↦ Tψ, and ρ_ab = Im ψ†[T_a,T_b]ψ; the real part is exactly zero.

| vacuum | symmetry | dim G | n_BG | rank ρ | n_B (quadratic) | n_A (linear) |
|---|---|---|---|---|---|---|
| P0 | U(8) | 64 | **15** | **14** | **7** | **1** |
| R | SO(7)×U(1)_ψ₀×U(1)₇ | 23 | **1** | **0** | **0** | **1** |
| P7 | same | 23 | **7** | **0** | **0** | **7** |
| F7 | same | 23 | **11** | **10** | **5** | **1** |

**Bogoliubov check.** I linearised GP for an explicit potential with exactly the stated symmetry and fitted the small-k exponent of each branch:
- **P0:** 1 linear (c = 1) and 7 quadratic (ω = k²/2).
- **R:** 1 linear and 7 gapped (gap Δ).
- **P7:** 7 linear (the phonon and 6 director modes) and 1 gapped (ψ₀).
- **F7:** 1 linear, 5 quadratic and 2 gapped (ψ₀, and the 7-sector conjugate direction).

All of these match the table.

**Supplementary, under the action's continuous group G₂×U(1)_ψ₀ (n_BG / rank / n_B / n_A):**
- R: 1/0/0/1
- P7: 6/0/0/6
- F7: 11/10/5/1

Under G₂×U(1)_ψ₀ the 7-sector phase is not a symmetry at P7.

**Failed check:** my first branch classifier used an absolute gap threshold and labelled the k = 10⁻³ phonon as gapped. I replaced it with an exponent-based classifier.

## Task 5: linear coupling (`task5_coupling.py`, `task5_output.txt`)

Write ψ = (φ₀ + δ)n̂ + χ with n̂†χ = 0. Then ρ = φ₀² + 2φ₀ Re δ + |δ|² + |χ|², and the current is j = j[φ₀, δ] + O(χ²); there is no term linear in χ (checked symbolically). Consequences:

- **Internal fluctuations carry no density and no current at linear order.** A defect that couples to the medium only through the total density (Branch C) or through the lattice velocity (−ρ_n u̇·v_s) therefore does **not** couple linearly to the internal branches.
- **There is no anomalous term in the internal sector.** The ⊥ block of the quadratic Hamiltonian is χ†L_⊥χ with L_⊥ = −½∇² + U∗ρ₀ − μ, and contains no χχ or χ̄χ̄ terms. The internal Bogoliubov coefficients are therefore v_k = 0, the condensate is the internal-quasiparticle vacuum, and V(x − vt)|ψ|² ⊃ Vχ†χ annihilates it. The density vertex creates **no internal quanta at second order**. In fact it creates none at any order, because N_⊥ = ∫ψ†P_⊥ψ is a U(8) charge and both the two-body dynamics and the vertex are U(8)-invariant. Only the in-line (n̂) block has Bogoliubov pairing, which gives the phonon with Landau speed c_s.

**Checks:**
- I built the Hessian of the GP energy on a periodic, non-uniform soft-core background (24-point ring).
  - The ⊥–∥ cross block is 3·10⁻¹¹.
  - The commutator of the ⊥ block with i is 2·10⁻¹¹, meaning no pairing.
  - The ⊥ block equals 2dx·L_⊥ to within 3·10⁻¹¹.
  - The ∥ block's commutator with i is 1.51, meaning pairing is present there.
- In an 8-component GP run with a density vertex moving at 0.3c_s, N_⊥ is conserved to a relative 8·10⁻¹³.
- Contrast: a vertex that mixes n̂ linearly into a ⊥ direction moves momentum into the ⊥ sector at **0.97×** the golden rule at the same subsonic speed.

**Failed check, resolved:** a first contrast run used a Gaussian vertex with s(0) ≠ 0 and V₀ = 0.1 in 1D, and gave only 0.06× the golden rule. Two causes:
- the 1D infrared zero mode, a growing global rotation of n̂;
- nonlinear sharing of momentum with the ∥ sector.

With an odd vertex (s(0) = 0) and V₀ = 0.02 the ratio is 0.97.

**Assumption:** the oriented term O is a total derivative for smooth fields, so it does not enter the bulk linearised dynamics. It acts only at cores, which is Task 6's "source".

## Task 6: moving objects (`task6_moving.py`, `task6_output.txt`; m = ħ = 1 in the numerics)

**(a) Zero-energy Goldstone texture: it must radiate.** A texture of the internal Goldstone field is phase-locked to the condensate, so it has zero frequency in the condensate frame.
- The co-moving ansatz χ = f(x − vt) gives f_k = s_k / (k²/2m − k·v − i0).
- The denominator vanishes on the sphere |k − mv| = m|v|, which passes through k = 0. That sphere is non-empty for every v > 0 and meets the source support when s(0) ≠ 0.
- So no localised co-moving stationary solution exists. The far field contains an outgoing wake decaying as r^{−(d−1)/2}.
- Equivalently: in the object frame the locked field sits mv²/2 above the internal continuum edge, so it is embedded in the continuum.
- There is no threshold, because the Landau velocity of ω = k²/2m is 0.

**(b) Exponentially bound state (E_b > 0) in a uniform background: no radiation at any v.** The χ equation sees only ρ₀, not the condensate phase, so it is Galilean covariant.
- If g(ξ)e^{iE_b t} is the bound state in the object frame, then χ = e^{i(mv·x − mv²t/2)} g(x − vt) e^{iE_b t} is an exact lab-frame solution.
- Its object-frame energy, −E_b, stays below the continuum edge at every v.
- The naive unboosted ansatz would suggest a false threshold at v = √(2E_b/m).
- Simulation with a Pöschl–Teller well (E_b = ½): the overlap with the boosted bound state stays above 1 − 3·10⁻¹⁰ at v = 0.4, 1 and 2. The value v = 2 is above that false threshold.

**(c) Drag force for a source with s(0) finite.** With F = ∫d^dk/(2π)^d · 2π|s_k|² δ(k²/2m − k·v) k_∥, the resonance sits at k* = 2mv cos θ, giving:
- **2D: F = m²|s(0)|² v, so F ∝ v.**
- **3D: F = m³|s(0)|² v²/π, so F ∝ v².**
- In general F ∝ v^{d−1}.

Checks:
- Brute-force quadrature with a smeared delta reproduces the delta-resolved values (Gaussian source), and both approach the closed forms as v → 0.
- The fitted small-v exponents are 0.987 in 2D and 1.988 in 3D.
- In a 1D time-dependent simulation with a dipole source, dP/dt matches the golden rule (ratios 0.90, 1.06, 0.96 and 1.00 at v = 0.1, 0.2, 0.3 and 0.5). Emission occurs at every speed tested.

**(d) Bound state in a crystal: emission needs ħG·v ≥ E_b.** The moving lattice drives the bound state at frequencies G·v. Emission requires **ħG·v ≥ E_b** for some reciprocal vector G whose Fourier component (U∗ρ₀)_G is nonzero. This is first order, with rate ∝ |V_G|².
- The leading threshold is **v_c = E_b/(ħ|G_min|)**, for v ∥ G_min.
- Below it, only higher harmonics nG·v ≥ E_b contribute, suppressed as |V_G|^{2n}.

Simulation with G = 2, E_b = ½ (so v_c = 0.25):
- At v = 0.4, 0.7 and 1.0 the decay rate matches Fermi's golden rule (exact reflectionless continuum) within 0.5%, and it scales as A².
- At v = 0.1 the rate is 1·10⁻⁶, effectively nil.
- At v = 0.2 the rate is 2·10⁻⁵, consistent with the second-order 2G channel, which is open because 2G·v = 0.8 > E_b.

**Assumptions:**
- The ⊥ continuum edge is the bottom of L_⊥ (in a crystal, the lowest Bloch band, with m → m* at small k).
- The 1D simulations use dipole sources because they are infrared-regular. The claims with s(0) ≠ 0 are tested in 2D and 3D by quadrature.

## Files

The md5 of every file except this report is in `MANIFEST.md5`. The final message gives this report's md5.
