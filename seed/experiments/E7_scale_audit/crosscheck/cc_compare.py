#!/usr/bin/env python3
"""E7 cross-check: compare the independent values (cc_*.json) with the original results.json and
write crosscheck.json.  Agreement rule: within the original's stated tolerance where one exists,
otherwise relative difference <= 1e-3 (pure computations) or <= the stated reading uncertainty
(figure readings)."""
import json
import numpy as np

O = json.load(open("../results.json"))
D = O["details"]
A = json.load(open("cc_audit.json"))
H = json.load(open("cc_hedgehog.json"))

rows = []


def add(q, orig, mine, tol_rel=None, tol_abs=None, note=""):
    if tol_abs is not None:
        agree = abs(orig - mine) <= tol_abs
    else:
        agree = abs(orig - mine) <= (tol_rel if tol_rel is not None else 1e-3) * abs(orig)
    rows.append(dict(quantity=q, original=orig, recomputed=mine, rel_diff=(mine - orig) / orig if orig else None,
                     agree=bool(agree), note=note))


hh = A["hedgehog"]
add("a1 = M_cl/(F_pi/e)", O["hedgehog"]["best"]["a1"] if "best" in O["hedgehog"] else D["inputs"]["hedgehog"]["a1"], hh["a1"], 1e-6,
    note="Ritz-spectral energy minimisation vs solve_bvp/shooting")
add("Lambda", D["inputs"]["hedgehog"]["Lambda"], hh["Lambda"], 1e-6)
for k, nm in [("B", "x_B"), ("M", "x_M"), ("E", "x_E"), ("half", "x_half")]:
    add(f"radius a2 ({k})", D["inputs"]["hedgehog"][nm], hh["x"][k], 1e-6)
for k in ["B", "M", "E", "half"]:
    add(f"c0 ({k})", D["skyrme"]["c0"][k], hh["c0"][k], 1e-6)
pr = D["skyrme"]["proton"]
add("R_B at ANW (fm)", pr["R_B_fm"], A["ANW"]["R"]["B"], 1e-6)
add("R_M at ANW (fm)", pr["R_M_fm"], A["ANW"]["R"]["M"], 1e-6)
add("M_cl at ANW (MeV)", pr["M_classical_MeV"], A["ANW"]["M_cl"], 1e-6)
add("M_N model (MeV)", pr["M_N_model_MeV"], A["ANW"]["M_N"], 1e-6)
add("M_Delta model (MeV)", pr["M_Delta_model_MeV"], A["ANW"]["M_D"], 1e-6)
add("own fit F_pi (938.9, 1232)", pr["own_fit_to_MN_MDelta"]["F_pi_MeV"], A["fit"]["938.9_1232"]["F_pi"], 1e-6)
add("own fit e (938.9, 1232)", pr["own_fit_to_MN_MDelta"]["e"], A["fit"]["938.9_1232"]["e"], 1e-6)
add("proton MR (939 x R_B)", pr["MR_nucleon_model"]["value"], A["ANW"]["MR_939_B"], 1e-6)
add("proton MR classical c0/e^2", pr["MR_classical"]["value"], A["ANW"]["MR_classical_B"], 1e-6)
add("r_p/lambda_C (data)", pr["MR_data"]["value"], A["proton_data"]["rp_over_lambdaC"], 1e-6)
add("E_rot/M at ANW", pr["rotor_over_mass"]["value"], A["ANW"]["rot_over_M"], 1e-6)
fl = D["skyrme"]["semiclassical_floor"]
add("floor (MR)_min, E_rot<=M", fl["rot_over_M_le_1.0"]["MR_min_B"], A["electron"]["floor"]["1.0"]["MR_min_B"], 1e-6)
add("floor (MR)_min, E_rot<=0.1M", fl["rot_over_M_le_0.1"]["MR_min_B"], A["electron"]["floor"]["0.1"]["MR_min_B"], 1e-6)
el = D["skyrme"]["electron"]
add("lambda_C/R (LEP)", el["LEP"]["compton_over_R_min"], A["electron"]["LEP"]["lambdaC_over_R"], 1e-6)
add("lambda_C/R (SEED 1e-3 fm)", el["SEED"]["compton_over_R_min"], A["electron"]["SEED"]["lambdaC_over_R"], 1e-6)
add("e needed (LEP, B)", el["LEP"]["B"]["e_min"], A["electron"]["LEP"]["B"]["e"], 1e-6)
add("e needed (LEP, half)", el["LEP"]["half"]["e_min"], A["electron"]["LEP"]["half"]["e"], 1e-6)
add("e needed (LEP, M)", el["LEP"]["M"]["e_min"], A["electron"]["LEP"]["M"]["e"], 1e-6)
add("e needed (SEED, B)", el["SEED"]["B"]["e_min"], A["electron"]["SEED"]["B"]["e"], 1e-6)
add("F_pi needed (LEP, B) MeV", el["LEP"]["B"]["F_pi_MeV"], A["electron"]["LEP"]["B"]["F_pi_MeV"], 1e-6)
add("E_rot/M at electron fold (LEP, B)", el["LEP"]["B"]["rot_over_M"], A["electron"]["LEP"]["B"]["rot_over_M"], 1e-6,
    note="mine computed from I1 and F_pi in MeV, not from the closed formula")
