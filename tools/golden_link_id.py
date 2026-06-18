"""
golden_link_id.py — Independent identification of the golden-ellipse link type
=============================================================================
Settles the load-bearing question of the §3.4 retraction reversal: are the three
mutually-orthogonal golden ellipses (a=φ, b=1/φ) the BORROMEAN RINGS (μ̄=±1,
V4.29 correct) or the UNLINK (μ̄=0, V4.31's conclusion)?

Method (independent of the SQT-agent's extractor and of any μ̄ count):
  1. Build the three oriented golden ellipses exactly as in g2_milnor_sign.py.
  2. Apply a generic random rotation (break degenerate projection), project to 2D.
  3. Detect all transverse crossings; over/under from the dropped coordinate.
  4. Build a PD code from scratch (arc labelling along each oriented component,
     CCW arc order at each crossing starting from the incoming under-strand).
  5. Hand it to spherogram/SnapPy → simplify, count crossings, compute hyperbolic
     volume, identify against the census.

Validation FIRST, on controls with known answers, before trusting the golden run:
    • 3 separated circles  → must simplify to the 3-component UNLINK (0 crossings)
    • Hopf link (2 linked) → must give lk = ±1 / the Hopf link
    • braid Borromean      → vol 7.3277 / t12067  (the ground truth)
Only if the controls pass do we believe the golden-ellipse identification.

Requires numpy, snappy, spherogram. Author: §3.4-G2-CHIRAL audit, 2026-06-05.
"""

import math
import numpy as np
import spherogram
import snappy  # noqa: F401  (registers the kernel so Link.exterior() works)

PHI = (1 + math.sqrt(5)) / 2


