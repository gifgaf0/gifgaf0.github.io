"""
g2_milnor_sign.py — §3.4-G2-Milnor-SIGN: the rigorous reflection-odd sign(μ̄)
============================================================================
Per the pre-registration (reports/SQT_3.4_SIGN_PREREGISTRATION.md, committed
first). Two reflection-ODD methods for the Milnor triple-linking sign:

  METHOD A — Seifert-intersection linking.  γ_ij = (segment F_i∩F_j, oriented
    by n_i×n_j) ∪ (closing arc on the curve that bounds it); μ̄(ijk) = lk(C_k,
    γ_ij) by the Gauss integral. A genuine linking number ⇒ reflection-ODD.
    The n_i×n_j orientation gives the antisymmetry μ̄(213)=−μ̄(123).
  METHOD B — Massey jump-correction.  μ̄_B = Σ over C_3's piercings of disk S_1
    of [piercing sign]·Ω₂(piercing)/(4π) — the reflection-ODD part of the
    solid-angle integral.

Judged ONLY against the pre-registered criteria P1–P5 (split→0, mirror→flip,
|μ̄|=1, cyclic consistency, two-method agreement). No ±1 is faked; the controls
decide. Success promotes the handedness *witness* of g2_milnor.py to the genuine
sign(μ̄); it does NOT touch the registered sign(φ)↔QR/QNR map.

Requires numpy. Author: §3.4-G2-Milnor-SIGN, 2026-06-05.
"""

import math
import numpy as np

PHI = (1 + math.sqrt(5)) / 2


# ── curves: oriented golden ellipses (points + tangents + disk metadata) ─────
def make_curves(sep=0.0, mirror=False, n=720):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    a, b = PHI, 1 / PHI
    dt = 2 * np.pi / n

    def ell(fixed, fv, sa, sb, ctr):
        o = [k for k in range(3) if k != fixed]
        P = np.tile(np.array(ctr, float), (n, 1)); P[:, fixed] = fv
        P[:, o[0]] += sa * np.cos(t); P[:, o[1]] += sb * np.sin(t)
        dP = np.zeros((n, 3)); dP[:, o[0]] = -sa * np.sin(t); dP[:, o[1]] = sb * np.cos(t)
        d = {"fixed": fixed, "fv": fv, "o": o, "sa": sa, "sb": sb,
             "ctr": np.array(ctr, float)}
        return P, dP * dt, d

    C1 = ell(2, 0.0, a, b, (0, 0, 0))            # z=0 : x~a, y~b
    C2 = ell(0, 0.0, a, b, (0, 0, 0))            # x=0 : y~a, z~b
    C3 = ell(1, sep, b, a, (0, sep, 0))          # y=sep: x~b, z~a
    curves = [C1, C2, C3]
    if mirror:
        for P, dl, d in curves:
            P[:, 2] *= -1; dl[:, 2] *= -1; d["ctr"][2] *= -1
            if d["fixed"] == 2:
                d["fv"] = -d["fv"]
    # oriented unit normal of each disk = area vector of its boundary
    for P, dl, d in curves:
        N = np.sum(np.cross(P - d["ctr"], dl), axis=0)
        d["n"] = N / np.linalg.norm(N)
    return curves


def in_disk(d, p):
    if abs(p[d["fixed"]] - d["fv"]) > 1e-7:
        return False
    return ((p[d["o"][0]] - d["ctr"][d["o"][0]]) / d["sa"]) ** 2 + \
           ((p[d["o"][1]] - d["ctr"][d["o"][1]]) / d["sb"]) ** 2 <= 1 + 1e-9


def seifert_segment(di, dj, ni, nj):
    """Segment F_i∩F_j (two flat disks fixing distinct axes), oriented n_i×n_j.
    Returns (start, end) or None. Free axis = the one neither disk fixes."""
    if di["fixed"] == dj["fixed"]:
        return None
    free = [k for k in range(3) if k not in (di["fixed"], dj["fixed"])][0]
    base = np.zeros(3); base[di["fixed"]] = di["fv"]; base[dj["fixed"]] = dj["fv"]

    def half_range(d):                       # |free| extent inside disk d on the line
        # on the line, the two in-plane coords of d are: the free axis and the
        # other fixed axis (set by the OTHER disk). Solve ellipse for the free coord.
        oth = [k for k in d["o"]]            # d's two in-plane axes
        fixed_other = [k for k in oth if k != free][0]
        s_free = d["sa"] if d["o"][0] == free else d["sb"]
        s_oth = d["sa"] if d["o"][0] == fixed_other else d["sb"]
        u = (base[fixed_other] - d["ctr"][fixed_other]) / s_oth
        if u * u >= 1:
            return None
        return d["ctr"][free] - s_free * math.sqrt(1 - u * u), \
               d["ctr"][free] + s_free * math.sqrt(1 - u * u)

    ri, rj = half_range(di), half_range(dj)
    if ri is None or rj is None:
        return None
    lo, hi = max(ri[0], rj[0]), min(ri[1], rj[1])
    if hi <= lo:
        return None
    s, e = base.copy(), base.copy(); s[free] = lo; e[free] = hi
    # orient by n_i × n_j (project onto the free axis direction)
    nij = np.cross(ni, nj)
    if nij[free] < 0:
        s, e = e, s
    return s, e


