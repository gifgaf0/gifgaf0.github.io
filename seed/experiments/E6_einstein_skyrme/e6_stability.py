#!/usr/bin/env python3
"""E6 extension: radial (l = 0) linear stability of both branches.

Uses the pulsation equation derived in derive_pulsation.py (pulsation_coeffs.json):
    a xi'' + b xi' + c xi = omega^2 d xi,   a = -sigma N A,  d = A/(sigma N),  A = x^2 + 2 sin^2F
After checking numerically that b = -(sigma N A)' (self-adjoint, p = sigma N A, w = A/(sigma N), q = c), solve
    -(p xi')' + q xi = omega^2 w xi,  xi(x0) = 0 (F(0) = pi fixed), xi(X) = 0 (box),
by second-order finite differences on a uniform grid in t = ln x (symmetric tridiagonal generalized problem).
omega is in units of e f, measured at infinity (sigma(inf) = 1).  With massless pions the spectrum is
continuous from 0; in a box the lowest positive eigenvalues scale like 1/X^2, a bound negative eigenvalue
(instability) converges in X.  Run after e6_solve.py (reads out/stage_crit.json and out/stage_fixed_alpha.json).
"""
import json
import math
import os
import sys
import time

import numpy as np
import sympy as sp
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import es_core as ec  # noqa: E402

OUT = os.path.join(HERE, "out")
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:7.1f}s]", *a, flush=True)


with open(os.path.join(HERE, "pulsation_coeffs.json")) as fh:
    co = json.load(fh)
syms = sp.symbols('x F P m sg alpha')
fn = {k: sp.lambdify(syms, sp.sympify(co[k], locals={'alpha': syms[5]}), 'numpy') for k in ['a', 'b', 'c', 'd']}


X_START = 2.5e-3   # inner Dirichlet point (xi ~ x near the centre). The cut shifts the fold crossing by ~40*X_START^3
#                    in b (~6e-7 here); at h = 5e-3 the O(h^2) FD error shifts it by ~ -3.4e-6 (see zero_crossing_convergence)
H_PROFILE = 1e-3   # background profile step in t = ln x


def zero_freq_end(b, al, X=400.0, h=1e-3, x_start=X_START):
    """[reconciliation] Normalised end value xi(X)/max|xi| of the omega^2 = 0 solution of the same FD operator
    (xi ~ x at the inner end).  It vanishes exactly when the discrete operator has a zero eigenvalue, so its root
    in b is the zero crossing of omega^2 free of eigen-solver round-off (default tolerance eps*||T||_1)."""
    x, F, P, m, ls = ec.profile(b, al, H_PROFILE, ec.x0_for(b), max(X, 2e3))
    sg = np.exp(ls - ls[-1])
    stride = int(round(h / H_PROFILE))
    i0 = int(np.searchsorted(x, x_start))
    x, F, P, m, sg = x[i0::stride], F[i0::stride], P[i0::stride], m[i0::stride], sg[i0::stride]
    sel = x <= X * (1 + 1e-12)
    x, F, P, m, sg = x[sel], F[sel], P[sel], m[sel], sg[sel]
    ph = -fn['a'](x, F, P, m, sg, al) / x
    qh = x * fn['c'](x, F, P, m, sg, al)
    hh = np.log(x[1]) - np.log(x[0])
    pm = 0.5 * (ph[1:] + ph[:-1])
    xi = np.empty(len(x))
    xi[0], xi[1] = 0.0, x[1] - x[0]
    for i in range(1, len(x) - 1):
        xi[i + 1] = xi[i] + (pm[i - 1] * (xi[i] - xi[i - 1]) + hh**2 * qh[i] * xi[i]) / pm[i]
    return xi[-1] / np.max(np.abs(xi))


