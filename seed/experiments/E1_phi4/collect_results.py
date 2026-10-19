"""Collect E1a-E1e headline numbers into results.json (run after analyze_e1b/c/d.py and e1e_quanta.py).
Every entry: quantity, value, units/convention, target, tolerance, source, verdict, note."""
import json
import numpy as np
from phi4core import M_KINK

a = json.load(open("e1a_results.json"))
b = json.load(open("e1b_analysis.json"))
c = json.load(open("e1c_analysis.json"))
d = json.load(open("e1d_analysis.json"))
e = json.load(open("e1e_results.json"))
TWO_M = 2 * M_KINK
H = []


def add(q, val, unit, target, tol, verdict, note, source=""):
    H.append({"quantity": q, "value": val, "units_convention": unit, "target": target, "tolerance": tol,
              "verdict": verdict, "source": source, "note": note})


conv = "V=(1/4)(phi^2-1)^2, m=sqrt2, M_kink=2sqrt2/3, kink tanh(x/sqrt2) (rescaled units, phi0=1, hbar=1)"
# ---------------------------------------------------------------- E1a
add("E1a M_kink", a["verdict"]["M_kink"]["value"], conv, M_KINK, "relative 1e-4",
    a["verdict"]["M_kink"]["verdict"],
    f"Newton-relaxed lattice kink, dx=0.025; rel. err {a['verdict']['M_kink']['rel_err']:.1e} "
    f"(dx=0.05: {a['verdict']['baseline_dx=0.05']['M_rel_err']:.1e}, dx=0.1: {a['kink_mass']['dx=0.1']['rel_err_relaxed']:.1e})",
    "exact")
add("E1a shape-mode frequency omega_s", a["verdict"]["omega_s"]["value"], conv, float(np.sqrt(1.5)), "relative 1e-4",
    a["verdict"]["omega_s"]["verdict"],
    f"lowest nonzero eigenvalue of -d2+3phi_k^2-1 on the lattice, dx=0.025; rel. err {a['verdict']['omega_s']['rel_err']:.1e}; "
    f"time-domain measurement agrees to {max(abs(v['rel_err']) for v in a['shape_mode_dynamic'].values()):.1e}", "exact")
# ---------------------------------------------------------------- E1b
hb = b["headline"]
rich = b.get("dx_series_richardson", {})
add("E1b critical velocity v_c (dx->0 extrapolation)", hb.get("v_c_extrapolated", hb["v_c"]),
    "speed of each kink in the CM frame, units of c", 0.2598, "+-0.001",
    hb.get("v_c_extrapolated_verdict", hb["v_c_verdict"]),
    f"dx=0.1/0.05/0.025 (dt=0.4dx): {[round(rich['v_c'][k], 6) for k in ('dx0.1', 'dx0.05', 'dx0.025')] if rich else ''}; "
    f"Richardson p=2; x0=20 and t_post=1500 change it by <2e-5; range over all configurations {hb['v_c_spread_over_configs']}",
    "[summary] Campbell-Schonfeld-Wingate 1983; Anninos-Oliveira-Matzner 1991")
add("E1b critical velocity v_c (baseline dx=0.05, x0=12)", hb["v_c"], "same", 0.2598, "+-0.001", hb["v_c_verdict"],
    f"bracket from bisection; label = bounce count before escape", "[summary]")
add("E1b first two-bounce window (dx->0 extrapolation)", hb.get("first_window_extrapolated", hb["first_window"]), "v range",
    [0.1926, 0.2034], "+-0.003 on each edge",
    "CALIBRATED" if all(abs(x - y) <= 0.003 for x, y in zip(hb.get("first_window_extrapolated", hb["first_window"]),
                                                             (0.1926, 0.2034))) else "MISS",
    f"baseline dx=0.05: {[round(x, 5) for x in hb['first_window']]}; edge spread over configs lo {hb['first_window_spread_lo']}, "
    f"hi {hb['first_window_spread_hi']}", "[summary, one source]")
add("E1b two-bounce windows: >= 3, narrowing toward v_c", {"n_windows_base": hb["n_two_bounce_windows_found_base"],
                                                           "first_five": hb["first_five_windows"],
                                                           "first_five_widths": hb["first_five_widths"]},
    "count / v ranges / widths", ">= 3 windows narrowing toward v_c", "qualitative",
    "CALIBRATED" if (hb["n_two_bounce_windows_found_base"] >= 3 and hb["narrowing_toward_vc"]) else "MISS",
    f"windows 2-5 vs a literature list of unverified provenance (not preregistered): max edge difference "
    f"{hb['windows_vs_literature_max_edge_diff']:.4f}", "[summary]")