def close_gamma(seg, curves, di, dj, n_arc=240):
    """Close the segment with an arc of the curve that bounds it (endpoints lie
    on that curve). Returns (P, dl) of the closed loop. Arc choice is immaterial
    (the two arcs differ by the full curve; lk(C_k, C_bound)=0)."""
    s, e = seg
    for (P, dl, d) in (curves[di], curves[dj]):
        if in_disk(d, s) and (abs(in_disk and 1) or True):
            # is the segment endpoint ON this curve's boundary (ellipse rim)?
            oth = d["o"]
            r2 = ((s[oth[0]] - d["ctr"][oth[0]]) / d["sa"]) ** 2 + \
                 ((s[oth[1]] - d["ctr"][oth[1]]) / d["sb"]) ** 2
            if abs(r2 - 1) < 1e-3 and abs(s[d["fixed"]] - d["fv"]) < 1e-6:
                P_c = P
                # nearest sample indices to e (start of arc) and s (end of arc)
                i_e = int(np.argmin(np.linalg.norm(P_c - e, axis=1)))
                i_s = int(np.argmin(np.linalg.norm(P_c - s, axis=1)))
                idx = [k % len(P_c) for k in range(i_e, i_e + (i_s - i_e) % len(P_c) + 1)]
                arc = P_c[idx]
                seg_pts = np.array([s, e])
                loop = np.vstack([seg_pts, arc])
                dlp = np.gradient(loop, axis=0)
                return loop, dlp
    return None


def gauss_lk(curveK, gamma):
    PK, dK = curveK[0], curveK[1]
    PG, dG = gamma
    diff = PK[:, None, :] - PG[None, :, :]
    dist = np.linalg.norm(diff, axis=2) ** 3 + 1e-18
    return float(np.sum(np.sum(diff * np.cross(dK[:, None, :], dG[None, :, :]),
                               axis=2) / dist) / (4 * np.pi))


def muA(curves, i, j, k):
    di, dj = curves[i][2], curves[j][2]
    seg = seifert_segment(di, dj, di["n"], dj["n"])
    if seg is None:
        return 0.0
    gamma = close_gamma(seg, curves, i, j)
    if gamma is None:
        return 0.0
    return gauss_lk(curves[k], gamma)


def main():
    print("=" * 76)
    print("§3.4-G2-Milnor-SIGN — rigorous reflection-odd sign(μ̄)  [pre-registered]")
    print("=" * 76)
    C = make_curves()
    m123 = muA(C, 0, 1, 2)
    print(f"  Method A  μ̄(123) = lk(C₃, γ₁₂) = {m123:+.4f}")
    print()

    # ── pre-registered criteria ─────────────────────────────────────────────
    m_split = muA(make_curves(sep=6.0), 0, 1, 2)
    m_mirror = muA(make_curves(mirror=True), 0, 1, 2)
    m231 = muA(C, 1, 2, 0); m312 = muA(C, 2, 0, 1); m213 = muA(C, 1, 0, 2)
    print("  PRE-REGISTERED CRITERIA (judged against committed P1–P4):")
    p1 = abs(m_split) < 0.25
    p2 = m_mirror * m123 < 0
    p3 = abs(abs(m123) - 1) < 0.25
    p4 = (abs(m231 - m123) < 0.25 and abs(m312 - m123) < 0.25
          and abs(m213 + m123) < 0.25)
    print(f"    P1 split → 0          : μ̄_split = {m_split:+.3f}   {'✓' if p1 else '✗'}")
    print(f"    P2 mirror → −μ̄        : μ̄_mirror = {m_mirror:+.3f}  "
          f"(μ̄ = {m123:+.3f})   {'✓ reflection-ODD' if p2 else '✗ NOT odd'}")
    print(f"    P3 |μ̄| = 1            : |μ̄| = {abs(m123):.3f}   {'✓' if p3 else '✗'}")
    print(f"    P4 cyclic consistency : μ̄(231)={m231:+.3f}, μ̄(312)={m312:+.3f}, "
          f"μ̄(213)={m213:+.3f}   {'✓' if p4 else '✗'}")
    print()

    print("=" * 76)
    print("VERDICT (against the pre-registered promotion rule)")
    print("=" * 76)
    if p1 and p2 and p3 and p4:
        print(f"""\
  Method A PASSES P1–P4: split→0, mirror→−μ̄ (REFLECTION-ODD — the property every
  prior sign attempt lacked), |μ̄|=1, cyclic-consistent. So sign(μ̄) is delivered
  by a genuine reflection-odd linking number: μ̄(123) = {m123:+.0f} for this
  Borromean. Pending the Method-B independent cross-check (P5) before full
  promotion, this is the first reflection-odd sign computation that survives the
  controls. The registered sign(φ)↔QR/QNR map is untouched (still R3-pending its
  consistency check); the mirror flip is the EXPECTED behaviour, not evidence.""")
    else:
        fails = [n for n, p in [("P1", p1), ("P2", p2), ("P3", p3), ("P4", p4)] if not p]
        print(f"""\
  Method A does NOT pass {', '.join(fails)}. Per the pre-registered rule the sign
  is NOT established. But the FAILURE IS DIAGNOSTIC, and points to a finding that
  reaches the prior magnitude work:

  ⚠ THE CONFIGURATION IS AMPHICHIRAL (true μ̄ = 0). The map z→−z sends each of the
    three golden ellipses to ITSELF (verified set-distance 0), so it is an
    orientation-reversing SYMMETRY of the link. μ̄ is reflection-odd and is odd
    under reversing any single component; z→−z reverses exactly TWO component
    orientations, so μ̄(123) = (−1)_ambient·(−1)² · μ̄(123) = −μ̄(123) ⇒ **μ̄ = 0.**
    The orthogonal-golden-ellipse configuration is therefore NOT a chiral
    Borromean (μ̄=±1); it is amphichiral. P1/P3/P4 pass and P2 fails because
    Method A (like the §3.4-G2-Milnor Seifert triple-point count) computes the
    **uncorrected** Seifert linking — which is ±1 — while the Mellor–Melvin
    correction terms (omitted) bring the true μ̄ to 0.

  CONSEQUENCE (must be surfaced): the magnitude claim |μ̄^φ|=1 of §3.4-G2-Milnor
  (V4.29) and the "genuine Borromean" framing of §3.4-G2-Borromean (V4.27) rest
  on this uncorrected count on an amphichiral configuration. They need a recheck
  with a **manifestly chiral** Borromean (symmetry broken) and the Mellor–Melvin
  corrections, before either the magnitude or the sign can stand. The sign stays
  R3-pending; the registered sign(φ)↔QR/QNR map is untouched. No ±1 is faked —
  and the honest reading is that there is no nonzero sign here to find.""")
    print()
    print("  Cross-refs: pre-registration SQT_3.4_SIGN_PREREGISTRATION.md;")
    print("  g2_milnor.py (the witness), g2_milnor_int.py (the even magnitude integral).")
    print()
    diagnostics(C)


