"""Entry 025 generator. usage: gen.py ARM SEED RUNS PRIMES_PER_RUN OUTDIR [WORKERS]
Each run: s uniform b-bit with top bit set; consecutive primes >= s via gmpy2.next_prime;
the first prime is dropped (gap-weighted selection). For each kept prime records
p mod 12, its congruence class, eligibility, and hit = [|E(F_p)|/t is prime]. Integrity checks inline.
37a1 uses early-abort SEA (ellsea(E_p,1)) with a full ellap count on 1 prime in 97.
"""
import sys, os, random, json, numpy as np, gmpy2, cypari2
from multiprocessing import Pool
ARMS = {"A37_64":("37a1",64), "B37_128":("37a1",128), "CCM_128":("cm",128), "DCM_256":("cm",256),
        "DRY37_40":("37a1",40), "DRYCM_48":("cm",48)}
COEF = {"37a1":[0,0,1,-1,0], "cm":[0,0,0,-1,0]}
def run(args):
    arm, seed, r, n, outdir = args
    fn = f"{outdir}/{arm}_run{r:05d}.npz"
    if os.path.exists(fn): return fn                      # resumable
    curve, b = ARMS[arm]; t = 1 if curve == "37a1" else 8
    pari = cypari2.Pari(); pari.allocatemem(256*10**6, silent=True); E = pari.ellinit(COEF[curve])
    rng = random.Random(f"{seed}:{arm}:{r}")
    s = rng.getrandbits(b) | (1 << (b-1))
    p = gmpy2.next_prime(s - 1)
    ps = []
    for _ in range(n): ps.append(p); p = gmpy2.next_prime(p)
    ps = ps[1:]
    cls = np.zeros(len(ps), np.uint8); mod12 = np.zeros(len(ps), np.uint8); elig = np.zeros(len(ps), np.uint8); hit = np.zeros(len(ps), np.uint8)
    bad = 0
    for i, q in enumerate(ps):
        mod12[i] = q % 12
        # congruence class carrying the known abelian channels (bits: high = G-class, low = p≡1 mod 3)
        g = (q % 8 == 5) if curve == "cm" else (gmpy2.legendre(q, 37) == 1)
        cls[i] = 2*int(g) + int(q % 3 == 1)
        if curve == "cm" and q % 4 != 1: continue
        elig[i] = 1
        Q = int(q)
        if curve == "37a1":
            # early-abort SEA: returns 0 as soon as a small prime factor of #E is found, else #E exactly
            a = int(pari.ellsea(pari.ellinit(COEF[curve], Q), 1))
            if gmpy2.legendre(q, 37) == -1 and a % 2: bad += 1       # (p/37)=-1 => 2 | #E (early abort may or may not fire; a nonzero return is #E and must be even)
            if a != 0 and gmpy2.is_prime(a, 40): hit[i] = 1
            if i % 97 == 0:                                           # full-count subsample
                N = Q + 1 - int(pari.ellap(E, Q))
                if (a != 0 and a != N) or (a == 0 and gmpy2.is_prime(N, 40)): bad += 1   # early abort agrees
                if (Q + 1 - N)**2 > 4*Q: bad += 1                     # Hasse
                if gmpy2.legendre(q, 37) == -1 and N % 2: bad += 1
                Ep = pari.ellinit(COEF[curve], Q); P = pari.random(Ep)
                if pari.ellmul(Ep, P, N) != pari('[0]'): bad += 1
        else:
            ap = int(pari.ellap(E, Q)); N = Q + 1 - ap
            if ap*ap > 4*Q: bad += 1                                  # Hasse
            if N % 8: bad += 1                                        # 8 | #E for split p
            if q % 8 == 1 and N % 16: bad += 1                        # p≡1 (8) => 16 | #E
            if q % 8 == 5 and N % 16 != 8: bad += 1                   # p≡5 (8) => #E ≡ 8 (16): no further 2-adic channel
            if i % 97 == 0:                                           # group-order check at a random point
                Ep = pari.ellinit(COEF[curve], Q); P = pari.random(Ep)
                if pari.ellmul(Ep, P, N) != pari('[0]'): bad += 1
            if gmpy2.is_prime(N // 8, 40): hit[i] = 1
    for j in rng.sample(range(len(ps)-1), min(5, len(ps)-1)):   # consecutiveness, independent finder
        if int(pari.nextprime(int(ps[j]) + 1)) != int(ps[j+1]): bad += 1
    np.savez_compressed(fn, cls=cls, mod12=mod12, elig=elig, hit=hit, bad=np.int64(bad),
                        start_bits=np.int64(b), first=str(int(ps[0])), last=str(int(ps[-1])))
    return fn
if __name__ == "__main__":
    arm, seed, runs, n, outdir = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    w = int(sys.argv[6]) if len(sys.argv) > 6 else os.cpu_count()
    os.makedirs(outdir, exist_ok=True)
    with Pool(w) as pool:
        for k, fn in enumerate(pool.imap_unordered(run, [(arm, seed, r, n, outdir) for r in range(runs)])):
            if k % 50 == 0: print(k, fn, flush=True)
