#!/usr/bin/env python3
"""Independent additivity check V4.99 -> V4.100 (shares no code with the fold script).

Usage: python3 verify_v4_100_additive.py <path to the V4.100 file (canonical or dry run)>

Every V4.99 line must survive in V4.100 either unchanged or with one appended "[→ V4.100 (§2.100): …]" pointer: at the
end of a paragraph line, or just before the closing " |" of a table row. The appends must sit on exactly the seven V4.99
lines below, which carry V4.94's "q > 1032" (four), the Phase C note row (one), and the gauge paper's B1 entry and Phase B
row (two, added October 13 with the deposits), typed here from the correction and the deposit records themselves, not
from the fold script; each host must contain the keyword typed here and its pointer every fact typed here.
The only rewrites allowed are the title and the As-of line (the old As-of text kept verbatim). Every other difference
must be a pure insertion at the three declared places. §2.94's heading and C1 paragraph, §2.97, §2.99 and the frozen
§2.52 Open 3 row must be unchanged."""
import difflib, hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
a = open(os.path.join(HERE, "..", "..", "SQT_Master_Ledger_v4_99_CANONICAL.md"), encoding="utf-8").read()
b = open(sys.argv[1], encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "a86fa0907310b34413b42d7ebdbcb067"
print("V4.100 file:", sys.argv[1], "md5:", hashlib.md5(b.encode()).hexdigest(), "bytes:", len(b.encode()), "delta:",
      len(b.encode()) - len(a.encode()))
la, lb = a.split("\n"), b.split("\n")
PTR = re.compile(r"^ \[→ V4\.100 \(§2\.100\): [^\n|]*\]$")
KEYS = {   # V4.99 line (1-based): (keyword on the host line, fact the pointer must state)
    3484: ("holds deterministically for any q > 1032", "q = 1036"),
    3682: ("(q > 1032 at η = 2)", "q = 1036"),
    4638: ("**Phase C draft awaiting the author**", ("10.5281/zenodo.23270249", "10.5281/zenodo.23351706")),
    4651: ("a differential needs q ≤ 1032", "q ≤ 1035"),
    4746: ("(DFR = 0 for any q > 1032 at η = 2)", "q = 1036"),
    1724: ("**B1. Gauge paper v6.3 — correction drafted (v6.4).**", ("10.5281/zenodo.23351330", "October 13, 2026")),
    4635: ("**Phase B drafts awaiting the author** (gauge paper v6.4 → Zenodo;", ("10.5281/zenodo.23351330",)),
}


def appended(old, new):
    """The pointer text if new = old plus one pointer (paragraph end, or before a row's closing ' |'), else None."""
    if new.startswith(old) and len(new) > len(old) and not old.endswith(" |"):
        add = new[len(old):]
    elif old.endswith(" |") and new.endswith(" |") and new.startswith(old[:-2]) and len(new) > len(old):
        add = new[len(old) - 2:-2]
    else:
        return None
    return add if PTR.match(add) and add.count("[→ V4.100") == 1 else None


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
            if old == "# SQT Master Ledger — V4.99 Canonical" and new == "# SQT Master Ledger — V4.100 Canonical":
                n_title += 1; j += 1; break
            if old.startswith("**As of:** October 8, 2026 (V4.99 fold — "):
                tail = old[len("**As of:** October 8, 2026 (V4.99 fold — "):]
                if new.startswith("**As of:** ") and "(V4.100 fold — " in new and new.endswith(
                        "V4.99 fold (October 8, 2026) — " + tail):
                    n_asof += 1; j += 1; break
            add = appended(old, new)
            if add is not None:
                appends[i + 1] = add; j += 1; break
            if new == old:
                j += 1; break
            inserted.append((j, new)); j += 1
        else:
            print("UNMATCHED V4.99 line", i + 1, repr(old[:80])); ok = False
    inserted += [(k, lb[k]) for k in range(j, j2)]
print(f"title: {n_title}; As-of: {n_asof}; appends: {len(appends)}; inserted lines: {len(inserted)}; unchanged: {equal} of {len(la)}")
missing, extra = set(KEYS) - set(appends), set(appends) - set(KEYS)
print("appends on the expected 7 lines:", not missing and not extra, "| missing:", sorted(missing), "| extra:", sorted(extra))
bad = sorted(n for n, (kw, fact) in KEYS.items()
             if kw not in la[n - 1] or (n in appends and any(f not in appends[n]
                                                            for f in (fact if isinstance(fact, tuple) else (fact,)))))
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
DEPOSITS = ("10.5281/zenodo.23270249", "10.5281/zenodo.23351330", "10.5281/zenodo.23351706", "d1b8507a", "6bd55206",
            "10.5281/zenodo.19157947", "10.5281/zenodo.20078311", "10.5281/zenodo.23270248")
if place:
    rec, sec, chg = (frame(x) for x in blocks)
    place &= (len(rec[0]) == 1 and rec[0][0].startswith("**V4.100 fold-in record (")
              and rec[2].startswith("**V4.99 fold-in record (October 8, 2026):**") and rec[4] == 2)
    place &= (sec[0][0] == "### §2.100 — The SLWE Decryption Threshold, and Three Zenodo Deposits (V4.100)"
              and sec[1].startswith("**Registers and non-claims.** One R1 fact, one leg; three classifications")
              and sec[2] == "## J. Multi-Lens Reference and Phase Incommensurability" and sec[3] == 2 and sec[4] == 2
              and any(x.startswith("**Registers and non-claims.** One R1 fact, one leg; estate facts") for x in sec[0]))
    place &= (len(chg[0]) == 1 and chg[0][0].startswith("*V4.100 (") and "additions only" in chg[0][0]
              and chg[1].startswith("*V4.99 (October 8, 2026): additions only") and chg[3] == 1 and chg[2] is None)
print("insertions at the declared places (record / §2.100 / changelog):", place)
sec_text = "\n".join(x for _, x in inserted)
dep_ok = all(d in sec_text for d in DEPOSITS)
print("deposit facts present in the inserted text:", dep_ok, "| missing:", [d for d in DEPOSITS if d not in sec_text])
heads = [x for _, x in inserted if x.startswith("#")]
fixed = {"§2.94 heading": "### §2.94 — The October 2026 Audit Follow-Up, Phase C",
         "§2.94 C1 paragraph": "**C1. The SLWE negative result.**",
         "§2.97 heading": "### §2.97 — Closing the Substrate Program (V4.97)",
         "§2.99 heading": "### §2.99 — The Author's Close-Out Decisions (V4.99)",
         "§2.52 Open 3 row": "| **§2.52 Open 3**", "§2.97 C(f)": "- **(f) §2.52 Open 3"}
fixed_ok = True
for name, p in fixed.items():
    xa, xb = [x for x in la if x.startswith(p)], [x for x in lb if x.startswith(p)]
    good = len(xa) == 1 and xa == xb
    fixed_ok &= good
    print(name, "unchanged:", good)
n_ptr = b.count("[→ V4.100 (§2.100): ")
print("'[→ V4.100 (§2.100): ' occurrences:", n_ptr, "(expected 7, all in appends)")
ok &= (dep_ok and n_title == 1 and n_asof == 1 and not missing and not extra and not bad and place and fixed_ok
       and heads == ["### §2.100 — The SLWE Decryption Threshold, and Three Zenodo Deposits (V4.100)"]
       and n_ptr == 7 and sum(x.count("[→ V4.100 (§2.100): ") for _, x in inserted) == 0 and a.count("V4.100") == 0
       and equal + n_title + n_asof + len(appends) == len(la))
print("ADDITIVITY CHECK:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
