"""op_2_58_2d_lattice_attack.py — Primal LWE lattice construction for OP-2.58.2d.

Pre-freeze infrastructure (Brief 07 / OP-2.58.2d, item 3). This module
covers ONLY the primal-basis (a) construction of §3.6 of the
pre-registration. The Fano-projected basis (b) variant is a separate,
post-freeze task (it depends on §2.58.B Fano-line subspace data) and is
left as an explicit stub.

DISCIPLINE (pre-registration §6 / brief §6):
  - This is pre-freeze infrastructure. It does NOT run the attack.
  - It must not be executed against the §2.58.B construction at the spec
    parameters of §3.1 (k=32, q=4_294_977_961). Any entry point capable
    of spec-scale inputs is gated behind ``allow_spec_params=True`` which
    is never set by default.
  - Synthetic / toy-scale inputs only (q=911, k∈{7,14}).

PINNED CONVENTION (brief §3.2 — see op_2_58_2d_prefreeze_report.md):
  The brief's literal §3.2 basis uses ``+A_scalarᵀ`` in the middle block.
  That does NOT round-trip: with b = A·s + e, the target (e, s, 1) is in
  the lattice only if the middle block is ``-A_scalarᵀ`` (equivalently,
  the relation e = b − A·s). This module pins ``-A_scalarᵀ`` and the
  round-trip test confirms it. The basis (row convention, z·B):

      B = [ q · I_{n_eff}      0           0   ]   (n_eff rows)
          [  -A_scalarᵀ     I_{n_eff}      0   ]   (n_eff rows)
          [   b_scalarᵀ        0           1   ]   (1 row)

  dimensions (2·n_eff + 1) square; N_lat = 2·n_eff is the BKZ-relevant
  dimension (the +1 is the Kannan embedding coordinate). Target short
  vector v_target = (e_scalar, s_scalar, 1).
"""

from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sedenion_Fp import DIM, add_vec, basis_vec, mul_vec  # noqa: E402

# Spec parameters (pre-registration §3.1). Present only so the gate can
# refuse them; this module never runs the attack at these values.
SPEC_Q = 4_294_977_961
SPEC_K = 32

TOY_Q = 911
TOY_ETA = 2


class SpecParamsRefused(RuntimeError):
    """Raised when spec-scale parameters are requested without allow_spec_params."""


def _check_not_spec(q: int, k: int, allow_spec_params: bool) -> None:
    if allow_spec_params:
        return
    if q >= SPEC_Q or k >= SPEC_K:
        raise SpecParamsRefused(
            f"refusing q={q}, k={k}: looks like spec scale (q>={SPEC_Q} or "
            f"k>={SPEC_K}). This is pre-freeze infrastructure; pass "
            f"allow_spec_params=True only after the §6 freeze."
        )


# ---------------------------------------------------------------------------
# Left-multiplication (regular representation) of a sedenion
# ---------------------------------------------------------------------------


def left_mult_matrix(u: list[int], q: int) -> list[list[int]]:
    """16×16 matrix M_u over F_q with M_u · w = (u · w) for any sedenion w.

    Column j is u · e_j. Identical to ``op_2252_v2_kernel_involution.lmm``;
    re-derived here so the lattice module has no import cycle with the
    kernel-involution tool.
    """
    M = [[0] * DIM for _ in range(DIM)]
    for j in range(DIM):
        col = mul_vec(u, basis_vec(j), q)
        for i in range(DIM):
            M[i][j] = col[i] % q
    return M


# ---------------------------------------------------------------------------
# Sedenion ↔ scalar unrolling
# ---------------------------------------------------------------------------


def sedenion_matvec(A: list[list[list[int]]], s: list[list[int]], q: int) -> list[list[int]]:
    """(A·s)_i = Σ_j A_{ij} · s_j via sedenion products, mod q."""
    k = len(A)
    out = []
    for i in range(k):
        acc = [0] * DIM
        for j in range(k):
            acc = add_vec(acc, mul_vec(A[i][j], s[j], q), q)
        out.append(acc)
    return out


def flatten(vec_of_sedenions: list[list[int]]) -> list[int]:
    out: list[int] = []
    for sed in vec_of_sedenions:
        out.extend(sed)
    return out


