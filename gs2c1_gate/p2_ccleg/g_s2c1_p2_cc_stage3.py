#!/usr/bin/env python3
# g_s2c1_p2_cc_stage3.py — CC leg phases 3-4: structure check, a4_agg, falsifiers, arms, checkpoint (p2_cmp_v1).
# Arms are decided HERE, before any QUARANTINE/ artifact is opened.
import json, hashlib, math
import numpy as np
from mpmath import mp, mpf

mp.dps = 30
TAU_AGG = 1e-6
PREREG_MD5 = "2ea8ec13ffa3c32898cc24a3be605c64"
ADDENDA = {"P2": "2feff442dfd08a379443d893b8c7761b", "P2A": "71b4c7010e48601e07f6458c711dfb4a"}

ph1 = json.load(open("cc_p2_phase1.json"))
ph2 = json.load(open("cc_p2_phase2.json"))
xchk = json.load(open("cc_p2_pv_xcheck.json"))

def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

def fit(ks, R, powers, logs=()):
    cols = [ks**p for p in powers] + [ks**p * np.log(ks) for p in logs]
    A = np.vstack(cols).T
    coef, *_ = np.linalg.lstsq(A, R, rcond=None)
    resid = R - A @ coef
    return coef, float(np.sqrt(np.mean(resid**2)))

phase3, phase4, per_sub = {}, {}, {}
uni = []
for name in ("step_hex", "gem8_hex", "step_cubic", "gem8_cubic"):
    d1, d2 = ph1[name], ph2[name]
    D2T = d1["D2_analytic"]["T"]
    D2L = d1["D2_analytic"]["L"]
    ks = np.array([float(x) for x in d2["T"]["k"]])
    Delta = [mpf(s) for s in d2["T"]["Delta"]]
    R = np.array([float(dl - mpf(repr(D2T)) * mpf(repr(float(k))) ** 2) for dl, k in zip(Delta, ks)])
    # (i) pure even basis {k^4, k^6, k^8}
    c_even, rms_even = fit(ks, R, (4, 6, 8))
    # (ii) rejected alternative {k^3, k^4}
    c_odd, rms_odd = fit(ks, R, (3, 4))
    # (iii) rejected alternative {k^4, k^4 ln k}
    c_log, rms_log = fit(ks, R, (4,), logs=(4,))
    a4, a6, a8 = (float(x) for x in c_even)
    small = [
        float(abs(dl / mpf(repr(float(k))) ** 2 - mpf(repr(D2T)) - mpf(repr(a4)) * mpf(repr(float(k))) ** 2) / abs(mpf(repr(D2T))))
        for dl, k in zip(Delta, ks) if k <= 0.005
    ]
    smallk = max(small)
    # D0 anchor: closed form vs mp ladder D0
    d0_rel = abs(d1["D0"]["T"] - d2["T"]["D0_mp"]) / abs(d1["D0"]["T"])
    # L-channel small-k control: Delta_L/k^2 -> D2_L
    kL = d2["L"]["k"]
    dL = [mpf(s) for s in d2["L"]["Delta"]]
    j = kL.index(0.0046875)
    a2L_ladder = float(dL[j] / mpf(repr(kL[j])) ** 2 - mpf(repr(d2["L"].get("a4L", 0))))
    a2L_ladder_rel = abs(a2L_ladder - D2L) / abs(D2L)  # includes O(k^2) truncation ~ a4L*k^2/D2L
    structure_ok = bool(rms_even <= 1e-7 and rms_even < rms_odd and rms_even < rms_log)
    CI = max(d1["xi_doubling"]["D2_T_rel"], xchk[name]["max_rel_change"])
    CI_abs = CI * abs(D2T)
    disp = bool(abs(D2T) > max(TAU_AGG, CI_abs))
    fconv = bool(
        d1["xi_doubling"]["D2_T_rel"] <= 1e-6 and d1["xi_doubling"]["Q_T_rel"] <= 1e-9
        and xchk[name]["max_rel_change"] <= 1e-9 and xchk[name]["eps_richardson_rel"] <= 1e-6
    )
    fL = bool(abs(d1["D0"]["L"]) > TAU_AGG and abs(D2L) > max(TAU_AGG, CI * abs(D2L)) and a2L_ladder_rel <= 1e-2)
    if disp:
        arm = "A3-agg DISPERSIVE (grain-scale k^2)"
    elif abs(a4) > TAU_AGG:
        arm = "A2-agg"
    else:
        arm = "A1-agg"
    phase3[name] = {
        "ladder_k": list(ks), "Delta": [str(x) for x in Delta], "R_even_resid_rms": rms_even,
        "even_fit": {"a4": a4, "a6": a6, "a8": a8, "rms": rms_even},
        "alt_odd_fit": {"a3": float(c_odd[0]), "a4": float(c_odd[1]), "rms": rms_odd},
        "alt_log_fit": {"a4": float(c_log[0]), "a4log": float(c_log[1]), "rms": rms_log},
        "basis_selected": "pure even {k4,k6,k8}" if structure_ok else "AMBIGUOUS",
        "rms_ratio_odd_over_even": rms_odd / rms_even, "rms_ratio_log_over_even": rms_log / rms_even,
        "smallk_confirmation_rel": smallk, "D0_closed_vs_ladder_rel": d0_rel,
        "a2L_ladder_estimate": a2L_ladder, "a2L_ladder_vs_analytic_rel": a2L_ladder_rel,
    }
    phase4[name] = {
        "F_AGG_PIN_pass": d1["pin"]["pin_pass"], "F_AGG_KK_pass": d1["KK"]["pass"],
        "F_AGG_DISP_pass": disp, "F_AGG_L_pass": fL, "F_CONV_pass": fconv,
        "structure_no_odd_or_log_term": structure_ok,
        "a2_agg_of_record": D2T, "a2_L": D2L, "a4_agg": a4, "a6": a6,
        "CI_quadrature": CI_abs, "CI_quadrature_rel": CI, "tau_agg": TAU_AGG,
        "mechanical_arm_P2A": arm,
    }
    per_sub[name] = {
        "C1_pin": {"Q_T_a": d1["pin"]["Q_T_a"], "V_T": d1["pin"]["V_T"], "V_L": d1["pin"]["V_L"],
                   "pin_pass": d1["pin"]["pin_pass"]},
        "C2_KK": {"alpha_tie_max_rel": d1["KK"]["alpha_tie_max_rel"], "pass": d1["KK"]["pass"]},
        "C3_D0": {"T": d1["D0"]["T"], "L": d1["D0"]["L"]},
        "C4_a2_agg": {"T_analytic": D2T, "L_analytic": D2L, "CI_quadrature_rel": CI},
        "C5_a4_agg": {"T_even_basis": a4, "T_a6": a6, "even_basis_rms": rms_even,
                      "smallk_confirmation_rel": smallk},
        "C6_controls": {"F_AGG_DISP_pass": disp, "F_AGG_L_pass": fL, "F_CONV_pass": fconv,
                        "structure_no_odd_or_log_term": structure_ok},
        "C7_arm": arm,
        "a2_over_QT": D2T / d1["pin"]["Q_T_a"],
        "a2L_over_a2T": D2L / D2T,
    }
    uni.append(D2T / d1["pin"]["Q_T_a"])
    print(name, "a4 %.6e a6 %.6e rms_even %.2e rms_odd %.2e rms_log %.2e smallk %.2e arm %s"
          % (a4, a6, rms_even, rms_odd, rms_log, smallk, arm))

