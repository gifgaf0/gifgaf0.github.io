"""Analyse the robustness runs added by the resumed attempt (not preregistered):
  e1_verify.json            reproducibility, energy conservation, single-packet convergence
  e1b_boxcheck.json         v_c and window-1 edges in larger boxes
  e1d_coarse_oneway.jsonl   coarse grid with exact one-way initial velocity (+ single_oneway controls)
  e1d_slice_dx05.jsonl      k = 1 (A, sigma) slice at dx = 0.05 (+ slice_dx05_single controls)
  e1d_dxladder.json         point-level convergence ladder dx = 0.1, 0.05, 0.025, 0.0125
Writes e1_extra_analysis.json and fig_e1d_convergence.png. Missing inputs are skipped."""
import json
import os
import numpy as np
from scipy import ndimage
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

EDGES = np.array([0, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 64, 1e9])
out = {}


def jl(fn):
    return [json.loads(l) for l in open(fn)] if os.path.exists(fn) else None


def frac_vs_E(Ev, Pv):
    rows = []
    for a, b in zip(EDGES[:-1], EDGES[1:]):
        m = (Ev >= a) & (Ev < b)
        if m.sum():
            rows.append([float(a), float(b), int(m.sum()), int(Pv[m].sum()), float(Pv[m].mean())])
    return rows


def slice_metrics(Pm, Em):
    """Same definitions as analyze_e1d.py (4-connected regions, enclosed holes, A-line switches)."""
    l4, n4 = ndimage.label(Pm)
    s4 = sorted(np.bincount(l4.ravel())[1:].tolist(), reverse=True)
    fl = np.sum(np.abs(np.diff(Pm.astype(int), axis=0)), axis=0)
    lno, nno = ndimage.label(~Pm)
    enclosed = [i for i in range(1, nno + 1) if not np.any(lno[0, :] == i) and not np.any(lno[:, 0] == i)
                and not np.any(lno[:, -1] == i) and not np.any(lno[-1, :] == i)]
    withp = Pm.any(axis=0)
    return {"n_produced": int(Pm.sum()), "regions_4conn": int(n4), "singletons_4conn": int(sum(1 for z in s4 if z == 1)),
            "regions_ge3": int(sum(1 for z in s4 if z >= 3)), "region_sizes_top5": s4[:5],
            "enclosed_holes": len(enclosed), "A_lines_with_production": int(withp.sum()),
            "A_lines_non_monotonic": int(np.sum(fl > 1)),
            "frac_non_monotonic": float(np.sum(fl > 1) / max(1, withp.sum())),
            "mean_switches_on_producing_lines": float(fl[withp].mean()) if withp.any() else None,
            "frac_vs_E": frac_vs_E(Em.ravel(), Pm.ravel())}


def ragged_verdict(m):
    return "CONFIRMED" if (m["frac_non_monotonic"] >= 0.2 or m["regions_ge3"] >= 3) else (
        "REFUTED" if (m["regions_4conn"] - m["singletons_4conn"] <= 1 and m["frac_non_monotonic"] <= 0.05) else "AMENDED")


# ---------------------------------------------------------------- verify
if os.path.exists("e1_verify.json"):
    v = json.load(open("e1_verify.json"))
    v3 = {}
    for r in v["V3_single_packet_convergence"]:
        v3.setdefault(f"A={r['A']},sigma={r['sigma']},k={r['k']},single={r['single']}", []).append(
            {"dx": r["dx"], "dt": round(r["dx"] * r["cfl"], 5), "produced": r["produced"], "pair_since": r["pair_since"]})
    out["verify"] = {"reproducibility_gauss_all_agree": v["V1_reproducibility"]["all_gauss_agree"],
                     "reproducibility_kkbar_all_agree": v["V1_reproducibility"]["all_kkbar_agree"],
                     "n_gauss_rerun": len(v["V1_reproducibility"]["gauss"]),
                     "n_kkbar_rerun": len(v["V1_reproducibility"]["kkbar"]),
                     "energy_drift": {e["kind"]: e["max_rel_drift"] for e in v["V2_energy_conservation"]},
                     "single_packet_convergence": v3}