add("E_rot/M at electron fold (SEED, B)", el["SEED"]["B"]["rot_over_M"], A["electron"]["SEED"]["B"]["rot_over_M"], 1e-6)
add("e^2/16pi^2 (LEP, B)", el["LEP"]["B"]["naive_loop_parameter_e2_over_16pi2"], A["electron"]["LEP"]["B"]["e2_over_16pi2"], 1e-6)
add("floor / electron MR (LEP)", el["failure_factor_vs_floor"]["value"], A["electron"]["floor_over_electron_LEP"], 1e-6)
fam_o = {r["beta"]: r for r in D["skyrme"]["pion_mass_family"]["rows"]}
for r in H["pion_mass_family"]:
    if r["beta"] in fam_o:
        add(f"c0_B(beta={r['beta']})", fam_o[r["beta"]]["c0_B"], r["c0_B"], 2e-3,
            note="my L-spread is 2e-3 at beta=8, 4e-4 at beta=16" if r["beta"] >= 8 else "")
hp = D["hopfion"]
add("hopfion E_W (ansatz)", hp["E_W_ansatz"], A["hopfion"]["E_W"], 1e-6, note="exact identity E_W = a1/(3 pi^2) (derived here) + 3D finite-difference check")
add("hopfion R_ring (Ward)", hp["R_ring_ward"], A["hopfion"]["R_ring"], 1e-4)
add("hopfion R_rms energy (Ward)", hp["R_rms_ward"], A["hopfion"]["R_rms"], 1e-3,
    note="DISAGREE: original spline has a spurious f ~ a/r tail that inflates the rms; exact = x_E/sqrt2")
add("hopfion c0 (rms)", hp["c0_hopf_rms"], A["hopfion"]["c0_rms"], 1e-3, note="follows from R_rms")
add("hopfion c0 (ring)", hp["c0_hopf_ring"], A["hopfion"]["c0_ring"], 1e-4)
add("hopfion g^2 min (LEP, rms)", hp["electron_LEP"]["g2_min"], A["hopfion"]["LEP"]["g2_min_rms"], 1e-3)
dl = D["pairs"]["demidov_levkov"]
add("DL 2 g^2 M_S", dl["two_g2_M_S_computed"], A["demidov_levkov"]["two_g2_MS"], 1e-6,
    note="also: left edge of DL Fig. 3b digitised at g^2E = %.3f" % A["demidov_levkov"]["digitized"]["left_edge_g2E_fig3b"])
add("DL v (degenerate)", dl["v_degenerate"], A["demidov_levkov"]["v_degenerate"], 1e-6)
add("DL F at threshold (Fig. 3b)", dl["F2_exponent_read"]["at_threshold"], A["demidov_levkov"]["digitized"]["F_threshold"], tol_abs=0.05,
    note="pixel digitisation vs eye reading; stated uncertainty +-0.05")
add("DL F at g^2E = 11.5 (Fig. 3b)", dl["F2_exponent_read"]["at_g2E_11p5"], A["demidov_levkov"]["digitized"]["F_at_11p5"], tol_abs=0.05,
    note="DISAGREE beyond the stated +-0.05: plateau is 3.85, not 3.93")
add("DL g^2 N_min high energy (Fig. 7b)", dl["g2Nmin_classical_read"]["high_energy"], A["demidov_levkov"]["digitized"]["g2Nmin_high"], tol_abs=0.03)
add("kappa = F/N_pair (high energy)", dl["kappa_suppression_per_pair_quantum"]["value"][0], A["demidov_levkov"]["kappa_per_pair_quantum"][0], tol_abs=0.008,
    note="inherits the F reading")
for P in ["P=0.1", "P=0.368", "P=0.5"]:
    add(f"g^2 for {P}", dl["coupling_for_unsuppressed_two_particle_production"]["rows"][P]["g2"], A["demidov_levkov"]["unsuppressed"][P]["g2"], 0.013,
        note="inherits the F reading (tolerance = 0.05/3.93)")
