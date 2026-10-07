# Phase A report: kill surfaces (October 6–7, 2026)

**Plain-language summary.** Phase A tested the four places where the October 6 audit said the program could break. All four broke, in different ways.
- The medium has no carrier for gravitational waves.
- Its hidden internal waves drag on any twisted-texture matter.
- The proton ropelength check fails by the ledger's own rule.
- Neither static picture of gravity survives contact with falling neutrons or with classical elasticity.

What stands is the mathematics, the model medium as a well-measured object, and light as one shear wave by declaration. Everything else physical now rests on named inputs or has been withdrawn. The ledger is folded to V4.92 (+22 KB), with every dependent entry annotated.

## Verdicts

| Part | Question | Verdict | Decided by |
|---|---|---|---|
| **A1** | What polarization would the medium's gravitational wave show a detector? | **FALSIFIED.** Pure vector (spin 1), no tensor part. GW170817 prefers tensor over vector by about 10²¹. The "GW170817 pass" is withdrawn everywhere, and the transverse line keeps only light | Two independent derivations agreeing to 3×10⁻¹⁶; LIGO–Virgo published Bayes factors |
| **A2** | What do the vacuum's 15 unused field directions do? | **Two downgrades.** (1) Seven gapless, quadratic branches with speed limit zero (m* = m/f_s: 10.5 in 2D, about 315 in 3D), so twisted-texture matter (Fano-line cores, the K₇ vortex) feels friction at every speed. (2) The vortex-selection gate used the wrong symmetry: half-quantum protection is accidental | Two legs; m* cross-checked against the banked superfluid fraction to 6×10⁻⁵ |
| **A3** | Does the proton ropelength prediction survive? Is baryon number protected? Is the mass table a prediction? | **§2.15 retracted to Conjecture.** The ideal Borromean ropelength is at most 58.006, below the 60.194 ± 0.3 window, and gives m_p = 759 MeV. Both 60.194 and 80.95 are m_p run backwards. A = 20 uses a non-standard reduction (the standard value is 70). **Linking is unprotected.** **§2.1 is a fit** (dof −1): under PDG 2024, d, c, W and Z miss by more than 2% | Two legs, 46/46 numbers identical |
| **A4** | Do §2.89 (bowl) and §2.90 (tension) survive? | **Both downgraded.** "Flat" is not "no slope": neutrons and atoms fall. Elastic defects do not attract as 1/r² (Eshelby). **KC-EP** made a standing rule: it fires for both | Standard theorems (re-derived in sympy) and published measurements; no second leg needed |

## Blast radius

The ledger has 44 annotated entries; the full lists are in each result file.
- **A1:** the M.ONT/M.REL annexes, §2.88.E, ten §2.91 subsections, the Part V polycrystal row and eight Part VI gate rows.
- **A2:** §2.91.U, §2.88.D.2, §2.91.P and the G-VS1 row.
- **A3:** §2.15, §§2.4–2.6, §2.82, §2.14, §2.1, the M.ONT declaration and three Part V/VI rows.
- **A4:** §2.89 (×2), §2.90 (×4), §2.88 and §2.91.D.

Outside the ledger, STATUS.md is updated. Paper VII, the calculators and the posted papers are Phase B.

## What the substrate program still stands on

- **Mathematics.** PSL(2,7), the lattice results, and the Borromean and ropelength geometry.
- **The model medium.** It is real and measured twice: crystal, shear wave, two sounds, and seven internal branches.
- **Declared, not derived:**
  - light as the shear wave (the units election);
  - knots as embedded objects;
  - a ropelength-organised mass formula, as a fit;
  - a vacuum whose stability, vortex protection and matter-hosting each need a named import (I4, I6, immiscibility).
- **Gone:**
  - gravitational waves;
  - every gravity mechanism on record (the longitudinal bridge earlier; §2.89 and §2.90 now);
  - the proton-mass prediction;
  - protected baryon number;
  - the 2% mass headline.
- **Standing tests:** KC1–KC3 (radiation, aberration, Cherenkov) and KC-EP.
- **Registered successors:** G-OBD1 (does zero-point energy select the vacuum?) and G-RCX1 (what could protect a Borromean baryon?).

## Process notes

- **Exposure.** In all three two-leg parts, the blind second leg returned before the first-leg script was written (H-A1-1, H-A2-1, H-A3-1).
  - The decisive first-leg values were worked out beforehand, and all are deterministic computations, so no free choice was exposed.
  - Fix for next time: file the first leg's values before launching the second leg.
- **Sources not read.** Two literature pages could not be fetched (rate-limited); see A3 H-A3-2. No verdict depends on them.
- **Project store.** The ledger store has 1,983 units free; V4.92 is 22,100 B larger than V4.91. The swap needs the author's word and about 20 KB freed, or an instruction to keep the canonical ledger in the repository.

## Files

All files are on branch `claude/audit-followup-oct6`, under `audit_followup/`:
- `A1_polarization/`, `A2_internal_modes/`, `A3_matter/` and `A4_gravity/`: pre-registrations, locks, scripts, outputs, second legs and results;
- `fold_v4_92/`: the fold script, the independent check and the authorization record.

The canonical `SQT_Master_Ledger_v4_92_CANONICAL.md` (md5 `a98cf1b6f12578537e11270d2cdf0fda`) is delivered in the conversation.
