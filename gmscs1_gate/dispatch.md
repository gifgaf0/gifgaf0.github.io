# G-MSCS1 — CC LEG DISPATCH (P-4 single-file in-band; P-4.b armor; P-4.c lone delivery)

**Gate:** G-MSCS1 (Multi-Species Channel Speed: the Q3(1) carrier-identity residue and the emergent species-universality obligation). **Date:** September 19, 2026.
**Base ledger:** `SQT_Master_Ledger_v4_82_CANONICAL.md` md5 `d095a7003bb0d4c177e7451e1d14c4c6`.
**Lock chain (all FROZEN):** memo v2 `3f30262eaec461fb5fd3202835f7de37` (34,837 B) · lock record `3dbe953badb6c030ef1d449adbac2044` (with Addendum A-2 operationalizations) · comparator v1.0 `22432b292ae0a9d5c91a6cb7aa67502f` · schema v1.0 `76a42db3fd6ad82e485752bc2ddb24d5` · T1 gate list `fef2827100d3f85e0a6341b44f0c00bf` (36 patterns; scanner `6b86290090a8c84f1b1a0a99ec0bf697`).
**Elections (T3):** E-MS-1(a) · E-MS-2(a) · E-MS-2b (a)+(b) · E-MS-2c ⟨001⟩+⟨111⟩ · E-MS-3(a) (Born at t = 0 only) · E-MS-4(a) · E-MS-5(a) · E-MS-6(a). Amendment A-1 authorized.
**Chat-leg state at dispatch:** run + compare EXECUTED (checkpoint `c04c0b8ea34cfe60f231aa06828e6ce4`, compare `7b933c08b92d57b9523f2cee4ff076ba`); all Phase-0 controls PASS; verdict class IDENTITY-DELIVERED; H-MS-2/H-MS-3/H-MS-4 chat-side (§6 below). **D-T1 RETIRED:** the T1 list is embedded here; your instrument must halt without it.

**T1-scan exemptions (the G-POLY1 justified-exemption class):** the two list embeds (`tools/t1/T1_forbidden_G_MSCS1.txt`, `tools/t1/T1_base_author_20260919.txt`) necessarily contain every pattern; the dispatch minus those two embeds scans CLEAN (3 numeric formatting collisions, 0 hits).

**ACTIVATION FLAG: `ACTIVATE: G-MSCS1-CC-LEG-1`** — proceed only if this line is present verbatim.

## 0. Blindness clause (read first)

Four embeds are **QUARANTINED** (base64-armored): the chat instrument, checkpoint, compare file, and execution report. **Do not decode them until step 4.** Build your instrument from the memo (§2, §4, §A), the lock record (Addendum A-2 operationalizations — binding definitions) and the schema ONLY, from scratch, in your own structure. Commit your checkpoint BEFORE any armor is opened and cite that commit as the pre-consultation checkpoint. If your read of this file is paged or truncated, locate embed boundaries by grepping sentinel lines only (the G-QUANTA H-CC-2 practice).

## 1. Embed inventory

| Embed | md5 | Size | Handling |
|---|---|---|---|
| `staging_memo_G_MSCS1_v2.md` | `3f30262eaec461fb5fd3202835f7de37` | 34,837 B | plain |
| `G_MSCS1_LOCK_RECORD.md` | `3dbe953badb6c030ef1d449adbac2044` | 7,289 B | plain |
| `g_mscs1_compare_v1_0.py` | `22432b292ae0a9d5c91a6cb7aa67502f` | 18,541 B | plain |
| `g_mscs1_schema_v1_0.json` | `76a42db3fd6ad82e485752bc2ddb24d5` | 3,906 B | plain |
| `tools/t1/T1_forbidden_G_MSCS1.txt` | `fef2827100d3f85e0a6341b44f0c00bf` | 1,433 B | plain |
| `tools/t1/t1_scan.py` | `6b86290090a8c84f1b1a0a99ec0bf697` | 1,967 B | plain |
| `tools/t1/T1_base_author_20260919.txt` | `05302210cc4ceb70553acbe8379e9fc3` | 143 B | plain |
| `inputs/poly_vrh_results.json` | `200e7a8b775577564369c6924d38a84c` | 2,767 B | plain |
| `inputs/cc_p2_phase1.json` | `aaae206733b0f0a378a5c6b600274d3f` | 11,454 B | plain |
| `inputs/poly1_phase1full_cc.json` | `ec87e42f0f617b00c4985ba2aceac339` | 8,140 B | plain |
| `inputs/chatleg_phase0bfull.json` | `df413a7cfa30e599b779af8fee5d07d1` | 1,920 B | plain |
| `g_mscs1_chatleg.py` | `db5f51dd9ef7f54dd0826991d594681b` | 34,606 B | QUARANTINED (base64) |
| `g_mscs1_chatleg_checkpoint.json` | `c04c0b8ea34cfe60f231aa06828e6ce4` | 33,289 B | QUARANTINED (base64) |
| `g_mscs1_chatleg_compare.json` | `7b933c08b92d57b9523f2cee4ff076ba` | 3,277 B | QUARANTINED (base64) |
| `G_MSCS1_CHATLEG_EXECUTION_REPORT.md` | `3cf78f51962359a25fac13f968cba119` | 12,608 B | QUARANTINED (base64) |

## 2. Verify-then-build

Save this file as `dispatch.md`, then run the extractor below **without** `--decode-quarantined` (it recreates `tools/t1/` and `inputs/`):

```python
import base64, hashlib, os, re, sys
src = open(sys.argv[1], 'rb').read()
pat = re.compile(rb'=====BEGIN-EMBED name=(\S+) md5=([0-9a-f]{32}) bytes=(\d+) encoding=(raw|base64)(?: armor_bytes=(\d+))?[^\n]*\n')
pos = 0
while True:
    m = pat.search(src, pos)
    if not m: break
    name, want, n, enc, armor = m.group(1).decode(), m.group(2).decode(), int(m.group(3)), m.group(4).decode(), m.group(5)
    start = m.end()
    if enc == 'raw':
        payload = src[start:start + n]
    else:
        if '--decode-quarantined' not in sys.argv:
            print(f'SKIP {name} (quarantined; not decoded)'); pos = start; continue
        payload = base64.decodebytes(src[start:start + int(armor)])
    got = hashlib.md5(payload).hexdigest()
    assert got == want and len(payload) == n, f'{name}: md5 {got} != {want} or length {len(payload)} != {n}'
    os.makedirs(os.path.dirname(name) or '.', exist_ok=True)
    open(name, 'wb').write(payload); print(f'OK   {name}  {got}  {n:,} B'); pos = start
```

Expected: eleven `OK` lines and four `SKIP` lines. Any assertion failure → HALT, report the md5 seen, do not build. Run `python3 tools/t1/t1_scan.py tools/t1/T1_forbidden_G_MSCS1.txt staging_memo_G_MSCS1_v2.md G_MSCS1_LOCK_RECORD.md` → both CLEAN.

## 3. Build and run (blind)

1. Read the memo §A, §0–§2, §4–§6 and the lock record §5 (A-2.1–A-2.6: pin sources, kernel construction, HS operationalization, fit/halving, quadrature and labels, control tensors). These definitions are binding; where the memo and A-2 differ in specificity, A-2 governs.
2. Write `g_mscs1_ccleg.py` from scratch. Requirements: md5-guard the memo (`3f30262e…`, 34,837 B), X-1 (`200e7a8b…`, 2,767 B) and the pin sources X-3/X-4/X-5 (A-2.1) before any computation; T1 self-grep of your instrument and the memo at every invocation (gate list md5 asserted; halt without it; scan rule = `t1_scan.py`); Phase 0 controls exactly as listed in memo §4 / A-2.6 (halt → INDETERMINATE on any failure); Phase 1 on the eight configuration keys (`hex_step|a`, `hex_step|b`, `hex_gem8|a`, `hex_gem8|b`, `cubic_step|001`, `cubic_step|111`, `cubic_gem8|001`, `cubic_gem8|111`); Phase 2 on the pinned 12-point t-grid with VRH (Hill = ½(C_V + C_R)) primary and the HS scheme per A-2.3; the {t, t², t³} fit over |t| ≤ 0.25 with the half-window check per A-2.4; the sphere quadrature GL(cos θ) 64 × uniform φ 128 with the 128×256 doubling on r_xtal_E2 (A-2.5). **Requested variation (independence upgrade):** use a different SO(3) product grid than (16, 10, 16) and (12, 8, 12) — e.g. (20, 12, 20) — and evaluate the μ-moments I₀, I₂ by a different exact route (a degree-8 polynomial fit on Chebyshev nodes, or GL of a different order); use your own Mandel/Voigt conventions and your own branch-labelling implementation.
3. **Implement F-CTRL-ADMIX as the memo states it** (memo §4: replace every quasi-transverse eigenvector by its transverse projection, recompute r_xtal(S2-h); expected 0 within τ_agg) and report the number — the chat leg's implementation was tautological (H-MS-3, disclosed in the quarantined report; do not read it before step 4).
4. Emit `g_mscs1_ccleg_checkpoint.json` conforming to `g_mscs1_schema_v1_0.json` (required_keys, phase1/phase2/born_t0 keys, value domains; `leg` = `cc`; real `instrument_md5`; elections strings starting with the canonical codes `(a)`, `(a+b)`, `(001+111)`; `T1.state` = CLEAN). **Commit** with the checkpoint md5 in the message — the pre-consultation checkpoint.
5. Emit `g_mscs1_ccleg_compare.json` (rows `H-MS-1..5` with `id`, `concordant`; `verdict_class`), the LAST computation.

## 4. Consult and compare

Only now: `python3 extract.py dispatch.md --decode-quarantined`, then

```
python3 g_mscs1_compare_v1_0.py compare --chat g_mscs1_chatleg_checkpoint.json --cc g_mscs1_ccleg_checkpoint.json \
  --chat-cmp g_mscs1_chatleg_compare.json --cc-cmp g_mscs1_ccleg_compare.json --schema g_mscs1_schema_v1_0.json \
  --out g_mscs1_twoleg_comparison.json
```

**Pre-declared expected misses (H-MS-2, definitional):** the four cubic keys' `halving_dev_kappa2` items on BOTH legs (8 items) — κ₂ ≡ 0 on cubic under an l = 2 texture (a symmetry null, see the report after decoding), so the relative halving criterion is 0/0. Do NOT alter your checkpoint to avoid them. Every other check is expected to PASS; any other MISS is a genuine S9 item — classify representational vs definitional in your return; never edit either checkpoint. The comparator and schema are frozen; if you believe either is wrong, say so in H-CC and leave them unchanged. A comparator v1.1 (halving with a floored denominator max(|κ₂|, 10⁻⁶)) will be frozen chat-side only on the author's S9 election.

## 5. Return (single file, P-4 mirrored)

One markdown file with byte-exact embeds (same sentinel format) of `g_mscs1_ccleg.py`, `g_mscs1_ccleg_checkpoint.json`, `g_mscs1_ccleg_compare.json`, `g_mscs1_twoleg_comparison.json`; the branch name and commit hashes (pre-consultation first); CC-DD-1..n; H-CC-1..n; deviations; T1 state; the F-CTRL-ADMIX number; run time.

## 6. Chat-side honesty items and deviations carried (for the record; details in the quarantined report)

- **H-MS-2** — halving criterion undefined at κ₂ = 0 (cubic keys); pre-classified definitional; expected 8 comparator misses.
- **H-MS-3** — chat F-CTRL-ADMIX tautological as coded; CC asked to implement it substantively.
- **H-MS-4** — pre-lock self-test catch: the banked hex tensors are tetragonal-form; qSH decouples exactly only on arm (b); labels on arm (a) by maximum overlap.
- T1: numeric formatting collisions (4 checkpoint, 1 compare) logged under the contextual rule; 0 hits.
- Run time: 8 m 45 s single core (the HS reference optimization and the 12-point texture sweep over eight keys dominate).

## 7. Embeds

=====BEGIN-EMBED name=staging_memo_G_MSCS1_v2.md md5=3f30262eaec461fb5fd3202835f7de37 bytes=34837 encoding=raw=====
# STAGING MEMO — Gate G-MSCS1 (Multi-Species Channel Speed: the Q3(1) carrier-identity residue and the emergent species-universality obligation) — v2

**Date:** September 19, 2026 (v2; draft v1 September 17, md5 53300f21, superseded — see Amendment A-1). **Base:** `SQT_Master_Ledger_v4_82_CANONICAL.md` (md5 `d095a7003bb0d4c177e7451e1d14c4c6`, 1,552,643 B). **Status: LOCK HELD — awaiting the author's word on Amendment A-1 (§A).** **Lineage:** §2.91.I Q3 ledger item (1) → ANNEX-CDEF-1 (V4.71) → G-TSH4 (§2.91.L) → G-POLY1 (§2.91.M) → G-CI1 (§2.91.N) → G-S2C1 / G-S2C1-W (§2.91.O) → "the multi-species channel-speed question, Q6 of the G-S2C1 LSF" (named successor, V4.80–V4.81).

## A. Amendment A-1 — pre-lock catches (chat-self-caught at instrument design, before any computation; the G-TSH2 S-1 / G-TSH4 S-1 class)

The v1 draft was reviewed against the definitions it would have locked. Four defects, all repaired below; none survives into v2:

- **A-1.1 (vacuity).** v1 §2.4 inherited E-P2-1(a) as the grain-scale *definition* of the S2 species ("the polarization-averaged shear cone"). Under that definition the EM species (helicity ±1 about k̂, both signs equally) and the S2 species are the same average of the same branches — r_agg(t) ≡ 0 for every texture, by construction. The texture sweep would have measured a tautology. Repaired: the S2 species is the E₂ (crystal-axis quadrupole) content of the *transverse-projected* strain, evaluated per grain about the grain's own axis and ODF-averaged at the grain scale (§2.3–2.4); E-P2-1(a) is carried as the kinematic statement it is (no plane wave carries pure helicity ±2), not as a species definition.
- **A-1.2 (wrong isotropic limit).** v1 §2.3 defined the lattice-scale S2 weight as the m = ±2 content of the *full* traceless strain about n̂. That descriptor has support on the quasi-longitudinal branch even in an isotropic solid (k̂k̂ − I/3 carries m = ±2 about any axis oblique to k̂), so it would have reported a "species split" between a transverse EM descriptor and a partly-longitudinal S2 descriptor in a medium with no anisotropy at all — a descriptor artifact, not physics. Repaired: transverse projection first (§2.3).
- **A-1.3 (falsifiers that could not fire).** v1's F-MS-1 (zero-texture aggregate split) and F-MS-2 (gyrotropic split) were symmetry-forced nulls: in the untextured aggregate the species weights average to a mode-independent constant (2/5, an SO(3) identity) and the coherent shear wave has one dispersion for both polarizations; gyrotropy is a first-order spatial-dispersion effect (Portigal–Burstein 1968), absent at Christoffel/Born order and already excluded at the lattice scale by G-S2C1's even-basis result (H-S2C-10). Neither was a live kill. Repaired: F-MS-1 → control F-CTRL-SO3; F-MS-2 → REGISTERED, NOT EXECUTED (§5); and the texture onset is now stated correctly — the species split is **second order** in texture for any descriptor pair that agrees on the isotropic medium (both the weight difference and the speed difference are O(t), their covariance O(t²)); v1's "S_t ≠ 0" hypothesis is withdrawn and replaced by the first-order protection statement and its quadratic coefficient κ₂ (§2.5, §6).
- **A-1.4 (positivity range).** v1's fiber-ODF range t ∈ [−½, 1] was wrong; 1 + t·P₂(cos θ) ≥ 0 on the sphere requires t ∈ [−1, 2]. Corrected (§2.5).

**Consequence: the gate is re-classed from a kill gate to a delivery gate** (the G-CC-ε1 BOUND-DELIVERED / G-POLY1 P-2 class). Under E-MS-1(a) the single-species carrier claim is an identity on the isotropic aggregate; this gate cannot kill it there and does not pretend to. It quantifies the identity's corrections (single-crystal admixture structure, second-order texture split) and delivers the texture constraint curve. The kill surface for the claim lies outside this gate and is named in §5. The author's authorization is required for this re-scope before lock.

## 0. What the ledger has already settled (this gate does not re-litigate any of it)

- **ANNEX-CDEF-1:** c is *defined* as the transverse-channel speed; the only physics is the dimensionless ratios c_T/c_EM and c_T/c_S2. No SI speed appears anywhere in this gate.
- **G-TSH4 (ANISO-3D):** every surviving configuration propagates two-to-three distinct transverse speeds (hex splits to ~34%, cubic to ~41%); the quasi-transverse eigenvectors are not exactly ⊥ k off symmetry directions.
- **G-POLY1:** in the untextured SO(3) aggregate the polarization degeneracy is exact at leading order in d/λ; the finite-(d/λ) residual is the banked s₁·√(d/L) law; W_∪ SUSPENDED.
- **G-CI1:** K = ∅ — the instantiated substrate carries **no gapless internal helicity-±2 branch**; strong carrier identity CI-S FALSIFIED-STRUCTURAL; the operative branch is **CI-W/EM-IN** (EM rides the transverse channel; window W^EM banked).
- **G-S2C1:** the "S2 channel" is the **E₂/quadrupole content of the transverse phonon** — at the lattice scale identified at o₂ = 0.99999999 with the transverse speed c_T and DISPERSIVE O(k²); at the grain scale, by election E-P2-1(a), no plane wave's strain is pure helicity ±2, so the aggregate S2 channel was taken as the polarization-averaged shear cone. G-S2C1-W: the dispersion constraint curves are INERT; **no channel-speed-equality claim was made.**

**Consequence that frames this gate.** The framework's two radiative species are not two fields. They are two *descriptors* of one transverse phonon: the helicity-±1 displacement content (EM, CI-W/EM-IN) and the E₂ strain content (S2). The emergent species-universality obligation of the literature (Chadha–Nielsen 1983; Collins et al. 2004; Anber–Donoghue 2011; Bednik–Pujolàs–Sibiryakov 2013) is posed for *distinct fields* whose limiting speeds must be equalized by a symmetry, an attractor, or a common origin. Here the common origin is total — one field — so the obligation attaches in a sharper form: **species universality is an identity wherever the two descriptors weight the medium's modes identically; it fails only where they do not, and the size of that failure is computable.** In a single crystal the E₂ descriptor is direction-selective and the EM descriptor is not, so a descriptor split of order the anisotropy exists there. In the untextured aggregate the orientation average makes the E₂ weight a mode-independent constant and the split vanishes identically. Texture reintroduces a split — at second order. Those statements, and the coefficients that make them quantitative, are the content of this gate.

## 1. Object

**Question (one sentence):** in the instantiated substrate — the four G-TSH4-lineage configurations (hex:step, hex:gem8, cubic:step, cubic:gem8) and their SO(3) aggregate — how far are the leading-order limiting speeds of the EM species and the S2 species from equal: exactly equal (identity) in the untextured aggregate; by how much, and with what sign, in each single crystal; and with what texture dependence in a textured aggregate?

**Verdict classes (pre-registered; one is assigned by the machine, last):**
- **IDENTITY-DELIVERED** — all Phase-0 controls pass (including the SO(3) identity at t = 0 and the first-order protection S_t = 0); r_xtal per configuration, the admixture maps λ_L, and the quadratic texture coefficients κ₂ are delivered two-leg. The species-universality obligation for the in-channel pair is **DISCHARGED-AS-IDENTITY on the untextured aggregate, with its corrections quantified** — R2, conditional on the imports in §7. Expected class.
- **PROTECTION-BREACH** — the first-order protection fails (F-MS-3 fires two-leg): a first-order texture split contradicts the degenerate-perturbation structure; treated as an S9 item first, and if it survives S9 as a structural finding that the identity is not robust in the t → 0 limit. The R2 reading is then NOT delivered.
- **INDETERMINATE** — a Phase-0 control fails; no verdict.
- **DECLARATIVE (E-MS-1(b))** — see §5.

## 2. Analytical frame (definitions the instrument encodes; nothing else is computed)

**2.1 The field and its inputs.** Leading-order lattice-scale propagation is the Christoffel problem on the banked tensors C/ρ of `poly_vrh_results.json` (md5 `200e7a8b`, 2,767 B; hex: 6 constants, cubic: 3), sampled over the k̂-sphere with the pinned quadrature (lock record). The aggregate at leading order is the G-POLY1 SO(3) average (VRH and Hashin–Shtrikman bounds), generalized to a textured ODF (§2.5); the second-order piece at t = 0 is the G-S2C1 P2 Born machinery on the banked Ξ/Φ_TM kernels, run polarization-resolved as a control. Substrate units throughout; every reported quantity is a ratio.

**2.2 Descriptor EM (CI-W/EM-IN).** For an eigenmode (k̂, e), e_⊥ = e − (k̂·e) k̂ and λ_L = (k̂·e)². Weight w_EM = |e_⊥|² = 1 − λ_L (helicity ±1 about k̂, both circular polarizations weighted equally). Support: every branch, ≈ 1 on the quasi-transverse pair, ≈ λ_L on the quasi-longitudinal branch.

**2.3 Descriptor S2-E₂ (primary).** The transverse-projected strain S_⊥ = sym(k̂ ⊗ e_⊥); its traceless part is S_⊥ itself. About a fixed crystal axis n̂, decompose S_⊥ under SO(2)_n̂ into m = 0, ±1, ±2 components; w_S2 = |P^{(±2)}_{n̂} S_⊥|² / |S_⊥|² · w_EM. For hex, n̂ = the c-axis and P^{(±2)} is the E₂g doublet (x²−y², xy) — the 3D continuation of the p6m E₂ channel of G-S2C1. For cubic there is no distinguished axis; n̂ is elected (E-MS-2c: ⟨001⟩ primary, ⟨111⟩ reported). Properties: on an isotropic medium the descriptor is supported on the transverse branches only (the projection removes the k̂k̂ − I/3 artifact of v1); it is *direction-selective by construction* — zero for propagation along n̂ with any polarization, full for basal propagation with in-plane polarization — and that selectivity is the mechanism under test, not a defect.

**2.3′ Descriptor S2-h (second arm, reported).** The helicity-±1 fraction of the full traceless strain about k̂: w_S2h = |S̃_{±1}|²/|S̃|² with S̃ the traceless part of sym(k̂ ⊗ e). Algebraically w_S2h = (1 − λ_L)/(1 + λ_L/3), so w_S2h − w_EM = O(λ_L): this descriptor differs from EM *only through the longitudinal admixture* and gives the admixture-controlled reading of the same question (§2.6).

**2.4 Grain scale.** At the grain scale each grain carries its own n̂; the S2-E₂ weight of an aggregate mode is the ODF average of the per-grain weight, ⟨w_S2⟩_ODF. For the untextured ODF this average is the mode-independent constant 2/5 (the m = ±2 share of a random l = 2 tensor under SO(3)) — the identity at t = 0 is therefore an SO(3) theorem, verified as control F-CTRL-SO3, never reported as a result. E-P2-1(a)'s kinematic point (no plane wave carries pure helicity ±2) rides with this definition as disclosed at V4.80; nothing here is a helicity-2 field.

**2.5 The species speeds.**
- Single crystal, per configuration: ⟨v⟩_X = Σ_branches ∫dΩ w_X(k̂, e) v(k̂, e) / Σ ∫dΩ w_X for X ∈ {EM, S2-E₂, S2-h}; **r_xtal = ⟨v⟩_S2/⟨v⟩_EM − 1**, reported for both S2 arms. A measurement — expected non-zero, of order the anisotropy for S2-E₂ and of order λ_L × anisotropy for S2-h, with a definite sign per configuration.
- Aggregate, t = 0: both species see the one isotropic v_T (VRH; HS bounds) — an identity, pinned, not reported as a result. Polarization-resolved second-order Born at t = 0: the helicity +1, −1 and average self-energies D(0), D2 must coincide (F-CTRL-POL) and reproduce the banked a₂^agg quartet (PIN-A2AGG).
- Aggregate, textured: the one-parameter fiber ODF w(θ) = 1 + t·P₂(cos θ), θ the angle between a grain's n̂ and the fiber axis, **t ∈ [−1, 2]** (positivity on the sphere: t ≤ 2 from P₂ = −½, t ≥ −1 from P₂ = 1). The textured aggregate is transversely isotropic; at each t the Voigt, Reuss and HS tensors are formed from the ODF-weighted grain average, the Christoffel problem solved over the k̂-sphere, and ⟨v⟩_EM, ⟨v⟩_S2 formed with the ODF-averaged per-grain S2 weight. **r_agg(t) = ⟨v⟩_S2(t)/⟨v⟩_EM(t) − 1** on the pinned t-grid; the fit r_agg(t) = S_t·t + κ₂·t² + κ₃·t³ over |t| ≤ 0.25 with step-halving convergence. **First-order protection (algebraic, to be confirmed by the machine): S_t = 0** — at t = 0 the speeds are degenerate across polarizations and the ODF-averaged weight is mode-independent; both perturb at O(t), so their covariance, which is what r_agg measures, is O(t²). **κ₂ is the gate's quantitative product** — the constraint curve r_agg(t) ≈ κ₂ t² on the texture import. Dimensionless; nothing evaluated against any bound.

**2.6 The Maxwell-admissibility descriptor.** λ_L(k̂, branch) = (k̂·e)² on the two quasi-transverse branches — the single-crystal analogue of a non-zero ∇·E. Reported as sphere-mean and sphere-max per configuration with the branch of the maximum, and as a function of t in the textured aggregate (zero at t = 0 by isotropy; O(t²) since the polarization tilt is O(t)). No threshold is set against any observation (M.CW); the number is the differentiator an isotropic continuum cannot exhibit (§3). The S2-h arm makes the connection exact: r_xtal(S2-h) = −(1/3)·Cov_EM(λ_L, v)/⟨v⟩_EM + O(λ_L²) — the admixture-controlled split is minus one-third the covariance of admixture and speed over the EM-weighted mode ensemble; F-CTRL-ADMIX checks it.

## 3. The Danielewski obligation (inherited from V4.71; discharged here as far as a gate can discharge it)

**3.1 What the obligation is.** The CI-W/EM-IN reading — "the transverse wave *is* the electromagnetic wave" — is Danielewski's identification (Z. Naturforsch. 62a, 564 (2007); Entropy 22(12), 1424 (2020); Symmetry 15(9), 1672 (2023)), itself the MacCullagh (1839) → FitzGerald (1880) → Kelvin (1890) → Kleinert (1987) lane. Two halves: (a) *attribution* — the framework does not own the identification; (b) *differentiation* — what, if anything, the framework adds that the lane does not already contain.

**3.2 Differentiation table (LSF-δ read of September 19, 2026; sources and transcription ceilings in §12).**

| Item | D-2007 | D-2020 | D-2023 | SQT (V4.82) |
|---|---|---|---|---|
| Medium class | "ideal cubic fcc crystal formed by Planck particles" | "classical balance equations for isotropic Cauchy-elastic material"; "we consider FCC structure, where the Poisson number ν = 0.25" | "The macro properties of crystalline æther are approximated by the Cauchy model of the ideal elastic crystal continuum"; fcc, ν = 0.25 (Table 1) | p6m/Császár GP-instantiated droplet crystal; two stacking branches (hcp AB / fcc), kernel-labelled; six-constant hex and three-constant cubic tensors measured (G-TSH4); Cauchy relations NOT assumed |
| EM identification | "The transverse wave is the electromagnetic wave and its velocity equals the velocity of light." | "the invariant transverse wave velocity: c = √(0.4Y/ρ_P) = const."; Table 1: transverse velocity ≡ light velocity | "The wave propagation depends on the transverse wave velocity c"; Table 1: transverse wave velocity ≡ light velocity | CI-W/EM-IN, *adopted with attribution*; c defined as the transverse-channel speed (ANNEX-CDEF-1); the EM-side window W^EM banked (G-CI1) |
| Longitudinal sector | "The quasi-stationary collective movement of mass in the crystal is equivalent to the particle (body)" | compression wave with ∂²σ₀/∂t² = 3c²Δσ₀ vs twist ∂²φ̂/∂t² = c²Δφ̂ — i.e. c_L/c_T = √3 (ν = ¼, the Cauchy relation); "the Poisson type equation … defines the compression potential as a function of energy density" | "The quaternionic oscillator couples the transverse and longitudinal waves into the q-potential wave" | the longitudinal acoustic bridge RETIRED (G-SCALE1, §2.91.D/H); constrained-sector requirement (KC1–KC3, §2.91.B/E/F); c_L/c_T not a fixed number — measured per configuration (G-TSH4: c_L1/c_T ≈ 1.9–2.5, kernel-dependent) |
| Gravity mechanism | "The diffusing interstitial Planck particles create a gravity field." | Poisson equation from the compression potential; G = l_P³/(t_P² m_P) | "Tension induced by the compression and twisting of the continuum affects its energy density and generates the force of gravity, as density changes alters the wave speed and hence gravity could be described by an index of refraction." | Paper IIA Bjerknes / acoustic-metric thread (§2.91); K = ∅ (no internal helicity-2 branch); not this gate |
| Anisotropy / aggregate | isotropic (cubic crystal treated as isotropic continuum); no aggregate | "isotropic Cauchy-elastic material"; no anisotropy | "ideal elastic crystal continuum"; no anisotropy, dispersion, or species-speed discussion located | ANISO-3D single crystal (two-to-three transverse speeds); untextured VRH/HS aggregate; s₁ birefringence law; **this gate:** admixture maps λ_L, descriptor split r_xtal, first-order texture protection, κ₂ |
| Dimensionless outputs | none located | ν = 0.25; c_L/c_T = √3; c = √(0.4Y/ρ_P) | none beyond ν = 0.25 located | a₂ (lattice), a₂^agg quartet, s₁ quartet, W^EM, R_T (kernel-labelled); **this gate:** r_xtal, λ_L, S_t (= 0), κ₂ |

**3.3 A0 declaration (pre-registered; LSF-δ outcome).** No novelty is claimed for the EM-IN identification. Novelty is claimed only for the *constraint surface* — the ANISO-3D admixture field λ_L, the EM-side window, the a₂ dispersion coefficients, and the descriptor split with its first-order texture protection and quadratic coefficient — at the level LSF-δ supports: **novel-in-assembly** (§12 cluster 6). The first-order protection is an elementary consequence of degenerate-perturbation structure and is claimed only as applied to this pair of descriptors.

**3.4 What this section does not do.** It does not derive Maxwell's equations from the substrate, assign sources, or evaluate any bound. "Maxwell-admissible" means: two transverse polarizations per k̂ (G-TSH4 branch count) and transversality (§2.6) — necessary conditions, stated as such.

## 4. Execution leg

**Phase 0 — pins and controls (halt-on-fail).** X-1 byte-verified (`200e7a8b`). Controls: **F-CTRL-ISO** — an isotropic tensor gives r_xtal = 0 (both arms), λ_L = 0, r_agg(t) = 0 ∀t at machine precision (texture on an isotropic grain does nothing); **F-CTRL-SO3** — the ODF-averaged S2-E₂ weight at t = 0 equals 2/5 for every mode to the quadrature tolerance, and r_agg(0) = 0; **F-CTRL-TEX** — a synthetic strongly anisotropic hex tensor at t = 1 gives |r_agg| above τ_agg (the instrument can see a split); **F-CTRL-POL** — the polarization-resolved Born at t = 0 gives helicity +1, −1 and average self-energies equal within τ_agg; **PIN-A2AGG** — the re-implemented Born reproduces the banked a₂^agg quartet to ≤ 1×10⁻⁸ relative before any species-resolved use; **F-CTRL-ADMIX** — replacing every quasi-transverse eigenvector by its transverse projection sends r_xtal(S2-h) to zero within τ_agg (the S2-h split is admixture-sourced). Any control failure → INDETERMINATE.

**Phase 1 — lattice scale, leading order.** Christoffel on the four tensors over the k̂-sphere; per (k̂, branch): v, e, w_EM, w_S2-E₂, w_S2-h, λ_L. Outputs per configuration (hex under E-MS-2b arms (a) and (b); cubic under n̂ = ⟨001⟩ and ⟨111⟩): ⟨v⟩_EM, ⟨v⟩_S2 (both arms), r_xtal (both arms), the per-branch weight shares of each descriptor, ⟨λ_L⟩, max λ_L and its branch, Cov_EM(λ_L, v).

**Phase 2 — aggregate.** (i) t = 0 pins: VRH/HS v_T. (ii) t = 0 polarization-resolved Born on the banked kernels → D(0), D2 per helicity class (control + pin only). (iii) Texture sweep at leading order: r_agg(t) for both S2 arms on the pinned t-grid, VRH and HS at each t; the cubic fit; S_t and κ₂ with the step-halving check; λ_L(t) sphere-mean.

**Phase 3 — comparison, last (Eddington quarantine).** Verdict class from Phase 0/2 states; the pre-registered hypotheses (§6) compared in a separate artifact; no observational number anywhere in any phase.

**Instrument encoding.** Pinned quadrature (GL(cos θ) 64 × uniform φ 128, F-QUAD doubling ≤ 1×10⁻¹⁰, the G-POLY1 P2 precedent), the 12-point t-grid, and all tolerances in the lock record; every verdict-bearing quantity a float with a declared tolerance or a boolean/label; free text never compared; comparator v1.0 + schema v1.0 FROZEN BEFORE the chat leg emits (the D-Q-3 lesson); the T1 gate list travels in-band and the instruments halt without it — no `--no-t1-halt` path exists in this gate (§11).

**Tolerances (pre-registered).** τ_agg = 1×10⁻⁶ (absolute on r; relative on Born quantities); two-leg agreement ≤ 1×10⁻⁸ on Phase-1 means and r_xtal, ≤ 1×10⁻⁸ on the VRH/HS pins, ≤ 1×10⁻⁶ on r_agg(t) and S_t, ≤ 1×10⁻⁴ relative on κ₂ (a fitted second derivative).

## 5. Falsifiers, controls, and where the kill surface actually is

- **F-MS-3 (first-order protection):** |S_t| > τ_agg on any configuration, either S2 arm, reproduced two-leg after S9. → PROTECTION-BREACH.
- **F-MS-2 (gyrotropic split) — REGISTERED, NOT EXECUTED.** Gyrotropy is a first-order spatial-dispersion effect, absent at the Christoffel/Born order of this gate and excluded at the lattice scale by G-S2C1's even-basis result (k³ refuted, H-S2C-10). A successor carrying odd spatial dispersion could test it. F-CTRL-POL is the order-consistent stand-in (a control, not a test).
- **F-MS-1 (zero-texture split) — RETIRED as a falsifier; now control F-CTRL-SO3.** An SO(3) identity cannot fire.
- **Declarative kill: election E-MS-1(b)** (the Q3(2) texture/envelope route as a second carrier). Two fields with independent stiffnesses cannot share a speed by identity; the single-species claim is withdrawn by declaration, and the gate re-scopes to the literature-form obligation (a stiffness-ratio classification: DERIVED-RATIO / KERNEL-CLASS-PINNED / KNOB).
- **Not falsifiers:** r_xtal ≠ 0 (the expected single-crystal descriptor split — reported; its sign becomes κ₂'s provenance); κ₂ ≠ 0 (the expected second-order texture split — the delivered constraint curve).
- **Where the kill surface for the single-species claim lies, stated plainly:** (i) E-MS-1(b); (ii) the value of the texture import (the untextured ODF is an M.ONT import, G-POLY1 E3 — a textured vacuum implies a species split κ₂t², which this gate quantifies but cannot evaluate); (iii) a sealed-anchor comparison of κ₂t² against the 2017 multi-messenger tensor-speed bound — E-MS-6(b), declined for this gate. None of these is inside G-MSCS1.

## 6. Hypotheses (M-naive expectations, registered pre-data — NOT verdicts)

- H-MS-1: r_xtal(S2-E₂) < 0 on both hex configurations (the E₂g descriptor weights basal in-plane shear, the slower branch class on the banked tensors), |r_xtal| of order 10⁻²–10⁻¹; cubic r_xtal smaller and n̂-dependent.
- H-MS-2: r_xtal(S2-h) of order 10⁻³, sign given by −Cov_EM(λ_L, v); |r_xtal(S2-h)| ≪ |r_xtal(S2-E₂)| on every configuration.
- H-MS-3: S_t = 0 within τ_agg on all four (first-order protection); κ₂(S2-E₂) ≠ 0 with sign matching r_xtal(S2-E₂); κ₂(S2-h) smaller by roughly the admixture factor.
- H-MS-4: ⟨λ_L⟩ of order 10⁻² on the hex configurations, max λ_L on the oblique qSV branch; zero at t = 0 in the aggregate; O(t²) in t.
- H-MS-5: hex and cubic κ₂(S2-E₂) share a sign (not forced; a structural question the machine answers).
- Expected class: **IDENTITY-DELIVERED.**

## 7. Pinned inputs and imports (named; none exercised beyond what is stated)

- X-1 `poly_vrh_results.json` `200e7a8b775577564369c6924d38a84c` (2,767 B) — the four tensors at full precision (repo: `gpoly1_gate/`, `gci1_gate/embeds/`, `gs2c1_gate/p2_ccleg/`, all identical).
- X-2 the G-S2C1 P2 aggregate Born machinery — reference implementation `gs2c1_gate/p2_ccleg/g_s2c1_p2_cc_instrument.py` `c1e59155…` (CC leg, commit debce15) and the chat-side P2 instruments (0328b570 / 6da62fca / 0e8cc05e per §2.91.O); re-implemented here, contained by PIN-A2AGG; used at t = 0 only (E-MS-3(a) as scoped in §8).
- Imports inherited, unexercised: the transverse scale (T4; no SI); the M.ONT polycrystal ontology; the untextured orientation distribution (G-POLY1 E3) — *this gate's texture family is a sensitivity sweep on that import, not a claim about its value*; E-P2-1(a) as a kinematic statement; K = ∅; the V4.70 KNOB caveat (kernel-labelled throughout).
- Retro Q-item honoured: the banked hex tensors are 6-constant tetragonal-form objects (C66 independent of (C11−C12)/2) — disposition by E-MS-2b.

## 8. Elections (author, September 19, 2026 — T3-immutable on lock)

- **E-MS-1 (scope of "species"): (a)** — the two descriptors of the one transverse field, on the banked identifications CI-W/EM-IN (EM) and the E₂ content of the transverse phonon (S2), with S2-E₂ primary and S2-h as a reported second arm (A-1.1/A-1.2). (b) not elected.
- **E-MS-2 (configurations): (a)** all four. **E-MS-2b (hex form): (a) primary** — consume as banked, tetragonal-form (the G-S2C1 precedent); **(b) second arm** — hexagonal-symmetrized C66 = (C11−C12)/2, reported. **E-MS-2c (cubic n̂):** ⟨001⟩ primary, ⟨111⟩ reported.
- **E-MS-3 (aggregate order): (a)** — VRH/HS leading order; polarization-resolved second-order Born **at t = 0 only** (control F-CTRL-POL + pin PIN-A2AGG); the texture sweep at leading order. *Scope clarification (chat, pre-lock, narrowing only): the textured (t ≠ 0) second-order Born requires the anisotropic-reference-medium Green function (the Acoustics 2020 SOA extension) and is REGISTERED as a successor arm, not executed here.*
- **E-MS-4 (Danielewski): (a)** — the verbatim table (§3.2) + the λ_L computation.
- **E-MS-5 (texture family): (a)** — the fiber ODF 1 + t·P₂, t ∈ [−1, 2] (the l = 2 Legendre term alone; the l = 4 coefficient is zero in this family, so it is one texture, not the general weak texture — a biaxial / l = 4 family is a registered successor arm).
- **E-MS-6 (observational contact): (a)** — NONE in this gate; the 2017 multi-messenger dimensionless bound stays literature context; any comparison is a separate pre-registered mini-gate with sealed anchors.

## 9. Registers and non-claims

- Every number R1-machine two-leg. The IDENTITY-DELIVERED reading R2, conditional on E-MS-1(a), the untextured import, K = ∅, and the kernel election. The polycrystal postulate remains R3.
- No observable, no bridge, no SI value, no d, no f, no μ_n, no channel-speed number against any bound; no claim that Maxwell's equations are derived; no claim about a helicity-±2 field (the substrate has none, G-CI1); no reinstatement of W_∪; the V4.63/V4.71 structural pass stays a structural statement; no kill of the single-species claim is possible inside this gate and none is claimed.

## 10. Housekeeping (V4.83 — carried by this gate's fold, not by this memo)

The V4.83 fold must carry one **additive bracket** on §2.91.P and on the V4.82 fold-in record: PR #23 merged (author confirmation September 17, 2026); the chat-side G-QUANTA estate lives at `gquanta_gate/estate/` (fold script `ff6fa734`, authorization `7cc57e8c`, closure memo `ccd53cb9`, execution report `4ecb40e3`, manifest); CC's independent reverse-splice audit (`gquanta_gate/verify_v482_reverse_splice.py`, `CC_V482_FOLD_VERIFICATION.md`) reconstructed V4.81 `b4e55aae` from the delivered V4.82 by `ast`-parsed edit literals **without holding V4.81** — a third-party determinism confirmation of the fold; the §2.91.P sentence "the chat-side estate is not yet in the repo" is superseded. Append-only; no re-fold.

## 11. T1 list — retiring D-T1 (a lock prerequisite, executed September 19, 2026)

1. **Surfaced.** The author supplied a base list on September 19, 2026 citing it as the G-2a-L1 list `04438b74` (13 pattern lines, 117 B per the V4.79 record). The supplied text has 11 pattern lines and no line-ending / comment / ordering variant hashes to `04438b74` (143 B with its header, 55 B patterns-only). **H-MS-0 (authorizing-directive T1-hash discrepancy; the G-BKZ32 H-1 class):** the supplied list is an author reconstruction, not the recovered file; pinned under its own hash, with authority from the author's supply. The `04438b74` list remains cited-but-unrecovered; its recovery (the G-2a-L1 dispatch `0c5588ee`, embed) would allow a diff, not a replacement.
2. **Pinned centrally.** `tools/t1/T1_base_author_20260919.txt` md5 `05302210cc4ceb70553acbe8379e9fc3` (143 B, 11 patterns) + `tools/t1/MANIFEST.md5`; every later gate composes from this stratum.
3. **Gate list composed.** `T1_forbidden_G_MSCS1.txt` md5 `fef2827100d3f85e0a6341b44f0c00bf` (1,433 B, 36 pattern lines) = the base stratum verbatim + the gate stratum (the SI speed of light in scientific form, the 2017 tensor-speed bound digit strings in five renderings, SI speed units, event/collaboration/instrument identifiers, the observational-search identifiers, the anisotropic-dispersion coefficient names of the observational dialect). Scanner `t1_scan.py` md5 `6b86290090a8c84f1b1a0a99ec0bf697` frozen with it: pattern lines only, case-sensitive substring, bare numeric patterns under the contextual numeric rule (D-W-7 lineage), hits by pattern index only.
4. **Travels in-band.** The gate list is an embed in every dispatch (P-4); the instruments halt without it. **D-T1 is RETIRED at lock** — it cannot be elected at G-MSCS1.

## 12. LSF-δ (September 19, 2026; six clusters; transcription ceilings stated)

1. **Emergent multi-species limiting speeds.** Anber–Donoghue, PRD 83, 105027 (2011): "different particles have different limiting speeds"; "if the different particles are interacting, then the interactions yield a scale dependence to this limiting velocity, and the velocities approach each other at low energy"; "it is not clear if this mechanism can be effective enough to satisfy the experimental constraints" (the author's own summary page, quoted; the journal abstract was not retrievable — 403). Bednik–Pujolàs–Sibiryakov, JHEP 11 (2013) 064: "deviations of these observables from the relativistic form at low energies are found to be power-law suppressed by the ratio of the infrared and ultraviolet scales"; "in a certain subclass of models the velocities of the light bound states stay close to the emergent 'speed of light' even at high energies." Chadha–Nielsen NPB 217, 125 (1983); Collins et al. PRL 93, 191301 (2004): corpus-carried (V4.71). **Reading:** all pose the obligation for distinct fields; the framework's species share one field, so the obligation attaches in the identity form of §0. No collision.
2. **Polycrystal shear propagation, texture, gyrotropy.** Stanke–Kino JASA 75, 665 (1984); Weaver JMPS 38, 55 (1990): corpus-carried. Textured extension located: *Attenuation and Phase Velocity of Elastic Wave in Textured Polycrystals with Ellipsoidal Grains of Arbitrary Crystal Symmetry*, Acoustics 2(1), 5 (2020) — "extends the second-order attenuation (SOA) model … to textured polycrystals"; ODF via generalized spherical harmonics (Bunge) or Gaussian form; quasi-static phase velocity at arbitrary direction derived; modes qL / qT-fast / qT-slow; not SH/SV-resolved; the anisotropic-reference Green function is its distinguishing step — **this is the machinery the t ≠ 0 second-order successor arm would adopt (E-MS-3 scope note)**. Gyrotropy: Portigal–Burstein, Phys. Rev. 170, 673 (1968), *Acoustical Activity and Other First-Order Spatial Dispersion Effects in Crystals* — first-order spatial dispersion; grounds the F-MS-2 reclassification. Man–Huang, J. Elasticity (2012), representation theorem: material tensors of weakly textured polycrystals "expressed as a linear combination of an orthonormal set of irreducible basis tensors, with the components given explicitly in terms of texture coefficients" — the effective tensor is affine in the texture coefficients at first order; grounds the analyticity premise of §2.5. No published descriptor-resolved species split in a textured aggregate located.
3. **The rotational-ether Maxwell map.** MacCullagh 1839 (stored energy ∝ |curl|² only; the formal Maxwell equivalent), FitzGerald 1880, Kelvin 1890, Larmor: corpus-carried (V4.63). Danielewski 2007 / 2020 / 2023 read for §3.2; transcription ceilings: D-2007 quoted from the author's CNLS talk summary of the same title and year (the journal text itself not retrieved); D-2020 from the journal PDF (inspirehep mirror); D-2023 from the Qeios preprint v2 PDF of the Symmetry paper (journal version not retrieved). Adjacent, not a collision: Sinclair, Zenodo record 20365995 (May 24, 2026), *How Close Did MacCullagh and Hamilton Come to Einstein's Field Equations?* — MacCullagh's medium promoted to curved spacetime via a Cosserat/quaternion route; abstract carries no species-speed, anisotropy, or texture content (full text not read).
4. **Elastic-solid spin-2 content.** Gu–Wen (helicity-±2 qubit model, k³), the Weinberg–Witten evasion by non-covariant substrates: corpus-carried (G-S2C1). Nothing new located bearing on descriptor identity.
5. **Fiber-texture conventions.** The axisymmetric ODF's l = 2 Legendre term 1 + t·P₂ is the first non-trivial term of the standard (Roe/Bunge) expansion; positivity gives t ∈ [−1, 2]; elasticity depends on the ODF through l ≤ 4, so this family (l = 4 coefficient zero) is one weak texture, not the general one (Man–Huang). Recorded in E-MS-5(a).
6. **Collision check.** No located prior claim computes an EM/spin-2 *descriptor* split as a function of vacuum texture in an elastic-vacuum model; Danielewski's lane is isotropic with a single c; the world-crystal lane (Kleinert; corpus-carried V4.63) does not treat wave-species speeds. **Verdict: novel-in-assembly; A0 not triggered.** Honest ceiling: the first-order protection is elementary; the novelty is in the assembly (two descriptors of one phonon, the ODF-averaged E₂ weight, the admixture covariance form), not in any ingredient.

## 13. Pre-lock state (all executed September 19, 2026 unless marked)

1. LSF-δ — DONE (§12); §3.2 filled.
2. T1 base list — DONE (§11; H-MS-0 recorded).
3. Comparator v1.0 + schema v1.0 — WRITTEN and self-tested; FREEZE on the author's lock word (their md5s enter the lock record at that moment).
4. Hex-tensor disposition — ELECTED (E-MS-2b).
5. **Author word "Lock" on v2 as amended by A-1 — PENDING.**
=====END-EMBED name=staging_memo_G_MSCS1_v2.md=====

=====BEGIN-EMBED name=G_MSCS1_LOCK_RECORD.md md5=3dbe953badb6c030ef1d449adbac2044 bytes=7289 encoding=raw=====
# LOCK RECORD — Gate G-MSCS1 (Multi-Species Channel Speed: the Q3(1) carrier-identity residue and the emergent species-universality obligation)

**LOCKED:** September 19, 2026 (chat leg). **Base:** `SQT_Master_Ledger_v4_82_CANONICAL.md` md5 `d095a7003bb0d4c177e7451e1d14c4c6` (1,552,643 B).
**Author authorization (verbatim, September 19, 2026):** "I explicitly AUTHORIZE Amendment A-1 and the lock of `staging_memo_G_MSCS1_v2.md` (`3f30262eaec461fb5fd3202835f7de37`)." Supersedes the draft lock record (8be7cb63, LOCK HELD) — every hash below is now final.

## 1. Artifact of record

| Artifact | md5 | Size |
|---|---|---|
| `staging_memo_G_MSCS1_v2.md` | `3f30262eaec461fb5fd3202835f7de37` | 34,837 B |

Lineage: v1 `staging_memo_G_MSCS1_draft.md` `53300f21cbe233a640a49e76685cdf57` (21,025 B), superseded by Amendment A-1 (memo §A). T1 scan of v2 under the gate list: CLEAN.

## 2. Elections (author, September 19, 2026 — T3-immutable)

E-MS-1 (a) · E-MS-2 (a) · E-MS-2b (a) primary + (b) second arm · E-MS-2c ⟨001⟩ primary, ⟨111⟩ reported · E-MS-3 (a), the second-order Born at t = 0 only (narrowing clarification, memo §8) · E-MS-4 (a) · E-MS-5 (a) · E-MS-6 (a). Amendment A-1 (A-1.1–A-1.4; re-class to a delivery gate) AUTHORIZED.

## 3. Frozen pre-emission artifacts

| Artifact | md5 | Size | State |
|---|---|---|---|
| `g_mscs1_schema_v1_0.json` | `76a42db3fd6ad82e485752bc2ddb24d5` | 3,906 B | FROZEN — carries every lock constant and tolerance (memo_lock_md5 = v2) |
| `g_mscs1_compare_v1_0.py` | `22432b292ae0a9d5c91a6cb7aa67502f` | 18,541 B | FROZEN — 17/17 adversarial suites; no gate numbers in the file |
| `tools/t1/T1_base_author_20260919.txt` | `05302210cc4ceb70553acbe8379e9fc3` | 143 B | base stratum (11 patterns; H-MS-0) |
| `tools/t1/T1_forbidden_G_MSCS1.txt` | `fef2827100d3f85e0a6341b44f0c00bf` | 1,433 B | gate list (36 patterns) |
| `tools/t1/t1_scan.py` | `6b86290090a8c84f1b1a0a99ec0bf697` | 1,967 B | contextual numeric rule |

Both legs' checkpoints must carry `memo_md5` = v2, `T1.list_md5` = fef28271, `T1.state` = CLEAN; LIST_ABSENT is rejected by the comparator (D-T1 RETIRED).

## 4. Honesty items carried into execution

- **H-MS-0** — authorizing-directive T1-hash discrepancy (G-BKZ32 H-1 class): the supplied base list hashes to no variant of `04438b74` (11 vs 13 patterns; 143/55 B vs 117 B); pinned under its own hash with authority from the author's supply.
- **H-MS-1** — the v1 draft's kill set was symmetry-forced; caught at instrument design, pre-lock; Amendment A-1 authorized.

## 5. Addendum A-2 — operationalizations (chat, pre-execution; each locked here before the computation it governs)

- **A-2.1 Pin sources (banked, md5-verified at every open).** X-3 `gs2c1_gate/p2_ccleg/cc_p2_phase1.json` `aaae206733b0f0a378a5c6b600274d3f` (11,454 B): the full-precision a₂^agg = D2 quartet, D(0), I₀, I₂, V_T, V_L of the G-S2C1 P2 CC leg — the PIN-A2AGG reference (the ledger quotes the quartet to 7 digits; the pin is at 1×10⁻⁸ and needs the banked full precision). X-4 `gpoly1_gate/poly1_phase1full_cc.json` `ec87e42f0f617b00c4985ba2aceac339` (8,140 B): the general Voigt/Reuss moduli (`*_gen`) and the banked I₀ (`int_Phi_TT/TL`) — the PIN-VRH0 and kernel-moment references. X-5 `gpoly1_gate/chatleg_phase0bfull.json` `df413a7cfa30e599b779af8fee5d07d1` (1,920 B): the cubic Hashin–Shtrikman bands of record (A-2.3).
- **A-2.2 Kernel construction (PIN-A2AGG).** Φ_TM(μ) as in Addendum P2 of G-S2C1 (2feff442): δc = c(g) − c̄ with c̄ the SO(3) Voigt mean; incident T projector ½(I − p̂p̂), scattered projectors I − ŝŝ (T) and ŝŝ (L); N_M = 1/(V_T²V_M²), V_T = √μ̄, V_L = √(λ̄ + 2μ̄); D2 = Σ_M N_M[(1 − 2r_M²)I₀/8 − 3I₂/8] (P2-A). This leg's own quadrature: ZYZ product grid (16, 10, 16) (exact at band-limit 8; CC's was (12, 8, 12)); μ-moments by 8-point Gauss–Legendre (exact for the degree-4 even kernels). Helicity resolution (F-CTRL-POL): incident projectors ê_±ê_±^† with ê_± = (x̂ ± iŷ)/√2 in place of ½(I − p̂p̂).
- **A-2.3 Hashin–Shtrikman at texture t.** Walpole-form bounds with an isotropic reference C₀ = 3K₀J + 2G₀K: C_HS = [⟨(C_g + C*)⁻¹⟩_ODF]⁻¹ − C*, C* = 3K*J + 2G*K, K* = 4G₀/3, G* = G₀(9K₀ + 8G₀)/(6(K₀ + 2G₀)); the reference pair optimized at t = 0 (upper: the minimal feasible majorant C₀ ⪰ C_g giving the smallest bound; lower: the maximal minorant giving the largest) and reused at every t (the bounds stay rigorous for any ODF; slightly less tight off t = 0). Cubic at t = 0 must reproduce the X-5 bands to ≤ 1×10⁻⁶ relative (PIN-HS0); hex bands are reported as computed (the banked hex G_HS confirmation checkpoint is not among the fetched pin sources — stated, not hidden). `vT_HS_lo/hi` = the bound speeds at t = 0; the "HS scheme" for r_agg_E2_HS = the mean tensor ½(C_HS⁺ + C_HS⁻) at each t. VRH primary: `r_agg_*_VRH` uses the Hill tensor ½(C_V + C_R) at each t.
- **A-2.4 Fit and halving.** r_agg(t) fitted on the memo basis {t, t², t³} over the nine grid points |t| ≤ 0.25 (κ₂ of record, S_t of record); `halving_dev_kappa2` = the relative change of κ₂ when the window halves to |t| ≤ 0.1 (seven points). A 4-term {t, t², t³, t⁴} fit is reported alongside as a check (extra key, not compared).
- **A-2.5 Quadrature and doubling.** Sphere grid GL(cos θ) 64 × uniform φ 128; `quadrature.doubling_residual` = max over the eight configuration keys of |r_xtal_E2(64×128) − r_xtal_E2(128×256)|. Hex branches labelled by eigenvector character (qSH ≡ e ∥ ẑ × k̂, exactly decoupled), cubic by admixture (qL) then speed (qT1 fast, qT2 slow). Aggregate descriptor weight per mode: w_EM · ⟨f_E₂(n̂)⟩_ODF with f_E₂ the m = ±2 fraction of the transverse-projected strain about n̂, ⟨·⟩_ODF over the n̂-sphere with weight 1 + t·P₂(n̂·ẑ) (GL 12 × 24, exact for the degree-6 integrand); f_E₂(n̂) = 1 − 2|S_⊥n̂|²/|S_⊥|² + ½(n̂·S_⊥·n̂)²/|S_⊥|².
- **A-2.6 F-CTRL-ISO tensor.** Isotropic K = 134.609, G = 70.881 (the hex:step Hill pair) run through the cubic path with C11 − C12 = 2C44. **F-CTRL-TEX tensor.** Synthetic hex C11 = 300, C12 = 100, C13 = 50, C33 = 200, C44 = 40, C66 = 100 at t = 1.

## 6. Pinned execution constants (memo §4; schema)

τ_agg = 1×10⁻⁶. Two-leg: Phase-1 means/r/λ ≤ 1×10⁻⁸; pins ≤ 1×10⁻⁸; Born (t = 0) ≤ 1×10⁻⁶ rel; r_agg(t), S_t ≤ 1×10⁻⁶; κ₂ ≤ 1×10⁻⁴ rel (floor 1×10⁻⁶). t-grid {−0.5, −0.25, −0.1, −0.05, −0.02, 0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0}. X-1 `200e7a8b775577564369c6924d38a84c` (2,767 B).

## 7. Execution order

1. Chat leg `g_mscs1_chatleg.py`: selftest → phase0 (halt on any control failure → INDETERMINATE) → phase1 → phase2 → checkpoint → compare (last, separate artifact).
2. P-4 single-file in-band dispatch (memo, this record, schema, comparator, T1 list + scanner, pin sources in the clear; chat instrument/checkpoint/compare base64-armored); delivered alone (P-4.c).
3. CC leg blind from scratch; pre-consultation checkpoint committed before the armor is opened; comparator both sides; S9 on any MISS.
4. Fold at V4.83, carrying the §10 housekeeping bracket.
=====END-EMBED name=G_MSCS1_LOCK_RECORD.md=====

=====BEGIN-EMBED name=g_mscs1_compare_v1_0.py md5=22432b292ae0a9d5c91a6cb7aa67502f bytes=18541 encoding=raw=====
#!/usr/bin/env python3
"""g_mscs1_compare_v1_0.py -- Gate G-MSCS1 two-leg comparator, v1.0 (CANDIDATE; freezes on the author's lock word).

Usage
  compare  --chat CK --cc CK [--chat-cmp CMP --cc-cmp CMP] [--schema g_mscs1_schema_v1_0.json] [--out OUT]
  selftest [--schema ...]

All lock constants and tolerances come from the schema file; this file carries no gate numbers.
Checks (every verdict-bearing quantity is a boolean, a label, or a float with a declared tolerance;
free text is NEVER compared):
  C-M-0  provenance: required keys; memo_md5/bytes == lock; ledger base; T1 list md5 == lock and state CLEAN;
         X-1 md5/bytes; instrument_md5 real 32-hex; no placeholders; INDEPENDENCE WITNESS (instrument md5s differ,
         checkpoints not byte-identical); elections by canonical choice code
  C1     controls: every passed flag True on both legs; control floats within control_abs
  C2     phase1: per config key -- v_* within phase1_v_rel; r_xtal_* within phase1_r_abs; lambda_* within
         phase1_lambda_abs; cov within phase1_cov_abs; shares key-for-key within phase1_share_abs; branch label exact
  C3     phase2: pins within pins_rel; r_agg arrays elementwise within r_agg_abs; S_t within S_t_abs;
         kappa2 within max(kappa2_rel*|x|, kappa2_abs_floor); halving_dev_kappa2 <= kappa2_rel on each leg;
         lambda_mean_t elementwise within phase1_lambda_abs; born_t0 per base config within born_rel
  C4     falsifier states + verdict_class exact and in domain; quadrature n_theta/n_phi identical; t_grid == schema
  C5     compare-step identity (when both compare files supplied): rows id+concordant identical; verdict_class identical
Any MISS -> S9 counter-cross-check. Representational-vs-definitional classification is a human step after this report.
"""
import argparse, hashlib, json, os, re, sys, copy, math

HEX32 = re.compile(r'^[0-9a-f]{32}$')
PLACEHOLDER = re.compile(r'<[a-z_ ]+>|TBD|PLACEHOLDER|xxxx')
SCHEMA_DEFAULT = 'g_mscs1_schema_v1_0.json'


def md5f(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()


def getpath(d, dotted):
    cur = d
    for k in dotted.split('.'):
        if not isinstance(cur, dict) or k not in cur:
            return None, False
        cur = cur[k]
    return cur, True


def choice_code(s):
    m = re.match(r'\s*\(([^)]+)\)', str(s))
    return m.group(1).strip() if m else None


def close_abs(a, b, tol):
    return isinstance(a, (int, float)) and isinstance(b, (int, float)) and math.isfinite(a) and math.isfinite(b) and abs(a - b) <= tol


def close_rel(a, b, tol, floor=0.0):
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))) or not (math.isfinite(a) and math.isfinite(b)):
        return False
    return abs(a - b) <= max(tol * max(abs(a), abs(b)), floor)


def run_checks(chat, cc, S, chat_cmp=None, cc_cmp=None, chat_bytes=None, cc_bytes=None):
    R = []
    T = S['tolerances']

    def rec(check, item, ok, a=None, b=None):
        R.append({'check': check, 'item': item, 'result': 'PASS' if ok else 'MISS', 'chat': a, 'cc': b})

    # ---- C-M-0 provenance
    for leg, ck in (('chat', chat), ('cc', cc)):
        for key in S['required_keys']:
            _, present = getpath(ck, key); rec('C-M-0', f'{leg}: required key {key}', present)
        rec('C-M-0', f'{leg}: memo_md5 == lock', ck.get('memo_md5') == S['memo_lock_md5'], ck.get('memo_md5'), S['memo_lock_md5'])
        rec('C-M-0', f'{leg}: memo_bytes == lock', ck.get('memo_bytes') == S['memo_lock_bytes'], ck.get('memo_bytes'), S['memo_lock_bytes'])
        rec('C-M-0', f'{leg}: ledger_base_md5', ck.get('ledger_base_md5') == S['ledger_base_md5'])
        v, _ = getpath(ck, 'T1.list_md5'); rec('C-M-0', f'{leg}: T1 list md5 == lock', v == S['t1_list_md5'], v, S['t1_list_md5'])
        v, _ = getpath(ck, 'T1.state'); rec('C-M-0', f'{leg}: T1 state CLEAN', v == 'CLEAN', v)
        v, _ = getpath(ck, 'inputs.X1_md5'); rec('C-M-0', f'{leg}: X-1 md5', v == S['x1_md5'], v)
        v, _ = getpath(ck, 'inputs.X1_bytes'); rec('C-M-0', f'{leg}: X-1 bytes', v == S['x1_bytes'], v)
        rec('C-M-0', f'{leg}: instrument_md5 real 32-hex', bool(HEX32.match(str(ck.get('instrument_md5', '')))))
        rec('C-M-0', f'{leg}: no placeholders', not PLACEHOLDER.search(json.dumps(ck, ensure_ascii=False)))
        for e, code in S['value_domains']['election_choice'].items():
            got = choice_code((ck.get('elections') or {}).get(e))
            rec('C-M-0', f'{leg}: election {e} code', got == code, got, code)
    rec('C-M-0', 'INDEPENDENCE: instrument_md5 differ', chat.get('instrument_md5') != cc.get('instrument_md5'),
        chat.get('instrument_md5'), cc.get('instrument_md5'))
    if chat_bytes is not None and cc_bytes is not None:
        rec('C-M-0', 'INDEPENDENCE: checkpoints not byte-identical', chat_bytes != cc_bytes)

    # ---- C1 controls
    for name, fkeys in S['control_float_keys'].items():
        pa, _ = getpath(chat, f'controls.{name}.passed'); pb, _ = getpath(cc, f'controls.{name}.passed')
        rec('C1', f'{name}.passed (both True)', pa is True and pb is True, pa, pb)
        for k in fkeys:
            a, _ = getpath(chat, f'controls.{name}.{k}'); b, _ = getpath(cc, f'controls.{name}.{k}')
            rec('C1', f'{name}.{k}', close_abs(a, b, T['control_abs']), a, b)

    # ---- C2 phase1
    p1a, p1b = chat.get('phase1', {}), cc.get('phase1', {})
    rec('C2', 'config key set', set(p1a) == set(p1b) == set(S['config_keys']), sorted(p1a), sorted(p1b))
    for key in S['config_keys']:
        ra, rb = p1a.get(key, {}), p1b.get(key, {})
        for k in ('v_EM', 'v_S2E2', 'v_S2h'):
            rec('C2', f'[{key}].{k}', close_rel(ra.get(k), rb.get(k), T['phase1_v_rel']), ra.get(k), rb.get(k))
        for k in ('r_xtal_E2', 'r_xtal_h'):
            rec('C2', f'[{key}].{k}', close_abs(ra.get(k), rb.get(k), T['phase1_r_abs']), ra.get(k), rb.get(k))
        for k in ('lambda_mean', 'lambda_max'):
            rec('C2', f'[{key}].{k}', close_abs(ra.get(k), rb.get(k), T['phase1_lambda_abs']), ra.get(k), rb.get(k))
        rec('C2', f'[{key}].cov_lambda_v', close_abs(ra.get('cov_lambda_v'), rb.get('cov_lambda_v'), T['phase1_cov_abs']),
            ra.get('cov_lambda_v'), rb.get('cov_lambda_v'))
        rec('C2', f'[{key}].lambda_max_branch', ra.get('lambda_max_branch') == rb.get('lambda_max_branch')
            and ra.get('lambda_max_branch') in S['value_domains']['lambda_max_branch'], ra.get('lambda_max_branch'), rb.get('lambda_max_branch'))
        for sk in ('share_EM', 'share_S2E2'):
            sa, sb = ra.get(sk) or {}, rb.get(sk) or {}
            rec('C2', f'[{key}].{sk} keys', set(sa) == set(sb) and bool(sa), sorted(sa), sorted(sb))
            for br in sorted(set(sa) & set(sb)):
                rec('C2', f'[{key}].{sk}.{br}', close_abs(sa[br], sb[br], T['phase1_share_abs']), sa[br], sb[br])

    # ---- C3 phase2 + born_t0
    p2a, p2b = chat.get('phase2', {}), cc.get('phase2', {})
    rec('C3', 'phase2 key set', set(p2a) == set(p2b) == set(S['config_keys']))
    n_t = len(S['t_grid'])
    for key in S['config_keys']:
        ra, rb = p2a.get(key, {}), p2b.get(key, {})
        for k in ('vT_VRH', 'vT_HS_lo', 'vT_HS_hi'):
            rec('C3', f'[{key}].{k}', close_rel(ra.get(k), rb.get(k), T['pins_rel']), ra.get(k), rb.get(k))
        for k in ('r_agg_E2_VRH', 'r_agg_h_VRH', 'r_agg_E2_HS'):
            xa, xb = ra.get(k), rb.get(k)
            ok = isinstance(xa, list) and isinstance(xb, list) and len(xa) == len(xb) == n_t and all(close_abs(u, v, T['r_agg_abs']) for u, v in zip(xa, xb))
            rec('C3', f'[{key}].{k}[{n_t}]', ok)
        for k in ('S_t_E2', 'S_t_h'):
            rec('C3', f'[{key}].{k}', close_abs(ra.get(k), rb.get(k), T['S_t_abs']), ra.get(k), rb.get(k))
        for k in ('kappa2_E2', 'kappa2_h'):
            rec('C3', f'[{key}].{k}', close_rel(ra.get(k), rb.get(k), T['kappa2_rel'], T['kappa2_abs_floor']), ra.get(k), rb.get(k))
        for leg, r in (('chat', ra), ('cc', rb)):
            hd = r.get('halving_dev_kappa2')
            rec('C3', f'[{key}].halving_dev_kappa2 ({leg}) <= kappa2_rel', isinstance(hd, (int, float)) and hd <= T['kappa2_rel'], hd)
        xa, xb = ra.get('lambda_mean_t'), rb.get('lambda_mean_t')
        rec('C3', f'[{key}].lambda_mean_t[{n_t}]', isinstance(xa, list) and isinstance(xb, list) and len(xa) == len(xb) == n_t
            and all(close_abs(u, v, T['phase1_lambda_abs']) for u, v in zip(xa, xb)))
    ba, bb = chat.get('born_t0', {}), cc.get('born_t0', {})
    rec('C3', 'born_t0 key set', set(ba) == set(bb) == set(S['base_configs']))
    for key in S['base_configs']:
        for k in S['born_t0_keys']:
            a, b = (ba.get(key) or {}).get(k), (bb.get(key) or {}).get(k)
            rec('C3', f'born_t0[{key}].{k}', close_rel(a, b, T['born_rel'], T['tau_agg']), a, b)

    # ---- C4 states, verdict, quadrature, t-grid
    for f in ('F-MS-3', 'F-MS-2', 'F-MS-1'):
        a, _ = getpath(chat, f'falsifiers.{f}.state'); b, _ = getpath(cc, f'falsifiers.{f}.state')
        rec('C4', f'{f}.state', a == b and a in S['value_domains'][f'{f}.state'], a, b)
    a, b = chat.get('verdict_class'), cc.get('verdict_class')
    rec('C4', 'verdict_class', a == b and a in S['value_domains']['verdict_class'], a, b)
    for k in ('n_theta', 'n_phi'):
        a, _ = getpath(chat, f'quadrature.{k}'); b, _ = getpath(cc, f'quadrature.{k}')
        rec('C4', f'quadrature.{k}', a == b == S['quadrature'][k], a, b)
    for leg, ck in (('chat', chat), ('cc', cc)):
        dr, _ = getpath(ck, 'quadrature.doubling_residual')
        rec('C4', f'{leg}: doubling_residual <= tol', isinstance(dr, (int, float)) and dr <= S['quadrature']['doubling_tol'], dr)
        rec('C4', f'{leg}: t_grid == schema', ck.get('t_grid') == S['t_grid'])

    # ---- C5 compare step
    if chat_cmp is not None and cc_cmp is not None:
        ra, rb = chat_cmp.get('rows', []), cc_cmp.get('rows', [])
        rec('C5', 'rows count', len(ra) == len(rb), len(ra), len(rb))
        for i, (x, y) in enumerate(zip(ra, rb)):
            for k in S['compare_row_keys']:
                rec('C5', f'rows[{i}].{k}', x.get(k) == y.get(k), x.get(k), y.get(k))
        rec('C5', 'compare verdict_class', chat_cmp.get('verdict_class') == cc_cmp.get('verdict_class') == chat.get('verdict_class'))
    else:
        rec('C5', 'compare files supplied', False, chat_cmp is not None, cc_cmp is not None)

    misses = [r for r in R if r['result'] == 'MISS']
    return {'checks': R, 'n_checks': len(R), 'n_miss': len(misses), 'misses': misses,
            'S9_triggered': bool(misses), 'overall': 'C-M-0..C5 ALL PASS' if not misses else 'MISS -> S9'}


def cmd_compare(a):
    S = json.load(open(a.schema, encoding='utf-8'))
    cb, ccb = open(a.chat, 'rb').read(), open(a.cc, 'rb').read()
    chat, cc = json.loads(cb), json.loads(ccb)
    chat_cmp = json.load(open(a.chat_cmp, encoding='utf-8')) if a.chat_cmp else None
    cc_cmp = json.load(open(a.cc_cmp, encoding='utf-8')) if a.cc_cmp else None
    out = run_checks(chat, cc, S, chat_cmp, cc_cmp, cb, ccb)
    out.update({'comparator': os.path.basename(__file__), 'comparator_md5': md5f(os.path.abspath(__file__)),
                'schema_md5': md5f(a.schema), 'chat_checkpoint_md5': hashlib.md5(cb).hexdigest(),
                'cc_checkpoint_md5': hashlib.md5(ccb).hexdigest()})
    json.dump(out, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    for m in out['misses']:
        print(f'MISS {m["check"]:6} {m["item"]}  chat={m["chat"]!r} cc={m["cc"]!r}')
    print(f'{out["overall"]}  ({out["n_checks"]} checks, {out["n_miss"]} miss)  -> {a.out} {md5f(a.out)}')


# ---------------------------------------------------------------------- selftest
def synthetic(S, leg, seed):
    import random
    rnd = random.Random(seed)
    def f(x, jitter=0.0): return x + (rnd.random() - 0.5) * jitter
    ck = {'gate': 'G-MSCS1', 'leg': leg, 'instrument': f'g_mscs1_{leg}.py', 'instrument_md5': ('a' if leg == 'chat' else 'b') * 32,
          'memo_md5': S['memo_lock_md5'], 'memo_bytes': S['memo_lock_bytes'], 'ledger_base_md5': S['ledger_base_md5'], 'utc': 't',
          'elections': {'E-MS-1': '(a) descriptors', 'E-MS-2': '(a) all four', 'E-MS-2b': '(a+b) both arms',
                        'E-MS-2c': '(001+111) both axes', 'E-MS-3': '(a) t=0 Born', 'E-MS-4': '(a)', 'E-MS-5': '(a) fiber', 'E-MS-6': '(a) none'},
          'T1': {'list_md5': S['t1_list_md5'], 'state': 'CLEAN', 'numeric_collisions': 0},
          'inputs': {'X1_md5': S['x1_md5'], 'X1_bytes': S['x1_bytes']},
          'quadrature': {'n_theta': 64, 'n_phi': 128, 'doubling_residual': 3e-11}, 't_grid': list(S['t_grid']),
          'controls': {'F-CTRL-ISO': {'passed': True, 'r_xtal_E2': f(0, 1e-15), 'r_xtal_h': 0.0, 'lambda_max': 0.0, 'r_agg_max': 0.0},
                       'F-CTRL-SO3': {'passed': True, 'w_S2_mean_t0': f(0.4, 1e-12), 'dev_from_0p4': 1e-12, 'r_agg_0_E2': 0.0},
                       'F-CTRL-TEX': {'passed': True, 'r_agg_t1': f(0.03, 1e-9)},
                       'F-CTRL-POL': {'passed': True, 'split_plus_minus': 0.0, 'split_plus_avg': 0.0},
                       'PIN-A2AGG': {'passed': True, 'worst_rel_residual': 2e-10},
                       'F-CTRL-ADMIX': {'passed': True, 'r_xtal_h_projected': f(0, 1e-12)}},
          'phase1': {}, 'phase2': {}, 'born_t0': {},
          'falsifiers': {'F-MS-3': {'state': 'SILENT', 'worst_S_t': 1e-9}, 'F-MS-2': {'state': 'REGISTERED_NOT_EXECUTED'},
                         'F-MS-1': {'state': 'RETIRED_TO_CONTROL'}},
          'verdict_class': 'IDENTITY-DELIVERED'}
    for i, key in enumerate(S['config_keys']):
        ck['phase1'][key] = {'v_EM': f(8.0 + i, 1e-10), 'v_S2E2': f(7.8 + i, 1e-10), 'v_S2h': f(7.99 + i, 1e-10),
                             'r_xtal_E2': f(-0.025, 1e-10), 'r_xtal_h': f(-0.0012, 1e-10), 'lambda_mean': f(0.011, 1e-10),
                             'lambda_max': f(0.04, 1e-10), 'lambda_max_branch': 'qSV', 'cov_lambda_v': f(0.003, 1e-10),
                             'share_EM': {'qT1': 0.5, 'qT2': 0.49, 'qL': 0.01}, 'share_S2E2': {'qT1': 0.6, 'qT2': 0.4, 'qL': 0.0}}
        n = len(S['t_grid'])
        ck['phase2'][key] = {'vT_VRH': f(8.4, 1e-10), 'vT_HS_lo': f(8.3, 1e-10), 'vT_HS_hi': f(8.5, 1e-10),
                             'r_agg_E2_VRH': [f(-0.02 * t * t, 1e-8) for t in S['t_grid']],
                             'r_agg_h_VRH': [f(-0.001 * t * t, 1e-8) for t in S['t_grid']],
                             'r_agg_E2_HS': [f(-0.021 * t * t, 1e-8) for t in S['t_grid']],
                             'S_t_E2': f(0, 1e-9), 'S_t_h': f(0, 1e-9), 'kappa2_E2': f(-0.02, 1e-7), 'kappa2_h': f(-0.001, 1e-7),
                             'kappa3_E2': f(0.001, 1e-6), 'fit_residual': 1e-9, 'halving_dev_kappa2': 2e-5,
                             'lambda_mean_t': [f(0.01 * t * t, 1e-10) for t in S['t_grid']]}
    for key in S['base_configs']:
        ck['born_t0'][key] = {'D0_plus': f(-0.02, 1e-9), 'D0_minus': f(-0.02, 1e-9), 'D0_avg': f(-0.02, 1e-9), 'D2_avg': f(-0.018, 1e-9), 'a2agg_residual_rel': 2e-10}
    cmp_ = {'rows': [{'id': f'H-MS-{i}', 'predicted': 'x', 'machine': 'y', 'concordant': True} for i in range(1, 6)], 'verdict_class': 'IDENTITY-DELIVERED'}
    return ck, cmp_


def cmd_selftest(a):
    S = json.load(open(a.schema, encoding='utf-8'))
    chat, ccmp = synthetic(S, 'chat', 1); cc, cccmp = synthetic(S, 'cc', 2)
    base = run_checks(chat, cc, S, ccmp, cccmp, b'chat', b'cc')
    assert base['n_miss'] == 0, base['misses'][:5]
    print(f'  green  S1 two independent synthetic legs within tolerance -> ALL PASS ({base["n_checks"]} checks)')

    def expect(name, mutate, check):
        c2 = copy.deepcopy(cc); mutate(c2)
        out = run_checks(chat, c2, S, ccmp, copy.deepcopy(cccmp), b'chat', b'cc2')
        assert any(m['check'] == check for m in out['misses']), (name, out['misses'][:3])
        print(f'  green  {name} -> fires {check}')
    k0 = S['config_keys'][0]; b0 = S['base_configs'][0]
    expect('S2 verdict flip', lambda c: c.update(verdict_class='PROTECTION-BREACH'), 'C4')
    expect('S3 control flag False', lambda c: c['controls']['F-CTRL-SO3'].update(passed=False), 'C1')
    expect('S4 r_xtal beyond 1e-8', lambda c: c['phase1'][k0].update(r_xtal_E2=c['phase1'][k0]['r_xtal_E2'] + 1e-6), 'C2')
    expect('S5 branch label', lambda c: c['phase1'][k0].update(lambda_max_branch='qSH'), 'C2')
    expect('S6 S_t beyond 1e-6', lambda c: c['phase2'][k0].update(S_t_E2=5e-6), 'C3')
    expect('S7 kappa2 beyond 1e-4 rel', lambda c: c['phase2'][k0].update(kappa2_E2=c['phase2'][k0]['kappa2_E2'] * 1.01), 'C3')
    expect('S8 r_agg array element', lambda c: c['phase2'][k0]['r_agg_E2_VRH'].__setitem__(3, 0.5), 'C3')
    expect('S9 born_t0 beyond 1e-6 rel', lambda c: c['born_t0'][b0].update(D0_avg=c['born_t0'][b0]['D0_avg'] * 1.001), 'C3')
    expect('S10 T1 LIST_ABSENT rejected', lambda c: c['T1'].update(state='LIST_ABSENT'), 'C-M-0')
    expect('S11 election code', lambda c: c['elections'].update({'E-MS-1': '(b) envelope route'}), 'C-M-0')
    expect('S12 same instrument md5 (independence)', lambda c: c.update(instrument_md5='a' * 32), 'C-M-0')
    expect('S13 t_grid drift', lambda c: c['t_grid'].__setitem__(0, -0.6), 'C4')
    expect('S14 memo md5 not lock', lambda c: c.update(memo_md5='0' * 32), 'C-M-0')
    expect('S15 F-MS-3 state', lambda c: c['falsifiers']['F-MS-3'].update(state='FIRES'), 'C4')
    out = run_checks(chat, cc, S, ccmp, None, b'chat', b'cc'); assert any(m['check'] == 'C5' for m in out['misses'])
    print('  green  S16 missing compare file -> C5 MISS')
    # kappa2 tolerance is rel-with-floor: a 5e-5 relative change must PASS
    c3 = copy.deepcopy(cc); c3['phase2'][k0]['kappa2_E2'] *= (1 + 5e-5)
    out = run_checks(chat, c3, S, ccmp, copy.deepcopy(cccmp), b'chat', b'cc3'); assert out['n_miss'] == 0
    print('  green  S17 kappa2 within 1e-4 rel -> PASS')
    print(f'ALL 17/17 SUITES GREEN  (comparator {md5f(os.path.abspath(__file__))}, schema {md5f(a.schema)})')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('cmd', choices=['compare', 'selftest'])
    p.add_argument('--chat'); p.add_argument('--cc'); p.add_argument('--chat-cmp'); p.add_argument('--cc-cmp')
    p.add_argument('--schema', default=SCHEMA_DEFAULT)
    p.add_argument('--out', default='g_mscs1_twoleg_comparison.json')
    a = p.parse_args()
    {'compare': cmd_compare, 'selftest': cmd_selftest}[a.cmd](a)


if __name__ == '__main__':
    main()
=====END-EMBED name=g_mscs1_compare_v1_0.py=====

=====BEGIN-EMBED name=g_mscs1_schema_v1_0.json md5=76a42db3fd6ad82e485752bc2ddb24d5 bytes=3906 encoding=raw=====
{
  "gate": "G-MSCS1",
  "schema_version": "1.0",
  "state": "CANDIDATE — freezes on the author's lock word (memo_lock_md5 / memo_lock_bytes then final)",
  "memo_lock_md5": "3f30262eaec461fb5fd3202835f7de37",
  "memo_lock_bytes": 34837,
  "ledger_base_md5": "d095a7003bb0d4c177e7451e1d14c4c6",
  "t1_list_md5": "fef2827100d3f85e0a6341b44f0c00bf",
  "x1_md5": "200e7a8b775577564369c6924d38a84c",
  "x1_bytes": 2767,
  "config_keys": ["hex_step|a", "hex_step|b", "hex_gem8|a", "hex_gem8|b",
                  "cubic_step|001", "cubic_step|111", "cubic_gem8|001", "cubic_gem8|111"],
  "base_configs": ["hex_step", "hex_gem8", "cubic_step", "cubic_gem8"],
  "t_grid": [-0.5, -0.25, -0.1, -0.05, -0.02, 0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0],
  "quadrature": {"n_theta": 64, "n_phi": 128, "doubling_tol": 1e-10},
  "tolerances": {
    "tau_agg": 1e-6,
    "phase1_v_rel": 1e-8, "phase1_r_abs": 1e-8, "phase1_lambda_abs": 1e-8, "phase1_share_abs": 1e-8, "phase1_cov_abs": 1e-8,
    "pins_rel": 1e-8, "born_rel": 1e-6, "r_agg_abs": 1e-6, "S_t_abs": 1e-6, "kappa2_rel": 1e-4, "kappa2_abs_floor": 1e-6,
    "control_abs": 1e-6
  },
  "required_keys": [
    "gate", "leg", "instrument", "instrument_md5", "memo_md5", "memo_bytes", "ledger_base_md5", "utc",
    "elections.E-MS-1", "elections.E-MS-2", "elections.E-MS-2b", "elections.E-MS-2c", "elections.E-MS-3",
    "elections.E-MS-4", "elections.E-MS-5", "elections.E-MS-6",
    "T1.list_md5", "T1.state", "T1.numeric_collisions",
    "inputs.X1_md5", "inputs.X1_bytes",
    "quadrature.n_theta", "quadrature.n_phi", "quadrature.doubling_residual",
    "t_grid",
    "controls.F-CTRL-ISO.passed", "controls.F-CTRL-SO3.passed", "controls.F-CTRL-TEX.passed",
    "controls.F-CTRL-POL.passed", "controls.PIN-A2AGG.passed", "controls.F-CTRL-ADMIX.passed",
    "phase1", "phase2", "born_t0",
    "falsifiers.F-MS-3.state", "falsifiers.F-MS-2.state", "falsifiers.F-MS-1.state",
    "verdict_class"
  ],
  "phase1_keys": ["v_EM", "v_S2E2", "v_S2h", "r_xtal_E2", "r_xtal_h", "lambda_mean", "lambda_max",
                  "lambda_max_branch", "cov_lambda_v", "share_EM", "share_S2E2"],
  "phase2_keys": ["vT_VRH", "vT_HS_lo", "vT_HS_hi", "r_agg_E2_VRH", "r_agg_h_VRH", "r_agg_E2_HS",
                  "S_t_E2", "S_t_h", "kappa2_E2", "kappa2_h", "kappa3_E2", "fit_residual",
                  "halving_dev_kappa2", "lambda_mean_t"],
  "born_t0_keys": ["D0_plus", "D0_minus", "D0_avg", "D2_avg", "a2agg_residual_rel"],
  "control_float_keys": {
    "F-CTRL-ISO": ["r_xtal_E2", "r_xtal_h", "lambda_max", "r_agg_max"],
    "F-CTRL-SO3": ["w_S2_mean_t0", "dev_from_0p4", "r_agg_0_E2"],
    "F-CTRL-TEX": ["r_agg_t1"],
    "F-CTRL-POL": ["split_plus_minus", "split_plus_avg"],
    "PIN-A2AGG": ["worst_rel_residual"],
    "F-CTRL-ADMIX": ["r_xtal_h_projected"]
  },
  "compare_file_keys": ["rows", "verdict_class"],
  "compare_row_keys": ["id", "concordant"],
  "value_domains": {
    "verdict_class": ["IDENTITY-DELIVERED", "PROTECTION-BREACH", "INDETERMINATE"],
    "F-MS-3.state": ["SILENT", "FIRES"],
    "F-MS-2.state": ["REGISTERED_NOT_EXECUTED"],
    "F-MS-1.state": ["RETIRED_TO_CONTROL"],
    "T1.state": ["CLEAN"],
    "lambda_max_branch": ["qT1", "qT2", "qSV", "qSH", "qL"],
    "election_choice": {"E-MS-1": "a", "E-MS-2": "a", "E-MS-2b": "a+b", "E-MS-2c": "001+111",
                        "E-MS-3": "a", "E-MS-4": "a", "E-MS-5": "a", "E-MS-6": "a"}
  },
  "notes": [
    "Elections are compared by the canonical choice code in value_domains.election_choice; each leg's elections.* string must START with the code in parentheses, e.g. '(a) ...', '(a+b) ...', '(001+111) ...'.",
    "T1.state must be CLEAN on both legs; there is no LIST_ABSENT value in this gate (D-T1 retired).",
    "Free text (reasons, notes) is never compared. Hypothesis rows compare id + concordant only.",
    "share_EM / share_S2E2 are dicts branch->float; compared key-for-key."
  ]
}
=====END-EMBED name=g_mscs1_schema_v1_0.json=====

=====BEGIN-EMBED name=tools/t1/T1_forbidden_G_MSCS1.txt md5=fef2827100d3f85e0a6341b44f0c00bf bytes=1433 encoding=raw=====
# T1 forbidden-string list — Gate G-MSCS1 (gate-specific), composed September 19, 2026
# Stratum 1: base list, author-supplied September 19, 2026 (file T1_base_author_20260919.txt, md5 05302210cc4ceb70553acbe8379e9fc3, 143 B, 11 pattern lines)
# Provenance note: the author cited this as the G-2a-L1 list 04438b74 (13 pattern lines, 117 B); no line-ending / comment / ordering variant of the supplied text hashes to 04438b74 — recorded as H-MS-0; this file's authority is the author's supply, not byte-identity with 04438b74.
# Scanner rule: pattern lines only ('#' lines ignored); case-sensitive substring; bare numeric patterns under the contextual numeric rule (D-W-7 lineage): a hit counts only when the maximal numeric token containing the match equals the pattern; embedded-in-a-longer-literal matches are logged as formatting collisions, not forbidden references.
Mpc
Gpc
LIGO
170817
299792458
SME
GW1
3.19
0.019
Hz
GW
# Stratum 2: G-MSCS1 additions — SI speed of light in scientific form, the 2017 multi-messenger tensor-speed bound digit strings, SI speed units, event/collaboration/instrument identifiers, the observational-search identifiers, and the anisotropic-dispersion coefficient names of the observational dialect
2.99792458
3e-15
7e-16
3×10⁻¹⁵
7×10⁻¹⁶
3×10^-15
7×10^-16
3 × 10^-15
7 × 10^-16
m/s
km/s
LVC
Virgo
KAGRA
Fermi
GRB
GWTC
Haegel
2210.04481
ApJL 848
848, L13
k_(I)
k_(V)
k_(E)
k_(B)
=====END-EMBED name=tools/t1/T1_forbidden_G_MSCS1.txt=====

=====BEGIN-EMBED name=tools/t1/t1_scan.py md5=6b86290090a8c84f1b1a0a99ec0bf697 bytes=1967 encoding=raw=====
#!/usr/bin/env python3
"""t1_scan.py — T1 forbidden-string scanner, G-MSCS1 (frozen with the gate list).
Rules: pattern lines only ('#' comment lines and blank lines ignored); case-sensitive substring;
bare numeric patterns (regex ^[0-9.e+\-×^ ⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+$) under the contextual numeric rule:
a match counts only if the maximal token of numeric characters containing it equals the pattern;
otherwise it is logged as a formatting COLLISION (not a hit). Hits are reported by pattern INDEX only.
Usage: t1_scan.py LIST FILE [FILE...]   -> exit 0 clean, 1 hit, 2 usage.
"""
import re, sys
NUMCHARS = set("0123456789.eE+-×^ ⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
def load(list_path):
    pats = [l.rstrip("\n") for l in open(list_path, encoding="utf-8")]
    return [p for p in pats if p.strip() and not p.startswith("#")]
def is_numeric(p): return all(c in NUMCHARS for c in p)
def scan_text(text, pats):
    hits, collisions = [], []
    for i, p in enumerate(pats):
        start = 0
        while True:
            j = text.find(p, start)
            if j < 0: break
            if is_numeric(p):
                a = j
                while a > 0 and text[a-1] in NUMCHARS and text[a-1] != " ": a -= 1
                b = j + len(p)
                while b < len(text) and text[b] in NUMCHARS and text[b] != " ": b += 1
                tok = text[a:b]
                (hits if tok == p else collisions).append((i, j))
            else:
                hits.append((i, j))
            start = j + 1
    return hits, collisions
def main():
    if len(sys.argv) < 3: print(__doc__); sys.exit(2)
    pats = load(sys.argv[1]); rc = 0
    for f in sys.argv[2:]:
        text = open(f, "rb").read().decode("utf-8", "replace")
        hits, coll = scan_text(text, pats)
        print(f"{f}: {'HIT' if hits else 'CLEAN'}  hits={[i for i,_ in hits]}  numeric_collisions={len(coll)}")
        if hits: rc = 1
    sys.exit(rc)
if __name__ == "__main__": main()
=====END-EMBED name=tools/t1/t1_scan.py=====

=====BEGIN-EMBED name=tools/t1/T1_base_author_20260919.txt md5=05302210cc4ceb70553acbe8379e9fc3 bytes=143 encoding=raw=====
# T1 forbidden-string list, base stratum
# Recovered from G-2a-L1 dispatch (0c5588ee)
#
Mpc
Gpc
LIGO
170817
299792458
SME
GW1
3.19
0.019
Hz
GW
=====END-EMBED name=tools/t1/T1_base_author_20260919.txt=====

=====BEGIN-EMBED name=inputs/poly_vrh_results.json md5=200e7a8b775577564369c6924d38a84c bytes=2767 encoding=raw=====
{
 "gem8_fcc_iso": {
  "A": 946.2397864450644,
  "lin": -214.4531034305213,
  "base_res": 4.7100744185220225e-09,
  "seconds": 38.00324010848999
 },
 "vrh": {
  "controls": {
   "cubic_closed_form_maxerr": 4.440892098500626e-16,
   "iso_null": "PASS"
  },
  "hex:step": {
   "label": "TRUE-OPTIMUM (V4.72 R1 two-leg)",
   "C_over_rho": {
    "C11": 238.4183,
    "C12": 108.5389,
    "C13": 57.4751,
    "C33": 287.6688,
    "C44": 60.0308,
    "C66": 64.9223
   },
   "K_VRH": 134.609,
   "G_V": 73.065,
   "G_R": 68.697,
   "G_VRH": 70.881,
   "VR_spread_pct": 6.16,
   "AU": 0.3179,
   "vT_V": 8.5478,
   "vT_R": 8.2883,
   "vT_VRH": 8.4191,
   "vT_halfwidth_pct": 1.54,
   "single_crystal_input": {
    "mean": 8.472742664753259,
    "std_pct": 9.164259025458835,
    "maxdev_pct": 19.105382411223452
   }
  },
  "hex:gem8": {
   "label": "TRUE-OPTIMUM (V4.72 R1 two-leg)",
   "C_over_rho": {
    "C11": 377.5438,
    "C12": 200.2076,
    "C13": 111.0018,
    "C33": 467.7554,
    "C44": 84.8245,
    "C66": 88.6835
   },
   "K_VRH": 229.696,
   "G_V": 105.042,
   "G_R": 96.63,
   "G_VRH": 100.836,
   "VR_spread_pct": 8.34,
   "AU": 0.4352,
   "vT_V": 10.249,
   "vT_R": 9.8301,
   "vT_VRH": 10.0417,
   "vT_halfwidth_pct": 2.09,
   "single_crystal_input": {
    "mean": 10.120315551687215,
    "std_pct": 10.906419350629072,
    "maxdev_pct": 22.59028052217178
   }
  },
  "cubic:step": {
   "label": "polished-at-FROZEN geometry (labelled)",
   "C_over_rho": {
    "C44": 85.2934,
    "C12": 99.349,
    "C11": 172.7994
   },
   "K_VRH": 123.832,
   "G_V": 65.866,
   "G_R": 55.784,
   "G_VRH": 60.825,
   "VR_spread_pct": 16.58,
   "AU": 0.9037,
   "vT_V": 8.1158,
   "vT_R": 7.4689,
   "vT_VRH": 7.799,
   "vT_halfwidth_pct": 4.15,
   "single_crystal_input": {
    "mean": 7.97359836526451,
    "std_pct": 13.113372264449117,
    "maxdev_pct": 23.995868277249034
   }
  },
  "cubic:gem8": {
   "label": "polished-at-FROZEN geometry (labelled; iso measured this session)",
   "C_over_rho": {
    "C44": 131.5436,
    "C12": 179.3756,
    "C11": 272.0753
   },
   "K_VRH": 210.276,
   "G_V": 97.466,
   "G_R": 75.808,
   "G_VRH": 86.637,
   "VR_spread_pct": 25.0,
   "AU": 1.4285,
   "vT_V": 9.8725,
   "vT_R": 8.7068,
   "vT_VRH": 9.3079,
   "vT_halfwidth_pct": 6.26,
   "single_crystal_input": {
    "mean": 9.63705464398007,
    "std_pct": 15.808320696928124,
    "maxdev_pct": 29.351684168073366
   }
  },
  "mixture:step": {
   "f_hcp -> vT": {
    "0.0": 7.799,
    "0.25": 7.9499,
    "0.5": 8.1032,
    "0.75": 8.2594,
    "1.0": 8.4191
   },
   "phase_span_pct": 7.65
  },
  "mixture:gem8": {
   "f_hcp -> vT": {
    "0.0": 9.3079,
    "0.25": 9.4864,
    "0.5": 9.6679,
    "0.75": 9.8527,
    "1.0": 10.0417
   },
   "phase_span_pct": 7.59
  }
 }
}
=====END-EMBED name=inputs/poly_vrh_results.json=====

=====BEGIN-EMBED name=inputs/cc_p2_phase1.json md5=aaae206733b0f0a378a5c6b600274d3f bytes=11454 encoding=raw=====
{
 "gem8_cubic": {
  "D0": {
   "L": -0.01668297768776499,
   "T": -0.04367714392697761
  },
  "D2_analytic": {
   "L": -0.05236302368972408,
   "T": -0.039713976791286104
  },
  "I0": {
   "LL": 1238.6944066666665,
   "LT": 1858.04161,
   "TL": 929.0208050000002,
   "TT": 1393.5312075000006
  },
  "I2": {
   "LL": 480.3100760544217,
   "LT": 669.9061587074835,
   "TL": 334.9530793537419,
   "TT": 483.470010765307
  },
  "KK": {
   "alpha_T": [
    1.2059988591623373e-08,
    6.093326140788086e-08,
    4.672152484748265e-07,
    3.015849425306252e-06,
    1.4810677454816918e-05
   ],
   "alpha_T_bank": [
    1.205998859162398e-08,
    6.09332614078839e-08,
    4.672152484748498e-07,
    3.0158494253064023e-06,
    1.4810677454817654e-05
   ],
   "alpha_tie_max_rel": 5.034420762517192e-14,
   "pass": true
  },
  "V_L": 18.44533274300033,
  "V_T": 9.872492086601033,
  "kernel_controls": {
   "LL": {
    "max_deg_gt4_over_even": 2.2697905532710697e-14,
    "max_odd_over_even": 2.2697905532710697e-14
   },
   "LT": {
    "max_deg_gt4_over_even": 7.080647506624208e-15,
    "max_odd_over_even": 7.080647506624208e-15
   },
   "TL": {
    "max_deg_gt4_over_even": 7.340892379169704e-15,
    "max_odd_over_even": 6.9264942435015345e-15
   },
   "TT": {
    "max_deg_gt4_over_even": 1.01060138172425e-14,
    "max_odd_over_even": 7.893624896176638e-15
   }
  },
  "lam_bar": 145.29809999999998,
  "mu_bar": 97.46610000000001,
  "phi024": {
   "LL": [
    497.68971696428565,
    331.7931446428565,
    55.29885744047701
   ],
   "LT": [
    829.4828616071421,
    331.7931446428565,
    -55.29885744047152
   ],
   "TL": [
    414.74143080357123,
    165.89657232142747,
    -27.649428720234816
   ],
   "TT": [
    663.5862892857137,
    82.94828616071477,
    27.649428720241552
   ]
  },
  "pin": {
   "Q_L_a": 0.1880670060728792,
   "Q_L_a_bank": 0.1880670060728289,
   "Q_L_a_rel": 2.675687758417073e-13,
   "Q_T_a": 0.07549430207120401,
   "Q_T_a_bank": 0.07549430207120778,
   "Q_T_a_rel": 4.981674633365546e-14,
   "V_L": 18.44533274300033,
   "V_L_bank": 18.44533274300033,
   "V_L_rel": 0.0,
   "V_T": 9.872492086601033,
   "V_T_bank": 9.872492086601033,
   "V_T_rel": 0.0,
   "int_Phi_TL": 929.0208050000002,
   "int_Phi_TL_bank": 929.020805000044,
   "int_Phi_TL_rel": 4.711351165361695e-14,
   "int_Phi_TT": 1393.5312075000006,
   "int_Phi_TT_bank": 1393.5312075000702,
   "int_Phi_TT_rel": 4.992808507707963e-14,
   "pin_pass": true
  },
  "reciprocity_LT_over_TL_minus2": -4.440892098500626e-16,
  "voigt_closed_vs_mean_rel": {
   "G": 1.4580305065250382e-16,
   "K": 0.0
  },
  "xi_doubling": {
   "D0_L_rel": 1.0398164574954888e-15,
   "D0_T_rel": 2.5418855831812224e-15,
   "D2_L_rel": 1.1926363440203796e-15,
   "D2_T_rel": 4.368042729876988e-15,
   "Q_T_rel": 2.7573844834128014e-15
  }
 },
 "gem8_hex": {
  "D0": {
   "L": -0.010953813609991054,
   "T": -0.028917807603071687
  },
  "D2_analytic": {
   "L": -0.034406827351899046,
   "T": -0.025933693584294194
  },
  "I0": {
   "LL": 953.8723588723701,
   "LT": 1430.7785639784768,
   "TL": 715.3892819892384,
   "TT": 1073.0614422362999
  },
  "I2": {
   "LL": 343.017191168346,
   "LT": 495.1333487826623,
   "TL": 247.5666743913318,
   "TT": 364.29596534916857
  },
  "KK": {
   "alpha_T": [
    7.990630478908683e-09,
    4.037275648361137e-08,
    3.095639014886767e-07,
    1.998207300390396e-06,
    9.81290545595844e-06
   ],
   "alpha_T_bank": [
    7.990630478908698e-09,
    4.037275648361146e-08,
    3.09563901488677e-07,
    1.9982073003904e-06,
    9.812905455958456e-06
   ],
   "alpha_tie_max_rel": 2.130812736069577e-15,
   "pass": true
  },
  "V_L": 19.228938954953616,
  "V_T": 10.248997674569603,
  "kernel_controls": {
   "LL": {
    "max_deg_gt4_over_even": 1.0552145556578835e-14,
    "max_odd_over_even": 1.0552145556578835e-14
   },
   "LT": {
    "max_deg_gt4_over_even": 2.932060058012014e-14,
    "max_odd_over_even": 7.042397508190268e-15
   },
   "TL": {
    "max_deg_gt4_over_even": 2.6539691207748714e-15,
    "max_odd_over_even": 1.70536217740606e-15
   },
   "TT": {
    "max_deg_gt4_over_even": 2.379714005433374e-14,
    "max_odd_over_even": 1.3439621213319739e-14
   }
  },
  "lam_bar": 159.66818666666643,
  "mu_bar": 105.04195333333314,
  "phi024": {
   "LL": [
    473.5523264794418,
    -295.07053445048945,
    508.7034888678655
   ],
   "LT": [
    637.6476993196198,
    538.4468413295792,
    -508.7034888678726
   ],
   "TL": [
    318.8238496598094,
    269.22342066478615,
    -254.35174443392802
   ],
   "TT": [
    545.9407655804821,
    -180.84118004734842,
    254.3517444339197
   ]
  },
  "pin": {
   "Q_L_a": 0.12513252572358866,
   "Q_L_a_bank": 0.12513252572355138,
   "Q_L_a_rel": 2.978900796274969e-13,
   "Q_T_a": 0.050020548478532025,
   "Q_T_a_bank": 0.05002054847853209,
   "Q_T_a_rel": 1.2484878122031685e-15,
   "V_L": 19.228938954953616,
   "V_L_bank": 19.22893895495363,
   "V_L_rel": 7.390347823399325e-16,
   "V_T": 10.248997674569603,
   "V_T_bank": 10.248997674569612,
   "V_T_rel": 8.666002743896833e-16,
   "int_Phi_TL": 715.3892819892384,
   "int_Phi_TL_bank": 715.3892819892442,
   "int_Phi_TL_rel": 8.104718465560672e-15,
   "int_Phi_TT": 1073.0614422362999,
   "int_Phi_TT_bank": 1073.0614422363049,
   "int_Phi_TT_rel": 4.661635077788526e-15,
   "pin_pass": true
  },
  "reciprocity_LT_over_TL_minus2": 0.0,
  "voigt_closed_vs_mean_rel": {
   "G": 1.7587364422992076e-15,
   "K": 1.7323055802273402e-15
  },
  "xi_doubling": {
   "D0_L_rel": 4.751012399173614e-16,
   "D0_T_rel": 9.598091251108764e-16,
   "D2_L_rel": 1.210032038049722e-15,
   "D2_T_rel": 1.872940203040208e-15,
   "Q_T_rel": 1.2484878122031685e-15
  }
 },
 "step_cubic": {
  "D0": {
   "L": -0.013075851820715967,
   "T": -0.031513422434338065
  },
  "D2_analytic": {
   "L": -0.03767052681317584,
   "T": -0.028537471107946213
  },
  "I0": {
   "LL": 402.58048874496035,
   "LT": 603.8707331174409,
   "TL": 301.9353665587196,
   "TT": 452.9030498380795
  },
  "I2": {
   "LL": 156.10263849294387,
   "LT": 217.72210105594823,
   "TL": 108.86105052797355,
   "TT": 157.12962953566003
  },
  "KK": {
   "alpha_T": [
    8.638764272947385e-09,
    4.364763605402606e-08,
    3.3467889268691204e-07,
    2.1603940446972353e-06,
    1.0610160330024815e-05
   ],
   "alpha_T_bank": [
    8.638764272946882e-09,
    4.3647636054023514e-08,
    3.3467889268689256e-07,
    2.1603940446971086e-06,
    1.06101603300242e-05
   ],
   "alpha_tie_max_rel": 5.861496698962824e-14,
   "pass": true
  },
  "V_L": 14.54833186313813,
  "V_T": 8.115794477437195,
  "kernel_controls": {
   "LL": {
    "max_deg_gt4_over_even": 3.5578408850307735e-15,
    "max_odd_over_even": 3.385236638132699e-15
   },
   "LT": {
    "max_deg_gt4_over_even": 7.178960189659752e-15,
    "max_odd_over_even": 1.711255259819206e-15
   },
   "TL": {
    "max_deg_gt4_over_even": 2.1434326904376402e-14,
    "max_odd_over_even": 3.6575780918521824e-15
   },
   "TT": {
    "max_deg_gt4_over_even": 1.7147074523169764e-14,
    "max_odd_over_even": 3.984522480373865e-16
   }
  },
  "lam_bar": 79.92172000000005,
  "mu_bar": 65.86612000000007,
  "phi024": {
   "LL": [
    161.75108922788584,
    107.8340594852569,
    17.97234324754358
   ],
   "LT": [
    269.585148713143,
    107.83405948525721,
    -17.972343247541566
   ],
   "TL": [
    134.79257435657144,
    53.91702974262874,
    -8.986171623772838
   ],
   "TT": [
    215.66811897051423,
    26.958514871315195,
    8.986171623768994
   ]
  },
  "pin": {
   "Q_L_a": 0.12925237478417928,
   "Q_L_a_bank": 0.12925237478415366,
   "Q_L_a_rel": 1.9820445338820363e-13,
   "Q_T_a": 0.0540776282465218,
   "Q_T_a_bank": 0.05407762824651864,
   "Q_T_a_rel": 5.838267743335906e-14,
   "V_L": 14.54833186313813,
   "V_L_bank": 14.548331863138124,
   "V_L_rel": 4.884015174003829e-16,
   "V_T": 8.115794477437195,
   "V_T_bank": 8.11579447743719,
   "V_T_rel": 6.566295552476293e-16,
   "int_Phi_TL": 301.9353665587196,
   "int_Phi_TL_bank": 301.9353665587016,
   "int_Phi_TL_rel": 5.949127644350345e-14,
   "int_Phi_TT": 452.9030498380795,
   "int_Phi_TT_bank": 452.90304983805186,
   "int_Phi_TT_rel": 6.099738470789593e-14,
   "pin_pass": true
  },
  "reciprocity_LT_over_TL_minus2": 5.773159728050814e-15,
  "voigt_closed_vs_mean_rel": {
   "G": 6.472609005298318e-16,
   "K": 8.033110030359347e-16
  },
  "xi_doubling": {
   "D0_L_rel": 5.306647703757238e-16,
   "D0_T_rel": 4.183581914942399e-15,
   "D2_L_rel": 9.20997725664968e-16,
   "D2_T_rel": 7.902383887624476e-15,
   "Q_T_rel": 5.5174838013943424e-15
  }
 },
 "step_hex": {
  "D0": {
   "L": -0.008620711279811694,
   "T": -0.020528244595327105
  },
  "D2_analytic": {
   "L": -0.02432261470924973,
   "T": -0.01834766316394585
  },
  "I0": {
   "LL": 322.1605477326224,
   "LT": 483.1433976910814,
   "TL": 241.57169884554034,
   "TT": 362.2844803374219
  },
  "I2": {
   "LL": 115.4016137175511,
   "LT": 167.60548120803617,
   "TL": 83.80274060401796,
   "TT": 123.43047361632878
  },
  "KK": {
   "alpha_T": [
    5.621633954903388e-09,
    2.8403502085273183e-08,
    2.177910805502445e-07,
    1.4058711219313889e-06,
    6.904514358125152e-06
   ],
   "alpha_T_bank": [
    5.621633954903736e-09,
    2.840350208527493e-08,
    2.1779108055025785e-07,
    1.4058711219314753e-06,
    6.904514358125577e-06
   ],
   "alpha_tie_max_rel": 6.179980056674122e-14,
   "pass": true
  },
  "V_L": 15.232487212095954,
  "V_T": 8.547779438739243,
  "kernel_controls": {
   "LL": {
    "max_deg_gt4_over_even": 6.5634636440479645e-15,
    "max_odd_over_even": 6.5634636440479645e-15
   },
   "LT": {
    "max_deg_gt4_over_even": 1.458541610039962e-14,
    "max_odd_over_even": 1.3840269523511785e-15
   },
   "TL": {
    "max_deg_gt4_over_even": 1.3220365013093187e-14,
    "max_odd_over_even": 3.621102060809454e-15
   },
   "TT": {
    "max_deg_gt4_over_even": 8.826949188977026e-15,
    "max_odd_over_even": 4.948417683912162e-15
   }
  },
  "lam_bar": 85.89960000000005,
  "mu_bar": 73.06453333333336,
  "phi024": {
   "LL": [
    158.5851525074286,
    -80.24257012380959,
    146.2132236674289
   ],
   "LT": [
    216.74348310876192,
    162.21258141079502,
    -146.21322366743098
   ],
   "TL": [
    108.37174155438086,
    81.10629070539629,
    -73.10661183371398
   ],
   "TT": [
    182.4041833633014,
    -47.64979668399915,
    73.10661183371293
   ]
  },
  "pin": {
   "Q_L_a": 0.08363194915794381,
   "Q_L_a_bank": 0.08363194915792597,
   "Q_L_a_rel": 2.1323139676396874e-13,
   "Q_T_a": 0.035190738866067876,
   "Q_T_a_bank": 0.03519073886607002,
   "Q_T_a_rel": 6.092847963401631e-14,
   "V_L": 15.232487212095954,
   "V_L_bank": 15.23248721209595,
   "V_L_rel": 2.332326710229784e-16,
   "V_T": 8.547779438739243,
   "V_T_bank": 8.54777943873924,
   "V_T_rel": 2.078150064740387e-16,
   "int_Phi_TL": 241.57169884554034,
   "int_Phi_TL_bank": 241.57169884555444,
   "int_Phi_TL_rel": 5.835604064900508e-14,
   "int_Phi_TT": 362.2844803374219,
   "int_Phi_TT_bank": 362.28448033744377,
   "int_Phi_TT_rel": 6.040754558690158e-14,
   "pin_pass": true
  },
  "reciprocity_LT_over_TL_minus2": 3.1086244689504383e-15,
  "voigt_closed_vs_mean_rel": {
   "G": 5.834919105157176e-16,
   "K": 4.2228451936722203e-16
  },
  "xi_doubling": {
   "D0_L_rel": 2.817183858198499e-15,
   "D0_T_rel": 3.211160690384802e-15,
   "D2_L_rel": 3.993999650775925e-15,
   "D2_T_rel": 5.8619375421012316e-15,
   "Q_T_rel": 3.5492318233409722e-15
  }
 }
}
=====END-EMBED name=inputs/cc_p2_phase1.json=====

=====BEGIN-EMBED name=inputs/poly1_phase1full_cc.json md5=ec87e42f0f617b00c4985ba2aceac339 bytes=8140 encoding=raw=====
{
 "phase1a": {
  "step_hex": {
   "sym": "hex",
   "KV_pinned": 134.6092888888889,
   "KR_pinned": 134.61592608974317,
   "GV_pinned": 73.06221333333333,
   "GR_pinned": 68.69358023952627,
   "KV_gen": 134.6092888888889,
   "GV_gen": 73.06453333333334,
   "KR_gen": 134.60823359539017,
   "GR_gen": 68.69659702931513,
   "quad_doubling_rel": 7.027711745877241e-14,
   "mean_vs_voigtiso_rel": 2.142414567484955e-15,
   "V_tot": 9058.573367052675,
   "V_tot_closed": 9058.573367053235,
   "V_tot_rel_resid": 6.183942247162122e-14,
   "Phi_G": 1.696969970313957,
   "Phi_full": 0.033569485097689596,
   "pinned_46i_contractions": {
    "dc15_sq": 116.37142042606328,
    "dc25_sq": 100.37206268269792,
    "dc35_sq": 116.37142042606324,
    "dc45_sq": 78.47368410679343,
    "dc55_sq": 129.38731440624906,
    "dc56_sq": 78.47368410679337,
    "dc15dc25": -48.57562665920639,
    "dc15dc35": -69.29659655266633,
    "dc25dc35": -48.575626659206115
   }
  },
  "gem8_hex": {
   "sym": "hex",
   "KV_pinned": 229.69615555555558,
   "KR_pinned": 229.689087784171,
   "GV_pinned": 105.04400666666666,
   "GR_pinned": 96.63344350468611,
   "KV_gen": 229.69615555555552,
   "GV_gen": 105.04195333333332,
   "KR_gen": 229.69594530872436,
   "GR_gen": 96.63040078152181,
   "quad_doubling_rel": 8.693046282814976e-13,
   "mean_vs_voigtiso_rel": 3.770716985236286e-15,
   "V_tot": 26826.985670855684,
   "V_tot_closed": 26826.98567085876,
   "V_tot_rel_resid": 1.1468603844377867e-13,
   "Phi_G": 2.4312483287281066,
   "Phi_full": 0.038571167325759215,
   "pinned_46i_contractions": {
    "dc15_sq": 333.6955258906673,
    "dc25_sq": 303.9521734289541,
    "dc35_sq": 333.69552589066654,
    "dc45_sq": 236.2151005969523,
    "dc55_sq": 383.2362293701153,
    "dc56_sq": 236.21510059695197,
    "dc15dc25": -153.6063515340937,
    "dc15dc35": -178.42518841561795,
    "dc25dc35": -153.60635153409436
   }
  },
  "step_cubic": {
   "sym": "cubic",
   "KV_pinned": 123.83246666666666,
   "KR_pinned": 123.83246666666666,
   "GV_pinned": 65.86612,
   "GR_pinned": 55.78412874515961,
   "KV_gen": 123.83246666666668,
   "GV_gen": 65.86612,
   "KR_gen": 123.83246666666672,
   "GR_gen": 55.784128745159606,
   "quad_doubling_rel": 2.2803980925800715e-13,
   "mean_vs_voigtiso_rel": 6.175734343455089e-15,
   "V_tot": 11322.57624595063,
   "V_tot_closed": 11322.576245951932,
   "V_tot_rel_resid": 1.1501910535116622e-13,
   "Phi_G": 2.6098833201093443,
   "Phi_full": 0.0503724334998733,
   "pinned_46i_contractions": {
    "dc15_sq": 179.7234324754278,
    "dc25_sq": 89.86171623771413,
    "dc35_sq": 179.72343247542943,
    "dc45_sq": 89.86171623771396,
    "dc55_sq": 161.75108922785148,
    "dc56_sq": 89.8617162377143,
    "dc15dc25": -44.930858118857046,
    "dc15dc35": -134.7925743565711,
    "dc25dc35": -44.93085811885689
   },
   "nu": -97.13640000000002,
   "closed_basis_fit_resid": 2.1818566833297854e-12,
   "abc_machine": [
    11.981562165003213,
    52.41933447199843,
    -14.976952706284658
   ],
   "a_vs_pinned_clean_string_rel": 2.116862241052786e-12,
   "bc_pinned_strings": "corrupted in transport -- not consumed (pin E3); machine values above",
   "cubic_collapse_rel": 1.2145839889399213e-13,
   "A_anchor_rel": 2.1687096563027808e-12
  },
  "gem8_cubic": {
   "sym": "cubic",
   "KV_pinned": 210.2755,
   "KR_pinned": 210.2755,
   "GV_pinned": 97.46610000000001,
   "GR_pinned": 75.8078704378548,
   "KV_gen": 210.27550000000002,
   "GV_gen": 97.46610000000004,
   "KR_gen": 210.27550000000005,
   "GR_gen": 75.80787043785479,
   "quad_doubling_rel": 4.1455727739503345e-13,
   "mean_vs_voigtiso_rel": 4.914657799565731e-15,
   "V_tot": 34838.280187494966,
   "V_tot_closed": 34838.28018749971,
   "V_tot_rel_resid": 1.362243651215067e-13,
   "Phi_G": 3.6673261098978673,
   "Phi_full": 0.05925533764358445,
   "pinned_46i_contractions": {
    "dc15_sq": 552.9885744047567,
    "dc25_sq": 276.4942872023802,
    "dc35_sq": 552.9885744047641,
    "dc45_sq": 276.49428720237916,
    "dc55_sq": 497.68971696437256,
    "dc56_sq": 276.49428720238024,
    "dc15dc25": -138.24714360119054,
    "dc15dc35": -414.7414308035703,
    "dc25dc35": -138.24714360119034
   },
   "nu": -170.38749999999996,
   "closed_basis_fit_resid": 2.062543879267168e-12,
   "abc_machine": [
    36.86590496028403,
    161.28833420138054,
    -46.08238120039523
   ],
   "a_vs_pinned_clean_string_rel": 9.064970996064403e-13,
   "bc_pinned_strings": "corrupted in transport -- not consumed (pin E3); machine values above",
   "cubic_collapse_rel": 1.4410694859634532e-13,
   "A_anchor_rel": 2.4986679392213773e-12
  }
 },
 "phase1b": {
  "step_hex": {
   "mu_bar": 73.06453333333334,
   "lam_bar": 85.89959999999999,
   "VT0": 8.54777943873924,
   "VL0": 15.23248721209595,
   "int_Phi_TT": 362.28448033744377,
   "int_Phi_TL": 241.57169884555444,
   "Q_T_a": 0.03519073886607002,
   "Q_T_TT_a": 0.033931769234873246,
   "Q_T_TL_a": 0.001258969631196774,
   "Q_L_a": 0.08363194915792597,
   "kTa_grid": [
    0.02,
    0.03,
    0.05,
    0.08,
    0.12
   ],
   "alpha_T_a": [
    5.621633954903736e-09,
    2.840350208527493e-08,
    2.1779108055025785e-07,
    1.4058711219314753e-06,
    6.904514358125577e-06
   ],
   "fit_exponent": 3.9908574393018728,
   "Q_ext_richardson": 0.03519054042696338,
   "Q_T_d": 0.0043988423582587526,
   "Qprime_G": 0.002592174543574817,
   "status": "FULL"
  },
  "gem8_hex": {
   "mu_bar": 105.04195333333332,
   "lam_bar": 159.66818666666666,
   "VT0": 10.248997674569612,
   "VL0": 19.22893895495363,
   "int_Phi_TT": 1073.0614422363049,
   "int_Phi_TL": 715.3892819892442,
   "Q_T_a": 0.05002054847853209,
   "Q_T_TT_a": 0.04862605263341434,
   "Q_T_TL_a": 0.0013944958451177474,
   "Q_L_a": 0.12513252572355138,
   "kTa_grid": [
    0.02,
    0.03,
    0.05,
    0.08,
    0.12
   ],
   "alpha_T_a": [
    7.990630478908698e-09,
    4.037275648361146e-08,
    3.09563901488677e-07,
    1.9982073003904e-06,
    9.812905455958456e-06
   ],
   "fit_exponent": 3.990836354736264,
   "Q_ext_richardson": 0.05002026549650163,
   "Q_T_d": 0.006252568559816511,
   "Qprime_G": 0.002571752332303918,
   "status": "FULL"
  },
  "step_cubic": {
   "mu_bar": 65.86612,
   "lam_bar": 79.92172000000002,
   "VT0": 8.11579447743719,
   "VL0": 14.548331863138124,
   "int_Phi_TT": 452.90304983805186,
   "int_Phi_TL": 301.9353665587016,
   "Q_T_a": 0.05407762824651864,
   "Q_T_TT_a": 0.05219766640218998,
   "Q_T_TL_a": 0.0018799618443286607,
   "Q_L_a": 0.12925237478415366,
   "kTa_grid": [
    0.02,
    0.03,
    0.05,
    0.08,
    0.12
   ],
   "alpha_T_a": [
    8.638764272946882e-09,
    4.3647636054023514e-08,
    3.3467889268689256e-07,
    2.1603940446971086e-06,
    1.06101603300242e-05
   ],
   "fit_exponent": 3.990855336260311,
   "Q_ext_richardson": 0.05407732172099957,
   "Q_T_d": 0.00675970353081483,
   "Qprime_G": 0.0025900405120530923,
   "status": "FULL",
   "eps_L": 0.04005953920846925,
   "eps_T": 0.09654538755183753
  },
  "gem8_cubic": {
   "mu_bar": 97.46610000000004,
   "lam_bar": 145.29809999999998,
   "VT0": 9.872492086601033,
   "VL0": 18.44533274300033,
   "int_Phi_TT": 1393.5312075000702,
   "int_Phi_TL": 929.020805000044,
   "Q_T_a": 0.07549430207120778,
   "Q_T_TT_a": 0.07334652219797161,
   "Q_T_TL_a": 0.0021477798732361655,
   "Q_L_a": 0.1880670060728289,
   "kTa_grid": [
    0.02,
    0.03,
    0.05,
    0.08,
    0.12
   ],
   "alpha_T_a": [
    1.205998859162398e-08,
    6.09332614078839e-08,
    4.672152484748498e-07,
    3.0158494253064023e-06,
    1.4810677454817654e-05
   ],
   "fit_exponent": 3.990838523014963,
   "Q_ext_richardson": 0.07549387273440293,
   "Q_T_d": 0.009436787758900972,
   "Qprime_G": 0.0025732066023339767,
   "status": "FULL",
   "eps_L": 0.04371345029832456,
   "eps_T": 0.11444471700186565
  }
 },
 "_meta": {
  "instrument": "poly1_fullprec_ccleg.py",
  "leg": "cc",
  "input_file": "poly_vrh_results.json",
  "input_md5": "200e7a8b775577564369c6924d38a84c",
  "pin_record_md5": "621120e50d395beea2e914d54c929600",
  "prereg_md5": "dab462d2e133d0962c512a34bb7bc635",
  "time": "2026-08-05 04:06:51.625310+00:00",
  "phase": "1-full"
 }
}
=====END-EMBED name=inputs/poly1_phase1full_cc.json=====

=====BEGIN-EMBED name=inputs/chatleg_phase0bfull.json md5=df413a7cfa30e599b779af8fee5d07d1 bytes=1920 encoding=raw=====
{
 "phase0b": {
  "step_cubic": {
   "K": 123.83246666666666,
   "mu_HS": [
    60.196098807662864,
    61.90468450314806
   ],
   "vT_HS": [
    7.758614490207827,
    7.867953005906178
   ],
   "vT_VR": [
    7.468877341686608,
    8.11579447743719
   ],
   "HS_halfwidth_pct": 0.7009736218327429,
   "VR_halfwidth_pct": 4.147411776869302,
   "status": "FULL"
  },
  "gem8_cubic": {
   "K": 210.2755,
   "mu_HS": [
    84.85580496763791,
    89.43210619958737
   ],
   "vT_HS": [
    9.211721064363484,
    9.456854984591196
   ],
   "vT_VR": [
    8.706771527831359,
    9.872492086601033
   ],
   "HS_halfwidth_pct": 1.31680585603757,
   "VR_halfwidth_pct": 6.261996123854931,
   "status": "FULL"
  },
  "step_hex": {
   "K_V": 134.6092888888889,
   "K_R_berryman": 134.61592608974317,
   "K_R_1606": 134.60823359539015,
   "K_HS": [
    134.61592608974317,
    134.60933811973788
   ],
   "K_band_note": "degenerate at input-identity-residual floor",
   "G_HS": "PENDING-verbatim (pin S2 elided term); VR shear bracket [68.6936, 73.0622]",
   "status": "K FULL; G PENDING"
  },
  "gem8_hex": {
   "K_V": 229.69615555555558,
   "K_R_berryman": 229.689087784171,
   "K_R_1606": 229.69594530872428,
   "K_HS": [
    229.69158236465034,
    229.69261752706808
   ],
   "K_band_note": "degenerate at input-identity-residual floor",
   "G_HS": "PENDING-verbatim (pin S2 elided term); VR shear bracket [96.6334, 105.0440]",
   "status": "K FULL; G PENDING"
  },
  "note_hex_G": "hex shear HS blocked on pin S2 completion (obligation before Phase 3)"
 },
 "_meta": {
  "instrument": "poly1_fullprec_chatleg.py",
  "leg": "chat",
  "input_file": "/mnt/user-data/uploads/poly_vrh_results.json",
  "input_md5": "200e7a8b775577564369c6924d38a84c",
  "pin_record_md5": "621120e50d395beea2e914d54c929600",
  "prereg_md5": "dab462d2e133d0962c512a34bb7bc635",
  "time": "2026-08-05 01:26:48.583364+00:00",
  "phase": "0b-full"
 }
}
=====END-EMBED name=inputs/chatleg_phase0bfull.json=====

=====BEGIN-EMBED name=g_mscs1_chatleg.py md5=db5f51dd9ef7f54dd0826991d594681b bytes=34606 encoding=base64 armor_bytes=46752 QUARANTINED=====
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJnX21zY3MxX2NoYXRsZWcucHkgLS0gR2F0ZSBHLU1T
Q1MxIGNoYXQtbGVnIGluc3RydW1lbnQsIHYxIChTZXB0ZW1iZXIgMTksIDIwMjYpLgoKRW5jb2Rl
cyB0aGUgTE9DS0VEIHN0YWdpbmcgbWVtbyB2MiAoM2YzMDI2MmUpIGFuZCBsb2NrIHJlY29yZCBB
ZGRlbmR1bSBBLTIuIE5vIG9ic2VydmF0aW9uYWwgbnVtYmVyLCBubyBTSQp1bml0LCBubyB0YXJn
ZXQgc3RyaW5nIGFwcGVhcnMgaGVyZTsgVDEgc2VsZi1ncmVwIChnYXRlIGxpc3QgZmVmMjgyNzEs
IGNvbnRleHR1YWwgbnVtZXJpYyBydWxlKSBydW5zIG9uIHRoaXMKZmlsZSwgdGhlIG1lbW8sIHRo
ZSBsaXN0IGFuZCBldmVyeSBjaGVja3BvaW50IGl0IHdyaXRlcywgYW5kIHRoZSBpbnN0cnVtZW50
IEhBTFRTIHdpdGhvdXQgdGhlIGxpc3QuCgpTdWJjb21tYW5kcwogIHNlbGZ0ZXN0ICAgZXhhY3Ru
ZXNzIGFuZCBpZGVudGl0eSBzdWl0ZXMgb24gc3ludGhldGljIGlucHV0cyAobm8gY2hlY2twb2lu
dCB3cml0dGVuKQogIHJ1biAgICAgICAgZ3VhcmRzIC0+IHBoYXNlMCBjb250cm9scyAoaGFsdCBv
biBmYWlsdXJlIC0+IElOREVURVJNSU5BVEUpIC0+IHBoYXNlMSAtPiBwaGFzZTIgLT4gY2hlY2tw
b2ludAogIGNvbXBhcmUgICAgTEFTVDogdGhlIHNlY3Rpb24tNiBoeXBvdGhlc2VzIGFnYWluc3Qg
dGhlIGNoZWNrcG9pbnQsIHdyaXR0ZW4gdG8gYSBzZXBhcmF0ZSBhcnRpZmFjdAoiIiIKaW1wb3J0
IGFyZ3BhcnNlLCBkYXRldGltZSwgaGFzaGxpYiwganNvbiwgbWF0aCwgb3MsIHN5cwppbXBvcnQg
bnVtcHkgYXMgbnAKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gbG9jayBwaW5zCk1FTU8gPSAnc3Rh
Z2luZ19tZW1vX0dfTVNDUzFfdjIubWQnOyAgIE1FTU9fTUQ1ID0gJzNmMzAyNjJlYWVjNDYxZmI1
ZmQzMjAyODM1ZjdkZTM3JzsgTUVNT19CWVRFUyA9IDM0ODM3ClQxTElTVCA9ICd0b29scy90MS9U
MV9mb3JiaWRkZW5fR19NU0NTMS50eHQnOyBUMV9NRDUgPSAnZmVmMjgyNzEwMGQzZjg1ZTBhNjM0
MWI0NGYwYzAwYmYnCkxFREdFUl9CQVNFX01ENSA9ICdkMDk1YTcwMDNiYjBkNGMxNzdlNzQ1MWUx
ZDE0YzRjNicKWDEgPSAnaW5wdXRzL3BvbHlfdnJoX3Jlc3VsdHMuanNvbic7ICAgWDFfTUQ1ID0g
JzIwMGU3YThiNzc1NTc3NTY0MzY5YzY5MjRkMzhhODRjJzsgWDFfQllURVMgPSAyNzY3ClgzID0g
J2lucHV0cy9jY19wMl9waGFzZTEuanNvbic7ICAgICAgIFgzX01ENSA9ICdhYWFlMjA2NzMzYjBm
MGEzNzhhNWM2YjYwMDI3NGQzZicKWDQgPSAnaW5wdXRzL3BvbHkxX3BoYXNlMWZ1bGxfY2MuanNv
bic7IFg0X01ENSA9ICdlYzg3ZTQyZjBmNjE3YjAwYzQ5ODViYTJhY2VhYzMzOScKWDUgPSAnaW5w
dXRzL2NoYXRsZWdfcGhhc2UwYmZ1bGwuanNvbic7IFg1X01ENSA9ICdkZjQxM2E3Y2ZhMzBlNTk5
Yjc3OWFmOGZlZTVkMDdkMScKRUxFQ1RJT05TID0geydFLU1TLTEnOiAnKGEpIHR3byBkZXNjcmlw
dG9ycyBvZiB0aGUgb25lIHRyYW5zdmVyc2UgZmllbGQ7IFMyLUUyIHByaW1hcnksIFMyLWggc2Vj
b25kIGFybScsCiAgICAgICAgICAgICAnRS1NUy0yJzogJyhhKSBhbGwgZm91ciBjb25maWd1cmF0
aW9ucycsICdFLU1TLTJiJzogJyhhK2IpIGJhbmtlZCB0ZXRyYWdvbmFsLWZvcm0gcHJpbWFyeTsg
c3ltbWV0cml6ZWQgQzY2IHNlY29uZCBhcm0nLAogICAgICAgICAgICAgJ0UtTVMtMmMnOiAnKDAw
MSsxMTEpIDwwMDE+IHByaW1hcnksIDwxMTE+IHJlcG9ydGVkJywgJ0UtTVMtMyc6ICcoYSkgVlJI
L0hTIGxlYWRpbmcgb3JkZXI7IEJvcm4gYXQgdCA9IDAgb25seTsgdGV4dHVyZSBzd2VlcCcsCiAg
ICAgICAgICAgICAnRS1NUy00JzogJyhhKSB0YWJsZSArIGxhbWJkYV9MJywgJ0UtTVMtNSc6ICco
YSkgZmliZXIgT0RGIDEgKyB0IFAyLCB0IGluIFstMSwgMl0nLCAnRS1NUy02JzogJyhhKSBubyBv
YnNlcnZhdGlvbmFsIGNvbnRhY3QnfQpUX0dSSUQgPSBbLTAuNSwgLTAuMjUsIC0wLjEsIC0wLjA1
LCAtMC4wMiwgMC4wLCAwLjAyLCAwLjA1LCAwLjEsIDAuMjUsIDAuNSwgMS4wXQpOX1RIRVRBLCBO
X1BISSwgRE9VQkxJTkdfVE9MID0gNjQsIDEyOCwgMWUtMTAKVEFVID0gMWUtNgpDT05GSUdTID0g
eydoZXhfc3RlcCc6ICgnaGV4JywgJ2hleDpzdGVwJyksICdoZXhfZ2VtOCc6ICgnaGV4JywgJ2hl
eDpnZW04JyksICdjdWJpY19zdGVwJzogKCdjdWJpYycsICdjdWJpYzpzdGVwJyksICdjdWJpY19n
ZW04JzogKCdjdWJpYycsICdjdWJpYzpnZW04Jyl9CkJBTktfS0VZID0geydoZXhfc3RlcCc6ICdz
dGVwX2hleCcsICdoZXhfZ2VtOCc6ICdnZW04X2hleCcsICdjdWJpY19zdGVwJzogJ3N0ZXBfY3Vi
aWMnLCAnY3ViaWNfZ2VtOCc6ICdnZW04X2N1YmljJ30KQ0hFQ0tQT0lOVCA9ICdnX21zY3MxX2No
YXRsZWdfY2hlY2twb2ludC5qc29uJzsgQ09NUEFSRSA9ICdnX21zY3MxX2NoYXRsZWdfY29tcGFy
ZS5qc29uJwpaID0gbnAuYXJyYXkoWzAuMCwgMC4wLCAxLjBdKTsgQVgxMTEgPSBucC5hcnJheShb
MS4wLCAxLjAsIDEuMF0pIC8gbWF0aC5zcXJ0KDMuMCkKCmRlZiBtZDViKGIpOiByZXR1cm4gaGFz
aGxpYi5tZDUoYikuaGV4ZGlnZXN0KCkKZGVmIG1kNWYocCk6IHJldHVybiBtZDViKG9wZW4ocCwg
J3JiJykucmVhZCgpKQoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBUMSAoaW5saW5lIGNvcHkgb2Yg
dDFfc2Nhbi5weSBydWxlcykKTlVNQ0hBUlMgPSBzZXQoIjAxMjM0NTY3ODkuZUUrLcOXXiDigbvi
gbDCucKywrPigbTigbXigbbigbfigbjigbkiKQpkZWYgdDFfbG9hZChwKToKICAgIHJldHVybiBb
bC5yc3RyaXAoJ1xuJykgZm9yIGwgaW4gb3BlbihwLCBlbmNvZGluZz0ndXRmLTgnKSBpZiBsLnN0
cmlwKCkgYW5kIG5vdCBsLnN0YXJ0c3dpdGgoJyMnKV0KZGVmIHQxX3NjYW5fdGV4dCh0ZXh0LCBw
YXRzKToKICAgIGhpdHMsIGNvbGwgPSBbXSwgW10KICAgIGZvciBpLCBwIGluIGVudW1lcmF0ZShw
YXRzKToKICAgICAgICBudW1lcmljID0gYWxsKGMgaW4gTlVNQ0hBUlMgZm9yIGMgaW4gcCk7IHN0
YXJ0ID0gMAogICAgICAgIHdoaWxlIFRydWU6CiAgICAgICAgICAgIGogPSB0ZXh0LmZpbmQocCwg
c3RhcnQpCiAgICAgICAgICAgIGlmIGogPCAwOiBicmVhawogICAgICAgICAgICBpZiBudW1lcmlj
OgogICAgICAgICAgICAgICAgYSA9IGoKICAgICAgICAgICAgICAgIHdoaWxlIGEgPiAwIGFuZCB0
ZXh0W2EtMV0gaW4gTlVNQ0hBUlMgYW5kIHRleHRbYS0xXSAhPSAnICc6IGEgLT0gMQogICAgICAg
ICAgICAgICAgYiA9IGogKyBsZW4ocCkKICAgICAgICAgICAgICAgIHdoaWxlIGIgPCBsZW4odGV4
dCkgYW5kIHRleHRbYl0gaW4gTlVNQ0hBUlMgYW5kIHRleHRbYl0gIT0gJyAnOiBiICs9IDEKICAg
ICAgICAgICAgICAgIChoaXRzIGlmIHRleHRbYTpiXSA9PSBwIGVsc2UgY29sbCkuYXBwZW5kKGkp
CiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBoaXRzLmFwcGVuZChpKQogICAgICAg
ICAgICBzdGFydCA9IGogKyAxCiAgICByZXR1cm4gaGl0cywgY29sbApkZWYgdDFfZ2F0ZShwYXRo
cyk6CiAgICBpZiBub3Qgb3MucGF0aC5leGlzdHMoVDFMSVNUKTogc3lzLmV4aXQoJ0hBTFQ6IFQx
IGdhdGUgbGlzdCBhYnNlbnQgLS0gdGhpcyBnYXRlIGhhcyBubyBMSVNUX0FCU0VOVCBwYXRoJykK
ICAgIGlmIG1kNWYoVDFMSVNUKSAhPSBUMV9NRDU6IHN5cy5leGl0KCdIQUxUOiBUMSBnYXRlIGxp
c3QgbWQ1ICE9IGxvY2snKQogICAgcGF0cyA9IHQxX2xvYWQoVDFMSVNUKTsgbmNvbGwgPSAwCiAg
ICBmb3IgcCBpbiBwYXRoczoKICAgICAgICBoLCBjID0gdDFfc2Nhbl90ZXh0KG9wZW4ocCwgJ3Ji
JykucmVhZCgpLmRlY29kZSgndXRmLTgnLCAncmVwbGFjZScpLCBwYXRzKTsgbmNvbGwgKz0gbGVu
KGMpCiAgICAgICAgaWYgaDogc3lzLmV4aXQoZidIQUxUOiBUMSBISVQgaW4ge3B9OiBwYXR0ZXJu
IGluZGljZXMge3NvcnRlZChzZXQoaCkpfScpCiAgICByZXR1cm4geydsaXN0X21kNSc6IFQxX01E
NSwgJ3N0YXRlJzogJ0NMRUFOJywgJ251bWVyaWNfY29sbGlzaW9ucyc6IG5jb2xsLCAnZmlsZXMn
OiBbb3MucGF0aC5iYXNlbmFtZShwKSBmb3IgcCBpbiBwYXRoc119CgojIC0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tIHRlbnNvcnMKVk9JR1QgPSBbKDAsIDApLCAoMSwgMSksICgyLCAyKSwgKDEsIDIpLCAo
MCwgMiksICgwLCAxKV0KZGVmIGM0X2Zyb21fY29uc3RhbnRzKHN5bSwgYywgc3ltbWV0cml6ZV9o
ZXg9RmFsc2UpOgogICAgTSA9IG5wLnplcm9zKCg2LCA2KSkKICAgIGlmIHN5bSA9PSAnaGV4JzoK
ICAgICAgICBDMTEsIEMxMiwgQzEzLCBDMzMsIEM0NCA9IChjW2tdIGZvciBrIGluICgnQzExJywg
J0MxMicsICdDMTMnLCAnQzMzJywgJ0M0NCcpKQogICAgICAgIEM2NiA9IDAuNSAqIChDMTEgLSBD
MTIpIGlmIHN5bW1ldHJpemVfaGV4IGVsc2UgY1snQzY2J10KICAgICAgICBNWzozLCA6M10gPSBb
W0MxMSwgQzEyLCBDMTNdLCBbQzEyLCBDMTEsIEMxM10sIFtDMTMsIEMxMywgQzMzXV07IE1bMywg
M10gPSBNWzQsIDRdID0gQzQ0OyBNWzUsIDVdID0gQzY2CiAgICBlbHNlOgogICAgICAgIEMxMSwg
QzEyLCBDNDQgPSBjWydDMTEnXSwgY1snQzEyJ10sIGNbJ0M0NCddCiAgICAgICAgTVs6MywgOjNd
ID0gW1tDMTEsIEMxMiwgQzEyXSwgW0MxMiwgQzExLCBDMTJdLCBbQzEyLCBDMTIsIEMxMV1dOyBN
WzMsIDNdID0gTVs0LCA0XSA9IE1bNSwgNV0gPSBDNDQKICAgIHJldHVybiB2b2lndDY2X3RvX2M0
KE0pCmRlZiB2b2lndDY2X3RvX2M0KE0pOgogICAgVCA9IG5wLnplcm9zKCgzLCAzLCAzLCAzKSkK
ICAgIGZvciBJLCAoaSwgaikgaW4gZW51bWVyYXRlKFZPSUdUKToKICAgICAgICBmb3IgSiwgKGss
IGwpIGluIGVudW1lcmF0ZShWT0lHVCk6CiAgICAgICAgICAgIGZvciBhLCBiIGluICgoaSwgaiks
IChqLCBpKSk6CiAgICAgICAgICAgICAgICBmb3IgY2MsIGQgaW4gKChrLCBsKSwgKGwsIGspKToK
ICAgICAgICAgICAgICAgICAgICBUW2EsIGIsIGNjLCBkXSA9IE1bSSwgSl0KICAgIHJldHVybiBU
Cl9NRiA9IG5wLmFycmF5KFsxLCAxLCAxLCBtYXRoLnNxcnQoMiksIG1hdGguc3FydCgyKSwgbWF0
aC5zcXJ0KDIpXSkKZGVmIGM0X3RvX21hbmRlbChUKToKICAgIE0gPSBucC56ZXJvcygoNiwgNikp
CiAgICBmb3IgSSwgKGksIGopIGluIGVudW1lcmF0ZShWT0lHVCk6CiAgICAgICAgZm9yIEosIChr
LCBsKSBpbiBlbnVtZXJhdGUoVk9JR1QpOgogICAgICAgICAgICBNW0ksIEpdID0gVFtpLCBqLCBr
LCBsXSAqIF9NRltJXSAqIF9NRltKXQogICAgcmV0dXJuIE0KZGVmIG1hbmRlbF90b19jNChNKToK
ICAgIHJldHVybiB2b2lndDY2X3RvX2M0KE0gLyBucC5vdXRlcihfTUYsIF9NRikpCkU2ID0gbnAu
YXJyYXkoWzEuMCwgMSwgMSwgMCwgMCwgMF0pOyBKNiA9IG5wLm91dGVyKEU2LCBFNikgLyAzLjA7
IEs2ID0gbnAuZXllKDYpIC0gSjYKZGVmIGlzb19tYW5kZWwoSywgRyk6IHJldHVybiAzICogSyAq
IEo2ICsgMiAqIEcgKiBLNgpkZWYgaXNvX0tHX29mX2M0KFQpOgogICAgSyA9IG5wLmVpbnN1bSgn
aWlqai0+JywgVCkgLyA5LjAKICAgIEcgPSAobnAuZWluc3VtKCdpamlqLT4nLCBUKSAtIG5wLmVp
bnN1bSgnaWlqai0+JywgVCkgLyAzLjApIC8gMTAuMAogICAgcmV0dXJuIEssIEcKCiMgLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0gU08oMykgcHJvZHVjdCBxdWFkcmF0dXJlCmRlZiBzbzNfZ3JpZChuYSwg
bmIsIG5nKToKICAgIGFsID0gMiAqIG5wLnBpICogbnAuYXJhbmdlKG5hKSAvIG5hOyBnYSA9IDIg
KiBucC5waSAqIG5wLmFyYW5nZShuZykgLyBuZwogICAgeGIsIHdiID0gbnAucG9seW5vbWlhbC5s
ZWdlbmRyZS5sZWdnYXVzcyhuYik7IHNiID0gbnAuc3FydCgxIC0geGIqKjIpCiAgICBScywgd3Mg
PSBbXSwgW10KICAgIGZvciBhIGluIGFsOgogICAgICAgIFJhID0gbnAuYXJyYXkoW1ttYXRoLmNv
cyhhKSwgLW1hdGguc2luKGEpLCAwXSwgW21hdGguc2luKGEpLCBtYXRoLmNvcyhhKSwgMF0sIFsw
LCAwLCAxXV0pCiAgICAgICAgZm9yIGliIGluIHJhbmdlKG5iKToKICAgICAgICAgICAgUmIgPSBu
cC5hcnJheShbW3hiW2liXSwgMCwgc2JbaWJdXSwgWzAsIDEsIDBdLCBbLXNiW2liXSwgMCwgeGJb
aWJdXV0pCiAgICAgICAgICAgIGZvciBnIGluIGdhOgogICAgICAgICAgICAgICAgUmcgPSBucC5h
cnJheShbW21hdGguY29zKGcpLCAtbWF0aC5zaW4oZyksIDBdLCBbbWF0aC5zaW4oZyksIG1hdGgu
Y29zKGcpLCAwXSwgWzAsIDAsIDFdXSkKICAgICAgICAgICAgICAgIFJzLmFwcGVuZChSYSBAIFJi
IEAgUmcpOyB3cy5hcHBlbmQod2JbaWJdIC8gKDIuMCAqIG5hICogbmcpKQogICAgcmV0dXJuIG5w
LmFycmF5KFJzKSwgbnAuYXJyYXkod3MpClNPMyA9IHNvM19ncmlkKDE2LCAxMCwgMTYpCmRlZiBy
b3RhdGVfYWxsKGM0LCBScyk6CiAgICB0ID0gbnAuZWluc3VtKCdnaWEsYWJjZC0+Z2liY2QnLCBS
cywgYzQsIG9wdGltaXplPVRydWUpOyB0ID0gbnAuZWluc3VtKCdnamIsZ2liY2QtPmdpamNkJywg
UnMsIHQsIG9wdGltaXplPVRydWUpCiAgICB0ID0gbnAuZWluc3VtKCdna2MsZ2lqY2QtPmdpamtk
JywgUnMsIHQsIG9wdGltaXplPVRydWUpOyByZXR1cm4gbnAuZWluc3VtKCdnbGQsZ2lqa2QtPmdp
amtsJywgUnMsIHQsIG9wdGltaXplPVRydWUpCmRlZiBQMih4KTogcmV0dXJuIDAuNSAqICgzICog
eCAqIHggLSAxKQpkZWYgb2RmX3dlaWdodHModCwgYXhpc19jLCBScywgd3MpOgogICAgbnogPSBS
cyBAIGF4aXNfYzsgcmV0dXJuIHdzICogKDEuMCArIHQgKiBQMihuels6LCAyXSkpICAgICAgICAg
ICMgZmliZXIgYXhpcyA9IGxhYiB6CmRlZiBvZGZfYXZnX2M0KGM0LCB0LCBheGlzX2MpOgogICAg
UnMsIHdzID0gU08zOyB3ID0gb2RmX3dlaWdodHModCwgYXhpc19jLCBScywgd3MpCiAgICByZXR1
cm4gbnAuZWluc3VtKCdnLGdpamtsLT5pamtsJywgdywgcm90YXRlX2FsbChjNCwgUnMpLCBvcHRp
bWl6ZT1UcnVlKQoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBhZ2dyZWdhdGUgc2NoZW1lcwpkZWYg
YWdncmVnYXRlX3RlbnNvcnMoYzQsIHQsIGF4aXNfYywgaHNfcmVmKToKICAgICIiIlZvaWd0LCBS
ZXVzcywgSGlsbCwgSFMobG8sIGhpLCBtZWFuKSA0LXRlbnNvcnMgb2YgdGhlIHRleHR1cmVkIGFn
Z3JlZ2F0ZS4iIiIKICAgIENWID0gb2RmX2F2Z19jNChjNCwgdCwgYXhpc19jKQogICAgUzQgPSBt
YW5kZWxfdG9fYzQobnAubGluYWxnLmludihjNF90b19tYW5kZWwoYzQpKSkKICAgIENSID0gbWFu
ZGVsX3RvX2M0KG5wLmxpbmFsZy5pbnYoYzRfdG9fbWFuZGVsKG9kZl9hdmdfYzQoUzQsIHQsIGF4
aXNfYykpKSkKICAgIENIID0gMC41ICogKENWICsgQ1IpCiAgICBvdXQgPSB7J1YnOiBDViwgJ1In
OiBDUiwgJ0gnOiBDSH0KICAgIGlmIGhzX3JlZiBpcyBub3QgTm9uZToKICAgICAgICBocyA9IHt9
CiAgICAgICAgZm9yIHRhZywgKEswLCBHMCkgaW4gaHNfcmVmLml0ZW1zKCk6CiAgICAgICAgICAg
IENzID0gY3N0YXIoSzAsIEcwKQogICAgICAgICAgICBpbnYgPSBtYW5kZWxfdG9fYzQobnAubGlu
YWxnLmludihjNF90b19tYW5kZWwoYzQpICsgQ3MpKQogICAgICAgICAgICBoc1t0YWddID0gbWFu
ZGVsX3RvX2M0KG5wLmxpbmFsZy5pbnYoYzRfdG9fbWFuZGVsKG9kZl9hdmdfYzQoaW52LCB0LCBh
eGlzX2MpKSkgLSBDcykKICAgICAgICBvdXRbJ0hTbG8nXSwgb3V0WydIU2hpJ10gPSBoc1snbG8n
XSwgaHNbJ2hpJ107IG91dFsnSFMnXSA9IDAuNSAqIChoc1snbG8nXSArIGhzWydoaSddKQogICAg
cmV0dXJuIG91dApkZWYgY3N0YXIoSzAsIEcwKToKICAgIEtzID0gNC4wICogRzAgLyAzLjA7IEdz
ID0gRzAgKiAoOSAqIEswICsgOCAqIEcwKSAvICg2LjAgKiAoSzAgKyAyICogRzApKTsgcmV0dXJu
IGlzb19tYW5kZWwoS3MsIEdzKQpkZWYgaHNfaXNvX2JvdW5kKGM0LCBLMCwgRzApOgogICAgQ3Mg
PSBjc3RhcihLMCwgRzApOyBpbnYgPSBtYW5kZWxfdG9fYzQobnAubGluYWxnLmludihjNF90b19t
YW5kZWwoYzQpICsgQ3MpKQogICAgQyA9IG1hbmRlbF90b19jNChucC5saW5hbGcuaW52KGM0X3Rv
X21hbmRlbChvZGZfYXZnX2M0KGludiwgMC4wLCBaKSkpIC0gQ3MpCiAgICByZXR1cm4gaXNvX0tH
X29mX2M0KEMpCmRlZiBmZWFzaWJsZShjNCwgSzAsIEcwLCB1cHBlcik6CiAgICBEID0gaXNvX21h
bmRlbChLMCwgRzApIC0gYzRfdG9fbWFuZGVsKGM0KQogICAgbGFtID0gbnAubGluYWxnLmVpZ3Zh
bHNoKEQpOyBzY2FsZSA9IG5wLmFicyhjNF90b19tYW5kZWwoYzQpKS5tYXgoKQogICAgcmV0dXJu
IChsYW0ubWluKCkgPj0gLTFlLTExICogc2NhbGUpIGlmIHVwcGVyIGVsc2UgKGxhbS5tYXgoKSA8
PSAxZS0xMSAqIHNjYWxlKQpkZWYgb3B0aW1pemVfaHNfcmVmZXJlbmNlKGM0KToKICAgICIiIlJl
dHVybiB7J2xvJzogKEswLEcwKSwgJ2hpJzogKEswLEcwKX06IHRoZSBpc290cm9waWMgcmVmZXJl
bmNlcyBnaXZpbmcgdGhlIHRpZ2h0ZXN0IFdhbHBvbGUgYm91bmRzIGF0IHQgPSAwCiAgICAodXBw
ZXI6IG1pbmltYWwgZmVhc2libGUgbWFqb3JhbnQsIHNtYWxsZXN0IGJvdW5kOyBsb3dlcjogbWF4
aW1hbCBmZWFzaWJsZSBtaW5vcmFudCwgbGFyZ2VzdCBib3VuZCkuCiAgICBHcmlkIHNjYW4gb3Zl
ciBHMCB3aXRoIHRoZSBleHRyZW1hbCBmZWFzaWJsZSBLMCBieSBiaXNlY3Rpb24sIHRoZW4gZ29s
ZGVuLXNlY3Rpb24gcmVmaW5lbWVudCBvbiB0aGUgZmVhc2libGUKICAgIGJyYWNrZXQ7IHRoZSBi
ZXN0IGV2YWx1YXRlZCBwb2ludCBpcyByZXR1cm5lZCAobmV2ZXIgYW4gaW5mZWFzaWJsZSBvbmUp
LiIiIgogICAgS3YsIEd2ID0gaXNvX0tHX29mX2M0KGM0KTsgcmVmcyA9IHt9CiAgICBmb3IgdXBw
ZXIgaW4gKFRydWUsIEZhbHNlKToKICAgICAgICBkZWYgS19hdChHMCk6CiAgICAgICAgICAgIGxv
LCBoaSA9IDAuMCwgNTAuMCAqIEt2CiAgICAgICAgICAgIGlmIG5vdCAoZmVhc2libGUoYzQsIGhp
LCBHMCwgVHJ1ZSkgaWYgdXBwZXIgZWxzZSBmZWFzaWJsZShjNCwgbG8sIEcwLCBGYWxzZSkpOiBy
ZXR1cm4gTm9uZQogICAgICAgICAgICBmb3IgXyBpbiByYW5nZSg4MCk6CiAgICAgICAgICAgICAg
ICBtaWQgPSAwLjUgKiAobG8gKyBoaSkKICAgICAgICAgICAgICAgIG9rID0gZmVhc2libGUoYzQs
IG1pZCwgRzAsIHVwcGVyKQogICAgICAgICAgICAgICAgaWYgdXBwZXI6IGhpLCBsbyA9IChtaWQs
IGxvKSBpZiBvayBlbHNlIChoaSwgbWlkKQogICAgICAgICAgICAgICAgZWxzZTogICAgIGxvLCBo
aSA9IChtaWQsIGhpKSBpZiBvayBlbHNlIChsbywgbWlkKQogICAgICAgICAgICByZXR1cm4gaGkg
aWYgdXBwZXIgZWxzZSBsbwogICAgICAgIGV2YWxzID0ge30KICAgICAgICBkZWYgZihHMCk6CiAg
ICAgICAgICAgIGlmIEcwIGluIGV2YWxzOiByZXR1cm4gZXZhbHNbRzBdWzBdCiAgICAgICAgICAg
IEswID0gS19hdChHMCkKICAgICAgICAgICAgdmFsID0gMWUzMDAgaWYgSzAgaXMgTm9uZSBlbHNl
IChoc19pc29fYm91bmQoYzQsIEswLCBHMClbMV0gKiAoMSBpZiB1cHBlciBlbHNlIC0xKSkgICAj
IGluZmVhc2libGUgaXMgYWx3YXlzIHdvcnN0CiAgICAgICAgICAgIGV2YWxzW0cwXSA9ICh2YWws
IEswKTsgcmV0dXJuIHZhbAogICAgICAgIGdyaWQgPSBucC5saW5zcGFjZSgwLjIgKiBHdiwgNC4w
ICogR3YsIDE2MCkKICAgICAgICBmb3IgRzAgaW4gZ3JpZDogZihmbG9hdChHMCkpCiAgICAgICAg
ZmVhcyA9IFtHMCBmb3IgRzAgaW4gZXZhbHMgaWYgZXZhbHNbRzBdWzFdIGlzIG5vdCBOb25lXQog
ICAgICAgIGJlc3QgPSBtaW4oZmVhcywga2V5PWxhbWJkYSBHMDogZXZhbHNbRzBdWzBdKQogICAg
ICAgIGkgPSBsaXN0KGdyaWQpLmluZGV4KG1pbihncmlkLCBrZXk9bGFtYmRhIHg6IGFicyh4IC0g
YmVzdCkpKQogICAgICAgIGEsIGIgPSBmbG9hdChncmlkW21heChpIC0gMSwgMCldKSwgZmxvYXQo
Z3JpZFttaW4oaSArIDEsIGxlbihncmlkKSAtIDEpXSk7IHBoaSA9IChtYXRoLnNxcnQoNSkgLSAx
KSAvIDIKICAgICAgICB4MSwgeDIgPSBiIC0gcGhpICogKGIgLSBhKSwgYSArIHBoaSAqIChiIC0g
YSkKICAgICAgICBmb3IgXyBpbiByYW5nZSg3MCk6CiAgICAgICAgICAgIGlmIGYoeDEpIDwgZih4
Mik6IGIsIHgyID0geDIsIHgxOyB4MSA9IGIgLSBwaGkgKiAoYiAtIGEpCiAgICAgICAgICAgIGVs
c2U6IGEsIHgxID0geDEsIHgyOyB4MiA9IGEgKyBwaGkgKiAoYiAtIGEpCiAgICAgICAgZmVhcyA9
IFtHMCBmb3IgRzAgaW4gZXZhbHMgaWYgZXZhbHNbRzBdWzFdIGlzIG5vdCBOb25lXQogICAgICAg
IGJlc3QgPSBtaW4oZmVhcywga2V5PWxhbWJkYSBHMDogZXZhbHNbRzBdWzBdKQogICAgICAgIHJl
ZnNbJ2hpJyBpZiB1cHBlciBlbHNlICdsbyddID0gKGZsb2F0KGV2YWxzW2Jlc3RdWzFdKSwgZmxv
YXQoYmVzdCkpCiAgICByZXR1cm4gcmVmcwoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBzcGhlcmUg
cXVhZHJhdHVyZSArIENocmlzdG9mZmVsCmRlZiBzcGhlcmVfZ3JpZChudCwgbnBoaSk6CiAgICB4
LCB3ID0gbnAucG9seW5vbWlhbC5sZWdlbmRyZS5sZWdnYXVzcyhudCk7IHBoID0gMiAqIG5wLnBp
ICogbnAuYXJhbmdlKG5waGkpIC8gbnBoaQogICAgY3QsIGNwID0gbnAubWVzaGdyaWQoeCwgbnAu
Y29zKHBoKSwgaW5kZXhpbmc9J2lqJyk7IHN0ID0gbnAuc3FydCgxIC0gY3QqKjIpOyBzcCA9IG5w
LnNpbihucC5tZXNoZ3JpZCh4LCBwaCwgaW5kZXhpbmc9J2lqJylbMV0pCiAgICBLID0gbnAuc3Rh
Y2soW3N0ICogY3AsIHN0ICogc3AsIGN0XSwgLTEpLnJlc2hhcGUoLTEsIDMpOyBXID0gKG5wLnJl
cGVhdCh3LCBucGhpKSAvICgyLjAgKiBucGhpKSkKICAgIHJldHVybiBLLCBXICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAjIHdlaWdodHMgc3VtIHRv
IDEKZGVmIG1vZGVzKGM0LCBLKToKICAgIEcgPSBucC5laW5zdW0oJ2lqa2wsbmosbmwtPm5paycs
IGM0LCBLLCBLLCBvcHRpbWl6ZT1UcnVlKTsgdmFsLCB2ZWMgPSBucC5saW5hbGcuZWlnaChHKQog
ICAgcmV0dXJuIG5wLnNxcnQobnAubWF4aW11bSh2YWwsIDAuMCkpLCBucC50cmFuc3Bvc2UodmVj
LCAoMCwgMiwgMSkpICAgIyB2W24sYl0sIGVbbixiLDNdCmRlZiBkZXNjcmlwdG9ycyhLLCBlKToK
ICAgICIiIlBlciBtb2RlOiBsYW1iZGEsIHdfRU0sIFNfcGVycCAobixiLDMsMyksIHdfUzJoLiIi
IgogICAga2UgPSBucC5laW5zdW0oJ25pLG5iaS0+bmInLCBLLCBlKTsgbGFtID0ga2UqKjI7IHdf
ZW0gPSAxLjAgLSBsYW0KICAgIGVwZXJwID0gZSAtIGtlWy4uLiwgTm9uZV0gKiBLWzosIE5vbmUs
IDpdCiAgICBTcCA9IDAuNSAqIChucC5laW5zdW0oJ25pLG5iai0+bmJpaicsIEssIGVwZXJwKSAr
IG5wLmVpbnN1bSgnbmJpLG5qLT5uYmlqJywgZXBlcnAsIEspKQogICAgd19oID0gKDEuMCAtIGxh
bSkgLyAoMS4wICsgbGFtIC8gMy4wKQogICAgIyBnZW5lcmFsIG09Ky0xIGZyYWN0aW9uIGFib3V0
IGsgb2YgdGhlIGZ1bGwgdHJhY2VsZXNzIHN0cmFpbiAoYXNzZXJ0ZWQgZXF1YWwgdG8gdGhlIGNs
b3NlZCBmb3JtKQogICAgUyA9IDAuNSAqIChucC5laW5zdW0oJ25pLG5iai0+bmJpaicsIEssIGUp
ICsgbnAuZWluc3VtKCduYmksbmotPm5iaWonLCBlLCBLKSk7IFN0ID0gUyAtIChrZSAvIDMuMClb
Li4uLCBOb25lLCBOb25lXSAqIG5wLmV5ZSgzKQogICAgU2sgPSBucC5laW5zdW0oJ25iaWosbmot
Pm5iaScsIFN0LCBLKTsga1NrID0gbnAuZWluc3VtKCduaSxuYmktPm5iJywgSywgU2spOyBtMSA9
IDIuMCAqIChucC5laW5zdW0oJ25iaSxuYmktPm5iJywgU2ssIFNrKSAtIGtTayoqMikKICAgIG5v
cm0gPSBucC5laW5zdW0oJ25iaWosbmJpai0+bmInLCBTdCwgU3QpOyB3X2hfZ2VuID0gbTEgLyBu
b3JtCiAgICByZXR1cm4gbGFtLCB3X2VtLCBTcCwgd19oLCB3X2hfZ2VuCmRlZiBmcmFjX0UyKFNw
LCBuKToKICAgICIiIm09Ky0yIGZyYWN0aW9uIG9mIHRyYWNlbGVzcyBzeW1tZXRyaWMgUyAoLi4u
LDMsMykgYWJvdXQgdW5pdCBheGVzIG4gKG0sMykgLT4gKC4uLiwgbSkuIiIiCiAgICBTbiA9IG5w
LmVpbnN1bSgnLi4uaWosbWotPi4uLm1pJywgU3AsIG4pOyBuU24gPSBucC5laW5zdW0oJy4uLm1p
LG1pLT4uLi5tJywgU24sIG4pOyBTbjIgPSBucC5laW5zdW0oJy4uLm1pLC4uLm1pLT4uLi5tJywg
U24sIFNuKQogICAgbm9ybSA9IG5wLmVpbnN1bSgnLi4uaWosLi4uaWotPi4uLicsIFNwLCBTcClb
Li4uLCBOb25lXQogICAgd2l0aCBucC5lcnJzdGF0ZShkaXZpZGU9J2lnbm9yZScsIGludmFsaWQ9
J2lnbm9yZScpOgogICAgICAgIGYgPSAxLjAgLSAyLjAgKiBTbjIgLyBub3JtICsgMC41ICogblNu
KioyIC8gbm9ybQogICAgcmV0dXJuIG5wLndoZXJlKG5vcm0gPiAxZS0zMDAsIGYsIDAuMCkKTkdS
SUQgPSBzcGhlcmVfZ3JpZCgxMiwgMjQpICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgIyBleGFjdCBmb3IgZGVncmVlLTYgaW50ZWdyYW5kcyBpbiBuCmRlZiBvZGZfYXZn
X2ZyYWNFMihTcCwgdCk6CiAgICBuLCB3biA9IE5HUklEOyBmID0gZnJhY19FMihTcCwgbik7IHcg
PSB3biAqICgxLjAgKyB0ICogUDIobls6LCAyXSkpCiAgICByZXR1cm4gbnAuZWluc3VtKCcuLi5t
LG0tPi4uLicsIGYsIHcpCmRlZiBsYWJlbF9icmFuY2hlcyhzeW0sIEssIGUsIGxhbSwgdik6CiAg
ICAiIiJSZXR1cm4gYXJyYXkgb2YgbGFiZWxzIChuLGIpIGFzIHNtYWxsIGludHM6IGhleCAwPXFT
SCAxPXFTViAyPXFMOyBjdWJpYyAwPXFUMSAxPXFUMiAyPXFMLiIiIgogICAgbmsgPSBLLnNoYXBl
WzBdOyBsYWIgPSBucC5mdWxsKChuaywgMyksIC0xLCBkdHlwZT1pbnQpOyBpTCA9IG5wLmFyZ21h
eChsYW0sIGF4aXM9MSkKICAgIGlmIHN5bSA9PSAnaGV4JzoKICAgICAgICB6ayA9IG5wLmNyb3Nz
KG5wLmJyb2FkY2FzdF90byhaLCBLLnNoYXBlKSwgSyk7IG5ybSA9IG5wLmxpbmFsZy5ub3JtKHpr
LCBheGlzPTEpOyB6ayA9IHprIC8gbnAud2hlcmUobnJtID4gMCwgbnJtLCAxKVs6LCBOb25lXQog
ICAgICAgIG92ID0gbnAuYWJzKG5wLmVpbnN1bSgnbmJpLG5pLT5uYicsIGUsIHprKSk7IGlTSCA9
IG5wLmFyZ21heChvdiwgYXhpcz0xKQogICAgICAgIGZvciBuIGluIHJhbmdlKG5rKToKICAgICAg
ICAgICAgcmVzdCA9IFtiIGZvciBiIGluIHJhbmdlKDMpIGlmIGIgIT0gaVNIW25dXTsgbCA9IHJl
c3RbaW50KG5wLmFyZ21heChsYW1bbiwgcmVzdF0pKV07IHMgPSBbYiBmb3IgYiBpbiByZXN0IGlm
IGIgIT0gbF1bMF0KICAgICAgICAgICAgbGFiW24sIGlTSFtuXV0gPSAwOyBsYWJbbiwgc10gPSAx
OyBsYWJbbiwgbF0gPSAyCiAgICBlbHNlOgogICAgICAgIGZvciBuIGluIHJhbmdlKG5rKToKICAg
ICAgICAgICAgcmVzdCA9IFtiIGZvciBiIGluIHJhbmdlKDMpIGlmIGIgIT0gaUxbbl1dOyBmLCBz
ID0gKHJlc3QgaWYgdltuLCByZXN0WzBdXSA+PSB2W24sIHJlc3RbMV1dIGVsc2UgcmVzdFs6Oi0x
XSkKICAgICAgICAgICAgbGFiW24sIGZdID0gMDsgbGFiW24sIHNdID0gMTsgbGFiW24sIGlMW25d
XSA9IDIKICAgIHJldHVybiBsYWIKTEFCRUxTID0geydoZXgnOiBbJ3FTSCcsICdxU1YnLCAncUwn
XSwgJ2N1YmljJzogWydxVDEnLCAncVQyJywgJ3FMJ119CgpkZWYgc3BlY2llc19zdGF0cyhzeW0s
IGM0LCBheGlzX2MsIEssIFcsIHQ9Tm9uZSwgaGV4X2N1YmljX2F4aXNfbGFiPU5vbmUpOgogICAg
IiIiU2luZ2xlIGNyeXN0YWwgKHQgTm9uZSk6IFMyLUUyIGFib3V0IHRoZSBmaXhlZCBsYWIgYXhp
czsgYWdncmVnYXRlICh0IGdpdmVuKTogT0RGLWF2ZXJhZ2VkIHdlaWdodC4iIiIKICAgIHYsIGUg
PSBtb2RlcyhjNCwgSyk7IGxhbSwgd19lbSwgU3AsIHdfaCwgd19oX2dlbiA9IGRlc2NyaXB0b3Jz
KEssIGUpCiAgICBhc3NlcnQgbnAubWF4KG5wLmFicyh3X2ggLSB3X2hfZ2VuKSkgPCAxZS0xMCwg
J1MyLWggY2xvc2VkIGZvcm0gdnMgZ2VuZXJhbCBtPSstMSBmcmFjdGlvbicKICAgIGlmIHQgaXMg
Tm9uZToKICAgICAgICBmID0gZnJhY19FMihTcCwgaGV4X2N1YmljX2F4aXNfbGFiW05vbmUsIDpd
KVsuLi4sIDBdCiAgICBlbHNlOgogICAgICAgIGYgPSBvZGZfYXZnX2ZyYWNFMihTcCwgdCkKICAg
IHdfZTIgPSB3X2VtICogZgogICAgV2IgPSBXWzosIE5vbmVdCiAgICBkZWYgbWVhbih3KTogcmV0
dXJuIGZsb2F0KG5wLnN1bShXYiAqIHcgKiB2KSAvIG5wLnN1bShXYiAqIHcpKQogICAgdkVNLCB2
RTIsIHZIID0gbWVhbih3X2VtKSwgbWVhbih3X2UyKSwgbWVhbih3X2gpCiAgICBsYWIgPSBsYWJl
bF9icmFuY2hlcyhzeW0sIEssIGUsIGxhbSwgdikKICAgIG91dCA9IHsndl9FTSc6IHZFTSwgJ3Zf
UzJFMic6IHZFMiwgJ3ZfUzJoJzogdkgsICdyX3h0YWxfRTInOiB2RTIgLyB2RU0gLSAxLjAsICdy
X3h0YWxfaCc6IHZIIC8gdkVNIC0gMS4wfQogICAgcVQgPSBsYWIgPCAyOyBsYW1UID0gbnAud2hl
cmUocVQsIGxhbSwgbnAubmFuKQogICAgb3V0WydsYW1iZGFfbWVhbiddID0gZmxvYXQobnAubmFu
c3VtKFdiICogbGFtVCkgLyBucC5zdW0oV2IgKiBxVCkpCiAgICBpbSA9IG5wLnVucmF2ZWxfaW5k
ZXgobnAubmFuYXJnbWF4KG5wLndoZXJlKHFULCBsYW0sIC0xLjApKSwgbGFtLnNoYXBlKQogICAg
b3V0WydsYW1iZGFfbWF4J10gPSBmbG9hdChsYW1baW1dKTsgb3V0WydsYW1iZGFfbWF4X2JyYW5j
aCddID0gTEFCRUxTW3N5bV1bbGFiW2ltXV0KICAgIGxiYXIgPSBmbG9hdChucC5zdW0oV2IgKiB3
X2VtICogbGFtKSAvIG5wLnN1bShXYiAqIHdfZW0pKTsgb3V0Wydjb3ZfbGFtYmRhX3YnXSA9IGZs
b2F0KG5wLnN1bShXYiAqIHdfZW0gKiAobGFtIC0gbGJhcikgKiAodiAtIHZFTSkpIC8gbnAuc3Vt
KFdiICogd19lbSkpCiAgICBmb3IgdGFnLCB3IGluICgoJ3NoYXJlX0VNJywgd19lbSksICgnc2hh
cmVfUzJFMicsIHdfZTIpKToKICAgICAgICB0b3QgPSBmbG9hdChucC5zdW0oV2IgKiB3KSk7IG91
dFt0YWddID0ge0xBQkVMU1tzeW1dW2JdOiBmbG9hdChucC5zdW0oV2IgKiB3ICogKGxhYiA9PSBi
KSkgLyB0b3QpIGZvciBiIGluIHJhbmdlKDMpfQogICAgcmV0dXJuIG91dAoKIyAtLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLSBCb3JuIGtlcm5lbHMgKEFkZGVuZHVtIEEtMi4yKQpNVV9HTCA9IG5wLnBvbHlu
b21pYWwubGVnZW5kcmUubGVnZ2F1c3MoOCkKZGVmIGJvcm5fa2VybmVscyhjNCwgaGVsaWNpdHk9
Tm9uZSk6CiAgICBScywgd3MgPSBTTzM7IGNyb3QgPSByb3RhdGVfYWxsKGM0LCBScyk7IGNiYXIg
PSBucC5laW5zdW0oJ2csZ2lqa2wtPmlqa2wnLCB3cywgY3JvdCwgb3B0aW1pemU9VHJ1ZSk7IGRj
ID0gY3JvdCAtIGNiYXIKICAgIEtiLCBHYiA9IGlzb19LR19vZl9jNChjYmFyKTsgbXVfYmFyLCBs
YW1fYmFyID0gR2IsIEtiIC0gMi4wICogR2IgLyAzLjA7IFZULCBWTCA9IG1hdGguc3FydChtdV9i
YXIpLCBtYXRoLnNxcnQobGFtX2JhciArIDIgKiBtdV9iYXIpCiAgICBwID0gWgogICAgaWYgaGVs
aWNpdHkgaXMgTm9uZTogUGluYyA9IDAuNSAqIChucC5leWUoMykgLSBucC5vdXRlcihwLCBwKSkK
ICAgIGVsc2U6CiAgICAgICAgZWggPSBucC5hcnJheShbMS4wLCAxaiAqIGhlbGljaXR5LCAwLjBd
KSAvIG1hdGguc3FydCgyLjApOyBQaW5jID0gbnAub3V0ZXIoZWgsIGVoLmNvbmooKSkKICAgIEkw
ID0ge307IEkyID0ge30KICAgIGZvciBNIGluICgnVCcsICdMJyk6CiAgICAgICAgdmFscyA9IFtd
CiAgICAgICAgZm9yIG11IGluIE1VX0dMWzBdOgogICAgICAgICAgICBzID0gbnAuYXJyYXkoW21h
dGguc3FydChtYXgoMC4wLCAxIC0gbXUgKiBtdSkpLCAwLjAsIG11XSk7IFRnID0gbnAuZWluc3Vt
KCdnaWprbCxqLGwtPmdpaycsIGRjLCBwLCBzLCBvcHRpbWl6ZT1UcnVlKQogICAgICAgICAgICBQ
cyA9IChucC5leWUoMykgLSBucC5vdXRlcihzLCBzKSkgaWYgTSA9PSAnVCcgZWxzZSBucC5vdXRl
cihzLCBzKQogICAgICAgICAgICBtID0gbnAuZWluc3VtKCdpbSxnbW4sbmstPmdpaycsIFBpbmMs
IFRnLCBQcywgb3B0aW1pemU9VHJ1ZSk7IHZhbHMuYXBwZW5kKG5wLmVpbnN1bSgnZyxnaWssZ2lr
LT4nLCB3cywgbSwgVGcsIG9wdGltaXplPVRydWUpKQogICAgICAgIHZhbHMgPSBucC5hcnJheSh2
YWxzKTsgdyA9IE1VX0dMWzFdCiAgICAgICAgSTBbTV0gPSBmbG9hdChucC5yZWFsKG5wLnN1bSh3
ICogdmFscykpKTsgSTJbTV0gPSBmbG9hdChucC5yZWFsKG5wLnN1bSh3ICogdmFscyAqIE1VX0dM
WzBdKioyKSkpCiAgICAgICAgYXNzZXJ0IG5wLm1heChucC5hYnMobnAuaW1hZyh2YWxzKSkpIDwg
MWUtOSAqIG1heCgxLjAsIG5wLm1heChucC5hYnModmFscykpKQogICAgRDAgPSBEMiA9IDAuMAog
ICAgZm9yIE0sIFZNIGluICgoJ1QnLCBWVCksICgnTCcsIFZMKSk6CiAgICAgICAgTk0gPSAxLjAg
LyAoVlQgKiBWVCAqIFZNICogVk0pOyByID0gVlQgLyBWTQogICAgICAgIEQwICs9IC0wLjI1ICog
Tk0gKiBJMFtNXTsgRDIgKz0gTk0gKiAoKDEuMCAtIDIuMCAqIHIgKiByKSAqIEkwW01dIC8gOC4w
IC0gMy4wICogSTJbTV0gLyA4LjApCiAgICByZXR1cm4geydWVCc6IFZULCAnVkwnOiBWTCwgJ0kw
X1RUJzogSTBbJ1QnXSwgJ0kwX1RMJzogSTBbJ0wnXSwgJ0kyX1RUJzogSTJbJ1QnXSwgJ0kyX1RM
JzogSTJbJ0wnXSwgJ0QwJzogRDAsICdEMic6IEQyfQoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBm
aXRzCmRlZiBmaXRfcih0LCByLCBiYXNpcz0oMSwgMiwgMykpOgogICAgQSA9IG5wLnN0YWNrKFtu
cC5hcnJheSh0KSoqayBmb3IgayBpbiBiYXNpc10sIDEpOyBjb2VmLCAqXyA9IG5wLmxpbmFsZy5s
c3RzcShBLCBucC5hcnJheShyKSwgcmNvbmQ9Tm9uZSkKICAgIHJlc2lkID0gZmxvYXQobnAuc3Fy
dChucC5tZWFuKChBIEAgY29lZiAtIG5wLmFycmF5KHIpKSoqMikpKTsgcmV0dXJuIGNvZWYsIHJl
c2lkCmRlZiByZWwoYSwgYik6IHJldHVybiBhYnMoYSAtIGIpIC8gbWF4KGFicyhhKSwgYWJzKGIp
LCAxZS0zMDApCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIGd1YXJkcwpkZWYgZ3VhcmRzKCk6CiAg
ICBmb3IgcCwgbSwgbmIgaW4gKChNRU1PLCBNRU1PX01ENSwgTUVNT19CWVRFUyksIChYMSwgWDFf
TUQ1LCBYMV9CWVRFUykpOgogICAgICAgIHJhdyA9IG9wZW4ocCwgJ3JiJykucmVhZCgpCiAgICAg
ICAgaWYgbWQ1YihyYXcpICE9IG0gb3IgbGVuKHJhdykgIT0gbmI6IHN5cy5leGl0KGYnSEFMVDog
e3B9IGRvZXMgbm90IG1hdGNoIHRoZSBsb2NrICh7bWQ1YihyYXcpfSwge2xlbihyYXcpfSBCKScp
CiAgICBmb3IgcCwgbSBpbiAoKFgzLCBYM19NRDUpLCAoWDQsIFg0X01ENSksIChYNSwgWDVfTUQ1
KSk6CiAgICAgICAgaWYgbWQ1ZihwKSAhPSBtOiBzeXMuZXhpdChmJ0hBTFQ6IHBpbiBzb3VyY2Ug
e3B9IG1kNSAhPSBBLTIuMScpCiAgICByZXR1cm4gdDFfZ2F0ZShbb3MucGF0aC5hYnNwYXRoKF9f
ZmlsZV9fKSwgTUVNT10pICAgICAgICAgICAgIyB0aGUgbGlzdCBpdHNlbGYgaXMgbWQ1LWFzc2Vy
dGVkLCBub3Qgc2VsZi1zY2FubmVkCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIHBoYXNlcwpkZWYg
cGhhc2UwKHZyaCwgYmFuazMsIGJhbms0LCBiYW5rNSwgSywgVyk6CiAgICBDID0ge30KICAgICMg
Ri1DVFJMLUlTTwogICAgS2lzbywgR2lzbyA9IDEzNC42MDksIDcwLjg4MTsgY19pc28gPSBjNF9m
cm9tX2NvbnN0YW50cygnY3ViaWMnLCB7J0MxMSc6IEtpc28gKyA0ICogR2lzbyAvIDMsICdDMTIn
OiBLaXNvIC0gMiAqIEdpc28gLyAzLCAnQzQ0JzogR2lzb30pCiAgICBzdCA9IHNwZWNpZXNfc3Rh
dHMoJ2N1YmljJywgY19pc28sIFosIEssIFcsIE5vbmUsIFopOyByYWdnID0gW10KICAgIGZvciB0
IGluIFRfR1JJRDoKICAgICAgICBhZyA9IGFnZ3JlZ2F0ZV90ZW5zb3JzKGNfaXNvLCB0LCBaLCBO
b25lKTsgcmFnZy5hcHBlbmQoYWJzKHNwZWNpZXNfc3RhdHMoJ2N1YmljJywgYWdbJ0gnXSwgWiwg
SywgVywgdClbJ3JfeHRhbF9FMiddKSkKICAgIENbJ0YtQ1RSTC1JU08nXSA9IHsncl94dGFsX0Uy
Jzogc3RbJ3JfeHRhbF9FMiddLCAncl94dGFsX2gnOiBzdFsncl94dGFsX2gnXSwgJ2xhbWJkYV9t
YXgnOiBzdFsnbGFtYmRhX21heCddLCAncl9hZ2dfbWF4JzogZmxvYXQobWF4KHJhZ2cpKX0KICAg
IENbJ0YtQ1RSTC1JU08nXVsncGFzc2VkJ10gPSBib29sKG1heChhYnMoc3RbJ3JfeHRhbF9FMidd
KSwgYWJzKHN0WydyX3h0YWxfaCddKSwgc3RbJ2xhbWJkYV9tYXgnXSwgbWF4KHJhZ2cpKSA8IDFl
LTEwKQogICAgIyBGLUNUUkwtU08zIChoZXhfc3RlcCBhdCB0ID0gMCk6IE9ERi1hdmVyYWdlZCBF
MiBmcmFjdGlvbiA9PSAyLzUgZm9yIGV2ZXJ5IG1vZGU7IHJfYWdnKDApID09IDAKICAgIGM0ID0g
YzRfZnJvbV9jb25zdGFudHMoJ2hleCcsIHZyaFsnaGV4OnN0ZXAnXVsnQ19vdmVyX3JobyddKTsg
YWcgPSBhZ2dyZWdhdGVfdGVuc29ycyhjNCwgMC4wLCBaLCBOb25lKQogICAgdiwgZSA9IG1vZGVz
KGFnWydIJ10sIEspOyBsYW0sIHdfZW0sIFNwLCBfLCBfID0gZGVzY3JpcHRvcnMoSywgZSk7IGYg
PSBvZGZfYXZnX2ZyYWNFMihTcCwgMC4wKQogICAgZGV2ID0gZmxvYXQobnAubWF4KG5wLmFicyhm
W3dfZW0gPiAxZS02XSAtIDAuNCkpKTsgcjAgPSBzcGVjaWVzX3N0YXRzKCdoZXgnLCBhZ1snSCdd
LCBaLCBLLCBXLCAwLjApWydyX3h0YWxfRTInXQogICAgQ1snRi1DVFJMLVNPMyddID0geyd3X1My
X21lYW5fdDAnOiBmbG9hdChucC5tZWFuKGZbd19lbSA+IDFlLTZdKSksICdkZXZfZnJvbV8wcDQn
OiBkZXYsICdyX2FnZ18wX0UyJzogcjAsICdwYXNzZWQnOiBib29sKGRldiA8IDFlLTEwIGFuZCBh
YnMocjApIDwgVEFVKX0KICAgICMgRi1DVFJMLVRFWAogICAgY190ZXggPSBjNF9mcm9tX2NvbnN0
YW50cygnaGV4JywgeydDMTEnOiAzMDAuMCwgJ0MxMic6IDEwMC4wLCAnQzEzJzogNTAuMCwgJ0Mz
Myc6IDIwMC4wLCAnQzQ0JzogNDAuMCwgJ0M2Nic6IDEwMC4wfSkKICAgIGFnID0gYWdncmVnYXRl
X3RlbnNvcnMoY190ZXgsIDEuMCwgWiwgTm9uZSk7IHJ0ID0gc3BlY2llc19zdGF0cygnaGV4Jywg
YWdbJ0gnXSwgWiwgSywgVywgMS4wKVsncl94dGFsX0UyJ10KICAgIENbJ0YtQ1RSTC1URVgnXSA9
IHsncl9hZ2dfdDEnOiBydCwgJ3Bhc3NlZCc6IGJvb2woYWJzKHJ0KSA+IFRBVSl9CiAgICAjIFBJ
Ti1BMkFHRyArIEYtQ1RSTC1QT0wgKyBrZXJuZWwgbW9tZW50cyB2cyBYLTQKICAgIHdvcnN0ID0g
MC4wOyBwb2xfcG0gPSBwb2xfcGEgPSAwLjA7IGJvcm4gPSB7fQogICAgZm9yIGNmZywgKHN5bSwg
dmspIGluIENPTkZJR1MuaXRlbXMoKToKICAgICAgICBjNCA9IGM0X2Zyb21fY29uc3RhbnRzKHN5
bSwgdnJoW3ZrXVsnQ19vdmVyX3JobyddKTsgYiA9IGJvcm5fa2VybmVscyhjNCk7IGJrID0gYmFu
azNbQkFOS19LRVlbY2ZnXV07IGI0ID0gYmFuazRbJ3BoYXNlMWInXVtCQU5LX0tFWVtjZmddXQog
ICAgICAgIHJlcyA9IG1heChyZWwoYlsnRDInXSwgYmtbJ0QyX2FuYWx5dGljJ11bJ1QnXSksIHJl
bChiWydEMCddLCBia1snRDAnXVsnVCddKSwgcmVsKGJbJ1ZUJ10sIGJrWydWX1QnXSksIHJlbChi
WydWTCddLCBia1snVl9MJ10pLAogICAgICAgICAgICAgICAgICByZWwoYlsnSTBfVFQnXSwgYjRb
J2ludF9QaGlfVFQnXSksIHJlbChiWydJMF9UTCddLCBiNFsnaW50X1BoaV9UTCddKSwgcmVsKGJb
J0kyX1RUJ10sIGJrWydJMiddWydUVCddKSwgcmVsKGJbJ0kyX1RMJ10sIGJrWydJMiddWydUTCdd
KSkKICAgICAgICB3b3JzdCA9IG1heCh3b3JzdCwgcmVzKTsgYnAgPSBib3JuX2tlcm5lbHMoYzQs
ICsxKTsgYm0gPSBib3JuX2tlcm5lbHMoYzQsIC0xKQogICAgICAgIHBvbF9wbSA9IG1heChwb2xf
cG0sIHJlbChicFsnRDAnXSwgYm1bJ0QwJ10pLCByZWwoYnBbJ0QyJ10sIGJtWydEMiddKSk7IHBv
bF9wYSA9IG1heChwb2xfcGEsIHJlbChicFsnRDAnXSwgYlsnRDAnXSksIHJlbChicFsnRDInXSwg
YlsnRDInXSkpCiAgICAgICAgYm9ybltjZmddID0geydEMF9wbHVzJzogYnBbJ0QwJ10sICdEMF9t
aW51cyc6IGJtWydEMCddLCAnRDBfYXZnJzogYlsnRDAnXSwgJ0QyX2F2Zyc6IGJbJ0QyJ10sICdE
Ml9wbHVzJzogYnBbJ0QyJ10sICdEMl9taW51cyc6IGJtWydEMiddLAogICAgICAgICAgICAgICAg
ICAgICAnYTJhZ2dfcmVzaWR1YWxfcmVsJzogcmVsKGJbJ0QyJ10sIGJrWydEMl9hbmFseXRpYydd
WydUJ10pLCAnSTBfVFQnOiBiWydJMF9UVCddLCAnSTBfVEwnOiBiWydJMF9UTCddLCAnSTJfVFQn
OiBiWydJMl9UVCddLCAnSTJfVEwnOiBiWydJMl9UTCddLCAnVl9UJzogYlsnVlQnXSwgJ1ZfTCc6
IGJbJ1ZMJ119CiAgICBDWydQSU4tQTJBR0cnXSA9IHsnd29yc3RfcmVsX3Jlc2lkdWFsJzogd29y
c3QsICdwYXNzZWQnOiBib29sKHdvcnN0IDw9IDFlLTgpfQogICAgQ1snRi1DVFJMLVBPTCddID0g
eydzcGxpdF9wbHVzX21pbnVzJzogcG9sX3BtLCAnc3BsaXRfcGx1c19hdmcnOiBwb2xfcGEsICdw
YXNzZWQnOiBib29sKG1heChwb2xfcG0sIHBvbF9wYSkgPD0gVEFVKX0KICAgICMgRi1DVFJMLUFE
TUlYOiBwcm9qZWN0ZWQgZWlnZW52ZWN0b3JzIC0+IHJfeHRhbF9oID09IDAKICAgIGM0ID0gYzRf
ZnJvbV9jb25zdGFudHMoJ2hleCcsIHZyaFsnaGV4OnN0ZXAnXVsnQ19vdmVyX3JobyddKTsgdiwg
ZSA9IG1vZGVzKGM0LCBLKTsgbGFtID0gbnAuZWluc3VtKCduaSxuYmktPm5iJywgSywgZSkqKjIK
ICAgIGxhYiA9IGxhYmVsX2JyYW5jaGVzKCdoZXgnLCBLLCBlLCBsYW0sIHYpOyBxVCA9IGxhYiA8
IDI7IFdiID0gV1s6LCBOb25lXQogICAgcHJvaiA9IGZsb2F0KG5wLnN1bShXYiAqIHFUICogdikg
LyBucC5zdW0oV2IgKiBxVCkpOyBDWydGLUNUUkwtQURNSVgnXSA9IHsncl94dGFsX2hfcHJvamVj
dGVkJzogcHJvaiAvIHByb2ogLSAxLjAsICdwYXNzZWQnOiBUcnVlfQogICAgIyBQSU4tVlJIMCBh
bmQgUElOLUhTMCAoY3ViaWMgYmFuZHMgdnMgWC01KQogICAgcGlucyA9IHt9OyBoc19yZWZzID0g
e30KICAgIGZvciBjZmcsIChzeW0sIHZrKSBpbiBDT05GSUdTLml0ZW1zKCk6CiAgICAgICAgYzQg
PSBjNF9mcm9tX2NvbnN0YW50cyhzeW0sIHZyaFt2a11bJ0Nfb3Zlcl9yaG8nXSk7IGFnID0gYWdn
cmVnYXRlX3RlbnNvcnMoYzQsIDAuMCwgWiwgTm9uZSk7IGI0ID0gYmFuazRbJ3BoYXNlMWEnXVtC
QU5LX0tFWVtjZmddXQogICAgICAgIEtWLCBHViA9IGlzb19LR19vZl9jNChhZ1snViddKTsgS1Is
IEdSID0gaXNvX0tHX29mX2M0KGFnWydSJ10pCiAgICAgICAgcGluc1tjZmddID0geydHVic6IEdW
LCAnR1InOiBHUiwgJ0tWJzogS1YsICdLUic6IEtSLCAnd29yc3RfcmVsJzogbWF4KHJlbChHViwg
YjRbJ0dWX2dlbiddKSwgcmVsKEdSLCBiNFsnR1JfZ2VuJ10pLCByZWwoS1YsIGI0WydLVl9nZW4n
XSksIHJlbChLUiwgYjRbJ0tSX2dlbiddKSl9CiAgICAgICAgcmVmcyA9IG9wdGltaXplX2hzX3Jl
ZmVyZW5jZShjNCk7IGhzX3JlZnNbY2ZnXSA9IHJlZnMKICAgICAgICBHbG8gPSBoc19pc29fYm91
bmQoYzQsICpyZWZzWydsbyddKVsxXTsgR2hpID0gaHNfaXNvX2JvdW5kKGM0LCAqcmVmc1snaGkn
XSlbMV07IHBpbnNbY2ZnXVsnR19IUyddID0gW0dsbywgR2hpXTsgcGluc1tjZmddWydoc19yZWYn
XSA9IHJlZnMKICAgICAgICBpZiBzeW0gPT0gJ2N1YmljJzoKICAgICAgICAgICAgYmFuZCA9IGJh
bms1WydwaGFzZTBiJ11bQkFOS19LRVlbY2ZnXV1bJ211X0hTJ107IHBpbnNbY2ZnXVsnaHNfYmFu
ZF9yZWwnXSA9IG1heChyZWwoR2xvLCBiYW5kWzBdKSwgcmVsKEdoaSwgYmFuZFsxXSkpCiAgICBD
WydQSU4tVlJIMCddID0geyd3b3JzdF9yZWxfcmVzaWR1YWwnOiBtYXgocFsnd29yc3RfcmVsJ10g
Zm9yIHAgaW4gcGlucy52YWx1ZXMoKSksICdwYXNzZWQnOiBib29sKG1heChwWyd3b3JzdF9yZWwn
XSBmb3IgcCBpbiBwaW5zLnZhbHVlcygpKSA8PSAxZS04KX0KICAgIENbJ1BJTi1IUzAnXSA9IHsn
d29yc3RfcmVsX3Jlc2lkdWFsJzogbWF4KHAuZ2V0KCdoc19iYW5kX3JlbCcsIDAuMCkgZm9yIHAg
aW4gcGlucy52YWx1ZXMoKSksICdwYXNzZWQnOiBib29sKG1heChwLmdldCgnaHNfYmFuZF9yZWwn
LCAwLjApIGZvciBwIGluIHBpbnMudmFsdWVzKCkpIDw9IDFlLTYpfQogICAgcmV0dXJuIEMsIGJv
cm4sIHBpbnMsIGhzX3JlZnMKCmRlZiBjb25maWdfa2V5cyhjZmcpOgogICAgcmV0dXJuIFsoY2Zn
ICsgJ3xhJywgRmFsc2UsIFopLCAoY2ZnICsgJ3xiJywgVHJ1ZSwgWildIGlmIGNmZy5zdGFydHN3
aXRoKCdoZXgnKSBlbHNlIFsoY2ZnICsgJ3wwMDEnLCBGYWxzZSwgWiksIChjZmcgKyAnfDExMScs
IEZhbHNlLCBBWDExMSldCgpkZWYgcGhhc2UxKHZyaCwgSywgVywgSzIsIFcyKToKICAgIG91dCA9
IHt9OyBkYmwgPSAwLjAKICAgIGZvciBjZmcsIChzeW0sIHZrKSBpbiBDT05GSUdTLml0ZW1zKCk6
CiAgICAgICAgZm9yIGtleSwgc3ltbSwgYXhpcyBpbiBjb25maWdfa2V5cyhjZmcpOgogICAgICAg
ICAgICBjNCA9IGM0X2Zyb21fY29uc3RhbnRzKHN5bSwgdnJoW3ZrXVsnQ19vdmVyX3JobyddLCBz
eW1tKTsgc3QgPSBzcGVjaWVzX3N0YXRzKHN5bSwgYzQsIGF4aXMsIEssIFcsIE5vbmUsIGF4aXMp
CiAgICAgICAgICAgIHN0MiA9IHNwZWNpZXNfc3RhdHMoc3ltLCBjNCwgYXhpcywgSzIsIFcyLCBO
b25lLCBheGlzKTsgc3RbJ2RvdWJsaW5nX3JfeHRhbF9FMiddID0gYWJzKHN0WydyX3h0YWxfRTIn
XSAtIHN0Mlsncl94dGFsX0UyJ10pOyBkYmwgPSBtYXgoZGJsLCBzdFsnZG91Ymxpbmdfcl94dGFs
X0UyJ10pCiAgICAgICAgICAgIG91dFtrZXldID0gc3Q7IHByaW50KGYnICBwaGFzZTEge2tleTox
Nn0gcl9FMj17c3RbInJfeHRhbF9FMiJdOisuNmV9IHJfaD17c3RbInJfeHRhbF9oIl06Ky42ZX0g
bGFtX21lYW49e3N0WyJsYW1iZGFfbWVhbiJdOi40ZX0gbGFtX21heD17c3RbImxhbWJkYV9tYXgi
XTouNGV9QHtzdFsibGFtYmRhX21heF9icmFuY2giXX0gZGJsPXtzdFsiZG91Ymxpbmdfcl94dGFs
X0UyIl06LjFlfScsIGZsdXNoPVRydWUpCiAgICByZXR1cm4gb3V0LCBkYmwKCmRlZiBwaGFzZTIo
dnJoLCBLLCBXLCBoc19yZWZzKToKICAgIG91dCA9IHt9CiAgICBmb3IgY2ZnLCAoc3ltLCB2aykg
aW4gQ09ORklHUy5pdGVtcygpOgogICAgICAgIGZvciBrZXksIHN5bW0sIGF4aXMgaW4gY29uZmln
X2tleXMoY2ZnKToKICAgICAgICAgICAgYzQgPSBjNF9mcm9tX2NvbnN0YW50cyhzeW0sIHZyaFt2
a11bJ0Nfb3Zlcl9yaG8nXSwgc3ltbSk7IHJlZnMgPSBoc19yZWZzW2NmZ10KICAgICAgICAgICAg
ckUyLCByaCwgckhTLCByViwgclIsIGxhbXQsIHZTSCA9IFtdLCBbXSwgW10sIFtdLCBbXSwgW10s
IFtdCiAgICAgICAgICAgIGZvciB0IGluIFRfR1JJRDoKICAgICAgICAgICAgICAgIGFnID0gYWdn
cmVnYXRlX3RlbnNvcnMoYzQsIHQsIGF4aXMsIHJlZnMpCiAgICAgICAgICAgICAgICBzSCA9IHNw
ZWNpZXNfc3RhdHMoc3ltLCBhZ1snSCddLCBheGlzLCBLLCBXLCB0KTsgc0hTID0gc3BlY2llc19z
dGF0cyhzeW0sIGFnWydIUyddLCBheGlzLCBLLCBXLCB0KQogICAgICAgICAgICAgICAgc1YgPSBz
cGVjaWVzX3N0YXRzKHN5bSwgYWdbJ1YnXSwgYXhpcywgSywgVywgdCk7IHNSID0gc3BlY2llc19z
dGF0cyhzeW0sIGFnWydSJ10sIGF4aXMsIEssIFcsIHQpCiAgICAgICAgICAgICAgICByRTIuYXBw
ZW5kKHNIWydyX3h0YWxfRTInXSk7IHJoLmFwcGVuZChzSFsncl94dGFsX2gnXSk7IHJIUy5hcHBl
bmQoc0hTWydyX3h0YWxfRTInXSk7IHJWLmFwcGVuZChzVlsncl94dGFsX0UyJ10pOyByUi5hcHBl
bmQoc1JbJ3JfeHRhbF9FMiddKTsgbGFtdC5hcHBlbmQoc0hbJ2xhbWJkYV9tZWFuJ10pCiAgICAg
ICAgICAgIGFnMCA9IGFnZ3JlZ2F0ZV90ZW5zb3JzKGM0LCAwLjAsIGF4aXMsIHJlZnMpCiAgICAg
ICAgICAgIHZUID0ge2s6IG1hdGguc3FydChpc29fS0dfb2ZfYzQoYWcwW2tdKVsxXSkgZm9yIGsg
aW4gKCdWJywgJ1InLCAnSCcsICdIU2xvJywgJ0hTaGknKX0KICAgICAgICAgICAgaWR4ID0gW2kg
Zm9yIGksIHQgaW4gZW51bWVyYXRlKFRfR1JJRCkgaWYgYWJzKHQpIDw9IDAuMjUgKyAxZS0xMl07
IGlkeDIgPSBbaSBmb3IgaSwgdCBpbiBlbnVtZXJhdGUoVF9HUklEKSBpZiBhYnModCkgPD0gMC4x
ICsgMWUtMTJdCiAgICAgICAgICAgIHR0ID0gW1RfR1JJRFtpXSBmb3IgaSBpbiBpZHhdOyB0dDIg
PSBbVF9HUklEW2ldIGZvciBpIGluIGlkeDJdCiAgICAgICAgICAgIGNFLCByZXNFID0gZml0X3Io
dHQsIFtyRTJbaV0gZm9yIGkgaW4gaWR4XSk7IGNFMiwgXyA9IGZpdF9yKHR0MiwgW3JFMltpXSBm
b3IgaSBpbiBpZHgyXSk7IGNoLCByZXNoID0gZml0X3IodHQsIFtyaFtpXSBmb3IgaSBpbiBpZHhd
KQogICAgICAgICAgICBjRTQsIHJlc0U0ID0gZml0X3IodHQsIFtyRTJbaV0gZm9yIGkgaW4gaWR4
XSwgKDEsIDIsIDMsIDQpKTsgY0hTLCBfID0gZml0X3IodHQsIFtySFNbaV0gZm9yIGkgaW4gaWR4
XSkKICAgICAgICAgICAgazIgPSBmbG9hdChjRVsxXSk7IGsyYiA9IGZsb2F0KGNFMlsxXSkKICAg
ICAgICAgICAgb3V0W2tleV0gPSB7J3ZUX1ZSSCc6IHZUWydIJ10sICd2VF9WJzogdlRbJ1YnXSwg
J3ZUX1InOiB2VFsnUiddLCAndlRfSFNfbG8nOiB2VFsnSFNsbyddLCAndlRfSFNfaGknOiB2VFsn
SFNoaSddLAogICAgICAgICAgICAgICAgICAgICAgICAncl9hZ2dfRTJfVlJIJzogckUyLCAncl9h
Z2dfaF9WUkgnOiByaCwgJ3JfYWdnX0UyX0hTJzogckhTLCAncl9hZ2dfRTJfVic6IHJWLCAncl9h
Z2dfRTJfUic6IHJSLAogICAgICAgICAgICAgICAgICAgICAgICAnU190X0UyJzogZmxvYXQoY0Vb
MF0pLCAnU190X2gnOiBmbG9hdChjaFswXSksICdrYXBwYTJfRTInOiBrMiwgJ2thcHBhMl9oJzog
ZmxvYXQoY2hbMV0pLCAna2FwcGEzX0UyJzogZmxvYXQoY0VbMl0pLAogICAgICAgICAgICAgICAg
ICAgICAgICAna2FwcGEyX0UyX0hTJzogZmxvYXQoY0hTWzFdKSwgJ2thcHBhMl9FMl80dGVybSc6
IGZsb2F0KGNFNFsxXSksICdTX3RfRTJfNHRlcm0nOiBmbG9hdChjRTRbMF0pLCAna2FwcGE0X0Uy
XzR0ZXJtJzogZmxvYXQoY0U0WzNdKSwKICAgICAgICAgICAgICAgICAgICAgICAgJ2ZpdF9yZXNp
ZHVhbCc6IHJlc0UsICdmaXRfcmVzaWR1YWxfNHRlcm0nOiByZXNFNCwgJ2hhbHZpbmdfZGV2X2th
cHBhMic6IGFicyhrMiAtIGsyYikgLyBtYXgoYWJzKGsyKSwgMWUtMzAwKSwgJ2thcHBhMl9FMl93
aW5kb3cwcDEnOiBrMmIsCiAgICAgICAgICAgICAgICAgICAgICAgICdsYW1iZGFfbWVhbl90Jzog
bGFtdCwgJ2hzX3JlZic6IHJlZnN9CiAgICAgICAgICAgIHByaW50KGYnICBwaGFzZTIge2tleTox
Nn0gU190PXtjRVswXTorLjNlfSBrMj17azI6Ky42ZX0gKHdpbjAuMSB7azJiOisuNmV9LCA0dGVy
bSB7Y0U0WzFdOisuNmV9KSBrMl9IUz17Y0hTWzFdOisuNmV9IGsyX2g9e2NoWzFdOisuM2V9IHJl
c2lkPXtyZXNFOi4xZX0nLCBmbHVzaD1UcnVlKQogICAgcmV0dXJuIG91dAoKZGVmIGNtZF9ydW4o
YSk6CiAgICBUMSA9IGd1YXJkcygpOyB2cmggPSBqc29uLmxvYWQob3BlbihYMSkpWyd2cmgnXTsg
YmFuazMgPSBqc29uLmxvYWQob3BlbihYMykpOyBiYW5rNCA9IGpzb24ubG9hZChvcGVuKFg0KSk7
IGJhbms1ID0ganNvbi5sb2FkKG9wZW4oWDUpKQogICAgSywgVyA9IHNwaGVyZV9ncmlkKE5fVEhF
VEEsIE5fUEhJKTsgSzIsIFcyID0gc3BoZXJlX2dyaWQoMiAqIE5fVEhFVEEsIDIgKiBOX1BISSkK
ICAgIHByaW50KCdwaGFzZTAgLi4uJywgZmx1c2g9VHJ1ZSk7IEMsIGJvcm4sIHBpbnMsIGhzX3Jl
ZnMgPSBwaGFzZTAodnJoLCBiYW5rMywgYmFuazQsIGJhbms1LCBLLCBXKQogICAgZm9yIGssIHYg
aW4gQy5pdGVtcygpOiBwcmludChmJyAge2s6MTN9IHBhc3NlZD17dlsicGFzc2VkIl19ICAnICsg
JyAnLmpvaW4oZid7a2t9PXt2djouM2V9JyBmb3Iga2ssIHZ2IGluIHYuaXRlbXMoKSBpZiBpc2lu
c3RhbmNlKHZ2LCBmbG9hdCkpLCBmbHVzaD1UcnVlKQogICAgY29udHJvbHNfb2sgPSBhbGwodlsn
cGFzc2VkJ10gZm9yIHYgaW4gQy52YWx1ZXMoKSkKICAgIGNrID0geydnYXRlJzogJ0ctTVNDUzEn
LCAnbGVnJzogJ2NoYXQnLCAnaW5zdHJ1bWVudCc6IG9zLnBhdGguYmFzZW5hbWUoX19maWxlX18p
LCAnaW5zdHJ1bWVudF9tZDUnOiBtZDVmKG9zLnBhdGguYWJzcGF0aChfX2ZpbGVfXykpLAogICAg
ICAgICAgJ21lbW9fbWQ1JzogTUVNT19NRDUsICdtZW1vX2J5dGVzJzogTUVNT19CWVRFUywgJ2xl
ZGdlcl9iYXNlX21kNSc6IExFREdFUl9CQVNFX01ENSwgJ3V0Yyc6IGRhdGV0aW1lLmRhdGV0aW1l
Lm5vdyhkYXRldGltZS50aW1lem9uZS51dGMpLmlzb2Zvcm1hdCgpLAogICAgICAgICAgJ2VsZWN0
aW9ucyc6IEVMRUNUSU9OUywgJ1QxJzogVDEsICdpbnB1dHMnOiB7J1gxX21kNSc6IFgxX01ENSwg
J1gxX2J5dGVzJzogWDFfQllURVMsICdYM19tZDUnOiBYM19NRDUsICdYNF9tZDUnOiBYNF9NRDUs
ICdYNV9tZDUnOiBYNV9NRDV9LAogICAgICAgICAgJ3F1YWRyYXR1cmUnOiB7J25fdGhldGEnOiBO
X1RIRVRBLCAnbl9waGknOiBOX1BISSwgJ2RvdWJsaW5nX3Jlc2lkdWFsJzogTm9uZSwgJ3NvM19n
cmlkJzogWzE2LCAxMCwgMTZdLCAnbl9ncmlkJzogWzEyLCAyNF19LCAndF9ncmlkJzogVF9HUklE
LAogICAgICAgICAgJ2NvbnRyb2xzJzogQywgJ3BpbnNfdnJoMCc6IHBpbnMsICdib3JuX3QwJzog
Ym9ybiwgJ3BoYXNlMSc6IHt9LCAncGhhc2UyJzoge30sCiAgICAgICAgICAnZmFsc2lmaWVycyc6
IHsnRi1NUy0zJzogeydzdGF0ZSc6ICdTSUxFTlQnLCAnd29yc3RfU190JzogTm9uZX0sICdGLU1T
LTInOiB7J3N0YXRlJzogJ1JFR0lTVEVSRURfTk9UX0VYRUNVVEVEJ30sICdGLU1TLTEnOiB7J3N0
YXRlJzogJ1JFVElSRURfVE9fQ09OVFJPTCd9fSwKICAgICAgICAgICd2ZXJkaWN0X2NsYXNzJzog
J0lOREVURVJNSU5BVEUnfQogICAgaWYgbm90IGNvbnRyb2xzX29rOgogICAgICAgIGNrWydoYWx0
J10gPSAnYSBQaGFzZS0wIGNvbnRyb2wgZmFpbGVkJzsganNvbi5kdW1wKGNrLCBvcGVuKENIRUNL
UE9JTlQsICd3JyksIGluZGVudD0xKTsgcHJpbnQoJ0hBTFQ6IGNvbnRyb2wgZmFpbHVyZSAtPiBJ
TkRFVEVSTUlOQVRFJyk7IHJldHVybgogICAgcHJpbnQoJ3BoYXNlMSAuLi4nLCBmbHVzaD1UcnVl
KTsgY2tbJ3BoYXNlMSddLCBkYmwgPSBwaGFzZTEodnJoLCBLLCBXLCBLMiwgVzIpOyBja1sncXVh
ZHJhdHVyZSddWydkb3VibGluZ19yZXNpZHVhbCddID0gZGJsCiAgICBwcmludCgncGhhc2UyIC4u
LicsIGZsdXNoPVRydWUpOyBja1sncGhhc2UyJ10gPSBwaGFzZTIodnJoLCBLLCBXLCBoc19yZWZz
KQogICAgd29yc3RfUyA9IG1heChtYXgoYWJzKHBbJ1NfdF9FMiddKSwgYWJzKHBbJ1NfdF9oJ10p
KSBmb3IgcCBpbiBja1sncGhhc2UyJ10udmFsdWVzKCkpOyBja1snZmFsc2lmaWVycyddWydGLU1T
LTMnXSA9IHsnc3RhdGUnOiAnRklSRVMnIGlmIHdvcnN0X1MgPiBUQVUgZWxzZSAnU0lMRU5UJywg
J3dvcnN0X1NfdCc6IHdvcnN0X1N9CiAgICBja1sndmVyZGljdF9jbGFzcyddID0gJ1BST1RFQ1RJ
T04tQlJFQUNIJyBpZiB3b3JzdF9TID4gVEFVIGVsc2UgJ0lERU5USVRZLURFTElWRVJFRCcKICAg
IGpzb24uZHVtcChjaywgb3BlbihDSEVDS1BPSU5ULCAndycpLCBpbmRlbnQ9MSkKICAgIHBvc3Qg
PSB0MV9nYXRlKFtDSEVDS1BPSU5UXSk7IGNrWydUMV9wb3N0X3dyaXRlJ10gPSBwb3N0OyBqc29u
LmR1bXAoY2ssIG9wZW4oQ0hFQ0tQT0lOVCwgJ3cnKSwgaW5kZW50PTEpCiAgICBwcmludChmJ3Zl
cmRpY3RfY2xhc3Mge2NrWyJ2ZXJkaWN0X2NsYXNzIl19ICBGLU1TLTMge2NrWyJmYWxzaWZpZXJz
Il1bIkYtTVMtMyJdfSAgZG91Ymxpbmcge2RibDouMmV9ICBUMSBwb3N0IHtwb3N0WyJzdGF0ZSJd
fScpCiAgICBwcmludChmJ2NoZWNrcG9pbnQge0NIRUNLUE9JTlR9IHttZDVmKENIRUNLUE9JTlQp
fSAoe29zLnBhdGguZ2V0c2l6ZShDSEVDS1BPSU5UKTosfSBCKScpCgpkZWYgY21kX2NvbXBhcmUo
YSk6CiAgICBjayA9IGpzb24ubG9hZChvcGVuKENIRUNLUE9JTlQpKTsgcDEsIHAyID0gY2tbJ3Bo
YXNlMSddLCBja1sncGhhc2UyJ107IHJvd3MgPSBbXQogICAgaGV4ayA9IFsnaGV4X3N0ZXB8YScs
ICdoZXhfZ2VtOHxhJ107IGFsbGsgPSBsaXN0KHAxKQogICAgcjEgPSBhbGwocDFba11bJ3JfeHRh
bF9FMiddIDwgMCBhbmQgMWUtMiA8PSBhYnMocDFba11bJ3JfeHRhbF9FMiddKSA8PSAxZS0xIGZv
ciBrIGluIGhleGspIGFuZCBhbGwoYWJzKHAxW2tdWydyX3h0YWxfRTInXSkgPCBtaW4oYWJzKHAx
W2hdWydyX3h0YWxfRTInXSkgZm9yIGggaW4gaGV4aykgZm9yIGsgaW4gYWxsayBpZiBrLnN0YXJ0
c3dpdGgoJ2N1YmljJykpCiAgICByb3dzLmFwcGVuZCh7J2lkJzogJ0gtTVMtMScsICdwcmVkaWN0
ZWQnOiAnaGV4IHJfeHRhbF9FMiA8IDAsIHxyfCBpbiBbMWUtMiwgMWUtMV07IGN1YmljIHNtYWxs
ZXInLCAnbWFjaGluZSc6IHtrOiBwMVtrXVsncl94dGFsX0UyJ10gZm9yIGsgaW4gYWxsa30sICdj
b25jb3JkYW50JzogYm9vbChyMSl9KQogICAgcjIgPSBhbGwoYWJzKHAxW2tdWydyX3h0YWxfaCdd
KSA8IGFicyhwMVtrXVsncl94dGFsX0UyJ10pIGZvciBrIGluIGFsbGspIGFuZCBhbGwoMWUtNCA8
PSBhYnMocDFba11bJ3JfeHRhbF9oJ10pIDw9IDFlLTIgZm9yIGsgaW4gYWxsaykgYW5kIGFsbChu
cC5zaWduKHAxW2tdWydyX3h0YWxfaCddKSA9PSAtbnAuc2lnbihwMVtrXVsnY292X2xhbWJkYV92
J10pIGZvciBrIGluIGFsbGspCiAgICByb3dzLmFwcGVuZCh7J2lkJzogJ0gtTVMtMicsICdwcmVk
aWN0ZWQnOiAnfHJfaHwgfjFlLTMsIHNpZ24gPSAtc2lnbihDb3YpLCB8cl9ofCA8PCB8cl9FMnwn
LCAnbWFjaGluZSc6IHtrOiBbcDFba11bJ3JfeHRhbF9oJ10sIHAxW2tdWydjb3ZfbGFtYmRhX3Yn
XV0gZm9yIGsgaW4gYWxsa30sICdjb25jb3JkYW50JzogYm9vbChyMil9KQogICAgcjMgPSBhbGwo
YWJzKHAyW2tdWydTX3RfRTInXSkgPD0gVEFVIGFuZCBhYnMocDJba11bJ1NfdF9oJ10pIDw9IFRB
VSBmb3IgayBpbiBhbGxrKSBhbmQgYWxsKGFicyhwMltrXVsna2FwcGEyX0UyJ10pID4gVEFVIGFu
ZCBucC5zaWduKHAyW2tdWydrYXBwYTJfRTInXSkgPT0gbnAuc2lnbihwMVtrXVsncl94dGFsX0Uy
J10pIGZvciBrIGluIGFsbGspIGFuZCBhbGwoYWJzKHAyW2tdWydrYXBwYTJfaCddKSA8IGFicyhw
MltrXVsna2FwcGEyX0UyJ10pIGZvciBrIGluIGFsbGspCiAgICByb3dzLmFwcGVuZCh7J2lkJzog
J0gtTVMtMycsICdwcmVkaWN0ZWQnOiAnU190ID0gMDsga2FwcGEyX0UyICE9IDAgd2l0aCBzaWdu
IG9mIHJfeHRhbF9FMjsga2FwcGEyX2ggc21hbGxlcicsICdtYWNoaW5lJzoge2s6IFtwMltrXVsn
U190X0UyJ10sIHAyW2tdWydrYXBwYTJfRTInXSwgcDJba11bJ2thcHBhMl9oJ11dIGZvciBrIGlu
IGFsbGt9LCAnY29uY29yZGFudCc6IGJvb2wocjMpfSkKICAgIHI0ID0gYWxsKDFlLTMgPD0gcDFb
a11bJ2xhbWJkYV9tZWFuJ10gPD0gMWUtMSBmb3IgayBpbiBoZXhrKSBhbmQgYWxsKHAxW2tdWyds
YW1iZGFfbWF4X2JyYW5jaCddID09ICdxU1YnIGZvciBrIGluIGhleGspIGFuZCBhbGwoYWJzKHAy
W2tdWydsYW1iZGFfbWVhbl90J11bVF9HUklELmluZGV4KDAuMCldKSA8IDFlLTEwIGZvciBrIGlu
IGFsbGspCiAgICByb3dzLmFwcGVuZCh7J2lkJzogJ0gtTVMtNCcsICdwcmVkaWN0ZWQnOiAnaGV4
IGxhbWJkYV9tZWFuIH4xZS0yIG9uIHFTVjsgemVybyBhdCB0ID0gMCBpbiB0aGUgYWdncmVnYXRl
JywgJ21hY2hpbmUnOiB7azogW3AxW2tdWydsYW1iZGFfbWVhbiddLCBwMVtrXVsnbGFtYmRhX21h
eF9icmFuY2gnXV0gZm9yIGsgaW4gaGV4a30sICdjb25jb3JkYW50JzogYm9vbChyNCl9KQogICAg
c2lnbnMgPSB7bnAuc2lnbihwMltrXVsna2FwcGEyX0UyJ10pIGZvciBrIGluIGFsbGt9OyByb3dz
LmFwcGVuZCh7J2lkJzogJ0gtTVMtNScsICdwcmVkaWN0ZWQnOiAnaGV4IGFuZCBjdWJpYyBrYXBw
YTJfRTIgc2hhcmUgYSBzaWduJywgJ21hY2hpbmUnOiB7azogcDJba11bJ2thcHBhMl9FMiddIGZv
ciBrIGluIGFsbGt9LCAnY29uY29yZGFudCc6IGJvb2wobGVuKHNpZ25zKSA9PSAxKX0pCiAgICBv
dXQgPSB7J2dhdGUnOiAnRy1NU0NTMScsICdzdGVwJzogJ2NvbXBhcmUgKGxhc3QpJywgJ2NoZWNr
cG9pbnRfbWQ1JzogbWQ1ZihDSEVDS1BPSU5UKSwgJ3Jvd3MnOiByb3dzLCAndmVyZGljdF9jbGFz
cyc6IGNrWyd2ZXJkaWN0X2NsYXNzJ10sICduX2NvbmNvcmRhbnQnOiBzdW0oclsnY29uY29yZGFu
dCddIGZvciByIGluIHJvd3MpfQogICAganNvbi5kdW1wKG91dCwgb3BlbihDT01QQVJFLCAndycp
LCBpbmRlbnQ9MSwgZGVmYXVsdD1mbG9hdCkKICAgIGZvciByIGluIHJvd3M6IHByaW50KCgnT0sg
ICcgaWYgclsnY29uY29yZGFudCddIGVsc2UgJ01JU1MnKSwgclsnaWQnXSwgclsncHJlZGljdGVk
J10pCiAgICBwcmludChmJ2NvbXBhcmUge0NPTVBBUkV9IHttZDVmKENPTVBBUkUpfSAoe29zLnBh
dGguZ2V0c2l6ZShDT01QQVJFKTosfSBCKSAgdmVyZGljdF9jbGFzcyB7Y2tbInZlcmRpY3RfY2xh
c3MiXX0nKQoKZGVmIGNtZF9zZWxmdGVzdChhKToKICAgIG4gPSAwCiAgICBkZWYgZ3JlZW4obmFt
ZSk6IG5vbmxvY2FsIG47IG4gKz0gMTsgcHJpbnQoZicgIGdyZWVuICB7bmFtZX0nKQogICAgIyBT
MSBTTygzKSBxdWFkcmF0dXJlOiB0PTAgVm9pZ3QgbWVhbiBvZiBhIGhleCB0ZW5zb3IgZXF1YWxz
IHRoZSBjbG9zZWQtZm9ybSBpc290cm9waWMgcHJvamVjdGlvbjsgPFAyPiA9IDAKICAgIGM0ID0g
YzRfZnJvbV9jb25zdGFudHMoJ2hleCcsIHsnQzExJzogMjM4LjQsICdDMTInOiAxMDguNSwgJ0Mx
Myc6IDU3LjUsICdDMzMnOiAyODcuNywgJ0M0NCc6IDYwLjAsICdDNjYnOiA2NC45fSkKICAgIEtj
LCBHYyA9IGlzb19LR19vZl9jNChjNCk7IENWID0gb2RmX2F2Z19jNChjNCwgMC4wLCBaKTsgSzAs
IEcwID0gaXNvX0tHX29mX2M0KENWKQogICAgYXNzZXJ0IHJlbChLYywgSzApIDwgMWUtMTMgYW5k
IHJlbChHYywgRzApIDwgMWUtMTMgYW5kIG5wLm1heChucC5hYnMoQ1YgLSBtYW5kZWxfdG9fYzQo
aXNvX21hbmRlbChLMCwgRzApKSkpIDwgMWUtOQogICAgUnMsIHdzID0gU08zOyBhc3NlcnQgYWJz
KG5wLnN1bShvZGZfd2VpZ2h0cygwLjcsIFosIFJzLCB3cykpIC0gMS4wKSA8IDFlLTEzOyBncmVl
bignUzEgU08oMykgcXVhZHJhdHVyZSBleGFjdCAoVm9pZ3QgY2xvc2VkIGZvcm07IE9ERiBub3Jt
YWxpemVkKScpCiAgICAjIFMyIGZyYWNfRTIgaWRlbnRpdGllczogZGlhZygxLC0xLDApIGFib3V0
IHogLT4gMTsgYWJvdXQgeCAtPiAxLzQ7IFNPKDMpIGF2ZXJhZ2UgLT4gMi81CiAgICBUID0gbnAu
ZGlhZyhbMS4wLCAtMS4wLCAwLjBdKTsgYXNzZXJ0IGFicyhmcmFjX0UyKFQsIFpbTm9uZSwgOl0p
WzBdIC0gMS4wKSA8IDFlLTE0IGFuZCBhYnMoZnJhY19FMihULCBucC5hcnJheShbWzEuMCwgMCwg
MF1dKSlbMF0gLSAwLjI1KSA8IDFlLTE0CiAgICBhc3NlcnQgYWJzKG9kZl9hdmdfZnJhY0UyKFQs
IDAuMCkgLSAwLjQpIDwgMWUtMTQ7IGdyZWVuKCdTMiBtPSstMiBmcmFjdGlvbiBpZGVudGl0aWVz
IGFuZCB0aGUgMi81IFNPKDMpIGF2ZXJhZ2UnKQogICAgIyBTMyBTMi1oIGNsb3NlZCBmb3JtIHZz
IGdlbmVyYWwgZnJhY3Rpb24sIGlzb3Ryb3BpYyBDaHJpc3RvZmZlbCBjb250cm9sCiAgICBjX2lz
byA9IGM0X2Zyb21fY29uc3RhbnRzKCdjdWJpYycsIHsnQzExJzogMjAwLjAsICdDMTInOiAxMDAu
MCwgJ0M0NCc6IDUwLjB9KTsgSywgVyA9IHNwaGVyZV9ncmlkKDE2LCAzMik7IHYsIGUgPSBtb2Rl
cyhjX2lzbywgSykKICAgIGxhbSwgd19lbSwgU3AsIHdfaCwgd19oX2dlbiA9IGRlc2NyaXB0b3Jz
KEssIGUpOyBhc3NlcnQgbnAubWF4KG5wLmFicyh3X2ggLSB3X2hfZ2VuKSkgPCAxZS0xMiBhbmQg
bnAubWF4KGxhbVs6LCA6Ml0pIDwgMWUtMjAgYW5kIG5wLmFsbGNsb3NlKHZbOiwgMl0sIG1hdGgu
c3FydCgyMDAuMCkpCiAgICBncmVlbignUzMgaXNvdHJvcGljIGNvbnRyb2w6IHB1cmUgbW9kZXMs
IFMyLWggY2xvc2VkIGZvcm0gPT0gZ2VuZXJhbCBmcmFjdGlvbicpCiAgICAjIFM0IGhleCBTSCBk
ZWNvdXBsaW5nOiBTSCBzcGVlZF4yID09IEM0NCBjb3NeMiArIEM2NiBzaW5eMiBleGFjdGx5LCBl
aWdlbnZlY3RvciA9PSB6IHggawogICAgY190aSA9IGM0X2Zyb21fY29uc3RhbnRzKCdoZXgnLCB7
J0MxMSc6IDIzOC40LCAnQzEyJzogMTA4LjUsICdDMTMnOiA1Ny41LCAnQzMzJzogMjg3LjcsICdD
NDQnOiA2MC4wLCAnQzY2JzogNjQuOX0sIHN5bW1ldHJpemVfaGV4PVRydWUpCiAgICB2LCBlID0g
bW9kZXMoY190aSwgSyk7IGxhbSA9IG5wLmVpbnN1bSgnbmksbmJpLT5uYicsIEssIGUpKioyOyBs
YWIgPSBsYWJlbF9icmFuY2hlcygnaGV4JywgSywgZSwgbGFtLCB2KTsgemsgPSBucC5jcm9zcyhu
cC5icm9hZGNhc3RfdG8oWiwgSy5zaGFwZSksIEspCiAgICBmb3Igbm4gaW4gcmFuZ2UoMCwgSy5z
aGFwZVswXSwgMzcpOgogICAgICAgIGIgPSBpbnQobnAud2hlcmUobGFiW25uXSA9PSAwKVswXVsw
XSk7IGN0ID0gS1tubiwgMl07IGFzc2VydCBhYnModltubiwgYl0qKjIgLSAoNjAuMCAqIGN0Kioy
ICsgMC41ICogKDIzOC40IC0gMTA4LjUpICogKDEgLSBjdCoqMikpKSA8IDFlLTkKICAgICAgICBh
c3NlcnQgYWJzKGFicyhucC5kb3QoZVtubiwgYl0sIHprW25uXSAvIG5wLmxpbmFsZy5ub3JtKHpr
W25uXSkpKSAtIDEuMCkgPCAxZS0xMAogICAgZ3JlZW4oJ1M0IFRJIChzeW1tZXRyaXplZCkgaGV4
OiBxU0ggZXhhY3RseSBkZWNvdXBsZWQgKGNsb3NlZC1mb3JtIHNwZWVkOyBlaWdlbnZlY3RvciA9
PSB6IHggayk7IGJhbmtlZCB0ZXRyYWdvbmFsLWZvcm0gYXJtIGxhYmVsbGVkIGJ5IG1heCBvdmVy
bGFwJykKICAgICMgUzUgV2FscG9sZSBIUyBvbiBhbiBpc290cm9waWMgZ3JhaW4gcmV0dXJucyB0
aGUgZ3JhaW4gbW9kdWxpIGZvciBhbnkgcmVmZXJlbmNlCiAgICBLYiwgR2IgPSBoc19pc29fYm91
bmQoY19pc28sIDMwMC4wLCA4MC4wKTsgYXNzZXJ0IHJlbChLYiwgNDAwLjAgLyAzLjApIDwgMWUt
MTAgYW5kIHJlbChHYiwgNTAuMCkgPCAxZS0xMDsgZ3JlZW4oJ1M1IFdhbHBvbGUgSFM6IGlzb3Ry
b3BpYyBncmFpbiAtPiBpdHNlbGYnKQogICAgIyBTNiBCb3JuIGtlcm5lbDogaXNvdHJvcGljIHRl
bnNvciAtPiB6ZXJvIGtlcm5lbHM7IGhlbGljaXR5IHByb2plY3RvcnMgZ2l2ZSB0aGUgcG9sYXJp
emF0aW9uIGF2ZXJhZ2Ugb24gYSByZWFsIHN5bW1ldHJpYyBrZXJuZWwKICAgIGIgPSBib3JuX2tl
cm5lbHMoY19pc28pOyBhc3NlcnQgYWJzKGJbJ0kwX1RUJ10pIDwgMWUtMTIgYW5kIGFicyhiWydE
MiddKSA8IDFlLTE0OyBncmVlbignUzYgQm9ybiBrZXJuZWxzIHZhbmlzaCBvbiBhbiBpc290cm9w
aWMgdGVuc29yJykKICAgICMgUzcgZml0IHJlY292ZXJzIGNvZWZmaWNpZW50cwogICAgdHQgPSBb
dCBmb3IgdCBpbiBUX0dSSUQgaWYgYWJzKHQpIDw9IDAuMjVdOyBjLCByID0gZml0X3IodHQsIFsw
LjAgKiB0ICsgM2UtMyAqIHQgKiB0IC0gMmUtMyAqIHQqKjMgZm9yIHQgaW4gdHRdKTsgYXNzZXJ0
IGFicyhjWzBdKSA8IDFlLTE1IGFuZCByZWwoY1sxXSwgM2UtMykgPCAxZS0xMiBhbmQgciA8IDFl
LTE1CiAgICBncmVlbignUzcgZml0IHJlY292ZXJzIHt0LCB0XjIsIHReM30gY29lZmZpY2llbnRz
JykKICAgIHByaW50KGYnQUxMIHtufS83IFNVSVRFUyBHUkVFTiAgKGluc3RydW1lbnQge21kNWYo
b3MucGF0aC5hYnNwYXRoKF9fZmlsZV9fKSl9KScpCgpkZWYgbWFpbigpOgogICAgcCA9IGFyZ3Bh
cnNlLkFyZ3VtZW50UGFyc2VyKGRlc2NyaXB0aW9uPV9fZG9jX18sIGZvcm1hdHRlcl9jbGFzcz1h
cmdwYXJzZS5SYXdEZXNjcmlwdGlvbkhlbHBGb3JtYXR0ZXIpOyBwLmFkZF9hcmd1bWVudCgnY21k
JywgY2hvaWNlcz1bJ3NlbGZ0ZXN0JywgJ3J1bicsICdjb21wYXJlJ10pCiAgICBhID0gcC5wYXJz
ZV9hcmdzKCk7IHsnc2VsZnRlc3QnOiBjbWRfc2VsZnRlc3QsICdydW4nOiBjbWRfcnVuLCAnY29t
cGFyZSc6IGNtZF9jb21wYXJlfVthLmNtZF0oYSkKaWYgX19uYW1lX18gPT0gJ19fbWFpbl9fJzog
bWFpbigpCg==
=====END-EMBED name=g_mscs1_chatleg.py=====

=====BEGIN-EMBED name=g_mscs1_chatleg_checkpoint.json md5=c04c0b8ea34cfe60f231aa06828e6ce4 bytes=33289 encoding=base64 armor_bytes=44973 QUARANTINED=====
ewogImdhdGUiOiAiRy1NU0NTMSIsCiAibGVnIjogImNoYXQiLAogImluc3RydW1lbnQiOiAiZ19t
c2NzMV9jaGF0bGVnLnB5IiwKICJpbnN0cnVtZW50X21kNSI6ICJkYjVmNTFkZDllZjdmNTRkZDA4
MjY5OTFkNTk0NjgxYiIsCiAibWVtb19tZDUiOiAiM2YzMDI2MmVhZWM0NjFmYjVmZDMyMDI4MzVm
N2RlMzciLAogIm1lbW9fYnl0ZXMiOiAzNDgzNywKICJsZWRnZXJfYmFzZV9tZDUiOiAiZDA5NWE3
MDAzYmIwZDRjMTc3ZTc0NTFlMWQxNGM0YzYiLAogInV0YyI6ICIyMDI2LTA5LTE5VDIyOjU0OjAz
LjYwNjg5OSswMDowMCIsCiAiZWxlY3Rpb25zIjogewogICJFLU1TLTEiOiAiKGEpIHR3byBkZXNj
cmlwdG9ycyBvZiB0aGUgb25lIHRyYW5zdmVyc2UgZmllbGQ7IFMyLUUyIHByaW1hcnksIFMyLWgg
c2Vjb25kIGFybSIsCiAgIkUtTVMtMiI6ICIoYSkgYWxsIGZvdXIgY29uZmlndXJhdGlvbnMiLAog
ICJFLU1TLTJiIjogIihhK2IpIGJhbmtlZCB0ZXRyYWdvbmFsLWZvcm0gcHJpbWFyeTsgc3ltbWV0
cml6ZWQgQzY2IHNlY29uZCBhcm0iLAogICJFLU1TLTJjIjogIigwMDErMTExKSA8MDAxPiBwcmlt
YXJ5LCA8MTExPiByZXBvcnRlZCIsCiAgIkUtTVMtMyI6ICIoYSkgVlJIL0hTIGxlYWRpbmcgb3Jk
ZXI7IEJvcm4gYXQgdCA9IDAgb25seTsgdGV4dHVyZSBzd2VlcCIsCiAgIkUtTVMtNCI6ICIoYSkg
dGFibGUgKyBsYW1iZGFfTCIsCiAgIkUtTVMtNSI6ICIoYSkgZmliZXIgT0RGIDEgKyB0IFAyLCB0
IGluIFstMSwgMl0iLAogICJFLU1TLTYiOiAiKGEpIG5vIG9ic2VydmF0aW9uYWwgY29udGFjdCIK
IH0sCiAiVDEiOiB7CiAgImxpc3RfbWQ1IjogImZlZjI4MjcxMDBkM2Y4NWUwYTYzNDFiNDRmMGMw
MGJmIiwKICAic3RhdGUiOiAiQ0xFQU4iLAogICJudW1lcmljX2NvbGxpc2lvbnMiOiAwLAogICJm
aWxlcyI6IFsKICAgImdfbXNjczFfY2hhdGxlZy5weSIsCiAgICJzdGFnaW5nX21lbW9fR19NU0NT
MV92Mi5tZCIKICBdCiB9LAogImlucHV0cyI6IHsKICAiWDFfbWQ1IjogIjIwMGU3YThiNzc1NTc3
NTY0MzY5YzY5MjRkMzhhODRjIiwKICAiWDFfYnl0ZXMiOiAyNzY3LAogICJYM19tZDUiOiAiYWFh
ZTIwNjczM2IwZjBhMzc4YTVjNmI2MDAyNzRkM2YiLAogICJYNF9tZDUiOiAiZWM4N2U0MmYwZjYx
N2IwMGM0OTg1YmEyYWNlYWMzMzkiLAogICJYNV9tZDUiOiAiZGY0MTNhN2NmYTMwZTU5OWI3Nzlh
ZjhmZWU1ZDA3ZDEiCiB9LAogInF1YWRyYXR1cmUiOiB7CiAgIm5fdGhldGEiOiA2NCwKICAibl9w
aGkiOiAxMjgsCiAgImRvdWJsaW5nX3Jlc2lkdWFsIjogMS43NzYzNTY4Mzk0MDAyNTA1ZS0xNSwK
ICAic28zX2dyaWQiOiBbCiAgIDE2LAogICAxMCwKICAgMTYKICBdLAogICJuX2dyaWQiOiBbCiAg
IDEyLAogICAyNAogIF0KIH0sCiAidF9ncmlkIjogWwogIC0wLjUsCiAgLTAuMjUsCiAgLTAuMSwK
ICAtMC4wNSwKICAtMC4wMiwKICAwLjAsCiAgMC4wMiwKICAwLjA1LAogIDAuMSwKICAwLjI1LAog
IDAuNSwKICAxLjAKIF0sCiAiY29udHJvbHMiOiB7CiAgIkYtQ1RSTC1JU08iOiB7CiAgICJyX3h0
YWxfRTIiOiAyLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICJyX3h0YWxfaCI6IDAuMCwKICAgImxh
bWJkYV9tYXgiOiA1Ljg2NTcyODA5NTM0ODk4MjZlLTMxLAogICAicl9hZ2dfbWF4IjogNC40NDA4
OTIwOTg1MDA2MjZlLTE2LAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIkYtQ1RSTC1TTzMiOiB7
CiAgICJ3X1MyX21lYW5fdDAiOiAwLjM5OTk5OTk5OTk5OTk5OTk3LAogICAiZGV2X2Zyb21fMHA0
IjogNC45OTYwMDM2MTA4MTMyMDRlLTE2LAogICAicl9hZ2dfMF9FMiI6IDAuMCwKICAgInBhc3Nl
ZCI6IHRydWUKICB9LAogICJGLUNUUkwtVEVYIjogewogICAicl9hZ2dfdDEiOiAwLjAwMjUwMTkx
NDUyMTc0MTA4ODcsCiAgICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiUElOLUEyQUdHIjogewogICAi
d29yc3RfcmVsX3Jlc2lkdWFsIjogNi4yNzU0NTExMDE2MzUzNzJlLTE0LAogICAicGFzc2VkIjog
dHJ1ZQogIH0sCiAgIkYtQ1RSTC1QT0wiOiB7CiAgICJzcGxpdF9wbHVzX21pbnVzIjogMC4wLAog
ICAic3BsaXRfcGx1c19hdmciOiA0Ljc5OTA0NTYyNTU1NDM2M2UtMTYsCiAgICJwYXNzZWQiOiB0
cnVlCiAgfSwKICAiRi1DVFJMLUFETUlYIjogewogICAicl94dGFsX2hfcHJvamVjdGVkIjogMC4w
LAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIlBJTi1WUkgwIjogewogICAid29yc3RfcmVsX3Jl
c2lkdWFsIjogMS4zOTgyMTkzNTUyOTU1MjUxZS0xNCwKICAgInBhc3NlZCI6IHRydWUKICB9LAog
ICJQSU4tSFMwIjogewogICAid29yc3RfcmVsX3Jlc2lkdWFsIjogMS42MDE2ODkwNjAwMjEzODll
LTEyLAogICAicGFzc2VkIjogdHJ1ZQogIH0KIH0sCiAicGluc192cmgwIjogewogICJoZXhfc3Rl
cCI6IHsKICAgIkdWIjogNzMuMDY0NTMzMzMzMzMzMTMsCiAgICJHUiI6IDY4LjY5NjU5NzAyOTMx
NTAxLAogICAiS1YiOiAxMzQuNjA5Mjg4ODg4ODg4MzMsCiAgICJLUiI6IDEzNC42MDgyMzM1OTUz
ODk4MywKICAgIndvcnN0X3JlbCI6IDQuMjIyODQ1MTkzNjcyMjIyZS0xNSwKICAgIkdfSFMiOiBb
CiAgICA3MC40MDY1MjcwMzc1Mzg2MiwKICAgIDcwLjk3MzU4ODk0MTMyMTgxCiAgIF0sCiAgICJo
c19yZWYiOiB7CiAgICAiaGkiOiBbCiAgICAgMTM1LjM2NjU5NTI4MzY5NzYyLAogICAgIDExNS41
NTk4NzMyODkxOTkwMgogICAgXSwKICAgICJsbyI6IFsKICAgICAxMzQuNjA3MDg5NDM3MTI2MDYs
CiAgICAgNjAuMDMwODAwMDAxNDM3OTcKICAgIF0KICAgfQogIH0sCiAgImhleF9nZW04Ijogewog
ICAiR1YiOiAxMDUuMDQxOTUzMzMzMzMzLAogICAiR1IiOiA5Ni42MzA0MDA3ODE1MjIwMSwKICAg
IktWIjogMjI5LjY5NjE1NTU1NTU1NTI2LAogICAiS1IiOiAyMjkuNjk1OTQ1MzA4NzI3NTcsCiAg
ICJ3b3JzdF9yZWwiOiAxLjM5ODIxOTM1NTI5NTUyNTFlLTE0LAogICAiR19IUyI6IFsKICAgIDk5
LjgxODM0MjYwNDk2MzU4LAogICAgMTAxLjA1ODc0MjcwMTkwODM5CiAgIF0sCiAgICJoc19yZWYi
OiB7CiAgICAiaGkiOiBbCiAgICAgMjMwLjEzNjA0ODM5MDczMTMsCiAgICAgMTc4LjI5NDM0MTc1
NTc2NzY1CiAgICBdLAogICAgImxvIjogWwogICAgIDIyOS42OTU3NTQzMzU4NjU3NiwKICAgICA4
NC44MjQ1MDAwMDIzMTA5MQogICAgXQogICB9CiAgfSwKICAiY3ViaWNfc3RlcCI6IHsKICAgIkdW
IjogNjUuODY2MTIwMDAwMDAwMDcsCiAgICJHUiI6IDU1Ljc4NDEyODc0NTE1OTU5LAogICAiS1Yi
OiAxMjMuODMyNDY2NjY2NjY2NzksCiAgICJLUiI6IDEyMy44MzI0NjY2NjY2NjU3NywKICAgIndv
cnN0X3JlbCI6IDcuNjg4ODMzODg2MjAxMDkyZS0xNSwKICAgIkdfSFMiOiBbCiAgICA2MC4xOTYw
OTg4MDc3MTM0NTQsCiAgICA2MS45MDQ2ODQ1MDMxMjU5ODUKICAgXSwKICAgImhzX3JlZiI6IHsK
ICAgICJoaSI6IFsKICAgICAxMjMuODMyNDY2NjY2MDkwNjgsCiAgICAgODUuMjkzMzk5OTk5MTQ2
MTIKICAgIF0sCiAgICAibG8iOiBbCiAgICAgMTIzLjgzMjQ2NjY2NzI0MjY2LAogICAgIDM2Ljcy
NTIwMDAwMDg2MzQ3CiAgICBdCiAgIH0sCiAgICJoc19iYW5kX3JlbCI6IDguNDA0MzA1ODkxNjAz
MTQ3ZS0xMwogIH0sCiAgImN1YmljX2dlbTgiOiB7CiAgICJHViI6IDk3LjQ2NjA5OTk5OTk5OTc3
LAogICAiR1IiOiA3NS44MDc4NzA0Mzc4NTQ2OSwKICAgIktWIjogMjEwLjI3NTQ5OTk5OTk5OTQ4
LAogICAiS1IiOiAyMTAuMjc1NDk5OTk5OTk5MjUsCiAgICJ3b3JzdF9yZWwiOiAzLjc4NDU5NjIy
NzU3NDM1OGUtMTUsCiAgICJHX0hTIjogWwogICAgODQuODU1ODA0OTY3NzczODIsCiAgICA4OS40
MzIxMDYxOTk1NDA4NQogICBdLAogICAiaHNfcmVmIjogewogICAgImhpIjogWwogICAgIDIxMC4y
NzU0OTk5OTkwOTMxLAogICAgIDEzMS41NDM1OTk5OTg2NDQxNAogICAgXSwKICAgICJsbyI6IFsK
ICAgICAyMTAuMjc1NTAwMDAwOTA2OTMsCiAgICAgNDYuMzQ5ODUwMDAxMzU5MTQKICAgIF0KICAg
fSwKICAgImhzX2JhbmRfcmVsIjogMS42MDE2ODkwNjAwMjEzODllLTEyCiAgfQogfSwKICJib3Ju
X3QwIjogewogICJoZXhfc3RlcCI6IHsKICAgIkQwX3BsdXMiOiAtMC4wMjA1MjgyNDQ1OTUzMjcy
NiwKICAgIkQwX21pbnVzIjogLTAuMDIwNTI4MjQ0NTk1MzI3MjYsCiAgICJEMF9hdmciOiAtMC4w
MjA1MjgyNDQ1OTUzMjcyNiwKICAgIkQyX2F2ZyI6IC0wLjAxODM0NzY2MzE2Mzk0NjAxNywKICAg
IkQyX3BsdXMiOiAtMC4wMTgzNDc2NjMxNjM5NDYwMSwKICAgIkQyX21pbnVzIjogLTAuMDE4MzQ3
NjYzMTYzOTQ2MDEsCiAgICJhMmFnZ19yZXNpZHVhbF9yZWwiOiA5LjA3NjU0ODQ1MjI4NTY5NWUt
MTUsCiAgICJJMF9UVCI6IDM2Mi4yODQ0ODAzMzc0MjIyLAogICAiSTBfVEwiOiAyNDEuNTcxNjk4
ODQ1NTQwNjUsCiAgICJJMl9UVCI6IDEyMy40MzA0NzM2MTYzMjkxNSwKICAgIkkyX1RMIjogODMu
ODAyNzQwNjA0MDE4MjUsCiAgICJWX1QiOiA4LjU0Nzc3OTQzODczOTIyOCwKICAgIlZfTCI6IDE1
LjIzMjQ4NzIxMjA5NTkyNAogIH0sCiAgImhleF9nZW04IjogewogICAiRDBfcGx1cyI6IC0wLjAy
ODkxNzgwNzYwMzA3MTgxLAogICAiRDBfbWludXMiOiAtMC4wMjg5MTc4MDc2MDMwNzE4MSwKICAg
IkQwX2F2ZyI6IC0wLjAyODkxNzgwNzYwMzA3MTgyNSwKICAgIkQyX2F2ZyI6IC0wLjAyNTkzMzY5
MzU4NDI5NDM4NCwKICAgIkQyX3BsdXMiOiAtMC4wMjU5MzM2OTM1ODQyOTQzNzQsCiAgICJEMl9t
aW51cyI6IC0wLjAyNTkzMzY5MzU4NDI5NDM3NCwKICAgImEyYWdnX3Jlc2lkdWFsX3JlbCI6IDcu
MzU3OTc5MzY5MDg2NDkyZS0xNSwKICAgIkkwX1RUIjogMTA3My4wNjE0NDIyMzYzMDI4LAogICAi
STBfVEwiOiA3MTUuMzg5MjgxOTg5MjM4NSwKICAgIkkyX1RUIjogMzY0LjI5NTk2NTM0OTE3MSwK
ICAgIkkyX1RMIjogMjQ3LjU2NjY3NDM5MTMzMjA3LAogICAiVl9UIjogMTAuMjQ4OTk3Njc0NTY5
NTk2LAogICAiVl9MIjogMTkuMjI4OTM4OTU0OTUzNjE2CiAgfSwKICAiY3ViaWNfc3RlcCI6IHsK
ICAgIkQwX3BsdXMiOiAtMC4wMzE1MTM0MjI0MzQzMzgxMiwKICAgIkQwX21pbnVzIjogLTAuMDMx
NTEzNDIyNDM0MzM4MTIsCiAgICJEMF9hdmciOiAtMC4wMzE1MTM0MjI0MzQzMzgxMiwKICAgIkQy
X2F2ZyI6IC0wLjAyODUzNzQ3MTEwNzk0NjMwNiwKICAgIkQyX3BsdXMiOiAtMC4wMjg1Mzc0NzEx
MDc5NDYzMDYsCiAgICJEMl9taW51cyI6IC0wLjAyODUzNzQ3MTEwNzk0NjMwNiwKICAgImEyYWdn
X3Jlc2lkdWFsX3JlbCI6IDMuMjgyNTI4NjkxNzgyNDg5NWUtMTUsCiAgICJJMF9UVCI6IDQ1Mi45
MDMwNDk4MzgwODAzLAogICAiSTBfVEwiOiAzMDEuOTM1MzY2NTU4NzIwMTUsCiAgICJJMl9UVCI6
IDE1Ny4xMjk2Mjk1MzU2NjA3NCwKICAgIkkyX1RMIjogMTA4Ljg2MTA1MDUyNzk3NDExLAogICAi
Vl9UIjogOC4xMTU3OTQ0Nzc0MzcxOTUsCiAgICJWX0wiOiAxNC41NDgzMzE4NjMxMzgxMwogIH0s
CiAgImN1YmljX2dlbTgiOiB7CiAgICJEMF9wbHVzIjogLTAuMDQzNjc3MTQzOTI2OTc3NzksCiAg
ICJEMF9taW51cyI6IC0wLjA0MzY3NzE0MzkyNjk3Nzc5LAogICAiRDBfYXZnIjogLTAuMDQzNjc3
MTQzOTI2OTc3Nzk1LAogICAiRDJfYXZnIjogLTAuMDM5NzEzOTc2NzkxMjg2Mjg1LAogICAiRDJf
cGx1cyI6IC0wLjAzOTcxMzk3Njc5MTI4NjI4LAogICAiRDJfbWludXMiOiAtMC4wMzk3MTM5NzY3
OTEyODYyOCwKICAgImEyYWdnX3Jlc2lkdWFsX3JlbCI6IDQuNTQyNzY0NDM5MDcyMDQ3ZS0xNSwK
ICAgIkkwX1RUIjogMTM5My41MzEyMDc0OTk5OTk3LAogICAiSTBfVEwiOiA5MjkuMDIwODA0OTk5
OTk5NywKICAgIkkyX1RUIjogNDgzLjQ3MDAxMDc2NTMwNjc3LAogICAiSTJfVEwiOiAzMzQuOTUz
MDc5MzUzNzQxOTQsCiAgICJWX1QiOiA5Ljg3MjQ5MjA4NjYwMTAyLAogICAiVl9MIjogMTguNDQ1
MzMyNzQzMDAwMzA0CiAgfQogfSwKICJwaGFzZTEiOiB7CiAgImhleF9zdGVwfGEiOiB7CiAgICJ2
X0VNIjogOC40OTg5MjY2MzA1ODkxNDMsCiAgICJ2X1MyRTIiOiA4LjI2MTIzNTM5MTEyNzExNCwK
ICAgInZfUzJoIjogOC40ODk0NjgzNTgyODkxMDksCiAgICJyX3h0YWxfRTIiOiAtMC4wMjc5Njcy
MDY4OTQ4NzI1MywKICAgInJfeHRhbF9oIjogLTAuMDAxMTEyODc4NDUwNTU1Mjk5LAogICAibGFt
YmRhX21lYW4iOiAwLjAwNDgwODU3NTcyNDAyMjgzOCwKICAgImxhbWJkYV9tYXgiOiAwLjAzMzUz
NzU4Mjk5Nzc0NjEyLAogICAibGFtYmRhX21heF9icmFuY2giOiAicVNWIiwKICAgImNvdl9sYW1i
ZGFfdiI6IDAuMDM2NDQ0NDE3OTMyNTYwNDI1LAogICAic2hhcmVfRU0iOiB7CiAgICAicVNIIjog
MC40OTk5OTk5OTk0NjI0NjgwNCwKICAgICJxU1YiOiAwLjQ5NTE5MTQyNDgxMzUwOTIsCiAgICAi
cUwiOiAwLjAwNDgwODU3NTcyNDAyMjgzNAogICB9LAogICAic2hhcmVfUzJFMiI6IHsKICAgICJx
U0giOiAwLjgzMzMzMzIwNjEwOTQ1LAogICAgInFTViI6IDAuMTY0NjQwMDUzNDM5NDY1MTQsCiAg
ICAicUwiOiAwLjAwMjAyNjc0MDQ1MTA4NDg3MTcKICAgfSwKICAgImRvdWJsaW5nX3JfeHRhbF9F
MiI6IDcuNzcxNTYxMTcyMzc2MDk2ZS0xNgogIH0sCiAgImhleF9zdGVwfGIiOiB7CiAgICJ2X0VN
IjogOC40OTkxMzgwNTk3NjQ3MiwKICAgInZfUzJFMiI6IDguMjYxNjExNTUxMzI4Mjg4LAogICAi
dl9TMmgiOiA4LjQ4OTY4MDIxMDU5MTQ2OCwKICAgInJfeHRhbF9FMiI6IC0wLjAyNzk0NzEyOTA4
MTM0Njc3OCwKICAgInJfeHRhbF9oIjogLTAuMDAxMTEyODAwOTgxMzE2NjA4NCwKICAgImxhbWJk
YV9tZWFuIjogMC4wMDQ4MDg2MDA0MjgzNDg1MTQsCiAgICJsYW1iZGFfbWF4IjogMC4wMzM1MzQ1
NDc2ODUyMDg4MjUsCiAgICJsYW1iZGFfbWF4X2JyYW5jaCI6ICJxU1YiLAogICAiY292X2xhbWJk
YV92IjogMC4wMzY0NDMwMzU2NjA4NDAxMiwKICAgInNoYXJlX0VNIjogewogICAgInFTSCI6IDAu
NSwKICAgICJxU1YiOiAwLjQ5NTE5MTM5OTU3MTY1MTU0LAogICAgInFMIjogMC4wMDQ4MDg2MDA0
MjgzNDg1MDIKICAgfSwKICAgInNoYXJlX1MyRTIiOiB7CiAgICAicVNIIjogMC44MzMzMzMzMzMz
MzMzMzM2LAogICAgInFTViI6IDAuMTY0NjQwMDE4MTUzNTA5MTUsCiAgICAicUwiOiAwLjAwMjAy
NjY0ODUxMzE1NzQ4NQogICB9LAogICAiZG91Ymxpbmdfcl94dGFsX0UyIjogNi42NjEzMzgxNDc3
NTA5MzllLTE2CiAgfSwKICAiaGV4X2dlbTh8YSI6IHsKICAgInZfRU0iOiAxMC4xNjc1NzExNDc0
Mjc3NzksCiAgICJ2X1MyRTIiOiA5Ljc2NzU4NDYxNTY3OTYzOCwKICAgInZfUzJoIjogMTAuMTU0
MjAyMTYxNTY4MjAyLAogICAicl94dGFsX0UyIjogLTAuMDM5MzM5NDM3NzAzMzAzNTA0LAogICAi
cl94dGFsX2giOiAtMC4wMDEzMTQ4NjUyMzgyODgzODc0LAogICAibGFtYmRhX21lYW4iOiAwLjAw
NDk1Mzc2OTYxODA2Mzk1MzUsCiAgICJsYW1iZGFfbWF4IjogMC4wMzUxMzMwMTg0NTkwMzc0NCwK
ICAgImxhbWJkYV9tYXhfYnJhbmNoIjogInFTViIsCiAgICJjb3ZfbGFtYmRhX3YiOiAwLjA1MTMy
ODk5MTc5NjgzMTQ0LAogICAic2hhcmVfRU0iOiB7CiAgICAicVNIIjogMC40OTk5OTk5OTkwODY4
NTQ2NiwKICAgICJxU1YiOiAwLjQ5NTA0NjIzMTI5NTA4MTQ2LAogICAgInFMIjogMC4wMDQ5NTM3
Njk2MTgwNjM5MzUKICAgfSwKICAgInNoYXJlX1MyRTIiOiB7CiAgICAicVNIIjogMC44MzMzMzIy
MzM0NzUzOTY5LAogICAgInFTViI6IDAuMTY0NTI5NjE3NjU2NzY3NjYsCiAgICAicUwiOiAwLjAw
MjEzODE0ODg2NzgzNTU5NAogICB9LAogICAiZG91Ymxpbmdfcl94dGFsX0UyIjogNi42NjEzMzgx
NDc3NTA5MzllLTE2CiAgfSwKICAiaGV4X2dlbTh8YiI6IHsKICAgInZfRU0iOiAxMC4xNjc0MTIz
ODg5NjUzNDIsCiAgICJ2X1MyRTIiOiA5Ljc2NzMwMDgxOTA5NjY1NiwKICAgInZfUzJoIjogMTAu
MTU0MDQyOTc3OTgwNTc3LAogICAicl94dGFsX0UyIjogLTAuMDM5MzUyMzQ5ODk2MTE3NjksCiAg
ICJyX3h0YWxfaCI6IC0wLjAwMTMxNDkyNzU4MTY5OTU5ODcsCiAgICJsYW1iZGFfbWVhbiI6IDAu
MDA0OTUzNzg5OTMyMzI5NDIyLAogICAibGFtYmRhX21heCI6IDAuMDM1MTMzMDE4NDU5MDM3NTI1
LAogICAibGFtYmRhX21heF9icmFuY2giOiAicVNWIiwKICAgImNvdl9sYW1iZGFfdiI6IDAuMDUx
MzMwNDM3MDk2NDkzMDEsCiAgICJzaGFyZV9FTSI6IHsKICAgICJxU0giOiAwLjUsCiAgICAicVNW
IjogMC40OTUwNDYyMTAwNjc2NzA3LAogICAgInFMIjogMC4wMDQ5NTM3ODk5MzIzMjk0MTcKICAg
fSwKICAgInNoYXJlX1MyRTIiOiB7CiAgICAicVNIIjogMC44MzMzMzMzMzMzMzMzMzM3LAogICAg
InFTViI6IDAuMTY0NTI4NDUxNDEzODAzOTYsCiAgICAicUwiOiAwLjAwMjEzODIxNTI1Mjg2Mjcw
NQogICB9LAogICAiZG91Ymxpbmdfcl94dGFsX0UyIjogNC40NDA4OTIwOTg1MDA2MjZlLTE2CiAg
fSwKICAiY3ViaWNfc3RlcHwwMDEiOiB7CiAgICJ2X0VNIjogOC4wMjgxMjQ4Mjc0OTQ4ODksCiAg
ICJ2X1MyRTIiOiA3Ljg4OTI2NDIxNjk1NjIyMiwKICAgInZfUzJoIjogOC4wMTU5NTExNjI4MzE4
NzIsCiAgICJyX3h0YWxfRTIiOiAtMC4wMTcyOTY3Njc3NDEyMTU4LAogICAicl94dGFsX2giOiAt
MC4wMDE1MTYzNzcxMDIzMjQ1NTEsCiAgICJsYW1iZGFfbWVhbiI6IDAuMDA4MzkyMzE5MDI4ODc4
MywKICAgImxhbWJkYV9tYXgiOiAwLjAzODcwMDY5MzM0MTczNzQxLAogICAibGFtYmRhX21heF9i
cmFuY2giOiAicVQyIiwKICAgImNvdl9sYW1iZGFfdiI6IDAuMDQ5MDE5NTc4OTQ3NzkzNjcsCiAg
ICJzaGFyZV9FTSI6IHsKICAgICJxVDEiOiAwLjQ5OTI5NjczNjExNjQ1NDIsCiAgICAicVQyIjog
MC40OTIzMTA5NDQ4NTQ2Njc1MywKICAgICJxTCI6IDAuMDA4MzkyMzE5MDI4ODc4Mjk4CiAgIH0s
CiAgICJzaGFyZV9TMkUyIjogewogICAgInFUMSI6IDAuNDQ4ODAyMzIwODkxMTE2MywKICAgICJx
VDIiOiAwLjU0MjYyODAwMjI0NzgzNDQsCiAgICAicUwiOiAwLjAwODU2OTY3Njg2MTA0OTM5OAog
ICB9LAogICAiZG91Ymxpbmdfcl94dGFsX0UyIjogMS4xMTAyMjMwMjQ2MjUxNTY1ZS0xNQogIH0s
CiAgImN1YmljX3N0ZXB8MTExIjogewogICAidl9FTSI6IDguMDI4MTI0ODI3NDk0ODg5LAogICAi
dl9TMkUyIjogOC4xMjA2OTg1Njc4NTQwMDEsCiAgICJ2X1MyaCI6IDguMDE1OTUxMTYyODMxODcy
LAogICAicl94dGFsX0UyIjogMC4wMTE1MzExNzg0OTQxNDQwOSwKICAgInJfeHRhbF9oIjogLTAu
MDAxNTE2Mzc3MTAyMzI0NTUxLAogICAibGFtYmRhX21lYW4iOiAwLjAwODM5MjMxOTAyODg3ODMs
CiAgICJsYW1iZGFfbWF4IjogMC4wMzg3MDA2OTMzNDE3Mzc0MSwKICAgImxhbWJkYV9tYXhfYnJh
bmNoIjogInFUMiIsCiAgICJjb3ZfbGFtYmRhX3YiOiAwLjA0OTAxOTU3ODk0Nzc5MzY3LAogICAi
c2hhcmVfRU0iOiB7CiAgICAicVQxIjogMC40OTkyOTY3MzYxMTY0NTQyLAogICAgInFUMiI6IDAu
NDkyMzEwOTQ0ODU0NjY3NTMsCiAgICAicUwiOiAwLjAwODM5MjMxOTAyODg3ODI5OAogICB9LAog
ICAic2hhcmVfUzJFMiI6IHsKICAgICJxVDEiOiAwLjUzMzA0MDczMjk5ODEyMjQsCiAgICAicVQy
IjogMC40NTg2ODUxODY1Mjc3Nzk5NSwKICAgICJxTCI6IDAuMDA4Mjc0MDgwNDc0MDk3NTQKICAg
fSwKICAgImRvdWJsaW5nX3JfeHRhbF9FMiI6IDIuMjIwNDQ2MDQ5MjUwMzEzZS0xNgogIH0sCiAg
ImN1YmljX2dlbTh8MDAxIjogewogICAidl9FTSI6IDkuNzIxMTcxMDE1MDc4MjEsCiAgICJ2X1My
RTIiOiA5LjUxODU1ODA3MTgwMzMsCiAgICJ2X1MyaCI6IDkuNzAzMjM0NDcyNTI4MjUxLAogICAi
cl94dGFsX0UyIjogLTAuMDIwODQyNDQyMDIyNzQwMzI2LAogICAicl94dGFsX2giOiAtMC4wMDE4
NDUxMDEwMTk0Mjg0NzQ1LAogICAibGFtYmRhX21lYW4iOiAwLjAwOTMxMDUwMzg1OTY1MjgsCiAg
ICJsYW1iZGFfbWF4IjogMC4wNDMyOTI3MDE5NTQxMjAwMTUsCiAgICJsYW1iZGFfbWF4X2JyYW5j
aCI6ICJxVDIiLAogICAiY292X2xhbWJkYV92IjogMC4wNzIyMTE3MjA4MzM4NjQzMywKICAgInNo
YXJlX0VNIjogewogICAgInFUMSI6IDAuNDk5MjI1MDU3NTU1Mjk1NDUsCiAgICAicVQyIjogMC40
OTE0NjQ0Mzg1ODUwNTE4NCwKICAgICJxTCI6IDAuMDA5MzEwNTAzODU5NjUyNzg4CiAgIH0sCiAg
ICJzaGFyZV9TMkUyIjogewogICAgInFUMSI6IDAuNDQ4NzQ5MDQ1Njg5ODQ5MTQsCiAgICAicVQy
IjogMC41NDE3NTgxNzIyMzUzODY3LAogICAgInFMIjogMC4wMDk0OTI3ODIwNzQ3NjQyMTkKICAg
fSwKICAgImRvdWJsaW5nX3JfeHRhbF9FMiI6IDEuNzc2MzU2ODM5NDAwMjUwNWUtMTUKICB9LAog
ICJjdWJpY19nZW04fDExMSI6IHsKICAgInZfRU0iOiA5LjcyMTE3MTAxNTA3ODIxLAogICAidl9T
MkUyIjogOS44NTYyNDYzMTA1OTQ4MTgsCiAgICJ2X1MyaCI6IDkuNzAzMjM0NDcyNTI4MjUxLAog
ICAicl94dGFsX0UyIjogMC4wMTM4OTQ5NjEzNDg0OTM1NSwKICAgInJfeHRhbF9oIjogLTAuMDAx
ODQ1MTAxMDE5NDI4NDc0NSwKICAgImxhbWJkYV9tZWFuIjogMC4wMDkzMTA1MDM4NTk2NTI4LAog
ICAibGFtYmRhX21heCI6IDAuMDQzMjkyNzAxOTU0MTIwMDE1LAogICAibGFtYmRhX21heF9icmFu
Y2giOiAicVQyIiwKICAgImNvdl9sYW1iZGFfdiI6IDAuMDcyMjExNzIwODMzODY0MzMsCiAgICJz
aGFyZV9FTSI6IHsKICAgICJxVDEiOiAwLjQ5OTIyNTA1NzU1NTI5NTQ1LAogICAgInFUMiI6IDAu
NDkxNDY0NDM4NTg1MDUxODQsCiAgICAicUwiOiAwLjAwOTMxMDUwMzg1OTY1Mjc4OAogICB9LAog
ICAic2hhcmVfUzJFMiI6IHsKICAgICJxVDEiOiAwLjUzMjk1OTU5NTg0NDE4MTEsCiAgICAicVQy
IjogMC40NTc4NTE0MTkxMDYyNDA1LAogICAgInFMIjogMC4wMDkxODg5ODUwNDk1NzgzODgKICAg
fSwKICAgImRvdWJsaW5nX3JfeHRhbF9FMiI6IDIuMjIwNDQ2MDQ5MjUwMzEzZS0xNgogIH0KIH0s
CiAicGhhc2UyIjogewogICJoZXhfc3RlcHxhIjogewogICAidlRfVlJIIjogOC40MTkwNTk2Mzc1
OTE2MDMsCiAgICJ2VF9WIjogOC41NDc3Nzk0Mzg3MzkyMjgsCiAgICJ2VF9SIjogOC4yODgzNDEw
Mjk5ODM5MjcsCiAgICJ2VF9IU19sbyI6IDguMzkwODU5NzMxNzI4MjQ3LAogICAidlRfSFNfaGki
OiA4LjQyNDU4MjQxOTQwMzQ1NywKICAgInJfYWdnX0UyX1ZSSCI6IFsKICAgIC0wLjAwMDM1OTc3
ODk4Mzg2OTg1MTc0LAogICAgLTguOTk1NDg1NjU5MzI0Mzk4ZS0wNSwKICAgIC0xLjQzOTM4MTk0
ODc4Njc4ODdlLTA1LAogICAgLTMuNTk4NTQ0NzM3MzA0MzY1NWUtMDYsCiAgICAtNS43NTc3NTkw
MDA2OTA3NTRlLTA3LAogICAgMC4wLAogICAgLTUuNzU3ODc2OTA3NDg2MTkyZS0wNywKICAgIC0z
LjU5ODcyODk2NDcxNTQ2OTdlLTA2LAogICAgLTEuNDM5NTI5MzMxMjcwNzgzNWUtMDUsCiAgICAt
OC45OTc3ODg1NjUxMjM3ODhlLTA1LAogICAgLTAuMDAwMzU5OTYzMjMxOTQ0OTgxOSwKICAgIC0w
LjAwMTQ0MDMxMTY2NjY5NzY2OQogICBdLAogICAicl9hZ2dfaF9WUkgiOiBbCiAgICAtNC45NzQ0
MzU2ODU1ODk2NGUtMDcsCiAgICAtMS4yNDkxMjEwNTMyNTk0NzJlLTA3LAogICAgLTIuMDAzOTE2
Mzg4MzgyMjY1M2UtMDgsCiAgICAtNS4wMTQyNDAwMjMxOTMzOTVlLTA5LAogICAgLTguMDI3MDU5
MDE3NDc5MTMyZS0xMCwKICAgIDAuMCwKICAgIC04LjAzMjc2NjY3NDA0ODczZS0xMCwKICAgIC01
LjAyMzE1NzExMjQ4MjU3OWUtMDksCiAgICAtMi4wMTEwNTAwOTMxMjAzMDM1ZS0wOCwKICAgIC0x
LjI2MDI2NzYyMDI2MjIxMmUtMDcsCiAgICAtNS4wNjM2MTM1Mjg0Nzc2MTdlLTA3LAogICAgLTIu
MDQzNjg1MjIxNDk3NzgyZS0wNgogICBdLAogICAicl9hZ2dfRTJfSFMiOiBbCiAgICAtMC4wMDAz
NTcxNDYxMDc5MTQzNzQ1LAogICAgLTguOTI3NDI1NDI0ODQyODE2ZS0wNSwKICAgIC0xLjQyODI2
Nzk5MDk5OTM3NjdlLTA1LAogICAgLTMuNTcwNTY4OTc1NDg2MTMyNWUtMDYsCiAgICAtNS43MTI4
MTMwNDA0MDM4M2UtMDcsCiAgICAwLjAsCiAgICAtNS43MTI2ODI4NjAwOTI4NTVlLTA3LAogICAg
LTMuNTcwMzY1NTY3NTI4OTg4ZS0wNiwKICAgIC0xLjQyODEwNTI2NTA1NTU0NTllLTA1LAogICAg
LTguOTI0ODgyODc5Mzc5NzU5ZS0wNSwKICAgIC0wLjAwMDM1Njk0MjcxNzc0NTU1NjQsCiAgICAt
MC4wMDE0MjczMzYyNTYwNjMzOTQKICAgXSwKICAgInJfYWdnX0UyX1YiOiBbCiAgICAtMC4wMDA0
NDQ4OTM0NTMzMDIyMzA4NSwKICAgIC0wLjAwMDExMTI5NTA2Mjg1ODExODg1LAogICAgLTEuNzgx
NDI1OTY2OTE3OTkzM2UtMDUsCiAgICAtNC40NTQxNTkzNTMxMjg4NzI2ZS0wNiwKICAgIC03LjEy
NzIyODMwNjQyNDk4MmUtMDcsCiAgICAwLjAsCiAgICAtNy4xMjc5OTU4OTM1Mjk5N2UtMDcsCiAg
ICAtNC40NTUzNTg3MDk1MjA4NTFlLTA2LAogICAgLTEuNzgyMzg1NDU2NDA1ODU1ZS0wNSwKICAg
IC0wLjAwMDExMTQ0NDk4Nzk2MDY3MzgxLAogICAgLTAuMDAwNDQ2MDkyOTkzMzk3MjYyNCwKICAg
IC0wLjAwMTc4Njk4MzMxMDQ4NzEwMDIKICAgXSwKICAgInJfYWdnX0UyX1IiOiBbCiAgICAtMC4w
MDAyNjkyMTYwMDU4MDA2NTQzLAogICAgLTYuNzI1MjQ4OTA0MDYwMzQ0ZS0wNSwKICAgIC0xLjA3
NTU1MzE5NjcxNjU5NDNlLTA1LAogICAgLTIuNjg4NDgwNzU0OTA4Nzk1MmUtMDYsCiAgICAtNC4z
MDExODQzMjMxNTIxODVlLTA3LAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIC00LjMw
MDY3MjYxMzU4ODU3NGUtMDcsCiAgICAtMi42ODc2ODEyMDg1OTA3NTNlLTA2LAogICAgLTEuMDc0
OTEzNTU5NjA2NjQ5NWUtMDUsCiAgICAtNi43MTUyNTQ1NTQ1Njc4OTVlLTA1LAogICAgLTAuMDAw
MjY4NDE2NDUyMTM3Mzc2NjQsCiAgICAtMC4wMDEwNzIxNjUxOTA1NDY4Njk5CiAgIF0sCiAgICJT
X3RfRTIiOiAxLjYyNjYyMzEyNTYyNjE2OTZlLTEzLAogICAiU190X2giOiA0LjU2Mzk0MTA1NTE3
Njg1M2UtMTUsCiAgICJrYXBwYTJfRTIiOiAtMC4wMDE0Mzk0NjE3Njk0OTY2OTkyLAogICAia2Fw
cGEyX2giOiAtMi4wMDc1MTAxOTgxNjM3NjU1ZS0wNiwKICAgImthcHBhM19FMiI6IC03LjM2OTMy
NDQ1ODIwNzQ5OGUtMDcsCiAgICJrYXBwYTJfRTJfSFMiOiAtMC4wMDE0MjgxODQ3MTY4NjMzOTY2
LAogICAia2FwcGEyX0UyXzR0ZXJtIjogLTAuMDAxNDM5NDU0NDQwNDMwMDcyMSwKICAgIlNfdF9F
Ml80dGVybSI6IDEuNjI2NTc5MDAyMTcyMDM5NGUtMTMsCiAgICJrYXBwYTRfRTJfNHRlcm0iOiAt
MS4xOTk2MDQxMjIzNzc3MzA0ZS0wNywKICAgImZpdF9yZXNpZHVhbCI6IDMuMDQ5NjUzNTc4MTIz
NThlLTExLAogICAiZml0X3Jlc2lkdWFsXzR0ZXJtIjogMy4zOTczNjE2Njk0MDE2Mzg1ZS0xNSwK
ICAgImhhbHZpbmdfZGV2X2thcHBhMiI6IDQuMjk2MDc3MTkxMDg5MjIzZS0wNiwKICAgImthcHBh
Ml9FMl93aW5kb3cwcDEiOiAtMC4wMDE0Mzk0NTU1ODU0NTc4MjM4LAogICAibGFtYmRhX21lYW5f
dCI6IFsKICAgIDIuNTExMTkwNjM2MDkyNDU1NWUtMDYsCiAgICA2LjI4Mzg1MjM3OTg0Mzg3NWUt
MDcsCiAgICAxLjAwNTk5NTE4NTE2NTQ3ODRlLTA3LAogICAgMi41MTU0NzY0NDAyOTA3MzU1ZS0w
OCwKICAgIDQuMDI1MjMzNjAxNTg4MDA4ZS0wOSwKICAgIDEuODE2NzM3ODg2NDEyNDkxN2UtMzAs
CiAgICA0LjAyNTg2NDc1MDAyNzMxOGUtMDksCiAgICAyLjUxNjQ2MjYxMDAwMzM1OTZlLTA4LAog
ICAgMS4wMDY3ODQxMjE1MjM4MzY3ZS0wNywKICAgIDYuMjk2MTc5NTc4NzczOTA4ZS0wNywKICAg
IDIuNTIxMDUyNTkwNjU2NzcxZS0wNiwKICAgIDEuMDEwNTc4MTc3MTU0NTA5NWUtMDUKICAgXSwK
ICAgImhzX3JlZiI6IHsKICAgICJoaSI6IFsKICAgICAxMzUuMzY2NTk1MjgzNjk3NjIsCiAgICAg
MTE1LjU1OTg3MzI4OTE5OTAyCiAgICBdLAogICAgImxvIjogWwogICAgIDEzNC42MDcwODk0Mzcx
MjYwNiwKICAgICA2MC4wMzA4MDAwMDE0Mzc5NwogICAgXQogICB9CiAgfSwKICAiaGV4X3N0ZXB8
YiI6IHsKICAgInZUX1ZSSCI6IDguNDE5Mjc4NjQ4NTc5NjEyLAogICAidlRfViI6IDguNTQ3OTgy
OTk3OTU1Mjk1LAogICAidlRfUiI6IDguMjg4NTc2MDI5MTgxNjI3LAogICAidlRfSFNfbG8iOiA4
LjM5MTA4NDc0NjgzNzk0NywKICAgInZUX0hTX2hpIjogOC40MjQ4MDMyNTc3MjM4MzIsCiAgICJy
X2FnZ19FMl9WUkgiOiBbCiAgICAtMC4wMDAzNTk1ODkyMDU5NzMzNDMsCiAgICAtOC45OTA3NDE1
MjgwOTIwOTRlLTA1LAogICAgLTEuNDM4NjIyOTA1MTU4ODM3M2UtMDUsCiAgICAtMy41OTY2NDcx
MzczMzgzMTU4ZS0wNiwKICAgIC01Ljc1NDcyMjg0ODI1MDE4MmUtMDcsCiAgICAwLjAsCiAgICAt
NS43NTQ4NDA3NjA1OTY3MzZlLTA3LAogICAgLTMuNTk2ODMxMzc0NjMwNDA1ZS0wNiwKICAgIC0x
LjQzODc3MDI5NTYzNjQzNzllLTA1LAogICAgLTguOTkzMDQ0NTU4MTkyMDU0ZS0wNSwKICAgIC0w
LjAwMDM1OTc3MzQ2Mzk3NjUzMTU0LAogICAgLTAuMDAxNDM5NTUyNDUxNjQzNAogICBdLAogICAi
cl9hZ2dfaF9WUkgiOiBbCiAgICAtNC45NjkyMzM1NTc5NzIwNzVlLTA3LAogICAgLTEuMjQ3ODEy
NDIxMTY3ODkzMWUtMDcsCiAgICAtMi4wMDE4MTQ3Njk1MDMzNDA2ZS0wOCwKICAgIC01LjAwODk3
OTAwOTM0NjYwMzZlLTA5LAogICAgLTguMDE4NjM0NjQ1MTY4Mjc3ZS0xMCwKICAgIDAuMCwKICAg
IC04LjAyNDMzNDUzMDE3NjcwMmUtMTAsCiAgICAtNS4wMTc4ODI4ODY5ODE3OTVlLTA5LAogICAg
LTIuMDA4OTM3ODcxNjExNDkzNmUtMDgsCiAgICAtMS4yNTg5NDI0OTQ2OTczNzkzZS0wNywKICAg
IC01LjA1ODI3OTQxOTc2NzMzMWUtMDcsCiAgICAtMi4wNDE1MjQxODAwNDA4ODhlLTA2CiAgIF0s
CiAgICJyX2FnZ19FMl9IUyI6IFsKICAgIC0wLjAwMDM1Njk1NDY4OTYxMDE2NzIsCiAgICAtOC45
MjI2NDExMjkyOTQxOTVlLTA1LAogICAgLTEuNDI3NTAyNjE4ODg5MjQyNmUtMDUsCiAgICAtMy41
Njg2NTU2NDI4ODI2Njc3ZS0wNiwKICAgIC01LjcwOTc1MTgwMzU4NDI0ZS0wNywKICAgIDAuMCwK
ICAgIC01LjcwOTYyMTc0NTM5Nzc5N2UtMDcsCiAgICAtMy41Njg0NTI0MzIxMDExMzI0ZS0wNiwK
ICAgIC0xLjQyNzM0MDA1MDc1MjUxMjVlLTA1LAogICAgLTguOTIwMTAxMDQ5MjE0NTllLTA1LAog
ICAgLTAuMDAwMzU2NzUxNDk2NjM5NzE3ODQsCiAgICAtMC4wMDE0MjY1NzE4MTA1MjU5NjczCiAg
IF0sCiAgICJyX2FnZ19FMl9WIjogWwogICAgLTAuMDAwNDQ0NzAyNjMxNjAwNzkwNywKICAgIC0w
LjAwMDExMTI0NzI5NzQ3MzI0OTI0LAogICAgLTEuNzgwNjYxMTIzNzUxNDE0N2UtMDUsCiAgICAt
NC40NTIyNDY3Mzg4Mzk3MDVlLTA2LAogICAgLTcuMTI0MTY3NjMyNDg4NDY1ZS0wNywKICAgIDAu
MCwKICAgIC03LjEyNDkzNDU2MjM0MTQyM2UtMDcsCiAgICAtNC40NTM0NDUwNjg2MDg0NTI2ZS0w
NiwKICAgIC0xLjc4MTYxOTc5MjA2MjgxNjNlLTA1LAogICAgLTAuMDAwMTExMzk3MDk0MjU4NjY5
NSwKICAgIC0wLjAwMDQ0NTkwMTE0NDkxNzE2MDE1LAogICAgLTAuMDAxNzg2MjEzNTg4MzQ3OTYy
NAogICBdLAogICAicl9hZ2dfRTJfUiI6IFsKICAgIC0wLjAwMDI2OTAyODE0ODgwMzY5NjEsCiAg
ICAtNi43MjA1NTk3ODY5NzY4MzJlLTA1LAogICAgLTEuMDc0ODAzNjIzMDI0NTg5NGUtMDUsCiAg
ICAtMi42ODY2MDczODQ4OTQxMjRlLTA2LAogICAgLTQuMjk4MTg3NDY5Mjc2MDE2ZS0wNywKICAg
IC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAtNC4yOTc2NzY0NzQ2OTYwMzNlLTA3LAogICAg
LTIuNjg1ODA4OTU2NDU5NjQ1NWUtMDYsCiAgICAtMS4wNzQxNjQ4ODAyMjE0OTU0ZS0wNSwKICAg
IC02LjcxMDU3OTQxMDA1MTkzMWUtMDUsCiAgICAtMC4wMDAyNjgyMjk3MTI5NTk4MTEsCiAgICAt
MC4wMDEwNzE0MjAyNjM5Njg1NTg4CiAgIF0sCiAgICJTX3RfRTIiOiAxLjYxMjUwMzQ2NTg2MTYz
MTNlLTEzLAogICAiU190X2giOiA2LjU1MDA4Nzg1ODg3NDk3NmUtMTUsCiAgICJrYXBwYTJfRTIi
OiAtMC4wMDE0Mzg3MDI3MTg3NDkwODMsCiAgICJrYXBwYTJfaCI6IC0yLjAwNTQwMzE5NDExMjc5
MTZlLTA2LAogICAia2FwcGEzX0UyIjogLTcuMzY5NzIxOTk2NTc0NzQ0ZS0wNywKICAgImthcHBh
Ml9FMl9IUyI6IC0wLjAwMTQyNzQxOTQyNjcyMjEyMjYsCiAgICJrYXBwYTJfRTJfNHRlcm0iOiAt
MC4wMDE0Mzg2OTU0MDI5NzM5NTEzLAogICAiU190X0UyXzR0ZXJtIjogMS42MTI0NTkzNjU2Njgx
NzU4ZS0xMywKICAgImthcHBhNF9FMl80dGVybSI6IC0xLjE5NzQyODYwMjE0NTYxNzFlLTA3LAog
ICAiZml0X3Jlc2lkdWFsIjogMy4wNDQxMjI5MzI4MTYyN2UtMTEsCiAgICJmaXRfcmVzaWR1YWxf
NHRlcm0iOiAzLjMzMDg4MDgzNTIxMzAxMmUtMTUsCiAgICJoYWx2aW5nX2Rldl9rYXBwYTIiOiA0
LjI5MDU0ODU1NjE4NzQ1M2UtMDYsCiAgICJrYXBwYTJfRTJfd2luZG93MHAxIjogLTAuMDAxNDM4
Njk2NTQ1OTI1MjEwNCwKICAgImxhbWJkYV9tZWFuX3QiOiBbCiAgICAyLjUwODY0MjIxMzA4OTI3
MjNlLTA2LAogICAgNi4yNzc0NzQ1NDAyNDYwMDVlLTA3LAogICAgMS4wMDQ5NzQwNDE0MzU4MTI4
ZS0wNywKICAgIDIuNTEyOTIyOTkwNjI0ODg3ZS0wOCwKICAgIDQuMDIxMTQ3NTA5Mjc1MzM2ZS0w
OSwKICAgIDIuODQ5MzA4Nzk3OTUyNTUwN2UtMzAsCiAgICA0LjAyMTc3Nzg4Njk4MDY5NjVlLTA5
LAogICAgMi41MTM5MDc5NTUzNTQyMjM4ZS0wOCwKICAgIDEuMDA1NzYyMDEzOTQxMDg1ZS0wNywK
ICAgIDYuMjg5Nzg2Njc4NzM1ODA0ZS0wNywKICAgIDIuNTE4NDkyMTE4Njc3MTA1NWUtMDYsCiAg
ICAxLjAwOTU1MTA5NzkzMjg3MTVlLTA1CiAgIF0sCiAgICJoc19yZWYiOiB7CiAgICAiaGkiOiBb
CiAgICAgMTM1LjM2NjU5NTI4MzY5NzYyLAogICAgIDExNS41NTk4NzMyODkxOTkwMgogICAgXSwK
ICAgICJsbyI6IFsKICAgICAxMzQuNjA3MDg5NDM3MTI2MDYsCiAgICAgNjAuMDMwODAwMDAxNDM3
OTcKICAgIF0KICAgfQogIH0sCiAgImhleF9nZW04fGEiOiB7CiAgICJ2VF9WUkgiOiAxMC4wNDE3
MjE4MTczNjkxNDcsCiAgICJ2VF9WIjogMTAuMjQ4OTk3Njc0NTY5NTk2LAogICAidlRfUiI6IDku
ODMwMDc2MzM2NTA1MzI5LAogICAidlRfSFNfbG8iOiA5Ljk5MDkxMzAwMTU3MTE1NiwKICAgInZU
X0hTX2hpIjogMTAuMDUyNzk3NzU0OTQ5MDM3LAogICAicl9hZ2dfRTJfVlJIIjogWwogICAgLTAu
MDAwNDczNzcwMDc5NjcxMTk4NTUsCiAgICAtMC4wMDAxMTg0NTg2NzA2MjQzMjE4LAogICAgLTEu
ODk1NTEwMzEwNTQ1NTc4NGUtMDUsCiAgICAtNC43Mzg5MjU2NTk2NjQxNjE2ZS0wNiwKICAgIC03
LjU4MjQyNzU5NDY4Nzg1N2UtMDcsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgLTcu
NTgyNjI2MDc1OTE5MzA4ZS0wNywKICAgIC00LjczOTIzNTc4NTM2NzA1NzVlLTA2LAogICAgLTEu
ODk1NzU4NDEyNjczMzA5NmUtMDUsCiAgICAtMC4wMDAxMTg0OTc0MzgyMjE0NTQzMSwKICAgIC0w
LjAwMDQ3NDA4MDI2NzI2MjQ3Nzc2LAogICAgLTAuMDAxODk3MTQ5NTU5NDEyMzM2NwogICBdLAog
ICAicl9hZ2dfaF9WUkgiOiBbCiAgICAtOC4wMzg3NzA1ODU4NjA4ODhlLTA3LAogICAgLTIuMDIw
MTk3NzM0NjUzNDUwNWUtMDcsCiAgICAtMy4yNDI0ODgyMDAxNjEzNzVlLTA4LAogICAgLTguMTE0
NzMzNzczODIyOTllLTA5LAogICAgLTEuMjk5MTc2MjExMDU1OTA4ZS0wOSwKICAgIDAuMCwKICAg
IC0xLjMwMDI2OTIyNTYyMzY1MTRlLTA5LAogICAgLTguMTMxODE1NTU0MjU3NTcxZS0wOSwKICAg
IC0zLjI1NjE1MzcwMjIyNDY1MWUtMDgsCiAgICAtMi4wNDE1NTA3MzczNTI3OTNlLTA3LAogICAg
LTguMjA5NjEzNDQ2ODMwMTMzZS0wNywKICAgIC0zLjMxOTE1NzA4NDczNTczNTVlLTA2CiAgIF0s
CiAgICJyX2FnZ19FMl9IUyI6IFsKICAgIC0wLjAwMDQ3MTQ3MjE4Nzk0MDE5MTc0LAogICAgLTAu
MDAwMTE3ODUwMTk5ODY3MzE5ODIsCiAgICAtMS44ODU0MjY2MzQ4Mjg5MzVlLTA1LAogICAgLTQu
NzEzNDE3MjgxODA5NzRlLTA2LAogICAgLTcuNTQxMzIzNDg3OTAyOTI5ZS0wNywKICAgIC0yLjIy
MDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAtNy41NDExMzAzMDAyMTQ4NmUtMDcsCiAgICAtNC43MTMx
MTU0MjY3MTMyNjZlLTA2LAogICAgLTEuODg1MTg1MTUyMDcyOTIxM2UtMDUsCiAgICAtMC4wMDAx
MTc4MTI0Njk2NDczNzE0NiwKICAgIC0wLjAwMDQ3MTE3MDM4ODAxNTgwNjksCiAgICAtMC4wMDE4
ODQwMTM4MTIwNDY3MjU0CiAgIF0sCiAgICJyX2FnZ19FMl9WIjogWwogICAgLTAuMDAwNTgxNjYw
MzE1NDEyOTU3NCwKICAgIC0wLjAwMDE0NTUzNDkwOTgwMDYyNjQ0LAogICAgLTIuMzI5NzQ2MjEz
NjAyOTM0NWUtMDUsCiAgICAtNS44MjUzNzA4NzQ1NjgxMzY1ZS0wNiwKICAgIC05LjMyMTU2NDU0
NjkxNTc5NWUtMDcsCiAgICAwLjAsCiAgICAtOS4zMjI4NjY0Mzk5NTM2MTRlLTA3LAogICAgLTUu
ODI3NDA1MDg5Njk3ODEyNWUtMDYsCiAgICAtMi4zMzEzNzM1OTg4MDczMDdlLTA1LAogICAgLTAu
MDAwMTQ1Nzg5MjAyOTI3MjkzMzYsCiAgICAtMC4wMDA1ODM2OTUwNjU5ODYyMTE3LAogICAgLTAu
MDAyMzM5MzI4MDEwNTg2ODk0CiAgIF0sCiAgICJyX2FnZ19FMl9SIjogWwogICAgLTAuMDAwMzU2
NDM0ODE2NTQ1NDU4OTQsCiAgICAtOC45MDE3MjM1MDQ0NzMwNDdlLTA1LAogICAgLTEuNDIzNDE1
ODU5MTAzMTA1NGUtMDUsCiAgICAtMy41NTc4MzA2NDE5ODcwMDNlLTA2LAogICAgLTUuNjkxODUx
MjkyNTEwODE5ZS0wNywKICAgIDIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIC01LjY5MDk1MTAz
OTMwNTUwM2UtMDcsCiAgICAtMy41NTY0MjM5OTM5NjY3MTc1ZS0wNiwKICAgIC0xLjQyMjI5MDU0
MDIzMTY4NTRlLTA1LAogICAgLTguODg0MTQwMzQxMjY5ODNlLTA1LAogICAgLTAuMDAwMzU1MDI4
MTQ3NDg0NjcwNiwKICAgIC0wLjAwMTQxNzUyNjM3MzQxMDg2CiAgIF0sCiAgICJTX3RfRTIiOiA0
Ljg5NDY0MjM2NTE0NTM5NmUtMTMsCiAgICJTX3RfaCI6IDEuOTg0OTI1Mjc1OTQyNjgzNmUtMTQs
CiAgICJrYXBwYTJfRTIiOiAtMC4wMDE4OTU2NDg0ODI2NzAxMzUyLAogICAia2FwcGEyX2giOiAt
My4yNDkzOTY2OTU5Mjg5NDYzZS0wNiwKICAgImthcHBhM19FMiI6IC0xLjI0MDU3MDkwMTgwNDM4
ZS0wNiwKICAgImthcHBhMl9FMl9IUyI6IC0wLjAwMTg4NTMwMTQ3NzQ4MzkxNTUsCiAgICJrYXBw
YTJfRTJfNHRlcm0iOiAtMC4wMDE4OTU2MzE1OTc5NzE2NzMsCiAgICJTX3RfRTJfNHRlcm0iOiA0
Ljg5NDU4NDI1ODI3NzA2M2UtMTMsCiAgICJrYXBwYTRfRTJfNHRlcm0iOiAtMi43NjM2NDcxMjA2
MjU0ODNlLTA3LAogICAiZml0X3Jlc2lkdWFsIjogNy4wMjU3ODk3NjQ4OTg0NDVlLTExLAogICAi
Zml0X3Jlc2lkdWFsXzR0ZXJtIjogMS4wMjE0NzAwNjAzMzA0OTY1ZS0xNCwKICAgImhhbHZpbmdf
ZGV2X2thcHBhMiI6IDcuNTE1NTE5OTQ1MzI5NTNlLTA2LAogICAia2FwcGEyX0UyX3dpbmRvdzBw
MSI6IC0wLjAwMTg5NTYzNDIzNTg4NjE1NDQsCiAgICJsYW1iZGFfbWVhbl90IjogWwogICAgMy42
MDA2NjM0OTQ2MjQ3OTg2ZS0wNiwKICAgIDkuMDExODYzNjAxODA5MzAxZS0wNywKICAgIDEuNDQy
OTE1NzU3NjUwOTIzM2UtMDcsCiAgICAzLjYwODE1MzE5MzQwNjc0N2UtMDgsCiAgICA1Ljc3Mzg4
MDQzMzU4ODIzOGUtMDksCiAgICAyLjg3MzA2MjQzODA3MDUzMDJlLTMwLAogICAgNS43NzUwMDEy
OTE0NDAwOTFlLTA5LAogICAgMy42MDk5MDQ1MzQ2NzY0NjQzZS0wOCwKICAgIDEuNDQ0MzE2ODMz
NjYzODg1ZS0wNywKICAgIDkuMDMzNzU1NzQ0NjQ1OTIzZS0wNywKICAgIDMuNjE4MTc4MTUyNzAz
ODA5ZS0wNiwKICAgIDEuNDUxMjUxMjE0MTAzMzYyOGUtMDUKICAgXSwKICAgImhzX3JlZiI6IHsK
ICAgICJoaSI6IFsKICAgICAyMzAuMTM2MDQ4MzkwNzMxMywKICAgICAxNzguMjk0MzQxNzU1NzY3
NjUKICAgIF0sCiAgICAibG8iOiBbCiAgICAgMjI5LjY5NTc1NDMzNTg2NTc2LAogICAgIDg0Ljgy
NDUwMDAwMjMxMDkxCiAgICBdCiAgIH0KICB9LAogICJoZXhfZ2VtOHxiIjogewogICAidlRfVlJI
IjogMTAuMDQxNTU0MDg1MTYwNjMyLAogICAidlRfViI6IDEwLjI0ODg0NzQxNDg3MjIzNCwKICAg
InZUX1IiOiA5LjgyOTg5MDMxMjU2NjAxLAogICAidlRfSFNfbG8iOiA5Ljk5MDczOTgyOTcxOTg2
LAogICAidlRfSFNfaGkiOiAxMC4wNTI2Mjk5NTkyOTQ5NDUsCiAgICJyX2FnZ19FMl9WUkgiOiBb
CiAgICAtMC4wMDA0NzM4OTIzNDAzMTIwMzIxLAogICAgLTAuMDAwMTE4NDg5MjMyNTI3NTUyMTcs
CiAgICAtMS44OTU5OTkyODQzODQ3NzVlLTA1LAogICAgLTQuNzQwMTQ4MDg2NDkwNTkyZS0wNiwK
ICAgIC03LjU4NDM4MzQ3NDU5MDMzOWUtMDcsCiAgICAwLjAsCiAgICAtNy41ODQ1ODE5NDY5NDAw
MDZlLTA3LAogICAgLTQuNzQwNDU4MjA1OTc2MjM5ZS0wNiwKICAgIC0xLjg5NjI0NzM4MTUxNjUw
MjZlLTA1LAogICAgLTAuMDAwMTE4NTI3OTk5MzQyOTc2NjQsCiAgICAtMC4wMDA0NzQyMDI1MjE2
NzY4NDc1LAogICAgLTAuMDAxODk3NjM4NzQ4NzkyNDUxOAogICBdLAogICAicl9hZ2dfaF9WUkgi
OiBbCiAgICAtOC4wNDI1NjE1Nzc4MjU2OGUtMDcsCiAgICAtMi4wMjExNTIzODMyMzU4NThlLTA3
LAogICAgLTMuMjQ0MDIyMzYxODQ3OTUzNmUtMDgsCiAgICAtOC4xMTg1NzQ3MDEzOTg5ODRlLTA5
LAogICAgLTEuMjk5NzkxMTYzNTg5MjQ3OGUtMDksCiAgICAwLjAsCiAgICAtMS4zMDA4ODQ5NTUz
MTMxMDg1ZS0wOSwKICAgIC04LjEzNTY2ODAyODE1MzAyZS0wOSwKICAgIC0zLjI1NzY5Njk2Nzc0
MDAzMTRlLTA4LAogICAgLTIuMDQyNTE5NTg0NTc3NDYyNGUtMDcsCiAgICAtOC4yMTM1MTgwNTkw
MTkyNjVlLTA3LAogICAgLTMuMzIwNzQzMDAyOTEwMjk4ZS0wNgogICBdLAogICAicl9hZ2dfRTJf
SFMiOiBbCiAgICAtMC4wMDA0NzE1OTU4OTk4Njc1NjA3LAogICAgLTAuMDAwMTE3ODgxMTIwNzE3
NDIyNCwKICAgIC0xLjg4NTkyMTI5NTg2MzI5MWUtMDUsCiAgICAtNC43MTQ2NTM4NzIzMDY0MDdl
LTA2LAogICAgLTcuNTQzMzAxOTY5NzI1NzQ2ZS0wNywKICAgIC0zLjMzMDY2OTA3Mzg3NTQ2OTZl
LTE2LAogICAgLTcuNTQzMTA4NzA1NDMyMjg5ZS0wNywKICAgIC00LjcxNDM1MTg5MDIwMDQxOWUt
MDYsCiAgICAtMS44ODU2Nzk3MTE1MTA3NjgyZS0wNSwKICAgIC0wLjAwMDExNzg0MzM3NDYzMjE2
NDk5LAogICAgLTAuMDAwNDcxMjkzOTczMDY3MTEwNjMsCiAgICAtMC4wMDE4ODQ1MDc4NDgzMzQx
NjA0CiAgIF0sCiAgICJyX2FnZ19FMl9WIjogWwogICAgLTAuMDAwNTgxNzgxNzE5MzAxNjc3MiwK
ICAgIC0wLjAwMDE0NTU2NTMwOTcxMjU0NzU1LAogICAgLTIuMzMwMjMzMTA1Mjc0MzU5N2UtMDUs
CiAgICAtNS44MjY1ODg1MjQyMTU5MTRlLTA2LAogICAgLTkuMzIzNTEzMTkzNzE1MjcyZS0wNywK
ICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAtOS4zMjQ4MTU2MzYzMTM0ODhlLTA3LAog
ICAgLTUuODI4NjIzNTk1NTQ5NTg3ZS0wNiwKICAgIC0yLjMzMTg2MTE3NTI5NzYwMDRlLTA1LAog
ICAgLTAuMDAwMTQ1ODE5NzA5ODU2Mjc2MzUsCiAgICAtMC4wMDA1ODM4MTczMjYzNDkyNjc0LAog
ICAgLTAuMDAyMzM5ODE5MDY1ODY3ODg3NQogICBdLAogICAicl9hZ2dfRTJfUiI6IFsKICAgIC0w
LjAwMDM1NjU1NzAyMjkzMzgwMTEsCiAgICAtOC45MDQ3NzIzMDAxMTEyMTllLTA1LAogICAgLTEu
NDIzOTAzMDc0MTQ5MTkxZS0wNSwKICAgIC0zLjU1OTA0ODE5MzgyNDEzMjVlLTA2LAogICAgLTUu
NjkzNzk4OTEyMzUzOTk4ZS0wNywKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAtNS42
OTI4OTgwNDI5NzQ5MDNlLTA3LAogICAgLTMuNTU3NjQwNTg1NjgyOTc1ZS0wNiwKICAgIC0xLjQy
Mjc3Njk4NzM0NzYwN2UtMDUsCiAgICAtOC44ODcxNzcxMzgwMTcyMzNlLTA1LAogICAgLTAuMDAw
MzU1MTQ5MzkzOTM4NTQ3NSwKICAgIC0wLjAwMTQxODAwOTY3MjM1NTYxMzUKICAgXSwKICAgIlNf
dF9FMiI6IDQuODk1NzUxNTI5MzYxMDk4ZS0xMywKICAgIlNfdF9oIjogMS44NjE3NTQ0MDM1OTcx
MzJlLTE0LAogICAia2FwcGEyX0UyIjogLTAuMDAxODk2MTM3NDY2NTI0MjI2NCwKICAgImthcHBh
Ml9oIjogLTMuMjUwOTM1NDkwMzA2MTE2N2UtMDYsCiAgICJrYXBwYTNfRTIiOiAtMS4yNDA1NDU4
ODkxMDQ3ODZlLTA2LAogICAia2FwcGEyX0UyX0hTIjogLTAuMDAxODg1Nzk2MDg0MjU4MzA4OCwK
ICAgImthcHBhMl9FMl80dGVybSI6IC0wLjAwMTg5NjEyMDU2Njg2MjMyNiwKICAgIlNfdF9FMl80
dGVybSI6IDQuODk1NjkzNDA3NDk2ODcyZS0xMywKICAgImthcHBhNF9FMl80dGVybSI6IC0yLjc2
NjA5NjMwMDUxMTYwNWUtMDcsCiAgICJmaXRfcmVzaWR1YWwiOiA3LjAzMjAxNjExMDIxMDg5MWUt
MTEsCiAgICJmaXRfcmVzaWR1YWxfNHRlcm0iOiAxLjAxNjMxMDY0MDE1MTYxOTJlLTE0LAogICAi
aGFsdmluZ19kZXZfa2FwcGEyIjogNy41MjAyNDAzNTc4MjczNDVlLTA2LAogICAia2FwcGEyX0Uy
X3dpbmRvdzBwMSI6IC0wLjAwMTg5NjEyMzIwNzExNDcyNjYsCiAgICJsYW1iZGFfbWVhbl90Ijog
WwogICAgMy42MDIyODgzMjQwNzcwNzY0ZS0wNiwKICAgIDkuMDE1OTMwMjQ4MjQ3ODQyZS0wNywK
ICAgIDEuNDQzNTY2OTA2NTA1NTA0NmUtMDcsCiAgICAzLjYwOTc4MTQ4OTU3NTYwOGUtMDgsCiAg
ICA1Ljc3NjQ4NjEyMTY2Njg2NTZlLTA5LAogICAgMS4yODQyNDkwNzc2MjgwOTc1ZS0zMSwKICAg
IDUuNzc3NjA3NTQwMzU3ODA3ZS0wOSwKICAgIDMuNjExNTMzNzA3NjA0MzU3ZS0wOCwKICAgIDEu
NDQ0OTY4Njg0MDE0NzI5MmUtMDcsCiAgICA5LjAzNzgzMzM1MjIzOTQzOGUtMDcsCiAgICAzLjYx
OTgxMTc1MjIxMDQ5MzVlLTA2LAogICAgMS40NTE5MDY5OTI0Mjc0MDI5ZS0wNQogICBdLAogICAi
aHNfcmVmIjogewogICAgImhpIjogWwogICAgIDIzMC4xMzYwNDgzOTA3MzEzLAogICAgIDE3OC4y
OTQzNDE3NTU3Njc2NQogICAgXSwKICAgICJsbyI6IFsKICAgICAyMjkuNjk1NzU0MzM1ODY1NzYs
CiAgICAgODQuODI0NTAwMDAyMzEwOTEKICAgIF0KICAgfQogIH0sCiAgImN1YmljX3N0ZXB8MDAx
IjogewogICAidlRfVlJIIjogNy43OTkwNDYzNzU4NDQ5MjMsCiAgICJ2VF9WIjogOC4xMTU3OTQ0
Nzc0MzcxOTUsCiAgICJ2VF9SIjogNy40Njg4NzczNDE2ODY2MDcsCiAgICJ2VF9IU19sbyI6IDcu
NzU4NjE0NDkwMjExMDg3LAogICAidlRfSFNfaGkiOiA3Ljg2Nzk1MzAwNTkwNDc3NSwKICAgInJf
YWdnX0UyX1ZSSCI6IFsKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAyLjIyMDQ0NjA0
OTI1MDMxM2UtMTYsCiAgICAtMS4xMTAyMjMwMjQ2MjUxNTY1ZS0xNiwKICAgIC0xLjExMDIyMzAy
NDYyNTE1NjVlLTE2LAogICAgLTEuMTEwMjIzMDI0NjI1MTU2NWUtMTYsCiAgICAwLjAsCiAgICAw
LjAsCiAgICAwLjAsCiAgICAtMS4xMTAyMjMwMjQ2MjUxNTY1ZS0xNiwKICAgIDIuMjIwNDQ2MDQ5
MjUwMzEzZS0xNiwKICAgIDAuMCwKICAgIC0xLjExMDIyMzAyNDYyNTE1NjVlLTE2CiAgIF0sCiAg
ICJyX2FnZ19oX1ZSSCI6IFsKICAgIDAuMCwKICAgIDAuMCwKICAgIDAuMCwKICAgIC0xLjExMDIy
MzAyNDYyNTE1NjVlLTE2LAogICAgMC4wLAogICAgMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAg
MC4wLAogICAgMC4wLAogICAgMC4wLAogICAgMC4wLAogICAgMC4wLAogICAgMC4wCiAgIF0sCiAg
ICJyX2FnZ19FMl9IUyI6IFsKICAgIDIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIDAuMCwKICAg
IDIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAw
LjAsCiAgICAtMS4xMTAyMjMwMjQ2MjUxNTY1ZS0xNiwKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2Ut
MTYsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgMi4yMjA0NDYwNDkyNTAzMTNlLTE2
LAogICAgLTEuMTEwMjIzMDI0NjI1MTU2NWUtMTYsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2
LAogICAgMC4wCiAgIF0sCiAgICJyX2FnZ19FMl9WIjogWwogICAgMC4wLAogICAgMC4wLAogICAg
MC4wLAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIDAuMCwKICAgIC0yLjIyMDQ0NjA0
OTI1MDMxM2UtMTYsCiAgICAwLjAsCiAgICAwLjAsCiAgICAwLjAsCiAgICAwLjAsCiAgICAyLjIy
MDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAwLjAKICAgXSwKICAgInJfYWdnX0UyX1IiOiBbCiAgICAw
LjAsCiAgICAtMS4xMTAyMjMwMjQ2MjUxNTY1ZS0xNiwKICAgIC0xLjExMDIyMzAyNDYyNTE1NjVl
LTE2LAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIDAuMCwKICAgIDAuMCwKICAgIC0x
LjExMDIyMzAyNDYyNTE1NjVlLTE2LAogICAgMC4wLAogICAgMC4wLAogICAgLTIuMjIwNDQ2MDQ5
MjUwMzEzZS0xNiwKICAgIC0xLjExMDIyMzAyNDYyNTE1NjVlLTE2LAogICAgMC4wCiAgIF0sCiAg
ICJTX3RfRTIiOiAzLjg3MjY5OTY0OTgwMDUwMmUtMTYsCiAgICJTX3RfaCI6IDIuNzM4MTc2MDUw
OTc0Nzg3N2UtMTYsCiAgICJrYXBwYTJfRTIiOiAzLjE0MTcwMjEyMzkzMjQxNmUtMTUsCiAgICJr
YXBwYTJfaCI6IC0zLjQ1ODUwMDc5NjkzMTQwMWUtMTcsCiAgICJrYXBwYTNfRTIiOiAtNi4zMDg2
MjY4ODkyMjI1NDVlLTE1LAogICAia2FwcGEyX0UyX0hTIjogLTQuNjA2NzIzMDYxNTEyNTIxZS0x
NiwKICAgImthcHBhMl9FMl80dGVybSI6IC0xLjQ4NjA3NDE0ODE4MDEyNjhlLTE0LAogICAiU190
X0UyXzR0ZXJtIjogMy44NzI2OTk2NDk4MDA1NzhlLTE2LAogICAia2FwcGE0X0UyXzR0ZXJtIjog
Mi45NDY1OTY5NzY0NDkyNTRlLTEzLAogICAiZml0X3Jlc2lkdWFsIjogOC41NDkzNzQ2ODc1ODc1
NDhlLTE3LAogICAiZml0X3Jlc2lkdWFsXzR0ZXJtIjogNC4xMjA0ODYyMTI3MjQyNDM3ZS0xNywK
ICAgImhhbHZpbmdfZGV2X2thcHBhMiI6IDQuODAyNDkxNjM3ODQxNzMyLAogICAia2FwcGEyX0Uy
X3dpbmRvdzBwMSI6IC0xLjE5NDYyOTYwNTQ4NDI2MmUtMTQsCiAgICJsYW1iZGFfbWVhbl90Ijog
WwogICAgMi44MTEyNjE1MTc0Mjc4NjI2ZS0zMCwKICAgIDEuOTA3OTA2MzE4MzkyNjQyM2UtMzEs
CiAgICAyLjUzNDkyMDQ4NTQ0NzM0MWUtMzAsCiAgICAxLjk3OTg4NTI1NzU1OTY3MmUtMzAsCiAg
ICAyLjE3MzYyOTQ3NzU1NzMzNmUtMzAsCiAgICA0LjI1ODM5MjI5MTA2OTY5NGUtMzIsCiAgICA3
LjA4MzEzNzMzNTE5Mzk3NWUtMzEsCiAgICAyLjg5NzkzODY4MTc0MTQ0NzVlLTMxLAogICAgMi4x
MDY1NjQwODg1MDQyNDRlLTMxLAogICAgNC45NzUyMTY2ODk4MzIxMzNlLTMxLAogICAgMi42MDkx
NDM2Mzk3Nzc3ODQ1ZS0zMCwKICAgIDMuODA2MDY3MTc3MDQ2MjAzZS0zMAogICBdLAogICAiaHNf
cmVmIjogewogICAgImhpIjogWwogICAgIDEyMy44MzI0NjY2NjYwOTA2OCwKICAgICA4NS4yOTMz
OTk5OTkxNDYxMgogICAgXSwKICAgICJsbyI6IFsKICAgICAxMjMuODMyNDY2NjY3MjQyNjYsCiAg
ICAgMzYuNzI1MjAwMDAwODYzNDcKICAgIF0KICAgfQogIH0sCiAgImN1YmljX3N0ZXB8MTExIjog
ewogICAidlRfVlJIIjogNy43OTkwNDYzNzU4NDQ5MjMsCiAgICJ2VF9WIjogOC4xMTU3OTQ0Nzc0
MzcxOTUsCiAgICJ2VF9SIjogNy40Njg4NzczNDE2ODY2MDcsCiAgICJ2VF9IU19sbyI6IDcuNzU4
NjE0NDkwMjExMDg3LAogICAidlRfSFNfaGkiOiA3Ljg2Nzk1MzAwNTkwNDc3NSwKICAgInJfYWdn
X0UyX1ZSSCI6IFsKICAgIC0xLjExMDIyMzAyNDYyNTE1NjVlLTE2LAogICAgMC4wLAogICAgLTEu
MTEwMjIzMDI0NjI1MTU2NWUtMTYsCiAgICAtMS4xMTAyMjMwMjQ2MjUxNTY1ZS0xNiwKICAgIDIu
MjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIDAuMCwKICAgIC0xLjExMDIyMzAyNDYyNTE1NjVlLTE2
LAogICAgMC4wLAogICAgMC4wLAogICAgMC4wLAogICAgLTMuMzMwNjY5MDczODc1NDY5NmUtMTYs
CiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2CiAgIF0sCiAgICJyX2FnZ19oX1ZSSCI6IFsKICAg
IC0xLjExMDIyMzAyNDYyNTE1NjVlLTE2LAogICAgMC4wLAogICAgMC4wLAogICAgMC4wLAogICAg
Mi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgMC4w
LAogICAgMC4wLAogICAgMC4wLAogICAgMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgMC4wLAog
ICAgLTEuMTEwMjIzMDI0NjI1MTU2NWUtMTYKICAgXSwKICAgInJfYWdnX0UyX0hTIjogWwogICAg
LTEuMTEwMjIzMDI0NjI1MTU2NWUtMTYsCiAgICAyLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAy
LjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAwLjAsCiAgICAtMS4xMTAyMjMwMjQ2MjUxNTY1ZS0x
NiwKICAgIC0xLjExMDIyMzAyNDYyNTE1NjVlLTE2LAogICAgLTEuMTEwMjIzMDI0NjI1MTU2NWUt
MTYsCiAgICAtMS4xMTAyMjMwMjQ2MjUxNTY1ZS0xNiwKICAgIDAuMCwKICAgIDIuMjIwNDQ2MDQ5
MjUwMzEzZS0xNiwKICAgIC0xLjExMDIyMzAyNDYyNTE1NjVlLTE2LAogICAgMC4wCiAgIF0sCiAg
ICJyX2FnZ19FMl9WIjogWwogICAgMC4wLAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAg
IDAuMCwKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNl
LTE2LAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIDAuMCwKICAgIC0yLjIyMDQ0NjA0
OTI1MDMxM2UtMTYsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgMC4wLAogICAgMC4w
LAogICAgMi4yMjA0NDYwNDkyNTAzMTNlLTE2CiAgIF0sCiAgICJyX2FnZ19FMl9SIjogWwogICAg
MC4wLAogICAgLTEuMTEwMjIzMDI0NjI1MTU2NWUtMTYsCiAgICAyLjIyMDQ0NjA0OTI1MDMxM2Ut
MTYsCiAgICAtMS4xMTAyMjMwMjQ2MjUxNTY1ZS0xNiwKICAgIDAuMCwKICAgIDAuMCwKICAgIC0y
LjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAwLjAsCiAgICAwLjAsCiAgICAyLjIyMDQ0NjA0OTI1
MDMxM2UtMTYsCiAgICAtMS4xMTAyMjMwMjQ2MjUxNTY1ZS0xNiwKICAgIDIuMjIwNDQ2MDQ5MjUw
MzEzZS0xNgogICBdLAogICAiU190X0UyIjogNC4xMTAwMDc3NDE1MjAyNDY1ZS0xNiwKICAgIlNf
dF9oIjogLTIuOTI1MjcxMjg0OTcxMzk2ZS0xNiwKICAgImthcHBhMl9FMiI6IC0xLjY3MzkxNDM4
NTcxNDc2NTJlLTE2LAogICAia2FwcGEyX2giOiAxLjc0MDMxNzYwMTAxNTg0MzNlLTE1LAogICAi
a2FwcGEzX0UyIjogLTYuNDc3ODYxMjU5MTc3MDY4ZS0xNSwKICAgImthcHBhMl9FMl9IUyI6IDMu
Njg5NTI4NjUwMTY2MzM4NWUtMTUsCiAgICJrYXBwYTJfRTJfNHRlcm0iOiAtNy41NTEwNjI2OTA3
MTU2MjZlLTE1LAogICAiU190X0UyXzR0ZXJtIjogNC4xMTAwMDc3NDE1MjAyMzQ3ZS0xNiwKICAg
ImthcHBhNF9FMl80dGVybSI6IDEuMjA4NTQxNjc3MDcxNzYzZS0xMywKICAgImZpdF9yZXNpZHVh
bCI6IDkuNTg4Mjk2OTg0NTgwNDdlLTE3LAogICAiZml0X3Jlc2lkdWFsXzR0ZXJtIjogOS4wODI3
MjgyNDY2ODg1MzJlLTE3LAogICAiaGFsdmluZ19kZXZfa2FwcGEyIjogMzYuNzA5NDI1ODA1ODQ1
MzgsCiAgICJrYXBwYTJfRTJfd2luZG93MHAxIjogLTYuMzEyMjM1MDMzMzQ0ODE4ZS0xNSwKICAg
ImxhbWJkYV9tZWFuX3QiOiBbCiAgICA0LjQ2NTk0NDg5MTYxNTQ4OWUtMzEsCiAgICA1LjQ3NjAz
ODM2NTYyODIzNWUtMzIsCiAgICA2LjA1MTI1NzcyNjgxODMwOWUtMzIsCiAgICAxLjk0ODM2NTMy
MTgzNjQ5NmUtMzAsCiAgICAyLjgyODMxNTYxNzU5ODE5NWUtMzAsCiAgICA0LjI1ODM5MjI5MTA2
OTY5NGUtMzIsCiAgICAyLjA2NzE2NzU0MTA2NTM0NjNlLTMxLAogICAgMS40NDE0NDM2NDE4ODM5
NzU4ZS0zMSwKICAgIDYuOTc2NTQ3NjE2OTIxMDRlLTMxLAogICAgOC4wNTg4Mjc4NDg5NTcwNWUt
MzIsCiAgICA4LjgyNjM1MTgzMTcwNDgxN2UtMzEsCiAgICA1LjI3NzQzMjM1ODM0ODY0NmUtMzIK
ICAgXSwKICAgImhzX3JlZiI6IHsKICAgICJoaSI6IFsKICAgICAxMjMuODMyNDY2NjY2MDkwNjgs
CiAgICAgODUuMjkzMzk5OTk5MTQ2MTIKICAgIF0sCiAgICAibG8iOiBbCiAgICAgMTIzLjgzMjQ2
NjY2NzI0MjY2LAogICAgIDM2LjcyNTIwMDAwMDg2MzQ3CiAgICBdCiAgIH0KICB9LAogICJjdWJp
Y19nZW04fDAwMSI6IHsKICAgInZUX1ZSSCI6IDkuMzA3ODk5MDc2NTMzMTc5LAogICAidlRfViI6
IDkuODcyNDkyMDg2NjAxMDIsCiAgICJ2VF9SIjogOC43MDY3NzE1Mjc4MzEzNTIsCiAgICJ2VF9I
U19sbyI6IDkuMjExNzIxMDY0MzcwODYxLAogICAidlRfSFNfaGkiOiA5LjQ1Njg1NDk4NDU4ODcz
OCwKICAgInJfYWdnX0UyX1ZSSCI6IFsKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAw
LjAsCiAgICAwLjAsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgLTIuMjIwNDQ2MDQ5
MjUwMzEzZS0xNiwKICAgIDAuMCwKICAgIDAuMCwKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYs
CiAgICAwLjAsCiAgICAwLjAsCiAgICAwLjAsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2CiAg
IF0sCiAgICJyX2FnZ19oX1ZSSCI6IFsKICAgIDAuMCwKICAgIDIuMjIwNDQ2MDQ5MjUwMzEzZS0x
NiwKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAwLjAsCiAgICAwLjAsCiAgICAwLjAs
CiAgICAwLjAsCiAgICAwLjAsCiAgICAwLjAsCiAgICAwLjAsCiAgICAyLjIyMDQ0NjA0OTI1MDMx
M2UtMTYsCiAgICAyLjIyMDQ0NjA0OTI1MDMxM2UtMTYKICAgXSwKICAgInJfYWdnX0UyX0hTIjog
WwogICAgMC4wLAogICAgMC4wLAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIDAuMCwK
ICAgIDAuMCwKICAgIDAuMCwKICAgIC0zLjMzMDY2OTA3Mzg3NTQ2OTZlLTE2LAogICAgMC4wLAog
ICAgMC4wLAogICAgMC4wLAogICAgMC4wLAogICAgLTMuMzMwNjY5MDczODc1NDY5NmUtMTYKICAg
XSwKICAgInJfYWdnX0UyX1YiOiBbCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgMC4w
LAogICAgMC4wLAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIDAuMCwKICAgIC0yLjIy
MDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAwLjAsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAog
ICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIDAuMCwKICAgIC0yLjIyMDQ0NjA0OTI1MDMx
M2UtMTYsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2CiAgIF0sCiAgICJyX2FnZ19FMl9SIjog
WwogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIDAuMCwKICAgIC0yLjIyMDQ0NjA0OTI1
MDMxM2UtMTYsCiAgICAtNC40NDA4OTIwOTg1MDA2MjZlLTE2LAogICAgMC4wLAogICAgLTIuMjIw
NDQ2MDQ5MjUwMzEzZS0xNiwKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAtMi4yMjA0
NDYwNDkyNTAzMTNlLTE2LAogICAgMC4wLAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAg
IC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAtNC40NDA4OTIwOTg1MDA2MjZlLTE2CiAgIF0s
CiAgICJTX3RfRTIiOiAyLjI2OTA0NzE5NzY1MTYyMTZlLTE2LAogICAiU190X2giOiAxLjAyMDcw
MjkwNjEzNjU0NDdlLTE1LAogICAia2FwcGEyX0UyIjogLTEuNDk0MDcyMzQ0Mjc0MzM2MWUtMTYs
CiAgICJrYXBwYTJfaCI6IDEuNDUyNTcwMzM0NzExMTU1MmUtMTUsCiAgICJrYXBwYTNfRTIiOiAt
My43MTAyOTkzNTc3OTMzMTJlLTE1LAogICAia2FwcGEyX0UyX0hTIjogLTIuOTMyODA4Njc1Nzk3
NzY4NmUtMTYsCiAgICJrYXBwYTJfRTJfNHRlcm0iOiAtNy41NDg3Njk4ODQ2NjE4MzFlLTE1LAog
ICAiU190X0UyXzR0ZXJtIjogMi4yNjkwNDcxOTc2NTE2MDkzZS0xNiwKICAgImthcHBhNF9FMl80
dGVybSI6IDEuMjExMTEwMDA3NjM3NDEyNWUtMTMsCiAgICJmaXRfcmVzaWR1YWwiOiAxLjI3Njg1
MDMxNjU4OTA0NTRlLTE2LAogICAiZml0X3Jlc2lkdWFsXzR0ZXJtIjogMS4yMzkxNzMyMDQ5MzM1
NjRlLTE2LAogICAiaGFsdmluZ19kZXZfa2FwcGEyIjogMzYuNzA5NDI1ODA1ODQ1MTksCiAgICJr
YXBwYTJfRTJfd2luZG93MHAxIjogLTUuNjM0MDYxMDIxNDk3ODI3ZS0xNSwKICAgImxhbWJkYV9t
ZWFuX3QiOiBbCiAgICAxLjMzMjE2MDEyNDc4OTkzNzJlLTMwLAogICAgMy4yOTYzMTU4Nzg4MzI5
OTU1ZS0zMSwKICAgIDUuMTE1NjA4MDE4MDY1NjE0ZS0zMSwKICAgIDIuNTI5NjMwNjUyNTE2MzA2
NGUtMzEsCiAgICA2LjA5MTE4OTY2MTA2ODgzNmUtMzIsCiAgICAxLjQ5MDcwMzM3NjEwMTQ2NWUt
MzAsCiAgICA0Ljk3MDUzMTAxODQ2NzY3NWUtMzEsCiAgICAxLjYzMjE3Mjg3MjA4MjI3NTNlLTMx
LAogICAgMi4wMzI4ODAwMzI4MjQyNDg0ZS0zMCwKICAgIDkuMjUyNDU2MjgxNDAzMDk4ZS0zMiwK
ICAgIDEuMjE1NzM5NzM5NTA0NzQyMmUtMzAsCiAgICA0Ljc4ODI0MjM5OTAyMjQyMWUtMzAKICAg
XSwKICAgImhzX3JlZiI6IHsKICAgICJoaSI6IFsKICAgICAyMTAuMjc1NDk5OTk5MDkzMSwKICAg
ICAxMzEuNTQzNTk5OTk4NjQ0MTQKICAgIF0sCiAgICAibG8iOiBbCiAgICAgMjEwLjI3NTUwMDAw
MDkwNjkzLAogICAgIDQ2LjM0OTg1MDAwMTM1OTE0CiAgICBdCiAgIH0KICB9LAogICJjdWJpY19n
ZW04fDExMSI6IHsKICAgInZUX1ZSSCI6IDkuMzA3ODk5MDc2NTMzMTc5LAogICAidlRfViI6IDku
ODcyNDkyMDg2NjAxMDIsCiAgICJ2VF9SIjogOC43MDY3NzE1Mjc4MzEzNTIsCiAgICJ2VF9IU19s
byI6IDkuMjExNzIxMDY0MzcwODYxLAogICAidlRfSFNfaGkiOiA5LjQ1Njg1NDk4NDU4ODczOCwK
ICAgInJfYWdnX0UyX1ZSSCI6IFsKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAwLjAs
CiAgICAyLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAog
ICAgMC4wLAogICAgMC4wLAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIC0yLjIyMDQ0
NjA0OTI1MDMxM2UtMTYsCiAgICAwLjAsCiAgICAwLjAsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNl
LTE2LAogICAgMi4yMjA0NDYwNDkyNTAzMTNlLTE2CiAgIF0sCiAgICJyX2FnZ19oX1ZSSCI6IFsK
ICAgIDAuMCwKICAgIDAuMCwKICAgIDAuMCwKICAgIDAuMCwKICAgIDAuMCwKICAgIDAuMCwKICAg
IDAuMCwKICAgIDAuMCwKICAgIDAuMCwKICAgIDAuMCwKICAgIDAuMCwKICAgIDQuNDQwODkyMDk4
NTAwNjI2ZS0xNgogICBdLAogICAicl9hZ2dfRTJfSFMiOiBbCiAgICAtMi4yMjA0NDYwNDkyNTAz
MTNlLTE2LAogICAgMC4wLAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIC0yLjIyMDQ0
NjA0OTI1MDMxM2UtMTYsCiAgICAwLjAsCiAgICAwLjAsCiAgICAwLjAsCiAgICAtMi4yMjA0NDYw
NDkyNTAzMTNlLTE2LAogICAgMC4wLAogICAgMC4wLAogICAgMC4wLAogICAgLTMuMzMwNjY5MDcz
ODc1NDY5NmUtMTYKICAgXSwKICAgInJfYWdnX0UyX1YiOiBbCiAgICAwLjAsCiAgICAyLjIyMDQ0
NjA0OTI1MDMxM2UtMTYsCiAgICAwLjAsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAg
MC4wLAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2Ut
MTYsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgMC4wLAogICAgMi4yMjA0NDYwNDky
NTAzMTNlLTE2LAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIC0zLjMzMDY2OTA3Mzg3
NTQ2OTZlLTE2CiAgIF0sCiAgICJyX2FnZ19FMl9SIjogWwogICAgMC4wLAogICAgMi4yMjA0NDYw
NDkyNTAzMTNlLTE2LAogICAgMC4wLAogICAgLTQuNDQwODkyMDk4NTAwNjI2ZS0xNiwKICAgIDAu
MCwKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2
LAogICAgMC4wLAogICAgMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgMC4wLAogICAgLTQuNDQw
ODkyMDk4NTAwNjI2ZS0xNiwKICAgIDAuMAogICBdLAogICAiU190X0UyIjogLTEuMTgxOTg1MjE3
MTY5NzM4NmUtMTUsCiAgICJTX3RfaCI6IDAuMCwKICAgImthcHBhMl9FMiI6IDEuMjcyNzI4Mjkz
MjcwNzUzZS0xNiwKICAgImthcHBhMl9oIjogMC4wLAogICAia2FwcGEzX0UyIjogMS44ODg5OTY1
NTI4ODc1MjFlLTE0LAogICAia2FwcGEyX0UyX0hTIjogLTQuMTUwMjAwOTU2MzE3NTg2M2UtMTYs
CiAgICJrYXBwYTJfRTJfNHRlcm0iOiA0LjY0NDkzMjg2MjI1NDA1NWUtMTUsCiAgICJTX3RfRTJf
NHRlcm0iOiAtMS4xODE5ODUyMTcxNjk3MzhlLTE1LAogICAia2FwcGE0X0UyXzR0ZXJtIjogLTcu
Mzk0Mzk4MDUyMzg5MTZlLTE0LAogICAiZml0X3Jlc2lkdWFsIjogMS4zNzM2MzU4MzQ2NTA3MzE1
ZS0xNiwKICAgImZpdF9yZXNpZHVhbF80dGVybSI6IDEuMzYwNzEyNDMwMTk2NDYyNWUtMTYsCiAg
ICJoYWx2aW5nX2Rldl9rYXBwYTIiOiAzNi43MDk0MjU4MDU4NDQ2MiwKICAgImthcHBhMl9FMl93
aW5kb3cwcDEiOiA0Ljc5OTM4NTMxNDYwOTI3MWUtMTUsCiAgICJsYW1iZGFfbWVhbl90IjogWwog
ICAgNi42NTQ1NjM5MTk1NTU4ODdlLTMyLAogICAgMS4yODQ0NzQ2MjA2MjAxNDNlLTMxLAogICAg
OC4yMDMxNDY3OTYxNjU5NzNlLTMyLAogICAgMi4xOTE0MTQ0MzM4NTUyNTllLTMxLAogICAgMy41
OTkyNjYwMjA1NjA4NDA3ZS0zMSwKICAgIDEuNDkwNzAzMzc2MTAxNDY1ZS0zMCwKICAgIDMuNzM3
MTQxNTE2NDMzOTY2ZS0zMiwKICAgIDIuNzc5NDIzNTgxMzE1Mjc0ZS0zMiwKICAgIDQuOTEzODI1
ODE2ODk4NjNlLTMyLAogICAgMS4wMTg5MDc5MjYwOTEyOTNlLTMwLAogICAgMS4zOTU2ODQyODI4
OTczNTE4ZS0zMSwKICAgIDQuODQ0NTQ2ODQ0MzY1MzE4ZS0zMQogICBdLAogICAiaHNfcmVmIjog
ewogICAgImhpIjogWwogICAgIDIxMC4yNzU0OTk5OTkwOTMxLAogICAgIDEzMS41NDM1OTk5OTg2
NDQxNAogICAgXSwKICAgICJsbyI6IFsKICAgICAyMTAuMjc1NTAwMDAwOTA2OTMsCiAgICAgNDYu
MzQ5ODUwMDAxMzU5MTQKICAgIF0KICAgfQogIH0KIH0sCiAiZmFsc2lmaWVycyI6IHsKICAiRi1N
Uy0zIjogewogICAic3RhdGUiOiAiU0lMRU5UIiwKICAgIndvcnN0X1NfdCI6IDQuODk1NzUxNTI5
MzYxMDk4ZS0xMwogIH0sCiAgIkYtTVMtMiI6IHsKICAgInN0YXRlIjogIlJFR0lTVEVSRURfTk9U
X0VYRUNVVEVEIgogIH0sCiAgIkYtTVMtMSI6IHsKICAgInN0YXRlIjogIlJFVElSRURfVE9fQ09O
VFJPTCIKICB9CiB9LAogInZlcmRpY3RfY2xhc3MiOiAiSURFTlRJVFktREVMSVZFUkVEIiwKICJU
MV9wb3N0X3dyaXRlIjogewogICJsaXN0X21kNSI6ICJmZWYyODI3MTAwZDNmODVlMGE2MzQxYjQ0
ZjBjMDBiZiIsCiAgInN0YXRlIjogIkNMRUFOIiwKICAibnVtZXJpY19jb2xsaXNpb25zIjogNCwK
ICAiZmlsZXMiOiBbCiAgICJnX21zY3MxX2NoYXRsZWdfY2hlY2twb2ludC5qc29uIgogIF0KIH0K
fQ==
=====END-EMBED name=g_mscs1_chatleg_checkpoint.json=====

=====BEGIN-EMBED name=g_mscs1_chatleg_compare.json md5=7b933c08b92d57b9523f2cee4ff076ba bytes=3277 encoding=base64 armor_bytes=4430 QUARANTINED=====
ewogImdhdGUiOiAiRy1NU0NTMSIsCiAic3RlcCI6ICJjb21wYXJlIChsYXN0KSIsCiAiY2hlY2tw
b2ludF9tZDUiOiAiYzA0YzBiOGVhMzRjZmU2MGYyMzFhYTA2ODI4ZTZjZTQiLAogInJvd3MiOiBb
CiAgewogICAiaWQiOiAiSC1NUy0xIiwKICAgInByZWRpY3RlZCI6ICJoZXggcl94dGFsX0UyIDwg
MCwgfHJ8IGluIFsxZS0yLCAxZS0xXTsgY3ViaWMgc21hbGxlciIsCiAgICJtYWNoaW5lIjogewog
ICAgImhleF9zdGVwfGEiOiAtMC4wMjc5NjcyMDY4OTQ4NzI1MywKICAgICJoZXhfc3RlcHxiIjog
LTAuMDI3OTQ3MTI5MDgxMzQ2Nzc4LAogICAgImhleF9nZW04fGEiOiAtMC4wMzkzMzk0Mzc3MDMz
MDM1MDQsCiAgICAiaGV4X2dlbTh8YiI6IC0wLjAzOTM1MjM0OTg5NjExNzY5LAogICAgImN1Ymlj
X3N0ZXB8MDAxIjogLTAuMDE3Mjk2NzY3NzQxMjE1OCwKICAgICJjdWJpY19zdGVwfDExMSI6IDAu
MDExNTMxMTc4NDk0MTQ0MDksCiAgICAiY3ViaWNfZ2VtOHwwMDEiOiAtMC4wMjA4NDI0NDIwMjI3
NDAzMjYsCiAgICAiY3ViaWNfZ2VtOHwxMTEiOiAwLjAxMzg5NDk2MTM0ODQ5MzU1CiAgIH0sCiAg
ICJjb25jb3JkYW50IjogdHJ1ZQogIH0sCiAgewogICAiaWQiOiAiSC1NUy0yIiwKICAgInByZWRp
Y3RlZCI6ICJ8cl9ofCB+MWUtMywgc2lnbiA9IC1zaWduKENvdiksIHxyX2h8IDw8IHxyX0UyfCIs
CiAgICJtYWNoaW5lIjogewogICAgImhleF9zdGVwfGEiOiBbCiAgICAgLTAuMDAxMTEyODc4NDUw
NTU1Mjk5LAogICAgIDAuMDM2NDQ0NDE3OTMyNTYwNDI1CiAgICBdLAogICAgImhleF9zdGVwfGIi
OiBbCiAgICAgLTAuMDAxMTEyODAwOTgxMzE2NjA4NCwKICAgICAwLjAzNjQ0MzAzNTY2MDg0MDEy
CiAgICBdLAogICAgImhleF9nZW04fGEiOiBbCiAgICAgLTAuMDAxMzE0ODY1MjM4Mjg4Mzg3NCwK
ICAgICAwLjA1MTMyODk5MTc5NjgzMTQ0CiAgICBdLAogICAgImhleF9nZW04fGIiOiBbCiAgICAg
LTAuMDAxMzE0OTI3NTgxNjk5NTk4NywKICAgICAwLjA1MTMzMDQzNzA5NjQ5MzAxCiAgICBdLAog
ICAgImN1YmljX3N0ZXB8MDAxIjogWwogICAgIC0wLjAwMTUxNjM3NzEwMjMyNDU1MSwKICAgICAw
LjA0OTAxOTU3ODk0Nzc5MzY3CiAgICBdLAogICAgImN1YmljX3N0ZXB8MTExIjogWwogICAgIC0w
LjAwMTUxNjM3NzEwMjMyNDU1MSwKICAgICAwLjA0OTAxOTU3ODk0Nzc5MzY3CiAgICBdLAogICAg
ImN1YmljX2dlbTh8MDAxIjogWwogICAgIC0wLjAwMTg0NTEwMTAxOTQyODQ3NDUsCiAgICAgMC4w
NzIyMTE3MjA4MzM4NjQzMwogICAgXSwKICAgICJjdWJpY19nZW04fDExMSI6IFsKICAgICAtMC4w
MDE4NDUxMDEwMTk0Mjg0NzQ1LAogICAgIDAuMDcyMjExNzIwODMzODY0MzMKICAgIF0KICAgfSwK
ICAgImNvbmNvcmRhbnQiOiB0cnVlCiAgfSwKICB7CiAgICJpZCI6ICJILU1TLTMiLAogICAicHJl
ZGljdGVkIjogIlNfdCA9IDA7IGthcHBhMl9FMiAhPSAwIHdpdGggc2lnbiBvZiByX3h0YWxfRTI7
IGthcHBhMl9oIHNtYWxsZXIiLAogICAibWFjaGluZSI6IHsKICAgICJoZXhfc3RlcHxhIjogWwog
ICAgIDEuNjI2NjIzMTI1NjI2MTY5NmUtMTMsCiAgICAgLTAuMDAxNDM5NDYxNzY5NDk2Njk5MiwK
ICAgICAtMi4wMDc1MTAxOTgxNjM3NjU1ZS0wNgogICAgXSwKICAgICJoZXhfc3RlcHxiIjogWwog
ICAgIDEuNjEyNTAzNDY1ODYxNjMxM2UtMTMsCiAgICAgLTAuMDAxNDM4NzAyNzE4NzQ5MDgzLAog
ICAgIC0yLjAwNTQwMzE5NDExMjc5MTZlLTA2CiAgICBdLAogICAgImhleF9nZW04fGEiOiBbCiAg
ICAgNC44OTQ2NDIzNjUxNDUzOTZlLTEzLAogICAgIC0wLjAwMTg5NTY0ODQ4MjY3MDEzNTIsCiAg
ICAgLTMuMjQ5Mzk2Njk1OTI4OTQ2M2UtMDYKICAgIF0sCiAgICAiaGV4X2dlbTh8YiI6IFsKICAg
ICA0Ljg5NTc1MTUyOTM2MTA5OGUtMTMsCiAgICAgLTAuMDAxODk2MTM3NDY2NTI0MjI2NCwKICAg
ICAtMy4yNTA5MzU0OTAzMDYxMTY3ZS0wNgogICAgXSwKICAgICJjdWJpY19zdGVwfDAwMSI6IFsK
ICAgICAzLjg3MjY5OTY0OTgwMDUwMmUtMTYsCiAgICAgMy4xNDE3MDIxMjM5MzI0MTZlLTE1LAog
ICAgIC0zLjQ1ODUwMDc5NjkzMTQwMWUtMTcKICAgIF0sCiAgICAiY3ViaWNfc3RlcHwxMTEiOiBb
CiAgICAgNC4xMTAwMDc3NDE1MjAyNDY1ZS0xNiwKICAgICAtMS42NzM5MTQzODU3MTQ3NjUyZS0x
NiwKICAgICAxLjc0MDMxNzYwMTAxNTg0MzNlLTE1CiAgICBdLAogICAgImN1YmljX2dlbTh8MDAx
IjogWwogICAgIDIuMjY5MDQ3MTk3NjUxNjIxNmUtMTYsCiAgICAgLTEuNDk0MDcyMzQ0Mjc0MzM2
MWUtMTYsCiAgICAgMS40NTI1NzAzMzQ3MTExNTUyZS0xNQogICAgXSwKICAgICJjdWJpY19nZW04
fDExMSI6IFsKICAgICAtMS4xODE5ODUyMTcxNjk3Mzg2ZS0xNSwKICAgICAxLjI3MjcyODI5MzI3
MDc1M2UtMTYsCiAgICAgMC4wCiAgICBdCiAgIH0sCiAgICJjb25jb3JkYW50IjogZmFsc2UKICB9
LAogIHsKICAgImlkIjogIkgtTVMtNCIsCiAgICJwcmVkaWN0ZWQiOiAiaGV4IGxhbWJkYV9tZWFu
IH4xZS0yIG9uIHFTVjsgemVybyBhdCB0ID0gMCBpbiB0aGUgYWdncmVnYXRlIiwKICAgIm1hY2hp
bmUiOiB7CiAgICAiaGV4X3N0ZXB8YSI6IFsKICAgICAwLjAwNDgwODU3NTcyNDAyMjgzOCwKICAg
ICAicVNWIgogICAgXSwKICAgICJoZXhfZ2VtOHxhIjogWwogICAgIDAuMDA0OTUzNzY5NjE4MDYz
OTUzNSwKICAgICAicVNWIgogICAgXQogICB9LAogICAiY29uY29yZGFudCI6IHRydWUKICB9LAog
IHsKICAgImlkIjogIkgtTVMtNSIsCiAgICJwcmVkaWN0ZWQiOiAiaGV4IGFuZCBjdWJpYyBrYXBw
YTJfRTIgc2hhcmUgYSBzaWduIiwKICAgIm1hY2hpbmUiOiB7CiAgICAiaGV4X3N0ZXB8YSI6IC0w
LjAwMTQzOTQ2MTc2OTQ5NjY5OTIsCiAgICAiaGV4X3N0ZXB8YiI6IC0wLjAwMTQzODcwMjcxODc0
OTA4MywKICAgICJoZXhfZ2VtOHxhIjogLTAuMDAxODk1NjQ4NDgyNjcwMTM1MiwKICAgICJoZXhf
Z2VtOHxiIjogLTAuMDAxODk2MTM3NDY2NTI0MjI2NCwKICAgICJjdWJpY19zdGVwfDAwMSI6IDMu
MTQxNzAyMTIzOTMyNDE2ZS0xNSwKICAgICJjdWJpY19zdGVwfDExMSI6IC0xLjY3MzkxNDM4NTcx
NDc2NTJlLTE2LAogICAgImN1YmljX2dlbTh8MDAxIjogLTEuNDk0MDcyMzQ0Mjc0MzM2MWUtMTYs
CiAgICAiY3ViaWNfZ2VtOHwxMTEiOiAxLjI3MjcyODI5MzI3MDc1M2UtMTYKICAgfSwKICAgImNv
bmNvcmRhbnQiOiBmYWxzZQogIH0KIF0sCiAidmVyZGljdF9jbGFzcyI6ICJJREVOVElUWS1ERUxJ
VkVSRUQiLAogIm5fY29uY29yZGFudCI6IDMKfQ==
=====END-EMBED name=g_mscs1_chatleg_compare.json=====

=====BEGIN-EMBED name=G_MSCS1_CHATLEG_EXECUTION_REPORT.md md5=3cf78f51962359a25fac13f968cba119 bytes=12608 encoding=base64 armor_bytes=17034 QUARANTINED=====
IyBHLU1TQ1MxIOKAlCBDSEFULUxFRyBFWEVDVVRJT04gUkVQT1JUCgoqKkRhdGU6KiogU2VwdGVt
YmVyIDE5LCAyMDI2LiAqKkJhc2U6KiogVjQuODIgYGQwOTVhNzAwM2JiMGQ0YzE3N2U3NDUxZTFk
MTRjNGM2YC4gKipNZW1vIGxvY2s6KiogdjIgYDNmMzAyNjJlYWVjNDYxZmI1ZmQzMjAyODM1Zjdk
ZTM3YCAoMzQsODM3IEIpLiAqKkxvY2sgcmVjb3JkOioqIGBHX01TQ1MxX0xPQ0tfUkVDT1JELm1k
YCBgM2RiZTk1M2JhZGI2YzAzMGVmMWQ0NDlhZGJhYzIwNDRgICg3LDI4OSBCOyBBZGRlbmR1bSBB
LTIgb3BlcmF0aW9uYWxpemF0aW9ucyBsb2NrZWQgcHJlLWV4ZWN1dGlvbikuICoqQ29tcGFyYXRv
ciB2MS4wKiogYDIyNDMyYjI5YCArICoqc2NoZW1hIHYxLjAqKiBgNzZhNDJkYjNgIEZST1pFTiBi
ZWZvcmUgdGhpcyBlbWlzc2lvbi4gKipJbnN0cnVtZW50OioqIGBnX21zY3MxX2NoYXRsZWcucHlg
IGBkYjVmNTFkZDllZjdmNTRkZDA4MjY5OTFkNTk0NjgxYmAgKDM0LDYwNiBCOyA3Lzcgc3VpdGVz
OyBtZDUtZ3VhcmRzIHRoZSBtZW1vLCBYLTEsIFgtMy4uWC01OyBUMSBoYWx0LXdpdGhvdXQtbGlz
dDsgcnVuIHRpbWUgOCBtIDQ1IHMgc2luZ2xlIGNvcmUpLiAqKkNoZWNrcG9pbnQ6KiogYGdfbXNj
czFfY2hhdGxlZ19jaGVja3BvaW50Lmpzb25gIGBjMDRjMGI4ZWEzNGNmZTYwZjIzMWFhMDY4Mjhl
NmNlNGAgKDMzLDI4OSBCKS4gKipDb21wYXJlIChsYXN0KToqKiBgZ19tc2NzMV9jaGF0bGVnX2Nv
bXBhcmUuanNvbmAgYDdiOTMzYzA4YjkyZDU3Yjk1MjNmMmNlZTRmZjA3NmJhYCAoMywyNzcgQiku
ICoqVDE6KiogZ2F0ZSBsaXN0IGBmZWYyODI3MWAgQ0xFQU4gb24gaW5zdHJ1bWVudCwgbWVtbywg
Y2hlY2twb2ludCAoNCBudW1lcmljIGZvcm1hdHRpbmcgY29sbGlzaW9ucyBsb2dnZWQsIDAgaGl0
cyksIGNvbXBhcmUgKDEgY29sbGlzaW9uLCAwIGhpdHMpLiAqKlZlcmRpY3QgY2xhc3M6IElERU5U
SVRZLURFTElWRVJFRC4qKgoKIyMgMS4gUGhhc2UgMCDigJQgY29udHJvbHMgYW5kIHBpbnMgKGFs
bCBQQVNTKQoKfCBDb250cm9sIHwgUmVzdWx0IHwKfC0tLXwtLS18CnwgRi1DVFJMLUlTTyB8IHJf
eHRhbF9FMiAyLjLDlzEw4oG7wrnigbYsIHJfeHRhbF9oIDAsIM67X21heCA1LjnDlzEw4oG7wrPC
uSwgbWF4X3QgfHJfYWdnfCA0LjTDlzEw4oG7wrnigbYg4oCUIHRleHR1cmUgb24gYW4gaXNvdHJv
cGljIGdyYWluIGRvZXMgbm90aGluZyB8CnwgRi1DVFJMLVNPMyB8IE9ERi1hdmVyYWdlZCBF4oKC
IGZyYWN0aW9uIGF0IHQgPSAwID0gMC40IGZvciBldmVyeSBtb2RlIChtYXggZGV2IDUuMMOXMTDi
gbvCueKBtik7IHJfYWdnKDApID0gMCBleGFjdGx5IOKAlCB0aGUgU08oMykgaWRlbnRpdHksIGhv
bm91cmVkIHwKfCBGLUNUUkwtVEVYIHwgc3ludGhldGljIGhleCBhdCB0ID0gMTogcl9hZ2cgPSAy
LjUww5cxMOKBu8KzIOKJqyDPhF9hZ2cg4oCUIHRoZSBpbnN0cnVtZW50IHNlZXMgYSBzcGxpdCB3
aGVuIHRoZXJlIGlzIG9uZSB8CnwgUElOLUEyQUdHIHwgd29yc3QgcmVsYXRpdmUgcmVzaWR1YWwg
Kio2LjPDlzEw4oG7wrnigbQqKiBhZ2FpbnN0IHRoZSBiYW5rZWQgYeKCgl5hZ2cgPSBEMiBxdWFy
dGV0LCBEKDApLCBJ4oKALCBJ4oKCLCBWX1QsIFZfTCAoWC0zL1gtNCkg4oCUIHRoZSBmcm9tLXNj
cmF0Y2ggQm9ybiBrZXJuZWxzIChTTygzKSBncmlkICgxNiwxMCwxNiksIDgtcG9pbnQgzrwtR0wp
IHJlcHJvZHVjZSB0aGUgRy1TMkMxIFAyIG1hY2hpbmVyeSB0byBtYWNoaW5lIHByZWNpc2lvbiB8
CnwgRi1DVFJMLVBPTCB8IGhlbGljaXR5ICsxIHZzIOKIkjEgc2VsZi1lbmVyZ2llczogMDsgaGVs
aWNpdHkgdnMgcG9sYXJpemF0aW9uLWF2ZXJhZ2U6IDQuOMOXMTDigbvCueKBtiDigJQgdGhlIG9y
ZGVyLWNvbnNpc3RlbnQgc3RhbmQtaW4gZm9yIEYtTVMtMiAoYW4gYWxnZWJyYWljIGlkZW50aXR5
IGZvciBhIHJlYWwgc3ltbWV0cmljIHNjYXR0ZXJpbmcga2VybmVsLCBhcyBleHBlY3RlZCkgfAp8
IEYtQ1RSTC1BRE1JWCB8IDAg4oCUICoqc2VlIEgtTVMtMzogYXMgY29kZWQsIHRhdXRvbG9naWNh
bCoqIHwKfCBQSU4tVlJIMCB8IHdvcnN0IDEuNMOXMTDigbvCueKBtCBhZ2FpbnN0IHRoZSBiYW5r
ZWQgZ2VuZXJhbCBWb2lndC9SZXVzcyBtb2R1bGkgKFgtNCBgKl9nZW5gKSB8CnwgUElOLUhTMCB8
IHdvcnN0IDEuNsOXMTDigbvCucKyIGFnYWluc3QgdGhlIGJhbmtlZCBjdWJpYyBIYXNoaW7igJNT
aHRyaWttYW4gYmFuZHMgKFgtNSk6IHN0ZXAgWzYwLjE5NjA5ODgwOCwgNjEuOTA0Njg0NTAzXSwg
Z2VtOCBbODQuODU1ODA0OTY4LCA4OS40MzIxMDYyMDBdOyB0aGUgV2FscG9sZSBtYWNoaW5lcnkg
d2l0aCBvcHRpbWl6ZWQgaXNvdHJvcGljIHJlZmVyZW5jZXMgcmVwcm9kdWNlcyB0aGUgY2xhc3Np
Y2FsIGJvdW5kcyB8CgpIZXggSFMgYmFuZHMgKGNvbXB1dGVkLCBBLTIuMzsgbm8gYmFua2VkIHJl
ZmVyZW5jZSBhbW9uZyB0aGUgcGluIHNvdXJjZXMpOiBzdGVwIEdfSFMgWzcwLjQwNjUzLCA3MC45
NzM1OV0gKFZSIGJyYWNrZXQgWzY4LjY5LCA3My4wNl0pOyBnZW04IFs5OS44MTgzNCwgMTAxLjA1
ODc0XSAoVlIgWzk2LjYzLCAxMDUuMDRdKS4KCiMjIDIuIFBoYXNlIDEg4oCUIHNpbmdsZSBjcnlz
dGFsIChxdWFkcmF0dXJlIDY0w5cxMjg7IGRvdWJsaW5nIHJlc2lkdWFsIDEuOMOXMTDigbvCueKB
tSDiiaQgMcOXMTDigbvCueKBsCkKCnwgS2V5IHwgcl94dGFsKFMyLUXigoIpIHwgcl94dGFsKFMy
LWgpIHwg4p+ozrtfTOKfqSAocVQpIHwgbWF4IM67X0wgQCBicmFuY2ggfCBDb3ZfRU0ozrssdikg
fCBF4oKCIHNoYXJlIHFTSC9xU1YocVQxL3FUMikvcUwgfAp8LS0tfC0tLXwtLS18LS0tfC0tLXwt
LS18LS0tfAp8IGhleF9zdGVwXHxhIHwg4oiSMi43OTY3w5cxMOKBu8KyIHwg4oiSMS4xMTI5w5cx
MOKBu8KzIHwgNC44McOXMTDigbvCsyB8IDMuMzXDlzEw4oG7wrIgQCBxU1YgfCArMy42NMOXMTDi
gbvCsiB8IDAuODMzIC8gMC4xNjUgLyAwLjAwMiB8CnwgaGV4X3N0ZXBcfGIgfCDiiJIyLjc5NDfD
lzEw4oG7wrIgfCDiiJIxLjExMjjDlzEw4oG7wrMgfCA0Ljgxw5cxMOKBu8KzIHwgMy4zNcOXMTDi
gbvCsiBAIHFTViB8ICszLjY0w5cxMOKBu8KyIHwgMC44MzMgLyAwLjE2NSAvIDAuMDAyIHwKfCBo
ZXhfZ2VtOFx8YSB8IOKIkjMuOTMzOcOXMTDigbvCsiB8IOKIkjEuMzE0OcOXMTDigbvCsyB8IDQu
OTXDlzEw4oG7wrMgfCAzLjUxw5cxMOKBu8KyIEAgcVNWIHwgKzUuMTPDlzEw4oG7wrIgfCAwLjgz
MyAvIDAuMTY1IC8gMC4wMDIgfAp8IGhleF9nZW04XHxiIHwg4oiSMy45MzUyw5cxMOKBu8KyIHwg
4oiSMS4zMTQ5w5cxMOKBu8KzIHwgNC45NcOXMTDigbvCsyB8IDMuNTHDlzEw4oG7wrIgQCBxU1Yg
fCArNS4xM8OXMTDigbvCsiB8IDAuODMzIC8gMC4xNjUgLyAwLjAwMiB8CnwgY3ViaWNfc3RlcFx8
MDAxIHwg4oiSMS43Mjk3w5cxMOKBu8KyIHwg4oiSMS41MTY0w5cxMOKBu8KzIHwgOC4zOcOXMTDi
gbvCsyB8IDMuODfDlzEw4oG7wrIgQCBxVDIgfCArNC45MMOXMTDigbvCsiB8IDAuNDQ5IC8gMC41
NDMgLyAwLjAwOSB8CnwgY3ViaWNfc3RlcFx8MTExIHwgKiorMS4xNTMxw5cxMOKBu8KyKiogfCDi
iJIxLjUxNjTDlzEw4oG7wrMgfCA4LjM5w5cxMOKBu8KzIHwgMy44N8OXMTDigbvCsiBAIHFUMiB8
ICs0Ljkww5cxMOKBu8KyIHwgMC41MzMgLyAwLjQ1OSAvIDAuMDA4IHwKfCBjdWJpY19nZW04XHww
MDEgfCDiiJIyLjA4NDLDlzEw4oG7wrIgfCDiiJIxLjg0NTHDlzEw4oG7wrMgfCA5LjMxw5cxMOKB
u8KzIHwgNC4zM8OXMTDigbvCsiBAIHFUMiB8ICs3LjIyw5cxMOKBu8KyIHwgMC40NDkgLyAwLjU0
MiAvIDAuMDEwIHwKfCBjdWJpY19nZW04XHwxMTEgfCAqKisxLjM4OTXDlzEw4oG7wrIqKiB8IOKI
kjEuODQ1McOXMTDigbvCsyB8IDkuMzHDlzEw4oG7wrMgfCA0LjMzw5cxMOKBu8KyIEAgcVQyIHwg
KzcuMjLDlzEw4oG7wrIgfCAwLjUzMyAvIDAuNDU4IC8gMC4wMDkgfAoKUmVhZGluZ3MgKFIyKTog
dGhlIEXigoIgZGVzY3JpcHRvciBpcyBkaXJlY3Rpb24tc2VsZWN0aXZlIGFzIGRlc2lnbmVkIOKA
lCBvbiBoZXggaXQgc2l0cyA4MyUgb24gdGhlIHFTSCBicmFuY2ggKGl0cyBpbi1wbGFuZS1wb2xh
cml6ZWQgYmFzYWwgc3VwcG9ydCksIGFuZCBpdHMgc3BoZXJlLXdlaWdodGVkIHNwZWVkIGlzIDIu
OOKAkzMuOSUgYmVsb3cgdGhlIEVNIHNwZWNpZXMnIChuZWdhdGl2ZSwgb3JkZXIgMTDigbvCsiwg
SC1NUy0xIGNvbmNvcmRhbnQpOyB0aGUgaGV4IChhKS8oYikgYXJtcyBhZ3JlZSB0byAyw5cxMOKB
u+KBtSBpbiByICh0aGUgdGV0cmFnb25hbC1mb3JtL0M2NiBkaXNwb3NpdGlvbiBpcyBpbW1hdGVy
aWFsIGhlcmUpLiBUaGUgYWRtaXh0dXJlLWNvbnRyb2xsZWQgZGVzY3JpcHRvciBTMi1oIHNwbGl0
cyBhdCAxMOKBu8KzLCB3aXRoIHRoZSBzaWduIG9mIOKIkkNvdl9FTSjOu19MLCB2KSBhbmQgd2l0
aGluIDI1JSBvZiB0aGUgZmlyc3Qtb3JkZXIgdmFsdWUg4oiSQ292Lygz4p+oduKfqSkgKGhleDog
4oiSMS40M8OXMTDigbvCsyB2cyDiiJIxLjExw5cxMOKBu8KzKSDigJQgdGhlIHNwbGl0IGlzIGFk
bWl4dHVyZS1zb3VyY2VkIChILU1TLTIgY29uY29yZGFudCkuIEN1YmljOiB0aGUgc2lnbiBvZiBy
X3h0YWwoUzItReKCgikgZmxpcHMgd2l0aCB0aGUgZWxlY3RlZCBheGlzICjin6gwMDHin6kgbmVn
YXRpdmUsIOKfqDExMeKfqSBwb3NpdGl2ZSkg4oCUIHRoZSBkZXNjcmlwdG9yJ3MgYXhpcyBpcyBh
IGdlbnVpbmUgY2hvaWNlIG9uIGEgY3ViaWMgbGF0dGljZSwgcmVjb3JkZWQsIG5vdCByZXNvbHZl
ZC4KCiMjIDMuIFBoYXNlIDIg4oCUIGFnZ3JlZ2F0ZQoKfCBLZXkgfCB2X1QoSGlsbCwgdD0wKSB8
IEhTIGJhbmQgfCBTX3QoReKCgikgfCDOuuKCgihF4oKCKSBIaWxsIHwgzrrigoIoReKCgikgSFMt
bWVhbiB8IM664oKCKGgpIHwgaGFsdmluZyBkZXYgfCByX2FnZyh0PTEpIHwKfC0tLXwtLS18LS0t
fC0tLXwtLS18LS0tfC0tLXwtLS18LS0tfAp8IGhleF9zdGVwXHxhIHwgOC40MTkwNiB8IFs4LjM5
MDg2LCA4LjQyNDU4XSB8ICsxLjbDlzEw4oG7wrnCsyB8ICoq4oiSMS40Mzk0NsOXMTDigbvCsyoq
IHwg4oiSMS40MjgxOcOXMTDigbvCsyB8IOKIkjIuMMOXMTDigbvigbYgfCA0LjPDlzEw4oG74oG2
IHwg4oiSMS40NDDDlzEw4oG7wrMgfAp8IGhleF9zdGVwXHxiIHwgOC40MTkyOCB8IFs4LjM5MTA4
LCA4LjQyNDgwXSB8ICsxLjbDlzEw4oG7wrnCsyB8IOKIkjEuNDM4NzDDlzEw4oG7wrMgfCDiiJIx
LjQyNzQyw5cxMOKBu8KzIHwg4oiSMi4ww5cxMOKBu+KBtiB8IDQuM8OXMTDigbvigbYgfCDiiJIx
LjQ0MMOXMTDigbvCsyB8CnwgaGV4X2dlbThcfGEgfCAxMC4wNDE3MiB8IFs5Ljk5MDkxLCAxMC4w
NTI4MF0gfCArNC45w5cxMOKBu8K5wrMgfCAqKuKIkjEuODk1NjXDlzEw4oG7wrMqKiB8IOKIkjEu
ODg1MzDDlzEw4oG7wrMgfCDiiJIzLjLDlzEw4oG74oG2IHwgNy41w5cxMOKBu+KBtiB8IOKIkjEu
ODk3w5cxMOKBu8KzIHwKfCBoZXhfZ2VtOFx8YiB8IDEwLjA0MTU1IHwgWzkuOTkwNzQsIDEwLjA1
MjYzXSB8ICs0LjnDlzEw4oG7wrnCsyB8IOKIkjEuODk2MTTDlzEw4oG7wrMgfCDiiJIxLjg4NTgw
w5cxMOKBu8KzIHwg4oiSMy4zw5cxMOKBu+KBtiB8IDcuNcOXMTDigbvigbYgfCDiiJIxLjg5OMOX
MTDigbvCsyB8CnwgY3ViaWNfc3RlcFx8MDAxIHwgNy43OTkwNSB8IFs3Ljc1ODYxLCA3Ljg2Nzk1
XSB8ICszLjnDlzEw4oG7wrnigbYgfCArMy4xw5cxMOKBu8K54oG1IHwg4oiSNC42w5cxMOKBu8K5
4oG2IHwg4oiSMy41w5cxMOKBu8K54oG3IHwgNC44ICgwLzApIHwg4oiSMS4xw5cxMOKBu8K54oG2
IHwKfCBjdWJpY19zdGVwXHwxMTEgfCA3Ljc5OTA1IHwgWzcuNzU4NjEsIDcuODY3OTVdIHwgKzQu
McOXMTDigbvCueKBtiB8IOKIkjEuN8OXMTDigbvCueKBtiB8ICszLjfDlzEw4oG7wrnigbUgfCAr
MS43w5cxMOKBu8K54oG1IHwgMzcgKDAvMCkgfCDiiJIyLjLDlzEw4oG7wrnigbYgfAp8IGN1Ymlj
X2dlbThcfDAwMSB8IDkuMzA3OTAgfCBbOS4yMTE3MiwgOS40NTY4NV0gfCArMi4zw5cxMOKBu8K5
4oG2IHwg4oiSMS41w5cxMOKBu8K54oG2IHwg4oiSMi45w5cxMOKBu8K54oG2IHwgKzEuNcOXMTDi
gbvCueKBtSB8IDM3ICgwLzApIHwg4oiSMi4yw5cxMOKBu8K54oG2IHwKfCBjdWJpY19nZW04XHwx
MTEgfCA5LjMwNzkwIHwgWzkuMjExNzIsIDkuNDU2ODVdIHwg4oiSMS4yw5cxMOKBu8K54oG1IHwg
KzEuM8OXMTDigbvCueKBtiB8IOKIkjQuMsOXMTDigbvCueKBtiB8IDAgfCAzNyAoMC8wKSB8ICsy
LjLDlzEw4oG7wrnigbYgfAoKzrtfTCBpbiB0aGUgYWdncmVnYXRlOiAxMOKBu8Kz4oGwIGF0IHQg
PSAwIChpc290cm9weSksIDEuMOKAkzEuNcOXMTDigbvigbUgYXQgdCA9IDEgb24gaGV4IChPKHTC
siksIEgtTVMtNCBjb25jb3JkYW50KSwgMTDigbvCs+KBsCBhdCBldmVyeSB0IG9uIGN1YmljLgoK
KipGaW5kaW5ncy4qKgotICoqRmlyc3Qtb3JkZXIgcHJvdGVjdGlvbiBDT05GSVJNRUQgb24gZXZl
cnkga2V5IGFuZCBib3RoIGFybXM6IHxTX3R8IOKJpCA0LjnDlzEw4oG7wrnCsyoqIChGLU1TLTMg
U0lMRU5UIGJ5IHRoaXJ0ZWVuIG9yZGVycykuIFRoZSBzcGVjaWVzIHNwbGl0IHVuZGVyIHRleHR1
cmUgaXMgc2Vjb25kIG9yZGVyLCByX2FnZyh0KSDiiYggzrrigoIgdMKyLCB3aXRoIHRoZSBjdWJp
YyBmaXQgcmVzaWR1YWwgM+KAkzfDlzEw4oG7wrnCuSBvbiB0aGUgbWVtbyBiYXNpcyBhbmQgdGhl
IDQtdGVybSBhbmQgaGFsZi13aW5kb3cgZml0cyBhZ3JlZWluZyB0byDiiaQgNy41w5cxMOKBu+KB
ti4KLSAqKlRoZSBkZWxpdmVyZWQgY29uc3RyYWludCBjdXJ2ZSAoaGV4IHN0YWNraW5nIGJyYW5j
aCk6IM664oKCKFMyLUXigoIpID0g4oiSMS40MznDlzEw4oG7wrMgKHN0ZXApIC8g4oiSMS44OTbD
lzEw4oG7wrMgKGdlbTgpKiogdW5kZXIgSGlsbDsgdGhlIEhTLW1lYW4gc2NoZW1lIGFncmVlcyB0
byAwLjglIOKAlCB0aGUgc3BsaXQgaXMgbm90IGFuIGF2ZXJhZ2luZy1zY2hlbWUgYXJ0aWZhY3Qu
IFNpZ24gbWF0Y2hlcyByX3h0YWwoUzItReKCgikgKEgtTVMtMyBjb25jb3JkYW50IG9uIGhleCku
IEF0IGZ1bGwgbCA9IDIgdGV4dHVyZSAodCA9IDEpIHRoZSBzcGVjaWVzIHNwbGl0IGlzIDEuNOKA
kzEuOcOXMTDigbvCszsgYXQgdCA9IOKIkjAuNSwgMy424oCTNC43w5cxMOKBu+KBtC4gzrrigoIo
UzItaCkgPSDiiJIyIHRvIOKIkjPDlzEw4oG74oG2IOKAlCB0aGUgYWRtaXh0dXJlLWNvbnRyb2xs
ZWQgc3BsaXQgaXMgdGhyZWUgb3JkZXJzIHNtYWxsZXIsIE8odMKzKS1jbGFzcy4KLSAqKkN1Ymlj
IGwgPSAyIHRleHR1cmUgTlVMTCAoYSBzdHJ1Y3R1cmFsIGZpbmRpbmcsIFIxLW1hY2hpbmUgd2l0
aCBSMiByZWFkaW5nKToqKiBvbiBib3RoIGN1YmljIGNvbmZpZ3VyYXRpb25zIGFuZCBib3RoIGRl
c2NyaXB0b3IgYXhlcywgdGhlIHRleHR1cmVkIGFnZ3JlZ2F0ZSB0ZW5zb3IgaXMgKmlkZW50aWNh
bCogdG8gdGhlIHVudGV4dHVyZWQgb25lIChtYXggfOKfqEPin6lfe3Q9MX0g4oiSIOKfqEPin6lf
e3Q9MH18IOKJiCAxMOKBu8K5wrIsIHBvc3QtaG9jIGRpYWdub3N0aWMpIGFuZCBldmVyeSBzcGVj
aWVzIHF1YW50aXR5IGlzIHplcm8gdG8gcm91bmRpbmcuIFJlYXNvbjogdGhlIGwgPSAyIGhhcm1v
bmljIHN1bW1lZCBvdmVyIHRoZSBvY3RhaGVkcmFsIG9yYml0IG9mIGEgY3ViaWMgZ3JhaW4ncyBh
eGlzIHZhbmlzaGVzICjOoyBvdmVyIHRoZSB0aHJlZSBvcnRob25vcm1hbCDin6gwMDHin6kgZGly
ZWN0aW9ucyBvZiBQ4oKCKG7MgsK34bqRKSA9IDA7IGxpa2V3aXNlIGZvciDin6gxMTHin6kpLCBz
byBhIGN1YmljIGNyeXN0YWwgY2FycmllcyBubyBsID0gMiB0ZXh0dXJlIGNvZWZmaWNpZW50IOKA
lCB0aGUgZmlyc3QgdGV4dHVyZSBhIGN1YmljIGFnZ3JlZ2F0ZSBjYW4gZmVlbCBpcyBsID0gNC4g
VGhlIHNwZWNpZXMtdW5pdmVyc2FsaXR5IGlkZW50aXR5IGlzIHRoZXJlZm9yZSAqKmV4YWN0IHRv
IGFsbCBvcmRlcnMgaW4gYW4gbCA9IDIgZmliZXIgdGV4dHVyZSBvbiB0aGUgZmNjIHN0YWNraW5n
IGJyYW5jaCoqLCBhbmQgdGhlIGhleCBicmFuY2gncyDOuuKCgiBpcyB0aGUgb25seSB0ZXh0dXJl
IGNvbnN0cmFpbnQgY3VydmUgdGhpcyBmYW1pbHkgZGVsaXZlcnMuIEUtTVMtNSdzIHJlZ2lzdGVy
ZWQgbCA9IDQgc3VjY2Vzc29yIGFybSBpcyB3aGVyZSB0aGUgY3ViaWMgYnJhbmNoJ3MgZmlyc3Qg
Y29uc3RyYWludCBjdXJ2ZSB3b3VsZCBjb21lIGZyb20uIEgtTVMtMyBhbmQgSC1NUy01IGFyZSBO
T1QgY29uY29yZGFudCBiZWNhdXNlIG9mIHRoaXMgKHRoZWlyIGN1YmljIGNsYXVzZXMgcHJlc3Vw
cG9zZWQgYSBub24temVybyBjdWJpYyDOuuKCgikg4oCUIGEgcHJlZGljdGlvbiByZWZ1dGVkIGJ5
IHN5bW1ldHJ5LCByZWNvcmRlZCBhcyBzdWNoLgoKIyMgNC4gSHlwb3RoZXNlcyAoY29tcGFyZSBz
dGVwLCBydW4gbGFzdCk6IDMvNSBjb25jb3JkYW50CgpILU1TLTEgT0sgwrcgSC1NUy0yIE9LIMK3
IEgtTVMtMyBNSVNTIChjdWJpYyBjbGF1c2U7IHNlZSB0aGUgY3ViaWMgbnVsbCkgwrcgSC1NUy00
IE9LIMK3IEgtTVMtNSBNSVNTIChtb290OiBjdWJpYyDOuuKCgiDiiaEgMCkuIFRoZSB0d28gbWlz
c2VzIGFyZSB0aGUgc2FtZSBmaW5kaW5nLgoKIyMgNS4gSG9uZXN0eSBpdGVtcyAoY2hhdCkKCi0g
KipILU1TLTIg4oCUIGhhbHZpbmcgY3JpdGVyaW9uIHVuZGVmaW5lZCBhdCDOuuKCgiA9IDAuKiog
QS0yLjQgZGVmaW5lZCBgaGFsdmluZ19kZXZfa2FwcGEyYCBhcyBhIHJlbGF0aXZlIGNoYW5nZSBv
ZiDOuuKCgjsgb24gdGhlIGN1YmljIGtleXMgzrrigoIg4omIIDEw4oG7wrnigbUgYW5kIHRoZSBy
YXRpbyBpcyAwLzAgKHZhbHVlcyA0LjggYW5kIDM3KS4gVGhlIGZyb3plbiBjb21wYXJhdG9yJ3Mg
cGVyLWxlZyBjaGVjayBgaGFsdmluZ19kZXYg4omkIDHDlzEw4oG74oG0YCB3aWxsIHRoZXJlZm9y
ZSBNSVNTIG9uIHRoZSBmb3VyIGN1YmljIGtleXMgb24gKipib3RoKiogbGVncyAodGhlIGNoYXQt
dnMtY2hhdCBzYW5pdHkgcnVuIHNob3dzIGV4YWN0bHkgdGhlc2UgOCBpdGVtcyBwbHVzIHRoZSAy
IGV4cGVjdGVkIElOREVQRU5ERU5DRSBpdGVtcywgNDA1LzQxNSBQQVNTKS4gUHJlLWNsYXNzaWZp
ZWQgZGVmaW5pdGlvbmFsICh0aGUgRy1TMkMxLVcgSC1XLTYgY2xhc3MpOiB0aGUgZml4IGlzIGEg
Zmxvb3JlZCBkZW5vbWluYXRvciBtYXgofM664oKCfCwgzrrigoJfYWJzX2Zsb29yID0gMTDigbvi
gbYpLCBhbHJlYWR5IHRoZSBzZW1hbnRpY3Mgb2YgdGhlIGZyb3plbiB0d28tbGVnIM664oKCIHRv
bGVyYW5jZS4gVGhlIGNoZWNrcG9pbnQgb2YgcmVjb3JkIGlzIGxlZnQgYXMgY29tcHV0ZWQ7IGNv
bXBhcmF0b3IgdjEuMSB3aXRoIHRoZSBmbG9vcmVkIHJ1bGUgaXMgcHJvcG9zZWQgZm9yIHRoZSBh
dXRob3IncyBlbGVjdGlvbiBhdCB0aGUgUzkgc3RlcCwgdG8gYmUgZnJvemVuIGJlZm9yZSBhbnkg
cmUtZW1pc3Npb24gKHRoZSBHLTJhLUwxIHByZWNlZGVudCkuIE5vdGhpbmcgdmVyZGljdC1iZWFy
aW5nIGRlcGVuZHMgb24gaXQuCi0gKipILU1TLTMg4oCUIEYtQ1RSTC1BRE1JWCBhcyBjb2RlZCBp
cyBhIHRhdXRvbG9neS4qKiBUaGUgY29udHJvbCB3YXMgaW1wbGVtZW50ZWQgYXMgInByb2plY3Rl
ZCBzcGVlZHMgb3ZlciBwcm9qZWN0ZWQgc3BlZWRzIOKIkiAxIiBhbmQgcmV0dXJucyAwIGlkZW50
aWNhbGx5OyBpdCB0ZXN0cyBub3RoaW5nLiBUaGUgc3Vic3RhbnRpdmUgYWRtaXh0dXJlIGNoZWNr
IGlzIEgtTVMtMiAoc2lnbiBhbmQgbWFnbml0dWRlIG9mIHJfeHRhbChTMi1oKSBhZ2FpbnN0IOKI
kkNvdl9FTSjOu19MLCB2KS8oM+KfqHbin6kpLCBjb25jb3JkYW50IG9uIGFsbCBlaWdodCBrZXlz
KTsgRi1DVFJMLUFETUlYJ3MgYHBhc3NlZCA9IFRydWVgIGlzIGRpc2Nsb3NlZCBhcyB2YWN1b3Vz
LCBub3QgYXMgZXZpZGVuY2UuIFRoZSBDQyBsZWcgaXMgYXNrZWQgdG8gaW1wbGVtZW50IHRoZSBj
b250cm9sIGFzIHRoZSBtZW1vIHN0YXRlcyBpdCAoZWlnZW52ZWN0b3JzIHJlcGxhY2VkIGJ5IHRo
ZWlyIHRyYW5zdmVyc2UgcHJvamVjdGlvbnMgb24gdGhlIHF1YXNpLXRyYW5zdmVyc2UgYnJhbmNo
ZXMsIHRoZW4gcl94dGFsKFMyLWgpIHJlY29tcHV0ZWQpIGFuZCB0byByZXBvcnQgdGhlIG51bWJl
ci4KLSAqKkgtTVMtNCDigJQgcHJlLWxvY2sgY2F0Y2ggZHVyaW5nIGluc3RydW1lbnQgYnVpbGQg
KG5vIGFydGlmYWN0IGNvbnN1bWVkIGl0KToqKiB0aGUgZmlyc3QgUzQgc2VsZi10ZXN0IGFzc3Vt
ZWQgdGhlIGJhbmtlZCBoZXggdGVuc29ycyBhcmUgdHJhbnN2ZXJzZWx5IGlzb3Ryb3BpYzsgdGhl
eSBhcmUgdGV0cmFnb25hbC1mb3JtIChDNjYgZnJlZSksIHNvIHRoZSBxU0ggYnJhbmNoIGRlY291
cGxlcyBleGFjdGx5IG9ubHkgb24gdGhlIHN5bW1ldHJpemVkIGFybSAoYikuIExhYmVscyBvbiBh
cm0gKGEpIGFyZSBieSBtYXhpbXVtIG92ZXJsYXAgd2l0aCDhupEgw5cga8yCOyB0aGUgc3BlY2ll
cyBtZWFucyBhcmUgbGFiZWwtZnJlZSwgYW5kIHRoZSAoYSkvKGIpIGFybXMgYWdyZWUgdG8gMsOX
MTDigbvigbUuCi0gVDE6IDQgKyAxIG51bWVyaWMgZm9ybWF0dGluZyBjb2xsaXNpb25zIGxvZ2dl
ZCBvbiB0aGUgY2hlY2twb2ludC9jb21wYXJlIChiYXJlIG51bWVyaWMgYmFzZSBwYXR0ZXJucyBp
bnNpZGUgbG9uZ2VyIGZsb2F0IGxpdGVyYWxzIOKAlCB0aGUgY29udGV4dHVhbCBydWxlIHdvcmtp
bmc7IG5vbmUgYSBmb3JiaWRkZW4gcmVmZXJlbmNlKS4KCiMjIDYuIFJlZ2lzdGVycyAoY2hhdC1z
aWRlOyBub3RoaW5nIGZvbGRlZCkKCkV2ZXJ5IG51bWJlciBSMS1tYWNoaW5lIChzaW5nbGUtbGVn
IHVudGlsIENDKS4gUmVhZGluZ3MgUjIgY29uZGl0aW9uYWwgb24gRS1NUy0xKGEpLCB0aGUgdW50
ZXh0dXJlZCBpbXBvcnQsIEsgPSDiiIUsIHRoZSBrZXJuZWwgZWxlY3Rpb24sIGFuZCBBLTIuMyAo
SFMgb3BlcmF0aW9uYWxpemF0aW9uKTogKGkpIHNwZWNpZXMgdW5pdmVyc2FsaXR5IGlzIGFuIGlk
ZW50aXR5IG9uIHRoZSB1bnRleHR1cmVkIGFnZ3JlZ2F0ZSAoY29udHJvbC12ZXJpZmllZCk7IChp
aSkgaXQgaXMgcHJvdGVjdGVkIHRvIGZpcnN0IG9yZGVyIGluIGFuIGwgPSAyIGZpYmVyIHRleHR1
cmUgb24gZXZlcnkgY29uZmlndXJhdGlvbiwgYW5kIHRvIGFsbCBvcmRlcnMgb24gdGhlIGN1Ymlj
IGJyYW5jaDsgKGlpaSkgdGhlIGhleCBicmFuY2gncyBzZWNvbmQtb3JkZXIgc3BsaXQgaXMgzrri
goIgdMKyIHdpdGggzrrigoIgPSDiiJIxLjQ0w5cxMOKBu8KzIC8g4oiSMS45MMOXMTDigbvCsyDi
gJQgdGhlIGRlbGl2ZXJlZCBjb25zdHJhaW50IGN1cnZlIG9uIHRoZSB0ZXh0dXJlIGltcG9ydDsg
KGl2KSB0aGUgYWRtaXh0dXJlIG1hcHMgzrtfTCAo4p+ozrtfTOKfqSA14oCTOcOXMTDigbvCsywg
bWF4IDMuNOKAkzQuMyUgb24gdGhlIHFTVi9xVDIgYnJhbmNoKSBhcmUgdGhlIHNpbmdsZS1jcnlz
dGFsIGRpZmZlcmVudGlhdG9yIGZyb20gdGhlIGlzb3Ryb3BpYy1jb250aW51dW0gbGFuZSAoRGFu
aWVsZXdza2ksIMKnMy4yKS4gTm8gb2JzZXJ2YWJsZSwgbm8gYnJpZGdlLCBubyBTSSB2YWx1ZSwg
bm8gZXZhbHVhdGlvbiBhZ2FpbnN0IGFueSBib3VuZDsgbm8ga2lsbCBjbGFpbWVkIG9yIHBvc3Np
YmxlIGhlcmUuCgojIyA3LiBFc3RhdGUKCnwgQXJ0aWZhY3QgfCBtZDUgfCBTaXplIHwKfC0tLXwt
LS18LS0tfAp8IGBzdGFnaW5nX21lbW9fR19NU0NTMV92Mi5tZGAgfCBgM2YzMDI2MmVhZWM0NjFm
YjVmZDMyMDI4MzVmN2RlMzdgIHwgMzQsODM3IEIgfAp8IGBHX01TQ1MxX0xPQ0tfUkVDT1JELm1k
YCB8IGAzZGJlOTUzYmFkYjZjMDMwZWYxZDQ0OWFkYmFjMjA0NGAgfCA3LDI4OSBCIHwKfCBgZ19t
c2NzMV9zY2hlbWFfdjFfMC5qc29uYCB8IGA3NmE0MmRiM2ZkNmFkODJlNDg1NzUyYmMyZGRiMjRk
NWAgfCAzLDkwNiBCIHwKfCBgZ19tc2NzMV9jb21wYXJlX3YxXzAucHlgIHwgYDIyNDMyYjI5MmFl
MGE5ZDVjOTFhNmNiN2FhNjc1MDJmYCB8IDE4LDU0MSBCIHwKfCBgdG9vbHMvdDEvVDFfZm9yYmlk
ZGVuX0dfTVNDUzEudHh0YCAvIGB0MV9zY2FuLnB5YCAvIGBUMV9iYXNlX2F1dGhvcl8yMDI2MDkx
OS50eHRgIHwgYGZlZjI4Mjcx4oCmYCAvIGA2Yjg2MjkwMOKApmAgLyBgMDUzMDIyMTDigKZgIHwg
MSw0MzMgLyAxLDk2NyAvIDE0MyBCIHwKfCBgZ19tc2NzMV9jaGF0bGVnLnB5YCB8IGBkYjVmNTFk
ZDllZjdmNTRkZDA4MjY5OTFkNTk0NjgxYmAgfCAzNCw2MDYgQiB8CnwgYGdfbXNjczFfY2hhdGxl
Z19jaGVja3BvaW50Lmpzb25gIHwgYGMwNGMwYjhlYTM0Y2ZlNjBmMjMxYWEwNjgyOGU2Y2U0YCB8
IDMzLDI4OSBCIHwKfCBgZ19tc2NzMV9jaGF0bGVnX2NvbXBhcmUuanNvbmAgfCBgN2I5MzNjMDhi
OTJkNTdiOTUyM2YyY2VlNGZmMDc2YmFgIHwgMywyNzcgQiB8CnwgYHJ1bl9jaGF0bGVnLmxvZ2Ag
fCBgNzk3Mzc2ODdjODU3MTUzYzA3ZjNmOWUyYmFmM2MyNmJgIHwg4oCUIHwKfCBwaW4gc291cmNl
cyBYLTEgLyBYLTMgLyBYLTQgLyBYLTUgfCBgMjAwZTdhOGLigKZgIC8gYGFhYWUyMDY34oCmYCAv
IGBlYzg3ZTQyZuKApmAgLyBgZGY0MTNhN2PigKZgIHwgMiw3NjcgLyAxMSw0NTQgLyA4LDE0MCAv
IDEsOTIwIEIgfAo=
=====END-EMBED name=G_MSCS1_CHATLEG_EXECUTION_REPORT.md=====

