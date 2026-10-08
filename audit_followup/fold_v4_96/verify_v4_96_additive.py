#!/usr/bin/env python3
"""Independent additivity check V4.95 -> V4.96 (shares no code with the fold script).

Usage: python3 verify_v4_96_additive.py <path to the V4.96 file (canonical or dry run)>

Every V4.95 line must survive in V4.96 either unchanged or as an in-line append whose added text is one
"[→ V4.96 (§2.96): …]" pointer. The appends must sit on exactly the ten V4.95 lines below, typed from ELECTION_N50.md's
"Ledger" list independently of the fold script's prefixes; each host line must contain the keyword typed here. The only
rewrites allowed are the title and As-of lines (the old As-of text kept verbatim after the version label). Every other
difference must be a pure insertion at the three declared places. §2.92.A and the frozen §2.52 Open 3 row must be
unchanged."""
import difflib, hashlib, re, sys

a = open("/home/claude/fold/SQT_Master_Ledger_v4_95_CANONICAL.md", encoding="utf-8").read()
b = open(sys.argv[1], encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "3b6c11c33fdc88566f8cc1774d2d6a7b"
print("V4.96 file:", sys.argv[1], "md5:", hashlib.md5(b.encode()).hexdigest(), "bytes:", len(b.encode()), "delta:",
      len(b.encode()) - len(a.encode()))
la, lb = a.split("\n"), b.split("\n")
PTR = re.compile(r"^ \[→ V4\.96 \(§2\.96\): [^\n]*\]$")
KEYS = {   # V4.95 line number (1-based) -> keyword on that line
    297: "c is defined as the propagation speed",                          # ANNEX-CDEF-1
    1660: "Gate G-POLY1 REGISTERED",                                        # §2.91.M (the polycrystal postulate)
    1662: "Gate G-CI1 REGISTERED",                                          # §2.91.N (W^EM_∪)
    1692: "What the substrate program still stands on",                     # §2.92.E (the light carrier)
    1730: "The bound (R1-machine two-leg)",                                 # §2.95
    4407: "Polycrystalline-vacuum / domain-averaging (VRH) exploration",    # Part V: the postulate's banked row
    4446: "carrier-identity gate",                                          # Part VI: G-CI1
    4450: "W_∪′ re-derivation mini-gate",                                   # Part VI: G-S2C1-W
    4465: "Polycrystal validity floor",                                     # Part VI: the floor row (the election)
    4466: "Lattice-spacing bound",                                          # Part VI: the V4.95 bound row
}


def appended(old, new):
    if old.endswith(" |") and old.startswith("| "):
        if new.endswith(" |") and new.startswith(old[:-2]) and len(new) > len(old):
            add = new[len(old) - 2:-2]
            return add if PTR.match(add) and add.count("[→ V4.96") == 1 else None
        return None
    if new.startswith(old) and len(new) > len(old):
        add = new[len(old):]
        return add if PTR.match(add) and add.count("[→ V4.96") == 1 else None
    return None


ok = True
n_title = n_asof = 0
appends, inserted = {}, []
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
equal_lines = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        equal_lines += i2 - i1
        continue
    if tag == "delete":
        print("UNEXPECTED delete of V4.95 lines", i1 + 1, "-", i2); ok = False; continue
    if tag == "insert":
        inserted += [(j, lb[j]) for j in range(j1, j2)]; continue
    j = j1
    for i in range(i1, i2):
        old = la[i]
        while j < j2:
            new = lb[j]
            if old.startswith("# SQT Master Ledger — V4.95") and new == old.replace("V4.95", "V4.96"):
                n_title += 1; j += 1; break
            if old.startswith("**As of:** October 7, 2026 (V4.95 fold — "):
                tail = old[len("**As of:** October 7, 2026 (V4.95 fold — "):]
                if new.startswith("**As of:** ") and "(V4.96 fold — " in new and new.endswith(
                        "V4.95 fold (October 7, 2026) — " + tail):
                    n_asof += 1; j += 1; break
            got = appended(old, new)
            if got is not None:
                appends[i + 1] = got; j += 1; break
            if new == old:
                j += 1; break
            inserted.append((j, new)); j += 1
        else:
            print("UNMATCHED V4.95 line", i + 1, repr(old[:80])); ok = False
    inserted += [(k, lb[k]) for k in range(j, j2)]

print(f"title rewrites: {n_title}; As-of rewrites: {n_asof}; in-line pointer appends: {len(appends)}; inserted lines: "
      f"{len(inserted)} ({sum(len(x.encode()) + 1 for _, x in inserted)} B); V4.95 lines carried unchanged: {equal_lines} of "
      f"{len(la)}")
missing, extra = set(KEYS) - set(appends), set(appends) - set(KEYS)
print("appends on the expected 10 lines:", not missing and not extra, "| missing:", sorted(missing), "| extra:", sorted(extra))
bad_key = sorted(n for n in KEYS if KEYS[n] not in la[n - 1])
print("every host line contains its typed keyword:", not bad_key, "| failing:", bad_key)

idx = [j for j, _ in inserted]
blocks, start = [], None
for k, j in enumerate(idx):
    if start is None:
        start = j
    if k + 1 == len(idx) or idx[k + 1] != j + 1:
        blocks.append((start, j)); start = None
print("inserted blocks (V4.96 1-based line ranges):", [(x + 1, y + 1) for x, y in blocks])
place_ok = len(blocks) == 3


def frame(blk):
    nb = [k for k in range(blk[0], blk[1] + 1) if lb[k].strip()]
    before = next(k for k in range(nb[0] - 1, -1, -1) if lb[k].strip())
    after = next((k for k in range(nb[-1] + 1, len(lb)) if lb[k].strip()), None)
    return ([lb[k] for k in nb], lb[before], None if after is None else lb[after], nb[0] - before,
            None if after is None else after - nb[-1])


if place_ok:
    rec, sec, chg = (frame(x) for x in blocks)
    place_ok &= (len(rec[0]) == 1 and rec[0][0].startswith("**V4.96 fold-in record (")
                 and rec[2].startswith("**V4.95 fold-in record (October 7, 2026):**") and rec[4] == 2)
    place_ok &= (len(sec[0]) == 6 and sec[0][0].startswith("### §2.96 — ")
                 and sec[0][4].startswith("**What rests on which data.**")
                 and sec[1].startswith("**The floor, registers and non-claims.** The homogenization literature")
                 and sec[2] == "## J. Multi-Lens Reference and Phase Incommensurability" and sec[3] == 2 and sec[4] == 2)
    place_ok &= (len(chg[0]) == 1 and chg[0][0].startswith("*V4.96 (") and "additions only" in chg[0][0]
                 and chg[1].startswith("*V4.95 (October 7, 2026): additions only") and chg[3] == 1 and chg[2] is None)
print("insertions at the declared places (record / §2.96 / changelog):", place_ok)
heads = [x for _, x in inserted if x.startswith("#")]
print("inserted headings:", heads)
fixed = {"§2.92.A": "**A. Polarization gate (A1) — FALSIFIED", "§2.52 Open 3": "| **§2.52 Open 3**"}
fixed_ok = True
for name, p in fixed.items():
    xa, xb = [x for x in la if x.startswith(p)], [x for x in lb if x.startswith(p)]
    good = len(xa) == 1 and xa == xb
    fixed_ok &= good
    print(name, "unchanged:", good)
n_ptr = b.count("[→ V4.96 (§2.96): ")
n_ins = sum(x.count("[→ V4.96") for _, x in inserted)
print("'[→ V4.96 (§2.96): ' occurrences:", n_ptr, "(expected 10, all in appends); '[→ V4.96' inside inserted text:", n_ins,
      "(expected 3: the §2.96 preamble, the record and the changelog each name the pointer form once)")
ok &= (n_title == 1 and n_asof == 1 and not missing and not extra and not bad_key and place_ok and fixed_ok
       and heads == ["### §2.96 — The Polycrystal Floor Elected: N = 50 (V4.96)"]
       and n_ptr == 10 and sum(x.count("[→ V4.96 (§2.96): ") for _, x in inserted) == 0 and n_ins == 3
       and a.count("V4.96") == 0 and equal_lines + n_title + n_asof + len(appends) == len(la))
print("ADDITIVITY CHECK:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
