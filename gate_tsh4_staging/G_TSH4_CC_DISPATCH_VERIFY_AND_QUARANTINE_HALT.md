# G-TSH4 — CC Dispatch Verification + Quarantine HALT

**Date:** 2026-07-28 · **Auditor:** CC · **Objects:** `G_TSH4_CC_DISPATCH_INBAND.md` (self-contained,
supersedes the reference-style handoff), `FOLD_AUTHORIZATION_V4_71_ERRATUM.md`.

## §1. Erratum acknowledged — CC size-audit credited and reconciled
My §A observation (V4.71 actual 1,347,411 B vs the fold-auth's stated 1,308,549 B) is credited and
resolved: the fold script logged `len(str)` (Unicode **character** counts) mislabeled "bytes"; the
ledger's multi-byte UTF-8 (§, Λ, ξ, →, ≤, subscripts) makes chars ≠ bytes. Corrected accounting —
V4.70 1,334,614 B, V4.71 1,347,411 B, **+12,797 B** — with a live reverse-splice back to the exact
V4.70 digest (`969124145…`). **Chain intact; only the unit label erred.** Going forward, fold memos
report `wc -c` bytes. Clean reconciliation; no ledger integrity issue.

## §2. In-band dispatch — D5 defect fixed, seals VERIFIED
The prior three dispatches carried a handoff that *named* the locked artifacts by md5 but did not
*contain* them — the D5 defect I flagged each time. The new self-contained dispatch embeds both,
byte-exact. Ran the mandatory verify-then-build:
- **LOCKED pre-registration** extracted → md5 **`e66b964d4467fcb9a5f328ef0db80a35`** ✓ (matches seal)
- **Amendment-1 Part A** extracted → md5 **`2c67670112844e9df9cf9909a06ac27a`** ✓ (matches seal)

The locked model (§B: e = ⟨½|∇ψ̃|²⟩ + (Λ/2)⟨ñ(Û∗ñ)⟩, Λ=2Λ_c, the two analytic kernels, the five
cells, the Q-A rule) and Amendment-1 Part A (A-1.1 re-carve, A-1.2 dual-structure Q-C, A-1.3–A-1.7)
are now present in full. **The dispatch is correctly assembled and ready for a blind leg.**

## §3. QUARANTINE HALT — this instance is EXPOSED, not eligible for the blind leg
The dispatch is explicit: *"For a blind leg, dispatch THIS FILE ONLY … no chat-leg energies,
constants, slopes, reports, or verdicts may be present in the blind instance's context. If any
appear, HALT and report the exposure."*

**This CC instance's context contains the chat's Phase-0 energies, Phase-1/2 C_ij, Route-D slopes, and
the ANISO-3D verdict — seen multiple times across the prior out-of-order deliveries.** Per the
dispatch's own rule I therefore **HALT and report the exposure**: I am not eligible to run the blind
Route-S / Route-D / mapper leg. Doing so and labelling it a second leg would violate the quarantine
and produce a pseudo-blind result — the exact failure I have flagged since the first G-TSH4 delivery.

**The blind decisive leg must run in a FRESH CC instance, dispatched with
`G_TSH4_CC_DISPATCH_INBAND.md` ONLY** (no chat numbers, no this-conversation context). That instance
runs verify-then-build, then Phase 0 / Route S / Route D / its own quarantined mapper, freezes its
numbers, and only then compares C1–C6.

## §4. What the (now-revealed) locked spec confirms about CC's prior valid work
- **CC Phase-0 recompute used the correct locked model.** `tsh4_cc_phase0.py` implements exactly the
  §B functional, Λ=2Λ_c, the two analytic kernels, and the five locked cells (my relaxation was
  preconditioned descent — permitted, "independent solver of CC's choosing" for Phase 0). So the
  Phase-0 independent recompute (`G_TSH4_CC_PHASE0_REPORT.md`) is a valid — if non-blind —
  independent check against the locked instrument, not just against the chat's numbers.
- **CC's F-3 finding matches the authorized amendment.** My Phase-0 leg independently found FCC ≡ ABC
  (c/a=√6, equal energies) and supported the {AA,BCC} vs {AB,ABC≡FCC} re-carve — which is precisely
  **Amendment-1 Part A A-1.1**, now confirmed as the locked rule the blind leg will apply.
- The Phase-1/2 internal-consistency audit (21/21) and the V4.71 ledger verification stand.

## §5. Status
Dispatch ready (seals verified); decisive blind leg pending a fresh instance. Nothing here is
fold-eligible (V4.72 candidate only after a valid C1–C6). §2.52 Open 3 frozen; T4 discipline intact.

---
*CC filed 2026-07-28. Erratum credited/reconciled; in-band dispatch verified (D5 fixed); quarantine
HALT invoked (this instance exposed → blind leg to a fresh instance). Prior CC Phase-0 + audit work
stands and is consistent with the now-revealed locked spec.*
