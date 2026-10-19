#!/usr/bin/env python3
"""E7 cross-check: Q = 1 Faddeev-Skyrme 'hedgehog-Hopf' ansatz n = U tau3 U^dagger.

Analytic reduction (derived for this cross-check, see CROSSCHECK.md):
with U = cos f + i sin f (rhat.tau) and the left current l_i^a,  M M^T = f'^2 P + (s^2/r^2)(1-P), so

  (dn)^2                 = 4 [ f'^2 sin^2(th) + (s^2/r^2)(1 + cos^2 th) ]
  sum_ij (d_i n x d_j n)^2 = 32 (s^2/r^2) [ f'^2 sin^2 th + (s^2/r^2) cos^2 th ]

and after the angular integral, in Ward units (E8: E = (1/(32 sqrt2 pi^2)) int[(dn)^2 + 1/2 sum_ij (d_i n x d_j n)^2])

  E_W = (1/(3 sqrt2 pi)) int dr [ r^2 f'^2 + 2 sin^2 f + 4 sin^2 f f'^2 + 2 sin^4 f / r^2 ].

Substituting r = y/sqrt2 turns this into exactly (1/(3 pi^2)) x the ANW Skyrme functional, so
the optimal ansatz profile is f(r) = F_Skyrme(sqrt2 r) and E_W(ansatz) = a1/(3 pi^2), while
lengths are R_Ward = x_ANW / sqrt2 (energy rms radius x_E/sqrt2, ring radius x_half/sqrt2).

This script checks the reduction NUMERICALLY by building n(x) explicitly from SU(2) matrices,
differentiating by central finite differences in 3D Cartesian coordinates, and integrating the
full energy density over (r, theta) at two azimuths.  Writes cc_hopfion.json.
"""
import json
import numpy as np
from numpy.polynomial.legendre import leggauss
from cc_hedgehog import Hedgehog, basis, observables

PI = np.pi
tau = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]


def skyrme_profile():
    h = Hedgehog(N=60, L=2.0, Nq=1200)
    h.solve()
    return h


def F_of_x(h, x):
    shp = np.shape(x)
    xf = np.ravel(x)
    t = xf / (h.L + xf)
    Phi, dPhi, F0, dF0 = basis(t, h.N)
    return (F0 + h.c @ Phi).reshape(shp)


def nfield(h, X, Y, Z, lam=1.0):
    """n^a = (1/2) Tr(tau_a U tau3 U^+), U = exp(i f(r) rhat.tau), f(r) = F(sqrt2 r / lam)."""
    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    f = F_of_x(h, np.sqrt(2) * r / lam)
    c, s = np.cos(f), np.sin(f)
    a0, a1, a2, a3 = c, s * X / r, s * Y / r, s * Z / r
    # U = a0 + i a.tau ; n = R(U) e3 computed with explicit matrices (vectorised)
    U = np.empty(X.shape + (2, 2), complex)
    U[..., 0, 0] = a0 + 1j * a3
    U[..., 0, 1] = 1j * a1 + a2
    U[..., 1, 0] = 1j * a1 - a2
    U[..., 1, 1] = a0 - 1j * a3
    Ud = np.conj(np.swapaxes(U, -1, -2))
    M = U @ tau[2] @ Ud
    n = np.stack([0.5 * np.real(np.einsum('ij,...ji->...', tau[k], M)) for k in range(3)], axis=-1)
    return n


