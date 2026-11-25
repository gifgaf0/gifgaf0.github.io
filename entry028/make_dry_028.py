"""make_dry_028.py SEED TARGET OUTDIR -- full-size (N = 2.0e10) synthetic multinomial dry run.
TARGET: 'hyb' (truth = frozen c_hyb) or 'full' (truth = frozen c_full).  Each stratum's lag-1 table is
Multinomial(n = 12,500,000, p_r) with p_r(a,b) = (1 + sum_chi c_chi(y_r) chi(a) chi(b)) / 256 on the 16 units mod 60,
so E[chi(p)chi(p')] = c_chi(y_r) exactly for the three (orthogonal) characters.  Height drift:
c_chi(y_r) = c_216,chi(y_r) * C_target / mean_r c_216,chi (realistic stratum-by-stratum drift).  Lag 2:
Multinomial(n - 1) with Entry 026's arm-E lag-2 values.  Records use the production format and seed rule."""
import os as _os; PRED = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "pred")
import sys, os, json, random, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from read_028 import REC, MAGIC
seed, target, outdir = sys.argv[1:4]
pred = json.load(open(os.path.join(os.path.dirname(__file__), "pred_028.json")))
drift = json.load(open(os.path.join(PRED, "drift_216.json")))
U = np.array([1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59])
CH = {"chi-3": (3, np.where(U % 3 == 1, 1, -1)), "chi-4": (4, np.where(U % 4 == 1, 1, -1)),
      "leg5": (5, np.where(np.isin(U % 5, (1, 4)), 1, -1))}
LAG2 = {"chi-3": -0.013298, "chi-4": -0.013063, "leg5": -0.011430}
key = {"hyb": "chyb", "full": "cfull"}[target]
rng = np.random.default_rng(int.from_bytes(seed.encode(), "little") % 2**63)
os.makedirs(outdir, exist_ok=True); Y0, W, NPER = 1_050_000_000_000, 500_000_000, 12_500_000
for c0 in range(0, 2000, 50):
    recs = np.zeros(50, REC)
    for i, r in enumerate(range(c0, c0 + 50)):
        py = random.Random(f"{seed}:E028:{r}"); y = Y0 + W * r; s = y + py.randrange(100_000_000); j = py.randrange(NPER)
        P1 = np.ones((16, 16)); P2 = np.ones((16, 16))
        for c, (q, v) in CH.items():
            d = np.array(drift[str(q)]); cr = d[r] * pred["cells"][c][key] / d.mean()
            P1 += cr * np.outer(v, v); P2 += LAG2[c] * np.outer(v, v)
        recs[i]["magic"] = MAGIC; recs[i]["r"] = r; recs[i]["y_r"] = y; recs[i]["s_r"] = s; recs[i]["pair_index"] = j
        recs[i]["nkept"] = NPER + 1
        recs[i]["lag1"] = rng.multinomial(NPER, (P1 / P1.sum()).ravel())
        recs[i]["lag2"] = rng.multinomial(NPER - 1, (P2 / P2.sum()).ravel())
    recs.tofile(os.path.join(outdir, f"chunk_{c0:04d}.bin"))
    json.dump(dict(entry="028", seed=seed, y0=Y0, width=W, strata=list(range(c0, c0 + 50)), synthetic=target),
              open(os.path.join(outdir, f"chunk_{c0:04d}.json"), "w"))
print(f"dry data {seed} ({target}) written to {outdir}")
