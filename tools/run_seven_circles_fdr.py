"""
run_seven_circles_fdr.py — Seven-circles look-elsewhere analysis (real dump)
============================================================================
Companion to tools/fdr_lookelsewhere.py. Consumes the canonical dump produced
by the seven-circles generator (cross_ratios.txt + cross_ratios_by_chord.json)
and answers the two questions at the granularity each is actually claimed:

  Finding #1 (TOTAL):  are 123 matches over N cross-ratios more than chance?
      The right control is a PLACEBO LIBRARY: keep the real CR values fixed,
      replace the 23 framework constants with random fake constants, and ask how
      many matches a random library catches. (Resampling the values against the
      REAL library is degenerate — it trivially recovers ~123.)

  Finding #2 (PER-CONSTANT, CHORD GRANULARITY):  is "cos 18 deg at 14/40 chord
      positions" special? Null: draw a random fake constant and count how many of
      the 40 chords contain >=1 CR within tolerance of it. Compare 14.

Each test is run under two nulls:
  - log-uniform over the value support [1, max];
  - empirical-density: fake constants ARE randomly chosen actual CR values, so
    they sit exactly where the pipeline piles up mass (strictest geometry control).

Usage:
  python3 tools/run_seven_circles_fdr.py cross_ratios.txt cross_ratios_by_chord.json
  python3 tools/run_seven_circles_fdr.py <txt> <json> --tol 5e-4 --draws 30000

Reuses the matching convention of fdr_lookelsewhere (value AND reciprocal).
stdlib only.
"""

import argparse
import bisect
import json
import math
import random
import sys

PHI = (1 + math.sqrt(5)) / 2
LIBRARY = {  # production 23-entry CURATED_CONSTANTS (mirrors fdr_lookelsewhere)
    "phi": PHI, "phi^-1": 1/PHI, "phi^-2": 1/PHI**2, "phi^-3": 1/PHI**3,
    "phi^-5": 1/PHI**5, "phi^5": PHI**5, "phi/2": PHI/2, "1/(2*phi)": 1/(2*PHI),
    "sqrt5/2": math.sqrt(5)/2, "cos(18deg)": math.sqrt(2+PHI)/2,
    "sin(36deg)": math.sqrt(3-PHI)/2, "cos(pi/7)": math.cos(math.pi/7),
    "cos(2pi/7)": math.cos(2*math.pi/7), "cos(3pi/7)": math.cos(3*math.pi/7),
    "epsilon_2": 1 - math.pi/(2*math.sqrt(3)),
    "eps_3/eps_2": (1-math.pi/(3*math.sqrt(2)))/(1-math.pi/(2*math.sqrt(3))),
    "arctan(1/sqrt2)": math.atan(1/math.sqrt(2)), "pulsation": 0.09480,
    "void": 0.71284, "gap": 0.28716, "8/21": 8/21, "84": 84.0, "21": 21.0,
}


def windows(c, tol):
    """Match windows for constant c: direct and (unless c~1) reciprocal."""
    w = [(c * (1 - tol), c * (1 + tol))]
    if c > 0 and abs(c - 1.0 / c) > tol * c:
        r = 1.0 / c
        w.append((r * (1 - tol), r * (1 + tol)))
    return w


def count_in_sorted(sorted_vals, lo, hi):
    return bisect.bisect_right(sorted_vals, hi) - bisect.bisect_left(sorted_vals, lo)


def value_hits(c, tol, sorted_vals):
    """# of flat CR values within tol of c (value or reciprocal)."""
    return sum(count_in_sorted(sorted_vals, lo, hi) for lo, hi in windows(c, tol))


def chord_hits(c, tol, chords_sorted):
    """# of chords with >=1 CR within tol of c (value or reciprocal)."""
    wins = windows(c, tol)
    hit = 0
    for cr in chords_sorted:
        if any(count_in_sorted(cr, lo, hi) > 0 for lo, hi in wins):
            hit += 1
    return hit


def make_sampler(kind, sorted_vals):
    if kind == "empirical":
        return lambda: sorted_vals[random.randrange(len(sorted_vals))]
    if kind == "log":
        la, lb = math.log(sorted_vals[0]), math.log(sorted_vals[-1])
        return lambda: math.exp(random.uniform(la, lb))
    raise ValueError(kind)


