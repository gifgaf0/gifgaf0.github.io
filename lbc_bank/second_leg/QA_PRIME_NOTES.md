# Q-A' notes: static hydrodynamic route, step kernel, g = 22 (second leg)

Code: `cc2d_hydro.py`. Results: `qa_prime_results.json`, with every number written as repr(float). Caches and logs: `WORK/qap_*`
(WORK = the scratchpad `work/` folder). Units: hbar = m = R = 1, mean density rho = 1. Energies and moduli are per unit area.
Run order: `astar N`, `fd N`, `lr N`, `twist 64`, `collect`, `compare`, with N = 32, 48, 64, 80. N = 64 is primary.

## Definitions used (SPEC section 4, which matches dispatch Sec. 3 Q-A')
- e(rho, eps) = E_cell / A_eps. The cell rows a_i go to (I + eps) a_i, and N_cell = rho A_eps, so the density is held
  fixed while the cell is strained. The reference is the relaxed hexagonal cell (a = a*, rho = 1).
- alpha = d2e/drho2 (eps = 0). M = C_xxxx = d2e/deps_xx2. C_xxyy = d2e/deps_xx deps_yy. mu = C_xyxy = (1/4) d2e/ds2,
  with eps_xy = eps_yx = s. gamma = d2e/drho deps_xx.
- rho_n = 1 - f_s, rho_s = f_s. a = rho alpha - 2 gamma + M/rho_n. b = (rho_s/rho_n)(alpha M - gamma^2).
  c_pm^2 = [a pm sqrt(a^2 - 4b)]/2. c_T^2 = mu/rho_n. c_*^2 = rho_s M/(rho rho_n). F_minus = (c_*^2 - c_minus^2)/(c_plus^2 - c_minus^2).
  The static share is (F_minus/c_minus^2)/(F_minus/c_minus^2 + F_plus/c_plus^2).
- The spec and the dispatch agree on all of these definitions. I found no disagreement to flag.

## Method
1. **a\*.** A Gaussian seed gives the crystal ground state. The other states follow by continuation in a (cc2d.ground_state:
   L-BFGS, then Newton-Krylov; no imaginary time and no split step). a* is the root of the analytic Hellmann-Feynman stress
   de/da at fixed rho. The stress is computed with this file's own code: d|G|^2/deps and the kernel derivatives
   V' = -pi g J2/k^2 and V'' = pi g J3/(2k^3), with V(s) = Uhat(sqrt s). The root is found by brentq, then polished with
   secant steps. Two cross-checks: the vertex of a 7-point degree-6 fit of e(a), and cc2d.optimize_a run here.
2. **Finite differences (primary moduli).** Ground states at strained cells and shifted densities use cc2d with the
   reference plane-wave index set fixed. This is the consistent Galerkin derivative: rho_K depends only on the fractional
   coefficients, so the cell enters only through G. The GP residual tolerance is 1e-12. Each energy is evaluated again with
   this file's own plane-wave functional `PW` (its own FFT box P = 4R+2, its own kernel code); the largest difference from
   cc2d's energies is 1.14e-15 relative. Central differences use steps h = 2e-3 and h/2 = 1e-3, followed by Richardson
   (4 D(h/2) - D(h))/3. The mixed derivatives (C_xxyy, gamma) use the 4-point stencil with the same h on both axes.
   Solver convergence: states solved again at tol 1e-9, 1e-10 and 3e-13 change e by at most 1.0e-15 relative, which meets
   the target of 1e-13 or better.
3. **Analytic linear response (independent check of every modulus).** Let x be the coefficient vector, with
   sum x^2 = rho. Then F(x, eps) = sum 1/2 |G_eps|^2 x^2 + 1/2 sum_K Uhat(|K_eps|) rho_K^2, where rho_K does not depend on
   eps. The bordered constrained response gives alpha = 1/(2 x.A^-1 x) and gamma_a = x.A^-1 beta_a / x.A^-1 x. It also gives
   C_ab = d2F_ab|_x - 2 beta_a.A^-1 beta_b + 2 (x.A^-1 beta_a)(x.A^-1 beta_b)/(x.A^-1 x).
   Here A = L + 2X is the dense matrix on the inversion-even real subspace (dimension 1387 at N = 64; lowest eigenvalue
   17.759, so positive definite), and beta_a = (dH/deps_a) psi0. alpha computed this way is the requested A/(dN/dmu),
   with dN/dmu = 2<psi0|A_Gamma^-1|psi0> = 0.0420635272937023 per cell. x.A^-1 x from the dense Cholesky solve equals the
   value from CG with cc2d's matrix-free Hessian to 0 relative difference.
