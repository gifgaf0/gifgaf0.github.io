#!/usr/bin/env python3
"""Independent additivity check V4.101 -> V4.102 (shares no code with the fold script).

Usage: python3 verify_v4_102_additive.py <path to the V4.101 file> <path to the V4.102 file>

Every V4.101 line must survive in V4.102 either unchanged or with one appended "[→ V4.102 (§2.102): …]" pointer, and the
appends must sit on exactly the two V4.101 lines typed below (§1.3's closing paragraph; §2.69's retirement paragraph).
The only rewrites allowed are the title and the As-of line (the old As-of text kept verbatim after the new prefix).
Every other difference must be a pure insertion at the three declared places: before the V4.101 fold-in record, between
§2.101's registers line and the Cluster J heading, and after the V4.101 changelog line. §2.101 must be unchanged.
"""
import difflib, hashlib, re, sys

a = open(sys.argv[1], encoding="utf-8").read()
b = open(sys.argv[2], encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "4a67c76037b63adc6037aec0d7f2ac4d", "not V4.101"
print("V4.102 file:", sys.argv[2], "md5:", hashlib.md5(b.encode()).hexdigest(), "bytes:", len(b.encode()),
      "delta: +%d" % (len(b.encode()) - len(a.encode())))
la, lb = a.split("\n"), b.split("\n")
HOSTS = {  # typed host prefix in V4.101 -> fact its pointer must state
    "These are mathematical facts about finite Coxeter groups.": "τ(n)",
    "**Retirement of the octonionic-structure hypothesis at 256-bit residue distribution scale.**": "congruence class",
}
host_idx = {}
for pre in HOSTS:
    idx = [i for i, x in enumerate(la) if x.startswith(pre)]
    assert len(idx) == 1, (pre, idx)
    host_idx[idx[0]] = pre
PTR = re.compile(r" \[→ V4\.102 \(§2\.102\): [^\n|\[\]]*\]")

ok = True
appends, rewrites, inserted = {}, [], []
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes():
    if tag == "equal":
        continue
    if tag == "delete":
        print("UNEXPECTED delete at V4.101 line", i1 + 1); ok = False; continue
    if tag == "insert":
        inserted.append((i1, j1, j2)); continue
    # replace: pair lines one-to-one where possible, extra new lines are insertions
    if (i2 - i1) > (j2 - j1):
        print("UNEXPECTED replace shrinking lines at", i1 + 1); ok = False; continue
    for k in range(i2 - i1):
        old, new = la[i1 + k], lb[j1 + k]
        if old == "# SQT Master Ledger — V4.101 Canonical" and new == "# SQT Master Ledger — V4.102 Canonical":
            rewrites.append("title"); continue
        OLD_PRE, KEEP = "**As of:** October 13, 2026 (V4.101 fold — ", "V4.101 fold (October 13, 2026) — "
        if old.startswith(OLD_PRE) and new.startswith("**As of:** October 22, 2026 (V4.102 fold — "):
            # the new line must be: <new prefix> + "V4.101 fold (October 13, 2026) — " + <old text after its prefix>
            if new.count(KEEP) == 1 and new.split(KEEP, 1)[1] == old[len(OLD_PRE):]:
                rewrites.append("as-of"); continue
            print("As-of rewrite does not keep the old text"); ok = False; continue
        if i1 + k in host_idx and new.startswith(old) and PTR.fullmatch(new[len(old):]):
            pre = host_idx[i1 + k]
            if HOSTS[pre] not in new[len(old):]:
                print("pointer misses its fact on", pre[:50]); ok = False
            appends[pre] = new[len(old):]; continue
        print("UNEXPECTED change at V4.101 line", i1 + k + 1, ":", old[:80]); ok = False
    if (j2 - j1) > (i2 - i1):
        inserted.append((i2, j1 + (i2 - i1), j2))

print("rewrites:", rewrites)
print("pointer appends:", len(appends), "on", [p[:40] for p in appends])
ok &= sorted(rewrites) == ["as-of", "title"] and len(appends) == 2

# insertions: classify by the V4.101 line they precede
rec101 = [i for i, x in enumerate(la) if x.startswith("**V4.101 fold-in record (October 13, 2026):**")][0]
j_head = [i for i, x in enumerate(la) if x == "## J. Multi-Lens Reference and Phase Incommensurability"][0]
ch101 = [i for i, x in enumerate(la) if x.startswith("*V4.101 (October 13, 2026): additions only")][0]
places = {}
for i, j1, j2 in inserted:
    block = lb[j1:j2]
    nonblank = [x for x in block if x != ""]
    # the record and its blank separator may align as [record, ""] before the V4.101 record or ["", record] before
    # the blank line above it; either way exactly one non-blank line, the V4.102 record, and one blank
    if (i in (rec101, rec101 - 1) and len(block) == 2 and len(nonblank) == 1
            and nonblank[0].startswith("**V4.102 fold-in record (October 22, 2026):**")):
        places["record"] = block
    elif i in (j_head, j_head - 1) and any(x.startswith("### §2.102 — ") for x in block):
        places["§2.102"] = block
    elif i == ch101 + 1 and block[0].startswith("*V4.102 (October 22, 2026): additions only"):
        places["changelog"] = block
    else:
        print("UNEXPECTED insertion before V4.101 line", i + 1, ":", block[0][:80]); ok = False
print("insertions at:", sorted(places))
ok &= sorted(places) == ["changelog", "record", "§2.102"]

# §2.101 untouched
s101 = [i for i, x in enumerate(la) if x.startswith("### §2.101 — ")][0]
seg_a = "\n".join(la[s101:j_head])
ok &= seg_a in b
print("§2.101 block unchanged:", seg_a in b)
# §2.102 sits after §2.101 and before Cluster J in V4.102
p101, p102, pJ = b.index("### §2.101 — "), b.index("### §2.102 — "), b.index("## J. Multi-Lens Reference")
ok &= p101 < p102 < pJ
print("order §2.101 < §2.102 < J:", p101 < p102 < pJ)
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
