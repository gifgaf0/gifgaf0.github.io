# G_CI1_LOCK_RECORD.md — Lock record for Gate G-CI1 (the Q3(1) Carrier-Identity Claim)

**Lock executed:** August 17, 2026 (Pacific), 2026-08-18T00:21Z (container UTC). **Lock authority:** the author's explicit freeze word of August 17, 2026 (reproduced verbatim in §3). **This file is a T1-scan-EXEMPT embed** (one of exactly two: this lock record and `anchors_G_CI1_SEALED.md`), because it carries the author's election text verbatim, which contains observational-dialect tokens by design (the two-document convention of the pre-registration header).

## §1 — Lock chain (byte-anchored)

| Artifact | md5 | bytes | status |
|---|---|---|---|
| Base canonical `SQT_Master_Ledger_v4_76_CANONICAL.md` | `f539d10cb4f73c81e7d9fdbe7fa63714` | 1,432,221 | re-anchored at lock (§13.1 of the pre-registration): V4.76 is the current canonical; no later canonical exists |
| Staging memo `staging_memo_Q3_1_carrier_identity.md` | `ca6d891f51c425bd46ffbb1dee4e45f8` | 30,363 | APPROVED (author, August 17, 2026); not amended |
| Pre-registration `G_CI1_EXECUTION_PREREGISTRATION.md` | `6c480340658a54e9da5d3553a8890c46` | 36,793 | **LOCKED byte-identical to the reviewed draft** (the author's confirmed md5); its header text reads "DRAFT — NOT LOCKED" by construction of byte-identity; this record is the lock (the G-POLY1 / G-2a-S8 precedent) |
| T1 forbidden-string list `t1_forbidden_G_CI1.txt` | `653a0b7447e68aa8a094e62337a24da3` | 1,127 | **FROZEN byte-identical** to the reviewed draft `t1_forbidden_G_CI1_DRAFT.txt` (same md5); 78 case-sensitive regex lines; header text says DRAFT by construction of byte-identity |
| Sealed anchor file `anchors_G_CI1_SEALED.md` | `dd8fe2d364624750201ad9c9ffef575c` | 17,652 | **SEALED at lock** (second and final seal; the first seal 6cdf147d / 17,694 B superseded before any instrument touched it — G-CI1.H-3 below); census = 12 rows (4 TR + ACH-DIM + ACH-DISP + BIR-1 + BIR-2 + POL + DIFF + VLD + CONV); pipe-safe (10 separators per row, no pipe outside table rows), superscript-free (E3-6(a) semantics never engage); UNOPENED by any instrument before Phase 3; md5 + census asserted at every open |

**T1 self-scan of the pre-registration against the frozen list (case-sensitive, the declared discipline): 0 hits** — recorded also in `ci1_phase0.json`. Transparency note: a case-insensitive scan returns exactly one collision, the satellite token `INTEGRAL` against the ordinary mathematical word "integral" (pre-registration line 207); this is precisely why the list is declared case-sensitive; no change was made.

## §2 — Author's election directive (VERBATIM; the E-0…E-9 text of record)

> **Directive: Authorize Staging Memo and Elections for G-CI1**
> The staging memo is approved. The B-3 (helicity/irrep) burden discovery is a critical and correct structural catch. The CI-S vs CI-W differentiation is ratified.
> I authorize the following elections:
> * E-0: Gate name G-CI1 is adopted.
> * E-1: (a) Aggregate isotropized transverse acoustic channel as referent.
> * E-2: CI-S and CI-W definitions adopted and T3-immutable.
> * E-3: Scope restricted to radiative sectors; matter-sector routed to named successor.
> * E-4: Phase-1 R-b policy adopted (inventory only, no new model construction).
> * E-6: Gauge-paper firewall maintained.
> * E-7: Kernels {step, gem8}, hex primary + cubic labelled.
> * E-9: CC full-from-scratch; CC-blind-first for Phase-3 read.
> **For E-5 (Sealed-anchor roster):**
> Proceed with A-EM-TRANS, A-ACHROM, A-BIR-EM, A-POL, and A-DIFF. For the A-EM-TRANS ladder, include Radio, Optical, X-ray, and VHE γ-ray (e.g., H.E.S.S.) rungs to ensure maximum regime coverage.
> Draft the pre-registration (`G_CI1_EXECUTION_PREREGISTRATION.md`), including the exact thresholds and tolerances for E-8. Do not lock or execute Phase 0 until I explicitly authorize the freeze.

**Election E-8** is carried by the locked pre-registration §5 and confirmed by PF-4 below. **Dialect-label dictionary for the sealed roster** (the pre-registration uses abstract labels): TR-1 = the author's "Radio" rung (realized at seal as a low-frequency radio-galaxy detection at 150 MHz, redshift-anchored — the longest-wavelength band of the roster, chosen for maximum regime coverage at the long-wavelength end; the CMB monopole spectrum is carried by the ACH-DIM row instead); TR-2 = "Optical"; TR-3 = "X-ray"; TR-4 = "VHE γ-ray (e.g., H.E.S.S.)" (realized as the H.E.S.S. 1ES 1101-232 spectrum, per the author's example).

## §3 — Author's freeze directive and pre-lock-flag resolutions (VERBATIM)

