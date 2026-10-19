"""Apply the E1 reconciliation (after the independent cross-check) to results.json and seed_claims.json.

Run after collect_results.py and the reconciliation analyses. Idempotent: it overwrites the fields it owns and adds
or replaces rows by their quantity name. Inputs: results.json, seed_claims.json, e1c_reconcile_analysis.json,
e1d_confound.json, e1d_speedtest.json, e1_timereversal.json.

Verdict words (PLAN.md section 1): CALIBRATED only for literature targets; CONFIRMED / AMENDED / REFUTED /
QUANTIFIED / OPEN for seed claims and the PLAN predictions derived from them; CHECK PASSED for internal checks;
NO_TARGET marks informational rows that carry no verdict.
"""
import json
import numpy as np
from scipy.stats import spearmanr

R = json.load(open("results.json"))
c = json.load(open("e1c_reconcile_analysis.json"))
cf = json.load(open("e1d_confound.json"))
sp = json.load(open("e1d_speedtest.json"))
tr = json.load(open("e1_timereversal.json"))
H = R["headline"]


def row(q):
    for h in H:
        if h["quantity"] == q:
            return h
    raise KeyError(q)


def upsert(q, **kw):
    for h in H:
        if h["quantity"] == q:
            h.update(kw)
            return h
    h = {"quantity": q}
    h.update(kw)
    H.append(h)
    return h


def add_note(h, text, tag):
    if tag not in h.get("note", ""):
        h["note"] = (h.get("note", "") + "; " if h.get("note") else "") + text


# ================================================================== E1b: offset diagnosis (minor issue 5)
for q in ("E1b critical velocity v_c (dx->0 extrapolation)", "E1b critical velocity v_c (baseline dx=0.05, x0=12)"):
    add_note(row(q), "offset diagnosis (reconciliation): the independent Fourier + RK4 cross-check (other x0, box and "
                     "integrator) gives 0.260066, within 1e-5 of ours, so the +2.6e-4 offset from 0.2598 lies in the "
                     "[summary] target, not in either computation; CALIBRATED stands (inside +-0.001)",
             "offset diagnosis")

# ================================================================== E1c (major issue 1, minor issue 4)
lad99 = c["omega_0.99_y4_ladder"]
lad91 = c["omega_0.91_hole_y4_ladder"]
conv_prod_99 = sorted(float(v) for v, d in lad99.items() if d["class"] == "converged producer")
sens_99 = sorted(float(v) for v, d in lad99.items() if d["class"] == "resolution-sensitive")
p41, p43 = c["point_0.41"], c["point_0.43"]
ens = c["omega_0.99_neighbourhood_ensemble_y4_dx0.05_dt0.02"]
div43 = c["phi0_divergence_from_finest_y4"]["0.43"]
t_div_y4_43 = sorted(d["t_diverge_phi0_gt_0.1"] for d in div43["vs_reference"]
                     if d["scheme"] == "y4" and d["t_diverge_phi0_gt_0.1"])
n_y4_43 = len(p43["y4_calls"])
n_y4_43_pair = sum(1 for x in p43["y4_calls"] if x[2])
n_lf_43 = len(p43["lf_calls"])
n_lf_43_pair = sum(1 for x in p43["lf_calls"] if x[2])
h = row("E1c (omega,v)=(0.99,0.43) produces a pair")
h.update({
    "value": {"fourth_order_y4_calls_(dx,dt,pair_at_T,since)": p43["y4_calls"],
              "original_leapfrog_calls_(dx,dt,pair_at_T,since)": p43["lf_calls"],
              "crosscheck_calls": "no pair to 1.5T: FD6+RK4 (dx 0.08, dt 0.032); Fourier + 4th-order splitting at "
                                  "(dx, dt) = (0.1, 0.02), (0.05, 0.02), (0.1, 0.01)",
              "phi0_divergence_times_between_y4_resolutions": t_div_y4_43},
    "units_convention": "DSV criterion: pair present at t=T (one light-crossing time); evolved to 1.5T",
    "verdict": "OPEN",
    "note": (f"RECONCILED (cross-check M1 upheld in part): the call is not demonstrated either way; the point is "
             f"chaotic. Fourth-order time stepping (Yoshida composition of the original step, e1c_reconcile.py) gives "
             f"no pair at {n_y4_43 - n_y4_43_pair} of {n_y4_43} (dx, dt) settings and a pair from t = 870 at the finest, "
             f"(0.0125, 0.005), where it sits at +-128 at T (DSV Fig. 1: about +-140); the leapfrog produces at "
             f"{n_lf_43_pair} of {n_lf_43} settings run here (4 of 11 distinct settings counting the cross-check's, pairs "
             f"forming at t = 780-1160); "
             f"the cross-check's four higher-order runs give none. phi(0,t) of the two finest y4 runs separate at "
             f"t = {lad99['0.430'].get('t_div_two_finest')}, before the pair forms, and their difference grows by a factor of ~600 between "
             f"t = 800 and 850: the trains leave a long-lived central oscillation whose fate is decided at t ~ 830-870, "
             f"beyond the convergence horizon of any affordable run. Neighbourhood ensemble inside DSV's 0.01 cell (y4, "
             f"dx 0.05, dt 0.02, v = 0.425-0.435 step 0.001): {ens['0.43']['n_producing']} of {ens['0.43']['n']} produce; "
             f"in the 0.41 cell {ens['0.41']['n_producing']} of {ens['0.41']['n']} (v = {ens['0.41']['producing_v']}). "
             f"The original 'pair since t = 1160, still separating at 1.5T, the pair is real' came from one unconverged "
             f"run (dx = 0.1, dt = 0.04, whose phi(0,t) leaves the converged one at t ~ 258). DSV-like production in this "
             f"column is converged at v = {', '.join(f'{v:.2f}' for v in conv_prod_99)} (pair from t = 590 at every "
             f"setting); OPEN."),
    "reconciled": True})