# ── geometry ─────────────────────────────────────────────────────────────────
def golden_ellipses(n=400):
    """Three orthogonal golden ellipses, oriented, as in g2_milnor_sign.py."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    a, b = PHI, 1 / PHI
    C1 = np.stack([a * np.cos(t), b * np.sin(t), np.zeros(n)], 1)      # z=0
    C2 = np.stack([np.zeros(n), a * np.cos(t), b * np.sin(t)], 1)      # x=0
    C3 = np.stack([b * np.cos(t), np.zeros(n), a * np.sin(t)], 1)      # y=0
    return [C1, C2, C3]


def three_circles_split(n=200):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    base = np.stack([np.cos(t), np.sin(t), np.zeros(n)], 1)
    return [base + [0, 0, 0], base + [5, 0, 0], base + [10, 0, 0]]


def hopf(n=300):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    C1 = np.stack([np.cos(t), np.sin(t), np.zeros(n)], 1)
    C2 = np.stack([1 + np.cos(t), np.zeros(n), np.sin(t)], 1)
    return [C1, C2]


def rand_rotation(seed):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(3, 3))
    Q, R = np.linalg.qr(A)
    return Q * np.sign(np.diag(R))


# ── crossing detection + PD code ─────────────────────────────────────────────
def seg_intersection(p1, p2, p3, p4):
    """2D intersection params (s,t) of segments p1p2 and p3p4, or None."""
    d1 = p2 - p1
    d2 = p4 - p3
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-12:
        return None
    s = ((p3[0] - p1[0]) * d2[1] - (p3[1] - p1[1]) * d2[0]) / den
    t = ((p3[0] - p1[0]) * d1[1] - (p3[1] - p1[1]) * d1[0]) / den
    if 1e-9 < s < 1 - 1e-9 and 1e-9 < t < 1 - 1e-9:
        return s, t
    return None


def build_pd(curves):
    """Return a spherogram PD-style crossing list, or raise on degeneracy."""
    # crossings: list of dicts with component/segment/param/height/2D point
    cross = []
    ncomp = len(curves)
    for ci in range(ncomp):
        Ci = curves[ci]
        ni = len(Ci)
        for cj in range(ci, ncomp):
            Cj = curves[cj]
            nj = len(Cj)
            for a in range(ni):
                p1, p2 = Ci[a, :2], Ci[(a + 1) % ni, :2]
                z1a, z2a = Ci[a, 2], Ci[(a + 1) % ni, 2]
                b0 = a + 2 if ci == cj else 0   # skip adjacent self-segments
                for b in range(b0, nj):
                    if ci == cj and (b == a or (b + 1) % nj == a or b == (a + 1) % ni):
                        continue
                    p3, p4 = Cj[b, :2], Cj[(b + 1) % nj, :2]
                    hit = seg_intersection(p1, p2, p3, p4)
                    if hit is None:
                        continue
                    s, tt = hit
                    zi = z1a + s * (z2a - z1a)
                    zj = Cj[b, 2] + tt * (Cj[(b + 1) % nj, 2] - Cj[b, 2])
                    if abs(zi - zj) < 1e-9:
                        raise ValueError("degenerate height at crossing")
                    cross.append({
                        "i": (ci, a + s), "j": (cj, b + tt),
                        "i_over": zi > zj,
                        "ti": Ci[(a + 1) % ni, :2] - Ci[a, :2],
                        "tj": Cj[(b + 1) % nj, :2] - Cj[b, :2],
                        "pt": p1 + s * (p2 - p1),
                    })
    if not cross:
        return [], ncomp
    # ── label arcs: walk each component, split at its crossing passages ───────
    # collect passages per component: (param, crossing_idx, role) role: 'i' or 'j'
    passages = {c: [] for c in range(ncomp)}
    for k, x in enumerate(cross):
        passages[x["i"][0]].append((x["i"][1], k, "i"))
        passages[x["j"][0]].append((x["j"][1], k, "j"))
    for c in passages:
        passages[c].sort()
    # arc label = unique id per (component, position-in-walk).  The arc LEAVING a
    # passage and arriving at the next passage gets one label.
    arc_id = {}
    nid = 0
    for c in range(ncomp):
        m = len(passages[c])
        for r in range(m):
            arc_id[(c, r)] = nid       # arc after the r-th passage on comp c
            nid += 1
    # for each crossing, find under_in/out, over_in/out arc labels
    pos_in_walk = {}   # (k, role) -> index r in passages[component]
    for c in range(ncomp):
        for r, (_, k, role) in enumerate(passages[c]):
            pos_in_walk[(k, role)] = r
    pd = []
    for k, x in enumerate(cross):
        ci = x["i"][0]; cj = x["j"][0]
        ri = pos_in_walk[(k, "i")]; rj = pos_in_walk[(k, "j")]
        mi = len(passages[ci]); mj = len(passages[cj])
        in_i = arc_id[(ci, (ri - 1) % mi)]   # arc arriving at this passage on i
        out_i = arc_id[(ci, ri)]             # arc leaving
        in_j = arc_id[(cj, (rj - 1) % mj)]
        out_j = arc_id[(cj, rj)]
        if x["i_over"]:
            over_in, over_out, over_t = in_i, out_i, x["ti"]
            und_in, und_out, und_t = in_j, out_j, x["tj"]
        else:
            over_in, over_out, over_t = in_j, out_j, x["tj"]
            und_in, und_out, und_t = in_i, out_i, x["ti"]
        # CCW order of the four ends, starting from under-in (direction -und_t)
        ends = [
            (math.atan2(-und_t[1], -und_t[0]), und_in),
            (math.atan2(und_t[1], und_t[0]), und_out),
            (math.atan2(-over_t[1], -over_t[0]), over_in),
            (math.atan2(over_t[1], over_t[0]), over_out),
        ]
        a0 = ends[0][0]
        ends_sorted = sorted(ends, key=lambda e: (e[0] - a0) % (2 * math.pi))
        pd.append([lbl for _, lbl in ends_sorted])
    return pd, ncomp


def identify(curves, seed, label):
    R = rand_rotation(seed)
    rc = [c @ R.T for c in curves]
    pd, ncomp = build_pd(rc)
    if not pd:
        return f"{label} seed{seed}: 0 crossings, {ncomp} comps (split/unlink)"
    L = spherogram.Link(pd)
    nc0 = len(L.crossings)
    L.simplify(mode="global")
    info = f"{label} seed{seed}: raw {nc0} cr → simplified {len(L.crossings)} cr, " \
           f"{len(L.link_components)} comps"
    try:
        M = L.exterior()
        vol = float(M.volume())
        ids = M.identify()
        info += f"; vol={vol:.6f}; id={ids[0] if ids else 'none'}"
    except Exception as e:
        info += f"; (no hyperbolic structure: {type(e).__name__})"
    return info


def main():
    print("=" * 78)
    print("Independent link-type identification (own extractor + SnapPy)")
    print("=" * 78)
    print()
    print("GROUND TRUTH (spherogram braid closure):")
    B = spherogram.Link(braid_closure=[1, -2, 1, -2, 1, -2])
    print(f"  (σ₁σ₂⁻¹)³ : vol={float(B.exterior().volume()):.6f}, "
          f"id={B.exterior().identify()[0]}")
    print()
    print("CONTROLS (validate the extractor before trusting it):")
    for s in range(3):
        print("  " + identify(three_circles_split(), s, "3-split-circles"))
    for s in range(3):
        print("  " + identify(hopf(), s, "Hopf"))
    print()
    print("GOLDEN ELLIPSES (a=φ, b=1/φ) — the filed §3.4 configuration:")
    for s in range(6):
        print("  " + identify(golden_ellipses(), s, "golden"))
    print()
    print("=" * 78)
    print("If the controls pass (split→unlink, Hopf→Hopf) and golden→vol 7.3277,")
    print("the golden ellipses ARE the Borromean rings (μ̄=±1) ⇒ V4.29 correct,")
    print("V4.31 amphichirality retraction ERRONEOUS (it assumed μ̄ reflection-odd;")
    print("μ̄ is reflection-EVEN, so the symmetry imposes no constraint).")
    print("=" * 78)


if __name__ == "__main__":
    main()
