# A1 polarization gate: blind second leg (leg 2)

**Plain-language summary.** A wave that pushes the vacuum medium back and forth along one direction (its amplitude is a vector) can only stretch an L-shaped interferometer's arms in the *vector* pattern (transverse wave) or the *scalar* pattern (longitudinal wave). It never produces the *plus/cross tensor* pattern that LIGO–Virgo observe. I checked this exactly for every sky direction and polarization. I also checked it numerically on the agreed grid by three independent routes, with finite arms, and for an interferometer built entirely from the medium itself (mirrors at material points, light being the medium's own shear wave, with the most general isotropic strain dependence of its speed). The tensor part is exactly zero in every case. A tensor-looking projection appears only from things that break the medium's symmetry about the wave direction, or at second order in the wave amplitude:
- grain texture and the detector's motion through the medium: both small and model-dependent, and both still vary with polarization angle like a vector;
- second order in the wave amplitude: genuinely spin 2, but about 10⁻²¹ times smaller.

---

## 0. Provenance

- Locked spec: `/home/claude/gifgaf0.github.io/audit_followup/A1_polarization/A1_PREREG.md`, md5 **`d5f6aa3bd50743c5d69e54338494bb27`**. I verified it before reading and the script verifies it again (check 0.1). I read no other file under the excluded paths and ran no git commands.
- Deliverables (all in `/home/claude/a1_leg2/`):
  - `leg2_derive.py`: run `python3 leg2_derive.py` (about 2.5 min; exit 0 iff every check passes).
  - `leg2_output.txt`: its stdout.
  - `leg2_grid.json`
  - this report.
- `_pylib/` holds sympy 1.14.0, installed with `pip --target`. The system Python had no sympy, and this kept every write inside the directory.
- Environment: Python 3.13.16, numpy 2.5.3, sympy 1.14.0.
- **Final run: 74 checks, 74 passed, 0 failed.**

## Conventions (exactly the brief's)

The script uses the brief's k̂, m̂, n̂, p̂, q̂, e_A, D = ½(x̂x̂ − ŷŷ) and F_A = D:e_A, with ε = sym(k̂⊗a) after dropping the common factor −f′/c.
- (p̂, q̂, k̂) is right-handed, and k̂ is the propagation direction.
- The basis is orthogonal with e_A:e_B = 2δ_AB, so c_A = ε:e_A / 2.

Closed-form patterns (verified symbolically, check 1.4e):

| pattern | closed form | ψ spin weight |
|---|---|---|
| F₊ | ½(1+cos²θ)cos2φ cos2ψ − cosθ sin2φ sin2ψ | 2 |
| F× | −½(1+cos²θ)cos2φ sin2ψ − cosθ sin2φ cos2ψ | 2 |
| F_x | sinθ (cosθ cos2φ cosψ − sin2φ sinψ) | 1 |
| F_y | −sinθ (cosθ cos2φ sinψ + sin2φ cosψ) | 1 |
| F_b | −½ sin²θ cos2φ | 0 |
| F_l | (1/√2) sin²θ cos2φ  (= −√2 F_b) | 0 |

---

## Task 1: Kinematics

**Method.** In sympy I set u = a f(t − k̂·x/c), with a symbolic a = (a₁, a₂, a₃), k̂(θ, φ) and an undefined f. Zero-tests are rigorous:
- polynomial reduction modulo k·k = 1, or
- modulo sin² + cos² = 1 (a Gröbner basis), or
- `simplify` for expressions that carry f.

**Results.**
- ε = sym(∇u) = −(f′/c)·½(k̂a + ak̂), exactly (1.1a). The rotation is ω = ½∇×u = −(f′/2c) k̂×a (1.1b), an axial vector with helicity ±1.
- **Helicity decomposition.**
  - Basis: e_± = (m̂ ∓ i n̂)/√2, which rotate as e^{±iα} about k̂ (1.3a). The orthonormal tensor basis is E_{±2} = e_±e_±, E_{±1} = (k̂e_± + e_±k̂)/√2, E_{0l} = k̂k̂ and E_{0b} = P/√2 (1.3b).
  - With a = a_∥k̂ + a₊e₊ + a₋e₋:
    **ε = −(f′/c)[ a_∥ k̂k̂ + (a₊/√2)E₊₁ + (a₋/√2)E₋₁ ]**
  - Helicity ±2: **0**.
  - Helicity ±1: a_±/√2, the transverse part of a.
  - Helicity 0: all of it in k̂k̂ (coefficient k̂·a). The transverse-trace (breathing) component is **0** (1.3c–f).
