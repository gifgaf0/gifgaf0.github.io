"""drift_028.py -- local (2.16) correlation at every stratum's mean run midpoint (archived predictor).
Exact evaluation at 2,000 points takes ~16 min per character, so the local curve is evaluated exactly at
33 Chebyshev nodes in log y and interpolated (degree 32); the interpolant is validated against exact local
values at 5 strata.  Output pred/drift_216.json (per-stratum shape for the dry runs + discrete means)."""
import os as _os; PRED = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "pred")
import json, math, numpy as np
from predict_026 import marg, corr
from band_028 import strata_mid
ym = strata_mid(True); u = np.log(ym); a, b = u.min(), u.max()
k = np.arange(33); xn = np.cos(np.pi * (k + 0.5) / 33); un = (a + b) / 2 + (b - a) / 2 * xn
def loc(q, uu): rq, Mx = marg(q, q, uu); return corr(q, Mx / Mx.sum(), rq)
out = {"y_mid": ym.tolist()}
for q in (3, 4, 5):
    f = np.array([loc(q, x) for x in un])
    ch = np.polynomial.chebyshev.Chebyshev.fit(xn, f, 32)
    v = ch((2 * u - a - b) / (b - a))
    chk = {r: (loc(q, float(u[r])), float(v[r])) for r in (0, 517, 1000, 1499, 1999)}
    out[str(q)] = v.tolist(); out[f"check_{q}"] = {str(r): x for r, x in chk.items()}
    print(q, "discrete mean", repr(float(v.mean())), " max |interp - exact| at check strata", max(abs(x - y) for x, y in chk.values()), flush=True)
json.dump(out, open(PRED + "/drift_216.json", "w"))
