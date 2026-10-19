"""Analyse E1c (DSV breather trains): production map, qualitative targets, figure.
Reads e1c_grid.json, e1c_fine.json, e1c_high.json, e1c_dxcheck.json, e1c_example.json,
e1c_example_spacetime.npz. Writes e1c_analysis.json and fig_e1c_dsv.png."""
import json
import os
import numpy as np
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from phi4core import M_KINK, grid, free_quanta
from e1c_dsv import dsv_initial

TWO_M = 2 * M_KINK
runs = json.load(open("e1c_grid.json"))["runs"] + json.load(open("e1c_fine.json"))["runs"]
runs = sorted(runs, key=lambda r: (r["omega"], r["v"]))
oms = sorted(set(r["omega"] for r in runs))
vs = sorted(set(r["v"] for r in runs))
key = {(r["omega"], r["v"]): r for r in runs}
ex = json.load(open("e1c_example.json"))
out = {"n_runs_main": len(runs), "omega_values": oms, "v_values": [vs[0], vs[-1], len(vs)]}

crit = {"dsv": "produced_dsv", "survive": "survives_to_1.5T", "persist": "produced_persist"}
per_omega = {}
for o in oms:
    row = {}
    for cn, ck in crit.items():
        pv = [r["v"] for r in runs if r["omega"] == o and r[ck]]
        row[cn] = {"n": len(pv), "v_min": min(pv) if pv else None, "v_max": max(pv) if pv else None,
                   "v_median": float(np.median(pv)) if pv else None}
    per_omega[f"{o:.2f}"] = row
out["per_omega"] = per_omega

trend = {}
for cn in crit:
    oo = [o for o in oms if per_omega[f"{o:.2f}"][cn]["n"] > 0]
    med = [per_omega[f"{o:.2f}"][cn]["v_median"] for o in oo]
    vmax = [per_omega[f"{o:.2f}"][cn]["v_max"] for o in oo]
    vmin = [per_omega[f"{o:.2f}"][cn]["v_min"] for o in oo]
    rho_med = spearmanr(oo, med) if len(oo) > 2 else None
    rho_max = spearmanr(oo, vmax) if len(oo) > 2 else None
    rho_min = spearmanr(oo, vmin) if len(oo) > 2 else None
    trend[cn] = {"spearman_omega_vs_median_v": [float(rho_med[0]), float(rho_med[1])] if rho_med else None,
                 "spearman_omega_vs_vmax": [float(rho_max[0]), float(rho_max[1])] if rho_max else None,
                 "spearman_omega_vs_vmin": [float(rho_min[0]), float(rho_min[1])] if rho_min else None,
                 "n_producing_total": int(sum(r[crit[cn]] for r in runs))}
out["trend"] = trend

# high-v pass-through
hv = {}
for vcut in (0.8, 0.85, 0.9):
    sel = [r for r in runs if r["v"] >= vcut - 1e-9]
    hv[f"v>={vcut}"] = {"n": len(sel), "n_produced_dsv": int(sum(r["produced_dsv"] for r in sel))}
out["high_v"] = hv

# holes: non-producing points with producing neighbours on both sides in v (step 0.01)
# and on both sides in omega
holes = []
for (o, v), r in key.items():
    if r["produced_dsv"]:
        continue
    io, iv = oms.index(o), vs.index(v)
    nv = [key.get((o, vs[iv + d])) for d in (-1, 1) if 0 <= iv + d < len(vs)]
    no = [key.get((oms[io + d], v)) for d in (-1, 1) if 0 <= io + d < len(oms)]
    if len(nv) == 2 and all(q["produced_dsv"] for q in nv):
        holes.append({"omega": o, "v": v, "type": "v-neighbours produce",
                      "omega_neighbours_produce": [q["produced_dsv"] for q in no]})
out["holes_dsv"] = holes
probe = {}
for v in (0.80, 0.81, 0.82, 0.83, 0.84):
    for o in (0.90, 0.91, 0.92):
        r = key.get((o, round(v, 2)))
        if r:
            probe[f"({o:.2f},{v:.2f})"] = {"dsv": r["produced_dsv"], "survive": r["survives_to_1.5T"]}
out["near_0.91_0.82"] = probe

# example
out["example_0.99_0.43"] = {k: ex[k] for k in ("produced_dsv", "produced_persist", "survives_to_1.5T",
                                               "pair_continuously_present_since", "E0", "n_pairs_T")}
out["example_0.99_0.43"]["E0_over_2M"] = ex["E0"] / TWO_M

# omega > 0.99
if os.path.exists("e1c_high.json"):
    hr = json.load(open("e1c_high.json"))["runs"]
    out["omega_gt_0.99"] = {f"{o}": {"n": sum(1 for r in hr if r["omega"] == o),
                                     "produced_dsv_at_v": [r["v"] for r in hr if r["omega"] == o and r["produced_dsv"]],
                                     "survives_at_v": [r["v"] for r in hr if r["omega"] == o and r["survives_to_1.5T"]]}
                            for o in sorted(set(r["omega"] for r in hr))}
