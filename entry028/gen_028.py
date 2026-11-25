"""gen_028.py SEED OUTDIR R_START R_END [--y0 Y0] [--chunk 50] -- Entry 028 data generation.
Stratum r: y_r = Y0 + 5e8*r; rng = random.Random(f"{SEED}:E028:{r}"); s_r = y_r + rng.randrange(100_000_000);
pair_index = rng.randrange(12_500_000).  Calls the compiled gen_028 on chunks of strata; each chunk is
chunk_RRRR.bin (records) + chunk_RRRR.json (seed, Y0, strata, sha256 of gen_028.c).  Resumable: finished
chunks (json present) are skipped."""
import sys, os, json, random, subprocess, hashlib, time, argparse
ap = argparse.ArgumentParser(); ap.add_argument("seed"); ap.add_argument("outdir"); ap.add_argument("r0", type=int); ap.add_argument("r1", type=int)
ap.add_argument("--y0", type=float, default=1.05e12); ap.add_argument("--chunk", type=int, default=50)
a = ap.parse_args()
HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, "gen_028"); SRC = os.path.join(HERE, "gen_028.c")
src_sha = hashlib.sha256(open(SRC, "rb").read()).hexdigest()
Y0 = int(a.y0); W = 500_000_000; OFFSET = 100_000_000; NPER = 12_500_000
def stratum_params(seed, r, y0=Y0):
    rng = random.Random(f"{seed}:E028:{r}")
    y = y0 + W * r; s = y + rng.randrange(OFFSET); j = rng.randrange(NPER)
    return y, s, j
if __name__ == "__main__":
    os.makedirs(a.outdir, exist_ok=True)
    for c0 in range(a.r0, a.r1, a.chunk):
        rs = list(range(c0, min(c0 + a.chunk, a.r1)))
        base = os.path.join(a.outdir, f"chunk_{c0:04d}")
        if os.path.exists(base + ".json"): continue
        lines = "".join("%d %d %d %d\n" % ((r,) + stratum_params(a.seed, r)) for r in rs)
        t = time.time()
        subprocess.run([GEN, base + ".bin.part"], input=lines.encode(), check=True)
        os.replace(base + ".bin.part", base + ".bin")
        json.dump(dict(entry="028", seed=a.seed, y0=Y0, width=W, strata=rs, gen_c_sha256=src_sha,
                       seconds=round(time.time() - t, 2)), open(base + ".json", "w"))
        print(f"chunk {c0}: {len(rs)} strata in {time.time()-t:.1f}s", flush=True)
