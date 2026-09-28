#!/usr/bin/env python3
"""foldin_v4_86_hk_closeout.py — FOLDS V4.86: HOUSEKEEPING ONLY — the repo desk closed out. No gate content, no Part V/VI row,
no retraction; additive brackets fill the slots V4.85 left open and record H-MS2-8 (the V4.85 fold-time repository
observation was wrong — stale chat-side clone; erratum ERRATUM_V4_85_H_MS2_8.md in gmscs2_gate/estate/).
Ten additive edits on SQT_Master_Ledger_v4_85_CANONICAL.md (md5 d9c237a7…):
  E1 title; E2 As-of prepend (accumulated); E3 V4.86 fold-in record (before V4.85); E4 additive bracket on the V4.85
  record's housekeeping sentence (the three merge commits and dates; the HK-2 landing; H-MS2-8); E5 additive bracket on
  §2.91.S's estate sentence (gmscs2_gate/ and gmscs2_gate/estate/ on main); E6 additive bracket on the §2.91.Q V4.85
  bracket's slot (PR #27 merged 6774013); E7 additive bracket on the §2.91.P V4.85 bracket (PR #28 merged 3a41828);
  E8 additive bracket on the V4.84-record V4.85 bracket (the slots filled); E9 additive bracket on the V4.83-record V4.85
  bracket (the slot filled); E10 changelog.
Facts that are only known at execution (the HK-2 PR number, merge commit, date; the fold-time git ls-remote answer; the
authorization record's md5) are read from v486_facts.json and asserted present — the edit text never carries a
placeholder into the ledger. `--dry-run` uses stand-in facts and writes to a scratch path to prove the anchors and the
reverse-splice before the real facts exist.
§2.52 Open 3: untouched — the unique Part VI row asserted byte-identical pre/post, in addition to the reverse-splice.
Anchors read from the file (never retyped) and asserted unique; reverse-splice reconstructs V4.85 byte-identically
before the output is accepted. Append-only; nothing prior modified; no retraction.
"""
import hashlib, json, sys, os

DRY = "--dry-run" in sys.argv
SRC = "/home/claude/v486/SQT_Master_Ledger_v4_85_CANONICAL.md"
OUT = "/home/claude/v486/SQT_Master_Ledger_v4_86_CANONICAL.md" if not DRY else "/home/claude/v486/_dryrun_v4_86.md"
V485 = "d9c237a7089d3ac69ffd3056d9c69c05"
V485_BYTES = 1715587

REQUIRED = ["fold_date_long", "fold_utc", "directive_stamp", "auth_md5", "auth_bytes", "hk2_pr", "hk2_branch", "hk2_head",
            "hk2_merge", "hk2_utc", "hk2_pdt", "landing_md5", "landing_bytes", "estate_ok", "lsremote_main", "lsremote_utc",
            "hk2_return", "store_note", "estate_tar_md5", "erratum_md5", "cc_items"]
if DRY:
    F = {k: f"⟨{k}⟩" for k in REQUIRED}
    F.update(fold_date_long="September 99, 2026", auth_bytes="9,999", hk2_pr="#99", hk2_merge="0000000", hk2_head="0000000", cc_items="⟨cc_items⟩",
             lsremote_main="0000000", estate_tar_md5="d86b9ffde9a6cf53fe11dd5009472b24", erratum_md5="196dbe30e9f5ab71169e7f90c61a62c8")
else:
    F = json.load(open("/home/claude/v486/v486_facts.json", encoding="utf-8"))
    for k in REQUIRED:
        assert k in F and F[k] and "⟨" not in str(F[k]), f"fact {k} missing or placeholder — halt"

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V485, "base V4.85 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V485_BYTES
L = s.split("\n")

# exact full anchors read from the file (never retyped)
LINE_CH85 = L[4613]   # *V4.85 (September 27, 2026): additions only — ...*
assert LINE_CH85.startswith("*V4.85 (September 27, 2026): additions only") and s.count(LINE_CH85) == 1
assert L[4614] == "" and len(L) == 4615, "changelog is no longer the tail — re-anchor"
O3_MARKS = [l for l in L if l.startswith("| **§2.52 Open 3**")]
assert len(O3_MARKS) == 1 and s.count(O3_MARKS[0]) == 1
O3_PRE = O3_MARKS[0]

