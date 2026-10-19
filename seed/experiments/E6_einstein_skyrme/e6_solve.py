#!/usr/bin/env python3
"""E6: a fold with gravity -- hedgehog Einstein-Skyrme solutions, both branches, alpha_crit, ADM mass,
equivalence-principle (O(alpha)) check, physical-scale numbers.

Run:  NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 e6_solve.py
Each stage writes its result into out/stage_<name>.json and is skipped on re-run if that file exists
(delete out/ to recompute everything).  Deterministic (no random numbers).
"""
import json
import math
import os
import sys
import time

import numpy as np
from scipy.integrate import solve_bvp
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import es_core as ec  # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:7.1f}s]", *a, flush=True)


def stage(name, fn):
    path = os.path.join(OUT, f"stage_{name}.json")
    if os.path.exists(path):
        with open(path) as fh:
            log(f"stage {name}: loaded checkpoint")
            return json.load(fh)
    log(f"stage {name}: computing")
    res = fn()
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1)
    log(f"stage {name}: done")
    return res


# ------------------------------------------------------------------ helpers
def first_flip(b, h=ec.DEFAULT['h'], xmax=ec.DEFAULT['xmax']):
    """Smallest alpha (scanned upward from 0) at which the shooting class at fixed b changes from -1."""
    if ec.classify(b, 0.0, h, xmax) != -1:
        raise ValueError(f"class at alpha=0 is not overshoot for b={b}")
    a_prev, a = 0.0, 1e-7
    while a < 0.5:
        c = ec.classify(b, a, h, xmax)
        if c != -1:
            return a_prev, a
        a_prev = a
        a = a * 1.05 if a < 0.01 else a + 0.0005
    raise ValueError("no flip found")


def alpha_of_b(b, h=ec.DEFAULT['h'], xmax=ec.DEFAULT['xmax']):
    lo, hi = first_flip(b, h, xmax)
    return ec.bisect_alpha(b, lo, hi, h, xmax)[0]


def simpson_t(y, h):
    """Composite Simpson on a uniform grid (len odd); falls back to dropping the last point if even."""
    n = len(y)
    if n % 2 == 0:
        return simpson_t(y[:-1], h) + 0.5 * h * (y[-2] + y[-1])
    return h / 3.0 * (y[0] + y[-1] + 4.0 * y[1:-1:2].sum() + 2.0 * y[2:-1:2].sum())


def cumtrapz(y, x):
    out = np.zeros_like(y)
    out[1:] = np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))
    return out


def flat_densities(x, F, P):
    s2 = np.sin(F)**2
    lam_r, lam_t = P**2, s2 / x**2
    rho = 0.5 * (lam_r + 2 * lam_t) + 0.5 * (2 * lam_r * lam_t + lam_t**2)
    p_r = 2 * lam_r * (0.5 + lam_t) - rho
    p_t = lam_t * (1 + lam_r + lam_t) - rho
    return rho, p_r, p_t


# ------------------------------------------------------------------ stage 1: flat skyrmion
def stage_flat():
    res = {"convergence": []}
    for h in [4e-3, 2e-3, 1e-3, 5e-4]:
        for xmax in [1e5, 1e6]:
            b, _, _ = ec.bisect_b(0.0, 1.8, 2.2, h, xmax)
            o = ec.observables(b, 0.0, h, xmax)
            res["convergence"].append(dict(h=h, xmax=xmax, b=b, m_inf=o["m_inf"], C=o["C"]))
            log(f"  flat h={h} xmax={xmax:.0e}: b={b:.15f} m={o['m_inf']:.15f} C={o['C']:.12f}")
    best = [r for r in res["convergence"] if r["h"] == 5e-4 and r["xmax"] == 1e6][0]
    res.update(b_flat=best["b"], m0=best["m_inf"], C_flat=best["C"])
    # virial on the dense profile: E2 = E4
    x, F, P, m, ls = ec.profile(best["b"], 0.0, 5e-4, ec.x0_for(best["b"]), 2e3)
    s2 = np.sin(F)**2
    e2 = 0.5 * P**2 * x**2 + s2
    e4 = s2 * P**2 + s2**2 / (2 * x**2)
    hh = np.log(x[1] / x[0])
    E2 = simpson_t(e2 * x, hh)
    E4 = simpson_t(e4 * x, hh)
    # pieces outside the grid: core [0, x0] from the series (x^2 rho2 ~ 3b^2 x^2/2, x^2 rho4 ~ 3b^4 x^2/2) and
    # tail beyond x_end (F = C/x^2: e2 ~ 3C^2/x^4, e4 ~ O(x^-8))
    b0, x0 = best["b"], x[0]
    E2 += 0.5 * b0**2 * x0**3 + best["C"]**2 / x[-1]**3
    E4 += 0.5 * b0**4 * x0**3
    res.update(E2=E2, E4=E4, virial=E2 / E4 - 1, m_from_quadrature=E2 + E4)
    return res


