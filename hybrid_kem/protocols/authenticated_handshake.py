"""Authenticated key exchange over the hybrid KEM and composite signatures.

A two- or three-message handshake that gives two parties a shared 32-byte
session key, authenticated with the composite ML-DSA + EdDSA signature. The
design follows the well-understood TLS 1.3 / SIGMA pattern: an *ephemeral*
hybrid-KEM key agreement for secrecy, and a signature over the full transcript
for authentication and identity binding. It is assembled entirely from the
standardised primitives in this package.

    Initiator (I)                               Responder (R)
    ------------                                -------------
    ephemeral (pk_e, sk_e) = HybridKEM.keygen()
    --- msg1: suite, id_I, [vk_I], pk_e ----->
                                                (ct, ss) = Encaps(pk_e)
                                                TH = H(transcript)
                                                sig_R = Sign_R(TH)
    <-- msg2: id_R, vk_R, ct, sig_R -----------
    ss = Decaps(sk_e, ct)
    TH = H(transcript); verify sig_R under vk_R
    key = HKDF(ss; salt=TH)
    --- msg3: sig_I  (mutual auth only) ------>
                                                verify sig_I; key = HKDF(ss; salt=TH)

Transcript hash (length-prefixed fields, so no concatenation ambiguity):

    TH = SHA3-256( SUITE_ID | id_I | vk_I | id_R | vk_R | pk_e | ct )

SUITE_ID names both the KEM profile and the signature profile, so a party that
signs it cannot be steered onto a different suite (downgrade binding across the
single offered suite). vk_R is inside TH, so the signature authenticates the
exact key the initiator is checking against (guards against unknown-key-share).
The session key is salted by TH, so it agrees only if both sides saw the same
transcript, and it depends on the KEM secret for confidentiality.

What this provides: responder authentication (and initiator authentication in
mutual mode), session-key secrecy as long as either KEM leg holds, transcript
integrity, identity binding, and per-handshake forward secrecy (the KEM key is
ephemeral -- discard sk_e after the handshake). The initiator MUST reject the
handshake if sig_R does not verify (``finish`` raises ``AuthenticationError``),
so a key is never derived from an unauthenticated transcript.

What this is NOT: a standardised or formally analysed protocol. It is an
engineering construction that reuses the TLS 1.3 / SIGMA design with
post-quantum primitives. For production, use TLS 1.3 (hybrid groups) or another
reviewed protocol from a maintained library. There is no negotiation (one fixed
suite per handshake), no 0-RTT, and no cross-session replay protection beyond
the freshness of the ephemeral KEM key.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from typing import Optional, Tuple

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from ..hybrid_kem import HybridKEM, default_drbg
from ..sig_composite.composite_mldsa import PROFILES as SIG_PROFILES
from ..sig_composite.composite_mldsa import CompositeMLDSA

PROTO = b"hybrid-ake/v1"
CTX_SERVER = b"hybrid-ake/responder-auth/v1"
CTX_CLIENT = b"hybrid-ake/initiator-auth/v1"
INFO_KEY = b"hybrid-ake/session-key/v1"
SESSION_KEY_LEN = 32


class HandshakeError(Exception):
    """Base class for handshake failures."""


class AuthenticationError(HandshakeError):
    """A transcript signature did not verify, or the peer was not the expected one."""


class ProtocolError(HandshakeError):
    """A message was malformed or the suites did not match."""


def _lp(*chunks: bytes) -> bytes:
    """Length-prefixed concatenation (4-byte big-endian lengths)."""
    return b"".join(len(c).to_bytes(4, "big") + c for c in chunks)


def _unlp(buf: bytes, n: int) -> list[bytes]:
    out, off = [], 0
    for _ in range(n):
        if off + 4 > len(buf):
            raise ProtocolError("truncated message")
        length = int.from_bytes(buf[off:off + 4], "big")
        off += 4
        if off + length > len(buf):
            raise ProtocolError("truncated message")
        out.append(buf[off:off + length])
        off += length
    if off != len(buf):
        raise ProtocolError("trailing bytes in message")
    return out


def _suite_id(kem_profile: str, sig_profile: str) -> bytes:
    return b" ".join((PROTO, kem_profile.encode(), sig_profile.encode()))


# ---------------------------------------------------------------------------
# Identities
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PeerIdentity:
    """A peer's public identity: a name and a composite verification key."""

    name: bytes
    verification_key: bytes
    sig_profile: str

    def verify(self, signature: bytes, message: bytes, context: bytes) -> bool:
        return CompositeMLDSA(self.sig_profile).verify(
            self.verification_key, signature, message, context
        )


@dataclass
class Identity:
    """A long-term signing identity (composite ML-DSA + EdDSA)."""

    name: bytes
    sig_profile: str
    _sk: bytes
    _pk: bytes

    @classmethod
    def generate(cls, name: str | bytes, sig_profile: str = "id-MLDSA65-Ed25519-SHA512",
                 drbg=None) -> "Identity":
        if sig_profile not in SIG_PROFILES:
            raise ValueError(f"unknown signature profile {sig_profile!r}")
        pk, sk = CompositeMLDSA(sig_profile).keygen(drbg or default_drbg(b"ake-identity"))
        nm = name.encode() if isinstance(name, str) else name
        return cls(name=nm, sig_profile=sig_profile, _sk=sk, _pk=pk)

    @property
    def public(self) -> PeerIdentity:
        return PeerIdentity(self.name, self._pk, self.sig_profile)

    def sign(self, message: bytes, context: bytes) -> bytes:
        return CompositeMLDSA(self.sig_profile).sign(self._sk, message, context)


# ---------------------------------------------------------------------------
# Handshake state and transcript
# ---------------------------------------------------------------------------


