"""Robust scoring layer for the capillary variance scanner.

Companion to capillary_variance.py. Replaces the mean/stddev z-scoring and
the global ``_STDDEV_FLOOR = 1e-6`` hack with robust estimators and
metric-appropriate absolute floors.

Design principle (the correction that drove this patch)
-------------------------------------------------------
The core weakness is small-sample variance estimation. With N=5 a
mean/pstdev baseline is frequently *artificially tight* -- the true jitter
simply did not appear in five draws -- so a variant subject to the same
ambient jitter scores a huge z. The 1e-6 floor is the degenerate extreme of
that same failure, not a separate bug.

This bites the two numeric metrics differently, so they are scored
differently:

  * TIMING is continuous and genuinely noisy. A deviation over a tiny
    baseline is usually a GC pause / scheduler hiccup / network blip that
    five samples missed -- real noise scored as signal. So timing uses a
    robust centre + scale AND an absolute floor: sub-floor deviations are
    never anomalous, no matter how tight the baseline looks.

  * LENGTH is often deterministic. When the body length never varies, a
    one-byte change is exactly the thing we are hunting -- flagging it is
    correct, even though a z-score there is meaningless. So length
    branches: a deterministic baseline uses an any-change rule (report the
    byte delta, not a fake z); a genuinely jittering baseline uses the
    robust z.

The unavoidable N=5 tension
---------------------------
MAD resists outliers (good for heavy-tailed latency) but collapses to zero
on small clustered samples. Range/d2 never collapses but is driven by the
extreme (bad for heavy tails). They pull opposite ways, and five samples
cannot pin the spread of a skewed distribution either way. Below
``_MAD_STABLE_N`` this module backs MAD with range/d2 -- a conservative
stopgap that widens the envelope (trading a possible miss for fewer false
alarms). The real fix is more baseline samples; raise ``--samples`` toward
15-20 and MAD becomes stable enough to stand alone.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import Callable

# ----------------------------------------------------------------------------
# Constants (these replace _STDDEV_FLOOR = 1e-6 in capillary_variance.py)
# ----------------------------------------------------------------------------

# Scale factor making MAD a consistent estimator of sigma under normality.
_MAD_TO_SIGMA = 1.4826

# Hartley's d2 constants: E[range]/sigma for a normal sample of size n.
# Lets the observed range stand in as a sigma estimate for small samples,
# which is where MAD most often collapses to zero on clustered data.
_D2 = {
    2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704,
    8: 2.847, 9: 2.970, 10: 3.078, 11: 3.173,
}
# At/above this sample size MAD is stable enough to use alone; below it we
# back MAD with the range estimator so a clustered small baseline does not
# produce a near-zero scale (and thus spurious huge z-scores).
_MAD_STABLE_N = 12

# Absolute floors: the irreducible measurement noise we refuse to be more
# precise than, regardless of how stable a short baseline happens to look.
#
# Timing: network + scheduler jitter is millisecond-scale, not microsecond.
# A robust scale below this is treated as this value, so a deterministic
# endpoint needs a ~3 * floor deviation (with z_threshold=3.0) to flag --
# i.e. a few milliseconds, not a few microseconds. Tune DOWN toward 1e-4 for
# a trusted localhost target where sub-millisecond timing is meaningful.
_TIME_SCALE_FLOOR_S = 1.0e-3
# Length: only a div-by-zero guard for the *jittering* branch. The
# deterministic branch never divides (it uses the any-change rule), so this
# stays tiny on purpose and does not suppress real byte changes.
_LENGTH_SCALE_FLOOR_B = 0.5

# Recommended baseline sample count. The scanner's current default of 5 is
# too few for stable scale estimation; prefer this.
RECOMMENDED_SAMPLES = 15

_STRONG_SIGNALS = frozenset({"status", "body", "length", "timing"})


# ----------------------------------------------------------------------------
# Robust scale estimation
# ----------------------------------------------------------------------------

def _median(xs: list[float]) -> float:
    return statistics.median(xs)


def _mad(xs: list[float], center: float | None = None) -> float:
    """Median absolute deviation (raw, unscaled)."""
    c = _median(xs) if center is None else center
    return statistics.median([abs(x - c) for x in xs])


def robust_scale(xs: list[float], floor: float) -> tuple[float, float]:
    """Return ``(center, sigma_hat)`` using median + scaled MAD, floored.

    For small samples (n < _MAD_STABLE_N) the scaled MAD is backed by a
    range/d2 estimate and the *wider* of the two is taken, because MAD
    frequently reads zero on a small clustered baseline. This is
    conservative: on a small baseline with an outlier it also widens the
    envelope, trading a possible miss for fewer false alarms. The floor both
    prevents division by zero and encodes the metric's irreducible noise --
    a baseline tighter than the floor is treated as exactly the floor.
    """
    n = len(xs)
    center = _median(xs)
    sigma_mad = _MAD_TO_SIGMA * _mad(xs, center)

    if n < _MAD_STABLE_N:
        d2 = _D2.get(n, _D2[2])
        sigma_range = (max(xs) - min(xs)) / d2 if n >= 2 else 0.0
        sigma = max(sigma_mad, sigma_range)
    else:
        sigma = sigma_mad

    return center, max(sigma, floor)


# ----------------------------------------------------------------------------
# Baseline stats container (replaces length_mean/length_stddev/time_mean/
# time_stddev on the Baseline dataclass)
# ----------------------------------------------------------------------------

@dataclass
class RobustBaselineStats:
    """Robust replacements for the mean/stddev fields in ``Baseline``."""

    length_center: float
    length_scale: float
    length_deterministic: bool
    time_center: float
    time_scale: float
    n: int

    @classmethod
    def from_samples(
        cls,
        lengths: list[int],
        times: list[float],
        *,
        time_floor: float = _TIME_SCALE_FLOOR_S,
        length_floor: float = _LENGTH_SCALE_FLOOR_B,
    ) -> "RobustBaselineStats":
        # "Deterministic" means the baseline length literally never varied --
        # the honest test, rather than "MAD == 0" (which a clustered sample
        # can hit while still genuinely varying).
        length_deterministic = len(set(lengths)) == 1
        length_center, length_scale = robust_scale(
            [float(x) for x in lengths], length_floor
        )
        time_center, time_scale = robust_scale(times, time_floor)
        return cls(
            length_center=length_center,
            length_scale=length_scale,
            length_deterministic=length_deterministic,
            time_center=time_center,
            time_scale=time_scale,
            n=len(lengths),
        )

    def describe(self) -> str:
        ldet = " (deterministic)" if self.length_deterministic else ""
        return (
            f"length~{self.length_center:.0f}B scale={self.length_scale:.1f}B{ldet} "
            f"time~{self.time_center:.4f}s scale={self.time_scale:.4f}s "
            f"n={self.n}"
        )


# ----------------------------------------------------------------------------
# Per-metric verdicts
# ----------------------------------------------------------------------------

@dataclass
class MetricVerdict:
    """One metric's deviation, its robust z, and whether it fired."""

    z: float        # robust z; 0.0 in the deterministic-length any-change branch
    delta: float    # signed deviation from the baseline centre
    fired: bool
    reason: str     # human-readable basis for the verdict


