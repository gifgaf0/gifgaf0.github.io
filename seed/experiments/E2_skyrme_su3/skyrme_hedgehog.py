#!/usr/bin/env python3
"""E2 -- the B = 1 Skyrme hedgehog, massless pions, ANW conventions.

Conventions (PLAN.md E2):
  L = (F_pi^2/16) Tr d_mu U d^mu U^dag + (1/(32 e^2)) Tr [L_mu, L_nu]^2,  L_mu = U^dag d_mu U
  F_pi in the 186-MeV convention (f_pi = F_pi/2), dimensionless radius x = e F_pi r.
  Hedgehog U0 = exp(i tau.rhat F(r)), F(0) = pi, F -> C/x^2 at large x (massless pions).

  M   = 4 pi (F_pi/e) K,  K = int dx x^2 [ (1/8)(F'^2 + 2 s^2/x^2) + (1/2)(s^2/x^2)(s^2/x^2 + 2 F'^2) ]
  I1  = (2 pi/3) Lambda / (e^3 F_pi),  Lambda = int x^2 s^2 [1 + 4(F'^2 + s^2/x^2)] dx
  I2  = (pi/2)   J2     / (e^3 F_pi),  J2     = int x^2 (1 - cos F)[1 + F'^2 + 2 s^2/x^2] dx
  gA  = -(pi/(3 e^2)) D,  D = int x^2 [F' + sin2F/x + 4(sin2F F'^2/x + 2 s^2 F'/x^2 + s^2 sin2F/x^3)] dx
        (formula read in Acus et al. hep-ph/9605435 eqs. 4.9-4.10 after x = 2 r~. verify_densities.py
         shows it is 3/2 of the ball integral of the Noether current, i.e. the q->0 transverse form
         factor with the massless pion pole, and that D = -2C exactly)

Euler-Lagrange equation (x 4 of ANW's form):
  (x^2 + 8 s^2) F'' + 2 x F' + 4 sin2F F'^2 - sin2F - 4 sin2F s^2/x^2 = 0.

Three discretisations, all Chebyshev collocation + Newton:
  (A) PRIMARY, as instructed: x in [0, X], F(0) = pi, Robin condition F' + 2F/x = 0 at X, plus
      analytic tails beyond X from F = C/x^2 - C^3/(21 x^6), C = X^2 F(X).
  (B) CROSS-CHECK: the whole half line via x = L (1+t)/(1-t); F is analytic in t on [-1,1]
      (asymptotic series in 1/x^2, no logs), so no truncation and no tail is needed.
  (C) BIAS DEMO: x in [0, X] with Dirichlet F(X) = 0 and no tails (what NOT to do).

Writes profile.json (profile on a grid) and out/hedgehog.json; prints its own checks.
Deterministic; runtime ~10 s on one core.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


# ----------------------------------------------------------------------------- spectral tools
def cheb(N):
    """Chebyshev-Gauss-Lobatto nodes t_j = cos(pi j/N) and differentiation matrix (Trefethen)."""
    t = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.hstack([2.0, np.ones(N - 1), 2.0]) * (-1.0) ** np.arange(N + 1)
    T = np.tile(t, (N + 1, 1)).T
    dT = T - T.T
    D = np.outer(c, 1.0 / c) / (dT + np.eye(N + 1))
    D = D - np.diag(D.sum(axis=1))
    return D, t


def clencurt(N):
    """Clenshaw-Curtis weights on the same nodes (Trefethen)."""
    theta = np.pi * np.arange(N + 1) / N
    w = np.zeros(N + 1)
    ii = np.arange(1, N)
    v = np.ones(N - 1)
    if N % 2 == 0:
        w[0] = w[N] = 1.0 / (N ** 2 - 1)
        for k in range(1, N // 2):
            v = v - 2.0 * np.cos(2 * k * theta[ii]) / (4 * k ** 2 - 1)
        v = v - np.cos(N * theta[ii]) / (N ** 2 - 1)
    else:
        w[0] = w[N] = 1.0 / N ** 2
        for k in range(1, (N - 1) // 2 + 1):
            v = v - 2.0 * np.cos(2 * k * theta[ii]) / (4 * k ** 2 - 1)
    w[ii] = 2.0 * v / N
    return w


def bary_weights(N):
    w = (-1.0) ** np.arange(N + 1)
    w[0] *= 0.5
    w[-1] *= 0.5
    return w


def bary_eval(tn, fn, wb, t):
    """Barycentric interpolation of nodal values fn (nodes tn) at points t."""
    t = np.atleast_1d(np.asarray(t, dtype=float))
    out = np.empty_like(t)
    for k, tk in enumerate(t):
        d = tk - tn
        j = np.where(np.abs(d) < 1e-15)[0]
        if j.size:
            out[k] = fn[j[0]]
        else:
            q = wb / d
            out[k] = np.dot(q, fn) / q.sum()
    return out


# ----------------------------------------------------------------------------- the ODE
def ode_terms(x, F, Fp, Fpp):
    """Residual G and partial derivatives dG/dF, dG/dF', dG/dF'' (x > 0)."""
    s = np.sin(F)
    s2 = s * s
    s2F = np.sin(2 * F)
    c2F = np.cos(2 * F)
    G = (x ** 2 + 8 * s2) * Fpp + 2 * x * Fp + 4 * s2F * Fp ** 2 - s2F - 4 * s2F * s2 / x ** 2
    GF = 8 * s2F * Fpp + 8 * c2F * Fp ** 2 - 2 * c2F - 4 * (2 * c2F * s2 + s2F * s2F) / x ** 2
    GFp = 2 * x + 8 * s2F * Fp
    GFpp = x ** 2 + 8 * s2
    return G, GF, GFp, GFpp


