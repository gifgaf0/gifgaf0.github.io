#!/usr/bin/env python3
"""
Cross-check of the O(alpha) quantities from the FLAT profile (computed here with the
spectral solver of xc_iso.py at alpha = 0), plus the physical-scale numbers.

Per unit alpha (alpha = 4 pi G f^2, x = e f r, masses in units 4 pi f/e):
  u      : Lap u = rho, u(inf) = 0     (Newtonian potential Phi = alpha u)
  u_T    : Lap u_T = rho + p_r + 2 p_t (Tolman potential; lapse dA = alpha u_T)
  m1_Newton  = 1/2 int x^2 rho u dx  (= -int x rho m dx)
  m1_GR(iso) = 1/2 int x^2 rho u dx + int x^2 (p_r + 2 p_t) u dx   [first-order expansion of
               M_ADM = int x^2 rho psi^5 dx in isotropic gauge, dF-term vanishes by stationarity]
  m1_GR(Schw)= -int x (rho + p_r) m dx
  d ln A(0)/d alpha = u_T(0)
Deflection (isotropic gauge, gauge invariant at infinity):
  defl(b)/alpha = (2/b) int_0^inf [m(b cosh t) + m_T(b cosh t)] / cosh^2 t dt
Shapiro chord (Schwarzschild-type coordinates, as defined in the original report):
  dt = int_0^X [h00 + hrr] dx,  h00 = 2(1 - sigma) + 2 alpha m/x, hrr = 2 alpha m/x
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xc_iso as X

HERE = os.path.dirname(os.path.abspath(__file__))
res = {}


def flat(N, L):
    g = X.Grid(N, L)
    U, ok = X.newton(X.flat_guess(g), 0.0, g)
    assert ok
    return g, U


def profiles(g, U):
    (Fi, Fx, Fxx), (Pi, Px, Pxx), (Ai, Ax, Axx) = X.pointwise(U, g)[0]
    x = g.x
    args = (x, Fi, Fx, Fxx, Pi, Px, Pxx, Ai, Ax, Axx)
    rho = X.f_rho(*args); pr = X.f_pr(*args); pt = X.f_pt(*args)
    return x, rho, pr, pt


def cumint(g, integrand_x, from_zero=True):
    """antiderivative in x of nodal integrand (interior nodes; ends set to limits 0)."""
    n = g.N + 1
    fx = np.zeros(n)
    fx[1:-1] = integrand_x * g.L / (1 - g.si) ** 2      # d/ds
    D = g.D.copy()
    rhs = fx.copy()
    if from_zero:
        D[0, :] = 0; D[0, 0] = 1; rhs[0] = 0
    else:
        D[-1, :] = 0; D[-1, -1] = 1; rhs[-1] = 0
    return np.linalg.solve(D, rhs)


def quad(g, integrand_x):
    return np.sum(g.wcc[1:-1] * integrand_x * g.L / (1 - g.si) ** 2)


rows = []
for (N, L) in [(80, 1.5), (100, 1.5), (120, 1.0), (120, 2.0)]:
    g, U = flat(N, L)
    x, rho, pr, pt = profiles(g, U)
    tr = pr + 2 * pt
    m = cumint(g, x ** 2 * rho)                       # m(s) at all nodes
    mT = cumint(g, x ** 2 * (rho + tr))
    J = cumint(g, -x * rho, from_zero=False)          # J(s) = int_s^1 x rho dx  (D J = -x rho x_s)
    JT = cumint(g, -x * (rho + tr), from_zero=False)
    Jr = cumint(g, -x * (rho + pr), from_zero=False)  # 1 - sigma per alpha (Schwarzschild, first order)
    mi = m[1:-1]
    u = -mi / x - J[1:-1]
    uT = -mT[1:-1] / x - JT[1:-1]
    m0 = m[-1]
    m1N = 0.5 * quad(g, x ** 2 * rho * u)
    m1N_id = -quad(g, x * rho * mi)
    m1GR_iso = m1N + quad(g, x ** 2 * tr * u)
    m1GR_schw = -quad(g, x * (rho + pr) * mi)
    cross = quad(g, x ** 2 * tr * u)
    uT0 = -JT[0]
    lnsig0 = -Jr[0]
    vonlaue = quad(g, x ** 2 * tr)
    pr_weight = quad(g, x * pr * mi) / quad(g, x * rho * mi)
    r = dict(N=N, L=L, m0=m0, E_flat_f_over_e=4 * np.pi * m0, m1_newton=m1N, m1_newton_identity=m1N_id,
             m1_GR_iso=m1GR_iso, m1_GR_schw=m1GR_schw, cross_trace_term=cross,
             dlnA0_dalpha=uT0, dlnsigma0_dalpha_schw=lnsig0, vonlaue=vonlaue, pr_weight=pr_weight,
             pr0_over_rho0=float(pr[0] / rho[0]))
    rows.append(r)
    print('N=%d L=%.1f m0=%.12f  m1_N=%.9f (id %.9f)  m1_GR_iso=%.9f  m1_GR_schw=%.9f  cross=%.7f  dlnA0=%.7f (schw %.7f)  vonLaue=%.1e  pr-weight=%.6f' % (
        N, L, m0, m1N, m1N_id, m1GR_iso, m1GR_schw, cross, uT0, lnsig0, vonlaue, pr_weight))
res['first_order_rows'] = rows

# ---------------- metric profile, deflection, Shapiro on the finest grid
g, U = flat(120, 1.5)
x, rho, pr, pt = profiles(g, U)
tr = pr + 2 * pt
m = cumint(g, x ** 2 * rho)
mT = cumint(g, x ** 2 * (rho + tr))
Jr = cumint(g, -x * (rho + pr), from_zero=False)
m0 = m[-1]


def interp_x(vals, xq):
    sq = xq / (xq + g.L)
    return g.interp(vals, sq)


xd = np.exp(np.linspace(np.log(1e-3), np.log(200), 20001))
md = interp_x(m, xd)
oneminusN = 2 * md / xd
k = np.argmax(oneminusN)
res['per_alpha'] = dict(oneminusN_max=oneminusN[k], x_at_max=xd[k], oneminus_sigma0=-(-Jr[0]),
                        m0=m0)
# deflection
tt, wt = np.polynomial.legendre.leggauss(400)
T = 30.0
tg = 0.5 * T * (tt + 1); wg = 0.5 * T * wt


def defl(b):
    r = b * np.cosh(tg)
    r = np.minimum(r, 1e12)
    s_ = r / (r + g.L)
    mm = g.interp(m, s_) + g.interp(mT, s_)
    return 2.0 / b * np.sum(wg * mm / np.cosh(tg) ** 2)


bs = np.exp(np.linspace(np.log(0.05), np.log(50), 3001))
dd = np.array([defl(b) for b in bs])
kb = np.argmax(dd)
# refine max
from scipy.optimize import minimize_scalar
opt = minimize_scalar(lambda lb: -defl(np.exp(lb)), bracket=(np.log(bs[kb - 1]), np.log(bs[kb]), np.log(bs[kb + 1])))
bmax = float(np.exp(opt.x)); dmax = -opt.fun
res['per_alpha'].update(deflection_max=dmax, b_at_max=bmax, deflection_b50_over_pointmass=defl(50.0) / (4 * m0 / 50.0))
print('per alpha: max(1-N)=%.6f at x=%.5f; 1-sigma(0)=%.6f; defl max=%.5f at b=%.5f; defl(50)/(4m0/50)=%.7f' % (
    oneminusN[k], xd[k], Jr[0], dmax, bmax, defl(50.0) / (4 * m0 / 50.0)))

# ---------------- physical numbers
Ggev = 6.70883e-39       # G/(hbar c) in GeV^-2
hbarc = 0.1973269804     # GeV fm
c_fm_s = 2.99792458e23   # fm/s
e = 5.45
phys = {}
for f in (0.0645, 0.0922):
    al = 4 * np.pi * Ggev * f ** 2
    ell = hbarc / (e * f)                # fm per x-unit
    x1 = 1.0 / ell
    M = 4 * np.pi * f / e * m0           # GeV
    sig1 = interp_x(Jr, np.array([x1]))[0]
    m1fm = interp_x(m, np.array([x1]))[0]
    # Shapiro chord -1 fm .. +1 fm in Schwarzschild-type coordinates (first order)
    xs = np.linspace(0, x1, 4001)[1:]
    sj = interp_x(Jr, xs); mj = interp_x(m, xs)
    integrand = 2 * sj + 4 * mj / xs      # per alpha, h00 + hrr
    from scipy.integrate import simpson
    chord = simpson(np.concatenate([[2 * Jr[0]], integrand]), x=np.concatenate([[0.0], xs]))
    dt = al * chord * ell / c_fm_s
    GM_c3 = Ggev * M * hbarc / c_fm_s
    # same chord in isotropic coordinates (to show the coordinate dependence)
    uT_ = -interp_x(mT, xs) / xs - interp_x(cumint(g, -x * (rho + tr), from_zero=False), xs)
    u_ = -mj / xs - interp_x(cumint(g, -x * rho, from_zero=False), xs)
    chord_iso = simpson(-(uT_ + u_) * 2, x=xs)   # -(U+V) with U=alpha uT, V = alpha u, both halves
    # deflection at 1 fm and max
    d1 = defl(x1) * al
    phys['f=%.4f' % f] = dict(alpha=al, alpha_over_crit=al / 0.040378525287, M_cl_GeV=M, length_unit_fm=ell, x_at_1fm=x1,
                              oneminusN_max=oneminusN[k] * al, r_at_max_fm=xd[k] * ell, oneminusN_1fm=2 * m1fm / x1 * al,
                              oneminus_sigma0=Jr[0] * al, oneminus_sigma_1fm=sig1 * al, oneminus_gtt0=2 * Jr[0] * al,
                              deflection_max_rad=dmax * al, b_at_max_fm=bmax * ell, deflection_1fm=d1,
                              pointmass_1fm=4 * m0 / x1 * al, GM_over_c3_s=GM_c3, shapiro_chord_schw_s=dt,
                              shapiro_chord_schw_over_GM=dt / GM_c3, shapiro_chord_iso_s=al * chord_iso * ell / c_fm_s)
    print('f=%.4f GeV: alpha=%.5e  M=%.5f GeV  1-N max=%.4e at %.4f fm  1-N(1fm)=%.4e  1-sig0=%.4e  1-sig(1fm)=%.4e  defl max=%.4e at %.4f fm  defl(1fm)=%.4e (pm %.4e)  GM/c3=%.4e s  shapiro(schw)=%.4e s (%.4f GM)  shapiro(iso)=%.4e s' % (
        f, al, M, oneminusN[k] * al, xd[k] * ell, 2 * m1fm / x1 * al, Jr[0] * al, sig1 * al, dmax * al, bmax * ell, d1, 4 * m0 / x1 * al, GM_c3, dt, dt / GM_c3, al * chord_iso * ell / c_fm_s))
res['physical'] = phys
json.dump(res, open(os.path.join(HERE, 'out', 'xc_firstorder.json'), 'w'), indent=1, default=float)
