#!/usr/bin/env python3
# run_cc_phase4.py — G-S2C1 CC leg Phase 4: A-2 estimator, falsifiers, arm.
# A-2: joint LSQ  w_T/k = c (1 + a2 (ka)^2 + a4 (ka)^4)  over a COMMON floor-clean rung
# set fixed at the resolution of record (n=40): sigma_r = floor_w2 / (2 w_T^2) < 3e-7
# (floor_w2 = the A-1 Hermitian Goldstone |w2| at n=40); excluded rungs listed, never
# silently dropped; window systematic = |a2(common) - a2(sigma_r < 1e-6 set)| at n=40.
# F-CONV (A-2): a2 across successive resolutions |da2| <= 1e-7 if |a2| <= 1e-5 else
# |da2|/|a2| <= 1e-2; c_T: |dc_T|/c_T <= 1e-5.  F-ISO: |c_T(GK)/c_T(GM) - 1| <= 0.01.
# F-MIX: min o2(T) >= 0.90.  F-DISP at tau = 1e-6 with CI = max(resolution deltas, window).
# Controls: F-CTRL-L (compressional branch must show nonzero dispersion through the same
# fitter), F-CTRL-INJ (synthetic (ka)^2 injection at 10x tau recovered within CI).
# Arms A1..A5 per prereg §5, decided by these numbers alone (quarantine still sealed).
import json
import numpy as np

RES = [24, 32, 40]
TAU = 1e-6
THETA_ISO = 0.01
THETA_ID = 0.90
SIG_COMMON = 3e-7
SIG_WINDOW = 1e-6
A_STAR = 1.46059


def joint_fit(ka_arr, y_arr):
    x = np.asarray(ka_arr, float) ** 2
    V = np.vstack([np.ones_like(x), x, x * x]).T
    p, *_ = np.linalg.lstsq(V, np.asarray(y_arr, float), rcond=None)
    return float(p[0]), float(p[1] / p[0]), float(p[2] / p[0])


def load(n):
    return json.load(open("cc_phase3_%d.json" % n))


def rung(d, tag, ka):
    return d["rungs"]["%s_%.9f" % (tag, ka)]


