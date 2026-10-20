"""Cross-check E2, step 5: side claims about g_A, the asymptotic tail and the Dirichlet bias.

(a) Axial Noether current computed numerically from the PLAN.md Lagrangian: J^a_i = dL/d(d_i eps)
    for the local axial rotation U -> exp(i eps tau^a/2) U exp(i eps tau^a/2), obtained by
    replacing d_iU -> d_iU + eta (i/2){tau^a, U} and differentiating the (degree-4 in eta)
    static Lagrangian with an exact 5-point stencil.  Normalisation <0|A|pi> = f_pi p.
    Hedgehog profile: my own shooting solution (xc_profile.npz from xc_hedgehog.py).
    Then:  G_ball(R) = int_{|x|<R} J^3_3 d^3x  (units 1/e^2), and with <p up|D33|p up> = -1/3
    the ball-integral g_A is -(2/3) G_ball / e^2.  Compare with ANW's -(pi/(3e^2)) D, D = -2C,
    and with the Goldberger-Treiman-type far-field value 2 pi C/(3 e^2) (derived by hand in
    CROSSCHECK.md: pi^a -> (g_A/(8 pi f_pi)) <sigma_i tau_a> n_i / r^2 in the chiral limit).
(b) the report's large-x asymptotics: relative residual of C/x^2 and of the 3-term form.
(c) Dirichlet box F(X) = 0 without tails: M, Lambda, D for X = 10, 20, 40 (report: Lambda
    37.09/44.11/47.59, M +0.120%/+0.015% and D -25.71/-25.89 at X = 20/40).
Writes xc_axial.json.  Deterministic.
"""
import json, math, time
import numpy as np
from scipy.interpolate import CubicHermiteSpline
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

OUT = '/home/user/gifgaf0.github.io/seed/experiments/E2_skyrme_su3/crosscheck/'
t0 = time.time()
Z = np.load(OUT + 'xc_profile.npz')
xs, Fs, dFs, C = Z['x'], Z['F'], Z['dF'], float(Z['C'])
H = json.load(open(OUT + 'xc_hedgehog.json'))
D_mine = H['D']


def rhs_F(x, F, P):
    s = math.sin(F); s2F = math.sin(2*F)
    return -(2*x*P + 4*s2F*P*P - s2F - 4*s2F*s*s/(x*x))/(x*x + 8*s*s)


d2Fs = np.array([rhs_F(max(x, 1e-6), F, P) for x, F, P in zip(xs, Fs, dFs)])
Fi = CubicHermiteSpline(xs, Fs, dFs)
dFi = CubicHermiteSpline(xs, dFs, d2Fs)

tau = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], complex)


def comm(a, b):
    return a@b - b@a


def Lstatic(U, D):
    Ud = U.conj().T
    L = [Ud@d for d in D]
    l2 = -sum(np.trace(d@d.conj().T).real for d in D)/16
    l4 = sum(np.trace(comm(L[i], L[j])@comm(L[i], L[j])).real for i in range(3) for j in range(3))/32
    return l2 + l4


def field(v):
    r = np.linalg.norm(v); n = v/r
    F = float(Fi(r)); P = float(dFi(r)); s, c = math.sin(F), math.cos(F)
    tn = np.einsum('k,kij->ij', n, tau)
    U = c*np.eye(2) + 1j*s*tn
    D = []
    for i in range(3):
        dn = (np.eye(3)[i] - n[i]*n)/r
        D.append(-s*P*n[i]*np.eye(2) + 1j*(np.einsum('k,kij->ij', dn, tau)*s + tn*c*P*n[i]))
    return U, D


def current(v, a, i):
    U, D = field(v)
    dU = 0.5j*(tau[a]@U + U@tau[a])
    h = 0.1
    def f(eta):
        DD = [D[k] + (eta*dU if k == i else 0) for k in range(3)]
        return Lstatic(U, DD)
    return (f(-2*h) - 8*f(-h) + 8*f(h) - f(2*h))/(12*h)


gx, gw = np.polynomial.legendre.leggauss(12)
nphi = 16
phis = 2*math.pi*np.arange(nphi)/nphi
dirs = []
for ct, w in zip(gx, gw):
    st = math.sqrt(1 - ct*ct)
    for ph in phis:
        dirs.append((np.array([st*math.cos(ph), st*math.sin(ph), ct]), w*2*math.pi/nphi))


def shell(r, rr=False):
    """angular integral of J^3_3 and (if rr) of n_i n_a J^a_i (all a,i) at radius r"""
    s33 = 0.0; srr = 0.0
    for n, w in dirs:
        v = r*n
        j33 = current(v, 2, 2)
        s33 += w*j33
        if rr:
            srr += w*sum(n[i]*n[a]*current(v, a, i) for a in range(3) for i in range(3))
    return s33, srr


# radial integration of the ball integral on [0, R] with Gauss-Legendre panels
edges = [0, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24]
gr, gwr = np.polynomial.legendre.leggauss(10)
G = 0.0; Gs = {}
for lo, hi in zip(edges[:-1], edges[1:]):
    for t, w in zip(gr, gwr):
        r = 0.5*(hi - lo)*(t + 1) + lo
        G += 0.5*(hi - lo)*w*r*r*shell(r)[0]
    Gs[hi] = G
