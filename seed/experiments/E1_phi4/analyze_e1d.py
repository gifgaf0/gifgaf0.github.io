"""Analyse E1d (colliding Gaussian packets): production vs energy, regions,
speed/width dependence, single-packet controls, slices, phase diagnostic.
Reads e1d_coarse.json, e1d_single.json, e1d_dxcheck.json, e1d_sliceAk_*.json,
e1d_sliceAs_*.json, e1d_phase.json (whichever exist).
Writes e1d_analysis.json, fig_e1d_coarse.png, fig_e1d_slices.png."""
import glob
import json
import os
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from phi4core import M_KINK

TWO_M = 2 * M_KINK
out = {}
co = json.load(open("e1d_coarse.json"))["runs"]
As = sorted(set(r["A"] for r in co))
Ss = sorted(set(r["sigma"] for r in co))
Ks = sorted(set(r["k"] for r in co))
key = {(r["A"], r["sigma"], r["k"]): r for r in co}
P = np.zeros((len(As), len(Ss), len(Ks)), bool)
E = np.zeros(P.shape)
for i, A in enumerate(As):
    for j, s in enumerate(Ss):
        for l, k in enumerate(Ks):
            r = key[(A, s, k)]
            P[i, j, l] = r["produced"]
            E[i, j, l] = r["E_over_2M"]
out["coarse_grid"] = {"A": As, "sigma": Ss, "k": Ks, "vg": [k / np.sqrt(k * k + 2) for k in Ks],
                      "n_runs": int(P.size), "n_produced": int(P.sum()),
                      "E_over_2M_range": [float(E.min()), float(E.max())]}

edges = np.array([0, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 64, 1e9])


def frac_vs_E(Ev, Pv):
    rows = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (Ev >= a) & (Ev < b)
        if m.sum():
            rows.append([float(a), float(b), int(m.sum()), int(Pv[m].sum()), float(Pv[m].mean())])
    return rows


out["coarse_frac_vs_E"] = frac_vs_E(E.ravel(), P.ravel())
prod_runs = [r for r in co if r["produced"]]
rmin = min(prod_runs, key=lambda r: r["E_over_2M"])
out["coarse_min_producing"] = {k: rmin[k] for k in ("A", "sigma", "k", "vg", "E", "E_over_2M", "N_lin", "E_quad")}
out["coarse_any_below_threshold"] = int(sum(1 for r in prod_runs if r["E_over_2M"] < 1.0))
out["coarse_frac_above_threshold"] = float(P[E >= 1].mean())
# connected regions
lab6, n6 = ndimage.label(P)
lab26, n26 = ndimage.label(P, structure=np.ones((3, 3, 3)))
sizes6 = sorted(np.bincount(lab6.ravel())[1:].tolist(), reverse=True)
out["coarse_regions"] = {"n_6conn": int(n6), "sizes_6conn": sizes6, "n_26conn": int(n26),
                         "sizes_26conn": sorted(np.bincount(lab26.ravel())[1:].tolist(), reverse=True)}
# monotonicity along A
flips = []
for j in range(len(Ss)):
    for l in range(len(Ks)):
        seq = P[:, j, l].astype(int)
        flips.append(int(np.sum(np.abs(np.diff(seq)))))
flips = np.array(flips)
out["coarse_A_lines"] = {"n_lines": int(flips.size), "lines_with_production": int(np.sum(P.any(axis=0))),
                         "lines_with_>1_flip(non-monotonic in A)": int(np.sum(flips > 1)),
                         "max_flips": int(flips.max())}
# speed and width dependence
sp = []
for l, k in enumerate(Ks):
    m = E[:, :, l] >= 1
    pk = P[:, :, l]
    pe = E[:, :, l][pk]
    sp.append({"k": k, "vg": k / np.sqrt(k * k + 2), "frac_all": float(pk.mean()),
               "frac_E_above_2M": float(pk[m].mean()) if m.sum() else None,
               "min_producing_E_over_2M": float(pe.min()) if pe.size else None,
               "frac_in_E_band_2_8": float(pk[(E[:, :, l] >= 2) & (E[:, :, l] < 8)].mean())
               if ((E[:, :, l] >= 2) & (E[:, :, l] < 8)).sum() else None})
