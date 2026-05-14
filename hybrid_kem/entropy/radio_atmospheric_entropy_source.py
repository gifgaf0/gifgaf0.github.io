"""Radio + atmospheric entropy source — three-channel design (Brief 07).

This module exposes **three architecturally separate** outputs,
mirroring Brief 06's microphone dual-channel design but with one
extra channel for atmospheric/cosmic noise:

- :meth:`RadioAtmosphericEntropySource.thermal_sample_raw` — Channel R1.
  Receiver front-end thermal noise (Johnson–Nyquist, mixer, ADC
  input). Creditable physical entropy. Default H_min placeholder
  is 1.0 bits/sample after low-8-bit extraction.
- :meth:`RadioAtmosphericEntropySource.atmospheric_conditioner` — Channel R2.
  Sferic-rich HF / cosmic background. **Conditioner only** — XOR
  into R1 *after* health tests as additional diversity. Not
  creditable as primary entropy; observable by adversaries with
  distributed receiver networks.
- :meth:`RadioAtmosphericEntropySource.rf_environment_fingerprint` — Channel R3.
  Power-spectrum snapshot of the local RF environment (FM band by
  default). **Personalisation only** — fully reproducible by a
  nearby receiver and therefore *never* entropy. Suitable as DRBG
  ``personalization_string`` to diversify across locations.

CORRECT three-channel usage::

    radio = RadioAtmosphericEntropySource(backend)
    seed = radio.thermal_sample_raw(48)              # R1
    atmo = radio.atmospheric_conditioner(48)         # R2
    fp = radio.rf_environment_fingerprint()          # R3
    conditioned = bytes(a ^ b for a, b in zip(seed, atmo))
    drbg.instantiate(entropy_input=conditioned, nonce=os.urandom(16),
                     personalization=fp)

WRONG patterns (any of these is a security defect)::

    # 1. Atmospheric content as primary entropy:
    drbg.instantiate(entropy_input=radio.atmospheric_conditioner(48), …)
    # 2. RF fingerprint as primary entropy:
    drbg.instantiate(entropy_input=radio.rf_environment_fingerprint(), …)
    # 3. Concatenating R2/R3 into entropy_input:
    drbg.instantiate(entropy_input=seed + atmo + fp, …)

R2 and R3 are observable to varying degrees by adversaries and
must never carry the IND-CCA2 hardness chain on their own.

See ``RADIO_NOTES.md`` for frequency selection guidance, AGC
disable procedure for common SDRs, IQ-imbalance acknowledgement,
and per-channel security analysis.
"""

from __future__ import annotations

import hashlib
import math
import random as _random
import time
from dataclasses import dataclass
from typing import Protocol

from .health_tests import HealthTestResult, run_health_tests
from .microphone_entropy_source import SimulatedEstimationError
from .quartz_entropy_source import (
    HardwareUnavailableError,
    HealthTestFailureError,
)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class FrequencyOutOfRangeError(ValueError):
    """Requested centre frequency is outside the SDR's tuning range."""


class SaturationError(RuntimeError):
    """ADC saturation detected on the thermal-noise sampling frequency.

    Reduce ``thermal_gain_db`` and resample.
    """


class SignalPresentError(RuntimeError):
    """A strong narrowband signal is present on the sampling frequency.

    Retune to a clear frequency before resampling. The ``frequency_hz``
    attribute carries the offending bin.
    """

    def __init__(self, message: str, frequency_hz: int | None = None,
                 peak_db: float | None = None):
        super().__init__(message)
        self.frequency_hz = frequency_hz
        self.peak_db = peak_db


class InsufficientAtmosphericActivityError(RuntimeError):
    """No frequency bins exceed the sferic-detection threshold.

    Caller should fall back to thermal-only operation. Common causes:
    indoor location with strong shielding, very low solar/sferic
    activity, or wrong ``atmospheric_freq_hz``.
    """


# ---------------------------------------------------------------------------
# SDR backend abstraction
# ---------------------------------------------------------------------------