4. **f_s.** The linear-response value is 1 - (2/N)<d_x psi0|L^-1|d_x psi0>, with L dense on the odd real subspace
   (dimension 1386; lowest eigenvalue 14.76). It is computed along x, y and at 30 degrees. The twist value uses
   psi = e^{ik.r} phi, with the lattice fixed and k = 0.02, 0.04, 0.06 |b1| along x and y. Each phi is found by this file's
   own dense Newton. That Newton works in the real-coefficient subspace phi(-r) = phi*(r), which contains no zero modes,
   and solves a bordered normalisation constraint; it converges quadratically to a residual of about 1e-14.
   f_k = 2(E(k)-E(0))/(N k^2) is then extrapolated by a 3-point Richardson polynomial in k^2. The linear-response value is
   primary because it is the exact k -> 0 limit; the twist values and the hydro outputs computed with the twist f_s are
   also stored.
5. **Hydrodynamics.** Evaluated from the formulas above. Independent check: I wrote the linearised Lagrangian
   L = -n phi_t - (rho/2) phi_x^2 + (rho_n/2)(u_t - phi_x)^2 - (alpha/2) n^2 - gamma n u_x - (M/2) u_x^2 with a source V n,
   solved the 3x3 response system numerically, and took F_nu from the pole residues. This reproduces c_pm^2 to 1e-16 and
   F_minus to 8.5e-12 absolute. The residues sum to 1 (f-sum), and the static limit equals M/(alpha M - gamma^2).

## Results (N = 64, primary)
| quantity | value |
|---|---|
| a* (stress root) | 1.4573382531939647 |
| e per area at a* | 31.26602577489632 |
| mu (chemical) at a* | 55.85080532784254 |
| f_s (linear response, x) | 0.09518823686011202 |
| f_s twist, x / y | 0.09518823519828155 / 0.0951882358231422 |
| alpha | 43.726596216764335 |
| M = C_xxxx | 91.64325226773684 |
| C_xxyy | 30.5059772184683 |
| mu = C_xyxy | 30.568637536439642 |
| gamma | 8.017959775526625 |
| a | 128.9750056290254 |
| b | 414.80825903597116 |
| c_minus | 1.8167718025575543 |
| c_plus | 11.210456986512957 |
| c_T | 5.812445879721162 |
| c_*^2 | 9.641076695577466 |
| F_minus | 0.051811930464356795 |
| static share of the lower branch | 0.6753841581964672 |

The linear-response moduli are alpha 43.72659629172488, M 91.64325228736546, C_xxyy 30.505977209973143,
mu 30.56863753869616 and gamma 8.017959767672727.

## Checks (all in `checks` in the JSON)
- **Stress at rho = 1.** The analytic de/deps is 1.3e-14 (xx), 1.4e-14 (yy) and -5.6e-16 (xy). The finite-difference
  stresses after Richardson are -2.3e-10, -1.3e-9 and 1.5e-12.
- **Isotropy.** C_xxxx - C_xxyy = 61.13727504926854 and 2 C_xyxy = 61.137275072879284, a relative residual of -3.9e-10.
  The linear-response residual is 0 to double precision.
  - C_yyyy equals C_xxxx to 2.4e-10.
  - The pure shear (eps_xx = -eps_yy = s) gives the same mu to 1.1e-10.
  - The isotropic dilation equals 2M + 2C_xxyy to 2.5e-10, and equals a*^2 d2e/da2 to 1.5e-10.
- **alpha against A/(dN/dmu).** The relative difference is -1.7e-9. alpha from dmu/drho agrees as well.
- **gamma.** The energy route and the dmu/deps_xx route agree to 1.8e-10. gamma_yy equals gamma_xx and gamma_xy is 0.
- **Finite differences against linear response.** All five moduli agree to 1.7e-9 or better (table `fd_vs_lr_rel`).
  The size of the Richardson correction shows the h^2 error: 1.5e-8 (alpha), -2.8e-6 (M), -1.9e-6 (C_xxyy),
  -3.3e-7 (mu) and 3.4e-5 (gamma).
