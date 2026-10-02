#!/usr/bin/env python3
"""g_vs1_compare_v1_0.py — Gate G-VS1 two-leg comparator v1.0 (frozen at lock with schema v1.0).
Usage:  python3 g_vs1_compare_v1_0.py compare CHAT.json CC.json [out.json]
        python3 g_vs1_compare_v1_0.py selftest
Every check is exact equality of JSON values (strings of exact rationals, integers, booleans, lists, dicts); no tolerance.
Checks: C-VS-0 identity (equal locked artifacts; different instruments; equal elections); C-VS-1 Phase 0; C-VS-2 Phase 1;
C-VS-3 Phase 2 (stratum table + sampling); C-VS-4 Phase 3 (F-a map + forcing table); C-VS-5 verdict class code;
C-VS-6 T1 post-write hits empty on both legs. A (preread, preread) pair compares C-VS-0, C-VS-1 and C-VS-6 only.
Misses in the per-stratum 'invariants.*' keys are flagged REPRESENTATIONAL (a leg may use other rational representatives) — S9-eligible."""
import json, sys, hashlib, copy
SCHEMA = "g_vs1_schema_v1_0.json"; SCHEMA_MD5 = "4690e07d5a22cc7a1c5d08db39eda3fe"

def get(d, path):
    cur = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur: return ("<MISSING>",)
        cur = cur[part]
    return cur
def eq(a, b): return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)

def compare(A, B, schema):
    res = []
    def check(cid, name, va, vb, kind="EXACT"):
        ok = eq(va, vb)
        res.append(dict(check=cid, name=name, result="PASS" if ok else "MISS", kind=kind, chat=va if not ok else None, cc=vb if not ok else None))
    preread = (A.get("mode") == "preread" and B.get("mode") == "preread")
    # C-VS-0 identity
    for k in schema["identity"]["compared_equal"]: check("C-VS-0", f"identity.{k}", get(A, f"identity.{k}"), get(B, f"identity.{k}"))
    for k in schema["identity"]["compared_different"]:
        va, vb = get(A, f"identity.{k}"), get(B, f"identity.{k}")
        res.append(dict(check="C-VS-0", name=f"identity.{k} differ", result="PASS" if (va != vb and "<MISSING>" not in (va, vb)) else "MISS", kind="DIFFERENT", chat=va, cc=vb))
    # C-VS-1 Phase 0
    for sec in ("0a", "0b", "0c", "0d", "0e", "0f"):
        for k in schema["phase0"][sec]["compared"]: check("C-VS-1", f"phase0.{sec}.{k}", get(A, f"phase0.{sec}.{k}"), get(B, f"phase0.{sec}.{k}"))
    for k in schema["phase0"]["compared"]: check("C-VS-1", f"phase0.{k}", get(A, f"phase0.{k}"), get(B, f"phase0.{k}"))
    if not preread:
        for k in schema["phase1"]["compared"]: check("C-VS-2", f"phase1.{k}", get(A, f"phase1.{k}"), get(B, f"phase1.{k}"))
        for lab in schema["phase2"]["stratum_labels"]:
            for k in schema["phase2"]["per_stratum_compared"]:
                kind = "REPRESENTATIONAL" if k.startswith("invariants.") else "EXACT"
                check("C-VS-3", f"phase2.strata.{lab}.{k}", get(A, f"phase2.strata.{lab}.{k}"), get(B, f"phase2.strata.{lab}.{k}"), kind)
        for k in schema["phase2"]["compared"]: check("C-VS-3", f"phase2.{k}", get(A, f"phase2.{k}"), get(B, f"phase2.{k}"))
        for form in schema["phase3"]["forms"]:
            deg = get(A, f"phase3.F_a.{form}.degree")
            keys = schema["phase3"]["per_form_compared_deg4"] if deg == 4 else schema["phase3"]["per_form_compared_deg2"]
            for k in keys: check("C-VS-4", f"phase3.F_a.{form}.{k}", get(A, f"phase3.F_a.{form}.{k}"), get(B, f"phase3.F_a.{form}.{k}"))
        for k in schema["phase3"]["compared"]: check("C-VS-4", f"phase3.{k}", get(A, f"phase3.{k}"), get(B, f"phase3.{k}"))
        check("C-VS-5", "verdict.class_code", get(A, "verdict.class_code"), get(B, "verdict.class_code"))
    for leg, D in (("chat", A), ("cc", B)):
        hits = get(D, "T1_post_write.hits")
        res.append(dict(check="C-VS-6", name=f"T1_post_write.hits ({leg}) empty", result="PASS" if hits == [] else "MISS", kind="EXACT", chat=hits if leg == "chat" else None, cc=hits if leg == "cc" else None))
    n = len(res); misses = [r for r in res if r["result"] != "PASS"]
    rep = [r for r in misses if r["kind"] == "REPRESENTATIONAL"]
    summary = dict(checks=n, passed=n - len(misses), misses=len(misses), representational_misses=len(rep), exact_misses=len(misses) - len(rep),
                   preread_pair=preread, verdict_codes=[get(A, "verdict.class_code"), get(B, "verdict.class_code")],
                   ALL_PASS=(len(misses) == 0), schema_md5=SCHEMA_MD5)
    return dict(summary=summary, results=res)

