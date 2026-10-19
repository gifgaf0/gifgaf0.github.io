"""Apply the E1 reconciliation (after the independent cross-check) to results.json and seed_claims.json.

Run after collect_results.py. Idempotent: it overwrites the fields it owns and adds or replaces
rows by their quantity name. Inputs: results.json, e1c_reconcile_analysis.json, e1d_confound.json,
e1_timereversal.json, e1_extra_analysis.json, e1e_results.json.
"""
import json
import numpy as np

R = json.load(open("results.json"))
c = json.load(open("e1c_reconcile_analysis.json"))
cf = json.load(open("e1d_confound.json"))
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


# ------------------------------------------------------------------ E1b: offset diagnosis
for q in ("E1b critical velocity v_c (dx->0 extrapolation)", "E1b critical velocity v_c (baseline dx=0.05, x0=12)"):
    h = row(q)
    if "offset diagnosis" not in h["note"]:
        h["note"] += ("; offset diagnosis (reconciliation): the independent Fourier + RK4 cross-check (other x0, box and "
                      "integrator) gives 0.260066, within 1e-5 of ours, so the +2.6e-4 offset from 0.2598 lies in the "
                      "[summary] target, not in either computation")

# ------------------------------------------------------------------ E1c: example point
p41, p43 = c["point_0.41"], c["point_0.43"]
div43 = c["phi0_divergence_from_finest_y4"]["0.43"]["vs_reference"]
t_div_y4 = [d["t_diverge_phi0_gt_0.1"] for d in div43 if d["scheme"] == "y4" and d["t_diverge_phi0_gt_0.1"]]
lf43 = p43["lf_calls"]
h = row("E1c (omega,v)=(0.99,0.43) produces a pair")
h.update({
    "value": {"fourth_order_y4_calls_(dx,dt,pair_at_T,since)": p43["y4_calls"],
              "original_leapfrog_calls_(dx,dt,pair_at_T,since)": lf43,
              "trajectory_divergence_time_between_y4_resolutions": t_div_y4},
    "units_convention": "DSV criterion: pair present at t=T (one light-crossing time); evolved to 1.5T",
    "verdict": "OPEN",
    "note": ("RECONCILED: not a converged producer. Fourth-order time stepping (e1c_reconcile.py) gives no pair up to 1.5T at "
             "every (dx, dt) tried; the original leapfrog gives a pair at some (dx, dt) and not others (here and in the "
             "cross-check: 4 of 10 settings, forming at t = 780-1160). phi(0,t) of the two finest y4 runs separate after "
             f"t ~ {min(t_div_y4) if t_div_y4 else 'n/a'}: the long-lived central oscillation is sensitive, so no affordable "
             "resolution settles whether a pair leaves it later. The converged evolution (t < ~750) has no pair. The "
             "original 'pair since t=1160, still separating at 1.5T' came from one unconverged discretisation "
             "(dx = 0.1, dt = 0.04, whose phi(0,t) leaves the converged one at t ~ 258). See the omega = 0.99 column row."),
    "reconciled": True})
col = c["omega_0.99_column_y4_dx0.05_dt0.02"]
upsert("E1c omega = 0.99 column with fourth-order time stepping (reconciliation)",
       value={"producing_v": [float(v) for v, r in col.items() if r["pair_at_T"]], "v_scanned": [float(v) for v in col],
              "point_0.41_y4_calls_(dx,dt,pair_at_T,since)": p41["y4_calls"],
              "point_0.41_leapfrog_calls_(dx,dt,pair_at_T,since)": p41["lf_calls"]},
       units_convention="DSV criterion; y4 = Yoshida 4th-order composition of the original velocity-Verlet step, "
                        "dx = 0.05, dt = 0.02 for the scan",
       target="DSV Fig. 2: omega = 0.99 produces at v = 0.43 only (read)", tolerance="qualitative",
       verdict="NO_TARGET", source="e1c_reconcile.py, e1c_reconcile_analysis.json",
       note="converged producer at v = 0.41 (pair from t = 590 at every y4 resolution and in the leapfrog as dt -> 0); "
            "DSV's omega = 0.99 production near v ~ 0.4 is reproduced, 0.02 below their example point",
       reconciled=True)
