#!/usr/bin/env python3
"""Independent additivity check V4.97 -> V4.98 (shares no code with the fold script).

Usage: python3 verify_v4_98_additive.py <path to the V4.98 file (canonical or dry run)>

Every V4.97 line must survive in V4.98 either unchanged or as an in-line append whose added text is one
"[→ V4.98 (§2.98): …]" pointer. The appends must sit on exactly the seven V4.97 lines below, typed from the brief's
Step 4b list and Phase C's "found, not annotated" items (PHASE_C_REPORT.md, decision 5), not from the fold script; each
host line must contain the keyword typed here and its pointer the fact typed here. The only rewrites allowed are the title
and the As-of line (the old As-of text kept verbatim). Every other difference must be a pure insertion at the three
declared places. §2.97, §2.92.A and the frozen §2.52 Open 3 row must be unchanged."""
import difflib, hashlib, re, sys

a = open("/home/claude/fold/SQT_Master_Ledger_v4_97_CANONICAL.md", encoding="utf-8").read()
b = open(sys.argv[1], encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "a5a07bcd4f8ca13c87f65974d5580f24"
print("V4.98 file:", sys.argv[1], "md5:", hashlib.md5(b.encode()).hexdigest(), "bytes:", len(b.encode()), "delta:",
      len(b.encode()) - len(a.encode()))
la, lb = a.split("\n"), b.split("\n")
PTR = re.compile(r"^ \[→ V4\.98 \(§2\.98\): [^\n]*\]$")
KEYS = {   # V4.97 line (1-based): (keyword on the host line, fact the pointer must state)
    39: ("V4.97 fold-in record", "fold note (3) is withdrawn"),
    1952: ("face-inheritance principle", "3, 7 and 15"),
    2583: ("L1.5 selection is chirality-uniform", "(3,12), (5,10) and (6,9) have χ = +1"),
    3713: ("Canary threat-model interpretation", "prime number theorem for arithmetic progressions"),
    4401: ("top quark's knot assignment", "7₁, the torus knot T(2,7), is also chiral"),
    4434: ("Each snap event", "not a division algebra"),
    4484: ("Position A — tension-carrying filaments", "hexagonal (honeycomb) tiling"),
}

ok = True
n_title = n_asof = 0
appends, inserted = {}, []
equal = 0
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        equal += i2 - i1; continue
    if tag == "delete":
        print("UNEXPECTED delete", i1 + 1, i2); ok = False; continue
    if tag == "insert":
        inserted += [(j, lb[j]) for j in range(j1, j2)]; continue
    j = j1
    for i in range(i1, i2):
        old = la[i]
        while j < j2:
            new = lb[j]
            if old == "# SQT Master Ledger — V4.97 Canonical" and new == "# SQT Master Ledger — V4.98 Canonical":
                n_title += 1; j += 1; break
            if old.startswith("**As of:** October 8, 2026 (V4.97 fold — "):
                tail = old[len("**As of:** October 8, 2026 (V4.97 fold — "):]
                if new.startswith("**As of:** October 8, 2026 (V4.98 fold — ") and new.endswith(
                        "V4.97 fold (October 8, 2026) — " + tail):
                    n_asof += 1; j += 1; break
            if new.startswith(old) and len(new) > len(old) and PTR.match(new[len(old):]) \
                    and new[len(old):].count("[→ V4.98") == 1:
                appends[i + 1] = new[len(old):]; j += 1; break
            if new == old:
                j += 1; break
            inserted.append((j, new)); j += 1
        else:
            print("UNMATCHED V4.97 line", i + 1, repr(old[:80])); ok = False
    inserted += [(k, lb[k]) for k in range(j, j2)]
print(f"title: {n_title}; As-of: {n_asof}; appends: {len(appends)}; inserted lines: {len(inserted)}; unchanged: {equal} of {len(la)}")
missing, extra = set(KEYS) - set(appends), set(appends) - set(KEYS)
print("appends on the expected 7 lines:", not missing and not extra, "| missing:", sorted(missing), "| extra:", sorted(extra))
bad = sorted(n for n, (kw, fact) in KEYS.items() if kw not in la[n - 1] or (n in appends and fact not in appends[n]))
print("host keywords and pointer facts as typed:", not bad, "| failing:", bad)

idx = [j for j, _ in inserted]
blocks, st = [], None
for k, j in enumerate(idx):
    if st is None: st = j
    if k + 1 == len(idx) or idx[k + 1] != j + 1:
        blocks.append((st, j)); st = None
print("inserted blocks:", [(x + 1, y + 1) for x, y in blocks])


def frame(blk):
    nb = [k for k in range(blk[0], blk[1] + 1) if lb[k].strip()]
    before = next(k for k in range(nb[0] - 1, -1, -1) if lb[k].strip())
    after = next((k for k in range(nb[-1] + 1, len(lb)) if lb[k].strip()), None)
    return [lb[k] for k in nb], lb[before], (None if after is None else lb[after]), nb[0] - before, (
        None if after is None else after - nb[-1])


place = len(blocks) == 3
if place:
    rec, sec, chg = (frame(x) for x in blocks)
    place &= (len(rec[0]) == 1 and rec[0][0].startswith("**V4.98 fold-in record (October 8, 2026):**")
              and rec[2].startswith("**V4.97 fold-in record (October 8, 2026):**") and rec[4] == 2)
    place &= (sec[0][0] == "### §2.98 — The Remaining Mathematics after the Close-Out (V4.98)"
              and sec[1].startswith("**Registers and non-claims.** This is a decision record.")
              and sec[2] == "## J. Multi-Lens Reference and Phase Incommensurability" and sec[3] == 2 and sec[4] == 2
              and any(x.startswith("**Registers and non-claims.** Annotations only") for x in sec[0]))
    place &= (len(chg[0]) == 1 and chg[0][0].startswith("*V4.98 (October 8, 2026): additions only")
              and chg[1].startswith("*V4.97 (October 8, 2026): additions only") and chg[3] == 1 and chg[2] is None)
print("insertions at the declared places (record / §2.98 / changelog):", place)
heads = [x for _, x in inserted if x.startswith("#")]
fixed = {"§2.92.A": "**A. Polarization gate (A1) — FALSIFIED", "§2.52 Open 3 row": "| **§2.52 Open 3**",
         "§2.97 heading": "### §2.97 — Closing the Substrate Program (V4.97)", "§2.97 C(f)": "- **(f) §2.52 Open 3",
         "Substrate program row": "| **Substrate program — CLOSED (V4.97)**"}
fixed_ok = True
for name, p in fixed.items():
    xa, xb = [x for x in la if x.startswith(p)], [x for x in lb if x.startswith(p)]
    good = len(xa) == 1 and xa == xb
    fixed_ok &= good
    print(name, "unchanged:", good)
n_ptr = b.count("[→ V4.98 (§2.98): ")
print("'[→ V4.98 (§2.98): ' occurrences:", n_ptr, "(expected 7, all in appends)")
ok &= (n_title == 1 and n_asof == 1 and not missing and not extra and not bad and place and fixed_ok
       and heads == ["### §2.98 — The Remaining Mathematics after the Close-Out (V4.98)"] and n_ptr == 7
       and sum(x.count("[→ V4.98 (§2.98): ") for _, x in inserted) == 0 and a.count("V4.98") == 0
       and equal + n_title + n_asof + len(appends) == len(la))
print("ADDITIVITY CHECK:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
