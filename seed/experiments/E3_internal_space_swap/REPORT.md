# E3 — Swap the internal space: G2 and the flag manifold SU(3)/T²

*Run report, corrected at reconciliation (2026-10-19). The changes are listed in the Reconciliation section at the end; no number of the original run was changed.*

## Question

SEED.md §7.2 asks what happens to the B = 1 fold when the internal space SU(3) is replaced by:
- the group G2;
- the flag manifold SU(3)/T².

PLAN.md §4 (E3) turns this into definite checks.

**G2:**
- the Dynkin indices of its SU(2) subgroups, and the branching of 7 and 14;
- the inertia tensor of the embedded hedgehog on all 14 directions;
- the rigid-rotor spectrum with no Wess–Zumino (WZ) term, including the seed's claim (§2) that every fold is a boson;
- the stability of the embedded hedgehog.

**SU(3)/T²:**
- the moment-map hexagon;
- π₂ = ℤ² charges of explicit maps;
- a π₃ = ℤ (Hopf-type) charge computed through the SU(3) lift.

## Method

All code is in this directory and is deterministic (fixed seeds, single thread). Every script prints its own checks.

### 1. g2 from the octonions (`e3_g2_algebra.py`)

**Octonions.** Imaginary units e₀…e₆, with products e_i e_{i+1} = e_{i+3} (mod 7) and cyclic. Numerical checks: alternative to 1e-14, norm-multiplicative, non-associative.

**g2.** g2 = Der(O), the null space of the linear derivation conditions on 7×7 matrices D:
- dimension 14;
- antisymmetric, and preserves the associative 3-form;
- closed under commutators (residual 8e-16);
- Killing form negative definite, adjoint irreducible, rank 2.

**Conventions:**
- Bilinear form B(X,Y) = −Tr₇(XY). The Killing form equals −4B.
- The Skyrme Lagrangian on G2 uses ½Tr₇. Checked: ½Tr₇ = Tr₃ on su(3) to 3e-16. The embedded long-root hedgehog reproduces the SU(2) static energy to 1e-11.

**su(3).** The stabiliser of e₆ is 8-dimensional. With the complex structure J = L_{e₆} on e₆^⊥ ≅ ℂ³, it acts as all traceless anti-Hermitian 3×3 matrices. The su(3) Casimir on 7 has eigenvalues 4/3 (×6) and 0, so 7 = 3 + 3̄ + 1.

**SU(2) subalgebras** (all with standard relations [T_a,T_b] = ε_abc T_c):
- long: isospin (λ₁, λ₂, λ₃) of that su(3);
- short: the centraliser of the long one (it contains the hypercharge generator);
- index-4: the diagonal of long × short, and also SO(3) ⊂ SU(3);
- principal: T₃ᴾ = T₃ᴸ + 3T₃ˢ, with raising operators built from the simple-root vectors.

**Dynkin index** = −Tr₇(T₃T₃).

**Branching.** From the joint eigenvalues of the long and short su(2) Casimirs on the 7 and the 14. The Cartan subalgebra is span(T₃ᴸ, T₃ˢ). Weights are written as (m_L, m_S), with inner product (λ,μ) = m_L m_L′ + m_S m_S′/3. Long roots then have |α|² = 1 and short roots 1/3.

### 2. Hedgehog (`e3_hedgehog.py`)

L = (F²/16)Tr ∂U∂U† + (1/32e²)Tr[L_μ,L_ν]², with F = F_π in the 186-MeV convention and x = eF_π r.

ODE: (x² + 8 sin²F)F″ + 2xF′ + 4 sin2F F′² − sin2F − 4 sin²F sin2F/x² = 0, with F(0) = π.

Solver: two-sided shooting, matched at x = 3.
- Outward from the origin with slope F′(0).
- Inward from X with the asymptotic form F = C/x² − C³/(21x⁶), which is stable inward.
- Newton iteration on (F′(0), C); DOP853 with rtol 1e-13.
- Run for X = 40, 80, 160.

Integrals use adaptive quadrature, with the tail mapped by t = 1/x. Radial formulas used for comparison:
- I₁ = (2π/3)Λ/(e³F), with Λ = ∫x² sin²F[1 + 4(F′² + sin²F/x²)];
- I₂ = (π/2)(e³F)⁻¹ ∫x²(1−cos F)(1 + F′² + 2 sin²F/x²) (Kopeliovich).

### 3. Inertia tensor on g2 (`e3_inertia.py`)

Rotate the hedgehog: U = A U₀ Aᵀ, with Ω = AᵀȦ = ω_a T_a in a B-orthonormal basis of g2 (long 3, short 3 rescaled by 1/√3, then the 8-dimensional complement).

Then L₀ = A(U₀ᵀΩU₀ − Ω)Aᵀ, and

I_ab = ∫d³x [ −(1/16)Tr₇(M_a M_b) − (1/16) Σ_i Tr₇([M_a,l_i][M_b,l_i]) ],

with M_a = U₀ᵀT_aU₀ − T_a and l_i = U₀ᵀ∂_iU₀, in units of 1/(e³F).

