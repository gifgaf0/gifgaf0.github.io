"""Plots for the exploratory Sym^2-scale session. Binning rule is the frozen one in session_log.md:
25 equal-width bins of width 0.2 on x in (0,5]; mean over primes; sd/sqrt(n); bins with n<30 not plotted."""
import csv, sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SER = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]   # categorical slots 1-4 (fixed order by K)
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2,
                     "figure.dpi": 150, "savefig.bbox": "tight"})

def load(f):
    with open(f) as fh:
        rows = list(csv.DictReader(fh))
    d = {k: np.array([float(r[k]) if k != "window" else 0 for r in rows]) for k in rows[0]}
    return d

def stat(d, which="S1", piece="total"):
    """Return per-prime value of the requested statistic/piece (unscaled)."""
    num = {}
    for c in ("c0", "c2"):
        num[c] = {"ell": d[f"ell_{c}"], "hyp": d[f"hyp_{c}"], "id": d[f"id_{c}"]}
        num[c]["total"] = num[c]["ell"] + num[c]["hyp"] + num[c]["id"]
    D = d["D_c0"] + d["D_c2"]
    if which == "S1":
        return (num["c0"][piece] + num["c2"][piece]) / D
    if which == "S2":
        return (num["c0"][piece] - num["c2"][piece]) / D
    if which == "k0":
        return num["c0"][piece] / d["D_c0"]
    if which == "k2":
        return num["c2"][piece] / d["D_c2"]
    raise ValueError(which)

def scale(d, v, s):
    return {"raw": v, "sqrtX": v * np.sqrt(d["X"]), "sqrtp": v * np.sqrt(d["p"])}[s]

def binned(x, y, xmax=5.0, width=0.2, nmin=30):
    edges = np.arange(0, xmax + 1e-9, width)
    if edges[-1] < xmax - 1e-9: edges = np.append(edges, edges[-1] + width)
    cx, m, e = [], [], []
    for a, b in zip(edges[:-1], edges[1:]):
        sel = (x > a) & (x <= b)
        n = sel.sum()
        if n >= nmin:
            cx.append(x[sel].mean()); m.append(y[sel].mean()); e.append(y[sel].std(ddof=1) / np.sqrt(n))
    return np.array(cx), np.array(m), np.array(e)

SLAB = {"raw": "E", "sqrtX": r"$\sqrt{X}\cdot E$", "sqrtp": r"$\sqrt{p}\cdot E$"}
