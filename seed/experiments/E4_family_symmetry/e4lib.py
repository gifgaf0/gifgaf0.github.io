"""
e4lib.py -- shared machinery for experiment E4 (the order-21 group on three generations).

* Exact arithmetic in Q(zeta), zeta = exp(2 pi i / 7): an element is an integer vector of
  7 coefficients on 1, zeta, ..., zeta^6 (canonical form: coefficient of zeta^6 is 0, using
  1 + zeta + ... + zeta^6 = 0) divided by 7^e.  Exact 3x3 matrices are stored the same way.
* The seed's matrices, exactly as in ../../hexagon_check.py:
      D  = diag(zeta, zeta^2, zeta^4)
      C  = [[0,1,0],[0,0,1],[1,0,0]]        (the 120-degree Weyl turn)
      R  = Klein's involution  (i/sqrt7) [[z-z^6, z^2-z^5, z^4-z^3], ...]
      flip = -[[0,0,1],[0,1,0],[1,0,0]],  Rf = flip R flip^-1
  F21 = <D, C>,  PSL(2,7) (seed copy) = <D, C, Rf>.
  i/sqrt7 is exact in Q(zeta): i sqrt7 = zeta + zeta^2 + zeta^4 - zeta^3 - zeta^5 - zeta^6
  (quadratic Gauss sum, p = 7 = 3 mod 4), so i/sqrt7 = (that)/7.
* Finite-group utilities: closure, multiplication table, classes, characters,
  intertwiners (Clebsch-Gordan coefficients) by null spaces, number recognition.
"""
import cmath
import itertools
import math

import numpy as np

ZETA = cmath.exp(2j * cmath.pi / 7)
OMEGA = cmath.exp(2j * cmath.pi / 3)
B7 = (-1 + 1j * math.sqrt(7)) / 2          # = zeta + zeta^2 + zeta^4 (ATLAS b7)

# ---------------------------------------------------------------- exact Q(zeta)
_T = np.zeros((7, 7, 7), dtype=np.int64)   # cyclic convolution tensor (zeta^7 = 1)
for _p in range(7):
    for _q in range(7):
        _T[_p, _q, (_p + _q) % 7] = 1


def _canon(num):
    return num - num[..., 6:7]


class XMat:
    """Exact matrix over Q(zeta): value = sum_k num[..., k] zeta^k / 7^e."""
    __slots__ = ("num", "e")

    def __init__(self, num, e=0):
        num = _canon(np.asarray(num, dtype=np.int64))
        while e > 0 and np.all(num % 7 == 0):
            num = num // 7
            e -= 1
        self.num, self.e = num, e

    def __matmul__(self, other):
        num = np.einsum("ikp,kjq,pqm->ijm", self.num, other.num, _T)
        return XMat(num, self.e + other.e)

    def key(self):
        return (self.e,) + tuple(self.num.ravel().tolist())

    def numeric(self):
        pw = ZETA ** np.arange(7)
        return (self.num @ pw) / 7.0 ** self.e

    def trace(self):
        n = self.num.shape[0]
        return XScalar(sum(self.num[i, i] for i in range(n)), self.e)

    def is_identity(self):
        n = self.num.shape[0]
        return self.key() == XMat.identity(n).key()

    def conj(self):
        # zeta^k -> zeta^-k
        num = self.num[..., [(-k) % 7 for k in range(7)]]
        return XMat(num, self.e)

    def T(self):
        return XMat(np.transpose(self.num, (1, 0, 2)), self.e)

    @staticmethod
    def identity(n=3):
        num = np.zeros((n, n, 7), dtype=np.int64)
        for i in range(n):
            num[i, i, 0] = 1
        return XMat(num, 0)


class XScalar:
    __slots__ = ("num", "e")

    def __init__(self, num, e=0):
        num = _canon(np.asarray(num, dtype=np.int64))
        while e > 0 and np.all(num % 7 == 0):
            num = num // 7
            e -= 1
        self.num, self.e = num, e

    def key(self):
        return (self.e,) + tuple(self.num.tolist())

    def numeric(self):
        return complex(np.dot(self.num, ZETA ** np.arange(7)) / 7.0 ** self.e)

    def __eq__(self, other):
        return self.key() == other.key()