class SDRBackend(Protocol):
    def read_iq_samples(
        self,
        center_freq_hz: int,
        sample_rate_hz: int,
        n_samples: int,
        gain_db: float = 20.0,
    ) -> list[complex]:
        ...

    def scan_power_spectrum(
        self,
        start_freq_hz: int,
        stop_freq_hz: int,
        step_hz: int,
        dwell_ms: int = 10,
    ) -> list[tuple[int, float]]:
        ...

    def device_info(self) -> dict:
        ...


try:
    import SoapySDR  # type: ignore[import-not-found]  # noqa: F401
    SOAPYSDR_AVAILABLE = True
except Exception:
    SOAPYSDR_AVAILABLE = False


class SoapySDRBackend:
    """Real-hardware backend over SoapySDR (stub).

    SoapySDR is typically installed via the system package manager
    (``apt install soapysdr-module-rtlsdr soapysdr-module-hackrf``,
    ``brew install soapysdr``) rather than pip — see RADIO_NOTES.md.
    The constructor refuses if SoapySDR is not importable.
    """

    def __init__(self, device_args: str = "driver=rtlsdr"):
        if not SOAPYSDR_AVAILABLE:
            raise ImportError(
                "SoapySDR is not installed. Install via system package "
                "manager (apt/brew) or use SimulatedSDRBackend for tests."
            )
        self._device_args = device_args

    def read_iq_samples(self, center_freq_hz: int, sample_rate_hz: int,
                        n_samples: int, gain_db: float = 20.0) -> list[complex]:
        raise NotImplementedError(
            "SoapySDRBackend.read_iq_samples is a stub; integrate vendor SDK."
        )

    def scan_power_spectrum(self, start_freq_hz: int, stop_freq_hz: int,
                              step_hz: int, dwell_ms: int = 10
                              ) -> list[tuple[int, float]]:
        raise NotImplementedError(
            "SoapySDRBackend.scan_power_spectrum is a stub; integrate vendor SDK."
        )

    def device_info(self) -> dict:
        return {
            "device_name": f"soapy[{self._device_args}]",
            "driver": "soapy",
            "freq_range_hz": [24_000_000, 1_700_000_000],
            "sample_rate_range_hz": [225_000, 3_200_000],
            "adc_bits": 8,
            "has_agc": True,
        }


