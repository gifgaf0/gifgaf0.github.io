"""
collect_results.py -- assemble results.json (headline numbers with units/conventions, target,
tolerance, source and verdict) from out/groups.json, out/yukawa.json, out/lnr.json, out/fits.jsonl,
out/realcoupling.json and out/reconcile_checks.json (reconciliation).
out/structure.json (e4_structure.py: exact generic-rank scan used for the structural diagnosis).
Run last:  python3 collect_results.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
G = json.load(open(os.path.join(OUT, "groups.json")))
Y = json.load(open(os.path.join(OUT, "yukawa.json")))
L = json.load(open(os.path.join(OUT, "lnr.json")))
F = [json.loads(l) for l in open(os.path.join(OUT, "fits.jsonl"))]
S = json.load(open(os.path.join(OUT, "structure.json")))      # exact generic-rank scan (e4_structure.py)
ROB_PATH = os.path.join(OUT, "robustness.json")                # e4_robustness.py (determinism, 300-start check)
ROB = json.load(open(ROB_PATH)) if os.path.exists(ROB_PATH) else None
RC = json.load(open(os.path.join(OUT, "realcoupling.json")))          # e4_realcoupling.py (reconciliation)
RK = json.load(open(os.path.join(OUT, "reconcile_checks.json")))      # e4_reconcile_checks.py (reconciliation)
F_ALL = F
F = [r for r in F_ALL if not r["variant"].endswith("-real")]         # original survey: complex couplings (161 classes)
FR = [r for r in F_ALL if r["variant"].endswith("-real")]            # reconciliation: real couplings (144 classes)

cal = []


def add(quantity, ours, target, tol, source, ok, note=""):
    cal.append({"quantity": quantity, "value": ours, "target": target, "tolerance": tol, "source": source,
                "verdict": "CALIBRATED" if ok else "MISS", "note": note})


gc, yc, lc = G["checks"], Y["checks"], L["checks"]
add("group orders |<D,C>|, |<D,C,Rf>|", f"{G['orders']['F21']}, {G['orders']['PSL']}", "21, 168", "exact",
    "SEED.md section 3; LNR 0709.1447", G["orders"] == {"F21": 21, "PSL": 168})
add("seed Rf and Rf*D versus LNR triplet generators A, B (eqs. 22-23)", "identical (exact Q(zeta7) arithmetic)",
    "LNR A^[3], B^[3]", "exact", "LNR 0709.1447 eqs. (22)-(23)",
    gc["seed Rf = LNR A^[3] (eq. 23), exactly"]["pass"] and gc["LNR B^[3] (eq. 22) = A D exactly, i.e. LNR AB = D"]["pass"])
add("F21 character table (classes 1, 7(d), 7(d^2), 3(c), 3(c^3))", G["char_table_F21"],
    "1:(1,1,1,1,1) 1':(1,w,w^2,1,1) 1'':(1,w^2,w,1,1) 3:(3,0,0,b7,b7bar) 3bar:(3,0,0,b7bar,b7)", "exact",
    "LNR 0709.1447 Sec. 5", any(k.startswith("F21 character table = LNR") and v["pass"] for k, v in gc.items()))
add("PSL(2,7) character table (classes 1, 21A, 56B, 42[A,B], 24AB, 24AB^2)", G["char_table_PSL"],
    "LNR table (3:(3,-1,0,1,b7,b7bar), 6:(6,2,0,0,-1,-1), 7:(7,-1,1,-1,0,0), 8:(8,0,-1,0,1,1))", "exact",
    "LNR 0709.1447 Sec. 3", gc["PSL character table = LNR Sec. 3 table"]["pass"])
add("F21 Kronecker products", {k: G["kronecker_F21"][k] for k in ("3 x 3", "3 x 3b")},
    "3x3 = (3+3bar)_s + 3bar_a ; 3x3bar = 1+1'+1''+3+3bar", "exact", "LNR 0709.1447 Sec. 5; 0706.2341 Sec. 3.1; PLAN E4",
    any(k.startswith("F21 Kronecker products = LNR") and v["pass"] for k, v in gc.items()))
add("PSL(2,7) Kronecker products (all 14 products of non-trivial irreps)", {k: G["kronecker_PSL"][k] for k in ("3 x 3", "3 x 3b")},
    "3x3 = 6_s + 3bar_a ; 3x3bar = 1+8 ; and LNR's other 12 entries", "exact", "LNR 0709.1447 Sec. 3; PLAN E4",
    gc["PSL(2,7) Kronecker products = LNR table (all 14 entries)"]["pass"])
add("branching PSL(2,7) -> F21", G["branching_PSL_to_F21"], "6=3+3bar, 7=1+3+3bar, 8=1'+1''+3+3bar", "exact",
    "LNR 0709.1447 Sec. 5; 0706.2341 Sec. 3", any(k.startswith("PSL(2,7) -> F21 branching") and v["pass"] for k, v in gc.items()))
add("branching SU(3) -> PSL(2,7), 11 irreps up to (2,2)", {k: v["decomp"] for k, v in G["branching_SU3_to_PSL"].items()},
    "LNR table (dimension content; bars lost in the PDF text)", "exact", "LNR 0709.1447 Sec. 3",
    any(k.startswith("SU(3) -> PSL(2,7) branching") and v["pass"] for k, v in gc.items()))
add("LNR octet generator A^[8] (Gell-Mann basis), all 64 entries", "max deviation 3e-16",
    "LNR eq. (46)", "1e-12", "LNR 0709.1447 eq. (46)", gc["LNR eq. (46): all 64 entries of A^[8] (Gell-Mann basis) reproduced"]["pass"])
add("F21 Clebsch-Gordan coefficients (D-diagonal basis)", "all 8 LNR combinations are intertwiners",
    "LNR eqs. (64)-(66)", "exact", "LNR 0709.1447 eqs. (64)-(66)",
    any(k.startswith("LNR F21 Clebsch-Gordan coefficients") and v["pass"] for k, v in gc.items()),
    "LNR act with row convention (their eq. 28); in the column convention used here their 1' and 1'' "
    "singlet combinations exchange (omega <-> omega^2); triplet CGs identical in both conventions")
add("number of F21 invariants in 3x3x3barx3bar (LNR operator psi psi' xi xi')", 5, 5, "exact", "LNR 0706.2341 Sec. 3.1, 4.1",
    any(k.startswith("LNR effective operator") and v["pass"] for k, v in yc.items()))
add("LNR seesaw M_Maj, M_Dir, M_nu at alpha=beta=-1", L["matrices"]["M_nu"],
    "M_Maj=[[1,-1,-1],[-1,1,-1],[-1,-1,1]], M_Dir=[[-1,0,0],[0,1,-2],[0,-2,1]], M_nu ~ (1/2)[[0,1,1],[1,-4,5],[1,5,-4]]",
    "exact", "LNR 0706.2341 Sec. 4.1",
    all(v["pass"] for k, v in lc.items() if k.startswith("M_")))
add("LNR light-neutrino eigenvalue ratios", L["matrices"]["eigenvalue_ratios"], [1, -2, 9], "exact", "LNR 0706.2341 Sec. 4.1",
    L["matrices"]["eigenvalue_ratios"] == [1, -2, 9])
add("Dm31^2/Dm21^2 at alpha=beta=-1", "80/3 = 26.667", "80/3 (LNR: 26.7)", "exact", "LNR 0706.2341 Sec. 4.1",
    L["r_atm_sol_exact"] == "80/3")
add("alpha windows for r in [21.3, 45.1] (beta=-1, normal ordering)", L["alpha_windows_LNR_range_21.3_45.1"],
    L["alpha_windows_quoted_by_LNR"], "0.01 (LNR's two decimals)", "LNR 0706.2341 Sec. 4.1",
    any(k.startswith("LNR's alpha windows") and v["pass"] for k, v in lc.items()))
h = L["haze"]["pole masses"]
add("theta13 with charged-lepton haze lambda_e = sqrt(me/mmu) (pole masses)", f"{h['theta13_linear_deg']:.3f} deg", "2.8 deg",
    "0.05 deg", "LNR 0706.2341 Sec. 4.2", abs(h["theta13_linear_deg"] - 2.8) < 0.05)
add("theta12 with the same haze", f"{h['theta12_linear_deg']:.2f} deg", "32.4 deg", "0.05 deg", "LNR 0706.2341 Sec. 4.2",
    abs(h["theta12_linear_deg"] - 32.4) < 0.05, "the sign of the haze rotation is the one in LNR's printed U_-1 "
    f"(it reproduces all nine entries of their U_MNSP); the opposite sign gives {h['opposite_sign_theta12_deg']:.2f} deg")

cmp = L["comparison_NuFIT6"]
findings = [
    {"quantity": "Schur: singular values of the general F21- (PSL-) invariant mass matrix for L=R=3 with a trivial scalar",
     "value": "three equal (1 coupling); L=3,R=3bar: 0 couplings; Majorana 3x3x1: 0 couplings", "target": "PLAN E4: degenerate",
     "tolerance": "exact", "verdict": "NO_TARGET", "note": "commutant of the triplet is 1-dimensional for both groups; "
     "a single 1, 1' or 1'' vev gives equal |masses|, any two of them already give three distinct masses (F21 broken to Z7)"},
    {"quantity": "LNR integer point vs NuFIT 6.0: sin^2 theta13", "value": f"{cmp['sin2_theta13']['LNR']:.5f}",
     "target": "0.02195 (+0.00054 -0.00058)", "tolerance": "pull with sigma from 3sigma range/3",
     "verdict": "NO_TARGET", "outcome": "excluded by data", "note": f"pull {cmp['sin2_theta13']['pull']:.1f} sigma"},
    {"quantity": "LNR integer point vs NuFIT 6.0: Dm31^2/Dm21^2", "value": "26.667 (80/3)", "target": "33.83 +- 0.92",
     "tolerance": "1 sigma", "verdict": "NO_TARGET", "outcome": "excluded by data", "note": f"pull {cmp['r_atm_sol']['pull']:.1f} sigma"},
    {"quantity": "LNR alpha refit to NuFIT ratio (beta=-1)", "value": f"alpha = {', '.join(f'{a:.4f}' for a in L['alpha_solving_r_eq_NuFIT6_central'])}",
     "target": "r = 33.83", "tolerance": "fit", "verdict": "NO_TARGET",
     "note": "mixing stays exactly tri-bimaximal (theta13 = 0) for every alpha; m3/m1 = 9 for every alpha"},
]
# residual patterns
for gname in ("F21", "PSL"):
    rows = Y["residual_patterns"][gname]
    best_l = min((p for p in rows if p["kind"] != "quark"), key=lambda p: p["chi2"])
    best_q = min((p for p in rows if p["kind"] == "quark"), key=lambda p: p["chi2"])
    pc = RK["pattern_counts"][gname]
    findings.append({"quantity": f"{gname}: number of full-residual-symmetry mixing patterns",
                     "value": f"{pc['tags(kind,G_l,G_nu,|U|^2)']} (sector, G_l, G_nu, |U|^2) combinations; "
                              f"{pc['distinct_absU2_structures']} distinct |U|^2 structures up to row/column permutations",
                     "target": "count", "tolerance": "exact", "verdict": "NO_TARGET", "note": json.dumps(pc["by_kind"])})
    findings.append({"quantity": f"{gname}: best full-residual-symmetry lepton pattern (0 mixing parameters, 4 obs.)",
                     "value": f"chi2 = {best_l['chi2']:.1f} ({best_l['G1']} x {best_l['G2']}, {best_l['kind']})",
                     "target": "p > 0.01", "tolerance": "chi2 test, 4 dof", "verdict": "NO_TARGET", "outcome": "excluded by data",
                     "note": f"best s12^2={best_l['best']['s12sq']:.3f}, s13^2={best_l['best']['s13sq']:.4f}, s23^2={best_l['best']['s23sq']:.3f}"})
    findings.append({"quantity": f"{gname}: best full-residual-symmetry CKM pattern (0 mixing parameters, 4 obs.)",
                     "value": f"chi2 = {best_q['chi2']:.3g} ({best_q['G1']} x {best_q['G2']})", "target": "p > 0.01",
                     "tolerance": "chi2 test, 4 dof", "verdict": "NO_TARGET", "outcome": "excluded by data",
                     "note": f"lambda = {best_q['best']['lambda']:.3f}"})
for o in sorted(Y["z2_partial_PSL"], key=lambda x: x["chi2"])[:3]:
    findings.append({"quantity": f"PSL(2,7) Z2-partial lepton class G_l={o['G_l']}, fixed column |U|^2={o['fixed_column_abs2']}",
                     "value": f"chi2 = {o['chi2']:.2f} (2 params, 4 obs., p = {o['p_value']:.2f})", "target": "p > 0.01",
                     "tolerance": "chi2 test, 2 dof", "verdict": "NO_TARGET",
                     "outcome": "fits data (p > 0.01)" if o["survives(p>0.01)"] else "excluded by data",
                     "note": f"best s12^2={o['best']['s12sq']:.3f} s13^2={o['best']['s13sq']:.4f} s23^2={o['best']['s23sq']:.3f} delta={o['best']['delta_deg']:.0f} deg"})

# texture survey: deterministic structural diagnosis from the stored best-fit observables
def diagnose(r):
    o = r.get("best_obs")
    reasons = S["classes"][r["name"]]["structural_reasons"]
    if reasons:
        return "structural (exact rank scan): " + "; ".join(reasons)
    if r.get("structural"):
        return r["structural"]
    if not o:
        return None
    if r["sector"] == "quark" and o[4] == o[4] and (o[4] < 1e-9 or abs(o[4] - 1) < 1e-9):
        return "CKM is a permutation matrix for all parameters (M_u and M_d both diagonal in this class)"
    if r["sector"] == "lepton":
        if o[0] < 1e-6 or o[1] < 1e-6:
            return "massless charged lepton at the best fit (rank <= 2)"
        if abs(o[2] - 1) < 1e-6:
            return "r = 1 exactly: degenerate pair m2 = m3 (Z3-symmetric circulant M_nu)"
        if o[4] < 1e-12 and abs(o[3] - 1 / 3) < 1e-9:
            return "exactly tri-bimaximal: theta13 = 0"
    else:
        if o[4] != o[4] or o[4] < 1e-9:
            return "CKM = 1 identically (lambda = 0)"
        if min(o[:4]) < 1e-6:
            return "massless quark at the best fit"
    return None


for r in F_ALL:
    r["diagnosis"] = diagnose(r)
    # final label: same pass/fail outcome as the fit verdict; a fit 'excluded' whose matrices are exactly
    # rank-deficient/degenerate is relabelled 'excluded (structural)' (its chi2 is then a rounding artefact)
    r["verdict_fit"] = r["verdict"]
    dead = bool(S["classes"][r["name"]]["structural_reasons"]) or (r["diagnosis"] or "").startswith("CKM is a permutation")
    r["verdict_final"] = "excluded (structural)" if (dead and r["verdict"].startswith("excluded")) else r["verdict"]
    assert not (dead and not r["verdict"].startswith("excluded")), r["name"]

def summarize(FF):
    surv_ = {"lepton": {}, "quark": {}}
    surv_fit_ = {"lepton": {}, "quark": {}}
    for r in FF:
        surv_[r["sector"]].setdefault(r["verdict_final"], []).append(r["name"])
        surv_fit_[r["sector"]].setdefault(r["verdict_fit"], []).append(r["name"])
    return ({s: {v: len(n) for v, n in d.items()} for s, d in surv_.items()},
            {s: {v: len(n) for v, n in d.items()} for s, d in surv_fit_.items()})


summary_survey, summary_survey_fitlabels = summarize(F)
summary_real, summary_real_fitlabels = summarize(FR)
survivors = [r for r in F if r["verdict_final"] == "SURVIVES"]
accom = [r for r in F if r["verdict_final"].startswith("accommodates")]
survivors_real = [r for r in FR if r["verdict_final"] == "SURVIVES"]
accom_real = [r for r in FR if r["verdict_final"].startswith("accommodates")]


def relabel_stats(FF):
    rel = [r for r in FF if r["verdict_final"] == "excluded (structural)" and r["verdict_fit"] == "excluded"]
    causes = {}
    for r in rel:
        d = r["diagnosis"] or ""
        # primary cause first: a class that is dead for two reasons is counted under the first that applies
        k = ("rank-deficient charged-fermion matrix (Z7 familon)" if " has rank " in d else
             "exactly degenerate light neutrinos (r = 1)" if "neutrinos have an exactly degenerate" in d else
             "exactly degenerate charged-fermion pair" if "has an exactly degenerate pair" in d else
             "CKM a permutation matrix (M_u, M_d both diagonal)" if "permutation" in d else d)
        causes[k] = causes.get(k, 0) + 1
    return {"n_relabelled": len(rel), "by_sector": {s: sum(r["sector"] == s for r in rel) for s in ("lepton", "quark")},
            "chi2_range": [min(r["chi2"] for r in rel), max(r["chi2"] for r in rel)] if rel else None, "causes": causes,
            "names": [r["name"] for r in rel]}


relabel = relabel_stats(F)
relabel_real = relabel_stats(FR)
best_nonaccom = {}
for s in ("lepton", "quark"):
    cands = [r for r in F if r["sector"] == s and r["verdict_final"] != "excluded (structural)" and (r.get("dof") or 0) >= 1]
    if cands:
        b = min(cands, key=lambda r: r["chi2"])
        best_nonaccom[s] = {"name": b["name"], "chi2": b["chi2"], "n_eff": b["n_eff"], "dof": b.get("dof"),
                            "p_value": b.get("p_value"), "pulls": b.get("pulls"), "best_obs": b.get("best_obs"),
                            "diagnosis": b.get("diagnosis")}
findings.append({"quantity": "F21 texture survey (LNR framework), complex couplings (161 classes): classes by verdict",
                 "value": summary_survey, "target": "report either way (PLAN E4)", "tolerance": "p > 0.01 rule",
                 "verdict": "NO_TARGET", "note": f"{len(survivors)} predictive survivors; {len(accom)} accommodate with N_eff >= N_obs"})
rc_best = {k: v["best_branch"] for k, v in RC["survivors"].items()}
rc_min = {k: (v["chi2_min_including_branch_polish"], v["p_value_at_that_minimum"]) for k, v in RC["survivors"].items()}
rc_nb = [v["n_branches_lower_bound"] for v in RC["survivors"].values()]
findings.append({"quantity": "F21 texture survey, real (CP-conserving) couplings (144 classes; reconciliation): classes by verdict",
                 "value": summary_real, "target": "report either way (PLAN E4)", "tolerance": "p > 0.01 rule",
                 "verdict": "NO_TARGET",
                 "note": f"{len(survivors_real)} predictive survivors (dof = 1): "
                         + "; ".join(f"{r['name']} chi2 {r['chi2']:.3f} (survey multistart; {rc_min[r['name']][0]:.3f} after "
                                     f"polishing from the delta branches, p {rc_min[r['name']][1]:.2f})" for r in survivors_real)
                         + f"; {len(accom_real)} accommodate with N_eff >= N_obs. Each survivor's one prediction: delta on a discrete "
                           f"set of at least {min(rc_nb) if rc_nb else 0}-{max(rc_nb) if rc_nb else 0} branches spread over the whole circle "
                           f"(union {RC['union_of_delta_branches_deg']}); nearest to NuFIT's 177 deg: 152.3 and 207.7 deg"})

res = {
    "experiment": "E4 -- the order-21 group on three generations (SEED.md sections 3, 7.3; PLAN.md section 4 E4)",
    "conventions": G["conventions"],
    "data_used": {
        "NuFIT": "NuFIT 6.0 arXiv:2410.05380v1 Table 1, IC19 w/o SK-atm, NO: s12^2 0.307(+12-11), s23^2 0.561(+12-15) "
                 "[3sigma 0.430-0.596], s13^2 0.02195(+54-58), delta 177(+19-20) deg, Dm21^2 7.49(19)e-5, Dm31^2 2.534(+25-23)e-3 eV^2; "
                 "r = 33.83 +- 0.92; chi2 sigmas = (3sigma edge - bf)/3 per side",
        "UTfit": "UTfit 2022 arXiv:2212.03894v1 Appendix: lambda 0.22519(83), A 0.828(11), rhobar 0.1609(95), etabar 0.347(10)",
        "masses": "Huang & Zhou arXiv:2009.04851v2, MS-bar at M_Z (full SM); ratios with max(exp, 10%) relative error",
    },
    "calibration": cal,
    "findings": findings,
    "residual_patterns_count": {g: len(Y["residual_patterns"][g]) for g in ("F21", "PSL")},
    "z2_partial_PSL": Y["z2_partial_PSL"],
    "texture_survey_coupling_convention": "complex couplings (alpha, beta in 'min'; all c_k, alpha in 'gen'); 'LNR exact' has real alpha. "
                                          "The real-coupling variants (min-real, gen-real) are reported separately (reconciliation).",
    "texture_survey_summary": summary_survey,
    "texture_survey_summary_fit_labels_before_rank_scan": summary_survey_fitlabels,
    "texture_survey_relabelled_by_rank_scan": relabel,
    "texture_survey_observables": {"lepton": ["me/mmu", "mmu/mtau", "Dm31^2/Dm21^2 (NO)", "s12^2", "s13^2", "s23^2", "delta_deg"],
                                   "quark": ["mu/mc", "mc/mt", "md/ms", "ms/mb", "lambda", "A", "rhobar", "etabar"]},
    "texture_survey_rule": "N_eff = generic rank of d(obs)/d(params); dof = N_obs - N_eff; dof >= 1: SURVIVES if p > 0.01; "
                           "dof <= 0: 'accommodates (no prediction)' if chi2 < 1 else excluded (fixed before fitting)",
    "texture_survey_survivors": [{k: r[k] for k in ("name", "n_par", "n_eff", "chi2", "dof", "p_value", "best_obs", "pulls")}
                                 for r in survivors],
    "texture_survey_accommodating": [{k: r.get(k) for k in ("name", "n_par", "n_eff", "chi2")} for r in accom],
    "texture_survey_all": [{k: r.get(k) for k in ("name", "verdict_final", "verdict_fit", "n_par", "n_eff", "dof", "chi2", "p_value", "diagnosis",
                                                  "best_obs", "pulls")} for r in F],
    "texture_survey_best_predictive": best_nonaccom,
    "texture_survey_real_couplings": {
        "convention": "all couplings real (alpha, beta in min-real; c_k, alpha in gen-real): CP-conserving Lagrangian, CP violated "
                      "only by vev phases. LNR take alpha = beta = -1 real and neglect phase-setting invariants (0706.2341 Sec. 3.2, 4.1).",
        "summary": summary_real, "summary_fit_labels_before_rank_scan": summary_real_fitlabels,
        "relabelled_by_rank_scan": relabel_real,
        "survivors": [{k: r[k] for k in ("name", "n_par", "n_eff", "chi2", "dof", "p_value", "best_obs", "pulls")} for r in survivors_real],
        "survivor_predictions": RC["survivors"],
        "accommodating": [{k: r.get(k) for k in ("name", "n_par", "n_eff", "chi2")} for r in accom_real],
        "all": [{k: r.get(k) for k in ("name", "verdict_final", "verdict_fit", "n_par", "n_eff", "dof", "chi2", "p_value", "diagnosis",
                                       "best_obs", "pulls")} for r in FR]},
    "reconcile_checks": RK,
    "robustness": ROB,
    "seed_claims": [
        {"claim": "SEED 3: <D, 120-degree turn> = Z7 x| Z3 (order 21) in SU(3), inside the flipped copy of Klein's PSL(2,7) (order 168)",
         "verdict": "CONFIRMED", "evidence": "exact closure in Z[zeta7, 1/7]: orders 21 and 168, F21 a subgroup; the seed's Rf equals LNR's A^[3] exactly"},
        {"claim": "SEED 3: the triplets are complex (PSL(2,7) and F21)", "verdict": "CONFIRMED",
         "evidence": "Frobenius-Schur indicator 0 for 3, 3bar of both groups; character b7 = (-1 + i sqrt7)/2 on the order-7 classes"},
        {"claim": "SEED 3: flavour model-builders used both groups as family symmetries", "verdict": "CONFIRMED",
         "evidence": "LNR 0706.2341 seesaw example reproduced exactly (matrices, eigenvalue ratios 1:-2:9, 80/3, theta13 2.82 deg)"},
        {"claim": "SEED 7.3 / PLAN: with F21 unbroken an irreducible triplet cannot get three different masses", "verdict": "CONFIRMED",
         "evidence": "commutant of the 3 is 1-dim for F21 and PSL(2,7): L=R=3 with singlet Higgs -> three equal masses; L=3,R=3bar -> none; "
                     "no Majorana singlet mass. Distinct masses need vevs of at least two of 1, 1', 1'' (F21 broken to Z7) or triplet vevs"},
        {"claim": "PLAN: mixing comes from misalignment between residual subgroups of different sectors", "verdict": "AMENDED",
         "evidence": "true for PSL(2,7) (3 of 12 Z2-partial classes fit: G_l = Z7 with <Z7,Z2> = PSL(2,7), TM1 with <Z3,Z2> = S4, TM2 with "
                     "<Z3,Z2> = A4); every full-residual pattern is excluded (best PSL lepton chi2 = 162, F21 2459); for F21 alone no subgroup can "
                     "be a non-degenerate Majorana residual symmetry (odd order: no Z2), so F21 mixing needs vevs with no residual symmetry"},
        {"claim": "PLAN: the LNR example (alpha = beta = -1) is excluded by NuFIT 6.0", "verdict": "CONFIRMED",
         "evidence": "sin^2 theta13 0.00242 vs 0.02195 (-34 sigma); r = 80/3 vs 33.83 +- 0.92 (-7.8 sigma); theta13 = 0 for every alpha without the haze"},
        {"claim": "SEED 3/7.3: F21 (inside PSL(2,7)) acting on three generations does a job", "verdict": "AMENDED",
         "evidence": "F21 restricts couplings but gives no masses or hierarchy without breaking and predicts only after vevs are chosen. "
                     f"With complex couplings {len(survivors)} of {len(F)} LNR-framework alignment classes both fit and predict "
                     f"({len(accom)} fit with N_eff = N_obs). With real (CP-conserving) couplings, LNR's own convention, "
                     f"{len(survivors_real)} of {len(FR)} classes survive with dof = 1 ("
                     + "; ".join(f"{r['name'].split('|', 1)[1]}: chi2_min {rc_min[r['name']][0]:.2f}, p {rc_min[r['name']][1]:.2f}"
                                 for r in survivors_real)
                     + "); each needs a generic (hand-put) phi10 vev for the charged-lepton masses, and its one prediction is weak: "
                       f"delta restricted to at least {min(rc_nb) if rc_nb else 0} discrete branches spread over the whole circle, "
                       "the nearest to the best fit at 152.3 and 207.7 deg"},
    ],
    "all_checks_pass": {"groups": G["all_pass"], "yukawa": Y["all_pass"], "lnr": L["all_pass"], "structure": S["all_pass"],
                        "robustness": ROB["all_pass"] if ROB else None, "realcoupling": RC["all_pass"],
                        "reconcile_checks": RK["all_pass"]},
}
with open(os.path.join(HERE, "results.json"), "w") as f:
    json.dump(res, f, indent=1, default=str)
print("calibration:", sum(c["verdict"] == "CALIBRATED" for c in cal), "/", len(cal))
print("relabelled by the rank scan (complex couplings):", relabel["n_relabelled"], relabel["by_sector"], relabel["chi2_range"], relabel["causes"])
print("real-coupling survey (final labels):", json.dumps(summary_real))
print("real-coupling survivors:", [(r["name"], round(r["chi2"], 3), r["n_eff"], round(r["p_value"], 3)) for r in survivors_real])
print("real-coupling accommodating:", len(accom_real))
print("survey (final labels):", json.dumps(summary_survey))
print("survey (fit labels before exact rank scan):", json.dumps(summary_survey_fitlabels))
print("predictive survivors:", [r["name"] for r in survivors])
print("accommodating:", [(r["name"], r["n_eff"]) for r in accom])
print("best predictive:", json.dumps(best_nonaccom, indent=1))
