"""Tests for the BBF-G-S 2019 combiner (combiner.kdf_combiner)."""

from __future__ import annotations

import pytest

from hybrid_kem.combiner.kdf_combiner import combine


def _inputs():
    return {
        "ss_a": b"\x01" * 32,
        "ss_b": b"\x02" * 32,
        "ct_a": b"\x03" * 64,
        "ct_b": b"\x04" * 64,
        "pk_a": b"\x05" * 32,
        "pk_b": b"\x06" * 32,
    }


def test_output_is_32_bytes():
    out = combine(**_inputs())
    assert len(out) == 32


def test_deterministic():
    a = combine(**_inputs())
    b = combine(**_inputs())
    assert a == b


def test_changing_ss_a_changes_output():
    base = combine(**_inputs())
    args = _inputs()
    args["ss_a"] = b"\x11" * 32
    assert combine(**args) != base


def test_changing_ss_b_changes_output():
    base = combine(**_inputs())
    args = _inputs()
    args["ss_b"] = b"\x12" * 32
    assert combine(**args) != base


def test_transcript_binding_ct_a():
    base = combine(**_inputs())
    args = _inputs()
    args["ct_a"] = b"\x99" * 64
    assert combine(**args) != base, "must be transcript-binding on ct_a"


def test_transcript_binding_ct_b():
    base = combine(**_inputs())
    args = _inputs()
    args["ct_b"] = b"\x99" * 64
    assert combine(**args) != base, "must be transcript-binding on ct_b"


def test_pk_change_alters_output():
    base = combine(**_inputs())
    args = _inputs()
    args["pk_a"] = b"\xee" * 32
    assert combine(**args) != base


def test_empty_ss_rejected():
    args = _inputs()
    args["ss_a"] = b""
    with pytest.raises(ValueError):
        combine(**args)


def test_concat_ambiguity_resolved():
    # If we naively concatenated ct_a||ct_b without length-prefixing, then
    # (ct_a=AB, ct_b=CD) and (ct_a=ABCD, ct_b=) would collide. Verify they don't.
    a = combine(b"x"*32, b"y"*32, b"AB", b"CD", b"p"*32, b"q"*32)
    b = combine(b"x"*32, b"y"*32, b"ABCD", b"", b"p"*32, b"q"*32)
    assert a != b
