"""E1d reconciliation, decisive test: at FIXED packet shape (A, sigma), does a slower packet produce more?

Why. On the coarse grid slower packets produce more at matched energy (Spearman -0.8 to -0.9), but at matched energy
a slow packet is taller (or wider) than a fast one, and amplitude controls production (cross-check issue M3). The
stored coarse grid has one call per (A, sigma, k), and ~20% of single calls flip under refinement or a shift of the
collision phase. This scan replaces each call by a production probability: the fraction of 8 collision phases
(x0 shifted over one carrier-phase period 2 pi k / m^2 in 8 steps, as in e1d_gauss.py 'phase') that produce.

Design (fixed before any run of this script):
  A in {0.5, 0.6, 0.7, 0.8, 0.9, 1.0}, sigma in {2, 4, 8}, k in the coarse set (v_g = 0.17-0.90),
  8 collision phases each, both initial-velocity forms (baseline narrow-band and exact one-way), dx = 0.1,
  dt = 0.04; plus one single-packet control per (A, sigma, k, form). Everything else (x0 = 4 sigma + 10 + shift,
  T, box, absorbing layer, pair test with persistence over 0.8T-T) is exactly e1d_gauss.py / e1d_extra.py.
  Resolution check: the baseline form at sigma = 4 repeated at dx = 0.05, dt = 0.02.
Statistics (e1d_speedtest_analysis in this file, run with argument 'analyze'):
  * all production: logistic P ~ (one intercept per shape (A, sigma)) + v_g, over shapes whose 72 runs are not all
    alike; coefficient of v_g with Wald 95% CI; stratified permutation test (k labels permuted within shape).
  * collision-needed production: the same, restricted to (A, sigma, k) whose single packet does not produce.
Decision rule (fixed in advance): the matched-energy speed preference is a speed effect if the v_g coefficient is
  below 0 with p < 0.05 in both forms; it is NOT a speed effect if in both forms the 95% CI excludes -1.19, half the
  matched-energy coefficient -2.38 (logistic P ~ log A + log E + v_g, e1d_confound.json); otherwise undecided.
Usage: python e1d_speedtest.py run [nproc]     (resumable; checkpoint e1d_speedtest.jsonl)
       python e1d_speedtest.py analyze          (writes e1d_speedtest.json)
"""
import sys
import os
import json
import time
import numpy as np
from multiprocessing import Pool
import e1d_gauss as G
from e1d_extra import oneway_initial
from phi4core import grid, Sim, count_pairs, PERSIST_FRACS, energy_density

OUT = "e1d_speedtest.jsonl"
A_SET = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
S_SET = (2.0, 4.0, 8.0)
K_SET = tuple(float(k) for k in G.K_COARSE)
NPH = 8
M2 = 2.0
HALF_MATCHED = -2.3841486947439554 / 2      # e1d_confound.json, baseline, all, P~logA+logE+vg


def key_of(A, s, k, form, q, dx, single):
    return f"{form}_A{A:.2f}_s{s:g}_k{k:g}_q{q}_dx{dx:g}_{'single' if single else 'pair'}"


def run_one(job):
    A, s, k, form, q, dx, single = job
    shift = q * (2 * np.pi * k / M2) / NPH
    vg, x0, t_coll, T, Lphys = G.setup(A, s, k, shift)
    x = grid(Lphys + G.WSP, dx)
    if form == "oneway":
        phi, pi = oneway_initial(x, A, s, k, x0, single=single)
    else:
        phi, pi = G.gauss_initial(x, A, s, k, x0, single=single)
    dt = G.CFL * dx
    E0 = float(np.sum(energy_density(phi, pi, dx, -1.0, -1.0)) * dx)
    sim = Sim(x, phi, pi, dt, Lphys=Lphys, W=G.WSP, gmax=G.GMAX)
    nT = int(round(T / dt))
    done, persist = 0, []
    for m in sorted({int(round(f * nT)) for f in PERSIST_FRACS}):
        sim.run(m - done)
        done = m
        persist.append(count_pairs(x, sim.phi))
    return {"key": key_of(*job), "A": A, "sigma": s, "k": k, "vg": vg, "form": form, "phase_index": q,
            "x0_shift": shift, "dx": dx, "single": single, "E_over_2M": E0 / G.TWO_M,
            "produced": bool(all(n >= 1 for n in persist)), "npairs_persist": persist}


def jobs_list():
    J = []
    for form in ("baseline", "oneway"):
        for A in A_SET:
            for s in S_SET:
                for k in K_SET:
                    J.append((A, s, k, form, 0, 0.1, True))
                    J += [(A, s, k, form, q, 0.1, False) for q in range(NPH)]
    for A in A_SET:
        for k in K_SET:
            J.append((A, 4.0, k, "baseline", 0, 0.05, True))
            J += [(A, 4.0, k, "baseline", q, 0.05, False) for q in range(NPH)]
    return J


