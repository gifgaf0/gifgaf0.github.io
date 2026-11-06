"""
E10 B3: analysis with the direct-solve cross-checks run in parallel (same computation as b3_pipeline.py analyse;
b3_scan.analyse is called unchanged, with solve_point served from a cache filled by 4 workers beforehand).
The rays' (k, q) points are generated with the same arithmetic as b3_scan.analyse.
Run: python3 b3_analyse_par.py > log_b3_analysis.txt  -> b3_results.json
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import json, time, platform, pickle
import numpy as np, scipy
from multiprocessing import Pool
import b3_scan as B
import b3_pipeline as P
from u3radial import Radial
from u3common import LAMBDAS, m_bulk

CACHE = '/tmp/claude-0/b3_direct_cache'


def ray_tasks(lam):
    sol = P.load_all(lam)
    win = {ij: v[0] for ij, v in sol.items() if v[0]['in_window']}
    Tc = {}
    for ij in win:
        T, *_ = B.tcal(win, *ij)
        if T is not None:
            Tc[ij] = T
    tasks = []
    for (i, j), T in Tc.items():
        for (di, dj) in ((1, 0), (0, 1)):
            nb = (i + di, j + dj)
            if nb in Tc and np.sign(T) != np.sign(Tc[nb]) and T != 0:
                Tb = Tc[nb]; t = T / (T - Tb)
                ks = (i + t * di) * B.DK; qs = (j + t * dj) * B.DQ
                for u in (0.97, 1.0, 1.03):
                    kk, qq = ks / u, qs / u
                    near = min(sol, key=lambda ij: (ij[0] * B.DK - kk) ** 2 + (ij[1] * B.DQ - qq) ** 2)
                    tasks.append((lam, kk, qq, near))
    return tasks


def run_task(t):
    lam, kk, qq, near = t
    f = os.path.join(CACHE, f'{lam:g}_{kk!r}_{qq!r}.pkl')
    if os.path.exists(f):
        return
    R = Radial(lam, dr=B.DR, rmax=B.RMAX, relax_alpha=True)
    x0 = P.load_point(lam, *near)[1]
    o, x = B.solve_point(R, kk, qq, x0)
    pickle.dump((o, x), open(f + '.tmp', 'wb')); os.replace(f + '.tmp', f)


_orig = B.solve_point


def cached_solve_point(R, k, q, x0):
    f = os.path.join(CACHE, f'{R.lam:g}_{k!r}_{q!r}.pkl')
    if os.path.exists(f):
        return pickle.load(open(f, 'rb'))
    print(f'cache miss lam={R.lam} k={k!r} q={q!r}; solving', flush=True)
    return _orig(R, k, q, x0)


if __name__ == '__main__':
    os.makedirs(CACHE, exist_ok=True)
    t0 = time.time()
    tasks = [t for lam in LAMBDAS for t in ray_tasks(lam)]
    print(f'{len(tasks)} direct solves on rays', flush=True)
    with Pool(4) as pool:
        for n, _ in enumerate(pool.imap_unordered(run_task, tasks, chunksize=1)):
            if n % 30 == 0:
                print(f'  {n} done, {time.time() - t0:.0f} s', flush=True)
    B.solve_point = cached_solve_point
    out = [P.analyse_lambda(lam) for lam in LAMBDAS]
    gc = json.load(open('b3_gradcheck.json'))
    results = dict(meta=dict(label='Exploration', prereg='PREREG_B2B3.md §3', instrument='u3radial.Radial',
                             dr=B.DR, rmax=B.RMAX, dk=B.DK, dq=B.DQ, k_max=B.NK * B.DK, q_cap=B.Q_CAP * B.DQ,
                             leak_max=B.LEAK_MAX, edge=B.EDGE, alpha0=B.ALPHA0, minimizer=dict(method='L-BFGS-B', **B.OPTS),
                             runs='lam=0.8 rows k<=0.10 from run 1 (b3_scan.py); everything else run 2 (b3_pipeline.py)',
                             software=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__)),
                   gradient_check=gc, lambdas=[])
    for lam, recs, summ, log in out:
        results['lambdas'].append(dict(lam=lam, m_bulk=m_bulk(lam), summary=summ, solves=recs, log=log))
    results['analysis_seconds'] = time.time() - t0
    with open('b3_results.json', 'w') as fh:
        json.dump(results, fh, separators=(',', ':'), default=float)
    print('analysis written', flush=True)
