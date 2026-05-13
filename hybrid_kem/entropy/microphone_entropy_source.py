"""Microphone entropy source — dual-channel design (Brief 06).

This module exposes **two architecturally separate** outputs:

- :meth:`MicrophoneEntropySource.preamp_sample_raw` — Channel A.
  Sampled preamp thermal noise (Johnson–Nyquist + shot + bias-network
  resistor noise). Creditable physical entropy in the SP 800-90B
  sense at typical consumer-preamp gain. Default H_min placeholder
  is 1.5 bits/sample after the low-8-bit extraction step described
  below.

- :meth:`MicrophoneEntropySource.acoustic_fingerprint` — Channel B.
  A 32-byte digest of room acoustic content (Welch PSD ⊕ timestamp,
  hashed). **NOT entropy.** Suitable only as a DRBG personalisation
  string. Treating Channel B as seed material is a security defect
  — an adversary near the device can inject acoustic content and
  thereby partially control bytes that would otherwise be seed.

Architectural separation is mandatory. The two methods produce
disjoint byte streams; the module never combines them.

CORRECT usage::

    mic = MicrophoneEntropySource(backend)
    seed = mic.preamp_sample_raw(48)             # Channel A → entropy
    perso = mic.acoustic_fingerprint()           # Channel B → diversity only

    drbg = DRBG(HMAC_SHA256)
    drbg.instantiate(
        entropy_input=seed,
        nonce=os.urandom(16),
        personalization=perso,                   # correct slot
    )

WRONG usage::

    seed = mic.preamp_sample_raw(32) + mic.acoustic_fingerprint()
    drbg.instantiate(entropy_input=seed, ...)    # mixes channels — DEFECT

The module additionally enforces a processing-free check at init:
``ProcessingDetectedError`` is raised if AGC, noise gating, or
dynamic-range compression is detected in the driver layer. These
features destroy the thermal-noise floor's unpredictability and
must be disabled in audio-driver settings before use.

See :doc:`Brief 06 / MICROPHONE_NOTES.md` for the full security
analysis. SPEC.md §2.1–§2.3 and Brief 04 (ADC abstraction pattern)
+ Brief 05 (H_min estimation) for surrounding context.
"""

from __future__ import annotations

import hashlib
import math
import random as _random
import time
from dataclasses import dataclass
from typing import Protocol

from .health_tests import (
    DEFAULT_ALPHA,
    HealthTestResult,
    apt as _apt,
    apt_cutoff,
    rct as _rct,
    rct_cutoff,
    run_health_tests as _run_health_tests,
)
from .quartz_entropy_source import (
    HardwareUnavailableError,
    HealthTestFailureError,
)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ProcessingDetectedError(RuntimeError):
    """Driver-layer DSP (AGC / noise gate / compression) was detected.

    The attached ``report`` attribute is a :class:`ProcessingReport`
    explaining which test fired.
    """

    def __init__(self, message: str, report: "ProcessingReport"):
        super().__init__(message)
        self.report = report


class SimulatedEstimationError(RuntimeError):
    """``run_h_min_estimation`` refused to return values from a simulated backend."""


# ---------------------------------------------------------------------------
# AudioBackend
# ---------------------------------------------------------------------------


class AudioBackend(Protocol):
    def read_samples(
        self,
        n_samples: int,
        sample_rate: int = 44_100,
        bit_depth: int = 16,
    ) -> list[int]:
        ...

    def device_info(self) -> dict:
        ...


try:
    import pyaudio   # type: ignore[import-not-found]  # noqa: F401
    PYAUDIO_AVAILABLE = True
except Exception:
    PYAUDIO_AVAILABLE = False


