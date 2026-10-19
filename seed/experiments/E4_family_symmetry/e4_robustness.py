"""
e4_robustness.py -- E4 part 4c: robustness of the texture fits (added when the interrupted run was resumed).
  (a) determinism: refit six classes from scratch (fits finished before AND after the container
      restart) and compare chi2, N_eff and verdict with out/fits.jsonl;
  (b) global-minimum check: the four non-structural 'excluded' lepton classes with dof = 0 all stop at
      chi2 = 72.49; refit one of them (lepton|min|phi10=Z3|phi5=G|phi1=Z3) from 300 random starts.
Writes out/robustness.json.  Run: python3 e4_robustness.py   (about 3 min on one core)
"""
import json
import os
import time

import numpy as np
from scipy.optimize import least_squares

import e4_fits as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
t0 = time.time()
stored = {json.loads(l)["name"]: json.loads(l) for l in open(os.path.join(OUT, "fits.jsonl"))}
want = ["lepton|min|phi10=Z3|phi5=G|phi1=Z3", "lepton|min|phi10=G|phi5=Z3|phi1=Z3",
        "lepton|min|phi10=G|phi5=Z3|phi1=P", "quark|min|phi10=G|phi5=G",
        "quark|gen|phi10=G|phi5=Z3", "lepton|LNR exact|phi10=G|phi5=(-1,1,1)|phi1=(1,1,1)"]
refits = []
for c in F.class_list():
    nm = F.cname(c)
    if nm not in want:
        continue
    rec = F.fit_class(c, None)
    rec["verdict"] = F.verdict(rec)
    s = stored[nm]
    same = (rec["n_eff"] == s["n_eff"] and rec["verdict"] == s["verdict"]
            and abs(rec["chi2"] - s["chi2"]) <= 1e-9 * max(1.0, abs(s["chi2"])) + 1e-15)
    refits.append({"name": nm, "chi2_new": rec["chi2"], "chi2_stored": s["chi2"], "n_eff_new": rec["n_eff"],
                   "n_eff_stored": s["n_eff"], "verdict_new": rec["verdict"], "verdict_stored": s["verdict"],
                   "identical": bool(same)})
    print(f"refit {nm}: chi2 {rec['chi2']:.6g} (stored {s['chi2']:.6g}), N_eff {rec['n_eff']} ({s['n_eff']}), "
          f"{rec['verdict']} -> {'identical' if same else 'DIFFERENT'}")

c = {"sector": "lepton", "variant": "min", "phi10": "Z3", "phi5": "G", "phi1": "Z3"}
obsf, pullf, nobs = F.make_fun(c)
n = F.npar(c)
rng = np.random.default_rng(2026)
fun = lambda p: pullf(obsf(p))
vals = []
for s in range(300):
    p0 = F.random_start(c, rng, n)
    r = least_squares(fun, p0, method="trf", max_nfev=200 * (n + 1), xtol=1e-12, ftol=1e-12, gtol=1e-12)
    vals.append(float(np.sum(r.fun ** 2)))
vals = np.sort(vals)
ms = {"class": F.cname(c), "n_starts": 300, "chi2_min": float(vals[0]), "five_smallest": vals[:5].tolist(),
      "fraction_within_0.1_of_min": float(np.mean(vals < vals[0] + 0.1)),
      "stored_chi2_after_polish": stored[F.cname(c)]["chi2"]}
print(f"300 starts on {ms['class']}: min chi2 {ms['chi2_min']:.4f} (stored, polished: {ms['stored_chi2_after_polish']:.4f}); "
      f"fraction of starts within 0.1 of the minimum {ms['fraction_within_0.1_of_min']:.2f}")
checks = {"six refits identical to the stored fits": all(r["identical"] for r in refits),
          "300-start minimum within 0.1 of the stored chi2 (no lower minimum found)":
              ms["chi2_min"] > ms["stored_chi2_after_polish"] - 0.1}
for k, v in checks.items():
    print(f"[{'PASS' if v else 'FAIL'}] {k}")
json.dump({"refits": refits, "many_starts": ms, "checks": checks, "all_pass": all(checks.values()),
           "runtime_s": time.time() - t0}, open(os.path.join(OUT, "robustness.json"), "w"), indent=1)
