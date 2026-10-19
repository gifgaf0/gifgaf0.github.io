"""
xc2_lib.py -- helpers for the second-round E0 cross-check (xc2_e0.py).

Written without reading the original E0 scripts.  Methods chosen to differ from
both the original (hand-written Q(zeta7) class, BFS closure, Cayley table) and
the earlier cross-check pass (Q[Z7] class, mod-p Schreier-Sims, Todd-Coxeter):

  * Q(zeta7) is sympy's AlgebraicField QQ<exp(2 pi i/7)> (dense polynomials
    modulo the minimal polynomial that sympy itself computes), i.e. the
    preregistered "sympy over Q(zeta7)" route.
  * Group orders: exact orbit-stabiliser chain on PROJECTIVE POINTS of K^3
    (base [e1],[e2],[e3],[1:1:1], Schreier generators), no full enumeration.
  * Isomorphism type: explicit isomorphism onto PSL(2,F7) acting on P^1(F7),
    built from the conjugation action on Sylow-7 subgroups.
  * Q(sqrt5): pairs of Fractions; the icosahedral group is found by brute force
    as the rotations that permute the 12 vertices (orbit-stabiliser 12 x 5).
  * Lattices / Weyl groups: integer and Fraction 2x2 matrices in the basis
    b1 = (1,-1,0), b2 = (0,1,-1) of Lambda.
"""
from fractions import Fraction
import itertools

import sympy as sp
from sympy import QQ

# ---------------------------------------------------------------- Q(zeta7)
ZETA_SYM = sp.exp(2 * sp.pi * sp.I / 7)
K = QQ.algebraic_field(ZETA_SYM)
Z = K.from_sympy(ZETA_SYM)
K0, K1 = K.zero, K.one
_ZP = [K1]
for _ in range(13):
    _ZP.append(_ZP[-1] * Z)


def zp(k):
    """zeta^k"""
    return _ZP[k % 7]


def kint(n):
    return K(n)


def kcoeffs(e):
    """coefficients c_0..c_5 of e = sum c_k zeta^k (sympy stores highest first)"""
    lst = list(e.to_list())[::-1]
    return lst + [0] * (6 - len(lst))


def kconj(e):
    """complex conjugation = the Galois automorphism zeta -> zeta^-1"""
    out = K0
    for k, c in enumerate(kcoeffs(e)):
        if c:
            out = out + K(c) * zp(-k)
    return out


def kgal(e, a):
    """Galois automorphism zeta -> zeta^a"""
    out = K0
    for k, c in enumerate(kcoeffs(e)):
        if c:
            out = out + K(c) * zp(a * k)
    return out


def kfloat(e):
    import cmath
    return sum(complex(float(c)) * cmath.exp(2j * cmath.pi * k / 7) for k, c in enumerate(kcoeffs(e)))


def kkey(e):
    return e.to_tuple()


# ---------------------------------------------------------------- 3x3 matrices over K (tuples of 9)
def M(rows):
    return tuple(rows[i][j] if not isinstance(rows[i][j], int) else K(rows[i][j]) for i in range(3) for j in range(3))


