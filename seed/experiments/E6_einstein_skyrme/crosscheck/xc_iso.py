#!/usr/bin/env python3
"""
Cross-check of E6 in ISOTROPIC gauge with a Chebyshev pseudo-spectral Newton solver
on the compactified radius x = L s/(1-s), s in [0,1] (s = 1 is spatial infinity).

   ds^2 = -A^2 dt^2 + psi^4 (dx^2 + x^2 dOmega^2),   x = e f r,  alpha = 4 pi G f^2
   Lap psi = -(alpha/2) rho psi^5                               (Hamiltonian constraint)
   (x^2 psi^2 A')' = alpha x^2 psi^6 A (rho + p_r + 2 p_t)       (R^t_t equation)
   EL[F] from  int A psi^6 x^2 rho dx                            (matter)
   BC: F(0)=pi, psi'(0)=A'(0)=0;  F(inf)=0, psi(inf)=A(inf)=1.
Masses (units 4 pi f/e, same as the original's m(inf)):
   m_ADM  = mu/alpha with psi -> 1 + mu/(2x)   and   m_ADM = int x^2 rho psi^5 dx
   m_Komar = int x^2 psi^6 A (rho+p_r+2p_t) dx  (= lapse fall-off) -- must equal m_ADM.
The fold (alpha_crit) is located WITHOUT maximising alpha over a shooting parameter:
pseudo-arclength continuation from the flat skyrmion, then a Moore-Spence extended
system  G(U,alpha)=0, G_U v = 0, l.v = 1  solved by Newton.
Jacobians by complex-step differentiation (exact to round-off).
"""
import json, sys, time
import numpy as np
import sympy as sp

HERE = '/home/user/gifgaf0.github.io/seed/experiments/E6_einstein_skyrme/crosscheck/'

# ------------------------------------------------------------------ symbolic -> numeric
_eq = json.load(open(HERE + 'xc_equations.json'))['iso']
x_ = sp.Symbol('x', real=True)
Ff, Pf, Af = sp.Function('F')(x_), sp.Function('psi')(x_), sp.Function('A')(x_)
syms = sp.symbols('xx F Fx Fxx P Px Pxx A Ax Axx')
sub = [(sp.Derivative(Ff, (x_, 2)), syms[3]), (sp.Derivative(Pf, (x_, 2)), syms[6]),
       (sp.Derivative(Af, (x_, 2)), syms[9]), (sp.Derivative(Ff, x_), syms[2]),
       (sp.Derivative(Pf, x_), syms[5]), (sp.Derivative(Af, x_), syms[8]),
       (Ff, syms[1]), (Pf, syms[4]), (Af, syms[7]), (x_, syms[0])]


def _load(key):
    expr = eval(_eq[key], {**{k: getattr(sp, k) for k in dir(sp) if not k.startswith('_')}})
    for a, b in sub:
        expr = expr.subs(a, b)
    return expr


EL = _load('EL')
c2 = sp.diff(EL, syms[3])
ELn = sp.simplify(EL / c2)
rho_e, pr_e, pt_e = _load('rho'), _load('pr'), _load('pt')
f_EL = sp.lambdify(syms, ELn, 'numpy')
f_rho = sp.lambdify(syms, rho_e, 'numpy')
f_pr = sp.lambdify(syms, pr_e, 'numpy')
f_pt = sp.lambdify(syms, pt_e, 'numpy')


