"""Alpha decay entropy source — dual-channel design (Brief 07).

This module exposes **two architecturally separate** outputs:

- :meth:`AlphaDecayEntropySource.interarrival_sample_raw` — Channel A.
  Inter-arrival timing from radioactive decay events. Genuinely IID by
  the underlying physics (memoryless quantum-tunneling), so the
  SP 800-90B IID track applies directly — no Keplerian correction
  (cf. circle_entropy), no normality conjecture (cf. irrational
  conditioner), and no acoustic-injection threat (cf. microphone).
  Conservative entropy budget defaults to 1 bit per sample after the
  ``F(t) = 1 - exp(-λt)`` transform plus 8-bit quantisation.

- :meth:`AlphaDecayEntropySource.count_rate_fingerprint` — Channel B.
  A 32-byte digest of count-rate-plus-timestamp. **NOT entropy.**
  Suitable only as a DRBG personalisation string or operational
  fingerprint. Treating Channel B as seed material is a security
  defect — count rate is predictable to anyone who knows the source
  activity, geometry, and ambient temperature.

Architectural separation is mandatory. The two methods produce
disjoint byte streams; the module never combines them.

CORRECT usage::

    src = AlphaDecayEntropySource(backend)
    seed = src.interarrival_sample_raw(48)        # Channel A → entropy
    perso = src.count_rate_fingerprint()          # Channel B → diversity only

    drbg = DRBG(HMAC_SHA256)
    drbg.instantiate(
        entropy_input=seed[:32],
        nonce=seed[32:48],
        personalization=perso,                    # correct slot
    )

WRONG usage::

    seed = src.interarrival_sample_raw(32) + src.count_rate_fingerprint()
    drbg.instantiate(entropy_input=seed, ...)     # mixes channels — DEFECT

Security notes (per Brief 07 §"Security Notes"):

1. The physics is the strongest entropy case in the project. Inter-arrival
   times from radioactive decay are memoryless in the formal sense, not
   merely "look random".
2. The detector is where the IID story can break — dead time, pile-up,
   after-pulses, electronic noise. :func:`detect_non_poisson` catches the
   common failure modes; it is not exhaustive. Re-run after any hardware
   change.
3. Source activity sets bandwidth, not entropy quality. A 1 kHz source at
   8 quantiser bits and 1 bit/sample of conservative H_min gives
   ~125 bytes/second of seed-quality entropy.
4. Legal note (not legal advice): possession of small sealed alpha sources
   varies by jurisdiction. Operator's responsibility.
5. **Cross-check against another source.** Whenever this source is used in
   production, the conditioning chain MUST include at least one independent
   entropy input (QRNGSource and/or /dev/urandom).
6. λ is re-estimated on every call; never cached across calls.

See ``entropy/ALPHA_DECAY_NOTES.md`` for the detector-characterisation
analysis, SPEC.md §2.1–§2.3 for the surrounding architecture, and
Brief 06 / MICROPHONE_NOTES.md for the channel-separation pattern this
module follows.
"""

from __future__ import annotations

import hashlib
import math
import random as _random
import time
from dataclasses import dataclass
from typing import Protocol

from .health_tests import (
    HealthTestResult,
)
from .health_tests import (
    run_health_tests as _run_health_tests,
)
from .quartz_entropy_source import (
    HardwareUnavailableError,
    HealthTestFailureError,
)

# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class NonPoissonError(RuntimeError):
    """Detector characterisation rejected the backend as non-Poisson.

    The attached ``report`` attribute is a :class:`PoissonReport` showing
    which of the three diagnostic tests fired (rate stability, KS-fit to
    exponential, sub-dead-time events).
    """

    def __init__(self, message: str, report: "PoissonReport"):
        super().__init__(message)
        self.report = report


class SimulatedEstimationError(RuntimeError):
    """``run_h_min_estimation`` refused to surface values from a simulated backend."""


# ---------------------------------------------------------------------------
# TimingBackend
# ---------------------------------------------------------------------------


