"""
E10 Amendment A: regenerate the original B3 solutions (lam = 1, dr = 0.1, r_max = 20) needed as warm starts,
by replaying the original warm-start chain (see verify_common docstring), and compare with b3_results.json.
Run: python3 verify_orig.py > log_verify_orig.txt
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import sys, time, json
import numpy as np
from multiprocessing import Pool
import b3_scan as B
import verify_common as V


def needed():
    S = V.select_S()
    pts = V.points_for(S)
    rec = V.orig_records()
    need = set()
    for (i, j) in pts:
        for ii in range(i + 1):
            need.add((ii, j))
    # every needed (i>0, j) must have been warm-started from (i-1, j) in the original run
    for (i, j) in need:
        if i > 0:
            assert rec[(i, j)]['warm_from'] == f'({(i - 1) * B.DK:.2f},{j * B.DQ:.2f})', (i, j, rec[(i, j)]['warm_from'])
    jmax = max(j for _, j in need)
    for j in range(jmax + 1):
        need.add((0, j))
        if j > 0:
            assert rec[(0, j)]['warm_from'] == f'(0.00,{(j - 1) * B.DQ:.2f})'
    return sorted(need)


def solve_one(R, rec, i, j, x0):
    o, x = B.solve_point(R, i * B.DK, j * B.DQ, x0)
    r = rec[(i, j)]
    o['i'] = i; o['j'] = j
    o['orig_E'] = r['E']; o['rel_dE_vs_orig'] = o['E'] / r['E'] - 1
    o['orig_alpha'] = r['alpha']; o['orig_I'] = r['I']; o['orig_nit'] = r['nit']
    V.save('orig', i, j, o, x)
    return o


def row0(jmax):
    R = V.radial('orig'); rec = V.orig_records(); x = None
    for j in range(jmax + 1):
        p = V.load('orig', 0, j)
        if p is not None:
            x = p[1]; continue
        x0 = R.initial(alpha=B.ALPHA0) if j == 0 else x
        o = solve_one(R, rec, 0, j, x0)
        x = V.load('orig', 0, j)[1]
        if j % 20 == 0:
            print(f'row0 j={j} E={o["E"]:.12f} rel dE vs orig {o["rel_dE_vs_orig"]:.1e}', flush=True)


def column(args):
    j, imax = args
    if j < 0:
        return row0(imax)
    R = V.radial('orig'); rec = V.orig_records()
    while V.load('orig', 0, j) is None:
        time.sleep(3)
    for i in range(1, imax + 1):
        if V.load('orig', i, j) is not None:
            continue
        x0 = V.load('orig', i - 1, j)[1]
        solve_one(R, rec, i, j, x0)
    return j


if __name__ == '__main__':
    need = needed()
    jmax = max(j for _, j in need)
    cols = {}
    for (i, j) in need:
        if i > 0:
            cols[j] = max(cols.get(j, 0), i)
    print(f'{len(need)} original points to regenerate (row 0 up to j={jmax}; {len(cols)} columns)', flush=True)
    tasks = [(-1, jmax)] + sorted(cols.items())
    t0 = time.time()
    with Pool(int(os.environ.get('VERIFY_WORKERS', 4))) as pool:
        for r in pool.imap_unordered(column, tasks, chunksize=1):
            pass
    worst = 0.0; rows = []
    for (i, j) in need:
        o, _ = V.load('orig', i, j)
        worst = max(worst, abs(o['rel_dE_vs_orig'])); rows.append(o['rel_dE_vs_orig'])
    print(f'regenerated {len(need)} points in {time.time() - t0:.0f} s; max |E/E_orig - 1| = {worst:.2e}; '
          f'bitwise-equal E at {sum(r == 0 for r in rows)}/{len(rows)}', flush=True)
