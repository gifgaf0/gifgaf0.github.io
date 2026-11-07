# Regenerate specific B37_128 runs with the frozen gen.run() into a fresh directory.
# usage: python3 regen.py ENTRY_DIR RUNLIST OUTDIR
import sys, os
entry, runlist, outdir = sys.argv[1:4]
sys.path.insert(0, entry)
import gen
from multiprocessing import Pool
SEED = "3ffa707eb1d3c2a115be7fa81c3af89618a7097e35632d140d8801224bda98da"
runs = [int(x) for x in open(runlist).read().split()]
os.makedirs(outdir, exist_ok=False)
with Pool(4) as p:
    for k, fn in enumerate(p.imap_unordered(gen.run, [("B37_128", SEED, r, 1001, outdir) for r in runs])):
        if k % 10 == 0: print(k, fn, flush=True)
print("done", len(runs), flush=True)
