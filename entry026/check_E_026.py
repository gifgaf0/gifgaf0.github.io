"""check_E_026.py -- independent re-computation of the arm-E generator output (numpy segmented sieve,
written separately from gen_E_026.c). Writes the same quantities to an .npz:
nprimes, sum mod 2^64, xor, and per-block nprimes, first, last, lag1[16,16], lag2[16,16].
Usage: check_E_026.py lo hi blocksize out.npz
"""
import sys, numpy as np
lo, hi, B = (int(float(v)) for v in sys.argv[1:4]); out = sys.argv[4]
U = [1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59]
IDX = -np.ones(60, np.int64); IDX[U] = np.arange(16)
r = int(hi ** 0.5) + 2
s = np.ones(r + 1, bool); s[:2] = False
for i in range(2, int(r ** 0.5) + 1):
    if s[i]: s[i * i::i] = False
base = np.nonzero(s)[0]; base = base[base > 2]
nb = (hi - lo + B - 1) // B
cnt = np.zeros(nb, np.int64); first = np.zeros(nb, np.uint64); last = np.zeros(nb, np.uint64)
L1 = np.zeros((nb, 256), np.int64); L2 = np.zeros((nb, 256), np.int64)
SEGW = 1 << 26                                # integers per segment
tot = 0; sm = np.uint64(0); xr = np.uint64(0)
carry = np.zeros(0, np.int64)                 # last two primes of the previous segment
for a in range(lo, hi, SEGW):
    b = min(a + SEGW, hi)
    o0 = a | 1                                # first odd >= a
    n = (b - o0 + 1) // 2
    if n <= 0: continue
    seg = np.ones(n, bool)
    for p in base:
        p = int(p)
        if p * p >= b: break
        m = max(p * p, ((o0 + p - 1) // p) * p)
        if m % 2 == 0: m += p
        seg[(m - o0) // 2::p] = False
    pr = o0 + 2 * np.nonzero(seg)[0].astype(np.int64)
    if len(pr) == 0: continue
    blk = (pr - lo) // B
    c = np.bincount(blk, minlength=nb);
    for k in np.nonzero(c)[0]:
        if cnt[k] == 0: first[k] = pr[blk == k][0]
    cnt += c
    last[blk[-1]] = pr[-1]
    for k in np.unique(blk): last[k] = pr[blk == k][-1]
    tot += len(pr)
    u = pr.astype(np.uint64)
    sm = np.uint64((int(sm) + int(u.sum(dtype=np.uint64))) % (1 << 64))
    xr = np.uint64(int(xr) ^ int(np.bitwise_xor.reduce(u)))
    allp = np.concatenate((carry, pr))
    res = IDX[allp % 60]; ab = (allp - lo) // B
    # carry holds the last <= 2 primes already seen. Lag-1 pairs already counted: those inside carry,
    # so start at carry[-1]. Lag-2 pairs (allp[i], allp[i+2]) with i+2 >= len(carry) are all new.
    k1 = len(carry) - 1 if len(carry) else 0
    i1 = res[k1:-1] * 16 + res[k1 + 1:]
    if len(i1):
        L1 += np.bincount(ab[k1:-1] * 256 + i1, minlength=nb * 256).reshape(nb, 256)
    i2 = res[:-2] * 16 + res[2:]
    if len(i2):
        L2 += np.bincount(ab[:-2] * 256 + i2, minlength=nb * 256).reshape(nb, 256)
    carry = allp[-2:]
    print(f"{b:.4e} {tot}", file=sys.stderr, flush=True) if (a - lo) % (SEGW * 32) == 0 else None
np.savez(out, nprimes=tot, sum=sm, xor=xr, cnt=cnt, first=first, last=last,
         lag1=L1.reshape(nb, 16, 16), lag2=L2.reshape(nb, 16, 16))
print("primes", tot, file=sys.stderr)
