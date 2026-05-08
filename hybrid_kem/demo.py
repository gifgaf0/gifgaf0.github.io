"""End-to-end smoke demo for the hybrid PQC testbed.

Runs:
1. Build a QRNGSource in local-only mode with health tests applied.
2. Seed a HMAC-DRBG-SHA256 from it.
3. Run hybrid keygen / encaps / decaps; assert the recovered shared secret
   matches the encapsulated one.

Intended as a quick "does the wire actually carry voltage" check after a
fresh checkout. Not a benchmark and not a security argument.
"""

from __future__ import annotations

import logging

from hybrid_kem.entropy.drbg import DRBG, HMAC_SHA256
from hybrid_kem.entropy.health_tests import HealthTests
from hybrid_kem.entropy.qrng_source import QRNGSource
from hybrid_kem.hybrid_kem import HybridKEM


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    log = logging.getLogger("demo")

    src = QRNGSource(provider="local", health_test=HealthTests(), mix_with_os=True)
    seed = src.get_bytes(48)

    drbg = DRBG(HMAC_SHA256)
    drbg.instantiate(seed[:32], seed[32:48], b"hybrid-kem-demo")

    h = HybridKEM(standard_backend="auto", slwe_mode="stub")
    log.info("standard backend = %s (post-quantum=%s)", h.standard.backend, h.is_post_quantum)

    pk, sk = h.keygen(drbg)
    ct, ss_enc = h.encaps(pk, drbg)
    ss_dec = h.decaps(sk, ct)

    assert ss_enc == ss_dec, "decaps did not recover the encapsulated secret"
    log.info("hybrid_pk = %d bytes", len(pk))
    log.info("hybrid_sk = %d bytes", len(sk))
    log.info("hybrid_ct = %d bytes", len(ct))
    log.info("ss_final  = %s", ss_enc.hex())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
