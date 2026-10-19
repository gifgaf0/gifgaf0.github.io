"""
cc2_collect.py -- assembles crosscheck.json from BOTH cross-check passes and the original results.json.

First pass  (cc_groups, cc_lnr, cc_yukawa, cc_residual, cc_z2gen, cc_texture[--minreal]):  out/*_cc.json(l)
Second pass (cc2_exact_invariants, cc2_lnr_closed, cc2_minreal_verify, cc2_texture_convfix): out/*_cc2.json(l)
Run after all of them.  Deterministic; prints a short summary.
"""
import json, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
O = HERE + "out/"
ORIG = json.load(open(HERE + "../results.json"))
ld = lambda f: json.load(open(O + f))
g, l, y, r, z2 = ld("groups_cc.json"), ld("lnr_cc.json"), ld("yukawa_cc.json"), ld("residual_cc.json"), ld("z2gen_cc.json")
ex, lc, mv = ld("exact_invariants_cc2.json"), ld("lnr_closed_cc2.json"), ld("minreal_verify_cc2.json")
tex = [json.loads(x) for x in open(O + "texture_cc.jsonl") if x.strip()]
texr = [json.loads(x) for x in open(O + "texture_cc_minreal.jsonl") if x.strip()]
fix = [json.loads(x) for x in open(O + "texture_cc2_convfix.jsonl") if x.strip()]

# ---------------------------------------------------------------- texture comparison class by class
def norm_orig(name):
    p = name.split("|")
    if "LNR exact" in name: return ("lepton", "LNR")
    d = dict(q.split("=") for q in p[2:])
    return ("lepton", p[1], d["phi5"], d["phi10"], d["phi1"]) if p[0] == "lepton" else ("quark", p[1], d["phi10"], d["phi5"])
def norm_mine(name):
    if "LNR-exact" in name: return ("lepton", "LNR")
    sec, var, rest = name.split(":")
    d = dict(q.split("=") for q in rest.split(","))
    return ("lepton", var, d["phi5"], d["phi10"], d["phi1"]) if sec == "lep" else ("quark", var, d["phi10"], d["phi5"])
orig = {norm_orig(c["name"]): c for c in ORIG["texture_survey_all"]}
mine = {norm_mine(c["name"]): c for c in tex}
for c in fix:                                  # second pass: consistent-convention refits replace first-pass gen lepton fits
    mine[norm_mine(c["name"])] = dict(mine[norm_mine(c["name"])], **{k: c[k] for k in ("n_eff", "dof", "chi2", "verdict")}, convfix=True)
per, dis = [], []
for k, o in orig.items():
    m = mine[k]
    same_v = o["verdict_final"] == m["verdict"]
    same_n = o["verdict_final"] == "excluded (structural)" or o["n_eff"] == m["n_eff"]
    per.append(dict(cls="|".join(k), orig=o["verdict_final"], cc=m["verdict"], orig_neff=o["n_eff"], cc_neff=m["n_eff"],
                    orig_chi2=o["chi2"], cc_chi2=m["chi2"], agree=bool(same_v and same_n)))
    if not (same_v and same_n): dis.append(per[-1])
cnt = collections.Counter((k[0], m["verdict"]) for k, m in mine.items())
summ = {"lepton": {}, "quark": {}}
for (s, v), n in cnt.items(): summ[s][v] = n
minreal = [dict(name=c["name"], npar=c["npar"], n_eff=c["n_eff"], dof=c["dof"], chi2=c["chi2"], verdict=c["verdict"])
           for c in texr if c["verdict"] not in ("excluded (structural)",)]
relab = [c["name"] for c in ORIG["texture_survey_all"] if c["verdict_fit"] == "excluded" and c["verdict_final"] == "excluded (structural)"]

checks = {"first_pass": {"groups": g["checks"], "lnr": l["checks"], "yukawa": y["checks"], "residual": r["checks"]},
          "second_pass": {"exact_invariants": ex["checks"], "lnr_closed": lc["checks"], "minreal_verify": mv["checks"]}}
n_pass = sum(v for d in checks.values() for dd in d.values() for v in dd.values())
n_all = sum(len(dd) for d in checks.values() for dd in d.values())

