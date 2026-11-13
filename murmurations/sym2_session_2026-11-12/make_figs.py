import os, glob, json
import numpy as np
import matplotlib.pyplot as plt
from plots import load, stat, scale, binned, SER, INK, INK2, SLAB

os.makedirs("figs", exist_ok=True)
Ks = [150, 300, 1000, 2500]
src = {150: "data/E_K150_C_5.csv", 300: "data/E_K300_C_5.csv",
       1000: "data/T_K1000_C_5.csv", 2500: "data/T_K2500_C_5.csv"}
D = {K: load(f) for K, f in src.items() if os.path.exists(f)}
col = dict(zip(Ks, SER))
HYP = dict(color=INK2, ls="--", lw=1.2)
IDL = dict(color=INK2, ls=":", lw=1.2)

def eb(ax, x, m, e, c, lab, xf=lambda v: v):
    ax.errorbar(xf(x), m, yerr=e, color=c, lw=1.6, marker="o", ms=3.5, capsize=0, elinewidth=1, label=lab)

def lines(ax, d, which, s, xf=lambda v: v, label=True):
    o = np.argsort(d["x"])
    ax.plot(xf(d["x"][o]), scale(d, stat(d, which, "hyp"), s)[o], **HYP, label="hyperbolic term (−1/2)" if label else None)
    ax.plot(xf(d["x"][o]), scale(d, stat(d, which, "id"), s)[o], **IDL, label="identity term" if label else None)

# ---- Fig 1: S1 overlay, sqrt(X) scaling; total / elliptic only / x^(1/3)
fig, axs = plt.subplots(1, 3, figsize=(13, 3.8))
for K, d in D.items():
    tot = scale(d, stat(d, "S1"), "sqrtX"); ell = scale(d, stat(d, "S1", "ell"), "sqrtX")
    lab = f"K={K}" if len(binned(d["x"], tot)[0]) else f"K={K}: no bin with n≥30"
    eb(axs[0], *binned(d["x"], tot), col[K], lab)
    eb(axs[1], *binned(d["x"], ell), col[K], f"K={K}")
    eb(axs[2], *binned(d["x"], tot), col[K], f"K={K}", xf=np.cbrt)
for i, K in enumerate(D):
    lines(axs[0], D[K], "S1", "sqrtX", label=(i == 0))
    lines(axs[2], D[K], "S1", "sqrtX", xf=np.cbrt, label=False)
axs[0].set_title("S1 (unweighted), total", loc="left"); axs[1].set_title("S1, elliptic part only (total − hyperbolic − identity)", loc="left")
axs[2].set_title("S1, total, against x^(1/3)", loc="left")
for a in axs[:2]: a.set_xlabel("x = p/X,  X = ((K−1)/2π)²")
axs[2].set_xlabel("x^(1/3)")
for a in axs: a.set_ylabel(SLAB["sqrtX"]); a.axhline(0, color=INK2, lw=0.6)
for a in axs: a.set_ylim(-2, 1.5)
axs[0].legend(fontsize=7, frameon=False, ncol=2)
fig.suptitle(y=1.03, t="Unweighted family average of λ_f(p²) at the Sym² scale, conductor window Φ(X_k/X). Binned means ± s.e. over primes (25 bins of width 0.2).", fontsize=9, x=0.01, ha="left")
fig.savefig("figs/fig1_S1_overlay_sqrtX.png"); plt.close(fig)

# ---- Fig 2: per-K small multiples with scatter
fig, axs = plt.subplots(1, len(D), figsize=(3.4 * len(D), 3.4), sharey=True)
for a, (K, d) in zip(np.atleast_1d(axs), D.items()):
    tot = scale(d, stat(d, "S1"), "sqrtX")
    a.scatter(d["x"], tot, s=2, color=col[K], alpha=0.35, lw=0)
    eb(a, *binned(d["x"], tot), col[K], "binned mean")
    lines(a, d, "S1", "sqrtX")
    n = len(d["x"]); tr = "truncated t (τ=1e-4)" if d["truncated"].max() > 0 else "all t"
    a.set_title(f"K={K}: {n} primes, {tr}", loc="left", fontsize=8); a.set_xlabel("x = p/X")
    a.axhline(0, color=INK2, lw=0.6)
np.atleast_1d(axs)[0].set_ylabel(SLAB["sqrtX"]); np.atleast_1d(axs)[0].legend(fontsize=7, frameon=False)
np.atleast_1d(axs)[0].set_ylim(-3, 2.5)
fig.suptitle(y=1.03, t="S1 per prime (faint) and binned (frozen rule). Some per-prime points fall outside the y-range shown.", fontsize=9, x=0.01, ha="left")
fig.savefig("figs/fig2_S1_per_K.png"); plt.close(fig)

