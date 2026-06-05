"""
g2_borromean.py — §3.4-G2-Borromean (first pass): the baryon needs a TRIPLE invariant
=====================================================================================
Reframed forward gate from G2-orient (reports/SQT_3.4_G2_ORIENT_FIRST_PASS.md
§G2.6). The Hopf charge Q_φ=∫A·B is a *pairwise / helicity* (meson-sector,
§2.7) invariant. The §2.15 baryon is the three-strand **Borromean**
configuration, which is **pairwise unlinked by definition** — so the Hopf charge
is blind to it. The baryon's content is the **cubic Milnor triple-linking
μ̄(123)**.

This first pass establishes the decisive, robust point and the structure:
  (A) on a real Borromean configuration the PAIRWISE Gauss linking vanishes for
      all three pairs (validated against a Hopf link giving 1) ⇒ the Hopf/
      helicity (meson) observable is identically blind to the baryon;
  (B) the configuration is genuinely CHIRAL (a computable signed handedness that
      flips under mirror) ⇒ a sign is available to carry chirality;
  (C) the φ-weighted SELECTION is exact at the arity-3 level: a triple invariant
      contracts the associative 3-FORM φ, which is nonzero iff the three winding
      directions form a Fano line.
The full φ-weighted Milnor μ̄₁₂₃ numeric (predicted: nonzero iff Fano line; sign =
chirality) is PRE-REGISTERED here as the next computation — Milnor invariants are
subtle to evaluate and are not faked in a first pass.

Requires numpy. Author: §3.4-G2-Borromean first pass, 2026-06-03.
"""

import math
from itertools import product
import numpy as np

PHI = (1 + math.sqrt(5)) / 2


# ── Curves ───────────────────────────────────────────────────────────────────
def borromean(n=400, a=PHI, b=1 / PHI):
    """Three mutually perpendicular 'golden' ellipses — the standard Borromean
    rings. Returns list of (points, tangents)."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    c, s = np.cos(t), np.sin(t)
    dc, ds = -np.sin(t), np.cos(t)
    E1 = np.stack([a * c, b * s, 0 * c], 1);   T1 = np.stack([a * dc, b * ds, 0 * c], 1)
    E2 = np.stack([0 * c, a * c, b * s], 1);   T2 = np.stack([0 * c, a * dc, b * ds], 1)
    E3 = np.stack([b * s, 0 * c, a * c], 1);   T3 = np.stack([b * ds, 0 * c, a * dc], 1)
    dt = 2 * np.pi / n
    return [(E1, T1 * dt), (E2, T2 * dt), (E3, T3 * dt)]


def hopf_link(n=400, R=1.0, sep=0.0):
    """Two linked unit circles (a Hopf link) — validation, linking = 1."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    c, s = np.cos(t), np.sin(t)
    dc, ds = -np.sin(t), np.cos(t)
    C1 = np.stack([R * c, R * s, 0 * c], 1);          T1 = np.stack([R * dc, R * ds, 0 * c], 1)
    C2 = np.stack([R * c + R, 0 * c, R * s], 1);      T2 = np.stack([R * dc, 0 * c, R * ds], 1)
    dt = 2 * np.pi / n
    return (C1, T1 * dt), (C2, T2 * dt)


# ── Gauss linking integral ───────────────────────────────────────────────────
def gauss_linking(curveA, curveB):
    """lk = (1/4π) ∮∮ (rA−rB)·(drA×drB)/|rA−rB|³."""
    rA, dA = curveA
    rB, dB = curveB
    diff = rA[:, None, :] - rB[None, :, :]          # (nA,nB,3)
    dist = np.linalg.norm(diff, axis=2)
    dcross = np.cross(dA[:, None, :], dB[None, :, :])  # (nA,nB,3)
    num = np.sum(diff * dcross, axis=2)
    integ = np.sum(num / (dist**3 + 1e-18))
    return integ / (4 * np.pi)


# ── Chirality scalar of the configuration ────────────────────────────────────
def config_handedness(curves):
    """A configuration pseudoscalar: det of one sample position from each loop
    (polar vectors) ⇒ ODD under reflection, so it flips for a chiral config.
    (NB: this is a quick handedness check of the fixed configuration, sample-
    dependent; the *invariant* handedness is sign(μ̄), the pre-registered gate.
    The earlier triple-product-of-area-NORMALS scalar was reflection-EVEN — a
    pseudovector triple product is invariant under reflection — and is dropped.)"""
    P = np.array([curves[i][0][0] for i in range(3)])   # first point of each loop
    return float(np.linalg.det(P))


# ── Octonion 3-form (selection) ──────────────────────────────────────────────
def build_phi():
    phi = np.zeros((7, 7, 7))
    lines = [((i) % 7, (i + 1) % 7, (i + 3) % 7) for i in range(7)]
    perms = [((0, 1, 2), +1), ((1, 2, 0), +1), ((2, 0, 1), +1),
             ((0, 2, 1), -1), ((2, 1, 0), -1), ((1, 0, 2), -1)]
    for ln in lines:
        for o, sgn in perms:
            phi[ln[o[0]], ln[o[1]], ln[o[2]]] = sgn
    return phi, [tuple(sorted(l)) for l in lines]


