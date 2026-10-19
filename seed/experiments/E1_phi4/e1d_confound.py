"""E1d reconciliation: is the matched-energy speed preference a speed effect or an amplitude effect?

The cross-check pointed out that at matched energy slow packets carry larger amplitude A, and
that production is controlled by A. This script tests the speed dependence with A held fixed,
on the stored coarse-grid calls (no new simulations):

 1. matched-energy bands [2,4), [4,8), [8,16) (E/2M): mean A against group velocity v_g;
 2. stratified permutation tests (runs with E > 2M only). Statistic: sum over strata of
    Spearman-free association  S = sum_strata sum_runs (P - Pbar_stratum)(v_g - vbar_stratum);
    S < 0 means slower packets produce more within strata. Null: production labels permuted
    within each stratum (20000 permutations, fixed seed). Strata:
      (a) fixed A                      (speed and energy both vary; sigma pooled)
      (b) fixed (A, sigma)             (only k varies: faster = more energy)
      (c) fixed (E/2M band, A bin)     (matched energy and amplitude; sigma compensates)
    for all production and for collision-needed production (single packet alone makes no pair),
    in both initial-velocity forms;
 3. logistic regressions (E > 2M):  P ~ log A + log sigma + v_g  and  P ~ log A + log E + v_g,
    coefficients with Wald standard errors (IRLS).
Writes e1d_confound.json.
"""
import json
import numpy as np
from phi4core import M_KINK

rng = np.random.default_rng(20261019)
NPERM = 20000


def load(form):
    if form == "baseline":
        pair = json.load(open("e1d_coarse.json"))["runs"]
        single = json.load(open("e1d_single.json"))["runs"]
    else:
        pair = [json.loads(l) for l in open("e1d_coarse_oneway.jsonl") if l.strip()]
        single = [json.loads(l) for l in open("e1d_single_oneway.jsonl") if l.strip()]
    sp = {(r["A"], r["sigma"], r["k"]): r["produced"] for r in single}
    rows = []
    for r in pair:
        key = (r["A"], r["sigma"], r["k"])
        P = bool(r["produced"])
        Pc = P and not sp.get(key, False)
        if P and key not in sp:
            raise RuntimeError(f"missing single-packet control for {key}")
        rows.append((r["A"], r["sigma"], r["k"], r["vg"], r["E_over_2M"], P, Pc))
    a = np.array(rows, dtype=float)
    return {"A": a[:, 0], "sigma": a[:, 1], "k": a[:, 2], "vg": a[:, 3], "E": a[:, 4],
            "P": a[:, 5], "Pc": a[:, 6]}


def strat_perm(P, v, strata):
    """Within-stratum covariance statistic and permutation p-values (two-sided and one-sided)."""
    groups = [np.where(strata == s)[0] for s in np.unique(strata)]
    groups = [g for g in groups if len(g) >= 2 and 0 < P[g].sum() < len(g)]
    if not groups:
        return {"n_informative_strata": 0}
    vc = [v[g] - v[g].mean() for g in groups]
    Ps = [P[g] for g in groups]
    S = float(sum(np.dot(p - p.mean(), c) for p, c in zip(Ps, vc)))
    null = np.zeros(NPERM)
    for i in range(NPERM):
        null[i] = sum(np.dot(rng.permutation(p), c) for p, c in zip(Ps, vc))
    # scale: express S as a mean within-stratum difference in v_g (producing minus all)
    nprod = sum(p.sum() for p in Ps)
    return {"n_informative_strata": len(groups), "n_runs": int(sum(len(g) for g in groups)),
            "n_producing": int(nprod), "S": S,
            "mean_vg_shift_of_producers": S / nprod,
            "p_two_sided": float((np.sum(np.abs(null) >= abs(S) - 1e-12) + 1) / (NPERM + 1)),
            "p_slower_produces_more": float((np.sum(null <= S + 1e-12) + 1) / (NPERM + 1))}


