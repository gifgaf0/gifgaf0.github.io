#!/usr/bin/env python3
"""foldin_v4_97_closeout.py — fold V4.97: §2.97, closing the substrate program, and the Part VI sweep.

Folds the author's approved §2.97 text (audit_followup/inputs/CLOSING_ENTRY_V4_97_DRAFT.md, md5 10270b68…) after §2.96,
with fill-ins and mechanical fixes only:
  - the HTML review note removed;
  - "October [DATE]" → "October 8";
  - C(f)'s bracketed alternative left out (the F7 default);
  - C(e)'s "move" implemented by reference, because rows are not moved under append-only.
The sweep follows audit_followup/closeout/co1_classification.json (CO-1).

Base: SQT_Master_Ledger_v4_96_CANONICAL.md (md5 120b076a…, 1,877,637 B; produced by foldin_v4_96_floor_election.py).

Edits (all additive):
  E1   title;
  E2   As-of prepend;
  E2b  a V4.97 note at the head of the Status line, inserted after "**Status:** ";
  E3   the V4.97 fold-in record (before the V4.96 record);
  E4   pointers on the Preamble's KC-EP and M.ONT headers and on §2.91.D's kill set;
  E5   §2.97 (after §2.96, before Cluster J);
  E6   43 Part VI row pointers;
  E7   11 banner lines (Part II clusters A, B, D, E, F, H, I, N, O; Parts IV and V);
  E8   two Part VI rows after the lattice-spacing-bound row;
  E9   the Successor intake block before "Closed / dropped";
  E10  one changelog line.
Anchors are read from the file and asserted unique; every fragment lands exactly once; the reverse splice must
reconstruct V4.96 byte-identically.
"""
import argparse
import hashlib
import json

ap = argparse.ArgumentParser()
ap.add_argument("--head", required=True, help="estate head at fold (short sha)")
ap.add_argument("--ls-remote", required=True, help="time of the live git ls-remote")
ap.add_argument("--main", required=True, help="main's short sha from that ls-remote")
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

ROOT = "/home/claude/gifgaf0.github.io/audit_followup"
SRC = "/home/claude/fold/SQT_Master_Ledger_v4_96_CANONICAL.md"
OUT = ("/home/claude/fold/SQT_Master_Ledger_v4_97_DRYRUN_NOT_CANONICAL.md" if args.dry_run
       else "/home/claude/fold/SQT_Master_Ledger_v4_97_CANONICAL.md")
V496, V496_BYTES = "120b076a613b7ef4074193c03df2cf0d", 1877637
DRAFT, DRAFT_MD5 = ROOT + "/inputs/CLOSING_ENTRY_V4_97_DRAFT.md", "10270b68a446f6025331f132f8d48038"
CLS = ROOT + "/closeout/co1_classification.json"
DATE = "October 8, 2026"

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V496, "base V4.96 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V496_BYTES
assert "§2.97" not in s and "V4.97" not in s
L = s.split("\n")
assert len(L) == 4742 and L[-1] == "", "line structure changed — re-anchor"


def one_line(prefix):
    hits = [x for x in L if x.startswith(prefix)]
    assert len(hits) == 1, f"anchor not unique: {prefix!r} ({len(hits)})"
    assert s.count("\n" + hits[0] + "\n") == 1
    return hits[0]


