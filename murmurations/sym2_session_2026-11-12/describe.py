"""Descriptive numbers for the note (not tests): bin-by-bin agreement between K values,
size of pieces, and per-prime scatter. Frozen bins."""
import os, json
import numpy as np
from plots import load, stat, scale, binned

src = {300: "data/E_K300_C_5.csv", 1000: "data/T_K1000_C_5.csv", 2500: "data/T_K2500_C_5.csv"}
D = {K: load(f) for K, f in src.items() if os.path.exists(f)}
out = {}
B = {}
for K, d in D.items():
    tot = scale(d, stat(d, "S1"), "sqrtX")
    cx, m, e = binned(d["x"], tot)
    ell = binned(d["x"], scale(d, stat(d, "S1", "ell"), "sqrtX"))[1]
    hyp = scale(d, stat(d, "S1", "hyp"), "sqrtX")
    B[K] = (cx, m, e)
    out[K] = dict(nprimes=int(len(tot)), nbins=int(len(cx)), hyp_mean=float(hyp.mean()), hyp_range=[float(hyp.min()), float(hyp.max())],
                  binned_min=float(m.min()), x_at_min=float(cx[m.argmin()]), binned_max_beyond_0p4=float(m[cx > 0.4].max()),
                  median_se=float(np.median(e)), per_prime_sd_median=float(np.median(e * np.sqrt(len(tot) / max(1, len(cx))))),
                  last_bin=[float(cx[-1]), float(m[-1]), float(e[-1])], ell_last_bin=float(ell[-1]))
pairs = [(300, 1000), (1000, 2500), (300, 2500)]
for a, b in pairs:
    if a in B and b in B:
        ca, ma, ea = B[a]; cb, mb, eb_ = B[b]
        # match bins by index of bin (same frozen edges): use bin centre rounding
        ia = {int(c // 0.2): i for i, c in enumerate(ca)}; ib = {int(c // 0.2): i for i, c in enumerate(cb)}
        common = sorted(set(ia) & set(ib))
        z = np.array([(ma[ia[j]] - mb[ib[j]]) / np.hypot(ea[ia[j]], eb_[ib[j]]) for j in common])
        dlt = np.array([ma[ia[j]] - mb[ib[j]] for j in common])
        out[f"{a}vs{b}"] = dict(nbins=len(common), max_abs_diff=float(np.abs(dlt).max()), rms_diff=float(np.sqrt((dlt**2).mean())),
                                n_abs_z_gt2=int((np.abs(z) > 2).sum()), max_abs_z=float(np.abs(z).max()))
json.dump(out, open("data/describe.json", "w"), indent=1)
print(json.dumps(out, indent=1))
