"""
sedenion_Fp.py
==============
Construct the sedenion algebra S over F_p for a mod-455 prime p,
enumerate its zero-divisors, and verify the 84-pair structure.

Sedenions: 16-dimensional Cayley-Dickson double of the octonions.
Basis: e0 (real unit), e1..e15 (imaginary units).
Multiplication defined recursively via Cayley-Dickson construction.

Over F_p (p ≡ 1 mod 455): we expect the zero-divisor structure to
mirror the real case (Moreno 1998, Cawagas 2004: exactly 84 pairs).

This is a finite-field analog — a new computation, not in the literature.
"""

from itertools import combinations

# ─────────────────────────────────────────────────────────────────
# CAYLEY-DICKSON MULTIPLICATION TABLE (standard basis e0..e15)
# ─────────────────────────────────────────────────────────────────
# Build via recursive CD construction.
# At each level, (a,b)(c,d) = (ac - d*conj(b), d*a + b*conj(c))
# where conj at level n flips sign of all imaginary parts.
# We represent each basis element as an index 0..2^n - 1.
# Multiplication: returns (index, sign) where result = sign * e_index

def build_cd_table(n_levels):
    """
    Build the Cayley-Dickson multiplication table for 2^n_levels dimensions.
    Returns mult[i][j] = (k, sign) meaning e_i * e_j = sign * e_k
    """
    dim = 2 ** n_levels
    # Initialize: at level 0 (reals), e0*e0 = e0
    # mult[i][j] = (result_index, sign)
    mult = [[(0, 1)] * dim for _ in range(dim)]

    # Level 0: just the real unit
    mult[0][0] = (0, 1)

    def cd_mult(mult_prev, dim_prev):
        """One CD doubling step."""
        dim_new = dim_prev * 2
        new_mult = [[(0, 1)] * dim_new for _ in range(dim_new)]

        def conj_sign(i, dim):
            """Conjugate of e_i: e_0 -> e_0, e_k -> -e_k for k>0"""
            return (i, 1) if i == 0 else (i, -1)

        # (a, b)(c, d) = (ac - conj(d)b, da + b*conj(c))
        # Indices: left half = 0..dim_prev-1, right half = dim_prev..dim_new-1
        # e_i for i < dim_prev is "a" part; e_{i+dim_prev} is "b=(0,...,0,1,...)"

        for i in range(dim_new):
            for j in range(dim_new):
                # Decompose i = (a_idx, b_idx), j = (c_idx, d_idx)
                if i < dim_prev:
                    a_idx, a_sign = i, 1
                    b_idx, b_sign = None, 0
                else:
                    a_idx, a_sign = None, 0
                    b_idx, b_sign = i - dim_prev, 1

                if j < dim_prev:
                    c_idx, c_sign = j, 1
                    d_idx, d_sign = None, 0
                else:
                    c_idx, c_sign = None, 0
                    d_idx, d_sign = j - dim_prev, 1

                # Result components:
                # real part: ac - conj(d)*b
                # imag part: d*a + b*conj(c)

                result_real = []   # list of (idx, sign) contributions to real half
                result_imag = []   # list of (idx, sign) contributions to imag half

                # ac term (real part)
                if a_idx is not None and c_idx is not None:
                    r, s = mult_prev[a_idx][c_idx]
                    result_real.append((r, s * a_sign * c_sign))

                # -conj(d)*b term (real part)
                if d_idx is not None and b_idx is not None:
                    cd_idx, cd_s = conj_sign(d_idx, dim_prev)
                    r, s = mult_prev[cd_idx][b_idx]
                    result_real.append((r, -s * cd_s * d_sign * b_sign))

                # d*a term (imag part)
                if d_idx is not None and a_idx is not None:
                    r, s = mult_prev[d_idx][a_idx]
                    result_imag.append((r, s * d_sign * a_sign))

                # b*conj(c) term (imag part)
                if b_idx is not None and c_idx is not None:
                    cc_idx, cc_s = conj_sign(c_idx, dim_prev)
                    r, s = mult_prev[b_idx][cc_idx]
                    result_imag.append((r, s * b_sign * cc_s))

                # Collect: should have at most one nonzero term in each half
                # (since we're working with basis elements)
                real_terms = [(r, s) for r, s in result_real if s != 0]
                imag_terms = [(r, s) for r, s in result_imag if s != 0]

                # For basis multiplication, exactly one of real/imag is nonzero
                all_terms = [(r, s) for r, s in real_terms] + \
                            [(r + dim_prev, s) for r, s in imag_terms]

                # Filter zero contributions
                all_terms = [(idx, s) for idx, s in all_terms if s != 0]

                if len(all_terms) == 0:
                    new_mult[i][j] = (0, 0)  # zero result (shouldn't happen for basis)
                elif len(all_terms) == 1:
                    new_mult[i][j] = all_terms[0]
                else:
                    # Multiple terms — means we have a sum, encode as list
                    new_mult[i][j] = all_terms

        return new_mult

    # Build level by level
    current = [[(0, 1)]]  # 1x1: e0*e0=e0
    for level in range(1, n_levels + 1):
        dim_prev = 2 ** (level - 1)
        current = cd_mult(current, dim_prev)

    return current


