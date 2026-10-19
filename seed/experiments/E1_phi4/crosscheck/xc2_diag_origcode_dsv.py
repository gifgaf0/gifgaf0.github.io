"""Diagnosis: run the ORIGINAL E1c code (copied, unmodified) for the DSV example point at other
resolutions / time steps, to see whether its own call is robust."""
import sys, json, time
import numpy as np
import e1c_dsv as E
cases = [(0.1, 0.4), (0.05, 0.4), (0.1, 0.2), (0.05, 0.2), (0.025, 0.4), (0.1, 0.1)]
out = []
for dx, cfl in cases:
    E.CFL = cfl
    t0 = time.time()
    r = E.run_dsv(0.99, 0.43, dx)
    row = dict(dx=dx, dt=dx * cfl, produced_dsv=r['produced_dsv'], survives=r['survives_to_1.5T'],
               since=r['pair_continuously_present_since'], intervals_T=r['final_positive_intervals_T'][:3],
               first_any=float(np.argmax(np.array(r['npairs_series']) > 0) * 10.0) if max(r['npairs_series']) > 0 else None,
               wall=time.time() - t0)
    out.append(row)
    print(json.dumps(row), flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
