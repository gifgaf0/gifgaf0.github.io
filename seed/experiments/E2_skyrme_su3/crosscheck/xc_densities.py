"""Cross-check E2, step 3: densities straight from the Lagrangian as written in PLAN.md.

Method (independent of the original's analytic L_mu construction): build the embedded SU(3)
hedgehog U0(r) = exp(i tau.n F(r)) (upper-left 2x2 block) as a 3x3 matrix on Cartesian
points, take *spatial* derivatives by 6th-order central finite differences of the matrix
field, time derivatives from U(t) = exp(i t Omega.lambda/2) U0 exp(-i t Omega.lambda/2)
(dU/dt = i[Omega.lambda/2, U0]), and evaluate

   static energy  eps = (1/16) sum_i Tr d_iU d_iU^+ - (1/32) sum_ij Tr [L_i,L_j]^2
   rotation       (1/2) i_ab W_a W_b = -(1/16) Tr L_0^2 - (1/16) sum_i Tr [L_0,L_i]^2
   stress         T_ij = (1/8) Re Tr d_iU d_jU^+ - (1/8) sum_k Tr [L_i,L_k][L_j,L_k] - delta_ij eps

(units F_pi/e for energies, x = e F_pi r, I = (1/(e^3 F_pi)) int d^3x i_ab; T_ij from
T_mn = 2 dL/dg^mn - g_mn L in the mostly-minus metric).  Angular averages use a
Lebedev-free product rule: 14-point Gauss-Legendre in cos(theta) x 24-point trapezoid in phi.
The angular means are compared with the radial formulas used by the report:

   eps      = (1/8)(F'^2 + 2 s^2/x^2) + (1/2)(s^2/x^2)(s^2/x^2 + 2F'^2)
   <i_11>   = (1/6) s^2 [1 + 4(F'^2 + s^2/x^2)]          (=> I1 = (2pi/3) Lambda/(e^3F))
   <i_44>   = (1/8)(1 - cos F)(1 + F'^2 + 2 s^2/x^2)      (=> I2 = (pi/2) J2/(e^3F))
   T_rr, T_thth as in the report's derrick section.

The identities hold for any profile (no equation of motion needed), so a deliberately
arbitrary test profile is used.  Deterministic.  Writes xc_densities.json.
"""
import json, math, time
import numpy as np

OUT = '/home/user/gifgaf0.github.io/seed/experiments/E2_skyrme_su3/crosscheck/'
t0 = time.time()

lam = np.zeros((8, 3, 3), complex)
lam[0][0, 1] = lam[0][1, 0] = 1
lam[1][0, 1] = -1j; lam[1][1, 0] = 1j
lam[2][0, 0] = 1; lam[2][1, 1] = -1
lam[3][0, 2] = lam[3][2, 0] = 1
lam[4][0, 2] = -1j; lam[4][2, 0] = 1j
lam[5][1, 2] = lam[5][2, 1] = 1
lam[6][1, 2] = -1j; lam[6][2, 1] = 1j
lam[7] = np.diag([1, 1, -2])/math.sqrt(3)
# sanity: Tr(l_a l_b) = 2 delta_ab
assert np.allclose(np.einsum('aij,bji->ab', lam, lam), 2*np.eye(8))
tau = lam[:3, :2, :2]


def Fprof(r):
    # arbitrary smooth test profile with F(0) = pi (not a solution)
    return math.pi*math.exp(-0.55*r)*(1 + 0.2*r - 0.03*r*r) + 0.1*math.sin(r)*math.exp(-r)


def dFprof(r, h=1e-6):
    return (Fprof(r + h) - Fprof(r - h))/(2*h)


def U0(v):
    r = np.linalg.norm(v); n = v/r; F = Fprof(r)
    U = np.eye(3, dtype=complex)
    U[:2, :2] = math.cos(F)*np.eye(2) + 1j*math.sin(F)*np.einsum('i,ijk->jk', n, tau)
    return U