# Build the sedenion (level 4, 16-dimensional) table
print("Building Cayley-Dickson multiplication table for sedenions (16D)...")
_raw_table = build_cd_table(4)

# Convert to a clean 16x16 table: mult[i][j] = list of (idx, sign) pairs
DIM = 16
MULT = [[None]*DIM for _ in range(DIM)]
for i in range(DIM):
    for j in range(DIM):
        r = _raw_table[i][j]
        if isinstance(r, tuple):
            MULT[i][j] = [r] if r[1] != 0 else []
        else:
            MULT[i][j] = [(idx, s) for idx, s in r if s != 0]

print("Table built.")

# ─────────────────────────────────────────────────────────────────
# SEDENION ARITHMETIC OVER F_p
# ─────────────────────────────────────────────────────────────────

def mul_basis(i, j):
    """Multiply basis elements e_i * e_j. Returns list of (index, sign)."""
    return MULT[i][j]

def mul_vec(x, y, p):
    """Multiply two sedenion elements x, y (length-16 vectors over F_p)."""
    result = [0] * DIM
    for i in range(DIM):
        if x[i] == 0:
            continue
        for j in range(DIM):
            if y[j] == 0:
                continue
            for (k, s) in mul_basis(i, j):
                result[k] = (result[k] + x[i] * y[j] * s) % p
    return result

def is_zero(v, p):
    return all(c % p == 0 for c in v)

def basis_vec(i):
    v = [0]*DIM
    v[i] = 1
    return v

def add_vec(x, y, p):
    return [(a + b) % p for a, b in zip(x, y)]

def scale_vec(x, s, p):
    return [(c * s) % p for c in x]


# ─────────────────────────────────────────────────────────────────
# ZERO-DIVISOR SEARCH OVER F_p
# ─────────────────────────────────────────────────────────────────

