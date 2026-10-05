#!/usr/bin/env python3
"""Assemble the CORRECTED first leg (v2, post-comparison, labelled as such) in the comparison schema, plus the paper
tables v2. Inputs: jobA_2d.json (2D, converged states), jobB_3d.json (3D, K = 30, q = 0.15), jobC_melt.json (melting end),
and the first leg's v1 checkpoint for the quantities the defect does not touch (static hydro route, f_s)."""
import json, math
import numpy as np
A = json.load(open("jobA_2d.json")); B = json.load(open("jobB_3d.json")); C = json.load(open("jobC_melt.json"))
V1 = json.load(open("/home/claude/bank/dispatch/lbc_chat_checkpoint.json"))
phi = (1+5**0.5)/2
ck = {"schema": "lbc_2leg_schema_v1.0", "leg": "chat-v2-corrected-post-comparison", "2d": {}}
keymap = {"44": "soft_g44", "28": "soft_g28", "22": "soft_g22", "16": "soft_g16", "14": "soft_g14",
          "13.5": "soft_g13.5", "13": "soft_g13", "13.25": "ref_g13.25", "35g6": "g6_g35"}
for key, lab in keymap.items():
    r = A[lab]
    ck["2d"][key] = {k: r[k] for k in ("astar", "c2", "cT", "c1", "F2", "Z21", "S2")}
    if "f_s" in V1["2d"][key]:
        ck["2d"][key]["f_s"] = V1["2d"][key]["f_s"]          # not affected by the BdG defect (second leg: <= 1.3e-4)
g22 = A["soft_g22"]
ck["2d"]["22"]["cT_30deg_kf005"] = g22["cT_GK_kf005"]
ck["2d"]["22"]["fsum_resid_max"] = g22["fsum_resid_max"]; ck["2d"]["22"]["static_resid_max"] = g22["static_resid_max"]
ck["hydro_g22"] = V1["hydro_g22"]                             # static finite-strain route: no BdG, unaffected
# 3D: K = 30, q = 0.15, all three directions (the second leg's definition)
K = B["K30"]; rows = [r for r in K["rows"] if abs(r["q"]-0.15) < 1e-9]
def tr(r):
    om = r["om"]; assert om[4] > 1.05*max(om[1:4]), "transverse not above the gapped optical modes"
    return [om[4]/r["q"], om[5]/r["q"]]
cts = [x for r in rows for x in tr(r)]
gm = [r for r in rows if r["dir"] == "basal_GM"][0]
ck["3d"] = {"c2": float(np.median([r["om"][0]/r["q"] for r in rows])), "cT_min": min(cts), "cT_max": max(cts),
            "c1_basal_q015": gm["om"][6]/gm["q"], "F2_basal_q015": gm["fshare"][0], "Z21_basal_q015": gm["Z"][0]/gm["Z"][6],
            "S2_basal_q015": gm["sshare"][0], "c_kappa": math.sqrt(gm["vol"]/gm["chi_direct"])}
# melting
def h(r): return r["g"]*(r["mu_c"]-r["eps_c"]) - r["mu_c"]**2/(2*np.pi)
r13, r1325 = A["ref_g13"], A["ref_g13.25"]
h0, h1 = h(r13), h(r1325)
Lc = 13.0 + 0.25*(-h0)/(h1-h0)
w = (Lc-13.0)/0.25
lin = lambda x0, x1: (1-w)*x0 + w*x1
mu_Lc = lin(r13["mu_c"], r1325["mu_c"])
e6, e55 = A["ref_g12.6"]["eps_c"]-A["ref_g12.6"]["eps_u"], A["ref_g12.55"]["eps_c"]-A["ref_g12.55"]["eps_u"]
gx = 12.6 + (12.55-12.6)*(-e6)/(e55-e6)
meta = [A[f"ref_g{k}"] for k in ("12.9", "12.8", "12.7", "12.6", "12.55")]
metaC = [c for c in C if "ratio" in c]
all_ratios = [r["c2"]/r["cT"] for r in A.values()] + [c["ratio"] for c in metaC]
crystal_found = [c["g"] for c in C if c["contrast"] > 0.05]
ck["melting"] = {"Lambda_c": Lc, "Lambda_u": mu_Lc/np.pi, "energy_crossing": gx,
                 "ratio_at_Lambda_c": lin(r13["c2"]/r13["cT"], r1325["c2"]/r1325["cT"]),
                 "F2_at_Lambda_c": lin(r13["F2"], r1325["F2"]),
                 "ratio_max_metastable": max([r["c2"]/r["cT"] for r in meta] + [c["ratio"] for c in metaC]),
                 "branch_end_g": min(crystal_found),    # a BOUND: lowest g at which the chat side found the crystal
                 "any_c2_ge_cT": bool(max(all_ratios) >= 1.0)}
