#!/usr/bin/env python3
"""foldin_v4_96_floor_election.py — STAGED fold V4.96: the polycrystal floor elected (N = 50).

Records the author's election "I select N = 50" (October 7, 2026, 19:16 PDT) on the polycrystal-floor row and its
consequences, computed from the §2.95 two-leg numbers by `lattice_bound/ls_election_n50.py`. The fold runs only on the
author's fold word: the word, its time, the estate head and the live `git ls-remote` facts are passed on the command line
and written into the record verbatim. A dry run (placeholders, --dry-run) writes a candidate file that is not canonical.

Base: SQT_Master_Ledger_v4_95_CANONICAL.md (md5 3b6c11c3…, 1,871,378 B; produced by foldin_v4_95_lattice_bound.py).

Edits (all additive): E1 title; E2 As-of prepend; E3 the V4.96 fold-in record (before the V4.95 record); E5 §2.96 (after
§2.95's last paragraph, before Cluster J); E6 ten in-line "[→ V4.96 (§2.96): …]" pointers; E8 one changelog line.
(No E4, no E7: no Preamble rule and no new Part VI row; the election is recorded on the floor row itself.)
Anchors are read from the file and asserted unique; every fragment lands exactly once; the reverse splice must
reconstruct V4.95 byte-identically.
"""
import argparse
import hashlib

ap = argparse.ArgumentParser()
ap.add_argument("--word", required=True, help="the author's fold word, verbatim")
ap.add_argument("--when", required=True, help="when the fold word was given (local time)")
ap.add_argument("--date", required=True, help="fold date for the ledger, e.g. 'October 7, 2026'")
ap.add_argument("--head", required=True, help="estate head at fold (short sha)")
ap.add_argument("--ls-remote", required=True, help="UTC timestamp of the live git ls-remote")
ap.add_argument("--main", required=True, help="main's short sha from that ls-remote")
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

SRC = "/home/claude/fold/SQT_Master_Ledger_v4_95_CANONICAL.md"
OUT = ("/home/claude/fold/SQT_Master_Ledger_v4_96_DRYRUN_NOT_CANONICAL.md" if args.dry_run
       else "/home/claude/fold/SQT_Master_Ledger_v4_96_CANONICAL.md")
V495, V495_BYTES = "3b6c11c33fdc88566f8cc1774d2d6a7b", 1871378
DATE = args.date

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V495, "base V4.95 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V495_BYTES
assert "§2.96" not in s and "V4.96" not in s
L = s.split("\n")
assert len(L) == 4727 and L[-1] == "", "line structure changed — re-anchor"


def one_line(prefix):
    hits = [x for x in L if x.startswith(prefix)]
    assert len(hits) == 1, f"anchor not unique: {prefix!r} ({len(hits)})"
    assert s.count("\n" + hits[0] + "\n") == 1
    return hits[0]


# ---------------------------------------------------------------- E1 title
T_OLD = "# SQT Master Ledger — V4.95 Canonical\n"
T_NEW = "# SQT Master Ledger — V4.96 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD

# ---------------------------------------------------------------- E2 As-of
A_OLD = "**As of:** October 7, 2026 (V4.95 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = (f"**As of:** {DATE} (V4.96 fold — **the polycrystal floor ELECTED at N = 50 cells per grain (§2.96; the "
         "author's election): with it the photon data require a ≤ 4.15×10⁻³⁷ m (0.026 ℓ_P), and the declared 12–47 ℓ_P "
         "lattice leaves no light window on any arm. No scale pinned. Nothing published or sent.** V4.95 fold "
         "(October 7, 2026) — ")

# ---------------------------------------------------------------- E6 pointers (prefix, text, kind)
BR = [
    ("| **Polycrystal validity floor** (§2.94.C2 P2",
     "[→ V4.96 (§2.96): ELECTED — N = 50 (the author, October 7, 2026: 'I select N = 50'). At this floor the photon "
     "data require a ≤ 4.15×10⁻³⁷ m (0.026 ℓ_P), and the declared chain leaves no window on any arm.]", "row"),
    ("| **Lattice-spacing bound** (§2.95",
     "[→ V4.96 (§2.96): at the elected floor N = 50, a ≤ 4.15×10⁻³⁷ m (0.026 ℓ_P; with τ × 10, 0.055 ℓ_P).]", "row"),
    ("**The bound (R1-machine two-leg).** Attenuation",
     "[→ V4.96 (§2.96): the author elected N = 50, so the data require a ≤ 4.15×10⁻³⁷ m = 0.026 ℓ_P.]", "para"),
    ("**N. Gate G-CI1 REGISTERED + LOCKED + EXECUTED",
     "[→ V4.96 (§2.96): at the elected floor N = 50, the declared chain's fifty cells (≥ 9.50×10⁻³³ m) exceed this "
     "window's edge 2.5-fold, so under that chain the window is empty even on its own anchor; off the chain, the photon "
     "data require a ≤ 4.15×10⁻³⁷ m. The window of record stands as computed.]", "para"),
    ("| **Gate G-CI1** (the Q3(1) carrier-identity gate:",
     "[→ V4.96 (§2.96): at the elected floor N = 50: under the declared chain, empty on every arm; otherwise a ≤ "
     "4.15×10⁻³⁷ m.]", "row"),
    ("| **Gate G-S2C1-W** (the W_∪′ re-derivation mini-gate",
     "[→ V4.96 (§2.96): at the elected floor N = 50 its a_phys band leaves no light window on any arm (50·a_phys ≥ "
     "9.50×10⁻³³ m > 3.764×10⁻³³ m); the verdict stands as recorded.]", "row"),
    ("**DECLARED (reading (a); author word \"Lock\", July 22, 2026;",
     "[→ V4.96 (§2.96): with the elected floor N = 50, the photon data bound the transverse lattice scale at a ≤ "
     "4.15×10⁻³⁷ m (0.026 ℓ_P); the import stays unexercised.]", "para"),
    ("**E. What the substrate program still stands on.**",
     "[→ V4.96 (§2.96): at the elected floor N = 50 the light carrier's cells must be ≤ 0.026 ℓ_P.]", "para"),
    ("**M. Gate G-POLY1 REGISTERED + LOCKED + PARTIALLY EXECUTED",
     "[→ V4.96 (§2.96): on the light side the polycrystal postulate now needs cells ≤ 4.15×10⁻³⁷ m (0.026 ℓ_P) at the "
     "elected floor N = 50, and the declared chain leaves it no grain size; the postulate stays R3.]", "para"),
    ("| **Polycrystalline-vacuum / domain-averaging (VRH) exploration**",
     "[→ V4.96 (§2.96): on the light side the postulate needs cells ≤ 0.026 ℓ_P at the elected floor N = 50; under the "
     "declared chain no grain size remains. Still R3.]", "row"),
]
EDITS = []
for prefix, text, kind in BR:
    old = one_line(prefix)
    assert "[→ V4.96" not in old and "\n" not in text
    assert text.startswith("[→ V4.96 (§2.96): ") and text.endswith("]")
    if kind == "para":
        assert not old.endswith(" |")
        new = old + " " + text
    else:
        assert old.endswith(" |") and old.startswith("| ") and "|" not in text
        new = old[:-2] + " " + text + " |"
    EDITS.append((old, new))
assert len({o for o, _ in EDITS}) == len(EDITS), "two pointers on one line"
NBR = len(EDITS)
assert NBR == 10

# ---------------------------------------------------------------- E5 §2.96
J_ANCH = "## J. Multi-Lens Reference and Phase Incommensurability\n"
assert s.count(J_ANCH) == 1 and s.count("\n\n" + J_ANCH) == 1
REG95 = one_line("**The floor, registers and non-claims.** The homogenization literature")
assert s.count(REG95 + "\n\n" + J_ANCH) == 1
S296 = [
    "### §2.96 — The Polycrystal Floor Elected: N = 50 (V4.96)",
    f"*(Folded V4.96, {DATE}: the author's election of the polycrystal validity floor — \"I select N = 50\" (October 7, "
    f"2026, 19:16 PDT) — and fold word \"{args.word}\" ({args.when}). The consequences are computed from §2.95's two-leg "
    "numbers by `lattice_bound/ls_election_n50.py`: no new derivation, and no scale is pinned. \"What rests on which "
    "data\" adds the two sentences the author asked for with the fold word, the second scoped to the TeV arms (see "
    "`FOLD_AUTHORIZATION_V4_96.md`). The affected entries carry [→ V4.96 (§2.96)] pointers.)*",
    "**In plain language.** The author has set the minimum vacuum grain at 50 lattice cells, the low end of what the "
    "materials literature supports for a grain to behave as a bulk crystal. With that floor the photon data require a "
    "lattice spacing of at most 4.15×10⁻³⁷ m, 0.026 Planck lengths. The ledger's declared lattice, 12–47 Planck lengths, "
    "leaves no light window on any photon arm, not even on W^EM_∪'s own sub-TeV anchor.",
    "**Consequences.** (1) a ≤ d_max/50 = 4.15×10⁻³⁷ m = 0.0257 ℓ_P (combined; decisive the Cygnus arm; the Crab gives "
    "0.0260 ℓ_P; with τ × 10, 0.0553 ℓ_P). The anchor arm alone would allow 7.53×10⁻³⁵ m (4.66 ℓ_P). (2) Under the "
    "declared chain (a_phys ∈ [1.899, 7.588]×10⁻³⁴ m; G-S2C1-W's E-W-1(a)), fifty cells span 9.50×10⁻³³–3.79×10⁻³² m, "
    "wider than every arm's d_max, including W^EM_∪'s edge of 3.764×10⁻³³ m (by a factor of 2.52): the window is empty "
    "on every arm. (3) A lattice at or above ℓ_P leaves no window, since the combined bound allows at most 1.28 cells "
    "per grain at a = ℓ_P.",
    "**What rests on which data.** With the PeV bound, the no-window verdict holds for every N ≥ 2 (for a Planck-length "
    "lattice at 10× the loss, every N ≥ 3); N = 50 sets only the quoted spacing (0.026 ℓ_P, or 0.055 at 10× the loss). "
    "Without the PeV data, W^EM_∪'s original anchor alone would need N ≥ 20 for the declared-chain verdict and would fit "
    "a Planck-length lattice up to N ≈ 233. The TeV arms close most of that without PeV photons: Mrk 501 (16 TeV) and "
    "GRB 221009A (7.7 TeV) fit a Planck-length lattice only up to N = 6 and N = 10 (13 and 23 at 10× the loss) and leave "
    "the declared chain no window for any N ≥ 2, so the Planck-lattice verdict at N = 50 does not depend on the PeV data, "
    "which extend it from N ≥ 7 down to N ≥ 2 (from N ≥ 14 to N ≥ 3 at 10× the loss).",
    "**Registers and non-claims.** The election is the author's (T3-immutable); the consequences "
    "are R1 arithmetic on two-leg numbers, and (2) is conditional on E-W-1(a). No scale is pinned and no lower limit on "
    "a is declared. W^EM_∪ of record, the G-S2C1-W verdict and the polycrystal postulate's register (R3) stand as "
    "recorded; A1, A2, the second-sound drag and KC-EP are untouched. Nothing is published or sent.",
]
S296_TXT = "\n\n".join(S296) + "\n\n"

# ---------------------------------------------------------------- E3 fold-in record
R_ANCH = "**V4.95 fold-in record (October 7, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = (f"**V4.96 fold-in record ({DATE}):** POLYCRYSTAL FLOOR ELECTED — the author's election \"I select N = 50\" "
          f"(October 7, 2026, 19:16 PDT) and fold word \"{args.word}\" ({args.when}); `FOLD_AUTHORIZATION_V4_96.md`. The "
          "consequences were computed from the §2.95 two-leg numbers (`ls_election_n50.py`; both legs' d_max agree to "
          "10⁻¹²): a ≤ 4.15×10⁻³⁷ m (0.026 ℓ_P); under the declared chain the window is empty on every arm, including "
          "W^EM_∪'s anchor; a lattice at or above ℓ_P leaves no window. At the author's request §2.96 also records which "
          "verdicts rest on which data: the PeV arms exclude a Planck-length lattice for every N ≥ 2, and the TeV arms "
          "alone already do so for N ≥ 7. Recorded as §2.96, with "
          f"{NBR} in-line [→ V4.96] pointers. No scale pinned; nothing published or sent. Estate: `audit_followup/` on "
          f"branch `claude/audit-followup-oct6` (head at fold `{args.head}`); `git ls-remote` {args.ls_remote}: main = "
          f"`{args.main}`. No §3.x; no observable bridge.\n\n")

