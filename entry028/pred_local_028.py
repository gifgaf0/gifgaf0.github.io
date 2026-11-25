"""pred_local_028.py q KIND -- archived predictor's LOCAL correlation at each of the 4 band nodes
(for the exact discrete 2,000-stratum average via a cubic in log y through the node values)."""
import os as _os; PRED = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "pred")
import sys, json, math, time
from predict_026 import marg, corr, OTHERS
from band_028 import nodes
q, kind = int(sys.argv[1]), sys.argv[2]
P = {"216": [], "full": OTHERS[q][:7]}[kind]; Q = q
for p in P: Q *= p
ys, ws = nodes(4); vals = []
for y in ys:
    t = time.time(); rq, Mx = marg(Q, q, math.log(y)); vals.append(corr(q, Mx / Mx.sum(), rq))
    print(q, kind, f"{y:.6e}", repr(vals[-1]), f"{time.time()-t:.0f}s", flush=True)
avg = sum(w * v for w, v in zip(ws, vals))
json.dump(dict(q=q, kind=kind, nodes=ys, weights=ws, local=vals, gl4=avg), open(f"{PRED}/local_{kind}_q{q}.json", "w"), indent=1)
print("gl4 average", repr(avg))
