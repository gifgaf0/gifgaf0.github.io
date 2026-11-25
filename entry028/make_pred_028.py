"""make_pred_028.py [N_PER] -- freeze-candidate predictions, tolerance and power for Entry 028.
Reads pred/*.json (archived-predictor ladder values on the band, Q0=60 hybrid node files, discrete
(2.16) strata). Writes pred_028.json and prints every number for review."""
import os as _os; PRED = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "pred")
import json, math, sys, numpy as np
from scipy import stats
from band_028 import nodes, LO, HI
NPER = float(sys.argv[1]) if len(sys.argv) > 1 else 1.25e7
Q = {"chi-3": 3, "chi-4": 4, "leg5": 5}; NAMES = ["chi-3", "chi-4", "leg5"]
A = 0.01 / 6; z1 = round(float(stats.norm.isf(A)), 4); z2 = round(float(stats.norm.isf(A / 2)), 4); z80 = float(stats.norm.ppf(0.8))
L = lambda kind, q, n: json.load(open(f"{PRED}/ladder_{kind}_q{q}_n{n}.json"))["corr"]
H4 = [json.load(open(f"{PRED}/hyb_n4_node{i}.json")) for i in range(4)]
import os
H2 = [json.load(open(f"{PRED}/hyb_n2_node{i}.json")) for i in range(2)] if os.path.exists(PRED + "/hyb_n2_node1.json") else None
D = json.load(open(PRED + "/drift_216.json"))
ys4, w4 = nodes(4); ys2, w2 = nodes(2)
# Exact discrete weights: the estimator is the equal-weight mean over the 2,000 strata, whose mean run
# midpoints are strata_mid(); a cubic in log y through the 4 node values, averaged over those midpoints,
# gives fixed weights lw (sum 1).  Validated below on c_216 against the exact discrete mean.
from band_028 import strata_mid
um = np.log(strata_mid(True)); un = np.log(np.array(ys4))
lw = np.array([np.mean(np.prod([(um - un[j]) / (un[i] - un[j]) for j in range(4) if j != i], axis=0)) for i in range(4)])
LOC = lambda kind, q: json.load(open(f"{PRED}/local_{kind}_q{q}.json"))["local"]
out = dict(entry="028", alpha_prime=A, z1=z1, z2=z2, n_per_stratum=NPER, strata=2000, N=2000 * NPER,
           band=[1.05e12, 2.05e12], midpoint_range=[LO, HI], nodes4=ys4, weights4=w4, cells={}, checks={})
print(f"Entry 028 predictions. alpha' = {A:.4e}; z1 = {z1}, z2 = {z2}; N = {2000*NPER:.3e} pairs\n")
print("Quadrature checks (4-node vs 2-node GL in log y, dy weight; discrete 2,000-stratum mean for c_216):")
for c in NAMES:
    q = Q[c]
    c216_4, c216_2 = L("216", q, 4), L("216", q, 2); r7_4, r7_2 = L("r7", q, 4), L("r7", q, 2)
    disc = float(np.mean(D[str(q)]))
    h5_4 = sum(w * h["c_hyb_K5"][c] for w, h in zip(w4, H4)); h5_2 = sum(w * h["c_hyb_K5"][c] for w, h in zip(w2, H2)) if H2 else float("nan")
    out["checks"][c] = dict(c216_4_minus_2=c216_4 - c216_2, c216_4_minus_discrete=c216_4 - disc, r7_4_minus_2=r7_4 - r7_2,
                            hybK5_4_minus_2=h5_4 - h5_2)
    print(f"  {c}: c216 4-2 {c216_4-c216_2:+.1e}, 4-discrete {c216_4-disc:+.1e}; through-7 4-2 {r7_4-r7_2:+.1e}; hybrid K5 4-2 {h5_4-h5_2:+.1e}")
print(f"\nDiscrete-stratum weights {np.round(lw, 6).tolist()} (sum {lw.sum():.12f}); GL4 weights {np.round(w4, 6).tolist()}")
for c in NAMES:
    q = Q[c]; dd = float(lw @ np.array(LOC("216", q))); ex = float(np.mean(D[str(q)]))
    out["checks"][c].update(c216_discrete_weights_minus_exact_discrete=dd - ex)
    print(f"  {c}: c216 via discrete weights {dd:+.12f} vs exact 2,000-stratum mean {ex:+.12f}: {dd-ex:+.1e}")