# ---------------------------------------------------------------- E1 title, E2 As-of, E2b Status
T_OLD, T_NEW = "# SQT Master Ledger — V4.96 Canonical\n", "# SQT Master Ledger — V4.97 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD
A_OLD = "**As of:** October 7, 2026 (V4.96 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = (f"**As of:** {DATE} (V4.97 fold — **the substrate program CLOSED (§2.97; the author's decision of October 7, "
         "2026): the vacuum as a Gross–Pitaevskii supersolid, light as its shear wave, matter as knots and textures in it, "
         "and gravity as a property of the medium close on verdicts already on record. The mathematics, the second-sound "
         "paper, the SLWE negative result and the alpha-decay data carry forward, with the organizing idea at R3; no "
         "successor is opened (conditions §2.97.D). A decision record: nothing derived, published or sent.** V4.96 fold "
         "(October 7, 2026) — ")
S_OLD = "**Status:** Mathematical foundation frozen. "
assert s.count(S_OLD) == 1 and L[3].startswith(S_OLD)
S_NEW = (f"**Status:** **V4.97 ({DATE}): the substrate program is CLOSED (§2.97). The physics program described next "
         "closed with it; the mathematics keeps its registers, and no successor is opened (§2.97.D).** Mathematical "
         "foundation frozen. ")

# ---------------------------------------------------------------- pointer texts
P = "[→ V4.97 (§2.97): "
PTXT = {
    "a": P + "closed with the substrate program (§2.97.C(a)).]",
    "a_obd": P + "closed unopened with the substrate program; its only purpose was to select the substrate's vacuum "
                 "(§2.97.C(a)).]",
    "a_mont": P + "closed with the substrate program; M.ONT closes with it (§2.97.B.4, C(a)).]",
    "a_6771c": P + "closed with the substrate program (§2.97.C(a)); the OP-2.67.6 gates stay standing for any "
                   "statistics-from-geometry claim (§2.97.B.4).]",
    "b_6771b": P + "the physical reading closes with the substrate program; the mathematics stays open (§2.97.C(b)).]",
    "b_256a": P + "tagging the physical claims closes with the substrate program; tagging the mathematical values stays "
                  "open (§2.97.C(b)).]",
    "b_256b": P + "the physical-parameter reading closes with the substrate program; the geometric address stays open "
                  "(§2.97.C(b)).]",
    "b_263": P + "the vacuum-fold reading (§2.26) closes with the substrate program; the fold-geometry question stays "
                 "open as mathematics (§2.97.C(b)).]",
    "b_milnor": P + "the physical sign reading closes with the substrate program; the curve computations keep their "
                    "registers (§2.97.C(b)).]",
    "b_273": P + "the physical mapping this gate serves closes with the substrate program; §2.73's algebraic "
                 "decomposition keeps its register (§2.97.C(b)).]",
    "b_274map": P + "the mapping closes with the substrate program; §2.74's algebraic duality keeps its register "
                    "(§2.97.C(b)).]",
    "b_2741b": P + "the physical mapping closes with the substrate program; the YB-orbit structure keeps its register "
                   "(§2.97.C(b)).]",
    "b_eqq": P + "the physical SU(2)-doublet reading closes with the substrate program; the representation theory keeps "
                 "its register (§2.97.C(b)).]",
    "b_e1": P + "the chirality reading closes with the substrate program; the algebra keeps its register (§2.97.C(b)).]",
    "b_dict": P + "the substrate and particle mapping closes with the program; the algebraic identifications keep their "
                  "registers (§2.97.C(b)).]",
    "b_a2": P + "the ejection-mechanism reading closes with the substrate program; the count structure keeps its "
                "register, and the alpha-decay data stand (§2.97.B.2, C(b)).]",
    "b_rung": P + "the electron-anchor placement closes with the substrate program; reconciling the numberings stays "
                  "open (§2.97.C(b)).]",
    "e": P + "listed in Part VI's Successor intake (not opened); not closed (§2.97.C(e)).]",
    "e_rcx": P + "listed in Part VI's Successor intake (not opened), re-scoped there to what protects a knotted or "
                 "linked configuration in a relativistic field; not closed (§2.97.C(e)).]",
}
cls = json.load(open(CLS, encoding="utf-8"))
assert cls["base_md5"] == V496
EDITS = []
for r in cls["rows"]:
    if not r["pointer"]:
        continue
    old = L[r["line"] - 1]
    assert old.startswith("| ") and old.endswith(" |") and "[→ V4.97" not in old, r["line"]
    t = PTXT[r["pointer"]]
    assert "|" not in t and t.endswith("]")
    EDITS.append((old, old[:-2] + " " + t + " |"))
N_ROW = len(EDITS)
assert N_ROW == 43

# ---------------------------------------------------------------- E4 Preamble and §2.91.D
PRE = [
    ("### KC-EP — The Equivalence-Principle Kill Condition (standing; V4.92)",
     P + "standing for any successor that proposes a medium or a gravity mechanism (§2.97.B.4).]"),
    ("### The Particle-Ontology Declaration Flag (M.ONT)",
     P + "closed with the substrate program (§2.97.B.4).]"),
    ("**D. The kill set as amended (Amendment 1, author-authorized July 14);",
     P + "KC1–KC3 and KC-EP stay standing for any successor that proposes a medium or a gravity mechanism "
         "(§2.97.B.4).]"),
]
for prefix, t in PRE:
    old = one_line(prefix)
    assert not old.endswith(" |") and "[→ V4.97" not in old
    EDITS.append((old, old + " " + t))
assert len({o for o, _ in EDITS}) == len(EDITS) == 46, "two pointers on one line"

# ---------------------------------------------------------------- E7 banners
def GEN(x):
    return (f"the substrate program is closed, and Cluster {x}'s physics closes with it (§2.97.C(a)); its mathematics "
            "keeps its registers (§2.97.B.1)")
END = ". Nothing below is rewritten.]*"
BAN = [
    ("## A. Empirical Anchors and the Mass Table", GEN("A") + ", and the alpha-decay data stand (§2.97.B.2)"),
    ("## B. K₇ Combinatorial Structure and ε-per-Edge", GEN("B")),
    ("## D. Magnetism, Heavy Elements, and the Iron-Block Boundary", GEN("D")),
    ("## E. Cayley-Dickson Tower and Hexagonal Vacuum", GEN("E")),
    ("## F. Borromean Confinement (Conjecture 1)", GEN("F")),
    ("## H. Angle as Stored Energy and K₇ Angular Tax", GEN("H")),
    ("## I. Five-Seam Transfer Coefficient and Physical Scale Ladders",
     GEN("I") + "; §2.93.B0 (the second-sound paper) and §2.94.C1 (the SLWE negative result) stand on their own "
           "(§2.97.B.2)"),
    ("## N. Continuum-Limit Fidelity",
     GEN("N") + "; §2.69.4 and §2.69.5, filed under this heading, are crypto and outside the closure (§2.97.C(c))"),
    ("## O. Conjectural Re-Readings", GEN("O") + "; OP-2.63's geometric question stays open (§2.97.C(b))"),
    ("# PART IV — TIER 4: CONJECTURES AWAITING MECHANISM",
     "the substrate program is closed. The conjectures below that await a physical mechanism close with it "
     "(§2.97.C(a): §4.7, §4.10, §4.11–§4.13, §4.15)"),
    ("# PART V — BANKED R3 / EXPLORATION-MODE",
     "Part V is archived as it stands (§2.97.C(g)). Its physics R3 items can be promoted only through a successor's "
     "gates; its R1 mathematical items, such as the odd-power rung theorem (§A) and the OP-PSL.3 finiteness "
     "obstruction, remain mathematics"),
]
BANNERS = []
for head, body in BAN:
    assert s.count("\n" + head + "\n\n") == 1 and L.count(head) == 1
    i = L.index(head)
    assert L[i + 1] == "" and L[i + 2].strip(), head
    line = "*" + P + body + END
    BANNERS.append((head, line))
assert len(BANNERS) == 11

# ---------------------------------------------------------------- E5 §2.97 from the approved draft
d = open(DRAFT, encoding="utf-8").read()
assert hashlib.md5(d.encode("utf-8")).hexdigest() == DRAFT_MD5
k = d.index("### §2.97 — Closing the Substrate Program (V4.97)")
assert d[:k].lstrip().startswith("<!--") and d[:k].rstrip().endswith("-->")      # the review note: removed
body = d[k:].rstrip("\n")
FILL = [("October [DATE], 2026", "October 8, 2026"),
        (" [AUTHOR: or keep it as a frozen historical row, outside the closure.]", "")]
for a, b in FILL:
    assert body.count(a) == 1, a
    body = body.replace(a, b, 1)
for bad in ("[DATE]", "[AUTHOR", "<!--", "-->"):
    assert bad not in body
S297_TXT = body + "\n\n"
J_ANCH = "## J. Multi-Lens Reference and Phase Incommensurability\n"
REG96 = one_line("**Registers and non-claims.** The election is the author's (T3-immutable)")
assert s.count(REG96 + "\n\n" + J_ANCH) == 1

# ---------------------------------------------------------------- E8 two Part VI rows
LB = one_line("| **Lattice-spacing bound** (§2.95")
ROWS = [
    "| **Substrate program — CLOSED (V4.97)** (§2.97: the vacuum as a Gross–Pitaevskii supersolid, single- and "
    "16-component; light as its transverse shear wave; matter as knots and textures in it; gravity as a property of the "
    f"medium) | **CLOSED (V4.97, {DATE})** — on the author's decision of October 7, 2026; a decision record, nothing "
    "newly derived; each pillar's verdict was already on record (§2.97.A). Open substrate-physics rows close with it and "
    "carry [→ V4.97] pointers (C(a)); where a row joins mathematics to a physical reading, the reading closes and the "
    "mathematics stays open (C(b)); crypto rows are outside the closure (C(c)); author actions stay open until done "
    "(C(d)); the C(e) items wait in the Successor intake block below; **§2.52 Open 3 is listed here as closed with the "
    "program, its row's text untouched (C(f))**; Part V is archived as it stands (C(g)); two rows are left to the author "
    "(C(h): OP-C7-1, OP-2.77-FB). The organizing idea carries forward at R3 (§2.97.B.3). |",
    "| **Successor program — NOT OPENED (conditions §2.97.D)** | **NOT OPENED** — §2.97 records the conditions and "
    "opens nothing: a new file with its own gates; a prior-address survey as its first entry; Lorentz invariance by "
    "construction, not by tuning; dimensionless outputs, with each configuration's particle declared before computing; "
    "energy accounting, conserved labels and KC-EP respected; a pre-registered first claim compared without fitting. |",
]

# ---------------------------------------------------------------- E9 the Successor intake block
CD_ANCH = "\n\n## Closed / dropped (carried forward for audit reference)\n"
assert s.count(CD_ANCH) == 1
INTAKE = "\n".join([
    "## Successor intake (not opened) (added V4.97)",
    "",
    "*(§2.97.C(e). Listed by reference: each item stays where it is recorded, and no row's text is changed "
    "(append-only). Nothing here is opened; a successor must first meet §2.97.D.)*",
    "",
    "| Item | Where it is recorded | Status of record |",
    "|---|---|---|",
    "| **G-RCX1**, re-scoped from \"what protects Borromean linking in this vacuum\" to \"what protects a knotted or "
    "linked configuration in a relativistic field\"; the answer class already on record is a conserved topological "
    "charge (§2.84 Part C, Q = L) | Part VI, High-priority structural gates (registered by §2.92.C) | REGISTERED, "
    "unopened |",
    "| **§3.4-G2-knot** (whether a Faddeev–Hopf field soliton realizes a Borromean three-strand) | Part VI, "
    "Lower-priority items | Open |",
    "| **§3.4-G2-CHIRAL** | Part VI, Lower-priority items | Its row records ✓ CLOSED (V4.32, §3.09) |",
    "| **§2.84 Part C** (Faddeev–Hopf stabilization, Q = L; R1, generic) | Part II, §2.84 (Cluster L); a section, not a "
    "Part VI row | R1, standard and Hopfion-generic (SUPPORTING) |",
    "| **G-QUANTA's discriminator** (§2.91.P, R2, with its Derrick and Vakulenko–Kapitanskii prior art) | Part VI, "
    "High-priority structural gates (Gate G-QUANTA) | Its row records CLOSED (V4.82) |",
]) + "\n\n"
INTAKE_INS = "\n\n" + INTAKE + "## Closed / dropped (carried forward for audit reference)\n"

# ---------------------------------------------------------------- E3 fold-in record
R_ANCH = "**V4.96 fold-in record (October 7, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = (
    f"**V4.97 fold-in record ({DATE}):** SUBSTRATE PROGRAM CLOSED — §2.97 folded from the author's approved text "
    f"(`audit_followup/inputs/CLOSING_ENTRY_V4_97_DRAFT.md`, md5 `10270b68`) on the close-out brief (October 7, 2026, "
    "22:19 PDT) and the author's facts (October 8, 2026, 07:09 PDT); `FOLD_AUTHORIZATION_V4_97.md`. Only fill-ins and "
    "mechanical fixes were made: the review note removed, the date entered, C(f)'s bracketed alternative left out (the F7 "
    "default), and C(e)'s \"move\" made by reference, as a Part VI \"Successor intake (not opened)\" block, since rows "
    "are not moved under append-only. The sweep classified every Part VI row whose status reads Open, Registered, "
    "Standing or Partially executed (94 of 163; `closeout/CO1_CLASSIFICATION.md`). It added "
    f"{N_ROW} row pointers: 27 closed with the program (C(a)), 14 split (C(b)) and 2 sent to the intake (C(e)). There "
    "are none on mathematics, crypto or author-action rows, or on rows already closed. Two rows are left to the author "
    "under C(h): OP-C7-1 and OP-2.77-FB. Also added: pointers on the Preamble's KC-EP header (standing), its M.ONT header "
    "(closed) and §2.91.D's kill set (standing); banner lines at the heads of Part II clusters A, B, D, E, F, H, I, N and "
    "O and of Parts IV and V (clusters C, G, J and K are mixed, L is mathematics and M is crypto, so they have no "
    "banner); two Part VI rows (Substrate program — CLOSED; Successor program — NOT OPENED) after the "
    "lattice-spacing-bound row; and a V4.97 note at the head of the Status line. Fold notes, reported to the author, "
    "with §2.97's text folded as approved: (1) C(e) names §3.4-G2-CHIRAL as Faddeev–Hopf soliton work, but it is "
    "curve-level Milnor-invariant work, and its row records ✓ CLOSED (V4.32, §3.09). The Faddeev–Hopf rows are "
    "§3.4-G2-orient (closed, R1) and §3.4-G2-knot (open). G-QUANTA's row is CLOSED (V4.82), and §2.84 Part C is a "
    "section, not a row; both are listed in the intake by reference. (2) C(a) names G-POLY1, whose row records CLOSED: "
    "GATE COMPLETE (V4.76), so it carries no pointer. G-ζ1, G-κ1, G-IIB-L1, G-CC-ε1 and the M.ONT gate had already "
    "executed or been declared; they carry pointers because their status still reads Open or Registered. (3) B.2 "
    "writes \"(§2.93.B4, R2)\", but §2.93.B4 records the alpha-decay data at R1 and the Z = 88 observation at R2. No "
    "number was derived and no register changed; nothing was published, deposited or sent; the §2.52 Open 3 row is "
    "untouched. Estate: `audit_followup/` on branch `claude/audit-followup-oct6` (head at fold "
    f"`{args.head}`); `git ls-remote` {args.ls_remote}: main = `{args.main}`. No §3.x; no observable bridge.\n\n")

