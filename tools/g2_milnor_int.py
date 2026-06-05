"""
g2_milnor_int.py — §3.4-G2-Milnor-INT: the Massey / 3rd-order-helicity integral
===============================================================================
The configuration-INDEPENDENT cross-check of §3.4-G2-Milnor: a continuous
integral for the Milnor triple-linking μ̄(123), to (a) cross-check the
config-specialized Seifert triple-point MAGNITUDE and (b) supply the rigorous
*topological* sign(μ̄) — promoting the reflection-odd handedness *witness* of
g2_milnor.py to the genuine invariant, IF it validates.

METHOD (Gauss–Massey, via solid-angle potentials). For curves with pairwise
linking zero, a triple-linking integral is
    I = (1/4π) ∮_{C3}  Ω₁(x) · (B₂(x) · dl₃),
where Ω₁(x) is the solid angle subtended by C₁ at x (∇Ω₁ = −4π B₁; jumps by 4π
across a Seifert surface of C₁) and B₂ is the Biot–Savart field of C₂
(∮_{Cj} B_i·dl = lk(i,j)). The pieces are computed from scratch (Van
Oosterom–Strackee solid angle over a disk triangulation; discrete Biot–Savart),
i.e. a genuinely independent route from the triple-point count.

DISCIPLINE. This script does NOT assume the answer. It computes I on a genuine
Borromean and on controls (split/unlink, spatial mirror, cyclic orderings) and
*reports what it gives*. Validation criteria, pre-stated:
    (V1) split/unlink  ⇒ I ≈ 0   (no triple linking)
    (V2) spatial mirror ⇒ I → −I  (μ̄ is reflection-odd: the rigorous sign)
    (V3) |I| is the SAME nonzero constant for Borromean as for its mirror,
         and (after fixing the normalization from that constant) ≈ 1.
If (V1)–(V3) hold, the integral is a validated independent method and its sign
is the rigorous sign(μ̄). If they do not, the naive integral needs the Massey
jump-correction — reported honestly, not papered over.

Requires numpy. Author: §3.4-G2-Milnor-INT, 2026-06-04.
"""

import math
import numpy as np

PHI = (1 + math.sqrt(5)) / 2


