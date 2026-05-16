"""Seven-Circles Cross-Ratio Probe (Brief 07, formalised).

Reproduces and replaces the v1 scratch experiment at
``tools/_seven_circles_source/seven_circles_tight.py``. Brief 07 spec:
sweep 40 chord positions across the seven natural torus circles at the
canonical parameters (R=3, r=1) and count how many distinct chord
positions yield at least one 4-point cross-ratio that matches a
framework constant from a 23-entry curated library at 0.05% relative
tolerance.

The construction is taken verbatim from
``tools/_seven_circles_source/seven_circles_experiment.py``,
``…/seven_circles_tight.py``, and ``…/three_perspectives.py``. The
``CURATED_CONSTANTS`` library, the line-circle intersection geometry,
the cross-ratio formula, and the wing-tip circle derivation all come
from those files.

§X.1 of ``borromean_circumscription_derivation.md`` cites this probe
as the prior geometric address for cos 18° in the void correction
ζ·(1−cos 18°). cos 18° = √(2+φ)/2 (verified to float64 precision in
``tools/rho_derivation.py``).

EPISTEMIC NOTE — the 27/40 vs 14/40 reconciliation
==================================================

Brief 07 expected ``cos18_hits == 27`` (citing the scratch note).
The v5 of ``borromean_circumscription_derivation.md`` revised the
expected count to 14/40 with the dominant matches concentrating in
the hole-boundary geometry. **The probe verifies 14/40** at the
documented 0.05% tolerance with no parameter adjustment. The scratch
note's 27/40 figure does not reproduce under the construction
spelled out in the brief and the source files; the citable count is
14/40. cos 18° remains the joint-highest-frequency constant, tied
with √5/2 at 14/40 each, with cos(π/7) at 13/40.
"""

from __future__ import annotations

import math
from itertools import combinations
from math import atan, atan2, cos, pi, sin, sqrt
from typing import Optional

import numpy as np


# ---------------------------------------------------------------------------
# Curated framework constants
# ---------------------------------------------------------------------------
#
# Verbatim from ``tools/_seven_circles_source/seven_circles_tight.py``
# (the 23-entry "tightened" library — no generic rationals).

PHI = (1.0 + sqrt(5.0)) / 2.0

CURATED_CONSTANTS: dict[str, tuple[float, str]] = {
    # φ-tower (framework-specific)
    "phi":              (PHI,                              "(1+√5)/2"),
    "phi^-1":           (1.0 / PHI,                        "1/φ"),
    "phi^-2":           (1.0 / PHI ** 2,                   "1/φ²"),
    "phi^-3":           (1.0 / PHI ** 3,                   "1/φ³"),
    "phi^-5":           (1.0 / PHI ** 5,                   "1/φ⁵"),
    "phi^5":            (PHI ** 5,                         "φ⁵"),
    # 5-fold trig (framework-specific only)
    "phi/2":            (PHI / 2.0,                        "cos(36°)"),
    "1/(2*phi)":        (1.0 / (2.0 * PHI),                "cos(72°)"),
    "sqrt5/2":          (sqrt(5.0) / 2.0,                  "t parameter"),
    "cos(18deg)":       (sqrt(2.0 + PHI) / 2.0,            "cos(18°) = √(2+φ)/2"),
    "sin(36deg)":       (sqrt(3.0 - PHI) / 2.0,            "sin(36°)"),
    # 7-fold trig (PSL(2,7) / Klein quartic)
    "cos(pi/7)":        (cos(pi / 7.0),                    "Klein triangle"),
    "cos(2pi/7)":       (cos(2.0 * pi / 7.0),              "7-fold"),
    "cos(3pi/7)":       (cos(3.0 * pi / 7.0),              "7-fold"),
    # Framework-specific packing
    "epsilon_2":        (1.0 - pi / (2.0 * sqrt(3.0)),     "ζ lattice tax"),
    "eps_3/eps_2":      ((1.0 - pi / (3.0 * sqrt(2.0))) /
                          (1.0 - pi / (2.0 * sqrt(3.0))),  "Hales ratio"),
    "arctan(1/sqrt2)":  (atan(1.0 / sqrt(2.0)),            "Prop P.α"),
    # Pulsation / void / gap (84-decomposition)
    "pulsation":        (0.09480,                          "pulsation amplitude"),
    "void":             (0.71284,                          "1 - gap"),
    "gap":              (0.28716,                          "84 - cascade ratio"),
    # Lattice + PSL(2,7) coset
    "8/21":             (8.0 / 21.0,                       "Cheeger constant"),
    # Cl-tower-related
    "84":               (84.0,                             "Cl(2)+Cl(4)+Cl(6)"),
    "21":               (21.0,                             "K₇ / Császár edges"),
}