# ---------------------------------------------------------------- E1 title
T_OLD = "# SQT Master Ledger — V4.85 Canonical\n"
T_NEW = "# SQT Master Ledger — V4.86 Canonical\n"
assert s.count(T_OLD) == 1

# ---------------------------------------------------------------- E2 As-of (accumulated prepend)
A_OLD = "**As of:** September 27, 2026 (V4.85 fold — "
A_SUM = (f"**As of:** {F['fold_date_long']} (V4.86 fold — **HOUSEKEEPING ONLY: the repository desk CLOSED OUT — PR #27 (gmscs1_gate/estate/) merged 6774013, PR #28 (the V4.79 canonical removed from the root) merged 3a41828, PR #29 (the G-MSCS2 CC leg, gmscs2_gate/) merged 14bcf93, all on September 27, 2026, 01:00:05–01:01:08 UTC; the gmscs2 fold-side estate landed as PR {F['hk2_pr']} ({F['hk2_merge']}, {F['hk2_utc']} UTC) → gmscs2_gate/estate/; no canonical ledger in the repository (FOLD_LEDGER_2026-06-18 restored); the base-list election (05302210 operative; 04438b74 not a generic base) standing. H-MS2-8 (chat-side, honesty): the V4.85 fold-time repository observation — 'at fold time (September 27, 01:07 UTC) the live remote showed main = d0a0e31 with none of the three contained' — was WRONG: all three had merged six minutes earlier; the chat-side clone's fetch refspec had been restricted to one branch since a single-branch shallow clone, so git fetch --all refreshed nothing relevant and a stale local ref was read instead of git ls-remote; the author's directive was accurate; scope bounded to three September 27 observations, nothing verdict-bearing touched; V4.85 not edited (append-only), the erratum {F['erratum_md5'][:8]} beside the records that carry the error in gmscs2_gate/estate/; process note binding: fold-time repository observations by git ls-remote, quoted. No gate content, no Part V/VI row, no retraction; §2.52 Open 3 untouched.** Full V4.86 record below. V4.85 fold (September 27, 2026) — ")
assert s.count(A_OLD) == 1

