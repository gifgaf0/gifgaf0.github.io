"""
THREE-PERSPECTIVE TEST
=======================

Same chord cutting the same two circles. Compute three different
cross-ratios based on observer position:

  CR_line:  external observer parameterizing the chord as a line
            (what we have been doing)
  CR_spine: observer at spine center, using angles to the 4 points
            seen from the origin
  CR_tube:  observer at tube center (R,0), using angles to the 4 points
            seen from (R,0)

Pre-registered prediction (recorded BEFORE computation):
  - CR_line stays in the mixed pool (φ/2, cos(π/7), cos(18°), √5/2, void)
  - CR_spine should preferentially expose L-perspective content
    (outer geometry / scale gap): void, gap, φ-tower values
  - CR_tube should preferentially expose O-perspective content
    (local curvature / breathing): the PULSATION 0.0948 should appear
    here if it has any geometric address at all

Falsification:
  If all three perspectives produce the same constant pool with the
  same distribution, perspective is not a structural filter.
  If pulsation appears in CR_tube but not CR_line or CR_spine, the
  perspective filter is real AND the pulsation has an O-perspective
  geometric address.
"""

import numpy as np
from math import pi, sqrt, cos, sin, atan, atan2
import sys
sys.path.insert(0, '/home/claude/circles_experiment')
from seven_circles_experiment import line_circle_intersect, cross_ratio
from seven_circles_tight import CURATED_CONSTANTS

PHI = (1 + sqrt(5)) / 2
STRICT_TOL = 5e-5


def two_circles(R, r):
    return [("spine", 0.0, 0.0, R), ("tube", R, 0.0, r)]


def chord_intersections(R, r, d, theta):
    """Returns list of (which_circle, x, y, t_line) for 4 intersection points."""
    px, py = d*cos(theta), d*sin(theta)
    dx, dy = -sin(theta), cos(theta)
    L = 20.0
    x1, y1 = px - L*dx, py - L*dy
    x2, y2 = px + L*dx, py + L*dy

    points = []
    for label, cx, cy, rad in two_circles(R, r):
        pts = line_circle_intersect(x1, y1, x2, y2, cx, cy, rad)
        for x, y, t in pts:
            points.append((label, x, y, t))
    points.sort(key=lambda p: p[3])
    return points


def cr_line(points):
    """Cross-ratio using chord parameter t."""
    if len(points) != 4:
        return None
    ts = [p[3] for p in points]
    return cross_ratio(*ts)


def cr_from_center(points, cx, cy):
    """Cross-ratio using angles to the 4 points as seen from (cx, cy).
    Returns CR of the four angles (treated as positions on a circle,
    so we use cross-ratio of their tangent-half-angle parameter, which
    is the standard projective cross-ratio on a conic)."""
    if len(points) != 4:
        return None
    # Angle from center to each point
    angles = []
    for label, x, y, t in points:
        a = atan2(y - cy, x - cx)
        angles.append(a)
    # For points on a circle, the cross-ratio can be computed using
    # the tangent half-angle: u = tan(α/2). This gives the standard
    # projective parameter on the circle viewed as RP^1.
    # If a point is NOT on the circle (i.e., it's just being viewed
    # angularly), we still use this parameter — it gives the angular
    # cross-ratio as seen from (cx, cy).
    us = [np.tan(a / 2) for a in angles]
    return cross_ratio(*us)


def match_curated(value, tol=STRICT_TOL):
    """Return (name, desc, rel_err, cval) of best match, or None."""
    if value is None or not np.isfinite(value) or abs(value) < 1e-10:
        return None
    best = None
    for name, (cv, desc) in CURATED_CONSTANTS.items():
        for v, sfx in [(value, ""), (1/value, " (recip)")]:
            if abs(v) < 1e-10: continue
            rel = abs(v - cv) / abs(cv)
            if rel < tol:
                if best is None or rel < best[2]:
                    best = (name + sfx, desc, rel, cv)
    return best


def classify(name):
    five = {'phi/2','1/(2*phi)','sqrt5/2','cos(18deg)','sin(36deg)',
            'phi','phi^-1','phi^-2','phi^-5','phi^5','phi^-3'}
    seven = {'cos(pi/7)','cos(2pi/7)','cos(3pi/7)'}
    eight4 = {'pulsation','void','gap'}
    base = name.replace(" (recip)", "")
    if base in five: return "5-fold"
    if base in seven: return "7-fold"
    if base in eight4: return "84-decomp"
    if base == 'arctan(1/sqrt2)': return "Prop P.α"
    if base == 'eps_3/eps_2' or base == 'epsilon_2': return "packing"
    if base == '8/21': return "PSL(2,7)"
    return "other"


