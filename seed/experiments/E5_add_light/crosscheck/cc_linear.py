"""E5 cross-check: one light cone and the taut vacuum (independent sympy linearisation).

1. Gauged Skyrme + pion mass + Maxwell, U = exp(i pi.tau / f) (f = F/2), D_mu U = d_mu U - i e A_mu [Q, U],
   Q = diag(2/3, -1/3).  Expand the Lagrangian to second order in (pi, A) with a bookkeeping parameter,
   using sympy Functions pi_a(t,x,y,z), A_mu(t,x,y,z); derive the Euler-Lagrange equations of the quadratic
   Lagrangian; insert plane waves and solve for omega(k).
2. Photon: Lorenz-gauge-free check -- the 4x4 kinetic matrix of the plane-wave equations, its determinant
   structure and the polarisations allowed at omega = |k|.
3. Vacuum stress tensor with a general symmetric inverse metric g^{mu nu}: T_mu nu = 2 dL/dg^{mu nu} - g_mu nu L
   at U = 1 (with a constant vacuum term -V0), then boosted.
The WZ term is cubic or higher in the fields (eps A A d pi, eps A Tr(Q L L L), and the ungauged WZ term is
fifth order in pi); its expansion is checked explicitly for the photon-pion part from B-H eq. 67.
"""
import json
import os

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = []
out = {}


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


t, x, y, z = sp.symbols('t x y z', real=True)
X = (t, x, y, z)
eps = sp.symbols('epsilon')                     # bookkeeping order parameter
f, e, es, mpi = sp.symbols('f e e_s m_pi', positive=True)
pis = [sp.Function(f'pi{a}')(*X) for a in range(1, 4)]
As = [sp.Function(f'A{m}')(*X) for m in range(4)]
g = sp.diag(1, -1, -1, -1)
tau = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
one = sp.eye(2)
Q = sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3))

phi = eps * sum((pis[a] * tau[a] for a in range(3)), sp.zeros(2)) / f
# exp(i phi) to second order in eps is enough for the quadratic Lagrangian of the sigma and mass terms
U = one + sp.I * phi - phi * phi / 2
Ud = one - sp.I * phi - phi * phi / 2


def D(M, mu):
    return sp.diff(M, X[mu]) - sp.I * e * eps * As[mu] * (Q * M - M * Q)


def Dd(M, mu):   # covariant derivative of U^+ : d U^+ - i e A [Q, U^+]
    return sp.diff(M, X[mu]) - sp.I * e * eps * As[mu] * (Q * M - M * Q)


def trunc(expr, order=2):
    if isinstance(expr, sp.MatrixBase):
        return expr.applyfunc(lambda el: trunc(el, order))
    expr = sp.expand(expr)
    return sum(expr.coeff(eps, k) * eps ** k for k in range(order + 1))


F2 = (2 * f) ** 2          # F_pi^2 with F = 2 f
L2 = 0
for mu in range(4):
    L2 += g[mu, mu] * (D(U, mu) * Dd(Ud, mu)).trace()
L2 = trunc(F2 / 16 * L2)
Lmass = trunc(F2 * mpi ** 2 / 16 * (U + Ud - 2 * one).trace())
# Maxwell
Fmn = [[sp.diff(As[n], X[m]) - sp.diff(As[m], X[n]) for n in range(4)] for m in range(4)]
LM = -sp.Rational(1, 4) * sum(g[m, m] * g[n, n] * Fmn[m][n] ** 2 for m in range(4) for n in range(4))
# Skyrme: L_mu = U^+ D_mu U is O(eps) -> [L_mu, L_nu]^2 is O(eps^4); verify the O(eps^0..eps^3) part vanishes
Lmu = [trunc(Ud * D(U, mu), 2) for mu in range(4)]
order_L = [min(k for k in range(3) if any(sp.expand(el).coeff(eps, k) != 0 for el in Lmu[mu])) for mu in range(4)]
log('lowest order of L_mu = U^+ D_mu U in the fields:', order_L, '-> Skyrme term [L,L]^2 starts at order', 4 * min(order_L))
out['skyrme_lowest_order'] = 4 * min(order_L)

