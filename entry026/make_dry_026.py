"""make_dry_026.py -- synthetic dry-run data for Entry 026 (no real primes in the decisive ranges).
Pair tables mod 60 come from the predictor: (2.16) at Q = 60*7*11*13, marginalised to the 16 units
mod 60 (so 2, 3, 5, 7, 11, 13 are absorbed for every character). Counts are multinomial per block
(arm E: 200 blocks, 7.24e8 pairs in all) or per run (R64, R128: 9,999 pairs per run).
mode null:   data drawn from the T60 tables; the dry-run prediction file uses their marginals as 'full HL'.
mode effect: each table is mixed with the independent table, T = lam*T60 + (1-lam)*rowsum x colsum,
             lam = c216/cfull for chi_-4 at that height, so the correlations sit near (2.16).
Usage: make_dry_026.py MODE NRUNS64 NRUNS128 OUTDIR PRED_JSON SEED
"""
import sys, os, json, math
import numpy as np
from predict_026 import marg
ln2 = math.log(2)
mode, n64, n128, outdir, predfn, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6])
rng = np.random.default_rng(seed)
os.makedirs(outdir, exist_ok=True)
pred = json.load(open(predfn))
Q = 60 * 7 * 11 * 13
def T60(L):
    rq, M = marg(Q, 60, L); return M / M.sum()
Ls = {'E': math.log(1.01e12), 'R64': 63.5 * ln2, 'R128': 127.5 * ln2}
U = np.array([1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59])
def chiv(q):
    return {3: np.where(U % 3 == 1, 1, -1), 4: np.where(U % 4 == 1, 1, -1), 5: np.where(np.isin(U % 5, (1, 4)), 1, -1)}[q]
dpred = json.loads(json.dumps(pred)); dpred['dry_run'] = mode
for a, L in Ls.items():
    T = T60(L)
    if mode == 'effect':
        c = pred['cells'][f'{a}_4']; lam = c['c216'] / c['cfull']
        T = lam * T + (1 - lam) * np.outer(T.sum(1), T.sum(0))
    for q in (3, 4, 5):
        v = chiv(q); dpred['cells'][f'{a}_{q}']['cfull'] = float(v @ (T60(L) if mode == 'effect' else T) @ v)
        dpred['cells'][f'{a}_{q}']['dry_table_corr'] = float(v @ T @ v)
    p = T.ravel()
    if a == 'E':
        nb = 200; n = 724_000_000 // nb
        L1 = rng.multinomial(n, p, size=nb).reshape(nb, 16, 16)
        L2 = rng.multinomial(n, p, size=nb).reshape(nb, 16, 16)
        per = 3 + 512
        blk = np.zeros((nb, per), np.uint64)
        blk[:, 0] = n + 1; blk[:, 3:259] = L1.reshape(nb, 256); blk[:, 259:] = L2.reshape(nb, 256)
        hdr = np.array([0x3032364547454e45, 10**12, 102 * 10**10, 10**8, nb, nb * (n + 1), 0, 0], np.uint64)
        np.concatenate((hdr, blk.ravel())).tofile(os.path.join(outdir, 'E.bin'))
    else:
        bits = int(a[1:]); d = os.path.join(outdir, a); os.makedirs(d, exist_ok=True)
        nruns = n64 if bits == 64 else n128
        for c0 in range(0, nruns, 100):
            k = min(100, nruns - c0)
            L1 = rng.multinomial(9999, p, size=k).reshape(k, 16, 16).astype(np.uint16)
            L2 = rng.multinomial(9998, p, size=k).reshape(k, 16, 16).astype(np.uint16)
            np.savez(os.path.join(d, f'R{bits}_{c0:06d}.npz'), seed=np.array(f'dry-{seed}'), runs=np.arange(c0, c0 + k), lag1=L1, lag2=L2,
                     first=np.array([''] * k), last=np.array([''] * k))
json.dump(dpred, open(os.path.join(outdir, 'pred_dry.json'), 'w'), indent=1)
print('dry data written to', outdir)
