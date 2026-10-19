#!/usr/bin/env python3
"""E6 figures (reads out/stage_*.json, recomputes profiles with es_core).  Writes fig_branches.png,
fig_profiles.png, fig_ep.png (small PNGs)."""
import json
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import es_core as ec  # noqa: E402

OUT = os.path.join(HERE, "out")
BLUE, ORANGE, AQUA, INK, INK2, GRID = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2.0,
                     "legend.frameon": False, "savefig.dpi": 130})


def load(name):
    with open(os.path.join(OUT, f"stage_{name}.json")) as fh:
        return json.load(fh)


flat, crit, branch, ep, fixed = load("flat"), load("crit"), load("branch"), load("ep"), load("fixed_alpha")
best = crit["runs"][2]
ac, bc = best["alpha_crit"], best["b_crit"]
rows = sorted(branch["rows"] + [dict(b=bc, alpha=ac, m_inf=best["m_inf"])], key=lambda r: r["b"])
rows = [dict(b=flat["b_flat"], alpha=0.0, m_inf=flat["m0"])] + rows
b = np.array([r["b"] for r in rows])
a = np.array([r["alpha"] for r in rows])
M = 4 * math.pi * np.array([r["m_inf"] for r in rows])
low, up = b <= bc, b >= bc

# ---------------------------------------------------------------- fig_branches
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.0))
ax[0].plot(b[low], a[low], color=BLUE, label="lower branch")
ax[0].plot(b[up], a[up], color=ORANGE, label="upper branch")
ax[0].plot([bc], [ac], "o", ms=7, color=INK, mec="white", mew=1.5, zorder=5)
ax[0].annotate(f"fold: $\\alpha_{{crit}}$ = {ac:.7f}\n$b$ = {bc:.4f}", (bc, ac), xytext=(6.0, 0.036), fontsize=8,
               color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax[0].set_xscale("log")
ax[0].set_xlabel("branch parameter $b = -F'(0)$  ($x = e f r$)")
ax[0].set_ylabel(r"$\alpha = 4\pi G f^2$")
ax[0].set_ylim(0, 0.045)
ax[0].legend(loc="upper right", fontsize=8)
ax[0].set_title("solution curve", fontsize=9, color=INK, loc="left")
sel = a > 1.5e-3
ax[1].plot(a[low & sel | (low & (a == 0))], M[low & sel | (low & (a == 0))], color=BLUE, label="lower")
ax[1].plot(a[up & sel], M[up & sel], color=ORANGE, label="upper")
ax[1].plot([ac], [4 * math.pi * best["m_inf"]], "o", ms=7, color=INK, mec="white", mew=1.5, zorder=5)
ax[1].set_xlabel(r"$\alpha$")
ax[1].set_ylabel(r"$M_{ADM}$  [$f/e$]")
ax[1].set_ylim(55, 140)
ax[1].text(0.002, 75.5, "flat skyrmion 72.92", fontsize=7.5, color=INK2)
ax[1].text(0.0105, 112, "upper branch:\n$\\sqrt{\\alpha}\\,m \\to$ Bartnik-McKinnon\nas $\\alpha \\to 0$", fontsize=7.5, color=INK2)
ax[1].legend(loc="upper right", fontsize=8)
ax[1].set_title("ADM mass (cusp at the fold)", fontsize=9, color=INK, loc="left")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_branches.png"))
plt.close(fig)

# ---------------------------------------------------------------- fig_profiles
cases = [("flat ($\\alpha$=0)", flat["b_flat"], 0.0, INK2, "-")]
r03 = [r for r in fixed["rows"] if abs(r["alpha"] - 0.03) < 1e-12][0]
cases.append(("lower, $\\alpha$=0.03", r03["lower"]["b"], 0.03, BLUE, "-"))
cases.append((f"fold, $\\alpha$={ac:.5f}", bc, ac, AQUA, "-"))
cases.append(("upper, $\\alpha$=0.03", r03["upper"]["b"], 0.03, ORANGE, "--"))
fig, ax = plt.subplots(1, 3, figsize=(7.6, 2.7))
for lab, bb, al, col, ls in cases:
    x, F, P, m, lsg = ec.profile(bb, al, 2e-3, ec.x0_for(bb), 2e3)
    lsinf = lsg[-1]
    sel = x <= 8
    ax[0].plot(x[sel], F[sel] / math.pi, color=col, ls=ls, label=lab, lw=1.8)
    ax[1].plot(x[sel], 1 - 2 * al * m[sel] / x[sel], color=col, ls=ls, lw=1.8)
    ax[2].plot(x[sel], np.exp(lsg[sel] - lsinf), color=col, ls=ls, lw=1.8)
ax[0].set_ylabel(r"$F/\pi$")
ax[1].set_ylabel(r"$N = 1 - 2\alpha m/x$")
ax[2].set_ylabel(r"$\sigma$")
for q in ax:
    q.set_xlabel(r"$x = e f r$")
ax[0].legend(fontsize=7, loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_profiles.png"))
plt.close(fig)

# ---------------------------------------------------------------- fig_ep
A = np.array([r["alpha"] for r in ep["full"]])
D = (np.array([r["m_inf"] for r in ep["full"]]) - flat["m0"]) / A
fig, ax = plt.subplots(figsize=(4.6, 3.0))
aa = np.linspace(0, A.max(), 50)
c = np.polyfit(A, D, 3)
ax.plot(aa * 1e3, np.polyval(c, aa), color=BLUE, lw=1.5, label="cubic fit to full solutions")
ax.plot(A * 1e3, D, "o", ms=6, color=BLUE, mec="white", mew=1.2, label="full Einstein-Skyrme, lower branch")
ax.axhline(ep["m1_GR_first_order"], color=AQUA, lw=2, ls="--",
           label=f"GR first order, $-\\int(\\rho+p_r)Gm/r$: {ep['m1_GR_first_order']:.3f}")
ax.axhline(ep["m1_newton"], color=ORANGE, lw=2,
           label=f"Newtonian, $\\frac{{1}}{{2}}\\int\\rho\\Phi$: {ep['m1_newton']:.3f}")
ax.set_xlabel(r"$\alpha$  ($\times 10^{-3}$)")
ax.set_ylabel(r"$[m_\infty(\alpha) - m_0]/\alpha$  (units $4\pi f/e$)")
ax.set_ylim(min(ep["m1_GR_first_order"], D.min()) - 1.0, max(ep["m1_newton"], D.max()) + 1.5)
ax.legend(fontsize=6.8, loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_ep.png"))
plt.close(fig)
for fn in ["fig_branches.png", "fig_profiles.png", "fig_ep.png"]:
    print(fn, os.path.getsize(os.path.join(HERE, fn)) // 1024, "KB")

# ---------------------------------------------------------------- fig_stability
st = load("stability")
sc = sorted(st["scan"] + [dict(b=r["b"], alpha=r["alpha"], omega2_X800=r["omega2_lowest"])
                         for r in st["rows"] if r["label"] != "flat"], key=lambda r: r["b"])
bs = np.array([r["b"] for r in sc])
w2 = np.array([r["omega2_X800"] for r in sc])
fig, ax = plt.subplots(figsize=(4.6, 2.9))
lo_, up_ = bs < bc, bs > bc
ax.axhline(0, color=INK2, lw=0.8)
ax.axvline(bc, color=INK2, lw=0.8, ls=":")
ax.plot(bs[lo_], w2[lo_], "o-", color=BLUE, ms=5, lw=1.5, mec="white", label="lower branch (no negative mode)")
ax.plot(bs[up_], w2[up_], "o-", color=ORANGE, ms=5, lw=1.5, mec="white", label="upper branch (one negative mode)")
ax.text(bc + 0.03, -1.55, f"fold $b$ = {bc:.6f}\nzero crossing of $\\omega^2$: {st['zero_crossing_b']['X=800']:.6f}", fontsize=7.5, color=INK2)
ax.set_xlabel("branch parameter $b = -F'(0)$")
ax.set_ylabel(r"lowest radial $\omega^2$  [$(ef)^2$]")
ax.legend(fontsize=7, loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_stability.png"))
plt.close(fig)
print("fig_stability.png", os.path.getsize(os.path.join(HERE, "fig_stability.png")) // 1024, "KB")
