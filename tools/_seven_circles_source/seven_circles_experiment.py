"""
Seven-Circles Cross-Ratio Experiment
=====================================

Procedure (fixed before running):
1. Define the seven natural torus circles in canonical coordinates (R=3, r=1).
2. Sweep a chord across the configuration; at each position compute all
   intersections.
3. Compute all chord-segment ratios, all radius ratios, and all 4-point
   cross-ratios on each chord.
4. Compare every computed value against the framework constants list
   with tolerance 0.5% (relative).
5. Report:
   - Total comparisons made
   - Number of matches
   - Null-model (random) hit rate for the same number of trials
   - Which framework constants matched, by what construction
6. Sweep over chord position to check stability.

NO PRE-SELECTION OF CIRCLES. NO TARGETING. Report everything.

Falsification criterion: if hit rate ≈ null rate, the seven-circle structure
does not encode framework constants beyond chance.
"""

import numpy as np
from itertools import combinations
from math import pi, sqrt, cos, sin, atan2, atan

# ============================================================
# FRAMEWORK CONSTANTS (from ledger and inventory files)
# ============================================================

PHI = (1 + sqrt(5)) / 2
PHI_INV = 1 / PHI

# All constants drawn from the framework. Source noted.
FRAMEWORK_CONSTANTS = {
    # φ-tower values
    "phi":              (PHI,            "(1+√5)/2"),
    "phi^-1":           (PHI_INV,        "1/φ = φ-1"),
    "phi^-2":           (PHI_INV**2,     "1/φ²"),
    "phi^-3":           (PHI_INV**3,     "1/φ³"),
    "phi^-4":           (PHI_INV**4,     "1/φ⁴"),
    "phi^-5":           (PHI_INV**5,     "1/φ⁵"),
    "phi^2":            (PHI**2,         "φ²"),
    "phi^3":            (PHI**3,         "φ³"),
    "phi^5":            (PHI**5,         "φ⁵"),

    # 5-fold trig register (phi_trig_inventory.md)
    "phi/2":            (PHI/2,          "cos(36°)"),
    "1/(2*phi)":        (1/(2*PHI),      "cos(72°)"),
    "sqrt5/2":          (sqrt(5)/2,      "controls t parameter"),
    "sqrt(2+phi)/2":    (sqrt(2+PHI)/2,  "cos(18°)"),
    "sqrt(3-phi)/2":    (sqrt(3-PHI)/2,  "sin(36°)"),

    # 7-fold trig register (Klein quartic / Fano)
    "cos(pi/7)":        (cos(pi/7),      "Klein triangle angle"),
    "cos(2pi/7)":       (cos(2*pi/7),    "7-fold trig"),
    "cos(3pi/7)":       (cos(3*pi/7),    "7-fold trig"),
    "sin(pi/7)":        (sin(pi/7),      "7-fold trig"),

    # Packing / framework constants
    "epsilon_2":        (1 - pi/(2*sqrt(3)),     "ζ = 9.31% lattice tax"),
    "epsilon_3":        (1 - pi/(3*sqrt(2)),     "3D packing gap"),
    "eps_3/eps_2":      ((1 - pi/(3*sqrt(2)))/(1 - pi/(2*sqrt(3))), "Hales ratio"),
    "arctan(1/sqrt2)":  (atan(1/sqrt(2)),        "Prop P.α"),
    "tan(arctan(1/√2))":(1/sqrt(2),              "Prop P.α tangent"),

    # Pulsation-related (from May 13 entry)
    "pulsation_0.0948": (0.09480,        "pulsation amplitude"),
    "void_0.71284":     (0.71284,        "1 - gap"),
    "gap_0.28716":      (0.28716,        "84 - cascade ratio"),

    # Lattice tax
    "14/15":            (14/15,          "lattice geometric tax"),
    "24deg":            (24*pi/180,      "per-edge deficit"),
    "8/21":             (8/21,           "Cheeger constant PSL(2,7)"),
    "2/3":              (2/3,            "λ₁ coset Laplacian"),

    # Simple rationals that show up
    "1/2":              (0.5,            "half"),
    "1/3":              (1/3,            "third"),
    "1/4":              (0.25,           "quarter"),
    "1/5":              (0.2,            "fifth"),
    "1/6":              (1/6,            "sixth"),
    "1/7":              (1/7,            "seventh"),
    "2/7":              (2/7,            "two sevenths"),
    "3/7":              (3/7,            "three sevenths"),
    "5/7":              (5/7,            "five sevenths"),

    # π-related
    "pi":               (pi,             "π"),
    "pi/2":             (pi/2,           "π/2"),
    "pi/3":             (pi/3,           "π/3"),
    "pi/4":             (pi/4,           "π/4"),
    "pi/5":             (pi/5,           "π/5"),
    "pi/6":             (pi/6,           "π/6"),
    "pi/7":             (pi/7,           "π/7"),
    "2pi":              (2*pi,           "2π"),
    "2/pi":             (2/pi,           "2/π"),
    "1/pi":             (1/pi,           "1/π"),

    # √2, √3 family
    "sqrt2":            (sqrt(2),        "√2"),
    "sqrt3":            (sqrt(3),        "√3"),
    "1/sqrt2":          (1/sqrt(2),      "1/√2"),
    "sqrt2/2":          (sqrt(2)/2,      "√2/2"),
    "sqrt3/2":          (sqrt(3)/2,      "√3/2"),
}

