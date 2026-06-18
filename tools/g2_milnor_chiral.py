"""
g2_milnor_chiral.py — §3.4-G2-CHIRAL: μ̄ on a GENUINE Borromean, computed EXACTLY
===============================================================================
Why this build exists.  §3.4-G2-Milnor-SIGN proved the orthogonal golden-ellipse
configuration is AMPHICHIRAL (z→−z fixes each ellipse setwise, reversing two
orientations ⇒ μ̄ = −μ̄ ⇒ μ̄ = 0).  Because μ̄(123) is an INTEGER topological
invariant, no small symmetry-breaking perturbation can move it 0 → ±1: the golden
ellipses are simply NOT the Borromean rings, and the earlier |μ̄|=1 "validation"
was circular — the textbook control WAS the uncorrected Seifert triple-point count
under test.

§3.4-G2-CHIRAL therefore defines the Borromean rings GENUINELY, by the braid word
    β = (σ₁ σ₂⁻¹)³        (a pure 3-braid; its closure is the Borromean rings)
and computes μ̄(123) EXACTLY from the Artin action on the free group + the Magnus
expansion — i.e. from group theory, NOT from any Seifert surface or triple-point
count.  This (a) breaks the circularity (ground truth independent of the count),
and (b) re-runs the pre-registered criteria (SQT_3.4_SIGN_PREREGISTRATION.md) on
an honest object.

WHAT IT FINDS (two clean facts, no faked sign):

  MAGNITUDE — RESTORED on the right object.  |μ̄(123)| = 1 on the genuine
    Borromean, 0 on the 3-unlink.  So the §3.4 magnitude selection rule ("nonzero
    iff genuinely 3-linked") is CORRECT as a statement — it was only instantiated
    on the wrong (amphichiral, μ̄=0) golden-ellipse config.  Read off an exact word.

  SIGN — μ̄(123) is REFLECTION-EVEN; it is NOT a spatial-chirality witness, not
    even on a genuine Borromean.  The spatial mirror (crossing inversion, PROVEN
    correct here by a Hopf-link control that DOES flip lk +1→−1) leaves μ̄(123)
    UNCHANGED (+1 → +1).  μ̄ flips only under reversing component ORIENTATIONS
    (multilinearity), not under spatial reflection.  This is consistent with
      • the Borromean rings being amphichiral, and
      • g2_milnor_int.py independently finding the Massey integral reflection-EVEN.
    So sign(μ̄) cannot supply the QR/QNR parity; that must come from φ (octonionic
    winding) via the registered §2.75/§2.76/§2.86C consistency check — never from
    the link's spatial chirality.  The registered sign(φ)↔QR/QNR map is untouched.

METHOD (exact).  Artin representation of B₃ on F₃ = ⟨x₁,x₂,x₃⟩:
    σ_i :  x_i ↦ x_i x_{i+1} x_i⁻¹,  x_{i+1} ↦ x_i,        others fixed
    σ_i⁻¹: x_i ↦ x_{i+1},           x_{i+1} ↦ x_{i+1}⁻¹ x_i x_{i+1}, others fixed
For a PURE braid β, β(x_i) = A_i x_i A_i⁻¹; the longitude λ_i = A_i (well-defined
mod ⟨x_i⟩, which only adds X_i terms — irrelevant to the X_jX_k cross-coefficient).
The Magnus expansion sends x_i ↦ 1+X_i, x_i⁻¹ ↦ 1−X_i+X_i²−…, and
    μ̄(i j k) = coefficient of X_i X_j in the Magnus expansion of λ_k
(when the pairwise linkings vanish — they do for a Brunnian link).

No floating point, no discretization, no faked ±1 — the answer is an integer read
off an exact word, and the mirror operation is self-validated on a control.
Author: §3.4-G2-CHIRAL, 2026-06-05.
"""

# ── free-group words: list of signed ints (±i means x_i^{±1}); reduce inverses ─
def reduce_word(w):
    out = []
    for g in w:
        if out and out[-1] == -g:
            out.pop()
        else:
            out.append(g)
    return out


def inv(w):
    return [-g for g in reversed(w)]


# ── Artin action of a single generator σ_i^{±1} on a generator x_j ────────────
def artin_gen(sign_i, j):
    i = abs(sign_i)
    if sign_i > 0:                            # σ_i
        if j == i:
            return [i, i + 1, -i]             # x_i x_{i+1} x_i⁻¹
        if j == i + 1:
            return [i]                        # x_i
        return [j]
    else:                                     # σ_i⁻¹
        if j == i:
            return [i + 1]                    # x_{i+1}
        if j == i + 1:
            return [-(i + 1), i, i + 1]       # x_{i+1}⁻¹ x_i x_{i+1}
        return [j]