# dx check
if os.path.exists("e1c_dxcheck.json"):
    dr = json.load(open("e1c_dxcheck.json"))["runs"]
    agree = [(r["produced_dsv"] == key[(r["omega"], r["v"])]["produced_dsv"]) for r in dr if (r["omega"], r["v"]) in key]
    agree_s = [(r["survives_to_1.5T"] == key[(r["omega"], r["v"])]["survives_to_1.5T"]) for r in dr if (r["omega"], r["v"]) in key]
    dis = [(r["omega"], r["v"], r["produced_dsv"], key[(r["omega"], r["v"])]["produced_dsv"]) for r in dr
           if (r["omega"], r["v"]) in key and r["produced_dsv"] != key[(r["omega"], r["v"])]["produced_dsv"]]
    out["dx_check"] = {"n": len(agree), "agree_frac_dsv": float(np.mean(agree)),
                       "agree_frac_survive": float(np.mean(agree_s)),
                       "disagreements_omega_v_dx0.05_dx0.1": dis}

# energies and quanta of producing runs
prod = [r for r in runs if r["produced_dsv"]]
surv = [r for r in runs if r["survives_to_1.5T"]]


def nlin(o, v):
    x = grid(660.0, 0.1)
    phi, pi = dsv_initial(x, o, v)
    return free_quanta(phi, pi, 0.1)


emin = {}
for name, sel in (("produced_dsv", prod), ("survives_to_1.5T", surv)):
    if sel:
        r = min(sel, key=lambda q: q["E0"])
        Eq, Nl = nlin(r["omega"], r["v"])
        emin[name] = {"omega": r["omega"], "v": r["v"], "E": r["E0"], "E_over_2M": r["E0"] / TWO_M,
                      "N_E_over_m": r["E0"] / np.sqrt(2), "N_lin": Nl, "E_quad": Eq}
        rs = sorted(sel, key=lambda q: q["N_lin"] if "N_lin" in q else 0)
out["min_energy_producing"] = emin
allE = np.array([r["E0"] for r in runs])
out["E_over_2M_range_all_runs"] = [float(allE.min() / TWO_M), float(allE.max() / TWO_M)]
# minimum N_lin over producing runs (compute for all producing; cheap)
nl = []
for r in surv:
    Eq, Nl = nlin(r["omega"], r["v"])
    nl.append((Nl, r["omega"], r["v"], r["E0"]))
if nl:
    m = min(nl)
    out["min_Nlin_producing_survive"] = {"N_lin": m[0], "omega": m[1], "v": m[2], "E": m[3]}
json.dump(out, open("e1c_analysis.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("trend", "high_v", "example_0.99_0.43", "min_energy_producing")}, indent=1))
print("holes", holes[:10])
print("near (0.91,0.82)", probe)
print("omega>0.99", out.get("omega_gt_0.99"))
print("dx", out.get("dx_check"))

# ---------------------------------------------------------------- figure
fig = plt.figure(figsize=(7.4, 7.0))
ax = fig.add_axes([0.09, 0.42, 0.55, 0.53])
for r in runs:
    if r["survives_to_1.5T"]:
        ax.scatter(r["omega"], r["v"], marker="s", s=14, c="#d1495b", lw=0)
    elif r["produced_dsv"]:
        ax.scatter(r["omega"], r["v"], marker="s", s=14, facecolors="none", edgecolors="#d1495b", lw=0.8)
    else:
        ax.scatter(r["omega"], r["v"], marker=".", s=3, c="#9a9a9a")
if os.path.exists("e1c_high.json"):
    for r in hr:
        if r["v"] >= 0.4 - 1e-9:
            mk = dict(marker="s", s=14, c="#d1495b", lw=0) if r["survives_to_1.5T"] else (
                dict(marker="s", s=14, facecolors="none", edgecolors="#d1495b", lw=0.8) if r["produced_dsv"]
                else dict(marker=".", s=3, c="#9a9a9a"))
            ax.scatter(r["omega"], r["v"], **mk)
ax.scatter([0.99], [0.43], marker="o", s=60, facecolors="none", edgecolors="k", lw=1)
ax.scatter([0.91], [0.82], marker="D", s=50, facecolors="none", edgecolors="#1f6fb4", lw=1)
ax.set_xlabel("omega")
ax.set_ylabel("v")
ax.set_xlim(0.895, 0.998)
ax.set_ylim(0.39, 0.91)
ax.set_title("E1c: DSV trains, pair at t=T (filled: still there at 1.5T)", fontsize=8)
ax2 = fig.add_axes([0.72, 0.42, 0.25, 0.53])
d = np.load("e1c_example_spacetime.npz")
st, xs = d["st"], d["x"]
tt = np.arange(st.shape[0]) * float(d["dt_rec"])
ax2.imshow(st, origin="lower", aspect="auto", extent=[xs[0], xs[-1], tt[0], tt[-1]], cmap="RdBu_r",
           vmin=-1.3, vmax=1.3, interpolation="nearest")
ax2.axhline(1200, color="k", lw=0.6, ls="--")
ax2.set_xlim(-400, 400)
ax2.set_xlabel("x")
ax2.set_ylabel("t")
ax2.set_title("(0.99, 0.43): phi(x,t)", fontsize=8)
ax3 = fig.add_axes([0.09, 0.07, 0.86, 0.25])
for o in oms:
    pv = [r["v"] for r in runs if r["omega"] == o and r["produced_dsv"]]
    ax3.scatter([o] * len(pv), pv, s=4, c="#d1495b")
med = [(o, per_omega[f"{o:.2f}"]["dsv"]["v_median"]) for o in oms if per_omega[f"{o:.2f}"]["dsv"]["n"]]
if med:
    ax3.plot([m[0] for m in med], [m[1] for m in med], "k-o", ms=3, lw=1, label="median producing v")
ax3.set_xlabel("omega")
ax3.set_ylabel("producing v")
ax3.legend(fontsize=7)
fig.savefig("fig_e1c_dsv.png", dpi=105)
print("wrote fig_e1c_dsv.png")