bw = D["pairs"]["QED_breit_wheeler"]
add("BW sigma_max/(pi r_e^2)", bw["sigma_max_over_pi_re2"], A["breit_wheeler"]["sigma_max_over_pi_re2"], 1e-6)
add("BW sigma_max (mb)", bw["sigma_max_mb"], A["breit_wheeler"]["sigma_max_mb"], 1e-6)
add("BW sqrt(s)/2m_e at max", bw["sqrt_s_at_max_over_2me"], A["breit_wheeler"]["sqrt_s_over_2me"], 1e-5)
add("log10 exp(-F/alpha)", bw["hypothetical_fold_suppression"]["exp_minus_F_over_alpha_log10"], A["demidov_levkov"]["log10_exp_minus_F_over_alpha"], 0.013,
    note="inherits F: -229 not -234")
vac = D["vacuum"]
add("rho_Lambda (GeV^4)", vac["Planck2018_TTTEEE_lowE_lensing"]["rho_L_GeV4"], A["vacuum"]["rho_L_GeV4"], 1e-6,
    note="mine from SI: 3H0^2/(8 pi G) c^2 (hbar c)^3")
add("rho_Lambda^(1/4) (meV)", vac["Planck2018_TTTEEE_lowE_lensing"]["rho_L_quarter_meV"], A["vacuum"]["rho_L_quarter_meV"], 1e-6)
add("Lambda/m_Pl^2", vac["Planck_Lambda"]["Lambda_over_mPl2_ours"], A["vacuum"]["Lambda_over_MPl2"], 1e-6)
ratio_map = {"f_pi^4 (f_pi = 92.07 MeV = 130.2/sqrt2)": "f_pi (92.07 MeV)", "v_EW^4 (v = 246.22 GeV)": "v_EW 246.22 GeV",
             "Higgs potential depth m_H^2 v^2/8": "Higgs depth m_H^2 v^2/8", "M_Pl^4 reduced (2.435e18 GeV)": "M_Pl reduced",
             "M_Pl^4 unreduced (1.221e19 GeV)": "M_Pl unreduced", "m_e^4": "m_e"}
for ko, km in ratio_map.items():
    add(f"ratio {km}/rho_L", vac["ratios_scale4_over_rhoL"][ko]["ratio"], A["vacuum"]["ratios"][km], 1e-4)

n_dis = sum(not r["agree"] for r in rows)
out = dict(experiment="E7 Scale and coupling audit -- independent cross-check",
           n_quantities=len(rows), n_disagree=n_dis, comparisons=rows,
           extra_independent=dict(
               hopfion_identity="E_W[n = U tau3 U^+] = (1/(3 pi^2)) x ANW Skyrme functional after r = y/sqrt2: E_W = a1/(3 pi^2) = %.10f" % A["hopfion"]["E_W"],
               pion_mass_floor=A["pion_mass_floor"],
               E1e_phi4=A.get("E1e_phi4"),
               other_radius_definitions=dict(c0_meanB=A["hedgehog"]["c0"]["meanB"], c0_E90=A["hedgehog"]["c0"]["E90"]),
               e2_over_a1_LEP=A["electron"]["LEP"]["B"]["e2_over_a1"]))