def score_timing(
    sample_time: float, stats: RobustBaselineStats, z_threshold: float
) -> MetricVerdict:
    """Robust z for timing. The absolute floor on ``time_scale`` means
    ``|z| >= z_threshold`` already implies a deviation of at least
    ``z_threshold * floor`` seconds, so a deterministic-timing endpoint
    needs a few real milliseconds (not microseconds) to fire."""
    delta = sample_time - stats.time_center
    z = delta / stats.time_scale
    fired = abs(z) >= z_threshold
    reason = (
        f"|z|={abs(z):.2f} >= {z_threshold:.1f} "
        f"(delta={delta:+.4f}s over scale {stats.time_scale:.4f}s)"
        if fired
        else f"within envelope (|z|={abs(z):.2f}, delta={delta:+.4f}s)"
    )
    return MetricVerdict(z=z, delta=delta, fired=fired, reason=reason)


def score_length(
    sample_length: int, stats: RobustBaselineStats, z_threshold: float
) -> MetricVerdict:
    """Length scoring with the deterministic/noisy split.

    Deterministic baseline -> any byte change is signal; flag on any nonzero
    delta and report the byte delta (a z-score would be meaningless).
    Jittering baseline -> robust z against the floored scale.
    """
    delta = float(sample_length) - stats.length_center

    if stats.length_deterministic:
        fired = sample_length != int(round(stats.length_center))
        reason = (
            f"deterministic baseline changed by {int(delta):+d}B"
            if fired
            else "matches deterministic baseline length"
        )
        return MetricVerdict(z=0.0, delta=delta, fired=fired, reason=reason)

    z = delta / stats.length_scale
    fired = abs(z) >= z_threshold
    reason = (
        f"|z|={abs(z):.2f} >= {z_threshold:.1f} (delta={int(delta):+d}B)"
        if fired
        else f"within envelope (|z|={abs(z):.2f}, delta={int(delta):+d}B)"
    )
    return MetricVerdict(z=z, delta=delta, fired=fired, reason=reason)