def build_scalar_lwe(
    A: list[list[list[int]]],
    s: list[list[int]],
    e: list[list[int]],
    q: int,
) -> dict:
    """Unroll a Module-SLWE instance (A, s, e) over 𝕊_q^k to scalar-LWE.

    Returns a dict with:
      A_scalar  : (n_eff × n_eff) list[list[int]] over F_q
      s_scalar  : length n_eff
      e_scalar  : length n_eff
      b_scalar  : length n_eff, = (A_scalar·s_scalar + e_scalar) mod q
      b_sedenion: the sedenion form of b = A·s + e (for cross-check)
      n_eff     : k · 16
    """
    k = len(A)
    n_eff = k * DIM
    # A_scalar: block (i,j) = left-mult matrix of A_{ij}
    A_scalar = [[0] * n_eff for _ in range(n_eff)]
    for i in range(k):
        for j in range(k):
            block = left_mult_matrix(A[i][j], q)
            for r in range(DIM):
                for c in range(DIM):
                    A_scalar[i * DIM + r][j * DIM + c] = block[r][c]
    s_scalar = flatten(s)
    e_scalar = flatten(e)
    # b via the scalar operator
    b_scalar = [0] * n_eff
    for r in range(n_eff):
        acc = 0
        row = A_scalar[r]
        for c in range(n_eff):
            acc += row[c] * s_scalar[c]
        b_scalar[r] = (acc + e_scalar[r]) % q
    # b via sedenion products (independent cross-check)
    b_sed = sedenion_matvec(A, s, q)
    for i in range(len(b_sed)):
        b_sed[i] = [x % q for x in add_vec(b_sed[i], e[i], q)]
    return {
        "A_scalar": A_scalar,
        "s_scalar": [x % q for x in s_scalar],
        "e_scalar": list(e_scalar),
        "b_scalar": b_scalar,
        "b_sedenion": b_sed,
        "n_eff": n_eff,
    }


# ---------------------------------------------------------------------------
# Primal lattice construction (pinned -A^T convention)
# ---------------------------------------------------------------------------


def build_primal_lattice(A_scalar: list[list[int]], b_scalar: list[int], q: int) -> list[list[int]]:
    """Primal LWE lattice basis B (rows), pinned -A_scalarᵀ convention.

    Returns the (2·n_eff + 1) square integer matrix described in the
    module docstring. Lattice membership uses the row convention: a
    lattice point is z·B for an integer row vector z.
    """
    n = len(A_scalar)
    N = 2 * n + 1
    B = [[0] * N for _ in range(N)]
    # Block 1: q·I in the first n rows / first n cols
    for i in range(n):
        B[i][i] = q
    # Block 2: rows n..2n-1 = [ -A_scalarᵀ | I | 0 ]
    #   row (n+j) gets -A_scalar[:, j] in cols 0..n-1, and 1 at col n+j.
    for j in range(n):
        for i in range(n):
            B[n + j][i] = (-A_scalar[i][j])
        B[n + j][n + j] = 1
    # Block 3: last row = [ b_scalarᵀ | 0 | 1 ]
    for i in range(n):
        B[2 * n][i] = b_scalar[i] % q
    B[2 * n][2 * n] = 1
    return B


def target_vector(e_scalar: list[int], s_scalar: list[int]) -> list[int]:
    """v_target = (e_scalar, s_scalar, 1)."""
    return list(e_scalar) + list(s_scalar) + [1]


def recover_lattice_coeffs(
    A_scalar: list[list[int]],
    s_scalar: list[int],
    e_scalar: list[int],
    b_scalar: list[int],
    q: int,
) -> list[int]:
    """Integer coefficient vector z with z·B = v_target.

    By construction z = (m_0, s_scalar, 1) where
        m_0 = (e_scalar + A_scalar·s_scalar − b_scalar) / q   (exact integer).
    """
    n = len(A_scalar)
    m0 = [0] * n
    for r in range(n):
        acc = 0
        row = A_scalar[r]
        for c in range(n):
            acc += row[c] * s_scalar[c]
        num = e_scalar[r] + acc - b_scalar[r]
        assert num % q == 0, f"m_0 coordinate {r} not divisible by q"
        m0[r] = num // q
    return m0 + list(s_scalar) + [1]


def vec_mat_mul(z: list[int], B: list[list[int]]) -> list[int]:
    """z·B (row vector times matrix), exact integer arithmetic."""
    N = len(B)
    out = [0] * N
    for i in range(N):
        zi = z[i]
        if zi == 0:
            continue
        row = B[i]
        for c in range(N):
            out[c] += zi * row[c]
    return out


# ---------------------------------------------------------------------------
# Norms and the Gaussian heuristic
# ---------------------------------------------------------------------------


def l2_norm(v: list[int]) -> float:
    return math.sqrt(sum(x * x for x in v))


def log_det_primal(n_eff: int, q: int) -> float:
    """log(det B). B is block lower-triangular with diagonal blocks
    q·I_{n_eff}, I_{n_eff}, [1], so det = q^{n_eff}."""
    return n_eff * math.log(q)


