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
Pc = None
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
    Pc = np.zeros(P.shape, bool)
    for i, A in enumerate(As):
        for j, s_ in enumerate(Ss):
            for l, k in enumerate(Ks):
                Pc[i, j, l] = P[i, j, l] and (A, s_, k) not in sset
    out["coarse_collision_needed"] = {"n": int(Pc.sum()), "frac_vs_E": frac_vs_E(E.ravel(), Pc.ravel()),
                                      "single_also_frac_vs_E": frac_vs_E(E.ravel(), (P & ~Pc).ravel())}
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
for fn in sorted(f for f in glob.glob("e1d_slice*.json") if not f.endswith("_single.json")):
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
    # single-packet controls on the producing points (e1d_single_slices.py)
    Sm = np.zeros_like(Pm)
    sfn = fn.replace(".json", "_single.json")
    if os.path.exists(sfn):
        sk = {(r["A"], r[ax2]): r["single_produced"] for r in json.load(open(sfn))["runs"]}
        Sm = np.array([[bool(sk.get((a, y), False)) for y in ya] for a in xa]) & Pm
        Cm = Pm & ~Sm
        lc4, nc4 = ndimage.label(Cm)
        sc4 = sorted(np.bincount(lc4.ravel())[1:].tolist(), reverse=True)
        flc = np.sum(np.abs(np.diff(Cm.astype(int), axis=0)), axis=0)
        slices[os.path.basename(fn)]["single_packet"] = {
            "n_producing": int(Pm.sum()), "n_single_also_produces": int(Sm.sum()),
            "n_collision_needed": int(Cm.sum()),
            "collision_needed_regions_4conn": int(nc4), "collision_needed_region_sizes_top10": sc4[:10],
            "collision_needed_singletons": int(sum(1 for z in sc4 if z == 1)),
            "collision_needed_frac_vs_E": frac_vs_E(Em.ravel(), Cm.ravel()),
            "collision_needed_A_lines_non_monotonic": int(np.sum(flc > 1)),
            "collision_needed_A_lines_with_production": int(np.sum(Cm.any(axis=0))),
            "min_E_over_2M_collision_needed": float(Em[Cm].min()) if Cm.any() else None,
            "min_E_over_2M_single_also": float(Em[Sm].min()) if Sm.any() else None,
            "min_A_single_also": float(min(xa[i] for i in np.where(Sm.any(axis=1))[0])) if Sm.any() else None}
    slices[os.path.basename(fn)]["_maps"] = (xa, ya, Pm, Em, ax2, Sm)
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
for fn in sorted(f for f in glob.glob("e1d_slice*.json") if not f.endswith("_single.json")):
    gp += [r for r in json.load(open(fn))["runs"] if r["produced"]]
gp += prod_runs
rE = min(gp, key=lambda r: r["E"])
rN = min(gp, key=lambda r: r["N_lin"])
out["quanta"] = {"min_E_producing": {k: rE[k] for k in ("A", "sigma", "k", "E", "E_over_2M", "N_lin")},
                 "min_E_producing_N_E_over_m": rE["E"] / np.sqrt(2),
                 "min_Nlin_producing": {k: rN[k] for k in ("A", "sigma", "k", "E", "E_over_2M", "N_lin")}}

# ---------------------------------------------------------------- operational tests of the E1d predictions
# Fixed during the run, after the coarse scan and before the 2D slices were inspected (PLAN.md gives
# no numerical definition of "ragged"; see REPORT.md, Deviations).
#  ragged:  a single clean threshold in a 2D slice means production iff A > A_c(y): one producing
#           4-connected region and every A-line with at most one 0->1 change.  CONFIRMED if, in at least
#           one slice, >= 20% of the A-lines that contain production are non-monotonic (>1 change) or there
#           are >= 3 producing regions of >= 3 points; REFUTED if every slice has one region (ignoring
#           singletons) and <= 5% non-monotonic lines; otherwise AMENDED.
#  speed:   at matched energy, fraction producing vs group velocity (coarse grid, E/2M bands [2,4),[4,8),
#           [8,16)); Spearman over the 9 speeds in each band. "favours low speed" if rho < 0 with p < 0.05
#           in the majority of bands.
#  width:   same with sigma (11 widths); "favours wide packets" if rho > 0 with p < 0.05 in the majority.
from scipy.stats import spearmanr
tests = {}
rag = []
for fn, s in out["slices"].items():
    lines = s["A_lines"]
    frac_nm = lines["non_monotonic(>1 flip)"] / max(1, lines["with_production"])
    big = [z for z in s["region_sizes_4conn_top10"] if z >= 3]
    rag.append({"slice": fn, "frac_nonmonotonic_A_lines": frac_nm, "n_regions_ge3": len(big),
                "n_regions_ignoring_singletons": len([z for z in s["region_sizes_4conn_top10"] if z >= 2])})
