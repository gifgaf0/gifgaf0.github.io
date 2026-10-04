# XCHECK2D — independent 2D cross-check of this leg's 2D instrument

Files: `xcheck2d.py` (code, written from scratch), `xcheck2d_results.json` (all numbers, full precision, plus the
comparison block), this note. Caches/states: `scratchpad/work/xc2d/` (not part of the deliverable).

Order of work (independence): the code and every own number were produced, and `xcheck2d_results.json` was
saved (snapshot md5 `a5a603d7165f9a044b1911bf94efb2cc`, 2026-10-04T16:14:23Z, kept in the scratch folder),
before any other agent's file in `lbc_bank/second_leg/` was opened. After that only `qa_results.json` was read.
`cc2d.py` was never opened: no difference came anywhere near a threshold, so there was nothing to diagnose in
it. The `cases` block of the results file is byte-identical in content to the pre-comparison snapshot (checked
in code: `own_cases_identical_to_precompare_snapshot = true`).

## Method (what is different from the main instrument)

* Cell: rectangular two-droplet supercell `Lx = a`, `Ly = sqrt(3) a`, droplets at (0,0) and (a/2, sqrt(3)a/2).
  Cartesian plane waves `G = (2 pi m/Lx, 2 pi n/Ly)` with a SQUARE index cut `|m|,|n| <= M` (anisotropic in k,
  as requested). Two resolutions: M = 14 (841 plane waves) and M = 22 (2025 plane waves; BdG matrix 4050 x 4050).
  Primary numbers = M = 22.
* Ground state: Galerkin stationary point in that basis. Density, `U*rho` and `(U*rho) psi` are evaluated on a
  zero-padded Cartesian FFT grid with >= 4M+1 points per axis, so every product is exact (no aliasing) and the
  discrete energy is exactly translation invariant (the Goldstone modes are exactly gapless). Solver: L-BFGS on
  the normalised energy from a two-Gaussian seed (only for fresh seeds), then Newton on the bordered system
  `[GP residual = 0, sum|c|^2 = 1]` with a dense Jacobian in the symmetry-reduced coefficient space (mirrors x, y;
  m+n even), built from exact analytic Jacobian-vector products. Never imaginary time. GP residual ~1e-14.
  A contrast guard re-seeds if a solve falls onto the uniform state.
* a*: scipy Brent (`minimize_scalar`, bracket from a 9-point scan) on `e(a) = E/area` at rho = 1, then refined by
  `brentq` on the analytic Hellmann-Feynman derivative `de/da = -(1/a)[2 e_kin + 1/2 sum_K k U'(k) |rho_K|^2]`
  (exact at fixed normalised coefficients because the constraint `sum c^2 = 1` does not depend on a; step kernel
  `k U'(k) = -2 pi g J2(k)`). The reported a* is the derivative root; the pure-Brent value is also stored
  (`a_brent`, differs by <= 4e-9 relative, the energy-flatness limit). A finite-difference check of de/da is stored.
* gamma6 kernel: primary quadrature Gauss-Legendre 2400 nodes on [0, 2.5]; validated against tanh-sinh, composite
  Gauss-Legendre (260 panels x 20) and QUADPACK on k in [0, 260]: max |diff| = 2.29e-13 Uhat(0) (< 1e-12 required).
  The residual is a uniform 2.3e-13 relative scale error of numpy's 2400-node Legendre weights (Uhat(0) exact
  = 2 pi Gamma(1/3)/6 is reproduced by the three alternative quadratures); it is invisible in every observable
  (it shows up only as a 2.2e-13 relative difference of e* for g6 vs the main instrument).
* BdG: full non-Hermitian REAL eigenproblem `[[L+X, X], [-X, -(L+X)]]` (dgeev) in the supercell basis at Bloch q;
  `L_GG' = 1/2|q+G|^2 delta + Phi_{G-G'} - mu delta`, `X = P diag(Uhat(|q+K|)) P^T` with `P_{G,K} = psi_{G-K}`
  (K summed over the full support |m_K|,|n_K| <= 2M, i.e. no truncation of the intermediate sum). Positive-norm
  modes kept; normalisation `area * sum(|u|^2-|v|^2) = 1` per supercell; eta-orthonormalisation inside
  (near-)degenerate clusters (relative tol 1e-9) so that full-spectrum sums are exact.
  `Z = |area sum_G psi_G (u_G+v_G)|^2` (per supercell = 2 x per primitive cell; confirmed after comparison:
  Z_super / Z_qa = 2.0000000 at every q). F, S, Z ratios and speeds are intensive.
