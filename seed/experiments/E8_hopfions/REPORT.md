# E8: Knots. Faddeev–Skyrme Hopf solitons (Model C)

## Question

Can our own code reproduce the Faddeev–Skyrme Hopf-soliton energies and configuration types in Sutcliffe 2007, Table 2 (PLAN.md §4, E8)? Charges Q = 1–4 are required; Q = 5–7 were attempted within the budget. And do the seed's statements in SEED.md §4 and §6C hold?
- E/Q^{3/4} stays near 1.2, so the energy per unit charge falls and bigger folds store charge more cheaply.
- E₂ < 2E₁.
- Q = 7 is a trefoil.

*This report was corrected after the independent cross-check (crosscheck/CROSSCHECK.md). Corrected passages are marked; the changes are listed in the Reconciliation section at the end.*

## Method

**Model and conventions.** The energy is

E = C₀ ∫ [∂ᵢφ·∂ᵢφ + ½(∂ᵢφ×∂ⱼφ)·(∂ᵢφ×∂ⱼφ)] d³x,  C₀ = 1/(32√2 π²),

for a unit vector φ: ℝ³ → S² with φ → e₃ at infinity. This is Sutcliffe's normalisation: Ward's conjectured bound reads E ≥ Q^{3/4}, and the proven bound is E ≥ (3/16)^{3/8} Q^{3/4} = 0.534 Q^{3/4}. Energies are dimensionless.

**Discretisation.**
- Grid: N³ points on [−7.5, 7.5]³ with spacing h = 15/(N−1). φ = e₃ on the whole boundary of the grid, as in Sutcliffe's runs.
- σ-model term on links: E₂ = h Σ_links |φ(x+eᵢ) − φ(x)|².
- Skyrme term on plaquettes: for each (i, j) plaquette with i-edges a, c and j-edges b, d, E₄ = (1/4h) Σ [|a×b|² + |a×d|² + |c×b|² + |c×d|²]. This average over the four corner pairings has no checkerboard null modes.
- The gradient is the exact derivative of the discrete energy. On smooth fields the lattice energy converges from below at second order.

