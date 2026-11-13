"""Follow-up analyses (EXPLORATORY, no new trace computation). Uses existing CSVs only.
F1: K=100 c=1 rebinned with width-2 bins (new variant, not the frozen rule).
F2: cross-K agreement of the elliptic part (frozen bins).
F3: window comparison at K=300 (frozen bins), bin values near the named features."""
import json, numpy as np
from plots import load, stat, scale, binned
out = {}
# F1
d = load("data/E_K100_C_c1.csv")
tot = scale(d, stat(d, "S1"), "sqrtX"); ell = scale(d, stat(d, "S1", "ell"), "sqrtX")
hyp = scale(d, stat(d, "S1", "hyp"), "sqrtX"); idt = scale(d, stat(d, "S1", "id"), "sqrtX")
edges = np.arange(0, 42.01, 2.0); rows = []
for a, b in zip(edges[:-1], edges[1:]):
    s = (d["x"] > a) & (d["x"] <= b); n = int(s.sum())
    if n < 2: continue
    f = lambda v: (float(v[s].mean()), float(v[s].std(ddof=1) / np.sqrt(n)))
    rows.append(dict(bin=[a, b], n=n, xmean=float(d["x"][s].mean()), total=f(tot), ell=f(ell),
                     hyp=float(hyp[s].mean()), ident=float(idt[s].mean())))
out["F1_K100_c1_width2"] = rows
# pooled x>10 and x>20
for lo in (5, 10, 20):
    s = d["x"] > lo; n = int(s.sum())
    out[f"F1_pooled_x_gt_{lo}"] = dict(n=n, total=[float(tot[s].mean()), float(tot[s].std(ddof=1)/np.sqrt(n))],
                                      ell=[float(ell[s].mean()), float(ell[s].std(ddof=1)/np.sqrt(n))], hyp=float(hyp[s].mean()))
# F2
src = {300: "data/E_K300_C_5.csv", 1000: "data/T_K1000_C_5.csv", 2500: "data/T_K2500_C_5.csv"}
B = {}
for K, f in src.items():
    dd = load(f); B[K] = binned(dd["x"], scale(dd, stat(dd, "S1", "ell"), "sqrtX"))
for a, b in [(300, 1000), (1000, 2500), (300, 2500)]:
    ca, ma, ea = B[a]; cb, mb, eb = B[b]
    ia = {int(c // 0.2): i for i, c in enumerate(ca)}; ib = {int(c // 0.2): i for i, c in enumerate(cb)}
    for excl in (False, True):
        com = [j for j in sorted(set(ia) & set(ib)) if not (excl and j == 0)]
        dl = np.array([ma[ia[j]] - mb[ib[j]] for j in com]); z = dl / np.array([np.hypot(ea[ia[j]], eb[ib[j]]) for j in com])
        out[f"F2_ell_{a}vs{b}" + ("_excl_first" if excl else "")] = dict(nbins=len(com), rms_diff=float(np.sqrt((dl**2).mean())),
            max_abs_diff=float(np.abs(dl).max()), n_abs_z_gt2=int((np.abs(z) > 2).sum()), max_abs_z=float(np.abs(z).max()))
# F3
F3 = {}
for kind in ("C", "N"):
    dd = load(f"data/E_K300_{kind}_5.csv")
    cx, m, e = binned(dd["x"], scale(dd, stat(dd, "S1"), "sqrtX"))
    _, me, ee = binned(dd["x"], scale(dd, stat(dd, "S1", "ell"), "sqrtX"))
    F3[kind] = dict(x=cx.round(3).tolist(), total=m.round(3).tolist(), se=e.round(3).tolist(), ell=me.round(3).tolist(),
                    hyp=float(scale(dd, stat(dd, "S1", "hyp"), "sqrtX").mean()))
    # local extrema of the binned total (beyond first bin), and drop/rise sizes in units of s.e.
    ext = []
    for i in range(2, len(m) - 1):
        if (m[i] < m[i-1] and m[i] < m[i+1]) or (m[i] > m[i-1] and m[i] > m[i+1]):
            kindx = "min" if m[i] < m[i-1] else "max"
            dz = min(abs(m[i]-m[i-1])/np.hypot(e[i], e[i-1]), abs(m[i]-m[i+1])/np.hypot(e[i], e[i+1]))
            ext.append((kindx, round(float(cx[i]), 2), round(float(m[i]), 3), round(float(dz), 2)))
    F3[kind]["local_extrema_(type,x,value,min_step_z)"] = ext
    # linear trend of total over x in (1,5]
    s = cx > 1; F3[kind]["slope_x_gt1"] = float(np.polyfit(cx[s], m[s], 1, w=1/e[s])[0])
out["F3_K300_window"] = F3
json.dump(out, open("followup.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "F3_K300_window"}, indent=0)[:6000])
for kind in "CN":
    print(kind, "hyp", round(F3[kind]["hyp"], 3), "slope", round(F3[kind]["slope_x_gt1"], 3))
    print(" extrema", F3[kind]["local_extrema_(type,x,value,min_step_z)"])
    print(" x    ", F3[kind]["x"]); print(" tot  ", F3[kind]["total"]); print(" se   ", F3[kind]["se"])

# F1b/F3b (first run inline, added here so the script reproduces every logged number) -> followup_extra.json
ex = {}
s = d["x"] > 5
A = np.vstack([np.ones(s.sum()), d["x"][s]]).T; c, *_ = np.linalg.lstsq(A, tot[s], rcond=None)
r = tot[s] - A @ c; cov = np.linalg.inv(A.T @ A) * r.var(ddof=2)
ex["F1b_K100_total_line_x_gt5"] = dict(intercept=float(c[0]), slope=float(c[1]), slope_se=float(np.sqrt(cov[1, 1])))
for K, f in ((1000, "data/T_K1000_C_5.csv"), (2500, "data/T_K2500_C_5.csv")):
    dd = load(f); cx, m, e = binned(dd["x"], scale(dd, stat(dd, "S1"), "sqrtX"))
    i = {v: int(np.argmin(abs(cx - v))) for v in (1.3, 1.7, 2.3)}
    zz = lambda a, b: float((m[i[a]] - m[i[b]]) / np.hypot(e[i[a]], e[i[b]]))
    ex[f"F3b_K{K}_C"] = dict(bump17_minus_x13_z=zz(1.7, 1.3), bump17_minus_dip23_z=zz(1.7, 2.3),
                            values={str(v): [float(m[i[v]]), float(e[i[v]])] for v in i})
json.dump(ex, open("followup_extra.json", "w"), indent=1)
print(json.dumps(ex, indent=1))