# ------------------------------------------------------------------ stage 2: alpha_crit by maximisation
def stage_crit():
    res = {"runs": []}
    for h, xmax in [(2e-3, 1e6), (1e-3, 1e6), (5e-4, 1e6), (1e-3, 1e5), (1e-3, 1e7)]:
        f = lambda b: -alpha_of_b(b, h, xmax)
        opt = minimize_scalar(f, bounds=(2.7, 3.2), method="bounded", options=dict(xatol=1e-9, maxiter=200))
        bc = opt.x
        ac = -opt.fun
        # parabola through points around the maximum as a second estimate
        db = 2e-3
        bs = bc + db * np.arange(-3, 4)
        als = np.array([alpha_of_b(bb, h, xmax) for bb in bs])
        c = np.polyfit(bs - bc, als, 4)
        p = np.poly1d(c)
        dp = p.deriv()
        roots = [r.real for r in dp.r if abs(r.imag) < 1e-12 and abs(r.real) < 3 * db]
        bpar = bc + roots[0]
        apar = p(roots[0])
        o = ec.observables(bc, ac, h, xmax)
        res["runs"].append(dict(h=h, xmax=xmax, alpha_crit=ac, b_crit=bc, alpha_crit_polyfit=float(apar),
                                b_crit_polyfit=float(bpar), curvature=float(c[2]), m_inf=o["m_inf"],
                                sigma0=o["sigma0"], Nmin=o["Nmin"], xNmin=o["xNmin"], C=o["C"],
                                nfev=int(opt.nfev)))
        log(f"  h={h} xmax={xmax:.0e}: alpha_crit={ac:.15f} b_crit={bc:.9f} polyfit={apar:.15f} "
            f"m={o['m_inf']:.10f} sigma0={o['sigma0']:.8f} Nmin={o['Nmin']:.8f}")
    r = {(q["h"], q["xmax"]): q for q in res["runs"]}
    a1, a2, a3 = r[(2e-3, 1e6)]["alpha_crit"], r[(1e-3, 1e6)]["alpha_crit"], r[(5e-4, 1e6)]["alpha_crit"]
    res["richardson_rk4"] = a3 + (a3 - a2) / 15.0
    res["observed_order"] = math.log(abs((a1 - a2) / (a2 - a3)), 2) if a2 != a3 else float("nan")
    return res


# ------------------------------------------------------------------ stage 3: branch curve alpha(b)
def stage_branch(b_flat):
    bs = list(b_flat + np.array([1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 2e-2, 4e-2, 6e-2, 8e-2]))
    bs += list(np.round(np.arange(2.10, 4.0001, 0.05), 6)) + list(np.round(np.arange(4.2, 10.0001, 0.2), 6))
    bs += list(np.round(np.geomspace(10.5, 200.0, 30), 6))
    rows = []
    for b in bs:
        a = alpha_of_b(b)
        o = ec.observables(b, a)
        rows.append(o)
    log(f"  {len(rows)} points; max alpha on grid = {max(r['alpha'] for r in rows):.9f}")
    return {"rows": rows}


