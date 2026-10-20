"""E1d/E1e robustness of the lowest-quanta producing Gaussian runs (added during the run,
not preregistered).
 1. The 5 producing runs with the smallest N_lin and the 5 with the smallest energy (all
    Gaussian scans) are rerun at dx = 0.05 (dt = 0.02) and as single packets (no collision).
 2. A local grid around the smallest-N_lin producer: A +- 0.025 in steps of 0.005, k +- 0.05
    in steps of 0.01 (11 x 11, same sigma, dx = 0.1).
 3. That producer with x0 shifted over one carrier-phase period (8 shifts).
Writes e1d_probe_min.json.  Runtime ~3-5 min on 2 cores."""
import glob
import json
import time
import numpy as np
from multiprocessing import Pool
import e1d_gauss as G

t0 = time.time()
runs = json.load(open("e1d_coarse.json"))["runs"]
for fn in sorted(f for f in glob.glob("e1d_slice*.json") if not f.endswith("_single.json")):
    runs += json.load(open(fn))["runs"]
prod = sorted([r for r in runs if r["produced"]], key=lambda r: r["N_lin"])
top = []
seen = set()
for r in prod:
    kk = (r["A"], r["sigma"], r["k"])
    if kk not in seen:
        seen.add(kk)
        top.append(r)
    if len(top) == 5:
        break
best = top[0]
topE = []
seenE = set()
for r in sorted([r for r in runs if r["produced"]], key=lambda r: r["E"]):
    kk = (r["A"], r["sigma"], r["k"])
    if kk not in seenE:
        seenE.add(kk)
        topE.append(r)
    if len(topE) == 5:
        break
jobs = []
for r in top + [q for q in topE if (q["A"], q["sigma"], q["k"]) not in seen]:
    jobs.append(("dx0.05", (r["A"], r["sigma"], r["k"], 0.05, False, 0.0)))
    jobs.append(("single", (r["A"], r["sigma"], r["k"], 0.1, True, 0.0)))
for dA in np.round(np.linspace(-0.025, 0.025, 11), 4):
    for dk in np.round(np.linspace(-0.05, 0.05, 11), 4):
        A, k = round(best["A"] + dA, 4), round(best["k"] + dk, 4)
        if k > 0.05:
            jobs.append(("local", (A, best["sigma"], k, 0.1, False, 0.0)))
per = 2 * np.pi * best["k"] / 2.0
for q in range(8):
    jobs.append(("phase", (best["A"], best["sigma"], best["k"], 0.1, False, float(q * per / 8))))


def job(a):
    tag, args = a
    r = G.run_gauss(*args)
    r["tag"] = tag
    r["x0_shift"] = args[5]
    return r


with Pool(2) as p:
    res = p.map(job, jobs, chunksize=2)
out = {"top5_by_N_lin": [{k: r[k] for k in ("A", "sigma", "k", "vg", "E_over_2M", "N_lin")} for r in top],
       "top5_by_E": [{k: r[k] for k in ("A", "sigma", "k", "vg", "E_over_2M", "N_lin")} for r in topE],
       "dx0.05": [{k: r[k] for k in ("A", "sigma", "k", "produced", "E_over_2M", "N_lin")} for r in res if r["tag"] == "dx0.05"],
       "single": [{k: r[k] for k in ("A", "sigma", "k", "produced")} for r in res if r["tag"] == "single"],
       "local_grid_around": {k: best[k] for k in ("A", "sigma", "k")},
       "local": [{k: r[k] for k in ("A", "k", "produced", "E_over_2M", "N_lin")} for r in res if r["tag"] == "local"],
       "phase": [{k: r[k] for k in ("x0_shift", "produced", "E_over_2M")} for r in res if r["tag"] == "phase"],
       "runtime_s": time.time() - t0}
loc = out["local"]
out["local_summary"] = {"n": len(loc), "n_produced": int(sum(r["produced"] for r in loc)),
                        "min_N_lin_producing": min([r["N_lin"] for r in loc if r["produced"]], default=None)}
out["phase_summary"] = {"n": 8, "n_produced": int(sum(r["produced"] for r in out["phase"]))}
json.dump(out, open("e1d_probe_min.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("top5_by_N_lin", "top5_by_E", "dx0.05", "single", "local_summary", "phase_summary")}, indent=1))
As = sorted(set(r["A"] for r in loc))
ks = sorted(set(r["k"] for r in loc))
kd = {(r["A"], r["k"]): r["produced"] for r in loc}
for A in As[::-1]:
    print(f"{A:.3f} " + "".join("#" if kd[(A, k)] else "." for k in ks))
print(f"runtime {time.time() - t0:.0f} s")
