#!/usr/bin/env python3
"""E7 part 1b: size-times-mass constant of the Q = 1 Faddeev-Skyrme hopfion (variational estimate).

Physical model (hbar = c = 1), two couplings:
    E = int d^3x [ (kappa2/2) (d_i n)^2 + (kappa4/4) sum_{i,j} (d_i n x d_j n)^2 ],
    kappa2 has dimension mass^2, kappa4 is dimensionless (it multiplies the whole action once the
    length l = sqrt(kappa4/kappa2) is scaled out, so 1/g^2 := kappa4).
With x = l xt this is E = 16 sqrt(2) pi^2 sqrt(kappa2 kappa4) E_W[n], where E_W is the Ward/Sutcliffe
normalised energy (PLAN E8) E_W = (1/(32 sqrt2 pi^2)) int [ (d n)^2 + (1/2) sum_ij (d_i n x d_j n)^2 ] d^3xt.
Hence  M R = 16 sqrt(2) pi^2 kappa4 E_W Rt  =: c0_hopf * kappa4  (R = l Rt).

Ansatz (Q = 1 exactly): n = U e3 U^+ with the degree-1 SU(2) hedgehog U = exp(i f(r) rhat.tau),
i.e. n = rotation by 2 f(r) about rhat applied to e3; f(0) = pi, f(inf) = 0. The Hopf charge of this
map equals deg U = 1. The profile f is optimised freely (spline in t = r/(r+1), 24 nodes) at the
Derrick-optimal scale, so E_ans >= E_true (upper bound); literature E_W(Q=1) = 1.204 (Sutcliffe 2007
lattice) to 1.22.
Outputs hopfion.json.  Runtime ~1-3 min, one core.
"""
import json, os, time
import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))


def build_density():
    f, fp, r, th, ph = sp.symbols('f fp r th ph', real=True)
    rh = sp.Matrix([sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)])
    e3 = sp.Matrix([0, 0, 1])
    n = sp.cos(2 * f) * e3 + (1 - sp.cos(2 * f)) * rh.dot(e3) * rh + sp.sin(2 * f) * rh.cross(e3)
    dr = sp.diff(n, f) * fp
    dth = sp.diff(n, th) / r
    dph = sp.diff(n, ph) / (r * sp.sin(th))
    d2 = dr.dot(dr) + dth.dot(dth) + dph.dot(dph)
    c = lambda a, b: a.cross(b).dot(a.cross(b))
    d4 = c(dr, dth) + c(dr, dph) + c(dth, dph)
    nn = n.dot(n)
    fn = sp.lambdify((f, fp, r, th, ph), [d2, d4, nn], 'numpy')
    return fn


DENS = build_density()

# quadrature grids: r via t in (0,1), r = t/(1-t); theta Gauss-Legendre
NT, NTH = 600, 64
tg, tw = np.polynomial.legendre.leggauss(NT)
tq = 0.5 * (tg + 1); twq = 0.5 * tw
rq = tq / (1 - tq); drdt = 1 / (1 - tq)**2
cg, cw = np.polynomial.legendre.leggauss(NTH)   # cos(theta)
thq = np.arccos(cg)
R, TH = np.meshgrid(rq, thq, indexing='ij')
W = (twq * drdt)[:, None] * cw[None, :] * R**2   # r^2 dr dcos(theta)

KN = 24
tnodes = np.linspace(0, 1, KN + 2)


def profile(vals):
    fv = np.concatenate([[np.pi], vals, [0.0]])
    cs = CubicSpline(tnodes, fv, bc_type='not-a-knot')
    f = cs(tq); dfdt = cs(tq, 1)
    return f, dfdt / drdt, cs


def energies(vals, phi=0.0):
    f, fp, _ = profile(vals)
    F = np.broadcast_to(f[:, None], R.shape); FP = np.broadcast_to(fp[:, None], R.shape)
    d2, d4, nn = DENS(F, FP, R, TH, phi)
    norm = 2 * np.pi / (32 * np.sqrt(2) * np.pi**2)    # azimuthal integral done (density is phi independent)
    E2 = norm * np.sum(W * d2)
    # d4 = sum_{i<j} |d_i n x d_j n|^2 = (1/2) sum_{i,j}, which is exactly the Ward quartic weight
    E4 = norm * np.sum(W * d4)
    return E2, E4, d2, d4, nn