def run(nproc):
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            try:
                done.add(json.loads(l)["key"])
            except (json.JSONDecodeError, KeyError):
                pass
    todo = [j for j in jobs_list() if key_of(*j) not in done]
    todo.sort(key=lambda j: -G.setup(j[0], j[1], j[2])[3] * G.setup(j[0], j[1], j[2])[4] / j[5] ** 2)
    print(f"{len(done)} done, {len(todo)} to run", flush=True)
    t0 = time.time()
    with Pool(nproc) as pool, open(OUT, "a") as f:
        for i, r in enumerate(pool.imap_unordered(run_one, todo, chunksize=4)):
            f.write(json.dumps(r) + "\n")
            f.flush()
            if (i + 1) % 200 == 0:
                print(f"{i + 1}/{len(todo)} {time.time() - t0:.0f} s", flush=True)
    print(f"all done, {time.time() - t0:.0f} s", flush=True)


# ------------------------------------------------------------------------------------------------ analysis
def logit_fe(y, v, strata):
    """Logistic regression with one intercept per stratum and a common slope on v. Returns slope, se, z."""
    us = np.unique(strata)
    X = np.zeros((len(y), len(us) + 1))
    for i, u in enumerate(us):
        X[strata == u, i] = 1.0
    X[:, -1] = v
    b = np.zeros(X.shape[1])
    for _ in range(200):
        p = 1.0 / (1.0 + np.exp(-(X @ b)))
        W = p * (1 - p) + 1e-12
        H = X.T @ (X * W[:, None]) + 1e-9 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p))
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    p = 1.0 / (1.0 + np.exp(-(X @ b)))
    H = X.T @ (X * (p * (1 - p))[:, None]) + 1e-9 * np.eye(X.shape[1])
    se = float(np.sqrt(np.linalg.inv(H)[-1, -1]))
    return float(b[-1]), se


def perm_test(y, v, strata, nperm=20000, seed=11):
    rng = np.random.default_rng(seed)
    groups = [np.where(strata == u)[0] for u in np.unique(strata)]
    vc = [v[g] - v[g].mean() for g in groups]
    ys = [y[g] for g in groups]
    S = sum(float(np.dot(a, c)) for a, c in zip(ys, vc))
    null = np.array([sum(float(np.dot(rng.permutation(a), c)) for a, c in zip(ys, vc)) for _ in range(nperm)])
    return S, float((np.sum(np.abs(null) >= abs(S) - 1e-12) + 1) / (nperm + 1)), \
        float((np.sum(null <= S + 1e-12) + 1) / (nperm + 1))


