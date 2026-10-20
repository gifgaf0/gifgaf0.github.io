"""
xc_lib.py -- independent tools for the E0 cross-check (written without reading
the original E0 scripts).

Representations used here (deliberately different from the original E0 code,
which works in a 6-dim basis 1..zeta^5 of Q(zeta7) and closes groups by BFS
over exact matrices):

* Q(zeta7) as the group algebra Q[Z7] modulo the all-ones vector:
  an element is a 7-tuple of Fractions (c_0..c_6) meaning sum c_k zeta^k,
  canonicalised by subtracting c_0*(1,...,1) (so c_0 = 0; basis zeta..zeta^6).
* Reduction mod a prime p = 1 (mod 7): zeta -> a primitive 7th root of unity in
  F_p.  Matrix groups are then turned into permutation groups (action on the
  orbit of e1, e2, e3 in F_p^3) and handled with a deterministic
  Schreier-Sims algorithm written here.
* Todd-Coxeter coset enumeration (HLT with coincidences) for presentations.
* Q(sqrt5) as pairs of Fractions (a, b) = a + b sqrt5.
"""
from fractions import Fraction as Fr
from collections import deque

# --------------------------------------------------------------------------
# Q(zeta7) as Q[Z7]/(1+x+...+x^6)
# --------------------------------------------------------------------------
N7 = 7


class Z7:
    __slots__ = ("c",)

    def __init__(self, coeffs=None):
        if coeffs is None:
            coeffs = [0] * 7
        c = [Fr(x) for x in coeffs]
        c0 = c[0]
        if c0:
            c = [x - c0 for x in c]
        self.c = tuple(c)

    @staticmethod
    def zeta(k=1):
        v = [0] * 7
        v[k % 7] = 1
        return Z7(v)

    @staticmethod
    def const(q):
        # q = q*1 ; 1 = -(zeta+...+zeta^6)
        return Z7([q] + [0] * 6)

    def __add__(self, o):
        if not isinstance(o, Z7):
            o = Z7.const(o)
        return Z7([a + b for a, b in zip(self.c, o.c)])

    __radd__ = __add__

    def __neg__(self):
        return Z7([-a for a in self.c])

    def __sub__(self, o):
        if not isinstance(o, Z7):
            o = Z7.const(o)
        return self + (-o)

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if not isinstance(o, Z7):
            o = Fr(o)
            return Z7([a * o for a in self.c])
        r = [Fr(0)] * 7
        for i, a in enumerate(self.c):
            if a:
                for j, b in enumerate(o.c):
                    if b:
                        r[(i + j) % 7] += a * b
        return Z7(r)

    __rmul__ = __mul__

    def __eq__(self, o):
        if not isinstance(o, Z7):
            o = Z7.const(o)
        return self.c == o.c

    def __hash__(self):
        return hash(self.c)

    def is_zero(self):
        return all(x == 0 for x in self.c)

    def conj(self):
        # complex conjugation = Galois automorphism zeta -> zeta^-1
        r = [Fr(0)] * 7
        for k, a in enumerate(self.c):
            r[(-k) % 7] += a
        return Z7(r)

    def galois(self, a):
        r = [Fr(0)] * 7
        for k, x in enumerate(self.c):
            r[(a * k) % 7] += x
        return Z7(r)

    def is_rational(self):
        # rational iff c_1 = ... = c_6 (then value = -c_1)
        return len(set(self.c[1:])) == 1

    def rational_value(self):
        assert self.is_rational()
        return -self.c[1]

    def to_complex(self):
        import cmath
        z = cmath.exp(2j * cmath.pi / 7)
        return sum(complex(float(a)) * z ** k for k, a in enumerate(self.c))

    def modp(self, p, w):
        s = 0
        for k, a in enumerate(self.c):
            if a:
                s += a.numerator * pow(a.denominator, -1, p) * pow(w, k, p)
        return s % p

    def __repr__(self):
        return "Z7(" + ",".join(str(x) for x in self.c[1:]) + ")"


ZERO = Z7()
ONE = Z7.const(1)
z = [Z7.zeta(k) for k in range(7)]
# quadratic Gauss sum, G^2 = -7 ; numerically G = +i sqrt7
G = z[1] + z[2] + z[4] - z[3] - z[5] - z[6]
I_OVER_SQRT7 = G * Fr(1, 7)          # = i/sqrt7  (since i/sqrt7 = i/(G/i) = -1/G = G/7)
B7 = z[1] + z[2] + z[4]


# 3x3 matrices over Z7 ------------------------------------------------------
def mat(rows):
    return tuple(tuple(x if isinstance(x, Z7) else Z7.const(x) for x in r) for r in rows)


def mmul(A, B):
    return tuple(tuple(sum((A[i][k] * B[k][j] for k in range(3)), ZERO) for j in range(3))
                 for i in range(3))