def dU(v, i, h=2e-3):
    e = np.zeros(3); e[i] = h
    c = [(-1/60, -3), (3/20, -2), (-3/4, -1), (3/4, 1), (-3/20, 2), (1/60, 3)]
    return sum(w*U0(v + k*e) for w, k in c)/h


def comm(a, b):
    return a@b - b@a


def local(v):
    U = U0(v); Ud = U.conj().T
    D = [dU(v, i) for i in range(3)]
    L = [Ud@D[i] for i in range(3)]
    e2 = sum(np.trace(D[i]@D[i].conj().T).real for i in range(3))/16
    e4 = -sum(np.trace(comm(L[i], L[j])@comm(L[i], L[j])).real for i in range(3) for j in range(3))/32
    eps = e2 + e4
    T = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            T[i, j] = np.trace(D[i]@D[j].conj().T).real/8 \
                - sum(np.trace(comm(L[i], L[k])@comm(L[j], L[k])).real for k in range(3))/8 \
                - (eps if i == j else 0.0)
    # rotational quadratic form: q(W) = -(1/16) Tr L0^2 - (1/16) sum_i Tr [L0,L_i]^2 = (1/2) i_ab W_a W_b
    L0s = []
    for a in range(8):
        dUdt = 1j*comm(lam[a]/2, U)
        L0s.append(Ud@dUdt)
    def bil(A, B):  # symmetric bilinear form from q
        val = -np.trace(A@B).real/16
        val += -sum(np.trace(comm(A, L[i])@comm(B, L[i])).real for i in range(3))/16
        return val
    iab = np.array([[2*bil(L0s[a], L0s[b]) for b in range(8)] for a in range(8)])
    return eps, e2, e4, T, iab


gx, gw = np.polynomial.legendre.leggauss(14)
nphi = 24
phis = 2*math.pi*np.arange(nphi)/nphi


def angular_mean(r):
    acc_eps = acc_e2 = acc_e4 = 0.0; acc_i = np.zeros((8, 8)); acc_rr = acc_tt = 0.0
    for ct, w in zip(gx, gw):
        st = math.sqrt(1 - ct*ct)
        for ph in phis:
            n = np.array([st*math.cos(ph), st*math.sin(ph), ct])
            et = np.array([ct*math.cos(ph), ct*math.sin(ph), -st])
            eps, e2, e4, T, iab = local(r*n)
            ww = w/(2*nphi)
            acc_eps += ww*eps; acc_e2 += ww*e2; acc_e4 += ww*e4; acc_i += ww*iab
            acc_rr += ww*n@T@n; acc_tt += ww*et@T@et
    return acc_eps, acc_e2, acc_e4, acc_i, acc_rr, acc_tt


