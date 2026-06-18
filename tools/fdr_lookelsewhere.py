"""
fdr_lookelsewhere.py — Program-level false-discovery / look-elsewhere calculator
================================================================================
Perspective-1 instrument (see reports/SQT_v4.24_FIVE_PERSPECTIVES.md).

PURPOSE
-------
The Prior Address Standard audits each constant's lineage *individually*. It does
not bound the program-wide rate at which a *random* probe value lands within
tolerance of *some* entry of a small "framework constant" library. This tool
supplies the missing number: given

    N   = number of probe values computed (e.g. cross-ratios, mass ratios),
    M   = size of the curated constant library,
    tau = relative match tolerance (e.g. 5e-4 = 0.05%),

it prints the EXPECTED number of spurious hits under an explicit null, the
expected number of distinct constants hit, a Poisson p-value for an observed
count, and an enrichment factor (observed / expected). Print this beside every
hit table so "cos 18° appears at 14/40" carries its own null expectation.

THE NULL MODELS
---------------
A "hit" on constant c is |v - c| / c <= tau, i.e. v in [c(1-tau), c(1+tau)].
Optionally v's reciprocal is also matched (the seven-circles convention), which
is equivalent to adding 1/c as a second target.

  log-uniform   ln(v) ~ Uniform[ln a, ln b].   Per-target probability is
                p_c = ln((1+tau)/(1-tau)) / ln(b/a)   (constant across targets).
                This is the right null when probe values span orders of
                magnitude and you have no reason to prefer any scale.

  uniform       v ~ Uniform[a, b].   p_c = 2*tau*c / (b - a)   (grows with c).

  empirical     v drawn (with replacement) from a supplied list of the ACTUAL
                probe values. This is the most defensible null: it asks "how
                often would the SAME pipeline hit a constant by chance?" and so
                folds in the real geometry of the value distribution. Monte
                Carlo only.

Targets whose match interval falls outside [a, b] (or outside the empirical
support) contribute 0 and are reported as unreachable.

EXPECTED COUNTS (analytic)
--------------------------
  E[total hits]            = N * sum_c p_c                       (value x target events)
  E[distinct consts hit]   = sum_c (1 - (1 - p_c)^N)
  p-value for observed K    = P(Poisson(E[total]) >= K)          (rare-event approx)
  enrichment               = observed / E[total]

USAGE
-----
  # Analytic, log-uniform null over [0.05, 25], 11495 probes, 0.05% tol,
  # default partial library, observed 123 total matches:
  python3 fdr_lookelsewhere.py --n 11495 --tol 5e-4 --range 0.05 25 \
      --null log --reciprocal --observed 123 --mc 20000

  # Empirical null from a file of computed cross-ratios (one float per line):
  python3 fdr_lookelsewhere.py --values cross_ratios.txt --tol 5e-4 \
      --reciprocal --observed 123 --mc 20000

  # Per-constant significance for a single constant's chord-position count:
  python3 fdr_lookelsewhere.py --n 40 --tol 5e-4 --range 0.05 25 --null log \
      --only "cos(18deg)" --observed 14

Importable: expected_hits(...), monte_carlo(...), poisson_sf(...).

Author: review instrument for the SQT program (2026-06-03). stdlib only.
"""

import argparse
import math
import random
import sys

# ── Framework constant library (full 23-entry CURATED_CONSTANTS) ─────────────
# Canonical version from seven_circles_tight.py (supplied by the seven-circles
# generator, 2026-06-03). This is the production library; M = 23.
PHI = (1 + math.sqrt(5)) / 2
DEFAULT_LIBRARY = {
    # φ-tower (framework-specific)
    "phi":              PHI,
    "phi^-1":           1 / PHI,
    "phi^-2":           1 / PHI**2,
    "phi^-3":           1 / PHI**3,
    "phi^-5":           1 / PHI**5,
    "phi^5":            PHI**5,
    # 5-fold trig
    "phi/2":            PHI / 2,                 # cos(36°)
    "1/(2*phi)":        1 / (2 * PHI),           # cos(72°)
    "sqrt5/2":          math.sqrt(5) / 2,        # t parameter
    "cos(18deg)":       math.sqrt(2 + PHI) / 2,  # cos(18°)
    "sin(36deg)":       math.sqrt(3 - PHI) / 2,  # sin(36°)
    # 7-fold trig (PSL(2,7) / Klein quartic)
    "cos(pi/7)":        math.cos(math.pi / 7),
    "cos(2pi/7)":       math.cos(2 * math.pi / 7),
    "cos(3pi/7)":       math.cos(3 * math.pi / 7),
    # Framework packing constants
    "epsilon_2":        1 - math.pi / (2 * math.sqrt(3)),   # ζ lattice tax
    "eps_3/eps_2":      (1 - math.pi / (3 * math.sqrt(2)))
                        / (1 - math.pi / (2 * math.sqrt(3))),  # Hales ratio
    "arctan(1/sqrt2)":  math.atan(1 / math.sqrt(2)),        # Prop P.α
    # 84-decomposition values
    "pulsation":        0.09480,
    "void":             0.71284,
    "gap":              0.28716,
    # Lattice + PSL(2,7) coset
    "8/21":             8 / 21,                  # Cheeger constant
    "84":               84.0,                    # Cl(2)+Cl(4)+Cl(6)
    "21":               21.0,                    # K₇ / Császár edges
}
DEFAULT_LIBRARY_IS_PARTIAL = False  # full production 23-entry library