if rag:
    conf = any(r["frac_nonmonotonic_A_lines"] >= 0.2 or r["n_regions_ge3"] >= 3 for r in rag)
    refu = all(r["n_regions_ignoring_singletons"] <= 1 and r["frac_nonmonotonic_A_lines"] <= 0.05 for r in rag)
    tests["ragged"] = {"per_slice": rag, "verdict": "CONFIRMED" if conf else ("REFUTED" if refu else "AMENDED")}
# same test on the collision-needed production only (pair run produces, single packet alone does not)
ragc = []
for fn, s in out["slices"].items():
    sp_ = s.get("single_packet")
    if not sp_:
        continue
    frac_nm = sp_["collision_needed_A_lines_non_monotonic"] / max(1, sp_["collision_needed_A_lines_with_production"])
    sz = sp_["collision_needed_region_sizes_top10"]
    ragc.append({"slice": fn, "frac_nonmonotonic_A_lines": frac_nm, "n_regions_ge3": len([z for z in sz if z >= 3]),
                 "n_regions_ignoring_singletons": len([z for z in sz if z >= 2]),
                 "n_regions_total": sp_["collision_needed_regions_4conn"]})
if ragc:
    conf = any(r["frac_nonmonotonic_A_lines"] >= 0.2 or r["n_regions_ge3"] >= 3 for r in ragc)
    refu = all(r["n_regions_ignoring_singletons"] <= 1 and r["frac_nonmonotonic_A_lines"] <= 0.05 for r in ragc)
    tests["ragged_collision_needed"] = {"per_slice": ragc,
                                        "verdict": "CONFIRMED" if conf else ("REFUTED" if refu else "AMENDED")}
bands_t = [(2, 4), (4, 8), (8, 16)]
PSETS = [("", P)]
if "coarse_collision_needed" in out:
    PSETS.append(("_collision_needed", Pc))
for (suffix, PP), (name, axis_vals, axis) in [(ps, ax_) for ps in PSETS for ax_ in
                                               (("speed", [k / np.sqrt(k * k + 2) for k in Ks], 2), ("width", Ss, 1))]:
    P_ = PP
    rows = []
    for a, b in bands_t:
        xs, fs, ns = [], [], []
        for idx, val in enumerate(axis_vals):
            if axis == 2:
                Ee, Pp = E[:, :, idx], P_[:, :, idx]
            else:
                Ee, Pp = E[:, idx, :], P_[:, idx, :]
            m = (Ee >= a) & (Ee < b)
            if m.sum() >= 3:
                xs.append(val)
                fs.append(float(Pp[m].mean()))
                ns.append(int(m.sum()))
        rho = spearmanr(xs, fs) if len(xs) > 2 else None
        rows.append({"E_band": [a, b], "x": xs, "frac": fs, "n": ns,
                     "spearman": [float(rho[0]), float(rho[1])] if rho is not None else None})
    sign = -1 if name == "speed" else 1
    good = sum(1 for r in rows if r["spearman"] and np.isfinite(r["spearman"][0])
               and sign * r["spearman"][0] > 0 and r["spearman"][1] < 0.05)
    bad = sum(1 for r in rows if r["spearman"] and np.isfinite(r["spearman"][0])
              and sign * r["spearman"][0] < 0 and r["spearman"][1] < 0.05)
    tests[name + suffix] = {"rows": rows, "bands_supporting": good, "bands_contradicting": bad,
                   "verdict": "CONFIRMED" if good >= 2 else ("REFUTED" if bad >= 2 else "NOT_SUPPORTED")}
out["prediction_tests"] = tests
print("prediction tests:", json.dumps(tests, indent=1))

