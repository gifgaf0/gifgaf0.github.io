"""Tests for op_2_58_2d_bkz_driver (Brief 11 Item 2 pre-flight gates).

Locks all four pre-reg / Brief-11 pre-flight assertions so a future refactor
cannot silently flip them:
  - float_type="ld" guard refuses any other float_type.
  - exact-q assertion fails on 2**32 and any non-pinned value.
  - −A_scalarᵀ round-trip exact at both q=911 and q=SPEC_Q.
  - PRODUCTION_RUN spec-parameter gate is enforced via the sys.modules lookup.
"""

from __future__ import annotations

import pytest

from tools.op_2_58_2d_bkz_driver import (
    SPEC_Q,
    FloatTypeRefused,
    ModulusRefused,
    _assert_ld,
    assert_spec_gate_enforced,
    assert_spec_q,
    round_trip_check,
    run_preflight,
)


# -- 2a: float_type="ld" guard --------------------------------------------


def test_float_type_ld_accepted():
    _assert_ld("ld")  # should not raise


@pytest.mark.parametrize("ft", ["d", "double", "dpe", "mpfr", None, "long_double"])
def test_float_type_other_rejected(ft):
    with pytest.raises(FloatTypeRefused, match="float_type='ld'"):
        _assert_ld(ft)


# -- 2c: exact-q assertion ------------------------------------------------


def test_exact_q_pinned_value_passes():
    assert_spec_q(SPEC_Q)  # 4_294_977_961


def test_exact_q_rejects_2_to_32():
    """The most likely shorthand-confusion: 2**32 = 4_294_967_296 is NOT
    the pinned modulus (off by 10665). Must be rejected loudly."""
    with pytest.raises(ModulusRefused, match="shorthand"):
        assert_spec_q(2 ** 32)


@pytest.mark.parametrize("q_bad", [911, 4_294_967_295, 4_294_967_311, 4_294_977_962])
def test_exact_q_rejects_other_values(q_bad):
    with pytest.raises(ModulusRefused):
        assert_spec_q(q_bad)


# -- 2b: −A_scalarᵀ round-trip --------------------------------------------


def test_round_trip_at_toy_q():
    """At q=911 k=7 the primal basis z·B must equal (e, s, 1) exactly."""
    r = round_trip_check(q=911, k=7)
    assert r["pass"] is True
    assert r["N_lat"] == 2 * 7 * 16 + 1  # 225
    assert r["reconstructed_matches_target"] is True


def test_round_trip_at_spec_q():
    """At q=SPEC_Q the round-trip must hold too (uses k=4 for speed; the
    construction is k-independent so a smaller k suffices for the algebraic
    round-trip property)."""
    r = round_trip_check(q=SPEC_Q, k=4)
    assert r["pass"] is True
    assert r["N_lat"] == 2 * 4 * 16 + 1  # 129
    assert r["reconstructed_matches_target"] is True


# -- 2d: PRODUCTION_RUN gate-enforcement ----------------------------------


def test_spec_gate_enforced():
    """The spec-parameter gate must refuse gen_toy_instance(q=SPEC_Q, ...)
    with allow_spec_params=False — verified via the sys.modules lookup
    pattern (a naive isinstance against the bare-imported SpecParamsRefused
    would silently fail due to the dual-class-object problem)."""
    assert_spec_gate_enforced()  # raises if not enforced


# -- Aggregated pre-flight -------------------------------------------------


def test_run_preflight_all_pass():
    """run_preflight() runs all four gates and returns PASS for each.
    This is what the orchestrator calls before flipping PRODUCTION_RUN."""
    res = run_preflight(verbose=False)
    assert res["float_type_ld_guard"] == "PASS"
    assert res["exact_q_assertion"] == "PASS"
    assert res["production_run_gate_enforced"] == "PASS"
    assert res["round_trip_q_toy"]["pass"] is True
    assert res["round_trip_q_spec"]["pass"] is True
