#!/usr/bin/env python3
"""E7 second cross-check (x2): compare the original results.json with my x2_* recomputation
(and, where present, with the earlier cross-check's cc_* numbers), then write crosscheck.json.

Run after x2_hedgehog.py, x2_hopfion.py, x2_dl.py, x2_audit.py.  Prints the table.
"""
import json
import os

O = json.load(open("../results.json"))
D = O["details"]
H = json.load(open("x2_hedgehog.json"))
HP = json.load(open("x2_hopfion.json"))
DLx = json.load(open("x2_dl.json"))
A = json.load(open("x2_audit.json"))
CC = json.load(open("cc_audit.json")) if os.path.exists("cc_audit.json") else None
CCH = json.load(open("cc_hedgehog.json")) if os.path.exists("cc_hedgehog.json") else None

hd = {h["quantity"]: h for h in O["headline"]}
sk = D["skyrme"]
S = H["massless"]
rows = []


def add(name, orig, mine, tol_rel=1e-5, tol_abs=None, note="", prior=None):
    if orig is None or mine is None:
        agree = None
        rel = None
    else:
        rel = (mine - orig) / orig if orig != 0 else mine - orig
        if tol_abs is not None:
            agree = abs(mine - orig) <= tol_abs
        else:
            agree = abs(rel) <= tol_rel
    rows.append(dict(quantity=name, original=orig, recomputed=mine, prior_crosscheck=prior,
                     rel_diff=rel, tolerance=(f"abs {tol_abs}" if tol_abs is not None else f"rel {tol_rel:g}"),
                     agree=agree, note=note))


ccb = CCH["best"] if CCH and "best" in CCH else None
# --- hedgehog
add("a1 = M_cl/(F_pi/e)", hd["a1 = M_cl/(F_pi/e)"]["value"], S["a1"], 1e-8,
    note="own shooting+bisection vs original solve_bvp; PLAN target 36.4633 (0.2%) passes: -0.004%",
    prior=ccb and ccb.get("a1"))
add("Lambda", hd["Lambda (I1 = (2pi/3) Lambda/(e^3 F_pi))"]["value"], S["Lambda"], 1e-7,
    note="PLAN target 50.9 (0.5%) passes: +0.155%", prior=ccb and ccb.get("Lambda"))
add("virial E2/E4", hd["virial E2/E4"]["value"], S["virial_E2_over_E4"], 1e-8)
for k, ok in (("B", "xB"), ("M", "xM"), ("E", "xE"), ("half", "x_half")):
    add(f"radius a2 ({k})", sk["a2"][k], S[ok], 1e-7, prior=ccb and ccb.get(ok))
for k in ("B", "half", "E", "M"):
    add(f"c0 ({k})", sk["c0"][k], H["c0"][k], 1e-7)
add("tail coefficient C (F -> C/x^2)", O["hedgehog"]["convergence"][2]["C_tail"], S["C_tail"], 1e-6)
add("slope -F'(0)", O["hedgehog"]["convergence"][2]["slope0"], S["slope0"], 1e-8)
pr = sk["proton"]
an = A["anw"]
add("M_cl at ANW (MeV)", pr["M_classical_MeV"], an["M_cl"], 1e-8)
add("M_N model at ANW (MeV)", pr["M_N_model_MeV"], an["M_N"], 1e-8)
add("M_Delta model at ANW (MeV)", pr["M_Delta_model_MeV"], an["M_D"], 1e-8)
add("R_B at ANW (fm) [target 0.59 +- 0.01]", pr["R_B_fm"], an["R_B"], 1e-7)
add("R_M at ANW (fm) [target 0.92 +- 0.01]", pr["R_M_fm"], an["R_M"], 1e-7)
add("own fit F_pi (938.9, 1232) MeV", pr["own_fit_to_MN_MDelta"]["F_pi_MeV"], A["fit"]["F_pi"], 1e-7)
add("own fit e (938.9, 1232)", pr["own_fit_to_MN_MDelta"]["e"], A["fit"]["e"], 1e-7)
add("proton M R/hbar c (939 MeV x R_B)", pr["MR_nucleon_model"]["value"], an["MR_939"], 1e-7)
add("proton M R/hbar c classical (c0/e^2)", pr["MR_classical"]["value"], an["MR_classical"], 1e-7)
add("r_p/lambda_C (data)", pr["MR_data"]["value"], A["proton_data_rp_over_lambdaC"], 1e-7)
add("E_rot/M at ANW", pr["rotor_over_mass"]["value"], an["rot_over_M"], 1e-7)
fl = sk["semiclassical_floor"]
add("floor (MR)_min, E_rot <= M", fl["rot_over_M_le_1.0"]["MR_min_B"], A["floor"]["1.0"]["MR_min_B"], 1e-7,
    note="my route: root of E_rot(e) = M(e) in MeV, checked at two F_pi")
