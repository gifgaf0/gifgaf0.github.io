#!/usr/bin/env python3
"""g_mscs2_compare_v1_1.py — two-leg comparator for Gate G-MSCS2, v1.1 CANDIDATE (September 26, 2026; NOT frozen until the author's S9 election).

v1.1 = v1.0 (80d3b907) with the schema v1.1 CANDIDATE asserted (its one delta: the cubic quadform null tolerance at the gate's absolute
kappa floor, 1e-6, in place of 1e-10). The comparator logic is unchanged; the tolerance is read from the schema. Row count unchanged (356).

Compares the chat-leg and CC-leg checkpoints against g_mscs2_schema_v1_0.json.
Checks: C0 provenance + independence witness; C1 Phase 0 (13 pins/controls: passed on both legs AND the
float rule re-evaluated per leg from the reported float); C2 Phase 2 per configuration/arm key (12-point arrays
elementwise; S4/biref absolute; kappas relative with an absolute floor — a null compares as a null, never 0/0;
the hex quadratic form; the cubic quadform null); C3 Phase 3 (verdict identity, verdict recomputed from the
states by the schema rule, falsifier states). Free text is never compared.

Usage:
  compare  : python3 g_mscs2_compare_v1_1.py compare CHAT.json CC.json [--schema S.json] [--out OUT.json]
  selftest : python3 g_mscs2_compare_v1_1.py selftest
Exit: 0 all PASS, 1 any MISS, 2 usage/fatal.
"""
import hashlib, json, sys, copy, math

SCHEMA_DEFAULT = "g_mscs2_schema_v1_1_CANDIDATE.json"
SCHEMA_MD5 = "d270899c95a2b69c3adf818a69667490"   # schema v1.1 CANDIDATE md5; asserted at load

def md5_file(p): return hashlib.md5(open(p, "rb").read()).hexdigest()

def load_schema(path):
    raw = open(path, "rb").read(); h = hashlib.md5(raw).hexdigest()
    if h != SCHEMA_MD5: raise SystemExit(f"FATAL: schema md5 {h} != frozen {SCHEMA_MD5}")
    return json.loads(raw.decode("utf-8")), h

def isnum(v): return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)

def get(d, path, default=None):
    cur = d
    for k in path.split("."):
        if not isinstance(cur, dict) or k not in cur: return default
        cur = cur[k]
    return cur

class Rec:
    def __init__(self): self.rows = []
    def add(self, check, name, ok, a=None, b=None, note=""):
        self.rows.append({"check": check, "name": name, "pass": bool(ok), "chat": a, "cc": b, "note": note})
    def summary(self):
        n = len(self.rows); p = sum(r["pass"] for r in self.rows); return {"checks": n, "pass": p, "miss": n - p}

def rule_ok(v, rule):
    if not isnum(v): return False
    r = rule["rule"]
    if r == "le": return v <= rule["threshold"]
    if r == "ge": return v >= rule["threshold"]
    if r == "gt": return v > rule["threshold"]
    if r == "le_rel_floor": return True   # handled with context
    return False

def rel_floor_ok(a, b, rel, floor):
    return isnum(a) and isnum(b) and abs(a - b) <= max(rel * max(abs(a), abs(b)), floor)

def recompute_verdict(ck, S):
    P0 = get(ck, "phase0", {}) or {}
    if any(get(P0, f"{it}.passed") is not True for it in S["phase0"]["items"]): return "INDETERMINATE"
    P2 = get(ck, "phase2", {}) or {}
    tau, floor = S["tolerances"]["tau_agg"], S["tolerances"]["kappa_floor"]
    worst = 0.0
    for k in S["keys"]:
        for f in ("S4_E2", "S4_h"):
            v = get(P2, f"{k}.{f}")
            if not isnum(v): return "INDETERMINATE"
            worst = max(worst, abs(v))
    if worst > tau: return "PROTECTION-BREACH"
    if all(isnum(get(P2, f"{k}.kappa44_E2")) and abs(get(P2, f"{k}.kappa44_E2")) <= floor for k in S["primary_cubic_keys"]): return "L4-NULL"
    return "IDENTITY-DELIVERED-L4"