- U₀ = exp(F n̂·X) and its derivatives are exact, via the eigen-decomposition of n̂·X (this works for any embedded SU(2), including the principal one).
- Quadrature: 96 radial Gauss nodes on x = 2t/(1−t), and 12 Gauss × 24 uniform angular points. A coarse grid (48, 8×16) differs by 1.4e-10.
- The same code with 3×3 matrices and Tr₃ gives the SU(3) tensor.
- Static energy and baryon density B = −(1/24π²)·½∫ε_ijk Tr₇(l_i l_j l_k) come from the same quadrature.

### 4. Rotor spectrum (`e3_g2_reps.py`, `e3_g2_su3_branching.py`)

By Peter–Weyl, L²(G2) = ⊕ R⊗R*. Left action = flavour; right action = body frame.
- The short block has zero inertia, so physical states satisfy R_a = 0 on su(2)_short: a right SU(2)_short singlet.
- The spin J is the right SU(2)_long spin. The spatial rotation of the hedgehog equals a right SU(2)_long rotation.
- H = M + J(J+1)/(2I₁) + [C₂(R) − J(J+1)]/(2I₂), with C₂(λ) = (λ, λ+2ρ). In this normalisation C₂(7) = 2 and C₂(14) = 4.

G2 irreps up to dim 500 were constructed as follows:
- weight multiplicities from Freudenthal's formula in exact rational arithmetic;
- checked against Weyl's dimension formula and Weyl invariance;
- branching n(j_L,j_S) = m(j_L,j_S) − m(j_L+1,j_S) − m(j_L,j_S+1) + m(j_L+1,j_S+1).

Independent check: explicit representations Sym²7, Λ²7, 7⊗14, Sym²14 and Λ²14 were built from the 7×7 generators and decomposed by the G2, SU(2)_L and SU(2)_S Casimirs. All 12 components (27, 64, 77, 77′ and the rest) match the Freudenthal branching and C₂ values. The SU(3) content of G2 irreps uses the su(3) Casimir on the same spaces.

Energies are given:
- in units of 1/I₁, using I₁/I₂ = 2.624713 from my own profile;
- in MeV at PLAN's rounded ANW point (F_π = 129 MeV, e = 5.45);
- in MeV at E2's own fitted ANW point (F_π = 129.26 MeV, e = 5.4440; added at reconciliation, `make_results.py` reads it from E2's `results.json`);
- in MeV at an SU(3) refit point. That point comes from fitting the N_c = 3 SU(3) rotor (E(8) = M + 3/8I₁ + 3/4I₂, E(10) = E(8) + 3/2I₁) to the PDG 2026 octet and decuplet centres, 1151.19 and 1382.11 MeV (pdg package; Δ(1232) mixed-charge 1232.0 MeV).

### 5. Stability (`e3_stability.py`, `e3_stability_refine.py`, `reconcile_stability_r40.py`)

Fluctuation U = U₀ exp(φ), φ ∈ g2. With D_iφ = ∂_iφ + [l_i,φ]:

L_i = l_i + D_iφ + ½[D_iφ, φ] + O(φ³).

The second-order energy is
- −(N/16)[Tr(DφDφ) + Tr(l[Dφ,φ])]
- −(N/32)Σ_ij[Tr(G₁G₁) + 2Tr(G₀G₂)],

with N = ½, G₀ = [l_i,l_j], G₁ = [l_i,D_jφ] + [D_iφ,l_j], and G₂ = [D_iφ,D_jφ] + ½([l_i,[D_jφ,φ]] + [[D_iφ,φ],l_j]).

The blocks (3,1), (1,3) and (2,4) carry SU(2)_short spins 0, 1 and 3/2, so the Hessian does not couple them. The (1,3) block decouples even non-linearly, because su(2)_short commutes with su(2)_long and is Killing-orthogonal to it.

**Validation of the quadratic form:**
- Against the full energy of U₀e^{εφ} by central differences with Richardson extrapolation (h = 4e-3 and 2e-3), for random localized φ in each block: agreement 3.5e-10, 1.8e-9 and 7.8e-9.
- On exact zero modes: iso-rotation, G2 rotation, kaon rotation and translation give |Q| ≤ 1.1e-8, against typical Q ~ 10.

**Ritz analysis:**
- Basis φ = Σ h_k(r) Y_lm(n̂) E_A: piecewise-linear radial hats (sinh-spaced, Dirichlet at r = R) × real harmonic polynomials with l ≤ 3 × the internal basis.
- Generalized eigenproblem H c = λ S c, with S the L² metric.
- l ≤ 3 contains complete grand-spin channels K ≤ 2 for (3,1) (isospin 1) and K ≤ 5/2 for (2,4) (isospin ½).
- Runs: R = 20 (30 elements) and R = 40 (40 elements), plus refinement to 15, 30, 60 and 90 elements at R = 20 for the long and kaon blocks.
- Level assignment (added at reconciliation, `reconcile_stability_r40.py`): with the same Ritz machinery, each eigenvector of the (3,1) block is projected onto the Ritz-space images of the six exact zero modes (translations φ = l_i, iso-rotations φ = U₀ᵀT_aU₀ − T_a). A triplet whose content in that span exceeds 0.5 is a zero-mode triplet, otherwise continuum. Runs: R = 20 (nr = 15, 30) and R = 40 (nr = 40, 80).

### 6. Flag manifold (`e3_flag.py`)

