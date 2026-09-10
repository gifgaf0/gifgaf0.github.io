#!/usr/bin/env python3
# g_s2c1_compare.py — Gate G-S2C1 two-leg comparator (FROZEN pre-return). Schema s2c1_cmp_v1.
# Usage: python3 g_s2c1_compare.py s2c1_chat_cmp_checkpoint.json s2c1_cc_cmp_checkpoint.json
# This gate carries FLOAT quantities; tolerances are stated per item and were fixed BEFORE the CC leg ran:
#   C1 substrate   kernel U0 rel 1e-9 ; mean_rho abs 1e-4 (both legs at fixed mu = 53.225) ; residual/lambda_min booleans identical
#   C2 WARD (A-1)  pass_a, pass_b identical (True) ; values reported
#   C3 speeds      c_T rel 1e-4 per direction ; c_L1_framework rel 1e-3 ; R_T_framework rel 1e-3 ; F-ISO pass identical
#   C4 F-MIX       pass identical ; min o2 reported
#   C5 F-DISP      a2 per direction: SAME SIGN and relative agreement <= 5e-2 ; a4: same sign and relative <= 5e-1 ; F_CONV_pass_A2 identical
#   C6 arm         base arm identical per direction (A1..A5 token)
# Any MISS -> S9 counter-cross-check (prereg §8); no verdict before S9 closes. Provenance fields are reported, never compared.
import json, sys, hashlib
def load(p): return json.load(open(p, encoding="utf-8"))
def rel(a, b): return abs(a - b) / max(abs(a), abs(b), 1e-300)
def arm_token(s): return str(s).strip().split()[0]
def main(cp, cc):
    A, B = load(cp), load(cc)
    for p in (cp, cc): print("checkpoint %s md5 %s" % (p, hashlib.md5(open(p, "rb").read()).hexdigest()))
    assert A["schema"] == B["schema"] == "s2c1_cmp_v1" and A["prereg_md5"] == B["prereg_md5"] == "2ea8ec13ffa3c32898cc24a3be605c64"
    miss, notes = [], []
    def chk(tag, ok, desc):
        (notes if ok else miss).append("%s %s: %s" % (tag, "pass" if ok else "MISS", desc)); print("  %s %s  %s" % (tag, "PASS" if ok else "MISS", desc))
    a, b = A["C1_substrate"], B["C1_substrate"]
    chk("C1", rel(a["kernel_U0"], b["kernel_U0"]) <= 1e-9, "kernel U0 %r vs %r" % (a["kernel_U0"], b["kernel_U0"]))
    chk("C1", abs(a["mean_rho"] - b["mean_rho"]) <= 1e-4, "mean_rho %r vs %r" % (a["mean_rho"], b["mean_rho"]))
    chk("C1", a["residual_le_1e-10"] == b["residual_le_1e-10"] == True, "residual<=1e-10 %r vs %r" % (a["residual_le_1e-10"], b["residual_le_1e-10"]))
    chk("C1", a["lambda_min_L_Gamma_ge_minus1e-12"] == b["lambda_min_L_Gamma_ge_minus1e-12"] == True, "lambda_min(L) floor")
    a, b = A["C2_ward_A1"], B["C2_ward_A1"]
    chk("C2", a["pass_a_analytic"] == b["pass_a_analytic"] == True and a["pass_b_hermitian"] == b["pass_b_hermitian"] == True, "A-1 (a)/(b) chat %r/%r cc %r/%r" % (a["pass_a_analytic"], a["pass_b_hermitian"], b["pass_a_analytic"], b["pass_b_hermitian"]))
    for d in ("GK", "GM"):
        a, b = A["C3_speeds"][d], B["C3_speeds"][d]
        chk("C3", rel(a["c_T"], b["c_T"]) <= 1e-4, "%s c_T %.6f vs %.6f (rel %.1e)" % (d, a["c_T"], b["c_T"], rel(a["c_T"], b["c_T"])))
        chk("C3", rel(a["c_L1_framework"], b["c_L1_framework"]) <= 1e-3, "%s c_L1 %.5f vs %.5f" % (d, a["c_L1_framework"], b["c_L1_framework"]))
        chk("C3", rel(a["R_T_framework"], b["R_T_framework"]) <= 1e-3, "%s R_T %.5f vs %.5f" % (d, a["R_T_framework"], b["R_T_framework"]))
    chk("C3", A["C3_F_ISO"]["pass"] == B["C3_F_ISO"]["pass"], "F-ISO pass %r vs %r (splits %.1e / %.1e)" % (A["C3_F_ISO"]["pass"], B["C3_F_ISO"]["pass"], A["C3_F_ISO"]["cT_split"], B["C3_F_ISO"]["cT_split"]))
    chk("C4", A["C4_F_MIX"]["pass"] == B["C4_F_MIX"]["pass"], "F-MIX pass %r vs %r (min o2 %s / %s)" % (A["C4_F_MIX"]["pass"], B["C4_F_MIX"]["pass"], A["C4_F_MIX"]["min_o2_T"], B["C4_F_MIX"]["min_o2_T"]))
    for d in ("GK", "GM"):
        a, b = A["C5_F_DISP"][d], B["C5_F_DISP"][d]
        chk("C5", (a["a2"] * b["a2"] > 0) and rel(a["a2"], b["a2"]) <= 5e-2, "%s a2 %+.4e vs %+.4e (rel %.1e)" % (d, a["a2"], b["a2"], rel(a["a2"], b["a2"])))
        chk("C5", (a["a4"] * b["a4"] > 0) and rel(a["a4"], b["a4"]) <= 5e-1, "%s a4 %+.3e vs %+.3e (rel %.1e)" % (d, a["a4"], b["a4"], rel(a["a4"], b["a4"])))
        chk("C5", a["F_CONV_pass_A2"] == b["F_CONV_pass_A2"], "%s F-CONV(A-2) %r vs %r" % (d, a["F_CONV_pass_A2"], b["F_CONV_pass_A2"]))
        chk("C6", arm_token(A["C6_arm"][d]) == arm_token(B["C6_arm"][d]), "%s arm %s vs %s" % (d, A["C6_arm"][d], B["C6_arm"][d]))
    print("VERDICT chat=%s cc=%s" % ({d: arm_token(A["C6_arm"][d]) for d in ("GK", "GM")}, {d: arm_token(B["C6_arm"][d]) for d in ("GK", "GM")}))
    if miss: print("RESULT: S9 TRIGGERED — %d miss(es); counter-cross-check before any verdict." % len(miss)); return 2
    print("RESULT: C1–C6 ALL PASS — S9 NOT triggered; two-leg single-crystal result stands; P2 aggregate + fold pending author authorization."); return 0
if __name__ == "__main__": sys.exit(main(sys.argv[1], sys.argv[2]))
