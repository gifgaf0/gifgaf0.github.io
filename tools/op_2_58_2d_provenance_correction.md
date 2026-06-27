# op_2_58_2d_provenance_correction.md — Brief 11 Item 1

**Status**: Append-only branch-resident provenance correction, mirroring the
canonical ledger entry (the canonical `SQT_Master_Ledger_v4_34_CANONICAL.md`
does not live on this branch; this file is the on-branch anchor, same
pattern as `op_2_58_2d_dfr_reference.md` for §2.66.1). Filed as a positive
finding (a caught error is a result, per ledger discipline).

**Date filed**: May 28, 2026 (session date), corresponding to the
correction surfaced in Brief 11 §0.

---

## §1. The false prior-status assertion

A prior session-state record (and the memory derived from it) asserted:
> "OP-2.58.2d 42-run primary dispatched; 30-day external compute in progress."

**This was false.** No primary-run dispatch ever occurred. The assertion
appears to have crystallised from a conflation of two distinct events:
the Brief-10 proof-of-life run (k=4, β=20, σ=2.42 — quarantined as
non-binding pipeline data) and the (a)/(b)-I/(b)-II toy comparison of
Brief 10.6 (k=7, q=911 — toy ratification, not binding). Neither is the
binding §3.1 schedule; neither flipped `PRODUCTION_RUN`.

## §2. Verified ground truth (at time of Brief 11 filing)

Mechanical checks against branch state `claude/nextgen-crypto-testspace-bhwUO`:

1. **`PRODUCTION_RUN` flag** in `tools/op_2_58_2d_primary_run.py:48`:
   ```
   PRODUCTION_RUN = False
   ```
   Never flipped to `True`. The §4.1 authorization anchor is unarmed.

2. **`OP_2_58_2D_PROOF_OF_LIFE` env var**: unset across the orchestrator's
   execution history (the proof-of-life env-gate is the only path that
   bypasses the spec-Q gate without `PRODUCTION_RUN=True`, and was used
   exactly once at k=4 sub-spec for the Brief-10 pipeline demonstration).

3. **`op_2_58_2d_audit_log.md`**: does not exist on the branch (verified
   `find . -name "op_2_58_2d_audit_log*"` returns empty). The audit log is
   the artifact written at Entry 001 = authorization. Its absence is
   evidence no authorization was recorded.

4. **`op_2_58_2d_result.md`**: does not exist on the branch. The result
   doc is the post-compute closure deliverable per pre-reg §7.

5. **Git log of the OP-2.58.2d commit chain**: every commit since Brief 10
   is design/integrity/proof-of-life work; no `Entry 001` commit, no
   schedule-execution commit, no closure commit. Last commit before this
   correction:
   ```
   e6de8ad OP-2.58.2d Brief 10.7 Item 4: prefreeze report §11 — σ noise-model reconciliation closure
   ```
   The chain is pre-launch throughout.

The false assertion was not detectable from these checks until they were
performed — the same artifact-location pattern as §2.69 / §2.69.1 / §2.69.2:
a load-bearing state ("is the primary running?") that no agent could
verify against a concrete flag until one did. This correction performs
the verification and records the outcome before any new dispatch.

## §3. Regime ratification — q = 4,294,977,961 is the binding regime by design

Brief 11 §0 raises a separate clarification: the frozen pre-reg's q
(4,294,977,961) is binding **by design**, not by oversight, and is
deliberately retained despite the q=911 production-security conclusion
of the q-reversal finding.

**The two are different surfaces**:

- **OP-2.58.2d at q = 4,294,977,961** tests *structured-leakage at the
  adversary-favorable lattice*. Larger q ⇒ easier lattice (the BDD ratio
  ‖v_target‖ / gh shrinks as q grows for fixed n_eff). A null at the
  easier lattice is the **stronger null**: if BKZ cannot find the
  pair-kernel at q = 2³² where the gap is enormous, it cannot find it at
  q = 911 where the gap is smaller still relative to target norm. The
  pre-reg §3.1 pin is therefore correct for the leakage test.

- **OP-2.58.5 at q = 911** is the *concrete-security thread* — what
  modulus the deployed KEM ships with. That decision (q=911 per the
  q-reversal) is independent of the leakage-test choice and is governed
  by §2.66.1 DFR analysis at the production parameters.

Running the q = 4,294,977,961 instance executes the frozen freeze; it is
**not** a parameter change and does **not** open OP-2.58.2d.2. A future
reader encountering the q = 2³² pin in §3.1 should understand it as the
intended adversary-favorable test parameter, not as a pre-reversal
leftover that needs correcting. This ratification line forecloses that
misreading.

## §4. Consequences

- The §6 freeze stands. The full §1–§6 binding text on-branch is
  unchanged. No §3.* retraction event.
- The §4.1 `PRODUCTION_RUN` flag remains `False` until and unless Brief
  11 Items 2 and 3 clear; if they clear and the agent is on a persistent
  workstation (not an ephemeral container per §4.5), the flip is the
  single authorization act recorded as Entry 001 of the audit log.
- The ledger gains one append-only correction entry (this file mirrors
  it on-branch); no prior canonical content is modified.

## §5. Cross-references

- **Canonical (off-branch, target of the mirroring)**: the V4.34 Cluster
  M append-only correction entry filed under §2.69-family numbering
  (sibling to §2.69.1/§2.69.2/§2.69.3) for the artifact-location pattern.
- **Brief 11 §0** (CLAUDE_CODE_BRIEF_11_OP_2_58_2D_PRIMARY_RUN_DISPATCH.md):
  the brief opening this correction.
- **OP-2.58.2d Rev 5 pre-reg §3.1**: names q = 4,294,977,961 as the
  binding regime; this correction ratifies that pin as intentional.
- **OP-2.58.5**: the production-security thread at q = 911; deliberately
  distinct from this attack's regime.
- **§2.69, §2.69.1, §2.69.2, §2.69.3**: the artifact-location pattern
  this correction extends.
- **Branch state evidence**: `tools/op_2_58_2d_primary_run.py:48`,
  absence of `op_2_58_2d_audit_log.md` and `op_2_58_2d_result.md`,
  git log of the OP-2.58.2d commit chain.
