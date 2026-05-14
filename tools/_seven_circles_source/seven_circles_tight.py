"""
Seven-Circles Cross-Ratio Experiment — TIGHTENED VERSION
=========================================================

Changes from v1:
1. Tolerance: 0.05% (was 0.5%) — 10x stricter
2. Constant library: 18 framework-specific values, no generic rationals
   (no 1/2, 1/3, 1/4, π/2, π/3, π/4, √2, √3 — these match by accident at high N)
3. Reports WHICH 4-circle combinations produce matches, so we can audit
   whether they have structural meaning (Fano line, Császár face cycle, etc.)
4. Reciprocal counted as ONE match, not two
5. Null model run with same restricted library

This is the sharpened test. If a match shows up here, it has a much
better claim to being real geometric content.
"""

import numpy as np
from itertools import combinations
from math import pi, sqrt, cos, sin, atan
import sys
sys.path.insert(0, '/home/claude/circles_experiment')
from seven_circles_experiment import (
    define_circles, run_chord, cross_ratio, line_circle_intersect
)

# ============================================================
# CURATED FRAMEWORK CONSTANTS — no generic rationals
# ============================================================

PHI = (1 + sqrt(5)) / 2

CURATED_CONSTANTS = {
    # φ-tower (framework-specific)
    "phi":              (PHI,                    "(1+√5)/2"),
    "phi^-1":           (1/PHI,                  "1/φ"),
    "phi^-2":           (1/PHI**2,               "1/φ²"),
    "phi^-3":           (1/PHI**3,               "1/φ³"),
    "phi^-5":           (1/PHI**5,               "1/φ⁵"),
    "phi^5":            (PHI**5,                 "φ⁵"),

    # 5-fold trig (only the framework-specific ones, not 1/2 or √2/2)
    "phi/2":            (PHI/2,                  "cos(36°)"),
    "1/(2*phi)":        (1/(2*PHI),              "cos(72°)"),
    "sqrt5/2":          (sqrt(5)/2,              "t parameter"),
    "cos(18deg)":       (sqrt(2+PHI)/2,          "cos(18°)"),
    "sin(36deg)":       (sqrt(3-PHI)/2,          "sin(36°)"),

    # 7-fold trig (PSL(2,7) / Klein quartic)
    "cos(pi/7)":        (cos(pi/7),              "Klein triangle"),
    "cos(2pi/7)":       (cos(2*pi/7),            "7-fold"),
    "cos(3pi/7)":       (cos(3*pi/7),            "7-fold"),

    # Framework-specific packing constants
    "epsilon_2":        (1 - pi/(2*sqrt(3)),     "ζ = 9.31% lattice tax"),
    "eps_3/eps_2":      ((1 - pi/(3*sqrt(2)))/(1 - pi/(2*sqrt(3))), "Hales ratio"),
    "arctan(1/sqrt2)":  (atan(1/sqrt(2)),        "Prop P.α"),

    # The pulsation we're trying to address
    "pulsation":        (0.09480,                "pulsation amplitude"),
    "void":             (0.71284,                "1 - gap"),
    "gap":              (0.28716,                "84 - cascade ratio"),

    # Lattice + PSL(2,7) coset
    "8/21":             (8/21,                   "Cheeger constant"),

    # Cl-tower-related
    "84":               (84.0,                   "Cl(2)+Cl(4)+Cl(6)"),
    "21":               (21.0,                   "K₇ edges / Császár edges"),
}

TOLERANCE = 0.0005  # 0.05%


def match_curated(value):
    """Match value against curated constants. Reports only first match per direction."""
    if value is None or not np.isfinite(value) or abs(value) < 1e-10:
        return None
    # Check value and reciprocal
    best = None
    for name, (cval, desc) in CURATED_CONSTANTS.items():
        for v, suffix in [(value, ""), (1/value, " (recip)")]:
            if abs(v) < 1e-10:
                continue
            rel = abs(v - cval) / abs(cval)
            if rel < TOLERANCE:
                if best is None or rel < best[2]:
                    best = (name + suffix, desc, rel, cval)
    return best


def null_rate_curated(n_samples, seed=42):
    """Null model with the curated library."""
    rng = np.random.default_rng(seed)
    log_vals = rng.uniform(np.log(0.01), np.log(100), n_samples)
    vals = np.exp(log_vals)
    hits = sum(1 for v in vals if match_curated(v) is not None)
    return hits, hits / n_samples