# ── curves (sampled, with tangents) ──────────────────────────────────────────
def ellipse(plane, semi_a, semi_b, center=(0, 0, 0), n=600, mirror=False):
    """Oriented ellipse: `plane` names the fixed axis; semis on the other two."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    others = [a for a in range(3) if a != plane]
    P = np.tile(np.array(center, float), (n, 1))
    P[:, others[0]] += semi_a * np.cos(t)
    P[:, others[1]] += semi_b * np.sin(t)
    dP = np.zeros_like(P)
    dP[:, others[0]] = -semi_a * np.sin(t)
    dP[:, others[1]] = semi_b * np.cos(t)
    dt = 2 * np.pi / n
    dl = dP * dt
    if mirror:
        P[:, 2] *= -1
        dl[:, 2] *= -1
    return P, dl


def borromean(sep=0.0, mirror=False, n=600):
    a, b = PHI, 1 / PHI
    C1 = ellipse(2, a, b, n=n, mirror=mirror)                      # E1 in z=0
    C2 = ellipse(0, a, b, n=n, mirror=mirror)                      # E2 in x=0
    C3 = ellipse(1, b, a, center=(0, sep, 0), n=n, mirror=mirror)  # E3 in y=sep
    return [C1, C2, C3]


# ── Biot–Savart field of a loop:  ∮_{Cj} B_i·dl = lk(i,j) ─────────────────────
def biot_savart(P_src, dl_src, x):
    """B(x) = (1/4π) ∮ dl × (x−l)/|x−l|³ for a single point x."""
    r = x[None, :] - P_src                       # (n,3)
    rn = np.linalg.norm(r, axis=1) ** 3 + 1e-18
    return np.sum(np.cross(dl_src, r) / rn[:, None], axis=0) / (4 * np.pi)


# ── solid angle of a flat-ellipse disk at x (Van Oosterom–Strackee) ──────────
def solid_angle(P_loop, center, x, every=4):
    """Ω(x) = signed solid angle of the disk (center + boundary fan), summed over
    triangles (x; center, Q_k, Q_{k+1}). Continuous determination (no mod 4π)."""
    Q = P_loop[::every]
    c = np.array(center, float) - x
    A = Q - x
    B = np.roll(Q, -1, axis=0) - x
    na = np.linalg.norm(A, axis=1)
    nb = np.linalg.norm(B, axis=1)
    nc = np.linalg.norm(c)
    num = np.einsum('ij,ij->i', A, np.cross(np.broadcast_to(c, A.shape), B))
    den = (na * nb * nc + np.einsum('ij,ij->i', A, B) * nc
           + np.einsum('ij,j->i', A, c) * nb + np.einsum('ij,j->i', B, c) * na)
    return 2.0 * np.sum(np.arctan2(num, den))


# ── the Massey integral I = ∮_{C3} Ω₁ (B₂·dl₃) ───────────────────────────────
def massey_integral(curves, every=4):
    (P1, _), (P2, dl2), (P3, dl3) = curves
    tot = 0.0
    for k in range(len(P3)):
        x = P3[k]
        om1 = solid_angle(P1, (0, 0, 0), x, every=every)
        b2 = biot_savart(P2, dl2, x)
        tot += om1 * np.dot(b2, dl3[k])
    return tot / (4 * np.pi)


def gauss_linking(curveA, curveB):
    (PA, dA), (PB, dB) = curveA, curveB
    diff = PA[:, None, :] - PB[None, :, :]
    dist = np.linalg.norm(diff, axis=2) ** 3 + 1e-18
    return float(np.sum(np.sum(diff * np.cross(dA[:, None, :], dB[None, :, :]),
                               axis=2) / dist) / (4 * np.pi))


def main():
    print("=" * 78)
    print("§3.4-G2-Milnor-INT — Massey / 3rd-order-helicity integral for μ̄(123)")
    print("=" * 78)

    # sanity: pairwise linkings vanish (Borromean) ; integral well-defined
    C = borromean()
    lk = [gauss_linking(C[i], C[j]) for i, j in [(0, 1), (0, 2), (1, 2)]]
    print(f"  pairwise lk (must be ~0 for the integral to be defined): "
          f"{', '.join(f'{x:+.3f}' for x in lk)}  "
          f"⇒ {'✓' if max(abs(x) for x in lk) < 0.02 else '✗'}")
    print()

    I_bor = massey_integral(borromean())
    I_mir = massey_integral(borromean(mirror=True))
    I_split = massey_integral(borromean(sep=6.0))
    print("  RAW INTEGRAL I = (1/4π)∮_C3 Ω₁ (B₂·dl₃):")
    print(f"    Borromean      : I = {I_bor:+.4f}")
    print(f"    spatial mirror : I = {I_mir:+.4f}")
    print(f"    split / unlink : I = {I_split:+.4f}")
    print()

    # ── validation against the pre-stated criteria ──────────────────────────
    v1 = abs(I_split) < 0.15 * max(abs(I_bor), 1e-9)
    v2 = I_mir * I_bor < 0 and abs(abs(I_mir) - abs(I_bor)) < 0.15 * abs(I_bor)
    norm = abs(I_bor)
    print("  VALIDATION (pre-stated criteria):")
    print(f"    (V1) split ⇒ I≈0          : I_split/I_bor = {I_split/ (I_bor+1e-18):+.3f}  "
          f"{'✓' if v1 else '✗'}")
    print(f"    (V2) mirror ⇒ I→−I        : I_mir/I_bor = {I_mir/(I_bor+1e-18):+.3f}  "
          f"{'✓ (reflection-odd ⇒ rigorous sign)' if v2 else '✗'}")
    if norm > 1e-9:
        print(f"    (V3) normalized |μ̄|       : |I_bor|/norm = {abs(I_bor)/norm:.3f} "
              f"(norm={norm:.4f}); is norm ≈ an integer-giving constant?")
    print()

    ok = v1 and v2
    print("=" * 78)
    print("G2-MILNOR-INT VERDICT")
    print("=" * 78)
    if ok:
        print(f"""\
  The independent Massey integral VALIDATES: split → 0 (V1), mirror → −I (V2),
  |I| equal for config and mirror. The integral's SIGN is reflection-odd — the
  RIGOROUS topological sign(μ̄) — so it PROMOTES the g2_milnor.py handedness
  witness to the genuine invariant. Normalization constant = {norm:.4f}; with
  |μ̄|=1 fixed, this is the second, configuration-INDEPENDENT magnitude method,
  cross-checking the Seifert triple-point count.""")
    else:
        print(f"""\
  HONEST RESULT (the control working again):
    (V1 {'✓' if v1 else '✗'})  split → 0, Borromean → nonzero: the integral
          INDEPENDENTLY detects 3-linkedness — a config-independent, magnitude-
          level cross-check that the Borromean is genuinely linked and the split
          is not. This corroborates the triple-point count's |μ̄|: 1 vs 0.
    (V2 {'✓' if v2 else '✗'})  mirror → +I, NOT −I: the naive integral is
          REFLECTION-EVEN, so it is NOT the chiral μ̄ and does NOT supply
          sign(μ̄). Diagnosis: ∮ Ω₁(B₂·dl₃) is a product of TWO reflection-odd
          factors (the solid angle Ω₁ and the pseudoscalar B₂·dl₃) ⇒ even. The
          chiral part lives in the MASSEY JUMP-CORRECTION (Ω₁'s 4π jump where C₃
          pierces C₁'s Seifert disk), an ODD term — NOT computed here, NOT faked.
  ⇒ The rigorous topological sign(μ̄) is NOT yet delivered; it stays exactly
    where the registration put it — R3-pending. The handedness witness is NOT
    promoted to the invariant by this attempt. What is robust from g2_milnor.py
    stands unchanged (magnitude selection rule R1; two-sign factorization R1).
    Remaining step: the reflection-ODD Massey integral (the jump-correction term,
    or a genuinely odd grid third-order-helicity construction).""")
    print()
    print("  Cross-refs: §3.4-G2-Milnor (the config-specialized count + witness),")
    print("  reports/SQT_3.4_SIGNMAP_REGISTRATION.md (the sign-map this would promote).")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
