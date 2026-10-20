#!/usr/bin/env python3
"""
E3 part 2: the B = 1 hedgehog profile (own solver), mass, virial, I1 and I2 from the
radial formulas.  Used by the inertia, spectrum and stability scripts.

Skyrme model, L = (F^2/16) Tr(d_mu U d^mu U^+) + (1/32 e^2) Tr[L_mu, L_nu]^2,
F = F_pi in the 186-MeV convention, x = e F r.  Hedgehog U = exp(i F(r) n.tau).
Energy  M = (4 pi F/e) int dx [ x^2 F'^2/8 + s^2/4 + s^4/(2 x^2) + s^2 F'^2 ],  s = sin F
ODE     (x^2 + 8 s^2) F'' + 2 x F' + 4 sin2F F'^2 - sin2F - 4 s^2 sin2F / x^2 = 0
        F(0) = pi,  F ~ C/x^2 - C^3/(21 x^6)  (x -> infinity)
Radial formulas (to be compared with the 3D quadrature of e3_inertia.py):
  I1 = (2 pi/3) Lambda / (e^3 F),  Lambda = int x^2 s^2 [1 + 4 (F'^2 + s^2/x^2)] dx     (ANW)
  I2 = (pi/2) / (e^3 F) int x^2 (1 - cos F) (1 + F'^2 + 2 s^2/x^2) dx                    (Kopeliovich)

Writes profile_e3.npz and hedgehog_results.json.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp, solve_bvp, quad
from scipy.optimize import brentq
from scipy.interpolate import CubicHermiteSpline

X0 = 1e-5


def rhs(x, y):
    F, dF = y
    s, s2F = np.sin(F), np.sin(2 * F)
    ddF = -(2 * x * dF + 4 * s2F * dF**2 - s2F - 4 * s**2 * s2F / x**2) / (x**2 + 8 * s**2)
    return np.vstack([dF, ddF]) if np.ndim(F) else np.array([dF, ddF])


def shoot(a, X=30.0):
    def ev_neg(x, y): return y[0] + 0.05
    ev_neg.terminal = True
    def ev_up(x, y): return y[1] - 1e-3 if x > 0.5 else -1.0
    ev_up.terminal = True
    sol = solve_ivp(rhs, (X0, X), [np.pi - a * X0, -a], method='DOP853', rtol=1e-12, atol=1e-14,
                    events=[ev_neg, ev_up])
    if sol.t_events[0].size:
        return +1.0   # overshoot: crosses zero -> slope too steep
    if sol.t_events[1].size:
        return -1.0   # turns back up -> too shallow
    x, F, dF = sol.t[-1], sol.y[0, -1], sol.y[1, -1]
    return x * dF + 2 * F


def solve_profile(X, xm=3.0):
    """two-sided shooting: outward from x = X0 with slope -a, inward from x = X with the
    asymptotic form F = C/x^2 - C^3/(21 x^6); match F and F' at xm (both directions stable)."""
    a0 = brentq(lambda a: shoot(a, 25.0), 0.5, 1.5, xtol=1e-12)
    opts = dict(method='DOP853', rtol=1e-13, atol=1e-15, dense_output=True)

    def out(a):
        return solve_ivp(rhs, (X0, xm), [np.pi - a * X0, -a], **opts)

    def inn(C):
        F = C / X**2 - C**3 / (21 * X**6)
        dF = -2 * C / X**3 + 6 * C**3 / (21 * X**7)
        return solve_ivp(rhs, (X, xm), [F, dF], **opts)

    def resid(p):
        o, i = out(p[0]), inn(p[1])
        return np.array([o.y[0, -1] - i.y[0, -1], o.y[1, -1] - i.y[1, -1]])

    p = np.array([a0, 8.0])
    for it in range(30):                      # Newton with finite-difference Jacobian
        r = resid(p)
        Jm = np.zeros((2, 2))
        for k in range(2):
            dp = np.zeros(2); dp[k] = 1e-7 * max(1.0, abs(p[k]))
            Jm[:, k] = (resid(p + dp) - resid(p - dp)) / (2 * dp[k])
        step = np.linalg.solve(Jm, -r)
        p = p + step
        if np.abs(step).max() < 1e-14 * max(1, np.abs(p).max()):
            break
    o, i = out(p[0]), inn(p[1])

    class Sol:
        pass
    sol = Sol()
    sol.a, sol.C, sol.match_resid = p[0], p[1], float(np.abs(resid(p)).max())

    def ev(x):
        x = np.atleast_1d(np.asarray(x, float))
        res = np.empty((2, x.size))
        m = x <= xm
        if m.any():
            res[:, m] = o.sol(np.clip(x[m], X0, xm))
        if (~m).any():
            res[:, ~m] = i.sol(np.clip(x[~m], xm, X))
        return res
    sol.sol = lambda x: ev(x) if np.ndim(x) else ev(x)[:, 0]
    sol.x = np.concatenate([o.t, i.t])
    return sol, a0