def energy(h, lam=1.0, phi=0.0, Nr=500, Nth=64, hstep=1e-4, Lmap=1.5):
    u, w = leggauss(Nr)
    t = 0.5 * (u + 1); wt = 0.5 * w
    r = Lmap * t / (1 - t); wr = wt * Lmap / (1 - t) ** 2
    v, wv = leggauss(Nth)
    th = np.arccos(v)                # integrate over cos(theta)
    R, TH = np.meshgrid(r, th, indexing='ij')
    WR, WTH = np.meshgrid(wr, wv, indexing='ij')
    X = R * np.sin(TH) * np.cos(phi); Y = R * np.sin(TH) * np.sin(phi); Z = R * np.cos(TH)
    n0 = nfield(h, X, Y, Z, lam)
    d = []
    for e in np.eye(3):
        npl = nfield(h, X + hstep * e[0], Y + hstep * e[1], Z + hstep * e[2], lam)
        nmi = nfield(h, X - hstep * e[0], Y - hstep * e[1], Z - hstep * e[2], lam)
        d.append((npl - nmi) / (2 * hstep))
    e2 = sum(np.sum(di * di, axis=-1) for di in d)
    e4 = 0.0
    for i in range(3):
        for j in range(3):
            cr = np.cross(d[i], d[j])
            e4 = e4 + 0.5 * np.sum(cr * cr, axis=-1)
    norm = 1 / (32 * np.sqrt(2) * PI ** 2)
    jac = 2 * PI * R ** 2 * WR * WTH          # d^3x = r^2 dr dcos(th) dphi (axially symmetric)
    E2 = norm * np.sum(jac * e2); E4 = norm * np.sum(jac * e4)
    dens = norm * (e2 + e4)
    Rrms = np.sqrt(np.sum(jac * dens * R ** 2) / np.sum(jac * dens))
    unit_err = np.max(np.abs(np.sum(n0 * n0, axis=-1) - 1))
    return dict(E=E2 + E4, E2=E2, E4=E4, Rrms=Rrms, unit_err=unit_err)


def main():
    h = skyrme_profile()
    ob = observables(h)
    a1, xE, xh = ob["a1"], ob["xE"], ob["x_half"]
    pred = dict(E_W=a1 / (3 * PI ** 2), R_rms=xE / np.sqrt(2), R_ring=xh / np.sqrt(2))
    print("analytic mapping: E_W = a1/(3pi^2) = %.10f, R_rms = x_E/sqrt2 = %.8f, R_ring = x_half/sqrt2 = %.8f"
          % (pred["E_W"], pred["R_rms"], pred["R_ring"]))
    res = {}
    for (Nr, Nth) in [(300, 48), (500, 64)]:
        for phi in [0.0, 0.7]:
            r = energy(h, phi=phi, Nr=Nr, Nth=Nth)
            res[f"Nr{Nr}_Nth{Nth}_phi{phi}"] = r
            print(f"numeric 3D-FD (Nr={Nr}, Nth={Nth}, phi={phi}): E_W = {r['E']:.10f}  E2/E4 = {r['E2']/r['E4']:.8f}"
                  f"  R_rms = {r['Rrms']:.8f}  max||n|-1| = {r['unit_err']:.1e}")
    # Derrick check: scaling lam -> energy minimal at lam = 1
    der = {lam: energy(h, lam=lam, Nr=300, Nth=48)["E"] for lam in [0.95, 1.0, 1.05]}
    print("Derrick scan E(lam):", der)
    best = res["Nr500_Nth64_phi0.0"]
    c0 = 16 * np.sqrt(2) * PI ** 2
    out = dict(analytic=pred, numeric=res, derrick_scan={str(k): v for k, v in der.items()},
               c0_hopf_rms=c0 * best["E"] * best["Rrms"],
               c0_hopf_ring=c0 * best["E"] * pred["R_ring"],
               c0_hopf_rms_analytic=c0 * pred["E_W"] * pred["R_rms"],
               note="M R = 16 sqrt2 pi^2 kappa4 E_W R_Ward (hbar=c=1); kappa4 = 1/g^2")
    print("c0_hopf (energy rms) = %.3f ; c0_hopf (ring) = %.3f" % (out["c0_hopf_rms"], out["c0_hopf_ring"]))
    with open("cc_hopfion.json", "w") as f:
        json.dump(out, f, indent=1, default=float)


if __name__ == "__main__":
    main()
