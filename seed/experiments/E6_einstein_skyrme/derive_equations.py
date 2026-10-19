#!/usr/bin/env python3
"""E6 step 1: derive the hedgehog Einstein-Skyrme equations with sympy and check them.

Model (static energy density; the static Lagrangian density is L = -rho in either signature):
    L = (f^2/4) Tr(d_mu U d^mu U^dag) + 1/(32 e^2) Tr([U^dag d_mu U, U^dag d_nu U]^2)   (mostly-minus form)
    rho = -(f^2/4) g^{ij} Tr(L_i L_j) - 1/(32 e^2) g^{ik} g^{jl} Tr([L_i,L_j][L_k,L_l]),  L_i = U^dag d_i U
    metric ds^2 = -sigma(r)^2 N(r) dt^2 + dr^2/N(r) + r^2 dOmega^2,   N = 1 - 2 mu(r)/r,  mu = G m(r)
    hedgehog U = cos F(r) + i sin F(r) n.tau

Checks printed:
  (A) the reduced rho(F, F', N, r) equals the matrix expression in the curved spatial metric
      (numerically, Cartesian coordinates, arbitrary test profiles), to ~1e-15;
  (B) Einstein tensor of the metric; G^t_t = 8 pi G T^t_t  ->  mu' = 4 pi G r^2 rho;
      G^r_r - G^t_t = 8 pi G (T^r_r - T^t_t)  ->  sigma'/sigma = 4 pi G r (rho + p_r)/N;
  (C) the matter equation from the reduced action S = -4 pi int dt int sigma r^2 rho dr;
  (D) the remaining Einstein equation G^th_th = 8 pi G T^th_th holds identically once (B),(C) are used;
  (E) dimensionless form with x = e f r, alpha = 4 pi G f^2, N = 1 - 2 alpha m(x)/x, M = 4 pi (f/e) m;
  (F) series at the regular centre, F = pi - b x + c3 x^3 + c5 x^5, m = m3 x^3 + m5 x^5.
Writes derived_equations.json (series coefficients as strings, used by e6_solve.py as a check).
"""
import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ok_all = True


def report(name, ok, detail=""):
    global ok_all
    ok_all &= bool(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")


# ---------------------------------------------------------------- (A) reduced energy density
f, e = sp.symbols('f e', positive=True)
X, Y, Z = sp.symbols('X Y Z', real=True)
R = sp.sqrt(X**2 + Y**2 + Z**2)
# arbitrary smooth test profiles (only used for this numerical identity check)
Ftest = sp.pi * sp.exp(-R**2 / 3) * (1 + R / 5)
Ntest = 1 - sp.Rational(3, 10) * R**2 * sp.exp(-R)
I2 = sp.eye(2)
tau = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
nvec = [X / R, Y / R, Z / R]
U = sp.cos(Ftest) * I2 + sp.I * sp.sin(Ftest) * (nvec[0] * tau[0] + nvec[1] * tau[1] + nvec[2] * tau[2])
Ud = U.H
coords = [X, Y, Z]
pt = {X: sp.Rational(7, 10), Y: -sp.Rational(4, 10), Z: sp.Rational(11, 10)}
fv, ev = sp.Rational(13, 10), sp.Rational(17, 10)
Lmat = []
for c in coords:
    Lmat.append((Ud * sp.diff(U, c)).subs(pt).evalf(30))
Nv = Ntest.subs(pt).evalf(30)
nv = [sp.N(q.subs(pt), 30) for q in nvec]
ginv = [[(1 if i == j else 0) + (Nv - 1) * nv[i] * nv[j] for j in range(3)] for i in range(3)]


def tr(M):
    return sp.N(M.trace(), 30)


rho2 = 0
rho4 = 0
for i in range(3):
    for j in range(3):
        rho2 += -(fv**2 / 4) * ginv[i][j] * tr(Lmat[i] * Lmat[j])
comm = [[Lmat[i] * Lmat[j] - Lmat[j] * Lmat[i] for j in range(3)] for i in range(3)]
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                gg = ginv[i][k] * ginv[j][l]
                if gg != 0:
                    rho4 += -(1 / (32 * ev**2)) * gg * tr(comm[i][j] * comm[k][l])
rho_matrix = sp.re(sp.N(rho2 + rho4, 30))

r = sp.symbols('r', positive=True)
Fr = sp.pi * sp.exp(-r**2 / 3) * (1 + r / 5)
Nr = 1 - sp.Rational(3, 10) * r**2 * sp.exp(-r)
Fp = sp.diff(Fr, r)
s2 = sp.sin(Fr)**2


def rho_reduced(N, Fp, s2, r, f, e):
    return (f**2 / 2) * (N * Fp**2 + 2 * s2 / r**2) + (1 / (2 * e**2)) * (s2 / r**2) * (2 * N * Fp**2 + s2 / r**2)


rv = R.subs(pt)
rho_red = sp.N(rho_reduced(Nr, Fp, s2, r, fv, ev).subs(r, rv), 30)
relA = abs((rho_matrix - rho_red) / rho_red)
report("(A) reduced rho == matrix rho in curved spatial metric", relA < 1e-20, f"rel.diff = {float(relA):.2e}")

# ---------------------------------------------------------------- (B) Einstein tensor
t, th, ph = sp.symbols('t theta phi', real=True)
G = sp.symbols('G', positive=True)
sig = sp.Function('sigma')(r)
mu = sp.Function('mu')(r)
N = 1 - 2 * mu / r
xs = [t, r, th, ph]
g = sp.diag(-sig**2 * N, 1 / N, r**2, r**2 * sp.sin(th)**2)
gi = g.inv()
dim = 4
Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], xs[c]) + sp.diff(g[d, c], xs[b]) - sp.diff(g[b, c], xs[d]))
                         for d in range(dim)) / 2) for c in range(dim)] for b in range(dim)] for a in range(dim)]


