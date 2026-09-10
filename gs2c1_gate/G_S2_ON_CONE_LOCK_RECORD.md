# G-S2C1 (display: Gate G-S2-ON-CONE) — LOCK RECORD

**Lock date:** September 2, 2026. **Authorization (verbatim, author):** "I authorize elections E-0 through E-8 under the default values specified in §6 of the staging memo. Proceed to lock the pre-registration byte-identical, mint `G_S2_ON_CONE_LOCK_RECORD.md`, freeze the T1 list, and execute Phase 0 (harness build, validation, and positive controls F-CTRL-L / F-CTRL-INJ). … Do not proceed to Phase 1 (the single-crystal ka-ladder fit) without explicit authorization."

## Locked artifacts

| Artifact | md5 | bytes | Status |
|---|---|---|---|
| `G_S2_ON_CONE_EXECUTION_PREREGISTRATION.md` | 2ea8ec13ffa3c32898cc24a3be605c64 | 12,984 | LOCKED — byte-identical (cmp) to the approved `staging_memo_G_S2_ON_CONE.md` |
| `t1_forbidden_G_S2_ON_CONE.txt` | 8cd89b9a82704accd89f7ff6f5e220b4 | 144 | FROZEN — 16 pattern lines, pattern-lines-only (H-2 rule) |

## Elections (T3-immutable from this record)

- **E-0** gate name **G-S2C1**; display name "Gate G-S2-ON-CONE".
- **E-1 (b)** substrate scope: single crystal + polycrystalline aggregate.
- **E-2** S2 channel: E₂/quadrupole (traceless-strain) projector under C₆ᵥ; overlap threshold θ_id = 0.90; ω₂(k) = the branch of maximal overlap.
- **E-3** kernel family for c_T: gem8 primary (g* = 20, a* = 1.46059, μ = 53.225, ρ₀ = 1, substrate units); gem4/gem3 as reported sub-annotations; no cross-kernel averaging (KNOB discipline, F3-class).
- **E-4** k-window ka ∈ [10⁻³, 0.3], dyadic ladder, fit basis {(ka)², (ka)⁴}, both symmetry directions Γ–M and Γ–K.
- **E-5** zero-thresholds |a₂|, |a₄| < 10⁻⁶ at the two-leg CI; θ_iso = 1%; F-CONV per-quantity thresholds fixed at Phase-0 close (see the Phase-0 report).
- **E-6** leg architecture: chat leg = projector + ladder + fits on the instantiated BdG stack; CC leg = full-from-scratch independent BdG + own projector + own fitter; comparator frozen pre-return; S9 on any miss.
- **E-7** consequence routing PF-S2 as prereg §1/§5: A1 ⇒ W_∪ REINSTATED; A2/A3 ⇒ W_∪ stays suspended, W_∪′ re-derived from the measured dispersion scale (retire if empty); A4 ⇒ GW-side of CI-W VOID; A5 ⇒ no verdict.
- **E-8** dispatch discipline: P-4 in-band with P-4.b base64 armor on all quarantined embeds (first gate under the amendment).

## Registered expectation (pre-data, Eddington trap 4)

M-naive expectation: **DISPERSIVE** (Gu–Wen helicity-±2 lattice modes disperse as k³; Stanke–Kino/Weaver shear-branch phase-velocity dispersion nonzero at second order). A1 ON-CONE-EXACT would be the surprising outcome; A2/A3 the expected ones. Registered so that no outcome can be spun.

## Phase gating

Phase 0 (harness build, validation, F-CTRL-L, F-CTRL-INJ, C-NEG engine validation) AUTHORIZED and executed under this lock. **Phase 1 (single-crystal ka-ladder fit — crystallization + Bloch-BdG on the crystal) NOT AUTHORIZED**; the harness carries a hard activation flag `PHASE1_AUTHORIZED = False`.
