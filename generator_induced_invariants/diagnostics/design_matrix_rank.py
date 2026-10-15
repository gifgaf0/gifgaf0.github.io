#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
design_matrix_rank.py -- a pre-standardization diagnostic for seed-generated public keys.

THE IDEA (see the companion outline, sections 2 and 4)
------------------------------------------------------
Many public-key constructions build their public object by applying a *fixed family
of linear maps* to random seeds -- to compress a key, to inherit a symmetry, or to
support a reduction. Whenever they do, the flattened public object factors as

        M  =  R . D

where R carries ALL the seed randomness and D is a single FIXED "design matrix"
whose entries are the coordinates of the generator's images. Because R only ever
multiplies the fixed D, no amount of seed entropy can push M outside the image of D:

        rank M  <=  rank D          for every instance size.

If rank D is below the ambient dimension, the public key is distinguishable from
random and key recovery drops to a problem of dimension rank(D), not the ambient
dimension. The rank ceiling is the cheapest and most lethal of D's invariants;
common left annihilators and fixed invariant subspaces are the same phenomenon.

THE SATURATION RULE (why this hides)
------------------------------------
If the generator contributes only c independent images, then for instances with
fewer than c columns the generated object is GENERICALLY FULL RANK and looks exactly
like a uniform control. The ceiling only separates once the instance is large enough
to exhaust the generator. *A rank check run below saturation returns a clean result
even for a broken scheme.* This tool therefore refuses to certify from a sub-saturation
check and reproduces the saturation curve explicitly.

THE DIAGNOSTIC
--------------
  1. Rewrite the construction as M = R.D; isolate the fixed design matrix D.
  2. Count c = independent generator images (columns of D); note the saturation size.
  3. Compute rank D EXACTLY over the real field F_q (not floating point), and compare
     against ambient at an instance size ABOVE saturation.
  4. Cross-check against a uniform control of identical shape.
  5. Flag a ceiling (distinguisher + dimension-reduced recovery) or a nontrivial common
     invariant subspace.

Necessary, not sufficient: passing this means only that THIS class of weakness is
absent. (The built-in SLWE case: even with the structure removed, the scheme still
failed on its modulus-to-noise ratio -- a separate matter this tool does not judge.)

SCOPE / ETHICS
--------------
A defensive evaluation tool. The built-in case study is the author's own withdrawn
sedenion Module-LWE proposal. The tool analyses the structure of a public-key
construction you hand it; it is not an attack on any deployed system.

No third-party dependencies required (pure-Python exact linear algebra over F_p).