* Zone folding: the supercell spectrum at q contains the primitive sector q (support on m+n even) and the folded
  sector q+M (support on m+n odd); they decouple exactly. Modes are classified by their support fraction. This
  matters: e.g. at g = 44 the lowest folded mode (an M-point phonon, omega = 1.0071) lies BELOW omega_1(q) at
  |q|a/2pi = 0.03 (2.1851); it carries exactly zero density weight and is excluded.
* Labels: among the three lowest primitive-sector modes, along a1 the mirror y -> -y parity is computed from the
  eigenvector (exactly -1 for one mode = T, whose Z <= 3.3e-23 absolute, <= 2.4e-21 of Z_2, i.e. round-off);
  2 / 1 = lower / upper mirror-even mode. Displacement projections confirm: T is polarised along y (direction
  cosine >= 0.9994), 2 and 1 along x (transverse cosine <= 6.5e-9). The 4th
  primitive-sector mode at |q|a/2pi = 0.03 sits 6.9x (g = 13.25) to 21x (g = 44) above omega_1 and does not scale
  with q (gapped); omega/q of T, 2, 1 varies by <= 1.1 % over the four q (gapless). At 30 deg, T = the acoustic
  mode with the smallest Z (Z_T/Z_max <= 2.2e-21; the 30-deg mirror is not a symmetry of the square cut, but the
  breaking is negligible because the coefficients at the cut are <= 1e-12).
* Sum rules: f-sum `sum omega Z / (N q^2/2) - 1` over the FULL spectrum (2025 positive modes) <= 5.3e-11;
  static: `sum 2Z/omega` vs a direct dense solve `2 area c^T A^{-1} c` (A = L + 2X), <= 1.7e-10.
* Gamma sector: |L psi0|, |A d_x psi0|, |A d_y psi0| relative ~1e-17; lowest eigenvalues of L: one zero, of
  A: two zeros (1e-13), as required.
* f_s: finite phase twists only. `psi = e^{ik.r} phi`, phi minimised (real Fourier coefficients by the
  inversion-plus-conjugation symmetry, mirror transverse to k kept) at fixed cell, k in {0.01, 0.02, 0.03, 0.04},
  along x and along y; `f(k) = 2(e(k)-e(0))/k^2`; reported value = quadratic-in-k^2 extrapolation through the
  first three twists, mean of x and y. Diagnostic only (not the reported value): linear response
  `1 - (2/N)<d psi0|L^-1|d psi0>` with the same Galerkin L; twist vs linear response: -5.4e-10 (g = 22),
  +1.3e-10 (g = 13.25). x/y spread at M = 22 is ~1e-8 for g = 22 (round-off in energy differences of ~5e-6 on
  e ~ 31), 2e-10 for g = 13.25.

## Own results (M = 22; full precision; units hbar = m = R = 1, rho_bar = 1)

| quantity | step g=44 | step g=22 | step g=13.25 | g6 g=35 |
|---|---|---|---|---|
| a* | 1.3926604829399245 | 1.4573382531939647 | 1.5077291618363953 | 1.4375363391770095 |
| c2 | 0.5958886312865221 | 1.8028151885913157 | 3.3866520689160837 | 2.176808705025885 |
| cT | 8.714840419849022 | 5.804364892099028 | 4.492747648397131 | 6.649116770694803 |
| c1 | 16.105773876200555 | 11.17244627523787 | 8.2872945409014 | 13.533100713412953 |
| F2 (0.05) | 0.003245978028958736 | 0.05148207014616423 | 0.37258565830640034 | 0.0431982432103191 |
| Z2/Z1 (0.05) | 0.08774413511328606 | 0.33568927208842186 | 1.4848889059074428 | 0.2808007665583592 |
| S2 (0.05) | 0.7026083294933982 | 0.6747428660010414 | 0.7846838143020883 | 0.6356917003239787 |
| cT at 30 deg (0.05) | 8.715568708032544 | 5.8049347478806705 | 4.50493834865872 | 6.643816322164751 |
| f_s (twist) | - | 0.09518823680881244 | 0.5337640313902468 | - |
| max f-sum resid | 5.2964937887026785e-11 | 2.8889524949202105e-11 | 3.479185491980882e-11 | 1.580987427423802e-11 |
| max static resid | 1.6610384025058113e-10 | 1.2718183763289714e-11 | 1.0711069822510528e-11 | 5.000128569070623e-11 |
| e* = eps_c | 53.82803334215831 | 31.266025774896363 | 20.693508793109107 | 46.156969715688206 |
| mu_c | 96.22867925018438 | 55.85080532784256 | 38.789482886215595 | 85.12032008145971 |

