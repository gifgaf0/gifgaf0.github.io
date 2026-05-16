"""Proton charge radius prediction from P¹(2,3,7) Borromean circumscription.

Backs the formula in ``borromean_circumscription_derivation.md §3``:

    ρ = R_hyp × (49/4) × (1 + ζ·(1−cos18°))

No fitting. No free parameters. Every constant is computed from its
definition, except for the single physical input ``λ̄_p`` from
CODATA 2018 (used only to convert ρ to femtometres for the comparison
with muonic-hydrogen and α-matched measurements).

Run as a script (``python tools/rho_derivation.py``) to print the full
derivation and write ``reports/rho_derivation_output.txt``. Tests live
in ``tools/test_rho_derivation.py``.
"""

from __future__ import annotations

import math
import os
import sys
from typing import Any


# ---------------------------------------------------------------------------
# Constants (CODATA 2018; experimental r_p values)
# ---------------------------------------------------------------------------

# Proton reduced Compton wavelength.
# CODATA 2018: λ̄_p = ℏ / (m_p · c).
LAMBDA_P_BAR_FM = 0.21030892

# Experimental proton charge radius values.
R_P_MUON_FM = 0.84087   # Pohl et al. 2013, muonic hydrogen
R_P_ALPHA_FM = 0.83854  # α-matched value

# Derived for verification.
RHO_MUON = R_P_MUON_FM / LAMBDA_P_BAR_FM
RHO_ALPHA = R_P_ALPHA_FM / LAMBDA_P_BAR_FM


# ---------------------------------------------------------------------------
# (2,3,7) hyperbolic triangle
# ---------------------------------------------------------------------------


def compute_237_triangle() -> dict[str, Any]:
    """All geometric quantities of the (2,3,7) triangle in the K = -1 plane.

    Hyperbolic law of cosines for sides: for the side opposite angle A,
    ``cosh(a) = (cos(A) + cos(B)·cos(C)) / (sin(B)·sin(C))``.
    Hyperbolic law of sines: ``sinh(a)/sin(A) = 2·sinh(R)``, so for the
    side opposite the right angle, ``sinh(R) = sinh(a)/2``.
    """
    alpha = math.pi / 2
    beta = math.pi / 3
    gamma = math.pi / 7

    def side_opposite(A: float, B: float, C: float) -> float:
        cosh_a = (
            (math.cos(A) + math.cos(B) * math.cos(C))
            / (math.sin(B) * math.sin(C))
        )
        return math.acosh(cosh_a)

    side_a = side_opposite(alpha, beta, gamma)
    side_b = side_opposite(beta, alpha, gamma)
    side_c = side_opposite(gamma, alpha, beta)

    sinh_R = math.sinh(side_a) / 2.0
    R_hyp = math.asinh(sinh_R)

    psl27_order = 168
    domain_count = psl27_order
    area = math.pi / 42.0
    area_check = math.pi * (1.0 - 1.0 / 2.0 - 1.0 / 3.0 - 1.0 / 7.0)
    total_angular = domain_count * area
    R_over_r = domain_count / 42.0  # 168/42 = 4 exactly

    return {
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "angle_sum": alpha + beta + gamma,
        "area": area,
        "area_check": area_check,
        "side_a": side_a,
        "side_b": side_b,
        "side_c": side_c,
        "sinh_R": sinh_R,
        "R_hyp": R_hyp,
        "PSL27_order": psl27_order,
        "domain_count": domain_count,
        "total_angular": total_angular,
        "R_over_r": R_over_r,
    }


# ---------------------------------------------------------------------------
# Physical scale L = 14 × (7/2) × λ̄_p = 49 × λ̄_p
# ---------------------------------------------------------------------------


