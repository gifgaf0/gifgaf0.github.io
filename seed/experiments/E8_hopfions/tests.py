"""
tests.py -- self-checks of the E8 tools (run before trusting any relaxation).

1. exact discrete gradient vs finite differences of the discrete energy;
2. continuum limit of the lattice energy on a smooth analytic field (O(h^2));
3. Hopf charge normalisation and sign on rational-map fields of known charge
   (A11 -> 1, A21 -> 2, A12 -> 2, A22 -> 4, A31 -> 3, K32 Q=5,6,7);
4. curve extraction + knot invariants on analytic curves (unknot, trefoil, Hopf link)
   and on the rational-map trefoil field;
5. timing of one energy+gradient evaluation.
Usage: NUMBA_NUM_THREADS=2 python3 tests.py
"""
import time
import json
import numpy as np
import fs_lib as fs

rng = np.random.default_rng(12345)
out = {}

# ---------------------------------------------------------------- 1. gradient
N = 14
x = np.linspace(-1, 1, N)
h = x[1] - x[0]
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
v = np.stack([np.sin(2 * X + Y), np.cos(3 * Y - Z) + 0.3, np.sin(Z * X) + 0.5 + 0.2 * rng.normal(size=X.shape)], -1)
phi = v / np.linalg.norm(v, axis=-1, keepdims=True)
g = np.zeros_like(phi)
e2, e4 = fs.energy_grad(phi, h, g, True)
d = rng.normal(size=phi.shape)
eps = 1e-6
ep = sum(fs.energy_grad(phi + eps * d, h, np.zeros_like(phi), False))
em = sum(fs.energy_grad(phi - eps * d, h, np.zeros_like(phi), False))
fd = (ep - em) / (2 * eps)
an = float((g * d).sum())
out['grad_check_rel_err'] = abs(fd - an) / abs(an)
print(f"[1] gradient check: analytic {an:.10e}  finite-diff {fd:.10e}  rel err {out['grad_check_rel_err']:.2e}")
assert out['grad_check_rel_err'] < 1e-6

# ---------------------------------------------------------------- 2. continuum limit
# smooth compactly-varying field: phi = stereo(W) with W = (x1 + i x2) * exp(-r^2) * 1.5 (Q=0, smooth)
# exact energy by high-order quadrature on a fine grid with spectral-accuracy derivatives is not
# needed: check that lattice energies converge as h^2 (Richardson).
def smooth_field(N, L=4.0):
    x = np.linspace(-L, L, N)
    h = x[1] - x[0]
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    W = 1.5 * (X + 1j * Y + 0.5 * Z) * np.exp(-(X ** 2 + Y ** 2 + Z ** 2) / 2)
    return fs.stereo_to_phi(W), h

Es = []
for Nn in (41, 81, 161):
    p, hh = smooth_field(Nn)
    gg = np.zeros_like(p)
    a, b = fs.energy_grad(p, hh, gg, False)
    Es.append((hh, a, b))
    print(f"[2] smooth field h={hh:.4f}: E2/C0-units = {a:.6f}  E4 = {b:.6f}")
r2 = (Es[0][1] - Es[1][1]) / (Es[1][1] - Es[2][1])
r4 = (Es[0][2] - Es[1][2]) / (Es[1][2] - Es[2][2])
out['continuum_ratio_E2'] = r2
out['continuum_ratio_E4'] = r4
print(f"[2] successive-difference ratios (4 = second order): E2 {r2:.3f}, E4 {r4:.3f}")

