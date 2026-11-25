"""EXPLORATORY general-Q0 fixed-lambda cumulant engine (matrix form).

c_0 = (1/phi) chi^T (lam M0) chi,         M0 = Sh (I - a Sh)^{-1}
c_k = (1/phi) lam (-lam)^{k-2} chi^T P G_k P chi,   P = I - lam M0   (P 1 = 0, 1^T P = 0)
(G_k)_{R,R'} = sum over (s_1..s_{k-1}) >= 1, s = sum s_i, R' = R + s steps:
               a^{s-k+1} Delta_k(points 0, off_R(S_1), ..., off_R(S_{k-1}))
Delta_k = Moebius cumulant of the singular series over p not dividing Q0.
Positions are kept in half-units (all differences even; odd p | d <=> p | d/2).
"""
import math, itertools
import numpy as np

_PC = {}
def primes_upto(n):
    if n in _PC: return _PC[n]
    s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, int(n ** .5) + 1):
        if s[i]: s[i * i::i] = False
    _PC[n] = np.nonzero(s)[0]; return _PC[n]

def odd_prime_factors(n):
    f = set(); d = 3
    while n % 2 == 0: n //= 2
    while d * d <= n:
        while n % d == 0: f.add(d); n //= d
        d += 2
    if n > 1: f.add(n)
    return f

_CK = {}
def Ck(k, excl, pmax=2_000_000):
    key = (k, tuple(sorted(excl)), pmax)
    if key not in _CK:
        ps = primes_upto(pmax).astype(float); ps = ps[(ps >= 7) & ~np.isin(ps, list(excl))]
        _CK[key] = float(np.exp(np.sum(np.log1p(-k / ps) - k * np.log1p(-1.0 / ps))))
    return _CK[key]

def S_subsets(pts, subsets, Nhalf, excl, prime_set=None):
    shape = pts[0].shape; full = prime_set is None
    out = {s: np.full(shape, Ck(len(s), excl) if full else 1.0) for s in subsets}
    if full:
        small = [p for p in (3, 5) if p not in excl]
        big = [int(p) for p in primes_upto(max(Nhalf, 7)) if p >= 7 and p not in excl]
    else:
        small = sorted(prime_set); big = []
    for p in small + big:
        r = [x % p for x in pts]; eq = {}
        def E(i, j):
            key = (min(i, j), max(i, j))
            if key not in eq: eq[key] = (r[key[0]] == r[key[1]])
            return eq[key]
        for s in subsets:
            k = len(s); nu = np.ones(shape, np.int64)
            for idx in range(1, k):
                new = np.ones(shape, bool)
                for j in s[:idx]: new &= ~E(j, s[idx])
                nu += new
            if p in small:
                out[s] = out[s] * ((1 - nu / p) / (1 - 1.0 / p) ** k)
            else:
                m = nu < k
                if m.any(): out[s][m] *= (p - nu[m]) / (p - k)
    return out

def delta_all(pts, Nhalf, excl, prime_set=None):
    k = len(pts); idx = tuple(range(k))
    subs = [c for r in range(2, k + 1) for c in itertools.combinations(idx, r)]
    S = S_subsets(pts, subs, Nhalf, excl, prime_set)
    D = np.zeros(pts[0].shape)
    for r in range(0, k + 1):
        for c in itertools.combinations(idx, r):
            D = D + (-1) ** (k - r) * (S[c] if r >= 2 else 1.0)
    return D

