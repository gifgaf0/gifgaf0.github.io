"""
check_ansatz_energy.py -- independent check of the energy normalisation and of the lattice
discretisation.  The energy of the axially symmetric rational-map field W = Z1/Z0 is computed
(a) by Gauss-Legendre quadrature of the continuum energy density with exact (symbolic)
derivatives in spherical coordinates, (b) on the lattice at several spacings, for
  1. the linear profile f = pi (Lf - r)/Lf, Lf = 4 (kink at r = Lf: first-order lattice error),
  2. the smooth profile f = pi exp(-r^2/w^2), w = 2 (field smooth: second-order lattice error).
Usage: NUMBA_NUM_THREADS=2 python3 check_ansatz_energy.py
"""
import json
import numpy as np
import sympy as sp
import fs_lib as fs

rho, z = sp.symbols('rho z', real=True)
r = sp.sqrt(rho ** 2 + z ** 2)


def density(f):
    s = sp.sin(f) / r
    Z1 = rho * s                      # theta = 0
    Z0r, Z0i = sp.cos(f), z * s
    den = Z0r ** 2 + Z0i ** 2
    Wr = Z1 * Z0r / den
    Wi = -Z1 * Z0i / den
    a = Wr ** 2 + Wi ** 2
    phi = sp.Matrix([2 * Wr / (1 + a), 2 * Wi / (1 + a), (1 - a) / (1 + a)])
    pr = phi.diff(rho)
    pz = phi.diff(z)
    pt = sp.Matrix([-phi[1], phi[0], 0])   # d_theta phi = e3 x phi (W -> e^{i theta} W)
    c = lambda u, v: u.cross(v).dot(u.cross(v))
    d = (pr.dot(pr) + pz.dot(pz) + pt.dot(pt) / rho ** 2 + c(pr, pz) + (c(pr, pt) + c(pz, pt)) / rho ** 2)
    return sp.lambdify((rho, z), d, 'numpy')


def quad(fd, Rmax, n):
    xr, wr = np.polynomial.legendre.leggauss(n)
    xt, wt = np.polynomial.legendre.leggauss(n)
    R = 0.5 * Rmax * (xr + 1); wR = 0.5 * Rmax * wr
    T = 0.5 * np.pi * (xt + 1); wT = 0.5 * np.pi * wt
    RR, TT = np.meshgrid(R, T, indexing='ij')
    val = fd(RR * np.sin(TT), RR * np.cos(TT))
    return float(fs.C0 * 2 * np.pi * np.sum(val * (RR ** 2 * np.sin(TT)) * wR[:, None] * wT[None, :]))


def lattice_field(N, fprof, L=7.5):
    x, h = fs.grid(N, L)
    X1, X2, X3 = np.meshgrid(x, x, x, indexing='ij')
    rr = np.sqrt(X1 ** 2 + X2 ** 2 + X3 ** 2)
    ff, sf = fprof(rr)
    Z1 = (X1 + 1j * X2) * sf
    Z0 = np.cos(ff) + 1j * X3 * sf
    pq = Z1 * np.conj(Z0); pp = np.abs(Z1) ** 2; qq = np.abs(Z0) ** 2
    p = np.stack([2 * pq.real, 2 * pq.imag, qq - pp], -1) / (pp + qq)[..., None]
    fs.set_boundary(p)
    return p, h


out = {}
cases = {
    'linear_Lf4': (sp.pi * (4 - r) / 4, 4.0,
                   lambda rr: (np.where(rr < 4, np.pi * (4 - rr) / 4, 0.0),
                               np.where(rr < 4, np.sin(np.pi * (4 - rr) / 4) / np.where(rr > 0, rr, 1), 0.0)
                               + np.where(rr == 0, np.pi / 4, 0.0))),
    'gauss_w2': (sp.pi * sp.exp(-r ** 2 / 4), 7.5,
                 lambda rr: (np.pi * np.exp(-rr ** 2 / 4),
                             np.where(rr > 0, np.sin(np.pi * np.exp(-rr ** 2 / 4)) / np.where(rr > 0, rr, 1), 0.0))),
}
for name, (fexpr, Rmax, fprof) in cases.items():
    fd = density(fexpr)
    Eq = [quad(fd, Rmax, n) for n in (60, 120, 240)]
    print(f'[{name}] continuum quadrature: {Eq}')
    lat = []
    for N in (76, 101, 151, 201):
        p, h = lattice_field(N, fprof)
        e2, e4 = fs.energy_grad(p, h, np.zeros_like(p), False)
        E = fs.C0 * (e2 + e4)
        lat.append((h, E, E / Eq[-1] - 1))
        print(f'[{name}] lattice h={h:.4f}: E = {E:.6f}  rel. dev {E/Eq[-1]-1:+.4%}')
    out[name] = dict(E_quadrature=Eq, lattice=lat)
json.dump(out, open('check_ansatz_energy.json', 'w'), indent=1)
