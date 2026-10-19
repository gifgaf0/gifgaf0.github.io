"""Independent hedgehog profile solver for the cross-check: two-sided shooting.

Radial energy density (per dx, without the 4 pi), derived below and validated numerically against the
matrix Lagrangian of cc_lib (check printed by cc_hedgehog.py):
    e(x, F, F') = x^2 F'^2/8 + s^2/4 + s^2 F'^2 + s^4/(2 x^2) + beta^2 x^2 (1 - c)/4
The Euler-Lagrange equation and the small-x / large-x series are generated with sympy here.
Inner solution: series F = pi + a x + b x^3 + c5 x^5 at x0, integrated outward (DOP853).
Outer solution: massless F = C/x^2 + d C^3/x^6 (+ ...); massive F = C (1 + beta x) e^{-beta x}/x^2,
integrated inward from X.  (a, C) are fixed by matching F, F' at x_m (scipy root).
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import root

_x, _F, _Fp, _b2 = sp.symbols('x F Fp beta2', real=True)
_s, _c = sp.sin(_F), sp.cos(_F)
E_RAD = _x ** 2 * _Fp ** 2 / 8 + _s ** 2 / 4 + _s ** 2 * _Fp ** 2 + _s ** 4 / (2 * _x ** 2) \
    + _b2 * _x ** 2 * (1 - _c) / 4

# Euler-Lagrange: d/dx (de/dF') - de/dF = 0, with F'' as unknown
_Fpp = sp.symbols('Fpp')
_dedFp = sp.diff(E_RAD, _Fp)
_total = sp.diff(_dedFp, _x) + sp.diff(_dedFp, _F) * _Fp + sp.diff(_dedFp, _Fp) * _Fpp - sp.diff(E_RAD, _F)
_Fpp_sol = sp.solve(sp.Eq(_total, 0), _Fpp)[0]
FPP = sp.lambdify((_x, _F, _Fp, _b2), _Fpp_sol, 'numpy')
EDENS = sp.lambdify((_x, _F, _Fp, _b2), E_RAD, 'numpy')


def _inner_series():
    a, b, c5 = sp.symbols('a b c5')
    X = sp.symbols('X', positive=True)
    Fs = sp.pi + a * X + b * X ** 3 + c5 * X ** 5
    res = _total.subs({_Fpp: sp.diff(Fs, X, 2)}).subs({_Fp: sp.diff(Fs, X)}).subs({_F: Fs}).subs({_x: X})
    ser = sp.series(sp.simplify(res), X, 0, 6).removeO()
    ser = sp.expand(ser)
    coeffs = sp.Poly(ser, X).all_coeffs()[::-1]
    # lowest non-trivial orders determine b, then c5
    sol_b = None
    for k, co in enumerate(coeffs):
        co = sp.simplify(co)
        if co == 0:
            continue
        if sol_b is None and co.has(b):
            sol_b = sp.solve(co, b)[0]
            continue
        if sol_b is not None and co.subs(b, sol_b).has(c5):
            sol_c = sp.solve(sp.simplify(co.subs(b, sol_b)), c5)[0]
            return sp.lambdify((a, _b2), sol_b), sp.lambdify((a, _b2), sol_c), sol_b, sol_c
    raise RuntimeError('series failed')


B_OF_A, C5_OF_A, B_EXPR, C5_EXPR = _inner_series()


def _outer_series():
    C, d = sp.symbols('C d')
    y = sp.symbols('y', positive=True)   # y = 1/x
    Fs = C / _x ** 2 + d / _x ** 6
    res = _total.subs({_Fpp: sp.diff(Fs, _x, 2)}).subs({_Fp: sp.diff(Fs, _x)}).subs({_F: Fs}).subs({_b2: 0})
    res = sp.simplify(res.subs(_x, 1 / y))
    ser = sp.expand(sp.series(res, y, 0, 9).removeO())
    # find the lowest power that contains d
    for k in range(0, 9):
        co = sp.simplify(ser.coeff(y, k))
        if co != 0 and co.has(d):
            return sp.solve(co, d)[0]
    raise RuntimeError('outer series failed')


D_EXPR = _outer_series()          # d as a function of C (expect -C^3/21 or similar)
D_OF_C = sp.lambdify(sp.symbols('C'), D_EXPR)


def rhs(x, y, beta2):
    return [y[1], FPP(x, y[0], y[1], beta2)]


def tail(x, C, beta):
    """outer asymptotic form and derivative."""
    if beta == 0:
        d = D_OF_C(C)
        return C / x ** 2 + d / x ** 6, -2 * C / x ** 3 - 6 * d / x ** 7
    z = beta * x
    f = C * (1 + z) * np.exp(-z) / x ** 2
    fp = C * np.exp(-z) * (beta / x ** 2 - (1 + z) * beta / x ** 2 - 2 * (1 + z) / x ** 3)
    return f, fp


def solve_profile(beta=0.0, x0=1e-3, xm=1.5, X=40.0, rtol=1e-13, guess=None):
    b2 = beta ** 2

    def inner(a):
        bb, cc = B_OF_A(a, b2), C5_OF_A(a, b2)
        y0 = [np.pi + a * x0 + bb * x0 ** 3 + cc * x0 ** 5, a + 3 * bb * x0 ** 2 + 5 * cc * x0 ** 4]
        return solve_ivp(rhs, (x0, xm), y0, args=(b2,), method='DOP853', rtol=rtol, atol=1e-15,
                         dense_output=True)

    def outer(C):
        f, fp = tail(X, C, beta)
        return solve_ivp(rhs, (X, xm), [f, fp], args=(b2,), method='DOP853', rtol=rtol, atol=1e-17,
                         dense_output=True)

    def resid(p):
        si, so = inner(p[0]), outer(p[1])
        return [si.y[0, -1] - so.y[0, -1], si.y[1, -1] - so.y[1, -1]]

    if guess is None:
        guess = [-1.0, 8.6] if beta == 0 else [-1.1, 8.0]
    sol = root(resid, guess, method='hybr', options={'xtol': 1e-14})
    a, C = sol.x
    si, so = inner(a), outer(C)
    return Profile(a, C, beta, x0, xm, X, si, so, resid(sol.x))


class Profile:
    def __init__(self, a, C, beta, x0, xm, X, si, so, res):
        self.a, self.C, self.beta, self.x0, self.xm, self.X = a, C, beta, x0, xm, X
        self.si, self.so, self.res = si, so, res
        self.b2 = beta ** 2

    def __call__(self, x):
        x = np.asarray(x, dtype=float)
        F = np.empty_like(x); Fp = np.empty_like(x)
        m0 = x < self.x0
        m1 = (x >= self.x0) & (x <= self.xm)
        m2 = (x > self.xm) & (x <= self.X)
        m3 = x > self.X
        if m0.any():
            a = self.a; bb = B_OF_A(a, self.b2); cc = C5_OF_A(a, self.b2); xx = x[m0]
            F[m0] = np.pi + a * xx + bb * xx ** 3 + cc * xx ** 5
            Fp[m0] = a + 3 * bb * xx ** 2 + 5 * cc * xx ** 4
        if m1.any():
            y = self.si.sol(x[m1]); F[m1], Fp[m1] = y[0], y[1]
        if m2.any():
            y = self.so.sol(x[m2]); F[m2], Fp[m2] = y[0], y[1]
        if m3.any():
            F[m3], Fp[m3] = tail(x[m3], self.C, self.beta)
        return F, Fp


def gl_panels(edges, npt=16):
    xg, wg = np.polynomial.legendre.leggauss(npt)
    xs, ws = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        xs.append(0.5 * (hi - lo) * xg + 0.5 * (hi + lo))
        ws.append(0.5 * (hi - lo) * wg)
    return np.concatenate(xs), np.concatenate(ws)


def radial_grid(xmax, npt=16):
    edges = np.concatenate([[0.0], np.geomspace(0.01, xmax, 90)])
    return gl_panels(edges, npt)
