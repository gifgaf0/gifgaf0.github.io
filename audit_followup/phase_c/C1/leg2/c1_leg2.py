#!/usr/bin/env python3
"""
C1 leg 2 (blind second leg): exact rank over F_p of the flattened
Singer-orbit sedenion public matrix.

Built only from Section 1 of audit_followup/phase_c/C1/C1_PREREG.md and the
run list handed to leg 2.  No code, data or output of leg 1, and no other
repository file or tool, was read or imported.  Everything is written from
scratch here:

  * sedenions over F_p by the Cayley-Dickson recursion
        (a, b)(c, d) = (a c - conj(d) b,  d a + b conj(c)),
    conj negating every coordinate except the real one of that level, and the
    basis e_0..e_15 with e_{i+8} = (0, e_i) (first half = a, second half = b,
    recursively at every level);
  * the Singer action sigma: coefficient of e_i -> e_{(i mod 7)+1} and of
    e_{i+8} -> e_{(i mod 7)+1+8} for i = 1..7, e_0 and e_8 fixed;
  * A[i][j] = sigma^j(seed_i), j = 0..k-1, sigma applied literally j times
    (no mod-7 shortcut, so the period-7 block equality is tested, not built in);
    seeds independent uniform in F_p^16;
  * M[16i + r][16j + c] = coefficient r of A[i][j] * e_c (left multiplication);
  * rank_{F_p}(M) by python-flint nmod_mat.rank() AND by an own exact
    Gaussian elimination in Python integers (no floats, no fixed-width ints).

Usage
    python3 -I -B c1_leg2.py              full pre-registered run; writes
                                          leg2_results.json, leg2_seeds.json and
                                          leg2_run.log next to this script
    python3 -I -B c1_leg2.py --selftest   quick checks; prints only, writes nothing
"""

import argparse
import datetime
import hashlib
import json
import os
import platform
import random
import sys
import time

import flint

P_TOY = 911
P_SPEC = 4294977961
PRIMES = (P_TOY, P_SPEC)
DIM = 16
KS_MAIN = (8, 16, 32, 64)
N_SETS = 3
CURVE_P = P_TOY
CURVE_KS = tuple(range(1, 11))
BOUND = 112                      # 7 distinct column blocks x 16 columns
RNG_PREFIX = "SQT-C1-leg2"       # all randomness = random.Random(sha256(prefix|tag))


# --------------------------------------------------------------------------
# logging
# --------------------------------------------------------------------------
class Logger:
    def __init__(self, path=None):
        self.t0 = time.time()
        self.fh = open(path, "w", encoding="utf-8") if path else None

    def __call__(self, msg=""):
        line = "[%8.1fs] %s" % (time.time() - self.t0, msg)
        print(line, flush=True)
        if self.fh:
            self.fh.write(line + "\n")
            self.fh.flush()

    def close(self):
        if self.fh:
            self.fh.close()


# --------------------------------------------------------------------------
# primality (own deterministic Miller-Rabin): guards that F_p is a field
# --------------------------------------------------------------------------
_MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)  # deterministic below 3.3e24


def is_prime_mr(n):
    if n < 2:
        return False
    for b in _MR_BASES:
        if n % b == 0:
            return n == b
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _MR_BASES:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


# --------------------------------------------------------------------------
# Cayley-Dickson algebra
# --------------------------------------------------------------------------
def cd_conj(x, p):
    """Conjugate at the level of x: negate every coordinate except the real one."""
    if p is None:
        return [x[0]] + [-v for v in x[1:]]
    return [x[0] % p] + [(-v) % p for v in x[1:]]


def cd_mul(x, y, p):
    """Cayley-Dickson product of two coordinate vectors of length 2^n.

    x = (a, b), y = (c, d) split into first / second halves, so e_{i+h} = (0, e_i);
    (a, b)(c, d) = (a c - conj(d) b,  d a + b conj(c)).
    p = modulus (all arithmetic mod p) or None (exact integers)."""
    n = len(x)
    if n == 1:
        v = x[0] * y[0]
        return [v % p] if p is not None else [v]
    h = n // 2
    a, b = x[:h], x[h:]
    c, d = y[:h], y[h:]
    ac = cd_mul(a, c, p)
    db = cd_mul(cd_conj(d, p), b, p)
    da = cd_mul(d, a, p)
    bc = cd_mul(b, cd_conj(c, p), p)
    if p is None:
        return [u - v for u, v in zip(ac, db)] + [u + v for u, v in zip(da, bc)]
    return [(u - v) % p for u, v in zip(ac, db)] + [(u + v) % p for u, v in zip(da, bc)]