def tail_C(FX, X):
    # F(X) = C/X^2 - C^3/(21 X^6)
    return brentq(lambda C: C / X**2 - C**3 / (21 * X**6) - FX, 0.5 * FX * X**2, 2 * FX * X**2)


class Profile:
    def __init__(self, sol, X):
        self.sol, self.X = sol, X
        self.C = sol.C

    def __call__(self, x):
        x = np.asarray(x, float)
        inside = x <= self.X
        xi = np.clip(x, X0, self.X)
        F_in, dF_in = self.sol.sol(xi)
        xo = np.maximum(x, self.X)
        F_out = self.C / xo**2 - self.C**3 / (21 * xo**6)
        dF_out = -2 * self.C / xo**3 + 6 * self.C**3 / (21 * xo**7)
        # below X0: linear in x
        F_in = np.where(x < X0, np.pi + self.sol.sol(X0)[1] * x, F_in)
        dF_in = np.where(x < X0, self.sol.sol(X0)[1], dF_in)
        return np.where(inside, F_in, F_out), np.where(inside, dF_in, dF_out)


def integrals(prof):
    def integ(fun):
        tot = 0.0
        edges = [0, 0.5, 1, 2, 3, 5, 8, 12, 20, 35] + [e for e in (40, 50, 65, 80, 100, 130, 160) if e < prof.X] + [prof.X]
        for a, b in zip(edges[:-1], edges[1:]):
            if b <= prof.X:
                tot += quad(fun, a, b, epsabs=1e-13, epsrel=1e-12, limit=400)[0]
        # tail: substitute t = 1/x (the integrands fall off like 1/x^2)
        tot += quad(lambda t: fun(1.0 / t) / t**2 if t > 0 else 0.0, 0.0, 1.0 / prof.X,
                    epsabs=1e-14, epsrel=1e-12, limit=400)[0]
        return tot

    def e2(x):
        F, d = prof(x); s = np.sin(F)
        return 4 * np.pi * (x**2 * d**2 / 8 + s**2 / 4)

    def e4(x):
        F, d = prof(x); s = np.sin(F)
        return 4 * np.pi * (s**4 / (2 * x**2) + s**2 * d**2) if x > 0 else 4 * np.pi * (s**2 * d**2)

    def lam(x):
        F, d = prof(x); s = np.sin(F)
        return x**2 * s**2 * (1 + 4 * (d**2 + (s**2 / x**2 if x > 0 else d**2)))

    def i2(x):
        F, d = prof(x); s = np.sin(F)
        return x**2 * 2 * np.sin(F / 2)**2 * (1 + d**2 + (2 * s**2 / x**2 if x > 0 else 2 * d**2))

    def bar(x):
        F, d = prof(x)
        return -(2 / np.pi) * np.sin(F)**2 * d

    def r2(x):  # isoscalar (baryon) mean square radius
        F, d = prof(x)
        return -(2 / np.pi) * x**2 * np.sin(F)**2 * d

    E2, E4 = integ(e2), integ(e4)
    Lam, J2, B, R2 = integ(lam), integ(i2), integ(bar), integ(r2)
    return dict(E2=E2, E4=E4, M=E2 + E4, Lambda=Lam, I1=2 * np.pi / 3 * Lam, I2_radial=np.pi / 2 * J2,
                I2_integral=J2, B=B, r2_baryon=R2)


