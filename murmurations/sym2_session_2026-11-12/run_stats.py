"""Compute per-prime pieces for one (table, K, window, range) and write a CSV.
Usage: python3 -I run_stats.py <table_prefix> <K> <window C|N> <xmax|c1> <out.csv> [truncated]
'c1' means p <= K^2 (c = 1 range). 'truncated' marks rows whose t-range is partial."""
import sys, glob, csv
import numpy as np
from math import sqrt
from sym2lib import window, per_prime, Xof

prefix, K, kind, rng, outf = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
trunc = len(sys.argv) > 6 and sys.argv[6] == "truncated"
X = Xof(K)
pmax = K * K if rng == "c1" else float(rng) * X
ks, w = window(K, kind)

rows = []
for f in sorted(glob.glob(prefix + "_w*.npz")):
    z = dict(np.load(f))
    for i, p in enumerate(z["ps"]):
        p = int(p)
        if p > pmax: continue
        a, b = z["offs"][i], z["offs"][i + 1]
        tlo = int(z["tlos"][i])
        t = np.arange(tlo, 2 * p, dtype=np.int64)
        r = per_prime(p, t, z["vals"][a:b], ks, w)
        r.update(p=p, x=p / X, X=X, K=K, window=kind, tlo=tlo, truncated=int(trunc or tlo > 0))
        rows.append(r)
rows.sort(key=lambda r: r["p"])
keys = ["K", "window", "p", "x", "X", "tlo", "truncated"] + sorted(k for k in rows[0] if "_c" in k)
with open(outf, "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=keys); wr.writeheader()
    for r in rows: wr.writerow({k: r[k] for k in keys})
print(f"wrote {len(rows)} rows to {outf}")
