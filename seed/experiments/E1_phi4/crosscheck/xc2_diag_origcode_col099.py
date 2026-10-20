"""Diagnosis: ORIGINAL E1c code (unmodified copy) on the omega = 0.99 column near DSV's producing
point, at (dx, dt) = (0.1, 0.04) [original], (0.1, 0.02) and (0.05, 0.02)."""
import sys, json, time
import numpy as np
import e1c_dsv as E
vs = [round(0.38 + 0.01 * i, 2) for i in range(11)]
out = []
for dx, cfl in [(0.1, 0.4), (0.1, 0.2), (0.05, 0.4)]:
    E.CFL = cfl
    row = []
    for v in vs:
        try:
            r = E.run_dsv(0.99, v, dx)
            row.append([v, r['produced_dsv'], r['pair_continuously_present_since']])
        except Exception as ex:
            row.append([v, None, str(ex)])
    out.append(dict(dx=dx, dt=dx * cfl, rows=row))
    print(dx, dx * cfl, [(a, b) for a, b, c in row], flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
