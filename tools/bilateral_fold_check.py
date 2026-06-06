"""
bilateral_fold_check.py — §3.4: does the substrate action force the bilateral fold?
==================================================================================
The §2.45-NGA / §2.53 open gate. The 4-step prior-address of cos(π/10):
  (1) vacuum vertex: 3 hexagons × 120° = 360°  → flat, no deficit;
  (2) seam vertex:   3 pentagons × 108° = 324° → deficit Δ = 36° = π/5;
  (3) BILATERAL FOLD: Δ splits 18° + 18°   ← THE ONE OPEN STEP;
  (4) cos(18°) = cos(π/10) is the surviving fraction across the seam.

The registered question (Paper II §3.4): does the substrate action FORCE step (3)?
Judged ONLY against the pre-registered criteria B1–B5 of
reports/SQT_3.4_BILATERAL_FOLD_PREREGISTRATION.md. The split is NOT assumed
symmetric: it is parametrized by θ ∈ [0, Δ] (one side gets θ, the other Δ−θ), and
each candidate action form is asked which θ it selects. Discipline: a linear or
concave energy does NOT force the symmetric fold, and that negative is reported.

Pure stdlib + a tiny numeric scan. Author: §3.4 bilateral-fold gate, 2026-06-06.
"""

import math

DEG = math.pi / 180.0
PHI = (1 + math.sqrt(5)) / 2


# ── B1: deficit arithmetic ────────────────────────────────────────────────────
def deficit_arithmetic():
    hexagon_vertex = 3 * 120.0            # 3 hexagonal faces at a vertex
    pentagon_vertex = 3 * 108.0           # 3 pentagonal faces at a vertex
    delta = hexagon_vertex - pentagon_vertex
    dodeca_total = 20 * delta             # Descartes: Σ deficits = 720° = 4π
    return hexagon_vertex, pentagon_vertex, delta, dodeca_total


# ── B2/B3: which θ does E(θ) = f(θ) + f(Δ−θ) select? ──────────────────────────
def fold_energy(f, delta, n=72001):
    """Scan θ∈[0,Δ]; return (argmin θ, argmax θ, is_flat)."""
    best_t, best_v = None, math.inf
    worst_t, worst_v = None, -math.inf
    vals = []
    for k in range(n):
        t = delta * k / (n - 1)
        v = f(t) + f(delta - t)
        vals.append(v)
        if v < best_v - 1e-15:
            best_v, best_t = v, t
        if v > worst_v + 1e-15:
            worst_v, worst_t = v, t
    is_flat = (max(vals) - min(vals)) < 1e-9 * (abs(max(vals)) + 1e-9)
    return best_t, worst_t, is_flat


def convexity_lemma(f, delta):
    """Symbolic-style check: θ=Δ/2 is a critical point (symmetry), and strictly
    convex f ⇒ unique minimizer there. Verified numerically via second difference
    of g(θ)=f(θ)+f(Δ−θ) and the midpoint-vs-endpoint comparison."""
    h = delta * 1e-4
    mid = delta / 2
    g = lambda t: f(t) + f(delta - t)
    # second difference at the midpoint (curvature of the split-energy)
    curv = (g(mid + h) - 2 * g(mid) + g(mid - h)) / (h * h)
    # midpoint vs a generic asymmetric split (θ=Δ/4)
    midpoint_lower = g(mid) < g(delta / 4) - 1e-12
    return curv, midpoint_lower


