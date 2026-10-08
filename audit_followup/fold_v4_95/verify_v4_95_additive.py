#!/usr/bin/env python3
"""Independent additivity check V4.94 -> V4.95 (shares no code with the fold script).

Every V4.94 line must survive in V4.95 either unchanged or as an in-line append whose added text is one
"[→ V4.95 (§2.95): …]" pointer (at the end of a paragraph line, or just before the closing " |" of a table row). The
appends must sit on exactly the nine V4.94 lines below, typed from LS_PREREG.md §10 and LS_RESULT.md ("What it touches")
independently of the fold script's prefixes; each host line must contain the keyword typed here from a reading of that
line (a guard against a mis-aimed anchor). The only rewrites allowed are the declared title and As-of lines; the As-of
rewrite must keep the whole old text after its version label. Every other difference must be a pure insertion, at the
four declared places. The A1 verdict paragraph (§2.92.A) must be untouched."""
import difflib, hashlib, re, sys

a = open("/home/claude/fold/SQT_Master_Ledger_v4_94_CANONICAL.md", encoding="utf-8").read()
b = open("/home/claude/fold/SQT_Master_Ledger_v4_95_CANONICAL.md", encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "708df4cf8f4703088c89b4fad96584bd"
print("V4.95 md5:", hashlib.md5(b.encode()).hexdigest(), "bytes:", len(b.encode()), "delta:", len(b.encode()) - len(a.encode()))
la, lb = a.split("\n"), b.split("\n")
PTR = re.compile(r"^ \[→ V4\.95 \(§2\.95\): [^\n]*\]$")

KEYS = {   # V4.94 line number (1-based) -> keyword on that line
    295: "c is defined as the propagation speed",          # ANNEX-CDEF-1 (the ANNEX-SC-1 substitution clause)
    1634: "Gate G-SCALE1 EXECUTED",                         # §2.91.H (ANNEX-SC-1)
    1660: "Gate G-CI1 REGISTERED",                          # §2.91.N (W^EM_∪)
    1670: "Gate G-MSCS2 REGISTERED",                        # §2.91.S (b₁ banked)
    1672: "Gate G-MSCS-A REGISTERED",                       # §2.91.T (E-SA-1(b) successor)
    1690: "What the substrate program still stands on",     # §2.92.E (the light-only transverse carrier)
    4432: "carrier-identity gate",                          # Part VI: G-CI1 row
    4436: "W_∪′ re-derivation mini-gate",                   # Part VI: G-S2C1-W row
    4451: "Polycrystal validity floor",                     # Part VI: the floor row
}
assert len(KEYS) == 9


def appended(old, new):
    """Return the added text if `new` is `old` with one pointer appended (paragraph) or inserted before ' |' (row)."""
    if old.endswith(" |") and old.startswith("| "):
        if new.endswith(" |") and new.startswith(old[:-2]) and len(new) > len(old):
            add = new[len(old) - 2:-2]
            return add if PTR.match(add) and add.count("[→ V4.95") == 1 else None
        return None
    if new.startswith(old) and len(new) > len(old):
        add = new[len(old):]
        return add if PTR.match(add) and add.count("[→ V4.95") == 1 else None
    return None


ok = True
n_title = n_asof = 0
appends = {}                       # V4.94 line number (1-based) -> added text
inserted = []                      # (V4.95 index, text)
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
equal_lines = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        equal_lines += i2 - i1
        continue
    if tag == "delete":
        print("UNEXPECTED delete of V4.94 lines", i1 + 1, "-", i2); ok = False; continue
    if tag == "insert":
        inserted += [(j, lb[j]) for j in range(j1, j2)]; continue
    j = j1
    for i in range(i1, i2):
        old = la[i]
        while j < j2:
            new = lb[j]
            if old.startswith("# SQT Master Ledger — V4.94") and new == old.replace("V4.94", "V4.95"):
                n_title += 1; j += 1; break
            if old.startswith("**As of:** October 7, 2026 (V4.94 fold — "):
                tail = old[len("**As of:** October 7, 2026 (V4.94 fold — "):]
                if new.startswith("**As of:** October 7, 2026 (V4.95 fold — ") and new.endswith(
                        "V4.94 fold (October 7, 2026) — " + tail):
                    n_asof += 1; j += 1; break
            got = appended(old, new)
            if got is not None:
                appends[i + 1] = got; j += 1; break
            if new == old:
                j += 1; break
            inserted.append((j, new)); j += 1
        else:
            print("UNMATCHED V4.94 line", i + 1, repr(old[:80])); ok = False
    inserted += [(k, lb[k]) for k in range(j, j2)]

print(f"title rewrites: {n_title}; As-of rewrites: {n_asof}; in-line pointer appends: {len(appends)}; inserted lines: "
      f"{len(inserted)} ({sum(len(x.encode()) + 1 for _, x in inserted)} B); V4.94 lines carried unchanged: {equal_lines} of "
      f"{len(la)}")
missing, extra = set(KEYS) - set(appends), set(appends) - set(KEYS)
print("appends on the expected 9 lines:", not missing and not extra, "| missing:", sorted(missing), "| extra:", sorted(extra))
bad_key = sorted(n for n in KEYS if KEYS[n] not in la[n - 1])
print("every host line contains its typed keyword:", not bad_key, "| failing:", bad_key)

idx = [j for j, _ in inserted]
blocks, start = [], None
for k, j in enumerate(idx):
    if start is None:
        start = j
    if k + 1 == len(idx) or idx[k + 1] != j + 1:
        blocks.append((start, j)); start = None
print("inserted blocks (V4.95 1-based line ranges):", [(x + 1, y + 1) for x, y in blocks])
place_ok = len(blocks) == 4


def frame(blk):
    """Non-blank lines of an inserted block, with the nearest non-blank V4.95 lines before and after it."""
    nb = [k for k in range(blk[0], blk[1] + 1) if lb[k].strip()]
    before = next(k for k in range(nb[0] - 1, -1, -1) if lb[k].strip())
    after = next((k for k in range(nb[-1] + 1, len(lb)) if lb[k].strip()), None)
    return ([lb[k] for k in nb], lb[before], None if after is None else lb[after], nb[0] - before,
            None if after is None else after - nb[-1])


if place_ok:
    rec, sec, rows, chg = (frame(x) for x in blocks)
    place_ok &= (len(rec[0]) == 1 and rec[0][0].startswith("**V4.95 fold-in record (October 7, 2026):**")
                 and rec[2].startswith("**V4.94 fold-in record (October 7, 2026):**") and rec[4] == 2)
    place_ok &= (len(sec[0]) == 6 and sec[0][0].startswith("### §2.95 — ")
                 and sec[1].startswith("**Registers and non-claims.** C1: the ranks R1")
                 and sec[2] == "## J. Multi-Lens Reference and Phase Incommensurability" and sec[3] == 2 and sec[4] == 2)
    place_ok &= (len(rows[0]) == 1 and rows[0][0].startswith("| **Lattice-spacing bound**") and rows[0][0].endswith(" |")
                 and rows[0][0].count("|") == 3
                 and rows[1].startswith("| **Polycrystal validity floor**") and "[→ V4.95 (§2.95): " in rows[1]
                 and rows[2].startswith("| **G-C1 gate** (angle-3") and rows[3] == 1 and rows[4] == 1)
    place_ok &= (len(chg[0]) == 1 and chg[0][0].startswith("*V4.95 (October 7, 2026): additions only")
                 and chg[1].startswith("*V4.94 (October 7, 2026): additions only") and chg[3] == 1 and chg[2] is None)
print("insertions at the declared places (record / §2.95 / one Part VI row / changelog):", place_ok)
heads = [x for _, x in inserted if x.startswith("#")]
print("inserted headings:", heads)

# the A1 verdict paragraph is untouched
a1a = [x for x in la if x.startswith("**A. Polarization gate (A1) — FALSIFIED")]
a1b = [x for x in lb if x.startswith("**A. Polarization gate (A1) — FALSIFIED")]
a1_ok = len(a1a) == 1 and a1a == a1b
print("§2.92.A (the A1 verdict) unchanged:", a1_ok)
n_ptr = b.count("[→ V4.95 (§2.95): ")
n_ins = sum(x.count("[→ V4.95") for _, x in inserted)
print("'[→ V4.95 (§2.95): ' occurrences in V4.95:", n_ptr, "(expected 9, all in appends); '[→ V4.95' inside inserted "
      "text:", n_ins, "(the §2.95 preamble, the record and the changelog each name the pointer form once)")
ok &= (n_title == 1 and n_asof == 1 and not missing and not extra and not bad_key and place_ok and a1_ok
       and heads == ["### §2.95 — The Lattice-Spacing Bound: How Fine the Lattice Must Be for the Light Window (V4.95)"]
       and n_ptr == 9 and sum(x.count("[→ V4.95 (§2.95): ") for _, x in inserted) == 0 and n_ins == 3
       and a.count("V4.95") == 0 and equal_lines + n_title + n_asof + len(appends) == len(la))
print("ADDITIVITY CHECK:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
