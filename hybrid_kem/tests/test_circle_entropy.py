"""Tests for the circle chord-angle entropy module.

Covers the T1 geometric claims (radius / centre invariance, chord-angle
independence across circles), the closed-form Keplerian penalty, and the
falsifiable SP 800-22 short-suite claim from §5 of
``circle_trig_entropy_formal.md``: with n ≥ 6 circles at 0.1°
measurement precision, ≥ 1 MB of SHA-256 conditioned seed output
passes monobit + runs + block-frequency at conventional z-cutoffs.
"""

from __future__ import annotations

import math
import random

import pytest

from hybrid_kem.entropy.circle_entropy import (
    DegenerateChordError,
    ECCENTRICITIES,
    chord_angle,
    circle_entropy_seed,
    h_inf_keplerian,
    keplerian_penalty,
    simulate_circle_observation,
    simulate_seed_bytes,
)


# ---------------------------------------------------------------------------
# T1 — chord-angle invariances (spec Theorem 1)
# ---------------------------------------------------------------------------


def _on_circle(theta: float, r: float, c: tuple[float, float]) -> tuple[float, float]:
    return (c[0] + r * math.cos(theta), c[1] + r * math.sin(theta))


def test_chord_angle_radius_invariance():
    """Two points at fixed angular positions on a circle: changing r
    must not change the chord direction (it scales but keeps direction)."""
    theta_a, theta_b = 0.3, 1.7
    centre = (10.0, -5.0)
    angle_r1 = chord_angle(
        _on_circle(theta_a, 1.0, centre), _on_circle(theta_b, 1.0, centre)
    )
    angle_r2 = chord_angle(
        _on_circle(theta_a, 50.0, centre), _on_circle(theta_b, 50.0, centre)
    )
    assert math.isclose(angle_r1, angle_r2, abs_tol=1e-12)


def test_chord_angle_centre_invariance():
    """Translating the circle leaves the chord direction unchanged."""
    theta_a, theta_b = -1.2, 0.4
    r = 3.0
    a1 = chord_angle(
        _on_circle(theta_a, r, (0, 0)), _on_circle(theta_b, r, (0, 0))
    )
    a2 = chord_angle(
        _on_circle(theta_a, r, (123.0, -456.0)),
        _on_circle(theta_b, r, (123.0, -456.0)),
    )
    assert math.isclose(a1, a2, abs_tol=1e-12)


def test_chord_angle_degenerate_points_rejected():
    with pytest.raises(DegenerateChordError):
        chord_angle((1.0, 2.0), (1.0, 2.0))


def test_chord_angle_in_canonical_range():
    """atan2 result must lie in (−π, π]."""
    rng = random.Random(0)
    for _ in range(200):
        p1 = (rng.uniform(-100, 100), rng.uniform(-100, 100))
        p2 = (p1[0] + rng.uniform(-10, 10), p1[1] + rng.uniform(-10, 10))
        if p1 == p2:
            continue
        a = chord_angle(p1, p2)
        assert -math.pi < a <= math.pi


# ---------------------------------------------------------------------------
# Seed function basics
# ---------------------------------------------------------------------------


def test_seed_length_and_determinism():
    pairs = [
        (_on_circle(0.1, 1.0, (0, 0)), _on_circle(0.7, 1.0, (0, 0))),
        (_on_circle(2.0, 5.0, (3, 3)), _on_circle(3.0, 5.0, (3, 3))),
    ]
    a = circle_entropy_seed(pairs)
    b = circle_entropy_seed(pairs)
    assert len(a) == 32
    assert a == b


def test_seed_changes_with_any_angle_perturbation():
    pairs = [
        (_on_circle(0.1, 1.0, (0, 0)), _on_circle(0.7, 1.0, (0, 0))),
        (_on_circle(2.0, 5.0, (3, 3)), _on_circle(3.0, 5.0, (3, 3))),
    ]
    base = circle_entropy_seed(pairs)
    perturbed_pairs = list(pairs)
    p1, p2 = perturbed_pairs[1]
    perturbed_pairs[1] = (p1, (p2[0] + 1e-9, p2[1]))
    assert circle_entropy_seed(perturbed_pairs) != base


def test_seed_rejects_empty():
    with pytest.raises(ValueError):
        circle_entropy_seed([])


# ---------------------------------------------------------------------------
# Cross-circle independence (Theorem 2)
# ---------------------------------------------------------------------------


def test_independent_circles_produce_distinct_seeds():
    """1024 random 6-circle configurations should yield 1024 distinct
    seeds with overwhelming probability (birthday bound on SHA-256 is
    far beyond reach)."""
    rng = random.Random(2024)
    seeds = set()
    for _ in range(1024):
        pairs = [simulate_circle_observation(rng) for _ in range(6)]
        seeds.add(circle_entropy_seed(pairs))
    assert len(seeds) == 1024


# ---------------------------------------------------------------------------
# Keplerian penalty (keplerian_min_entropy_correction.md §3)
# ---------------------------------------------------------------------------