upsert("E1c omega = 0.99 column, fourth-order convergence ladder (reconciliation)",
       value={v: {"class": d["class"], "calls_(dx,dt,pair_at_T,since)": d["calls_(dx,dt,pair_at_T,since)"],
                  "original_map_call": d["original_map_call_dx0.1_dt0.04"]} for v, d in lad99.items()},
       units_convention="DSV criterion; y4 = Yoshida 4th-order composition of the original velocity-Verlet step; "
                        "converged = same call at >= 2 (dx, dt) settings",
       target="DSV Fig. 2: omega = 0.99 produces at v = 0.43 (read)", tolerance="qualitative",
       verdict="NO_TARGET", source="e1c_reconcile.py, e1c_reconcile_analysis.json",
       note=f"converged producer(s): {conv_prod_99}; resolution-sensitive: {sens_99}; single-resolution producers "
            f"(neighbourhood ensemble): {[float(v) for v, d in lad99.items() if d['class'] == 'single resolution only' and any(x[2] for x in d['calls_(dx,dt,pair_at_T,since)'])]}; "
            "every other v in 0.38-0.50 makes no pair. Production at omega = 0.99 is a sparse, fractured set near "
            "v ~ 0.40-0.41 (3 of 11 initial data in the 0.41 cell, 0 of 11 in the 0.43 cell at y4 dx 0.05); DSV's "
            "omega = 0.99 production near v ~ 0.4 is reproduced, 0.02 below their sampled point",
       reconciled=True)

# holes: resolution check of DSV's named hole (0.91, 0.82) and its neighbours
hole_cls = {v: d["class"] for v, d in lad91.items()}
hole_ok = (hole_cls.get("0.820") == "no pair at any resolution" and hole_cls.get("0.800") == "converged producer"
           and hole_cls.get("0.850") == "converged producer")
h = row("E1c holes, e.g. near (0.91,0.82)")
h["value"]["fourth_order_check_omega_0.91"] = {v: {"class": d["class"],
                                                   "calls_(dx,dt,pair_at_T,since)": d["calls_(dx,dt,pair_at_T,since)"],
                                                   "original_map_call": d["original_map_call_dx0.1_dt0.04"]}
                                               for v, d in lad91.items()}
h["verdict"] = "CALIBRATED" if hole_ok else "OPEN"
h["note"] = ("list in e1c_analysis.json; RECONCILED: the named hole was resolution-checked with fourth-order time stepping "
             "at (dx, dt) = (0.05, 0.02) and (0.025, 0.01): " + ", ".join(f"v = {v}: {k}" for v, k in hole_cls.items())
             + ("; (0.91, 0.82) makes no pair at every resolution (original leapfrog dx 0.1 and 0.05, y4 dx 0.05 and "
                "0.025) while 0.80 produces at all four and 0.85 at the three where it was run, so a hole at (0.91, 0.82) inside the band is "
                "robust; its extent is not (0.81-0.82 at dx 0.1 and y4 dx 0.05, 0.82-0.83 at y4 dx 0.025)" if hole_ok else
                "; the hole is not converged with producing neighbours on both sides"))
h["reconciled"] = True

# trend with the converged omega = 0.99 column
main = json.load(open("e1c_grid.json"))["runs"] + json.load(open("e1c_fine.json"))["runs"]
med = {}
for r in main:
    if r["produced_dsv"]:
        med.setdefault(round(r["omega"], 2), []).append(r["v"])
