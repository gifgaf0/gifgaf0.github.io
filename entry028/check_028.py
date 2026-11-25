"""check_028.py -- independent re-computation of one Entry 028 stratum (numpy bool sieve, written
separately from gen_028.c: no presieve, no carried offsets, fixed 2^26-integer segments).
Returns nkept, first, last, sum mod 2^64, xor, pair, lag1[16,16], lag2[16,16] for the kept primes
(primes >= s_r: take n + 2 = 12,500,002, drop the first)."""
import numpy as np
U = [1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59]
IDX = -np.ones(60, np.int64); IDX[U] = np.arange(16)
_base = None
def base(lim=1460000):
    global _base
    if _base is None:
        s = np.ones(lim + 1, bool); s[:2] = False
        for i in range(2, int(lim ** 0.5) + 1):
            if s[i]: s[i * i::i] = False
        _base = np.nonzero(s)[0]; _base = _base[_base > 2]
    return _base
def stratum(y_r, s_r, pair_index, ntake=12_500_002, width=500_000_000):
    bp = base(); got = []; need = ntake; a = s_r; lim = y_r + width
    SEGW = 1 << 26
    while need > 0:
        if a >= lim: raise RuntimeError("boundary reached")
        b = min(a + SEGW, lim); o0 = a | 1; n = (b - o0 + 1) // 2
        seg = np.ones(n, bool)
        for p in bp:
            p = int(p)
            if p * p >= b: break
            m = max(p * p, ((o0 + p - 1) // p) * p)
            if m % 2 == 0: m += p
            seg[(m - o0) // 2::p] = False
        pr = o0 + 2 * np.nonzero(seg)[0].astype(np.int64)
        got.append(pr[:need]); need -= len(got[-1]); a = b
    q = np.concatenate(got)[1:]                       # drop the first prime >= s_r
    res = IDX[q % 60]
    L1 = np.bincount(res[:-1] * 16 + res[1:], minlength=256).reshape(16, 16)
    L2 = np.bincount(res[:-2] * 16 + res[2:], minlength=256).reshape(16, 16)
    u = q.astype(np.uint64)
    return dict(nkept=len(q), first=int(q[0]), last=int(q[-1]), sum=int(u.sum(dtype=np.uint64)),
                xor=int(np.bitwise_xor.reduce(u)), pair=(int(q[pair_index]), int(q[pair_index + 1])),
                lag1=L1, lag2=L2)
