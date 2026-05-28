"""Tests for op_2_58_2d_construction (Brief 10.5). Toy scale q=911 only.

No test executes at spec parameters; test_spec_gate_enforced asserts the gate.
"""

from __future__ import annotations

import sys

import numpy as np
import pytest

from tools.op_2_58_2d_construction import (
    TOY_P,
    gen_public_matrix,
    gen_spec_instance,
    gen_zd_noise_sample,
)
from tools.op_2252_v2_kernel_involution import enumerate_two_term_ZDs, lmm, rref_kernel
from tools.op_2_58_2d_D1_fano_union_dimension import rank_modp
from tools.sedenion_Fp import DIM, add_vec, basis_vec, mul_vec

# The construction raises the bare-imported SpecParamsRefused (see Brief 09).
SpecParamsRefused = sys.modules["op_2_58_2d_lattice_attack"].SpecParamsRefused
SPEC_Q = 4_294_977_961
SPEC_K = 32


def _zd_set(p):
    return {tuple(d["vec"]) for d in enumerate_two_term_ZDs(p)}


def _zero(p):
    return [0] * DIM


def test_secret_is_non_zd():
    rng = np.random.default_rng(1)
    zd = _zd_set(TOY_P)
    for k in (1, 7):
        for _ in range(100):
            sample = gen_zd_noise_sample(TOY_P, k, sigma=2, rng=rng)
            for sv in sample["s"]:
                assert tuple(sv) not in zd


def test_z_is_zd():
    rng = np.random.default_rng(2)
    zd = _zd_set(TOY_P)
    for k in (1, 7):
        for _ in range(100):
            sample = gen_zd_noise_sample(TOY_P, k, sigma=2, rng=rng)
            for zv in sample["z"]:
                assert tuple(zv) in zd


def test_fano_line_label_consistency():
    rng = np.random.default_rng(3)
    sample = gen_zd_noise_sample(TOY_P, 7, sigma=2, rng=rng)
    for (a, b), L in zip(sample["pair"], sample["ell"]):
        prod = mul_vec(basis_vec(a), basis_vec(b), TOY_P)
        nz = [i for i, v in enumerate(prod) if v % TOY_P != 0]
        assert len(nz) == 1
        assert L == frozenset({a, b, nz[0]})


def test_pair_label_consistency():
    rng = np.random.default_rng(4)
    sample = gen_zd_noise_sample(TOY_P, 7, sigma=2, rng=rng)
    for (a, b), zv in zip(sample["pair"], sample["z"]):
        assert a < b
        # z = e_a + e_{b+8}: exactly those two coordinates are 1.
        expected = add_vec(basis_vec(a), basis_vec(b + 8), TOY_P)
        assert list(zv) == expected


def test_noise_in_kernel():
    rng = np.random.default_rng(5)
    for sigma in (1, 2, 4):
        sample = gen_zd_noise_sample(TOY_P, 7, sigma=sigma, rng=rng)
        for zv, ev in zip(sample["z"], sample["e"]):
            assert mul_vec(zv, ev, TOY_P) == _zero(TOY_P)


def test_noise_alpha_range():
    rng = np.random.default_rng(6)
    sample = gen_zd_noise_sample(TOY_P, 7, sigma=2, rng=rng)
    assert set(np.unique(sample["alphas"])).issubset({-1, 0, 1})


def test_noise_alpha_distribution():
    rng = np.random.default_rng(7)
    vals = []
    while len(vals) < 1000:
        sample = gen_zd_noise_sample(TOY_P, 7, sigma=2, rng=rng)
        vals.extend(sample["alphas"].ravel().tolist())
    vals = np.array(vals[:1000])
    n = len(vals)
    expected = n / 3
    sd = (n * (1 / 3) * (2 / 3)) ** 0.5
    for v in (-1, 0, 1):
        count = int(np.sum(vals == v))
        assert abs(count - expected) < 3 * sd, f"alpha={v} count {count} off uniform"


