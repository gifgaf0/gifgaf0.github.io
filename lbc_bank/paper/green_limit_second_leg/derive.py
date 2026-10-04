#!/usr/bin/env python3
"""
Blind second-leg computation: zero-T supersolid hydrodynamics (1 longitudinal direction),
Green's (incompressible) limit alpha -> infinity.

Routes:
  A. Euler-Lagrange of the full 3-field Lagrangian (theta, drho, u) -> 3x3 plane-wave det.
  B. Independent Hamiltonian route (canonical pairs (theta,-drho), (u,pi_u)) -> 4x4 linear
     generator, eigenvalues checked numerically against route A.
  C. Green limits (fixed gamma; gamma = g sqrt(alpha)) via series in eps = 1/sqrt(alpha).
  D. d-dimensional isotropic check: full vector Lagrangian in d=2,3 reproduces the 1D model
     with M = lambda + 2 mu for the longitudinal wave and c_T^2 = mu/rho_n for transverse;
     positive-definiteness of the (drho, eps_ij) energy; Green-limit bound.
"""
import sympy as sp
import random
from sympy.calculus.euler import euler_equations

I = sp.I
t, x = sp.symbols('t x', real=True)
w, q = sp.symbols('omega q', positive=True)
X = sp.Symbol('X')  # X = omega^2/q^2
rs, rn, al, M, mu = sp.symbols('rho_s rho_n alpha M mu', positive=True)
ga = sp.Symbol('gamma', real=True)
rho = rs + rn

# ---------------------------------------------------------------- A. Euler-Lagrange
th = sp.Function('theta')(t, x)
dr = sp.Function('drho')(t, x)
u = sp.Function('u')(t, x)
L = (-dr*sp.diff(th, t) - rho/2*sp.diff(th, x)**2
     + rn/2*(sp.diff(u, t) - sp.diff(th, x))**2
     - al/2*dr**2 - ga*dr*sp.diff(u, x) - M/2*sp.diff(u, x)**2)
eqs = euler_equations(L, [th, dr, u], [t, x])
A_, R_, U_ = sp.symbols('A R U')
E = sp.exp(I*(q*x - w*t))
sub = {th: A_*E, dr: R_*E, u: U_*E}
rows = []
for eq in eqs:
    expr = sp.simplify(eq.lhs.subs(sub).doit()/E)
    rows.append([sp.expand(expr).coeff(v) for v in (A_, R_, U_)])
Mat = sp.Matrix(rows)
det = sp.factor(sp.expand(Mat.det()))
print("3x3 plane-wave matrix (theta, drho, u):")
sp.pprint(Mat)
poly = sp.expand(sp.simplify(det.subs(w, sp.sqrt(X)*q)/q**4))
poly = sp.collect(sp.expand(poly), X)
# normalise to leading coefficient rho_n
lead = sp.Poly(poly, X).LC()
P_norm = sp.expand(poly*rn/lead)
print("\nDispersion polynomial (normalised, = 0):")
print(sp.collect(P_norm, X))
target = rn*X**2 - (M + rn*(rho*al - 2*ga))*X + rs*(al*M - ga**2)
assert sp.simplify(P_norm - target) == 0
print("  == rho_n X^2 - [M + rho_n(rho alpha - 2 gamma)] X + rho_s(alpha M - gamma^2)   [checked]")

S = rho*al - 2*ga + M/rn                    # c+^2 + c-^2
P = rs/rn*(al*M - ga**2)                     # c+^2 * c-^2
cp2 = (S + sp.sqrt(S**2 - 4*P))/2
cm2 = (S - sp.sqrt(S**2 - 4*P))/2

# transverse
up = sp.Function('uperp')(t, x)
Lp = rn/2*sp.diff(up, t)**2 - mu/2*sp.diff(up, x)**2
eqp = euler_equations(Lp, [up], [t, x])[0]
Up = sp.Symbol('Up')
cT2 = sp.solve(sp.simplify(eqp.lhs.subs(up, Up*E).doit()/E/Up).subs(w, sp.sqrt(X)*q), X)[0]
print("\nTransverse: c_T^2 =", cT2)

# ---------------------------------------------------------------- B. Hamiltonian route (numeric)
def ham_speeds(rs_, rn_, al_, ga_, M_, q_=1.0):
    import numpy as np
    # z = (theta, drho, u, pi_u);  -i omega z = A z
    A = np.array([[0, -al_, -1j*q_*ga_, 0],
                  [(rs_+rn_)*q_**2, 0, 0, -1j*q_],
                  [1j*q_, 0, 0, 1/rn_],
                  [0, 1j*q_*ga_, -M_*q_**2, 0]], dtype=complex)
    lam = np.linalg.eigvals(A)
    om = 1j*lam
    assert max(abs(om.imag)) < 1e-9*max(abs(om.real)), om
    return sorted(set(round(abs(o.real)/q_, 10) for o in om))

