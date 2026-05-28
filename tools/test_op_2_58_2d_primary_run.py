"""Tests for op_2_58_2d_primary_run (Brief 10). No spec-parameter execution.

These assert the freeze gate halts in the current (unfrozen, no-construction)
state and that the spec-parameter run body is unreachable.
"""

from __future__ import annotations

import pytest

from tools.op_2_58_2d_primary_run import (
    BASES,
    BETAS,
    PRODUCTION_RUN,
    SAMPLES,
    _run_one,
    build_job_matrix,
    check_construction_available,
    main,
    verify_freeze,
)


def test_production_run_flag_is_disarmed():
    assert PRODUCTION_RUN is False


def test_freeze_verification_passes_with_stub():
    """Post-Brief-10 §6 signature stub: verify_freeze() recognises the
    committed signature and freeze date in OP_2_58_2d_staging_PREREGISTRATION.md."""
    fz = verify_freeze()
    assert fz["ok"] is True, fz
    assert fz["freeze_date"] == "2026-05-27"
    assert "AUTHORIZED_RUN_V4.11_MAY_27_2026" in (fz["freeze_signature"] or "")


def test_main_completes_without_dispatch():
    """Freeze passes; basis (b) is implemented; construction module is
    available. Without OP_2_58_2D_PROOF_OF_LIFE, main() reaches end-of-flow
    (queues the 42-run schedule, dispatches nothing) and returns 0."""
    import os
    os.environ.pop("OP_2_58_2D_PROOF_OF_LIFE", None)
    assert main() == 0


def test_job_matrix_is_42_runs():
    jobs = build_job_matrix()
    assert len(jobs) == len(BETAS) * len(SAMPLES) * len(BASES) == 42


def test_construction_preconditions_met():
    """Post-Brief-10.5 + basis-(b) candidate implementation: construction
    module is importable and basis (b) probes successfully."""
    con = check_construction_available()
    assert con["basis_b_ready"] is True, con
    assert con["construction_ready"] is True, con
    assert con["blockers"] == []


def test_run_one_refuses_without_verified_freeze():
    with pytest.raises(RuntimeError, match="freeze not verified"):
        _run_one({"beta": 20, "sample": SAMPLES[0], "basis": BASES[0]},
                 freeze={"ok": False})


def test_run_one_refuses_when_neither_gate_armed():
    """Freeze ok but PRODUCTION_RUN=False and proof_of_life not requested:
    still refuses (the §4.1 audit anchor)."""
    with pytest.raises(RuntimeError, match="PRODUCTION_RUN"):
        _run_one({"beta": 20, "sample": SAMPLES[0], "basis": BASES[0]},
                 freeze={"ok": True})
