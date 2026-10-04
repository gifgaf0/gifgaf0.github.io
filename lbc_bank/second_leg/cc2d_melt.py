#!/usr/bin/env python3
"""cc2d_melt -- Q-C, approach to melting of the 2D step-kernel crystal (second leg; numpy/scipy only).

Built on the 2D instrument cc2d.py of this leg (plane-wave Galerkin, Newton-Krylov ground states, Cholesky BdG).
Units hbar = m = R = 1, mean density 1, step kernel Uhat(k) = 2 pi g J1(k)/k.

Definitions (dispatch Sec. 3 / spec Sec. 5)
  a*        root of the envelope-theorem derivative de/da (e = E_cell/A at fixed density) with d2e/da2 > 0, i.e. the
            local minimum of e(a) followed continuously from g = 16 (fresh ground state at every a, seeded from the
            nearest already solved a; downhill walk in a until de/da changes sign, then Brent on de/da).
  eps_c     E_cell/N_cell at a*;  mu_c = GP eigenvalue at a*;  P_c = mu_c - eps_c;  P_u = mu_c^2/(2 pi g)
  f(g)      g (mu_c - eps_c) - mu_c^2/(2 pi)      -> Lambda_c = root, Lambda_u = mu_c(Lambda_c)/pi
  h(g)      eps_c - pi g/2                         -> energy crossing = root
  branch end: lowest g at which the a*-optimised crystal is still a local minimum.  Criteria ('lost'):
            (i) the seeded ground state collapses to the uniform state, (ii) no local minimum of e(a) is found by
            the downhill walk inside the window (a-curvature criterion: the minimum has merged with the maximum of
            e(a)), (iii) the constrained Hessian at fixed cell restricted to the fully symmetric (C6v, Gamma) sector
            has a negative eigenvalue, (iv) d2e/da2 < 0 at the found root.
            Independent locator: the fold of the a*-branch is where the extremum of de/da between the minimum and the
            maximum of e(a) reaches zero: G(g) = extremum_a de/da (g) = 0 (Brent in g, bounded Brent in a).
  BdG       cc2d.speeds along a1, |q|a/2pi in {0.03, 0.05, 0.075, 0.10}, LSQ speeds through the origin, F2 at 0.05.
            Dynamical stability: Cholesky of A(q) at those q (cc2d.bdg 'unstable'), plus min eig A(q) on a BZ grid.

Subcommands (each step caches to WORK/qc and is resumable):
  python3 cc2d_melt.py branch      continuation g = 16, 15.75, ... (0.25) until lost, then 0.05 steps, then bisection
  python3 cc2d_melt.py grid        extra points every 0.05 in [12.5, 13.0]
  python3 cc2d_melt.py up          a* states above 16 (sign checks of f and h; BdG for the boolean)
  python3 cc2d_melt.py roots       Lambda_c and energy crossing (Brent, fresh a*-optimised solve per evaluation)
  python3 cc2d_melt.py fold        fold locator G(g) = 0 and e(a) scans around the end
  python3 cc2d_melt.py ratiomax    maximum of c2/cT along the metastable continuation (bounded Brent in g)
  python3 cc2d_melt.py dyn         onset of the BdG instability (imaginary omega) at each Q-A q (bisection in g)
  python3 cc2d_melt.py bdg [max]   BdG (Kcut 80) for every cached state lacking it
  python3 cc2d_melt.py conv        N / Kcut convergence at Lambda_c and at the last state before the end
  python3 cc2d_melt.py collect     write qc_results.json
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '2')
import sys
import json
import time
import math
import numpy as np
import scipy.linalg as sla
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cc2d  # noqa: E402

WORK = cc2d.WORK
QC = os.path.join(WORK, 'qc')
os.makedirs(QC, exist_ok=True)
N = 64
KCUT = 80.0
FRACS = (0.03, 0.05, 0.075, 0.10)
GS_TOL = 1e-12
PI = math.pi
PTS_JSON = os.path.join(QC, 'points.json')
ROOTS_JSON = os.path.join(QC, 'roots.json')
FOLD_JSON = os.path.join(QC, 'fold.json')
CONV_JSON = os.path.join(QC, 'conv.json')
LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)


def gkey(g):
    return repr(float(g))


# ----------------------------------------------------------------------------------------------------------
# persistence
# ----------------------------------------------------------------------------------------------------------
def load_points():
    if os.path.exists(PTS_JSON):
        with open(PTS_JSON) as f:
            return json.load(f)
    return {}


def save_points(P):
    tmp = PTS_JSON + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(cc2d.jsonable(P), f, indent=1)
    os.replace(tmp, PTS_JSON)


def state_path(g):
    return os.path.join(QC, 'st_%s.npz' % gkey(g))


def save_state(g, st):
    cc2d.save_states(state_path(g), {'st': st})


def load_state_g(g):
    p = state_path(g)
    if not os.path.exists(p):
        return None
    d = cc2d.load_state(p, 'st')
    return cc2d.state_from_saved(d, tol=GS_TOL)


def json_load(p, default):
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return default


def _finite(o):
    if isinstance(o, dict):
        return {k: _finite(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_finite(v) for v in o]
    if isinstance(o, float) and not math.isfinite(o):
        return None
    return o


def json_save(obj, p):
    tmp = p + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(_finite(cc2d.jsonable(obj)), f, indent=1, allow_nan=False)
    os.replace(tmp, p)


# ----------------------------------------------------------------------------------------------------------
# fixed-cell solves and the a* search
# ----------------------------------------------------------------------------------------------------------
class Lost(Exception):
    def __init__(self, why, detail=None):
        super().__init__(why)
        self.why = why
        self.detail = detail or {}


PCG_BREAKDOWNS = []   # cc2d.pcg raises ZeroDivisionError when rz underflows to 0 (near-singular Hessian); see notes


def solve_fixed(kern, a, seed):
    st = None
    for tol in (GS_TOL, 1e-11):
        try:
            st = cc2d.ground_state(cc2d.hex_cell(a), kern, N, 1.0, seed=seed, tol=tol)
            break
        except ZeroDivisionError:
            PCG_BREAKDOWNS.append({'g': kern.g, 'a': float(a), 'tol': tol})
            log('   cc2d.pcg breakdown (ZeroDivisionError) at g=%r a=%r tol=%g' % (kern.g, a, tol))
    if st is None:
        return None, False
    ok = (not st.uniform) and bool(st.info.get('newton', {}).get('converged', False))
    return st, ok


def astar_search(kern, a_guess, seed, window=0.04, step0=2e-3, xtol_rel=1e-14):
    """local minimum of e(a) reached by a downhill walk from a_guess; returns dict or raises Lost."""
    cache = {}
    order = []
    seed_contrast = seed.contrast if isinstance(seed, cc2d.State) else None

    def ev(a):
        a = float(a)
        if a in cache:
            return cache[a]
        if cache:
            ak = min(cache, key=lambda x: abs(x - a) if cache[x][2] else 1e9)
            sd = cache[ak][0] if cache[ak][2] else seed
        else:
            sd = seed
        st, ok = solve_fixed(kern, a, sd)
        D = cc2d.dedA_envelope(st) if ok else float('nan')
        cache[a] = (st, D, ok)
        if st is None:
            order.append({'a': a, 'dedA': D, 'ok': False, 'pcg_breakdown': True})
        else:
            order.append({'a': a, 'dedA': D, 'ok': ok, 'uniform': st.uniform, 'contrast': st.contrast,
                          'resid': st.resid, 'e': st.e})
        return cache[a]

    a0 = float(a_guess)
    a_seed = float(np.linalg.norm(seed.cell[0])) if isinstance(seed, cc2d.State) else a0
    # the guess may fall outside the (narrow, near the end) interval of a in which the crystal exists at fixed
    # cell: fall back to the seed's own a and then to smaller a (the interval extends far below a*)
    cands = [a0, a_seed] + [a_seed * (1.0 - x) for x in (2e-4, 5e-4, 1e-3, 2e-3, 4e-3)]
    ok0 = False
    for ac in cands:
        st0, D0, ok0 = ev(ac)
        if ok0:
            a0 = float(ac)
            break
    if not ok0:
        raise Lost('seeded solve collapsed to uniform at the guess, at the seed a and at 5 smaller a',
                   {'a_guess': a0, 'walk': order})
    # curvature estimate for a Newton-sized first step
    dl = 1e-4 * a0
    _, D1, ok1 = ev(a0 + dl)
    if not ok1:
        dl = -dl
        _, D1, ok1 = ev(a0 + dl)
    k0 = (D1 - D0) / dl if ok1 else float('nan')
    direction = -1.0 if D0 > 0 else 1.0
    if ok1 and k0 > 0:
        step = min(max(1.3 * abs(D0) / k0, 1e-5 * a0), step0 * a0 * 5)
    else:
        step = step0 * a0
    a, D = a0, D0
    bracket = None
    for it in range(200):
        an = a + direction * step
        if abs(an - a0) > window * a0:
            raise Lost('no local minimum of e(a) within the window (downhill walk reached the window edge)',
                       {'a_guess': a0, 'walk': order, 'window': window})
        stn, Dn, okn = ev(an)
        if not okn:
            step *= 0.25
            if step < 1e-9 * a0:
                raise Lost('no local minimum of e(a) before the crystal ceases to exist at fixed cell '
                           '(downhill walk ends at collapse to uniform)', {'a_guess': a0, 'walk': order,
                                                                            'a_edge': a})
            continue
        if np.sign(Dn) != np.sign(D):
            bracket = (min(a, an), max(a, an))
            break
        # accelerate: secant-based estimate if the slope is positive along the walk
        kk = (Dn - D) / (an - a)
        a, D = an, Dn
        if kk > 0:
            step = min(max(1.3 * abs(D) / kk, 1e-6 * a0), 4 * step)
        else:
            step = min(2.0 * step, 0.01 * a0)
    if bracket is None:
        raise Lost('walk did not bracket', {'walk': order})

    def fD(x):
        s, d, okk = ev(x)
        if not okk:
            raise Lost('collapse inside the bracket', {'walk': order})
        return d
    ar = brentq(fD, bracket[0], bracket[1], xtol=xtol_rel * bracket[0], rtol=1e-15, maxiter=200)
    st, Dr, okr = ev(ar)
    # curvature by central differences: largest h (from 1e-4 a* down) with a* +- 2h inside the existence interval,
    # steps 2h and h, Richardson
    hrel = 1e-4
    d2c = d2f = float('nan')
    while hrel > 1e-8:
        h = hrel * ar
        okall = all(ev(ar + s * h)[2] for s in (2.0, -2.0, 1.0, -1.0))
        if okall:
            d2c = (ev(ar + 2 * h)[1] - ev(ar - 2 * h)[1]) / (4 * h)
            d2f = (ev(ar + h)[1] - ev(ar - h)[1]) / (2 * h)
            break
        hrel *= 0.5
    d2 = (4 * d2f - d2c) / 3.0
    return {'astar': float(ar), 'state': st, 'dedA_at_astar': float(Dr), 'd2e_da2': float(d2),
            'd2e_da2_coarse': float(d2c), 'd2e_da2_fine': float(d2f), 'd2e_fd_hrel': float(hrel),
            'bracket_a': list(bracket), 'n_solves': len(cache), 'walk': order,
            'seed_contrast': seed_contrast}


# ----------------------------------------------------------------------------------------------------------
# Hessian checks at fixed cell
# ----------------------------------------------------------------------------------------------------------
def sym_sector_hessian(st, nev=4):
    """constrained Hessian (A = L + 2X on real perturbations orthogonal to psi0) restricted to the fully symmetric
    (point-group invariant) subspace of the ground-state basis.  Returns the lowest eigenvalues."""
    g = st.grid
    ctx = st.ctx
    perms = g.perms()
    nm = g.nm
    oid = -np.ones(nm, dtype=int)
    orbits = []
    for i in range(nm):
        if oid[i] >= 0:
            continue
        mem = np.unique(np.array([p[i] for p in perms]))
        oid[mem] = len(orbits)
        orbits.append(mem)
    no = len(orbits)
    B = np.zeros((nm, no))
    for k, mem in enumerate(orbits):
        B[mem, k] = 1.0 / math.sqrt(len(mem))
    c = st.c
    pc = B.T @ c.real
    sym_err = float(np.linalg.norm(B @ pc - c) / np.linalg.norm(c))
    H = np.empty((no, no))
    imag_max = 0.0
    for k in range(no):
        hk = ctx.hess(B[:, k].astype(complex))
        imag_max = max(imag_max, float(np.max(np.abs(hk.imag))))
        H[:, k] = B.T @ hk.real
    asym = float(np.max(np.abs(H - H.T)) / np.max(np.abs(H)))
    H = 0.5 * (H + H.T)
    Q = sla.null_space(pc[None, :])
    Hc = Q.T @ H @ Q
    ev = sla.eigvalsh(Hc)
    ev_un = sla.eigvalsh(H)
    return {'n_orbits': no, 'n_group': len(perms), 'psi_sym_err': sym_err, 'H_asym': asym,
            'hess_imag_max': imag_max, 'lowest_constrained': [float(x) for x in ev[:nev]],
            'lowest_unconstrained': [float(x) for x in ev_un[:nev]]}


def gamma_full_hessian(st, Kcut=60.0, nev=4):
    """constrained Hessian in the whole Gamma (q = 0) sector: A on the complement of {psi0, d_x psi0, d_y psi0}
    (the BdG plane-wave basis |G| < Kcut); returns the lowest eigenvalues (all irreps)."""
    mats = cc2d.bdg_matrices(st, np.zeros(2), Kcut)
    L, X, s = mats['L'], mats['X'], mats['s']
    A = L + 2.0 * X
    dx = 1j * mats['gx'] * s
    dy = 1j * mats['gy'] * s
    V = np.stack([s, dx, dy], axis=0).astype(complex)
    Q = sla.null_space(V.conj())
    Ac = Q.conj().T @ A @ Q
    Ac = 0.5 * (Ac + Ac.conj().T)
    ev = sla.eigvalsh(Ac)
    eL = sla.eigvalsh(L)
    return {'Kcut': Kcut, 'nbasis': int(L.shape[0]), 'A_lowest_constrained': [float(x) for x in ev[:nev]],
            'L_lowest': [float(x) for x in eL[:3]]}


def bz_scan(st, Kcut=50.0, nq=6):
    return cc2d.stability_scan(st, Kcut, nq)


# ----------------------------------------------------------------------------------------------------------
# one branch point
# ----------------------------------------------------------------------------------------------------------
def point_record(g, o, extra_checks=True):
    st = o['state']
    mu, eps = st.mu, st.eps
    rec = {'g': float(g), 'astar': o['astar'], 'eps_c': eps, 'mu_c': mu, 'e_per_area': st.e, 'E_cell': st.E,
           'contrast': st.contrast, 'rho_max': st.rho_max, 'rho_min': st.rho_min, 'modulation': st.modulation,
           'gs_resid': st.resid, 'P_c': mu - eps, 'P_u_at_mu_c': mu * mu / (2 * PI * g),
           'f': g * (mu - eps) - mu * mu / (2 * PI), 'eps_minus_pi_g_half': eps - PI * g / 2.0,
           'dedA_at_astar': o['dedA_at_astar'], 'd2e_da2': o['d2e_da2'],
           'd2e_da2_coarse': o['d2e_da2_coarse'], 'd2e_da2_fine': o['d2e_da2_fine'], 'd2e_fd_hrel': o['d2e_fd_hrel'],
           'bracket_a': o['bracket_a'], 'n_solves': o['n_solves']}
    if extra_checks:
        t = time.time()
        rec['sym_hessian'] = sym_sector_hessian(st)
        rec['gamma_hessian'] = gamma_full_hessian(st)
        rec['bz_scan'] = bz_scan(st)
        rec['t_checks'] = time.time() - t
    lost = []
    if extra_checks and rec['sym_hessian']['lowest_constrained'][0] < 0:
        lost.append('symmetric-sector Hessian at fixed cell negative')
    if not (o['d2e_da2'] > 0):
        lost.append('a-curvature d2e/da2 <= 0')
    rec['lost_criteria'] = lost
    return rec


def nearest_seed(P, g, prefer_above=True):
    """the cached good state closest in g (from above if available) + a linear extrapolation of a*."""
    good = [(float(k), v) for k, v in P.items() if v.get('status') == 'ok']
    if not good:
        return None, None
    if prefer_above:
        above = [x for x in good if x[0] > g]
        cand = above if above else good
    else:
        cand = good
    cand.sort(key=lambda x: abs(x[0] - g))
    g1, r1 = cand[0]
    a_guess = r1['astar']
    if len(cand) > 1:
        g2, r2 = cand[1]
        if abs(g2 - g1) > 1e-12:
            a_guess = r1['astar'] + (r2['astar'] - r1['astar']) / (g2 - g1) * (g - g1)
            if abs(a_guess - r1['astar']) > 0.01 * r1['astar']:
                a_guess = r1['astar']
    st = load_state_g(g1)
    return st, a_guess


def run_g(P, g, seed_state=None, a_guess=None, checks=True, tag='branch'):
    k = gkey(g)
    if k in P and P[k].get('status') in ('ok', 'lost'):
        return P[k]
    t0 = time.time()
    if seed_state is None:
        seed_state, a_guess = nearest_seed(P, g)
    kern = cc2d.Kernel('step', g)
    try:
        o = astar_search(kern, a_guess, seed_state)
        rec = point_record(g, o, checks)
        rec['status'] = 'ok' if not rec['lost_criteria'] else 'lost'
        rec['a_guess'] = a_guess
        if rec['status'] == 'ok':
            save_state(g, o['state'])
    except Lost as ex:
        rec = {'g': float(g), 'status': 'lost', 'lost_criteria': [ex.why], 'a_guess': a_guess,
               'walk': ex.detail.get('walk'), 'a_edge': ex.detail.get('a_edge')}
    rec['tag'] = tag
    rec['time'] = time.time() - t0
    rec['pcg_breakdowns_so_far_in_process'] = len(PCG_BREAKDOWNS)
    P[k] = rec
    save_points(P)
    if rec['status'] == 'ok':
        log('g=%r ok a*=%r eps=%r mu=%r f=%r h=%r d2e=%r lam_sym=%r t=%.1f' % (
            g, rec['astar'], rec['eps_c'], rec['mu_c'], rec['f'], rec['eps_minus_pi_g_half'], rec['d2e_da2'],
            rec.get('sym_hessian', {}).get('lowest_constrained', [None])[0], rec['time']))
    else:
        log('g=%r LOST %s' % (g, rec['lost_criteria']))
    return rec


# ----------------------------------------------------------------------------------------------------------
# steps
# ----------------------------------------------------------------------------------------------------------
def initial_seed():
    d = cc2d.load_state(os.path.join(WORK, 'qa_states.npz'), 'step_g16_aroot')
    st = cc2d.state_from_saved(d, tol=GS_TOL)
    return st, float(np.linalg.norm(st.cell[0]))


def cmd_branch(args):
    P = load_points()
    if gkey(16.0) not in P:
        st, a = initial_seed()
        run_g(P, 16.0, st, a)
    # coarse 0.25 steps
    g = 16.0
    last_ok = 16.0
    first_lost = None
    while g > 5.0:
        g = round(g - 0.25, 10)
        r = run_g(P, g)
        if r['status'] != 'ok':
            first_lost = g
            break
        last_ok = g
    log('coarse: last ok', last_ok, 'first lost', first_lost)
    # 0.05 steps
    g = last_ok
    while True:
        g = round(g - 0.05, 10)
        if first_lost is not None and g <= first_lost + 1e-12:
            break
        r = run_g(P, g)
        if r['status'] != 'ok':
            first_lost = g
            break
        last_ok = g
    log('fine: last ok', last_ok, 'first lost', first_lost)
    last_ok_fine, first_lost_fine = last_ok, first_lost
    # bisection
    if first_lost is None:
        log('no loss found down to g = 5')
        return
    lo, hi = first_lost, last_ok
    hist = [[lo, hi]]
    tol_b = float(args[0]) if args else 1e-7
    while hi - lo > tol_b:
        mid = 0.5 * (lo + hi)
        r = run_g(P, mid, tag='bisect')
        if r['status'] == 'ok':
            hi = mid
        else:
            lo = mid
        hist.append([lo, hi])
        log('bisect bracket', lo, hi)
    br = json_load(FOLD_JSON, {})
    br['bisection_bracket'] = [lo, hi]
    br['bisection_history'] = hist
    br['bisection_bracket_first_le_0.005'] = next(x for x in hist if x[1] - x[0] <= 0.005)
    br['continuation_last_ok_0.05'] = last_ok_fine
    br['continuation_first_lost_0.05'] = first_lost_fine
    json_save(br, FOLD_JSON)


def cmd_up(args):
    P = load_points()
    gs = [16.5, 17.0, 18.0, 19.0, 20.0, 22.0, 25.0, 28.0, 32.0, 36.0, 40.0, 44.0]
    for g in gs:
        run_g(P, g, tag='up')


def cmd_grid(args):
    """extra branch points every 0.05 between 13.0 and 12.5 (continuation from above)."""
    P = load_points()
    for g in np.round(np.arange(12.95, 12.501, -0.05), 10):
        run_g(P, float(g), tag='grid005')


def eval_fresh(g, P):
    """fresh a*-optimised solve at g (seeded from the nearest cached state); returns record (not cached in P)."""
    st, a_guess = nearest_seed(P, g, prefer_above=False)
    kern = cc2d.Kernel('step', g)
    o = astar_search(kern, a_guess, st)
    return o


def cmd_roots(args):
    P = load_points()
    R = json_load(ROOTS_JSON, {})
    good = sorted([(float(k), v) for k, v in P.items() if v.get('status') == 'ok'])
    for name, fld in (('Lambda_c', 'f'), ('energy_crossing', 'eps_minus_pi_g_half')):
        if name in R and R[name].get('done'):
            continue
        br = None
        for (g1, r1), (g2, r2) in zip(good[:-1], good[1:]):
            if np.sign(r1[fld]) != np.sign(r2[fld]):
                br = (g1, g2, r1[fld], r2[fld])
        if br is None:
            R[name] = {'done': True, 'root': None, 'note': 'no sign change on the computed branch'}
            continue
        evals = []

        def F(g):
            o = eval_fresh(g, P)
            st = o['state']
            val = g * (st.mu - st.eps) - st.mu ** 2 / (2 * PI) if fld == 'f' else st.eps - PI * g / 2.0
            evals.append({'g': g, 'value': val, 'astar': o['astar'], 'mu_c': st.mu, 'eps_c': st.eps})
            log(name, 'g=%r val=%r a*=%r' % (g, val, o['astar']))
            return val
        root = brentq(F, br[0], br[1], xtol=1e-9, rtol=1e-15, maxiter=100)
        o = eval_fresh(root, P)
        st = o['state']
        rec = {'done': True, 'root': float(root), 'branch_bracket': [br[0], br[1]],
               'branch_bracket_values': [br[2], br[3]], 'brent_xtol': 1e-9, 'evals': evals,
               'astar': o['astar'], 'mu_c': st.mu, 'eps_c': st.eps, 'd2e_da2': o['d2e_da2'],
               'contrast': st.contrast, 'f': root * (st.mu - st.eps) - st.mu ** 2 / (2 * PI),
               'eps_minus_pi_g_half': st.eps - PI * root / 2.0}
        # final bracket from the Brent evaluations
        below = [e for e in evals if e['g'] < root]
        above = [e for e in evals if e['g'] > root]
        if below and above:
            eb = max(below, key=lambda e: e['g'])
            ea = min(above, key=lambda e: e['g'])
            rec['final_bracket'] = [eb['g'], ea['g']]
            rec['final_bracket_values'] = [eb['value'], ea['value']]
            rec['final_bracket_width'] = ea['g'] - eb['g']
        if name == 'Lambda_c':
            rec['Lambda_u'] = st.mu / PI
        # cache the state at the root and insert it as a branch point
        save_state(root, st)
        P[gkey(root)] = dict(point_record(root, o, True), status='ok', tag=name)
        save_points(P)
        R[name] = rec
        json_save(R, ROOTS_JSON)


def bdg_record(st):
    t = time.time()
    sp = cc2d.speeds(st, 0.0, FRACS, KCUT)
    b = {'Kcut': KCUT, 'fracs': list(FRACS), 'unstable': bool(sp.get('unstable', False))}
    b['per_q'] = [{'frac': r['frac'], 'qabs': r['qabs'], 'unstable': r['unstable'], 'min_omega2': r['min_omega2'],
                   'n_negative_omega2': r.get('n_negative_omega2'),
                   'fsum_resid': r.get('fsum_resid'), 'static_resid': r.get('static_resid'),
                   'omega_T': r.get('T', {}).get('omega'), 'omega_2': r.get('2', {}).get('omega'),
                   'omega_1': r.get('1', {}).get('omega'), 'F2': r.get('2', {}).get('F'),
                   'Z2': r.get('2', {}).get('Z'), 'Z1': r.get('1', {}).get('Z'), 'S2': r.get('2', {}).get('S'),
                   'FT': r.get('T', {}).get('F'), 'parity_T': r.get('T', {}).get('parity'),
                   'label1_is_second_even': r.get('label1_is_second_even'),
                   'full_rhoT_over_rho2': r.get('full_rhoT_over_rho2'),
                   'omega_low': r.get('omega_low'), 'omega2_low': r.get('omega2_low')} for r in sp['per_q']]
    if not b['unstable']:
        b.update({'c2': sp['c2'], 'cT': sp['cT'], 'c1': sp['c1'], 'ratio_c2_cT': sp['c2'] / sp['cT'],
                  'F2': sp['ref']['F2'], 'Z21': sp['ref']['Z21'], 'S2': sp['ref']['S2'],
                  'F1': sp['ref']['F1'], 'FT': sp['ref']['FT'],
                  'v_over_q': {lab: sp['v_over_q_' + lab] for lab in ('T', '2', '1')},
                  'lowest_gapped_omega_per_q': sp['lowest_gapped_omega_per_q'],
                  'fsum_resid_max': sp['fsum_resid_max'], 'static_resid_max': sp['static_resid_max'],
                  'c2_ge_cT': bool(sp['c2'] >= sp['cT'])})
    b['time'] = time.time() - t
    return b


def cmd_bdg(args):
    P = load_points()
    nmax = int(args[0]) if args else 10 ** 9
    keys = sorted([k for k, v in P.items() if v.get('status') == 'ok' and 'bdg' not in v], key=lambda k: -float(k))
    n = 0
    for k in keys:
        if n >= nmax:
            break
        st = load_state_g(float(k))
        b = bdg_record(st)
        P = load_points()
        P[k]['bdg'] = b
        save_points(P)
        n += 1
        log('bdg g=%s unstable=%s ratio=%r F2=%r t=%.1f' % (k, b['unstable'], b.get('ratio_c2_cT'), b.get('F2'),
                                                           b['time']))


def point_with_bdg(P, g, tag):
    """branch point at g (fresh a*-optimised solve, cached) with its BdG record."""
    r = run_g(P, g, tag=tag)
    if r['status'] != 'ok':
        return r
    if 'bdg' not in r:
        st = load_state_g(g)
        r['bdg'] = bdg_record(st)
        P[gkey(g)] = r
        save_points(P)
    return r


def cmd_ratiomax(args):
    """maximum of c2/cT (LSQ speeds) along the metastable continuation: bounded Brent in g around the best grid
    point (each evaluation a fresh a*-optimised solve + BdG)."""
    P = load_points()
    R = json_load(ROOTS_JSON, {})
    gLc = R['Lambda_c']['root']
    tab = sorted([(float(k), v['bdg']['ratio_c2_cT']) for k, v in P.items()
                  if v.get('status') == 'ok' and v.get('bdg', {}).get('ratio_c2_cT') is not None and float(k) <= gLc + 1e-12])
    j = int(np.argmax([x[1] for x in tab]))
    if j == len(tab) - 1:
        R['ratio_max'] = {'at_Lambda_c_end': True, 'g': tab[j][0], 'ratio': tab[j][1]}
        json_save(R, ROOTS_JSON)
        return
    lo = tab[max(j - 1, 0)][0]
    hi = tab[min(j + 1, len(tab) - 1)][0]
    hist = []

    def negr(g):
        r = point_with_bdg(P, float(g), 'ratio_max')
        val = r['bdg']['ratio_c2_cT']
        hist.append({'g': float(g), 'ratio': val})
        log('ratiomax g=%r ratio=%r' % (g, val))
        return -val
    res = minimize_scalar(negr, bounds=(lo, hi), method='bounded', options={'xatol': 1e-4, 'maxiter': 60})
    gm = float(res.x)
    r = point_with_bdg(P, gm, 'ratio_max')
    R['ratio_max'] = {'g_at_max': gm, 'ratio_max': r['bdg']['ratio_c2_cT'], 'grid_best': list(tab[j]),
                      'search_bracket': [lo, hi], 'xatol': 1e-4, 'history': hist,
                      'F2_at_max': r['bdg']['F2'], 'c2_at_max': r['bdg']['c2'], 'cT_at_max': r['bdg']['cT']}
    json_save(R, ROOTS_JSON)
    log('ratio max', R['ratio_max']['ratio_max'], 'at g', gm)


def bdg_single(st, frac):
    a = float(np.linalg.norm(st.cell[0]))
    q = np.array([frac * 2.0 * PI / a, 0.0])
    r = cc2d.bdg(st, q, KCUT, nlow=6, chi_cg=False, full_check=False)
    return {'frac': frac, 'unstable': bool(r['unstable']), 'min_omega2': r['min_omega2'],
            'omega2_over_q2_min': r['min_omega2'] / float(q @ q)}


def cmd_dyn(args):
    """onset of the BdG dynamical instability along the continuation: for each |q|a/2pi in (0.03, 0.05, 0.075,
    0.10, 0.01, 0.005) the g below which the Bloch sector q along a1 has imaginary omega (bisection in g,
    fresh a*-optimised solve at every evaluation)."""
    P = load_points()
    R = json_load(ROOTS_JSON, {})
    D = R.get('dyn', {})
    for frac in (0.03, 0.05, 0.075, 0.10, 0.01, 0.005):
        key = repr(frac)
        if key in D:
            continue
        good = sorted([float(k) for k, v in P.items() if v.get('status') == 'ok' and float(k) <= 12.6])
        status = {}
        for g in good:
            st = load_state_g(g)
            status[g] = bdg_single(st, frac)['unstable']
        uns = [g for g in good if status[g]]
        sta = [g for g in good if not status[g]]
        if not uns:
            D[key] = {'onset': None, 'note': 'stable at every cached state'}
            continue
        lo = max(uns)
        hi = min([g for g in sta if g > lo])
        hist = []
        while hi - lo > 1e-6:
            mid = 0.5 * (lo + hi)
            r = run_g(P, mid, tag='dyn')
            if r['status'] != 'ok':
                lo = mid
                continue
            st = load_state_g(mid)
            bs = bdg_single(st, frac)
            hist.append({'g': mid, 'unstable': bs['unstable'], 'min_omega2': bs['min_omega2']})
            if bs['unstable']:
                lo = mid
            else:
                hi = mid
        D[key] = {'onset_bracket': [lo, hi], 'onset_mid': 0.5 * (lo + hi), 'history': hist}
        log('dyn frac', frac, 'onset bracket', lo, hi)
        R['dyn'] = D
        json_save(R, ROOTS_JSON)
    R['dyn'] = D
    json_save(R, ROOTS_JSON)


# ----------------------------------------------------------------------------------------------------------
# the end of the branch: de/da profiles across the interval of a in which the crystal exists at fixed cell
# ----------------------------------------------------------------------------------------------------------
def profile_D(g, seed, a_center, left=0.004, dl=1e-4, dr=2e-5, edge_tol=1e-11):
    """de/da(a) at coupling g from a_center to the left (fixed range) and to the right until the fixed-cell crystal
    ceases to exist (collapse to uniform); the right edge is refined by bisection in a.  Continuation seeding."""
    kern = cc2d.Kernel('step', g)
    rows = []
    st_c, ok = solve_fixed(kern, a_center, seed)
    if not ok:
        return {'g': g, 'error': 'no crystal at a_center'}
    rows.append((a_center, cc2d.dedA_envelope(st_c), st_c.contrast))
    sd = st_c
    a = a_center
    left_ok, left_bad = a_center, None
    while a > a_center * (1.0 - left):
        a -= dl * a_center
        st, ok = solve_fixed(kern, a, sd)
        if not ok:
            rows.append((a, None, None))
            left_bad = a
            break
        sd = st
        left_ok = a
        rows.append((a, cc2d.dedA_envelope(st), st.contrast))
    sd = st_c
    a = a_center
    last_ok_state = st_c
    while True:
        an = a + dr * a_center
        st, ok = solve_fixed(kern, an, sd)
        if not ok:
            a_bad = an
            break
        sd = st
        last_ok_state = st
        a = an
        rows.append((a, cc2d.dedA_envelope(st), st.contrast))
        if a > a_center * 1.05:
            a_bad = None
            break
    a_ok = a
    edge_rows = []
    if a_bad is not None:
        while a_bad - a_ok > edge_tol * a_ok:
            am = 0.5 * (a_ok + a_bad)
            st, ok = solve_fixed(kern, am, last_ok_state)
            if ok:
                a_ok = am
                last_ok_state = st
                edge_rows.append((am, cc2d.dedA_envelope(st), st.contrast))
            else:
                a_bad = am
    rows = sorted([r for r in rows if r[1] is not None])
    allr = sorted(rows + edge_rows)
    D = np.array([r[1] for r in allr])
    sc = int(np.sum(np.sign(D[1:]) != np.sign(D[:-1])))
    jmax = int(np.argmax(D))
    out = {'g': g, 'a_center': a_center, 'right_edge_a_bracket': [a_ok, a_bad], 'n_points': len(allr),
           'left_scan_lowest_ok_a': left_ok, 'left_scan_first_failed_a': left_bad,
           'dedA_sign_changes': sc, 'dedA_max': float(D[jmax]), 'a_at_dedA_max': float(allr[jmax][0]),
           'dedA_at_last_ok_before_edge': float(edge_rows[-1][1]) if edge_rows else float(rows[-1][1]),
           'rows_coarse': [{'a': r[0], 'dedA': r[1], 'contrast': r[2]} for r in rows[::5]],
           'rows_edge': [{'a': r[0], 'dedA': r[1], 'contrast': r[2]} for r in edge_rows[-12:]]}
    out['sym_hessian_at_edge_state'] = sym_sector_hessian(last_ok_state)['lowest_constrained'][:2]
    return out


def global_scan(g, avals, sigmas=(0.22,)):
    """fixed-cell ground states from Gaussian-droplet seeds (no continuation) over a range of a: does any crystal
    exist at coupling g?"""
    kern = cc2d.Kernel('step', g)
    rows = []
    for a in avals:
        for sg in sigmas:
            try:
                st = cc2d.ground_state(cc2d.hex_cell(a), kern, N, 1.0, seed=None, sigma_seed=sg, tol=GS_TOL)
            except ZeroDivisionError:
                PCG_BREAKDOWNS.append({'g': g, 'a': float(a), 'global_scan': True})
                rows.append({'a': float(a), 'sigma_seed': sg, 'pcg_breakdown': True, 'uniform': None,
                             'converged': False})
                continue
            conv = bool(st.info.get('newton', {}).get('converged', False))
            row = {'a': float(a), 'sigma_seed': sg, 'uniform': st.uniform, 'converged': conv,
                   'contrast': st.contrast, 'eps': st.eps}
            if not st.uniform and conv:
                row['dedA'] = cc2d.dedA_envelope(st)
                row['lambda_sym'] = sym_sector_hessian(st)['lowest_constrained'][0]
            rows.append(row)
    return {'g': g, 'rows': rows, 'n_crystal': int(sum(1 for r in rows if r['uniform'] is False and r['converged']))}


def cmd_fold(args):
    P = load_points()
    F = json_load(FOLD_JSON, {})
    good = sorted([(float(k), v) for k, v in P.items() if v.get('status') == 'ok'])
    lost = sorted([(float(k), v) for k, v in P.items() if v.get('status') == 'lost'])
    g_ok, r_ok = good[0]
    g_lost = max(x[0] for x in lost if x[0] < g_ok)
    st_ok = load_state_g(g_ok)
    if 'profile_last_ok' not in F:
        F['profile_last_ok'] = profile_D(g_ok, st_ok, r_ok['astar'])
        F['profile_last_ok']['astar'] = r_ok['astar']
        json_save(F, FOLD_JSON)
    if 'profile_first_lost' not in F:
        F['profile_first_lost'] = profile_D(g_lost, st_ok, r_ok['astar'])
        json_save(F, FOLD_JSON)
    if 'profile_first_lost_wide' not in F:
        F['profile_first_lost_wide'] = profile_D(g_lost, st_ok, r_ok['astar'], left=0.08, dl=5e-4)
        json_save(F, FOLD_JSON)
    # a coarser look a little further below the end (crystal at fixed cell still exists, e(a) monotonic)
    for dg in (0.01, 0.05):
        key = 'profile_end_minus_%g' % dg
        if key not in F:
            F[key] = profile_D(g_ok - dg, st_ok, r_ok['astar'] * (1.0 - 0.002), left=0.03, dl=1e-3)
            json_save(F, FOLD_JSON)
    for gs in (g_lost, round(g_ok - 0.1, 6), 12.0):
        key = 'global_scan_g%r' % gs
        if key not in F:
            F[key] = global_scan(gs, np.round(np.arange(1.30, 1.801, 0.025), 6))
            log(key, 'n_crystal', F[key]['n_crystal'])
            json_save(F, FOLD_JSON)
    # extrapolation of the symmetric-sector eigenvalue along the branch: lambda^2 linear in g near the end
    near = [(g, r) for g, r in good if g < g_ok + 0.003 and 'sym_hessian' in r]
    if len(near) >= 3:
        gg = np.array([x[0] for x in near])
        ll = np.array([x[1]['sym_hessian']['lowest_constrained'][0] for x in near])
        p1 = np.polyfit(gg, ll ** 2, 1)
        p2 = np.polyfit(gg, ll ** 2, 2) if len(near) >= 4 else None
        F['lambda_sym_extrapolation'] = {'n': len(near), 'g': gg, 'lambda_sym': ll,
                                         'g_lambda0_linear_in_lambda2': float(-p1[1] / p1[0]),
                                         'g_lambda0_quadratic_in_lambda2': (float(np.max(np.roots(p2).real))
                                                                           if p2 is not None else None)}
        dd = np.array([x[1]['d2e_da2'] for x in near])
        F['lambda_sym_extrapolation']['d2e_da2'] = dd
    for k in ('profile_last_ok', 'profile_first_lost'):
        pr = F[k]
        log(k, 'g=%r edge=%r sign_changes=%r Dmax=%r D_edge=%r' % (pr['g'], pr['right_edge_a_bracket'],
                                                                   pr['dedA_sign_changes'], pr['dedA_max'],
                                                                   pr['dedA_at_last_ok_before_edge']))
    json_save(F, FOLD_JSON)


def cmd_foldbdg(args):
    """placeholder kept for the CLI (BdG at the end states is computed by 'bdg' on the bisection states)."""
    return


# ----------------------------------------------------------------------------------------------------------
# convergence (N and Kcut) at Lambda_c and near the end
# ----------------------------------------------------------------------------------------------------------
def cmd_conv(args):
    """N / Kcut convergence at Lambda_c, at the maximum of c2/cT and at g = 12.4; robustness of the branch-end
    bracket and of the BdG-instability onset under N and Kcut."""
    global N, KCUT
    P = load_points()
    R = json_load(ROOTS_JSON, {})
    F = json_load(FOLD_JSON, {})
    C = json_load(CONV_JSON, {})
    C.pop('last_ok', None)
    targets = {'Lambda_c': R['Lambda_c']['root'], 'g12.4': 12.4}
    if 'ratio_max' in R and R['ratio_max'].get('g_at_max') is not None:
        targets['ratio_max'] = R['ratio_max']['g_at_max']
    N0, K0 = N, KCUT
    for name, g in targets.items():
        if name in C:
            continue
        rows = []
        st0 = load_state_g(g)
        a0 = P[gkey(g)]['astar']
        for NN in (48, 64, 80):
            N = NN
            kern = cc2d.Kernel('step', g)
            o = astar_search(kern, a0, st0)
            st = o['state']
            row = {'N': NN, 'astar': o['astar'], 'eps_c': st.eps, 'mu_c': st.mu,
                   'f': g * (st.mu - st.eps) - st.mu ** 2 / (2 * PI), 'h': st.eps - PI * g / 2,
                   'd2e_da2': o['d2e_da2'], 'n_planewaves': int(st.grid.nm)}
            for kc in ((60.0, 80.0, 100.0) if NN == 64 else (80.0,)):
                sp = cc2d.speeds(st, 0.0, FRACS, kc)
                if sp.get('unstable'):
                    row['Kcut_%g' % kc] = {'unstable': True}
                    continue
                row['Kcut_%g' % kc] = {'c2': sp['c2'], 'cT': sp['cT'], 'c1': sp['c1'],
                                       'ratio_c2_cT': sp['c2'] / sp['cT'], 'F2': sp['ref']['F2']}
            rows.append(row)
            log('conv', name, NN, row['astar'], row['Kcut_80'].get('ratio_c2_cT'))
        N = N0
        C[name] = {'g': g, 'rows': rows}
        json_save(C, CONV_JSON)
    # branch-end bracket under N
    if 'branch_end_bracket_vs_N' not in C and F.get('bisection_bracket'):
        lo, hi = F['bisection_bracket']
        g_ok, g_lost = hi + 1e-5, lo - 1e-5
        st0 = load_state_g(hi)
        a0 = P[gkey(hi)]['astar']
        out = {'g_test_ok': g_ok, 'g_test_lost': g_lost, 'rows': []}
        for NN in (48, 80):
            N = NN
            row = {'N': NN}
            for nm, g in (('above', g_ok), ('below', g_lost)):
                try:
                    o = astar_search(cc2d.Kernel('step', g), a0, st0)
                    row[nm] = {'minimum_found': True, 'astar': o['astar'], 'd2e_da2': o['d2e_da2']}
                except Lost as ex:
                    row[nm] = {'minimum_found': False, 'why': ex.why}
            out['rows'].append(row)
            log('branch-end bracket N=%d' % NN, row)
        N = N0
        C['branch_end_bracket_vs_N'] = out
        json_save(C, CONV_JSON)
    # BdG instability onset (q frac 0.03) under N and Kcut
    dyn = R.get('dyn', {}).get(repr(0.03), {})
    if 'dyn_onset_vs_N_Kcut' not in C and dyn.get('onset_bracket'):
        lo, hi = dyn['onset_bracket']
        out = {'g_test_stable': hi + 1e-4, 'g_test_unstable': lo - 1e-4, 'rows': []}
        for NN, kc in ((48, 80.0), (80, 80.0), (64, 60.0), (64, 100.0)):
            N, KCUT = NN, kc
            row = {'N': NN, 'Kcut': kc}
            for nm, g in (('above', hi + 1e-4), ('below', lo - 1e-4)):
                stn = load_state_g(min([float(k) for k, v in P.items() if v.get('status') == 'ok'],
                                       key=lambda x: abs(x - g)))
                o = astar_search(cc2d.Kernel('step', g), float(np.linalg.norm(stn.cell[0])), stn)
                row[nm] = bdg_single(o['state'], 0.03)
            out['rows'].append(row)
            log('dyn onset check', row)
        N, KCUT = N0, K0
        C['dyn_onset_vs_N_Kcut'] = out
        json_save(C, CONV_JSON)


# ----------------------------------------------------------------------------------------------------------
# collect
# ----------------------------------------------------------------------------------------------------------
def cmd_collect(args):
    P = load_points()
    R = json_load(ROOTS_JSON, {})
    F = json_load(FOLD_JSON, {})
    C = json_load(CONV_JSON, {})
    qa = json_load(os.path.join(HERE, 'qa_results.json'), {})
    good = sorted([(float(k), v) for k, v in P.items() if v.get('status') == 'ok'], key=lambda x: -x[0])
    lostp = sorted([(float(k), v) for k, v in P.items() if v.get('status') == 'lost'], key=lambda x: -x[0])
    table = []
    for g, r in good:
        b = r.get('bdg', {})
        table.append({'g': g, 'tag': r.get('tag'), 'astar': r['astar'], 'eps_c': r['eps_c'], 'mu_c': r['mu_c'],
                      'contrast': r['contrast'], 'f': r['f'], 'eps_minus_pi_g_half': r['eps_minus_pi_g_half'],
                      'P_c': r['P_c'], 'P_u_at_mu_c': r['P_u_at_mu_c'], 'd2e_da2': r['d2e_da2'],
                      'lambda_sym_min': r.get('sym_hessian', {}).get('lowest_constrained', [None])[0],
                      'gamma_A_min_constrained': r.get('gamma_hessian', {}).get('A_lowest_constrained', [None])[0],
                      'bz_min_eig_A': r.get('bz_scan', {}).get('min_eig_A'),
                      'bdg_unstable': b.get('unstable'), 'c2': b.get('c2'), 'cT': b.get('cT'), 'c1': b.get('c1'),
                      'ratio_c2_cT': b.get('ratio_c2_cT'), 'F2': b.get('F2'), 'Z21': b.get('Z21'),
                      'S2': b.get('S2'), 'fsum_resid_max': b.get('fsum_resid_max'),
                      'static_resid_max': b.get('static_resid_max'),
                      'min_omega2_at_qa_q': [x['min_omega2'] for x in b.get('per_q', [])] or None,
                      'gs_resid': r['gs_resid']})
    out = {'schema_note': 'Q-C melting, second leg; all numbers repr(float)', 'settings': {
        'N': N, 'Kcut': KCUT, 'fracs': list(FRACS), 'gs_tol': GS_TOL, 'kernel': 'step', 'rho': 1.0,
        'astar_definition': 'root of the envelope derivative de/da (Brent, xtol 1e-14 a) at the local minimum of e(a) '
                            'reached by a downhill walk from the continuation guess',
        'seed': 'WORK/qa_states.npz step_g16_aroot, then continuation (nearest cached state from above)'}}
    lc = R.get('Lambda_c', {})
    ec = R.get('energy_crossing', {})
    out['Lambda_c'] = lc.get('root')
    out['Lambda_u'] = lc.get('Lambda_u')
    out['energy_crossing'] = ec.get('root')
    out['Lambda_c_detail'] = lc
    out['energy_crossing_detail'] = ec
    pLc = P.get(gkey(lc['root'])) if lc.get('root') is not None else None
    if pLc and 'bdg' in pLc:
        out['ratio_at_Lambda_c'] = pLc['bdg']['ratio_c2_cT']
        out['F2_at_Lambda_c'] = pLc['bdg']['F2']
        out['bdg_at_Lambda_c'] = pLc['bdg']
    # metastable continuation: Lambda_c down to the end
    meta = [t for t in table if lc.get('root') is not None and t['g'] <= lc['root'] + 1e-12 and
            t['ratio_c2_cT'] is not None]
    if meta:
        m = max(meta, key=lambda t: t['ratio_c2_cT'])
        out['ratio_max_metastable'] = m['ratio_c2_cT']
        out['ratio_max_metastable_at_g'] = m['g']
        out['ratio_max_metastable_n_states'] = len(meta)
    bb = F.get('bisection_bracket')
    out['branch_end_g'] = 0.5 * (bb[0] + bb[1]) if bb else None
    out['branch_end_bisection_bracket'] = bb
    out['branch_end_bracket_first_le_0.005'] = F.get('bisection_bracket_first_le_0.005')
    out['branch_end_continuation_bracket_step_0.05'] = [F.get('continuation_first_lost_0.05'),
                                                        F.get('continuation_last_ok_0.05')]
    out['branch_end_criterion'] = (
        'a-curvature: below the bracket the downhill walk in a finds no local minimum of e(a); de/da < 0 on the whole '
        'interval of a where the fixed-cell crystal exists, up to its right edge where the fixed-cell crystal folds '
        '(symmetric-sector eigenvalue -> 0) and the solve collapses to the uniform state. Above the bracket the minimum '
        'exists with d2e/da2 -> 0+ and the symmetric-sector eigenvalue small but positive: the minimum of e(a) merges '
        'with the maximum of e(a) that sits just inside the fixed-cell existence edge (fold of the a*-branch).')
    g_last = min(t['g'] for t in table)
    tl = [t for t in table if t['g'] == g_last][0]
    pl = F.get('profile_last_ok', {})
    pf = F.get('profile_first_lost_wide', F.get('profile_first_lost', {}))
    out['branch_end_last_ok_state'] = {
        'g': g_last, 'astar': tl['astar'], 'd2e_da2': tl['d2e_da2'], 'lambda_sym_min': tl['lambda_sym_min'],
        'eps_c': tl['eps_c'], 'mu_c': tl['mu_c'], 'contrast': tl['contrast'], 'f': tl['f'],
        'eps_minus_pi_g_half': tl['eps_minus_pi_g_half'], 'bdg_unstable_at_qa_q': tl['bdg_unstable'],
        'fixed_cell_right_edge_a': pl.get('right_edge_a_bracket'), 'dedA_sign_changes_in_interval':
            pl.get('dedA_sign_changes'), 'dedA_max_in_interval': pl.get('dedA_max'),
        'dedA_just_inside_edge': pl.get('dedA_at_last_ok_before_edge'),
        'lambda_sym_at_edge_state': pl.get('sym_hessian_at_edge_state')}
    out['branch_end_first_lost_state'] = {
        'g': pf.get('g'), 'fixed_cell_interval_a': [pf.get('left_scan_lowest_ok_a'),
                                                    (pf.get('right_edge_a_bracket') or [None])[0]],
        'left_scan_first_failed_a': pf.get('left_scan_first_failed_a'),
        'dedA_sign_changes_in_interval': pf.get('dedA_sign_changes'), 'dedA_max_in_interval': pf.get('dedA_max'),
        'dedA_just_inside_edge': pf.get('dedA_at_last_ok_before_edge'),
        'lambda_sym_at_edge_state': pf.get('sym_hessian_at_edge_state')}
    lx = F.get('lambda_sym_extrapolation', {})
    out['lambda_sym_zero_extrapolation_g'] = lx.get('g_lambda0_linear_in_lambda2')
    allr = [t for t in table if t['c2'] is not None]
    out['any_c2_ge_cT'] = bool(any(t['c2'] >= t['cT'] for t in allr)) if allr else None
    out['any_c2_ge_cT_n_states'] = len(allr)
    out['n_crystal_states_total'] = len(table)
    out['n_crystal_states_bdg_unstable'] = sum(1 for t in table if t['bdg_unstable'])
    out['max_ratio_all_states'] = max(t['ratio_c2_cT'] for t in allr) if allr else None
    out['ratio_max_detail'] = R.get('ratio_max')
    dyn = R.get('dyn', {})
    out['bdg_instability_onsets'] = dyn
    qa_on = [(float(k), v) for k, v in dyn.items() if float(k) in FRACS and v.get('onset_bracket')]
    if qa_on:
        fk, fv = max(qa_on, key=lambda x: x[1]['onset_mid'])
        out['bdg_instability_first_g'] = fv['onset_mid']
        out['bdg_instability_first_bracket'] = fv['onset_bracket']
        out['bdg_instability_first_q_frac'] = fk
    sm = [(float(k), v['onset_mid']) for k, v in dyn.items() if float(k) < 0.02 and v.get('onset_mid')]
    if len(sm) == 2:
        (q1, g1), (q2, g2) = sorted(sm)
        kap = (g1 - g2) / (q2 * q2 - q1 * q1)
        out['bdg_instability_q_to_0_estimate'] = g1 + kap * q1 * q1
        out['bdg_instability_q_to_0_note'] = 'onset(q) = g0 - kappa q^2 through the |q|a/2pi = 0.005 and 0.01 onsets'
    out['branch_table'] = table
    out['lost_points'] = [{'g': g, 'criteria': r['lost_criteria'], 'tag': r.get('tag'),
                           'a_edge': r.get('a_edge'), 'last_walk': (r.get('walk') or [])[-3:]} for g, r in lostp]
    out['fold'] = F
    out['convergence'] = C
    # consistency with qa_results.json at the Q-A g values
    cons = {}
    for gq in ('16', '14', '13.5', '13.25', '13'):
        p = qa.get('points', {}).get(gq)
        mine = P.get(gkey(float(gq)))
        if p and mine and 'bdg' in mine:
            b = mine['bdg']
            cons[gq] = {k: {'qc': b[k2] if k2 in b else mine.get(k2), 'qa': p[k1],
                            'rel_diff': abs((b[k2] if k2 in b else mine.get(k2)) - p[k1]) / abs(p[k1])}
                        for k, k1, k2 in (('astar', 'astar', 'astar'), ('c2', 'c2', 'c2'), ('cT', 'cT', 'cT'),
                                          ('c1', 'c1', 'c1'), ('F2', 'F2', 'F2'), ('Z21', 'Z21', 'Z21'),
                                          ('S2', 'S2', 'S2'), ('eps', 'e_per_particle', 'eps_c'), ('mu', 'mu', 'mu_c'))}
            cons[gq]['ratio_qc'] = b['ratio_c2_cT']
            cons[gq]['ratio_qa'] = p['c2'] / p['cT']
            cons[gq]['qa_astar_aroot'] = p['astar_crosscheck']['dedA_root']
            cons[gq]['astar_vs_qa_aroot_rel'] = abs(mine['astar'] - p['astar_crosscheck']['dedA_root']) / mine['astar']
    out['consistency_with_qa_results'] = cons
    json_save(out, os.path.join(HERE, 'qc_results.json'))
    log('wrote qc_results.json')
    for k in ('Lambda_c', 'Lambda_u', 'energy_crossing', 'ratio_at_Lambda_c', 'F2_at_Lambda_c', 'ratio_max_metastable',
              'ratio_max_metastable_at_g', 'branch_end_g', 'branch_end_bisection_bracket', 'any_c2_ge_cT',
              'bdg_instability_first_g', 'bdg_instability_first_bracket', 'bdg_instability_q_to_0_estimate',
              'max_ratio_all_states', 'lambda_sym_zero_extrapolation_g'):
        log(k, repr(out.get(k)))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'collect'
    args = sys.argv[2:]
    {'branch': cmd_branch, 'up': cmd_up, 'grid': cmd_grid, 'ratiomax': cmd_ratiomax, 'dyn': cmd_dyn, 'roots': cmd_roots, 'bdg': cmd_bdg, 'fold': cmd_fold,
     'foldbdg': cmd_foldbdg, 'conv': cmd_conv, 'collect': cmd_collect}[cmd](args)


if __name__ == '__main__':
    main()
