"""gen_R_026.py -- Entry 026 random-start arms (R64, R128).
Run r of arm R{b}: start s uniform in [2^(b-1), 2^b) from random.Random(f"{SEED}:R{b}:{r}"), where SEED is the
randomness (hex) of the drand round fixed by the beacon rule of the entry; 10^4 + 1 consecutive
primes from the first prime >= s (gmpy2.next_prime); the first prime is dropped, leaving 10^4 primes
and 9,999 adjacent pairs (Entry 025 convention). Stored per run: lag-1 and lag-2 pair tables of
residues mod 60 (16 x 16, the units), and one sampled consecutive pair for the integrity checks.
Chunks of 100 runs, resumable; the seed is stored in every chunk.
Usage: gen_R_026.py BITS SEED OUTDIR RUN_START RUN_END
"""
import sys, os, json, random
import numpy as np, gmpy2
NP = 10 ** 4 + 1
U = [1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59]
IDX = {u: i for i, u in enumerate(U)}
bits, SEED, outdir, r0, r1 = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
os.makedirs(outdir, exist_ok=True)
CH = 100
for c0 in range(r0, r1, CH):
    fn = os.path.join(outdir, f'R{bits}_{c0:06d}.npz')
    if os.path.exists(fn):
        continue
    runs = list(range(c0, min(c0 + CH, r1)))
    L1 = np.zeros((len(runs), 16, 16), np.uint16); L2 = np.zeros((len(runs), 16, 16), np.uint16)
    first, lastp, sample = [], [], []
    for j, run in enumerate(runs):
        rng = random.Random(f"{SEED}:R{bits}:{run}")
        s = rng.getrandbits(bits - 1) | (1 << (bits - 1))
        k = rng.randrange(1, NP - 1)                     # sampled pair (i, i+1), i >= 1
        p = gmpy2.next_prime(s - 1)
        res = []
        for i in range(NP):
            q = gmpy2.next_prime(p)
            if i == k:
                sample.append({'run': run, 'i': i, 'p': str(p), 'p_next': str(q)})
            if i >= 1:
                res.append(IDX[int(p % 60)])
                if i == 1: first.append(str(p))
                if i == NP - 1: lastp.append(str(p))
            p = q
        r = np.array(res)
        np.add.at(L1[j], (r[:-1], r[1:]), 1)
        np.add.at(L2[j], (r[:-2], r[2:]), 1)
    np.savez(fn, seed=np.array(SEED), runs=np.array(runs), lag1=L1, lag2=L2, first=np.array(first), last=np.array(lastp))
    json.dump(sample, open(fn.replace('.npz', '_sample.json'), 'w'))
    print('wrote', fn, flush=True)