def logit(X, y, names):
    X = np.column_stack([np.ones(len(y)), X])
    b = np.zeros(X.shape[1])
    for _ in range(100):
        eta = X @ b
        p = 1.0 / (1.0 + np.exp(-eta))
        W = p * (1 - p) + 1e-12
        H = X.T @ (X * W[:, None])
        g = X.T @ (y - p)
        step = np.linalg.solve(H, g)
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    p = 1.0 / (1.0 + np.exp(-(X @ b)))
    H = X.T @ (X * (p * (1 - p))[:, None])
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    pc = np.clip(p, 1e-15, 1 - 1e-15)
    dev = float(-2.0 * np.sum(y * np.log(pc) + (1 - y) * np.log(1 - pc)))
    out = {n: {"coef": float(bb), "se": float(s), "z": float(bb / s)}
           for n, bb, s in zip(["const"] + names, b, se)}
    out["deviance"] = {"coef": dev, "se": 0.0, "z": 0.0}
    return out


out = {"notes": "runs with E > 2 M_kink only, except item 1; v_g = k / sqrt(k^2 + 2); "
                "P = pair run produces; Pc = pair run produces and the single packet alone does not"}
for form in ("baseline", "oneway"):
    d = load(form)
    res = {}
    # 1. matched-energy bands
    vgs = np.unique(np.round(d["vg"], 6))
    bands = {}
    for lo, hi in ((2, 4), (4, 8), (8, 16)):
        m = (d["E"] >= lo) & (d["E"] < hi)
        rows = []
        for v in vgs:
            mm = m & (np.abs(d["vg"] - v) < 1e-6)
            if mm.sum() >= 3:
                rows.append({"vg": round(float(v), 4), "n": int(mm.sum()), "mean_A": round(float(d["A"][mm].mean()), 3),
                             "frac_P": round(float(d["P"][mm].mean()), 3)})
        bands[f"[{lo},{hi})"] = rows
    res["matched_energy_bands"] = bands
    # 2. stratified permutation tests
    m = d["E"] > 1.0
    Aq = np.round(d["A"][m], 3)
    sq = d["sigma"][m]
    Eb = np.digitize(d["E"][m], [2, 3, 4, 6, 8, 12, 16, 24, 32, 64])
    strata = {"fixed_A": Aq, "fixed_A_sigma": Aq * 1000 + sq,
              "fixed_Eband_A": Eb * 1000 + np.round(Aq * 10)}
    tests = {}
    for lab, P in (("all", d["P"][m]), ("collision_needed", d["Pc"][m])):
        for sn, st in strata.items():
            tests[f"{lab}__{sn}"] = strat_perm(P, d["vg"][m], st)
    res["stratified_tests"] = tests
    # 3. logistic regressions
    X1 = np.column_stack([np.log(d["A"][m]), np.log(d["sigma"][m]), d["vg"][m]])
    X2 = np.column_stack([np.log(d["A"][m]), np.log(d["E"][m]), d["vg"][m]])
    X0 = np.column_stack([np.log(d["A"][m]), np.log(d["sigma"][m])])
    res["logit"] = {}
    for lab, P in (("all", d["P"][m]), ("collision_needed", d["Pc"][m])):
        res["logit"][lab] = {"P~logA+logsigma": logit(X0, P, ["logA", "logsigma"]),
                             "P~logA+logsigma+vg": logit(X1, P, ["logA", "logsigma", "vg"]),
                             "P~logA+logE+vg": logit(X2, P, ["logA", "logE", "vg"])}
    res["n_runs_E_gt_2M"] = int(m.sum())
    out[form] = res

json.dump(out, open("e1d_confound.json", "w"), indent=1)
for form in ("baseline", "oneway"):
    print(f"=== {form}")
    for b, rows in out[form]["matched_energy_bands"].items():
        print(" band", b, [(r["vg"], r["mean_A"], r["frac_P"]) for r in rows])
    for k, t in out[form]["stratified_tests"].items():
        if t.get("n_informative_strata"):
            print(f" {k:34s} strata={t['n_informative_strata']:3d} runs={t['n_runs']:4d} prod={t['n_producing']:4d} "
                  f"dvg={t['mean_vg_shift_of_producers']:+.4f} p2={t['p_two_sided']:.4f} p(slow>)={t['p_slower_produces_more']:.4f}")
    for lab, mods in out[form]["logit"].items():
        for mn, co in mods.items():
            print(f" logit {lab:17s} {mn:22s}", {k: (round(v['coef'], 3), round(v['z'], 2)) for k, v in co.items()})
