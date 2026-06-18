# §3.4 CORRECTION — The Golden Ellipses ARE the Borromean Rings; the Amphichirality Retraction Was an Error

**Date:** 2026-06-05
**Register:** **R1** — an authoritative computational identification (SnapPy),
independently reproduced. **Tool:** `tools/golden_link_id.py`.
**Status:** This note **reverses** the amphichirality finding of
`SQT_3.4_G2_MILNOR_SIGN_FIRST_PASS.md` and corrects the framing of
`SQT_3.4_G2_CHIRAL_FIRST_PASS.md`. It supports reversing the canonical V4.31 /
§3.08 retraction.

> **The error, stated plainly.** The amphichirality "proof" (μ̄=0 for the golden
> config) rested on **μ̄ being reflection-ODD**. μ̄(123) is reflection-**EVEN**.
> With the correct parity, the z→−z symmetry imposes **no constraint** on μ̄, and
> the golden ellipses are free to be — and **are** — the genuine Borromean rings
> (μ̄=±1). The original V4.29 magnitude claim was **correct**; its retraction
> (V4.31/§3.08) was **wrong** and should itself be retracted.

## §1 — The load-bearing fact, settled authoritatively

Are the three mutually-orthogonal golden ellipses (a=φ, b=1/φ) the **Borromean
rings** (μ̄=±1) or the **unlink** (μ̄=0)? Settled with SnapPy, via an extractor
written independently of the SQT-agent's:

**Ground truth** (spherogram braid closure): (σ₁σ₂⁻¹)³ → vol **7.327725**, census
name **t12067** = 6³₂ = L6a4 = the Borromean rings.

**Controls** (validate the extractor before trusting it):
- 3 separated circles → **0 crossings, 3 components** (unlink) — no spurious
  crossings manufactured.
- Hopf link → simplifies to **2 crossings, 2 components** — the correct minimal
  diagram (Hopf is non-hyperbolic, vol 0, as expected).

**Golden ellipses** (the filed §3.4 configuration), 6 independent random
projections:

    vol = 7.327725,  id = t12067,  3 components   — identical for all 6 seeds.

To 6 digits, the golden-ellipse complement IS the Borromean-rings complement.
(This is also the classical fact behind the International Mathematical Union logo:
three mutually-perpendicular golden ellipses realise the Borromean rings — flat
ellipses can, even though round circles cannot, by Freedman–Skora.)

**⇒ μ̄(123) = ±1 on the golden config. It is a genuine Borromean.**

## §2 — Why the amphichirality argument was invalid

The symmetry fact in `SQT_3.4_G2_MILNOR_SIGN_FIRST_PASS.md` is **correct**: z→−z
fixes each golden ellipse setwise, reversing the orientations of E₂ and E₃
(verified, set-distance 0). The **inference** to μ̄=0 was the error. Writing g for
that orientation-reversing isometry symmetry:

- **(A)** g is an orientation-reversing isometry ⇒ μ̄(g(L)) = ε·μ̄(L), where ε is
  the **reflection parity** of μ̄.
- **(B)** g(L) = L with E₂, E₃ reversed ⇒ μ̄(g(L)) = (−1)(−1)·μ̄(L) = μ̄(L).

Combining: **ε·μ̄ = μ̄.**
- If ε = −1 (reflection-**odd**): −μ̄ = μ̄ ⇒ μ̄ = 0. ← the original (wrong) claim.
- If ε = +1 (reflection-**even**): μ̄ = μ̄ ⇒ **no constraint**. ← the truth.

**μ̄(123) is reflection-EVEN.** This is confirmed four independent ways:
1. The exact braid/Magnus computation in `tools/g2_milnor_chiral.py` (the spatial
   mirror, Hopf-validated, leaves μ̄ unchanged).
2. The SQT-agent's independent matrix-Magnus.
3. Theory: a length-3 Milnor invariant is a Vassiliev invariant of order 2; the
   mirror acts on order-n by (−1)ⁿ = (+1) for n=2.
4. The Borromean rings are amphichiral (textbook) **with** μ̄=±1 — which is only
   consistent if μ̄ is reflection-even.

So "amphichiral ⇒ μ̄=0" is false for a reflection-even invariant. The golden
config is amphichiral **and** has μ̄=±1; both hold simultaneously, precisely
because μ̄ is even. The whole confusion was the false premise that μ̄ is odd.

## §3 — What this corrects (and what stands)

