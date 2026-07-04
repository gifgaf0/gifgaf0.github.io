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

---

## Addendum 1 (2026-07-02) — the which-4 gating check is DISCHARGED POSITIVE (SQT ledger read)

The gating check I said was required — and could not run from this repo (needs §2.85) — was
run by the SQT as a **pure ledger read** against §2.85 Parts A–E, §2.87, §2.87.A (V4.50
canonical). Both caveats discharge positive; `G_2a_S4_addendum1_which4_discharged.md` archived.

- **Caveat 3 (which 4):** it **is the spin-3/2 quartet** — §2.85 Part B puts μ_n's sign+magnitude
  in the "factor of 4 = spin-3/2 quartet as a single SU(2) irrep"; the color-4 alternative is
  excluded by §2.87.A's distinct-4 obstruction (R1). So my flagged tension is **resolved** — the
  ternary/Sym³ reading targets the right object.
- **Caveat 1 (neutron is spin-½):** the formula consumes the quartet via **exchange statistics**
  (color ε^{abc} antisym × fermionic total ⇒ spin-flavor symmetric ⇒ like-flavor diquark spin-1
  ⇒ the 4/3 vs −1/3), and the neutron's spin-½ is the **mixed-symmetry branch of the same
  Schur–Weyl decomposition** whose symmetric branch is the quartet. No mismatch.

**My decidable confirmations** (the parts not needing §2.85; `verify_discharge_decidable.py`):
- μ_p/μ_n = (4μ_u−μ_d)/(4μ_d−μ_u) = **−3/2** exactly (SU(6), the ledger's cited parameter-free
  ratio), **2.7%** from experiment — the "~3%" the ledger claims. The factor-of-4 is the
  numerator coefficient on the like-charge quark.
- Schur–Weyl branch structure (my spine, `verify_schurweyl_spine.py`): 4_sym quartet and
  (2+2)_mixed neutron are two branches of **one** (ℂ²)^⊗3 decomposition — caveat-1's structural
  core, **confirmed decidably.**

**Honest boundary (what I did NOT independently verify):** the *ledger reads themselves* —
§2.85 Part B's verbatim factor-of-4 identification, §2.87.A's distinct-4 obstruction, §2.85
Part E's K₇-tube ↔ §2.50 2π-C reduction — require sections that live in the **framework
project's canonical ledger, not this code repo**. They are recorded as **SQT-audited**, not
second-legged here.

**The relocation (M.CW — the import moves, it does not vanish).** The octahedral premise
entered *only* via §2.87's whole-soliton reduction (π₁(SO(3)/S₄)=2O, collective central −1) —
the route G-2a-S1/S2/S3 + V4.50 blocked. The exchange route supplies the same spinor phase
from **per-strand spinoriality + S₃ exchange + ε^{abc}**, with no collective octahedral
geometry — so the **tetrahedral cap is harmless** (the quartet lives in Schur–Weyl on
(ℂ²)^⊗3, not in a rigid octahedral rotor band). The import **relocates** from the blocked
whole-soliton octahedral premise to the **open §2.50 per-strand spinor gate** (canon's
"μ_n spinor-promotion gate"; same 2π-C structure as the electron's spin, a consilience worth
noting).

**Sharpened G-2a-S4 (still NOT pre-registered):** does each Borromean strand carry the §2.50
spinor half-period (per-tube-traversal −1 ↦ −Id)? *If yes* → Schur–Weyl forces the 4-dim
symmetric channel to be the irreducible spin-3/2 → μ_n → −3/2, **through the tetrahedral
geometry the baryon actually has.** Falsification arm: bosonic (+1) phase ⇒ spin content
unfixed ⇒ μ_n stays 0 (Part B dark-branch default). The decision scalar is a topological
per-tube phase, not a whole-soliton spatial-symmetry computation — the regime where the
octahedral obstruction does not live.

**Net (register unchanged everywhere).** G-2a-S1/S2/S3 and V4.49/V4.50 stand exactly as
filed; the octahedral blockage is real and stays banked. What changes is its **load-bearing
status for μ_n**: from "the sole route" to "one route, now bypassed in principle by the
exchange route, pending the open §2.50 per-strand spinor gate." The addendum derives nothing
new — it **re-routes the μ_n line from a blocked import to an open one** and shows the
octahedral import was never necessary for the *formula*, only for one *derivation* of it.
Still R3. My assessment: the gating risk I flagged is resolved positively and the object is
confirmed to be the spin quartet — the path is now clean and canon-native, but the per-strand
spinor phase (§2.50) is the real remaining gate, and existence≠magnitude (M.CW) still bounds
it to the −3/2 ratio, not the full number.
