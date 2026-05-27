"""op_2_58_2d_classifier.py — Projection classifier for OP-2.58.2d §3.3.

Pre-freeze infrastructure (Brief 07 / OP-2.58.2d, item 2). Implements the
argmax-Fano-line and argmax-pair-kernel classifier under the projection
metric ‖P_S v‖² / ‖v‖², per §3.3 of the pre-registration.

BIT-EXACTNESS CAVEAT (brief §2.3, §6 / see op_2_58_2d_prefreeze_report.md):
  §2.3 requires this classifier be *bit-exact* with the §2.66.2 classifier.
  The §2.66.2 classifier source (op_2_58_2_leakage_test.py,
  op_2_58_2b_advanced_attacks.py) is NOT present in the repo, so the
  bit-exactness comparison cannot be performed. This module reconstructs
  the classifier from the §3.3 specification and the kernel-basis output of
  op_2252_v2_kernel_involution.py. The reconstruction is internally
  consistent and analytically validated (in-subspace closure = 1.0), but
  the "identical to §2.66.2" claim is UNVERIFIED. See the report.

SUBSPACE DEFINITIONS (pinned; pre-registration §2.1 + §3.6(b)):
  - K_{a,b} (4D, "16→4 drop"): the right-kernel of L_x for the cross-edge
    ZD x = e_a + e_{b+8} (a < b, both in {1..7}), per OP-2.25.2-V2. By that
    result every kernel basis vector is a clean two-term ±1 cross-edge ZD;
    the real span of those four vectors is K_{a,b}.
  - F_L (8D, "16→8 drop"): the real span of the kernels of the three pairs
    lying on Fano line L = {a,b,c} — i.e. span(K_{a,b} ∪ K_{a,c} ∪ K_{b,c}).
    Verified to be exactly 8-dimensional for all seven lines at p=911.
    "Using the kernel-basis output of op_2252_v2_kernel_involution.py"
    per §3.6(b).

  FINDING (for §3.3 pre-freeze revision): the seven F_L real subspaces are
  NOT pairwise disjoint — a basis vector of one F_L can lie entirely inside
  another (a direct consequence of the kernel-involution structure, where a
  pair's kernel is supported on the cross-edges of *other* lines through the
  shared third point). So §2.5 test 3's strict "‖P_{F_L'} b‖²/‖b‖² < 1 for
  all L' ≠ L" does NOT hold. The operative classifier properties that DO
  hold are (i) in-subspace closure ‖P_{F_L} b‖²/‖b‖² = 1, and (ii) a near-
  uniform argmax distribution on random vectors (≈ 1/7). See the report.

CANDIDATES: a candidate vector v ∈ 𝕊_q^k is a length-16k integer vector
(k sedenion blocks of 16). The projection metric sums the squared
projected norm block-wise: ‖P_S v‖² = Σ_i ‖P_S v^{(i)}‖² over the k blocks,
with P_S the 16-dimensional orthogonal projection onto S. For k=1 this is
the single-sedenion classifier.
"""

from __future__ import annotations

import os
import sys
from itertools import combinations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sedenion_Fp import DIM, add_vec, basis_vec  # noqa: E402
from op_2252_v2_kernel_involution import (  # noqa: E402
    classify_two_term,
    lmm,
    normalize_kernel_vec,
    rref_kernel,
)

TOY_P = 911
N_INTERIOR = 7  # octonion imaginaries e_1..e_7


