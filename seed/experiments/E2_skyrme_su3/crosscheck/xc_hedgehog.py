"""Cross-check E2, step 2: the B=1 hedgehog by two-sided SHOOTING (not collocation).

Method (deliberately different from the original's Chebyshev collocation):
  * outward integration from x0 = 1e-3 with the origin series F = pi + a x + c3 x^3 + c5 x^5,
  * inward integration from X with the large-x series F = C/x^2 + ... (to 1/x^14, xc_derive.py),
  * DOP853, rtol 1e-13; match F and F' at x_m; 2 unknowns (a, C), Newton with FD Jacobian.
  * All integrals are carried as extra ODE components (quadrature along the ODE),
    plus [0, x0] from the origin series and [X, inf) from the asymptotic series (scipy quad
    in y = 1/x).
Conventions (PLAN.md E2): L = (F^2/16) Tr dU dU^+ + (1/(32e^2)) Tr[L,L]^2, F_pi = 186-MeV
convention, x = e F_pi r.  Energies in F_pi/e; I = coef/(e^3 F_pi).
Writes xc_hedgehog.json.  Deterministic.  Runtime ~1 min on one core.
"""
import json, math, time
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import minimize_scalar, brentq

OUT = '/home/user/gifgaf0.github.io/seed/experiments/E2_skyrme_su3/crosscheck/'
t0 = time.time()
PI = math.pi


def rhs_F(x, F, P):
    s = math.sin(F); s2F = math.sin(2*F)
    return -(2*x*P + 4*s2F*P*P - s2F - 4*s2F*s*s/(x*x))/(x*x + 8*s*s)


def dens(x, F, P):
    """integrands (per dx), dimensionless; returns array of
    [e2, e4, Lambda, J2, Dbracket, r2B, B, p]  with e2,e4 such that E = 4 pi int (e2+e4) dx."""
    s = math.sin(F); c = math.cos(F); s2F = math.sin(2*F)
    lr = P; lt = s/x
    e2 = x*x*(1/8)*(lr*lr + 2*lt*lt)
    e4 = x*x*0.5*(lt*lt)*(lt*lt + 2*lr*lr)
    lam = x*x*s*s*(1 + 4*(lr*lr + lt*lt))
    # 1 - cos F written as 2 sin^2(F/2): the naive form underflows to 0 for F < ~1.5e-8
    # (x > ~2e4), which silently dropped ~1.2e-3 of the J2 tail in the first attempt.
    j2 = x*x*2*math.sin(0.5*F)**2*(1 + lr*lr + 2*lt*lt)
    dbr = x*x*(P + s2F/x + 4*(s2F*P*P/x + 2*s*s*P/(x*x) + s*s*s2F/x**3))
    r2 = -(2/PI)*x*x*s*s*P
    bb = -(2/PI)*s*s*P
    Trr = (1/8)*(lr*lr - 2*lt*lt) + 0.5*lt*lt*(2*lr*lr - lt*lt)
    Ttt = -(1/8)*lr*lr + 0.5*lt**4
    pp = x*x*(Trr + 2*Ttt)/3
    return np.array([e2, e4, lam, j2, dbr, r2, bb, pp])


NQ = 8


def sys_full(x, Y):
    F, P = Y[0], Y[1]
    return np.concatenate(([P, rhs_F(x, F, P)], dens(x, F, P)))


def origin(a, x):
    c3 = (-4*a**5 - 2*a**3)/(120*a**2 + 15)
    c5 = a**5*(448*a**6 + 88*a**4 + 32*a**2 + 5)/(175*(512*a**6 + 192*a**4 + 24*a**2 + 1))
    F = PI + a*x + c3*x**3 + c5*x**5
    P = a + 3*c3*x**2 + 5*c5*x**4
    return F, P


def asym(C, x):
    y = 1.0/x
    co = {2: C, 6: -C**3/21, 8: -4*C**3/3, 10: 2*C**5/385, 12: 136*C**5/273,
          14: -8*C**5*(2*C**2 - 21021)/24255}
    F = sum(v*y**k for k, v in co.items())
    P = sum(-k*v*y**(k + 1) for k, v in co.items())
    return F, P


