# B5 — The η / Flach item: purpose closed; a note is drafted (not sent)

**Plain-language summary.** The ledger still lists the η-invariant computation discussed with Flach as open. Its only purpose was to decide whether the internal geometry of the model fixes a Finkelstein–Rubinstein (FR) spin sign. That was settled at V4.84 by a different route: the 2π loop is contractible in the orbit, so there is no sign. A short note telling Flach this is drafted in `FLACH_NOTE_DRAFT.md`, for the author to send or not. The ledger row gets a bracket in the Phase B fold. Nothing was sent.

## What the ledger says

| Point | Ledger evidence (V4.92) |
|---|---|
| The computation's purpose | §2.87 (L1065): the FR sign is the parity of the APS η-invariant, which "unifies the μ_n factor of 4 with the S⁷/PSL(2,7) η-invariant thread (§G / the Flach problem)". The Part VI row (L4553), "Full Donnelly η-defect sum for the FR parity", is "Open … the Flach-correspondence computation". |
| The purpose closed | V4.84, Gate G-2a-A1 (§2.91.R; L1664): "π₁(Orbit) = 0 — the 2π-rotation loop is contractible in the collective-coordinate orbit: no spin sign from the substrate's internal geometry". |
| The space | S⁷/PSL(2,7), the seven-dimensional orbifold (§2.87; Part VI row; `addendum_target2_eta_reduction.md` §4 in the store, "η(S⁷/PSL(2,7)) = (1/168) Σ … Step (iii) over ℚ̄ is the Flach-correspondence computation"). ℙ¹(2,3,7) appears in the ledger only in the unrelated proton-radius thread (§2.82 area). |

Two actions of PSL(2,7) on S⁷ appear in the record. The PSL(2,7) note's Open Problem 4.4 strata fit only the 8-dimensional irreducible representation ρ₈ (§2.87, `verify_eta_action.py`), and the B2 v3 draft names that action. The store addendum's inputs used the octonion permutation action 1 ⊕ 7, which gives a different orbifold. The draft note says "a linear action" so it is right whichever one the original message meant.

## If the question was read as one about ℙ¹(2,3,7)

These are the brief's three points, stated in the note.
- **η vanishes.** On a two-dimensional orbifold the Dirac operator anticommutes with the chirality grading, so its spectrum is symmetric and η = 0.
- **Spin structure.** An orbifold spin structure needs each isotropy group ℤ/m to lift isomorphically into Spin(2). For even m both lifts of a generator have order 2m, so a cone point of order 2 obstructs it in the strict sense. The note says "may", because weaker conventions exist.
- **The meaningful version.** It lives on the Seifert three-manifold over ℙ¹(2,3,7), the Brieskorn sphere Σ(2,3,7).

## If the S⁷/PSL(2,7) number is still wanted

Donnelly's equivariant η is a finite sum over the conjugacy classes of PSL(2,7), built from the fixed-point data already on record (B2: fixed dimensions 4/2/2/2/2 for 2A/3A/4A/7A/7B under ρ₈). It can be computed in-house. It is no longer needed for μ_n.

## Ledger bracket for the Phase B fold

| Line | Entry | Bracket |
|---|---|---|
| L4553 | Part VI, "Full Donnelly η-defect sum for the FR parity" | Its purpose (an FR sign from the internal geometry) closed at V4.84 (§2.91.R: π₁(Orbit) = 0, no spin sign). No longer needed for μ_n; optional. The S⁷/PSL(2,7) η is a finite Donnelly sum, computable in-house. A short note to Flach is drafted (B5), not sent. |