def gaussian_heuristic(dim: int, log_det: float) -> float:
    """gh(Λ) = (det)^{1/dim} · sqrt(dim / (2πe)).

    Returned in the same length units as the basis (here, lattice
    coordinates). The shortest non-zero vector of a random lattice of
    this dimension and determinant is expected near this length.
    """
    log_gh = log_det / dim + 0.5 * (math.log(dim) - math.log(2 * math.pi * math.e))
    return math.exp(log_gh)


# ---------------------------------------------------------------------------
# Toy instance generation
# ---------------------------------------------------------------------------


def gen_toy_instance(
    seed: int = 20260527,
    q: int = TOY_Q,
    k: int = 7,
    eta: int = TOY_ETA,
    h_s: int | None = None,
    allow_spec_params: bool = False,
) -> dict:
    """Generate a synthetic toy Module-SLWE instance (A, s, e).

    - A: k×k matrix of uniform sedenions over 𝕊_q.
    - e: length-k sedenion vector; each of the 16k scalar coordinates is
      uniform in {−η, …, +η} (sparse-uniform noise, η = noise bound).
    - s: length-k sedenion vector whose 16k scalar form has exactly h_s
      nonzero coordinates, each ±1 (sparse ternary secret).

    h_s defaults to round(64 · k / 32) (proportional to the spec
    h_s = 64 at k = 32). At k = 7 this is h_s_toy = 14.

    NOT for spec parameters. The gate refuses q ≥ SPEC_Q or k ≥ SPEC_K
    unless allow_spec_params=True.
    """
    _check_not_spec(q, k, allow_spec_params)
    if h_s is None:
        h_s = round(64 * k / 32)
    rng = random.Random(seed)
    n_eff = k * DIM

    # A: uniform sedenions
    A = [[[rng.randrange(q) for _ in range(DIM)] for _ in range(k)] for _ in range(k)]

    # e: sparse-uniform in {-eta..eta}, stored as residues mod q
    e_scalar = [rng.randint(-eta, eta) for _ in range(n_eff)]
    e = [[e_scalar[i * DIM + d] % q for d in range(DIM)] for i in range(k)]

    # s: exactly h_s nonzero scalar coords, each ±1
    s_scalar = [0] * n_eff
    positions = rng.sample(range(n_eff), h_s)
    for pos in positions:
        s_scalar[pos] = rng.choice((-1, 1))
    s = [[s_scalar[i * DIM + d] % q for d in range(DIM)] for i in range(k)]

    return {
        "A": A, "s": s, "e": e,
        "s_scalar_signed": s_scalar,
        "e_scalar_signed": e_scalar,
        "q": q, "k": k, "eta": eta, "h_s": h_s, "n_eff": n_eff, "seed": seed,
    }


# ---------------------------------------------------------------------------
# Fano-projected basis (b) — CANDIDATE implementation (Brief 10.6 ratification)
# ---------------------------------------------------------------------------

_FANO_UNION_BASIS_CACHE: dict[int, list[list[int]]] = {}


def _fano_union_basis(q: int) -> list[list[int]]:
    """14 length-16 vectors over F_q spanning the F_L union (per D1, Brief 08).

    Re-derived in-module (no D1 import) to keep the lattice module self-contained.
    Cached per q. The union dimension is 14 at both q=911 and q=SPEC_Q (verified
    by op_2_58_2d_D1_fano_union_dimension).
    """
    if q in _FANO_UNION_BASIS_CACHE:
        return _FANO_UNION_BASIS_CACHE[q]
    from itertools import combinations as _comb
    from op_2252_v2_kernel_involution import lmm as _lmm, rref_kernel as _rrk

    def _kernel_vecs(a: int, b: int) -> list[list[int]]:
        x = add_vec(basis_vec(a), basis_vec(b + 8), q)
        return [[c % q for c in v] for v in _rrk(_lmm(x, q), q)]

    lines = set()
    for a, b in _comb(range(1, 8), 2):
        prod = mul_vec(basis_vec(a), basis_vec(b), q)
        nz = [i for i, v in enumerate(prod) if v % q != 0]
        lines.add(frozenset({a, b, nz[0]}))
    lines_sorted = sorted(tuple(sorted(L)) for L in lines)

    all_gens: list[list[int]] = []
    for (a, b, c) in lines_sorted:
        for (i, j) in [(a, b), (a, c), (b, c)]:
            all_gens.extend(_kernel_vecs(i, j))

    def _rank_q(cols: list[list[int]]) -> int:
        if not cols:
            return 0
        rows = [list(c) for c in cols]
        r = 0
        for c in range(DIM):
            piv = next((i for i in range(r, len(rows)) if rows[i][c] % q != 0), None)
            if piv is None:
                continue
            rows[r], rows[piv] = rows[piv], rows[r]
            inv = pow(rows[r][c], -1, q)
            rows[r] = [(x * inv) % q for x in rows[r]]
            for i in range(len(rows)):
                if i == r:
                    continue
                f = rows[i][c]
                if f != 0:
                    rows[i] = [(rows[i][x] - f * rows[r][x]) % q for x in range(DIM)]
            r += 1
        return r

    basis: list[list[int]] = []
    cur = 0
    for g in all_gens:
        if _rank_q(basis + [g]) > cur:
            basis.append(list(g))
            cur += 1
            if cur == 14:
                break
    assert cur == 14, f"F_L union basis at q={q} has rank {cur}, expected 14"
    _FANO_UNION_BASIS_CACHE[q] = basis
    return basis


