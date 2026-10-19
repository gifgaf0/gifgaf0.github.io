#!/usr/bin/env python3
"""E2 -- assemble results.json (headline numbers, targets, tolerances, verdicts) from out/*.json."""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
HBARC = 197.3269804  # MeV fm


def load(n):
    with open(os.path.join(OUT, n)) as f:
        return json.load(f)


def verdict_rel(val, tgt, tol):
    return "CALIBRATED" if abs(val / tgt - 1) <= tol else "MISS"


# Verdict words (PLAN §1): CALIBRATED = literature target reproduced within tolerance; CONFIRMED = a seed
# claim holds. PASS (not a PLAN word) marks an internal consistency check with a preregistered tolerance
# (virial, von Laue). Reconciliation: every exact/qualitative verdict below is now derived from an
# asserted check in out/*.json instead of being hard-coded.
def from_check(cond, word):
    return word if cond else "MISS"


def main():
    hh = load("hedgehog.json"); ref = hh["reference_halfline_N160"]
    vf = load("verify.json"); ro = load("rotor.json"); dv = load("derrick.json")
    anw = ro["parameter_sets"]["ANW_SU2_fit"]; s3 = ro["parameter_sets"]["SU3_refit_PDG_centres"]
    rc, dc = ro["checks"], dv["checks"]
    gA_pdg, gA_pdg_err = abs(ro["pdg"]["gA_over_gV"]), ro["pdg"]["gA_over_gV_err"]
    head = []

    def add(q, val, unit, tgt, tol, src, verdict, note=""):
        head.append({"quantity": q, "value": val, "unit": unit, "target": tgt, "tolerance": tol, "source": src,
                     "verdict": verdict, "note": note})

    M = ref["M_over_Fpi_e"]
    tM = 1.2315 * 3 * np.pi ** 2
    tSW = 23.2 * np.pi / 2          # Schechter-Weigel E = 23.2 pi f_pi/e with f_pi = F_pi/2
    vM = all(verdict_rel(M, t_, 0.002) == "CALIBRATED" for t_ in (tM, 36.5, tSW))
    add("classical mass M_cl", M, "F_pi/e (F_pi 186-MeV convention)", tM, "0.2%",
        "PLAN E2 target 36.5 F_pi/e = 1.2315 x 3pi^2. Provenance corrected in reconciliation: neither number "
        "appears in the cited texts. [read: Schechter-Weigel hep-ph/9907554 sec. 2: E = 23.2 pi f_pi/e = 36.44 F_pi/e]; "
        "36.5 is ANW's value (secondary sources); 1.2315 x 3pi^2 is the standard E/(12 pi^2) in Skyrme units (not read)",
        "CALIBRATED" if vM else "MISS",
        f"M/(3 pi^2 F_pi/e) = {ref['M_over_3pi2']:.7f}; {100*(M/tM-1):+.3f}% from 1.2315 x 3pi^2 = {tM:.3f}, "
        f"{100*(M/36.5-1):+.2f}% from 36.5, {100*(M/tSW-1):+.3f}% from SW's 23.2 pi/2 = {tSW:.2f}: inside 0.2% of all three")
    add("Lambda in I1 = (2pi/3) Lambda/(e^3 F_pi)", ref["Lambda"], "dimensionless", 50.9, "0.5%",
        "PLAN E2 target 50.9 (ANW's value). [read: Schechter-Weigel hep-ph/9907554: alpha^2 = 53.3/(e^3 f_pi), "
        "i.e. Lambda = 3 x 53.3/pi = 50.90]", verdict_rel(ref["Lambda"], 50.9, 0.005),
        f"{100*(ref['Lambda']/50.9-1):+.3f}%; I1 = {ref['I1_coef']:.4f}/(e^3 F_pi). With F(X)=0 at X = 10/20/40 and no tail: "
        f"{hh['dirichlet_no_tails']['X10']['Lambda']:.2f}/{hh['dirichlet_no_tails']['X20']['Lambda']:.2f}/{hh['dirichlet_no_tails']['X40']['Lambda']:.2f}")
    add("ANW fit F_pi (M_N = 939, M_Delta = 1232 MeV, SU(2) rotor)", anw["F_pi"], "MeV", 129.0, "1%",
        "PLAN E2 (ANW via secondary sources); upgraded in reconciliation to [read: Acus et al. hep-ph/9605435 "
        "Table 1, ANW column: f_pi = 64.5 MeV, i.e. F_pi = 129 MeV]", verdict_rel(anw["F_pi"], 129.0, 0.01),
        f"{100*(anw['F_pi']/129-1):+.2f}%")
    add("ANW fit e", anw["e"], "dimensionless", 5.45, "1%",
        "PLAN E2 (ANW via secondary sources); [read: Acus et al. Table 1, ANW column: e = 5.45]",
        verdict_rel(anw["e"], 5.45, 0.01), f"{100*(anw['e']/5.45-1):+.2f}%")
    add("g_A at the ANW fit (SU(2), -(pi/(3e^2)) D)", anw["gA_SU2"], "dimensionless", 0.61, "+-0.01",
        "PLAN E2; formula read in Acus et al. hep-ph/9605435 eqs. 4.9-4.10; [read: Acus et al. Table 1, ANW column: g_A = 0.61]",
        "CALIBRATED" if abs(anw["gA_SU2"] - 0.61) <= 0.01 else "MISS",
        f"D = {ref['D_gA']:.9f} = -2C (D/(-2C) - 1 = {ref['D_gA']/(-2*ref['C'])-1:+.0e}). This formula is 3/2 of the ball "
        f"integral of the Noether axial current (the q->0 transverse form factor with a massless pion pole); the bare ball "
        f"integral gives {2/3*anw['gA_SU2']:.3f}. PDG 2026 g_A/g_V = -{gA_pdg:.4f} +- {gA_pdg_err:.4f}: the model is "
        f"{100*(anw['gA_SU2']/gA_pdg-1):+.0f}%")
    add("I2 coefficient (pi/2) J2, I2 = coef/(e^3 F_pi)", ref["I2_coef"], "dimensionless", 40.5, "1.5% (exact vs arctan ansatz)",
        "PLAN E2 [read: Praszalowicz eq. 28, arctan ansatz; formula Kopeliovich hep-th/9707067 eq. 22c]. The target is a "
        "variational (arctan-ansatz) value, not a published exact-profile I2: a weak calibration that only excludes "
        "formula slips above 1.5%",
        verdict_rel(ref["I2_coef"], 40.5, 0.015),
        f"J2 = {ref['J2']:.6f}; arctan ansatz recomputed: {hh['arctan_ansatz']['I2_coef']:.4f} "
        f"(exact is {100*(ref['I2_coef']/hh['arctan_ansatz']['I2_coef']-1):+.2f}% above it); I1/I2 = {ref['I1_over_I2']:.5f}. "
        "The I2 density is verified independently: explicit SU(3) matrices U = A U0 A^dag here (5e-15), finite "
        "differences of the Lagrangian in the cross-check (7e-11)")
    add("lowest allowed SU(3) irreps, Y_R = 1", "8 (J=1/2), 10 (J=3/2), 10bar (J=1/2), then 27 (J=3/2), 35 (J=5/2), 27 (J=1/2)",
        "", "8 (1/2), 10 (3/2), 10bar (1/2), then 27", "exact", "PLAN E2 [read: DPP hep-ph/9703373 eqs. 9-11]",
        from_check(rc["lowest allowed Y_R=1 levels: 8(1/2), 10(3/2), 10bar(1/2), 27(3/2), 35(5/2), 27(1/2) at both sets"], "CALIBRATED"),
        "asserted by su3_rotor.py. The order depends only on I1/I2 = 2.62 (one profile), so the two parameter sets are one "
        "test; it follows from the DPP rotor formula and the WZ rule, so this calibrates the irrep code, not new physics")
    add("E(10) - E(8)", "3/(2 I1)", "", "3/(2 I1)", "exact", "PLAN E2 [read: DPP eq. 12]",
        from_check(rc["E(10)-E(8) = 3/(2 I1) exactly"], "CALIBRATED"),
        f"algebraic identity of the DPP rotor formula (checks the Casimir code); exact rational arithmetic; "
        f"{anw['E10_minus_E8']:.1f} MeV (ANW set), {s3['E10_minus_E8']:.1f} MeV (SU(3) refit)")
    add("E(10bar) - E(8)", "3/(2 I2)", "", "3/(2 I2)", "exact", "PLAN E2 [read: DPP eq. 13]",
        from_check(rc["E(10bar)-E(8) = 3/(2 I2) exactly"], "CALIBRATED"),
        f"algebraic identity of the DPP rotor formula; exact; {anw['E10bar_minus_E8']:.1f} MeV (ANW set), "
        f"{s3['E10bar_minus_E8']:.1f} MeV (SU(3) refit)")
    add("virial E2/E4 - 1 at the solution", ref["virial_dev"], "", 0.0, "1e-4", "PLAN E2 (internal check)",
        from_check(abs(ref["virial_dev"]) < 1e-4 and dc["virial_E2_eq_E4_1e-4"], "PASS"),
        f"also {dv['E2_over_E4_minus_1']:+.1e} from an independent quadrature; E(mu) minimum at mu* = {dv['mu_star']:.9f}. "
        "PASS = internal check (PLAN reserves CALIBRATED for literature targets)")
    add("von Laue: int d^3x p / int d^3x |p|", dv["von_Laue_ratio"], "", 0.0, "1e-6 (numerical zero)", "PLAN E2 (internal check)",
        from_check(abs(dv["von_Laue_ratio"]) < 1e-6 and dc["von_Laue_zero"], "PASS"),
        f"single pressure node at x = {dv['pressure_nodes_x'][0]:.5f} (root), p(0) = {dv['p0']:.6f} > 0 inside; stress "
        "tensor verified against the Noether T_ij")
    add("Derrick: sigma-model energy under shrinking (SEED §4)", "E2(mu) = E2/mu, strictly decreasing; radial sigma-model ODE ends at F = pi/2",
        "", "no minimum without the Skyrme term", "qualitative", "PLAN E2 / Derrick 1964 (seed claim §4)",
        from_check(dc["no_minimum_without_Skyrme_term"] and dc["scaling_law_by_quadrature"], "CONFIRMED"),
        f"scaling law verified by quadrature to {dv['scaling_max_rel_dev']:.0e} (an exact identity); verdict word changed "
        "from CALIBRATED to CONFIRMED in reconciliation (this is a seed claim, not a literature number)")
    nct = ro["Nc_table"]
    lowest = "; ".join(f"Nc={k} {v['lowest_states'][0]['irrep']}({v['lowest_states'][0]['J']})" for k, v in nct.items())
    add("N_c parity: J half-integer iff N_c odd (B = 1, Y_R = N_c/3; SEED §2)", "holds for N_c = 1..7 (all irreps p+q <= 16) and N_c <= 15 (p+q <= 30)",
        "", "J half-integer exactly when N_c odd", "exact", "PLAN E2 prediction (Witten 1983; seed claim §2)",
        from_check(rc["J half-integer iff Nc odd (Nc=1..7, p+q<=16; sweep Nc<=15, p+q<=30)"], "CONFIRMED"),
        f"conditional on the imported WZ rule Y_R = N_c B/3 (not derived here). Lowest states: {lowest}. "
        "Proof: 2J = m12-m22 = (N_c + 2p + 4q)/3 = N_c mod 2. Verdict word changed from CALIBRATED in reconciliation")
    # predictions (no literature target)
    add("E(8) - E_SU2(N) at ANW parameters = 3/(4 I2)", anw["E8_minus_EN_SU2"], "MeV", "about 385 (preregistered expectation)", "none",
        "PLAN E2 prediction", "NO_TARGET", "agrees with the preregistered expectation")
    add("SU(3) refit to PDG octet/decuplet centres: F_pi", s3["F_pi"], "MeV", "about 114 (expectation)", "none", "PLAN E2 prediction", "NO_TARGET",
        f"centres {ro['pdg']['octet_centre_MeV']:.2f} and {ro['pdg']['decuplet_centre_MeV']:.2f} MeV (PDG 2026, isospin averaged, state-weighted)")
    add("SU(3) refit: e", s3["e"], "dimensionless", "about 5.25 (expectation)", "none", "PLAN E2 prediction", "NO_TARGET", "")
    add("SU(3) refit: antidecuplet E(10bar)", s3["E10bar"], "MeV", "near 1760 (expectation)", "none", "PLAN E2 prediction", "NO_TARGET",
        "rigid rotor, exact SU(3); no 10bar state at this mass is listed by PDG")
    add("ANW set: E(8), E(10), E(10bar)", [anw["E8"], anw["E10"], anw["E10bar"]], "MeV", "none", "", "", "NO_TARGET",
        f"vs PDG centres 1151.2 / 1382.1: octet {100*(anw['E8']/ro['pdg']['octet_centre_MeV']-1):+.0f}%, decuplet {100*(anw['E10']/ro['pdg']['decuplet_centre_MeV']-1):+.0f}%")
    add("SU(3) refit: g_A (SU(2) formula; SU(3)-symmetric rotor x 7/10)", [s3["gA_SU2"], s3["gA_SU3_symmetric"]], "dimensionless", "none", "", "",
        "NO_TARGET", "<p|D33|p> = -1/3 (SU(2)) vs -7/30 (SU(3) octet), computed from explicit Clebsch-Gordan intertwiners")
    so = ro["optional_symmetry_breaking"]
    gu = so["sum_rules"]["Guadagnini 8(N+Xi*)+3Sigma-11Lambda-8Sigma*"]
    add("OPTIONAL Guadagnini relation 8(N+Xi*)+3Sigma = 11Lambda+8Sigma* with PDG 2026", gu["PDG_value_MeV"], "MeV (LHS-RHS)", 0.0,
        "none (first-order relation)", "Praszalowicz eq. 11 [read]; Guadagnini 1984", "NO_TARGET",
        f"{100*gu['relative']:+.3f}% of the sides; holds identically for H' = -alpha D88 + beta Y (computed matrix elements). "
        f"2 fitted inputs alpha = {so['alpha_MeV']:.0f} MeV, beta = {so['beta_MeV']:.0f} MeV reproduce the 8 multiplets with rms {so['rms_MeV']:.1f} MeV")
    # extra hedgehog numbers
    r2 = ref["r2B"]
    extras = {
        "C_asymptotic": {"value": ref["C"], "meaning": "F -> C/x^2 - C^3/(21x^6) - (4/3)C^3/x^8"},
        "Fprime0": {"value": ref["Fp0"], "meaning": "dF/dx at x = 0"},
        "r2_baryon_dimless": {"value": r2, "meaning": "<r^2>_B (e F_pi)^2 = -(2/pi) int x^2 s^2 F' dx"},
        "r_baryon_rms_fm_ANW": {"value": float(np.sqrt(r2) / (anw["e"] * anw["F_pi"]) * HBARC),
                                "meaning": "isoscalar (baryon) rms radius at the ANW fit (E5's target is 0.59 fm)"},
        "I1_ANW_fm": anw["I1_fm"], "I2_ANW_fm": anw["I2_fm"], "I1_SU3refit_fm": s3["I1_fm"], "I2_SU3refit_fm": s3["I2_fm"],
        "M_cl_ANW_MeV": anw["M_cl"], "M_cl_SU3refit_MeV": s3["M_cl"],
        "invI1_invI2_MeV": {"ANW": [anw["invI1"], anw["invI2"]], "SU3refit": [s3["invI1"], s3["invI2"]]},
    }
    claims = [
        {"claim": "SEED §2: for SU(3) the Wess-Zumino term makes the fold a fermion when N_c is odd (Witten 1983)",
         "verdict": "CONFIRMED",
         "evidence": "Conditional on the WZ constraint Y_R = N_c B/3 (taken from Witten/DPP, not derived here): every allowed state has 2J = N_c mod 2 for N_c = 1..15 (p+q <= 30); lowest states listed for N_c = 1..7. E2 tests the group theory that follows from the rule, not the WZ mechanism"},
        {"claim": "SEED §4: in 3D a static fold cannot be held by gradient energy alone (Derrick); something must push back",
         "verdict": "CONFIRMED",
         "evidence": f"E2[F(mu x)] = E2/mu exactly (quadrature, {dv['scaling_max_rel_dev']:.0e}); the sigma-model radial ODE has no solution reaching F = 0 (ends at pi/2); with the Skyrme term E2/E4 - 1 = {ref['virial_dev']:+.1e} (reference) and {dv['E2_over_E4_minus_1']:+.1e} (independent quadrature), int p d^3x / int |p| d^3x = {dv['von_Laue_ratio']:+.1e}"},
        {"claim": "SEED §6B: quantizing the hedgehog's rotations, the lowest states fill the octet and the decuplet (Guadagnini 1984)",
         "verdict": "CONFIRMED",
         "evidence": "Lowest allowed (Y_R = 1) states are 8 (J=1/2) and 10 (J=3/2), asserted by su3_rotor.py (the order depends only on I1/I2 = 2.62, so the two parameter sets are one test); the same rotor also predicts exotic 10bar (J=1/2) and 27 at E(8) + 3/(2I2) and above (about 1760 MeV at the SU(3) refit), which the seed does not mention"},
        {"claim": "SEED §6B: with exact SU(3) every member of a multiplet has one mass; the splittings need a symmetry-breaking term with more parameters",
         "verdict": "CONFIRMED",
         "evidence": "All d_R(2J+1) rotor states of 8, 10, 10bar are degenerate (explicit matrices). Optional first-order H' = -alpha D88 + beta Y needs 2 fitted inputs; it reproduces the 8 PDG multiplets with rms 4 MeV and implies GMO, equal spacing and Guadagnini's relation (PDG: +0.04%)"},
        {"claim": "SEED §6B: F sets the units and e is the only pure number, so every prediction is a ratio",
         "verdict": "CONFIRMED",
         "evidence": "M = 36.46 F_pi/e, I = coef/(e^3 F_pi), g_A = 18.09/e^2: every dimensionless observable is a function of e alone (massless pions, N_c fixed; a pion mass would add m_pi/(e F_pi)). True by construction (dimensional analysis)"},
        {"claim": "SEED §6B: for nucleons the model lands within roughly 30% (ANW 1983)",
         "verdict": "AMENDED",
         "evidence": f"Masses are fit inputs. The one non-fit nucleon static property E2 computes, g_A = {anw['gA_SU2']:.2f} vs |g_A/g_V| = {gA_pdg:.4f}(13) (PDG 2026), is {100*(1-anw['gA_SU2']/gA_pdg):.0f}% low, outside 30%; in the SU(3)-symmetric rotor it drops further by 7/10. Whether the other static properties (radii, magnetic moments) land within 30% is E5's test; E2 does not assert it (reconciliation: the earlier 'most static properties within about 30%' clause is withdrawn here as not shown by E2). Context: the fitted F_pi = 129 MeV is 30.5% below 186 MeV if the masses are regarded as the inputs"},
    ]
    res = {
        "experiment": "E2 -- the fold in SU(2) and SU(3) (Skyrme hedgehog, rigid-rotor quantisation)",
        "conventions": "L = (F_pi^2/16) Tr dU dU^dag + (1/(32 e^2)) Tr[L_mu,L_nu]^2, F_pi in the 186-MeV convention "
                       "(f_pi = F_pi/2), x = e F_pi r, massless pions, hedgehog F(0) = pi, F ~ C/x^2",
        "headline": head,
        "extras": extras,
        "seed_claims": claims,
        "pdg_inputs": ro["pdg"],
        "reconciliation": [
            "verdict words: N_c parity and Derrick are seed claims -> CONFIRMED; virial and von Laue are internal checks -> PASS",
            "exact/qualitative verdicts derived from asserted checks; the lowest-multiplet ordering is now asserted in su3_rotor.py",
            "target provenance: M_cl and Lambda [read] in Schechter-Weigel as 23.2 pi f_pi/e and 53.3/(e^3 f_pi); ANW F_pi, e, g_A [read] in Acus et al. Table 1",
            "I2 target flagged as an arctan-ansatz value (weak calibration)",
            "PDG 2026 g_A/g_V = -1.2753 +- 0.0013 (was quoted as 1.2754, the 2024 value)",
            "(p,q) = (1,3) named 24bar (was printed as 24)",
            "C now from F(100) plus the asymptotic series (end-point 2nd derivative was off by 4.5e-10; D shifts by 2.3e-10)",
            "pressure node from a root finder (2.152373; was a grid midpoint 2.152214); p(0) from the exact small-x formula",
            "SEED §6B 30% claim: AMENDED kept on the g_A evidence; the 'most static properties' clause withdrawn (E5's test)",
        ],
        "checks": {"skyrme_hedgehog.py": hh["all_checks_pass"], "verify_densities.py": vf["all_checks_pass"],
                   "su3_rotor.py": ro["all_checks_pass"], "derrick_virial.py": dv["all_checks_pass"]},
        "all_checks_pass": all([hh["all_checks_pass"], vf["all_checks_pass"], ro["all_checks_pass"], dv["all_checks_pass"]]),
    }
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)
    for h in head:
        v = h["value"]
        vs = f"{v:.6g}" if isinstance(v, float) else str(v)
        print(f"[{h['verdict']:10s}] {h['quantity']}: {vs} {h['unit']}  (target {h['target']}, tol {h['tolerance']})")
    print("all checks pass:", res["all_checks_pass"])


if __name__ == "__main__":
    main()