med[0.99] = conv_prod_99 or med.get(0.99, [])
oms = sorted(med)
rho_c = spearmanr(oms, [float(np.median(med[o])) for o in oms])
h = row("E1c producing region trends to lower v as omega rises")
add_note(h, f"reconciliation: with the omega = 0.99 column replaced by its converged producer(s) {conv_prod_99}, "
            f"Spearman rho = {rho_c[0]:.3f} (p = {rho_c[1]:.1e}); cross-check FD6 code: -0.94", "reconciliation: with")
h["reconciled"] = True
for q in ("E1c trains pass through at high v", "E1c no production for omega > 0.99"):
    add_note(row(q), "reproduced by the cross-check (FD6: 0/18 at v >= 0.86; 0/6 at omega = 0.995)", "reproduced by the")

m = c["map_vs_dsv_fig2"]
upsert("E1c map vs DSV Fig. 2, point by point (reconciliation)",
       value={k: m[k] for k in ("n_dsv_producing", "n_ours_producing", "hits", "false_positives", "missed", "jaccard",
                                 "ours_within_0.01_of_dsv")},
       units_convention="omega 0.90-0.99 x v 0.40-0.90 (step 0.01); original map dx = 0.1, dt = 0.04; DSV Fig. 2 "
                        "digitised from the arXiv PDF (dsv_fig2_reading.json)",
       target="none", tolerance="none", verdict="NO_TARGET", source="e1c_reconcile_analysis.py",
       note="replaces the report's 'band by band' wording: band locations agree, individual points often do not "
            "(cross-check, v step 0.02: 14 of 22 hits, 7 false positives); point calls at dx = 0.1 are not converged "
            "(5 of the 14 lowest-energy producers of the original map are not reproduced with fourth-order stepping: 4 make "
            "no pair at dx = 0.05, and (0.95, 0.62) makes one at dx = 0.05 but not at 0.025)",
       reconciled=True)
h = row("E1c dx check (dx 0.05 vs 0.1)")
h["note"] = ("agreement is trivial in the omega = 0.99 column: its dx = 0.1 producers (v = 0.41, 0.43) are not on the "
             "dx = 0.05 grid (step 0.02), which has no omega = 0.99 producer; the example point was not in this check")
h["reconciled"] = True

# ================================================================== E1d
# sanity check verdict word (minor issue 1)
for q in ("E1d no production below E = 2 M_kink",
          "E1d no production below E = 2 M_kink, every Gaussian run (pair and single packet, all variants)"):
    h = row(q)
    h["verdict"] = "CHECK PASSED" if h["value"] == 0 else "OPEN"
    add_note(h, "verdict word CHECK PASSED (energy-conservation sanity check, not a literature calibration); the seed "
                "claim it bears on is the section 2 row", "verdict word CHECK PASSED")
    h["reconciled"] = True
h = row("Check: E1d k = 1 slice at dx = 0.05 vs dx = 0.1")
h["verdict"] = "CHECK PASSED"
h["reconciled"] = True

# lowest producing energies: family-specific upper bounds on the onset (major issue 4)
for q in ("E1d lowest producing energy reproduced at dx=0.05", "E1d lowest producing energy, all Gaussian runs (dx=0.1)"):
    add_note(row(q), "an upper bound on the classical onset within this family only; over all initial data the infimum "
                     "is 2M (time-reversed captures, see the section 2 row)", "upper bound on the classical onset")

# slices: counts are illustrative (minor issue 2)
for q in ("E1d slice e1d_sliceAk_16.0.json", "E1d slice e1d_sliceAs_1.0.json", "E1d producing regions (coarse 3D grid)"):
    h = row(q)
    add_note(h, "region, hole and switch counts are illustrative, not converged (they change with dx and between codes, "
                "e.g. sigma = 16, k = 2 line: 17 switches here, 9 in the cross-check); robust: non-monotonic lines with "
                "the same onset A in both codes, and the production fractions", "illustrative")
    h["reconciled"] = True


# speed and width (major issue 3)
def lg(form, lab, model, var):
    co = cf[form]["logit"][lab][model][var]
    return round(co["coef"], 2), round(co["z"], 1)


dec = sp["decision"]
spb, spo = sp["baseline_dx0.1"], sp["oneway_dx0.1"]
speed_verdict = {"not a speed effect": "REFUTED", "speed effect": "CONFIRMED"}.get(dec["all"], "OPEN")
speed_verdict_c = {"not a speed effect": "REFUTED", "speed effect": "CONFIRMED"}.get(dec["non_self_folding_packets"],
                                                                                    "OPEN")
if speed_verdict == speed_verdict_c:
    speed_final = speed_verdict
