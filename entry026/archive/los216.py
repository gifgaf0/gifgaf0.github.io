#!/usr/bin/env python3
"""
Lemke Oliver–Soundararajan eq. (2.16): density of consecutive-prime pairs
p_n ≡ a, p_{n+1} ≡ b (mod q) at height y,

  d/dy pi(y;q,(a,b)) = (q/phi^2) * alpha^eps(a,b) / (log y)^2 * (D0 + D1 + D2)(a,b;y)

alpha = 1 - q/(phi log y); w(h) = alpha^(h phi/q); kappa = q/(phi alpha log y)
D0 = sum_{h ≡ b-a} S(h) w(h)
D1 = -kappa sum_{h ≡ b-a} w(h) sum_{1<=t<h, (t+a,q)=1} [S0(t) + S0(h-t)]
D2 = kappa^2 sum_{h ≡ b-a} w(h) sum_{1<=t1<t2<h, (t_i+a,q)=1} S0(t2-t1)
with S(d) = S_q({0,d}) (Hardy–Littlewood singular series over p ∤ q) and
S0(d) = S(d) - 1 (the paper's S_{q,0}({0,d}); S_{q,0} vanishes on singletons).
eps(a,b): #{0<t<h0 : (t+a,q)=1} = phi h0/q + eps, h0 ≡ b-a in [1,q].

Sums are computed exactly (no Prop. 2.1 substitution), truncated where w(h) < 1e-17.
"""
import math
from functools import lru_cache
import numpy as np


def _primes(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, int(n ** .5) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]
_PR = _primes(10_000_000)


def _factors(n):
    f, d = set(), 2
    while d * d <= n:
        while n % d == 0: f.add(d); n //= d
        d += 1
    if n > 1: f.add(n)
    return f


@lru_cache(maxsize=None)
def _Cprime(q):
    qf = _factors(q)
    ps = _PR[(_PR >= 3) & ~np.isin(_PR, list(qf))].astype(float)
    return float(np.exp(np.sum(np.log1p(-1.0 / (ps - 1) ** 2))))


@lru_cache(maxsize=None)
def S_table(q, H):
    """S(d) = S_q({0,d}) for d = 0..H."""
    qf = _factors(q); C = _Cprime(q)
    spf = np.arange(H + 1)
    for p in range(2, int(H ** .5) + 1):
        if spf[p] == p:
            m = spf[p*p::p]; spf[p*p::p] = np.where(m == np.arange(p*p, H + 1, p), p, m)
    S = np.zeros(H + 1)
    for d in range(1, H + 1):
        val, n = C, d
        if 2 not in qf:
            val *= 2.0 if d % 2 == 0 else 0.0
        while n > 1:
            p = spf[n]
            if p >= 3 and p not in qf: val *= (p - 1) / (p - 2)
            while n % p == 0: n //= p
        S[d] = val
    return S


def phi(n): return round(n * math.prod(1 - 1/p for p in _factors(n))) if n > 1 else 1


@lru_cache(maxsize=256)
def _arrays(q, a, y):
    """Everything in the density that depends on (q, a, y) but not on b (cached)."""
    ph = phi(q); L = math.log(y)
    alpha = 1 - q / (ph * L); kappa = q / (ph * alpha * L)
    lw = math.log(alpha) * ph / q                       # log w(1)
    H = int(math.ceil(39.0 / -lw)) + q
    S = S_table(q, H); S0 = S - 1.0
    t = np.arange(H + 1)
    c = (np.gcd(t + a, q) == 1).astype(float); c[0] = 0.0
    S0z = S0.copy(); S0z[0] = 0.0
    P1 = np.concatenate([[0.0], np.cumsum(c * S0z)[:-1]])          # sum_{1<=t<h} c(t) S0(t)
    conv = np.convolve(c, S0z)[:H + 1]                               # sum_{t} c(t) S0(h-t), t>=1, h-t>=1
    Q = np.concatenate([[0.0], np.cumsum(c * conv)[:-1]])            # sum_{t2<h} c(t2) conv(t2)
    return ph, L, alpha, kappa, lw, H, S, P1, conv, Q


def density(q, a, b, y):
    ph, L, alpha, kappa, lw, H, S, P1, conv, Q = _arrays(q, a, y)
    v = (b - a) % q
    h = np.arange(v if v else q, H + 1, q)
    w = np.exp(lw * h)
    D0 = np.sum(S[h] * w)
    D1 = -kappa * np.sum(w * (P1[h] + conv[h]))
    D2 = kappa ** 2 * np.sum(w * Q[h])
    h0 = v if v else q
    cnt = sum(1 for tt in range(1, h0) if math.gcd(tt + a, q) == 1)
    eps = cnt - ph * h0 / q
    return (q / ph ** 2) * alpha ** eps / L ** 2 * (D0 + D1 + D2)


def pair_density_table(q, y):
    units = [a for a in range(1, q) if math.gcd(a, q) == 1]
    return units, {(a, b): density(q, a, b, y) for a in units for b in units}


def cumulative(q, a, b, x, y0=1e3, nodes=400):
    """pi(x;q,(a,b)) ~ integral_{y0}^{x} density dy (contribution below y0 is negligible here)."""
    u, wts = np.polynomial.legendre.leggauss(nodes)
    lo, hi = math.log(y0), math.log(x)
    us = (hi - lo) / 2 * u + (hi + lo) / 2
    return (hi - lo) / 2 * sum(wt * math.exp(uu) * density(q, a, b, math.exp(uu)) for uu, wt in zip(us, wts))


if __name__ == "__main__":
    # normalization: sum over all pairs should be ~ 1/log y (density of primes)
    for q in (3, 4, 7, 13):
        for y in (1e9, 2 ** 255.5):
            units, tab = pair_density_table(q, y)
            print(f"q={q:>2} y={y:.1e}: sum of pair densities x log y = {sum(tab.values()) * math.log(y):.6f}")
    # validation against the paper's Table, rows (2.16)
    paper = {1e9: (1.137e7, 1.405e7, 1.148e7, 1.395e7), 1e10: (1.028e8, 1.247e8, 1.037e8, 1.239e8),
             1e11: (9.383e8, 1.121e9, 9.450e8, 1.114e9), 1e12: (8.630e9, 1.017e10, 8.684e9, 1.012e10)}
    print("\nRelative difference from the paper's (2.16) values  [q=3 (1,1), q=3 (1,2), q=4 (1,1), q=4 (1,3)]")
    for x, ref in paper.items():
        ours = [cumulative(3, 1, 1, x), cumulative(3, 1, 2, x), cumulative(4, 1, 1, x), cumulative(4, 1, 3, x)]
        print(f"  x=1e{int(math.log10(x))}: " + "  ".join(f"{o/r-1:+.4f}" for o, r in zip(ours, ref)))
