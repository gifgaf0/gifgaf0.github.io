# G_CI1_CC_S9_REPORT.md — Gate G-CI1, CC leg, S9 re-derivation return (r2)

**Executed under:** mini-dispatch `G_CI1_CC_S9_MINIDISPATCH.md`, md5 `4c21c43d7a2b36aa54985b2d7043b1d3` (63,187 B), path (a) per Addendum 4 ruling S9-R1 (`b3f8cbd58cd2202f971abc823eef76ac`). **Base canonical** V4.76 `f539d10cb4f73c81e7d9fdbe7fa63714`. **The r1 return stays intact** (dispatch `420082d54f11817c9d64a8198f1042ae`; r1 Phase-3 checkpoint `e97d9a1cbf94e5e8cd390b99dab87cf0`, byte-asserted before this run); this return ADDS a re-derivation, it replaces nothing.

**Headline:** all six re-derived interval sets converge to the Chat Read #2 edges. Worst re-derived-arm edge deviation against the embedded record: **5.7e-08** (gate 1e-6). Carried arms re-emitted from unchanged machinery, worst deviation against the r1 checkpoint **3.7e-11**. Verdict class **P-CI-W/EM-IN-WINDOWED**, **OOM-ROBUST** — unchanged, as already two-leg confirmed. Every number below was derived from this leg's own Phase-2 curves and quadratures (`ci1_phase2_cc.json` untouched, md5 re-asserted against the r1 record at open); the disclosed record was consulted only to confirm the r1 defect and, after computation, to state the deviations above. Prose discipline M-1/M-2: row ids, verdict classes, dimensionless ratios, and window edges in SI length units only.

## 1. Scope executed (nothing else re-run)

