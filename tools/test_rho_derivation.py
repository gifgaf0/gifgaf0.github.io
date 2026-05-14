"""Tests for tools/rho_derivation.py (Brief 08)."""

from __future__ import annotations

import math

import pytest

from tools.rho_derivation import (
    LAMBDA_P_BAR_FM,
    R_P_MUON_FM,
    compute_237_triangle,
    compute_rho,
    compute_scale_factor,
    compute_void_correction,
)


def test_area_is_pi_over_42():
    tri = compute_237_triangle()
    assert math.isclose(tri["area"], math.pi / 42.0, abs_tol=1e-10)
    assert math.isclose(tri["area"], tri["area_check"], abs_tol=1e-12)


def test_psl27_coverage_is_4pi():
    tri = compute_237_triangle()
    assert math.isclose(tri["total_angular"], 4 * math.pi, abs_tol=1e-10)


def test_r_over_r_is_4():
    tri = compute_237_triangle()
    # 168/42 = 4 exactly under IEEE 754.
    assert tri["R_over_r"] == 4.0


def test_R_hyp_value():
    tri = compute_237_triangle()
    # Spec §3.1: R_hyp = 0.324902 (to 5 dp).
    assert tri["R_hyp"] == pytest.approx(0.324902, abs=1e-5)


def test_angle_sum_below_pi():
    """Hyperbolic triangle: angle sum < π."""
    tri = compute_237_triangle()
    assert tri["angle_sum"] < math.pi


def test_cos18_identity():
    void = compute_void_correction()
    assert void["identity_check"] is True
    assert math.isclose(
        void["cos18_formula"], void["cos18_direct"], abs_tol=1e-12
    )


def test_zeta_matches_definition():
    void = compute_void_correction()
    assert math.isclose(
        void["zeta"], 1.0 - math.pi / math.sqrt(12.0), abs_tol=1e-15
    )


def test_scale_factor_is_49():
    scale = compute_scale_factor()
    # 14 * 3.5 = 49 exactly in IEEE 754.
    assert scale["L_normalized"] == 49.0
    assert scale["n_faces"] == 14
    assert scale["half_period"] == 3.5


def test_rho_structural():
    rho = compute_rho()
    # Spec §3.3: ρ_structural = 3.9800 to 4 dp.
    assert rho["rho_structural"] == pytest.approx(3.9800, abs=1e-4)


def test_rho_predicted_vs_muon():
    rho = compute_rho()
    # Spec DoD: error < 0.01%.
    assert rho["error_vs_muon_pct"] < 0.01


def test_predicted_r_p_in_femtometres():
    rho = compute_rho()
    expected = rho["rho_predicted"] * LAMBDA_P_BAR_FM
    assert math.isclose(rho["r_p_predicted_fm"], expected, abs_tol=1e-15)
    # Expected ≈ 0.84085 fm vs muonic 0.84087.
    assert abs(rho["r_p_predicted_fm"] - R_P_MUON_FM) < 1e-3


def test_no_free_parameters():
    """compute_rho() takes no arguments and is deterministic — two calls
    must produce byte-identical results."""
    a = compute_rho()
    b = compute_rho()
    assert a == b


def test_void_correction_factor_above_one():
    void = compute_void_correction()
    assert void["factor"] > 1.0
    assert void["factor"] < 1.01  # correction is small