**Reversed / corrected:**
- **`SQT_3.4_G2_MILNOR_SIGN_FIRST_PASS.md`** — the amphichirality finding (μ̄=0,
  "not a Borromean") is **withdrawn**. The golden config is a genuine Borromean,
  μ̄=±1. (The verified z→−z symmetry fact stays; only the μ̄=0 inference is wrong.)
- **`SQT_3.4_G2_CHIRAL_FIRST_PASS.md`** — its **premise** (golden config
  amphichiral / "magnitude restored on a *different* object") is wrong: the
  magnitude is confirmed on the **same**, filed object. Its own reflection-even
  result is exactly what breaks the amphichirality argument — a contradiction I
  failed to catch when I wrote it. The SQT-agent's audit caught it.
- **Canonical V4.31 / §3.08** (the amphichirality retraction of V4.29): an
  **erroneous retraction**; recommend reversing it (a V4.32 / §3.09 entry).

**Stands (correct, and now properly situated):**
- **V4.29 magnitude |μ̄^φ|=1**: correct, correctly instantiated on the golden
  config (a genuine Borromean). **Restore.**
- **sign(μ̄) is reflection-EVEN** (from `g2_milnor_chiral.py`): correct and
  important. μ̄ flips only under reversing a *component orientation*, never under
  spatial mirror. ⇒ **sign(μ̄) is NOT a spatial-parity / chirality witness**, even
  on a genuine Borromean. The V4.29 "sign(μ̄)↔parity (forced)" and the
  "reflection-odd handedness witness ↔ sign(μ̄)" identifications are **closed
  NEGATIVE**.
- **sign(φ) ↔ QR/QNR map**: **untouched, R3-pending**, and now the **sole** route
  to the QR/QNR parity (μ̄-chirality is foreclosed) — exactly where the
  registration always put it.
- The earlier `g2_milnor_int.py` finding (Massey integral nonzero on golden,
  reflection-even) is now fully consistent: nonzero ⇒ genuine Borromean;
  even ⇒ no odd jump-correction to find (there never was one).

## §4 — My error, owned

I built `g2_milnor_chiral.py` **on top of** the amphichirality premise while
**simultaneously proving** the reflection-even fact that destroys it, and did not
flag the contradiction. The reflection-parity of μ̄ was the load-bearing step and
I took the "odd" version from memory in the SIGN report without checking it. The
SQT-agent's independent audit (re-deriving the parity, then SnapPy-identifying the
link) caught both. Independently reproduced here (`tools/golden_link_id.py`, own
extractor, controls passing, 6 seeds) — the correction is confirmed, not merely
conceded.

## §5 — Proposed canonical update (append-only): V4.32 / §3.09

A **§3.09 "§3.08 retraction reversed"** entry, append-only:
- records the reflection-parity error and the SnapPy identification (vol 7.327725,
  t12067, 6 seeds, controls validated) as the provenance;
- **restores** V4.29's magnitude (|μ̄^φ|=1 on the genuine-Borromean golden config);
- folds the correct sign finding: **sign(μ̄) reflection-even ⇒ sign-as-parity
  CLOSED NEGATIVE**; **sign(φ)↔QR/QNR** the sole route, R3-pending;
- closes **§3.4-G2-CHIRAL** (magnitude confirmed on the real config; sign-as-parity
  closed-negative);
- the §3.08 entry and its row annotations stay in place (append-only) but are
  marked **reversed by §3.09**.

| Task | Status |
|---|---|
| golden-ellipse link type | **RESOLVED (R1):** Borromean rings (vol 7.327725 / t12067, SnapPy, 6 seeds, controls passing; reproduced independently). μ̄=±1. |
| V4.29 magnitude \|μ̄^φ\|=1 | **CORRECT — restore.** Correctly instantiated on the genuine-Borromean golden config. |
| V4.31 / §3.08 retraction | **ERRONEOUS — reverse** (assumed μ̄ reflection-odd; μ̄ is reflection-even). |
| sign(μ̄) ↔ parity | **CLOSED NEGATIVE (R1):** μ̄ reflection-even ⇒ no spatial-parity content. |
| sign(φ) ↔ QR/QNR | **Unchanged — R3-pending** its §2.75/§2.76/§2.86C consistency check (sole route). |

*Reproduce: `python3 tools/golden_link_id.py` (requires snappy, spherogram).
Append-only; cross-refs: `g2_milnor_chiral.py` (reflection-even sign),
`g2_milnor_sign.py` + its report (the withdrawn amphichirality finding),
`SQT_3.4_SIGNMAP_REGISTRATION.md` (the map — untouched).*