c2 < cT at every point (no c2 > cT). Convergence M = 14 vs M = 22: max relative difference over a*, speeds,
F2, Z21, S2, cT30, f_s is 5.2e-9 (g = 44, F2), 2.7e-10 (g = 22), 3.4e-10 (g = 13.25), 4.0e-11 (g6 35); the
coefficient magnitude at the cut is 1e-7 (g = 44, M = 14) down to 1e-18.

## Comparison with qa_results.json (main instrument)

Every overlapping quantity agrees far inside the requested thresholds (0.1 % speeds/a*, 1 % F2/Z21/f_s,
0.005 abs S2). Maximum |relative difference| over the four points:
a* 2.2e-8, c2 7.9e-8, cT 4.3e-8, c1 8.6e-8, cT30 4.2e-8, F2 1.4e-7, Z21 8.6e-8, f_s 1.7e-8; S2 max |abs diff|
3.8e-8. Per-q frequencies along a1 agree to <= 1.1e-7, F2 at every q to <= 1.4e-7. Nothing is flagged.

Diagnosis of the remaining 1e-8..1e-7 differences (no implementation error):
* The main instrument reports a* = its bounded-Brent value with xatol = 1e-7 a. Its own envelope-theorem root
  `astar_crosscheck.dedA_root` equals this code's a* to <= 7e-15 relative (bit-identical for g = 44, 22),
  whereas its reported Brent value sits 9e-9 (g = 44) .. 2.2e-8 (g = 13.25) relative below that root. All its
  observables are evaluated at the Brent a.
* Re-evaluating this code's observables at the main instrument's reported a (post-comparison diagnostic, stored
  under `comparison_with_qa_results.diagnosis_at_qa_reported_a`, M = 14) collapses the differences to:
  speeds <= 1.4e-9, F2 <= 3.1e-9, Z21 <= 1.5e-9, S2 <= 1.2e-10, e <= 2.2e-13, mu <= 2.2e-13, linear-response
  f_s 3.5e-15 (g = 22) and 5.0e-13 (g = 13.25). The residual 1e-9 at g = 44 matches this code's own M = 14
  discretisation error there (5e-9 lo/hi for F2).
* f_s: the main instrument quotes the linear-response value; its own twist values use large twists (0.02..0.06
  of |b1|) and differ from its linear-response value by 1.8e-8 (g = 22) and 3.5e-7 (g = 13.25), compliant
  with the spec's 1e-4 rule; this code's small-twist values agree with linear response to <= 5.4e-10.
* mu differs by 2.4e-9..6.1e-9 relative, again the a-offset (d mu/da ~ 9 at g = 22).

Conclusion: the two implementations (different cell, basis cut, ground-state solver, eigen-algebra and f_s
route) agree to the level set by the main instrument's a* tolerance; at equal a they agree to ~1e-9 or better.
Neither implementation is wrong. Minor remark for the main instrument: quoting a* (and evaluating at) the
de/da root it already computes would remove its ~1e-8 a* offset; this has no effect at the dispatch tolerances.

## Run

```
python3 xcheck2d.py quad
for c in step44 step22 step13.25 g6_35; do for M in 14 22; do python3 xcheck2d.py astar $c $M; done; done
for c in step44 step22 step13.25 g6_35; do for M in 14 22; do python3 xcheck2d.py bdg $c $M; done; done
for c in step22 step13.25; do for M in 14 22; do python3 xcheck2d.py fs $c $M; python3 xcheck2d.py fslr $c $M; done; done
python3 xcheck2d.py collect      # writes xcheck2d_results.json (own numbers)
python3 xcheck2d.py diagqa       # post-comparison diagnostic (reads qa_results.json)
python3 xcheck2d.py compare      # adds the comparison block
```
Timing (2 threads): a* ~15 s per case and resolution; one BdG eig at M = 22 ~22 s; twists ~10 s per case.