# ---------------------------------------------------------------- box check
if os.path.exists("e1b_boxcheck.json"):
    bc = json.load(open("e1b_boxcheck.json"))
    out["boxcheck"] = {"reference_box40": bc["reference_box40_W30_dx0.05_dt0.01"],
                       "cases": [{k: c[k] for k in ("Lphys", "W", "transition", "v", "shift_vs_box40")} for c in bc["cases"]],
                       "max_abs_shift": float(max(abs(c["shift_vs_box40"]) for c in bc["cases"]))}

# ---------------------------------------------------------------- one-way coarse grid
co = {(r["A"], r["sigma"], r["k"]): r for r in json.load(open("e1d_coarse.json"))["runs"]}
ow = jl("e1d_coarse_oneway.jsonl")
fig_ow = None
if ow and len(ow) == len(co):
    so = jl("e1d_single_oneway.jsonl") or []
    sset = {(r["A"], r["sigma"], r["k"]) for r in so if r["produced"]}
    E = np.array([r["E_over_2M"] for r in ow])
    P = np.array([r["produced"] for r in ow])
    Pb = np.array([co[(r["A"], r["sigma"], r["k"])]["produced"] for r in ow])
    Eb = np.array([co[(r["A"], r["sigma"], r["k"])]["E_over_2M"] for r in ow])
    C = np.array([r["produced"] and (r["A"], r["sigma"], r["k"]) not in sset for r in ow])
    prod = [r for r in ow if r["produced"]]
    rmin = min(prod, key=lambda r: r["E_over_2M"])
    coll = [r for r in prod if (r["A"], r["sigma"], r["k"]) not in sset]
    rminc = min(coll, key=lambda r: r["E_over_2M"]) if coll else None
    # matched-energy speed and width tests (same rule as analyze_e1d.py)
    Ks = sorted(set(r["k"] for r in ow))
    Ss = sorted(set(r["sigma"] for r in ow))
    tests = {}
    for name, vals, field in (("speed", Ks, "k"), ("width", Ss, "sigma")):
        for suffix, PP in (("", P), ("_collision_needed", C)):
            rows = []
            for a, b in ((2, 4), (4, 8), (8, 16)):
                xs, fs = [], []
                for val in vals:
                    m = np.array([r[field] == val for r in ow]) & (E >= a) & (E < b)
                    if m.sum() >= 3:
                        xs.append(val / np.sqrt(val * val + 2) if field == "k" else val)
                        fs.append(float(PP[m].mean()))
                rho = spearmanr(xs, fs) if len(xs) > 2 else None
                rows.append({"E_band": [a, b], "x": xs, "frac": fs,
                             "spearman": [float(rho[0]), float(rho[1])] if rho is not None else None})
            sign = -1 if name == "speed" else 1
            good = sum(1 for r in rows if r["spearman"] and np.isfinite(r["spearman"][0]) and sign * r["spearman"][0] > 0
                       and r["spearman"][1] < 0.05)
            bad = sum(1 for r in rows if r["spearman"] and np.isfinite(r["spearman"][0]) and sign * r["spearman"][0] < 0
                      and r["spearman"][1] < 0.05)
            tests[name + suffix] = {"rows": rows, "verdict": "CONFIRMED" if good >= 2 else ("REFUTED" if bad >= 2 else "NOT_SUPPORTED")}
    out["coarse_oneway"] = {
        "n_runs": len(ow), "n_produced": int(P.sum()), "n_produced_baseline": int(Pb.sum()),
        "point_agreement_with_baseline": float(np.mean(P == Pb)),
        "agreement_by_k_sigma_product": {
            "k*sigma<2": float(np.mean((P == Pb)[np.array([r["k"] * r["sigma"] < 2 for r in ow])])),
            "k*sigma>=2": float(np.mean((P == Pb)[np.array([r["k"] * r["sigma"] >= 2 for r in ow])]))},
        "energy_rel_change_vs_baseline_median": float(np.median(np.abs(E - Eb) / Eb)),
        "any_below_2M": int(np.sum(P & (E < 1))),
        "min_producing": {k: rmin[k] for k in ("A", "sigma", "k", "E_over_2M", "N_lin")} | {
            "single_packet_also": (rmin["A"], rmin["sigma"], rmin["k"]) in sset},
        "min_producing_collision_needed": {k: rminc[k] for k in ("A", "sigma", "k", "E_over_2M", "N_lin")} if rminc else None,
        "n_single_packet_also": int(len(sset)), "n_collision_needed": int(C.sum()),
        "frac_vs_E": frac_vs_E(E, P), "frac_vs_E_baseline": frac_vs_E(Eb, Pb),
        "collision_needed_frac_vs_E": frac_vs_E(E, C), "tests": tests,
        "regions_note": "see e1d_analysis.json for the baseline 3D region count"}
    lab = np.zeros((15, 11, 9), bool)
    As = sorted(set(r["A"] for r in ow))
    for r in ow:
        lab[As.index(r["A"]), Ss.index(r["sigma"]), Ks.index(r["k"])] = r["produced"]
    l6, n6 = ndimage.label(lab)
    out["coarse_oneway"]["regions_6conn"] = {"n": int(n6), "sizes": sorted(np.bincount(l6.ravel())[1:].tolist(), reverse=True)}
    fig_ow = (frac_vs_E(E, P), frac_vs_E(Eb, Pb), frac_vs_E(E, C))

