"""Diagnosis: ORIGINAL E1c code (unmodified copy) at (0.99, 0.41) for a ladder of (dx, dt)."""
import sys, json
import e1c_dsv as E
out = []
for dx, cfl in [(0.1, 0.4), (0.1, 0.2), (0.1, 0.1), (0.05, 0.4), (0.05, 0.2), (0.025, 0.2)]:
    E.CFL = cfl
    r = E.run_dsv(0.99, 0.41, dx)
    row = dict(dx=dx, dt=dx * cfl, produced_dsv=r['produced_dsv'], since=r['pair_continuously_present_since'],
               intervals_T=r['final_positive_intervals_T'][:2])
    out.append(row); print(json.dumps(row), flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
