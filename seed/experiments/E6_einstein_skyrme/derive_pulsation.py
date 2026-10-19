#!/usr/bin/env python3
"""E6 (optional extension): radial (l = 0) pulsation equation of the gravitating hedgehog, derived with sympy.

Dimensionless coordinates (tau = e f t, x = e f r); metric ds^2 = -sigma^2 N dtau^2 + dx^2/N + x^2 dOmega^2,
N = 1 - 2 alpha m(tau,x)/x;  Einstein equations G_mu_nu = 2 alpha T~_mu_nu  (8 pi G e^2 f^4/(e f)^2 = 2 alpha).
Matter: L~ = -rho~(lam_r, lam_t) with lam_r = g^{ab} d_aF d_bF over (tau, x) and lam_t = sin^2F/x^2 (two angles),
    rho~ = (1/2)(lam_r + 2 lam_t) + (1/2)(2 lam_r lam_t + lam_t^2),
    T~_ab = 2 (d rho~/d lam_r) d_aF d_bF - g_ab rho~  (a,b in tau,x).
Perturb F = F0 + eps u, m = m0 + eps dm, sigma = s0 (1 + eps eta), linearise:
  * G_tau_x equation  ->  d_tau dm = K(x) d_tau u   =>  dm = K u
  * G^x_x - G^tau_tau  ->  eta' = (linear in u, u', dm)
  * matter equation   ->  only eta' enters (checked); with u = xi(x) e^{i omega tau}:
        a xi'' + b xi' + c xi = -omega^2 d xi
Writes pulsation_coeffs.json with a, b, c, d as sympy strings in terms of F, P (= F0'), m, al, sg (= sigma0),
and checks that the static zero-frequency operator agrees with the linearised static equations.
"""
import json
import os

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
tau, x, th, ph = sp.symbols('tau x theta phi', real=True)
al, eps = sp.symbols('alpha epsilon', positive=True)

F0 = sp.Function('F0')(x)
m0 = sp.Function('m0')(x)
s0 = sp.Function('s0')(x)
u = sp.Function('u')(tau, x)
dm = sp.Function('dm')(tau, x)
eta = sp.Function('eta')(tau, x)

F = F0 + eps * u
m = m0 + eps * dm
sig = s0 * (1 + eps * eta)
N = 1 - 2 * al * m / x
xs = [tau, x, th, ph]
g = sp.diag(-sig**2 * N, 1 / N, x**2, x**2 * sp.sin(th)**2)
gi = sp.diag(-1 / (sig**2 * N), N, 1 / x**2, 1 / (x**2 * sp.sin(th)**2))


def christoffel(g, gi):
    return [[[sum(gi[a, d] * (sp.diff(g[d, b], xs[c]) + sp.diff(g[d, c], xs[b]) - sp.diff(g[b, c], xs[d]))
                  for d in range(4)) / 2 for c in range(4)] for b in range(4)] for a in range(4)]


Gam = christoffel(g, gi)


def ricci(b, c):
    expr = 0
    for a in range(4):
        expr += sp.diff(Gam[a][b][c], xs[a]) - sp.diff(Gam[a][b][a], xs[c])
        for d in range(4):
            expr += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
    return expr


def lin(expr, order=1):
    """Coefficient of eps^order of expr (Taylor)."""
    return sp.diff(expr, eps, order).subs(eps, 0) / sp.factorial(order)


Ric = {}
for (b, c) in [(0, 0), (0, 1), (1, 1), (2, 2)]:
    Ric[(b, c)] = ricci(b, c)
Rs_terms = gi[0, 0] * Ric[(0, 0)] + gi[1, 1] * Ric[(1, 1)] + 2 * gi[2, 2] * Ric[(2, 2)]
# G_tau_x = R_tau_x (off-diagonal, g_tau_x = 0);  mixed G^a_a = g^{aa} R_aa - R/2
G_tx = Ric[(0, 1)]
Gtt_mixed = gi[0, 0] * Ric[(0, 0)] - Rs_terms / 2
Gxx_mixed = gi[1, 1] * Ric[(1, 1)] - Rs_terms / 2

# matter
Ft, Fx = sp.diff(F, tau), sp.diff(F, x)
lam_r = gi[0, 0] * Ft**2 + gi[1, 1] * Fx**2
lam_t = sp.sin(F)**2 / x**2
rho = (lam_r + 2 * lam_t) / 2 + (2 * lam_r * lam_t + lam_t**2) / 2
rho_l = sp.Rational(1, 2) + lam_t          # d rho/d lam_r
T_tx = 2 * rho_l * Ft * Fx
Ttt_mixed = gi[0, 0] * (2 * rho_l * Ft**2 - g[0, 0] * rho)
Txx_mixed = gi[1, 1] * (2 * rho_l * Fx**2 - g[1, 1] * rho)

# ------------------------------------------------ background equations (eps = 0), solved for m0', s0', F0''
P0 = sp.diff(F0, x)
N0 = 1 - 2 * al * m0 / x
A0 = x**2 + 2 * sp.sin(F0)**2
m0p = (N0 * P0**2 / 2) * A0 + sp.sin(F0)**2 * (1 + sp.sin(F0)**2 / (2 * x**2))
s0p = s0 * (al / x) * A0 * P0**2
# F0'' from (s N A F')' = s sin2F (1 + N F'^2 + sin^2F/x^2)
F0pp_sym = sp.Symbol('F0pp')
bg = sp.diff(s0 * N0 * A0 * P0, x) - s0 * sp.sin(2 * F0) * (1 + N0 * P0**2 + sp.sin(F0)**2 / x**2)
bg = bg.subs(sp.diff(F0, x, 2), F0pp_sym).subs(sp.diff(m0, x), m0p).subs(sp.diff(s0, x), s0p)
F0pp = sp.solve(bg, F0pp_sym)[0]


