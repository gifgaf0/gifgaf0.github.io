#!/usr/bin/env python3
"""foldin_v4_100_slwe_threshold.py — fold V4.100: §2.100, the SLWE decryption threshold corrected, and three Zenodo
deposits recorded (the SLWE note; the gauge paper v6.4; Fluid Lattice Topology with its notice). Staged October 10 with
the threshold and the note; extended October 13, on the author's word, with the gauge paper and FLT deposits.

The fact: V4.94's brackets say decryption at the spec's noise never fails "for any q > 1032". That comes from
258 < q/4 and ignores the half unit lost in rounding q/2. At q = 1033, a prime, the worst case |N| = 258 decodes wrongly
under every decoder and rounding tried; from q = 1036 nothing fails (first prime 1039). Computed by
audit_followup/closeout/step3/3b_slwe_eprint/v2_runs/dfr_exact.py (one leg; no verdict rests on it).

Base: SQT_Master_Ledger_v4_99_CANONICAL.md at the repository root (md5 a86fa090…, 1,913,925 B; produced by
foldin_v4_99_decisions.py). Edits (all additive): title; As-of prepend; the V4.100 fold-in record (before the V4.99
record); §2.100 (after §2.99, before Cluster J); seven in-line "[→ V4.100 (§2.100): …]" pointers (three paragraph lines,
four table rows, where the pointer goes inside the last cell); one changelog line. Deposit facts: Zenodo record pages and
DataCite, read at fold time on October 13, 2026. Anchors are read from the file and
asserted unique; every fragment lands exactly once; the reverse splice must reconstruct V4.99 byte-identically.
"""
import argparse
import hashlib
import os

ap = argparse.ArgumentParser()
ap.add_argument("--word", required=True, help="the author's fold word, verbatim")
ap.add_argument("--when", required=True, help="time of the word, e.g. '20:05 PDT'")
ap.add_argument("--date", required=True, help="fold date, e.g. 'October 11, 2026'")
ap.add_argument("--head", required=True, help="estate head (branch commit) at fold time")
ap.add_argument("--ls-remote", required=True, help="UTC time of the live git ls-remote")
ap.add_argument("--main", required=True, help="main's sha from that ls-remote")
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "SQT_Master_Ledger_v4_99_CANONICAL.md"))
OUT = ("/home/claude/fold/SQT_Master_Ledger_v4_100_DRYRUN_NOT_CANONICAL.md" if args.dry_run
       else "/home/claude/fold/SQT_Master_Ledger_v4_100_CANONICAL.md")
V499 = "a86fa0907310b34413b42d7ebdbcb067"
DATE = args.date

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V499, "base V4.99 md5 mismatch — halt"
V499_BYTES = len(s.encode("utf-8"))
assert "§2.100" not in s and "V4.100" not in s
L = s.split("\n")
assert len(L) == 4919 and L[-1] == "", "line structure changed — re-anchor"


def one_line(prefix):
    hits = [x for x in L if x.startswith(prefix)]
    assert len(hits) == 1, f"anchor not unique: {prefix!r} ({len(hits)})"
    assert s.count("\n" + hits[0] + "\n") == 1
    return hits[0]


T_OLD, T_NEW = "# SQT Master Ledger — V4.99 Canonical\n", "# SQT Master Ledger — V4.100 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD
A_OLD = "**As of:** October 8, 2026 (V4.99 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = (f"**As of:** {DATE} (V4.100 fold — **the SLWE decryption threshold corrected (§2.100): q = 1033 fails, and "
         "decryption never fails from q = 1036 (first prime 1039), not \"for any q > 1032\"; three Zenodo deposits "
         "recorded: the SLWE note, the gauge paper v6.4, and Fluid Lattice Topology with its notice. No verdict or "
         "register changes; nothing published or sent from here.** "
         "V4.99 fold (October 8, 2026) — ")