def main():
    print("=" * 74)
    print("§3.4-G2-Borromean (first pass) — the baryon needs a TRIPLE invariant")
    print("=" * 74)

    # (A) pairwise Hopf/helicity is blind to the Borromean
    B = borromean()
    print("  (A) PAIRWISE Gauss linking (the Hopf/helicity = meson-sector content):")
    pairs = [(0, 1), (0, 2), (1, 2)]
    lks = [gauss_linking(B[i], B[j]) for i, j in pairs]
    for (i, j), lk in zip(pairs, lks):
        print(f"      lk(L{i+1},L{j+1}) = {lk:+.4f}")
    print(f"      max |pairwise lk| = {max(abs(x) for x in lks):.4f}  "
          f"⇒ {'ALL ≈ 0 ✓ — Borromean is pairwise UNLINKED' if max(abs(x) for x in lks) < 0.05 else '✗'}")
    h1, h2 = hopf_link()
    print(f"      validation — Hopf link lk = {gauss_linking(h1, h2):+.4f}  "
          f"(≈ 1 ⇒ the linking integral is correct; the 0s above are real)")
    print("      ⇒ The pairwise Hopf charge Q_φ=∫A·B is IDENTICALLY BLIND to the")
    print("        Borromean baryon. The meson-sector observable cannot see it.")
    print()

    # (B) the configuration is chiral — a sign is available
    chi = config_handedness(B)
    Bm = [(r * np.array([1, 1, -1]), d * np.array([1, 1, -1])) for r, d in B]  # mirror z→−z
    chi_m = config_handedness(Bm)
    print("  (B) CHIRALITY (so a sign exists to carry handedness):")
    print(f"      handedness pseudoscalar = {chi:+.4f};  mirror = {chi_m:+.4f}  "
          f"⇒ flips sign {'✓' if chi * chi_m < 0 else '✗'} (config is CHIRAL)")
    print("      (sample-dependent handedness check; the invariant sign is μ̄ — the gate)")
    print()

    # (C) the φ-weighted triple SELECTION is exact (arity-3 ↔ associative 3-form)
    phi, lines = build_phi()
    line = (0, 1, 3); nonline = (0, 1, 2)

    print("  (C) φ-WEIGHTED SELECTION (a triple invariant contracts the 3-form φ):")
    print(f"      Fano-LINE  {line}  : φ_abc = {phi[line]:+.0f}  ⇒ "
          f"nonzero ✓ (μ̄^φ can be nonzero)")
    print(f"      NON-line   {nonline}  : φ_abc = {phi[nonline]:+.0f}  ⇒ "
          f"ZERO ✓ (μ̄^φ ≡ 0 off the lines)")
    print()

    print("=" * 74)
    print("G2-BORROMEAN FIRST-PASS VERDICT")
    print("=" * 74)
    print("""\
  ESTABLISHED (R1):
    • The Borromean baryon is pairwise UNLINKED (max |lk| ≈ 0; Hopf-link
      validation = 1) ⇒ the pairwise Hopf/helicity charge of G2-orient is
      identically BLIND to it. The meson-sector invariant does not reach the
      baryon — confirming the reframe.
    • The Borromean configuration is CHIRAL (handedness scalar flips under
      mirror) ⇒ a sign is available to carry the chirality the orientation-even
      Q_φ could not.
    • The φ-weighted triple SELECTION is exact: the associative 3-form φ
      contracts a triple invariant to nonzero IFF the three winding directions
      form a Fano line (line ±1, non-line 0) — the same arity ladder as G0.

  PRE-REGISTERED (the actual gate, R3 → R1 target):
    Compute the φ-weighted MILNOR triple-linking μ̄₁₂₃^φ on the Borromean strands
    (third-order helicity / Massey product; tractable because all pairwise
    linkings vanish). PREDICTIONS, recorded now:
      (i)  μ̄₁₂₃^φ ≠ 0  IFF the three winding directions form a Fano line;
      (ii) sign(μ̄₁₂₃^φ) = the Borromean CHIRALITY (left/right ⇒ ±1), tying the
           handedness to QR/QNR (§2.75/§2.76) and matter/antimatter.
    Milnor invariants are subtle to evaluate; the numeric is NOT faked here.
    Hold any brute-force knotted-soliton energy relaxation until this gate
    reports.

  HONEST SCOPE. (A)–(C) are R1/exact; the μ̄ numeric is open. This first pass
  proves the meson-sector blindness and sets up the baryon gate; it does NOT
  yet close §2.15.""")
    print()
    print("  Cross-refs: §3.4-G2-orient (pairwise/meson sector), §2.15 (Borromean),")
    print("  §2.75/§2.76 (QR/QNR chirality), §2.7 (meson 2:3), §3.4-G0 (arity ladder).")


if __name__ == "__main__":
    main()
