r"""Second-leg (blind) check, Q3 + Q4: derive chi from L, branch weights, Green limit.
Plane waves exp(i(qx - w t)); longitudinal sector (drho, theta, u_L), transverse u_T separately.
Linear source terms in L written as  s_r*drho + s_th*theta + s_u*u.
"""
import sympy as sp
import numpy as np
from sympy.calculus.euler import euler_equations

t, x = sp.symbols('t x', real=True)
q, w = sp.symbols('q omega', positive=True)
rs, rn, al, ga, M, mu, g = sp.symbols('rho_s rho_n alpha gamma M mu g', positive=True)
rho = rs + rn
th, dr, u = [sp.Function(n)(t, x) for n in ('theta', 'drho', 'u')]
s_r, s_th, s_u = [sp.Function(n)(t, x) for n in ('s_r', 's_th', 's_u')]

L = (-dr * sp.diff(th, t) - rho / 2 * sp.diff(th, x)**2
     + rn / 2 * (sp.diff(u, t) - sp.diff(th, x))**2
     - al / 2 * dr**2 - ga * dr * sp.diff(u, x) - M / 2 * sp.diff(u, x)**2
     + s_r * dr + s_th * th + s_u * u)
eqs = euler_equations(L, [dr, th, u], [t, x])

Dh, Thh, uh, Sr, Sth, Su = sp.symbols('Dh Th uh S_r S_th S_u')
amp = {dr: Dh, th: Thh, u: uh, s_r: Sr, s_th: Sth, s_u: Su}
def pw(expr):
    reps = {}
    for d in expr.atoms(sp.Derivative):
        fac = 1
        for var, n in d.variable_count:
            fac *= (-sp.I * w if var == t else sp.I * q)**n
        reps[d] = fac * amp[d.expr]
    return sp.expand(expr.xreplace(reps).xreplace(amp))
lin = [pw(e.lhs - e.rhs) for e in eqs]
A, b = sp.linear_eq_to_matrix(lin, [Dh, Thh, uh])       # A Phi = b,  b = -S
print("Fourier-space EOM matrix A (Hermitian):", A)
G = sp.simplify(-A.inv())                                  # Phi = G S
detA = sp.expand(A.det())

# density response to an external potential: L contains -U drho  ->  S_r = -U  -> chi = -G_rr
chi = sp.factor(-G[0, 0])
chi_given = q**2 * (rho * rn * w**2 - rs * M * q**2) / (
    rn * w**4 - (M + rho * rn * al - 2 * rn * ga) * q**2 * w**2 + rs * (al * M - ga**2) * q**4)
print("chi derived =", chi)
print("chi derived - chi given =", sp.simplify(chi - chi_given))
print("f-sum: w^2 chi/q^2 at w->oo =", sp.limit(w**2 * chi_given / q**2, w, sp.oo))

# ---- branch weights -------------------------------------------------------
X_ = sp.symbols('X', positive=True)          # X = w^2/q^2
Bc = (M + rho * rn * al - 2 * rn * ga)
Cc = rs * (al * M - ga**2)
Dpoly = rn * X_**2 - Bc * X_ + Cc
cp2, cm2 = sp.symbols('c_p2 c_m2', positive=True)
Zp = (rho * rn * cp2 - rs * M) / (rn * (cp2 - cm2))
Zm = -(rho * rn * cm2 - rs * M) / (rn * (cp2 - cm2))
print("chi = q^2 [Z_+/(w^2-c_+^2 q^2) + Z_-/(w^2-c_-^2 q^2)],  Z_+-= +-(rho rho_n c_+-^2 - rho_s M)/(rho_n(c_+^2-c_-^2))")
print("Z_+ + Z_- =", sp.simplify(Zp + Zm))
vals = {rs: 0.7, rn: 0.45, al: 3.1, ga: 0.6, M: 2.2}
disc = float((Bc**2 - 4 * rn * Cc).subs(vals))
cm2v = float(((Bc - sp.sqrt(disc)) / (2 * rn)).subs(vals)); cp2v = float(((Bc + sp.sqrt(disc)) / (2 * rn)).subs(vals))
qq, ww = 0.9, 1.3
Zpv = float(Zp.subs(vals).subs({cp2: cp2v, cm2: cm2v})); Zmv = float(Zm.subs(vals).subs({cp2: cp2v, cm2: cm2v}))
pf = qq**2 * (Zpv / (ww**2 - cp2v * qq**2) + Zmv / (ww**2 - cm2v * qq**2))
print(f"partial-fraction check: {pf:.12f} vs chi {float(chi_given.subs(vals).subs({q: qq, w: ww})):.12f};"
      f"  Z_+={Zpv:.4f}, Z_-={Zmv:.4f}")
X0 = rs * M / (rho * rn)
print("D(X0=rho_s M/(rho rho_n)) =", sp.factor(sp.simplify(Dpoly.subs(X_, X0))),
      " <= 0  => c_-^2 <= X0 <= c_+^2  => Z_+, Z_- >= 0")

# ---- transverse sector ----------------------------------------------------
uT, sT = sp.Function('uT')(t, x), sp.Function('sT')(t, x)
LT = rn / 2 * sp.diff(uT, t)**2 - mu / 2 * sp.diff(uT, x)**2 + sT * uT
eT = euler_equations(LT, [uT], [t, x])[0]
uTh, STh = sp.symbols('uTh STh')
amp.update({uT: uTh, sT: STh})
uTsol = sp.solve(pw(eT.lhs - eT.rhs), uTh)[0]
print("transverse response u_T =", sp.factor(uTsol), " -> pole w^2 = (mu/rho_n) q^2")

