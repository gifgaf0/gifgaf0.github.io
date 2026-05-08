"""KEM combiner per Bindel-Brendel-Fischlin-Goncalves-Stebila 2019, §3.2.

Construction:
    salt = SHA256("hybrid-kem-v1")
    ikm  = ss_A || ss_B
    info = ct_A || ct_B || pk_A || pk_B
    ss_final = HKDF(SHA256, salt, ikm, info, 32)

Including the ciphertexts and public keys in ``info`` binds the shared secret
to the full transcript (transcript-binding combiner). This prevents the
"duplicating-ciphertext" class of attacks in BBF-G-S §4.

The combiner is IND-CCA2 secure if **either** ss_A or ss_B is secure, given
that HKDF acts as a PRF when keyed by either input alone (the dual-PRF
assumption discussed in BBF-G-S §3).
"""

from __future__ import annotations

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

COMBINER_LABEL = b"hybrid-kem-v1"
SS_LEN = 32


def _label_salt() -> bytes:
    h = hashes.Hash(hashes.SHA256())
    h.update(COMBINER_LABEL)
    return h.finalize()


def combine(
    ss_a: bytes,
    ss_b: bytes,
    ct_a: bytes,
    ct_b: bytes,
    pk_a: bytes,
    pk_b: bytes,
) -> bytes:
    """Combine two KEM outputs into a single 32-byte shared secret.

    Inputs are passed by length-prefixed concatenation in ``info`` so that
    different splits of the same byte string never collide.
    """
    if not ss_a or not ss_b:
        raise ValueError("both shared secrets must be non-empty")
    info = b"".join(
        len(x).to_bytes(4, "big") + x for x in (ct_a, ct_b, pk_a, pk_b)
    )
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=SS_LEN,
        salt=_label_salt(),
        info=info,
    )
    return hkdf.derive(ss_a + ss_b)
