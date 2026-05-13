"""Tests for the Brief 05 crystal calibration module."""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

import pytest

from hybrid_kem.entropy.crystal_calibrator import (
    CalibrationNotFoundError,
    CrystalCalibrator,
    SimulatedCalibrationError,
    collision_estimate,
    compute_psd,
    estimate_h_min,
    fingerprint_distance,
    markov_estimate,
    mcv_estimate,
)
from hybrid_kem.entropy.drbg import DRBG, HMAC_SHA256
from hybrid_kem.entropy.health_tests import HealthTests
from hybrid_kem.entropy.quartz_entropy_source import (
    FingerprintedSimulatedADCBackend,
    QuartzEntropySource,
    SimulatedADCBackend,
)


KEY32 = b"\xab" * 32


def _make_calibrator(tmp_path, *, samples=4096, n_fft=256):
    return CrystalCalibrator(
        db_path=tmp_path / "calib.jsonl",
        n_fft_bins=n_fft,
        calibration_samples=samples,
    )


# ---------------------------------------------------------------------------
# Functional
# ---------------------------------------------------------------------------


def test_calibrate_produces_fingerprint(tmp_path):
    cal = _make_calibrator(tmp_path)
    adc = FingerprintedSimulatedADCBackend(n_channels=3, seed=1)
    cal.calibrate("crystal_A", channel=0, adc=adc, stress_levels=[0])
    fps = cal.all_fingerprints()
    assert len(fps) == 1
    fp = fps[0]
    assert fp.crystal_id == "crystal_A"
    assert fp.stress_level == 0
    assert fp.sample_count == 4096
    assert sum(fp.psd_profile) == pytest.approx(1.0, abs=1e-6)


def test_calibrate_all_stress_levels(tmp_path):
    cal = _make_calibrator(tmp_path)
    adc = FingerprintedSimulatedADCBackend(n_channels=3, seed=2)
    cal.calibrate("crystal_B", channel=1, adc=adc, stress_levels=[0, 1, 2, 3])
    fps = [fp for fp in cal.all_fingerprints() if fp.crystal_id == "crystal_B"]
    assert len(fps) == 4
    assert {fp.stress_level for fp in fps} == {0, 1, 2, 3}


def test_identify_correct_crystal(tmp_path):
    cal = _make_calibrator(tmp_path)
    adc = FingerprintedSimulatedADCBackend(n_channels=3, seed=3)
    for ch in range(3):
        cal.calibrate(f"crystal_{ch}", channel=ch, adc=adc, stress_levels=[0])
    # Now sample from channel 1 again and ask the calibrator to identify it.
    fresh_adc = FingerprintedSimulatedADCBackend(n_channels=3, seed=4)
    samples = [fresh_adc.read_voltage(1) for _ in range(4096)]
    matches = cal.identify(samples, stress_level=0,
                            sample_rate=adc.sample_rate_hz())
    assert matches, "no matches returned"
    assert matches[0][0] == "crystal_1", matches


def test_identify_returns_sorted_distances(tmp_path):
    cal = _make_calibrator(tmp_path)
    adc = FingerprintedSimulatedADCBackend(n_channels=3, seed=5)
    for ch in range(3):
        cal.calibrate(f"crystal_{ch}", channel=ch, adc=adc, stress_levels=[0])
    samples = [adc.read_voltage(0) for _ in range(4096)]
    matches = cal.identify(samples, stress_level=0,
                            sample_rate=adc.sample_rate_hz())
    distances = [d for _, d in matches]
    assert distances == sorted(distances)


def test_update_health_test_params_returns_dict(tmp_path):
    """Real-hardware backend (mocked as a class with a non-Simulated name)
    is required for `update_health_test_params` to return values.

    We exercise the helper by constructing a fingerprint with a manufactured
    ``backend_class`` field that does not contain 'Simulated' (impersonating
    a real hardware run for the unit test). The function returns a fully
    populated dict.
    """
    cal = _make_calibrator(tmp_path)
    adc = FingerprintedSimulatedADCBackend(n_channels=2, seed=6)
    cal.calibrate("crystal_A", channel=0, adc=adc, stress_levels=[0])
    # Inject a "hardware-class" fingerprint by direct append (test only).
    from hybrid_kem.entropy.crystal_calibrator import CrystalFingerprint
    fake_hw = CrystalFingerprint(
        crystal_id="hw_crystal", stress_level=0,
        psd_profile=[1.0, 0.0],
        psd_bin_hz=1.0,
        h_min_estimate=4.2,
        h_min_method="min(mcv,collision,markov,compression)",
        sample_count=44100,
        calibrated_at="2026-05-13T00:00:00Z",
        backend_class="HardwareADCBackend",   # not "Simulated*"
    )
    cal._append(fake_hw)
    out = cal.update_health_test_params(source=None, stress_level=0,
                                          crystal_id="hw_crystal")
    assert set(out.keys()) >= {"h_min", "rct_cutoff", "apt_window",
                                "apt_cutoff", "source_crystal_id",
                                "source_stress_level", "calibrated_at"}
    assert out["h_min"] > 0
    assert out["source_crystal_id"] == "hw_crystal"