Author: M. Gifford, 2026. Reproduces Table 1 of "A rank collapse in a sedenion
Module-LWE proposal, and why a uniform matrix does not repair it" (Zenodo, 2026).
"""

from __future__ import annotations

import argparse
import random
import sys
from abc import ABC, abstractmethod
from typing import List, Sequence

IntMatrix = List[List[int]]
IntVec = List[int]


# --------------------------------------------------------------------------- #
# Exact rank over a prime field F_p (Gaussian elimination, no floating point).  #
# --------------------------------------------------------------------------- #
def rank_mod_p(matrix: Sequence[Sequence[int]], p: int) -> int:
    """Exact rank of `matrix` over F_p. O(rows * cols^2)."""
    M = [[x % p for x in row] for row in matrix]
    if not M:
        return 0
    nrows, ncols = len(M), len(M[0])
    rank = 0
    prow = 0
    for col in range(ncols):
        piv = next((r for r in range(prow, nrows) if M[r][col] % p != 0), None)
        if piv is None:
            continue
        M[prow], M[piv] = M[piv], M[prow]
        inv = pow(M[prow][col], -1, p)  # modular inverse; needs gcd(pivot, p)=1
        M[prow] = [(x * inv) % p for x in M[prow]]
        prow_vals = M[prow]
        for r in range(nrows):
            if r != prow:
                f = M[r][col] % p
                if f:
                    M[r] = [(M[r][i] - f * prow_vals[i]) % p for i in range(ncols)]
        prow += 1
        rank += 1
        if prow == nrows:
            break
    return rank


def q_rank_by_multiprime(matrix: Sequence[Sequence[int]], primes: Sequence[int]) -> int:
    """Rank over Q equals max rank over F_p across primes (bad primes only lower it)."""
    return max(rank_mod_p(matrix, p) for p in primes)


# --------------------------------------------------------------------------- #
# A pluggable interface for any seed-generated construction.                   #
# --------------------------------------------------------------------------- #
class GeneratorScheme(ABC):
    """Implement this for your own construction to run the diagnostic on it."""

    name: str = "unnamed"
    block_dim: int = 1  # d: coordinates per module/algebra component

    @abstractmethod
    def design_matrix(self) -> IntMatrix:
        """The FIXED design matrix D (integer entries). rank D caps rank M for all k."""

    @abstractmethod
    def ambient_rank(self, k: int) -> int:
        """Full rank a uniform control would have at instance size k (e.g. block_dim*k)."""

    @abstractmethod
    def realize(self, k: int, seeds: Sequence[IntVec], p: int) -> IntMatrix:
        """Build the ACTUAL flattened public matrix M at instance size k, mod p."""

    @abstractmethod
    def random_seeds(self, k: int, p: int, rng: random.Random) -> List[IntVec]:
        """Fresh random seeds for one realization at instance size k."""

    def design_full_rank(self) -> int:
        """Full rank the design matrix could have (min of its two dimensions)."""
        D = self.design_matrix()
        return min(len(D), len(D[0])) if D and D[0] else 0


# --------------------------------------------------------------------------- #
# Cayley-Dickson algebra (reals -> ... -> sedenions) over the integers.        #
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
    first = [ac[i] - db[i] for i in range(h)]
    second = [da[i] + bc[i] for i in range(h)]
    return first + second


def _unit(dim: int, i: int) -> IntVec:
    v = [0] * dim
    v[i] = 1
    return v


# --------------------------------------------------------------------------- #
# Built-in case study: the sedenion Module-LWE ("SLWE") Singer-orbit scheme.    #
# --------------------------------------------------------------------------- #
class SLWEScheme(GeneratorScheme):
    """
    Public matrix A_{ij} = sigma^j(seed_i), sigma an order-7 coordinate permutation
    (the 'Singer cycle') on the 16-dim sedenion algebra. The flattening s |-> A s
    factors as M = (S (x) I_16) . N with N the fixed 256x112 design matrix
        N_{16m+u, 16j+c} = coefficient u of  sigma^j(e_m) . e_c .
    rank N = 76 over Q and over every prime tried, so rank A <= 76 for every k.
    Reproduces Table 1 of the Zenodo note.
    """

    name = "SLWE (sedenion Module-LWE, Singer-orbit public matrix)"
    block_dim = 16

    def __init__(self) -> None:
        # sigma: fixes e0,e8; 7-cycles (1..7) and (9..15). perm[t] = index of sigma(e_t).
        perm = list(range(16))
        for t in range(1, 8):
            perm[t] = (t % 7) + 1          # e_t -> e_{(t mod 7)+1}
        for t in range(1, 8):
            perm[t + 8] = (t % 7) + 9      # e_{t+8} -> e_{(t mod 7)+9}
        self.perm = perm                    # order-7 permutation of the 16 coordinates
        self._sigma_pow_cache = {0: list(range(16))}

    def _sigma_pow_perm(self, j: int) -> List[int]:
        """Index permutation of sigma^j (j taken mod 7, since sigma^7 = id)."""
        j %= 7
        if j in self._sigma_pow_cache:
            return self._sigma_pow_cache[j]
        prev = self._sigma_pow_perm(j - 1)
        cur = [self.perm[prev[t]] for t in range(16)]  # apply sigma once more
        self._sigma_pow_cache[j] = cur
        return cur

    def _sigma_pow_apply(self, vec: IntVec, j: int) -> IntVec:
        """Apply sigma^j to a coefficient vector: (sigma v)[perm[t]] = v[t]."""
        P = self._sigma_pow_perm(j)
        out = [0] * 16
        for t in range(16):
            out[P[t]] = vec[t]
        return out

    def design_matrix(self) -> IntMatrix:
        d = self.block_dim
        N = [[0] * (7 * d) for _ in range(d * d)]  # 256 x 112
        for m in range(d):
            for j in range(7):
                img = self._sigma_pow_perm(j)[m]       # sigma^j(e_m) = e_{img}
                for c in range(d):
                    prod = _cd_mul(_unit(d, img), _unit(d, c))  # +/- unit vector
                    for u in range(d):
                        if prod[u]:
                            N[d * m + u][d * j + c] = prod[u]
        return N

    def ambient_rank(self, k: int) -> int:
        return self.block_dim * k

    def realize(self, k: int, seeds: Sequence[IntVec], p: int) -> IntMatrix:
        d = self.block_dim
        M = [[0] * (d * k) for _ in range(d * k)]
        for i in range(k):
            for j in range(k):
                w = self._sigma_pow_apply(seeds[i], j)  # sigma^j(seed_i)
                for c in range(d):
                    prod = _cd_mul(w, _unit(d, c))       # (sigma^j seed_i) . e_c
                    for u in range(d):
                        v = prod[u] % p
                        if v:
                            M[d * i + u][d * j + c] = v
        return M

    def random_seeds(self, k: int, p: int, rng: random.Random) -> List[IntVec]:
        return [[rng.randrange(p) for _ in range(self.block_dim)] for _ in range(k)]


# --------------------------------------------------------------------------- #
# A PASSING control: a genuinely uniform construction (design matrix = I).      #
#   M = R directly, no fixed generator gadget, so D is full rank and nothing    #
#   collapses. Demonstrates the diagnostic distinguishes sound from broken.     #
# --------------------------------------------------------------------------- #
class UniformControlScheme(GeneratorScheme):
    name = "Uniform control (no generator; full-rank design)"
    block_dim = 16

    def design_matrix(self) -> IntMatrix:
        d = self.block_dim
        return [[1 if i == j else 0 for j in range(d)] for i in range(d)]  # I_16, rank 16

    def ambient_rank(self, k: int) -> int:
        return self.block_dim * k

    def realize(self, k: int, seeds: Sequence[IntVec], p: int) -> IntMatrix:
        n = self.block_dim * k
        rng = random.Random(0xC0FFEE + k)
        return [[rng.randrange(p) for _ in range(n)] for _ in range(n)]

    def random_seeds(self, k: int, p: int, rng: random.Random) -> List[IntVec]:
        return [[rng.randrange(p) for _ in range(self.block_dim)] for _ in range(k)]

    def design_full_rank(self) -> int:
        return self.block_dim


# --------------------------------------------------------------------------- #
# The driver: run the diagnostic on a scheme and print a report.               #
# --------------------------------------------------------------------------- #
DEFAULT_PRIMES = [911, 2731, 2147483647, 4294977961]  # F_911, F_2731, 2^31-1, the note's q


def _saturation_k(scheme: GeneratorScheme, rho: int) -> int:
    """Smallest instance size k at which a uniform control's rank exceeds the ceiling."""
    k = 1
    while scheme.ambient_rank(k) <= rho and k < 10_000:
        k += 1
    return k