def main():
    print("=" * 70)
    print("THREE-PERSPECTIVE TEST")
    print("=" * 70)
    print("Same chords cutting two circles, three observer cross-ratios:")
    print("  CR_line:  external line parameter")
    print("  CR_spine: angular CR as seen from spine center")
    print("  CR_tube:  angular CR as seen from tube center")
    print(f"Tolerance: {STRICT_TOL*100:.4f}%")
    print()

    R, r = 3.0, 1.0
    print(f"Config: R={R}, r={r}")
    print()

    # Dense sweep over (d, theta)
    n_d, n_theta = 100, 100
    d_grid = np.linspace(0.05, R + r - 0.05, n_d)
    theta_grid = np.linspace(0.01, pi - 0.01, n_theta)

    n_4pt = 0
    matches_line = []
    matches_spine = []
    matches_tube = []
    matches_pulsation = []  # special: any perspective hitting pulsation

    for theta in theta_grid:
        for d in d_grid:
            pts = chord_intersections(R, r, d, theta)
            if len(pts) != 4:
                continue
            n_4pt += 1

            crL = cr_line(pts)
            crS = cr_from_center(pts, 0.0, 0.0)      # spine center
            crT = cr_from_center(pts, R, 0.0)        # tube center

            for cr, lst in [(crL, matches_line),
                            (crS, matches_spine),
                            (crT, matches_tube)]:
                if cr is None: continue
                m = match_curated(cr)
                if m:
                    lst.append((d, theta, cr, m[0], classify(m[0]), m[2]))
                    if classify(m[0]) == "84-decomp" and "pulsation" in m[0]:
                        matches_pulsation.append((
                            "line" if lst is matches_line else
                            "spine" if lst is matches_spine else "tube",
                            d, theta, cr, m[2]))

    print(f"Chord configurations with 4 intersections: {n_4pt}")
    print()

    # ============================================================
    # Tabulate by perspective and register
    # ============================================================
    from collections import Counter

    print("=" * 70)
    print("RESULTS BY PERSPECTIVE")
    print("=" * 70)

    for pname, mlist in [("CR_line  (external)",   matches_line),
                          ("CR_spine (from origin)", matches_spine),
                          ("CR_tube  (from tube center)", matches_tube)]:
        print(f"\n{pname}: {len(mlist)} total matches "
              f"({100*len(mlist)/n_4pt:.2f}% hit rate)")
        if not mlist:
            continue
        # By register
        reg_count = Counter(m[4] for m in mlist)
        print(f"  Register distribution:")
        for reg, count in reg_count.most_common():
            pct = 100 * count / len(mlist)
            print(f"    {reg:<18s}  {count:4d}  ({pct:5.1f}%)")
        # By specific constant
        const_count = Counter(m[3].replace(" (recip)", "") for m in mlist)
        print(f"  Top constants:")
        for c, count in const_count.most_common(8):
            print(f"    {c:<24s}  {count:4d}")

    # ============================================================
    # Pulsation-specific check
    # ============================================================
    print()
    print("=" * 70)
    print("PULSATION-SPECIFIC CHECK (0.0948)")
    print("=" * 70)
    if matches_pulsation:
        print(f"Pulsation matches: {len(matches_pulsation)}")
        for persp, d, theta, cr, rel in matches_pulsation[:20]:
            print(f"  [{persp}] d={d:.4f}, θ={theta*180/pi:.2f}°: "
                  f"CR={cr:.5f} (rel={rel*100:.4f}%)")
    else:
        print("Pulsation: NO MATCHES in any perspective at 0.005% tolerance.")

    # ============================================================
    # Cross-comparison: which constants are EXCLUSIVE to which perspective?
    # ============================================================
    print()
    print("=" * 70)
    print("CONSTANT EXCLUSIVITY")
    print("=" * 70)
    print("Does each perspective expose constants the others miss?")
    print()

    consts_line = set(m[3].replace(" (recip)", "") for m in matches_line)
    consts_spine = set(m[3].replace(" (recip)", "") for m in matches_spine)
    consts_tube = set(m[3].replace(" (recip)", "") for m in matches_tube)

    print(f"Constants in CR_line:  {sorted(consts_line)}")
    print(f"Constants in CR_spine: {sorted(consts_spine)}")
    print(f"Constants in CR_tube:  {sorted(consts_tube)}")
    print()

    only_line = consts_line - consts_spine - consts_tube
    only_spine = consts_spine - consts_line - consts_tube
    only_tube = consts_tube - consts_line - consts_spine
    all_three = consts_line & consts_spine & consts_tube

    print(f"Only in CR_line:  {sorted(only_line) if only_line else '(none)'}")
    print(f"Only in CR_spine: {sorted(only_spine) if only_spine else '(none)'}")
    print(f"Only in CR_tube:  {sorted(only_tube) if only_tube else '(none)'}")
    print(f"In all three:     {sorted(all_three) if all_three else '(none)'}")

    # ============================================================
    # Distribution comparison: do the perspectives DIFFER significantly?
    # ============================================================
    print()
    print("=" * 70)
    print("ARE THE PERSPECTIVES DISTINGUISHABLE?")
    print("=" * 70)
    print()

    # Get total hit count by register for each perspective
    def reg_dist(mlist):
        c = Counter(m[4] for m in mlist)
        total = sum(c.values()) or 1
        return {r: count/total for r, count in c.items()}

    dL = reg_dist(matches_line)
    dS = reg_dist(matches_spine)
    dT = reg_dist(matches_tube)

    all_regs = set(dL.keys()) | set(dS.keys()) | set(dT.keys())
    print(f"{'Register':<18s}  {'line':>8s}  {'spine':>8s}  {'tube':>8s}")
    for reg in sorted(all_regs):
        print(f"  {reg:<16s}  {100*dL.get(reg,0):>7.2f}%  "
              f"{100*dS.get(reg,0):>7.2f}%  {100*dT.get(reg,0):>7.2f}%")


if __name__ == "__main__":
    main()
