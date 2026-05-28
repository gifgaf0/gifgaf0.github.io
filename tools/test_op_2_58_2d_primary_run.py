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


def test_main_halts_on_construction():
    """Freeze passes; main() halts at the construction check on basis (b)
    Fano-projected lattice unimplemented (exit code 2)."""
    assert main() == 2


def test_job_matrix_is_42_runs():
    jobs = build_job_matrix()
    assert len(jobs) == len(BETAS) * len(SAMPLES) * len(BASES) == 42


def test_construction_preconditions_unmet():
    con = check_construction_available()
    assert con["basis_b_ready"] is False
    assert any("§2.58.B" in b for b in con["blockers"])


def test_run_one_refuses_without_verified_freeze():
    with pytest.raises(RuntimeError):
        _run_one({"beta": 20, "sample": SAMPLES[0], "basis": BASES[0]},
                 freeze={"ok": False})


def test_run_one_refuses_even_if_freeze_ok_when_disarmed():
    # Freeze ok but PRODUCTION_RUN is False → still refuses (the AND guard).
    with pytest.raises(RuntimeError):
        _run_one({"beta": 20, "sample": SAMPLES[0], "basis": BASES[0]},
                 freeze={"ok": True})
