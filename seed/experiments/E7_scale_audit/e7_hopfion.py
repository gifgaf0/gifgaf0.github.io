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
map equals deg U = 1. The profile f is optimised freely at the Derrick-optimal scale, so
E_ans >= E_true (upper bound); literature E_W(Q=1) = 1.204 (Sutcliffe 2007 lattice) to 1.22.

RECONCILIATION FIX (after the cross-check): version 1 used a not-a-knot cubic spline for f(t),
t = r/(1+r), with f(1) = 0 but a free slope at t = 1, i.e. a spurious f ~ a/r tail. The energy and
the ring radius are insensitive to it, but the energy-rms radius int r^2 eps d^3r is not (it was
cut off only by the last Gauss node) and came out 2.144 instead of 2.061. The profile is now
f(t) = (1-t)^2 h(t) with h a free spline (h(0) = pi), which builds in the correct f ~ C/r^2 tail.

Identity used as an extra check (verified symbolically below): averaged over angles, the ansatz's
quadratic and quartic densities are (16/3)(f'^2 + 2 sin^2 f/r^2) and (16/3)(4 sin^2 f f'^2/r^2 +
2 sin^4 f/r^4), so E_W[f] = (1/(3 pi^2)) x the ANW hedgehog functional of F(y) = f(y/sqrt2).
Consequences: E_W(ansatz) = a1/(3 pi^2) exactly (NOT an independent calibration of the Skyrme
solver), R_rms = x_E/sqrt2 and R_ring = x_half/sqrt2 with the hedgehog radii of e7_hedgehog.py.
Outputs hopfion.json.  Runtime ~1-2 min, one core.
"""
import json, os, time
import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize, brentq

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
    # symbolic check of the angular-average identity (at a fixed phi, the density is phi independent)
    u = sp.symbols('u')
    ok = True
    for dens, claim in [(d2, sp.Rational(16, 3) * (fp**2 + 2 * sp.sin(f)**2 / r**2)),
                        (d4, sp.Rational(16, 3) * (4 * sp.sin(f)**2 * fp**2 / r**2 + 2 * sp.sin(f)**4 / r**4))]:
        integ = sp.integrate(sp.expand(sp.simplify(dens.subs(ph, sp.Rational(3, 10))).subs(th, sp.acos(u))), (u, -1, 1))
        resid = sp.simplify(sp.expand_trig(integ - claim))
        ok = ok and (resid == 0)
    return fn, bool(ok)


DENS, IDENTITY_OK = build_density()

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
    """f(t) = (1-t)^2 h(t); h spline with h(0) = pi and KN+1 free node values (including h(1),
    the C/r^2 tail amplitude). f ~ h(1)/r^2 at large r: no spurious 1/r tail."""
    hv = np.concatenate([[np.pi], vals])
    cs = CubicSpline(tnodes, hv, bc_type='not-a-knot')
    h = cs(tq); hp = cs(tq, 1)
    f = (1 - tq)**2 * h
    dfdt = -2 * (1 - tq) * h + (1 - tq)**2 * hp
    return f, dfdt / drdt, cs


def energies_of(f, fp, phi=0.0):
    F = np.broadcast_to(f[:, None], R.shape); FP = np.broadcast_to(fp[:, None], R.shape)
    d2, d4, nn = DENS(F, FP, R, TH, phi)
    norm = 2 * np.pi / (32 * np.sqrt(2) * np.pi**2)    # azimuthal integral done (density is phi independent)
    E2 = norm * np.sum(W * d2)
    # d4 = sum_{i<j} |d_i n x d_j n|^2 = (1/2) sum_{i,j}, which is exactly the Ward quartic weight
    E4 = norm * np.sum(W * d4)
    return E2, E4, d2, d4, nn


def energies(vals, phi=0.0):
    f, fp, _ = profile(vals)
    return energies_of(f, fp, phi)


def scaled_energy(vals):
    E2, E4 = energies(vals)[:2]
    return 2 * np.sqrt(E2 * E4)


NORM = 2 * np.pi / (32 * np.sqrt(2) * np.pi**2)
WR = twq * drdt * rq**2


def energies_radial(vals):
    """Same energies with the angular integral done analytically (identity checked symbolically above).
    Used only to drive the optimiser quickly; the final profile is evaluated with the 3D-angle quadrature."""
    f, fp, _ = profile(vals)
    s2 = np.sin(f)**2
    E2 = NORM * np.sum(WR * (16 / 3) * (fp**2 + 2 * s2 / rq**2))
    E4 = NORM * np.sum(WR * (16 / 3) * (4 * s2 * fp**2 / rq**2 + 2 * s2**2 / rq**4))
    return E2, E4


def scaled_energy_radial(vals):
    E2, E4 = energies_radial(vals)
    return 2 * np.sqrt(E2 * E4)


def scaled_observables(E2, E4, d2, d4):
    lam = np.sqrt(E4 / E2)          # optimal rescaling r -> lam r
    eps_s = lam * d2 + d4 / lam      # density of the rescaled configuration at r = lam r0 (up to a constant)
    rms_s = np.sqrt(np.sum(W * eps_s * R**2) / np.sum(W * eps_s)) * lam
    return lam, 2 * np.sqrt(E2 * E4), rms_s


def exact_profile_check():
    """Feed f(r) = F_Skyrme(sqrt2 r) (e7_hedgehog.py solution, C/x^2 tail beyond its grid) through the
    same 3D-angle quadrature. Independent of the spline optimiser."""
    p = os.path.join(HERE, 'hedgehog_profile.npz')
    hj = os.path.join(HERE, 'hedgehog.json')
    if not (os.path.exists(p) and os.path.exists(hj)):
        return None
    d = np.load(p); H = json.load(open(hj))['best']
    xs, Fs, dFs = d['x'], d['F'], d['dF']
    C = H['C_tail']
    y = np.sqrt(2) * rq
    F = np.where(y <= xs[-1], np.interp(y, xs, Fs), C / np.maximum(y, 1e-300)**2)
    dF = np.where(y <= xs[-1], np.interp(y, xs, dFs), -2 * C / np.maximum(y, 1e-300)**3)
    F = np.where(y < xs[0], np.pi + dFs[0] * y, F)
    f = F; fp = np.sqrt(2) * dF
    E2, E4, d2, d4, _ = energies_of(f, fp)
    lam, Emin, rms = scaled_observables(E2, E4, d2, d4)
    t_ring = brentq(lambda r: np.interp(np.sqrt(2) * r, xs, Fs) - np.pi / 2, 0.1, 10)
    return dict(E_W=float(Emin), E2_over_E4=float(E2 / E4), R_rms=float(rms), R_ring=float(t_ring * lam),
                identity_predictions=dict(E_W=H['a1'] / (3 * np.pi**2), R_rms=H['xrms_E'] / np.sqrt(2),
                                          R_ring=H['x_half'] / np.sqrt(2)))


def main():
    t0 = time.time()
    # initial guess: f = pi/(1+r^2), i.e. h = pi (1+r)^2/(1+r^2) at the free nodes (-> pi at t = 1)
    r_nodes = tnodes[1:-1] / (1 - tnodes[1:-1])
    v0 = np.concatenate([np.pi * (1 + r_nodes)**2 / (1 + r_nodes**2), [np.pi]])
    print(f"symbolic angular-average identity holds: {IDENTITY_OK}", flush=True)
    print(f"initial scaled energy {scaled_energy(v0):.5f}", flush=True)
    # optimiser driven by the radial (angle-integrated) energy: the C/r^2-tail parametrisation has a nearly flat
    # tail direction, and with the 3D-angle quadrature in the loop it needed > 15 CPU-min (v2 first attempt)
    res = minimize(scaled_energy_radial, v0, method='L-BFGS-B',
                   options=dict(maxiter=20000, ftol=1e-15, gtol=1e-11, maxfun=2000000, maxcor=50))
    v = res.x
    E2, E4, d2, d4, nn = energies(v)          # final profile evaluated with the full 3D-angle quadrature
    E2r, E4r = energies_radial(v)
    print(f"optimiser: {res.message}, nit = {res.nit}; 3D vs radial energy rel. diff "
          f"{abs(E2 + E4 - E2r - E4r) / (E2 + E4):.1e}", flush=True)
    lam, Emin, rms_s = scaled_observables(E2, E4, d2, d4)
    # phi independence and unit-norm checks
    E2b, E4b = energies(v, phi=0.7)[:2]
    _, _, cs = profile(v)
    t_ring = brentq(lambda t: (1 - t)**2 * cs(t) - np.pi / 2, 1e-6, 1 - 1e-6)
    r_ring = t_ring / (1 - t_ring) * lam
    c0_rms = 16 * np.sqrt(2) * np.pi**2 * Emin * rms_s
    c0_ring = 16 * np.sqrt(2) * np.pi**2 * Emin * r_ring
    c0_lit_rms = 16 * np.sqrt(2) * np.pi**2 * 1.204 * rms_s
    exact = exact_profile_check()
    out = dict(
        model="Faddeev-Skyrme E = int[(kappa2/2)(dn)^2 + (kappa4/4) sum_ij (d_i n x d_j n)^2]; Ward units",
        ansatz="n = U e3 U^+, U = exp(i f(r) rhat.tau), f = (1-t)^2 h(t) with free spline h (C/r^2 tail built in), "
               "Derrick-optimal scale; Q = 1",
        E_W_ansatz=float(Emin), E_W_literature=1.204, E_W_literature_note="Sutcliffe 2007 Table 2 (lattice, ~1% low); 1.21-1.22 more accurate",
        ansatz_excess_over_1p204=float(Emin / 1.204 - 1),
        virial_E2_eq_E4_after_scaling=True, E2_unscaled=float(E2), E4_unscaled=float(E4), scale_factor=float(lam),
        tail_amplitude_h1_unscaled=float(v[-1]),
        phi_independence_rel=float(abs(E2b + E4b - E2 - E4) / (E2 + E4)),
        unit_norm_maxdev=float(np.max(np.abs(nn - 1))),
        R_rms_energy_ward=float(rms_s), R_ring_ward=float(r_ring),
        c0_hopf_rms=float(c0_rms), c0_hopf_ring=float(c0_ring), c0_hopf_rms_with_lit_energy=float(c0_lit_rms),
        formula="M R = 16 sqrt(2) pi^2 kappa4 E_W Rt = c0_hopf * kappa4 (hbar = c = 1); length unit l = sqrt(kappa4/kappa2)",
        identity=dict(symbolic_check_pass=IDENTITY_OK,
                      statement="E_W[f] = (1/(3 pi^2)) E_ANW[F], F(y) = f(y/sqrt2): E_W(ansatz) = a1/(3 pi^2), "
                                "R_rms = x_E/sqrt2, R_ring = x_half/sqrt2",
                      consequence="E_W(ansatz) is the Skyrme a1 again, so it is not an independent calibration"),
        exact_profile_check=exact,
        optimizer=dict(success=bool(res.success), nit=int(res.nit), message=str(res.message),
                       driver="L-BFGS-B on the angle-integrated energy; final profile evaluated with the 3D-angle quadrature",
                       rel_diff_3D_vs_radial=float(abs(E2 + E4 - E2r - E4r) / (E2 + E4))),
        quadrature=dict(NT=NT, NTH=NTH, spline_nodes=KN),
        version="v2 (reconciliation): tail-correct profile; v1 gave R_rms = 2.1441 from a spurious a/r spline tail",
        runtime_s=time.time() - t0)
    with open(os.path.join(HERE, 'hopfion.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))
    print("\nCHECKS")
    print(f"  |n| = 1 to {out['unit_norm_maxdev']:.1e};  phi independence {out['phi_independence_rel']:.1e}")
    print(f"  ansatz energy {Emin:.6f} vs literature 1.204-1.22 (upper bound expected): excess {100*(Emin/1.204-1):.1f}% over 1.204")
    if exact:
        ip = exact['identity_predictions']
        print(f"  identity: E_W {Emin:.7f} vs a1/(3pi^2) {ip['E_W']:.7f}; R_rms {rms_s:.5f} vs x_E/sqrt2 {ip['R_rms']:.5f}; "
              f"R_ring {r_ring:.5f} vs x_half/sqrt2 {ip['R_ring']:.5f}")
        print(f"  exact profile through the same quadrature: E_W {exact['E_W']:.7f}, R_rms {exact['R_rms']:.5f}, "
              f"R_ring {exact['R_ring']:.5f}, E2/E4 {exact['E2_over_E4']:.6f}")


if __name__ == '__main__':
    main()
