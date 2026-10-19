#!/usr/bin/env python3
"""
Cross-check of E6 radial (l = 0) stability, written for the cross-check.

Pulsation operator: derived from scratch in xc_pulsation_derive.py (Schwarzschild-type gauge,
areal radius R):  a xi'' + b xi' + c xi + w^2 d xi = 0 with a = -p, p = s N (R^2 + 2 sin^2 F),
so the Sturm-Liouville form is  -(p xi')' + q xi = w^2 W xi  with q = c, W = -d.

Backgrounds come from the ISOTROPIC-gauge spectral solutions (xc_iso.py), converted to
Schwarzschild quantities pointwise:  R = x psi^2, R_x = psi^2 + 2 x psi psi_x,
N = R_x^2 / psi^4, sigma = A psi^2 / R_x, alpha m = R (1 - N)/2, F_R = F_x / R_x.
The SL problem is then written in the isotropic radius x (p~ = p/R_x, q~ = q R_x, W~ = W R_x)
and in the compactified Chebyshev variable s (x = L s/(1-s)), Dirichlet at s = 0 and s = 1,
and solved as a dense generalized eigenproblem (Chebyshev collocation; the original used
finite differences in ln R in a finite box).

Checks printed:
  * negative-mode count and lowest eigenvalue on both branches at alpha = 0.02, 0.035, 0.04
    (plus the flat skyrmion), for two background resolutions;
  * lowest eigenvalue along the branch through the fold: it must cross zero AT the fold
    (the static zero mode d/db at fixed alpha_crit) -- an independent test of q.
"""
import json, os, sys, time
import numpy as np
import scipy.linalg as sla
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xc_iso as X

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
T0 = time.time()


def log(*a):
    print('[%7.1fs]' % (time.time() - T0), *a, flush=True)


_pj = json.load(open(os.path.join(HERE, 'xc_pulsation.json')))
_ns = {k: getattr(sp, k) for k in dir(sp) if not k.startswith('_')}
_a, _c, _d, _p = (eval(_pj[k], _ns) for k in ('a', 'c', 'd', 'p'))
_syms = sorted(_c.free_symbols | _a.free_symbols, key=lambda s: s.name)
_names = [s.name for s in _syms]
assert set(_names) == {'F1', 'Fv', 'alpha', 'mv', 'sv', 'x'}, _names
assert sp.simplify(_a + _p) == 0
f_p = sp.lambdify(_syms, _p, 'numpy')
f_q = sp.lambdify(_syms, _c, 'numpy')
f_W = sp.lambdify(_syms, -_d, 'numpy')


def call(f, F1, Fv, alpha, mv, sv, x):
    kw = dict(F1=F1, Fv=Fv, alpha=alpha, mv=mv, sv=sv, x=x)
    return f(*[kw[n] for n in _names]) * np.ones_like(x)


def schw_background(U, g, alpha):
    (Fi, Fx, Fxx), (Pi, Px, Pxx), (Ai, Ax, Axx) = X.pointwise(U, g)[0]
    x = g.x
    R = x * Pi ** 2
    Rx = Pi ** 2 + 2 * x * Pi * Px
    N = Rx ** 2 / Pi ** 4
    sig = Ai * Pi ** 2 / Rx
    am = R * (1 - N) / 2
    m = am / alpha if alpha > 0 else np.zeros_like(R)
    FR = Fx / Rx
    return dict(x=x, R=R, Rx=Rx, N=N, sig=sig, m=m, F=Fi, FR=FR)


def spectrum(U, g, alpha, nev=4):
    B = schw_background(U, g, alpha)
    R, Rx = B['R'], B['Rx']
    p = call(f_p, B['FR'], B['F'], alpha, B['m'], B['sig'], R)
    q = call(f_q, B['FR'], B['F'], alpha, B['m'], B['sig'], R)
    W = call(f_W, B['FR'], B['F'], alpha, B['m'], B['sig'], R)
    xs = g.L / (1 - g.si) ** 2           # dx/ds at interior nodes
    P = np.zeros(g.N + 1)
    P[1:-1] = p / Rx / xs
    P[0] = 0.0
    P[-1] = g.L                          # limit p/(R_x x_s) -> L at infinity (psi, sigma, N -> 1)
    Q = q * Rx * xs
    Wt = W * Rx * xs
    D = g.D
    K = -(D @ np.diag(P) @ D)[1:-1, 1:-1] + np.diag(Q)
    M = np.diag(Wt)
    ev = sla.eigvals(K, M)
    ev = ev[np.isfinite(ev)]
    order = np.argsort(ev.real)
    ev = ev[order]
    nneg = int(np.sum((ev.real < -1e-8) & (np.abs(ev.imag) < 1e-6 * np.maximum(1, np.abs(ev.real)))))
    ncomplex = int(np.sum(np.abs(ev.imag) > 1e-6 * np.maximum(1, np.abs(ev.real))))
    return ev[:nev], nneg, ncomplex


