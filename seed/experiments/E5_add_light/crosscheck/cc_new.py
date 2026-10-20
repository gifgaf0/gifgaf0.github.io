"""E5 cross-check, second pass (new checks added in this pass; independent of the original E5 code).

1. A THIRD hedgehog solver: direct minimisation of the discretised energy functional (finite elements on a
   compactified coordinate, damped Newton with the exact tridiagonal Hessian), Richardson-extrapolated in N.
   Different from both the original (solve_bvp collocation) and the first cross-check pass (shooting).
   EM observables (r_I0, r_M, mu_p, mu_n, g_A, g_piNN) are then formed from this profile with textbook
   integrals; the moment formulas themselves were verified from Noether currents in cc_hedgehog.py.
2. Wess-Zumino normalisation consistency: the A_mu-linear part of the gauged WZ term (Bernstein-Holstein
   eq. 67, coefficient -N_c/48pi^2) integrated over the static hedgehog must give charge N_c/6 (= B/2 at N_c = 3),
   with no isovector part.  The same coefficient fixes the pi0 -> gamma gamma amplitude (cc_pi0.py), so this ties
   the anomaly width to integer baryon charges.
3. Anomaly-consistent quark charges: nucleon-like (Y = N_c/3) charges for N_c = 1..9, Gelfand-Tsetlin.
4. PDG 2026 inputs queried independently (pdg package) and the data-side numbers recomputed
   (isoscalar radii, ratios, the within-30% tally, Gamma(pi0 -> gg)).
5. pi0 width from the textbook amplitude A = N_c alpha/(3 pi f), Gamma = A^2 m^3/(64 pi).
Run: NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 cc_new.py
Writes cc_new.json and cc_new_log.txt.
"""
import json
import os
import sys
import time
import warnings
from fractions import Fraction as Fr

import numpy as np
import sympy as sp
from scipy.linalg import solve_banded

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cc_lib as L   # noqa: E402

HBARC = 197.3269804
LOG = []
OUT = {}
T0 = time.time()


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ============================================================================ 1. variational profile
xs_, F_, D_ = sp.symbols('x F D', real=True)
e_rad = xs_ ** 2 * D_ ** 2 / 8 + sp.sin(F_) ** 2 / 4 + sp.sin(F_) ** 2 * D_ ** 2 + sp.sin(F_) ** 4 / (2 * xs_ ** 2)
fn = {k: sp.lambdify((xs_, F_, D_), v, 'numpy') for k, v in
      {'e': e_rad, 'eF': sp.diff(e_rad, F_), 'eD': sp.diff(e_rad, D_), 'eFF': sp.diff(e_rad, F_, 2),
       'eFD': sp.diff(e_rad, F_, D_), 'eDD': sp.diff(e_rad, D_, 2)}.items()}


def fe_profile(N, s=2.0):
    """nodes u_k = k/N on [0,1], x = s u/(1-u); F(0) = pi, F(inf) = 0; cells use the midpoint rule
    (second order). Returns node x, F and the energy 4 pi int e dx."""
    u = np.linspace(0.0, 1.0, N + 1)
    x = np.empty(N + 1)
    x[:-1] = s * u[:-1] / (1 - u[:-1])
    x[-1] = np.inf
    # cells: work in u with dx = s/(1-u)^2 du; midpoint in u
    um = 0.5 * (u[:-1] + u[1:])
    xm = s * um / (1 - um)
    jac = s / (1 - um) ** 2          # dx/du at the midpoint
    hu = np.diff(u)
    F = 2 * np.arctan((1.4 / np.maximum(x, 1e-100)) ** 2)   # initial guess with the right asymptotics
    F[0] = np.pi; F[-1] = 0.0

    def parts(F):
        Fm = 0.5 * (F[:-1] + F[1:])
        Dm = (F[1:] - F[:-1]) / (hu * jac)     # dF/dx at the midpoint
        return Fm, Dm

    def energy(F):
        Fm, Dm = parts(F)
        return 4 * np.pi * np.sum(fn['e'](xm, Fm, Dm) * jac * hu)

    def grad_hess(F):
        Fm, Dm = parts(F)
        w = jac * hu
        eF, eD = fn['eF'](xm, Fm, Dm), fn['eD'](xm, Fm, Dm)
        eFF, eFD, eDD = fn['eFF'](xm, Fm, Dm), fn['eFD'](xm, Fm, Dm), fn['eDD'](xm, Fm, Dm)
        dd = 1.0 / (hu * jac)
        g = np.zeros(N + 1)
        g[:-1] += w * (0.5 * eF - dd * eD)
        g[1:] += w * (0.5 * eF + dd * eD)
        Hd = np.zeros(N + 1)
        Hd[:-1] += w * (0.25 * eFF - dd * eFD + dd ** 2 * eDD)
        Hd[1:] += w * (0.25 * eFF + dd * eFD + dd ** 2 * eDD)
        Ho = w * (0.25 * eFF - dd ** 2 * eDD)
        return 4 * np.pi * g, 4 * np.pi * Hd, 4 * np.pi * Ho

    # Levenberg-Marquardt-damped Newton: (H + mu diag|H|) step = -g, accept only if the energy decreases
    mu = 1e-2
    E0 = energy(F)
    for it in range(400):
        g, Hd, Ho = grad_hess(F)
        gi = g[1:-1]
        accepted = False
        for _ in range(40):
            ab = np.zeros((3, N - 1))
            ab[0, 1:] = Ho[1:-1]
            ab[1] = Hd[1:-1] + mu * np.abs(Hd[1:-1])
            ab[2, :-1] = Ho[1:-1]
            step = solve_banded((1, 1), ab, -gi)
            Ft = F.copy(); Ft[1:-1] += step
            Et = energy(Ft)
            if np.isfinite(Et) and Et <= E0:
                accepted = True
                break
            mu *= 4.0
        if not accepted:
            break
        F, dE, E0 = Ft, E0 - Et, Et
        mu = max(mu / 4.0, 1e-14)
        if np.max(np.abs(step)) < 1e-12:
            break
    return x, F, energy(F), it, um, xm, jac, hu


