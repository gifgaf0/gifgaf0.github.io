# G-2a-S9 SECOND-LEG REPORT (CC, independent) — the Pin fork of the flat home

**Date:** 2026-07-10 · **Pre-registration:** `G_2a_S9_EXECUTION_PREREGISTRATION.md` (**DRAFT**,
author-lock pending) · **Script:** `gate2a_s9_secondleg.py` (exact Cℓ(3)± over ℚ(√2)) ·
**Base:** V4.59.

> **STATUS.** CC leg run against the **DRAFT** pre-reg, **ahead of author-lock and the chat leg**
> (S8 precedent: that draft was byte-identical to its lock and running ahead converged). Nothing
> folded. If the locked pre-reg changes the hypotheses, I re-run. The run doubled as a design check
> — see the self-caught bug (under-generated N) below.

## Method (independent)
Explicit Clifford algebra Cℓ(3)^q over ℚ(√2), q = e_i² = **+1 (Pin⁺)** / **−1 (Pin⁻)**; Pin±(3)
covers O(3) by the twisted adjoint ρ(x)v = α(x) v x⁻¹. The amphichiral square is lift-independent
((±x)²=x²), so B1 is a direct Clifford computation. The Γ/N presentation, Φ_flat, and the pinned g_A
come from S7 (shared, flagged). **Convention** fixed per the pre-reg §0. **Scope:** full O(3) action;
**no time-reversal reading anywhere** (Eddington trap 2 honored).

## In-execution collision check (Eddington trap 5) — done
Searched for a published Pin±-lift classification of #24 / I2₁2₁2₁ or its normalizer with the
amphichiral class isolated. **None found** — the pieces (I2₁2₁2₁ crystallography; Borromean orbifold;
Kirby–Taylor/Blau–Dabrowski Pin theory) exist separately; no source assembles this. Novelty class:
**novel-in-assembly**, as registered. *(Sources at end.)*

## Element dictionary (pinned BEFORE any square — Eddington trap 3)
Reusing the S7 Φ_flat over the full N: the amphichiral class **g_A = (id; +,+,+; −1)** is realized by
the **glide reflection** (B = diag(−1,1,1) | (0,0,1)) — reflection in the x-mirror plus a z-glide;
its point part is an **order-2 reflection** (det −1). **g_A² = (I | (0,0,2)) = 2e₃ ∈ Γ.** And
**g_A ≠ −I**: Φ_flat(−I) is the *different* class (id; +,−,−; −1). So g_A is a genuine reflection-type
element, not point-inversion — the confusion the pre-reg quarantines is avoided.

## Calibration + regression (machinery controls)
- **Calibration:** ω = e₁e₂e₃ covers −I with **ω² = −q** (ω²=−1 in Pin⁺, +1 in Pin⁻). Verified.
- **Regression:** the π-rotation lift (bivector e₂e₃) covers diag(1,−1,−1) and squares to **−1 in
  *both* Pin types** (Pin-blind — the proper sector is the common Spin(3)). This reproduces the S8
  ambient-2π meridian −1: **the fork lives only in the improper (reflection) sector.**

## H-B / decisive bit B1 — the amphichiral square (PASS, R1)
g_A's point part lifts to the unit vector **e₁** (ρ(e₁)=diag(−1,1,1)); the glide translation 2e₃ is
spin-trivial (+1). So **(lift g_A)² = e₁² = q**:
- **Pin⁺: g_A² = +1** (g_A lifts to an involution).
- **Pin⁻: g_A² = −1** (g_A lifts to an order-4 element; its square is the central −1).

**B1 = Pin-DISTINGUISHING (branch a): the fork is real and binary — the flat home's amphichiral
symmetry sees the Pin type.** (For the record, −I=ρ(ω) gives ω²=−q, the *opposite* assignment — a
distinct element, confirming g_A≠−I matters.)

## H-A — the Pin structure set (both types populated)
The proper sector (d=+1) is the **same Spin(3)** in both algebras (products of two vectors cancel
the e_i² sign), so every S8 Spin structure sits in both. Extending over the improper coset: every
improper isometry lifts to an odd Clifford element, which exists in **both** Cℓ(3)⁺ and Cℓ(3)⁻; the
point-group double cover closes to order **96 = 2×48** in both types (ρ surjects onto O_h). So **both
Pin types are populated** — this is **not** a forced Pin selection; the types are distinguished only
by the amphichiral square (B1), and — see B2 — the improper extension forces the S8 boundary bit.