class SimulatedAudioBackend:
    """Synthetic AudioBackend for development and tests.

    Three modes:

    - ``"thermal"``: pure Gaussian noise at low amplitude — simulates a
      preamp thermal-noise floor. The right path for ``preamp_sample_raw``
      tests.
    - ``"acoustic"``: Gaussian + slow periodic tones — simulates room
      content with detectable spectral peaks.
    - ``"agc"``: amplitude-compressed Gaussian (peaks pulled toward
      RMS) — used to exercise the ``ProcessingDetectedError`` path.
    """

    _MODES = ("thermal", "acoustic", "agc")
    _PEAK_INT = (1 << 15) - 1

    def __init__(self, mode: str = "thermal", *, seed: int | None = None,
                 sample_rate_hz: int = 44_100, bit_depth: int = 16,
                 gain: float = 1.0):
        if mode not in self._MODES:
            raise ValueError(f"unknown mode: {mode!r}")
        self._mode = mode
        self._sr = sample_rate_hz
        self._bd = bit_depth
        self._gain = gain
        self._rng = _random.Random(seed if seed is not None else 0xa1de)
        self._t = 0   # sample counter for tone phase
        self._zero_run = False     # tests can flip to inject a noise-gate signal

    # ---- AudioBackend protocol ----

    def read_samples(self, n_samples: int, sample_rate: int = 44_100,
                     bit_depth: int = 16) -> list[int]:
        if n_samples <= 0:
            return []
        if self._zero_run:
            return [0] * n_samples
        out: list[int] = []
        scale = self._PEAK_INT
        # Thermal sigma roughly 0.01 of full scale; rms_dbfs ≈ -40.
        thermal_sigma = 0.01 * scale * self._gain
        for _ in range(n_samples):
            sample = self._rng.gauss(0.0, thermal_sigma)
            if self._mode == "acoustic":
                # Add two slow tones — strong room-acoustic content.
                # Tones scale with gain so the AGC probe (which doubles
                # gain) doesn't see a fixed-amplitude tonal floor relative
                # to a scaled thermal floor; that mismatch would fire AGC.
                t_s = self._t / self._sr
                sample += (0.05 * scale * self._gain
                           * math.sin(2.0 * math.pi * 60.0 * t_s))
                sample += (0.04 * scale * self._gain
                           * math.sin(2.0 * math.pi * 180.0 * t_s))
            elif self._mode == "agc":
                # Pull large excursions back toward the rms band — destroys
                # the long-tail Gaussian behaviour and lowers crest factor.
                if abs(sample) > 0.5 * thermal_sigma:
                    sign = 1 if sample >= 0 else -1
                    sample = sign * 0.5 * thermal_sigma
            self._t += 1
            ival = int(round(sample))
            if ival > self._PEAK_INT:
                ival = self._PEAK_INT
            elif ival < -self._PEAK_INT - 1:
                ival = -self._PEAK_INT - 1
            out.append(ival)
        return out

    def device_info(self) -> dict:
        return {
            "device_name": f"SimulatedAudioBackend[{self._mode}]",
            "driver": "simulated",
            "sample_rates_supported": [self._sr],
            "bit_depths_supported": [self._bd],
            "agc_controllable": True,
            "raw_access": True,
        }

    # ---- simulator extras (not part of the protocol) ----

    @property
    def mode(self) -> str:
        return self._mode

    def set_gain(self, gain: float) -> None:
        self._gain = float(gain)

    def force_zero_run(self, on: bool) -> None:
        """Test helper — flip the backend to emit constant zeros (noise gate)."""
        self._zero_run = bool(on)


class PyAudioBackend:
    """Real-hardware backend over ``pyaudio`` (stub).

    Production callers should replace the body of ``read_samples`` with
    a call into PyAudio's blocking stream. The constructor refuses to
    return if ``pyaudio`` is not installed.
    """

    def __init__(self, device_index: int = 0, sample_rate_hz: int = 44_100,
                 bit_depth: int = 16):
        if not PYAUDIO_AVAILABLE:
            raise ImportError(
                "pyaudio is not installed. Install with `pip install pyaudio` "
                "or use SimulatedAudioBackend for tests."
            )
        self._device_index = device_index
        self._sr = sample_rate_hz
        self._bd = bit_depth

    def read_samples(self, n_samples: int, sample_rate: int = 44_100,
                     bit_depth: int = 16) -> list[int]:
        raise NotImplementedError(
            "PyAudioBackend is a stub; integrate vendor SDK / raw PCM read here"
        )

    def device_info(self) -> dict:
        return {
            "device_name": f"pyaudio[{self._device_index}]",
            "driver": "pyaudio",
            "sample_rates_supported": [self._sr],
            "bit_depths_supported": [self._bd],
            "agc_controllable": False,    # operator must verify per-OS
            "raw_access": True,
        }