def find_zero_divisor_pairs_two_term(p):
    """
    Find all pairs of two-term imaginary elements (e_a + s1*e_b, e_c + s2*e_d)
    that multiply to zero, for a,b,c,d in {1..15} distinct.

    This matches Moreno's classification: canonical zero-divisors of S
    are pairs of elements of the form (e_a + e_b) with specific index quadruples.

    Over F_p we allow coefficients in F_p, but start with the ±1 case
    which matches the real sedenion canonical pairs exactly.
    """
    pairs = set()

    imag_indices = list(range(1, 16))  # e1..e15

    count = 0
    for a, b in combinations(imag_indices, 2):
        ea = basis_vec(a)
        eb = basis_vec(b)
        for sa in [1, p-1]:   # sa = +1 or -1
            for sb in [1, p-1]:  # sb = +1 or -1
                x = add_vec(scale_vec(ea, sa, p), scale_vec(eb, sb, p), p)
                # x = sa*e_a + sb*e_b
                # Find all y = sc*e_c + sd*e_d such that x*y = 0
                for c, d in combinations(imag_indices, 2):
                    if set([a,b]) == set([c,d]):
                        continue
                    ec = basis_vec(c)
                    ed = basis_vec(d)
                    for sc in [1, p-1]:
                        for sd in [1, p-1]:
                            y = add_vec(scale_vec(ec, sc, p),
                                       scale_vec(ed, sd, p), p)
                            prod = mul_vec(x, y, p)
                            if is_zero(prod, p):
                                # Canonical form: sort indices
                                key = (min(a,b), max(a,b), min(c,d), max(c,d),
                                       sa if a < b else sb,
                                       sb if a < b else sa,
                                       sc if c < d else sd,
                                       sd if c < d else sc)
                                pairs.add(key)
        count += 1
        if count % 20 == 0:
            print(f"  Progress: {count}/{len(imag_indices)*(len(imag_indices)-1)//2} pairs checked, {len(pairs)} zero-div found")

    return pairs


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # First verify the multiplication table over Q (p=large prime as proxy)
    # by checking known octonion sub-algebra properties
    p_test = 10007  # large prime for initial sanity check

    print("\n=== Sanity checks on multiplication table ===")

    # e1*e1 should = -e0 (imaginary units square to -1)
    e1 = basis_vec(1)
    e1sq = mul_vec(e1, e1, p_test)
    expected = [p_test-1, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  # -e0 mod p
    print(f"e1*e1 = {e1sq[:4]}... (expected [{p_test-1},0,0,0,...] = -e0)")
    assert e1sq == expected, f"e1*e1 failed: {e1sq}"

    # e1*e2 = e3 (standard octonion rule for first 8 basis elements)
    e2 = basis_vec(2)
    e3 = basis_vec(3)
    e1e2 = mul_vec(e1, e2, p_test)
    print(f"e1*e2 = basis index with coeff 1 at: {[i for i,v in enumerate(e1e2) if v!=0]}")

    # e0 is identity
    e0 = basis_vec(0)
    for i in range(1, 5):
        ei = basis_vec(i)
        r = mul_vec(e0, ei, p_test)
        assert r == ei, f"e0*e{i} != e{i}"
    print("e0 is identity: OK")

    # All imaginary units square to -e0
    for i in range(1, 16):
        ei = basis_vec(i)
        sq = mul_vec(ei, ei, p_test)
        assert sq[0] == p_test - 1 and all(sq[j]==0 for j in range(1,16)), \
            f"e{i}^2 = {sq}, expected -e0"
    print("All e_i^2 = -e0 (i=1..15): OK")

    # Now work over p=911
    p = 911
    print(f"\n=== Zero-divisor search over F_{p} ===")
    print(f"p = {p}, p mod 455 = {p % 455}, p mod 5={p%5}, p mod 7={p%7}, p mod 13={p%13}")
    print("Searching for canonical two-term zero-divisor pairs...")
    print("(This covers the Moreno/Cawagas canonical form: x=e_a+/-e_b, y=e_c+/-e_d)")

    zd_pairs = find_zero_divisor_pairs_two_term(p)
    print(f"\nTotal canonical zero-divisor (a,b,c,d) quadruples found: {len(zd_pairs)}")

    # Count unordered {(a,b),(c,d)} pairs (canonical pairs per Moreno)
    unordered = set()
    for key in zd_pairs:
        a_idx, b_idx, c_idx, d_idx = key[0], key[1], key[2], key[3]
        canonical = tuple(sorted([(a_idx, b_idx), (c_idx, d_idx)]))
        unordered.add(canonical)

    print(f"Unordered {{(a,b),(c,d)}} canonical pairs: {len(unordered)}")
    print(f"Expected (real sedenions, Moreno 1998): 84")

