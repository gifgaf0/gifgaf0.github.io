"""Collect E1a-E1e headline numbers into results.json (run after the analyze_* scripts)."""
import json
import numpy as np
from phi4core import M_KINK

a = json.load(open("e1a_results.json"))
b = json.load(open("e1b_analysis.json"))
c = json.load(open("e1c_analysis.json"))
d = json.load(open("e1d_analysis.json"))
TWO_M = 2 * M_KINK
SQ2 = np.sqrt(2)

H = []


def add(q, val, unit, target, tol, verdict, note, source=""):
    H.append({"quantity": q, "value": val, "units_convention": unit, "target": target, "tolerance": tol,
              "verdict": verdict, "source": source, "note": note})


conv = "V=(1/4)(phi^2-1)^2, m=sqrt2, M_kink=2sqrt2/3 (rescaled units, phi0=1)"
# E1a
add("E1a M_kink", a["verdict"]["M_kink"]["value"], conv, M_KINK, "relative 1e-4",
    a["verdict"]["M_kink"]["verdict"], f"relaxed lattice kink, dx=0.025; rel. err {a['verdict']['M_kink']['rel_err']:.1e} "
    f"(dx=0.05: {a['verdict']['baseline_dx=0.05']['M_rel_err']:.1e})", "exact")
add("E1a shape-mode frequency omega_s", a["verdict"]["omega_s"]["value"], conv, float(np.sqrt(1.5)), "relative 1e-4",
    a["verdict"]["omega_s"]["verdict"], f"eigenvalue of -d2+3phi_k^2-1, dx=0.025; rel. err {a['verdict']['omega_s']['rel_err']:.1e}; "
    f"dynamical measurement agrees to {max(abs(v['rel_err']) for v in a['shape_mode_dynamic'].values()):.1e}", "exact")
# E1b
hb = b["headline"]
add("E1b critical velocity v_c", hb["v_c"], "speed of each kink in the CM frame, units of c", 0.2598, "+-0.001",
    hb["v_c_verdict"], f"dx=0.05, x0=12; range over 5 numerical configurations {hb['v_c_spread_over_configs']}",
    "[summary] CSW 1983 / Anninos et al. 1991")
add("E1b first two-bounce window", hb["first_window"], "v range", [0.1926, 0.2034], "+-0.003 on each edge",
    hb["first_window_verdict"], f"edges spread over configs lo {hb['first_window_spread_lo']}, hi {hb['first_window_spread_hi']}",
    "[summary, one source]")
add("E1b number of two-bounce windows, narrowing", {"n_windows_base": hb["n_two_bounce_windows_found_base"],
                                                     "first_five_widths": hb["first_five_widths"]},
    "count / widths", ">= 3 windows narrowing toward v_c", "qualitative",
    "CALIBRATED" if (hb["n_two_bounce_windows_found_base"] >= 3 and hb["narrowing_toward_vc"]) else "MISS",
    f"first five windows {hb['first_five_windows']}; max edge difference to the literature list "
    f"{hb['windows_vs_literature_max_edge_diff']:.4f}", "[summary]")
add("E1b resonance check (extra, not preregistered)", b["resonance_check"]["slope_T12_per_window"], "time units per window",
    b["resonance_check"]["2pi_over_omega_s"], "none", "NO_TARGET",
    "time between 1st and 2nd bounce grows by about one shape-mode period per window (CSW mechanism)")
# E1c
ex = c["example_0.99_0.43"]
add("E1c (omega,v)=(0.99,0.43) produces a pair", ex["produced_dsv"], "DSV criterion: pair present at t=T (one light-crossing time)",
    True, "qualitative", "CALIBRATED" if ex["produced_dsv"] else "MISS",
    f"pair continuously present from t={ex['pair_continuously_present_since']} (T=1200); survives to 1.5T: {ex['survives_to_1.5T']}; "
    f"fails our stricter persistence criterion (pair over [0.8T,T]): {not ex['produced_persist']}", "[read] arXiv:0803.0670")
tr = c["trend"]["dsv"]
add("E1c producing region trends to lower v as omega rises", tr["spearman_omega_vs_median_v"], "Spearman rho, p (omega vs median producing v)",
    "rho < 0", "qualitative", "CALIBRATED" if (tr["spearman_omega_vs_median_v"] and tr["spearman_omega_vs_median_v"][0] < 0
                                                and tr["spearman_omega_vs_median_v"][1] < 0.05) else "MISS",
    f"vmax: {tr['spearman_omega_vs_vmax']}, vmin: {tr['spearman_omega_vs_vmin']}", "[read]")