class TimingBackend(Protocol):
    def read_events(self, n_events: int, timeout_s: float = 60.0) -> list[int]:
        ...

    def detector_info(self) -> dict:
        ...


_DEFAULT_DEAD_TIME_NS = 1_000          # 1 µs, applies to 'dead_time' mode
_DEFAULT_TIMING_RESOLUTION_NS = 1
_DEAD_TIME_DEFAULT = object()         # sentinel for "use per-mode default"


class SimulatedTimingBackend:
    """Synthetic TimingBackend for development and tests.

    Three modes:

    - ``"ideal"``: pure exponential inter-arrivals at ``rate_hz`` with
      no dead time and no pile-up. The reference path for
      ``interarrival_sample_raw`` tests.
    - ``"dead_time"``: exponential inter-arrivals with a fixed
      non-paralyzable dead time. Every emitted Δt is ``dead_time_ns``
      plus a fresh ``Exp(rate_hz)`` sample, so the detector check sees
      strictly Δt ≥ dead_time_ns. At default τ·λ ≈ 1e-3 the KS-fit
      against ``Exp(λ_hat)`` still passes, which mirrors a realistic
      detector.
    - ``"biased"``: gamma-distributed inter-arrivals
      (shape ``bias_shape`` ≥ 2 by default), used to exercise the
      ``detect_non_poisson`` KS-rejection path. The mean matches a
      Poisson process at ``rate_hz`` so rate-stability passes but the
      shape mismatch is large.

    Two test hooks (not part of the protocol) inject specific failure
    modes:

    - :meth:`force_constant_interarrival` — flip the backend to emit
      identical Δt values (drives the health-test fail path).
    - :meth:`force_sub_dead_time_rate` — fraction of events to emit
      below ``dead_time_ns`` (drives the detector's dead-time check).
    """

    _MODES = ("ideal", "dead_time", "biased")

    def __init__(
        self,
        mode: str = "ideal",
        *,
        rate_hz: float = 1_000.0,
        dead_time_ns=_DEAD_TIME_DEFAULT,
        timing_resolution_ns: int = _DEFAULT_TIMING_RESOLUTION_NS,
        bias_shape: float = 3.0,
        seed: int | None = None,
        detector_serial: str = "SIMULATED-001",
    ):
        if mode not in self._MODES:
            raise ValueError(f"unknown mode: {mode!r}")
        if rate_hz <= 0:
            raise ValueError("rate_hz must be positive")
        if dead_time_ns is _DEAD_TIME_DEFAULT:
            # Per-mode default: 1 µs only for 'dead_time' (per Brief 07 spec);
            # 'ideal' and 'biased' carry no detector dead time, so the
            # declared value must be 0 or the detector check spuriously
            # fires on rare short exponential draws.
            dt_int: int = _DEFAULT_DEAD_TIME_NS if mode == "dead_time" else 0
        else:
            dt_int = int(dead_time_ns)
        if dt_int < 0:
            raise ValueError("dead_time_ns must be non-negative")
        dead_time_ns = dt_int
        if bias_shape <= 1.0:
            # shape=1 is exponential, which is the Poisson process itself.
            raise ValueError("bias_shape must be > 1 to be detectable as non-Poisson")
        self._mode = mode
        self._rate_hz = float(rate_hz)
        self._dead_time_ns = int(dead_time_ns)
        self._timing_resolution_ns = int(timing_resolution_ns)
        self._bias_shape = float(bias_shape)
        self._serial = str(detector_serial)
        self._rng = _random.Random(seed if seed is not None else 0xa1da5)  # noqa: S311  # simulator only
        self._cum_time_ns = 0
        self._force_constant = False
        self._force_sub_dead_time_rate = 0.0

    # ---- TimingBackend protocol ----

    def read_events(self, n_events: int, timeout_s: float = 60.0) -> list[int]:
        if n_events <= 0:
            return []
        # In real hardware, timeout would gate the blocking read. For the
        # simulator we ignore it — events are generated instantly.
        _ = timeout_s
        mean_dt_ns = 1e9 / self._rate_hz
        out: list[int] = []
        for _ in range(n_events):
            if self._force_constant:
                dt_ns = float(mean_dt_ns)
            elif (self._force_sub_dead_time_rate > 0.0
                  and self._rng.random() < self._force_sub_dead_time_rate):
                # Inject a sub-dead-time interval to exercise detector check.
                dt_ns = max(1.0, 0.5 * self._dead_time_ns)
            elif self._mode == "ideal":
                dt_ns = self._rng.expovariate(1.0) * mean_dt_ns
            elif self._mode == "dead_time":
                # Non-paralyzable: every gap starts with the dead-time floor.
                dt_ns = self._dead_time_ns + self._rng.expovariate(1.0) * mean_dt_ns
            elif self._mode == "biased":
                # Gamma with shape=bias_shape and mean=mean_dt_ns.
                # gammavariate(alpha, beta) has mean alpha*beta, so
                # beta = mean / alpha.
                dt_ns = self._rng.gammavariate(
                    self._bias_shape, mean_dt_ns / self._bias_shape,
                )
            else:
                raise AssertionError(f"unreachable mode: {self._mode!r}")
            # Round to the declared timing resolution (mimic detector quantiser).
            dt_ns = max(self._timing_resolution_ns,
                        int(round(dt_ns / self._timing_resolution_ns))
                        * self._timing_resolution_ns)
            self._cum_time_ns += int(dt_ns)
            out.append(self._cum_time_ns)
        return out

    def detector_info(self) -> dict:
        return {
            "detector_type": "simulated",
            "discriminator_threshold_mv": None,
            "dead_time_ns": self._dead_time_ns,
            "timing_resolution_ns": self._timing_resolution_ns,
            "source_isotope": None,
            "source_activity_bq": self._rate_hz,
            "detector_serial": self._serial,
        }

    # ---- simulator extras (not part of the protocol) ----

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def rate_hz(self) -> float:
        return self._rate_hz

    def force_constant_interarrival(self, on: bool) -> None:
        """Test helper — flip the backend to emit identical Δt values."""
        self._force_constant = bool(on)

    def force_sub_dead_time_rate(self, fraction: float) -> None:
        """Test helper — fraction in [0,1] of events emitted with Δt < dead_time_ns."""
        if not 0.0 <= fraction <= 1.0:
            raise ValueError("fraction must be in [0, 1]")
        self._force_sub_dead_time_rate = float(fraction)


