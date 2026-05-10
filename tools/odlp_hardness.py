"""Empirical sedenion ODLP hardness probe (Brief 04, OP-D).

The sedenion ``h = g^n`` discrete-log problem is a *finite-commutative-
algebra* DLP: powers of a single sedenion element ``g`` lie in
``F_p[g] = F_p[X]/m_g(X)``, where ``m_g`` is its minimal polynomial of
degree at most DIM = 16. The unit group of ``F_p[g]`` factors via
the Chinese remainder theorem according to the irreducible
factorisation of ``m_g``; for irreducible ``m_g`` of degree ``d``,
``F_p[g] ≅ F_{p^d}`` and the DLP reduces to the classical DLP in
``F_{p^d}^*`` of order ``p^d − 1``.

Pohlig-Hellman therefore succeeds quickly whenever ``p^d − 1`` factors
into small primes (whatever ``d`` happens to be for the random ``g``
under attack). Mod-455 primes have ``p − 1`` divisible by ``5·7·13``
by construction, so the smoothness of low-``d`` cases is expected;
this script measures it directly.

What the script does, per Brief 04 §1:

1. For each test prime ``p ∈ {911, 8191, 11831, 14561, 16381}``:
   a. Compute and factor ``p^d − 1`` for ``d ∈ {1, 2, 4, 8}``.
   b. Pick a random sedenion ``g`` whose powers stay in the
      ``d``-dim sub-algebra ``F_p[e_1]^d`` (i.e., ``g ∈ F_p · 1
      + F_p · e_1`` for ``d = 2``); sample a random exponent ``n``;
      compute ``h = g^n`` via square-and-multiply.
   c. Apply Pohlig-Hellman to ``(g, h)`` using the factored order.
   d. Record wall-clock time and success.

Stop condition (per brief): if PH succeeds in well under a second
at every prime, document and stop without running Task 2 (index
calculus).
"""

from __future__ import annotations

import math
import os
import random
import sys
import time
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sedenion_Fp import mul_vec, basis_vec, DIM   # noqa: E402

TEST_PRIMES = [911, 8191, 11831, 14561, 16381]


# ---------------------------------------------------------------------------
# Sedenion exponentiation (power-associative, square-and-multiply)
# ---------------------------------------------------------------------------


def sedenion_pow(g: list[int], n: int, p: int) -> list[int]:
    if n == 0:
        return basis_vec(0)
    if n == 1:
        return list(g)
    result = basis_vec(0)
    base = list(g)
    while n > 0:
        if n & 1:
            result = mul_vec(result, base, p)
        n >>= 1
        if n:
            base = mul_vec(base, base, p)
    return result


# ---------------------------------------------------------------------------
# Integer factorisation (Miller-Rabin + Pollard rho)
# ---------------------------------------------------------------------------


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _pollard_rho(n: int, rng: random.Random,
                 deadline: float | None = None) -> int | None:
    if n % 2 == 0:
        return 2
    while True:
        if deadline is not None and time.monotonic() > deadline:
            return None
        x = rng.randrange(2, n - 1)
        y = x
        c = rng.randrange(1, n - 1)
        d = 1
        steps = 0
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
            steps += 1
            if deadline is not None and (steps & 0xff) == 0 \
                    and time.monotonic() > deadline:
                return None
        if d != n:
            return d


