# E4: the order-21 group on three generations

*SEED.md §3 and §7.3; PLAN.md §4 E4. First agent ran the groups, Yukawa, LNR and most of the fits. After a container restart a second agent finished the fits, added an exact structural-rank scan and robustness checks, and wrote this report. An independent cross-check (`crosscheck/`) reproduced every calibration and every texture verdict, and raised one major and six minor issues. A reconciliation pass resolved all seven: it fixed the δ pull, reran the affected scripts, and added a real-coupling variant of the texture survey. The numbers below are the reconciled ones; the "Reconciliation" section at the end lists what changed.*

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
- Residual symmetries ("direct" approach). For every pair (G_ℓ, G_ν) of subgroups with non-degenerate eigenvalues on the 3, the mixing matrix is U = V_ℓ†V_ν. It is fitted to (s₁₂², s₁₃², s₂₃², δ) over all row and column permutations and complex conjugation: 0 parameters, 4 observables. A "pattern" below is a (sector, G_ℓ type, G_ν type, |U|²) combination. The number of distinct |U|² structures up to row and column permutations is quoted separately.
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
- "min" is LNR's leading order: I₃ only in the charged sectors; c₁…₄ = β in M_D. **β and α are complex** here.
- "gen" gives all invariants independent complex couplings.

That makes 2×64 lepton classes, 2×16 quark classes, and LNR's exact point, which has real α (161 in total). This is the survey as preregistered and first run. The original report did not state that α and β were complex. LNR themselves take α = β = −1, real, and neglect "invariants capable of setting their phases" (0706.2341 §3.2).

**Real-coupling variants (added in the reconciliation).** "min-real" and "gen-real" are the same classes with every coupling real (α, β, c_k). The Lagrangian is then CP-conserving, and CP is violated only by vev phases. Quarks have no "min-real" class, because the quark "min" variant has no couplings at all. That adds 64 + 64 lepton and 16 quark classes (144). For any survivor with dof = 1, `e4_realcoupling.py` works out its one prediction. It fixes the other six lepton observables at their central values, solves for the parameters from 300 random starts, and lists the discrete δ branches. It propagates the 1σ errors of r, s₁₂², s₁₃² and s₂₃² into δ, and re-checks N_eff at 30 random points.

Observables:
- Leptons (7): m_e/m_μ, m_μ/m_τ, r = Δm²₃₁/Δm²₂₁ (normal ordering), s₁₂², s₁₃², s₂₃², δ.
- Quarks (8): m_u/m_c, m_c/m_t, m_d/m_s, m_s/m_b, λ, A, ρ̄, η̄.
- Overall mass scales are not fitted.

Data and error conventions (set in `data_targets.py` before any fit; values checked against the source PDFs in this session):
- NuFIT 6.0 (arXiv:2410.05380 Table 1, IC19 without SK-atm, normal ordering): s₁₂² = 0.307, s₂₃² = 0.561, s₁₃² = 0.02195, δ = 177°, r = 33.83 ± 0.92. The angles and δ use one-sided σ = (3σ edge − best fit)/3.
- δ is periodic, so its pull uses the representative δ + 360°k with the smallest |pull|. With σ = 81.7° above and 27° below, the two branches cross at δ = 87.5°, which lies inside NuFIT's excluded window of 62°–96°. (Reconciliation fix. The original wrapped δ into [−3°, 357°), so δ = 0° = 360° got pull −6.56 instead of +2.24, and χ² jumped at 357°.)
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
- The scan covers all 305 classes, the real-coupling variants included; 221 are structurally dead.

