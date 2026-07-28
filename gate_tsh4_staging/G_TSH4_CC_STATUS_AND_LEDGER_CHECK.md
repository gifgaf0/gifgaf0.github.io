# G-TSH4 — CC Status + V4.71 Ledger Verification (3rd dispatch)

**Date:** 2026-07-23 · **Auditor:** CC.

## §A. V4.71 canonical ledger — VERIFIED (now in hand)
For the first time the canonical `SQT_Master_Ledger_v4_71_CANONICAL.md` was delivered (previously in
`/mnt/project`, inaccessible). Integrity:
- **md5 = `9517f4fb7aa2de65b0b4a69985962d8f` — matches** the base referenced by the CDEF-1 fold
  authorization, the G-TSH4 pre-registration, both Phase reports, and the CC handoff. Authentic. ✓
- Content spot-check consistent with the CC audit trail: ANNEX-CDEF-1 present (7×), KNOB present
  (20×), §2.91.A–K present, G-TSH1/2/3 folded (17/9/10 mentions), no G-TSH4 (correctly under-gate). ✓

**Documentation inconsistency flagged (not a ledger problem):** `FOLD_AUTHORIZATION_V4_71.md` states
V4.71 size = **1,308,549** bytes (V4.70 1,295,979 + 12,570). The actual V4.71 file (same md5
`9517f4fb`) is **1,347,411** bytes — **+38,862 over the memo's figure**. Since the md5 is the binding
lock and it matches, the ledger is genuine; the fold-auth memo's byte-size line (and thus its
`+12,570` / reverse-splice byte-accounting) is internally inconsistent with the object it seals. Worth
a one-line correction to that memo for the record.

## §B. Standing blockers — persist for a THIRD dispatch
The CC handoff again lists what "travels" as (1) `G_TSH4_EXECUTION_PREREGISTRATION.md` (`e66b964d`,
LOCKED — the strain/shear conventions, cubic E4 direction sets, Q-A rule, F-ISO instantiations,
falsifier constants) and (2) Amendment-1 Part A. **Neither is attached** in this delivery (nor the
prior two). Consequently:
1. **The decisive Q-C / Route-S / Route-D leg cannot be validly second-legged.** Its comparison items
   (C3 elastic constants/curvatures, C4 Route-D slopes + mode-ID, C5 F-ISO instantiations) are defined
   by strain-mode and shear-deformation conventions that live *only* in the locked pre-registration.
   Building them blind would produce numbers that are not convention-matched to the chat leg — a
   pseudo-second-leg, not a valid C1–C6 comparison. (C44 in particular needs shear-deformation
   machinery that is exactly the locked instrument's content.)
2. **Phase-1/2 independence is broken.** The quarantined chat energies, C_ij, Route-D slopes, and the
   ANISO-3D verdict have now been exposed to CC three times. A Phase-1/2 leg I author cannot be blind.

## §C. What CC has delivered on G-TSH4 (the tractable, valid pieces)
- **Phase-0 independent recompute** (`G_TSH4_CC_PHASE0_REPORT.md`, committed): fresh solver, true-GP
  minima — Q-A ordering (AB<{FCC≈ABC}<BCC<AA) confirmed both kernels; hcp/fcc near-degeneracy ~1e-4
  confirmed (gap matches the polished report <0.3%); **F-3 arm-label defect independently confirmed**
  (ABC free-c/a→√6, ABC energy = FCC energy <2e-7); the **E5(b) straddle shown method-sensitive**
  (split-step puts gem8 below δ_E, true-GP puts both above) → supports E5b(a). This was robust to the
  exposure (deterministic, different method, landed a subtly different δ_E call).
- **Internal-consistency audit** of the Phase-1/2 material (`G_TSH4_CC_CONSISTENCY_AUDIT.md`,
  committed, 21/21): the chat leg's C_ij→speed, Zener, A_3D, hex F-ISO identity, Route-D
  static/dynamical cross-check, and mapper logic are all self-consistent. (Explicitly not an
  independent leg.)

## §D. The path to a valid decisive leg (recommendation, unchanged and now firmer)
The Q-C decisive content (fcc ANISO-3D / hcp near-ISO, the §2.88.B answer and the live Q3(1) splitting
stake) deserves a *real* second leg, and it is worth the heavy 3D compute — but only if it is valid:
- Dispatch a **fresh CC instance, blind**, with only the locked `G_TSH4_EXECUTION_PREREGISTRATION.md`
  (`e66b964d`) + Amendment-1 Part A in-band — no chat energies/verdict. It freezes its own Phase-0/
  Route-S/Route-D numbers, then C1–C6.
- If instead this (already-exposed) instance is to proceed, it must be recorded **non-blind /
  independence-caveated**, and it still needs the locked pre-registration for the strain/shear/mode-ID
  conventions or the comparison isn't apples-to-apples.

**Optional offer (not auto-run):** CC can produce a *convention-robust, large-signal* corroboration of
the decisive claim — the FCC cubic Zener anisotropy (A = C44/C′ via standard Voigt strain, both
kernels; the qualitative "fcc strongly anisotropic, hcp near-isotropic") — explicitly labelled
**independent physics corroboration in CC's own conventions, NOT the locked-instrument C1–C6 leg.**
Say the word if that's wanted despite the convention caveat; otherwise the decisive leg waits for the
locked pre-registration.

---
*CC status filed 2026-07-23. Ledger V4.71 verified (md5 authentic; fold-auth size line inconsistent).
Decisive Q-C leg blocked on the (thrice-undelivered) locked pre-registration; Phase-0 + consistency
pieces stand.*