def build_fano_projected_lattice(
    A_scalar: list[list[int]] | None = None,
    b_scalar: list[int] | None = None,
    q: int = TOY_Q,
    k: int = 7,
    allow_spec_params: bool = False,
) -> list[list[int]]:
    """Candidate basis (b) of §3.6 — F_L-restricted primal lattice.

    Replaces the n_eff = k·DIM rows of q·I_n on the e-side of basis (a) with
    14·k rows of form (q·v in block i, zeros elsewhere) where v ranges over the
    14-vector F_L union basis (D1, Brief 08). The s-side and Kannan rows are
    inherited unchanged from basis (a). Result is rectangular: (30k+1) × (32k+1)
    integer matrix; lattice rank 30k+1.

    POST-FREEZE / Brief-10.6 caveat: §3.6(b) admits several geometrically
    distinct readings of "Fano-projected." This implementation realises the
    F_L-restricted variant — the e-side quotient is generated by q·F_L per
    block instead of q·I_n. The Brief-10 primary run uses basis (a); basis (b)
    is included for orchestrator-level completeness and σ-statistic comparison.
    Whether this is the canonical reading is a Brief-10.6 design question.

    If called with no args (orchestrator construction-availability probe), runs
    a small toy probe to confirm the implementation works end-to-end.
    """
    if A_scalar is None:
        # Orchestrator probe path: build a tiny in-module toy basis to confirm
        # the implementation reaches a valid return without raising.
        inst = gen_toy_instance(k=k, q=q, allow_spec_params=allow_spec_params)
        lwe = build_scalar_lwe(inst["A"], inst["s"], inst["e"], q)
        A_scalar = lwe["A_scalar"]
        b_scalar = lwe["b_scalar"]
    _check_not_spec(q, k, allow_spec_params)
    n = len(A_scalar)
    assert n == k * DIM, f"A_scalar dim {n} != k*DIM = {k*DIM}"
    F = _fano_union_basis(q)
    N_cols = 2 * n + 1
    rows: list[list[int]] = []
    # 14k rows: q·F_L union basis per block.
    for i in range(k):
        for v in F:
            row = [0] * N_cols
            for d in range(DIM):
                row[i * DIM + d] = q * v[d]
            rows.append(row)
    # n s-side rows: [-A_scalarᵀ | I_n | 0]
    for j in range(n):
        row = [0] * N_cols
        for i in range(n):
            row[i] = -A_scalar[i][j]
        row[n + j] = 1
        rows.append(row)
    # Kannan row: [b | 0 | 1]
    row = [0] * N_cols
    for i in range(n):
        row[i] = b_scalar[i] % q
    row[2 * n] = 1
    rows.append(row)
    return rows


if __name__ == "__main__":
    inst = gen_toy_instance()
    lwe = build_scalar_lwe(inst["A"], inst["s"], inst["e"], inst["q"])
    print(f"toy instance: q={inst['q']} k={inst['k']} n_eff={lwe['n_eff']} h_s={inst['h_s']}")
    B = build_primal_lattice(lwe["A_scalar"], lwe["b_scalar"], inst["q"])
    print(f"lattice basis: {len(B)}×{len(B[0])} (N_lat = 2·n_eff = {2*lwe['n_eff']})")
    vt = target_vector(inst["e_scalar_signed"], inst["s_scalar_signed"])
    print(f"||v_target|| = {l2_norm(vt):.3f}")
    gh = gaussian_heuristic(2 * lwe["n_eff"] + 1, log_det_primal(lwe["n_eff"], inst["q"]))
    print(f"gh(B) = {gh:.3f}  → BDD holds: {l2_norm(vt) < gh}")