IDENT = M([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


def mmul(A, B):
    return tuple(A[3 * i] * B[j] + A[3 * i + 1] * B[3 + j] + A[3 * i + 2] * B[6 + j]
                 for i in range(3) for j in range(3))


def mapply(A, v):
    return tuple(A[3 * i] * v[0] + A[3 * i + 1] * v[1] + A[3 * i + 2] * v[2] for i in range(3))


def mscal(s, A):
    return tuple(s * a for a in A)


def mconj(A):
    return tuple(kconj(a) for a in A)


def mtrans(A):
    return tuple(A[3 * j + i] for i in range(3) for j in range(3))


def mdag(A):
    return mconj(mtrans(A))


def mdet(A):
    a, b, c, d, e, f, g, h, i = A
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def madj(A):
    a, b, c, d, e, f, g, h, i = A
    return (e * i - f * h, c * h - b * i, b * f - c * e,
            f * g - d * i, a * i - c * g, c * d - a * f,
            d * h - e * g, b * g - a * h, a * e - b * d)


def minv(A):
    d = mdet(A)
    return mscal(K1 / d, madj(A))


def mkey(A):
    return tuple(kkey(a) for a in A)


def mtrace(A):
    return A[0] + A[4] + A[8]


def mpow(A, n):
    R = IDENT
    for _ in range(n):
        R = mmul(R, A)
    return R


def morder(A, cap=200):
    R = A
    for n in range(1, cap + 1):
        if R == IDENT:
            return n
        R = mmul(R, A)
    return None


def in_SU3(A):
    return mmul(A, mdag(A)) == IDENT and mdet(A) == K1


# ---------------------------------------------------------------- projective orbit-stabiliser chain
def proj_norm(v):
    for c in v:
        if c != K0:
            inv = K1 / c
            return tuple(x * inv for x in v)
    raise ValueError("zero vector")


def proj_key(v):
    return tuple(kkey(x) for x in proj_norm(v))


def stabiliser_chain_order(gens, base=None):
    """|<gens>| by an exact orbit-stabiliser chain on projective points of K^3.

    For each base point b: orbit of [b] under the current group, a transversal,
    and the Schreier generators u_{g x}^-1 g u_x of the stabiliser.  After the
    projective frame [e1],[e2],[e3],[1:1:1] the remaining group consists of
    scalar matrices, enumerated directly.  Returns (order, orbit_sizes)."""
    if base is None:
        base = [(K1, K0, K0), (K0, K1, K0), (K0, K0, K1), (K1, K1, K1)]
    cur = list({mkey(g): g for g in gens if g != IDENT}.values())
    sizes = []
    for b in base:
        bk = proj_key(b)
        trans = {bk: IDENT}
        pts = {bk: proj_norm(b)}
        queue = [bk]
        while queue:
            xk = queue.pop()
            x = pts[xk]
            for g in cur:
                y = mapply(g, x)
                yk = proj_key(y)
                if yk not in trans:
                    trans[yk] = mmul(g, trans[xk])
                    pts[yk] = proj_norm(y)
                    queue.append(yk)
        sizes.append(len(trans))
        sch = {}
        for xk, u in trans.items():
            for g in cur:
                yk = proj_key(mapply(g, pts[xk]))
                s = mmul(minv(trans[yk]), mmul(g, u))
                if s != IDENT:
                    sch[mkey(s)] = s
        cur = list(sch.values())
    # remaining group: scalars (each generator must be scalar)
    for g in cur:
        assert g[1] == g[2] == g[3] == g[5] == g[6] == g[7] == K0 and g[0] == g[4] == g[8], "not scalar"
    scal = closure(cur) if cur else [IDENT]
    sizes.append(len(scal))
    order = 1
    for s in sizes:
        order *= s
    return order, sizes


def closure(gens):
    """all elements of <gens> (BFS, right multiplication by generators)"""
    seen = {mkey(IDENT): IDENT}
    frontier = [IDENT]
    while frontier:
        new = []
        for A in frontier:
            for g in gens:
                B = mmul(A, g)
                k = mkey(B)
                if k not in seen:
                    seen[k] = B
                    new.append(B)
        frontier = new
    return list(seen.values())


# ---------------------------------------------------------------- permutations (tuples)
def pmul(a, b):
    """(a*b)(x) = a(b(x)) -- apply b first"""
    return tuple(a[x] for x in b)


def pinv(a):
    r = [0] * len(a)
    for i, x in enumerate(a):
        r[x] = i
    return tuple(r)


def pclosure(gens, n):
    e = tuple(range(n))
    seen = {e}
    frontier = [e]
    while frontier:
        new = []
        for a in frontier:
            for g in gens:
                b = pmul(g, a)
                if b not in seen:
                    seen.add(b)
                    new.append(b)
        frontier = new
    return frozenset(seen)


def porder(a):
    e = tuple(range(len(a)))
    b, n = a, 1
    while b != e:
        b = pmul(a, b)
        n += 1
    return n


def pclasses(G):
    G = list(G)
    left = set(G)
    out = []
    while left:
        g = next(iter(left))
        cl = {pmul(pmul(h, g), pinv(h)) for h in G}
        out.append(frozenset(cl))
        left -= cl
    return out


# ---------------------------------------------------------------- PSL(2,7) on P^1(F7): points 0..6 and 7 = infinity
INF = 7


def mobius(a, b, c, d):
    """x -> (a x + b)/(c x + d) over F7 as a permutation of 0..7"""
    out = []
    for x in range(8):
        if x == INF:
            num, den = a, c
        else:
            num, den = (a * x + b) % 7, (c * x + d) % 7
        if den % 7 == 0:
            out.append(INF)
        else:
            out.append(num * pow(den, 5, 7) % 7)
    return tuple(out)


def psl27_standard():
    """all x -> (ax+b)/(cx+d) with ad - bc = 1 over F7, as permutations of P^1(F7)"""
    S = set()
    for a, b, c, d in itertools.product(range(7), repeat=4):
        if (a * d - b * c) % 7 == 1:
            S.add(mobius(a, b, c, d))
    return frozenset(S)


# ---------------------------------------------------------------- Q(sqrt5) as (a, b) = a + b sqrt5
class Q5:
    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a, self.b = Fraction(a), Fraction(b)

    def __add__(s, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return Q5(s.a + o.a, s.b + o.b)

    __radd__ = __add__

    def __neg__(s):
        return Q5(-s.a, -s.b)

    def __sub__(s, o):
        return s + (-(o if isinstance(o, Q5) else Q5(o)))

    def __rsub__(s, o):
        return Q5(o) - s

    def __mul__(s, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)

    __rmul__ = __mul__

    def inv(s):
        n = s.a * s.a - 5 * s.b * s.b
        return Q5(s.a / n, -s.b / n)

    def __truediv__(s, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return s * o.inv()

    def __eq__(s, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def gal(s):
        return Q5(s.a, -s.b)

    def __repr__(s):
        return f"({s.a}{'+' if s.b >= 0 else '-'}{abs(s.b)}*sqrt5)"


def q5det(A):
    (a, b, c), (d, e, f), (g, h, i) = A
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def q5mul(A, B):
    return tuple(tuple(sum((A[i][k] * B[k][j] for k in range(3)), Q5(0)) for j in range(3)) for i in range(3))


def q5inv(A):
    (a, b, c), (d, e, f), (g, h, i) = A
    adj = ((e * i - f * h, c * h - b * i, b * f - c * e),
           (f * g - d * i, a * i - c * g, c * d - a * f),
           (d * h - e * g, b * g - a * h, a * e - b * d))
    dinv = q5det(A).inv()
    return tuple(tuple(x * dinv for x in row) for row in adj)


def q5apply(A, v):
    return tuple(sum((A[i][k] * v[k] for k in range(3)), Q5(0)) for i in range(3))


def q5T(A):
    return tuple(tuple(A[j][i] for j in range(3)) for i in range(3))


def q5cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def q5dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


# ---------------------------------------------------------------- exact linear algebra over Q (Fractions)
def nullspace_dim(rows, ncols):
    """dimension of the nullspace of a rational matrix given as a list of rows"""
    A = [[Fraction(x) for x in r] for r in rows]
    rank, col = 0, 0
    m = len(A)
    while rank < m and col < ncols:
        piv = next((r for r in range(rank, m) if A[r][col] != 0), None)
        if piv is None:
            col += 1
            continue
        A[rank], A[piv] = A[piv], A[rank]
        pv = A[rank][col]
        A[rank] = [x / pv for x in A[rank]]
        for r in range(m):
            if r != rank and A[r][col] != 0:
                f = A[r][col]
                A[r] = [x - f * y for x, y in zip(A[r], A[rank])]
        rank += 1
        col += 1
    return ncols - rank


def nullspace(rows, ncols):
    """basis of the nullspace (list of Fraction vectors)"""
    A = [[Fraction(x) for x in r] for r in rows]
    m = len(A)
    pivcols = []
    rank = 0
    for col in range(ncols):
        piv = next((r for r in range(rank, m) if A[r][col] != 0), None)
        if piv is None:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        pv = A[rank][col]
        A[rank] = [x / pv for x in A[rank]]
        for r in range(m):
            if r != rank and A[r][col] != 0:
                f = A[r][col]
                A[r] = [x - f * y for x, y in zip(A[r], A[rank])]
        pivcols.append(col)
        rank += 1
        if rank == m:
            break
    free = [c for c in range(ncols) if c not in pivcols]
    basis = []
    for fc in free:
        v = [Fraction(0)] * ncols
        v[fc] = Fraction(1)
        for r, pc in enumerate(pivcols):
            v[pc] = -A[r][fc]
        basis.append(v)
    return basis


def rank_of(rows, ncols):
    return ncols - nullspace_dim(rows, ncols)