def newton(F0, build, tol=1e-13, maxit=60, verbose=False):
    """Damped Newton. Stops at |dF| < tol, or when |dF| < 1e-10 stops decreasing (round-off floor)."""
    F = F0.copy()
    prev = np.inf
    for it in range(maxit):
        R, J = build(F)
        dF = np.linalg.solve(J, -R)
        lam = 1.0
        # simple damping: keep F within a sane range during the first steps
        while np.max(np.abs(lam * dF)) > 0.5:
            lam *= 0.5
        F = F + lam * dF
        nrm = np.max(np.abs(dF))
        if verbose:
            print(f"    newton it {it:2d}  |dF| = {nrm:.3e}  lam = {lam}")
        if lam == 1.0 and (nrm < tol or (nrm < 1e-10 and nrm > 0.5 * prev)):
            R, _ = build(F)
            return F, it + 1, float(nrm)
        prev = nrm
    raise RuntimeError("Newton did not converge")


# ----------------------------------------------------------------------------- (A)/(C) finite box
def solve_box(N, X, bc="robin", verbose=False):
    D, t = cheb(N)
    x = X * (1.0 - t) / 2.0           # t=1 -> x=0 (index 0), t=-1 -> x=X (index N)
    Dx = D * (-2.0 / X)
    Dxx = Dx @ Dx
    inner = np.arange(1, N)
    wrow = 1.0 / (1.0 + x[inner] ** 2)

    def build(F):
        Fp = Dx @ F
        Fpp = Dxx @ F
        R = np.empty(N + 1)
        J = np.zeros((N + 1, N + 1))
        G, GF, GFp, GFpp = ode_terms(x[inner], F[inner], Fp[inner], Fpp[inner])
        R[inner] = wrow * G
        J[inner, :] = wrow[:, None] * (GFp[:, None] * Dx[inner, :] + GFpp[:, None] * Dxx[inner, :])
        J[inner, inner] += wrow * GF
        R[0] = F[0] - np.pi
        J[0, 0] = 1.0
        if bc == "robin":          # leading-order asymptotic condition (as instructed)
            R[N] = Fp[N] + 2.0 * F[N] / X
            J[N, :] = Dx[N, :]
            J[N, N] += 2.0 / X
        elif bc == "robin2":       # next orders: F' + 2F/x = (4/21) C^3 x^-7 + 8 C^3 x^-9, C ~ x^2 F
            R[N] = Fp[N] + 2.0 * F[N] / X - F[N] ** 3 * (4.0 / 21.0 / X + 8.0 / X ** 3)
            J[N, :] = Dx[N, :]
            J[N, N] += 2.0 / X - 3 * F[N] ** 2 * (4.0 / 21.0 / X + 8.0 / X ** 3)
        elif bc == "dirichlet":
            R[N] = F[N]
            J[N, N] = 1.0
        else:
            raise ValueError(bc)
        return R, J

    with np.errstate(over="ignore"):
        F0 = 2.0 * np.arctan((1.9365 / np.maximum(x, 1e-300)) ** 2)
    F0[0] = np.pi
    if bc == "dirichlet":
        F0 = F0 - F0[-1] * x / X
    F, its, res = newton(F0, build, verbose=verbose)
    Fp = Dx @ F
    w = clencurt(N) * (X / 2.0)        # dx = (X/2) dt
    return dict(kind="box", bc=bc, N=N, X=X, t=t, x=x, F=F, Fp=Fp, w=w, its=its, res=res)