RT, AT = 1e-13, 1e-15


def shoot(a, C, x0, xm, X, quadrature=False):
    F0, P0 = origin(a, x0)
    F1, P1 = asym(C, X)
    if quadrature:
        y0 = np.concatenate(([F0, P0], np.zeros(NQ)))
        y1 = np.concatenate(([F1, P1], np.zeros(NQ)))
        fun = sys_full
    else:
        y0 = np.array([F0, P0]); y1 = np.array([F1, P1])
        fun = lambda x, Y: [Y[1], rhs_F(x, Y[0], Y[1])]
    so = solve_ivp(fun, (x0, xm), y0, method='DOP853', rtol=RT, atol=AT, dense_output=quadrature)
    si = solve_ivp(fun, (X, xm), y1, method='DOP853', rtol=RT, atol=AT, dense_output=quadrature)
    return so, si


def solve(x0=1e-3, xm=1.5, X=25.0, a=-1.0, C=8.6):
    v = np.array([a, C], float)
    for it in range(30):
        so, si = shoot(v[0], v[1], x0, xm, X)
        r = so.y[:2, -1] - si.y[:2, -1]
        if np.max(np.abs(r)) < 1e-13:
            break
        J = np.zeros((2, 2))
        for j, hj in enumerate((1e-6, 1e-6)):
            w = v.copy(); w[j] += hj
            so2, si2 = shoot(w[0], w[1], x0, xm, X)
            J[:, j] = ((so2.y[:2, -1] - si2.y[:2, -1]) - r)/hj
        v = v - np.linalg.solve(J, r)
    return v, it, np.max(np.abs(r))


def integrals(a, C, x0, xm, X):
    so, si = shoot(a, C, x0, xm, X, quadrature=True)
    Iin = so.y[2:, -1]                 # int_x0^xm
    Iout = -si.y[2:, -1]               # int_xm^X  (integrated from X down to xm)
    # [0, x0] from origin series (Gauss-Legendre 20 pts)
    g, w = np.polynomial.legendre.leggauss(20)
    xs = 0.5*x0*(g + 1); ws = 0.5*x0*w
    I0 = sum(wi*dens(xi, *origin(a, xi)) for xi, wi in zip(xs, ws))
    # [X, inf) from asymptotic series, in y = 1/x
    It = np.zeros(NQ)
    for k in range(NQ):
        f = lambda yy, k=k: dens(1/yy, *asym(C, 1/yy))[k]/yy**2
        It[k] = quad(f, 0.0, 1.0/X, epsabs=1e-16, epsrel=1e-13, limit=200)[0]
    tot = I0 + Iin + Iout + It
    names = ['e2', 'e4', 'Lambda', 'J2', 'D', 'r2B', 'B', 'p']
    d = dict(zip(names, tot))
    d['E2'] = 4*PI*d['e2']; d['E4'] = 4*PI*d['e4']; d['M'] = d['E2'] + d['E4']
    d['tail_Lambda'] = It[2]; d['tail_J2'] = It[3]
    d['_so'] = so; d['_si'] = si
    return d


print('=== two-sided shooting ===')
runs = {}
ref = None
for (x0, xm, X) in [(1e-3, 1.5, 25.0), (1e-3, 2.5, 25.0), (5e-4, 1.0, 40.0), (1e-3, 1.5, 15.0)]:
    v, it, res = solve(x0, xm, X)
    d = integrals(v[0], v[1], x0, xm, X)
    key = 'x0=%g xm=%g X=%g' % (x0, xm, X)
    runs[key] = dict(a=v[0], C=v[1], M=d['M'], Lambda=d['Lambda'], J2=d['J2'], D=d['D'], E2=d['E2'],
                     E4=d['E4'], B=d['B'], r2B=d['r2B'], pint=d['p'], newton_its=it, residual=res)
    print('%-28s a=%.12f C=%.11f M=%.12f Lam=%.10f J2=%.10f D=%.10f B-1=%.1e res=%.1e' %
          (key, v[0], v[1], d['M'], d['Lambda'], d['J2'], d['D'], d['B'] - 1, res))
    if ref is None:
        ref = d; refv = v; refgeom = (x0, xm, X)