def zpow(k):
    v = np.zeros(7, dtype=np.int64)
    v[k % 7] = 1
    return v


def xscalar_from_powers(coeffs, e=0):
    """coeffs: dict power -> integer coefficient."""
    v = np.zeros(7, dtype=np.int64)
    for k, c in coeffs.items():
        v[k % 7] += c
    return XScalar(v, e)


B7_X = xscalar_from_powers({1: 1, 2: 1, 4: 1})          # b7 exactly
B7BAR_X = xscalar_from_powers({3: 1, 5: 1, 6: 1})
GAUSS = {1: 1, 2: 1, 4: 1, 3: -1, 5: -1, 6: -1}         # i sqrt 7


def seed_generators():
    """Exact D, C, R (Klein), flip, Rf exactly as in hexagon_check.py."""
    D = np.zeros((3, 3, 7), dtype=np.int64)
    D[0, 0] = zpow(1)
    D[1, 1] = zpow(2)
    D[2, 2] = zpow(4)
    C = np.zeros((3, 3, 7), dtype=np.int64)
    for (i, j) in ((0, 1), (1, 2), (2, 0)):
        C[i, j, 0] = 1
    # Klein's R = (i/sqrt7) * P where P_ij in {z - z^6, z^2 - z^5, z^4 - z^3}
    a = {1: 1, 6: -1}
    b = {2: 1, 5: -1}
    c = {4: 1, 3: -1}
    P = [[a, b, c], [b, c, a], [c, a, b]]
    # multiply by i sqrt 7 / 7  (i/sqrt7 = i sqrt7 / 7)
    R = np.zeros((3, 3, 7), dtype=np.int64)
    for i in range(3):
        for j in range(3):
            for k1, c1 in P[i][j].items():
                for k2, c2 in GAUSS.items():
                    R[i, j, (k1 + k2) % 7] += c1 * c2
    flip = np.zeros((3, 3, 7), dtype=np.int64)
    for (i, j) in ((0, 2), (1, 1), (2, 0)):
        flip[i, j, 0] = -1
    X = dict(D=XMat(D), C=XMat(C), R=XMat(R, 1), flip=XMat(flip))
    X["Rf"] = X["flip"] @ X["R"] @ X["flip"]          # flip^-1 = flip
    return X


# ---------------------------------------------------------------- groups
def closure(gens):
    """Exact closure.  Returns list of XMat, element 0 is the identity."""
    n = gens[0].num.shape[0]
    I = XMat.identity(n)
    elems = [I]
    index = {I.key(): 0}
    frontier = [I]
    while frontier:
        new = []
        for M in frontier:
            for g in gens:
                N = M @ g
                k = N.key()
                if k not in index:
                    index[k] = len(elems)
                    elems.append(N)
                    new.append(N)
        frontier = new
    return elems, index