def basis(i, dim=DIM):
    v = [0] * dim
    v[i] = 1
    return v


def structure_sparse(p):
    """Nonzero structure constants, from cd_mul on basis vectors:
    list of (m, c, r, coef) with coefficient r of e_m * e_c equal to coef != 0."""
    out = []
    for m in range(DIM):
        em = basis(m)
        for c in range(DIM):
            prod = cd_mul(em, basis(c), p)
            for r, coef in enumerate(prod):
                if coef:
                    out.append((m, c, r, coef))
    return out


def left_mult_matrix(a, sparse, p):
    """16 x 16 matrix of y -> a*y over F_p; column c is a*e_c (by bilinearity)."""
    L = [[0] * DIM for _ in range(DIM)]
    for m, c, r, coef in sparse:
        am = a[m]
        if am:
            L[r][c] += am * coef
    return [[v % p for v in row] for row in L]


def mat_vec(L, y, p):
    return [sum(l * v for l, v in zip(row, y)) % p for row in L]


# --------------------------------------------------------------------------
# Singer action
# --------------------------------------------------------------------------
def sigma(v):
    """sigma(v)[(i mod 7)+1] = v[i] and sigma(v)[(i mod 7)+1+8] = v[i+8], i = 1..7;
    coordinates 0 and 8 unchanged."""
    w = list(v)
    for i in range(1, 8):
        t = (i % 7) + 1
        w[t] = v[i]
        w[t + 8] = v[i + 8]
    return w


def sigma_power(v, j):
    for _ in range(j):
        v = sigma(v)
    return v


# --------------------------------------------------------------------------
# randomness
# --------------------------------------------------------------------------
def rng_for(tag):
    h = hashlib.sha256((RNG_PREFIX + "|" + tag).encode("utf-8")).digest()
    return random.Random(int.from_bytes(h, "big"))


def uniform_vector(rng, p):
    return [rng.randrange(p) for _ in range(DIM)]


