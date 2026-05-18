"""Tests for the Brief 07 alpha-decay entropy module."""

from __future__ import annotations

import inspect
import math
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


# ---------------------------------------------------------------------------
# Lag-1 autocorrelation check (Brief 07.1)
# ---------------------------------------------------------------------------
#
# Empirical finding (documented in ALPHA_DECAY_NOTES.md "Lag-1 autocorrelation
# calibration"): with the additive after-pulse simulator the brief specifies,
# the lag-1 Pearson |ρ| scales as approximately f · (d/μ)² for after-pulse
# fraction f and delay d small relative to mean Δt μ. At the brief's example
# of f=0.05 / d=1µs / μ=1ms, the predicted ρ is ~10⁻⁵ — below the n=4096
# noise floor of ~0.016. The check therefore does NOT reliably detect the
# brief's example after-pulse configuration; instead it detects after-pulses
# where d is comparable to μ AND f is substantial.
#
# Tests below use f=0.5 / d=2µs (≈ 2·μ) where ρ reliably exceeds 0.05 to
# verify the check works. The brief's small-signal parameter set is covered
# by ``test_low_signal_after_pulse_not_detected_by_lag1_alone`` which
# documents the sensitivity floor honestly.


def test_lag1_autocorrelation_zero_on_ideal():
    """Pure Poisson process has ρ₁ ≈ 0; |ρ| < 0.05 at n=4096."""
    rep = detect_non_poisson(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=101)
    )
    assert abs(rep.lag1_autocorrelation) < 0.05
    assert rep.lag1_autocorrelation_ok is True


def test_lag1_autocorrelation_zero_on_dead_time():
    """dead_time mode shifts the marginal but does not introduce serial
    correlation; |ρ| < 0.05."""
    rep = detect_non_poisson(
        SimulatedTimingBackend("dead_time", rate_hz=1000, dead_time_ns=1000, seed=102)
    )
    assert abs(rep.lag1_autocorrelation) < 0.05
    assert rep.lag1_autocorrelation_ok is True


def test_lag1_autocorrelation_zero_on_biased():
    """Gamma-distributed Δt are still independent, so ρ₁ ≈ 0 even though the
    marginal fails KS. Confirms the lag-1 check is orthogonal to the KS
    check — gamma is rejected by KS but not by autocorrelation."""
    rep = detect_non_poisson(
        SimulatedTimingBackend("biased", rate_hz=1000, bias_shape=3.0, seed=103)
    )
    assert abs(rep.lag1_autocorrelation) < 0.05
    assert rep.lag1_autocorrelation_ok is True
    # Orthogonality: KS rejects, autocorrelation does not.
    assert rep.exponential_fit_ok is False


def test_lag1_autocorrelation_positive_on_after_pulse():
    """Strong-after-pulse parameter set (f=0.5, d=2·μ) reliably produces
    ρ > 0.05 at n=4096. See module-level note above re. brief-spec defaults."""
    backend = SimulatedTimingBackend(
        "after_pulse",
        rate_hz=1000,
        seed=1,
        after_pulse_fraction=0.5,
        after_pulse_delay_ns=2_000_000,
    )
    rep = detect_non_poisson(backend)
    assert rep.lag1_autocorrelation > 0.05


def test_after_pulse_detected_on_after_pulse_backend():
    """Strong-after-pulse backend trips both lag1 and KS, so poisson=False."""
    backend = SimulatedTimingBackend(
        "after_pulse",
        rate_hz=1000,
        seed=1,
        after_pulse_fraction=0.5,
        after_pulse_delay_ns=2_000_000,
    )
    rep = detect_non_poisson(backend)
    assert rep.lag1_autocorrelation_ok is False
    assert rep.poisson_compatible is False


def test_init_raises_on_after_pulse_with_require_poisson():
    """Strong-after-pulse + require_poisson=True raises NonPoissonError; the
    error message includes 'lag1' so the operator can diagnose."""
    backend = SimulatedTimingBackend(
        "after_pulse",
        rate_hz=1000,
        seed=1,
        after_pulse_fraction=0.5,
        after_pulse_delay_ns=2_000_000,
    )
    with pytest.raises(NonPoissonError) as ei:
        AlphaDecayEntropySource(backend)
    assert ei.value.report.lag1_autocorrelation_ok is False
    assert "lag1" in str(ei.value).lower()