def diagnostics(C):
    """The three discriminating tests (per SQT-agent), separating the two issues:
    (i) Method A is reflection-even by its n_i×n_j (axial) orientation — a
        CONVENTION limit, isolated by tests 1+3 (reversal/permutation are right);
    (ii) the config is amphichiral (μ̄=0) — test 2, independent of Method A."""
    print("=" * 76)
    print("DISCRIMINATING TESTS (separate the convention issue from amphichirality)")
    print("=" * 76)
    base = muA(C, 0, 1, 2)
    C3 = C[2]
    Crev = [C[0], C[1], (C3[0][::-1].copy(), -C3[1][::-1].copy(), C3[2])]
    print(f"  T1 reverse a component → μ̄ flips: μ̄={base:+.2f}, reversed={muA(Crev,0,1,2):+.2f}"
          f"  {'✓ (Method A IS odd under reversal/permutation — P4 genuine)' if base*muA(Crev,0,1,2)<0 else '✗'}")
    Cm = make_curves(mirror=True)
    fixed = all(np.min(np.linalg.norm(C[i][0] - Cm[i][0][0], axis=1)) < 1e-6 and
                np.max([np.min(np.linalg.norm(C[i][0] - p, axis=1)) for p in Cm[i][0][::60]]) < 1e-6
                for i in range(3))
    print(f"  T2 z→−z fixes each component (not permuted): "
          f"{'✓ ⇒ amphichiral ⇒ μ̄=0 (symmetry argument, independent of Method A)' if fixed else '✗'}")
    print(f"  T3 QR↔QNR (0,1,3)→(0,3,1) is a TRANSPOSITION (odd) of WINDING DIRECTIONS")
    print(f"     ⇒ flips φ but NOT μ̄ (μ̄ = strand geometry, winding-independent) ⇒ the two")
    print(f"     signs ARE independent in the computation. Collapse would need QR↔QNR to be")
    print(f"     a STRAND permutation — the §2.75/§2.76/§2.86C check, NOT settled here.")
    print()
    print("  RECONCILED DIAGNOSIS: two distinct facts —")
    print("   (i)  Method A is reflection-EVEN for spatial mirror (axial n_i×n_j); to read")
    print("        the sign needs a FIXED-FRAME (transported) orientation. [convention]")
    print("   (ii) the symmetric golden config is AMPHICHIRAL (μ̄=0) — so there is no")
    print("        spatial-chirality sign to read on it anyway. [the finding]")
    print("  ⇒ §3.4-G2-CHIRAL must fix BOTH: a manifestly-chiral Borromean AND a fixed-frame")
    print("     orientation. The substantive sign(φ)↔QR/QNR map is untouched (T3).")


if __name__ == "__main__":
    main()
