"""Round-trip and convention tests for op_2_58_2d_lattice_attack (Brief 07, item 3).

All exact integer linear algebra — no BKZ, no spec parameters, toy scale only
(q=911, k=7). See op_2_58_2d_prefreeze_report.md for the pinned convention and
the §3.2 sign deviation.
"""

from __future__ import annotations

import math

import pytest

from tools.op_2_58_2d_lattice_attack import (
    DIM,
    SPEC_K,
    SPEC_Q,
    SpecParamsRefused,
    build_primal_lattice,
    build_scalar_lwe,
    gaussian_heuristic,
    gen_toy_instance,
    l2_norm,
    left_mult_matrix,
    log_det_primal,
    recover_lattice_coeffs,
    target_vector,
    vec_mat_mul,
)
from tools.sedenion_Fp import basis_vec, mul_vec


def _toy():
    inst = gen_toy_instance(seed=20260527, q=911, k=7, eta=2)
    lwe = build_scalar_lwe(inst["A"], inst["s"], inst["e"], inst["q"])
    return inst, lwe


# ---------------------------------------------------------------------------
# §3.3 test 1 — known-instance round-trip
# ---------------------------------------------------------------------------


def test_target_is_in_lattice_round_trip():
    inst, lwe = _toy()
    B = build_primal_lattice(lwe["A_scalar"], lwe["b_scalar"], inst["q"])
    v_target = target_vector(inst["e_scalar_signed"], inst["s_scalar_signed"])
    z = recover_lattice_coeffs(
        lwe["A_scalar"], inst["s_scalar_signed"], inst["e_scalar_signed"],
        lwe["b_scalar"], inst["q"],
    )
    assert vec_mat_mul(z, B) == v_target


def test_recovered_coeffs_have_expected_form():
    """z = (m_0, s_scalar, 1): last coord 1, middle block equals s_scalar."""
    inst, lwe = _toy()
    z = recover_lattice_coeffs(
        lwe["A_scalar"], inst["s_scalar_signed"], inst["e_scalar_signed"],
        lwe["b_scalar"], inst["q"],
    )
    n = lwe["n_eff"]
    assert z[-1] == 1
    assert z[n:2 * n] == inst["s_scalar_signed"]


def test_target_norm_matches_independent_computation():
    inst, _ = _toy()
    v_target = target_vector(inst["e_scalar_signed"], inst["s_scalar_signed"])
    independent = math.sqrt(
        sum(x * x for x in inst["e_scalar_signed"])
        + sum(x * x for x in inst["s_scalar_signed"])
        + 1
    )
    assert math.isclose(l2_norm(v_target), independent, rel_tol=0, abs_tol=1e-9)


# ---------------------------------------------------------------------------
# §3.3 test 2 — short-vector (BDD) check
# ---------------------------------------------------------------------------


def test_target_shorter_than_gaussian_heuristic():
    inst, lwe = _toy()
    v_target = target_vector(inst["e_scalar_signed"], inst["s_scalar_signed"])
    n = lwe["n_eff"]
    gh = gaussian_heuristic(2 * n + 1, log_det_primal(n, inst["q"]))
    assert l2_norm(v_target) < gh, (
        f"||v_target||={l2_norm(v_target):.3f} not < gh={gh:.3f}; "
        "LWE instance not in the unique-decoding regime"
    )


# ---------------------------------------------------------------------------
# §3.3 test 3 — convention sanity
# ---------------------------------------------------------------------------


def test_determinant_is_q_to_the_n_eff():
    """B is block lower-triangular with diagonal blocks q·I, I, [1], so
    det = q^{n_eff}. Verify the above-diagonal blocks are zero (which makes
    the determinant exactly q^{n_eff}) and that log det matches."""
    inst, lwe = _toy()
    B = build_primal_lattice(lwe["A_scalar"], lwe["b_scalar"], inst["q"])
    n = lwe["n_eff"]
    N = 2 * n + 1
    # Above-diagonal blocks must be zero: cols [n:2n] of rows [0:n], col [2n]
    # of rows [0:2n].
    for i in range(n):
        for c in range(n, N):
            assert B[i][c] == 0
    for i in range(n, 2 * n):
        assert B[i][2 * n] == 0
    # Diagonal blocks: q·I, then I, then 1.
    for i in range(n):
        assert B[i][i] == inst["q"]
    for i in range(n, 2 * n):
        assert B[i][i] == 1
    assert B[2 * n][2 * n] == 1
    log_det = log_det_primal(n, inst["q"])
    assert math.isclose(log_det, n * math.log(inst["q"]), rel_tol=1e-12)


def test_exact_determinant_small_instance():
    """Exact integer determinant on a tiny k=1 instance (dim 33) confirms
    det = q^{n_eff} beyond the structural argument."""
    inst = gen_toy_instance(seed=20260527, q=911, k=1, eta=2, h_s=1)
    lwe = build_scalar_lwe(inst["A"], inst["s"], inst["e"], inst["q"])
    B = build_primal_lattice(lwe["A_scalar"], lwe["b_scalar"], inst["q"])
    det = _integer_determinant([row[:] for row in B])
    assert det == inst["q"] ** lwe["n_eff"]


