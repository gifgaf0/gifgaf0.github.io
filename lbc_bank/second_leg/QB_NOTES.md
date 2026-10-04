# Q-B second leg: 3D AB (hcp-type) supersolid, BdG weights

Instrument: `cc3d.py` (numpy/scipy only). Results: `qb_results.json`. All numbers in the JSON are full precision.
Run order: `python3 cc3d.py lambdac`, then `python3 cc3d.py pipeline --stage {gs,bdg,full,offdiag,smallq,fs,extras}`, then
`python3 cc3d.py assemble`. Each step caches to the scratch folder, so re-running skips finished work.
Threads: OMP/OPENBLAS/MKL = 2.

## Model and constants
- Units hbar = m = R = 1, mean density 1. Uhat(k) = 4 pi (sin k - k cos k)/k^3, with a Taylor series below k = 1.
- Lambda_c = min over Uhat<0 of -k^2/(4 Uhat). Bounded Brent minimisation gives 21.713734623865676. The stationarity
  root 5(sin k - k cos k) = k^2 sin k gives k* = 5.44861331461245 and Lambda_c = 21.713734623865665. The two differ by
  1.07e-14. Lambda = 2 Lambda_c = 43.42746924773133.
- a = 1.3859646002819213 and c = 2.2595969088482843, as given.

## Ground state (no imaginary time, no split-step)
- Discretisation. Galerkin plane waves |G| < Kpsi. The energy and the gradient are evaluated exactly on an FFT grid
  with at least 4h+1 points per axis, where h is the largest Miller index in the sphere, so there is no aliasing. The
  discrete energy is therefore an exact functional of the retained coefficients, and it is invariant under every
  space-group operation and under translations.
- Solver. Preconditioned L-BFGS on E(psi), with psi = sqrt(N) phi/|phi| and the kinetic preconditioner
  (alpha/(alpha+G^2/2))^(1/2). This is followed by a Newton polish: GMRES on the bordered system (H - mu)psi = 0,
  |psi|^2 = N. In the orthorhombic cell the system is also bordered with the 3 translation modes. Final max-norm
  residuals of (H - mu)psi lie between 3e-13 and 1.6e-12 for all sphere runs, and are at most 1.3e-11 for the box
  grids. All are below 1e-10.
- Primitive cell: a1 = (a,0,0), a2 = (a/2, sqrt3 a/2, 0), a3 = (0,0,c). The origin is on the inversion centre, so the
  sites are at +-(1/6,1/6,1/4) and are equivalent to (0,0,0) and (1/3,1/3,1/2). The state is restricted to
  inversion-even functions, which makes all BdG matrices real.
- Orthorhombic cell (a, sqrt3 a, c), with sites exactly as specified: (0,0,0), (1/2,1/2,0), (1/2,1/6,1/2), (0,2/3,1/2).
- Energy per particle at K = 50: 68.34274926596238 (primitive cell) and 68.34274926596235 (orthorhombic cell).
  mu = 117.7995561803753 (primitive) and 117.79955618037529 (orthorhombic). The relative differences are 4e-16 for
  the energy and 1e-16 for mu. They agree at every K tested (30, 40, 50) to below 7e-16.
- An independent pseudo-spectral box-grid solve of the orthorhombic cell (6 odd grids, from 15x25x23 to 35x61x57)
  converges to the same values: energy relative difference -2.7e-10 on 15x25x23, 4e-14 on 19x33x29, and at most 6e-16
  from 23x41x37 upward.
- Kpsi convergence of the primitive energy per particle: K = 30 gives 68.34274982203581, K = 40 gives
  68.342749266054, K = 50 gives 68.34274926596238, K = 60 gives 68.34274926596237. K = 50 is converged to 1e-15.
- The droplets are strongly localised: n_max = 40.19 and n_min about 1.35e-6.
- Starting widths sigma = 0.15, 0.3 and 0.5 lead to the same state, in both cells, at K = 30.