def test_simulated_calibration_blocks_health_update(tmp_path):
    cal = _make_calibrator(tmp_path)
    adc = FingerprintedSimulatedADCBackend(n_channels=2, seed=7)
    cal.calibrate("crystal_A", channel=0, adc=adc, stress_levels=[0])
    with pytest.raises(SimulatedCalibrationError):
        cal.update_health_test_params(source=None, stress_level=0,
                                       crystal_id="crystal_A")


# ---------------------------------------------------------------------------
# Discriminability
# ---------------------------------------------------------------------------


def test_discriminability_report_single_crystal(tmp_path):
    cal = _make_calibrator(tmp_path)
    adc = FingerprintedSimulatedADCBackend(n_channels=2, seed=8)
    cal.calibrate("only_crystal", channel=0, adc=adc, stress_levels=[0])
    rep = cal.discriminability_report(stress_level=0)
    assert rep.puf_assessment == "inconclusive"
    assert "needs >= 2" in rep.notes


def test_discriminability_report_two_distinct_crystals(tmp_path):
    cal = _make_calibrator(tmp_path)
    adc = FingerprintedSimulatedADCBackend(n_channels=3, seed=9)
    for ch in range(3):
        cal.calibrate(f"crystal_{ch}", channel=ch, adc=adc, stress_levels=[0])
    rep = cal.discriminability_report(stress_level=0)
    assert rep.puf_assessment == "supported"
    assert rep.puf_tier == "T2"
    assert rep.min_inter_distance is not None
    assert rep.min_inter_distance > 0.05


def test_discriminability_report_identical_crystals(tmp_path):
    """Same channel calibrated twice under different IDs → no
    inter-crystal separation; expected verdict is falsified."""
    cal = _make_calibrator(tmp_path)
    adc = FingerprintedSimulatedADCBackend(n_channels=2, seed=10)
    cal.calibrate("crystal_alpha", channel=0, adc=adc, stress_levels=[0])
    # Reset the simulator's internal time counter by building a fresh ADC
    # with the same seed so the second calibration is byte-identical.
    adc2 = FingerprintedSimulatedADCBackend(n_channels=2, seed=10)
    cal.calibrate("crystal_beta", channel=0, adc=adc2, stress_levels=[0])
    rep = cal.discriminability_report(stress_level=0)
    # With byte-identical samples the inter-crystal JSD is zero → falsified.
    assert rep.min_inter_distance is not None
    assert rep.min_inter_distance < 0.001
    assert rep.puf_assessment == "falsified"


def test_puf_falsification_text_in_report(tmp_path):
    cal = _make_calibrator(tmp_path)
    adc1 = FingerprintedSimulatedADCBackend(n_channels=2, seed=11)
    adc2 = FingerprintedSimulatedADCBackend(n_channels=2, seed=11)
    cal.calibrate("a", channel=0, adc=adc1, stress_levels=[0])
    cal.calibrate("b", channel=0, adc=adc2, stress_levels=[0])
    out = tmp_path / "report.md"
    cal.export_report(out, stress_level=0)
    text = out.read_text()
    assert "FALSIFIED" in text


# ---------------------------------------------------------------------------
# H_min estimators
# ---------------------------------------------------------------------------


def test_most_common_value_estimate_constant():
    samples = [42] * 1000
    assert mcv_estimate(samples) == pytest.approx(0.0, abs=1e-9)


def test_gaussian_noise_h_min_reasonable():
    # Uniform random samples in [-1, 1]: after byte quantisation the
    # distribution covers the full range, the Markov / collision
    # estimators see broad transition statistics, and the compression
    # estimator can't compress uniform data. All four estimators
    # therefore land well above the 0.5 conservative lower bound.
    rng = random.Random(123)
    samples = [rng.uniform(-1.0, 1.0) for _ in range(8192)]
    h_min, _ = estimate_h_min(samples)
    assert 0.5 <= h_min <= 8.0, h_min


def test_h_min_is_minimum_across_estimators():
    rng = random.Random(456)
    samples = [rng.gauss(0.0, 0.2) for _ in range(4096)]
    h_min, label = estimate_h_min(samples)
    # Re-run individual estimators on the same quantised stream.
    from hybrid_kem.entropy.crystal_calibrator import _quantise_to_byte
    quant = _quantise_to_byte(samples)
    indiv = [
        mcv_estimate(quant),
        collision_estimate(quant),
        markov_estimate(quant),
    ]
    from hybrid_kem.entropy.crystal_calibrator import compression_estimate
    indiv.append(compression_estimate(quant))
    assert h_min == pytest.approx(min(indiv), abs=1e-9)
    assert "min(" in label