s33R, srrR = shell(24.0, rr=True)
surf = (24.0**3)*srrR/3        # pure-surface form: int_ball J_i = oint x_i (n.J) dS -> (R^3/3) oint n_i n_a J^a_i
print('ball integral G(R) of J^3_3:', {k: round(v, 6) for k, v in Gs.items()})
print('surface form at R=24: %.6f' % surf)
gA_ball_e2 = -(2/3)*Gs[24]
gA_ANW_e2 = -(math.pi/3)*D_mine
gA_GT_e2 = 2*math.pi*C/3
print('g_A e^2: ball %.6f   ANW formula %.6f   far-field (GT) %.6f   ratio ball/ANW = %.6f' %
      (gA_ball_e2, gA_ANW_e2, gA_GT_e2, gA_ball_e2/gA_ANW_e2))
e_ANW = H['ANW']['e']
print('at the ANW fit e = %.5f: |g_A(ball)| = %.4f, g_A(ANW) = %.4f' % (e_ANW, abs(gA_ball_e2)/e_ANW**2, gA_ANW_e2/e_ANW**2))

# (b) asymptotic tail check (note: xc_profile.npz uses the 6-term series beyond X = 25, so the
#     x = 40 entry only measures the size of the omitted series terms, not solver error)
asym_rows = {}
for x in [10.0, 20.0, 40.0]:
    F = float(Fi(x))
    one = C/x**2; three = C/x**2 - C**3/(21*x**6) - 4*C**3/(3*x**8)
    asym_rows[x] = dict(F=F, rel_one=abs(one/F - 1), rel_three=abs(three/F - 1), abs_three=abs(three - F))
    print('x=%g: |C/x^2 / F - 1| = %.1e   |3-term/F - 1| = %.1e  (abs %.1e)' % (x, abs(one/F - 1), abs(three/F - 1), abs(three - F)))


# (c) Dirichlet box F(X) = 0, no tails: single-parameter shooting in a = F'(0)
def origin(a, x):
    c3 = (-4*a**5 - 2*a**3)/(120*a**2 + 15)
    c5 = a**5*(448*a**6 + 88*a**4 + 32*a**2 + 5)/(175*(512*a**6 + 192*a**4 + 24*a**2 + 1))
    return math.pi + a*x + c3*x**3 + c5*x**5, a + 3*c3*x**2 + 5*c5*x**4


def dens(x, F, P):
    s = math.sin(F); s2F = math.sin(2*F); lt = s/x
    e = x*x*((1/8)*(P*P + 2*lt*lt) + 0.5*lt*lt*(lt*lt + 2*P*P))
    lam = x*x*s*s*(1 + 4*(P*P + lt*lt))
    j2 = x*x*2*math.sin(F/2)**2*(1 + P*P + 2*lt*lt)
    dbr = x*x*(P + s2F/x + 4*(s2F*P*P/x + 2*s*s*P/(x*x) + s*s*s2F/x**3))
    return [e, lam, j2, dbr]


def box(X):
    x0 = 1e-3
    def endF(a):
        F0, P0 = origin(a, x0)
        so = solve_ivp(lambda x, Y: [Y[1], rhs_F(x, Y[0], Y[1])], (x0, X), [F0, P0], method='DOP853',
                       rtol=1e-12, atol=1e-14)
        return so.y[0, -1]
    a = brentq(endF, -1.2, -0.9, xtol=1e-14)
    F0, P0 = origin(a, x0)
    fun = lambda x, Y: [Y[1], rhs_F(x, Y[0], Y[1])] + dens(x, Y[0], Y[1])
    so = solve_ivp(fun, (x0, X), [F0, P0, 0, 0, 0, 0], method='DOP853', rtol=1e-12, atol=1e-14)
    I = so.y[2:, -1]
    return dict(a=a, M=4*math.pi*I[0], Lambda=I[1], J2=I[2], D=I[3])


boxes = {}
for X in [10.0, 20.0, 40.0]:
    b = box(X); boxes[X] = b
    print('Dirichlet X=%g: M %+.3f%%  Lambda %.3f (%+.1f%%)  J2 %.3f (%+.1f%%)  D %.3f  (D/C = %.3f)' %
          (X, 100*(b['M']/H['M'] - 1), b['Lambda'], 100*(b['Lambda']/H['Lambda'] - 1), b['J2'],
           100*(b['J2']/H['J2'] - 1), b['D'], b['D']/C))

checks = {
    # (overall sign of J depends on the orientation convention of the Noether current; magnitudes compared)
    '|ball-integral g_A| = (2/3) ANW g_A (to 1e-4)': abs(abs(gA_ball_e2/gA_ANW_e2) - 2/3) < 1e-4,
    'ball integral equals its surface form at R=24 (1e-4)': abs(surf/Gs[24] - 1) < 1e-4,
    'ANW formula = far-field (Goldberger-Treiman) value 2piC/3 (1e-9)': abs(gA_ANW_e2/gA_GT_e2 - 1) < 1e-9,
}
for k, v in checks.items():
    print('CHECK %-70s %s' % (k, 'PASS' if v else 'FAIL'))
json.dump(dict(G_ball=Gs, surface_R24=surf, gA_ball_e2=gA_ball_e2, gA_ANW_e2=gA_ANW_e2, gA_GT_e2=gA_GT_e2,
               ratio_ball_ANW=gA_ball_e2/gA_ANW_e2, gA_ball_ANWfit=gA_ball_e2/e_ANW**2,
               asymptotics={str(k): v for k, v in asym_rows.items()}, dirichlet={str(k): v for k, v in boxes.items()},
               checks=checks, all_pass=all(checks.values()), runtime_s=time.time() - t0),
          open(OUT + 'xc_axial.json', 'w'), indent=1, default=float)
print('all checks pass:', all(checks.values()), ' runtime %.1f s' % (time.time() - t0))
