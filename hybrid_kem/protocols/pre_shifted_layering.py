"""Pre-shifted layering state machine (PRE_SHIFTED_LAYERING_SPEC §4).

Implements §9 item 3 of ``PRE_SHIFTED_LAYERING_SPEC.md``: the
``LayeredProtocolState`` dataclass and the ``advance_edge`` /
``advance_face`` / ``derive_key_material`` / ``initialize_session``
functions described in §4.

NOT a secure protocol. This is a design-sketch implementation of the
state machine. The grade-gap argument is T3 per §6 of the spec.
Production key material must come from ML-KEM (FIPS 203). See §10 of
the spec for the explicit non-goals.

The state advances deterministically given the same sequence of
``event_entropy`` inputs, so two parties observing the same protocol
events compute byte-identical states without coordination messages
(spec §5).

Algebraic constants (all T1, verified externally per spec §9 items 1-2
and re-verified locally in :func:`_verify_period_constants`):

- ``INNER_PERIOD = 6``   — A₄ acting on 4 points, lcm{1,2,3}
- ``OUTER_PERIOD = 84``  — PSL(2,7) acting on P¹(F₇), lcm{1,2,3,4,7}
- ``PRE_SHIFT_N  = 91``  — Fano-aligned offset (= 7 · 13)

Identities (verified in tests):

- ``gcd(PRE_SHIFT_N, INNER_PERIOD) == 1``
- ``gcd(PRE_SHIFT_N, OUTER_PERIOD) == 7``  (shared Fano factor)
- ``lcm(INNER_PERIOD, OUTER_PERIOD, PRE_SHIFT_N) == 1092``

The minimal valid N is 85; we use 91 for the structural Fano
alignment documented in spec §3.3.
"""

from __future__ import annotations

import hashlib
import hmac
import math
from dataclasses import dataclass, replace


# ---------------------------------------------------------------------------
# Constants (T1)
# ---------------------------------------------------------------------------

INNER_PERIOD = 6
OUTER_PERIOD = 84
PRE_SHIFT_N = 91
LAYER_REALIGN_LCM = 1092  # lcm(INNER_PERIOD, OUTER_PERIOD, PRE_SHIFT_N)

# Group sizes used by the two layers. PSL(2,7) has order 168 — the
# edge-element index ranges over the full group, even though the
# point-set action cycles with period 84.
PSL_2_7_ORDER = 168
CL8_BIVECTOR_COUNT = 14

# Pre-shift initialization seed domain separator (spec §4.4).
_INIT_FACE_INFO = b"hybrid_kem/pre_shifted_layering|init-face|v1"
_KEY_INFO_TAG = b"hybrid_kem/pre_shifted_layering|face-layer-key-v1"


# ---------------------------------------------------------------------------
# Internal period self-check
# ---------------------------------------------------------------------------


def _lcm(values):
    out = 1
    for v in values:
        out = out * v // math.gcd(out, v)
    return out


def _verify_period_constants() -> None:
    """Recompute period values locally (no SymPy dependency).

    Period = lcm of element orders restricted to the point-set action.
    A₄ on 4 points: element orders {1,2,3} → lcm = 6.
    PSL(2,7) on P¹(F₇): element orders {1,2,3,4,7} → lcm = 84.
    """
    inner = _lcm((1, 2, 3))
    outer = _lcm((1, 2, 3, 4, 7))
    assert inner == INNER_PERIOD, (inner, INNER_PERIOD)
    assert outer == OUTER_PERIOD, (outer, OUTER_PERIOD)
    assert math.gcd(PRE_SHIFT_N, INNER_PERIOD) == 1
    assert math.gcd(PRE_SHIFT_N, OUTER_PERIOD) == 7
    assert _lcm((INNER_PERIOD, OUTER_PERIOD, PRE_SHIFT_N)) == LAYER_REALIGN_LCM


_verify_period_constants()


# ---------------------------------------------------------------------------
# HKDF (RFC 5869) — local minimal implementation, no extra dependency
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
# State
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LayeredProtocolState:
    """Immutable layered state. Spec §4.1.

    The frozen dataclass mirrors the spec's "Returns new state. Does
    not mutate." contract on every transition.
    """

    edge_element: int  # 0..PSL_2_7_ORDER-1
    edge_step: int
    face_element: int  # 0..CL8_BIVECTOR_COUNT-1
    face_step: int
    session_id: bytes  # 16 bytes; agreed via outer KEM
    epoch: int

    def check_invariant(self) -> None:
        """Spec §4.1: ``face_step == edge_step + PRE_SHIFT_N``."""
        if self.face_step != self.edge_step + PRE_SHIFT_N:
            raise ValueError(
                f"layering invariant violated: "
                f"face_step={self.face_step}, "
                f"edge_step={self.edge_step}, "
                f"expected face_step={self.edge_step + PRE_SHIFT_N}"
            )
        if not 0 <= self.edge_element < PSL_2_7_ORDER:
            raise ValueError(f"edge_element out of range: {self.edge_element}")
        if not 0 <= self.face_element < CL8_BIVECTOR_COUNT:
            raise ValueError(f"face_element out of range: {self.face_element}")
        if len(self.session_id) != 16:
            raise ValueError(f"session_id must be 16 bytes; got {len(self.session_id)}")


