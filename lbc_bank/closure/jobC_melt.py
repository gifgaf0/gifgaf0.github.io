#!/usr/bin/env python3
"""Corrected first leg, melting end: continue the crystal below the first leg's 'branch end' (12.47) with seeded
relaxation at the second leg's a* values, converge tightly, and test long-wavelength dynamical stability with the first
leg's own BdG pencil (raw lowest omega^2, unclipped) at |q|a/2pi = 0.03 and 0.05 along a1."""
import sys, json, time
import numpy as np
sys.path.insert(0, "/home/claude/sqt_persp/gate_tsh1_staging"); import g_tsh1_chatleg as T
sys.path.insert(0, "/home/claude/lbc_exploration"); from lbc_weights import bdg_full
from gsolve2d import tight, residual
from jobA_2d import measure
# a* of the second leg's branch table (qc_results.json); 12.37 interpolated between 12.40 and 12.35
pts = [(12.55, 1.514654767906371), (12.50, 1.51529816851384), (12.45, 1.516002330056777),
       (12.40, 1.5168103105250197), (12.37, 1.5174486), (12.35, 1.5178744771874821)]
out = []; seed = None; t0 = time.time()
for g, a in pts:
    st = T.relax_cell(a, g, "soft", Nc=96, psi_init=seed)
    st, _ = T.polish(st); st, rl, rn = tight(st)
    res, _, _ = residual(st["psi"], st["ge"], st["Uk"])
    rho = st["psi"]**2; contrast = float((rho.max()-rho.min())/rho.mean())
    unit = 2*np.pi/a; w2 = {}
    for kf in (0.03, 0.05, 0.075, 0.10):
        rr = T.bdg(st, g, "soft", kf*unit*np.array([1.0, 0.0]), n=32, want_modes=False)
        w2[kf] = rr["w2min"]
    rec = dict(g=g, a=a, residual=res, contrast=contrast, eps_minus_eps_u=float(st["E_area"]-np.pi*g/2), w2min=w2)
    if contrast > 0.05 and min(w2.values()) > 0:
        m = measure(st, g, "soft", a)
        rec.update(c2=m["c2"], cT=m["cT"], c1=m["c1"], ratio=m["c2"]/m["cT"], F2=m["F2"])
    out.append(rec); seed = st["psi"] if contrast > 0.05 else seed
    print(f"[g={g}] a={a:.5f} res={res:.1e} contrast={contrast:.2f} eps_c-eps_u={rec['eps_minus_eps_u']:+.4f} "
          f"w2min(kf .03/.05/.075/.10)={[f'{w2[k]:+.5f}' for k in w2]} "
          + (f"c2/cT={rec['ratio']:.4f} (c2={rec['c2']:.4f}, cT={rec['cT']:.4f})" if 'ratio' in rec else "c2/cT undefined")
          + f" ({time.time()-t0:.0f}s)", flush=True)
    json.dump(out, open("jobC_melt.json", "w"), indent=1, default=float)
print("JOB C DONE", flush=True)
