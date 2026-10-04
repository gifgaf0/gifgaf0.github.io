#!/usr/bin/env python3
"""Consolidate the numbers the paper cites into one table (paper_tables.json + markdown).
Speeds: least-squares through-origin fit of omega(q) over kf in [0.03, 0.10] (Gamma-M); weights at kf = 0.05.
Sources: lbc_results.json (g = 22 canonical, gamma6), lbc_sweep_low.json (g = 13..20), lbc_sweep_refine.json
(continuation 13.25 .. 12.55), lbc_hydro.json (f_s at g = 22), lbc_3d.json (3D hcp)."""
import json, numpy as np
D = "/home/claude/lbc_exploration/"; S = "/tmp/claude-0/-home-claude/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad/lbc/"
A = json.load(open(D+"lbc_results.json")); H = json.load(open(D+"lbc_hydro.json"))
LOW = json.load(open(S+"lbc_sweep_low.json")); REF = json.load(open(S+"lbc_sweep_refine.json"))
D3 = json.load(open(D+"lbc_3d.json"))
rows = []
def from_lbc(tag, fs=None):
    o = A[tag]; gm = [r for r in o["rows"] if r["dir"] == "GM" and 0.029 < r["kf"] < 0.101]
    qs = np.array([r["q"] for r in gm])
    fit = lambda i: float(np.sum(qs*np.array([r["modes"][i]["om"] for r in gm]))/np.sum(qs*qs))
    r5 = [r for r in gm if abs(r["kf"]-0.05) < 1e-9][0]; m = r5["modes"]
    stat = r5["static_modesum"]
    return dict(label=tag, g=o["g"], kernel=o["kern"], astar=o["astar"], f_s=fs, c2=fit(0), cT=fit(1), c1=fit(2),
                F2=m[0]["fshare"], Z21=m[0]["Z"]/m[2]["Z"], S2=(2*m[0]["Z"]/m[0]["om"])/stat, phase="stable")
rows.append(from_lbc("soft_g44")); rows.append(from_lbc("soft_g34")); rows.append(from_lbc("soft_g28"))
rows.append(from_lbc("soft_g22", fs=H["fs"]["x_0.02"]))
def from_sweep(o, phase):
    r5 = [r for r in o["rows"] if r["dir"] == "GM" and abs(r["kf"]-0.05) < 1e-9][0]
    return dict(label=f"soft_g{o['g']:g}", g=o["g"], kernel="soft", astar=o["astar"], f_s=o["f_s"], c2=o["c_Lm_fit"],
                cT=o["c_T_fit"], c1=o["c_Lp_fit"], F2=r5["F_Lm"], Z21=r5["Zq_Lm"]/r5["Zq_Lp"], S2=r5["S_Lm"], phase=phase,
                eps_minus_eps_u=o["eps_c"]-o["eps_u"], h=o["g"]*(o["mu_c"]-o["eps_c"])-o["mu_c"]**2/(2*np.pi))
for k in ["20", "18", "17", "16", "15.5", "15", "14.5", "14", "13.5", "13"]:
    rows.append(from_sweep(LOW[k], "stable"))
for k in ["13.25"]:
    rows.append(from_sweep(REF[k], "stable (continuation)"))
for k in ["12.9", "12.8", "12.7", "12.6", "12.55"]:
    if k in REF and REF[k].get("crystal"):
        rows.append(from_sweep(REF[k], "metastable"))
g6 = from_lbc("g6_g35"); rows.append(g6)
# coexistence boundary Lambda_c from h(Lambda) = 0 (linear interpolation between 13.25 and 13.0, continuation data)
h1, h0 = [r["h"] for r in rows if r["label"] in ("soft_g13.25",)][0], REF["13"]["g"]*(REF["13"]["mu_c"]-REF["13"]["eps_c"])-REF["13"]["mu_c"]**2/(2*np.pi)
Lc = 13.0 + 0.25*(-h0)/(h1-h0)
Lu = None
# energy crossing (fixed density): between 12.6 and 12.55 on the continuation
e6, e55 = REF["12.6"]["eps_c"]-REF["12.6"]["eps_u"], REF["12.55"]["eps_c"]-REF["12.55"]["eps_u"]
gx = 12.6 + (12.55-12.6)*(-e6)/(e55-e6)
ratio_at = lambda g: np.interp(g, [13.0, 13.25], [REF["13"]["c_Lm_fit"]/REF["13"]["c_T_fit"], REF["13.25"]["c_Lm_fit"]/REF["13.25"]["c_T_fit"]])
mu_c_Lc = np.interp(Lc, [13.0, 13.25], [REF["13"]["mu_c"], REF["13.25"]["mu_c"]])
Lu = mu_c_Lc/np.pi
# 3D
r3 = [r for r in D3["rows"]]
d3 = dict(label="3D hcp step, Lambda = 2 Lambda_c", c2=float(np.median([r["om"][0]/r["q"] for r in r3])),
          cT_range=[float(min(min(r["om"][4], r["om"][5])/r["q"] for r in r3)), float(max(max(r["om"][4], r["om"][5])/r["q"] for r in r3))],
          cT_mean_dyn=7.68, c1_range=[float(min(r["om"][6]/r["q"] for r in r3)), float(max(r["om"][6]/r["q"] for r in r3))],
          F2_range=[float(min(r["fshare"][0] for r in r3)), float(max(r["fshare"][0] for r in r3))],
          Z21_range=[float(min(r["Z"][0]/r["Z"][6] for r in r3)), float(max(r["Z"][0]/r["Z"][6] for r in r3))],
          S2_range=[float(min(r["sshare"][0] for r in r3)), float(max(r["sshare"][0] for r in r3))])
out = dict(rows=rows, Lambda_c=float(Lc), Lambda_u=float(Lu), energy_crossing=float(gx),
           ratio_at_Lambda_c=float(ratio_at(Lc)),
           ratio_max_metastable=float(max(r["c2"]/r["cT"] for r in rows if r["phase"] == "metastable")),
           F2_at_Lambda_c=float(np.interp(Lc, [13.0, 13.25], [[r for r in rows if r["label"]=="soft_g13"][0]["F2"], [r for r in rows if r["label"]=="soft_g13.25"][0]["F2"]])),
           three_d=d3)
json.dump(out, open("paper_tables.json", "w"), indent=1)
print("| g | phase | a* | f_s | c2 | c_T | c1 | c2/c_T | F2 | Z2/Z1 | S2 |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    fs = f"{r['f_s']:.3f}" if r["f_s"] is not None else "—"
    print(f"| {r['g']:g}{' (γ6)' if r['kernel']=='g6' else ''} | {r['phase']} | {r['astar']:.4f} | {fs} | {r['c2']:.3f} | {r['cT']:.3f} | {r['c1']:.3f} | "
          f"{r['c2']/r['cT']:.3f} | {r['F2']:.4f} | {r['Z21']:.3f} | {r['S2']:.3f} |")
print(f"\nLambda_c (common tangent, fixed density) = {Lc:.3f};  Lambda_u = mu_c(Lambda_c)/pi = {Lu:.3f};  energy crossing = {gx:.3f}")
print(f"c2/c_T at Lambda_c = {out['ratio_at_Lambda_c']:.3f}; F2 at Lambda_c = {out['F2_at_Lambda_c']:.3f}; max on metastable branch = {out['ratio_max_metastable']:.3f}")
print("3D:", json.dumps(d3))