out["coarse_vs_speed"] = sp
wd = []
for j, s in enumerate(Ss):
    m = E[:, j, :] >= 1
    ps = P[:, j, :]
    pe = E[:, j, :][ps]
    wd.append({"sigma": s, "frac_all": float(ps.mean()),
               "frac_E_above_2M": float(ps[m].mean()) if m.sum() else None,
               "min_producing_E_over_2M": float(pe.min()) if pe.size else None,
               "frac_in_E_band_2_8": float(ps[(E[:, j, :] >= 2) & (E[:, j, :] < 8)].mean())
               if ((E[:, j, :] >= 2) & (E[:, j, :] < 8)).sum() else None})
out["coarse_vs_width"] = wd
# logistic-style summary: fraction producing in (vg, E band) table
tab = []
bands = [(1, 2), (2, 4), (4, 8), (8, 16), (16, 64), (64, 1e9)]
for l, k in enumerate(Ks):
    row = []
    for a, b in bands:
        m = (E[:, :, l] >= a) & (E[:, :, l] < b)
        row.append([int(m.sum()), float(P[:, :, l][m].mean()) if m.sum() else None])
    tab.append({"k": k, "bands": row})
out["coarse_speed_x_energy"] = {"bands": bands, "rows": tab}
tabw = []
for j, s in enumerate(Ss):
    row = []
    for a, b in bands:
        m = (E[:, j, :] >= a) & (E[:, j, :] < b)
        row.append([int(m.sum()), float(P[:, j, :][m].mean()) if m.sum() else None])
    tabw.append({"sigma": s, "bands": row})
out["coarse_width_x_energy"] = {"bands": bands, "rows": tabw}
# initial data already reaching phi > 0 (A > 1 region)
pos0 = np.array([r["phi0_init_max"] > 0 for r in co])
Pv = np.array([r["produced"] for r in co])
out["coarse_initial_phi_positive"] = {"n_runs_phi_max>0_at_t0": int(pos0.sum()),
                                      "frac_produced_among_them": float(Pv[pos0].mean()) if pos0.sum() else None,
                                      "frac_produced_among_rest": float(Pv[~pos0].mean()),
                                      "n_produced_with_phi_max<0_at_t0": int(Pv[~pos0].sum())}
# single-packet controls
if os.path.exists("e1d_single.json"):
    sg = json.load(open("e1d_single.json"))["runs"]
    sp_prod = [r for r in sg if r["produced"]]
    out["single_packet_controls"] = {"n_tested(=producing pair runs)": len(sg),
                                     "n_single_packet_also_produces": len(sp_prod),
                                     "examples": [(r["A"], r["sigma"], r["k"]) for r in sp_prod[:10]]}
    sset = {(r["A"], r["sigma"], r["k"]) for r in sp_prod}
    coll = [r for r in prod_runs if (r["A"], r["sigma"], r["k"]) not in sset]
    if coll:
        rmc = min(coll, key=lambda r: r["E_over_2M"])
        out["coarse_min_producing_collision_only"] = {k: rmc[k] for k in ("A", "sigma", "k", "vg", "E", "E_over_2M", "N_lin")}
# dx check
if os.path.exists("e1d_dxcheck.json"):
    dc = json.load(open("e1d_dxcheck.json"))["runs"]
    ag = [r["produced"] == key[(r["A"], r["sigma"], r["k"])]["produced"] for r in dc]
    out["dx_check"] = {"n": len(ag), "agree_frac": float(np.mean(ag)),
                       "n_prod_dx0.05": int(sum(r["produced"] for r in dc)),
                       "n_prod_dx0.1_same_points": int(sum(key[(r["A"], r["sigma"], r["k"])]["produced"] for r in dc)),
                       "disagreements": [(r["A"], r["sigma"], r["k"], r["produced"], round(r["E_over_2M"], 2)) for r in dc
                                         if r["produced"] != key[(r["A"], r["sigma"], r["k"])]["produced"]]}