spread = {q: max(abs(r[q] - runs[list(runs)[0]][q]) for r in runs.values()) for q in ['M', 'Lambda', 'J2', 'D', 'C', 'a']}
print('spread over 4 geometries:', {k: '%.1e' % v for k, v in spread.items()})

a, C = refv
M, Lam, J2, D = ref['M'], ref['Lambda'], ref['J2'], ref['D']
E2, E4 = ref['E2'], ref['E4']
I1c = 2*PI/3*Lam
I2c = PI/2*J2
print('\nM/(F/e) = %.10f  = %.8f x 3pi^2' % (M, M/(3*PI**2)))
print('Lambda = %.8f  I1 coef = %.6f   J2 = %.8f  I2 coef = %.6f  I1/I2 = %.6f' % (Lam, I1c, J2, I2c, I1c/I2c))
print('C = %.9f   F\'(0) = %.9f   D = %.10f  -2C = %.10f   diff %.1e' % (C, a, D, -2*C, D + 2*C))
print('virial E2/E4-1 = %.2e   int x^2 p dx = %.2e  (expected (E4-E2)/(12 pi) = %.2e)' %
      (E2/E4 - 1, ref['p'], (E4 - E2)/(12*PI)))
print('tails beyond X: Lambda %.6f (C^2/X = %.6f), J2 %.6f' % (ref['tail_Lambda'], C**2/refgeom[2], ref['tail_J2']))

# --- truncation biases (what you'd get without tails / with a Dirichlet box) -----------
Lam_notail = Lam - ref['tail_Lambda']
print('Lambda truncated at X=%g, no tail: %.4f (%.2f%%)' % (refgeom[2], Lam_notail, 100*(Lam_notail/Lam - 1)))


# --- profile comparison with the original's profile.json (outputs only) --------------
def Fof(x):
    x0, xm, X = refgeom
    if x < x0:
        return origin(a, x)
    if x <= xm:
        z = ref['_so'].sol(x); return z[0], z[1]
    if x <= X:
        z = ref['_si'].sol(x); return z[0], z[1]
    return asym(C, x)


xs_tab = np.linspace(0.0, 60.0, 12001)
tab = np.array([Fof(max(xx, 1e-9)) for xx in xs_tab])
np.savez(OUT + 'xc_profile.npz', x=xs_tab, F=tab[:, 0], dF=tab[:, 1], C=C, a=a)
prof = json.load(open('/home/user/gifgaf0.github.io/seed/experiments/E2_skyrme_su3/profile.json'))
xp = np.array(prof['x']); Fp_ = np.array(prof['F']); dFp = np.array(prof['dFdx'])
mine = np.array([Fof(xx) for xx in xp])
dF = np.max(np.abs(mine[:, 0] - Fp_)); dP = np.max(np.abs(mine[:, 1] - dFp))
print('max |F_mine - F_orig| on profile.json grid (0..%g): %.1e ; |F\'| diff %.1e' % (xp[-1], dF, dP))

# --- pressure node -----------------------------------------------------------------
def pres(x):
    F, P = Fof(x)
    return dens(x, F, P)[7]/(x*x)
xnode = brentq(pres, 1.0, 4.0, xtol=1e-12)
p0 = pres(1e-3)
print('pressure: p(0) = %.4f, single node at x = %.5f' % (p0, xnode))
signs = [np.sign(pres(xx)) for xx in np.linspace(0.01, 30, 3000)]
nnodes = int(np.sum(np.abs(np.diff(signs)) > 0))
print('sign changes of p on (0, 30]:', nnodes)

