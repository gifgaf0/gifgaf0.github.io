#!/usr/bin/env python3
"""foldin_v4_98_mathematics.py — fold V4.98: §2.98, the remaining mathematics (close-out brief, Step 4b).

Annotates the mathematics and crypto items on Phase C's "found, not annotated" list (PHASE_C_REPORT.md, decision 5),
in place, and withdraws the V4.97 record's fold note (3). Physics items on that list are covered by §2.97 and get no
separate note (the brief). Facts checked by v498_checks.py (one leg; no verdict depends on them).

Base: SQT_Master_Ledger_v4_97_CANONICAL.md (md5 a5a07bcd…, 1,903,201 B; produced by foldin_v4_97_closeout.py).
Edits (all additive): E1 title; E2 As-of prepend; E3 the V4.98 fold-in record (before the V4.97 record); E5 §2.98 (after
§2.97, before Cluster J); E6 seven in-line "[→ V4.98 (§2.98): …]" pointers; E8 one changelog line.
Anchors are read from the file and asserted unique; every fragment lands exactly once; the reverse splice must
reconstruct V4.97 byte-identically.
"""
import argparse
import hashlib

ap = argparse.ArgumentParser()
ap.add_argument("--head", required=True)
ap.add_argument("--ls-remote", required=True)
ap.add_argument("--main", required=True)
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

SRC = "/home/claude/fold/SQT_Master_Ledger_v4_97_CANONICAL.md"
OUT = ("/home/claude/fold/SQT_Master_Ledger_v4_98_DRYRUN_NOT_CANONICAL.md" if args.dry_run
       else "/home/claude/fold/SQT_Master_Ledger_v4_98_CANONICAL.md")
V497, V497_BYTES = "a5a07bcd4f8ca13c87f65974d5580f24", 1903201
DATE = "October 8, 2026"

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V497, "base V4.97 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V497_BYTES
assert "§2.98" not in s and "V4.98" not in s
L = s.split("\n")
assert len(L) == 4881 and L[-1] == "", "line structure changed — re-anchor"


def one_line(prefix):
    hits = [x for x in L if x.startswith(prefix)]
    assert len(hits) == 1, f"anchor not unique: {prefix!r} ({len(hits)})"
    assert s.count("\n" + hits[0] + "\n") == 1
    return hits[0]


T_OLD, T_NEW = "# SQT Master Ledger — V4.97 Canonical\n", "# SQT Master Ledger — V4.98 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD
A_OLD = "**As of:** October 8, 2026 (V4.97 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = (f"**As of:** {DATE} (V4.98 fold — **the remaining mathematics annotated (§2.98): six small corrections of fact "
         "from Phase C's \"found, not annotated\" list — §2.76(b)'s sum-15 χ claim, §2.53's imaginaries column, §2.69's "
         "canary, and three mathematical slips inside physics entries closed by §2.97 — and one correction to the V4.97 "
         "record. No verdict or register changes; nothing published or sent.** V4.97 fold (October 8, 2026) — ")