# ---------------------------------------------------------------- E3 fold-in record
R_ANCH = "**V4.85 fold-in record (September 27, 2026):**"
assert s.count(R_ANCH) == 1
RECORD = (f"**V4.86 fold-in record ({F['fold_date_long']}):** HOUSEKEEPING FOLD — the repository desk closed out; author-authorized (directive of {F['directive_stamp']}, recorded verbatim in `FOLD_AUTHORIZATION_V4_86.md` {F['auth_md5']}, {F['auth_bytes']} B — 'once you confirm the HK-2 PR is merged alongside PRs #27, #28, and #29, proceed with generating the V4.86 bracket to formally close out the repo desk' — the condition met and confirmed by `git ls-remote` at {F['lsremote_utc']} UTC: refs/heads/main = {F['lsremote_main']}; standing rules: append-only, anchors read from the file and asserted unique, reverse-splice byte-identical, the §2.52 Open 3 row untouched; no gate content, no Part V/VI row, no retraction). "
          "**HK-1 CLOSED — the three slots V4.85 left open, filled from the repository:** PR #27 — `gmscs1_gate/estate/` (the V4.83-delivered tarball 027afc74: closure memo 0825f136, comparator v1.1 54b32988, comparison d4a5b271, v1.1 supplementary 948852fe, authorization 76b43814, fold script 9f798c35, manifest; + CC's `CC_LANDING_VERIFICATION.md` 492b912d), branch claude/hk1-gmscs2-dispatch-e6vcfh-task-a head e3380c1, **merged 6774013, September 27, 2026, 01:00:05 UTC** (September 26, 18:00:05 PDT); PR #28 — `SQT_Master_Ledger_v4_79_CANONICAL.md` (6cfeca22, 1,493,745 B) removed from the repository root, exactly one deletion, `FOLD_LEDGER_2026-06-18.md` the only ledger file at the root, history retaining the blob, branch …-task-b head 9f530f0, **merged 3a41828, 01:00:29 UTC**; PR #29 — the G-MSCS2 CC leg of record, `gmscs2_gate/` (34 files: the return 290b3431, instrument e58ba9a6, checkpoint 9961745d, comparison a91d84a5, the decoded chat embeds, the dispatch 9af4306c, the T1 tools, X-1, X-6, CC's own tooling) and `gmscs1_gate/HK1_CC_RETURN_INBAND.md` 75f5f542, branch claude/hk1-gmscs2-dispatch-e6vcfh head 3849c3d, **merged 14bcf93, 01:01:08 UTC** — all three by the author within 63 seconds, four minutes before the V4.85 fold directive of 18:04 PDT. Chat-side content verification (September 27, 19:45 UTC): gmscs1_gate/estate/ 6/6 byte-exact against the delivered manifest, the manifest on main identical to the delivered one; PR #28's diff the single deletion; PR #29's diff 35 files under gmscs1_gate/ and gmscs2_gate/ only; gmscs2_gate/ 31/31 byte-identical against the chat-side files of record (the three remaining files CC's own extract / return-builder / hypothesis-compare scripts, as listed in the return). "
          f"**HK-2 CLOSED — the gmscs2 fold-side estate landed:** dispatch `HK2_GMSCS2_ESTATE_LANDING_DISPATCH_INBAND.md` v2 d09e6157 (649,371 B; P-4 single-file in-band, P-4.b armor on the tarball, P-4.c lone delivery; activation flag `ACTIVATE: HK2-GMSCS2-ESTATE-LANDING`; v1 782fe954 superseded — it lacked the erratum and carried the stale merge state inside its embedded records); the estate tarball `gmscs2_foldside_estate.tar.gz` {F['estate_tar_md5']} (117,969 B; 17 files: closure memo e43a0732, execution reports ae032ab9 / b6a96692, fold authorization 7eb8d344, fold script foldin_v4_85_gmscs2.py e1f55056, delta-only a6393324, the independent additive verifier cd5d6216, comparator v1.1 96d76bc1 + schema v1.1 d270899c FROZEN, the chat-side v1.0 run a91d84a5 and the v1.1 supplementary 91841a49, the determinism witness set 68569dac / ebe47964 / 4b1aa5f1, the V4.85 staging note 7be337ff, the erratum {F['erratum_md5'][:8]}, manifest 23d2dbf5 self-excluded); D-HK2-1 — the author's directive named the chat-leg tarball (c1b76d09, already on main via PR #29 as gmscs2_gate/), the fold-side tarball is what lands, recorded in the dispatch and CC's landing note; D-HK2-2 — armor-body collisions (gate-list indices 0, 5, 6, 9, 10, 22; base-list 0, 5, 6, 9, 10), not text. Landed by CC as **PR {F['hk2_pr']}** (branch {F['hk2_branch']}, head {F['hk2_head']}), **merged {F['hk2_merge']}, {F['hk2_utc']} UTC** ({F['hk2_pdt']} PDT) → `gmscs2_gate/estate/` — chat-side verification against the manifest: {F['estate_ok']}; CC's `CC_LANDING_VERIFICATION.md` {F['landing_md5']} ({F['landing_bytes']} B); CC's HK-2 return {F['hk2_return']}. {F['cc_items']} "
          "**H-MS2-8 (chat-side; honesty; housekeeping).** V4.85 states in its record, §2.91.S, the §2.91.Q / §2.91.P / V4.84-record / V4.83-record brackets, the closure memo e43a0732 §1.8 and the authorization 7eb8d344 that 'at fold time (September 27, 2026, 01:07 UTC) the live remote showed main = d0a0e31 with none of the three branches contained … recorded as observed'. That was false: all three had merged at 01:00:05 / 01:00:29 / 01:01:08 UTC — six minutes earlier — and main was 14bcf93. **The author's fold directive was accurate; the chat-side observation was not.** Cause: the chat-side clone had been created as a single-branch shallow clone during the G-2a-A1 cycle, so its fetch refspec was restricted to that one branch; every later `git fetch --all --prune` refreshed only that branch and reported up to date while origin/main stayed at d0a0e31; the V4.84 fold-time practice — `git ls-remote`, a live query, quoted in FOLD_AUTHORIZATION_V4_84.md — was not used at the V4.85 fold time. Found and fixed September 27, 19:41 UTC (refspec +refs/heads/*; main then advanced d0a0e31..14bcf93 on the first fetch). Scope bounded: the three September 27 observations (01:07 fold time, carried into V4.85; the 04:16 HK-2 report; the 12:18 scheduled check); every earlier repository observation of record was correct (V4.84 fold time by ls-remote, September 21; the V4.85 staging note's PR #25 / #26 / #13 verification, September 22; the HK-1 dispatch, September 23; the G-MSCS2 lock, chat-leg report and closure memo observations, September 26 — the three PRs had not merged at any of those times); the V4.85 statements on PR #25 (022fa3c), PR #26 (e3df402) and PR #13 (d0a0e31) are correct; nothing verdict-bearing is touched — the G-MSCS2 verdict, coefficients, comparisons and honesty items do not depend on the repository state. Disposition: V4.85 (d9c237a7) not edited — append-only — the wrong observation stands as written with the erratum `ERRATUM_V4_85_H_MS2_8.md` (" + F['erratum_md5'] + ", 5,320 B) beside it in gmscs2_gate/estate/; this record and the brackets below carry the correction. **Process note, binding on the chat side from this fold:** a fold-time repository observation is made with `git ls-remote <remote>` (live), never with a locally cached ref, and the record quotes the command and the refs it returned; any local clone used for content checks is fetched with the full refspec and its origin/main cross-checked against the ls-remote answer before being cited — this fold's observation: `git ls-remote origin refs/heads/main` at " + F['lsremote_utc'] + " UTC → " + F['lsremote_main'] + ". "
          "**PR #13 items closed:** g2a_l1_gate/ on main (PR #13, d0a0e31, September 22) — the G-2a-L1 estate recovered, the cited T1 list 04438b74 recovered (the §2.91.Q V4.85 bracket); the V4.79 canonical it committed at the root removed (PR #28); the author's election of September 23 (05302210 the operative base; 04438b74 not a generic base) standing as E-MS2-7. **Repository state at this fold:** main = " + F['lsremote_main'] + "; estates on main: gquanta_gate/estate/, gs2c1w_gate/estate/, g2aa1_gate/estate/ (PR #26), gmscs1_gate/estate/ (PR #27), g2a_l1_gate/ (PR #13), gmscs2_gate/estate/ (PR " + F['hk2_pr'] + "); canonical ledgers on main: none; the active canonical in project knowledge: V4.86 (this file) — " + F['store_note'] + " "
          "Estate: chat outputs/gmscs2/v486/ — this fold script, `FOLD_AUTHORIZATION_V4_86.md`, the V4.86 staging note (the three merges, H-MS2-8, the HK-2 slot), the delta-only file and the additive verifier's output; the erratum and the HK-2 dispatch builder in outputs/hk2/. No successor registered by this fold; the G-MSCS2 successors stand as registered at V4.85. Folded as this record + the title/As-of bump + six additive brackets (the V4.85 record's housekeeping sentence; §2.91.S's estate sentence; the §2.91.Q, §2.91.P, V4.84-record and V4.83-record V4.85 brackets) + one changelog line; append-only; nothing prior modified; the §2.52 Open 3 row untouched.\n\n")