- **Λ(k̂)ε = PεP − ½P tr(Pε) vanishes identically** for arbitrary k̂, a and f. Three independent proofs:
  - simplification in spherical angles (1.2a);
  - pure polynomial reduction modulo |k|² = 1 (1.2b). The identity needs only |k̂| = 1; without the constraint the raw polynomials are nonzero;
  - the general lemma Λ(k̂) sym(k̂⊗v) = 0 for any vector v (1.2c).
- **Stronger statement.** Only four symmetric tensors can be built linearly from a by an isotropic, even hemitropic, response: sym(k̂⊗a), (k̂·a)I, (k̂·a)k̂k̂ and sym(k̂⊗(k̂×a)). All four have Λ = 0 (1.2d).
  - Reason: k̂ is invariant under rotations about itself, and a carries only helicities 0 and ±1. Nothing linear in a can carry ±2.
  - Spin-weight form of the same fact: ε(R_k̂(α) a) is annihilated by d³/dα³ + d/dα, so its harmonics in α are only 0 and ±1 (1.3g).
  - Control: a_⊥⊗a_⊥ fails that test and passes the spin-2 test (1.3h, 1.3i).

**Classification.**
- Transverse plane wave: pure helicity ±1 (**vector**).
- Longitudinal plane wave: pure helicity 0 (**scalar**, longitudinal; no breathing component).
- Tensor (±2) content: **none**. Λ(k̂)ε ≡ 0.

## Task 2: Antenna mapping

**Methods.**

(a) **Tensor decomposition**, two numerical routes:
- orthogonal projection, c_A = ε:e_A / (e_A:e_A);
- a generic 6×6 linear solve, which does not assume orthogonality.

Both are compared with the symbolic closed form. R is computed three ways: Σ c_A F_A, D:ε directly, and the closed form.

(b) **Direct finite-arm integration**: δL_û(t) = ∫₀ᴸ û·∂_s u(sû, t) ds.
- ∂u comes from complex-step differentiation of the displacement field itself (no strain formula is used), with 64-point Gauss–Legendre quadrature.
- Uniform-strain limit (ramp f): −(δL_x − δL_y)/(2L) reproduces R at all 240 grid points to 1.7×10⁻¹⁶ (2.B1).
- Finite arms (L/λ = 0.3, two-tone waveform):
  - matches the closed form (û·a)[f(t − L k̂·û/c) − f(t)] to 7×10⁻¹⁶ (2.B2);
  - FFT over 32 values of ψ, transverse: |H₁| = 0.93, |H_{m≥2}| ≤ 9×10⁻¹⁷ (2.B3);
  - longitudinal: only m = 0 (2.B4).
- Positive control: a TT metric-type wave sent through the same pipeline shows only m = ±2 (2.B5).

(c) **Fourier analysis in ψ** of R = Σ c_A F_A(ψ):
- transverse: only m = ±1;
- longitudinal: only m = 0;
- calibration: F₊ and F× are spin 2, F_x and F_y spin 1, F_b and F_l spin 0 (2.C1–C3).

**Results (exact).**
- **Transverse wave** a_T(χ):
  - c_x = ½cos χ and c_y = ½sin χ; c₊ = c× = c_b = c_l = 0.
  - R = ½ sin θ [cos θ cos 2φ cos(ψ+χ) − sin 2φ sin(ψ+χ)].
- **Longitudinal wave** a_L = k̂:
  - c_l = 1/√2; every other coefficient is 0, including c_b.
  - R = ½ sin²θ cos 2φ (= c_l F_l).
