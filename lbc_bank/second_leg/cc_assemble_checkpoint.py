#!/usr/bin/env python3
"""cc_assemble_checkpoint.py -- fill the lbc_2leg_schema_v1.0 skeleton (dispatch embed E4) from this leg's task
results and write lbc_cc_checkpoint.json (leg "cc").

Sources (all in this folder): qa_results.json (Q-A), qa_prime_results.json (Q-A'), qb_results.json (Q-B),
qc_results.json (Q-C), qd_results.json (Q-D). Every schema value is copied at full precision; nothing is rounded.
Extra keys (reported by the comparator as CC-only, not compared) carry the reading alternatives and the
cross-check agreement figures.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)

skel = load("dispatch_embeds/lbc_2leg_schema_v1.0_skeleton.json")
qa, qp, qb, qc, qd = (load(n) for n in ("qa_results.json", "qa_prime_results.json", "qb_results.json",
                                        "qc_results.json", "qd_results.json"))
x2, x3 = load("xcheck2d_results.json"), load("xcheck3d_results.json")

ck = json.loads(json.dumps(skel))
assert ck["schema"] == "lbc_2leg_schema_v1.0" and ck["leg"] == "cc"

# ---- 2D (Q-A) ----
for key, slot in ck["2d"].items():
    p = qa["points"][key]
    for k in slot:
        slot[k] = p[k]
    # CC-only extras
    slot["cc_astar_dedA_root"] = p["astar_crosscheck"]["dedA_root"]
    slot["cc_f_s_linear_response"] = p["f_s_detail"]["lr_x"]
    slot["cc_f_s_twist_extrapolated"] = p["f_s_detail"]["twist_x"]
    slot["cc_e_per_particle"] = p["e_per_particle"]
    slot["cc_mu"] = p["mu"]
    slot["cc_c2_gt_cT"] = p["c2_gt_cT"]
    for k in ("cT_30deg_kf005", "fsum_resid_max", "static_resid_max", "f_s"):
        if k not in slot:
            slot["cc_" + k] = p[k]

# ---- Q-A' hydro at g = 22 ----
for k in ck["hydro_g22"]:
    ck["hydro_g22"][k] = qp[k]

# ---- 3D (Q-B) ----
for k in ck["3d"]:
    ck["3d"][k] = qb["schema"][k]
e = qb["extras"]
ck["3d"]["cc_c2_q03"] = e["c2_q03"]
ck["3d"]["cc_F2_basal_q03"] = e["F2_basal_q03"]
ck["3d"]["cc_c_kappa_q03"] = e["c_kappa_q03"]
ck["3d"]["cc_transverse_speeds_q015"] = e["transverse_speeds_q015"]
ck["3d"]["cc_cT_mean_all_dir_pol_q015"] = e["cT_mean_all_dir_pol_q015"]
ck["3d"]["cc_Lambda_c"] = qb["Lambda_c"]
ck["3d"]["cc_Lambda"] = qb["Lambda"]

# ---- Q-C melting ----
for k in ck["melting"]:
    ck["melting"][k] = qc[k]
# the boolean is the OR over every crystal state computed in this leg (Q-A, g6, Q-C branch, 3D)
any_ge = bool(qc["any_c2_ge_cT"]) or any(bool(p["c2_gt_cT"]) for p in qa["points"].values()) \
    or bool(e["flag_c2_gt_cT"])
ck["melting"]["any_c2_ge_cT"] = any_ge
ck["melting"]["cc_ratio_max_metastable_at_g"] = qc["ratio_max_metastable_at_g"]
ck["melting"]["cc_branch_end_bisection_bracket"] = qc["branch_end_bisection_bracket"]
ck["melting"]["cc_bdg_long_wave_instability_first_g"] = qc["bdg_instability_first_g"]
ck["melting"]["cc_bdg_long_wave_instability_q_to_0_g"] = qc["bdg_instability_q_to_0_estimate"]

# ---- Q-D loss ----
for k in ck["loss"]:
    ck["loss"][k] = qd[k]
alt = qd["alternatives"]
ck["loss"]["cc_band_orders_recovered_reading"] = alt["band_recovered_orders"]
ck["loss"]["cc_band_orders_R3_without_F2"] = alt["band_orders_with_R3_without_F2"]
ck["loss"]["cc_eq3_coefficient_with_own_cT_mean"] = qd["eq3_alternatives"]["with_own_cT_mean"]
ck["loss"]["cc_drag_convention"] = qd["drag_derivation_checks"]["convention"]

# ---- leg-level extras ----
ck["cc_meta"] = {
    "methods": "2D: plane-wave primitive cell, L-BFGS + Newton-Krylov ground states, Brent a*, dense BdG (Cholesky, "
               "circular cut), f_s by linear response and finite twist; Q-A': finite strains at fixed density with "
               "Richardson; Q-C: a*-optimized continuation, Brent roots; 3D: hexagonal primitive cell BdG "
               "(orthorhombic cell ground state checked equal), sphere cut; Q-D: two independent drag derivations.",
    "independent_xcheck_2d": "rectangular 2-droplet supercell, square cut, full non-Hermitian BdG eig, twist f_s",
    "independent_xcheck_3d": "orthorhombic 4-site cell, box cut, generalized Hermitian BdG",
}

# fill check: no null left anywhere in the schema part
def nulls(d, pre=""):
    for k, v in d.items():
        kk = f"{pre}.{k}" if pre else k
        if isinstance(v, dict):
            yield from nulls(v, kk)
        elif v is None or (isinstance(v, list) and any(x is None for x in v)):
            yield kk
missing = [k for k in nulls({s: ck[s] for s in skel if isinstance(skel[s], dict)}) if ".cc_" not in "." + k
           and not k.split(".")[-1].startswith("cc_")]
assert not missing, missing
for sec in ("2d", "hydro_g22", "3d", "melting", "loss"):
    for k, v in skel[sec].items():
        if isinstance(v, list):
            got = ck[sec][k]
            assert isinstance(got, list) and len(got) == len(v), (sec, k)

with open(os.path.join(HERE, "lbc_cc_checkpoint.json"), "w") as f:
    json.dump(ck, f, indent=1)
print("wrote lbc_cc_checkpoint.json; any_c2_ge_cT =", any_ge)
