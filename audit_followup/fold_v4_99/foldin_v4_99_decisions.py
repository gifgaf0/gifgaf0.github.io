#!/usr/bin/env python3
"""foldin_v4_99_decisions.py — fold V4.99: §2.99, the author's close-out decisions (directive of October 8, 2026).

One correction of mathematical fact (§2.22's count of imaginary units) and the classifications the close-out left to the
author: OP-C7-1 and OP-2.77-FB under §2.97.C(b), mathematics only, open; §4.14 under §2.97.C(a). It also records the
elections the author confirmed (F7; no banners on the mixed clusters) and the ledger's move into the repository.
The fact is checked by v499_checks.py (one leg; no verdict depends on it).

Base: SQT_Master_Ledger_v4_98_CANONICAL.md (md5 5c50db11…, 1,908,920 B; produced by foldin_v4_98_mathematics.py).
Edits (all additive): E1 title; E2 As-of prepend; E3 the V4.99 fold-in record (before the V4.98 record); E5 §2.99 (after
§2.98, before Cluster J); E6 four in-line "[→ V4.99 (§2.99): …]" pointers; E8 one changelog line.
Anchors are read from the file and asserted unique; every fragment lands exactly once; the reverse splice must
reconstruct V4.98 byte-identically.
"""
import argparse
import hashlib

ap = argparse.ArgumentParser()
ap.add_argument("--head", required=True)
ap.add_argument("--ls-remote", required=True)
ap.add_argument("--main", required=True)
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

SRC = "/home/claude/fold/SQT_Master_Ledger_v4_98_CANONICAL.md"
OUT = ("/home/claude/fold/SQT_Master_Ledger_v4_99_DRYRUN_NOT_CANONICAL.md" if args.dry_run
       else "/home/claude/fold/SQT_Master_Ledger_v4_99_CANONICAL.md")
V498, V498_BYTES = "5c50db1147527b25c87b5962b5e955ed", 1908920
DATE = "October 8, 2026"

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V498, "base V4.98 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V498_BYTES
assert "§2.99" not in s and "V4.99" not in s
L = s.split("\n")
assert len(L) == 4902 and L[-1] == "", "line structure changed — re-anchor"


def one_line(prefix):
    hits = [x for x in L if x.startswith(prefix)]
    assert len(hits) == 1, f"anchor not unique: {prefix!r} ({len(hits)})"
    assert s.count("\n" + hits[0] + "\n") == 1
    return hits[0]


T_OLD, T_NEW = "# SQT Master Ledger — V4.98 Canonical\n", "# SQT Master Ledger — V4.99 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD
A_OLD = "**As of:** October 8, 2026 (V4.98 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = (f"**As of:** {DATE} (V4.99 fold — **the author's close-out decisions (§2.99): §2.22's imaginary-unit counts "
         "corrected to 0, 1, 3, 7 and 15; OP-C7-1 and OP-2.77-FB classified as mathematics, staying open; §4.14 closed "
         "with the program; the canonical ledger now kept in the repository. No verdict or register changes; nothing "
         "published or sent.** V4.98 fold (October 8, 2026) — ")