class SerialTimingBackend:
    """Real-hardware backend over a serial-attached counter (stub).

    Production callers replace the body of ``read_events`` with the
    vendor SDK call (e.g., µC reading a high-resolution timer triggered
    by a PIN-photodiode discriminator). Same gate as
    :class:`PyAudioBackend` in Brief 06 and :class:`SerialADCBackend`
    in Brief 04.
    """

    def __init__(
        self,
        device_path: str,
        *,
        dead_time_ns: int = _DEFAULT_DEAD_TIME_NS,
        timing_resolution_ns: int = _DEFAULT_TIMING_RESOLUTION_NS,
        source_isotope: str | None = None,
        source_activity_bq: float | None = None,
        detector_serial: str | None = None,
    ):
        self._device_path = device_path
        self._dead_time_ns = int(dead_time_ns)
        self._timing_resolution_ns = int(timing_resolution_ns)
        self._isotope = source_isotope
        self._activity = source_activity_bq
        self._serial = detector_serial

    def read_events(self, n_events: int, timeout_s: float = 60.0) -> list[int]:
        raise NotImplementedError(
            "SerialTimingBackend is a stub; integrate vendor SDK / serial read here"
        )

    def detector_info(self) -> dict:
        return {
            "detector_type": "PIN",
            "discriminator_threshold_mv": None,
            "dead_time_ns": self._dead_time_ns,
            "timing_resolution_ns": self._timing_resolution_ns,
            "source_isotope": self._isotope,
            "source_activity_bq": self._activity,
            "detector_serial": self._serial,
        }


# ---------------------------------------------------------------------------
# Poisson-process characterisation
# ---------------------------------------------------------------------------


