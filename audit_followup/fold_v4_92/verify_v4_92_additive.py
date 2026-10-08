#!/usr/bin/env python3
"""Independent additivity check V4.91 -> V4.92 (shares no code with the fold script).

Every V4.91 line must survive in V4.92 either unchanged or as an in-line append whose added text is a "[→ V4.92 …]" bracket
(at the end of a paragraph line, or just before the closing " |" of a table row). The only rewrites allowed are the declared
title and As-of lines; the As-of rewrite must keep the whole old text after its version label. Every other difference
must be a pure insertion. The §2.52 Open 3 row must be untouched."""
import difflib, hashlib, re, sys

a = open("/home/claude/fold/SQT_Master_Ledger_v4_91_CANONICAL.md", encoding="utf-8").read()
b = open("/home/claude/fold/SQT_Master_Ledger_v4_92_CANONICAL.md", encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "ce9ca6873adb5686227f5d103b41e3cc"
print("V4.92 md5:", hashlib.md5(b.encode()).hexdigest(), "bytes:", len(b.encode()), "delta:", len(b.encode()) - len(a.encode()))
la, lb = a.split("\n"), b.split("\n")
BR = re.compile(r"^ \[→ V4\.92 [^\n]*\]$")

def appended(old, new):
    """Return the added text if `new` is `old` with one bracket appended (paragraph) or inserted before ' |' (row)."""
    if old.endswith(" |") and old.startswith("| "):
        if new.endswith(" |") and new.startswith(old[:-2]) and len(new) > len(old):
            add = new[len(old) - 2:-2]
            return add if BR.match(add) else None
        return None
    if new.startswith(old) and len(new) > len(old):
        add = new[len(old):]
        return add if BR.match(add) else None
    return None

ok = True
n_title = n_asof = n_append = 0
inserted = []
appends = []
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
equal_lines = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        equal_lines += i2 - i1
        continue
    if tag == "delete":
        print("UNEXPECTED delete of V4.91 lines", i1 + 1, "-", i2); ok = False; continue
    if tag == "insert":
        inserted += lb[j1:j2]; continue
    # replace: align each old line to a later new line in order; the rest are insertions
    j = j1
    for i in range(i1, i2):
        old = la[i]
        while j < j2:
            new = lb[j]
            if old.startswith("# SQT Master Ledger — V4.91") and new == old.replace("V4.91", "V4.92"):
                n_title += 1; j += 1; break
            if old.startswith("**As of:** October 4, 2026 (V4.91 fold — "):
                tail = old[len("**As of:** October 4, 2026 (V4.91 fold — "):]
                if new.startswith("**As of:** October 7, 2026 (V4.92 fold — ") and new.endswith(
                        "V4.91 fold (October 4, 2026) — " + tail):
                    n_asof += 1; j += 1; break
            add = appended(old, new)
            if add is not None:
                n_append += 1; appends.append((old[:70], add)); j += 1; break
            if new == old:
                j += 1; break
            inserted.append(new); j += 1
        else:
            print("UNMATCHED V4.91 line", i + 1, repr(old[:80])); ok = False
    inserted += lb[j:j2]

print(f"title rewrites: {n_title}; As-of rewrites: {n_asof}; in-line bracket appends: {n_append}; "
      f"inserted lines: {len(inserted)} ({sum(len(x.encode()) + 1 for x in inserted)} B); V4.91 lines carried unchanged: "
      f"{equal_lines} of {len(la)}")
o3a = [x for x in la if x.startswith("| **§2.52 Open 3**")]
o3b = [x for x in lb if x.startswith("| **§2.52 Open 3**")]
print("§2.52 Open 3 row identical and unique:", o3a == o3b and len(o3a) == 1)
heads = [x for x in inserted if x.startswith("#")]
print("inserted headings:", heads)
print("inserted Part VI rows:", [x[:40] for x in inserted if x.startswith("| **")])
print("inserted record/changelog:", [x[:40] for x in inserted if x.startswith("**V4.92 fold-in") or x.startswith("*V4.92 (")])
ok &= (n_title == 1 and n_asof == 1 and n_append == 44 and o3a == o3b and len(o3a) == 1
       and equal_lines + n_title + n_asof + n_append == len(la))
# every V4.91 line is accounted for, and nothing outside the declared kinds changed
print("ADDITIVITY CHECK:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