# ============================================================
# SEVEN CIRCLES (canonical torus silhouette, R=3, r=1)
# ============================================================

def define_circles(R=3.0, r=1.0):
    """Returns list of (label, center_x, center_y, radius)."""
    circles = []
    # ① Outer equator
    circles.append(("1_outer",      0.0, 0.0, R + r))
    # ② Inner equator (hole edge)
    circles.append(("2_hole",       0.0, 0.0, R - r))
    # ③ Spine circle
    circles.append(("3_spine",      0.0, 0.0, R))
    # ④ Tube cross-section (right side; the left is mirror)
    circles.append(("4_tube_R",     R,   0.0, r))
    # ⑤ Geometric mean
    circles.append(("5_geo_mean",   0.0, 0.0, sqrt(R*R - r*r)))
    # ⑥ Heptagon inradius in hole
    circles.append(("6_hept_in",    0.0, 0.0, (R - r) * cos(pi/7)))
    # ⑦ Wing-tip circle: through (R,-r), (-R,-r), (0,-(R-r))
    # by symmetry the center is on the y-axis. Three points on a circle:
    # (R,-r) and (-R,-r) are reflections → center at (0, y0)
    # (0, y0): distance to (R,-r) = √(R² + (y0+r)²)
    # distance to (0,-(R-r)) = |y0 + (R-r)|
    # set equal: R² + (y0+r)² = (y0+(R-r))²
    # R² + y0² + 2r·y0 + r² = y0² + 2(R-r)·y0 + (R-r)²
    # R² + 2r·y0 + r² = 2(R-r)·y0 + (R-r)²
    # 2r·y0 - 2(R-r)·y0 = (R-r)² - R² - r²
    # 2y0(r - R + r) = (R-r)² - R² - r²
    # 2y0(2r - R) = R² - 2Rr + r² - R² - r² = -2Rr
    # y0 = -Rr / (2r - R) = Rr / (R - 2r)
    if R != 2*r:
        y0 = R*r / (R - 2*r)
        radius_7 = abs(y0 + (R - r))
        circles.append(("7_wingtip", 0.0, y0, radius_7))
    return circles


# ============================================================
# CHORD-CIRCLE INTERSECTIONS
# ============================================================

def line_circle_intersect(x1, y1, x2, y2, cx, cy, r):
    """
    Line through (x1,y1)-(x2,y2), circle at (cx,cy) radius r.
    Returns list of (x,y) intersection points (0, 1, or 2 points).
    """
    dx, dy = x2 - x1, y2 - y1
    fx, fy = x1 - cx, y1 - cy
    a = dx*dx + dy*dy
    b = 2 * (fx*dx + fy*dy)
    c = fx*fx + fy*fy - r*r
    disc = b*b - 4*a*c
    if disc < 0:
        return []
    sq = sqrt(disc)
    t1 = (-b - sq) / (2*a)
    t2 = (-b + sq) / (2*a)
    pts = []
    pts.append((x1 + t1*dx, y1 + t1*dy, t1))
    if disc > 1e-12:
        pts.append((x1 + t2*dx, y1 + t2*dy, t2))
    return pts


def cross_ratio(t1, t2, t3, t4):
    """Standard cross-ratio of 4 colinear points parameterized by t-values."""
    num = (t1 - t3) * (t2 - t4)
    den = (t1 - t4) * (t2 - t3)
    if abs(den) < 1e-14:
        return None
    return num / den


# ============================================================
# CONSTANT MATCHING
# ============================================================

def match_to_framework(value, tolerance=0.005):
    """
    Return list of (constant_name, description, rel_error) for matches
    within `tolerance` relative error.
    Also checks the reciprocal of the value.
    """
    if value is None or not np.isfinite(value):
        return []
    if abs(value) < 1e-10:
        return []
    matches = []
    for name, (cval, desc) in FRAMEWORK_CONSTANTS.items():
        for v, marker in [(value, ""), (1/value, "^-1")]:
            if abs(v) < 1e-10:
                continue
            rel = abs(v - cval) / abs(cval)
            if rel < tolerance:
                matches.append((name + marker, desc, rel))
    return matches


