"""Tests for the pre-shifted layering state machine (spec §4)."""

from __future__ import annotations

import math
import os

import pytest

from hybrid_kem.protocols.pre_shifted_layering import (
    CL8_BIVECTOR_COUNT,
    INNER_PERIOD,
    LAYER_REALIGN_LCM,
    LayeredProtocolState,
    OUTER_PERIOD,
    PRE_SHIFT_N,
    PSL_2_7_ORDER,
    _derive_element,
    advance_edge,
    advance_face,
    derive_key_material,
    initialize_session,
)


# ---------------------------------------------------------------------------
# Algebraic constants (spec §2, §3)
# ---------------------------------------------------------------------------


def test_period_constants_match_spec():
    assert INNER_PERIOD == 6
    assert OUTER_PERIOD == 84
    assert PRE_SHIFT_N == 91


def test_period_derivation_lcm_of_element_orders():
    """A₄ on 4 points → orders {1,2,3} → lcm = 6.
    PSL(2,7) on P¹(F₇) → orders {1,2,3,4,7} → lcm = 84.
    """
    def _lcm(xs):
        out = 1
        for x in xs:
            out = out * x // math.gcd(out, x)
        return out

    assert _lcm([1, 2, 3]) == INNER_PERIOD
    assert _lcm([1, 2, 3, 4, 7]) == OUTER_PERIOD


def test_pre_shift_n_coprimality():
    """Spec §3.3: gcd(91,6)=1, gcd(91,84)=7."""
    assert math.gcd(PRE_SHIFT_N, INNER_PERIOD) == 1
    assert math.gcd(PRE_SHIFT_N, OUTER_PERIOD) == 7


def test_layer_realign_lcm():
    """Spec §3.3: lcm(6, 84, 91) = 1092."""
    def _lcm(*xs):
        out = 1
        for x in xs:
            out = out * x // math.gcd(out, x)
        return out

    assert _lcm(INNER_PERIOD, OUTER_PERIOD, PRE_SHIFT_N) == LAYER_REALIGN_LCM
    assert LAYER_REALIGN_LCM == 1092


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------


def test_initialize_session_establishes_invariant():
    state = initialize_session(os.urandom(16))
    state.check_invariant()
    assert state.edge_step == 0
    assert state.face_step == PRE_SHIFT_N
    assert state.edge_element == 0
    assert 0 <= state.face_element < CL8_BIVECTOR_COUNT
    assert state.epoch == 0


def test_initialize_session_deterministic_in_session_id():
    """Same session_id ⇒ byte-identical post-init state. This is what
    makes coordination-message-free sync possible (spec §5.2)."""
    sid = os.urandom(16)
    a = initialize_session(sid)
    b = initialize_session(sid)
    assert a == b


def test_initialize_session_distinct_session_ids_differ():
    a = initialize_session(b"A" * 16)
    b = initialize_session(b"B" * 16)
    assert a.face_element != b.face_element or a != b


def test_initialize_session_rejects_bad_session_id_length():
    with pytest.raises(ValueError):
        initialize_session(b"too-short")


# ---------------------------------------------------------------------------
# advance_edge / advance_face
# ---------------------------------------------------------------------------


def test_advance_edge_increments_step_and_maintains_invariant_after_face_catchup():
    state = initialize_session(b"S" * 16)
    e = advance_edge(state, b"entropy-1")
    # After only the edge step the invariant is intentionally broken
    # (face_step - edge_step == PRE_SHIFT_N - 1). One face step
    # restores it. This matches the spec's "face follows" arrow in
    # §4.4.
    with pytest.raises(ValueError):
        e.check_invariant()
    f = advance_face(e, b"entropy-1-face")
    f.check_invariant()
    assert f.edge_step == 1
    assert f.face_step == PRE_SHIFT_N + 1


def test_advance_requires_entropy():
    state = initialize_session(b"S" * 16)
    with pytest.raises(ValueError):
        advance_edge(state, b"")
    with pytest.raises(ValueError):
        advance_face(state, b"")


def test_advance_is_pure_no_mutation():
    state = initialize_session(b"S" * 16)
    snapshot = (state.edge_element, state.edge_step,
                state.face_element, state.face_step, state.epoch)
    _ = advance_edge(state, b"entropy")
    _ = advance_face(state, b"entropy")
    assert (state.edge_element, state.edge_step,
            state.face_element, state.face_step, state.epoch) == snapshot


def test_advance_edge_deterministic_same_inputs():
    """Same (state, entropy) → same next state. Required for sync."""
    state = initialize_session(b"S" * 16)
    a = advance_edge(state, b"event-X")
    b = advance_edge(state, b"event-X")
    assert a == b


def test_advance_edge_different_entropy_different_state():
    state = initialize_session(b"S" * 16)
    a = advance_edge(state, b"event-A")
    b = advance_edge(state, b"event-B")
    assert a.edge_element != b.edge_element


def test_epoch_increments_on_outer_rotation():
    state = initialize_session(b"S" * 16)
    # Take OUTER_PERIOD edge steps. epoch should hit 1 exactly when
    # edge_step rolls past 84. Face also advances on each step to
    # preserve the invariant.
    for i in range(OUTER_PERIOD):
        state = advance_edge(state, f"e{i}".encode())
        state = advance_face(state, f"f{i}".encode())
    assert state.edge_step == OUTER_PERIOD
    assert state.epoch == 1


# ---------------------------------------------------------------------------
# Two-party synchronization (spec §5)
# ---------------------------------------------------------------------------