class SimulatedSDRBackend:
    """Synthetic SDR backend for tests.

    Modes:

    - ``"thermal"`` — complex Gaussian noise, no signal. The right
      backend for ``thermal_sample_raw`` tests.
    - ``"atmospheric"`` — complex Gaussian + sporadic high-amplitude
      bursts (sferic-like). Sufficient sferic activity to satisfy
      ``atmospheric_conditioner``'s 6 dB peak threshold.
    - ``"rf_environment"`` — deterministic spectrum with several
      known peaks (simulating FM/Wi-Fi/etc.). On ``read_iq_samples``
      injects a strong narrowband tone so ``detect_strong_signal``
      fires (used by tests for the SignalPresentError path).
    - ``"saturated"`` — clipped near ``±1±1j``; ``detect_saturation``
      fires. Used for the SaturationError path.
    """

    _MODES = ("thermal", "atmospheric", "rf_environment", "saturated")

    def __init__(self, mode: str = "thermal", *, seed: int | None = None,
                 freq_range_hz: tuple[int, int] = (100_000, 6_000_000_000),
                 sample_rate_range_hz: tuple[int, int] = (225_000, 3_200_000),
                 adc_bits: int = 8):
        if mode not in self._MODES:
            raise ValueError(f"unknown mode: {mode!r}")
        self._mode = mode
        self._rng = _random.Random(seed if seed is not None else 0xc0de)
        self._freq_range = freq_range_hz
        self._sr_range = sample_rate_range_hz
        self._adc_bits = adc_bits
        self._t = 0
        self._stuck_value: complex | None = None

    def read_iq_samples(self, center_freq_hz: int, sample_rate_hz: int,
                        n_samples: int, gain_db: float = 20.0) -> list[complex]:
        if not (self._freq_range[0] <= center_freq_hz <= self._freq_range[1]):
            raise FrequencyOutOfRangeError(
                f"{center_freq_hz} Hz outside {self._freq_range}"
            )
        if self._stuck_value is not None:
            return [self._stuck_value] * n_samples
        out: list[complex] = []
        # Atmospheric content is HF-only in real life. The simulator's
        # 'atmospheric' mode therefore behaves atmospherically only when
        # the SDR is tuned to HF (< 100 MHz); at UHF / SHF (e.g. the
        # default 1.42 GHz thermal frequency) the same backend returns
        # clean Gaussian noise. This matches operator expectations for
        # multi-channel use (R1 at quiet UHF, R2 at HF) from one SDR.
        effective_mode = self._mode
        if effective_mode == "atmospheric" and center_freq_hz >= 100_000_000:
            effective_mode = "thermal"
        # Front-end thermal noise: low-amplitude complex Gaussian.
        sigma = 0.05 * (1.0 + gain_db / 100.0)
        for _ in range(n_samples):
            re = self._rng.gauss(0.0, sigma)
            im = self._rng.gauss(0.0, sigma)
            if effective_mode == "atmospheric":
                # Deterministic narrowband content (an ionospheric
                # resonance stand-in) modulated by a slow envelope, so
                # the magnitude-PSD has a clear discrete peak the
                # conditioner can lock onto. Layered over sporadic
                # high-amplitude bursts (sferic discharges).
                t_s = self._t / sample_rate_hz
                env = 0.4 + 0.3 * math.sin(2.0 * math.pi * 50.0 * t_s)
                # Narrowband tone at 100 kHz offset from centre.
                tone_a = 0.3 * env * math.cos(2.0 * math.pi * 100_000.0 * t_s)
                tone_b = 0.3 * env * math.sin(2.0 * math.pi * 100_000.0 * t_s)
                re += tone_a
                im += tone_b
                if self._rng.random() < 0.02:
                    burst_phase = self._rng.uniform(0.0, 2.0 * math.pi)
                    re += 0.6 * math.cos(burst_phase)
                    im += 0.6 * math.sin(burst_phase)
            elif effective_mode == "rf_environment":
                # A strong narrowband tone at ~10% of sample rate so the
                # PSD shows an easily-detected peak (SignalPresentError).
                t_s = self._t / sample_rate_hz
                tone = 0.4 * math.cos(2.0 * math.pi * 0.1 * sample_rate_hz * t_s)
                re += tone
                im += tone
            elif effective_mode == "saturated":
                # Pull magnitudes to the ADC rails — clipped IQ.
                re = 0.99 if re >= 0 else -0.99
                im = 0.99 if im >= 0 else -0.99
            self._t += 1
            # Clamp into normalised IQ range.
            if re > 1.0: re = 1.0
            elif re < -1.0: re = -1.0
            if im > 1.0: im = 1.0
            elif im < -1.0: im = -1.0
            out.append(complex(re, im))
        return out

    def scan_power_spectrum(self, start_freq_hz: int, stop_freq_hz: int,
                              step_hz: int, dwell_ms: int = 10
                              ) -> list[tuple[int, float]]:
        if start_freq_hz >= stop_freq_hz or step_hz <= 0:
            raise ValueError("invalid scan range")
        # Generate a deterministic power profile per mode.
        out: list[tuple[int, float]] = []
        f = start_freq_hz
        while f <= stop_freq_hz:
            if self._mode == "rf_environment":
                # A few stable peaks across the band.
                base = -90.0
                # Three "stations" at quartile offsets.
                span = stop_freq_hz - start_freq_hz
                for k in (1, 2, 3):
                    centre = start_freq_hz + (span * k) // 4
                    if abs(f - centre) < step_hz * 4:
                        base = -45.0 + 5.0 * (k - 2)
                        break
                # Add a tiny seeded jitter so different scans differ when
                # the user expects time-varying fingerprints.
                power = base + self._rng.uniform(-1.0, 1.0)
            elif self._mode == "atmospheric":
                power = -75.0 + self._rng.uniform(-3.0, 3.0)
            elif effective_mode == "saturated":
                power = -10.0
            else:
                power = -85.0 + self._rng.uniform(-1.0, 1.0)
            out.append((f, power))
            f += step_hz
        return out

    def device_info(self) -> dict:
        return {
            "device_name": f"SimulatedSDRBackend[{self._mode}]",
            "driver": "simulated",
            "freq_range_hz": list(self._freq_range),
            "sample_rate_range_hz": list(self._sr_range),
            "adc_bits": self._adc_bits,
            "has_agc": False,
        }

    @property
    def mode(self) -> str:
        return self._mode

    def force_stuck(self, value: complex | None) -> None:
        """Test helper: pin every IQ sample to a constant complex value."""
        self._stuck_value = value


