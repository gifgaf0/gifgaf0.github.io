# Random-start arms: shift from the local density at 2^(b-0.5) to the uniform-in-y average over
# [2^(b-1), 2^b) (4-node Gauss-Legendre in log y, dy weight), as a function of the absorbed set.
import math, sys, json
from predict_026 import corr_at, OTHERS
ln2 = math.log(2)
b, q = int(sys.argv[1]), int(sys.argv[2])
out = {}
for k in (0, 4, 5, 6):
    P = OTHERS[q][:k]
    loc = corr_at(q, P, L=(b-0.5)*ln2)
    uni = corr_at(q, P, rng=(2.0**(b-1), 2.0**b), nodes=4, uniform=True)
    out[k] = (loc, uni)
    print(f"R{b} q={q} through {P[-1] if P else '-':>2}: local {loc:+.9f} uniform {uni:+.9f} shift {uni-loc:+.3e}", flush=True)
json.dump({str(k): v for k, v in out.items()}, open(f"ushift_R{b}_{q}.json", "w"))
