# Compare regenerated B37_128 runs with the archived ones (from the committed chunk tarballs).
# usage: compare.py ARCHIVE_DIR REGEN_DIR RUNLIST131 RUNLIST46
import sys, glob, tarfile, io, numpy as np, json
arch, regen, l131, l46 = sys.argv[1:5]
want = {f"B37_128_run{int(r):05d}.npz" for r in open(l131).read().split()}
s46 = {f"B37_128_run{int(r):05d}.npz" for r in open(l46).read().split()}
archived = {}
for t in sorted(glob.glob(arch + "/B37_128_chunk*.tar")):
    with tarfile.open(t) as tf:
        for m in tf.getmembers():
            if m.name in want: archived[m.name] = tf.extractfile(m).read()
res = {"compared": 0, "identical": 0, "mismatches": [], "missing": sorted(want - set(archived))}
for name in sorted(want):
    if name not in archived: continue
    a = np.load(io.BytesIO(archived[name])); b = np.load(f"{regen}/{name}")
    diff = [k for k in ("hit", "cls", "elig", "mod12") if not np.array_equal(a[k], b[k])]
    diff += [k for k in ("first", "last") if str(a[k]) != str(b[k])]
    res["compared"] += 1
    if diff: res["mismatches"].append({"run": name, "fields": diff})
    else: res["identical"] += 1
res["subset46_compared"] = len(s46 & set(archived)); res["subset46_mismatches"] = [m for m in res["mismatches"] if m["run"] in s46]
print(json.dumps(res, indent=1))
