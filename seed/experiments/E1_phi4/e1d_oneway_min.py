"""E1d/E1e: are the lowest-energy producers of the one-way coarse grid (e1d_coarse_oneway.jsonl)
reproduced at finer resolution? Reruns the 6 lowest-E producing points at dx = 0.05 and 0.025
(dt = 0.4 dx) and runs each as a single packet at dx = 0.05.
Writes e1d_oneway_min.json.  Runtime ~1-2 min on 2 processes."""
import json
import time
from multiprocessing import Pool
from e1d_extra import run_custom


def _job(a):
    A, s, k, dx, single = a
    r = run_custom(A, s, k, dx=dx, single=single, oneway=True)
    return {kk: r[kk] for kk in ("A", "sigma", "k", "dx", "single", "produced", "E_over_2M", "N_lin")}


if __name__ == "__main__":
    t0 = time.time()
    ow = [json.loads(l) for l in open("e1d_coarse_oneway.jsonl")]
    pts = sorted([r for r in ow if r["produced"]], key=lambda r: r["E_over_2M"])[:6]
    jobs = [(p["A"], p["sigma"], p["k"], dx, False) for p in pts for dx in (0.05, 0.025)]
    jobs += [(p["A"], p["sigma"], p["k"], 0.05, True) for p in pts]
    with Pool(2) as pool:
        res = pool.map(_job, jobs, chunksize=1)
    rows = []
    for p in pts:
        row = {"A": p["A"], "sigma": p["sigma"], "k": p["k"], "E_over_2M": p["E_over_2M"], "N_lin": p["N_lin"],
               "dx0.1": p["produced"]}
        for r in res:
            if (r["A"], r["sigma"], r["k"]) == (p["A"], p["sigma"], p["k"]):
                row[("single_dx" if r["single"] else "dx") + str(r["dx"])] = r["produced"]
        rows.append(row)
        print(row)
    rep = [r for r in rows if r.get("dx0.05") and r.get("dx0.025")]
    best = min(rep, key=lambda r: r["E_over_2M"]) if rep else None
    json.dump({"rows": rows, "lowest_reproduced_at_dx0.05_and_0.025": best, "runtime_s": time.time() - t0},
              open("e1d_oneway_min.json", "w"), indent=1)
    print("lowest reproduced:", best, f"{time.time() - t0:.0f} s")
