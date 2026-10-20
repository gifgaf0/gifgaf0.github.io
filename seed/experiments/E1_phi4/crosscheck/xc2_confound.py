"""Amplitude confound of the E1d matched-energy speed test.  For the original coarse grid (data file
e1d_coarse.json + e1d_single.json) and for the FD6 cross-check coarse grid: mean amplitude per v_g in each
energy band, and the speed dependence of production at FIXED amplitude (E > 2M).  Writes xc2_confound.json."""
import json, os, glob
import numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); ORIG = os.path.dirname(HERE)
key = lambda r: (round(r['A'], 4), round(r['sigma'], 4), round(r['k'], 4))
orig = json.load(open(os.path.join(ORIG, 'e1d_coarse.json')))['runs']
single = {key(r): r['produced'] for r in json.load(open(os.path.join(ORIG, 'e1d_single.json')))['runs']}
fd6 = [json.loads(l) for p in sorted(glob.glob(os.path.join(HERE, 'xc_e1d_coarse_w*.jsonl'))) for l in open(p)]
out = {}
for name, runs, pk in [('original', orig, 'produced'), ('fd6', fd6, 'prod')]:
    A = np.array([r['A'] for r in runs]); k = np.array([r['k'] for r in runs]); E = np.array([r['E_over_2M'] for r in runs])
    P = np.array([r[pk] for r in runs]); vg = np.round(k / np.sqrt(k * k + 2), 4)
    res = dict(bands={}, fixed_A={})
    for lo, hi in [(2, 4), (4, 8), (8, 16)]:
        m = (E >= lo) & (E < hi)
        xs = [v for v in sorted(set(vg)) if (m & (vg == v)).sum() >= 3]
        res['bands'][f'{lo}-{hi}'] = dict(vg=xs, mean_A=[round(float(A[m & (vg == v)].mean()), 3) for v in xs],
                                          frac=[round(float(P[m & (vg == v)].mean()), 3) for v in xs],
                                          rho_A_vs_vg=float(spearmanr(xs, [A[m & (vg == v)].mean() for v in xs])[0]))
    for a in sorted(set(A)):
        m = (A == a) & (E > 1)
        xs = [v for v in sorted(set(vg)) if (m & (vg == v)).sum() >= 3]
        fs = [float(P[m & (vg == v)].mean()) for v in xs]
        if len(xs) > 2 and len(set(fs)) > 1:
            rho, p = spearmanr(xs, fs)
            res['fixed_A'][str(a)] = dict(n=int(m.sum()), rho=float(rho), p=float(p))
    if name == 'original':
        coll = np.array([r['produced'] and not single.get(key(r), False) for r in runs])
        res['fixed_A_collision_needed'] = {}
        for a in sorted(set(A)):
            m = (A == a) & (E > 1)
            xs = [v for v in sorted(set(vg)) if (m & (vg == v)).sum() >= 3]
            fs = [float(coll[m & (vg == v)].mean()) for v in xs]
            if len(xs) > 2 and len(set(fs)) > 1:
                rho, p = spearmanr(xs, fs)
                res['fixed_A_collision_needed'][str(a)] = dict(rho=float(rho), p=float(p))
    out[name] = res
    sig = {a: v for a, v in res['fixed_A'].items() if v['p'] < 0.05}
    print(name, 'mean A by vg in [2,4):', res['bands']['2-4']['mean_A'], ' fixed-A significant (p<0.05):', sig)
    if 'fixed_A_collision_needed' in res:
        print('   collision-needed fixed-A significant:', {a: v for a, v in res['fixed_A_collision_needed'].items() if v['p'] < 0.05})
json.dump(out, open(os.path.join(HERE, 'xc2_confound.json'), 'w'), indent=1)
