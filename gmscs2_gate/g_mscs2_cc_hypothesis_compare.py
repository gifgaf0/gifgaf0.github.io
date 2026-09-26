#!/usr/bin/env python3
"""g_mscs2_cc_hypothesis_compare.py -- the memo section 6 hypotheses HYP-MS2-1..5 against the
CC checkpoint (dispatch step 3.5; a separate artifact, written last). Hypotheses are M-naive
expectations registered pre-data, NOT verdicts; this file records whether each is met by the
CC leg's numbers, nothing more. Usage: python3 g_mscs2_cc_hypothesis_compare.py [CKPT] [--out F]
"""
import hashlib, json, sys

def md5_file(p): return hashlib.md5(open(p, "rb").read()).hexdigest()

def main():
    args = sys.argv[1:]
    out = None
    if "--out" in args:
        i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
    ck_path = args[0] if args else "g_mscs2_ccleg_checkpoint.json"
    ck = json.load(open(ck_path, encoding="utf-8"))
    P1, P2 = ck["phase1"], ck["phase2"]
    hexk = ["hex_step|a", "hex_step|b", "hex_gem8|a", "hex_gem8|b"]
    cubk = ["cubic_step|001", "cubic_step|111", "cubic_gem8|001", "cubic_gem8|111"]
    prim = ["cubic_step|001", "cubic_gem8|001"]
    rows = []

    def add(hyp, clause, met, detail):
        rows.append({"hypothesis": hyp, "clause": clause, "met": bool(met), "detail": detail})

    # HYP-MS2-1: kappa44(S2-E2) != 0 on both fcc configurations, |kappa44| of order 1e-3 .. 1e-2;
    #            kappa44(S2-h) smaller by roughly the admixture factor
    k44 = {k: P2[k]["kappa44_E2"] for k in cubk}
    add("HYP-MS2-1", "kappa44_E2 non-zero on both primary fcc keys (above the 1e-6 floor)",
        all(abs(k44[k]) > 1e-6 for k in prim), {k: k44[k] for k in prim})
    add("HYP-MS2-1", "|kappa44_E2| of order 1e-3 .. 1e-2 on the primary fcc keys",
        all(1e-3 <= abs(k44[k]) <= 1e-2 for k in prim), {k: abs(k44[k]) for k in prim})
    ratio = {k: P2[k]["kappa44_h"] / P2[k]["kappa44_E2"] for k in cubk}
    admix = {k: P1[k]["lambda_mean"] for k in cubk}
    add("HYP-MS2-1", "kappa44_h smaller than kappa44_E2 in magnitude (ratio reported with <lambda_L> for scale)",
        all(abs(P2[k]["kappa44_h"]) < abs(P2[k]["kappa44_E2"]) for k in cubk),
        {"kappa44_h/kappa44_E2": ratio, "lambda_mean": admix})
    # HYP-MS2-2: sign kappa44(001) = sign r_xtal(001) < 0; sign kappa44(111) = sign r_xtal(111) > 0
    for k in cubk:
        rx = P1[k]["r_xtal_E2"]
        want_neg = k.endswith("|001")
        add("HYP-MS2-2", f"{k}: sign kappa44_E2 == sign r_xtal_E2 and {'< 0' if want_neg else '> 0'}",
            (k44[k] < 0) == want_neg and (rx < 0) == want_neg, {"kappa44_E2": k44[k], "r_xtal_E2": rx})
    # HYP-MS2-3: S4 = 0 within tau_agg on all keys, both arms
    ws = max(max(abs(P2[k]["S4_E2"]), abs(P2[k]["S4_h"])) for k in P2)
    add("HYP-MS2-3", "|S4_E2|, |S4_h| <= 1e-6 on every key", ws <= 1e-6, {"worst_S4": ws})
    # HYP-MS2-4: hex |kappa44| < |kappa22|; kappa24 != 0 with |kappa24| between them; kappa22 reproduces kappa2 (pin)
    for k in hexk:
        q = P2[k]["quadform"]
        add("HYP-MS2-4", f"{k}: |kappa44| < |kappa22|", abs(q["kappa44"]) < abs(q["kappa22"]), {"kappa22": q["kappa22"], "kappa44": q["kappa44"]})
        add("HYP-MS2-4", f"{k}: kappa24 non-zero (above the 1e-6 floor) with |kappa44| < |kappa24| < |kappa22|",
            abs(q["kappa24"]) > 1e-6 and abs(q["kappa44"]) < abs(q["kappa24"]) < abs(q["kappa22"]),
            {"kappa24_fit": q["kappa24"], "kappa24_richardson": P2[k]["kappa24_richardson"]})
        add("HYP-MS2-4", f"{k}: kappa22 reproduces kappa2_E2 (l = 2 family) to 1e-4 relative",
            abs(q["kappa22"] - P2[k]["kappa2_E2"]) <= 1e-4 * abs(P2[k]["kappa2_E2"]), {"kappa22": q["kappa22"], "kappa2_E2": P2[k]["kappa2_E2"]})
    # HYP-MS2-5: fcc birefringence coefficient of order 1e-1 per unit t4, two orders above the descriptor split at t4 ~ 0.25
    for k in prim:
        b1 = P2[k]["biref_b1_VRH"]
        split = abs(P2[k]["kappa44_E2"]) * 0.25 ** 2
        add("HYP-MS2-5", f"{k}: |b1| of order 1e-1 (0.03 .. 0.3)", 0.03 <= abs(b1) <= 0.3, {"biref_b1_VRH": b1})
        add("HYP-MS2-5", f"{k}: |b1| * 0.25 exceeds the descriptor split |kappa44| * 0.25^2 by >= two orders",
            abs(b1) * 0.25 / split >= 100.0, {"biref_at_0p25": abs(b1) * 0.25, "descriptor_split_at_0p25": split, "ratio": abs(b1) * 0.25 / split})
    add("Expected class", "IDENTITY-DELIVERED-L4", ck["phase3"]["verdict_class"] == "IDENTITY-DELIVERED-L4", {"verdict_class": ck["phase3"]["verdict_class"]})
    res = {"artifact": "G-MSCS2 CC-leg hypothesis compare (memo section 6; not verdicts)", "checkpoint_md5": md5_file(ck_path),
           "leg": ck["leg"], "summary": {"clauses": len(rows), "met": sum(r["met"] for r in rows), "not_met": sum(not r["met"] for r in rows)}, "rows": rows}
    txt = json.dumps(res, indent=1, ensure_ascii=False)
    if out: open(out, "w", encoding="utf-8").write(txt)
    for r in rows:
        print(f"  [{'MET' if r['met'] else 'NOT MET'}] {r['hypothesis']}: {r['clause']}")
    print(f"hypothesis compare: {res['summary']}")

if __name__ == "__main__":
    main()
