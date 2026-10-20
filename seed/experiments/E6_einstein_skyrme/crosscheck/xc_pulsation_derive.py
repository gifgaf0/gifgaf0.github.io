#!/usr/bin/env python3
"""
Cross-check: radial pulsation operator of the Einstein-Skyrme hedgehog, derived from scratch.
Gauge: ds^2 = -s(t,x)^2 N dt^2 + dx^2/N + x^2 dOmega^2, N = 1 - 2 alpha m(t,x)/x.
Perturbation: F = F0 + eps xi(x) cos(w t), m = m0 + eps dm(x) cos(w t), s = s0 (1 + eps eta(x) cos(w t)).
  dm  from the momentum constraint G_tx = 2 alpha T_tx (exact: m_t = N (x^2+2 sin^2F) F' F_t)
  eta' from G^x_x - G^t_t = 2 alpha (rho + p_r)   (checked here to hold with time dependence)
Result: a xi'' + b xi' + c xi + w^2 d xi = 0 with coefficients in (x, F0, F0', m0, s0) after
eliminating F0'' (background EL), m0' (= x^2 rho), s0'/s0.  Saved to xc_pulsation.json.
"""
import json, time
import sympy as sp

t0 = time.time()
t, x, th = sp.symbols('t x theta', real=True)
al, eps, w = sp.symbols('alpha epsilon omega', positive=True)
coords = [t, x, th, sp.Symbol('phi')]

m = sp.Function('m')(t, x); s = sp.Function('s')(t, x); F = sp.Function('F')(t, x)
N = 1 - 2 * al * m / x
g = sp.diag(-s ** 2 * N, 1 / N, x ** 2, x ** 2 * sp.sin(th) ** 2)
gi = g.inv()
n = 4
Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b]) - sp.diff(g[b, c], coords[d]))
                         for d in range(n)) / 2) for c in range(n)] for b in range(n)] for a in range(n)]
Ric = sp.zeros(n, n)
for b in range(n):
    for c in range(n):
        e = 0
        for a in range(n):
            e += sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
            for d in range(n):
                e += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
        Ric[b, c] = sp.simplify(e)
Rmix = sp.simplify(gi * Ric)
Rs = sp.simplify(sum(Rmix[i, i] for i in range(n)))
G = sp.simplify(Rmix - Rs / 2 * sp.eye(n))
chk = sp.simplify(G[1, 1] - G[0, 0] - 2 * N * sp.diff(s, x) / (s * x))
print('G^x_x - G^t_t - 2N s_x/(s x) (time dependent) =', chk)

# matter
X = gi[0, 0] * sp.diff(F, t) ** 2 + gi[1, 1] * sp.diff(F, x) ** 2
lt = sp.sin(F) ** 2 / x ** 2
rho = X * lt + X / 2 + lt ** 2 / 2 + lt
pr_static = X * lt + X / 2 - lt ** 2 / 2 - lt   # valid when F_t = 0 (only needed to first order)
# T^x_x - T^t_t for time-dependent: T_ab = 2 drho/dX dF_a dF_b - g_ab rho (L=-rho)
dX = sp.diff(rho, sp.Symbol('dummy')) if False else None
Xs, lts = sp.symbols('Xs lts')
rho_fun = Xs * lts + Xs / 2 + lts ** 2 / 2 + lts
drdX = sp.diff(rho_fun, Xs).subs({Xs: X, lts: lt})
T_lo = sp.zeros(2, 2)
dF = [sp.diff(F, t), sp.diff(F, x)]
for a in range(2):
    for b in range(2):
        T_lo[a, b] = 2 * drdX * dF[a] * dF[b] - g[a, b] * rho
Tmix_tt = gi[0, 0] * T_lo[0, 0]
Tmix_xx = gi[1, 1] * T_lo[1, 1]
# Einstein: G^x_x - G^t_t = 2 alpha (T^x_x - T^t_t)  ->  s_x/s = alpha x (T^x_x - T^t_t)/N
eta_rhs = al * x * (Tmix_xx - Tmix_tt) / N     # = d/dx ln s

# reduced matter Lagrangian sqrt(-g) L / (4 pi sin) = s x^2 (-rho)
Lr = -s * x ** 2 * rho
Ft_, Fx_ = sp.symbols('Ft_ Fx_')
Lsub = Lr.subs({sp.Derivative(F, t): Ft_, sp.Derivative(F, x): Fx_})
EL = (sp.diff(sp.diff(Lsub, Ft_).subs({Ft_: sp.Derivative(F, t), Fx_: sp.Derivative(F, x)}), t)
      + sp.diff(sp.diff(Lsub, Fx_).subs({Ft_: sp.Derivative(F, t), Fx_: sp.Derivative(F, x)}), x)
      - sp.diff(Lsub, F).subs({Ft_: sp.Derivative(F, t), Fx_: sp.Derivative(F, x)}))