random.seed(1)
for _ in range(5):
    vals = dict(rho_s=random.uniform(.1, 2), rho_n=random.uniform(.1, 2), alpha=random.uniform(.5, 5),
                M=random.uniform(.5, 5))
    gmax = (vals['alpha']*vals['M'])**.5
    vals['gamma'] = random.uniform(-.9*gmax, .9*gmax)
    num = [float(sp.sqrt(e.subs({rs: vals['rho_s'], rn: vals['rho_n'], al: vals['alpha'],
                                 ga: vals['gamma'], M: vals['M']}))) for e in (cm2, cp2)]
    hs = ham_speeds(vals['rho_s'], vals['rho_n'], vals['alpha'], vals['gamma'], vals['M'])
    assert all(abs(a-b) < 1e-8 for a, b in zip(sorted(num), hs)), (num, hs)
print("Hamiltonian route agrees with EL dispersion at 5 random stable points.")

# limits that check the formula
print("\nchecks: rho_s->0  roots:", sp.solve(target.subs(rs, 0), X))
print("        rho_n->0  root :", sp.simplify(sp.solve(sp.limit(target, rn, 0), X)[0]))

# ---------------------------------------------------------------- C. Green limits
eps = sp.Symbol('epsilon', positive=True)   # alpha = 1/eps^2
g = sp.Symbol('g', real=True)
fs = sp.Symbol('f_s', positive=True)

def perturb_root(F, var, y0, n):
    """Solve F(y, eps)=0 as power series y = y0 + y1 eps + ... (F polynomial in y, eps)."""
    cs = sp.symbols('y1:%d' % (n+1))
    yser = y0 + sum(c*eps**(k+1) for k, c in enumerate(cs))
    Fe = sp.expand(F.subs(var, yser))
    sol = {}
    for k in range(1, n+1):
        ck = sp.expand(Fe.coeff(eps, k).subs(sol))
        sk = sp.solve(ck, cs[k-1])
        sol[cs[k-1]] = sp.simplify(sk[0])
    return sp.expand(yser.subs(sol))

def series_both(gamma_expr, n=3):
    # s = eps^2 S, p = eps^2 P are polynomials in eps (alpha = 1/eps^2).
    # c-^2 = Y : eps^2 Y^2 - s Y + p = 0, regular root Y0 = p0/s0
    # c+^2 = W/eps^2 : W^2 - s W + p eps^2 = 0, root W0 = s0
    s_ = sp.expand((S.subs({ga: gamma_expr}).subs(al, 1/eps**2))*eps**2)
    p_ = sp.expand((P.subs({ga: gamma_expr}).subs(al, 1/eps**2))*eps**2)
    Yv, Wv = sp.symbols('Yv Wv')
    s0, p0 = s_.subs(eps, 0), p_.subs(eps, 0)
    cm = perturb_root(eps**2*Yv**2 - s_*Yv + p_, Yv, sp.simplify(p0/s0), n)
    cpW = perturb_root(Wv**2 - s_*Wv + p_*eps**2, Wv, s0, n + 2)
    return cm, sp.expand(cpW/eps**2)

def coeffs(expr, lo, hi):
    e = sp.expand(expr)
    return {k: sp.factor(sp.simplify(e.coeff(eps, k))) for k in range(lo, hi+1)}

cm_a, cp_a = series_both(ga, 4)
print("\n(2a) fixed gamma, alpha = 1/eps^2:")
ca = coeffs(cm_a, 0, 2)
print("  c-^2 coefficients of eps^0, eps^1, eps^2(=1/alpha):", ca)
print("   eps^0 == f_s M/rho_n :", sp.simplify(ca[0] - (rs/rho)*M/rn) == 0)
print("   eps^2 == -rho_s (gamma - M/rho)^2/(rho rho_n) :",
      sp.simplify(ca[2] + rs*(ga - M/rho)**2/(rho*rn)) == 0)
cpa = coeffs(cp_a, -2, 0)
print("  c+^2 coefficients of eps^-2(=alpha), eps^-1, eps^0:", cpa,
      " eps^0 == M/rho - 2gamma:", sp.simplify(cpa[0] - (M/rho - 2*ga)) == 0)

cm_b, cp_b = series_both(g/eps, 3)
print("\n(2b) gamma = g sqrt(alpha), alpha = 1/eps^2:")
cb = coeffs(cm_b, 0, 1)
print("  c-^2 coefficients of eps^0, eps^1(=alpha^-1/2):", cb)
print("   eps^0 == f_s (M-g^2)/rho_n :", sp.simplify(cb[0] - (rs/rho)*(M - g**2)/rn) == 0,
      "; eps^1 == eps^0 * 2g/rho :", sp.simplify(cb[1] - cb[0]*2*g/rho) == 0)
cpb = coeffs(cp_b, -2, 0)
print("  c+^2 coefficients of eps^-2, eps^-1, eps^0:", cpb,
      " eps^0 == M/rho + f_s g^2/rho_n:", sp.simplify(cpb[0] - (M/rho + rs*g**2/(rho*rn))) == 0)