add("floor (MR)_min, E_rot <= 0.1 M", fl["rot_over_M_le_0.1"]["MR_min_B"], A["floor"]["0.1"]["MR_min_B"], 1e-7,
    note="= 2.3947; results.json note rounds it to 2.40, report text to 2.39")
add("e_max for E_rot <= M", fl["rot_over_M_le_1.0"]["e_max"], A["floor"]["1.0"]["e_max"], 1e-7)
el = sk["electron"]
for b in ("LEP", "SEED"):
    add(f"lambda_C/R ({b})", el[b]["compton_over_R_min"], A["electron"][b]["compton_over_R"], 1e-8)
    for k in ("B", "half", "M", "E"):
        add(f"e needed ({b}, {k})", el[b][k]["e_min"], A["electron"][b][k]["e_min"], 1e-7)
    add(f"F_pi needed ({b}, B) MeV", el[b]["B"]["F_pi_MeV"], A["electron"][b]["B"]["F_pi"], 1e-7)
    add(f"E_rot/M at electron fold ({b}, B)", el[b]["B"]["rot_over_M"], A["electron"][b]["B"]["rot_over_M"], 1e-7,
        note="mine from I1 and M in MeV at (e, F_pi), not the closed formula")
    add(f"e^2/16pi^2 at electron fold ({b}, B)", el[b]["B"]["naive_loop_parameter_e2_over_16pi2"],
        A["electron"][b]["B"]["e2_over_16pi2"], 1e-7)
add("floor / electron MR (LEP)", hd["electron needed (MR) / semiclassical floor"]["value"],
    A["electron"]["LEP"]["floor_over_MR"], 1e-7)
# pion-mass family
fam_o = {round(r["beta"], 4): r for r in sk["pion_mass_family"]["rows"]} if "pion_mass_family" in sk and "rows" in sk["pion_mass_family"] else None
if fam_o is None:
    # find the list in the details
    for v in sk.values():
        if isinstance(v, dict) and "c0_B_min" in v:
            fam_o = {round(r["beta"], 4): r for r in v.get("rows", v.get("family", []))}
for r in H["pion_mass_family"]:
    b = round(r["beta"], 4)
    o = fam_o.get(b) if fam_o else None
    add(f"c0_B(beta={b})", o and o["c0_B"], r["c0_B"], 1e-6)
    add(f"c0_half(beta={b})", o and o["c0_half"], r["c0_half"], 1e-6)
# --- hopfion
hop = D["hopfion"]
Ah = A["hopfion"]
add("hopfion E_W (ansatz)", hop["E_W_ansatz"], HP["E_W"], 1e-6,
    note="mine: direct 3D finite-difference evaluation; equals a1/(3 pi^2) = 1.2314457 (an identity)")
add("hopfion R_ring (Ward)", hop["R_ring_ward"], HP["R_ring"], 2e-5, note="mine: argmin n3 on the equator")
add("hopfion R_rms energy (Ward)", hop["R_rms_ward"], HP["R_rms"], 1e-3,
    note="DISAGREE: exact value x_E/sqrt2 = 2.0608 (3D quadrature, resolution-independent); original's "
         "spline profile carries a spurious f ~ a/r tail (see x2_hopfion tail_sensitivity)")
