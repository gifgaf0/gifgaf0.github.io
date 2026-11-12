"""build_026.py -- Entry 026 integrity checks. Prints PASS/FAIL per check; computes no correlation.
Usage: build_026.py E_BIN CHECK_NPZ LO HI SEED R64_DIR N64 R128_DIR N128
  E_BIN      gen_E_026 output; CHECK_NPZ check_E_026.py output for the same range (independent sieve).
  LO, HI     the pre-registered arm-E range.
  SEED       the beacon randomness (hex); N64, N128 the pre-registered run counts (runs 0..N-1).
"""
import sys, os, glob, json, random
import numpy as np, cypari2
pari = cypari2.Pari()
efn, cfn, LO, HI, SEED = sys.argv[1], sys.argv[2], int(float(sys.argv[3])), int(float(sys.argv[4])), sys.argv[5]
ARMS_R = ((64, sys.argv[6], int(sys.argv[7])), (128, sys.argv[8], int(sys.argv[9])))
NP = 10 ** 4 + 1
fails = 0
def check(name, ok, info=''):
    global fails
    fails += (not ok); print(f"{'PASS' if ok else 'FAIL'}  {name}  {info}", flush=True)

# ---------- arm E ----------
h = np.fromfile(efn, np.uint64)
nb = int(h[4]); blk = h[8:].reshape(nb, 3 + 512)
c = np.load(cfn)
check('E header range', int(h[1]) == LO and int(h[2]) == HI, f'[{int(h[1])}, {int(h[2])})')
check('E prime count = independent sieve', int(h[5]) == int(c['nprimes']), f'{int(h[5]):,} vs {int(c["nprimes"]):,}')
check('E sum and xor of primes = independent sieve', h[6] == c['sum'] and h[7] == c['xor'])
check('E per-block counts, first, last = independent sieve',
      (blk[:, 0] == c['cnt']).all() and (blk[:, 1] == c['first']).all() and (blk[:, 2] == c['last']).all())
check('E lag-1 and lag-2 tables = independent sieve',
      (blk[:, 3:259].reshape(nb, 16, 16) == c['lag1']).all() and (blk[:, 259:].reshape(nb, 16, 16) == c['lag2']).all())
n = int(h[5])
check('E lag-1 total = primes - 1, lag-2 total = primes - 2', int(blk[:, 3:259].sum()) == n - 1 and int(blk[:, 259:].sum()) == n - 2)
check('E block counts sum to prime count', int(blk[:, 0].sum()) == n)
B = int(h[3]); bad = 0
for k in range(nb):
    a, b = LO + k * B, min(LO + (k + 1) * B, HI)
    if int(blk[k, 1]) != int(pari.nextprime(a)) or int(blk[k, 2]) != int(pari.precprime(b - 1)): bad += 1
check('E first and last prime of every block = PARI nextprime / precprime', bad == 0, f'{nb} blocks, {bad} mismatches')

# ---------- arms R64, R128 ----------
for bits, d, nruns in ARMS_R:
    files = sorted(glob.glob(os.path.join(d, f'R{bits}_*.npz')))
    runs, L1, L2, first, last, samples, seeds = [], [], [], [], [], [], set()
    for fn in files:
        z = np.load(fn); seeds.add(str(z['seed'])); runs += list(z['runs']); L1.append(z['lag1']); L2.append(z['lag2'])
        first += list(z['first']); last += list(z['last']); samples += json.load(open(fn.replace('.npz', '_sample.json')))
    L1 = np.concatenate(L1).astype(np.int64); L2 = np.concatenate(L2).astype(np.int64)
    check(f'R{bits} every chunk generated with the beacon seed', seeds == {SEED}, f'{len(files)} chunks')
    check(f'R{bits} run indices exactly 0..{nruns - 1}', sorted(runs) == list(range(nruns)), f'{len(runs)} runs')
    check(f'R{bits} every run has 9,999 lag-1 and 9,998 lag-2 pairs',
          (L1.sum(axis=(1, 2)) == 9999).all() and (L2.sum(axis=(1, 2)) == 9998).all())
    bad_start = bad_len = 0
    for run, f0, l0 in zip(runs, first, last):
        rng = random.Random(f"{SEED}:R{bits}:{run}")
        s = rng.getrandbits(bits - 1) | (1 << (bits - 1))
        p0 = pari.nextprime(s); p1 = pari.nextprime(p0 + 1)          # first prime >= s is dropped
        bad_start += int(p1) != int(f0)
        bad_len += not (int(f0).bit_length() == bits and int(l0).bit_length() == bits and int(l0) > int(f0))
    check(f'R{bits} first kept prime of every run = PARI nextprime from the seeded start', bad_start == 0, f'{bad_start} mismatches')
    check(f'R{bits} first and last kept primes have {bits} bits', bad_len == 0)
    bad = 0
    for smp in samples:
        p, q = int(smp['p']), int(smp['p_next'])
        if not (pari.isprime(p) and pari.isprime(q) and int(pari.nextprime(p + 1)) == q): bad += 1
    check(f'R{bits} sampled pair per run proven prime and consecutive (PARI isprime, nextprime)', bad == 0, f'{len(samples)} pairs, {bad} failures')
    check(f'R{bits} distinct starts', len(set(first)) == len(first))
print(f"\nintegrity failures: {fails}")
