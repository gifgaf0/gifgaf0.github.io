"""Tests for the toy-mode SLWE wrapper backed by tools/sqt_slwe.py.

The supplied source self-reports DFR ≈ 0.48 at (p=911, k=4) with the
verdict "noise too large for this p" — i.e., the brief's
"DFR < 0.01 over 1000 trials" target is not met as shipped. These
tests therefore split into:

- structural correctness (sizes, determinism, basic roundtrip on a
  successful trial), which we assert,
- empirical DFR over 1000 trials, which we measure and record but do
  *not* assert below 0.01 — there is a separate xfail-marked test
  that pins the target so the assertion lights up if/when the source
  is fixed.
"""

from __future__ import annotations

import pytest

from hybrid_kem.entropy.drbg import DRBG
from hybrid_kem.kem_slwe.slwe_wrapper import SLWEWrapper

K_TOY = 4
TOY_PK_BYTES = (K_TOY * K_TOY + K_TOY) * 16 * 2   # k*k matrix + k vector, 16 coeffs * 2 bytes
TOY_SK_BYTES = K_TOY * 16 * 2
TOY_CT_BYTES = K_TOY * 16 * 2 + 2                 # k sedenions + 2-byte c2

DFR_TRIALS = 1000
CATASTROPHE_CEILING = 0.55  # noise-only ≈ 0.5; reject anything worse


def _drbg(seed: int) -> DRBG:
    d = DRBG()
    d.instantiate(seed.to_bytes(32, "big"), b"\x42" * 16, b"slwe-toy-test")
    return d


@pytest.fixture(scope="module")
def wrapper() -> SLWEWrapper:
    return SLWEWrapper(mode="toy")


def test_toy_pk_sk_sizes(wrapper):
    pk, sk = wrapper.keygen(_drbg(1))
    assert len(pk) == TOY_PK_BYTES, len(pk)
    assert len(sk) == TOY_SK_BYTES, len(sk)


def test_toy_ct_size(wrapper):
    pk, _sk = wrapper.keygen(_drbg(2))
    ct, ss = wrapper.encaps(pk, _drbg(3))
    assert len(ct) == TOY_CT_BYTES, len(ct)
    assert len(ss) == 32


def test_toy_decaps_returns_32_bytes(wrapper):
    pk, sk = wrapper.keygen(_drbg(4))
    ct, _ss = wrapper.encaps(pk, _drbg(5))
    out = wrapper.decaps(sk, ct)
    assert isinstance(out, bytes)
    assert len(out) == 32


def test_toy_keygen_deterministic_under_drbg(wrapper):
    """Same DRBG seed at keygen reproduces the same (pk, sk)."""
    a = wrapper.keygen(_drbg(11))
    b = wrapper.keygen(_drbg(11))
    assert a == b


def test_toy_at_least_one_trial_succeeds(wrapper):
    """Smoke check: at least one of 32 trials decapsulates to the right ss.

    This guards the wiring (serialisation, sedenion arithmetic, dispatch)
    against catastrophic regressions. We do not assert anything stronger
    because the source's noise budget gives ~50% per trial.
    """
    successes = 0
    for i in range(32):
        pk, sk = wrapper.keygen(_drbg(100 + i))
        ct, ss_enc = wrapper.encaps(pk, _drbg(200 + i))
        ss_dec = wrapper.decaps(sk, ct)
        if ss_enc == ss_dec:
            successes += 1
    assert successes >= 1, (
        "wrapper round-trip never succeeded over 32 trials — "
        "wiring is broken (the supplied source's DFR is ~0.5, "
        "not 1.0)"
    )


@pytest.mark.slow
def test_toy_measure_dfr_1000(wrapper, record_property):
    """Run 1000 trials, record empirical DFR, refuse to call it healthy.

    We assert only the catastrophe ceiling (DFR < 0.55 — i.e., the
    scheme is at least not anti-correct). The brief's < 0.01 target
    is pinned in test_toy_dfr_target_xfail below; if/when the source's
    noise budget is fixed, that test will start passing.
    """
    fails = 0
    for i in range(DFR_TRIALS):
        pk, sk = wrapper.keygen(_drbg(0x1000 + i))
        ct, ss_enc = wrapper.encaps(pk, _drbg(0x2000 + i))
        if wrapper.decaps(sk, ct) != ss_enc:
            fails += 1
    dfr = fails / DFR_TRIALS
    record_property("slwe_toy_dfr", dfr)
    assert dfr < CATASTROPHE_CEILING, (
        f"DFR {dfr:.3f} exceeds catastrophe ceiling {CATASTROPHE_CEILING}"
    )


@pytest.mark.slow
@pytest.mark.xfail(
    reason="supplied source self-reports DFR≈0.48 at (p=911,k=4); "
           "noise > p/4 budget. See tools/BRIEF_02_SUMMARY.md.",
    strict=False,
)
def test_toy_dfr_target_xfail(wrapper):
    """Brief 02 §1 target: DFR < 0.01 over 1000 trials. Currently fails."""
    fails = 0
    for i in range(DFR_TRIALS):
        pk, sk = wrapper.keygen(_drbg(0x3000 + i))
        ct, ss_enc = wrapper.encaps(pk, _drbg(0x4000 + i))
        if wrapper.decaps(sk, ct) != ss_enc:
            fails += 1
    dfr = fails / DFR_TRIALS
    assert dfr < 0.01, f"DFR {dfr:.3f} above brief target 0.01"
