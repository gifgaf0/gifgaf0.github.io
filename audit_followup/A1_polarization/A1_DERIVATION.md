# A1 — What a detector sees when the transverse channel's wave passes (first leg)

**Plain-language summary.** The ledger's gravitational-wave channel ("S2") is, after grain averaging, the vacuum crystal's ordinary transverse sound wave: the same wave the ledger uses for light. A transverse sound wave shakes the medium sideways, and the stretching it produces always has one direction along the wave's travel. Detectors classify waves by how their signal changes when the wave's polarization is rotated: a gravitational wave of general relativity repeats after a half turn (tensor), this wave only after a full turn (vector). That holds for any detector built from the medium, for any coupling constants, and even in a single anisotropic crystal. Nothing else in the substrate can supply the tensor pattern, because none of its fields has two spatial indices. So the channel presents a pure vector wave, which is the pattern LIGO–Virgo rule out.

**Files.** `a1_derivation.py` (md5 `c9892a6db861683ab47de62521b472d3`) → `leg1_output.txt` (`c33c99eb…`), `leg1_grid.json` (`c46f3007…`), `leg1_results.json` (`997cbfee…`). 43 checks, all pass; about 3.5 minutes. Symbolic identities are decided exactly (half-angle rational parametrization, `sympy.cancel`), so a PASS is a proof of the identity, not a numerical agreement.

**Conventions.** Exactly those fixed in the second-leg dispatch: k̂(θ,φ) = (sinθ cosφ, sinθ sinφ, cosθ); m̂ = ∂k̂/∂θ; n̂ = (−sinφ, cosφ, 0); p̂ = cosψ m̂ + sinψ n̂, q̂ = −sinψ m̂ + cosψ n̂; e₊ = p̂p̂ − q̂q̂, e× = p̂q̂ + q̂p̂, e_x = p̂k̂ + k̂p̂, e_y = q̂k̂ + k̂q̂, e_b = p̂p̂ + q̂q̂, e_l = √2 k̂k̂; detector tensor D = ½(x̂x̂ − ŷŷ); F_A = D:e_A.

---

## 1. Which wave the S2 channel is, on the ledger's own record

- **G-CI1 (§2.91.N, V4.77)** found no gapless helicity-±2 branch in the substrate (F-IRR fires, K = ∅) and killed the strong reading CI-S. Its locked pre-registration (prereg `6c480340`, in `gci1_gate/G_CI1_CC_DISPATCH_INBAND.md`) also **named and foreclosed the vector-carrier reading CI-V**: "The S2 sector is the helicity-±1 transverse acoustic wave itself. This is vocabulary substitution (spin-2 → spin-1) foreclosed by E-2 … Its would-be first surface is A-POL. Recorded so that no post-verdict slide into it can occur silently (PF-3)." The author confirmed PF-3 at the lock. G-CI1's own polarization rule P-POL reads: "{+1, −1}-only → FAIL". With K = ∅ the arm was recorded as VOID-NO-CANDIDATE.
- **G-S2C1 (§2.91.O, V4.80)** then elected E-P2-1(a): "under full SO(3) grain averaging a propagating plane wave's strain carries helicity 0/±1, never pure ±2, so the aggregate S2 channel is the polarization-averaged shear cone itself." In substance this is CI-V. PF-3's tripwire did not fire, and A-POL was never run against it.
- **G-MSCS1 (§2.91.Q, V4.83)** made the identification explicit: "EM and S2 are two descriptors of the one transverse phonon". S2-E₂ is the m = ±2 fraction of the strain *about the crystal axis*; S2-h is "the helicity-±1 fraction of the full traceless strain about k̂".

So the object to test is a plane wave of the untextured aggregate's transverse branch, u(x, t) = a f(t − k̂·x/c_T) with a ⊥ k̂. The m = ±2 content about a crystal axis is a grain-frame label. A detector classifies by helicity about the direction the wave travels.

## 2. Kinematics: the strain has no tensor part (checks K1–K2, H1–H6)

The strain of any plane displacement wave is ε = sym(∇u) = −(f′/c) · ½(k̂a + ak̂). With P = 1 − k̂k̂:

- Pk̂ = 0, so PεP = 0; and tr(Pε) = a·Pk̂ = 0. Hence **Λ(k̂)ε = PεP − ½P tr(Pε) = 0 identically**, for every k̂ and every a (K1, exact).
- On the six-tensor basis, with a = cosχ p̂ + sinχ q̂ + λk̂: c₊ = c× = c_b = 0; c_x = ½cosχ; c_y = ½sinχ; c_l = λ/√2 (H2–H5, exact).
- The physical polarization angle is ψ + χ: cosχ p̂(ψ) + sinχ q̂(ψ) = p̂(ψ+χ) (H6). So the transverse wave is helicity ±1 (vector), the longitudinal part is helicity 0 (longitudinal scalar, no breathing), and **helicity ±2 is absent**.

## 3. Antenna mapping (checks A1–A11)

The six patterns, decided exactly (A1):