json.dump(out, open("e1d_analysis.json", "w"), indent=1)
pr ={k: v for k, v in out.items() if k not in ("coarse_speed_x_energy", "coarse_width_x_energy")}
print(json.dumps(pr, indent=1)[:12000])

# ---------------------------------------------------------------- figures
fig, axs = plt.subplots(2, 2, figsize=(7.6, 6.2))
ax = axs[0, 0]
fe = out["coarse_frac_vs_E"]
xc = [np.sqrt(max(a, 0.25) * min(b, 128)) for a, b, n, m, f in fe]
ax.semilogx(xc, [f for a, b, n, m, f in fe], "o-", c="#d1495b", ms=4, label="coarse 3D grid, all pairs")
if "coarse_collision_needed" in out:
    fc = out["coarse_collision_needed"]["frac_vs_E"]
    ax.semilogx(xc, [f for a, b, n, m, f in fc], "^-", c="#edae49", ms=4, label="coarse, collision needed")
for (fn, s), col in zip(slices.items(), ("#1f6fb4", "#555555")):
    fs = s["frac_vs_E"]
    ax.semilogx([np.sqrt(max(a, 0.25) * min(b, 128)) for a, b, n, m, f in fs], [f for a, b, n, m, f in fs], "s--",
                ms=3, lw=0.8, c=col, label=fn.replace("e1d_", "").replace(".json", "") + ", all pairs")
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
# fraction producing among runs with E > 2M, per (sigma, k) cell (one axis per variable; no twin axes)
Fm = np.full((len(Ss), len(Ks)), np.nan)
for j in range(len(Ss)):
    for l in range(len(Ks)):
        m = E[:, j, l] >= 1
        if m.sum():
            Fm[j, l] = P[:, j, l][m].mean()
im = ax.imshow(Fm, origin="lower", aspect="auto", cmap="Reds", vmin=0, vmax=1)
ax.set_xticks(range(len(Ks)))
ax.set_xticklabels([f"{k / np.sqrt(k * k + 2):.2f}" for k in Ks], fontsize=6)
ax.set_yticks(range(len(Ss)))
ax.set_yticklabels([f"{s:g}" for s in Ss], fontsize=6)
ax.set_xlabel("group velocity k/omega_k")
ax.set_ylabel("sigma")
cb = fig.colorbar(im, ax=ax, fraction=0.05)
cb.ax.tick_params(labelsize=6)
ax.set_title("fraction producing (runs with E > 2M), over A", fontsize=8)
fig.tight_layout()
fig.savefig("fig_e1d_coarse.png", dpi=100)

if slices:
    n = len(slices)
    fig, axs = plt.subplots(1, n, figsize=(3.9 * n, 4.0), squeeze=False)
    for ax, (fn, s) in zip(axs[0], slices.items()):
        xa, ya, Pm, Em, ax2n, Sm = s["_maps"]
        X, Y = np.meshgrid(ya, xa)
        from matplotlib.colors import ListedColormap
        from matplotlib.patches import Patch
        cat = np.where(Sm, 2, np.where(Pm, 1, 0)).astype(float)
        cmap3 = ListedColormap(["#eeeeee", "#edae49", "#a4243b"])
        ax.pcolormesh(np.array(ya), np.array(xa), cat, cmap=cmap3, vmin=-0.5, vmax=2.5, shading="nearest")
        handles = [Patch(color="#edae49", label="pair; the single packet alone makes none (collision needed)"),
                   Patch(color="#a4243b", label="pair; the single packet alone also folds into a pair"),
                   Patch(color="#eeeeee", label="no pair")]
        cs = ax.contour(np.array(ya), np.array(xa), Em, levels=[1, 2, 4, 8, 16, 32], colors="k", linewidths=0.6)
        ax.clabel(cs, fontsize=6, fmt="%g")
        if ax2n == "sigma":
            ax.set_xscale("log")
        ax.set_xlabel(ax2n)
        ax.set_ylabel("A")
        ax.set_title(f"{s['mode']} at {'sigma' if s['mode'] == 'sliceAk' else 'k'}={s['fixed'][0]}; contours: E/2M_kink", fontsize=7)
    fig.legend(handles=handles, fontsize=6.5, loc="lower center", ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig("fig_e1d_slices.png", dpi=100)
print("figures written")
