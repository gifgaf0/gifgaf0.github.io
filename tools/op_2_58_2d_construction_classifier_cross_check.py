"""op_2_58_2d_construction_classifier_cross_check.py — Brief 10.5 Item 3.

Cross-checks the §2.58.B construction's noise sampler against the §3.3 projection
classifier. For 100 toy (s, z, e) samples at q=911, k=7, and each σ ∈ {1, 2, 4},
runs the pair-kernel classifier on every noise coordinate e_i and measures the
empirical pair-recovery rate against the recorded Convention-C pair label.

PASS iff recovery at all three σ values is within ±3% of the Brief-08 with-lift
baseline (96.2%). A FAIL is a §2.4 halt-and-surface event. Non-test utility.
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from op_2_58_2d_classifier import TOY_P, FanoLineClassifier  # noqa: E402
from op_2_58_2d_construction import gen_zd_noise_sample  # noqa: E402

BASELINE_BRIEF08 = 0.962
TOLERANCE = 0.03
SIGMAS = [1, 2, 4]
N_SAMPLES = 100
K = 7
SEED = 20260601


def recovery_at_sigma(clf: FanoLineClassifier, sigma: int, seed: int = SEED,
                      n_samples: int = N_SAMPLES, k: int = K) -> dict:
    rng = np.random.default_rng(seed)
    hits = 0
    total = 0
    for _ in range(n_samples):
        sample = gen_zd_noise_sample(TOY_P, k, sigma, rng)
        for i in range(k):
            res = clf.classify(sample["e"][i])
            hits += res["pair"] == sample["pair"][i]
            total += 1
    rate = hits / total
    return {"sigma": sigma, "hits": hits, "total": total, "recovery": rate,
            "within_band": abs(rate - BASELINE_BRIEF08) <= TOLERANCE}


def run() -> dict:
    clf = FanoLineClassifier(TOY_P)
    per_sigma = [recovery_at_sigma(clf, s) for s in SIGMAS]
    all_in_band = all(r["within_band"] for r in per_sigma)
    rates = [r["recovery"] for r in per_sigma]
    spread = max(rates) - min(rates)
    return {"per_sigma": per_sigma, "pass": all_in_band,
            "rate_spread_across_sigma": spread}


def main() -> int:
    out = run()
    print("=" * 70)
    print("§2.58.B construction × §3.3 classifier cross-check (q=911, k=7, N=100)")
    print(f"baseline (Brief-08 with-lift): {BASELINE_BRIEF08:.1%} ± {TOLERANCE:.0%}")
    print("=" * 70)
    for r in out["per_sigma"]:
        flag = "in-band" if r["within_band"] else "OUT-OF-BAND"
        print(f"  σ={r['sigma']}: recovery {r['recovery']:.3%} "
              f"({r['hits']}/{r['total']}) — {flag}")
    print(f"\n  spread across σ: {out['rate_spread_across_sigma']:.3%}")
    print(f"  RESULT: {'PASS' if out['pass'] else 'FAIL (halt-and-surface, §2.4)'}")
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