def summarize(samples, observed):
    samples = sorted(samples)
    n = len(samples)
    mean = sum(samples) / n
    ge = sum(1 for s in samples if s >= observed)
    return {
        "mean": mean,
        "p50": samples[n // 2],
        "p95": samples[min(int(0.95 * n), n - 1)],
        "p99": samples[min(int(0.99 * n), n - 1)],
        "max": samples[-1],
        "observed": observed,
        "enrichment": observed / mean if mean > 0 else float("inf"),
        "p_value": ge / n,
    }


def verdict(p):
    return ("SIGNAL (rare under the null)" if p < 1e-3
            else "marginal" if p < 0.05
            else "CONSISTENT WITH PIPELINE GEOMETRY")


def line(label, s):
    print(f"  {label:<22s} obs={s['observed']:<5g} mean={s['mean']:7.3f} "
          f"enrich={s['enrichment']:6.2f}x  p={s['p_value']:.3e}  "
          f"[p95={s['p95']}, p99={s['p99']}, max={s['max']}]  -> {verdict(s['p_value'])}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Seven-circles look-elsewhere analysis.")
    ap.add_argument("values", help="cross_ratios.txt (one CR per line)")
    ap.add_argument("by_chord", help="cross_ratios_by_chord.json")
    ap.add_argument("--tol", type=float, default=5e-4)
    ap.add_argument("--draws", type=int, default=30000,
                    help="placebo draws / fake libraries (default 30000)")
    ap.add_argument("--observed-total", type=int, default=123)
    ap.add_argument("--seed", type=int, default=12345)
    args = ap.parse_args(argv)
    random.seed(args.seed)

    vals = sorted(float(x) for x in open(args.values) if x.strip())
    data = json.load(open(args.by_chord))
    chords_sorted = [sorted(ch["cross_ratios"]) for ch in data["chords"]]
    n_chords = len(chords_sorted)

    reachable = [n for n, c in LIBRARY.items() if value_hits(c, args.tol, vals) > 0]
    lib_size = len(LIBRARY)

    print("=" * 78)
    print("SEVEN-CIRCLES LOOK-ELSEWHERE ANALYSIS (real dump)")
    print("=" * 78)
    print(f"  N cross-ratios       : {len(vals)}   support [{vals[0]:.4g}, {vals[-1]:.4g}]")
    print(f"  chords               : {n_chords}")
    print(f"  library size M       : {lib_size}   reachable at tol={args.tol:g}: "
          f"{len(reachable)}")
    print(f"  tolerance / draws    : {args.tol:g} / {args.draws}")
    print()

    # ── Finding #1: total-count placebo-LIBRARY ──────────────────────────────
    print("FINDING #1 — total matches vs a random 23-constant library")
    print("-" * 78)
    for kind in ("log", "empirical"):
        sampler = make_sampler(kind, vals)
        totals = []
        for _ in range(args.draws):
            fake = [sampler() for _ in range(lib_size)]
            totals.append(sum(value_hits(c, args.tol, vals) for c in fake))
        s = summarize(totals, args.observed_total)
        line(f"placebo-lib [{kind}]", s)
    print("  (Resampling values against the REAL library is omitted: degenerate "
          "~123 by construction.)")
    print()

    # ── Finding #2: per-constant, chord granularity ──────────────────────────
    print("FINDING #2 — per-constant CHORD-granularity significance (k/40)")
    print("-" * 78)
    headline = ["cos(18deg)", "sqrt5/2", "cos(pi/7)"]
    obs_chord = {n: chord_hits(LIBRARY[n], args.tol, chords_sorted) for n in headline}
    for kind in ("log", "empirical"):
        print(f"  null = {kind}-{'uniform' if kind=='log' else 'density'}:")
        sampler = make_sampler(kind, vals)
        # one shared pool of fake constants per null, scored at chord granularity
        fake_scores = [chord_hits(sampler(), args.tol, chords_sorted)
                       for _ in range(args.draws)]
        fake_scores.sort()
        fmean = sum(fake_scores) / len(fake_scores)
        for name in headline:
            obs = obs_chord[name]
            ge = sum(1 for s in fake_scores if s >= obs)
            p = ge / len(fake_scores)
            enr = obs / fmean if fmean > 0 else float("inf")
            print(f"    {name:<12s} {obs:>2d}/{n_chords}  "
                  f"fake_mean={fmean:5.2f}  enrich={enr:5.2f}x  "
                  f"p={p:.3e}  -> {verdict(p)}")
        print()

    print("Reading: a high analytic enrichment with a non-significant placebo "
          "p-value\nmeans the hits come from where the pipeline piles up CR "
          "values, not from\nthe constant being special. The empirical-density "
          "null is the strictest\n(fake constants sit exactly on the value mass).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