def factorise(n: int, *, seed: int = 0xd1f,
              deadline: float | None = None) -> dict[int, int]:
    """Full integer factorisation. Trial division to 10 000, then Pollard rho.

    If ``deadline`` (a ``time.monotonic()`` value) is passed and we don't
    finish in time, the partial factorisation is returned with a sentinel
    composite key set to the unfactored remainder. Use
    ``factorise_completed`` to detect this case.
    """
    if n <= 1:
        return {}
    rng = random.Random(seed)
    factors: dict[int, int] = {}
    # Trial division.
    d = 2
    while d <= 10_000 and d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            factors[d] = e
        d += 1
    # Recursive Pollard rho on the remainder.
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if deadline is not None and time.monotonic() > deadline:
            # Bail out, leaving the unfactored remainder under a special key.
            factors[-1] = m
            for other in stack:
                factors[-1] = factors.get(-1, 1) * other
            break
        if is_prime(m):
            factors[m] = factors.get(m, 0) + 1
            continue
        f = _pollard_rho(m, rng, deadline=deadline)
        if f is None:
            factors[-1] = m
            for other in stack:
                factors[-1] = factors.get(-1, 1) * other
            break
        stack.append(f)
        stack.append(m // f)
    return factors


def factorise_completed(facs: dict[int, int]) -> bool:
    return -1 not in facs


def largest_prime_factor(facs: dict[int, int]) -> int:
    return max(facs) if facs else 1


# ---------------------------------------------------------------------------
# Pohlig-Hellman in a finite cyclic group (group ops abstracted)
# ---------------------------------------------------------------------------


def _bsgs(power, op, identity, g, h, order: int) -> Optional[int]:
    """Baby-step giant-step.

    ``power(g, n)`` computes g^n; ``op(a, b)`` is the group multiplication;
    ``identity`` is e. Returns ``n`` with ``power(g, n) == h``, or None.
    """
    m = math.isqrt(order) + 1
    table: dict[tuple, int] = {}
    cur = identity
    for j in range(m):
        # Use a hashable key for the group element.
        table[tuple(cur)] = j
        cur = op(cur, g)
    # gm_inv = g^{-m} = g^{order - m}
    gm_inv = power(g, order - m)
    cur = list(h)
    for i in range(m + 1):
        key = tuple(cur)
        if key in table:
            n = i * m + table[key]
            if n < order:
                return n
        cur = op(cur, gm_inv)
    return None


def pohlig_hellman(power, op, identity, g, h, order_factors: dict[int, int],
                   subgroup_pow=None) -> Optional[int]:
    """PH solver: log_g(h) where g has known factored order in an abelian group.

    For each prime power ``q^k | order``:
      - reduce to a subgroup of order ``q^k``,
      - solve the DLP there by lifting q-by-q (each lift is a single BSGS
        in a subgroup of order q),
      - CRT-combine to get ``log_g(h) mod order``.
    """
    order = 1
    for q, k in order_factors.items():
        order *= q ** k

    residues: list[tuple[int, int]] = []
    for q, k in order_factors.items():
        qk = q ** k
        # Project g, h into the order-qk subgroup.
        cof = order // qk
        g_qk = power(g, cof)
        h_qk = power(h, cof)

        # Baby-q lift for q^k.
        x = 0
        gamma = power(g_qk, qk // q)
        for i in range(k):
            cofactor = qk // (q ** (i + 1))
            # Compute h_i = (h_qk * g_qk^{-x})^{cofactor}
            inv_gx = power(g_qk, qk - x) if x > 0 else identity
            h_i = power(op(h_qk, inv_gx), cofactor)
            d_i = _bsgs(power, op, identity, gamma, h_i, q)
            if d_i is None:
                return None
            x += d_i * (q ** i)
        residues.append((x % qk, qk))

    # CRT combine.
    n = 0
    M = 1
    for x_i, m_i in residues:
        # CRT step: solve n ≡ n_so_far (mod M), n ≡ x_i (mod m_i)
        if M == 1:
            n = x_i
            M = m_i
            continue
        # Find inv of M mod m_i
        inv_M = pow(M % m_i, -1, m_i)
        diff = (x_i - n) % m_i
        n = n + M * (diff * inv_M % m_i)
        M *= m_i
        n %= M
    return n % order


# ---------------------------------------------------------------------------
# Sedenion DLP attack inside a 2-dim sub-algebra F_p[e_1] ≅ F_{p^2}
# ---------------------------------------------------------------------------
#
# F_p[e_1] = {a + b·e_1 : a, b ∈ F_p}. The sub-algebra is associative
# (it's a 2-dim commutative ring), and e_1^2 = -1 in S_p, so this is
# F_p[X]/(X^2+1). For p ≡ 3 (mod 4) — true at p = 911, 8191, etc. —
# X^2+1 is irreducible and F_p[X]/(X^2+1) is the field F_{p^2}. The
# unit group has order p^2 − 1.


def random_subalg_element(p: int, rng: random.Random) -> list[int]:
    v = basis_vec(0)
    v[0] = rng.randrange(0, p)
    v[1] = rng.randrange(1, p)   # ensure non-trivial e_1 component
    return v


def _exact_order(power, identity, g, group_order: int,
                 group_factors: dict[int, int]) -> int:
    """Compute the exact order of g, given that g^group_order == identity."""
    n = group_order
    for q in group_factors:
        while n % q == 0 and power(g, n // q) == identity:
            n //= q
    return n


def attack_subalg_dlp(p: int, *, max_bsgs_prime: int = 1_000_000,
                      seed: int = 0xb04, max_g_attempts: int = 16) -> dict:
    rng = random.Random(seed * p)
    p_minus_1_squared = p * p - 1
    p_squared_facs = factorise(p_minus_1_squared)

    out: dict = {
        "p": p,
        "p_mod_4": p % 4,
        "subalgebra": "F_p[e_1] (multiplication via e_1^2 = -1)",
        "subalgebra_is_field": (p % 4 == 3),
        "ambient_unit_group_order": p_minus_1_squared,
        "ambient_order_factorisation": p_squared_facs,
        "ambient_largest_prime_factor": largest_prime_factor(p_squared_facs),
    }

    # When p ≡ 1 (mod 4), F_p[e_1] = F_p × F_p (not a field). The "order"
    # of an element is the lcm of its component orders, and the cyclic-PH
    # routine doesn't directly apply. We still attack each component
    # separately by treating the DLP coordinate-wise, but for this brief
    # we simply note the structural fact and skip the cyclic-PH attempt.
    def s_pow(v, n):
        return sedenion_pow(v, n, p)

    def s_mul(a, b):
        return mul_vec(a, b, p)

    identity = basis_vec(0)

    # Trial elements until we find a g of large-enough order to exercise PH.
    n_secret = None
    h = None
    g = None
    g_order = 0
    for attempt in range(max_g_attempts):
        candidate = random_subalg_element(p, rng)
        if s_pow(candidate, p_minus_1_squared) != identity:
            # Element is a zero divisor (only possible when p ≡ 1 mod 4 and
            # the F_p × F_p structure has 1-component-zero elements).
            continue
        ord_c = _exact_order(s_pow, identity, candidate, p_minus_1_squared,
                             p_squared_facs)
        if ord_c > g_order:
            g, g_order = candidate, ord_c
        if g_order == p_minus_1_squared:
            break

    if g is None:
        out["status"] = "no_invertible_element_found"
        return out

    g_order_facs = {q: e for q, e in factorise(g_order).items()}
    largest_in_g = largest_prime_factor(g_order_facs)
    out.update({
        "g_order": g_order,
        "g_order_factorisation": g_order_facs,
        "g_order_largest_prime_factor": largest_in_g,
    })

    if largest_in_g > max_bsgs_prime:
        out["status"] = "skipped"
        out["reason"] = (
            f"largest prime factor {largest_in_g} > BSGS budget "
            f"{max_bsgs_prime}"
        )
        return out

    n_secret = rng.randrange(1, g_order)
    h = s_pow(g, n_secret)

    t0 = time.perf_counter()
    n_recovered = pohlig_hellman(s_pow, s_mul, identity, g, h, g_order_facs)
    t_ph = time.perf_counter() - t0

    if n_recovered is None:
        out["status"] = "failure: PH returned None"
        out["wall_clock_seconds"] = t_ph
        return out

    h_check = s_pow(g, n_recovered)
    success = h_check == h
    out.update({
        "status": "success" if success else "mismatch",
        "secret_n_bits": n_secret.bit_length(),
        "wall_clock_seconds": t_ph,
        "secret_recovered_modulo_g_order":
            (n_recovered == n_secret % g_order),
    })
    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Attack a degree-16 sub-algebra DLP (Brief 04 extension)
# ---------------------------------------------------------------------------


def _is_lin_indep_set(vectors: list[list[int]], p: int) -> bool:
    """Check whether the given vectors over F_p are linearly independent."""
    M = [list(v) for v in vectors]
    rows = len(M)
    if not M:
        return True
    cols = len(M[0])
    rank = 0
    for c in range(cols):
        if rank >= rows:
            break
        piv = None
        for r in range(rank, rows):
            if M[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        inv = pow(M[rank][c], p - 2, p)
        M[rank] = [(v * inv) % p for v in M[rank]]
        for r in range(rows):
            if r != rank and M[r][c] != 0:
                factor = M[r][c]
                M[r] = [(M[r][j] - factor * M[rank][j]) % p
                        for j in range(cols)]
        rank += 1
    return rank == rows


def find_full_degree_sedenion(p: int, rng: random.Random,
                              max_attempts: int = 32) -> list[int] | None:
    """Find a sedenion g whose minimal polynomial has degree DIM = 16.

    Equivalently: {1, g, g^2, ..., g^15} is linearly independent in F_p^16.
    This guarantees ``F_p[g] ≅ F_{p^16}`` and ord(g) divides p^16 − 1.
    """
    for _ in range(max_attempts):
        g = [rng.randrange(0, p) for _ in range(DIM)]
        powers = [basis_vec(0)]
        cur = list(g)
        for _ in range(DIM - 1):
            powers.append(list(cur))
            cur = mul_vec(cur, g, p)
        powers.append(list(cur))    # this is g^DIM; for the rank check we
                                    # want the first DIM powers (1..g^{DIM-1}).
        if _is_lin_indep_set(powers[:DIM], p):
            return g
    return None


def attack_d16_dlp(p: int, *,
                   max_seconds: float = 1800.0,
                   max_bsgs_prime: int = 10**11,
                   seed: int = 0xb04 ^ 16) -> dict:
    """Attempt PH against the full d=16 sedenion DLP at the given prime.

    Stages, each with its own slice of the budget:

    1. Pick a random sedenion ``g`` whose minimal polynomial has full
       degree DIM = 16. ``F_p[g] ≅ F_{p^16}``.
    2. Factor ``p^16 − 1`` (the order of the unit group) within budget.
    3. Compute the exact order of ``g``.
    4. Sample ``n``, compute ``h = g^n``.
    5. Run Pohlig-Hellman on (g, h) using the factored order, with a
       global wall-clock check after each prime-power subgroup.

    Returns a dict with stage timings and outcome. Each stage is allowed
    to bail out cleanly with ``status`` set to a stage-specific token if
    the deadline is hit.
    """
    deadline = time.monotonic() + max_seconds
    rng = random.Random(seed * p)

    out: dict = {
        "p": p,
        "degree": DIM,
        "max_seconds": max_seconds,
    }

    # --- Stage 1: find a generator of full degree.
    t0 = time.monotonic()
    g = find_full_degree_sedenion(p, rng)
    out["t_find_g"] = time.monotonic() - t0
    if g is None:
        out["status"] = "no_full_degree_sedenion_found"
        return out

    # --- Stage 2: factor p^16 - 1.
    t0 = time.monotonic()
    n_field = pow(p, DIM) - 1
    facs = factorise(n_field, deadline=deadline)
    out["t_factor_p16_minus_1"] = time.monotonic() - t0
    out["p16_minus_1"] = n_field
    out["p16_minus_1_factorisation"] = dict(facs)

    if not factorise_completed(facs):
        out["status"] = "factoring_timeout"
        out["unfactored_remainder"] = facs[-1]
        return out

    largest = max(facs)
    out["p16_minus_1_largest_prime_factor"] = largest

    if largest > max_bsgs_prime:
        out["status"] = "ph_infeasible_largest_prime_too_big"
        out["bsgs_budget_largest_prime"] = max_bsgs_prime
        return out

    # --- Stage 3: exact order of g.
    t0 = time.monotonic()
    def s_pow(v, n):
        return sedenion_pow(v, n, p)

    def s_mul(a, b):
        return mul_vec(a, b, p)

    identity = basis_vec(0)
    if s_pow(g, n_field) != identity:
        out["status"] = "g_not_in_unit_group"
        return out
    g_order = _exact_order(s_pow, identity, g, n_field, facs)
    out["t_compute_order"] = time.monotonic() - t0
    out["g_order"] = g_order
    g_order_facs = factorise(g_order)
    out["g_order_factorisation"] = dict(g_order_facs)
    out["g_order_largest_prime_factor"] = max(g_order_facs)

    # --- Stage 4: sample exponent and compute h.
    n_secret = rng.randrange(1, g_order)
    h = s_pow(g, n_secret)

    if time.monotonic() > deadline:
        out["status"] = "deadline_before_ph"
        return out

    # --- Stage 5: Pohlig-Hellman. Use only g_order's factor list.
    t0 = time.monotonic()
    n_recovered = pohlig_hellman(s_pow, s_mul, identity, g, h, g_order_facs)
    out["t_ph"] = time.monotonic() - t0

    if n_recovered is None:
        out["status"] = "ph_returned_none"
        return out

    success = (s_pow(g, n_recovered) == h)
    out["status"] = "success" if success else "ph_mismatch"
    out["secret_n_bits"] = n_secret.bit_length()
    out["secret_recovered_modulo_g_order"] = (n_recovered == n_secret % g_order)
    out["wall_clock_seconds_total"] = (
        out.get("t_find_g", 0) + out.get("t_factor_p16_minus_1", 0)
        + out.get("t_compute_order", 0) + out.get("t_ph", 0)
    )
    return out


def smoothness_table(primes: list[int],
                     degrees: tuple[int, ...] = (1, 2, 4, 8)) -> list[dict]:
    """Largest prime factor of ``p^d - 1`` for each prime / degree.

    Generic sedenion ``g`` has ``F_p[g] ≅ F_{p^d}`` for some ``d ≤ 16``.
    PH against the DLP in ``F_{p^d}^*`` runs in time bounded by
    ``O(sqrt(largest prime factor of p^d - 1))``. This table is the
    smoothness-side argument that extends the empirical result from
    the d=2 sub-algebra to all small ``d``.
    """
    out = []
    for p in primes:
        row = {"p": p}
        for d in degrees:
            n = pow(p, d) - 1
            facs = factorise(n)
            row[f"p^{d}-1"] = n
            row[f"p^{d}-1_largest_prime"] = largest_prime_factor(facs)
        out.append(row)
    return out


def main() -> int:
    print("Sedenion ODLP empirical hardness probe — F_p[e_1] sub-algebra DLP\n")
    print(f"{'p':>6}  {'p mod 4':>7}  {'g order':>10}  "
          f"{'largest q':>10}  {'PH time (s)':>12}  status")
    print("-" * 78)
    for p in TEST_PRIMES:
        r = attack_subalg_dlp(p)
        print(f"{p:>6}  {r['p_mod_4']:>7}  {r.get('g_order', 0):>10}  "
              f"{r.get('g_order_largest_prime_factor', 0):>10}  "
              f"{r.get('wall_clock_seconds', float('nan')):>12.6f}  "
              f"{r['status']}")

    print("\nSmoothness of p^d - 1 (largest prime factor; PH cost ≈ sqrt of this):\n")
    print(f"{'p':>6}  {'p^1-1':>10}  {'p^2-1':>10}  {'p^4-1':>14}  {'p^8-1':>20}")
    print("-" * 72)
    for row in smoothness_table(TEST_PRIMES):
        print(f"{row['p']:>6}  "
              f"{row['p^1-1_largest_prime']:>10}  "
              f"{row['p^2-1_largest_prime']:>10}  "
              f"{row['p^4-1_largest_prime']:>14}  "
              f"{row['p^8-1_largest_prime']:>20}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