# perturbation
F0 = sp.Function('F0')(x); m0 = sp.Function('m0')(x); s0 = sp.Function('s0')(x)
xi = sp.Function('xi')(x); eta = sp.Function('eta')(x)
c = sp.cos(w * t)
Fp = F0 + eps * xi * c
dm = (1 - 2 * al * m0 / x) * (x ** 2 + 2 * sp.sin(F0) ** 2) * sp.diff(F0, x) * xi   # from G_tx (see xc_derive S2)
mp = m0 + eps * dm * c
sp_ = s0 * (1 + eps * eta * c)
rep = {F: Fp, m: mp, s: sp_}
ELp = EL.subs(rep).doit()
lin = sp.diff(ELp, eps).subs(eps, 0)
lin = sp.simplify(lin / c) if False else lin
# eta' from the linearised (ln s)' equation
etap_expr = sp.diff(sp.log(sp_), x)
rhs_p = eta_rhs.subs(rep).doit()
eta1 = sp.diff(rhs_p, eps).subs(eps, 0) / c        # = eta'
eta1 = sp.simplify(eta1)
# background relations
F0pp = sp.Symbol('F0pp')
EL0 = EL.subs({F: F0, m: m0, s: s0}).doit()
EL0 = EL0.subs(sp.Derivative(F0, (x, 2)), F0pp)
F0pp_sol = sp.solve(sp.Eq(EL0, 0), F0pp)[0]
rho0 = rho.subs({F: F0, m: m0, s: s0}).doit()
lnS0p = eta_rhs.subs({F: F0, m: m0, s: s0}).doit()
lin = sp.expand(lin)
lin = lin.subs(sp.Derivative(eta, x), eta1 * 1)
# remove the cos(w t) factor: all terms are linear in cos or have sin^2... evaluate at t=0 after w^2 from d2/dt2
lin = lin.subs(t, 0)
lin = lin.subs(sp.Derivative(F0, (x, 3)), sp.diff(F0pp_sol, x))
lin = lin.subs(sp.Derivative(F0, (x, 2)), F0pp_sol)
lin = lin.subs(sp.Derivative(m0, (x, 2)), sp.diff(x ** 2 * rho0, x))
lin = lin.subs(sp.Derivative(m0, x), x ** 2 * rho0)
lin = lin.subs(sp.Derivative(s0, x), s0 * lnS0p)
lin = lin.subs(sp.Derivative(F0, (x, 2)), F0pp_sol)
lin = lin.subs(sp.Derivative(m0, x), x ** 2 * rho0)
print('eta remaining?', lin.has(eta))
xi2, xi1, xi0 = sp.symbols('xi2 xi1 xi0')
lin = lin.subs(sp.Derivative(xi, (x, 2)), xi2).subs(sp.Derivative(xi, x), xi1).subs(xi, xi0)
Fv, F1, mv, sv = sp.symbols('Fv F1 mv sv')
lin = lin.subs(sp.Derivative(F0, x), F1).subs(F0, Fv).subs(m0, mv).subs(s0, sv)
lin = sp.expand(lin)
a_ = sp.simplify(lin.coeff(xi2))
b_ = sp.simplify(lin.coeff(xi1))
rest = sp.expand(lin - a_ * xi2 - b_ * xi1)
c_ = sp.simplify(rest.coeff(xi0).subs(w, 0))
d_ = sp.simplify((rest.coeff(xi0) - rest.coeff(xi0).subs(w, 0)) / w ** 2)
print('a =', sp.factor(a_))
print('d =', sp.factor(d_))
# Sturm-Liouville check: p = exp(int b/a); expect p = s N (x^2 + 2 sin^2 F)
Nv = 1 - 2 * al * mv / x
p_guess = sv * Nv * (x ** 2 + 2 * sp.sin(Fv) ** 2)
# d/dx p_guess along the background:
dp = (sp.diff(p_guess, x) + sp.diff(p_guess, Fv) * F1 + sp.diff(p_guess, mv) * (x ** 2 * rho0.subs(sp.Derivative(F0, x), F1).subs(F0, Fv).subs(m0, mv))
      + sp.diff(p_guess, sv) * sv * lnS0p.subs(sp.Derivative(F0, x), F1).subs(F0, Fv).subs(m0, mv))
slchk = sp.simplify(b_ / a_ - dp / p_guess)
print('SL check b/a - p\'/p =', slchk)
out = dict(a=sp.srepr(a_), b=sp.srepr(b_), c=sp.srepr(c_), d=sp.srepr(d_), p=sp.srepr(p_guess), sl_check=str(slchk),
           time_dependent_GxxGtt_check=str(chk))
json.dump(out, open('/home/user/gifgaf0.github.io/seed/experiments/E6_einstein_skyrme/crosscheck/xc_pulsation.json', 'w'))
print('done %.1fs' % (time.time() - t0))
