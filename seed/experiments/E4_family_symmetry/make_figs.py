"""
make_figs.py -- the three E4 figures (small PNGs) from out/*.json and out/fits.jsonl.
Run after e4_yukawa.py, e4_lnr.py and e4_fits.py:  python3 make_figs.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from data_targets import NUFIT, R_ATM_SOL, R_ATM_SOL_ERR

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"          # reference categorical slots 1-3
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
                     "axes.spines.right": False, "legend.frameon": False})

Y = json.load(open(os.path.join(OUT, "yukawa.json")))
L = json.load(open(os.path.join(OUT, "lnr.json")))

# ---------------- figure 1: lepton mixing patterns from residual symmetries
FLOOR = 2e-4
fig, ax = plt.subplots(figsize=(5.6, 3.9), dpi=130)
bf12, lo12, hi12 = NUFIT["s12sq"]
bf13, lo13, hi13 = NUFIT["s13sq"]
ax.add_patch(plt.Rectangle((bf12 - 3 * lo12, bf13 - 3 * lo13), 3 * (lo12 + hi12), 3 * (lo13 + hi13),
                           facecolor="#d9d8d3", edgecolor=INK2, lw=0.8, zorder=1))
ax.annotate("NuFIT 6.0\n3σ", (bf12 + 3 * hi12, bf13), xytext=(6, 0), textcoords="offset points",
            color=INK2, va="center", fontsize=8)


def pts(rows):
    xs, ys = [], []
    for p in rows:
        b = p["best"]
        xs.append(b["s12sq"])
        ys.append(max(b["s13sq"], FLOOR))
    return np.array(xs), np.array(ys)


f21 = [p for p in Y["residual_patterns"]["F21"] if p["kind"] != "quark"]
psl = [p for p in Y["residual_patterns"]["PSL"] if p["kind"] != "quark"]
x, y = pts(psl)
ax.scatter(x, y, s=34, color=S2, edgecolor=SURF, lw=1.2, zorder=3, label="PSL(2,7): full residual symmetry")
x, y = pts(f21)
ax.scatter(x, y, s=46, color=S1, edgecolor=SURF, lw=1.2, zorder=4, marker="s", label="F21: full residual symmetry")
z2 = Y["z2_partial_PSL"]
x = np.array([o["best"]["s12sq"] for o in z2])
y = np.array([max(o["best"]["s13sq"], FLOOR) for o in z2])
ok = np.array([o["survives(p>0.01)"] for o in z2])
ax.scatter(x[ok], y[ok], s=46, color=S3, edgecolor=SURF, lw=1.2, zorder=5, marker="D",
           label="PSL(2,7): Z2-partial, best fit (survives)")
ax.scatter(x[~ok], y[~ok], s=40, facecolor="none", edgecolor=S3, lw=1.4, zorder=5, marker="D",
           label="PSL(2,7): Z2-partial, best fit (excluded)")
h = L["haze"]["pole masses"]["unitary"]
ax.scatter([1 / 3], [FLOOR], s=60, color=INK, marker="x", zorder=6)
ax.annotate("TBM / LNR (θ13 = 0)", (1 / 3, FLOOR), xytext=(4, 7), textcoords="offset points", fontsize=8, color=INK)
ax.scatter([h["s12sq"]], [h["s13sq"]], s=60, color=INK, marker="+", zorder=6)
ax.annotate("LNR + haze", (h["s12sq"], h["s13sq"]), xytext=(-56, 6), textcoords="offset points", fontsize=8, color=INK)
ax.set_yscale("log")
ax.set_ylim(1e-4, 0.6)
ax.set_xlim(-0.02, 0.62)
ax.axhline(FLOOR * 1.6, color=GRID, lw=0.8)
ax.text(0.60, FLOOR * 0.75, "θ13 = 0 plotted here", ha="right", fontsize=7, color=INK2)
ax.set_xlabel("sin²θ12")
ax.set_ylabel("sin²θ13")
ax.set_title("Lepton mixing fixed by residual subgroups (masses free)", fontsize=9, color=INK, loc="left")
ax.legend(fontsize=7, loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_residual_patterns.png"))
plt.close(fig)

# ---------------- figure 2: LNR ratio versus alpha (beta = -1)
al = np.linspace(-1.6, 0.4, 40001)
m1 = np.abs(1 / (al - 1))
m2 = np.abs(-1 / (2 * al + 1))
m3 = np.abs(9 / (al - 1))
with np.errstate(divide="ignore", invalid="ignore"):
    r = (m3 ** 2 - m1 ** 2) / (m2 ** 2 - m1 ** 2)
r[(m2 <= m1) | (m3 <= m2)] = np.nan
fig, ax = plt.subplots(figsize=(5.6, 3.2), dpi=130)
ax.axhspan(21.3, 45.1, color="#ecebe7", zorder=0)
ax.axhspan(R_ATM_SOL - 3 * R_ATM_SOL_ERR, R_ATM_SOL + 3 * R_ATM_SOL_ERR, color="#c9c8c2", zorder=1)
ax.text(0.38, 44, "LNR 2007 3σ range (Schwetz 2006)", ha="right", va="top", fontsize=7, color=INK2)
ax.text(0.38, R_ATM_SOL + 3 * R_ATM_SOL_ERR + 0.6, "NuFIT 6.0 ±3σ", ha="right", va="bottom", fontsize=7, color=INK)
ax.plot(al, r, color=S1, lw=2, zorder=3)
ax.scatter([-1], [80 / 3], s=50, color=INK, zorder=4)
ax.annotate("α = β = −1: 80/3", (-1, 80 / 3), xytext=(8, -12), textcoords="offset points", fontsize=8, color=INK)
ax.set_ylim(0, 60)
ax.set_xlim(-1.6, 0.4)
ax.set_xlabel("α (Majorana I4 coefficient), β = −1")
ax.set_ylabel("Δm²31 / Δm²21")
ax.set_title("LNR seesaw: mixing stays exactly tri-bimaximal (θ13 = 0) for every α", fontsize=9, color=INK, loc="left")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_lnr_alpha.png"))
plt.close(fig)

# ---------------- figure 3: texture survey
recs = [json.loads(l) for l in open(os.path.join(OUT, "fits.jsonl"))]
fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.2), dpi=130, sharey=True)
for ax, sector in zip(axes, ("lepton", "quark")):
    rows = [r_ for r_ in recs if r_["sector"] == sector and not r_.get("structural")]
    groups = {"SURVIVES": (S3, "D", "survives (p > 0.01)"), "accommodates (no prediction)": (S1, "o", "accommodates (N_eff ≥ N_obs)"),
              "excluded": (S2, "s", "excluded")}
    rng = np.random.default_rng(1)
    for v, (col, mk, lab) in groups.items():
        sel = [r_ for r_ in rows if r_["verdict"] == v]
        if not sel:
            continue
        xs = np.array([r_["n_eff"] for r_ in sel], dtype=float) + rng.uniform(-0.18, 0.18, len(sel))
        ys = np.array([max(r_["chi2"], 1e-3) for r_ in sel])
        ax.scatter(xs, ys, s=30, color=col, marker=mk, edgecolor=SURF, lw=1, label=lab, zorder=3)
    nobs = 7 if sector == "lepton" else 8
    ax.axvline(nobs - 0.5, color=INK2, lw=0.8, ls="--")
    ax.text(nobs - 0.4, 2e5, f"N_obs = {nobs}", fontsize=7, color=INK2)
    ax.set_yscale("log")
    ax.set_ylim(5e-4, 1e7)
    ax.set_xlabel("effective parameters N_eff")
    ax.set_title(f"{sector}s", fontsize=9, color=INK, loc="left")
axes[0].set_ylabel("χ²_min  (values < 1e-3 shown at 1e-3)")
axes[0].legend(fontsize=7, loc="lower left")
fig.suptitle("F21 (LNR framework) texture classes that are not structurally dead", fontsize=9, color=INK, x=0.02, ha="left")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_texture_survey.png"))
plt.close(fig)
for f in ("fig_residual_patterns.png", "fig_lnr_alpha.png", "fig_texture_survey.png"):
    print(f, os.path.getsize(os.path.join(HERE, f)) // 1024, "KB")
