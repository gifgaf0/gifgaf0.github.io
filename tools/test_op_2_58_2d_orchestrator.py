"""Tests for op_2_58_2d_orchestrator (Brief 11 Item 4 lane/checkpoint/audit).

Validates the orchestrator plumbing against the mock target end-to-end:
  - 6-lane parallel dispatch over the 42-job matrix.
  - Per-run completion ledger (idempotent restart).
  - Per-tour basis checkpoint (mock writes 3 tour files per run).
  - Audit-log writer with fsync (Entry 001 + per-run entries).
  - Per-run 7-day cap enforced off persisted accumulated_compute_s.
  - Global 30-day ceiling enforcement.
  - β-monotonic lane semantics.
  - Ephemeral-environment guard refuses binding launch.
"""

from __future__ import annotations

import os
import tempfile

import pytest

from tools.op_2_58_2d_orchestrator import (
    BASES,
    BETAS,
    GLOBAL_CEILING_SECONDS,
    PER_RUN_CAP_SECONDS,
    SAMPLES,
    AuditLog,
    EphemeralEnvironmentRefused,
    Ledger,
    detect_ephemeral_environment,
    emit_launch_command,
    mock_runner,
    run_binding,
    run_mock,
)


# -- Mock end-to-end -------------------------------------------------------


def test_run_mock_completes_all_42_jobs():
    """The mock dispatch should complete all 7×3×2=42 jobs and produce
    ledger + audit log + checkpoints with correct shape."""
    with tempfile.TemporaryDirectory() as tmp:
        res = run_mock(run_dir=tmp, n_workers=6)
        assert res["n_jobs"] == 42
        assert res["n_done"] == 42, res
        assert res["n_aborted"] == 0
        assert os.path.exists(res["ledger_path"])
        assert os.path.exists(res["audit_path"])
        # Each run created its checkpoint subdir with 3 tour files.
        ckpt_root = res["checkpoint_root"]
        assert os.path.isdir(ckpt_root)
        sample_run_dir = os.path.join(ckpt_root, "b20_s20260601_a-primal")
        assert os.path.isdir(sample_run_dir)
        tour_files = sorted(p for p in os.listdir(sample_run_dir)
                            if p.startswith("basis_t"))
        assert len(tour_files) == 3, tour_files


def test_audit_log_has_entry_001_authorization():
    """Entry 001 must be the authorization record with freeze_signature,
    prereg_sha256, and PRODUCTION_RUN flip per §4.3."""
    with tempfile.TemporaryDirectory() as tmp:
        run_mock(run_dir=tmp, n_workers=2)
        with open(os.path.join(tmp, "audit_log.md"), encoding="utf-8") as f:
            text = f.read()
        assert "Entry 001" in text
        assert "Authorization" in text
        assert "freeze_signature" in text
        assert "prereg_sha256" in text
        assert "PRODUCTION_RUN: True" in text
        assert "binding_q: 4294977961" in text


def test_audit_log_one_entry_per_run():
    """42 runs ⇒ 43 entries (001 authorization + 42 per-run)."""
    with tempfile.TemporaryDirectory() as tmp:
        run_mock(run_dir=tmp, n_workers=4)
        with open(os.path.join(tmp, "audit_log.md"), encoding="utf-8") as f:
            text = f.read()
        # Count entry headers
        entry_count = text.count("\n## Entry ")
        assert entry_count == 43, entry_count


# -- Ledger idempotent restart --------------------------------------------


def test_ledger_idempotent_restart_skips_done():
    """A second invocation against the same run_dir must not re-run any
    completed (β, sample, basis) — the ledger is the source of truth."""
    with tempfile.TemporaryDirectory() as tmp:
        run_mock(run_dir=tmp, n_workers=4)
        # Pin the audit-log size BEFORE the second invocation.
        first_log_size = os.path.getsize(os.path.join(tmp, "audit_log.md"))
        # Re-invoke — should be a no-op for already-done runs.
        res = run_mock(run_dir=tmp, n_workers=4)
        assert res["n_done"] == 42
        # Audit log GREW because Entry 001 is re-written each invocation
        # (mock convention), but no new per-run entries should appear since
        # all jobs are done. The growth is bounded by ONE Entry 001 block.
        second_log_size = os.path.getsize(os.path.join(tmp, "audit_log.md"))
        growth = second_log_size - first_log_size
        # Entry 001 is ~500 bytes; 42 per-run entries would be ~12kB.
        assert growth < 1500, f"unexpected log growth {growth}B suggests re-runs"


# -- Per-run cap and global ceiling enforcement ---------------------------