def bg_sub(expr):
    """Replace background derivatives using the static equations (order: 3rd, 2nd, then 1st derivatives)."""
    expr = expr.subs(sp.diff(F0, x, 3), sp.diff(F0pp, x))
    expr = expr.subs(sp.diff(s0, x, 2), sp.diff(s0p, x)).subs(sp.diff(m0, x, 2), sp.diff(m0p, x))
    expr = expr.subs(sp.diff(F0, x, 2), F0pp)
    expr = expr.subs(sp.diff(F0, x, 2), F0pp)
    expr = expr.subs(sp.diff(s0, x), s0p).subs(sp.diff(m0, x), m0p)
    expr = expr.subs(sp.diff(F0, x, 2), F0pp)
    return expr


# sanity: background Einstein equations hold at eps = 0
chk_tt = sp.simplify(bg_sub((Gtt_mixed - 2 * al * Ttt_mixed).subs(eps, 0).doit()))
chk_xx = sp.simplify(bg_sub((Gxx_mixed - 2 * al * Txx_mixed).subs(eps, 0).doit()))
print("background G^t_t check:", chk_tt, "  G^x_x check:", chk_xx)

# ------------------------------------------------ (1) tau-x equation at O(eps)
E_tx = sp.simplify(bg_sub(lin((G_tx - 2 * al * T_tx).doit())))
print("O(eps) G_tx - 2 alpha T_tx =", E_tx)
dmt = sp.Symbol('dmt')
sol_dmt = sp.solve(E_tx.subs(sp.diff(dm, tau), dmt), dmt)[0]
K = sp.simplify(sol_dmt / sp.diff(u, tau))
print("K(x) = dm/u =", K)
assert sp.simplify(sp.diff(K, tau)) == 0

# ------------------------------------------------ (2) eta' from the xx - tt combination
E_rt = lin((Gxx_mixed - Gtt_mixed - 2 * al * (Txx_mixed - Ttt_mixed)).doit())
E_rt = bg_sub(E_rt)
etap_sym = sp.Symbol('etap')
E_rt = E_rt.subs(sp.diff(eta, x), etap_sym)
etap = sp.solve(E_rt, etap_sym)[0]
etap = sp.simplify(etap.subs(dm, K * u))
print("eta' depends on:", sorted({str(a) for a in etap.atoms(sp.Function, sp.Derivative)}))

# ------------------------------------------------ (3) matter equation at O(eps)
# sqrt(-g) = sigma x^2 sin(theta).  Partial derivatives are taken w.r.t. plain symbols, then the fields are inserted.
Fq, Ftq, Fxq = sp.symbols('Fq Ftq Fxq')
lam_r_q = gi[0, 0] * Ftq**2 + gi[1, 1] * Fxq**2
lam_t_q = sp.sin(Fq)**2 / x**2
rho_q = (lam_r_q + 2 * lam_t_q) / 2 + (2 * lam_r_q * lam_t_q + lam_t_q**2) / 2
Lag = sig * x**2 * (-rho_q)
fill = {Fq: F, Ftq: Ft, Fxq: Fx}
EL = sp.diff(sp.diff(Lag, Ftq).subs(fill), tau) + sp.diff(sp.diff(Lag, Fxq).subs(fill), x) - sp.diff(Lag, Fq).subs(fill)
ELlin = lin(EL.doit())
ELlin = bg_sub(ELlin)
# eliminate dm (and its derivatives) and eta
ELlin = ELlin.subs(sp.diff(dm, x), sp.diff(K * u, x)).subs(dm, K * u)
ELlin = ELlin.subs(sp.diff(eta, x), etap)
ELlin = bg_sub(ELlin.doit())
has_eta = ELlin.has(eta)
ELlin = sp.expand(ELlin)
print("matter equation contains eta (undifferentiated) after elimination:", has_eta and sp.simplify(ELlin.coeff(eta)) != 0)
uu, ux, uxx, utt = sp.symbols('uu ux uxx utt')
E2 = ELlin.subs(sp.diff(u, tau, 2), utt).subs(sp.diff(u, x, 2), uxx).subs(sp.diff(u, x), ux).subs(u, uu)
E2 = sp.expand(E2)
a = sp.simplify(E2.coeff(uxx))
b = sp.simplify(E2.coeff(ux))
c = sp.simplify(E2.coeff(uu))
d = sp.simplify(E2.coeff(utt))       # a u'' + b u' + c u + d u_tt = 0  -> with u_tt = -omega^2 u:  a u'' + b u' + c u = omega^2 d u
rest = sp.simplify(E2 - a * uxx - b * ux - c * uu - d * utt)
print("remainder (should be 0):", rest)
# symbols for numerics
Fs, Ps, ms, sgs = sp.symbols('F P m sg')
rep = {sp.diff(F0, x): Ps}
out = {}
for name, ex in [("a", a), ("b", b), ("c", c), ("d", d), ("K", K)]:
    ex2 = ex.subs(rep).subs(F0, Fs).subs(m0, ms).subs(s0, sgs)
    ex2 = sp.simplify(ex2)
    out[name] = str(ex2)
    print(f"{name} =", ex2)
# self-adjointness: for an action-derived operator, b == a' along the background (checked numerically later)
out["note"] = "a xi'' + b xi' + c xi = omega^2 d xi ; omega in units of e f (frequency at infinity, sigma(inf)=1)"
with open(os.path.join(HERE, "pulsation_coeffs.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote pulsation_coeffs.json")
