# E4: the order-21 group on three generations

*SEED.md §3 and §7.3; PLAN.md §4 E4. First agent ran the groups, Yukawa, LNR and most of the fits. After a container restart a second agent finished the fits, added an exact structural-rank scan and robustness checks, and wrote this report. Single computation; the independent cross-check is pending (`crosscheck/`).*

## Question

SEED.md §3 places F₂₁ = ℤ₇⋊ℤ₃ = ⟨D, C⟩ and Klein's PSL(2,7) inside SU(3). Here D = diag(ζ, ζ², ζ⁴), ζ = e^{2πi/7}, and C is the 120° Weyl turn (a cyclic permutation). §3 suggests "PSL(2,7) ⊃ F₂₁ acting on three generations", and §7.3 asks: "give the order-21 group a job … see which couplings it allows." E4 asks four things:

1. Do the groups, their representations and their tensor products come out as published (Luhn, Nasri & Ramond, "LNR")?
2. Which Yukawa and Majorana couplings does each group allow, and what mass matrices follow, before and after vacuum alignments?
3. Does the LNR seesaw example reproduce, and does it survive current data?
4. Which texture classes can fit lepton (NuFIT 6.0) and quark (UTfit 2022) data, and do any of them predict anything?

## Method

**Groups (e4_groups.py, e4lib.py).**
- Generators are built exactly as in `hexagon_check.py`: D, C, Klein's R = (i/√7)P, the flip −(x↔z), and R_f = flip·R·flip⁻¹.
- All arithmetic is exact. A matrix entry is an integer vector over the powers of ζ times a power of 1/7, so the 3×3 matrices live in ℤ[ζ₇, 1/7]. Group closure, conjugacy classes and element orders are computed in this arithmetic.
- Irreps:
  - F₂₁: 1, 1′, 1″, 3, 3̄.
  - PSL(2,7): 1, 3, 3̄, 6, 8 (LNR's explicit matrices, each verified as a homomorphism), and the 7, obtained by projection from 3⊗6 after removing 3̄ and 8 (projector rank 7).
  - All irreps are rotated to an F₂₁-adapted, D-diagonal basis.
- Character tables, Frobenius–Schur indicators, Kronecker products and branching rules come from characters.
- Clebsch–Gordan coefficients are null spaces of the intertwiner equations ρ_c(g)X = X(ρ_a⊗ρ_b)(g) on the generators. They are explicit in the D-diagonal basis for F₂₁, and stored as matrices for every PSL product (`out/reps.npz`).

**Couplings (e4_yukawa.py).**
- Invariant Yukawa tensors are the null space of the generators acting on L̄⊗R⊗H. Majorana tensors use symmetrized N⊗N⊗Φ.
- Cases: L, R ∈ {3, 3̄, 1+1′+1″}, with H and Φ running over every irrep of F₂₁ and of PSL(2,7).
- Mass matrix: M_ij = Σ_a y_a Y^a_ijk ⟨h_k⟩. Covariance M(ρ_H v) = ρ_L M ρ_R† is checked.
- Vacuum alignments and their stabilizers (exact, and up to a phase): (1,1,1), the D-eigenvector (0,0,1), LNR's (−1,1,1), and (0,1,−1).
- Residual symmetries ("direct" approach). For every pair (G_ℓ, G_ν) of subgroups with non-degenerate eigenvalues on the 3, the mixing matrix is U = V_ℓ†V_ν. It is fitted to (s₁₂², s₁₃², s₂₃², δ) over all row and column permutations and complex conjugation: 0 parameters, 4 observables.
  - Majorana neutrinos need G_ν = ℤ₂×ℤ₂ (Klein).
  - For PSL(2,7), "ℤ₂-partial" classes fix one column (the +1 eigenvector of a ℤ₂). The remaining 2-dimensional subspace is rotated by an angle θ and a phase φ: 2 parameters, 4 observables. The fit uses a 91×72 grid in (θ, φ), all permutations, then a Nelder–Mead refinement.

**LNR seesaw (e4_lnr.py).** Exact sympy computation of LNR's operator ψψ′ξξ′ (fermions in 3, familons in 3̄), for which five F₂₁ invariants exist. With u = ⟨ξ⟩ and u′ = ⟨ξ′⟩:
- M_ii = c₀u_iu′_i.
- M_ij = c₁u_iu′_j + c₂u_ju′_i on the C-orbit O_A = {(1,3),(3,2),(2,1)}.
- M_ij = c₃u_iu′_j + c₄u_ju′_i on O_B = {(1,2),(2,3),(3,1)}.
- M_R = diag(u_i²) + α(u_iu_j)_{i≠j}, and M_ν = −M_D M_R⁻¹ M_Dᵀ.
- Inputs: ⟨φ₁⟩ ∝ (1,1,1), ⟨φ₅⟩ ∝ (−1,1,1), β = c₁…₄ = −1.
- Haze: U_PMNS = U_ℓ†U_TB, with a Cabibbo-like charged-lepton rotation λ_e = √(m_e/m_μ).

**Texture survey (e4_fits.py).** LNR framework: all fermions in the F₂₁ triplet, familons φ₁₀ (for Q, u^c, e^c), φ₅ (for L, d^c) and φ₁ (for ν^c) in 3̄, and flavor-singlet Higgs fields. The mass matrices are
- M_e = Dirac(⟨φ₅⟩, ⟨φ₁₀⟩)
- M_D = Dirac(⟨φ₅⟩, ⟨φ₁⟩)
- M_R = Majorana(⟨φ₁⟩; α)
- M_u = symmetric Majorana-type(⟨φ₁₀⟩; α_u)
- M_d = Dirac(⟨φ₁₀⟩, ⟨φ₅⟩).

Each familon takes one of four alignments:

| Alignment | vev | Origin | Real parameters |
|---|---|---|---|
| Z3 | (1,1,1) | κ > 0 vacuum of LNR's potential | 0 |
| P | (e^{if₁}, e^{if₂}, 1) | κ > 0 vacuum manifold; contains LNR's (−1,1,1) | 2 |
| Z7 | (0,0,1) | κ < 0 vacuum | 0 |
| G | (x₁e^{if₁}, x₂e^{if₂}, 1) | generic, put in by hand (LNR's "haze") | 4 |

There are two coupling variants:
- "min" is LNR's leading order: I₃ only in the charged sectors; c₁…₄ = β in M_D.
- "gen" gives all invariants independent complex couplings.

That makes 2×64 lepton classes, 2×16 quark classes, and LNR's exact point (161 in total).

Observables:
- Leptons (7): m_e/m_μ, m_μ/m_τ, r = Δm²₃₁/Δm²₂₁ (normal ordering), s₁₂², s₁₃², s₂₃², δ.
- Quarks (8): m_u/m_c, m_c/m_t, m_d/m_s, m_s/m_b, λ, A, ρ̄, η̄.
- Overall mass scales are not fitted.

Data and error conventions (set in `data_targets.py` before any fit; values checked against the source PDFs in this session):
- NuFIT 6.0 (arXiv:2410.05380 Table 1, IC19 without SK-atm, normal ordering): s₁₂² = 0.307, s₂₃² = 0.561, s₁₃² = 0.02195, δ = 177°, r = 33.83 ± 0.92. The angles and δ use one-sided σ = (3σ edge − best fit)/3.
- UTfit 2022: λ = 0.22519(83), A = 0.828(11), ρ̄ = 0.1609(95), η̄ = 0.347(10).
- Mass ratios: MS-bar at M_Z (Huang & Zhou, arXiv:2009.04851), fitted in log space with relative error max(experimental, 10%).

Fit procedure:
- χ² is minimized by multistart trust-region least squares: min(60, 16 + 2n) starts for n parameters, 4 starts for prescreened-dead classes, then a polish step.
- Seeds come from the CRC32 of the class name, so runs are deterministic.
- N_eff is the largest rank of ∂(obs)/∂(params), taken at the best fit and at 3 random points.

**Survival rule (fixed before fitting).** dof = N_obs − N_eff.
- dof ≥ 1: the class survives if p > 0.01.
- dof ≤ 0: the class "accommodates (no prediction)" if χ² < 1, and is excluded otherwise.

**Structural scan (e4_structure.py; added on resumption).**
- Generic ranks are taken from 40 random points with O(1) moduli (tolerance 10⁻⁹), so that rank deficiency is not confused with hierarchy. A class is structurally dead if M_e, M_u or M_d has rank < 3 or an exact degenerate pair, if M_R is singular, or if the light neutrinos have an exact degenerate pair, at every point.
- Sympy confirms the key case: a (0,0,1) familon in the five-invariant Dirac matrix gives det = 0 and rank 2.

**Convergence and robustness.**
- The group theory is exact; the one floating-point comparison (all 64 entries of LNR's A^[8]) agrees to 3×10⁻¹⁶.
- Fit determinism: six classes refitted from scratch, three from before the restart and three from after, are identical in χ², N_eff and verdict.
- Global minimum: the four lepton classes that fail at χ² = 72.49 reach the same value from independently seeded starts. A 300-start rerun of one of them finds a minimum of 72.498, with no lower one; the polished stored value is 72.490.
- All 37 accommodating fits reach χ² ≤ 1.7×10⁻¹⁷.
- The prescreen (200 random points) and the exact scan agree on all 93 prescreen-dead classes.
- Re-running e4_groups, e4_yukawa and e4_lnr in this session reproduces groups.json, yukawa.json and lnr.json identically (54/54, 15/15 and 14/14 checks pass).

## Calibration

| Quantity | Ours | Target | Tolerance | Source | Verdict |
|---|---|---|---|---|---|
| \|⟨D,C⟩\|, \|⟨D,C,R_f⟩\| | 21, 168 | 21, 168 | exact | SEED §3; LNR 0709.1447 | CALIBRATED |
| R_f and R_f·D vs LNR triplet generators | identical: R_f = A^[3], R_f·D = B^[3] | LNR eqs. (22)–(23) | exact | LNR 0709.1447 | CALIBRATED |
| F₂₁ character table | 3: (3,0,0,b₇,b̄₇); 1′: (1,ω,ω²,1,1) … | LNR §5 | exact | LNR 0709.1447 | CALIBRATED |
| PSL(2,7) character table | 3: (3,−1,0,1,b₇,b̄₇); 6: (6,2,0,0,−1,−1); 7: (7,−1,1,−1,0,0); 8: (8,0,−1,0,1,1) | LNR §3 | exact | LNR 0709.1447 | CALIBRATED |
| F₂₁ Kronecker products | 3⊗3 = (3+3̄)_s + 3̄_a; 3⊗3̄ = 1+1′+1″+3+3̄ | 3+3̄+3̄; 1+1′+1″+3+3̄ | exact | LNR; PLAN | CALIBRATED |
| PSL(2,7) Kronecker products (14) | 3⊗3 = 6_s + 3̄_a; 3⊗3̄ = 1+8; others as LNR | LNR table | exact | LNR 0709.1447 | CALIBRATED |
| PSL → F₂₁ branching | 6 = 3+3̄; 7 = 1+3+3̄; 8 = 1′+1″+3+3̄ | same | exact | LNR | CALIBRATED |
| SU(3) → PSL(2,7), 11 irreps up to (2,2) | e.g. 10 = 3̄+7; 15′ = 1+6+8; 27 = 2·6+7+8 | LNR table (dimensions) | exact | LNR | CALIBRATED |
| LNR A^[8], all 64 entries | max deviation 3×10⁻¹⁶ | LNR eq. (46) | 10⁻¹² | LNR | CALIBRATED |
| F₂₁ Clebsch–Gordan coefficients | all 8 LNR combinations are intertwiners | LNR eqs. (64)–(66) | exact | LNR | CALIBRATED |
| F₂₁ invariants of ψψ′ξξ′ | 5 | 5 | exact | LNR 0706.2341 | CALIBRATED |
| M_Maj, M_Dir, M_ν at α = β = −1 | M_ν = ½[[0,1,1],[1,−4,5],[1,5,−4]] | same | exact | LNR 0706.2341 §4.1 | CALIBRATED |
| Light-ν eigenvalue ratios | 1 : −2 : 9 | 1 : −2 : 9 | exact | LNR | CALIBRATED |
| Δm²₃₁/Δm²₂₁ | 80/3 = 26.667 | 80/3 (26.7) | exact | LNR | CALIBRATED |
| α windows for r ∈ [21.3, 45.1] | (−1.143, −0.946), (−0.220, −0.154) | (−1.15, −0.95), (−0.22, −0.15) | 0.01 | LNR | CALIBRATED |
| θ₁₃ with haze λ_e = √(m_e/m_μ) | 2.819° | 2.8° | 0.05° | LNR §4.2 | CALIBRATED |
| θ₁₂ with the same haze | 32.45° | 32.4° | 0.05° | LNR §4.2 | CALIBRATED |

Notes on the calibration:
- LNR write group actions in a row convention (their eq. 28). In the column convention used here, their 1′ and 1″ singlet combinations exchange (ω ↔ ω²); the triplet Clebsch–Gordan coefficients are identical in both conventions.
- θ₁₃ is 2.792° with MS-bar masses at M_Z.
- The sign of the haze rotation is an input chosen to match LNR; the other sign gives θ₁₂ = 38.09°.
- PLAN's pass criterion ("Kronecker products and LNR outputs reproduce exactly") is met.

## Findings

**1. Allowed couplings.** Number of independent Dirac couplings in L̄⊗R⊗H for F₂₁ (rows L, R; columns H):

| L, R | 1 | 1′ | 1″ | 3 | 3̄ |
|---|---|---|---|---|---|
| 3, 3 | 1 | 1 | 1 | 1 | 1 |
| 3, 3̄ | 0 | 0 | 0 | 1 | 2 |
| 3, 1+1′+1″ | 0 | 0 | 0 | 3 | 0 |
| 1+1′+1″, 1+1′+1″ | 3 | 3 | 3 | 0 | 0 |

For PSL(2,7), L = R = 3 couples only to H = 1 or H = 8 (one coupling each), and L = 3, R = 3̄ couples to H = 3̄ or H = 6.

Closed forms in the D-diagonal basis, for L = R = 3:
- H = 3: M = [[0,0,yh₃],[yh₁,0,0],[0,yh₂,0]].
- H = 3̄: M = [[0,yh₁,0],[0,0,yh₂],[yh₃,0,0]].
- H = 1′: M = yh·diag(1, ω, ω²).

Majorana masses for ν^c in a triplet:
- F₂₁: Φ = 3 gives the off-diagonal [[0,f₃,f₂],[f₃,0,f₁],[f₂,f₁,0]]; Φ = 3̄ gives diag(f₂, f₃, f₁).
- PSL(2,7): only Φ = 6 is allowed.
- Neither group allows a singlet Majorana mass.

**2. Schur (PLAN prediction).** The commutant of the triplet is one-dimensional for both groups. With only a trivial scalar:
- L = R = 3 gives one coupling and three equal masses (singular values 1.0104 ×3 at a random coupling);
- L = 3, R = 3̄ gives no coupling;
- no Majorana mass is allowed.

A single 1′ or 1″ vev still gives equal |masses|. Three distinct masses need 1+1′+1″ vevs together (F₂₁ broken to ℤ₇) or triplet vevs. **An unbroken F₂₁ cannot make a hierarchy.**

**3. Alignments.**
- (1,1,1) is fixed by a ℤ₃.
- (0,0,1) is fixed by no element, but its ray is fixed by ℤ₇.
- LNR's (−1,1,1) and (0,1,−1) are fixed by nothing, not even up to a phase.

With a single triplet Higgs and L = R = 3:
- a ℤ₃-aligned vev gives three equal masses;
- a ℤ₇-aligned vev gives rank 1;
- a generic vev gives masses equal to |vev components| with no mixing (a generalized permutation). The hierarchy is then whatever the vevs are given.

Higgs fields in 1+3+3̄, all ℤ₃-aligned, give a circulant M with |U|² = 1/3 everywhere. With D-eigenvector vevs no common ℤ₇ survives, because the 3 and 3̄ components carry different ℤ₇ phases.

**4. Residual symmetries** (fig_residual_patterns.png).
- F₂₁ has one ℤ₇ and seven ℤ₃ subgroups and, being of odd order, no ℤ₂. On the 3, an invariant symmetric Majorana matrix vanishes under ℤ₇ (D-weight sums 1+2, 2+4, … are never 0 mod 7) and has a degenerate pair under ℤ₃. **No F₂₁ subgroup can be the residual symmetry of a non-degenerate Majorana neutrino mass matrix.**
- F₂₁ (Dirac neutrinos, and quarks): 10 distinct mixing patterns, built from 3 |U|² structures (identity, trimaximal Fourier, ℤ₃–ℤ₃′). All are excluded; the best lepton pattern has χ² = 2459 and the best CKM pattern χ² = 1.08×10⁵ (4 observables, 0 parameters).
- PSL(2,7) (ℤ₇ ×8, ℤ₃ ×28, ℤ₂ ×21, ℤ₄ ×21, ℤ₂×ℤ₂ ×14): 97 full-residual patterns, all excluded. The best lepton pattern is ℤ₃×ℤ₇ with Dirac ν, χ² = 200 (s₁₂² = 0.293, s₁₃² = 0.027, s₂₃² = 0.158). The best Klein–Majorana pattern has χ² = 692. The best CKM pattern has χ² = 7.7×10⁴, with λ = 0.416.
- PSL(2,7) ℤ₂-partial classes (2 parameters, 4 observables, 2 dof): **3 of 12 fit**. Each column below is listed as |U_e·|², then the μ and τ rows in some order.

| G_ℓ | Fixed first column | χ² | p | s₁₂² | s₁₃² | s₂₃² | δ |
|---|---|---|---|---|---|---|---|
| ℤ₇ | (0.664, 0.204, 0.132) | 2.13 | 0.34 | 0.321 | 0.0220 | 0.555 | 253° |
| ℤ₃ (TM1) | (2/3, 1/6, 1/6) | 2.54 | 0.28 | 0.318 | 0.0220 | 0.553 | 284° |
| ℤ₃ (TM2, second column trimaximal) | (1/3, 1/3, 1/3) | 7.63 | 0.022 | 0.341 | 0.0219 | 0.562 | 235° |

  The next class has χ² = 31.5. TM1 and TM2 are the patterns PSL(2,7) shares with its S₄ subgroups. The ℤ₇ class uses PSL's order-7 elements together with a ℤ₂ that F₂₁ does not have.

**5. LNR example** (fig_lnr_alpha.png).
- Every number in the calibration table reproduces.
- For β = −1 the light-neutrino matrix is exactly tri-bimaximal for every α. Its masses are 1/(α−1), −1/(2α+1) and 9/(α−1), so |m₃/m₁| = 9 always.
- Against NuFIT 6.0:
  - sin²θ₁₃ = 0.00242 (with haze) against 0.02195: pull −34.1σ.
  - r = 80/3 against 33.83 ± 0.92: −7.8σ.
  - s₁₂² = 0.288: −1.8σ.
  - s₂₃² = 0.499: −1.4σ in the 3σ-range convention, −4.1σ with the 1σ error.
- Refitting α to r = 33.83 gives α = −1.0621 or −0.1787. θ₁₃ stays exactly 0 without the haze. **The LNR point is excluded, as PLAN predicted.**
- Only the identity of the seed's PSL(2,7) leaves LNR's M_ν invariant. M_ν is invariant under the tri-bimaximal Klein pair (S, μ–τ), but neither is in PSL(2,7) in this representation. **Its tri-bimaximal form comes from the parameter choice, not from a residual symmetry.**

**6. Texture survey** (fig_texture_survey.png; results.json → `texture_survey_all`).

| Sector | Classes | Structurally dead | Fit excluded | Accommodates (N_eff = N_obs) | Survives with dof ≥ 1 |
|---|---|---|---|---|---|
| Leptons | 129 | 90 | 5 | 34 | 0 |
| Quarks | 32 | 29 | 0 | 3 | 0 |

- Before the exact rank scan, 23 of the dead classes were labelled "excluded" with χ² of about 5×10³ to 10⁴. Their best fits had m_e/m_μ or m_d/m_s between 10⁻⁷ and 10⁻⁴, which is rounding noise on a singular value that is exactly zero.
- Causes of structural death:
  - φ₅ or φ₁₀ = ℤ₇ makes M_e (or M_d) rank ≤ 2;
  - φ₁ = ℤ₇ makes M_R singular;
  - ℤ₃-symmetric neutrino sectors give r = 1;
  - in the minimal quark variant M_u and M_d are both diagonal, so CKM is a permutation matrix (LNR: "no quark CKM mixing").
- Every class that fits has N_eff = N_obs, with 10 to 30 real parameters, and predicts nothing. Each needs at least one familon with free phases (P) or a generic vev (G). In the minimal variant every fitting class needs a G vev, which is LNR's "Cabibbo haze" put in by hand.
- The five lepton failures:
  - four minimal classes (φ₅ = G, with φ₁₀ and φ₁ each ℤ₃ or P) at χ² = 72.49 with dof = 0, failing on s₂₃² (0.203; pull −8.2);
  - LNR's exact point (N_eff = 3, dof = 4) at χ² = 1472, with θ₁₃ = 0 (pull −38.3).
- **No alignment class in this framework both fits the data and predicts anything.**

## What it means for the seed

- **§3 group facts: CONFIRMED.**
  - ⟨D, C⟩ = ℤ₇⋊ℤ₃ has order 21 and lies inside the seed's flipped PSL(2,7) of order 168.
  - The seed's R_f is exactly LNR's generator A^[3], so the seed's copy is the one flavor model-builders use.
  - The triplets are complex (Frobenius–Schur indicator 0, b₇ = (−1+i√7)/2). The uniqueness clause of §3 (classification of simple subgroups of SU(3)) was not tested here.
- **§3, "model-builders have used both groups": CONFIRMED.** The LNR model reproduces exactly.
- **PLAN: an unbroken F₂₁ cannot give a triplet three masses: CONFIRMED.** Masses and hierarchy require breaking F₂₁ with flavon vevs, and the hierarchy then comes from the vevs.
- **PLAN: mixing from misaligned residual subgroups: AMENDED.**
  - It holds for PSL(2,7): three 2-parameter ℤ₂-partial classes fit, and they predict s₁₂² ≈ 0.32–0.34 and δ ≈ 235°–284°.
  - It fails for F₂₁ alone. Every F₂₁ residual pattern is excluded, and F₂₁ cannot provide a Majorana residual symmetry at all, so F₂₁ models get their mixing from vevs that leave no residual symmetry.
- **PLAN: the LNR example is excluded by data: CONFIRMED** (θ₁₃ at −34σ, r at −7.8σ).
- **§3/§7.3, "F₂₁ acting on three generations does a job": AMENDED.**
  - What F₂₁ does: it restricts the allowed couplings (the tables above, the five-invariant structure, no bare Majorana mass for a triplet ν^c).
  - What it does not do: give masses or a hierarchy without breaking, or predict anything before vevs are chosen. Of 161 alignment classes in the most developed F₂₁ framework, none fits and predicts.
  - The leptonic patterns that do work come from PSL(2,7)'s ℤ₂ elements, which it shares with S₄, not from the order-21 group.
  - E4 says nothing about why a fold would carry a family index. That link remains an assignment, not a result.

## Deviations from the plan

1. **Interrupted run.** A container restart killed the first agent after 108 of 161 fits. The remaining 53 ran with unchanged code; e4_fits.py resumes from out/fits.jsonl. Determinism was verified by refitting six classes.
2. **Structural scan added after fitting** (e4_structure.py). Twenty-three fit-"excluded" classes were relabelled "excluded (structural)". No pass/fail outcome changed, and results.json keeps both labels.
3. **Robustness script added** (e4_robustness.py): the 300-start check and the six determinism refits.
4. **Error conventions not in PLAN.md.** The 3σ-range/3 one-sided σ for angles and δ, the 10% floor on mass ratios and the M_Z running masses were set by the first agent before any fit, in data_targets.py.
5. **NuFIT variant.** IC19 without SK-atm, normal ordering, as the orchestrator notes specify. In that variant inverted ordering is preferred by Δχ² = 0.6. Normal ordering is used throughout because LNR's spectrum is normal.
6. **Fit scope.** The least-squares survey covers the LNR framework only. The other fermion and scalar assignments, for both groups, are covered by invariant counting, closed-form mass matrices and residual-symmetry fits.
7. **Extra analysis.** PSL(2,7) full and ℤ₂-partial residual patterns were added beyond the plan. Lepton and quark sectors were fitted separately.
8. **Haze sign.** The sign of the haze rotation was chosen to reproduce LNR's θ₁₂ = 32.4°.

## Limitations

- **Tree-level textures only.** There is no renormalization-group running between the flavor scale and M_Z beyond the 10% floor on mass ratios, and no vacuum-alignment dynamics: the alignments are inputs. Only ℤ₃, ℤ₇ and the P manifold are vacua of LNR's familon potential; G is put in by hand.
- **No joint fit.** Leptons and quarks were fitted separately. A joint SU(5) fit (shared φ₁₀ and φ₅) is more restrictive in χ², but it was not run.
- **N_eff is numerical.** It is the Jacobian rank at 4 points. Local multistart optimization can miss a global minimum; the "excluded at dof = 0" verdicts rely on that, and only one class was rechecked with 300 starts.
- **δ convention.** The δ errors are loose, (3σ edge − best fit)/3. The three PSL survivors put δ inside NuFIT's 3σ range but outside its 1σ range, so their status depends on how δ is treated. A precise s₁₂² measurement tests them directly.
- **Look-elsewhere.** Twelve ℤ₂-partial classes, each scanned over 36 row/column permutations, were tested; three pass at p > 0.01.
- **No PSL flavon survey.** No flavon-based texture survey was run for PSL(2,7).
- **Not cross-checked yet.** The independent second computation (`crosscheck/`) has not been done.

## How to reproduce

From `seed/experiments/E4_family_symmetry/`, on one thread (Python 3.13, numpy 2.5.3, scipy 1.18.1, sympy 1.14, numba 0.68, matplotlib 3.11):

```
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 e4_groups.py     > out/groups.log      #   8 s  -> out/groups.json, out/reps.npz (54 checks)
python3 e4_yukawa.py     > out/yukawa.log      #  79 s  -> out/yukawa.json (15 checks)
python3 e4_lnr.py        > out/lnr.log         #   2 s  -> out/lnr.json (14 checks)
python3 e4_fits.py                             # ~9 min total (408 s + 120 s across the restart); resumable,
                                               #   appends to out/fits.jsonl, log in out/fits.log
                                               #   (delete out/fits.jsonl to refit from scratch)
python3 e4_structure.py  > out/structure.log   #   3 s  -> out/structure.json (3 checks)
python3 e4_robustness.py > out/robustness.log  # 182 s  -> out/robustness.json (2 checks)
python3 collect_results.py                     # <1 s   -> results.json
python3 make_figs.py                           #   1 s  -> fig_residual_patterns.png, fig_lnr_alpha.png, fig_texture_survey.png
```

All scripts are deterministic. Fit seeds come from the CRC32 of the class name, and the other seeds are fixed. Each script prints its own PASS/FAIL checks. Literature PDFs (LNR 0706.2341 and 0709.1447, NuFIT 6.0 2410.05380, UTfit 2212.03894, Huang & Zhou 2009.04851) were read from the arXiv mirror and kept outside the repository.