P = "[→ V4.98 (§2.98): "
BR = [
    ("(b) **L1.5 selection is chirality-uniform but TS-orbit-mixed.**",
     P + "false as stated. Of the six sum-15 twosets, (1,14), (2,13) and (4,11) have χ = −1 and (3,12), (5,10) and (6,9) "
         "have χ = +1 (s = 5, 3, 6 and 1, 4, 2), so the selection is not chirality-uniform. The TS_O1/TS_O2 split is the "
         "structure-constant sign of OP-2.74.1c.i (V4.94).]"),
    ("**Principle (R2 — face-inheritance principle).**",
     P + "in the table below the Imaginaries column should read 3, 7 and 15 for ℍ, 𝕆 and 𝕊: an algebra of dimension "
         "2ⁿ has 2ⁿ − 1 imaginary units. The column gives half the dimension.]"),
    ("**Canary threat-model interpretation (R2).**",
     P + "the null was guaranteed in advance. By the prime number theorem for arithmetic progressions, primes are "
         "equidistributed over the 288 reduced residue classes mod 455, and at 256 bits every deviation, Chebyshev's bias "
         "included, is far below what 50,000 samples can resolve. The outcome says nothing about the scheme: modulus-level "
         "unobservability is a theorem, not a finding of this test.]"),
    ("**Position A — tension-carrying filaments",
     P + "a geometric slip. Three edges meeting at 120° form a vertex of the hexagonal (honeycomb) tiling, not of "
         "equilateral triangles, whose corners are 60° with six edges at each vertex (3 × 120° = 6 × 60° = 360°). The two "
         "tilings are dual and share the symmetry group p6m. The physics of this entry is closed with the program "
         "(§2.97).]"),
    ("The top quark's knot assignment carries a tension",
     P + "7₁, the torus knot T(2,7), is also chiral: its Jones polynomial t³ + t⁵ − t⁶ + t⁷ − t⁸ + t⁹ − t¹⁰ is not "
         "symmetric under t → 1/t. So chirality does not separate 7₁ from 8₁. The amphicheiral knots of up to eight "
         "crossings are 4₁, 6₃, 8₃, 8₉, 8₁₂, 8₁₇ and 8₁₈. The physics of this entry is closed with the program (§2.97).]"),
    ("**Conjecture (R3 framing; R2 sub-claims).** Each snap event",
     P + "the sedenions (dimension 16) are not a division algebra: they have zero divisors (the 84 two-term zero "
         "divisors of §2.55). By Hurwitz's theorem the normed division algebras over ℝ have dimensions 1, 2, 4 and 8 "
         "only. The physics of this entry is closed with the program (§2.97).]"),
    ("**V4.97 fold-in record (October 8, 2026):**",
     P + "fold note (3) is withdrawn. §2.93.B4's own disposition reads \"The data and the Z = 88 observation are banked "
         "(R2)\", R2 being the register of its dispositions (§2.93: \"R1 for the arithmetic, R2 for the dispositions\"). "
         "§2.97.B.2's \"(§2.93.B4, R2)\" follows that disposition.]"),
]
EDITS = []
for prefix, text in BR:
    old = one_line(prefix)
    assert "[→ V4.98" not in old and "\n" not in text and text.endswith("]")
    assert not old.endswith(" |")                      # all seven hosts are paragraph lines
    EDITS.append((old, old + " " + text))
assert len({o for o, _ in EDITS}) == len(EDITS) == 7

J_ANCH = "## J. Multi-Lens Reference and Phase Incommensurability\n"
REG97 = one_line("**Registers and non-claims.** This is a decision record.")
assert s.count(REG97 + "\n\n" + J_ANCH) == 1
S298 = [
    "### §2.98 — The Remaining Mathematics after the Close-Out (V4.98)",
    f"*(Folded V4.98, {DATE}, on the close-out brief, Step 4b: the mathematics and crypto items on Phase C's \"found, "
    "not annotated\" list (§2.94; `PHASE_C_REPORT.md`, decision 5), annotated in place. Physics items on that list are "
    "covered by §2.97 and get no separate note. Each fact was checked once (`fold_v4_98/v498_checks.py`); no verdict "
    "rests on them, so there is no second leg. The affected entries carry [→ V4.98 (§2.98)] pointers.)*",
    "**In plain language.** Six small corrections of mathematical fact, and one correction to the previous fold's own "
    "record. None changes a result that the program kept.",
    "1. **§2.76(b), the sum-15 twosets.** \"a + b = 15 picks out χ = −1 exclusively\" is false: (1,14), (2,13) and (4,11) "
    "have χ = −1, and (3,12), (5,10) and (6,9) have χ = +1. This agrees with Phase C's math_A.\n"
    "2. **§2.53, the Imaginaries column.** ℍ, 𝕆 and 𝕊 have 3, 7 and 15 imaginary units, not 2, 4 and 8.\n"
    "3. **§2.69, the canary.** The null result was guaranteed by the prime number theorem for arithmetic progressions, "
    "so it tests nothing about the scheme.\n"
    "4. **C.COSM.4 (§4.15).** 120° trivalent junctions are vertices of the hexagonal tiling, not of equilateral "
    "triangles.\n"
    "5. **§4.7.** 7₁ is also chiral, so chirality does not separate 7₁ from 8₁.\n"
    "6. **C.COSM.2 (§4.12).** The sedenions are not a division algebra.\n"
    "7. **The V4.97 record's fold note (3)** is withdrawn: §2.97.B.2 follows §2.93.B4's own disposition.",
    "Items 4–6 sit in physics entries closed by §2.97; their notes correct only the mathematics. **Not annotated "
    "(physics, covered by §2.97):** G-C1 against §2.64.A, the verify-then-widen couplings, and the cosmogony entries' "
    "falsifiability.",
    "**Registers and non-claims.** Annotations only: R1 facts, one leg each. No verdict, register or open row changes; "
    "the mathematics keeps its registers; nothing is published, deposited or sent.",
]
S298_TXT = "\n\n".join(S298) + "\n\n"

