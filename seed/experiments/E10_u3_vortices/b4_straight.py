"""
E10 Route B, B4 (PREREG_B4 §3 'Starts'): re-solve the straight string at the interpolated (k*, q*) of sign
change #66 (verify_results.json V1b) on the V1b radial grid (dr = 0.05, r_max = 40), warm-started from V1b's
bracketing solution.  Label: Exploration.

The V1b field files were not committed (verify_common: FIELDS under /tmp).  They are regenerated here by
replaying exactly the recorded chain (same instrument, same options; nothing new):
  orig grid (dr = 0.1, r_max = 20): row k = 0, q = 0 .. 24.8 from the abelian-Higgs initial, then (i, 248) from
  (i-1, 248) for i = 1..6 (asserted against b3_results.json 'warm_from');
  V1b: (5, 248) and (6, 248) from the orig solutions padded with vacuum (verify_common.pad);
  (k*, q*): from V1b (6, 248), as the V1b R-ray u = 1 solve did (warm_from [6, 248]).
Each regenerated E is compared with the recorded value.  Writes b4_fields/straight/*.npz and b4_straight.json.
Run: python3 b4_straight.py > log_b4_straight.txt
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import json, time
import numpy as np
import b3_scan as B
import verify_common as V

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, 'b4_fields', 'straight'); os.makedirs(D, exist_ok=True)
J = 248


def f(run, i, j):
    return os.path.join(D, f'{run}_{i}_{j}.npz')


def save(run, i, j, o, x):
    p = f(run, i, j); np.savez(p + '.tmp.npz', x=x, o=json.dumps(o, default=float)); os.replace(p + '.tmp.npz', p)


def load(run, i, j):
    p = f(run, i, j)
    if not os.path.exists(p):
        return None
    z = np.load(p); return json.loads(str(z['o'])), z['x']


def sc66():
    v = json.load(open(os.path.join(HERE, 'verify_results.json')))['V1b']
    s = [s for s in v['sign_changes'] if s['index'] == 66][0]
    pts = {(p['i'], p['j']): p for p in v['points']}
    return s, pts


def main():
    t0 = time.time()
    rec = V.orig_records()
    s, pts = sc66()
    assert [V.ij_of(b) for b in s['between']] == [(5, J), (6, J)]
    Ro = V.radial('orig')
    x = None
    for j in range(J + 1):
        p = load('orig', 0, j)
        if p is not None:
            x = p[1]; continue
        if j > 0:
            assert rec[(0, j)]['warm_from'] == f'(0.00,{(j - 1) * B.DQ:.2f})'
        x0 = Ro.initial(alpha=B.ALPHA0) if j == 0 else x
        o, x = B.solve_point(Ro, 0.0, j * B.DQ, x0)
        o['rel_dE_vs_orig'] = o['E'] / rec[(0, j)]['E'] - 1 if rec[(0, j)]['E'] else o['E'] - rec[(0, j)]['E']
        save('orig', 0, j, o, x)
        if j % 20 == 0 or j == J:
            print(f'orig row0 j={j} E={o["E"]:.12f} rel dE vs B3 {o["rel_dE_vs_orig"]:.1e} ({time.time() - t0:.0f} s)', flush=True)
    for i in range(1, 7):
        if load('orig', i, J) is None:
            assert rec[(i, J)]['warm_from'] == f'({(i - 1) * B.DK:.2f},{J * B.DQ:.2f})'
            o, x = B.solve_point(Ro, i * B.DK, J * B.DQ, load('orig', i - 1, J)[1])
            o['rel_dE_vs_orig'] = o['E'] / rec[(i, J)]['E'] - 1
            save('orig', i, J, o, x)
            print(f'orig ({i},{J}) E={o["E"]:.12f} rel dE vs B3 {o["rel_dE_vs_orig"]:.1e}', flush=True)
    Rn = V.radial('V1b')
    for i in (5, 6):
        if load('V1b', i, J) is None:
            o, x = B.solve_point(Rn, i * B.DK, J * B.DQ, V.pad(Ro, load('orig', i, J)[1], Rn))
            o['rel_dE_vs_V1b'] = o['E'] / pts[(i, J)]['E'] - 1
            save('V1b', i, J, o, x)
            print(f'V1b ({i},{J}) E={o["E"]:.12f} rel dE vs V1b record {o["rel_dE_vs_V1b"]:.1e} nit={o["nit"]}', flush=True)
    ks, qs = s['k_star'], s['q_star']
    if load('star', 0, 0) is None:
        o, x = B.solve_point(Rn, ks, qs, load('V1b', 6, J)[1])
        save('star', 0, 0, o, x)
    o, x = load('star', 0, 0)
    Eray = [r['E'] for r in s['ray'] if r['u'] == 1.0][0]
    out = dict(k_star=ks, q_star=qs, dr=Rn.dr, rmax=Rn.rmax, warm_from='V1b (6,248) regenerated',
               star=o, E_ray_u1_recorded=Eray, rel_dE_vs_ray=o['E'] / Eray - 1,
               V1b_regen={str(i): load('V1b', i, J)[0]['rel_dE_vs_V1b'] for i in (5, 6)},
               orig_regen_max_rel=max(abs(load('orig', i, j)[0]['rel_dE_vs_orig'])
                                      for (i, j) in [(0, jj) for jj in range(J + 1)] + [(ii, J) for ii in range(1, 7)]),
               seconds=time.time() - t0)
    json.dump(out, open(os.path.join(HERE, 'b4_straight.json'), 'w'), indent=1, default=float)
    print(f'star: E={o["E"]:.12f} (V1b ray u=1: {Eray:.12f}, rel {out["rel_dE_vs_ray"]:.1e}) I={o["I"]:.6f} '
          f'omega={o["omega"]:.6f} alpha={o["alpha"]:.6f} rq={o["r_charge_rms"]:.5f} T={o["T"]:.9f}', flush=True)


if __name__ == '__main__':
    main()
