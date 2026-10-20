#!/usr/bin/env python3
"""E7 second cross-check (x2): SU(2) Skyrme hedgehog by my own shooting + bisection code.

Written without reading the original E7 scripts (or the earlier cc_* cross-check scripts).
Conventions (PLAN.md E2/E7, ANW): L = (F_pi^2/16) Tr dU dU^+ + 1/(32 e^2) Tr[L_mu, L_nu]^2,
F_pi in the 186-MeV convention, x = e F_pi r, optional pion mass beta = m_pi/(e F_pi):

  M = (F_pi/e) * 4 pi int_0^inf eps(x) dx,
  eps = x^2 F'^2/8 + sin^2F/4 + sin^2F F'^2 + sin^4F/(2 x^2) + (beta^2/4) x^2 (1 - cos F).

Euler-Lagrange equation (derived by hand, checked here by a finite-difference variation of
the energy):  F'' (x^2/4 + 2 s^2) = sin2F/4 - sin2F F'^2 + s^2 sin2F/x^2 + (beta^2/4) x^2 s - x F'/2.

Method: integrate from x0 = 1e-4 with F = pi - a x0, F' = -a (DOP853, rtol 1e-13) and bisect on
a: overshoot (F < 0) means a too large, turn-back (F' > 0 with F > 0) means a too small.
Observables are integrated on the bisection trajectory up to a matching radius X where the
two bracketing trajectories still agree to 1e-9 (absolute); beyond X (massless case) the analytic tail
F = C/x^2 - C^3/(21 x^6) is used (I derived the x^-6 correction from the field equation).

Radius definitions (x units; R = x/(e F_pi)):
  baryon rms        <x^2>_B = int x^2 b dx,  b = -(2/pi) sin^2F F'   (int b dx = 1)
  isoscalar magn.   <x^2>_M = int x^4 b dx / int x^2 b dx           (ANW)
  energy rms        <x^2>_E = int x^2 eps dx / int eps dx
  half-baryon       F(x_half) = pi/2   (1 - (F - sinF cosF)/pi = 1/2  <=>  F = pi/2)
  [extra] mean baryon radius int x b dx, and the radius enclosing 90 % of the energy.
Deterministic; prints its own checks; writes x2_hedgehog.json.
"""
import json
import time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss

PI = np.pi
X0 = 1e-4


def rhs(x, y, beta):
    F, P = y
    s = np.sin(F)
    s2F = np.sin(2 * F)
    num = s2F / 4 - s2F * P * P + s * s * s2F / (x * x) + 0.25 * beta * beta * x * x * s - 0.5 * x * P
    return [P, num / (0.25 * x * x + 2 * s * s)]


def shoot(a, beta, xmax, dense=False):
    def ev_cross(x, y, beta):
        return y[0]
    ev_cross.terminal = True
    ev_cross.direction = -1

    def ev_turn(x, y, beta):
        return y[1]
    ev_turn.terminal = True
    ev_turn.direction = 1
    sol = solve_ivp(rhs, (X0, xmax), [PI - a * X0, -a], args=(beta,), method="DOP853",
                    rtol=1e-13, atol=1e-15, events=(ev_cross, ev_turn), dense_output=dense)
    if sol.t_events[0].size:
        kind = +1          # overshoot: a too large
    elif sol.t_events[1].size:
        kind = -1          # turned back: a too small
    else:
        # no event before xmax: classify by the sign of the growing-mode admixture,
        # q = F' - F k'/k with k the decaying linear tail (k = 1/x^2 massless, Yukawa k1 massive)
        x, (F, P) = sol.t[-1], sol.y[:, -1]
        logk_p = -2.0 / x if beta == 0 else (-beta - 2.0 / x + beta / (1 + beta * x))
        q = P - F * logk_p
        kind = -1 if q > 0 else +1
    return kind, sol


def solve_profile(beta, xmax=400.0, a_lo=0.3, a_hi=40.0):
    # make sure the bracket is valid
    k, _ = shoot(a_lo, beta, xmax)
    assert k == -1, ("a_lo not too small", beta, k)
    k, _ = shoot(a_hi, beta, xmax)
    assert k == +1, ("a_hi not too large", beta, k)
    for it in range(200):
        a = 0.5 * (a_lo + a_hi)
        if a == a_lo or a == a_hi:
            break
        k, sol = shoot(a, beta, xmax)
        if k == +1:
            a_hi = a
        elif k == -1:
            a_lo = a
        else:
            break
    _, slo = shoot(a_lo, beta, xmax, dense=True)
    _, shi = shoot(a_hi, beta, xmax, dense=True)
    # validity: where the two bracketing trajectories still agree
    xend = min(slo.t[-1], shi.t[-1])
    xs = np.linspace(X0, xend, 200001)
    Flo, Fhi = slo.sol(xs)[0], shi.sol(xs)[0]
    dif = np.abs(Flo - Fhi)
    bad = np.where(dif > 1e-9)[0]
    xvalid = xs[bad[0]] if bad.size else xend
    return 0.5 * (a_lo + a_hi), a_hi - a_lo, slo, shi, xvalid