def analyze():
    from scipy.stats import spearmanr
    rs = [json.loads(l) for l in open(OUT) if l.strip()]
    out = {"design": {"A": A_SET, "sigma": S_SET, "k": K_SET, "n_phases": NPH,
                      "decision_rule": "speed effect if v_g coefficient < 0 with p < 0.05 in both forms; not a speed "
                                       f"effect if in both forms the 95% CI excludes {HALF_MATCHED:.3f} (half the "
                                       "matched-energy coefficient); else undecided"},
           "n_runs": len(rs)}
    for form, dx in (("baseline", 0.1), ("oneway", 0.1), ("baseline", 0.05)):
        pair = [r for r in rs if r["form"] == form and r["dx"] == dx and not r["single"]]
        sing = {(r["A"], r["sigma"], r["k"]): r["produced"] for r in rs
                if r["form"] == form and r["dx"] == dx and r["single"]}
        if not pair:
            continue
        y = np.array([r["produced"] for r in pair], float)
        v = np.array([r["vg"] for r in pair])
        st = np.array([round(r["A"] * 10) * 100 + r["sigma"] for r in pair])
        nsf = np.array([not sing.get((r["A"], r["sigma"], r["k"]), True) for r in pair])
        res = {"n_pair_runs": len(pair), "n_producing": int(y.sum())}
        for lab, mask in (("all", np.ones(len(y), bool)), ("non_self_folding_packets", nsf)):
            yy, vv, ss = y[mask], v[mask], st[mask]
            keep = np.isin(ss, [u for u in np.unique(ss) if 0 < yy[ss == u].sum() < (ss == u).sum()])
            if keep.sum() < 10:
                res[lab] = {"n_informative_shapes": 0}
                continue
            b, se = logit_fe(yy[keep], vv[keep], ss[keep])
            S, p2, p1 = perm_test(yy[keep], vv[keep], ss[keep])
            pz = float(2 * (1 - 0.5 * (1 + __import__("math").erf(abs(b / se) / np.sqrt(2)))))
            # phase-averaged production probability per (shape, k), and per-shape Spearman over k
            per_shape = []
            for u in np.unique(ss):
                m = ss == u
                ks = sorted(set(vv[m]))
                prob = [float(yy[m][vv[m] == q].mean()) for q in ks]
                rho = spearmanr(ks, prob)[0] if len(ks) > 2 and np.std(prob) > 0 else None
                per_shape.append({"A": round((int(u) // 100) / 10, 2),
                                  "sigma": float(u % 100), "vg": [round(q, 4) for q in ks],
                                  "P_phase_avg": prob, "spearman_vg": None if rho is None else float(rho)})
            vgs = sorted(set(vv))
            res[lab] = {"n_runs": int(mask.sum()), "n_informative_shapes": int(len(np.unique(ss[keep]))),
                        "n_runs_informative": int(keep.sum()), "n_producing": int(yy.sum()),
                        "vg_coef": b, "vg_se": se, "vg_ci95": [b - 1.96 * se, b + 1.96 * se], "p_wald": pz,
                        "perm_S": S, "perm_p_two_sided": p2, "perm_p_slower_produces_more": p1,
                        "P_vs_vg_pooled": {f"{q:.4f}": float(yy[vv == q].mean()) for q in vgs},
                        "n_shapes_spearman_neg_lt_-0.6": int(sum(1 for s_ in per_shape if s_["spearman_vg"] is not None
                                                                 and s_["spearman_vg"] < -0.6)),
                        "n_shapes_spearman_pos_gt_0.6": int(sum(1 for s_ in per_shape if s_["spearman_vg"] is not None
                                                                and s_["spearman_vg"] > 0.6)),
                        "per_shape": per_shape}
        res["single_packet_self_folds"] = {f"A{a:.1f}_s{s:g}": [sing.get((a, s, k)) for k in K_SET]
                                           for a in A_SET for s in S_SET if (a, s, K_SET[0]) in sing}
        out[f"{form}_dx{dx:g}"] = res
    # paired resolution check: baseline sigma = 4 at dx 0.1 vs 0.05
    a = {(r["A"], r["k"], r["phase_index"]): r["produced"] for r in rs
         if r["form"] == "baseline" and r["dx"] == 0.1 and r["sigma"] == 4.0 and not r["single"]}
    b_ = {(r["A"], r["k"], r["phase_index"]): r["produced"] for r in rs
          if r["form"] == "baseline" and r["dx"] == 0.05 and r["sigma"] == 4.0 and not r["single"]}
    com = sorted(set(a) & set(b_))
    if com:
        pa = {}
        pb = {}
        for (A, k, q) in com:
            pa.setdefault((A, k), []).append(a[(A, k, q)])
            pb.setdefault((A, k), []).append(b_[(A, k, q)])
        fa = np.array([np.mean(pa[c]) for c in sorted(pa)])
        fb = np.array([np.mean(pb[c]) for c in sorted(pb)])
        out["resolution_check_sigma4_baseline"] = {
            "n_common_runs": len(com), "call_agreement": float(np.mean([a[c] == b_[c] for c in com])),
            "phase_avg_prob_corr": float(np.corrcoef(fa, fb)[0, 1]) if np.std(fa) > 0 and np.std(fb) > 0 else None,
            "phase_avg_prob_mean_abs_diff": float(np.mean(np.abs(fa - fb)))}
    dec = {}
    for lab in ("all", "non_self_folding_packets"):
        r1, r2 = out.get("baseline_dx0.1", {}).get(lab, {}), out.get("oneway_dx0.1", {}).get(lab, {})
        if not r1.get("n_informative_shapes") or not r2.get("n_informative_shapes"):
            dec[lab] = "undecided (too few informative shapes)"
            continue
        neg = all(r["vg_ci95"][1] < 0 for r in (r1, r2))
        nospeed = all(r["vg_ci95"][0] > HALF_MATCHED for r in (r1, r2))
        dec[lab] = "speed effect" if neg else ("not a speed effect" if nospeed else "undecided")
    out["decision"] = dec
    json.dump(out, open("e1d_speedtest.json", "w"), indent=1)
    for kf in ("baseline_dx0.1", "oneway_dx0.1", "baseline_dx0.05"):
        if kf in out:
            for lab in ("all", "non_self_folding_packets"):
                r = out[kf].get(lab, {})
                if r.get("n_informative_shapes"):
                    print(f"{kf:16s} {lab:25s} shapes={r['n_informative_shapes']:2d} runs={r['n_runs_informative']:4d} "
                          f"prod={r['n_producing']:4d} vg_coef={r['vg_coef']:+.3f} CI=[{r['vg_ci95'][0]:+.3f}, "
                          f"{r['vg_ci95'][1]:+.3f}] p={r['p_wald']:.3g} perm p2={r['perm_p_two_sided']:.3g} "
                          f"p(slow>)={r['perm_p_slower_produces_more']:.3g} rho<-0.6: {r['n_shapes_spearman_neg_lt_-0.6']} "
                          f"rho>0.6: {r['n_shapes_spearman_pos_gt_0.6']}")
                    print("   pooled P vs vg:", {k_: round(p_, 3) for k_, p_ in r["P_vs_vg_pooled"].items()})
    print("resolution check:", out.get("resolution_check_sigma4_baseline"))
    print("decision:", dec)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(int(sys.argv[2]) if len(sys.argv) > 2 else 2)
    else:
        analyze()
