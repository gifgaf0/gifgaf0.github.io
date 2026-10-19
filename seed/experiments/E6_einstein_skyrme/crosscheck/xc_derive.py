#!/usr/bin/env python3
"""
Independent cross-check of E6 (Einstein-Skyrme hedgehog): symbolic derivation.

Written from scratch for the cross-check (the original scripts were not read).
Conventions (PLAN.md E6): L = (f^2/4) Tr(dU dU^+) + 1/(32 e^2) Tr[L_mu,L_nu]^2,
f = F_pi/2, x = e f r, alpha = 4 pi G f^2.  Units: lengths 1/(e f), energy
density e^2 f^4.  In these units the Einstein equations read
        G^mu_nu = 2 alpha T^mu_nu .

Hedgehog strain eigenvalues: lam_r^2 = g^{rr} F'^2 (time-dependent: X = g^{ab} dF_a dF_b),
lam_t^2 = sin^2F / R^2 (R = areal radius), twice.
   rho = 1/2 (X + 2 lt) + 1/2 (2 X lt + lt^2)         (lt = lam_t^2)
   p_r = 2 X d rho/dX - rho ,  p_t = 2 lt (d rho/d lt)/2 - rho  (per angular direction)
Static Lagrangian density = -rho.

Gauges used here (different from the original's Schwarzschild-type shooting):
 (I) isotropic:  ds^2 = -A^2 dt^2 + psi^4 (dx^2 + x^2 dOmega^2)
 (S) Schwarzschild-like, only for the stability / node-count check:
     ds^2 = -s^2 N dt^2 + dx^2/N + x^2 dOmega^2, N = 1 - 2 alpha m/x

Checks printed:
  I1  G^t_t = 4 psi^-5 Lap(psi)            -> Lichnerowicz eq. Lap psi = -(alpha/2) rho psi^5
  I2  R^t_t = -psi^-6 (x^2 psi^2 A')'/(x^2 A) -> (x^2 psi^2 A')' = alpha x^2 psi^6 A (rho+p_r+2p_t)
  I3  div T (r-component) = -F' * EL[F] / (A psi^6 x^2)  (Noether identity: stresses consistent
      with rho and with the field equation from the reduced action)
  S1  m' = x^2 rho,  (ln s)' = alpha x (rho+p_r)/N
  S2  momentum constraint G_tx = 2 alpha T_tx  ->  delta m (for the pulsation equation)
Outputs: xc_equations.json with sympy srepr strings of the residuals.
"""
import json, time
import sympy as sp

t0 = time.time()
t, x, th, ph = sp.symbols('t x theta phi', real=True)
al = sp.symbols('alpha', positive=True)
coords = [t, x, th, ph]


def einstein_mixed(g):
    """Return (G^mu_nu, R^mu_nu) for metric matrix g (functions of coords)."""
    gi = sp.simplify(g.inv())
    n = 4
    Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                Gam[a][b][c] = sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b])
                                                         - sp.diff(g[b, c], coords[d])) for d in range(n)) / 2)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            expr = 0
            for a in range(n):
                expr += sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
                for d in range(n):
                    expr += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
            Ric[b, c] = sp.simplify(expr)
    Rmix = sp.simplify(gi * Ric)
    Rs = sp.simplify(sum(Rmix[i, i] for i in range(n)))
    Gmix = sp.simplify(Rmix - Rs / 2 * sp.eye(n))
    return Gmix, Rmix, Ric, gi


def rho_p(X, lt):
    rho = sp.Rational(1, 2) * (X + 2 * lt) + sp.Rational(1, 2) * (2 * X * lt + lt ** 2)
    pr = 2 * X * sp.diff(rho, X) - rho
    pt = lt * sp.diff(rho, lt) - rho      # d rho/d(lam_theta^2) for ONE angular direction = diff(rho,lt)/2
    return sp.expand(rho), sp.expand(pr), sp.expand(pt)


out = {}
ok_all = True

# ---------------- (I) isotropic gauge -----------------
A = sp.Function('A')(x)
psi = sp.Function('psi')(x)
F = sp.Function('F')(x)
g = sp.diag(-A ** 2, psi ** 4, psi ** 4 * x ** 2, psi ** 4 * x ** 2 * sp.sin(th) ** 2)
Gm, Rm, Ric, gi = einstein_mixed(g)
lap = sp.diff(x ** 2 * sp.diff(psi, x), x) / x ** 2
chk1 = sp.simplify(Gm[0, 0] - 4 * lap / psi ** 5)
chk2 = sp.simplify(Rm[0, 0] + sp.diff(x ** 2 * psi ** 2 * sp.diff(A, x), x) / (x ** 2 * psi ** 6 * A))
print('I1  G^t_t - 4 psi^-5 Lap psi        =', chk1)
print('I2  R^t_t + (x^2psi^2A\')\'/(x^2psi^6A) =', chk2)
ok_all &= (chk1 == 0) and (chk2 == 0)

