"""Two-point circle chord-angle entropy (circle_trig_entropy_formal §1–§8).

EXPERIMENTAL conditioner-layer entropy source. Each pair of points on a
circle yields one radius-invariant, center-invariant angle φ = atan2(Δy,
Δx). n geometrically independent circles produce n independent angles;
the concatenation under SHA-256 is the conditioned seed.

NOT a primary entropy source. Same architectural position as
:class:`IrrationalConditioner` (Brief 03): upstream of the DRBG, downstream
of SP 800-90B health tests, never a replacement for a vetted noise source.

The implementation also exposes the closed-form Keplerian min-entropy
penalty Penalty(e) = log₂((1+e)² / √(1−e²)) bits from
keplerian_min_entropy_correction.md §2, and a small ``simulate_*``
helper used by the SP 800-22 short-suite test.

CORRECT usage::

    pairs = observe_six_celestial_bodies()   # external observation
    seed = circle_entropy_seed(pairs)
    drbg.instantiate(entropy_input=raw_entropy_bytes,
                     personalization=seed)

WRONG usage (the seed is a *conditioner*, not entropy)::

    drbg.instantiate(entropy_input=circle_entropy_seed(pairs))

If an adversary has the ephemeris and the observation timestamp, the
chord-angle vector is recoverable up to measurement precision; the
genuine entropy contribution is the sub-precision measurement jitter,
not the angles themselves.
"""

from __future__ import annotations

import hashlib
import math
import struct
from typing import Iterable, Sequence, Tuple

PointPair = Tuple[Tuple[float, float], Tuple[float, float]]


# ---------------------------------------------------------------------------
# Eccentricities used by the Keplerian penalty (NASA fact-sheet values).
# Same numbers as keplerian_min_entropy_correction.md §7.
# ---------------------------------------------------------------------------

ECCENTRICITIES = {
    "Mercury": 0.2056,
    "Venus": 0.0068,
    "Earth": 0.0167,
    "Mars": 0.0934,
    "Jupiter": 0.0484,
    "Saturn": 0.0542,
    "Moon": 0.0549,
}


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class DegenerateChordError(ValueError):
    """Raised when a point pair coincides and the chord direction is undefined."""


# ---------------------------------------------------------------------------
# Core chord-angle extraction (spec §1, §8)
# ---------------------------------------------------------------------------


def chord_angle(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Return the chord direction atan2(Δy, Δx) ∈ (−π, π] for the segment p1→p2.

    Radius and center cancel by Theorem 1: subtracting the two
    on-circle equations eliminates (h, k) and r, leaving only the
    coordinate differences.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx == 0.0 and dy == 0.0:
        raise DegenerateChordError("points are identical; chord undefined")
    return math.atan2(dy, dx)


def circle_entropy_seed(point_pairs: Sequence[PointPair]) -> bytes:
    """Hash n chord angles into a 32-byte conditioner seed (spec §8).

    Each angle is serialised at full IEEE 754 precision (17g) and tagged
    by its circle index so two configurations that happen to share
    angles in a different order produce distinct seeds.
    """
    if not point_pairs:
        raise ValueError("at least one point pair required")
    raw = bytearray(b"circle_entropy_v1|")
    for i, (p1, p2) in enumerate(point_pairs):
        phi = chord_angle(p1, p2)
        raw += f"C{i}:{phi:.17g}|".encode("ascii")
    return hashlib.sha256(bytes(raw)).digest()


# ---------------------------------------------------------------------------
# Keplerian min-entropy correction (keplerian_min_entropy_correction.md §2)
# ---------------------------------------------------------------------------


def keplerian_penalty(eccentricity: float) -> float:
    """Min-entropy bits to subtract from the uniform H∞ estimate.

    Penalty(e) = log₂((1+e)² / √(1−e²)). Precision-independent.
    Valid for 0 ≤ e < 1.
    """
    if not 0.0 <= eccentricity < 1.0:
        raise ValueError("eccentricity must be in [0, 1)")
    return math.log2((1 + eccentricity) ** 2 / math.sqrt(1 - eccentricity ** 2))


def h_inf_keplerian(eccentricity: float, precision_deg: float) -> float:
    """Corrected H∞ for one Keplerian orbit at given angular precision."""
    if precision_deg <= 0:
        raise ValueError("precision_deg must be positive")
    eps_rad = math.radians(precision_deg)
    h_uniform = math.log2(2 * math.pi / eps_rad)
    return h_uniform - keplerian_penalty(eccentricity)


# ---------------------------------------------------------------------------
# Simulator for SP 800-22 testing (spec §9 item 1)
# ---------------------------------------------------------------------------


def simulate_circle_observation(
    rng,
    radius_range: Tuple[float, float] = (1.0, 100.0),
    center_range: Tuple[float, float] = (-1000.0, 1000.0),
    angle_noise_rad: float = math.radians(0.1),
) -> PointPair:
    """Simulate one circle and two noisy observations on it.

    The circle has a random radius and centre drawn uniformly from the
    supplied ranges. Two points are sampled at independent uniform
    angles, then perturbed by a Gaussian whose standard deviation
    matches the spec's 0.1° measurement-precision case (§4 case A).
    Returns the noisy (x, y) coordinates of the two observations.
    """
    r = rng.uniform(*radius_range)
    cx = rng.uniform(*center_range)
    cy = rng.uniform(*center_range)
    pts = []
    for _ in range(2):
        theta = rng.uniform(0.0, 2 * math.pi)
        x = cx + r * math.cos(theta) + rng.gauss(0.0, angle_noise_rad * r)
        y = cy + r * math.sin(theta) + rng.gauss(0.0, angle_noise_rad * r)
        pts.append((x, y))
    return pts[0], pts[1]


def simulate_seed_bytes(
    rng,
    *,
    n_circles: int = 6,
    n_seeds: int,
) -> bytes:
    """Generate ``n_seeds`` independent circle configurations and return
    the concatenated SHA-256 outputs as ``n_seeds * 32`` bytes.

    Used by the SP 800-22 short-suite test. Each configuration's seed
    is fully independent — no shared circles across iterations.
    """
    if n_seeds <= 0:
        raise ValueError("n_seeds must be positive")
    chunks = []
    for _ in range(n_seeds):
        pairs = [simulate_circle_observation(rng) for _ in range(n_circles)]
        chunks.append(circle_entropy_seed(pairs))
    return b"".join(chunks)


__all__ = [
    "DegenerateChordError",
    "ECCENTRICITIES",
    "chord_angle",
    "circle_entropy_seed",
    "h_inf_keplerian",
    "keplerian_penalty",
    "simulate_circle_observation",
    "simulate_seed_bytes",
]