P = "[→ V4.99 (§2.99): "
BR = [
    ("**Construction (R2).** The p6m planar lattice admits a series of quotients indexed by Cayley-Dickson imaginary count",
     P + "the counts are off. ℝ, ℂ, ℍ, 𝕆 and 𝕊 have 0, 1, 3, 7 and 15 imaginary units, since an algebra of dimension 2ⁿ "
         "has 2ⁿ − 1 (for ℍ, 𝕆 and 𝕊 that is 3, 7 and 15, as at §2.53). The numbers 1, 2, 4, 8 and 16 are the "
         "dimensions. Their sum, 31 = 2⁵ − 1, is five real units and 26 imaginaries, not 30 imaginaries plus 1 real. The "
         "entry's substrate reading is closed with the program (§2.97); this note corrects only the count.]"),
    ("*[→ V4.97 (§2.97): the substrate program is closed. The conjectures below that await a physical mechanism close "
     "with it",
     P + "§4.14 (the Doc-3 intake audit), which §2.97.C(a) does not name, closes with them as well: the author's "
         "classification of October 8, 2026.]"),
    ("**Status.** Nothing promoted to §2.x. Items 1–2 → Tier-4 holding-pen (R3)",
     P + "closed with the substrate program under §2.97.C(a), on the author's classification of October 8, 2026. The "
         "items stay as filed.]"),
    ("**V4.97 fold-in record (October 8, 2026):**",
     P + "the two rows left to the author under C(h), OP-C7-1 and OP-2.77-FB, are classified C(b): mathematics only, "
         "staying open (the author, October 8, 2026). Like the other mathematics rows, they carry no pointer.]"),
]
EDITS = []
for prefix, text in BR:
    old = one_line(prefix)
    assert "[→ V4.99" not in old and "\n" not in text and text.endswith("]") and "|" not in text
    assert not old.endswith(" |")                      # all four hosts are paragraph lines
    EDITS.append((old, old + " " + text))
assert len({o for o, _ in EDITS}) == len(EDITS) == 4

J_ANCH = "## J. Multi-Lens Reference and Phase Incommensurability\n"
REG98 = one_line("**Registers and non-claims.** Annotations only: R1 facts, one leg each.")
assert s.count(REG98 + "\n\n" + J_ANCH) == 1
S299 = [
    "### §2.99 — The Author's Close-Out Decisions (V4.99)",
    f"*(Folded V4.99, {DATE}, on the author's directive of 08:43 PDT (\"Finalize Close-Out (V4.99)\"; "
    "`FOLD_AUTHORIZATION_V4_99.md`). It records one correction of mathematical fact and the decisions the close-out "
    "left to the author. The affected entries carry [→ V4.99 (§2.99)] pointers. The fact was checked once "
    "(`fold_v4_99/v499_checks.py`); no verdict rests on it, so there is no second leg.)*",
    "**In plain language.** The author settled what the close-out left open. §2.22's count of imaginary units is "
    "corrected, the three items left unclassified are classified, and the ledger now lives in the repository.",
    "1. **§2.22, the imaginary units.** ℝ, ℂ, ℍ, 𝕆 and 𝕊 have 0, 1, 3, 7 and 15 imaginary units, not 1, 2, 4, 8 and "
    "16; for ℍ, 𝕆 and 𝕊 this is the §2.53 correction of V4.98. The numbers 1, 2, 4, 8 and 16 are the dimensions, and "
    "their sum 31 = 2⁵ − 1 is five real units and 26 imaginaries.\n"
    "2. **The two rows left under §2.97.C(h).** OP-C7-1 and OP-2.77-FB are classified C(b): mathematics only, staying "
    "open. As mathematics rows they carry no pointer; the V4.97 record carries the classification.\n"
    "3. **§4.14, the Doc-3 intake audit.** Classified C(a): it closes with the substrate program. Its Status line and "
    "the Part IV banner carry pointers.\n"
    "4. **Elections confirmed.** F7: §2.97.C(f) stands as folded, with the §2.52 Open 3 row untouched and listed as "
    "closed with the program. The mixed clusters C, G, J and K get no banner; their row-level pointers suffice.\n"
    "5. **Where the ledger lives.** The canonical ledger is now kept in the repository. V4.98 was committed at the root "
    "on branch `claude/audit-followup-oct6` (`5d9577c`), replacing `FOLD_LEDGER_2026-06-18.md`, the in-repository "
    "stand-in since June 18, whose entries this ledger records (the V4.40–V4.42 records and the Preamble's "
    "literature-first rule). This reverses the June 18 rule and the author's September 23 election that removed the "
    "V4.79 canonical from the root (PR #28). The project store's copy (V4.96) was deleted on the author's "
    "authorization; the store keeps STATUS.md and the phase reports.",
    "**Registers and non-claims.** One R1 fact, one leg; three classifications and two elections, recorded as the "
    "author made them. No verdict or register changes; the mathematics keeps its registers; nothing is published, "
    "deposited or sent; no successor is opened.",
]
S299_TXT = "\n\n".join(S299) + "\n\n"

