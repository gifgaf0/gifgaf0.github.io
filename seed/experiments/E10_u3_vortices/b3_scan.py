"""
E10 Route B, B3 (PREREG_B2B3 §3): fixed-charge straight elementary string, radial reduction (u3radial.py).

  E(k, q) = min_{h, a, alpha} [ T + k^2 J + q^2 / (4 I) ],  J = I (same Gauss-law quadratic form, §2.3 of the
  report), omega = q / (2 I).  lam in {0.8, 1.0, 1.2}; G = diag(0, 1, 0).

Scan (PREREG §3): k = 0 first, q = 0, 0.1, ... until the window closes (omega >= m_bulk, or > 1 % of the charge
density within 4 units of the box edge); then k = 0.05 ... 1.0 (step 0.05), q scanned the same way.
Warm start: nearest solved neighbour (Euclidean in (k, q)).  Thin-ring test as E9 Phase 0.
Run: python3 b3_scan.py > log_b3.txt   (one worker per lambda)  -> b3_results.json
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import numpy as np, json, time, sys, platform
from multiprocessing import Pool
from scipy.optimize import minimize
from scipy.interpolate import CloughTocher2DInterpolator, CubicSpline
import scipy
from u3radial import Radial, fd_check_radial
from u3common import LAMBDAS, m_bulk

DR, RMAX = 0.1, 20.0
DK, DQ = 0.05, 0.1
NK = int(os.environ.get('B3_NK', 20))   # k = 0 .. 1.0 (env override for smoke tests only)
Q_CAP = int(os.environ.get('B3_QCAP', 300))   # safety cap: q <= 30 per row (set before the run; reaching it is recorded)
LEAK_MAX, EDGE = 0.01, 4.0
ALPHA0 = np.pi / 4 - 0.05   # initial orientation of the very first state (flat direction at k = q = 0)
OPTS = dict(maxiter=20000, maxfun=40000, gtol=1e-9, ftol=1e-12, maxcor=20)


def solve_point(R, k, q, x0):
    res = minimize(R.make_fg(k, q), x0, jac=True, method='L-BFGS-B', options=OPTS)
    o = R.observables(res.x, k, q)
    g = R.make_fg(k, q)(res.x)[1]
    o.update(k=round(k, 10), q=round(q, 10), J=o['I'], success=bool(res.success), message=str(res.message),
             nit=int(res.nit), grad_max=float(np.max(np.abs(g))),
             iter_cap_hit=bool(res.nit >= OPTS['maxiter'] or res.nfev >= OPTS['maxfun']))
    apply_q0_rule(o)
    return o, res.x


def apply_q0_rule(o):
    """Deviation (REPORT §7): at q = 0 there is no charge, so the leak test (a fraction of the charge density)
    cannot fail; leak := 0.  The fraction of the unit (omega = 1) kinetic density is kept as leak_unit_density.
    (Run 1 evaluated it from the unit density, which is numerical noise once I -> 0 at k > 0, alpha -> 0.)"""
    if o['q'] == 0 and 'leak_unit_density' not in o:
        o['leak_unit_density'] = o['leak']; o['leak'] = 0.0
    return o


def in_window(o, mb):
    return bool(o['omega'] < mb and o['leak'] < LEAK_MAX)


def scan_lambda(lam):
    tag = f'lam{lam:g}'
    mb = m_bulk(lam)
    R = Radial(lam, dr=DR, rmax=RMAX, relax_alpha=True)
    t0 = time.time()
    sol = {}; recs = []; log = []

    def warm(i, j):
        if not sol:
            return R.initial(alpha=ALPHA0), 'abelian-Higgs initial'
        best = min(sol, key=lambda ij: ((ij[0] - i) * DK) ** 2 + ((ij[1] - j) * DQ) ** 2 + 1e-12 * ij[1])
        return sol[best][1], f'({best[0] * DK:.2f},{best[1] * DQ:.2f})'

    capped = []
    I0 = T0 = None
    for i in range(NK + 1):
        k = i * DK; j = 0; any_in = False
        while j <= Q_CAP:
            q = j * DQ
            x0, src = warm(i, j)
            o, x = solve_point(R, k, q, x0)
            if I0 is None:      # frozen-profile reference: static string at alpha = pi/4
                h, ap, _ = R.unpack(x)
                I0, _ = R.K_solve(h, ap, np.pi / 4); T0 = o['T']
            wc = q / (2 * I0)
            o['Tcal_frozen'] = T0 - (k * k + wc * wc) * I0
            o['omega_over_mbulk'] = o['omega'] / mb
            o['warm_from'] = src; o['i'] = i; o['j'] = j
            o['in_window'] = in_window(o, mb)
            sol[(i, j)] = (o, x); recs.append(o)
            if not o['success'] or o['iter_cap_hit']:
                log.append(f'[{tag}] NOT CONVERGED k={k:.2f} q={q:.2f}: {o["message"]} nit={o["nit"]} grad_max={o["grad_max"]:.2e}')
            if not o['in_window']:
                break
            any_in = True; j += 1
        if j > Q_CAP:
            capped.append(round(k, 10)); log.append(f'[{tag}] Q_CAP reached at k={k:.2f}')
        last = recs[-1]
        print(f'[{tag}] k={k:.2f}: in-window q up to {(j - 1) * DQ if any_in else None:}, closed at q={last["q"]:.2f} '
              f'(omega/m={last["omega_over_mbulk"]:.4f}, leak={last["leak"]:.2e}), {time.time() - t0:.0f} s', flush=True)
    # raw solves saved before the analysis (the analysis can be re-run from these)
    np.savez_compressed(f'b3_raw_{tag}.npz', keys=np.array(list(sol.keys())), xs=np.array([v[1] for v in sol.values()]))
    with open(f'b3_raw_{tag}.json', 'w') as fh:
        json.dump(recs, fh, separators=(',', ':'), default=float)
    try:
        summ = analyse(tag, R, lam, mb, sol, log)
    except Exception as ex:                      # keep the scan even if the analysis fails
        import traceback
        log.append(f'[{tag}] ANALYSIS FAILED: {traceback.format_exc()}')
        summ = dict(verdict='ANALYSIS FAILED', sign_changes=[], n_in_window=None)
    summ.update(q_capped_at_k=capped, I0_static_alpha_pi4=I0, T0_static=T0, scan_seconds=time.time() - t0)
    for l in log:
        print(l, flush=True)
    print(f'[{tag}] {len(recs)} solves, {summ["n_in_window"]} in window, sign changes {len(summ["sign_changes"])}, '
          f'verdict {summ["verdict"]}, {summ["scan_seconds"]:.0f} s', flush=True)
    return lam, recs, summ, log


def tcal(win, i, j):
    o = win[(i, j)]; flags = []
    if i == 0:
        dEk = 0.0; flags.append('k=0 (k dE/dk = 0)')
    elif (i - 1, j) in win and (i + 1, j) in win:
        dEk = (win[(i + 1, j)]['E'] - win[(i - 1, j)]['E']) / (2 * DK)
    elif (i + 1, j) in win:
        dEk = (win[(i + 1, j)]['E'] - o['E']) / DK; flags.append('one-sided k (forward)')
    elif (i - 1, j) in win:
        dEk = (o['E'] - win[(i - 1, j)]['E']) / DK; flags.append('one-sided k (backward)')
    else:
        dEk = None; flags.append('no k neighbour in window')
    if j == 0:
        dEq = 0.0; flags.append('q=0 (q dE/dq = 0)')
    elif (i, j - 1) in win and (i, j + 1) in win:
        dEq = (win[(i, j + 1)]['E'] - win[(i, j - 1)]['E']) / (2 * DQ)
    elif (i, j + 1) in win:
        dEq = (win[(i, j + 1)]['E'] - o['E']) / DQ; flags.append('one-sided q (forward)')
    elif (i, j - 1) in win:
        dEq = (o['E'] - win[(i, j - 1)]['E']) / DQ; flags.append('one-sided q (backward)')
    else:
        dEq = None; flags.append('no q neighbour in window')
    k, q = i * DK, j * DQ
    T = None if (dEk is None or dEq is None) else o['E'] - k * dEk - q * dEq
    return T, dEk, dEq, flags


def analyse(tag, R, lam, mb, sol, log):
    win = {ij: v[0] for ij, v in sol.items() if v[0]['in_window']}
    Tc = {}
    for (i, j), o in win.items():
        T, dEk, dEq, flags = tcal(win, i, j)
        o['Tcal'] = T; o['dEdk'] = dEk; o['dEdq'] = dEq; o['Tcal_flags'] = flags
        o['Tcal_envelope'] = o['T'] - (o['k'] ** 2 + o['omega'] ** 2) * o['I']
        if T is not None:
            Tc[(i, j)] = T
    sc = []
    for (i, j), T in Tc.items():
        for (di, dj) in ((1, 0), (0, 1)):
            nb = (i + di, j + dj)
            if nb in Tc and np.sign(T) != np.sign(Tc[nb]) and T != 0:
                Tb = Tc[nb]; t = T / (T - Tb)
                oa, ob = win[(i, j)], win[nb]
                sc.append(dict(between=[[i * DK, j * DQ], [nb[0] * DK, nb[1] * DQ]],
                               k_star=(i + t * di) * DK, q_star=(j + t * dj) * DQ,
                               omega_star=oa['omega'] + t * (ob['omega'] - oa['omega']),
                               flags=sorted(set(oa['Tcal_flags'] + ob['Tcal_flags']))))
    pts = np.array([[i, j] for (i, j) in win], float)
    Ev = np.array([win[ij]['E'] for ij in win])
    interp = CloughTocher2DInterpolator(pts, Ev) if len(pts) >= 3 and len(set(pts[:, 0])) > 1 else None
    row0 = sorted(j for (i, j) in win if i == 0)
    spl0 = CubicSpline(np.array(row0) * DQ, [win[(0, j)]['E'] for j in row0]) if len(row0) >= 4 else None
    for c in sc:
        ks, qs = c['k_star'], c['q_star']
        c['omega_star_over_mbulk'] = c['omega_star'] / mb

        def Eint(kk, qq):
            if ks == 0 and spl0 is not None and kk == 0:
                return float(spl0(qq)) if 0 <= qq <= row0[-1] * DQ else float('nan')
            return float(interp(kk / DK, qq / DQ)) if interp is not None else float('nan')

        def f(u):           # f(u) = u E(k*/u, q*/u);  d2E/dR2 = (2 pi / R_eq) f''(1), sign independent of n, Q
            return u * Eint(ks / u, qs / u)
        d2 = {}
        for hh in (0.03, 0.06):
            d2[f'h={hh}'] = (f(1 + hh) - 2 * f(1.0) + f(1 - hh)) / hh ** 2
        c['f2_interp'] = d2; c['f2'] = d2['h=0.03']
        c['interpolant'] = 'CubicSpline along k=0 row' if ks == 0 else 'Clough-Tocher (index coords)'
        c['stable_R'] = bool(np.isfinite(c['f2']) and c['f2'] > 0)
        Ed = {}; dconv = True
        for u in (0.97, 1.0, 1.03):
            kk, qq = ks / u, qs / u
            near = min(sol, key=lambda ij: (ij[0] * DK - kk) ** 2 + (ij[1] * DQ - qq) ** 2)
            o, _ = solve_point(R, kk, qq, sol[near][1])
            Ed[u] = u * o['E']; dconv &= o['success']
        c['f2_direct'] = (Ed[1.03] - 2 * Ed[1.0] + Ed[0.97]) / 0.03 ** 2
        c['direct_converged'] = bool(dconv)
        c['interp_direct_sign_agree'] = bool(np.isfinite(c['f2']) and np.sign(c['f2']) == np.sign(c['f2_direct']))
    good = [c for c in sc if c['stable_R']]
    ratios = [(o['Tcal'] / o['E'], o['k'], o['q']) for o in win.values() if o['Tcal'] is not None]
    mn = min(ratios) if ratios else (float('nan'), None, None)
    qmax_by_k = {f'{i * DK:.2f}': max(j for (ii, j) in win if ii == i) * DQ for i in sorted({ij[0] for ij in win})}
    return dict(n_solves=len(sol), n_in_window=len(win), n_not_converged=sum(not v[0]['success'] for v in sol.values()),
                q_max_in_window_by_k=qmax_by_k, sign_changes=sc, verdict='WINDOW' if good else 'NONE',
                min_Tcal_over_E=float(mn[0]), argmin_Tcal_over_E=dict(k=mn[1], q=mn[2]),
                max_abs_Tcal_fd_minus_env_over_E=float(max((abs(o['Tcal'] - o['Tcal_envelope']) / o['E']
                                                            for o in win.values() if o['Tcal'] is not None
                                                            and all('one-sided' not in f for f in o['Tcal_flags'])),
                                                           default=float('nan'))))


if __name__ == '__main__':
    t_start = time.time()
    print(f'Python {platform.python_version()}, NumPy {np.__version__}, SciPy {scipy.__version__}, {os.cpu_count()} cores', flush=True)
    gc, _ = fd_check_radial(lam=1.0, k=0.3, q=1.7, dr=DR, rmax=RMAX)
    print(f'outer gradient check (radial, lam=1, k=0.3, q=1.7, 40 coords incl. alpha, 5-point FD step 1e-4): worst rel err {gc:.2e}', flush=True)
    gc2, _ = fd_check_radial(lam=0.8, k=0.0, q=2.5, seed=3, dr=DR, rmax=RMAX)
    print(f'outer gradient check (radial, lam=0.8, k=0, q=2.5): worst rel err {gc2:.2e}', flush=True)
    with Pool(3) as pool:
        out = pool.map(scan_lambda, LAMBDAS, chunksize=1)
    results = dict(meta=dict(label='Exploration', prereg='PREREG_B2B3.md §3', instrument='u3radial.Radial',
                             dr=DR, rmax=RMAX, dk=DK, dq=DQ, k_max=NK * DK, q_cap=Q_CAP * DQ, leak_max=LEAK_MAX,
                             edge=EDGE, alpha0=ALPHA0, minimizer=dict(method='L-BFGS-B', **OPTS),
                             software=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__)),
                   gradient_check=dict(lam1_k0p3_q1p7=gc, lam0p8_k0_q2p5=gc2), lambdas=[])
    for lam, recs, summ, log in out:
        results['lambdas'].append(dict(lam=lam, m_bulk=m_bulk(lam), summary=summ, solves=recs, log=log))
    results['total_seconds'] = time.time() - t_start
    with open(os.environ.get('B3_OUT', 'b3_results.json'), 'w') as fh:
        json.dump(results, fh, separators=(',', ':'), default=float)
    print(f'total {results["total_seconds"]:.0f} s', flush=True)