def compare(chat, cc, S):
    R = Rec()
    # ---------------- C0 provenance ----------------
    for k in S["required_top"]:
        R.add("C0", f"required key {k} present (chat)", k in chat); R.add("C0", f"required key {k} present (cc)", k in cc)
    for k in ("memo_lock_md5", "ledger_base_md5", "t1_list_md5", "x1_md5", "x6_chat_md5", "x6_cc_md5"):
        R.add("C0", f"{k} == schema (chat)", chat.get(k) == S[k], chat.get(k), S[k]); R.add("C0", f"{k} == schema (cc)", cc.get(k) == S[k], cc.get(k), S[k])
    R.add("C0", "gate label", chat.get("gate") == S["gate"] and cc.get("gate") == S["gate"], chat.get("gate"), cc.get("gate"))
    R.add("C0", "leg labels chat/cc", chat.get("leg") == "chat" and cc.get("leg") == "cc", chat.get("leg"), cc.get("leg"))
    for f in S["t1_scan_required"]:
        R.add("C0", f"t1_scan.{f} CLEAN (chat)", get(chat, f"t1_scan.{f}") in S["t1_scan_domain"], get(chat, f"t1_scan.{f}"))
        R.add("C0", f"t1_scan.{f} CLEAN (cc)", get(cc, f"t1_scan.{f}") in S["t1_scan_domain"], None, get(cc, f"t1_scan.{f}"))
    R.add("C0", "elections == schema (chat)", chat.get("elections") == S["elections"], chat.get("elections"), S["elections"])
    R.add("C0", "elections == schema (cc)", cc.get("elections") == S["elections"], cc.get("elections"), S["elections"])
    R.add("C0", "independence witness: instrument_md5 differ", bool(chat.get("instrument_md5")) and bool(cc.get("instrument_md5")) and chat.get("instrument_md5") != cc.get("instrument_md5"), chat.get("instrument_md5"), cc.get("instrument_md5"))
    # ---------------- C1 phase0 ----------------
    A, B = chat.get("phase0", {}) or {}, cc.get("phase0", {}) or {}
    for it in S["phase0"]["items"]:
        pa, pb = get(A, f"{it}.passed"), get(B, f"{it}.passed")
        R.add("C1", f"phase0.{it}.passed true both legs", pa is True and pb is True, pa, pb)
        for fk, rule in S["phase0"]["float_rules"].get(it, {}).items():
            for leg, D in (("chat", A), ("cc", B)):
                v = get(D, f"{it}.{fk}")
                R.add("C1", f"phase0.{it}.{fk} ({leg}) {rule['rule']} {rule['threshold']}", rule_ok(v, rule), v if leg == "chat" else None, v if leg == "cc" else None)
    # ---------------- C2 phase2 ----------------
    P2 = S["phase2"]; A, B = chat.get("phase2", {}) or {}, cc.get("phase2", {}) or {}
    for k in S["keys"]:
        ka, kb = A.get(k) or {}, B.get(k) or {}
        R.add("C2", f"phase2[{k}] present both legs", bool(ka) and bool(kb))
        for ak, n in P2["array_keys"].items():
            va, vb = ka.get(ak), kb.get(ak)
            okl = isinstance(va, list) and isinstance(vb, list) and len(va) == n and len(vb) == n and all(isnum(x) for x in va + vb)
            R.add("C2", f"phase2[{k}].{ak} length {n} both legs", okl, len(va) if isinstance(va, list) else None, len(vb) if isinstance(vb, list) else None)
            worst = max((abs(x - y) for x, y in zip(va, vb)), default=float("inf")) if okl else float("inf")
            R.add("C2", f"phase2[{k}].{ak} elementwise <= {P2['array_tol_abs']}", okl and worst <= P2["array_tol_abs"], None, None, f"worst {worst:.3e}" if okl else "")
        for fk, tol in P2["abs_keys"].items():
            va, vb = ka.get(fk), kb.get(fk)
            R.add("C2", f"phase2[{k}].{fk} abs <= {tol}", isnum(va) and isnum(vb) and abs(va - vb) <= tol, va, vb)
        for fk, (rel, floor) in P2["rel_keys"].items():
            va, vb = ka.get(fk), kb.get(fk)
            R.add("C2", f"phase2[{k}].{fk} rel <= {rel} (floor {floor})", rel_floor_ok(va, vb, rel, floor), va, vb)
        for fk, rule in P2["per_leg_rules"].items():
            for leg, D in (("chat", ka), ("cc", kb)):
                v = D.get(fk); kv = D.get("kappa44_E2")
                ok = isnum(v) and isnum(kv) and v <= max(rule["rel"] * abs(kv), rule["floor"])
                R.add("C2", f"phase2[{k}].{fk} ({leg}) <= max(rel*|kappa44|, floor)", ok, v if leg == "chat" else None, v if leg == "cc" else None)
        qa, qb = ka.get("quadform") or {}, kb.get("quadform") or {}
        for fk, (rel, floor) in P2["quadform_keys"].items():
            va, vb = qa.get(fk), qb.get(fk)
            R.add("C2", f"phase2[{k}].quadform.{fk} rel <= {rel} (floor {floor})", rel_floor_ok(va, vb, rel, floor), va, vb)
        if k in S["cubic_keys"]:
            for fk in ("kappa22", "kappa24"):
                for leg, Q in (("chat", qa), ("cc", qb)):
                    v = Q.get(fk)
                    R.add("C2", f"phase2[{k}].quadform.{fk} ({leg}) cubic null abs <= {P2['quadform_cubic_null_abs']}", isnum(v) and abs(v) <= P2["quadform_cubic_null_abs"], v if leg == "chat" else None, v if leg == "cc" else None)
    # ---------------- C3 phase3 ----------------
    P3 = S["phase3"]; A, B = chat.get("phase3", {}) or {}, cc.get("phase3", {}) or {}
    for fk, t in P3["exact_keys"].items():
        va, vb = A.get(fk), B.get(fk)
        R.add("C3", f"phase3.{fk} typed str both legs", isinstance(va, str) and isinstance(vb, str), va, vb)
        R.add("C3", f"phase3.{fk} equal", isinstance(va, str) and va == vb, va, vb)
    for leg, D in (("chat", A), ("cc", B)):
        R.add("C3", f"phase3.verdict_class in domain ({leg})", D.get("verdict_class") in P3["verdict_domain"], D.get("verdict_class") if leg == "chat" else None, D.get("verdict_class") if leg == "cc" else None)
        for fk, rule in P3["float_keys"].items():
            v = D.get(fk); R.add("C3", f"phase3.{fk} ({leg}) {rule['rule']} {rule['threshold']}", rule_ok(v, rule), v if leg == "chat" else None, v if leg == "cc" else None)
    for leg, ck, D in (("chat", chat, A), ("cc", cc, B)):
        rv = recompute_verdict(ck, S)
        R.add("C3", f"verdict recomputed == reported ({leg})", rv == D.get("verdict_class"), rv if leg == "chat" else None, rv if leg == "cc" else None, f"reported {D.get('verdict_class')}")
        ws = max([abs(get(ck, f"phase2.{k}.{f}", float('nan'))) for k in S["keys"] for f in ("S4_E2", "S4_h")], default=float("nan"))
        R.add("C3", f"worst_S4 consistent with phase2 ({leg})", isnum(D.get("worst_S4")) and isnum(ws) and abs(D.get("worst_S4") - ws) <= 1e-15, None, None)
        fm3 = "FIRES" if isnum(ws) and ws > S["tolerances"]["tau_agg"] else "SILENT"
        R.add("C3", f"F-MS2-3 state consistent ({leg})", D.get("F-MS2-3") == fm3, D.get("F-MS2-3") if leg == "chat" else None, D.get("F-MS2-3") if leg == "cc" else None)
    return R

