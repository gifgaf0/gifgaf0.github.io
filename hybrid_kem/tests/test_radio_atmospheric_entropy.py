"""Tests for the Brief 07 radio + atmospheric entropy module."""

from __future__ import annotations

import inspect
import time

import pytest

from hybrid_kem.entropy.drbg import DRBG, HMAC_SHA256
from hybrid_kem.entropy.radio_atmospheric_entropy_source import (
    HealthTestFailureError,
    InsufficientAtmosphericActivityError,
    RadioAtmosphericEntropySource,
    SaturationError,
    SignalPresentError,
    SimulatedEstimationError,
    SimulatedSDRBackend,
    SoapySDRBackend,
    detect_saturation,
    detect_strong_signal,
)


# ---------------------------------------------------------------------------
# Functional
# ---------------------------------------------------------------------------


def test_thermal_sample_raw_produces_output():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("thermal", seed=1))
    out = src.thermal_sample_raw(64)
    assert isinstance(out, bytes)
    assert len(out) == 64


def test_atmospheric_conditioner_produces_output():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("atmospheric", seed=2))
    out = src.atmospheric_conditioner(32)
    assert isinstance(out, bytes)
    assert len(out) == 32


def test_rf_fingerprint_is_32_bytes():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("rf_environment", seed=3))
    fp = src.rf_environment_fingerprint()
    assert len(fp) == 32


def test_rf_fingerprint_changes_over_time():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("rf_environment", seed=4))
    a = src.rf_environment_fingerprint()
    time.sleep(0.01)
    b = src.rf_environment_fingerprint()
    assert a != b


def test_three_channels_produce_independent_outputs():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("atmospheric", seed=5))
    r1 = src.thermal_sample_raw(32)
    r2 = src.atmospheric_conditioner(32)
    r3 = src.rf_environment_fingerprint()
    assert r1 != r2
    assert r1 != r3
    assert r2 != r3


def test_status_returns_required_keys():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("thermal", seed=6))
    s = src.status()
    required = {
        "backend", "thermal_freq_hz", "atmospheric_freq_hz",
        "rf_scan_range_hz", "h_min_estimate", "h_min_source",
        "total_bytes_produced", "health_test_failures",
        "saturation_events", "signal_present_events",
        "last_fingerprint_at",
    }
    assert required.issubset(s.keys())


# ---------------------------------------------------------------------------
# Saturation / signal detection
# ---------------------------------------------------------------------------


def test_saturation_detected_on_saturated_backend():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("saturated", seed=7))
    with pytest.raises(SaturationError):
        src.thermal_sample_raw(32)


def test_strong_signal_detected():
    src = RadioAtmosphericEntropySource(
        SimulatedSDRBackend("rf_environment", seed=8)
    )
    with pytest.raises(SignalPresentError):
        src.thermal_sample_raw(32)


def test_thermal_sampling_clean_on_thermal_backend():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("thermal", seed=9))
    out = src.thermal_sample_raw(64)
    assert len(out) == 64
    assert src.status()["saturation_events"] == 0
    assert src.status()["signal_present_events"] == 0


def test_saturation_events_counter_increments():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("saturated", seed=10))
    with pytest.raises(SaturationError):
        src.thermal_sample_raw(32)
    assert src.status()["saturation_events"] == 1
    # Repeat — counter increments.
    with pytest.raises(SaturationError):
        src.thermal_sample_raw(32)
    assert src.status()["saturation_events"] == 2


# ---------------------------------------------------------------------------
# Atmospheric conditioner
# ---------------------------------------------------------------------------


def test_atmospheric_conditioner_raises_on_no_activity():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("thermal", seed=11))
    with pytest.raises(InsufficientAtmosphericActivityError):
        src.atmospheric_conditioner(32)


def test_atmospheric_conditioner_succeeds_on_atmospheric_mode():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("atmospheric", seed=12))
    out = src.atmospheric_conditioner(64)
    assert len(out) == 64


def test_conditioner_xor_pattern():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("atmospheric", seed=13))
    seed = src.thermal_sample_raw(32)
    atmo = src.atmospheric_conditioner(32)
    conditioned = bytes(a ^ b for a, b in zip(seed, atmo))
    assert conditioned != seed
    assert conditioned != atmo
    assert len(conditioned) == 32


# ---------------------------------------------------------------------------
# Health tests
# ---------------------------------------------------------------------------


def test_health_tests_pass_thermal_noise():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("thermal", seed=14))
    out = src.thermal_sample_raw(1024)
    assert len(out) == 1024
    assert src.status()["health_test_failures"] == 0