# ---------------------------------------------------------------- E10 changelog
LINE_CH96 = one_line("*V4.96 (October 7, 2026): additions only")
assert L[4740] == LINE_CH96 and L[4741] == ""
CH_NEW = (f"*V4.97 ({DATE}): additions only — title/As-of header bump; a V4.97 note at the head of the Status line; "
          "the V4.97 fold-in record; §2.97 (closing the substrate program) after §2.96; "
          f"{len(EDITS)} in-line [→ V4.97] pointers ({N_ROW} Part VI rows, the KC-EP and M.ONT headers, §2.91.D); "
          f"{len(BANNERS)} banner lines (Part II clusters A, B, D, E, F, H, I, N, O; Parts IV and V); two Part VI rows "
          "after the lattice-spacing-bound row; the Successor intake block before Closed / dropped; reverse-splice "
          "byte-identical to V4.96 (`120b076a`); the §2.52 Open 3 row untouched.*")


def build():
    frags = [T_NEW, A_NEW, S_NEW, RECORD, S297_TXT, INTAKE, CH_NEW] + [n for _, n in EDITS] + [b for _, b in BANNERS] + ROWS
    for fr in [A_NEW, S_NEW, RECORD, S297_TXT, INTAKE, CH_NEW] + ROWS + [b for _, b in BANNERS]:
        assert s.count(fr) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(S_OLD, S_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    for old, new in EDITS:
        assert out.count("\n" + old + "\n") == 1
        out = out.replace("\n" + old + "\n", "\n" + new + "\n", 1)
    for head, ban in BANNERS:
        assert out.count("\n" + head + "\n\n") == 1
        out = out.replace("\n" + head + "\n\n", "\n" + head + "\n\n" + ban + "\n\n", 1)
    out = out.replace(REG96 + "\n\n" + J_ANCH, REG96 + "\n\n" + S297_TXT + J_ANCH, 1)
    assert out.count("\n" + LB + "\n") == 1                                      # the bound row carries no pointer
    out = out.replace("\n" + LB + "\n", "\n" + LB + "\n" + "\n".join(ROWS) + "\n", 1)
    out = out.replace(CD_ANCH, INTAKE_INS, 1)
    out = out.replace("\n" + LINE_CH96 + "\n", "\n" + LINE_CH96 + "\n" + CH_NEW + "\n", 1)
    for fr in frags:
        assert out.count(fr) == 1, f"fragment count != 1: {fr[:60]!r}"
    assert out.count(P) == len(EDITS) + len(BANNERS)
    # reverse splice
    rev = out.replace("\n" + LINE_CH96 + "\n" + CH_NEW + "\n", "\n" + LINE_CH96 + "\n", 1)
    rev = rev.replace(INTAKE_INS, CD_ANCH, 1)
    rev = rev.replace("\n" + LB + "\n" + "\n".join(ROWS) + "\n", "\n" + LB + "\n", 1)
    rev = rev.replace(REG96 + "\n\n" + S297_TXT + J_ANCH, REG96 + "\n\n" + J_ANCH, 1)
    for head, ban in BANNERS:
        rev = rev.replace("\n" + head + "\n\n" + ban + "\n\n", "\n" + head + "\n\n", 1)
    for old, new in EDITS:
        rev = rev.replace("\n" + new + "\n", "\n" + old + "\n", 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(S_NEW, S_OLD, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V496 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    print(("DRY RUN (not canonical): " if args.dry_run else "V4.97 FOLDED: ") + OUT)
    print("bytes:", len(b), "(V4.96 %d B; delta +%d B); chars delta +%d" % (V496_BYTES, len(b) - V496_BYTES, len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("in-line pointers:", len(EDITS), f"({N_ROW} rows + 3 Preamble/§2.91.D) | banners:", len(BANNERS),
          "| §2.97 chars:", len(S297_TXT), "| record chars:", len(RECORD))
    print("reverse-splice: BYTE-IDENTICAL to V4.96 (%s) — PASS" % V496)
    print("all fragments landed exactly once — PASS")