# ------------------------------------------------------------------ stage 4: fixed-alpha shooting on b
def stage_fixed_alpha(branch, crit):
    rows = branch["rows"]
    bc = crit["runs"][2]["b_crit"]
    pts = sorted([(r["b"], r["alpha"]) for r in rows] + [(bc, crit["runs"][2]["alpha_crit"])])
    bs = np.array([p[0] for p in pts])
    als = np.array([p[1] for p in pts])
    ic = int(np.argmax(als))
    out = []
    for a in [1e-3, 5e-3, 1e-2, 2e-2, 3e-2, 3.5e-2, 4e-2, 4.03e-2, 4.037e-2]:
        sols = {}
        for name, sl in [("lower", slice(0, ic + 1)), ("upper", slice(ic, None))]:
            bb, aa = bs[sl], als[sl]
            # bracket: neighbouring grid points with alpha on either side of a
            idx = [i for i in range(len(aa) - 1) if (aa[i] - a) * (aa[i + 1] - a) <= 0]
            if not idx:
                continue
            i = idx[0]
            lo, hi = bb[i], bb[i + 1]
            if name == "lower":
                hi = min(hi, bc)
            else:
                lo = max(lo, bc)
            # classes at the ends must differ (overshoot on the inner side of the curve)
            try:
                b_sol, _, _ = ec.bisect_b(a, lo, hi)
            except ValueError as err:
                log("   ", name, a, err)
                continue
            o = ec.observables(b_sol, a)
            o["alpha_of_b_check"] = alpha_of_b(b_sol)
            sols[name] = o
        out.append(dict(alpha=a, **sols))
        msg = "  alpha=%.5f " % a + " ".join(f"{k}: b={v['b']:.10f} m={v['m_inf']:.9f}" for k, v in sols.items())
        log(msg)
    return {"rows": out}


# ------------------------------------------------------------------ stage 5: BVP cross-check of alpha_crit
def stage_bvp(crit, X=200.0, tol=1e-9):
    def odefun(t, y, p):
        al = p[0]
        x = np.exp(t)
        F, Q, m = y
        P = Q / x
        s = np.sin(F)
        s2 = s * s
        s2F = np.sin(2 * F)
        N = 1 - 2 * al * m / x
        A = x * x + 2 * s2
        mp = 0.5 * N * P * P * A + s2 * (1 + s2 / (2 * x * x))
        Np = -2 * al * (mp / x - m / (x * x))
        sr = al / x * A * P * P
        Ap = 2 * x + 2 * s2F * P
        Fpp = (s2F * (1 + N * P * P + s2 / (x * x)) - (sr * N * A + Np * A + N * Ap) * P) / (N * A)
        return np.vstack([Q, Q + x * x * Fpp, x * mp])

    def make_bc(b, x0):
        def bc(ya, yb, p):
            Fs, Ps, ms, _ = ec.series_start(b, p[0], x0)
            return np.array([ya[0] - Fs, ya[1] - x0 * Ps, ya[2] - ms,
                             yb[1] + (2 + 2 * p[0] * yb[2] / X) * yb[0]])
        return bc

    cache = {}

    def solve_at(b):
        x0 = ec.x0_for(b)
        a_guess = alpha_of_b(b)
        xs, F, P, m, ls = ec.profile(b, a_guess, 2e-3, x0, X)
        t = np.log(xs)
        sel = np.unique(np.concatenate([np.arange(0, len(t), 40), [len(t) - 1]]))
        y0 = np.vstack([F[sel], (xs * P)[sel], m[sel]])
        sol = solve_bvp(odefun, make_bc(b, x0), t[sel], y0, p=[a_guess], tol=tol, max_nodes=200000)
        cache[b] = (sol.status, sol.p[0], a_guess, len(sol.x))
        return sol.p[0], sol.status

    f = lambda b: -solve_at(b)[0]
    opt = minimize_scalar(f, bounds=(2.8, 3.1), method="bounded", options=dict(xatol=1e-7, maxiter=100))
    a_c, status = solve_at(opt.x)
    st = cache[opt.x]
    log(f"  BVP X={X} tol={tol}: alpha_crit={a_c:.12f} at b={opt.x:.8f} (status {status}, nodes {st[3]}; "
        f"shooting alpha at that b {st[2]:.12f})")
    return dict(X=X, tol=tol, alpha_crit=float(a_c), b_crit=float(opt.x), status=int(status),
                nodes=int(st[3]), shooting_alpha_same_b=float(st[2]))