dlr = A["demidov_levkov"]
out["issues"] = [
    dict(severity="minor", id="DL-F-plateau",
         description="DL Fig. 3b two-particle exponent at high energy is %.3f (pixel digitisation, axis calibrated on tick-label centres), not 3.93; "
                     "the difference exceeds the stated +-0.05 reading uncertainty. Threshold value %.3f vs 4.45 is within it. Downstream: "
                     "kappa 0.630 -> %.3f; g^2 for P = 0.1, 1/e, 0.5: %.2f, %.2f, %.2f (not 1.71, 3.93, 5.67); M_S/m at P = 0.1: %.2f; "
                     "exp(-F/alpha) = 10^%.0f (not 10^-234). No verdict changes." % (
                         dlr["digitized"]["F_at_11p5"], dlr["digitized"]["F_threshold"], dlr["kappa_per_pair_quantum"][0],
                         dlr["unsuppressed"]["P=0.1"]["g2"], dlr["unsuppressed"]["P=0.368"]["g2"], dlr["unsuppressed"]["P=0.5"]["g2"],
                         dlr["unsuppressed"]["P=0.1"]["M_S_over_m"], dlr["log10_exp_minus_F_over_alpha"]),
         fix="Replace F2 = 3.93 by 3.85 in e7_audit.py, the figure legend, results.json, REPORT.md and the summary."),
    dict(severity="minor", id="hopfion-rms",
         description="Hopfion energy-rms radius is %.4f Ward units (exact: x_E/sqrt2; confirmed by a 3D finite-difference evaluation), not 2.1441; "
                     "c0_hopf(rms) = %.1f (not 589.7), g^2_min(LEP, rms) = %.2e (not 2.07e9). Cause: the 24-node cubic spline in t with f(1) = 0 "
                     "and not-a-knot ends has df/dt(1) != 0, i.e. a spurious f ~ a/r tail; the rms integral is linearly sensitive to it out to the "
                     "last Gauss node (r ~ 2e5). Energy and ring radius are unaffected." % (A["hopfion"]["R_rms"], A["hopfion"]["c0_rms"], A["hopfion"]["LEP"]["g2_min_rms"]),
         fix="Build f ~ (1-t)^2 into the spline (or use the identity f(r) = F_Skyrme(sqrt2 r)); report c0 = 341-567, g^2 >= 1.2e9-2.0e9."),
    dict(severity="minor", id="hopfion-calibrated-label",
         description="The hedgehog-Hopf ansatz energy is identically a1/(3 pi^2): with n = U tau3 U^+ the angular-integrated Ward energy equals "
                     "(1/(3 pi^2)) x the ANW hedgehog functional after r = y/sqrt2. So E_W = 1.2314 is the Skyrme number again, not an independent "
                     "hopfion calibration, and the 'within 5% above 1.204' tolerance is self-chosen (E8's preregistered 2% would fail).",
         fix="Label it 'variational upper bound, consistent with 1.204-1.22' rather than CALIBRATED; note the identity."),
    dict(severity="minor", id="proton-MR-label",
         description="'Proton M R/hbar c = 2.826 CALIBRATED': 2.8 is a PLAN expectation, not a literature target, and the +-0.05 is self-set. "
                     "Under PLAN's own definition M R/hbar c = c0/e^2 (classical mass) the value is 2.598, outside 2.8 +- 0.05; the pass depends on using 939 MeV.",
         fix="Report as 'consistent with the PLAN expectation when M = 939 MeV (2.83); classical c0/e^2 = 2.60'; drop CALIBRATED."),
    dict(severity="minor", id="pairs-evidence",
         description="The pairs verdict rests on figure readings of Demidov-Levkov plus the scaling argument, not on a computation in this run; the "
                     "PLAN-specified E1e input was missing at run time but now exists: E1e gives N_min lambda/m^2 <= 1.69 (Gaussian packets, reproduced at "
                     "dx = 0.05), i.e. g^2 N_min <= 3.38 = 2.5 N_pair, so classical production from <= 2 quanta needs g^2 >= 1.69 (lambda/m^2 >= 0.84). "
                     "This agrees with the DL-based estimate. The g^2 thresholds extrapolate the leading exponent exp(-F/g^2) to g^2 ~ 2-6, outside its "
                     "validity (prefactors and higher orders are O(1) there); the shaded 'unsuppressed' band of fig_vacuum_pairs.png is such an extrapolation.",
         fix="Add the E1e combination (PLAN wording); describe the thresholds as indicative."),
    dict(severity="minor", id="labels-and-rounding",
         description="results.json labels lambda_C/R and the vacuum ratios QUANTIFIED while the summary says NO_TARGET; (MR)_min at E_rot <= 0.1 M is "
                     "quoted as 2.40 in a results.json note and 2.39 elsewhere (2.3947).",
         fix="Harmonise labels and rounding."),
    dict(severity="minor", id="E2-profile",
         description="PLAN E7 says 'compute c0 from the E2 profile'; E7 solved its own hedgehog. Harmless (agrees with E2's a1 and Lambda to 1e-11) but not listed as a deviation.",
         fix="List it among the deviations."),
    dict(severity="minor", id="LEP-model-dependence",
         description="The LEP r_e < 1.1e-19 m (Schael et al. 2013 Eq. 3.9, verified) assumes the VV contact model with positive interference and "
                     "electromagnetic coupling strength; the report quotes it without that qualifier.",
         fix="Add the qualifier."),
]
out["overall"] = "confirmed_with_corrections"
with open("cc_crosscheck.json", "w") as f:   # first cross-check pass; crosscheck.json is written by x2_crosscheck_json.py
    json.dump(out, f, indent=1, default=float)
for r in rows:
    print(f"{'OK ' if r['agree'] else 'XX '} {r['quantity']:42s} orig={r['original']:.6g}  mine={r['recomputed']:.6g}  rel={r['rel_diff']:+.2e}  {r['note']}")
print(f"{len(rows)} quantities, {n_dis} disagree")