def fe_observables(N):
    x, F, E, it, um, xm, jac, hu = fe_profile(N)
    Fm = 0.5 * (F[:-1] + F[1:])
    Dm = (F[1:] - F[:-1]) / (hu * jac)
    s = np.sin(Fm)
    w = jac * hu
    Lam = np.sum(xm ** 2 * s ** 2 * (1 + 4 * (Dm ** 2 + s ** 2 / xm ** 2)) * w)
    B = -(2 / np.pi) * np.sum(s ** 2 * Dm * w)
    R2 = -(2 / np.pi) * np.sum(xm ** 2 * s ** 2 * Dm * w) / B
    # <x^4>_B integrand ~ x^4 * s^2 F' ~ x^4 * C^2/x^4 * 2C/x^3 -> converges as 1/x^2 (fine in u)
    R4 = -(2 / np.pi) * np.sum(xm ** 4 * s ** 2 * Dm * w) / B
    # D-integral of ANW for g_A: D = int x^2 [F' + sin2F/x + 4 (sin^2F/x^2 F' + sin^2F/x^2 sin2F/x ... )]
    # use the surface form instead: g_A = 2 pi C/(3 e^2), C from the tail x^2 F at large x
    sel = (x > 30) & (x < 80) & np.isfinite(x)
    C = np.median(x[sel] ** 2 * F[sel] + (x[sel] ** 2 * F[sel]) ** 3 / (21 * x[sel] ** 4) * 0)  # leading-order C
    # refine with the next tail term F = C/x^2 - C^3/(21 x^6): solve per node
    Cs = []
    for xi, Fi in zip(x[sel], F[sel]):
        c = xi ** 2 * Fi
        for _ in range(5):
            c = xi ** 2 * Fi + c ** 3 / (21 * xi ** 4)
        Cs.append(c)
    C = float(np.median(Cs))
    return {'N': N, 'newton_iters': it, 'M_over_3pi2': E / (3 * np.pi ** 2), 'Lambda': Lam, 'B': B, 'R2': R2,
            'R4': R4, 'C': C, 'Fprime0': (F[1] - F[0]) / (x[1] - x[0])}


def richardson(a, b, p=2):
    return {k: (b[k] * 2 ** p - a[k]) / (2 ** p - 1) if isinstance(a[k], float) else b[k] for k in a}


log('== 1. third hedgehog solver: finite-element energy minimisation (damped Newton) ==')
fe = [fe_observables(N) for N in (4000, 8000, 16000)]
for r in fe:
    log('  ', {k: (round(v, 9) if isinstance(v, float) else v) for k, v in r.items()})
# observed convergence order per quantity from the three meshes, then Richardson with that order
p_obs = {}
for k in fe[0]:
    if isinstance(fe[0][k], float) and k not in ('B',):
        d1, d2 = fe[0][k] - fe[1][k], fe[1][k] - fe[2][k]
        p_obs[k] = float(np.log2(d1 / d2)) if d1 * d2 > 0 and abs(d2) > 1e-14 else 2.0
