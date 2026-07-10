# G-2a-S8 SECOND-LEG REPORT (CC, independent) — spinorial structure of the flat home

**Date:** 2026-07-10 · **Pre-registration:** `G_2a_S8_EXECUTION_PREREGISTRATION.md` (locked; **byte-
identical** to the draft I first ran against) · **Script:** `gate2a_s8_secondleg.py` (exact ℚ +
quaternions + an SU(2)/ℚ(i,√2) cross-check) · **Base:** V4.56 · **Chat leg:** `g_2a_s8_chatleg.py`
+ `G_2a_S8_CHATLEG_REPORT.md` + `G_2a_S8_CC_HANDOFF.md`.

> **STATUS — two-leg agreement achieved.** I first ran this leg against the DRAFT pre-reg (ahead of
> author-lock and the chat leg — the timing-confirmation question tool errored and you said continue,
> per the S5 precedent). The locked pre-reg then arrived **byte-identical** to that draft, so the
> hypotheses I computed against were correct. I then read the chat report + handoff (**not** the chat
> script — the handoff forbids reading it before the first run, which I honored) and extended this leg
> to cover the full handoff target table **T1–T17**. **Every decisive bit and target agrees with the
> chat leg**, including — found independently by my own BFS — the same word t₍₁,₁,₁₎ = r₁r₂r₁r₃r₁.
> The first-pass design check also caught two bugs in my own code (below).

## Method (independent)
Per the pre-reg's CC-leg spec ("cohomological extension-class route vs direct quaternion
enumeration"): **H-A/H-B by exact unit-quaternion (Spin(3)) arithmetic**; **H-C by the mod-2 homology
finite model** — build N⁺/2ℤ³ (order 192, point group O=24) and compute H₁(N⁺;ℤ/2) directly as
G / ⟨commutators, squares⟩, locating [e_f] and exhibiting the twisting character explicitly. Only the
S7-verified Γ/N⁺ presentation is shared (flagged, per S4/S7 precedent). Scope = **N⁺ only (Spin(3),
not Pin)**; the amphichiral sector is the S9 bank, untouched here.

**Finite-model validity (stated, not assumed):** 2ℤ³ ⊆ [N⁺,N⁺] because the point group O contains the
2-fold rotations and (1−A_f)ℤ³ ⊇ 2ℤ³; hence N⁺^ab = (N⁺/2ℤ³)^ab and **H₁(N⁺;ℤ/2) = H₁(N⁺/2ℤ³;ℤ/2)** —
the finite model computes the real group's mod-2 first homology exactly.

## H-A — no spinorial lift of Γ (PASS, R1)
In Γ, **r_f² = e** (verified by matrix multiplication), but every lift s(r_f)=±q_f satisfies
s(r_f)² = q_f² = **−1** ≠ s(e)=+1. Exhaustive over all 2³ sign assignments: **no section exists** →
the extension 1→ℤ/2→Γ̃→Γ→1 is **non-split**. Every deck representation on spinor fields therefore
factors through Γ̃ with **−1 ↦ −Id forced** — the algebraic shape of the §2.50 desideratum, realized
structurally in the orbifold home. The live falsifier (a consistent section) did **not** fire.

## H-B — the ambient-2π meridian sign (PASS, R1) — decisive bit B1 = FORCED
Respecting the loop dictionary: the decisive datum is at **μ_f** (ambient 2π, deck class r_f²), **not**
the cone loop m_f (deck r_f). Monodromy(μ_f) = (lift r_f)² = **q_f² = −1** for every strand f. Under any
twist χ ∈ Hom(Γ,ℤ/2), the lift becomes χ(r_f)·q_f and squares to χ(r_f)²·q_f² = q_f² = −1 — **twist-
independent** (χ(r_f)²=+1). So **B1 = B1-FORCED: the ambient-2π per-strand spinor sign is −1 for every
strand, in every Γ-spinorial structure.**
- **R3 bank (logged, uninterpreted):** the cone loop m_f carries ±q_f — order 4 (q_f²=−1, q_f⁴=1),
  twist-**dependent** in sign — a ℤ/4 refinement native to the cone-π scaffolding.

## H-C — the turn-over sign system (PASS, R1) — decisive bit B2 = CHOICE
On the full N⁺/2ℤ³ (order 192, point group O=24; the 3-fold and odd generators verified to normalize
Γ independently): **H₁(N⁺;ℤ/2) has order 4**, and **[e_f] ≠ 0** for every strand f (also [(1,1,1)]≠0,
[r_1]≠0). The triple relation e₁e₂e₃ = (1,1,1) ∈ L ⊂ Γ holds; S₄-equivariance forces [e₁]=[e₂]=[e₃].
- Because [e_f] ≠ 0, a twisting character exists — and the computation **exhibits an explicit one**: a
  genuine homomorphism χ: N⁺→ℤ/2 with **χ(e_f)=−1** (all f), χ(w)=χ(c)=+1. Twisting by χ flips every
  turn-over sign while leaving μ_f monodromy at −1 (χ(r_f)²=1).
- Therefore **B2 = B2-CHOICE:** the turn-over sign is a genuine spin-structure datum — the classical
  T³ periodic/antiperiodic **boundary condition** surviving into N⁺ — **not** structurally forced.
  The import is **located as a boundary-condition choice** on the flat home (the pre-reg flagged this
  as the most M.BRIDGE-informative branch).

