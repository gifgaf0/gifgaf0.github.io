# Step 3 — expectation, written before evaluating any number (2026-10-04 UTC)

Object: the V4.67 loss length l = gamma*M*tau*xi/P (per channel P in {A, J, O}), re-evaluated on the
measured 3D slow branch (c2 ~ 0.062 c_T, f-sum share F2 ~ 0.17 %) instead of the retired fluid branch
(c_s = 0.382 c, single branch, F = 1). xi = l_P (declared), gamma, L_prop, maps and tau taken verbatim
from V4.67; only the branch changes.

Physics I expect to govern it: at fixed knot-substrate vertex V(q), the drag a supersonic
density-coupled source feels from branch nu is (rho F_nu / 4 pi v^2) Int q^3 |V|^2 dq in 3D
(point source) and (rho F_nu / 2 pi v^2) S(M_nu) Int q^2 |V|^2 dq per unit length for a filament,
S(M) = 1/sqrt(1 - 1/M^2) -- proportional to the branch's f-sum share, otherwise independent of its
speed. So:
  l_new / l_old = [S(phi^2)/S(c/c2)] / F2  ~  (1.08/1.00)/0.0017  ~  6e2  ->  +2.8 orders.
Expectation: about 39 orders short (V4.67 headline -42.0 -> about -39.2); same as the author's.
Reading-dependence I expect: (i) taking the closure's M-linear form literally with M = c/c2 adds
about +0.8 order (-> about -38.4); (ii) holding the static core deficit (not the vertex) fixed
converts V = delta-rho/chi_static, and the measured compressibility speed exceeds the declared
c_s, which costs about 2 orders against reading (fixed vertex) (-> about -41). FAIL in every
reading. xi_req drops by roughly F2 (x ~ 1/600) to ~2e4 m: still macroscopic.
