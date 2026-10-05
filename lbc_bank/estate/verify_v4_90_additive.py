#!/usr/bin/env python3
"""Independent additivity check V4.89 -> V4.90 (no fold-script code reused).
Every difference must be a pure insertion, except the declared title and As-of rewrites; the As-of rewrite must keep the
whole old line after its version label; the §2.91.V line must be an in-line append; the §2.52 Open 3 row must be untouched."""
import difflib, hashlib
a = open("SQT_Master_Ledger_v4_89_CANONICAL.md", encoding="utf-8").read()
b = open("SQT_Master_Ledger_v4_90_CANONICAL.md", encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "db01bd273629ce7a385ff3c7fb6efdfc"
print("V4.90 md5:", hashlib.md5(b.encode()).hexdigest(), "bytes:", len(b.encode()), "delta:", len(b.encode()) - len(a.encode()))
la, lb = a.split("\n"), b.split("\n")
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
equal_lines = sum(i2 - i1 for t, i1, i2, j1, j2 in sm.get_opcodes() if t == "equal")
ok = True
for tag, i1, i2, j1, j2 in ops:
    if tag == "insert":
        print(f"insert  after V4.89 line {i1}: +{j2-j1} line(s), {sum(len(x.encode())+1 for x in lb[j1:j2])} B")
    elif tag == "replace" and i2 - i1 == 1 and j2 - j1 == 1:
        old, new = la[i1], lb[j1]
        if new.startswith(old):
            print(f"append  V4.89 line {i1+1}: in-line insertion of {len(new)-len(old)} chars, 0 removed")
        elif old.startswith("# SQT Master Ledger — V4.89") and new == old.replace("V4.89", "V4.90"):
            print(f"title   V4.89 line {i1+1}: declared label rewrite V4.89 -> V4.90")
        elif old.startswith("**As of:** October 4, 2026 (V4.89 fold — "):
            head_new = "**As of:** October 4, 2026 (V4.90 fold — "
            tail_old = old[len("**As of:** October 4, 2026 (V4.89 fold — "):]
            good = new.startswith(head_new) and new.endswith("V4.89 fold (October 4, 2026) — " + tail_old)
            print(f"as-of   V4.89 line {i1+1}: declared rewrite; old text after the label kept verbatim at the end: {good}")
            ok &= good
        else:
            print(f"UNEXPECTED replace at V4.89 line {i1+1}"); ok = False
    else:
        print("UNEXPECTED op", tag, i1, i2, j1, j2); ok = False
print("total ops:", len(ops), "| V4.89 lines carried unchanged:", equal_lines, "of", len(la))
o3a = [x for x in la if x.startswith("| **§2.52 Open 3**")]
o3b = [x for x in lb if x.startswith("| **§2.52 Open 3**")]
print("§2.52 Open 3 row identical and unique:", o3a == o3b and len(o3a) == 1)
ok &= (o3a == o3b and len(o3a) == 1) and len(ops) == 5 and equal_lines == len(la) - 3
print("ADDITIVITY CHECK:", "PASS" if ok else "FAIL")