# ---------------------------------------------------------------- D. isotropic d-dim
lam_ = sp.Symbol('lambda', real=True)
def full_d_check(d):
    xs = sp.symbols('x1:%d' % (d+1), real=True)
    TH = sp.Function('TH')(t, *xs)
    DR = sp.Function('DR')(t, *xs)
    U = [sp.Function('U%d' % i)(t, *xs) for i in range(d)]
    grad = lambda f: [sp.diff(f, xi) for xi in xs]
    eps_ij = [[(sp.diff(U[i], xs[j]) + sp.diff(U[j], xs[i]))/2 for j in range(d)] for i in range(d)]
    tr = sum(eps_ij[i][i] for i in range(d))
    gth = grad(TH)
    Ld = (-DR*sp.diff(TH, t) - rho/2*sum(a**2 for a in gth)
          + rn/2*sum((sp.diff(U[i], t) - gth[i])**2 for i in range(d))
          - al/2*DR**2 - ga*DR*tr - lam_/2*tr**2
          - mu*sum(eps_ij[i][j]**2 for i in range(d) for j in range(d)))
    eqs = euler_equations(Ld, [TH, DR] + U, [t] + list(xs))
    amps = sp.symbols('a0:%d' % (d+2))
    Ed = sp.exp(I*(q*xs[0] - w*t))
    subs = {TH: amps[0]*Ed, DR: amps[1]*Ed}
    for i in range(d):
        subs[U[i]] = amps[2+i]*Ed
    Mt = sp.Matrix([[sp.expand(sp.simplify(e.lhs.subs(subs).doit()/Ed)).coeff(a) for a in amps]
                    for e in eqs])
    dd = sp.factor(sp.expand(Mt.det().subs(w, sp.sqrt(X)*q)))
    return dd

for d in (2, 3):
    dd = full_d_check(d)
    long_ok = sp.simplify(sp.Poly(dd, X).as_expr().subs(X, 0)) is not None
    # factor out longitudinal 1D polynomial with M = lambda+2mu and transverse (rho_n X - mu)^(d-1)
    longit = target.subs(M, lam_ + 2*mu)
    quo = sp.cancel(dd/(longit*(rn*X - mu)**(d-1)))
    print(f"\nd={d}: full-vector det / [1D longitudinal(M=lam+2mu) * (rho_n X - mu)^{d-1}] =", quo)

# positive definiteness of quadratic energy in (drho, eps_ij), d = 2, 3
K = sp.Symbol('K', real=True)
def energy_hessian(d, lam_val):
    n = d*(d+1)//2
    v = sp.symbols('e0:%d' % n)
    drs = sp.Symbol('dr')
    E_ = [[None]*d for _ in range(d)]
    k = 0
    for i in range(d):
        for j in range(i, d):
            E_[i][j] = E_[j][i] = v[k]; k += 1
    tr = sum(E_[i][i] for i in range(d))
    W = al/2*drs**2 + ga*drs*tr + lam_val/2*tr**2 + mu*sum(E_[i][j]**2 for i in range(d) for j in range(d))
    vars_ = [drs] + list(v)
    return sp.hessian(W, vars_)

for d in (2, 3):
    H = energy_hessian(d, K - 2*mu/d)
    cp = sp.factor(H.charpoly(sp.Symbol('z')).as_expr())
    print(f"\nd={d}: char. poly of energy Hessian (lambda = K - 2mu/d):", cp)
    # numeric test of the claimed criterion: PD <=> mu>0, alpha>0, alpha*K > gamma^2
    import numpy as np
    bad = 0
    for _ in range(4000):
        vals = {mu: random.uniform(-1, 3), al: random.uniform(.01, 3), K: random.uniform(-2, 4),
                ga: random.uniform(-3, 3)}
        if vals[mu] <= 0 or vals[al] <= 0:
            continue
        Hn = np.array(H.subs(vals).evalf(), dtype=float)
        pd = np.all(np.linalg.eigvalsh(Hn) > 0)
        claim = vals[al]*vals[K] > vals[ga]**2
        bad += (pd != claim)
    print(f"  PD <=> (mu>0, alpha>0, alpha K > gamma^2): mismatches in random test = {bad}")

# Green-limit ratio in the isotropic case and its bound
dsym = sp.Symbol('d', positive=True)
Miso = K + 2*(dsym - 1)*mu/dsym
ratio = fs*(Miso - g**2)/mu            # c-^2/c_T^2 in Green limit, g^2 = lim gamma^2/alpha in [0, K)
print("\nGreen-limit c-^2/c_T^2 (isotropic) =", sp.expand(ratio))
print("  with K - g^2 > 0 (stability)  ->  c-^2/c_T^2 > 2(d-1) f_s/d ;",
      " inf attained as K - g^2 -> 0+:", sp.simplify(ratio.subs(g**2, K)))
for d in (2, 3):
    print(f"  d={d}: bound c-^2/c_T^2 > {sp.Rational(2*(d-1), d)} f_s ;  c->c_T guaranteed for f_s >= {sp.Rational(d, 2*(d-1))}")
