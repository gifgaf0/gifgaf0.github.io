"""E1b: separate time-step and grid-spacing errors on v_c and the first window edges.
Bisection (to 1e-5) of three transitions for several (dx, CFL = dt/dx) pairs.
Writes e1b_dtcheck.json.  Runtime ~5 min on 2 cores."""
import json
import time
import numpy as np
from multiprocessing import Pool
import e1b_kkbar as E

CASES = [(0.05, 0.4), (0.05, 0.2), (0.05, 0.1), (0.025, 0.4), (0.025, 0.2), (0.1, 0.4), (0.1, 0.1)]
# (name, v_lo, v_hi, predicate true at v_hi side)
TRANS = [("v_c", 0.25975, 0.2606, lambda r: r["label"] == 1),
         ("w1_lo", 0.19235, 0.1935, lambda r: r["label"] == 2),
         ("w1_hi", 0.2030, 0.2042, lambda r: r["label"] != 2)]


def bisect(case):
    dx, cfl = case
    E.CFL = cfl
    out = {}
    for name, lo, hi, pred in TRANS:
        a, b = lo, hi
        while b - a > 1e-5:
            m = 0.5 * (a + b)
            if pred(E.collide(m, 12.0, dx)):
                b = m
            else:
                a = m
        out[name] = 0.5 * (a + b)
    return {"dx": dx, "cfl": cfl, "dt": dx * cfl, **out}


if __name__ == "__main__":
    t0 = time.time()
    with Pool(2) as p:
        res = p.map(bisect, CASES, chunksize=1)
    for r in res:
        print(r)
    json.dump({"cases": res, "runtime_s": time.time() - t0}, open("e1b_dtcheck.json", "w"), indent=1)
    print(f"total {time.time() - t0:.0f} s")
