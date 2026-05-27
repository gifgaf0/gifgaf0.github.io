# OP-2.58.2d Item L1 — §2.66.2 pair-vs-line attribution cross-check

**Date:** May 27, 2026
**Brief:** CLAUDE_CODE_BRIEF_08 §2 (Item L1)
**Status:** Pre-freeze. Toy scale only; no §2.58.B execution.
**Feeds:** F1 interpretation (§3.2) and the §3.3 attribution sentence.

---

## Resolution: UNATTRIBUTABLE — in fact UNLOCATABLE

The §2.66.2 classifier-soundness numbers (65.4%, 93.0%) **cannot be attributed
to the pair vs the line classifier, because the source attribution does not
exist anywhere in this repository or its git history.** This is the §7
edge case ("L1 cannot locate the §2.66.2 attribution at all"), which is
stronger than the §2.4 "reports both numbers without a caption" case.

### What was searched (candidate locations from brief §2.2 and beyond)

| Target | Result |
|---|---|
| `SQT_Master_Ledger_v4_0_CANONICAL.md` (§2.2 location 1) | **Does not exist.** No file matching `*ledger*` or `*canonical*` anywhere in the working tree. |
| `phase_b_audit_log.md` entries 001–009 (§2.2 location 2) | **Does not exist.** No file matching `*audit_log*` or `*phase_b*`. |
| §2.66.2 classifier source (`op_2_58_2_leakage_test.py`, `op_2_58_2b_advanced_attacks.py`) | **Absent** (already recorded as Brief-07 finding F1 in `op_2_58_2d_prefreeze_report.md`). |
| Repo-wide grep for `65.4`, `93.0`, `2.66.2`, `classifier-soundness`, `signed-lift` | The only occurrences of `65.4` / `93.0` are inside `op_2_58_2d_prefreeze_report.md` itself, written as `(one of 65.4% / 93.0%)` — i.e. as *unattributed reference data carried in from the predecessor brief*, never as a captioned pair/line result. |
| `git log --all -S "65.4%"` and `-S "2.66.2"` | Both strings enter the repo for the first time at commit `766c6f5` (the Brief-07 deliverable). No earlier commit, on any branch, ever contained them. |
| `git log --all --name-only` for ledger/audit/2_66/leakage/soundness filenames | **NONE FOUND** in the entire history of any branch. |

### Verbatim quote of the §2.66.2 numbers as they appear in the repo

From `op_2_58_2d_prefreeze_report.md` (the only source):

> | pair recovery | 96.2% | (one of 65.4% / 93.0%) | 4.76% |
> | Fano-line recovery | 88.0% | (one of 65.4% / 93.0%) | 14.29% |

The "(one of …)" notation is itself the prior author's acknowledgement that the
pair/line assignment was already unknown at Brief-07 time. No primary §2.66.2
record disambiguates it.

## Required L1 statement (brief §2.3 template)

> §2.66.2's reported numbers (65.4%, 93.0%) **cannot be assigned** to the pair
> classifier or the line classifier on the classifier-soundness diagnostic
> (raw noise, no A·s mask, q = 911): the §2.66.2 source, the SQT master ledger,
> and the Phase-B audit log are all **absent from the repository and its full
> git history**. The numbers survive only as uncaptioned reference data in the
> Brief-07 prefreeze report.

## §3.3 edit string

**No change to the Rev 3 attribution can be made on evidence, because there is
no evidence.** The Rev 3 provisional attribution ("65.4% = line, 93.0% = pair")
is neither confirmable nor refutable. The correct pre-freeze action is therefore
**not** to patch in a specific attribution but to replace the attribution-
dependent sentence with the attribution-robust (b/c) framing — see Item F1,
which resolves to the (b/c) closure paragraph independently of L1 and appends
the measured 4-number matrix.

## Retraction-grade flag (brief §7)

Per brief §7, the total absence of the §2.66.2 attribution is a **§3.\*
retraction-grade finding for the §2.66.2 work itself**: the SQT thread's
reliance on §2.66.2 as a load-bearing reference (cross-attack comparability,
the 65.4%/93.0% soundness baseline) is **weaker than the Rev 3 pre-registration
assumes.** There is no ledger file in this repo to record a ledger entry into;
the finding is therefore surfaced here and escalated into the prefreeze report's
freeze section. F1 still proceeds under the §3.2 "unattributable" branch.