# ---------------------------------------------------------------- 3. Hopf charge
qres = {}
for name in ['A11', 'A21', 'A12', 'A31', 'A22', 'K32_Q5', 'K32_Q6', 'L22_Q6', 'K32_Q7']:
    Qexp, fun = fs.MAPS[name]
    for Nn in (101, 151):
        p, hh = fs.rational_map_field(Nn, fun, Lf=7.5)
        t0 = time.time()
        Q, nhh, _ = fs.hopf_charge(p, hh)
        qres[f'{name}_N{Nn}'] = dict(Q_expected=Qexp, Q=Q, hedgehog_cells=nhh)
        print(f"[3] {name:7s} N={Nn}: Q = {Q:+.4f} (expected {Qexp}), hedgehog cells {nhh}, {time.time()-t0:.1f}s")
out['hopf_rational_maps'] = qres

# ---------------------------------------------------------------- 4. knots
s = np.linspace(0, 2 * np.pi, 400, endpoint=False)
tref = np.stack([np.sin(s) + 2 * np.sin(2 * s), np.cos(s) - 2 * np.cos(2 * s), -np.sin(3 * s)], -1)
unk = np.stack([np.cos(s), np.sin(s), 0.3 * np.sin(2 * s)], -1)
fig8 = np.stack([(2 + np.cos(2 * s)) * np.cos(3 * s), (2 + np.cos(2 * s)) * np.sin(3 * s), np.sin(4 * s)], -1)
A_tref, nt = fs.alexander_polynomial(tref)
A_unk, nu = fs.alexander_polynomial(unk)
A_f8, nf = fs.alexander_polynomial(fig8)
print(f"[4] Alexander: parametric trefoil {A_tref} ({nt} crossings), unknot {A_unk} ({nu}), figure-8 {A_f8} ({nf})")
c1 = np.stack([np.cos(s), np.sin(s), 0 * s], -1)
c2 = np.stack([1 + np.cos(s), 0 * s, np.sin(s)], -1)
Lk, wr, _ = fs.linking_matrix([c1, c2])
print(f"[4] Hopf link linking number {Lk[0,1]:+.1f}")
out['alexander_parametric_trefoil'] = str(A_tref)
out['alexander_unknot'] = str(A_unk)
out['alexander_fig8'] = str(A_f8)
out['hopf_link_lk'] = Lk[0, 1]

for name in ['A11', 'A21', 'K32_Q7', 'L22_Q6']:
    Qexp, fun = fs.MAPS[name]
    p, hh = fs.rational_map_field(101, fun, Lf=7.5, offset=(0.031, 0.017, 0.023))
    loops, info = fs.preimage_curves(p, hh)
    mu = 0.1
    tgt = (np.sqrt(2 * mu - mu ** 2), 0.0, -1 + mu)
    lloops, linfo = fs.preimage_curves(p, hh, target=tgt)
    Lk, wr, _ = fs.linking_matrix(loops + lloops)
    npos = len(loops)
    qlink = Lk[:npos, npos:].sum()
    alex = [str(fs.alexander_polynomial(l)[0]) for l in loops]
    print(f"[4] IC {name}: position comps {npos} (info {info}), linking comps {len(lloops)}, "
          f"lk(position, linking) total = {qlink:+.1f}, pos-pos lk {Lk[:npos,:npos].tolist()}, Alexander {alex}")
    out[f'ic_curves_{name}'] = dict(n_position=npos, n_linking=len(lloops), lk_total=qlink, alexander=alex, info=info)

# ---------------------------------------------------------------- 5. timing
for Nn in (76, 101, 151):
    p, hh = fs.rational_map_field(Nn, fs.MAPS['A11'][1], Lf=4.0)
    gg = np.zeros_like(p)
    fs.energy_grad(p, hh, gg, True)
    t0 = time.time()
    for _ in range(3):
        a, b = fs.energy_grad(p, hh, gg, True)
    dtm = (time.time() - t0) / 3
    out[f'time_energy_grad_N{Nn}_s'] = dtm
    print(f"[5] N={Nn}: energy+grad {dtm:.3f} s;  A11 ansatz (Lf=4) E = {fs.C0*(a+b):.4f}")

json.dump(out, open('tests_output.json', 'w'), indent=1, default=float)
print("tests written to tests_output.json")