# ---------------------------------------------------------------- dx = 0.05 slice
sl = jl("e1d_slice_dx05.jsonl")
base = json.load(open("e1d_sliceAs_1.0.json"))["runs"]
maps = None
if sl and len(sl) == len(base):
    xa = sorted(set(r["A"] for r in base))
    ya = sorted(set(r["sigma"] for r in base))
    kb = {(r["A"], r["sigma"]): r for r in base}
    kf = {(r["A"], r["sigma"]): r for r in sl}
    Pb = np.array([[kb[(a, y)]["produced"] for y in ya] for a in xa])
    Pf = np.array([[kf[(a, y)]["produced"] for y in ya] for a in xa])
    Em = np.array([[kb[(a, y)]["E_over_2M"] for y in ya] for a in xa])
    mb, mf = slice_metrics(Pb, Em), slice_metrics(Pf, Em)
    res = {"dx0.1": mb, "dx0.05": mf, "point_agreement": float(np.mean(Pb == Pf)),
           "ragged_verdict_dx0.1": ragged_verdict(mb), "ragged_verdict_dx0.05": ragged_verdict(mf)}
    # agreement after smoothing: production fraction in 4x4 blocks
    nb = 4
    fb = np.array([[Pb[i:i + nb, j:j + nb].mean() for j in range(0, Pb.shape[1] - nb + 1, nb)]
                   for i in range(0, Pb.shape[0] - nb + 1, nb)])
    ff = np.array([[Pf[i:i + nb, j:j + nb].mean() for j in range(0, Pf.shape[1] - nb + 1, nb)]
                   for i in range(0, Pf.shape[0] - nb + 1, nb)])
    res["block4x4_fraction_mean_abs_diff"] = float(np.mean(np.abs(fb - ff)))
    res["block4x4_fraction_corr"] = float(np.corrcoef(fb.ravel(), ff.ravel())[0, 1])
    ss = jl("e1d_slice_dx05_single.jsonl")
    Sf = np.zeros_like(Pf)
    if ss is not None and len(ss) == int(Pf.sum()):
        sk = {(r["A"], r["sigma"]): r["produced"] for r in ss}
        Sf = np.array([[bool(sk.get((a, y), False)) for y in ya] for a in xa]) & Pf
        Cf = Pf & ~Sf
        mc = slice_metrics(Cf, Em)
        res["dx0.05_collision_needed"] = mc
        res["ragged_verdict_dx0.05_collision_needed"] = ragged_verdict(mc)
        res["dx0.05_n_single_also"] = int(Sf.sum())
        # baseline collision-needed for comparison
        bs = json.load(open("e1d_sliceAs_1.0_single.json"))["runs"]
        skb = {(r["A"], r["sigma"]): r["single_produced"] for r in bs}
        Sb = np.array([[bool(skb.get((a, y), False)) for y in ya] for a in xa]) & Pb
        res["dx0.1_collision_needed_n"] = int((Pb & ~Sb).sum())
        res["dx0.1_n_single_also"] = int(Sb.sum())
        res["single_also_point_agreement"] = float(np.mean(Sb == Sf))
    out["slice_k1_dx0.05"] = res
    maps = (xa, ya, Pb, Pf, Em, Sf)