def test_health_tests_fail_constant_iq():
    backend = SimulatedSDRBackend("thermal", seed=15)
    backend.force_stuck(complex(0.0, 0.0))
    src = RadioAtmosphericEntropySource(backend)
    with pytest.raises(HealthTestFailureError):
        src.thermal_sample_raw(256)


def test_health_tests_imported_from_shared_module():
    """Verify the radio module imports run_health_tests from the shared
    location and does not redefine RCT/APT locally."""
    import hybrid_kem.entropy.radio_atmospheric_entropy_source as radio_mod
    src = inspect.getsource(radio_mod)
    assert "from .health_tests import" in src
    # Local definitions of rct() / apt() would be a refactor regression.
    assert "def rct(" not in src
    assert "def apt(" not in src


# ---------------------------------------------------------------------------
# H_min estimation
# ---------------------------------------------------------------------------


def test_h_min_estimation_returns_required_keys():
    """The simulator guard raises; wrap with a non-Simulated-named backend."""

    class _FakeHWSDRBackend:
        def __init__(self, inner):
            self._inner = inner

        def read_iq_samples(self, c, sr, n, g=20.0):
            return self._inner.read_iq_samples(c, sr, n, g)

        def scan_power_spectrum(self, a, b, s, dwell_ms=10):
            return self._inner.scan_power_spectrum(a, b, s, dwell_ms)

        def device_info(self):
            return self._inner.device_info()

    inner = SimulatedSDRBackend("thermal", seed=16)
    src = RadioAtmosphericEntropySource(_FakeHWSDRBackend(inner))
    out = src.run_h_min_estimation(n_samples=8192)
    required = {
        "h_min_mcv", "h_min_collision", "h_min_markov",
        "h_min_compression", "h_min_conservative",
        "n_samples", "sample_rate", "bit_depth",
        "backend_class", "estimated_at",
    }
    assert required.issubset(out.keys())


def test_h_min_conservative_is_minimum():
    class _FakeHWSDRBackend:
        def __init__(self, inner):
            self._inner = inner

        def read_iq_samples(self, c, sr, n, g=20.0):
            return self._inner.read_iq_samples(c, sr, n, g)

        def scan_power_spectrum(self, a, b, s, dwell_ms=10):
            return self._inner.scan_power_spectrum(a, b, s, dwell_ms)

        def device_info(self):
            return self._inner.device_info()

    inner = SimulatedSDRBackend("thermal", seed=17)
    src = RadioAtmosphericEntropySource(_FakeHWSDRBackend(inner))
    out = src.run_h_min_estimation(n_samples=8192)
    assert out["h_min_conservative"] == min(
        out["h_min_mcv"], out["h_min_collision"],
        out["h_min_markov"], out["h_min_compression"],
    )


def test_simulated_estimation_blocked():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("thermal", seed=18))
    with pytest.raises(SimulatedEstimationError):
        src.run_h_min_estimation(n_samples=4096)


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------


def test_pipeline_integration():
    src = RadioAtmosphericEntropySource(SimulatedSDRBackend("atmospheric", seed=19))
    seed = src.thermal_sample_raw(48)
    atmo = src.atmospheric_conditioner(48)
    fp = src.rf_environment_fingerprint()
    conditioned = bytes(a ^ b for a, b in zip(seed, atmo))
    drbg = DRBG(HMAC_SHA256)
    drbg.instantiate(
        entropy_input=conditioned[:32],
        nonce=conditioned[32:48],
        personalization=fp,
    )
    assert drbg.state == "instantiated"
    assert len(drbg.generate(64)) == 64


def test_wrong_channel_usage_documented():
    import hybrid_kem.entropy.radio_atmospheric_entropy_source as radio_mod
    docstring = radio_mod.__doc__ or ""
    assert "WRONG" in docstring
    assert "CORRECT" in docstring


# ---------------------------------------------------------------------------
# SoapySDR stub
# ---------------------------------------------------------------------------


def test_soapy_backend_stub():
    # Whether SoapySDR is installed or not, the stub class either raises
    # ImportError at init or NotImplementedError on read_iq_samples.
    from hybrid_kem.entropy.radio_atmospheric_entropy_source import (
        SOAPYSDR_AVAILABLE,
    )
    if not SOAPYSDR_AVAILABLE:
        with pytest.raises(ImportError):
            SoapySDRBackend()
    else:
        b = SoapySDRBackend()
        with pytest.raises(NotImplementedError):
            b.read_iq_samples(100_000_000, 2_048_000, 1024)
