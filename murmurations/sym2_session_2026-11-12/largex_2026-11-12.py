"""F5 (EXPLORATORY): large-x behaviour of S1 (conductor window, sqrt(X) scaling) at K = 100, 150, 200.
Width-2 bins beyond x = 5 (same rule as the K = 100 rebinning, F1). Pooled means for x > 5 and x > 10
over each K's own range, plus pooled means over common ranges. Updates followup.json under key F5_largex."""
import json, os, numpy as np
from plots import load, stat, scale
src = {100: "data/E_K100_C_c1.csv", 150: "data/E_K150_C_20.csv", 200: "data/E_K200_C_11.3.csv"}
if os.path.exists("data/E_K200_C_15.csv"): src[200] = "data/E_K200_C_15.csv"
def pool(x, v, lo, hi):
    s = (x > lo) & (x <= hi); n = int(s.sum())
    return dict(n=n, mean=float(v[s].mean()), se=float(v[s].std(ddof=1) / np.sqrt(n))) if n > 1 else None
F5 = {}
for K, f in src.items():
    d = load(f); x = d["x"]
    tot = scale(d, stat(d, "S1"), "sqrtX"); ell = scale(d, stat(d, "S1", "ell"), "sqrtX"); hyp = scale(d, stat(d, "S1", "hyp"), "sqrtX")
    xmax = float(x.max()); r = dict(file=f, nprimes=int(len(x)), xmax=xmax, hyp=float(hyp.mean()))
    r["bins_width2_beyond5"] = []
    for a in np.arange(5.0, xmax, 2.0):
        b = a + 2.0; s = (x > a) & (x <= b); n = int(s.sum())
        if n >= 30:
            r["bins_width2_beyond5"].append(dict(bin=[float(a), float(b)], n=n, xmean=float(x[s].mean()),
                total=[float(tot[s].mean()), float(tot[s].std(ddof=1)/np.sqrt(n))], ell=[float(ell[s].mean()), float(ell[s].std(ddof=1)/np.sqrt(n))]))
    for lo in (5, 10):
        r[f"x_gt_{lo}_own_range"] = dict(total=pool(x, tot, lo, xmax), ell=pool(x, ell, lo, xmax))
    for lo, hi in ((5, 11.28), (10, 11.28), (5, 15), (10, 15), (5, 20), (10, 20)):
        if xmax >= hi - 0.02: r[f"common_({lo},{hi}]"] = dict(total=pool(x, tot, lo, hi), ell=pool(x, ell, lo, hi))
    F5[K] = r
fu = json.load(open("followup.json")); fu["F5_largex"] = F5; json.dump(fu, open("followup.json", "w"), indent=1)
for K, r in F5.items():
    print(f"K={K} n={r['nprimes']} xmax={r['xmax']:.2f} hyp={r['hyp']:.3f} ({r['file']})")
    for k in [k for k in r if k.startswith("x_gt") or k.startswith("common")]:
        t, e = r[k]["total"], r[k]["ell"]
        if t: print(f"   {k:22s} n={t['n']:4d} total {t['mean']:+.3f} ± {t['se']:.3f}   ell {e['mean']:+.3f} ± {e['se']:.3f}   (−hyp {-r['hyp']:.3f})")
    print("   width-2 bins:", [(round(b['xmean'],1), round(b['total'][0],3), round(b['ell'][0],3)) for b in r["bins_width2_beyond5"]])

# F5b: K-dependence of the common-range offsets (5,15] and (10,15]: weighted fits total = a + b/K, and pure b/K (offset -> 0).
F5b = {}
for rng in ("common_(5,15]", "common_(10,15]"):
    Ks = np.array([K for K in F5 if rng in F5[K]], float)
    m = np.array([F5[int(K)][rng]["total"]["mean"] for K in Ks]); e = np.array([F5[int(K)][rng]["total"]["se"] for K in Ks])
    w = 1 / e**2
    A = np.vstack([np.ones_like(Ks), 1 / Ks]).T; C = np.linalg.inv(A.T @ (A * w[:, None])); ab = C @ (A.T @ (w * m))
    chi_ab = float(np.sum(w * (m - A @ ab) ** 2))
    b0 = float(np.sum(w * m / Ks) / np.sum(w / Ks**2)); chi_b = float(np.sum(w * (m - b0 / Ks) ** 2))
    c0 = float(np.sum(w * m) / np.sum(w)); chi_c = float(np.sum(w * (m - c0) ** 2))
    F5b[rng] = dict(K=Ks.tolist(), mean=m.tolist(), se=e.tolist(),
                    fit_a_plus_b_over_K=dict(a=float(ab[0]), a_se=float(np.sqrt(C[0, 0])), b=float(ab[1]), b_se=float(np.sqrt(C[1, 1])), chi2=chi_ab, dof=len(Ks) - 2),
                    fit_pure_b_over_K=dict(b=b0, chi2=chi_b, dof=len(Ks) - 1), fit_constant=dict(c=c0, c_se=float(np.sqrt(1 / np.sum(w))), chi2=chi_c, dof=len(Ks) - 1))
fu = json.load(open("followup.json")); fu["F5b_offset_vs_K"] = F5b; json.dump(fu, open("followup.json", "w"), indent=1)
print(json.dumps(F5b, indent=1))
