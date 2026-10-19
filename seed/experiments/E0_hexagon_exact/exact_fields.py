"""
exact_fields.py -- exact arithmetic used by e0_exact.py (no floating point anywhere
in the decisions; floats appear only when printing a numerical value for a human).

  Z7   : the cyclotomic field Q(zeta), zeta = exp(2 pi i / 7), elements stored as
         (c0..c5)/d with integers c_k, positive integer d, gcd = 1, in the basis
         1, zeta, ..., zeta^5, using zeta^6 = -(1 + zeta + ... + zeta^5).
         Complex conjugation is the field automorphism zeta -> zeta^-1.
  Q5   : the real quadratic field Q(sqrt5), elements a + b sqrt5 with Fractions.
  matrices: tuples of tuples of field elements; generic product / determinant.
  finite groups: closure from generators with exact hashing, words, right-
         multiplication permutations, Cayley table and the usual derived data.
"""
from fractions import Fraction
from math import gcd
import cmath


# ----------------------------------------------------------------------------
# Q(zeta_7)
# ----------------------------------------------------------------------------
class Z7:
    __slots__ = ("c", "d")

    # ---- construction ----
    @staticmethod
    def _make(c, d):
        if d < 0:
            c = tuple(-x for x in c)
            d = -d
        g = gcd(d, *c)
        if g > 1:
            c = tuple(x // g for x in c)
            d //= g
        o = object.__new__(Z7)
        o.c = c
        o.d = d
        return o

    @staticmethod
    def _from7(full, d):
        """full = integer coefficients of zeta^0..zeta^6 (over common denominator d)."""
        c6 = full[6]
        return Z7._make(tuple(full[k] - c6 for k in range(6)), d)

    @staticmethod
    def rat(n, d=1):
        f = Fraction(n, d)
        return Z7._make((f.numerator, 0, 0, 0, 0, 0), f.denominator)

    @staticmethod
    def zeta(k=1):
        full = [0] * 7
        full[k % 7] = 1
        return Z7._from7(full, 1)

    # ---- arithmetic ----
    def __add__(self, o):
        if not isinstance(o, Z7):
            o = Z7.rat(o)
        return Z7._make(tuple(a * o.d + b * self.d for a, b in zip(self.c, o.c)), self.d * o.d)

    __radd__ = __add__

    def __neg__(self):
        return Z7._make(tuple(-a for a in self.c), self.d)

    def __sub__(self, o):
        if not isinstance(o, Z7):
            o = Z7.rat(o)
        return self + (-o)

    def __rsub__(self, o):
        return Z7.rat(o) - self if not isinstance(o, Z7) else o - self

    def __mul__(self, o):
        if not isinstance(o, Z7):
            f = Fraction(o)
            return Z7._make(tuple(a * f.numerator for a in self.c), self.d * f.denominator)
        a, b = self.c, o.c
        full = [0] * 7
        for i in range(6):
            ai = a[i]
            if ai:
                for j in range(6):
                    if b[j]:
                        full[(i + j) % 7] += ai * b[j]
        return Z7._from7(full, self.d * o.d)

    __rmul__ = __mul__

    def galois(self, a):
        """the automorphism sigma_a : zeta -> zeta^a (a = 1..6)."""
        full = [0] * 7
        for k in range(6):
            full[(a * k) % 7] += self.c[k]
        return Z7._from7(full, self.d)

    def conj(self):
        """complex conjugation under zeta = exp(2 pi i/7): sigma_{-1}."""
        return self.galois(6)

    def norm(self):
        """field norm N(x) = prod_a sigma_a(x) (a rational number)."""
        p = Z7.rat(1)
        for a in range(1, 7):
            p = p * self.galois(a)
        assert p.is_rational()
        return p.to_fraction()

    def inv(self):
        if self.is_zero():
            raise ZeroDivisionError
        p = Z7.rat(1)
        for a in range(2, 7):
            p = p * self.galois(a)
        n = (self * p)
        assert n.is_rational()
        return p * (1 / n.to_fraction())

    def __truediv__(self, o):
        if not isinstance(o, Z7):
            return self * (1 / Fraction(o))
        return self * o.inv()

    def __pow__(self, n):
        r = Z7.rat(1)
        b = self
        if n < 0:
            b = b.inv()
            n = -n
        while n:
            if n & 1:
                r = r * b
            b = b * b
            n >>= 1
        return r

    # ---- predicates ----
    def is_zero(self):
        return not any(self.c)

    def is_rational(self):
        return not any(self.c[1:])

    def is_real(self):
        return self == self.conj()

    def to_fraction(self):
        assert self.is_rational()
        return Fraction(self.c[0], self.d)

    def __eq__(self, o):
        if not isinstance(o, Z7):
            o = Z7.rat(o)
        return self.c == o.c and self.d == o.d

    def __hash__(self):
        return hash((self.c, self.d))

    def key(self):
        return self.c + (self.d,)

    # ---- for humans only ----
    def complex(self):
        z = cmath.exp(2j * cmath.pi / 7)
        return sum(ck * z ** k for k, ck in enumerate(self.c)) / self.d

    def __repr__(self):
        terms = []
        for k, ck in enumerate(self.c):
            if ck:
                terms.append(f"{ck}" + ("" if k == 0 else f"z^{k}"))
        s = " + ".join(terms) if terms else "0"
        return f"({s})/{self.d}" if self.d != 1 else f"({s})"


ZERO7, ONE7 = Z7.rat(0), Z7.rat(1)
# quadratic Gauss sum: G = sum_k (k/7) zeta^k ; G^2 = -7 and G = +i sqrt7 under zeta = e^{2 pi i/7}
GAUSS7 = (Z7.zeta(1) + Z7.zeta(2) + Z7.zeta(4)) - (Z7.zeta(3) + Z7.zeta(5) + Z7.zeta(6))


# ----------------------------------------------------------------------------
# Q(sqrt5)
# ----------------------------------------------------------------------------
class Q5:
    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return Q5(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return Q5(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return Q5(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return Q5(self.a * o.a + 5 * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def galois(self):
        return Q5(self.a, -self.b)

    def inv(self):
        n = self.a * self.a - 5 * self.b * self.b
        return Q5(self.a / n, -self.b / n)

    def __truediv__(self, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return self * o.inv()

    def is_rational(self):
        return self.b == 0

    def __eq__(self, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def key(self):
        return (self.a, self.b)

    def value(self):
        return float(self.a) + float(self.b) * 5 ** 0.5

    def __repr__(self):
        return f"({self.a} + {self.b}*sqrt5)"


# ----------------------------------------------------------------------------
# matrices over any of the fields above (or Fractions)
# ----------------------------------------------------------------------------
def mat(rows):
    return tuple(tuple(r) for r in rows)


def mmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return tuple(tuple(sum((A[i][k] * B[k][j] for k in range(1, m)), A[i][0] * B[0][j])
                       for j in range(p)) for i in range(n))


def mvec(A, v):
    return tuple(sum((A[i][k] * v[k] for k in range(1, len(v))), A[i][0] * v[0]) for i in range(len(A)))


def transpose(A):
    return tuple(tuple(A[i][j] for i in range(len(A))) for j in range(len(A[0])))


def conjT(A):
    return tuple(tuple(A[i][j].conj() for i in range(len(A))) for j in range(len(A[0])))


def mconj(A):
    return tuple(tuple(x.conj() for x in r) for r in A)


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def trace(M):
    return sum((M[i][i] for i in range(1, len(M))), M[0][0])


def mkey(M):
    return tuple(x.key() for r in M for x in r)


def identity(n, one, zero):
    return tuple(tuple(one if i == j else zero for j in range(n)) for i in range(n))


# ----------------------------------------------------------------------------
# finite groups from generators
# ----------------------------------------------------------------------------
class FiniteGroup:
    """Closure of generators under a product, with exact hashing.

    elems[i]   : the element (matrix etc.)
    words[i]   : tuple of generator indices with elems[i] = e * g_w1 * g_w2 * ...
    rmul[g][i] : index of elems[i] * gens[g]
    table      : Cayley table, table[i][j] = index of elems[i]*elems[j] (built lazily,
                 exactly, by composing the generator permutations along words[j]).
    """

    def __init__(self, gens, mul, key, ident, cap=100000):
        self.gens = list(gens)
        self.mul, self.key = mul, key
        self.elems = [ident]
        self.index = {key(ident): 0}
        self.words = [()]
        self.rmul = [dict() for _ in gens]
        frontier = [0]
        while frontier:
            new = []
            for i in frontier:
                for gi, g in enumerate(self.gens):
                    N = mul(self.elems[i], g)
                    k = key(N)
                    j = self.index.get(k)
                    if j is None:
                        j = len(self.elems)
                        self.index[k] = j
                        self.elems.append(N)
                        self.words.append(self.words[i] + (gi,))
                        new.append(j)
                        if j > cap:
                            raise RuntimeError("group larger than cap")
                    self.rmul[gi][i] = j
            frontier = new
        self.n = len(self.elems)
        self.rmul = [[r[i] for i in range(self.n)] for r in self.rmul]
        self._table = None

    def __len__(self):
        return self.n

    def find(self, M):
        return self.index.get(self.key(M))

    def contains(self, M):
        return self.key(M) in self.index

    @property
    def table(self):
        if self._table is None:
            n = self.n
            cols = []
            for j in range(n):
                col = list(range(n))
                for g in self.words[j]:
                    r = self.rmul[g]
                    col = [r[x] for x in col]
                cols.append(col)
            self._table = [[cols[j][i] for j in range(n)] for i in range(n)]
            self.e = 0
            self.inv = [row.index(0) for row in self._table]
        return self._table

    # derived data (all from the exact Cayley table)
    def order_of(self, i):
        t = self.table
        k, x = 1, i
        while x != 0:
            x = t[x][i]
            k += 1
        return k

    def conj_classes(self):
        t = self.table
        inv = self.inv
        seen, classes = set(), []
        for x in range(self.n):
            if x in seen:
                continue
            cl = sorted({t[t[g][x]][inv[g]] for g in range(self.n)})
            seen.update(cl)
            classes.append(cl)
        return classes

    def closure(self, idxs):
        """subgroup generated by the given element indices (as a frozenset of indices)."""
        t = self.table
        gens = list(idxs)
        S = {0}
        frontier = [0]
        while frontier:
            new = []
            for x in frontier:
                for g in gens:
                    y = t[x][g]
                    if y not in S:
                        S.add(y)
                        new.append(y)
            frontier = new
        return frozenset(S)

    def conjugate_subgroup(self, H, g):
        t, inv = self.table, self.inv
        return frozenset(t[t[g][h]][inv[g]] for h in H)