add("E1b resonance check (not preregistered)", b["resonance_check"]["slope_T12_per_window"], "time units per window",
    b["resonance_check"]["2pi_over_omega_s"], "none", "NO_TARGET",
    "time between 1st and 2nd bounce grows by about one shape-mode period 2pi/omega_s per window (CSW mechanism)")
# ---------------------------------------------------------------- E1c
ex = c["example_0.99_0.43"]
add("E1c (omega,v)=(0.99,0.43) produces a pair", ex["produced_dsv"], "DSV criterion: pair present at t=T (one light-crossing time)",
    True, "qualitative", "CALIBRATED" if ex["produced_dsv"] else "MISS",
    f"pair first meets the pair test at t={ex['pair_continuously_present_since']} (T=1200) after a long-lived central "
    f"oscillation; still present and separating at 1.5T: {ex['survives_to_1.5T']}; E/2M={ex['E0_over_2M']:.2f}",
    "[read] arXiv:0803.0670")
tr = c["trend"]["dsv"]
add("E1c producing region trends to lower v as omega rises", tr["spearman_omega_vs_median_v"],
    "Spearman rho, p (omega vs median producing v)", "rho < 0", "qualitative",
    "CALIBRATED" if (tr["spearman_omega_vs_median_v"] and tr["spearman_omega_vs_median_v"][0] < 0
                     and tr["spearman_omega_vs_median_v"][1] < 0.05) else "MISS",
    f"vmax: {tr['spearman_omega_vs_vmax']}, vmin: {tr['spearman_omega_vs_vmin']}", "[read]")
hv = c["high_v"]
add("E1c trains pass through at high v", hv, "producing runs at v >= 0.85 / 0.9", "no production at the highest v",
    "qualitative", "CALIBRATED" if hv["v>=0.9"]["n_produced_dsv"] == 0 else "MISS", "", "[read]")
add("E1c holes, e.g. near (0.91,0.82)", {"n_holes": len(c["holes_dsv"]), "probe": c["near_0.91_0.82"]},
    "non-producing points whose two v-neighbours (step 0.01) produce", "holes exist", "qualitative",
    "CALIBRATED" if len(c["holes_dsv"]) > 0 else "MISS", "list in e1c_analysis.json", "[read]")
og = c.get("omega_gt_0.99", {})
n_og = sum(len(v["produced_dsv_at_v"]) for v in og.values())
add("E1c no production for omega > 0.99", og, "omega in {0.992, 0.995}, v 0.20-0.90 step 0.02", "none found",
    "qualitative", "CALIBRATED" if n_og == 0 else "MISS", "DSV: 'we have not found ... for omega > 0.99'", "[read]")
if "dx_check" in c:
    add("E1c dx check (dx 0.05 vs 0.1)", c["dx_check"], "agreement of the production call", "none", "none", "NO_TARGET", "")
# ---------------------------------------------------------------- E1d
add("E1d no production below E = 2 M_kink", d["coarse_any_below_threshold"], "producing runs with E < 2M_kink (coarse grid)",
    0, "exact (energy conservation)", "CALIBRATED" if d["coarse_any_below_threshold"] == 0 else "MISS", "sanity check")
rep = {(r["A"], r["sigma"], r["k"]): r["reproduced"] for r in e["gaussian_packets"].get("dx0.05_reproduction_of_smallest_producers", [])}
rmin = e["gaussian_packets"]["min_E_any"]
add("E1d lowest producing energy, all Gaussian runs (dx=0.1)", rmin["E_over_2M"], "E / 2M_kink",
    "prediction: > 1", "none", "NO_TARGET",
    f"A={rmin['A']}, sigma={rmin['sigma']}, k={rmin['k']}; single packet alone produces: {rmin['single_packet_alone_produces']}; "
    f"reproduced at dx=0.05: {rep.get((rmin['A'], rmin['sigma'], rmin['k']))}")
rr = e["gaussian_packets"].get("robust", {}).get("min_E_reproduced")
if rr:
    add("E1d lowest producing energy reproduced at dx=0.05", rr["E_over_2M"], "E / 2M_kink", "prediction: > 1", "none",
        "NO_TARGET", f"A={rr['A']}, sigma={rr['sigma']}, k={rr['k']}; collision needed")
add("E1d fraction producing vs E/2M (coarse grid)", d["coarse_frac_vs_E"], "[E/2M lo, hi, n, n_prod, frac]", "none", "none",
    "NO_TARGET", f"{d['coarse_grid']['n_produced']}/{d['coarse_grid']['n_runs']} coarse runs produce")
add("E1d producing regions (coarse 3D grid)", d["coarse_regions"], "connected components (6- and 26-connectivity)",
    "prediction: ragged", "qualitative", "NO_TARGET", "")