elif "CONFIRMED" in (speed_verdict, speed_verdict_c) and "REFUTED" in (speed_verdict, speed_verdict_c):
    speed_final = "OPEN"
else:
    speed_final = "REFUTED" if "REFUTED" in (speed_verdict, speed_verdict_c) and "CONFIRMED" not in (
        speed_verdict, speed_verdict_c) else "OPEN"


def ci(r):
    return f"{r['vg_coef']:+.2f} [{r['vg_ci95'][0]:+.2f}, {r['vg_ci95'][1]:+.2f}]"


speed_txt = (f"6 A x 3 sigma x 9 k x 8 collision phases, both phi_t forms: "
             f"logistic v_g coefficient with one intercept per (A, sigma), 95% CI, positive = faster produces more: "
             f"all production {ci(spb['all'])} baseline, {ci(spo['all'])} one-way; packets that do not self-fold "
             f"{ci(spb['non_self_folding_packets'])} / {ci(spo['non_self_folding_packets'])}; pre-set rule: a speed "
             f"effect would need CI < 0 in both forms, 'not a speed effect' if both CIs exclude -1.19 (half the "
             f"matched-energy coefficient -2.38); outcome: all production '{dec['all']}', non-self-folding "
             f"'{dec['non_self_folding_packets']}'")
conf_txt = ("the matched-energy correlation reproduces (also in the cross-check), but at matched energy a slow packet is "
            "taller (band [2,4): mean A 0.85-0.90 at v_g <= 0.33 vs 0.36 at v_g = 0.90) or wider; on the stored coarse "
            "grid, P ~ log A + log sigma + v_g gives v_g (coef, z) = "
            f"{lg('baseline', 'all', 'P~logA+logsigma+vg', 'vg')} baseline, {lg('oneway', 'all', 'P~logA+logsigma+vg', 'vg')} "
            f"one-way; collision-needed {lg('baseline', 'collision_needed', 'P~logA+logsigma+vg', 'vg')} / "
            f"{lg('oneway', 'collision_needed', 'P~logA+logsigma+vg', 'vg')} (e1d_confound.json)")
for q in ("E1d prediction test: speed", "E1d prediction test: speed_collision_needed"):
    h = row(q)
    h["verdict"] = speed_final
    h["note"] = ("RECONCILED (cross-check M3 upheld): this row's matched-energy test passes as computed, but the verdict "
                 "is on the PLAN prediction 'production favours low speed', and the correlation is not a speed effect: "
                 + conf_txt + "; fixed-shape test (e1d_speedtest.py): " + speed_txt)
    h["reconciled"] = True
st = {f: {k: {kk: cf[f]["stratified_tests"][k][kk] for kk in ("n_informative_strata", "mean_vg_shift_of_producers",
                                                              "p_two_sided", "p_slower_produces_more")}
          for k in ("all__fixed_A", "all__fixed_A_sigma", "collision_needed__fixed_A", "collision_needed__fixed_A_sigma")}
      for f in ("baseline", "oneway")}
upsert("E1d speed dependence at fixed amplitude, stored coarse grid (reconciliation)",
       value={"stratified_permutation_tests": st,
              "logit_vg_(coef,z)_given_logA_logsigma": {f: {lab: lg(f, lab, "P~logA+logsigma+vg", "vg")
                                                            for lab in ("all", "collision_needed")}
                                                        for f in ("baseline", "oneway")},
              "logit_vg_(coef,z)_given_logA_logE": {f: {lab: lg(f, lab, "P~logA+logE+vg", "vg")
                                                        for lab in ("all", "collision_needed")}
                                                    for f in ("baseline", "oneway")},
              "deviance_(A,sigma,vg)_vs_(A,E,vg)": {f: [round(cf[f]["logit"]["all"]["P~logA+logsigma+vg"]["deviance"]["coef"], 1),
                                                        round(cf[f]["logit"]["all"]["P~logA+logE+vg"]["deviance"]["coef"], 1)]
                                                    for f in ("baseline", "oneway")}},
       units_convention="coarse grid, runs with E > 2M; strata = fixed A or fixed (A, sigma); 20000 within-stratum "
                        "permutations; mean_vg_shift < 0 means producers are slower than their stratum",
       target="slower produces more (PLAN E1d)", tolerance="p < 0.05",
       verdict=speed_final, source="e1d_confound.py",
       note="no slow preference once amplitude (and width) are fixed; the one nominally significant stratified result "
            "(baseline, fixed (A, sigma), p2 = 0.03) has faster packets producing more. At fixed (A, E) slower packets do "
            "produce more, but there a slower packet is wider, and the (A, sigma, v_g) description fits better than "
            "(A, E, v_g) (lower deviance, same parameter count)",
       reconciled=True)
