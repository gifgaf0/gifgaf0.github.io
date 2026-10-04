# Q-A notes (2D instrument cc2d.py, second leg)

All numbers below are copied programmatically from `qa_results.json` (full precision, `repr`).
Units hbar = m = R = 1, mean density 1. Step kernel unless marked g6.

## Method

* **Discretisation.** Plane-wave Galerkin in fractional coordinates of a general 2x2 cell (rows a1, a2). psi is
  stored as coefficients c_G on the inscribed disc |G| < pi N/max|a_i| of the N x N FFT box (made exactly
  invariant under the detected point group). All products (rho = psi^2, (U*rho) psi, the BdG kernels) are formed
  on a 2N x 2N grid, which is alias free for these band limits: the discrete energy is the exact functional of a
  trigonometric polynomial, hence exactly translation invariant (checked: 1.2e-16) and point-group symmetric.
  Interaction via Uhat(|G|) (exact for periodic densities). g6 transform: 2400-node Gauss-Legendre on [0, 2.5]
  (production) checked against a tanh-sinh rule on [0, 3] and against the small-k power series.
* **Ground state.** Never imaginary time / split step. Preconditioned L-BFGS (variable change
  psi = sqrt(rho) T y/||T y||, T = (G^2/2 + sigma)^(-1/2)) only when the seed is far (residual > 1e-3), then
  Newton-Krylov: projected preconditioned CG on the constrained Hessian A = L + 2X restricted to the complement
  of {psi, i psi, d_x psi, d_y psi}, kinetic preconditioner, until ||H psi - mu psi||/||psi|| < 1e-11 (achieved
  1e-14 ... 3e-12). psi is real and strictly positive (minimum at the triangle centres; e.g. g=44: 0.0091).
  Collapse to the uniform state is detected through the modulation (max-min)/(max+min) < 1e-6.
* **a\*.** Bounded Brent on e(a) = E_cell/A at rho = 1 (N_cell = A), xatol = 1e-7 a, inside a bracket found by a
  coarse continuation scan (all scan points checked non-uniform). Cross-checks: 5-point quartic fit
  (h = 2e-3 a), 3-point parabola, and the root of the envelope-theorem derivative
  de/da = -(1/a) sum G^2|c_G|^2 - (1/2a) sum Uhat'(G) G |rho_G|^2 (brentq). Because e(a) is flat at the
  minimum, Brent's answer carries a round-off jitter of a few 1e-8 relative (the root is reproducible to 1e-16
  across N). The reported `astar` is the Brent value (as specified); the root value is in
  `astar_crosscheck.dedA_root`, and every point re-solved at the root is saved as `<name>_aroot`.
