# G_CI1_CC_S9_MINIDISPATCH.md — Gate G-CI1, S9 resolution mini-dispatch (path (a); P-4: one self-contained file)

Minted 2026-08-23T18:53:57.294180+00:00 by the chat leg on the author's election (Addendum 4, embedded verbatim below). Base canonical V4.76 md5 `f539d10cb4f73c81e7d9fdbe7fa63714`. Original dispatch `420082d54f11817c9d64a8198f1042ae`; your r1 return is byte-verified on the record (X-1 ALL PASS) and **stays intact** — this mini-dispatch adds a re-derivation, it replaces nothing in the repo history.

## 0. What this is
Your Phase-3 read #1 and the chat leg's read #2 agree on the verdict CLASS (`P-CI-W/EM-IN-WINDOWED`, OOM-ROBUST), on F-IRR (FIRES, K empty), on A-POL (VOID-NO-CANDIDATE), and on the frequency/wavelength arms TR-1, TR-2, BIR-1 to 4.2e-11. Six interval sets diverge (TR-3, TR-4, ACH-DISP, BIR-2, DIFF, ACH-DIM), with exact convention fingerprints — the full evidence is the embedded C-CI-4 run-2 record. The author has ruled the sealed text dispositive and elected path (a): **you re-derive the six arms; nothing else is re-run.**

## 1. Standing rules (unchanged)
T1 self-grep at every invocation against the embedded frozen list (three embeds here are exempt: the sealed file, the lock-record class, the list itself); T4; M-1/M-2 (never echo a sealed row; prose reports carry row ids, verdict classes, dimensionless ratios, and window edges in SI length units only); elections E-10, E-11, E-12 and readings H-4, H-6 in force. **The sealed file `dd8fe2d364624750201ad9c9ffef575c` may be opened immediately** after the md5 and census-12 asserts — the blind-first constraint is spent. Halts: any hash mismatch, any T1 hit, any binder failure (loud, masked). Number every self-catch (H-CC-8 onward); nothing silently corrected.

## 2. The field map you need (chat H-14, confirmed against the sealed bytes)
Rows split on the pipe character with a leading pipe: field 1 = row id, field 5 = the anchor-text slot, field 6 = params, field 8 = Binding. **For the CONV row only, the SI-constants text — the exact SI defining constants and the k(E), k(lambda), k(nu) conversion definitions, the length-unit pins, and the cosmology pins — lives in field 5.** The CONV params field (6) carries the channel-speed import and RULES R1–R4. Bind k(E) from field 5 by named-key regex. If your r1 binder fell back to an internal constant set for the energy conversions, this field map is the likely reason; say so (or say otherwise) in your own root-cause acknowledgment.

## 3. Scope of re-derivation (ONLY these; everything else carried forward)
1. **TR-3, TR-4, ACH-DISP, BIR-2, DIFF:** rebind the energy-to-wavevector conversion **k(E) = E/(hbar*c)** from the sealed CONV field-5 text (your r1 edges are exactly consistent with E/(h*c), a factor 2pi low, while your own lambda/nu arms used the sealed 2pi-carrying forms — the internal-inconsistency check is your fastest self-confirmation). Re-evaluate the five arms against your OWN Phase-2 curves (`ci1_phase2_cc.json`, untouched).
2. **DIFF, additionally:** the sealed sign map makes the in-model differential negative — the **negative band edge binds**; and the **upper edge is validity-capped** at the strongest-reading validity limit with VOID beyond (election E-11: no ray-regime grant; a VOID can only widen a window). No unbounded exclusion.
3. **ACH-DIM:** re-derive the **onset edge** with a D_lt ladder that **passes a 1e-10 doubling gate asserted at the largest sealed z** (the CMB-epoch row). A fixed-step linear-z Simpson at your r1 resolution has a z-step of about 0.3 there; the chat leg's own linear-z ladder loudly failed the same gate at that z and was replaced by a log-substitution ladder (u = ln(1+z'); Simpson in u), which passes with orders of margin — use that or any ladder that demonstrably passes AT that z. Record old/new D_lt at that z and the gate evidence. The D-independent validity edge should not move.
4. **Carried forward, must be identical to r1:** TR-1, TR-2, BIR-1, POL (carry the r1 entries or re-emit from your unchanged machinery — the chat comparator asserts identity either way). Phases 0–2, F-IRR, and the verdict-class machinery are NOT re-run. Recompute the per-config windows, W_union, and the OOM x10 / x0.1 bands from the corrected arm set.

## 4. Self-check fingerprints (from the embedded run-2 record; use them to confirm your r1 defect, then derive)
Your r1-over-chat edge ratios, identical across configs: TR-3/TR-4 onset x(2pi)^(4/3), cutoffs x2pi; ACH-DISP both edges x2pi; BIR-2 live-edge x2pi, upper identical; DIFF onset x13.00743 = 2pi*sqrt(30/7), upper unbounded-vs-capped; ACH-DIM onset -5.44e-5 (config-independent), validity edge identical. **Disclosure note:** the expected corrected edges are necessarily disclosed by the embedded S9 record. The verification value of this re-run is your independent re-execution of the corrected bindings against your OWN curves and quadratures with doubling evidence — derive, never transcribe. If your sealed-conformant re-derivation does NOT converge to the disclosed edges, report the divergence exactly as computed; S9 then stays open for the author. No leg forces agreement.

## 5. Deliverables (push to the repo path gci1_gate/, r1 files left intact)
- **`ci1_phase3_cc_r2.json`** — same schema as r1 (full `per_oom` with all ten arms at x1 / x10 / x0.1), plus a top-level **`s9_rederivation`** block: scope list; the k(E) binding statement and its field-5 source; the DIFF band-edge and upper-cap statements; `D_lt_largest_z` old/new with the doubling-gate evidence; per-arm old/new edge pairs; your H-items (H-CC-8 onward) including your own root-cause acknowledgment or counter-analysis.
- **`G_CI1_CC_S9_REPORT.md`** — prose report (row ids, ratios, edges in SI length units only).
- Updated instruments (e.g. `g_ci1_phase3_mapper_ccleg_r2.py`), each T1-clean at invocation.
- md5 + byte count for every artifact; independent T1 scan results (must be zero).

## 6. Chat-side commitments (hashes only)
- `ci1_phase3_chat.json`: md5 `276586f94c8d426c38ff12228c91289d` (23,097 B)
- `g_ci1_phase3_mapper_chatleg.py`: md5 `49d153e4aa52305407e7887f8e0f6666` (17,242 B)
- `g_ci1_ci4_compare_r3.py`: md5 `956036f05e90c9ecfc32883dcbf2b910` (8,086 B)
- `ci1_twoleg_compare.json`: md5 `82d04fa6a74a0135b8805189d4305a9e` (14,721 B)
The run-3 comparator above is **frozen before your re-derivation exists**; it gates the six arms at 1e-6 against Chat Read #2, asserts carried-arm identity to r1, and mechanically issues S9 CLOSED + fold-staging AUTHORIZED (the Addendum-4 conditional clause) or S9 OPEN. Chat expectation pin PIN-CH-S9-1 is recorded in Addendum 4.

---
# EMBEDS (byte-exact; fences `<<<EMBED name md5 bytes TAG>>>` … `<<<END name>>>`; content = every byte between the fence lines, excluding the newline after the opening fence and the newline before the closing fence)

## LOCK RECORD ADDENDUM 4 (lock-record class, T1-exempt embed; the S9-R1 ruling and the conditional fold authorization, VERBATIM)
<<<EMBED G_CI1_LOCK_RECORD_ADDENDUM_4.md b3f8cbd58cd2202f971abc823eef76ac 4412 EXEMPT>>>
# G_CI1_LOCK_RECORD_ADDENDUM_4.md — Addendum 4 to the G-CI1 lock record (append-only; base `a6adbb6a`, Addenda 1–3 `e5029ae8` / `92672d5a` / `4c0b52c6` unmodified)

**Date:** August 21, 2026. **Scope:** the author's S9 resolution election (path (a)), the conditional fold authorization, and the S9 mini-dispatch protocol. Lock-record class (T1-exempt embed by the two-document convention).

## A4.1 — Author's directive (VERBATIM)
> **Directive: Elect Path (a) to Resolve S9 and Authorize Mini-Dispatch**
> The Chat Read #2 execution, the C-CI-4 comparison, and the drafted closure memo are confirmed. The H-11 through H-16 honesty ledger items are acknowledged.
> The S9 root-cause analysis is accepted. The sealed CONV text is dispositive regarding the k(E) conversion.
> I elect resolution path (a) to clear the S9 blocker.
> 1. Mint the P-4 mini-dispatch to the CC leg.
> 2. Instruct CC to re-derive the five energy-anchored arms enforcing k(E) = E/(ħc), the negative band edge on A-DIFF, and the validity-capped upper edges per E-11.
> 3. Instruct CC to re-derive the ACH-DIM onset using a D_lt ladder that passes the 1e-10 doubling gate at the largest sealed z.
> 4. Execute the C-CI-4 re-run upon CC's return.
> Report back with the final C-CI-4 (run 3) verdict. If MATCH ≤ 1e-6 is achieved across all arms, you are authorized to stage the V4.77-class fold.