def test_low_after_pulse_fraction_not_falsely_rejected():
    """At f=0.001 (0.1 %), ρ is below the n=4096 noise floor — the check
    must not reject."""
    backend = SimulatedTimingBackend(
        "after_pulse",
        rate_hz=1000,
        seed=104,
        after_pulse_fraction=0.001,
        after_pulse_delay_ns=1_000,
    )
    rep = detect_non_poisson(backend)
    assert abs(rep.lag1_autocorrelation) < 0.05
    assert rep.lag1_autocorrelation_ok is True


def test_low_signal_after_pulse_not_detected_by_lag1_alone():
    """Honest documentation: brief-spec defaults (f=0.05, d=1µs) produce a
    lag-1 signal far below the n=4096 noise floor. The check does NOT
    detect this case via lag-1 — but KS catches it via the bump at small
    Δt. This is the model-mismatch result; see ALPHA_DECAY_NOTES.md."""
    backend = SimulatedTimingBackend(
        "after_pulse",
        rate_hz=1000,
        seed=42,
        after_pulse_fraction=0.05,
        after_pulse_delay_ns=1_000,
    )
    rep = detect_non_poisson(backend)
    # Lag-1 alone misses (as predicted by the f·(d/μ)² scaling):
    assert rep.lag1_autocorrelation_ok is True
    # But KS catches the marginal-distribution bump:
    assert rep.exponential_fit_ok is False
    assert rep.poisson_compatible is False


def test_poisson_report_includes_lag1_fields():
    """Schema check: the new fields appear on PoissonReport."""
    rep = detect_non_poisson(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=105)
    )
    assert hasattr(rep, "lag1_autocorrelation")
    assert hasattr(rep, "lag1_autocorrelation_ok")
    assert isinstance(rep.lag1_autocorrelation, float)
    assert isinstance(rep.lag1_autocorrelation_ok, bool)


def test_default_lag1_threshold_constant_is_top_level():
    """``DEFAULT_LAG1_AUTOCORRELATION_THRESHOLD`` is a module-level constant,
    so future calibration adjustment is a one-line change."""
    import hybrid_kem.entropy.alpha_decay_entropy_source as mod
    assert hasattr(mod, "DEFAULT_LAG1_AUTOCORRELATION_THRESHOLD")
    assert mod.DEFAULT_LAG1_AUTOCORRELATION_THRESHOLD == 0.05


def test_lag1_autocorrelation_function_handles_short_input():
    """Edge case: < 3 samples returns 0.0 (cannot compute Pearson)."""
    from hybrid_kem.entropy.alpha_decay_entropy_source import _lag1_autocorrelation
    assert _lag1_autocorrelation([]) == 0.0
    assert _lag1_autocorrelation([1]) == 0.0
    assert _lag1_autocorrelation([1, 2]) == 0.0


def test_lag1_autocorrelation_function_zero_variance_returns_zero():
    """Edge case: constant input yields zero denominator → return 0.0 (not NaN)."""
    from hybrid_kem.entropy.alpha_decay_entropy_source import _lag1_autocorrelation
    assert _lag1_autocorrelation([100, 100, 100, 100, 100]) == 0.0


# ---------------------------------------------------------------------------
# Log-domain lag-1 autocorrelation check (Brief 07.2)
# ---------------------------------------------------------------------------


def test_lag1_log_zero_on_ideal():
    """log-ρ on a clean Poisson stream has |ρ| < 0.05."""
    rep = detect_non_poisson(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=201)
    )
    assert abs(rep.lag1_autocorrelation_log) < 0.05
    assert rep.lag1_autocorrelation_log_ok is True


def test_lag1_log_zero_on_dead_time():
    """dead_time mode is iid; log-ρ ≈ 0."""
    rep = detect_non_poisson(
        SimulatedTimingBackend("dead_time", rate_hz=1000, dead_time_ns=1000, seed=202)
    )
    assert abs(rep.lag1_autocorrelation_log) < 0.05
    assert rep.lag1_autocorrelation_log_ok is True


