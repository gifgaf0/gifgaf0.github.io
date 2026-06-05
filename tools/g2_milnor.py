"""
g2_milnor.py — §3.4-G2-Milnor: the φ-weighted Milnor triple-linking on the baryon
=================================================================================
The actual baryon gate pre-registered in §3.4-G2-Borromean. G2-orient showed the
pairwise Hopf charge is blind to the Borromean baryon; the baryon's content is
the cubic Milnor triple-linking μ̄(123). This computes the φ-weighted version

    μ̄^φ = φ_{d₁d₂d₃} · μ̄(123)

on a genuine Borromean configuration, with the discipline the audit demanded:

  • MAGNITUDE |μ̄| validated on controls (not asserted): |μ̄| = number of triple
    points of the three flat Seifert disks. Borromean ⇒ 1 (textbook), split/
    unlink ⇒ 0, mirror ⇒ 1 (|μ̄| is reflection-invariant). The pre-registered
    magnitude predictions are the falsifiable core.
  • The TWO INDEPENDENT SIGNS are exposed and shown independent:
      sign(μ̄)  — geometric Borromean handedness; flips under a SPATIAL MIRROR;
      sign(φ)  — octonion-orientation of the winding assignment; flips under
                 CYCLIC (QR↔QNR) REASSIGNMENT of the windings.
  • The PHYSICAL sign-map (which physical chirality ↔ which computed sign) is an
    explicit FRAMEWORK PRE-COMMIT slot (§2.75/§2.76), NOT read off.

CAUGHT-NOT-HIDDEN. A first attempt took sign(μ̄) = sign det[surface normals];
that is a triple product of PSEUDOvectors and is **reflection-EVEN** — it failed
the built-in mirror control (did not flip). The chiral sign(μ̄) is instead the
configuration's POLAR-vector handedness pseudoscalar (flips under mirror), used
below. The normals still correctly certify the triple point is transverse
(|μ̄|, reflection-invariant). The fully rigorous chiral sign is the open
third-order-helicity INTEGRAL — the remaining independent cross-check, NOT faked.

HONEST SCOPE. Whether a FIELD (Faddeev–Hopf) soliton realizes a Borromean
three-strand at all is the deferred hard step (the real G2-knot), separate from
this topological gate.

Requires numpy. Author: §3.4-G2-Milnor, 2026-06-03 (v2, mirror-control-corrected).
"""

import math
import numpy as np

PHI = (1 + math.sqrt(5)) / 2


def build_phi():
    phi = np.zeros((7, 7, 7))
    lines = [((i) % 7, (i + 1) % 7, (i + 3) % 7) for i in range(7)]
    perms = [((0, 1, 2), +1), ((1, 2, 0), +1), ((2, 0, 1), +1),
             ((0, 2, 1), -1), ((2, 1, 0), -1), ((1, 0, 2), -1)]
    for ln in lines:
        for o, s in perms:
            phi[ln[o[0]], ln[o[1]], ln[o[2]]] = s
    return phi, [tuple(sorted(l)) for l in lines]