def selftest():
    """builds a synthetic pair from a minimal skeleton: identical legs must PASS everything; a perturbed stratum pi1 must MISS exactly once;
    a changed representative must produce REPRESENTATIONAL misses only on invariants.*; identical instrument md5 must MISS C-VS-0."""
    schema = json.load(open(SCHEMA))
    def skel(inst):
        d = dict(gate="G-VS1", leg="x", mode="run", identity={k: "v" for k in schema["identity"]["required"]}, phase0={}, phase1={}, phase2={"strata": {}}, phase3={"F_a": {}, "forcing_table": {}}, verdict={"class_code": "VC-3"}, T1_post_write={"hits": []})
        d["identity"]["instrument_md5"] = inst; d["identity"]["elections"] = {"E-VS-1": "a"}
        for sec in ("0a", "0b", "0c", "0d", "0e", "0f"):
            d["phase0"][sec] = {}
            for k in schema["phase0"][sec]["compared"]:
                cur = d["phase0"][sec]
                parts = k.split(".")
                for p in parts[:-1]: cur = cur.setdefault(p, {})
                cur[parts[-1]] = 1
        d["phase0"]["all_pass"] = True
        for k in schema["phase1"]["compared"]:
            cur = d["phase1"]; parts = k.split(".")
            for p in parts[:-1]: cur = cur.setdefault(p, {})
            cur[parts[-1]] = "1"
        for lab in schema["phase2"]["stratum_labels"]:
            st = {}
            for k in schema["phase2"]["per_stratum_compared"]:
                cur = st; parts = k.split(".")
                for p in parts[:-1]: cur = cur.setdefault(p, {})
                cur[parts[-1]] = "Z"
            d["phase2"]["strata"][lab] = st
        for k in schema["phase2"]["compared"]:
            cur = d["phase2"]; parts = k.split(".")
            for p in parts[:-1]: cur = cur.setdefault(p, {})
            cur[parts[-1]] = True
        for form in schema["phase3"]["forms"]:
            deg = 2 if form.startswith("D-a") else 4
            keys = schema["phase3"]["per_form_compared_deg4"] if deg == 4 else schema["phase3"]["per_form_compared_deg2"]
            d["phase3"]["F_a"][form] = {k: ("x" if k != "degree" else deg) for k in keys}
        for k in schema["phase3"]["compared"]:
            cur = d["phase3"]; parts = k.split(".")
            for p in parts[:-1]: cur = cur.setdefault(p, {})
            cur[parts[-1]] = "MAP"
        return d
    A, B = skel("aaa"), skel("bbb")
    r1 = compare(A, B, schema); t1 = r1["summary"]["ALL_PASS"]
    B2 = copy.deepcopy(B); B2["phase2"]["strata"]["F7"]["pi1"] = "0"
    r2 = compare(A, B2, schema); t2 = (r2["summary"]["misses"] == 1 and r2["summary"]["exact_misses"] == 1)
    B3 = copy.deepcopy(B); B3["phase2"]["strata"]["I7"]["invariants"]["rho_norm"] = "1/2"
    r3 = compare(A, B3, schema); t3 = (r3["summary"]["misses"] == 1 and r3["summary"]["representational_misses"] == 1)
    B4 = copy.deepcopy(B); B4["identity"]["instrument_md5"] = "aaa"
    r4 = compare(A, B4, schema); t4 = (r4["summary"]["misses"] == 1 and any(r["name"].endswith("differ") and r["result"] == "MISS" for r in r4["results"]))
    B5 = copy.deepcopy(B); B5["T1_post_write"]["hits"] = [3]
    r5 = compare(A, B5, schema); t5 = (r5["summary"]["misses"] == 1)
    A6, B6 = copy.deepcopy(A), copy.deepcopy(B); A6["mode"] = B6["mode"] = "preread"; A6["phase1"] = B6["phase1"] = None
    r6 = compare(A6, B6, schema); t6 = (r6["summary"]["ALL_PASS"] and r6["summary"]["preread_pair"] and r6["summary"]["checks"] < r1["summary"]["checks"])
    B7 = copy.deepcopy(B); B7["verdict"]["class_code"] = "VC-4"
    r7 = compare(A, B7, schema); t7 = (r7["summary"]["misses"] == 1)
    tests = dict(identical_pass=t1, pi1_miss=t2, representational_miss=t3, same_instrument_miss=t4, t1_hit_miss=t5, preread_pair=t6, verdict_miss=t7, total_checks=r1["summary"]["checks"])
    n_ok = sum(1 for k, v in tests.items() if k != "total_checks" and v)
    print("SELFTEST", "PASS" if n_ok == 7 else "FAIL", f"({n_ok}/7)", tests)
    return n_ok == 7

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("compare", "selftest"): print(__doc__); sys.exit(1)
    if sys.argv[1] == "selftest": sys.exit(0 if selftest() else 1)
    schema = json.load(open(SCHEMA))
    if hashlib.md5(open(SCHEMA, "rb").read()).hexdigest() != SCHEMA_MD5: print("HALT: schema md5 mismatch"); sys.exit(2)
    A = json.load(open(sys.argv[2])); B = json.load(open(sys.argv[3]))
    out = compare(A, B, schema)
    s = out["summary"]
    print(f"G-VS1 two-leg comparison: {s['checks']} checks, {s['passed']} PASS, {s['misses']} MISS ({s['representational_misses']} representational, {s['exact_misses']} exact); verdict codes {s['verdict_codes']}; ALL_PASS={s['ALL_PASS']}")
    for r in out["results"]:
        if r["result"] != "PASS": print("  MISS", r["check"], r["name"], r["kind"])
    if len(sys.argv) > 4: open(sys.argv[4], "w").write(json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False))