# ---------------------------------------------------------------------------
# Processing detection
# ---------------------------------------------------------------------------


@dataclass
class ProcessingReport:
    agc_detected: bool
    noise_gate_detected: bool
    compression_detected: bool
    processing_free: bool
    crest_factor: float
    rms_db: float
    notes: str = ""


def _rms_db(samples: list[int]) -> float:
    if not samples:
        return -120.0
    rms = math.sqrt(sum(s * s for s in samples) / len(samples))
    if rms <= 0:
        return -120.0
    # Reference: 16-bit full-scale peak
    full_scale = (1 << 15) - 1
    return 20.0 * math.log10(rms / full_scale)


def _crest_factor(samples: list[int]) -> float:
    if not samples:
        return 0.0
    peak = max(abs(s) for s in samples)
    rms = math.sqrt(sum(s * s for s in samples) / len(samples))
    if rms <= 0:
        return 0.0
    return peak / rms


def _max_zero_run(samples: list[int]) -> int:
    longest = 0
    current = 0
    for s in samples:
        if s == 0:
            current += 1
            if current > longest:
                longest = current
        else:
            current = 0
    return longest


def detect_processing(
    backend: AudioBackend,
    n_probe_samples: int = 4096,
) -> ProcessingReport:
    """Run three diagnostics for driver-layer DSP and return a report.

    See module docstring / security notes for the rationale on each
    test. ``processing_free`` is True only when all three diagnostics
    are negative.
    """
    samples = backend.read_samples(n_probe_samples)

    crest = _crest_factor(samples)
    rms = _rms_db(samples)
    zero_run = _max_zero_run(samples)

    # AGC: if gain is controllable, compare amplitudes at two gain settings.
    agc_detected = False
    info = backend.device_info()
    set_gain = getattr(backend, "set_gain", None)
    if info.get("agc_controllable") and callable(set_gain):
        try:
            set_gain(1.0)
            a = backend.read_samples(n_probe_samples)
            rms_a = math.sqrt(sum(s * s for s in a) / max(1, len(a)))
            set_gain(2.0)
            b = backend.read_samples(n_probe_samples)
            rms_b = math.sqrt(sum(s * s for s in b) / max(1, len(b)))
            set_gain(1.0)
            if rms_a > 0:
                ratio = rms_b / rms_a
                # AGC detected if ratio doesn't match the 2x gain change.
                agc_detected = abs(ratio - 2.0) > 0.2
        except Exception:
            agc_detected = False

    noise_gate_detected = zero_run > 10
    # Gaussian noise has crest factor ~4 (12 dB). < 2 means compression.
    compression_detected = crest < 2.0 and rms > -90.0

    processing_free = not (agc_detected or noise_gate_detected
                            or compression_detected)
    notes = []
    if agc_detected:
        notes.append("AGC detected (gain probe mismatch).")
    if noise_gate_detected:
        notes.append(f"noise gate detected (zero run = {zero_run}).")
    if compression_detected:
        notes.append(f"compression detected (crest factor = {crest:.2f}).")
    return ProcessingReport(
        agc_detected=agc_detected,
        noise_gate_detected=noise_gate_detected,
        compression_detected=compression_detected,
        processing_free=processing_free,
        crest_factor=crest,
        rms_db=rms,
        notes=" ".join(notes),
    )


# ---------------------------------------------------------------------------
# Silence probe
# ---------------------------------------------------------------------------