## A4.2 — Rulings now T3-immutable
- **S9-R1 (path (a) elected):** the sealed CONV text is dispositive on k(E) = E/(ħc); the CC leg re-derives TR-3, TR-4, ACH-DISP, BIR-2, DIFF under the sealed conversion, with the negative band edge binding on A-DIFF and validity-capped upper edges per E-11 (VOID beyond; a VOID can only widen a window); and re-derives the ACH-DIM onset with a D_lt ladder that passes a 1e-10 doubling gate asserted at the largest sealed z. Nothing else is re-run; the four matched arms (TR-1, TR-2, BIR-1, POL) must arrive identical to the r1 read.
- **Conditional fold authorization:** if C-CI-4 run 3 returns MATCH ≤ 1e-6 across all arms (with carried-arm identity, class, OOM bands, per-config and union edges agreeing), the chat leg is **authorized to stage the V4.77-class fold** (§2.91.N + Part VI row + §2.91.M W_∪-conditionality annotation) without a further round trip; the fold executes only on the author's explicit fold authorization message, per standing practice.
- **Run-3 comparator frozen pre-return:** `g_ci1_ci4_compare_r3.py` md5 `956036f05e90c9ecfc32883dcbf2b910` (8,086 B; T1 zero) — minted and hashed before the CC re-derivation exists; it gates the six re-derived arms at 1e-6 against Chat Read #2, asserts the four carried arms identical to r1, and issues CLOSED/AUTHORIZED or OPEN/WITHHELD mechanically.
- **PIN-CH-S9-1 (chat expectation, pre-declared):** convergence of all six re-derived arms to the Chat Read #2 edges at ≤ 1e-6; carried arms identical; per-config union edges 3.7642e-33 / 3.3478e-33 / 3.2619e-33 / 2.9186e-33 class; W_∪ of record (0, 3.76416643e-33] SI length units; OOM ×10 / ×0.1 unions in the 8.11e-33 / 1.75e-33 class; verdict class and OOM-robustness unchanged. A non-converging return is reported as-is to the author (S9 stays OPEN); no leg forces agreement.

## A4.3 — Mini-dispatch protocol
The mini-dispatch `G_CI1_CC_S9_MINIDISPATCH.md` (P-4, one self-contained file; md5 recorded in its manifest and the release report) embeds byte-exact: this Addendum 4 (lock-record class, exempt), the frozen T1 list (self-referential, exempt), the sealed anchor file `dd8fe2d3` (exempt; open allowed immediately after md5 + census-12 assert — the blind-first constraint is spent), the C-CI-4 run-2 record `756973ee` (the S9 evidence; scanned), and the Phase-3 closure memo `dd1a02ec` (scanned). The chat Phase-3 checkpoint is NOT embedded: the expected edges are necessarily disclosed by the S9 record, and the verification value of the re-run lies in CC's independent re-execution of the corrected bindings against CC's own Phase-2 curves and quadratures, with doubling evidence — CC derives, never transcribes.

## A4.4 — On return
X-1 byte-hash of `ci1_phase3_cc_r2.json`, the S9 report, and the updated instruments; independent T1 re-scan; C-CI-4 run 3 under the frozen comparator; then either **S9 CLOSED + fold staging** (green path) or **S9 OPEN + report** (divergent path). Standing untouched: §2.52 Open 3, §2.87.J, OP-2.58.2d, P-LEX-1.

<<<END G_CI1_LOCK_RECORD_ADDENDUM_4.md>>>

## T1 FROZEN LIST (self-referential embed — exempt from the scan by construction)
<<<EMBED t1_forbidden_G_CI1.txt 653a0b7447e68aa8a094e62337a24da3 1127 EXEMPT>>>
# G-CI1 T1 forbidden-string list — DRAFT (frozen at lock; md5 recorded in the lock record)
# One Python regex per line; lines beginning with '#' are comments. Case-sensitive.
# Applied by self-grep to every instrument file and checkpoint of every phase, both legs.
# Exempt embeds: anchors_G_CI1_SEALED.md and G_CI1_LOCK_RECORD.md only.
# --- inherited class (G-POLY1 lineage) ---
\bMpc\b
\bGpc\b
\bkpc\b
\bpc\b
\bHz\b
\b[kMGT]Hz\b
GW1
170817
170814
GWTC
LIGO
Virgo
KAGRA
\bLVK\b
\bSME\b
299792458
2\.99792458
2\.998e8
\b3e8\b
\bm/s\b
\bkm/s\b
\bmeters?\b
\bmetres?\b
# --- EM extension (band / source-class / instrument / unit / constant tokens) ---
\bradio\b
X-ray
x-ray
gamma-ray
γ-ray
\bVHE\b
\b[kMGT]eV\b
\beV\b
H\.E\.S\.S
\bHESS\b
\bMAGIC\b
VERITAS
\bFermi\b
\bLAT\b
\bCTA\b
LHAASO
\bHAWC\b
\bEBL\b
blazar
quasar
\bQSO\b
\bAGN\b
\bGRB\b
\bFRB\b
pulsar
magnetar
supernova
\bSNe?\b
\bIa\b
Kostel
Mewes
Aharonian
\b1ES\b
\bMk[nr]\b
\bPKS\b
Chandra
\bXMM\b
NuSTAR
\bSwift\b
INTEGRAL
\bnm\b
\bÅ\b
Angstrom
micron
\bμm\b
redshift
\bz\s*=\s*\d
6\.626
6\.62607
4\.1357
1\.054571
1\.602176
1\.616255
1\.616e-35
Planck length

<<<END t1_forbidden_G_CI1.txt>>>

## SEALED ANCHOR FILE (T1-exempt embed; md5 + census-12 assert at open; open allowed IMMEDIATELY — the blind-first constraint is spent)
<<<EMBED anchors_G_CI1_SEALED.md dd8fe2d364624750201ad9c9ffef575c 17652 EXEMPT>>>
# anchors_G_CI1_SEALED.md — G-CI1 sealed anchor file (SEALED AT LOCK, August 17, 2026)

STATUS: SEALED. CENSUS = 12 rows (4 x A-EM-TRANS + 2 x A-ACHROM + 2 x A-BIR-EM + 1 x A-POL + 1 x A-DIFF + 1 x VLD + 1 x CONV). T1-SCAN-EXEMPT EMBED (one of the two exempt embeds; the other is G_CI1_LOCK_RECORD.md). UNOPENED by any instrument before Phase 3 (pre-registration §4, Phase 3.1); md5-asserted at every open; census asserted at every open. Rows are parsed by structured fields and NEVER echoed (M-1); every comparison is formed dimensionless before any print (M-2). H-16 lesson applied: the pipe character is the field separator ONLY — no absolute-value bars anywhere in this file; abs() is spelled out. All numerics in params are plain ASCII e-notation; no superscript glyphs appear in any field (E3-6(a) frozen-ASCII semantics therefore never engage; ascii_flag = CLEAN on every row).

Row schema (9 fields, in order): id / class / pattern / dialect_ref / anchor_text / params / Caveat / Binding / ascii_flag
Read order (Phase 3.1): TR-1, TR-2, TR-3, TR-4, ACH-DIM, ACH-DISP, BIR-1, BIR-2, POL, DIFF; VLD and CONV are parsed first (mapper configuration), never evaluated as arms. Post-verdict disclosure via the sanctioned checkpoint carriers verbatim (anchor_text, Caveat, Binding).

Provenance discipline: every anchor_text quantity was retrieved from the named source at seal time (August 17, 2026) and transcribed; quantities NOT retrieved from a source are marked [RECALLED-FLAG] inside params and carry a conservative two-reading rule. Nothing in this file was evaluated against any curve at seal time.