m = c["map_vs_dsv_fig2"]
upsert("E1c map vs DSV Fig. 2, point by point (reconciliation)",
       value={k: m[k] for k in ("n_dsv_producing", "n_ours_producing", "hits", "false_positives", "missed", "jaccard",
                                 "ours_within_0.01_of_dsv")},
       units_convention="omega 0.90-0.99 x v 0.40-0.90 (step 0.01); original map dx = 0.1, dt = 0.04; DSV Fig. 2 "
                        "digitized (dsv_fig2_reading.json)",
       target="none", tolerance="none", verdict="NO_TARGET", source="e1c_reconcile_analysis.py",
       note="band locations agree; individual points do not (point calls are not converged at dx = 0.1)",
       reconciled=True)
h = row("E1c dx check (dx 0.05 vs 0.1)")
h["note"] = ("agreement is trivial in the omega = 0.99 column: its dx = 0.1 producers (v = 0.41, 0.43) are not on the "
             "dx = 0.05 grid (step 0.02), which has no omega = 0.99 producer; the example point was not in this check")
h["reconciled"] = True

# ------------------------------------------------------------------ E1d: verdict word for the sanity check
for q in ("E1d no production below E = 2 M_kink",
          "E1d no production below E = 2 M_kink, every Gaussian run (pair and single packet, all variants)"):
    h = row(q)
    h["verdict"] = "CONFIRMED" if h["value"] == 0 else "REFUTED"
    if "not a literature calibration" not in h["note"]:
        h["note"] += "; verdict word CONFIRMED (a prediction check, not a literature calibration)"
    h["reconciled"] = True

# slices: counts are illustrative
for q in ("E1d slice e1d_sliceAk_16.0.json", "E1d slice e1d_sliceAs_1.0.json", "E1d producing regions (coarse 3D grid)"):
    h = row(q)
    if "illustrative" not in h["note"]:
        h["note"] += ("; region, hole and switch counts are illustrative, not converged (they change with dx and between "
                      "codes, e.g. sigma = 16, k = 2 line: 17 switches here, 9 in the cross-check); robust: non-monotonic "
                      "lines with the same onset in both codes")
    h["reconciled"] = True

# speed tests: amplitude confound
b, o = cf["baseline"], cf["oneway"]


def lg(form, lab, model, var):
    return round(cf[form]["logit"][lab][model][var]["coef"], 3), round(cf[form]["logit"][lab][model][var]["z"], 2)


conf_note = ("RECONCILED: the matched-energy correlation reproduces (also in the cross-check) but it is an amplitude effect: "
             "at matched energy slow packets carry larger A (band [2,4): mean A 0.85-0.90 at v_g <= 0.33 vs 0.36 at "
             "v_g = 0.90). At fixed (A, sigma) speed has no significant effect: logistic P ~ log A + log sigma + v_g gives "
             f"v_g coefficient (coef, z) = {lg('baseline', 'all', 'P~logA+logsigma+vg', 'vg')} baseline, "
             f"{lg('oneway', 'all', 'P~logA+logsigma+vg', 'vg')} one-way (positive = faster produces more); collision-needed "
             f"{lg('baseline', 'collision_needed', 'P~logA+logsigma+vg', 'vg')} / "
             f"{lg('oneway', 'collision_needed', 'P~logA+logsigma+vg', 'vg')}. See e1d_confound.json.")
for q in ("E1d prediction test: speed", "E1d prediction test: speed_collision_needed"):
    h = row(q)
    h["verdict"] = "AMENDED"
    h["note"] = conf_note
    h["reconciled"] = True
st = {f: {k: {kk: cf[f]["stratified_tests"][k][kk] for kk in ("n_informative_strata", "mean_vg_shift_of_producers",
                                                              "p_two_sided", "p_slower_produces_more")}
          for k in ("all__fixed_A", "all__fixed_A_sigma", "collision_needed__fixed_A", "collision_needed__fixed_A_sigma")}
      for f in ("baseline", "oneway")}
