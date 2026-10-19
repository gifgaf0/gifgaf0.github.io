#!/usr/bin/env python3
"""Cross-check E8: tests of the independent 3D tools (xc_lib3d.py).
Writes xc_tests3d.json.  Deterministic.  ~5 min on 2 threads."""
import json, os, time
import numpy as np
import xc_lib3d as X
import xc_axial_spectral as A

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}

# 1. reference energy of an analytic axial field (W = Z1/Z0, Gaussian profile
#    f = pi exp(-(r/s)^2), s = 1.5) from the spectral axial quadrature
def gauss_psi(rho, z, s=1.5):
    r = np.sqrt(rho ** 2 + z ** 2)
    f = np.pi * np.exp(-(r / s) ** 2)
    sfr = np.where(r > 0, np.sin(f) / np.where(r > 0, r, 1), 0.0)
    W = rho * sfr / (np.cos(f) + 1j * z * sfr)
    aW = np.abs(W) ** 2
    return np.stack([2 * W.real / (1 + aW), 2 * W.imag / (1 + aW), (1 - aW) / (1 + aW)], -1)

ref = {}
for N in (64, 96, 128):
    G = A.Geometry('inf', N, N, L=1.5)
    u = A.set_boundary(gauss_psi(G.node_rho, G.node_z), G)
    ref[N] = A.energy_grad(G, u, 1, parts=True)
print('reference (spectral axial quadrature):', ref, flush=True)
Eref = ref[128][0]
out['reference_energy_gauss_s1.5'] = {str(k): v for k, v in ref.items()}

def gauss_field(N, L=7.5, s=1.5):
    x = np.linspace(-L, L, N)
    Xg, Yg, Zg = np.meshgrid(x, x, x, indexing='ij')
    r = np.sqrt(Xg ** 2 + Yg ** 2 + Zg ** 2)
    f = np.pi * np.exp(-(r / s) ** 2)
    sfr = np.where(r > 0, np.sin(f) / np.where(r > 0, r, 1), 0.0)
    W = (Xg + 1j * Yg) * sfr / (np.cos(f) + 1j * Zg * sfr)
    aW = np.abs(W) ** 2
    return np.stack([2 * W.real / (1 + aW), 2 * W.imag / (1 + aW), (1 - aW) / (1 + aW)], -1)

rows = []
for N in (61, 76, 101, 121, 151, 201):
    h = 15.0 / (N - 1)
    phi = gauss_field(N)
    t = time.time()
    el = X.energy_lp(phi, h)[0]; e2 = X.energy_c2(phi, h)[0]; e4 = X.energy_c4(phi, h)[0]
    rows.append(dict(N=N, h=h, E_lp=el, E_c2=e2, E_c4=e4,
                     rel_lp=el / Eref - 1, rel_c2=e2 / Eref - 1, rel_c4=e4 / Eref - 1))
    print(rows[-1], f'{time.time()-t:.1f}s', flush=True)
out['lattice_vs_reference'] = rows

# 2. gradient check of the 4th-order energy
rng = np.random.default_rng(0)
N = 21; h = 0.4
phi = gauss_field(N, L=4.0)
phi[1:-1, 1:-1, 1:-1] += 0.05 * rng.standard_normal(phi[1:-1, 1:-1, 1:-1].shape)
phi /= np.linalg.norm(phi, axis=-1, keepdims=True)
c4 = X.C4Energy(N)
E, _, _, g = c4(phi, h); g = g.copy()
errs = []
for _ in range(8):
    i, j, k = rng.integers(2, N - 2, 3); c = rng.integers(0, 3)
    e = 1e-4; pp = phi.copy(); pm = phi.copy(); pp[i, j, k, c] += e; pm[i, j, k, c] -= e
    fd = (X.energy_c4(pp, h)[0] - X.energy_c4(pm, h)[0]) / (2 * e)
    errs.append(abs(fd - g[i, j, k, c]) / abs(fd))
out['c4_gradient_max_rel_err'] = max(errs)
print('c4 gradient check', max(errs), 'energy consistency', E, X.energy_c4(phi, h)[0], flush=True)

# 3. Hopf charge (free-space Whitehead) of rational-map fields
maps = {1: (lambda a, b: a, lambda a, b: b), 2: (lambda a, b: a ** 2, lambda a, b: b),
        4: (lambda a, b: a ** 2, lambda a, b: b ** 2),
        7: (lambda a, b: a ** 2 * b, lambda a, b: a ** 3 + b ** 2)}
hq = {}
for N in (76, 101, 151):
    for q, (nu, de) in maps.items():
        phi = X.rational_map_field(N, 7.5, nu, de, offset=(0.05, 0.03, 0.02))
        t = time.time()
        Q = X.hopf_whitehead(phi, 15.0 / (N - 1))
        hq[f'Q{q}_N{N}'] = Q
        print(f'Hopf Q{q} N{N}: {Q:.5f} ({time.time()-t:.1f}s)', flush=True)
out['hopf_rational_maps'] = hq

# 4. curves of the trefoil rational-map field
N = 101; h = 0.15
phi = X.rational_map_field(N, 7.5, maps[7][0], maps[7][1], offset=(0.05, 0.03, 0.02))
pos, pr1 = X.preimage_curves(phi, h, 7.5, [0, 0, -1])
oth, pr2 = X.preimage_curves(phi, h, 7.5, [np.sin(2.0), 0, np.cos(2.0)])
rng = np.random.default_rng(3)
alex = []
for P in pos:
    for _ in range(3):
        pol, det, nc = X.alexander(P, X.random_rotation(rng))
        alex.append((str(pol), det, nc))
lk = sum(X.linking_number(P, Qc) for P in pos for Qc in oth)
out['trefoil_initial'] = dict(n_position=len(pos), n_other=len(oth), problems=[pr1, pr2],
                              alexander=alex, linking=lk)
print(out['trefoil_initial'], flush=True)
# unknot / Hopf link sanity checks on parametric curves
s = np.linspace(0, 2 * np.pi, 400, endpoint=False)
tre = np.stack([np.sin(s) + 2 * np.sin(2 * s), np.cos(s) - 2 * np.cos(2 * s), -np.sin(3 * s)], -1)
f8 = np.stack([(2 + np.cos(2 * s)) * np.cos(3 * s), (2 + np.cos(2 * s)) * np.sin(3 * s), np.sin(4 * s)], -1)
c1 = np.stack([np.cos(s), np.sin(s), 0 * s], -1); c2 = np.stack([1 + np.cos(s), 0 * s, np.sin(s)], -1)
R = X.random_rotation(np.random.default_rng(5))
out['parametric'] = dict(trefoil=str(X.alexander(tre, R)[:2]), figure8=str(X.alexander(f8, R)[:2]),
                         unknot=str(X.alexander(c1, R)[:2]), hopf_link=X.linking_number(c1, c2))
print(out['parametric'], flush=True)
json.dump(out, open(os.path.join(HERE, 'xc_tests3d.json'), 'w'), indent=1, default=str)
