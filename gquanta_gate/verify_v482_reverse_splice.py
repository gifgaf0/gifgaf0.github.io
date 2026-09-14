#!/usr/bin/env python3
"""CC-side independent verification of the delivered V4.82.

Extracts the seven edit literals from foldin_v4_82_gquanta.py by AST (the fold script is
never executed), then reverses them against the delivered V4.82 and checks the result
hashes to the locked V4.81 md5. Confirms the fold without needing V4.81 itself.
"""
import ast, hashlib, sys

SCRIPT, LEDGER = sys.argv[1], sys.argv[2]
V481 = "b4e55aaea76a2152f7b1873309aec077"
V481_BYTES = 1529485

tree = ast.parse(open(SCRIPT, encoding="utf-8").read())
WANT = {"AUTH_MD5", "AUTH_BYTES", "T_OLD", "T_NEW", "A_OLD", "A_SUM",
        "R_ANCH", "RECORD", "J_ANCH", "SEC_P", "ROW_V", "ROW_VI", "CH_NEW"}
ns = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1:
        t = node.targets[0]
        names = [t.id] if isinstance(t, ast.Name) else \
                [e.id for e in t.elts] if isinstance(t, ast.Tuple) else []
        if names and set(names) & WANT:
            val = eval(compile(ast.Expression(node.value), "<lit>", "eval"), {"__builtins__": {}}, ns)
            if len(names) == 1:
                ns[names[0]] = val
            else:
                for n, v in zip(names, val):
                    ns[n] = v
missing = WANT - set(ns)
assert not missing, f"could not extract: {missing}"
print(f"extracted {len(ns)} edit literals from {SCRIPT.split('/')[-1]} (script not executed)")

s = open(LEDGER, encoding="utf-8").read()
raw = open(LEDGER, "rb").read()
print(f"delivered V4.82: {len(raw):,} B  md5 {hashlib.md5(raw).hexdigest()}")

# --- forward-edit presence: each inserted fragment must appear exactly once
for name in ("T_NEW", "A_SUM", "RECORD", "SEC_P", "ROW_V", "ROW_VI", "CH_NEW"):
    n = s.count(ns[name])
    print(f"  {'OK  ' if n == 1 else 'FAIL'} {name} present exactly once (count={n})")
    assert n == 1, name
# --- pre-edit fragments must be absent
for name in ("T_OLD", "A_OLD"):
    n = s.count(ns[name])
    print(f"  {'OK  ' if n == 0 else 'FAIL'} {name} absent (count={n})")
    assert n == 0, name
# --- §2.52 Open 3 frozen row present and unique
o3 = [l for l in s.split("\n") if l.startswith("| **§2.52 Open 3**")]
print(f"  {'OK  ' if len(o3) == 1 else 'FAIL'} §2.52 Open 3 row unique (count={len(o3)})")
assert len(o3) == 1

# --- reverse the seven edits (independent reimplementation, not the script's code)
rev = s
for frag in (ns["CH_NEW"], ns["ROW_VI"], ns["ROW_V"]):
    before = rev
    rev = rev.replace("\n" + frag, "", 1)
    assert rev != before
rev = rev.replace(ns["SEC_P"], "", 1)
rev = rev.replace(ns["RECORD"], "", 1)
rev = rev.replace(ns["A_SUM"], ns["A_OLD"], 1)
rev = rev.replace(ns["T_NEW"], ns["T_OLD"], 1)

b = rev.encode("utf-8")
got = hashlib.md5(b).hexdigest()
print(f"\nreverse-splice result: {len(b):,} B  md5 {got}")
print(f"locked V4.81:          {V481_BYTES:,} B  md5 {V481}")
ok = got == V481 and len(b) == V481_BYTES
print("REVERSE-SPLICE: " + ("BYTE-IDENTICAL TO V4.81 — PASS" if ok else "FAIL"))
print(f"delta V4.81 -> V4.82: +{len(raw) - V481_BYTES:,} B")
sys.exit(0 if ok else 1)
