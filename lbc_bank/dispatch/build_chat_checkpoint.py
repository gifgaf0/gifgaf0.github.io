#!/usr/bin/env python3
"""Build the chat-leg checkpoint of the paper-cited numbers in the comparison schema (lbc_2leg_schema v1.0)."""
import json
T = json.load(open("/home/claude/bank/paper_tables.json"))
H = json.load(open("/home/claude/lbc_exploration/lbc_hydro.json"))
S3 = json.load(open("/home/claude/bank/step3_loss_length.json"))
D3 = json.load(open("/home/claude/lbc_exploration/lbc_3d.json"))
A = json.load(open("/home/claude/lbc_exploration/lbc_results.json"))
LOW = json.load(open("/tmp/claude-0/-home-claude/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad/lbc/lbc_sweep_low.json"))
REF = json.load(open("/tmp/claude-0/-home-claude/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad/lbc/lbc_sweep_refine.json"))
ck = {"schema": "lbc_2leg_schema_v1.0", "leg": "chat", "2d": {}}
want = {"44": "soft_g44", "28": "soft_g28", "22": "soft_g22", "16": "soft_g16", "14": "soft_g14",
        "13.5": "soft_g13.5", "13": "soft_g13", "13.25": "soft_g13.25", "35g6": None}
for key, lab in want.items():
    r = [x for x in T["rows"] if (x["label"] == lab) or (key == "35g6" and x["kernel"] == "g6")][0]
    ck["2d"][key] = {k: r[k] for k in ("astar", "c2", "cT", "c1", "F2", "Z21", "S2")}
    if r["f_s"] is not None: ck["2d"][key]["f_s"] = r["f_s"]
# Gamma-K transverse speed at kf 0.05 for g = 22 (isotropy check)
gk = [r for r in A["soft_g22"]["rows"] if r["dir"] == "GK" and abs(r["kf"]-0.05) < 1e-9][0]
ck["2d"]["22"]["cT_GK_kf005"] = gk["modes"][1]["om"]/gk["q"]
ck["2d"]["22"]["fsum_resid_max"] = max(abs(r["fsum_ratio"]-1) for r in A["soft_g22"]["rows"])
ck["2d"]["22"]["static_resid_max"] = max(abs(r["static_ratio"]-1) for r in A["soft_g22"]["rows"])
E = H["elastic"]; P = H["prediction"]
ck["hydro_g22"] = {"f_s": E["f_s"], "alpha": E["alpha_R"], "M": E["M_R"], "Cxxyy": E["Cxxyy"], "mu": E["mu_R"],
                   "gamma": E["gamma"], "F_minus": P["F_minus"], "c_minus": P["c_minus"], "c_plus": P["c_plus"],
                   "c_T": P["c_T"], "static_share_minus": P["static_share_minus"]}
d3 = T["three_d"]
r015 = [r for r in D3["rows"] if r["dir"] == "basal_GM" and abs(r["q"]-0.15) < 1e-9][0]
ck["3d"] = {"c2": d3["c2"], "cT_min": d3["cT_range"][0], "cT_max": d3["cT_range"][1], "c1_basal_q015": r015["om"][6]/r015["q"],
            "F2_basal_q015": r015["fshare"][0], "Z21_basal_q015": r015["Z"][0]/r015["Z"][6], "S2_basal_q015": r015["sshare"][0],
            "c_kappa": S3["c_kappa"]}
ck["melting"] = {"Lambda_c": T["Lambda_c"], "Lambda_u": T["Lambda_u"], "energy_crossing": T["energy_crossing"],
                 "ratio_at_Lambda_c": T["ratio_at_Lambda_c"], "F2_at_Lambda_c": T["F2_at_Lambda_c"],
                 "ratio_max_metastable": T["ratio_max_metastable"], "branch_end_g": 12.47, "never_reaches_one": True}
rd = S3["readings"]
ck["loss"] = {"v467_best_orders": S3["V467"]["best"], "v467_worst_orders": S3["V467"]["worst"],
              "main_orders_recovered": rd["fixed vertex, filament (main)"]["orders_recovered"],
              "main_headline_orders": rd["fixed vertex, filament (main)"]["headline"],
              "band_orders": [min(min(v["headline"]) for v in rd.values()), max(max(v["headline"]) for v in rd.values())],
              "xi_req_main_m": rd["fixed vertex, filament (main)"]["xi_req_m"],
              "eq3_coefficient": 16*3.141592653589793*10*(7.68/S3["c_kappa"])**4/d3["F2_range"][0],
              "eq4_bound": 1/(2*3.1974e11**2), "drag_prefactor_3d": "rho*F/(4*pi*v^2)"}
json.dump(ck, open("lbc_chat_checkpoint.json", "w"), indent=1)
print(json.dumps(ck, indent=1)[:3000])
