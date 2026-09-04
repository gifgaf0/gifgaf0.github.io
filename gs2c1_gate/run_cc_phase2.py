#!/usr/bin/env python3
# run_cc_phase2.py — G-S2C1 CC leg Phase 2: WARD-Gamma per Addendum A-1.
# (a) analytic-mode Ward residual: ||(L+2X) d_x psi0|| / ||d_x psi0|| (and d_y) <= 1e-9
# (b) Hermitian-form Goldstone |w2| <= 1e-8 at Gamma with lambda_min(L) >= -1e-12.
# Halt on failure. Writes cc_phase2.json. The Gamma Goldstone floor at the resolution of
# record is the A-2 floor_w2 used for the floor-clean rung selection.
import json, sys
import numpy as np
import s2c1_cc_core as core

RES = [24, 32, 40]


def main():
    out = {"gate": "G-S2C1", "leg": "cc", "phase": 2, "resolutions": {}}
    for n in RES:
        cell = core.Cell(n)
        c = np.load("cc_psi0_n%d.npy" % n)
        fl = core.Fluct(cell, c)
        L, X, _ = fl.matrices(0.0, 0.0)
        A2X = L + 2.0 * X
        wr = {}
        for tag, Gc in (("dx", 1j * cell.Gx), ("dy", 1j * cell.Gy)):
            v = (Gc * c).ravel()[fl.sel]
            wr[tag] = float(np.linalg.norm(A2X @ v) / np.linalg.norm(v))
        spec = fl.hermitian_spectrum(0.0, 0.0, nlow=6)
        low = sorted(np.abs(spec["w2_all_low"]))
        goldstone = float(max(low[:3]))
        entry = {
            "n": n,
            "ward_residual_dx": wr["dx"], "ward_residual_dy": wr["dy"],
            "pass_a_analytic": bool(max(wr.values()) <= 1e-9),
            "hermitian_goldstone_abs_w2": goldstone,
            "w2_low6_abs_sorted": [float(x) for x in low],
            "lambda_min_L_Gamma": spec["lambda_min_L"],
            "pass_b_hermitian": bool(goldstone <= 1e-8 and spec["lambda_min_L"] >= -1e-12),
        }
        out["resolutions"][str(n)] = entry
        print(json.dumps(entry, indent=1))
    rec = out["resolutions"][str(RES[-1])]
    out["record"] = {
        "resolution_of_record": RES[-1],
        "pass_a_analytic": rec["pass_a_analytic"],
        "pass_b_hermitian": rec["pass_b_hermitian"],
        "analytic_ward_residual_max": max(rec["ward_residual_dx"], rec["ward_residual_dy"]),
        "hermitian_goldstone_abs_w2_max": rec["hermitian_goldstone_abs_w2"],
        "lambda_min_L_Gamma": rec["lambda_min_L_Gamma"],
        "floor_w2_for_A2": rec["hermitian_goldstone_abs_w2"],
    }
    allpass = all(out["resolutions"][str(n)]["pass_a_analytic"] and
                  out["resolutions"][str(n)]["pass_b_hermitian"] for n in RES)
    out["WARD_GAMMA_pass"] = bool(allpass)
    json.dump(out, open("cc_phase2.json", "w"), indent=1)
    print("phase 2 complete; WARD_GAMMA_pass =", allpass)
    if not allpass:
        print("HALT: WARD-Gamma (A-1) failed")
        sys.exit(2)

if __name__ == "__main__":
    main()
