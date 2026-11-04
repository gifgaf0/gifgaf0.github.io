"""
E10 Route B, B4: instrument checks before any loop run (PREREG_B4 §3, task checks 1, 2, 4).  Label: Exploration.
  1. Gradient of E_Q (static + twist + Q^2/4I with the inner CG solve, envelope gradient) against a 5-point FD
     stencil at random coordinates of every block (H re/im, W_rho, W_z, Wt_phi), on random fields, ring mode.
  2. Gauge invariance under a smooth axisymmetric U(3) gauge transformation Omega(rho, z) (random fields):
     E_static, E_twist and I unchanged; control: transforming H alone.
  3'. numba kernels against the numpy reference (same functional).
  4. Vacuum: n = Q = 0, H = 1, W = 0 -> E = 0 (also n = 3, Q = 0, Wt_phi = 0: E = 0).
Run: python3 b4_checks.py > log_b4_checks.txt   (-> b4_checks.json)
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import json
import numpy as np
from scipy.linalg import expm
from b4_axi import Axi, I3
from u3common import herm, herm_params, dag, EB


def rand_fields(A, rng, amp=0.3):
    H = A.Hb.copy()
    Hi = I3 + amp * (rng.normal(size=(A.nHi, 3, 3)) + 1j * rng.normal(size=(A.nHi, 3, 3)))
    H[~A.bd] = Hi
    Wr = amp * rng.normal(size=A.shapes['Wr']); Wz = amp * rng.normal(size=A.shapes['Wz'])
    Pt = amp * rng.normal(size=A.shapes['P'])
    return H, Wr, Wz, Pt


def gradcheck(mode='ring', seed=0, eps=1e-5):
    A = Axi(h=0.5, rho_max=5.0, zhalf=2.5, n=3, Q=7.3, mode=mode, R_L=6.0, cg_tol=1e-14)
    rng = np.random.default_rng(seed)
    v = A.pack(*rand_fields(A, rng))
    E0, g = A.fg(v)
    nH = A.nHi * 9
    blocks = dict(H_re=(0, nH), H_im=(nH, 2 * nH), W_rho=(2 * nH, 2 * nH + int(np.prod(A.shapes['Wr']))))
    o = blocks['W_rho'][1]
    blocks['W_z'] = (o, o + int(np.prod(A.shapes['Wz']))); o = blocks['W_z'][1]
    blocks['Wt_phi'] = (o, v.size)
    rows = []; worst = 0.0
    for name, (a, b) in blocks.items():
        for i in rng.choice(np.arange(a, b), 8, replace=False):
            def E(d):
                vv = v.copy(); vv[i] += d; A.X = None; return A.fg(vv)[0]
            fd = (-E(2 * eps) + 8 * E(eps) - 8 * E(-eps) + E(-2 * eps)) / (12 * eps)
            err = abs(fd - g[i]) / max(abs(fd), 1e-6 * abs(E0))
            worst = max(worst, err); rows.append(dict(block=name, i=int(i), grad=float(g[i]), fd=float(fd), rel_err=float(err)))
    return dict(mode=mode, E=E0, worst_rel_err=worst, rows=rows, lattice=dict(h=A.h, Nr=A.Nr, Nz=A.Nz, n=A.n, Q=A.Q))


def gauge_check(seed=1):
    A = Axi(h=0.25, rho_max=6.0, zhalf=3.0, n=3, Q=5.0, cg_tol=1e-13)
    rng = np.random.default_rng(seed)
    H, Wr, Wz, Pt = rand_fields(A, rng, amp=0.2)
    v = A.pack(H, Wr, Wz, Pt)
    o0 = A.observables(v)
    # smooth Omega(rho, z) = exp(i theta(rho, z)), theta = sum_p c_p(rho, z) E_p with smooth c_p, |theta| <= ~0.7
    c = np.zeros((A.Nr, A.Nz, 9))
    for p in range(9):
        a1, a2, ph = rng.normal(size=3)
        c[..., p] = 0.25 * np.sin(a1 * A.RHO + ph) * np.cos(a2 * A.Z)
    Om = np.array([expm(1j * herm(x)) for x in c.reshape(-1, 9)]).reshape(A.Nr, A.Nz, 3, 3)
    U, _ = A.links(Wr, Wz)
    from b4_axi import log_unitary
    Ur = Om[:-1] @ U[0] @ dag(Om[1:]); Uz = Om[:, :-1] @ U[1] @ dag(Om[:, 1:])
    P = A.Pfull(Pt); P2 = Om @ P @ dag(Om)
    H2 = Om @ H
    A2 = Axi(h=0.25, rho_max=6.0, zhalf=3.0, n=3, Q=5.0, cg_tol=1e-13)
    A2.Hb = H2.copy()                                  # boundary values transformed too (identity of the lattice functional)
    Pt2 = herm_params(P2 - A2.n * A2.G)
    v2 = A2.pack(H2, herm_params(log_unitary(Ur) / A.h), herm_params(log_unitary(Uz) / A.h), Pt2)
    o1 = A2.observables(v2)
    A3 = Axi(h=0.25, rho_max=6.0, zhalf=3.0, n=3, Q=5.0, cg_tol=1e-13); A3.Hb = H2.copy()
    o3 = A3.observables(A3.pack(H2, Wr, Wz, Pt))
    rel = lambda a, b: abs(a / b - 1)
    return dict(max_abs_theta_param=float(np.abs(c).max()),
                E_static=[o0['E_static'], o1['E_static']], E_twist=[o0['E_twist'], o1['E_twist']], I=[o0['I'], o1['I']],
                rel_dE_static=rel(o1['E_static'], o0['E_static']), rel_dE_twist=rel(o1['E_twist'], o0['E_twist']),
                rel_dI=rel(o1['I'], o0['I']),
                control_H_only=dict(E_static=o3['E_static'], E_twist=o3['E_twist'], I=o3['I']))


def vacuum_check():
    out = {}
    for n in (0, 3):
        A = Axi(h=0.25, n=n, Q=0.0)
        v = A.pack(A.Hb.copy(), np.zeros(A.shapes['Wr']), np.zeros(A.shapes['Wz']), np.zeros(A.shapes['P']))
        E, g = A.fg(v)
        out[f'n={n}'] = dict(E=E, max_abs_grad=float(np.abs(g).max()))
    return out


def fast_vs_ref(seed=5):
    """numba kernels (b4_fast) against the numpy reference implementation of the same functional."""
    out = {}
    for fast in (False, True):
        A = Axi(h=0.25, rho_max=10.0, zhalf=5.0, n=3, Q=40.0, cg_tol=1e-13, fast=fast)
        rng = np.random.default_rng(seed)
        v = A.pack(*rand_fields(A, rng, amp=0.2))
        out[fast] = A.fg(v)
    return dict(E_ref=out[False][0], E_fast=out[True][0], rel_dE=abs(out[True][0] / out[False][0] - 1),
                rel_dgrad_max=float(np.abs(out[True][1] - out[False][1]).max() / np.abs(out[False][1]).max()))


if __name__ == '__main__':
    res = dict(gradient_ring=gradcheck('ring'), gradient_flat=gradcheck('flat', seed=3), gauge=gauge_check(),
               vacuum=vacuum_check(), fast_vs_reference=fast_vs_ref())
    print(json.dumps({k: (v if k != 'gradient_ring' and k != 'gradient_flat' else {kk: vv for kk, vv in v.items() if kk != 'rows'}) for k, v in res.items()}, indent=1, default=float))
    for r in res['gradient_ring']['rows']:
        print('ring', r)
    json.dump(res, open('b4_checks.json', 'w'), indent=1, default=float)
