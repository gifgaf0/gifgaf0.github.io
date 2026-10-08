#!/usr/bin/env python3
"""V4.98: the small checks behind the mathematics annotations (one leg each; they confirm facts, not verdicts).

(1) §2.76(b): the quadratic character χ(s), s = (y − 8 − x) mod 7, of the six sum-15 twosets (x, y), x ≤ 7 < y.
(2) §2.53: imaginary units of ℝ, ℂ, ℍ, 𝕆, 𝕊 = dimension − 1.
(3) §4.7: 7₁ = T(2,7) is chiral. Its Jones polynomial, from the torus-knot formula
    V = t^{(p−1)(q−1)/2} (1 − t^{p+1} − t^{q+1} + t^{p+q}) / (1 − t²), is not symmetric under t → 1/t.
(4) C.COSM.2: the sedenions have zero divisors, so they are not a division algebra. The Cayley–Dickson product is
    built from scratch, and a zero product of two nonzero elements e_i ± e_j is exhibited.
(5) C.COSM.4: a trivalent junction at 120° is a vertex of the hexagonal tiling. Degree 3 and corner 120° satisfy the
    angle sum 3 × 120° = 360°; for the triangular tiling, degree 6 at 60°. Arithmetic only.
"""
import json
from fractions import Fraction
out = {}

# (1)
QR = {1, 2, 4}
chi = lambda s: 1 if s % 7 in QR else -1
rows = []
for x in range(1, 8):
    y = 15 - x
    if 9 <= y <= 15:
        s = (y - 8 - x) % 7
        rows.append((x, y, s, chi(s)))
out["sum15"] = rows
assert [r[:2] for r in rows] == [(1, 14), (2, 13), (3, 12), (4, 11), (5, 10), (6, 9)]
assert {(x, y) for x, y, s, c in rows if c == +1} == {(3, 12), (5, 10), (6, 9)}

# (2)
out["imaginaries"] = {a: d - 1 for a, d in (("R", 1), ("C", 2), ("H", 4), ("O", 8), ("S", 16))}
assert [out["imaginaries"][k] for k in "RCHOS"] == [0, 1, 3, 7, 15]

# (3) Laurent polynomials as dicts exponent -> coeff (exponents may be half-integers in general; here integers)
def mul(a, b):
    r = {}
    for i, x in a.items():
        for j, y in b.items():
            r[i + j] = r.get(i + j, 0) + x * y
    return {k: v for k, v in r.items() if v}
def div_by_1_minus_t2(num):
    """exact polynomial division of num by (1 - t^2)"""
    num = dict(num); q = {}
    while num:
        lo = min(num)
        c = num[lo]
        q[lo] = c                                   # c t^lo (1 - t^2) = c t^lo - c t^{lo+2}
        num[lo] -= c
        num[lo + 2] = num.get(lo + 2, 0) + c
        num = {k: v for k, v in num.items() if v}
        assert len(q) < 100
    return q
p, qq = 2, 7
num = {0: 1, p + 1: -1, qq + 1: -1, p + qq: 1}
V = mul({(p - 1) * (qq - 1) // 2: 1}, div_by_1_minus_t2(num))
Vinv = {-k: v for k, v in V.items()}
out["jones_7_1"] = dict(sorted(V.items()))
assert V == {3: 1, 5: 1, 6: -1, 7: 1, 8: -1, 9: 1, 10: -1}, V
assert V != Vinv                                       # not symmetric: chiral

# (4) Cayley–Dickson: (a,b)(c,d) = (ac − d*b, da + bc*), conjugation (a,b)* = (a*, −b)
def conj(x):
    if len(x) == 1: return x[:]
    h = len(x) // 2
    return conj(x[:h]) + [-v for v in x[h:]]
def cd(x, y):
    n = len(x)
    if n == 1: return [x[0] * y[0]]
    h = n // 2
    a, b, c, d = x[:h], x[h:], y[:h], y[h:]
    l = [u - v for u, v in zip(cd(a, c), cd(conj(d), b))]
    r = [u + v for u, v in zip(cd(d, a), cd(b, conj(c)))]
    return l + r
def e(i, n=16):
    v = [0] * n; v[i] = 1; return v
zd = None
for i in range(1, 8):
    for j in range(9, 16):
        for k in range(1, 8):
            for l in range(9, 16):
                for s1 in (1, -1):
                    for s2 in (1, -1):
                        u = [a + s1 * b for a, b in zip(e(i), e(j))]
                        w = [a + s2 * b for a, b in zip(e(k), e(l))]
                        if not any(cd(u, w)):
                            zd = (i, j, s1, k, l, s2); break
                    if zd: break
                if zd: break
            if zd: break
        if zd: break
    if zd: break
assert zd is not None
out["sedenion_zero_divisor"] = "(e%d %s e%d)(e%d %s e%d) = 0" % (zd[0], "+" if zd[2] > 0 else "-", zd[1], zd[3], "+" if zd[5] > 0 else "-", zd[4])
# sanity: the octonions (n = 8) have no such zero product among e_i ± e_j
for i in range(1, 8):
    for j in range(1, 8):
        if i != j:
            for k in range(1, 8):
                for l in range(1, 8):
                    if k != l:
                        for s1 in (1, -1):
                            for s2 in (1, -1):
                                u = [a + s1 * b for a, b in zip(e(i, 8), e(j, 8))]
                                w = [a + s2 * b for a, b in zip(e(k, 8), e(l, 8))]
                                assert any(cd(u, w))

# (5)
out["junctions"] = {"hexagonal": (3, 120, 3 * 120), "triangular": (6, 60, 6 * 60)}
assert out["junctions"]["hexagonal"][2] == 360 and out["junctions"]["triangular"][2] == 360
json.dump(out, open("v498_checks.json", "w"), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(k, ":", v)
print("ALL CHECKS PASS")