- All routes agree to ≤ 2.8×10⁻¹⁶. The JSON holds the computed projection values; analytically zero coefficients appear as rounding residue ≤ 1.7×10⁻¹⁶ and are not snapped to 0.
- Sky averages by exact quadrature:
  - ⟨F₊²⟩ = ⟨F×²⟩ = ⟨F_x²⟩ = ⟨F_y²⟩ = 1/5, ⟨F_b²⟩ = 1/15, ⟨F_l²⟩ = 2/15;
  - ⟨R_T²⟩ = 1/20 and ⟨R_L²⟩ = 1/15;
  - **tensor fraction f_T = 0 exactly**.

Sample rows from `leg2_grid.json`:

| wave | θ | φ | ψ | χ | c_x | c_y | c_l | R |
|---|---|---|---|---|---|---|---|---|
| T | 0.3 | 0.0 | 0.0 | 0.0 | 0.5 | 0.0 | ~0 | 0.14116061834875884 |
| T | 0.9 | 0.0 | 0.4 | 0.5 | 0.4387912809451863 | 0.23971276930210156 | ~0 | 0.1513383487326641 |
| T | 1.5 | 2.1 | 0.4 | 1.3 | 0.13374941431229365 | 0.48177909270859653 | ~0 | 0.43330150249447813 |
| L | 1.5 | 0.0 | 0.4 | — | ~0 | ~0 | 0.7071067811865477 | 0.4974981241501115 |
| L | 2.9 | 4.0 | 1.1 | — | ~0 | ~0 | 0.7071067811865476 | −0.00416422853886614 |

**JSON layout.**
- 180 transverse and 60 longitudinal entries.
- Loop order: θ (outermost), φ, ψ, χ (innermost).
- Keys exactly as specified.
- Floats are written with Python's shortest round-trip repr, so they are exact doubles.

**Classification.**
- Transverse: **vector**, spin weight 1 in ψ.
- Longitudinal: **scalar**, spin weight 0.
- Tensor content: zero.

## Task 3: The medium's own detector (no metric assumed)

**Model** (first order in the wave; eikonal along the unperturbed ray; c_T = 1):
- **Geometry.** Arm û of length L, beam splitter at 0 and end mirror at Lû.
- **Probe speed** relative to the local medium is c[1 + d], with
  d = α tr ε + β û·ε·û + γ ê·ε·ê + ζ ê·ε·(d̂×ê).
  - This is the most general isotropic form that is linear in ε and even in ê (a linear polarization is defined up to sign).
  - ζ is the only additional (hemitropic) term, and it is odd in the propagation direction d̂.
  - Off-diagonal terms such as ê·ε·f̂ only convert polarization, which affects the interference signal at second order.
- **Advection.** The probe is advected by the local medium velocity w = ∂u/∂t (Galilean, first order).
- **Mirrors.** They sit at material points. The script also tests two kinds of offset:
  - *universal* offsets Δ = κ₁ a f + κ₂ (k̂·a) k̂ f′ + κ₃ (k̂×a) f;
  - *non-universal* offsets, where the beam splitter and the end mirror respond differently.
- **Round-trip time**, for detection at time t, emission at t₀ = t − 2L/c, and U_E, U_B the end-mirror and beam-splitter displacements:

  T − 2L/c = [2û·U_E(t₀+L/c) − û·U_B(t₀) − û·U_B(t)]/c
  − (1/c) ∫₀ᴸ [d_fwd + d_bwd] ds
  − (1/c²) ∫₀ᴸ [û·w_fwd − û·w_bwd] ds

  The script evaluates this exactly, with complex-step derivatives of u.

