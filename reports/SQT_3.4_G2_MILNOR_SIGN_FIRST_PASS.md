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
> the **uncorrected** Seifert count, and the validation was **circular** (the
> control was that same count). **The filed V4.29 magnitude is RETRACTED as
> filed**, independently of any recheck (μ̄=0 is proven now).

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

## §3 — Consequence: RETRACTION-grade, not just a flag (per SQT-agent; concurred)

This reaches **already-folded canonical R1 results**, and the honest scope is a
**retraction**, not a provisional flag — μ̄=0 is **proven now**; the recheck
answers a *different* question. (My earlier "flag pending recheck" under-stated
it; corrected here.)

**The decisive point — the validation was circular.** The §3.4-G2-Milnor
magnitude was "validated" against the **textbook |μ̄|=1** — but that control was
*itself* the uncorrected Seifert triple-point count, the very quantity under test.
There was **never an independent check** that the configuration was genuinely
Borromean; now there is a proof (μ̄=0) that it was not.

- **§3.4-G2-Milnor (V4.29) magnitude:** "|μ̄^φ|=1 iff genuine Borromean", filed
  canonical R1 (and in Paper II §3.4.6), used a configuration that is **not** a
  genuine Borromean (μ̄=0). The **filed value is wrong as filed** ⇒ **retract**.
- **§3.4-G2-Borromean (V4.27, B):** the "chiral, a sign is available" framing —
  the config is amphichiral; the witness tracks **no** nonzero invariant on it.
- **§3.4-G2-Milnor-INT (V4.30):** the integral as a "second magnitude method for
  |μ̄|" — it detected nonzero *geometry* but μ̄=0, so it was **not measuring μ̄**.

The recheck (§3.4-G2-CHIRAL) is a **separate, NEW** question — does a *manifestly
chiral* Borromean give |μ̄^φ|=1 with corrections? — **not** a pending validation
of the filed claim (already wrong).

**Survives intact (config-independent / different object):** V4.26 §3.4-SYM /
G0 / G1′ / G1″ (vacuum, no Borromean); **V4.27 §3.4-G2-orient** (Q_φ on a charge-1
*hopfion*, not the ellipses — meson sector stands); V4.27(A) pairwise-unlinked
(lk=0) and V4.27(C)/V4.29 **φ-orientation** (algebraic); the **registered
sign(φ)↔QR/QNR map** (untouched, T3, still R3-pending its consistency check).
The selection-rule **structure** (φ picks Fano lines; μ̄ supplies the magnitude)
is **not refuted — just never instantiated** (μ̄=0 on the degenerate config); the
recheck decides whether it holds on a real chiral Borromean.

## §4 — The required fix (§3.4-G2-CHIRAL, the real next step)

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

Until then: **the sign stays R3-pending**, and **the §3.4-G2-Milnor magnitude is
RETRACTED as filed** (μ̄=0 on the tested config, proven now) — not merely flagged
pending the recheck. No result is faked; the honest reading is that there is no
nonzero sign on this configuration to find, *because it is amphichiral.*

## §5 — Proposed canonical update (a V4.31 walk-back; framework author's call)

A genuine **§3.x retraction-log entry** (the thread's first — the magnitude was
filed canonical R1, now proven wrong on the tested config; unlike the
V4.2/V4.11/§2.78 unfiled-draft precedents), plus additive annotations on the
V4.27/V4.29/V4.30 rows, a finding section (amphichirality R1 + the Method-A
convention issue + T3), the new **§3.4-G2-CHIRAL** open task, and a one-line
Paper II §3.4.6 retraction note. **Full retraction recommended** (concurring with
the SQT-agent): μ̄=0 is proven independently of the recheck.

| Task | Status |
|---|---|
| §3.4-G2-Milnor-SIGN | **First pass — R1 finding (amphichirality):** Method A is reflection-odd, cyclic-consistent, but P2 fails because **z→−z is a symmetry of the golden-orthogonal config ⇒ μ̄(123)=0** (verified). The sign is not established (there is none here). |
| §3.4-G2-Milnor (V4.29 magnitude) | **RETRACT as filed.** |μ̄^φ|=1 used the uncorrected Seifert count on an **amphichiral (μ̄=0)** config; the validation was circular (the "textbook |μ̄|=1" control *was* that same count). Filed value wrong as filed; selection rule re-opened, restoration is the §3.4-G2-CHIRAL question. |
| §3.4-G2-CHIRAL (new) | **Open — prerequisite:** build a manifestly-chiral Borromean (symmetry broken) and recompute magnitude + sign with corrections. |

*Reproduce: `python3 tools/g2_milnor_sign.py`. Pre-registration:
`SQT_3.4_SIGN_PREREGISTRATION.md`. Append-only; this report does not itself
modify canonical, but RECOMMENDS the V4.27/V4.29 magnitude flag above.*