def _slow_mock_runner(beta, sample, basis, ckpt_dir, acc_s):
    """Stand-in that reports very large accumulated_compute_s to trigger the
    per-run cap. Used to verify the cap actually fires."""
    return {"shortest_norm": 1.0, "pair_recovery": 0.05, "sigma_stat": 0.1,
            "accumulated_compute_s": PER_RUN_CAP_SECONDS + 1.0}


def test_per_run_cap_aborts_lane():
    """If a runner reports accumulated_compute_s > 7-day cap, the lane
    must abort and subsequent β's in the same lane must not run."""
    with tempfile.TemporaryDirectory() as tmp:
        from itertools import product
        ledger = Ledger(os.path.join(tmp, "completion_ledger.json"))
        audit = AuditLog(os.path.join(tmp, "audit_log.md"))
        jobs = list(product(BETAS, SAMPLES, BASES))
        ledger.initialize_schedule(jobs)
        counter = {"n": 0}
        # Run ONE lane synchronously with the slow runner.
        from tools.op_2_58_2d_orchestrator import _run_lane
        _run_lane(SAMPLES[0], BASES[0], BETAS, _slow_mock_runner,
                  ledger, audit, os.path.join(tmp, "ckpt"),
                  GLOBAL_CEILING_SECONDS, PER_RUN_CAP_SECONDS, counter)
        # β=20 should be aborted; β≥30 in this lane must remain pending.
        s20 = ledger.get(20, SAMPLES[0], BASES[0])
        s30 = ledger.get(30, SAMPLES[0], BASES[0])
        assert s20.status == "aborted", s20
        assert s30.status == "pending", s30


def test_global_ceiling_aborts_lane_at_next_step():
    """If global accumulated_compute_s exceeds the 30-day ceiling, the
    next β in the next lane stage aborts before dispatch."""
    with tempfile.TemporaryDirectory() as tmp:
        from itertools import product
        ledger = Ledger(os.path.join(tmp, "completion_ledger.json"))
        audit = AuditLog(os.path.join(tmp, "audit_log.md"))
        jobs = list(product(BETAS, SAMPLES, BASES))
        ledger.initialize_schedule(jobs)
        # Pre-poison the ledger with accumulated compute beyond the ceiling.
        ledger.update(20, SAMPLES[0], BASES[0], status="done",
                      accumulated_compute_s=GLOBAL_CEILING_SECONDS + 1.0)
        # Next β in the same lane must abort due to global ceiling.
        from tools.op_2_58_2d_orchestrator import _run_lane
        counter = {"n": 0}
        _run_lane(SAMPLES[0], BASES[0], BETAS, mock_runner,
                  ledger, audit, os.path.join(tmp, "ckpt"),
                  GLOBAL_CEILING_SECONDS, PER_RUN_CAP_SECONDS, counter)
        # β=30 must have aborted.
        s30 = ledger.get(30, SAMPLES[0], BASES[0])
        assert s30.status == "aborted"
        assert "ceiling" in (s30.abort_reason or "")


# -- Ephemeral environment guard ------------------------------------------


def test_detect_ephemeral_finds_managed_remote():
    """In this managed-remote container the detector must report ephemeral."""
    env = detect_ephemeral_environment()
    assert env["is_ephemeral"] is True, env
    assert env["reasons"], "must list at least one reason"


def test_run_binding_refuses_ephemeral_without_override():
    """The binding-launch entry must raise EphemeralEnvironmentRefused when
    invoked from a managed-remote container."""
    with tempfile.TemporaryDirectory() as tmp:
        with pytest.raises(EphemeralEnvironmentRefused, match="ephemeral"):
            run_binding(prereg_path="OP_2_58_2d_staging_PREREGISTRATION.md",
                        run_dir=tmp, n_workers=2, allow_ephemeral=False)


# -- Launch command emission ----------------------------------------------


def test_emit_launch_command_contains_required_steps():
    """The emitted command must include: pre-flight invocation, mock
    validation, the actual launch, and audit-log tail instructions."""
    cmd = emit_launch_command(
        prereg_path="OP_2_58_2d_staging_PREREGISTRATION.md",
        run_dir="/var/op_2_58_2d_run",
        n_workers=8,
    )
    assert "op_2_58_2d_bkz_driver.py" in cmd, "pre-flight step missing"
    assert "run_mock" in cmd, "mock validation step missing"
    assert "op_2_58_2d_orchestrator" in cmd, "actual launch missing"
    assert "tail -f" in cmd, "audit-log tail instruction missing"
    assert "PRODUCTION_RUN" in cmd or "Brief 11" in cmd, "Brief context missing"
    assert "sha256" in cmd.lower(), "prereg sha256 reference missing"
