"""Brief 02 epilogue Task 1: ZD-pair density of CBD(η=2) over F_p^16.

The supplied SLWE source filters its random non-ZD vectors by checking
exactly the case ``len(non_zero_indices) == 2`` against the precomputed
``zd_pairs`` set (sedenion ZD pairs of basis-vector pairs). For
rejection-sampling small vectors to be viable, the rejection rate must
be small.

This script samples ``n_trials`` vectors from CBD(η=2) over F_p^16 at
the requested primes and reports:

- the fraction of vectors that fall on a "ZD pair" by the source's
  exact definition (exactly 2 non-zero entries, those indices in
  ``zd_pairs``);
- the all-zero rate (the source also rejects these); and
- a few coefficient-magnitude statistics for sanity.

Output is written to stdout and to tools/zd_density_results.md.
"""

from __future__ import annotations

import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sqt_slwe as _slwe   # populates zd_pairs once the module imports
from sedenion_Fp import DIM


CBD2_VALUES = [-2, -1, 0, 1, 2]
CBD2_WEIGHTS = [1, 4, 6, 4, 1]   # binomial(4, k) for k=0..4 → CBD₂


def cbd2_sample(p: int) -> list[int]:
    return [random.choices(CBD2_VALUES, weights=CBD2_WEIGHTS)[0] % p
            for _ in range(DIM)]


def classify(v: list[int], p: int, zd_pairs: set) -> str:
    nz = [i for i, c in enumerate(v) if c != 0]
    if not nz:
        return "all_zero"
    if len(nz) == 2:
        idx = tuple(sorted(nz))
        if idx in zd_pairs:
            return "zd_pair"
    return "ok"


def measure_at_prime(p: int, n_trials: int, seed: int) -> dict:
    random.seed(seed)
    _slwe.p = p   # the zd_pairs set is prime-independent (audit: same 84
                  # quadruples for all primes), so we can switch p freely.
    counts = Counter()
    abs_sum = 0
    abs_max = 0
    for _ in range(n_trials):
        v = cbd2_sample(p)
        counts[classify(v, p, _slwe.zd_pairs)] += 1
        for c in v:
            cc = c if c <= p // 2 else c - p
            a = abs(cc)
            abs_sum += a
            if a > abs_max:
                abs_max = a
    total = sum(counts.values())
    return {
        "p": p,
        "trials": total,
        "ok": counts.get("ok", 0),
        "zd_pair": counts.get("zd_pair", 0),
        "all_zero": counts.get("all_zero", 0),
        "zd_pair_frac": counts.get("zd_pair", 0) / total,
        "all_zero_frac": counts.get("all_zero", 0) / total,
        "rejection_rate": (counts.get("zd_pair", 0)
                           + counts.get("all_zero", 0)) / total,
        "mean_abs_coeff": abs_sum / (total * DIM),
        "max_abs_coeff": abs_max,
    }


def main() -> int:
    n_trials = 100_000
    rows = []
    for p, seed in [(911, 0xb02), (8191, 0xb03)]:
        r = measure_at_prime(p, n_trials, seed)
        rows.append(r)
        print(f"p = {p:>5d}  trials={r['trials']}  ok={r['ok']}  "
              f"zd_pair={r['zd_pair']} ({r['zd_pair_frac']*100:.4f}%)  "
              f"all_zero={r['all_zero']} ({r['all_zero_frac']*100:.4f}%)  "
              f"reject={r['rejection_rate']*100:.4f}%  "
              f"E[|coef|]={r['mean_abs_coeff']:.3f}")

    md = ["# CBD(η=2) ZD-pair density over F_p^16",
          "",
          "100 000 samples per prime; CBD(η=2) gives entries in {-2,-1,0,1,2} "
          "with weights (1,4,6,4,1)/16. A vector is counted as ZD-pair when "
          "it has exactly two non-zero entries whose indices are an unordered "
          "pair in the precomputed `zd_pairs` set (42 pairs).",
          "",
          "| p | ok | zd-pair | (% of samples) | all-zero | rejection rate | E[|coef|] |",
          "|---|---:|---:|---:|---:|---:|---:|"]
    for r in rows:
        md.append(
            f"| {r['p']} | {r['ok']} | {r['zd_pair']} | "
            f"{r['zd_pair_frac']*100:.4f}% | {r['all_zero']} | "
            f"{r['rejection_rate']*100:.4f}% | {r['mean_abs_coeff']:.3f} |"
        )
    md.append("")
    md.append("Verdict: rejection sampling is viable iff zd-pair rate < 1%. "
              f"Observed rate at both primes is "
              f"{max(r['zd_pair_frac'] for r in rows)*100:.4f}%.")
    Path("tools/zd_density_results.md").write_text("\n".join(md) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