def sha256_json(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# public matrix and flattening
# --------------------------------------------------------------------------
def singer_public_matrix(seeds):
    """A[i][j] = sigma^j(seed_i), j = 0..k-1 (sigma applied j times)."""
    k = len(seeds)
    A = []
    for s in seeds:
        row = [list(s)]
        for _ in range(1, k):
            row.append(sigma(row[-1]))
        A.append(row)
    return A


def uniform_public_matrix(rng, k, p):
    return [[uniform_vector(rng, p) for _ in range(k)] for _ in range(k)]


def flatten(A, sparse, p):
    """M[16i + r][16j + c] = coefficient r of A[i][j] * e_c."""
    k = len(A)
    n = DIM * k
    M = [[0] * n for _ in range(n)]
    for i in range(k):
        for j in range(k):
            L = left_mult_matrix(A[i][j], sparse, p)
            for r in range(DIM):
                M[DIM * i + r][DIM * j: DIM * j + DIM] = L[r]
    return M


# --------------------------------------------------------------------------
# exact rank, two ways
# --------------------------------------------------------------------------
def rank_flint(M, p):
    if not M:
        return 0
    return int(flint.nmod_mat(M, p).rank())


def rank_own(M, p):
    """Exact rank over F_p: row-echelon Gaussian elimination in Python integers.
    Invariant: rows >= rank are zero in all columns < col, so only tails are updated."""
    A = [[v % p for v in row] for row in M]
    nr = len(A)
    nc = len(A[0]) if nr else 0
    rank = 0
    for col in range(nc):
        if rank == nr:
            break
        piv = -1
        for r in range(rank, nr):
            if A[r][col]:
                piv = r
                break
        if piv < 0:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        prow = A[rank]
        inv = pow(prow[col], -1, p)
        tail = [(v * inv) % p for v in prow[col:]]
        for r in range(rank + 1, nr):
            row = A[r]
            f = row[col]
            if f:
                row[col:] = [(x - f * y) % p for x, y in zip(row[col:], tail)]
        rank += 1
    return rank


# --------------------------------------------------------------------------
# block structure checks
# --------------------------------------------------------------------------
def period7_check(M, k):
    """{j: column block j == column block j+7} for every j with j+7 < k."""
    res = {}
    for j in range(0, k - 7):
        a, b = DIM * j, DIM * (j + 7)
        res[j] = all(row[a:a + DIM] == row[b:b + DIM] for row in M)
    return res


def distinct_column_blocks(M, k):
    return len({tuple(tuple(row[DIM * j: DIM * j + DIM]) for row in M) for j in range(k)})


def universal_matrix(sparse, p):
    """Seed-free matrix N (256 x 112): N[16m + r][16j + c] = coeff r of sigma^j(e_m) * e_c,
    m = 0..15, j = 0..6.  For seeds S (k x 16): M = (S kron I_16) N_k, where N_k repeats
    the 7 column blocks with period 7; so rank(M) <= rank(N), with equality if rank(S) = 16."""
    N = [[0] * (DIM * 7) for _ in range(DIM * DIM)]
    for m in range(DIM):
        v = basis(m)
        for j in range(7):
            L = left_mult_matrix(v, sparse, p)
            for r in range(DIM):
                N[DIM * m + r][DIM * j: DIM * j + DIM] = L[r]
            v = sigma(v)
    return N


# --------------------------------------------------------------------------
# sanity checks of the algebra and of sigma
# --------------------------------------------------------------------------
def exact_structure_checks():
    """Over the integers (characteristic 0)."""
    E = [basis(i) for i in range(DIM)]
    xor_ok, anti_ok = True, True
    for i in range(DIM):
        for j in range(DIM):
            prod = cd_mul(E[i], E[j], None)
            nz = [(r, v) for r, v in enumerate(prod) if v]
            if len(nz) != 1 or nz[0][0] != (i ^ j) or nz[0][1] not in (1, -1):
                xor_ok = False
            if i >= 1 and j >= 1 and i != j:
                other = cd_mul(E[j], E[i], None)
                if [-v for v in other] != prod:
                    anti_ok = False
    # deterministic witness of non-alternativity: x = e_a + e_b, y = e_c
    witness = None
    for a in range(1, DIM):
        for b in range(a + 1, DIM):
            x = [0] * DIM
            x[a] = 1
            x[b] = 1
            for c in range(1, DIM):
                y = E[c]
                lhs = cd_mul(cd_mul(x, x, None), y, None)
                rhs = cd_mul(x, cd_mul(x, y, None), None)
                if lhs != rhs:
                    witness = {"x": "e_%d + e_%d" % (a, b), "y": "e_%d" % c,
                               "(xx)y": {str(r): v for r, v in enumerate(lhs) if v},
                               "x(xy)": {str(r): v for r, v in enumerate(rhs) if v}}
                    break
            if witness:
                break
        if witness:
            break
    # octonion witness search over the same family (must find nothing)
    oct_counter = 0
    for a in range(1, 8):
        for b in range(a + 1, 8):
            x = [0] * DIM
            x[a] = 1
            x[b] = 1
            for c in range(1, 8):
                if cd_mul(cd_mul(x, x, None), E[c], None) != cd_mul(x, cd_mul(x, E[c], None), None):
                    oct_counter += 1
    table_signs = [[0] * DIM for _ in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            prod = cd_mul(E[i], E[j], None)
            table_signs[i][j] = prod[i ^ j]
    return {
        "e_i_e_j_is_plus_or_minus_e_(i_xor_j)_all_i_j": xor_ok,
        "imaginary_units_anticommute": anti_ok,
        "e1e2_eq_e3": cd_mul(E[1], E[2], None) == E[3],
        "e1e4_eq_e5": cd_mul(E[1], E[4], None) == E[5],
        "e1e8_eq_e9": cd_mul(E[1], E[8], None) == E[9],
        "sedenion_non_alternativity_witness": witness,
        "octonion_counterexamples_in_family_e_a+e_b,e_c": oct_counter,
        "sign_table_e_i_e_j_coefficient_of_e_(i_xor_j)": table_signs,
    }


def norm(x, p):
    return sum(v * v for v in x) % p


def sanity_checks(p, sparse, trials=200):
    out = {}
    rng = rng_for("sanity|p=%d" % p)
    E = [basis(i) for i in range(DIM)]
    minus_e0 = [p - 1] + [0] * (DIM - 1)

    # (1) e_i e_i = -e_0 for i = 1..15
    fails = [i for i in range(1, DIM) if cd_mul(E[i], E[i], p) != minus_e0]
    out["e_i_squared_eq_minus_e0_i_1_to_15"] = (len(fails) == 0)
    out["e_i_squared_failures"] = fails

    # (2) e_0 is the identity (basis, both sides; and 100 random elements, both sides)
    out["e0_identity_on_basis_both_sides"] = all(
        cd_mul(E[0], E[c], p) == E[c] and cd_mul(E[c], E[0], p) == E[c] for c in range(DIM))
    ok = True
    for _ in range(100):
        x = uniform_vector(rng, p)
        if cd_mul(E[0], x, p) != x or cd_mul(x, E[0], p) != x:
            ok = False
    out["e0_identity_on_100_random_both_sides"] = ok

    # (3) octonions alternative on random elements; sedenions not
    o_left = o_right = o_closed = o_norm = 0
    s_left = s_right = s_norm = s_flex = 0
    for _ in range(trials):
        x = [rng.randrange(p) for _ in range(8)] + [0] * 8
        y = [rng.randrange(p) for _ in range(8)] + [0] * 8
        xx, xy, yx = cd_mul(x, x, p), cd_mul(x, y, p), cd_mul(y, x, p)
        o_left += cd_mul(xx, y, p) == cd_mul(x, xy, p)
        o_right += cd_mul(yx, x, p) == cd_mul(y, xx, p)
        o_closed += all(v == 0 for v in xy[8:])
        o_norm += norm(xy, p) == norm(x, p) * norm(y, p) % p
    for _ in range(trials):
        x = uniform_vector(rng, p)
        y = uniform_vector(rng, p)
        xx, xy, yx = cd_mul(x, x, p), cd_mul(x, y, p), cd_mul(y, x, p)
        s_left += cd_mul(xx, y, p) == cd_mul(x, xy, p)
        s_right += cd_mul(yx, x, p) == cd_mul(y, xx, p)
        s_norm += norm(xy, p) == norm(x, p) * norm(y, p) % p
        s_flex += cd_mul(xy, x, p) == cd_mul(x, yx, p)
    out["trials"] = trials
    out["octonion_left_alternative_(xx)y=x(xy)_pass"] = o_left
    out["octonion_right_alternative_(yx)x=y(xx)_pass"] = o_right
    out["octonion_product_closed_in_e0..e7"] = o_closed
    out["octonion_norm_multiplicative_pass"] = o_norm
    out["sedenion_left_alternative_(xx)y=x(xy)_pass"] = s_left
    out["sedenion_right_alternative_(yx)x=y(xx)_pass"] = s_right
    out["sedenion_norm_multiplicative_pass"] = s_norm
    out["sedenion_flexible_(xy)x=x(yx)_pass"] = s_flex

    # (4) left-multiplication matrices agree with the direct product
    lm_ok = True
    for _ in range(30):
        a = uniform_vector(rng, p)
        b = uniform_vector(rng, p)
        L = left_mult_matrix(a, sparse, p)
        if mat_vec(L, b, p) != cd_mul(a, b, p):
            lm_ok = False
        for c in range(DIM):
            if [L[r][c] for r in range(DIM)] != cd_mul(a, E[c], p):
                lm_ok = False
    out["left_mult_matrix_equals_direct_product_30_random"] = lm_ok

    # (5) sigma
    sig = {}
    v = uniform_vector(rng, p)
    sig["sigma^7_is_identity_on_random_vector"] = sigma_power(v, 7) == v
    sig["sigma^7_is_identity_on_basis"] = all(sigma_power(E[i], 7) == E[i] for i in range(DIM))
    sig["sigma^d_not_identity_for_d_1_to_6"] = all(sigma_power(v, d) != v for d in range(1, 7))
    sig["fixes_e0_e8"] = sigma(E[0]) == E[0] and sigma(E[8]) == E[8]
    sig["e1->e2, e7->e1, e9->e10, e15->e9"] = (sigma(E[1]) == E[2] and sigma(E[7]) == E[1]
                                              and sigma(E[9]) == E[10] and sigma(E[15]) == E[9])
    images = {}
    for i in range(DIM):
        w = sigma(E[i])
        images[i] = w.index(1)
    sig["image_index_of_e_i"] = images
    auto = True
    for _ in range(50):
        x = uniform_vector(rng, p)
        y = uniform_vector(rng, p)
        if sigma(cd_mul(x, y, p)) != cd_mul(sigma(x), sigma(y), p):
            auto = False
            break
    sig["descriptive_sigma_is_algebra_automorphism"] = auto
    out["sigma"] = sig
    return out


# --------------------------------------------------------------------------
# runs
# --------------------------------------------------------------------------
def singer_run(p, k, seeds, sparse, log, label, do_own=True):
    t = time.time()
    A = singer_public_matrix(seeds)
    M = flatten(A, sparse, p)
    t_build = time.time() - t
    t = time.time()
    rf = rank_flint(M, p)
    t_flint = time.time() - t
    ro, t_own = None, None
    if do_own:
        t = time.time()
        ro = rank_own(M, p)
        t_own = time.time() - t
    p7 = period7_check(M, k)
    ndist = distinct_column_blocks(M, k)
    rS = rank_flint(seeds, p)
    few = sum(1 for s in seeds if sum(1 for v in s if v) <= 2)
    rec = {
        "prime": p, "k": k, "n": DIM * k, "label": label,
        "rank_flint": rf, "rank_own": ro,
        "flint_equals_own": (ro is None) or (rf == ro),
        "rank_le_112": rf <= BOUND and (ro is None or ro <= BOUND),
        "bound_min_16k_112": min(DIM * k, BOUND),
        "period7_pairs_checked": len(p7),
        "period7_all_equal": all(p7.values()) if p7 else None,
        "period7_failures": [j for j, ok in p7.items() if not ok],
        "distinct_column_blocks": ndist,
        "rank_seed_matrix_S": rS,
        "seeds_with_le_2_nonzero_coords": few,
        "seeds_sha256": sha256_json(seeds),
        "seconds": {"build": round(t_build, 2), "flint": round(t_flint, 2),
                    "own": round(t_own, 2) if t_own is not None else None},
    }
    log("  %-22s p=%-10d k=%-2d n=%-4d rank flint=%-4d own=%-4s  <=112:%s  blocks j==j+7 (%d pairs): %s  "
        "distinct col blocks=%d  rank(S)=%d  [build %.1fs, flint %.2fs, own %s]"
        % (label, p, k, DIM * k, rf, ro, rec["rank_le_112"], len(p7), rec["period7_all_equal"], ndist, rS,
           t_build, t_flint, ("%.1fs" % t_own) if t_own is not None else "-"))
    return rec


def control_run(p, k, sparse, log, do_own=True):
    rng = rng_for("control|p=%d|k=%d" % (p, k))
    t = time.time()
    A = uniform_public_matrix(rng, k, p)
    M = flatten(A, sparse, p)
    t_build = time.time() - t
    t = time.time()
    rf = rank_flint(M, p)
    t_flint = time.time() - t
    ro, t_own = None, None
    if do_own:
        t = time.time()
        ro = rank_own(M, p)
        t_own = time.time() - t
    rec = {
        "prime": p, "k": k, "n": DIM * k,
        "rank_flint": rf, "rank_own": ro,
        "flint_equals_own": (ro is None) or (rf == ro),
        "full_rank_16k": rf == DIM * k and (ro is None or ro == DIM * k),
        "entries_sha256": sha256_json(A),
        "seconds": {"build": round(t_build, 2), "flint": round(t_flint, 2),
                    "own": round(t_own, 2) if t_own is not None else None},
    }
    log("  control                p=%-10d k=%-2d n=%-4d rank flint=%-4d own=%-4s  full(16k=%d):%s  "
        "[build %.1fs, flint %.2fs, own %s]"
        % (p, k, DIM * k, rf, ro, DIM * k, rec["full_rank_16k"], t_build, t_flint,
           ("%.1fs" % t_own) if t_own is not None else "-"))
    return rec


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, sort_keys=False)
        fh.write("\n")


def md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def selftest():
    log = Logger(None)
    log("SELFTEST (no files written)")
    for p in PRIMES:
        log("prime %d: Miller-Rabin %s, flint %s" % (p, is_prime_mr(p), bool(flint.fmpz(p).is_prime())))
    ex = exact_structure_checks()
    log("exact: xor table %s, anticommute %s, witness %s, octonion counterexamples %d"
        % (ex["e_i_e_j_is_plus_or_minus_e_(i_xor_j)_all_i_j"], ex["imaginary_units_anticommute"],
           ex["sedenion_non_alternativity_witness"], ex["octonion_counterexamples_in_family_e_a+e_b,e_c"]))
    for p in PRIMES:
        sp = structure_sparse(p)
        sc = sanity_checks(p, sp, trials=20)
        log("p=%d sanity: %s" % (p, json.dumps(sc)))
        for k in (1, 2, 8):
            rng = rng_for("selftest|%d|%d" % (p, k))
            seeds = [uniform_vector(rng, p) for _ in range(k)]
            singer_run(p, k, seeds, sp, log, "selftest-singer")
        control_run(p, 8, sp, log)
    log("SELFTEST done")


def full_run(outdir):
    os.makedirs(outdir, exist_ok=True)
    path_log = os.path.join(outdir, "leg2_run.log")
    path_res = os.path.join(outdir, "leg2_results.json")
    path_seeds = os.path.join(outdir, "leg2_seeds.json")
    log = Logger(path_log)
    t_start = datetime.datetime.now(datetime.timezone.utc)

    prereg = os.path.normpath(os.path.join(outdir, "..", "C1_PREREG.md"))
    prereg_md5 = md5_file(prereg) if os.path.exists(prereg) else None
    script_md5 = md5_file(os.path.abspath(__file__))

    log("C1 leg 2 (blind) -- start %s" % t_start.isoformat())
    log("python %s | python-flint %s | %s" % (platform.python_version(), flint.__version__, platform.platform()))
    log("prereg md5 %s | script md5 %s" % (prereg_md5, script_md5))
    log("randomness: random.Random(int(sha256('%s|' + tag))) ; randrange(p) per coordinate" % RNG_PREFIX)

    results = {
        "leg": 2,
        "object": "C1_PREREG.md section 1: Singer-orbit sedenion public matrix, flattened by left multiplication",
        "started_utc": t_start.isoformat(),
        "environment": {"python": platform.python_version(), "python_flint": flint.__version__,
                        "platform": platform.platform()},
        "provenance": {"prereg_path": "audit_followup/phase_c/C1/C1_PREREG.md", "prereg_md5": prereg_md5,
                       "script": "c1_leg2.py", "script_md5": script_md5},
        "randomness": {"generator": "Python random.Random (MT19937) seeded with int(sha256(prefix|tag))",
                       "prefix": RNG_PREFIX,
                       "tags": {"singer": "singer|p=<p>|k=<k>|set=<s>", "control": "control|p=<p>|k=<k>",
                                "curve": "curve|p=911 (10 seeds; the curve at k uses the first k)",
                                "sanity": "sanity|p=<p>"},
                       "draw": "rng.randrange(p) for each of the 16 coordinates, seed after seed (row-major for controls)"},
        "rank_methods": {"flint": "python-flint nmod_mat(M, p).rank()",
                         "own": "row-echelon Gaussian elimination mod p in Python integers (rank_own)"},
    }
    seeds_out = {"note": "Seed vectors (coordinates 0..15 in F_p) for every Singer-orbit matrix of leg 2.",
                 "singer": {}, "curve_p911": None}

    # --- fields
    log("")
    log("== primes ==")
    pr = {}
    for p in PRIMES:
        mr = is_prime_mr(p)
        fl = bool(flint.fmpz(p).is_prime())
        pr[str(p)] = {"miller_rabin_deterministic": mr, "flint_is_prime": fl, "p_mod_455": p % 455}
        log("p=%d  prime(MR)=%s prime(flint)=%s  p mod 455 = %d" % (p, mr, fl, p % 455))
    # extra: q is the smallest prime above 2^32 that is 1 mod 455
    n0 = 2 ** 32
    first = n0 + ((1 - n0) % 455)
    cand = first
    while not is_prime_mr(cand):
        cand += 455
    pr["smallest_prime_above_2^32_congruent_1_mod_455"] = cand
    log("smallest prime > 2^32 with p = 1 mod 455: %d (spec q = %d) -> %s" % (cand, P_SPEC, cand == P_SPEC))
    results["primes"] = pr

    # --- sanity
    log("")
    log("== sanity checks of the algebra ==")
    ex = exact_structure_checks()
    log("exact (over Z): e_i e_j = +-e_(i xor j) for all i,j: %s ; imaginary units anticommute: %s ; "
        "e1e2=e3: %s ; e1e4=e5: %s ; e1e8=e9: %s"
        % (ex["e_i_e_j_is_plus_or_minus_e_(i_xor_j)_all_i_j"], ex["imaginary_units_anticommute"],
           ex["e1e2_eq_e3"], ex["e1e4_eq_e5"], ex["e1e8_eq_e9"]))
    log("exact witness of sedenion non-alternativity: %s" % json.dumps(ex["sedenion_non_alternativity_witness"]))
    log("same witness family inside the octonions (e_a+e_b, e_c with a,b,c<=7): %d counterexamples"
        % ex["octonion_counterexamples_in_family_e_a+e_b,e_c"])
    log("sign table (row i, col j: coefficient of e_(i xor j) in e_i e_j):")
    for i, row in enumerate(ex["sign_table_e_i_e_j_coefficient_of_e_(i_xor_j)"]):
        log("   e_%-2d: %s" % (i, " ".join("%+d" % v for v in row)))
    results["sanity_exact"] = ex

    sparse = {}
    results["sanity_mod_p"] = {}
    for p in PRIMES:
        sparse[p] = structure_sparse(p)
        sc = sanity_checks(p, sparse[p])
        results["sanity_mod_p"][str(p)] = sc
        log("p=%d: nonzero structure constants: %d" % (p, len(sparse[p])))
        for key, val in sc.items():
            if key == "sigma":
                for k2, v2 in val.items():
                    log("p=%d:   sigma: %s = %s" % (p, k2, v2))
            else:
                log("p=%d:   %s = %s" % (p, key, val))

    # --- main runs
    log("")
    log("== main runs: Singer-orbit public matrix, k in %s, 3 seed sets each ==" % (KS_MAIN,))
    main = []
    for p in PRIMES:
        for k in KS_MAIN:
            for s in range(N_SETS):
                rng = rng_for("singer|p=%d|k=%d|set=%d" % (p, k, s))
                seeds = [uniform_vector(rng, p) for _ in range(k)]
                seeds_out["singer"]["p=%d|k=%d|set=%d" % (p, k, s)] = seeds
                rec = singer_run(p, k, seeds, sparse[p], log, "singer set %d" % s)
                rec["set"] = s
                main.append(rec)
                results["main_runs"] = main
                write_json(path_res, results)
    write_json(path_seeds, seeds_out)

    # --- controls
    log("")
    log("== controls: fully uniform A ==")
    controls = []
    for p in PRIMES:
        for k in KS_MAIN:
            rec = control_run(p, k, sparse[p], log)
            controls.append(rec)
            results["controls"] = controls
            write_json(path_res, results)

    # --- curve
    log("")
    log("== descriptive curve at p = 911, k = 1..10 (one seed list of 10; the matrix at k uses seeds 0..k-1) ==")
    rng = rng_for("curve|p=%d" % CURVE_P)
    seeds10 = [uniform_vector(rng, CURVE_P) for _ in range(max(CURVE_KS))]
    seeds_out["curve_p911"] = seeds10
    curve = []
    for k in CURVE_KS:
        rec = singer_run(CURVE_P, k, seeds10[:k], sparse[CURVE_P], log, "curve")
        curve.append(rec)
    results["curve_p911"] = curve
    write_json(path_res, results)
    write_json(path_seeds, seeds_out)

    # --- extra: seed-free universal matrix N
    log("")
    log("== extra (descriptive): seed-free matrix N[16m+r][16j+c] = coeff r of sigma^j(e_m) e_c, 256 x 112 ==")
    uni = {}
    for p in PRIMES:
        N = universal_matrix(sparse[p], p)
        rf, ro = rank_flint(N, p), rank_own(N, p)
        uni[str(p)] = {"rank_flint": rf, "rank_own": ro}
        log("p=%d: rank N flint=%d own=%d" % (p, rf, ro))
    results["extra_universal_matrix_N"] = {
        "definition": "N[16m + r][16j + c] = coefficient r of sigma^j(e_m) * e_c, m = 0..15, j = 0..6",
        "relation": "M = (S kron I_16) N_k with S the k x 16 seed matrix and N_k the k column blocks "
                    "(block j = block j mod 7 of N); so rank(M) <= rank(N), equality when rank(S) = 16",
        "ranks": uni,
    }
    consistent = []
    for rec in main + curve:
        rN = uni[str(rec["prime"])]["rank_flint"]
        if rec["rank_seed_matrix_S"] == DIM and rec["k"] >= 7:
            consistent.append(rec["rank_flint"] == rN)
        if rec["rank_flint"] > rN:
            consistent.append(False)
    results["extra_universal_matrix_N"]["all_runs_consistent_with_N"] = all(consistent)
    log("all Singer runs consistent with rank(N) (rank(M) <= rank(N); = when rank(S)=16, k>=7): %s"
        % all(consistent))

    # --- summary
    table = []
    for p in PRIMES:
        for k in KS_MAIN:
            rs = [r["rank_flint"] for r in main if r["prime"] == p and r["k"] == k]
            ro = [r["rank_own"] for r in main if r["prime"] == p and r["k"] == k]
            c = [r for r in controls if r["prime"] == p and r["k"] == k][0]
            table.append({"k": k, "prime": p, "n": DIM * k, "singer_ranks_flint": rs, "singer_ranks_own": ro,
                          "control_rank_flint": c["rank_flint"], "control_rank_own": c["rank_own"],
                          "deficit_16k_minus_max_rank": DIM * k - max(rs)})
    singer_all = main + curve
    summary = {
        "table": table,
        "curve_p911": [{"k": r["k"], "rank_flint": r["rank_flint"], "rank_own": r["rank_own"],
                        "bound_min_16k_112": r["bound_min_16k_112"]} for r in curve],
        "all_main_singer_ranks_le_112": all(r["rank_le_112"] for r in main),
        "all_controls_full_rank_16k": all(r["full_rank_16k"] for r in controls),
        "flint_equals_own_everywhere": all(r["flint_equals_own"] for r in singer_all + controls)
                                       and all(v["rank_flint"] == v["rank_own"] for v in uni.values()),
        "own_elimination_runs": sum(1 for r in singer_all + controls if r["rank_own"] is not None),
        "period7_block_equality_all_singer_matrices_k_ge_8": all(
            r["period7_all_equal"] for r in singer_all if r["k"] >= 8),
        "period7_pairs_checked_total": sum(r["period7_pairs_checked"] for r in singer_all),
        "distinct_column_blocks_eq_min_k_7": all(r["distinct_column_blocks"] == min(r["k"], 7) for r in singer_all),
        "seeds_with_le_2_nonzero_coords_total": sum(r["seeds_with_le_2_nonzero_coords"] for r in singer_all),
        "leg2_side_of_PASS_rule": None,
    }
    summary["leg2_side_of_PASS_rule"] = (
        "rank <= 112 at all four k (both primes, all sets): %s; both controls full rank at every (k, p): %s"
        % (summary["all_main_singer_ranks_le_112"], summary["all_controls_full_rank_16k"]))
    results["summary"] = summary
    t_end = datetime.datetime.now(datetime.timezone.utc)
    results["finished_utc"] = t_end.isoformat()
    results["wall_seconds"] = round((t_end - t_start).total_seconds(), 1)
    write_json(path_res, results)

    log("")
    log("== summary ==")
    log("k   prime        n     Singer ranks (flint)   (own)              control flint/own")
    for row in table:
        log("%-3d %-12d %-5d %-22s %-18s %d/%s"
            % (row["k"], row["prime"], row["n"], row["singer_ranks_flint"], row["singer_ranks_own"],
               row["control_rank_flint"], row["control_rank_own"]))
    log("curve p=911: " + ", ".join("k=%d:%d" % (r["k"], r["rank_flint"]) for r in curve))
    for key in ("all_main_singer_ranks_le_112", "all_controls_full_rank_16k", "flint_equals_own_everywhere",
                "own_elimination_runs", "period7_block_equality_all_singer_matrices_k_ge_8",
                "period7_pairs_checked_total", "distinct_column_blocks_eq_min_k_7",
                "seeds_with_le_2_nonzero_coords_total"):
        log("%s: %s" % (key, summary[key]))
    log("finished %s (wall %.1fs)" % (t_end.isoformat(), results["wall_seconds"]))
    log.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true", help="quick checks only; writes no files")
    ap.add_argument("--outdir", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()
    if args.selftest:
        selftest()
    else:
        try:
            full_run(args.outdir)
        except Exception:
            import traceback
            with open(os.path.join(args.outdir, "leg2_run.log"), "a", encoding="utf-8") as fh:
                fh.write("FATAL:\n" + traceback.format_exc())
            raise


if __name__ == "__main__":
    main()