def ricci(b, c):
    expr = 0
    for a in range(dim):
        expr += sp.diff(Gam[a][b][c], xs[a]) - sp.diff(Gam[a][b][a], xs[c])
        for d in range(dim):
            expr += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
    return sp.simplify(expr)


Ric = sp.Matrix(dim, dim, lambda b, c: ricci(b, c))
Rs = sp.simplify(sum(gi[a, b] * Ric[a, b] for a in range(dim) for b in range(dim)))
Gmix = sp.simplify(gi * Ric - sp.eye(4) * Rs / 2)   # G^a_b
Gtt, Grr, Gthth = sp.simplify(Gmix[0, 0]), sp.simplify(Gmix[1, 1]), sp.simplify(Gmix[2, 2])
print("G^t_t   =", Gtt)
print("G^r_r   =", Grr)
print("G^th_th =", sp.simplify(Gthth))

# ---------------------------------------------------------------- matter stress tensor from metric variation
# rho depends on the metric only through lam_r = g^{rr} F'^2, lam_th = g^{thth} sin^2F, lam_ph = g^{phph} sin^2F sin^2 th
lr, lt, lp = sp.symbols('lambda_r lambda_t lambda_p', nonnegative=True)
rho_l = (f**2 / 2) * (lr + lt + lp) + (1 / (2 * e**2)) * (lr * lt + lr * lp + lt * lp)
F = sp.Function('F')(r)
Fd = sp.diff(F, r)
sub_l = {lr: N * Fd**2, lt: sp.sin(F)**2 / r**2, lp: sp.sin(F)**2 / r**2}
rho = rho_l.subs(sub_l)
# T^mu_nu = -2 g^{mu a} dL/dg^{a nu} + delta L, L = -rho:  T^t_t = -rho; T^r_r = 2 lam_r drho/dlam_r - rho; ...
Ttt = -rho
Trr = (2 * lr * sp.diff(rho_l, lr) - rho_l).subs(sub_l)
Tthth = (2 * lt * sp.diff(rho_l, lt) - rho_l).subs(sub_l)
rho_plus_pr = sp.simplify(Trr - Ttt)
target = N * Fd**2 * (f**2 + 2 * sp.sin(F)**2 / (e**2 * r**2))
report("rho + p_r = N F'^2 (f^2 + 2 sin^2F/(e^2 r^2))", sp.simplify(rho_plus_pr - target) == 0)