assert len(CURATED_CONSTANTS) == 23, (
    f"Library must contain 23 framework constants; got {len(CURATED_CONSTANTS)}"
)

# Canonical probe parameters.
R_CANONICAL = 3.0
r_CANONICAL = 1.0
N_CHORD_POSITIONS = 40
D_MIN = 0.1
D_MAX = 3.8
DEFAULT_TOL = 5.0e-4  # 0.05% relative


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------


def define_seven_circles(R: float = R_CANONICAL, r: float = r_CANONICAL) -> list[dict]:
    """Return the seven natural torus circles for T(R, r).

    Circle definitions come from ``seven_circles_experiment.py``:

    1. outer equator     (origin, R+r)
    2. hole equator      (origin, R−r)
    3. spine             (origin, R)
    4. tube cross-section ((R, 0), r)
    5. geometric mean    (origin, √(R²−r²))
    6. heptagon inradius (origin, (R−r)·cos(π/7))
    7. wing-tip          ((0, R·r/(R−2r)), |y₀+(R−r)|)

    The wing-tip circle passes through (R,−r), (−R,−r), (0,−(R−r));
    by symmetry its centre is on the y-axis, and the closed form
    follows from setting the three radial distances equal. Undefined
    at R = 2r.
    """
    if R <= 0 or r <= 0:
        raise ValueError("R and r must be positive")
    if R == 2 * r:
        raise ValueError("Wing-tip circle is undefined at R = 2r")
    circles: list[dict] = [
        {"centre": (0.0, 0.0), "radius": R + r,
         "label": "1_outer"},
        {"centre": (0.0, 0.0), "radius": R - r,
         "label": "2_hole"},
        {"centre": (0.0, 0.0), "radius": R,
         "label": "3_spine"},
        {"centre": (R, 0.0),   "radius": r,
         "label": "4_tube_R"},
        {"centre": (0.0, 0.0), "radius": sqrt(R * R - r * r),
         "label": "5_geo_mean"},
        {"centre": (0.0, 0.0), "radius": (R - r) * cos(pi / 7.0),
         "label": "6_hept_in"},
    ]
    y0 = R * r / (R - 2 * r)
    radius7 = abs(y0 + (R - r))
    circles.append({
        "centre": (0.0, y0), "radius": radius7, "label": "7_wingtip",
    })
    return circles


def _line_circle_intersect(
    x1: float, y1: float, x2: float, y2: float,
    cx: float, cy: float, rad: float,
) -> list[tuple[float, float, float]]:
    """Return (x, y, t) for each intersection of line p1→p2 with the circle."""
    dx, dy = x2 - x1, y2 - y1
    fx, fy = x1 - cx, y1 - cy
    a = dx * dx + dy * dy
    b = 2.0 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - rad * rad
    disc = b * b - 4.0 * a * c
    if disc < 0:
        return []
    sq = sqrt(disc)
    t1 = (-b - sq) / (2.0 * a)
    t2 = (-b + sq) / (2.0 * a)
    out: list[tuple[float, float, float]] = [
        (x1 + t1 * dx, y1 + t1 * dy, t1)
    ]
    if disc > 1e-12:
        out.append((x1 + t2 * dx, y1 + t2 * dy, t2))
    return out


def _chord_endpoints(d: float, theta: float, L: float = 20.0
                     ) -> tuple[float, float, float, float]:
    """Return (x1, y1, x2, y2) for a chord at distance d, angle θ."""
    px, py = d * cos(theta), d * sin(theta)
    dx, dy = -sin(theta), cos(theta)
    return px - L * dx, py - L * dy, px + L * dx, py + L * dy


def _intersect_chord(circles: list[dict], d: float, theta: float
                     ) -> list[tuple[str, float, float, float]]:
    """Return (label, x, y, t) for each intersection of the chord with any circle."""
    x1, y1, x2, y2 = _chord_endpoints(d, theta)
    pts: list[tuple[str, float, float, float]] = []
    for circle in circles:
        cx, cy = circle["centre"]
        rad = circle["radius"]
        for x, y, t in _line_circle_intersect(x1, y1, x2, y2, cx, cy, rad):
            pts.append((circle["label"], x, y, t))
    pts.sort(key=lambda p: p[3])
    return pts