| | closed form | spin weight in ψ |
|---|---|---|
| F₊ | ½(1+cos²θ) cos2φ cos2ψ − cosθ sin2φ sin2ψ | 2 |
| F× | −½(1+cos²θ) cos2φ sin2ψ − cosθ sin2φ cos2ψ | 2 |
| F_x | sinθ (cosθ cos2φ cosψ − sin2φ sinψ) | 1 |
| F_y | −sinθ (cosθ cos2φ sinψ + sin2φ cosψ) | 1 |
| F_b | −½ sin²θ cos2φ | 0 |
| F_l | (√2/2) sin²θ cos2φ = −√2 F_b (this e_l normalization) | 0 |

- **S2 (transverse) wave:** R = D:ε = ½(cosχ F_x + sinχ F_y) = ½ sinθ [cosθ cos2φ cos(ψ+χ) − sin2φ sin(ψ+χ)] (A2, A3). Pure vector patterns.
- **Longitudinal wave:** R = F_l/√2 = ½ sin²θ cos2φ (A4). Scalar.
- **Grid:** the 240 points of the common grid are in `leg1_grid.json`; the largest |c₊|, |c×| on the transverse grid is 8.6×10⁻¹⁷, i.e. rounding (A6).
- **Spin-weight test** (64-point FFT in ψ at 40 random sky positions): the S2 wave shows only |m| = 1 (other harmonics ≤ 2×10⁻¹⁷); the longitudinal wave only m = 0; the controls behave as they must, a tensor wave only |m| = 2 and a breathing wave only m = 0 (A7–A10).
- **An arbitrary anisotropic response map** (a random 3×3×3×3 tensor G, response D:sym(G:ε)) still shows only |m| = 1 (A11). Any linear response is linear in a = p̂(ψ+χ), so it can only contain cos(ψ+χ) and sin(ψ+χ). This is why a single crystal, a texture or a detector moving through the medium cannot turn this wave into a tensor wave in the spin-weight sense.

## 4. A detector made of the substrate itself (checks D1–D4)

The framework's detector is built from the same medium. The model:

- **Mirrors.** Any linear, rotation-covariant response to the local wave fields at long wavelength, X = B u with B = β1 + β_L k̂k̂ (frequency-dependent, possibly complex). The knot–lattice vertex of record, −ρ_n u̇·v_s (second-sound paper Sec. 6, derived twice), is of this form: it entrains a knot of impulse P by a fraction of the lattice velocity. Mirrors at material points are β = 1, β_L = 0. The value of β is not needed.
- **Light.** The probe is a short-wavelength transverse phonon of the same medium (CI-W/EM-IN). In material coordinates, in the homogeneously strained isotropic aggregate, its speed is W = c_T [1 + ½(α₁ tr ε + α₂ N·ε·N + α₃ P·ε·P)]. This is the most general isotropic form linear in ε and even in the probe polarization P (acoustoelastic effect). Objectivity removes any dependence on the local rotation.
- **Round trip.** T = 2L_mat/W, so δT/T = δL_mat/L − δW/W.

The differential signal is a multiple of D:ε in every configuration (exact):

| wave | probe polarization | S |
|---|---|---|
| S2 (transverse) | same in both arms (vertical) | 2(β − 1 − α₂/2) · D:ε |
| S2 (transverse) | perpendicular to each arm, horizontal | 2(β − 1 − α₂/2 + α₃/2) · D:ε |
| longitudinal | vertical | 2(β + β_L − 1 − α₂/2) · D:k̂k̂ |
| longitudinal | perpendicular, horizontal | 2(β + β_L − 1 − α₂/2 + α₃/2) · D:k̂k̂ |

So the substrate's own interferometer reads the S2 wave through the standard vector patterns F_x, F_y, with a gain set by medium constants. If the gain vanished, the wave would be invisible at linear order. Either way there is no tensor response.

## 5. Could anything else in the substrate supply helicity ±2? (R-1, check I1)

- **Field content of record** (G-2a-A1 Phase 0, §2.91.R): ψ ∈ ℂ⊗𝕆, 16 real fields that are scalars under spatial rotations, with the spatial–internal direct product holding (F-A1-1 silent: no spin–orbit-type locking). In the crystal phase there is also one spatial vector field, the displacement u.
- **Helicity count.** In an isotropic medium the linear modes carry definite helicity: a scalar supplies h = 0, a vector h = 0, ±1. Helicity ±2 needs a propagating field with two spatial indices, and the field content has none. This is the structural reason behind G-CI1's K = ∅.
- **Internal L_⊥ waves** have no polarization vector at all, so their response is independent of ψ (I1): helicity 0.
- **The oriented three-body term** O = ∫φ_abc ψ_a ∂_xψ_b ∂_yψ_c couples internal and spatial indices only through the antisymmetric ∂_x∧∂_y. For a single plane wave on a uniform background it is a total derivative, and it involves only imaginary octonion indices. It produces no symmetric spatial tensor.

## 6. Admixtures (R-2, R-3)

