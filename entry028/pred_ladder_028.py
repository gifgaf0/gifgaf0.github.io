"""pred_ladder_028.py q kind nodes -- archived Entry 026 predictor on the Entry 028 band.
kind: 216 (no absorption) | full (absorbed through 19) | r7 (through 7, quadrature check only)."""
import os as _os; PRED = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "pred")
import sys, json, time, math
from predict_026 import corr_at, OTHERS
from band_028 import LO, HI
q, kind, n = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
P = {"216": [], "full": OTHERS[q][:7], "r7": OTHERS[q][:3]}[kind]
t = time.time()
c = corr_at(q, P, rng=(LO, HI), nodes=n, uniform=True)
out = dict(q=q, kind=kind, nodes=n, absorbed=P, corr=c, seconds=round(time.time() - t, 1))
json.dump(out, open(f"{PRED}/ladder_{kind}_q{q}_n{n}.json", "w"), indent=1); print(json.dumps(out), flush=True)