upsert("E1d speed dependence at fixed amplitude (reconciliation)",
       value={"stratified_permutation_tests": st,
              "logit_vg_coef_z": {f: {lab: lg(f, lab, "P~logA+logsigma+vg", "vg") for lab in ("all", "collision_needed")}
                                  for f in ("baseline", "oneway")},
              "deviance_drop_adding_vg_to_logA_logsigma": {
                  f: {lab: round(cf[f]["logit"][lab]["P~logA+logsigma"]["deviance"]["coef"]
                                 - cf[f]["logit"][lab]["P~logA+logsigma+vg"]["deviance"]["coef"], 2)
                      for lab in ("all", "collision_needed")} for f in ("baseline", "oneway")}},
       units_convention="coarse grid, runs with E > 2M; strata = fixed A or fixed (A, sigma); 20000 within-stratum "
                        "permutations; mean_vg_shift < 0 means producers are slower than their stratum",
       target="slower produces more (PLAN E1d)", tolerance="p < 0.05",
       verdict="NOT_SUPPORTED", source="e1d_confound.py",
       note="no speed preference once amplitude (and width) are fixed; the one nominally significant stratified result "
            "(baseline, fixed (A, sigma), p2 = 0.03) has faster packets producing more",
       reconciled=True)
h = row("E1d single_packet_controls")
h["note"] = ("self-folding threshold matches a local over-barrier estimate: the trough phi = -1 - A has V > V(0) = 1/4 when "
             "A > sqrt2 - 1 = 0.414 (observed minimum A 0.375-0.425; the packet's kinetic energy lowers it)")
h["reconciled"] = True

# ------------------------------------------------------------------ E1e: DSV producer resolution check
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
if "RECONCILED" not in h["note"]:
    h["note"] = ("RECONCILED: value unchanged (set by the Gaussian packet A=0.8, sigma=2, k=0.5, reproduced at dx = 0.05 and "
                 "0.025 here and in two independent codes); the DSV candidate listed in the note is superseded by the "
                 "converged DSV producer row. " + h["note"])
h["reconciled"] = True

# ------------------------------------------------------------------ section 2: time reversal
cs = tr["cases"]
upsert("Seed section 2: pair-free data producing a pair at E -> 2M (time reversal; reconciliation)",
       value=[{"v": x["v"], "Tf": x["Tf"], "E_over_2M": x["reversed_data"]["E_over_2M"],
               "max_phi_initial": x["reversed_data"]["max_phi"],
               "pair_after_reversal_dt_dt/2_dt/4": [r["n_pairs_end"] for r in x["reverse_evolution"]],
               "fine_tuning_probes": [[p["probe"], p["n_pairs_end"]] for p in x["fine_tuning_probes"]]} for x in cs],
       units_convention="kk_initial(v, x0=10) evolved to Tf (bound state no longer reaches phi = 0 for 100 time units), "
                        "velocities reversed, evolved Tf again; no absorbing layer; dx = 0.1",
       target="classical infimum of the production energy = 2M (time-reversal argument; DSV 2008 p. 1)",
       tolerance="qualitative", verdict="CONFIRMED", source="e1_timereversal.py",
       note="initial data with phi < 0 everywhere (no kink) and E just above 2M make an outgoing pair when evolved with "
            "the exact inverse of the forward lattice map (same dt); with dt/2 or dt/4, with the far radiation truncated, "
            "or with noise of amplitude 1e-8 added in |x| < 50, no pair forms. Existence follows from time-reversal "
            "invariance of the equation; the demonstration shows the data are tuned beyond 1e-8, i.e. production near "
            "2M is non-generic. Simple packet families start producing far above 2M",
       reconciled=True)

R["reconciliation"] = {
    "date": "2026-10-19",
    "files": ["e1c_reconcile.py", "e1c_reconcile.jsonl", "e1c_reconcile_analysis.py", "e1c_reconcile_analysis.json",
              "dsv_fig2_reading.json", "fig_e1c_reconcile.png", "e1d_confound.py", "e1d_confound.json",
              "e1_timereversal.py", "e1_timereversal.json", "reconcile_results.py"],
    "summary": "E1c example point (0.99, 0.43) CALIBRATED -> OPEN (sensitive, unconverged); omega = 0.99 production "
               "reproduced at v = 0.41. Seed section 4 DSV claim CONFIRMED -> AMENDED. E1d speed preference is an "
               "amplitude effect (speed tests -> AMENDED; fixed-amplitude test NOT_SUPPORTED). Seed section 2 "
               "AMENDED -> CONFIRMED (infimum 2M by time reversal, demonstrated). Sanity check verdict word "
               "CALIBRATED -> CONFIRMED. Slice counts marked illustrative. v_c offset attributed to the target. Found during "
               "reconciliation: the E1e DSV producer (0.95, 0.62) is not converged (produces at dx = 0.05, not at "
               "dx = 0.025 with fourth-order time stepping); E1e DSV rows -> OPEN, replaced by the lowest converged "
               "DSV producer."}