rich = {k: ((fe[2][k] * 2 ** round(p_obs[k]) - fe[1][k]) / (2 ** round(p_obs[k]) - 1) if k in p_obs else fe[2][k]) for k in fe[2]}
rich_prev = {k: ((fe[1][k] * 2 ** round(p_obs[k]) - fe[0][k]) / (2 ** round(p_obs[k]) - 1) if k in p_obs else fe[1][k]) for k in fe[1]}
log('  observed convergence orders:', {k: round(v, 2) for k, v in p_obs.items()})
log('  Richardson (8000, 16000):', {k: (round(v, 9) if isinstance(v, float) else v) for k, v in rich.items()})
log('  Richardson spread vs (4000, 8000):', {k: f'{abs(rich[k] - rich_prev[k]):.1e}' for k in rich if isinstance(rich[k], float)})
OUT['fe_profile'] = {'runs': fe, 'richardson': rich, 'richardson_prev': rich_prev}

# physical numbers from the FE profile, ANW parameters
Fpi, e = 129.0, 5.45
fm = HBARC / (e * Fpi)
lam = (2 * np.pi / 3) * rich['Lambda'] / (e ** 3 * Fpi)            # MeV^-1
r2_0 = rich['R2'] * fm ** 2 / HBARC ** 2                             # MeV^-2
MN = 939.0
mu_S = 2 * MN * r2_0 / (12 * lam)
mu_V = 2 * MN * lam / 6
gA = 2 * np.pi * rich['C'] / (3 * e ** 2)
phys = {'r_I0_fm': np.sqrt(rich['R2']) * fm, 'rM_ANW_fm': np.sqrt(rich['R4'] / rich['R2']) * fm,
        'rM_Sachs_fm': np.sqrt(0.6 * rich['R4'] / rich['R2']) * fm,
        'mu_p': mu_S + mu_V, 'mu_n': mu_S - mu_V, 'mu_p_over_mu_n': (mu_S + mu_V) / (mu_S - mu_V),
        'g_A': gA, 'g_piNN': 2 * MN * gA / Fpi, 'M_N': Fpi / e * 3 * np.pi ** 2 * rich['M_over_3pi2'] + 3 / (8 * lam),
        'M_Delta': Fpi / e * 3 * np.pi ** 2 * rich['M_over_3pi2'] + 15 / (8 * lam),
        'isovector_slope_C2_over_Lambda': rich['C'] ** 2 / rich['Lambda'],
        'isovector_r2_slope_fm': rich['C'] ** 2 / rich['Lambda'] * fm}
log('  ANW-parameter observables from the FE profile:', {k: round(float(v), 6) for k, v in phys.items()})
OUT['fe_ANW'] = {k: float(v) for k, v in phys.items()}

# ============================================================================ 2. WZ normalisation
log('== 2. gauged-WZ A_mu-linear term (B-H eq. 67) on the static hedgehog ==')
# profile for the integrand: reuse the FE N=8000 profile through interpolation of F and F'
x8, F8, *_ = fe_profile(8000)
fin = np.isfinite(x8)
xg_, Fg_ = x8[fin], F8[fin]


def prof(r):
    Fv = np.interp(r, xg_, Fg_)
    Fpv = np.interp(r, 0.5 * (xg_[1:] + xg_[:-1]), np.diff(Fg_) / np.diff(xg_))
    return Fv, Fpv


xr, wr = np.polynomial.legendre.leggauss(16)
edges = np.concatenate([[0.0], np.geomspace(0.01, 60.0, 70)])
X, W = [], []
for lo, hi in zip(edges[:-1], edges[1:]):
    X.append(0.5 * (hi - lo) * xr + 0.5 * (hi + lo)); W.append(0.5 * (hi - lo) * wr)