# ---------------------------------------------------------------- dx ladder
if os.path.exists("e1d_dxladder.json"):
    out["dxladder"] = json.load(open("e1d_dxladder.json"))["summary"]
    rows_ = json.load(open("e1d_dxladder.json"))["rows"]
    out["dxladder"]["rows"] = rows_
    for grp, sel in (("changed_0.1_vs_0.05", [r for r in rows_ if r["dx0.1"] != r["dx0.05"]]),
                     ("unchanged_0.1_vs_0.05", [r for r in rows_ if r["dx0.1"] == r["dx0.05"]])):
        out["dxladder"][grp] = {"n": len(sel),
                                "agree_0.05_0.025": float(np.mean([r["dx0.05"] == r["dx0.025"] for r in sel])),
                                "agree_0.025_0.0125": float(np.mean([r["dx0.025"] == r["dx0.0125"] for r in sel])),
                                "producing_fraction_by_dx": {k: float(np.mean([r[k] for r in sel]))
                                                             for k in ("dx0.1", "dx0.05", "dx0.025", "dx0.0125")}}

# ---------------------------------------------------------------- census: any producing run below 2M?
cen = {"n_runs": 0, "n_producing": 0, "n_producing_below_2M": 0, "min_E_over_2M_producing_pair_runs": None,
       "min_E_over_2M_producing_single_packets": None, "files": []}
def _acc(rows, single_E_half=False, single=False):
    for r in rows:
        if "produced" in r:
            p = r["produced"]
        elif "single_produced" in r:
            p = r["single_produced"]
        else:
            continue
        e = r.get("E_over_2M")
        cen["n_runs"] += 1
        if not p:
            continue
        cen["n_producing"] += 1
        if e is None:
            continue
        if single_E_half:
            e = 0.5 * e
        if e < 1.0:
            cen["n_producing_below_2M"] += 1
        key = "min_E_over_2M_producing_single_packets" if (single or r.get("single")) else "min_E_over_2M_producing_pair_runs"
        cen[key] = e if cen[key] is None else min(cen[key], e)
for fn in ("e1d_coarse.json", "e1d_dxcheck.json", "e1d_phase.json", "e1d_single.json", "e1d_sliceAk_16.0.json",
           "e1d_sliceAs_1.0.json"):
    _acc(json.load(open(fn))["runs"])
    cen["files"].append(fn)
for fn in ("e1d_sliceAk_16.0_single.json", "e1d_sliceAs_1.0_single.json"):
    pair = {(r["A"], r["sigma"], r["k"]): r["E_over_2M"] for r in json.load(open(fn.replace("_single", "")))["runs"]}
    rows = [dict(r, E_over_2M=pair[(r["A"], r["sigma"], r["k"])]) for r in json.load(open(fn))["runs"]]
    _acc(rows, single_E_half=True, single=True)
    cen["files"].append(fn + " (single-packet energy taken as half the pair energy)")
