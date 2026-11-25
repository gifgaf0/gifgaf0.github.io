"""build_028.py SEED DATADIR [--y0 Y0] [--M 2000] [--nverify 20] [--hashes FILE] [--write-hashes FILE]
Entry 028 integrity suite (expected: 0 failures).  Checks:
 C1 chunk seeds all equal SEED;  C2 stratum indices exactly 0..M-1, each once;
 C3 y_r, s_r, pair_index re-derived from SEED match every record;  C4 magic, flags = 0, n + 1 kept primes,
    lag-1 total n, lag-2 total n - 1 (n = 12,500,000);  C5 boundary: last kept prime < y_r + 5e8;
 C6 PARI: first kept prime = nextprime(nextprime(s_r) + 1), every stratum;
 C7 PARI: sampled pair proven prime (isprime) and consecutive (nextprime(p + 1) = q), every stratum;
 C8 independent numpy sieve (check_028.py) on NVERIFY strata chosen by random.Random(f"{SEED}:E028:verify"):
    count, first, last, sum mod 2^64, xor, sampled pair, lag-1 and lag-2 tables;
 C9 (with --hashes) every chunk file matches its recorded sha256; C10 every chunk made by the frozen gen_028.c.
No character statistic is computed."""
import sys, os, glob, json, random, hashlib, argparse
import numpy as np, cypari2
from read_028 import read, MAGIC
from check_028 import stratum
ap = argparse.ArgumentParser(); ap.add_argument("seed"); ap.add_argument("datadir")
ap.add_argument("--y0", type=float, default=1.05e12); ap.add_argument("--M", type=int, default=2000)
ap.add_argument("--nverify", type=int, default=20); ap.add_argument("--hashes"); ap.add_argument("--write-hashes")
a = ap.parse_args(); Y0 = int(a.y0); W = 500_000_000; OFFSET = 100_000_000; NPER = 12_500_000
HERE = os.path.dirname(os.path.abspath(__file__))
SRC_SHA = hashlib.sha256(open(os.path.join(HERE, "gen_028.c"), "rb").read()).hexdigest()
pari = cypari2.Pari()
fails = []
def check(name, ok, detail=""):
    print(f"  {name}: {'ok' if ok else 'FAIL'} {detail}", flush=True)
    if not ok: fails.append(name)
metas = sorted(glob.glob(os.path.join(a.datadir, "chunk_*.json")))
recs, seeds, srcs = [], set(), set()
for m in metas:
    j = json.load(open(m)); seeds.add(j["seed"]); srcs.add(j["gen_c_sha256"])
    recs.append(read(m[:-5] + ".bin"))
print(f"build_028: {len(metas)} chunks, expected seed {a.seed!r}, y0 {Y0:.4e}, M {a.M}")
if not recs:
    print("  C0 data present: FAIL no chunk files in " + a.datadir); print("build_028: 1 failures: C0 data present"); sys.exit(1)
R = np.concatenate(recs); print(f"  {len(R)} strata records")
if a.hashes:
    if not os.path.exists(a.hashes):
        print(f"  C9 chunk sha256: FAIL hash file {a.hashes} missing"); print("build_028: 1 failures: C9"); sys.exit(1)
    H = json.load(open(a.hashes)); bad = [f for f, h in H.items() if not os.path.exists(os.path.join(a.datadir, f)) or hashlib.sha256(open(os.path.join(a.datadir, f), 'rb').read()).hexdigest() != h]
    check("C9 chunk sha256", not bad and len(H) == 2 * len(metas), f"mismatched: {bad}" if bad else f"{len(H)} files")
check("C10 generator", srcs == {SRC_SHA}, f"{sorted(srcs)} vs {SRC_SHA[:12]}")
check("C1 seed", seeds == {a.seed}, f"chunk seeds {sorted(seeds)}")
r = R['r'].astype(np.int64)
check("C2 indices", sorted(r.tolist()) == list(range(a.M)), f"{len(r)} records, range {r.min() if len(r) else None}..{r.max() if len(r) else None}")
mism = 0
for x in R:
    rng = random.Random(f"{a.seed}:E028:{int(x['r'])}"); y = Y0 + W * int(x['r']); s = y + rng.randrange(OFFSET); jj = rng.randrange(NPER)
    mism += (int(x['y_r']) != y) + (int(x['s_r']) != s) + (int(x['pair_index']) != jj)
check("C3 seeded starts", mism == 0, f"{mism} mismatched fields")
ok4 = (R['magic'] == MAGIC).all() and (R['flags'] == 0).all() and (R['nkept'] == NPER + 1).all() \
      and (R['lag1'].sum(axis=1) == NPER).all() and (R['lag2'].sum(axis=1) == NPER - 1).all()
check("C4 counts", bool(ok4))
check("C5 boundary", bool((R['last'] < R['y_r'] + W).all()), f"max last - y_r = {int((R['last'] - R['y_r']).max()):,} < {W:,}; max run span last - s_r = {int((R['last'] - R['s_r']).max()):,} (+ offset window {OFFSET:,} must stay < {W:,})")
bad6 = sum(int(pari.nextprime(pari.nextprime(int(x['s_r'])) + 1)) != int(x['first']) for x in R)
check("C6 PARI first kept", bad6 == 0, f"{bad6} of {len(R)} differ")
bad7 = 0
for x in R:
    p, q = int(x['pair_p']), int(x['pair_q'])
    bad7 += not (pari.isprime(p) and pari.isprime(q) and int(pari.nextprime(p + 1)) == q)
check("C7 PARI sampled pair", bad7 == 0, f"{bad7} of {len(R)} fail")
sel = random.Random(f"{a.seed}:E028:verify").sample(range(a.M), min(a.nverify, a.M))
byr = {int(x['r']): x for x in R}; bad8 = []
for rr in sorted(sel):
    if rr not in byr: bad8.append(rr); continue
    x = byr[rr]; c = stratum(int(x['y_r']), int(x['s_r']), int(x['pair_index']))
    same = (c['nkept'] == x['nkept'] and c['first'] == x['first'] and c['last'] == x['last'] and c['sum'] == x['sum']
            and c['xor'] == x['xor'] and c['pair'] == (int(x['pair_p']), int(x['pair_q']))
            and (c['lag1'].ravel() == x['lag1']).all() and (c['lag2'].ravel() == x['lag2']).all())
    if not same: bad8.append(rr)
check("C8 independent sieve", not bad8, f"{len(sel)} strata {sorted(sel)}; mismatched {bad8}")
if a.write_hashes:
    H = {os.path.basename(f): hashlib.sha256(open(f, 'rb').read()).hexdigest()
         for m in metas for f in (m, m[:-5] + ".bin")}
    json.dump(H, open(a.write_hashes, "w"), indent=1); print(f"  wrote {len(H)} chunk hashes to {a.write_hashes}")
print(f"build_028: {len(fails)} failures" + (f": {', '.join(fails)}" if fails else ""))
sys.exit(1 if fails else 0)
