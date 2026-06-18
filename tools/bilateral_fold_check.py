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


def localization_scan(f, delta, Ns=(1, 2, 3, 5, 10, 50, 1000)):
    """Distribute the deficit over N equal sub-folds: E_N = N·f(Δ/N). Does the
    energy PREFER localization (small N) or smearing (large N)? This tests the
    single-seam ANSATZ — the load-bearing assumption behind the gate (SQT-agent
    audit): a convex energy SMEARS (E_N→0 as N→∞), so the single localized fold is
    its WORST case — the localization is imposed AGAINST the metric, not by it."""
    Es = [(N, N * f(delta / N)) for N in Ns]
    if Es[-1][1] < Es[0][1] - 1e-9:
        trend = "decreasing → SMEARS (opposes localization)"
    elif abs(Es[-1][1] - Es[0][1]) < 1e-9:
        trend = "flat → INDIFFERENT to localization"
    else:
        trend = "increasing → localizes (prefers single fold)"
    return Es, trend


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

    # ── B6 (audit add-on) — is the single-seam localization preferred? ───────
    print("  B6 — the single-seam ANSATZ, tested (SQT-agent audit): distribute Δ")
    print("       over N equal sub-folds, E_N = N·f(Δ/N) — which N does each prefer?")
    for label, f in forms:
        Es, trend = localization_scan(f, delta)
        tag = label.split("[")[0].strip()
        print(f"     {tag:34} {trend}")
    print("     ⇒ the convex (GP) energy SMEARS — the single localized fold is its")
    print("       WORST case; localization is imposed AGAINST the metric (anti-GP),")
    print("       and the linear (Regge) term is indifferent to it too. So NEITHER")
    print("       term wants a single localized symmetric fold — localization is a")
    print("       separate (topological/ansatz) input, NOT supplied by the action.")
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
  GATE ADVANCED, NOT CLOSED — and the head-on attack lands as a clean instance of
  M.CW (combinatorics cannot fix the metric/sign). With the split left free:
    • the bare deficit-angle (Regge / topological) term is LINEAR ⇒ split-
      indifferent AND localization-indifferent: it CANNOT force the fold (the
      genuinely informative R1 negative — the "topological action forces it"
      reading is false);
    • forcing the symmetric split requires a fold-energy that is strictly CONVEX
      in the split angle θ — a SIGN (f″>0). This is Jensen-standard once convexity
      is granted (any convex f gives Δ/2: θ², θ⁴, cosh… all land on 18°), so the
      load-bearing import is convexity-in-θ, NOT "the GP functional" specifically.
    • and that convex energy SMEARS (B6): unconstrained it prefers N→∞ sub-folds
      (E_N→0), so the single-seam localization is its WORST case — imposed AGAINST
      the metric. Localization is a separate (topological/ansatz) input.
  So step (3) reduces to TWO named metric-class imports: (i) convexity-in-θ (a
  sign) and (ii) single-seam localization (anti-GP). By M.CW a sign is exactly
  what combinatorics can never supply — so "derive convexity from the lattice
  axioms" is NOT an achievable combinatorial task; the gate bottoms out at the
  standing substrate metric/dynamics import (the same one blocking §2.52
  pulsation=ζ). With (3) granted, step (4) gives cos18° = cos(π/10) = √(2+φ)/2.

  HONEST SCOPE (M.CW / M.BRIDGE): R1 for the geometry, the value identity, and the
  Regge split/localization-indifference negative; R2 (conditional on the two
  imports) for the forced bilateral fold. NOT R1 closure, and NOT a breach of the
  wall — it is the wall, precisely located. No observable asserted ((1−cos18°)
  void is downstream). No value reverse-engineered: θ and N were free.""")
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