# ------------------------------------------------------------------ stage 6: equivalence principle / O(alpha)
def stage_ep(flat):
    b0, m0 = flat["b_flat"], flat["m0"]
    h = 5e-4
    # full nonlinear lower-branch solutions at small alpha (fixed-alpha shooting on b)
    alphas = [2e-4 * j for j in range(1, 11)]
    full = []
    for a in alphas:
        b, _, _ = ec.bisect_b(a, b0 - 0.05, b0 + 0.05, h)
        o = ec.observables(b, a, h)
        full.append(dict(alpha=a, b=b, m_inf=o["m_inf"], sigma0=o["sigma0"]))
    A = np.array(alphas)
    D = (np.array([r["m_inf"] for r in full]) - m0) / A
    fits = {}
    for deg in [2, 3, 4]:
        c = np.polyfit(A, D, deg)
        fits[f"deg{deg}"] = dict(m1=float(c[-1]), m2=float(c[-2]))
    # first-order integrals on the flat profile
    x, F, P, m, ls = ec.profile(b0, 0.0, h, ec.x0_for(b0), 2e4)
    hh = np.log(x[1] / x[0])
    rho, p_r, p_t = flat_densities(x, F, P)
    C = F[-1] * x[-1]**2
    # (i) Newtonian, Phi from Poisson: lap(phi) = rho~ (phi = Phi/alpha), phi(inf) = 0
    #     radial Green's-function solution phi(x) = -[m(x)/x + int_x^inf rho~ y dy]
    inner = m / x
    outer_int = rho * x * x       # integrand of int rho y dy in t (dy = y dt)
    rev = np.concatenate([[0.0], np.cumsum(0.5 * (outer_int[1:] + outer_int[:-1]) * hh)])
    outer = rev[-1] - rev + C**2 / (x[-1]**4) * 0.75   # tail of int rho y dy beyond x_max (rho ~ 3C^2/x^6)
    phi = -(inner + outer)
    # check Poisson's equation directly: (x^2 phi')' = x^2 rho
    dphi = np.gradient(phi, x)
    lhs = np.gradient(x**2 * dphi, x)
    sel = (x > 0.05) & (x < 50)
    poisson_resid = float(np.max(np.abs(lhs[sel] - x[sel]**2 * rho[sel]) / np.max(x[sel]**2 * rho[sel])))
    m1_N = 0.5 * simpson_t(x**2 * rho * phi * x, hh)           # (1/2) int rho Phi d^3x in units 4 pi f/e, per alpha
    m1_N_alt = -simpson_t(m * x * rho * x, hh)                  # -int m x rho~ dx  (identity check)
    # (ii) GR first order, Schwarzschild gauge: dM = -G int (rho + p_r) m/r dV
    m1_GR = -simpson_t((m / x) * x**2 * (rho + p_r) * x, hh)
    # (iii) linearised gravity in harmonic gauge (one-graviton exchange between stress tensors):
    #   dE = -G int int [rho rho'/2 + (rho p' + p rho')/2 + p_ij p'_ij - p p'/2] / |x - y|,  p = p_ii
    p_tr = p_r + 2 * p_t
    Dl = p_r - p_t
    w = x**3      # r^2 dr = x^3 dt

    def K0(a, bfun):
        cin = np.concatenate([[0.0], np.cumsum(0.5 * ((bfun * w)[1:] + (bfun * w)[:-1]) * hh)])
        g = bfun * x * x
        cout = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * hh)])
        cout = cout[-1] - cout
        pot = cin / x + cout
        return simpson_t(a * w * pot, hh)

    def K2(a, bfun):
        g1 = bfun * x**5
        cin = np.concatenate([[0.0], np.cumsum(0.5 * (g1[1:] + g1[:-1]) * hh)])
        g2 = bfun   # int b r'^2 / r'^3 * r'^... : int_r^inf b(r') r'^2 r^2/r'^3 dr' = r^2 int b/r' dr' = r^2 int b dt
        cout = np.concatenate([[0.0], np.cumsum(0.5 * (g2[1:] + g2[:-1]) * hh)])
        cout = cout[-1] - cout
        pot = cin / x**3 + x**2 * cout
        return simpson_t(a * w * pot, hh)

    S = 0.5 * K0(rho, rho) + K0(rho, p_tr) + (3 * K0(p_t, p_t) + 2 * K0(p_t, Dl) + K0(Dl, Dl) / 3.0
                                              + (2.0 / 15.0) * K2(Dl, Dl)) - 0.5 * K0(p_tr, p_tr)
    m1_lin = -S          # (4 pi)^2 from the angular integrals cancels 1/(16 pi^2): m1 = -(1/16pi^2) * (4pi)^2 * S
    breakdown = dict(rho_rho=-0.5 * K0(rho, rho), rho_p=-K0(rho, p_tr),
                     pij_pij=-(3 * K0(p_t, p_t) + 2 * K0(p_t, Dl) + K0(Dl, Dl) / 3.0 + (2.0 / 15.0) * K2(Dl, Dl)),
                     p_p=0.5 * K0(p_tr, p_tr))
    sel2 = x < 50
    pr_min_over_rho_max = float(np.min(p_r[sel2]) / np.max(rho[sel2]))
    pr_max_over_rho_max = float(np.max(p_r[sel2]) / np.max(rho[sel2]))
    laue = simpson_t(x**2 * p_tr * x, hh) / simpson_t(x**2 * np.abs(p_tr) * x, hh)
    pr_frac = simpson_t((m / x) * x**2 * p_r * x, hh) / simpson_t((m / x) * x**2 * rho * x, hh)
    res = dict(full=full, fits=fits, m1_full=fits["deg3"]["m1"], m1_newton=m1_N, m1_newton_identity=m1_N_alt,
               m1_GR_first_order=m1_GR, m1_linearised_harmonic=m1_lin, poisson_residual=poisson_resid,
               von_laue_ratio=laue, pr_over_rho_weighted=pr_frac, exchange_breakdown=breakdown,
               pr_min_over_rho_max=pr_min_over_rho_max, pr_max_over_rho_max=pr_max_over_rho_max,
               pr_centre_over_rho_centre=float(p_r[0] / rho[0]),
               newton_vs_full_rel=(m1_N - fits["deg3"]["m1"]) / fits["deg3"]["m1"],
               GR_vs_full_rel=(m1_GR - fits["deg3"]["m1"]) / fits["deg3"]["m1"],
               lin_vs_full_rel=(m1_lin - fits["deg3"]["m1"]) / fits["deg3"]["m1"],
               sigma0_slope_full=float(np.polyfit(A, np.log(np.array([r["sigma0"] for r in full])) / A, 2)[-1]),
               sigma0_slope_first_order=-simpson_t((x**2 + 2 * np.sin(F)**2) * P**2 / x * x, hh))
    log(f"  m1: full={res['m1_full']:.8f} GR1={m1_GR:.8f} lin={m1_lin:.8f} Newton={m1_N:.8f} ({m1_N_alt:.8f}); "
        f"Newton/full-1={res['newton_vs_full_rel']:+.4%}  GR1/full-1={res['GR_vs_full_rel']:+.2e} "
        f"lin/full-1={res['lin_vs_full_rel']:+.2e}; von Laue {laue:.1e}; Poisson resid {poisson_resid:.1e}")
    return res


