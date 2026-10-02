#!/usr/bin/env python3
"""foldin_v4_88_g_vs1.py — V4.87 (dc243cb4) -> V4.88: the G-VS1 gate fold (the standard fold-script pattern).
Edits (all additive): E1 title bump; E2 As-of prepend; E3 the V4.88 fold-in record (before the V4.87 record);
E4 §2.91.U (after §2.91.T, before the Cluster J heading); E5 one Part VI row (after the G-MSCS-A row);
E6 the HK-4 housekeeping bracket at two anchors; E7 the G-QUANTA C1 scoping bracket at three anchors; E8 the changelog line.
Every inserted text is read from the closure memo (a7e2604d) §5 — "exactly as drafted" — with the two marked placeholders
filled (the directive's date/time; the fold-time ls-remote). Anchors are read from the file and asserted at their counts;
the reverse splice must reproduce the base md5; the §2.52 Open 3 row must be byte-identical; a delta-only listing is written."""
import hashlib, re, sys
SRC = "/home/claude/v488/SQT_Master_Ledger_v4_87_CANONICAL.md"; BASE_MD5 = "dc243cb4fd98f8c79e2a139f138eb6b0"; BASE_BYTES = 1757725
OUT = "/home/claude/v488/SQT_Master_Ledger_v4_88_CANONICAL.md"; DELTA = "/home/claude/v488/V4_88_DELTA_ONLY.txt"
MEMO = "/home/claude/g_vs1_gate/estate/G_VS1_TWOLEG_CLOSURE_MEMO.md"; MEMO_MD5 = "a7e2604d4dc56b1c12310880d5407211"
AUTH = "/home/claude/v488/FOLD_AUTHORIZATION_V4_88.md"
DIRECTIVE_TIME = "October 2, 2026, 14:51 PDT"; LSREMOTE = "2026-10-02 21:52:01 UTC"
def md5(s): return hashlib.md5(s.encode("utf-8")).hexdigest()
def must(text, needle, n, label):
    c = text.count(needle)
    assert c == n, f"{label}: count {c} != {n}"
base = open(SRC, encoding="utf-8").read()
assert md5(base) == BASE_MD5 and len(base.encode("utf-8")) == BASE_BYTES, "base mismatch"
memo = open(MEMO, encoding="utf-8").read(); assert md5(memo) == MEMO_MD5, "closure memo mismatch"
def between(a, b, src=memo):
    i = src.find(a); assert i >= 0, a[:40]; i += len(a); j = src.find(b, i); assert j >= 0, b[:40]; return src[i:j]
# ---- texts from the closure memo §5
summary = between('prepended: **"V4.88 fold — ', ' Full V4.88 record below."**')
record = between("**V4.88 fold-in record (October 2, 2026):**", "\n\n**§2.91.U (new; after §2.91.T):**").strip()
record = "**V4.88 fold-in record (October 2, 2026):** " + record
record = record.replace("author-authorized (directive of ⟨date/time⟩)", f"author-authorized (directive of {DIRECTIVE_TIME} — 'I explicitly AUTHORIZE the V4.88 fold')")
record = record.replace("Repository state at fold by `git ls-remote` ⟨to be quoted at fold⟩:", f"Repository state at fold by `git ls-remote` ({LSREMOTE}):")
assert "⟨" not in record and "⟩" not in record, "unfilled placeholder in the record"
U = between("**§2.91.U (new; after §2.91.T):** ", "\n\n**Part VI row (after the G-MSCS-A row):**").strip()
assert U.startswith("**U. Gate G-VS1 REGISTERED + LOCKED + EXECUTED")
row = between("**Part VI row (after the G-MSCS-A row):** `", "`\n")
assert row.startswith("| **Gate G-VS1**") and row.count("|") == 3
hk4 = between("after `the rest with HK-4)` (§2.91.T's estate bracket): **", "**\n\n**G-QUANTA C1 scoping bracket")
assert hk4.startswith("[→ V4.88 housekeeping: HK-4 landed") and hk4.endswith("the desk closed.]")
gq = between("(the G-QUANTA Part VI row): **", "**\n\n**Changelog line:**")
assert gq.startswith("[→ G-VS1 (V4.88) scoping:") and gq.endswith("no re-scoring.]")
changelog = between("**Changelog line:** *", "*\n\n**Housekeeping to carry:**")
changelog = "*" + changelog + "*"
# ---- anchors (asserted on the base)
T_OLD = "# SQT Master Ledger — V4.87 Canonical\n"; T_NEW = "# SQT Master Ledger — V4.88 Canonical\n"
A_OLD = "**As of:** September 30, 2026 (V4.87 fold — "
A_NEW = "**As of:** October 2, 2026 (V4.88 fold — **" + summary + "** Full V4.88 record below. V4.87 fold (September 30, 2026) — "
R_ANCH = "**V4.87 fold-in record (September 30, 2026):**"
J_ANCH = "\n\n## J. Multi-Lens Reference and Phase Incommensurability\n"
ROW_A = [l for l in base.split("\n") if l.startswith("| **Gate G-MSCS-A**")]; assert len(ROW_A) == 1; ROW_A = ROW_A[0]
LINE87 = [l for l in base.split("\n") if l.startswith("*V4.87 (September 30, 2026): additions only")]; assert len(LINE87) == 1; LINE87 = LINE87[0]
HK_1 = "they land with HK-4 together with the chat-side estate."
HK_2 = "the rest with HK-4)"
GQ_1 = "PASS L_B Borromean baryon / K₇ vortex / electron 2π closure"
GQ_2 = "K₇ vortex (§3.4) PASS — the independence witness"
GQ_3 = "PASS L_B Borromean / K₇ vortex (witness, GP class) / electron 2π"
for needle, n, label in [(T_OLD, 1, "title"), (A_OLD, 1, "As-of"), (R_ANCH, 1, "record anchor"), (J_ANCH, 1, "J heading"), (ROW_A + "\n", 1, "G-MSCS-A row"),
                         (LINE87 + "\n", 1, "V4.87 changelog"), (HK_1, 1, "HK-4 anchor 1"), (HK_2, 1, "HK-4 anchor 2"), (GQ_1, 1, "G-QUANTA anchor 1"),
                         (GQ_2, 1, "G-QUANTA anchor 2"), (GQ_3, 1, "G-QUANTA anchor 3"), (T_NEW, 0, "new title absent"), (A_NEW, 0, "new As-of absent")]:
    must(base, needle, n, label)