R_ANCH = "**V4.97 fold-in record (October 8, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = (f"**V4.98 fold-in record ({DATE}):** REMAINING MATHEMATICS — §2.98 and {len(EDITS)} in-line [→ V4.98] pointers, "
          "on the close-out brief's Step 4b (\"One fold (V4.98) for the remaining mathematics\"; "
          "`FOLD_AUTHORIZATION_V4_98.md`): the sum-15 χ claim of §2.76(b), the §2.53 imaginaries column, the §2.69 canary, "
          "and the mathematical slips in C.COSM.4, §4.7 and C.COSM.2, from Phase C's \"found, not annotated\" list; plus "
          "the withdrawal of the V4.97 record's fold note (3), whose reading of §2.93.B4 was incomplete. Facts checked "
          "by `v498_checks.py` (one leg). No verdict, register or row changes; nothing published or sent. Estate: "
          f"`audit_followup/` on branch `claude/audit-followup-oct6` (head at fold `{args.head}`); `git ls-remote` "
          f"{args.ls_remote}: main = `{args.main}`. No §3.x; no observable bridge.\n\n")

LINE_CH97 = one_line("*V4.97 (October 8, 2026): additions only")
assert L[4879] == LINE_CH97 and L[4880] == ""
CH_NEW = (f"*V4.98 ({DATE}): additions only — title/As-of header bump; the V4.98 fold-in record; §2.98 (the remaining "
          f"mathematics) after §2.97; {len(EDITS)} in-line [→ V4.98] pointers; reverse-splice byte-identical to V4.97 "
          "(`a5a07bcd`); the §2.52 Open 3 row untouched.*")


def build():
    frags = [T_NEW, A_NEW, RECORD, S298_TXT, CH_NEW] + [n for _, n in EDITS]
    for fr in [A_NEW, RECORD, S298_TXT, CH_NEW]:
        assert s.count(fr) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    for old, new in EDITS:
        if old.startswith(R_ANCH):                       # the V4.97 record line now follows the new record
            assert out.count(RECORD + old + "\n") == 1
            out = out.replace(RECORD + old + "\n", RECORD + new + "\n", 1)
            continue
        assert out.count("\n" + old + "\n") == 1
        out = out.replace("\n" + old + "\n", "\n" + new + "\n", 1)
    out = out.replace(REG97 + "\n\n" + J_ANCH, REG97 + "\n\n" + S298_TXT + J_ANCH, 1)
    out = out.replace("\n" + LINE_CH97 + "\n", "\n" + LINE_CH97 + "\n" + CH_NEW + "\n", 1)
    for fr in frags:
        assert out.count(fr) == 1, f"fragment count != 1: {fr[:60]!r}"
    assert out.count(P) == len(EDITS)
    rev = out.replace("\n" + LINE_CH97 + "\n" + CH_NEW + "\n", "\n" + LINE_CH97 + "\n", 1)
    rev = rev.replace(REG97 + "\n\n" + S298_TXT + J_ANCH, REG97 + "\n\n" + J_ANCH, 1)
    for old, new in EDITS:
        rev = rev.replace(new + "\n", old + "\n", 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V497 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    print(("DRY RUN (not canonical): " if args.dry_run else "V4.98 FOLDED: ") + OUT)
    print("bytes:", len(b), "(V4.97 %d B; delta +%d B); chars delta +%d" % (V497_BYTES, len(b) - V497_BYTES, len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("pointers:", len(EDITS), "| §2.98 chars:", len(S298_TXT), "| record chars:", len(RECORD))
    print("reverse-splice: BYTE-IDENTICAL to V4.97 (%s) — PASS" % V497)
    print("all fragments landed exactly once — PASS")