X, W = np.concatenate(X), np.concatenate(W)
nS, wS = L.sphere_rule(6, 8)
Na = len(wS)
xv = (X[:, None, None] * nS[None]).reshape(-1, 3)
Wt = (W[:, None] * X[:, None] ** 2 * wS[None]).reshape(-1)
U, dU = L.hedgehog(xv, *prof(np.repeat(X, Na)))
Ud = L.dag(U)
Lf = [dU[:, i] @ Ud for i in range(3)]                 # L_i = d_i U U^+   (B-H convention)
Rf = [L.dag(dU[:, i]) @ U for i in range(3)]           # R_i = d_i U^+ U
EPS = np.zeros((3, 3, 3))
EPS[0, 1, 2] = EPS[1, 2, 0] = EPS[2, 0, 1] = 1
EPS[0, 2, 1] = EPS[2, 1, 0] = EPS[1, 0, 2] = -1
res_wz = {}
for name, Qm in (('isoscalar 1/6', np.eye(2) / 6), ('isovector tau3/2', L.TAU[2] / 2),
                 ('Q = diag(2/3,-1/3)', np.diag([2 / 3, -1 / 3]).astype(complex))):
    acc = np.zeros(len(Wt), dtype=complex)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if EPS[i, j, k] != 0:
                    acc += EPS[i, j, k] * L.tr(Qm[None] @ (Lf[i] @ Lf[j] @ Lf[k] - Rf[i] @ Rf[j] @ Rf[k]))
    J0 = -(1.0 / (48 * np.pi ** 2)) * acc.real            # per unit N_c (eps^{0ijk} = eps_ijk)
    res_wz[name] = float(np.sum(Wt * J0))
log('  int J^0_WZ d^3x per unit N_c:', res_wz, ' expected magnitude 1/6 = 0.1666667 for the isoscalar part, 0 isovector')
OUT['WZ_charge_per_Nc'] = res_wz

# ============================================================================ 3. anomaly-consistent charges
log('== 3. charges with anomaly-consistent quark charges (Gelfand-Tsetlin) ==')


def gt_states(p, q):
    out = []
    for m12 in range(q, p + q + 1):
        for m22 in range(0, q + 1):
            for m11 in range(m22, m12 + 1):
                I3 = Fr(m11) - Fr(m12 + m22, 2)
                Y = Fr(m12 + m22) - Fr(2, 3) * (p + 2 * q)
                out.append((Fr(m12 - m22, 2), I3, Y))
    return out


rows3 = []
for Nc in (1, 3, 5, 7, 9):
    # lowest irrep containing Y = N_c/3 with J = 1/2 is (1, (N_c-1)/2)
    p, q = 1, (Nc - 1) // 2
    st = gt_states(p, q)
    qu, qd = Fr(1, 2) + Fr(1, 2 * Nc), -Fr(1, 2) + Fr(1, 2 * Nc)
    # Q = (qu - qd)(I3 + Y/2) + [(qu - qd)/3 + qd] * (quark number = N_c B)
    ident = (qu - qd) / 3 + qd
    Qcons = sorted({s[1] + s[2] / 2 + ident * Nc for s in st if s[2] == Fr(Nc, 3)})
    Qfix = sorted({s[1] + s[2] / 2 for s in st if s[2] == Fr(Nc, 3)})
    rows3.append({'N_c': Nc, 'irrep': (p, q), 'Q_fixed': [str(v) for v in Qfix], 'Q_consistent': [str(v) for v in Qcons],
                  'TrQ^2tau3_times_Nc_consistent': str(Nc * (qu ** 2 - qd ** 2))})
    log(f'  N_c={Nc}: irrep {(p, q)}  fixed-charge Q {[str(v) for v in Qfix]}  anomaly-consistent Q {[str(v) for v in Qcons]}'
        f'  N_c(qu^2-qd^2) = {Nc * (qu ** 2 - qd ** 2)}')
OUT['charges_Nc'] = rows3

# ============================================================================ 4. PDG 2026 inputs, data side
log('== 4. PDG 2026 inputs (independent query) and data-side numbers ==')
warnings.filterwarnings('ignore')
try:
    import pdg
    api = pdg.connect()

    def get(pid):
        b = api.get(pid).best_summary()
        return float(b.value), (float(b.error) if b.error is not None else float('nan'))
    pd = {k: get(v) for k, v in {'mu_p': 'S016MM', 'mu_n': 'S017MM', 'r_p': 'S016CR', 'r2_n': 'S017MCR',
                                 'rM_p': 'S016MCR', 'rM_n': 'S017MRD', 'gA': 'S017AV', 'm_pi0': 'S009M',
                                 'tau_pi0': 'S009T'}.items()}
    bf = [b for b in api.get_particle_by_name('pi0').exclusive_branching_fractions() if '2gamma' in b.description][0]
    pd['BR_gg'] = (float(bf.value), float(bf.error))
    src = 'pdg package'
except Exception as ex:  # pragma: no cover
    pd, src = {}, f'failed: {ex}'
