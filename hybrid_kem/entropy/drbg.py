"""SP 800-90A Rev 1 deterministic random bit generators.

Implementations:
- HMAC-DRBG with SHA-256 (§10.1.2), primary.
- CTR-DRBG with AES-256, no derivation function (§10.2.1), alternate.

Both DRBGs share the public ``DRBG`` API. State machine: ``uninstantiated``
-> ``instantiated`` -> ``failed``. ``generate`` raises ``ReseedRequiredError``
when the reseed counter exceeds the configured interval and the caller has
not refreshed entropy.

References:
- NIST SP 800-90A Rev 1, June 2015.
"""

from __future__ import annotations

import hmac
import os
from dataclasses import dataclass
from typing import Optional

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# ---------------------------------------------------------------------------
# Constants per SP 800-90A
# ---------------------------------------------------------------------------

HMAC_SHA256 = "hmac-sha256"
AES_CTR_256 = "aes-ctr-256"

# §10.1.2 / §10.2.1 reseed interval upper bound: 2^48 generate calls.
RESEED_INTERVAL = 1 << 48

# §10.1.2: HMAC-DRBG-SHA256 has security strength 256 bits.
HMAC_SHA256_SECURITY_STRENGTH = 32  # bytes
HMAC_SHA256_OUTLEN = 32

# §10.2.1 Table 3: AES-256 keylen=32, blocklen=16, seedlen = key+block = 48.
AES_KEYLEN = 32
AES_BLOCKLEN = 16
AES_SEEDLEN = AES_KEYLEN + AES_BLOCKLEN
AES_SECURITY_STRENGTH = 32  # bytes

# §10.2.1 max bytes per generate request = 2^19 bits / 8 = 65536.
AES_MAX_BYTES_PER_REQUEST = 1 << 16

# §10.1.2 max bytes per request: 2^19 bits = 65536 bytes.
HMAC_MAX_BYTES_PER_REQUEST = 1 << 16


class ReseedRequiredError(RuntimeError):
    """Raised when the reseed counter is exhausted and reseed has not been called."""


class DRBGStateError(RuntimeError):
    """Raised on illegal state transitions (e.g., generate before instantiate)."""


# ---------------------------------------------------------------------------
# HMAC-DRBG (SP 800-90A §10.1.2)
# ---------------------------------------------------------------------------


@dataclass
class _HMACState:
    K: bytes
    V: bytes
    reseed_counter: int


class _HMACDRBG:
    out_len = HMAC_SHA256_OUTLEN
    security_strength = HMAC_SHA256_SECURITY_STRENGTH
    digestmod = "sha256"

    def __init__(self) -> None:
        self._state: Optional[_HMACState] = None

    # Update step, §10.1.2.2.
    def _update(self, provided_data: bytes) -> None:
        K = self._state.K
        V = self._state.V
        K = hmac.new(K, V + b"\x00" + provided_data, self.digestmod).digest()
        V = hmac.new(K, V, self.digestmod).digest()
        if provided_data:
            K = hmac.new(K, V + b"\x01" + provided_data, self.digestmod).digest()
            V = hmac.new(K, V, self.digestmod).digest()
        self._state.K = K
        self._state.V = V

    # Instantiate, §10.1.2.3.
    def instantiate(self, entropy: bytes, nonce: bytes, personalization: bytes) -> None:
        if len(entropy) < self.security_strength:
            raise ValueError("entropy_input shorter than security strength")
        seed = entropy + nonce + personalization
        self._state = _HMACState(
            K=b"\x00" * self.out_len,
            V=b"\x01" * self.out_len,
            reseed_counter=1,
        )
        self._update(seed)

    # Reseed, §10.1.2.4.
    def reseed(self, entropy: bytes, additional_input: bytes) -> None:
        if self._state is None:
            raise DRBGStateError("DRBG not instantiated")
        if len(entropy) < self.security_strength:
            raise ValueError("entropy_input shorter than security strength")
        self._update(entropy + additional_input)
        self._state.reseed_counter = 1

    # Generate, §10.1.2.5.
    def generate(self, n: int, additional_input: bytes) -> bytes:
        if self._state is None:
            raise DRBGStateError("DRBG not instantiated")
        if n > HMAC_MAX_BYTES_PER_REQUEST:
            raise ValueError("request exceeds max bytes per generate")
        if self._state.reseed_counter > RESEED_INTERVAL:
            raise ReseedRequiredError("reseed required before next generate")
        if additional_input:
            self._update(additional_input)
        out = bytearray()
        while len(out) < n:
            self._state.V = hmac.new(
                self._state.K, self._state.V, self.digestmod
            ).digest()
            out.extend(self._state.V)
        self._update(additional_input)
        self._state.reseed_counter += 1
        return bytes(out[:n])

    @property
    def reseed_counter(self) -> int:
        return self._state.reseed_counter if self._state else 0

    @property
    def instantiated(self) -> bool:
        return self._state is not None


# ---------------------------------------------------------------------------
# CTR-DRBG, AES-256, no df (SP 800-90A §10.2.1.2 / §10.2.1.5.1)
# ---------------------------------------------------------------------------


@dataclass
class _CTRState:
    Key: bytes
    V: bytes
    reseed_counter: int


def _aes_ecb_encrypt(key: bytes, block: bytes) -> bytes:
    # AES-ECB-encrypt of a single 16-byte block, used as the CTR-DRBG primitive.
    enc = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    return enc.update(block) + enc.finalize()


def _inc_counter(V: bytes) -> bytes:
    n = (int.from_bytes(V, "big") + 1) & ((1 << (AES_BLOCKLEN * 8)) - 1)
    return n.to_bytes(AES_BLOCKLEN, "big")