- **R-2, scalar companions on the cone.** From the ledger's two-leg 3D record (V4.90): second sound c₂/c_T = 0.059–0.061 and first sound c₁/c_T = 2.00–2.19. The internal branches are not on any cone (A2). GW170817 and GRB 170817A arrived within 1.74 s after about 40 Mpc, so −3×10⁻¹⁵ ≤ Δv/v ≤ 7×10⁻¹⁶ (ApJL 848, L13 (2017)). A helicity-0 branch would have arrived about 10⁸ years earlier or later. The on-cone signal of the S2 reading is therefore pure vector, not a vector+scalar mixture.
- **R-3, bounded tensor projections** (reading Λ only; the spin weight stays 1 in every case):
  - texture: the banked windows (G-MSCS-A) cap the texture strength at about 10⁻⁶, giving a TT amplitude of order 10⁻⁶;
  - detector motion through the substrate (v/c ≈ 1.23×10⁻³ against the CMB frame): a toy model gives a TT power fraction of 0.67 (v/c)² ≈ 1.0×10⁻⁶ about the phase normal (B1). The second leg finds 0.65 (v/c)² about the phase normal, 2.6 (v/c)² about the ray direction, and 0 about the tilted axis;
  - second order in the wave amplitude: genuine helicity ±2, but relative size h ≈ 10⁻²¹, power fraction ≈ 10⁻⁴².

## 7. Secondary arms (structural only, no decision weight)

### S-1. Binary radiation and the double pulsar (checks S1a–S1f)

- **Dipole.** A binary's dipole moment of the coupled charge is (g₁ − g₂)·m₁m₂/(m₁+m₂)·r (S1f). It vanishes only if every body carries the same charge-to-mass ratio, which is the universality (equivalence-principle) condition of A4 and KC1(b). Any species dependence radiates at the orbital frequency, enhanced over quadrupole radiation by about (c/v)² ≈ 10⁵ for the double pulsar.
- **Quadrupole.** With universal coupling the leading term is ℓ = 2 at twice the orbital frequency, scaling like GR's (∝ Ω⁶). Its coefficient is set by a coupling the framework does not derive (M.CW). For orientation, take a Maxwell-type vector channel whose static force has Newton's magnitude. Exact angular integrals (S1a, S1b) with the Landau–Lifshitz prefactors give **P_vector/P_GR = 1/4** (S1c): 75 % short of the double pulsar's 1.3×10⁻⁴ agreement (Kramer et al., PRX 11, 041050 (2021)). Matching it needs a coupling four times Newton's in static strength, and a static vector force between like charges repels.
- **Angular pattern.** A helicity-±1 wave cannot carry away J_z = ±2 along the orbital axis, so vector quadrupole emission vanishes on the axis (S1d), where GR's is maximal (S1e). The pulsar timing measures total power only, so it cannot see this. The LIGO–Virgo test with vector-consistent inclination dependence does (Takeda et al. 2021: ln B = 21.1 for GW170817, 51.0 with the jet prior).
- **Reading.** The double pulsar can constrain the coupling but cannot confirm the channel. Not decisive by itself.

### S-2. Pulsar timing against Hellings–Downs (checks S2a–S2c)

Earth-term overlap reduction functions, normalized so that Hellings–Downs → ½ at zero separation, computed by direct sky integration:
- tensor = the Hellings–Downs closed form to ≤ 10⁻⁷ (S2a);
- breathing = (3 + cos ξ)/8 (S2b);
- **vector = ½[3 ln(2/(1 − cos ξ)) − 4 cos ξ − 3]**, with a fit residual of 3×10⁻¹³ (S2c). It grows without bound as ξ → 0 (1.87 at ξ = 0.35 rad, against HD's 0.33) and needs pulsar-term and distance treatment at small separations.

| ξ (rad) | 0.35 | 0.70 | 1.00 | 1.40 | 1.80 | 2.20 | 2.60 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| Hellings–Downs | 0.333 | 0.093 | −0.064 | −0.151 | −0.103 | 0.027 | 0.164 | 0.244 |
| vector (S2 reading) | 1.865 | 0.181 | −0.375 | −0.521 | −0.313 | 0.023 | 0.325 | 0.488 |

- NANOGrav's 15-year data favour Hellings–Downs correlations over an uncorrelated common process with a Bayes factor of 200–1000 (p = 5×10⁻⁵ to 1.9×10⁻⁴; ApJL 951, L8 (2023)). Its polarization search covered transverse modes only, giving HD over scalar-transverse at a Bayes factor of about 2 (ApJL 964, L14 (2024)), and excluded vector modes because they need pulsar distances.
- **Reading.** The S2 reading predicts a correlation curve that is not Hellings–Downs. That is mildly adverse, and untested by NANOGrav for vector modes. Not decisive.

## 8. Result handed to the verdict step

At linear order in the untextured aggregate, the S2 response has **no tensor component**: Λ(k̂)ε ≡ 0, and the response has spin weight 1 in the polarization angle. The pattern is pure vector (F_x, F_y). Any tensor projection under reading Λ is bounded by about 4×10⁻⁶ in power. The verdict and the second-leg comparison are in `A1_VERDICT.md`.