def test_row_operations_preserve_target_membership():
    """Adding an integer multiple of one basis row to another preserves the
    lattice, hence v_target stays a member (with updated coefficients)."""
    inst, lwe = _toy()
    B = build_primal_lattice(lwe["A_scalar"], lwe["b_scalar"], inst["q"])
    v_target = target_vector(inst["e_scalar_signed"], inst["s_scalar_signed"])
    z = recover_lattice_coeffs(
        lwe["A_scalar"], inst["s_scalar_signed"], inst["e_scalar_signed"],
        lwe["b_scalar"], inst["q"],
    )
    # Apply a unimodular row op: row0 += 3·row1. The lattice is unchanged;
    # v_target = z·B still holds with z' where z'_0 absorbs the change.
    B2 = [row[:] for row in B]
    for c in range(len(B2[0])):
        B2[0][c] += 3 * B2[1][c]
    # New coefficients: z'·B2 = z·B requires z'_1 = z_1 − 3·z'_0, z'_0 = z_0.
    z2 = z[:]
    z2[1] = z[1] - 3 * z[0]
    assert vec_mat_mul(z2, B2) == v_target


def test_lattice_contains_q_unit_vectors():
    """Each q-row is the vector (0,…,q,…,0); these are lattice members."""
    inst, lwe = _toy()
    B = build_primal_lattice(lwe["A_scalar"], lwe["b_scalar"], inst["q"])
    n = lwe["n_eff"]
    N = 2 * n + 1
    for i in range(n):
        expected = [0] * N
        expected[i] = inst["q"]
        assert B[i] == expected


# ---------------------------------------------------------------------------
# §3.3 test 4 — sedenion-unrolling sanity
# ---------------------------------------------------------------------------


def test_left_mult_block_matches_sedenion_product():
    """A_11 · s_1 computed two ways: sedenion product vs 16×16 block."""
    inst, _ = _toy()
    q = inst["q"]
    A11 = inst["A"][0][0]
    s1 = inst["s"][0]
    direct = mul_vec(A11, s1, q)
    block = left_mult_matrix(A11, q)
    via_block = [sum(block[r][c] * s1[c] for c in range(DIM)) % q for r in range(DIM)]
    assert direct == via_block


def test_left_mult_matrix_on_basis_vectors():
    """Column j of M_u is u·e_j by definition."""
    inst, _ = _toy()
    q = inst["q"]
    u = inst["A"][1][2]
    M = left_mult_matrix(u, q)
    for j in range(DIM):
        col = [M[r][j] for r in range(DIM)]
        assert col == mul_vec(u, basis_vec(j), q)


# ---------------------------------------------------------------------------
# §3.3 test 5 — scalar-LWE round-trip
# ---------------------------------------------------------------------------


def test_scalar_lwe_consistency():
    """A_scalar·s_scalar + e_scalar = b_scalar (mod q), independent of the
    lattice."""
    inst, lwe = _toy()
    q = inst["q"]
    n = lwe["n_eff"]
    A_scalar = lwe["A_scalar"]
    s_scalar = lwe["s_scalar"]
    e_scalar = [x % q for x in lwe["e_scalar"]]
    recomputed = []
    for r in range(n):
        acc = sum(A_scalar[r][c] * s_scalar[c] for c in range(n))
        recomputed.append((acc + e_scalar[r]) % q)
    assert recomputed == [x % q for x in lwe["b_scalar"]]


def test_sedenion_and_scalar_b_agree():
    """b computed via sedenion products equals b_scalar reshaped."""
    inst, lwe = _toy()
    q = inst["q"]
    b_from_sed = []
    for sed in lwe["b_sedenion"]:
        b_from_sed.extend(x % q for x in sed)
    assert b_from_sed == [x % q for x in lwe["b_scalar"]]


# ---------------------------------------------------------------------------
# Discipline gate (brief §6)
# ---------------------------------------------------------------------------


def test_spec_params_refused_by_default():
    with pytest.raises(SpecParamsRefused):
        gen_toy_instance(q=SPEC_Q, k=SPEC_K)


def test_spec_params_allowed_with_flag():
    """The gate can be opened explicitly (this does NOT run any attack —
    it only constructs a tiny instance to prove the flag works). Use k=1
    to keep it cheap; q=SPEC_Q triggers the gate."""
    inst = gen_toy_instance(q=SPEC_Q, k=1, h_s=1, allow_spec_params=True)
    assert inst["q"] == SPEC_Q


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _integer_determinant(M: list[list[int]]) -> int:
    """Exact integer determinant via the Bareiss fraction-free algorithm."""
    n = len(M)
    sign = 1
    prev = 1
    for i in range(n - 1):
        if M[i][i] == 0:
            swap = next((r for r in range(i + 1, n) if M[r][i] != 0), None)
            if swap is None:
                return 0
            M[i], M[swap] = M[swap], M[i]
            sign = -sign
        for r in range(i + 1, n):
            for c in range(i + 1, n):
                M[r][c] = (M[r][c] * M[i][i] - M[r][i] * M[i][c]) // prev
        prev = M[i][i]
    return sign * M[n - 1][n - 1]
