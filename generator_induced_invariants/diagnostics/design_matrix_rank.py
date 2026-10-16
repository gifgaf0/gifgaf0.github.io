#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
design_matrix_rank.py -- a pre-standardization diagnostic for seed-generated public keys.

THE IDEA (see the companion note, sections 2 and 4)
---------------------------------------------------
Many public-key constructions build their public object by applying a *fixed family
of linear maps* to random seeds -- to compress a key, to inherit a symmetry, or to
support a reduction. ("Seeds" are the coefficients the generator consumes, after any
XOF expansion.) The public map M(seeds) is then linear in the seeds, and at instance
size k it factors as

        M_k  =  R_k . D_k

where R_k carries ALL the seed randomness and D_k is a FIXED "design matrix". Because
R_k only ever multiplies the fixed D_k, every row of every key lies in row(D_k):

        rank M_k  <=  rank D_k          for every draw of the seeds.

The factorization is not unique (R = M, D = identity always works), so a full-rank D
proves nothing unless it is MINIMAL: row(D_k) = W_k, the span of the rows of the
realizations at unit seeds. A ceiling found with any valid D is real; a pass needs the
minimal one. This tool checks D_k against the realizations: their rows must lie in
row(D_k), and at the sizes it can afford they must span it.

If rank D_k is below the number of columns b at the DEPLOYED size, a fixed vector of
ker D_k is annihilated by every key, which a matrix drawn from the distribution the
security argument assumes does not do (Corollary 1). If rank D_k is also below the
smaller dimension of M_k, every key is rank-deficient and noise recovery drops to an
LWE instance of dimension at most rank D_k (Corollary 2). Row space and kernel are the
only invariants the factorization transfers. Fixed invariant subspaces are another
matter: ML-KEM's multiplication maps share them and no attack exploits them; they are
a weakness only when the projected noise is far from uniform (the note's Remark 1),
which this tool does not test.

THE SATURATION RULE (why this hides)
------------------------------------
A rank check on a realized instance of dimension n can certify only rho >= n: a
full-rank result at n <= rho is exactly what a scheme with ceiling rho also produces.
In the built-in case (rho = 76) the realized object is full rank for every k <= 4
(n <= 64), identical to the controls, and first falls short at k = 5 (rank 72 of 80).
*A rank check run below the ceiling returns a clean result even for a broken scheme.*
This tool therefore takes its verdict from the design at the deployed size; the
empirical curve is a cross-check, not the verdict.

THE DIAGNOSTIC (note, section 4)
--------------------------------
  0. Count: rank D_k <= min(distinct rows, distinct columns of D_k). If that is below
     the number of columns at a deployed size, the scheme fails before any elimination.
  1. Factor: write the construction as M_k = R_k . D_k with D_k minimal
     (design_matrix(k) below).
  2. Build the design at each deployed size and, when the rows of D_k do not depend on k
     and the generator has finitely many images, the full design (full_design() below),
     which bounds every size at once.
  3. Compute rho = rank D_k EXACTLY over the working field F_q (q prime). When D has
     integer entries, also compute its rank over Q, which bounds every modulus.
  4. Confirm at the smallest size where rank D_k falls below the number of columns,
     against samples of the distribution the security argument assumes. A realized row
     outside row(D_k) contradicts Proposition 1: the factorization is wrong (ERROR).
  5. Flag a distinguisher when rho < b, and a ceiling when rho < min(a, b), at a
     deployed size; print the reduced dimension, at which the lattice estimate must be
     rerun (whether that is fatal depends on rho).

Passing is necessary for any security argument that assumes a full-rank (uniform)
matrix, and never sufficient. (The built-in SLWE case: even with the structure removed,
the scheme still failed on its parameters -- the modulus-to-noise ratio at the first
parameter set, hybrid attacks on its sparse secret at the second -- which this tool
does not judge.)

USE
---
  python3 -I design_matrix_rank.py --self-test                 regression test
  python3 -I design_matrix_rank.py                             built-in schemes
  python3 -I design_matrix_rank.py --plugin FILE.py:ClassName  your construction
A plugin subclasses GeneratorScheme; "from design_matrix_rank import GeneratorScheme"
works in the plugin file even under -I. Exit status: 0 if every verdict is PASS (or
the self-test passes), 1 if some verdict is FAIL, 2 on ERROR, on a self-test mismatch,
or on any unexpected exception.

SCOPE / ETHICS
--------------
A defensive evaluation tool. The built-in case study is the author's own withdrawn
sedenion Module-LWE proposal; the built-in controls are a sedenion module matrix with
independent uniform entries and an ML-KEM-shaped module lattice. The tool analyses the
structure of a construction you hand it; it is not an attack on any deployed system.

No third-party dependencies: pure-Python exact linear algebra over F_p and over Q.
Python 3.8 or later.

Author: M. Gifford, 2026. Companion to "Generator-induced invariants in lattice public
keys: a pre-standardization rank diagnostic"; reproduces the columns k <= 8 of Table 1
of that note and of "A rank collapse in a sedenion Module-LWE proposal, and why a
uniform matrix does not repair it" (Zenodo, 2026).
"""

from __future__ import annotations

import argparse
import importlib.util
import random
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Sequence, Tuple

IntMatrix = List[List[int]]
IntVec = List[int]


# --------------------------------------------------------------------------- #
# Exact linear algebra: rank over F_p, rank over Q, kernels. No floating point. #
# --------------------------------------------------------------------------- #
def is_prime(n: int) -> bool:
    """Miller-Rabin with the first twelve primes as bases (deterministic below 3.3e24)."""
    if n < 2:
        return False
    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for b in bases:
        if n % b == 0:
            return n == b
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for b in bases:
        x = pow(b, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def rank_mod_p(matrix: Sequence[Sequence[int]], p: int) -> int:
    """Exact rank of `matrix` over F_p, p prime (forward Gaussian elimination)."""
    rows = [[x % p for x in row] for row in matrix]
    rows = [r for r in rows if any(r)]
    if not rows:
        return 0
    nrows, ncols = len(rows), len(rows[0])
    rank = 0
    for col in range(ncols):
        piv = None
        for i in range(rank, nrows):
            if rows[i][col]:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        prow = rows[rank]
        inv = pow(prow[col], -1, p)  # modular inverse (Python 3.8+)
        if inv != 1:
            prow[col:] = [(x * inv) % p for x in prow[col:]]
        tail = prow[col:]
        for i in range(rank + 1, nrows):
            r = rows[i]
            f = r[col]
            if f:
                r[col:] = [(a - f * b) % p for a, b in zip(r[col:], tail)]
        rank += 1
        if rank == nrows:
            break
    return rank


def rank_over_Q(matrix: Sequence[Sequence[int]]) -> int:
    """Exact rank over Q of an integer matrix, by Bareiss fraction-free elimination.

    Every intermediate entry is a minor of the input, so each division is exact. Since
    reducing an integer matrix modulo p cannot raise its rank, the result bounds the
    rank over F_p for EVERY prime p at once."""
    rows = [list(row) for row in matrix if any(row)]
    if not rows:
        return 0
    nrows, ncols = len(rows), len(rows[0])
    rank, prev = 0, 1
    for col in range(ncols):
        piv = None
        for i in range(rank, nrows):
            if rows[i][col]:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        prow = rows[rank]
        pv = prow[col]
        tail = prow[col:]
        for i in range(rank + 1, nrows):
            r = rows[i]
            f = r[col]
            if f:
                r[col:] = [(pv * a - f * b) // prev for a, b in zip(r[col:], tail)]
            elif pv != prev:
                r[col:] = [(pv * a) // prev for a in r[col:]]
        prev = pv
        rank += 1
        if rank == nrows:
            break
    return rank


def kernel_mod_p(matrix: Sequence[Sequence[int]], p: int) -> List[IntVec]:
    """A basis of the right kernel {x : D x = 0} over F_p (reduced row echelon form)."""
    rows = [[x % p for x in row] for row in matrix]
    ncols = len(rows[0]) if rows else 0
    pivots: List[int] = []
    r = 0
    for col in range(ncols):
        piv = next((i for i in range(r, len(rows)) if rows[i][col]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][col], -1, p)
        rows[r] = [(x * inv) % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][col]:
                f = rows[i][col]
                rows[i] = [(a - f * b) % p for a, b in zip(rows[i], rows[r])]
        pivots.append(col)
        r += 1
        if r == len(rows):
            break
    pivot_set = set(pivots)
    basis = []
    for free in (c for c in range(ncols) if c not in pivot_set):
        x = [0] * ncols
        x[free] = 1
        for i, pc in enumerate(pivots):
            x[pc] = (-rows[i][free]) % p
        basis.append(x)
    return basis


def mat_vec_mod_p(M: Sequence[Sequence[int]], x: Sequence[int], p: int) -> IntVec:
    return [sum(a * b for a, b in zip(row, x)) % p for row in M]


def transpose(M: Sequence[Sequence[int]]) -> IntMatrix:
    return [list(c) for c in zip(*M)] if M else []


def _canon(vec: Sequence[int]):
    """Integer vector up to sign (first nonzero entry positive), or None for zero."""
    for x in vec:
        if x:
            return tuple(vec) if x > 0 else tuple(-t for t in vec)
    return None


def _canon_mod(vec: Sequence[int], p: int):
    """Vector over F_p up to a nonzero scalar (first nonzero entry 1), or None for zero."""
    for x in vec:
        if x % p:
            inv = pow(x % p, -1, p)
            return tuple((t * inv) % p for t in vec)
    return None


def distinct_rows(M: Sequence[Sequence[int]]) -> IntMatrix:
    """Nonzero rows of an integer matrix, repeats up to sign removed (row space unchanged)."""
    seen, out = set(), []
    for row in M:
        key = _canon(row)
        if key is not None and key not in seen:
            seen.add(key)
            out.append(list(key))
    return out


def distinct_rows_mod(M: Sequence[Sequence[int]], p: int) -> IntMatrix:
    """Nonzero rows over F_p, repeats up to a scalar removed (row space unchanged)."""
    seen, out = set(), []
    for row in M:
        key = _canon_mod(row, p)
        if key is not None and key not in seen:
            seen.add(key)
            out.append(list(key))
    return out


def compress(M: Sequence[Sequence[int]]) -> IntMatrix:
    """Drop zero and repeated (up to sign) rows and columns: rank is unchanged."""
    return transpose(distinct_rows(transpose(distinct_rows(M))))


def hstack(A: Sequence[Sequence[int]], B: Sequence[Sequence[int]]) -> IntMatrix:
    if len(A) != len(B):
        raise ValueError(f"hstack: {len(A)} rows against {len(B)}")
    return [list(a) + list(b) for a, b in zip(A, B)]


def block_diag(block: Sequence[Sequence[int]], copies: int) -> IntMatrix:
    h, w = len(block), len(block[0])
    out = [[0] * (w * copies) for _ in range(h * copies)]
    for t in range(copies):
        for i in range(h):
            out[h * t + i][w * t:w * (t + 1)] = list(block[i])
    return out


_RANK_CACHE: Dict[Tuple, int] = {}


def _cached_rank(M: IntMatrix, p: Optional[int]) -> int:
    """rank_mod_p (p given) or rank_over_Q (p None), memoized on the matrix's content."""
    key = (p, len(M), tuple(map(tuple, M)))
    if key not in _RANK_CACHE:
        _RANK_CACHE[key] = rank_over_Q(M) if p is None else rank_mod_p(M, p)
    return _RANK_CACHE[key]


# --------------------------------------------------------------------------- #
# The interface a construction implements.                                     #
# --------------------------------------------------------------------------- #
class GeneratorScheme(ABC):
    """Implement this for your own construction to run the diagnostic on it.

    Required: design_matrix(k), ambient_rank(k), realize(k, seeds, p), random_seeds(k, p, rng),
    and the class attribute parameter_sets = [(label, deployed size k, working prime q), ...].
    Optional: shape(k) for a non-square map, full_design(), reference_realize(k, p, rng),
    reference_kernel_check(x, p). realize() must be linear in the seeds.
    """

    name: str = "unnamed"
    block_dim: int = 1             # d: coordinates per module/algebra component
    parameter_sets: Sequence[Tuple[str, int, int]] = ()
    integer_design: bool = True    # D has integer entries, fixed independently of q
    reference_name: str = "uniform matrix over F_p"

    @abstractmethod
    def design_matrix(self, k: int) -> IntMatrix:
        """The MINIMAL design D_k at size k: row(D_k) is spanned by the rows of the realizations at
        unit seeds. Its columns are the columns of M_k; only its row space matters, so repeated rows
        may be dropped. A larger D still bounds the rank but can hide a ceiling."""

    @abstractmethod
    def ambient_rank(self, k: int) -> int:
        """Rank of a matrix of M_k's shape drawn from the assumed distribution (the smaller dimension)."""

    @abstractmethod
    def realize(self, k: int, seeds: Sequence[IntVec], p: int) -> IntMatrix:
        """The ACTUAL flattened public matrix M_k at size k, mod p; linear in the seeds."""

    @abstractmethod
    def random_seeds(self, k: int, p: int, rng: random.Random) -> List[IntVec]:
        """Fresh random seeds for one realization at size k."""

    def shape(self, k: int) -> Tuple[int, int]:
        """(rows a, columns b) of M_k. Override for a non-square map."""
        n = self.ambient_rank(k)
        return n, n

    def full_design(self) -> Optional[IntMatrix]:
        """If the rows of D_k do not depend on k and the generator has finitely many images: one
        design, with the same rows, whose columns contain those of every D_k. Otherwise None."""
        return None

    def reference_realize(self, k: int, p: int, rng: random.Random) -> IntMatrix:
        """A sample of the distribution the scheme's security argument assumes for M_k."""
        a, b = self.shape(k)
        return [[rng.randrange(p) for _ in range(b)] for _ in range(a)]

    def reference_kernel_check(self, x: IntVec, p: int) -> Optional[str]:
        """Optional: why a reference sample has M x != 0 except with negligible probability."""
        return None


def realization_span(scheme: GeneratorScheme, k: int, p: int) -> Tuple[IntMatrix, int]:
    """Distinct rows of the realizations at every unit seed, and the number of unit seeds.
    Their span is W_k, the row space of the minimal design."""
    template = scheme.random_seeds(k, p, random.Random(0))
    seen, rows, units = set(), [], 0
    for t, vec in enumerate(template):
        for m in range(len(vec)):
            seeds = [[0] * len(v) for v in template]
            seeds[t][m] = 1
            units += 1
            for row in scheme.realize(k, seeds, p):
                key = _canon_mod(row, p)
                if key is not None and key not in seen:
                    seen.add(key)
                    rows.append(list(key))
    return rows, units


def realize_is_linear(scheme: GeneratorScheme, k: int, p: int, rng: random.Random) -> bool:
    """M(s1 + s2) = M(s1) + M(s2) and M(c s1) = c M(s1) for random seeds and a random c."""
    s1, s2 = scheme.random_seeds(k, p, rng), scheme.random_seeds(k, p, rng)
    c = rng.randrange(2, p) if p > 2 else 1
    add = [[(x + y) % p for x, y in zip(u, v)] for u, v in zip(s1, s2)]
    scl = [[(c * x) % p for x in u] for u in s1]
    M1, M2 = scheme.realize(k, s1, p), scheme.realize(k, s2, p)
    MA, MS = scheme.realize(k, add, p), scheme.realize(k, scl, p)
    return (all((x + y - z) % p == 0 for r1, r2, ra in zip(M1, M2, MA) for x, y, z in zip(r1, r2, ra))
            and all((c * x - z) % p == 0 for r1, rs in zip(M1, MS) for x, z in zip(r1, rs)))


# --------------------------------------------------------------------------- #
# Sedenions: Cayley-Dickson doubling (reals -> ... -> sedenions) over Z.       #
#   (a,b)(c,d) = (ac - conj(d) b,  d a + b conj(c))      [the note's convention] #
# --------------------------------------------------------------------------- #
def _cd_conj(x: IntVec) -> IntVec:
    n = len(x)
    if n == 1:
        return [x[0]]
    h = n // 2
    return _cd_conj(x[:h]) + [-t for t in x[h:]]


def _cd_mul(x: IntVec, y: IntVec) -> IntVec:
    n = len(x)
    if n == 1:
        return [x[0] * y[0]]
    h = n // 2
    a, b, c, d = x[:h], x[h:], y[:h], y[h:]
    ac = _cd_mul(a, c)
    db = _cd_mul(_cd_conj(d), b)
    da = _cd_mul(d, a)
    bc = _cd_mul(b, _cd_conj(c))
    return [ac[i] - db[i] for i in range(h)] + [da[i] + bc[i] for i in range(h)]


def _cd_mul_alt(x: IntVec, y: IntVec) -> IntVec:
    """The other common convention, (a,b)(c,d) = (ac - d conj(b), conj(a) d + c b); self-test only.
    It defines the opposite algebra: _cd_mul_alt(x, y) = _cd_mul(y, x)."""
    n = len(x)
    if n == 1:
        return [x[0] * y[0]]
    h = n // 2
    a, b, c, d = x[:h], x[h:], y[:h], y[h:]
    ac = _cd_mul_alt(a, c)
    db = _cd_mul_alt(d, _cd_conj(b))
    ad = _cd_mul_alt(_cd_conj(a), d)
    cb = _cd_mul_alt(c, b)
    return [ac[i] - db[i] for i in range(h)] + [ad[i] + cb[i] for i in range(h)]


def _unit(dim: int, i: int) -> IntVec:
    v = [0] * dim
    v[i] = 1
    return v


def _basis_table(dim: int = 16, mul=_cd_mul) -> List[List[Tuple[int, int]]]:
    """e_a e_b = sign * e_index, read off the Cayley-Dickson product above."""
    table = []
    for a in range(dim):
        row = []
        for b in range(dim):
            prod = mul(_unit(dim, a), _unit(dim, b))
            idx = next(i for i, v in enumerate(prod) if v)
            row.append((prod[idx], idx))
        table.append(row)
    return table


SED = _basis_table(16)


def sed_left_matrix(w: Sequence[int], p: int) -> IntMatrix:
    """16x16 matrix of y -> w y over F_p: column c holds the coefficients of w e_c."""
    L = [[0] * 16 for _ in range(16)]
    for a, wa in enumerate(w):
        if wa:
            for c in range(16):
                s, i = SED[a][c]
                L[i][c] += s * wa
    return [[v % p for v in row] for row in L]


def sed_right_matrix(x: Sequence[int], p: int) -> IntMatrix:
    """16x16 matrix of a -> a x over F_p: column m holds the coefficients of e_m x."""
    R = [[0] * 16 for _ in range(16)]
    for m in range(16):
        for b, xb in enumerate(x):
            if xb:
                s, i = SED[m][b]
                R[i][m] += s * xb
    return [[v % p for v in row] for row in R]


def _sed_module_matrix(blocks: Sequence[Sequence[Sequence[int]]], p: int) -> IntMatrix:
    """Flatten a k x k matrix of sedenions (blocks[i][j]) into the 16k x 16k map s -> A s."""
    k = len(blocks)
    M = [[0] * (16 * k) for _ in range(16 * k)]
    for i in range(k):
        for j in range(k):
            L = sed_left_matrix(blocks[i][j], p)
            for u in range(16):
                M[16 * i + u][16 * j:16 * j + 16] = L[u]
    return M


def _uniform_sedenion_module(k: int, p: int, rng: random.Random) -> IntMatrix:
    return _sed_module_matrix([[[rng.randrange(p) for _ in range(16)] for _ in range(k)]
                               for _ in range(k)], p)


def _sedenion_reference_check(x: IntVec, p: int) -> Optional[str]:
    """Corollary 1 against independent uniform sedenion entries: block row i of M x is
    sum_j A_ij x_j; if a -> a x_j is invertible for some j, that sum is uniform, so the
    block row vanishes with probability p^-16, independently over the block rows."""
    k = len(x) // 16
    for j in range(k):
        xj = x[16 * j:16 * j + 16]
        if any(xj) and rank_mod_p(sed_right_matrix(xj, p), p) == 16:
            return (f"right multiplication by block {j} of x is invertible over F_{p}, so a "
                    f"reference sample has M x = 0 with probability p^-{16 * k}")
    return None


# --------------------------------------------------------------------------- #
# Built-in case study: the sedenion Module-LWE ("SLWE") Singer-orbit scheme.    #
# --------------------------------------------------------------------------- #
class SLWEScheme(GeneratorScheme):
    """
    Public matrix A_ij = sigma^j(seed_i), sigma an order-7 coordinate permutation (the
    'Singer cycle') on the sedenions: it fixes e0 and e8 and maps e_t -> e_(t+1) for
    t = 1..6, e_7 -> e_1, and likewise e_9..e_15. The flattening s |-> A s factors as
    M_k = (S (x) I_16) . N_k, where N_k (256 x 16k) takes its column block j from the
    fixed 256x112 matrix N, N_{16m+u, 16j+c} = coefficient u of sigma^j(e_m) . e_c.
    rank N = 76 over Q, so rank M_k <= 76 at every k and every modulus. Version 1 of the
    scheme specified q ~ 2^32 with q = 1 (mod 455); the negative-result note instantiates it
    with the least such prime, 4294977961.
    """

    name = "SLWE (sedenion Module-LWE, Singer-orbit public matrix)"
    block_dim = 16
    parameter_sets = (("version 1: k = 32, q = 4294977961 (instantiating q ~ 2^32)", 32, 4294977961),
                      ("version 2: k = 64, q = 911", 64, 911))
    reference_name = "independent uniform sedenion entries"

    def __init__(self) -> None:
        perm = list(range(16))
        for t in range(1, 8):
            perm[t] = (t % 7) + 1          # e_t -> e_{(t mod 7)+1}
            perm[t + 8] = (t % 7) + 9      # e_{t+8} -> e_{(t mod 7)+9}
        self.perm = perm                    # perm[t] = index of sigma(e_t)
        self._pows = {0: list(range(16))}
        self._N: Optional[IntMatrix] = None

    def sigma_pow(self, j: int) -> List[int]:
        """Index permutation of sigma^j (j taken mod 7, since sigma^7 = id)."""
        j %= 7
        if j not in self._pows:
            prev = self.sigma_pow(j - 1)
            self._pows[j] = [self.perm[prev[t]] for t in range(16)]
        return self._pows[j]

    def sigma_apply(self, vec: Sequence[int], j: int) -> IntVec:
        P = self.sigma_pow(j)
        out = [0] * 16
        for t in range(16):
            out[P[t]] = vec[t]
        return out

    def full_design(self, table: Optional[List[List[Tuple[int, int]]]] = None) -> IntMatrix:
        """N (256 x 112); `table` swaps in another multiplication table (self-test only)."""
        if table is None and self._N is not None:
            return [row[:] for row in self._N]
        tab = SED if table is None else table
        N = [[0] * 112 for _ in range(256)]
        for m in range(16):
            for j in range(7):
                img = self.sigma_pow(j)[m]               # sigma^j(e_m) = e_img
                for c in range(16):
                    s, u = tab[img][c]                   # e_img e_c = s e_u
                    N[16 * m + u][16 * j + c] = s
        if table is None:
            self._N = N
        return [row[:] for row in N]

    def design_matrix(self, k: int) -> IntMatrix:
        N = SLWEScheme.full_design(self)
        return [[row[16 * (j % 7) + c] for j in range(k) for c in range(16)] for row in N]

    def ambient_rank(self, k: int) -> int:
        return 16 * k

    def realize(self, k: int, seeds: Sequence[IntVec], p: int) -> IntMatrix:
        return _sed_module_matrix([[self.sigma_apply(seeds[i], j) for j in range(k)]
                                   for i in range(k)], p)

    def random_seeds(self, k: int, p: int, rng: random.Random) -> List[IntVec]:
        return [[rng.randrange(p) for _ in range(16)] for _ in range(k)]

    def reference_realize(self, k: int, p: int, rng: random.Random) -> IntMatrix:
        return _uniform_sedenion_module(k, p, rng)

    def reference_kernel_check(self, x: IntVec, p: int) -> Optional[str]:
        return _sedenion_reference_check(x, p)


# --------------------------------------------------------------------------- #
# Passing controls. Their designs are full rank by construction (independent    #
# blocks); RowSeededGenericScheme with enough seed length is a non-trivial one.  #
# --------------------------------------------------------------------------- #
class SedenionModuleControl(GeneratorScheme):
    """A_ij independent uniform sedenions: the 'repair' of the note's Section 3.5 and the
    distribution the SLWE reduction assumed. M_k = R_k . D_k with D_k block-diagonal: one
    copy per block column of the sedenion structure-constant table T (rows (m,u), columns c,
    T = coefficient u of e_m e_c), whose distinct rows are the 16 unit vectors."""

    name = "Control: sedenion module, independent uniform entries"
    block_dim = 16
    parameter_sets = SLWEScheme.parameter_sets
    reference_name = "the same distribution"

    def __init__(self) -> None:
        T = [[0] * 16 for _ in range(256)]
        for m in range(16):
            for c in range(16):
                s, u = SED[m][c]
                T[16 * m + u][c] = s
        self.T = distinct_rows(T)          # 16 x 16: same row space as T

    def design_matrix(self, k: int) -> IntMatrix:
        return block_diag(self.T, k)

    def ambient_rank(self, k: int) -> int:
        return 16 * k

    def realize(self, k: int, seeds: Sequence[IntVec], p: int) -> IntMatrix:
        return _sed_module_matrix([[seeds[k * i + j] for j in range(k)] for i in range(k)], p)

    def random_seeds(self, k: int, p: int, rng: random.Random) -> List[IntVec]:
        return [[rng.randrange(p) for _ in range(16)] for _ in range(k * k)]

    def reference_realize(self, k: int, p: int, rng: random.Random) -> IntMatrix:
        return _uniform_sedenion_module(k, p, rng)

    def reference_kernel_check(self, x: IntVec, p: int) -> Optional[str]:
        return _sedenion_reference_check(x, p)


class RingModuleControl(GeneratorScheme):
    """The ML-KEM shape (FIPS 203): a k x k matrix of independent uniform elements of
    Z_q[X]/(X^n + 1), every block its own coefficients. The design for one block column is
    the negacyclic structure-constant table (rows (m,u), columns c, entry = coefficient u of
    X^m X^c), whose distinct rows are the n unit vectors; D_k is k copies of it."""

    block_dim = 256
    reference_name = "the same distribution"

    def __init__(self, n: int = 256, q: int = 3329, sizes: Sequence[int] = (2, 3, 4)) -> None:
        self.n = n
        self.block_dim = n
        self.name = (f"Control: ML-KEM-shaped module over Z_{q}[X]/(X^{n}+1), "
                     f"independent uniform blocks")
        self.parameter_sets = tuple((f"k = {k}, n = {n}, q = {q}", k, q) for k in sizes)
        keys = set()
        for m in range(n):
            for u in range(n):
                keys.add((u - m) % n)      # X^m X^c = +-X^u exactly when c = u - m mod n
        self.T = [_unit(n, c) for c in sorted(keys)]   # distinct rows of the n^2 x n table

    def design_matrix(self, k: int) -> IntMatrix:
        return block_diag(self.T, k)

    def ambient_rank(self, k: int) -> int:
        return self.n * k

    def _block(self, a: Sequence[int], p: int) -> IntMatrix:
        n = self.n
        B = [[0] * n for _ in range(n)]
        for m in range(n):
            if a[m]:
                for c in range(n):
                    u = m + c
                    if u < n:
                        B[u][c] = a[m] % p
                    else:
                        B[u - n][c] = (-a[m]) % p
        return B

    def realize(self, k: int, seeds: Sequence[IntVec], p: int) -> IntMatrix:
        n = self.n
        M = [[0] * (n * k) for _ in range(n * k)]
        for i in range(k):
            for j in range(k):
                B = self._block(seeds[k * i + j], p)
                for u in range(n):
                    M[n * i + u][n * j:n * j + n] = B[u]
        return M

    def random_seeds(self, k: int, p: int, rng: random.Random) -> List[IntVec]:
        return [[rng.randrange(p) for _ in range(self.n)] for _ in range(k * k)]

    def reference_realize(self, k: int, p: int, rng: random.Random) -> IntMatrix:
        return self.realize(k, self.random_seeds(k, p, rng), p)


class RowSeededGenericScheme(GeneratorScheme):
    """Block row i = sum_m seed_i[m] G_m (j-th column block taken from G's block j mod r):
    one seed of length ell per block row, d x d blocks, r distinct column blocks. D has
    ell*d rows and r*d columns, so rank M_k <= min(ell*d, r*d) whatever G is: it passes
    when both counts reach the number of columns, and fails otherwise."""

    def __init__(self, d: int, ell: int, r: int, deployed_k: int, q: int = 911,
                 seed: int = 99) -> None:
        self.d, self.ell, self.r = d, ell, r
        self.block_dim = d
        self.name = f"Row-seeded generic design (d={d}, seed length {ell}, {r} images)"
        self.parameter_sets = ((f"k = {deployed_k}, q = {q}", deployed_k, q),)
        rng = random.Random(seed)
        self.G = [[rng.randrange(-3, 4) for _ in range(r * d)] for _ in range(ell * d)]

    def design_matrix(self, k: int) -> IntMatrix:
        d, r = self.d, self.r
        return [[row[d * (j % r) + c] for j in range(k) for c in range(d)] for row in self.G]

    def ambient_rank(self, k: int) -> int:
        return self.d * k

    def realize(self, k: int, seeds: Sequence[IntVec], p: int) -> IntMatrix:
        d = self.d
        Dk = self.design_matrix(k)
        M = []
        for i in range(k):
            for u in range(d):
                row = [0] * (d * k)
                for m in range(self.ell):
                    s = seeds[i][m]
                    if s:
                        g = Dk[d * m + u]
                        row = [(a + s * b) % p for a, b in zip(row, g)]
                M.append(row)
        return M

    def random_seeds(self, k: int, p: int, rng: random.Random) -> List[IntVec]:
        return [[rng.randrange(p) for _ in range(self.ell)] for _ in range(k)]


# --------------------------------------------------------------------------- #
# Inputs the tool must catch (self-test regressions).                          #
# --------------------------------------------------------------------------- #
class InconsistentScheme(GeneratorScheme):
    """A design that does not contain the realizations (the error the first version's
    uniform control made: a fixed 16x16 identity 'design' for a uniform 16k x 16k matrix)."""

    name = "Must be rejected: design does not contain the realizations"
    block_dim = 4
    parameter_sets = (("k = 4, q = 911", 4, 911),)

    def design_matrix(self, k: int) -> IntMatrix:
        return [[1 if c == u else 0 for c in range(4 * k)] for u in range(4)]   # rank 4 only

    def ambient_rank(self, k: int) -> int:
        return 4 * k

    def realize(self, k: int, seeds: Sequence[IntVec], p: int) -> IntMatrix:
        return [[x % p for x in row] for row in seeds]                         # uniform

    def random_seeds(self, k: int, p: int, rng: random.Random) -> List[IntVec]:
        return [[rng.randrange(p) for _ in range(4 * k)] for _ in range(4 * k)]


class IdentityDesignSLWE(SLWEScheme):
    """SLWE's realization with the identity as its 'design': a valid factorization (R = M), so
    Proposition 1 holds, but not the minimal one -- it would hide the ceiling of 76."""

    name = "Must be rejected: SLWE realization with a non-minimal (identity) design"
    parameter_sets = (("k = 5, q = 911", 5, 911),)

    def design_matrix(self, k: int) -> IntMatrix:
        return [[1 if c == r else 0 for c in range(16 * k)] for r in range(16 * k)]

    def full_design(self, table=None):
        return None


class PermutedDesignSLWE(SLWEScheme):
    """N_k with its columns reversed: the right rank, the wrong row space."""

    name = "Must be rejected: SLWE design with the right rank and the wrong row space"
    parameter_sets = (("k = 5, q = 911", 5, 911),)

    def design_matrix(self, k: int) -> IntMatrix:
        return [row[::-1] for row in SLWEScheme.design_matrix(self, k)]

    def full_design(self, table=None):
        return None


class TruncatedFullDesignSLWE(SLWEScheme):
    """A 'full design' with fewer rows than D_k, so it cannot contain D_k's columns."""

    name = "Must be rejected: full design with fewer rows than the design"
    parameter_sets = (("k = 5, q = 911", 5, 911),)

    def full_design(self, table=None):
        return SLWEScheme.full_design(self)[:76]


class WideScheme(GeneratorScheme):
    """M(s) = sum_m s_m A_m G with G a fixed 48 x 64 matrix: a 32 x 64 map whose keys have full
    row rank 32, yet all share a fixed 16-dimensional kernel (Corollary 1 needs only rho < b)."""

    name = "Must fail: wide 32 x 64 map with a 48-dimensional design"
    parameter_sets = (("a = 32, b = 64, q = 911", 1, 911),)

    def __init__(self) -> None:
        rng = random.Random(5)
        self.G = [[rng.randrange(-3, 4) for _ in range(64)] for _ in range(48)]
        A = [[[rng.randrange(-3, 4) for _ in range(48)] for _ in range(32)] for _ in range(4)]
        self.C = [[[sum(Am[i][t] * self.G[t][j] for t in range(48)) for j in range(64)]
                   for i in range(32)] for Am in A]

    def design_matrix(self, k: int) -> IntMatrix:
        return [row[:] for row in self.G]

    def shape(self, k: int) -> Tuple[int, int]:
        return 32, 64

    def ambient_rank(self, k: int) -> int:
        return 32

    def realize(self, k: int, seeds: Sequence[IntVec], p: int) -> IntMatrix:
        s = seeds[0]
        return [[sum(s[m] * self.C[m][i][j] for m in range(4)) % p for j in range(64)]
                for i in range(32)]

    def random_seeds(self, k: int, p: int, rng: random.Random) -> List[IntVec]:
        return [[rng.randrange(p) for _ in range(4)]]


# --------------------------------------------------------------------------- #
# The driver.                                                                  #
# --------------------------------------------------------------------------- #
def diagnose(scheme: GeneratorScheme, max_k: int = 8, seed_sets: int = 3, seed: int = 12345,
             extra_primes: Sequence[int] = (), max_dim: int = 256, check_budget: int = 4_000_000,
             quiet: bool = False) -> dict:
    """Steps 0, 3, 4 and 5 on the designs the scheme supplies (steps 1 and 2): print a report and
    return the findings. The verdict is taken at each deployed size; the design is checked against
    the realizations at every size the curve realizes, and for minimality where affordable."""
    say = (lambda *a, **k: None) if quiet else print
    rng = random.Random(seed)
    res: dict = {"name": scheme.name, "psets": [], "curve": [], "errors": [], "k_confirm": None,
                 "kernel_test": None, "full_design": None, "minimality": [], "empirical": []}
    psets = list(scheme.parameter_sets)
    say("=" * 78)
    say(" DESIGN-MATRIX RANK DIAGNOSTIC")
    say(f" scheme: {scheme.name}")
    say("=" * 78)

    def stop(msg: str) -> dict:
        res["errors"].append(msg)
        res["verdict"] = "ERROR"
        say(f"\n[5] VERDICT\n    *** ERROR -- {msg} ***")
        say("=" * 78 + "\n")
        return res

    if not psets:
        return stop("no parameter_sets declared: the verdict is taken at the deployed size")
    composite = [q for _, _, q in psets if not is_prime(q)] + [p for p in extra_primes if not is_prime(p)]
    if composite:
        return stop(f"modulus {composite} is not prime: the tool does linear algebra over the field "
                     f"F_p (for an integer design, the rank over Q still bounds the rank modulo any prime)")

    # [0] count and [3] exact rank at each deployed size.
    say("\n[0] Count, and [3] exact rank of the design at each deployed size")
    for label, kd, q in psets:
        D = scheme.design_matrix(kd)
        a, b = scheme.shape(kd)
        if not D or len(D[0]) != b:
            return stop(f"design_matrix({kd}) has {len(D[0]) if D else 0} columns; M_k has {b}")
        g = len(distinct_rows(D))
        c = len(distinct_rows(transpose(D)))
        Dc = compress(D)
        rho = _cached_rank(Dc, q)
        rho_Q = _cached_rank(Dc, None) if scheme.integer_design else None
        extra = {p: _cached_rank(Dc, p) for p in extra_primes}
        entry = {"label": label, "k": kd, "q": q, "a": a, "b": b, "ambient": min(a, b), "rows": g,
                 "cols": c, "count_bound": min(g, c), "rho": rho, "rho_Q": rho_Q, "extra": extra,
                 "kernel": rho < b, "ceiling": rho < min(a, b)}
        res["psets"].append(entry)
        say(f"    {label}")
        say(f"      M_k is {a} x {b}; D_k is {len(D)} x {b}, with {g} distinct rows and {c} distinct "
            f"columns (up to sign) -> rank D_k <= {min(g, c)}"
            + ("   FAILS BY COUNTING ALONE" if min(g, c) < b else ""))
        line = f"      rank D_k over F_{q} = {rho}"
        if rho_Q is not None:
            line += f";  over Q = {rho_Q} (bounds every modulus)"
        say(line)
        for p, r in extra.items():
            say(f"      rank D_k over F_{p} = {r}   (cross-check)")
        if rho < b:
            say(f"      -> a fixed kernel of dimension {b - rho} is shared by every key (Corollary 1)")
        if rho < min(a, b):
            say(f"      -> CEILING: rank M_k <= {rho} < {min(a, b)} for every seed draw; recovery in "
                f"dimension <= {rho} (Corollary 2)")
        elif rho < b:
            say(f"      -> no rank ceiling (rho >= {min(a, b)} rows), but the fixed kernel distinguishes")
        else:
            say(f"      -> no ceiling: rank D_k = {rho} = number of columns")

    # [2] the full design, if the scheme supplies one.
    F = scheme.full_design()
    if F is not None:
        for _, kd, _ in psets:
            if len(F) != len(scheme.design_matrix(kd)):
                return stop(f"full_design() has {len(F)} rows but design_matrix({kd}) has "
                            f"{len(scheme.design_matrix(kd))}: they must share rows (Proposition 2)")
        Fc = compress(F)
        rhoF = {q: _cached_rank(Fc, q) for _, _, q in psets}
        rhoF_Q = _cached_rank(Fc, None) if scheme.integer_design else None
        hyp = {kd: _cached_rank(compress(hstack(F, scheme.design_matrix(kd))), q) == rhoF[q]
               for _, kd, q in psets}
        res["full_design"] = {"shape": (len(F), len(F[0])), "rho": rhoF, "rho_Q": rhoF_Q, "hyp": hyp}
        say(f"\n[2] Full design (every generator image): {len(F)} x {len(F[0])}")
        for q, r in rhoF.items():
            say(f"      rank over F_{q} = {r}")
        say("      col(D_k) inside col(full design) [Proposition 2's hypothesis] at k = "
            + ", ".join(f"{k}: {'yes' if ok else 'NO'}" for k, ok in hyp.items()))
        if all(hyp.values()):
            bound = rhoF_Q if rhoF_Q is not None else max(rhoF.values())
            say(f"      -> rank M_k <= {bound} at every size k"
                + (" and every modulus (rank over Q)" if rhoF_Q is not None else ""))
        else:
            say("      -> hypothesis fails: the full design bounds no size beyond those checked")

    # [4] empirical curve, consistency and minimality (cross-checks; the verdict comes from [0]/[3]).
    p0 = min(q for _, _, q in psets)
    failing = any(e["kernel"] for e in res["psets"])
    rankD: Dict[int, int] = {}

    def rank_D(k: int) -> int:
        if k not in rankD:
            rankD[k] = _cached_rank(compress(scheme.design_matrix(k)), p0)
        return rankD[k]

    k_conf = None
    if failing:
        for k in range(1, max(e["k"] for e in res["psets"]) + 1):
            if scheme.shape(k)[1] > rank_D(k):
                k_conf = k
                break
    res["k_confirm"] = k_conf
    ks: List[int] = []
    k = 1
    while k <= max_k and max(scheme.shape(k)) <= max_dim:
        ks.append(k)
        k += 1
    if k_conf is not None and k_conf not in ks and max(scheme.shape(k_conf)) <= max_dim:
        ks += list(range(ks[-1] + 1 if ks else 1, k_conf + 1))
    say(f"\n[4] Empirical rank over F_{p0} vs the assumed distribution ({scheme.reference_name}), "
        f"{seed_sets} seed set(s):")
    say(f"      {'k':>3} {'shape':>11} {'rank D_k':>9} {'assumed':>8} "
        + " ".join(f"{'seeds' + str(s + 1):>7}" for s in range(seed_sets)))
    realized_at: Dict[int, List[IntMatrix]] = {}
    for k in ks:
        a, b = scheme.shape(k)
        amb, rD = min(a, b), rank_D(k)
        ref = rank_mod_p(scheme.reference_realize(k, p0, random.Random(777 + k)), p0)
        mats = [scheme.realize(k, scheme.random_seeds(k, p0, rng), p0) for _ in range(seed_sets)]
        realized = [rank_mod_p(M, p0) for M in mats]
        if k == k_conf:
            realized_at[k] = mats
        res["curve"].append((k, (a, b), rD, ref, realized))
        outside = False
        if rD < b:   # rows of every key must lie in row(D_k) (automatic when D_k has full column rank)
            Dk_rows = distinct_rows_mod([[x % p0 for x in row] for row in scheme.design_matrix(k)], p0)
            outside = any(rank_mod_p(Dk_rows + [list(r) for r in M], p0) != rD for M in mats)
        if outside or any(r > rD for r in realized):
            res["errors"].append(f"at k = {k} a realized row lies outside row(D_k): Proposition 1 "
                                 f"forbids this, so design_matrix(k) does not describe realize(k)")
            flag = "  <-- INCONSISTENT"
        elif min(realized) < amb:
            flag = "  <-- deficient"
            if seed_sets >= 2 and max(realized) < amb and rD >= amb:
                res["empirical"].append(k)
                flag = "  <-- deficient beyond the design"
        elif failing:
            flag = "  <-- full rank here: the deficiency is invisible to a rank check at this size"
        else:
            flag = ""
        say(f"      {k:>3} {f'{a}x{b}':>11} {rD:>9} {ref:>8} " + " ".join(f"{r:>7}" for r in realized)
            + flag)
    if failing and k_conf is not None and k_conf not in ks:
        say(f"      (confirmation needs size k = {k_conf}, dimension {max(scheme.shape(k_conf))} > "
            f"--max-dim {max_dim}; the verdict rests on the exact design rank)")

    # Linearity and minimality: does row(D_k) equal the span of the realizations at unit seeds?
    def units(k: int) -> int:
        return sum(len(v) for v in scheme.random_seeds(k, p0, random.Random(0)))

    affordable = [k for k in ks if units(k) * scheme.shape(k)[0] * scheme.shape(k)[1] <= check_budget]
    check_ks = sorted({1} | ({k_conf} if k_conf in affordable else set())
                      | ({max(affordable)} if affordable else set()))
    say(f"\n    Design vs realizations at unit seeds (minimality, Section 2.1), k = {check_ks}:")
    for k in check_ks:
        if not realize_is_linear(scheme, k, p0, random.Random(seed + k)):
            res["errors"].append(f"realize() is not linear in the seeds at k = {k}")
            say(f"      k = {k}: realize() is NOT linear in the seeds")
            continue
        W, n_units = realization_span(scheme, k, p0)
        dimW, rD, b = rank_mod_p(W, p0), rank_D(k), scheme.shape(k)[1]
        Dk_rows = distinct_rows_mod([[x % p0 for x in row] for row in scheme.design_matrix(k)], p0)
        contained = rD == b or rank_mod_p(Dk_rows + W, p0) == rD
        res["minimality"].append({"k": k, "dimW": dimW, "rank_D": rD, "contained": contained})
        verdict = ("minimal" if contained and dimW == rD else
                   "NOT contained in row(D_k)" if not contained else "NOT minimal")
        say(f"      k = {k}: {n_units} unit seeds span {dimW} dimensions; rank D_k = {rD} -> {verdict}")
        if not contained:
            res["errors"].append(f"at k = {k} the realizations leave row(D_k): the design is invalid")
        elif dimW < rD:
            res["errors"].append(f"design_matrix({k}) is not minimal: rank D_k = {rD} but the realizations "
                                 f"span only {dimW}; a pass would be meaningless (Section 2.1)")

    # Corollary 1 at the confirmation size: a fixed kernel vector of D_k vs the assumed distribution.
    if k_conf is not None and k_conf in realized_at:
        basis = kernel_mod_p(distinct_rows(scheme.design_matrix(k_conf)), p0)
        if basis:
            krng = random.Random(seed + 1)
            x = [0] * len(basis[0])
            for v in basis:
                cf = krng.randrange(1, p0)
                x = [(a + cf * b) % p0 for a, b in zip(x, v)]
            hits = sum(1 for M in realized_at[k_conf] if not any(mat_vec_mod_p(M, x, p0)))
            refs = [scheme.reference_realize(k_conf, p0, random.Random(4242 + t)) for t in range(seed_sets)]
            ref_hits = sum(1 for M in refs if not any(mat_vec_mod_p(M, x, p0)))
            why = scheme.reference_kernel_check(x, p0)
            res["kernel_test"] = {"k": k_conf, "dim_ker": len(basis), "keys": hits,
                                  "reference": ref_hits, "n": seed_sets, "why": why}
            say(f"\n    Corollary 1 at k = {k_conf}: dim ker D_k = {len(basis)}; a fixed x in ker D_k gives "
                f"M x = 0 for {hits}/{seed_sets} keys and {ref_hits}/{seed_sets} samples of the "
                f"assumed distribution")
            if why:
                say(f"    ({why})")
            if hits < seed_sets:
                res["errors"].append(f"a key at k = {k_conf} has M x != 0 for x in ker D_k")

    # [5] verdict.
    say("\n[5] VERDICT")
    if res["errors"]:
        res["verdict"] = "ERROR"
        say("    *** ERROR -- the design does not describe the construction. ***")
        for e in res["errors"]:
            say(f"    {e}")
    elif failing:
        res["verdict"] = "FAIL"
        say("    *** FAIL -- generator-induced invariant at a deployed size. ***")
        for e in res["psets"]:
            if e["kernel"]:
                kind = (f"ceiling: rank M_k <= {e['rho']} < {e['ambient']}" if e["ceiling"]
                        else "fixed kernel only (keys can have full row rank)")
                say(f"    {e['label']}: rank D_k = {e['rho']} < {e['b']} columns -- {kind}")
        say("    Consequences (note, Corollaries 1 and 2):")
        say("      - a fixed x in ker D_k has M x = 0 for every key, which a sample of the assumed")
        say(f"        distribution ({scheme.reference_name}) does not;")
        ceilings = [e["rho"] for e in res["psets"] if e["ceiling"]]
        if ceilings:
            say(f"      - noise recovery is an LWE instance of dimension at most {min(ceilings)}: rerun the")
            say("        lattice estimate there (whether that is fatal depends on rho and the parameters);")
        say("      - no amount of seed entropy repairs this (R only ever multiplies the fixed D).")
        say("    Removing the structure clears THIS flag only; check the parameters separately.")
    elif res["empirical"]:
        res["verdict"] = "FAIL"
        say(f"    *** FAIL -- every seed set is rank-deficient at k = {res['empirical']}, although the "
            f"design is full rank there. ***")
        say("    The keys are deficient beyond what the design explains; Corollary 2 applies with the")
        say("    realized rank. A larger deployed size may or may not inherit this: check it directly.")
    else:
        res["verdict"] = "PASS"
        say("    PASS -- rank D_k equals the number of columns at every deployed size; the design")
        say(f"    contains the realizations at every size tested and is minimal at k = {check_ks}.")
        say("    At the deployed sizes the verdict relies on design_matrix(k) being minimal there too.")
        say("    Necessary for a security argument that assumes a full-rank (uniform) matrix, not")
        say("    sufficient: invariant subspaces whose projected noise is far from uniform (note,")
        say("    Remark 1) and the lattice estimate itself need their own checks.")
    say("=" * 78 + "\n")
    return res


# --------------------------------------------------------------------------- #
# Self-test: the note's Table 1 and every computational fact it cites.         #
# --------------------------------------------------------------------------- #
def self_test() -> int:
    failures: List[str] = []

    def check(ok: bool, text: str) -> None:
        print(f"    [{'ok' if ok else 'MISMATCH'}] {text}")
        if not ok:
            failures.append(text)

    print("[self-test] the note's Table 1 and the facts it cites ...")
    s = SLWEScheme()
    N = s.full_design()
    q1 = 4294977961
    check(len(N) == 256 and len(N[0]) == 112, "design matrix N is 256 x 112")
    ranks = {p: rank_mod_p(N, p) for p in (911, 2731, 2147483647, q1)}
    rQ = rank_over_Q(N)
    check(rQ == 76 and all(r == 76 for r in ranks.values()),
          f"rank N = 76 over Q (exact, fraction-free) and over F_911, F_2731, F_(2^31-1), F_q "
          f"[got Q:{rQ}, {sorted(set(ranks.values()))}]")
    check(all(is_prime(p) and p % 455 == 1 for p in (911, 2731, q1))
          and not any(is_prime(x) for x in range(2 ** 32 + 1, q1) if x % 455 == 1),
          "911, 2731 and q = 4294977961 are prime and = 1 (mod 455); q is the least such prime above 2^32")
    g, c = len(distinct_rows(N)), len(distinct_rows(transpose(N)))
    check(c == 112 and min(g, c) == 112,
          f"counting: N has {g} distinct rows and {c} distinct columns, so rank M <= 112 before any elimination")

    # Table 1, k <= 8, over F_911: realized ranks equal rank N_k (Proposition 1 is tight).
    expected = [16, 32, 48, 64, 72, 74, 76, 76]
    rng = random.Random(2026)
    design = [rank_mod_p(compress(s.design_matrix(k)), 911) for k in range(1, 9)]
    realized = [[rank_mod_p(s.realize(k, s.random_seeds(k, 911, rng), 911), 911) for _ in range(3)]
                for k in range(1, 9)]
    check(design == expected, f"rank N_k, k = 1..8: {design}")
    alt_table = _basis_table(16, _cd_mul_alt)
    opposite = all(alt_table[a][b] == SED[b][a] for a in range(16) for b in range(16))
    N_alt = s.full_design(alt_table)
    alt_k = [rank_mod_p(compress([[row[16 * (j % 7) + cc] for j in range(k) for cc in range(16)]
                                  for row in N_alt]), 911) for k in range(1, 9)]
    check(opposite and rank_over_Q(N_alt) == 76 and alt_k == expected,
          f"other Cayley-Dickson convention: the opposite algebra; rank N = 76 over Q, rank N_k = {alt_k}")
    check(all(all(r == e for r in rr) for rr, e in zip(realized, expected)),
          f"Table 1, Singer orbit, k = 1..8 over F_911 (3 seed sets each): {[rr[0] for rr in realized]} "
          f"= rank N_k, not min(16k, 76)")
    ctrl = SedenionModuleControl()
    uni = [rank_mod_p(ctrl.realize(k, ctrl.random_seeds(k, 911, rng), 911), 911) for k in range(1, 9)]
    check(uni == [16 * k for k in range(1, 9)],
          f"Table 1, independent uniform sedenion entries, k = 1..8 over F_911: {uni}")

    # 76 = 16 + 6 x 10: discrete Fourier transform over the power index j (F_911 has 7th roots of 1).
    p = 911
    w = next(pow(h, (p - 1) // 7, p) for h in range(2, p) if pow(h, (p - 1) // 7, p) != 1)
    parts = []
    for t in range(7):
        om = pow(w, t, p)
        Nh = [[sum(pow(om, j, p) * row[16 * j + cc] for j in range(7)) % p for cc in range(16)]
              for row in N]
        parts.append(rank_mod_p(Nh, p))
    check(parts == [16] + [10] * 6, f"76 = 16 + 6 x 10 over F_911 (characters of <sigma>): {parts}")

    # sigma is not an automorphism, nor a collineation of the Fano plane as the product labels it.
    P = s.perm
    bad = sum(1 for a in range(16) for b in range(16)
              if (SED[a][b][0], P[SED[a][b][1]]) != SED[P[a]][P[b]])
    check(bad == 144, f"sigma breaks sigma(xy) = sigma(x)sigma(y) on {bad} of 256 basis products")
    lines = {frozenset((a, b, SED[a][b][1])) for a in range(1, 8) for b in range(1, 8) if a != b}
    image = frozenset(P[t] for t in (1, 2, 3))
    check(len(lines) == 7 and frozenset((1, 2, 3)) in lines and image not in lines,
          f"octonion lines {sorted(sorted(l) for l in lines)}; sigma maps {{1,2,3}} to "
          f"{sorted(image)}, not a line")

    # Corollary 1 against the distribution the reduction assumed.
    basis = kernel_mod_p(distinct_rows(s.design_matrix(8)), 911)
    krng = random.Random(7)
    x = [0] * 128
    for v in basis:
        cf = krng.randrange(1, 911)
        x = [(a + cf * b) % 911 for a, b in zip(x, v)]
    keys = sum(1 for _ in range(3)
               if not any(mat_vec_mod_p(s.realize(8, s.random_seeds(8, 911, rng), 911), x, 911)))
    refs = sum(1 for t in range(3)
               if not any(mat_vec_mod_p(_uniform_sedenion_module(8, 911, random.Random(t)), x, 911)))
    why = _sedenion_reference_check(x, 911)
    check(len(basis) == 52 and keys == 3 and refs == 0 and why is not None,
          f"Corollary 1: x in ker N_8 (dim {len(basis)}) gives M x = 0 for {keys}/3 Singer keys and "
          f"{refs}/3 uniform-sedenion samples; {why or 'NO invertible block'}")

    # Verdicts.
    def verdict(sc: GeneratorScheme, **kw) -> dict:
        return diagnose(sc, quiet=True, **kw)

    r = verdict(SLWEScheme(), max_k=5, seed_sets=1)
    check(r["verdict"] == "FAIL" and [e["rho"] for e in r["psets"]] == [76, 76]
          and [e["count_bound"] for e in r["psets"]] == [112, 112] and r["k_confirm"] == 5
          and all(m["contained"] and m["dimW"] == m["rank_D"] for m in r["minimality"]),
          "verdict SLWE: FAIL at both parameter sets (rank D_k = 76; count bound 112; first visible at "
          "k = 5); design minimal at the sizes checked")
    r = verdict(SedenionModuleControl(), max_k=4, seed_sets=1)
    check(r["verdict"] == "PASS" and [e["rho"] for e in r["psets"]] == [512, 1024],
          "verdict control, independent uniform sedenion entries: PASS (rank D_k = 512, 1024)")
    ring = RingModuleControl()
    full = [rank_mod_p(compress(ring.design_matrix(k)), 3329) for k in (2, 3, 4)]
    r = verdict(RingModuleControl(n=16, sizes=(2, 3, 4)), max_k=4, seed_sets=1)
    check(full == [512, 768, 1024] and r["verdict"] == "PASS",
          f"verdict control, ML-KEM shape: rank D_k = {full} at n = 256, q = 3329; PASS (pipeline at n = 16)")
    r = verdict(RowSeededGenericScheme(d=4, ell=16, r=8, deployed_k=8), max_k=8, seed_sets=2)
    check(r["verdict"] == "PASS" and r["psets"][0]["rho"] == 32,
          "verdict, row-seeded design with seed length 16 and 8 images (64 x 32, rank 32): PASS")
    r = verdict(RowSeededGenericScheme(d=2, ell=8, r=3, deployed_k=8), max_k=8, seed_sets=1)
    check(r["verdict"] == "FAIL" and r["psets"][0]["rho"] == 6,
          "verdict, full-rank 16 x 6 design reused with period 3: FAIL (rank 6 < 16)")
    r = verdict(RowSeededGenericScheme(d=4, ell=4, r=7, deployed_k=8), max_k=8, seed_sets=1)
    check(r["verdict"] == "FAIL" and r["psets"][0]["count_bound"] == 16,
          "verdict, one length-4 seed per block row: FAIL by counting (16 design rows < 32)")
    r = verdict(WideScheme(), max_k=1, seed_sets=2)
    check(r["verdict"] == "FAIL" and r["psets"][0]["kernel"] and not r["psets"][0]["ceiling"]
          and r["psets"][0]["rho"] == 48,
          "verdict, wide 32 x 64 map with a rank-48 design: FAIL by its fixed kernel, no rank ceiling")
    r = verdict(InconsistentScheme(), max_k=4, seed_sets=1)
    check(r["verdict"] == "ERROR", "verdict, design that does not contain the realizations: ERROR")
    r = verdict(IdentityDesignSLWE(), max_k=5, seed_sets=1)
    check(r["verdict"] == "ERROR" and any("not minimal" in e for e in r["errors"]),
          "verdict, SLWE realization with the identity as design (valid, not minimal): ERROR")
    r = verdict(PermutedDesignSLWE(), max_k=5, seed_sets=1)
    check(r["verdict"] == "ERROR", "verdict, design with the right rank and the wrong row space: ERROR")
    r = verdict(TruncatedFullDesignSLWE(), max_k=5, seed_sets=1)
    check(r["verdict"] == "ERROR", "verdict, full design with fewer rows than the design: ERROR")
    r = verdict(RowSeededGenericScheme(d=2, ell=8, r=3, deployed_k=8, q=8192), max_k=8, seed_sets=1)
    check(r["verdict"] == "ERROR", "verdict, composite working modulus 8192: ERROR, not a crash")

    print("[self-test] " + ("PASS" if not failures else f"FAIL ({len(failures)} mismatch(es))") + "\n")
    return 0 if not failures else 2


# --------------------------------------------------------------------------- #
def _load_plugin(spec: str) -> GeneratorScheme:
    path, _, cls = spec.rpartition(":")
    if not path or not cls:
        raise SystemExit("--plugin expects FILE.py:ClassName")
    sys.modules.setdefault("design_matrix_rank", sys.modules[__name__])  # importable under -I
    loader_spec = importlib.util.spec_from_file_location("user_scheme", path)
    if loader_spec is None or loader_spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    module = importlib.util.module_from_spec(loader_spec)
    loader_spec.loader.exec_module(module)
    return getattr(module, cls)()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Design-matrix rank diagnostic for seed-generated public keys.")
    ap.add_argument("--self-test", action="store_true",
                    help="reproduce the note's Table 1 and the facts it cites, check the verdicts, exit")
    ap.add_argument("--scheme", choices=["slwe", "sedenion-control", "ring-control", "all"],
                    default="all", help="built-in scheme(s) to diagnose (default: all)")
    ap.add_argument("--plugin", metavar="FILE.py:CLASS",
                    help="diagnose your own GeneratorScheme subclass instead")
    ap.add_argument("--max-k", type=int, default=8, help="largest size in the empirical curve (default 8)")
    ap.add_argument("--max-dim", type=int, default=256,
                    help="largest realized dimension in the curve (default 256; pure Python is slow above)")
    ap.add_argument("--seed-sets", type=int, default=3, help="seed sets per size (default 3)")
    ap.add_argument("--primes", default="", help="extra primes for a cross-check of rank D_k, comma-separated")
    args = ap.parse_args(argv)

    try:
        if args.self_test:
            return self_test()
        extra = [int(t) for t in args.primes.split(",") if t.strip()]
        if args.plugin:
            schemes = [_load_plugin(args.plugin)]
        else:
            schemes = []
            if args.scheme in ("slwe", "all"):
                schemes.append(SLWEScheme())
            if args.scheme in ("sedenion-control", "all"):
                schemes.append(SedenionModuleControl())
            if args.scheme in ("ring-control", "all"):
                schemes.append(RingModuleControl())
        worst = 0
        for sc in schemes:
            v = diagnose(sc, max_k=args.max_k, seed_sets=args.seed_sets, extra_primes=extra,
                         max_dim=args.max_dim)["verdict"]
            worst = max(worst, {"PASS": 0, "FAIL": 1, "ERROR": 2}[v])
        return worst
    except Exception as exc:  # any crash is an ERROR (exit 2), never a FAIL (exit 1)
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