class FiniteGroup:
    def __init__(self, gens, names=None):
        self.elems, self.index = closure(gens)
        self.n = len(self.elems)
        self.num = np.array([g.numeric() for g in self.elems])   # (n,3,3) complex
        # multiplication table
        mt = np.empty((self.n, self.n), dtype=np.int64)
        for i, a in enumerate(self.elems):
            for j, b in enumerate(self.elems):
                mt[i, j] = self.index[(a @ b).key()]
        self.mt = mt
        self.inv = np.array([int(np.where(mt[i] == 0)[0][0]) for i in range(self.n)])
        # element orders
        orders = []
        for i in range(self.n):
            k, x = 1, i
            while x != 0:
                x = mt[x, i]
                k += 1
            orders.append(k)
        self.order = np.array(orders)
        # classes
        seen = -np.ones(self.n, dtype=np.int64)
        classes = []
        for i in range(self.n):
            if seen[i] >= 0:
                continue
            cl = sorted({int(mt[mt[g, i], self.inv[g]]) for g in range(self.n)})
            for x in cl:
                seen[x] = len(classes)
            classes.append(cl)
        self.classes = classes
        self.class_of = seen
        self.gen_idx = [self.index[g.key()] for g in gens]

    def idx(self, X):
        return self.index[X.key()]

    def contains(self, X):
        return X.key() in self.index

    def char_from_rep(self, rep):
        """rep: (n, d, d) numeric matrices -> character per class (complex)."""
        tr = np.trace(rep, axis1=1, axis2=2)
        return np.array([tr[cl[0]] for cl in self.classes])

    def inner(self, chi1, chi2):
        sizes = np.array([len(c) for c in self.classes])
        return np.sum(sizes * np.conj(chi1) * chi2) / self.n

    def power_class_map(self, k):
        """class index of g^k for g in each class."""
        out = []
        for cl in self.classes:
            g = cl[0]
            x = 0
            for _ in range(k):
                x = self.mt[x, g]
            out.append(int(self.class_of[x]))
        return np.array(out)

    def check_hom(self, rep, tol=1e-9):
        """max |rho(a) rho(b) - rho(ab)| over all pairs (vectorised in chunks)."""
        err = 0.0
        for i in range(self.n):
            prod = np.einsum("ab,jbc->jac", rep[i], rep)
            err = max(err, np.max(np.abs(prod - rep[self.mt[i]])))
        return err


# ---------------------------------------------------------------- linear algebra
def nullspace(A, tol=1e-9):
    if A.shape[0] == 0:
        return np.eye(A.shape[1], dtype=complex)
    u, s, vh = np.linalg.svd(A)
    rank = int(np.sum(s > tol * max(1.0, s[0] if len(s) else 1.0)))
    return vh[rank:].conj().T


def invariants(reps, gens_idx, tol=1e-9):
    """Basis (columns) of vectors fixed by kron(reps...)(g) for generators g."""
    blocks = []
    for gi in gens_idx:
        M = np.array([[1.0 + 0j]])
        for r in reps:
            M = np.kron(M, r[gi])
        blocks.append(M - np.eye(M.shape[0]))
    return nullspace(np.vstack(blocks), tol)


def intertwiners(rep_src, rep_tgt, gens_idx, tol=1e-9):
    """All K (dim_src x dim_tgt) with rep_src(g) K = K rep_tgt(g).  Returns list of K."""
    ds, dt = rep_src.shape[1], rep_tgt.shape[1]
    rows = []
    for gi in gens_idx:
        A = rep_src[gi]
        B = rep_tgt[gi]
        # vec(A K - K B) = (I_dt kron A - B^T kron I_ds) vec(K)   (column-major vec)
        rows.append(np.kron(np.eye(dt), A) - np.kron(B.T, np.eye(ds)))
    N = nullspace(np.vstack(rows), tol)
    Ks = [N[:, k].reshape((dt, ds)).T for k in range(N.shape[1])]
    return Ks


def rref(M, tol=1e-9):
    M = M.astype(complex).copy()
    r = 0
    rows, cols = M.shape
    for c in range(cols):
        if r >= rows:
            break
        p = r + int(np.argmax(np.abs(M[r:, c])))
        if abs(M[p, c]) < tol:
            continue
        M[[r, p]] = M[[p, r]]
        M[r] /= M[r, c]
        for k in range(rows):
            if k != r:
                M[k] -= M[k, c] * M[r]
        r += 1
    M[np.abs(M) < tol] = 0
    return M[:r]


