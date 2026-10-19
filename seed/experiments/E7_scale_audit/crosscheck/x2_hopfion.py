#!/usr/bin/env python3
"""E7 second cross-check (x2): hedgehog-Hopf ansatz of the Faddeev-Skyrme model, evaluated
directly from the definition of the energy on a 3D spherical quadrature.

Ward normalisation (PLAN.md E8): E_W = 1/(32 sqrt2 pi^2) int [ d_i n . d_i n
                                         + 1/2 sum_ij (d_i n x d_j n)^2 ] d^3x.
Ansatz: n = U e3 U^+ with U = exp(i f(r) rhat.tau), i.e. e3 rotated by the angle 2 f(r) about
rhat (Rodrigues formula).  Q = 1 (Hopf map composed with a degree-1 map S^3 -> S^3).

Derivatives d_i n are taken by 4th-order central finite differences of the explicit n(x)
(no use of any reduced formula).  Angular integration: Gauss-Legendre in cos(theta) x uniform
phi; radial: Gauss-Legendre in t with r = L t/(1-t).

Profile: I derived by hand that, after angular averaging, this energy equals a1/(3 pi^2) when
f(r) = F_Skyrme(sqrt2 r) (r = x/sqrt2 maps the ANW functional onto it).  Here that identity is
NOT assumed: the code evaluates the 3D energy for f(r) = F(sqrt2 r), checks Derrick
stationarity (E2 = E4), checks that random smooth profile perturbations raise the energy at
second order, and then measures the energy-rms radius and the ring radius (n = -e3) directly.
Deterministic (seeded); writes x2_hopfion.json.
"""
import json
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
import x2_hedgehog as hh

PI = np.pi
NORM = 1.0 / (32 * np.sqrt(2) * PI ** 2)


class Profile:
    """Skyrme profile F(x) from the x2 shooting solution, analytic C/x^2 - C^3/(21x^6) tail."""
    def __init__(self, Xm=40.0):
        a, da, slo, shi, xv = hh.solve_profile(0.0)
        self.slo, self.shi, self.Xm = slo, shi, Xm
        ob = hh.observables(0.0, a, da, slo, shi, Xm)
        self.C = ob["C_tail"]
        self.a = a
        self.ob = ob

    def F(self, x):
        x = np.asarray(x, float)
        out = np.empty_like(x)
        inn = x <= self.Xm
        xi = np.maximum(x[inn], hh.X0)
        out[inn] = 0.5 * (self.slo.sol(xi)[0] + self.shi.sol(xi)[0])
        small = x[inn] < hh.X0
        if small.any():
            tmp = out[inn]
            tmp[small] = PI - self.a * x[inn][small]
            out[inn] = tmp
        xo = x[~inn]
        out[~inn] = self.C / xo ** 2 - self.C ** 3 / (21 * xo ** 6)
        return out


def nfield(X, f_of_r):
    """X: (...,3) points -> n (...,3): e3 rotated by angle 2 f(r) about rhat."""
    r = np.linalg.norm(X, axis=-1)
    rh = X / r[..., None]
    th = 2 * f_of_r(r)
    e3 = np.array([0.0, 0.0, 1.0])
    c, s = np.cos(th)[..., None], np.sin(th)[..., None]
    cross = np.cross(rh, e3)
    dot = rh[..., 2:3]
    return e3 * c + cross * s + rh * dot * (1 - c)


def energy_3d(f_of_r, Nr=360, Nth=48, Nph=4, L=1.2, h=1e-3, want_density=False):
    u, w = leggauss(Nr)
    t = 0.5 * (u + 1); wt = 0.5 * w
    r = L * t / (1 - t)
    wr = wt * L / (1 - t) ** 2
    ct, wc = leggauss(Nth)
    st = np.sqrt(1 - ct ** 2)
    ph = (np.arange(Nph) + 0.5) * 2 * PI / Nph
    wph = 2 * PI / Nph
    R, CT, PH = np.meshgrid(r, ct, ph, indexing="ij")
    ST = np.sqrt(1 - CT ** 2)
    X = np.stack([R * ST * np.cos(PH), R * ST * np.sin(PH), R * CT], axis=-1)
    W = (wr[:, None, None] * wc[None, :, None] * wph) * R ** 2
    # derivatives: 4th-order central differences with a step proportional to min(r, 1)
    hs = h * np.minimum(R, 1.0)[..., None]
    D = []
    for i in range(3):
        e = np.zeros(3); e[i] = 1.0
        dn = (-nfield(X + 2 * hs * e, f_of_r) + 8 * nfield(X + hs * e, f_of_r)
              - 8 * nfield(X - hs * e, f_of_r) + nfield(X - 2 * hs * e, f_of_r)) / (12 * hs)
        D.append(dn)
    e2 = sum(np.sum(D[i] ** 2, axis=-1) for i in range(3))
    e4 = 0.0
    for i in range(3):
        for j in range(3):
            if i != j:
                e4 = e4 + 0.5 * np.sum(np.cross(D[i], D[j]) ** 2, axis=-1)
    E2 = NORM * np.sum(W * e2)
    E4 = NORM * np.sum(W * e4)
    eps = e2 + e4
    Er2 = NORM * np.sum(W * R ** 2 * eps)
    n = nfield(X, f_of_r)
    out = dict(E=E2 + E4, E2=E2, E4=E4, Rrms=np.sqrt(Er2 / (E2 + E4)),
               unit_norm_maxdev=float(np.max(np.abs(np.linalg.norm(n, axis=-1) - 1))))
    # phi-independence of the energy density (per (r, theta) the spread over phi)
    out["phi_spread_rel"] = float(np.max(np.abs(eps - eps.mean(axis=2, keepdims=True)))
                                  / np.max(np.abs(eps)))
    if want_density:
        out["_eps"] = eps; out["_R"] = R; out["_W"] = W
    return out


