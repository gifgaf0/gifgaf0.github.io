"""
cc_minreal_detail.py -- sensitivity test (NOT part of the original survey): the LNR 'min' classes with REAL
alpha, beta (LNR's own convention: integer alpha = beta = -1, 'neglecting phases').
For each minreal class with dof >= 1 that is not structurally dead:
  (1) refit from 60 starts (deterministic seed) -> chi2, p, observables;
  (2) refit WITHOUT the delta term from 60 starts; every exact solution (chi2_6 < 1e-8) gives a delta value:
      this is what the one remaining degree of freedom predicts.
Writes out/minreal_detail.json.
"""
import json, math, sys, zlib
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2 as chi2dist
sys.path.insert(0, "/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck")
import cc_texture as T

base = T.base
recs = [json.loads(l) for l in open(base + "texture_cc_minreal.jsonl") if l.strip()]
targets = [r["name"] for r in recs if r["verdict"] != "excluded (structural)" and r["dof"] >= 1]
print("minreal classes with dof >= 1 (not dead):", targets)
cls = {c[0]: c for c in T.classes(include_minreal=True)}
out = {}
for name in targets:
    _, sector, npar, obs = cls[name]
    f = T.residual_fn(sector, obs)
    rng = np.random.default_rng(zlib.crc32(("detail" + name).encode()))
    c, px = T.fit(f, npar, rng, 60)
    ne = T.n_eff(f, npar, rng, p_best=px)
    dof = 7 - ne
    p = float(1 - chi2dist.cdf(c, dof))
    o, _ = obs(px)
    pulls = f(px)
    f6 = lambda q: f(q)[:6]
    deltas = []
    for k in range(60):
        q0 = T.random_point(rng, npar)
        try:
            r = least_squares(f6, q0, method="trf", max_nfev=300 * (npar + 1), xtol=1e-13, ftol=1e-13, gtol=1e-13)
        except Exception:
            continue
        if np.sum(r.fun ** 2) < 1e-8:
            oo, _ = obs(r.x)
            if oo["delta"] is not None: deltas.append(round(oo["delta"], 2))
    dset = sorted(set(round(d, 0) for d in deltas))
    out[name] = dict(npar=npar, n_eff=ne, dof=dof, chi2=c, p=p, obs={k: o[k] for k in ("me_mmu", "mmu_mtau", "r", "s12sq", "s13sq", "s23sq", "delta")},
                     pulls=list(map(float, pulls)), best_p=list(map(float, px)), delta_from_exact_6obs_fits=dset, n_exact=len(deltas))
    print(f"{name}: npar={npar} neff={ne} dof={dof} chi2={c:.4g} p={p:.3g}")
    print("   obs:", {k: (round(v, 5) if v is not None else None) for k, v in out[name]["obs"].items()})
    print("   pulls:", np.round(pulls, 3))
    print(f"   delta predicted by exact fits to the other 6 observables ({len(deltas)} solutions): {dset}")
json.dump(out, open(base + "minreal_detail.json", "w"), indent=1, default=str)
