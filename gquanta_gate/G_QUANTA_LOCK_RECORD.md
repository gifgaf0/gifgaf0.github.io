# LOCK RECORD — Gate G-QUANTA (Topological Stability & Composite Quanta Discriminator)

**Locked:** September 10, 2026 (chat leg). **Author authorization (verbatim):** "I explicitly AUTHORIZE the lock of `staging_memo_G_QUANTA_v2.md`".
**Base:** `SQT_Master_Ledger_v4_81_CANONICAL.md`, md5 `b4e55aaea76a2152f7b1873309aec077`.

## 1. Frozen artifact of record

| Artifact | md5 | Size |
|---|---|---|
| `staging_memo_G_QUANTA_v2.md` | `0039d001769569297c2aa8ccbded5a3b` | 4,863 B (50 lines) |

sha256 `9979e933ddbe7ab6d3b554b1773397458ad86062ef6c157244c16dcf69b564ef`.

Frozen byte-for-byte from the author-supplied text of September 10. The file in this estate is the artifact of record; if the author's local copy hashes differently, this md5 governs and the local copy is superseded (D5 lesson from G-TSH1: the locked artifact travels in-band).

The memo's own status line still reads `DRAFT — NOT LOCKED`; that line is inside the frozen bytes and is superseded by this record. No re-lock.

## 2. Elections (T3-immutable)

- **E-Q-1 (Promotion Path): (b) Promote standalone.** The graded-base companion memo shares only the type-(b) tower claim, which this gate tests independently.
- **E-Q-2 (Dimension Perspective): (a) E-perspective (3D) for envelopes, L-perspective (2D/3D) for defects.** Extended (infinite-total-energy) defects are explicitly in scope: C2 is satisfied by a finite core size from the GP gradient-vs-interaction balance, without requiring finite global energy.

## 3. What the lock fixes

- §2 discriminator: C1 (continuous topological charge over a continuous configuration space; discrete labels over discrete spaces = NO) and C2 (Derrick-evading functional: competing dilation exponents, or a rigid geometric constraint). PASS ⇔ C1 ∧ C2.
- §3 functional inventory: Ropelength (rigid constraint), Gross–Pitaevskii (competing exponents). Nothing else qualifies at this gate.
- §4 inventory matrix: six rows, six encoded columns. **This table is the sole input to the instrument.** No verdict text exists anywhere in the memo §4 or in the instrument.
- §5 hypotheses H-Q-1..6: predictions only, quarantined from evaluation; consulted only in the `compare` step, which runs last (Eddington quarantine).
- §6 falsifiers: F-QUANTA-1 (single-scaling stable object), F-QUANTA-2 (tower rung with continuous charge + competing-term bound), F-QUANTA-3 **REGISTERED, NOT EXECUTED**.

## 4. Lock-record annotations (not memo text; author may strike before the leg runs)

Promotion conditions carried from the September 10 review and accepted in the directive:

- **PC-1 non-trivial partition:** ≥ 1 PASS and ≥ 1 FAIL.
- **PC-2 independence witness:** ≥ 1 PASS via a functional class other than the ropelength class (Rigid Constraint), so the rule is not a restatement of L_B.
- **PC-3 concordance:** machine verdicts vs H-Q-1..6, evaluated in the separate `compare` step; any discordance is a finding (demotion or a hole in the rule), not a promotion.

**O-1 (observation, no verdict effect):** the two Discrete-space rows (tower rungs, SLWE matrices) are assigned E-Perspective, which §3 defines as the 3D continuum EFT. C1 fails on `Discrete` regardless of perspective, so the verdicts are unaffected; recorded for an optional amendment.

**F-QUANTA-1 is inert-by-inventory:** the locked table declares no `Single Exponent` functional class, so F-1 cannot fire on this run. Its silence is not a test passed and will be reported as such.

## 5. Instrument (chat leg)

| Artifact | md5 | Size | State |
|---|---|---|---|
| `g_quanta_chatleg.py` v1 | `79072196cdfc480f4073195d96100d2e` | 21,156 B | self-tests 9/9 GREEN; **evaluation of record NOT run** |

Behaviour: md5-guards the memo against the lock before reading (verified: a one-byte tamper halts with exit 1, no checkpoint written); T1 self-grep of instrument + memo before evaluation and of the checkpoint after; parses §4 at run time; vocabulary-locked (unknown class/space → halt); writes E8 JSON checkpoint `g_quanta_chatleg_checkpoint.json`; `compare` writes a separate `g_quanta_chatleg_compare.json` and never modifies the checkpoint.

Self-test suites: S1 parser/normalisation · S2 C1/C2 truth table (7 cases) · S3 F-QUANTA-2 firing · S4 F-QUANTA-1 firing + inert flag · S5 PC-1/PC-2 · S6 vocabulary lock · S7 md5 guard · S8 hypothesis match · S9 T1 scan mechanics.

**T1 requirement:** the run of record needs the T1 forbidden-string list (13 pattern lines, md5 `04438b74`, per the G-2a-L1 estate) supplied as `T1_forbidden_strings.txt` beside the memo, or via `--t1 PATH`. Without it the instrument halts; `--no-t1-halt` records deviation D-T1 instead. Hits are reported by pattern index, never by text.

## 6. Execution order from here

1. Author supplies the T1 list (or elects D-T1).
2. Author word to execute → `python3 g_quanta_chatleg.py evaluate` → checkpoint md5 reported.
3. `python3 g_quanta_chatleg.py compare` (PC-3), last.
4. P-4 single-file in-band CC dispatch: memo + lock record + instrument + T1 list as byte-exact embeds; CC leg blind, own implementation of the §2 rules.
5. Two-leg comparison C1–C6; S9 on any miss.
6. Fold authorization → V4.82 (after V4.81 is in project knowledge).

Nothing has been evaluated. No checkpoint exists. No prior ledger content touched.
