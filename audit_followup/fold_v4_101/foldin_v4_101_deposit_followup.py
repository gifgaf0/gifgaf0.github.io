#!/usr/bin/env python3
"""foldin_v4_101_deposit_followup.py — fold V4.101: §2.101, two things the author did on Zenodo after V4.100 was folded.
STAGED: run with --dry-run until the author gives the fold word.

(1) The SLWE note's revision deposited as version 2 (doi:10.5281/zenodo.23352161), which completes the citation in
Fluid Lattice Topology's notice; (2) the gauge paper's Zenodo description replaced by the v6.4 abstract. Facts from
DataCite (and Zenodo where readable) at staging and fold time; nothing is computed.

Base: SQT_Master_Ledger_v4_100_CANONICAL.md at the repository root (md5 35a20a1f…, 1,923,114 B). Edits (all additive):
title; As-of prepend; the V4.101 fold-in record (before the V4.100 record); §2.101 (after §2.100, before Cluster J);
four in-line "[→ V4.101 (§2.101): …]" pointers (§2.100 items 3, 5 and 6; the Phase C row, inside its last cell); one
changelog line. Anchors are read from the file and asserted unique; every fragment lands exactly once; the reverse
splice must reconstruct V4.100 byte-identically.
"""
import argparse
import hashlib
import os

ap = argparse.ArgumentParser()
ap.add_argument("--word", required=True, help="the author's fold word, verbatim")
ap.add_argument("--when", required=True, help="time of the word, e.g. '15:05 PDT'")
ap.add_argument("--date", required=True, help="fold date, e.g. 'October 13, 2026'")
ap.add_argument("--head", required=True, help="estate head (branch commit) at fold time")
ap.add_argument("--ls-remote", required=True, help="UTC time of the live git ls-remote")
ap.add_argument("--main", required=True, help="main's sha from that ls-remote")
ap.add_argument("--file-check", required=True,
                help="what was read about the note's file at fold time, e.g. "
                     "'Zenodo lists one file, slwe_negative_result_v2.pdf, md5 31284174…' or 'not readable at fold time'")
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "SQT_Master_Ledger_v4_100_CANONICAL.md"))
OUT = ("/home/claude/fold/SQT_Master_Ledger_v4_101_DRYRUN_NOT_CANONICAL.md" if args.dry_run
       else "/home/claude/fold/SQT_Master_Ledger_v4_101_CANONICAL.md")
V4100 = "35a20a1f2db1ad66663b4cd60b7c8234"
DATE = args.date

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V4100, "base V4.100 md5 mismatch — halt"
BASE_BYTES = len(s.encode("utf-8"))
assert "§2.101" not in s and "V4.101" not in s
L = s.split("\n")
assert len(L) == 4937 and L[-1] == "", "line structure changed — re-anchor"


def one_line(prefix):
    hits = [x for x in L if x.startswith(prefix)]
    assert len(hits) == 1, f"anchor not unique: {prefix!r} ({len(hits)})"
    assert s.count("\n" + hits[0] + "\n") == 1
    return hits[0]


T_OLD, T_NEW = "# SQT Master Ledger — V4.100 Canonical\n", "# SQT Master Ledger — V4.101 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD
A_OLD = "**As of:** October 13, 2026 (V4.100 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = (f"**As of:** {DATE} (V4.101 fold — **the SLWE note's revision deposited (§2.101), so the figures quoted by "
         "Fluid Lattice Topology's notice are on Zenodo; the gauge record's description corrected to the v6.4 "
         "abstract. No verdict or register changes; nothing published or sent from here.** "
         "V4.100 fold (October 13, 2026) — ")

P = "[→ V4.101 (§2.101): "
BR = [  # (host prefix, must-contain on the host, pointer text, is_table_row)
    ("3. **The note.** The author deposited the SLWE negative-result note", "for the author to deposit as version 2",
     P + "deposited as version 2 on October 13, 2026 (doi:10.5281/zenodo.23352161).]", False),
    ("5. **The gauge paper, v6.4.**", "the description is metadata that the author can edit",
     P + "the author replaced the description with the v6.4 abstract on October 13.]", False),
    ("6. **Fluid Lattice Topology, with its notice.**", "which Zenodo does not yet hold",
     P + "the revision is on Zenodo since October 13 (doi:10.5281/zenodo.23352161).]", False),
    ("| **Phase C draft awaiting the author** (the SLWE negative-result note → IACR ePrint;", "for the author to deposit as version 2",
     P + "the revision was deposited as version 2 on October 13, 2026 (doi:10.5281/zenodo.23352161).]", True),
]
EDITS = []
for prefix, must, text, row in BR:
    old = one_line(prefix)
    assert must in old and "[→ V4.101" not in old and "\n" not in text and text.endswith("]") and "|" not in text
    if row:
        assert old.endswith(" |")
        new = old[:-2] + " " + text + " |"
    else:
        assert not old.endswith(" |")
        new = old + " " + text
    EDITS.append((old, new))
assert len({o for o, _ in EDITS}) == len(EDITS) == 4

