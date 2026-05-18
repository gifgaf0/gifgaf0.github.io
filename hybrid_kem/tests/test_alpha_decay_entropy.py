"""Tests for the Brief 07 alpha-decay entropy module."""

from __future__ import annotations

import inspect
import time

import pytest

from hybrid_kem.entropy.alpha_decay_entropy_source import (
    AlphaDecayEntropySource,
    HealthTestFailureError,
    NonPoissonError,
    PoissonReport,
    SimulatedEstimationError,
    SimulatedTimingBackend,
    detect_non_poisson,
)
from hybrid_kem.entropy.drbg import DRBG, HMAC_SHA256

# ---------------------------------------------------------------------------
# Functional
# ---------------------------------------------------------------------------


def test_interarrival_sample_raw_produces_output():
    src = AlphaDecayEntropySource(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=1)
    )
    out = src.interarrival_sample_raw(64)
    assert isinstance(out, bytes)
    assert len(out) == 64


def test_count_rate_fingerprint_is_32_bytes():
    src = AlphaDecayEntropySource(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=2)
    )
    fp = src.count_rate_fingerprint()
    assert len(fp) == 32


def test_count_rate_fingerprint_changes_over_time():
    src = AlphaDecayEntropySource(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=3)
    )
    a = src.count_rate_fingerprint()
    time.sleep(0.001)
    b = src.count_rate_fingerprint()
    assert a != b


def test_status_returns_required_keys():
    src = AlphaDecayEntropySource(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=4)
    )
    s = src.status()
    required = {
        "detector_info",
        "last_rate_estimate_hz",
        "last_poisson_report",
        "samples_drawn_session",
        "bytes_emitted_session",
        "health_test_failures_session",
        "h_min_per_sample_bits",
        "quantizer_bits",
    }
    assert required.issubset(s.keys())


def test_channel_separation_independent_outputs():
    src = AlphaDecayEntropySource(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=5)
    )
    seed = src.interarrival_sample_raw(32)
    perso = src.count_rate_fingerprint()
    # Different byte streams (Channel A vs Channel B).
    assert seed != perso
    # And they update separate counters.
    assert src.status()["bytes_emitted_session"] == 32


# ---------------------------------------------------------------------------
# Detector characterisation
# ---------------------------------------------------------------------------


def test_poisson_compatible_on_ideal_backend():
    rep = detect_non_poisson(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=6)
    )
    assert isinstance(rep, PoissonReport)
    assert rep.poisson_compatible is True
    assert rep.rate_stable is True
    assert rep.exponential_fit_ok is True
    assert rep.dead_time_ok is True


def test_poisson_compatible_on_realistic_dead_time_backend():
    # Realistic detector dead time at default 1 µs / 1 kHz: τλ ≈ 1e-3,
    # KS-fit still passes.
    rep = detect_non_poisson(
        SimulatedTimingBackend("dead_time", rate_hz=1000, dead_time_ns=1000, seed=7)
    )
    assert rep.poisson_compatible is True
    assert rep.dead_time_ok is True


def test_non_poisson_detected_on_biased_backend():
    rep = detect_non_poisson(
        SimulatedTimingBackend("biased", rate_hz=1000, bias_shape=3.0, seed=8)
    )
    assert rep.exponential_fit_ok is False
    assert rep.poisson_compatible is False


def test_sub_dead_time_events_caught():
    """Backend that emits some Δt < dead_time_ns fails the dead-time check."""
    backend = SimulatedTimingBackend(
        "ideal", rate_hz=1000, dead_time_ns=2_000_000, seed=9,
    )
    # Mode 'ideal' generates Δt ~ Exp(λ) without enforcing dead time, so a
    # declared dead_time_ns of 2 ms (≈ 2× mean Δt) catches plenty.
    backend.force_sub_dead_time_rate(0.1)
    rep = detect_non_poisson(backend)
    assert rep.dead_time_ok is False
    assert rep.sub_dead_time_events > 0
    assert rep.poisson_compatible is False


def test_init_raises_on_non_poisson():
    with pytest.raises(NonPoissonError) as ei:
        AlphaDecayEntropySource(
            SimulatedTimingBackend("biased", rate_hz=1000, seed=10)
        )
    assert ei.value.report.poisson_compatible is False
    assert ei.value.report.exponential_fit_ok is False