def resolve(U, g, alpha, N2):
    g2 = X.Grid(N2, g.L)
    U2, ok = X.newton(X.regrid(U, g, g2), alpha, g2)
    assert ok
    return U2, g2


if __name__ == '__main__':
    res = {'fixed': [], 'fold_scan': []}
    sols = np.load(os.path.join(OUT, 'xc_fixed_sols.npz'))
    keys = sorted(k[:-2] for k in sols.files if k.endswith('_U'))
    for k in keys:
        br, a = k.split('_')
        a = float(a)
        if a not in (0.0, 0.02, 0.035, 0.04):
            continue
        U = sols[k + '_U']; NL = sols[k + '_NL']
        g = X.Grid(int(NL[0]), float(NL[1]))
        row = dict(branch=br, alpha=a, b_schw=X.central(U, g)['b_schw'])
        for N2 in (int(NL[0]), int(NL[0]) + 40):
            U2, g2 = (U, g) if N2 == g.N else resolve(U, g, a, N2)
            ev, nneg, ncx = spectrum(U2, g2, a)
            row['N%d' % N2] = dict(lowest=[float(e.real) for e in ev], nneg=nneg, ncomplex=ncx)
            log('%s alpha=%.3f N=%d L=%.3f b=%.5f  nneg=%d ncomplex=%d  lowest w^2: %s' % (
                br, a, N2, g.L, row['b_schw'], nneg, ncx, ' '.join('%.7g' % e.real for e in ev)))
        res['fixed'].append(row)

    # ---- scan through the fold
    z = np.load(os.path.join(OUT, 'xc_fold_U.npy'))
    NL = np.load(os.path.join(OUT, 'xc_fold_grid.npy'))
    g = X.Grid(int(NL[0]), float(NL[1]))
    U0, a0 = z[:-1], z[-1]
    Wsc = 100.0
    J = X.jac(U0, a0, g); J[:, -1] /= Wsc
    t = np.linalg.svd(J)[2][-1]
    if X.central(U0 + 1e-4 * t[:-1], g)['b_schw'] < X.central(U0, g)['b_schw']:
        t = -t
    Y0 = np.concatenate([U0, [a0 * Wsc]])
    bf = X.central(U0, g)['b_schw']
    scan = []
    for h in np.linspace(-0.03, 0.03, 13):
        Yp = Y0 + h * t
        Yh, ok = X.corrector(Yp.copy(), t, Yp, g, Wsc)
        Uh, ah = Yh[:-1], Yh[-1] / Wsc
        ev, nneg, ncx = spectrum(Uh, g, ah)
        bh = X.central(Uh, g)['b_schw']
        scan.append((bh, ah, float(ev[0].real), nneg))
        log('fold scan b=%.7f alpha=%.12f lowest=%.4e nneg=%d' % (bh, ah, ev[0].real, nneg))
    sc = np.array(scan)
    # zero crossing of the bound-state eigenvalue. On the lower side the lowest eigenvalue is the
    # discretised continuum floor (~4e-7 here, positive), so fit only the points at/after the fold,
    # where the bound state is the lowest eigenvalue, and extrapolate/interpolate to zero.
    lam = sc[:, 2]
    selb = sc[:, 0] >= bf - 1e-9
    cf = np.polyfit(sc[selb, 0] - bf, lam[selb], 2)
    rts = [r.real for r in np.roots(cf) if abs(r.imag) < 1e-12]
    b0 = bf + min(rts, key=abs)
    log('fold b (this grid) = %.7f ; zero crossing of lowest w^2 at b = %s' % (bf, b0))
    res['fold_scan'] = dict(rows=scan, b_fold=bf, b_zero=b0, N=g.N, L=g.L)
    json.dump(res, open(os.path.join(OUT, 'xc_stability.json'), 'w'), indent=1, default=float)
    log('done')