def test_kernel_basis_is_4d():
    rng = np.random.default_rng(8)
    sample = gen_zd_noise_sample(TOY_P, 7, sigma=2, rng=rng)
    for i in range(7):
        kb = [[int(x) for x in sample["kernels"][i, j]] for j in range(4)]
        assert len(kb) == 4
        assert rank_modp(kb, TOY_P) == 4


def test_b_round_trip():
    rng = np.random.default_rng(9)
    inst = gen_spec_instance(TOY_P, k=7, sigma=2, rng=rng)
    A, s, e, b = inst["A"], inst["s"], inst["e"], inst["b"]
    for i in range(inst["k"]):
        acc = [0] * DIM
        for j in range(inst["k"]):
            acc = add_vec(acc, mul_vec([int(x) for x in A[i, j]], s[j], TOY_P), TOY_P)
        recomputed = add_vec(acc, e[i], TOY_P)
        assert list(b[i]) == recomputed
        # b - A·s - e ≡ 0
        diff = [(b[i][d] - acc[d] - e[i][d]) % TOY_P for d in range(DIM)]
        assert diff == _zero(TOY_P)


def test_spec_gate_enforced():
    rng = np.random.default_rng(10)
    with pytest.raises(SpecParamsRefused):
        gen_spec_instance(p=SPEC_Q, k=SPEC_K, sigma=2, rng=rng)


@pytest.mark.parametrize("structure", ["psl27_equivariant", "singer_cycle"])
def test_matrix_structure_halts(structure):
    rng = np.random.default_rng(11)
    with pytest.raises(NotImplementedError) as excinfo:
        gen_public_matrix(TOY_P, 7, rng, structure=structure)
    msg = str(excinfo.value)
    assert "§2.3" in msg
    assert "§2.69.2" in msg


# ---------------------------------------------------------------------------
# §2.3-bis (revised) — trapdoor cardinality (line / pair / kernel)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("reading", ["fano_line_7", "kernel_42"])
def test_trapdoor_cardinality_halts(reading):
    """OP-2.58.B.card / §2.58.B.1: non-pair cardinalities must halt with a
    runtime message citing OP-2.58.B.card and §2.58.B.1."""
    rng = np.random.default_rng(12)
    with pytest.raises(NotImplementedError) as excinfo:
        gen_zd_noise_sample(TOY_P, k=7, sigma=1, rng=rng,
                            trapdoor_cardinality=reading)
    msg = str(excinfo.value)
    assert "OP-2.58.B.card" in msg, msg
    assert "§2.58.B.1" in msg, msg


def _rref_kernel_key(z_vec, p):
    """RREF fingerprint of ker(L_z) as a hashable tuple — unique per subspace."""
    K = rref_kernel(lmm(z_vec, p), p)
    A = [list(v) for v in K]
    nr, nc = len(A), len(A[0]) if A else 0
    r = 0
    for c in range(nc):
        if r >= nr:
            break
        piv = next((i for i in range(r, nr) if A[i][c] % p != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(nr):
            if i != r and A[i][c] % p != 0:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(nc)]
        r += 1
    return tuple(tuple(row) for row in A[:r])


def test_42_kernel_partition():
    """§2.58.B.1 (A1 finding): the 84 two-term ZDs partition into exactly 42
    distinct ker(L_z), 2 per unordered pair, at toy scale. Locks the finding
    so a future refactor of the kernel machinery cannot silently regress it."""
    zds = enumerate_two_term_ZDs(TOY_P)
    assert len(zds) == 84, f"expected 84 ZDs, got {len(zds)}"
    kernels: dict[tuple, list[tuple[int, int]]] = {}
    pairs: set[frozenset[int]] = set()
    for zd in zds:
        key = _rref_kernel_key(zd["vec"], TOY_P)
        kernels.setdefault(key, []).append(tuple(zd["interior_pair"]))
        pairs.add(frozenset(zd["interior_pair"]))
    assert len(kernels) == 42, f"expected 42 distinct kernels, got {len(kernels)}"
    assert all(len(v) == 2 for v in kernels.values()), \
        f"expected 2 ZDs per kernel, got {sorted({len(v) for v in kernels.values()})}"
    assert len(pairs) == 21, f"expected 21 unordered pairs, got {len(pairs)}"
