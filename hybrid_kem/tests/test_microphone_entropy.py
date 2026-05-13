"""Tests for the Brief 06 microphone entropy module."""

from __future__ import annotations

import importlib
import inspect
import time
from pathlib import Path

import pytest

from hybrid_kem.entropy.drbg import DRBG, HMAC_SHA256
from hybrid_kem.entropy.health_tests import HealthTestResult, run_health_tests
from hybrid_kem.entropy.microphone_entropy_source import (
    HealthTestFailureError,
    MicrophoneEntropySource,
    ProcessingDetectedError,
    SimulatedAudioBackend,
    SimulatedEstimationError,
    detect_processing,
)


# ---------------------------------------------------------------------------
# Functional
# ---------------------------------------------------------------------------


def test_preamp_sample_raw_produces_output():
    src = MicrophoneEntropySource(SimulatedAudioBackend("thermal", seed=1))
    out = src.preamp_sample_raw(64)
    assert isinstance(out, bytes)
    assert len(out) == 64


def test_acoustic_fingerprint_is_32_bytes():
    src = MicrophoneEntropySource(SimulatedAudioBackend("acoustic", seed=2))
    fp = src.acoustic_fingerprint(window_ms=200)
    assert len(fp) == 32


def test_acoustic_fingerprint_changes_over_time():
    src = MicrophoneEntropySource(SimulatedAudioBackend("acoustic", seed=3))
    a = src.acoustic_fingerprint(window_ms=100)
    time.sleep(0.01)
    b = src.acoustic_fingerprint(window_ms=100)
    assert a != b


def test_preamp_and_acoustic_outputs_independent():
    src = MicrophoneEntropySource(SimulatedAudioBackend("thermal", seed=4))
    seed = src.preamp_sample_raw(32)
    perso = src.acoustic_fingerprint(window_ms=100)
    assert seed != perso
    # Different lengths anyway, but also different byte values up to common len.
    common = min(len(seed), len(perso))
    assert seed[:common] != perso[:common]


def test_status_returns_required_keys():
    src = MicrophoneEntropySource(SimulatedAudioBackend("thermal", seed=5))
    s = src.status()
    required = {
        "backend", "sample_rate", "bit_depth", "processing_free",
        "h_min_estimate", "h_min_source", "total_bytes_produced",
        "health_test_failures", "last_fingerprint_at",
    }
    assert required.issubset(s.keys())


# ---------------------------------------------------------------------------
# Processing detection
# ---------------------------------------------------------------------------


def test_processing_free_on_thermal_backend():
    rep = detect_processing(SimulatedAudioBackend("thermal", seed=6))
    assert rep.processing_free is True


def test_agc_detected_on_agc_backend():
    rep = detect_processing(SimulatedAudioBackend("agc", seed=7))
    assert rep.processing_free is False
    # 'agc' mode lowers crest factor → compression_detected fires; some seeds
    # also trigger AGC via the gain-probe path.
    assert rep.compression_detected or rep.agc_detected


def test_noise_gate_detected_on_silent_backend():
    backend = SimulatedAudioBackend("thermal", seed=8)
    backend.force_zero_run(True)
    rep = detect_processing(backend)
    assert rep.noise_gate_detected is True
    assert rep.processing_free is False


def test_init_raises_on_processing_detected():
    with pytest.raises(ProcessingDetectedError) as ei:
        MicrophoneEntropySource(SimulatedAudioBackend("agc", seed=9))
    assert ei.value.report.processing_free is False


def test_init_allows_processing_with_flag_false():
    # Must not raise even though processing is detected.
    src = MicrophoneEntropySource(
        SimulatedAudioBackend("agc", seed=10),
        require_processing_free=False,
    )
    assert src.status()["processing_free"] is False


# ---------------------------------------------------------------------------
# Silence probe
# ---------------------------------------------------------------------------


def test_silence_probe_no_tonal_content_thermal():
    src = MicrophoneEntropySource(SimulatedAudioBackend("thermal", seed=11))
    assert src.status()["silence_probe"]["tonal_content_detected"] in (False, True)
    # On the deterministic seed, thermal mode should be tonal-free; assert it.
    assert src.status()["silence_probe"]["tonal_content_detected"] is False


def test_silence_probe_tonal_content_acoustic():
    src = MicrophoneEntropySource(SimulatedAudioBackend("acoustic", seed=12))
    assert src.status()["silence_probe"]["tonal_content_detected"] is True


def test_silence_probe_does_not_block_operation():
    # 'acoustic' mode has tonal content but must still allow init.
    src = MicrophoneEntropySource(SimulatedAudioBackend("acoustic", seed=13))
    out = src.preamp_sample_raw(32)
    assert len(out) == 32


# ---------------------------------------------------------------------------
# Health tests
# ---------------------------------------------------------------------------


def test_health_tests_pass_thermal_noise():
    src = MicrophoneEntropySource(SimulatedAudioBackend("thermal", seed=14))
    # Run several blocks to exercise APT.
    out = src.preamp_sample_raw(1024)
    assert len(out) == 1024
    assert src.status()["health_test_failures"] == 0