def scaled_energy(vals):
    E2, E4 = energies(vals)[:2]
    return 2 * np.sqrt(E2 * E4)


def main():
    t0 = time.time()
    # initial guess: f = 2 arctan((a/r)^2) style mapped profile
    r_nodes = tnodes[1:-1] / (1 - tnodes[1:-1])
    v0 = np.pi / (1 + r_nodes**2)
    print(f"initial scaled energy {scaled_energy(v0):.5f}", flush=True)
    res = minimize(scaled_energy, v0, method='L-BFGS-B', options=dict(maxiter=3000, ftol=1e-13, gtol=1e-9, maxfun=200000))
    v = res.x
    E2, E4, d2, d4, nn = energies(v)
    lam = np.sqrt(E4 / E2)          # optimal rescaling r -> lam r of the optimised profile
    Emin = 2 * np.sqrt(E2 * E4)
    # phi independence and unit-norm checks
    E2b, E4b = energies(v, phi=0.7)[:2]
    # radii of the rescaled configuration (lengths multiply by lam)
    # rescaled configuration n(r/lam): its quadratic energy is lam*E2, quartic E4/lam, and its energy
    # density at r = lam*r0 is proportional to lam*d2(r0) + d4(r0)/lam
    eps_s = lam * d2 + d4 / lam
    rms_s = np.sqrt(np.sum(W * eps_s * R**2) / np.sum(W * eps_s)) * lam
    _, _, cs = profile(v)
    from scipy.optimize import brentq
    t_ring = brentq(lambda t: cs(t) - np.pi / 2, 1e-6, 1 - 1e-6)
    r_ring = t_ring / (1 - t_ring) * lam
    c0_rms = 16 * np.sqrt(2) * np.pi**2 * Emin * rms_s
    c0_ring = 16 * np.sqrt(2) * np.pi**2 * Emin * r_ring
    c0_lit_rms = 16 * np.sqrt(2) * np.pi**2 * 1.204 * rms_s
    out = dict(
        model="Faddeev-Skyrme E = int[(kappa2/2)(dn)^2 + (kappa4/4) sum_ij (d_i n x d_j n)^2]; Ward units",
        ansatz="n = U e3 U^+, U = exp(i f(r) rhat.tau), free spline profile, Derrick-optimal scale; Q = 1",
        E_W_ansatz=float(Emin), E_W_literature=1.204, E_W_literature_note="Sutcliffe 2007 Table 2 (lattice, ~1% low); 1.21-1.22 more accurate",
        ansatz_excess_over_1p204=float(Emin / 1.204 - 1),
        virial_E2_eq_E4_after_scaling=True, E2_unscaled=float(E2), E4_unscaled=float(E4), scale_factor=float(lam),
        phi_independence_rel=float(abs(E2b + E4b - E2 - E4) / (E2 + E4)),
        unit_norm_maxdev=float(np.max(np.abs(nn - 1))),
        R_rms_energy_ward=float(rms_s), R_ring_ward=float(r_ring),
        c0_hopf_rms=float(c0_rms), c0_hopf_ring=float(c0_ring), c0_hopf_rms_with_lit_energy=float(c0_lit_rms),
        formula="M R = 16 sqrt(2) pi^2 kappa4 E_W Rt = c0_hopf * kappa4 (hbar = c = 1); length unit l = sqrt(kappa4/kappa2)",
        optimizer=dict(success=bool(res.success), nit=int(res.nit), message=str(res.message)),
        quadrature=dict(NT=NT, NTH=NTH, spline_nodes=KN),
        runtime_s=time.time() - t0)
    with open(os.path.join(HERE, 'hopfion.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))
    print("\nCHECKS")
    print(f"  |n| = 1 to {out['unit_norm_maxdev']:.1e};  phi independence {out['phi_independence_rel']:.1e}")
    print(f"  ansatz energy {Emin:.4f} vs literature 1.204-1.22 (upper bound expected): excess {100*(Emin/1.204-1):.1f}%")


if __name__ == '__main__':
    main()