* **BdG.** Bloch sector q, orthonormal plane waves exp(i(q+G).r)/sqrt(A) with circular cut |q+G| < Kcut;
  dense L(q) = diag(|q+G|^2/2 - mu) + [Phi_{G-G'}], X(q) = Psi diag(Uhat(|q+K|)) Psi^H with exact convolution
  tables; A = L + 2X = C C^T (Cholesky), K = C^T L C, full eigh; Z = omega |<C^-1 s|w>|^2, s = exp(iqr) psi0.
  Mode identification by polarisation: the mirror R with R q = q (q || a1: y -> -y; 30 deg: the 30-deg line) is
  found automatically; L and A are split into exact even/odd blocks. T = lowest odd mode (zero density
  weight), 2 = lowest even, 1 = upper longitudinal (second even, confirmed as the max-F mode among the next three
  even modes at every q). The unblocked solve is also done: parity of its eigenvectors is +-1 to 1e-15 and the
  odd mode there has |rho_T|/|rho_2| <= 3.5e-9. Displacement projections Px, Py (cosines) are recorded: T is pure
  y-displacement (Px = 0). Gaplessness: omega/q of T, 2, 1 is flat over the four q (see `v_over_q`) while the
  next modes stay at finite frequency (`lowest_gapped_omega_per_q`, >= 6.3 at g=13, vs max omega_1 = 3.38).
  Sum rules over the FULL spectrum: f-sum vs N_cell q^2/2 (analytic), static sum vs chi_static from a separate
  matrix-free FFT-applied A(q) solved by preconditioned CG (different code path, same basis).
  F = omega Z/(N_cell q^2/2); S = (2Z/omega)/sum_all(2Z/omega) (dispatch definition; identical to the SPEC
  definition (2Z/omega)/chi_CG to <= 5e-15, recorded as `S_vs_chi_cg`).
* **Speeds.** q || a1, |q|a/2pi in {0.03, 0.05, 0.075, 0.10}; c = sum omega q / sum q^2. F2, Z21 = Z2/Z1, S2 at 0.05.
  cT_30deg_kf005 = omega_T/|q| at |q|a/2pi = 0.05 along 30 deg to a1.
* **Superfluid fraction.** Primary: linear response f_s = 1 - (2/N_cell)<d_x psi0|L^-1|d_x psi0> (PCG, psi0 projected
  out). Also a finite twist psi = exp(ik.r) phi at fixed cell: complex Newton-Krylov from the LR guess, energies at
  k = (0.02, 0.04, 0.06)|b1|, f(k) = 2(E(k)-E0)/(N_cell k^2) extrapolated to k -> 0 exactly through a polynomial in
  k^2 (3 points). x and y directions both computed (isotropy). A dense plane-wave pseudo-inverse route is a third check.
* **Stability.** min eigenvalue of A(q) on an 8x8 grid of the BZ plus the M and K points (Kcut = 50).

## Production settings

N = 64 (psi disc |G| < pi N/a, about 2773 plane waves; Gmax 125-145), Kcut = 80.0 (849-1009 basis functions at q = 0.05),
ground-state tolerance 1e-11, Brent xatol 1e-7 a, twist k = (0.02, 0.04, 0.06)|b1|, stability grid 8x8 at Kcut 50.
Continuation (step): g = [44.0, 40.0, 36.0, 32.0, 28.0, 25.0, 22.0, 20.0, 18.0, 16.0, 15.0, 14.5, 14.0, 13.75, 13.5, 13.25, 13.0]; each point seeded by the previous converged state (fractional coordinates), first
a* guess by linear extrapolation in g. The g6 point starts from a Gaussian droplet seed.
Ground states: `scratchpad/work/qa_states.npz` (keys `<name>__c/mi/ni/N/cell/astar/psi/mu/E/rho/kind/g`, names
`step_g<g>` for every continuation g, `g6_g35`, and `<name>_aroot`).

## Results (Q-A)

| point | astar | e per particle | mu | contrast | peak density |
|---|---|---|---|---|---|
| 44 | 1.3926604701432632 | 53.82803334215834 | 96.22867891205 | 142730.07575579826 | 11.864132187221296 |
| 28 | 1.4344407460001043 | 37.76752501681813 | 67.29892328493968 | 5335.6131727739585 | 9.330808255407595 |
| 22 | 1.4573382222657398 | 31.266025774896413 | 55.85080498752188 | 1112.1006440658048 | 8.085214059575717 |
| 16 | 1.488195993433918 | 24.249827421221596 | 44.06180013159592 | 142.27457691840598 | 6.268973690252047 |
| 14 | 1.501728235875289 | 21.699429261305276 | 40.16819180510461 | 52.47353454768383 | 5.238394083888996 |
| 13.5 | 1.505636113713476 | 21.032744397607527 | 39.23756609645684 | 37.919937552061 | 4.875979391221013 |
| 13.25 | 1.507729128132037 | 20.693508793109096 | 38.789482753911415 | 31.48042231360819 | 4.662743928503432 |
| 13 | 1.5099592056754438 | 20.34966721107239 | 38.36123226898402 | 25.489377364249446 | 4.416462947569954 |
| 35g6 | 1.4375363197237399 | 46.15696971567819 | 85.12031987626334 | 1021.3845858270981 | 8.747646406609578 |

| point | c2 | cT | c1 | F2 | Z21 | S2 | c2 > cT |
|---|---|---|---|---|---|---|---|
| 44 | 0.5958886255965102 | 8.714840662432088 | 16.105774372101827 | 0.0032459780481869055 | 0.08774413933008127 | 0.7026083483329414 | False |
| 28 | 1.2880195244675108 | 6.660403814583182 | 12.67749996620366 | 0.021468326001725047 | 0.21538142676197036 | 0.6787756184033542 | False |
| 22 | 1.8028151316050003 | 5.8043651397829645 | 11.172446904533974 | 0.051482070039054396 | 0.335689301054332 | 0.6747429043945447 | False |
| 16 | 2.688615944601287 | 4.906417869979765 | 9.408902779193728 | 0.15972380035221942 | 0.6656559574054087 | 0.6992645974113894 | False |
| 14 | 3.1714741032868843 | 4.60488392740682 | 8.65738770247263 | 0.27789046559555847 | 1.0586611144889737 | 0.7428987578053835 | False |
| 13.5 | 3.3152471499511345 | 4.5300825532700335 | 8.422446326119438 | 0.334356054974865 | 1.2948997041704637 | 0.7671383166759972 | False |
| 13.25 | 3.386651802383835 | 4.492747758640106 | 8.287295256049886 | 0.37258560686256326 | 1.4848888199280448 | 0.7846838338295686 | False |
| 13 | 3.4496308456926457 | 4.45536315520834 | 8.130683743886095 | 0.422531301376562 | 1.786256725595615 | 0.8089680572046474 | False |
| 35g6 | 2.176808658849081 | 6.649116872001452 | 13.533101106902558 | 0.04319824279623224 | 0.2808007782623577 | 0.6356917220074685 | False |

| point | f_s (LR, x) | f_s twist x | f_s twist y | cT_30deg_kf005 | fsum_resid_max | static_resid_max |
|---|---|---|---|---|---|---|
| 44 | 0.005539436008009213 | 0.005539435945222045 | 0.005539435972126849 | 8.715568949329636 | 2.051435898361869e-11 | 3.3631787855158604e-15 |
| 28 | 0.03913971506181002 | 0.039139714525484516 | 0.03913971473486053 | 6.660475056983426 | 1.8774244868635332e-11 | 2.891267195567419e-15 |
| 22 | 0.09518823839305457 | 0.09518823672030537 | 0.09518823734774065 | 5.804934993853741 | 5.2653870924998635e-11 | 1.7859331850001767e-15 |
| 16 | 0.2782140224350095 | 0.27821401199723833 | 0.27821401491266007 | 4.910241752994209 | 4.8189310664719936e-11 | 4.8348656047754054e-15 |
| 14 | 0.43612084661859807 | 0.4361207976786413 | 0.4361208037462507 | 4.6131210825651 | 8.693546074860845e-11 | 2.9527812935302555e-15 |
| 13.5 | 0.49717846931087406 | 0.4971783621277477 | 0.49717836981153307 | 4.5406424273227035 | 1.1893899280126485e-10 | 4.713690092734433e-15 |
| 13.25 | 0.5337640299980182 | 0.5337638442239174 | 0.5337638530505682 | 4.504938450706033 | 1.7686022399293634e-10 | 3.751112233538947e-15 |
| 13 | 0.5762926332873413 | 0.5762922448541119 | 0.5762922552096692 | 4.469736983863429 | 1.225397537850006e-10 | 3.244172701705743e-15 |
| 35g6 | 0.09407141363105664 | 0.09407141162707264 | 0.09407141224735527 | 6.643816420804684 | 7.173559270619534e-12 | 3.810582309054398e-15 |

Boolean c2 > cT at any Q-A point: False; max c2/cT over the Q-A points = 0.7742647962736801 (at g = 13).

Per-q omega, Z, F, S (and parity, displacement cosines, omega/q) of T, 2, 1 and the next even/odd modes are in
`points.<g>.per_q_a1`; the 30-degree data in `points.<g>.q30_detail`.

### Existence of the crystal at g = 13

The crystal branch, followed by continuation from g = 44 (steps of 0.25 below g = 14), exists at g = 13 with
a* = 1.5099592056754438, contrast 25.489377364249446, and is a local minimum: A(q) > 0 on the whole BZ grid (min eigenvalue 0.6367246454640854 at the
smallest grid q; 4.901046726957551 at M, 3.5708794361022678 at K), e''(a) = 30.665416462838635 > 0, and the BdG spectrum is real at all q computed.
No collapse to the uniform state occurred anywhere on the path. Note: at fixed density the crystal energy per
particle stays BELOW the uniform value pi g/2 at every computed g (e_c - pi g/2 = -0.07068503726126707 at g = 13,
-0.11954253692328365 at g = 13.25, -0.17300601412357608 at g = 13.5, -0.29171931382327543 at g = 14), so the fixed-density energy crossing (if it is reached before
the fold) and the branch end both lie below g = 13; both are left to the melting continuation. Below g ~ 14.737 the
uniform state is also locally stable (two competing local minima).

## Checks (selftests, `qa_results.json["selftests"]`)

* Kernels: step Uhat(0)/(pi g) = 1.0; g6 Uhat(0)/g = 2.805377873352097 vs 2 pi Gamma(1/3)/6 = 2.8053778733521546;
  g6 quadratures (k in [0, 400], 4001 values): max|GL - tanh-sinh|/Uhat(0) = 2.0841226808666025e-14, GL vs series (k <= 6) 2.142014977557341e-14;
  on the k values actually used at the g6 point: padded box 2.0841226808666025e-14, BdG K set 2.0262303841758635e-14.
  Step uniform roton instability: g_inst = 14.737096188571947 at k = 4.77900846850157.
* Uniform state (step g = 10): E/A rel. error 1.1308638867425837e-16, mu rel. error 0.0; Bogoliubov omega rel. error 4.307203352477748e-14, F = 0.9999999999999141,
  other modes F = 0.0, chi rel. error 1.9576667791684064e-16. (g6, g = 5: omega rel. error 3.0257871024135715e-15, F = 1.000000000000006.)
* Crystal g = 22: gradient vs finite difference 1.3997914156029874e-07, Hessian vs finite difference 2.397607591459764e-06 (O(h^2) limited);
  translation invariance 1.235566546910568e-16; mu vs dE/dN (Richardson) 6.704576900637735e-14.
  Gamma sector (Kcut 80): ||L psi0||/||psi0|| = 1.609081061305046e-14, ||A d_x psi0||/||d_x psi0|| = 6.071470163631054e-14, ||A d_y psi0|| rel = 7.186273234394574e-14;
  lowest eigenvalues of L: [1.3189592675820172e-14, 14.762194956334083]; of A: [9.026491975964375e-14, 1.4000818677176046e-13, 17.759002473703312] (one phase zero mode, two translation zero modes).
  q = 0.05 along a1: f-sum residual 9.99115276721857e-11, static residual 2.5974916686149275e-15, unblocked |rho_T|/|rho_2| = 1.3326771638571168e-10.
  Full non-Hermitian 2n x 2n BdG (different algebra) vs Cholesky route, lowest 8: max rel. difference 2.381008507071061e-11.
  f_s: LR x 0.09518823520570774, LR y 0.09518823520570807, twist x 0.09518823354259418 (rel 1.7471839455143328e-08), dense plane-wave route 0.09518823520569519.
  Three gapless branches: omega/q at |q|a/2pi = 0.01, 0.02 is (T, 2, 1) = (5.8123331368977285, 1.8165808340041187, 11.209958252753562), (5.8119959527068294, 1.8160076958196625, 11.208460874648784); next modes at finite omega.
* At every Q-A point: f_s twist vs LR relative difference <= 6.8e-7 (x and y), LR isotropy <= 4e-14, f-sum residual
  <= 1.8e-10, static residual <= 5e-15, A(q) > 0 on the BZ grid, |rho_T|/|rho_2| (unblocked) <= 3.5e-9.

## Convergence (`qa_results.json["convergence"]`)

At step g = 44 (most localised, contrast 1.4e5), step g = 13 (near melting) and g6 g = 35: grid N in
{32, 48, 64, 96} (a* re-optimised for each N; speeds at Kcut 70) and Kcut in {40, 50, 60, 70, 80, 90} at N = 64.
Maximum relative deviation from the finest setting:

| case | quantity set | max rel. deviation (worst quantity) |
|---|---|---|
| step_44 | N 32..96 | 9.29944548231521e-09 (Z21); a* 1.3717277116699049e-09 |
| step_44 | Kcut 40..90 | 5.8422831110006884e-08 (F2); a* - |
| step_13 | N 32..96 | 2.631753645028569e-07 (F2); a* 3.4864245586655055e-08 |
| step_13 | Kcut 40..90 | 5.601079404693633e-10 (cT_30); a* - |
| g6_35 | N 32..96 | 1.0781922953615778e-08 (Z21); a* 3.1762512170063504e-09 |
| g6_35 | Kcut 40..90 | 1.1600362093141419e-09 (F2); a* - |

The envelope-derivative root of a* is identical across N to <= 2e-16 relative (e.g. g = 13: 1.509959244362702 for every N).
All the residual N-dependence (<= 2.7e-7, in F2 at g = 13) is the Brent a* jitter (3.5e-8) propagated, not
discretisation error. Everything reported is stable to well below 1e-5 relative, a* to below 1e-7.

## Ambiguities and choices

* Primary a* = Brent (as specified); the more precise envelope-root a* differs by <= 3.5e-8 relative; the
  reported BdG/f_s numbers are evaluated at the Brent a* (differences at the root are below 3e-7 relative).
  States at the root are saved for strain finite differences (de/da there ~1e-14).
* S uses the dispatch definition (spectral sum); the SPEC definition with chi_CG agrees to 5e-15.
* "c2 > cT": evaluated with the LSQ speeds along a1; never true at the Q-A points (max c2/cT = 0.774 at g = 13).
* The orchestrator's build prompt (not the dispatch, and not the SPEC) described the crystal below g ~ 14.737 as a
  metastable branch; at fixed density 1 the computed
  crystal energy is lower than the uniform one down to g = 13 (see above), so here it is the uniform state that
  is metastable between g = 13 and 14.737 (both are local minima). Flagged, no change of method.
* Mirror-line degeneracies: none encountered (T, 2, 1 are well separated); the parity-block solve makes the labels
  independent of accidental crossings anyway.

## Files

* `cc2d.py` - library + CLI (`python3 cc2d.py selftest | qa | conv | aroot | collect | point --g G --a A`).
  API documented at the top of the file (strain use: general cell + fixed mask + seed; melting use: find_astar,
  speeds, superfluid_fraction, bdg (reports `unstable` when A(q) is not positive), stability_scan).
* `qa_results.json` - settings, selftests, convergence, points (keys 44, 28, 22, 16, 14, 13.5, 13.25, 13, 35g6),
  summary, intermediate continuation points, envelope-root states.
* `scratchpad/work/qa_states.npz` - converged ground states for seeding.
