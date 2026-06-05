# §3.4-G2-Milnor-SIGN First Pass — The Configuration Is Amphichiral (μ̄ = 0): a Finding That Reaches the Magnitude

**Date:** 2026-06-05
**Register:** **R1** — a rigorous structural finding (a verified symmetry forces
μ̄=0). **Pre-registration:** `reports/SQT_3.4_SIGN_PREREGISTRATION.md` (committed
before computing). **Tool:** `tools/g2_milnor_sign.py`.
**Eddington watch:** ACTIVE — no sign was faked; the pre-registered control (P2)
caught the issue, and it turned out to be deeper than an orientation bug.

> **This is not a routine partial.** The disciplined sign build, judged against
> the pre-committed criteria, has surfaced that the configuration used throughout
> §3.4-G2-Borromean (V4.27) and §3.4-G2-Milnor (V4.29) is **amphichiral with true
> μ̄(123) = 0** — *not* a chiral Borromean (μ̄=±1). The prior |μ̄|=1 results are
> the **uncorrected** Seifert count. **The magnitude claim needs a recheck.**

## §1 — What the sign build computed

Method A (the reflection-odd Seifert-intersection linking, μ̄(ijk)=lk(C_k, γ_ij))
against the pre-registered criteria:

| Criterion | Result | |
|---|---|---|
| **P1** split → 0 | μ̄_split = −0.001 | ✓ |
| **P3** \|μ̄\| = 1 | \|μ̄\| = 0.971 | ✓ |
| **P4** cyclic consistency | μ̄(231)=μ̄(312)=−0.97, μ̄(213)=+0.97 | ✓ |
| **P2** mirror → −μ̄ | μ̄_mirror = −0.97 (= μ̄, **no flip**) | **✗** |

Method A is internally consistent — correct cyclic symmetry, correct
transposition antisymmetry, unit magnitude — yet **does not flip under the z→−z
mirror.** Per the pre-registered rule the sign is **not established.** But the
*pattern* (P1/P3/P4 pass, only P2 fails) is diagnostic.

## §2 — The finding (R1): the configuration is amphichiral, μ̄ = 0

**z→−z is a symmetry of the configuration.** Verified directly: the mirror sends
each of the three golden ellipses to **itself** (set-distance 0.0000 for all
three). So z→−z is an *orientation-reversing symmetry* of the link.

**Therefore μ̄(123) = 0.** μ̄ is reflection-odd, and odd under reversing any single
component (Magnus: reversing component k flips the meridian/longitude, negating
the X₁X₂ coefficient). The map z→−z reverses exactly **two** component
orientations (E₂, E₃; E₁ lies in z=0 and is fixed). Hence

    μ̄(123) = (−1)_ambient · (−1)² · μ̄(123) = −μ̄(123)  ⟹  μ̄(123) = 0.

The orthogonal-golden-ellipse configuration is **amphichiral**, not a chiral
Borromean. (This is airtight given the verified symmetry; it is not an
orientation-bookkeeping artifact of Method A.)

**Why the counts said |μ̄|=1.** Method A's lk(C₃,γ₁₂) and the §3.4-G2-Milnor
Seifert **triple-point count** both compute the *uncorrected* Seifert linking,
which is ±1 for this configuration. The **Mellor–Melvin correction terms** (the
curve–surface boundary contributions, omitted in both) bring the true μ̄ to 0.
The single transverse triple point at the origin is cancelled by the corrections
the symmetry guarantees.

## §2.5 — Sharpened: TWO distinct issues (per SQT-agent analysis + 3 tests)

The agent correctly flagged that I conflated two things. Separating them
(discriminating tests now in the tool):