class Disk:
    """Flat elliptical Seifert disk in the plane {axis = val}, oriented by ∂D."""
    def __init__(self, axis, val, semis, center=(0., 0., 0.), n=720):
        self.axis, self.val, self.semis = axis, val, semis
        self.center = np.array(center, float)
        others = [a for a in range(3) if a != axis]
        t = np.linspace(0, 2 * np.pi, n, endpoint=False)
        pts = np.tile(self.center, (n, 1))
        pts[:, axis] = val
        pts[:, others[0]] = self.center[others[0]] + semis[others[0]] * np.cos(t)
        pts[:, others[1]] = self.center[others[1]] + semis[others[1]] * np.sin(t)
        self.pts = pts
        self._set_normal()

    def _set_normal(self):
        dr = np.gradient(self.pts, axis=0)
        area = np.sum(np.cross(self.pts - self.center, dr), axis=0)
        self.normal = area / np.linalg.norm(area)

    def mirror_z(self):
        self.pts[:, 2] *= -1
        self.center[2] *= -1
        self.val = -self.val if self.axis == 2 else self.val
        self._set_normal()

    def contains(self, p):
        if abs(p[self.axis] - self.val) > 1e-9:
            return False
        return sum(((p[a] - self.center[a]) / se) ** 2
                   for a, se in self.semis.items()) <= 1.0 + 1e-9

    def sample(self):                       # a generic, non-axis-aligned boundary point
        return self.pts[len(self.pts) // 5]   # t = 2π/5


def borromean_disks(a=PHI, b=1 / PHI, sep=0.0, mirror=False):
    """Three perpendicular golden ellipses (standard Borromean). sep>0 splits
    loop 3 away (unlink control); mirror=True applies the spatial mirror z→−z."""
    disks = [Disk(2, 0.0, {0: a, 1: b}),                       # E1 in z=0
             Disk(0, 0.0, {1: a, 2: b}),                       # E2 in x=0
             Disk(1, sep, {0: b, 2: a}, center=(0., sep, 0.))]  # E3 in y=sep
    if mirror:
        for D in disks:
            D.mirror_z()
    return disks


def milnor_magnitude(disks):
    """|μ̄(123)| = number of transverse triple points of the three disks. The
    three disks each fix one coordinate; the candidate triple point has those
    three coordinates; it counts iff it lies in all three disks and the normals
    are linearly independent (transverse). Reflection-INVARIANT, as |μ̄| must be."""
    if sorted(D.axis for D in disks) != [0, 1, 2]:
        return 0
    p = np.zeros(3)
    for D in disks:
        p[D.axis] = D.val
    if not all(D.contains(p) for D in disks):
        return 0
    transverse = abs(np.linalg.det(np.stack([D.normal for D in disks]))) > 1e-6
    return 1 if transverse else 0


def handedness(disks):
    """Chiral sign of the configuration: det of one generic POLAR sample per loop
    (reflection-ODD ⇒ flips under mirror). This is sign(μ̄) up to a global
    convention; |·| is not meaningful, only its sign and its mirror behaviour."""
    return float(np.linalg.det(np.stack([D.sample() for D in disks])))


def main():
    phi, lines = build_phi()
    print("=" * 78)
    print("§3.4-G2-Milnor — φ-weighted Milnor triple-linking μ̄^φ on the baryon")
    print("=" * 78)

    # ── MAGNITUDE: validate on controls ──────────────────────────────────────
    mag = milnor_magnitude(borromean_disks())
    mag_mir = milnor_magnitude(borromean_disks(mirror=True))
    mag_split = milnor_magnitude(borromean_disks(sep=6.0))
    print("  MAGNITUDE |μ̄(123)| = #transverse triple points of the Seifert disks")
    print(f"    Borromean              : |μ̄| = {mag}   (textbook |μ̄| = 1 "
          f"{'✓' if mag == 1 else '✗'})")
    print(f"    split / unlink (sep=6) : |μ̄| = {mag_split}   "
          f"⇒ {'0 ✓ (CONTROL: non-Borromean)' if mag_split == 0 else '✗'}")
    print(f"    spatial mirror         : |μ̄| = {mag_mir}   "
          f"⇒ {'1 ✓ (|μ̄| reflection-invariant)' if mag_mir == 1 else '✗'}")
    print()

    # ── SIGN: chiral, from the polar handedness (mirror control) ─────────────
    h = handedness(borromean_disks())
    h_mir = handedness(borromean_disks(mirror=True))
    sgn = int(np.sign(h))
    print("  SIGN(μ̄) — chiral handedness (polar pseudoscalar; flips under mirror)")
    print(f"    config = {h:+.3f}  →  mirror = {h_mir:+.3f}   "
          f"⇒ flips {'✓ (CONTROL: chirality)' if h * h_mir < 0 else '✗'}")
    print("    [the earlier sign det[normals] was reflection-EVEN — pseudovector")
    print("     triple product — and FAILED this control; replaced. The fully")
    print("     rigorous chiral sign is the open 3rd-order-helicity INTEGRAL.]")
    print()

    # ── φ-selection + the two independent signs ──────────────────────────────
    line = (0, 1, 3)        # a QR Fano line  (winding directions d₁,d₂,d₃)
    nonline = (0, 1, 2)     # NOT a line
    line_qnr = (0, 3, 1)    # same line, anti-cyclic = QR↔QNR conjugate order
    print("  TWO INDEPENDENT SIGNS (the Eddington-exposed structure):")
    print(f"    sign(φ): line {line}→{int(phi[line]):+d}, "
          f"QNR-conjugate {line_qnr}→{int(phi[line_qnr]):+d}  ⇒ flips under "
          f"winding reassignment {'✓' if phi[line_qnr] == -phi[line] else '✗'}")
    print(f"    sign(μ̄): config→{sgn:+d}, mirror→{int(np.sign(h_mir)):+d}  "
          f"⇒ flips under spatial mirror "
          f"{'✓' if np.sign(h_mir) == -sgn else '✗'}")
    print("    the two flip under INDEPENDENT operations — all 4 combinations:")
    print(f"      {'windings':<10}{'space':<9}μ̄^φ = sign(φ)·|μ̄|·sign(μ̄)")
    for wname, wtri, sname, ssgn in [("line", line, "config", sgn),
                                     ("line", line, "mirror", -sgn),
                                     ("QNR", line_qnr, "config", sgn),
                                     ("QNR", line_qnr, "mirror", -sgn)]:
        mphi = int(phi[wtri]) * mag * ssgn
        print(f"      {wname:<10}{sname:<9}μ̄^φ = {int(phi[wtri]):+d}·{mag}·{ssgn:+d} "
              f"= {mphi:+d}")
    print()

    # ── pre-registered magnitude predictions (committed before running) ──────
    print("  PRE-REGISTERED |μ̄^φ| (committed):")
    cases = [("Fano line + Borromean", abs(int(phi[line])) * mag, 1),
             ("non-line  + Borromean", abs(int(phi[nonline])) * mag, 0),
             ("Fano line + split (non-Borromean)", abs(int(phi[line])) * mag_split, 0)]
    allok = all(v == pred for _, v, pred in cases)
    for nm, v, pred in cases:
        print(f"    {nm:<36}: |μ̄^φ| = {v}  (predicted {pred}) "
              f"{'✓' if v == pred else '✗'}")
    print()

    print("=" * 78)
    print("G2-MILNOR VERDICT")
    print("=" * 78)
    print(f"""\
  MAGNITUDE (R1, validated on controls — {'ALL ✓' if allok else 'MISMATCH ✗'}): |μ̄^φ| = 1 on a
  Fano-line genuine Borromean, 0 off-line, 0 on a non-Borromean link. The
  baryon's cubic triple invariant is nonzero precisely when the windings form a
  Fano line AND the strands are genuinely Borromean — the pre-registered
  prediction holds.

  SIGN STRUCTURE (R1 for independence; chiral sign = polar handedness, mirror-
  validated): μ̄^φ = sign(φ)·|μ̄|·sign(μ̄) carries TWO independent ±1 signs that
  flip under TWO independent operations — sign(μ̄) under a spatial mirror,
  sign(φ) under QR↔QNR winding reassignment (all four combinations realized).

  PHYSICAL SIGN-MAP — *framework pre-commit required; NOT asserted here.*
     ┌─ sign(μ̄)  [flips under spatial mirror]        ↔  ???
     └─ sign(φ)   [flips under QR↔QNR reassignment]    ↔  ???
  Whether spatial parity and the QR/QNR algebraic chirality (§2.75/§2.76) are
  DISTINCT (one in each sign) or COINCIDE is the registrable prediction; this
  computation supplies the two independent signs but does NOT decide the map.

  OPEN (honest): (1) the independent 3rd-order-helicity INTEGRAL cross-check —
  the rigorous chiral sign(μ̄) and a second magnitude method (not faked);
  (2) the field-soliton realization of a Borromean three-strand (the real
  G2-knot). Brute-force soliton relaxation stays held.

  Eddington note: the reflection-EVEN det[normals] sign was caught by the mirror
  control and replaced — the control discipline working as intended.""")
    print()
    print("  Cross-refs: §3.4-G2-Borromean (setup), §3.4-G2-orient (meson sector),")
    print("  §2.15 (Borromean baryon), §2.75/§2.76 (QR/QNR), §3.4-G0 (arity ladder).")


if __name__ == "__main__":
    main()
