#!/usr/bin/env python3
# run_cc_phase5_checkpoint.py — G-S2C1 CC leg Phase 5: assemble the comparison checkpoint
# s2c1_cc_cmp_checkpoint.json in schema s2c1_cmp_v1 with EXACTLY the dispatch §3 blocks and
# keys, then run the T1 scan over every CC instrument and output. The checkpoint is hashed
# and committed BEFORE the quarantine is decoded (procedural blindness, P-4.b).
import json, hashlib, subprocess, sys

INSTRUMENTS = [
    "s2c1_cc_core.py", "run_cc_validation.py", "run_cc_phase1.py", "run_cc_phase2.py",
    "run_cc_phase3.py", "run_cc_phase4.py", "run_cc_phase5_checkpoint.py",
    "write_cc_phase0.py", "sanitize_t1_floats.py",
]
OUTPUTS = [
    "cc_phase0.json", "cc_instrument_validation.json", "cc_phase1.json", "cc_phase2.json",
    "cc_phase3_24.json", "cc_phase3_32.json", "cc_phase3_40.json", "cc_phase4.json",
]


def md5f(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def main():
    ph1 = json.load(open("cc_phase1.json"))
    ph2 = json.load(open("cc_phase2.json"))
    ph4 = json.load(open("cc_phase4.json"))
    rec1 = ph1["resolutions"]["40"]
    rec2 = ph2["record"]

    cp = {
        "schema": "s2c1_cmp_v1",
        "gate": "G-S2C1",
        "leg": "cc",
        "prereg_md5": "2ea8ec13ffa3c32898cc24a3be605c64",
        "addenda_md5": {"A1": "8bf51bd05c691f3f03d796b231cdd262",
                        "A2": "a9bda086213ee0afe1e2ba01055659cd"},
        "source_md5": md5f("G_S2C1_CC_DISPATCH_INBAND.md"),
        "C1_substrate": {
            "kernel_U0": 20.0,
            "g_star": 20.0,
            "a_star": 1.46059,
            "mu_fixed": 53.225,
            "mean_rho": rec1["mean_rho"],
            "residual_rel": rec1["residual_rel"],
            "residual_le_1e-10": rec1["residual_le_1e-10"],
            "lambda_min_L_Gamma_ge_minus1e-12": rec1["lambda_min_L_Gamma_ge_minus1e-12"],
            "resolution_of_record": "n=40 Fourier-collocation band basis (dim 1521), dealiased",
        },
        "C2_ward_A1": {
            "pass_a_analytic": rec2["pass_a_analytic"],
            "pass_b_hermitian": rec2["pass_b_hermitian"],
            "analytic_ward_residual_max": rec2["analytic_ward_residual_max"],
            "hermitian_goldstone_abs_w2_max": rec2["hermitian_goldstone_abs_w2_max"],
            "lambda_min_L_Gamma": rec2["lambda_min_L_Gamma"],
        },
        "C3_speeds": {},
        "C3_F_ISO": {"cT_split": ph4["F_ISO"]["cT_split"], "pass": ph4["F_ISO"]["pass"]},
        "C4_F_MIX": {"min_o2_T": {t: ph4["directions"][t]["F_MIX"]["min_o2_T"]
                                  for t in ("GK", "GM")},
                     "pass": bool(all(ph4["directions"][t]["F_MIX"]["pass"]
                                      for t in ("GK", "GM")))},
        "C5_F_DISP": {},
        "C6_arm": ph4["C6_arm"],
        "registered_expectation": ph4["registered_expectation"],
    }
    for t in ("GK", "GM"):
        dd = ph4["directions"][t]
        cp["C3_speeds"][t] = {
            "c_T": dd["c_T"],
            "c_L1_framework": dd["c_L1_framework"],
            "c_other_compressional": dd["c_other_compressional"],
            "R_T_framework": dd["R_T_framework"],
        }
        cp["C5_F_DISP"][t] = {
            "a2": dd["a2"],
            "a4": dd["a4"],
            "CI_a2_total": dd["CI_a2_total"],
            "regime": dd["F_CONV"]["regime"],
            "F_CONV_pass_A2": dd["F_CONV"]["pass"],
            "rungs_used_ka": ph4["rung_selection_A2"]["common"],
        }
    json.dump(cp, open("s2c1_cc_cmp_checkpoint.json", "w"), indent=1)
    print("s2c1_cc_cmp_checkpoint.json md5", md5f("s2c1_cc_cmp_checkpoint.json"))

    # T1 scan (frozen list; exemptions: locked prereg/addenda/reports + quarantined artifacts)
    scan = INSTRUMENTS + OUTPUTS + ["s2c1_cc_cmp_checkpoint.json"]
    r = subprocess.run(["grep", "-n", "-i", "-F", "-f", "t1_forbidden_G_S2_ON_CONE.txt"] + scan,
                       capture_output=True, text=True)
    hits = r.stdout.strip()
    print("T1 scan:", "ZERO HITS" if not hits else "HITS FOUND:\n" + hits)
    if hits:
        sys.exit(3)

if __name__ == "__main__":
    main()