# --- local equilibrium T_rr' + 2 (T_rr - T_tt)/x = 0 at a few points -------------------
def Tcomp(x):
    F, P = Fof(x); s = math.sin(F); lr = P; lt = s/x
    Trr = (1/8)*(lr*lr - 2*lt*lt) + 0.5*lt*lt*(2*lr*lr - lt*lt)
    Ttt = -(1/8)*lr*lr + 0.5*lt**4
    return Trr, Ttt
eq_res = 0.0
for xx in [0.3, 0.8, 1.5, 2.2, 4.0, 8.0]:
    h = 1e-4
    dTrr = (Tcomp(xx + h)[0] - Tcomp(xx - h)[0])/(2*h)
    Trr, Ttt = Tcomp(xx)
    eq_res = max(eq_res, abs(dTrr + 2*(Trr - Ttt)/xx)/max(abs(Trr), 1e-12))
print('local equilibrium residual (relative): %.1e' % eq_res)

# --- arctan ansatz F = 2 arctan(r0^2/x^2) ------------------------------------------------
def ansatz(r0):
    def FP(x):
        u = r0*r0/(x*x)
        return 2*math.atan(u), 2*(-2*r0*r0/x**3)/(1 + u*u)
    def integ(k):
        f = lambda x: dens(x, *FP(x))[k]
        return quad(f, 0, 1, limit=400, epsabs=1e-14, epsrel=1e-13)[0] + \
            quad(lambda yy: f(1/yy)/yy**2, 0, 1, limit=400, epsabs=1e-14, epsrel=1e-13)[0]
    return integ
def Mans(r0):
    ig = ansatz(r0); return 4*PI*(ig(0) + ig(1))
opt = minimize_scalar(Mans, bracket=(1.5, 2.0, 2.5), tol=1e-12)
r0s = opt.x
ig = ansatz(r0s)
J2a = ig(3); Lama = ig(2)
print('arctan ansatz: r0 = %.6f, M = %.6f (exact %.6f, +%.3f%%), Lambda = %.4f, I2 coef = %.5f; exact I2 coef is %+.3f%% from it'
      % (r0s, opt.fun, M, 100*(opt.fun/M - 1), Lama, PI/2*J2a, 100*(I2c/(PI/2*J2a) - 1)))

# --- sigma model (no Skyrme term): radial ODE x^2 F'' + 2x F' - sin 2F = 0 in t = ln x ---
# F_tt + F_t - sin 2F = 0.  Start near F = pi on the unstable manifold: F = pi - eps e^{t}.
sig_end = {}
for eps in [1e-3, 1e-6, 1e-9]:
    t0_ = math.log(eps)  # F = pi - e^{t - t0} ... start at t=t_start with deviation eps
    so = solve_ivp(lambda t, Y: [Y[1], -Y[1] + math.sin(2*Y[0])], (0, 200), [PI - eps, -eps],
                   method='DOP853', rtol=1e-11, atol=1e-13)
    sig_end[str(eps)] = so.y[0, -1]
print('sigma-model radial ODE from F=pi: final F/(pi/2) =', {k: round(v/(PI/2), 9) for k, v in sig_end.items()})
# Derrick scaling of the sigma-model energy: E2[F(mu x)] vs E2/mu
def E2_scaled(mu):
    f = lambda x: dens(x, Fof(mu*x)[0], mu*Fof(mu*x)[1])[0]
    return 4*PI*(quad(f, 0, 1, limit=400, epsabs=1e-13, epsrel=1e-12)[0] +
                 quad(lambda yy: f(1/yy)/yy**2, 0, 1, limit=400, epsabs=1e-13, epsrel=1e-12)[0])
der = {}
for mu in [0.5, 1.0, 2.0, 4.0]:
    der[mu] = E2_scaled(mu)
    print('  mu=%.1f  E2(mu)=%.10f  E2/mu=%.10f' % (mu, der[mu], E2/mu))
der_dev = max(abs(der[mu]*mu/E2 - 1) for mu in der)
# Skyrme-model dilation curve E(mu) = E2/mu + mu E4 minimum
mustar = math.sqrt(E2/E4)