P = "[→ V4.100 (§2.100): "
# (host prefix, must-contain on the host, pointer text, is_table_row)
BR = [
    ("- **OP-2.58.5 (new, opened by §2.66).**", "holds deterministically for any q > 1032 at η = 2",
     P + "not for any q > 1032. At q = 1033, a prime, the worst-case noise (258) decodes wrongly under every decoder "
         "and rounding tried; criterion (ii) holds deterministically from q = 1036, so the first prime is 1039.]", False),
    ("**Closure declaration.** OP-2.58.1.a (DFR at spec) is CLOSED with a null binding finding.", "(q > 1032 at η = 2)",
     P + "the bound 258 < q/4 ignores the half unit lost in rounding q/2: q = 1033 fails, and from q = 1036 decryption "
         "never fails (first prime 1039). At spec (q ≈ 2³²) nothing changes.]", False),
    ("| **OP-2.58.1.b** (ZD-vs-CBD DFR differential; sharpened) |", "a differential needs q ≤ 1032",
     P + "failures remain possible up to q = 1033, and up to 1035 with the reference decoder `tools/sqt_slwe.py`, so "
         "the differential needs q ≤ 1035.]", True),
    ("| **OP-2.58.1a harness port** (port the adjoint/DFR harness", "(DFR = 0 for any q > 1032 at η = 2)",
     P + "DFR = 0 from q = 1036, not 1033; the conclusion (no port is needed for DFR at spec) is unchanged.]", True),
    ("| **Phase C draft awaiting the author** (the SLWE negative-result note → IACR ePrint;", "IACR ePrint",
     P + "the author deposited the note on Zenodo on October 9, 2026 (doi:10.5281/zenodo.23270249). An independent "
         "audit on October 10 found four misstatements; the revision is in the repository (merged in PR #41; its "
         "Section 7 cites commit 4eb3014), for the author to deposit as version 2. Fluid Lattice Topology carries a "
         "notice withdrawing its security claims since October 13 (doi:10.5281/zenodo.23351706). Posting to ePrint is "
         "optional.]", True),
    ("**B1. Gauge paper v6.3 — correction drafted (v6.4).**", "Draft: `phase_b/B1/v6_4_draft/`",
     P + "v6.4 was deposited on October 13, 2026 (doi:10.5281/zenodo.23351330), after a close-out pass and a final "
         "pass that fixed small errors and changed no conclusion.]", False),
    ("| **Phase B drafts awaiting the author** (gauge paper v6.4 → Zenodo;", "gauge paper v6.4 → Zenodo",
     P + "the gauge paper v6.4 was deposited on October 13, 2026 (doi:10.5281/zenodo.23351330). This pointer says "
         "nothing about the row's other drafts.]", True),
]
EDITS = []
for prefix, must, text, row in BR:
    old = one_line(prefix)
    assert must in old and "[→ V4.100" not in old and "\n" not in text and text.endswith("]") and "|" not in text
    if row:
        assert old.endswith(" |")
        new = old[:-2] + " " + text + " |"
    else:
        assert not old.endswith(" |")
        new = old + " " + text
    EDITS.append((old, new))
assert len({o for o, _ in EDITS}) == len(EDITS) == 7