print("\nPredictions (frozen = exact discrete 2,000-stratum mean; GL4 over the spec range in brackets):")
for c in NAMES:
    q = Q[c]; cfull_gl = L("full", q, 4); c216_gl = L("216", q, 4)
    cfull = float(lw @ np.array(LOC("full", q))); c216 = float(lw @ np.array(LOC("216", q)))
    k5 = float(sum(w * h["c_hyb_K5"][c] for w, h in zip(lw, H4))); T6 = float(sum(w * h["mc6"][c][0] for w, h in zip(lw, H4)))
    k5_gl = sum(w * h["c_hyb_K5"][c] for w, h in zip(w4, H4)) + sum(w * h["mc6"][c][0] for w, h in zip(w4, H4))
    semc = math.sqrt(sum((w * h["mc6"][c][1]) ** 2 for w, h in zip(lw, H4))); semc_max = max(h["mc6"][c][1] for h in H4)
    chyb = k5 + T6; tau = max(4.0e-6, 0.6 * abs(T6)) + 3 * semc
    # lower/upper half (report-only): cubic in log y through the 4 node values, averaged with dy weight
    co = np.polyfit(np.log(ys4), [h["c_hyb_K6"][c] for h in H4], 3)
    def avg(lo, hi):
        yy, ww = nodes(8, lo, hi); return float(sum(w * np.polyval(co, math.log(y)) for y, w in zip(yy, ww)))
    mid = LO + 1000 * 5e8
    out["cells"][c] = dict(c216=c216, cfull=cfull, cr23=None, chyb=chyb, chyb_K5=k5, T6_tail=T6, se_mc=semc, se_mc_node_max=semc_max,
                           tau_hyb=tau, chyb_lower=avg(LO, LO + 999 * 5e8), chyb_upper=avg(mid, HI),
                           ladder_minus_hyb=cfull - chyb, gl4_spec_range=dict(c216=c216_gl, cfull=cfull_gl, chyb=k5_gl), node_values={"c_hyb_K6": [h["c_hyb_K6"][c] for h in H4], "c_full": LOC("full", q), "c216": LOC("216", q), "T6": [h["mc6"][c] for h in H4]})
    print(f"  {c}: [GL4: c216 {c216_gl:+.9f}, c_full {cfull_gl:+.9f}, c_hyb {k5_gl:+.9f}]")
    print(f"  {c}: c216 {c216:+.8f}  c_full {cfull:+.8f}  c_hyb(K=5) {k5:+.8f}  T6 {T6:+.3e} ± {semc:.1e} (node max {semc_max:.1e})  "
          f"c_hyb {chyb:+.8f}  tau_hyb {tau:.3e}  c_full - c_hyb {cfull-chyb:+.3e}")
print("\nPower and separation (planned s.e. = binomial sqrt((1 - c^2)/N); the paired-strata s.e. is the test statistic):")
for nper in (1.25e7, 1e7):
    N = 2000 * nper; print(f"  n = {nper:.3g} per stratum (N = {N:.3g}):")
    for c in NAMES:
        p = out["cells"][c]; se = math.sqrt((1 - p["chyb"] ** 2) / N); gap = p["chyb"] - p["cfull"]; band = p["tau_hyb"] + z2 * se
        pw_nom = stats.norm.sf(z1 - gap / se); pw_wc = stats.norm.sf(z1 - (gap - p["tau_hyb"]) / se)
        miss80 = p["tau_hyb"] + (z2 + z80) * se
        pass_null_wc = stats.norm.cdf((band - p["tau_hyb"]) / se) - stats.norm.cdf((-band - p["tau_hyb"]) / se)
        thyb_fail_if_full = 1 - (stats.norm.cdf((band - (p["cfull"] - p["chyb"])) / se) - stats.norm.cdf((-band - (p["cfull"] - p["chyb"])) / se))
        outside = abs(p["cfull"] - p["chyb"]) > band
        rec = dict(se_planned=se, gap=gap, band=band, Tlad_power_nominal=pw_nom, Tlad_power_worst=pw_wc, Thyb_miss80=miss80,
                   Thyb_pass_worst_null=pass_null_wc, Thyb_fail_prob_if_ladder_true=thyb_fail_if_full, cfull_outside_band=bool(outside),
                   cfull_margin=abs(p["cfull"] - p["chyb"]) - band)
        if nper == NPER: p.update(rec)
        else: p[f"at_n{nper:.3g}"] = rec
        print(f"    {c}: se {se:.3e}; gap c_hyb - c_full {gap:+.3e}; T-lad power nominal {pw_nom:.4f}, worst-case {pw_wc:.4f}; "
              f"T-hyb band {band:.3e}, 80% detectable miss {miss80:.3e}, worst-case null pass {pass_null_wc:.5f}; "
              f"c_full outside band: {outside} (margin {abs(p['cfull']-p['chyb'])-band:+.2e}); P(T-hyb fails | ladder true) {thyb_fail_if_full:.4f}")
out["decisive"] = [f"T-lad {c}" for c in NAMES] + [f"T-hyb {c}" for c in NAMES]
json.dump(out, open("pred_028.json", "w"), indent=1)
print("\nwrote pred_028.json")