@dataclass
class PoissonReport:
    rate_estimate_hz: float
    rate_cv_across_windows: float
    rate_stable: bool
    ks_statistic: float
    ks_p_value: float
    exponential_fit_ok: bool
    sub_dead_time_events: int
    dead_time_ok: bool
    poisson_compatible: bool
    n_probe_events: int
    notes: str = ""


_DETECT_NON_POISSON_KS_ALPHA = 0.01
_DETECT_NON_POISSON_RATE_CV_THRESHOLD = 0.25
_DETECT_NON_POISSON_N_SUBWINDOWS = 8


def detect_non_poisson(
    backend: TimingBackend,
    n_probe_events: int = 4096,
) -> PoissonReport:
    """Three-diagnostic Poisson-compatibility check.

    See Brief 07 §"Detector Characterization" for the rationale on each
    test. ``poisson_compatible`` is True only when all three diagnostics
    pass.
    """
    if n_probe_events < _DETECT_NON_POISSON_N_SUBWINDOWS * 2:
        raise ValueError(
            f"n_probe_events must be >= {_DETECT_NON_POISSON_N_SUBWINDOWS * 2}"
        )
    timestamps = backend.read_events(n_probe_events)
    if len(timestamps) < n_probe_events:
        raise HardwareUnavailableError(
            f"backend returned {len(timestamps)} of {n_probe_events} events"
        )
    info = backend.detector_info()
    dead_time_ns = int(info.get("dead_time_ns") or 0)

    deltas = [timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))]
    if not deltas:
        raise HardwareUnavailableError("backend produced fewer than 2 timestamps")

    total_ns = timestamps[-1] - timestamps[0]
    if total_ns <= 0:
        raise HardwareUnavailableError(
            "backend timestamps are non-monotonic (total span <= 0)"
        )
    rate_estimate_hz = (len(deltas)) / (total_ns / 1e9)

    # 1) Rate stability across N sub-windows by time.
    n_sub = _DETECT_NON_POISSON_N_SUBWINDOWS
    sub_dur_ns = total_ns / n_sub
    sub_counts = [0] * n_sub
    for t in timestamps:
        idx = int((t - timestamps[0]) / sub_dur_ns)
        if idx >= n_sub:
            idx = n_sub - 1
        sub_counts[idx] += 1
    mean_count = sum(sub_counts) / n_sub
    var_count = sum((c - mean_count) ** 2 for c in sub_counts) / n_sub
    rate_cv = math.sqrt(var_count) / mean_count if mean_count > 0 else float("inf")
    rate_stable = rate_cv < _DETECT_NON_POISSON_RATE_CV_THRESHOLD

    # 2) KS-fit against Exp(λ_hat). MLE for exponential rate is
    #    λ = N / Σ Δt; scipy parametrises Exp by scale=1/λ.
    lam_hat_per_ns = len(deltas) / sum(deltas) if sum(deltas) > 0 else 0.0
    try:
        from scipy import stats
        ks = stats.kstest(deltas, "expon", args=(0, 1.0 / lam_hat_per_ns))
        ks_stat = float(ks.statistic)
        ks_p = float(ks.pvalue)
    except Exception as exc:  # pragma: no cover - scipy is a hard dep
        raise RuntimeError(f"scipy unavailable for KS test: {exc}") from exc
    exponential_fit_ok = ks_p >= _DETECT_NON_POISSON_KS_ALPHA

    # 3) Dead-time check.
    sub_dt = sum(1 for d in deltas if d < dead_time_ns) if dead_time_ns > 0 else 0
    dead_time_ok = (sub_dt == 0)

    poisson_compatible = bool(rate_stable and exponential_fit_ok and dead_time_ok)
    notes_parts: list[str] = []
    if not rate_stable:
        notes_parts.append(f"rate CV {rate_cv:.3f} >= {_DETECT_NON_POISSON_RATE_CV_THRESHOLD}")
    if not exponential_fit_ok:
        notes_parts.append(f"KS p={ks_p:.4f} < {_DETECT_NON_POISSON_KS_ALPHA}")
    if not dead_time_ok:
        notes_parts.append(f"{sub_dt} sub-dead-time events")

    return PoissonReport(
        rate_estimate_hz=rate_estimate_hz,
        rate_cv_across_windows=rate_cv,
        rate_stable=rate_stable,
        ks_statistic=ks_stat,
        ks_p_value=ks_p,
        exponential_fit_ok=exponential_fit_ok,
        sub_dead_time_events=sub_dt,
        dead_time_ok=dead_time_ok,
        poisson_compatible=poisson_compatible,
        n_probe_events=n_probe_events,
        notes="; ".join(notes_parts),
    )