# ---------------------------------------------------------------- selftest
T4 = [-0.5, -0.25, -0.1, -0.05, -0.02, 0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0]
def canonical_checkpoint(leg, S):
    """Synthetic checkpoint carrying the memo's a-priori shape (HYP-MS2-1..5). NOT a result."""
    prov = {k: S[k] for k in ("memo_lock_md5", "ledger_base_md5", "t1_list_md5", "x1_md5", "x6_chat_md5", "x6_cc_md5")}
    p0 = {}
    vals = {"PIN-XTAL": {"worst_rel": 1e-12}, "PIN-VRH0": {"worst_rel": 3e-12}, "PIN-HS0": {"worst_rel": 2e-9}, "PIN-K2": {"worst_rel_hex_kappa2": 2e-6, "worst_abs_cubic_kappa2": 1e-15},
            "F-CTRL-ISO": {"worst_abs": 1e-14}, "F-CTRL-SO3": {"dev_from_0p4": 4e-15, "r_agg_0_abs": 1e-14}, "F-CTRL-POS": {"min_odf_weight": 0.5},
            "F-CTRL-L2NULL": {"worst_abs": 4e-14}, "F-CTRL-L4EXHAUST": {"worst_rel_tensor": 2e-15, "worst_abs_r_agg": 1e-15},
            "F-CTRL-C4": {"worst_rel_affine": 1e-14, "worst_rel_closed_form": 4e-15, "h0_effect_rel": 1e-15}, "F-CTRL-MARG": {"worst_abs": 2e-14},
            "F-CTRL-TEX4": {"r_agg_t1_abs": 2.3e-3}, "F-CTRL-QUAD": {"doubling_residual": 1e-13}}
    for it in S["phase0"]["items"]:
        p0[it] = dict(vals[it]); p0[it]["passed"] = True
    p2 = {}
    for i, k in enumerate(S["keys"]):
        cub = k.startswith("cubic"); kap = (-3.1e-3 if "001" in k else 2.2e-3) if cub else -0.9e-3
        eps = 1e-9 if leg == "cc" else 0.0
        r = [kap * t * t - 0.4e-3 * t**3 + eps for t in T4]
        p2[k] = {"r_agg_E2_VRH": r, "r_agg_h_VRH": [x * 1e-3 for x in r], "r_agg_E2_HS": [x * 0.99 for x in r], "r_agg_E2_V": [x * 1.02 for x in r], "r_agg_E2_R": [x * 0.98 for x in r],
                 "lambda_mean_t4": [1e-5 * t * t for t in T4], "S4_E2": 2e-13 + eps, "S4_h": 1e-13, "biref_b1_VRH": (0.12 if cub else 0.05) + eps,
                 "kappa44_E2": kap * (1 + eps), "kappa44_h": kap * 1e-3, "kappa444_E2": -0.4e-3, "kappa44_E2_HS": kap * 0.99, "halving_dev_kappa44": abs(kap) * 2e-5,
                 "vT_VRH": 8.4 + i * 0.1, "vT_HS_lo": 8.39 + i * 0.1, "vT_HS_hi": 8.41 + i * 0.1,
                 "quadform": {"kappa22": (0.0 if cub else -1.44e-3) + (1e-16 if cub else eps), "kappa24": (0.0 if cub else -0.5e-3) + (2e-16 if cub else eps), "kappa44": kap * (1 + eps), "residual": 1e-9}}
    ck = {"gate": "G-MSCS2", "leg": leg, "instrument_md5": ("chat" * 8) if leg == "chat" else ("cc00" * 8), **prov,
          "t1_scan": {"instrument": "CLEAN", "memo": "CLEAN"}, "elections": dict(S["elections"]), "phase0": p0, "phase2": p2,
          "phase3": {"verdict_class": "IDENTITY-DELIVERED-L4", "F-MS2-3": "SILENT", "F-MS2-4": "SILENT", "F-MS2-2": "REGISTERED_NOT_EXECUTED", "worst_S4": 2e-13 + eps}}
    return ck