def gl_grid(a, b, npan, order=32):
    u, w = leggauss(order)
    edges = np.geomspace(a, b, npan + 1)
    lo, hi = edges[:-1, None], edges[1:, None]
    x = (0.5 * (hi - lo) * (u + 1) + lo).ravel()
    W = (0.5 * (hi - lo) * w).ravel()
    return x, W


def dens(x, F, P, beta):
    s = np.sin(F)
    e2 = x * x * P * P / 8 + s * s / 4
    e4 = s * s * P * P + s ** 4 / (2 * x * x)
    e0 = 0.25 * beta * beta * x * x * (1 - np.cos(F))
    return e2, e4, e0


def observables(beta, a, da, slo, shi, X):
    # average the two bracketing trajectories (they agree to 1e-10 below X)
    x, W = gl_grid(X0, X, 400)
    ylo, yhi = slo.sol(x), shi.sol(x)
    F = 0.5 * (ylo[0] + yhi[0])
    P = 0.5 * (ylo[1] + yhi[1])
    # inner piece [0, X0]: F ~ pi - a x, contributes O(X0^3) -> include leading terms
    e2, e4, e0 = dens(x, F, P, beta)
    eps = e2 + e4 + e0
    s = np.sin(F)
    I = {}
    I["E2"] = np.sum(W * e2)
    I["E4"] = np.sum(W * e4)
    I["E0"] = np.sum(W * e0)
    I["Lam"] = np.sum(W * x * x * s * s * (1 + 4 * (P * P + s * s / (x * x))))
    b = -(2 / PI) * s * s * P
    I["B0"] = np.sum(W * b)
    I["B1"] = np.sum(W * x * b)
    I["B2"] = np.sum(W * x * x * b)
    I["B4"] = np.sum(W * x ** 4 * b)
    I["Ex2"] = np.sum(W * x * x * eps)
    # [0, X0] inner contributions (F = pi - a x): e2 ~ a^2 x^2/8 + a^2 x^2/4, e4 ~ a^4 x^2 + a^4 x^2/2
    I["E2"] += (a * a / 8 + a * a / 4) * X0 ** 3 / 3
    I["E4"] += 1.5 * a ** 4 * X0 ** 3 / 3
    I["B0"] += (2 / PI) * a ** 3 * X0 ** 3 / 3
    tail = {}
    C = None
    if beta == 0.0:
        Fx, Px = 0.5 * (slo.sol(X) + shi.sol(X))
        # F = C/x^2 - C^3/(21 x^6) + D x : solve for C (D is the residual growing mode)
        def resid(C):
            Fm = C / X ** 2 - C ** 3 / (21 * X ** 6)
            Pm = -2 * C / X ** 3 + 6 * C ** 3 / (21 * X ** 7)
            D = (Fx - Fm) / X
            return Px - (Pm + D)
        C = brentq(resid, 1.0, 20.0)
        C2, C4 = C * C, C ** 4
        # leading + first corrections, integrated analytically from X to infinity
        # e2: x^2F'^2/8 + s^2/4 with F = C/x^2 - C^3/(21x^6):
        #   x^2F'^2/8 = C^2/(2x^4) - (2*6/21)C^4/(8 x^8)*... keep O(x^-8) terms
        #   F'  = -2C/x^3 + 6C^3/(21x^7);  F'^2 = 4C^2/x^6 - 24C^4/(21 x^10)
        #   x^2F'^2/8 = C^2/(2x^4) - 3C^4/(21 x^8)
        #   s^2 = F^2 - F^4/3 = C^2/x^4 - 2C^4/(21x^8) - C^4/(3x^8)
        tail["E2"] = C2 / (2 * 3 * X ** 3) - 3 * C4 / (21 * 7 * X ** 7) \
            + 0.25 * (C2 / (3 * X ** 3) - (2 / 21 + 1 / 3) * C4 / (7 * X ** 7))
        #   e4 = s^2F'^2 + s^4/(2x^2) = 4C^4/x^10 + C^4/(2 x^10)
        tail["E4"] = 4.5 * C4 / (9 * X ** 9)
        tail["E0"] = 0.0
        #   Lam: x^2 s^2 (1 + 4F'^2 + 4 s^2/x^2) = C^2/x^2 - (2/21+1/3) C^4/x^6 + 20 C^4/x^8
        tail["Lam"] = C2 / X - (2 / 21 + 1 / 3) * C4 / (5 * X ** 5) + 20 * C4 / (7 * X ** 7)
        #   b = -(2/pi) s^2 F' = (4/pi) C^3/x^7 (leading)
        tail["B0"] = (4 / PI) * C ** 3 / (6 * X ** 6)
        tail["B1"] = (4 / PI) * C ** 3 / (5 * X ** 5)
        tail["B2"] = (4 / PI) * C ** 3 / (4 * X ** 4)
        tail["B4"] = (4 / PI) * C ** 3 / (2 * X ** 2)
        #   x^2 eps = (3/4) C^2/x^2 + O(x^-6)
        tail["Ex2"] = 0.75 * C2 / X - (3 / 21 + 0.25 * (2 / 21 + 1 / 3)) * C4 / (5 * X ** 5)
        for k in tail:
            I[k] += tail[k]
    else:
        # Yukawa tail: linearised equation x^2F'' + 2xF' - 2F - beta^2 x^2 F = 0,
        # F = A k(x) + D g(x), k = e^{-bx}(1+bx)/x^2 (decaying), g = (bx cosh bx - sinh bx)/x^2
        Fx, Px = 0.5 * (slo.sol(X) + shi.sol(X))
        bb = beta
        def kf(x):
            return np.exp(-bb * x) * (1 + bb * x) / x ** 2
        def kp(x):
            return np.exp(-bb * x) * (-bb * (1 + bb * x) / x ** 2 + bb / x ** 2 - 2 * (1 + bb * x) / x ** 3)
        def gf(x):
            z = bb * x
            return (z * np.cosh(z) - np.sinh(z)) / x ** 2
        def gp(x):
            z = bb * x
            return (bb * np.cosh(z) + z * bb * np.sinh(z) - bb * np.cosh(z)) / x ** 2 - 2 * (z * np.cosh(z) - np.sinh(z)) / x ** 3
        Mtx = np.array([[kf(X), gf(X)], [kp(X), gp(X)]])
        A, D = np.linalg.solve(Mtx, [Fx, Px])
        xt, Wt = gl_grid(X, X + 80.0 / bb + 40.0, 200)
        Ft, Pt = A * kf(xt), A * kp(xt)
        e2t, e4t, e0t = dens(xt, Ft, Pt, beta)
        st = np.sin(Ft)
        bt = -(2 / PI) * st * st * Pt
        tail = {"E2": np.sum(Wt * e2t), "E4": np.sum(Wt * e4t), "E0": np.sum(Wt * e0t),
                "Lam": np.sum(Wt * xt * xt * st * st * (1 + 4 * (Pt * Pt + st * st / xt ** 2))),
                "B0": np.sum(Wt * bt), "B1": np.sum(Wt * xt * bt), "B2": np.sum(Wt * xt * xt * bt),
                "B4": np.sum(Wt * xt ** 4 * bt), "Ex2": np.sum(Wt * xt * xt * (e2t + e4t + e0t)),
                "A": float(A), "D_growing": float(D)}
        for k in ("E2", "E4", "E0", "Lam", "B0", "B1", "B2", "B4", "Ex2"):
            I[k] += tail[k]
    E = I["E2"] + I["E4"] + I["E0"]
    a1 = 4 * PI * E
    out = dict(beta=beta, slope0=a, slope_bracket=da, X_match=X, C_tail=C,
               a1=a1, E2=4 * PI * I["E2"], E4=4 * PI * I["E4"], E0=4 * PI * I["E0"],
               virial_E2_over_E4=I["E2"] / I["E4"],
               derrick_rel=(I["E2"] - I["E4"] + 3 * I["E0"]) / E,
               Lambda=I["Lam"], B=I["B0"],
               xB=np.sqrt(I["B2"]), xM=np.sqrt(I["B4"] / I["B2"]), xE=np.sqrt(I["Ex2"] / E),
               xmeanB=I["B1"], tails={k: float(v) for k, v in tail.items()})
    # half-baryon radius (F = pi/2) and 90 % energy radius
    def Fof(xx):
        return 0.5 * (slo.sol(xx)[0] + shi.sol(xx)[0])
    out["x_half"] = brentq(lambda xx: Fof(xx) - PI / 2, 0.05, min(X, 20.0), xtol=1e-14)
    xg, Wg = gl_grid(X0, X, 400)
    yy = 0.5 * (slo.sol(xg) + shi.sol(xg))
    e2, e4, e0 = dens(xg, yy[0], yy[1], beta)
    cum = np.cumsum(Wg * (e2 + e4 + e0)) / E
    out["x_E90"] = float(np.interp(0.9, cum, xg))
    out["C_tail_efpi_units"] = None if C is None else C / 4
    return out