def main():
    ph2 = json.load(open("cc_phase2.json"))
    floor_w2 = ph2["record"]["floor_w2_for_A2"]
    data = {n: load(n) for n in RES}
    ladder = data[RES[0]]["ladder_ka"]
    nrec = RES[-1]

    # --- rung selection at the resolution of record (per direction, then intersection) ---
    sel = {"floor_w2": floor_w2, "sigma_r": {}, "common": None, "window": None, "excluded": None}
    sets = {}
    for tag in ("GK", "GM"):
        sig = {}
        for ka in ladder:
            wT = rung(data[nrec], tag, ka)["w_T"]
            sig["%.9f" % ka] = floor_w2 / (2.0 * wT * wT)
        sel["sigma_r"][tag] = sig
        sets[tag] = {"common": [ka for ka in ladder if sig["%.9f" % ka] < SIG_COMMON],
                     "window": [ka for ka in ladder if sig["%.9f" % ka] < SIG_WINDOW]}
    common = sorted(set(sets["GK"]["common"]) & set(sets["GM"]["common"]), reverse=True)
    window = sorted(set(sets["GK"]["window"]) & set(sets["GM"]["window"]), reverse=True)
    sel["common"] = common
    sel["window"] = window
    sel["excluded"] = sorted(set(ladder) - set(common), reverse=True)
    sel["window_equals_common"] = bool(set(window) == set(common))

    out = {"gate": "G-S2C1", "leg": "cc", "phase": 4, "tau": TAU,
           "rung_selection_A2": sel, "directions": {}, "controls": {}, "checks": {}}

    # --- admissibility across the whole ladder ---
    lam_ok = all(rung(data[n], tag, ka)["lambda_min_L_ge_minus1e-12"]
                 for n in RES for tag in ("GK", "GM") for ka in ladder)
    out["checks"]["lambda_min_L_all_rungs_ok"] = bool(lam_ok)
    pc = {}
    for tag in ("GK", "GM"):
        for ka in (0.3, 0.01875):
            e = rung(data[nrec], tag, ka)
            if "product_vs_hermitian_relC" in e:
                pc["%s_%.5f" % (tag, ka)] = e["product_vs_hermitian_relC"]
    out["checks"]["product_form_crosscheck_relC"] = pc

    arms = {}
    for tag in ("GK", "GM"):
        dd = {"fits_common": {}, "F_CONV": {}, "window": {}}
        fits = {}
        for n in RES:
            ka_arr = common
            y = [rung(data[n], tag, ka)["w_T"] * A_STAR / ka for ka in ka_arr]
            cT, a2, a4 = joint_fit(ka_arr, y)
            fits[n] = (cT, a2, a4)
            dd["fits_common"][str(n)] = {"c_T": cT, "a2": a2, "a4": a4}
        cT, a2, a4 = fits[nrec]
        regime = "absolute" if abs(a2) <= 10 * TAU else "relative"
        conv_pairs = {}
        conv_ok = True
        for (na, nb) in ((RES[0], RES[1]), (RES[1], RES[2])):
            da2 = abs(fits[nb][1] - fits[na][1])
            dcT = abs(fits[nb][0] - fits[na][0]) / abs(fits[nb][0])
            if regime == "absolute":
                ok_a2 = da2 <= 1e-7
                metric = da2
            else:
                metric = da2 / abs(fits[nb][1])
                ok_a2 = metric <= 1e-2
            ok_cT = dcT <= 1e-5
            conv_pairs["%d_to_%d" % (na, nb)] = {
                "da2_abs": da2, "da2_metric": metric, "dcT_rel": dcT,
                "pass_a2": bool(ok_a2), "pass_cT": bool(ok_cT)}
            conv_ok = conv_ok and ok_a2 and ok_cT
        dd["F_CONV"] = {"regime": regime, "pairs": conv_pairs, "pass": bool(conv_ok)}
        yw = [rung(data[nrec], tag, ka)["w_T"] * A_STAR / ka for ka in window]
        cTw, a2w, a4w = joint_fit(window, yw)
        window_term = abs(a2w - a2)
        dd["window"] = {"rungs": window, "a2_window": a2w, "window_term": window_term}
        res_deltas = [conv_pairs[p]["da2_abs"] for p in conv_pairs]
        CI = max(max(res_deltas), window_term)
        dd["a2"] = a2
        dd["a4"] = a4
        dd["c_T"] = cT
        dd["CI_a2_total"] = CI
        # a4 uncertainty from the same resolution deltas
        CI4 = max(abs(fits[RES[1]][2] - fits[RES[0]][2]), abs(fits[RES[2]][2] - fits[RES[1]][2]))
        dd["CI_a4_resolution"] = CI4
        # compressional branches (fit both sequences over the common set)
        comp = {}
        for key in ("w_comp_low", "w_comp_high"):
            yc = [rung(data[nrec], tag, ka)[key] * A_STAR / ka for ka in common]
            cc, b2, b4 = joint_fit(common, yc)
            comp[key] = {"c": cc, "b2": b2, "b4": b4}
        cs = sorted([comp["w_comp_low"]["c"], comp["w_comp_high"]["c"]])
        dd["compressional"] = comp
        dd["c_L1_framework"] = cs[1]
        dd["c_other_compressional"] = cs[0]
        dd["R_T_framework"] = cT / cs[1]
        # F-MIX over the full ladder at the resolution of record
        o2min = min(rung(data[nrec], tag, ka)["o2_T"] for ka in ladder)
        r2min = min(rung(data[nrec], tag, ka)["R2_T"] for ka in ladder)
        gsmin = min(rung(data[nrec], tag, ka)["grad_share_T"] for ka in ladder)
        dd["F_MIX"] = {"min_o2_T": o2min, "min_R2_T": r2min, "min_grad_share_T": gsmin,
                       "pass": bool(o2min >= THETA_ID)}
        # F-DISP
        disp2 = abs(a2) - CI > TAU
        zero2 = abs(a2) + CI < TAU or abs(a2) <= TAU
        disp4 = abs(a4) - CI4 > TAU
        dd["F_DISP"] = {"a2_above_tau_beyond_CI": bool(disp2),
                        "a2_zero_consistent": bool(zero2),
                        "a4_above_tau_beyond_CI": bool(disp4)}
        out["directions"][tag] = dd

    # F-ISO
    cGKt = out["directions"]["GK"]["c_T"]
    cGMt = out["directions"]["GM"]["c_T"]
    split = abs(cGKt / cGMt - 1.0)
    out["F_ISO"] = {"cT_split": split, "pass": bool(split <= THETA_ISO)}

    # F-CTRL-L: the higher compressional branch must show nonzero dispersion via the same fitter
    ctrl_L = {}
    for tag in ("GK", "GM"):
        b2 = out["directions"][tag]["compressional"]["w_comp_high"]["b2"]
        ctrl_L[tag] = {"b2_L1": b2, "nonzero": bool(abs(b2) > TAU)}
    out["controls"]["F_CTRL_L"] = {**ctrl_L, "pass": bool(all(v["nonzero"] for v in ctrl_L.values()))}

    # F-CTRL-INJ: inject a2_inj = 1e-5 into the record-resolution T data, refit, recover
    inj = {}
    A2_INJ = 1e-5
    for tag in ("GK", "GM"):
        y = np.array([rung(data[nrec], tag, ka)["w_T"] * A_STAR / ka for ka in common])
        x = np.array(common) ** 2
        y_inj = y * (1.0 + A2_INJ * x)
        _, a2i, _ = joint_fit(common, y_inj)
        rec = a2i - out["directions"][tag]["fits_common"][str(nrec)]["a2"]
        inj[tag] = {"recovered_delta_a2": rec, "target": A2_INJ,
                    "ok": bool(abs(rec - A2_INJ) < 0.01 * A2_INJ)}
    out["controls"]["F_CTRL_INJ"] = {**inj, "pass": bool(all(v["ok"] for v in inj.values()))}

    # --- arms ---
    for tag in ("GK", "GM"):
        dd = out["directions"][tag]
        if not dd["F_MIX"]["pass"]:
            arm = "A4 CHANNEL-UNDEFINED"
        elif (not dd["F_CONV"]["pass"]) or (not out["controls"]["F_CTRL_L"]["pass"]) \
                or (not out["controls"]["F_CTRL_INJ"]["pass"]) or (not lam_ok):
            arm = "A5 INSTRUMENT-LIMITED"
        elif dd["F_DISP"]["a2_above_tau_beyond_CI"]:
            arm = "A3 DISPERSIVE-O(k^2)"
        elif dd["F_DISP"]["a2_zero_consistent"] and dd["F_DISP"]["a4_above_tau_beyond_CI"]:
            arm = "A2 ON-CONE-PROTECTED-O(k^4)"
        elif dd["F_DISP"]["a2_zero_consistent"] and not dd["F_DISP"]["a4_above_tau_beyond_CI"] \
                and out["F_ISO"]["pass"]:
            arm = "A1 ON-CONE-EXACT"
        else:
            arm = "A5 INSTRUMENT-LIMITED"
        arms[tag] = arm
    out["C6_arm"] = arms
    out["registered_expectation"] = "DISPERSIVE"

    json.dump(out, open("cc_phase4.json", "w"), indent=1)
    for tag in ("GK", "GM"):
        dd = out["directions"][tag]
        print("%s: c_T=%.6f a2=%+.6e (CI %.2e) a4=%+.4e regime=%s F-CONV=%s arm=%s" %
              (tag, dd["c_T"], dd["a2"], dd["CI_a2_total"], dd["a4"],
               dd["F_CONV"]["regime"], dd["F_CONV"]["pass"], arms[tag]))
    print("F-ISO split=%.3e pass=%s | F-CTRL-L pass=%s | F-CTRL-INJ pass=%s" %
          (out["F_ISO"]["cT_split"], out["F_ISO"]["pass"],
           out["controls"]["F_CTRL_L"]["pass"], out["controls"]["F_CTRL_INJ"]["pass"]))
    print("common rungs:", common, "| window rungs:", window)

if __name__ == "__main__":
    main()