# ---------------------------------------------------------------------------
# Saturation / strong-signal detection
# ---------------------------------------------------------------------------


def detect_saturation(samples: list[complex],
                      clip_threshold: float = 0.95,
                      clip_fraction_limit: float = 0.01) -> bool:
    if not samples:
        return False
    n_clipped = sum(1 for s in samples
                    if abs(s.real) > clip_threshold
                    or abs(s.imag) > clip_threshold)
    return (n_clipped / len(samples)) > clip_fraction_limit


def detect_strong_signal(samples: list[complex],
                         signal_threshold_db: float = 20.0
                         ) -> tuple[bool, int, float]:
    """Return ``(present, peak_bin, peak_db_over_median)``.

    Drops the DC bin and the highest two bins before computing the
    peak/median ratio, mirroring Brief 06's silence-probe FFT
    treatment.
    """
    if len(samples) < 32:
        return False, 0, 0.0
    try:
        import numpy as _np
        from scipy.fft import fft   # type: ignore[import-not-found]
    except Exception:
        return False, 0, 0.0
    arr = _np.asarray(samples, dtype=_np.complex128)
    arr -= arr.mean()
    spec = _np.abs(fft(arr))
    if spec.size <= 8:
        return False, 0, 0.0
    trimmed = spec[1:-2]
    peak_idx = int(_np.argmax(trimmed))
    peak = float(trimmed[peak_idx])
    median = float(_np.median(trimmed))
    if median <= 0:
        return False, 0, 0.0
    db = 20.0 * math.log10(peak / median)
    return db > signal_threshold_db, peak_idx + 1, db


# ---------------------------------------------------------------------------
# RadioAtmosphericEntropySource
# ---------------------------------------------------------------------------