## BdG
- Basis: plane waves e^{i(q+G)r}/sqrt(V) with |q+G| < Kcut, in the primitive cell.
  - L = h - mu, with Phi_hat computed exactly from the band-limited n0.
  - X_GG' = Lambda sum_G'' psi_hat(G-G'') Uhat(|q+G''|) psi_hat(G''-G'), summed over |q+G''| < Kcut+Kpsi, which is
    exact. It is built with blocked dsyrk.
  - A = L + 2X. The reduction is A = CC^T and K = C^T L C, solved with eigh (low subset, or the full spectrum).
  - f+ = sqrt(w) C^-T w_hat, Z = w (t.w_hat)^2 with t = C^-1 s, and chi_static = 2|t|^2 from the direct static solve.
  - F = wZ/(N q^2/2), and S = (2Z/w)/chi_static.
- Checks on the construction:
  - The dense A agrees with an FFT matrix-free A to about 2e-15.
  - Unit test: a uniform state at Lambda = 10 reproduces Bogoliubov frequencies to 1.2e-13, and reproduces Z and chi
    exactly.
  - The symmetry operations leave s = e^{iqr}psi0 invariant to about 1e-15.
  - Gamma sector (K = 40 and 50): L has exactly one zero eigenvalue (the phase mode, -2e-13). Its next eigenvalue is
    0.004729, the bonding/antibonding A/B sublattice splitting; it is not a zero mode. A has exactly three zero
    eigenvalues (about 1e-13; |A d_j psi0|/|d_j psi0| is at most 1.4e-12). All other eigenvalues are at least 8.59.
- Mode identification uses three tests:
  - Little-group parities relative to s. Along x: mirror z and the c-glide normal to y. Along y: mirror x and mirror z.
    Along z: mirror x and the c-glide; the degenerate transverse doublet is rotated to diagonalise mirror x.
  - Displacement cosines between psi0 f+ and e^{iqr} d_j rho0.
  - Gaplessness, w(0.3)/w(0.15) within 5% of 2.

  Every direction has exactly 4 gapless branches: L2 (phase-like), L1, and two transverse branches. Transverse modes
  have Z of about 1e-26 (F of about 1e-24), which is zero by symmetry.
- A gapped low mode at w of about 0.84 is the relative A/B sublattice phase mode. Its w changes by about 1% or less
  between q = 0.15 and 0.3, and it is not acoustic. It sits in the Ty sector along x and along z, and in the L sector along y.
  Along x it has an avoided crossing with the y-polarised transverse acoustic branch near q of about 0.105. That
  crossing is why cT(x, Ty) = w/q rises with q (8.0263 at q = 0.02, 8.0401 at 0.15, 8.0731 at 0.3), while cT(y, Tx)
  falls (8.0260, then 8.0211, then 8.0061). The two agree as q -> 0 (in-plane isotropy). The schema quotes the values
  at q = 0.15, as the dispatch asks.

## Results (consistent Galerkin Kpsi = Kcut = 50, q = 0.15 along x)
| key | value |
|---|---|
| c2 | 0.470555527432646 |
| cT_min | 7.7493459895352235 (q along z, x/y doublet) |
| cT_max | 8.04006531797928 (q along x, y-polarised) |
| c1_basal_q015 | 16.13717890367541 |
| F2_basal_q015 | 0.0016666207042539045 |
| Z21_basal_q015 | 0.05734519151329853 |
| S2_basal_q015 | 0.6629042326549988 |
| c_kappa | 9.38464586499687 (primitive-cell vol 3.758944204413818, chi 0.042680559259732326) |

All transverse speeds at q = 0.15:
- q along x: Tz = 7.759918215513492, Ty = 8.04006531797928.
- q along y: Tz = 7.759913717756439, Tx = 8.02114166784809.
- q along z: Tx = Ty = 7.7493459895352235.

Their mean over the 6 direction/polarisation pairs is 7.846621816361291 (7.84162134568752 at q = 0.3, and
7.842621439822274 from the LSQ slopes). c2 > cT never occurs; c2/cT_min = 0.06072196648182799.

Values at q = 0.3 along x:
- c2 = 0.4690738113072362 and c1 = 16.086149687681637.
- F2_basal_q03 = 0.001657360829173931.
- Z21 = 0.057351301811260434 and S2 = 0.6627861929814147.
- c_kappa = 9.380357231113022.