def compute_scale_factor() -> dict[str, Any]:
    """Single-mechanism Z₇-on-oriented-faces scale.

    14 = first even 7 = Császár-face count (Cayley-Dickson orientation
    doubling of Z₇). 7/2 = half the Singer period. The factor of 2 from
    orientation and the factor of 1/2 from the half-period cancel,
    leaving 49 = 7². One mechanism — Z₇ acting on the already-doubled
    oriented face structure — not two independent Z₇ actions.
    """
    n_faces = 14
    half_period = 7.0 / 2.0
    L_normalized = n_faces * half_period  # 49 exactly
    L_fm = L_normalized * LAMBDA_P_BAR_FM
    return {
        "n_faces": n_faces,
        "half_period": half_period,
        "L_normalized": L_normalized,
        "lambda_p_bar_fm": LAMBDA_P_BAR_FM,
        "L_fm": L_fm,
    }


# ---------------------------------------------------------------------------
# Void correction 1 + ζ·(1 − cos 18°)
# ---------------------------------------------------------------------------


def compute_void_correction() -> dict[str, Any]:
    """Void × void interface — ζ (hexagonal packing) × (1 − cos 18°) (pentagon).

    Verifies the closed-form identity ``cos(π/10) = √(2+φ)/2`` where
    ``φ = (1+√5)/2``. Both forms are computed; they must agree to 1e-12.
    """
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    cos18_formula = math.sqrt(2.0 + phi) / 2.0
    cos18_direct = math.cos(math.pi / 10.0)
    identity_verified = math.isclose(
        cos18_formula, cos18_direct, abs_tol=1e-12
    )

    zeta = 1.0 - math.pi / math.sqrt(12.0)
    pentagon_void = 1.0 - cos18_direct
    correction = zeta * pentagon_void
    factor = 1.0 + correction
    return {
        "phi": phi,
        "cos18_formula": cos18_formula,
        "cos18_direct": cos18_direct,
        "identity_check": identity_verified,
        "zeta": zeta,
        "pentagon_void": pentagon_void,
        "correction": correction,
        "factor": factor,
    }


# ---------------------------------------------------------------------------
# Full ρ prediction
# ---------------------------------------------------------------------------