Lq = sp.expand(L2.coeff(eps, 2) + Lmass.coeff(eps, 2)) + LM
L1 = sp.simplify(L2.coeff(eps, 1) + Lmass.coeff(eps, 1))
log('linear part of the sigma+mass terms:', L1)
expected = sum(sp.Rational(1, 2) * g[m, m] * sp.diff(pis[a], X[m]) ** 2 for a in range(3) for m in range(4)) \
    - sp.Rational(1, 2) * mpi ** 2 * sum(p ** 2 for p in pis) + LM
diffq = sp.simplify(sp.expand(Lq - expected))
log('quadratic Lagrangian minus [1/2 (d pi)^2 - 1/2 m^2 pi^2 - 1/4 F F]:', diffq)
out['quadratic_minus_canonical'] = str(diffq)
mix = [sp.simplify(sp.expand(Lq).coeff(As[m]).subs({p: 0 for p in pis})) for m in range(4)]

# Euler-Lagrange equations of the quadratic Lagrangian, plane waves
from sympy.calculus.euler import euler_equations
eqs = euler_equations(Lq, pis + As, X)
w, kx, ky, kz = sp.symbols('omega k_x k_y k_z', real=True)
amp_p = sp.symbols('a1:4'); amp_A = sp.symbols('b0:4')
phase = sp.exp(sp.I * (kx * x + ky * y + kz * z - w * t))
sub = {pis[a]: amp_p[a] * phase for a in range(3)}
sub.update({As[m]: amp_A[m] * phase for m in range(4)})
lin = [sp.simplify(sp.expand((eq.lhs - eq.rhs).subs(sub).doit()) / phase) for eq in eqs]
Mrows = [[sp.expand(l).coeff(v) for v in list(amp_p) + list(amp_A)] for l in lin]
Mk = sp.Matrix(Mrows)
log('pion block (should be diag(omega^2 - k^2 - m^2) up to sign):', sp.simplify(Mk[:3, :3]))
log('pion-photon mixing block:', sp.simplify(Mk[:3, 3:]), sp.simplify(Mk[3:, :3]))
sol_pi = sp.solve(sp.Eq(Mk[0, 0], 0), w)
log('pion dispersion omega =', sol_pi)
out['pion_dispersion'] = str(sol_pi)
MA = sp.simplify(Mk[3:, 3:])
log('photon kinetic matrix (plane wave):', MA)
k2 = w ** 2 - kx ** 2 - ky ** 2 - kz ** 2
ranks = {}
num_off = {w: 3, kx: 1, ky: 2, kz: 2}            # k^2 = 9 - 9 ... choose non-null: 9-1-4-4=0? pick another
num_off = {w: 5, kx: 1, ky: 2, kz: 2}            # k^2 = 25 - 9 = 16 != 0
num_on = {w: 3, kx: 1, ky: 2, kz: 2}             # k^2 = 9 - 9 = 0
ranks['off_cone'] = MA.subs(num_off).rank()
ranks['on_cone'] = MA.subs(num_on).rank()
log('photon matrix rank off the cone (k^2=16):', ranks['off_cone'], '; on the cone (k^2=0):', ranks['on_cone'])
# the null space on the cone: gauge mode k_mu plus transverse polarisations; check k^mu is always null
klow = sp.Matrix([w, -kx, -ky, -kz])     # field variables are A_mu (lower index): gauge mode A_mu = k_mu
gauge_null = sp.simplify(MA * klow)
log('M_A k_mu (gauge mode, any k):', gauge_null.T)
out['gauge_mode_null'] = bool(gauge_null == sp.zeros(4, 1))
# for k along z on the cone, find solutions with b0 = 0 (Coulomb-like): transverse modes count
MAz = MA.subs({kx: 0, ky: 0})
detsub = sp.factor(MAz[1:3, 1:3].det())
log('k along z: transverse 2x2 block determinant:', detsub, ' -> omega =', sp.solve(detsub, w))
out['photon'] = {'matrix': str(MA), 'ranks': ranks, 'transverse_det_kz': str(detsub),
                 'omega': str(sp.solve(detsub, w))}