def enumerate_chord_positions(circles: list[dict],
                              n: int = N_CHORD_POSITIONS,
                              d_min: float = D_MIN,
                              d_max: float = D_MAX,
                              theta: float = 0.0) -> list[dict]:
    """Enumerate the n horizontal chord positions over d ∈ [d_min, d_max].

    Returns a list of length n; each entry is::

        {"chord_id": int, "d": float, "theta": float, "pts": list}

    The brief's reference signature uses ``circle_i``/``circle_j`` keys.
    The scratch reference uses chord position (d-value) as the
    primary discriminator and computes cross-ratios over all 4-subsets
    of intersection points; this implementation follows the scratch
    reference, documented in the module docstring. The dict shape is
    kept compatible (a ``chord_id`` is still present); the
    circle-pair information is recovered from each cross-ratio's
    label tuple.
    """
    ds = np.linspace(d_min, d_max, n)
    return [
        {"chord_id": i, "d": float(d), "theta": float(theta),
         "pts": _intersect_chord(circles, float(d), theta)}
        for i, d in enumerate(ds)
    ]


# ---------------------------------------------------------------------------
# Cross-ratio
# ---------------------------------------------------------------------------


def _cross_ratio(t1: float, t2: float, t3: float, t4: float) -> Optional[float]:
    num = (t1 - t3) * (t2 - t4)
    den = (t1 - t4) * (t2 - t3)
    if abs(den) < 1e-14:
        return None
    return num / den


def compute_cr_tube(
    pts: list[tuple[str, float, float, float]],
    tube_centre: tuple[float, float],
) -> Optional[float]:
    """Cross-ratio of 4 points using tangent-half-angle from ``tube_centre``.

    Follows ``three_perspectives.py``: for each point compute the
    angle from ``tube_centre``, then the projective parameter
    ``tan(α/2)``. The cross-ratio of these four projective parameters
    is the angular cross-ratio as seen from the tube centre.
    Returns ``None`` for degenerate configurations.
    """
    if len(pts) != 4:
        return None
    cx, cy = tube_centre
    us: list[float] = []
    for _label, x, y, _t in pts:
        angle = atan2(y - cy, x - cx)
        us.append(math.tan(angle / 2.0))
    return _cross_ratio(*us)


def compute_cr_line(
    pts: list[tuple[str, float, float, float]],
) -> Optional[float]:
    """Cross-ratio along the chord parameter (external projective frame)."""
    if len(pts) != 4:
        return None
    return _cross_ratio(*[p[3] for p in pts])


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------


def _best_match(value: float, tol: float
                ) -> Optional[tuple[str, float, float]]:
    """Return (name, constant_value, rel_err) for the best match of ``value``
    or its reciprocal within ``tol``, or ``None``."""
    if value is None or not np.isfinite(value) or abs(value) < 1e-10:
        return None
    best: Optional[tuple[str, float, float]] = None
    for name, (cval, _desc) in CURATED_CONSTANTS.items():
        candidates = [(value, "")]
        if abs(value) > 1e-10:
            candidates.append((1.0 / value, " (recip)"))
        for v, sfx in candidates:
            rel = abs(v - cval) / abs(cval)
            if rel < tol and (best is None or rel < best[2]):
                best = (name + sfx, cval, rel)
    return best


# ---------------------------------------------------------------------------
# Public probe
# ---------------------------------------------------------------------------


def run_probe(R: float = R_CANONICAL, r: float = r_CANONICAL,
              tol: float = DEFAULT_TOL,
              n_positions: int = N_CHORD_POSITIONS) -> dict:
    """Run the seven-circles probe and return the full result dict.

    Counts, per curated constant, the number of chord positions
    (out of ``n_positions``) at which that constant appears in at
    least one 4-point chord cross-ratio. cos 18° is the
    framework-specific target; the full distribution is also reported.
    """
    circles = define_seven_circles(R, r)
    positions = enumerate_chord_positions(circles, n=n_positions)

    # Per-constant: set of chord_ids where it appears at least once.
    constant_positions: dict[str, set[int]] = {
        name: set() for name in CURATED_CONSTANTS
    }
    n_cr_total = 0
    n_cr_matched = 0
    for pos in positions:
        pts = pos["pts"]
        if len(pts) < 4:
            continue
        for combo in combinations(pts, 4):
            ts = [p[3] for p in combo]
            cr = _cross_ratio(*ts)
            if cr is None or not np.isfinite(cr):
                continue
            n_cr_total += 1
            m = _best_match(cr, tol)
            if m is not None:
                n_cr_matched += 1
                base = m[0].replace(" (recip)", "")
                constant_positions[base].add(pos["chord_id"])

    counts = {name: len(ids) for name, ids in constant_positions.items()}
    top = sorted(counts.items(), key=lambda kv: -kv[1])

    cos18_value = cos(pi / 10.0)
    cos18_identity = sqrt(2.0 + PHI) / 2.0
    identity_verified = math.isclose(cos18_value, cos18_identity, abs_tol=1e-12)

    return {
        "total_positions": n_positions,
        "cos18_hits": counts["cos(18deg)"],
        "cos18_fraction": counts["cos(18deg)"] / n_positions,
        "cos18_value": cos18_value,
        "cos18_identity": cos18_identity,
        "identity_verified": identity_verified,
        "full_distribution": counts,
        "top_constants": [(n, c) for n, c in top if c > 0],
        "tolerance": tol,
        "n_cross_ratios_computed": n_cr_total,
        "n_cross_ratios_matched": n_cr_matched,
        "R": R,
        "r": r,
    }


