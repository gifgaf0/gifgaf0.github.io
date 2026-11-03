"""
E10 Route B, B3: resumed scan (run 2), pipelined over k rows.  Same functional, grid, solver options, window test,
cap and warm-start rule as b3_scan.py (run 1); the only change is the q = 0 leak rule (b3_scan.apply_q0_rule).

Warm-start equivalence.  In the sequential order of run 1 (rows k = 0, 0.05, ...; q upward within a row), the
nearest solved neighbour of (i, j) is (i-1, j) whenever row i-1 reached j (distance 0.05), otherwise (i, j-1)
(distance 0.1; any other solved point is farther).  So row i only needs row i-1's point j, or the knowledge that
row i-1 ended before j.  Workers solve rows concurrently and wait on exactly that dependency, which reproduces the
sequential warm-start chain point for point.

For lam = 0.8, rows i <= 2 (k <= 0.10) are imported from run 1 (b3_raw_lam0.8.npz/json); their in-window decisions
are unchanged by the q = 0 rule (checked on import).  lam = 1.0 and 1.2 are recomputed from k = 0 (run 1 was stopped
before saving them).  Every point is written to POINTS/<tag>/<i>_<j>.npz as it is solved.
Run: python3 b3_pipeline.py import <lam>   (after run 1 saved its raw file for lam)
     python3 b3_pipeline.py run            (rows 3..20 for all lambdas, 4 workers)
     python3 b3_pipeline.py analyse        (-> b3_results.json)
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import sys, json, time, glob, platform
import numpy as np
from multiprocessing import Pool
import scipy
import b3_scan as B
from u3radial import Radial
from u3common import LAMBDAS, m_bulk

POINTS = os.environ.get('B3_POINTS', '/tmp/claude-0/b3_points')
I_FIRST = 3


def tagof(lam):
    return f'lam{lam:g}'


def pdir(lam):
    d = os.path.join(POINTS, tagof(lam)); os.makedirs(d, exist_ok=True); return d


def save_point(lam, o, x):
    np.savez(os.path.join(pdir(lam), f'{o["i"]}_{o["j"]}.npz'), x=x, o=json.dumps(o, default=float))


def load_point(lam, i, j):
    f = os.path.join(pdir(lam), f'{i}_{j}.npz')
    if not os.path.exists(f):
        return None
    z = np.load(f)
    return json.loads(str(z['o'])), z['x']


def end_file(lam, i):
    return os.path.join(pdir(lam), f'end_{i}.json')


def do_import(lam):
    tag = tagof(lam)
    z = np.load(f'b3_raw_run1_{tag}.npz'); recs = json.load(open(f'b3_raw_run1_{tag}.json'))
    keys = [tuple(k) for k in z['keys']]
    xs = dict(zip(keys, z['xs']))
    last = {}
    n = 0
    for o in recs:
        i, j = o['i'], o['j']
        if i >= I_FIRST:
            continue
        old = o['in_window']
        B.apply_q0_rule(o)
        o['in_window'] = B.in_window(o, m_bulk(lam))
        assert o['in_window'] == old, (lam, i, j)
        o['run'] = 1
        save_point(lam, o, xs[(i, j)])
        last[i] = max(last.get(i, -1), j); n += 1
        if not o['in_window'] or j == B.Q_CAP:
            json.dump(dict(last_j=j, closed=not o['in_window']), open(end_file(lam, i), 'w'))
    for i in range(I_FIRST):
        assert os.path.exists(end_file(lam, i)), (lam, i)
    o00, _ = load_point(lam, 0, 0)
    print(f'imported {n} run-1 points for {tag}; rows 0..{I_FIRST - 1} last j = {last}', flush=True)


def ref(lam):
    """I0 (static string at alpha = pi/4) and T0, as in run 1 (computed from the (0,0) solve)."""
    o, x = load_point(lam, 0, 0)
    R = Radial(lam, dr=B.DR, rmax=B.RMAX, relax_alpha=True)
    h, ap, _ = R.unpack(x)
    I0, _ = R.K_solve(h, ap, np.pi / 4)
    return I0, o['T']


def row(args):
    lam, i = args
    tag = tagof(lam); mb = m_bulk(lam)
    if os.path.exists(end_file(lam, i)):
        return lam, i, 'already done'
    R = Radial(lam, dr=B.DR, rmax=B.RMAX, relax_alpha=True)
    if i > 0:
        while not os.path.exists(os.path.join(pdir(lam), '0_0.npz')):
            time.sleep(5)
        I0, T0 = ref(lam)
    k = i * B.DK; j = 0; t0 = time.time(); waited = 0.0
    while True:
        q = j * B.DQ
        prev = load_point(lam, i, j)
        if prev is not None:            # resume after an interruption
            o, x = prev
            if i == 0 and j == 0:
                I0, T0 = ref(lam)
        else:
            while True:
                if i == 0:
                    if j == 0:
                        x0, src = R.initial(alpha=B.ALPHA0), 'abelian-Higgs initial'
                    else:
                        x0, src = load_point(lam, 0, j - 1)[1], f'(0.00,{(j - 1) * B.DQ:.2f})'
                    break
                dep = load_point(lam, i - 1, j)
                if dep is not None:
                    x0, src = dep[1], f'({(i - 1) * B.DK:.2f},{q:.2f})'; break
                if os.path.exists(end_file(lam, i - 1)) and json.load(open(end_file(lam, i - 1)))['last_j'] < j:
                    x0, src = load_point(lam, i, j - 1)[1], f'({k:.2f},{(j - 1) * B.DQ:.2f})'; break
                time.sleep(2); waited += 2
            o, x = B.solve_point(R, k, q, x0)
            if i == 0 and j == 0:
                h_, ap_, _ = R.unpack(x); I0, _ = R.K_solve(h_, ap_, np.pi / 4); T0 = o['T']
            o['Tcal_frozen'] = T0 - (k * k + (q / (2 * I0)) ** 2) * I0
            o['omega_over_mbulk'] = o['omega'] / mb
            o['warm_from'] = src; o['i'] = i; o['j'] = j; o['run'] = 2
            o['in_window'] = B.in_window(o, mb)
            save_point(lam, o, x)
            if not o['success'] or o['iter_cap_hit']:
                print(f'[{tag}] NOT CONVERGED k={k:.2f} q={q:.2f}: {o["message"]} nit={o["nit"]} grad_max={o["grad_max"]:.2e}', flush=True)
        if not o['in_window'] or j >= B.Q_CAP:
            capped = o['in_window'] and j >= B.Q_CAP
            json.dump(dict(last_j=j, closed=not o['in_window'], capped=capped), open(end_file(lam, i), 'w'))
            print(f'[{tag}] k={k:.2f}: in-window q up to {(j - 1) * B.DQ if not capped else q:.1f}, '
                  f'{"Q_CAP reached (still in window)" if capped else "closed"} at q={q:.2f} '
                  f'(omega/m={o["omega_over_mbulk"]:.4f}, leak={o["leak"]:.2e}), {time.time() - t0:.0f} s (waited {waited:.0f} s)', flush=True)
            return lam, i, 'done'
        j += 1


def load_all(lam):
    sol = {}
    for f in glob.glob(os.path.join(pdir(lam), '*_*.npz')):
        b = os.path.basename(f)[:-4]
        if b.startswith('end'):
            continue
        i, j = map(int, b.split('_'))
        o, x = load_point(lam, i, j)
        sol[(i, j)] = (o, x)
    return sol


def analyse_lambda(lam):
    tag = tagof(lam); mb = m_bulk(lam)
    R = Radial(lam, dr=B.DR, rmax=B.RMAX, relax_alpha=True)
    sol = load_all(lam); log = []
    t0 = time.time()
    summ = B.analyse(tag, R, lam, mb, sol, log)
    ends = {i: json.load(open(end_file(lam, i))) for i in range(B.NK + 1) if os.path.exists(end_file(lam, i))}
    I0, T0 = ref(lam)
    summ.update(q_capped_at_k=[round(i * B.DK, 10) for i, e in ends.items() if e.get('capped') or (e['last_j'] == B.Q_CAP and not e['closed'])],
                I0_static_alpha_pi4=I0, T0_static=T0, analysis_seconds=time.time() - t0, row_ends=ends)
    recs = [sol[k][0] for k in sorted(sol)]
    for l in log:
        print(l, flush=True)
    print(f'[{tag}] {len(recs)} solves, {summ["n_in_window"]} in window, sign changes {len(summ["sign_changes"])}, '
          f'verdict {summ["verdict"]}', flush=True)
    return lam, recs, summ, log


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'import':
        do_import(float(sys.argv[2]))
    elif cmd == 'run':
        lams = [float(a) for a in sys.argv[2:]] or list(LAMBDAS)
        tasks = [(lam, i) for i in range(0, B.NK + 1) for lam in lams]
        with Pool(int(os.environ.get('B3_WORKERS', 4))) as pool:
            for r in pool.imap_unordered(row, tasks, chunksize=1):
                pass
        print('run done', flush=True)
    elif cmd == 'analyse':
        t_start = time.time()
        with Pool(3) as pool:
            out = pool.map(analyse_lambda, LAMBDAS, chunksize=1)
        gc = json.load(open('b3_gradcheck.json')) if os.path.exists('b3_gradcheck.json') else None
        results = dict(meta=dict(label='Exploration', prereg='PREREG_B2B3.md §3', instrument='u3radial.Radial',
                                 dr=B.DR, rmax=B.RMAX, dk=B.DK, dq=B.DQ, k_max=B.NK * B.DK, q_cap=B.Q_CAP * B.DQ,
                                 leak_max=B.LEAK_MAX, edge=B.EDGE, alpha0=B.ALPHA0, minimizer=dict(method='L-BFGS-B', **B.OPTS),
                                 runs='rows k<=0.10 from run 1 (b3_scan.py), rows k>=0.15 from run 2 (b3_pipeline.py)',
                                 software=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__)),
                       gradient_check=gc, lambdas=[])
        for lam, recs, summ, log in out:
            results['lambdas'].append(dict(lam=lam, m_bulk=m_bulk(lam), summary=summ, solves=recs, log=log))
        results['analysis_seconds'] = time.time() - t_start
        with open('b3_results.json', 'w') as fh:
            json.dump(results, fh, separators=(',', ':'), default=float)
        print('analysis written', flush=True)
