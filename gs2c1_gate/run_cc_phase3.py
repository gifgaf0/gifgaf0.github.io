#!/usr/bin/env python3
# run_cc_phase3.py — G-S2C1 CC leg Phase 3: the E-4 dyadic ka-ladder, both symmetry
# directions (GK along a bond, GM at 30 deg), three resolutions n in {24, 32, 40}.
# Per rung: the S2 branch (branch of maximal traceless-strain fraction o2 among
# lattice-phonon modes: R2 >= 0.90, grad share >= 0.5), w_T, the two compressional
# branches, lambda_min(L) at every k; product-form cross-checks at ka = 0.3 and 0.01875
# at the resolution of record. Writes cc_phase3_<n>.json progressively per rung.
import json, sys, time
import numpy as np
import s2c1_cc_core as core

RES = [24, 32, 40]
CROSSCHECK_KA = (0.3, 0.01875)
THETA_ID = 0.90


def analyze_rung(cell, c, fl, tag, ka, do_product):
    k = (ka / core.A_STAR) * core.direction_unit(tag)
    spec = fl.hermitian_spectrum(k[0], k[1], nlow=6)
    branches = []
    for (w2, f) in spec["modes"]:
        ch = core.mode_character(cell, c, f, fl, k[0], k[1])
        w = float(np.sqrt(abs(w2)))
        branches.append({"w2": float(w2), "w": w, "o2": ch["o2"], "R2": ch["R2"],
                         "grad_share": ch["grad_share"]})
    branches.sort(key=lambda b: b["w2"])
    phon = [i for i, b in enumerate(branches)
            if b["R2"] >= 0.90 and b["grad_share"] >= 0.5]
    s2_idx = max(phon, key=lambda i: branches[i]["o2"]) if phon else None
    acoustic3 = list(range(3))
    comp = sorted(set(acoustic3) - {s2_idx}) if s2_idx is not None else acoustic3[:2]
    comp = comp[:2]
    entry = {
        "ka": ka, "k_abs": float(np.linalg.norm(k)), "direction": tag,
        "lambda_min_L": spec["lambda_min_L"],
        "lambda_min_L_ge_minus1e-12": bool(spec["lambda_min_L"] >= -1e-12),
        "asym_X_presym": spec["asym_X"],
        "branches_low6": branches,
        "s2_branch_index": s2_idx,
        "w_T": branches[s2_idx]["w"] if s2_idx is not None else None,
        "o2_T": branches[s2_idx]["o2"] if s2_idx is not None else None,
        "R2_T": branches[s2_idx]["R2"] if s2_idx is not None else None,
        "grad_share_T": branches[s2_idx]["grad_share"] if s2_idx is not None else None,
        "w_comp_low": branches[comp[0]]["w"] if len(comp) > 0 else None,
        "w_comp_high": branches[comp[1]]["w"] if len(comp) > 1 else None,
    }
    if do_product:
        w2p = fl.product_w2(k[0], k[1], nlow=8)
        wT2 = branches[s2_idx]["w2"] if s2_idx is not None else None
        if wT2 is not None:
            j = int(np.argmin(np.abs(w2p - wT2)))
            entry["product_form_w2_T"] = [float(w2p[j].real), float(w2p[j].imag)]
            entry["product_vs_hermitian_relC"] = float(abs(w2p[j] - wT2) / abs(wT2))
    return entry


def main():
    only = [int(x) for x in sys.argv[1:]] or RES
    for n in only:
        cell = core.Cell(n)
        c = np.load("cc_psi0_n%d.npy" % n)
        fl = core.Fluct(cell, c)
        out = {"gate": "G-S2C1", "leg": "cc", "phase": 3, "n": n,
               "theta_id": THETA_ID, "ladder_ka": core.LADDER_KA, "rungs": {}}
        t0 = time.time()
        for tag in ("GK", "GM"):
            for ka in core.LADDER_KA:
                do_prod = (n == RES[-1]) and any(abs(ka - x) < 1e-12 for x in CROSSCHECK_KA)
                e = analyze_rung(cell, c, fl, tag, ka, do_prod)
                out["rungs"]["%s_%.9f" % (tag, ka)] = e
                json.dump(out, open("cc_phase3_%d.json" % n, "w"), indent=1)
                print("n=%d %s ka=%.9f  w_T=%s o2=%s lamminL=%.3e  (%.1fs)" %
                      (n, tag, ka, e["w_T"], e["o2_T"], e["lambda_min_L"], time.time() - t0),
                      flush=True)
        print("phase 3 n=%d complete (%.1fs)" % (n, time.time() - t0), flush=True)

if __name__ == "__main__":
    main()