# ---------------------------------------------------------------------------
# Tamper-detection hook on QuartzEntropySource
# ---------------------------------------------------------------------------


def test_verify_identity_correct_crystal_passes(tmp_path):
    cal = _make_calibrator(tmp_path, samples=4096, n_fft=256)
    adc = FingerprintedSimulatedADCBackend(n_channels=2, seed=12)
    cal.calibrate("crystal_A", channel=0, adc=adc, stress_levels=[1])
    src = QuartzEntropySource(
        adc, KEY32, n_keyed_crystals=2,
        commitment_log_path=tmp_path / "commits.jsonl",
        window_ms=200, min_dwell_ms=50,
    )
    audit_log = tmp_path / "identity_audit.jsonl"
    ok = src.verify_crystal_identity(
        cal, channel=0, crystal_id="crystal_A", stress_level=1,
        n_verification_samples=2048,
        threshold=0.5,                   # generous; tonal signal is highly distinct
        audit_log=audit_log,
    )
    assert ok is True
    assert audit_log.exists()


def test_verify_identity_wrong_crystal_fails(tmp_path):
    cal = _make_calibrator(tmp_path, samples=4096, n_fft=256)
    adc = FingerprintedSimulatedADCBackend(n_channels=2, seed=13)
    cal.calibrate("crystal_A", channel=0, adc=adc, stress_levels=[1])
    cal.calibrate("crystal_B", channel=1, adc=adc, stress_levels=[1])
    src = QuartzEntropySource(
        adc, KEY32, n_keyed_crystals=2,
        commitment_log_path=tmp_path / "commits.jsonl",
        window_ms=200, min_dwell_ms=50,
    )
    audit_log = tmp_path / "identity_audit.jsonl"
    # Verify channel 1 samples *against* crystal_A's fingerprint — should fail.
    ok = src.verify_crystal_identity(
        cal, channel=1, crystal_id="crystal_A", stress_level=1,
        n_verification_samples=2048,
        threshold=0.10,                  # tight enough to separate distinct tones
        audit_log=audit_log,
    )
    assert ok is False


def test_verify_identity_logged(tmp_path):
    cal = _make_calibrator(tmp_path, samples=2048, n_fft=256)
    adc = FingerprintedSimulatedADCBackend(n_channels=2, seed=14)
    cal.calibrate("crystal_A", channel=0, adc=adc, stress_levels=[0])
    src = QuartzEntropySource(
        adc, KEY32, n_keyed_crystals=2,
        commitment_log_path=tmp_path / "commits.jsonl",
        window_ms=200, min_dwell_ms=50,
    )
    audit_log = tmp_path / "identity_audit.jsonl"
    for _ in range(3):
        src.verify_crystal_identity(
            cal, channel=0, crystal_id="crystal_A", stress_level=0,
            n_verification_samples=1024, audit_log=audit_log,
        )
    lines = audit_log.read_text().splitlines()
    assert len(lines) == 3
    for line in lines:
        rec = json.loads(line)
        assert "result" in rec
        assert "distance" in rec
        assert "timestamp_utc" in rec


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------


def test_full_calibration_pipeline(tmp_path):
    """Calibrate 3 channels → discriminability report → sample_raw works."""
    cal = _make_calibrator(tmp_path, samples=2048, n_fft=256)
    adc = FingerprintedSimulatedADCBackend(n_channels=3, seed=15)
    for ch in range(3):
        cal.calibrate(f"crystal_{ch}", channel=ch, adc=adc, stress_levels=[0, 1])
    rep = cal.discriminability_report(stress_level=0)
    assert rep.puf_assessment in ("supported", "inconclusive", "falsified")
    src = QuartzEntropySource(
        adc, KEY32, n_keyed_crystals=3,
        commitment_log_path=tmp_path / "commits.jsonl",
        window_ms=200, min_dwell_ms=50,
    )
    # sample_raw uses an internal HealthTests, not the calibrated one;
    # we just confirm the pipeline runs end-to-end.
    out = src.sample_raw(64)
    assert len(out) == 64


def test_export_report_writes_file(tmp_path):
    cal = _make_calibrator(tmp_path, samples=2048, n_fft=256)
    adc = FingerprintedSimulatedADCBackend(n_channels=3, seed=16)
    for ch in range(3):
        cal.calibrate(f"crystal_{ch}", channel=ch, adc=adc, stress_levels=[0])
    out = tmp_path / "calibration_report.md"
    cal.export_report(out, stress_level=0)
    text = out.read_text()
    assert "PUF assessment" in text
    assert "Pairwise distances" in text
    assert len(text) > 200