out = dict(
    experiment="E4 cross-check (independent re-computation, two passes)",
    overall="confirmed_with_corrections",
    scripts={"first_pass": ["cc_groups.py", "cc_lnr.py", "cc_yukawa.py", "cc_residual.py", "cc_z2gen.py", "cc_texture.py", "cc_minreal_detail.py", "test_texture_forms.py", "cc_collect.py (superseded by cc2_collect.py)"],
             "second_pass": ["cc2_exact_invariants.py", "cc2_lnr_closed.py", "cc2_minreal_verify.py", "cc2_texture_convfix.py", "cc2_collect.py"]},
    checks=checks, checks_passed=f"{n_pass}/{n_all}",
    failed_checks_explained={"first_pass/residual: PSL best lepton chi2 = 200":
        "cross-check gets 162.1. Diagnosis (original code, data_targets.pull_delta and e4_fits.lepton_pulls): delta is wrapped into "
        "[bf-180, bf+180) = [-3, 357) deg before the one-sided pull, so delta = 0 = 360 deg (inside NuFIT's 3sigma range 96..422) "
        "gets pull -6.56 instead of +2.24. Reproducing that wrap gives 200.05. Verdict unchanged (excluded either way)."},
    groups=dict(orders=g["orders"], F21_table=g["F21_table"], PSL_table=g["PSL_table"], branch_PSL_F21=g["branch_PSL_F21"],
                branch_SU3_PSL=g["branch_SU3_PSL"], F21_invariants=g["F21_invariants_33bb"], A8_max_dev=g["A8_max_dev"],
                F21_kron_monomial=ex["F21_kron_monomial"], LNR_Mdir_structure_match=ex["LNR_Mdir_structure_match"]),
    lnr=dict(eigenvalues=l["eigenvalues"], r=l["r"], masses_beta_m1=l["masses_beta_m1"], alpha_windows_grid=l["alpha_windows"],
             alpha_windows_exact=lc["alpha_windows_exact"], alpha_refit_exact=lc["alpha_refit_exact"], haze=lc["haze"], pulls=lc["pulls"],
             LNR_exact_no_haze_chi2=lc["LNR_exact_no_haze_chi2"], Mnu_stabilizer_in_PSL=l["Mnu_stabilizer_in_PSL"]),
    yukawa=dict(F21_dirac_table_characters=y["F21_dirac_table"], F21_dirac_table_monomial=ex["F21_dirac_table_monomial"],
                PSL_dirac_table=y["PSL_dirac_table"], majorana_counts=y["majorana_counts"], stabilisers=y["stabilisers"]),
    residual=dict(F21=r["F21"], PSL=r["PSL"], z2_partial=r["z2_partial"], z2_generated_group_orders=z2),
    texture=dict(summary_cc=summ, summary_original=ORIG["texture_survey_summary"], n_compared=len(per), n_disagree=len(dis),
                 disagreements=dis, per_class=per,
                 note_first_pass_disagreement="first pass: lepton|min|G|P|P chi2 76.31 vs original 72.49 (same verdict; the original's "
                                              "minimum is lower, i.e. the first-pass optimiser stopped higher). The 4 classes at 72.49 agree otherwise.",
                 convention_fix="second pass refitted all 64 'gen' lepton classes with a consistent (holomorphic) PMNS convention; "
                                "the first pass mixed conventions (U_e from M_e M_e^dagger, U_nu conjugated)",
                 relabelled_after_rank_scan=dict(n=len(relab), names=relab, report_says=23)),
    real_coupling_variant=dict(first_pass_minreal_nonstructural=minreal, second_pass=mv["classes"],
        note="NOT part of the original survey: LNR 'min' classes with real alpha, beta (LNR's own convention). "
             "Classes phi5=Z3/phi1=P, phi5=P/phi1=Z3, phi5=P/phi1=P (each with phi10=G) have dof = 1 and p > 0.01, i.e. they "
             "SURVIVE the preregistered rule. With complex alpha, beta (the original's unstated choice) they have dof = 0."),
)
json.dump(out, open(HERE + "crosscheck.json", "w"), indent=1, default=str)
print(f"checks passed {n_pass}/{n_all}; texture classes compared {len(per)}, disagreements {len(dis)}")
for d in dis: print("  ", d)
print("cc summary:", summ); print("orig summary:", ORIG["texture_survey_summary"])
print("relabelled after rank scan:", len(relab))
for k, v in mv["classes"].items(): print("  real/complex variant", k, "dof", v["dof"], "chi2", round(v["chi2"], 4), "p", v["p"])
print("wrote crosscheck.json")