# ---------------------------------------------------------------- slices
slices = {}
for fn in sorted(glob.glob("e1d_slice*.json")):
    d = json.load(open(fn))
    rr = d["runs"]
    if d["mode"] == "sliceAk":
        ax2 = "k"
    else:
        ax2 = "sigma"
    xa = sorted(set(r["A"] for r in rr))
    ya = sorted(set(r[ax2] for r in rr))
    kk = {(r["A"], r[ax2]): r for r in rr}
    Pm = np.array([[kk[(a, y)]["produced"] for y in ya] for a in xa])
    Em = np.array([[kk[(a, y)]["E_over_2M"] for y in ya] for a in xa])
    l4, n4 = ndimage.label(Pm)
    l8, n8 = ndimage.label(Pm, structure=np.ones((3, 3)))
    s4 = sorted(np.bincount(l4.ravel())[1:].tolist(), reverse=True)
    s8 = sorted(np.bincount(l8.ravel())[1:].tolist(), reverse=True)
    fl = np.sum(np.abs(np.diff(Pm.astype(int), axis=0)), axis=0)
    # holes: non-producing connected regions not touching the low-A edge (enclosed gaps)
    lno, nno = ndimage.label(~Pm)
    enclosed = [i for i in range(1, nno + 1) if not np.any(lno[0, :] == i) and not np.any(lno[:, 0] == i)
                and not np.any(lno[:, -1] == i) and not np.any(lno[-1, :] == i)]
    pr = [r for r in rr if r["produced"]]
    mn = min(pr, key=lambda r: r["E_over_2M"]) if pr else None
    slices[os.path.basename(fn)] = {
        "mode": d["mode"], "fixed": d["args"], "n_runs": len(rr), "n_produced": int(Pm.sum()),
        "A_range": [xa[0], xa[-1], len(xa)], f"{ax2}_range": [ya[0], ya[-1], len(ya)],
        "regions_4conn": int(n4), "region_sizes_4conn_top10": s4[:10], "n_singleton_regions_4conn": int(sum(1 for s in s4 if s == 1)),
        "regions_8conn": int(n8), "region_sizes_8conn_top10": s8[:10],
        "enclosed_nonproducing_holes": len(enclosed),
        "frac_vs_E": frac_vs_E(Em.ravel(), Pm.ravel()),
        "A_lines": {"n": int(fl.size), "with_production": int(np.sum(Pm.any(axis=0))),
                    "non_monotonic(>1 flip)": int(np.sum(fl > 1)), "max_flips": int(fl.max()),
                    "mean_flips_on_producing_lines": float(fl[Pm.any(axis=0)].mean()) if Pm.any() else None},
        "min_producing": {k: mn[k] for k in ("A", "sigma", "k", "vg", "E_over_2M", "N_lin")} if mn else None,
        "runtime_s": d["runtime_s"]}
    slices[os.path.basename(fn)]["_maps"] = (xa, ya, Pm, Em, ax2)
out["slices"] = {k: {kk2: v for kk2, v in s.items() if kk2 != "_maps"} for k, s in slices.items()}

if os.path.exists("e1d_phase.json"):
    ph = json.load(open("e1d_phase.json"))["runs"]
    pts = {}
    for r in ph:
        pts.setdefault((r["A"], r["k"]), []).append(r["produced"])
    fr = np.array([np.mean(v) for v in pts.values()])
    out["phase_diagnostic"] = {"n_points": len(pts), "shifts_per_point": 8,
                               "n_points_outcome_depends_on_phase": int(np.sum((fr > 0) & (fr < 1))),
                               "n_always": int(np.sum(fr == 1)), "n_never": int(np.sum(fr == 0)),
                               "mean_production_fraction": float(fr.mean())}

# E1e numbers from Gaussian runs
allprod = prod_runs[:]
for fn, s in slices.items():
    pass
gp = []
for fn in glob.glob("e1d_slice*.json"):
    gp += [r for r in json.load(open(fn))["runs"] if r["produced"]]
gp += prod_runs
rE = min(gp, key=lambda r: r["E"])
rN = min(gp, key=lambda r: r["N_lin"])
out["quanta"] = {"min_E_producing": {k: rE[k] for k in ("A", "sigma", "k", "E", "E_over_2M", "N_lin")},
                 "min_E_producing_N_E_over_m": rE["E"] / np.sqrt(2),
                 "min_Nlin_producing": {k: rN[k] for k in ("A", "sigma", "k", "E", "E_over_2M", "N_lin")}}