**Results.**
- A rigid translation of medium and mirrors gives zero delay at any L: mirror motion and advection cancel exactly (3.1). The signal therefore depends only on gradients.
- **Long-wavelength detector tensor.** I extracted it numerically with static strains and matched it to the formula to 10⁻¹³ (3.2):

  **S/T₀ = G:ε, with G = (1−β)(x̂x̂ − ŷŷ) − γ(ê₁ê₁ − ê₂ê₂)**

  α and ζ drop out, and G is always traceless.
  - Same probe polarization in both arms (vertical, ê₁ = ê₂ = ẑ): G = 2(1−β) D.
  - Perpendicular to each arm in the horizontal plane (ê₁ = ŷ on the x-arm, ê₂ = x̂ on the y-arm): G = 2(1−β+γ) D.
  - Asymmetric control (ẑ, x̂): G = 2(1−β+γ/2) D + (γ/2)(x̂x̂ + ŷŷ − 2ẑẑ). This detector tensor is non-standard, but it still contracts ε.
- **(i) Transverse test wave:** S/T₀ = −(f′/c) B_eff [cos χ F_x + sin χ F_y], with B_eff = 1−β (vertical) or 1−β+γ (perpendicular-horizontal).
  - This is pure vector patterns.
  - Verified against the grid R at all 180 points to 2×10⁻¹⁶ (3.3).
- **(ii) Longitudinal test wave:** S/T₀ = −(f′/c) B_eff sin²θ cos2φ = −(f′/c) B_eff √2 F_l (equivalently +2(f′/c) B_eff F_b).
  - This is the scalar pattern; breathing and longitudinal are degenerate for a traceless detector tensor.
  - Verified at all 60 points (3.3).
- **Offsets.**
  - Universal offsets only rescale or rotate the vector amplitude inside sym(k̂⊗·), possibly with a different time dependence. The patterns stay F_x and F_y (and F_l for the longitudinal wave).
  - Non-universal offsets are an equivalence-principle-violating option. They add a dipole term 2(κ_E − κ_B)(x̂ − ŷ)·a f/c that is not suppressed by L/λ. It is not one of the six standard patterns, but it is linear in a, so its spin weight is at most 1.
- **Finite arms** (L/λ = 0.3), all couplings on, three offset models × three polarization configurations (3.4):
  - transverse: |H_{m≥2}| ≤ 4.5×10⁻¹⁶ against |H₁| ≈ 2–4;
  - longitudinal: only m = 0.

**Can a helicity-±2 term appear? No.** For any coupling constants, offsets, probe polarizations and arm length, the differential signal is a linear functional of the vector amplitude a.
- Rotating a about k̂ by ψ can only produce harmonics 0 and ±1.
- In the long-wavelength limit the signal is G:ε with Λ(k̂)ε ≡ 0, so c₊ = c× = 0 whatever G is.

## Task 4: Other possible helicity-±2 sources

**(a) Internal field components that are scalars under spatial rotation.**
- The only symmetric tensors linear in such an amplitude are β₁ I + β₂ k̂k̂, and Λ of these is 0 (4a.1). They carry helicity 0 only: the breathing/longitudinal pattern, independent of ψ.
- Spatial-vector internal fields (for example microrotations) also give at most ±1.
- Only an internal field that is a spatial tensor of rank ≥ 2 could carry ±2 at linear order.
- Through a single-crystal map, a scalar amplitude can pick up an O(η) e₊/e× projection, but it stays ψ-independent and averages to zero in the aggregate (4b.6).

**(b) Anisotropic single-crystal response map.**
- The wave's strain is still sym(k̂⊗a); this is kinematics, so Λε ≡ 0 regardless of the medium.
- Anisotropy enters only through the response map. I modelled it as T_eff = ε + η Q_dev:ε, where Q_dev is a cubic, deviatoric fourth-rank tensor and η its strength.
- Λ(k̂)T_eff is then nonzero at O(η): up to 0.05 for η = 0.1, so c₊ and c× ≠ 0 when the response is rewritten with the standard D. Equivalently, the detector tensor becomes D + η Q_dev:D while the wave itself stays vector.
- R(ψ) stays first-harmonic: c₊ and c× vary as ψ and 3ψ, never 2ψ (4b.3).
- Size:
  - single crystal: f_T ≈ 0.075 η² under the Λ-projection definition;
  - N randomly oriented grains on the probe path: the residual falls as η/√N (fitted slope −0.51), so f_T ≈ 0.075 η²/N;
  - untextured aggregate: exactly zero, because the orientation average is isotropic (4b.4–4b.5).

