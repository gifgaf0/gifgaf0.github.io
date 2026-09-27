#!/usr/bin/env python3
"""verify_v4_85_additive.py — INDEPENDENT additive-diff verification of the V4.85 fold (does not use the fold script's
constants): walks every V4.84 line in order and requires it to reappear in V4.85 either verbatim or as a pure-insertion
parent (char-level SequenceMatcher: only 'equal'/'insert' opcodes), with the declared header bumps at lines 1 (title) and
3 (As-of prepend; the V4.84 tail preserved verbatim) as the only substitutions. Writes V4_85_DELTA_ONLY.txt (every
inserted segment, tagged by position) for the T1 scan. Exit 0 = PASS."""
import hashlib, difflib, sys
A = "/home/claude/v485/SQT_Master_Ledger_v4_84_CANONICAL.md"; B = "/home/claude/v485/SQT_Master_Ledger_v4_85_CANONICAL.md"
a = open(A, encoding="utf-8").read(); b = open(B, encoding="utf-8").read()
print("V4.84", hashlib.md5(a.encode()).hexdigest(), len(a.encode()), "B"); print("V4.85", hashlib.md5(b.encode()).hexdigest(), len(b.encode()), "B")
a = a.split("\n"); b = b.split("\n")
def additive_segments(old, new):
    if not old or len(new) < len(old) or old == new: return None
    i = 0
    while i < len(old) and old[i] == new[i]: i += 1
    k2 = 0
    while k2 < len(old) - i and old[-1 - k2] == new[-1 - k2]: k2 += 1
    if new[:i] + new[len(new) - k2:] == old: return [(i, new[i:len(new) - k2])]
    segs = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag == "equal": continue
        if tag != "insert": return None
        segs.append((i1, new[j1:j2]))
    return segs
out = []; j = 0
for i, old in enumerate(a):
    ln = i + 1
    if ln == 1:
        new = b[j]; j += 1
        assert old == "# SQT Master Ledger — V4.84 Canonical" and new == "# SQT Master Ledger — V4.85 Canonical"
        out.append(("HEADER BUMP V4.84 line 1", new)); continue
    if ln == 3:
        new = b[j]; j += 1; head = "**As of:** September 21, 2026 (V4.84 fold — "; assert old.startswith(head)
        tail = old[len(head):]; assert new.endswith(tail) and new.startswith("**As of:** September 27, 2026 (V4.85 fold — ")
        out.append(("HEADER BUMP V4.84 line 3: As-of prepend; the V4.84 tail preserved verbatim", new[:len(new) - len(tail)])); continue
    while True:
        assert j < len(b), f"V4.84 line {ln} not recovered"
        new = b[j]; j += 1
        if new == old: break
        segs = additive_segments(old, new)
        if segs is not None:
            for col, seg in segs: out.append((f"MODIFY V4.84 line {ln}: additive insertion at col {col}", seg))
            break
        out.append((f"INSERT before V4.84 line {ln}", new))
assert j == len(b), f"trailing new lines unaccounted: {len(b) - j}"
o3a = [l for l in a if l.startswith("| **§2.52 Open 3**")]; o3b = [l for l in b if l.startswith("| **§2.52 Open 3**")]
assert len(o3a) == 1 and o3a == o3b, "§2.52 Open 3 row changed"
txt = "".join(f"[{k}] {v}\n" for k, v in out)
open("/home/claude/v485/V4_85_DELTA_ONLY.txt", "w", encoding="utf-8").write(txt)
print("ADDITIVE DIFF VERIFIED — every V4.84 line recovered in order; modified lines are pure insertions; header bumps at lines 1 and 3 only; §2.52 Open 3 row byte-identical")
print("delta entries:", len(out), " lines added:", len(b) - len(a), " delta file md5:", hashlib.md5(txt.encode()).hexdigest(), len(txt.encode()), "B")
for k, v in out: print("  ", k)