# ---- Green limit: chi at fixed (q, w) -------------------------------------
e = sp.symbols('e', positive=True)
chi_a = sp.together(chi_given.subs(al, 1 / e))
print("\nGreen limit, gamma fixed:  alpha*chi ->", sp.factor(sp.limit(chi_a / e, e, 0)))
chi_b = sp.together(chi_given.subs({al: 1 / e**2, ga: g / e}))
print("Green limit, gamma = g sqrt(alpha):  alpha*chi ->", sp.factor(sp.limit(chi_b / e**2, e, 0)))

# perturbative lower root and Z_-
delta = sp.factor(sp.simplify(Dpoly.subs(X_, X0).subs(al, 0)))   # D(X0) is alpha-independent
print("gamma fixed: c_-^2 = rho_s M/(rho rho_n) + delta/(rho rho_n alpha),  delta =", delta)
print("             Z_- ~ -delta/(rho rho_n alpha^2) =", sp.factor(-delta / (rho * rn)), "/alpha^2")

def branches(a, gam, p):
    r = p['rs'] + p['rn']
    P = [p['rn'], -(p['M'] + r * p['rn'] * a - 2 * p['rn'] * gam), p['rs'] * (a * p['M'] - gam**2)]
    cm, cp = np.sort(np.roots(P).real)
    Zp_ = (r * p['rn'] * cp - p['rs'] * p['M']) / (p['rn'] * (cp - cm))
    Zm_ = -(r * p['rn'] * cm - p['rs'] * p['M']) / (p['rn'] * (cp - cm))
    return cm, cp, Zm_, Zp_

p = dict(rs=0.7, rn=0.45, M=2.2)
gfix, gg = 0.6, 0.9
r_ = p['rs'] + p['rn']
print("\n  alpha     c_-^2(gam fixed)  alpha^2 Z_-   c_+^2/alpha | c_-^2(gam=g sqrt a)  alpha Z_-")
for a in [1e2, 1e3, 1e4, 1e5, 1e6]:
    cm, cp, Zm_, Zp_ = branches(a, gfix, p)
    cmb, cpb, Zmb, Zpb = branches(a, gg * np.sqrt(a), p)
    print(f"  {a:8.0e}   {cm:.6f}        {a*a*Zm_:.6f}     {cp/a:.4f}    |  {cmb:.6f}           {a*Zmb:.6f}")
print("  predicted:   c_-^2 ->", round(p['rs'] * p['M'] / (r_ * p['rn']), 6),
      "  a^2 Z_- ->", round(p['rs'] * (p['M'] / r_ - gfix)**2 / (r_ * p['rn']), 6),
      " c_+^2/a -> rho =", r_,
      "| c_-^2 ->", round(p['rs'] * (p['M'] - gg**2) / (r_ * p['rn']), 6),
      "  a Z_- ->", round(p['rs'] * gg**2 / (r_ * p['rn']), 6))

# ---- lower-mode residues of the full Green matrix: which channels couple ----
print("\nResidue of G (in w) at the lower pole w0 = c_- q (q=1): couplings of each source channel")
def residue_matrix(a, gam, qv=1.0):
    sub = {rs: p['rs'], rn: p['rn'], M: p['M'], al: a, ga: gam, q: qv}
    cm, cp, _, _ = branches(a, gam, p)
    w0 = np.sqrt(cm) * qv
    R = np.zeros((3, 3), dtype=complex)
    for i in range(3):
        for j in range(3):
            f = sp.lambdify(w, G[i, j].subs(sub), 'numpy')
            hh = 1e-7 * w0
            R[i, j] = 0.5 * (f(w0 + hh) * hh + f(w0 - hh) * (-hh))
    return R
for a in [1e2, 1e4, 1e6]:
    R = residue_matrix(a, gfix)
    print(f"  alpha={a:.0e}: |R_rr|={abs(R[0,0]):.3e} |R_thth|={abs(R[1,1]):.3e} |R_uu|={abs(R[2,2]):.3e}"
          f" |R_r,th|={abs(R[0,1]):.3e} |R_r,u|={abs(R[0,2]):.3e}  rank-1 check |R_rr R_thth-R_rth R_thr|={abs(R[0,0]*R[1,1]-R[0,1]*R[1,0]):.1e}")
print("  -> drho channel decouples (R_rr ~ alpha^-2, R_r,x ~ alpha^-1); theta and u_L channels stay O(1).")
print("  vortex longitudinal source vector (S_r, S_th, S_u) = (V.v - |v|^2/2, div(rho_s v) = 0, [rho_n d_t v]_L = 0)")

# ---- prescribed (alpha-independent) core mass deficit, Green limit ----
print("\nPrescribed core mass deficit Dc moving with the vortex (alpha -> oo, gamma fixed):")
Dc = sp.symbols('Dc')
def glim(expr):
    return sp.factor(sp.limit(sp.together(expr.subs(al, 1 / e)), e, 0))
# Berry term -Dc d_t theta  ->  S_th = d_t Dc -> -i w Dc ;  gamma term -gamma Dc d_x u -> S_u = i q gamma Dc
uB = glim(G[2, 1] * (-sp.I * w * Dc))
uG = glim(G[2, 2] * (sp.I * q * ga * Dc))
print("  u_L from Berry-term coupling  :", uB)
print("  u_L from gamma-term coupling  :", uG)
print("  u_L from energy vertex alpha*Dc on drho (equivalent form):", glim(G[2, 0] * (1 / e) * Dc).subs(e, 1 / al))
print("  u_L from alpha-independent drho vertex S (e.g. V.v):      ", glim(G[2, 0] * Dc))