# ---------------------------------------------------------------- E8 changelog
LINE_CH95 = one_line("*V4.95 (October 7, 2026): additions only")
assert L[4725] == LINE_CH95 and L[4726] == ""
CH_NEW = (f"*V4.96 ({DATE}): additions only — title/As-of header bump; the V4.96 fold-in record; §2.96 (the polycrystal "
          f"floor elected, N = 50) after §2.95; {NBR} in-line [→ V4.96] pointers; reverse-splice byte-identical to V4.95 "
          "(`3b6c11c3`).*")


def build():
    frags = [T_NEW, A_NEW, RECORD, S296_TXT, CH_NEW] + [n for _, n in EDITS]
    for fr in [A_NEW, RECORD, S296_TXT, CH_NEW]:
        assert s.count(fr) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    for old, new in EDITS:
        assert out.count("\n" + old + "\n") == 1
        out = out.replace("\n" + old + "\n", "\n" + new + "\n", 1)
    out = out.replace(REG95 + "\n\n" + J_ANCH, REG95 + "\n\n" + S296_TXT + J_ANCH, 1)   # §2.95's last line: no pointer
    out = out.replace("\n" + LINE_CH95 + "\n", "\n" + LINE_CH95 + "\n" + CH_NEW + "\n", 1)
    for fr in frags:
        assert out.count(fr) == 1, f"fragment count != 1: {fr[:60]!r}"
    assert out.count("[→ V4.96 (§2.96): ") == NBR
    rev = out.replace("\n" + LINE_CH95 + "\n" + CH_NEW + "\n", "\n" + LINE_CH95 + "\n", 1)
    rev = rev.replace(REG95 + "\n\n" + S296_TXT + J_ANCH, REG95 + "\n\n" + J_ANCH, 1)
    for old, new in EDITS:
        rev = rev.replace("\n" + new + "\n", "\n" + old + "\n", 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V495 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    print(("DRY RUN (not canonical): " if args.dry_run else "V4.96 FOLDED: ") + OUT)
    print("bytes:", len(b), "(V4.95 %d B; delta +%d B); chars delta +%d" % (V495_BYTES, len(b) - V495_BYTES, len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("pointers:", NBR, "| §2.96 chars:", len(S296_TXT), "| record chars:", len(RECORD))
    print("reverse-splice: BYTE-IDENTICAL to V4.95 (%s) — PASS" % V495)
    print("all fragments landed exactly once — PASS")