class Model:
    def __init__(self, Q0, chi, y):
        self.Q0 = Q0
        self.units = [n for n in range(1, Q0) if math.gcd(n, Q0) == 1]
        self.phi = len(self.units)
        self.chi = np.array([chi(u) for u in self.units], float)
        self.excl = odd_prime_factors(Q0)
        self.steps = [((self.units[(i + 1) % self.phi] - self.units[i]) % Q0) or Q0 for i in range(self.phi)]
        assert all(s % 2 == 0 for s in self.steps)
        self.set_y(y)
    def set_y(self, y):
        self.y = y; self.L = math.log(y)
        self.lam = self.Q0 / (self.phi * self.L); self.a = 1 - self.lam
        ph = self.phi
        Sh = np.zeros((ph, ph))
        for i in range(ph): Sh[i, (i + 1) % ph] = 1
        self.Sh = Sh
        self.M0 = Sh @ np.linalg.inv(np.eye(ph) - self.a * Sh)
        self.P = np.eye(ph) - self.lam * self.M0
    def offsets(self, N):
        """off[R][s] in half-units for s=0..N."""
        off = np.zeros((self.phi, N + 1), np.int64)
        for R in range(self.phi):
            for s in range(1, N + 1):
                off[R, s] = off[R, s - 1] + self.steps[(R + s - 1) % self.phi] // 2
        return off
    def c0(self):
        return float(self.chi @ (self.lam * self.M0) @ self.chi) / self.phi
    def G(self, k, N, prime_set=None, chunk=800_000):
        ph = self.phi; a = self.a; off = self.offsets(N); Nhalf = int(off.max())
        Gm = np.zeros((ph, ph))
        tri = {}
        def heads(depth, budget):
            if depth == 0: yield (); return
            for g in range(1, budget - 2 * depth + 2):
                for rest in heads(depth - 1, budget - g): yield (g,) + rest
        def tri_for(M):
            if M not in tri:
                b2, b3 = np.meshgrid(np.arange(1, M), np.arange(1, M), indexing='ij')
                mm = (b2 + b3) <= M; tri[M] = (b2[mm], b3[mm])
            return tri[M]
        # build list of gap tuples (k-1 gaps)
        def gap_batches():
            if k == 2:
                yield [np.arange(1, N + 1)]; return
            if k == 3:
                b2, b3 = tri_for(N); yield [b2, b3]; return
            parts = []; n = 0
            for h in heads(k - 3, N):
                M = N - sum(h)
                if M < 2: continue
                b2, b3 = tri_for(M)
                if len(b2) == 0: continue
                parts.append(tuple(np.full(len(b2), g) for g in h) + (b2, b3)); n += len(b2)
                if n >= chunk:
                    yield [np.concatenate(c) for c in zip(*parts)]; parts = []; n = 0
            if parts: yield [np.concatenate(c) for c in zip(*parts)]
        for gaps in gap_batches():
            S = [np.zeros_like(gaps[0])]
            for g in gaps: S.append(S[-1] + g)
            s = S[-1]
            for R in range(ph):
                pts = [off[R][Si] for Si in S]
                D = delta_all(pts, Nhalf, self.excl, prime_set)
                w = a ** (s - (k - 1.0)) * D
                Gm[R] += np.bincount((R + s) % ph, weights=w, minlength=ph)
        return Gm
    def ck(self, k, N, prime_set=None):
        Gm = self.G(k, N, prime_set)
        lam = self.lam
        return float(self.chi @ (lam * (-lam) ** (k - 2) * self.P @ Gm @ self.P) @ self.chi) / self.phi

def lichtblau(Qp, chi, y, block=None):
    """Exact absorbed model at modulus Qp (lam' = Qp/(phi L)); chi on integers."""
    L = math.log(y)
    fac = odd_prime_factors(Qp) | ({2} if Qp % 2 == 0 else set())
    units = []
    step = block or min(Qp, 20_000_000)
    for st in range(0, Qp, step):
        n = np.arange(st, min(st + step, Qp), dtype=np.int64)
        m = np.ones(len(n), bool)
        for p in fac: m &= (n % p != 0)
        units.append(n[m].astype(np.int64))
    u = np.concatenate(units); ph = len(u)
    x = chi(u).astype(np.float64)
    lamp = Qp / (ph * L); ap = 1 - lamp
    def Rk(k):
        k %= ph
        if k == 0: return float(np.dot(x, x))
        return float(np.dot(x[:-k], x[k:]) + np.dot(x[-k:], x[:k]))
    nmax = int(70 / lamp) + 10
    tot = 0.0
    if nmax >= ph:   # exact periodic geometric sum (R(k) has period ph)
        for k in range(1, ph + 1): tot += ap ** (k - 1) * Rk(k)
        tot /= (1 - ap ** ph)
    else:            # ap**nmax < 1e-30: truncation exact to double precision
        for k in range(1, nmax + 1): tot += ap ** (k - 1) * Rk(k)
    return lamp * tot / ph

CHI = {
    "chi-4": lambda n: np.where(np.asarray(n) % 4 == 1, 1, -1) if not np.isscalar(n) else (1 if n % 4 == 1 else -1),
    "chi-3": lambda n: np.where(np.asarray(n) % 3 == 1, 1, -1) if not np.isscalar(n) else (1 if n % 3 == 1 else -1),
    "leg5":  lambda n: np.where(np.isin(np.asarray(n) % 5, (1, 4)), 1, -1) if not np.isscalar(n) else (1 if n % 5 in (1, 4) else -1),
}
Q0 = {"chi-4": 4, "chi-3": 6, "leg5": 10}

def gl_nodes(lo, hi, n=2):
    u, w = np.polynomial.legendre.leggauss(n)
    a_, b_ = math.log(lo), math.log(hi)
    us = (b_ - a_) / 2 * u + (a_ + b_) / 2
    ws = w * np.exp(us); ws = ws / ws.sum()   # dy weight (matches archived c216 to 1e-10)
    return [math.exp(x) for x in us], list(ws)
