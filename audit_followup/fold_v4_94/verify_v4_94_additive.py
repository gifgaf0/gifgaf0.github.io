#!/usr/bin/env python3
"""Independent additivity check V4.93 -> V4.94 (shares no code with the fold script).

Every V4.93 line must survive in V4.94 either unchanged or as an in-line append whose added text is one
"[→ V4.94 (§2.94.C1|C2): …]" bracket (at the end of a paragraph line, or just before the closing " |" of a table row).
The appends must sit on exactly the 113 V4.93 lines below — 34 for C1 and 79 for C2, typed from C1_RESULT.md and
C2_RESULT.md, independently of the fold script's prefixes — and each host line must contain the keyword typed here from a
reading of that line (a guard against a mis-aimed anchor). The only rewrites allowed are the declared title and As-of lines;
the As-of rewrite must keep the whole old text after its version label. Every other difference must be a pure insertion, at
the four declared places. The §2.52 Open 3 row may change only by the one authorized append (the G-ζ1 result)."""
import difflib, hashlib, re, sys

a = open("/home/claude/fold/SQT_Master_Ledger_v4_93_CANONICAL.md", encoding="utf-8").read()
b = open("/home/claude/fold/SQT_Master_Ledger_v4_94_CANONICAL.md", encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "0aa63a0bec9becbfb911dba3454255f2"
print("V4.94 md5:", hashlib.md5(b.encode()).hexdigest(), "bytes:", len(b.encode()), "delta:", len(b.encode()) - len(a.encode()))
la, lb = a.split("\n"), b.split("\n")
BR = re.compile(r"^ \[→ V4\.94 \(§2\.94\.C([12])\): [^\n]*\]$")

C1_KEYS = {
    3233: "single technical thread", 3241: "Tier 4 (theoretical sketch", 3290: "OP-2.58.1.a — CBD-baseline DFR",
    3292: "OP-2.58.5 (new", 3332: "sum-to-14 ZD complement rule", 3335: "Negative result (R1, by exhaustive comparison)",
    3347: "sum-14 complement constraint", 3359: "BFS verdict", 3374: "RD-03: OSP-Lattice",
    3445: "Production scaling at spec", 3453: "actually-binding parameter question is q itself", 3474: "Var(N) = 129",
    3490: "Closure declaration", 3525: "What this DOES establish", 3539: "OP-2.58.2c", 3541: "OP-2.58.2e",
    3543: "Closure conditions", 3817: "Security reading (scoped, R2)", 4421: "Gate G-BKZ32", 4444: "OP-2.58.1.a",
    4445: "OP-2.58.1.b", 4446: "OP-2.58.2** (Fano-line class leakage", 4447: "OP-2.58.2c", 4448: "OP-2.58.2d",
    4449: "OP-2.58.2e", 4452: "OP-2.58.5", 4453: "OP-2.59-A, B, C", 4454: "RD-01 to RD-04",
    4458: "§2.66.2 source recovery", 4459: "Cluster M citation hygiene", 4539: "§3.1 ephemeral-distribution fix",
    4540: "OP-2.58.1a harness port", 4608: "OQ-01", 4611: "OP-2.58.1.a",
}
C2_KEYS = {
    # P1
    4364: "zeta_tax_unified_picture", 4378: "G-FOLD1 gate", 4599: "ζ-tax gate 3",
    # P2
    293: "c is defined as the propagation speed", 1632: "Gate G-SCALE1 EXECUTED", 1658: "Gate G-CI1 REGISTERED",
    4420: "Gate G-CI1", 4424: "Gate G-S2C1-W",
    # P3
    279: "Worked examples (corrected)", 283: "Why the motivating frustration", 424: "2π-B", 1373: "first-stable-closure",
    1379: "r_eff(electron) ≡ 1 by definition", 1662: "Gate G-QUANTA REGISTERED", 1672: "Gate G-VS1 REGISTERED",
    4255: "Electron", 4376: "electron_cl2_filtration_floor", 4382: "stability and composite quanta",
    4425: "Gate G-QUANTA", 4610: "OP-2.14",
    # P4
    1045: "μ_p = (4μ_u − μ_d)/3", 1053: "Spin-3/2 is the **faithful**", 1057: "spinorial promotion",
    1067: "The reduction [R1 core + R2]", 1080: "fermionic geometry is **six-dimensional**", 1084: "Net for μ_n",
    1096: "forced assignment question", 1100: "four-4", 1118: "Gate 2a, sharpened", 1134: "Net (R2, conditional",
    1154: "octahedral premise relocates", 1666: "Gate G-2a-A1 REGISTERED", 4438: "G-2a-S1 / G-2a-S2",
    4563: "μ_n spinor-promotion gate", 4565: "↔ spin-3/2", 4574: "Gate 2a — is the baryon",
    4578: "Factor-assignment question", 4579: "Soliton spin-isospin locking",
    # P5
    4393: "§2.52 Open 3",
    # math
    2771: "OP-2.81.1 (R2)", 2772: "OP-2.81.2 (R2)", 4468: "OP-2.81.1", 4469: "OP-2.81.2",
    2149: "Why this excludes the identity matching", 2194: "capacity exhaustion", 4478: "OP-2.67.1b",
    496: "§2.68.8.1 supplies the structural mechanism", 2353: "involutions and order-4 elements",
    3215: "F₂₁ vertex-permutations", 3219: "principal anti-automorphism", 1760: "168 co-occurrence is a coincidence",
    4587: "G-2a.3", 2461: "Lifted to SL(2,7)", 2371: "OP-2.75-CR", 2494: "Galois-twist relation", 4543: "OP-2.75-CR",
    2853: "collapse to Cℓ(0,2)", 2857: "Schur consistency", 2869: "does NOT natively harbor", 2531: "V4.7 update",
    2003: "ZD quadruples found", 2060: "OP-2.67.1a — CLOSED", 2068: "Resolved (Tier 2)", 1782: "1-factorizations",
    1950: "arctan(1/√2)", 1792: "log(4π)/log(7)", 3402: "Sign Duality", 3412: "Orbit-stabilizer accounting",
    484: "Theorem 4.", 1740: "V₄ stabilizer", 3189: "Fixing the imaginary unit e₇", 2440: "OP-2.74.1c.i.",
    2442: "OP-2.74.1c.iii.", 4531: "OP-2.74.1c.i**", 4533: "OP-2.74.1c.iii**", 1972: "7 orbits of 12 elements",
    2036: "42-edge combinatorial object", 408: "1.099% gap", 1353: "84/arctan(1/√2)",
}
assert len(C1_KEYS) == 34 and len(C2_KEYS) == 79 and not set(C1_KEYS) & set(C2_KEYS)
EXPECTED = {**{k: "1" for k in C1_KEYS}, **{k: "2" for k in C2_KEYS}}


def appended(old, new):
    """Return (part, added text) if `new` is `old` with one bracket appended (paragraph) or inserted before ' |' (row)."""
    if old.endswith(" |") and old.startswith("| "):
        if new.endswith(" |") and new.startswith(old[:-2]) and len(new) > len(old):
            add = new[len(old) - 2:-2]
            m = BR.match(add)
            return (m.group(1), add) if m and add.count("[→ V4.94") == 1 else None
        return None
    if new.startswith(old) and len(new) > len(old):
        add = new[len(old):]
        m = BR.match(add)
        return (m.group(1), add) if m and add.count("[→ V4.94") == 1 else None
    return None


ok = True
n_title = n_asof = 0
appends = {}                       # V4.93 line number (1-based) -> (part, added text)
inserted = []                      # (V4.94 index, text)
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
equal_lines = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        equal_lines += i2 - i1
        continue
    if tag == "delete":
        print("UNEXPECTED delete of V4.93 lines", i1 + 1, "-", i2); ok = False; continue
    if tag == "insert":
        inserted += [(j, lb[j]) for j in range(j1, j2)]; continue
    j = j1
    for i in range(i1, i2):
        old = la[i]
        while j < j2:
            new = lb[j]
            if old.startswith("# SQT Master Ledger — V4.93") and new == old.replace("V4.93", "V4.94"):
                n_title += 1; j += 1; break
            if old.startswith("**As of:** October 7, 2026 (V4.93 fold — "):
                tail = old[len("**As of:** October 7, 2026 (V4.93 fold — "):]
                if new.startswith("**As of:** October 7, 2026 (V4.94 fold — ") and new.endswith(
                        "V4.93 fold (October 7, 2026) — " + tail):
                    n_asof += 1; j += 1; break
            got = appended(old, new)
            if got is not None:
                appends[i + 1] = got; j += 1; break
            if new == old:
                j += 1; break
            inserted.append((j, new)); j += 1
        else:
            print("UNMATCHED V4.93 line", i + 1, repr(old[:80])); ok = False
    inserted += [(k, lb[k]) for k in range(j, j2)]

print(f"title rewrites: {n_title}; As-of rewrites: {n_asof}; in-line bracket appends: {len(appends)}; inserted lines: "
      f"{len(inserted)} ({sum(len(x.encode()) + 1 for _, x in inserted)} B); V4.93 lines carried unchanged: {equal_lines} of "
      f"{len(la)}")
missing, extra = set(EXPECTED) - set(appends), set(appends) - set(EXPECTED)
print("appends on the expected 113 lines:", not missing and not extra, "| missing:", sorted(missing), "| extra:",
      sorted(extra))
wrong_part = sorted(n for n, (p, _) in appends.items() if n in EXPECTED and EXPECTED[n] != p)
print("each append carries its line's part (C1 / C2):", not wrong_part, "| mismatched:", wrong_part)
bad_key = sorted(n for n in EXPECTED if (C1_KEYS.get(n) or C2_KEYS.get(n)) not in la[n - 1])
print("every host line contains its typed keyword:", not bad_key, "| failing:", bad_key)
by_part = {"C1": 0, "C2": 0}
for n, (p, _) in appends.items():
    by_part["C" + p] += 1
print("appends by part:", by_part)

# where the insertions landed (each block must be contiguous and sit at its declared place)
idx = [j for j, _ in inserted]
blocks, start = [], None
for k, j in enumerate(idx):
    if start is None:
        start = j
    if k + 1 == len(idx) or idx[k + 1] != j + 1:
        blocks.append((start, j)); start = None
print("inserted blocks (V4.94 1-based line ranges):", [(x + 1, y + 1) for x, y in blocks])
place_ok = len(blocks) == 4


def frame(blk):
    """Non-blank lines of an inserted block, with the nearest non-blank V4.94 lines before and after it (blank lines are
    ignored when locating a block, since which blank difflib calls 'inserted' is arbitrary)."""
    nb = [k for k in range(blk[0], blk[1] + 1) if lb[k].strip()]
    before = next(k for k in range(nb[0] - 1, -1, -1) if lb[k].strip())
    after = next((k for k in range(nb[-1] + 1, len(lb)) if lb[k].strip()), None)
    return ([lb[k] for k in nb], lb[before], None if after is None else lb[after], nb[0] - before,
            None if after is None else after - nb[-1])


if place_ok:
    rec, sec, rows, chg = (frame(x) for x in blocks)
    place_ok &= (len(rec[0]) == 1 and rec[0][0].startswith("**V4.94 fold-in record (October 7, 2026):**")
                 and rec[2].startswith("**V4.93 fold-in record (October 7, 2026):**") and rec[4] == 2)
    place_ok &= (len(sec[0]) == 5 and sec[0][0].startswith("### §2.94 — ")
                 and sec[1].startswith("**Registers and non-claims.** B1's three verdicts")
                 and sec[2] == "## J. Multi-Lens Reference and Phase Incommensurability" and sec[3] == 2 and sec[4] == 2)
    place_ok &= (len(rows[0]) == 3 and all(x.startswith("| **") and x.endswith(" |") for x in rows[0])
                 and rows[1].startswith("| **Alpha-decay paper: correction of the deposit**")
                 and rows[2].startswith("| **G-C1 gate** (angle-3") and rows[3] == 1 and rows[4] == 1)
    place_ok &= (len(chg[0]) == 1 and chg[0][0].startswith("*V4.94 (October 7, 2026): additions only")
                 and chg[1].startswith("*V4.93 (October 7, 2026): additions only") and chg[3] == 1 and chg[2] is None)
print("insertions at the declared places (record / §2.94 / three Part VI rows / changelog):", place_ok)
heads = [x for _, x in inserted if x.startswith("#")]
print("inserted headings:", heads)

# §2.52 Open 3: the V4.93 row plus exactly one append, the G-ζ1 result, freeze kept
o3a = [x for x in la if x.startswith("| **§2.52 Open 3**")]
o3b = [x for x in lb if x.startswith("| **§2.52 Open 3**")]
o3_ok = (len(o3a) == 1 and len(o3b) == 1 and o3b[0].startswith(o3a[0][:-2] + " [→ V4.94 (§2.94.C2): the G-ζ1 result")
         and o3b[0].endswith("The row stays Open and frozen.] |") and o3b[0].count("[→ V4.94") == 1
         and "**Open**" in o3b[0] and o3a[0][:-2] in o3b[0])
print("§2.52 Open 3: V4.93 row + exactly the one authorized append (G-ζ1; Open and frozen):", o3_ok)
n_v494 = b.count("[→ V4.94 (§2.94.C")
n_ins = sum(x.count("[→ V4.94 (§2.94.C") for _, x in inserted)    # §2.94's own sentence naming the two pointer forms
print("'[→ V4.94 (§2.94.C' occurrences in V4.94:", n_v494, "= 113 appends +", n_ins, "in inserted text (expected 2, the "
      "§2.94 preamble naming the pointer forms)")
n_v494 -= n_ins if n_ins == 2 else 0
ok &= (n_title == 1 and n_asof == 1 and not missing and not extra and not wrong_part and not bad_key and place_ok and o3_ok
       and heads == ["### §2.94 — The October 2026 Audit Follow-Up, Phase C: the Crypto Negative Result and the Annotation "
                     "Batch (V4.94)"]
       and by_part == {"C1": 34, "C2": 79} and n_v494 == 113 and a.count("[→ V4.94") == 0
       and equal_lines + n_title + n_asof + len(appends) == len(la))
print("ADDITIVITY CHECK:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