def check_EL(beta=0.0):
    """Finite-difference check that rhs() is the Euler-Lagrange equation of eps."""
    rng = np.random.default_rng(1)
    x = 0.7 + rng.random(5)
    F = 1.0 + rng.random(5)
    P = -rng.random(5)
    h = 1e-6
    def e(F, P, x):
        e2, e4, e0 = dens(x, F, P, beta)
        return e2 + e4 + e0
    dE_dF = (e(F + h, P, x) - e(F - h, P, x)) / (2 * h)
    # d/dx (de/dP) along a path with F' = P and F'' = Q
    Q = np.array([rhs(xi, [Fi, Pi], beta)[1] for xi, Fi, Pi in zip(x, F, P)])
    def dEdP(F, P, x):
        return (e(F, P + h, x) - e(F, P - h, x)) / (2 * h)
    dt = 1e-5
    ddx = (dEdP(F + P * dt + 0.5 * Q * dt * dt, P + Q * dt, x + dt)
           - dEdP(F - P * dt + 0.5 * Q * dt * dt, P - Q * dt, x - dt)) / (2 * dt)
    return float(np.max(np.abs(ddx - dE_dF)))


def main():
    t0 = time.time()
    res = {"method": "own shooting (DOP853 rtol 1e-13) + bisection on F'(0); analytic C/x^2 - C^3/(21x^6) tail",
           "EL_check_max_residual": {"beta0": check_EL(0.0), "beta2": check_EL(2.0)}}
    print("Euler-Lagrange FD check (max |d/dx de/dF' - de/dF|):", res["EL_check_max_residual"])
    # massless: matching radius scan
    a, da, slo, shi, xv = solve_profile(0.0)
    print(f"beta=0: slope a = {a:.14f} (bracket {da:.1e}), trajectories agree to 1e-9 up to x = {xv:.1f}")
    scan = []
    for X in sorted({20.0, 30.0, 40.0, min(60.0, 0.9 * xv)}):
        ob = observables(0.0, a, da, slo, shi, X)
        scan.append(ob)
        print(f"  X={X:6.1f}: a1={ob['a1']:.10f} Lam={ob['Lambda']:.8f} xB={ob['xB']:.9f} "
              f"xM={ob['xM']:.9f} xE={ob['xE']:.9f} xh={ob['x_half']:.10f} C={ob['C_tail']:.6f} "
              f"E2/E4={ob['virial_E2_over_E4']:.10f} B={ob['B']:.12f}")
    best = scan[-1]
    spread = {k: float(max(abs(s[k] - best[k]) / abs(best[k]) for s in scan if s["X_match"] >= 30))
              for k in ("a1", "Lambda", "xB", "xM", "xE", "x_half")}
    print("  relative spread over the X values >= 30:", spread)
    res["massless"] = best
    res["massless_X_scan"] = [{k: s[k] for k in ("X_match", "a1", "Lambda", "xB", "xM", "xE", "x_half", "C_tail")}
                              for s in scan]
    res["massless_X_spread"] = spread
    c0 = {"B": best["a1"] * best["xB"], "half": best["a1"] * best["x_half"],
          "E": best["a1"] * best["xE"], "M": best["a1"] * best["xM"],
          "meanB": best["a1"] * best["xmeanB"], "E90": best["a1"] * best["x_E90"]}
    res["c0"] = c0
    print("  c0 =", {k: round(v, 5) for k, v in c0.items()})
    # pion-mass family
    fam = []
    for beta in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0):
        a_hi = 40.0 if beta < 8 else 200.0
        a_b, da_b, slo_b, shi_b, xv_b = solve_profile(beta, xmax=60.0 / np.sqrt(1 + beta), a_hi=a_hi)
        ob = observables(beta, a_b, da_b, slo_b, shi_b, xv_b)
        Fend = 0.5 * (slo_b.sol(xv_b)[0] + shi_b.sol(xv_b)[0])
        ob["F_at_X"] = float(Fend)
        ob["c0_B"] = ob["a1"] * ob["xB"]
        ob["c0_half"] = ob["a1"] * ob["x_half"]
        fam.append(ob)
        print(f"beta={beta:5.2f}: a1={ob['a1']:.8f} xB={ob['xB']:.8f} c0_B={ob['c0_B']:.6f} "
              f"c0_half={ob['c0_half']:.6f} derrick={ob['derrick_rel']:.1e} X={xv_b:.2f} F(X)={Fend:.1e} B={ob['B']:.10f}")
    res["pion_mass_family"] = [{k: v for k, v in f.items() if k != "tails"} for f in fam]
    res["runtime_s"] = time.time() - t0
    with open("x2_hedgehog.json", "w") as fh:
        json.dump(res, fh, indent=1, default=float)
    print(f"done in {res['runtime_s']:.1f} s")


if __name__ == "__main__":
    main()
