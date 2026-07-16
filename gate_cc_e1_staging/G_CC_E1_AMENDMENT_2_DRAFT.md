# G-CC-ε1 — AMENDMENT 2 (DRAFT — staged for author authorization)

**Amends** the locked pre-registration (md5 `e3afcbd6f23bd483861a07f896e8d6b7`) **and Amendment 1** (md5 `a09f6fc992cc185f62ce84fcdbadc012`) under the §8 protocol. **Trigger:** the A1.1 D1b(iv) wake decomposition was **machine-falsified in execution** (chat leg md5 `7ad7fbd2a8a22f990b48f31ea1cd50e0`, D1b.3; halt report md5 `a3e9b22e9af0065be87ac5c7b34648bd`) — the relative-flow stress term was omitted. This amendment adopts the banked identities T2–T5 as registered structure and conditions the flow-channel classification on the ANNEX-VC-1 declaration. **Execution resumes only under the complete set {lock + A1 + A2 + VC declaration}; the CC leg dispatches only then.**

---

## A2.1 — The corrected wake decomposition (adopts T2, T3, T4)

The registered decomposition becomes, per the exact two-fluid identity Σ_c ρ_c u_c⊗u_c = J⊗J/ρ_tot + (ρ₁ρ₂/ρ_tot)Δu⊗Δu:

  **P_wake = ε²·P_mono + ε_J²·P_J + P_rel + P_cross**,

where P_mono is the density-monopole channel (D1a, exact ε²·S_shape factorization); P_J the net-current quadrupole (controlled by ε_J); **P_rel the relative-flow (spin-sector) quadrupole — winding-EVEN, unsuppressible by counter-winding, with support = the component overlap ρ₁ρ₂/ρ_tot** (interface-localized on the immiscible branch, overlap integral = w/2 exactly for the tanh step); P_cross bounded by Cauchy–Schwarz from the diagonal terms. A1's ε_J definition and D1b(i)–(iii) stand unchanged; only the (iv) formula is superseded.

## A2.2 — VC-branch conditioning (adopts T5)

The flow channel's far field carries the topological floor Σρ_cu_c²|_far ≥ (κ/2πr)²·w₁²·ρ₁∞. The derivation phase is **VC-branch-agnostic** (all maps and floors computed regardless); the **classification and comparison consume the ANNEX-VC-1 declaration**: under **VC-A** (ρ₁∞ > 0) the flow channel enters the comparison as an order-one term with no residual parameter — recorded as such, not smoothed; under **VC-B** (ρ₁∞ = 0) P_J and P_rel are core-localized and enter through the (ε_J, overlap) maps; the VC-B-S1 stability item (the annular winding carrier) registers as a named follow-on gate, not assumed.

## A2.3 — D2/D3/D4 extensions

**D2:** deliver **three maps** over (η, ν; w₂): ε, ε_J, and the **overlap map** O ≡ the normalized ∫(ρ₁ρ₂/ρ_tot)|Δu|²-weight of P_rel; F1/F2 variational families + independent numerics as locked. **D3:** floors for all three — ε_min (F4-anchored, as locked); the ε_J amplitude-matching floor (as A1); the **overlap floor** (immiscible-branch interface bound; on the miscible branch the coexistence-region bound, honestly reported if no floor exists — the locked NO-FLOOR clause extends to O). Under VC-A the topological floor is a **constant of the configuration, not floorable** — recorded, not optimized. **D4:** the dimensional-closure audit runs per channel (three CLOSED/SURFACE/WALLED classes), KC3-blind as locked.

## A2.4 — Comparison step

Unchanged in discipline (thresholds in one function, run last, both legs). It consumes **the triple (ε, ε_J, O) + the declared VC branch** through the three D4 forms. **ARM B (kill) fires only on the joint floor of all admissible channels, parameter-free within the admissible region**; under VC-A, if the order-one flow term admits no satisfying region under any admissible import, the comparison reports the Arm-C shape as found — pre-stated here, not prejudged.

## A2.5 — Honesty and process

A1's D1b(iv) formula was chat-side drafting, author-authorized, and machine-falsified by its own registered falsifier — logged (halt report §3, item 3) alongside the two smaller chat self-catches (D1a.1 normalization; D1b.4 assert target). The three banked D1 theorem sets (T1–T5) are adopted as registered structure and are **not re-derived** by the resumed chat leg; the CC leg derives them independently per the two-leg rule. The V4.65 annotation flag extends: the annex consequence line's eventual additive annotation reads KC3 as bounding **the triple** under the declared VC branch.

## A2.6 — Authorization

This amendment supersedes A1.1's D1b(iv) formula, adopts T2–T5 as registered structure, extends D2–D4 to three channels, and conditions classification on ANNEX-VC-1. Nothing else changes. **On authorization this document freezes (md5 recorded); execution resumes under {lock e3afcbd6…, A1 a09f6fc9…, A2 md5, VC declaration}.**

*Drafted July 15, 2026, chat leg.*