def mscale(A, s):
    return tuple(tuple(x * s for x in r) for r in A)


def mconj(A):
    return tuple(tuple(x.conj() for x in r) for r in A)


def mdagger(A):
    return tuple(tuple(A[j][i].conj() for j in range(3)) for i in range(3))


def mdet(A):
    a = A
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def mtrace(A):
    return A[0][0] + A[1][1] + A[2][2]


ID3 = mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


def meq(A, B):
    return all(A[i][j] == B[i][j] for i in range(3) for j in range(3))


def mpow(A, n):
    R = ID3
    for _ in range(n):
        R = mmul(R, A)
    return R


def in_SU3(A):
    return meq(mmul(A, mdagger(A)), ID3) and mdet(A) == ONE


def mmodp(A, p, w):
    return tuple(tuple(x.modp(p, w) for x in r) for r in A)


def eval_word(word, gens, mul, ident):
    """word: list of (index, power) or list of indices; gens: list of elements."""
    R = ident
    for t in word:
        R = mul(R, gens[t])
    return R


# --------------------------------------------------------------------------
# finite field matrices and permutation representation
# --------------------------------------------------------------------------
def prim7(p):
    assert (p - 1) % 7 == 0
    for g in range(2, p):
        w = pow(g, (p - 1) // 7, p)
        if w != 1:
            return w
    raise ValueError


def fmul(A, B, p):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) % p for j in range(3)) for i in range(3))


def fapply(A, v, p):
    return tuple(sum(A[i][k] * v[k] for k in range(3)) % p for i in range(3))


def perm_rep(mats, p):
    """Faithful permutation representation of <mats> on the orbit(s) of e1,e2,e3."""
    E = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    pts = []
    index = {}
    q = deque()
    for e in E:
        if e not in index:
            index[e] = len(pts)
            pts.append(e)
            q.append(e)
    while q:
        v = q.popleft()
        for M in mats:
            u = fapply(M, v, p)
            if u not in index:
                index[u] = len(pts)
                pts.append(u)
                q.append(u)
    perms = []
    for M in mats:
        perms.append(tuple(index[fapply(M, v, p)] for v in pts))
    return pts, index, perms


def perm_of_matrix(M, pts, index, p):
    """Permutation induced by a mod-p matrix on the domain, or None if it does not preserve it."""
    out = []
    for v in pts:
        u = fapply(M, v, p)
        if u not in index:
            return None
        out.append(index[u])
    return tuple(out)


# permutations: tuple p, p[i] = image of i ; product a*b = "a then b"
def pmul(a, b):
    return tuple(b[x] for x in a)


def pinv(a):
    r = [0] * len(a)
    for i, x in enumerate(a):
        r[x] = i
    return tuple(r)


def pid(n):
    return tuple(range(n))


def pcomp(a, b):
    """function composition a o b (apply b first): matches matrix products, perm(MN) = perm(M) o perm(N)."""
    return tuple(a[j] for j in b)


def porder(a):
    e = pid(len(a))
    k, x = 1, a
    while x != e:
        x = pmul(x, a)
        k += 1
    return k


class BSGS:
    """Deterministic Schreier-Sims (Holt, Handbook of CGT, alg. SCHREIERSIMS)."""

    def __init__(self, gens, n):
        self.n = n
        self.e = pid(n)
        self.B = []
        self.T = []          # strong generators
        gens = [g for g in gens if g != self.e]
        for g in gens:
            if all(g[b] == b for b in self.B):
                self.B.append(next(i for i in range(n) if g[i] != i))
            self.T.append(g)
        self.U = [None] * len(self.B)
        for i in range(len(self.B)):
            self._orbit(i)
        i = len(self.B) - 1
        while i >= 0:
            restart = False
            Si = self._S(i)
            for x, ux in list(self.U[i].items()):
                for s in Si:
                    y = s[x]
                    h = pmul(pmul(ux, s), pinv(self.U[i][y]))
                    r, j = self.strip(h, i + 1)
                    if r != self.e:
                        if j == len(self.B):
                            self.B.append(next(k for k in range(n) if r[k] != k))
                            self.U.append(None)
                        self.T.append(r)
                        for l in range(i + 1, j + 1):
                            self._orbit(l)
                        i = j
                        restart = True
                        break
                if restart:
                    break
            if not restart:
                i -= 1

    def _S(self, i):
        return [t for t in self.T if all(t[b] == b for b in self.B[:i])]

    def _orbit(self, i):
        b = self.B[i]
        S = self._S(i)
        U = {b: self.e}
        q = deque([b])
        while q:
            x = q.popleft()
            for s in S:
                y = s[x]
                if y not in U:
                    U[y] = pmul(U[x], s)
                    q.append(y)
        self.U[i] = U

    def strip(self, g, start=0):
        for i in range(start, len(self.B)):
            x = g[self.B[i]]
            if x not in self.U[i]:
                return g, i
            g = pmul(g, pinv(self.U[i][x]))
        return g, len(self.B)

    def order(self):
        o = 1
        for U in self.U:
            o *= len(U)
        return o

    def contains(self, g):
        r, j = self.strip(g)
        return r == self.e and j == len(self.B)


