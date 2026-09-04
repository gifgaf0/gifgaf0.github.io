#!/usr/bin/env python3
# cc_s9_fingerprint.py — G-S2C1 S9 fingerprint (post-hash, quarantine legitimately open).
# Reproduces the mechanism analysis for the three comparator MISSes. No re-tuning: no CC
# quantity is recomputed or altered; the CC checkpoint of record is the pre-decode commit.
import json
import numpy as np
import s2c1_cc_core as core

A = core.A_STAR
COMMON = [0.3, 0.15, 0.075, 0.0375]


def joint_fit(ka_arr, y):
    x = np.asarray(ka_arr) ** 2
    V = np.vstack([np.ones_like(x), x, x * x]).T
    p, *_ = np.linalg.lstsq(V, np.asarray(y), rcond=None)
    return float(p[0]), float(p[1] / p[0]), float(p[2] / p[0])


def main():
    chat_lad = json.load(open("QUARANTINE/g_s2c1_phase1_ladder_checkpoint.json"))
    chat_cp = json.load(open("QUARANTINE/s2c1_chat_cmp_checkpoint.json"))
    mine = json.load(open("cc_phase3_40.json"))
    out = {}

    # F-S9-1: kernel_U0 — key semantics, not substrate
    u0 = float(core.uhat_radial(np.array([0.0]))[0])
    out["F_S9_1_kernel_U0"] = {
        "chat_kernel_U0": chat_cp["C1_substrate"]["kernel_U0"],
        "cc_kernel_U0_reported": 20.0,
        "cc_Uhat_at_q0": u0,
        "rel_diff_Uhat0": abs(u0 - chat_cp["C1_substrate"]["kernel_U0"]) / u0,
        "mechanism": "schema key semantics: chat reported the q=0 kernel transform Uhat(0) "
                     "under kernel_U0; CC reported the real-space amplitude U0=20 (g_star "
                     "agrees identically at 20.0). The independent CC Hankel quadrature "
                     "reproduces the chat Uhat(0) to 3.1e-13 relative: substrates identical.",
    }

    # F-S9-2/3: a4 — fitter equivalence + rung-level shape difference
    fp = {}
    for tag in ("GK", "GM"):
        blk = chat_lad["step3_ladder"]["runs"]["40"]["T"][tag]
        ka = np.array(blk["ka"])
        r = np.array(blk["r"])
        idx = [int(np.argmin(np.abs(ka - c))) for c in COMMON]
        y_chat = 1.0 + r[idx]
        _, a2c, a4c = joint_fit(COMMON, y_chat)
        y_mine = np.array([mine["rungs"]["%s_%.9f" % (tag, c)]["w_T"] * A / c for c in COMMON])
        _, a2m, a4m = joint_fit(COMMON, y_mine)
        shape = (y_mine / y_mine[-1]) / (y_chat / y_chat[-1]) - 1.0
        fp[tag] = {
            "chat_a2_a4_refit_by_cc_fitter": [a2c, a4c],
            "chat_a2_a4_in_checkpoint": [chat_cp["C5_F_DISP"][tag]["a2"],
                                         chat_cp["C5_F_DISP"][tag]["a4"]],
            "fitter_equivalent": bool(abs(a4c - chat_cp["C5_F_DISP"][tag]["a4"]) < 1e-12),
            "cc_a2_a4": [a2m, a4m],
            "rung_shape_rel_diff_vs_ka": {("%g" % c): float(s) for c, s in zip(COMMON, shape)},
            "chat_internal_a4_drift_32v40": chat_lad["F_CONV"]["a4_T_%s_abs_32v40" % tag],
        }
    out["F_S9_2_3_a4"] = {
        "per_direction": fp,
        "mechanism": "the CC fitter applied to the chat leg's own r(k) reproduces the chat "
                     "(a2, a4) exactly, so the a4 misses live entirely in the omega_T(k) "
                     "inputs. The legs' dimensionless ladder shapes differ by ~9e-6 (GK) / "
                     "1.3e-5 (GM) at the outer rungs; through the 4-rung quadratic fit this "
                     "maps to delta-a2 ~ 4.5e-4 / 7.0e-4 (the observed, PASSING a2 gaps) and "
                     "delta-a4 ~ 4e-3 / 6e-3 (the observed a4 gaps). The chat leg's own "
                     "internal a4 resolution drift (8.6e-3 / 6.2e-3, 32v40) exceeds its |a4|; "
                     "the CC drift is 1.6e-4 / 3.2e-4. a4 at the 1e-3 scale is below the "
                     "two-leg systematic floor; the frozen a4 criterion (same sign, <=5e-1 "
                     "rel) implicitly assumed |a4| above that floor. Verdict-irrelevant: "
                     "both arms are A3 from a2, and a2 agrees within its 5e-2 tolerance.",
    }
    out["disposition"] = ("S9 recorded; no re-tuning; arms untouched (A3/A3 both legs, both "
                          "directions); chat side re-runs the frozen comparator on return.")
    json.dump(out, open("cc_s9_fingerprint.json", "w"), indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