# ----------------------------------------------------------------------------- (B) half line
def solve_mapped(N, L=2.0, verbose=False):
    D, t = cheb(N)
    # t=1 (index 0) is x=infinity, t=-1 (index N) is x=0
    inner = np.arange(1, N)
    ti = t[inner]
    x = np.full(N + 1, np.inf)
    x[1:] = L * (1 + t[1:]) / (1 - t[1:])
    x[N] = 0.0
    tx = (1 - ti) ** 2 / (2 * L)
    txx = -(1 - ti) ** 3 / (2 * L ** 2)
    D2 = D @ D
    xi = x[inner]
    wrow = 4.0 / ((1 + ti) ** 2 * (1 - ti) ** 2)     # = 1/(x^2 tx^2)

    def build(F):
        Ft = D @ F
        Ftt = D2 @ F
        Fp = tx * Ft[inner]
        Fpp = tx ** 2 * Ftt[inner] + txx * Ft[inner]
        G, GF, GFp, GFpp = ode_terms(xi, F[inner], Fp, Fpp)
        R = np.empty(N + 1)
        J = np.zeros((N + 1, N + 1))
        R[inner] = wrow * G
        dFp = tx[:, None] * D[inner, :]
        dFpp = (tx ** 2)[:, None] * D2[inner, :] + txx[:, None] * D[inner, :]
        J[inner, :] = wrow[:, None] * (GFp[:, None] * dFp + GFpp[:, None] * dFpp)
        J[inner, inner] += wrow * GF
        R[0] = F[0]
        J[0, 0] = 1.0
        R[N] = F[N] - np.pi
        J[N, N] = 1.0
        return R, J

    xs = np.where(np.isfinite(x), x, 1e300)
    with np.errstate(over="ignore"):
        F0 = 2.0 * np.arctan((1.9365 / np.maximum(xs, 1e-300)) ** 2)
    F0[N] = np.pi
    F0[0] = 0.0
    F, its, res = newton(F0, build, verbose=verbose)
    Ft = D @ F
    Ftt = D2 @ F
    Fp = np.zeros(N + 1)
    Fp[1:] = (1 - t[1:]) ** 2 / (2 * L) * Ft[1:]
    C = 2.0 * L ** 2 * Ftt[0]                  # F ~ C (1-t)^2/(4 L^2) near t = 1
    wt = clencurt(N)
    xt = np.full(N + 1, np.inf)
    xt[1:] = 2 * L / (1 - t[1:]) ** 2           # dx/dt
    return dict(kind="mapped", N=N, L=L, t=t, x=x, F=F, Fp=Fp, Ft=Ft, C=C, wt=wt, xt=xt,
                its=its, res=res, D=D)


# ----------------------------------------------------------------------------- integrands
def sin2F_minus_2F(F):
    """sin(2F) - 2F without cancellation for small F."""
    y = 2.0 * F
    out = np.sin(y) - y
    small = np.abs(y) < 0.05
    ys = y[small]
    out[small] = -ys ** 3 / 6 + ys ** 5 / 120 - ys ** 7 / 5040 + ys ** 9 / 362880
    return out


def densities(x, F, Fp):
    """Radial integrands (per dx) of K, E2, E4, Lambda, J2, the g_A bracket (IBP form, without the
    boundary term C), baryon number and baryon-density <r^2>. At x = 0 every integrand vanishes."""
    x = np.asarray(x, float)
    out = {}
    pos = x > 0
    xs = np.where(pos, x, 1.0)
    s = np.sin(F)
    s2 = s * s
    c = np.cos(F)
    s2F = np.sin(2 * F)
    q = np.where(pos, s2 / xs ** 2, 0.0)              # s^2/x^2
    e2 = 0.125 * (x ** 2 * Fp ** 2 + 2 * s2)
    e4 = 0.5 * s2 * (q + 2 * Fp ** 2)
    out["E2"] = e2
    out["E4"] = e4
    out["K"] = e2 + e4
    out["Lambda"] = x ** 2 * s2 * (1 + 4 * (Fp ** 2 + q))
    omc = 2 * np.sin(F / 2) ** 2                       # 1 - cos F without cancellation
    out["J2"] = x ** 2 * omc * (1 + Fp ** 2 + 2 * q)
    # g_A bracket: int x^2[F' + sin2F/x] = C + int x (sin2F - 2F)  (x^2 F -> C, 0 at x = 0)
    gA = x * sin2F_minus_2F(F) + 4 * (x * s2F * Fp ** 2 + 2 * s2 * Fp + np.where(pos, s2 * s2F / xs, 0.0))
    out["gA_bulk"] = gA
    out["B"] = -(2.0 / np.pi) * s2 * Fp
    out["r2B"] = -(2.0 / np.pi) * x ** 2 * s2 * Fp
    for k in out:
        out[k] = np.where(pos, out[k], 0.0)
    return out