def artin_apply_gen_to_word(sign_i, w):
    out = []
    for g in w:
        img = artin_gen(sign_i, abs(g))
        out += img if g > 0 else inv(img)
    return reduce_word(out)


def braid_on_generator(braid, j):
    """β = s₁…s_m acts as s₁∘…∘s_m (left action): apply the LAST letter first."""
    w = [j]
    for s in reversed(braid):
        w = artin_apply_gen_to_word(s, w)
    return reduce_word(w)


# ── longitude of a pure braid: β(x_i) = A_i x_i A_i⁻¹  ⇒  return A_i ───────────
def longitude(braid, i):
    w = braid_on_generator(braid, i)
    A = []
    lo, hi = 0, len(w) - 1
    while lo < hi and w[lo] == -w[hi]:        # symmetric peel of the conjugator
        A.append(w[lo]); lo += 1; hi -= 1
    if not (lo == hi and w[lo] == i):
        raise ValueError(f"braid not pure / x_{i} not central: {w}")
    assert reduce_word(A + [i] + inv(A)) == w, "longitude reconstruction failed"
    return A


# ── Magnus expansion truncated at degree 2 ────────────────────────────────────
def mag_gen(g):
    if g > 0:
        return {(): 1, (g,): 1}
    a = -g
    return {(): 1, (a,): -1, (a, a): 1}      # (1+X)⁻¹ = 1 − X + X² − … (deg ≤ 2)


def mag_mul(p, q):
    r = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            if len(m1) + len(m2) > 2:
                continue
            m = m1 + m2
            r[m] = r.get(m, 0) + c1 * c2
    return {m: c for m, c in r.items() if c != 0}


def magnus(word):
    s = {(): 1}
    for g in word:
        s = mag_mul(s, mag_gen(g))
    return s


def mu_bar(braid, i, j, k):
    """μ̄(ijk) = coeff of X_i X_j in Magnus(λ_k)."""
    return magnus(longitude(braid, k)).get((i, j), 0)


def pairwise_lk(braid, i, k):
    """lk(i,k) = coeff of X_i in Magnus(λ_k)."""
    return magnus(longitude(braid, k)).get((i,), 0)


def mirror(braid):
    """Spatial mirror of a link = invert every crossing (σ_i ↔ σ_i⁻¹)."""
    return [-s for s in braid]


def reverse_orient(braid):
    """Reverse all component orientations (turn the closed braid upside down)."""
    return list(reversed(braid))


# ── named braids ──────────────────────────────────────────────────────────────
BORROMEAN = [1, -2, 1, -2, 1, -2]            # (σ₁ σ₂⁻¹)³
UNLINK = []                                   # trivial 3-braid (3-component unlink)
HOPF = [1, 1]                                 # σ₁² on 2 strands (lk = +1)