**(c) Detector moving at v ≈ 1.2×10⁻³ c relative to the medium.**
- Symmetry argument: with a preferred vector V, the response can contain sym(V⊗a). Its TT part, Λ(k̂) sym(V⊗a) = ½|V_⊥|[cos(α+β) e₊ + sin(α+β) e×], is nonzero.
- Explicit Galilean toy (the probe is advected by the flow −V seen in the detector frame) gives T_eff = −(f′/c)[sym((k̂ + V/c)⊗a) + (V·a/c) I] + O(v³). This is a **pure helicity-1 wave about the tilted axis k̂ + V/c** (residual 10⁻⁹).
- The tensor projection amplitude is at most v_⊥/c ≈ 1.2×10⁻³. f_T depends on the reference axis:
  - about the phase normal k̂: f_T ≈ 0.65 (v/c)² ≈ 9×10⁻⁷;
  - about the detector-frame ray (apparent-source) direction k̂ − V/c: f_T ≈ 2.6 (v/c)² ≈ 4×10⁻⁶;
  - about k̂ + V/c: 0.
- ψ spin weight is still 1 (4c.1–4c.4).
- This is consistent with the Eardley–Lee–Lightman–Wagoner–Will classification. For class III₅ (Ψ₃ ≠ 0), whether Ψ₄ is present depends on the observer: Ψ₄′ = e^{−2iφ}(Ψ₄ + 4σ̄Ψ₃ + 6σ̄²Ψ₂) with σ ~ v/c.
- Caveat: the same toy predicts a Michelson–Morley anisotropy of about 7×10⁻⁷, far above experimental bounds. A viable medium needs an emergent-Lorentz completion, and the true coefficient depends on it (it could be zero). The robust statement is a tensor projection of O(v/c) in amplitude, O(10⁻⁶) in power.

**(d) Second order in the wave amplitude.**
- (∇u)(∇u)ᵀ = (f′/c)² a⊗a, and Λ(k̂)(a_⊥⊗a_⊥) = ½|a|²[cos 2α e₊ + sin 2α e×]. This is **genuine helicity ±2 (spin weight 2)** (4d.1–4d.2).
- The Green–Lagrange term (∇u)ᵀ∇u ∝ k̂k̂ is helicity 0 only (4d.3).
- Size relative to the linear term: about |∇u| ~ h ≲ 10⁻²¹, so f_T ~ 10⁻⁴². It sits at 2f and 0, not at the linear waveform.

**(e) Extra: multipath or scattering by texture (a non-plane field).**
- Waves superposed from directions that differ by δ give a TT part proportional to δ (exactly 0.7071 δ in the test, 4e.1).
- For GW170817, staying coherent within about 10 ms over about 40 Mpc requires δ ≲ 2×10⁻⁹, so f_T ≲ 5×10⁻¹⁸.

---

## Assumptions

1. Linear order in the wave amplitude, except 4d. A single plane wave at the detector, except 4e.
2. For Tasks 1–3 the untextured aggregate is treated as a homogeneous isotropic continuum: statistical isotropy is taken to give exactly isotropic response tensors.
3. For Tasks 1–3 the detector is at rest in the medium frame, and helicity is taken about the phase normal k̂.
4. The probe speed equals the GW speed (= c_T, the same branch). The probe is dispersionless. I use a first-order eikonal (perturbations integrated along the unperturbed ray), a common detection time for both arms, and polarization preserved up to sign on reflection.
5. The probe is Galilean-advected by the local medium velocity. In the long-wavelength limit this cancels against mirror motion and does not affect any classification.
6. Normalization follows the brief: the factor −f′/c is dropped and R = D:ε with ε = +sym(k̂⊗a), so R is the half-differential strain.
7. The Task 4 models (the cubic Q_dev map and the Galilean flow) are representative examples backing the symmetry arguments. Their O(1) coefficients (0.075, 0.65, 2.6) are model-specific. η = 0.1 is illustrative; v = 1.2×10⁻³ c; h ~ 10⁻²¹.

