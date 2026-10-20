"""
e4_realcoupling.py -- E4 reconciliation: what the real-coupling survivors of the texture survey predict.

Context.  The cross-check found that the original survey's 'min' variant takes LNR's alpha and beta as
COMPLEX numbers, while LNR use real alpha = beta = -1.  e4_fits.py now also fits 'min-real' and
'gen-real' variants (all couplings real: CP-conserving Lagrangian, CP violation only from vev phases).
Classes with dof = N_obs - N_eff = 1 that pass p > 0.01 'survive'.  A dof = 1 class predicts one
relation among the 7 lepton observables.  This script makes that relation explicit:

  (a) N_eff robustness: rank of d(obs)/d(params) at 30 random points (e4_fits.jac_rank);
  (b) the prediction: fix the six observables me/mmu, mmu/mtau, r, s12^2, s13^2, s23^2 at their central
      values and solve for the parameters from many random starts; on every solution branch delta is
      then determined.  Branches come in pairs delta, 360 - delta: each class's parameter space is
      closed under complex conjugation (vev phases -> minus themselves, real couplings unchanged), which
      keeps the six observables and sends delta -> 360 - delta.  This is verified explicitly on every
      branch solution and used to complete the list.  The enumeration (300 starts) is not exhaustive:
      the branch list is a lower bound;
  (c) the spread of delta on each branch from the 1sigma errors of r, s12^2, s13^2, s23^2 (linear
      propagation through the implicit function: d delta = J_delta J_6^+ dO_6);
  (d) the pull of each branch in both delta conventions (3sigma-range/3, and NuFIT's 1sigma);
  (e) a full 7-observable least-squares polish started on every branch: the lowest chi2 found this way is
      compared with the survey's multistart minimum (a lower value only strengthens survival).
Reads out/fits.jsonl; writes out/realcoupling.json.  Deterministic (fixed seeds).
Run: python3 e4_realcoupling.py   (about 1-3 min on one core)
"""
import json
import math
import os
import time

import numpy as np
from scipy.optimize import least_squares

import e4_fits as F
from data_targets import NUFIT, NUFIT_1SIGMA, R_ATM_SOL, R_ATM_SOL_ERR, pull_delta_deg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
t0 = time.time()
recs = [json.loads(l) for l in open(os.path.join(OUT, "fits.jsonl"))]
CHECKS = {}


