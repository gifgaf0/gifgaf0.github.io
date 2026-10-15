"""End-to-end smoke demo for the hybrid PQC KEM.

Runs, for each profile (X-Wing and ML-KEM-1024 + X25519):
1. Build a QRNGSource in local-only mode with SP 800-90B health tests.
2. Seed an SP 800-90A HMAC-DRBG-SHA256 from it.
3. Run hybrid keygen / encaps / decaps and assert the recovered shared secret
   matches the encapsulated one.

Intended as a quick "does the wire actually carry voltage" check after a fresh
checkout. Not a benchmark and not a security argument.
"""

from __future__ import annotations

import logging

from hybrid_kem.entropy.drbg import DRBG, HMAC_SHA256
from hybrid_kem.entropy.health_tests import HealthTests
from hybrid_kem.entropy.qrng_source import QRNGSource
from hybrid_kem.hybrid_kem import PROFILES, HybridKEM


def _seeded_drbg() -> DRBG:
    src = QRNGSource(provider="local", health_test=HealthTests(), mix_with_os=True)
    seed = src.get_bytes(48)
    drbg = DRBG(HMAC_SHA256)
    drbg.instantiate(seed[:32], seed[32:48], b"hybrid-kem-demo")
    return drbg


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    log = logging.getLogger("demo")

    for profile in PROFILES:
        h = HybridKEM(profile=profile)
        log.info("profile=%s  category=%d  post-quantum=%s",
                 profile, h.nist_category, h.is_post_quantum)

        pk, sk = h.keygen(_seeded_drbg())
        ct, ss_enc = h.encaps(pk, _seeded_drbg())
        ss_dec = h.decaps(sk, ct)

        assert ss_enc == ss_dec, "decaps did not recover the encapsulated secret"
        log.info("  pk=%d B  sk=%d B  ct=%d B  ss=%s",
                 len(pk), len(sk), len(ct), ss_enc.hex())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