# ---------------------------------------------------------------------------
# Crystallographic exclusion check (three-perspective)
# ---------------------------------------------------------------------------


def run_pentagon_exclusion(R: float = R_CANONICAL, r: float = r_CANONICAL,
                           tol: float = DEFAULT_TOL,
                           n_d: int = 100, n_theta: int = 100) -> dict:
    """Two-circle three-perspective probe (spine + tube).

    Verbatim setup from ``three_perspectives.py``: sweep (d, θ); at
    each chord that yields exactly 4 intersections, compute CR_line
    (external projective frame) and CR_tube (angular from tube
    centre). Count cos 18° hits per perspective.

    The brief's ``test_pentagon_excluded_from_bulk`` requires
    ``CR_tube > 3 × CR_line``.
    """
    cos18 = sqrt(2.0 + PHI) / 2.0
    two_circles_geom = [
        {"centre": (0.0, 0.0), "radius": R, "label": "spine"},
        {"centre": (R, 0.0),   "radius": r, "label": "tube"},
    ]
    hits_line = 0
    hits_tube = 0
    n_four = 0
    for theta in np.linspace(0.01, pi - 0.01, n_theta):
        for d in np.linspace(0.05, R + r - 0.05, n_d):
            pts = _intersect_chord(two_circles_geom, float(d), float(theta))
            if len(pts) != 4:
                continue
            n_four += 1
            for cr_val, bucket in (
                (compute_cr_line(pts), "L"),
                (compute_cr_tube(pts, (R, 0.0)), "T"),
            ):
                if cr_val is None or not np.isfinite(cr_val):
                    continue
                rel = abs(cr_val - cos18) / cos18
                rel_recip = (abs(1.0 / cr_val - cos18) / cos18
                             if abs(cr_val) > 1e-10 else float("inf"))
                if rel < tol or rel_recip < tol:
                    if bucket == "L":
                        hits_line += 1
                    else:
                        hits_tube += 1
    ratio = (hits_tube / hits_line) if hits_line > 0 else float("inf")
    return {
        "n_four_point_configs": n_four,
        "cr_line_cos18_hits": hits_line,
        "cr_tube_cos18_hits": hits_tube,
        "tube_over_line": ratio,
        "passes_three_x_threshold": ratio > 3.0,
        "tolerance": tol,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _print_probe(result: dict) -> None:
    print("=" * 70)
    print("SEVEN-CIRCLES PROBE — Brief 07")
    print("=" * 70)
    print(f"R = {result['R']},  r = {result['r']}")
    print(f"Chord positions: {result['total_positions']}")
    print(f"Tolerance:       {result['tolerance'] * 100:.4f}% relative")
    print(f"Cross-ratios computed: {result['n_cross_ratios_computed']}")
    print(f"Cross-ratios matched:  {result['n_cross_ratios_matched']}")
    print()
    print(f"cos 18° identity √(2+φ)/2 ≡ cos(π/10): {result['identity_verified']}")
    print(f"  value:    {result['cos18_value']:.15f}")
    print(f"  identity: {result['cos18_identity']:.15f}")
    print()
    print(f"cos 18° hits: {result['cos18_hits']}/{result['total_positions']}"
          f"  ({100*result['cos18_fraction']:.2f}%)")
    print()
    print("Constants ranked by chord-position hits:")
    for name, count in result["top_constants"]:
        cval = CURATED_CONSTANTS[name][0]
        desc = CURATED_CONSTANTS[name][1]
        bar = "█" * count
        print(f"  {count:3d}/{result['total_positions']}  {name:<18s}"
              f" {cval:>11.6f}  {desc:<28s}  {bar}")


if __name__ == "__main__":
    res = run_probe()
    _print_probe(res)
    print()
    excl = run_pentagon_exclusion()
    print("=" * 70)
    print("PENTAGON EXCLUSION (three-perspective spine+tube)")
    print("=" * 70)
    print(f"4-point chord configs: {excl['n_four_point_configs']}")
    print(f"CR_line cos18 hits:    {excl['cr_line_cos18_hits']}")
    print(f"CR_tube cos18 hits:    {excl['cr_tube_cos18_hits']}")
    if math.isfinite(excl["tube_over_line"]):
        print(f"CR_tube / CR_line:     {excl['tube_over_line']:.2f}")
    else:
        print("CR_tube / CR_line:     ∞ (CR_line = 0)")
    print(f"Passes 3× threshold:   {excl['passes_three_x_threshold']}")
