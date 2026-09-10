#!/usr/bin/env python3
# verify_v4_79_reverse_splice.py — CC-side independent verification of the
# V4.79 fold (Gate G-2a-L1). Reconstructs V4.78 byte-exactly FROM the V4.79
# canonical by inverting the eight additive edits, using the edit constants
# extracted from foldin_v4_79_g2aL1.py via AST (nothing retyped by hand).
# Verifies, without possessing V4.78:
#   * V4.79 md5/bytes == the author-authorized candidate (6cfeca22, 1,493,745 B)
#   * reverse-splice md5/bytes == V4.78 (98b9f63f, 1,474,281 B)
#   * the §2.52 Open 3 Part VI row is unique and byte-identical pre/post
#   * each of the eight edits is present exactly once in V4.79
import ast, hashlib, sys

LEDGER = "../SQT_Master_Ledger_v4_79_CANONICAL.md"
SCRIPT = "foldin_v4_79_g2aL1.py"
V479_MD5, V479_BYTES = "6cfeca2248c3b89c4ff13ac5034f8a95", 1493745
V478_MD5, V478_BYTES = "98b9f63f1158bd7e0af43f9129a51f06", 1474281

def fail(msg):
    print("VERIFY FAILED: " + msg)
    sys.exit(1)

# --- extract the fold script's literal constants (implicit-concat strings) ---
tree = ast.parse(open(SCRIPT, encoding="utf-8").read())
C = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 \
       and isinstance(node.targets[0], ast.Name):
        try:
            C[node.targets[0].id] = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            pass
need = ["T_OLD", "T_NEW", "A_OLD", "A_SUM", "R_ANCH", "RECORD", "SEC_ANCH",
        "SEC", "ANN_ANCH", "ANNOT", "P4_ANCH", "P4_NEW", "ROW", "CH_NEW"]
missing = [k for k in need if k not in C or not isinstance(C[k], str)]
if missing:
    fail("constants not extracted: %s" % missing)
print("edit constants extracted from %s: %d strings" % (SCRIPT, len(need)))

raw = open(LEDGER, "rb").read()
if hashlib.md5(raw).hexdigest() != V479_MD5:
    fail("V4.79 md5 mismatch")
if len(raw) != V479_BYTES:
    fail("V4.79 byte count mismatch")
print("V4.79 canonical: md5 %s, %d B — matches the authorized candidate" %
      (V479_MD5, V479_BYTES))
s = raw.decode("utf-8")
L = s.split("\n")

# the two anchors the fold script read from V4.78 rather than retyping
row_bkz = [l for l in L if l.startswith("| **Gate G-BKZ32**")]
ch78 = [l for l in L if l.startswith("*V4.78 (August 27, 2026)")]
if len(row_bkz) != 1 or s.count(row_bkz[0]) != 1:
    fail("G-BKZ32 anchor row not unique")
if len(ch78) != 1 or s.count(ch78[0]) != 1:
    fail("V4.78 changelog anchor not unique")
ROW_BKZ, LINE_CH78 = row_bkz[0], ch78[0]

# §2.52 Open 3 row: unique now; must be byte-identical after the reverse-splice
o3 = [l for l in L if l.startswith("| **§2.52 Open 3**")]
if len(o3) != 1 or s.count(o3[0]) != 1:
    fail("§2.52 Open 3 row not unique in V4.79")
O3 = o3[0]

# each edit present exactly once in V4.79
edits = [
    ("E1 title",       C["T_NEW"]),
    ("E2 As-of",       C["A_SUM"]),
    ("E3 fold record", C["RECORD"] + C["R_ANCH"]),
    ("E4 §2.87.J",     "\n" + C["SEC"] + C["SEC_ANCH"][1:]),
    ("E5 annotation",  C["ANNOT"] + C["ANN_ANCH"]),
    ("E6 P-4.b",       C["P4_NEW"]),
    ("E7 Part VI row", "\n" + ROW_BKZ + "\n" + C["ROW"] + "\n"),
    ("E8 changelog",   LINE_CH78 + "\n" + C["CH_NEW"]),
]
for name, needle in edits:
    n = s.count(needle)
    if n != 1:
        fail("%s: expected exactly 1 occurrence, found %d" % (name, n))
    print("  %s present exactly once" % name)

# --- reverse-splice (same order as the fold script's own reverse section) ---
rev = s
rev = rev.replace(LINE_CH78 + "\n" + C["CH_NEW"], LINE_CH78, 1)
rev = rev.replace("\n" + ROW_BKZ + "\n" + C["ROW"] + "\n",
                  "\n" + ROW_BKZ + "\n", 1)
rev = rev.replace(C["P4_NEW"], C["P4_ANCH"], 1)
rev = rev.replace(C["ANNOT"] + C["ANN_ANCH"], C["ANN_ANCH"], 1)
rev = rev.replace("\n" + C["SEC"] + C["SEC_ANCH"][1:], C["SEC_ANCH"], 1)
rev = rev.replace(C["RECORD"] + C["R_ANCH"], C["R_ANCH"], 1)
rev = rev.replace(C["A_SUM"], C["A_OLD"], 1)
rev = rev.replace(C["T_NEW"], C["T_OLD"], 1)
rb = rev.encode("utf-8")
if hashlib.md5(rb).hexdigest() != V478_MD5:
    fail("reverse-splice md5 %s != V4.78 %s" % (hashlib.md5(rb).hexdigest(), V478_MD5))
if len(rb) != V478_BYTES:
    fail("reverse-splice byte count %d != %d" % (len(rb), V478_BYTES))
print("reverse-splice: V4.78 reconstructed BYTE-IDENTICAL (md5 %s, %d B) — PASS"
      % (V478_MD5, V478_BYTES))

o3_rev = [l for l in rev.split("\n") if l.startswith("| **§2.52 Open 3**")]
if o3_rev != [O3] or rev.count(O3) != 1:
    fail("§2.52 Open 3 row not byte-identical pre/post")
print("§2.52 Open 3 row: unique and byte-identical pre/post — PASS")
print("delta: +%d B over V4.78 (all eight edits additive)" % (V479_BYTES - V478_BYTES))
print("RESULT: V4.79 VERIFIED CC-SIDE — authorized candidate, additive-only, reversible")