class _CTRDRBG:
    seedlen = AES_SEEDLEN
    keylen = AES_KEYLEN
    blocklen = AES_BLOCKLEN
    security_strength = AES_SECURITY_STRENGTH

    def __init__(self) -> None:
        self._state: Optional[_CTRState] = None

    # Update, §10.2.1.2.
    def _update(self, provided_data: bytes) -> None:
        if len(provided_data) != self.seedlen:
            raise ValueError("provided_data length must equal seedlen")
        temp = bytearray()
        V = self._state.V
        Key = self._state.Key
        while len(temp) < self.seedlen:
            V = _inc_counter(V)
            temp.extend(_aes_ecb_encrypt(Key, V))
        temp = bytes(temp[: self.seedlen])
        mixed = bytes(a ^ b for a, b in zip(temp, provided_data))
        self._state.Key = mixed[: self.keylen]
        self._state.V = mixed[self.keylen :]

    # Instantiate (no df, §10.2.1.3.1).
    def instantiate(self, entropy: bytes, nonce: bytes, personalization: bytes) -> None:
        # No-df form requires entropy_input length == seedlen. Caller can pass
        # a longer buffer; we truncate after concatenation per §10.2.1.3.1.
        seed_material = entropy + nonce + personalization
        if len(seed_material) < self.seedlen:
            raise ValueError("seed material shorter than seedlen")
        seed_material = seed_material[: self.seedlen]
        self._state = _CTRState(
            Key=b"\x00" * self.keylen,
            V=b"\x00" * self.blocklen,
            reseed_counter=1,
        )
        self._update(seed_material)

    # Reseed (no df, §10.2.1.4.1).
    def reseed(self, entropy: bytes, additional_input: bytes) -> None:
        if self._state is None:
            raise DRBGStateError("DRBG not instantiated")
        seed = entropy + additional_input
        if len(seed) < self.seedlen:
            raise ValueError("seed material shorter than seedlen")
        seed = seed[: self.seedlen]
        self._update(seed)
        self._state.reseed_counter = 1

    # Generate (no df, §10.2.1.5.1).
    def generate(self, n: int, additional_input: bytes) -> bytes:
        if self._state is None:
            raise DRBGStateError("DRBG not instantiated")
        if n > AES_MAX_BYTES_PER_REQUEST:
            raise ValueError("request exceeds max bytes per generate")
        if self._state.reseed_counter > RESEED_INTERVAL:
            raise ReseedRequiredError("reseed required before next generate")
        if additional_input:
            ai = additional_input + b"\x00" * (self.seedlen - len(additional_input)) \
                if len(additional_input) < self.seedlen else additional_input[: self.seedlen]
            self._update(ai)
        else:
            ai = b"\x00" * self.seedlen
        out = bytearray()
        while len(out) < n:
            self._state.V = _inc_counter(self._state.V)
            out.extend(_aes_ecb_encrypt(self._state.Key, self._state.V))
        self._update(ai)
        self._state.reseed_counter += 1
        return bytes(out[:n])

    @property
    def reseed_counter(self) -> int:
        return self._state.reseed_counter if self._state else 0

    @property
    def instantiated(self) -> bool:
        return self._state is not None


# ---------------------------------------------------------------------------
# Public DRBG facade
# ---------------------------------------------------------------------------


class DRBG:
    """SP 800-90A facade over HMAC-DRBG (default) and CTR-DRBG-AES-256."""

    def __init__(self, algorithm: str = HMAC_SHA256) -> None:
        if algorithm == HMAC_SHA256:
            self._impl = _HMACDRBG()
            self.security_strength = HMAC_SHA256_SECURITY_STRENGTH
        elif algorithm == AES_CTR_256:
            self._impl = _CTRDRBG()
            self.security_strength = AES_SECURITY_STRENGTH
        else:
            raise ValueError(f"unknown algorithm: {algorithm}")
        self.algorithm = algorithm
        self._state_str = "uninstantiated"

    def instantiate(
        self,
        entropy_input: bytes,
        nonce: bytes,
        personalization: bytes = b"",
    ) -> None:
        if self._state_str == "instantiated":
            raise DRBGStateError("already instantiated")
        try:
            self._impl.instantiate(entropy_input, nonce, personalization)
        except Exception:
            self._state_str = "failed"
            raise
        self._state_str = "instantiated"

    def reseed(self, entropy_input: bytes, additional_input: bytes = b"") -> None:
        if self._state_str != "instantiated":
            raise DRBGStateError("DRBG not instantiated")
        self._impl.reseed(entropy_input, additional_input)

    def generate(self, n_bytes: int, additional_input: bytes = b"") -> bytes:
        if self._state_str != "instantiated":
            raise DRBGStateError("DRBG not instantiated")
        return self._impl.generate(n_bytes, additional_input)

    @property
    def needs_reseed(self) -> bool:
        return self._impl.reseed_counter > RESEED_INTERVAL

    @property
    def state(self) -> str:
        return self._state_str

    @property
    def reseed_counter(self) -> int:
        return self._impl.reseed_counter

    @classmethod
    def seeded_from_os(cls, algorithm: str = HMAC_SHA256) -> "DRBG":
        """Convenience: instantiate from os.urandom for tests and demos.

        Production callers should drive instantiation from QRNGSource so that
        provenance and health tests are accounted for explicitly.
        """
        d = cls(algorithm)
        if algorithm == HMAC_SHA256:
            d.instantiate(os.urandom(32), os.urandom(16), b"hybrid-kem-default")
        else:
            d.instantiate(os.urandom(48), b"", b"")
        return d