add("hopfion c0 (rms)", hop["c0_hopf_rms"], Ah["c0_rms"], 1e-3, note="follows from R_rms")
add("hopfion c0 (ring)", hop["c0_hopf_ring"], Ah["c0_ring"], 2e-5)
add("hopfion g^2 min (LEP, rms)", hop["electron_LEP"]["g2_min"], Ah["LEP"]["g2_min_rms"], 1e-3)
add("hopfion sqrt(kappa2) (LEP, rms) MeV", hop["electron_LEP"]["sqrt_kappa2_MeV"], Ah["LEP"]["sqrt_kappa2_MeV_rms"], 1e-3)
# --- pairs
dl = D["pairs"]["demidov_levkov"]
add("DL 2 g^2 M_S", dl["two_g2_M_S_computed"], DLx["model"]["two_g2MS"], 1e-9,
    note="also: left edge of Fig. 3b digitised at g^2E = 6.240 (axis labelled 2g^2M_S)")
add("DL v (degenerate)", dl["v_degenerate"], DLx["model"]["v"], 1e-9)
add("DL F at threshold (Fig. 3b)", dl["F2_exponent_read"]["at_threshold"], DLx["fig3b"]["F_left"], tol_abs=0.05,
    note="pixel reading, axes calibrated on tick marks")
add("DL F high-energy plateau (Fig. 3b, g^2E >= 10.5)", dl["F2_exponent_read"]["at_g2E_11p5"],
    DLx["fig3b"]["F_plateau_mean_E_gt_10p5"], tol_abs=0.05,
    note="DISAGREE beyond the stated +-0.05: the plateau sits 87 px below the 4.0 tick at 555 px/unit")
add("DL g^2 N_min high energy (Fig. 7b)", dl["g2Nmin_classical_read"]["high_energy"],
    DLx["fig7b"]["g2Nmin_plateau_mean_E_gt_8p5"], tol_abs=0.03)
ku = dl["kappa_suppression_per_pair_quantum"]["value"]
add("kappa = F/N_pair (high energy)", ku[0], A["pairs"]["kappa_hi"], tol_abs=0.05 / 6.2358,
    note="inherits the F reading")
add("kappa = F/N_pair (threshold)", ku[1], A["pairs"]["kappa_lo"], tol_abs=0.05 / 6.2358)
rws = dl["coupling_for_unsuppressed_two_particle_production"]["rows"]
add("g^2 for P = 0.1", rws["P=0.1"]["g2"], A["pairs"]["g2_P0p1"], tol_abs=0.05 / 2.3026, note="inherits F")
add("g^2 for P = 1/e", rws["P=0.368"]["g2"], A["pairs"]["g2_P1e"], tol_abs=0.05, note="inherits F")
add("g^2 for P = 0.5", rws["P=0.5"]["g2"], A["pairs"]["g2_P0p5"], tol_abs=0.05 / 0.6931, note="inherits F")
add("M_S/m at P = 0.1", rws["P=0.1"]["M_S_over_m"], A["pairs"]["MS_over_m_at_P0p1"], 2e-2)
add("N_min/N_pair", dl["Nmin_over_Npair"]["value"], A["pairs"]["Nmin_over_Npair"], 1e-2)
# --- Breit-Wheeler
bw = A["breit_wheeler"]
add("BW sigma_max/(pi r_e^2)", hd["Breit-Wheeler sigma_max"]["value"], bw["sigma_max_over_pi_re2"], 1e-8)
add("BW sigma_max (mb)", 170.06, bw["sigma_max_mb"], 1e-4, note="report quotes 170 mb")
add("BW sqrt(s)/2m_e at max", 1.40, bw["sqrt_s_over_2m"], tol_abs=0.005)
add("log10 exp(-F/alpha)", -233.89, A["pairs"]["log10_exp_minus_F_over_alpha"], tol_abs=0.05 / 0.0073 / 2.3026,
    note="inherits F: -229, not -234; with g^2 = e^2 = 4 pi alpha it is -18.2 (not quoted in the report)")
# --- vacuum
v = A["vacuum"]
vo = D["vacuum"]
add("rho_Lambda (GeV^4)", vo["Planck2018_TTTEEE_lowE_lensing"]["rho_L_GeV4"], v["rho_Lambda_GeV4"], 1e-7,
    note="mine from SI: Omega_L 3H0^2/(8 pi G) c^2 (hbar c)^3")