log('  ', src, {k: v for k, v in pd.items()})
data = {}
if pd:
    data['rE_I0_fm'] = np.sqrt(pd['r_p'][0] ** 2 + pd['r2_n'][0])
    mp, mn = pd['mu_p'][0], pd['mu_n'][0]
    rM2 = (mp * pd['rM_p'][0] ** 2 + mn * pd['rM_n'][0] ** 2) / (mp + mn)
    data['rM_I0_fm'] = np.sqrt(rM2)
    data['rM_I0_err_from_rMp_only'] = (2 * pd['rM_p'][0] * mp / (mp + mn)) * pd['rM_p'][1] / (2 * np.sqrt(rM2))
    data['r_V_fm'] = np.sqrt(pd['r_p'][0] ** 2 - pd['r2_n'][0])
    data['mu_p_over_mu_n'] = mp / mn
    hbar_eVs = 6.582119569e-16
    data['Gamma_gg_eV'] = hbar_eVs / pd['tau_pi0'][0] * pd['BR_gg'][0]
    data['Gamma_gg_err_eV'] = data['Gamma_gg_eV'] * np.hypot(pd['tau_pi0'][1] / pd['tau_pi0'][0], pd['BR_gg'][1] / pd['BR_gg'][0])
    model = {'mu_p': phys['mu_p'], 'mu_n': phys['mu_n'], 'mu_p_over_mu_n': phys['mu_p_over_mu_n'], 'g_A': phys['g_A'],
             'g_piNN': phys['g_piNN'], 'rE_I0': phys['r_I0_fm'], 'rM_I0_Sachs': phys['rM_Sachs_fm']}
    dval = {'mu_p': mp, 'mu_n': mn, 'mu_p_over_mu_n': mp / mn, 'g_A': abs(pd['gA'][0]), 'g_piNN': 13.1,
            'rE_I0': data['rE_I0_fm'], 'rM_I0_Sachs': data['rM_I0_fm']}
    tally = {k: model[k] / dval[k] - 1 for k in model}
    data['deviation'] = tally
    data['n_within_30'] = int(sum(abs(v) <= 0.30 for v in tally.values()))
    data['n_within_33'] = int(sum(abs(v) <= 0.33 for v in tally.values()))
    data['n_within_35'] = int(sum(abs(v) <= 0.35 for v in tally.values()))
    # f_pi itself as a prediction of the ANW fit (not in the original's tally): 64.5 vs 92.21 MeV
    data['f_pi_fold_over_phys_ANW'] = 64.5 / 92.21
    log('  data-side:', {k: (round(float(v), 5) if not isinstance(v, dict) else {kk: round(float(vv), 4) for kk, vv in v.items()})
                         for k, v in data.items()})
OUT['pdg'] = {k: list(v) for k, v in pd.items()}
OUT['data_side'] = {k: (float(v) if not isinstance(v, dict) else {kk: float(vv) for kk, vv in v.items()}) for k, v in data.items()}

# ============================================================================ 5. pi0 width, textbook amplitude
alpha = 1 / 137.035999177
m = pd['m_pi0'][0] if pd else 134.9768


def width(f, Nc=3):
    A = Nc * alpha / (3 * np.pi * f)          # MeV^-1, M = A eps(k1,e1,k2,e2)
    return A ** 2 * m ** 3 / (64 * np.pi) * 1e6   # eV


pi0 = {'Nc3_f92.21': width(92.21), 'Nc1_f92.21': width(92.21, 1), 'f64.5': width(64.5),
       'f56.877': width(56.877), 'f_for_PrimExII': 92.21 * np.sqrt(width(92.21) / 7.802)}
pi0['pull_PrimExII'] = (pi0['Nc3_f92.21'] - 7.802) / 0.117
pi0['pull_Nc1'] = (pi0['Nc1_f92.21'] - 7.802) / 0.117
if pd:
    pi0['pull_PDG'] = (pi0['Nc3_f92.21'] - data['Gamma_gg_eV']) / data['Gamma_gg_err_eV']
log('== 5. pi0 width from A = N_c alpha/(3 pi f) ==', {k: round(v, 5) for k, v in pi0.items()})
OUT['pi0_textbook'] = pi0

OUT['runtime_s'] = time.time() - T0
log(f'done in {time.time() - T0:.1f} s')
json.dump(OUT, open(os.path.join(HERE, 'cc_new.json'), 'w'), indent=1, default=str)
open(os.path.join(HERE, 'cc_new_log.txt'), 'w').write('\n'.join(LOG) + '\n')