class RadioAtmosphericEntropySource:
    SAMPLES_PER_BLOCK = 64
    BLOCK_OUTPUT_BYTES = 32
    H_MIN_PLACEHOLDER = 1.0
    FINGERPRINT_LEN = 32
    SFERIC_THRESHOLD_DB = 6.0

    def __init__(
        self,
        backend: SDRBackend,
        thermal_freq_hz: int = 1_420_405_752,
        thermal_sample_rate_hz: int = 2_048_000,
        thermal_gain_db: float = 20.0,
        atmospheric_freq_hz: int = 10_000_000,
        atmospheric_sample_rate_hz: int = 2_048_000,
        rf_scan_start_hz: int = 88_000_000,
        rf_scan_stop_hz: int = 108_000_000,
        rf_scan_step_hz: int = 100_000,
    ):
        self._backend = backend
        self._thermal_freq = thermal_freq_hz
        self._thermal_sr = thermal_sample_rate_hz
        self._thermal_gain = thermal_gain_db
        self._atmo_freq = atmospheric_freq_hz
        self._atmo_sr = atmospheric_sample_rate_hz
        self._scan_start = rf_scan_start_hz
        self._scan_stop = rf_scan_stop_hz
        self._scan_step = rf_scan_step_hz
        self._h_min = self.H_MIN_PLACEHOLDER
        self._h_min_source = "placeholder"
        self._total_bytes = 0
        self._health_failures = 0
        self._saturation_events = 0
        self._signal_present_events = 0
        self._last_fingerprint_at: str | None = None

    # ------------------------------------------------------------------
    # R1: thermal noise (entropy)
    # ------------------------------------------------------------------

    def thermal_sample_raw(self, n_bytes: int) -> bytes:
        if n_bytes <= 0:
            raise ValueError("n_bytes must be positive")
        n_blocks = math.ceil(n_bytes / self.BLOCK_OUTPUT_BYTES)
        total_samples = n_blocks * self.SAMPLES_PER_BLOCK
        try:
            iq = self._backend.read_iq_samples(
                self._thermal_freq, self._thermal_sr,
                total_samples, self._thermal_gain,
            )
        except HardwareUnavailableError:
            raise
        except NotImplementedError as exc:
            raise HardwareUnavailableError(str(exc)) from exc

        if detect_saturation(iq):
            self._saturation_events += 1
            raise SaturationError(
                f"ADC saturation detected at {self._thermal_freq} Hz; "
                f"reduce thermal_gain_db (current {self._thermal_gain})"
            )
        present, bin_idx, peak_db = detect_strong_signal(iq)
        if present:
            self._signal_present_events += 1
            # Map the FFT bin back to an offset from centre frequency.
            offset_hz = int(self._thermal_sr * bin_idx / max(1, len(iq))) \
                        if iq else 0
            raise SignalPresentError(
                f"strong signal detected near {self._thermal_freq + offset_hz} Hz "
                f"({peak_db:.1f} dB above median); retune before sampling",
                frequency_hz=self._thermal_freq + offset_hz,
                peak_db=peak_db,
            )

        # Use the imaginary component (Brief: less correlated with DC).
        # Quantise to int16, take the low byte for the entropy stream.
        low_bytes = bytearray()
        for s in iq:
            i16 = int(round(s.imag * 32767))
            if i16 > 32767: i16 = 32767
            elif i16 < -32768: i16 = -32768
            low_bytes.append(i16 & 0xff)

        result = run_health_tests(list(low_bytes), h_min=self._h_min)
        if not result.passed:
            self._health_failures += 1
            raise HealthTestFailureError(
                f"SP 800-90B health test failed: rct_ok={result.rct_passed}, "
                f"apt_ok={result.apt_passed}, rct_max_run={result.rct_max_run}, "
                f"apt_max_count={result.apt_max_count}"
            )

        out = bytearray()
        for b in range(n_blocks):
            block = bytes(low_bytes[b * self.SAMPLES_PER_BLOCK:
                                     (b + 1) * self.SAMPLES_PER_BLOCK])
            out.extend(hashlib.sha256(block).digest())
        digest = bytes(out[:n_bytes])
        self._total_bytes += len(digest)
        return digest

    # ------------------------------------------------------------------
    # R2: atmospheric conditioner (NOT entropy)
    # ------------------------------------------------------------------

    def atmospheric_conditioner(self, n_bytes: int,
                                 window_ms: int = 200) -> bytes:
        if n_bytes <= 0:
            raise ValueError("n_bytes must be positive")
        n_samples = max(64, self._atmo_sr * window_ms // 1000)
        iq = self._backend.read_iq_samples(
            self._atmo_freq, self._atmo_sr, n_samples,
        )
        # Welch PSD on the magnitude; pull bins > 6 dB above median.
        try:
            import numpy as _np
            from scipy.signal import welch   # type: ignore[import-not-found]
        except Exception as exc:
            raise InsufficientAtmosphericActivityError(
                f"scipy unavailable for PSD: {exc}"
            ) from exc
        arr = _np.asarray(iq, dtype=_np.complex128)
        if arr.size < 32:
            raise InsufficientAtmosphericActivityError("not enough samples")
        nperseg = min(512, arr.size)
        # Welch PSD of the complex IQ signal directly (return_onesided=False
        # gives the full two-sided spectrum; for IQ we want both halves).
        freqs, psd = welch(arr, fs=self._atmo_sr, nperseg=nperseg,
                           return_onesided=False)
        median = float(_np.median(psd))
        if median <= 0:
            raise InsufficientAtmosphericActivityError(
                "atmospheric PSD is zero — receiver may be silent"
            )
        threshold = median * (10.0 ** (self.SFERIC_THRESHOLD_DB / 10.0))
        active_bins = [(int(freqs[i]), float(psd[i]))
                       for i in range(len(psd)) if psd[i] > threshold]
        if not active_bins:
            raise InsufficientAtmosphericActivityError(
                f"no PSD bins exceed median by {self.SFERIC_THRESHOLD_DB} dB; "
                "atmospheric activity is too low for conditioner use"
            )
        ts = time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime())
        # Hash the active-bin payload + timestamp; expand to n_bytes via
        # SHA-256 chaining if more than 32 bytes are requested.
        seed_h = hashlib.sha256()
        for f, p in active_bins:
            # Two-sided PSD has negative frequencies — use signed encoding.
            seed_h.update(int(f).to_bytes(8, "big", signed=True))
            seed_h.update(int(round(p * 1e9)).to_bytes(8, "big", signed=True))
        seed_h.update(ts.encode())
        seed = seed_h.digest()
        out = bytearray()
        i = 0
        while len(out) < n_bytes:
            h = hashlib.sha256()
            h.update(seed)
            h.update(i.to_bytes(4, "big"))
            out.extend(h.digest())
            i += 1
        return bytes(out[:n_bytes])

    # ------------------------------------------------------------------
    # R3: RF environment fingerprint (NOT entropy)
    # ------------------------------------------------------------------

    def rf_environment_fingerprint(self, *, normalize: bool = True,
                                    location_hint: bytes = b"") -> bytes:
        spectrum = self._backend.scan_power_spectrum(
            self._scan_start, self._scan_stop, self._scan_step,
        )
        powers = [p for _, p in spectrum]
        if normalize and powers:
            lo, hi = min(powers), max(powers)
            span = (hi - lo) if hi > lo else 1.0
            powers = [(p - lo) / span for p in powers]
        ts = time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime())
        h = hashlib.sha256()
        for (f, _), p in zip(spectrum, powers):
            h.update(f.to_bytes(8, "big"))
            h.update(int(round(p * 1e6)).to_bytes(8, "big", signed=True))
        h.update(ts.encode())
        h.update(location_hint)
        digest = h.digest()[: self.FINGERPRINT_LEN]
        self._last_fingerprint_at = ts
        return digest

    # ------------------------------------------------------------------
    # H_min estimation
    # ------------------------------------------------------------------

    def run_h_min_estimation(self, n_samples: int = 131_072) -> dict:
        if isinstance(self._backend, SimulatedSDRBackend):
            raise SimulatedEstimationError(
                "refusing to surface H_min from SimulatedSDRBackend; "
                "real hardware required"
            )
        from .crystal_calibrator import (
            collision_estimate,
            compression_estimate,
            markov_estimate,
            mcv_estimate,
        )
        iq = self._backend.read_iq_samples(
            self._thermal_freq, self._thermal_sr, n_samples, self._thermal_gain,
        )
        low = []
        for s in iq:
            i16 = int(round(s.imag * 32767))
            if i16 > 32767: i16 = 32767
            elif i16 < -32768: i16 = -32768
            low.append(i16 & 0xff)
        out = {
            "h_min_mcv": mcv_estimate(low),
            "h_min_collision": collision_estimate(low),
            "h_min_markov": markov_estimate(low),
            "h_min_compression": compression_estimate(low),
            "n_samples": n_samples,
            "sample_rate": self._thermal_sr,
            "bit_depth": 16,
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
            "thermal_freq_hz": self._thermal_freq,
            "atmospheric_freq_hz": self._atmo_freq,
            "rf_scan_range_hz": [self._scan_start, self._scan_stop],
            "h_min_estimate": self._h_min,
            "h_min_source": self._h_min_source,
            "total_bytes_produced": self._total_bytes,
            "health_test_failures": self._health_failures,
            "saturation_events": self._saturation_events,
            "signal_present_events": self._signal_present_events,
            "last_fingerprint_at": self._last_fingerprint_at,
        }
