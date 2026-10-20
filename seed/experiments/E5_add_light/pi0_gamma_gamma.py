#!/usr/bin/env python3
"""
E5: pi0 -> gamma gamma from the gauged Wess-Zumino term, evaluated.

Formula (derived in symbolic_derivations.py, section 9, from Bernstein-Holstein eq. 67 / Witten 1983):
    Gamma = alpha^2 m^3 N_c^2 / (576 pi^3 f^2)      [quark charges (2/3, -1/3), f in the 92-MeV convention]
Inputs: alpha = 1/137.035999177 (CODATA 2022), m_pi0 from PDG 2026, f = 92.21 MeV (PDG 2010 value used by
Bernstein-Holstein; preregistered). Data: PrimEx-II 7.802 +- 0.117 eV; PDG 2026 Gamma(gg) = hbar BR/tau.
Then the same formula at the Skyrme fold's own fitted f (ANW: F = 129 MeV -> f = 64.5 MeV; own SU(3) refit
from hedgehog_results.json, or recomputed). Writes pi0_results.json.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
ALPHA = 1 / 137.035999177
HBAR_MeV_s = 6.582119569e-22


def width_eV(f_MeV, Nc=3, m=134.9768, alpha=ALPHA):
    return alpha**2 * m**3 * Nc**2 / (576 * math.pi**3 * f_MeV**2) * 1e6


def pdg_values():
    try:
        import pdg
        api = pdg.connect()
        tau = api.get("S009T").summary_values()[0]
        br = api.get("S009.1").summary_values()[0]
        mpi = api.get("S009M").summary_values()[0]
        G = HBAR_MeV_s / tau.value * br.value * 1e6
        dG = G * math.sqrt((tau.error_positive / tau.value)**2 + (br.error_positive / br.value)**2)
        return {"tau_s": tau.value, "tau_err_s": tau.error_positive, "BR_gg": br.value, "BR_err": br.error_positive,
                "m_pi0_MeV": mpi.value, "Gamma_gg_eV": G, "Gamma_gg_err_eV": dG, "source": "PDG 2026 sqlite (pdg package)"}
    except Exception as ex:
        return {"m_pi0_MeV": 134.9768, "Gamma_gg_eV": 7.72, "Gamma_gg_err_eV": 0.12,
                "source": "fallback values from PLAN.md (pdg package unavailable: %s)" % ex}


def su3_refit_f():
    p = os.path.join(HERE, "hedgehog_results.json")
    if os.path.exists(p):
        h = json.load(open(p))
        return h["own_SU3_fit"]["f_pi_MeV"], h["own_SU2_fit"]["f_pi_MeV"], "hedgehog_results.json"
    import hedgehog_em as H
    sol = H.solve_profile(0.0, X=200.0)
    d = H.static_dimensionless(sol)
    m = H.pdg_masses()
    F3, e3, _, _ = H.fit_su3(d, sum(m["octet"]) / 8, sum(m["decuplet"]) / 10)
    F2, e2 = H.fit_su2(d)
    return F3 / 2, F2 / 2, "recomputed"


def main():
    pd = pdg_values()
    m = pd["m_pi0_MeV"]
    primex, dprimex = 7.802, 0.117
    G3 = width_eV(92.21, 3, m)
    G1 = width_eV(92.21, 1, m)
    f3, f2, src = su3_refit_f()
    out = {
        "formula": "Gamma = alpha^2 m^3 N_c^2/(576 pi^3 f^2)",
        "inputs": {"alpha": ALPHA, "m_pi0_MeV": m, "f_MeV": 92.21, "PrimExII_eV": [primex, dprimex], "PDG2026": pd},
        "Gamma_Nc3_f92.21_eV": G3,
        "Gamma_Nc1_f92.21_eV": G1,
        "pull_vs_PrimExII_sigma": (G3 - primex) / dprimex,
        "pull_vs_PDG2026_sigma": (G3 - pd["Gamma_gg_eV"]) / pd["Gamma_gg_err_eV"],
        "Nc1_pull_vs_PrimExII_sigma": (G1 - primex) / dprimex,
        "f_needed_for_PrimExII_central_MeV": 92.21 * math.sqrt(G3 / primex),
        "Gamma_at_ANW_f64.5_eV": width_eV(64.5, 3, m),
        "ratio_ANW_to_PrimExII": width_eV(64.5, 3, m) / primex,
        "own_SU2_fit_f_MeV": f2, "Gamma_at_own_SU2_fit_eV": width_eV(f2, 3, m),
        "own_SU3_refit_f_MeV": f3, "Gamma_at_own_SU3_refit_eV": width_eV(f3, 3, m),
        "ratio_SU3_refit_to_PrimExII": width_eV(f3, 3, m) / primex,
        "f_source": src,
        "caveat_Nc": "N_c^2 scaling assumes N_c-independent quark charges (2/3,-1/3). With anomaly-consistent charges "
                     "Q = diag(1/2+1/2N_c, -1/2+1/2N_c) the amplitude factor N_c Tr(Q^2 tau3) = 1 for every N_c "
                     "(symbolic check 9f; Baer & Wiese hep-ph/0105258), so pi0 -> gg alone does not count colours.",
    }
    for k, v in out.items():
        if isinstance(v, float):
            print("%-36s %.4f" % (k, v))
    print("PDG 2026 Gamma(gg) = %.3f +- %.3f eV" % (pd["Gamma_gg_eV"], pd["Gamma_gg_err_eV"]))
    ok = abs(out["pull_vs_PrimExII_sigma"]) < 2 and abs(out["Nc1_pull_vs_PrimExII_sigma"]) > 5
    print("preregistered pass (LO within 2 sigma of PrimEx-II, N_c=1 excluded):", ok)
    out["pass"] = ok
    with open(os.path.join(HERE, "pi0_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