# Einstein equations solved for mu' and sigma'
eq_tt = sp.Eq(Gtt, 8 * sp.pi * G * Ttt)
mup = sp.solve(eq_tt, sp.diff(mu, r))[0]
report("G^t_t eq  ->  mu' = 4 pi G r^2 rho", sp.simplify(mup - 4 * sp.pi * G * r**2 * rho) == 0)
eq_rt = sp.Eq(Grr - Gtt, 8 * sp.pi * G * (Trr - Ttt))
sigp = sp.solve(eq_rt, sp.diff(sig, r))[0]
report("G^r_r - G^t_t eq  ->  sigma'/sigma = 4 pi G r (rho+p_r)/N",
       sp.simplify(sigp / sig - 4 * sp.pi * G * r * rho_plus_pr / N) == 0)

# ---------------------------------------------------------------- (C) matter equation from reduced action
Lred = sig * r**2 * rho          # static action S = -4 pi int dt int Lred dr ; extremise int Lred dr over F
EL = sp.diff(sp.diff(Lred, Fd), r) - sp.diff(Lred, F)
# claimed form: (sigma N (f^2 r^2 + 2 sin^2F/e^2) F')' = sigma sin 2F (f^2 + N F'^2/e^2 + sin^2F/(e^2 r^2))
claimed = sp.diff(sig * N * (f**2 * r**2 + 2 * sp.sin(F)**2 / e**2) * Fd, r) \
    - sig * sp.sin(2 * F) * (f**2 + N * Fd**2 / e**2 + sp.sin(F)**2 / (e**2 * r**2))
report("(C) Euler-Lagrange equation for F", sp.simplify(sp.expand(EL - claimed)) == 0)

# ---------------------------------------------------------------- (D) theta-theta equation is implied
Fdd = sp.solve(sp.Eq(EL, 0), sp.diff(F, r, 2))[0]
resid = Gthth - 8 * sp.pi * G * Tthth
# order matters: second derivatives of the metric first (they bring in F'', sigma', mu'), then F'', then sigma', mu'
resid = resid.subs(sp.diff(sig, r, 2), sp.diff(sigp, r)).subs(sp.diff(mu, r, 2), sp.diff(mup, r))
resid = resid.subs(sp.diff(F, r, 2), Fdd)
resid = resid.subs(sp.diff(sig, r), sigp).subs(sp.diff(mu, r), mup)
resid = sp.simplify(resid)
report("(D) G^th_th = 8 pi G T^th_th follows from the other equations", resid == 0, f"residual = {resid}")

# ---------------------------------------------------------------- (E) dimensionless form
x, al = sp.symbols('x alpha', positive=True)
Fx = sp.Function('F')(x)
mx = sp.Function('m')(x)
sx = sp.Function('sigma')(x)
Nx = 1 - 2 * al * mx / x
# r = x/(e f); mu(r) = G M(r) with M = 4 pi (f/e) m(x) -> mu = alpha m /(e f)
Fs, Fxs, ms = sp.symbols('F_s Fx_s m_s')
N_of_x = 1 - 2 * al * ms / x
rho_phys = rho_reduced(N_of_x, e * f * Fxs, sp.sin(Fs)**2, x / (e * f), f, e)
rho_tilde_s = (N_of_x * Fxs**2 / 2) * (x**2 + 2 * sp.sin(Fs)**2) / x**2 + sp.sin(Fs)**2 * (1 + sp.sin(Fs)**2 / (2 * x**2)) / x**2
chk = sp.simplify(rho_phys / (e**2 * f**4) - rho_tilde_s)
rho_tilde = rho_tilde_s.subs({Fxs: sp.diff(Fx, x), Fs: Fx, ms: mx})
report("(E) rho = e^2 f^4 rho~(x),  x^2 rho~ = (N F'^2/2)(x^2+2 sin^2F) + sin^2F (1 + sin^2F/(2x^2))", chk == 0)
# m'(x) = x^2 rho~ with N = 1 - 2 alpha m/x and alpha = 4 pi G f^2:
#   d mu/dx = (1/(e f)) 4 pi G r^2 rho = 4 pi G f^2 x^2 rho~ /(e f) = alpha x^2 rho~/(e f)  [mu = alpha m/(e f)]
lhs = sp.diff(al * mx / (e * f), x)
rhs = (1 / (e * f)) * 4 * sp.pi * G * (x / (e * f))**2 * (e**2 * f**4) * rho_tilde
chkm = sp.simplify((lhs - rhs).subs(sp.diff(mx, x), x**2 * rho_tilde).subs(G, al / (4 * sp.pi * f**2)))
report("(E) m'(x) = x^2 rho~ with alpha = 4 pi G f^2", chkm == 0)
# sigma'(x)/sigma = (alpha/x)(x^2 + 2 sin^2F) F'^2
sp_r = 4 * sp.pi * G * r * rho_plus_pr / N
sp_x = sp.simplify((sp_r / (e * f)).subs({mu: al * mx / (e * f)}).subs(Fd, e * f * sp.diff(Fx, x)).subs(F, Fx)
                   .subs(r, x / (e * f)).subs(G, al / (4 * sp.pi * f**2)))