## Handoff target table T1–T17 — reproduced (two-leg)
Extended the leg to cover the handoff's target table with the requested independence gestures:
- **SU(2)/ℚ(i,√2) cross-check** (independence req #1): U(2_f)² = −I for the three π-rotation lifts;
  translation SU(2)-part = I. (Main H-A/B1/H-C used quaternions — **flagged**, as the handoff allows;
  H-C's mod-2 homology route is itself the "cohomological extension-class" alternative to the chat's
  direct Q̃ enumeration.)
- **T16 (the sharp B2 statement):** both lifts (±U) of every deck π-rotation square to **z=−I**; both
  lifts (±I) of every turn-over e_f are **involutions** (square = +I, never z). **The −1 lives in the
  meridian channel, not the turn-over channel** — the cleanest form of "B2 is not the FR sign."
- **T5 (positive control):** all 2³=8 sign assignments over the pure-translation torus are consistent
  sections (the T³ spin structures) — so the H-A negative is a property of Γ's torsion, not a solver
  artifact.
- **T3 (own word search):** t₍₁,₁,₁₎ = **r₁ r₂ r₁ r₃ r₁** (length 5), class r̄₁+r̄₂+r̄₃ — found by my
  own BFS, matching the chat's word exactly.
- **T8/T9 (own affine solves):** c₃ (3-fold) → integral, b=0 valid (S7 even-coset slice); g₄ (4-fold)
  → all solutions (½,½,½) (S7 odd-coset shift class).
- **T12/T13:** |Hom(N⁺/2ℤ³, 𝔽₂)| = **4**; admissible turn-over restrictions = **{(+,+,+), (−,−,−)}**
  only — strand-uniform, exactly the chat's two admissible diagonal structures.

## H-D — verdict: SPLIT (B1-FORCED, B2-CHOICE) — MATCHES chat leg
- The **ambient-2π per-strand spinor phase (−1) is structural** in the flat home (twist-independent).
- The **turn-over sign is a located boundary-condition import** (a spin-structure choice on N⁺).
- So §2.50's import **relocates** to {cone-π orbifold scaffolding} + {carrier identification} +
  {turn-over boundary condition} — a **sharpened LOCATED-IMPORT**, and **explicitly NOT a §2.50
  closure** (the pre-reg's own scope clause; structurally impossible from here).
- **M.REL:** scale — none; metric — flat (S7, unchanged); **sign — {2π FORCED, turn-over CHOICE}**;
  ontology — the cone-π scaffolding and carrier-identification imports remain intact/undeclared.

## Eddington discipline (held)
- **−1 = −1 trap:** the orbifold-spinor −1 (this gate) is **not** identified with the framework
  per-strand carrier −1 (§2.50). Same symbol, distinct objects; **no identification made**, no drift
  toward μ_n.
- **2π-substitution trap:** the decisive bit is computed at **μ_f** (r_f²), never silently at m_f (r_f).
- **No numeric targets:** μ_n sealed; no mass/moment/observable consulted. §2.52 Open 3 untouched.

## Honesty — two bugs I caught in my own first pass
1. **Under-generated N⁺:** my initial generator set produced point group order 8 (|G|=64), not the
   full O (|G|=192). Fixed by adding a 3-fold generator (verified to normalize Γ). The H-C result is
   from the **correct** order-192 group.
2. **Wrong character:** I first hypothesized the twist χ(B,t)=(−1)^Σt — which is **not even well-
   defined** on N⁺ (odd elements have half-integer translation sum). The correct twisting character is
   the one the computation found by exhaustive homomorphism search. My hand-reasoning reached the
   right *verdict* (CHOICE) for a partly wrong reason; the rigorous computation supersedes it.

## Boundaries
- **Independence #1 (quaternions):** the main H-A/B1/H-C used quaternions, not the requested SU(2) —
  **flagged**, with an SU(2)/ℚ(i,√2) cross-check of the decisive lift facts added. H-C's mod-2 homology
  route is the "cohomological" method variation (vs the chat's direct Q̃ enumeration); H-A used a brute
  sign-sweep (same shape as the chat's), not the H² obstruction route.
- **Shared presentation:** independence is at the **code + method** level on the S7-verified Γ/N⁺
  presentation; flagged per S4/S7 precedent.
- **Scope:** N⁺/Spin only. The amphichiral (Pin⁺/Pin⁻) sector is the S9 bank — not addressed.
- **§7 KF partial-discharge memo:** a sibling item requiring author authorization before fold; **not**
  acted on here (it is not a computation for this leg).

## Verdict (second leg)
- **H-A: PASS (R1)** — Γ non-split; −1 ↦ −Id forced.
- **H-B: PASS (R1) — B1-FORCED** — μ_f monodromy −1, every strand, every twist.
- **H-C: PASS (R1) — B2-CHOICE** — [e_f]≠0 in H₁(N⁺;ℤ/2) (order 4); explicit twisting character exhibited.
- **H-D: SPLIT** — 2π phase structural, turn-over sign a located boundary-condition import; not a §2.50
  closure. M.CW/M.BRIDGE intact.

*Ready to cross-check against the chat leg once the pre-reg locks and it runs.*
