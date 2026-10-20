#!/usr/bin/env python3
"""
E3 part 5b: radial refinement of the Ritz spectra at fixed box R = 20, for the long block and the
kaon block (whose spectrum equals the (2,4) block's, see e3_stability.py).  The lowest eigenvalues
(zero modes: iso-rotations / G2 rotations, translations) should fall towards 0 as the radial mesh
is refined, while no eigenvalue becomes negative.
Writes stability_refine_results.json.
"""
import json
import time
import numpy as np
import e3_stability as st

t0 = time.time()
out = {}
for sec in ["long (3,1)", "kaon (su(3) part of (2,4))"]:
    out[sec] = {}
    for nr in (15, 30, 60, 90):
        ev = st.ritz(sec, R=20.0, nr=nr, lmax=3, nev=10)
        out[sec][str(nr)] = ev.tolist()
        print(f"{sec:28s} R=20 nr={nr:3d}: lowest {np.array2string(ev[:8], precision=3)}   [{time.time()-t0:.0f}s]", flush=True)
out["min_eigenvalue"] = min(min(v) for s in out.values() if isinstance(s, dict) for v in s.values())
print("minimum eigenvalue over all refinements:", out["min_eigenvalue"])
with open("stability_refine_results.json", "w") as fh:
    json.dump(out, fh, indent=1)