- **TR-3, TR-4, ACH-DISP, BIR-2, DIFF** — energy-to-wavevector conversion rebound from the sealed CONV row's 5th (anchor-slot) field by **named-key regex**: the action quantum h is bound by key and role-asserted; the reduced constant is **derived as h/(2\*pi)** from the sealed derivation marker; the sealed definition markers for k(E), k(lambda), k(nu) are asserted present. The bound conversion is **k(E) = E/(hbar\*c)**.
- **DIFF, additionally** — the criterion is evaluated **signed**; under the sealed sign map the in-model differential is negative, so the **negative band edge binds**. The upper edge is **validity-capped**: exclusion holds only while every bracket reading is wave-valid and excluding (the sealed both-edges rule; a reading beyond validity is VOID, not excluding), with **VOID beyond** — election E-11, no ray-regime grant, no unbounded exclusion.
- **ACH-DIM** — onset re-derived with a **log-substitution D_lt ladder** (u = ln(1+z'), Simpson n = 2^14) whose **1e-10 doubling gate is asserted per call at every bound z, including the largest sealed z** (the CMB-epoch row).
- **Carried:** TR-1, TR-2, BIR-1, POL re-emitted from unchanged machinery; Phases 0–2, F-IRR, and the verdict-class machinery not re-run. Windows and OOM bands recomputed from the corrected arm set.

## 2. Root-cause acknowledgment (H-CC-8; the dispatch section-2 diagnosis, confirmed)

Confirmed in this leg's own r1 source, with one refinement: the r1 CONV binder **did** read the 5th (anchor-slot) field — the field map was not the failure — but bound its constants by **magnitude window rather than named key**. The reduced-action-constant role was filled by the only J\*s-magnitude numeral present in that field, which is the action quantum h itself; the sealed text defines the reduced constant only symbolically (h/(2\*pi)) and pins k(E) = E/(hbar\*c). Every energy-anchored k was therefore a factor 2\*pi low, while the frequency- and wavelength-anchored arms used the sealed 2\*pi-carrying forms and matched the chat leg — the internal inconsistency named in the mini-dispatch, and the fastest self-confirmation here: r1's own TR-2 edges (wavelength) agree with chat to 1e-11 while r1's TR-3 edges (energy, same machinery) sit exactly (2\*pi)^(4/3) and 2\*pi high. The r1 pin PIN-CC-P3-1 promised named-key binding with loud masked halts; the CONV constants path fell short of that pin. Fixed in r2 by the named-key binder with derivation-marker asserts (a binder failure is a loud masked halt; no silent fallback).

## 3. Re-derived edges (x1 band, SI length units; old = r1, new = r2)

Ratios are old/new; the fingerprints predicted by the embedded record are reproduced **exactly** by this leg's own machinery.

| arm | config | old excl (r1) | new excl (r2) | old/new (lo, hi) |
|---|---|---|---|---|
| TR-3 | hex:step | [4.1079e-20, 2.0740e-10] | [3.5430e-21, 3.3009e-11] | (2pi)^(4/3) = 11.59417, 2pi |
| TR-3 | hex:gem8 | [3.6535e-20, 6.5586e-11] | [3.1512e-21, 1.0438e-11] | 11.59417, 2pi |
| TR-3 | cubic:step | [3.5597e-20, 6.5586e-11] | [3.0703e-21, 1.0438e-11] | 11.59417, 2pi |
| TR-3 | cubic:gem8 | [3.1851e-20, 6.5586e-11] | [2.7471e-21, 1.0438e-11] | 11.59417, 2pi |
| TR-4 | hex:step | [4.3642e-32, 3.5850e-18] | [3.7642e-33, 5.7058e-19] | 11.59417, 2pi |
| TR-4 | hex:gem8 | [3.8815e-32, 1.1337e-18] | [3.3478e-33, 1.8043e-19] | 11.59417, 2pi |
| TR-4 | cubic:step | [3.7819e-32, 1.1337e-18] | [3.2619e-33, 1.8043e-19] | 11.59417, 2pi |
| TR-4 | cubic:gem8 | [3.3839e-32, 1.1337e-18] | [2.9186e-33, 1.8043e-19] | 11.59417, 2pi |
| ACH-DISP | hex:step | [7.3483e-21, 6.1992e-11] | [1.1695e-21, 9.8663e-12] | 2pi, 2pi |
| ACH-DISP | hex:gem8 | [6.1808e-21, 1.9604e-11] | [9.8371e-22, 3.1200e-12] | 2pi, 2pi |
| ACH-DISP | cubic:step | [5.8921e-21, 1.9604e-11] | [9.3776e-22, 3.1200e-12] | 2pi, 2pi |
| ACH-DISP | cubic:gem8 | [4.9947e-21, 1.9604e-11] | [7.9493e-22, 3.1200e-12] | 2pi, 2pi |
| BIR-2 | all four | [3.8951e-10, 1.0813e+25] | [6.1992e-11, 1.0813e+25] | 2pi, 1 (upper is the N-rule edge, k-independent) |
| DIFF | hex:step | [1.0027e-16, unbounded] | [7.7086e-18, 1.9733e-12] | 2pi\*sqrt(30/7) = 13.00743, unbounded-vs-capped |
| DIFF | hex:gem8 | [8.4338e-17, unbounded] | [6.4839e-18, 6.2400e-13] | 13.00743, unbounded-vs-capped |
| DIFF | cubic:step | [8.0399e-17, unbounded] | [6.1810e-18, 6.2400e-13] | 13.00743, unbounded-vs-capped |
| DIFF | cubic:gem8 | [6.8153e-17, unbounded] | [5.2395e-18, 6.2400e-13] | 13.00743, unbounded-vs-capped |
| ACH-DIM | hex:step | [1.5172e-15, 7.2940e-07] | [1.5172e-15, 7.2940e-07] | 1 - 5.4406e-05, 1 (validity edge unmoved) |
| ACH-DIM | hex:gem8 | [1.3494e-15, 2.3066e-07] | [1.3494e-15, 2.3066e-07] | 1 - 5.4406e-05, 1 |
| ACH-DIM | cubic:step | [1.3147e-15, 2.3066e-07] | [1.3147e-15, 2.3066e-07] | 1 - 5.4406e-05, 1 |
| ACH-DIM | cubic:gem8 | [1.1764e-15, 2.3066e-07] | [1.1763e-15, 2.3066e-07] | 1 - 5.4406e-05, 1 |

(ACH-DIM old/new onsets differ in the 5th digit; the table's 5-digit rendering coincides for three configs. Full-precision pairs are in the checkpoint's `s9_rederivation.per_arm_old_new_x1` block.) The DIFF onset factor decomposes as the k factor 2\*pi times sqrt(30/7) from the band-edge change (the r1 both-signs magnitude test let the positive edge govern; the sealed sign map binds the negative edge — H-CC-9). The DIFF upper edge is now the strongest-reading validity cap with VOID beyond (E-11 — H-CC-10).

## 4. ACH-DIM / D_lt at the largest sealed z (H-CC-11)

- Old ladder (r1: fixed-step linear-z Simpson, n = 4096): D_lt = 1.3053923867e+26 SI length units; its own 4096-vs-8192 doubling deviation there is **1.518e-04 — the 1e-10 gate FAILS at that z** (the r1 gate was asserted only at z <= 6, where it passed; that is the defect).
- New ladder (u = ln(1+z') Simpson, n = 2^14): D_lt = 1.3051793345e+26 SI length units; doubling deviation **7.634e-15 — passes the 1e-10 gate with orders of margin**, asserted per call at every bound z.
- Shift new/old − 1 = **−1.632e-04**, propagating through the onset's D^(−1/3) scaling to the observed −5.4406e-05 onset move on all four configs — precisely the attribution in the S9 record. The D-independent ACH-DIM validity edge did not move (PIN-CC-S9-2 verified).
- Per-z gate evidence for every sealed z is recorded in the checkpoint (`D_lt_largest_z.per_z_gate_evidence`).

## 5. Windows and verdict (SI length units)

- Per config W^EM (x1): hex:step (0, 3.7641664288e-33]; hex:gem8 (0, 3.3478202275e-33]; cubic:step (0, 3.2619132000e-33]; cubic:gem8 (0, 2.9185931177e-33].
- **W^EM_union of record = (0, 3.7641664288e-33]** — the PIN-CH-S9-1 class, about one order tighter than the r1 read.
- OOM bands: x10 union (0, 8.1096507332e-33]; x0.1 union (0, 1.7471712864e-33].
- Verdict class **P-CI-W/EM-IN-WINDOWED**, **OOM-ROBUST** (x10 and x0.1 identical). F-IRR FIRES, K empty; POL VOID-NO-CANDIDATE; G-POLY1 window SUSPENDED per PF-1 and reported alongside only: (0, 2.1213132100130068].
- **Disclosure (H-CC-12):** with the DIFF exclusion validity-capped, the region beyond the largest arm-exclusion edge (d > 1.0812672472e+25 SI length units, the BIR-2 N-rule edge) is excluded by no arm — every arm is VOID there under its own N-rule, ray rule, or validity cap. The W keys of record carry the d→0+ connected component (G-POLY1 WINDOWED-class lineage); the far non-excluded component is serialized alongside under `*_far` keys and stated here. VOID never excludes and never counts as FAIL; a VOID can only widen a window.

## 6. Honesty ledger, this return (numbered continuations; full text in the checkpoint)

- **H-CC-8** — root-cause acknowledgment (section 2 above): magnitude-window CONV binding filled the reduced-constant role with the action quantum; sealed conversion re-bound by named key. CONFIRMED, no counter-analysis.
- **H-CC-9** — DIFF band edge: r1 both-signs magnitude test replaced by the sealed signed criterion; the negative edge binds.
- **H-CC-10** — DIFF upper edge: r1 ray-regime geometric-bracket grant removed per E-11; validity-capped, VOID beyond.
- **H-CC-11** — D_lt ladder: r1 doubling gate was never asserted at the largest sealed z, where it fails loudly; replaced by the log-substitution ladder with a per-call gate (section 4).
- **H-CC-12** — window-of-record disclosure (section 5).
- **H-CC-13** — self-catch on this instrument: the first r2 evaluation run capped the DIFF exclusion at the loosest reading's validity limit (mixed EXCL/VOID treated as EXCL), a factor k_hi/k_lo high against the embedded record. Resolved by the sealed both-edges rule itself, which is dispositive without the record: a reading beyond wave validity is VOID, not excluding, so the standard conservative combiner already yields the tightest-reading cap. The special-case combiner was deleted (DIFF now uses the same combiner as every arm); the defective run's checkpoint was superseded in place before any return; no other arm changed between runs.

## 7. Artifacts of this return (md5 / bytes; independent T1 scans all ZERO)

| artifact | md5 | bytes |
|---|---|---|
| `ci1_phase3_cc_r2.json` (checkpoint, r1 schema + `s9_rederivation` block) | `845ae6beb1b90fe34c540f843ffdb9f5` | 45,760 |
| `g_ci1_phase3_mapper_ccleg_r2.py` (instrument; T1 self-grep at invocation: 0) | see return manifest | see return manifest |
| `G_CI1_CC_S9_MINIDISPATCH.md` (provenance copy) | `4c21c43d7a2b36aa54985b2d7043b1d3` | 63,187 |
| `G_CI1_CC_S9_MANIFEST.json` (provenance copy) | `4a08dd1196ed0eb5ccd6fb677b3c2226` | 1,232 |

This report's own md5/bytes and the instrument's are recorded in `G_CI1_CC_S9_RETURN_MANIFEST.json`, written after this file is frozen. T1 scans: instrument 0 hits at invocation and at close; checkpoint 0 hits; this report 0 hits (scan result in the return manifest). r1 files untouched — byte-asserted at open.

**On return (Addendum 4 A4.4):** X-1 byte-hash, independent T1 re-scan, and C-CI-4 run 3 under the frozen comparator `956036f05e90c9ecfc32883dcbf2b910` are the chat leg's steps; expected outcome under PIN-CH-S9-1 is MATCH <= 1e-6 on all arms (this leg's own post-computation check: worst 5.7e-08), S9 CLOSED, fold staging AUTHORIZED — the fold itself executes only on the author's explicit authorization, per standing practice. If the comparator finds otherwise, S9 stays open and this return stands as computed; no leg forces agreement.
