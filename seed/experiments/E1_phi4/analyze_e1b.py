"""Analyse the E1b scans: v_c, two-bounce windows, convergence, figure.

Reads e1b_<tag>.json (tags base, dx0.1, x0_20, tpost1500, dx0.025), reruns a few
collisions for the bounce-time check and the phi(0,t) figure.
Writes e1b_analysis.json and fig_e1b_collisions.png.
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from e1b_kkbar import collide

TARGET_VC = 0.2598
TOL_VC = 0.001
TARGET_W1 = (0.1926, 0.2034)
TOL_W = 0.003
LIT_WINDOWS = [(0.1926, 0.2034), (0.2241, 0.2288), (0.2372, 0.2396), (0.2440, 0.2454), (0.2481, 0.2490)]
OMEGA_S = np.sqrt(1.5)

tags = ["base", "dx0.1", "x0_20", "tpost1500", "dx0.025"]
cfg = {}
for t in tags:
    fn = f"e1b_{t}.json"
    if os.path.exists(fn):
        cfg[t] = json.load(open(fn))

out = {"targets": {"v_c": TARGET_VC, "tol_v_c": TOL_VC, "first_window": TARGET_W1, "tol_window_edges": TOL_W,
                   "literature_windows_summary_source": LIT_WINDOWS},
       "configs": {}}


def main_windows(summ, minw=4e-4):
    """Two-bounce windows wider than minw (the 'main' sequence)."""
    return [w for w in summ["two_bounce_windows"] if w["width"] >= minw]


for t, d in cfg.items():
    s = d["summary"]
    ws = s["two_bounce_windows"]
    mw = main_windows(s)
    out["configs"][t] = {"dx": d["dx"], "x0": d["x0"], "t_post": d["t_post"], "scan": d["scan"],
                         "v_c": s["v_c"], "v_c_bracket": s["v_c_bracket"],
                         "n_two_bounce_windows_all": len(ws),
                         "two_bounce_windows_wider_than_4e-4": [[w["lo"], w["hi"], w["width"]] for w in mw],
                         "first_8_two_bounce_windows": [[w["lo"], w["hi"], w["width"]] for w in ws[:8]],
                         "n_runs": len(d["runs"]), "runtime_s": d["runtime_s"]}
    print(f"{t:10s} dx={d['dx']} x0={d['x0']} t_post={d['t_post']}  v_c={s['v_c']:.5f}  "
          f"#2b-windows={len(ws)}  first: " + ", ".join(f"[{w['lo']:.4f},{w['hi']:.4f}]" for w in ws[:5]))

base = cfg["base"]["summary"]
w = base["two_bounce_windows"]
vc = base["v_c"]
# spread over convergence configs
vcs = [out["configs"][t]["v_c"] for t in out["configs"]]
w1lo = [cfg[t]["summary"]["two_bounce_windows"][0]["lo"] for t in cfg]
w1hi = [cfg[t]["summary"]["two_bounce_windows"][0]["hi"] for t in cfg]
widths = [x["width"] for x in w[:5]]
narrowing = all(widths[i + 1] < widths[i] for i in range(len(widths) - 1))
out["headline"] = {
    "v_c": vc, "v_c_spread_over_configs": [min(vcs), max(vcs)],
    "v_c_verdict": "CALIBRATED" if abs(vc - TARGET_VC) <= TOL_VC else "MISS",
    "first_window": [w[0]["lo"], w[0]["hi"]],
    "first_window_spread_lo": [min(w1lo), max(w1lo)], "first_window_spread_hi": [min(w1hi), max(w1hi)],
    "first_window_verdict": "CALIBRATED" if (abs(w[0]["lo"] - TARGET_W1[0]) <= TOL_W and
                                              abs(w[0]["hi"] - TARGET_W1[1]) <= TOL_W) else "MISS",
    "first_five_windows": [[x["lo"], x["hi"]] for x in w[:5]],
    "first_five_widths": widths, "narrowing_toward_vc": narrowing,
    "n_two_bounce_windows_found_base": len(w),
    "windows_vs_literature_max_edge_diff": float(max(max(abs(a[0] - b[0]), abs(a[1] - b[1]))
                                                     for a, b in zip([[x["lo"], x["hi"]] for x in w[:5]], LIT_WINDOWS))),
}

# grid-spacing series (dt = 0.4 dx in all three): observed order and Richardson extrapolation
ser = [t for t in ("dx0.1", "base", "dx0.025") if t in cfg]
if len(ser) == 3:
    def q(t, name):
        s = cfg[t]["summary"]
        return {"v_c": s["v_c"], "w1_lo": s["two_bounce_windows"][0]["lo"],
                "w1_hi": s["two_bounce_windows"][0]["hi"]}[name]
    rich = {}
    for name in ("v_c", "w1_lo", "w1_hi"):
        a, b_, c_ = (q(t, name) for t in ser)
        ratio = (a - b_) / (b_ - c_) if b_ != c_ else float("nan")
        p = float(np.log2(abs(ratio))) if np.isfinite(ratio) and ratio != 0 else float("nan")
        p_use = 2.0   # leapfrog time error with dt proportional to dx dominates (4th-order space)
        ext = c_ + (c_ - b_) / (2 ** p_use - 1)
        rich[name] = {"dx0.1": a, "dx0.05": b_, "dx0.025": c_, "diff_ratio": float(ratio),
                      "observed_order": p, "richardson_p2": float(ext),
                      "uncertainty_est": float(abs(ext - c_) + 1.25e-5)}
    out["dx_series_richardson"] = rich
    out["headline"]["v_c_extrapolated"] = rich["v_c"]["richardson_p2"]
    out["headline"]["first_window_extrapolated"] = [rich["w1_lo"]["richardson_p2"], rich["w1_hi"]["richardson_p2"]]
    out["headline"]["v_c_extrapolated_verdict"] = ("CALIBRATED" if abs(rich["v_c"]["richardson_p2"] - TARGET_VC) <= TOL_VC
                                                   else "MISS")
    print("Richardson:", json.dumps(rich, indent=1))
if os.path.exists("e1b_dtcheck.json"):
    out["dt_check"] = json.load(open("e1b_dtcheck.json"))["cases"]

# resonance check: time between first and second bounce at the centre of each main window
res_rows = []
for i, ww in enumerate(main_windows(base)[:10]):
    vm = 0.5 * (ww["lo"] + ww["hi"])
    r = collide(vm, 12.0, 0.05)
    tb = r["t_bounces"]
    if len(tb) >= 2:
        res_rows.append([i + 1, vm, tb[1] - tb[0]])
res_rows = np.array(res_rows)
slope, icpt = np.polyfit(res_rows[:, 0], res_rows[:, 2], 1)
out["resonance_check"] = {"rows_window_index_v_T12": res_rows.tolist(), "slope_T12_per_window": float(slope),
                          "intercept": float(icpt), "2pi_over_omega_s": float(2 * np.pi / OMEGA_S),
                          "note": "CSW resonance picture: T12 grows by one shape-mode period per window"}
print("resonance slope", slope, "vs 2pi/omega_s", 2 * np.pi / OMEGA_S)
json.dump(out, open("e1b_analysis.json", "w"), indent=1)

# ---------------------------------------------------------------- figure
runs = sorted(cfg["base"]["runs"], key=lambda r: r["v"])
v = np.array([r["v"] for r in runs])
lab = np.array([r["label"] for r in runs])
fig, axs = plt.subplots(3, 1, figsize=(7.2, 7.6), gridspec_kw={"height_ratios": [1.1, 1.1, 1.3]})
ax = axs[0]
y = np.where(lab == 0, 0, np.minimum(lab, 6))
cols = {0: "#9a9a9a", 1: "#1f6fb4", 2: "#d1495b", 3: "#edae49", 4: "#66a182", 5: "#7a5195", 6: "#444444"}
for L in range(7):
    m = y == L
    ax.scatter(v[m], y[m], s=3, c=cols[L], lw=0)
for a, b in LIT_WINDOWS:
    ax.axvspan(a, b, color="#d1495b", alpha=0.12, lw=0)
ax.axvline(TARGET_VC, color="k", ls=":", lw=0.8)
ax.set_yticks(range(7))
ax.set_yticklabels(["capture", "1", "2", "3", "4", "5", "6+"])
ax.set_ylabel("bounces before escape")
ax.set_xlim(0.15, 0.30)
ax.set_title("E1b: outcome vs initial speed (dx=0.05, x0=12). Shaded: target window 1 and windows 2-5 of an unverified literature list; dotted: target v_c=0.2598", fontsize=7)
ax = axs[1]
m = (v > 0.240) & (v < 0.2615)
for L in range(7):
    mm = m & (y == L)
    ax.scatter(v[mm], y[mm], s=5, c=cols[L], lw=0)
ax.axvline(TARGET_VC, color="k", ls=":", lw=0.8)
ax.axvline(vc, color="#1f6fb4", ls="--", lw=0.8)
ax.set_yticks(range(7))
ax.set_yticklabels(["capture", "1", "2", "3", "4", "5", "6+"])
ax.set_xlim(0.240, 0.2615)
ax.set_xlabel("v (each kink, centre-of-mass frame)")
ax.set_title(f"zoom near v_c: ours {vc:.5f} (dashed), target 0.2598 (dotted)", fontsize=8)
ax = axs[2]
for vv, c in ((0.18, "#9a9a9a"), (0.20, "#d1495b"), (0.30, "#1f6fb4")):
    r = collide(vv, 12.0, 0.05, t_post=300.0, return_series=True)
    tt, cc = r["series"][0], r["series"][1]
    ax.plot(tt, cc, lw=0.7, c=c, label=f"v={vv}: " + ("capture" if r["label"] == 0 else f"{r['label']}-bounce escape"))
ax.set_xlim(0, 300)
ax.set_xlabel("t")
ax.set_ylabel("phi(0,t)")
ax.legend(fontsize=7, loc="lower right")
fig.tight_layout()
fig.savefig("fig_e1b_collisions.png", dpi=110)
print("wrote fig_e1b_collisions.png")
