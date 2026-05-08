"""Hybrid PQC testbed package root.

The public surface deliberately stays narrow: the hybrid KEM and the
entropy primitives. Submodules expose more for testing and integration.
"""

from .combiner.kdf_combiner import combine as combine_kems
from .entropy import DRBG, HealthTests, QRNGSource
from .hybrid_kem import HybridKEM

__all__ = [
    "DRBG",
    "HealthTests",
    "HybridKEM",
    "QRNGSource",
    "combine_kems",
]

__version__ = "0.1.0"