def test_health_tests_fail_constant_signal():
    backend = SimulatedAudioBackend("thermal", seed=15)
    backend.force_zero_run(True)
    # Init will fail processing detection first (zero run is a noise gate
    # signature). Bypass via require_processing_free=False so we exercise
    # the health-test fail path directly.
    src = MicrophoneEntropySource(backend, require_processing_free=False)
    with pytest.raises(HealthTestFailureError):
        src.preamp_sample_raw(256)
    assert src.status()["health_test_failures"] == 1


def test_health_test_extraction_refactored():
    """RCT / APT live in entropy.health_tests, not in the microphone module."""
    import hybrid_kem.entropy.microphone_entropy_source as mic_mod
    import hybrid_kem.entropy.health_tests as ht_mod
    src = inspect.getsource(mic_mod)
    # Microphone module imports rct/apt/run_health_tests from health_tests
    # and does not define its own RCT/APT logic.
    assert "from .health_tests import" in src
    assert "def rct(" not in src.replace("rct as ", "")
    assert "def apt(" not in src.replace("apt as ", "")
    # Make sure the canonical implementations exist there.
    assert hasattr(ht_mod, "rct")
    assert hasattr(ht_mod, "apt")
    assert hasattr(ht_mod, "run_health_tests")


# ---------------------------------------------------------------------------
# H_min estimation
# ---------------------------------------------------------------------------


def test_h_min_estimation_returns_all_keys():
    """Use a non-Simulated-named backend by subclassing the simulated one."""

    class _FakeHardwareAudioBackend(SimulatedAudioBackend):
        pass

    src = MicrophoneEntropySource(
        _FakeHardwareAudioBackend("thermal", seed=16),
        require_processing_free=False,   # subclass name still trips the guard
    )
    # We need to defeat the SimulatedAudioBackend isinstance check; the
    # cleanest way for the test is to swap the backend post-init with a
    # truly-non-Simulated wrapper.
    class _RealHardwareAudioBackend:
        def __init__(self, inner):
            self._inner = inner

        def read_samples(self, n, sr=44_100, bd=16):
            return self._inner.read_samples(n, sr, bd)

        def device_info(self):
            d = self._inner.device_info()
            d["device_name"] = "fake-hardware"
            return d

    src._backend = _RealHardwareAudioBackend(
        SimulatedAudioBackend("thermal", seed=17)
    )
    out = src.run_h_min_estimation(n_samples=8192)
    required = {
        "h_min_mcv", "h_min_collision", "h_min_markov",
        "h_min_compression", "h_min_conservative",
        "n_samples", "sample_rate", "bit_depth", "backend_class",
        "estimated_at",
    }
    assert required.issubset(out.keys())


def test_h_min_conservative_is_minimum():
    class _RealHardwareAudioBackend:
        def __init__(self, inner):
            self._inner = inner

        def read_samples(self, n, sr=44_100, bd=16):
            return self._inner.read_samples(n, sr, bd)

        def device_info(self):
            return self._inner.device_info() | {"device_name": "fake-hw"}

    inner = SimulatedAudioBackend("thermal", seed=18)
    src = MicrophoneEntropySource(inner)
    src._backend = _RealHardwareAudioBackend(inner)
    out = src.run_h_min_estimation(n_samples=8192)
    assert out["h_min_conservative"] == min(
        out["h_min_mcv"], out["h_min_collision"],
        out["h_min_markov"], out["h_min_compression"],
    )


def test_simulated_estimation_blocked():
    src = MicrophoneEntropySource(SimulatedAudioBackend("thermal", seed=19))
    with pytest.raises(SimulatedEstimationError):
        src.run_h_min_estimation(n_samples=4096)


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------


def test_pipeline_integration():
    """Quartz → preamp_sample_raw → DRBG with acoustic personalisation."""
    src = MicrophoneEntropySource(SimulatedAudioBackend("thermal", seed=20))
    seed = src.preamp_sample_raw(48)
    perso = src.acoustic_fingerprint(window_ms=100)
    drbg = DRBG(HMAC_SHA256)
    drbg.instantiate(
        entropy_input=seed[:32],
        nonce=seed[32:48],
        personalization=perso,
    )
    assert drbg.state == "instantiated"
    assert len(drbg.generate(64)) == 64


def test_wrong_channel_mixing_is_higher_entropy_floor_doc():
    """Documentation test — mixing channels still hashes through SHA-256,
    so the resulting bytes look uniform. The point of this test is to
    record that mixing is detectable only at the *architectural* level
    (it's an interface defect, not an output-distribution defect).
    Brief 06 explicitly asks for this as a comment/note test.
    """
    src = MicrophoneEntropySource(SimulatedAudioBackend("thermal", seed=21))
    seed = src.preamp_sample_raw(32)
    perso = src.acoustic_fingerprint(window_ms=100)
    bad_mix = seed + perso
    # Both halves are SHA-256 outputs; concatenation is still uniform-looking.
    # We just confirm the bytes are different from either half alone — the
    # security defect is architectural, not statistical.
    assert bad_mix[:32] != bad_mix[32:]
    assert len(bad_mix) == 64