# ── Targets (optionally include reciprocals) ─────────────────────────────────
def build_targets(library, include_reciprocal):
    """Return {label: value}, adding 1/c as '<name> (recip)' when requested
    and distinct from an existing target."""
    targets = dict(library)
    if include_reciprocal:
        seen = dict(library)
        for name, c in library.items():
            if c <= 0:
                continue
            r = 1.0 / c
            if all(abs(r - v) > 1e-12 for v in seen.values()):
                targets[name + " (recip)"] = r
                seen[name + " (recip)"] = r
    return targets


# ── Per-target hit probability under analytic nulls ──────────────────────────
def per_target_prob(c, tol, v_lo, v_hi, null):
    """Probability a single random value (drawn from the null on [v_lo,v_hi])
    lands within relative tolerance `tol` of constant c. Returns 0 for targets
    whose match interval lies outside [v_lo, v_hi]."""
    lo, hi = c * (1 - tol), c * (1 + tol)
    # clip the match interval to the support
    lo_c, hi_c = max(lo, v_lo), min(hi, v_hi)
    if hi_c <= lo_c:
        return 0.0
    if null == "log":
        return math.log(hi_c / lo_c) / math.log(v_hi / v_lo)
    if null == "uniform":
        return (hi_c - lo_c) / (v_hi - v_lo)
    raise ValueError(f"analytic per_target_prob: unknown null '{null}'")


def expected_hits(library, tol, n_probes, v_lo, v_hi, null="log",
                  include_reciprocal=True):
    """Analytic expectation. Returns dict with per-target probs/expected,
    total expected events, expected distinct constants hit, unreachable list."""
    targets = build_targets(library, include_reciprocal)
    per = {}
    unreachable = []
    for name, c in targets.items():
        p = per_target_prob(c, tol, v_lo, v_hi, null)
        if p == 0.0:
            unreachable.append(name)
        per[name] = {"value": c, "p": p, "expected": p * n_probes,
                     "p_at_least_one": 1 - (1 - p) ** n_probes}
    total_expected = sum(d["expected"] for d in per.values())
    distinct_expected = sum(d["p_at_least_one"] for d in per.values())
    return {
        "per_target": per,
        "total_expected": total_expected,
        "distinct_expected": distinct_expected,
        "n_targets": len(targets),
        "unreachable": unreachable,
    }


# ── Samplers for Monte Carlo ─────────────────────────────────────────────────
def log_uniform_sampler(v_lo, v_hi):
    la, lb = math.log(v_lo), math.log(v_hi)
    return lambda: math.exp(random.uniform(la, lb))


def uniform_sampler(v_lo, v_hi):
    return lambda: random.uniform(v_lo, v_hi)


def empirical_sampler(values):
    vals = list(values)
    return lambda: vals[random.randrange(len(vals))]


# Compute budget: cap total value-draws so large N stays responsive.
MC_MAX_DRAWS = 4_000_000