J_ANCH = "## J. Multi-Lens Reference and Phase Incommensurability\n"
REG100 = one_line("**Registers and non-claims.** One R1 fact, one leg; estate facts as recorded, the deposit facts")
assert s.count(REG100 + "\n\n" + J_ANCH) == 1
S2101 = [
    "### §2.101 — The SLWE Note's Revision Deposited, and the Gauge Record's Description (V4.101)",
    f"*(Folded V4.101, {DATE}, on the author's word of {args.when} (\"{args.word}\"; `FOLD_AUTHORIZATION_V4_101.md`). "
    "It records two things the author did on Zenodo after V4.100 was folded. The affected entries carry "
    "[→ V4.101 (§2.101)] pointers. The facts were read from DataCite, and from Zenodo where it could be read, at "
    "fold time; nothing is computed, so there is no leg.)*",
    "**In plain language.** The revised SLWE note is now on Zenodo, so the notice on *Fluid Lattice Topology* cites a "
    "note that contains the figures it quotes. The gauge paper's Zenodo description now gives the corrected abstract.",
    "1. **The note's revision.** The author deposited it on October 13, 2026, as version 2 of the record whose "
    "all-versions DOI is 10.5281/zenodo.23270248: doi:10.5281/zenodo.23352161, registered 21:52 UTC (DataCite). "
    f"The file: {args.file_check}. With it, the figures that the notice on *Fluid Lattice Topology* quotes (§2.100, "
    "item 6) are on Zenodo. The record's description was pasted from a draft wrapped at fixed width, and as DataCite "
    "harvested it, words run together at the wrap points; "
    "`audit_followup/closeout/step3/3b_slwe_eprint/ZENODO_V2_DESCRIPTION_UNWRAPPED.txt` is the same text unwrapped, "
    "and re-pasting it changes metadata only.\n"
    "2. **The gauge record's description.** By 21:39 UTC on October 13 the author had replaced it with the v6.4 "
    "abstract (DataCite): the rank-4 problem is \"addressed\", and hypercharge assignments are no longer listed among "
    "the results (§2.100, item 5).",
    "**Registers and non-claims.** Estate facts only, as read at fold time. No verdict, register or row status "
    "changes; the deposit and the edit are the author's; nothing is published, deposited or sent from here.",
]
S2101_TXT = "\n\n".join(S2101) + "\n\n"

R_ANCH = "**V4.100 fold-in record (October 13, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = (f"**V4.101 fold-in record ({DATE}):** DEPOSIT FOLLOW-UP — §2.101 and {len(EDITS)} in-line [→ V4.101] "
          f"pointers, on the author's word of {args.when} (\"{args.word}\"; `FOLD_AUTHORIZATION_V4_101.md`): the SLWE "
          "note's revision deposited as version 2 (doi:10.5281/zenodo.23352161), completing the citation in Fluid "
          "Lattice Topology's notice; the gauge record's description replaced by the v6.4 abstract. No verdict, "
          f"register or row changes; nothing published or sent from here. Estate: head at fold `{args.head}`; "
          f"`git ls-remote` {args.ls_remote}: main = `{args.main}`. No §3.x; no observable bridge.\n\n")

LINE_CH100 = one_line("*V4.100 (October 13, 2026): additions only")
assert L[4935] == LINE_CH100 and L[4936] == ""
CH_NEW = (f"*V4.101 ({DATE}): additions only — title/As-of header bump; the V4.101 fold-in record; §2.101 (the SLWE "
          f"note's revision deposited; the gauge record's description) after §2.100; {len(EDITS)} in-line [→ V4.101] "
          "pointers; reverse-splice byte-identical to V4.100 (`35a20a1f`).*")


def build():
    frags = [T_NEW, A_NEW, RECORD, S2101_TXT, CH_NEW] + [n for _, n in EDITS]
    for fr in [A_NEW, RECORD, S2101_TXT, CH_NEW]:
        assert s.count(fr) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    for old, new in EDITS:
        assert out.count("\n" + old + "\n") == 1
        out = out.replace("\n" + old + "\n", "\n" + new + "\n", 1)
    reg_now = REG100
    out = out.replace(reg_now + "\n\n" + J_ANCH, reg_now + "\n\n" + S2101_TXT + J_ANCH, 1)
    out = out.replace("\n" + LINE_CH100 + "\n", "\n" + LINE_CH100 + "\n" + CH_NEW + "\n", 1)
    for fr in frags:
        assert out.count(fr) == 1, f"fragment count != 1: {fr[:60]!r}"
    assert out.count(P) == len(EDITS)
    rev = out.replace("\n" + LINE_CH100 + "\n" + CH_NEW + "\n", "\n" + LINE_CH100 + "\n", 1)
    rev = rev.replace(reg_now + "\n\n" + S2101_TXT + J_ANCH, reg_now + "\n\n" + J_ANCH, 1)
    for old, new in EDITS:
        rev = rev.replace("\n" + new + "\n", "\n" + old + "\n", 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V4100 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    print(("DRY RUN (not canonical): " if args.dry_run else "V4.101 FOLDED: ") + OUT)
    print("bytes:", len(b), "(V4.100 %d B; delta +%d B); chars delta +%d" % (BASE_BYTES, len(b) - BASE_BYTES, len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("pointers:", len(EDITS), "| §2.101 chars:", len(S2101_TXT), "| record chars:", len(RECORD))
    print("reverse-splice: BYTE-IDENTICAL to V4.100 (%s) — PASS" % V4100)
    print("all fragments landed exactly once — PASS")