# ---------------------------------------------------------------------------
# AlphaDecayEntropySource
# ---------------------------------------------------------------------------


class AlphaDecayEntropySource:
    """Inter-arrival entropy source driven by a :class:`TimingBackend`.

    Channel A (``interarrival_sample_raw``) returns CDF-transformed,
    quantised, health-tested bytes drawn from the timing record of
    physical detection events. Channel B (``count_rate_fingerprint``)
    returns a SHA-256 digest over count + window + timestamp + serial
    for use as a DRBG personalisation string.

    See module docstring for the channel separation contract.
    """

    H_MIN_PLACEHOLDER = 1.0
    FINGERPRINT_LEN = 32
    _SUPPORTED_QUANTIZER_BITS = (4, 8, 16)

    def __init__(
        self,
        backend: TimingBackend,
        require_poisson: bool = True,
        h_min_per_sample_bits: float = 1.0,
        quantizer_bits: int = 8,
    ):
        if h_min_per_sample_bits <= 0:
            raise ValueError("h_min_per_sample_bits must be positive")
        if quantizer_bits not in self._SUPPORTED_QUANTIZER_BITS:
            raise ValueError(
                f"quantizer_bits must be one of "
                f"{self._SUPPORTED_QUANTIZER_BITS}; got {quantizer_bits}"
            )
        self._backend = backend
        self._quant_bits = int(quantizer_bits)
        self._h_min = float(h_min_per_sample_bits)
        self._h_min_source = "placeholder"
        self._info = backend.detector_info()
        self._dead_time_ns = int(self._info.get("dead_time_ns") or 0)
        self._last_poisson_report: PoissonReport | None = None
        self._last_rate_estimate_hz: float | None = None
        self._samples_drawn = 0
        self._bytes_emitted = 0
        self._health_failures = 0

        if require_poisson:
            report = detect_non_poisson(backend)
            self._last_poisson_report = report
            self._last_rate_estimate_hz = report.rate_estimate_hz
            if not report.poisson_compatible:
                raise NonPoissonError(
                    f"timing backend is not Poisson-compatible: {report.notes}",
                    report,
                )

    # ------------------------------------------------------------------
    # Channel A — inter-arrival entropy
    # ------------------------------------------------------------------

    def interarrival_sample_raw(self, n_bytes: int) -> bytes:
        if n_bytes <= 0:
            raise ValueError("n_bytes must be positive")
        n_samples = math.ceil(n_bytes * 8 / self._quant_bits)
        n_events = n_samples + 1
        try:
            timestamps = self._backend.read_events(n_events)
        except HardwareUnavailableError:
            raise
        except NotImplementedError as exc:
            raise HardwareUnavailableError(str(exc)) from exc
        if len(timestamps) < n_events:
            raise HardwareUnavailableError(
                f"timing backend returned {len(timestamps)} of {n_events} events"
            )
        deltas = [timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))]
        if self._dead_time_ns > 0:
            n_sub = sum(1 for d in deltas if d < self._dead_time_ns)
            if n_sub > 0:
                # Defense in depth — after init's detect_non_poisson this
                # should be zero. If it fires the backend is broken.
                raise HealthTestFailureError(
                    f"timing backend produced {n_sub} sub-dead-time intervals "
                    f"(dead_time_ns={self._dead_time_ns})"
                )

        lam_hat_per_ns = self._estimate_lambda(deltas)
        self._last_rate_estimate_hz = lam_hat_per_ns * 1e9

        out_bytes = self._cdf_quantize(deltas, lam_hat_per_ns)[:n_bytes]
        self._run_health_tests_or_raise(list(out_bytes))
        self._samples_drawn += n_samples
        self._bytes_emitted += len(out_bytes)
        return out_bytes

    @staticmethod
    def _estimate_lambda(deltas: list[int]) -> float:
        """MLE rate (in 1/ns) for an exponential inter-arrival series."""
        total = sum(deltas)
        if total <= 0:
            raise HealthTestFailureError(
                "inter-arrival total is non-positive; backend timestamps invalid"
            )
        return len(deltas) / total

    def _cdf_quantize(
        self,
        deltas: list[int],
        lam_hat_per_ns: float,
    ) -> bytes:
        """Apply u_i = 1 - exp(-λ·Δt_i) and pack ``quantizer_bits`` per sample.

        Quantiser uses the top ``quantizer_bits`` bits of u_i. Because
        u_i is uniform on [0, 1) under exact-λ assumptions, the byte
        values are uniform under the same. Health-test cutoffs are tuned
        by ``h_min_per_sample_bits`` to remain conservative.
        """
        qbits = self._quant_bits
        max_q = 1 << qbits
        # u_i in [0, 1); quantise = floor(u_i * 2^qbits).
        ints: list[int] = []
        for d in deltas:
            u = 1.0 - math.exp(-lam_hat_per_ns * d)
            if u >= 1.0:
                u = 1.0 - 1e-15
            elif u < 0.0:
                u = 0.0
            q = int(u * max_q)
            if q >= max_q:
                q = max_q - 1
            ints.append(q)
        return _pack_bits(ints, qbits)

    def _run_health_tests_or_raise(self, samples: list[int]) -> HealthTestResult:
        result = _run_health_tests(samples, h_min=self._h_min)
        if not result.passed:
            self._health_failures += 1
            raise HealthTestFailureError(
                f"SP 800-90B health test failed: rct_ok={result.rct_passed}, "
                f"apt_ok={result.apt_passed}, rct_max_run={result.rct_max_run}, "
                f"apt_max_count={result.apt_max_count}"
            )
        return result

    # ------------------------------------------------------------------
    # Channel B — count-rate fingerprint (NOT entropy)
    # ------------------------------------------------------------------

    def count_rate_fingerprint(self, window_ms: int = 1000) -> bytes:
        if window_ms <= 0:
            raise ValueError("window_ms must be positive")
        # The fingerprint counts events over a wall-clock window of
        # ``window_ms`` ms. For real hardware this is a tight loop on the
        # backend; for the simulated backend we derive an expected count
        # from the declared activity and the rate estimate.
        info = self._backend.detector_info()
        # Prefer the latest empirical rate estimate, fall back to declared.
        rate_hz = (self._last_rate_estimate_hz
                   or info.get("source_activity_bq")
                   or 0.0)
        try:
            rate_hz = float(rate_hz)
        except (TypeError, ValueError):
            rate_hz = 0.0
        count = int(round(rate_hz * window_ms / 1000.0))
        serial = (info.get("detector_serial") or "").encode()

        h = hashlib.sha256()
        h.update(int(count).to_bytes(8, "big", signed=False))
        h.update(int(window_ms).to_bytes(4, "big", signed=False))
        h.update(int(time.time_ns()).to_bytes(8, "big", signed=False))
        h.update(serial)
        return h.digest()[: self.FINGERPRINT_LEN]

    # ------------------------------------------------------------------
    # H_min estimation
    # ------------------------------------------------------------------

    def run_h_min_estimation(self, n_samples: int = 100_000) -> dict:
        if isinstance(self._backend, SimulatedTimingBackend):
            raise SimulatedEstimationError(
                "refusing to surface H_min from SimulatedTimingBackend; "
                "real hardware required"
            )
        from .crystal_calibrator import (
            collision_estimate,
            compression_estimate,
            markov_estimate,
            mcv_estimate,
        )
        n_events = n_samples + 1
        timestamps = self._backend.read_events(n_events)
        if len(timestamps) < n_events:
            raise HardwareUnavailableError(
                f"timing backend returned {len(timestamps)} of {n_events} events"
            )
        deltas = [timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))]
        lam_hat_per_ns = self._estimate_lambda(deltas)
        out_bytes = self._cdf_quantize(deltas, lam_hat_per_ns)
        # Unpack to per-sample symbol stream for the estimators.
        symbols = _unpack_bits(out_bytes, self._quant_bits, n_samples)
        out = {
            "h_min_mcv": mcv_estimate(symbols),
            "h_min_markov": markov_estimate(symbols),
            "h_min_collision": collision_estimate(symbols),
            "h_min_compression": compression_estimate(symbols),
            "n_samples": n_samples,
            "rate_estimate_hz": lam_hat_per_ns * 1e9,
            "quantizer_bits": self._quant_bits,
            "backend_class": type(self._backend).__name__,
            "estimated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        out["h_min_conservative"] = min(
            out["h_min_mcv"], out["h_min_markov"],
            out["h_min_collision"], out["h_min_compression"],
        )
        self._h_min = out["h_min_conservative"]
        self._h_min_source = "measured"
        self._last_rate_estimate_hz = out["rate_estimate_hz"]
        return out

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def status(self) -> dict:
        return {
            "detector_info": dict(self._info),
            "last_rate_estimate_hz": self._last_rate_estimate_hz,
            "last_poisson_report": self._last_poisson_report,
            "samples_drawn_session": self._samples_drawn,
            "bytes_emitted_session": self._bytes_emitted,
            "health_test_failures_session": self._health_failures,
            "h_min_per_sample_bits": self._h_min,
            "h_min_source": self._h_min_source,
            "quantizer_bits": self._quant_bits,
        }