report("(E) sigma'/sigma = (alpha/x)(x^2 + 2 sin^2F) F'^2",
       sp.simplify(sp_x - (al / x) * (x**2 + 2 * sp.sin(Fx)**2) * sp.diff(Fx, x)**2) == 0)
# matter equation in x
ELx = sp.diff(sx * Nx * (x**2 + 2 * sp.sin(Fx)**2) * sp.diff(Fx, x), x) \
    - sx * sp.sin(2 * Fx) * (1 + Nx * sp.diff(Fx, x)**2 + sp.sin(Fx)**2 / x**2)
print("dimensionless matter equation: (sigma N (x^2 + 2 sin^2F) F')' = sigma sin2F (1 + N F'^2 + sin^2F/x^2)")

# ---------------------------------------------------------------- (F) series at the centre
b, c3, c5, m3, m5 = sp.symbols('b c3 c5 m3 m5')
Fser = sp.pi - b * x + c3 * x**3 + c5 * x**5
mser = m3 * x**3 + m5 * x**5
# use sigma'/sigma to eliminate sigma: divide ELx by sigma
Fpp = sp.diff(Fser, x)
Nser = 1 - 2 * al * mser / x
sratio = (al / x) * (x**2 + 2 * sp.sin(Fser)**2) * Fpp**2
A = x**2 + 2 * sp.sin(Fser)**2
eqF = sratio * Nser * A * Fpp + sp.diff(Nser * A * Fpp, x) - sp.sin(2 * Fser) * (1 + Nser * Fpp**2 + sp.sin(Fser)**2 / x**2)
eqm = sp.diff(mser, x) - ((Nser * Fpp**2 / 2) * (x**2 + 2 * sp.sin(Fser)**2) + sp.sin(Fser)**2 * (1 + sp.sin(Fser)**2 / (2 * x**2)))
serF = sp.series(eqF, x, 0, 6).removeO()
serm = sp.series(eqm, x, 0, 6).removeO()
sol = sp.solve([serm.coeff(x, 2), serm.coeff(x, 4), serF.coeff(x, 3), serF.coeff(x, 5)], [m3, m5, c3, c5], dict=True)
sol = sol[0]
for k in [m3, c3, m5, c5]:
    sol[k] = sp.factor(sp.simplify(sol[k]))
    print(f"  {k} = {sol[k]}")
lower_ok = all(sp.simplify(serF.coeff(x, n)) == 0 for n in [0, 1, 2]) and sp.simplify(serm.coeff(x, 0)) == 0
lower_ok &= sp.simplify(serF.coeff(x, 1).subs(sol)) == 0
report("(F) series consistent at low orders", lower_ok)
report("(F) m3 = b^2 (1 + b^2)/2", sp.simplify(sol[m3] - b**2 * (1 + b**2) / 2) == 0)

out = {k.name: str(v) for k, v in sol.items()}
out["equations"] = {
    "m'": "(N F'^2/2)(x^2 + 2 sin^2 F) + sin^2 F (1 + sin^2 F/(2 x^2)),  N = 1 - 2 alpha m/x",
    "sigma'/sigma": "(alpha/x)(x^2 + 2 sin^2 F) F'^2",
    "matter": "(sigma N (x^2 + 2 sin^2F) F')' = sigma sin 2F (1 + N F'^2 + sin^2 F/x^2)",
    "units": "x = e f r, alpha = 4 pi G f^2, M_ADM = 4 pi (f/e) m(inf), f = F_pi/2",
}
with open(os.path.join(HERE, "derived_equations.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("ALL CHECKS PASS" if ok_all else "SOME CHECKS FAILED")
sys.exit(0 if ok_all else 1)