upsert("E1d speed dependence at fixed packet shape, phase-averaged (decisive test, reconciliation)",
       value={f: {lab: {kk: sp[f][lab][kk] for kk in ("n_informative_shapes", "n_runs_informative", "n_producing",
                                                       "vg_coef", "vg_se", "vg_ci95", "p_wald", "perm_p_two_sided",
                                                       "perm_p_slower_produces_more", "P_vs_vg_pooled")}
                  for lab in ("all", "non_self_folding_packets") if sp[f][lab].get("n_informative_shapes")}
              for f in ("baseline_dx0.1", "oneway_dx0.1", "baseline_dx0.05") if f in sp},
       units_convention="production probability over 8 collision phases; logistic slope on v_g with one intercept per "
                        "(A, sigma); positive = faster produces more",
       target="slower produces more (PLAN E1d)", tolerance="pre-set decision rule (e1d_speedtest.py docstring)",
       verdict=speed_final, source="e1d_speedtest.py, e1d_speedtest.json",
       note="fixed-shape test (e1d_speedtest.py): " + speed_txt + (f"; resolution check (baseline, sigma = 4, dx 0.1 vs 0.05): "
                         f"{sp.get('resolution_check_sigma4_baseline')}"),
       reconciled=True)
width_txt = (f"at matched energy no width preference in any band or form (cross-check FD6 -0.31, +0.12, "
             f"+0.41, all p > 0.2); at fixed amplitude wider packets produce more (stored grid, P ~ log A + log sigma: "
             f"log sigma z = {lg('baseline', 'all', 'P~logA+logsigma', 'logsigma')[1]} all production, "
             f"{lg('baseline', 'collision_needed', 'P~logA+logsigma', 'logsigma')[1]} collision-needed), because at fixed "
             f"A a wider packet carries more energy and more of it exceeds the self-folding threshold")
for q in ("E1d prediction test: width", "E1d prediction test: width_collision_needed"):
    h = row(q)
    h["verdict"] = "AMENDED"
    h["note"] = ("RECONCILED: verdict word on the PLAN prediction 'production favours wide packets' (was NOT_SUPPORTED, "
                 "not a PLAN word): " + width_txt)
    h["reconciled"] = True

h = row("E1d single_packet_controls")
h["note"] = ("self-folding threshold matches a local over-barrier estimate: the trough phi = -1 - A has "
             "V = (A(2+A))^2/4 > V(0) = 1/4 when A > sqrt2 - 1 = 0.414, so the trough can swing over the barrier "
             "(observed minimum A 0.375-0.425; the packet's kinetic energy lowers it). Self-folding gives 65% of coarse "
             "production and all production above ~4 x 2M that is not collision-needed; below 4 x 2M every producing "
             "run is collision-needed")
h["reconciled"] = True

# ================================================================== E1e
chk = {(r["omega"], r["v"]): r for r in c["dsv_producers_resolution_check"]}
e1e_dsv = c.get("e1e_dsv_lowest_converged")
r62 = chk.get((0.95, 0.62), {})
for q in ("E1e DSV trains, min_E_reproduced_dx0.05", "E1e DSV trains, min_N_lin_reproduced_dx0.05"):
    h = row(q)
    h["verdict"] = "OPEN"
    h["note"] = ("RECONCILED, superseded: (0.95, 0.62) is not a converged producer. Fourth-order time stepping gives a pair "
                 f"at dx = 0.05 (since t = {r62.get('y4_dx0.05_dt0.02', [None, None])[1]}) but none at dx = 0.025, "
                 f"dt = 0.01; phi(0,t) of the two separate at t = {r62.get('t_diverge_phi0')}, before the pair forms. "
                 "See 'E1e DSV trains, lowest converged producer'.")
    h["reconciled"] = True
n_conv = sum(1 for r in c["dsv_producers_resolution_check"] if r.get("converged_producer"))
n_chk = sum(1 for r in c["dsv_producers_resolution_check"] if r.get("y4_dx0.025_dt0.01") is not None)
if e1e_dsv:
    upsert("E1e DSV trains, lowest converged producer (reconciliation)",
           value={k: e1e_dsv[k] for k in ("omega", "v", "E_over_2M", "N_E_times_lambda_over_m2",
                                          "N_lin_times_lambda_over_m2")},
           units_convention="N*lambda/m^2; phi0^2 = m^2/(2 lambda); N_lin from the dx = 0.1 initial data as in e1e_quanta.py",
           target="N ~ 1/lambda (scaling)", tolerance="none", verdict="QUANTIFIED",
           source="e1c_reconcile.py, e1c_reconcile_analysis.py",
           note=(f"{e1e_dsv['criterion']}; the 14 lowest-energy producers of the original map were checked in order of E, "
                 f"{n_chk} reached the dx = 0.025 check and {n_conv} passed; upper bound within the DSV family"),
           reconciled=True)
