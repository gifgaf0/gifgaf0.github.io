#!/usr/bin/env python3
"""Symbolic checks of the identities quoted in the paper (T = 0 supersolid hydrodynamics, longitudinal sector):
(1) chi(q,w) = rho q^2 [F-/(w^2-c-^2 q^2) + F+/(w^2-c+^2 q^2)], F- + F+ = 1 (f-sum);
(2) F- = (c*^2 - c-^2)/(c+^2 - c-^2),  c*^2 = rho_s M/(rho rho_n);
(3) F- = rho_s (M - rho gamma)^2 / [rho^2 rho_n (c+^2 - c*^2)(c+^2 - c-^2)]  -> zero only if rho_s = 0 or M = rho gamma;
(4) compressibility sum rule sum F/c^2 = 1/c_kappa^2, c_kappa^2 = rho(alpha - gamma^2/M);
(5) incompressible limit alpha -> oo: c- -> c*, F- -> 0 like 1/alpha^2."""
import sympy as sp
w, q, x = sp.symbols("omega q x", positive=True)
rho, rn, al, ga, M = sp.symbols("rho rho_n alpha gamma M", positive=True)
rs = rho - rn
# response from the verified Lagrangian solution (external check, verify_lbc.py): numerator and denominator
num = q**2*(w**2*rho*rn - rs*M*q**2)
den = rn*w**4 - (M + al*rho*rn - 2*ga*rn)*q**2*w**2 + rs*(al*M - ga**2)*q**4
P = sp.expand(rn*x**2 - (M + al*rho*rn - 2*ga*rn)*x + rs*(al*M - ga**2))
cm2, cp2 = sp.symbols("c_m2 c_p2", positive=True)
cs2 = rs*M/(rho*rn)
# partial fractions in x = w^2/q^2: chi = rho q^2 * (x - cs2)/((x-cm2)(x-cp2)) * (q^2/q^2) ...
chi_x = sp.simplify((num/den).subs(w, sp.sqrt(x)*q))
target = rho*(x - cs2)/(rn*(P/rn)) * rn  # rho (x - c*^2)/((x-c-^2)(x-c+^2)) with P = rn (x-c-^2)(x-c+^2)
print("(1) chi(x) == rho (x - c*^2)/(P/rho_n) :", sp.simplify(chi_x - rho*(x - cs2)*rn/P) == 0)
# F- from residue at x = cm2 using P = rn (x-cm2)(x-cp2)
Fm = (cs2 - cm2)/(cp2 - cm2)          # residue form (definition)
# identity (3): P(c*^2) = -rho_s (M - rho gamma)^2 / rho^2
print("(3a) P(c*^2) + rho_s (M - rho gamma)^2/rho^2 == 0 :", sp.simplify(P.subs(x, cs2) + rs*(M - rho*ga)**2/rho**2) == 0)
# with P(c*^2) = rn (c*^2 - cm2)(c*^2 - cp2) => c*^2 - cm2 = rs (M - rho ga)^2 / (rho^2 rn (cp2 - c*^2))
Fm3 = rs*(M - rho*ga)**2/(rho**2*rn*(cp2 - cs2)*(cp2 - cm2))
chk = sp.simplify(Fm.subs(cm2, cs2 - rs*(M - rho*ga)**2/(rho**2*rn*(cp2 - cs2))) - Fm3.subs(cm2, cs2 - rs*(M - rho*ga)**2/(rho**2*rn*(cp2 - cs2))))
print("(3b) closed form for F- consistent with the residue form:", chk == 0)
# numeric check with the measured moduli (g = 22): rho=1
vals = {rho: 1, rn: 1-0.0951758, al: 43.73188, ga: 8.01530, M: 91.60676}
roots = sorted(float(r) for r in sp.Poly(P.subs(vals), x).nroots())
c_m2, c_p2 = roots
c_s2 = float(cs2.subs(vals))
print(f"    numeric: c-^2={c_m2:.6f} c+^2={c_p2:.6f} c*^2={c_s2:.6f}  F-(residue)={(c_s2-c_m2)/(c_p2-c_m2):.6f}  "
      f"F-(closed)={float(Fm3.subs(vals).subs({cm2: c_m2, cp2: c_p2})):.6f}  M/(rho gamma)={91.60676/8.0153:.2f}")
# (4) compressibility sum rule
ck2 = rho*(al - ga**2/M)
s4 = sp.simplify((Fm/cm2 + (1-Fm)/cp2).subs({cm2: c_m2, cp2: c_p2}).subs(vals) - (1/ck2).subs(vals))
print("(4) sum F/c^2 - 1/c_kappa^2 (numeric) =", float(s4))
# (5) incompressible limit
A = sp.symbols("A", positive=True)
vals5 = {rho: 1, rn: sp.Rational(9, 10), ga: 8, M: 92}
P5 = P.subs(vals5).subs(al, A)
for Aval in [1e2, 1e4, 1e6]:
    r = sorted(float(t) for t in sp.Poly(P5.subs(A, Aval), x).nroots())
    cs = float(cs2.subs(vals5))
    print(f"(5) alpha={Aval:.0e}: c-^2={r[0]:.6f} -> c*^2={cs:.6f}; F- = {(cs - r[0])/(r[1]-r[0]):.3e}")