# ---------------------------------------------------------------- E4 V4.85 record housekeeping sentence
HK_ANCH = "**The author's fold directive confirms merging PR #27, PR #28 and PR #29; at fold time (September 27, 2026, 01:07 UTC) the live remote showed main = d0a0e31 with none of the three branches contained, the V4.79 canonical still at the root, gmscs1_gate/estate/ and gmscs2_gate/ absent from main — recorded as observed, not resolved; merge commits and dates: ⟨to be entered at the V4.86 fold from the repository⟩.**"
assert s.count(HK_ANCH) == 1
HK_NEW = HK_ANCH + f" **[→ V4.86: the observation was WRONG (H-MS2-8 — a stale chat-side clone; erratum {F['erratum_md5'][:8]} in gmscs2_gate/estate/); at 01:07 UTC main was already 14bcf93 — PR #27 merged 6774013 (01:00:05 UTC), PR #28 merged 3a41828 (01:00:29 UTC), PR #29 merged 14bcf93 (01:01:08 UTC), the author's directive accurate; the gmscs2 fold-side estate then landed as PR {F['hk2_pr']} ({F['hk2_merge']}, {F['hk2_utc']} UTC) → gmscs2_gate/estate/. Full record at the V4.86 fold-in.]**"
assert s.count(HK_NEW) == 0