hv = c["high_v"]
add("E1c trains pass through at high v", hv, "counts of producing runs at high v", "no production at the highest v",
    "qualitative", "CALIBRATED" if hv["v>=0.9"]["n_produced_dsv"] == 0 else "MISS", "", "[read]")
add("E1c holes, e.g. near (0.91,0.82)", {"n_holes": len(c["holes_dsv"]), "probe": c["near_0.91_0.82"]},
    "non-producing points with producing v-neighbours", "holes exist", "qualitative",
    "CALIBRATED" if len(c["holes_dsv"]) > 0 else "MISS", "see e1c_analysis.json for the list", "[read]")
og = c.get("omega_gt_0.99", {})
n_og = sum(len(v["produced_dsv_at_v"]) for v in og.values())
add("E1c no production for omega > 0.99", og, "omega in {0.992, 0.995}, v 0.20-0.90", "no production", "qualitative",
    "CALIBRATED" if n_og == 0 else "MISS", "", "[read]")
# E1d
add("E1d no production below E = 2 M_kink", d["coarse_any_below_threshold"], "count of producing runs with E < 2M", 0,
    "exact (energy conservation)", "CALIBRATED" if d["coarse_any_below_threshold"] == 0 else "MISS", "sanity check")
add("E1d minimum producing energy (coarse grid)", d["coarse_min_producing"]["E_over_2M"], "E / 2M_kink", "none (prediction: > 1)",
    "none", "NO_TARGET", f"at A,sigma,k = {d['coarse_min_producing']['A']},{d['coarse_min_producing']['sigma']},{d['coarse_min_producing']['k']}")
add("E1d minimum producing energy (all Gaussian runs)", d["quanta"]["min_E_producing"]["E_over_2M"], "E / 2M_kink",
    "none", "none", "NO_TARGET", f"{d['quanta']['min_E_producing']}")
add("E1d producing regions (coarse 3D grid)", d["coarse_regions"], "connected components", "prediction: ragged",
    "qualitative", "NO_TARGET", "")
for k, s in d.get("slices", {}).items():
    add(f"E1d slice {k}", {"regions_4conn": s["regions_4conn"], "regions_8conn": s["regions_8conn"],
                           "singletons_4conn": s["n_singleton_regions_4conn"], "enclosed_holes": s["enclosed_nonproducing_holes"],
                           "A_lines_non_monotonic": s["A_lines"]["non_monotonic(>1 flip)"],
                           "A_lines_with_production": s["A_lines"]["with_production"]},
        "connected components / flips", "prediction: ragged", "qualitative", "NO_TARGET", f"fixed {s['fixed']}")
# E1e
g = d["quanta"]
dsvmin = c["min_energy_producing"]["survives_to_1.5T"]
for name, E, Nl in (("DSV trains (pair survives to 1.5T)", dsvmin["E"], dsvmin["N_lin"]),
                    ("Gaussian packets", g["min_E_producing"]["E"], g["min_E_producing"]["N_lin"])):
    add(f"E1e N_min = E_min/m, {name}", {"N_over_phi0sq": E / SQ2, "N_times_lambda_over_m2": E / (2 * SQ2),
                                          "N_lin_over_phi0sq_same_run": Nl, "N_lin_times_lambda_over_m2": Nl / 2},
        "phi0^2 = m^2/(2 lambda) for L=1/2(dPhi)^2-(lambda/4)(Phi^2-v^2)^2; hbar=1", "N ~ 1/lambda (scaling)",
        "none", "QUANTIFIED", "threshold 2M_kink alone corresponds to N*lambda/m^2 = 2/3")
gn = g["min_Nlin_producing"]
add("E1e smallest free-field quanta number among producing Gaussian runs", {"N_lin_over_phi0sq": gn["N_lin"],
                                                                              "N_lin_times_lambda_over_m2": gn["N_lin"] / 2},
    "N_lin = sum_q (|pi_q|^2+w_q^2|d_q|^2)/(2w_q)", "none", "none", "QUANTIFIED", f"{gn}")
json.dump({"experiment": "E1 phi^4 in 1+1D (PLAN.md section 4, E1a-E1e)", "convention": conv,
           "headline": H,
           "details_files": ["e1a_results.json", "e1b_analysis.json", "e1c_analysis.json", "e1d_analysis.json"]},
          open("results.json", "w"), indent=1, default=float)
for h in H:
    print(f"{h['verdict']:11s} {h['quantity']}: {h['value']}")