spread = (max(uni) - min(uni)) / abs(sum(uni) / 4)
json.dump(phase3, open("cc_p2_phase3.json", "w"), indent=1, sort_keys=True)
json.dump(phase4, open("cc_p2_phase4.json", "w"), indent=1, sort_keys=True)

checkpoint = {
    "schema": "p2_cmp_v1", "gate": "G-S2C1", "phase": "3 / P2 — CC leg", "leg": "cc",
    "prereg_md5": PREREG_MD5, "addenda_md5": ADDENDA,
    "source_md5": {
        "poly_vrh_results": md5("poly_vrh_results.json"),
        "poly1_phase1full_cc": md5("poly1_phase1full_cc.json"),
        "cc_p2_phase0": md5("cc_p2_phase0.json"), "cc_p2_phase1": md5("cc_p2_phase1.json"),
        "cc_p2_phase2": md5("cc_p2_phase2.json"), "cc_p2_pv_xcheck": md5("cc_p2_pv_xcheck.json"),
        "instrument": md5("g_s2c1_p2_cc_instrument.py"),
    },
    "election_E_P2_1": "(a) the aggregate S2 channel = the polarization-averaged transverse shear cone (full SO(3) grain average; projector 1/2(I - p p), scattered T+L summed)",
    "shared_layer_flagged": "Xi and Phi_TM rebuilt from scratch by this leg (ZYZ uniform x Gauss-Legendre SO(3) product quadrature, exact at l=8, doubled as control; kernels extracted as exact even mu-polynomials; closed-form mu-integrals). Re Sigma via series-closed-form F + exact pole-extraction PV in mpmath (dps 30), epsilon-regularized Richardson cross-check — method differs from the chat leg's Cauchy-weight PV quadrature + regular tail.",
    "per_substrate": per_sub,
    "F_AGG_UNI": {"a2_over_QT": {n: per_sub[n]["a2_over_QT"] for n in per_sub}, "a2_over_QT_spread_rel": spread},
}
with open("s2c1_p2_cc_cmp_checkpoint.json", "w") as f:
    json.dump(checkpoint, f, indent=1, sort_keys=True)
print("F-AGG-UNI spread_rel %.3e" % spread)
print("checkpoint md5", md5("s2c1_p2_cc_cmp_checkpoint.json"))
