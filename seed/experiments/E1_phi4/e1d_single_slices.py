"""E1d: single-packet controls for every producing point of a 2D slice (added during the run,
after the coarse single-packet controls showed that most large-amplitude packets fold into
pairs on their own). Runs the right-moving packet alone (same grid, same time, same
production criterion). Usage: python e1d_single_slices.py <slice.json> [nproc]
Writes <slice>_single.json with one record per producing slice point."""
import sys
import json
import time
from multiprocessing import Pool
import e1d_gauss as G


def job(a):
    A, s, k = a
    r = G.run_gauss(A, s, k, 0.1, True)
    return {"A": A, "sigma": s, "k": k, "single_produced": r["produced"]}


if __name__ == "__main__":
    fn = sys.argv[1]
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    t0 = time.time()
    runs = [r for r in json.load(open(fn))["runs"] if r["produced"]]
    jobs = sorted([(r["A"], r["sigma"], r["k"]) for r in runs],
                  key=lambda j: -G.setup(*j)[3] * G.setup(*j)[4])
    with Pool(nproc) as p:
        res = p.map(job, jobs, chunksize=8)
    out = fn.replace(".json", "_single.json")
    json.dump({"source": fn, "runs": res, "runtime_s": time.time() - t0}, open(out, "w"), indent=1)
    print(f"{out}: {len(res)} producing slice points, {sum(r['single_produced'] for r in res)} also produce "
          f"as a single packet, {time.time() - t0:.0f} s")