R_ANCH = "**V4.98 fold-in record (October 8, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = (f"**V4.99 fold-in record ({DATE}):** CLOSE-OUT DECISIONS — §2.99 and {len(EDITS)} in-line [→ V4.99] pointers, "
          "on the author's directive of October 8, 2026, 08:43 PDT (\"Finalize Close-Out (V4.99)\"; "
          "`FOLD_AUTHORIZATION_V4_99.md`): §2.22's imaginary-unit counts corrected to 0, 1, 3, 7 and 15; OP-C7-1 and "
          "OP-2.77-FB classified C(b), mathematics, open; §4.14 classified C(a), with pointers on its Status line and "
          "the Part IV banner; F7 and the unbannered mixed clusters confirmed. The fact is checked by `v499_checks.py` "
          "(one leg). No verdict, register or row changes; nothing published or sent. Estate: the canonical ledger now "
          "lives in the repository root (V4.98 committed at `5d9577c`, replacing `FOLD_LEDGER_2026-06-18.md`); the "
          "project store's V4.96 copy deleted October 8, 08:48 PDT; branch `claude/audit-followup-oct6` (head at fold "
          f"`{args.head}`); `git ls-remote` {args.ls_remote}: main = `{args.main}`. No §3.x; no observable bridge.\n\n")

LINE_CH98 = one_line("*V4.98 (October 8, 2026): additions only")
assert L[4900] == LINE_CH98 and L[4901] == ""
CH_NEW = (f"*V4.99 ({DATE}): additions only — title/As-of header bump; the V4.99 fold-in record; §2.99 (the author's "
          f"close-out decisions) after §2.98; {len(EDITS)} in-line [→ V4.99] pointers; reverse-splice byte-identical to "
          "V4.98 (`5c50db11`); the §2.52 Open 3 row untouched.*")


def build():
    frags = [T_NEW, A_NEW, RECORD, S299_TXT, CH_NEW] + [n for _, n in EDITS]
    for fr in [A_NEW, RECORD, S299_TXT, CH_NEW]:
        assert s.count(fr) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    for old, new in EDITS:
        assert out.count("\n" + old + "\n") == 1
        out = out.replace("\n" + old + "\n", "\n" + new + "\n", 1)
    out = out.replace(REG98 + "\n\n" + J_ANCH, REG98 + "\n\n" + S299_TXT + J_ANCH, 1)
    out = out.replace("\n" + LINE_CH98 + "\n", "\n" + LINE_CH98 + "\n" + CH_NEW + "\n", 1)
    for fr in frags:
        assert out.count(fr) == 1, f"fragment count != 1: {fr[:60]!r}"
    assert out.count(P) == len(EDITS)
    rev = out.replace("\n" + LINE_CH98 + "\n" + CH_NEW + "\n", "\n" + LINE_CH98 + "\n", 1)
    rev = rev.replace(REG98 + "\n\n" + S299_TXT + J_ANCH, REG98 + "\n\n" + J_ANCH, 1)
    for old, new in EDITS:
        rev = rev.replace("\n" + new + "\n", "\n" + old + "\n", 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V498 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    print(("DRY RUN (not canonical): " if args.dry_run else "V4.99 FOLDED: ") + OUT)
    print("bytes:", len(b), "(V4.98 %d B; delta +%d B); chars delta +%d" % (V498_BYTES, len(b) - V498_BYTES, len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("pointers:", len(EDITS), "| §2.99 chars:", len(S299_TXT), "| record chars:", len(RECORD))
    print("reverse-splice: BYTE-IDENTICAL to V4.98 (%s) — PASS" % V498)
    print("all fragments landed exactly once — PASS")
