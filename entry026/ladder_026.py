# Exact absorption ladder for every (height, character) cell. Model values only; no data.
import math, time, sys, json
from predict_026 import corr_at, OTHERS
ln2 = math.log(2)
HEIGHTS = {'E':   dict(rng=(1e12, 1.02e12), nodes=2),
           'R64': dict(L=63.5*ln2), 'R128': dict(L=127.5*ln2)}
h, q, kmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
out = {}
t = time.time()
for k in range(0, kmax+1):
    P = OTHERS[q][:k]
    c = corr_at(q, P, **HEIGHTS[h])
    out[k] = c
    print(f"{h} q={q} through {P[-1] if P else '-':>2}: {c:+.8f}" + (f"  step {c-out[k-1]:+.3e}" if k else "") + f"  [{time.time()-t:.0f}s]", flush=True)
json.dump({'h': h, 'q': q, 'P': OTHERS[q][:kmax], 'corr': out}, open(f"ladder_{h}_{q}.json", 'w'))
