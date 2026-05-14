"""Brief 03 — IrrationalConditioner (EXPERIMENTAL).

A conditioning layer that mixes a caller-supplied entropy buffer with
digit expansions of three irrational constants (φ, π, e) and live
timing jitter gathered during the computation. Sits between SP 800-90B
health tests and SP 800-90A DRBG instantiation.

NOT a primary entropy source. The digit expansions of φ, π, e are
deterministic and publicly known. Security of this conditioner rests on
two things:

  1. The caller-supplied ``entropy_bytes`` already contains
     uncertainty (it is the output of a healthy physical source that
     has passed RCT/APT). The conditioner only re-mixes it; it does
     not manufacture entropy from the constants.
  2. The *offset* into each digit table is selected from the supplied
     entropy, and the byte stream of selected digits is XOR-mixed
     with timing jitter that an offline attacker cannot observe.

Channel role: this is a whitening / non-linear-mixing transform whose
output has the same length as its input and is intended as
``entropy_input`` to ``DRBG.instantiate``.

CORRECT usage::

    src = QuartzEntropySource(...)
    raw = src.get_bytes(48)
    result = run_health_tests(raw, h_min=7.5)
    assert result.passed
    mixed = IrrationalConditioner().condition(raw)
    drbg.instantiate(entropy_input=mixed[:32], nonce=mixed[32:48])

WRONG usage (the conditioner is not a substitute for entropy)::

    # Do NOT do this — there is no physical-entropy input.
    seed = IrrationalConditioner().condition(b"\\x00" * 32)
    drbg.instantiate(entropy_input=seed, ...)

Because the constants and the offset-derivation function are public,
calling ``condition`` on a constant or low-entropy input gives a
deterministic-looking output that an attacker can predict modulo the
jitter component. That is *not* sufficient for cryptographic use.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Optional

import mpmath


class OffsetExhaustedError(RuntimeError):
    """Raised when the digit-offset namespace is exhausted within a session.

    The conditioner refuses to reuse an offset within its lifetime; once
    every valid offset has been consumed, callers must instantiate a
    fresh ``IrrationalConditioner`` (which is the signal to operators
    that ``precision_digits`` was set too low for the workload).
    """


class InsufficientEntropyError(ValueError):
    """Raised when ``entropy_bytes`` is too short to derive an offset.

    The offset-derivation function reads 11 bytes from the supplied
    entropy; shorter buffers are rejected.
    """


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_MIN_ENTROPY_BYTES = 11  # 8 bytes offset + 2 bytes length + 1 byte constant
_LENGTH_MIN = 16
_LENGTH_MAX = 128
_LENGTH_RANGE = _LENGTH_MAX - _LENGTH_MIN + 1  # 113
_VARIANT_STRIDE = 257  # coprime to typical max_offset; spreads variants
_DIGIT_GROUP_SIZE = 8  # ASCII digits per SHA-256 absorption
_DIGIT_GROUP_DIGEST_BYTES = 4  # first 4 bytes of each SHA-256 result


# ---------------------------------------------------------------------------
# Digit-table generation
# ---------------------------------------------------------------------------


def _fractional_digits(value: mpmath.mpf, precision: int) -> bytes:
    """Return ASCII bytes of the first ``precision`` digits after the point.

    ``value`` must have absolute value below 10 so the result has at most
    one integer digit (φ, π, e all satisfy this). We work entirely on the
    fractional part to keep digit indexing aligned across constants.

    Uses ``mpmath.nstr`` for the decimal expansion. Bypassing it via
    ``str(int(...))`` hits CPython 3.11's 4300-digit int-to-str cap.
    """
    # nstr returns a decimal string at the requested significant figures.
    # Request precision+5 sig figs so the integer digit (≤ 1 for φ, π, e)
    # is comfortably absorbed before the requested fractional digits.
    s = mpmath.nstr(value, precision + 5, strip_zeros=False)
    if "." not in s:
        s += "."
    integer_part, frac_part = s.split(".", 1)
    # Strip exponent notation if mpmath chose to emit one.
    if "e" in frac_part:
        frac_part = frac_part.split("e", 1)[0]
    if len(frac_part) < precision:
        frac_part = frac_part + "0" * (precision - len(frac_part))
    return frac_part[:precision].encode("ascii")


def _compute_digit_tables(precision_digits: int) -> dict[str, bytes]:
    """Compute φ, π, e digit tables at the requested precision.

    Uses a working precision of ``precision_digits + 50`` to absorb
    rounding error at the tail of the requested range, then truncates.
    """
    if precision_digits < 1000:
        raise ValueError("precision_digits must be >= 1000")
    saved_dps = mpmath.mp.dps
    try:
        mpmath.mp.dps = precision_digits + 50
        phi = (mpmath.mpf(1) + mpmath.sqrt(5)) / 2
        return {
            "phi": _fractional_digits(phi, precision_digits),
            "pi": _fractional_digits(mpmath.pi, precision_digits),
            "e": _fractional_digits(mpmath.e, precision_digits),
        }
    finally:
        mpmath.mp.dps = saved_dps


# ---------------------------------------------------------------------------
# HKDF (RFC 5869) -- minimal local implementation, no extra dependency
# ---------------------------------------------------------------------------


def _hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    if not salt:
        salt = b"\x00" * hashlib.sha256().digest_size
    return hmac.new(salt, ikm, hashlib.sha256).digest()


def _hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    hash_len = hashlib.sha256().digest_size
    n = (length + hash_len - 1) // hash_len
    if n > 255:
        raise ValueError("requested HKDF output too long")
    okm = b""
    previous = b""
    for i in range(1, n + 1):
        previous = hmac.new(
            prk, previous + info + bytes([i]), hashlib.sha256
        ).digest()
        okm += previous
    return okm[:length]


# ---------------------------------------------------------------------------
# IrrationalConditioner
# ---------------------------------------------------------------------------


_CONSTANT_NAMES = ("phi", "pi", "e")


class IrrationalConditioner:
    """Mix supplied entropy with irrational-constant digits and live jitter.

    Parameters
    ----------
    precision_digits:
        Number of decimal digits to retain for each of φ, π, e. Must be
        at least 1000. Larger values widen the offset namespace at the
        cost of one-time construction time.
    _fake_jitter:
        Test-only hook. If not ``None``, every call to ``condition`` uses
        this fixed 3-byte value in place of measured timing jitter. This
        makes outputs reproducible in unit tests; never set in
        production callers.
    """

    def __init__(
        self,
        precision_digits: int = 10_000,
        *,
        _fake_jitter: Optional[bytes] = None,
    ) -> None:
        self.precision_digits = precision_digits
        self._tables = _compute_digit_tables(precision_digits)
        # Maximum valid base offset such that any variant length fits.
        self._max_offset = precision_digits - _LENGTH_MAX
        if self._max_offset <= 0:
            raise ValueError(
                "precision_digits must exceed maximum extraction length"
            )
        self._used_offsets: set[int] = set()
        if _fake_jitter is not None and len(_fake_jitter) != 3:
            raise ValueError("_fake_jitter must be exactly 3 bytes")
        self._fake_jitter = _fake_jitter

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def condition(self, entropy_bytes: bytes) -> bytes:
        """Return ``len(entropy_bytes)`` bytes of conditioned output.

        Raises
        ------
        InsufficientEntropyError
            If ``entropy_bytes`` is shorter than 11 bytes.
        OffsetExhaustedError
            If every offset in the precision-bounded namespace has
            already been used in this session.
        """
        if len(entropy_bytes) < _MIN_ENTROPY_BYTES:
            raise InsufficientEntropyError(
                f"entropy_bytes must be at least {_MIN_ENTROPY_BYTES} bytes; "
                f"got {len(entropy_bytes)}"
            )

        base_offset, length, primary_name = self._derive_params(entropy_bytes)
        offset = self._claim_offset(base_offset, length)

        # Step 2: digitise extracted ASCII digits from primary constant.
        primary_bytes = self._extract(primary_name, offset, length)
        primary_digest = _digitise(primary_bytes)

        # Step 3: timing jitter sampled across digitisation of the
        # primary constant.
        if self._fake_jitter is not None:
            jitter = self._fake_jitter
        else:
            t0 = time.perf_counter_ns()
            # Touch the primary digest to keep the jitter window non-trivial
            # on systems where the digitise call is already cached.
            _ = hashlib.sha256(primary_digest).digest()
            t1 = time.perf_counter_ns()
            delta = (t1 - t0) & 0xFFFFFFFFFFFFFFFF
            jitter = delta.to_bytes(8, "big")[5:]  # low 3 bytes

        # Step 4: extract variant slices from all three constants at
        # offsets derived from the base offset.
        variant_digests = []
        for i, name in enumerate(_CONSTANT_NAMES):
            voffset = (offset + i * _VARIANT_STRIDE) % self._max_offset
            variant_bytes = self._extract(name, voffset, length)
            variant_digests.append(_digitise(variant_bytes))

        # Step 5: XOR-combine variant digests, expanded to the entropy
        # length via HKDF, with entropy and jitter as keying material.
        combined = bytes(a ^ b ^ c for a, b, c in zip(*variant_digests))
        prk = _hkdf_extract(salt=jitter, ikm=entropy_bytes + combined)
        info = (
            b"hybrid_kem/irrational_conditioner|v1|"
            + primary_name.encode("ascii")
            + b"|"
            + offset.to_bytes(8, "big")
            + b"|"
            + length.to_bytes(2, "big")
        )
        return _hkdf_expand(prk, info, len(entropy_bytes))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _derive_params(self, entropy_bytes: bytes) -> tuple[int, int, str]:
        base_offset = (
            int.from_bytes(entropy_bytes[:8], "big") % self._max_offset
        )
        length = _LENGTH_MIN + (
            int.from_bytes(entropy_bytes[8:10], "big") % _LENGTH_RANGE
        )
        primary_name = _CONSTANT_NAMES[entropy_bytes[10] % 3]
        return base_offset, length, primary_name

    def _claim_offset(self, base_offset: int, length: int) -> int:
        """Find an unused offset by linear probe from ``base_offset``."""
        offset = base_offset
        probes = 0
        # Probing budget is the entire namespace; we raise if exhausted.
        while offset in self._used_offsets:
            offset = (offset + 1) % self._max_offset
            probes += 1
            if probes >= self._max_offset:
                raise OffsetExhaustedError(
                    "all digit offsets used; instantiate a new "
                    "IrrationalConditioner with larger precision_digits"
                )
        self._used_offsets.add(offset)
        return offset

    def _extract(self, name: str, offset: int, length: int) -> bytes:
        table = self._tables[name]
        end = offset + length
        if end <= len(table):
            return bytes(table[offset:end])
        # Wrap once. The base-offset bound guarantees this only fires when
        # variant offsets near the end of the table need to wrap.
        wrap = end - len(table)
        return bytes(table[offset:]) + bytes(table[:wrap])

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    @property
    def offsets_used(self) -> int:
        return len(self._used_offsets)

    @property
    def offsets_remaining(self) -> int:
        return self._max_offset - len(self._used_offsets)


def _digitise(ascii_digits: bytes) -> bytes:
    """Hash groups of 8 ASCII digits with SHA-256, keep 4 bytes per group.

    The result has length ``ceil(len(ascii_digits) / 8) * 4``. With the
    16..128-digit length range, that is 8..64 bytes — enough headroom for
    the XOR-mix step regardless of caller entropy size.
    """
    out = bytearray()
    for i in range(0, len(ascii_digits), _DIGIT_GROUP_SIZE):
        group = ascii_digits[i:i + _DIGIT_GROUP_SIZE]
        digest = hashlib.sha256(group).digest()
        out.extend(digest[:_DIGIT_GROUP_DIGEST_BYTES])
    return bytes(out)


__all__ = [
    "IrrationalConditioner",
    "InsufficientEntropyError",
    "OffsetExhaustedError",
]