def test_two_parties_stay_synchronized_without_coordination():
    """Alice and Bob both initialize from the agreed session_id and
    independently apply the same event_entropy sequence. Their states
    must remain byte-identical across many steps.
    """
    sid = os.urandom(16)
    alice = initialize_session(sid)
    bob = initialize_session(sid)
    assert alice == bob

    events = [os.urandom(8) for _ in range(20)]
    for ev in events:
        alice = advance_face(advance_edge(alice, ev), ev + b"-f")
        bob = advance_face(advance_edge(bob, ev), ev + b"-f")
        assert alice == bob


def test_desync_recovery_via_replay():
    """Spec §5.3: a missed message → replay missed advance_edge calls
    using entropy derived from sequence numbers, up to one inner
    rotation period (6 steps). Beyond that, renegotiation."""
    sid = os.urandom(16)
    alice = initialize_session(sid)
    bob = initialize_session(sid)

    def seq_entropy(seq: int) -> bytes:
        return f"replay-seq-{seq}".encode()

    # Alice advances 5 steps; Bob misses them.
    for seq in range(5):
        ev = seq_entropy(seq)
        alice = advance_face(advance_edge(alice, ev), ev + b"-f")

    # Bob receives Alice's edge_step=5 in a header and replays.
    assert alice.edge_step == 5
    assert bob.edge_step == 0
    assert alice.edge_step - bob.edge_step <= INNER_PERIOD  # within window

    for seq in range(5):
        ev = seq_entropy(seq)
        bob = advance_face(advance_edge(bob, ev), ev + b"-f")

    assert alice == bob


def test_desync_beyond_inner_period_requires_renegotiation():
    """Spec §5.3 says > INNER_PERIOD gap requires renegotiation. We
    just verify that an INNER_PERIOD+1 gap is detectable from the
    publicly-observable edge_step counter."""
    sid = os.urandom(16)
    alice = initialize_session(sid)
    bob = initialize_session(sid)
    for seq in range(INNER_PERIOD + 1):
        ev = f"e{seq}".encode()
        alice = advance_face(advance_edge(alice, ev), ev + b"-f")
    gap = alice.edge_step - bob.edge_step
    assert gap > INNER_PERIOD


# ---------------------------------------------------------------------------
# Key derivation (spec §4.3)
# ---------------------------------------------------------------------------


def test_derive_key_material_length():
    state = initialize_session(b"S" * 16)
    for n in (16, 32, 64, 128):
        assert len(derive_key_material(state, b"enc", n)) == n


def test_derive_key_material_purpose_separation():
    state = initialize_session(b"S" * 16)
    k_enc = derive_key_material(state, b"encryption", 32)
    k_mac = derive_key_material(state, b"mac", 32)
    assert k_enc != k_mac


def test_key_material_excludes_edge_element():
    """Spec §4.3: edge_element is intentionally NOT in the IKM.
    Mutating only the edge_element must not change the key."""
    state = initialize_session(b"S" * 16)
    perturbed = LayeredProtocolState(
        edge_element=(state.edge_element + 1) % PSL_2_7_ORDER,
        edge_step=state.edge_step,
        face_element=state.face_element,
        face_step=state.face_step,
        session_id=state.session_id,
        epoch=state.epoch,
    )
    assert derive_key_material(state, b"k", 32) == derive_key_material(
        perturbed, b"k", 32
    )


def test_key_material_depends_on_face_element():
    state = initialize_session(b"S" * 16)
    perturbed = LayeredProtocolState(
        edge_element=state.edge_element,
        edge_step=state.edge_step,
        face_element=(state.face_element + 1) % CL8_BIVECTOR_COUNT,
        face_step=state.face_step,
        session_id=state.session_id,
        epoch=state.epoch,
    )
    assert derive_key_material(state, b"k", 32) != derive_key_material(
        perturbed, b"k", 32
    )


def test_key_material_depends_on_epoch():
    state = initialize_session(b"S" * 16)
    bumped = LayeredProtocolState(
        edge_element=state.edge_element,
        edge_step=state.edge_step,
        face_element=state.face_element,
        face_step=state.face_step,
        session_id=state.session_id,
        epoch=state.epoch + 1,
    )
    assert derive_key_material(state, b"k", 32) != derive_key_material(
        bumped, b"k", 32
    )


# ---------------------------------------------------------------------------
# _derive_element internals
# ---------------------------------------------------------------------------


def test_derive_element_in_group():
    for go in (PSL_2_7_ORDER, CL8_BIVECTOR_COUNT, 7, 84):
        out = _derive_element(0, b"entropy", 1, go)
        assert 0 <= out < go


def test_derive_element_step_decorrelates_repeats():
    """Same (current, entropy) at different step counters must give
    different group elements with overwhelming probability."""
    out_a = _derive_element(5, b"entropy", 1, PSL_2_7_ORDER)
    out_b = _derive_element(5, b"entropy", 2, PSL_2_7_ORDER)
    # 1/168 collision chance is acceptable for a single test, but
    # we make it robust by sampling 8 consecutive steps and demanding
    # at least 4 distinct values.
    outs = {
        _derive_element(5, b"entropy", s, PSL_2_7_ORDER)
        for s in range(1, 9)
    }
    assert len(outs) >= 4
    # And the explicit step-1 vs step-2 case must differ (with
    # negligible failure probability; if it ever collides, the test
    # is still informative).
    assert out_a != out_b