**Convergence and robustness.**
- The group theory is exact; the one floating-point comparison (all 64 entries of LNR's A^[8]) agrees to 3×10⁻¹⁶.
- Fit determinism: six classes refitted from scratch are identical in χ², N_eff and verdict (rerun after the δ fix). The δ-fixed refit was itself interrupted and resumed, at class 129.
- Global minimum: the four lepton classes that fail at χ² = 72.49 reach the same value from independently seeded starts. A 300-start rerun of one of them finds a minimum of 72.498, with no lower one; the polished stored value is 72.490.
- All 37 accommodating complex-coupling fits reach χ² ≤ 3.4×10⁻⁸, and all 32 real-coupling ones χ² ≤ 9.3×10⁻⁹.
- The real-coupling survivors' multistart minima are not all global. Polishing from the δ branches lowers two of them, 0.90 → 0.14 and 0.40 → 0.14. The cross-check found 0.021 for (G, P, ℤ₃). A lower χ² only strengthens survival.
- The prescreen (200 random points) and the exact scan agree on all 93 (complex) and 82 (real) prescreen-dead classes.
- The group theory and LNR outputs (e4_groups, e4_lnr) need no rerun: neither depends on the δ convention (e4_lnr compares the haze without δ). e4_yukawa was rerun, and 15/15 checks pass.

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
- The sign of the haze rotation is the one in LNR's printed U₋₁, which reproduces all nine entries of their displayed U_MNSP. It is not a free choice. The other sign gives θ₁₂ = 38.09°.
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

A single 1, 1′ or 1″ vev still gives equal |masses|. Three distinct masses need vevs for at least two of 1, 1′, 1″, or triplet vevs. Any two singlets already split all three masses at generic couplings (200 of 200 random points for each pair, `e4_reconcile_checks.py`), and they break F₂₁ to ℤ₇. **An unbroken F₂₁ cannot make a hierarchy.**

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
- F₂₁ (Dirac neutrinos, and quarks): 10 patterns (5 quark, 5 Dirac-lepton), built from 3 distinct |U|² structures (identity, trimaximal Fourier, ℤ₃–ℤ₃′). All are excluded; the best lepton pattern has χ² = 2459 and the best CKM pattern χ² = 1.08×10⁵ (4 observables, 0 parameters).
- PSL(2,7) (ℤ₇ ×8, ℤ₃ ×28, ℤ₂ ×21, ℤ₄ ×21, ℤ₂×ℤ₂ ×14): 97 full-residual patterns (43 quark, 43 Dirac-lepton, 11 Klein–Majorana), built from 26 distinct |U|² structures. All are excluded. The best lepton pattern is ℤ₃×ℤ₇ with Dirac ν, χ² = 162.1 (s₁₂² = 0.293, s₁₃² = 0.027, s₂₃² = 0.158, δ = 0°). The original report gave χ² = 200; that value came from the δ-wrap error, which gave δ = 0° a pull of −6.56 instead of +2.24. The best Klein–Majorana pattern has χ² = 692. The best CKM pattern has χ² = 7.7×10⁴, with λ = 0.416.
- PSL(2,7) ℤ₂-partial classes (2 parameters, 4 observables, 2 dof): **3 of 12 fit**. Each column below is listed as |U_e·|², then the μ and τ rows in some order.

| G_ℓ | Fixed first column | χ² | p | s₁₂² | s₁₃² | s₂₃² | δ |
|---|---|---|---|---|---|---|---|
| ℤ₇ | (0.664, 0.204, 0.132) | 2.13 | 0.34 | 0.321 | 0.0220 | 0.555 | 253° |
| ℤ₃ (TM1) | (2/3, 1/6, 1/6) | 2.54 | 0.28 | 0.318 | 0.0220 | 0.553 | 284° |
| ℤ₃ (TM2, second column trimaximal) | (1/3, 1/3, 1/3) | 7.63 | 0.022 | 0.341 | 0.0219 | 0.562 | 235° |

  The next class has χ² = 31.5. TM1 and TM2 are patterns of PSL(2,7)'s S₄ subgroups: the ℤ₃ and the column-fixing ℤ₂ generate S₄ (order 24) for TM1 and A₄ ⊂ S₄ (order 12) for TM2. The ℤ₇ class is different. Its ℤ₇ and ℤ₂ generate the whole PSL(2,7) (order 168), so it is not an S₄ pattern; it needs a ℤ₂, which F₂₁ does not have (`e4_reconcile_checks.py`). The δ fix changes no survivor. It lowers the χ² of the excluded (0, ½, ½) classes from 400.75 to 362.80.

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

**6. Texture survey** (fig_texture_survey.png; results.json → `texture_survey_all` and `texture_survey_real_couplings`).

*Complex couplings: the survey as preregistered and first run.* It was rerun from scratch with the corrected δ pull. No verdict changed, and no N_eff changed except the fit-level N_eff of one structurally dead class.

| Sector | Classes | Structurally dead | Fit excluded | Accommodates (N_eff = N_obs) | Survives with dof ≥ 1 |
|---|---|---|---|---|---|
| Leptons | 129 | 90 | 5 | 34 | 0 |
| Quarks | 32 | 29 | 0 | 3 | 0 |

- Before the exact rank scan, 26 dead classes (22 lepton, 4 quark) were labelled "excluded", with χ² from 1.9×10³ to 3.1×10⁶. (The original report said "23, χ² about 5×10³ to 10⁴"; that was a slip.)
  - 19 have a ℤ₇ familon that makes M_e or M_d rank 2. Their best fits show a tiny non-zero lightest mass, which is rounding noise on a singular value that is exactly zero.
  - 4 have exactly degenerate light neutrinos (r = 1).
  - 3 are minimal quark classes whose CKM is a permutation matrix.
- Causes of structural death:
  - φ₅ or φ₁₀ = ℤ₇ makes M_e (or M_d) rank ≤ 2;
  - φ₁ = ℤ₇ makes M_R singular;
  - ℤ₃-symmetric neutrino sectors give r = 1;
  - in the minimal quark variant M_u and M_d are both diagonal, so CKM is a permutation matrix (LNR: "no quark CKM mixing").
- Every class that fits has N_eff = N_obs, with 10 to 30 real parameters, and predicts nothing. Each needs at least one familon with free phases (P) or a generic vev (G). In the minimal variant every fitting class needs a G vev, which is LNR's "Cabibbo haze" put in by hand.
- The five lepton failures:
  - four minimal classes (φ₅ = G, with φ₁₀ and φ₁ each ℤ₃ or P) at χ² = 72.49 with dof = 0, failing on s₂₃² (0.203; pull −8.2);
  - LNR's exact point (N_eff = 3, dof = 4) at χ² = 1472, with θ₁₃ = 0 (pull −38.3).
- **With complex couplings, no alignment class in this framework both fits the data and predicts anything.**

*Real couplings (reconciliation; CP-conserving Lagrangian, CP violated only by vev phases, as in LNR).*

| Sector | Classes | Structurally dead | Fit excluded | Accommodates (N_eff = N_obs) | Survives (dof = 1) |
|---|---|---|---|---|---|
| Leptons (min-real + gen-real) | 128 | 92 | 4 | 29 | 3 |
| Quarks (gen-real) | 16 | 13 | 0 | 3 | 0 |

The three survivors are all min-real with φ₁₀ = G:

| φ₁₀, φ₅, φ₁ | n_par | N_eff | χ²_min (survey multistart) | χ²_min (polished from δ branches) | p | cross-check χ² |
|---|---|---|---|---|---|---|
| G, ℤ₃, P | 8 | 6 | 0.90 | 0.140 | 0.71 | 0.140 |
| G, P, ℤ₃ | 8 | 6 | 0.40 | 0.140 | 0.71 | 0.021 |
| G, P, P | 10 | 6 | 0.021 | 0.021 | 0.89 | 0.140 |

- **Why dof = 1.**
  - In "min", M_e = diag(u₅ᵢu₁₀ᵢ). The two moduli of the G vev fit m_e/m_μ and m_μ/m_τ exactly, and their ordering picks the row permutation of U_ν.
  - The neutrino sector then has 4 effective real parameters (two vev phases, α, β) for 5 observables (r, three angles, δ).
  - N_eff = 6 is the generic rank (maximum over 30 random points; values 5 and 6 occur).
  - With complex α and β the neutrino rank is 5, so the same classes only accommodate (dof = 0). That is the original's result, which the cross-check reproduced.
- **What they predict.**
  - Fix the other six observables at their central values. δ is then left on discrete branches: at least 16–22 per class (300 starts, completed by the exact conjugation symmetry δ → 360° − δ, which is verified on every branch).
  - The union is 25 values spread over the whole circle (15.5° … 344.5°). Each branch has a ±3° to ±16° spread from the 1σ errors of r and the angles.
  - The widest gap, 152.3° to 207.7°, surrounds NuFIT's best fit of 177°. The nearest branches have pulls −1.23σ and +1.61σ with NuFIT's 1σ errors (−0.91 and +0.38 in the 3σ-range convention).
  - Moving s₂₃² within its loose error fills part of the gap: the (G, P, P) minimum sits at δ = 187.9° with s₂₃² = 0.559.
  - The one constraint is real, but at current precision it barely restricts δ.
- **What they need.** Each survivor needs φ₁₀ = G, a generic vev put in by hand (LNR's "haze"), and that vev carries the whole charged-lepton hierarchy. Imposing CP is an assumption beyond F₂₁.
- **gen-real** has no survivor: 22 lepton classes accommodate with N_eff = 7, and 42 are dead. All four real-coupling failures are min-real classes with φ₅ = G and φ₁₀ ∈ {ℤ₃, P}, at χ² = 114–195 and failing on s₂₃² (pulls −9 to −13).
- **With real couplings, three lepton classes fit with one (weak) constraint.**

## What it means for the seed

- **§3 group facts: CONFIRMED.**
  - ⟨D, C⟩ = ℤ₇⋊ℤ₃ has order 21 and lies inside the seed's flipped PSL(2,7) of order 168.
  - The seed's R_f is exactly LNR's generator A^[3], so the seed's copy is the one flavor model-builders use.
  - The triplets are complex (Frobenius–Schur indicator 0, b₇ = (−1+i√7)/2). The uniqueness clause of §3 (classification of simple subgroups of SU(3)) was not tested here.
- **§3, "model-builders have used both groups": CONFIRMED.** The LNR F₂₁ model reproduces exactly. For PSL(2,7), the claim rests on LNR 0709.1447 proposing it as a family symmetry. That is a literature fact, not a computation here.
- **PLAN: an unbroken F₂₁ cannot give a triplet three masses: CONFIRMED.** Masses and a hierarchy require breaking F₂₁ with flavon vevs: at least two of the singlets 1, 1′, 1″, or triplets. The hierarchy then comes from the vevs.
- **PLAN: mixing from misaligned residual subgroups: AMENDED.**
  - It holds for PSL(2,7): three 2-parameter ℤ₂-partial classes fit, and they predict s₁₂² ≈ 0.32–0.34 and δ ≈ 235°–284°. Every full-residual pattern is excluded (best lepton χ² = 162).
  - It fails for F₂₁ alone. Every F₂₁ residual pattern is excluded (best lepton χ² = 2459), and F₂₁ cannot provide a Majorana residual symmetry at all, so F₂₁ models get their mixing from vevs that leave no residual symmetry.
- **PLAN: the LNR example is excluded by data: CONFIRMED** (θ₁₃ at −34σ, r at −7.8σ).
- **§3/§7.3, "F₂₁ acting on three generations does a job": AMENDED.**
  - What F₂₁ does: it restricts the allowed couplings (the tables above, the five-invariant structure, no bare Majorana mass for a triplet ν^c).
  - What it does not do: give masses or a hierarchy without breaking, or predict anything before vevs are chosen.
  - Texture survey, complex couplings (the preregistered survey): of 161 alignment classes in the most developed F₂₁ framework, none fits and predicts.
  - Texture survey, real (CP-conserving) couplings (LNR's own convention): 3 of 144 classes survive formally, with dof = 1, χ²_min = 0.02–0.14 and p = 0.71–0.89. Each needs a hand-put generic φ₁₀ vev for the charged-lepton masses. Its one prediction is weak: δ lies on one of at least 16 discrete branches spread over the whole circle, the nearest to the best fit at 152° and 208°. The verdict word is unchanged, but "none fits and predicts" holds only for complex couplings.
  - The residual-symmetry patterns that do work need ℤ₂ elements of PSL(2,7), which the order-21 group lacks. TM1 and TM2 are S₄ / A₄ patterns, and the ℤ₇ class uses ℤ₇ together with a ℤ₂, which generate all of PSL(2,7).
  - E4 says nothing about why a fold would carry a family index. That link remains an assignment, not a result.

## Deviations from the plan

1. **Interrupted run.** A container restart killed the first agent after 108 of 161 fits. The remaining 53 ran with unchanged code; e4_fits.py resumes from out/fits.jsonl. Determinism was verified by refitting six classes.
2. **Structural scan added after fitting** (e4_structure.py). In the 161-class survey, 26 (22 lepton, 4 quark) fit-"excluded" classes were relabelled "excluded (structural)". (The original report said 23, but the stored results already held 26.) No pass/fail outcome changed, and results.json keeps both labels.
3. **Robustness script added** (e4_robustness.py): the 300-start check and the six determinism refits.
4. **Error conventions not in PLAN.md.** The 3σ-range/3 one-sided σ for angles and δ, the 10% floor on mass ratios and the M_Z running masses were set by the first agent before any fit, in data_targets.py.
5. **NuFIT variant.** IC19 without SK-atm, normal ordering, as the orchestrator notes specify. In that variant inverted ordering is preferred by Δχ² = 0.6. Normal ordering is used throughout because LNR's spectrum is normal.
6. **Fit scope.** The least-squares survey covers the LNR framework only. The other fermion and scalar assignments, for both groups, are covered by invariant counting, closed-form mass matrices and residual-symmetry fits.
7. **Extra analysis.** PSL(2,7) full and ℤ₂-partial residual patterns were added beyond the plan. Lepton and quark sectors were fitted separately.
8. **Haze sign.** The sign of the haze rotation is taken from LNR's printed U₋₁. It reproduces their θ₁₂ = 32.4° and their whole displayed U_MNSP.
9. **Reconciliation: δ pull corrected** (data_targets.py, e4_fits.py). The original wrapped δ into [−3°, 357°). That is inconsistent with NuFIT's asymmetric 3σ range (96°–422°), and it was an error, not a stated convention. The fix is a change of convention after the fits. e4_yukawa.py, e4_fits.py (all 161 classes, from scratch), e4_structure.py and e4_robustness.py were rerun. The pre-reconciliation outputs are kept as out/*_v1_deltawrap.* and out/results_v1_prereconcile.json.
10. **Reconciliation: real-coupling variants added after the cross-check** (min-real, gen-real; 144 classes). They are not in PLAN.md. They were added because the preregistered survey's verdict turned out to depend on whether couplings are complex. Both conventions are reported, and neither is preferred after seeing the result.
11. **Reconciliation: new scripts.** e4_realcoupling.py gives the survivors' predictions. e4_reconcile_checks.py checks the singlet vevs, the pattern counts and the groups generated by the ℤ₂-partial survivors. reconcile_rerun.sh is the rerun driver.

## Limitations

- **Tree-level textures only.** There is no renormalization-group running between the flavor scale and M_Z beyond the 10% floor on mass ratios, and no vacuum-alignment dynamics: the alignments are inputs. Only ℤ₃, ℤ₇ and the P manifold are vacua of LNR's familon potential; G is put in by hand.
- **No joint fit.** Leptons and quarks were fitted separately. A joint SU(5) fit (shared φ₁₀ and φ₅) is more restrictive in χ², but it was not run.
- **N_eff is numerical.** It is the Jacobian rank at 4 points (30 random points for the real-coupling survivors). Local multistart optimization can miss a global minimum. The "excluded at dof = 0" verdicts rely on that, and only one class was rechecked with 300 starts.
- **δ convention.** The δ errors are loose, (3σ edge − best fit)/3. The three PSL survivors put δ inside NuFIT's 3σ range but outside its 1σ range, so their status depends on how δ is treated. A precise s₁₂² measurement tests them directly.
- **Look-elsewhere.** Twelve ℤ₂-partial classes, each scanned over 36 row/column permutations, were tested; three pass at p > 0.01. In the real-coupling survey, 5 non-dead classes had dof ≥ 1, and 3 pass at p > 0.01.
- **Coupling convention.** The texture survey's verdict depends on whether the couplings are complex (generic EFT) or real (CP imposed, CP violated only by vevs). Both are reported. Imposing CP is an extra assumption beyond F₂₁.
- **No PSL flavon survey.** No flavon-based texture survey was run for PSL(2,7).
- **Cross-checked.** The independent second computation (`crosscheck/`) agrees on every calibration and on all 161 texture verdicts. Its issues are resolved in the Reconciliation section below.

## How to reproduce

From `seed/experiments/E4_family_symmetry/`, on one thread (Python 3.13, numpy 2.5.3, scipy 1.18.1, sympy 1.14, numba 0.68, matplotlib 3.11):

```
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 e4_groups.py     > out/groups.log      #   8 s  -> out/groups.json, out/reps.npz (54 checks)
python3 e4_yukawa.py     > out/yukawa.log      #  90 s  -> out/yukawa.json (15 checks)
python3 e4_lnr.py        > out/lnr.log         #   2 s  -> out/lnr.json (14 checks)
python3 e4_fits.py                             # ~27 min (906 s complex + 711 s real-coupling) for 305 classes (161 complex + 144 real-coupling) on a shared core;
                                               #   resumable, appends to out/fits.jsonl, log in out/fits.log
                                               #   (delete out/fits.jsonl to refit from scratch)
python3 e4_structure.py  > out/structure.log   #   5 s  -> out/structure.json (3 checks)
python3 e4_robustness.py > out/robustness.log  # 229 s  -> out/robustness.json (2 checks)
python3 e4_realcoupling.py > out/realcoupling.log      # 268 s -> out/realcoupling.json (4 checks)
python3 e4_reconcile_checks.py > out/reconcile_checks.log  # 5 s -> out/reconcile_checks.json (4 checks)
python3 collect_results.py                     # <1 s   -> results.json
python3 make_figs.py                           #   1 s  -> fig_residual_patterns.png, fig_lnr_alpha.png, fig_texture_survey.png
```

`reconcile_rerun.sh` runs e4_yukawa, e4_fits, e4_structure and e4_robustness in sequence. All scripts are deterministic. Fit seeds come from the CRC32 of the class name, and the other seeds are fixed. Each script prints its own PASS/FAIL checks. Literature PDFs (LNR 0706.2341 and 0709.1447, NuFIT 6.0 2410.05380, UTfit 2212.03894, Huang & Zhou 2009.04851) were read from the arXiv mirror and kept outside the repository.

## Reconciliation

The independent cross-check (`crosscheck/`, verdict "confirmed with corrections") recomputed E4 with separate code and different methods:
- Burnside class-algebra character tables;
- exact monomial invariant counting;
- closed-form LNR α windows;
- an independent texture fitter.

It agreed on all 17 calibrations, every invariant count and mass-matrix form, the LNR numbers, the subgroup counts, the three ℤ₂-partial survivors, and all 161 texture verdicts with their N_eff. It raised one major and six minor issues. A reconciliation pass settled each by reading both codes and, where needed, by an extra computation. All seven are resolved and none is OPEN. Details are in `RECONCILE.md`.

| # | Issue (severity) | Who was right | Action | Effect |
|---|---|---|---|---|
| 1 | The texture-survey headline depends on an unstated choice: complex α, β in "min" (major) | Both computations are correct for their conventions; the original's headline was overstated | State the convention; add min-real and gen-real variants (144 classes) to e4_fits.py; work out the survivors' prediction (e4_realcoupling.py) | "0 predictive survivors" holds for complex couplings only. With real couplings, 3 lepton classes survive at dof = 1 (χ²_min 0.02–0.14, p 0.71–0.89), with a weak δ prediction (≥ 16 branches). The "F₂₁ does a job" verdict stays AMENDED, with revised evidence |
| 2 | δ pull wrapped into [−3°, 357°) (minor) | Cross-check | Pull now uses the representative with the smallest \|pull\|; e4_yukawa, e4_fits (all classes), e4_structure and e4_robustness rerun | PSL best full-residual lepton χ²: 200.0 → 162.1. Excluded (0, ½, ½) ℤ₂-partial classes: 400.75 → 362.80. No verdict changes |
| 3 | "23 relabelled classes, χ² 5×10³–10⁴" (minor) | Cross-check | Count computed in collect_results.py | 26 (22 lepton, 4 quark); 19 ℤ₇ rank, 4 r = 1, 3 permutation CKM; χ² 1.9×10³–3.1×10⁶ |
| 4 | "Three distinct masses need 1+1′+1″" (minor) | Cross-check | e4_reconcile_checks.py (a) | Any two singlet vevs suffice (200/200 points per pair) |
| 5 | "10 / 97 distinct patterns" (minor) | Cross-check (definition) | e4_reconcile_checks.py (b) | 10 / 97 (sector, G_ℓ, G_ν, \|U\|²) combinations; 3 / 26 distinct \|U\|² structures |
| 6 | "Haze sign is an input" (minor) | Cross-check (wording) | Reworded; the code already used LNR's printed U₋₁ | None on numbers |
| 7 | "Patterns that fit come from ℤ₂s shared with S₄" (minor) | Cross-check | e4_reconcile_checks.py (c) | ⟨ℤ₇, ℤ₂⟩ = PSL(2,7) (168); TM1 → S₄ (24); TM2 → A₄ (12). "Shared with S₄" now applies to TM1/TM2 only |

Points checked that needed no change:
- **PMNS convention.** The original is self-consistent: it uses the "barred" convention in both sectors, which gives the complex conjugate of the holomorphic PMNS, and every class is closed under conjugation. The convention slip the cross-check mentions was in its own first pass.
- **The 72.49 minimum.** It stands (300 starts find nothing lower). The cross-check's first-pass 76.31 for one such class was its own optimizer stopping early.

**Final headline after reconciliation.**
- Group theory and LNR calibrations: 17/17 CALIBRATED (unchanged).
- Schur and the absence of a Majorana residual symmetry for F₂₁: unchanged.
- PSL(2,7) ℤ₂-partial survivors: 3 of 12 (χ² 2.13, 2.54, 7.63).
- Full-residual patterns: all excluded (best lepton χ² 162.1 for PSL, 2459 for F₂₁).
- LNR example excluded (−34σ, −7.8σ).
- Texture survey: 0 predictive survivors with complex couplings. With real (CP-conserving) couplings, 3 survivors at dof = 1 whose δ prediction is weak.

All script checks pass: groups 54/54, yukawa 15/15, lnr 14/14, structure 3/3, robustness 2/2, realcoupling 4/4, reconcile_checks 4/4. results.json, this report and the seed-claim verdicts agree.