add("rho_Lambda^(1/4) (meV)", vo["Planck2018_TTTEEE_lowE_lensing"]["rho_L_quarter_meV"], v["rho_quarter_meV"], 1e-7)
add("rho with PLAN's rounded H0, Omega_L", vo["PLAN_rounded"]["rho_L_GeV4"], v["rho_with_PLAN_rounded"], 1e-7)
add("Lambda/m_Pl^2 (from 4.24e-66 eV^2)", vo["Planck_Lambda"]["Lambda_over_mPl2_ours"], v["Lambda_over_MPl2_from_4p24"], 1e-6)
add("relative uncertainty from Omega_L h^2", vo["Planck_OmegaLh2"]["rel_unc"], v["rel_unc_from_OLh2"], 1e-6)
ro = vo["ratios_scale4_over_rhoL"]
rm = v["ratios"]
add("f_pi^4/rho_L", ro["f_pi^4 (f_pi = 92.07 MeV = 130.2/sqrt2)"]["ratio"], rm["f_pi 92.07 MeV"], 5e-4,
    note="original uses 130.2/sqrt2 = 92.0653 MeV; I typed 92.07")
add("v_EW^4/rho_L", ro["v_EW^4 (v = 246.22 GeV)"]["ratio"], rm["v_EW 246.22 GeV"], 1e-6)
add("Higgs depth/rho_L", ro["Higgs potential depth m_H^2 v^2/8"]["ratio"], rm["Higgs depth m_H^2 v^2/8"], 1e-6)
for k_o, k_m in (("M_Pl^4 reduced", "M_Pl reduced"), ("M_Pl^4 unreduced", "M_Pl unreduced")):
    ko = [k for k in ro if k.startswith(k_o.split("^")[0]) and (("reduced" in k) and (("unreduced" in k) == ("unreduced" in k_o)))]
    add(k_m + "^4/rho_L", ro[ko[0]]["ratio"] if ko else None, rm[k_m], 1e-6)
add("m_e^4/rho_L", ro["m_e^4"]["ratio"], rm["m_e"], 1e-6)

n_cmp = sum(1 for r in rows if r["agree"] is not None)
n_dis = sum(1 for r in rows if r["agree"] is False)
for r in rows:
    flag = "  ?" if r["agree"] is None else ("OK " if r["agree"] else "XX ")
    o = r["original"]; m = r["recomputed"]
    fo = f"{o:.8g}" if isinstance(o, (int, float)) else str(o)
    fm = f"{m:.8g}" if isinstance(m, (int, float)) else str(m)
    rel = f"{r['rel_diff']:+.2e}" if isinstance(r["rel_diff"], float) else ""
    print(f"{flag} {r['quantity']:<48s} orig={fo:<16s} x2={fm:<16s} rel={rel:<10s} {r['note']}")
print(f"\n{n_cmp} compared, {n_dis} disagree")

extra = {
    "E1e_combination": {k: A["pairs"][k] for k in A["pairs"] if k.startswith("E1e")},
    "phi4_g2_Npair": A["pairs"]["phi4_g2_Npair"],
    "c0_extra_definitions": {"mean_baryon_radius": H["c0"]["meanB"], "radius_enclosing_90pct_energy": H["c0"]["E90"]},
    "c0_half_min_with_pion_mass_beta16": H["pion_mass_family"][-1]["c0_half"],
    "floor_with_half_baryon_radius": A["floor"]["1.0"]["MR_min_half"],
    "hopfion_tail_sensitivity": HP["tail_sensitivity"],
    "hopfion_derrick_E2_over_E4": HP["derrick_E2_over_E4"],
    "hopfion_perturbations": HP["perturbations"],
    "DL_fig3b_curve": {k: v for k, v in DLx["fig3b"].items() if k.startswith("F_at")},
    "DL_fig7b_curve": {k: v for k, v in DLx["fig7b"].items() if k.startswith("g2Nmin_at")},
    "log10_suppression_4pi_alpha": A["pairs"]["log10_exp_minus_F_over_4pi_alpha"],
    "LEP_bound_qualifier": "Schael et al. 2013 Eq. (3.9): VV contact model, positive interference, electromagnetic coupling strength (model dependent)",
}
json.dump({"rows": rows, "n_compared": n_cmp, "n_disagree": n_dis, "extra": extra},
          open("x2_compare_table.json", "w"), indent=1, default=float)
