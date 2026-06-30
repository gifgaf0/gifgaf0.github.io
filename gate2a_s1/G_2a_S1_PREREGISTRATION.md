# G-2a-S1 — Pre-Registration

**Gate:** G-2a-S1 (Gate 2a, **S**tructural screen **1** — Route 1: the necessary-condition
screen for the soliton spin-isospin locking, §2.87.A). Token chosen to avoid the
ledger-flagged "Gate 2a" / "G-2a" collision.
**Mode:** Audit. **Register ceiling:** R2 (admissibility). **Eddington watch: ACTIVE.**
**Written before any computation.** Chat-side first leg; CC second leg required before any ledger entry.

---

## Question (what this screen does, and what it provably cannot do)

§2.87.A postulates (R3) that the baryon soliton's spatial binary-octahedral group 2O is
**locked** to the 2O of an internal spin/isospin SU(2), so the spatial 2π rotation ↦ the
central −1 ↦ −Id (the Finkelstein–Rubinstein / spinor phase) and the rotational quartet
becomes spin-3/2 (the μ_n factor of 4).

This screen tests the **necessary structural conditions** for that locking to be realizable
at all — existence, forcing, and color-transversality of the embedding 2O ↪ SU(2)_internal.
It is **purely finite-group + Lie representation theory.**

**M.CW ceiling, stated up front:** whether the energy-minimizer *realizes* the locking is a
metric/dynamical fact (which way the minimizer tips). Combinatorics cannot fix it. This screen
can therefore return only **possible / impossible / forced**, never "the locking happens."
A PASS greenlights the dynamical routes (2/3); it does **not** derive the locking, and it does
**not** settle the upstream Assignment I vs II question (that needs physics, not group theory).

---

## Decision scalars (locked)

- **D1 (quartet forcing).** Among the irreps of 2O in the **genuine/fermionic sector**
  (central element ↦ −Id), the number of 4-dimensional irreps.
  Interpretation: D1 = 1 ⇒ the factor-of-4 quartet is **forced** (unique); D1 = 0 ⇒ no
  fermionic quartet (NULL — the FR-sign route to spin-3/2 is dead).

- **D2 (transversality).** dim_ℂ of the commutant of color SU(3) (acting as 3⊕1) inside
  M₄(ℂ), and whether that connected commutant is non-abelian enough to host 2O.
  Interpretation: if the single-SU(4) commutant is abelian (U(1)-class), 2O (non-abelian)
  cannot live in it ⇒ the locked spin-SU(2) **cannot be hosted inside the color SU(4)** and
  must be a **separate transverse factor** (the tensor-product arena ℂ⊗𝕆⊗ℍ that §2.87.A
  already forced). Tensor-product transversality is verified by construction.

- **Auxiliary checks (not decision scalars, but reported):** ⟨χ_{3/2},χ_{3/2}⟩_{2O} = 1
  (the quartet is a single irrep), χ_{3/2}(−1) = −4 (FR sign present), and the
  integer-spin/bosonic sector central image (+) to confirm FR *selects* the fermionic quartet.

---

## Falsification arms (locked)

- **NULL (program-relevant):** D1 = 0 (no fermionic quartet) **OR** no transverse realization
  in any arena (single-SU(4) abelian-commutant fail **and** tensor-product fail). ⇒ the locking
  route to a derived μ_n is structurally dead; report and stop.

- **PASS-possible (expected, R2):** D1 ≥ 1 **AND** ≥ 1 transverse arena admissible. ⇒ the
  necessary condition is met; greenlight Routes 2/3; the *dynamical* locking is the remaining
  open content (M.CW-walled). If D1 = 1, additionally report **FORCED quartet**.

- The screen **cannot** return "the locking is realized" (dynamical fact, walled).

---

## Declared imports

- Group/representation theory **only**. No substrate metric, no GP dynamics, no I1–I3 ticket.
  The M.CW ceiling (R2) is a direct consequence.
- The structural premise "the spin/isospin SU(2) is a factor **transverse to color**" is the
  tensor-product structure §2.87.A already forced (the distinct-4 obstruction). It is an
  **input** to this screen, not a result of it.
- This screen does **not** distinguish Assignment I (spin in ℂ⊗ℍ) from Assignment II (spin in
  ρ₆-ℂ⊗𝕆); both adopt a transverse-factor structure and both are expected to pass NC1–NC3.
  The assignment remains upstream and open.

## Eddington guard

The spin-3/2 / factor-of-4 / μ_n = −3/2 target is the **object whose admissibility is screened**,
not a tunable parameter. No continuous parameter is fit. The numeric target (−3/2, the factor 4)
is referenced only in the final interpretation, never in any construction.

## Out of scope — surfaced, not settled (the sharp sub-condition)

**NC5 (baryon strand-permutation).** The §2.15 baryon is a 3-strand Borromean carrying color-3.
A spatial 2O rotation acts on the soliton's spatial configuration; if it permutes the three
strands, it induces an S₃ ⊂ SU(3)_color action — i.e. spatial rotation would leak into **color**,
breaking transversality for the baryon specifically. Whether it does is **geometry-gated** (where
the strands sit relative to the octahedral axes), an M.ONT / Routes-2-3 input, **not** decidable by
this pure-group screen. Flagged as the place a genuine obstruction could still live, and as direct
motivation for the Route-2 relaxed-core eigenproblem (you need the core geometry to know how
rotations act on the strands).

## Provenance

`g_2a_s1_screen.py` (chat-side first leg). Self-contained; reuses the proven 2O construction
from `gate2a_color_spin_transversality.py`. CC second leg to be an independent from-scratch build.