## H-C / decisive bit B2 — interaction with the S8 boundary bit (PASS, R1) — FORCED
On the **full** N/2ℤ³ (order 384, point group O_h=48): **H₁(N;ℤ/2) has order 4, but [e_f]=0 and
[t₁₁₁]=0** — verified **two independent ways** (commutator/square-subgroup membership, *and* an
exhaustive search finding **no** homomorphism N→ℤ/2 with χ(e₁)=−1). Therefore:
- **B2 = FORCED (branch i):** the improper (Pin) sector **consumes** the S8 boundary bit. Over N⁺
  (S8) the turn-over sign was a free choice; over the full N it is forced — **only the χ(t₁₁₁)=+1
  ((+,+,+)) diagonal S8 structure extends over the improper coset; the (−,−,−) does not.** The
  residual §2.50-adjacent freedom in the turn-over sector shrinks to zero within the Pin-completed home.

*(This flips the S8 "CHOICE" — correctly, and it is a refinement, not a contradiction: a bit free on
N⁺ is pinned by the larger N. Verified twice precisely because it overturns the S8-level reading.)*

## H-D — verdict: OPEN-FORK
Net accounting across S8 → S9:
- **B1** makes choosing the Pin type a **new located ℤ/2 import** — the geometry does not select Pin⁺
  vs Pin⁻, but the amphichiral square distinguishes them (real & binary).
- **B2** **consumes** the old located ℤ/2 (the S8 boundary bit), forcing it to (+,+,+).
- So the located-ℤ/2 freedom **moves up one level**: from a boundary-condition bit on N⁺ to the Pin
  type on N. **NOT forced-Pin** (both types exist), **NOT Pin-blind** (the square sees the type).
- **M.REL:** scale — none; metric — flat (inherited); **sign — the Pin type is the axis under test,
  a located ℤ/2 import; the S8 boundary bit is consumed**; ontology — unchanged and quarantined (the
  cone-π scaffolding and the carrier identification are **not** made by this gate, verbatim from S8).

## Honesty — self-caught bug
My first B2 pass used N generators that produced only the **orientation-preserving** part (order 192,
point group T_h/O=24) — the glide reflection + 3-fold don't generate the axis-transpositions. Adding
the S8 proper-odd generator W fixed it to the correct full N (order 384, O_h=48), and the B2 result
**flipped** from "independent" (wrong group) to **FORCED** (correct group) — which is why I added the
second-way character cross-check before trusting it.

## Boundaries
- **DRAFT + ahead of chat leg:** this is the CC leg, ready to cross-check; no two-leg agreement yet.
- **Shared presentation:** independence at the **code + method** level (own Clifford build, own
  element-dictionary reuse of S7, own homology + character computations); the S7 Γ/N presentation is
  shared, flagged per S4/S7 precedent.
- **H-A depth:** I established structure *existence* in both Pin types (odd lifts + order-96 double
  cover) and the boundary-bit selection (B2), but did **not** enumerate the full Q̃± (order 768)
  structure count with the complete relation audit the chat leg is spec'd to do — that finer count is
  where a chat-leg cross-check would add most.

## Verdict (second leg)
- **Element dictionary (R1):** g_A = glide reflection, g_A²=2e₃, g_A≠−I.
- **B1 (R1): Pin-DISTINGUISHING** — g_A²=+1 (Pin⁺), −1 (Pin⁻). The fork is real and binary.
- **H-A (R1):** both Pin types populated; not a forced selection.
- **B2 (R1): FORCED** — the improper sector consumes the S8 boundary bit (χ(t₁₁₁)→+1).
- **H-D: OPEN-FORK** — the located ℤ/2 moves up from the boundary bit to the Pin type. No §2.50
  closure; ontology imports untouched; no μ_n; no time-reversal; §2.52 Open 3 untouched.

**Sources (collision check):** en.wikipedia.org/wiki/Space_group ; Kirby–Taylor 1990 (Pin structures,
LMS 151); Blau–Dabrowski 1989 (Pin structures on quotients); math.osu.edu lectures on orbifolds &
reflection groups; web.math.ucsb.edu Cooper–Hodgson–Kerckhoff (Borromean = cube-folding). No source
gives the Pin±-lift classification of #24's normalizer with the amphichiral class isolated.