def compute_rho() -> dict[str, Any]:
    """ρ = R_hyp × (49/4) × (1 + ζ·(1−cos18°)), no free parameters."""
    tri = compute_237_triangle()
    scale = compute_scale_factor()
    void = compute_void_correction()

    rho_structural = tri["R_hyp"] * (scale["L_normalized"] / 4.0)
    rho_predicted = rho_structural * void["factor"]
    r_p_predicted_fm = rho_predicted * LAMBDA_P_BAR_FM

    error_vs_muon_pct = abs(rho_predicted - RHO_MUON) / RHO_MUON * 100.0
    error_vs_alpha_pct = abs(rho_predicted - RHO_ALPHA) / RHO_ALPHA * 100.0
    return {
        "rho_structural": rho_structural,
        "rho_predicted": rho_predicted,
        "r_p_predicted_fm": r_p_predicted_fm,
        "rho_muon": RHO_MUON,
        "r_p_muon_fm": R_P_MUON_FM,
        "rho_alpha": RHO_ALPHA,
        "r_p_alpha_fm": R_P_ALPHA_FM,
        "error_vs_muon_pct": error_vs_muon_pct,
        "error_vs_alpha_pct": error_vs_alpha_pct,
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def _format_derivation() -> str:
    tri = compute_237_triangle()
    scale = compute_scale_factor()
    void = compute_void_correction()
    rho = compute_rho()

    lines: list[str] = []
    w = lines.append

    w("=== (2,3,7) Triangle Geometry ===")
    w(f"  alpha (π/2)              = {tri['alpha']:.12f}")
    w(f"  beta  (π/3)              = {tri['beta']:.12f}")
    w(f"  gamma (π/7)              = {tri['gamma']:.12f}")
    w(f"  angle sum                = {tri['angle_sum']:.12f}  (< π for hyp)")
    w(f"  area  (closed-form π/42) = {tri['area']:.12f}")
    w(f"  area  (1 − 1/2 − 1/3 − 1/7) × π = {tri['area_check']:.12f}")
    w(f"  side opposite π/2 (a)    = {tri['side_a']:.12f}")
    w(f"  side opposite π/3 (b)    = {tri['side_b']:.12f}")
    w(f"  side opposite π/7 (c)    = {tri['side_c']:.12f}")
    w(f"  sinh(R_hyp) = sinh(a)/2  = {tri['sinh_R']:.12f}")
    w(f"  R_hyp                    = {tri['R_hyp']:.12f}")
    w(f"  |PSL(2,7)|               = {tri['PSL27_order']}")
    w(f"  fundamental domain count = {tri['domain_count']}")
    w(f"  total angular content    = {tri['total_angular']:.12f}  ≡ 4π")
    w(f"  R/r = 168/42             = {tri['R_over_r']:.12f}  (exactly 4)")
    w("")

    w("=== Scale Factor ===")
    w(f"  n_faces (= 14, first even 7) = {scale['n_faces']}")
    w(f"  half Singer period (7/2)     = {scale['half_period']}")
    w(f"  L / λ̄_p = 14 × (7/2)         = {scale['L_normalized']}  (= 49)")
    w(f"  λ̄_p (CODATA 2018)           = {scale['lambda_p_bar_fm']:.8f} fm")
    w(f"  L  = 49 · λ̄_p               = {scale['L_fm']:.8f} fm")
    w("")

    w("=== Void Correction ===")
    w(f"  φ = (1+√5)/2                 = {void['phi']:.12f}")
    w(f"  cos(18°) via √(2+φ)/2        = {void['cos18_formula']:.12f}")
    w(f"  cos(π/10) direct             = {void['cos18_direct']:.12f}")
    w(f"  identity verified            = {void['identity_check']}")
    w(f"  ζ = 1 − π/√12                = {void['zeta']:.12f}")
    w(f"  pentagon void = 1 − cos18°   = {void['pentagon_void']:.12f}")
    w(f"  correction ζ·(1−cos18°)      = {void['correction']:.12f}")
    w(f"  factor 1 + correction        = {void['factor']:.12f}")
    w("")

    w("=== Proton Radius Prediction ===")
    w(f"  ρ_structural = R_hyp × 49/4                  = {rho['rho_structural']:.6f}")
    w(f"  ρ_predicted  = ρ_structural × (1 + ζ(1−cos18°)) = {rho['rho_predicted']:.6f}")
    w(f"  r_p          = ρ_predicted × λ̄_p             = {rho['r_p_predicted_fm']:.6f} fm")
    w(f"  vs muonic H  ρ = {rho['rho_muon']:.6f}, r_p = {rho['r_p_muon_fm']:.5f} fm "
      f"(error: {rho['error_vs_muon_pct']:.4f}%)")
    w(f"  vs α-matched ρ = {rho['rho_alpha']:.6f}, r_p = {rho['r_p_alpha_fm']:.5f} fm "
      f"(error: {rho['error_vs_alpha_pct']:.4f}%)")
    w("")

    w("=== Epistemic Summary ===")
    w("  R/r = 4:  T1  (group theory: 168 × π/42 = 4π, ratio 4π/π = 4)")
    w("  R_hyp:    T1  (hyperbolic law of sines / cosines)")
    w("  Scale:    T2  (14 × (7/2); Cayley-Dickson orientation doubling of Z₇)")
    w("  Void:     T2  (identified from principle; H²→ℝ³ derivation open)")
    w("  Formula:  T2  (no free parameters; ~0.002% from muonic H)")
    w("")
    return "\n".join(lines)


def print_derivation() -> None:
    text = _format_derivation()
    print(text)


def _write_report(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(_format_derivation())


_REPORT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "reports",
    "rho_derivation_output.txt",
)


if __name__ == "__main__":
    print_derivation()
    _write_report(_REPORT_PATH)
    print(f"[wrote {_REPORT_PATH}]", file=sys.stderr)