# ----------------------------------------------------------------------------
# Anomaly decision (revised reflection rule)
# ----------------------------------------------------------------------------

def decide_anomalous(signals: list[str]) -> bool:
    """Anomaly decision with the revised reflection rule.

    Any strong signal (status / body / length / timing) flags. Reflection is
    weak on its own -- a benign echo -- but reflection together with ANY
    other signal (even a weak one such as a header shift) is elevated to
    anomalous, since a reflected payload is the primary XSS tell. Pure
    reflection with nothing else stays annotation-only.
    """
    sigset = set(signals)
    if _STRONG_SIGNALS & sigset:
        return True
    if "reflection" in sigset and (sigset - {"reflection"}):
        return True
    return False


# ----------------------------------------------------------------------------
# All-pairs content floor (replaces the single-reference floor)
# ----------------------------------------------------------------------------

def all_pairs_min_similarity(
    bodies: list[str], sim_fn: Callable[[str, str], float]
) -> float:
    """Worst self-similarity across *all* pairs of baseline bodies.

    Replaces the original's "compare everything to the last sample" floor,
    which one unlucky reference sample can skew. O(N^2) in the number of
    samples -- cheap at the sample counts this tool uses.
    """
    if len(bodies) < 2:
        return 1.0
    worst = 1.0
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            s = sim_fn(bodies[i], bodies[j])
            if s < worst:
                worst = s
    return worst


# ----------------------------------------------------------------------------
# Self-test: exercises the degenerate cases the patch exists to fix.
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    Z = 3.0

    # 1. Deterministic timing: sub-ms deviation must NOT fire; few-ms must.
    s = RobustBaselineStats.from_samples([500] * 5, [0.10] * 5)
    assert not score_timing(0.1003, s, Z).fired, "0.3ms over flat baseline should not fire"
    assert score_timing(0.105, s, Z).fired, "5ms over flat baseline should fire"

    # 2. Clustered-but-noisy timing: a value already seen in the baseline
    #    must NOT fire (the old mean/stddev+floor would have flagged it).
    s = RobustBaselineStats.from_samples(
        [500] * 5, [0.10, 0.11, 0.10, 0.13, 0.10]
    )
    assert not score_timing(0.13, s, Z).fired, "value within observed range should not fire"
    assert score_timing(0.20, s, Z).fired, "value well beyond the range should fire"

    # 3. Deterministic length: any byte change fires; no change does not.
    s = RobustBaselineStats.from_samples([500] * 5, [0.10] * 5)
    assert score_length(501, s, Z).fired, "1-byte change on deterministic length should fire"
    assert not score_length(500, s, Z).fired, "no change should not fire"

    # 4. Jittering length: within-jitter change does not fire; large does.
    s = RobustBaselineStats.from_samples(
        [500, 502, 500, 510, 500], [0.10] * 5
    )
    assert not score_length(505, s, Z).fired, "within-jitter length change should not fire"
    assert score_length(560, s, Z).fired, "large length change should fire"

    # 5. Reflection rule.
    assert decide_anomalous(["timing"])
    assert not decide_anomalous(["reflection"])
    assert decide_anomalous(["reflection", "headers"]), "reflection + header drift elevates"
    assert not decide_anomalous(["headers"])

    # 6. All-pairs floor.
    eq = lambda a, b: 1.0 if a == b else 0.5
    assert all_pairs_min_similarity(["x", "x", "y"], eq) == 0.5

    print("all self-tests passed")
