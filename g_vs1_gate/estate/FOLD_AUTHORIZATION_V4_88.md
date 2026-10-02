# FOLD AUTHORIZATION — V4.88 (Gate G-VS1 — vacuum selection in the 16-component substrate, the HYP-A1-5 successor, CLOSED two-leg; delivery gate)

**Recorded:** October 2, 2026, 21:52 UTC (the author's directive timestamped October 2, 2026, 14:51 PDT). **Base:** `SQT_Master_Ledger_v4_87_CANONICAL.md` md5 `dc243cb4fd98f8c79e2a139f138eb6b0` (1,757,725 B). **Kind:** gate fold — §2.91.U written from the closure memo `G_VS1_TWOLEG_CLOSURE_MEMO.md` (`a7e2604d4dc56b1c12310880d5407211`, 23,468 B; §5, as drafted); one Part VI row; the V4.88 fold-in record; the title/As-of bump; the HK-4 housekeeping bracket at its two anchors and the G-QUANTA C1 scoping bracket at its three anchors, exactly as the closure memo specifies; one changelog line. No retraction; no lock record touched; the §2.52 Open 3 row untouched; reverse-splice byte-identical to V4.87. Two placeholders of the drafted record filled at fold, as the draft marks them: the authorizing directive's date/time (October 2, 2026, 14:51 PDT) and the fold-time `git ls-remote` observation (below).

## The author's directive (verbatim, October 2, 2026, 14:51 PDT)

> **Directive: Authorize V4.88 Fold (G-VS1)**
>
> I explicitly AUTHORIZE the V4.88 fold.
> Delete claude/staging_memo_G_VS1_v1.md from the project store to clear capacity for the swap.
> Please proceed with the following steps:
> Delete claude/staging_memo_G_VS1_v1.md from the project store.
> Execute foldin_v4_88_g_vs1.py (which you will need to write following the standard fold-script pattern) on base dc243cb4 (V4.87).
> Write the proposed fold record from the closure memo exactly as drafted as the new §2.91.U block.
> Append the HK-4 and G-QUANTA C1 scoping brackets to their respective anchors exactly as specified in the closure memo.
> Verify that the reverse-splice reconstructs V4.87 byte-identically.
> Check project store capacity and execute the V4.87 → V4.88 swap.
> Report back with the final V4.88 hash, bytes, and the store swap status.
> Once V4.88 is generated, build the final estate PR dispatch (HK-5) to land the G-VS1 artifacts onto main.

## The chain of the author's words that this fold rests on (verbatim in the lock record `71711946d1c4abb06fa17402e8d5a6c9` §3 and the dispatch `fa5f2cb3368727a06d078f0daffdd005`)

- September 30, 2026, 11:45 PDT: the gate opened ("Initiate Vacuum Selection (HYP-A1-5) Gate"; the HK-4 bracket to ride this fold; no standalone housekeeping fold).
- September 30, 12:10 PDT: the five readings Q-VS-1..5; elections E-VS-1(a) … E-VS-9(a); "Please proceed with the v2 draft."
- September 30, 19:46 PDT: **"Lock Gate G-VS1"** — E-VS-1 through E-VS-10(a); freeze; build; dispatch.
- The activation flag `ACTIVATE: G-VS1-CC-LEG-1` given to CC (CC's return §1, verbatim).
- October 2, 2026, 14:51 PDT: this fold authorization (the S9 election (a) implicit in "exactly as drafted": close on run 1, comparator v1.0 the run of record, v1.1 + projection supplementary).

## Repository state at fold (recorded as observed by `git ls-remote`, 2026-10-02 21:52:01 UTC — the H-MS2-8 process note)

`refs/heads/main` = `7460a7853a086c826a8d23af90f5f72854974f13` ("Merge pull request #33 from gifgaf0/claude/new-session-7flqwf", 2026-09-30 16:32:26 UTC — the HK-4 landing); `refs/heads/claude/new-session-tf548k` = `c21a25f2a37fcb3e3064219d48db093d3556af41` (CC's five G-VS1 commits: `82b2ff9` the thirteen raw embeds; `c44d731` instrument + pre-read checkpoint `7c407373`; `f9b88d9` the pre-consultation checkpoint `05e82029`, VC-3; `d3577eb` the return `90af4af5`; `c21a25f` the comparator runs) — **not on `main`**; it lands with HK-5 together with the chat-side estate `g_vs1_gate/estate/`. `refs/heads/claude/new-session-7flqwf` = `1360578` (retained; fully merged). No canonical ledger on `main`.

## Project store

`claude/staging_memo_G_VS1_v1.md` (the superseded v1 draft, `bfe0336a`) deleted from the project store on the author's word (this directive) before the swap; the v1 draft remains in the estate and on `main` after HK-5 (`g_vs1_gate/staging_memo_G_VS1_v1.md`, landed by CC's `82b2ff9`).

## T1

This record scans CLEAN under the gate list `324f577d` (31) and the base `05302210`.
