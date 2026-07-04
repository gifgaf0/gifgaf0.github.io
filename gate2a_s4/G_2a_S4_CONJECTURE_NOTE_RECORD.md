# G-2a-S4 — R3 Conjecture Note (code-repo record)

**Date:** 2026-07-02 · **Note:** `G_2a_S4_ternary_four_R3_conjecture_note.md` (SQT) ·
**Status: R3 EXPLORATION / CONJECTURE — idea-capture only.** Not a gate, not a fold, **no
register change.** The μ_n factor-of-4 stays a located/likely-blocked import (G-2a-S3). Kept
strictly separate from the audit-mode results (G-2a-S1/S2/S3); §2.52 untouched; M.BRIDGE
intact. Two-leg verification and the Prior Address Standard would be required before any of
the derivation route is banked past R3 — the note says so itself.

## What I verified — the decidable R2 spine ONLY (`verify_schurweyl_spine.py`)
The note's mathematical spine is textbook Schur–Weyl on three qubits; I confirmed it exactly:
- (ℂ²)^⊗3 splits as **4 (S₃-trivial) ⊕ 4 (S₃-std, = two spin-1/2 doublets)**; **sign rep
  absent** (Λ³ℂ² = 0).
- symmetric subspace: S² = 15/4 → **j = 3/2** — the quartet **is** Sym³(ℂ²), the totally
  symmetric (ternary) state of three doublets.
- std-isotypic: S² = 3/4 → two spin-1/2 doublets, mixed symmetry.

So the note's core reading is sound: the quartet is a **ternary** object (n=3 constituents,
dim Symⁿ = n+1) wearing a binary-looking dimension, and the missing S₃-sign rep is exactly
why ternary antisymmetry is exiled to color ε^{abc} — the Greenberg/Han–Nambu argument.
**All of this is standard, cited as prior art / motivation, not claimed as new** (the note is
explicit about that). Verified as R2-defensible.

## What I did NOT verify (correctly — it is R3 conjecture)
- The **exchange-derivation route** (derive the quartet from the FR strand-exchange phase +
  color sign, retiring the octahedral premise) — a candidate gate **G-2a-S4, NOT run**. It is
  a topological FR-phase computation to be pre-registered *only if* the gating check below
  passes.
- I did not invent any compute the note declines.

## The gating check — and why I can't discharge it here
The note's own caveat (3) [= (1)], flagged as **"the single biggest open check"**: is
§2.85's "factor-of-4" actually the Sym³ **spin-3/2** quartet (this note's object), or a
different 4 — the σ₄ half-spinor of Spin(6)=ℂ⊗𝕆 (Assignment I/II), or the color-4? There is a
real tension the record should not paper over: **μ_n is the neutron's magnetic moment, and
the neutron is spin-½** (the mixed-symmetry doublets), **not** the spin-3/2 quartet (the Δ).
The ternary-Sym³ reading is compelling *for a spin-3/2 quartet*; if §2.85's 4 is the neutron
moment, the reframing may be addressing the wrong object. Until that is disambiguated, the
conjecture's applicability is unestablished.

This disambiguation is a **pure audit step (no compute): read §2.85 against the note.**
**§2.85 lives in the framework project's canonical ledger, which is not in this code repo**
(`/mnt/project`, unmounted here) — so I cannot perform it from here. It is the correct next
action and it is the author's/SQT's to run against §2.85. Only if §2.85's 4 is the Sym³
quartet does pre-registering G-2a-S4 become worth it.

## Disposition (faithful)
Banked as R3 exploration in the Gate-2a cluster. No register change; the note offers a
*candidate alternative derivation* that — if it survives the which-4 disambiguation — would
relocate the factor-of-4 out from under the octahedral obstruction (which G-2a-S1/S2/S3 +
V4.50 closed against). Honest hedges carried: existence ≠ magnitude (M.CW — the exchange
route gives quartet *existence*, not the neutron-moment number); suggestive QCD-history
lineage is motivation, not derivation. Provenance: `verify_schurweyl_spine.py` (spine), the
archived note, and the cited standard rep-theory + QCD-history literature.
