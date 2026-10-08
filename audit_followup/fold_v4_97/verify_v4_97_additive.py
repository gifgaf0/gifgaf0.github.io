#!/usr/bin/env python3
"""Independent additivity check V4.96 -> V4.97 (shares no code with the fold script).

Usage: python3 verify_v4_97_additive.py <path to the V4.97 file (canonical or dry run)>

Every V4.96 line must survive in V4.97 unchanged, or as an in-line append whose added text is one
"[→ V4.97 (§2.97): …]" pointer. Three lines may be rewritten:
  - the title;
  - the As-of line, with the old text kept verbatim after "V4.96 fold (October 7, 2026) — ";
  - the Status line, with a note inserted after "**Status:** " and the old text kept verbatim.
The appends must sit on exactly the 46 V4.96 lines below. They are typed from CO1_CLASSIFICATION.md's "Pointer = yes" rows
and from the brief's three Preamble/§2.91.D items, independently of the fold script's code. Each host line must contain
the keyword typed here, and its pointer must say what its rule says.

Every other difference must be a pure insertion at a declared place:
  - the record;
  - eleven banners, each directly under its heading;
  - §2.97;
  - two Part VI rows under the lattice-spacing-bound row;
  - the intake block before "Closed / dropped";
  - the changelog line.
§2.97 must equal the approved draft with exactly its two fill-ins. Must be unchanged: §2.92.A, the frozen §2.52 Open 3 row
and §2.52's body, and the rows the sweep leaves alone because they are already closed (G-POLY1, §3.4-G2-CHIRAL, ζ-tax
gate 3, the polycrystal floor, the factor-assignment question)."""
import difflib
import hashlib
import re
import sys

