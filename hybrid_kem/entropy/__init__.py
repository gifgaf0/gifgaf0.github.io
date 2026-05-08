"""Entropy layer for the hybrid PQC testbed.

Provides:
- :class:`HealthTests`  SP 800-90B continuous health tests.
- :class:`DRBG`         SP 800-90A HMAC-DRBG / CTR-DRBG facade.
- :class:`QRNGSource`   Cloud QRNG with offline cache and OS mixing.

See ``hybrid_kem/SPEC.md`` §2.1-§2.3 for the architectural specification.
"""

from .drbg import (
    AES_CTR_256,
    DRBG,
    DRBGStateError,
    HMAC_SHA256,
    RESEED_INTERVAL,
    ReseedRequiredError,
)
from .health_tests import HealthTestFailure, HealthTests, apt_cutoff, rct_cutoff
from .qrng_source import QRNGSource

__all__ = [
    "AES_CTR_256",
    "DRBG",
    "DRBGStateError",
    "HealthTestFailure",
    "HealthTests",
    "HMAC_SHA256",
    "QRNGSource",
    "RESEED_INTERVAL",
    "ReseedRequiredError",
    "apt_cutoff",
    "rct_cutoff",
]
