#!/usr/bin/env python3
"""Independent additivity check V4.100 -> V4.101 (shares no code with the fold script).

Usage: python3 verify_v4_101_additive.py <path to the V4.101 file (canonical or dry run)>

Every V4.100 line must survive in V4.101 either unchanged or with one appended "[→ V4.101 (§2.101): …]" pointer (at the
end of a paragraph line, or just before the closing " |" of a table row). The appends must sit on exactly the four
V4.100 lines typed below: §2.100's items 3, 5 and 6, and the Phase C row. Each pointer must state the fact typed here.
The only rewrites allowed are the title and the As-of line (the old As-of text kept verbatim after the new prefix). Every
other difference must be a pure insertion at the three declared places. §2.100's heading, its italic header and its
registers line, §2.99's heading and the V4.100 record must be unchanged.
"""
import difflib, hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
a = open(os.path.join(HERE, "..", "..", "SQT_Master_Ledger_v4_100_CANONICAL.md"), encoding="utf-8").read()
b = open(sys.argv[1], encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "35a20a1f2db1ad66663b4cd60b7c8234"
print("V4.101 file:", sys.argv[1], "md5:", hashlib.md5(b.encode()).hexdigest(), "bytes:", len(b.encode()),
      "delta:", len(b.encode()) - len(a.encode()))
la, lb = a.split("\n"), b.split("\n")
TAG = "[→ V4.101 (§2.101): "
HOSTS = {  # typed host prefix in V4.100 -> fact its pointer must state
    "3. **The note.** The author deposited": "10.5281/zenodo.23352161",
    "5. **The gauge paper, v6.4.** The author deposited": "v6.4 abstract",
    "6. **Fluid Lattice Topology, with its notice.** This is": "10.5281/zenodo.23352161",
    "| **Phase C draft awaiting the author**": "10.5281/zenodo.23352161",
}
host_idx = {}
for pre in HOSTS:
    idx = [i for i, x in enumerate(la) if x.startswith(pre)]
    assert len(idx) == 1, (pre, idx)
    host_idx[idx[0]] = pre


def pointer_of(old, new):
    if not old.endswith(" |"):
        add = new[len(old):] if new.startswith(old) else None
    else:
        add = new[len(old) - 2:-2] if (new.startswith(old[:-2]) and new.endswith(" |")) else None
    if add and re.fullmatch(r" \[→ V4\.101 \(§2\.101\): [^\n|\[\]]*\]", add):
        return add
    return None


ok, t_ok, a_ok = True, 0, 0
appends, inserted, unchanged = {}, [], 0
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes():
    if tag == "equal":
        unchanged += i2 - i1
        continue
    if tag == "delete":
        print("UNEXPECTED delete at", i1 + 1); ok = False; continue
    if tag == "insert":
        inserted.extend(range(j1, j2)); continue
    j = j1
    for i in range(i1, i2):
        while j < j2:
            old, new = la[i], lb[j]
            if old == "# SQT Master Ledger — V4.100 Canonical" and new == "# SQT Master Ledger — V4.101 Canonical":
                t_ok += 1; j += 1; break
            if old.startswith("**As of:** October 13, 2026 (V4.100 fold — "):
                tail = old[len("**As of:** October 13, 2026 ("):]
                if new.startswith("**As of:** ") and "(V4.101 fold — " in new and new.endswith(
                        "V4.100 fold (October 13, 2026) — " + tail[len("V4.100 fold — "):]):
                    a_ok += 1; j += 1; break
            p = pointer_of(old, new)
            if p is not None:
                appends[i] = p; j += 1; break
            if old == new:
                unchanged += 1; j += 1; break
            inserted.append(j); j += 1
        else:
            print("UNMATCHED V4.100 line", i + 1, repr(la[i][:70])); ok = False
    inserted.extend(range(j, j2))

print(f"title: {t_ok}; As-of: {a_ok}; appends: {len(appends)}; inserted lines: {len(inserted)}; "
      f"unchanged: {unchanged} of {len(la)}")
hosts_ok = set(appends) == set(host_idx) and all(HOSTS[host_idx[i]] in appends[i] for i in appends)
print("appends exactly on the four typed hosts, each stating its fact:", hosts_ok)
blocks, start = [], None
for k, j in enumerate(sorted(inserted)):
    if start is None:
        start = prev = j
    elif j != prev + 1:
        blocks.append((start, prev)); start = j
    prev = j
if start is not None:
    blocks.append((start, prev))
print("inserted blocks (1-based):", [(x + 1, y + 1) for x, y in blocks])
text = [lb[j] for j in sorted(inserted)]
heads = [x for x in text if x.startswith("#")]


def frame(blk):
    """(non-blank inserted lines, the non-blank line before the block, the non-blank line after it)"""
    body = [lb[k] for k in range(blk[0], blk[1] + 1) if lb[k].strip()]
    before = next(lb[k] for k in range(blk[0] - 1, -1, -1) if lb[k].strip())
    after = next((lb[k] for k in range(blk[1] + 1, len(lb)) if lb[k].strip()), None)
    return body, before, after


place = len(blocks) == 3
if place:
    rec, sec, chg = (frame(x) for x in blocks)
    place &= (len(rec[0]) == 1 and rec[0][0].startswith("**V4.101 fold-in record (")
              and rec[2].startswith("**V4.100 fold-in record (October 13, 2026):**"))
    place &= (sec[0][0] == "### §2.101 — The SLWE Note's Revision Deposited, and the Gauge Record's Description (V4.101)"
              and heads == [sec[0][0]]
              and sec[1].startswith("**Registers and non-claims.** One R1 fact, one leg; estate facts as recorded, the deposit")
              and sec[2] == "## J. Multi-Lens Reference and Phase Incommensurability")
    place &= (len(chg[0]) == 1 and chg[0][0].startswith("*V4.101 (") and "additions only" in chg[0][0]
              and chg[1].startswith("*V4.100 (October 13, 2026): additions only") and chg[2] is None)
print("insertions at the declared places (record / §2.101 after §2.100 / changelog):", place)
facts = ("10.5281/zenodo.23352161", "10.5281/zenodo.23270248", "ZENODO_V2_DESCRIPTION_UNWRAPPED.txt", "21:39 UTC")
facts_ok = all(f in "\n".join(text) for f in facts)
print("typed facts present in §2.101 / record:", facts_ok)
fixed = ["### §2.100 — The SLWE Decryption Threshold, and Three Zenodo Deposits (V4.100)",
         "### §2.99 — The Author's Close-Out Decisions (V4.99)", "**V4.100 fold-in record (October 13, 2026):**",
         "*(Folded V4.100, October 13, 2026,", "**Registers and non-claims.** One R1 fact, one leg; estate facts as recorded, the deposit"]
fixed_ok = all(len([x for x in la if x.startswith(f)]) == 1 and [x for x in la if x.startswith(f)] ==
               [x for x in lb if x.startswith(f)] for f in fixed)
print("§2.100 heading/header/registers, §2.99 heading and the V4.100 record unchanged:", fixed_ok)
n_tag = b.count(TAG)
print("'[→ V4.101 (§2.101): ' occurrences:", n_tag, "(expected 4, all in appends)")
ok &= (t_ok == 1 and a_ok == 1 and hosts_ok and place and facts_ok and fixed_ok and n_tag == 4
       and a.count("V4.101") == 0 and unchanged + t_ok + a_ok + len(appends) == len(la))
print("ADDITIVITY CHECK:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