**(a) Moment map.** Haar-random U (QR with phase fix; seed 20261019), N = 10³…10⁶. Project diag(U diag(a) U†) = |U|²a onto the plane Σ = const. Compare with the convex hull of the permutations of a:
- inside test;
- area ratio;
- Hausdorff distance.

**(b) π₂ charges.** Lines L₁ = [p(z)] and L₃ = [conj r(z)], with p·r = 0 holomorphic polynomial vectors, and L₂ = (L₁ ⊕ L₃)^⊥. Charge of line k: Q_k = (1/2πi)∫Tr(P_k[∂_θP_k, ∂_φP_k]) dθdφ, computed two ways:
- Gauss–Legendre in cos θ × trapezoid in φ, at 64×128 and 96×192, with derivatives of the projectors by central differences;
- an exact lattice sum of triangle Berry phases (200×400).

Two cases were deformed by a smooth non-holomorphic W(n̂) ∈ U(3).

**(c) π₃ charge.**
- Five configurations g: ℝ³ → SU(3), equal to 1 outside r = 1.3 and C^∞:
  - C1: the SU(2) hedgehog;
  - C2: W(x)·hedgehog·T(x), non-embedded, with T diagonal;
  - C3: a product of two hedgehogs in different SU(2) blocks;
  - C4: an SO(3) hedgehog with f(0) = 2π (real lines);
  - C5: the inverse hedgehog.
- The flag configuration is P_k = g e_k e_k† g†.
- Charge (i): the lift degree B = −(1/24π²)∫ε Tr(ωωω), ω = g⁻¹dg, by spherical quadrature (96 × 32 × 64).
- Charge (ii): the same number from the projectors only, B = −(1/24π²)∫[3Σ_k A_k·B_k + ε_ijk Tr(θ_iθ_jθ_k)].
  - B_k: curvature of line k, from −i Tr(P[∂P,∂P]).
  - Tr θ³: sum over ordered triples of Tr(P_a dP_b P_b dP_c P_c dP_a).
  - A_k: from B_k in Coulomb gauge by FFT, on 64³, 96³ and 128³ grids in a box of side 3.
  - This decomposition of Tr(ω³) is Amari–Sawado 1805.10008 eq. 13; I re-derived it from the Maurer–Cartan equation.
  - The curvature formula was checked against the curl of the lift connection (relative 4e-7).

## Calibration and checks

Verdict words follow PLAN §1. CALIBRATED is used only where a literature target exists. CONFIRMED marks a seed claim or a preregistered PLAN E3 prediction about the fold. CHECK PASSED marks a derived mathematical input or an internal consistency check. (The run had labelled every row CALIBRATED; corrected at reconciliation.)

| quantity | ours | target | tolerance | source | verdict |
|---|---|---|---|---|---|
| Dynkin index, long-root SU(2) | 1.0000000000 | 1 | exact | Mayanskiy 1611.04070 §4, list after Table 2 (A₁ = A₁¹) [read] | CALIBRATED |
| Dynkin index, short-root SU(2) | 3.0000000000 | 3 | exact | Mayanskiy §4, list after Table 2 (Ã₁ = A₁³) [read] | CALIBRATED |
| Dynkin index, A₁⁴ (diag L×S; also SO(3)⊂SU(3)) | 4.0000000000 | 4 | exact | Mayanskiy §4, Table 2 [read] | CALIBRATED |
| Dynkin index, principal SU(2) | 28.000000000 | 28 | exact | Mayanskiy §4, Table 2 [read] | CALIBRATED |
| 14 under SU(2)_L×SU(2)_S | (3,1)+(1,3)+(2,4) | same | exact | Mayanskiy Prop. 4.1 (D½⊗D3/2) [read] | CALIBRATED |
| 14 under principal SU(2) | spin 1 + spin 5 | same | exact | Mayanskiy Prop. 4.1 (D₅) [read] | CALIBRATED |
| 7 under SU(2)_L×SU(2)_S | (2,2)+(1,3) | same | exact | PLAN (expected; derived) | CHECK PASSED |
| C₂(7), C₂(14) | 2.000000000000, 4.000000000000 | 2, 4 | exact | PLAN (normalisation) | CHECK PASSED |
| M_cl (own hedgehog) | 36.461646 F_π/e | 1.2315×3π² = 36.4633 | 0.2% | E2 target (provenance: see below) | CALIBRATED (−4.4e-5) |
| virial E₂ − E₄ | 4.1e-11 M | 0 | 1e-4 | Derrick (theorem) | CHECK PASSED |
| Λ | 50.978739 | 50.9 | 0.5% | ANW via PLAN E2 | CALIBRATED (0.15%) |
| I₂ | 40.678582 /(e³F_π) | arctan ansatz 40.5 | within 1.5% | Praszalowicz [read] | CALIBRATED (0.44%) |
| G2 inertia, long block (×3) | 106.769622 | (2π/3)Λ = 106.769622 | 1e-6 | PLAN E3 (expected) | CONFIRMED (1.6e-12) |
| G2 inertia, (2,4) block (×8) | 40.678582 | SU(3) I₂ | 1e-6 | PLAN E3 (expected) | CONFIRMED (1.7e-12) |
| G2 inertia, short block (×3) | < 7e-19 | 0 | 1e-10 | PLAN E3 (expected) | CONFIRMED |
| su(3) directions inside G2 vs 3×3 SU(3) | max diff 9e-12 | 0 | 1e-10 | Tr₇/2 = Tr₃ | CHECK PASSED |
| lowest G2 rotor states | 1 (J=0), 14 (J=1); no 7 | same | exact | PLAN E3 (seed prediction, SEED §2) | CONFIRMED |
| moment-map image, generic a | hexagon, angles 120°, sides alternating | Schur–Horn hexagon | exact | SEED §7.2; PLAN | CONFIRMED |
| moment-map image, a₁ = a₂ | triangle, 60° | triangle (CP²) | exact | PLAN | CONFIRMED |
| π₂ charges (9 maps) | integers to 1.8e-10 (continuum); exact (lattice) | integers spanning ℤ² | 1e-6 | SEED §7.2; PLAN | CONFIRMED |
| π₃ charge (5 configs) | lift degree 1, 1, 2, 4, −1 (≤ 1.4e-8); projector route same (≤ 4e-8) | integer = lift degree | 1e-3 | SEED §7.2; π₃(F_n) = ℤ: ABW 2101.11638 §1.4 [read]; formula: Amari–Sawado 1805.10008 eq. 13 [read] | CONFIRMED |