def fano_lines():
    """The seven lines of the Fano plane (each is a triple of points 1-7)."""
    return [
        (1, 2, 3),
        (1, 4, 5),
        (1, 6, 7),
        (2, 4, 6),
        (2, 5, 7),
        (3, 4, 7),
        (3, 5, 6),
    ]


def is_fano_line(circle_indices):
    """Check whether a triple of circle indices (1-7) is a Fano line."""
    s = tuple(sorted(circle_indices))
    return s in [tuple(sorted(l)) for l in fano_lines()]


def parse_circle_index(label):
    """Convert '1_outer', '4_tube_R' etc to integer 1-7."""
    return int(label.split("_")[0])


def main():
    print("=" * 70)
    print("SEVEN-CIRCLES EXPERIMENT — TIGHTENED VERSION")
    print("=" * 70)
    print(f"Tolerance: {TOLERANCE*100:.3f}% (0.05%)")
    print(f"Curated constants: {len(CURATED_CONSTANTS)}")
    print()

    R, r = 3.0, 1.0
    circles = define_circles(R, r)

    # ============================================================
    # PRIMARY CHORD
    # ============================================================
    d = 1.5
    pts = run_chord(circles, d, 0.0)
    print(f"Primary chord: d={d}, θ=0, R={R}, r={r}")
    print(f"Intersection points: {len(pts)}")
    print()

    # Cross-ratios only (the structural ones)
    all_crs = []
    for combo in combinations(pts, 4):
        labels = [p[0] for p in combo]
        ts = [p[3] for p in combo]
        cr = cross_ratio(*ts)
        if cr is not None and np.isfinite(cr):
            all_crs.append({"labels": labels, "value": cr})

    print(f"Cross-ratios computed: {len(all_crs)}")
    print()

    # Match
    matches = []
    for q in all_crs:
        m = match_curated(q["value"])
        if m:
            matches.append((q, m))

    n_matches = len(matches)
    print(f"Cross-ratio matches: {n_matches} ({100*n_matches/len(all_crs):.2f}%)")
    null_hits, null_rate = null_rate_curated(len(all_crs))
    print(f"Null model:          {null_hits} ({100*null_rate:.2f}%)")
    if null_rate > 0:
        print(f"Enrichment:          {(n_matches/len(all_crs))/null_rate:.2f}x")
    print()

    # ============================================================
    # Report matches with circle-quadruple structure
    # ============================================================
    print("=" * 70)
    print("MATCHES — primary chord")
    print("=" * 70)
    if not matches:
        print("(none)")
    for q, m in matches:
        name, desc, rel, cval = m
        circle_idx = [parse_circle_index(l) for l in q["labels"]]
        circle_set = sorted(set(circle_idx))
        # Tag if the unique circle indices form a Fano line (3 distinct)
        tag = ""
        if len(circle_set) == 3 and is_fano_line(tuple(circle_set)):
            tag = " [FANO LINE]"
        elif len(circle_set) == 4:
            # Check if any 3-subset is a Fano line
            for triple in combinations(circle_set, 3):
                if is_fano_line(triple):
                    tag = f" [contains Fano line {triple}]"
                    break
        print(f"\n  circles {circle_set}{tag}")
        print(f"    quadruple labels: {q['labels']}")
        print(f"    cr value = {q['value']:.6f}")
        print(f"    ≈ {name} = {cval:.6f}  ({desc})  rel_err={rel*100:.4f}%")

    # ============================================================
    # STABILITY across chord position
    # ============================================================
    print()
    print("=" * 70)
    print("STABILITY SWEEP — vary chord position")
    print("=" * 70)
    print(f"{'d':>6}  {'CRs':>6}  {'matches':>8}  {'obs':>7}  {'null':>7}  {'enrich':>7}")
    sweep_results = []
    for d_sweep in np.linspace(0.1, 3.8, 20):
        pts_s = run_chord(circles, d_sweep, 0.0)
        crs_s = []
        for combo in combinations(pts_s, 4):
            ts = [p[3] for p in combo]
            cr = cross_ratio(*ts)
            if cr is not None and np.isfinite(cr):
                crs_s.append({"labels": [p[0] for p in combo], "value": cr})
        ms_s = sum(1 for q in crs_s if match_curated(q["value"]))
        rate = ms_s/len(crs_s) if crs_s else 0
        _, nr = null_rate_curated(len(crs_s), seed=int(d_sweep*1000))
        enr = rate/nr if nr > 0 else 0
        sweep_results.append((d_sweep, len(crs_s), ms_s, rate, nr, enr))
        print(f"{d_sweep:6.2f}  {len(crs_s):6d}  {ms_s:8d}  {100*rate:6.3f}%  {100*nr:6.3f}%  {enr:6.2f}x")

    rates = [s[3] for s in sweep_results]
    nulls = [s[4] for s in sweep_results]
    print()
    print(f"Mean observed: {100*np.mean(rates):.3f}%  (std {100*np.std(rates):.3f}%)")
    print(f"Mean null:     {100*np.mean(nulls):.3f}%  (std {100*np.std(nulls):.3f}%)")
    if np.mean(nulls) > 0:
        print(f"Mean enrichment: {np.mean(rates)/np.mean(nulls):.2f}x")
    print()

    # ============================================================
    # REPARAMETERIZATION SWEEP
    # ============================================================
    print("=" * 70)
    print("REPARAMETERIZATION — vary R/r")
    print("=" * 70)
    print(f"{'R/r':>6}  {'CRs':>6}  {'matches':>8}  {'obs':>7}  {'null':>7}  {'enrich':>7}")

    # Persistent matches: which constants survive across R/r?
    persistence = {}
    rr_ratios = [1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0]
    repar_results = []
    for rr in rr_ratios:
        circles_rr = define_circles(rr, 1.0)
        d_rr = 0.3 * (rr + 1.0)
        pts_rr = run_chord(circles_rr, d_rr, 0.0)
        crs_rr = []
        for combo in combinations(pts_rr, 4):
            ts = [p[3] for p in combo]
            cr = cross_ratio(*ts)
            if cr is not None and np.isfinite(cr):
                crs_rr.append({"labels": [p[0] for p in combo], "value": cr})
        ms_rr_set = set()
        ms_rr = 0
        for q in crs_rr:
            m = match_curated(q["value"])
            if m:
                ms_rr += 1
                base = m[0].replace(" (recip)", "")
                ms_rr_set.add(base)
        rate = ms_rr/len(crs_rr) if crs_rr else 0
        _, nr = null_rate_curated(len(crs_rr), seed=int(rr*100))
        enr = rate/nr if nr > 0 else 0
        repar_results.append((rr, len(crs_rr), ms_rr, rate, nr, enr))
        print(f"{rr:6.2f}  {len(crs_rr):6d}  {ms_rr:8d}  {100*rate:6.3f}%  {100*nr:6.3f}%  {enr:6.2f}x")
        for name in ms_rr_set:
            persistence[name] = persistence.get(name, 0) + 1

    rates = [r[3] for r in repar_results]
    nulls = [r[4] for r in repar_results]
    print()
    print(f"Mean observed: {100*np.mean(rates):.3f}%  (std {100*np.std(rates):.3f}%)")
    print(f"Mean null:     {100*np.mean(nulls):.3f}%  (std {100*np.std(nulls):.3f}%)")
    if np.mean(nulls) > 0:
        print(f"Mean enrichment: {np.mean(rates)/np.mean(nulls):.2f}x")
    print()

    # Persistence table
    print("=" * 70)
    print("CONSTANT PERSISTENCE across R/r")
    print("=" * 70)
    print(f"Constants matching at SOME cross-ratio in N of {len(rr_ratios)} R/r trials:")
    print()
    for name, count in sorted(persistence.items(), key=lambda x: -x[1]):
        marker = "★" if count >= 7 else ("•" if count >= 5 else " ")
        print(f"  {count}/{len(rr_ratios)}  {marker}  {name}")

    # ============================================================
    # Null model expectation for persistence
    # ============================================================
    print()
    print("Expected persistence under null: probability that a random number")
    print("matches ANY curated constant within 0.05% =", end=" ")
    # Each constant covers a fraction ~2 * TOLERANCE * (log-uniform density at that value)
    # In log-space, each constant gets a window of width 2*TOLERANCE.
    # Total covered = 2*TOLERANCE * 2 * len(constants) (factor 2 for reciprocal)
    log_window = 2*TOLERANCE * 2 * len(CURATED_CONSTANTS)
    log_range = np.log(100) - np.log(0.01)
    p_per_value = log_window / log_range
    print(f"~{100*p_per_value:.3f}% per value")
    n_crs_typical = 495  # from primary chord
    p_any = 1 - (1 - p_per_value)**n_crs_typical
    print(f"P(at least one match among {n_crs_typical} CRs) under null = "
          f"{100*p_any:.1f}%")
    print("If persistence ≈ that probability × 8 trials → noise.")
    print("If persistence is much higher AND on specific constants → signal.")


if __name__ == "__main__":
    main()