def test_init_allows_non_poisson_with_flag_false():
    src = AlphaDecayEntropySource(
        SimulatedTimingBackend("biased", rate_hz=1000, seed=11),
        require_poisson=False,
    )
    # Status reflects the absence of a Poisson report.
    assert src.status()["last_poisson_report"] is None


# ---------------------------------------------------------------------------
# CDF transform correctness
# ---------------------------------------------------------------------------


def test_cdf_transform_produces_uniform_distribution():
    """1 - exp(-λ·Δt) on Exp(λ) inputs gives U[0,1) — KS-test against uniform."""
    from scipy import stats  # type: ignore[import-not-found]
    backend = SimulatedTimingBackend("ideal", rate_hz=1000, seed=12)
    timestamps = backend.read_events(10_001)
    deltas = [timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))]
    lam = AlphaDecayEntropySource._estimate_lambda(deltas)
    import math
    u = [1.0 - math.exp(-lam * d) for d in deltas]
    ks = stats.kstest(u, "uniform")
    assert ks.pvalue > 0.01, f"KS p={ks.pvalue} — u_i not uniform"


def test_cdf_transform_robust_to_rate_estimation_error():
    """A ±20 % wrong λ still yields a stream that passes RCT + APT."""
    backend = SimulatedTimingBackend("ideal", rate_hz=1000, seed=13)
    src = AlphaDecayEntropySource(backend)
    # Drive the CDF transform directly with a deliberately wrong rate.
    timestamps = backend.read_events(513)
    deltas = [timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))]
    true_lam = AlphaDecayEntropySource._estimate_lambda(deltas)
    for scale in (0.8, 1.2):
        wrong_lam = true_lam * scale
        out_bytes = src._cdf_quantize(deltas, wrong_lam)
        # Health tests must pass on the byte stream.
        result = src._run_health_tests_or_raise(list(out_bytes))
        assert result.passed


# ---------------------------------------------------------------------------
# Health tests
# ---------------------------------------------------------------------------


def test_health_tests_pass_ideal_backend():
    src = AlphaDecayEntropySource(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=14)
    )
    # Several blocks to exercise APT.
    out = src.interarrival_sample_raw(2048)
    assert len(out) == 2048
    assert src.status()["health_test_failures_session"] == 0


def test_health_tests_fail_constant_signal():
    backend = SimulatedTimingBackend("ideal", rate_hz=1000, seed=15)
    src = AlphaDecayEntropySource(backend)
    # Now force the backend into constant Δt — exp(-λ·const) is a single
    # value, so every quantised byte is identical and RCT will fire.
    backend.force_constant_interarrival(True)
    with pytest.raises(HealthTestFailureError):
        src.interarrival_sample_raw(256)
    assert src.status()["health_test_failures_session"] == 1


def test_health_test_extraction_shared():
    """RCT / APT live in entropy.health_tests, not in the alpha module."""
    import hybrid_kem.entropy.alpha_decay_entropy_source as alpha_mod
    import hybrid_kem.entropy.health_tests as ht_mod
    src = inspect.getsource(alpha_mod)
    assert "from .health_tests import" in src
    # The alpha module must not redefine RCT / APT.
    assert "def rct(" not in src
    assert "def apt(" not in src
    # Canonical implementations are reachable from health_tests.
    assert hasattr(ht_mod, "rct")
    assert hasattr(ht_mod, "apt")
    assert hasattr(ht_mod, "run_health_tests")


# ---------------------------------------------------------------------------
# H_min estimation
# ---------------------------------------------------------------------------


class _RealHardwareTimingBackend:
    """Wrapper that hides the simulated identity from the source's isinstance
    guard. Used purely to exercise the `run_h_min_estimation` happy path
    without real hardware in the test environment."""

    def __init__(self, inner: SimulatedTimingBackend):
        self._inner = inner

    def read_events(self, n_events: int, timeout_s: float = 60.0) -> list[int]:
        return self._inner.read_events(n_events, timeout_s)

    def detector_info(self) -> dict:
        d = self._inner.detector_info()
        d["detector_type"] = "fake-hardware"
        d["detector_serial"] = "FAKE-HW-001"
        return d