# ---------------------------------------------------------------- E5 §2.91.S estate sentence
SE_ANCH = "CC gmscs2_gate/ on claude/hk1-gmscs2-dispatch-e6vcfh (head 3849c3d; PR #29 per the author's fold directive; not on main at fold time — recorded as observed). Full record at the V4.85 fold-in."
assert s.count(SE_ANCH) == 1
SE_NEW = SE_ANCH + f" **[→ V4.86: 'not on main at fold time' was a wrong observation (H-MS2-8) — PR #29 had merged as 14bcf93 at 01:01:08 UTC, six minutes before; gmscs2_gate/ (34 files) on main since then, verified 31/31 byte-identical against the chat-side files of record; the fold-side estate landed as PR {F['hk2_pr']} ({F['hk2_merge']}, {F['hk2_utc']} UTC) → gmscs2_gate/estate/ (17 files incl. the erratum {F['erratum_md5'][:8]}; CC's landing note {F['landing_md5'][:8]}). The repository desk for this gate is closed.]**"
assert s.count(SE_NEW) == 0

# ---------------------------------------------------------------- E6 §2.91.Q V4.85 bracket slot
Q_ANCH = "merge commit and date: ⟨to be entered at the V4.86 fold from the repository⟩. The V4.83 canonical was not supplied to CC, so no reverse-splice check accompanied the landing.]**"
assert s.count(Q_ANCH) == 1
Q_NEW = Q_ANCH + " **[→ V4.86: PR #27 merged 6774013, September 27, 2026, 01:00:05 UTC — before the V4.85 fold time; the 'not contained' observation was wrong (H-MS2-8). gmscs1_gate/estate/ on main: 6/6 byte-exact against the delivered manifest 027afc74 + CC's landing note 492b912d.]**"
assert s.count(Q_NEW) == 0

# ---------------------------------------------------------------- E7 §2.91.P V4.85 bracket
P_ANCH = "confirmed merging by the author's V4.85 fold directive, not yet contained in main at fold time — recorded as observed.]**"
assert s.count(P_ANCH) == 1
P_NEW = P_ANCH + " **[→ V4.86: PR #28 merged 3a41828, September 27, 2026, 01:00:29 UTC — before the V4.85 fold time; the 'not yet contained' observation was wrong (H-MS2-8). The V4.79 canonical is gone from the root; FOLD_LEDGER_2026-06-18.md the only ledger file there; history retains the blob.]**"
assert s.count(P_NEW) == 0

# ---------------------------------------------------------------- E8 V4.84-record V4.85 bracket
V84_ANCH = "PR #13 (d0a0e31, September 22) put g2a_l1_gate/ and the V4.79 canonical on main (the §2.91.P and §2.91.Q brackets). Full record at the V4.85 fold-in.]**"
assert s.count(V84_ANCH) == 1
V84_NEW = V84_ANCH + f" **[→ V4.86: 'none contained in main at the V4.85 fold time' was wrong (H-MS2-8) — PR #27 6774013 (01:00:05 UTC), PR #28 3a41828 (01:00:29 UTC), PR #29 14bcf93 (01:01:08 UTC), all September 27, 2026, before the fold time; the gmscs2 fold-side estate PR {F['hk2_pr']} merged {F['hk2_merge']} ({F['hk2_utc']} UTC). Every housekeeping slot of the V4.84 and V4.85 records is now filled.]**"
assert s.count(V84_NEW) == 0

# ---------------------------------------------------------------- E9 V4.83-record V4.85 bracket
V83_ANCH = "merge commit and date ⟨to be entered at the V4.86 fold⟩; see the §2.91.Q V4.85 bracket.]**"
assert s.count(V83_ANCH) == 1
V83_NEW = V83_ANCH + " **[→ V4.86: PR #27 merged 6774013, September 27, 2026, 01:00:05 UTC (the 'not contained at the V4.85 fold time' observation wrong, H-MS2-8); gmscs1_gate/estate/ on main, 6/6 byte-exact. The G-MSCS1 estate slot, open since V4.83, is closed.]**"
assert s.count(V83_NEW) == 0

