# OP-2.58.2d primary-run audit log

**Append-only.** Once written, an entry is never edited (brief §3.2, §4.7).
Errors are corrected by appending a correction entry, never by in-place edit.

**Brief:** CLAUDE_CODE_BRIEF_10_OP_2_58_2D_PRIMARY_RUN.md
**Branch:** `claude/nextgen-crypto-testspace-bhwUO`
**Anchor commit (pre-run):** `bd26452` (head of the Brief-09 chain)
**Orchestrator:** `tools/op_2_58_2d_primary_run.py`

---

### Entry 001 — Pre-run freeze verification (brief §2.1)

Timestamp: 2026-05-27T22:23:59Z

**Result: FREEZE VERIFICATION FAILED → HALT. The primary run did not begin. No
spec-parameter code path was executed.**

§2.1 step 1–3 require the frozen pre-registration
`OP_2_58_2d_staging_PREREGISTRATION.md` to be present with a §6 freeze date
(`YYYY-MM-DD`) and freeze signature (not `[pending]`). The orchestrator's first
action (`verify_freeze()`) searched the repo and its candidate locations and
found **no pre-registration file**:

> frozen pre-registration OP_2_58_2d_staging_PREREGISTRATION.md not found in
> repo (searched: OP_2_58_2d_staging_PREREGISTRATION.md,
> tools/OP_2_58_2d_staging_PREREGISTRATION.md,
> reports/OP_2_58_2d_staging_PREREGISTRATION.md). It is session-side and was
> never committed; there is no frozen §6 to verify.

The pre-registration has been session-side throughout Briefs 07–09 (Claude Code
produced patch *recommendations*; the session held and edited the document).
With no committed Rev 5 / frozen §6 in the repo, the freeze cannot be verified
and — per brief §2.1 step 3 and §2.2 — the script **exits non-zero (code 1)
before any spec-parameter construction is reachable.** The `production_run`
audit anchor (brief §4.1) was never armed; `_run_one` was never called.

**Toolchain versions (brief §3.2 Entry 001 requirement):**
- fpylll 0.6.4 (`float_type="ld"` honored)
- Python 3.11.15
- OS: Linux 6.18.5

**§2.2 toolchain re-verification (recorded; all PASS — the tool-chain is not the
blocker):**
- (2) `op_2_58_2d_lattice_attack.py` — 14-test suite: PASS
- (3) `op_2_58_2d_classifier.py` — 9-test suite: PASS
- (4) `op_2_58_2d_bkz_smoke.py` — 11-test suite: PASS (34 toy tests total)
- (5) D1 F_L-union rank at q = 4,294,977,961: **14** (reproduces; expected 14)
- (1) fpylll importable, `ld` precision honored: PASS

**Additional preconditions (also unmet — recorded for the audit trail; these
are independent of the freeze blocker and each independently blocks Items 3–5):**
- **No §2.58.B construction artifact** exists in the repo. `gen_toy_instance`
  produces generic synthetic LWE, not the §2.58.B Fano-line-structured spec
  instance the primary run must attack. There is nothing to attack at spec
  parameters.
- **Basis (b) Fano-projected lattice is unimplemented** —
  `build_fano_projected_lattice` raises `NotImplementedError` ("post-freeze;
  depends on §2.58.B Fano-line subspace data"). 21 of the 42 scheduled runs
  (all basis-(b) runs) cannot execute even past the freeze gate.
- The frozen pre-reg's §5.x declaration text, §4.2 budget, §4.3 decision tree,
  and §4.4 early-termination rule are likewise session-side and unavailable, so
  no closure could quote them verbatim even if runs had executed.

---

### Entry 002 — Resource plan

**N/A — not reached.** Entry 002 (resource plan, parallelization, projected
end-date, audit-log integrity key) is written only after a successful Entry 001
freeze verification. Entry 001 halted; no resource plan was established and no
audit-log integrity key (hash of freeze signature + start-date) could be
computed, because there is no freeze signature.

---

### Entries 003+ — Per-run records

**None.** Zero of the 42 scheduled runs executed. No spec-parameter BKZ run was
dispatched. There are no per-run records to append, and (per the append-only
discipline) none will be fabricated.

---

### Status — HALT-AND-SURFACE (brief §2.1, §3.3, §9)

The primary run is blocked at the freeze gate and is surfaced to the session.
No §5.x outcome can be declared: the schedule did not run, so there is no result
to file. Per brief §9, this is not a pre-registration revision and not a §3.*
retraction — it is the freeze gate working as designed: the run cannot begin
until the frozen Rev 5 pre-registration (and the §2.58.B construction + basis
(b) implementation) are present in the repo.

**To unblock (session actions required, outside this brief's authority):**
1. Commit the frozen Rev 5 `OP_2_58_2d_staging_PREREGISTRATION.md` with a real
   §6 freeze date and signature.
2. Provide the §2.58.B spec-parameter construction (instance generator / public
   data) the run is to attack.
3. Provide the §2.58.B Fano-line subspace data so basis (b) can be implemented.

Until then, `op_2_58_2d_closure.md` and the closure ledger entry (Items 4–5) are
intentionally **not** produced — declaring a §5.x security outcome with zero
executed runs would be a fabricated result and a §3.*-grade integrity violation.