**Provenance of the M_cl target** (carried over from the E2 reconciliation, which read the sources): 36.5 F_π/e is ANW's own value, Schechter–Weigel (hep-ph/9907554 §2) give 23.2π f_π/e = 36.44 F_π/e, and the form 1.2315 × 3π² is the standard E/(12π²) rather than a value read in the cited texts. M_cl passes against all three: −0.004%, −0.11% and +0.05%.

Comparison with E2's profile.json, read only after all of the above was computed:
- max |ΔF| = 1.3e-10 on x ≤ 150;
- M 36.46164562 vs 36.46164563;
- Λ 50.97873911 vs 50.97873911;
- J₂ 25.8967896 vs 25.8967896;
- C 8.6385782 vs 8.6385782 (after E2's reconciliation corrected its stored C by 4.5e-10, the two agree to 1.8e-11);
- F′(0) −1.00376411 vs −1.00376411.

## Findings

### 1. G2 embeddings and the B = 1 fold

The long-root SU(2) has index 1, so the embedded long-root hedgehog is a generator of π₃(G2) = ℤ: B = 1.0000000000 with the ½Tr₇ baryon density. This is the SU(3) hedgehog sitting inside G2. It is locally linearly stable in G2 (§5). Whether it is the minimal-energy B = 1 configuration in G2 is OPEN: only local linear stability was shown.

Hedgehogs embedded in the other SU(2)s are smooth configurations with:
- B = 3 (short root), 4 (index 4) and 28 (principal);
- static energy exactly index × M_cl.

They are not claimed to be minima in their sectors.

The element exp(2πT₃ᴸ), the image of −1 ∈ SU(2)_L, equals exp(2πT₃ˢ) = diag(−1 on (2,2), +1 on (1,3)). It is central in the subgroup SO(4) = (SU(2)_L × SU(2)_S)/ℤ₂, but not in G2, whose centre is trivial.

### 2. Inertia

The 14×14 tensor is block diagonal (off-block entries < 5e-12). Its eigenvalues, in units of 1/(e³F_π), are:
- 106.769622 (×3, (3,1));
- 40.678582 (×8, (2,4));
- 0 (×3, (1,3)).

The ratio I₁/I₂ = 2.624713 is a pure number, independent of F_π and e. The 8-fold degeneracy also follows from Schur's lemma, since (2,4) is a real irreducible representation of SU(2)_L × SU(2)_S.

### 3. Rotor spectrum (no WZ term)

Allowed states are the (R, J) pairs with a (J, 0) component in R. Labels [a,b] are Dynkin labels, with a for the 7's weight and b for the 14's.

| R [a,b] | C₂ | J | (E−M)·I₁ | E at PLAN's ANW point (MeV) | E at E2's fit (MeV) | E at SU(3) refit (MeV) | SU(3) content of R |
|---|---|---|---|---|---|---|---|
| 1 [0,0] | 0 | 0 | 0 | 863.0 | 865.7 | 790.4 | 1 |
| 14 [0,1] | 4 | 1 | 3.6247 | 1572.0 | 1573.8 | 1348.4 | 8 + 3 + 3̄ |
| 27 [2,0] | 14/3 | 0 | 6.1243 | 2060.9 | 2062.0 | 1733.2 | 1 + 3 + 3̄ + 6 + 6̄ + 8 |
| 77 [0,2] | 10 | 2 | 8.2494 | 2476.5 | 2477.1 | 2060.4 | 8 + 6 + 6̄ + 15 + 15̄ + 27 |
| 77′ [3,0] | 8 | 1 | 8.8741 | 2598.7 | 2599.2 | 2156.5 | 1 + 3 + 3̄ + 6 + 6̄ + 8 + 10 + 10̄ + 15 + 15̄ |
| 189 [2,1] | 32/3 | 1 | 12.3738 | 3283.1 | 3282.8 | 2695.3 | |
| 77 [0,2] | 10 | 0 | 13.1236 | 3429.8 | 3429.2 | 2810.7 | |
| 273 [0,3] | 18 | 3 | 13.8741 | 3576.6 | 3575.8 | 2926.2 | |
| 448 [3,1] | 15 | 2 | 14.8112 | 3759.9 | 3758.9 | 3070.5 | |
| 182 [4,0] | 12 | 0 | 15.7483 | 3943.1 | 3941.9 | 3214.7 | |

Parameter points:
- PLAN's rounded ANW point (F_π = 129 MeV, e = 5.45): M_cl = 863.04 MeV, 1/I₁ = 195.58 MeV, 1/I₂ = 513.35 MeV.
- E2's own ANW fit (F_π = 129.26 MeV, e = 5.4440): M_cl = 865.75 MeV, 1/I₁ = 195.33 MeV, 1/I₂ = 512.69 MeV. The 14 sits 708.0 MeV above the singlet instead of 708.9; no level moves by more than 0.31%.
- SU(3) refit (fitted inputs): F_π = 113.75 MeV, e = 5.2474, giving M = 790.43 MeV, 1/I₁ = 153.94 MeV, 1/I₂ = 404.05 MeV. The same fit puts the SU(3) antidecuplet at 1757 MeV, in line with PLAN's expectation of about 1760.

The 7, 64 [1,1] and 286 [1,2] have no SU(2)_short singlet and give no state. Every multiplet appears once. Each (R, J) multiplet contains dim R × (2J+1) states.

The ground state is a J = 0 flavour singlet. The lowest flavoured state is the J = 1 14, which contains an SU(3) octet. So in G2 the hexagon (octet) appears among J = 1 bosons, not as a spin-½ ground multiplet.

Figure `fig_g2_spectrum.png` compares the G2 ladder with the SU(2) N/Δ and the N_c = 3 SU(3) rotor at PLAN's rounded ANW point.

### 4. Bosons only, and why

In all G2 irreps up to dimension 500, every SU(2)_L × SU(2)_S component has j_L + j_S ∈ ℤ, so the constraint j_S = 0 forces integer J. The underlying facts hold for every irrep:
- G2 has trivial centre and its weight lattice is the root lattice;
- equivalently, the 2π rotation exp(2πT₃ᴸ) acting from the right equals exp(2πT₃ˢ), which acts trivially on SU(2)_short singlets.

This conclusion does not need the WZ argument. In the collective-coordinate Lagrangian L = −M + ½ I_ab ω_a ω_b + c·ω, a term linear in the body-frame angular velocity ω would shift the right-generator constraint, as the WZ term does in SU(3) (Y_R = N_c B/3). Three invariances exclude it here:
- **Stabiliser gauge invariance.** A → A h(t) with h ∈ SU(2)_short leaves U unchanged. Invariance up to a total derivative requires the restriction of c to su(2)_short to be a character of su(2)_short. su(2) has none, so the constraint stays R_a = 0 on su(2)_short.
- **Invariance under constant h.** The rest of c must be Ad(SU(2)_short)-invariant. Under SU(2)_short, g2 = (3,1) + (1,3) + (2,4), so it can only lie in su(2)_long, the (3,1). This step alone does not exclude a linear term.
- **Rotational invariance.** A spatial rotation of the hedgehog equals a right SU(2)_long rotation (grand-spin symmetry), so the su(2)_long component of c must be Ad(SU(2)_long)-invariant. The adjoint of su(2) has no invariant vector, so c = 0.

In SU(3) the same reasoning leaves exactly one term, because there the stabiliser is U(1)_Y, which has a character; that is where the WZ term enters. In addition, π₁ = π₂ = 0 for G2/SU(2), so no other topological term exists. The Finkelstein–Rubinstein route is also closed: π₁ of the B = 1 configuration space is π₄(G2) = 0.

### 5. Stability of the embedded hedgehog

No negative eigenvalue was found in any block.

| block | R = 20, nr = 30 | R = 40, nr = 40 | interpretation |
|---|---|---|---|
| (3,1) | 7.4e-5 (×3) and 3.5e-4 (×3): zero modes; 8.0e-4 (×3): continuum | 5.4e-5 (×3): zero modes; 1.94e-4 (×3): first continuum level; 3.73e-4 (×3): zero modes, unresolved | translation and iso-rotation zero modes plus continuum. At R = 40, nr = 40 the second zero-mode triplet is not resolved and lies above the first continuum level |
| (1,3) | 7.72e-4 (×3) | 1.93e-4 (×3) | free massless modes: (1/32)(π/R)², exact 1/R² scaling |
| kaon (SU(3) part of (2,4)) | 7.05e-5 (×4), 7.84e-4 | 4.72e-5 (×4), 1.93e-4 | SU(3) rotation zero modes, then continuum |
| (2,4) | 7.05e-5 (×8), 7.84e-4 | 4.72e-5 (×8), 1.93e-4 | = kaon spectrum doubled (difference 1.6e-14, Schur) |

**Level assignment in the (3,1) block** (added at reconciliation, `reconcile_stability_r40.py`). Zero-mode content is the fraction of each Ritz eigenvector lying in the span of the six exact zero modes.

| run | level (×3) | zero-mode content | assignment |
|---|---|---|---|
| R = 20, nr = 15 | 2.11e-4 | 0.988 | zero modes |
| | 7.93e-4 | 0.056 | continuum |
| | 1.11e-3 | 0.860 | zero modes |
| R = 20, nr = 30 | 7.40e-5 | 0.988 | zero modes |
| | 3.47e-4 | 0.990 | zero modes |
| | 8.01e-4 | 0.003 | continuum |
| R = 40, nr = 40 | 5.42e-5 | 0.994 | zero modes |
| | 1.94e-4 | 0.003 | continuum ((1/32)(π/40)² = 1.93e-4) |
| | 3.73e-4 | 0.581 | zero modes, unresolved |
| R = 40, nr = 80 | 1.62e-5 | 0.993 | zero modes |
| | 1.23e-4 | 0.993 | zero modes |
| | 1.94e-4 | 0.002 | continuum (1.9388e-4 → 1.9409e-4 from nr = 40 to 80) |

So in the R = 40, nr = 40 column the zero modes are not all below the continuum: the first continuum level, 1.94e-4, lies between the two zero-mode triplets. At nr = 80 the zero-mode triplets fall to 1.6e-5 and 1.2e-4 while the continuum level stays put, and the expected order returns.

In this basis both zero-mode triplets mix translation and iso-rotation character, for example 32% and 68% for the lowest triplet at R = 40, nr = 40. The exact modes have opposite hedgehog parity, but the hats × harmonic-polynomial basis is not parity invariant. So the triplets cannot be labelled translation or iso-rotation one by one. The cross-check's cubic B-spline basis resolves both triplets: 7.5e-8 and 4.1e-6 at R = 40.

Radial refinement at R = 20 (nr = 15 → 90):
- the two long-block zero-mode triplets fall 2.1e-4 → 2.1e-5 and 1.11e-3 → 6.3e-5. At nr = 15 the 7.93e-4 triplet is the continuum level (zero-mode content 0.06), with the second zero-mode triplet (content 0.86) above it at 1.11e-3;
- kaon zero modes fall 1.9e-4 → 3.4e-5, levelling off at a box-truncation floor (the rotation mode decays only like 1/r²);
- continuum levels are converged.

Conclusion: the embedded B = 1 hedgehog is linearly stable inside G2 within the tested basis. All extra directions are either flat (rotations) or positive. Whether it is the global minimum in the B = 1 sector is OPEN.

### 6. Flag manifold

**Moment map** for a = (1, 0.3, −1.3):
- all 1.1×10⁶ samples lie inside the hexagon of permutations;
- the hexagon has all interior angles 120° and sides alternating √2(a₁−a₂) = 0.98995 and √2(a₂−a₃) = 2.26274; it is regular only when the eigenvalues are equally spaced;
- the sample hull approaches the hexagon slowly (area ratio 0.892, 0.957, 0.985, 0.9955 for N = 10³…10⁶; Hausdorff distance 0.25 → 0.019), because the pushed-forward measure is thin near the vertices.

For a = (1, 1, −2) the image is the equilateral triangle (area ratio 0.99995 at 10⁶). The orbit is then CP², not the flag manifold. See `fig_moment_map.png`.

**π₂.** Results for (Q₁, Q₂, Q₃) are in the table below. Q₁ + Q₂ + Q₃ = 0 to 3e-11. Continuum integrals are within 1.8e-10 of the integers; lattice sums are exact.

| map | (Q₁, Q₂, Q₃) |
|---|---|
| p = (1,z,0), q = (0,0,1) | (1, 0, −1) |
| p = (0,0,1), q = (1,z,0) | (0, 1, −1) |
| p = (1,z,0), q = (0,1,z) | (1, 1, −2) |
| p = (1,z,z²), q = (0,1,z) | (2, −1, −1) |
| Veronese Frenet frame | (2, 0, −2) |
| p = (1,z,z³), q = (0,0,1) | (3, −2, −1) |
| anti-holomorphic | (−1, 0, 1) |
| two non-holomorphic U(3) deformations | unchanged |

The first two maps generate ℤ² (determinant 1).

**π₃.** For C1–C5 the lift degrees are 1, 1, 2, 4, −1 (errors ≤ 1.4e-8). The projector-only formula gives the same integers at 64³, 96³ and 128³ (errors ≤ 4e-8 at 128³), with the following split:
- C1: two CS terms of −4π² each, Γ = 0;
- C4 (real lines): all A_k = 0, so the whole charge comes from Γ = −947.48 = −96π²;
- C2: CS terms (−41.40, −52.39, 0) plus Γ = 44.50.

The sign of the C4 degree depends on the orientation convention of the so(3) generators. `e3_flag.py` uses (L_a)_ij = +ε_aij; the cross-check, with the opposite convention, gets −4. The invariant is |deg| = 4, the Dynkin index of SO(3) ⊂ SU(3).

Multiplying the lift by a T²-valued map does not change the charge (C2 contains such a factor). So the charge belongs to the F2 configuration itself, as π₃(F₂) ≅ π₃(SU(3)) requires.

## What it means for the seed

- **§2, "a G₂-valued field alone makes only bosonic folds": CONFIRMED.** All allowed J are integers. The reason is representation-theoretic: −1_long = −1_short in G2, and physical states are SU(2)_short singlets. It holds for every irrep, and whether or not a WZ term could exist, because stabiliser and rotational invariance exclude any velocity-linear term (Findings §4).
- **PLAN §3 item 5 (the G2 argument needs H⁵(G2;ℝ) = 0): no verdict word, because it is a PLAN literature note, not a seed claim. E3 refines it.** H⁵(G2;ℝ) = 0 is what excludes a WZ term, but the bosonic rigid-rotor spectrum does not rest on it. E3 did not itself compute H⁵(G2;ℝ).
- **PLAN E3 seed prediction, lowest states 1 (J=0) then 14 (J=1), 7 not allowed: CONFIRMED.** The ladder above quantifies it: the gap is 3.62/I₁. That is 709 MeV at PLAN's rounded ANW point, 708 MeV at E2's own fit, and 558 MeV at the SU(3) refit. G2 therefore offers no spin-½ ground multiplet. If the seed wants fermionic matter from a G2 field, it needs extra structure.
- **§3, "G₂ contains SU(3) as the subgroup fixing one imaginary octonion": CONFIRMED.**
- **§4, π₃(G₂) = ℤ, with the long-root (SU(3)) hedgehog as a generator (B = 1): CONFIRMED.** Dynkin index 1 equals B = 1. The short-root hedgehog has B = 3.
- **PLAN E3, "the B = 1 fold is the long-root hedgehog", read as: it is the minimal-energy B = 1 configuration in G2: OPEN.** Only local linear stability was shown. Lower-energy B = 1 solutions elsewhere in G2 are not excluded; that needs full 3D minimisation in G2.
- **PLAN E3 inertia I₁ (×3), I₂ (×8, = SU(3) strange), 0 (×3): CONFIRMED.**
- **Stability of the embedded hedgehog in G2: CONFIRMED for local linear stability. Global minimality: OPEN.** The linear result holds in complete grand-spin channels K ≤ 2 (long) and K ≤ 5/2 ((2,4)) and boxes R ≤ 40.
- **§7.2, the moment-map image of SU(3)/T² is a hexagon: CONFIRMED.** For the torus moment map the angles are 120° and the sides alternate. The hexagon is regular only for equally spaced eigenvalues, and it becomes a triangle (CP²) when two eigenvalues coincide.
- **§7.2, π₂(SU(3)/T²) = ℤ²: CONFIRMED.**
- **§7.2, π₃(SU(3)/T²) = ℤ ("one knot number"): CONFIRMED.** The charge computed from the F2 data alone equals the SU(3)-lift degree.

## Deviations from the plan

1. **Profile.** PLAN says to compute the inertia "with the E2 profile". As instructed for independence, I solved the profile myself and compared with E2's profile.json only at the end (agreement 1e-10).
2. **Parameter points.** PLAN E3 asks for energies "at the E2 parameters". The run took PLAN's rounded ANW point (F_π = 129 MeV, e = 5.45), not E2's own fit (F_π = 129.26 MeV, e = 5.4440). At reconciliation the ladder was added at E2's fit as well: M = 865.75 MeV and a 14–1 gap of 708.0 MeV instead of 708.9, with every level within 0.31%. I also computed an SU(3) refit point myself (F_π = 113.75 MeV, e = 5.2474). All of these are fitted inputs, labelled as such.
3. **Stability method.** PLAN does not fix one. I used the second variation with a Ritz basis, which gives local linear stability only. Global minimality is reported as OPEN.
4. **π₃ formula.** ABW 2101.11638 (read, §1.4) states π₃(F_n) ≅ ℤ and H³ = 0 but gives no charge formula. I used the decomposition of Amari–Sawado 1805.10008 eq. 13 (ABW's ref. 23), re-derived it, and also computed the lift degree directly.
5. **Scope extensions.** Irreps were enumerated to dimension 500 (PLAN said about 300). The index-4 and principal SU(2)s were constructed explicitly, and the SU(3) content of the low G2 multiplets was added.
6. **Reused targets.** The hedgehog calibration targets (M_cl, Λ, I₂ vs arctan) are E2's preregistered targets, re-used to calibrate my own solver. No target or tolerance was changed.
7. **Reconciliation additions.** `reconcile_stability_r40.py` (level assignment in the (3,1) block) and the ladder at E2's own fit were added after the cross-check. Both add numbers; neither changes one.

## Limitations

- **Model.** Rigid-rotor semiclassical quantisation only: no coupling to vibrations or breathing modes, no loop or meson-cloud corrections, no symmetry breaking. The G2 model is the minimal transplant of the Skyrme Lagrangian with ½Tr₇. Other G2-invariant four-derivative terms, such as (Tr L_μL^μ)², were not considered.
- **MeV values.** They use parameters fitted to baryons in SU(2) or SU(3). A G2-valued field has no physical calibration, so only the ratios (in units of 1/I₁, with I₁/I₂ = 2.6247) are model statements.
- **Stability.** The check is linear, in a truncated basis (l ≤ 3, piecewise-linear radial elements, Dirichlet box R ≤ 40). The pion continuum is massless, so there is no spectral gap. Positive semi-definiteness is shown numerically, not proven. Non-linear instabilities and lower-energy B = 1 solutions elsewhere in G2 are not excluded. The zero modes are mesh-limited, and on the coarser meshes one zero-mode triplet can sit above the lowest continuum level (§5).
- **π₃ configurations.** They were built from known SU(3) maps. The projector-only route reproduces the charge without using the lift, apart from finite-difference derivatives of the projectors. It does not construct a lift from arbitrary F2 data.
- **Moment map.** Haar sampling converges slowly to the vertices. The exact statement is Schur–Horn, and the numerics are consistent with it (no sample outside, hull converging).
- **Spectrum.** Freudenthal enumeration covers irreps up to dimension 500. Higher states were not listed.

## How to reproduce

From `seed/experiments/E3_internal_space_swap/`:

    ./run_all.sh                # full pipeline, single thread (sets *_NUM_THREADS=1)
    SKIP_DONE=1 ./run_all.sh    # resume after an interruption (skips steps with logs/<step>.done)

At reconciliation `run_all.sh` was run once from scratch, end to end, with every step executed (no SKIP_DONE). It exited 0 in 1710 s (28.5 min) on a shared 4-core machine, with other jobs running. The step times below are from that run (`logs/run_all.log`); the original run's times are in brackets.

| step | time | writes |
|---|---|---|
| `e3_g2_algebra.py` | < 1 s [1 s] | algebra_results.json, g2_basis.npz (44/44 checks) |
| `e3_hedgehog.py` | 60 s [34 s] | hedgehog_results.json, profile_e3.npz |
| `e3_inertia.py` | 43 s [23 s] | inertia_results.json |
| `e3_g2_reps.py` | 2 s [1 s] | reps_results.json (uses the pdg package for the refit centres; falls back to PLAN's 1151/1382 MeV) |
| `e3_g2_su3_branching.py` | < 1 s [1 s] | su3_branching_results.json |
| `e3_stability.py` | 333 s [301 s] | stability_results.json |
| `e3_stability_refine.py` | 227 s [299 s] | stability_refine_results.json |
| `reconcile_stability_r40.py` | 201 s [new] | reconcile_stability_r40.json |
| `e3_flag.py` | 843 s [951 s] | flag_results.json, fig_moment_map.png |
| `make_results.py` | 1 s [3 s] | results.json, fig_g2_spectrum.png; compares with E2 profile.json and reads E2's fit from E2 results.json if present |

Logs are in `logs/`. The quick variants `python3 e3_stability.py quick` and `python3 e3_flag.py quick` run in about 2 minutes and 1 minute.

## Reconciliation

*Added 2026-10-19, after the independent cross-check (`crosscheck/CROSSCHECK.md`). The cross-check reproduced 61 of 61 compared quantities and every verdict, and raised 8 issues, all minor. Details are in `RECONCILE.md`.*

| # | issue | who was right | resolution |
|---|---|---|---|
| 1 | CALIBRATED used for seed claims and PLAN expectations | cross-check | Verdicts now follow PLAN §1 and are derived from checks in `make_results.py`. CALIBRATED is kept only for literature targets: the Mayanskiy indices and 14 branching, M_cl, Λ, I₂. CONFIRMED marks seed claims and PLAN E3 predictions: inertia blocks, rotor ladder, integer J, moment map, π₂, π₃. CHECK PASSED marks derived inputs and internal checks: 7 branching, C₂, virial, su(3) normalisation, no negative Hessian mode |
| 2 | Stability table, (3,1) at R = 40, nr = 40 | cross-check, one detail imprecise | 1.94e-4 (×3) is the first continuum level, lying between the two zero-mode triplets; this is shown by projecting the Ritz eigenvectors onto the exact zero modes (`reconcile_stability_r40.py`, table in Findings §5). The same problem in the R = 20, nr = 15 refinement row, which the cross-check had not flagged, is corrected: the second zero-mode triplet is at 1.11e-3, not 7.93e-4. In this basis both zero-mode triplets mix translation and iso-rotation character, so the cross-check's label "iso-rotation triplet" for 3.73e-4 does not apply one to one |
| 3 | "centre element" | cross-check | Now "the image of −1 ∈ SU(2)_L, central in SO(4), not in G2 (trivial centre)" |
| 4 | Velocity-linear-term argument incomplete; AMENDED on a PLAN note | cross-check | Argument completed with rotational (right SU(2)_L) invariance (Findings §4). PLAN §3 item 5 carries no verdict word ("refined") |
| 5 | Mayanskiy citation | cross-check | Now cites §4: Table 2 (A₁⁴, A₁²⁸) and the list after it (A₁¹, A₁³), verified in the arXiv PDF |
| 6 | "E2 parameters" | cross-check | Renamed "PLAN's rounded ANW point". The ladder at E2's own fit is added (`parameter_point_E2_fit`): 14–1 gap 708.0 MeV, every level within 0.31% |
| 7 | `run_all.sh` not run end to end | cross-check | Run once from scratch, end to end, single-threaded: exit 0 in 1710 s. Every regenerated output reproduces the original numbers exactly (only runtime fields differ), and both figures are byte-identical. The cross-check's comparison script, re-run on the new `results.json`, still gives 61/61 |
| 8 | "B = 1 fold is the long-root hedgehog: CONFIRMED" | cross-check | Split into two rows: π₃(G2) = ℤ generated by the long-root hedgehog, CONFIRMED; it being the minimal-energy B = 1 configuration in G2, OPEN |

Also carried over from the E2 reconciliation: the provenance of the M_cl target (see the calibration section).

No number of the original run changed, and no seed verdict changed. One row was split into CONFIRMED plus OPEN, and one AMENDED attached to a PLAN note was withdrawn. `results.json` now also holds the final `seed_claims`, a `reconciliation` block, `stability_R40_assignment` and `parameter_point_E2_fit`.