def bfs_elements(gens, ident, mul):
    """All elements with a shortest word (list of generator indices)."""
    words = {ident: []}
    q = deque([ident])
    while q:
        x = q.popleft()
        for k, g in enumerate(gens):
            y = mul(x, g)
            if y not in words:
                words[y] = words[x] + [k]
                q.append(y)
    return words


def conj_classes(elems):
    """elems: list of permutations forming a group."""
    seen = set()
    classes = []
    for g in elems:
        if g in seen:
            continue
        cl = set()
        for h in elems:
            cl.add(pmul(pmul(pinv(h), g), h))
        seen |= cl
        classes.append(cl)
    return classes


def closure(gens, n):
    e = pid(n)
    S = {e}
    q = deque([e])
    while q:
        x = q.popleft()
        for g in gens:
            y = pmul(x, g)
            if y not in S:
                S.add(y)
                q.append(y)
    return frozenset(S)


# --------------------------------------------------------------------------
# Todd-Coxeter (HLT with coincidences; Holt et al., Handbook of CGT, ch. 5)
# --------------------------------------------------------------------------
def todd_coxeter(ngens, relators, subgens=(), max_cosets=200000):
    """Generators 0..ngens-1; letter 2k = gen k, 2k+1 = its inverse.
    relators / subgens: lists of letters.  Returns the index of <subgens>."""
    ncols = 2 * ngens
    inv = [c ^ 1 for c in range(ncols)]
    table = [[None] * ncols]
    p = [0]

    def rep(c):
        r = c
        while p[r] != r:
            r = p[r]
        while p[c] != r:
            p[c], c = r, p[c]
        return r

    def define(c, x):
        if len(table) >= max_cosets:
            raise RuntimeError("coset limit")
        n = len(table)
        table.append([None] * ncols)
        p.append(n)
        table[c][x] = n
        table[n][inv[x]] = c

    def merge(k, l, q):
        k, l = rep(k), rep(l)
        if k != l:
            m, n = min(k, l), max(k, l)
            p[n] = m
            q.append(n)

    def coincidence(a, b):
        q = []
        merge(a, b, q)
        i = 0
        while i < len(q):
            e = q[i]
            i += 1
            for x in range(ncols):
                f = table[e][x]
                if f is not None:
                    table[f][inv[x]] = None
                    e1, f1 = rep(e), rep(f)
                    if table[e1][x] is not None:
                        merge(f1, table[e1][x], q)
                    elif table[f1][inv[x]] is not None:
                        merge(e1, table[f1][inv[x]], q)
                    else:
                        table[e1][x] = f1
                        table[f1][inv[x]] = e1

    def scan_and_fill(c, w):
        f, b = c, c
        i, j = 0, len(w) - 1
        while True:
            while i <= j and table[f][w[i]] is not None:
                f = table[f][w[i]]
                i += 1
            if i > j:
                if f != b:
                    coincidence(f, b)
                return
            while j >= i and table[b][inv[w[j]]] is not None:
                b = table[b][inv[w[j]]]
                j -= 1
            if j < i:
                coincidence(f, b)
                return
            elif i == j:
                table[f][w[i]] = b
                table[b][inv[w[i]]] = f
                return
            else:
                define(f, w[i])

    for w in subgens:
        scan_and_fill(0, w)
    c = 0
    while c < len(table):
        if p[c] == c:
            for r in relators:
                scan_and_fill(c, r)
                if p[c] != c:
                    break
            if p[c] == c:
                for x in range(ncols):
                    if table[c][x] is None:
                        define(c, x)
        c += 1
    return sum(1 for c in range(len(table)) if p[c] == c)


def word_letters(s, names):
    """'aB' -> letters; lower case = generator, upper case = inverse."""
    out = []
    for ch in s:
        k = names.index(ch.lower())
        out.append(2 * k + (1 if ch.isupper() else 0))
    return out


# --------------------------------------------------------------------------
# Q(sqrt5)
# --------------------------------------------------------------------------
class Q5:
    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a, self.b = Fr(a), Fr(b)

    def __add__(self, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return Q5(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return self + (-o)

    def __mul__(self, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return Q5(self.a * o.a + 5 * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def __eq__(self, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def gal(self):
        return Q5(self.a, -self.b)

    def __repr__(self):
        return f"({self.a}{'+' if self.b >= 0 else '-'}{abs(self.b)}*sqrt5)"
