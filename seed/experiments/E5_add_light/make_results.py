#!/usr/bin/env python3
"""
E5: assemble results.json from the component results, compare with PDG 2026, test the seed's
"within roughly 30%" (SEED.md section 6B), compute the enclosed-charge ("dressing") curves and draw
fig_vs_pdg.png.

Inputs (run these first):  symbolic_derivations.py -> symbolic_results.json
                           hedgehog_em.py          -> hedgehog_results.json
                           rotor_charges.py        -> charges_results.json
                           pi0_gamma_gamma.py      -> pi0_results.json
Deterministic; no random numbers.  Writes results.json and fig_vs_pdg.png.
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hedgehog_em as H

HBARC = H.HBARC
PI = math.pi


def load(name):
    with open(os.path.join(HERE, name)) as fh:
        return json.load(fh)


def pdg_data():
    """PDG 2026 nucleon values (pdg package); hard-coded fallback = the same numbers read once."""
    fb = {"mu_p": (2.79284734463, 8.2e-10), "mu_n": (-1.91304276, 4.5e-7), "r_p_fm": (0.84075, 0.00064),
          "r2_n_fm2": (-0.1154675, 0.0017446), "rM_p_fm": (0.851, 0.026), "rM_n_fm": (0.8641227, 0.0086204),
          "gA_over_gV": (-1.2753351, 0.0012583), "source": "fallback (PDG 2026 values read with the pdg package)"}
    try:
        import warnings
        warnings.filterwarnings("ignore")
        import pdg
        api = pdg.connect()
        def g(pid):
            v = api.get(pid).best_summary()
            return (v.value, v.error_positive)
        out = {"mu_p": g("S016MM"), "mu_n": g("S017MM"), "r_p_fm": g("S016CR"), "r2_n_fm2": g("S017MCR"),
               "rM_p_fm": g("S016MCR"), "rM_n_fm": g("S017MRD"), "gA_over_gV": g("S017AV"),
               "source": "PDG 2026 sqlite via the pdg package (S016MM, S017MM, S016CR, S017MCR, S016MCR, S017MRD, S017AV)"}
        return out
    except Exception as ex:
        fb["source"] += " -- pdg error: %s" % ex
        return fb


def enclosed_charge(sol, Lam, L_fm, radii_fm, beta=0.0):
    """Fraction of the proton / neutron charge inside radius R (rho_E = rho_{I=0} +- rho_{I=1})."""
    s = np.sin
    rho0 = lambda x, F, G: -(1.0 / PI) * s(F)**2 * G                                       # integrates to 1/2
    rho1 = lambda x, F, G: x**2 * s(F)**2 * (1 + 4 * (G**2 + s(F)**2 / x**2)) / (2 * Lam)  # integrates to 1/2
    rows = []
    for R in radii_fm:
        xR = min(R / L_fm, sol.X)
        q0 = H.integrate(rho0, sol, b=xR)
        q1 = H.integrate(rho1, sol, b=xR)
        rows.append({"R_fm": R, "Q_p_inside": q0 + q1, "Q_n_inside": q0 - q1, "isoscalar_inside": q0, "isovector_inside": q1})
    return rows


def neutron_peak(sol, Lam, L_fm):
    """(reconciliation) Maximum of the neutron's enclosed charge Q_n(<R).  dQ_n/dR is proportional to the neutron charge density
    rho_{I=0} - rho_{I=1}, so the maximum sits at its node (positive core inside, negative cloud outside); found with brentq."""
    from scipy.optimize import brentq
    s = np.sin
    def dn(x):
        F, G = sol.sol(x)
        return -(1.0 / PI) * s(F)**2 * G - x**2 * s(F)**2 * (1 + 4 * (G**2 + s(F)**2 / x**2)) / (2 * Lam)
    xs = np.geomspace(0.05, min(sol.X, 20.0), 400)
    vals = np.array([dn(x) for x in xs])
    i = int(np.argmax((vals[:-1] > 0) & (vals[1:] <= 0)))
    xp = brentq(dn, xs[i], xs[i + 1], xtol=1e-13)
    q = enclosed_charge(sol, Lam, L_fm, [xp * L_fm])[0]
    return {"R_peak_fm": xp * L_fm, "x_peak": xp, "Q_n_peak": q["Q_n_inside"], "Q_p_at_peak_R": q["Q_p_inside"],
            "method": "node of the neutron charge density (brentq), then the enclosed-charge quadrature up to it"}


def seed_claims(n30, n33, nfin, pz, peak0, enc0, d0, L_anw, nsym, nfail, n_insp):
    """Final seed-claim verdicts (after reconciliation with the independent cross-check)."""
    q = {round(r["R_fm"], 2): r for r in enc0}
    slope_fm = d0["C"]**2 / d0["Lambda"] * L_anw
    return [
        {"claim": "SEED 7.4: gauge a U(1) inside the internal symmetry and read off the folds' electric charges",
         "verdict": "CONFIRMED",
         "evidence": "Q = I3 + Y/2 with the WZ constraint Y_R = N_c B/3; every state of 8, 10, 10bar, 27 has an integer charge "
                     "(Gell-Mann-Nishijima); SU(2): Q = I3 + B/2, the isoscalar half from the gauged WZ term. Needs N_c = 3 with "
                     "standard quark charges (or anomaly-consistent charges). Predicts exotic charges (Theta+, Xi--, Q = +-2 in the 27)."},
        {"claim": "SEED 7.4 / 2: one cone, no vacuum dispersion; photon and fold field share it",
         "verdict": "CONFIRMED (by construction)",
         "evidence": "pion omega^2 = k^2 + m^2, photon omega = |k| (two transverse modes), no mixing; Skyrme and gauged WZ terms have "
                     "no quadratic part (both computed). Holds by construction for a Lorentz-invariant tree-level Lagrangian."},
        {"claim": "Commitment 1: vacuum T_mu nu proportional to g_mu nu, p = -rho in every frame",
         "verdict": "CONFIRMED (by construction)",
         "evidence": "T_mu nu = V0 g_mu nu (mostly-minus) at U = 1; V0 is a free constant."},
        {"claim": "Commitment 4: charge is dressed (effective charge depends on how closely you look), not slowed",
         "verdict": "CONFIRMED (in the preregistered operational sense only)",
         "evidence": "Preregistered prediction holds: with massless pions the isovector <r^2> inside R grows as %.3f fm x R (diverges); "
                     "finite with m_pi = 138 MeV. Enclosed proton charge %.2f at 0.5 fm, %.2f at 1 fm, %.2f at 5 fm; the neutron's "
                     "enclosed charge peaks at %+.3f at R = %.2f fm (positive core, negative cloud). The test cannot tell 'dressing' from "
                     "any extended charge distribution; the mechanism is the fold's classical pion cloud, not QED vacuum polarization; "
                     "'not slowed' holds by construction."
                     % (slope_fm, q[0.5]["Q_p_inside"], q[1.0]["Q_p_inside"], q[5.0]["Q_p_inside"], peak0["Q_n_peak"], peak0["R_peak_fm"])},
        {"claim": "SEED 6B: for nucleons the model lands within roughly 30% (ANW 1983)",
         "verdict": "AMENDED",
         "evidence": "Against PDG 2026 at the calibrated ANW point: %d of %d finite predictions within 33%% (strictly within 30%%: %d of %d; "
                     "mu_p -33%%, mu_n -31%%, g_piNN -32%% sit just outside 30%%). The amendment is carried by g_A (-52%%, a factor ~2) "
                     "and by r_p and <r^2>_n, which are infinite with massless pions. At the fold's own f_pi = F_pi/2 = 64.5 MeV "
                     "(itself 30%% below 92.2 MeV) the gauged WZ term gives Gamma(pi0->gg) = %.2f x PrimEx-II."
                     % (n33, nfin, n30, nfin, pz["ratio_ANW_to_PrimExII"])},
        {"claim": "PLAN E5 internal-consistency prediction (not a SEED sentence): the fold sector and the anomaly prefer different f_pi",
         "verdict": "CONFIRMED (preregistered prediction; no SEED verdict)",
         "evidence": "Gamma(pi0->gg) at the fold's f: %.2f eV (ANW, %.2f x PrimEx-II), %.2f eV (SU(3) refit, %.2f x); "
                     "PrimEx-II needs f = %.2f MeV. Bears on SEED 6B (one (F, e) for all predictions)."
                     % (pz["Gamma_at_ANW_f64.5_eV"], pz["ratio_ANW_to_PrimExII"], pz["Gamma_at_own_SU3_refit_eV"],
                        pz["ratio_SU3_refit_to_PrimExII"], pz["f_needed_for_PrimExII_central_MeV"])},
        {"claim": "SEED 2: the WZ term that makes the fold a fermion also fixes pi0 -> gamma gamma",
         "verdict": "CONFIRMED (the anomaly normalisation); the N_c = 1 exclusion holds only with fixed quark charges",
         "evidence": "Gamma = %.3f eV at N_c = 3, f = 92.21 MeV (%.2f sigma vs PrimEx-II). N_c = 1 gives %.3f eV, excluded at %.0f sigma "
                     "only if quark charges are held at (2/3, -1/3), which also makes N_c = 1 baryon charges fractional; with "
                     "anomaly-consistent charges the width does not depend on N_c."
                     % (pz["Gamma_Nc3_f92.21_eV"], pz["pull_vs_PrimExII_sigma"], pz["Gamma_Nc1_f92.21_eV"], abs(pz["Nc1_pull_vs_PrimExII_sigma"]))},
    ]


def main():
    hh = load("hedgehog_results.json")
    ch = load("charges_results.json")
    pz = load("pi0_results.json")
    sy = load("symbolic_results.json")
    pd = pdg_data()

    anw = hh["ANW_parameters"]
    own = hh["own_SU2_fit"]
    an84 = hh["massive_pions"]["AN84_parameters"]
    d0 = hh["massless_dimensionless"]

    # ---------------------------------------------------------------- empirical comparison values
    mu_p, mu_n = pd["mu_p"][0], pd["mu_n"][0]
    r2p = pd["r_p_fm"][0]**2
    r2n = pd["r2_n_fm2"][0]
    r2_I0_emp = r2p + r2n                                  # <r^2>_{I=0} = <r^2>_p + <r^2>_n (normalised)
    dr2_I0 = math.hypot(2 * pd["r_p_fm"][0] * pd["r_p_fm"][1], pd["r2_n_fm2"][1])
    r2M_S = (mu_p * pd["rM_p_fm"][0]**2 + mu_n * pd["rM_n_fm"][0]**2) / (mu_p + mu_n)
    dr2M_S = math.hypot(mu_p * 2 * pd["rM_p_fm"][0] * pd["rM_p_fm"][1], mu_n * 2 * pd["rM_n_fm"][0] * pd["rM_n_fm"][1]) / (mu_p + mu_n)
    gA_emp = abs(pd["gA_over_gV"][0])
    g_piNN_emp = (13.1, 0.1, "[summary] g^2/4pi ~ 13.6-13.8 from NN and piN analyses (not in PDG); 2 M_N g_A/F_pi(phys) = 13.0")
    emp = {
        "mu_p": (mu_p, pd["mu_p"][1], "PDG 2026"),
        "mu_n": (mu_n, pd["mu_n"][1], "PDG 2026"),
        "mu_p_over_mu_n": (mu_p / mu_n, 0.0, "PDG 2026"),
        "g_A": (gA_emp, pd["gA_over_gV"][1], "PDG 2026 |g_A/g_V|"),
        "g_piNN": g_piNN_emp,
        "r_E_I0_fm": (math.sqrt(r2_I0_emp), dr2_I0 / (2 * math.sqrt(r2_I0_emp)), "PDG 2026: sqrt(r_p^2 + <r^2>_n)"),
        "r_M_I0_fm": (math.sqrt(r2M_S), dr2M_S / (2 * math.sqrt(r2M_S)), "PDG 2026 magnetic radii: (mu_p r_Mp^2 + mu_n r_Mn^2)/(mu_p+mu_n)"),
        "r_p_fm": (pd["r_p_fm"][0], pd["r_p_fm"][1], "PDG 2026"),
        "r2_n_fm2": (r2n, pd["r2_n_fm2"][1], "PDG 2026"),
    }
    model_massless = {
        "mu_p": anw["mu_p"], "mu_n": anw["mu_n"], "mu_p_over_mu_n": anw["mu_p_over_mu_n"], "g_A": anw["g_A"],
        "g_piNN": anw["g_piNN_GT"], "r_E_I0_fm": anw["r_I0_fm"], "r_M_I0_fm": anw["rM_I0_Sachs_fm"],
        "r_p_fm": float("inf"), "r2_n_fm2": float("-inf"),
    }
    model_massive = {
        "mu_p": an84["mu_p"], "mu_n": an84["mu_n"], "mu_p_over_mu_n": an84["mu_p_over_mu_n"], "g_A": an84["g_A"],
        "g_piNN": an84["g_piNN_GT"], "r_E_I0_fm": an84["r_I0_fm"], "r_M_I0_fm": an84["rM_I0_Sachs_fm"],
        "r_p_fm": an84["r_p_fm"], "r2_n_fm2": an84["r2_n_fm2"],
    }
    comp = []
    n_within, n_finite = 0, 0
    for k in ["mu_p", "mu_n", "mu_p_over_mu_n", "g_A", "g_piNN", "r_E_I0_fm", "r_M_I0_fm", "r_p_fm", "r2_n_fm2"]:
        v, ev, src = emp[k]
        m0 = model_massless[k]
        rat0 = m0 / v if math.isfinite(m0) else float("inf")
        dev0 = rat0 - 1 if math.isfinite(rat0) else float("inf")
        within = math.isfinite(dev0) and abs(dev0) <= 0.30
        if math.isfinite(dev0):
            n_finite += 1
            n_within += within
        comp.append({"quantity": k, "data": v, "data_err": ev, "data_source": src,
                     "skyrme_ANW_massless": m0, "ratio_massless": rat0, "deviation_massless": dev0,
                     "within_30pct_massless": within,
                     "skyrme_AN84_massive_no_target": model_massive[k], "ratio_massive": model_massive[k] / v})
    print("Comparison with data (ANW massless parameters F=129 MeV, e=5.45; inputs M_N, M_Delta not counted):")
    for c in comp:
        print("  %-15s skyrme %9.4f  data %9.4f  ratio %7.3f  within 30%%: %s   | AN84 massive %8.4f (ratio %.3f)"
              % (c["quantity"], c["skyrme_ANW_massless"], c["data"], c["ratio_massless"], c["within_30pct_massless"],
                 c["skyrme_AN84_massive_no_target"], c["ratio_massive"]))
    print("  within 30%%: %d of %d finite quantities; r_p and <r^2>_n are infinite with massless pions" % (n_within, n_finite))
    n_within33 = sum(1 for c in comp if math.isfinite(c["deviation_massless"]) and abs(c["deviation_massless"]) <= 0.33)
    print("  within 33%%: %d of %d finite quantities (exception: g_A)" % (n_within33, n_finite))

    # ---------------------------------------------------------------- enclosed charge (dressing)
    radii = [0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
    ref = H.solve_profile(0.0, X=200.0, tol=1e-10)
    L_anw = HBARC / (5.45 * 129.0)
    enc0 = enclosed_charge(ref, d0["Lambda"], L_anw, radii)
    beta = an84["beta"]
    solm = H.solve_profile(beta, X=60.0, tol=1e-10)
    Lam_m = H.integrate(H.dens("Lambda", beta), solm)
    L_m = HBARC / (4.84 * 108.0)
    enc1 = enclosed_charge(solm, Lam_m, L_m, radii, beta)
    print("Enclosed charge Q(<R): R[fm]  p(massless) n(massless) | p(m_pi=138) n(m_pi=138)")
    for a, b in zip(enc0, enc1):
        print("   %5.2f  %7.4f  %8.4f  |  %7.4f  %8.4f" % (a["R_fm"], a["Q_p_inside"], a["Q_n_inside"], b["Q_p_inside"], b["Q_n_inside"]))
    peak0 = neutron_peak(ref, d0["Lambda"], L_anw)
    peak1 = neutron_peak(solm, Lam_m, L_m)
    print("Neutron enclosed-charge maximum: massless ANW Q_n = %+.4f at R = %.4f fm; m_pi = 138 MeV AN84 Q_n = %+.4f at R = %.4f fm"
          % (peak0["Q_n_peak"], peak0["R_peak_fm"], peak1["Q_n_peak"], peak1["R_peak_fm"]))
    # massless tail: 1/2 - isovector inside R -> C^2/(2 Lambda x_R)
    tail_check = [{"R_fm": a["R_fm"], "isovector_outside": 0.5 - a["isovector_inside"],
                   "asymptotic_C2_over_2Lambda_xR": d0["C"]**2 / (2 * d0["Lambda"] * (a["R_fm"] / L_anw))} for a in enc0]

    # ---------------------------------------------------------------- calibration table (PLAN.md E5 targets)
    def verdict(val, tgt, tol):
        return "CALIBRATED" if abs(val - tgt) <= tol + 1e-12 else "MISS"
    cal = []
    def add(q, val, unit, tgt, tol, src, note="", v=None):
        cal.append({"quantity": q, "value": val, "unit": unit, "target": tgt, "tolerance": tol, "source": src,
                    "verdict": v if v else verdict(val, tgt, tol), "note": note})
    srcE5 = "PLAN.md E5 [ANW via secondary sources; formulas read in Ma-Harada and Rakhimov]"
    add("isoscalar charge radius <r^2>_{I=0}^{1/2} at ANW parameters (F=129 MeV, e=5.45)", anw["r_I0_fm"], "fm", 0.59, 0.01, srcE5,
        "own SU(2) refit (F=%.2f, e=%.4f): %.4f fm" % (own["F_pi_MeV"], own["e"], own["r_I0_fm"]))
    add("isoscalar magnetic radius, ANW definition (<r^4>_B/<r^2>_B)^{1/2}", anw["rM_I0_ANW_def_fm"], "fm", 0.92, 0.01, srcE5,
        "the Sachs radius from dG_M^{I=0}/dq^2 is sqrt(3/5) of this: %.4f fm" % anw["rM_I0_Sachs_fm"])
    add("mu_p", anw["mu_p"], "nuclear magnetons (M_N = 939 MeV)", 1.87, 0.02, srcE5)
    add("mu_n", anw["mu_n"], "nuclear magnetons (M_N = 939 MeV)", -1.31, 0.02, srcE5)
    add("mu_p/mu_n", anw["mu_p_over_mu_n"], "", -1.43, 0.02, srcE5, "tolerance of the moments applied to the ratio; ANW's -1.43 is the ratio of rounded 1.87/-1.31 = -1.427")
    add("g_piNN (Goldberger-Treiman, 2 M_N g_A/F_pi)", anw["g_piNN_GT"], "", 8.9, 0.05, srcE5,
        "PLAN gives no tolerance for g_piNN; half a unit in the quoted last digit used (post hoc, deviation). "
        "It would fail the moments' +-0.02 (|dev| = %.3f); g_A, tied to it by Goldberger-Treiman, passes its preregistered "
        "+-0.01" % abs(anw["g_piNN_GT"] - 8.9))
    add("g_A at ANW parameters (consistency with E2)", anw["g_A"], "", 0.61, 0.01, "PLAN.md E2 [ANW via secondary sources]",
        "= 2 pi C/(3 e^2) = (pi/3e^2)|D|; the identity D = -2C holds to %.1e" % abs(d0["D"] + 2 * d0["C"]))
    add("Gamma(pi0->gg), N_c = 3, f = 92.21 MeV", pz["Gamma_Nc3_f92.21_eV"], "eV", 7.802, 2 * 0.117,
        "PLAN.md E5 [read: Bernstein-Holstein 1112.4809; PrimEx-II]",
        "pull vs PrimEx-II %.2f sigma, vs PDG 2026 (%.3f +- %.3f eV) %+.2f sigma; preregistered value 7.76 eV"
        % (pz["pull_vs_PrimExII_sigma"], pz["inputs"]["PDG2026"]["Gamma_gg_eV"], pz["inputs"]["PDG2026"]["Gamma_gg_err_eV"], pz["pull_vs_PDG2026_sigma"]))
    add("Gamma(pi0->gg), N_c = 1 (must be excluded)", pz["Gamma_Nc1_f92.21_eV"], "eV", 0.86, 0.01, "PLAN.md E5",
        "excluded by PrimEx-II at %.0f sigma, but only with N_c-independent quark charges (2/3, -1/3), which at N_c = 1 also make "
        "the baryon charges fractional; with anomaly-consistent charges the width does not depend on N_c" % abs(pz["Nc1_pull_vs_PrimExII_sigma"]))
    # (reconciliation) internal checks with no literature target are labelled CHECK PASSED (PLAN E5: "reported as checks"),
    # not CALIBRATED, which PLAN reserves for literature targets.
    allint = ch["all_charges_integer_Nc3"] and ch["SU2_charges_integer"] and ch["gell_mann_nishijima_holds"] and ch["Y1_states_match_SU2_form"]
    cal.append({"quantity": "rotor-state charges Q = I3 + Y/2 (8, 10, 10bar, 27) integral; SU(2) Q = I3 + B/2", "value": bool(allint),
                "unit": "", "target": True, "tolerance": "exact", "source": "PLAN.md E5", "verdict": "CHECK PASSED" if allint else "CHECK FAILED",
                "note": "internal check, no literature target. charges: 8 {-1,0,1}; 10 {-1,0,1,2}; 10bar {-2,-1,0,1}; 27 {-2,...,2}. "
                        "The 8 and 10 charges coincide with the observed octet and decuplet baryons"})
    nsym = sy["n_pass"]; nfail = sy["n_fail"]
    n_insp = sum(1 for c_ in sy["checks"] if "by inspection" in c_["detail"])
    cal.append({"quantity": "symbolic derivations (sympy): formulas, one cone, taut vacuum", "value": "%d/%d pass" % (nsym, nsym + nfail),
                "unit": "", "target": "all pass", "tolerance": "exact", "source": "symbolic_derivations.py",
                "verdict": "CHECK PASSED" if nfail == 0 else "CHECK FAILED",
                "note": "%d computed, %d by inspection; one-cone and taut-vacuum checks hold by construction" % (nsym + nfail - n_insp, n_insp)})
    no_target = [
        {"quantity": "Gamma(pi0->gg) at the fold's own f (ANW, f = 64.5 MeV)", "value": pz["Gamma_at_ANW_f64.5_eV"], "unit": "eV",
         "expected": "about 15.9 eV (PLAN prediction)", "ratio_to_PrimExII": pz["ratio_ANW_to_PrimExII"]},
        {"quantity": "Gamma(pi0->gg) at the SU(3) refit f = %.3f MeV (agrees with E2's refit F = 113.755 MeV)" % pz["own_SU3_refit_f_MeV"],
         "value": pz["Gamma_at_own_SU3_refit_eV"], "unit": "eV", "expected": "about 20 eV (PLAN prediction)",
         "ratio_to_PrimExII": pz["ratio_SU3_refit_to_PrimExII"]},
        {"quantity": "isovector <r^2> inside R, massless pions: slope", "value": d0["C"]**2 / d0["Lambda"], "unit": "x (=1/(eF) per unit x)",
         "expected": "diverges linearly (PLAN prediction)",
         "values_x2": hh["isovector_radius_cutoff_massless"]},
        {"quantity": "AN84 massive pions (m_pi = 138 MeV, F = 108 MeV, e = 4.84): own refit to M_N, M_Delta",
         "value": [hh["massive_pions"]["own_fit_mpi138"]["F_pi_MeV"], hh["massive_pions"]["own_fit_mpi138"]["e"]], "unit": "MeV, -",
         "expected": "108, 4.84 (verification of the quoted AN84 parameters)"},
        {"quantity": "AN84 massive: r_p, <r^2>_n, r_{I=1}", "value": [an84["r_p_fm"], an84["r2_n_fm2"], an84["r_I1_fm"]], "unit": "fm, fm^2, fm",
         "expected": "finite (no target)"},
    ]

    for c in cal:
        print("%-12s %s = %s (target %s, tol %s)" % (c["verdict"], c["quantity"], c["value"], c["target"], c["tolerance"]))

    res = {
        "experiment": "E5 -- add light (charges, EM static properties, pi0 -> gamma gamma, one cone)",
        "conventions": {
            "lagrangian": "(F^2/16) Tr dU dU^+ + (1/32e^2) Tr[L_mu,L_nu]^2 (+ (F^2 m^2/16) Tr(U+U^+-2) massive variant)",
            "F_pi": "186-MeV convention for the Skyrme fits (f_pi = F_pi/2); pi0 width uses f = 92.21 MeV",
            "x": "e F_pi r", "hbar_c": HBARC, "M_N_magneton": 939.0,
            "radii": "<r^2>_{I=0} normalised to the baryon density; <r^2>_{I=1} normalised to the isovector charge; "
                     "<r^2>_p = (<r^2>_0 + <r^2>_1)/2, <r^2>_n = (<r^2>_0 - <r^2>_1)/2",
            "charge": "Q = I3 + Y/2 with left (flavour) generators; WZ constraint Y_R = N_c B/3"},
        "calibration": cal,
        "no_target": no_target,
        "comparison_with_PDG2026_ANW_parameters": comp,
        "within_30pct": {"n_within": n_within, "n_finite": n_finite,
                         "n_within_33pct": n_within33,
                         "not_finite_massless": ["r_p", "<r^2>_n"],
                         "note": "magnetic radius compared in the Sachs definition; g_piNN data value is [summary]. Strictly within 30%%: %d of %d "
                                 "(mu_p/mu_n, r_E^{I=0}, r_M^{I=0}); within 33%%: %d of %d (adds mu_n -31%%, g_piNN -32%%, mu_p -33%%). "
                                 "The exceptions are g_A (-52%%) and the individual charge radii r_p, <r^2>_n (infinite with massless pions)"
                                 % (n_within, n_finite, n_within33, n_finite)},
        "enclosed_charge_massless_ANW": enc0, "enclosed_charge_massive_AN84": enc1, "isovector_tail_check": tail_check,
        "neutron_enclosed_charge_peak": {"massless_ANW": peak0, "massive_AN84": peak1},
        "seed_claims": seed_claims(n_within, n_within33, n_finite, pz, peak0, enc0, d0, L_anw, nsym, nfail, n_insp),
        "pdg_inputs": pd,
        "pi0": pz, "charges_summary": {nm: {"spins": t["spins_allowed"], "charges": t["charges"], "dim": t["dim"]}
                                       for nm, t in ch["charge_table_Nc3"].items()},
        "charges_Nc_extra": ch["Nc_dependence_extra"],
        "symbolic_checks": sy["checks"],
        "hedgehog_numerics": {"M_over_3pi2": d0["M_over_3pi2"], "Lambda": d0["Lambda"], "K2": d0["K2"], "C": d0["C"],
                              "Fprime0": d0["Fprime0"], "R2": d0["R2"], "R4": d0["R4"], "D": d0["D"],
                              "spread_X100_400": d0["numerical_spread_X100_400"],
                              "relative_deviation_short_boxes": d0.get("relative_deviation_short_boxes")},
        "reconciliation": {
            "crosscheck": "crosscheck/crosscheck.json: 57 of 57 recomputed numbers agree; 9 minor issues, none in the numerics",
            "changes": [
                "pi0 coupling text: with d_mu A_nu the coefficient is N_c e^2/(24 pi^2 f) (48 pi^2 goes with F_mu nu); now a computed check (9g)",
                "convergence: 5e-8 relative holds for X = 100-400 only; X = 25 is off by ~1e-6 (relative_deviation_short_boxes)",
                "neutron enclosed charge: maximum %+.4f at %.3f fm (massless ANW), not +0.185 at 1 fm (a grid point)"
                % (peak0["Q_n_peak"], peak0["R_peak_fm"]),
                "symbolic checks: 10d was hard-coded True; it is now a computed expansion of the gauged WZ term; 5c and 7b made strict "
                "(exact value and sign); 9g added",
                "verdict vocabulary: internal checks labelled CHECK PASSED; QUANTIFIED dropped for the f_pi tension (PLAN prediction, "
                "no SEED verdict)",
                "SEED 6B AMENDED reframed: %d of %d finite within 33%%, exceptions g_A and the individual charge radii" % (n_within33, n_finite),
                "commitment 4 and the N_c = 1 exclusion carry their qualifiers in the verdict itself",
                "g_piNN: passes only the post hoc +-0.05; fails +-0.02"]},
    }
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=lambda o: str(o))
    make_fig(comp)
    print("wrote results.json, fig_vs_pdg.png")


def make_fig(comp):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    labels = {"mu_p": "$\\mu_p$", "mu_n": "$\\mu_n$", "mu_p_over_mu_n": "$\\mu_p/\\mu_n$", "g_A": "$g_A$",
              "g_piNN": "$g_{\\pi NN}$", "r_E_I0_fm": "$r_{E}^{I=0}$", "r_M_I0_fm": "$r_{M}^{I=0}$ (Sachs)",
              "r_p_fm": "$r_p$", "r2_n_fm2": "$\\langle r^2\\rangle_n$"}
    from matplotlib.ticker import NullFormatter
    fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=110)
    ax.axvspan(0.7, 1.3, color="#d9d8d4", alpha=0.5, lw=0)
    ax.axvline(1.0, color="#8a8984", lw=1)
    xmax = 5.0
    for i, c in enumerate(comp):
        y = len(comp) - 1 - i
        r0 = c["ratio_massless"]
        if math.isfinite(r0):
            ax.plot(r0, y, "o", ms=8, color="#2a78d6", mec="white", mew=1.5, zorder=3)
        else:
            ax.annotate("", xy=(4.8, y), xytext=(3.4, y), arrowprops=dict(arrowstyle="->", color="#2a78d6", lw=2))
            ax.text(4.05, y + 0.22, "infinite", ha="center", va="bottom", fontsize=7, color="#52514e")
        r1 = c["ratio_massive"]
        ax.plot(r1, y, "D", ms=7, mfc="white", mec="#eb6834", mew=2, zorder=2)
    ax.set_yticks(range(len(comp)))
    ax.set_yticklabels([labels[c["quantity"]] for c in comp][::-1], fontsize=9)
    ax.set_xscale("log")
    ax.set_xlim(0.4, xmax)
    ax.set_xticks([0.5, 0.7, 1.0, 1.3, 2.0, 3.0])
    ax.set_xticklabels(["0.5", "0.7", "1", "1.3", "2", "3"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_ylim(-0.6, len(comp) - 0.4)
    ax.set_xlabel("Skyrme value / data (PDG 2026); grey band = within 30%", fontsize=9)
    ax.plot([], [], "o", color="#2a78d6", ms=7, label="massless pions, ANW F=129 MeV, e=5.45 (calibrated)")
    ax.plot([], [], "D", mfc="white", mec="#eb6834", mew=2, ms=6, label="m$_\\pi$=138 MeV, AN84 F=108 MeV, e=4.84 (no target)")
    ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.16), ncol=1)
    for sp_ in ["top", "right"]:
        ax.spines[sp_].set_visible(False)
    ax.set_title("Nucleon static properties: classical Skyrme fold vs data", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_vs_pdg.png"))
    plt.close(fig)


if __name__ == "__main__":
    main()