# ============================================================
# EXPERIMENT
# ============================================================

def run_chord(circles, d, theta):
    """
    Run one chord at perpendicular distance d from origin, angle theta.
    Returns dict of all measured quantities.
    """
    # Line: passes at distance d from origin, normal direction (cos θ, sin θ)
    # Parametrize as: point on line + t * direction
    # Closest point to origin: (d cos θ, d sin θ)
    # Direction along line: (-sin θ, cos θ)
    px, py = d*cos(theta), d*sin(theta)
    dx, dy = -sin(theta), cos(theta)
    # Two distant endpoints to define a finite segment
    L = 20.0
    x1, y1 = px - L*dx, py - L*dy
    x2, y2 = px + L*dx, py + L*dy

    all_points = []  # (circle_label, x, y, t_param)
    for label, cx, cy, r in circles:
        pts = line_circle_intersect(x1, y1, x2, y2, cx, cy, r)
        for x, y, t in pts:
            all_points.append((label, x, y, t))

    # Sort by t-parameter (position along line)
    all_points.sort(key=lambda p: p[3])

    return all_points


def compute_all_quantities(circles, chord_points):
    """
    Compute every plausible scale-invariant quantity:
    - All radius ratios
    - All chord-segment ratios on the chord
    - All cross-ratios of 4 colinear points
    """
    quantities = []

    # 1. Radius ratios
    for (l1, _, _, r1), (l2, _, _, r2) in combinations(circles, 2):
        if r1 > 0 and r2 > 0:
            quantities.append({
                "type": "radius_ratio",
                "construction": f"r({l1})/r({l2})",
                "value": r1/r2,
            })

    # 2. Chord-segment ratios (pairs of points / pairs of points)
    if len(chord_points) >= 4:
        t_vals = [(p[0], p[3]) for p in chord_points]
        # Pairwise distances along chord
        pairs = []
        for (l1, t1), (l2, t2) in combinations(t_vals, 2):
            pairs.append((l1, l2, abs(t1 - t2)))
        # Ratios of distances
        for (la1, la2, d1), (lb1, lb2, d2) in combinations(pairs, 2):
            if d2 > 1e-10:
                quantities.append({
                    "type": "segment_ratio",
                    "construction": f"|{la1}-{la2}|/|{lb1}-{lb2}|",
                    "value": d1/d2,
                })

    # 3. Cross-ratios of 4 colinear points
    if len(chord_points) >= 4:
        for combo in combinations(chord_points, 4):
            labels = [p[0] for p in combo]
            ts = [p[3] for p in combo]
            cr = cross_ratio(*ts)
            if cr is not None and np.isfinite(cr):
                quantities.append({
                    "type": "cross_ratio",
                    "construction": f"CR({labels[0]},{labels[1]};{labels[2]},{labels[3]})",
                    "value": cr,
                })

    return quantities


# ============================================================
# NULL MODEL
# ============================================================

def null_model_hit_rate(n_samples, tolerance=0.005, seed=42):
    """
    Generate n_samples random numbers in the same range as the experiment
    values and check match rate against framework constants.
    """
    rng = np.random.default_rng(seed)
    # Sample log-uniform over [0.01, 100] since values span orders of magnitude
    log_vals = rng.uniform(np.log(0.01), np.log(100), n_samples)
    vals = np.exp(log_vals)
    hits = 0
    for v in vals:
        if match_to_framework(v, tolerance):
            hits += 1
    return hits, hits / n_samples


# ============================================================
# RUN
# ============================================================