# --- physical numbers -------------------------------------------------------------------
hbarc = 197.3269804
MN, MD = 939.0, 1232.0
invI1 = (MD - MN)/1.5             # E = M + J(J+1)/(2 I1): Delta - N = 3/(2 I1)
Mcl = MN - 0.375*invI1
Fe = Mcl/M                        # F_pi/e in MeV
e3F = invI1*I1c                   # 1/I1 = e^3 F/(I1c)  -> e^3 F = I1c / I1
e = (e3F/Fe)**0.25
Fpi = Fe*e
gA = -(PI/(3*e*e))*D
gA_ball = 2/3*gA
eF = e*Fpi
r_rms = math.sqrt(ref['r2B'])*hbarc/eF
invI2 = e3F/I2c
print('\nANW fit: 1/I1 = %.4f MeV, M_cl = %.4f MeV, F_pi = %.4f MeV, e = %.5f, eF = %.3f MeV' %
      (invI1, Mcl, Fpi, e, eF))
print('g_A = %.5f (= 2 pi C/(3e^2) = %.5f), ball-integral version %.4f; 1/I2 = %.4f MeV, 3/(4I2) = %.3f MeV, r_B = %.4f fm' %
      (gA, 2*PI*C/(3*e*e), gA_ball, invI2, 0.75*invI2, r_rms))

checks = {
    'shooting converged (residual < 1e-12)': all(r['residual'] < 1e-12 for r in runs.values()),
    'geometry spread M < 1e-10': spread['M'] < 1e-10,
    'B = 1 to 1e-10': abs(ref['B'] - 1) < 1e-10,
    'D = -2C to 1e-8': abs(D + 2*C) < 1e-8,
    'virial |E2/E4-1| < 1e-9': abs(E2/E4 - 1) < 1e-9,
    'von Laue = (E4-E2)/(12pi)': abs(ref['p'] - (E4 - E2)/(12*PI)) < 1e-10,
    'Derrick scaling E2(mu)=E2/mu to 1e-9': der_dev < 1e-9,
    'sigma model ends at pi/2': all(abs(v - PI/2) < 1e-8 for v in sig_end.values()),
    'single pressure node': nnodes == 1,
}
for k, v in checks.items():
    print('CHECK %-45s %s' % (k, 'PASS' if v else 'FAIL'))

out = dict(method='two-sided shooting, DOP853 rtol 1e-13, ODE-carried quadrature + analytic tails',
           runs=runs, spread={k: float(v) for k, v in spread.items()},
           C=C, Fprime0=a, M=M, M_over_3pi2=M/(3*PI**2), Lambda=Lam, I1_coef=I1c, J2=J2, I2_coef=I2c,
           I1_over_I2=I1c/I2c, D=D, minus2C=-2*C, E2=E2, E4=E4, virial=E2/E4 - 1,
           vonLaue_int=ref['p'], vonLaue_rel=ref['p']/(E2/(4*PI)), mu_star=mustar,
           r2B=ref['r2B'], B=ref['B'], pressure_node_x=xnode, p0=p0, n_pressure_nodes=nnodes,
           local_equilibrium_resid=eq_res, Lambda_no_tail_X=Lam_notail,
           profile_vs_original=dict(maxdF=dF, maxdFp=dP),
           arctan=dict(r0=r0s, M=opt.fun, Lambda=Lama, I2_coef=PI/2*J2a),
           sigma_model_final_F=sig_end, derrick_E2_mu={str(k): v for k, v in der.items()}, derrick_dev=der_dev,
           ANW=dict(invI1=invI1, Mcl=Mcl, Fpi=Fpi, e=e, eF=eF, gA=gA, gA_ball=gA_ball, invI2=invI2,
                    E8_minus_N=0.75*invI2, r_rms_fm=r_rms, I1_fm=hbarc/invI1, I2_fm=hbarc/invI2),
           checks=checks, all_pass=all(checks.values()), runtime_s=time.time() - t0)
json.dump(out, open(OUT + 'xc_hedgehog.json', 'w'), indent=1, default=float)
print('all checks pass:', all(checks.values()), ' runtime %.1f s' % (time.time() - t0))