# ------------------------------------------------------------------ stage 7: upper branch -> Bartnik-McKinnon
def stage_bm(branch):
    # Bartnik-McKinnon (Einstein-Yang-Mills, first solution) by shooting, in BM units:
    #   m' = N w'^2 + (1-w^2)^2/(2 r^2), (sigma N w')' = sigma w (w^2-1)/r^2, sigma'/sigma = 2 w'^2/r
    from scipy.integrate import solve_ivp

    def rhs(r, y):
        w, wp, m = y
        N = 1 - 2 * m / r
        mp = N * wp**2 + (1 - w * w)**2 / (2 * r * r)
        sr = 2 * wp**2 / r
        Np = -2 * (mp / r - m / r**2)
        wpp = (w * (w * w - 1) / r**2 - (sr * N + Np) * wp) / N
        return [wp, wpp, mp]

    def cls(bb, rmax=2e4):
        r0 = 1e-4
        y0 = [1 - bb * r0**2, -2 * bb * r0, 2 * bb**2 * r0**3]
        ev1 = lambda r, y: y[0] + 1.0
        ev1.terminal = True
        ev2 = lambda r, y: y[1]
        ev2.terminal = True
        ev3 = lambda r, y: 1 - 2 * y[2] / r - 1e-12
        ev3.terminal = True
        s = solve_ivp(rhs, [r0, rmax], y0, method="DOP853", rtol=1e-12, atol=1e-14, events=[ev1, ev2, ev3])
        if s.t_events[0].size:
            return -1, s
        if s.t_events[1].size and s.y_events[1][0][0] > -1:
            return +1, s
        if s.t_events[2].size:
            return 2, s
        return (1 if s.y[0, -1] > -1 and s.y[1, -1] < 0 and False else 0), s

    lo, hi = 0.40, 0.50
    clo, chi = cls(lo)[0], cls(hi)[0]
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        c = cls(mid)[0]
        if c == clo:
            lo = mid
        else:
            hi = mid
    if clo == chi:
        raise ValueError("BM bracket does not change class")
    c, s = cls(0.5 * (lo + hi), rmax=2e3)
    # mass at large r: w ~ -1 + c/r, so m(inf) = m(R) + c^2/R^3; evaluate at several R as a check
    m_R = []
    for R in [50.0, 100.0, 200.0]:
        i = np.argmin(np.abs(s.t - R))
        cR = (s.y[0, i] + 1) * s.t[i]
        m_R.append(s.y[2, i] + cR**2 / s.t[i]**3)
    m_bm = m_R[-1]
    log(f"  BM mass with tail at R=50,100,200: {m_R}")
    rows = [r for r in branch["rows"] if r["b"] > 3.5]
    sa = np.array([r["alpha"] for r in rows])
    sm = np.array([r["sqrt_alpha_m"] for r in rows])
    small = sa < 2e-3
    c2 = np.polyfit(np.sqrt(sa[small]), sm[small], 2)
    log(f"  BM: b={0.5 * (lo + hi):.8f} m_BM={m_bm:.6f} (classes {clo},{chi}); upper-branch sqrt(alpha) m -> "
        f"{c2[-1]:.6f} (quadratic fit in sqrt(alpha), alpha<2e-3); smallest alpha {sa.min():.2e} gives {sm[np.argmin(sa)]:.6f}")
    c1 = np.polyfit(sa[sa < 3e-4], sm[sa < 3e-4], 1)
    log(f"  upper branch linear-in-alpha extrapolation (alpha<3e-4): {c1[-1]:.6f}")
    return dict(b_BM=0.5 * (lo + hi), m_BM=float(m_bm), m_BM_R=[float(q) for q in m_R],
                upper_sqrt_alpha_m_extrap=float(c2[-1]), upper_sqrt_alpha_m_extrap_linear=float(c1[-1]),
                upper_smallest_alpha=float(sa.min()), upper_sqrt_alpha_m_at_smallest=float(sm[np.argmin(sa)]))