J_ANCH = "## J. Multi-Lens Reference and Phase Incommensurability\n"
REG99 = one_line("**Registers and non-claims.** One R1 fact, one leg; three classifications and two elections")
assert s.count(REG99 + "\n\n" + J_ANCH) == 1
S2100 = [
    "### §2.100 — The SLWE Decryption Threshold, and Three Zenodo Deposits (V4.100)",
    f"*(Folded V4.100, {DATE}, on the author's word of {args.when} (\"{args.word}\"; `FOLD_AUTHORIZATION_V4_100.md`). It "
    "corrects one fact that V4.94 carried into four brackets, and records three Zenodo deposits: the SLWE note, the "
    "gauge paper v6.4, and Fluid Lattice Topology with its notice. The affected entries carry [→ V4.100 (§2.100)] "
    "pointers. The fact is computed once (`audit_followup/closeout/step3/3b_slwe_eprint/v2_runs/dfr_exact.py`); no "
    "verdict rests on it, so there is no second leg. The deposit facts were read from Zenodo and DataCite at fold "
    "time.)*",
    "**In plain language.** The ledger said decryption at the spec's noise never fails once the modulus exceeds 1032. "
    "That came from requiring the worst-case noise, 258, to stay below q/4, and it forgot that q/2 gets rounded. At "
    "q = 1033 the worst case fails. From q = 1036 nothing fails, so the first safe prime is 1039. At the spec's modulus, "
    "about 2³², nothing changes. Separately, the author has put three things on Zenodo: the SLWE note, the corrected "
    "gauge paper, and *Fluid Lattice Topology* with a notice that withdraws its security claims.",
    "1. **The threshold.** With N ~ CBD(258), so |N| ≤ 258, the message encoded as m⌊q/2⌋ or m⌈q/2⌉, and four decoding "
    "rules (thresholds at q/4 and 3q/4, the nearest point, rounding 2v/q on the centred value, and the branchless "
    "rounding of `tools/sqt_slwe.py`): every rule fails at q = 1033 on the worst case |N| = 258; the reference rule "
    "with m⌊q/2⌋ also fails at q = 1035; no rule fails for any q from 1036 to 5000. V4.94's \"q > 1032\" therefore "
    "reads \"q ≥ 1036\" (first prime 1039), and OP-2.58.1.b's differential needs q ≤ 1035. "
    "`audit_followup/phase_c/C1/C1_RESULT.md` carries the same correction as an addendum.\n"
    "2. **The failure rate at q = 911.** C1's 2^−353.5 is the tail P(|N| > 227). The failure rate for a uniform "
    "message bit is 2^−353.91, or 2^−351.45 with the reference decoder and m⌊q/2⌋. Both are consistent with the 2⁻²⁹⁵ "
    "bound of *Fluid Lattice Topology* v2.\n"
    "3. **The note.** The author deposited the SLWE negative-result note on Zenodo on October 9, 2026 "
    "(doi:10.5281/zenodo.23270249). An independent audit on October 10 found four misstatements in it: three about "
    "other documents, and the threshold above. The revision corrects them and adds estimates under the same lattice "
    "estimator: version 2's parameters with a uniform matrix at 2^167.2, between ML-KEM-512 (2^139.7) and ML-KEM-768 "
    "(2^196.4) and about 95 bits below ML-KEM-1024 (2^262.3); and, with weight-64 secrets, both rows of the working "
    "specification's security table below 2^128. It is in the repository (merged in PR #41; its Section 7 cites "
    "commit 4eb3014), for the author to deposit as version 2. At fold time Zenodo holds only the first version: "
    "DataCite lists one version under the note's all-versions DOI, 10.5281/zenodo.23270248. The working "
    "specification (`tools/SLWE_Prime_Master_v2.md`, v2.4) and C1_RESULT carry append-only addenda.\n"
    "4. **The hybrid KEM.** `hybrid_kem/README.md` and `STATUS.md` carry a dated notice (October 10, 2026). The "
    "wrapper derives SLWE's shared secret as SHA-256(bit ‖ ciphertext), so SLWE adds at most one bit. The hybrid "
    "rests on ML-KEM-1024 alone.\n"
    "5. **The gauge paper, v6.4.** The author deposited it on October 13, 2026, as Zenodo version v6 of the record "
    "whose all-versions DOI is 10.5281/zenodo.19157947: doi:10.5281/zenodo.23351330, CC BY 4.0, one file, "
    "`Gifford_Csaszar_Gauge_Group_v6_4_2026.pdf` (md5 d1b8507a…). That is the PDF that `build_v6_4_pdf.py` builds "
    "from `Gifford_Csaszar_Gauge_Group_v6_4_2026_FINAL.md` (md5 f24dcc37…) in "
    "`audit_followup/closeout/step2/2a_gauge_paper/`. A final pass that day fixed small errors (31 logged "
    "replacements; the revision note's item (ix)) and changed no conclusion. It left ten points for the author "
    "(J1–J10 in `FINAL_PASS_CHANGE_LOG.md`), none registered here. The weightiest, J1, is that color SU(3) mixes the "
    "three Fano lines through a vertex that the paper takes as the three generations, which bears on its verified "
    "claim (2). The record's description, as read at fold time, still summarizes the earlier abstract, with "
    "hypercharge assignments and the leading CKM mixing angle among the results; the paper's own abstract is "
    "corrected, and the description is metadata that the author can edit without a new version.\n"
    "6. **Fluid Lattice Topology, with its notice.** This is the ledger's Rosetta Stone manuscript "
    "(`rosetta_stone_arxiv_v1.md` is its first version's text). The author deposited it on October 13, 2026, as "
    "Zenodo version v4 of the record whose all-versions DOI is 10.5281/zenodo.20078311: "
    "doi:10.5281/zenodo.23351706, one file, `Fluid_Lattice_Topology_v3.pdf` (md5 6bd55206…). It is the version 2 "
    "text with its editorial suggestions taken out and a framed notice on page 1, which also opens the record's "
    "description: the scheme of Section IV is insecure at both published parameter sets, and the NIST Category 5 "
    "claims of both versions are withdrawn. The notice cites the SLWE note through its all-versions DOI; its figures "
    "for version 2's parameters (about 2^167 with a uniform matrix, against 2^262 for ML-KEM-1024) are in the note's "
    "revision, which Zenodo does not yet hold. The file calls itself version 3 and the record says v4. DataCite also "
    "lists a version 10.5281/zenodo.23351115, which could not be read; the author reported at 13:48 PDT deleting "
    "the paper by accident. The files are in `audit_followup/closeout/step3/3b_slwe_eprint/flt_v3/`.",
    "**Registers and non-claims.** One R1 fact, one leg; estate facts as recorded, the deposit facts as read from "
    "Zenodo and DataCite at fold time. No verdict, register or row status changes; the SLWE negative result "
    "(§2.94.C1) stands; the final pass's ten points are not registered. The deposits are the author's; nothing is "
    "published, deposited or sent from here.",
]
S2100_TXT = "\n\n".join(S2100) + "\n\n"

