"""E6 core: hedgehog Einstein-Skyrme ODEs (dimensionless, derived in derive_equations.py) and a shooting integrator.

Units: x = e f r, alpha = 4 pi G f^2, f = F_pi/2 (ANW F_pi = 129 MeV -> f = 64.5 MeV).
    N = 1 - 2 alpha m(x)/x,     M_ADM = 4 pi (f/e) m(inf)
    m'   = (N F'^2/2)(x^2 + 2 sin^2F) + sin^2F (1 + sin^2F/(2 x^2))
    (ln sigma)' = (alpha/x)(x^2 + 2 sin^2F) F'^2
    (sigma N (x^2 + 2 sin^2F) F')' = sigma sin2F (1 + N F'^2 + sin^2F/x^2)
Boundary conditions: F(0)=pi, m(0)=0 (series start), F->0 (F ~ C/x^2), sigma(inf)=1 (normalisation).

Integrator: classical RK4 in t = ln x with uniform step h (all structure is smooth in ln x; the decaying
tail F ~ C/x^2 is a pure exponential in t).  The shooting outcome is classified as
   -1 overshoot (F < 0), +1 undershoot (F' > 0 while F > 0), +2 horizon (N <= 0),
or, if none happens by x_max, by the sign of the growing-mode amplitude, sign(x F' + 2F) (F = A x + C/x^2 -> 3 A x).
"""
import math

import numpy as np
from numba import njit


@njit(cache=True)
def series_start(b, al, x0):
    """Series at the regular centre (derive_equations.py, part F): returns F, F', m at x0."""
    b2 = b * b
    c3 = -b**3 * (6 * al * b2**2 + 18 * al * b2 + 9 * al - 2 * b2 - 4) / (30 * (2 * b2 + 1))
    c5 = -b**5 * (584 * al**2 * b**10 + 3004 * al**2 * b**8 + 5588 * al**2 * b**6 + 4776 * al**2 * b**4
                  + 1934 * al**2 * b2 + 305 * al**2 - 576 * al * b**8 - 1720 * al * b**6 - 2020 * al * b**4
                  - 1108 * al * b2 - 240 * al + 56 * b**6 + 44 * b**4 + 64 * b2 + 40) / (1400 * (2 * b2 + 1)**3)
    m3 = b2 * (b2 + 1) / 2
    m5 = b**4 * (3 * al * b2 + 2 * al - 2 * b2 - 2) / 10
    F = math.pi - b * x0 + c3 * x0**3 + c5 * x0**5
    P = -b + 3 * c3 * x0**2 + 5 * c5 * x0**4
    m = m3 * x0**3 + m5 * x0**5
    # ln sigma from 0 to x0: (ln s)' ~ alpha x b^2 (1 + 2 b^2) + O(x^3)
    ls = al * b2 * (1 + 2 * b2) * x0**2 / 2
    return F, P, m, ls


@njit(cache=True)
def rhs_t(x, F, P, m, al):
    """d/dt of (F, P=dF/dx, m, ln sigma) with t = ln x."""
    s = math.sin(F)
    s2 = s * s
    s2F = math.sin(2.0 * F)
    N = 1.0 - 2.0 * al * m / x
    A = x * x + 2.0 * s2
    mp = 0.5 * N * P * P * A + s2 * (1.0 + s2 / (2.0 * x * x))
    Np = -2.0 * al * (mp / x - m / (x * x))
    sr = al / x * A * P * P
    Ap = 2.0 * x + 2.0 * s2F * P
    Fpp = (s2F * (1.0 + N * P * P + s2 / (x * x)) - (sr * N * A + Np * A + N * Ap) * P) / (N * A)
    return x * P, x * Fpp, x * mp, x * sr


@njit(cache=True)
def rk4_step(t, F, P, m, ls, hh, al):
    """One step of size hh in t = ln x; split into sub-steps when the trajectory moves fast
    (|dF| > 0.01 or |dP| > 5% of |P|+1 per sub-step).  Converged solutions never trigger the split at h <= 2e-3."""
    x = math.exp(t)
    k1 = rhs_t(x, F, P, m, al)
    nsub = 1 + int(abs(k1[0]) * hh / 0.01)
    n2 = 1 + int(abs(k1[1]) * hh / (0.05 * (abs(P) + 1.0)))
    if n2 > nsub:
        nsub = n2
    if nsub > 4096:
        nsub = 4096
    hs = hh / nsub
    for j in range(nsub):
        tt = t + j * hs
        x = math.exp(tt)
        k1 = rhs_t(x, F, P, m, al)
        xm = math.exp(tt + 0.5 * hs)
        k2 = rhs_t(xm, F + 0.5 * hs * k1[0], P + 0.5 * hs * k1[1], m + 0.5 * hs * k1[2], al)
        k3 = rhs_t(xm, F + 0.5 * hs * k2[0], P + 0.5 * hs * k2[1], m + 0.5 * hs * k2[2], al)
        xe = math.exp(tt + hs)
        k4 = rhs_t(xe, F + hs * k3[0], P + hs * k3[1], m + hs * k3[2], al)
        F += hs / 6.0 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        P += hs / 6.0 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        m += hs / 6.0 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        ls += hs / 6.0 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])
        if F < 0.0 or P > 0.0:
            break
    return F, P, m, ls, nsub