## Checks that failed

- **Final run: none (74/74 passed).**
- In the first run, three checks failed. All three were faults in how the checks were built; none reflected the physics:
  - **1.3h:** it used a general a with a longitudinal part, and a⊗a then legitimately contains first harmonics too. I replaced it with a transverse a and added a separate {0, ±1, ±2} test (1.3i).
  - **1.4a and 4d.3:** `sympy.simplify` did not reduce trig polynomials to zero. I replaced it with a rigorous reduction modulo sin² + cos² = 1, after which both pass.
- No numerical check ever failed.

## Disagreements with the spec's definitions that matter

1. **The two definitions in §3 are not equivalent in general.**
   - They agree only when the map from the wave's polarization to T (or to R) is covariant under rotations about k̂. That holds for the case of record, the isotropic aggregate with the detector at rest, and there both give zero.
   - When something fixed breaks that symmetry (texture or single-crystal response, or the detector's velocity through the substrate), they diverge. Λ(k̂)T_eff becomes nonzero, giving c₊ and c× ≠ 0, which is what an F₊/F× fit at a fixed sky position sees. Yet R(ψ) stays first-harmonic, because it is linear in the vector a.
   - Under the ψ definition, the medium wave can **never** have a tensor part at linear order, whatever the medium or detector. So the R-3 bounds mean something only under the Λ definition.
   - §4's sentence "nonzero but bounded … is not 'no tensor component'" therefore depends on which definition governs. The detector-motion term (O(v/c), model-dependent, possibly 0) is exactly the case where this matters. Either way, f_T ≲ 10⁻⁶.
2. **"Helicity about k̂ … in the detector's rest frame (the substrate frame up to v/c)" hides an O(v/c) ambiguity in k̂ itself.** k̂ could be the phase normal, the ray direction, or the apparent source direction. The TT projection of a vector wave about an axis tilted by δ is O(δ), so the R-3(b) number depends on that choice: 0.65 or 2.6 (v/c)² in the toy, and 0 about k̂ + V/c.
3. **Normalization of e_l.**
   - The brief's e_l = √2 k̂k̂ differs from Isi & Weinstein's e^l = ŵ_z⊗ŵ_z, for which F_l = +½ sin²θ cos2φ = −F_b.
   - With the brief's basis, c_l = 1/√2 and F_l = (1/√2) sin²θ cos2φ = −√2 F_b. R and the classification are unchanged.
   - A leg that used Isi & Weinstein's e_l would get c_l = 1 and fail the 10⁻¹⁰ coefficient comparison for a reason that is not physical.
   - The vector-mode signs agree with Isi & Weinstein: (p̂, q̂, k̂) is right-handed and k̂ is the propagation direction.
4. **Breathing and longitudinal are indistinguishable by pattern.** For an L-shaped (traceless) detector, F_l = −√2 F_b, so the only pattern-level class is "scalar". The six-tensor decomposition still separates them: the longitudinal wave is pure c_l, with c_b = 0.
5. **Minor: f_T's normalization is undefined for a vector wave.** "Unit strain-equivalent" in the f_T definition has no TT strain to normalize against. This is irrelevant while f_T = 0, but it needs fixing if the fraction branch is used.

## Files (md5)

| file | md5 |
|---|---|
| `leg2_derive.py` | `70f9fb29c1c1b9329b055c3f5a3fda39` |
| `leg2_output.txt` | `1af769366510cb34778987508e3f84ae` |
| `leg2_grid.json` | `be09df1f112737aca6a3359baaba32fa` |

Sources consulted, for conventions only (no derivation content taken):
- [Isi & Weinstein, arXiv:1710.03794](https://arxiv.org/abs/1710.03794): polarization-tensor and detector-tensor definitions.
- [arXiv:0908.0861](https://arxiv.org/abs/0908.0861): quotes the Eardley–Lee–Lightman–Wagoner–Will E(2) classes and the Ψ transformation under null rotations.