# ---------------------------------------------------------------------------
# Element derivation (spec §4.2)
# ---------------------------------------------------------------------------


def _derive_element(
    current: int, entropy: bytes, step: int, group_order: int
) -> int:
    """HKDF-keyed map (current, entropy, step) → next-element index.

    Salt = step counter, IKM = entropy, info = current-element bytes.
    The step counter prevents the same (current, entropy) pair from
    producing the same element at different protocol positions.
    """
    if step < 0:
        raise ValueError("step must be non-negative")
    if group_order <= 0:
        raise ValueError("group_order must be positive")
    prk = _hkdf_extract(salt=step.to_bytes(8, "big"), ikm=entropy)
    okm = _hkdf_expand(prk, info=current.to_bytes(4, "big"), length=4)
    return int.from_bytes(okm, "big") % group_order


# ---------------------------------------------------------------------------
# Public transitions (spec §4.2)
# ---------------------------------------------------------------------------


def advance_edge(
    state: LayeredProtocolState, event_entropy: bytes
) -> LayeredProtocolState:
    """Advance the edge layer by one step.

    ``event_entropy`` MUST be fresh per call. The group-element
    sequence alone never determines key material; structure
    determines WHEN to step, entropy determines WHAT the new state is
    (spec §4.2).

    Returns a new state. Does not mutate.
    """
    if not event_entropy:
        raise ValueError("event_entropy required")

    next_edge = _derive_element(
        current=state.edge_element,
        entropy=event_entropy,
        step=state.edge_step + 1,
        group_order=PSL_2_7_ORDER,
    )
    new_edge_step = state.edge_step + 1
    new_epoch = state.epoch + 1 if new_edge_step % OUTER_PERIOD == 0 else state.epoch
    return replace(
        state,
        edge_element=next_edge,
        edge_step=new_edge_step,
        epoch=new_epoch,
    )


def advance_face(
    state: LayeredProtocolState, event_entropy: bytes
) -> LayeredProtocolState:
    """Advance the face layer by one step (spec §4.2)."""
    if not event_entropy:
        raise ValueError("event_entropy required")
    next_face = _derive_element(
        current=state.face_element,
        entropy=event_entropy,
        step=state.face_step + 1,
        group_order=CL8_BIVECTOR_COUNT,
    )
    return replace(
        state,
        face_element=next_face,
        face_step=state.face_step + 1,
    )


# ---------------------------------------------------------------------------
# Initialization (spec §4.4)
# ---------------------------------------------------------------------------


def initialize_session(session_id: bytes) -> LayeredProtocolState:
    """Build the post-handshake state. Both parties run this on the
    agreed ``session_id`` (16 bytes); they obtain byte-identical
    states without coordination messages.

    Steps (spec §4.4):

    1. ``edge_step = face_step = 0``
    2. Advance face by ``PRE_SHIFT_N`` steps using a deterministic
       seed = ``HKDF(session_id, b'init-face')``.
    3. Resulting state has ``face_step = PRE_SHIFT_N``, ``edge_step = 0``,
       invariant established.

    The deterministic seed makes the initial face state computable
    from ``session_id`` alone (it is not secret). Security comes from
    the face layer running ahead of what an attacker can currently
    solve, not from the initial face state being unknown (spec §4.4).
    """
    if len(session_id) != 16:
        raise ValueError(f"session_id must be 16 bytes; got {len(session_id)}")

    seed_prk = _hkdf_extract(salt=session_id, ikm=_INIT_FACE_INFO)
    # Expand a per-step entropy stream so each advance_face call gets
    # a distinct deterministic event_entropy. 32 bytes per step ×
    # PRE_SHIFT_N steps fits in a single HKDF-Expand invocation.
    step_entropy = _hkdf_expand(
        seed_prk, info=b"init-face-step-stream", length=PRE_SHIFT_N * 32
    )

    # Pre-shift starts from canonical "zero" elements on both layers.
    # face_step is temporarily PRE_SHIFT_N - PRE_SHIFT_N = 0 here;
    # we bypass the invariant check until the pre-shift completes.
    state = LayeredProtocolState(
        edge_element=0,
        edge_step=0,
        face_element=0,
        face_step=0,
        session_id=session_id,
        epoch=0,
    )
    for i in range(PRE_SHIFT_N):
        chunk = step_entropy[i * 32:(i + 1) * 32]
        state = advance_face(state, chunk)
    state.check_invariant()
    return state


# ---------------------------------------------------------------------------
# Key derivation (spec §4.3)
# ---------------------------------------------------------------------------


def derive_key_material(
    state: LayeredProtocolState, purpose: bytes, length: int
) -> bytes:
    """Derive key material from the face layer only (spec §4.3).

    The edge element is intentionally absent from the IKM, so an
    adversary who recovers ``edge_element`` learns nothing about the
    key directly; they would still need to climb the grade gap to
    reach the face layer.

    ``purpose`` enforces domain separation between key types
    (encryption key, MAC key, ratchet seed, ...).
    """
    if length <= 0:
        raise ValueError("length must be positive")
    ikm = state.face_element.to_bytes(4, "big") + state.session_id
    salt = state.epoch.to_bytes(8, "big")
    info = purpose + b"|" + _KEY_INFO_TAG
    prk = _hkdf_extract(salt=salt, ikm=ikm)
    return _hkdf_expand(prk, info=info, length=length)