for f in ("e1c_reconcile_analysis.json", "e1d_confound.json", "e1_timereversal.json"):
    if f not in R["details_files"]:
        R["details_files"].append(f)

# ------------------------------------------------------------------ seed claims
SC = json.load(open("seed_claims.json"))


def claim(sec_prefix, text_prefix):
    for s in SC:
        if s["seed_section"].startswith(sec_prefix) and s["claim"].startswith(text_prefix):
            return s
    raise KeyError(text_prefix)


x01 = cs[0]
s = claim("§2", "A fold appears only with an antifold")
s["verdict"] = "CONFIRMED"
s["evidence"] = (
    "No producing run below 2M_kink in any Gaussian run (19,526: pair and single packet, both phi_t forms, all "
    "resolutions) or DSV run, in both the original and the independent codes; every production event is a "
    "kink-antikink pair. 2M is also the classical infimum: reversing a slow captured kink-antikink pair gives "
    f"pair-free data (phi < 0 everywhere) with E = {x01['reversed_data']['E_over_2M']:.4f} x 2M that make an outgoing "
    f"pair (v = {x01['v']}; e1_timereversal.json; DSV 2008 p. 1 state the same construction). Such data are extremely "
    "finely tuned: in the lattice demonstration the pair re-forms only under the exact inverse of the forward map, and "
    "noise of amplitude 1e-8, a halved time step or truncating the far radiation each destroy it. "
    "Simple packet families start producing well above 2M: lowest resolution-checked producers 1.86 x 2M "
    "(narrow-band packets), 2.70 x 2M (exact one-way packets), 7.2 x 2M (DSV trains); these are family-specific upper "
    "bounds on the onset. (Reconciled: was AMENDED on the claim that a classical field always needs extra energy; that "
    "holds only for the scanned families.)")
s = claim("§4", "Colliding trains of small pulses")
s["verdict"] = "AMENDED"
s["evidence"] = (
    "Over a wide range: yes. E1c reproduces DSV Fig. 2's band and its trend (producing v falls from ~0.73-0.85 at "
    "omega = 0.90 to ~0.41 at omega = 0.99; Spearman -0.99, cross-check -0.94), pass-through at high v, the hole at "
    "(0.91, 0.81-0.82) and no production above omega = 0.99; point by point it hits "
    f"{m['hits']} of DSV's {m['n_dsv_producing']} producing points with {m['false_positives']} false positives "
    f"({m['ours_within_0.01_of_dsv']} of our {m['n_ours_producing']} producers lie within 0.01 of a DSV point). "
    "'Most easily at low speed' is not what DSV report or what E1c shows: at each omega production is confined to a "
    "velocity band with none below it (omega = 0.90: nothing for v < 0.73), and the lowest-energy producers sit at "
    "v = 0.62-0.73 (E ~ 7 x 2M). What holds is DSV's statement that weaker pulses (higher omega) need lower speed and "
    "too-fast trains pass through. DSV's example point (0.99, 0.43) is OPEN (sensitive; no pair in converged "
    "fourth-order runs, a pair in some leapfrog runs); production at omega = 0.99 is converged at v = 0.41.")
s = claim("§4, §7.1", "The pair-production boundary")
s["evidence"] = (
    "Robust statements: in both slices most lines of fixed k or sigma switch between producing and not more than once "
    "as A rises (57/57 and 48/53), so there is no single threshold; this holds for collision-needed production alone, "
    "at half the grid spacing and time step (k = 1 slice), and in the independent code (sigma = 16, k = 1 line: 17 "
    "switches, onset A = 0.375 in both). The call at a point depends on the collision phase (51 of 60 boundary points "
    "flip under a shift of x0 within one carrier period) and, for ~20% of points, on the resolution down to "
    "dx = 0.0125; production fractions are stable (4x4-block fractions correlate 0.95 between dx = 0.1 and 0.05). "
    "Illustrative, unconverged counts: 24 and 48 producing regions, 267 and 141 enclosed holes (dx = 0.1).")
