"""Robustness of the DSV example point (0.99, 0.43) in the cross-check code: other dx, neighbouring v.
Each run is tracked every 10 time units up to 1.5 T with the report's pair test."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xc_e1c import run
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'xc_e1c_example_variants.json')
db = json.load(open(p)) if os.path.exists(p) else {}
cases = [(0.99, 0.43, 0.1), (0.99, 0.43, 0.05), (0.99, 0.41, 0.08), (0.99, 0.42, 0.08), (0.99, 0.44, 0.08)]
for om, v, dx in cases:
    k = f'{om}_{v}_{dx}'
    if k in db:
        continue
    t0 = time.time()
    r = run(om, v, dx=dx, tmax_fac=1.5, track=True)
    db[k] = {kk: r[kk] for kk in r if kk != 'hist'}
    db[k]['pair_times'] = [h[0] for h in r['hist'] if h[1]]
    json.dump(db, open(p, 'w'), indent=1)
    print(k, db[k]['first_pair_t'], db[k]['pair_at_T'], db[k]['pair_at_end'], f'{time.time()-t0:.0f}s', flush=True)