json.dump(out, open("e1d_analysis.json", "w"), indent=1)
pr = {k: v for k, v in out.items() if k not in ("coarse_speed_x_energy", "coarse_width_x_energy")}
print(json.dumps(pr, indent=1)[:12000])

# ---------------------------------------------------------------- figures
fig, axs = plt.subplots(2, 2, figsize=(7.6, 6.2))
ax = axs[0, 0]
fe = out["coarse_frac_vs_E"]
xc = [np.sqrt(max(a, 0.25) * min(b, 128)) for a, b, n, m, f in fe]
ax.semilogx(xc, [f for a, b, n, m, f in fe], "o-", c="#d1495b", ms=4, label="coarse 3D grid")
for fn, s in slices.items():
    fs = s["frac_vs_E"]
    ax.semilogx([np.sqrt(max(a, 0.25) * min(b, 128)) for a, b, n, m, f in fs], [f for a, b, n, m, f in fs], "s--",
                ms=3, lw=0.8, label=fn.replace("e1d_", "").replace(".json", ""))
ax.axvline(1, color="k", ls=":", lw=0.8)
ax.set_xlabel("E / 2M_kink")
ax.set_ylabel("fraction producing")
ax.legend(fontsize=6)
ax.set_title("production vs energy", fontsize=8)
ax = axs[0, 1]
for row in out["coarse_speed_x_energy"]["rows"]:
    pass
vg = [s["vg"] for s in sp]
ax.plot(vg, [s["frac_E_above_2M"] for s in sp], "o-", c="#1f6fb4", ms=4, label="all E > 2M")
ax.plot(vg, [s["frac_in_E_band_2_8"] for s in sp], "s--", c="#66a182", ms=4, label="2 < E/2M < 8")
ax.set_xlabel("group velocity k/omega_k")
ax.set_ylabel("fraction producing")
ax.legend(fontsize=7)
ax.set_title("speed dependence (coarse grid)", fontsize=8)
ax = axs[1, 0]
ax.semilogx(Ss, [s["frac_E_above_2M"] for s in wd], "o-", c="#1f6fb4", ms=4, label="all E > 2M")
ax.semilogx(Ss, [s["frac_in_E_band_2_8"] for s in wd], "s--", c="#66a182", ms=4, label="2 < E/2M < 8")
ax.set_xlabel("packet width sigma")
ax.set_ylabel("fraction producing")
ax.legend(fontsize=7)
ax.set_title("width dependence (coarse grid)", fontsize=8)
ax = axs[1, 1]
ax.semilogx(vg and Ks, [s["min_producing_E_over_2M"] for s in sp], "o-", c="#1f6fb4", ms=4, label="vs k")
ax2 = ax.twiny()
ax2.semilogx(Ss, [s["min_producing_E_over_2M"] for s in wd], "s--", c="#edae49", ms=4, label="vs sigma")
ax.set_xlabel("k (circles)")
ax2.set_xlabel("sigma (squares)", fontsize=8)
ax.set_ylabel("min producing E/2M")
ax.set_title("lowest producing energy", fontsize=8, pad=18)
fig.tight_layout()
fig.savefig("fig_e1d_coarse.png", dpi=100)

if slices:
    n = len(slices)
    fig, axs = plt.subplots(1, n, figsize=(3.8 * n, 3.6), squeeze=False)
    for ax, (fn, s) in zip(axs[0], slices.items()):
        xa, ya, Pm, Em, ax2n = s["_maps"]
        X, Y = np.meshgrid(ya, xa)
        ax.pcolormesh(Y if False else np.array(ya), np.array(xa), Pm.astype(float), cmap="Reds", vmin=0, vmax=1.3,
                      shading="nearest")
        cs = ax.contour(np.array(ya), np.array(xa), Em, levels=[1, 2, 4, 8, 16, 32], colors="k", linewidths=0.6)
        ax.clabel(cs, fontsize=6, fmt="%g")
        if ax2n == "sigma":
            ax.set_xscale("log")
        ax.set_xlabel(ax2n)
        ax.set_ylabel("A")
        ax.set_title(f"{s['mode']} at {s['fixed']}: red = pair; contours E/2M", fontsize=7)
    fig.tight_layout()
    fig.savefig("fig_e1d_slices.png", dpi=100)
print("figures written")