s = claim("PLAN E1d", "Production favours low speed and wide packets")
s["verdict"] = "AMENDED"
s["evidence"] = (
    "Neither speed nor width matters as such; amplitude controls production. At matched energy slower packets produce "
    "more (Spearman -0.82, -0.87, -0.88 baseline; -0.78 to -0.88 one-way; reproduced by the cross-check), but only "
    "because a slow packet of the same energy has a larger amplitude (band [2,4): mean A 0.85-0.90 at v_g <= 0.33 vs "
    "0.36 at v_g = 0.90). With A and sigma fixed, speed has no significant effect (logistic v_g coefficient "
    f"z = {lg('baseline', 'all', 'P~logA+logsigma+vg', 'vg')[1]} baseline, {lg('oneway', 'all', 'P~logA+logsigma+vg', 'vg')[1]} "
    f"one-way, positive = faster; collision-needed z = {lg('baseline', 'collision_needed', 'P~logA+logsigma+vg', 'vg')[1]} / "
    f"{lg('oneway', 'collision_needed', 'P~logA+logsigma+vg', 'vg')[1]}). Width: no preference at matched energy; at fixed A "
    "wider packets produce more because they carry more energy "
    f"(log sigma z = {lg('baseline', 'all', 'P~logA+logsigma+vg', 'logsigma')[1]}). (Reconciled: the earlier evidence "
    "'low speed: CONFIRMED' did not separate speed from amplitude.)")
s = claim("§8 / PLAN E1e", "A classical pair needs")
if e1e_dsv:
    dsv_txt = (f"DSV trains: the lowest converged producer is ({e1e_dsv['omega']}, {e1e_dsv['v']}), E = "
               f"{e1e_dsv['E_over_2M']:.2f} x 2M, N*lambda/m^2 = {e1e_dsv['N_E_times_lambda_over_m2']:.2f} (N = E/m) or "
               f"{e1e_dsv['N_lin_times_lambda_over_m2']:.2f} (N_lin); the earlier DSV value 4.78 / 3.93 at (0.95, 0.62) is "
               "withdrawn (that train produces at dx = 0.05 but not at dx = 0.025 with fourth-order time stepping)")
else:
    dsv_txt = ("DSV trains: no converged producer was found among the lowest-energy candidates checked; the earlier "
               "value 4.78 / 3.93 at (0.95, 0.62) is withdrawn (not converged)")
s["evidence"] = (
    "Classical dynamics is independent of phi0 (S = phi0^2 S~), so N = E/(hbar m) = (E~/(2 sqrt2)) m^2/lambda. Energy "
    "conservation alone gives N >= (2/3) m^2/lambda. The smallest producing initial states that survive resolution "
    "checks: narrow-band Gaussian packets (A=0.8, sigma=2, k=0.5; E = 1.86 x 2M) N*lambda/m^2 = 1.24 (N = E/m) or 1.69 "
    "(free-field occupation N_lin), reproduced at dx = 0.05 and 0.025 and in two independent codes; exact one-way "
    "packets (A=0.6, sigma=4, k=0.5; E = 2.70 x 2M) 1.80 or 1.96. " + dsv_txt + ". So classical pair-making from these "
    "families needs N ~ (1.2-2) m^2/lambda quanta: about 120-200 at lambda/m^2 = 0.01. These are upper bounds on the "
    "classical minimum over the scanned families; over all initial data the bound is the energy floor 2/3, reached only "
    "by finely tuned data (section 2).")
s = claim("§4", "Pile in enough energy")
if "sqrt2 - 1" not in s["evidence"]:
    s["evidence"] += (" The self-folding threshold matches a local over-barrier estimate: the trough phi = -1 - A has "
                      "potential energy above the barrier V(0) = 1/4 when A > sqrt2 - 1 = 0.414 (observed minimum A "
                      "0.375-0.425).")
json.dump(SC, open("seed_claims.json", "w"), indent=1, ensure_ascii=False)
R["seed_claims"] = SC
json.dump(R, open("results.json", "w"), indent=1, default=float)
for h in H:
    if h.get("reconciled"):
        print(f"{h['verdict']:13s} {h['quantity']}")
for s in SC:
    print(f"{s['verdict']:11s} {s['seed_section']}: {s['claim'][:70]}")