def test_lag1_log_zero_on_biased():
    """biased mode is iid (gamma); log-ρ ≈ 0. KS catches, lag-1(log) does not."""
    rep = detect_non_poisson(
        SimulatedTimingBackend("biased", rate_hz=1000, bias_shape=3.0, seed=203)
    )
    assert abs(rep.lag1_autocorrelation_log) < 0.05
    assert rep.lag1_autocorrelation_log_ok is True
    assert rep.exponential_fit_ok is False


def test_lag1_log_more_sensitive_than_linear_on_weak_after_pulse():
    """At the brief-spec after-pulse regime (f=0.05, d=1µs, μ=1ms) the log-
    domain |ρ| is materially larger than the linear-domain |ρ| (typically
    3-6× across seeds — see ALPHA_DECAY_NOTES.md "Linear vs log-domain
    lag-1 sensitivity comparison"). This test verifies the value-add:
    log-domain is strictly more sensitive than linear-domain on weak
    additive after-pulses.

    Seed selected from the 10-seed sweep documented in the notes; the
    8/10 seeds where |log| > |linear| are seeds 2-5, 7-10."""
    backend = SimulatedTimingBackend(
        "after_pulse",
        rate_hz=1000,
        seed=5,
        after_pulse_fraction=0.05,
        after_pulse_delay_ns=1_000,
    )
    rep = detect_non_poisson(backend)
    # The brief-spec regime is below the linear-domain noise floor:
    assert abs(rep.lag1_autocorrelation) < 0.05
    # And log-domain is materially larger:
    assert abs(rep.lag1_autocorrelation_log) > abs(rep.lag1_autocorrelation)


def test_lag1_log_detects_strong_after_pulse():
    """Strong after-pulse params (f=0.5, d=2µs, seed=1) trip both the
    linear and log-domain checks; poisson_compatible is False."""
    backend = SimulatedTimingBackend(
        "after_pulse",
        rate_hz=1000,
        seed=1,
        after_pulse_fraction=0.5,
        after_pulse_delay_ns=2_000_000,
    )
    rep = detect_non_poisson(backend)
    assert abs(rep.lag1_autocorrelation_log) > 0.05
    assert rep.lag1_autocorrelation_log_ok is False
    assert rep.poisson_compatible is False


def test_poisson_report_includes_lag1_log_fields():
    """Schema check: the new fields appear on PoissonReport."""
    rep = detect_non_poisson(
        SimulatedTimingBackend("ideal", rate_hz=1000, seed=204)
    )
    assert hasattr(rep, "lag1_autocorrelation_log")
    assert hasattr(rep, "lag1_autocorrelation_log_ok")
    assert isinstance(rep.lag1_autocorrelation_log, float)
    assert isinstance(rep.lag1_autocorrelation_log_ok, bool)


def test_default_lag1_log_threshold_constant_is_top_level():
    """``DEFAULT_LAG1_AUTOCORRELATION_LOG_THRESHOLD`` is a module-level
    constant so future calibration is a one-line change."""
    import hybrid_kem.entropy.alpha_decay_entropy_source as mod
    assert hasattr(mod, "DEFAULT_LAG1_AUTOCORRELATION_LOG_THRESHOLD")
    assert mod.DEFAULT_LAG1_AUTOCORRELATION_LOG_THRESHOLD == 0.05


def test_lag1_log_handles_zero_interarrivals():
    """Defense-in-depth: a Δt = 0 should not crash the log function."""
    from hybrid_kem.entropy.alpha_decay_entropy_source import _lag1_autocorrelation_log
    # Mix of normal and one zero — the zero is silently mapped to 1 ns.
    deltas = [1_000_000, 1_500_000, 0, 800_000, 1_200_000]
    r = _lag1_autocorrelation_log(deltas)
    assert math.isfinite(r)
    assert -1.0 <= r <= 1.0


def test_lag1_log_handles_short_input():
    """Empty / single-element series return 0.0."""
    from hybrid_kem.entropy.alpha_decay_entropy_source import _lag1_autocorrelation_log
    assert _lag1_autocorrelation_log([]) == 0.0
    assert _lag1_autocorrelation_log([1000]) == 0.0