- **(i) Method A is reflection-EVEN for the spatial mirror — a *convention*
  limit (the agent's "trap #4").** Its segment orientation uses n_i×n_j, a cross
  product of two *axial* surface normals, which is itself axial; an
  intrinsically-(re)computed orientation is reflection-even by construction. So
  Method A **cannot read spatial chirality on any config** — its P2 failure is
  *not by itself* evidence of μ̄=0. (Tests confirm Method A is nonetheless correct
  on the *permutation* structure: **T1** it flips under a component reversal;
  **P4** cyclic-invariant / transposition-odd. So only the *mirror* handling is
  convention-limited.) Fix: a **fixed-frame (transported)** orientation.
- **(ii) The configuration is amphichiral (μ̄=0) — the *finding*, and it rests on
  the symmetry argument, NOT on Method A.** **T2** confirms z→−z **fixes each
  component** (set-distance 0; *not* a permutation), so the §2 chain
  (μ̄ = −μ̄ ⟹ 0) holds independently of Method A's convention issue.

These **combine**: on the symmetric config, Method A can't see the sign *and*
there is no sign to see. The agent's deeper reading is right — the "geometric
Borromean handedness" the registration leaned on was **frame-dependent** on this
config (no topological spatial chirality), exactly as a physical parity must be.

## §2.6 — Framework-critical check (T3): the substantive map is NOT threatened

The agent's sharpest point: do sign(φ) and sign(μ̄) stay *independent*? **T3:** the
QR↔QNR conjugate used, (0,1,3)→(0,3,1), is a **transposition (odd)** — but of the
**winding directions** d_i (octonion indices), which flips **φ** and **not** μ̄
(μ̄ is the strand geometry, independent of which component each strand winds in).
So in the computation the **two signs are genuinely independent**. The collapse
the agent warned of would occur **only if** physical QR↔QNR is realized as a
**strand permutation** that is odd — and that is exactly the §2.75/§2.76/§2.86C
**consistency check the registration pre-committed to**. This sign build
**foregrounds** that check but does **not** settle it; the registered substantive
map sign(φ)↔QR/QNR is **untouched**. What is refined is only the *forced/geometric*
half (sign(μ̄)↔parity): the geometric witness is frame-dependent, not a topological
invariant, on the symmetric config.

## §3 — Consequence (must be surfaced): the magnitude claim needs a recheck

This reaches **already-folded canonical results**:

- **§3.4-G2-Milnor (V4.29):** the magnitude selection rule "|μ̄^φ| = 1 iff
  Fano-line genuine Borromean" was validated using the **Seifert triple-point
  count on this configuration** — which is the uncorrected count of an
  **amphichiral (μ̄=0)** link. The "1" is the uncorrected value; the corrected
  μ̄ is 0. **The magnitude claim does not stand on this configuration.**
- **§3.4-G2-Borromean (V4.27):** the "genuine Borromean (μ̄=±1)" framing is
  incorrect for the golden-orthogonal config; pairwise-unlinkedness was verified,
  but the triple-linking is **0**, so the config is amphichiral (possibly even
  unlinked — to be determined), not the chiral baryon.

**What is NOT affected:** the φ-weighted *selection* structure (φ_abc nonzero iff
Fano line) and the two-sign *factorization* are algebraic facts independent of
the link's chirality. The **registered sign(φ)↔QR/QNR map is untouched** (it was
never going to be confirmed by this computation). And the meson-sector G2-orient
result (pairwise Hopf charge) is independent of μ̄.

## §4 — The required fix (the real next step)

1. **Fix Method A's orientation (trap #4):** replace the axial n_i×n_j segment
   orientation with a **fixed-frame, transported** orientation, so the linking
   number is genuinely reflection-odd (P2-capable). Verify on a known-chiral
   link that it then flips under mirror.
2. **Use a manifestly CHIRAL Borromean** — break the z→−z symmetry (a chiral
   offset / screw arrangement, or a known μ̄=±1 parametrisation), confirmed
   chiral (μ̄≠0) by the symmetry check — and **recompute BOTH** the magnitude
   (does |μ̄^φ|=1 there, *with* the Mellor–Melvin corrections) **and** the sign
   (does the fixed-frame Method A flip under mirror, P2 passing).
3. **Determine the golden-orthogonal link type** (amphichiral nontrivial vs.
   unlink) for the record.
4. **Re-validate G2-Milnor's magnitude** on the chiral config with corrections
   before the |μ̄^φ|=1 claim is restated.

Until then: **the sign stays R3-pending**, and **the §3.4-G2-Milnor magnitude
result should be flagged "under review — configuration amphichiral, recheck on a
chiral Borromean required."** No result is faked; the honest reading is that
there is no nonzero sign on this configuration to find, *because the
configuration is amphichiral.*

## §5 — Proposed Part VI / canonical update

| Task | Status |
|---|---|
| §3.4-G2-Milnor-SIGN | **First pass — R1 finding (amphichirality):** Method A is reflection-odd, cyclic-consistent, but P2 fails because **z→−z is a symmetry of the golden-orthogonal config ⇒ μ̄(123)=0** (verified). The sign is not established (there is none here). |
| §3.4-G2-Milnor (V4.29 magnitude) | **FLAG: under review.** The |μ̄^φ|=1 selection rule used the uncorrected Seifert count on an **amphichiral** configuration; recheck required on a manifestly-chiral Borromean with Mellor–Melvin corrections. |
| §3.4-G2-CHIRAL (new) | **Open — prerequisite:** build a manifestly-chiral Borromean (symmetry broken) and recompute magnitude + sign with corrections. |

*Reproduce: `python3 tools/g2_milnor_sign.py`. Pre-registration:
`SQT_3.4_SIGN_PREREGISTRATION.md`. Append-only; this report does not itself
modify canonical, but RECOMMENDS the V4.27/V4.29 magnitude flag above.*