def diagnose(scheme: GeneratorScheme, primes=DEFAULT_PRIMES, max_k=8, seed_sets=3,
             seed=12345) -> dict:
    rng = random.Random(seed)
    D = scheme.design_matrix()
    d_rows, d_cols = len(D), (len(D[0]) if D else 0)
    ranks = {p: rank_mod_p(D, p) for p in primes}
    rho = max(ranks.values())
    d_full = scheme.design_full_rank()
    sat_k = _saturation_k(scheme, rho)

    print("=" * 74)
    print(f" DESIGN-MATRIX RANK DIAGNOSTIC")
    print(f" scheme: {scheme.name}")
    print("=" * 74)

    # 1. The fixed design matrix D and its rank over several characteristics.
    print(f"\n[1] Fixed design matrix D : {d_rows} x {d_cols}  (block_dim d = {scheme.block_dim})")
    print(f"    rank D by characteristic (exact):")
    for p in primes:
        print(f"        over F_{p:<12} : rank = {ranks[p]}")
    char_indep = len(set(ranks.values())) == 1
    print(f"    rank over Q (multi-prime) : {rho}")
    print(f"    -> rank D is {'CHARACTERISTIC-INDEPENDENT' if char_indep else 'characteristic-DEPENDENT'}"
          f" at the primes tried.")
    print(f"    design-matrix full rank would be min({d_rows},{d_cols}) = {d_full};"
          f"  ceiling rho = {rho}.")

    ceiling = rho < d_full
    print(f"\n[2] Ceiling:  rank M <= rho = {rho}  for EVERY instance size k  "
          f"(M = R.D, R only multiplies the fixed D).")
    print(f"    Saturation: a uniform control reaches rank {rho} at k = "
          f"{sat_k - 1 if sat_k>1 else 1}..{sat_k}; any empirical check at k < {sat_k} "
          f"cannot reveal the ceiling.")

    # 3. Empirical saturation curve: realized scheme vs uniform control.
    print(f"\n[3] Empirical rank vs a uniform control (over F_{primes[0]}, {seed_sets} seed sets):")
    header = f"      {'k':>3} {'ambient':>8} {'uniform':>8} " + \
             " ".join(f"{'seedset'+str(s+1):>9}" for s in range(seed_sets))
    print(header)
    curve = []
    for k in range(1, max_k + 1):
        amb = scheme.ambient_rank(k)
        uni = rank_mod_p(scheme.realize(k, scheme.random_seeds(k, primes[0], random.Random(999)),
                                        primes[0]), primes[0]) \
            if isinstance(scheme, UniformControlScheme) else \
            rank_mod_p(_uniform_matrix(amb, primes[0], random.Random(777 + k)), primes[0])
        realized = []
        for s in range(seed_sets):
            seeds = scheme.random_seeds(k, primes[0], rng)
            realized.append(rank_mod_p(scheme.realize(k, seeds, primes[0]), primes[0]))
        curve.append((k, amb, uni, realized))
        flag = "  <-- below ceiling, collapse invisible" if amb <= rho else \
               ("  <-- COLLAPSE" if realized and realized[0] < amb else "")
        print(f"      {k:>3} {amb:>8} {uni:>8} " +
              " ".join(f"{r:>9}" for r in realized) + flag)

    # 4. Verdict.
    print(f"\n[4] VERDICT")
    if ceiling:
        worst_k = max_k
        amb = scheme.ambient_rank(worst_k)
        print(f"    *** FAIL -- generator-induced rank ceiling detected. ***")
        print(f"    rank M is capped at {rho} regardless of k, against ambient {scheme.block_dim}*k "
              f"(= {amb} at k={worst_k}).")
        print(f"    Consequences:")
        print(f"      - the public key is DISTINGUISHABLE from uniform by an exact-rank / linear test;")
        print(f"      - key/noise recovery reduces to a problem of dimension {rho}, not the ambient "
              f"dimension;")
        print(f"      - NO amount of seed entropy repairs this (R only ever multiplies the fixed D).")
        print(f"    Necessary-not-sufficient: removing the structure clears THIS flag only; re-check "
              f"parameters (modulus/noise) separately.")
    else:
        print(f"    PASS -- design matrix is full rank ({rho} = min dim); no generator-induced rank "
              f"ceiling.")
        print(f"    (Necessary, not sufficient: other structural invariants and the lattice/parameter "
              f"estimate still require their own checks.)")
    print("=" * 74 + "\n")

    return {"rank_by_prime": ranks, "rho": rho, "design_full_rank": d_full,
            "ceiling": ceiling, "saturation_k": sat_k, "curve": curve,
            "char_independent": char_indep}


