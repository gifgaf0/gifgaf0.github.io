#!/usr/bin/env python3
"""lbc_2leg_compare.py — comparator for the second leg of the paper-cited LBC numbers (schema lbc_2leg_schema_v1.0).
Usage: python3 lbc_2leg_compare.py CHAT.json CC.json [OUT.json]
Every leaf of the chat checkpoint is compared with the CC value at the same dotted key, using the first matching
tolerance rule below (fnmatch on the dotted key). Missing on the CC side = MISS. Keys present only on the CC side are
listed as CC-ONLY (reported, not compared). Exit code 0 if no MISS, 1 otherwise. Free text is never compared.
Tolerance kinds: rel (|a-b| <= t*|a|), abs (|a-b| <= t), relabs (rel t1 OR abs t2), le (CC value <= t), bool, str.
"""
import json, sys, fnmatch, math

RULES = [
    ("2d.*.astar", ("rel", 0.005)),
    ("2d.*.c2", ("rel", 0.01)), ("2d.*.cT", ("rel", 0.01)), ("2d.*.c1", ("rel", 0.01)),
    ("2d.*.cT_30deg_kf005", ("rel", 0.01)),
    ("2d.*.F2", ("relabs", 0.03, 0.002)), ("2d.*.Z21", ("rel", 0.03)), ("2d.*.S2", ("abs", 0.02)),
    ("2d.*.f_s", ("rel", 0.02)),
    ("2d.*.fsum_resid_max", ("le", 1e-4)), ("2d.*.static_resid_max", ("le", 1e-4)),
    ("hydro_g22.static_share_minus", ("abs", 0.02)), ("hydro_g22.F_minus", ("relabs", 0.03, 0.002)),
    ("hydro_g22.*", ("rel", 0.02)),
    ("3d.F2*", ("relabs", 0.05, 0.0003)), ("3d.S2*", ("abs", 0.03)), ("3d.cT_*", ("rel", 0.03)), ("3d.*", ("rel", 0.02)),
    ("melting.any_c2_ge_cT", ("bool",)), ("melting.ratio_*", ("abs", 0.02)), ("melting.F2_at_Lambda_c", ("abs", 0.03)),
    ("melting.*", ("abs", 0.1)),
    ("loss.drag_prefactor_3d_coeff", ("rel", 0.01)), ("loss.xi_req_main_m*", ("rel", 0.10)), ("loss.eq3_coefficient", ("rel", 0.05)),
    ("loss.eq4_bound", ("rel", 0.01)), ("loss.*", ("abs", 0.1)),
]

def leaves(d, pre=""):
    for k, v in d.items():
        key = f"{pre}.{k}" if pre else k
        if isinstance(v, dict):
            yield from leaves(v, key)
        elif isinstance(v, list) and v and all(isinstance(x, (int, float)) for x in v):
            for i, x in enumerate(v):
                yield f"{key}[{i}]", x
        else:
            yield key, v

def rule_for(key):
    base = key.split("[")[0]
    for pat, r in RULES:
        if fnmatch.fnmatch(base, pat):
            return r
    return None

def norm(s): return str(s).replace(" ", "").lower()

def check(r, a, b):
    kind = r[0]
    if kind == "bool": return bool(a) == bool(b)
    if kind == "str": return norm(a) == norm(b)
    a, b = float(a), float(b)
    if not (math.isfinite(a) and math.isfinite(b)): return False
    if kind == "rel": return abs(a - b) <= r[1]*abs(a)
    if kind == "abs": return abs(a - b) <= r[1]
    if kind == "relabs": return abs(a - b) <= r[1]*abs(a) or abs(a - b) <= r[2]
    if kind == "le": return b <= r[1]
    raise ValueError(kind)

def main():
    chat = json.load(open(sys.argv[1])); cc = json.load(open(sys.argv[2]))
    assert chat.get("schema") == cc.get("schema") == "lbc_2leg_schema_v1.0", "schema mismatch"
    C = dict(leaves({k: v for k, v in chat.items() if k not in ("schema", "leg")}))
    K = dict(leaves({k: v for k, v in cc.items() if k not in ("schema", "leg")}))
    out = {"pass": [], "miss": [], "cc_only": sorted(set(K) - set(C))}
    for key, a in C.items():
        r = rule_for(key)
        if r is None:
            out["miss"].append({"key": key, "why": "no tolerance rule"}); continue
        if key not in K:
            out["miss"].append({"key": key, "why": "missing on CC side", "chat": a}); continue
        ok = check(r, a, K[key])
        (out["pass"] if ok else out["miss"]).append({"key": key, "chat": a, "cc": K[key], "rule": list(r)})
    print(f"checks: {len(C)}  PASS: {len(out['pass'])}  MISS: {len(out['miss'])}  CC-only: {len(out['cc_only'])}")
    for m in out["miss"]:
        print("  MISS", m)
    if len(sys.argv) > 3:
        json.dump(out, open(sys.argv[3], "w"), indent=1, default=str)
    sys.exit(1 if out["miss"] else 0)

if __name__ == "__main__":
    main()