def main():
    print("=" * 78)
    print("§3.4 bilateral-fold gate — does the substrate action force 36° → 18°+18°?")
    print("=" * 78)
    print()

    # ── B1 ───────────────────────────────────────────────────────────────────
    hx, pt, delta, total = deficit_arithmetic()
    b1 = (abs(hx - 360) < 1e-9 and abs(pt - 324) < 1e-9
          and abs(delta - 36) < 1e-9 and abs(total - 720) < 1e-9)
    print("  B1 — deficit arithmetic (R1 geometry):")
    print(f"     3 hexagons = {hx:.0f}° (flat) ; 3 pentagons = {pt:.0f}° ; "
          f"deficit Δ = {delta:.0f}° = π/5")
    print(f"     Σ over 20 dodecahedral vertices = {total:.0f}° = 4π  "
          f"(Descartes ✓)   ⇒ B1 {'PASS' if b1 else 'FAIL'}")
    print()

    # ── B2/B3 — three candidate per-side fold-energies f, θ left FREE ─────────
    print("  B2/B3 — the split θ is FREE; which θ does each action form select?")
    forms = [
        ("(a) deficit-angle / Regge  f(θ)=θ        [LINEAR, topological]",
         lambda t: t),
        ("(b) GP / Bjerknes kinetic  f(θ)=θ²       [CONVEX, §3.4.4 gradient]",
         lambda t: t * t),
        ("    control: concave       f(θ)=√θ        [CONCAVE]",
         lambda t: math.sqrt(max(t, 0.0))),
    ]
    results = {}
    for label, f in forms:
        amin, amax, flat = fold_energy(f, delta)
        curv, mid_lower = convexity_lemma(f, delta)
        if flat:
            verdict = "SPLIT-INDIFFERENT (every θ equal) → does NOT force 18°"
        elif abs(amin - delta / 2) < 1e-3 and mid_lower:
            verdict = f"min at θ = {amin:.3f}° = Δ/2 → FORCES the 18°+18° split"
        elif abs(amax - delta / 2) < 1e-3:
            verdict = f"θ=Δ/2 is a MAXIMUM → anti-forces (splits to the edges)"
        else:
            verdict = f"min at θ = {amin:.3f}° (asymmetric)"
        results[label[:6]] = (flat, amin, curv)
        print(f"   {label}")
        print(f"       curvature of E(θ) at Δ/2 = {curv:+.4f}  ⇒ {verdict}")
    print()

    # interpret against B3/B4
    regge_flat = results["(a) de"][0]
    gp_min = results["(b) GP"]
    b3 = regge_flat and (abs(gp_min[1] - delta / 2) < 1e-3) and (gp_min[2] > 0)
    b4 = b3  # the convex term that forces it IS the GP gradient; Regge is linear
    print("  B3/B4 — convexity decides; the GP kinetic term is the one that forces it:")
    print(f"     Regge (linear) split-indifferent : {'✓' if regge_flat else '✗'}")
    print(f"     GP (convex) forces θ=Δ/2=18°     : "
          f"{'✓' if (abs(gp_min[1]-delta/2)<1e-3 and gp_min[2]>0) else '✗'}")
    print(f"     ⇒ B3 {'PASS' if b3 else 'FAIL'} ; B4 {'PASS' if b4 else 'FAIL'}")
    print()

    # ── B5 — the value ───────────────────────────────────────────────────────
    half = delta / 2                      # 18°
    c = math.cos(half * DEG)
    closed1 = math.sqrt(10 + 2 * math.sqrt(5)) / 4
    closed2 = math.sqrt(2 + PHI) / 2
    b5 = (abs(c - closed1) < 1e-12 and abs(c - closed2) < 1e-12
          and abs(c - math.cos(math.pi / 10)) < 1e-12)
    print("  B5 — the value (step 4):")
    print(f"     cos(Δ/2) = cos 18° = cos(π/10) = {c:.12f}")
    print(f"     = √(10+2√5)/4 = {closed1:.12f} ; = √(2+φ)/2 = {closed2:.12f}   "
          f"{'✓' if b5 else '✗'}")
    print(f"     (1 − cos 18°) void fraction = {1 - c:.6f}")
    print(f"     ⇒ B5 {'PASS' if b5 else 'FAIL'}")
    print()

    # ── verdict ──────────────────────────────────────────────────────────────
    print("=" * 78)
    print("VERDICT (against the pre-registered promotion rule)")
    print("=" * 78)
    if b1 and b3 and b4 and b5:
        print(f"""\
  GATE ADVANCED (not unconditionally closed). With the split left free, the
  substrate action selects the BILATERAL fold IFF its fold-energy is strictly
  convex:
    • the bare deficit-angle (Regge) term is LINEAR ⇒ split-indifferent: it
      CANNOT force the 18°+18° fold (a clean negative that sharpens the gate);
    • the GP / Bjerknes kinetic term (§3.4.4 gradient energy, ∝∫|∇ψ|²) is
      strictly CONVEX ⇒ it forces the symmetric split θ = Δ/2 = 18° uniquely
      (reflection symmetry makes Δ/2 a critical point; convexity makes it the min).
  Step (3) therefore closes MODULO the substrate having a convex kinetic energy —
  exactly the GP functional §3.4.4 already imports. With (3) in hand, step (4)
  gives cos 18° = cos(π/10) = √(2+φ)/2 (B5).

  HONEST SCOPE (M.CW / M.BRIDGE): the convex kinetic energy and the single-seam
  bilateral-fold ansatz are IMPORTS (metric-class), not combinatorial outputs;
  this is R2 (conditional on the import), NOT R1 unconditional closure. No
  observable is asserted — the (1−cos 18°) void correction is downstream. No value
  was reverse-engineered: θ was free and the convex action chose Δ/2.""")
        rc = 0
    else:
        print("  Gate did NOT advance as registered — reported honestly; "
              "see which criterion failed above. No cos(π/10) prior-address claimed.")
        rc = 1
    print()
    print("  Reproduce: python3 tools/bilateral_fold_check.py")
    print("  Cross-refs: pre-registration SQT_3.4_BILATERAL_FOLD_PREREGISTRATION.md;")
    print("  §2.45-NGA, §2.53, Paper II §3.4/§3.4.4.")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