# ---- Fig 3: three scalings
fig, axs = plt.subplots(1, 3, figsize=(13, 3.6))
for a, s in zip(axs, ["raw", "sqrtX", "sqrtp"]):
    for i, (K, d) in enumerate(D.items()):
        bb = binned(d["x"], scale(d, stat(d, "S1"), s))
        if len(bb[0]): eb(a, *bb, col[K], f"K={K}")
        lines(a, d, "S1", s, label=(i == 0))
    allm = np.concatenate([np.concatenate([m - e, m + e]) for d in D.values() for (_, m, e) in [binned(d["x"], scale(d, stat(d, "S1"), s))]])
    lo, hi = allm.min(), allm.max(); pad = 0.25 * (hi - lo); a.set_ylim(min(lo - pad, 1.1 * min(0, lo)), hi + pad)
    a.set_title(f"S1 total, scaling {SLAB[s]}", loc="left"); a.set_xlabel("x = p/X"); a.axhline(0, color=INK2, lw=0.6)
axs[0].legend(fontsize=7, frameon=False, ncol=2)
fig.suptitle(y=1.03, t="Same bins in three scalings; dashed = hyperbolic term, dotted = identity term (clipped near x = 0), each in the same scaling.", fontsize=9, x=0.01, ha="left")
fig.savefig("figs/fig3_S1_scalings.png"); plt.close(fig)

# ---- Fig 4: mod-4 classes and S2 (path E only)
E = {K: load(f"data/E_K{K}_C_5.csv") for K in (150, 300)}
fig, axs = plt.subplots(1, 3, figsize=(13, 3.6), sharey=True)
for a, which, ttl in zip(axs, ["k0", "k2", "S2"], ["k ≡ 0 (mod 4) only  (ε_f = +1)", "k ≡ 2 (mod 4) only  (ε_f = −1)", "S2: weighted by i^k = ε_f"]):
    for i, (K, d) in enumerate(E.items()):
        bb = binned(d["x"], scale(d, stat(d, which), "sqrtX"))
        if len(bb[0]): eb(a, *bb, col[K], f"K={K}")
        lines(a, d, which, "sqrtX", label=(i == 0))
    a.set_title(ttl, loc="left"); a.set_xlabel("x = p/X"); a.axhline(0, color=INK2, lw=0.6)
axs[0].set_ylim(-2, 1.5); axs[0].set_ylabel(SLAB["sqrtX"]); axs[0].legend(fontsize=7, frameon=False)
fig.suptitle(y=1.03, t="Conductor window, all t (path E). Class panels and S2 at K ≥ 1000 were not computed (they need t near 0).", fontsize=9, x=0.01, ha="left")
fig.savefig("figs/fig4_classes_S2.png"); plt.close(fig)

# ---- Fig 5: narrow vs conductor window
fig, axs = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
for a, which in zip(axs, ["S1", "S2"]):
    for K in (150, 300):
        for kind, ls, mk in (("C", "-", "o"), ("N", "--", "s")):
            d = load(f"data/E_K{K}_{kind}_5.csv")
            x, m, e = binned(d["x"], scale(d, stat(d, which), "sqrtX"))
            if not len(x): continue
            a.errorbar(x, m, yerr=e, color=col[K], ls=ls, marker=mk, ms=3.5, lw=1.4, elinewidth=1,
                       label=f"K={K}, {'conductor Φ' if kind=='C' else 'narrow K^0.9'}")
    a.set_title(f"{which}: window comparison", loc="left"); a.set_xlabel("x = p/X"); a.axhline(0, color=INK2, lw=0.6)
for kind, lab in (("C", True), ("N", False)):
    d = load(f"data/E_K300_{kind}_5.csv")
    o = np.argsort(d["x"])
    for a, which in zip(axs, ["S1", "S2"]):
        a.plot(d["x"][o], scale(d, stat(d, which, "hyp"), "sqrtX")[o], color=INK2, ls="--" if kind == "C" else "-.", lw=1.2,
               label=(f"hyperbolic term, K=300, {'conductor' if kind=='C' else 'narrow'}" if which == "S1" else None))
for a in axs: a.set_ylim(-2, 1.5)
axs[0].set_ylabel(SLAB["sqrtX"]); axs[0].legend(fontsize=7, frameon=False)
fig.suptitle(y=1.03, t="Dependence on the k-window (R4). Hyperbolic lines drawn (K=300) for both windows; they differ by ~3%. Per prime the two windows differ by rms 0.33-0.50.", fontsize=9, x=0.01, ha="left")
fig.savefig("figs/fig5_window_comparison.png"); plt.close(fig)

# ---- Fig 6: K=100, c=1
d = load("data/E_K100_C_c1.csv")
fig, ax = plt.subplots(figsize=(9, 3.4))
tot = scale(d, stat(d, "S1"), "sqrtX")
ax.scatter(d["x"], tot, s=2, color=SER[0], alpha=0.4, lw=0)
eb(ax, *binned(d["x"], tot, xmax=40.4), SER[0], "S1 binned (width 0.2)")
lines(ax, d, "S1", "sqrtX"); ax.axhline(0, color=INK2, lw=0.6); ax.set_ylim(-3, 2.5)
ax.set_xlabel("x = p/X  (p ≤ K² = 10⁴)"); ax.set_ylabel(SLAB["sqrtX"]); ax.legend(fontsize=7, frameon=False)
ax.set_title("Supplementary: K=100, range c = 1, all t, conductor window", loc="left")
fig.savefig("figs/fig6_K100_c1.png"); plt.close(fig)
print("figs:", sorted(glob.glob("figs/*.png")))