# ------------------------------------------------------------------ stage 8: physical scale
HBARC_MEV_FM = 197.3269804
HBAR_GEV_S = 6.582119569e-25


def stage_phys(flat):
    G = 6.70883e-39       # GeV^-2 (hbar = c = 1), as specified for this experiment
    e_anw = 5.45
    b0 = flat["b_flat"]
    x, F, P, m, ls = ec.profile(b0, 0.0, 5e-4, ec.x0_for(b0), 2e4)
    hh = np.log(x[1] / x[0])
    C = F[-1] * x[-1]**2
    minf = m[-1] + C**2 / x[-1]**3
    # first-order metric functions per unit alpha:  1 - N = alpha * 2 m/x ;  -ln sigma = alpha * s(x)
    integ = (x**2 + 2 * np.sin(F)**2) * P**2 / x * x      # in t
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * hh)])
    s_of_x = cum[-1] - cum                                    # int_x^inf ... (tail beyond 2e4 negligible)
    oneminusN = 2 * m / x
    k_of_x = m / x
    t = np.log(x)
    g_spl = CubicSpline(t, k_of_x + s_of_x)   # (delta g_00)/(2 alpha)
    k_spl = CubicSpline(t, k_of_x)            # (delta g_rr)/(2 alpha)

    def gfun(xx):
        xx = np.asarray(xx, dtype=float)
        out = np.where(xx < x[-1], 0.0, minf / np.maximum(xx, 1e-300))
        inside = xx < x[-1]
        out[inside] = g_spl(np.log(np.maximum(xx[inside], x[0])))
        return out

    def kfun(xx):
        xx = np.asarray(xx, dtype=float)
        out = np.where(xx < x[-1], 0.0, minf / np.maximum(xx, 1e-300))
        inside = xx < x[-1]
        out[inside] = k_spl(np.log(np.maximum(xx[inside], x[0])))
        return out

    def deflection(bimp):
        # delta = -alpha * int_{-inf}^{inf} d/db [ g(r) + k(r) z^2/r^2 ] dz, evaluated by central difference in b
        def I(bb):
            u = np.linspace(0, 12, 24001)           # z = bb sinh(u)
            z = bb * np.sinh(u)
            r = np.sqrt(bb * bb + z * z)
            dz = bb * np.cosh(u)
            # subtract the point-mass form to make the integral convergent, add it back analytically
            f = gfun(r) + kfun(r) * z * z / (r * r) - (minf / r + minf * z * z / r**3)
            return 2 * np.trapezoid(f * dz, u)
        db = 1e-4 * bimp
        dI = (I(bimp + db) - I(bimp - db)) / (2 * db)
        return -dI + 4 * minf / bimp     # per unit alpha; point mass gives 4 m/b

    bgrid = np.geomspace(0.05, 50, 60)
    dgrid = np.array([deflection(bb) for bb in bgrid])
    imax = int(np.argmax(dgrid))
    out = dict(G_GeVm2=G, e=e_anw, per_alpha={})
    out["per_alpha"] = dict(
        oneminusN_max=float(oneminusN.max()), x_at_max=float(x[np.argmax(oneminusN)]),
        oneminus_sigma0=float(s_of_x[0]), m_inf=float(minf),
        deflection_max=float(dgrid[imax]), b_at_max=float(bgrid[imax]),
        deflection_grid=[[float(a), float(d)] for a, d in zip(bgrid, dgrid)])
    for fMeV in [64.5, 92.2]:
        fG = fMeV / 1000
        al = 4 * math.pi * G * fG**2
        unit_len_fm = HBARC_MEV_FM / (e_anw * fMeV)        # 1/(e f) in fm
        x1 = 1.0 / unit_len_fm                              # x at r = 1 fm
        M_GeV = 4 * math.pi * fG / e_anw * minf
        i1 = np.searchsorted(x, x1)
        oneN_1fm = float(np.interp(x1, x, oneminusN)) * al
        osig_1fm = float(np.interp(x1, x, s_of_x)) * al
        defl_1fm = deflection(x1) * al
        # Shapiro delay for a diametral chord from -1 fm to +1 fm: dt = int (h00 + hzz)/2 dz = 2 int_0^R [ (1-sigma) + 2 mu/r ] dr
        sel = x <= x1
        xx = np.concatenate([x[sel], [x1]])
        integrand = np.concatenate([s_of_x[sel] + 2 * k_of_x[sel], [np.interp(x1, x, s_of_x + 2 * k_of_x)]])
        chord = 2 * np.trapezoid(integrand, xx) * al        # in units of 1/(e f)
        shapiro_s = chord * (1.0 / (e_anw * fG)) * HBAR_GEV_S
        out[f"f={fMeV}MeV"] = dict(
            alpha=al, alpha_over_alpha_crit=al / 0.040378, M_cl_GeV=M_GeV, length_unit_fm=unit_len_fm,
            x_at_1fm=x1, oneminusN_max=float(oneminusN.max() * al), r_at_oneminusN_max_fm=float(x[np.argmax(oneminusN)] * unit_len_fm),
            oneminusN_1fm=oneN_1fm, oneminus_sigma_core=float(s_of_x[0] * al), oneminus_sigma_1fm=osig_1fm,
            oneminus_gtt_core=float(2 * s_of_x[0] * al),
            deflection_max_rad=float(dgrid[imax] * al), b_at_deflection_max_fm=float(bgrid[imax] * unit_len_fm),
            deflection_1fm_rad=float(defl_1fm), pointmass_deflection_1fm_rad=float(4 * al * minf / x1),
            GM_over_c3_s=G * M_GeV * HBAR_GEV_S, shapiro_chord_pm1fm_s=float(shapiro_s),
            shapiro_chord_pm1fm_over_GM=float(shapiro_s / (G * M_GeV * HBAR_GEV_S)))
        log(f"  f={fMeV} MeV: alpha={al:.4e} M={M_GeV:.4f} GeV 1-N max={oneminusN.max() * al:.3e} "
            f"1-N(1fm)={oneN_1fm:.3e} 1-sigma(0)={s_of_x[0] * al:.3e} 1-sigma(1fm)={osig_1fm:.3e} "
            f"defl max={dgrid[imax] * al:.3e} rad defl(1fm)={defl_1fm:.3e} Shapiro(+-1fm)={shapiro_s:.3e} s")
    return out


