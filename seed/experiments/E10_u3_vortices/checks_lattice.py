"""
E10 B2/B3 instrument checks for the 2D lattice (u3lattice.py):
  1. analytic gradient vs 5-point finite differences (static T, and full B3 functional with inner CG solve);
  2. gauge invariance of T and I under a smooth local U(3) transformation;
  3. global SU(3)_{C+F} invariance of T (any V) and of I (V commuting with G).
Run: python3 checks_lattice.py > log_checks_lattice.txt
"""
import numpy as np, json, scipy.linalg as sl
from u3common import herm, herm_params, dag, G_DIAG, EB
from u3lattice import Lattice2D, OPTS2D

rng = np.random.default_rng(0)
L, h, lam = 12, 0.5, 1.0
Lt = Lattice2D(lam, L=L, h=h)
Lt.Hb = (np.eye(3) + 0.3 * (rng.normal(size=(L, L, 3, 3)) + 1j * rng.normal(size=(L, L, 3, 3)))).astype(complex)
H0 = Lt.Hb.copy()
Wp0 = 0.4 * rng.normal(size=(2, L, L, 9))
v0 = Lt.pack(H0, Wp0)
out = {}

def fd5(f, v, i, eps):
    def E(d):
        vv = v.copy(); vv[i] += d; return f(vv)[0]
    return (-E(2 * eps) + 8 * E(eps) - 8 * E(-eps) + E(-2 * eps)) / (12 * eps)

for name, f in [('static T', Lt.T_fg)] + [('B3 functional k=0.3 q=1.7', None)]:
    if f is None:
        fg, st = Lt.make_fg(0.3, 1.7)
        def f(v, fg=fg, st=st):
            st.pop('w', None)          # cold CG start each call, tol 1e-12
            return fg(v)
    E0, g = f(v0)
    nH = Lt.nH
    act = np.zeros((2, L, L, 9), bool); act[0, :-1] = True; act[1, :, :-1] = True   # links that enter E
    act_idx = nH + np.nonzero(act.ravel())[0]
    idx = np.concatenate([rng.choice(nH // 2, 10, replace=False), nH // 2 + rng.choice(nH // 2, 10, replace=False),
                          rng.choice(act_idx, 20, replace=False)])
    inert = nH + np.nonzero(~act.ravel())[0]
    assert np.all(g[inert] == 0.0)
    worst = 0.0
    for i in idx:
        fd = fd5(f, v0, i, 1e-4)
        worst = max(worst, abs(fd - g[i]) / (abs(fd) + 1e-8))
    print(f'gradient check ({name}), L={L}, h={h}, 40 random coordinates, 5-point FD step 1e-4: worst rel err {worst:.2e}', flush=True)
    out[f'grad_{name}'] = worst

# ---- gauge invariance ----
Hs, Wps = H0, Wp0
U, *_ = Lt.links(Wps)
Ek, Eb, Ev, *_ = Lt.T_parts(Hs, U)
T0 = Ek + Eb + Ev
I0, *_ = Lt.K_solve(Hs, U, tol=1e-14)
th = np.stack([0.7 * np.sin(0.4 * Lt.x + 0.3 * p) * np.cos(0.25 * Lt.y - 0.2 * p) for p in range(9)], -1)
Om = np.array([sl.expm(1j * M) for M in herm(th).reshape(-1, 3, 3)]).reshape(L, L, 3, 3)
H1 = Om @ Hs
U1 = U.copy()
U1[0, :-1] = Om[:-1] @ U[0, :-1] @ dag(Om[1:]); U1[1, :, :-1] = Om[:, :-1] @ U[1, :, :-1] @ dag(Om[:, 1:])
Wp1 = herm_params(np.array([-1j * sl.logm(M) / h for M in U1.reshape(-1, 3, 3)]).reshape(2, L, L, 3, 3))
Wp1 = np.real(Wp1)
U1b, *_ = Lt.links(Wp1)
Ek, Eb, Ev, *_ = Lt.T_parts(H1, U1b)
T1 = Ek + Eb + Ev
I1, *_ = Lt.K_solve(H1, U1b, tol=1e-14)
Ek, Eb, Ev, *_ = Lt.T_parts(H1, U)
print(f'(control: transforming H only changes T to {Ek+Eb+Ev:.6f})')
print(f'gauge invariance (smooth local U(3), |theta| <= 0.7): T {T0:.12f} -> {T1:.12f} (rel {abs(T1-T0)/T0:.1e}); '
      f'I {I0:.12f} -> {I1:.12f} (rel {abs(I1-I0)/I0:.1e}); link round trip max|U - exp(ihW)| {np.max(np.abs(U1b[:, :-1, :-1] - U1[:, :-1, :-1])):.1e}', flush=True)
out['gauge'] = dict(T0=T0, T1=T1, I0=I0, I1=I1)

# ---- global SU(3)_{C+F} ----
A = herm(rng.normal(size=9)); A -= np.trace(A) / 3 * np.eye(3)
V = sl.expm(1j * A)
H2 = V @ Hs @ dag(V); U2 = V @ U @ dag(V)
Ek, Eb, Ev, *_ = Lt.T_parts(H2, U2)
T2 = Ek + Eb + Ev
B = np.zeros((3, 3), complex); B[0, 2] = 0.4 + 0.2j; B[2, 0] = np.conj(B[0, 2]); B[1, 1] = 0.3; B[0, 0] = -0.3
V2 = sl.expm(1j * B)          # commutes with G = diag(0,1,0)
H3 = V2 @ Hs @ dag(V2); U3 = V2 @ U @ dag(V2)
Ek, Eb, Ev, *_ = Lt.T_parts(H3, U3)
I3, *_ = Lt.K_solve(H3, U3, tol=1e-14)
I2, *_ = Lt.K_solve(H2, U2, tol=1e-14)
I2g, *_ = Lt.K_solve(H2, U2, G=V @ G_DIAG @ dag(V), tol=1e-14)
print(f'global SU(3)_C+F (generic V): T {T0:.12f} -> {T2:.12f} (rel {abs(T2-T0)/T0:.1e}); '
      f'I with G rotated too: {I2g:.12f} (rel {abs(I2g-I0)/I0:.1e}); I with G fixed (not a symmetry): {I2:.6f}', flush=True)
print(f'global (V commuting with G): I {I0:.12f} -> {I3:.12f} (rel {abs(I3-I0)/I0:.1e}); T {Ek+Eb+Ev:.12f}', flush=True)
out['global'] = dict(T0=T0, T2=T2, I2g=I2g, I2_Gfixed=I2, I3=I3)
json.dump(out, open('checks_lattice.json', 'w'), indent=1, default=float)
