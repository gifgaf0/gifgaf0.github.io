"""E1b box-size check (added by the resumed run; not preregistered).
Bisects v_c and the first two-bounce window edges (to 1e-5, as in e1b_dtcheck.py) at dx = 0.05,
dt = 0.01 for larger physical boxes and wider absorbing layers, to test whether radiation
reflected by the absorbing layer shifts v_c. Reference (Lphys, W) = (40, 30) at the same dx, dt:
v_c = 0.260079, window 1 = [0.192597, 0.203464] (e1b_dtcheck.json).
Writes e1b_boxcheck.json.  Runtime ~3 min on 2 processes."""
import json
import time
from multiprocessing import Pool
import e1b_kkbar as E

BOXES = [(100.0, 60.0), (200.0, 100.0)]
TRANS = {"v_c": (0.25975, 0.2606), "w1_lo": (0.19235, 0.1935), "w1_hi": (0.2030, 0.2042)}


def pred(name, r):
    """True on the high-v side of the transition."""
    if name == "v_c":
        return r["label"] == 1
    if name == "w1_lo":
        return r["label"] == 2
    return r["label"] != 2


def bisect(job):
    (L, W), name = job
    lo, hi = TRANS[name]
    E.LPHYS, E.WSP, E.CFL = L, W, 0.2
    a, b = lo, hi
    while b - a > 1e-5:
        m = 0.5 * (a + b)
        if pred(name, E.collide(m, 12.0, 0.05)):
            b = m
        else:
            a = m
    return {"Lphys": L, "W": W, "dx": 0.05, "dt": 0.01, "transition": name, "v": 0.5 * (a + b)}


if __name__ == "__main__":
    t0 = time.time()
    jobs = [(b, t) for b in BOXES for t in TRANS]
    with Pool(2) as p:
        res = p.map(bisect, jobs, chunksize=1)
    ref = {"v_c": 0.26007871093749996, "w1_lo": 0.1925970703125, "w1_hi": 0.20346406250000004}
    for r in res:
        r["shift_vs_box40"] = r["v"] - ref[r["transition"]]
        print(r)
    json.dump({"reference_box40_W30_dx0.05_dt0.01": ref, "cases": res, "runtime_s": time.time() - t0},
              open("e1b_boxcheck.json", "w"), indent=1)
    print(f"total {time.time() - t0:.0f} s")