Fp = sp.diff(F, x)
X_iso = Fp ** 2 / psi ** 4
lt_iso = sp.sin(F) ** 2 / (x ** 2 * psi ** 4)
Xs, lts = sp.symbols('X lt', positive=True)
rho_s, pr_s, pt_s = rho_p(Xs, lts)
print('rho  =', rho_s, '\np_r  =', pr_s, '\np_t  =', pt_s)
rho_i = rho_s.subs({Xs: X_iso, lts: lt_iso})
pr_i = pr_s.subs({Xs: X_iso, lts: lt_iso})
pt_i = pt_s.subs({Xs: X_iso, lts: lt_iso})

# matter equation from the reduced action  S = -int A psi^6 x^2 rho dx
Lred = A * psi ** 6 * x ** 2 * rho_i
EL = sp.diff(sp.diff(Lred, Fp), x) - sp.diff(Lred, F)      # = 0
EL = sp.simplify(EL)
# Noether identity: covariant divergence of T^mu_x
R_areal = x * psi ** 2
divT = sp.diff(pr_i, x) + sp.diff(A, x) / A * (rho_i + pr_i) + 2 * sp.diff(R_areal, x) / R_areal * (pr_i - pt_i)
chk3 = sp.simplify(divT - Fp * EL / (A * psi ** 6 * x ** 2))
print('I3  divT - F\' EL/(A psi^6 x^2)     =', chk3)
ok_all &= (chk3 == 0)

# G^x_x expression (diagnostic residual)
Gxx_iso = sp.simplify(Gm[1, 1])
Gthth_iso = sp.simplify(Gm[2, 2])

out['iso'] = {
    'rho': sp.srepr(rho_i), 'pr': sp.srepr(pr_i), 'pt': sp.srepr(pt_i),
    'EL': sp.srepr(EL), 'Gxx': sp.srepr(Gxx_iso), 'Gthth': sp.srepr(Gthth_iso),
}

# ---------------- (S) Schwarzschild-like gauge, time dependent -----------------
m = sp.Function('m')(t, x)
s = sp.Function('s')(t, x)
Ft = sp.Function('F')(t, x)
N = 1 - 2 * al * m / x
gS = sp.diag(-s ** 2 * N, 1 / N, x ** 2, x ** 2 * sp.sin(th) ** 2)
GmS, RmS, RicS, giS = einstein_mixed(gS)
GS_tx = sp.simplify(RicS[0, 1])   # G_tx = R_tx since g_tx = 0
# stress tensor, time-dependent hedgehog:  X = g^{ab} dF_a dF_b
X_S = giS[0, 0] * sp.diff(Ft, t) ** 2 + giS[1, 1] * sp.diff(Ft, x) ** 2
lt_S = sp.sin(Ft) ** 2 / x ** 2
rho_fun = rho_s  # as a function of X, lt; Lagrangian = -rho(X, lt)
dLdX = -sp.diff(rho_fun, Xs)
# T_ab = -2 dL/dg^{ab} + g_ab L ;  dX/dg^{ab} = dF_a dF_b
T_tx = sp.simplify((-2 * dLdX * sp.diff(Ft, t) * sp.diff(Ft, x)).subs({Xs: X_S, lts: lt_S}))
mom = sp.simplify(GS_tx - 2 * al * T_tx)
print('S2  G_tx - 2 alpha T_tx =', sp.factor(mom))
# static parts
rho_S = rho_s.subs({Xs: X_S, lts: lt_S})
pr_S = pr_s.subs({Xs: X_S, lts: lt_S})
# static check of m' and (ln s)'
stat = {sp.Derivative(m, t): 0, sp.Derivative(s, t): 0, sp.Derivative(Ft, t): 0}
Gtt_stat = sp.simplify(GmS[0, 0].subs(stat))
chkS1 = sp.simplify(Gtt_stat + 2 * al * sp.diff(m, x) / x ** 2)
print('S1a G^t_t + 2 alpha m\'/x^2          =', chkS1)
Gdiff = sp.simplify((GmS[1, 1] - GmS[0, 0]).subs(stat))
chkS1b = sp.simplify(Gdiff - 2 * al * x * 0 - (2 * N * sp.diff(s, x) / (s * x)))
print('S1b G^x_x - G^t_t - 2 N s\'/(s x)    =', chkS1b)
ok_all &= (chkS1 == 0) and (chkS1b == 0)
# so  (ln s)' = alpha x (rho + p_r)/N
# time-dependent matter Lagrangian (reduced):  sqrt(-g) L = s x^2 (-rho(X,lt))
LS = -(s * x ** 2 * rho_fun).subs({Xs: X_S, lts: lt_S})
out['S'] = {
    'Lred': sp.srepr(LS), 'T_tx': sp.srepr(T_tx), 'G_tx': sp.srepr(GS_tx),
    'GxxmGtt': sp.srepr(sp.simplify(GmS[1, 1] - GmS[0, 0])),
    'Gtt': sp.srepr(sp.simplify(GmS[0, 0])),
    'rho': sp.srepr(rho_S), 'pr': sp.srepr(pr_S),
}
out['all_symbolic_checks_pass'] = bool(ok_all)
json.dump(out, open('/home/user/gifgaf0.github.io/seed/experiments/E6_einstein_skyrme/crosscheck/xc_equations.json', 'w'))
print('ALL SYMBOLIC CHECKS PASS' if ok_all else 'SOME CHECK FAILED', ' (%.1f s)' % (time.time() - t0))