rows = []
worst = dict(eps=0, i11=0, i44=0, off=0, i88=0, Trr=0, Ttt=0, Tpoint=0)
for r in [0.35, 0.9, 1.6, 2.7, 4.1]:
    F = Fprof(r); P = dFprof(r); s = math.sin(F); x = r
    eps_ref = (1/8)*(P*P + 2*s*s/x/x) + 0.5*(s*s/x/x)*(s*s/x/x + 2*P*P)
    i11_ref = (1/6)*s*s*(1 + 4*(P*P + s*s/x/x))
    i44_ref = (1/8)*(1 - math.cos(F))*(1 + P*P + 2*s*s/x/x)
    lt = s/x
    Trr_ref = (1/8)*(P*P - 2*lt*lt) + 0.5*lt*lt*(2*P*P - lt*lt)
    Ttt_ref = -(1/8)*P*P + 0.5*lt**4
    eps, e2, e4, iab, Trr, Ttt = angular_mean(r)
    i11 = np.mean([iab[k, k] for k in range(3)])
    i44 = np.mean([iab[k, k] for k in range(3, 7)])
    off = np.max(np.abs(iab - np.diag(np.diag(iab))))
    spread13 = np.ptp([iab[k, k] for k in range(3)]); spread47 = np.ptp([iab[k, k] for k in range(3, 7)])
    rel = lambda a, b: abs(a/b - 1)
    worst['eps'] = max(worst['eps'], rel(eps, eps_ref))
    worst['i11'] = max(worst['i11'], rel(i11, i11_ref), spread13/i11_ref)
    worst['i44'] = max(worst['i44'], rel(i44, i44_ref), spread47/i44_ref)
    worst['off'] = max(worst['off'], off/i11_ref)
    worst['i88'] = max(worst['i88'], abs(iab[7, 7])/i11_ref)
    worst['Trr'] = max(worst['Trr'], abs(Trr - Trr_ref)/abs(eps_ref))
    worst['Ttt'] = max(worst['Ttt'], abs(Ttt - Ttt_ref)/abs(eps_ref))
    rows.append(dict(r=r, F=F, Fp=P, eps=eps, eps_ref=eps_ref, i11=i11, i11_ref=i11_ref, i44=i44,
                     i44_ref=i44_ref, i88=iab[7, 7], offdiag=off, Trr=Trr, Trr_ref=Trr_ref, Ttt=Ttt, Ttt_ref=Ttt_ref))
    print('r=%.2f  eps %.10f/%.10f  i11 %.10f/%.10f  i44 %.10f/%.10f  i88 %.1e  off %.1e  Trr %.3e/%.3e  Ttt %.3e/%.3e'
          % (r, eps, eps_ref, i11, i11_ref, i44, i44_ref, iab[7, 7], off, Trr, Trr_ref, Ttt, Ttt_ref))

# pointwise check of the hedgehog T_ij structure at one generic point (T = Trr n n + Ttt (1 - n n))
v = np.array([0.7, -1.1, 0.4]); r = np.linalg.norm(v); n = v/r
F = Fprof(r); P = dFprof(r); s = math.sin(F); lt = s/r
Trr_ref = (1/8)*(P*P - 2*lt*lt) + 0.5*lt*lt*(2*P*P - lt*lt)
Ttt_ref = -(1/8)*P*P + 0.5*lt**4
_, _, _, T, _ = local(v)
Tmodel = Trr_ref*np.outer(n, n) + Ttt_ref*(np.eye(3) - np.outer(n, n))
worst['Tpoint'] = float(np.max(np.abs(T - Tmodel)))
print('pointwise T_ij vs hedgehog form: max dev %.1e' % worst['Tpoint'])

tol = 1e-9
checks = {
    'energy density = radial formula (PLAN Lagrangian normalisation)': worst['eps'] < tol,
    "i_aa (a=1..3) = (1/6)s^2[1+4(F'^2+s^2/x^2)] -> I1 = (2pi/3)Lambda/(e^3F)": worst['i11'] < tol,
    "i_aa (a=4..7) = (1/8)(1-cosF)(1+F'^2+2s^2/x^2) -> I2 = (pi/2)J2/(e^3F)": worst['i44'] < tol,
    'i_88 = 0 and off-diagonal i_ab = 0': worst['i88'] < tol and worst['off'] < tol,
    'T_rr, T_thth as used for von Laue': worst['Trr'] < tol and worst['Ttt'] < tol and worst['Tpoint'] < tol,
}
for k, val in checks.items():
    print('CHECK %-75s %s' % (k, 'PASS' if val else 'FAIL'))
print('worst relative deviations:', {k: '%.1e' % val for k, val in worst.items()})
json.dump(dict(rows=rows, worst=worst, checks=checks, all_pass=all(checks.values()),
               runtime_s=time.time() - t0), open(OUT + 'xc_densities.json', 'w'), indent=1, default=float)
print('all checks pass:', all(checks.values()), ' runtime %.1f s' % (time.time() - t0))
