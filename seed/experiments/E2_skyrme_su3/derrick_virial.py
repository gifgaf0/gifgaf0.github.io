#!/usr/bin/env python3
"""E2 -- Derrick scaling, virial theorem and von Laue condition for the B = 1 hedgehog.

Units F_pi = e = 1 (x = e F_pi r, energies in F_pi/e). With E2 = 4pi int (1/8) x^2 (F'^2 + 2 s^2/x^2) dx and
E4 = 4pi int (1/2) s^2 (s^2/x^2 + 2 F'^2) dx, the dilated profile F_mu(x) = F(mu x) has
   E2[F_mu] = E2/mu,   E4[F_mu] = mu E4        (computed here by quadrature, not assumed)
so E(mu) = E2/mu + mu E4 is stationary at mu = 1 iff E2 = E4, and without the Skyrme term E(mu) = E2/mu
falls monotonically as the fold shrinks (mu -> inf): no minimum (Derrick 1964).
Also: the sigma-model-only radial equation x^2 F'' + 2x F' - sin 2F = 0 has no solution from F(0) = pi
to F(inf) = 0 (in s = ln x it is a damped pendulum between two maxima of V = cos(2F)/2); integrated
from the centre it always settles at F = pi/2.
Von Laue: stress tensor of the static hedgehog (derived from principal strains and verified against the
Noether stress tensor in verify_densities.py)
   T_rr  = (1/8)(F'^2 - 2 s^2/x^2) + (s^2/(2x^2))(2F'^2 - s^2/x^2),   T_thth = -(1/8)F'^2 + s^4/(2x^4),
   p = (T_rr + 2 T_thth)/3,   equilibrium  T_rr' + (2/x)(T_rr - T_thth) = 0,   int d^3x p = 0.
Writes out/derrick.json. Runtime ~5 s.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import skyrme_hedgehog as sh  # noqa: E402

OUT = os.path.join(HERE, "out")


def main():
    t0 = time.time()
    sol = sh.solve_mapped(140, L=2.0)
    wb = sh.bary_weights(sol["N"])
    L = sol["L"]

    def Fx(x):
        x = np.atleast_1d(x)
        t = (x - L) / (x + L)
        F = sh.bary_eval(sol["t"], sol["F"], wb, t)
        Fp = (1 - t) ** 2 / (2 * L) * sh.bary_eval(sol["t"], sol["Ft"], wb, t)
        return F, Fp

    # quadrature nodes on the half line (Gauss-Legendre in t, x = L(1+t)/(1-t))
    tg, wg = np.polynomial.legendre.leggauss(400)
    xg = L * (1 + tg) / (1 - tg)
    wx = wg * 2 * L / (1 - tg) ** 2

    def E2E4(mu):
        F, Fp = Fx(mu * xg)
        Fp = mu * Fp
        d = sh.densities(xg, F, Fp)
        return 4 * np.pi * np.dot(wx, d["E2"]), 4 * np.pi * np.dot(wx, d["E4"])

    E2, E4 = E2E4(1.0)
    print(f"E2 = {E2:.12f}, E4 = {E4:.12f} (F_pi/e); E2/E4 - 1 = {E2/E4-1:+.2e}; M = {E2+E4:.10f}")
    mus = np.exp(np.linspace(np.log(0.2), np.log(5.0), 41))
    rows = []
    scal_err = 0.0
    for mu in mus:
        e2, e4 = E2E4(mu)
        scal_err = max(scal_err, abs(e2 * mu / E2 - 1), abs(e4 / (mu * E4) - 1))
        rows.append((float(mu), float(e2), float(e4)))
    rows = np.array(rows)
    Etot = rows[:, 1] + rows[:, 2]
    imin = int(np.argmin(Etot))
    # refine the minimum of the quadrature-evaluated E(mu)
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda m: sum(E2E4(m)), bounds=(0.5, 2.0), method="bounded", options={"xatol": 1e-10})
    mu_star = r.x
    mono = bool(np.all(np.diff(rows[:, 1]) < 0))
    print(f"scaling law E2(mu) mu = E2, E4(mu)/mu = E4: max rel deviation {scal_err:.1e} over mu in [0.2, 5]")
    print(f"E(mu) minimum at mu* = {mu_star:.9f} (expected 1); E(mu*) = {r.fun:.10f}")
    print(f"sigma-model-only energy E2(mu) strictly decreasing in mu (shrinking): {mono}; E2(5)/E2(1) = {rows[-1,1]/E2:.4f}")

    # sigma model alone: radial ODE from the centre never reaches F = 0
    def rhs(s, y):            # s = ln x : F_ss = -F_s + sin 2F
        return [y[1], -y[1] + np.sin(2 * y[0])]
    ends = []
    for a in [0.1, 1.0, 10.0]:
        s0 = np.log(1e-4 / a)
        x0 = np.exp(s0)
        y0 = [np.pi - a * x0, -a * x0]
        so = solve_ivp(rhs, [s0, 40.0], y0, rtol=1e-11, atol=1e-13)
        ends.append((a, float(so.y[0, -1]), float(so.y[0].min())))
    print("sigma model only, shooting from F = pi - a x: F(x = e^40) = " +
          ", ".join(f"{e:.6f} (a={a}, min F {m:.4f})" for a, e, m in ends) + f"  [pi/2 = {np.pi/2:.6f}]")
    sig_ok = all(abs(e - np.pi / 2) < 1e-6 and m > 0.5 for a, e, m in ends)

    # von Laue
    x = xg
    F, Fp = Fx(x)
    s2 = np.sin(F) ** 2
    q = s2 / x ** 2
    Trr = 0.125 * (Fp ** 2 - 2 * q) + 0.5 * q * (2 * Fp ** 2 - q)
    Ttt = -0.125 * Fp ** 2 + 0.5 * q * q
    p = (Trr + 2 * Ttt) / 3
    vonlaue = np.dot(wx, x ** 2 * p)
    vonlaue_abs = np.dot(wx, x ** 2 * np.abs(p))
    print(f"von Laue: int x^2 p dx = {vonlaue:+.3e}; int x^2 |p| dx = {vonlaue_abs:.6f}; ratio {vonlaue/vonlaue_abs:+.1e}")
    # equilibrium on the Chebyshev nodes (spectral derivative of T_rr)
    t = sol["t"][1:-1]
    xs = L * (1 + t) / (1 - t)
    Fs = sol["F"][1:-1]
    Fps = (1 - t) ** 2 / (2 * L) * sol["Ft"][1:-1]
    s2s = np.sin(Fs) ** 2
    qs = s2s / xs ** 2
    Trr_n = np.zeros(sol["N"] + 1)
    Trr_n[1:-1] = 0.125 * (Fps ** 2 - 2 * qs) + 0.5 * qs * (2 * Fps ** 2 - qs)
    Trr_n[-1] = 0.125 * (sol["Fp"][-1] ** 2 - 2 * sol["Fp"][-1] ** 2) + 0.5 * sol["Fp"][-1] ** 2 * (2 * sol["Fp"][-1] ** 2 - sol["Fp"][-1] ** 2)
    Ttt_s = -0.125 * Fps ** 2 + 0.5 * qs * qs
    dTrr = ((1 - t) ** 2 / (2 * L)) * (sol["D"] @ Trr_n)[1:-1]
    eq_res = dTrr + 2 / xs * (Trr_n[1:-1] - Ttt_s)
    scale = np.abs(dTrr) + np.abs(2 / xs * (Trr_n[1:-1] - Ttt_s)) + 1e-300
    m = xs < 30
    eq_pt = float(np.max(np.abs(eq_res[m]) / scale[m]))
    eq_rel = float(np.max(np.abs(eq_res[m])) / np.max(np.abs(dTrr[m])))
    k = np.argmax(np.where(m, np.abs(eq_res) / scale, 0))
    print(f"local equilibrium T_rr' + 2(T_rr - T_thth)/x = 0 on nodes x < 30: max |residual| / max |T_rr'| = {eq_rel:.1e}"
          f"\n   (pointwise relative {eq_pt:.1e} at x = {xs[k]:.3g}, where both terms are ~1e-4 and round-off in the"
          f" spectral derivative dominates)")
    # pressure node
    xx = np.linspace(0.01, 15, 15000)
    Fq, Fpq = Fx(xx)
    qq = np.sin(Fq) ** 2 / xx ** 2
    pq = ((0.125 * (Fpq ** 2 - 2 * qq) + 0.5 * qq * (2 * Fpq ** 2 - qq)) + 2 * (-0.125 * Fpq ** 2 + 0.5 * qq * qq)) / 3
    sc = np.where(np.diff(np.sign(pq)) != 0)[0]
    # reconciliation: root of p(x) by Brent's method (was the midpoint of the grid interval, 2.15221)
    from scipy.optimize import brentq

    def p_of_x(xv):
        Fv, Fpv = Fx(xv)
        qv = np.sin(Fv[0]) ** 2 / xv ** 2
        Fpv = Fpv[0]
        return ((0.125 * (Fpv ** 2 - 2 * qv) + 0.5 * qv * (2 * Fpv ** 2 - qv)) + 2 * (-0.125 * Fpv ** 2 + 0.5 * qv * qv)) / 3
    nodes = [float(brentq(p_of_x, xx[i], xx[i + 1], xtol=1e-13)) for i in sc]
    a0 = -float(sol["Fp"][-1])                       # F = pi - a0 x near x = 0
    p0_exact = -a0 ** 2 / 8 + a0 ** 4 / 2           # T_rr = T_thth = -a^2/8 + a^4/2 at x = 0
    print(f"pressure p(x): p(0) = -a^2/8 + a^4/2 = {p0_exact:+.6f} (F_pi/e)(e F_pi)^3 [a = -F'(0) = {a0:.10f}; "
          f"grid value at x = 0.01: {pq[0]:+.6f}], sign changes at x = {nodes}; p < 0 outside")

    checks = {
        "virial_E2_eq_E4_1e-4": abs(E2 / E4 - 1) < 1e-4,
        "virial_E2_eq_E4_1e-10": abs(E2 / E4 - 1) < 1e-10,
        "scaling_law_by_quadrature": scal_err < 1e-9,
        "E_mu_minimum_at_1": abs(mu_star - 1) < 1e-6,
        "no_minimum_without_Skyrme_term": mono and sig_ok,
        "von_Laue_zero": abs(vonlaue / vonlaue_abs) < 1e-9,
        "local_equilibrium": eq_rel < 1e-6,
        "single_pressure_node_positive_core": len(nodes) == 1 and pq[0] > 0,
    }
    print("\nCHECKS")
    for k, v in checks.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    ok = all(checks.values())
    out = {"E2": E2, "E4": E4, "E2_over_E4_minus_1": E2 / E4 - 1, "scaling_max_rel_dev": scal_err,
           "mu_star": mu_star, "scaling_curve": {"mu": rows[:, 0].tolist(), "E2": rows[:, 1].tolist(), "E4": rows[:, 2].tolist()},
           "sigma_model_shooting_end_values": ends, "von_Laue_integral": vonlaue, "von_Laue_abs": vonlaue_abs,
           "von_Laue_ratio": vonlaue / vonlaue_abs, "equilibrium_max_residual_over_max_dTrr": eq_rel, "equilibrium_pointwise_rel": eq_pt,
           "pressure_nodes_x": nodes, "p0": p0_exact, "p_at_x0.01": float(pq[0]),
           "pressure_curve": {"x": xx[::50].tolist(), "x2p": (xx[::50] ** 2 * pq[::50]).tolist()},
           "checks": {k: bool(v) for k, v in checks.items()}, "all_checks_pass": bool(ok), "runtime_s": time.time() - t0}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "derrick.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nall checks pass: {ok};  runtime {time.time()-t0:.1f} s")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