c_kappa(q -> 0):
- Along x: 9.386022556462432, from a fit of V/chi = a + b q^2 + c q^4 to 7 values of q (K = 40). The two-point
  extrapolation in q^2 from q = 0.15 and 0.3 gives 9.386074974659767.
- Along y the limit is the same: 9.386022606417255.
- Along z it is 9.401121839026473. The static response of a hexagonal crystal depends on direction.

## Convergence (`convergence` block)
- Five consistent cuts were run, K = 30, 35, 40, 45 and 50, giving Nb(x, 0.15) = 1749, 2747, 4031, 5741 and 7885. The
  largest relative deviation from K = 50, over all schema keys, every transverse speed and the q = 0.3 values, is:

  | cut | max relative deviation from K = 50 |
  |---|---|
  | K = 45 | 1.75e-8 |
  | K = 40 | 2.19e-8 |
  | K = 35 | 2.59e-6 |
  | K = 30 | 1.38e-4 |

  So every schema quantity is stable to far better than 2e-4.
- Ground-state resolution against BdG cut (q along x): P60/C50 against P50/C50 differs by at most 1e-8 relative.
- Inconsistent pairs with Kpsi > Kcut (P60 with C30 or C35) converge more slowly. P60/C30 is off by 8e-3 in c2. This
  is why the consistent diagonal is the primary sequence.

## Sum rules (full spectrum, q along x)
| run | Nb | f-sum residual vs N q^2/2 | static spectral sum vs CG |
|---|---|---|---|
| K = 50, q = 0.15 | 7885 | -6.36e-11 | -5.7e-15 |
| K = 40, q = 0.15 | 4031 | 4.97e-11 | 1e-15 |
| K = 40, q = 0.3 | 4035 | 3.14e-11 | -8e-16 |

The CG solve is matrix-free, FFT-applied, preconditioned conjugate gradients, which is a different code path from
the dense Cholesky. The direct and CG values of chi agree to 5e-15.

## Extras (EXTRA keys only)
- Oblique direction, 45 deg in the x-z plane (K = 50, q = 0.15): the pure y-polarised transverse mode has speed
  7.895049207743887 and zero density weight. The three density-carrying acoustic branches have speeds
  0.46530680475513897, 9.147362192336107 (quasi-transverse, Z of 5e-5) and 15.833166750542595.
- Own optimum of the energy per particle at fixed density (Kpsi = 40 search with three quadratic-fit stages; final fit
  residual 1.3e-7): a = 1.3843727138396495 and c = 2.258452154195673, so c/a = 1.6313902546747732. This is a shift of
  -0.115% in a and -0.051% in c from the given point, and the energy gain is 7.2e-6 relative. Outputs there at K = 45:
  - c2 = 0.4698768774466194 and c1 = 16.200363177517808.
  - F2 = 0.0016691565215282075, Z21 = 0.05774092075712291 and S2 = 0.6656312547577686.
  - c_kappa = 9.38323072236285.
  - cT range 7.765436315926895 to 8.069663390186632.
- Linear-response superfluid fraction (Gamma sector, f_s = 1 - (2/N)<d_j psi0|L^-1|d_j psi0>, at K = 50): 0.0030815203840829364
  in the basal plane and 0.003016319145241142 along z. This was not requested; it is given for context only.

## Ambiguities and choices
- cT_min and cT_max are taken over the six direction/polarisation pairs (x, y, z), using w/q at q = 0.15. The z
  doublet counts once per polarisation. The LSQ range is 7.73573449094961 to 8.06649967716988 (extra). The 45-degree
  oblique mode is not included.
- The "mean transverse speed" is the plain arithmetic mean over those 6 pairs. The 7.68 scale was never used to choose
  anything.
- S: the spec divides by the direct chi_static, while the dispatch divides by sum_mu 2Z/w. Given the static sum-rule
  residual of about 1e-15 these are numerically identical. I used the direct chi.
- I used the primitive cell for BdG. c_kappa uses the primitive volume and the primitive-cell chi. The orthorhombic
  cell was used for the ground-state validation only.

## Compliance
- Nothing outside `lbc_bank/second_leg/` in the repo was read.
- No forbidden file names were read, and no git writes were made.
- No code from the dispatch was executed. The pattern check was a separate re-implementation of the stated rule, and
  every file I wrote scans clean.