R_ANCH = "**V4.99 fold-in record (October 8, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = (f"**V4.100 fold-in record ({DATE}):** SLWE THRESHOLD AND DEPOSITS — §2.100 and {len(EDITS)} in-line "
          "[→ V4.100] pointers, "
          f"on the author's word of {args.when} (\"{args.word}\"; `FOLD_AUTHORIZATION_V4_100.md`): V4.94's \"q > 1032\" "
          "corrected (q = 1033 fails; DFR = 0 from q = 1036; first prime 1039), computed by `dfr_exact.py` (one leg); "
          "the q = 911 tail and failure rate distinguished; three Zenodo deposits recorded: the SLWE note "
          "(doi:10.5281/zenodo.23270249, October 9; its October 10 revision not yet deposited), the gauge paper v6.4 "
          "(doi:10.5281/zenodo.23351330) and Fluid Lattice Topology with its notice (doi:10.5281/zenodo.23351706), "
          "both October 13; the hybrid KEM's notice recorded. No verdict, register or row changes; nothing published "
          f"or sent from here. Estate: head at fold `{args.head}`; `git ls-remote` {args.ls_remote}: main = "
          f"`{args.main}`. No §3.x; no observable bridge.\n\n")

LINE_CH99 = one_line("*V4.99 (October 8, 2026): additions only")
assert L[4917] == LINE_CH99 and L[4918] == ""
CH_NEW = (f"*V4.100 ({DATE}): additions only — title/As-of header bump; the V4.100 fold-in record; §2.100 (the SLWE "
          f"decryption threshold, and three Zenodo deposits) after §2.99; {len(EDITS)} in-line [→ V4.100] "
          "pointers; reverse-splice byte-identical to V4.99 (`a86fa090`).*")


def build():
    frags = [T_NEW, A_NEW, RECORD, S2100_TXT, CH_NEW] + [n for _, n in EDITS]
    for fr in [A_NEW, RECORD, S2100_TXT, CH_NEW]:
        assert s.count(fr) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    for old, new in EDITS:
        assert out.count("\n" + old + "\n") == 1
        out = out.replace("\n" + old + "\n", "\n" + new + "\n", 1)
    out = out.replace(REG99 + "\n\n" + J_ANCH, REG99 + "\n\n" + S2100_TXT + J_ANCH, 1)
    out = out.replace("\n" + LINE_CH99 + "\n", "\n" + LINE_CH99 + "\n" + CH_NEW + "\n", 1)
    for fr in frags:
        assert out.count(fr) == 1, f"fragment count != 1: {fr[:60]!r}"
    assert out.count(P) == len(EDITS)
    rev = out.replace("\n" + LINE_CH99 + "\n" + CH_NEW + "\n", "\n" + LINE_CH99 + "\n", 1)
    rev = rev.replace(REG99 + "\n\n" + S2100_TXT + J_ANCH, REG99 + "\n\n" + J_ANCH, 1)
    for old, new in EDITS:
        rev = rev.replace("\n" + new + "\n", "\n" + old + "\n", 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V499 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    print(("DRY RUN (not canonical): " if args.dry_run else "V4.100 FOLDED: ") + OUT)
    print("bytes:", len(b), "(V4.99 %d B; delta +%d B); chars delta +%d" % (V499_BYTES, len(b) - V499_BYTES, len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("pointers:", len(EDITS), "| §2.100 chars:", len(S2100_TXT), "| record chars:", len(RECORD))
    print("reverse-splice: BYTE-IDENTICAL to V4.99 (%s) — PASS" % V499)
    print("all fragments landed exactly once — PASS")
