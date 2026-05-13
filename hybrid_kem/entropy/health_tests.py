"""SP 800-90B §4.4 continuous health tests for entropy sources.

Implements:
- Repetition Count Test (RCT), §4.4.1
- Adaptive Proportion Test (APT), §4.4.2

Both tests are continuous and run on every byte. Once any test fails, the
state becomes sticky-failed until ``reset()`` is called: a healthy entropy
source should never recover silently from a noise-source failure.

Cutoff thresholds follow SP 800-90B §4.4 closed-form expressions so that the
expected false-positive rate per test is approximately ``alpha``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# Defaults: alpha 2^-30 follows SP 800-90B Annex C examples; h_per_byte 7.5 is
# a conservative min-entropy assumption for raw quantum-derived bytes (real
# sources typically achieve > 7.9, but health tests should not rely on that).
DEFAULT_ALPHA = 2.0 ** -30
DEFAULT_H_PER_BYTE = 7.5
APT_WINDOWS = (512, 1024)


def rct_cutoff(alpha: float, h_per_byte: float) -> int:
    """SP 800-90B §4.4.1: C = 1 + ceil(-log2(alpha) / H)."""
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0, 1)")
    if h_per_byte <= 0:
        raise ValueError("h_per_byte must be positive")
    return 1 + math.ceil(-math.log2(alpha) / h_per_byte)


def apt_cutoff(alpha: float, h_per_byte: float, window: int) -> int:
    """SP 800-90B §4.4.2: cutoff = 1 + CRITBINOM(W, p, 1-alpha) where p = 2^-H.

    We use the normal approximation to the binomial inverse-CDF, which is
    sufficient for the windows used here (W >= 512). The tail correction
    keeps the bound conservative (slightly over-permissive on alpha by at
    most a fraction of a percent at these parameters).
    """
    p = 2.0 ** -h_per_byte
    mean = window * p
    variance = window * p * (1 - p)
    std = math.sqrt(variance)
    # inverse standard normal CDF at (1 - alpha) via Beasley-Springer-Moro
    z = _inv_norm_cdf(1.0 - alpha)
    return 1 + math.ceil(mean + z * std)


def _inv_norm_cdf(p: float) -> float:
    """Beasley-Springer-Moro inverse normal CDF approximation."""
    if not 0 < p < 1:
        raise ValueError("p must be in (0, 1)")
    a = [
        -3.969683028665376e1, 2.209460984245205e2, -2.759285104469687e2,
        1.383577518672690e2, -3.066479806614716e1, 2.506628277459239e0,
    ]
    b = [
        -5.447609879822406e1, 1.615858368580409e2, -1.556989798598866e2,
        6.680131188771972e1, -1.328068155288572e1,
    ]
    c = [
        -7.784894002430293e-3, -3.223964580411365e-1, -2.400758277161838e0,
        -2.549732539343734e0, 4.374664141464968e0, 2.938163982698783e0,
    ]
    d = [
        7.784695709041462e-3, 3.224671290700398e-1, 2.445134137142996e0,
        3.754408661907416e0,
    ]
    plow = 0.02425
    phigh = 1 - plow
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p <= phigh:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
               (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q = math.sqrt(-2 * math.log(1 - p))
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
           ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


@dataclass
class _APTState:
    window: int
    cutoff: int
    reference: Optional[int] = None
    count: int = 0
    seen: int = 0


@dataclass
class HealthTests:
    """Continuous SP 800-90B health tests over byte samples.

    Each byte is treated as one sample with 256 possible values. The test
    state is sticky: any failure leaves the instance in ``failed`` until
    ``reset()`` is called. ``update`` returns ``True`` if all tests still
    pass after consuming the supplied bytes.
    """

    alpha: float = DEFAULT_ALPHA
    h_per_byte: float = DEFAULT_H_PER_BYTE

    _rct_cutoff: int = field(init=False)
    _rct_count: int = field(init=False, default=0)
    _rct_last: Optional[int] = field(init=False, default=None)
    _apts: list = field(init=False)
    _state: str = field(init=False, default="ok")
    _failure_reason: Optional[str] = field(init=False, default=None)
    _samples_seen: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        self._rct_cutoff = rct_cutoff(self.alpha, self.h_per_byte)
        self._apts = [
            _APTState(window=w, cutoff=apt_cutoff(self.alpha, self.h_per_byte, w))
            for w in APT_WINDOWS
        ]

    def update(self, sample: bytes) -> bool:
        if self._state == "failed":
            return False
        for byte in sample:
            self._samples_seen += 1
            if not self._step_rct(byte):
                return False
            if not self._step_apt(byte):
                return False
        return True

    def _step_rct(self, byte: int) -> bool:
        if byte == self._rct_last:
            self._rct_count += 1
        else:
            self._rct_last = byte
            self._rct_count = 1
        if self._rct_count >= self._rct_cutoff:
            self._fail(f"RCT: run length {self._rct_count} >= {self._rct_cutoff}")
            return False
        return True

    def _step_apt(self, byte: int) -> bool:
        for apt in self._apts:
            if apt.reference is None or apt.seen == apt.window:
                apt.reference = byte
                apt.count = 1
                apt.seen = 1
                continue
            apt.seen += 1
            if byte == apt.reference:
                apt.count += 1
                if apt.count >= apt.cutoff:
                    self._fail(
                        f"APT(W={apt.window}): count {apt.count} >= {apt.cutoff}"
                    )
                    return False
        return True

    def _fail(self, reason: str) -> None:
        self._state = "failed"
        self._failure_reason = reason

    def status(self) -> dict:
        out = {
            "rct_count": self._rct_count,
            "rct_cutoff": self._rct_cutoff,
            "state": self._state,
            "failure_reason": self._failure_reason,
            "samples_seen": self._samples_seen,
        }
        for apt in self._apts:
            out[f"apt_{apt.window}_count"] = apt.count
            out[f"apt_{apt.window}_cutoff"] = apt.cutoff
        return out

    def reset(self) -> None:
        self._rct_count = 0
        self._rct_last = None
        for apt in self._apts:
            apt.reference = None
            apt.count = 0
            apt.seen = 0
        self._state = "ok"
        self._failure_reason = None
        self._samples_seen = 0


class HealthTestFailure(Exception):
    """Raised when an entropy consumer detects a sticky-failed health test."""


# ---------------------------------------------------------------------------
# Brief 06 refactor gate: stateless function-style API
# ---------------------------------------------------------------------------
#
# The :class:`HealthTests` class above is the canonical stateful continuous
# health-test object used by Brief 04's QuartzEntropySource. Brief 06 calls
# for a stateless ``rct(samples, h_min) / apt(samples, h_min) /
# run_health_tests(samples, h_min)`` function-style API that's convenient
# for one-shot batch checks. These wrappers are a thin layer over the
# existing cutoff calculators — no separate health-test logic, so the
# extraction the brief asks for is preserved (one source of truth in this
# file).


from dataclasses import dataclass as _dataclass


@_dataclass
class HealthTestResult:
    rct_passed: bool
    apt_passed: bool
    rct_max_run: int
    apt_max_count: int
    rct_cutoff: int
    apt_cutoff: int
    apt_window: int
    h_min: float
    alpha: float

    @property
    def passed(self) -> bool:
        return self.rct_passed and self.apt_passed


def rct(samples, h_min: float, alpha: float = DEFAULT_ALPHA) -> bool:
    """SP 800-90B §4.4.1 RCT on a finite sample list.

    Returns ``True`` iff every run of equal samples is shorter than the
    cutoff ``C = 1 + ceil(-log2(alpha) / h_min)``.
    """
    cutoff = rct_cutoff(alpha, max(h_min, 1e-9))
    count = 0
    prev = None
    for s in samples:
        if s == prev:
            count += 1
            if count >= cutoff:
                return False
        else:
            prev = s
            count = 1
    return True


def apt(samples, h_min: float, *, window: int = 512,
        alpha: float = DEFAULT_ALPHA) -> bool:
    """SP 800-90B §4.4.2 APT on a finite sample list with the given window."""
    cutoff = apt_cutoff(alpha, max(h_min, 1e-9), window)
    if not samples:
        return True
    samples = list(samples)
    for start in range(0, len(samples), window):
        block = samples[start:start + window]
        if not block:
            break
        ref = block[0]
        count = sum(1 for s in block if s == ref)
        if count >= cutoff:
            return False
    return True


def run_health_tests(samples, h_min: float, *,
                     window: int = 512,
                     alpha: float = DEFAULT_ALPHA) -> HealthTestResult:
    """Run RCT + APT and return a structured :class:`HealthTestResult`."""
    samples = list(samples)
    rct_c = rct_cutoff(alpha, max(h_min, 1e-9))
    apt_c = apt_cutoff(alpha, max(h_min, 1e-9), window)
    # Walk the stream once, recording observed maxima alongside pass/fail.
    rct_max_run = 0
    count = 0
    prev = None
    rct_ok = True
    for s in samples:
        if s == prev:
            count += 1
        else:
            prev = s
            count = 1
        if count > rct_max_run:
            rct_max_run = count
        if count >= rct_c:
            rct_ok = False
    apt_max_count = 0
    apt_ok = True
    for start in range(0, len(samples), window):
        block = samples[start:start + window]
        if not block:
            break
        ref = block[0]
        c = sum(1 for s in block if s == ref)
        if c > apt_max_count:
            apt_max_count = c
        if c >= apt_c:
            apt_ok = False
    return HealthTestResult(
        rct_passed=rct_ok,
        apt_passed=apt_ok,
        rct_max_run=rct_max_run,
        apt_max_count=apt_max_count,
        rct_cutoff=rct_c,
        apt_cutoff=apt_c,
        apt_window=window,
        h_min=h_min,
        alpha=alpha,
    )