# ---------------------------------------------------------------- E10 changelog
CH_NEW = (f"*V4.86 ({F['fold_date_long']}): additions only — housekeeping fold, no gate content: title/As-of header bump (V4.85 → V4.86), the V4.86 fold-in summary prepended within the accumulated As-of header and the full V4.86 record at the top of the recent fold-in block (before V4.85) — the repository desk closed out (PR #27 6774013, PR #28 3a41828, PR #29 14bcf93, September 27, 2026, 01:00:05–01:01:08 UTC; the gmscs2 fold-side estate PR {F['hk2_pr']} {F['hk2_merge']}, {F['hk2_utc']} UTC) and H-MS2-8 recorded (the V4.85 fold-time repository observation wrong — stale chat-side clone; erratum in gmscs2_gate/estate/; the ls-remote process note binding) — "
          "six additive brackets: on the V4.85 fold-in record's housekeeping sentence, on §2.91.S's estate sentence, on the §2.91.Q V4.85 bracket's slot (PR #27), on the §2.91.P V4.85 bracket (PR #28), on the V4.84-record V4.85 bracket (the slots filled) and on the V4.83-record V4.85 bracket (the G-MSCS1 estate slot closed) — and this changelog line. No Part V or Part VI row. No retraction; no lock record touched; nothing prior modified. The §2.52 Open 3 row untouched (asserted byte-identical). Reverse-splice byte-verified against V4.85 (d9c237a7).*")
assert s.count(CH_NEW) == 0

# ================================================================ apply (forward)
out = s.replace(T_OLD, T_NEW, 1)
out = out.replace(A_OLD, A_SUM, 1)
out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
out = out.replace(HK_ANCH, HK_NEW, 1)
out = out.replace(SE_ANCH, SE_NEW, 1)
out = out.replace(Q_ANCH, Q_NEW, 1)
out = out.replace(P_ANCH, P_NEW, 1)
out = out.replace(V84_ANCH, V84_NEW, 1)
out = out.replace(V83_ANCH, V83_NEW, 1)
out = out.replace(LINE_CH85, LINE_CH85 + "\n" + CH_NEW, 1)

O3_POST = [l for l in out.split("\n") if l.startswith("| **§2.52 Open 3**")]
assert O3_POST == [O3_PRE] and out.count(O3_PRE) == 1, "§2.52 Open 3 row changed — halt"
for frag in (T_NEW, A_SUM, RECORD, HK_NEW, SE_NEW, Q_NEW, P_NEW, V84_NEW, V83_NEW, CH_NEW):
    assert out.count(frag) == 1
# bold balance: the inserted/modified text must not add an odd-** line (the base carries four pre-existing odd lines, left as is)
odd_base = sorted(l for l in s.split("\n") if l.count("**") % 2 == 1)
odd_out = sorted(l for l in out.split("\n") if l.count("**") % 2 == 1)
assert odd_out == odd_base, "an inserted or modified line has unbalanced bold — halt"

open(OUT, "w", encoding="utf-8", newline="\n").write(out)

# ================================================================ reverse-splice
rev = open(OUT, encoding="utf-8").read()
rev = rev.replace(LINE_CH85 + "\n" + CH_NEW, LINE_CH85, 1)
rev = rev.replace(V83_NEW, V83_ANCH, 1)
rev = rev.replace(V84_NEW, V84_ANCH, 1)
rev = rev.replace(P_NEW, P_ANCH, 1)
rev = rev.replace(Q_NEW, Q_ANCH, 1)
rev = rev.replace(SE_NEW, SE_ANCH, 1)
rev = rev.replace(HK_NEW, HK_ANCH, 1)
rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
rev = rev.replace(A_SUM, A_OLD, 1)
rev = rev.replace(T_NEW, T_OLD, 1)
rmd5 = hashlib.md5(rev.encode("utf-8")).hexdigest()
assert rmd5 == V485, "REVERSE-SPLICE FAILED: %s" % rmd5
assert rev == s

b = open(OUT, "rb").read()
print(("DRY RUN — " if DRY else "") + "V4.86 FOLDED:", OUT)
print("bytes:", len(b), " (V4.85 was %d B; delta +%d B)" % (V485_BYTES, len(b) - V485_BYTES))
print("md5:", hashlib.md5(b).hexdigest())
print("reverse-splice: BYTE-IDENTICAL to V4.85 (%s) — PASS" % V485)
print("§2.52 Open 3: the Part VI row byte-identical and unique — PASS")
print("edits landed exactly once: E1..E10 — PASS; no new unbalanced-bold line — PASS")
if DRY: os.remove(OUT); print("dry-run output removed")