def C_from_FX(FX, X):
    """Invert F(X) = C/X^2 - C^3/(21 X^6) - (4/3) C^3/X^8 for C (fixed point)."""
    C = X ** 2 * FX
    for _ in range(20):
        C = X ** 2 * FX + C ** 3 / (21.0 * X ** 4) + (4.0 / 3.0) * C ** 3 / X ** 6
    return C


def tails(C, X):
    """Analytic integrals over [X, inf) from F = C/x^2 - C^3/(21 x^6) - (4/3) C^3/x^8 + O(x^-10)
    (the x^-6 term comes from the sigma-model nonlinearity, the x^-8 term from the Skyrme term)."""
    E2t = C ** 2 / (4 * X ** 3) - C ** 4 / (28 * X ** 7) - (2.0 / 3.0) * C ** 4 / X ** 9
    E4t = C ** 4 / (2 * X ** 9)
    return {
        "E2": E2t,
        "E4": E4t,
        "K": E2t + E4t,
        "Lambda": C ** 2 / X - (3.0 / 35.0) * C ** 4 / X ** 5 + (52.0 / 21.0) * C ** 4 / X ** 7,
        "J2": C ** 2 / (2 * X) - C ** 4 / (56 * X ** 5) + (5.0 / 21.0) * C ** 4 / X ** 7,
        "gA_bulk": -(1.0 / 3.0) * C ** 3 / X ** 4 + 4 * C ** 3 / X ** 6 + 0.0,
        "B": (2.0 / (3.0 * np.pi)) * C ** 3 / X ** 6,
        "r2B": C ** 3 / (np.pi * X ** 4),
    }
# gA_bulk tail: x(sin2F-2F) ~ -(4/3) C^3 x^-5 -> -(1/3) C^3/X^4 ; Skyrme part ~ 24 C^3 x^-7 -> 4 C^3/X^6


def integrals_box(sol, with_tails=True):
    d = densities(sol["x"], sol["F"], sol["Fp"])
    X = sol["X"]
    FX = sol["F"][-1]
    C = C_from_FX(FX, X)
    res = {k: float(np.dot(sol["w"], v)) for k, v in d.items()}
    if with_tails:
        tl = tails(C, X)
        for k in res:
            res[k] += tl[k]
        res["gA_D"] = res["gA_bulk"] + C        # C = lim x^2 F; box: X^2 F(X) + tail-consistent
    else:
        # no tails: honest truncated sphere integral int_0^X x^2[F' + sin2F/x + ...]
        res["gA_D"] = res["gA_bulk"] + X ** 2 * FX
    res["C"] = float(C)
    res["Fp0"] = float(sol["Fp"][0])
    return res


def integrals_mapped(sol):
    t, x, F, Fp, C, L = sol["t"], sol["x"], sol["F"], sol["Fp"], sol["C"], sol["L"]
    xf = np.where(np.isfinite(x), x, 0.0)
    d = densities(xf, F, Fp)
    lim = {"Lambda": C ** 2 / (2 * L), "J2": C ** 2 / (4 * L)}   # (a/x^2) dx/dt -> a/(2L) at t = 1
    res = {}
    for k, v in d.items():
        g = np.empty_like(v)
        g[1:] = v[1:] * sol["xt"][1:]
        g[0] = lim.get(k, 0.0)
        res[k] = float(np.dot(sol["wt"], g))
    res["gA_D"] = res["gA_bulk"] + C
    res["C"] = float(C)
    res["Fp0"] = float(Fp[-1])
    return res


