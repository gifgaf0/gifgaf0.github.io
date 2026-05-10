"""Programmatic ring audit tests for ML-KEM's R_3329.

Wires the four-line analytical audit (Brief 03, commit 2017c4a) plus
the three Cl(6) naturality obstructions into the test suite. These
are *exact* assertions on computed mathematical facts; they should
always pass and run in well under a minute.

The audit functions live in ``tools/ring_audit.py`` and
``tools/clifford_check.py`` so they can be invoked from a script
context too. This file imports them and asserts the documented
results.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

# Make tools/ importable from the test suite.
_TOOLS = Path(__file__).resolve().parents[2] / "tools"
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from tools import clifford_check, ring_audit   # noqa: E402


# ---------------------------------------------------------------------------
# Audit line 1: factorisation of X^256 + 1 over F_3329
# ---------------------------------------------------------------------------


def test_audit_factor_r3329():
    r = ring_audit.factor_r3329()
    assert r["modulus"] == 3329
    assert r["degree"] == 256
    assert r["zeta"] == 17
    assert r["zeta_order"] == 256
    assert r["num_factors"] == 128
    assert r["factor_form"] == "X^2 - root"
    assert r["seventeen_is_quadratic_nonresidue"] is True
    assert r["distinct_roots"] is True
    assert r["all_factors_irreducible"] is True
    assert r["product_equals_X256_plus_1"] is True
    # Cross-check against the cached JSON if present.
    if r["json_match"] is not None:
        assert r["json_match"] is True


# ---------------------------------------------------------------------------
# Audit line 2: Z_7 subgroup of F_3329^*
# ---------------------------------------------------------------------------


def test_audit_singer_z7_premise_fails():
    r = ring_audit.singer_orbit_audit()
    assert r["q"] == 3329
    assert r["q_minus_1"] == 3328
    assert r["q_mod_7"] == 4   # not 1, contra the brief's misquoted premise
    assert r["q_minus_1_factorisation"] == {2: 8, 13: 1}
    assert r["z_7_subgroup_exists_in_F_q_star"] is False
    assert r["natural_cyclic_order"] == 128
    assert r["natural_cyclic_order_factorisation"] == {2: 7}
    # 7 ∤ 3328 — explicit check, not just a label.
    assert r["q_minus_1"] % 7 != 0


# ---------------------------------------------------------------------------
# Audit line 3: ZD pair graph
# ---------------------------------------------------------------------------


def test_audit_zd_graph_is_K128():
    r = ring_audit.zd_graph_audit()
    assert r["num_vertices"] == 128
    assert r["num_edges"] == 8128                        # = C(128, 2)
    assert r["each_factor_is_field"] is True
    assert r["graph_is_K_n"] is True
    assert r["graph_label"] == "K_128"
    assert r["automorphism_group"] == "Sym(128)"
    # log10(128!) ≈ 215.6 by Stirling. Sanity check the order of magnitude.
    assert 215.0 < r["automorphism_group_order_log10"] < 216.5


# ---------------------------------------------------------------------------
# Audit line 4: (2,3,7) angle triples in primitive 256-th roots
# ---------------------------------------------------------------------------


def test_audit_237_triples_in_primitives():
    r = ring_audit.discrete_circle_audit()
    assert r["modulus"] == 256
    assert r["ratio_237"] == (21, 14, 6)
    assert r["primitive_count"] == 128
    # Parity argument: 14m and 6m are even for every m, so no triple of
    # primitive 256-th roots (all-odd indices) can be (21:14:6)-proportional.
    assert r["parity_obstruction"] is True
    assert r["triples_in_primitives"] == 0
    assert r["triples_full_circle"] == 248
    assert r["total_unordered_primitive_triples"] == math.comb(128, 3)


# ---------------------------------------------------------------------------
# Cl(6) naturality obstructions (Task 4)
# ---------------------------------------------------------------------------


def test_clifford_obstruction_multiplicity():
    """The Cl(6) embedding into M_128(F_3329) has multiplicity 16."""
    r = clifford_check.obstruction_multiplicity()
    assert r["spinor_commutant_dim"] == 1, r
    assert r["spinor_irreducible"] is True
    assert r["multiplicity"] == 16
    assert r["lifted_commutant_dim_predicted"] == 256
    assert r["obstruction_holds"] is True


def test_clifford_obstruction_no_z2_6_in_cyclic_128():
    """The natural Z/128 NTT symmetry has no (Z/2)^6 subgroup."""
    r = clifford_check.obstruction_no_z2_6_in_z128()
    assert r["cyclic_order"] == 128
    assert r["elements_of_order_2_in_cyclic"] == 1
    assert r["elements_of_order_2_needed_for_(Z/2)^6"] == 63
    assert r["obstruction_holds"] is True


def test_clifford_obstruction_no_diagonal_cl6():
    """No faithful Cl(6) action by diagonal generators in M_128(F_3329)."""
    r = clifford_check.obstruction_no_diagonal_cl6()
    assert r["ambient_dim"] == 128
    assert r["two_random_diagonal_involutions_commute"] is True
    assert r["each_squares_to_identity"] is True
    assert r["obstruction_holds"] is True


# ---------------------------------------------------------------------------
# Brief 05 (OP-F): Singer-orbit A is rank-deficient at k=32
# ---------------------------------------------------------------------------
#
# Three exact-fact assertions extracted from the GS-profile audit
# (tools/gs_profile.py). The full profile is too slow for CI (~25 s
# at k=32) but the underlying structural facts that make it slow are
# fast to verify on their own and worth pinning so they cannot
# regress silently.


def _build_a_matrices(k: int, p: int, seed: int = 0xb05):
    import random as _r
    from tools import gs_profile as _gs
    A_singer = _gs.make_singer_A(k, p, _r.Random(seed))
    A_random = _gs.make_random_A(k, p, _r.Random(seed + 1))
    return _gs.flatten_sedenion_matrix(A_singer, p), \
           _gs.flatten_sedenion_matrix(A_random, p)


def test_singer_a_column_period_at_k32():
    """At k=32, columns of A_F at distance 112 are literal integer copies."""
    from tools import gs_profile as _gs
    Asf, _ = _build_a_matrices(k=32, p=8191)
    period = _gs._column_period(Asf)
    # 7 (Singer cycle order) × 16 (sedenion dim) = 112.
    assert period == 112, period


def test_singer_a_fp_rank_at_most_112():
    """Singer A_F has F_p-rank at most 7·16 = 112 at k=32."""
    from tools import gs_profile as _gs
    Asf, _ = _build_a_matrices(k=32, p=8191)
    r = _gs._matrix_rank_mod_p(Asf, 8191)
    assert r <= 112, r


def test_random_a_fp_rank_full_at_k32():
    """Uniform-random A_F is F_p full rank (= 512) at k=32 with overwhelming
    probability. Deterministic seed pins the result."""
    from tools import gs_profile as _gs
    _, Arf = _build_a_matrices(k=32, p=8191)
    r = _gs._matrix_rank_mod_p(Arf, 8191)
    assert r == 512, r