def main():
    print("=" * 70)
    print("SEVEN-CIRCLES CROSS-RATIO EXPERIMENT")
    print("=" * 70)
    print(f"Tolerance: 0.5% relative error")
    print(f"Framework constants in library: {len(FRAMEWORK_CONSTANTS)}")
    print()

    # Single chord at d=1.5, θ=0 (horizontal line at y=1.5)
    # This is one specific chord. We'll vary later.
    R, r = 3.0, 1.0
    circles = define_circles(R, r)
    print(f"Torus: R={R}, r={r}")
    print(f"Circles defined: {len(circles)}")
    for label, cx, cy, rad in circles:
        print(f"  {label}: center=({cx:.3f},{cy:.3f}), radius={rad:.5f}")
    print()

    # Run primary chord
    d_primary = 1.5
    theta_primary = 0.0  # horizontal
    print(f"Primary chord: d={d_primary}, θ={theta_primary} (horizontal y=1.5)")
    chord_points = run_chord(circles, d_primary, theta_primary)
    print(f"Intersection points on chord: {len(chord_points)}")
    for label, x, y, t in chord_points:
        print(f"  t={t:+.4f}  ({x:+.4f}, {y:+.4f})  on {label}")
    print()

    # Compute all quantities
    quantities = compute_all_quantities(circles, chord_points)
    n_radius = sum(1 for q in quantities if q["type"] == "radius_ratio")
    n_segment = sum(1 for q in quantities if q["type"] == "segment_ratio")
    n_cross = sum(1 for q in quantities if q["type"] == "cross_ratio")
    n_total = len(quantities)
    print(f"Quantities computed:")
    print(f"  Radius ratios:     {n_radius}")
    print(f"  Segment ratios:    {n_segment}")
    print(f"  4-point CR:        {n_cross}")
    print(f"  TOTAL:             {n_total}")
    print()

    # Match against framework
    print("=" * 70)
    print("MATCHES (relative error < 0.5%)")
    print("=" * 70)
    n_matches = 0
    matched_quantities = []
    for q in quantities:
        m = match_to_framework(q["value"], tolerance=0.005)
        if m:
            n_matches += 1
            matched_quantities.append((q, m))

    # Sort matches by type then construction
    matched_quantities.sort(key=lambda x: (x[0]["type"], x[0]["construction"]))

    def strip_inverse(name):
        return name[:-3] if name.endswith("^-1") else name

    for q, matches in matched_quantities:
        print(f"\n[{q['type']}] {q['construction']}")
        print(f"  value = {q['value']:.6f}")
        for name, desc, rel in matches:
            base = strip_inverse(name)
            print(f"  ≈ {name} = {FRAMEWORK_CONSTANTS[base][0]:.6f}  "
                  f"({desc})  rel_err={rel*100:.3f}%")

    print()
    print("=" * 70)
    print(f"TOTAL MATCHES: {n_matches} out of {n_total} ({100*n_matches/n_total:.2f}%)")
    print("=" * 70)
    print()

    # Null model
    print("NULL MODEL (random log-uniform values):")
    null_hits, null_rate = null_model_hit_rate(n_total, tolerance=0.005)
    print(f"  Random hits in {n_total} trials: {null_hits} ({100*null_rate:.2f}%)")
    print(f"  Observed:                       {n_matches} ({100*n_matches/n_total:.2f}%)")
    if null_rate > 0:
        enrichment = (n_matches/n_total) / null_rate
        print(f"  Enrichment factor: {enrichment:.2f}x")
    print()

    # ============================================================
    # STABILITY: vary the chord
    # ============================================================
    print("=" * 70)
    print("STABILITY SWEEP: vary chord position")
    print("=" * 70)
    print(f"Sweeping d from 0.1 to 3.8 (cannot exceed R+r=4), θ=0")
    print(f"{'d':>6}  {'pts':>4}  {'total':>7}  {'matches':>8}  {'rate':>7}  {'null':>7}")

    stability_results = []
    for d in np.linspace(0.1, 3.8, 20):
        pts = run_chord(circles, d, 0.0)
        qs = compute_all_quantities(circles, pts)
        mts = sum(1 for q in qs if match_to_framework(q["value"], 0.005))
        rate = mts / len(qs) if qs else 0
        _, null_r = null_model_hit_rate(len(qs), tolerance=0.005, seed=int(d*1000))
        stability_results.append((d, len(pts), len(qs), mts, rate, null_r))
        print(f"{d:6.2f}  {len(pts):4d}  {len(qs):7d}  {mts:8d}  {100*rate:6.2f}%  {100*null_r:6.2f}%")

    # Summary statistics across sweep
    rates = [s[4] for s in stability_results]
    nulls = [s[5] for s in stability_results]
    print()
    print(f"Mean observed rate: {100*np.mean(rates):.2f}% (std {100*np.std(rates):.2f}%)")
    print(f"Mean null rate:     {100*np.mean(nulls):.2f}% (std {100*np.std(nulls):.2f}%)")
    if np.mean(nulls) > 0:
        print(f"Mean enrichment:    {np.mean(rates)/np.mean(nulls):.2f}x")
    print()

    # Save matched-constants frequency table
    print("=" * 70)
    print("CONSTANTS THAT MATCHED (across primary chord)")
    print("=" * 70)
    constant_counts = {}
    for q, matches in matched_quantities:
        for name, desc, rel in matches:
            constant_counts[name] = constant_counts.get(name, 0) + 1
    for name, count in sorted(constant_counts.items(), key=lambda x: -x[1]):
        base = strip_inverse(name)
        val = FRAMEWORK_CONSTANTS[base][0]
        print(f"  {count:4d}x  {name:30s} = {val:.6f}")


if __name__ == "__main__":
    main()