h = row("E1e smallest classical N_lin*lambda/m^2 (producers reproduced at dx=0.05)")
add_note(h, "RECONCILED: value unchanged (set by the Gaussian packet A=0.8, sigma=2, k=0.5, reproduced at dx = 0.05 and "
            "0.025 here and in two independent codes); the DSV candidate in this note (3.93) is superseded by the converged "
            "DSV producer row (N_lin*lambda/m^2 = %.2f)" % (e1e_dsv["N_lin_times_lambda_over_m2"] if e1e_dsv else float("nan")),
         "RECONCILED: value unchanged")
h["reconciled"] = True
add_note(row("E1e threshold 2M_kink in quanta"), "approached (not attained) by finely tuned time-reversed captures "
                                                  "(section 2 row); simple families need 1.24 or more", "approached")

# ================================================================== section 2: time reversal (major issue 4)
cs = tr["cases"]
upsert("Seed section 2: pair-free data producing a pair at E -> 2M (time reversal; reconciliation)",
       value=[{"v": x["v"], "Tf": x["Tf"], "E_over_2M": x["reversed_data"]["E_over_2M"],
               "max_phi_initial": x["reversed_data"]["max_phi"],
               "energy_fraction_in_|x|<50": x["reversed_data"]["energy_within_|x|<50_over_2M"] /
               x["reversed_data"]["E_over_2M"],
               "pair_after_reversal_dt_dt/2_dt/4": [r["n_pairs_end"] for r in x["reverse_evolution"]],
               "fine_tuning_probes": [[p["probe"], p["n_pairs_end"]] for p in x["fine_tuning_probes"]]} for x in cs],
       units_convention="kk_initial(v, x0=10) evolved to Tf (bound state no longer reaches phi = 0 for 100 time units), "
                        "velocities reversed, evolved Tf again; no absorbing layer; dx = 0.1, dt = 0.04",
       target="classical infimum of the production energy = 2M (time-reversal argument; DSV 2008 p. 1)",
       tolerance="qualitative", verdict="CONFIRMED", source="e1_timereversal.py",
       note="initial data with phi < 0 everywhere (no kink: a decayed bion holding ~70% of the energy plus inward "
            "radiation) and E = 1.0012-1.005 x 2M make an outgoing pair under the exact inverse of the forward lattice "
            "map (same dt); with dt/2 or dt/4, with the far radiation truncated, or with noise of amplitude 1e-8 added "
            "in |x| < 50, no pair forms. Existence follows from time-reversal invariance of the field equation (the "
            "lattice run demonstrates it for the discrete map); the probes show the data are tuned beyond 1e-8, i.e. "
            "production near 2M is non-generic. Simple packet families start producing far above 2M",
       reconciled=True)

R["reconciliation"] = {
    "date": "2026-10-19",
    "files": ["e1c_reconcile.py", "e1c_reconcile.jsonl", "e1c_reconcile_analysis.py", "e1c_reconcile_analysis.json",
              "dsv_fig2_reading.json", "fig_e1c_reconcile.png", "e1c_example_y4.py", "e1c_example_y4.npz",
              "fig_e1c_example_y4.png", "e1d_confound.py", "e1d_confound.json",
              "e1d_speedtest.py", "e1d_speedtest.jsonl", "e1d_speedtest.json", "e1_timereversal.py",
              "e1_timereversal.json", "reconcile_results.py"],
    "summary": ("E1c example point (0.99, 0.43): CALIBRATED -> OPEN (chaotic: a pair only at the finest of five "
                "fourth-order settings and at 4 of 11 leapfrog settings, decided after the runs' trajectories separate; "
                f"0 of 11 neighbouring initial data produce; omega = 0.99 production converged at v = {conv_prod_99}). Hole (0.91, 0.82): "
                f"{row('E1c holes, e.g. near (0.91,0.82)')['verdict']} after a fourth-order check. Seed section 4 DSV "
                "claim CONFIRMED -> AMENDED. PLAN E1d speed preference: CONFIRMED -> "
                f"{speed_final} (amplitude/width confound; decisive fixed-shape test). Width: NOT_SUPPORTED -> AMENDED "
                "(holds at fixed amplitude, not at matched energy). Seed section 2: AMENDED -> CONFIRMED (infimum 2M by "
                "time reversal, demonstrated on the lattice; family onsets are upper bounds). Sanity-check verdict word "
                "CALIBRATED -> CHECK PASSED. Slice counts marked illustrative. v_c offset attributed to the target. Found "
                "during reconciliation: the E1e DSV producer (0.95, 0.62) is not converged; replaced by the lowest "
                "converged DSV producer."),
    "speed_verdicts": {"all_production": speed_verdict, "non_self_folding_packets": speed_verdict_c,
                       "final": speed_final}}
