"""Cross-check E2, step 1: symbolic derivations (independent of the original code).

From the radial energy density of the hedgehog in PLAN.md conventions
   L = (F^2/16) Tr dU dU^+ + (1/(32 e^2)) Tr [L_mu, L_nu]^2,  x = e F r,
   eps(x) = x^2 [ (1/8)(F'^2 + 2 s^2/x^2) + (1/2)(s^2/x^2)(s^2/x^2 + 2 F'^2) ],  s = sin F
derive
  (a) the Euler-Lagrange equation and compare to the report's form;
  (b) the series at the origin F = pi + a x + c3 x^3 + c5 x^5;
  (c) the large-x series F = C/x^2 + sum_k b_k / x^k (to 1/x^14), to check the report's
      -C^3/(21 x^6) - (4/3) C^3/x^8;
  (d) that the ANW g_A bracket x^2 [..] is the total derivative d/dx [x^3 h] with
      h = the rr-component of the current (so D = lim x^3 h = -2C).
Writes xc_derive.json with the coefficients (as strings) for xc_hedgehog.py.
"""
import json, sympy as sp

x = sp.symbols('x', positive=True)
F = sp.Function('F')
Fx = F(x); Fp = sp.diff(Fx, x)
s = sp.sin(Fx)
eps = x**2*(sp.Rational(1, 8)*(Fp**2 + 2*s**2/x**2)
            + sp.Rational(1, 2)*(s**2/x**2)*(s**2/x**2 + 2*Fp**2))
EL = sp.euler_equations(eps, Fx, x)[0].lhs   # d eps/dF - d/dx d eps/dF' = 0
EL = sp.simplify(EL)
Fpp = sp.diff(Fx, x, 2)
# report's form: (x^2 + 8 s^2) F'' + 2x F' + 4 sin2F F'^2 - sin2F - 4 sin2F s^2/x^2 = 0
rep = (x**2 + 8*s**2)*Fpp + 2*x*Fp + 4*sp.sin(2*Fx)*Fp**2 - sp.sin(2*Fx) - 4*sp.sin(2*Fx)*s**2/x**2
ratio = sp.simplify(sp.expand_trig(EL/rep))
print('EL / report_form =', ratio)
ok_el = sp.simplify(sp.expand_trig(EL + rep/4)) == 0 or sp.simplify(sp.expand_trig(EL - rep/4)) == 0 \
    or ratio.is_number
print('EL matches report form up to a constant factor:', ok_el)

# (b) origin series
a, c3, c5 = sp.symbols('a c3 c5')
Fo = sp.pi + a*x + c3*x**3 + c5*x**5
expr = rep.subs(Fpp, sp.diff(Fo, x, 2)).subs(Fp, sp.diff(Fo, x)).subs(Fx, Fo)
ser = sp.series(sp.expand_trig(expr), x, 0, 7).removeO()
ser = sp.expand(ser)
print('origin series: coeff x^1 (identically zero?) ->', sp.simplify(ser.coeff(x, 1)))
sol3 = sp.solve(ser.coeff(x, 3), c3)
c3v = sp.simplify(sol3[0])
sol5 = sp.solve(sp.expand(ser.coeff(x, 5)).subs(c3, c3v), c5)
c5v = sp.simplify(sol5[0])
print('c3 =', c3v, '  c5 =', c5v)
print('even coeffs (should vanish):', [sp.simplify(ser.coeff(x, k)) for k in (0, 2, 4)])

# (c) large-x series in y = 1/x, done with truncated Taylor polynomials (fast)
y = sp.symbols('y', positive=True)
C = sp.symbols('C')
nmax = 14
bs = sp.symbols('b3:%d' % (nmax + 1))
Fy = C*y**2 + sum(bs[k - 3]*y**k for k in range(3, nmax + 1))
def trunc(e, n=nmax + 3):
    e = sp.expand(e)
    return sum(e.coeff(y, k)*y**k for k in range(0, n + 1))