- **f_s.**
  - Twist against linear response: 1.75e-8 relative (x) and 1.09e-8 (y), against the requirement of 1e-4 or better.
  - x against y: 7e-15.
  - Dense L^-1 against cc2d's projected CG: 1.6e-14.
  - cc2d.superfluid_fraction gives a twist value of 0.09518823520015791, within 2e-11 of mine.
- **Basis convergence (N = 32, 48, 64, 80).**
  - a* agrees to 1.5e-16 and e to 1.6e-15.
  - The finite-difference moduli move by 2e-9 or less (finite-difference noise); the linear-response moduli by 1.2e-14 or less.
  - c_minus, c_plus, c_T, F_minus and the static share move by 5.5e-10 or less.
- **Sum rule.** Sum F/c^2 = M/(rho(alpha M - gamma^2)) = 0.02324224864274319, with 0 residual.
- **Speeds.** c_minus/c_T = 0.3125658010676754, so c_minus > c_T is false.

## Cross-check against Q-A (qa_results.json, point 22), read only after the static numbers above were written
The direct comparison sets the hydro values (q -> 0) against the BdG least-squares slopes over |q|a/2pi in {0.03, 0.05, 0.075, 0.10},
with weights taken at 0.05. Differences are relative, hydro minus BdG:
- c_minus vs c2 (1.8028151316050003): +7.7416e-3
- c_plus vs c1 (11.172446904533974): +3.4021e-3
- c_T vs cT (5.8043651397829645): +1.3922e-3. Against cT at 30 degrees: +1.2939e-3.
- F_minus vs F2 (0.051482070039054396): +6.4073e-3 relative, +3.2986e-4 absolute
- static share vs S2 (0.6747429043945447): +6.4125e-4 absolute
- f_s: -1.6e-8. The BdG point sits at the Brent a, which is 2.1e-8 away from the stress root.

These differences are finite-q dispersion. I extrapolated the BdG per-q values to q -> 0 with a polynomial in q^2
(degree 2 / degree 3, four points). Relative differences, hydro minus the q -> 0 value:
- c_T: -1.7e-8 / -4.3e-8
- c2: -2.0e-7 / +3.2e-8
- c1: +1.2e-7 / -5.7e-8
- F2: +1.8e-6 / +2.5e-8
- S2: +9.7e-8 / +5.6e-8

So the static route and the dynamic BdG route agree in the long-wavelength limit to about 1e-7.

## Observations on cc2d.py (no patch applied)
- **Wrong sign of the twist seed in `cc2d.superfluid_fraction`.** The seed is `c0 - 1j*kap*y` with y = L^-1 d_x psi0.
  With cc2d's kinetic term 1/2|G+k|^2, the first-order minimiser is phi = psi0 + i k L^-1 d_x psi0, so the sign is reversed.
  I checked this numerically at k = 0.02|b1|: the energy at the correctly signed seed is 31.266498975781783, and at the
  cc2d-signed seed it is 31.28443367317353; the converged energy is 31.266496975086646. The bug has no effect on results:
  Newton still converges to the same minimum, and cc2d's twist f_s matches mine to 2e-11. It only costs Newton iterations.
- **Q-A reports the Brent a, not the stress root.** The Q-A summary `astar` (1.4573382222657398) is the bounded-Brent value,
  which the cc2d docstring says carries round-off jitter. The envelope root is 1.4573382531939645, which equals my
  stress root to 1.5e-16. The 2.1e-8 offset is negligible for every output.
- **Things I confirmed correct.** cc2d energies match my own functional to 1.1e-15 or better. dedA_envelope matches my
  Hellmann-Feynman stress, and both give the same root. The Hessian `_Ctx.hess` matches my dense A (the x.A^-1 x values
  are identical). Strained cells keep the reference index set when mask=ref mask is passed, and the point group of a
  strained cell is detected correctly (C2v for eps_xx, C2 for eps_xy).

## Ambiguities and the choices I made
- **Which f_s enters the formulas.** I used the linear-response f_s. Using the twist f_s instead changes every output by
  less than 2e-8 relative; that variant is stored as `hydro_twist_fs`.
- **Strain convention.** Linear strain with e taken per strained area at fixed density. Because the first derivatives
  vanish at rho = 1 (relaxed cell), the second derivatives are the same as with Lagrangian strain.
- **Shear.** mu is defined as (1/4) d2e/ds2 with eps_xy = eps_yx = s, as specified. The pure-shear route gives the same
  value.