for f in ("e1c_reconcile_analysis.json", "e1d_confound.json", "e1d_speedtest.json", "e1_timereversal.json"):
    if f not in R["details_files"]:
        R["details_files"].append(f)

# ================================================================== seed claims
SC = json.load(open("seed_claims.json"))


def claim(text_prefix):
    for s in SC:
        if s["claim"].startswith(text_prefix):
            return s
    raise KeyError(text_prefix)


x05 = [x for x in cs if x["v"] == 0.05][0]
s = claim("A fold appears only with an antifold")
s["verdict"] = "CONFIRMED"
s["evidence"] = (
    "Floor: no producing run below 2M_kink in any Gaussian run (19,526: pair and single packet, both phi_t forms, all "
    "resolutions) or DSV run, in the original and in both independent codes; every production event is a kink-antikink "
    "pair. Infimum: 2M is also the classical infimum over all initial data. Reversing a slow captured kink-antikink pair "
    f"gives kink-free data (phi < 0 everywhere) with E = {x05['reversed_data']['E_over_2M']:.4f} x 2M that make an outgoing "
    f"pair (v = {x05['v']}; e1_timereversal.json; DSV 2008 p. 1 describe the same construction), and E -> 2M as v -> 0. "
    "Such data are extremely finely tuned: in the lattice demonstration the pair re-forms only under the exact inverse of "
    "the forward map, and noise of amplitude 1e-8, a halved time step or truncating the far radiation each destroy it. "
    "Onset in the scanned families: simple packets start producing well above 2M (lowest resolution-checked producers "
    f"1.86 x 2M for narrow-band packets, 2.70 x 2M for exact one-way packets, "
    f"{e1e_dsv['E_over_2M']:.2f} x 2M for DSV trains); these are family-specific upper bounds on where production starts, "
    "not a property of classical fields in general. (Reconciled: was AMENDED on the rationale that a classical field "
    "always needs extra energy; that holds only for the scanned families.)")
s = claim("Colliding trains of small pulses")
s["verdict"] = "AMENDED"
s["evidence"] = (
    "Over a wide range of settings: yes. E1c reproduces DSV Fig. 2's producing band and its trend (producing v falls from "
    f"~0.73-0.85 at omega = 0.90 to {conv_prod_99} at omega = 0.99; Spearman {rho_c[0]:.2f}, cross-check -0.94), "
    "pass-through at high v, the hole at (0.91, 0.82) and no production above omega = 0.99. Point by point the original "
    f"map hits {m['hits']} of DSV's {m['n_dsv_producing']} producing points with {m['false_positives']} false positives "
    f"({m['ours_within_0.01_of_dsv']} of our {m['n_ours_producing']} producers lie within 0.01 of a DSV point). 'Most easily "
    "at low speed' is not what DSV report or what E1c shows: at each omega production is confined to a velocity band "
    "with none below it (omega = 0.90: nothing for v < 0.73), slower bands belong to weaker pulses and do not cost less "
    "energy (the lowest-energy converged producers sit at v = 0.59-0.79, E ~ 7.8-8.2 x 2M; the omega = 0.99 producer at "
    "v = 0.41 has E = 12.3 x 2M). What holds is DSV's own statement: weaker pulses (higher omega) need lower speed, and "
    "too-fast trains pass through. DSV's example point (0.99, 0.43) is OPEN: its call is chaotic (a late pair at the "
    "finest of five fourth-order settings and at 4 of 11 leapfrog settings; 0 of 11 neighbouring initial "
    "data); production at omega = 0.99 is converged at v = 0.41.")
s = claim("The pair-production boundary")
s["evidence"] = (
    "Robust statements: in both 59 x 57 slices most lines of fixed k or sigma switch between producing and not more than "
    "once as A rises (57/57 and 48/53), so there is no single threshold; this holds for collision-needed production alone, "
    "at half the grid spacing and time step (k = 1 slice: 49/53), and in the independent code (sigma = 16 lines: same "
    "onset A = 0.375 and the same gap at A = 0.45-0.5). The call at a point depends on the collision phase (51 of 60 "
    "boundary points flip under a shift of x0 within one carrier period) and, for ~20% of points, on the resolution down "
    "to dx = 0.0125; production fractions are stable (4x4-block fractions correlate 0.95 between dx = 0.1 and 0.05). "
    "Region, hole and switch counts (e.g. 24 and 48 producing regions, 267 and 141 enclosed holes at dx = 0.1) are "
    "illustrative and not converged.")