def run(chat, cc, S):
    R = compare(chat, cc, S); return R, R.summary()

def selftest():
    S, h = load_schema(SCHEMA_DEFAULT); suites = []
    def suite(name, mut, expect_miss_min=1, expect_pass=False):
        a, b = canonical_checkpoint("chat", S), canonical_checkpoint("cc", S); mut(a, b); R, s = run(a, b, S)
        ok = (s["miss"] == 0) if expect_pass else (s["miss"] >= expect_miss_min); suites.append((name, ok, s)); return R
    suite("S1 canonical legs (1e-9 jitter on cc) -> ALL PASS", lambda a, b: None, expect_pass=True)
    suite("S2 a Phase-0 control fails on cc (passed false) -> C1 miss + verdict recompute INDETERMINATE", lambda a, b: b["phase0"]["F-CTRL-C4"].__setitem__("passed", False), 2)
    suite("S3 passed true but float violates its rule (PIN-K2 hex 2e-4) -> C1 miss", lambda a, b: a["phase0"]["PIN-K2"].__setitem__("worst_rel_hex_kappa2", 2e-4), 1)
    suite("S4 missing required key (phase2) on chat", lambda a, b: a.pop("phase2"), 1)
    suite("S5 wrong election code", lambda a, b: a["elections"].__setitem__("E-MS2-3", "b"), 1)
    suite("S6 T1 scan HIT on memo (cc)", lambda a, b: b["t1_scan"].__setitem__("memo", "HIT"), 1)
    suite("S7 identical instrument md5 (independence witness)", lambda a, b: b.__setitem__("instrument_md5", a["instrument_md5"]), 1)
    suite("S8 provenance md5 mismatch (x6 chat)", lambda a, b: a.__setitem__("x6_chat_md5", "deadbeef" * 4), 1)
    suite("S9 r_agg array disagrees at 1e-5 on one key", lambda a, b: b["phase2"]["hex_step|a"]["r_agg_E2_VRH"].__setitem__(9, b["phase2"]["hex_step|a"]["r_agg_E2_VRH"][9] + 1e-5), 1)
    suite("S10 kappa44 disagrees at 1e-3 relative", lambda a, b: b["phase2"]["cubic_step|001"].__setitem__("kappa44_E2", a["phase2"]["cubic_step|001"]["kappa44_E2"] * 1.001), 1)
    suite("S11 kappa null compares as null (both legs 1e-8 vs 3e-8: within the floor) -> PASS", lambda a, b: (a["phase2"]["hex_gem8|b"].__setitem__("kappa44_h", 1e-8), b["phase2"]["hex_gem8|b"].__setitem__("kappa44_h", 3e-8)), expect_pass=True)
    suite("S12 S4 breach on one leg (3e-6) -> C2 abs miss + C3 verdict/F-MS2-3 misses", lambda a, b: a["phase2"]["hex_step|a"].__setitem__("S4_E2", 3e-6), 2)
    suite("S13 verdict inconsistent with states (both report L4-NULL while cubic kappa44 is 3e-3)", lambda a, b: (a["phase3"].__setitem__("verdict_class", "L4-NULL"), b["phase3"].__setitem__("verdict_class", "L4-NULL")), 2)
    def l4null(a, b):
        for ck in (a, b):
            for k in ("cubic_step|001", "cubic_gem8|001"):
                ck["phase2"][k]["kappa44_E2"] = 1e-8; ck["phase2"][k]["quadform"]["kappa44"] = 1e-8; ck["phase2"][k]["halving_dev_kappa44"] = 1e-9
            ck["phase3"]["verdict_class"] = "L4-NULL"; ck["phase3"]["F-MS2-4"] = "FIRES"
    suite("S14 genuine L4-NULL on both legs, consistently reported -> ALL PASS", l4null, expect_pass=True)
    suite("S15 cubic quadform kappa22 above the floor (2e-6) on cc -> miss", lambda a, b: b["phase2"]["cubic_gem8|111"]["quadform"].__setitem__("kappa22", 2e-6), 1)
    def run1_aliasing(a, b):
        for ck in (a, b):
            for k in ("cubic_step|001", "cubic_step|111", "cubic_gem8|001", "cubic_gem8|111"):
                ck["phase2"][k]["quadform"]["kappa22"] = 4.5e-9; ck["phase2"][k]["quadform"]["kappa24"] = 3.5e-7
    suite("S19 run-1 cubic aliasing values (kappa22 4.5e-9, kappa24 3.5e-7) pass at the floor -> ALL PASS", run1_aliasing, expect_pass=True)
    suite("S16 halving deviation above floor and relative bound (cc)", lambda a, b: b["phase2"]["hex_step|b"].__setitem__("halving_dev_kappa44", 5e-6), 1)
    suite("S17 array wrong length (11) on chat", lambda a, b: a["phase2"]["hex_gem8|a"].__setitem__("lambda_mean_t4", a["phase2"]["hex_gem8|a"]["lambda_mean_t4"][:11]), 1)
    suite("S18 F-CTRL-TEX4 float below its gt threshold (instrument blind) -> C1 miss", lambda a, b: a["phase0"]["F-CTRL-TEX4"].__setitem__("r_agg_t1_abs", 1e-9), 1)
    allok = all(ok for _, ok, _ in suites)
    print(f"schema md5 {h}")
    for name, ok, s in suites: print(f"  [{'PASS' if ok else 'FAIL'}] {name}  (checks={s['checks']}, pass={s['pass']}, miss={s['miss']})")
    print("SELFTEST", "PASS" if allok else "FAIL"); return 0 if allok else 1