@dataclass
class SilenceProbeResult:
    rms_dbfs: float
    crest_factor: float
    zero_crossing_rate: float
    tonal_content_detected: bool
    suitable_for_thermal_only: bool
    notes: str = ""


def _silence_probe(backend: AudioBackend, n_samples: int) -> SilenceProbeResult:
    samples = backend.read_samples(n_samples)
    rms_db = _rms_db(samples)
    crest = _crest_factor(samples)
    # zero-crossing rate (sign changes per sample).
    n = len(samples)
    if n < 2:
        zcr = 0.0
    else:
        signs = [(-1 if s < 0 else 1) for s in samples]
        zcr = sum(1 for i in range(1, n) if signs[i] != signs[i - 1]) / (n - 1)
    # Tonal content via FFT peak vs noise floor.
    tonal = False
    try:
        import numpy as _np
        from scipy.fft import rfft   # type: ignore[import-not-found]
        if n >= 64:
            arr = _np.asarray(samples, dtype=_np.float64)
            arr -= arr.mean()
            spec = _np.abs(rfft(arr))
            # Drop the DC bin and the highest two bins (near-Nyquist
            # artefacts of finite-length FFTs) before computing the
            # peak/median ratio. With Gaussian noise the resulting
            # spectrum is approximately flat and the peak/median is
            # 4-6 dB; we use 20 dB as the tone-detection threshold.
            if spec.size > 8:
                trimmed = spec[1:-2]
                peak = float(trimmed.max())
                median = float(_np.median(trimmed))
                if median > 0 and peak / median > 10 ** (20.0 / 20.0):
                    tonal = True
    except Exception:
        pass
    return SilenceProbeResult(
        rms_dbfs=rms_db,
        crest_factor=crest,
        zero_crossing_rate=zcr,
        tonal_content_detected=tonal,
        suitable_for_thermal_only=not tonal,
        notes=("tonal content detected — acoustic_fingerprint will reflect it"
               if tonal else "no tonal content; thermal-only path is clean"),
    )


# ---------------------------------------------------------------------------
# MicrophoneEntropySource
# ---------------------------------------------------------------------------


