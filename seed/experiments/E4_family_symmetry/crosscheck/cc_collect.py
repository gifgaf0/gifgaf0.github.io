"""
cc_collect.py -- compares the cross-check outputs (out/*_cc.json, out/texture_cc*.jsonl) with the original
results.json and writes crosscheck.json. Run after the other cc_*.py scripts.
"""
import json, math, collections, os
import numpy as np

HERE = "/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/"
ORIG = json.load(open(HERE + "../results.json"))
g = json.load(open(HERE + "out/groups_cc.json"))
l = json.load(open(HERE + "out/lnr_cc.json"))
y = json.load(open(HERE + "out/yukawa_cc.json"))
r = json.load(open(HERE + "out/residual_cc.json"))
tex = [json.loads(x) for x in open(HERE + "out/texture_cc.jsonl") if x.strip()]
texr = [json.loads(x) for x in open(HERE + "out/texture_cc_minreal.jsonl") if x.strip()] if os.path.exists(HERE + "out/texture_cc_minreal.jsonl") else []

# ---------------------------------------------------------------- texture comparison, class by class
def norm_orig(name):
    # 'lepton|min|phi10=Z3|phi5=G|phi1=Z3' -> ('lepton','min','Z3'(phi5),'Z3'(phi10),...) canonical
    parts = name.split("|")
    if "LNR exact" in name: return ("lepton", "LNR")
    d = dict(p.split("=") for p in parts[2:])
    if parts[0] == "lepton": return ("lepton", parts[1], d["phi5"], d["phi10"], d["phi1"])
    return ("quark", parts[1], d["phi10"], d["phi5"])
def norm_mine(name):
    if "LNR-exact" in name: return ("lepton", "LNR")
    sec, var, rest = name.split(":")
    d = dict(p.split("=") for p in rest.split(","))
    if sec == "lep": return ("lepton", var, d["phi5"], d["phi10"], d["phi1"])
    return ("quark", var, d["phi10"], d["phi5"])
orig = {norm_orig(c["name"]): c for c in ORIG["texture_survey_all"]}
mine = {norm_mine(c["name"]): c for c in tex if ":minreal:" not in c["name"]}
rows, disagree = [], []
for k, o in orig.items():
    m = mine.get(k)
    if m is None:
        disagree.append((k, "missing in cross-check")); continue
    same_verdict = (o["verdict_final"] == m["verdict"])
    same_neff = (o["verdict_final"] == "excluded (structural)") or (o["n_eff"] == m["n_eff"])
    chi_ok = True
    if o["verdict_final"] == "excluded":
        chi_ok = abs(o["chi2"] - m["chi2"]) < 0.02 * o["chi2"] + 0.2
    rows.append(dict(cls="|".join(k), orig_verdict=o["verdict_final"], cc_verdict=m["verdict"], orig_neff=o["n_eff"], cc_neff=m["n_eff"],
                     orig_npar=o["n_par"], cc_npar=m["npar"], orig_chi2=o["chi2"], cc_chi2=m["chi2"], agree=bool(same_verdict and same_neff and chi_ok)))
    if not (same_verdict and same_neff and chi_ok): disagree.append((k, o["verdict_final"], m["verdict"], o["n_eff"], m["n_eff"], o["chi2"], m["chi2"]))
count_cc = collections.Counter((k[0], m["verdict"]) for k, m in mine.items())
summary_tex = {"lepton": {}, "quark": {}}
for (sec, v), n in count_cc.items(): summary_tex[sec][v] = n
print("texture classes compared:", len(rows), " disagreements:", len(disagree))
for d in disagree: print("  ", d)
print("cross-check survey summary:", summary_tex)
print("original survey summary  :", ORIG["texture_survey_summary"])

minreal = [dict(name=c["name"], npar=c["npar"], n_eff=c["n_eff"], dof=c["dof"], chi2=c["chi2"], verdict=c["verdict"],
                p=(None if c["dof"] < 1 else float(1 - __import__("scipy.stats", fromlist=["chi2"]).chi2.cdf(c["chi2"], c["dof"]))))
           for c in texr if c["verdict"] != "excluded (structural)"]
for c in minreal: print("  minreal:", c)

out = dict(
    experiment="E4 cross-check (independent re-computation)",
    scripts=["cc_groups.py", "cc_lnr.py", "cc_yukawa.py", "cc_residual.py", "cc_z2gen.py", "cc_texture.py", "cc_collect.py", "test_texture_forms.py"],
    checks={"groups": g["checks"], "lnr": l["checks"], "yukawa": y["checks"], "residual": r["checks"]},
    groups=dict(orders=g["orders"], F21_table=g["F21_table"], PSL_table=g["PSL_table"], branch_PSL_F21=g["branch_PSL_F21"],
                branch_SU3_PSL=g["branch_SU3_PSL"], F21_invariants=g["F21_invariants_33bb"], A8_max_dev=g["A8_max_dev"]),
    lnr=dict(eigenvalues=l["eigenvalues"], r=l["r"], masses_beta_m1=l["masses_beta_m1"], alpha_windows=l["alpha_windows"],
             alpha_refit=l["alpha_refit"], haze=l["haze"], pulls=l["nufit_pulls_LNR_haze"], Mnu_stabilizer_in_PSL=l["Mnu_stabilizer_in_PSL"]),
    yukawa=dict(F21_dirac_table=y["F21_dirac_table"], PSL_dirac_table=y["PSL_dirac_table"], majorana_counts=y["majorana_counts"]),
    residual=dict(F21=r["F21"], PSL=r["PSL"], z2_partial=[{k: v for k, v in q.items() if k != "info"} | {"best": q["info"]} for q in r["z2_partial"]]),
    texture=dict(summary_cc=summary_tex, summary_original=ORIG["texture_survey_summary"], n_compared=len(rows),
                 n_disagree=len(disagree), disagreements=[list(map(str, d)) for d in disagree], per_class=rows,
                 minreal_sensitivity=minreal),
)
json.dump(out, open(HERE + "crosscheck.json", "w"), indent=1, default=str)
print("wrote crosscheck.json")