def main():
    if len(sys.argv) < 2: print(__doc__); return 2
    if sys.argv[1] == "selftest": return selftest()
    if sys.argv[1] == "compare":
        args = sys.argv[2:]; schema = SCHEMA_DEFAULT; out = None
        if "--schema" in args: i = args.index("--schema"); schema = args[i + 1]; del args[i:i + 2]
        if "--out" in args: i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
        if len(args) != 2: print(__doc__); return 2
        S, h = load_schema(schema); chat = json.load(open(args[0], encoding="utf-8")); cc = json.load(open(args[1], encoding="utf-8"))
        R, s = run(chat, cc, S)
        res = {"comparator": "g_mscs2_compare_v1_1_CANDIDATE", "schema_md5": h, "chat_ckpt_md5": md5_file(args[0]), "cc_ckpt_md5": md5_file(args[1]), "summary": s, "misses": [r for r in R.rows if not r["pass"]], "rows": R.rows}
        txt = json.dumps(res, indent=1, ensure_ascii=False, sort_keys=True)
        if out: open(out, "w", encoding="utf-8").write(txt)
        print(f"G-MSCS2 two-leg comparison: checks={s['checks']} pass={s['pass']} miss={s['miss']}")
        for r in res["misses"]: print(f"  MISS [{r['check']}] {r['name']}: chat={r['chat']} cc={r['cc']} {r['note']}")
        return 0 if s["miss"] == 0 else 1
    print(__doc__); return 2

if __name__ == "__main__":
    sys.exit(main())
