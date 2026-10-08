# C2 pre-registration: the annotation batch (decision rules fixed before any check)

**Plain-language summary.** The brief's item C2 lists about twenty corrections to fold as annotations, with the instruction "Verify each item first." Most are factual slips: a wrong count, a wrong angle, a misread prior source. A few would downgrade or reverse an entry. This file fixes, before any check runs:
- how each item will be checked;
- what result leads to which annotation;
- which result stops an item instead.

Nothing goes into the ledger unless its check confirms it.

**Locked:** October 7, 2026, by commit, before any C2 computation. Source: the brief of October 6, item C2, and the audit findings of the same date (leads, to be verified).

## Rules that can downgrade or close something

| Item | Check | Decision rule |
|---|---|---|
| **P1. ζ-tax gate 3** (Part VI, "cosmological redshift framing commitment … with stated falsification gate") | Read the banked entry's own mechanism. Confirm DES's measured light-curve stretch exponent b from the paper. | **CLOSED: FAILED** if the banked entry makes the redshift a per-vertex amplitude penalty on the photon (Φ_out = Φ_in(1 − ζ)) with no change to emission and arrival intervals. That is the tired-light class of the welding lemma (G-FOLD1, R1), which predicts b = 0, against DES's b ≈ 1. A frame or metric recast is recorded as the only admissible alternative, and it abandons the amplitude mechanism. If the entry admits a time-dilating reading, the verdict is not FAILED; annotate the framing only. |
| **P3. §2.50.A, OP-2.14, G-QUANTA** | Read G-VS1 (§2.91.U) and §2.92.B for π₁ and the elementary winding at the vacuum of record and on each stratum. | If π₁ = 0 at the vacuum of record, the elementary winding is π on the polar strata, and 2π only where ψ₀ carries weight, then annotate **CONDITIONAL**: §2.50.A's 2π trap, OP-2.14's closure, and G-QUANTA's electron-2π and K₇-vortex PASS rows. Each holds only on a ψ₀-weighted vacuum (import I6, not forced). Otherwise annotate nothing. |
| **P4. μ_n** | Compute the quark-model magnetic moments exactly, from explicit three-quark spin⊗flavour states: p, n (spin ½), and the fully symmetric spin-3/2 states (Δ). | **DOWNGRADE** the identification "the factor of 4 = the spin-3/2 quartet" (§2.85 Part B, the μ_n spinor-promotion gate row, and the §2.87 unification sentence) if both hold: μ_p = (4μ_u − μ_d)/3 comes from the spin-½ coupling weights (⟨σ_z(u₁) + σ_z(u₂)⟩ = 4/3), and μ(Δ⁰) = μ_u + 2μ_d = 0 for μ_u = −2μ_d. The quartet programme then targets the Δ. Otherwise annotate nothing. |
| **M-rev. Math items that reverse an R1/Tier-2 statement** (the 42 size-2 matchings; §2.62.C's V₄ stabiliser; "PSL(2,7) does not act on 𝒴" against signed lifts; the §2.68.8.1 argument behind OP-2.67.1b(ii) "CLOSED"; §2.77's "inner" involution and the M₄(ℂ) span) | Exact computation from the ledger's own definitions. | Annotate as a correction of record if the computation contradicts the entry as written. If the computation agrees with the entry, or the entry's definition cannot be pinned, annotate nothing and say so. |

## Rules for annotation-only items

| Item | Check | Rule |
|---|---|---|
| **P2. Polycrystal** | Compute W^EM_∪'s edge divided by a_phys over the declared band. Read G-SCALE1's declaration scope. | Annotate the cells-per-grain range and the effect of a grain ≫ lattice floor. State what licenses ξ = ℓ_P on the transverse line, from the ledger's own record. No verdict. |
| **P5. §2.52 Open 3** | Read G-ζ1's verdict (§2.88.D.1). | Add the G-ζ1 result to the frozen row. The freeze stays in place, as the brief says: "Add the G-ζ1 result, and leave the freeze in place." This is the first fold authorised to touch that row, and only by appending. |
| **M. Remaining math corrections**: OP-2.81.1/2 by Moreno's criterion; K₈'s 1-factorizations; arctan(1/√2); log(4π)/log 7; §2.84A's labelling coincidence; OP-2.74.1c.i; the de Marrais pointers (§2.55, §2.68.4, §2.41.B); the α⁻¹ entries | Direct computation, or the cited literature for attributions and published counts | Annotate if confirmed; otherwise not. |

## Legs

- **Second leg.** Each check that decides a downgrade, a closure or a reversal (P1, P3, P4, M-rev) gets an independent recomputation of the decisive fact. For P1 and P3 the decisive facts are quotations from the ledger and DES, so a second reading suffices. For P4 and M-rev, a second computation is required.
- **One leg.** Everything else is an annotation, checked once.
- **Disagreement.** If two checks disagree, the item is not annotated and the disagreement is reported.
