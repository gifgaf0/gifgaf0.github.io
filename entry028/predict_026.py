# predict_026.py -- Entry 026 predictor.
# LO-S eq. (2.16) at modulus Q = q * prod(P), marginalised to classes mod q ("absorption").
# Code taken unchanged in substance from claude/research/exploratory_sign_size_2026-11-09.py (Part 2,
# on-the-fly marginal), which reproduces the project's frozen (2.16) values (mod-4 eps at 2^127.5 and
# 1e9-2e9, q=5 same-share at 2^255.5) and the archived mod-4 absorption ladder at 2^127.5.
# Additions here: character correlation, uniform-in-y averaging for random arms, CLI.
import numpy as np, math, sys, json, time

def primes_upto(n):
    s = np.ones(n+1, bool); s[:2] = False
    for i in range(2, int(n**0.5)+1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

_P = primes_upto(3_000_000)

def sing_series(Q, H):
    """S(d) for {0,d}, d=0..H, over primes not dividing Q (S[0] unused)."""
    C = 1.0
    for p in _P:
        if Q % p == 0 or p == 2: continue
        C *= p*(p-2.0)/((p-1.0)**2)
    Pm = float(_P[-1]); C *= math.exp(-1.0/(Pm*math.log(Pm)))
    S = np.full(H+1, C)
    if Q % 2 == 1:
        S[1::2] = 0.0; S[0::2] *= 2.0
    for p in _P:
        if p > H: break
        if p == 2 or Q % p == 0: continue
        S[p::p] *= (p-1.0)/(p-2.0)
    S[0] = 0.0
    return S

def units(Q):
    s = np.ones(Q, bool); s[0] = (Q == 1)
    n = Q; p = 2; fs = []
    while p*p <= n:
        if n % p == 0:
            fs.append(p)
            while n % p == 0: n //= p
        p += 1
    if n > 1: fs.append(n)
    for p in fs: s[::p] = False
    return s

def marg(Q, q, L, batch=1024):
    cop = units(Q)
    res = np.nonzero(cop)[0]
    phi = len(res)
    alpha = 1.0 - Q/(phi*L); kappa = Q/(phi*alpha*L)
    H = int(math.log(1e-15)/((phi/Q)*math.log(alpha))) + 2
    S = sing_series(Q, H); S0 = S - 1.0; S0[0] = 0.0
    h = np.arange(H+1)
    w = alpha**(h*phi/Q); w[0] = 0.0
    n = 1
    while n < 2*H+2: n *= 2
    fS0 = np.fft.rfft(S0, n)
    rq = [a for a in range(1, q+1) if math.gcd(a, q) == 1]
    pos = -np.ones(q, int)
    for i, a in enumerate(rq): pos[a % q] = i
    k = len(rq)
    M = np.zeros(k*k)
    h0 = ((h-1) % Q) + 1; h0[0] = 1
    for s in range(0, phi, batch):
        a = res[s:s+batch]
        T_idx = (a[:, None] + h[None, :]) % Q
        adm = cop[T_idx].astype(float); adm[:, 0] = 0.0
        aS = adm*S0[None, :]
        cs = np.cumsum(aS, axis=1)
        G1 = np.concatenate((np.zeros((len(a), 1)), cs[:, :-1]), axis=1)
        conv = np.fft.irfft(np.fft.rfft(adm, n, axis=1)*fS0[None, :], n, axis=1)[:, :H+1]
        c = adm*conv
        cc = np.cumsum(c, axis=1)
        F = np.concatenate((np.zeros((len(a), 1)), cc[:, :-1]), axis=1)
        T = w[None, :]*(S[None, :] - kappa*(G1+conv) + kappa*kappa*F)
        cum = np.cumsum(adm, axis=1)
        cnt = np.concatenate((np.zeros((len(a), 1)), cum[:, :-1]), axis=1)
        if H <= Q:
            eps = cnt - phi*h[None, :]/Q
        else:
            eps = cnt[:, h0] - phi*h0[None, :]/Q
        val = (alpha**eps)*T*adm
        val[:, 0] = 0.0
        ia = pos[a % q][:, None]; ib = pos[T_idx % q]
        good = ib >= 0
        np.add.at(M, (ia*k + ib)[good], val[good])
    M = M.reshape(k, k)*Q/(phi*phi)/(L*L)
    return rq, M

def table(q, absorb, L=None, rng=None, nodes=6, uniform=False):
    """Pair shares mod q.  L: local density at log y = L.  rng=(y0,y1): density integrated over
    primes in [y0,y1) (exhaustive arm; Gauss-Legendre in log y, weight dy).  uniform=True with rng:
    average of the *normalised* local table over y uniform in [y0,y1) (random-start arms)."""
    Q = q
    for p in absorb: Q *= p
    if rng is None:
        rq, M = marg(Q, q, L); return rq, M/M.sum()
    lo, hi = math.log(rng[0]), math.log(rng[1])
    x, wt = np.polynomial.legendre.leggauss(nodes)
    acc = 0
    for xi, wi in zip(x, wt):
        Ly = 0.5*(hi-lo)*xi + 0.5*(hi+lo)
        rq, Mi = marg(Q, q, Ly)
        if uniform:
            acc = acc + (Mi/Mi.sum())*math.exp(Ly)*wi     # dy weight, normalised local table
        else:
            acc = acc + Mi*math.exp(Ly)*wi               # dy weight, unnormalised density
    return rq, acc/acc.sum()

CHI = {3: {1: 1, 2: -1}, 4: {1: 1, 3: -1}, 5: {1: 1, 2: -1, 3: -1, 4: 1}}
OTHERS = {3: [2, 5, 7, 11, 13, 17, 19, 23], 4: [3, 5, 7, 11, 13, 17, 19, 23], 5: [2, 3, 7, 11, 13, 17, 19, 23]}

def corr(q, M, rq):
    v = np.array([CHI[q][a] for a in rq]); return float(v @ M @ v)

def corr_at(q, absorb, **kw):
    rq, M = table(q, absorb, **kw); return corr(q, M, rq)
