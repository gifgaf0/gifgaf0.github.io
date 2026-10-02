#!/usr/bin/env python3
"""verify_v4_88_additive.py — independent of the fold script: proves V4.88 is V4.87 plus insertions only.
Every line of V4.86 must appear in V4.87 either unchanged or as a prefix-preserving extension whose added text lies
entirely inside the new bracket/insertion segments; the header bumps (lines 1 and 3) are the only prefix changes; the
new lines are the V4.88 record, §2.91.U, the Part VI row and the changelog line; the §2.52 Open 3 row byte-identical."""
import difflib, hashlib, sys
A = open("/home/claude/v488/SQT_Master_Ledger_v4_87_CANONICAL.md", encoding="utf-8").read()
B = open("/home/claude/v488/SQT_Master_Ledger_v4_88_CANONICAL.md", encoding="utf-8").read()
assert hashlib.md5(A.encode()).hexdigest() == "dc243cb4fd98f8c79e2a139f138eb6b0"
la, lb = A.split("\n"), B.split("\n")
import re
BR = re.compile(r"^ \*\*\[.*\]\*\*$", re.S)
A_OLD = "**As of:** September 30, 2026 (V4.87 fold — "
changed, added, ok = [], [], True
# map each old line to the new line by exact match or by additive extension (character-level diff: inserts only)
def extension(a, b):
    """is b equal to a with zero or more ' **[...]**' segments inserted? returns (ok, inserted_segments)"""
    ins, ci, cj, n, m = [], 0, 0, len(a), len(b)
    while ci < n:
        if cj < m and a[ci] == b[cj]:
            ci += 1; cj += 1; continue
        if b.startswith(" **[", cj): lead, skip = "", 0
        elif b.startswith("**[", cj) and cj > 0 and b[cj - 1] == " ": lead, skip = " ", 1
        else: return False, [("NON-ADDITIVE", ci, a[ci:ci + 40], b[cj:cj + 40])]
        k = b.find("]**", cj)
        while k >= 0 and b[k + 3 + skip:k + 3 + skip + min(20, n - ci)] != a[ci:ci + min(20, n - ci)]: k = b.find("]**", k + 1)
        if k < 0: return False, [("UNTERMINATED BRACKET", b[cj:cj + 40])]
        ins.append(lead + b[cj:k + 3]); cj = k + 3 + skip
    if cj < m:
        tail = b[cj:]
        if BR.match(tail): ins.append(tail)
        else: return False, [("TRAILING NON-BRACKET", tail[:40])]
    if any(not BR.match(x) for x in ins): return False, [("NON-BRACKET INSERT", [x[:50] for x in ins])]
    return True, ins
jb = 0
for i, a in enumerate(la):
    # exact match within the next 6 new lines (lines skipped are additions)
    k = None
    for j in range(jb, min(jb + 6, len(lb))):
        if lb[j] == a: k = j; break
    if k is not None:
        added += lb[jb:k]; jb = k + 1; continue
    # header bumps (lines 1 and 3)
    if a.startswith("# SQT Master Ledger — V4.87"):
        assert lb[jb] == "# SQT Master Ledger — V4.88 Canonical"; changed.append(("header bump: title",)); jb += 1; continue
    if a.startswith(A_OLD):
        b = lb[jb]; marker = " Full V4.88 record below. V4.87 fold (September 30, 2026) — "
        assert b.startswith("**As of:** October 2, 2026 (V4.88 fold — ") and b.count(marker) == 1
        changed.append(("header bump: As-of prepend", b.index(marker) + len(marker) - len(A_OLD)))
        good, ins = extension(a[len(A_OLD):], b[b.index(marker) + len(marker):])
        if not good: ok = False; changed.append(("As-of line", i + 1) + tuple(ins[0]))
        else: changed.append(("bracketed line %d" % (i + 1), len(ins), sum(len(x) for x in ins)))
        jb += 1; continue
    # a bracket-extended old line, possibly preceded by inserted lines: the first additive extension within the next 6 new lines
    found = None
    for j in range(jb, min(jb + 6, len(lb))):
        good, ins = extension(a, lb[j])
        if good: found = (j, ins); break
    if found is None:
        ok = False; changed.append(("NON-ADDITIVE", i + 1, a[:40], lb[jb][:40])); break
    j, ins = found; added += lb[jb:j]; jb = j + 1
    changed.append(("bracketed line %d" % (i + 1), len(ins), sum(len(x) for x in ins)))
added += lb[jb:]
o3a = [l for l in la if l.startswith("| **§2.52 Open 3**")]; o3b = [l for l in lb if l.startswith("| **§2.52 Open 3**")]
assert o3a == o3b and len(o3a) == 1
print("changed lines:", len(changed)); [print("  ", c) for c in changed]
print("added lines:", len(added)); [print("  +", l[:90]) for l in added]
rows = [l for l in lb if l.startswith("| **Gate G-MSCS")]
print("Part VI gate rows cell counts:", [(r[:22], r.count("|")) for r in rows])
# the six new lines: the V4.88 fold-in record, a blank, §2.91.U, a blank, the Part VI row, the changelog line
nonblank = [l for l in added if l.strip()]
shape = (len(added) == 6 and len(nonblank) == 4
         and nonblank[0].startswith("**V4.88 fold-in record (October 2, 2026):**")
         and nonblank[1].startswith("**U. Gate G-VS1 REGISTERED + LOCKED + EXECUTED")
         and nonblank[2].startswith("| **Gate G-VS1")
         and nonblank[3].startswith("*V4.88 (October 2, 2026): additions only"))
print("added-line shape:", "OK" if shape else "UNEXPECTED")
final = ok and shape
print("ADDITIVE DIFF VERIFIED" if final else "ADDITIVE DIFF FAILED")
sys.exit(0 if final else 1)