def test_h_min_estimation_returns_all_keys():
    inner = SimulatedTimingBackend("ideal", rate_hz=1000, seed=16)
    src = AlphaDecayEntropySource(inner)
    src._backend = _RealHardwareTimingBackend(inner)
    out = src.run_h_min_estimation(n_samples=4096)
    required = {
        "h_min_mcv", "h_min_markov", "h_min_collision",
        "h_min_compression", "h_min_conservative",
        "n_samples", "rate_estimate_hz", "quantizer_bits",
        "backend_class", "estimated_at",
    }
    assert required.issubset(out.keys())


def test_h_min_conservative_is_minimum():
    inner = SimulatedTimingBackend("ideal", rate_hz=1000, seed=17)
    src = AlphaDecayEntropySource(inner)
    src._backend = _RealHardwareTimingBackend(inner)
    out = src.run_h_min_estimation(n_samples=4096)
    assert out["h_min_conservative"] == min(
        out["h_min_mcv"], out["h_min_markov"],
        out["h_min_collision"], out["h_min_compression"],
    )


def test_simulated_estimation_blocked():
    src = AlphaDecayEntropySource(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=18)
    )
    with pytest.raises(SimulatedEstimationError):
        src.run_h_min_estimation(n_samples=4096)


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------


def test_pipeline_integration():
    """AlphaDecay → interarrival_sample_raw → DRBG with count-rate personalisation."""
    src = AlphaDecayEntropySource(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=19)
    )
    seed = src.interarrival_sample_raw(48)
    perso = src.count_rate_fingerprint()
    drbg = DRBG(HMAC_SHA256)
    drbg.instantiate(
        entropy_input=seed[:32],
        nonce=seed[32:48],
        personalization=perso,
    )
    assert drbg.state == "instantiated"
    assert len(drbg.generate(64)) == 64


def test_composition_with_other_sources():
    """AlphaDecay XOR /dev/urandom → IrrationalConditioner → DRBG."""
    from hybrid_kem.entropy.irrational_conditioner import IrrationalConditioner
    from hybrid_kem.entropy.qrng_source import QRNGSource

    src = AlphaDecayEntropySource(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=20)
    )
    alpha_bytes = src.interarrival_sample_raw(48)
    qrng = QRNGSource(provider="local")
    qrng_bytes = qrng.get_bytes(48)
    mixed = bytes(a ^ b for a, b in zip(alpha_bytes, qrng_bytes, strict=True))
    conditioner = IrrationalConditioner(_fake_jitter=b"\x00\x00\x00")
    conditioned = conditioner.condition(mixed)
    drbg = DRBG(HMAC_SHA256)
    drbg.instantiate(
        entropy_input=conditioned[:32],
        nonce=conditioned[32:48],
        personalization=b"",
    )
    assert drbg.state == "instantiated"
    assert len(drbg.generate(32)) == 32


# ---------------------------------------------------------------------------
# Bit-packing helpers (private but unit-testable)
# ---------------------------------------------------------------------------


def test_bit_packing_roundtrip_8():
    from hybrid_kem.entropy.alpha_decay_entropy_source import _pack_bits, _unpack_bits
    symbols = [i % 256 for i in range(100)]
    packed = _pack_bits(symbols, 8)
    assert _unpack_bits(packed, 8, len(symbols)) == symbols


def test_bit_packing_roundtrip_4():
    from hybrid_kem.entropy.alpha_decay_entropy_source import _pack_bits, _unpack_bits
    symbols = [i % 16 for i in range(64)]
    packed = _pack_bits(symbols, 4)
    assert _unpack_bits(packed, 4, len(symbols)) == symbols


def test_bit_packing_roundtrip_16():
    from hybrid_kem.entropy.alpha_decay_entropy_source import _pack_bits, _unpack_bits
    symbols = [(i * 257) % 65536 for i in range(50)]
    packed = _pack_bits(symbols, 16)
    assert _unpack_bits(packed, 16, len(symbols)) == symbols


def test_wrong_channel_mixing_is_architectural_defect_doc():
    """Documentation test — mixing Channel A and Channel B still passes through
    SHA-256 (in the case of count_rate_fingerprint) and looks uniform. The
    defect is architectural (Channel B is not entropy), not statistical."""
    src = AlphaDecayEntropySource(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=21)
    )
    seed = src.interarrival_sample_raw(32)
    perso = src.count_rate_fingerprint()
    bad_mix = seed + perso
    assert bad_mix[:32] != bad_mix[32:]
    assert len(bad_mix) == 64
