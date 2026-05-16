"""Entropy layer for the hybrid PQC testbed.

Provides:
- :class:`HealthTests`        SP 800-90B continuous health tests.
- :class:`DRBG`               SP 800-90A HMAC-DRBG / CTR-DRBG facade.
- :class:`QRNGSource`         Cloud QRNG with offline cache and OS mixing.
- :class:`QuartzEntropySource` (Brief 04) keyed quartz physical entropy.
- :class:`DecoyField`         decoy crystal field for the quartz source.

See ``hybrid_kem/SPEC.md`` §2.1-§2.3 for the architectural specification.
"""

from .crystal_calibrator import (
    CalibrationNotFoundError,
    CalibrationResult,
    CrystalCalibrator,
    CrystalFingerprint,
    DiscriminabilityReport,
    SimulatedCalibrationError,
    compute_psd,
    fingerprint_distance,
)
from .decoy_field import DecoyField
from .drbg import (
    AES_CTR_256,
    DRBG,
    DRBGStateError,
    HMAC_SHA256,
    RESEED_INTERVAL,
    ReseedRequiredError,
)
from .health_tests import (
    DEFAULT_ALPHA,
    HealthTestFailure,
    HealthTestResult,
    HealthTests,
    apt,
    apt_cutoff,
    rct,
    rct_cutoff,
    run_health_tests,
)
from .circle_entropy import (
    DegenerateChordError,
    ECCENTRICITIES,
    chord_angle,
    circle_entropy_seed,
    h_inf_keplerian,
    keplerian_penalty,
    simulate_circle_observation,
    simulate_seed_bytes,
)
from .irrational_conditioner import (
    InsufficientEntropyError,
    IrrationalConditioner,
    OffsetExhaustedError,
)
from .microphone_entropy_source import (
    AudioBackend,
    MicrophoneEntropySource,
    ProcessingDetectedError,
    ProcessingReport,
    PyAudioBackend,
    SilenceProbeResult,
    SimulatedAudioBackend,
    SimulatedEstimationError,
    detect_processing,
)
from .radio_atmospheric_entropy_source import (
    FrequencyOutOfRangeError,
    InsufficientAtmosphericActivityError,
    RadioAtmosphericEntropySource,
    SDRBackend,
    SaturationError,
    SignalPresentError,
    SimulatedSDRBackend,
    SoapySDRBackend,
    detect_saturation,
    detect_strong_signal,
)
from .qrng_source import QRNGSource
from .quartz_entropy_source import (
    ADCBackend,
    FingerprintedSimulatedADCBackend,
    HardwareUnavailableError,
    HealthTestFailureError,
    InsufficientSamplesError,
    QuartzEntropySource,
    ScheduleEntry,
    SerialADCBackend,
    SessionCommitment,
    SimulatedADCBackend,
    StressSchedule,
    derive_stress_schedule,
    make_commitment,
    verify_commitment,
)

__all__ = [
    "ADCBackend",
    "AES_CTR_256",
    "CalibrationNotFoundError",
    "CalibrationResult",
    "CrystalCalibrator",
    "CrystalFingerprint",
    "DRBG",
    "DRBGStateError",
    "DecoyField",
    "DegenerateChordError",
    "DiscriminabilityReport",
    "ECCENTRICITIES",
    "FingerprintedSimulatedADCBackend",
    "HardwareUnavailableError",
    "HealthTestFailure",
    "HealthTestFailureError",
    "HealthTests",
    "HMAC_SHA256",
    "InsufficientEntropyError",
    "InsufficientSamplesError",
    "IrrationalConditioner",
    "OffsetExhaustedError",
    "QRNGSource",
    "QuartzEntropySource",
    "RESEED_INTERVAL",
    "ReseedRequiredError",
    "ScheduleEntry",
    "SerialADCBackend",
    "SessionCommitment",
    "SimulatedADCBackend",
    "SimulatedCalibrationError",
    "StressSchedule",
    "apt_cutoff",
    "chord_angle",
    "circle_entropy_seed",
    "compute_psd",
    "derive_stress_schedule",
    "fingerprint_distance",
    "h_inf_keplerian",
    "keplerian_penalty",
    "make_commitment",
    "rct_cutoff",
    "simulate_circle_observation",
    "simulate_seed_bytes",
    "verify_commitment",
]

