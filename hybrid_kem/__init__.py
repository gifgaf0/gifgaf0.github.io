"""Hybrid PQC testbed package root.

The public surface deliberately stays narrow: the hybrid KEM and the
entropy primitives. Submodules expose more for testing and integration.
"""

from .combiner.kdf_combiner import combine as combine_kems
from .entropy import DRBG, HealthTests, QRNGSource
from .hybrid_kem import HybridKEM
from .sig_composite.composite_mldsa import CompositeMLDSA

__all__ = [
    "DRBG",
    "CompositeMLDSA",
    "HealthTests",
    "HybridKEM",
    "QRNGSource",
    "combine_kems",
]

__version__ = "0.1.0"