def derived(I):
    K = I["K"]
    return {
        "M_over_Fpi_e": 4 * np.pi * K,                       # M_cl / (F_pi/e)
        "M_over_3pi2": 4 * np.pi * K / (3 * np.pi ** 2),    # = E/(12 pi^2) in Skyrme units
        "Lambda": I["Lambda"],
        "I1_coef": 2 * np.pi / 3 * I["Lambda"],             # I1 * e^3 F_pi
        "J2": I["J2"],
        "I2_coef": np.pi / 2 * I["J2"],                     # I2 * e^3 F_pi
        "I1_over_I2": (2 * np.pi / 3 * I["Lambda"]) / (np.pi / 2 * I["J2"]),
        "D_gA": I["gA_D"],
        "gA_times_e2": -np.pi / 3 * I["gA_D"],              # g_A * e^2
        "E2_over_E4": I["E2"] / I["E4"],
        "virial_dev": I["E2"] / I["E4"] - 1.0,
        "B": I["B"],
        "r2B": I["r2B"],                                    # <r^2>_B (e F_pi)^2
        "C": I["C"],
        "Fp0": I["Fp0"],
    }


# ----------------------------------------------------------------------------- arctan ansatz
def arctan_ansatz(x0, n=4000):
    """Integrals for F = 2 arctan(x0^2/x^2) (Praszalowicz hep-ph/0308114 eq. 25) by quadrature."""
    from scipy.integrate import quad
    def F(x):
        return 2 * np.arctan(x0 ** 2 / x ** 2)
    def Fp(x):
        return -4 * x0 ** 2 * x / (x ** 4 + x0 ** 4)
    out = {}
    for k in ["K", "Lambda", "J2"]:
        f = lambda x, k=k: float(densities(np.array([x]), np.array([F(x)]), np.array([Fp(x)]))[k][0])
        out[k] = quad(f, 0, np.inf, limit=400, epsabs=1e-13, epsrel=1e-12)[0]
    return out