a = open("/home/claude/fold/SQT_Master_Ledger_v4_96_CANONICAL.md", encoding="utf-8").read()
b = open(sys.argv[1], encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "120b076a613b7ef4074193c03df2cf0d"
draft = open("/home/claude/gifgaf0.github.io/audit_followup/inputs/CLOSING_ENTRY_V4_97_DRAFT.md", encoding="utf-8").read()
assert hashlib.md5(draft.encode()).hexdigest() == "10270b68a446f6025331f132f8d48038"
print("V4.97 file:", sys.argv[1], "md5:", hashlib.md5(b.encode()).hexdigest(), "bytes:", len(b.encode()), "delta:",
      len(b.encode()) - len(a.encode()))
la, lb = a.split("\n"), b.split("\n")
PTR = re.compile(r"^ \[→ V4\.97 \(§2\.97\): [^\n\]]*(\][^\n\]]*)*\]$")
A_SET = {4432: "L4.5 gate", 4434: "§2.50 gate", 4435: "top-quark knot assignment", 4436: "§2.7 ε-per-edge",
         4437: "§2.45-NGA Bjerknes gate", 4438: "§2.53 bilateral fold from §3.4", 4441: "G-ζ1", 4443: "M.ONT gate",
         4444: "Gate G-κ1", 4452: "Gate G-IIB-L1", 4453: "Gate G-CC-ε1", 4454: "Gate G-SCALE1", 4472: "Gate G-OBD1",
         4524: "OP-2.67.1c", 4545: "§2.46 simulation rerun", 4546: "§2.47 6% gap derivation",
         4547: "§3.4 Bjerknes-action Lagrangian audit", 4559: "§3.4-G1‴ / G4", 4592: "OP-2.25.2 branch (b)",
         4596: "OP-2.E-QQ.QQ3", 4607: "μ_n spinor-promotion gate", 4610: "§2.85 Condition 3",
         4618: "Gate 2a — is the baryon's spin geometry", 4623: "Soliton spin-isospin locking derivation",
         4641: "ζ-tax gate 1", 4642: "ζ-tax gate 2", 4644: "ζ-tax gate 4"}
B_SET = {4523: "OP-2.67.1b reframed", 4535: "OP-2.56-A", 4536: "OP-2.56-B", 4538: "OP-2.63", 4555: "§3.4-G2-Milnor-INT",
         4566: "§2.73 Gate A", 4567: "§2.73 Gate B", 4568: "§2.74 Part IV physical mapping", 4574: "OP-2.74.1b",
         4597: "§2.E-QQ promotion gate to R2", 4599: "OP-2.E-QQ.E1", 4619: "ℂ⊗𝕆 ↔ octonion-substrate dictionary",
         4633: "A2 alpha-decay count gate", 4634: "§2.41 / §2.53 rung-numbering reconciliation"}
E_SET = {4473: "Gate G-RCX1", 4556: "§3.4-G2-knot"}
PRE_SET = {243: "### KC-EP — The Equivalence-Principle Kill Condition", 249: "### The Particle-Ontology Declaration Flag",
           1622: "**D. The kill set as amended"}
KEYS = {**A_SET, **B_SET, **E_SET, **PRE_SET}
assert len(A_SET) == 27 and len(B_SET) == 14 and len(E_SET) == 2 and len(KEYS) == 46


def appended(old, new):
    if old.endswith(" |") and old.startswith("| "):
        if new.endswith(" |") and new.startswith(old[:-2]) and len(new) > len(old):
            add = new[len(old) - 2:-2]
            return add if PTR.match(add) and add.count("[→ V4.97") == 1 else None
        return None
    if new.startswith(old) and len(new) > len(old):
        add = new[len(old):]
        return add if PTR.match(add) and add.count("[→ V4.97") == 1 else None
    return None


ok = True
n_title = n_asof = n_status = 0
appends, inserted = {}, []
equal_lines = 0
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        equal_lines += i2 - i1
        continue
    if tag == "delete":
        print("UNEXPECTED delete of V4.96 lines", i1 + 1, "-", i2); ok = False; continue
    if tag == "insert":
        inserted += [(j, lb[j]) for j in range(j1, j2)]; continue
    j = j1
    for i in range(i1, i2):
        old = la[i]
        while j < j2:
            new = lb[j]
            if old.startswith("# SQT Master Ledger — V4.96") and new == old.replace("V4.96", "V4.97"):
                n_title += 1; j += 1; break
            if old.startswith("**As of:** October 7, 2026 (V4.96 fold — "):
                tail = old[len("**As of:** October 7, 2026 (V4.96 fold — "):]
                if new.startswith("**As of:** October 8, 2026 (V4.97 fold — ") and new.endswith(
                        "V4.96 fold (October 7, 2026) — " + tail):
                    n_asof += 1; j += 1; break
            if old.startswith("**Status:** Mathematical foundation frozen."):
                rest = old[len("**Status:** "):]
                if new.startswith("**Status:** **V4.97 (October 8, 2026): ") and new.endswith("** " + rest):
                    n_status += 1; j += 1; break
            got = appended(old, new)
            if got is not None:
                appends[i + 1] = got; j += 1; break
            if new == old:
                j += 1; break
            inserted.append((j, new)); j += 1
        else:
            print("UNMATCHED V4.96 line", i + 1, repr(old[:80])); ok = False
    inserted += [(k, lb[k]) for k in range(j, j2)]

print(f"title rewrites: {n_title}; As-of rewrites: {n_asof}; Status rewrites: {n_status}; in-line pointer appends: "
      f"{len(appends)}; inserted lines: {len(inserted)} ({sum(len(x.encode()) + 1 for _, x in inserted)} B); V4.96 lines "
      f"carried unchanged: {equal_lines} of {len(la)}")
missing, extra = set(KEYS) - set(appends), set(appends) - set(KEYS)
print("appends on the expected 46 lines:", not missing and not extra, "| missing:", sorted(missing), "| extra:", sorted(extra))
bad_key = sorted(n for n in KEYS if KEYS[n] not in la[n - 1])
print("every host line contains its typed keyword:", not bad_key, "| failing:", bad_key)
sem_bad = []
for n, add in appends.items():
    if n in A_SET and not ("closed with the substrate program" in add or "closed unopened with the substrate program" in add):
        sem_bad.append(n)
    if n in B_SET and not ("closes with" in add and ("stays open" in add or "keep" in add)):
        sem_bad.append(n)
    if n in E_SET and not ("Successor intake (not opened)" in add and "not closed" in add):
        sem_bad.append(n)
    if n in (243, 1622) and "standing" not in add:
        sem_bad.append(n)
    if n == 249 and "closed with the substrate program" not in add:
        sem_bad.append(n)
print("each pointer says what its rule says:", not sem_bad, "| failing:", sorted(sem_bad))

# ---- insertion blocks
idx = [j for j, _ in inserted]
blocks, start = [], None
for k, j in enumerate(idx):
    if start is None:
        start = j
    if k + 1 == len(idx) or idx[k + 1] != j + 1:
        blocks.append((start, j)); start = None
print("inserted blocks:", len(blocks), [(x + 1, y + 1) for x, y in blocks])


def prev_nonblank(k):
    return next(m for m in range(k - 1, -1, -1) if lb[m].strip())


def next_nonblank(k):
    return next((m for m in range(k + 1, len(lb)) if lb[m].strip()), None)


BANNER_HEADS = ["## A. Empirical Anchors and the Mass Table", "## B. K₇ Combinatorial Structure and ε-per-Edge",
                "## D. Magnetism, Heavy Elements, and the Iron-Block Boundary",
                "## E. Cayley-Dickson Tower and Hexagonal Vacuum", "## F. Borromean Confinement (Conjecture 1)",
                "## H. Angle as Stored Energy and K₇ Angular Tax",
                "## I. Five-Seam Transfer Coefficient and Physical Scale Ladders", "## N. Continuum-Limit Fidelity",
                "## O. Conjectural Re-Readings", "# PART IV — TIER 4: CONJECTURES AWAITING MECHANISM",
                "# PART V — BANKED R3 / EXPLORATION-MODE"]
found = {}
other = []
for blk in blocks:
    nb = [k for k in range(blk[0], blk[1] + 1) if lb[k].strip()]
    if not nb:
        other.append(blk); continue
    first = lb[nb[0]]
    before = lb[prev_nonblank(nb[0])]
    after_k = next_nonblank(nb[-1])
    after = None if after_k is None else lb[after_k]
    gap_b, gap_a = nb[0] - prev_nonblank(nb[0]), (None if after_k is None else after_k - nb[-1])
    if first.startswith("**V4.97 fold-in record (October 8, 2026):**") and len(nb) == 1:
        found["record"] = before.startswith("**Status:** ") is False and after.startswith(
            "**V4.96 fold-in record (October 7, 2026):**") and gap_a == 2
    elif first.startswith("*[→ V4.97 (§2.97): ") and len(nb) == 1 and first.endswith(". Nothing below is rewritten.]*"):
        found.setdefault("banners", []).append((before, gap_b, gap_a))
    elif first == "### §2.97 — Closing the Substrate Program (V4.97)":
        got = "\n".join(lb[nb[0]:nb[-1] + 1])
        want = draft[draft.index("### §2.97 — Closing the Substrate Program (V4.97)"):].rstrip("\n")
        want = want.replace("October [DATE], 2026", "October 8, 2026", 1)
        want = want.replace(" [AUTHOR: or keep it as a frozen historical row, outside the closure.]", "", 1)
        found["s297"] = (got == want and before.startswith("**Registers and non-claims.** The election is the author's")
                         and after == "## J. Multi-Lens Reference and Phase Incommensurability" and gap_b == 2 and gap_a == 2)
    elif first.startswith("| **Substrate program — CLOSED (V4.97)**") and len(nb) == 2:
        found["rows"] = (lb[nb[1]].startswith("| **Successor program — NOT OPENED (conditions §2.97.D)** |")
                         and before.startswith("| **Lattice-spacing bound** (§2.95") and gap_b == 1 and gap_a == 1
                         and after.startswith("| **G-C1 gate**") and "§2.52 Open 3 is listed here as closed with the program"
                         in first)
    elif first == "## Successor intake (not opened) (added V4.97)":
        body = [lb[k] for k in nb]
        found["intake"] = (len(body) == 9 and body[2] == "| Item | Where it is recorded | Status of record |"
                           and body[4].startswith("| **G-RCX1**, re-scoped") and body[5].startswith("| **§3.4-G2-knot**")
                           and body[6].startswith("| **§3.4-G2-CHIRAL**") and body[7].startswith("| **§2.84 Part C**")
                           and body[8].startswith("| **G-QUANTA's discriminator**")
                           and before.startswith("| **ζ-tax gate 4**")
                           and after == "## Closed / dropped (carried forward for audit reference)" and gap_a == 2)
    elif first.startswith("*V4.97 (October 8, 2026): additions only") and len(nb) == 1:
        found["changelog"] = before.startswith("*V4.96 (October 7, 2026): additions only") and gap_b == 1 and after is None
    else:
        other.append(blk)
bans = found.get("banners", [])
ban_ok = (sorted(x[0] for x in bans) == sorted(BANNER_HEADS) and all(g1 == 2 and g2 == 2 for _, g1, g2 in bans))
place_ok = (not other and found.get("record") and found.get("s297") and found.get("rows") and found.get("intake")
            and found.get("changelog") and ban_ok)
print("record:", found.get("record"), "| §2.97 = approved draft + its two fill-ins:", found.get("s297"), "| Part VI rows:",
      found.get("rows"), "| intake block:", found.get("intake"), "| changelog:", found.get("changelog"),
      "| banners under the 11 headings:", ban_ok, "| unexplained blocks:", other)
heads = [x for _, x in inserted if x.startswith("#")]
print("inserted headings:", heads)

# ---- untouched entries
fixed = {"§2.92.A": "**A. Polarization gate (A1) — FALSIFIED", "§2.52 Open 3 row": "| **§2.52 Open 3**",
         "§2.52 body (Open 3)": "**Open 3: Pulsation = ζ from §3.4.**", "§2.52 heading": "### §2.52 84-Gap Decomposition",
         "G-POLY1 row": "| **Gate G-POLY1**", "§3.4-G2-CHIRAL row": "| §3.4-G2-CHIRAL", "ζ-tax gate 3 row": "| **ζ-tax gate 3**",
         "floor row": "| **Polycrystal validity floor**", "factor-assignment row": "| **Factor-assignment question**",
         "G-QUANTA row": "| **Gate G-QUANTA**"}
fixed_ok = True
for name, p in fixed.items():
    xa, xb = [x for x in la if x.startswith(p)], [x for x in lb if x.startswith(p)]
    good = len(xa) == 1 and xa == xb
    fixed_ok &= good
    print(name, "unchanged:", good)
n_ptr = b.count("[→ V4.97 (§2.97): ")
n_ins = sum(x.count("[→ V4.97 (§2.97): ") for _, x in inserted)
print("'[→ V4.97 (§2.97): ' occurrences:", n_ptr, "(expected 57 = 46 appends + 11 banners); inside inserted text:", n_ins,
      "(expected 11, the banners)")
ok &= (n_title == 1 and n_asof == 1 and n_status == 1 and not missing and not extra and not bad_key and not sem_bad
       and place_ok and fixed_ok and n_ptr == 57 and n_ins == 11
       and heads == ["### §2.97 — Closing the Substrate Program (V4.97)", "## Successor intake (not opened) (added V4.97)"]
       and a.count("V4.97") == 0 and equal_lines + n_title + n_asof + n_status + len(appends) == len(la))
print("ADDITIVITY CHECK:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