def lowest_modes(b, al, X=200.0, h=5e-3, nev=3, check=False, nodes=False):
    """Lowest eigenvalues omega^2 on [X_START, X] with an FD grid of step h in t (h a multiple of H_PROFILE).
    Starting the grid at X_START (not at the series point x0 ~ 1e-3) keeps the matrix condition number below ~1e10,
    so the small box-continuum eigenvalues (~3e-5 at X=800) are resolved (absolute error ~ eps*||T||)."""
    x0 = ec.x0_for(b)
    x, F, P, m, ls = ec.profile(b, al, H_PROFILE, x0, max(X, 2e3))
    # normalise sigma at infinity: tail of ln sigma beyond 2e3 is ~ alpha C^2/x^4, negligible
    sg = np.exp(ls - ls[-1])
    stride = int(round(h / H_PROFILE))
    i0 = int(np.searchsorted(x, X_START))
    x, F, P, m, sg = x[i0::stride], F[i0::stride], P[i0::stride], m[i0::stride], sg[i0::stride]
    sel = x <= X * (1 + 1e-12)
    x, F, P, m, sg = x[sel], F[sel], P[sel], m[sel], sg[sel]
    a = fn['a'](x, F, P, m, sg, al)
    bb = fn['b'](x, F, P, m, sg, al)
    c = fn['c'](x, F, P, m, sg, al)
    d = fn['d'](x, F, P, m, sg, al)
    p = -a
    w = d
    sa = None
    if check:
        dp = np.gradient(p, x)
        inner = slice(10, -10)
        sa = float(np.max(np.abs(bb[inner] + dp[inner])) / np.max(np.abs(bb[inner])))
    t = np.log(x)
    hh = t[1] - t[0]
    ph = p / x                      # -(p xi')' + q xi = om^2 w xi  ->  -d/dt[(p/x) xi_t] + x q xi = om^2 x w xi
    qh = x * c
    wh = x * w
    pm = 0.5 * (ph[1:] + ph[:-1])   # half-point values
    n = len(x) - 2                  # interior unknowns (Dirichlet at both ends)
    diag = (pm[:-1] + pm[1:]) / hh**2 + qh[1:-1]
    off = -pm[1:-1] / hh**2
    s = 1.0 / np.sqrt(wh[1:-1])
    D = diag * s * s
    E = off * s[:-1] * s[1:]
    ev = eigh_tridiagonal(D, E, eigvals_only=True, select='i', select_range=(0, nev - 1))
    if nodes:
        # zero-frequency solution of the same FD operator, xi ~ x at the inner end: its sign changes count the
        # negative eigenvalues (discrete Sturm / Jacobi criterion), independent of the eigen-solver
        xi = np.empty(len(x))
        xi[0], xi[1] = 0.0, x[1] - x[0]
        for i in range(1, len(x) - 1):
            xi[i + 1] = xi[i] + (pm[i - 1] * (xi[i] - xi[i - 1]) + hh**2 * qh[i] * xi[i]) / pm[i]
            if abs(xi[i + 1]) > 1e200:
                xi[:i + 2] *= 1e-200
        nz = int(np.sum(np.sign(xi[2:]) * np.sign(xi[1:-1]) < 0))
        return ev, sa, nz
    return ev, sa


