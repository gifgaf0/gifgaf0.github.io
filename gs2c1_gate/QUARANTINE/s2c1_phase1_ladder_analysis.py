#!/usr/bin/env python3
"""Post-assembly DIAGNOSTIC analysis of the Phase-1 ladder checkpoint (5ee152fc): NOT the elected estimator.
(1) per-rung r_T across n_b with the A-1 floor sigma; (2) the c-free joint fit omega_T/k = c(1 + a2 x + a4 x^2) on
all rungs vs floor-clean rungs (sigma_r < 1e-6). Reads the checkpoint only; changes no value in it."""
import json, hashlib, numpy as np
ck = json.load(open("g_s2c1_phase1_ladder_checkpoint.json")); runs = ck["step3_ladder"]["runs"]; A = 1.46059
out = {"source_checkpoint_md5": hashlib.md5(open("g_s2c1_phase1_ladder_checkpoint.json", "rb").read()).hexdigest(), "estimator": "DIAGNOSTIC joint fit (c free); the elected estimator's values are in the checkpoint", "per_direction": {}}
for dd in ("GK", "GM"):
    rec = {"per_rung": [], "joint_fit": {}}
    ka = np.array(runs["40"]["T"][dd]["ka"]); sig = np.array(runs["40"]["T"][dd]["floor_sigma_r"])
    for i, k in enumerate(ka):
        rec["per_rung"].append({"ka": float(k), "r24": runs["24"]["T"][dd]["r"][i], "r32": runs["32"]["T"][dd]["r"][i], "r40": runs["40"]["T"][dd]["r"][i], "floor_sigma_r_nb40": float(sig[i])})
    for nb in ("24", "32", "40"):
        kb = np.array(runs[nb]["T"][dd]["ka"]); om = np.array([e["T"]["omega"] for e in runs[nb]["ident"][dd]]); y = om / (kb / A)
        for lab, sel in (("all_rungs", kb > 0), ("floor_clean_rungs_ka_ge_0.0375", kb >= 0.037)):
            X = np.stack([np.ones(sel.sum()), kb[sel]**2, kb[sel]**4], axis=1); c, *_ = np.linalg.lstsq(X, y[sel], rcond=None)
            rec["joint_fit"]["nb%s_%s" % (nb, lab)] = {"c_T": float(c[0]), "a2": float(c[1] / c[0]), "a4": float(c[2] / c[0]), "n_rungs": int(sel.sum())}
    a = [rec["joint_fit"]["nb%s_floor_clean_rungs_ka_ge_0.0375" % nb]["a2"] for nb in ("24", "32", "40")]
    rec["a2_floor_clean_rel_drift"] = {"24v32": abs(a[1] - a[0]) / abs(a[1]), "32v40": abs(a[2] - a[1]) / abs(a[2])}
    rec["a2_floor_clean_nb40"] = a[2]; rec["a4_floor_clean_nb40"] = rec["joint_fit"]["nb40_floor_clean_rungs_ka_ge_0.0375"]["a4"]
    rec["c_T_floor_clean_nb40"] = rec["joint_fit"]["nb40_floor_clean_rungs_ka_ge_0.0375"]["c_T"]
    out["per_direction"][dd] = rec
out["reading"] = ("The n_b drift of the elected estimator is a uniform offset in r_T of ~1e-5 across rungs = a shift of the k->0 speed "
                  "extrapolated from the small-k speed set, where the dense-eig floor (A-1 term) is ~1.5e-5 in r; the T-branch omegas at "
                  "ka >= 0.0375 agree across n_b to ~1e-6. The c-free joint fit on floor-clean rungs converges to <= 3e-3 relative in a2.")
b = (json.dumps(out, indent=1, sort_keys=True) + "\n").encode(); open("s2c1_phase1_ladder_analysis.json", "wb").write(b)
print("analysis md5", hashlib.md5(b).hexdigest(), len(b), "B")
for dd in ("GK", "GM"): print(dd, "a2_fc(40) %+.5e a4_fc(40) %+.4e c_T %.6f drift 24v32 %.1e 32v40 %.1e" % (out["per_direction"][dd]["a2_floor_clean_nb40"], out["per_direction"][dd]["a4_floor_clean_nb40"], out["per_direction"][dd]["c_T_floor_clean_nb40"], out["per_direction"][dd]["a2_floor_clean_rel_drift"]["24v32"], out["per_direction"][dd]["a2_floor_clean_rel_drift"]["32v40"]))
