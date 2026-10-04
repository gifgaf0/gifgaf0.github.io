#!/usr/bin/env python3
"""cc_diagnose_misses.py -- post-comparison diagnosis of the four comparator MISSes, written after the
pre-consultation checkpoint was committed (667644af02d7bf9253f9975e68ff662ed2d6b4f6).

Usage: python3 cc_diagnose_misses.py E6_DIR [OUT.json]
E6_DIR = folder holding the extracted first-leg outputs (embed E6). Only their JSON outputs are read;
none of the first-leg scripts is imported or executed. Neither checkpoint is touched.

1. Transverse speeds (2d.13.cT, 2d.22.cT_30deg_kf005, 3d.cT_min): refit the first leg's own per-q
   transverse frequencies with omega^2 = c^2 q^2 - eps (+ d q^4 when >= 4 q points) and compare the
   offset-free c with this leg's q -> 0 transverse speed (and the static finite-strain c_T at g = 22).
2. Branch end (melting.branch_end_g): report the first leg's last refine records (crystal flag,
   contrast, eps_c vs pi g/2, a* vs scan window).
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E6 = sys.argv[1]
def load(path):
    with open(path) as f:
        return json.load(f)

def offset_fit(qs, om):
    qs = np.asarray(qs, float); w2 = np.asarray(om, float)**2
    cols = [qs**2, -np.ones_like(qs)] + ([qs**4] if len(qs) >= 4 else [])
    x = np.linalg.lstsq(np.stack(cols, 1), w2, rcond=None)[0]
    return float(np.sqrt(x[0])), float(x[1])

cc = load(os.path.join(HERE, "qa_results.json"))["points"]
hy = load(os.path.join(HERE, "qa_prime_results.json"))
def cc_cT0(key):
    p = cc[key]["per_q_a1"]
    qs = np.array([r["qabs"] for r in p]); v = np.array([r["T"]["v_over_q"] for r in p])
    return float(np.polyfit(qs**2, v, 1)[1])

out = {"transverse_2d": {}, "transverse_3d": {}, "branch_end": {}}

res = load(os.path.join(E6, "lbc_results.json"))
for tag, key in (("soft_g22", "22"), ("soft_g28", "28"), ("soft_g44", "44"), ("g6_g35", "35g6")):
    o = res[tag]
    for d in ("GM", "GK"):
        rows = [w for w in o["rows"] if w["dir"] == d]
        if len(rows) < 3:
            continue
        qs = [w["q"] for w in rows]; om = [w["modes"][1]["om"] for w in rows]
        c, eps = offset_fit(qs, om)
        out["transverse_2d"][f"{key}_{d}"] = dict(
            chat_v_over_q=[float(w / q) for w, q in zip(om, qs)], chat_q=qs, offset_free_c=c, eps=eps,
            chat_ward_w2min=o["ward_w2min"], chat_gp_residual=o["gp_residual"], cc_cT_q0=cc_cT0(key),
            rel_offset_free_vs_cc=(c - cc_cT0(key)) / cc_cT0(key))
low = load(os.path.join(E6, "lbc_sweep_low.json")); ref = load(os.path.join(E6, "lbc_sweep_refine.json"))
for src, key in ((ref, "13"), (ref, "13.25"), (low, "13.5"), (low, "14"), (low, "16")):
    o = src[key]
    rows = [w for w in o["rows"] if w["dir"] == "GM"]
    qs = [w["q"] for w in rows]; om = [w["c_T"] * w["q"] for w in rows]
    c, eps = offset_fit(qs, om)
    out["transverse_2d"][f"{key}_GM"] = dict(
        chat_v_over_q=[w["c_T"] for w in rows], chat_q=qs, chat_cT_lsq=o["c_T_fit"], offset_free_c=c, eps=eps,
        chat_ward_w2min=o["ward_w2min"], chat_gp_residual=o["gp_residual"], cc_cT_q0=cc_cT0(key),
        rel_offset_free_vs_cc=(c - cc_cT0(key)) / cc_cT0(key))
out["transverse_2d"]["static_route_cT_g22"] = {"cc": hy["c_T"]}

d3 = load(os.path.join(E6, "lbc_3d.json"))
out["transverse_3d"]["chat_gcut"] = d3["gcut"]; out["transverse_3d"]["chat_NG"] = d3["NG"]
out["transverse_3d"]["chat_relax_residual"] = d3["res"]
out["transverse_3d"]["chat_near_gamma_omega"] = d3["near_gamma"]["om"][:6]
for r in d3["rows"]:
    out["transverse_3d"][f"{r['dir']}_q{r['q']:.2f}_om4_om5_over_q"] = [r["om"][4] / r["q"], r["om"][5] / r["q"]]
qb = load(os.path.join(HERE, "qb_results.json"))
out["transverse_3d"]["cc_transverse_speeds_q015"] = qb["extras"]["transverse_speeds_q015"]
out["transverse_3d"]["cc_cut_convergence_cT_min"] = {k: v["cT_min"] for k, v in
                                                     qb["convergence"]["consistent_cuts"].items()}

for key in ("12.55", "12.5", "12.45"):
    o = ref[key]
    out["branch_end"][key] = {k: o.get(k) for k in ("g", "astar", "crystal", "contrast", "eps_c", "eps_u",
                                                    "gp_residual", "ward_w2min")}
    out["branch_end"][key]["eps_c_minus_pi_g_half"] = o["eps_c"] - np.pi * o["g"] / 2
    out["branch_end"][key]["astar_at_scan_upper_edge"] = abs(o["astar"] - max(o["a_scan"])) < 1e-12
qc = load(os.path.join(HERE, "qc_results.json"))
out["branch_end"]["cc"] = {k: qc[k] for k in ("branch_end_g", "branch_end_bisection_bracket", "energy_crossing",
                                              "bdg_instability_first_g", "bdg_instability_q_to_0_estimate")}

text = json.dumps(out, indent=1, default=float)
print(text)
if len(sys.argv) > 2:
    with open(sys.argv[2], "w") as f:
        f.write(text + "\n")