# ----------------------------------------------------------------------------- main
def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    print("E2 hedgehog: Chebyshev collocation, massless pions, ANW units x = e F_pi r\n")

    # (B) reference: whole half line
    print("(B) half-line map x = L(1+t)/(1-t): N-convergence")
    ref = {}
    for N in [40, 60, 80, 120, 160]:
        s = solve_mapped(N, L=2.0)
        d = derived(integrals_mapped(s))
        ref[N] = (s, d)
        print(f"  N={N:4d}  M/(F/e)={d['M_over_Fpi_e']:.12f}  Lambda={d['Lambda']:.10f}  "
              f"J2={d['J2']:.10f}  D={d['D_gA']:.10f}  E2/E4-1={d['virial_dev']:+.2e}  "
              f"C={d['C']:.10f}  F'(0)={d['Fp0']:.10f}  newton={s['its']} last|dF|={s['res']:.1e}")
    sB, dB = ref[160]
    # map-parameter independence
    sB2 = solve_mapped(160, L=1.0)
    dB2 = derived(integrals_mapped(sB2))
    sB3 = solve_mapped(160, L=4.0)
    dB3 = derived(integrals_mapped(sB3))
    print("  L=1, N=160 : M/(F/e)={:.12f} Lambda={:.10f} J2={:.10f} D={:.10f}".format(
        dB2['M_over_Fpi_e'], dB2['Lambda'], dB2['J2'], dB2['D_gA']))
    print("  L=4, N=160 : M/(F/e)={:.12f} Lambda={:.10f} J2={:.10f} D={:.10f}".format(
        dB3['M_over_Fpi_e'], dB3['Lambda'], dB3['J2'], dB3['D_gA']))

    # (A) primary: box + Robin + tails
    print("\n(A) PRIMARY box [0,X], Robin F'+2F/x=0 at X, analytic tails: convergence in N and X")
    boxA = {}
    for X in [10.0, 20.0, 40.0, 80.0]:
        for N in [100, 200]:
            s = solve_box(N, X, "robin")
            I = integrals_box(s, with_tails=True)
            d = derived(I)
            I0 = integrals_box(s, with_tails=False)
            d0 = derived(I0)
            boxA[(X, N)] = (s, d, d0)
            print(f"  X={X:5.0f} N={N:4d}  M/(F/e)={d['M_over_Fpi_e']:.12f}  Lambda={d['Lambda']:.10f} "
                  f"(no tail {d0['Lambda']:.6f})  J2={d['J2']:.10f} (no tail {d0['J2']:.6f})  "
                  f"D={d['D_gA']:.10f}  E2/E4-1={d['virial_dev']:+.2e}  C={d['C']:.8f}")
    sA, dA, dA0 = boxA[(40.0, 200)]
    print("  improved Robin condition (next two asymptotic orders), N=200:")
    boxR2 = {}
    for X in [10.0, 20.0, 40.0]:
        s = solve_box(200, X, "robin2")
        d = derived(integrals_box(s, with_tails=True))
        boxR2[X] = d
        print(f"  X={X:5.0f} N= 200  M/(F/e)={d['M_over_Fpi_e']:.12f}  Lambda={d['Lambda']:.10f}  "
              f"J2={d['J2']:.10f}  D={d['D_gA']:.10f}  E2/E4-1={d['virial_dev']:+.2e}")

    # (C) Dirichlet F(X)=0, no tails: the bias
    print("\n(C) box with Dirichlet F(X)=0 and no tails (biased; shown for comparison)")
    dirich = {}
    for X in [10.0, 20.0, 40.0]:
        s = solve_box(200, X, "dirichlet")
        d = derived(integrals_box(s, with_tails=False))
        dirich[X] = d
        print(f"  X={X:5.0f}  M/(F/e)={d['M_over_Fpi_e']:.8f} ({(d['M_over_Fpi_e']/dB['M_over_Fpi_e']-1)*100:+.3f}%)"
              f"  Lambda={d['Lambda']:.6f} ({(d['Lambda']/dB['Lambda']-1)*100:+.2f}%)"
              f"  J2={d['J2']:.6f} ({(d['J2']/dB['J2']-1)*100:+.2f}%)")

    # independent non-spectral cross-check: scipy solve_bvp on [eps, X] with Robin BC + tails
    from scipy.integrate import solve_bvp, quad
    X = 40.0
    eps = 1e-3
    a0 = -dB["Fp0"]

    def fun(x, y):
        F, Fp = y
        s2 = np.sin(F) ** 2
        s2F = np.sin(2 * F)
        Fpp = -(2 * x * Fp + 4 * s2F * Fp ** 2 - s2F - 4 * s2F * s2 / x ** 2) / (x ** 2 + 8 * s2)
        return np.vstack([Fp, Fpp])

    def bc(ya, yb):
        # F(eps) = pi - a eps (series; a free) <=> F'(eps)*eps + (F(eps)-pi) = O(eps^3)
        return np.array([ya[0] - np.pi - ya[1] * eps, yb[1] + 2 * yb[0] / X])

    xg = np.linspace(eps, X, 4000)
    xg = eps + (X - eps) * (np.linspace(0, 1, 4000)) ** 2
    Fg = 2 * np.arctan((1.9365 / xg) ** 2)
    Fpg = -4 * 1.9365 ** 2 * xg / (xg ** 4 + 1.9365 ** 4)
    bv = solve_bvp(fun, bc, xg, np.vstack([Fg, Fpg]), tol=1e-10, max_nodes=200000)
    def dens_at(x, k):
        y = bv.sol(x)
        return float(densities(np.array([x]), np.array([y[0]]), np.array([y[1]]))[k][0])
    CX = X ** 2 * bv.sol(X)[0]
    tl = tails(CX, X)
    bvp = {}
    for k in ["K", "Lambda", "J2", "E2", "E4"]:
        brk = [eps, 0.5, 1, 2, 4, 8, 16, X]
        val = sum(quad(lambda x: dens_at(x, k), brk[i], brk[i + 1], limit=200, epsabs=1e-12, epsrel=1e-11)[0]
                  for i in range(len(brk) - 1))
        bvp[k] = val + tl[k]
    bvp_M = 4 * np.pi * bvp["K"]
    print(f"\nscipy solve_bvp cross-check (X=40, tol 1e-10, status {bv.status}, {bv.x.size} nodes): "
          f"M/(F/e)={bvp_M:.9f} Lambda={bvp['Lambda']:.8f} J2={bvp['J2']:.8f} E2/E4-1={bvp['E2']/bvp['E4']-1:+.1e}"
          f" F'(0)~{bv.sol(eps)[1]:.8f}")

    # arctan ansatz comparison (Praszalowicz)
    x0 = np.sqrt(15.0 / 4.0)
    arc = arctan_ansatz(x0)
    arc_M = 4 * np.pi * arc["K"]
    arc_I1 = 2 * np.pi / 3 * arc["Lambda"]
    arc_I2 = np.pi / 2 * arc["J2"]
    # Praszalowicz closed forms (eqs. 26-28, as read): M = (F/e) pi^2 (3 sqrt2/16)(4x0+15/x0),
    # I1 = pi^2 (sqrt2/12)(6x0^3+25x0)/(e^3F), I2 = pi^2 (sqrt2/16)(4x0^3+9x0)/(e^3F)
    pr_M = np.pi ** 2 * 3 * np.sqrt(2) / 16 * (4 * x0 + 15 / x0)
    pr_I1 = np.pi ** 2 * np.sqrt(2) / 12 * (6 * x0 ** 3 + 25 * x0)
    pr_I2 = np.pi ** 2 * np.sqrt(2) / 16 * (4 * x0 ** 3 + 9 * x0)
    print(f"\narctan ansatz x0=sqrt(15/4): quadrature M/(F/e)={arc_M:.6f} I1coef={arc_I1:.6f} I2coef={arc_I2:.6f}")
    print(f"   Praszalowicz closed forms:   M/(F/e)={pr_M:.6f} I1coef={pr_I1:.6f} I2coef={pr_I2:.6f}")

    # ------------------------------------------------------------------ checks
    print("\nCHECKS")
    ok = True
    def chk(name, cond, detail):
        nonlocal ok
        ok &= bool(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")
    chk("spectral convergence (B) N=120 vs 160", abs(ref[120][1]['Lambda'] - dB['Lambda']) < 1e-9,
        f"dLambda = {abs(ref[120][1]['Lambda'] - dB['Lambda']):.1e}")
    chk("map-parameter independence (L=1,2,4)", max(abs(dB2['Lambda'] - dB['Lambda']), abs(dB3['Lambda'] - dB['Lambda'])) < 1e-8,
        f"max dLambda = {max(abs(dB2['Lambda'] - dB['Lambda']), abs(dB3['Lambda'] - dB['Lambda'])):.1e}")
    for key in ["M_over_Fpi_e", "Lambda", "J2", "D_gA"]:
        rel = abs(dA[key] / dB[key] - 1)
        chk(f"(A) box X=40 + tails vs (B) half line: {key}", rel < 1e-6, f"rel diff {rel:.1e}")
    for key in ["M_over_Fpi_e", "Lambda", "J2", "D_gA"]:
        rel = abs(boxA[(80.0, 200)][1][key] / dB[key] - 1)
        chk(f"(A) box X=80 + tails vs (B) half line: {key}", rel < 2e-7, f"rel diff {rel:.1e}")
    rel = abs(boxA[(10.0, 200)][1]['Lambda'] / dB['Lambda'] - 1)
    chk("(A) X=10 with tails: error of size C^2/(21 X^4) ~ 4e-4 expected", rel < 1e-3, f"Lambda rel diff {rel:.1e}")
    rel = max(abs(boxR2[40.0][k] / dB[k] - 1) for k in ["M_over_Fpi_e", "Lambda", "J2", "D_gA"])
    chk("improved Robin condition, X=40", rel < 1e-8, f"max rel diff {rel:.1e}")
    chk("virial E2 = E4 (B)", abs(dB['virial_dev']) < 1e-10, f"E2/E4-1 = {dB['virial_dev']:.1e}")
    chk("virial E2 = E4 (A)", abs(dA['virial_dev']) < 1e-8, f"E2/E4-1 = {dA['virial_dev']:.1e}")
    chk("baryon number", abs(dB['B'] - 1) < 1e-11, f"B = {dB['B']:.14f}")
    chk("solve_bvp agrees with spectral (M, Lambda)", abs(bvp_M / dB['M_over_Fpi_e'] - 1) < 1e-6 and abs(bvp['Lambda'] / dB['Lambda'] - 1) < 1e-6,
        f"rel {abs(bvp_M / dB['M_over_Fpi_e'] - 1):.1e}, {abs(bvp['Lambda'] / dB['Lambda'] - 1):.1e}")
    chk("arctan closed forms reproduce by quadrature", abs(arc_I2 / pr_I2 - 1) < 1e-8 and abs(arc_M / pr_M - 1) < 1e-8,
        f"rel {abs(arc_M/pr_M-1):.1e}, {abs(arc_I1/pr_I1-1):.1e}, {abs(arc_I2/pr_I2-1):.1e}")
    # asymptotic form: x^2 F -> C - C^3/(21 x^4)
    xs = np.array([10.0, 20.0, 40.0])
    tt = (xs - sB['L']) / (xs + sB['L'])
    Fs = bary_eval(sB['t'], sB['F'], bary_weights(sB['N']), tt)
    C = dB['C']
    pred1 = C / xs ** 2
    pred = C / xs ** 2 - C ** 3 / (21 * xs ** 6) - (4.0 / 3.0) * C ** 3 / xs ** 8
    dev1 = np.abs(Fs / pred1 - 1)
    dev = np.abs(Fs / pred - 1)
    print("  asymptotics: |F/(C/x^2) - 1| =", ", ".join(f"{v:.1e}" for v in dev1),
          "; with -C^3/(21x^6) - (4/3)C^3/x^8:", ", ".join(f"{v:.1e}" for v in dev), " (x = 10, 20, 40)")
    chk("asymptotics F = C/x^2 - C^3/(21 x^6) - (4/3) C^3/x^8", np.max(dev[1:]) < 1e-6 and dev[0] < 1e-5,
        f"rel dev {dev[0]:.1e}, {dev[1]:.1e}, {dev[2]:.1e} at x = 10, 20, 40")

    # ------------------------------------------------------------------ outputs
    # profile.json from the half-line reference solution
    xgrid = np.concatenate([np.linspace(0, 20, 2001), np.linspace(20.5, 100, 160)])
    tg = np.where(xgrid > 0, (xgrid - sB['L']) / (xgrid + sB['L']), -1.0)
    wb = bary_weights(sB['N'])
    Fgrid = bary_eval(sB['t'], sB['F'], wb, tg)
    Ftg = bary_eval(sB['t'], sB['Ft'], wb, tg)
    Fpgrid = (1 - tg) ** 2 / (2 * sB['L']) * Ftg
    prof = {
        "description": "B=1 Skyrme hedgehog profile F(x), massless pions, ANW conventions",
        "conventions": "L = (F_pi^2/16) Tr dU dU^dag + (1/(32 e^2)) Tr[L_mu,L_nu]^2, F_pi in the 186-MeV "
                       "convention, x = e F_pi r; U = exp(i tau.rhat F), F(0) = pi",
        "method": "Chebyshev collocation on the whole half line, x = L(1+t)/(1-t), L = 2, N = 160; "
                  "agrees with the box [0,40] + Robin BC + analytic tails to <1e-8",
        "asymptotics": "F(x) = C/x^2 - C^3/(21 x^6) - (4/3) C^3/x^8 + O(x^-10); use beyond x = 100",
        "C": dB['C'], "Fprime0": dB['Fp0'],
        "M_over_Fpi_e": dB['M_over_Fpi_e'], "Lambda": dB['Lambda'], "J2": dB['J2'],
        "x": [round(v, 6) for v in xgrid.tolist()],
        "F": [float(f"{v:.12e}") for v in Fgrid.tolist()],
        "dFdx": [float(f"{v:.12e}") for v in Fpgrid.tolist()],
    }
    with open(os.path.join(HERE, "profile.json"), "w") as f:
        json.dump(prof, f, indent=0)

    out = {
        "reference_halfline_N160": dB,
        "halfline_N_convergence": {str(N): ref[N][1] for N in ref},
        "halfline_L1": dB2, "halfline_L4": dB3,
        "primary_box_X40_N200_tails": dA,
        "primary_box_X40_N200_no_tails": dA0,
        "box_improved_robin_N200": {f"X{int(X)}": d for X, d in boxR2.items()},
        "box_convergence": {f"X{int(X)}_N{N}": v[1] for (X, N), v in boxA.items()},
        "box_no_tail": {f"X{int(X)}_N{N}": v[2] for (X, N), v in boxA.items()},
        "dirichlet_no_tails": {f"X{int(X)}": d for X, d in dirich.items()},
        "solve_bvp_X40": {"M_over_Fpi_e": bvp_M, "Lambda": bvp["Lambda"], "J2": bvp["J2"],
                           "E2_over_E4": bvp["E2"] / bvp["E4"], "nodes": int(bv.x.size), "status": int(bv.status)},
        "arctan_ansatz": {"x0": x0, "M_over_Fpi_e": arc_M, "I1_coef": arc_I1, "I2_coef": arc_I2,
                          "Praszalowicz_closed_forms": {"M_over_Fpi_e": pr_M, "I1_coef": pr_I1, "I2_coef": pr_I2}},
        "all_checks_pass": bool(ok),
        "runtime_s": time.time() - t0,
    }
    with open(os.path.join(OUT, "hedgehog.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\nall checks pass: {ok};  runtime {time.time() - t0:.1f} s")
    print("wrote profile.json and out/hedgehog.json")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
