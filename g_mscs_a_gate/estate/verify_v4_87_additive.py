#!/usr/bin/env python3
"""verify_v4_87_additive.py — independent of the fold script: proves V4.87 is V4.86 plus insertions only.
Every line of V4.86 must appear in V4.87 either unchanged or as a prefix-preserving extension whose added text lies
entirely inside the new bracket/insertion segments; the header bumps (lines 1 and 3) are the only prefix changes; the
new lines are the V4.87 record, §2.91.T, the Part VI row and the changelog line; the §2.52 Open 3 row byte-identical."""
import difflib, hashlib, sys
A = open("/home/claude/v487/SQT_Master_Ledger_v4_86_CANONICAL.md", encoding="utf-8").read()
B = open("/home/claude/v487/SQT_Master_Ledger_v4_87_CANONICAL.md", encoding="utf-8").read()
assert hashlib.md5(A.encode()).hexdigest() == "d4c42a53cbd6d325ebc740879288e844"
la, lb = A.split("\n"), B.split("\n")
import re
BR = re.compile(r"^ \*\*\[.*\]\*\*$", re.S)
A_OLD = "**As of:** September 27, 2026 (V4.86 fold — "
changed, added, ok = [], [], True
# map each old line to the new line by exact match or by additive extension (character-level diff: inserts only)
jb = 0
for i, a in enumerate(la):
    # find a in lb at or after jb
    k = None
    for j in range(jb, min(jb + 6, len(lb))):
        if lb[j] == a: k = j; break
    if k is not None:
        added += lb[jb:k]; jb = k + 1; continue
    # extension candidates
    b = lb[jb]
    if a.startswith("# SQT Master Ledger — V4.86"):
        assert b == "# SQT Master Ledger — V4.87 Canonical"; changed.append(("header bump: title",)); jb += 1; continue
    if a.startswith(A_OLD):
        marker = " Full V4.87 record below. V4.86 fold (September 27, 2026) — "
        assert b.startswith("**As of:** September 30, 2026 (V4.87 fold — ") and b.count(marker) == 1
        changed.append(("header bump: As-of prepend", b.index(marker) + len(marker) - len(A_OLD)))
        a, b = a[len(A_OLD):], b[b.index(marker) + len(marker):]      # the rest of the As-of line is then tested like any other line
    # character-level two-pointer walk: b must equal a with zero or more " **[...]**" segments inserted (the segment's
    # leading space may have been consumed as the original space that preceded the insertion point)
    ins, ci, cj, n, m = [], 0, 0, len(a), len(b)
    while ci < n and ok:
        if cj < m and a[ci] == b[cj]:
            ci += 1; cj += 1; continue
        if b.startswith(" **[", cj):
            lead, skip = "", 0
        elif b.startswith("**[", cj) and cj > 0 and b[cj - 1] == " ":
            lead, skip = " ", 1          # the bracket followed a space that the walk already matched; the bracket's own trailing space is skipped
        else:
            ok = False; changed.append(("NON-ADDITIVE", i + 1, ci, a[ci:ci + 40], b[cj:cj + 40])); break
        k = b.find("]**", cj)
        while k >= 0 and b[k + 3 + skip:k + 3 + skip + min(20, n - ci)] != a[ci:ci + min(20, n - ci)]:
            k = b.find("]**", k + 1)
        if k < 0:
            ok = False; changed.append(("UNTERMINATED BRACKET", i + 1, b[cj:cj + 40])); break
        ins.append(lead + b[cj:k + 3]); cj = k + 3 + skip
    if ok and ci == n and cj < m:
        tail = b[cj:]
        if BR.match(tail): ins.append(tail)
        else: ok = False; changed.append(("TRAILING NON-BRACKET", i + 1, tail[:40]))
    bad = [x for x in ins if not BR.match(x)]
    if bad: ok = False; changed.append(("NON-BRACKET INSERT", i, [x[:50] for x in bad]))
    else: changed.append(("bracketed line %d" % (i + 1), len(ins), sum(len(x) for x in ins)))
    jb += 1
added += lb[jb:]
o3a = [l for l in la if l.startswith("| **§2.52 Open 3**")]; o3b = [l for l in lb if l.startswith("| **§2.52 Open 3**")]
assert o3a == o3b and len(o3a) == 1
print("changed lines:", len(changed)); [print("  ", c) for c in changed]
print("added lines:", len(added)); [print("  +", l[:90]) for l in added]
rows = [l for l in lb if l.startswith("| **Gate G-MSCS")]
print("Part VI gate rows cell counts:", [(r[:22], r.count("|")) for r in rows])
# the six new lines: the V4.87 fold-in record, a blank, §2.91.T, a blank, the Part VI row, the changelog line
nonblank = [l for l in added if l.strip()]
shape = (len(added) == 6 and len(nonblank) == 4
         and nonblank[0].startswith("**V4.87 fold-in record (September 30, 2026):**")
         and nonblank[1].startswith("**T. Gate G-MSCS-A REGISTERED + LOCKED + EXECUTED")
         and nonblank[2].startswith("| **Gate G-MSCS-A")
         and "V4.87" in nonblank[3])
print("added-line shape:", "OK" if shape else "UNEXPECTED")
final = ok and shape
print("ADDITIVE DIFF VERIFIED" if final else "ADDITIVE DIFF FAILED")
sys.exit(0 if final else 1)