# ---------------------------------------------------------------- number recognition
def recognize(z, tol=1e-8, maxden=84):
    """Express z as sqrt(p/q) * exp(2 pi i k/84) (k, p, q small) or a known constant."""
    if abs(z) < tol:
        return "0"
    named = {"b7": B7, "conj(b7)": B7.conjugate(), "w": OMEGA, "w^2": OMEGA ** 2}
    for s, v in named.items():
        if abs(z - v) < tol:
            return s
    r2 = abs(z) ** 2
    from fractions import Fraction
    fr = Fraction(r2).limit_denominator(200)
    if abs(float(fr) - r2) > 1e-7:
        return f"{z.real:+.6f}{z.imag:+.6f}i"
    ph = cmath.phase(z) / (2 * math.pi) * maxden
    k = round(ph) % maxden
    if abs(ph - round(ph)) > 1e-6:
        return f"{z.real:+.6f}{z.imag:+.6f}i"
    mag = "1" if fr == 1 else (f"sqrt({fr})" if fr.denominator != 1 or int(math.isqrt(fr.numerator)) ** 2 != fr.numerator else str(math.isqrt(fr.numerator)))
    if k == 0:
        return mag
    if k == maxden // 2:
        return "-" + mag
    g = math.gcd(k, maxden)
    return f"{mag}*e^(2pi i {k // g}/{maxden // g})"


def recognize_char(z, tol=1e-9):
    for s, v in (("b7", B7), ("conj(b7)", B7.conjugate()), ("w", OMEGA), ("w^2", OMEGA ** 2)):
        if abs(z - v) < tol:
            return s
    if abs(z.imag) < tol and abs(z.real - round(z.real)) < tol:
        return str(int(round(z.real)))
    return f"{z:.6f}"


# ---------------------------------------------------------------- mixing utilities
def pdg_matrix(s12sq, s13sq, s23sq, delta):
    s12, s13, s23 = np.sqrt([s12sq, s13sq, s23sq])
    c12, c13, c23 = np.sqrt([1 - s12sq, 1 - s13sq, 1 - s23sq])
    e = np.exp(1j * delta)
    return np.array([
        [c12 * c13, s12 * c13, s13 / e],
        [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
        [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])


def angles_from_U(U):
    """PDG-convention observables from a unitary matrix (rephasing invariant).
    Returns s12^2, s13^2, s23^2, delta (rad, in [0, 2pi)), J."""
    A = np.abs(U) ** 2
    s13sq = A[0, 2]
    c13sq = 1 - s13sq
    s12sq = A[0, 1] / c13sq if c13sq > 1e-15 else 0.0
    s23sq = A[1, 2] / c13sq if c13sq > 1e-15 else 0.0
    J = np.imag(U[1, 2] * np.conj(U[0, 2]) * U[0, 1] * np.conj(U[1, 1]))
    s12, s13, s23 = np.sqrt([s12sq, s13sq, s23sq])
    c12, c23 = np.sqrt([max(0.0, 1 - s12sq), max(0.0, 1 - s23sq)])
    c13 = np.sqrt(c13sq)
    denom = 2 * s12 * c12 * s23 * c23 * s13
    if denom > 1e-14:
        cosd = (A[1, 0] - s12sq * c23 ** 2 - c12 ** 2 * s23sq * s13sq) / denom
        sind = J / (denom / 2 * c13sq) if c13sq > 0 else 0.0
        delta = math.atan2(sind, np.clip(cosd, -1, 1)) % (2 * math.pi)
    else:
        delta = float("nan")
    return s12sq, s13sq, s23sq, delta, J


def wolfenstein_from_V(V):
    """lambda, A, rhobar, etabar from a CKM-like unitary matrix (rephasing invariant)."""
    V = np.where(np.abs(V) < 1e-12, 0, V)
    a11, a12, a23 = abs(V[0, 0]), abs(V[0, 1]), abs(V[1, 2])
    if a11 ** 2 + a12 ** 2 < 1e-24:
        return float("nan"), float("nan"), float("nan"), float("nan")
    lam = a12 / math.sqrt(a11 ** 2 + a12 ** 2)
    A = a23 / (lam ** 2 * math.sqrt(a11 ** 2 + a12 ** 2)) if lam > 0 else float("inf")
    den = V[1, 0] * np.conj(V[1, 2])
    if abs(den) < 1e-15:
        z = complex("nan")
    else:
        z = -V[0, 0] * np.conj(V[0, 2]) / den
    return lam, A, z.real, z.imag
