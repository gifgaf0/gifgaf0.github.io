"""Analyse the E1c reconciliation runs (e1c_reconcile.jsonl) and compare the E1c map with DSV Fig. 2.

1. omega = 0.99 column: the call, the time the pair first appears and the trajectory phi(0, t)
   for every (scheme, dx, dt); trajectory divergence time from the finest fourth-order run.
2. Point-level comparison of the original E1c map (e1c_grid.json + e1c_fine.json, dx = 0.1,
   dt = 0.04, v step 0.01) with the digitized DSV Fig. 2 (dsv_fig2_reading.json).
Writes e1c_reconcile_analysis.json and fig_e1c_reconcile.png.
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

runs = [json.loads(l) for l in open("e1c_reconcile.jsonl") if l.strip()]
runs99 = [r for r in runs if r["omega"] == 0.99]
out = {}

# ---------------------------------------------------------------- 1. omega = 0.99 column
table = []
for r in sorted(runs99, key=lambda r: (r["v"], r["scheme"], -r["dx"], -r["dt"])):
    table.append({"v": r["v"], "scheme": r["scheme"], "dx": r["dx"], "dt": r["dt"], "pair_at_T": r["produced_dsv"],
                  "pair_since": r["pair_continuously_present_since"], "first_pair": r["first_pair_any"],
                  "survives_1.5T": r["survives_to_1.5T"], "E0": r["E0"], "E_T_inner": r["E_T_inner"]})
out["omega_0.99_runs"] = table


def phi0(r):
    return np.load(os.path.join("reconcile_data", r["key"] + "_phi0.npy")).astype(float)


div = {}
for v in sorted(set(r["v"] for r in runs99)):
    rv = [r for r in runs99 if abs(r["v"] - v) < 1e-9]
    y4 = [r for r in rv if r["scheme"] == "y4"]
    if not y4:
        continue
    ref = min(y4, key=lambda r: (r["dx"], r["dt"]))
    p_ref = phi0(ref)
    rows = []
    for r in rv:
        if r is ref:
            continue
        p = phi0(r)
        n = min(len(p), len(p_ref))
        bad = np.where(np.abs(p[:n] - p_ref[:n]) > 0.1)[0]
        rows.append({"scheme": r["scheme"], "dx": r["dx"], "dt": r["dt"],
                     "t_diverge_phi0_gt_0.1": float(bad[0] * 0.5) if len(bad) else None,
                     "max_abs_diff_phi0_t<500": float(np.max(np.abs(p[:1001] - p_ref[:1001])))})
    div[f"{v:.2f}"] = {"reference": {"scheme": ref["scheme"], "dx": ref["dx"], "dt": ref["dt"]}, "vs_reference": rows}
out["phi0_divergence_from_finest_y4"] = div

col = {}
for r in runs99:
    if r["scheme"] == "y4" and r["dx"] == 0.05 and r["dt"] == 0.02:
        col[f"{r['v']:.2f}"] = {"pair_at_T": r["produced_dsv"], "pair_since": r["pair_continuously_present_since"],
                                 "survives_1.5T": r["survives_to_1.5T"]}
out["omega_0.99_column_y4_dx0.05_dt0.02"] = dict(sorted(col.items()))


def verdict_point(v):
    rv = [r for r in runs99 if abs(r["v"] - v) < 1e-9]
    y4 = [r for r in rv if r["scheme"] == "y4"]
    lf = [r for r in rv if r["scheme"] == "lf"]
    return {"y4_calls": sorted({(r["dx"], r["dt"], r["produced_dsv"], r["pair_continuously_present_since"]) for r in y4}),
            "lf_calls": sorted({(r["dx"], r["dt"], r["produced_dsv"], r["pair_continuously_present_since"]) for r in lf}),
            "y4_all_agree": len({r["produced_dsv"] for r in y4}) == 1 if y4 else None,
            "y4_call": y4[0]["produced_dsv"] if y4 and len({r["produced_dsv"] for r in y4}) == 1 else None}


out["point_0.41"] = verdict_point(0.41)
out["point_0.43"] = verdict_point(0.43)

# ---------------------------------------------------------------- 1b. DSV producers for E1e
from phi4core import M_KINK, grid, free_quanta
from e1c_dsv import dsv_initial
TWO_M = 2 * M_KINK
cands = sorted({(r["omega"], r["v"]) for r in runs if r["omega"] != 0.99})
e1e_rows = []
for om_, v_ in cands:
    a = [r for r in runs if r["omega"] == om_ and r["v"] == v_ and r["scheme"] == "y4" and r["dx"] == 0.05 and r["dt"] == 0.02]
    b = [r for r in runs if r["omega"] == om_ and r["v"] == v_ and r["scheme"] == "y4" and r["dx"] == 0.025 and r["dt"] == 0.01]
    row_ = {"omega": om_, "v": v_, "E_over_2M": (a or b)[0]["E0"] / TWO_M,
            "y4_dx0.05_dt0.02": [a[0]["produced_dsv"], a[0]["pair_continuously_present_since"]] if a else None,
            "y4_dx0.025_dt0.01": [b[0]["produced_dsv"], b[0]["pair_continuously_present_since"]] if b else None}
    if a and b:
        pa, pb = phi0(a[0]), phi0(b[0])
        n = min(len(pa), len(pb))
        bad = np.where(np.abs(pa[:n] - pb[:n]) > 0.1)[0]
        tdiv = float(bad[0] * 0.5) if len(bad) else None
        row_["t_diverge_phi0"] = tdiv
        f = [r["first_pair_any"] for r in (a[0], b[0]) if r["first_pair_any"] is not None]
        row_["converged_producer"] = bool(a[0]["produced_dsv"] and b[0]["produced_dsv"] and
                                          (tdiv is None or (f and tdiv >= max(f) - 1e-9)))
    e1e_rows.append(row_)
e1e_rows.sort(key=lambda r: r["E_over_2M"])
out["dsv_producers_resolution_check"] = e1e_rows
conv = [r for r in e1e_rows if r.get("converged_producer")]
if conv:
    r0 = conv[0]
    x = grid(660.0, 0.1)
    phi, pi = dsv_initial(x, r0["omega"], r0["v"])
    E_lat = None
    nlin = free_quanta(phi, pi, 0.1)[1]
    E0 = r0["E_over_2M"] * TWO_M
    out["e1e_dsv_lowest_converged"] = {"omega": r0["omega"], "v": r0["v"], "E_over_2M": r0["E_over_2M"],
                                       "N_E_times_lambda_over_m2": E0 / (2 * np.sqrt(2.0)),
                                       "N_lin_times_lambda_over_m2": nlin / 2.0,
                                       "criterion": "pair at T with y4 at (0.05, 0.02) and (0.025, 0.01), and phi(0,t) of "
                                                    "the two agree (to 0.1) until the pair has formed"}
else:
    out["e1e_dsv_lowest_converged"] = None

# ---------------------------------------------------------------- 2. map vs DSV Fig. 2
dsv = json.load(open("dsv_fig2_reading.json"))["producing_v"]
main = json.load(open("e1c_grid.json"))["runs"] + json.load(open("e1c_fine.json"))["runs"]
ours = {}
for r in main:
    ours.setdefault(f"{r['omega']:.2f}", {})[round(r["v"], 2)] = r["produced_dsv"]
cmp_rows, H, FP, MS, H1 = [], 0, 0, 0, 0
for om in sorted(dsv):
    d = set(round(v, 2) for v in dsv[om])
    o = {v for v, p in ours[om].items() if p}
    grid_v = set(ours[om])
    d &= grid_v
    hit = d & o
    fp = o - d
    ms = d - o
    near = {v for v in o if any(abs(v - w) < 0.0101 for w in d)}
    H += len(hit); FP += len(fp); MS += len(ms); H1 += len(near)
    cmp_rows.append({"omega": om, "dsv": sorted(d), "ours": sorted(o), "hits": len(hit), "false_pos": sorted(fp),
                     "missed": sorted(ms), "ours_within_0.01_of_a_dsv_point": len(near)})
nd = sum(len(r["dsv"]) for r in cmp_rows)
no = sum(len(r["ours"]) for r in cmp_rows)
out["map_vs_dsv_fig2"] = {"rows": cmp_rows, "n_dsv_producing": nd, "n_ours_producing": no, "hits": H,
                          "false_positives": FP, "missed": MS,
                          "jaccard": H / (H + FP + MS), "ours_within_0.01_of_dsv": H1,
                          "note": "original E1c map, dx = 0.1, dt = 0.04 (point calls not converged: dx = 0.05 rerun "
                                  "agrees on 95% of calls); DSV read from their Fig. 2 to the nearest 0.01"}
json.dump(out, open("e1c_reconcile_analysis.json", "w"), indent=1, default=float)

# ---------------------------------------------------------------- figure
fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.3), sharey=True)
style = {"y4": "-", "lf": "--"}
for ax, v in zip(axs, (0.41, 0.43)):
    rv = sorted([r for r in runs99 if abs(r["v"] - v) < 1e-9], key=lambda r: (r["scheme"] != "y4", r["dx"], r["dt"]))
    for r in rv:
        oz = np.array(r["outer_zero_series"])
        t = np.arange(len(oz)) * 10.0
        lab = f"{r['scheme']} dx={r['dx']:g} dt={r['dt']:g}"
        ax.plot(t, oz, style[r["scheme"]], lw=1.6 if r["scheme"] == "y4" else 1.0, label=lab,
                alpha=0.9 if r["scheme"] == "y4" else 0.7)
    ax.axvline(1200, color="k", lw=0.6, ls=":")
    ax.set_title(f"(omega, v) = (0.99, {v:.2f})", fontsize=9)
    ax.set_xlabel("t")
    ax.legend(fontsize=6, loc="upper left")
axs[0].set_ylabel("outer zero of the pair (0 = no pair)")
fig.suptitle("E1c reconciliation, omega = 0.99: y4 = 4th-order time stepping (solid), lf = original leapfrog (dashed)", fontsize=9)
fig.tight_layout()
fig.savefig("fig_e1c_reconcile.png", dpi=95)

print(json.dumps({k: out[k] for k in ("point_0.41", "point_0.43", "omega_0.99_column_y4_dx0.05_dt0.02")}, indent=1,
                 default=str))
print(json.dumps(out["phi0_divergence_from_finest_y4"], indent=1))
for r in out["dsv_producers_resolution_check"]:
    print("DSV E1e check", r)
print("lowest converged DSV producer:", out["e1e_dsv_lowest_converged"])
m = out["map_vs_dsv_fig2"]
print({k: m[k] for k in m if k != "rows"})
for r in m["rows"]:
    print(r["omega"], "hits", r["hits"], "FP", r["false_pos"], "missed", r["missed"])
