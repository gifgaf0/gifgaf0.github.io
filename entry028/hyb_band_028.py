"""hyb_band_028.py NODE_INDEX [NNODES] -- Q0 = 60 fixed-lambda hybrid at one band node (all three characters).
c_hyb = c_Lichtblau(Q = 60*7*11*13*17*19) + sum_{k=2..5} [c_k(all) - c_k(<=19)] + MC tail_6.
Deterministic truncation N (admissible steps): k=2: 900, 3: 400, 4: 170, 5: 110; check run at N-30 for k=5.
MC: 600,000 antithetic pairs x 16 start residues, seed = int(sha256('E028:hyb:k6:n{NNODES}:node{i}'))."""
import os as _os; PRED = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "pred")
import sys, json, math, time, hashlib, os
import numpy as np
from tb_028 import terms, lichtblau, CHI, mc_tail_multi
from band_028 import nodes
i = int(sys.argv[1]); nn = int(sys.argv[2]) if len(sys.argv) > 2 else 4
ys, ws = nodes(nn); y = ys[i]
names = ["chi-4", "chi-3", "leg5"]; P19 = [7, 11, 13, 17, 19]
N = {2: 900, 3: 400, 4: 170, 5: 110}
fn = f"{PRED}/hyb_n{nn}_node{i}.json"
res = json.load(open(fn)) if os.path.exists(fn) else dict(node=i, nnodes=nn, y=y, w=ws[i], N=N)
def save(): json.dump(res, open(fn, "w"), indent=1)
t0 = time.time(); log = lambda *a: print(f"[node {i} {time.time()-t0:6.0f}s]", *a, flush=True)
if "lich19" not in res:
    res["lich19"] = {n: lichtblau(60 * 7 * 11 * 13 * 17 * 19, CHI[n], y) for n in names}; save(); log("lich19", res["lich19"])
for k in (2, 3, 4, 5):
    if f"full{k}" not in res:
        res[f"full{k}"] = terms(60, names, y, k, N[k]); save(); log(f"full{k}", res[f"full{k}"])
    if f"r19_{k}" not in res:
        res[f"r19_{k}"] = terms(60, names, y, k, N[k], set(P19)); save(); log(f"r19_{k}", res[f"r19_{k}"])
if "full5_Nm30" not in res and i == nn - 1:
    res["full5_Nm30"] = terms(60, names, y, 5, N[5] - 30); save(); log("full5_Nm30", res["full5_Nm30"])
if "mc6" not in res and nn == 4:
    seed = int(hashlib.sha256(f"E028:hyb:k6:n{nn}:node{i}".encode()).hexdigest()[:16], 16)
    arr = mc_tail_multi(60, names, y, 6, 600_000, {19: P19}, batch=100_000, seed=seed)
    res["mc6"] = {n: [float(arr[(19, n)].mean()), float(arr[(19, n)].std(ddof=1) / math.sqrt(len(arr[(19, n)]))), len(arr[(19, n)])] for n in names}
    res["mc6_seed"] = seed; save(); log("mc6", res["mc6"])
res["c_hyb_K5"] = {n: res["lich19"][n] + sum(res[f"full{k}"][n] - res[f"r19_{k}"][n] for k in (2, 3, 4, 5)) for n in names}
if "mc6" in res: res["c_hyb_K6"] = {n: res["c_hyb_K5"][n] + res["mc6"][n][0] for n in names}
save(); log("DONE", res.get("c_hyb_K6", res["c_hyb_K5"]))