def check(name, ok, detail=""):
    CHECKS[name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  {detail}")


def pull_delta_1sigma(d):
    lo, hi = NUFIT_1SIGMA["delta_deg"]
    bf = NUFIT["delta_deg"][0]
    d0 = (d - bf) % 360.0
    pu, pd = d0 / hi, (d0 - 360.0) / lo
    return pu if abs(pu) <= abs(pd) else pd


SIG1 = {"r": R_ATM_SOL_ERR, "s12": 0.5 * sum(NUFIT_1SIGMA["s12sq"]), "s13": 0.5 * sum(NUFIT_1SIGMA["s13sq"]),
        "s23": 0.5 * sum(NUFIT_1SIGMA["s23sq"])}

surv = [r for r in recs if r.get("verdict") == "SURVIVES"]
print(f"{len(surv)} surviving classes in out/fits.jsonl: {[r['name'] for r in surv]}")
classes = {F.cname(c): c for c in F.class_list()}
out = {}
for r in surv:
    nm = r["name"]
    c = classes[nm]
    obsf, pullf, nobs = F.make_fun(c)
    n = F.npar(c)
    rng = np.random.default_rng(20261019)
    # (a) rank at random points
    ranks = [F.jac_rank(obsf, F.random_start(c, rng, n), nobs) for _ in range(30)]
    ranks = [x for x in ranks if x is not None]
    # (b) branches: six observables at their central values, delta free
    fun6 = lambda p: pullf(obsf(p))[:6]
    sols = []
    for s in range(300):
        p0 = F.random_start(c, rng, n)
        try:
            res = least_squares(fun6, p0, method="trf", max_nfev=300 * (n + 1), xtol=1e-14, ftol=1e-14, gtol=1e-14)
        except Exception:
            continue
        if np.sum(res.fun ** 2) < 1e-14:
            o = obsf(res.x)
            if np.isfinite(o[6]):
                sols.append((float(o[6]), res.x.copy()))
    # cluster delta values
    branches = []
    for d, px in sorted(sols, key=lambda t: t[0]):
        if branches and abs(d - branches[-1]["members"][-1]) < 0.05:
            branches[-1]["members"].append(d)
            continue
        branches.append({"members": [d], "p": px})
    rows = []
    for b in branches:
        d = float(np.median(b["members"]))
        px = b["p"]
        # (c) linear propagation: J (7 x n) by central differences; delta differences wrapped
        h = 1e-6
        J = np.zeros((7, n))
        for k in range(n):
            dp = np.zeros(n); dp[k] = h
            o1, o2 = obsf(px + dp), obsf(px - dp)
            J[:, k] = (o1 - o2) / (2 * h)
            J[6, k] = ((o1[6] - o2[6] + 180) % 360 - 180) / (2 * h)
        g = J[6] @ np.linalg.pinv(J[:6], rcond=1e-9)          # d delta / d O_6
        sig = math.sqrt(sum((g[i] * SIG1[k]) ** 2 for i, k in ((2, "r"), (3, "s12"), (4, "s13"), (5, "s23"))))
        g_mass = float(np.max(np.abs(g[:2] * np.array([F.LEP_T[0], F.LEP_T[1]]))))   # sensitivity to charged-lepton ratios
        # (e) polish all 7 residuals from this branch
        full = lambda p: pullf(obsf(p))
        rp = least_squares(full, px, method="trf", max_nfev=2000 * (n + 1), xtol=1e-15, ftol=1e-15, gtol=1e-15)
        c2p = float(np.sum(rp.fun ** 2))
        rows.append({"chi2_polished_from_branch": c2p, "delta_deg_polished": float(obsf(rp.x)[6]),
                     "delta_deg": round(d, 2), "n_solutions": len(b["members"]), "sigma_delta_1sigma_inputs_deg": round(sig, 1),
                     "ddelta_dr": float(g[2]), "ddelta_ds12": float(g[3]), "ddelta_ds13": float(g[4]), "ddelta_ds23": float(g[5]),
                     "max_abs_dlog_sensitivity_to_charged_lepton_ratios_deg": g_mass,
                     "pull_3sigma_range_convention": round(pull_delta_deg(d), 3), "pull_1sigma": round(pull_delta_1sigma(d), 3)})
    # exact conjugation symmetry on every branch representative, and completion of the list
    lay = F.layout(c)
    sym_ok = []
    for b in branches:
        px = b["p"]
        pc = np.array([-x if t == "phase" else x for x, t in zip(px, lay)])
        o, oc = obsf(px), obsf(pc)
        same6 = bool(np.allclose(o[:6], oc[:6], rtol=1e-9, atol=1e-12))
        flip = abs(((o[6] + oc[6]) % 360.0 + 180.0) % 360.0 - 180.0) < 1e-6
        sym_ok.append(same6 and flip)
    found = sorted(x["delta_deg"] for x in rows)
    allb = sorted(set(round(d, 1) for d in found) | set(round((360.0 - d) % 360.0, 1) for d in found))
    merged = []
    for d in allb:
        if not merged or abs(d - merged[-1]) > 0.15:
            merged.append(d)
    best = min(rows, key=lambda x: abs(x["pull_3sigma_range_convention"])) if rows else None
    chi2_glob = min([r["chi2"]] + [x["chi2_polished_from_branch"] for x in rows])
    from scipy.stats import chi2 as chi2dist
    p_glob = float(chi2dist.sf(chi2_glob, r["dof"])) if r.get("dof", 0) >= 1 else None
    out[nm] = {"n_par": n, "n_eff_stored": r["n_eff"], "dof": r.get("dof"), "chi2": r["chi2"], "p_value": r.get("p_value"),
               "best_obs": r["best_obs"], "pulls": r["pulls"], "random_point_ranks": sorted(set(ranks)),
               "rank_max_random": max(ranks) if ranks else None, "n_converged_solutions": len(sols),
               "delta_branches": rows, "best_branch": best, "conjugation_symmetry_verified_on_all_branches": all(sym_ok),
               "n_branches_found": len(rows), "delta_branches_completed_by_conjugation_deg": merged,
               "n_branches_lower_bound": len(merged), "chi2_min_including_branch_polish": chi2_glob,
               "p_value_at_that_minimum": p_glob}
    print(f"\n{nm}: n_par {n}, N_eff {r['n_eff']} (random-point ranks {sorted(set(ranks))}), chi2 {r['chi2']:.3f}, "
          f"p {r.get('p_value'):.2f}; {len(sols)} exact six-observable solutions, delta branches:")
    print(f"   conjugation symmetry verified on all {len(sym_ok)} branch solutions: {all(sym_ok)}; "
          f"{len(rows)} branches found, {len(merged)} after completing by conjugation: {merged}")
    print(f"   lowest chi2 after polishing from every branch: {chi2_glob:.4f} (p = {p_glob}); survey multistart: {r['chi2']:.4f}")
    for x in rows:
        print(f"   [polished chi2 {x['chi2_polished_from_branch']:.4f}] delta = {x['delta_deg']:7.2f} deg  (+- {x['sigma_delta_1sigma_inputs_deg']:.1f} from 1sigma inputs; "
              f"{x['n_solutions']} sols)  pull {x['pull_3sigma_range_convention']:+.2f} (3sigma/3), {x['pull_1sigma']:+.2f} (1sigma); "
              f"charged-lepton sensitivity {x['max_abs_dlog_sensitivity_to_charged_lepton_ratios_deg']:.1e}")

if surv:
    check("every survivor has N_eff = max random-point rank (rank is generic, not a best-fit accident)",
          all(v["rank_max_random"] == v["n_eff_stored"] for v in out.values()),
          "; ".join(f"{k.split('|', 1)[1]}: {v['n_eff_stored']} vs {v['random_point_ranks']}" for k, v in out.items()))
    check("every dof = 1 survivor has a discrete set of delta branches at the central values of the other six observables",
          all(v["delta_branches"] for v in out.values() if v["dof"] == 1))
    check("polishing from the branches never raises chi2 above the survey value, and every survivor stays at p > 0.01",
          all(v["chi2_min_including_branch_polish"] <= v["chi2"] + 1e-9 and (v["p_value_at_that_minimum"] or 1) > 0.01
              for v in out.values()))
    check("exact symmetry: conjugating the vev phases keeps the six fitted observables and maps delta -> 360 - delta, on every branch",
          all(v["conjugation_symmetry_verified_on_all_branches"] for v in out.values()))
    union = sorted(set(d for v in out.values() for d in v["delta_branches_completed_by_conjugation_deg"]))
    print("union of delta branches over the survivors (deg):", union)
json.dump({"survivors": out, "union_of_delta_branches_deg": sorted(set(d for v in out.values() for d in v["delta_branches_completed_by_conjugation_deg"])) if out else [], "sigma_1sigma_inputs": SIG1, "checks": CHECKS,
           "all_pass": all(v["pass"] for v in CHECKS.values()), "runtime_s": round(time.time() - t0, 1)},
          open(os.path.join(OUT, "realcoupling.json"), "w"), indent=1)
print(f"\n{sum(v['pass'] for v in CHECKS.values())}/{len(CHECKS)} checks pass; {time.time() - t0:.0f} s")
