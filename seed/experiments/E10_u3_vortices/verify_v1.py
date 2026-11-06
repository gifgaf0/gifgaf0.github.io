"""
E10 Amendment A §A.3, runs V1a / V1b / V1c (radial, lam = 1).  Label: Exploration, post-hoc verification.

  V1a: r_max = 40, dr = 0.1      V1b: r_max = 40, dr = 0.05 (decisive)      V1c: r_max = 60, dr = 0.05
Every point is warm-started from the regenerated original solution (verify_orig.py) padded with vacuum
(verify_common.pad); the Dirichlet edge h = 1 sits at the new r_max; the leak band is r > r_max - 4
(u3radial.Radial.observables).  Solver, window test, T-cal stencil and the R-ray direct solve are those of
b3_scan (unchanged).
V1c covers only the central sign change of S whose bracket has the most negative T-cal in V1b (selected by
'analyse V1b', written to verify_V1b.json['V1c_selection']).

Run:  python3 verify_v1.py solve V1a      (4 workers; per-point files; resumable)
      python3 verify_v1.py analyse V1a    (-> verify_V1a.json; R-ray direct solves, cached, 4 workers)
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import sys, json, time, math
import numpy as np
from multiprocessing import Pool
import b3_scan as B
import verify_common as V

MB = 1.0     # m_bulk at lam = 1


def S_for(run):
    S = V.select_S()
    if run == 'V1c':
        sel = json.load(open(os.path.join(V.HERE, 'verify_V1b.json')))['V1c_selection']
        S = [c for c in S if c['index'] == sel['index']]
    return S


def solve_task(args):
    run, i, j = args
    if V.load(run, i, j) is not None:
        return run, i, j, 'exists'
    Ro = V.radial('orig'); Rn = V.radial(run)
    xo = V.load('orig', i, j)[1]
    x0 = V.pad(Ro, xo, Rn)
    t = time.time()
    o, x = B.solve_point(Rn, i * B.DK, j * B.DQ, x0)
    o.update(i=i, j=j, run=run, dr=Rn.dr, rmax=Rn.rmax, warm_from='original (dr=0.1, r_max=20) padded with vacuum',
             omega_over_mbulk=o['omega'] / MB, in_window=B.in_window(o, MB), seconds=time.time() - t)
    V.save(run, i, j, o, x)
    print(f'[{run}] ({i * B.DK:.2f},{j * B.DQ:.1f}) E={o["E"]:.9f} I={o["I"]:.5f} w/m={o["omega_over_mbulk"]:.5f} '
          f'leak={o["leak"]:.1e} rq={o["r_charge_rms"]:.4f} nit={o["nit"]} {o["message"][:30]} {o["seconds"]:.0f}s', flush=True)
    return run, i, j, 'done'


def ray_file(run, kk, qq):
    d = os.path.join(V.FIELDS, run + '_rays'); os.makedirs(d, exist_ok=True)
    return os.path.join(d, f'{kk!r}_{qq!r}.json')


def ray_task(args):
    run, kk, qq, near = args
    f = ray_file(run, kk, qq)
    if os.path.exists(f):
        return
    Rn = V.radial(run)
    x0 = V.load(run, *near)[1]
    o, _ = B.solve_point(Rn, kk, qq, x0)
    o['warm_from_ij'] = list(near)
    json.dump(o, open(f + '.tmp', 'w'), default=float); os.replace(f + '.tmp', f)


def sign_change_eval(c, win, sol_keys):
    (i1, j1), (i2, j2) = V.ij_of(c['between'][0]), V.ij_of(c['between'][1])
    out = dict(index=c['index'], role=c['role'], between=c['between'], orig_k_star=c['k_star'], orig_q_star=c['q_star'],
               orig_omega_star_over_mbulk=c['omega_star_over_mbulk'], orig_flags=c['flags'], orig_f2_direct=c['f2_direct'])
    pts = {}
    for ij in ((i1, j1), (i2, j2)):
        o = win.get(ij)
        pts[ij] = None if o is None else B.tcal(win, *ij)
    out['bracket_in_window'] = all(win.get(ij) is not None for ij in pts)
    if not out['bracket_in_window']:
        out.update(persists=False, reason='a bracketing point left the window'); return out, None
    Ta, Tb = pts[(i1, j1)][0], pts[(i2, j2)][0]
    flags = sorted(set(pts[(i1, j1)][3] + pts[(i2, j2)][3]))
    out.update(Tcal=[Ta, Tb], flags=flags, central=not any('one-sided' in f or 'no ' in f for f in flags))
    if Ta is None or Tb is None or np.sign(Ta) == np.sign(Tb) or Ta == 0:
        out.update(persists=False, reason='no T-cal sign change at the bracketing points'); return out, None
    t = Ta / (Ta - Tb)
    oa, ob = win[(i1, j1)], win[(i2, j2)]
    ks = (i1 + t * (i2 - i1)) * B.DK; qs = (j1 + t * (j2 - j1)) * B.DQ
    out.update(persists=True, k_star=ks, q_star=qs, omega_star_over_mbulk=(oa['omega'] + t * (ob['omega'] - oa['omega'])) / MB,
               r_q_star=oa['r_charge_rms'] + t * (ob['r_charge_rms'] - oa['r_charge_rms']),
               leak_max_bracket=max(oa['leak'], ob['leak']), omega_lt_m_both=bool(oa['omega'] < MB and ob['omega'] < MB))
    tasks = []
    for u in (0.97, 1.0, 1.03):
        kk, qq = ks / u, qs / u
        near = min(sol_keys, key=lambda ij: (ij[0] * B.DK - kk) ** 2 + (ij[1] * B.DQ - qq) ** 2)
        tasks.append((kk, qq, near, u))
    return out, tasks


def analyse(run):
    S = S_for(run)
    pts = V.points_for(S)
    sol = {}
    for ij in pts:
        p = V.load(run, *ij)
        assert p is not None, (run, ij)
        sol[ij] = p[0]
    win = {ij: o for ij, o in sol.items() if o['in_window']}
    rec = V.orig_records()
    point_rows = []
    for ij in pts:
        o = sol[ij]; r = rec[ij]
        T, dEk, dEq, fl = B.tcal(win, *ij) if ij in win else (None, None, None, ['out of window'])
        row = dict(k=ij[0] * B.DK, q=ij[1] * B.DQ, i=ij[0], j=ij[1], E=o['E'], T=o['T'], I_q=o['I'],
                   omega_over_mbulk=o['omega'] / MB, leak=o['leak'], r_charge_rms=o['r_charge_rms'], alpha=o['alpha'],
                   Tcal=T, Tcal_flags=fl, Tcal_envelope=o['T'] - (o['k'] ** 2 + o['omega'] ** 2) * o['I'],
                   in_window=o['in_window'], success=o['success'], message=o['message'], nit=o['nit'],
                   grad_max=o['grad_max'], r_core=o['r_core'],
                   orig=dict(E=r['E'], T=r['T'], I_q=r['I'], omega_over_mbulk=r['omega_over_mbulk'], leak=r['leak'],
                             r_charge_rms=r['r_charge_rms'], alpha=r['alpha'], Tcal=r.get('Tcal'),
                             Tcal_envelope=r.get('Tcal_envelope')))
        point_rows.append(row)
    scs = []; ray_tasks = []
    for c in S:
        out, tasks = sign_change_eval(c, win, list(sol))
        scs.append(out)
        if tasks:
            out['_tasks'] = tasks
            ray_tasks += [(run, kk, qq, near) for (kk, qq, near, u) in tasks]
    with Pool(int(os.environ.get('VERIFY_WORKERS', 4))) as pool:
        list(pool.imap_unordered(ray_task, ray_tasks, chunksize=1))
    for out in scs:
        tasks = out.pop('_tasks', None)
        if not tasks:
            continue
        Ed = {}; conv = True; rays = []
        for (kk, qq, near, u) in tasks:
            o = json.load(open(ray_file(run, kk, qq)))
            Ed[u] = u * o['E']; conv &= o['success']
            rays.append(dict(u=u, k=kk, q=qq, E=o['E'], success=o['success'], warm_from=near, in_window=B.in_window(o, MB)))
        f2 = (Ed[1.03] - 2 * Ed[1.0] + Ed[0.97]) / 0.03 ** 2
        out.update(f2_direct=f2, direct_converged=bool(conv), ray=rays, stable_R_direct=bool(f2 > 0))
        n = max(1, math.ceil(3 * out['r_q_star'] * out['k_star'] - 1e-12))
        Req = n / out['k_star']
        out.update(A1_n=n, R_eq=Req, R_eq_over_r_q=Req / out['r_q_star'], Q=2 * np.pi * Req * out['q_star'],
                   d2E_dR2=2 * np.pi * f2 / Req)
        out['A4_1_pass'] = bool(out['central'] and out['stable_R_direct'] and out['leak_max_bracket'] < B.LEAK_MAX
                                and out['omega_lt_m_both'])
    res = dict(run=run, dr=V.RUNS[run][0], rmax=V.RUNS[run][1], n_points=len(pts), n_in_window=len(win),
               points=point_rows, sign_changes=scs,
               n_not_converged=sum(not o['success'] for o in sol.values()))
    if run == 'V1b':
        cand = [s for s in scs if s['role'] == 'central' and s.get('persists') and s.get('central')]
        rule = 'among the 14 central sign changes of S that persist in V1b with central differences'
        if not cand:
            cand = [s for s in scs if s['role'] == 'central' and s.get('Tcal') and None not in s['Tcal']]
            rule = 'no central sign change persists in V1b; among all 14 central ones with defined T-cal'
        if cand:
            best = min(cand, key=lambda s: min(s['Tcal']))
            res['V1c_selection'] = dict(index=best['index'], between=best['between'], Tcal_V1b=best['Tcal'],
                                        rule=rule + ': the most negative T-cal at a bracketing point')
    json.dump(res, open(os.path.join(V.HERE, f'verify_{run}.json'), 'w'), indent=1, default=float)
    print(f'[{run}] {len(pts)} points, {len(win)} in window; sign changes persisting: '
          f'{sum(bool(s.get("persists")) for s in scs)}/{len(scs)}; A.4(1)-type pass: {sum(bool(s.get("A4_1_pass")) for s in scs)}', flush=True)
    for s in scs:
        print('  ', s['index'], s['role'], s['between'], 'Tcal', s.get('Tcal'), 'persists', s.get('persists'),
              'central', s.get('central'), 'f2', s.get('f2_direct'), 'n', s.get('A1_n'), s.get('reason', ''), flush=True)
    if 'V1c_selection' in res:
        print('  V1c selection:', res['V1c_selection'], flush=True)


if __name__ == '__main__':
    cmd, run = sys.argv[1], sys.argv[2]
    if cmd == 'solve':
        pts = V.points_for(S_for(run))
        print(f'[{run}] {len(pts)} points: {pts}', flush=True)
        with Pool(int(os.environ.get('VERIFY_WORKERS', 4))) as pool:
            list(pool.imap_unordered(solve_task, [(run, i, j) for (i, j) in pts], chunksize=1))
        print(f'[{run}] solve done', flush=True)
    elif cmd == 'analyse':
        analyse(run)