pm = json.load(open("e1d_probe_min.json"))
_acc(pm["dx0.05"]); _acc(pm["local"]); _acc([dict(r, A=0.275) for r in pm["phase"]])
cen["files"].append("e1d_probe_min.json")
for fn in ("e1d_coarse_oneway.jsonl", "e1d_single_oneway.jsonl", "e1d_slice_dx05.jsonl", "e1d_slice_dx05_single.jsonl",
           "e1d_dxladder.jsonl"):
    rows = jl(fn)
    if rows:
        _acc(rows)
        cen["files"].append(fn)
if os.path.exists("e1d_oneway_min.json"):
    cen["files"].append("e1d_oneway_min.json (calls only)")
out["census_all_gaussian_runs"] = cen

json.dump(out, open("e1_extra_analysis.json", "w"), indent=1, default=float)
pr = json.loads(json.dumps(out, default=float))
for k in ("coarse_oneway",):
    if k in pr:
        pr[k].pop("tests", None)
print(json.dumps(pr, indent=1)[:9000])
if "coarse_oneway" in out:
    for n, t in out["coarse_oneway"]["tests"].items():
        print("one-way test", n, t["verdict"], [r["spearman"] for r in t["rows"]])

# ---------------------------------------------------------------- figure
if maps is not None or fig_ow is not None:
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.7))
    cmap3 = ListedColormap(["#eeeeee", "#edae49", "#a4243b"])
    if maps is not None:
        xa, ya, Pb, Pf, Em, Sf = maps
        for ax, Pm, ttl in ((axs[0], Pb, "dx = 0.1, dt = 0.04 (baseline)"), (axs[1], Pf, "dx = 0.05, dt = 0.02")):
            ax.pcolormesh(np.array(ya), np.array(xa), Pm.astype(float), cmap=ListedColormap(["#eeeeee", "#a4243b"]),
                          vmin=-0.5, vmax=1.5, shading="nearest")
            cs = ax.contour(np.array(ya), np.array(xa), Em, levels=[1, 2, 4, 8, 16, 32], colors="k", linewidths=0.6)
            ax.clabel(cs, fontsize=6, fmt="%g")
            ax.set_xscale("log")
            ax.set_xlabel("sigma")
            ax.set_ylabel("A")
            ax.set_title(f"k = 1 slice, {ttl}\nred: pair; contours: E/2M_kink", fontsize=7.5)
        axs[1].text(0.97, 0.03, f"{100 * out['slice_k1_dx0.05']['point_agreement']:.0f}% of calls\nagree with dx = 0.1",
                    transform=axs[1].transAxes, fontsize=7, ha="right", va="bottom",
                    bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))
    ax = axs[2]
    if fig_ow is not None:
        f1, f0, fc = fig_ow
        xc = [np.sqrt(max(a, 0.25) * min(b, 128)) for a, b, n, m, f in f0]
        ax.semilogx(xc, [f for a, b, n, m, f in f0], "o-", c="#d1495b", ms=4, label="narrow-band phi_t (baseline)")
        ax.semilogx([np.sqrt(max(a, 0.25) * min(b, 128)) for a, b, n, m, f in f1], [f for a, b, n, m, f in f1], "s--",
                    c="#1f6fb4", ms=4, label="exact one-way phi_t")
        ax.semilogx([np.sqrt(max(a, 0.25) * min(b, 128)) for a, b, n, m, f in fc], [f for a, b, n, m, f in fc], "^:",
                    c="#edae49", ms=4, label="exact one-way, collision needed")
        ax.axvline(1, color="k", ls=":", lw=0.8)
        ax.set_xlabel("E / 2M_kink")
        ax.set_ylabel("fraction producing (coarse grid)")
        ax.legend(fontsize=6.5)
        ax.set_title("initial-velocity variant, coarse 3D grid", fontsize=7.5)
    fig.tight_layout()
    fig.savefig("fig_e1d_convergence.png", dpi=95)
    print("wrote fig_e1d_convergence.png")