# ------------------------------------------------------------------ grid
class Grid:
    def __init__(self, N, L):
        self.N, self.L = N, L
        j = np.arange(N + 1)
        z = np.cos(np.pi * j / N)          # 1 .. -1
        s = (1 - z) / 2                    # 0 .. 1
        self.s = s
        c = np.ones(N + 1); c[0] = c[-1] = 2; c *= (-1) ** j
        S = np.tile(s, (N + 1, 1)).T
        dS = S - S.T
        D = np.outer(c, 1 / c) / (dS + np.eye(N + 1))
        D = D - np.diag(D.sum(axis=1))
        self.D = D
        self.D2 = D @ D
        self.bw = c.astype(float) * 0 + ((-1.0) ** j); self.bw[0] *= 0.5; self.bw[-1] *= 0.5
        si = s[1:-1]
        self.si = si
        self.x = L * si / (1 - si)
        self.sx = (1 - si) ** 2 / L
        self.sxx = -2 * (1 - si) ** 3 / L ** 2
        # Clenshaw-Curtis weights on [0,1]
        self.wcc = clenshaw_curtis(N) / 2.0

    def interp(self, vals, snew):
        """barycentric Chebyshev interpolation of nodal values to points snew"""
        s, w = self.s, self.bw
        d = snew[:, None] - s[None, :]
        exact = np.isclose(d, 0, atol=1e-15)
        d[exact] = 1
        q = w[None, :] / d
        out = (q @ vals) / q.sum(axis=1)
        r, cidx = np.nonzero(exact)
        out[r] = vals[cidx]
        return out