@njit(cache=True)
def shoot(b, al, h, x0, xmax, xrec):
    """Integrate from x0 to xmax.  Returns (code, x_rec, F, P, m, ls at the first grid point x_rec >= xrec
    (or at the end if the run stopped earlier), Nmin, xNmin)."""
    F, P, m, ls = series_start(b, al, x0)
    t = math.log(x0)
    tmax = math.log(xmax)
    nsteps = int(math.ceil((tmax - t) / h))
    hh = (tmax - t) / nsteps
    Nmin = 1.0
    xNmin = x0
    recF = 0.0
    recP = 0.0
    recm = 0.0
    recls = 0.0
    recx = x0
    recorded = False
    code = 0
    x = x0
    for i in range(nsteps):
        F, P, m, ls, nsub = rk4_step(t, F, P, m, ls, hh, al)
        t = math.log(x0) + (i + 1) * hh
        x = math.exp(t)
        N = 1.0 - 2.0 * al * m / x
        if N < Nmin:
            Nmin = N
            xNmin = x
        if (not recorded) and x >= xrec:
            recF, recP, recm, recls, recx = F, P, m, ls, x
            recorded = True
        if N <= 0.0:
            code = 2
            break
        if F < 0.0:
            code = -1
            break
        if P > 0.0:
            code = 1
            break
    if code == 0:
        g = x * P + 2.0 * F
        code = 1 if g > 0 else -1
    if not recorded:
        recF, recP, recm, recls, recx = F, P, m, ls, x
    return code, recx, recF, recP, recm, recls, Nmin, xNmin


@njit(cache=True)
def profile(b, al, h, x0, xmax):
    """Dense profile on the uniform t grid: arrays x, F, P, m, lnsigma (unnormalised)."""
    F, P, m, ls = series_start(b, al, x0)
    t0 = math.log(x0)
    tmax = math.log(xmax)
    nsteps = int(math.ceil((tmax - t0) / h))
    hh = (tmax - t0) / nsteps
    xs = np.empty(nsteps + 1)
    Fs = np.empty(nsteps + 1)
    Ps = np.empty(nsteps + 1)
    ms = np.empty(nsteps + 1)
    lss = np.empty(nsteps + 1)
    xs[0], Fs[0], Ps[0], ms[0], lss[0] = x0, F, P, m, ls
    t = t0
    for i in range(nsteps):
        F, P, m, ls, nsub = rk4_step(t, F, P, m, ls, hh, al)
        t = t0 + (i + 1) * hh
        xs[i + 1], Fs[i + 1], Ps[i + 1], ms[i + 1], lss[i + 1] = math.exp(t), F, P, m, ls
    return xs, Fs, Ps, ms, lss


# ------------------------------------------------------------------ python-level drivers
DEFAULT = dict(h=2e-3, xmax=1e6, xrec=2e3)


def x0_for(b):
    return min(1e-3, 2e-3 / max(b, 1.0))


def classify(b, al, h=DEFAULT['h'], xmax=DEFAULT['xmax']):
    return shoot(b, al, h, x0_for(b), xmax, DEFAULT['xrec'])[0]


def bisect_alpha(b, a_lo, a_hi, h=DEFAULT['h'], xmax=DEFAULT['xmax'], rel=4e-16, maxit=200):
    """At fixed b find alpha on the solution curve.  Requires class(a_lo) = -1, class(a_hi) in (+1, +2)."""
    c_lo = classify(b, a_lo, h, xmax)
    c_hi = classify(b, a_hi, h, xmax)
    if not (c_lo == -1 and c_hi in (1, 2)):
        raise ValueError(f"bad alpha bracket at b={b}: classes {c_lo},{c_hi} for {a_lo},{a_hi}")
    for _ in range(maxit):
        mid = 0.5 * (a_lo + a_hi)
        if mid in (a_lo, a_hi) or (a_hi - a_lo) <= rel * abs(mid):
            break
        c = classify(b, mid, h, xmax)
        if c == -1:
            a_lo = mid
        else:
            a_hi = mid
    return 0.5 * (a_lo + a_hi), a_lo, a_hi


def bisect_b(al, b_lo, b_hi, h=DEFAULT['h'], xmax=DEFAULT['xmax'], rel=4e-16, maxit=200):
    """At fixed alpha bisect on b = -F'(0) between two b values with opposite shooting classes."""
    c_lo = classify(b_lo, al, h, xmax)
    c_hi = classify(b_hi, al, h, xmax)
    if c_lo == c_hi or (c_lo in (1, 2) and c_hi in (1, 2)):
        raise ValueError(f"bad b bracket at alpha={al}: classes {c_lo},{c_hi}")
    for _ in range(maxit):
        mid = 0.5 * (b_lo + b_hi)
        if mid in (b_lo, b_hi) or (b_hi - b_lo) <= rel * abs(mid):
            break
        c = classify(mid, al, h, xmax)
        if (c == -1) == (c_lo == -1):
            b_lo = mid
        else:
            b_hi = mid
    return 0.5 * (b_lo + b_hi), b_lo, b_hi


def observables(b, al, h=DEFAULT['h'], xmax=DEFAULT['xmax'], xrec=DEFAULT['xrec']):
    """Mass, asymptotic coefficient, sigma(0), N_min for a converged (b, alpha)."""
    code, xr, F, P, m, ls, Nmin, xNmin = shoot(b, al, h, x0_for(b), xmax, xrec)
    C = F * xr**2
    # tails beyond x_rec (F = C/x^2): m_tail = C^2/x^3 ; (ln sigma)_tail = alpha C^2/x^4 (both negligible)
    m_inf = m + C**2 / xr**3
    ls_inf = ls + al * C**2 / xr**4
    return dict(b=b, alpha=al, m_inf=m_inf, C=C, sigma0=math.exp(-ls_inf), Nmin=Nmin, xNmin=xNmin,
                alpha_m=al * m_inf, sqrt_alpha_m=math.sqrt(al) * m_inf if al > 0 else float('nan'))