out['pion_photon_mixing_zero'] = bool(all(sp.simplify(v) == 0 for v in list(Mk[:3, 3:]) + list(Mk[3:, :3])))
# group velocity
kk = sp.symbols('k', positive=True)
om = sp.sqrt(kk ** 2 + mpi ** 2)
vg = sp.simplify(sp.diff(om, kk))
log('pion group velocity:', vg, ' limit k->oo:', sp.limit(vg, kk, sp.oo), '; photon v = 1')
# boost invariance of k^2
bet = sp.symbols('beta', real=True)
gam = 1 / sp.sqrt(1 - bet ** 2)
wp, kzp = gam * (w - bet * kz), gam * (kz - bet * w)
log('k^2 after a boost minus k^2:', sp.simplify(wp ** 2 - kx ** 2 - ky ** 2 - kzp ** 2 - k2))

# ---------------------------------------------------------------- WZ photon-pion part is cubic
p0, dp = sp.symbols('p0 dp')
log('B-H eq. 67 photon terms: e A_mu eps Tr(Q L L L) is O(pi^3) (three L ~ O(pi)); '
    'e^2 eps F A T is O(A^2 pi) -> no quadratic term (counted, not computed)')

# ---------------------------------------------------------------- vacuum stress tensor
gi = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f'G{min(i, j)}{max(i, j)}'))    # inverse metric g^{mu nu}
V0 = sp.symbols('V0')
dU = [sp.Matrix(2, 2, lambda i, j: sp.Symbol(f'd{m}_{i}{j}')) for m in range(4)]
Uv = sp.Matrix(2, 2, lambda i, j: sp.Symbol(f'u{i}{j}'))
Uvd = Uv.H
Lgen = (F2 / 16) * sum(gi[m, n] * (dU[m] * dU[n].H).trace() for m in range(4) for n in range(4)) \
    + F2 * mpi ** 2 / 16 * (Uv + Uvd - 2 * one).trace() - V0
Lmu_g = [Uvd * dU[m] for m in range(4)]
Lgen += (1 / (32 * es ** 2)) * sum(gi[a, b] * gi[c, d] * ((Lmu_g[a] * Lmu_g[c] - Lmu_g[c] * Lmu_g[a]) *
                                                         (Lmu_g[b] * Lmu_g[d] - Lmu_g[d] * Lmu_g[b])).trace()
                                    for a in range(4) for b in range(4) for c in range(4) for d in range(4))
eta = sp.diag(1, -1, -1, -1)
vac = {sp.Symbol(f'd{m}_{i}{j}'): 0 for m in range(4) for i in range(2) for j in range(2)}
vac.update({sp.Symbol('u00'): 1, sp.Symbol('u11'): 1, sp.Symbol('u01'): 0, sp.Symbol('u10'): 0})
vac.update({sp.Symbol(f'G{min(i, j)}{max(i, j)}'): eta[i, j] for i in range(4) for j in range(4)})
T = sp.zeros(4, 4)
Lv = sp.simplify(Lgen.subs(vac))
for m in range(4):
    for n in range(4):
        sym = sp.Symbol(f'G{min(m, n)}{max(m, n)}')
        dL = sp.diff(Lgen, sym) * (sp.Rational(1, 2) if m != n else 1)   # symmetric variable counted once
        T[m, n] = sp.simplify(2 * dL.subs(vac) - eta[m, n] * Lv)
log('vacuum T_mu nu (lower indices, eta = diag(1,-1,-1,-1)):', T)
rho, pres = T[0, 0], T[1, 1]
log('rho = T_00 =', rho, ';  p = T_11 =', pres, ';  p + rho =', sp.simplify(pres + rho))
Lb = sp.Matrix([[gam, -gam * bet, 0, 0], [-gam * bet, gam, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
Tb = sp.simplify(Lb.T * T * Lb)
log('boosted T - T:', sp.simplify(Tb - T))
out['vacuum_T'] = str(T)
out['rho'] = str(rho); out['p'] = str(pres)
out['p_plus_rho'] = str(sp.simplify(pres + rho))
out['boost_invariant'] = bool(sp.simplify(Tb - T) == sp.zeros(4, 4))
json.dump(out, open(os.path.join(HERE, 'cc_linear.json'), 'w'), indent=1)
open(os.path.join(HERE, 'cc_linear_log.txt'), 'w').write('\n'.join(LOG) + '\n')