def monte_carlo(library, tol, n_probes, sampler, trials=10000,
                include_reciprocal=True, observed=None, seed=12345):
    """Simulate `trials` independent runs of N=n_probes draws; count match
    events (value x target) per run. Membership is O(log M) via a sorted edge
    array (intervals are disjoint at the tolerances used). `trials` is reduced
    if trials*n_probes would exceed MC_MAX_DRAWS. Returns mean, std,
    percentiles, the effective trial count, and an empirical p-value
    P(spurious_total >= observed) if observed given."""
    random.seed(seed)
    targets = sorted(build_targets(library, include_reciprocal).values())
    # Flat sorted edge array; v is inside some interval iff bisect_right is odd.
    import bisect
    edges = []
    for c in targets:
        edges.append(c * (1 - tol))
        edges.append(c * (1 + tol))
    edges.sort()  # disjoint intervals -> already paired/ordered

    eff_trials = max(1, min(trials, MC_MAX_DRAWS // max(1, n_probes)))
    totals = []
    for _ in range(eff_trials):
        hits = 0
        for _ in range(n_probes):
            v = sampler()
            if bisect.bisect_right(edges, v) & 1:
                hits += 1
        totals.append(hits)
    totals.sort()
    trials = eff_trials
    n = len(totals)
    mean = sum(totals) / n
    var = sum((t - mean) ** 2 for t in totals) / n
    out = {
        "mean": mean,
        "std": math.sqrt(var),
        "p05": totals[int(0.05 * n)],
        "p50": totals[n // 2],
        "p95": totals[min(int(0.95 * n), n - 1)],
        "max": totals[-1],
        "trials": trials,
    }
    if observed is not None:
        ge = sum(1 for t in totals if t >= observed)
        out["observed"] = observed
        out["p_value_empirical"] = ge / n
        out["enrichment"] = observed / mean if mean > 0 else float("inf")
    return out


# ── Placebo-library test (single-constant significance, empirical) ───────────
def placebo_test(values, tol, observed, n_draws=20000, include_reciprocal=True,
                 seed=12345):
    """The Perspective-5 control. Draw `n_draws` random FAKE constants
    log-uniformly from the support of the actual probe `values`, and for each
    count how many of `values` land within relative tol of it (matching the
    reciprocal too, when requested, exactly as a real constant would be matched).

    This builds the null distribution of per-constant hit counts *induced by the
    real value distribution* — so a high score for a real constant only counts
    as signal if random constants in the same distribution rarely score as high.
    Returns mean, percentiles, and p-value = fraction of fake constants with
    hits >= observed. Requires the actual values (pipeline geometry is the
    whole point); an analytic null would make every fake constant identical."""
    import bisect
    random.seed(seed)
    vals = sorted(values)
    n = len(vals)
    v_lo, v_hi = vals[0], vals[-1]
    la, lb = math.log(v_lo), math.log(v_hi)

    def hits_for(c):
        total = 0
        for center in ((c, 1.0 / c) if include_reciprocal and c > 0 else (c,)):
            lo, hi = center * (1 - tol), center * (1 + tol)
            total += bisect.bisect_right(vals, hi) - bisect.bisect_left(vals, lo)
        return total

    counts = [hits_for(math.exp(random.uniform(la, lb))) for _ in range(n_draws)]
    counts.sort()
    mean = sum(counts) / n_draws
    ge = sum(1 for c in counts if c >= observed)
    return {
        "n_values": n,
        "support": (v_lo, v_hi),
        "draws": n_draws,
        "mean": mean,
        "p50": counts[n_draws // 2],
        "p95": counts[min(int(0.95 * n_draws), n_draws - 1)],
        "p99": counts[min(int(0.99 * n_draws), n_draws - 1)],
        "max": counts[-1],
        "observed": observed,
        "p_value": ge / n_draws,
        "enrichment": observed / mean if mean > 0 else float("inf"),
    }


# ── Poisson survival for analytic p-value ────────────────────────────────────
def poisson_sf(k, lam):
    """P(X >= k) for X ~ Poisson(lam). Stable for the small lam, modest k here."""
    if k <= 0:
        return 1.0
    # P(X < k) = sum_{i=0}^{k-1} e^-lam lam^i / i!
    term = math.exp(-lam)
    cdf = term
    for i in range(1, k):
        term *= lam / i
        cdf += term
    return max(0.0, 1.0 - cdf)


# ── Reporting ────────────────────────────────────────────────────────────────
def print_placebo_report(values, tol, observed, n_draws, include_reciprocal,
                         only, library):
    print("=" * 74)
    print("PLACEBO-LIBRARY TEST (single-constant significance vs the same "
          "distribution)")
    print("=" * 74)
    res = placebo_test(values, tol, observed, n_draws, include_reciprocal)
    print(f"  Actual values        : {res['n_values']}  "
          f"support [{res['support'][0]:.4g}, {res['support'][1]:.4g}]")
    print(f"  Fake constants drawn : {res['draws']} (log-uniform on support)")
    print(f"  Tolerance tau        : {tol:g}   reciprocal: "
          f"{'on' if include_reciprocal else 'off'}")
    if only and only in library:
        import bisect
        vals = sorted(values)
        c = library[only]
        rh = 0
        for center in ((c, 1.0 / c) if include_reciprocal and c > 0 else (c,)):
            lo, hi = center * (1 - tol), center * (1 + tol)
            rh += bisect.bisect_right(vals, hi) - bisect.bisect_left(vals, lo)
        print(f"  Real constant '{only}' = {c:.6f}: {rh} hits in the actual "
              f"values")
    print()
    print(f"  Fake-constant hit distribution: mean={res['mean']:.3f}  "
          f"[p50={res['p50']}, p95={res['p95']}, p99={res['p99']}, "
          f"max={res['max']}]")
    print(f"  OBSERVED                    : {res['observed']}")
    print(f"  Enrichment (obs / mean)     : {res['enrichment']:.2f}x")
    print(f"  Placebo p-value P(fake>=obs): {res['p_value']:.3e}")
    verdict = ("SIGNAL — rare among random constants" if res['p_value'] < 1e-3
               else "marginal" if res['p_value'] < 0.05
               else "CONSISTENT WITH PIPELINE GEOMETRY (not special)")
    print(f"  Verdict                     : {verdict}")
    print()
    print("  Reading: this asks whether the constant scores higher than RANDOM")
    print("  constants drawn from the same value distribution. A high analytic")
    print("  enrichment with a non-significant placebo p-value means the hits")
    print("  come from where the pipeline piles up values, not from the")
    print("  constant being special. Match the granularity of --observed to the")
    print("  granularity of the supplied values (flat CR list -> value-level).")
    return 0


def print_report(library, tol, n_probes, v_lo, v_hi, null, include_reciprocal,
                 observed, only, mc_trials, empirical_values):
    print("=" * 74)
    print("PROGRAM-LEVEL FALSE-DISCOVERY / LOOK-ELSEWHERE REPORT")
    print("=" * 74)
    lib = library
    if only:
        if only not in library:
            print(f"  ! constant '{only}' not in library; available:")
            for k in library:
                print(f"      {k}")
            return 1
        lib = {only: library[only]}
    is_empirical = empirical_values is not None
    print(f"  Probes N             : {n_probes}")
    print(f"  Library size M       : {len(lib)}"
          + (f"  (default is PARTIAL: {len(DEFAULT_LIBRARY)}/23)"
             if (library is DEFAULT_LIBRARY and not only and DEFAULT_LIBRARY_IS_PARTIAL)
             else ""))
    print(f"  Tolerance tau        : {tol:g}  ({tol*100:.4f}% relative)")
    print(f"  Reciprocal matching  : {'on' if include_reciprocal else 'off'}")
    if is_empirical:
        vs = sorted(empirical_values)
        print(f"  Null                 : empirical ({len(vs)} supplied values, "
              f"range [{vs[0]:.4g}, {vs[-1]:.4g}])  [Monte Carlo only]")
    else:
        null_label = "log-uniform" if null == "log" else "uniform"
        print(f"  Null                 : {null_label} on [{v_lo:g}, {v_hi:g}]")
    print()

    # Analytic block (skip if empirical null without an assumed range)
    if not is_empirical:
        res = expected_hits(lib, tol, n_probes, v_lo, v_hi, null,
                            include_reciprocal)
        print("  Per-target expected spurious hits "
              "(target | value | p_hit | E[hits] | P>=1):")
        for name, d in sorted(res["per_target"].items(),
                              key=lambda kv: -kv[1]["expected"]):
            flag = "  UNREACHABLE" if d["p"] == 0.0 else ""
            print(f"    {name:<18s} {d['value']:>10.6f}  {d['p']:.3e}  "
                  f"{d['expected']:>8.4f}  {d['p_at_least_one']:>6.3f}{flag}")
        print()
        print(f"  E[total spurious hits]      : {res['total_expected']:.3f}")
        print(f"  E[distinct constants hit]   : {res['distinct_expected']:.3f}"
              f"  (of {res['n_targets']} targets)")
        if res["unreachable"]:
            print(f"  Unreachable targets         : {len(res['unreachable'])} "
                  f"(match interval outside support)")
        if observed is not None:
            lam = res["total_expected"]
            pv = poisson_sf(int(math.ceil(observed)), lam)
            enr = observed / lam if lam > 0 else float("inf")
            print()
            print(f"  OBSERVED                    : {observed}")
            print(f"  Enrichment (obs / E)        : {enr:.2f}x")
            print(f"  Poisson p-value P(>= obs)   : {pv:.3e}")
            verdict = ("SIGNAL (well above chance)" if pv < 1e-3
                       else "marginal" if pv < 0.05
                       else "CONSISTENT WITH CHANCE")
            print(f"  Verdict                     : {verdict}")
        print()

    # Monte Carlo block
    if mc_trials and mc_trials > 0:
        if is_empirical:
            sampler = empirical_sampler(empirical_values)
        elif null == "log":
            sampler = log_uniform_sampler(v_lo, v_hi)
        else:
            sampler = uniform_sampler(v_lo, v_hi)
        mc = monte_carlo(lib, tol, n_probes, sampler, trials=mc_trials,
                         include_reciprocal=include_reciprocal,
                         observed=observed)
        print(f"  Monte Carlo ({mc['trials']} trials):")
        print(f"    spurious total hits  mean={mc['mean']:.3f} "
              f"std={mc['std']:.3f}  "
              f"[p05={mc['p05']}, p50={mc['p50']}, p95={mc['p95']}, "
              f"max={mc['max']}]")
        if observed is not None:
            print(f"    OBSERVED={mc['observed']}  "
                  f"enrichment={mc['enrichment']:.2f}x  "
                  f"empirical p-value P(>=obs)={mc['p_value_empirical']:.3e}")
        print()

    print("  Note: a default-library run UNDERSTATES the look-elsewhere effect")
    print("  if your true library is larger. Paste the production 23-entry")
    print("  CURATED_CONSTANTS and (ideally) supply the actual probe values")
    print("  via --values for the empirical null before citing significance.")
    return 0


def load_values(path):
    vals = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                vals.append(float(line.split()[0]))
            except ValueError:
                continue
    if not vals:
        raise SystemExit(f"no numeric values parsed from {path}")
    return vals


def demo():
    """Worked seven-circles example (reports/seven_circles_report.md)."""
    print("DEMO — seven-circles context (partial library; illustrative).\n")
    print(">>> total-match level: N=11495 cross-ratios, observed=123 matches\n")
    print_report(DEFAULT_LIBRARY, 5e-4, 11495, 0.05, 25.0, "log", True,
                 123, None, 20000, None)
    print("\n>>> single-constant level: cos(18deg) at 14 of 40 chord positions\n")
    print_report(DEFAULT_LIBRARY, 5e-4, 40, 0.05, 25.0, "log", True,
                 14, "cos(18deg)", 20000, None)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Program-level false-discovery / look-elsewhere calculator.")
    ap.add_argument("--n", type=int, default=None,
                    help="number of probe values computed")
    ap.add_argument("--tol", type=float, default=5e-4,
                    help="relative match tolerance (default 5e-4 = 0.05%%)")
    ap.add_argument("--range", type=float, nargs=2, metavar=("LO", "HI"),
                    default=[0.05, 25.0],
                    help="support [LO,HI] for analytic nulls (default 0.05 25)")
    ap.add_argument("--null", choices=["log", "uniform"], default="log",
                    help="analytic null model (default log)")
    ap.add_argument("--reciprocal", action="store_true",
                    help="also match v's reciprocal (seven-circles convention)")
    ap.add_argument("--observed", type=float, default=None,
                    help="observed hit count, for enrichment + p-value")
    ap.add_argument("--only", type=str, default=None,
                    help="restrict to a single library constant by name")
    ap.add_argument("--values", type=str, default=None,
                    help="file of actual probe values (one float/line) -> "
                         "empirical null (Monte Carlo)")
    ap.add_argument("--mc", type=int, default=0,
                    help="Monte Carlo trials (0 = analytic only; demo uses 20000)")
    ap.add_argument("--placebo", type=int, default=0, metavar="DRAWS",
                    help="placebo-library test: draw DRAWS random fake "
                         "constants from the --values support and rank the "
                         "observed count against them (requires --values, "
                         "--observed)")
    ap.add_argument("--demo", action="store_true",
                    help="run the worked seven-circles example and exit")
    args = ap.parse_args(argv)

    if args.demo:
        demo()
        return 0

    empirical_values = load_values(args.values) if args.values else None

    if args.placebo:
        if empirical_values is None or args.observed is None:
            ap.error("--placebo requires --values and --observed")
        return print_placebo_report(empirical_values, args.tol, args.observed,
                                    args.placebo, args.reciprocal, args.only,
                                    DEFAULT_LIBRARY)

    if empirical_values is not None:
        v_lo, v_hi = min(empirical_values), max(empirical_values)
        n_probes = args.n if args.n is not None else len(empirical_values)
        if args.mc == 0:
            args.mc = 20000  # empirical null requires MC
    else:
        v_lo, v_hi = args.range
        if args.n is None:
            ap.error("--n is required unless --values or --demo is given")
        n_probes = args.n

    return print_report(DEFAULT_LIBRARY, args.tol, n_probes, v_lo, v_hi,
                        args.null, args.reciprocal, args.observed, args.only,
                        args.mc, empirical_values)


if __name__ == "__main__":
    sys.exit(main())
