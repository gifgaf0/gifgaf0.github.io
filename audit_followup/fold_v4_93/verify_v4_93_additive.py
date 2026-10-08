#!/usr/bin/env python3
"""Independent additivity check V4.92 -> V4.93 (shares no code with the fold script).

Every V4.92 line must survive in V4.93 either unchanged or as an in-line append whose added text is a "[→ V4.93 …]" bracket
(at the end of a paragraph line, or just before the closing " |" of a table row). The appends must sit on exactly the 34
V4.92 lines listed below (the blast-radius table of FOLD_AUTHORIZATION_V4_93.md, typed independently of the fold script's
prefixes). The only rewrites allowed are the declared title and As-of lines; the As-of rewrite must keep the whole old text
after its version label. Every other difference must be a pure insertion, at the four declared places. The §2.52 Open 3
row must be untouched."""
import difflib, hashlib, re, sys

a = open("/home/claude/fold/SQT_Master_Ledger_v4_92_CANONICAL.md", encoding="utf-8").read()
b = open("/home/claude/fold/SQT_Master_Ledger_v4_93_CANONICAL.md", encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "a98cf1b6f12578537e11270d2cdf0fda"
print("V4.93 md5:", hashlib.md5(b.encode()).hexdigest(), "bytes:", len(b.encode()), "delta:", len(b.encode()) - len(a.encode()))
la, lb = a.split("\n"), b.split("\n")
BR = re.compile(r"^ \[→ V4\.93 \(§2\.93\.B[0-5][^\n]*\]$")
EXPECTED = {227, 315, 349, 385, 395, 396, 500, 527, 532, 534, 539, 655, 1008, 1065, 1069, 1431, 1682, 2193, 2219, 2260,
            2269, 2351, 2507, 2773, 2920, 3050, 3207, 3880, 3884, 3913, 4359, 4360, 4477, 4553}
assert len(EXPECTED) == 34


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
n_title = n_asof = 0
appends = {}                       # V4.92 line number (1-based) -> added text
inserted = []                      # (V4.93 index, text)
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
equal_lines = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        equal_lines += i2 - i1
        continue
    if tag == "delete":
        print("UNEXPECTED delete of V4.92 lines", i1 + 1, "-", i2); ok = False; continue
    if tag == "insert":
        inserted += [(j, lb[j]) for j in range(j1, j2)]; continue
    j = j1
    for i in range(i1, i2):
        old = la[i]
        while j < j2:
            new = lb[j]
            if old.startswith("# SQT Master Ledger — V4.92") and new == old.replace("V4.92", "V4.93"):
                n_title += 1; j += 1; break
            if old.startswith("**As of:** October 7, 2026 (V4.92 fold — "):
                tail = old[len("**As of:** October 7, 2026 (V4.92 fold — "):]
                if new.startswith("**As of:** October 7, 2026 (V4.93 fold — ") and new.endswith(
                        "V4.92 fold (October 7, 2026) — " + tail):
                    n_asof += 1; j += 1; break
            add = appended(old, new)
            if add is not None:
                appends[i + 1] = add; j += 1; break
            if new == old:
                j += 1; break
            inserted.append((j, new)); j += 1
        else:
            print("UNMATCHED V4.92 line", i + 1, repr(old[:80])); ok = False
    inserted += [(k, lb[k]) for k in range(j, j2)]

print(f"title rewrites: {n_title}; As-of rewrites: {n_asof}; in-line bracket appends: {len(appends)}; inserted lines: "
      f"{len(inserted)} ({sum(len(x.encode()) + 1 for _, x in inserted)} B); V4.92 lines carried unchanged: {equal_lines} of "
      f"{len(la)}")
missing, extra = EXPECTED - set(appends), set(appends) - EXPECTED
print("appends on the expected 34 lines:", not missing and not extra, "| missing:", sorted(missing), "| extra:", sorted(extra))
by_part = {}
for n, add in appends.items():
    k = re.match(r" \[→ V4\.93 \((§2\.93\.B[0-5])", add).group(1)
    by_part[k] = by_part.get(k, 0) + 1
print("appends by part:", dict(sorted(by_part.items())))

# where the insertions landed (each block must be contiguous and sit at its declared place)
idx = [j for j, _ in inserted]
blocks, start = [], None
for k, j in enumerate(idx):
    if start is None:
        start = j
    if k + 1 == len(idx) or idx[k + 1] != j + 1:
        blocks.append((start, j)); start = None
print("inserted blocks (V4.93 1-based line ranges):", [(x + 1, y + 1) for x, y in blocks])
place_ok = len(blocks) == 4


def frame(blk):
    """Non-blank lines of an inserted block, with the nearest non-blank V4.93 lines before and after it. (Which blank
    line difflib calls 'inserted' is arbitrary, so blanks are ignored when locating a block.)"""
    nb = [k for k in range(blk[0], blk[1] + 1) if lb[k].strip()]
    before = next(k for k in range(nb[0] - 1, -1, -1) if lb[k].strip())
    after = next((k for k in range(nb[-1] + 1, len(lb)) if lb[k].strip()), None)   # None: end of file
    return ([lb[k] for k in nb], lb[before], None if after is None else lb[after], nb[0] - before,
            None if after is None else after - nb[-1])


if place_ok:
    rec, sec, rows, chg = (frame(x) for x in blocks)
    place_ok &= (len(rec[0]) == 1 and rec[0][0].startswith("**V4.93 fold-in record (October 7, 2026):**")
                 and rec[2].startswith("**V4.92 fold-in record (October 7, 2026):**") and rec[4] == 2)
    place_ok &= (len(sec[0]) == 9 and sec[0][0].startswith("### §2.93 — ")
                 and sec[1].startswith("**Registers and non-claims.** A1–A3")
                 and sec[2] == "## J. Multi-Lens Reference and Phase Incommensurability" and sec[3] == 2 and sec[4] == 2)
    place_ok &= (len(rows[0]) == 3 and all(x.startswith("| **") and x.endswith(" |") for x in rows[0])
                 and rows[1].startswith("| **Gate G-RCX1**") and rows[2].startswith("| **G-C1 gate** (angle-3")
                 and rows[3] == 1 and rows[4] == 1)
    place_ok &= (len(chg[0]) == 1 and chg[0][0].startswith("*V4.93 (October 7, 2026): additions only")
                 and chg[1].startswith("*V4.92 (October 7, 2026): additions only") and chg[3] == 1)
print("insertions at the declared places (record / §2.93 / three Part VI rows / changelog):", place_ok)
heads = [x for _, x in inserted if x.startswith("#")]
print("inserted headings:", heads)
o3a = [x for x in la if x.startswith("| **§2.52 Open 3**")]
o3b = [x for x in lb if x.startswith("| **§2.52 Open 3**")]
print("§2.52 Open 3 row identical and unique:", o3a == o3b and len(o3a) == 1)
ok &= (n_title == 1 and n_asof == 1 and not missing and not extra and place_ok and o3a == o3b and len(o3a) == 1
       and heads == ["### §2.93 — The October 2026 Audit Follow-Up, Phase B: Papers and Calculators (V4.93)"]
       and equal_lines + n_title + n_asof + len(appends) == len(la))
print("ADDITIVITY CHECK:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