# split the PLAN E1d prediction into its speed and width parts
old = [x for x in SC if x["claim"].startswith("Production favours low speed and wide packets")]
if old:
    i = SC.index(old[0])
    sec = old[0]["seed_section"]
    SC[i:i + 1] = [{"seed_section": sec, "claim": "Production favours low speed.", "verdict": "", "evidence": ""},
                   {"seed_section": sec, "claim": "Production favours wide packets.", "verdict": "", "evidence": ""}]
s = claim("Production favours low speed")
s["verdict"] = speed_final
s["evidence"] = (
    "Not as a speed effect. At matched energy slower packets do produce more (Spearman -0.82, -0.87, -0.88 baseline; "
    "-0.78 to -0.88 one-way; reproduced by the cross-check), but only because a slow packet of the same energy is taller "
    "or wider, and amplitude controls production. Decisive test at fixed packet shape (A, sigma), with production "
    "averaged over 8 collision phases (e1d_speedtest.py): " + speed_txt + ". At fixed shape faster packets produce as "
    "much or more (a faster packet of the same shape carries more energy). The stored coarse grid agrees "
    f"(v_g z = {lg('baseline', 'all', 'P~logA+logsigma+vg', 'vg')[1]} baseline, "
    f"{lg('oneway', 'all', 'P~logA+logsigma+vg', 'vg')[1]} one-way given log A and log sigma; collision-needed "
    f"{lg('baseline', 'collision_needed', 'P~logA+logsigma+vg', 'vg')[1]} / "
    f"{lg('oneway', 'collision_needed', 'P~logA+logsigma+vg', 'vg')[1]}). (Reconciled: was 'low speed holds', AMENDED; "
    "that did not separate speed from amplitude.)")
s = claim("Production favours wide packets")
s["verdict"] = "AMENDED"
s["evidence"] = ("Holds only at fixed amplitude: " + width_txt + ". Wide packets do not win at matched energy.")
s = claim("A classical pair needs")
dsv_txt = (f"DSV trains: the lowest converged producer is ({e1e_dsv['omega']}, {e1e_dsv['v']}), E = "
           f"{e1e_dsv['E_over_2M']:.2f} x 2M, N*lambda/m^2 = {e1e_dsv['N_E_times_lambda_over_m2']:.2f} (N = E/m) or "
           f"{e1e_dsv['N_lin_times_lambda_over_m2']:.2f} (N_lin); the earlier DSV value 4.78 / 3.93 at (0.95, 0.62) is "
           "withdrawn (that train produces at dx = 0.05 but not at dx = 0.025 with fourth-order time stepping)")
s["evidence"] = (
    "Classical dynamics is independent of phi0 (S = phi0^2 S~), so N = E/(hbar m) = (E~/(2 sqrt2)) m^2/lambda. Energy "
    "conservation alone gives N >= (2/3) m^2/lambda. The smallest producing initial states that survive resolution "
    "checks: narrow-band Gaussian packets (A=0.8, sigma=2, k=0.5; E = 1.86 x 2M) N*lambda/m^2 = 1.24 (N = E/m) or 1.69 "
    "(free-field occupation N_lin), reproduced at dx = 0.05 and 0.025 and in two independent codes; exact one-way "
    "packets (A=0.6, sigma=4, k=0.5; E = 2.70 x 2M) 1.80 or 1.96. " + dsv_txt + ". So classical pair-making from these "
    "families needs N ~ (1.2-2) m^2/lambda quanta (Gaussian packets): about 120-200 at lambda/m^2 = 0.01. These are "
    "upper bounds on the classical minimum over the scanned families; over all initial data the bound is the energy "
    "floor 2/3, approached only by finely tuned data (section 2).")
s = claim("Pile in enough energy")
if "sqrt2 - 1" not in s["evidence"]:
    s["evidence"] += (" Mechanism of self-folding: the trough phi = -1 - A has potential energy above the barrier "
                      "V(0) = 1/4 when A > sqrt2 - 1 = 0.414, so it can swing over the barrier on its own (observed "
                      "minimum A 0.375-0.425; the packet's kinetic energy lowers it).")
json.dump(SC, open("seed_claims.json", "w"), indent=1, ensure_ascii=False)
R["seed_claims"] = SC
json.dump(R, open("results.json", "w"), indent=1, default=float)
for h in H:
    if h.get("reconciled"):
        print(f"{h['verdict']:13s} {h['quantity']}")
for s in SC:
    print(f"{s['verdict']:11s} {s['seed_section']}: {s['claim'][:70]}")