def _uniform_matrix(n: int, p: int, rng: random.Random) -> IntMatrix:
    return [[rng.randrange(p) for _ in range(n)] for _ in range(n)]


# --------------------------------------------------------------------------- #
# Self-test: reproduce Table 1 of the note and the rank-76 ceiling.            #
# --------------------------------------------------------------------------- #
def self_test() -> int:
    print("[self-test] reproducing the Zenodo note's Table 1 ...")
    s = SLWEScheme()
    N = s.design_matrix()
    assert len(N) == 256 and len(N[0]) == 112, f"design matrix shape {len(N)}x{len(N[0])} != 256x112"
    for p in (911, 2731, 2147483647, 4294977961):
        r = rank_mod_p(N, p)
        assert r == 76, f"rank N over F_{p} = {r}, expected 76"
    print("            rank N = 76 over F_911, F_2731, F_(2^31-1), F_q  [ok]")

    # Table 1 (Singer): k=1..8 -> 16,32,48,64,72,74,76,76 ; uniform -> 16k.
    expected = {1: 16, 2: 32, 3: 48, 4: 64, 5: 72, 6: 74, 7: 76, 8: 76}
    rng = random.Random(2026)
    for k, exp in expected.items():
        # three seed sets must all agree with the table (generic seeds)
        for _ in range(3):
            seeds = s.random_seeds(k, 911, rng)
            r = rank_mod_p(s.realize(k, seeds, 911), 911)
            assert r == exp, f"realized rank at k={k} = {r}, expected {exp}"
    print("            realized ranks k=1..8 = 16,32,48,64,72,74,76,76  (3 seed sets) [ok]")

    # Uniform control is full rank.
    uni = rank_mod_p(_uniform_matrix(80, 911, random.Random(5)), 911)
    assert uni == 80, f"uniform 80x80 rank {uni} != 80"
    print("            uniform control full rank                         [ok]")
    print("[self-test] PASS\n")
    return 0


# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Design-matrix rank diagnostic for seed-generated public keys.")
    ap.add_argument("--self-test", action="store_true",
                    help="reproduce the note's Table 1 and the rank-76 ceiling, then exit")
    ap.add_argument("--scheme", choices=["slwe", "control", "both"], default="both",
                    help="which built-in scheme(s) to diagnose (default: both)")
    ap.add_argument("--max-k", type=int, default=8,
                    help="largest instance size for the empirical curve (default 8; "
                         ">16 is slow in pure Python)")
    ap.add_argument("--seed-sets", type=int, default=3, help="random seed sets per k (default 3)")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    schemes = []
    if args.scheme in ("slwe", "both"):
        schemes.append(SLWEScheme())
    if args.scheme in ("control", "both"):
        schemes.append(UniformControlScheme())
    for sc in schemes:
        diagnose(sc, max_k=args.max_k, seed_sets=args.seed_sets)
    return 0


if __name__ == "__main__":
    sys.exit(main())