def main():
    t0 = time.time()
    P = Profile()
    a1 = P.ob["a1"]
    print(f"Skyrme a1 = {a1:.10f}, a1/(3 pi^2) = {a1 / (3 * PI ** 2):.10f}, xE/sqrt2 = "
          f"{P.ob['xE'] / np.sqrt(2):.8f}, x_half/sqrt2 = {P.ob['x_half'] / np.sqrt(2):.8f}")
    s2 = np.sqrt(2.0)
    base = lambda r: P.F(s2 * r)
    res = {"model": "Faddeev-Skyrme, Ward units; n = U e3 U^+, f(r) = F_Skyrme(sqrt2 r)",
           "a1": a1, "a1_over_3pi2": a1 / (3 * PI ** 2),
           "xE_over_sqrt2": P.ob["xE"] / s2, "xhalf_over_sqrt2": P.ob["x_half"] / s2}
    # resolution study
    conv = []
    for (Nr, Nth, Nph, L) in [(240, 32, 4, 1.2), (360, 48, 4, 1.2), (480, 64, 6, 1.2), (480, 64, 4, 0.8)]:
        o = energy_3d(base, Nr, Nth, Nph, L)
        o.update(Nr=Nr, Nth=Nth, Nph=Nph, L=L)
        conv.append(o)
        print(f"Nr={Nr} Nth={Nth} Nph={Nph} L={L}: E_W={o['E']:.9f} E2={o['E2']:.9f} E4={o['E4']:.9f} "
              f"R_rms={o['Rrms']:.7f} |n|-1={o['unit_norm_maxdev']:.1e} phi-spread={o['phi_spread_rel']:.1e}")
    best = conv[2]
    res["convergence"] = conv
    res["E_W"] = best["E"]; res["E2"] = best["E2"]; res["E4"] = best["E4"]; res["R_rms"] = best["Rrms"]
    # Derrick: E(lambda) = lambda E2 + E4/lambda for f(lambda r): stationary iff E2 = E4
    res["derrick_E2_over_E4"] = best["E2"] / best["E4"]
    # second-order optimality: random smooth bumps g(r) = r^2 e^{-r^2/s^2} (vanish at 0, decay fast)
    rng = np.random.default_rng(7)
    pert = []
    for k in range(4):
        amp = rng.normal(size=3)
        sc = np.array([0.5, 1.0, 2.0])
        def g(r, amp=amp):
            return sum(a * (r / s) ** 2 * np.exp(-(r / s) ** 2) for a, s in zip(amp, sc))
        Es = []
        for d in (-0.02, 0.0, 0.02):
            Es.append(energy_3d(lambda r, d=d: base(r) + d * g(r), 240, 32, 2, 1.2)["E"])
        first = (Es[2] - Es[0]) / 0.04
        second = (Es[2] - 2 * Es[1] + Es[0]) / 0.02 ** 2
        pert.append(dict(dE_first=first, d2E=second, E_minus=Es[0], E0=Es[1], E_plus=Es[2]))
        print(f"  perturbation {k}: dE/dd = {first:+.2e}, d2E/dd2 = {second:+.3e}")
    res["perturbations"] = pert
    # ring: minimise n3 on the equatorial plane (x, 0, 0)
    rr = np.linspace(0.3, 3.0, 270001)
    Xe = np.stack([rr, 0 * rr, 0 * rr], axis=-1)
    n3 = nfield(Xe, base)[:, 2]
    i = int(np.argmin(n3))
    res["R_ring"] = float(rr[i]); res["n3_min"] = float(n3[i])
    print(f"ring: n3 = {n3[i]:.12f} at r = {rr[i]:.6f}")
    # also the energy-rms radius with a deliberately wrong a/r tail (diagnostic of tail sensitivity)
    def with_tail(r, amp):
        return base(r) + amp * r / (1 + r ** 2) * (1 - np.exp(-r ** 2))
    tl = []
    for amp in (0.0, 2e-3, 5e-3):
        o = energy_3d(lambda r, amp=amp: with_tail(r, amp), 360, 32, 2, 1.2)
        o2 = energy_3d(lambda r, amp=amp: with_tail(r, amp), 360, 32, 2, 0.6)
        tl.append(dict(amp=amp, E=o["E"], Rrms_L1p2=o["Rrms"], Rrms_L0p6=o2["Rrms"]))
        print(f"  tail a/r with a = {amp:.0e}: E_W = {o['E']:.6f}, R_rms = {o['Rrms']:.4f} (L=1.2), "
              f"{o2['Rrms']:.4f} (L=0.6)")
    res["tail_sensitivity"] = tl
    c = 16 * np.sqrt(2) * PI ** 2
    res["c0h_rms"] = c * res["E_W"] * res["R_rms"]
    res["c0h_ring"] = c * res["E_W"] * res["R_ring"]
    print(f"E_W = {res['E_W']:.9f}, R_rms = {res['R_rms']:.6f}, R_ring = {res['R_ring']:.6f}, "
          f"c0h(rms) = {res['c0h_rms']:.3f}, c0h(ring) = {res['c0h_ring']:.3f}")
    res["runtime_s"] = time.time() - t0
    with open("x2_hopfion.json", "w") as fh:
        json.dump(res, fh, indent=1, default=float)
    print(f"done in {res['runtime_s']:.1f} s")


if __name__ == "__main__":
    main()