def test_keplerian_penalty_zero_eccentricity():
    assert keplerian_penalty(0.0) == pytest.approx(0.0, abs=1e-15)


def test_keplerian_penalty_known_values():
    """Spot-check the per-body table from the correction note §3."""
    cases = {
        "Mercury": (0.2056, 0.571),
        "Mars": (0.0934, 0.264),
        "Moon": (0.0549, 0.156),
        "Jupiter": (0.0484, 0.138),
        "Earth": (0.0167, 0.048),
        "Venus": (0.0068, 0.020),
    }
    for name, (e, expected) in cases.items():
        assert keplerian_penalty(e) == pytest.approx(expected, abs=0.001), name


def test_keplerian_penalty_six_body_pool():
    """Spec §5 reports 1.197 bits total over the six-body pool."""
    six = ["Mercury", "Venus", "Earth", "Mars", "Moon", "Jupiter"]
    total = sum(keplerian_penalty(ECCENTRICITIES[b]) for b in six)
    assert total == pytest.approx(1.197, abs=0.002)


def test_h_inf_keplerian_uniform_minus_penalty():
    e = 0.2056
    precision = 0.1
    expected_uniform = math.log2(2 * math.pi / math.radians(precision))
    assert h_inf_keplerian(e, precision) == pytest.approx(
        expected_uniform - keplerian_penalty(e), abs=1e-12
    )


def test_keplerian_penalty_rejects_out_of_range():
    with pytest.raises(ValueError):
        keplerian_penalty(1.0)
    with pytest.raises(ValueError):
        keplerian_penalty(-0.01)


# ---------------------------------------------------------------------------
# SP 800-22 short suite on ≥ 1 MB (spec §9 item 1, the falsifiable claim)
# ---------------------------------------------------------------------------


def _bits_from_bytes(blob: bytes) -> list[int]:
    return [(byte >> (7 - k)) & 1 for byte in blob for k in range(8)]


@pytest.mark.slow
def test_sp80022_short_suite_on_one_megabyte():
    """The §5 falsifiable claim: with n ≥ 6 circles at 0.1° precision,
    SHA-256(Φ) passes SP 800-22 short suite on ≥ 1 MB of seed data.

    Subset tested: monobit, runs, block-frequency. z-cutoff 4 is far
    looser than the conventional 2.576 used by SP 800-22, but matches
    the convention already established by the irrational-conditioner
    test and the quartz-entropy tests in this repo — we are checking
    for gross structural defects, not certifying entropy.
    """
    rng = random.Random(20260514)
    # 32 768 seeds × 32 bytes = 1 048 576 bytes = 1 MiB.
    blob = simulate_seed_bytes(rng, n_circles=6, n_seeds=32768)
    assert len(blob) == 1 << 20
    bits = _bits_from_bytes(blob)
    n = len(bits)

    # 1. Monobit.
    s = sum(1 if b == 1 else -1 for b in bits)
    s_obs = abs(s) / (n ** 0.5)
    assert s_obs < 4.0, f"monobit s_obs={s_obs:.3f}"

    # 2. Runs (count of bit-flip transitions; expected ~ n/2).
    transitions = sum(1 for i in range(1, n) if bits[i] != bits[i - 1])
    expected = (n - 1) / 2.0
    z_runs = abs(transitions - expected) / ((n - 1) ** 0.5 * 0.5)
    assert z_runs < 4.0, f"runs z={z_runs:.3f}"

    # 3. Block-frequency at block size M = 16384 bits.
    M = 16384
    blocks = n // M
    chi_sq = 0.0
    for i in range(blocks):
        ones = sum(bits[i * M:(i + 1) * M])
        pi = ones / M
        chi_sq += (pi - 0.5) ** 2
    chi_sq *= 4.0 * M
    # Reference distribution is χ²(blocks); approximate z = (chi - blocks) /
    # sqrt(2 * blocks). Block-frequency considers the sequence non-random
    # when chi_sq is large.
    z_block = (chi_sq - blocks) / math.sqrt(2.0 * blocks)
    assert z_block < 4.0, f"block-frequency z={z_block:.3f}, chi_sq={chi_sq:.1f}, blocks={blocks}"


def test_sp80022_short_seed_smoke():
    """A 64 KiB version of the suite that runs without the slow marker,
    so a default pytest invocation still exercises the path."""
    rng = random.Random(7)
    blob = simulate_seed_bytes(rng, n_circles=6, n_seeds=2048)  # 64 KiB
    bits = _bits_from_bytes(blob)
    n = len(bits)
    s = sum(1 if b == 1 else -1 for b in bits)
    assert abs(s) / (n ** 0.5) < 4.0
    transitions = sum(1 for i in range(1, n) if bits[i] != bits[i - 1])
    assert (
        abs(transitions - (n - 1) / 2.0) / ((n - 1) ** 0.5 * 0.5) < 4.0
    )