if __name__ == "__main__":
    res = {}
    runs = {}
    for X in (40.0, 80.0, 160.0):
        sol, a_shoot = solve_profile(X)
        prof = Profile(sol, X)
        I = integrals(prof)
        I["slope_F'(0)"] = float(sol.sol(X0)[1])
        I["slope_shooting"] = -a_shoot
        I["C_tail"] = prof.C
        I["nodes"] = int(sol.x.size)
        I["match_residual"] = sol.match_resid
        runs[X] = (sol, prof, I)
        slope = I["slope_F'(0)"]
        print(f"X={X:6.1f}: F'(0)={slope:.8f}  M={I['M']:.8f}  "
              f"E2={I['E2']:.8f} E4={I['E4']:.8f}  Lambda={I['Lambda']:.6f}  I2={I['I2_radial']:.6f}  "
              f"B={I['B']:.10f}  C={prof.C:.5f}  nodes={I['nodes']}")
    sol, prof, I = runs[160.0]
    res["convergence_in_X"] = {str(k): v[2] for k, v in runs.items()}
    res["final"] = I
    res["M_over_3pi2"] = I["M"] / (3 * np.pi**2)
    res["virial_E2_minus_E4_rel"] = (I["E2"] - I["E4"]) / I["M"]
    # literature checks (E2 targets, re-derived here as calibration of this solver)
    tgt = {"M_cl [F/e]": (I["M"], 1.2315 * 3 * np.pi**2, 0.002, "relative"),
           "Lambda": (I["Lambda"], 50.9, 0.005, "relative"),
           "I2 [1/(e^3 F)] vs arctan-ansatz 40.5": (I["I2_radial"], 40.5, 0.015, "relative"),
           "B": (I["B"], 1.0, 1e-8, "absolute"),
           "virial E2=E4": (res["virial_E2_minus_E4_rel"], 0.0, 1e-4, "absolute")}
    res["calibration"] = {}
    for k, (v, t, tol, kind) in tgt.items():
        dev = abs(v - t) / abs(t) if kind == "relative" else abs(v - t)
        res["calibration"][k] = dict(ours=v, target=t, tol=tol, kind=kind, deviation=dev, pass_=bool(dev <= tol))
        print(f"{'PASS' if dev <= tol else 'FAIL'} {k}: ours {v:.6f} target {t:.6f} dev {dev:.2e} tol {tol}")
    # physical units at ANW parameters
    Fpi, e = 129.0, 5.45
    hbarc = 197.3269804
    res["ANW"] = dict(F_pi_MeV=Fpi, e=e, M_MeV=I["M"] * Fpi / e,
                      inv_I1_MeV=e**3 * Fpi / I["I1"], inv_I2_MeV=e**3 * Fpi / I["I2_radial"],
                      I1_fm=I["I1"] / (e**3 * Fpi) * hbarc, I2_fm=I["I2_radial"] / (e**3 * Fpi) * hbarc,
                      N_mass_MeV=I["M"] * Fpi / e + 0.375 * e**3 * Fpi / I["I1"],
                      Delta_mass_MeV=I["M"] * Fpi / e + 1.875 * e**3 * Fpi / I["I1"])
    print("ANW units:", {k: round(v, 3) for k, v in res["ANW"].items()})
    # dense table for the other scripts (cubic Hermite with exact derivatives)
    xt = np.concatenate([np.linspace(0, 1, 2001), np.linspace(1, 10, 9001)[1:], np.linspace(10, 40, 6001)[1:],
                         np.linspace(40, 160, 2401)[1:]])
    Ft, dFt = prof(xt)
    ddFt = np.array([rhs(x, [F, d])[1] if x >= 1e-3 else 0.0 for x, F, d in zip(xt, Ft, dFt)])
    # near the origin the ODE right-hand side cancels to O(x^3)/O(x^2): use F'' = 6 b x from the
    # exact profile instead (F = pi - a x + b x^3, F'' is odd in x and vanishes at x = 0)
    small = (xt > 0) & (xt < 1e-3)
    h = 1e-5
    ddFt[small] = (prof(xt[small] + h)[1] - prof(np.maximum(xt[small] - h, X0))[1]) / \
        (xt[small] + h - np.maximum(xt[small] - h, X0))
    np.savez("profile_e3.npz", x=xt, F=Ft, dF=dFt, ddF=ddFt, C=prof.C, X=160.0)
    # interpolation self-test
    hs = CubicHermiteSpline(xt, Ft, dFt)
    xm = 0.5 * (xt[1:] + xt[:-1])
    err = np.abs(hs(xm) - prof(xm)[0]).max()
    hd = CubicHermiteSpline(xt, dFt, ddFt)
    errd = np.abs(hd(xm) - prof(xm)[1]).max()
    res["table_interp_max_err"] = float(err)
    res["table_interp_max_err_dF"] = float(errd)
    print(f"table interpolation max error F {err:.2e}, F' {errd:.2e}")
    with open("hedgehog_results.json", "w") as fh:
        json.dump(res, fh, indent=1, default=float)