def sin_ser(u):   # u = O(y^2): need u^1..u^7 to reach y^14
    out = 0; pw = u; fact = 1
    for k in range(1, 9, 2):
        out += (-1)**((k - 1)//2)*pw/sp.factorial(k)
        pw = trunc(pw*u*u)
    return trunc(out)
sF = sin_ser(Fy)
s2F = sin_ser(2*Fy)
dFdx = trunc(-y**2*sp.diff(Fy, y))
d2Fdx2 = trunc(-y**2*sp.diff(dFdx, y))
# multiply ODE by y^2 to keep polynomial: (1 + 8 s^2 y^2) F'' + 2 y F' + 4 y^2 s2F F'^2 - y^2 s2F - 4 y^4 s2F s^2
ode = trunc((1 + 8*trunc(sF**2)*y**2)*d2Fdx2 + 2*y*dFdx + 4*y**2*trunc(s2F*trunc(dFdx**2))
            - y**2*s2F - 4*y**4*trunc(s2F*trunc(sF**2)))
sols = {}
for k in range(3, nmax + 1):
    co = sp.expand(ode.coeff(y, k + 2).subs(sols))   # b_k first appears at y^(k+2)
    unknown = bs[k - 3]
    if co.has(unknown):
        sols[unknown] = sp.factor(sp.solve(co, unknown)[0])
    elif sp.simplify(co) != 0:
        print('inconsistency at order', k, co)
print('large-x series coefficients:')
asym = {}
for k in range(3, nmax + 1):
    v = sols.get(bs[k - 3], None)
    print('  1/x^%d :' % k, v)
    asym[k] = str(v)
ok_asym = sp.simplify(sols[bs[6 - 3]] + C**3/21) == 0 and sp.simplify(sols[bs[8 - 3]] + sp.Rational(4, 3)*C**3) == 0
print('report asymptotics -C^3/21 x^-6 and -(4/3)C^3 x^-8 reproduced:', ok_asym)

# (d) the ANW g_A bracket as a total derivative on solutions:
#   x^2 * bracket == d/dx [ x^3 F' (1 + 8 s^2/x^2) ]   with F'' from the EL equation.
# Done with S = sin F, Cc = cos F symbols and S^2 = 1 - Cc^2 eliminated.
xs, S, Cc, P, Q = sp.symbols('xs S Cc P Q')   # P = F', Q = F''
s2 = 2*S*Cc
bracket = P + s2/xs + 4*(s2*P**2/xs + 2*S**2*P/xs**2 + S**2*s2/xs**3)
h = P*(1 + 8*S**2/xs**2)
# d/dx of x^3 h: d(S)/dx = Cc P, d(Cc)/dx = -S P, dP/dx = Q
def ddx(e):
    return sp.diff(e, xs) + sp.diff(e, S)*Cc*P - sp.diff(e, Cc)*S*P + sp.diff(e, P)*Q
dtot = ddx(xs**3*h)
repq = (xs**2 + 8*S**2)*Q + 2*xs*P + 4*s2*P**2 - s2 - 4*s2*S**2/xs**2
Qsol = sp.solve(repq, Q)[0]
diff_expr = sp.simplify(sp.together((xs**2*bracket - dtot).subs(Q, Qsol)).subs(S**2, 1 - Cc**2))
diff_expr = sp.simplify(sp.expand(sp.numer(sp.together(diff_expr))).subs(S**2, 1 - Cc**2))
print("x^2*ANW bracket - d/dx[x^3 F'(1+8s^2/x^2)] on solutions =", diff_expr)
ok_tot = (diff_expr == 0)
print("=> D = lim x^3 F'(1+8 s^2/x^2) = -2C:", ok_tot)

out = dict(EL_matches=bool(ok_el), c3=str(c3v), c5=str(c5v), asym=asym, asym_report_ok=bool(ok_asym),
           D_total_derivative=bool(ok_tot))
json.dump(out, open('/home/user/gifgaf0.github.io/seed/experiments/E2_skyrme_su3/crosscheck/xc_derive.json', 'w'), indent=1)
print('ALL OK:', ok_el and ok_asym and ok_tot)