# ------------------------------------------------------------------ stage 9: linear-response check of metric at small alpha
def stage_linear_metric(flat):
    b0 = flat["b_flat"]
    res = []
    for a in [1e-6, 1e-5, 1e-4]:
        b, _, _ = ec.bisect_b(a, b0 - 0.01, b0 + 0.01, 5e-4)
        x, F, P, m, ls = ec.profile(b, a, 5e-4, ec.x0_for(b), 2e3)
        x0_, F0_, P0_, m0_, _ = ec.profile(b0, 0.0, 5e-4, ec.x0_for(b0), 2e3)
        oneminusN = 2 * a * m / x
        pred = 2 * a * np.interp(np.log(x), np.log(x0_), m0_ / x0_)
        res.append(dict(alpha=a, max_rel_dev_1mN=float(np.max(np.abs(oneminusN - pred)) / np.max(pred))))
    log("  " + "; ".join(f"alpha={r['alpha']:.0e}: max|(1-N)-(1-N)_lin|/max = {r['max_rel_dev_1mN']:.2e}" for r in res))
    return {"rows": res}


def main():
    flat = stage("flat", stage_flat)
    log(f"flat: b={flat['b_flat']:.12f} m0={flat['m0']:.12f} E=4pi m0={4 * math.pi * flat['m0']:.8f} f/e; "
        f"virial E2/E4-1={flat['virial']:.2e}")
    crit = stage("crit", stage_crit)
    log(f"alpha_crit (h=5e-4) = {crit['runs'][2]['alpha_crit']:.15f}; Richardson {crit['richardson_rk4']:.15f}; "
        f"observed order {crit['observed_order']:.2f}")
    branch = stage("branch", lambda: stage_branch(flat["b_flat"]))
    fixed = stage("fixed_alpha", lambda: stage_fixed_alpha(branch, crit))
    bvp = stage("bvp", lambda: stage_bvp(crit, X=200.0))
    bvp2 = stage("bvp_X400", lambda: stage_bvp(crit, X=400.0))
    ep = stage("ep", lambda: stage_ep(flat))
    bm = stage("bm", lambda: stage_bm(branch))
    phys = stage("phys", lambda: stage_phys(flat))
    lin = stage("linear_metric", lambda: stage_linear_metric(flat))
    log("all stages done")


if __name__ == "__main__":
    main()