def clenshaw_curtis(N):
    theta = np.pi * np.arange(N + 1) / N
    w = np.zeros(N + 1)
    v = np.ones(N - 1)
    if N % 2 == 0:
        w[0] = w[N] = 1.0 / (N ** 2 - 1)
        for k in range(1, N // 2):
            v -= 2 * np.cos(2 * k * theta[1:-1]) / (4 * k ** 2 - 1)
        v -= np.cos(N * theta[1:-1]) / (N ** 2 - 1)
    else:
        w[0] = w[N] = 1.0 / N ** 2
        for k in range(1, (N - 1) // 2 + 1):
            v -= 2 * np.cos(2 * k * theta[1:-1]) / (4 * k ** 2 - 1)
    w[1:-1] = 2 * v / N
    return w   # on [-1,1]


# ------------------------------------------------------------------ residual
def fields(U, g):
    n = g.N + 1
    return U[:n], U[n:2 * n], U[2 * n:]


def pointwise(U, g):
    F, P, A = fields(U, g)
    D, D2 = g.D, g.D2
    out = []
    for f in (F, P, A):
        fs, fss = D @ f, D2 @ f
        fi, fsi, fssi = f[1:-1], fs[1:-1], fss[1:-1]
        fx = fsi * g.sx
        fxx = fssi * g.sx ** 2 + fsi * g.sxx
        out.append((fi, fx, fxx))
    return out, (F, P, A)


def residual(U, alpha, g):
    (Fi, Fx, Fxx), (Pi, Px, Pxx), (Ai, Ax, Axx) = pointwise(U, g)[0]
    F, P, A = fields(U, g)
    x = g.x
    args = (x, Fi, Fx, Fxx, Pi, Px, Pxx, Ai, Ax, Axx)
    rho = f_rho(*args); pr = f_pr(*args); pt = f_pt(*args)
    sc = 1.0 / g.sx ** 2
    # EL(alpha-independent form) contains A, psi derivatives; normalised to F'' coefficient 1
    RF = f_EL(*args) * sc
    RP = (Pxx + 2 * Px / x + 0.5 * alpha * rho * Pi ** 5) * sc
    RA = (Axx + (2 / x + 2 * Px / Pi) * Ax - alpha * Pi ** 4 * Ai * (rho + pr + 2 * pt)) * sc
    Ds = g.D
    bc = [F[0] - np.pi, F[-1], (Ds @ P)[0], P[-1] - 1.0, (Ds @ A)[0], A[-1] - 1.0]
    R = np.concatenate([[bc[0]], RF, [bc[1]], [bc[2]], RP, [bc[3]], [bc[4]], RA, [bc[5]]])
    return R


def jac(U, alpha, g, with_alpha=True):
    n = U.size
    h = 1e-30
    J = np.empty((n, n + (1 if with_alpha else 0)))
    Uc = U.astype(complex)
    for k in range(n):
        Uc[k] += 1j * h
        J[:, k] = residual(Uc, alpha, g).imag / h
        Uc[k] -= 1j * h
    if with_alpha:
        J[:, n] = residual(U.astype(complex), alpha + 1j * h, g).imag / h
    return J


def newton(U, alpha, g, tol=1e-12, maxit=30, verbose=False):
    for it in range(maxit):
        R = residual(U, alpha, g)
        J = jac(U, alpha, g, with_alpha=False)
        dU = np.linalg.solve(J, -R)
        U = U + dU
        if verbose:
            print(it, np.abs(R).max(), np.abs(dU).max())
        if np.abs(dU).max() < tol:
            return U, True
    return U, False


# ------------------------------------------------------------------ diagnostics
def masses(U, alpha, g):
    (Fi, Fx, Fxx), (Pi, Px, Pxx), (Ai, Ax, Axx) = pointwise(U, g)[0]
    x = g.x
    args = (x, Fi, Fx, Fxx, Pi, Px, Pxx, Ai, Ax, Axx)
    rho = f_rho(*args); pr = f_pr(*args); pt = f_pt(*args)
    dxds = g.L / (1 - g.si) ** 2
    w = g.wcc[1:-1]
    m_int = np.sum(w * x ** 2 * rho * Pi ** 5 * dxds)
    m_kom = np.sum(w * x ** 2 * Pi ** 6 * Ai * (rho + pr + 2 * pt) * dxds)
    F, P, A = fields(U, g)
    Ps1 = (g.D @ P)[-1]
    As1 = (g.D @ A)[-1]
    mu_adm = -2 * g.L * Ps1
    mu_kom = g.L * As1
    E2 = np.sum(w * x ** 2 * 0.5 * (Fx ** 2 + 2 * np.sin(Fi) ** 2 / x ** 2) * dxds)
    E4 = np.sum(w * x ** 2 * np.sin(Fi) ** 2 / x ** 2 * (Fx ** 2 + 0.5 * np.sin(Fi) ** 2 / x ** 2) * dxds)
    vonlaue = np.sum(w * x ** 2 * Pi ** 6 * Ai * (pr + 2 * pt) * dxds)
    return dict(m_int=m_int, m_komar_int=m_kom, mu_adm=mu_adm, mu_komar=mu_kom,
                m_adm_tail=(mu_adm / alpha if alpha > 0 else np.nan),
                m_komar_tail=(mu_kom / alpha if alpha > 0 else np.nan),
                E2_flatform=E2, E4_flatform=E4, tolman_minus_rho_int=vonlaue)


def central(U, g):
    F, P, A = fields(U, g)
    Fs0 = (g.D @ F)[0]
    b_iso = -Fs0 / g.L            # dx/ds = L at s=0
    psi0 = P[0]
    b_schw = b_iso / psi0 ** 2    # areal radius R = x psi^2 -> dR/dx(0) = psi0^2
    return dict(b_iso=b_iso, psi0=psi0, A0=A[0], b_schw=b_schw)


def N_profile(U, g, ns=4000):
    """N = g^{RR} = (1 + 2 x psi'/psi)^2 vs areal radius R = x psi^2, on a dense grid."""
    F, P, A = fields(U, g)
    sd = np.linspace(1e-6, 0.999, ns)
    Pd = g.interp(P, sd); Psd = g.interp(g.D @ P, sd)
    xd = g.L * sd / (1 - sd)
    Pxd = Psd * (1 - sd) ** 2 / g.L
    N = (1 + 2 * xd * Pxd / Pd) ** 2
    R = xd * Pd ** 2
    return R, N, xd


def Grr_residual(U, alpha, g):
    """max |G^x_x - 2 alpha p_r| (not imposed; follows from Bianchi + regularity)."""
    (Fi, Fx, Fxx), (Pi, Px, Pxx), (Ai, Ax, Axx) = pointwise(U, g)[0]
    x = g.x
    args = (x, Fi, Fx, Fxx, Pi, Px, Pxx, Ai, Ax, Axx)
    pr = f_pr(*args)
    Gxx = f_Gxx(*args)
    return np.max(np.abs(Gxx - 2 * alpha * pr)), np.max(np.abs(2 * alpha * pr)) + 1e-300


f_Gxx = sp.lambdify(syms, _load('Gxx'), 'numpy')


def regrid(U, g_old, g_new):
    """move a solution to a new grid (different N and/or L) by Chebyshev interpolation in x."""
    F, P, A = fields(U, g_old)
    xs = g_new.L * g_new.s / np.where(g_new.s < 1, 1 - g_new.s, 1)
    s_old = np.where(g_new.s < 1, xs / (xs + g_old.L), 1.0)
    return np.concatenate([g_old.interp(F, s_old), g_old.interp(P, s_old), g_old.interp(A, s_old)])


def flat_guess(g, c=1.08):
    s = g.s
    x = np.where(s < 1, g.L * s / np.where(s < 1, 1 - s, 1), np.inf)
    F = np.where(s < 1, 2 * np.arctan(c / np.where(x > 0, x, 1e-300) ** 2), 0.0)
    F[0] = np.pi
    return np.concatenate([F, np.ones_like(s), np.ones_like(s)])


# ------------------------------------------------------------------ continuation
def tangent(U, alpha, g, tau_prev, W):
    J = jac(U, alpha, g)
    J[:, -1] /= W
    M = np.vstack([J, tau_prev[None, :]])
    rhs = np.zeros(M.shape[0]); rhs[-1] = 1
    t = np.linalg.solve(M, rhs)
    return t / np.linalg.norm(t)


def corrector(Y, tau, Ypred, g, W, tol=1e-12, maxit=25):
    n = Y.size - 1
    for it in range(maxit):
        U, a = Y[:n], Y[n] / W
        R = residual(U, a, g)
        J = jac(U, a, g); J[:, -1] /= W
        M = np.vstack([J, tau[None, :]])
        rhs = -np.concatenate([R, [tau @ (Y - Ypred)]])
        dY = np.linalg.solve(M, rhs)
        Y = Y + dY
        if np.abs(dY).max() < tol:
            return Y, True
    return Y, False


def moore_spence(U, alpha, v, g, tol=1e-13, maxit=40, verbose=True):
    """Solve G(U,a)=0, G_U v=0, l.v=1 (l = initial v normalised)."""
    n = U.size
    l = v / (v @ v)
    h = 1e-30

    def Gv(Uc, a, vv):
        return residual(Uc + 1j * h * vv, a, g).imag / h

    for it in range(maxit):
        R1 = residual(U, alpha, g)
        R2 = Gv(U.astype(complex), alpha, v)
        R3 = l @ v - 1
        J = jac(U, alpha, g)             # [G_U | G_a]
        GU, Ga = J[:, :n], J[:, n]
        # derivative of G_U v wrt U and alpha by central differences of complex-step products
        d = 1e-6
        H = np.empty((n, n))
        for k in range(n):
            e = np.zeros(n); e[k] = d
            H[:, k] = (Gv((U + e).astype(complex), alpha, v) - Gv((U - e).astype(complex), alpha, v)) / (2 * d)
        da = 1e-7
        Ha = (Gv(U.astype(complex), alpha + da, v) - Gv(U.astype(complex), alpha - da, v)) / (2 * da)
        M = np.zeros((2 * n + 1, 2 * n + 1))
        M[:n, :n] = GU; M[:n, 2 * n] = Ga
        M[n:2 * n, :n] = H; M[n:2 * n, n:2 * n] = GU; M[n:2 * n, 2 * n] = Ha
        M[2 * n, n:2 * n] = l
        rhs = -np.concatenate([R1, R2, [R3]])
        dz = np.linalg.solve(M, rhs)
        U = U + dz[:n]; v = v + dz[n:2 * n]; alpha = alpha + dz[2 * n]
        if verbose:
            print('  MS it %d  |G|=%.2e |Gv|=%.2e  dalpha=%.2e alpha=%.15f' % (it, np.abs(R1).max(), np.abs(R2).max(), dz[2 * n], alpha), flush=True)
        if abs(dz[2 * n]) < tol and np.abs(dz[:n]).max() < 1e-10:
            break
    return U, v, alpha


if __name__ == '__main__':
    g = Grid(60, 1.5)
    U = flat_guess(g)
    U, ok = newton(U, 0.0, g, verbose=True)
    print('flat ok', ok, masses(U, 0.0, g), central(U, g))
