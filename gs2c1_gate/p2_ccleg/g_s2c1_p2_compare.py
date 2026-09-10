#!/usr/bin/env python3
# g_s2c1_p2_compare.py — Gate G-S2C1 Probe P2 (aggregate) two-leg comparator (FROZEN pre-return). Schema p2_cmp_v1.
# Usage: python3 g_s2c1_p2_compare.py s2c1_p2_chat_cmp_checkpoint.json s2c1_p2_cc_cmp_checkpoint.json
# Tolerances fixed BEFORE the CC leg runs (per substrate; all four substrates):
#   C1 pin        Q_T_a, V_T, V_L rel <= 1e-10 (both legs reproduce the bank) ; pin_pass identical True
#   C2 KK         alpha tie-in <= 1e-9 on both legs (boolean identical True) ; values reported
#   C3 D0         static shift, T and L, rel <= 1e-8
#   C4 a2_agg     analytic D2, T and L, rel <= 1e-6 (closed form on the same kernels; absorbs quadrature-scheme differences)
#   C5 a4_agg     even-basis k^4 coefficient rel <= 5e-2 (fit-dependent) ; even-basis rms <= 1e-7 on both legs ; small-k confirmation <= 1e-3 both
#   C6 controls   F_AGG_DISP, F_AGG_L, F_CONV, structure booleans identical True
#   C7 arm        base arm token identical ("A3-agg")
# Any MISS -> S9 (prereg §8). Provenance fields reported, never compared.
import json, sys, hashlib
def load(p): return json.load(open(p, encoding="utf-8"))
def rel(a, b): return abs(a - b) / max(abs(a), abs(b), 1e-300)
def main(cp, cc):
    A, B = load(cp), load(cc)
    for p in (cp, cc): print("checkpoint %s md5 %s" % (p, hashlib.md5(open(p, "rb").read()).hexdigest()))
    assert A["schema"] == B["schema"] == "p2_cmp_v1" and A["prereg_md5"] == B["prereg_md5"] == "2ea8ec13ffa3c32898cc24a3be605c64"
    assert A["addenda_md5"]["P2"] == B["addenda_md5"]["P2"] and A["addenda_md5"]["P2A"] == B["addenda_md5"]["P2A"], "addenda lock mismatch"
    miss = []
    def chk(tag, ok, desc):
        (None if ok else miss).append(tag + " " + desc) if not ok else None; print("  %s %s  %s" % (tag, "PASS" if ok else "MISS", desc))
    for n in ("step_hex", "gem8_hex", "step_cubic", "gem8_cubic"):
        a, b = A["per_substrate"][n], B["per_substrate"][n]
        for q in ("Q_T_a", "V_T", "V_L"): chk("C1", rel(a["C1_pin"][q], b["C1_pin"][q]) <= 1e-10, "%s %s %r vs %r" % (n, q, a["C1_pin"][q], b["C1_pin"][q]))
        chk("C1", a["C1_pin"]["pin_pass"] == b["C1_pin"]["pin_pass"] == True, "%s pin_pass" % n)
        chk("C2", a["C2_KK"]["pass"] == b["C2_KK"]["pass"] == True, "%s KK tie-in chat %.1e cc %.1e" % (n, a["C2_KK"]["alpha_tie_max_rel"], b["C2_KK"]["alpha_tie_max_rel"]))
        for ch in ("T", "L"): chk("C3", rel(a["C3_D0"][ch], b["C3_D0"][ch]) <= 1e-8, "%s D0_%s %+.6e vs %+.6e" % (n, ch, a["C3_D0"][ch], b["C3_D0"][ch]))
        for ch in ("T_analytic", "L_analytic"): chk("C4", rel(a["C4_a2_agg"][ch], b["C4_a2_agg"][ch]) <= 1e-6, "%s a2_agg %s %+.6e vs %+.6e (rel %.1e)" % (n, ch, a["C4_a2_agg"][ch], b["C4_a2_agg"][ch], rel(a["C4_a2_agg"][ch], b["C4_a2_agg"][ch])))
        chk("C5", rel(a["C5_a4_agg"]["T_even_basis"], b["C5_a4_agg"]["T_even_basis"]) <= 5e-2, "%s a4_agg %+.4e vs %+.4e" % (n, a["C5_a4_agg"]["T_even_basis"], b["C5_a4_agg"]["T_even_basis"]))
        chk("C5", a["C5_a4_agg"]["even_basis_rms"] <= 1e-7 and b["C5_a4_agg"]["even_basis_rms"] <= 1e-7, "%s even-basis rms %.1e / %.1e" % (n, a["C5_a4_agg"]["even_basis_rms"], b["C5_a4_agg"]["even_basis_rms"]))
        chk("C5", a["C5_a4_agg"]["smallk_confirmation_rel"] <= 1e-3 and b["C5_a4_agg"]["smallk_confirmation_rel"] <= 1e-3, "%s small-k confirmation %.1e / %.1e" % (n, a["C5_a4_agg"]["smallk_confirmation_rel"], b["C5_a4_agg"]["smallk_confirmation_rel"]))
        for k in ("F_AGG_DISP_pass", "F_AGG_L_pass", "F_CONV_pass", "structure_no_odd_or_log_term"): chk("C6", a["C6_controls"][k] == b["C6_controls"][k] == True, "%s %s" % (n, k))
        chk("C7", a["C7_arm"].split()[0] == b["C7_arm"].split()[0], "%s arm %s vs %s" % (n, a["C7_arm"], b["C7_arm"]))
    print("F-AGG-UNI (reported): chat spread %.2e  cc spread %.2e" % (A["F_AGG_UNI"]["a2_over_QT_spread_rel"], B["F_AGG_UNI"]["a2_over_QT_spread_rel"]))
    if miss: print("RESULT: S9 TRIGGERED — %d miss(es); counter-cross-check before any verdict." % len(miss)); return 2
    print("RESULT: C1–C7 ALL PASS — S9 NOT triggered; two-leg aggregate result stands; fold pending author authorization."); return 0
if __name__ == "__main__": sys.exit(main(sys.argv[1], sys.argv[2]))