# loss: the V4.67 re-evaluation with the 3D K = 30, q = 0.15 inputs (formulas of step3_loss_length.py, unchanged)
lP, gam, Lprop = 1.616255e-35, 3.1974e11, 3.0857e20
pts = {(2.0,20):(15.17,4.68,1.82,8.06), (3.0,5):(9.35,0.61,1.6401,2.74), (3.0,10):(13.73,4.43,1.20,7.49), (3.0,20):(18.26,7.41,0.45,11.23)}
ell = lambda M, tau, P: gam*M*tau*lP/P
cand = [(ell(phi**2, T, P), k, ch) for k,(A_,J,O,T) in pts.items() for ch,P in (("A",A_),("J",J),("O",O))]
o_best = math.log10(max(cand)[0]/Lprop); o_worst = math.log10(min(cand)[0]/Lprop)
A_,J,O,T = pts[(3.0,20)]; xi_req_old = Lprop*O/(gam*phi**2*T)
F2s = [r["fshare"][0] for r in rows]; F2lo, F2hi = min(F2s), max(F2s)
c2v = ck["3d"]["c2"]; cTmean = 7.68; M_new = cTmean/c2v; ckap = ck["3d"]["c_kappa"]; cs_decl = cTmean/phi**2
S = lambda M: 1/math.sqrt(1-1/M**2)
read = {"main": lambda F: (S(phi**2)/S(M_new))/F, "point": lambda F: 1/F, "closure": lambda F: (M_new/phi**2)/F,
        "dressed": lambda F: (S(phi**2)/S(M_new))/F/((ckap/cs_decl)**4)}
heads = {k: [o_best+math.log10(f(F2hi)), o_best+math.log10(f(F2lo))] for k, f in read.items()}
ck["loss"] = {"v467_best_orders": o_best, "v467_worst_orders": o_worst,
              "main_orders_recovered": [math.log10(read["main"](F2hi)), math.log10(read["main"](F2lo))],
              "main_headline_orders": heads["main"],
              "band_orders": [min(min(v) for v in heads.values()), max(max(v) for v in heads.values())],
              "xi_req_main_m": [xi_req_old/read["main"](F2lo), xi_req_old/read["main"](F2hi)],
              "eq3_coefficient": 16*math.pi*10*(7.68/ckap)**4/F2lo,
              "eq4_bound": 1/(2*3.1974e11**2), "drag_prefactor_3d_coeff": 1/(4*math.pi)}
json.dump(ck, open("lbc_chat_checkpoint_v2.json", "w"), indent=1, default=float)
open("lbc_chat_checkpoint_v2.json", "a").write("\n")
# paper tables v2
order = ["soft_g44", "soft_g34", "soft_g28", "soft_g22", "soft_g20", "soft_g18", "soft_g16", "soft_g15", "soft_g14",
         "soft_g13.5", "ref_g13", "ref_g12.7", "g6_g35"]
tab = []
for lab in order:
    r = A[lab]
    tab.append(dict(label=lab, g=r["g"], kernel=r["kernel"], astar=r["astar"], f_s=r["f_s"], c2=r["c2"], cT=r["cT"], c1=r["c1"],
                    ratio=r["c2"]/r["cT"], F2=r["F2"], Z21=r["Z21"], S2=r["S2"], phase=r["phase"]))
tabC = [dict(g=c["g"], ratio=c.get("ratio"), c2=c.get("c2"), cT=c.get("cT"), w2min=c["w2min"], contrast=c["contrast"]) for c in C]
d3all = {k: {"rows": [dict(dir=r["dir"], q=r["q"], cT=tr(r), c2=r["om"][0]/r["q"], c1=r["om"][6]/r["q"], F2=r["fshare"][0],
                         Z21=r["Z"][0]/r["Z"][6], S2=r["sshare"][0]) for r in B[k]["rows"]], "near_gamma_om": B[k]["near_gamma_om"],
              "NG": B[k]["NG"], "e": B[k]["e_new"], "projres": B[k]["projres_new"]} for k in B}
json.dump(dict(rows=tab, melting_end=tabC, three_d=d3all, melting=ck["melting"]), open("paper_tables_v2.json", "w"), indent=1, default=float)
print(json.dumps(ck["melting"], indent=1)); print(json.dumps(ck["3d"], indent=1))
for r in tab:
    print(f"| {r['g']:g}{' (γ6)' if r['kernel']=='g6' else ''} | {r['astar']:.3f} | {('%.3f'%r['f_s']) if r['f_s'] else '—'} | {r['c2']:.3f} | {r['cT']:.3f} | {r['c1']:.2f} | {r['ratio']:.3f} | {r['F2']:.3f} | {r['Z21']:.3f} | {r['S2']:.2f} |")