def _signed_lift(int_vec_mod_p: list[int], p: int) -> np.ndarray:
    """Lift an F_p vector to ℝ^16 via the signed representative in (-p/2, p/2]."""
    return np.array(
        [(c % p) if (c % p) <= p // 2 else (c % p) - p for c in int_vec_mod_p],
        dtype=float,
    )


def _clean_kernel_vectors(a: int, b: int, p: int) -> list[np.ndarray]:
    """The four clean ±1 two-term cross-edge kernel vectors of K_{a,b}.

    Cross-edge ZD x = e_a + e_{b+8} (canonical a < b). Each rref kernel
    basis vector normalises to a two-term ±1 cross-edge (OP-2.25.2-V2); we
    materialise that clean integer vector and lift it to ℝ^16.
    """
    x = add_vec(basis_vec(a), basis_vec(b + 8), p)
    ker = rref_kernel(lmm(x, p), p)
    out: list[np.ndarray] = []
    for kv in ker:
        _, nz_scaled = normalize_kernel_vec(kv, p)
        cls = classify_two_term(nz_scaled)
        assert cls is not None, f"K_{{{a},{b}}} basis vector is not a clean 2-term ZD"
        vec = [0] * DIM
        for idx, coeff in nz_scaled:
            vec[idx] = coeff
        out.append(np.array(vec, dtype=float))
    return out


def _orthonormal_columns(vectors: list[np.ndarray]) -> np.ndarray:
    """Orthonormal basis (16 × rank) of the real span of the given vectors."""
    A = np.array(vectors, dtype=float).T  # 16 × m
    Q, R = np.linalg.qr(A)
    rank = int(np.sum(np.abs(np.diag(R)) > 1e-9))
    return Q[:, :rank]


def fano_lines_from_multiplication(p: int) -> list[frozenset]:
    """The 7 Fano lines {a,b,c} ⊂ {1..7} read from e_a·e_b = ±e_c."""
    lines = set()
    for a, b in combinations(range(1, 8), 2):
        from sedenion_Fp import mul_vec
        prod = mul_vec(basis_vec(a), basis_vec(b), p)
        nz = [(i, v) for i, v in enumerate(prod) if v != 0]
        assert len(nz) == 1
        c = nz[0][0]
        lines.add(frozenset({a, b, c}))
    assert len(lines) == 7
    return sorted(lines, key=sorted)


class FanoLineClassifier:
    """Projection classifier of §3.3. Precomputes the F_L and K_{a,b}
    orthonormal bases at construction; classify() is O(subspaces · k)."""

    def __init__(self, p: int = TOY_P):
        self.p = p
        self.lines = fano_lines_from_multiplication(p)
        # Pair index: 21 unordered pairs {a,b}, a<b in 1..7.
        self.pairs = list(combinations(range(1, N_INTERIOR + 1), 2))
        # K_{a,b} orthonormal bases (16 × 4).
        self._K: dict[tuple[int, int], np.ndarray] = {}
        for (a, b) in self.pairs:
            self._K[(a, b)] = _orthonormal_columns(_clean_kernel_vectors(a, b, p))
        # F_L orthonormal bases (16 × 8): span of the three on-line pair kernels.
        self._F: dict[frozenset, np.ndarray] = {}
        for L in self.lines:
            a, b, c = sorted(L)
            vecs: list[np.ndarray] = []
            for (i, j) in [(a, b), (a, c), (b, c)]:
                vecs.extend(_clean_kernel_vectors(i, j, p))
            self._F[L] = _orthonormal_columns(vecs)

    # ---- projection metric ----

    @staticmethod
    def _projection_ratio(v: np.ndarray, Q: np.ndarray) -> float:
        """‖P_S v‖² / ‖v‖² summed block-wise over 16-dim blocks of v."""
        n = v.shape[0]
        assert n % DIM == 0, f"candidate length {n} is not a multiple of {DIM}"
        denom = float(np.dot(v, v))
        if denom == 0.0:
            return 0.0
        num = 0.0
        for start in range(0, n, DIM):
            block = v[start:start + DIM]
            coeffs = Q.T @ block
            num += float(np.dot(coeffs, coeffs))
        return num / denom

    def fano_subspace_dim(self, L: frozenset) -> int:
        return int(self._F[L].shape[1])

    def pair_subspace_dim(self, pair: tuple[int, int]) -> int:
        return int(self._K[pair].shape[1])

    def _lift(self, v) -> np.ndarray:
        """Signed-lift the candidate mod p into (-p/2, p/2] before projecting.

        Candidates are mod-q residues; the Euclidean projection metric is
        meaningful only on the centred representative. Idempotent on
        already-small signed vectors (e.g. BKZ short vectors), so the real
        attack use is unaffected."""
        p = self.p
        arr = np.asarray(v)
        return np.array(
            [(int(c) % p) if (int(c) % p) <= p // 2 else (int(c) % p) - p for c in arr],
            dtype=float,
        )

    def fano_ratios(self, v) -> dict[frozenset, float]:
        va = self._lift(v)
        return {L: self._projection_ratio(va, Q) for L, Q in self._F.items()}

    def pair_ratios(self, v) -> dict[tuple[int, int], float]:
        va = self._lift(v)
        return {pr: self._projection_ratio(va, Q) for pr, Q in self._K.items()}

    def classify(self, v) -> dict:
        """Return argmax-Fano-line, argmax-pair-kernel, and their confidences.

        Result dict:
          fano_line        : frozenset({a,b,c})   — ℓ̂(v)
          fano_ratio       : float                — confidence at argmax line
          pair             : (a, b)               — (â, b̂)(v)
          pair_ratio       : float                — confidence at argmax pair
        """
        fr = self.fano_ratios(v)
        pr = self.pair_ratios(v)
        # Stable, reproducible argmax: highest ratio, ties broken by sorted key.
        best_L = sorted(fr, key=lambda L: (-fr[L], sorted(L)))[0]
        best_pair = sorted(pr, key=lambda P: (-pr[P], P))[0]
        return {
            "fano_line": best_L,
            "fano_ratio": fr[best_L],
            "pair": best_pair,
            "pair_ratio": pr[best_pair],
        }


if __name__ == "__main__":
    clf = FanoLineClassifier(TOY_P)
    print(f"classifier at p={TOY_P}")
    print(f"  Fano lines: {[sorted(L) for L in clf.lines]}")
    print(f"  F_L dims: {sorted({clf.fano_subspace_dim(L) for L in clf.lines})}")
    print(f"  K_(a,b) dims: {sorted({clf.pair_subspace_dim(p) for p in clf.pairs})}")
    # in-subspace closure on a K basis vector
    a, b = 1, 2
    kv = _clean_kernel_vectors(a, b, TOY_P)[0]
    res = clf.classify(kv)
    print(f"  classify(K_(1,2) basis vec): line={sorted(res['fano_line'])} "
          f"ratio={res['fano_ratio']:.4f}, pair={res['pair']} ratio={res['pair_ratio']:.4f}")