for k, s in d.get("slices", {}).items():
    add(f"E1d slice {k}", {"regions_4conn": s["regions_4conn"], "regions_8conn": s["regions_8conn"],
                           "singletons_4conn": s["n_singleton_regions_4conn"], "enclosed_holes": s["enclosed_nonproducing_holes"],
                           "A_lines_non_monotonic": s["A_lines"]["non_monotonic(>1 flip)"],
                           "A_lines_with_production": s["A_lines"]["with_production"],
                           "min_producing": s["min_producing"]},
        "connected components / flips along A", "prediction: ragged", "qualitative", "NO_TARGET", f"fixed {s['fixed']}")
pt = d.get("prediction_tests", {})
for name in ("ragged", "ragged_collision_needed", "speed", "width", "speed_collision_needed", "width_collision_needed"):
    if name in pt:
        add(f"E1d prediction test: {name}", {kk: vv for kk, vv in pt[name].items() if kk != "verdict"},
            "see analyze_e1d.py for the operational test", "see PLAN.md E1d", "operational", pt[name]["verdict"], "")
for key in ("single_packet_controls", "dx_check", "phase_diagnostic"):
    if key in d:
        add(f"E1d {key}", d[key], "", "none", "none", "NO_TARGET", "")
# ---------------------------------------------------------------- E1e
add("E1e threshold 2M_kink in quanta", e["threshold_2M_kink"]["N_E_times_lambda_over_m2"], "N*lambda/m^2 (N = E/m)",
    "none", "none", "QUANTIFIED", "energy conservation alone: N >= (2/3) m^2/lambda")
dd = e["dsv_trains"].get("produced_dsv") or {}
for tag in ("min_E_reproduced_dx0.05", "min_N_lin_reproduced_dx0.05"):
    r = dd.get(tag)
    if r:
        add(f"E1e DSV trains, {tag}", {"N_E_times_lambda_over_m2": r["N_E_times_lambda_over_m2"],
                                       "N_lin_times_lambda_over_m2": r["N_lin_times_lambda_over_m2"],
                                       "E_over_2M": r["E_over_2M"], "omega": r["omega"], "v": r["v"]},
            "N*lambda/m^2; phi0^2 = m^2/(2 lambda)", "N ~ 1/lambda (scaling)", "none", "QUANTIFIED",
            f"lowest producing train at dx=0.1 that is reproduced at dx=0.05; walk: {json.dumps(dd.get(tag.replace('reproduced_dx0.05', 'dx0.05_walk')))}")
g = e["gaussian_packets"]
for name in ("min_E_reproduced", "min_N_lin_reproduced"):
    r = g.get("robust", {}).get(name)
    if r:
        add(f"E1e Gaussian packets, {name} at dx=0.05", {"N_E_times_lambda_over_m2": r["N_E_times_lambda_over_m2"],
                                                         "N_lin_times_lambda_over_m2": r["N_lin_times_lambda_over_m2"],
                                                         "E_over_2M": r["E_over_2M"], "A": r["A"], "sigma": r["sigma"], "k": r["k"]},
            "N*lambda/m^2", "N ~ 1/lambda (scaling)", "none", "QUANTIFIED", "collision needed (the single packet alone makes no pair)")
for name in ("min_E_any", "min_N_lin_any"):
    r = g.get(name)
    if r:
        add(f"E1e Gaussian packets, raw {name} (NOT reproduced at dx=0.05)", {"N_E_times_lambda_over_m2": r["N_E_times_lambda_over_m2"],
                                                                              "N_lin_times_lambda_over_m2": r["N_lin_times_lambda_over_m2"],
                                                                              "E_over_2M": r["E_over_2M"], "A": r["A"],
                                                                              "sigma": r["sigma"], "k": r["k"]},
            "N*lambda/m^2", "N ~ 1/lambda (scaling)", "none", "QUANTIFIED",
            "isolated producing point; see e1d_probe_min.json (dx=0.05 rerun, local grid, phase shifts)")
add("E1e smallest classical N_lin*lambda/m^2 (producers reproduced at dx=0.05)", e["smallest_classical_N_lin_times_lambda_over_m2_found"],
    "N*lambda/m^2", "none", "none", "QUANTIFIED", json.dumps(e["implication"]))
json.dump({"experiment": "E1 phi^4 in 1+1D (PLAN.md section 4, E1a-E1e)", "convention": conv,
           "headline": H,
           "details_files": ["e1a_results.json", "e1b_analysis.json", "e1c_analysis.json", "e1d_analysis.json",
                             "e1e_results.json"]},
          open("results.json", "w"), indent=1, default=float)
for h in H:
    v = h["value"]
    vs = json.dumps(v, default=float)
    print(f"{h['verdict']:11s} {h['quantity']}: {vs[:150]}")
