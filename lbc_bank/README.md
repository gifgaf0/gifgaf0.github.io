# lbc_bank: the longitudinal-sector result (ledger V4.89) and the Phase 2 exploration

**Plain-language summary.** This folder holds the evidence for one result, plus an exploration that followed it.

- **The result.** In the program's supersolid model of the vacuum, the knots that stand for particles also couple to a second compression sound that is slower than light. Fast matter therefore sheds energy into it, and matter and light cannot share one speed limit. The ledger records this as V4.89, §2.91.V, single leg.
- **The paper.** A short negative-result paper on that finding is in `paper/`. The dispatch for an independent recomputation of the paper's numbers is in `dispatch/`.
- **The exploration (Phase 2, not on the ledger).** It screens other kinds of vacuum against the shared-speed-limit requirement. It also tests whether a three-ring ("Borromean") baryon is topologically protected. In the standard two-field class it is not.
- **Not here.** The canonical ledger is not in this repository.

## Map

| Path | What it is | Status |
|---|---|---|
| `../STATUS.md` | One-page plain-English status of the program | Current as of 4 Oct 2026 |
| `STEP1_SCOPE_CHECK.md` | Phase 1 step 1: nothing on the ledger removes the knots' density coupling, so the fold was cleared | Basis of the V4.89 fold |
| `oct3_exploration/` | The October 3 exploration: report (md5 3bb916f0), pre-compute expectation, 2D BdG weights, hydrodynamic route, 3D weights, JSON outputs, run logs | Byte-identical to the checksums cited in the report |
| `step3/` | Loss length re-evaluated on the measured 3D slow branch: still about 39 orders short. Expectation filed before computing | Cited by §2.91.V |
| `step4/` | Sweep toward melting (2D): c₂/c_T ≤ 0.78 in the supersolid phase, never 1. Coexistence boundary Λ_c ≈ 13.04 | Cited by §2.91.V |
| `external_review/` | The external reviewer's check `verify_lbc_external.py` (md5 cc12e688), and a path-adjusted runner | Cited by §2.91.V |
| `estate/` | Fold authorization (author's words verbatim), the fold script `foldin_v4_89_lbc_bank.py` (c8e9b4a5), the independent additivity check (09ae3719), and the author's brief of 3 Oct 2026 | Provenance |
| `paper/` | Draft "Second sound breaks the common light cone of a supersolid vacuum", outline and abstract, venue note, citation log, sympy identity checks, table builder | Draft; numbers awaiting the second leg |
| `dispatch/` | `LBC_SECOND_LEG_DISPATCH_INBAND.md` (md5 e5153dc527bf989eed0261e8aed91831), prepared and not run. Activation line: `ACTIVATE: LBC-2LEG-1`. Comparator (112 checks; self-test 112/112 PASS; a negative control catches injected misses), schema skeleton, T1 list and scanner, builders | Prepared, not run |
| `lit/` | Three citation-verified literature sweeps (prior art for the paper; vacuum Cherenkov and supersolid drag; solitons, q-theory and prior-address map) and `sym6_check.py` | Working notes |
| `phase2/` | Phase 2 report: shared-light-cone screen, prior-address map, three ranked questions. Also the Q1 calculation: S³ degree of Borromean configurations, Gauss linking numbers, Kauffman bracket, PSL(2,7) subgroup check | Exploration mode |
| `deps/g_tsh1_chatleg.py` | The G-TSH1 instrument the 2D scripts import (md5 621559e1). Copied from branch `claude/sqt-framework-perspectives-kMZyw`, `gate_tsh1_staging/` | Dependency of record |

## Paper supplementary index

| Label | File(s) |
|---|---|
| S1 | `oct3_exploration/lbc_weights.py` (2D BdG weights, f-sum and static sum rules) |
| S2 | `oct3_exploration/lbc_hydro.py` (static hydrodynamic route) |
| S3 | `oct3_exploration/lbc_3d.py` (3D weights) |
| S4 | `step4/lbc_sweep_low.py`, `step4/lbc_sweep_refine.py` (interaction sweep, coexistence boundary) |
| S5 | `step3/step3_loss_length.py` (loss length) |
| S6 | `paper/paper_identities_check.py` (symbolic identities), `external_review/verify_lbc_external.py` (independent re-derivation) |
| Tables | `paper/paper_tables.py` → `paper/paper_tables.json` |

## Re-running

The scripts are kept byte-identical to the versions whose checksums are cited, so they still contain the session's absolute paths. Map them as follows:

- `/home/claude/sqt_persp/gate_tsh1_staging` → `lbc_bank/deps/`
- `/home/claude/gifgaf0/gifgaf0.github.io/gtsh4_gate` → `gtsh4_gate/` at the repository root
- `/tmp/claude-0/…/scratchpad/lbc` → one working directory holding `oct3_exploration/*.py` and the `step4/` files. The sweeps import `lbc_weights` from it.
- `/home/claude/lbc_exploration` → `lbc_bank/oct3_exploration/`
- `/home/claude/bank` → `lbc_bank/step3/` and `lbc_bank/paper/`
- `/home/claude/fold` → wherever the canonical ledgers are kept (not in this repository)

`phase2/q1_degree_check.py` and `phase2/q1_group_check.py` have no path dependencies. `python3 q1_degree_check.py 128 192 256` takes about two minutes.

## Note for the second leg

The dispatch tells the second leg to work from `main` and not to read anything here except its own `lbc_bank/second_leg/` folder. The reason is that this folder holds the first leg's numbers and the paper draft in plain text.

If this branch is merged before the second leg runs, that rule still applies. The first leg's checkpoint and instruments travel only sealed, inside the dispatch (embeds E5 and E6).

## Checksums

`MANIFEST.md5` lists every file in this folder.
