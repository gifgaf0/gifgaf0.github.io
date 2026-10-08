#!/usr/bin/env python3
"""ls_twoleg_compare.py -- frozen before leg 2 returns (LS_PREREG.md §9).

Usage: python3 ls_twoleg_compare.py leg2/leg2_result.json

PASS iff: relative deviation <= 1e-6 on every D_lt, every d_max (arm x reading x
configuration), every record/reference union edge, d_comb, a_max(N), every dispersion
value and every texture t_max; the same decisive arm; identical EMPTY_P / EMPTY_D flags
at N = 20, 100, 1000.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PINS = {"ls_leg1.json": "9fd7a9ea0b1a0027b036d4e30d511068", "ls_compare.json": "a672887a43e912ef1d77d00dc5a83d5a"}
for fn, want in PINS.items():
    got = hashlib.md5(open(os.path.join(HERE, fn), "rb").read()).hexdigest()
    if got != want:
        sys.exit("HALT: %s md5 %s != %s" % (fn, got, want))
L1 = json.load(open(os.path.join(HERE, "ls_leg1.json")))
CMP = json.load(open(os.path.join(HERE, "ls_compare.json")))
L2_path = sys.argv[1]
L2 = json.load(open(L2_path))
TOL = 1e-6
CFGS = ["hex:step", "hex:gem8", "cubic:step", "cubic:gem8"]
NS = ["20", "100", "1000"]
checks = []


def rel(a, b):
    return abs(a - b) / abs(a)


def num(name, a, b):
    try:
        d = rel(float(a), float(b))
        ok = d <= TOL
    except Exception as exc:  # missing or malformed value
        d, ok = str(exc), False
    checks.append({"check": name, "leg1": a, "leg2": b, "rel_dev": d, "pass": ok})


def same(name, a, b):
    checks.append({"check": name, "leg1": a, "leg2": b, "pass": a == b})


for z, v in L1["D_lt"].items():
    num("D_lt(%s)" % z, v["m"], L2.get("D_lt_m", {}).get(z))

for arm, v1 in L1["arms"].items():
    v2 = L2.get("arms", {}).get(arm, {})
    r2 = {(r["E_tag"], r["D_tag"], r["k_tag"]): r for r in v2.get("readings", [])}
    for r in v1["readings"]:
        key = (r["E_tag"], r["D_tag"], r["k_tag"])
        for c in CFGS:
            num("%s %s %s" % (arm, "/".join(key), c), r["d_max"][c], r2.get(key, {}).get("d_max", {}).get(c))
    same("%s reading set" % arm, sorted("/".join(k) for k in [(r["E_tag"], r["D_tag"], r["k_tag"]) for r in v1["readings"]]),
         sorted("/".join(k) for k in r2))
    num("%s record_union" % arm, v1["record_union"], v2.get("record_union"))
    num("%s reference_union" % arm, v1["reference_union"], v2.get("reference_union"))

num("d_comb", L1["combined"]["d_comb"], L2.get("combined", {}).get("d_comb"))
same("decisive arm", L1["combined"]["decisive_arm"], L2.get("combined", {}).get("decisive_arm"))
for N in NS:
    num("a_max(%s)" % N, L1["combined_a_max"][N]["a_max_m"], L2.get("a_max_N_m", {}).get(N))
    same("EMPTY_P(%s)" % N, CMP["combined"]["per_N"][N]["EMPTY_P"], L2.get("EMPTY_P", {}).get(N))
    same("EMPTY_D(%s)" % N, CMP["combined"]["per_N"][N]["EMPTY_D"], L2.get("EMPTY_D", {}).get(N))

DMAP = {"6.9e11GeV|GK": "record_6.9e11GeV|GK", "6.9e11GeV|GM": "record_6.9e11GeV|GM",
        "6e-8EPl|GK": "abstract_6e-8EPl|GK", "6e-8EPl|GM": "abstract_6e-8EPl|GM"}
for k2, k1 in DMAP.items():
    num("dispersion %s" % k2, L1["dispersion"]["a_max"][k1]["m"], L2.get("dispersion_m", {}).get(k2))

for r, d1 in L1["texture"]["t_max"].items():
    for key, v in d1.items():
        num("t_max %s %s" % (r, key), v, L2.get("texture_t_max", {}).get(r, {}).get(key))

npass = sum(1 for c in checks if c["pass"])
worst = max((c["rel_dev"] for c in checks if isinstance(c.get("rel_dev"), float)), default=0.0)
verdict = "PASS" if npass == len(checks) else "MISS"
res = {"leg2_file": L2_path, "leg2_md5": hashlib.md5(open(L2_path, "rb").read()).hexdigest(),
       "tolerance": TOL, "n_checks": len(checks), "n_pass": npass, "worst_rel_dev": worst,
       "verdict": verdict, "checks": checks}
with open(os.path.join(HERE, "ls_twoleg_compare.json"), "w") as f:
    json.dump(res, f, indent=1, sort_keys=True)
print("two-leg comparison: %d/%d pass, worst rel dev %.3e -> %s" % (npass, len(checks), worst, verdict))
for c in checks:
    if not c["pass"]:
        print("  MISS:", c["check"], c.get("leg1"), c.get("leg2"), c.get("rel_dev"))
