# G_CI1_LOCK_RECORD_ADDENDUM_1.md — Addendum 1 to the G-CI1 lock record (append-only; the lock record `a6adbb6ab69bcc6184b8fc2f6bcb9f5b` is unmodified)

**Date:** August 18–19, 2026. **Base lock:** pre-registration `6c480340` LOCKED; T1 list `653a0b74` FROZEN; sealed file `dd8fe2d3` SEALED (census 12, UNOPENED); lock record `a6adbb6a`; Phase 0 CLOSED (`ci1_phase0.json` `b0498568`, A0 NOT TRIGGERED). This addendum is a T1-scan-EXEMPT embed of the lock-record class (it carries the author's directive text verbatim).

## A1.1 — PF-6 / PF-7 discharge (X-1 byte provenance)
`poly_vrh_results.json` md5 `200e7a8b775577564369c6924d38a84c` (2,767 B) — PASS. `G_POLY1_PIN_RECORD.md` md5 `621120e50d395beea2e914d54c929600` (10,759 B) — PASS. Verification checkpoint `ci1_resupply_verify.json` md5 `d99d21b2bc15d9f0075ee9d00e6c69d8` (1,835 B). Neither fallback invoked. Author acknowledgment: "The PF-6 and PF-7 re-supply verifications are confirmed. The byte-exact provenance is acknowledged."

## A1.2 — Author's directive (VERBATIM)

> **Directive: Acknowledge Resupply and Authorize Phase 1 (I-1 Irrep/Helicity Audit)**
> The PF-6 and PF-7 re-supply verifications are confirmed. The byte-exact provenance is acknowledged.
> For the Phase 2 items:
> 1. I authorize a specific T1-exemption line for the `G_POLY1_PIN_RECORD.md` embed in the CC dispatch due to the legacy Aluminum benchmark token.
> 2. I elect to leave the ray-regime attenuation VOID by default. We will not pin a new prior-art form; widening the window is the conservative and honest path.
> I authorize the execution of Phase 1 (I-1 irrep/helicity audit) on the chat leg.
> 1. Execute the R-a machine check to verify the helicity content of the transverse displacement channel and its derived strain/stress fields.
> 2. Execute the R-b inventory across the banked G-TSH4 and G-INT1 sectors for any ±2 content degenerate with the acoustic cone.
> 3. Form the candidate set K and render the F-IRR decision.
> 4. Record all findings and the F-IRR verdict in `ci1_phase1.json`.
> Report back with the Phase 1 checkpoint and the F-IRR verdict.

## A1.3 — Elections recorded (T3-immutable from this addendum)
- **E-10 (dispatch embed exemption):** the CC dispatch `G_CI1_CC_DISPATCH_INBAND.md` carries the frozen `G_POLY1_PIN_RECORD.md` byte-exact as a **third declared T1-scan-exempt embed** (justification: frozen upstream input, byte-exact by requirement; its single hit is the SI velocity-unit token of the He-2 aluminium benchmark control line, source-marked "SI units in this control only", not consumed by G-CI1). All other dispatch content remains T1-scanned.
- **E-11 (ray-regime attenuation):** VOID by default (§5.4); no new prior-art form is pinned; a VOID can only widen a window.

## A1.4 — Phase 1 (chat leg) closure
Instrument `g_ci1_phase1_irrep_chatleg.py` md5 `b5715bf62189c9f2105e451e396c21ce` (23,236 B); checkpoint `ci1_phase1.json` md5 `9d8e40b827f68d354335c2a147420636` (218,006 B); T1 zero hits on both; inputs: `poly_vrh_results.json` (byte-verified) as the E-7 tensors; 35 directions (13 lattice incl. axial/basal/oblique, 2 hex in-plane, 20 Fibonacci); θ ∈ {0.1, 2π/7, 2π/5}; τ_h = 1e-12. **F-IRR: FIRES (K = ∅) — CI-S FALSIFIED-STRUCTURAL; the CI-W arm activates; CI-W/EM-IN operative (PF-2); W_∪ doubly conditional and SUSPENDED from the Phase-3 intersection (PF-1, fold-time annotation).**

## A1.5 — Honesty ledger continued
**G-CI1.H-4 (interpretive item, author veto standing; the G-TSH3 D-3 pattern).** The R-a machine check confirms the pre-registered priors for the D-1 channel and for the strain of every plane wave (the ±2 strain component vanishes identically; machine max 4.6e-16) and for the isotropic aggregate stress (5e-16), but the derived STRESS of single-crystal qT branches carries anisotropy-induced ±2 kinematic components at generic directions (nonzero on 58/70 hex and 49/70 cubic branch-directions; max fraction 0.27–0.47 of the stress norm; zero at the axial and pure-mode directions). The F-IRR verdict of record is rendered under the D-4 first-clause reading (a branch's helicity content = the eigenphase multiset of its mode's polarization/orbital data; derived-field eigenphases are kinematic labels), consistent with D-6's "excitation". Under the alternative reading (derived-stress labels counted as branch content) the transverse pair — DEGENERATE by definition as the channel — would make K non-empty; that reading would also make every anisotropic elastic medium trivially "host ±2", emptying the B-3 burden. **Ratification of the reading of record is requested from the author; the verdict is T3-immutable only after ratification.**
**G-CI1.H-5 (process).** Two chat-side serializer defects (numpy scalar types) fired at first execution and were fixed before any output was consumed; no numerical content affected; recorded.

## A1.6 — What opens next
Phase 2 (I-2 regime map + I-3 residual ledger; containment 2.1 opens the phase) is branch-independent and opens on the author's word; the E-11 VOID election and the E-10 exemption apply at Phase-2 open. Phase 3 (sealed mapper, CC-blind-first) is steered by the ratified F-IRR verdict.