# ---------------------------------------------------------------- audit (issues and claim audit, written after reading the original code)
AUDIT = {
 "issues": [
  {
   "severity": "major",
   "description": "Texture-survey headline '0 predictive survivors / no alignment class both fits and predicts' depends on an unstated choice: in the 'min' (LNR leading-order) variant alpha and beta are COMPLEX in the original code (e4_fits.coupl / lepton_obs), while LNR use real alpha = beta = -1. With real alpha, beta (CP-conserving couplings, CP violation only from vev phases) the classes phi10=G with (phi5,phi1) = (Z3,P), (P,Z3), (P,P) have N_eff = 6, dof = 1 and fit NuFIT 6.0 with chi2 = 0.14 / 0.02 / 0.14 (p = 0.71 / 0.89 / 0.71): they SURVIVE the preregistered rule. Found in the first pass (cc_texture --minreal) and confirmed by independent code (cc2_minreal_verify.py).",
   "suggested_fix": "State that alpha, beta are complex in 'min'; report the real-coupling variant (3 survivors, dof = 1; their 'prediction' is a discrete set of delta values) and soften 'none fits and predicts' to 'none with complex couplings'."
  },
  {
   "severity": "minor",
   "description": "delta pull wraps delta into [bf-180, bf+180) = [-3, 357) deg (data_targets.pull_delta, e4_fits.lepton_pulls), inconsistent with NuFIT's asymmetric 3sigma range 96..422 deg: delta = 0 = 360 gets pull -6.56 instead of +2.24. Best PSL full-residual lepton pattern is chi2 = 162.1, not 200; non-surviving Z2-partial classes are inflated (e.g. 400.75 vs 362.80). No pass/fail verdict changes (all texture survivors/accommodations and the three Z2-partial survivors have delta inside 96..357).",
   "suggested_fix": "Pick the representative delta + 360k closest in pull (or wrap into [96, 456)); correct 200 -> 162 in report and results.json."
  },
  {
   "severity": "minor",
   "description": "Report/summary say 23 fit-'excluded' classes were relabelled structural after the rank scan, with chi2 'about 5e3 to 1e4' and m_e/m_mu or m_d/m_s 1e-7..1e-4 rounding noise. results.json itself has 26 relabelled (22 lepton + 4 quark), chi2 from 1.5e3 to 3.1e6; the rounding-noise explanation fits the 19 Z7 classes, the other 7 are dead through r = 1 degeneracy or a permutation CKM.",
   "suggested_fix": "Change 23 -> 26 and the chi2 range; split the causes."
  },
  {
   "severity": "minor",
   "description": "'Three distinct masses need 1+1'+1'' vevs together' is overstated: any two of the three singlet vevs (1+1', 1+1'', 1'+1'') already give three distinct masses generically (checked numerically).",
   "suggested_fix": "Say 'at least two of 1, 1', 1'' (F21 broken to Z7) or triplet vevs'."
  },
  {
   "severity": "minor",
   "description": "'10 distinct mixing patterns' (F21) and '97' (PSL) count (sector kind, G_l type, G_nu type, |U|^2) tags, double counting the same matrix for quark and Dirac-lepton use; the number of distinct |U|^2 structures up to row/column permutations is 3 (F21) and 26 (PSL).",
   "suggested_fix": "Define the count or quote distinct |U|^2 structures."
  },
  {
   "severity": "minor",
   "description": "The haze sign is described as 'an input chosen to reproduce LNR's 32.4 deg'; it is fixed by LNR's printed U_-1 (only that sign reproduces all nine entries of their displayed U_MNSP to O(lambda)), so it is not a free choice.",
   "suggested_fix": "Say the sign is LNR's (their printed U_-1)."
  },
  {
   "severity": "minor",
   "description": "'Leptonic patterns that fit come from PSL(2,7)'s Z2 elements (shared with S4)': true for TM1 (<Z3,t> = S4) and TM2 (<Z3,t> = A4); the Z7 class generates the whole PSL(2,7) (<Z7,t> = 168), so '(shared with S4)' does not apply to it. The report's table text is correct.",
   "suggested_fix": "Restrict the parenthesis to TM1/TM2."
  }
 ],
 "claim_audit": [
  {
   "claim": "<D,C> has order 21, <D,C,Rf> order 168, F21 subgroup; Rf = LNR A^[3], Rf D = B^[3]",
   "verdict": "supported",
   "note": "own exact Q(zeta7) arithmetic; presentation relations of PSL(2,7) verified exactly"
  },
  {
   "claim": "Character tables, FS indicators, Kronecker products, branchings, A^[8], CGs match LNR (17/17 CALIBRATED)",
   "verdict": "supported",
   "note": "Burnside + tensor-power peeling; exact monomial counting for F21; LNR targets re-read in 0709.1447"
  },
  {
   "claim": "Coupling tables, closed-form mass matrices, Schur degeneracy",
   "verdict": "supported",
   "note": "three methods agree (characters, Reynolds, exact monomial)"
  },
  {
   "claim": "Distinct masses need 1+1'+1'' together",
   "verdict": "overstated",
   "note": "two singlet vevs suffice"
  },
  {
   "claim": "LNR seesaw reproduced (M_nu, 1:-2:9, 80/3, alpha windows, theta13 2.82, theta12 32.4)",
   "verdict": "supported",
   "note": "closed form; the 5 F21 invariants are exactly LNR's displayed M_Dir structures"
  },
  {
   "claim": "LNR example excluded by NuFIT 6.0 (theta13 -34 sigma, r -7.8 sigma)",
   "verdict": "supported",
   "note": "-34.07, -7.82"
  },
  {
   "claim": "No F21 subgroup can be the residual symmetry of a non-degenerate Majorana mass matrix",
   "verdict": "supported",
   "note": "exact sympy, all 7 Z3"
  },
  {
   "claim": "F21 residual patterns all excluded (best lepton 2459, CKM 1.08e5)",
   "verdict": "supported",
   "note": "2459.1, 1.083e5"
  },
  {
   "claim": "PSL full-residual best lepton chi2 = 200",
   "verdict": "wrong",
   "note": "162.1; delta-wrap bug; verdict unchanged"
  },
  {
   "claim": "PSL Z2-partial: 3 of 12 fit (Z7 2.13, TM1 2.54, TM2 7.63)",
   "verdict": "supported",
   "note": "2.133, 2.541, 7.628; next 31.53"
  },
  {
   "claim": "Texture survey counts 90/5/34 and 29/0/3; 0 survivors",
   "verdict": "supported",
   "note": "161/161 class verdicts and N_eff reproduced (gen classes refitted with a consistent PMNS convention)"
  },
  {
   "claim": "No alignment class in this framework both fits and predicts",
   "verdict": "overstated",
   "note": "true only for complex alpha, beta; with LNR's real couplings 3 classes survive with dof = 1"
  },
  {
   "claim": "23 classes relabelled structural, chi2 5e3-1e4",
   "verdict": "wrong",
   "note": "26 in results.json, chi2 1.5e3-3.1e6"
  },
  {
   "claim": "Seed verdicts: section 3 CONFIRMED (x3), Schur CONFIRMED, residual misalignment AMENDED, LNR excluded CONFIRMED, 'F21 does a job' AMENDED",
   "verdict": "supported",
   "note": "verdict words hold; the 'does a job' evidence needs the real-coupling caveat"
  }
 ],
 "independent_values_summary": "all headline numbers reproduced except PSL best full-residual lepton chi2 (162.1 vs 200, delta-wrap bug, verdict unchanged)"
}
out.update(AUDIT)
json.dump(out, open(HERE + "crosscheck.json", "w"), indent=1, default=str)
print("audit:", len(AUDIT['issues']), "issues,", len(AUDIT['claim_audit']), "claims")