| id | class | pattern | dialect_ref | anchor_text | params | Caveat | Binding | ascii_flag |
|---|---|---|---|---|---|---|---|---|
| TR-1 | A-EM-TRANS | P-TRANS | memo Register F(i), longest-wavelength rung (author band 1: the low-frequency radio rung, chosen for maximum regime coverage at the long-wavelength end); source: Saxena et al. 2018 MNRAS 480, 2733 (arXiv:1806.01191) | TGSS J1530+1049, the most distant radio galaxy to date at a redshift of z = 5.72, selected from the TGSS ADR1 survey at 150 MHz; flux density of 170 mJy at a frequency of 150 MHz and 7.5 mJy at 1.4 GHz; compact morphology in VLA imaging at 1.4 GHz (deconvolved angular size 0.6 arcsec); Lyman-alpha redshift from GMOS spectroscopy (Saxena et al. 2018) | nu_ref = 1.5e8 Hz (primary; the survey selection frequency, a secure detection at 170 mJy); k_ref = 2*pi*nu_ref/c; secondary detected frequency nu_sec = 1.4e9 Hz reported alongside (informational, non-verdict); z_src = 5.72; D_ref = D_lt(5.72) per CONV rule R1; tau_r = 1.0 (arrival budget) | The intrinsic luminosity is not independently known, so tau_r = 1 is the CONSERVATIVE arrival budget of the P-TRANS pattern (the A-1 twin), read with the x10^(+/-1) OOM band; tighter residual budgets exist and would only tighten. Ionospheric and interstellar plasma effects at 150 MHz are modeled non-substrate propagation effects. | P-TRANS: alpha_T(x_ref; d) * D_ref <= tau_r. CONV rules R1 (D_lt) and R2 (k-dressing both-readings intersection: k_obs and (1+z_src)*k_obs; exclusion asserted only where both readings exclude; both reported). | CLEAN |
| TR-2 | A-EM-TRANS | P-TRANS | memo Register F(i), rung 2 (author band 2); source: Fan et al. 2003 AJ 125, 1649 (astro-ph/0301135) | quasar SDSS J114816.64+525150.3 at z=6.43 (redshift determined from the position of the Lyman break, accurate to 0.05), discovered in 1300 deg^2 of SDSS imaging data (Fan et al. 2003) | lambda_ref = 9.0e-7 m [RECALLED-FLAG: representative observed-frame wavelength of the detection band; the Lyman break sits at (1+z)*1.216e-7 m = 9.03e-7 m; the survey filter's effective wavelength (about 8.9e-7 m) was not retrieved from the anchor source]; k_ref = 2*pi/lambda_ref; two-reading bracket for the flag: lambda in [8.5e-7, 1.0e-6] m, exclusion asserted only if excluded at both edges; z_src = 6.43; D_ref = D_lt(6.43) per CONV R1; tau_r = 1.0 | Broadband detection (i-dropout selection); the representative wavelength is flagged and bracketed; tighter budgets only tighten. | P-TRANS as TR-1; CONV R1, R2, R3 (bracket both-readings). | CLEAN |
| TR-3 | A-EM-TRANS | P-TRANS | memo Register F(i), rung 3 (author band 3); source: Banados et al. 2018 ApJL 856, L25 (arXiv:1803.08105) | quasar ULAS J1342+0928 at z = 7.54: 45 ks Chandra observation, 14.0 (+4.8, -3.7) counts detected in the observed-frame energy range 0.5-7.0 keV (6 sigma detection); hardness ratio HR = -0.51 (+0.26, -0.28) between the 0.5-2.0 keV and 2.0-7.0 keV ranges | E_ref = 2.0e3 eV (observed-frame boundary between the two counted sub-bands; representative); E bracket for R3: [5.0e2, 7.0e3] eV (the detection band edges), exclusion asserted only if excluded at both edges, representative reported; k = E/(hbar*c); z_src = 7.54; D_ref = D_lt(7.54) per CONV R1; tau_r = 1.0 | 14 counts total; band-integrated detection; the sub-band counts are few; tighter budgets only tighten. | P-TRANS as TR-1; CONV R1, R2, R3. | CLEAN |
| TR-4 | A-EM-TRANS | P-TRANS | memo Register F(i), shortest-wavelength ground-based very-high-energy rung (author band 4); sources: Aharonian et al. (H.E.S.S. Collaboration) 2006 Nature 440, 1018 (astro-ph/0508073) and the collaboration's auxiliary data table for its Figure 2 | 1ES 1101-232, z = 0.186; spectrum data points from 0.165 to 3.292 TeV; highest bin: energy interval 2.615-3.292 TeV, mean energy 2.916 TeV, flux 4.73e-14 +/- 3.03e-14 per TeV cm^2 s; bin 1.650-2.077 TeV: mean 1.840 TeV, 1.17e-13 +/- 0.56e-13; bin 0.657-0.827 TeV: mean 0.733 TeV, 1.17e-12 +/- 0.37e-12 (auxiliary table); companion A&A paper: power law of index 2.94 +/- 0.20 over 200 GeV to 4 TeV | E_ref = 2.916e12 eV (highest measured bin, source-reported); conservative alternative reading E_alt = 7.33e11 eV (highest bin at or above 3 sigma); exclusion asserted only if excluded under BOTH E readings (R3), both reported; k = E/(hbar*c); z_src = 0.186; D_ref = D_lt(0.186) per CONV R1; tau_r = 1.0 | EBL pair-production is a modeled non-substrate opacity already acting on these photons; tau_r = 1 is the residual-additional-opacity budget (the A-1 twin, memo Register F(i)); the highest bin is a 1.6 sigma point, hence the E_alt reading. | P-TRANS as TR-1; CONV R1, R2, R3. | CLEAN |
| ACH-DIM | A-ACHROM | P-ACHROM-DIM | memo Register F(ii) chromatic-dimming class; sources: Fixsen et al. 1996 ApJ 473, 576; Mather et al. 1994 | FIRAS: rms deviations from a blackbody spectrum less than 50 parts per million of the peak of the cosmic microwave background; abs(y) < 15e-6 and abs(mu) < 9e-5 (95% CL) (Fixsen et al. 1996); wavelength range 0.5 to 5 mm | lambda_1 = 5.0e-3 m; lambda_2 = 5.0e-4 m (band edges); k_i = 2*pi/lambda_i; Delta_tau_r = 5.0e-5; z_src = 1090 [RECALLED-FLAG: nominal last-scattering redshift, not verbatim-retrieved; D_lt insensitive below 1e-4 relative]; D_ref = D_lt(1090) per CONV R1 | The 50 ppm figure is a model-fit residual (blackbody plus dipole plus Galactic terms), read at order-of-magnitude level (R2, the DLM-comparison precedent) with the x10^(+/-1) OOM band; a frequency-dependent attenuation across the band would appear as a distortion at the level of its differential optical depth. | P-ACHROM-DIM: abs(alpha_T(x_1;d) - alpha_T(x_2;d)) * D_ref <= Delta_tau_r; CONV R1, R2. | CLEAN |
| ACH-DISP | A-ACHROM | P-ACHROM-DISP | memo Register F(iii) vacuum-dispersion class (frequency-dependent speed within one observed band); source: Schaefer 1999 PRL 82, 4964 (astro-ph/9810479) | Delta c/c < 6.3 x 10^-21 based on the simultaneous arrival of a flare in GRB 930229 with a rise time of 220 +/- 30 microseconds for photons of 30 keV and 200 keV (Schaefer 1999); secondary, same source: Crab pulsar optical pulses at 0.35 and 0.55 microns, phase difference less than 10 microseconds at 2 kpc, Delta c/c less than 5 x 10^-17 | primary: E_1 = 3.0e4 eV, E_2 = 2.0e5 eV, k_i = E_i/(hbar*c), beta_r = 6.3e-21, z_src unknown (no redshift for this burst; observed-frame k only; R2 not applicable, flagged); secondary reading (informational, reported alongside, non-verdict): lambda_1 = 3.5e-7 m, lambda_2 = 5.5e-7 m, beta_sec = 5.0e-17 | A path-integrated two-energy simultaneity bound; the criterion is a speed-ratio comparison at the two k for the same d, no distance enters; the secondary reading is a distinct regime pin, reported not intersected. | P-ACHROM-DISP: abs(Delta_ch(x_1;d) - Delta_ch(x_2;d)) <= beta_r; ray regime x >= x_G: identical path averages imply zero difference, PASS-RAY (nondispersive rays), reported (§5.4). | CLEAN |
| BIR-1 | A-BIR-EM | P-BIR | memo Register F(iii) polarization-walk twin of the banked s_1 law, long-wavelength polarimetry; sources: Michilli et al. 2018 Nature 553, 182 (arXiv:1801.03965); Gajjar et al. 2018 ApJ 863, 2 | FRB 121102, localized to a dwarf galaxy at redshift z = 0.193: bursts show ~100% linearly polarized emission at 4.1-4.9 GHz (Arecibo) with RM_src = +1.46 x 10^5 rad m^-2; nearly 100% linear polarization at 4-8 GHz (GBT) | nu_ref = 4.5e9 Hz; k_ref = 2*pi*nu_ref/c; P_obs = 1.0 (nearly 100%); kappa_r = 1.0 rad (order-of-magnitude depolarization budget: a random-axis walk phase of order 1 rad would depolarize an ensemble; near-total observed polarization bounds Phi_RMS at that order); z_src = 0.193; D_ref = D_lt(0.193) per CONV R1; N-rules: N_lambda = d/lambda_ref >= 10 and N_dom = D_ref/d >= 10, else VOID-N | Depolarization dialect (random-axis walk), not fixed-axis coherent birefringence: the coherent-birefringence coefficient bounds of Register F(iii) are a different dialect and are NOT used as kappa_r. The observed polarization is after Faraday-rotation correction (a plasma effect, not a vacuum property). kappa_r read at OOM level with the x10^(+/-1) band; the comparison is R2 (DLM precedent). | P-BIR: Phi_RMS := s_1 * k_ref * sqrt(d * D_ref) <= kappa_r, live only under the N-rules; CONV R1, R2. | CLEAN |
| BIR-2 | A-BIR-EM | P-BIR | memo Register F(iii) polarization-walk twin, short-wavelength polarimetry; source: Gotz et al. 2014 MNRAS 444, 2776 (arXiv:1408.4121) | GRB 140206A: using INTEGRAL/IBIS as a Compton polarimeter, the linear polarization level of the second peak of the burst is constrained as being larger than 28% at 90% c.l.; TNG afterglow spectroscopy gives z = 2.739 (Gotz et al. 2014) | E bracket = [2.0e5, 8.0e5] eV [RECALLED-FLAG: the IBIS Compton-mode band was not verbatim-retrieved from the anchor source; R3 applies — exclusion asserted only if excluded at both edges]; k = E/(hbar*c); P_obs >= 0.28; kappa_r = 1.0 rad (OOM depolarization budget as BIR-1); z_src = 2.739; D_ref = D_lt(2.739) per CONV R1; N-rules as BIR-1 | Prompt-emission polarization lower limit; band flagged and bracketed; OOM level; R2 comparison. | P-BIR as BIR-1; CONV R1, R2, R3. | CLEAN |
| POL | A-POL | P-POL | memo Register E, LVK polarization program; sources: Abbott et al. 2017 PRL 119, 141101 (GW170814); the GWTC-1 tests-of-GR summary (arXiv:1905.05565 sec. 8); Takeda et al. 2021 PRD 103, 064037 (arXiv:2010.14538) | purely tensor polarizations preferred over purely vector or purely scalar polarizations: for GW170817 Bayes factors greater than 10^20 in favor of purely tensor polarizations; GW170814 and GW170818 give Bayes factors of a few tens and hundreds versus purely vector or scalar (GWTC-1 summary); Takeda et al. find logarithms of the Bayes factors of 2.775 and 3.636 for GW170814 and 21.078 and 44.544 for GW170817 in favor of pure tensor against pure vector and pure scalar respectively | categorical; evaluated on the Phase-1 candidate set K only: PASS iff K's helicity content contains {+2, -2} and is tensor-dominant; FAIL iff K's content is {+1, -1}-only; INDETERMINATE iff mixed; under CI-W/EM-IN (K empty) the arm is VOID-NO-CANDIDATE | The LVK tests are extreme-hypothesis tests (pure tensor vs pure vector vs pure scalar) and, per the papers' own caveat, do not preclude mixed-content scenarios; no viable theory predicts purely scalar or purely vector radiation, so the test is a null test. | P-POL categorical; mixed content maps to INDETERMINATE, not FAIL (the papers' own extreme-hypothesis caveat, Binding). | CLEAN |
| DIFF | A-DIFF | P-DIFF | memo Register E, the GW170817/GRB 170817A speed band; the ANNEX-CDEF-1 own-pre-registration clause discharged here (§3.2); source: Abbott et al. 2017 ApJL 848, L13 (arXiv:1710.05834) | observed time delay of (+1.74 +/- 0.05) s between GRB 170817A and GW170817; the difference between the speed of gravity and the speed of light constrained to be between -3 x 10^-15 and +7 x 10^-16 times the speed of light; luminosity distance 40 (+8, -14) Mpc | Delta_obs := (v_GW - c_EM)/c_EM in [B_lo_obs, B_hi_obs] = [-3.0e-15, +7.0e-16]; sign mapping onto the gate's Delta (Delta_S under CI-S, Delta_W under CI-W/EM-IN; both EM relative to the S2 reference, §6): Delta = -Delta_obs/(1 + Delta_obs) = -Delta_obs to better than 1e-14 relative, hence [B_lo, B_hi] = [-7.0e-16, +3.0e-15]; k_S2 = 2*pi*f_ref/c with f_ref = 1.0e2 Hz (inherited from the G-POLY1 A-1 reference frequency, lineage convention); k_EM: E bracket [1.0e4, 1.0e6] eV [RECALLED-FLAG: gamma-ray-monitor band edges not verbatim-retrieved; R3 applies, representative 1.0e5 eV reported]; distance informational only (the criterion is a speed-ratio comparison) | The source bound already folds an assumed emission-delay window; frozen as stated; f_ref = 1.0e2 Hz is a lineage convention (the signal spans a broader band); the sign convention of the observation is stated explicitly above so that no sign slip can occur at read. | P-DIFF: B_lo <= Delta <= B_hi; runs LAST of all arms; CC read #1 is the blind read of record (E-9). | CLEAN |
| VLD | VLD | validity-edge parameters (mirrors G-POLY1 A-4) | pre-registration §5 restated for the mapper (no physics; guards against silent drift) | eps_T^2 <= 0.10 (weak-fluctuation validity, per config; else all second-order arms VOID); Q_T(x)*x^3 <= 0.10 (coherent-wave validity, else VOID-INCOHERENT at that x); eps_T*x <= 1 (phase-perturbation validity, else VOID-PHASE); x_S = largest grid x satisfying both; x_G = 10 (ray-regime domain); overlap rule: exclusion only if BOTH models exclude; gap rule: VOID unless both boundary points excluded AND the leg's own abs(Delta_ch) (resp. alpha*d) is unimodal or monotone across the gap; N_lambda = N_dom = N_cell = 10; OOM band x10^(+1) and x10^(-1) on every sealed threshold; grid x = 10^n, n = -8, -7.5, ..., +8 (33 points); comparison edges 1e-6 relative; doubling gate 1e-8 (floor 1e-6, VOID-NUM); containment 1e-6; Rayleigh exponent control 4.00 +/- 0.02 on x in [1e-4, 1e-3]; substrate floor d >= N_cell*a in substrate units, NOT converted to SI, unexercised | thresholds: eps_T2_max = 1.0e-1; imk_rek_max = 1.0e-1; epsx_max = 1.0; x_G = 1.0e1; N_lambda = 10; N_dom = 10; N_cell = 10; OOM_factor = 1.0e1; grid_n_min = -8; grid_n_max = 8; grid_step = 0.5; tol_edge = 1.0e-6; tol_doubling = 1.0e-8; floor_doubling = 1.0e-6; tol_contain = 1.0e-6; exponent_target = 4.00; exponent_tol = 0.02; interval_equality_tol = 1.0e-6 | VOID never counts as FAIL and is reported distinctly from PASS; a VOID can only widen a window. | Every arm and config applies these rules identically; the mapper asserts this row's values against the locked pre-registration §5 at open (any mismatch is a §5.5 halt). | CLEAN |
| CONV | CONV | conversion constants and conventions | the only place SI values exist in this gate (T4); the transverse-scale import (A-SHEAR lineage, ANNEX-CDEF-1, election E-1(a)) is exercised here and in the Phase-3 mapper only | exact SI defining constants (2019 SI): c = 299792458 m/s; h = 6.62607015e-34 J s; e = 1.602176634e-19 C; k_B = 1.380649e-23 J/K; derived: hbar = h/(2*pi); 1 eV = 1.602176634e-19 J; k(E) = E/(hbar*c) for photon energy E; k(lambda) = 2*pi/lambda; k(nu) = 2*pi*nu/c; length units: 1 au = 149597870700 m (IAU 2012 exact), 1 pc = 648000/pi au = 3.0856775814913673e16 m, 1 Mpc = 1e6 pc; 1 Gyr = 3.15576e16 s (Julian); cosmology for redshift-to-distance (Planck 2018 VI abstract): H0 = 67.4 km/s/Mpc, Omega_m = 0.315, spatially flat, radiation neglected (effect on lookback time below 1e-3 relative for the roster's redshifts, in the conservative direction for the highest); Wien frequency-law constant x_pk = 2.821439372122079 | channel-speed import: c_ch = c = 299792458 m/s under E-1(a) (the aggregate isotropized transverse channel; A-SHEAR lineage; ANNEX-CDEF-1 reading (a)); the domain scale d in metres is the free axis and x = k*d is dimensionless; RULE R1 (distance): for redshift-anchored rows D_ref = D_lt(z) = c * Integral_0^z dz' / ((1+z') * H(z')), H(z) = H0 * sqrt(Omega_m*(1+z)^3 + 1 - Omega_m), the light-travel distance (smaller than the comoving distance: conservative, fewer exclusions); RULE R2 (k-dressing): for redshift-anchored rows every criterion is evaluated at k_obs and at (1+z)*k_obs, and an exclusion is asserted only where BOTH readings exclude (both reported); RULE R3 (brackets): where a row carries a bracket [RECALLED-FLAG] an exclusion is asserted only where both bracket edges exclude (representative reported); RULE R4: every sealed threshold recomputed at x10 and x0.1 (OOM robustness, §5.4) | The import is named, exercised only here and in the sealed mapper, and revocable with the A-SHEAR lineage exactly as W_union; no d is derived; every window is import-conditional. | Phase 3.2: convert each row's reference quantities to k_r and D_r using this row only; the Phase-3 mapper parses this row before any arm row; T4 holds outside this file and the mapper. | CLEAN |

END OF SEALED FILE. Census check string: ROWS=12.

<<<END anchors_G_CI1_SEALED.md>>>

## C-CI-4 RUN-2 RECORD (the S9 evidence: per-arm interval tables, ratio diagnostics, root causes A/B/C, PIN deviation table)
<<<EMBED ci1_ci4_compare.json 756973eeed879738cfa6a6f3586f554a 23880 SCANNED>>>
{
 "gate": "G-CI1",
 "record": "C-CI-4 Phase-3 two-leg comparison + PIN deviation table + S9 assertion",
 "leg": "chat (comparison performer)",
 "utc": "2026-08-22T04:12:31.348160+00:00",
 "provenance": {
  "chat_phase3": [
   "276586f94c8d426c38ff12228c91289d",
   23097
  ],
  "cc_phase3": [
   "e97d9a1cbf94e5e8cd390b99dab87cf0",
   30169
  ],
  "chat_mapper": [
   "49d153e4aa52305407e7887f8e0f6666",
   17242
  ],
  "cc_mapper_md5": "e7c02db36d3bf5942c0844bec9859b55",
  "comparison_run12_of_phases_1_2": "82d04fa6a74a0135b8805189d4305a9e",
  "dispatch": "420082d54f11817c9d64a8198f1042ae"
 },
 "tolerance": 1e-06,
 "verdict_class": {
  "chat": "P-CI-W/EM-IN-WINDOWED",
  "cc": "P-CI-W/EM-IN-WINDOWED",
  "MATCH": true
 },
 "oom_robust": {
  "chat": true,
  "cc": true,
  "MATCH": true
 },
 "W_union": {
  "chat": 3.7641664288e-33,
  "cc": 4.3642401616e-32,
  "reldev": 0.91374978715,
  "MATCH": false,
  "cc_over_chat": 11.594174286,
  "ratio_id": "(2pi)^(4/3)"
 },
 "OOM_bands": {
  "x10": {
   "chat": 8.1096507332e-33,
   "cc": 9.4024703997e-32,
   "cc_over_chat": 11.594174286,
   "ratio_id": "(2pi)^(4/3)"
  },
  "x0.1": {
   "chat": 1.7471712864e-33,
   "cc": 2.0257008401e-32,
   "cc_over_chat": 11.594174285,
   "ratio_id": "(2pi)^(4/3)"
  }
 },
 "per_arm": {
  "hex:step": {
   "TR-1": {
    "MATCH": true,
    "worst_edge_reldev": 0.0,
    "chat_excl": [
     [
      2.6780311672e-09,
      0.47334773405
     ]
    ],
    "cc_excl": [
     [
      2.6780311672e-09,
      0.47334773405
     ]
    ]
   },
   "TR-2": {
    "MATCH": true,
    "worst_edge_reldev": 0.0,
    "chat_excl": [
     [
      1.0599674567e-17,
      1.8207496854e-07
     ]
    ],
    "cc_excl": [
     [
      1.0599674567e-17,
      1.8207496854e-07
     ]
    ]
   },
   "TR-3": {
    "MATCH": false,
    "worst_edge_reldev": 0.91374978715,
    "chat_excl": [
     [
      3.5430384229e-21,
      3.3008862573e-11
     ]
    ],
    "cc_excl": [
     [
      4.1078604976e-20,
      2.0740080032e-10
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 11.594174286,
      "id": "(2pi)^(4/3)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.283185307,
      "id": "2pi"
     }
    ]
   },
   "TR-4": {
    "MATCH": false,
    "worst_edge_reldev": 0.91374978715,
    "chat_excl": [
     [
      3.7641664288e-33,
      5.7057700047e-19
     ]
    ],
    "cc_excl": [
     [
      4.3642401616e-32,
      3.585041026e-18
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 11.594174286,
      "id": "(2pi)^(4/3)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.2831853072,
      "id": "2pi"
     }
    ]
   },
   "ACH-DIM": {
    "MATCH": false,
    "worst_edge_reldev": 5.4406052428e-05,
    "chat_excl": [
     [
      1.5172429595e-15,
      7.2939937256e-07
     ]
    ],
    "cc_excl": [
     [
      1.5171604123e-15,
      7.2939937256e-07
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 0.99994559395,
      "id": "1 (match)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 1.0,
      "id": "1 (match)"
     }
    ]
   },
   "ACH-DISP": {
    "MATCH": false,
    "worst_edge_reldev": 0.84084505691,
    "chat_excl": [
     [
      1.1695208876e-21,
      9.866349023e-12
     ]
    ],
    "cc_excl": [
     [
      7.3483164197e-21,
      6.1992099217e-11
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 6.2831852749,
      "id": "2pi"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.2831853072,
      "id": "2pi"
     }
    ]
   },
   "BIR-1": {
    "MATCH": true,
    "worst_edge_reldev": 0.0,
    "chat_excl": [
     [
      0.66620546222,
      2.3119153034e+24
     ]
    ],
    "cc_excl": [
     [
      0.66620546222,
      2.3119153034e+24
     ]
    ]
   },
   "BIR-2": {
    "MATCH": false,
    "worst_edge_reldev": 0.84084505691,
    "chat_excl": [
     [
      6.1992099217e-11,
      1.0812672472e+25
     ]
    ],
    "cc_excl": [
     [
      3.8950784696e-10,
      1.0812672472e+25
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 6.2831853072,
      "id": "2pi"
     },
     {
      "edge": "hi",
      "cc_over_chat": 1.0,
      "id": "1 (match)"
     }
    ]
   },
   "POL": {
    "MATCH": true,
    "chat": "VOID-NO-CANDIDATE (K empty; ratified F-IRR)",
    "cc": "VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"
   },
   "DIFF": {
    "MATCH": false,
    "worst_edge_reldev": "inf",
    "chat_excl": [
     [
      7.7085928291e-18,
      1.9732698046e-12
     ]
    ],
    "cc_excl": [
     [
      1.002689761e-16,
      "inf"
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 13.007429284,
      "id": "2pi*sqrt(30/7)"
     },
     {
      "edge": "hi",
      "cc_over_chat": "inf",
      "id": "inf-vs-finite (structural)"
     }
    ]
   }
  },
  "hex:gem8": {
   "TR-1": {
    "MATCH": true,
    "worst_edge_reldev": 4.1984672178e-11,
    "chat_excl": [
     [
      2.3818200075e-09,
      0.14968569649
     ]
    ],
    "cc_excl": [
     [
      2.3818200074e-09,
      0.14968569649
     ]
    ]
   },
   "TR-2": {
    "MATCH": true,
    "worst_edge_reldev": 0.0,
    "chat_excl": [
     [
      9.4272677869e-18,
      5.7577160551e-08
     ]
    ],
    "cc_excl": [
     [
      9.4272677869e-18,
      5.7577160551e-08
     ]
    ]
   },
   "TR-3": {
    "MATCH": false,
    "worst_edge_reldev": 0.91374978715,
    "chat_excl": [
     [
      3.1511507058e-21,
      1.043831887e-11
     ]
    ],
    "cc_excl": [
     [
      3.6534990484e-20,
      6.5585891757e-11
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 11.594174286,
      "id": "(2pi)^(4/3)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.2831853073,
      "id": "2pi"
     }
    ]
   },
   "TR-4": {
    "MATCH": false,
    "worst_edge_reldev": 0.91374978714,
    "chat_excl": [
     [
      3.3478202275e-33,
      1.804322902e-19
     ]
    ],
    "cc_excl": [
     [
      3.8815211194e-32,
      1.1336895147e-18
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 11.594174285,
      "id": "(2pi)^(4/3)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.283185307,
      "id": "2pi"
     }
    ]
   },
   "ACH-DIM": {
    "MATCH": false,
    "worst_edge_reldev": 5.4406026441e-05,
    "chat_excl": [
     [
      1.34942404e-15,
      2.3065633412e-07
     ]
    ],
    "cc_excl": [
     [
      1.3493506232e-15,
      2.3065633412e-07
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 0.99994559397,
      "id": "1 (match)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 1.0,
      "id": "1 (match)"
     }
    ]
   },
   "ACH-DISP": {
    "MATCH": false,
    "worst_edge_reldev": 0.84084505824,
    "chat_excl": [
     [
      9.8370793445e-22,
      3.1200135103e-12
     ]
    ],
    "cc_excl": [
     [
      6.180819292e-21,
      1.9603623046e-11
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 6.2831853597,
      "id": "2pi"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.2831853071,
      "id": "2pi"
     }
    ]
   },
   "BIR-1": {
    "MATCH": true,
    "worst_edge_reldev": 0.0,
    "chat_excl": [
     [
      0.66620546222,
      2.3119153034e+24
     ]
    ],
    "cc_excl": [
     [
      0.66620546222,
      2.3119153034e+24
     ]
    ]
   },
   "BIR-2": {
    "MATCH": false,
    "worst_edge_reldev": 0.84084505691,
    "chat_excl": [
     [
      6.1992099217e-11,
      1.0812672472e+25
     ]
    ],
    "cc_excl": [
     [
      3.8950784696e-10,
      1.0812672472e+25
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 6.2831853072,
      "id": "2pi"
     },
     {
      "edge": "hi",
      "cc_over_chat": 1.0,
      "id": "1 (match)"
     }
    ]
   },
   "POL": {
    "MATCH": true,
    "chat": "VOID-NO-CANDIDATE (K empty; ratified F-IRR)",
    "cc": "VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"
   },
   "DIFF": {
    "MATCH": false,
    "worst_edge_reldev": "inf",
    "chat_excl": [
     [
      6.483855064e-18,
      6.2400270206e-13
     ]
    ],
    "cc_excl": [
     [
      8.4338287368e-17,
      "inf"
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 13.007429459,
      "id": "2pi*sqrt(30/7)"
     },
     {
      "edge": "hi",
      "cc_over_chat": "inf",
      "id": "inf-vs-finite (structural)"
     }
    ]
   }
  },
  "cubic:step": {
   "TR-1": {
    "MATCH": true,
    "worst_edge_reldev": 0.0,
    "chat_excl": [
     [
      2.3207011113e-09,
      0.14968569649
     ]
    ],
    "cc_excl": [
     [
      2.3207011113e-09,
      0.14968569649
     ]
    ]
   },
   "TR-2": {
    "MATCH": true,
    "worst_edge_reldev": 1.0886939782e-11,
    "chat_excl": [
     [
      9.1853585752e-18,
      5.7577160551e-08
     ]
    ],
    "cc_excl": [
     [
      9.1853585751e-18,
      5.7577160551e-08
     ]
    ]
   },
   "TR-3": {
    "MATCH": false,
    "worst_edge_reldev": 0.91374978715,
    "chat_excl": [
     [
      3.0702903335e-21,
      1.043831887e-11
     ]
    ],
    "cc_excl": [
     [
      3.5597481234e-20,
      6.5585891757e-11
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 11.594174286,
      "id": "(2pi)^(4/3)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.2831853073,
      "id": "2pi"
     }
    ]
   },
   "TR-4": {
    "MATCH": false,
    "worst_edge_reldev": 0.91374978715,
    "chat_excl": [
     [
      3.2619132e-33,
      1.804322902e-19
     ]
    ],
    "cc_excl": [
     [
      3.7819190146e-32,
      1.1336895147e-18
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 11.594174286,
      "id": "(2pi)^(4/3)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.283185307,
      "id": "2pi"
     }
    ]
   },
   "ACH-DIM": {
    "MATCH": false,
    "worst_edge_reldev": 5.4406040189e-05,
    "chat_excl": [
     [
      1.314797029e-15,
      2.3065633412e-07
     ]
    ],
    "cc_excl": [
     [
      1.3147254961e-15,
      2.3065633412e-07
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 0.99994559396,
      "id": "1 (match)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 1.0,
      "id": "1 (match)"
     }
    ]
   },
   "ACH-DISP": {
    "MATCH": false,
    "worst_edge_reldev": 0.84084505827,
    "chat_excl": [
     [
      9.3775765831e-22,
      3.1200135103e-12
     ]
    ],
    "cc_excl": [
     [
      5.8921051907e-21,
      1.9603623046e-11
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 6.2831853608,
      "id": "2pi"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.2831853071,
      "id": "2pi"
     }
    ]
   },
   "BIR-1": {
    "MATCH": true,
    "worst_edge_reldev": 0.0,
    "chat_excl": [
     [
      0.66620546222,
      2.3119153034e+24
     ]
    ],
    "cc_excl": [
     [
      0.66620546222,
      2.3119153034e+24
     ]
    ]
   },
   "BIR-2": {
    "MATCH": false,
    "worst_edge_reldev": 0.84084505691,
    "chat_excl": [
     [
      6.1992099217e-11,
      1.0812672472e+25
     ]
    ],
    "cc_excl": [
     [
      3.8950784696e-10,
      1.0812672472e+25
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 6.2831853072,
      "id": "2pi"
     },
     {
      "edge": "hi",
      "cc_over_chat": 1.0,
      "id": "1 (match)"
     }
    ]
   },
   "POL": {
    "MATCH": true,
    "chat": "VOID-NO-CANDIDATE (K empty; ratified F-IRR)",
    "cc": "VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"
   },
   "DIFF": {
    "MATCH": false,
    "worst_edge_reldev": "inf",
    "chat_excl": [
     [
      6.1809857669e-18,
      6.2400270206e-13
     ]
    ],
    "cc_excl": [
     [
      8.0398736366e-17,
      "inf"
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 13.007429462,
      "id": "2pi*sqrt(30/7)"
     },
     {
      "edge": "hi",
      "cc_over_chat": "inf",
      "id": "inf-vs-finite (structural)"
     }
    ]
   }
  },
  "cubic:gem8": {
   "TR-1": {
    "MATCH": true,
    "worst_edge_reldev": 0.0,
    "chat_excl": [
     [
      2.0764446741e-09,
      0.14968569649
     ]
    ],
    "cc_excl": [
     [
      2.0764446741e-09,
      0.14968569649
     ]
    ]
   },
   "TR-2": {
    "MATCH": true,
    "worst_edge_reldev": 0.0,
    "chat_excl": [
     [
      8.2185891153e-18,
      5.7577160551e-08
     ]
    ],
    "cc_excl": [
     [
      8.2185891153e-18,
      5.7577160551e-08
     ]
    ]
   },
   "TR-3": {
    "MATCH": false,
    "worst_edge_reldev": 0.91374978715,
    "chat_excl": [
     [
      2.7471387762e-21,
      1.043831887e-11
     ]
    ],
    "cc_excl": [
     [
      3.1850805759e-20,
      6.5585891757e-11
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 11.594174286,
      "id": "(2pi)^(4/3)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.2831853073,
      "id": "2pi"
     }
    ]
   },
   "TR-4": {
    "MATCH": false,
    "worst_edge_reldev": 0.91374978715,
    "chat_excl": [
     [
      2.9185931177e-33,
      1.804322902e-19
     ]
    ],
    "cc_excl": [
     [
      3.3838677276e-32,
      1.1336895147e-18
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 11.594174286,
      "id": "(2pi)^(4/3)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.283185307,
      "id": "2pi"
     }
    ]
   },
   "ACH-DIM": {
    "MATCH": false,
    "worst_edge_reldev": 5.4406056563e-05,
    "chat_excl": [
     [
      1.176413143e-15,
      2.3065633412e-07
     ]
    ],
    "cc_excl": [
     [
      1.176349139e-15,
      2.3065633412e-07
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 0.99994559394,
      "id": "1 (match)"
     },
     {
      "edge": "hi",
      "cc_over_chat": 1.0,
      "id": "1 (match)"
     }
    ]
   },
   "ACH-DISP": {
    "MATCH": false,
    "worst_edge_reldev": 0.84084505691,
    "chat_excl": [
     [
      7.9492594737e-22,
      3.1200135103e-12
     ]
    ],
    "cc_excl": [
     [
      4.9946667481e-21,
      1.9603623046e-11
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 6.283184949,
      "id": "2pi"
     },
     {
      "edge": "hi",
      "cc_over_chat": 6.2831853071,
      "id": "2pi"
     }
    ]
   },
   "BIR-1": {
    "MATCH": true,
    "worst_edge_reldev": 0.0,
    "chat_excl": [
     [
      0.66620546222,
      2.3119153034e+24
     ]
    ],
    "cc_excl": [
     [
      0.66620546222,
      2.3119153034e+24
     ]
    ]
   },
   "BIR-2": {
    "MATCH": false,
    "worst_edge_reldev": 0.84084505691,
    "chat_excl": [
     [
      6.1992099217e-11,
      1.0812672472e+25
     ]
    ],
    "cc_excl": [
     [
      3.8950784696e-10,
      1.0812672472e+25
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 6.2831853072,
      "id": "2pi"
     },
     {
      "edge": "hi",
      "cc_over_chat": 1.0,
      "id": "1 (match)"
     }
    ]
   },
   "POL": {
    "MATCH": true,
    "chat": "VOID-NO-CANDIDATE (K empty; ratified F-IRR)",
    "cc": "VOID-NO-CANDIDATE (K empty; CI-W/EM-IN face)"
   },
   "DIFF": {
    "MATCH": false,
    "worst_edge_reldev": "inf",
    "chat_excl": [
     [
      5.2395476836e-18,
      6.2400270206e-13
     ]
    ],
    "cc_excl": [
     [
      6.8153042438e-17,
      "inf"
     ]
    ],
    "ratio_diagnostics": [
     {
      "edge": "lo",
      "cc_over_chat": 13.007428609,
      "id": "2pi*sqrt(30/7)"
     },
     {
      "edge": "hi",
      "cc_over_chat": "inf",
      "id": "inf-vs-finite (structural)"
     }
    ]
   }
  }
 },
 "match_arms_worst_edge_reldev": 4.1984672178e-11,
 "PIN_CC_P3_deviation_table": [
  {
   "pin": "PIN-CC-P3-1 (named-key binders; loud masked halt)",
   "chat_status": "SAME DESIGN; two loud pre-verdict halts fired and were repaired before any verdict output: H-14 (CONV constants bound from the row's 5th/anchor-slot field; params field carries the channel-speed import + R1-R4) and H-15 (D_lt doubling-gate halt at the largest z; resolved by log-substitution Simpson at higher resolution, gate unchanged at 1e-10)",
   "deviation": "none in protocol"
  },
  {
   "pin": "PIN-CC-P3-2 (D_lt composite Simpson n=4096, 1e-10)",
   "chat_status": "u = ln(1+z) Simpson 2^14/2^15, doubling <= 1e-10 asserted per z; inter-leg D_lt agreement evidenced at the sub-10 sealed z values by TR-1, TR-2, BIR-1 (edges embed D_lt(z); agree at <= 4.2e-11); at the largest sealed z (the CMB epoch) the ACH-DIM onset edge diverges by ~5e-5 in the D^(-1/3) pattern of a D_lt error of ~1.5e-4 — consistent with truncation of a fixed-n linear-z Simpson ladder at that z (the chat leg's own linear-z 2048/4096 ladder failed its 1e-10 doubling gate exactly there and was replaced by a log-substitution ladder, H-15; the D-independent ACH-DIM validity edge agrees between the legs)",
   "deviation": "S9 component (C): ACH-DIM onset, small-magnitude, largest-z-specific; CC-side re-derivation with a doubling check at that z requested"
  },
  {
   "pin": "PIN-CC-P3-3 (24/decade scan + 64-step bisection)",
   "chat_status": "24/decade + 60-step geometric bisection; edge resolution orders below the 1e-6 comparison tolerance on both legs",
   "deviation": "none material"
  },
  {
   "pin": "PIN-CC-P3-4 (curve lookups from own Phase-2 tables; Rayleigh tails below 1e-4)",
   "chat_status": "same class; C-CI-2/3 bounded the inter-leg curve agreement at <= 1.14e-7",
   "deviation": "none material"
  },
  {
   "pin": "PIN-CC-P3-5 (conservative combiner: mixed EXCL/VOID may classify as VOID; classification-only divergence expected)",
   "chat_status": "one structural divergence surfaced BEYOND classification-only: the DIFF upper edge (cc: unbounded exclusion; chat: validity-capped, VOID beyond x_S with no ray grant per election E-11 and the section-5.4 gap rule — a VOID can only widen a window)",
   "deviation": "S9 component (iii) of A-DIFF"
  }
 ],
 "cc_pins_verbatim": [
  "PIN-CC-P3-1: role binding of sealed params cells is by named-key regex with per-row binders; a binder failure is a loud masked halt, no silent fallback.",
  "PIN-CC-P3-2: D_lt(z) by composite Simpson, n=4096 (doubling-checked at bind time to 1e-10 relative).",
  "PIN-CC-P3-3: window edges by per-decade-24 log scan + 64-step geometric bisection (edge resolution far below the 1e-6 comparison tolerance).",
  "PIN-CC-P3-4: curve lookups are log-log interpolations of this leg's own Phase-2 tables; certified Rayleigh tails below x = 1e-4.",
  "PIN-CC-P3-5: the conservative reading combiner (R2 x R3 product space) may classify a mixed EXCL/VOID point as VOID where the chat leg might bridge differently; any such divergence is classification-only (S9-lite class)."
 ],
 "S9": {
  "FIRES": true,
  "miss_arms": [
   "ACH-DIM",
   "ACH-DISP",
   "BIR-2",
   "DIFF",
   "TR-3",
   "TR-4"
  ],
  "match_arms": [
   "TR-1",
   "TR-2",
   "BIR-1",
   "POL"
  ],
  "root_cause_primary": "k(E) conversion divergence on every energy-anchored arm (TR-3, TR-4, ACH-DISP, BIR-2, DIFF): the sealed CONV row pins k(E) = E/(hbar*c); the CC edges are exactly consistent with k(E) = E/(h*c) — a factor 2pi low — as proven by the edge ratios: Rayleigh-onset edges shift by (2pi)^(4/3) (onset d ~ k^(-4/3)), validity/cutoff edges and the N_lambda live-edge by 2pi (d ~ 1/k), and the A-DIFF onset by 2pi*sqrt(30/7) (the k factor combined with the band-edge choice). The CC leg is additionally internally inconsistent: its wavelength/frequency arms (TR-1, TR-2, ACH-DIM, BIR-1) use the sealed k(lambda) = 2pi/lambda and k(nu) = 2pi*nu/c and MATCH the chat leg (TR-1, TR-2, BIR-1 at <= 4.2e-11), while its energy arms drop the 2pi. The sealed text is dispositive (E-2 class: convention fixed pre-evaluation in the sealed CONV row; the chat leg's Read #2 binds it verbatim). ACH-DIM is a separate, non-2pi miss — see root_cause_tertiary_ACH_DIM.",
  "root_cause_secondary_DIFF": "(ii) band-edge selection: the sealed sign map makes the in-model differential negative, so the negative band edge binds; the CC onset is consistent with the positive edge; (iii) upper-edge treatment: cc extends exclusion beyond wave validity (unbounded), chat caps at the strongest-reading validity edge and returns VOID beyond (election E-11: no ray-regime grant; a VOID can only widen a window).",
  "root_cause_tertiary_ACH_DIM": "the ACH-DIM onset edge (the only arm at the CMB-epoch sealed z) diverges by ~5e-5 with cc/chat = 0.99995 on the lower edge only — no 2pi-class factor; the D-independent validity edge agrees. The pattern matches a ~1.5e-4 relative D_lt(1090) difference through the onset's D^(-1/3) scaling. Leading candidate: fixed-n linear-z Simpson truncation at that z on the CC leg (PIN-CC-P3-2: a z-step of ~0.3 there), which is exactly where the chat leg's own linear-z ladder loudly failed its 1e-10 doubling gate before being replaced (H-15); the chat log-substitution ladder passes the gate there with orders of margin. Attribution is CC-confirmable in the S9 re-derivation; no sealed-text dispute is involved on this arm.",
  "resolution_paths": [
   "(a) CC re-derivation mini-dispatch (one P-4 file): re-derive the five energy-anchored arms from the sealed CONV text (k(E) = E/(hbar*c); negative band edge on A-DIFF; validity-capped upper edges per E-11) AND re-derive the ACH-DIM onset with a D_lt ladder that passes a 1e-10 doubling gate AT the largest sealed z; then C-CI-4 re-run. Expected outcome: convergence to the chat Read #2 edges; W_union of record (0, 3.76416643e-33].",
   "(b) author ruling now: the sealed text is dispositive; adopt the chat Read #2 edges as the numeric window of record, with the CC mini-verification to follow before fold. Both paths leave the verdict CLASS and OOM-robustness unchanged (already two-leg confirmed)."
  ],
  "what_is_already_two_leg_confirmed": "verdict class P-CI-W/EM-IN-WINDOWED; OOM-ROBUST; F-IRR FIRES / K empty (T3); the five sealed-conformant arms; PF-1 suspension handling; POL VOID-NO-CANDIDATE.",
  "fold_gate": "fold staging BLOCKED until the author closes S9 by path (a) or (b)."
 },
 "lineage": {
  "run1_superseded": {
   "md5": "e506e042f4f06cff8a719f2eaf0ae1f0",
   "bytes": 21668,
   "kept_at": "/home/claude/g_ci1_cc_return/ci1_ci4_compare_run1_superseded.json",
   "why": "H-16: run 1's PIN-P3-2 prose and the primary-root-cause sentence still listed ACH-DIM among the matching arms (stale pre-run expectation text), while the same run's machine table correctly flagged the ACH-DIM miss; prose corrected in run 2; no gate, interval, ratio, or verdict changed"
  }
 },
 "H": [
  "G-CI1.H-16 (chat): the run-1 comparator carried stale pre-run-expectation prose (ACH-DIM listed among matching arms) alongside a correct machine table; caught on first read of the run-1 output; corrected in run 2 with run 1 retained in workspace lineage; no number changed.",
  "G-CI1.H-15 (chat): the mapper's D_lt doubling gate halted loudly on first execution at the largest sealed z; resolved by a log-substitution Simpson ladder at higher resolution with the same 1e-10 gate; a numpy import was added in the same repair; no verdict output existed before the repair.",
  "G-CI1.H-13 and G-CI1.H-14 are embedded in the Phase-3 chat checkpoint (authorization hash mis-cite noted and corrected; CONV field-map fix caught by a masked binder halt)."
 ],
 "T1": {
  "instrument_hits": 0,
  "checkpoint_hits": 0,
  "float_digits": 11,
  "checkpoint_hits_final": 0
 }
}
<<<END ci1_ci4_compare.json>>>

## PHASE-3 CLOSURE MEMO (context; the author has elected path (a) of its section 6)
<<<EMBED G_CI1_PHASE3_CLOSURE_MEMO.md dd1a02eca875211755b0cf5915ac769c 8062 SCANNED>>>
# G_CI1_PHASE3_CLOSURE_MEMO.md — Gate G-CI1, Phase 3 closure (DRAFT for the author's review; fold staging deferred)

**Date:** August 21, 2026. **Status:** Phase 3 executed on both legs; C-CI-1…C-CI-4 complete. **The verdict CLASS is two-leg confirmed. The numeric window is under S9** (six-arm interval divergence, root-caused below). **Fold staging is BLOCKED until the author closes S9** by path (a) or (b) of §6.

## 1. Provenance chain
Prereg `6c480340` LOCKED; T1 list `653a0b74` FROZEN; sealed anchor file `dd8fe2d3` (census 12); lock record `a6adbb6a` + Addenda 1–3 (`e5029ae8` / `92672d5a` / `4c0b52c6`); dispatch `420082d5` (109,192 B). Chat: phase 0 `b0498568`; resupply `d99d21b2`; phase 1 `9d8e40b8`; phase 2 `ee61b4b1`; C-CI-1…3 comparison (run 2 of record) `82d04fa6`; **Chat Read #2 checkpoint `276586f94c8d426c38ff12228c91289d` (23,097 B), mapper `49d153e4` (17,242 B)**; **C-CI-4 comparison (run 2 of record) `756973eeed879738cfa6a6f3586f554a` (23,880 B), comparator `1c968ee0`**. CC (X-1 ALL PASS at byte level, repo commit ca012a5): phases 0–3 `a82462c4` / `b85ac5cf` / `f79113b7` / `e97d9a1c`; report `30ac9ef6`. Canonical base V4.76 `f539d10c`. T1: zero hits on every chat and CC artifact (independent chat-side re-scan included).

## 2. Verdict of record (two-leg confirmed)
**Verdict class `P-CI-W/EM-IN-WINDOWED`, OOM-ROBUST — identical on both legs.** F-IRR FIRES, K = ∅ (T3-immutable, author-ratified); CI-S FALSIFIED-STRUCTURAL; **CI-W/EM-IN is the operative branch**; A-POL is VOID-NO-CANDIDATE on both legs. Per PF-1 the G-POLY1 window (0, 2.1213132100130068] stays **SUSPENDED** from the Phase-3 intersection and is reported alongside only; the radiative component of the B-2 burden transfers to the S2-on-cone assumption, not discharged.

## 3. The two reads (window edges in SI length units)
**CC Read #1 (the verdict read of record, E-9):** W^EM_union = (0, 4.3642402e-32]; per config 4.3642e-32 / 3.8815e-32 / 3.7819e-32 / 3.3839e-32; OOM ×10 union 9.4025e-32, ×0.1 union 2.0257e-32.
**Chat Read #2 (sealed-conformant):** W^EM_union = (0, **3.76416643e-33**]; per config 3.7642e-33 / 3.3478e-33 / 3.2619e-33 / 2.9186e-33; OOM ×10 union 8.1097e-33, ×0.1 union 1.7472e-33.
Every union and OOM edge differs by the single factor **(2π)^(4/3) = 11.59417, exact to 1e-5** — the fingerprint of one convention divergence, not of independent numerical scatter.

## 4. C-CI-4 result
**MATCH (≤ 1e-6, actual worst 4.2e-11): TR-1, TR-2, BIR-1, POL** — the frequency/wavelength arms and the no-candidate arm, on all four configs. **MISS (S9): TR-3, TR-4, ACH-DISP, BIR-2, DIFF, ACH-DIM.** Ratio diagnostics (cc/chat, identical across configs):
- TR-3, TR-4: onset ×(2π)^(4/3); validity cutoff ×2π.
- ACH-DISP: both edges ×2π. BIR-2: N_λ live-edge ×2π; upper edge identical (N-rule, k-independent).
- DIFF: onset ×13.00743 = 2π·√(30/7) (the k factor combined with the band-edge choice); upper edge structural — CC unbounded, chat validity-capped (VOID beyond, per election E-11).
- ACH-DIM: onset −5.441e-5 relative (cc/chat = 0.99995), **identical on all four configs**, with the D-independent validity edge **identical to machine precision** — not a 2π-class miss.

## 5. S9 assertion — root causes
**(A) Primary — k(E) conversion (arms TR-3, TR-4, ACH-DISP, BIR-2, DIFF).** The sealed CONV row pins k(E) = E/(ħc). The CC edges are exactly consistent with k(E) = E/(hc) — a factor 2π low — as proven by the edge ratios in §4. The CC leg is internally inconsistent: its frequency/wavelength arms use the sealed k(λ) = 2π/λ and k(ν) = 2πν/c and match the chat leg at 4.2e-11, while its energy arms drop the 2π. **The sealed text is dispositive** (E-2 class: the convention was fixed pre-evaluation in the sealed CONV row; Chat Read #2 binds it verbatim). The chat conversion is also the self-consistent one: k(λ) = 2π/λ and k(E) = E/(ħc) agree identically at E = hc/λ.
**(B) Secondary — A-DIFF only.** (ii) Band edge: the sealed sign map makes the in-model differential negative, so the negative band edge binds; the CC onset is consistent with the positive edge. (iii) Upper edge: CC extends exclusion beyond wave validity (unbounded); chat caps at the strongest-reading validity edge and returns VOID beyond — per election **E-11** (no ray-regime grant; a VOID can only widen a window) and the §5.4 gap rule.
**(C) Tertiary — ACH-DIM onset.** The only arm at the CMB-epoch sealed z. The −5.44e-5 shift is config-independent and absent from the D-independent edge — the exact signature of a **D_lt difference of ~1.6e-4 relative** through the onset's D^(−1/3) scaling. Leading candidate: fixed-step linear-z Simpson truncation at that z on the CC leg (PIN-CC-P3-2; z-step ~0.3 there). Independent evidence: the chat leg's own linear-z 2048/4096 ladder **loudly failed its 1e-10 doubling gate at exactly that z** (H-15) and was replaced by a log-substitution ladder that passes with orders of margin. CC-confirmable; no sealed-text dispute on this arm.

## 6. Resolution paths (author's election)
**(a) — recommended.** One P-4 mini-dispatch: the CC leg re-derives the five energy-anchored arms from the sealed CONV text (k(E) = E/(ħc); negative band edge on A-DIFF; validity-capped upper edges per E-11) **and** re-derives the ACH-DIM onset with a D_lt ladder that passes a 1e-10 doubling gate at the largest sealed z; then C-CI-4 re-run. Expected: convergence to the Chat Read #2 edges; **W_∪ of record = (0, 3.76416643e-33] SI length units** (about one order tighter than the CC read).
**(b).** Author rules now that the sealed text is dispositive and adopts the Chat Read #2 edges as the numeric window of record, with the CC mini-verification to follow before fold.
Either path leaves §2 unchanged: the class, OOM-robustness, F-IRR, the operative branch, and the four matched arms are already two-leg settled. Under E-9, CC Read #1 remains the verdict read of record for the CLASS; the S9 procedure governs only the six divergent interval sets.

## 7. Honesty ledger, this phase
Chat: **H-11** (author-pasted CC report disclosed headline windows pre-read; CC-blind-first architecture unaffected); **H-12** (comparator over-gating in C-CI-3 run 1; spurious S9; corrected, run superseded and retained); **H-13** (the authorizing directive cited the G-POLY1 seal hash; the G-CI1 seal `dd8fe2d3` was asserted and used; intent unambiguous); **H-14** (CONV field-map: the sealed CONV row carries the SI-constants text in its anchor-slot field and the channel-speed import + R1–R4 in params; caught by a loud masked binder halt pre-verdict); **H-15** (D_lt doubling-gate halt at the largest sealed z; log-substitution ladder, same 1e-10 gate); **H-16** (run-1 C-CI-4 prose carried stale pre-run expectation text alongside a correct machine table; corrected in run 2, run 1 retained; a T1 invocation self-grep halted one intermediate comparator edit — a dialect token in new prose — reworded, zero output consumed). CC: H-CC-1…H-CC-7 as reported, accepted into the record. **PIN-CH-P3-1 verified:** the pre-declared expectation (energy-arm 2π-class divergence; wavelength-arm agreement; DIFF band-edge and cap structure) was realized in full; ACH-DIM was the one un-predicted miss, now attributed under (C).

## 8. Fold staging (deferred to the author; blocked until S9 closes)
Target V4.77-class fold after S9 closure: **§2.91.N** (G-CI1 verdict, both reads, the S9 record and its closure, W^EM_∪ of record, per-config edges, OOM bands, PF-1 suspension note); **Part VI row** (gate G-CI1: P-CI-W/EM-IN-WINDOWED, OOM-ROBUST, two-leg); **§2.91.M annotation** (W_∪ conditionality per PF-1). Standard anchored-splice script with anchor-uniqueness assertions and reverse-splice byte verification against V4.76 `f539d10c`. If path (b) is elected, the fold carries an explicit S9-closure annotation and attaches the CC verification receipt when it returns.

*Standing untouched: §2.52 Open 3 (frozen), §2.87.J (reserved), OP-2.58.2d, P-LEX-1.*

<<<END G_CI1_PHASE3_CLOSURE_MEMO.md>>>
