"""E1d point-level convergence ladder (added by the resumed run; not preregistered).
Does the production call at a single (A, sigma, k) point converge as dx -> 0?
Points: 24 of the coarse points whose call changed between dx = 0.1 and dx = 0.05
(e1d_dxcheck.json), plus 8 where it did not, chosen with a fixed seed. Each is run at
dx = 0.025 and dx = 0.0125 (dt = 0.4 dx); the dx = 0.1 and 0.05 calls are taken from the stored runs.
Resumable: results are appended to e1d_dxladder.jsonl.
Usage: python e1d_dxladder.py [nproc]   Runtime ~10-15 min on 2 processes."""
import sys
import json
import os
import time
import numpy as np
from multiprocessing import Pool
from e1d_extra import run_custom


def _job(a):
    A, s, k, dx = a
    r = run_custom(A, s, k, dx=dx)
    return r


if __name__ == "__main__":
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    co = {(r["A"], r["sigma"], r["k"]): r for r in json.load(open("e1d_coarse.json"))["runs"]}
    dc = json.load(open("e1d_dxcheck.json"))["runs"]
    dis = [r for r in dc if r["produced"] != co[(r["A"], r["sigma"], r["k"])]["produced"]]
    agr = [r for r in dc if r["produced"] == co[(r["A"], r["sigma"], r["k"])]["produced"]]
    rng = np.random.default_rng(31)
    pts = [dis[i] for i in sorted(rng.choice(len(dis), size=min(24, len(dis)), replace=False))]
    pts += [agr[i] for i in sorted(rng.choice(len(agr), size=8, replace=False))]
    jobs = [(p["A"], p["sigma"], p["k"], dx) for dx in (0.025, 0.0125) for p in pts]
    out = "e1d_dxladder.jsonl"
    done = set()
    if os.path.exists(out):
        for l in open(out):
            try:
                r = json.loads(l)
                done.add((r["A"], r["sigma"], r["k"], r["dx"]))
            except json.JSONDecodeError:
                pass
    todo = [j for j in jobs if j not in done]
    todo.sort(key=lambda j: -(j[1] * 8 + 100) / j[3] ** 2)
    print(f"{len(jobs)} jobs, {len(todo)} to run", flush=True)
    t0 = time.time()
    with Pool(nproc) as pool, open(out, "a") as f:
        for i, r in enumerate(pool.imap_unordered(_job, todo, chunksize=1)):
            f.write(json.dumps(r) + "\n")
            f.flush()
            print(f"{i + 1}/{len(todo)} A={r['A']} s={r['sigma']} k={r['k']} dx={r['dx']} -> {r['produced']} "
                  f"{time.time() - t0:.0f} s", flush=True)
    rs = [json.loads(l) for l in open(out)]
    lad = {}
    for r in rs:
        lad.setdefault((r["A"], r["sigma"], r["k"]), {})[r["dx"]] = r["produced"]
    dmap = {(r["A"], r["sigma"], r["k"]): r["produced"] for r in dc}
    rows = []
    for p in pts:
        key = (p["A"], p["sigma"], p["k"])
        rows.append({"A": key[0], "sigma": key[1], "k": key[2], "E_over_2M": p["E_over_2M"],
                     "dx0.1": co[key]["produced"], "dx0.05": dmap[key],
                     "dx0.025": lad.get(key, {}).get(0.025), "dx0.0125": lad.get(key, {}).get(0.0125)})
    agree = lambda a, b: [r[a] == r[b] for r in rows if r[a] is not None and r[b] is not None]
    summ = {"n_points": len(rows), "n_changed_0.1_vs_0.05": len([r for r in rows if r["dx0.1"] != r["dx0.05"]]),
            "agree_0.1_0.05": float(np.mean(agree("dx0.1", "dx0.05"))),
            "agree_0.05_0.025": float(np.mean(agree("dx0.05", "dx0.025"))),
            "agree_0.025_0.0125": float(np.mean(agree("dx0.025", "dx0.0125"))),
            "agree_0.05_0.0125": float(np.mean(agree("dx0.05", "dx0.0125")))}
    json.dump({"rows": rows, "summary": summ, "runtime_s": time.time() - t0}, open("e1d_dxladder.json", "w"), indent=1)
    print(json.dumps(summ, indent=1))