# ---------------------------------------------------------------------------
# Bit packing helpers
# ---------------------------------------------------------------------------


def _pack_bits(symbols: list[int], bits_per_symbol: int) -> bytes:
    """Pack a list of ``bits_per_symbol``-bit symbols MSB-first into bytes."""
    if bits_per_symbol == 8:
        return bytes(s & 0xff for s in symbols)
    if bits_per_symbol == 16:
        out = bytearray()
        for s in symbols:
            s &= 0xffff
            out.append((s >> 8) & 0xff)
            out.append(s & 0xff)
        return bytes(out)
    # General path (used for 4-bit).
    buf = 0
    n_bits = 0
    out = bytearray()
    mask = (1 << bits_per_symbol) - 1
    for s in symbols:
        buf = (buf << bits_per_symbol) | (s & mask)
        n_bits += bits_per_symbol
        while n_bits >= 8:
            n_bits -= 8
            out.append((buf >> n_bits) & 0xff)
    if n_bits > 0:
        out.append((buf << (8 - n_bits)) & 0xff)
    return bytes(out)


def _unpack_bits(packed: bytes, bits_per_symbol: int, n_symbols: int) -> list[int]:
    """Inverse of :func:`_pack_bits`."""
    if bits_per_symbol == 8:
        return [b for b in packed[:n_symbols]]
    if bits_per_symbol == 16:
        out = []
        for i in range(n_symbols):
            out.append((packed[2 * i] << 8) | packed[2 * i + 1])
        return out
    out: list[int] = []
    buf = 0
    n_bits = 0
    idx = 0
    mask = (1 << bits_per_symbol) - 1
    for byte in packed:
        buf = (buf << 8) | byte
        n_bits += 8
        while n_bits >= bits_per_symbol and idx < n_symbols:
            n_bits -= bits_per_symbol
            out.append((buf >> n_bits) & mask)
            idx += 1
        if idx >= n_symbols:
            break
    return out


__all__ = [
    "AlphaDecayEntropySource",
    "HardwareUnavailableError",
    "HealthTestFailureError",
    "NonPoissonError",
    "PoissonReport",
    "SerialTimingBackend",
    "SimulatedEstimationError",
    "SimulatedTimingBackend",
    "TimingBackend",
    "detect_non_poisson",
]
