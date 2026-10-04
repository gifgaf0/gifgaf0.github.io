#!/usr/bin/env python3
"""Second computation of the Table 2 rows that the blind comparison did not cover (g = 34, 20, 18, 15 and the
metastable 12.7, 12.5, 12.4), with the second leg's own instrument (second_leg/cc2d.py on main, unchanged):
a* by its Brent search, BdG speeds and weights by its parity-resolved solver, f_s by linear response.
Not blind: run chat-side after the first leg's values were known; the instrument and its settings are the second leg's."""
import sys, json, time, hashlib
sys.path.insert(0, "/tmp/claude-0/-home-claude-gifgaf0-github-io/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad")
assert hashlib.md5(open("/tmp/claude-0/-home-claude-gifgaf0-github-io/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad/cc2d.py", "rb").read()).hexdigest() == "e6da46ef68bea7ede8de7dbefa0f9ada"
import cc2d as C
keys = ("astar", "c2", "cT", "c1", "F2", "Z21", "S2", "f_s", "fsum_resid_max", "static_resid_max", "collapsed_to_uniform")
out = {}; t0 = time.time()
def save(): json.dump(C.jsonable(out), open("table2_cc_rows.json", "w"), indent=1)
for g, ag in ((34.0, 1.4163), (20.0, 1.4664832858524572), (18.0, 1.4766667978121657), (15.0, 1.4946365046225132)):
    res, st = C.run_point("step", g, ag, N=64, stab_nq=0)
    out[f"g{g}"] = {k: res.get(k) for k in keys}
    print(f"[g={g}] " + " ".join(f"{k}={res.get(k)}" for k in keys[:8]) + f" ({time.time()-t0:.0f}s)", flush=True); save()
seed = None
for g, a in ((13.0, 1.5099592443626995), (12.9, 1.5109044165973526), (12.8, 1.5118912026209708), (12.7, 1.5129328893871443),
             (12.6, 1.5140526146768853), (12.5, 1.51529816851384), (12.45, 1.516002330056777), (12.4, 1.5168103105250197)):
    if g in (12.7, 12.5, 12.4):
        res, st = C.run_point("step", g, a, seed=seed, N=64, stab_nq=0)
        out[f"meta_g{g}"] = {k: res.get(k) for k in keys}
        print(f"[meta g={g}] " + " ".join(f"{k}={res.get(k)}" for k in keys[:8]) + f" ({time.time()-t0:.0f}s)", flush=True); save()
        seed = st
    else:
        seed = C.ground_state(C.hex_cell(a), C.Kernel("step", g), 64, 1.0, seed=seed)
print("TABLE2_CC_ROWS DONE", flush=True)