def main():
    with open(os.path.join(OUT, "stage_crit.json")) as fh:
        crit = json.load(fh)
    with open(os.path.join(OUT, "stage_fixed_alpha.json")) as fh:
        fixed = json.load(fh)
    flat = json.load(open(os.path.join(OUT, "stage_flat.json")))
    ac, bc = crit["runs"][2]["alpha_crit"], crit["runs"][2]["b_crit"]
    res = {"alpha_crit": ac, "b_crit": bc, "rows": []}
    # self-adjointness check and convergence at one lower and one upper point
    for lab, bb, al in [("flat", flat["b_flat"], 0.0)] + [
            (f"{br} alpha={r['alpha']}", r[br]["b"], r["alpha"]) for r in fixed["rows"]
            if r["alpha"] in (0.02, 0.035, 0.04) for br in ("lower", "upper") if br in r]:
        row = dict(label=lab, b=bb, alpha=al, conv={})
        for X in [100.0, 200.0, 400.0, 800.0]:
            for h in [1e-2, 5e-3]:
                ev, sa, nz = lowest_modes(bb, al, X=X, h=h, check=(X == 200.0 and h == 5e-3), nodes=True)
                row["conv"][f"X={X:g},h={h:g}"] = [float(v) for v in ev]
                row.setdefault("nodes", {})[f"X={X:g},h={h:g}"] = nz
                if sa is not None:
                    row["self_adjoint_rel_err"] = sa
        row["omega2_lowest"] = row["conv"]["X=800,h=0.005"][0]
        row["n_negative_modes"] = row["nodes"]["X=800,h=0.005"]
        res["rows"].append(row)
        log(f"  {lab:22s} b={bb:.6f}: omega^2_min (X=100/200/400/800, h=5e-3) = "
            + " ".join(f"{row['conv'][f'X={X:g},h=0.005'][0]:+.6e}" for X in [100, 200, 400, 800])
            + f"; h=1e-2 at X=800: {row['conv']['X=800,h=0.01'][0]:+.6e}; nodes {row['nodes']['X=800,h=0.005']}"
            + f"; self-adjoint check {row.get('self_adjoint_rel_err', float('nan')):.1e}")
    # scan along the branch near the fold: lowest eigenvalue vs b, and its zero crossing
    with open(os.path.join(OUT, "stage_branch.json")) as fh:
        branch = json.load(fh)

    def alpha_b(b):
        import e6_solve as es
        return es.alpha_of_b(b)

    scan = []
    for db in [-0.4, -0.2, -0.1, -0.05, -0.02, -0.01, 0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 1.0, 3.0]:
        b = bc + db
        al = alpha_b(b)
        ev800, _, nz = lowest_modes(b, al, X=800.0, h=5e-3, nev=1, nodes=True)
        scan.append(dict(b=b, alpha=al, omega2_X800=float(ev800[0]), n_negative=nz))
        log(f"  scan b={b:.5f} alpha={al:.8f}: omega^2_min(X=800) = {ev800[0]:+.6e}  negative modes (node count) = {nz}")
    res["scan"] = scan
    # zero crossing of the lowest eigenvalue (X = 400 and X = 800) near the fold
    zc = {}
    for X in [200.0, 400.0, 800.0, 1600.0]:
        g = lambda b: lowest_modes(b, alpha_b(b), X=X, h=5e-3, nev=1)[0][0]
        try:
            zc[f"X={X:g}"] = brentq(g, bc - 0.05, bc + 0.05, xtol=1e-7)
        except ValueError as err:
            zc[f"X={X:g}"] = f"no sign change: {err}"
        log(f"  zero crossing of omega^2_min at X={X:g}: b = {zc[f'X={X:g}']}  (b_crit = {bc:.7f})")
    res["zero_crossing_b"] = zc
    res["zero_crossing_b_note"] = ("FD step h = 5e-3, inner cut 2.5e-3, eigen-solver default tolerance: not converged "
                                   "in h; see zero_crossing_convergence")
    # [reconciliation] convergence of the zero crossing in the FD step h and the inner cut, by the zero-frequency
    # (Jacobi) criterion at X = 400; Richardson in h^2 from h = 2e-3 and 1e-3
    acache = {}

    def ab_cached(b):
        if b not in acache:
            acache[b] = alpha_b(b)
        return acache[b]

    conv = []
    for xs in [5e-3, 2.5e-3, 1.25e-3]:
        row = dict(x_cut=xs, inner_cut_estimate_40xcut3=40 * xs**3, offsets={})
        for h in [5e-3, 2e-3, 1e-3]:
            zb = brentq(lambda b: zero_freq_end(b, ab_cached(b), X=400.0, h=h, x_start=xs), bc - 0.01, bc + 0.01,
                        xtol=1e-10)
            row["offsets"][f"h={h:g}"] = zb - bc
        o2, o1 = row["offsets"]["h=0.002"], row["offsets"]["h=0.001"]
        row["richardson_h0"] = o1 + (o1 - o2) / 3.0
        row["h2_coefficient"] = (o2 - o1) / (4e-6 - 1e-6)
        conv.append(row)
        log(f"  zero crossing - b_crit (Jacobi, X=400) at x_cut={xs:.2e}: "
            + ", ".join(f"{k}: {v:+.3e}" for k, v in row["offsets"].items())
            + f"; h->0: {row['richardson_h0']:+.2e} (40 x_cut^3 = {40 * xs**3:.1e}); h^2 coefficient {row['h2_coefficient']:.3f}")
    res["zero_crossing_convergence"] = conv
    with open(os.path.join(OUT, "stage_stability.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    log("stability done")


if __name__ == "__main__":
    main()