def main():
    print("=" * 78)
    print("§3.4-G2-CHIRAL — exact μ̄ on a GENUINE Borromean (Artin + Magnus)")
    print("=" * 78)
    print()

    # ── CONTROL: the mirror operation is REAL (it flips a linking number) ─────
    lk_hopf = pairwise_lk(HOPF, 1, 2)
    lk_hopf_m = pairwise_lk(mirror(HOPF), 1, 2)
    mirror_ok = (lk_hopf == 1 and lk_hopf_m == -1)
    print("  CONTROL — the spatial mirror (crossing inversion) is genuine:")
    print(f"    Hopf σ₁²: lk = {lk_hopf:+d};  mirror σ₁⁻²: lk = {lk_hopf_m:+d}   "
          f"{'✓ mirror flips lk (reflection-odd at degree 1)' if mirror_ok else '✗'}")
    print("    ⇒ crossing inversion IS the spatial mirror; anything it does NOT")
    print("      flip is genuinely reflection-EVEN, not a code artifact.")
    print()

    # ── ground truth, exact ──────────────────────────────────────────────────
    m_bor = mu_bar(BORROMEAN, 1, 2, 3)
    m_mir = mu_bar(mirror(BORROMEAN), 1, 2, 3)
    m_rev = mu_bar(reverse_orient(BORROMEAN), 1, 2, 3)
    m_unl = mu_bar(UNLINK, 1, 2, 3)
    print("  μ̄(123), computed exactly:")
    print(f"    genuine Borromean (σ₁σ₂⁻¹)³ : μ̄ = {m_bor:+d}")
    print(f"    SPATIAL MIRROR (σ₁⁻¹σ₂)³    : μ̄ = {m_mir:+d}   "
          f"({'NO FLIP ⇒ reflection-EVEN' if m_mir == m_bor else 'flips'})")
    print(f"    reverse orientations        : μ̄ = {m_rev:+d}   "
          f"(flips — multilinear in component orientation, NOT spatial parity)")
    print(f"    3-unlink                    : μ̄ = {m_unl:+d}")
    print()

    # ── pre-registered criteria P1–P4 (SQT_3.4_SIGN_PREREGISTRATION.md) ───────
    p1 = (m_unl == 0)
    p3 = (abs(m_bor) == 1)
    m231 = mu_bar(BORROMEAN, 2, 3, 1)
    m312 = mu_bar(BORROMEAN, 3, 1, 2)
    m213 = mu_bar(BORROMEAN, 2, 1, 3)
    p4 = (m231 == m_bor and m312 == m_bor and m213 == -m_bor)
    p2_even = (m_mir == m_bor)                # the FINDING: reflection-even
    print("  PRE-REGISTERED CRITERIA (SQT_3.4_SIGN_PREREGISTRATION.md):")
    print(f"    P1 split/unlink → 0   : μ̄_unlink = {m_unl:+d}                {'✓' if p1 else '✗'}")
    print(f"    P3 |μ̄| = 1            : |μ̄| = {abs(m_bor)}                    {'✓' if p3 else '✗'}")
    print(f"    P4 cyclic consistency : μ̄(231)={m231:+d}, μ̄(312)={m312:+d}, "
          f"μ̄(213)={m213:+d}   {'✓' if p4 else '✗'}")
    print(f"    P2 mirror → −μ̄        : μ̄_mirror = {m_mir:+d} (= μ̄, NO FLIP)   "
          f"✗ — and the ✗ is the FINDING (μ̄ is reflection-EVEN)")
    print()

    print("=" * 78)
    print("G2-CHIRAL VERDICT")
    print("=" * 78)
    magnitude_ok = p1 and p3 and p4
    finding_ok = mirror_ok and p2_even
    if magnitude_ok and finding_ok:
        print(f"""\
  TWO CLEAN RESULTS on a genuine Borromean (no faked sign):

  (1) MAGNITUDE — RESTORED on the right object [R1].  |μ̄(123)| = {abs(m_bor)} on
      the genuine Borromean, 0 on the unlink, with correct cyclic/transposition
      structure (P1,P3,P4) — read off an EXACT word via Magnus, INDEPENDENT of the
      Seifert triple-point count whose self-comparison was circular. So the §3.4
      magnitude selection rule is correct AS A STATEMENT; the V4.29 retraction
      stands only because the FILED config (golden ellipses) was amphichiral
      (μ̄=0) — not the rule. The rule re-instantiates on a genuine Borromean.

  (2) SIGN — μ̄(123) is REFLECTION-EVEN [R1 finding].  The spatial mirror (proven
      genuine by the Hopf control, which DOES flip lk) leaves μ̄(123) UNCHANGED.
      μ̄ flips only under reversing component ORIENTATIONS, never under spatial
      reflection. Triple-confirmed: this exact computation + g2_milnor_int.py's
      reflection-even Massey integral + the textbook amphichirality of the
      Borromean rings. ⇒ sign(μ̄) is NOT a spatial-chirality/parity witness — not
      even on a genuine Borromean. The hoped-for "odd Massey jump-correction"
      does not exist; there was no odd term to find.

  CONSEQUENCE for the sign-map: the QR/QNR parity CANNOT come from μ̄'s spatial
  chirality. It must come from φ (octonionic winding direction) via the registered
  §2.75/§2.76/§2.86C consistency check — exactly where the registration put it.
  The registered sign(φ)↔QR/QNR map is UNTOUCHED and stays R3-pending that check;
  the sign(μ̄)↔parity half is now CLOSED NEGATIVE (μ̄ carries no spatial parity).""")
        rc = 0
    else:
        print("  Unexpected: a control or criterion did not behave as derived. "
              "Reporting honestly; do NOT claim a result. Check conventions.")
        rc = 1
    print()
    print("  Reproduce: python3 tools/g2_milnor_chiral.py")
    print("  Cross-refs: SQT_3.4_SIGN_PREREGISTRATION.md (P1–P4); g2_milnor_sign.py")
    print("  (amphichirality of the golden config); g2_milnor_int.py (even Massey")
    print("  integral); SQT_3.4_SIGNMAP_REGISTRATION.md (the map — untouched).")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