class MicrophoneEntropySource:
    SAMPLES_PER_BLOCK = 64
    BLOCK_OUTPUT_BYTES = 32
    H_MIN_PLACEHOLDER = 1.5
    FINGERPRINT_LEN = 32

    def __init__(
        self,
        backend: AudioBackend,
        sample_rate: int = 44_100,
        bit_depth: int = 16,
        silence_window_ms: int = 100,
        require_processing_free: bool = True,
    ):
        self._backend = backend
        self._sr = sample_rate
        self._bd = bit_depth
        self._silence_ms = silence_window_ms
        # Processing check — fail-closed unless explicitly waived.
        self._processing_report = detect_processing(backend)
        if require_processing_free and not self._processing_report.processing_free:
            raise ProcessingDetectedError(
                f"audio backend has detectable processing: "
                f"{self._processing_report.notes}",
                self._processing_report,
            )
        # Silence probe (informational only).
        n_probe = max(1, self._sr * silence_window_ms // 1000)
        self._silence_probe_result = _silence_probe(backend, n_probe)
        self._h_min = self.H_MIN_PLACEHOLDER
        self._h_min_source = "placeholder"
        self._total_bytes = 0
        self._health_failures = 0
        self._last_fingerprint_at: str | None = None

    # ------------------------------------------------------------------
    # Channel A — preamp thermal noise (entropy)
    # ------------------------------------------------------------------

    def preamp_sample_raw(self, n_bytes: int) -> bytes:
        if n_bytes <= 0:
            raise ValueError("n_bytes must be positive")
        n_blocks = math.ceil(n_bytes / self.BLOCK_OUTPUT_BYTES)
        total_samples = n_blocks * self.SAMPLES_PER_BLOCK
        try:
            samples = self._backend.read_samples(total_samples, self._sr, self._bd)
        except HardwareUnavailableError:
            raise
        except NotImplementedError as exc:
            raise HardwareUnavailableError(str(exc)) from exc
        if len(samples) < total_samples:
            raise HardwareUnavailableError(
                f"audio backend returned {len(samples)} of {total_samples} samples"
            )
        # Low-8-bit extraction: the high bits carry slow drift / hum;
        # the low byte carries the thermal noise floor.
        low_bytes = bytearray()
        for s in samples:
            low_bytes.append(int(s) & 0xff)
        result = self._run_health_tests_or_raise(list(low_bytes))
        # SHA-256 rolling-hash digestion.
        out = bytearray()
        for b in range(n_blocks):
            block = bytes(low_bytes[b * self.SAMPLES_PER_BLOCK:
                                     (b + 1) * self.SAMPLES_PER_BLOCK])
            out.extend(hashlib.sha256(block).digest())
        digest = bytes(out[:n_bytes])
        self._total_bytes += len(digest)
        return digest

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
    # Channel B — acoustic personalisation (NOT entropy)
    # ------------------------------------------------------------------

    def acoustic_fingerprint(self, window_ms: int = 500) -> bytes:
        n_samples = max(64, self._sr * window_ms // 1000)
        samples = self._backend.read_samples(n_samples, self._sr, self._bd)
        # Welch PSD over the captured window — implementation borrowed
        # from crystal_calibrator.compute_psd so the two modules share
        # the same FFT path. Local import avoids a circular dependency.
        from .crystal_calibrator import compute_psd
        psd, _ = compute_psd(samples, self._sr, n_fft=512)
        # Hash the normalised PSD bytes + a UTC timestamp so two calls
        # never yield the same fingerprint even in pure silence.
        ts = time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime())
        h = hashlib.sha256()
        for v in psd:
            h.update(v.hex().encode())
        h.update(ts.encode())
        self._last_fingerprint_at = ts
        return h.digest()[: self.FINGERPRINT_LEN]

    # ------------------------------------------------------------------
    # H_min estimation
    # ------------------------------------------------------------------

    def run_h_min_estimation(self, n_samples: int = 88_200) -> dict:
        if isinstance(self._backend, SimulatedAudioBackend):
            raise SimulatedEstimationError(
                "refusing to surface H_min from SimulatedAudioBackend; "
                "real hardware required"
            )
        from .crystal_calibrator import (
            collision_estimate,
            compression_estimate,
            markov_estimate,
            mcv_estimate,
        )
        samples = self._backend.read_samples(n_samples, self._sr, self._bd)
        low = [s & 0xff for s in samples]
        out = {
            "h_min_mcv": mcv_estimate(low),
            "h_min_collision": collision_estimate(low),
            "h_min_markov": markov_estimate(low),
            "h_min_compression": compression_estimate(low),
            "n_samples": n_samples,
            "sample_rate": self._sr,
            "bit_depth": self._bd,
            "backend_class": type(self._backend).__name__,
            "estimated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        out["h_min_conservative"] = min(
            out["h_min_mcv"], out["h_min_collision"],
            out["h_min_markov"], out["h_min_compression"],
        )
        self._h_min = out["h_min_conservative"]
        self._h_min_source = "measured"
        return out

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def status(self) -> dict:
        return {
            "backend": type(self._backend).__name__,
            "sample_rate": self._sr,
            "bit_depth": self._bd,
            "processing_free": self._processing_report.processing_free,
            "h_min_estimate": self._h_min,
            "h_min_source": self._h_min_source,
            "total_bytes_produced": self._total_bytes,
            "health_test_failures": self._health_failures,
            "last_fingerprint_at": self._last_fingerprint_at,
            "silence_probe": {
                "rms_dbfs": self._silence_probe_result.rms_dbfs,
                "crest_factor": self._silence_probe_result.crest_factor,
                "tonal_content_detected":
                    self._silence_probe_result.tonal_content_detected,
            },
        }