> **Directive: Freeze G-CI1 Pre-registration and Authorize PF Resolutions**
> The T1 draft list md5 (`653a0b7447e68aa8a094e62337a24da3`) and the G_CI1_EXECUTION_PREREGISTRATION.md draft md5 (`6c480340658a54e9da5d3553a8890c46`) are confirmed.
> I explicitly AUTHORIZE the lock and FREEZE the pre-registration byte-identical to the reviewed text against V4.76.
> **Pre-lock Flag Resolutions (to be written verbatim into the lock record):**
> * PF-1 (Blast Radius): Acknowledged and amended as written. If F-IRR fires, W_∪ becomes doubly conditional; under CI-W/EM-IN it is SUSPENDED from the intersection.
> * PF-2 (CI-W Branching): Confirmed as written (EM-IN operative; EM-OUT author-declared; S2-IN defined).
> * PF-3 (CI-V Naming): Confirmed. CI-V is named-not-adopted and foreclosed by E-2.
> * PF-4 (E-8 Numbers): Confirmed as written (τ_h 1e-12, θ₁/θ₂ 3%/10%, containment 1e-6, Born exponent 4.00 ± 0.02, x_grid half-decade, etc.).
> * PF-5 (Census 12): Confirmed.
> * PF-6 (JSON Re-supply): Confirmed. I will re-supply `poly_vrh_results.json` `200e7a8b` before Phase 2.
> * PF-7 (Pin Record Re-supply): Confirmed. I will re-supply `621120e5` before Phase 2; fallback to verbatim re-retrieval.
> Execute the lock sequence:
> 1. Re-anchor to V4.76.
> 2. Mint `G_CI1_LOCK_RECORD.md`.
> 3. Draft, hash, and seal `anchors_G_CI1_SEALED.md` (census 12, T4-quarantined).
> 4. Open Phase 0.
> Report back with the lock hashes and the Phase 0 readiness status.

**Reading of PF-1 "acknowledged and amended as written":** the author's restatement is identical in content to the pre-registration §9.2 / §12 PF-1 text (doubly conditional on F-IRR firing; SUSPENDED from the intersection under CI-W/EM-IN); no textual amendment to the pre-registration was required or made (byte-identity preserved); the resolution is recorded here as ACKNOWLEDGED. PF-2, PF-3, PF-4, PF-5: CONFIRMED as written. PF-6, PF-7: CONFIRMED with the author's re-supply commitments before Phase 2; the pre-registered fallbacks stand.

## §4 — Elections in force (T3-immutable from this lock)

E-0 G-CI1; E-1(a) aggregate isotropized transverse acoustic channel; E-2 CI-S/CI-W definitions D-6/D-7 T3-immutable (D-8 CI-V named-not-adopted, PF-3); E-3 radiative sectors only, matter-sector successor G-CI2 named; E-4 R-b inventory only; E-5 roster A-EM-TRANS (TR-1…TR-4) + A-ACHROM (2) + A-BIR-EM (2) + A-POL + A-DIFF, sealed as census 12 with VLD + CONV; E-6 gauge-paper firewall; E-7 kernels {step, gem8}, hex primary + cubic labelled; E-8 §5 numbers as locked (PF-4); E-9 CC full-from-scratch, CC-blind-first Phase-3 read (CC read #1 = the blind read of record).

## §5 — Sealing statement and honesty ledger opening

**Sealed-file provenance.** Every quantity in `anchors_G_CI1_SEALED.md` was retrieved from its named published source at seal time and transcribed; four in-row items that were not verbatim-retrieved from the anchor source (a nominal last-scattering redshift, a representative optical filter wavelength, two instrument band brackets) are marked [RECALLED-FLAG] inside the sealed params and each carries a pre-declared conservative two-reading rule (exclusion asserted only where both readings exclude). No sealed quantity was evaluated against any curve at seal time; the Phase-1/2 instruments are pre-registered in closed form and consume no anchor.

**G-CI1.H-1 (process disclosure, chat leg, at lock).** The chat leg drafted the sealed file at lock, as the procedure requires (§13.3); the chat leg's Phase-3 blindness is therefore procedural — enforced by T1 (tokens), T4 (no SI outside the sealed file and mapper), the M-1…M-5 masking discipline, the pre-registered closed-form Phase-1/2 instruments, and the E-9 CC-blind-first architecture in which CC read #1 is the verdict read of record — not an information barrier. This is the same disclosure class as G-POLY1.H-8; recorded at lock, before any computation.

**G-CI1.H-3 (re-seal disclosure, at lock, before Phase 1).** The first sealed file (md5 6cdf147d8b96f89dc3c6c45b321aa66c, 17,694 B) realized TR-1 as the CMB monopole (microwave/mm-wave). On seal review — before Phase 1 opened and before any instrument had opened the file — TR-1 was re-realized as a 150 MHz radio-galaxy detection (a longer wavelength by two decades, redshift-anchored) to honor the author's E-5 wording "Radio" and the maximum-regime-coverage instruction; the CMB monopole spectrum remains the ACH-DIM row. The file was re-sealed (md5 dd8fe2d364624750201ad9c9ffef575c, 17,652 B; census 12 unchanged; structural checks re-run) and Phase 0 was re-run against the final seal. The superseded seal is not consumed anywhere.

**G-CI1.H-2 (hygiene note, at lock).** The frozen T1 list and the locked pre-registration carry the word "DRAFT" in their headers by construction of byte-identity with the author-confirmed hashes; the lock status is established by this record, not by the files' header strings.

## §6 — What opens now

Phase 0 (definitions, checklist, final A0 pass, sealed md5/census assert, T1 zero hits) opens on this lock and closes to `ci1_phase0.json`. Phase 1 opens only after Phase 0 closes with A0 NOT TRIGGERED. Nothing else changes: §2.52 Open 3 untouched; §2.87.J reserved; OP-2.58.2d and P-LEX-1 standing.