**Minimisation.**
- Method: arrested Newton flow, as in Sutcliffe 2007. The dynamics is φ_tt = −h⁻³ ∂E_lat/∂φ, projected onto the tangent plane (σ-model kinetic term only), integrated by symplectic Euler with dt = 0.1h. The velocity is set to zero whenever the energy rises.
- Safeguard: if the energy rose over a 10-time-unit interval (an instability of the explicit integrator), the last stored field is restored and dt is multiplied by 0.7. Every such event is logged.
- Grids: each charge is relaxed on N = 76 (h = 0.2), then 101 (0.15), then 121 (0.125, Q = 1 and 2 only), then 151 (h = 0.1, Sutcliffe's grid). Each stage starts from a tricubic interpolation of the previous one.
- Stage end: relative energy change below 10⁻⁷ over 20 time units, after a minimum flow time (40 by default; 300–400 at N = 76 for Q ≥ 3, so that knots and links can rearrange). Budget rules for the finest stages are listed under Deviations.

**Initial conditions.** All start from Sutcliffe's rational-map ansatz: (Z₁, Z₀) = ((x₁+ix₂) sin f/r, cos f + i x₃ sin f/r), with f = π(7.5 − r)/7.5 and W = (φ₁+iφ₂)/(1+φ₃).

| Q | initial map W |
|---|---|
| 1 | Z₁/Z₀ |
| 2 | Z₁²/Z₀ |
| 3 | Z₁³/Z₀ (squashed by ±2% to break the axial symmetry) |
| 4 | Z₁²/Z₀² |
| 5 | Z₁Z₀/(Z₁³+Z₀²) |
| 6 | Z₁³/(Z₁²−Z₀²) (Sutcliffe's link ansatz, eq. 3.7 with n = 2) |
| 7 | Z₁²Z₀/(Z₁³+Z₀²) (the preregistered trefoil map) |

Every centre is offset by (0.05, 0.03, 0.02) to break the lattice symmetries.

**Measurements.**
- *Hopf charge* by the Whitehead integral. B comes from exact plaquette solid angles (F_jk = φ·(∂ⱼφ×∂ₖφ)). A solves curl A = B by FFT in Coulomb gauge, and Q = (1/16π²) ∫ A·B.
  - The raw integral gives Q_W = −nm for Sutcliffe's ansatz W = Z₁ⁿ/Z₀ᵐ. Every Q and linking number below is multiplied by −1 to match his sign; only |Q| matters here.
  - A lattice hedgehog count (cells with non-zero net solid-angle flux) is zero in every field.
- *Curves.* Two curves are extracted as oriented closed polygons:
  - the position curve, where φ = −e₃;
  - the linking curve, where φ = (√(2μ−μ²), 0, −1+μ) with μ = 0.1.
- *Diagnostics on the curves:*
  - number of components;
  - Alexander polynomial of each position component, from 3 random projections;
  - linking matrix, from 3 projections;
  - Q from linking numbers, i.e. the total linking between position and linking curves (estimator-free);
  - twist of each component, T_a = Lk(C_a, linking curve) − Σ_{b≠a} lk(C_a, C_b);
  - planarity and circularity of each loop;
  - inertia tensor of the energy density;
  - degree m of the field on half-planes bounded by the symmetry axis.
- *Classification rules:*
  - A_{Q/m, m}: axial, every loop a planar circle, unlinked unknots, slice degree m.
  - Ã_{T,1}: a single unknotted loop that is not axial.
  - K₃,₂: a single loop with the trefoil's Alexander polynomial t² − t + 1.
  - L^{lk,lk}_{T₁,T₂}: two loops.

**Checks of the tools.** tests.py was rerun in this session.
- The discrete gradient matches finite differences to 1.1 × 10⁻¹⁰.
- On a smooth field, the ratios of successive differences are 3.95 (E₂) and 3.81 (E₄); 4 means second order.
- Rational-map fields of known charge (|Q| = 1 to 7) give |Q| within 0.026 of the integer at N = 101 and within 0.012 at N = 151.
- Alexander polynomials of parametric curves: trefoil t² − t + 1, unknot 1, figure-eight t² − 3t + 1. Linking number of a Hopf link: ±1.
- The Q = 7 initial field has one trefoil position curve with Q_link = 7.
- check_ansatz_energy.py compares the lattice energy of an analytic Gaussian-profile field with an exact Gauss–Legendre quadrature (1.5225976). The lattice energy is −0.86%, −0.47%, −0.20% and −0.11% off at h = 0.2, 0.15, 0.1 and 0.075, i.e. converging as h². This checks the normalisation C₀.

**Convergence and finite-size studies.**
- *Resolution.* Four spacings for Q = 1 and 2, three for the other charges. The continuum value is estimated by fitting E(h) = E₀ + a h² + b h⁴ to the three finest spacings. The quoted spread covers four fit variants.
- *Axisymmetric 2D reduction (axial2d.py).* This is independent code with its own lattice and L-BFGS minimiser, for A_{n,1} with n = 1 and 2: φ = R₃(nθ) ψ(ρ, z).
  - Normalisation check: on the Gaussian ansatz its Richardson value matches the quadrature to 10⁻⁸.
  - Runs: h = 0.2, 0.1 and 0.05 in a cylinder of radius R = 7.5 (ρ ≤ R, |z| ≤ R), and cylinders R = 7.5, 12, 18, 25 at h = 0.2 and 0.1.
- *3D box study* at dx = 0.2: L = 10 against L = 7.5, for Q = 1 and 2.
- *Stencil diagnostic (stencil_check.py).* The same fields are evaluated with a second-order centred-difference energy.

## Calibration

Targets are from Sutcliffe 2007 (arXiv:0705.1468), Table 2, read in the source text: dx = 0.1, 151³ grid, fixed boundary. He describes his absolute energies as about 1% low and his relative ones as accurate to about 0.1%. We compare our energies on the same grid and box as the table: dx = 0.1, 151³, [−7.5, 7.5]³, φ = e₃ on the boundary. PLAN fixed the table and the tolerances but not this convention, so the absolute-energy verdicts are labelled *same grid*. Against the continuum, Sutcliffe's table is about 2% low (see the table below and Finding 4a). Two parts of the calibration do not depend on the convention: the ratios and the types. *(Convention made explicit in reconciliation.)*

| quantity | ours | target | tolerance | source | verdict |
|---|---|---|---|---|---|
| E₁ (dx = 0.1) | 1.2226 | 1.204 | 2% | Sutcliffe T2 [read] | CALIBRATED, same grid (+1.55%) |
| E₂ | 1.9925 | 1.967 | 2% | " | CALIBRATED, same grid (+1.30%) |
| E₃ | 2.7885 | 2.754 | 2% | " | CALIBRATED, same grid (+1.25%) |
| E₄ | 3.5058 | 3.445 | 2% | " | CALIBRATED, same grid (+1.76%) |
| E₅ (optional) | 4.1639 | 4.095 | 2% | " | CALIBRATED, same grid (+1.68%) |
| E₆ (optional) | 4.7234 | 4.650 | 2% | " | CALIBRATED, same grid (+1.58%) |
| E₇ (optional) | 5.3362 | 5.242 | 2% | " | CALIBRATED, same grid (+1.80%) |
| E₂/E₁ | 1.6297 | 1.6337 | 1% | " | CALIBRATED (−0.24%) |
| E₃/E₁ | 2.2807 | 2.2874 | 1% | " | CALIBRATED (−0.29%) |
| E₄/E₁ | 2.8674 | 2.8613 | 1% | " | CALIBRATED (+0.21%) |
| E₅/E₁ | 3.4057 | 3.4012 | 1% | " | CALIBRATED (+0.13%) |
| E₆/E₁ | 3.8633 | 3.8621 | 1% | " | CALIBRATED (+0.03%) |
| E₇/E₁ | 4.3645 | 4.3538 | 1% | " | CALIBRATED (+0.25%) |
| types Q = 1…7 | A₁,₁, A₂,₁, Ã₃,₁ (bent), A₂,₂, L^{1,1}_{1,2}, L^{1,1}_{2,2}, K₃,₂ | same | same type | " | CALIBRATED (all 7) |
| Hopf charge, dx = 0.1 fields | max \|Q − n\| = 0.004 (solid-angle estimator); 0.007 (cross-check's free-space estimator) | integer | 0.05 | PLAN | CHECK PASSED (internal check) |
| E₁, continuum, infinite volume | 1.2248 ± 0.0003 (cross-check, spectral: 1.22493) | 1.21–1.22 | none set | PLAN context; Sutcliffe: "around 1.21" | CHECK PASSED (two codes agree); 0.4% above the context range, explained in Finding 3 |

**The same energies against the continuum** *(added in reconciliation)*. Below, Sutcliffe's table is compared with our same-box continuum estimates (dx → 0, same box and boundary). The cross-check's fourth-order energies of our fields agree with these estimates to within −0.02%/+0.07%.

| Q | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| same-box continuum | 1.2303 | 2.0024 | 2.8015 | 3.5212 | 4.1822 | 4.7427 | 5.3567 |
| table relative to it | −2.1% | −1.8% | −1.7% | −2.2% | −2.1% | −2.0% | −2.1% |

Under a continuum convention, Q = 1, 4, 5 and 7 would fall just outside the 2% tolerance; Q = 1 and 4 are required charges. Infinite-volume continuum values exist only for Q = 1 and 2; against them the table is 1.7% low for both. The ratio verdicts hold under either convention: the continuum ratios differ from Sutcliffe's by −0.45% to +0.02%. The type verdicts do not depend on the convention.

**Hopf charge.** Measured |Q| by spacing (dx = 0.2 → 0.1), from two Whitehead estimators and from linking numbers:

| Q | solid-angle estimator (ours) | free-space 4th-order estimator (cross-check) | from linking numbers |
|---|---|---|---|
| 1 | 0.992, 0.996, 0.997, 0.998 | 0.983, 0.994, 0.997, 0.998 | 1 at every spacing |
| 2 | 1.990, 1.995, 1.997, 1.998 | 1.979, 1.992, 1.996, 1.998 | 2 at every spacing |
| 3 | 2.987, 2.993, 2.997 | 2.973, 2.990, 2.997 | 3 at every spacing |
| 4 | 3.987, 3.994, 3.998 | 3.928, 3.978, 3.995 | 4 at every spacing |
| 5 | 4.985, 4.992, 4.997 | 4.933, 4.978, 4.994 | 5 at every spacing |
| 6 | 5.984, 5.992, 5.997 | 5.931, 5.977, 5.994 | 6 at every spacing |
| 7 | 6.983, 6.991, 6.996 | 6.914, 6.973, 6.993 | 7 at every spacing |

*(Corrected in reconciliation.)* We apply the criterion |Q − n| ≤ 0.05 to the dx = 0.1 fields; both estimators pass there. At dx = 0.2 the result depends on the estimator. Ours stays within 0.017 of the integer, but the cross-check's exceeds 0.05 for Q = 4–7 (0.068–0.086). Both discretise the same integral and converge to the integer as dx falls. The solid-angle fluxes make B exactly divergence-free on the lattice; fourth-order differences do not. The estimator-free check is the linking number of the position and linking curves. It is the exact integer in every field at every spacing: analyze.py computed it on the two finest fields, and qlink_coarse.py (added in reconciliation) on the dx = 0.2 and 0.15 fields. The first version graded the all-grid solid-angle result as CALIBRATED; it is an internal check, not a literature target.

## Findings

**1. Energies and resolution.** Units as above; the last column is the proven bound 0.534 Q^{3/4}.

| Q | E(0.2) | E(0.15) | E(0.125) | E(0.1) | dx → 0 (box 7.5) | spread | E/Q^{3/4} (0.1) | E/(Q E₁) (0.1) | 0.534 Q^{3/4} |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.1965 | 1.2123 | 1.2181 | 1.2226 | 1.2303 | 0.0007 | 1.2226 | 1.0000 | 0.534 |
| 2 | 1.9595 | 1.9794 | 1.9867 | 1.9925 | 2.0024 | 0.0007 | 1.1848 | 0.8149 | 0.898 |
| 3 | 2.7450 | 2.7712 | – | 2.7885 | 2.8015 | 0.0018 | 1.2233 | 0.7602 | 1.217 |
| 4 | 3.4429 | 3.4827 | – | 3.5058 | 3.5212 | 0.0069 | 1.2395 | 0.7169 | 1.510 |
| 5 | 4.0949 | 4.1377 | – | 4.1639 | 4.1822 | 0.0058 | 1.2453 | 0.6811 | 1.785 |
| 6 | 4.6510 | 4.6959 | – | 4.7234 | 4.7427 | 0.0060 | 1.2321 | 0.6439 | 2.046 |
| 7 | 5.2542 | 5.3057 | – | 5.3362 | 5.3567 | 0.0083 | 1.2400 | 0.6235 | 2.297 |

- **Convergence with spacing.** Energies rise monotonically with resolution: our lattice energy approaches the continuum from below. At dx = 0.1 they sit 0.4–0.6% below the same-box continuum estimates (fig_resolution.png). The cross-check made its own 4th-order energy evaluations of our dx = 0.1 fields. It also ran its own 3D relaxation of Q = 1 at spacings we did not use, which gives 1.2304. Both agree with these continuum estimates to ≤ 0.07%.
- **Virial.** The ratio (E₂−E₄)/E at dx = 0.1 ranges from −0.026 (Q = 1) to −0.015 and shrinks in magnitude as dx falls; for Q = 1 it is −0.075, −0.043, −0.033, −0.026. *(Attribution corrected in reconciliation.)* Most of this magnitude is discretisation. Extrapolated to dx → 0 in the same box, it is about −0.012 to −0.013 for Q = 1 (fits v₀ + ah² + bh⁴ to the three finest spacings, or v₀ + ah² to the two finest) and −0.004 to −0.011 for Q = 2–7. That is half (Q = 1) to three quarters of the dx = 0.1 value. The sign, E₄ > E₂, is what a soliton squeezed by the fixed boundary should show. The cross-check's spectral code gives −0.016 (Q = 1) and −0.007 (Q = 2) in the smaller cylinder R = 7.5, and E₂ = E₄ to 10⁻⁶ in infinite volume.
- **Continuum ratios** (same box): E_Q/E₁ = 1.6275, 2.2771, 2.8620, 3.3993, 3.8548, 4.3539 for Q = 2…7. Sutcliffe's are 1.6337, 2.2874, 2.8613, 3.4012, 3.8621, 4.3538. The cross-check's are 1.6276, 2.2772, 2.8618, 3.3992, 3.8547, 4.3538.

**2. Configuration types** (fig_position_curves.png). Each charge has the same type on its two finest grids. Twists are T_a from the Method section. The cross-check's independent curve tracer finds the same seven types.

| Q | type | what the curves show |
|---|---|---|
| 1 | A₁,₁ | One planar circle of radius 1.19 (out-of-plane rms/radius 0.001). Axial (inertia asymmetry < 10⁻⁴), slice degree 1, twist 1. |
| 2 | A₂,₁ | One circle of radius 1.73, twist 2, slice degree 1. |
| 3 | Ã₃,₁ (bent) | One unknotted loop, strongly non-planar (out-of-plane rms/radius 0.22, inertia asymmetry 0.37), twist 3. The cross-check's axial A₃,₁ (2.8229 in infinite volume) lies above it. |
| 4 | A₂,₂ | Axial, slice degree 2. Two nearly coincident unlinked circles of radius 1.81; total linking with the linking curve 4. The split of twist between the two coincident strands is not meaningful. |
| 5 | L^{1,1}_{1,2} | Two unknots linked once, twists 1 and 2: Q = 1 + 2 + 2·1 = 5. |
| 6 | L^{1,1}_{2,2} | Two unknots linked once, twists 2 and 2: Q = 6. Two separate φ₃ < −0.8 tubes. |
| 7 | K₃,₂ (trefoil) | One loop of length 34.1 whose Alexander polynomial is t² − t + 1 in all three projections, on both the dx = 0.15 and dx = 0.1 fields; linking with the linking curve 7. |

**3. Box size and infinite volume** (fig_box_axial.png). *(Box numbers and the infinite-volume estimate corrected in reconciliation.)*
- *Box effect, axial code, R = 7.5 → 25:*
  - Q = 1: 1.22199 → 1.21599 at h = 0.1, a shift of −0.49%. The continuum shift, Richardson-extrapolated from the h = 0.2 and 0.1 shifts, is −0.53%.
  - Q = 2: 1.99625 → 1.99341 at h = 0.1, a shift of −0.14%; the continuum shift is −0.15%.
  - The cross-check's spectral code gives −0.52% and −0.15% for the continuum shifts.
- *Decay of the box effect.*
  - Q = 1: the shift falls off as 1/R³ (fitted exponent 3.00). The energy beyond R = 25 is 1.8 × 10⁻⁴ in the continuum and 1.7 × 10⁻⁴ at h = 0.1; the cross-check's spectral value is 1.8 × 10⁻⁴. The first version estimated "about 10⁻⁴", which was too low.
  - Q = 2: the shift falls off as 1/R⁵ (exponent 5.02), consistent with a higher multipole tail; 7 × 10⁻⁶ lies beyond R = 25.
  - From R = 7.5 to infinity, the continuum shifts are −0.55% (Q = 1) and −0.15% (Q = 2).
- *3D box study at dx = 0.2:* going from L = 7.5 to L = 10 lowers E₁ by 0.20% and E₂ by 0.055%. The cube is larger than the inscribed cylinder, so its shift is smaller.
- *Continuum limits, same nominal box:*
  - Q = 1: axial code 1.2315 (Richardson; Aitken 1.2312), 3D code 1.2303;
  - Q = 2: axial code 2.0035, 3D code 2.0024.
  - The two independent codes agree to 0.1%, and the cylinder sits slightly higher, as expected for the smaller box. In the same cylinder, the cross-check's spectral code gives 1.23156 and 2.00345.
- *Infinite volume.* Add the continuum shift to R = 25 and the tail beyond it to the axial code's R = 7.5 continuum value. That gives:
  - E₁(∞, continuum) = 1.2248 ± 0.0003;
  - E₂(∞, continuum) = 2.0004 ± 0.0001;
  - E₂/E₁ = 1.6333 and E₂/(2E₁) = 0.8166.
  - The cross-check ran a Chebyshev spectral code on all of ℝ³ (compactified radius, converged to 10⁻⁹). It gives 1.2249321, 2.0004701 and 1.63313, so the two agree to 1 × 10⁻⁴.
  - Adding the same cylinder shift to the 3D cube values gives 1.2236 and 1.9994. These are lower estimates: the cube [−7.5, 7.5]³ contains the cylinder, so its box effect is smaller (+0.44% against +0.54% for Q = 1).
  - The first version quoted E₁ = 1.224–1.226 (1.225 ± 0.001) from two estimates, both of which used the h = 0.1 shift. One was 1.2243, from the 3D cube, which overcorrects as explained above. The other was 1.2255, from the axial code alone; it had no energy beyond R = 25, and the h = 0.1 shift is 0.0005 smaller than the continuum one. The two errors had opposite signs, and the quoted range contains the corrected value.
- *Comparison with the literature.* E₁ = 1.2249 is 0.4% above the 1.21–1.22 quoted in PLAN.md and about 1.2% above Sutcliffe's "around 1.21". *(Resolved in reconciliation; the first version left this open.)*
  - Two independent codes with different discretisations agree on the higher value to 10⁻⁴, so it is the literature range that needs revising.
  - The PLAN range is a summary-grade context statement without a tolerance.
  - Sutcliffe's "around 1.21" summarises several authors' computations, and the published values scatter on both sides. Ward (1999, hep-th/9811176) quotes 1.25 from Gladikowski and Hellmund's axially symmetric computation. He also quotes 1.13 from Battye and Sutcliffe's 3D lattice runs, which he expected to underestimate because of the finite volume. Both are in units of the conjectured bound, which is 1 here.
  - Lattice energies such as Sutcliffe's own 1.204 at dx = 0.1 lie below the continuum because of the discretisation (Finding 4). A fixed boundary at |x| = 7.5 raises the energy, by 0.44–0.54% for Q = 1, so the box does not explain the low values in our setting.

**4. Why we are 1.2–1.8% above the table.** Sutcliffe's paper says only "a finite difference scheme"; we have not seen his code. Three observations explain the offset, and a fourth limits what his minimiser can have been.

*(a) Our continuum values are higher still.* Against our same-box continuum estimates, Sutcliffe's dx = 0.1 energies are 1.7–2.2% low: −2.1%, −1.8%, −1.7%, −2.2%, −2.1%, −2.0%, −2.1% for Q = 1…7. So the true discrepancy against the continuum is larger than the 1.2–1.8% at dx = 0.1. The CALIBRATED verdicts above are for the same-grid comparison; against the continuum, Q = 1, 4, 5 and 7 would fall just outside 2%. The cross-check confirms these continuum values with its own fourth-order energies.

*(b) A centred-difference energy reproduces his table.* stencil_check.py evaluates each of our relaxed dx = 0.1 fields with the standard second-order centred-difference energy:

E_c = C₀ h³ Σ [Σᵢ |Dᵢφ|² + Σ_{i<j} |Dᵢφ×Dⱼφ|²],  Dᵢφ = (φ(x+eᵢ) − φ(x−eᵢ))/2h.

| Q | our energy | centred-difference energy, same field | Sutcliffe | centred vs Sutcliffe |
|---|---|---|---|---|
| 1 | 1.2226 | 1.2044 | 1.204 | +0.03% |
| 2 | 1.9925 | 1.9666 | 1.967 | −0.02% |
| 3 | 2.7885 | 2.7534 | 2.754 | −0.02% |
| 4 | 3.5058 | 3.4387 | 3.445 | −0.18% |
| 5 | 4.1639 | 4.0948 | 4.095 | −0.01% |
| 6 | 4.7234 | 4.6472 | 4.650 | −0.06% |
| 7 | 5.3362 | 5.2450 | 5.242 | +0.06% |

The cross-check reproduces this column with its own implementation. On our analytic Gaussian field the centred-difference error is 7.5–8.2 times ours (−1.67% against −0.20% at h = 0.1). *(Qualified in reconciliation.)* The ratio depends on the field: on the cross-check's sharper Gaussian test field it is 7.3–10.6 for h = 0.25–0.075 (10.2 at h = 0.1). "Several times larger" is the safe statement.

*(c) Our coarser grid matches his finer one.* Our dx = 0.2 energies agree with his dx = 0.1 values to within −0.6% to +0.2% for all seven charges.

The natural reading: the offset comes from the larger truncation error of a centred-difference-type energy evaluation, not from a difference in the solutions. That error is close to proportional to E, which is why the ratios agree within 0.3%. This is an inference, because his code was not available. It also explains his own "about 1% low" remark, which he made relative to an assumed true value near 1.21.

*(d) What his minimiser cannot have been (added in reconciliation).* A purely centred-difference energy cannot itself be the functional that was minimised.
- Its grid-scale (k = π) modes cost no gradient energy. Near a soliton, the unit-length constraint also gives them negative curvature: the second variation contains −|∂φ|²|δφ|². Any descent flow therefore amplifies them.
- stencil_relax.py tests this on our Q = 1 dx = 0.1 field with Sutcliffe's own method, arrested Newton flow:

| functional minimised | start | soliton lost by | centred energy then | E_link of the same field |
|---|---|---|---|---|
| 2nd-order centred | + 10⁻⁴ random perturbation | t = 4 (at t = 2: E_c = 0.60, 372 lattice hedgehogs) | 0.036 | 12 (636 at t = 2) |
| 2nd-order centred | unperturbed | t = 3 | 0.41 | 145 |
| 4th-order centred | + 10⁻⁴ random perturbation | t = 2 | 0.73 | 200 |

- A relaxation stage takes t = 40–100. The cross-check saw the same thing with L-BFGS on a fourth-order centred energy at h = 0.1875.
- So if Sutcliffe's numbers are centred-difference energies, his flow must have been stabilised some other way. One way is to discretise the field equations with direct second-derivative stencils, which do penalise grid-scale modes. The Battye–Sutcliffe code lineage that Sutcliffe 2007 cites works that way (hep-th/9811077; hep-th/0103026 §2.3.2), with fourth-order differences.
- The fourth-order centred energy of our dx = 0.1 Q = 1 field is 1.2302, close to the continuum. A fourth-order energy evaluation would therefore not reproduce 1.204; the second-order one does.
- His exact scheme remains unknown. The stencil reading is about how the energy was evaluated, and it matches his seven numbers to ≤ 0.18%.

**5. Seed-relevant numbers.**
- *Energy per unit charge.* E/Q falls monotonically: 1.223, 0.996, 0.929, 0.876, 0.833, 0.787, 0.762.
- *Stability against splitting.* Every E_Q is below the sum for its cheapest split into two lower-charge solutions:

| Q | cheapest split | E_Q below the split by |
|---|---|---|
| 2 | 1 + 1 | 18.5% |
| 3 | 1 + 2 | 13.3% |
| 4 | 2 + 2 | 12.0% |
| 5 | 1 + 4 | 11.9% |
| 6 | 1 + 5 | 12.3% |
| 7 | 1 + 6 | 10.3% |

- *Power law.* A fit E = cQ^p over Q = 1…7 at dx = 0.1 gives p = 0.764 and c = 1.205. Sutcliffe's table at the same charges gives p = 0.763.
- *Ratio to Ward's bound.* E/Q^{3/4} lies between 1.185 (Q = 2) and 1.245 (Q = 5); fig_energy_ratio.png.

## What it means for the seed

- **CONFIRMED (Q = 1–7): E/Q^{3/4} stays near 1.2, the energy per unit charge falls, and bigger folds store charge more cheaply (§4).**
  - For Q = 1–7, E/Q^{3/4} = 1.185–1.245 at dx = 0.1 and 1.19–1.25 after continuum extrapolation.
  - E/Q falls from 1.223 to 0.762.
  - Each soliton is 10–19% below its cheapest split.
  - The energies are those of the solutions reached from one start per charge. They are upper bounds on the minima and match Sutcliffe's survey.
  - With Q ≤ 7 and fixed-boundary boxes, the slow rise of E/Q^{3/4} from Q = 3 to 7 (1.22 → 1.24) is within the size of the finite-box and discretisation effects. It is not interpreted.
- **CONFIRMED: E₂ < 2E₁; a charge-2 fold does not split.** E₂/(2E₁) = 0.815 at dx = 0.1, 0.814 in the continuum (same box), and 0.8166 in infinite volume (our axial code and the cross-check's spectral code).
- **CONFIRMED as a reproduction of the literature minimum: Q = 7 is a trefoil (§4, §6C).** Global minimality was not re-searched here.
  - The trefoil seed relaxes to a stable trefoil: one position loop with Alexander polynomial t² − t + 1, Q_link = 7.
  - Its energy ratio E₇/E₁ = 4.3645 matches Sutcliffe's 4.3538 to 0.25%.
  - Caveat, now in the verdict: only one initial condition was used. That the trefoil is the *global* minimum rests on Sutcliffe's survey (his Table 1 also relaxes an L^{1,1}_{2,3} start into K₃,₂); we did not repeat it.
- **AMENDED: "E ≥ c|Q|^{3/4}; the 3/4 power is the right one, and the computed minima agree (Sutcliffe 2007)" (§4).**
  - Every energy lies above Ward's conjectured Q^{3/4} and above the proven 0.534 Q^{3/4}; the computed minima are 2.2–2.3 times the proven bound.
  - The fitted exponent over Q ≤ 7 is 0.764. That is consistent with 3/4, but a fit over charges this small cannot test an asymptotic exponent.
  - The optimality of 3/4 is a theorem of Lin & Yang (2004), PLAN §3.1. It is not a result of Sutcliffe's numerics, so the seed's attribution should change.
- **CONFIRMED as a reproduction of the literature types: the lowest folds are rings, and each charge has a definite knot or link (§4, §6C).** One start per charge; that these are the global minima rests on Sutcliffe's survey.
  - Q = 1–2 are axial rings, Q = 3 a bent ring, Q = 4 an axial A₂,₂, Q = 5–6 links and Q = 7 a trefoil. All match the literature.
  - Global minimality was not searched independently.

## Deviations from the plan

1. **Compute budget on the finest stages.** The dx = 0.1 stages for Q ≥ 3 were not run to the 10⁻⁷-per-20-units criterion. In each case the remaining energy drift is below 10⁻⁶ relative, far below the 2% and 1% tolerances.

| run | how the dx = 0.1 stage ended | relative energy change over the last 10 time units |
|---|---|---|
| Q3 | stop file at t = 50 | 4 × 10⁻⁸ |
| Q4 | stop_watcher.py rule (t ≥ 20 and change < 10⁻⁶ over 10 units), seen at t = 30 | 2.6 × 10⁻⁷ |
| Q6 | same rule, seen at t = 30 | < 10⁻⁷ |
| Q5 | stop file issued in advance, at t = 20 | 1.4 × 10⁻⁷ |
| Q7 | recorded from its t = 30 checkpoint by finalize_stage.py | the run had reached t = 40, with E lower by 6 × 10⁻⁷ relative |

   Earlier stages were also shortened:
   - Q6's N = 76 stage: minimum flow time lowered from 300 to 150. It had already passed a metastable drop at t ≈ 50.
   - Q6's N = 101 stage: ended at t = 60 by the same 10⁻⁶ rule.
   - Q5's dx = 0.1 stage: ran on 2 threads with dt = 0.07h from the start.

2. **Q7's dx = 0.1 stage.** The container restart killed the process before it wrote its stage summary. finalize_stage.py recomputed the summary from the last checkpoint; the recomputed energy equals the logged one exactly.
3. **Sign of Q.** Hopf charges are reported with Sutcliffe's sign; the raw Whitehead integral gives −Q for his ansatz.
4. **Initial conditions for Q = 5 and 6.** PLAN fixed only the Q = 7 trefoil seed. Q = 6 started from Sutcliffe's link ansatz (eq. 3.7, n = 2); his Table 1 reached L^{1,1}_{2,2} from a K₃,₂ start. Q = 5 started from Z₁Z₀/(Z₁³+Z₀²).
5. **Fix in the analysis.** The original twist rule assigned each linking-curve component to its nearest position component. At Q = 5 the linking curve is a single component threading both loops, and that rule gave L^{1,1}_{0,3}. Link twists are now computed as T_a = Lk(C_a, linking curve) − Σ_{b≠a} lk(C_a, C_b), which gives L^{1,1}_{1,2}. No other label changed.
6. **Additions not in the plan:** the axisymmetric 2D code, the 3D box study, the centred-difference stencil diagnostic and the infinite-volume continuum estimates.
7. **Provenance.** Three agents did this work in turn after interruptions; this report merges their runs. It is the first of the two independent computations that PLAN §2 requires; the crosscheck is separate.
8. **Reconciliation.** After the cross-check, the analysis was corrected and two diagnostics were added: linking numbers on the coarse fields, and three short centred-energy test relaxations. No soliton was re-relaxed and no dx = 0.1 energy changed. See Reconciliation.

## Limitations

- **One initial condition per charge.** Global minimality at Q = 3–7 is taken from Sutcliffe's survey, not re-established here. The seed verdicts carry this caveat.
- **Finite box.** The box effect was measured only for Q = 1 and 2. For larger charges, which are bigger solitons, it is unmeasured, so infinite-volume values are given only for Q = 1 and 2.
- **Continuum extrapolations** rest on three spacings (four for Q = 1 and 2). Fit-variant spreads run from 0.0007 (Q = 1, 2) to 0.008 (Q = 7). The axial box shift is extrapolated from two spacings (h = 0.2, 0.1); its uncertainty is folded into the ±0.0003 on E₁(∞).
- **The stencil explanation is an inference.** It reproduces Sutcliffe's numbers to within 0.2%, but his code was not available to confirm it. A pure centred functional cannot have been what his flow minimised (Finding 4d), so the inference concerns how he evaluated the energy.
- **Hopf-charge estimators.** At dx = 0.2 the Whitehead charge depends on the estimator (0.017 vs 0.086 from the integer). The linking-number charge is exact everywhere.
- **E₁ against the literature.** This is resolved (Finding 3): 1.2248 ± 0.0003 here and 1.22493 from the cross-check's spectral code. The quoted 1.21–1.22 is low.
- **Independence for Q ≥ 3.** The cross-check re-evaluated our Q = 3–7 fields with its own code (energies, charges, types) but relaxed only Q = 1 and 2 independently; its axial A₂,₂ attempt failed. So the Q = 3–7 minima were found by one code.
- **Twists at Q = 4.** For A₂,₂ the two position strands are nearly coincident, so per-component twists are not meaningful; only the total linking of 4 is.
- **Shared machine.** The machine was shared with other experiments (load average about 6 on 4 cores). Wall-clock times below are therefore only indicative.

## How to reproduce

Run from `seed/experiments/E8_hopfions/` with Python 3.13, numpy 2.5.3, scipy 1.18.1, numba 0.68 and matplotlib 3.11. Field checkpoints are written to the scratch directory hard-coded as `SCRATCH_DEFAULT` in relax.py (and as `SCRATCH` in analyze.py, finalize_stage.py, stencil_check.py, stencil_relax.py and qlink_coarse.py). Change it, or pass `--scratch`, elsewhere.

**1. Checks.** Set `NUMBA_NUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2`, then:
- `python3 tests.py`: about 1 minute; writes tests_output.json.
- `python3 check_ansatz_energy.py`: writes check_ansatz_energy.json; a few minutes.

**2. Production.** Single-threaded queues; restart-safe, resuming from checkpoints:
- `python3 stop_watcher.py &`: the budget rule for the dx = 0.1 stages of Q ≥ 4.
- `./run_queueA.sh &`: Q1, Q3, Q7 (its Q5 line was not used).
- `./run_queueB.sh &`: Q2, Q4, Q6.
- `./run_resume_Q6.sh`: how Q6 was actually finished.
- `./run_Q5_after_Q6.sh`, then `./run_Q5_N151.sh`: how Q5 was run.
- `python3 finalize_stage.py --run Q7_K32 --N 151`: records Q7's dx = 0.1 stage after the restart.
- The stop files actually used are kept in runs/STOP_*.

**3. Extras.** `./run_extra.sh` runs axial2d.py (40 min, writes axial2d.json) and the two 3D box runs (box_Q1_L10 3.4 min, box_Q2_L10 9.5 min).

**4. Analysis.**
- `python3 analyze.py`: about 1 minute (results cached per field); writes analysis_raw.json and runs/*_curves.npz.
- `python3 make_results.py`: writes results.json and fig_energy_ratio.png, fig_resolution.png, fig_position_curves.png, fig_box_axial.png.
- `python3 report_tables.py`: the tables in this report.
- `python3 stencil_check.py`: 15 s; writes stencil_check.json.

**5. Reconciliation** (single thread):
- `python3 qlink_coarse.py`: linking-number and solid-angle charges of the dx = 0.2 and 0.15 fields; a few minutes; writes qlink_coarse.json.
- `python3 stencil_relax.py --scheme c2 --tmax 40`, then `--scheme c2 --pert 0 --tmax 30 --log-every 1`, then `--scheme c4 --tmax 30 --log-every 1`. Each run stops by itself within 2 minutes, once the soliton is lost. They write stencil_relax.json and runs/stencil_relax_*.log.
- `python3 make_results.py` again. It now also reads crosscheck/xc_fields.json, crosscheck/xc_axial.json, qlink_coarse.json and stencil_relax.json when present. These feed comparison fields and the `reconciliation` block only; none of our values is taken from the cross-check. Output is logged in runs/make_results_reconcile.out, the tables in runs/report_tables_reconcile.out, and the figures are unchanged.

**Measured wall-clock times** (single thread unless noted):

| run | dx = 0.2 | dx = 0.15 | dx = 0.125 | dx = 0.1 | total |
|---|---|---|---|---|---|
| Q1 | 130 s | 277 s | 192 s | 954 s | 26 min |
| Q2 | 259 s | 365 s | 400 s | 1594 s | 44 min |
| Q3 | 568 s | 284 s | – | 1212 s | 34 min |
| Q4 | 1040 s | 445 s | – | 1633 s | 52 min |
| Q5 | 676 s | 569 s | – | 1120 s (2 threads) | 39 min |
| Q6 | about 6 min (two attempts) | 901 s | – | 1615 s | 48 min |
| Q7 | 875 s | 550 s | – | about 20 min to t = 30 | 44 min |

Run logs (JSON per stage) are in runs/*.log and runs/*.json. All headline numbers, with units, targets, tolerances and verdicts, are in results.json.

## Reconciliation

*Added after the independent cross-check (crosscheck/CROSSCHECK.md, crosscheck.json).* The cross-check reproduced every headline number. Most agree to better than 0.1%: our dx = 0.1 energies exactly, the same-box continuum energies to ≤ 0.07%, E₁ and E₂ in infinite volume, all seven types, and all Hopf charges. It found no blocking or major issue and raised seven minor ones. Each was checked against both codes, with extra computations where the codes alone could not decide. The cross-check was right on all seven, and the corrections are folded into the text above.

| # | issue | finding | change |
|---|---|---|---|
| 1 | Absolute-energy CALIBRATED depends on the convention | Cross-check right. Same grid +1.25% to +1.80% (pass); vs same-box continuum the table is 1.7–2.2% low (Q = 1, 4, 5, 7 outside 2%); vs infinite volume 1.7% low (Q = 1, 2) | Verdicts labelled "same grid"; continuum table added to Calibration; results.json carries both comparisons |
| 2 | Hopf-charge deviation depends on the estimator | Both numbers right; two discretisations of one integral. At dx = 0.1 both pass (≤ 0.004, ≤ 0.007); at dx = 0.2: 0.017 vs 0.086. New: linking-number Q is exact on every field at every spacing (qlink_coarse.py) | Criterion applied at dx = 0.1; verdict CHECK PASSED (internal check, not a literature target); both estimators and Q_link tabulated |
| 3 | E₁ literature discrepancy "not resolved" | Cross-check right. Our corrected 1.2248 ± 0.0003 vs its spectral 1.2249321. The PLAN range is summary-grade; the literature scatters (Ward 1999: axial 1.25, early 3D 1.13). Low lattice values are a discretisation effect; a fixed boundary raises E, so "finite-box underestimate" applies only to Ward's remark about early runs | Finding 3 and Limitations rewritten; calibration row CHECK PASSED |
| 4 | Energy beyond R = 25; box shift | Cross-check right. Our own axial data give a 1/R³ tail with 1.8 × 10⁻⁴ beyond R = 25 (not 10⁻⁴) and a continuum shift of −0.53% (−0.55% to ∞); cross-check −0.52%/−0.54%. The first infinite-volume estimates used the h = 0.1 shift; the 3D-cube one also overcorrected | make_results.py: continuum shift + power-law tail; E₁(∞) = 1.2248 ± 0.0003, E₂(∞) = 2.0004 ± 0.0001; cube estimate labelled a lower estimate; old values kept in results.json |
| 5 | Virial attribution | Cross-check right. Same-box continuum ≈ −0.012 to −0.013 (Q = 1) and −0.004 to −0.011 (Q = 2–7), against −0.015 to −0.026 at dx = 0.1 | Virial bullet rewritten; per-charge continuum estimates in results.json |
| 6 | Stencil wording ("8×"; null modes) | Cross-check right; confirmed by a new test. The ratio is field-dependent (7.5–10.6). Arrested Newton flow on a pure 2nd- or 4th-order centred energy destroys the Q = 1 soliton by t = 2–4, even unperturbed | Finding 4b qualified; Finding 4d added; stencil_relax.py run and documented |
| 7 | Minimality caveat in the seed verdict words | Cross-check right | Verdicts read "CONFIRMED as a reproduction of the literature minimum / types (one start per charge)" |

**What was computed in reconciliation.** No soliton was re-relaxed and no dx = 0.1 energy changed.
- qlink_coarse.py (analysis only, single thread, a few minutes).
- stencil_relax.py, three short arrested-Newton runs of a test functional on the Q = 1 dx = 0.1 field. Each was stopped by the soliton-lost criterion within t ≤ 4, about 5 minutes in total. An interrupted earlier reconciliation attempt had written this script but never run it; it gained `--pert` and `--log-every` options.
- make_results.py rerun. The headline energies, ratios, types and fitted exponent are unchanged. The infinite-volume estimates moved from 1.2243 (E₁) and 1.9996 (E₂) to 1.2248 and 2.0004; E₂/E₁ moved from 1.6332 to 1.6333. The four figures were regenerated byte-identical.

**Verdicts after reconciliation.**
- Calibration:
  - E₁–E₇: CALIBRATED, same-grid comparison at dx = 0.1. Against the continuum the table is about 2% low.
  - E_Q/E₁: CALIBRATED.
  - Types: CALIBRATED.
  - Hopf charge: CHECK PASSED.
  - E₁ and E₂ in infinite volume: CHECK PASSED, two independent codes agreeing, with no preregistered tolerance.
- Seed claims:
  - E/Q^{3/4} near 1.2 with falling energy per charge: CONFIRMED (Q = 1–7).
  - E₂ < 2E₁: CONFIRMED.
  - Q = 7 trefoil: CONFIRMED as a reproduction of the literature minimum (one start per charge).
  - 3/4 power: AMENDED.
  - Rings and definite knots or links: CONFIRMED as a reproduction of the literature types (one start per charge).

**Unresolved.** No discrepancy between the two computations is left open. Two limitations remain, neither of them a discrepancy:
- Sutcliffe's exact scheme is unknown, so the stencil reading stays an inference.
- The Q = 3–7 minima were found by our code only; the cross-check re-evaluated them but did not relax them.
