#!/usr/bin/env python3
"""Deflection per unit alpha computed two ways from the flat profile (first order in alpha):
 (iso)  defl = (2/b) int_0^inf [m + m_T](b cosh t) / cosh^2 t dt            (isotropic gauge)
 (schw) defl = -1/2 int d/db [dg00 + dg_zz] dz  in Schwarzschild coordinates, with
        dg00 = 2 s1(r) + 2 m/r,  dg_zz = (2 m/r) (z/r)^2,  s1 = (1 - sigma)/alpha = int_r^inf x (rho+p_r) dx
        d/db done analytically: dH/dr = -2 r p_r - 2 m/r^2, dK/dr = 2 r rho - 2 m/r^2 (H = dg00, K = 2m/r).
The two must agree (the total deflection is gauge invariant).  Also locates the maximum precisely.
"""
import os, sys, json
import numpy as np
from scipy.optimize import minimize_scalar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xc_iso as X

HERE = os.path.dirname(os.path.abspath(__file__))


def cumint(g, integrand_x, from_zero=True):
    n = g.N + 1
    fx = np.zeros(n)
    fx[1:-1] = integrand_x * g.L / (1 - g.si) ** 2
    D = g.D.copy(); rhs = fx.copy()
    if from_zero:
        D[0, :] = 0; D[0, 0] = 1; rhs[0] = 0
    else:
        D[-1, :] = 0; D[-1, -1] = 1; rhs[-1] = 0
    return np.linalg.solve(D, rhs)


out = {}
for (N, L) in [(100, 1.5), (140, 1.5), (140, 1.0)]:
    g = X.Grid(N, L)
    U, ok = X.newton(X.flat_guess(g), 0.0, g)
    (Fi, Fx, Fxx), (Pi, Px, Pxx), (Ai, Ax, Axx) = X.pointwise(U, g)[0]
    x = g.x
    args = (x, Fi, Fx, Fxx, Pi, Px, Pxx, Ai, Ax, Axx)
    rho = X.f_rho(*args); pr = X.f_pr(*args); pt = X.f_pt(*args)
    tr = pr + 2 * pt
    m = cumint(g, x ** 2 * rho)
    mT = cumint(g, x ** 2 * (rho + tr))
    s1 = cumint(g, -x * (rho + pr), from_zero=False)
    rhon = np.concatenate([[rho[0]], rho, [0.0]]); prn = np.concatenate([[pr[0]], pr, [0.0]])
    m0 = m[-1]

    def I(vals, r):
        return g.interp(vals, r / (r + g.L))

    tt, wt = np.polynomial.legendre.leggauss(600)
    T = 25.0
    tg = 0.5 * T * (tt + 1); wg = 0.5 * T * wt

    def defl_iso(b):
        r = np.minimum(b * np.cosh(tg), 1e12)
        return 2.0 / b * np.sum(wg * (I(m, r) + I(mT, r)) / np.cosh(tg) ** 2)

    def defl_schw(b):
        r = np.minimum(b * np.cosh(tg), 1e12)
        z = b * np.sinh(tg)
        mm = I(m, r); ss = I(s1, r); rr = I(rhon, r); pp = I(prn, r)
        K = 2 * mm / r
        dH = -2 * r * pp - 2 * mm / r ** 2
        dK = 2 * r * rr - 2 * mm / r ** 2
        dfdb = dH * b / r + dK * (b / r) * z ** 2 / r ** 2 + K * z ** 2 * (-2 * b / r ** 4)
        # dz = b cosh t dt, both halves
        return -0.5 * 2 * np.sum(wg * dfdb * b * np.cosh(tg))

    bs = np.exp(np.linspace(np.log(0.1), np.log(5), 400))
    di = np.array([defl_iso(b) for b in bs]); dsw = np.array([defl_schw(b) for b in bs])
    k = np.argmax(di)
    oi = minimize_scalar(lambda lb: -defl_iso(np.exp(lb)), bounds=(np.log(bs[k - 3]), np.log(bs[k + 3])), method='bounded',
                         options=dict(xatol=1e-10))
    k2 = np.argmax(dsw)
    os_ = minimize_scalar(lambda lb: -defl_schw(np.exp(lb)), bounds=(np.log(bs[k2 - 3]), np.log(bs[k2 + 3])), method='bounded',
                          options=dict(xatol=1e-10))
    row = dict(N=N, L=L, iso_max=-oi.fun, iso_bmax=float(np.exp(oi.x)), schw_max=-os_.fun, schw_bmax=float(np.exp(os_.x)),
               max_rel_diff_iso_schw=float(np.max(np.abs(di - dsw) / di)),
               at_b=dict((str(b), dict(iso=defl_iso(b), schw=defl_schw(b))) for b in (0.41, 0.5, 0.74, 0.7743, 1.0, 2.0, 50.0)),
               b50_over_pointmass=defl_iso(50.0) / (4 * m0 / 50.0))
    out['N%d_L%.1f' % (N, L)] = row
    print('N=%d L=%.1f  iso max=%.6f at b=%.5f | schw max=%.6f at b=%.5f | max rel diff iso/schw over b in [0.1,5]: %.2e | d(0.74)=%.6f d(0.7743)=%.6f | d(50)/(4m0/50)=%.7f' % (
        N, L, -oi.fun, np.exp(oi.x), -os_.fun, np.exp(os_.x), row['max_rel_diff_iso_schw'], defl_iso(0.74), defl_iso(0.7743),
        row['b50_over_pointmass']))
json.dump(out, open(os.path.join(HERE, 'out', 'xc_defl_check.json'), 'w'), indent=1, default=float)
