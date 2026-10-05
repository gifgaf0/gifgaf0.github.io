#!/usr/bin/env python3
"""foldin_v4_91_radiation_ratio.py — FOLDS V4.91: one figure at §2.91.V (banking annotation, no gate).
Author-authorized October 4, 2026, 20:21 PDT ("Go ahead a fold the updated figure"), on the staging note
lbc_bank/closure/NEXT_FOLD_NOTE.md: §2.91.V erratum (3) quotes the 3D quadrupole slow/fast power ratio as ≈ 9×10¹⁰,
computed with the first computation's c₁/c₂ = 33.6; with the V4.90 two-leg speeds it is 1.10–1.79×10¹¹.
Five additive edits on SQT_Master_Ledger_v4_90_CANONICAL.md (md5 ef69a573…, 1,777,039 B; the project-store copy was
read back at fold time and is byte-identical):
  E1 title; E2 As-of prepend (accumulated); E3 V4.91 fold-in record (before the V4.90 record);
  E4 one bracket at the end of §2.91.V; E5 one changelog line.
Anchors read from the file and asserted unique; the §2.52 Open 3 Part VI row asserted byte-identical; the reverse
splice must reconstruct V4.90 byte-identically before the output is accepted. Append-only; nothing prior modified.
Fold-time repository facts from a live `git ls-remote` immediately before the run (2026-10-05 03:22:08 UTC).
"""
import hashlib

SRC = "/home/claude/fold/SQT_Master_Ledger_v4_90_CANONICAL.md"
OUT = "/home/claude/fold/SQT_Master_Ledger_v4_91_CANONICAL.md"
V490, V490_BYTES = "ef69a5738e313c9d99ca2cdd641241f6", 1777039
LS_REMOTE = "2026-10-05 03:22:08 UTC"   # main = 6cd2c66 (PR #35 merged at 3664ed1); estate branch = 15237ea

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V490, "base V4.90 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V490_BYTES
L = s.split("\n")
assert len(L) == 4640 and L[-1] == "", "line structure changed — re-anchor"

# anchors read from the file (never retyped)
LINE_CH90 = L[4638]
assert LINE_CH90.startswith("*V4.90 (October 4, 2026): additions only") and s.count(LINE_CH90) == 1
V_LINE = L[1661]
assert V_LINE.startswith("**V. Longitudinal branch coupling on the instantiated supersolid") and s.count(V_LINE) == 1
ERR3 = "the 3D quadrupole slow/fast ratio is ≈ 9×10¹⁰, not ~10⁶"
assert V_LINE.count(ERR3) == 1 and s.count(ERR3) == 1, "erratum (3) not where staged"
O3 = [l for l in L if l.startswith("| **§2.52 Open 3**")]
assert len(O3) == 1 and s.count(O3[0]) == 1
O3_PRE = O3[0]

# ---------------------------------------------------------------- E1 title
T_OLD = "# SQT Master Ledger — V4.90 Canonical\n"
T_NEW = "# SQT Master Ledger — V4.91 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD

# ---------------------------------------------------------------- E2 As-of
A_OLD = "**As of:** October 4, 2026 (V4.90 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = ("**As of:** October 4, 2026 (V4.91 fold — **§2.91.V erratum (3): the 3D quadrupole slow/fast ratio is ≈ 10¹¹ "
         "(1.1–1.8×10¹¹ at the two-leg c₁/c₂ = 34–36), not 9×10¹⁰.** V4.90 fold (October 4, 2026) — ")

# ---------------------------------------------------------------- E3 fold-in record
R_ANCH = "**V4.90 fold-in record (October 4, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = ("**V4.91 fold-in record (October 4, 2026):** BANKING ANNOTATION, no gate; one figure; author-authorized "
          "(\"Go ahead a fold the updated figure\", October 4, 2026, 20:21 PDT; `FOLD_AUTHORIZATION_V4_91.md`). §2.91.V "
          "erratum (3) used the first computation's c₁/c₂ = 33.6; with V4.90's two-leg c₁ = 16.1–17.0 and c₂ = 0.471 "
          "the ratio is 1.10–1.79×10¹¹ (`lbc_bank/paper/revision_numbers_check.py`, R1; recomputed independently by a "
          "second reviewer). The paper was approved the same day (v1, `lbc_bank/paper/APPROVAL_V1.md`); its two-leg "
          "vortex-coupling derivation changes no ledger claim. `git ls-remote` " + LS_REMOTE + ": main = `6cd2c66` "
          "(PR #35 merged); estate branch = `15237ea`. No Part VI row; no retraction; §2.52 Open 3 untouched.\n\n")

# ---------------------------------------------------------------- E4 §2.91.V bracket
V_END = V_LINE[-60:]
assert V_LINE.endswith("static share, −39.2 orders, ξ_req, drag prefactor 1/4π.]") and s.count(V_END) == 1
BRACKET = (" [→ V4.91: erratum (3)'s ratio is ≈ 10¹¹ (1.1–1.8×10¹¹ at the corrected c₁/c₂ = 34–36), not 9×10¹⁰.]")
V_NEW = V_LINE + BRACKET

# ---------------------------------------------------------------- E5 changelog
CH_NEW = ("*V4.91 (October 4, 2026): additions only — title/As-of header bump; the V4.91 fold-in record; one bracket at "
          "§2.91.V; reverse-splice byte-identical to V4.90 (`ef69a573`); the §2.52 Open 3 row untouched.*")


def build():
    for frag in (A_NEW, RECORD, BRACKET, CH_NEW, T_NEW):
        assert s.count(frag) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    out = out.replace(V_LINE, V_NEW, 1)
    out = out.replace(LINE_CH90, LINE_CH90 + "\n" + CH_NEW, 1)
    O3_POST = [l for l in out.split("\n") if l.startswith("| **§2.52 Open 3**")]
    assert O3_POST == [O3_PRE] and out.count(O3_PRE) == 1, "§2.52 Open 3 row changed — halt"
    for frag in (T_NEW, A_NEW, RECORD, BRACKET, CH_NEW):
        assert out.count(frag) == 1
    # reverse-splice
    rev = out.replace(LINE_CH90 + "\n" + CH_NEW, LINE_CH90, 1)
    rev = rev.replace(V_NEW, V_LINE, 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V490 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    print("V4.91 FOLDED:", OUT)
    print("bytes:", len(b), "(V4.90 %d B; delta +%d B); chars delta +%d" % (V490_BYTES, len(b) - V490_BYTES,
                                                                            len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("reverse-splice: BYTE-IDENTICAL to V4.90 (%s) — PASS" % V490)
    print("§2.52 Open 3: Part VI row byte-identical and unique — PASS; edits E1..E5 landed exactly once — PASS")