assert base.count("**U. Gate G-VS1") == 0 and base.count("| **Gate G-VS1**") == 0
OPEN3 = [l for l in base.split("\n") if l.startswith("| **§2.52 Open 3**")]; assert len(OPEN3) == 1
# ---- forward (brackets on the base text first, then the insertions)
edits = [
    ("E6 HK-4 bracket (anchor 1, the V4.87 record)", HK_1, HK_1 + " **" + hk4 + "**", 1),
    ("E6 HK-4 bracket (anchor 2, §2.91.T estate bracket)", HK_2, HK_2 + " **" + hk4 + "**", 1),
    ("E7 G-QUANTA bracket (anchor 1, the V4.82 record)", GQ_1, GQ_1 + " **" + gq + "**", 1),
    ("E7 G-QUANTA bracket (anchor 2, §2.91.P)", GQ_2, GQ_2 + " **" + gq + "**", 1),
    ("E7 G-QUANTA bracket (anchor 3, the G-QUANTA Part VI row)", GQ_3, GQ_3 + " **" + gq + "**", 1),
    ("E1 title", T_OLD, T_NEW, 1),
    ("E2 As-of summary (prepended)", A_OLD, A_NEW, 1),
    ("E3 V4.88 fold-in record", R_ANCH, record + "\n\n" + R_ANCH, 1),
    ("E4 §2.91.U", J_ANCH, "\n\n" + U + J_ANCH, 1),
    ("E5 Part VI row", ROW_A + "\n", ROW_A + "\n" + row + "\n", 1),
    ("E8 changelog line", LINE87 + "\n", LINE87 + "\n" + changelog + "\n", 1),
]
out = base
for label, old, new, n in edits:
    must(out, old, n, label + " (forward)"); out = out.replace(old, new)
assert out.count(hk4) == 2 and out.count(gq) == 3 and out.count("**U. Gate G-VS1") == 1 and out.count(row) == 1
assert [l for l in out.split("\n") if l.startswith("| **§2.52 Open 3**")] == OPEN3, "Open 3 row changed"
assert [l for l in out.split("\n") if l.startswith("| **Gate G-VS1**")][0].count("|") == 3
# ---- reverse splice
back = out
for label, old, new, n in reversed(edits):
    must(back, new, n, label + " (reverse)"); back = back.replace(new, old)
assert md5(back) == BASE_MD5 and back == base, "REVERSE SPLICE FAILED"
open(OUT, "w", encoding="utf-8").write(out)
# ---- delta-only listing
d = [f"V4_88_DELTA_ONLY — every segment inserted into V4.87 ({BASE_MD5}) to make V4.88; nothing else changed (reverse-splice byte-identical)\n"]
d += ["=== E1 title ===", T_NEW, "=== E2 As-of summary (prepended) ===", A_NEW, "", "=== E3 V4.88 fold-in record ===", record, "", "=== E4 §2.91.U ===", U, "",
      "=== E5 Part VI row ===", row, "", "=== E6 HK-4 housekeeping bracket (×2: the V4.87 record; §2.91.T's estate bracket) ===", " **" + hk4 + "**", "",
      "=== E7 G-QUANTA C1 scoping bracket (×3: the V4.82 record; §2.91.P; the G-QUANTA Part VI row) ===", " **" + gq + "**", "", "=== E8 changelog line ===", changelog, ""]
open(DELTA, "w", encoding="utf-8").write("\n".join(d))
ob = out.encode("utf-8")
print("V4.88", md5(out), len(ob), "B (+%d B)" % (len(ob) - BASE_BYTES)); print("reverse-splice PASS; §2.52 Open 3 row byte-identical; delta", hashlib.md5(open(DELTA, "rb").read()).hexdigest())
for label, old, new, n in edits: print("  ", label, "x%d" % n)