@dataclass
class _State:
    role: str
    suite_id: bytes
    transcript_hash: bytes
    session_key: bytes
    # initiator keeps these to build msg3 in mutual mode:
    sig_r: Optional[bytes] = None


def _transcript_hash(suite_id, id_i, vk_i, id_r, vk_r, pk_e, ct) -> bytes:
    return hashlib.sha3_256(
        _lp(suite_id, id_i, vk_i, id_r, vk_r, pk_e, ct)
    ).digest()


def _derive_key(ss: bytes, th: bytes, suite_id: bytes) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=SESSION_KEY_LEN,
        salt=th,
        info=INFO_KEY + b" " + suite_id,
    )
    return hkdf.derive(ss)


# ---------------------------------------------------------------------------
# Initiator
# ---------------------------------------------------------------------------


class Initiator:
    """The handshake initiator (client).

    Authenticates the responder against ``peer``. If ``identity`` is given, the
    initiator also authenticates itself (mutual auth) and ``finish`` returns a
    third message to send.
    """

    def __init__(self, kem_profile: str, peer: PeerIdentity,
                 identity: Optional[Identity] = None) -> None:
        self._kem = HybridKEM(profile=kem_profile)
        self._kem_profile = kem_profile
        self._peer = peer
        self._identity = identity
        self._suite_id = _suite_id(kem_profile, peer.sig_profile)

    def start(self, drbg=None) -> Tuple[dict, bytes]:
        drbg = drbg or default_drbg(b"ake-initiator")
        pk_e, sk_e = self._kem.keygen(drbg)
        id_i = self._identity.name if self._identity else b""
        vk_i = self._identity.public.verification_key if self._identity else b""
        msg1 = _lp(self._suite_id, id_i, vk_i, pk_e)
        ctx = {"sk_e": sk_e, "pk_e": pk_e, "id_i": id_i, "vk_i": vk_i}
        return ctx, msg1

    def finish(self, ctx: dict, msg2: bytes,
               drbg=None) -> Tuple[bytes, Optional[bytes]]:
        id_r, vk_r, ct, sig_r = _unlp(msg2, 4)
        if vk_r != self._peer.verification_key or id_r != self._peer.name:
            raise AuthenticationError("responder identity does not match the expected peer")
        ss = self._kem.decaps(ctx["sk_e"], ct)
        th = _transcript_hash(self._suite_id, ctx["id_i"], ctx["vk_i"],
                              id_r, vk_r, ctx["pk_e"], ct)
        if not self._peer.verify(sig_r, th, CTX_SERVER):
            raise AuthenticationError("responder signature did not verify")
        key = _derive_key(ss, th, self._suite_id)
        msg3 = None
        if self._identity is not None:
            # bind the initiator's signature to the responder's, so it cannot be
            # replayed into a different handshake.
            th2 = hashlib.sha3_256(_lp(th, sig_r)).digest()
            msg3 = _lp(self._identity.sign(th2, CTX_CLIENT))
        return key, msg3


# ---------------------------------------------------------------------------
# Responder
# ---------------------------------------------------------------------------


class Responder:
    """The handshake responder (server).

    Authenticates itself with ``identity``. If ``require_peer`` is given, the
    handshake is mutual: ``respond`` returns state that ``confirm`` finalises
    once the initiator's msg3 arrives. If ``require_peer`` is None, the
    responder accepts an anonymous initiator (responder-only auth) and the
    session key is available straight after ``respond``.
    """

    def __init__(self, kem_profile: str, identity: Identity,
                 require_peer: Optional[PeerIdentity] = None) -> None:
        self._kem = HybridKEM(profile=kem_profile)
        self._kem_profile = kem_profile
        self._identity = identity
        self._require_peer = require_peer
        self._suite_id = _suite_id(kem_profile, identity.sig_profile)

    def respond(self, msg1: bytes, drbg=None) -> Tuple[dict, bytes]:
        suite_id, id_i, vk_i, pk_e = _unlp(msg1, 4)
        if suite_id != self._suite_id:
            raise ProtocolError("suite mismatch")
        if self._require_peer is not None:
            if vk_i != self._require_peer.verification_key or id_i != self._require_peer.name:
                raise AuthenticationError("initiator is not the required peer")
        drbg = drbg or default_drbg(b"ake-responder")
        ct, ss = self._kem.encaps(pk_e, drbg)
        id_r = self._identity.name
        vk_r = self._identity.public.verification_key
        th = _transcript_hash(suite_id, id_i, vk_i, id_r, vk_r, pk_e, ct)
        sig_r = self._identity.sign(th, CTX_SERVER)
        key = _derive_key(ss, th, suite_id)
        msg2 = _lp(id_r, vk_r, ct, sig_r)
        ctx = {"th": th, "sig_r": sig_r, "key": key, "id_i": id_i, "vk_i": vk_i}
        return ctx, msg2

    def session_key(self, ctx: dict) -> bytes:
        """The session key, for responder-only auth (no initiator to verify)."""
        if self._require_peer is not None:
            raise ProtocolError("mutual handshake: call confirm() with msg3 first")
        return ctx["key"]

    def confirm(self, ctx: dict, msg3: bytes) -> bytes:
        """Finalise a mutual handshake: verify the initiator's signature."""
        if self._require_peer is None:
            raise ProtocolError("responder-only handshake has no msg3")
        (sig_i,) = _unlp(msg3, 1)
        th2 = hashlib.sha3_256(_lp(ctx["th"], ctx["sig_r"])).digest()
        if not self._require_peer.verify(sig_i, th2, CTX_CLIENT):
            raise AuthenticationError("initiator signature did not verify")
        return ctx["key"]
