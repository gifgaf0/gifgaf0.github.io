# G-2a-A1 — CC LEG DISPATCH (P-4 single-file in-band; P-4.b armor; P-4.c lone delivery)

**Gate:** G-2a-A1 (Gate 2a: Baryon Spin Geometry & Factor Assignment — is the ρ₆/Cℓ(6) structure the baryon's spin factor, decided on the instantiated substrate). **Date:** September 20, 2026.
**Base ledger:** `SQT_Master_Ledger_v4_83_CANONICAL.md` md5 `40009ec0197876b130766f1ae7494360` (the canonical ledger is deliberately not in the repository; it is not needed for this leg).
**Lock chain (all FROZEN):** memo v2 `626aa868844220eb6c3801ef07a77783` (61,562 B) · lock record `8732c390be1f442faa589bf04f7ffe9f` (Addendum A-2.1–A-2.8 operationalizations, binding) · schema v1.0 `53111e0360dac138b02d5914efe85d5c` · comparator v1.0 `5afcd5890a9248f01a3d8a203e349039` (asserts the schema md5; 15 selftest suites) · gate T1 list `2026b782db3905d9f2ce35733823618c` (24 patterns = base `05302210cc4ceb70553acbe8379e9fc3` + stratum `ea3bbbbd98da8f4e9eee267beda492b7`; scanner `6b86290090a8c84f1b1a0a99ec0bf697`) · action-of-record extract `940b0bee4b2112e911ae738c3db2bc3d` (12,912 B).
**Answers and elections of record (T3):** Q-A1-1 16 real components / 8 complex amplitudes, the oriented term not U(1)-phase-invariant · Q-A1-2 the M.ONT envelope is a separate component (H2) · Q-A1-3 no real-unit-splitting term · E-A1-1…8 all **(a)**.
**Chat-leg state at dispatch:** run EXECUTED (checkpoint `8f657a23a68ef082f99a7579af78348c`; chat-vs-chat comparator sanity `ba0876074396e697614a4daa78da7682`); all Phase-0 controls PASS; the verdict class and every witness are in the quarantined checkpoint/report. **D-T1 RETIRED:** the T1 lists are embedded here; your instrument must halt without them and must scan itself, the memo and the extract at every invocation.

**T1-scan exemptions (the G-POLY1 justified-exemption class):** the three list embeds necessarily contain every pattern; the dispatch **plaintext** (minus those three embeds and minus the base64 armor *bodies*, which are transport encoding, not text) scans CLEAN against the gate list (0 hits, 0 numeric collisions); every payload scans CLEAN on its own before embedding. **D-A1-1 (recorded):** one alphabetic pattern (index 9) occurs three times as a substring coincidence inside one base64 armor body — an armor-transport collision (the alphabetic analogue of the contextual numeric rule), logged by pattern index; the decoded payload is CLEAN.

**ACTIVATION FLAG: `ACTIVATE: G-2a-A1-CC-LEG-1`** — proceed only if this line is present verbatim.

## 0. Blindness clause (read first)

Seven embeds are **QUARANTINED** (base64-armored): the chat instrument, checkpoint, chat-vs-chat compare file, run log, execution report, and the chat-side pre-lock sanity-check script and its log. **Do not decode any of them until step 4.** Build your instrument from the memo (§0–§2, §4–§7, §A), the lock record (Addendum A-2 — binding definitions) and the schema ONLY, from scratch, in your own structure. Commit your checkpoint BEFORE any armor is opened and cite that commit as the pre-consultation checkpoint. If your read of this file is paged or truncated, locate embed boundaries by grepping sentinel lines only (the G-QUANTA H-CC-2 practice).

## 1. Embed inventory

| Embed | md5 | Size | Handling |
|---|---|---|---|
| `staging_memo_G_2a_A1_v2.md` | `626aa868844220eb6c3801ef07a77783` | 61,562 B | plain |
| `G_2a_A1_LOCK_RECORD.md` | `8732c390be1f442faa589bf04f7ffe9f` | 11,279 B | plain |
| `g_2a_a1_schema_v1_0.json` | `53111e0360dac138b02d5914efe85d5c` | 6,405 B | plain |
| `g_2a_a1_compare_v1_0.py` | `5afcd5890a9248f01a3d8a203e349039` | 20,890 B | plain |
| `tools/t1/T1_forbidden_G_2a_A1.txt` | `2026b782db3905d9f2ce35733823618c` | 241 B | plain |
| `tools/t1/T1_base_author_20260919.txt` | `05302210cc4ceb70553acbe8379e9fc3` | 143 B | plain |
| `tools/t1/T1_stratum_G_2a_A1.txt` | `ea3bbbbd98da8f4e9eee267beda492b7` | 98 B | plain |
| `tools/t1/t1_scan.py` | `6b86290090a8c84f1b1a0a99ec0bf697` | 1,967 B | plain |
| `inputs/paper_II_3_4_4_and_3_4_7_extract.md` | `940b0bee4b2112e911ae738c3db2bc3d` | 12,912 B | plain |
| `g_2a_a1_chatleg.py` | `6360709d6a7eb5fc3df7fc8fd26dc36a` | 53,706 B | QUARANTINED (base64) |
| `g_2a_a1_chatleg_checkpoint.json` | `8f657a23a68ef082f99a7579af78348c` | 8,247 B | QUARANTINED (base64) |
| `g_2a_a1_chatleg_compare.json` | `ba0876074396e697614a4daa78da7682` | 66,541 B | QUARANTINED (base64) |
| `run_chatleg.log` | `c38903300a0bbd8bbd964618e9774c7e` | 782 B | QUARANTINED (base64) |
| `G_2a_A1_CHATLEG_EXECUTION_REPORT.md` | `3c82ded06a150343f01c0d92947c37b7` | 16,601 B | QUARANTINED (base64) |
| `prechecks/precheck_algebra.py` | `cf36395dba7ff35127f40e9f805ff1c7` | 9,120 B | QUARANTINED (base64) |
| `prechecks/precheck_algebra.log` | `81b5512817f7eebeb668817f6b3562f9` | 1,053 B | QUARANTINED (base64) |

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

Expected: nine `OK` lines and seven `SKIP` lines. Any assertion failure → HALT, report the md5 seen, do not build. Then run `python3 tools/t1/t1_scan.py tools/t1/T1_forbidden_G_2a_A1.txt staging_memo_G_2a_A1_v2.md G_2a_A1_LOCK_RECORD.md inputs/paper_II_3_4_4_and_3_4_7_extract.md` → all CLEAN; and `python3 g_2a_a1_compare_v1_0.py selftest` → SELFTEST PASS (this also proves the schema md5 you hold is the frozen one).

## 3. Build and run (blind)

1. Read the memo §2.1–§2.4 (the arena; the four forcing tests T1–T4; the ℍ criteria and candidates), §4 (the phases), §5 (falsifiers and controls), §7 (pinned inputs and adopted facts), and the lock record A-2.1–A-2.8 (conventions; the four sl₂-classes; the spinorial 2O; the Frobenius–Schur count; the homotopy bookkeeping; the Phase-2 pinned witness with its fixed profile; the 1344 complement search; the checkpoint discipline). Where the memo and A-2 differ in specificity, A-2 governs.
2. Write `g_2a_a1_ccleg.py` from scratch. Requirements: md5-guard the memo (`626aa868844220eb6c3801ef07a77783`, 61,562 B), the gate T1 list (`2026b782db3905d9f2ce35733823618c`, 241 B) and the extract (`940b0bee4b2112e911ae738c3db2bc3d`, 12,912 B) before any computation; T1 self-grep of your instrument, the memo and the extract at every invocation (scan rule = `t1_scan.py`; halt on any hit; no override flag); **Phase 0 exactly as memo §4 (0a)–(0e)** — in (0b) determine the **full continuous stabilizer of the oriented density inside so(16)** (its dimension and its identification), not merely the invariance of the 14 g₂ generators, together with the generic-so(16) negative control, the diagonal-phase subgroup order and the conjugation fact; halt → INDETERMINATE on any control failure; **Phase 1** T1–T4 with every witness key of the schema (integers exact; the spinorial-2O block may be floating point with the defect thresholded per the schema); the 1344 complement search per A-2.7; **Phase 1b** the P-ℂ checks and the five-candidate screen with the criterion values in the schema domain (the code string rule you use must be stated in your return); **Phase 2** on the pinned texture and its non-line control per A-2.6; **Phase 3** the verdict by the schema rule, last. **Requested variations (independence upgrade):** build g₂ as the stabilizer of the 3-form φ in so(7) rather than as derivations; enumerate SL(2,7)'s classes yourself for the Frobenius–Schur count; write your own exact-sequence bookkeeping for T3; you may optionally add the MV-G1 crystallized core as a second Phase-2 object (report it as an extra; the schema's Phase-2 keys refer to the homogeneous pinned witness).
3. Emit `g_2a_a1_ccleg_checkpoint.json` conforming to `g_2a_a1_schema_v1_0.json` (`required_top`; every typed key of Phases 0–3; `leg` = `cc`; your real `instrument_md5`; the eight elections as `"a"`; `t1_scan` = CLEAN for instrument/memo/extract). Put every adopted mathematical fact you rely on under a `citations` key and anything else under `extras` (both ignored by the comparator). **Commit** with the checkpoint md5 in the message — the pre-consultation checkpoint.
4. Emit nothing else before consulting; the verdict is the LAST computation.

## 4. Consult and compare

Only now: `python3 extract.py dispatch.md --decode-quarantined`, then

```
python3 g_2a_a1_compare_v1_0.py compare g_2a_a1_chatleg_checkpoint.json g_2a_a1_ccleg_checkpoint.json --schema g_2a_a1_schema_v1_0.json --out g_2a_a1_twoleg_comparison.json
```

Every check is expected to PASS except where the quarantined execution report (§7, H-A1-1/H-A1-2) pre-classifies a miss as definitional — read that section only after your commit, and classify every miss you see as representational, definitional, or substantive in your return. Do NOT alter your checkpoint to avoid a miss; never edit either checkpoint. The comparator and schema are frozen; if you believe either is wrong, say so in H-CC and leave them unchanged. Any schema v1.1 is frozen chat-side only on the author's S9 election.

## 5. Return (single file, P-4 mirrored)

One markdown file with byte-exact embeds (same sentinel format) of `g_2a_a1_ccleg.py`, `g_2a_a1_ccleg_checkpoint.json`, `g_2a_a1_twoleg_comparison.json` (and the chat-side comparison you ran); the branch name and commit hashes (pre-consultation first); CC-DD-1..n (definitions you had to fix yourself); H-CC-1..n (self-caught bugs, disagreements with the memo/lock record/schema); deviations; T1 state; the Phase-0 stabilizer dimension and identification you found; the H-screen code rule you used; run time. Repository placement per the gate convention: `g2aa1_gate/` for the CC-leg artifacts (the chat-side estate lands later in `g2aa1_gate/estate/` by a successor PR).

## 6. Embeds

=====BEGIN-EMBED name=staging_memo_G_2a_A1_v2.md md5=626aa868844220eb6c3801ef07a77783 bytes=61562 encoding=raw=====
# STAGING MEMO — Gate G-2a-A1 (Gate 2a: Baryon Spin Geometry & Factor Assignment — is the ρ₆/Cℓ(6) structure the baryon's *spin* factor, decided on the instantiated substrate) — v2

**Date:** September 20, 2026 (v2; draft v1 September 20, md5 ee3ce0e6, 50,251 B — superseded by this file; §A records every change). **Base:** `SQT_Master_Ledger_v4_83_CANONICAL.md` (md5 `40009ec0197876b130766f1ae7494360`, 1,589,553 B). **Status: LOCKED on the author's directive of September 20, 2026** ("LSF-δ Sweep, T1 List, and Lock G-2a-A1": Q-A1-1…3 answered; E-A1-1…8 all elected (a); the LSF-δ sweep executed and §12 filled; the gate T1 list built and pinned). The lock md5 of this file is recorded in `G_2a_A1_LOCK_RECORD.md`; the memo does not contain its own hash. **Lineage:** §2.85 → §2.87 → §2.87.A (Assignment I / II surfaced) → §2.87.B–I (G-2a-S1…S10) → §2.87.J (G-2a-L1: B3 Assignment NEUTRAL; "the discriminator is the named successor") → **this gate**.

**Opening directive (author, September 20, 2026):** "We are opening Gate 2a to resolve the physical identification of the baryon's spin geometry." The five required contents (analytical frame / factor assignment; physical instantiation; execution leg & falsifiers; LSF-δ obligations; V4.84 housekeeping) are §2, §2.4–2.5, §4–§5, §3 + §12, and §10.

## A. v1 → v2 record (the author's answers and elections applied; one chat-self-caught design correction)

- **A-2.1 (Q-A1-1, answered):** the field content of record is **16 real components (8 complex amplitudes)**, and the oriented term O is **not** U(1)-phase-invariant. Consequences applied: the continuous internal symmetry of the action of record is exactly G₂; the phase subgroup surviving O is finite (expected ℤ₃ for a term cubic in the complex amplitudes — Phase 0 (0b) determines the order and records the conjugation structure), so Sym_int = G₂ × (finite); T1's phase-character clause becomes trivial (Hom(2O, ℤ₃) = 1); T3's vacuum manifold of record is the accidental two-body sphere V = S¹⁵ (§2.3 T3), with the Sym_int-orbit table retained as the *locking inventory*; the v1 "half-quantum −1 trap" is replaced by the locked-lift trap (A-2.4).
- **A-2.2 (Q-A1-2, answered):** the M.ONT texture envelope is declared **a genuinely separate component (H2)**. Consequences: the §3.4.5 in-𝕆 hopfion (H1) is a *different object* from the declared envelope; its exclusion is carried as the "envelope-in-𝕆 kill" **control** (§2.3 T3(i)), not as a finding about M.ONT; H2 remains an import (R3) and the fold annotates the M.ONT declaration line with the screen's H2 outcome.
- **A-2.3 (Q-A1-3, answered):** the action of record contains **no** term splitting the real unit from Im𝕆. Consequences: H-A1-5 stands as the scoping note (§6); V₂ = S¹⁵ is recorded in Phase 0 (0d) as the vacuum manifold of record; the successor question it raises (vacuum selection / vortex protection in the 16-component substrate) is **registered in §9 as a named open item, not executed here**.
- **A-2.4 (design correction, chat-self-caught after v1, before any computation — the G-MSCS1 A-1 class):** v1's Phase-2 hypothesis ("internal G₂ part trivial; 2π monodromy +Id") was mis-stated. For a texture confined to an associative 3-plane ℍ_L, the locked family maps the spatial rotation by α into SO(4) = Stab_{G₂}(ℍ_L) acting on Im ℍ_L as the rotation by α, with kernel the long-root SU(2) (the pointwise stabilizer of ℍ_L); the internal image of the spatial 2π loop is therefore **path-dependent through the stabilizer** — {Id, σ_ℍ}, where σ_ℍ is the quaternion-subalgebra involution (−1 on ℍ_L^⊥) — and the invariant statement is about π₁ of the collective-coordinate orbit, not about a "monodromy element". Phase 2 (§4) and H-A1-4 (§6) are restated accordingly; T3(ii) carries the corrected guard. Nothing verdict-bearing changes: T1–T4 are unaffected.
- **A-2.5 (obligations discharged pre-lock):** the LSF-δ sweep of §12 executed on September 20, 2026 (seven clusters; verdicts and transcription ceilings filled); the gate T1 stratum (13 lines, `ea3bbbbd`) appended to the base list (`05302210`) → `tools/t1/T1_forbidden_G_2a_A1.txt` (md5 `2026b782db3905d9f2ce35733823618c`, 241 B, 24 pattern lines); the action-of-record extract pinned (§7); the eight elections recorded (§8).

## 0. What the ledger has already settled (this gate does not re-litigate any of it)

- **§2.85 Parts B–E (R1/R2):** S₃ forces a 4-dimensional symmetric channel but no spin content; spin-3/2 is the faithful 4-dim irrep of 2O = 2·S₄ and does **not** descend to S₄; "the factor of 4 is not in the discrete algebra" — it needs the spinorial promotion −1 ↦ −Id.
- **§2.87 (R1 algebra):** ρ₆ : PSL(2,7) → SO(6) has w₂ ≠ 0; its spin lift is SL(2,7) → Spin(6) ≅ SU(4) = the Cℓ(6) spinor structure; σ₄, σ₄' are the half-spinors; σ₄|_{2O} = the unique genuine 4-dim irrep of 2O; Cℓ(6) ≅ ℂ⊗𝕆; the ρ₈ orbifold is bosonic. **What §2.87 does NOT claim** (its own words): the *physical* claim that the baryon's spin geometry is the ρ₆/Cℓ(6) structure — that is Gate 2a.
- **§2.87.A (R1 + R2):** no single 4 hosts both spin-3/2 and color 3 ⊕ 1 (two proofs); the arena is ℂ⊗𝕆⊗ℍ ≅ (ℂ⊗𝕆) ⊗ (ℂ⊗ℍ), commuting factors; **Assignment I** (standard Furey/Dixon: ℂ⊗𝕆 = color/internal, spin/Lorentz in ℂ⊗ℍ) versus **Assignment II** (octonionic spin: the ρ₆-derived ℂ⊗𝕆 carries the soliton's spatial/rotational geometry, σ₄ = spin-3/2 directly, the central −1 ↦ −Id *is* the spatial FR sign); "μ_n's spin-3/2 requires Assignment II (or an equivalent derivation relocated to ℂ⊗ℍ)"; the ℂ of ℂ⊗𝕆 an honest gap; the ℍ factor identified as the spin/isospin home at R3.
- **§2.87.B–I (S1–S10):** the quartet is forced *given* octahedral 2O symmetry (D1 = 1); the canonical representative is only tetrahedral; octahedral symmetry is recovered at the **motion-group** level (O ≅ S₄, parity law); the motion S₄ and the Fano line-stabilizer S₄ are canonically one group (S5); the flat crystallographic home is maximally symmetric (S7) and **forces −1 ↦ −Id in the ambient-2π meridian channel** (S8), with the residual reduced to the Pin type (S9) and the ℤ/4 layer derived (S10). Standing non-claims throughout: no carrier identification (framework per-strand ℂ² ↔ orbifold spinor), no §2.50 closure.
- **§2.87.J (G-2a-L1, V4.79):** B1 SPLIT, B2 ASSEMBLED-RELOCATED (**the locking lives in the point/motion sector**), B3 lattices banked, **Assignment NEUTRAL** — the discriminator named as this successor; the dynamical clause stays behind M.CW (the I1–I3 ticket).
- **M.ONT declaration (V4.51):** the baryon is **two-component** — a filament core (Borromean linking, ropelength mass) inside a texture envelope carrying the rotor band (= spin) and the proton-as-hopfion commitment; "Assignment I/II untouched." **Author's answer of record (Q-A1-2, September 20, 2026): the envelope is a genuinely separate component.**
- **The action of record — Paper II §3.4.4 / §3.4.7 (V4.26 §3.4-SYM; V4.47 G-INT1), R1, extract pinned in §7:** ψ ∈ ℂ⊗𝕆 — **16 real components, 8 complex amplitudes (Q-A1-1)**; the continuous internal symmetry is G₂ = Aut(𝕆) acting irreducibly on Im(𝕆) = ℝ⁷; the two-body kernel is Schur-forced to a single scalar and is accidentally O(16)-invariant; the only non-O(16) term is the oriented three-form coupling O = ∫ φ_abc ψ_a ∂_xψ_b ∂_yψ_c — a total derivative, active only on defect cores, Fano-line-selective, **not U(1)-phase-invariant (Q-A1-1)**; no term splits the real unit from Im𝕆 **(Q-A1-3)**; imports I1 (target ℂ⊗𝕆), I2 (GP kinetic form), I3 (one scale), plus the roton profile. **§3.4.4's own module correction:** the PSL(2,7) *permutation* representation, in which ℝ⁷ = 1 ⊕ 6, "is the wrong module — G₂ does not act on the seven imaginaries by permutations"; only F₂₁ lifts unsigned, all 168 lift signed into an order-1344 group (§2.79).
- **§2.88.D.2 (G-INT1):** on a Fano-line core the internal fluctuation channel lifts a chiral pair {0, ±iσ}; 7 = 1 ⊕ 3 ⊕ 3̄ under the realized F₂₁; the full relaxed 7-component defect-core BdG solve was deferred "with the Gate-2a trigger flagged for if/when the explicit chiral-mode structure on the core is needed."
- **§2.D-FC / §2.77 (R1):** SL(2,7) has six ordinary irreps (1, 3, 3, 6, 7, 8) and five genuine ones (4, 4, 6, 6, 8); σ₄/σ₄' are a Galois pair.

**Consequence that frames this gate.** Every prior G-2a screen tested the *representation theory* of a locking that both Assignments share, and could not separate them (S1: "both adopt the transverse-factor structure and pass NC1–NC3 identically"; L1 B3: NEUTRAL). The Assignments differ in exactly one thing that the *instantiated substrate* — not the abstract algebra — can decide: **through which tensor factor the physical spatial rotation group acts.** Assignment II is the claim that the substrate's own ℂ⊗𝕆 field carries the spinorial Cℓ(6) action of the locked rotations (the central −1 of Spin(6) realized on ℂ⊗𝕆 = 4 ⊕ 4̄ as the FR sign). Assignment I is the claim that the ℂ⊗𝕆 field is rotation-bosonic (an internal label transported, if at all, by octonion automorphisms) so that the spin factor must be a *commuting* ℍ factor. Whether the substrate's symmetry group and target topology can carry the spinorial action at all is a configuration-independent property of the action of record; it therefore cannot be steered by choosing a core, and it is decided without ever consulting the magnetic-moment target. That is the design principle of this gate and the answer to the directive's "avoiding any post-hoc selection" requirement.

## 1. Object

**Question (one sentence):** in the instantiated substrate of record — the ℂ⊗𝕆-valued Gross–Pitaevskii/Bjerknes field with internal symmetry group Sym_int (pinned in Phase 0 from the action of record) and vacuum manifold of record V — can the ρ₆/Cℓ(6) spinor structure of §2.87 be carried by the octonionic factor as the physical, rotation-locked spin factor of the baryon (Assignment II), or is the octonionic factor rotation-bosonic so that the spin factor must be a commuting ℍ factor (Assignment I) — and, in the latter case, which structure in the K₇/supersolid substrate, if any, instantiates that ℍ factor?

**Verdict classes (pre-registered; assigned by the machine, last, from the encoded test results — no verdict text in any instrument):**
- **ASSIGNMENT-I-FORCED** — all four forcing tests T1–T4 (§2.3) hold on the action of record: no genuine 2O quartet in ℂ⊗𝕆 under Sym_int; the Cℓ(6) spinor action is not a symmetry of the instantiated action; the target-sector FR ℤ₂ vanishes; the substrate's internal 7 carries no ρ₆. The ρ₆/Cℓ(6) structure is then **not** the spin factor — forced away by the substrate, configuration-independently — and the spin factor is a commuting ℍ factor whose instantiation status is delivered by the §2.4 screen. R2, conditional on the imports in §7. **A-priori expected class** (§6; the §13 disclosure).
- **ASSIGNMENT-II-REALIZABLE** — at least one of T1–T4 fails on the action of record (a falsifier of §5 fires two-leg). The octonionic factor *can* carry a spinorial locked action; the Assignment is then a dynamical question, which this gate cannot decide (M.CW) — the gate **halts pre-verdict** with an H-item and a named successor (the locking computation on a 3-D core), per the G-BKZ32 pre-verdict-halt precedent. No Assignment-II *confirmation* is possible here.
- **UNDECIDED-BY-SUBSTRATE** — Phase 0 cannot pin Sym_int from the action of record in a way that decides a test (the only route: an ambiguity in the spatial–internal coupling structure, F-A1-1). Recorded as a Q-item; no verdict.
- **INDETERMINATE** — a Phase-0/Phase-1 control fails; no verdict.

**Deliverables independent of the verdict class:** the ℍ-factor instantiation screen (§2.4) with its criteria table; the ℂ-criterion disposition; the locking inventory (Sym_int-orbit types with stabilizers, Dynkin indices, π₃-injectivity, π₄ of the quotients) and the vacuum-manifold-of-record homotopy (π₁, π₄ of S¹⁵); the split/non-split disposition of the order-1344 signed-permutation group (banked, E-A1-6(a)); the Phase-2 witness (§4).

## 2. Analytical frame (definitions the instrument encodes; nothing else is computed)

**2.1 The arena, made precise.** Fix the octonion multiplication table with Fano lines {i, i+1, i+3} mod 7 (the §3.4-SIGNPHI convention: the multiplier ν₂ is an unsigned automorphism; QR = {1,2,4}). Three actions on the same 8-complex-dimensional space ℂ⊗𝕆 are distinguished and never conflated:
- **(A) the automorphism action** of G₂ = Aut(𝕆) (and of its finite subgroups — the realized signed Fano group of order 1344, F₂₁, any PSL(2,7) ⊂ G₂): g·(z ⊗ x) = z ⊗ g(x). It fixes the real unit; on Im𝕆 it is the real irreducible 7. Every element of the substrate's internal symmetry group acts on the octonionic index through (A), by the action of record.
- **(B) the phase action** of the finite phase group Sym_int ∩ U(1)_ℂ (Q-A1-1: the continuous U(1) is broken by O; expected ℤ₃): z ⊗ x ↦ ωz ⊗ x. Central.
- **(C) the Cℓ(6) spinor action:** the left-multiplication maps L_a = L_{e_a} on 𝕆 = ℝ⁸ satisfy L_aL_b + L_bL_a = −2δ_ab (Cℓ(0,7)); the bivectors L_aL_b (a < b ≤ 6) span spin(6) ≅ su(4) (15-dim) inside spin(7) (21-dim) inside so(8), commuting with the complex structure J = L₇; on ℂ⊗𝕆 = ℂ⁸ this SU(4) acts as 4 ⊕ 4̄ — Furey's construction, the action through which σ₄ and "σ₄|_{2O} = spin-3/2" (§2.87) are defined. Its central element −1 ∈ SU(4) acts as −Id on ℂ⊗𝕆.

**Assignment II, operationally:** there exists a locking (a subdirect product of the spatial rotation group — the motion-group O ≅ S₄ of §2.87.C–E, lifted — with Sym_int) under which the physical 2O acts on the substrate's ℂ⊗𝕆 through (C), with the spatial 2π ↦ −1 ∈ Spin(6) ↦ −Id realized as the FR sign on a genuine 4-dim quartet. **Assignment I, operationally:** every locked internal action on ℂ⊗𝕆 is of type (A) (possibly composed with (B)), hence ordinary (bosonic) on every 2O; the spinorial datum must be carried by a factor commuting with ℂ⊗𝕆 — the ℍ factor.

**2.2 The forcing criterion (E-A1-3(a)).** "The substrate forces X" means: X is a theorem about the action of record's symmetry group Sym_int and its vacuum manifold of record V, valid for **every** finite-energy configuration, machine-verifiable by exact arithmetic on the objects of §2.1. Nothing about an energy-minimizing core is assumed or computed (the dynamical selection stays behind M.CW — the I1–I3 ticket, §2.87.J). Four such theorems are tested; each has a live falsifier (§5); each is independent in its mathematical input (representation type / symmetry-group membership / homotopy / module content).

**2.3 The four forcing tests (Phase 1; R1-machine; both legs).**

- **T1 — representation content (the quartet cannot live in ℂ⊗𝕆 under Sym_int).** The spin-3/2 character of 2O, χ(q) = 2cos3φ + 2cosφ, is irreducible (⟨χ,χ⟩ = 1) with χ(−1) = −4 and **Frobenius–Schur indicator −1 (quaternionic type)**. A quaternionic irrep occurs in any *real* representation with even multiplicity. Under Sym_int = G₂ × (finite phase group) (Phase 0), ℂ⊗𝕆 restricted to any finite subgroup isomorphic to 2O is (phase character) ⊗ (1 ⊕ 7); the 7 of G₂ is a real representation; the phase character of 2O is trivial (Hom(2O, ℤ₃) = 1; and even under a continuous phase it could only be one of the two ordinary 1-dim characters, 2O^ab = ℤ/2, which twist χ to itself — 2O has one genuine 4-dim irrep); so the multiplicity of the quartet in the 7 is even and bounded by ⌊7/4⌋ = 1, hence **zero**, and the summand 1 is 1-dimensional. **Conclusion:** no subgroup of Sym_int acts on ℂ⊗𝕆 with a spin-3/2 constituent. *Branching check, exact:* the 7 restricted to each of the four sl₂-classes of G₂ (Jordan types [7], [3,3,1], [3,2,2], [2,2,1,1,1]) contains no 4 — built from explicit generators (the long-root SU(2) = the pointwise stabilizer of a quaternion subalgebra; the short-root SU(2) acting on its Im ℍ; the principal SU(2); an SU(2) ⊂ SU(3)). *Positive control C-A1-1:* the same test applied to (ℂ²)^⊗3 under the diagonal SU(2) reports the quartet with multiplicity exactly 1 (Sym³, §2.87.C P1) — the machine must find the quartet where it lives.
- **T2 — symmetry realizability (the Cℓ(6) spinor action is not a symmetry of the instantiated action).** (a) Compute Der(𝕆) = g₂ (14-dim) exactly as the derivations of the multiplication table; verify g₂ ⊂ spin(7)_L (the L-bivector algebra) and **dim(g₂ ∩ su(4)_L) = 8** — the intersection is su(3) (Günaydin–Gürsey: SU(3) = Stab_{G₂}(e₇) is generated by left-multiplication maps; here the two actions (A) and (C) *agree* exactly on SU(3) and nowhere else). (b) Build the spinorial 2O ⊂ SU(4)_L through (C) — the spin-3/2 su(2) inside su(4)_L on (ℝ⁸, J), exponentiated over the 48 unit quaternions — and test each element for octonion-automorphism membership (P(xy) = P(x)P(y) on the basis) — expected: **none** is an automorphism (a reportable defect on every element), so 2O_spinor ⊄ Sym_int (also forced by T1); its representation on ℂ⊗𝕆 must contain the quartet with multiplicity 2 (= 4 ⊕ 4̄) — the discriminating control C-A1-2. (c) **SL(2,7) ⊄ G₂:** SL(2,7) has exactly two solutions of g² = 1 (±I; machine-enumerated over 𝔽₇), so Σ_χ ν(χ)χ(1) = 2 (Frobenius–Schur); the ordinary irreps contribute 1 + 6 + 7 + 8 = 22 (ν = 1 for 1, 6, 7, 8; ν = 0 for the complex pair 3, 3̄ — adopted from the PSL(2,7) character table under E-A1-8(a), machine-checkable: the 6 is the permutation representation minus the trivial, the 7 is the G₂ 7 restricted, the 8 is the Steinberg representation, the 3's take the values (−1 ± √−7)/2); with the Galois pairs (σ₄, σ₄') and (σ₆, σ₆') sharing indicators (§2.77; the ATLAS pairings, adopted), the genuine sector must satisfy 2ν₄ + 3ν₆ + 2ν₈ = −5, whose only solutions have **ν₄ ∈ {0, −1}** — no genuine 4-dim irrep of real type; every faithful real representation of SL(2,7) therefore has real dimension ≥ 8 > 7, so SL(2,7) ⊄ O(7) ⊇ G₂. **Corollary (the G₂-involution lemma, exact and elementary):** the pointwise-fixed set of a non-trivial involutive automorphism of 𝕆 is a subalgebra of dimension 1, 2, 4 or 8 with an even number of −1's on Im𝕆; dimension 2 is impossible (left multiplication by a non-zero element of the 6-dim complement would map it injectively into a 2-dim space), so the fixed subalgebra is a quaternion algebra and **every involution of G₂ has trace −1 on the 7**. Hence the central element −1 ∈ Spin(6), which must act as −Id on ℂ⊗𝕆, is realizable inside Sym_int **only** through the phase group (B) — and not at all if that group is ℤ₃ — never by an automorphism. **Conclusion:** no symmetry of the instantiated action realizes the spinorial SL(2,7)/2O of §2.87 on the substrate field; σ₄ has no substrate carrier through symmetry. *Discriminating control C-A1-2:* the membership test returns automorphisms for all 1344 elements of the realized signed Fano group and defects for all 48 elements of 2O_spinor; the character test finds the quartet in the spinor action (multiplicity 2) and not in the automorphism action (multiplicity 0) — the test tells (A) from (C).
- **T3 — target topology (no FR ℤ₂ in the target sector; no internal double cover).** For a field with values in a target whose vacuum manifold is V (maps ℝ³ → V with a fixed vacuum at infinity), the fundamental group of the configuration space that carries the Finkelstein–Rubinstein sign is π₄(V) (FR 1968; Giulini 1993: "π₁(Q) ≅ π₄(SU(2)) ≅ ℤ₂"; Krusch–Speight 2006: π₄(S²) = ℤ₂ is what makes odd-charge hopfions fermionizable). **Under Q-A1-1/Q-A1-3 the vacuum manifold of record is the accidental two-body sphere V = S¹⁵ ⊂ ℂ⊗𝕆 = ℝ¹⁶** (every uniform state of fixed density is degenerate; the oriented term vanishes on all of them), so **π₁(V) = 0 and π₄(V) = 0 outright** — the target sector carries neither a vortex charge nor an FR ℤ₂. The **locking inventory** is computed alongside: the Sym_int-orbit types of ψ₀ ∈ ℂ⊗𝕆 by the rank (0, 1, 2) of the span of its two imaginary octonionic parts — a vector has at most two independent imaginary directions, which lie in a quaternion subalgebra, so its G₂-stabilizer always contains that subalgebra's pointwise stabilizer, the long-root SU(2) (Jordan type [2,2,1,1,1], Dynkin index 1), or is larger (SU(3) for rank 1, G₂ for rank 0) — with H₀, the Dynkin index of the sl₂ generating π₃(H₀), π₃-injectivity into π₃(G₂), and π₄(G₂/H₀) from the fibration exact sequence (π₁(G₂) = 0, π₃(G₂) = ℤ, π₄(G₂) = 0 — derived in-instrument from SU(3) → G₂ → S⁶ with the textbook π₄(SU(3)) = 0, π₃(SU(3)) = ℤ, π_k(S⁶) = 0 for k ≤ 5; Mimura 1967 cited as the canonical table, §12 L-A1-4). Expected: π₃(H₀) → π₃(G₂) injective and π₄(G₂/H₀) = 0 for all three ranks. **No internal double cover:** π₁(G₂) = 0 and the phase group is finite, so no binary-polyhedral vortex group can arise from the internal factor (contrast: SO(3)/Γ has π₁ = Γ*; that mechanism needs π₁ = ℤ₂ upstairs, which the internal group does not have — §12 L-A1-6). Two items the instrument records: (i) **the envelope-in-𝕆 kill (control, per Q-A1-2):** the §3.4.5 hopfion (n ∈ S² ⊂ Im ℍ_L ⊂ Im 𝕆) has its FR loop killed by the ambient target — the inclusion S² ↪ S⁶ (= G₂/SU(3)) ↪ S¹⁵ is null-homotopic (π₂(S⁶) = 0), so π₄(S²) = ℤ₂ → π₄(V) = 0 is the zero map; a texture confined to an associative 3-plane by *energy* is not a texture protected by *topology* — this is why the declared envelope must be a separate component (H2); (ii) **the locked-lift −1 trap (Eddington guard, pre-declared; A-2.4):** for a texture in an associative 3-plane the internal image of the spatial 2π loop is path-dependent through the stabilizer ({Id, σ_ℍ}: σ_ℍ = −1 on the 4-dim ℍ_L^⊥, which under the long-root SU(2) is 2 ⊕ 2 — the binary doubling, never a genuine quartet); a "−1 on a 4" that depends on the lift is gauge (module content, not dimension, decides: the distinct-4 discipline); the invariant is π₁ of the collective-coordinate orbit (Phase 2). *Positive controls C-A1-3:* the same exact-sequence machinery must return π₄(S²) = ℤ₂ (from U(1) → SU(2) → S²), π₄(S³) = ℤ₂, and π₁(SO(3)/T) = 2T (order 24).
- **T4 — module content (the substrate's 7 carries no ρ₆).** ρ₆ is the non-trivial part of the *permutation* representation of PSL(2,7) on the 7 Fano points (L²(G/S₄) = ρ₁ ⊕ ρ₆; χ₆(2A) = +2, permutation character 3 on the point-fixing involutions). The substrate's internal 7 is the *signed* octonionic 7, on which every order-2 element of any PSL(2,7) ⊂ G₂ has trace **−1** (the involution lemma of T2). Since a 7-dim representation containing ρ₆ has involution trace 2 + χ_rest(2A) = 3, **ρ₆ is not a constituent of the substrate's 7 under any PSL(2,7) ⊂ G₂** — the two possibilities are ρ₇ and 1 ⊕ 3 ⊕ 3̄, exactly the two non-conjugate embeddings of PSL(2,7) in G₂ in print (Cohen–Wales 1983 via Evans–Pugh, §12 L-A1-3). Machine content: enumerate the signed automorphism lifts of the three non-trivial pointwise-line-stabilizer collineations (8 lifts each; 24 in all), classify by order and trace (expected: every order-2 lift has trace −1; the trace-3 lifts have order 4 and square to the quaternion-subalgebra involution σ_ℍ), and compare with the permutation character (3) and χ₆ (2): the wrong-module gap is 4, exactly as §3.4.4 states. **Conclusion:** Assignment II's premise "the ρ₆-derived ℂ⊗𝕆" conflates the sign-blind coset module with the sign-carrying octonionic module — the very signs that make the oriented term φ_abc — and has no substrate carrier. *Control C-A1-4:* under the unsigned F₂₁ the machine must return 1 ⊕ 3 ⊕ 3̄ (the G-INT1 pin) and the ν₂ multiplier as an unsigned automorphism.

**What the four tests decide jointly.** T1 and T4 are about *what* ℂ⊗𝕆 can carry; T2 about *which group* can act; T3 about *whether any loop* can carry a sign. Assignment II needs all four to fail in its favour; Assignment I is forced if any one holds, and the gate reports all four so that the forcing is over-determined rather than single-threaded (PC-1). None of them is a dynamical statement (M.CW respected); none loads a target (Eddington quarantine: the magnetic-moment target strings are on the T1 list, §11).

**2.4 Physical instantiation — criteria for the ℂ⊗𝕆⊗ℍ resolution in the K₇/supersolid substrate (Phase 1b).** The three factors are located, or shown unlocatable, by criteria stated before any candidate is examined:
- **P-𝕆 (forced by I1):** the target algebra is 𝕆 with its structure constants φ (the seven imaginaries ↔ the seven Fano points ↔ the seven K₇ vertices via the two-Fano-plane face structure of §2.86); instantiated (MV-G1; G-INT1's Fano-line selectivity is the operational witness).
- **P-ℂ (centrality):** the ℂ of ℂ⊗𝕆 must be **central** — it must commute with every left-multiplication map L_a — for ℂ⊗𝕆 ≅ Cℓ(6) to hold as an algebra of maps (Furey). The GP condensate's complex structure (the i of the 8 complex amplitudes, action (B) and its continuous parent) is central by construction; the Cayley–Dickson doubling unit e₈ of the sedenion construction (§2.85's U(L) ⊂ 𝕊) is **not** — in 𝕊 = 𝕆 ⊕ 𝕆e₈ the doubling unit anticommutes with every imaginary unit of 𝕆 (exact, Cayley–Dickson). The §2.87.A "honest gap" therefore **closes by instantiation, conditional on I1/I2**: the ℂ is the condensate's complex structure; the e₈ candidate is excluded by centrality; the QR/QNR ℤ₂ is a sign, not a complex structure. Machine content: commutation of the complex unit with all L_a (exact); the e₈ anticommutation (exact).
- **P-ℍ (four criteria, all required):** a candidate ℍ factor must be **(i) tensor-commuting** with the ℂ⊗𝕆 maps (it acts on a *separate* index, never on a subspace of 𝕆 — else T1/T2 apply to it); **(ii) quaternionic** — it carries a Sp(1) = SU(2) structure with a genuine spin-½ module (the per-strand ℂ² carrier of §2.87.C, in whose Sym³ the quartet lives); **(iii) topologically protected** — the FR ℤ₂ it supplies survives in the *full* configuration space: either its target contributes π₄ = ℤ₂ as an independent factor, or the index is a spatial-spinor index acted on by the spin/Pin structure of space (the S8/S9 orbifold structure — the "carrier identification" the S-chain left open); **(iv) symmetry-lockable** — its SU(2) is tied to spatial rotation by a symmetry of the action (kinematically, as for a spinor index; or dynamically, as for a hedgehog — the latter M.CW-walled and *not* computed here).
- **Candidates screened (E-A1-4(a)):** **H1** the §3.4.5 hopfion in Im ℍ_L ⊂ Im 𝕆 — a *control* under Q-A1-2 (not the declared envelope): fails (i) (inside 𝕆) and (iii) (T3's envelope-in-𝕆 kill); **H2** the declared envelope — a genuinely separate S²-valued texture component (M.ONT path (3), Q-A1-2) — passes (i)–(iii) (π₄(S²) = ℤ₂ on its own factor), (iv) only dynamically (hedgehog; M.CW) — an **import** beyond I1–I3, R3; **H3** a spatial-spinor index, ψ ∈ ℂ⊗𝕆⊗ℍ with ℍ ↔ Spin(3) = Sp(1) — Dixon's T = ℂ⊗ℍ⊗𝕆 with ℍ in its Lorentz role — passes (i), (ii), (iv) kinematically and (iii) through the S8 flat-home meridian −1 — an **import** (the field content of record has no spinor index, Q-A1-1), R2-conditional on the S8/S9 ontology imports; **this is the identification the S-chain's "carrier identification" non-claim names**; **H4** the Fano-line quaternion subalgebra ℍ_L ⊂ 𝕆 (the G-INT1 line, its SO(4)-stabilizer SU(2)'s) — fails (i): a sub-apparatus of 𝕆, the 1 ⊕ 3 ⊕ 3̄ (color-like) structure, and by T1 carries only 2 ⊕ 2 (the binary doubling, Casimir 3/4 — §2.87.C's inequivalent module); **H5** the Cayley–Dickson doubling 𝕊 = 𝕆 ⊕ 𝕆e₈ — fails (ii) (a 2-dim doubling, not quaternionic) and the centrality of P-ℂ. **Expected screen outcome:** H2 and H3 admissible, **both imports**; H1, H4, H5 excluded by exact checks. **Consequence, if the screen lands as expected:** the ℂ⊗𝕆⊗ℍ resolution is **not instantiated** by the substrate as constituted (I1: ℂ⊗𝕆); the ℍ factor is a **located import I5** (E-A1-5(a): "the ℍ-factor / spinor-carrier import"), and the §2.50 per-strand spinor phase — the S-chain's single open import — is *the same import* in different bookkeeping: supplying the per-strand ℂ² *is* supplying the ℍ factor. No import is discharged; one is unified.

**2.5 What "K₇/supersolid" contributes and what it cannot.** The instantiated object is the MV-G1 roton-GP crystal (p6m; three Goldstone zeros — a supersolid), two-dimensional (import I4 for three propagating dimensions, §2.88.E). T1–T4 and the §2.4 criteria are target-space and symmetry-group facts, independent of spatial dimension and of the crystallization; they are decided on the action of record. The K₇ tube (the Császár-torus filament core, §3.4.4's forward prediction; the M.ONT filament) is not instantiated as a field solution anywhere in canon; the three-strand Borromean core needs three dimensions. **This gate therefore does not, and cannot, compute the locking dynamics on the K₇ tube** — that is the I1–I3 dynamical clause, unchanged.

## 3. The Assignment II structural-mapping obligation (LSF-δ — executed September 20, 2026; the table is §12)

Assignment II is non-standard *within the Furey/Dixon lane* but has a rich standard home *elsewhere*: the octonions as the **spacetime/spinor** algebra in ten dimensions (SL(2,𝕆) ≅ Spin(9,1); ℝ, ℂ, ℍ, 𝕆 ↔ spinors in D = 3, 4, 6, 10). The obligation was to map every published factor placement onto the SQT arena and state, for each, whether its octonionic-spin mechanism is compatible with a substrate whose octonionic index is a **spatial scalar** (the action of record; F-A1-1). **Result (§12):** in every octonionic-spin realization located, the octonion components carry a spacetime vector/spinor index on which SL(2,𝕆) acts — a spin–orbit structure the action of record does not contain (Phase 0 (0c) is the machine check); none operates on a scalar-index octonionic field; no rescue of Assignment II *here* exists in the literature swept, and no collision with the gate's question was found — novel-in-assembly verified at the stated ceilings.

## 4. Execution leg

**Phase 0 — the action of record, inventoried (R1; both legs; the extract of §7 md5-guarded).** (0a) Field content: 16 real components, 8 complex amplitudes, no spinor index (Q-A1-1) — asserted from the extract; (0b) Sym_int: the stabilizer of the full action (two-body single-scalar kernel + oriented term O) inside O(16): the 14 g₂ generators pass the exact invariance test of the O density; a generic so(16) element fails at a reportable margin (C-A1-5); the phase subgroup preserving O is finite — its order recorded (expected 3 for a term cubic in the complex amplitudes, Q-A1-1) — and the conjugation structure recorded as a fact (ψ ↦ ψ̄ carries O ↦ Ō); so Sym_int = G₂ × (finite), continuous part exactly G₂; (0c) **spatial–internal direct product**: every term contracts internal indices only through δ_ab and φ_abc and spatial indices only through ∂_x, ∂_y (the 2-form structure of O) — no term couples a spatial index to an internal index; recorded as an assert on the term list (**F-A1-1** is this assert failing); (0d) the vacuum manifold of record V = S¹⁵ (all uniform states of fixed density degenerate at two-body order; no real-unit-splitting term, Q-A1-3), with π₁ = π₄ = 0, and the Sym_int-orbit types of ψ₀ (rank 0/1/2) as the locking inventory with their stabilizers H₀ = G₂ / SU(3) / SU(2)_long, generic π₀ = 1; (0e) controls: L_⊥ψ₀ = 0 (G-INT1's exact zero mode) and 7 = 1 ⊕ 3 ⊕ 3̄ under F₂₁ (character re-check).

**Phase 1 — T1, T2, T3, T4 (R1-machine; exact arithmetic — sympy rationals / Fraction / exact algebraic numbers where √2 enters; floats only in character sums and automorphism defects, rounded or thresholded; both legs, CC blind, method variation requested: CC builds g₂ from the 3-form φ rather than from derivations, SL(2,7) from 𝔽₇ matrices with its own class enumeration, and the homotopy bookkeeping in its own exact-sequence code).** Every test emits its boolean, its integer witnesses (dimensions, traces, indicators, multiplicities, indices, group orders) and its control results into the E8 checkpoint; the verdict class is assembled in Phase 3 only. **The 1344 group (E-A1-6(a)):** the split/non-split disposition by complement search over the 64 lift-pairs of the presentation ⟨a, b | a², b³, (ab)⁷, [a,b]⁴⟩ (a, b fixed Fano collineations; each lifted by the 8 sign-kernel elements): a generated subgroup of order 168 ⇒ split; none ⇒ non-split — banked R1 structural, not verdict-bearing.

**Phase 1b — the ℍ screen (R1 for every criterion check; R2/R3 for the identifications).** Five candidates × four criteria, each criterion an exact check or an adopted homotopy fact, with the citation for every adopted fact in the checkpoint; outcome codes ADMISSIBLE-IMPORT / EXCLUDED(criteria) per candidate; H1 flagged `role: control` (Q-A1-2); the P-ℂ disposition; the I5 bookkeeping line (E-A1-5(a)).

**Phase 2 — the instantiated-core witness (E-A1-2(a); R1 for the configuration computed; zero verdict weight; a 2-D witness — it tests contractibility of the 2π loop in the collective-coordinate orbit, not half-integer spin, which is a 3-D statement carried by T3).** *Object:* the G-INT1 Fano-line texture core in the homogeneous ℂ⊗𝕆 GP substrate (same Sym_int; no roton) — the degree-1 texture ψ(x) = √ρ₀·n(x), n = (sin f cos φ, sin f sin φ, cos f) in the (e₁, e₂, e₄) frame of the line L = {1,2,4}, f(0) = π, f(∞) = 0 (a fixed rational-function profile is pinned in the lock record); *control:* the same texture in the non-line frame L' = {1,2,3}. *Computations:* (a) O ≠ 0 on L and O = 0 on L' (the §3.4.4 selection rule; the L' value is an exact zero of the structure constants, the L value a reported non-zero — each leg's magnitude is its own, only the booleans are compared); (b) the stabilizer of the configuration in SO(2)_space × Sym_int: exhibit the locked family (R_α, g_α) with g_α ∈ SO(4) = Stab_{G₂}(ℍ_L) acting on Im ℍ_L as the rotation by α about e₄, the kernel SU(2)_long (pointwise stabilizer of ℍ_L), the finite phase and conjugation parts, and π₀(Stab); (c) the internal images of the spatial 2π loop over the lifts through the stabilizer — expected {Id, σ_ℍ}, both exhibited as exact 8×8 matrices, with σ_ℍ's eigen-decomposition (+1 on ℍ_L, −1 on ℍ_L^⊥ = 2 ⊕ 2 under SU(2)_long) — labelled INTERNAL-HOLONOMY-GAUGE; (d) π₁(Orbit) for the orbit of the configuration under SO(2)_space × Sym_int: from the fibration Stab → G → Orbit with π₁(G) = ℤ (the spatial SO(2)) and the diagonal loop of Stab winding once in it, π₁(Orbit) = π₀(Stab) — expected trivial ⇒ **the 2π-rotation loop is contractible in the orbit: no spin sign** — T3's conclusion witnessed on an instantiated core; (e) the characters of the stabilizer's internal image on the 7 and on the G-INT1 chiral pair (ordinary: the pair transforms as e^{±iα}). This honours the §2.88.D.2 "Gate-2a trigger" at the level the question needs — the chiral pair's transformation under the locked elements — not the heavy relaxed-N BdG solve, which pins only σ (class-(b)) and is not required.

**Phase 3 — verdict assembly and comparison (last).** The verdict class from the four booleans and the controls (the rule is encoded in the schema; the comparator recomputes it on each leg); the ℍ-screen table; the locking inventory; the banked structural items; the comparator run against the frozen schema. Then, and only then, the §2.87/§2.87.A open-item dispositions are drafted for the fold (E-A1-7(a)).

**Order of operations (binding):** memo lock (this file; md5 in the lock record) → gate T1 list pinned (done, A-2.5) → schema v1.0 + comparator v1.0 frozen **before** the chat emission (the G-MSCS1 order; D-Q-3 not repeated) → chat instrument (md5-guards the memo, the T1 list, the action-of-record extract) → Phase 0 → Phase 1 → Phase 1b → Phase 2 → Phase 3 → execution report → P-4/P-4.b/P-4.c dispatch (the T1 lists in-band; D-T1 retired) → CC leg blind from scratch → two-leg comparison → S9 on misses → fold authorization → V4.84. **The chat leg is not executed until the author's word** (directive of September 20, 2026, item 4).

## 5. Falsifiers, controls, and where the kill surface actually is

- **F-A1-1 (kills the frame's premise; decided in Phase 0):** the action of record contains a term coupling a spatial derivative index to an octonionic index (a spin–orbit / Dray–Manogue-type structure), or Sym_int is strictly larger than G₂ × (finite phase) in a way that contains the spinor SU(4) or a spinorial SL(2,7)/2O (e.g. the oriented term absent and the accidental O(16) exact). Then T1–T2 do not apply as stated → ASSIGNMENT-II-REALIZABLE, pre-verdict halt, successor named. **This is the only route by which Assignment II survives this gate.**
- **F-A1-2 (kills T1):** the Frobenius–Schur indicator of χ_{3/2} computes to +1, or the 7 of G₂ is found non-real, or a branching of the 7 to an sl₂-class contains a 4.
- **F-A1-3 (kills T2):** dim(g₂ ∩ su(4)_L) ≠ 8; or an element of 2O_spinor passes the automorphism test; or SL(2,7) is found to have a genuine 4-dim irrep of real type (ν₄ = +1); or a G₂ involution with trace ≠ −1 is exhibited.
- **F-A1-4 (kills T3):** π₄(S¹⁵) ≠ 0 or π₁(S¹⁵) ≠ 0 (absurd, but asserted), or a locking-inventory stabilizer with π₃(H₀) → π₃(G₂) non-injective for a vector-type ψ₀, or an internal double cover (a binary-polyhedral π₁) — would restore a target-sector FR ℤ₂.
- **F-A1-5 (kills T4):** an order-2 signed automorphism lift of a Fano involution with trace 3, or a PSL(2,7) ⊂ G₂ whose 7 contains ρ₆.
- **F-A1-6 (kills the ℍ-instantiation deliverable in the other direction):** a candidate *inside* the field content of record passes all four P-ℍ criteria — the ℍ factor would then be instantiated without import, and I5 is not registered.
- **F-A1-7 (Phase 2 witness only):** π₁(Orbit) ≠ 0 for the pinned texture, or a genuine (central-negative) character on the chiral pair under a locked element — contradicts T3/T1; treated as a bug first (S9), a finding second.
- **Controls C-A1-1…5** (§2.3; plus C-A1-5: the Phase-0 negative control — a generic so(16) rotation must *fail* the O-invariance test at a reportable margin).
- **Where the kill surface for the μ_n programme actually is (named, not executed):** if the expected verdict lands, the spin-3/2 quartet must be built in the imported ℍ factor (the Sym³(ℂ²) route of §2.87.C P1, whose per-strand carrier is I5); the derived μ_n then rides (I5) + (the locking dynamics behind M.CW) + (the FR/η parity of Gate 2b). Nothing in this gate moves μ_n; §2.87.A's sentence "μ_n's spin-3/2 requires Assignment II (or an equivalent derivation relocated to ℂ⊗ℍ)" is resolved to its second clause, not its first.

## 6. Hypotheses (M-naive expectations, registered pre-data — NOT verdicts)

- **H-A1-1:** T1–T4 all hold on the action of record → ASSIGNMENT-I-FORCED. (The chat-side pre-lock sanity checks of §13 already return the T1, T2(a)/(c-count), T4 witnesses; the gate re-derives them two-leg under lock — they are disclosed, not banked.)
- **H-A1-2:** the ℍ screen admits exactly H2 and H3, both imports; H1 (control), H4, H5 excluded; P-ℂ closes by instantiation (complex unit central; e₈ non-central).
- **H-A1-3:** the order-1344 signed Fano group is a **non-split** extension 2³·PSL(2,7) — corroborated in print (§12 L-A1-3: "a nonsplit extension of ℤ₂³ by PSL(2,7)"); the complement search is expected to find none among the 64 lift-pairs — banked R1 structural, not verdict-bearing.
- **H-A1-4 (Phase 2, restated per A-2.4):** the stabilizer of the pinned Fano-line texture is a subdirect product with internal image inside SO(4) = Stab_{G₂}(ℍ_L) (type (A)), kernel SU(2)_long, π₀(Stab) = 1; the internal images of the spatial 2π loop are {Id, σ_ℍ} (path-dependent — gauge); π₁(Orbit) = 0; the chiral pair transforms ordinarily. O ≠ 0 on L, O = 0 on L'.
- **H-A1-5 (surfaced at memo design; R2 conditional; a scoping item, not a verdict of this gate — Q-A1-3 answered "proceed as stated"):** under the 16-real-component reading with the single-scalar kernel on all eight components and no term splitting the real unit from Im𝕆, the two-body vacuum manifold is S¹⁵ and **π₁ = 0 — the phase-vortex sector is not topologically protected in the 16-component substrate** (a winding in one complex line can be unwound through the other directions); protection would return if a term distinguished the real unit (V ⊇ S¹, π₁ = ℤ). The successor question is registered in §9; it bears on the G-QUANTA C1 evaluation of the K₇-vortex row only through its *declared* configuration space (no retraction implied; a scoping note).

## 7. Pinned inputs and imports (named; none exercised beyond what is stated)

- **The action of record (E-A1-1(a)):** `inputs/paper_II_3_4_4_and_3_4_7_extract.md` — md5 `940b0bee4b2112e911ae738c3db2bc3d`, 12,912 B — §3.4.4 and §3.4.7 transcribed verbatim from the project-knowledge canonical `paper_II_section_3_4_CANONICAL_v5_with_3_4_7.md` on September 20, 2026 (T1 CLEAN), with the author's answers of record (Q-A1-1, Q-A1-3) stated in its header; the instruments md5-guard the extract; the author may diff it against the canonical file at any time (a mismatch is an H-item). Read for structure only; no number from it is used.
- **T1:** base `tools/t1/T1_base_author_20260919.txt` (`05302210cc4ceb70553acbe8379e9fc3`, 143 B, 11 patterns); gate stratum `tools/t1/T1_stratum_G_2a_A1.txt` (`ea3bbbbd98da8f4e9eee267beda492b7`, 13 patterns); gate list `tools/t1/T1_forbidden_G_2a_A1.txt` (`2026b782db3905d9f2ce35733823618c`, 241 B, 24 patterns = base + stratum byte-exact); scanner `tools/t1/t1_scan.py` (`6b86290090a8c84f1b1a0a99ec0bf697`).
- The octonion convention (lines {i, i+1, i+3}); the SL(2,7) matrices over 𝔽₇; 2O as the 48 unit quaternions; Cℓ(0,7) left-multiplication maps on ℝ⁸ (columns L_a e_j = e_a·e_j); the Cayley–Dickson sedenion doubling for P-ℂ.
- Adopted mathematical facts, cited in the checkpoint, never re-derived: π₄(SU(3)) = 0, π₃(SU(3)) = ℤ, π₁(SU(3)) = 0, π_k(S⁶) = 0 for k ≤ 5 (textbook; used to derive π₁, π₃, π₄ of G₂ in-instrument); π_k of finite groups; π₂(S⁶) = 0; π₄(S²) = π₄(S³) = ℤ₂; the fibration long exact sequence; Dynkin index (computed exactly from the invariant form on the explicit generators, normalized to the long-root SU(2)); the even-multiplicity theorem for quaternionic irreps in real representations; FR: π₁(Config) = π₄(target) for based maps; the PSL(2,7) ordinary Frobenius–Schur indicators and the SL(2,7) Galois pairings (E-A1-8(a)); Cohen–Wales 1983 (two PSL(2,7) classes; the non-split 1344 group) — cross-check only, T4's argument is self-contained.
- Ledger inputs consumed: §2.87's construction of σ₄ (for 2O_spinor, T2(b)); §2.77/§2.D-FC's irrep dimensions and Galois pairing; §2.79's lifting facts; G-INT1's 1 ⊕ 3 ⊕ 3̄ pin (control); the M.ONT declaration + Q-A1-2 (the H2 identification).
- Chat-side pre-lock sanity checks (disclosed, §13): `prechecks/precheck_algebra.py` (`cf36395dba7ff35127f40e9f805ff1c7`).
- **No observational input. No ledger value. No magnetic moment, ratio, mass, or SI quantity anywhere in any instrument** (the T1 stratum of §11 enforces the first three).

## 8. Elections (author, September 20, 2026 — T3-immutable on lock)

- **E-A1-1 — action of record: (a)** the Paper II §3.4 canonical v5 file (via the pinned extract of §7).
- **E-A1-2 — Phase 2 witness object: (a)** a single Fano-line texture core in the homogeneous ℂ⊗𝕆 GP substrate (same Sym_int; cheap; CC-optional MV-G1 extension).
- **E-A1-3 — meaning of "forced": (a)** configuration-independent theorem on Sym_int and V (§2.2).
- **E-A1-4 — ℍ candidate set: (a)** H1–H5 all screened (H1 as control under Q-A1-2).
- **E-A1-5 — I5 bookkeeping: (a)** register "I5 — the ℍ-factor / spinor-carrier import" at the fold and record that the §2.50 per-strand spinor-phase import and I5 are one import in two bookkeepings (no discharge).
- **E-A1-6 — the 1344 group: (a)** compute split/non-split (complement search over the 64 lift-pairs of a standard presentation) and bank the answer as R1 structural.
- **E-A1-7 — fold treatment on the expected verdict: (a)** additive brackets — the §2.87 open-items "Factor-assignment question" row → CLOSED (Assignment I forced, R2 conditional); the "Gate 2a — is the baryon's spin geometry ρ₆/Cℓ(6)?" headline row → answered NO at the substrate level, the spin geometry relocated to the ℍ factor (I5), the dynamical clause unchanged; §2.87 / §2.87.A brackets recording that "σ₄|_{2O} = spin-3/2" stands as algebra and is relocated as physics (as §2.87.A anticipated); the M.ONT declaration line annotated with the H2 outcome; one §2.91.R body entry; one Part VI row. **No retraction** — §2.87 filed the physical claim as a non-claim.
- **E-A1-8 — the T2(c) method: (a)** the Frobenius–Schur count + Galois symmetry (SL(2,7) built from scratch; no character table constructed); the full character-table construction remains the CC-optional method variation.

## 9. Registers and non-claims

- **R1-machine:** every Phase-0/1/1b check and every Phase-2 number, both legs, exact arithmetic; the G₂-involution lemma (elementary; machine-instantiated).
- **R2, conditional:** the verdict class (on the action of record being the instantiated substrate — E-A1-1(a) and the pinned extract; on the adopted homotopy facts); the ℍ-screen outcome; the P-ℂ closure; the I5 unification.
- **R3:** the H3 identification (ℍ as the spatial-spinor index; the "carrier identification" of the S-chain) — named, not made; H2 (the declared envelope) as the spin home — named, not made.
- **Named open item registered by this memo (not executed; the fold carries it as a successor line):** *vacuum selection in the 16-component substrate* — whether a G₂-invariant term distinguishing the real unit from Im𝕆 (allowed by symmetry, absent from the action of record per Q-A1-3) is required for a topologically protected filament sector (H-A1-5); a bounded structural question for a successor gate; no verdict here.
- **Non-claims (binding):** no μ_n value, no ratio, no observable, no bridge (M.BRIDGE intact); no locking dynamics (M.CW; the I1–I3 ticket untouched); Gate 2a's *dynamical* clause not closed; no §2.50 closure (the import is unified with I5, not discharged); no retraction of any §2.87 algebra result; no statement about the Pin type (S9 residual unchanged); no statement about G-QUANTA's verdicts (H-A1-5 is a scoping note); the gauge-paper §7.4 firewall held; **§2.52 Open 3 untouched.**

## 10. Housekeeping (V4.84 — carried by this gate's fold, not by this memo)

- **Additive bracket on §2.91.Q and on the V4.83 fold-in record:** "[→ V4.84 housekeeping: PR #24 (CC G-MSCS1 leg of record, claude/new-session-r4afly, return ae2c3fdb) merged September 19, 2026; the chat-side G-MSCS1 fold estate — closure memo 0825f136, comparator v1.1 54b32988, chat-side comparison run d4a5b271, v1.1 candidate 948852fe, fold authorization 76b43814, fold script 9f798c35, manifest — landed at `gmscs1_gate/estate/` via the successor PR #⟨n⟩ (merged ⟨date⟩), per the gquanta_gate/estate/ (PR #23) precedent; V4.83 (40009ec0) active in project knowledge — author confirmation September 20, 2026.]" — the PR number and merge date to be filled at fold time from the merged PR; the canonical ledger stays out of the repository (FOLD_LEDGER_2026-06-18 policy).
- As-of header and changelog lines per the V4.83 pattern; the §2.52 Open 3 guard; reverse-splice byte-identity to V4.83.

## 11. T1 list (pinned; the base list travels in-band — D-T1 retired at G-MSCS1)

- **Base:** `tools/t1/T1_base_author_20260919.txt` (md5 05302210, 11 pattern lines, author-supplied, pinned H-MS-0).
- **Gate stratum G-2a-A1 (pinned September 20, 2026; 13 pattern lines, `tools/t1/T1_stratum_G_2a_A1.txt`, md5 ea3bbbbd — the patterns are not reproduced in this memo):** the neutron and proton magnetic-moment values in the nuclear unit to three and four decimals; the symbol of that unit and the name of that unit (with and without its qualifier); the two data-compilation acronyms; the proton and neutron masses in MeV to two decimals; the proton-to-electron mass ratio to two decimals; and the neutron-to-proton moment ratio to five decimals. The spin label "3/2" and the integer 4 are structural vocabulary of the gate and are **not** forbidden; the ratio the §2.85 constituent formula produces is not forbidden as a bare fraction (it would collide with "spin-3/2" under substring matching) — the values it is compared against are.
- **Gate list:** `tools/t1/T1_forbidden_G_2a_A1.txt` = base + stratum byte-exact, md5 `2026b782db3905d9f2ce35733823618c`, 241 B, 24 pattern lines.
- **Discipline:** the memo, the lock record, the extract, the instruments, the checkpoints, the comparator, the report and the dispatch are scanned; pattern-index-only reporting; the list itself md5-asserted, never self-scanned; the contextual numeric rule (D-W-7 lineage) in force. This memo, the extract, the pre-check script and the draft memo scan CLEAN against the gate list.

## 12. LSF-δ (executed September 20, 2026; seven clusters; per-source transcription ceilings stated)

Ceilings: **FT** = full-text (or full-text excerpt) read this session; **AB** = abstract or publisher description; **LS** = listing only (title/venue confirmed, text not retrieved); **SEC** = secondary exposition; **NF** = not fetched this session, standard reference cited. Verdict form per cluster: prior art / collision / differentiator.

| Cluster | Sources (ceiling) | What was found | Verdict |
|---|---|---|---|
| **L-A1-1** Assignment I lane (ℂ⊗𝕆 internal; ℂ⊗ℍ Lorentz/isospin) | Dixon, *Division Algebras: Octonions, Quaternions, Complex Numbers and the Algebraic Design of Physics*, Springer MAIA 290 (1994) (AB: "the intimate connection between the mathematics of the division algebras and the Standard Model … and the connection of this model to 10-dimensional spacetime implied by the mathematics"); Furey–Hughes, PLB 827 (2022) 136959, *One generation of standard model Weyl representations as a single copy of ℝ⊗ℂ⊗ℍ⊗𝕆* (AB + text excerpt: "colour symmetry is written using the purely octonionic part of A"; the placement presented as the chosen basis, not as forced); Furey PLB 742 (2015) 195; Furey EPJC 78 (2018) 375; Furey arXiv:1611.09182; Gresnigt EPJC 78 (2018) 91; Stoica AACA 28 (2018) 52 (LS, carried from the ledger's V4.42 sweep); Günaydin–Gürsey, J. Math. Phys. 14 (1973) 1651 (LS; content via Baez's exposition, SEC: the automorphisms fixing a unit imaginary form SU(3); 𝕆 = ℂ ⊕ ℂ³ with left multiplication by that ℂ as the complex structure). | The arena and the placement are prior art; the Günaydin–Gürsey left-multiplication construction is the T2(a) intersection fact in print. **No source states the placement as forced by a substrate symmetry** — the forcing question is the gate's. | prior art (arena, placement, T2(a)); no collision; differentiator: the substrate-forced assignment. |
| **L-A1-2** octonionic-spin lane (𝕆 as the spacetime/spinor factor) | Kugo–Townsend, Nucl. Phys. B 221 (1983) 357; Sudbery, J. Phys. A 17 (1984) 939; Evans, Nucl. Phys. B 298 (1988) 92; Manogue–Schray, J. Math. Phys. 34 (1993) 3746 (all LS via the nLab reference list, SEC: the table Spin(2,1)/SL(2,ℝ) … Spin(9,1)/"SL(2,𝕆)"; "spin group representations are naturally identified with 𝕂ⁿ"); Baez–Huerta, *Division algebras and supersymmetry II*, ATMP 15 (2011) 1373, arXiv:1003.3436 (FT excerpt: vectors in (n+2)-dim Minkowski space ↔ 2×2 hermitian matrices over 𝕂, spinors ↔ 𝕂²); Dray–Manogue, *Octonions, E₆, and particle physics*, arXiv:0911.2253 / J. Phys. Conf. Ser. 254 (2010) 012005 (FT excerpt: 10-D Lorentz transformations act via SL(2,𝕆) on two-component octonionic spinors; a preferred imaginary direction breaks G₂ → SU(3) in the 10 → 4+6 reduction; "the octonions encode the fundamental spacetime geometry itself"). | In every entry the octonion components **carry the spacetime spinor/vector index** on which SL(2,𝕆) acts — the F-A1-1 spin–orbit structure; none operates on a scalar-index octonionic field. Assignment II's structural home is this lane, and it requires exactly what the action of record lacks (Phase 0 (0c)). | prior art (octonionic spin *as spacetime spinors*); no collision (the SQT substrate is a condensate with a scalar-index field); differentiator: the missing spin–orbit structure — no rescue. |
| **L-A1-3** G₂ structure | Cohen–Wales, *Finite subgroups of G₂(ℂ)*, Comm. Algebra 11 (1983) 441 (LS; the abstract page not served) via Evans–Pugh, *Spectral measures for G₂ II: finite subgroups*, arXiv:1404.1866 (FT excerpt, Table 1: **PSL(2,7) has two non-conjugate embeddings, 7 → Σ₇ (irreducible) and Σ₁ + Σ₃ + Σ₃\***; the order-1344 group "a nonsplit extension of ℤ₂³ by PSL(2,7)"; PSL(2,8) three embeddings; PSL(2,13) two; PU(3,3), G₂(2) one each); Baez, *The Octonions*, Bull. AMS 39 (2002) 145, §G₂ (FT: G₂ = the subgroup of Spin(7) fixing a unit vector in S⁷, Spin(7)/G₂ = S⁷, dim 14, Der(𝕆) = g₂); nLab *G₂* (FT: Fix_{G₂}(ℍ) ≃ SU(2); G₂/SU(3) = S⁶); Conway–Smith, *On Quaternions and Octonions* (A K Peters 2003) (SEC review: Fano-plane multiplication; the 1344 statement not retrieved from the review); Dynkin 1957 (index), Bryant 1987, Harvey–Lawson 1982 (NF, standard). | T4's two possibilities (ρ₇; 1 ⊕ 3 ⊕ 3̄ — never 1 ⊕ ρ₆) and H-A1-3 (non-split) are **in print**; the pointwise stabilizer of a quaternion subalgebra is SU(2) and G₂/SU(3) = S⁶ as used in T3; the involution lemma is self-contained in §2.3 and needs no citation. | prior art adopted with attribution; no collision; T4 and H-A1-3 corroborated. |
| **L-A1-4** homotopy | Mimura, *The homotopy groups of Lie groups of low rank*, J. Math. Kyoto Univ. 6 (1967) 131 (LS: listing confirmed; the text is behind an access block this session); Mimura–Toda 1991; Bott 1956 (NF, standard). | Because the table was not retrievable, the gate **does not rely on it**: π₁, π₃, π₄ of G₂ are derived in-instrument from SU(3) → G₂ → S⁶ with textbook inputs (§7). Mimura is cited as the canonical table. | adopted; method made independent of the unretrieved table; no collision. |
| **L-A1-5** FR / spin-statistics for solitons | Finkelstein–Rubinstein, J. Math. Phys. 9 (1968) 1762 (LS); Giulini, *On the possibility of spinorial quantization in the Skyrme model*, arXiv:hep-th/9301101 / Mod. Phys. Lett. A 8 (1993) 1917 (FT excerpt: "π₁(Q, b) ≅ π₄(SU(2), e) ≅ ℤ₂"; spinorial states iff the 2π-rotation loop is non-contractible; odd/even winding sectors); Sorkin, Comm. Math. Phys. 115 (1988) 421 (LS); Krusch, Ann. Phys. 304 (2003) 103 (carried); Krusch–Speight, *Fermionic quantization of Hopf solitons*, Comm. Math. Phys. 264 (2006) 391, arXiv:hep-th/0503067 (FT excerpt: "Hopf solitons can be quantized as fermions if their Hopf charge is odd"; π₁ of the configuration space ≅ ℤ₂ for M = S³). | The criterion "spinorial quantization ⇔ the 2π loop is non-contractible; π₁(Config) = π₄(target)" is the standard one — adopted for T3. **No published FR/spin-statistics analysis of a G₂-symmetric or octonionic condensate was located** (search-listing ceiling). | prior art (criterion); no collision; novel-in-assembly at the stated ceiling. |
| **L-A1-6** multicomponent condensates and their defects | Leonhardt–Volovik, JETP Lett. 72 (2000) 46, arXiv:cond-mat/0003428 (AB: the N = ½ vortex "the counterpart of the Alice string" in an F = 1 condensate); Semenoff–Zhou, PRL 98 (2007) 100401 (AB verbatim: "Discrete quaternion symmetries result in two species of spin defects that can only appear in integer vortices while cyclic symmetries are found to result in a phase shift of 2π/3 (or 4π/3) and therefore 1/3- (or 2/3-) quantum vortices"); Kobayashi–Kawaguchi–Nitta–Ueda, PRL 103 (2009) 115301 (LS); the cyclic phase's "12 transformations form the non-Abelian tetrahedral group" with π₁(G/H) as the vortex charge group (arXiv:1606.07190, FT footnote level); Borgh–Ruostekoski, PRL 117 (2016) 275302 (LS); Kawaguchi–Ueda, Phys. Rep. 520 (2012) 253 and Mermin, Rev. Mod. Phys. 51 (1979) 591 (NF, standard: π₁(SO(3)/Γ) = Γ\*). | The binary-polyhedral vortex groups of the spin-1/spin-2 phases arise from the **SO(3)** spin-rotation factor (π₁(SO(3)) = ℤ₂), never from a simply connected internal factor — T3's "no internal double cover" differentiator holds against this lane; Alice-string / fractional-vortex holonomies are order-parameter monodromies, not spin signs — consistent with the locked-lift trap's distinction. | prior art (defect topology); no collision; differentiator: simply connected internal factor. |
| **L-A1-7** Skyrme locking (carried from §2.87.A) | Adkins–Nappi–Witten, Nucl. Phys. B 228 (1983) 552 (LS: listing confirmed). | Unchanged; re-cited for the H2 criterion (iv). | prior art; no collision. |

**Novel-in-assembly:** VERIFIED at the stated ceilings for the question as posed — a substrate-forced factor assignment in a G₂-symmetric ℂ⊗𝕆 condensate, with the ρ₆-versus-signed-7 module distinction as the decisive fact. No collision surfaced in any cluster. The one cluster that could have rescued Assignment II (L-A1-2) does so only through a spin–orbit structure the action of record lacks, which is exactly what Phase 0 (0c) tests.

## 13. Pre-lock state and the disclosure

- **Executed chat-side, disclosed, NOT gate results:** `prechecks/precheck_algebra.py` (md5 `cf36395dba7ff35127f40e9f805ff1c7`; sympy exact rationals; no ledger value, no target) returns: dim Der(𝕆) = 14; the Clifford relations of the seven left-multiplication maps on ℝ⁸; dim span(L-bivectors, a<b≤7) = 21 and (a<b≤6) = 15; g₂ ⊂ spin(7)_L; **dim(g₂ ∩ su(4)_L) = 8**; the quaternion-subalgebra involution σ_ℍ is an automorphism with trace −1, negating a single unit is not; the 24 signed automorphism lifts of the three non-trivial pointwise-line-stabilizer collineations split as (order 2, trace −1) × 12, (order 4, trace 3) × 6, (order 4, trace −1) × 6 — **every order-2 lift has trace −1** against permutation character 3 and χ₆ = 2; 2O: ⟨χ_{3/2}, χ_{3/2}⟩ = 1, χ(1) = 4, χ(−1) = −4, **Frobenius–Schur indicator −1**; SL(2,7): exactly two solutions of g² = 1. These are the T1, T2(a), T2(c-input) and T4 witnesses; run to make sure the frame is not vacuous before the elections; re-derived from scratch by both legs under lock. No homotopy table, no ℍ screen, no Phase 2, no 1344 complement search has been computed.
- **Lock conditions — all met on September 20, 2026:** elections E-A1-1…8 (all (a)); Q-A1-1…3 answered; the LSF-δ sweep executed (§12); the gate T1 list pinned (2026b782); the action-of-record extract pinned (940b0bee). **On the author's directive this file is frozen at its md5 (lock record), the lock record generated, and schema v1.0 + comparator v1.0 frozen before any chat emission. The chat leg is not executed until the author's word.**

*v2, September 20, 2026 — LOCKED. Base V4.83 (40009ec0). Supersedes draft v1 (ee3ce0e6).*
=====END-EMBED name=staging_memo_G_2a_A1_v2.md=====

=====BEGIN-EMBED name=G_2a_A1_LOCK_RECORD.md md5=8732c390be1f442faa589bf04f7ffe9f bytes=11279 encoding=raw=====
# LOCK RECORD — Gate G-2a-A1 (Gate 2a: Baryon Spin Geometry & Factor Assignment)

**Locked:** September 20, 2026, on the author's directive "LSF-δ Sweep, T1 List, and Lock G-2a-A1" (answers Q-A1-1…3; elections E-A1-1…8 all (a); items 1–4). **Base:** `SQT_Master_Ledger_v4_83_CANONICAL.md` md5 `40009ec0197876b130766f1ae7494360` (1,589,553 B). **Chat leg NOT executed** (directive item 4: "Do not execute the Chat leg yet").

## 1. The locked memo

| Artifact | md5 | bytes | status |
|---|---|---|---|
| `staging_memo_G_2a_A1_v2.md` | **`626aa868844220eb6c3801ef07a77783`** | 61,562 | **LOCKED** (T3-immutable; supersedes draft v1 `ee3ce0e66abd02dfab053b87bfd44b93`, 50,251 B) |

The memo carries the four forcing tests T1–T4 (§2.3), the ℍ-instantiation criteria and the five-candidate screen (§2.4), the verdict classes and their machine rule (§1), the falsifiers (§5), the registered hypotheses (§6), the pinned inputs (§7), the elections (§8), the LSF-δ table (§12), and the disclosure of the chat-side pre-lock sanity checks (§13).

## 2. Pre-emission artifacts, FROZEN before any chat emission (the G-MSCS1 order; D-Q-3 not repeated)

| Artifact | md5 | bytes | notes |
|---|---|---|---|
| `g_2a_a1_schema_v1_0.json` | **`53111e0360dac138b02d5914efe85d5c`** | 6,405 | carries memo lock md5/bytes, ledger base md5, T1 list md5, extract md5, the eight elections, the required keys and typed domains for Phases 0–3, the float rules (per leg; thresholds), the verdict rule, the comparison rules |
| `g_2a_a1_compare_v1_0.py` | **`5afcd5890a9248f01a3d8a203e349039`** | 20,890 | asserts the schema md5 at load; C0 provenance + independence witness, C1–C5; free text never compared; floats per leg only; verdict recomputed from the booleans on each leg; **15 selftest suites PASS** (canonical pair: 436 checks, 0 miss; each adversarial mutation produces ≥ 1 miss as designed) |
| `tools/t1/T1_forbidden_G_2a_A1.txt` | **`2026b782db3905d9f2ce35733823618c`** | 241 | gate list = base `05302210cc4ceb70553acbe8379e9fc3` (143 B, 11 patterns) + stratum `ea3bbbbd98da8f4e9eee267beda492b7` (13 patterns), byte-exact concatenation; 24 pattern lines; md5-asserted by the instruments, never self-scanned |
| `tools/t1/t1_scan.py` | `6b86290090a8c84f1b1a0a99ec0bf697` | 1,967 | the G-MSCS1 scanner, unchanged (contextual numeric rule; pattern-index-only reporting) |
| `inputs/paper_II_3_4_4_and_3_4_7_extract.md` | **`940b0bee4b2112e911ae738c3db2bc3d`** | 12,912 | the action of record (E-A1-1(a)): §3.4.4 + §3.4.7 transcribed verbatim from project knowledge on September 20, 2026, with the author's answers Q-A1-1/Q-A1-3 in its header; the author may diff against the canonical file (a mismatch is an H-item) |
| `prechecks/precheck_algebra.py` | `cf36395dba7ff35127f40e9f805ff1c7` | — | disclosed chat-side sanity checks (memo §13); NOT a gate artifact; not re-used by the instrument |

**T1 status at lock:** the locked memo, the draft memo, the extract, the pre-check script, the schema and the comparator all scan **CLEAN** against the gate list (24 patterns; 0 hits; 0 numeric collisions). Courtesy scan against the G-MSCS1 gate list (36 patterns): one hit from a G-MSCS1-only pattern occurring as a substring of a cited paper title — not on this gate's list; no action.

## 3. Answers and elections of record (T3-immutable)

- **Q-A1-1:** 16 real components (8 complex amplitudes); the oriented term O is not U(1)-phase-invariant.
- **Q-A1-2:** the M.ONT texture envelope is a genuinely separate component (H2).
- **Q-A1-3:** no term splits the real unit from Im𝕆; proceed with H-A1-5 as a scoping note.
- **E-A1-1 (a)** action of record = the Paper II §3.4 canonical v5 file, via the pinned extract. **E-A1-2 (a)** Phase-2 witness = a single Fano-line texture core in the homogeneous ℂ⊗𝕆 GP substrate (CC-optional MV-G1 extension). **E-A1-3 (a)** "forced" = configuration-independent theorem on Sym_int and V. **E-A1-4 (a)** H1–H5 all screened (H1 as control). **E-A1-5 (a)** register I5 at the fold; the §2.50 per-strand spinor-phase import and I5 recorded as one import in two bookkeepings. **E-A1-6 (a)** compute the 1344 split/non-split disposition; bank R1 structural. **E-A1-7 (a)** additive brackets only; no retraction. **E-A1-8 (a)** Frobenius–Schur count + Galois symmetry for T2(c).

## 4. Addendum A-2 — operationalizations binding on both legs (definitions the memo leaves to the instrument, fixed here before emission)

- **A-2.1 Conventions.** Octonion basis e₀…e₇, Fano lines {i, i+1, i+3} mod 7 with e_i e_{i+1} = e_{i+3} cyclic; left-multiplication matrices L_a with column j = e_a·e_j; the complex structure of (C) is J = L₇ (the bivectors L_aL_b, a<b≤6, commute with it); 2O = the 48 unit quaternions {±1, ±i, ±j, ±k, (±1±i±j±k)/2, (±u±v)/√2 for u ≠ v ∈ {1,i,j,k}}; χ_{3/2}(q) = 2cos3φ + 2cosφ with cosφ = Re q; Frobenius–Schur indicator ν(χ) = |G|⁻¹ Σ_g χ(g²), rounded and asserted integral.
- **A-2.2 g₂ and the sl₂-classes.** g₂ = the 14-dim solution space of D(xy) = D(x)y + xD(y) on the basis (chat); CC builds it as the stabilizer of the 3-form φ in so(7). The four sl₂-classes: long-root = the pointwise stabilizer of the quaternion subalgebra ⟨1, e₁, e₂, e₄⟩ (Jordan type [2,2,1,1,1]); short-root = the sl₂ acting on Im⟨e₁,e₂,e₄⟩ by rotation, extended through SO(4) = Stab_{G₂}(ℍ_L) ([3,2,2]); su(3)-sl₂ = an sl₂ inside the stabilizer of e₇ acting irreducibly on the 3 ([3,3,1]); principal = the sl₂ with the 7 irreducible ([7]). Branching = the list of SU(2)-irrep dimensions in the 7 (weights read from an exact Cartan element). Dynkin index = ⟨φ(h), φ(h)⟩_{g₂}/⟨h, h⟩ with the invariant forms normalized so that the long-root sl₂ has index 1 (expected short-root 3, su(3)-sl₂ 1, principal 28 — the index values are witnesses, not verdict-bearing; only the long-root generator's index enters T3).
- **A-2.3 T2(b) — the spinorial 2O.** Inside su(4)_L ⊂ so(8) (the span of L_aL_b, a<b≤6) choose the spin-3/2 su(2): an sl₂-triple whose action on (ℝ⁸, J) ≅ ℂ⁴ is the irreducible 4 (weights ±3/2, ±1/2 on an exact Cartan element); exponentiate the 48 elements of 2O through it; automorphism defect of a real 8×8 matrix P := max_{i,j} ‖P(e_i e_j) − P(e_i)P(e_j)‖ (exact where the entries lie in ℚ(√2); float otherwise). Reported: the count of elements with defect 0 (expected 0), the minimum defect over 2O \ {±Id} (float rule: > 10⁻⁶), and the multiplicity of χ_{3/2} in the 2O-character of ℂ⊗𝕆 under this action (expected 2 = 4 ⊕ 4̄; control C-A1-2).
- **A-2.4 T2(c) — the Frobenius–Schur count.** SL(2,7) enumerated over 𝔽₇ (336 elements); #{g : g² = 1} (expected 2); the ordinary sector's indicator sum 1 + 6 + 7 + 8 = 22 with ν(3) = ν(3̄) = 0 (adopted, machine-checkable as memo §2.3); the Diophantine solve of 2ν₄ + 3ν₆ + 2ν₈ = −5 over ν ∈ {−1, 0, 1} under the pairings ν(σ₄) = ν(σ₄'), ν(σ₆) = ν(σ₆'); `nu4_allowed` = the sorted set of ν₄ over all solutions (expected [−1, 0]).
- **A-2.5 T3 — homotopy bookkeeping.** π₁, π₃, π₄ of G₂ from the fibration SU(3) → G₂ → S⁶ with the adopted π₁(SU(3)) = 0, π₃(SU(3)) = ℤ, π₄(SU(3)) = 0, π_k(S⁶) = 0 (k ≤ 5); the vacuum manifold of record V = S¹⁵ (π₁ = π₄ = 0, adopted π_k(Sⁿ) = 0 for k < n); the locking inventory: rank r ∈ {0,1,2} of the span of the two imaginary parts of ψ₀, H₀ ∈ {G₂, SU(3), SU(2)_long}, π₀ for the generic representative (1), the generator sl₂ of π₃(H₀) and its index, π₃-injectivity (index ≠ 0), π₄(G₂/H₀) = coker(π₄(H₀) → π₄(G₂)) ⊕ ker(π₃(H₀) → π₃(G₂)) with π₄(G₂) = 0 (expected 0 for all three); controls: π₄(S²) from U(1) → SU(2) → S² with π₄(SU(2)) = ℤ₂, π₄(S³) = ℤ₂, π₁(SO(3)/T) = |2T| = 24 (from π₁(SO(3)) = ℤ₂ and the lift of T to 2T); "no internal double cover" := π₁(G₂) = 0 ∧ phase group finite; "envelope-in-𝕆 kill" := π₂(S⁶) = 0 (the inclusion S² ↪ S⁶ null-homotopic ⇒ induced map on π₄ zero).
- **A-2.6 Phase 2 — the pinned witness.** Domain ℝ² (r, φ); ψ(x) = √ρ₀ (sin f(r) cos φ e_a + sin f(r) sin φ e_b + cos f(r) e_c) with (a,b,c) = (1,2,4) for the line object and (1,2,3) for the non-line control; profile f(r) = π/(1 + r²) (fixed; `profile_id` = "lockrec-A-2.6"); ρ₀ = 1. Computations as memo §4 Phase 2 (a)–(e): O evaluated as the exact structure-constant contraction φ_abc times the geometric integral (the integral is common to both objects; O_nonline is the exact zero φ_{123} = 0; O_line ∝ φ_{124} = ±1 times a positive integral — reported per leg, only the booleans compared); the stabilizer's internal image SO(4) = Stab_{G₂}(ℍ_L) with kernel SU(2)_long; the two lifts (q_α, q_α) (diagonal, identity at 2π) and (1, q_α) (σ_ℍ at 2π) exhibited as exact 8×8 matrices; π₀(Stab) and π₁(Orbit) = π₀(Stab) per the fibration Stab → SO(2) × Sym_int → Orbit with the diagonal loop winding once in π₁(SO(2)) = ℤ; the chiral-pair characters e^{±iα}.
- **A-2.7 The 1344 group (E-A1-6(a)).** Generated as the set of signed permutation matrices on Im𝕆 that are automorphisms (expected order 1344); presentation of PSL(2,7): ⟨a, b | a² = b³ = (ab)⁷ = [a,b]⁴ = 1⟩ with a = the collineation (3 5)(6 7) fixing {1,2,4} pointwise and b = a fixed order-3 collineation (both legs state theirs); each generator lifted by the 8 sign-kernel elements → 64 pairs; the subgroup generated by each pair closed by BFS; `complements_found` = the number of pairs generating a subgroup of order exactly 168 (expected 0 ⇒ non-split).
- **A-2.8 Checkpoint discipline (E8).** One JSON checkpoint per leg with the keys of the schema; free text allowed anywhere else and never compared; every adopted fact carries its citation string in a `citations` field (ignored by the comparator); the instrument md5-guards the memo (626aa868), the T1 list (2026b782), the extract (940b0bee), scans itself, the memo and the extract with the scanner, and halts on any hit or any missing file — D-T1 is retired; no `--no-t1-halt` flag exists.

## 5. Order of operations from here (binding)

Memo LOCKED (this record) → schema v1.0 + comparator v1.0 FROZEN (this record) → **[await the author's word]** → chat instrument (guards as A-2.8) → Phase 0 → Phase 1 → Phase 1b → Phase 2 → Phase 3 → execution report → P-4/P-4.b/P-4.c dispatch (the T1 lists in-band) → CC leg blind from scratch (method variations: g₂ from φ; own class enumeration of SL(2,7); own exact-sequence code; optional MV-G1 extension) → two-leg comparison → S9 on misses → fold authorization → V4.84 (with the §10 housekeeping bracket).

## 6. Estate at lock (md5 / bytes)

memo v2 626aa868 / 61,562; draft v1 ee3ce0e6 / 50,251; lock record — this file; schema 53111e03 / 6,405; comparator 5afcd589 / 20,890; T1 gate list 2026b782 / 241; T1 stratum ea3bbbbd; T1 base 05302210 / 143; scanner 6b862900 / 1,967; extract 940b0bee / 12,912; prechecks cf36395d (+ log). Manifest `LOCK_MANIFEST.md5` alongside.
=====END-EMBED name=G_2a_A1_LOCK_RECORD.md=====

=====BEGIN-EMBED name=g_2a_a1_schema_v1_0.json md5=53111e0360dac138b02d5914efe85d5c bytes=6405 encoding=raw=====
{
  "schema": "G-2a-A1 checkpoint schema v1.0",
  "gate": "G-2a-A1",
  "frozen": "2026-09-20",
  "memo_lock_md5": "626aa868844220eb6c3801ef07a77783",
  "memo_lock_bytes": 61562,
  "ledger_base_md5": "40009ec0197876b130766f1ae7494360",
  "t1_list_md5": "2026b782db3905d9f2ce35733823618c",
  "action_extract_md5": "940b0bee4b2112e911ae738c3db2bc3d",
  "elections": {"E-A1-1": "a", "E-A1-2": "a", "E-A1-3": "a", "E-A1-4": "a", "E-A1-5": "a", "E-A1-6": "a", "E-A1-7": "a", "E-A1-8": "a"},
  "required_top": ["gate", "leg", "instrument_md5", "memo_lock_md5", "ledger_base_md5", "t1_list_md5", "action_extract_md5", "t1_scan", "elections", "phase0", "phase1", "phase1b", "phase2", "phase3"],
  "leg_domain": ["chat", "cc"],
  "t1_scan_required": ["instrument", "memo", "extract"],
  "t1_scan_domain": ["CLEAN"],
  "phase0": {
    "exact_keys": {
      "field_real_components": "int", "complex_amplitudes": "int", "spinor_index_present": "bool",
      "spatial_internal_direct_product": "bool", "sym_int_pinned": "bool",
      "sym_int_continuous": "str", "sym_int_continuous_dim": "int",
      "g2_preserves_O": "bool", "generic_so16_breaks_O": "bool",
      "phase_subgroup_order": "int", "O_phase_invariant": "bool", "conjugation_maps_O_to_conjugate": "bool",
      "two_body_symmetry": "str", "vacuum_manifold_of_record": "str", "pi1_V": "int", "pi4_V": "int",
      "real_unit_splitting_term_present": "bool",
      "controls": {"L_perp_zero_mode": "bool", "F21_split_1_3_3bar": "bool", "generic_so16_fails_margin_positive": "bool"}
    },
    "list_keys": {
      "locking_inventory": {"sort_by": "rank", "item_keys": {"rank": "int", "H0": "str", "H0_dim": "int", "pi0_generic": "int", "sl2_generator_jordan_type": "list", "sl2_generator_index": "int", "pi3_injective": "bool", "pi4_quotient": "int"}}
    },
    "domains": {"sym_int_continuous": ["G2"], "two_body_symmetry": ["O(16)"], "vacuum_manifold_of_record": ["S15"], "H0": ["G2", "SU3", "SU2_long"]}
  },
  "phase1": {
    "T1": {"exact_keys": {"holds": "bool", "chi32_norm": "int", "chi32_at_1": "int", "chi32_at_minus1": "int", "fs_indicator": "int", "seven_real": "bool", "quartet_multiplicity_upper": "int", "phase_char_on_2O_trivial": "bool", "branching_long_root": "list", "branching_short_root": "list", "branching_su3_sl2": "list", "branching_principal": "list", "control_sym3_quartet_mult": "int"}},
    "T2": {"exact_keys": {"holds": "bool", "dim_der": "int", "dim_bivectors_7": "int", "dim_bivectors_6": "int", "g2_in_spin7": "bool", "dim_g2_cap_su4": "int", "spinor_2O_order": "int", "spinor_2O_automorphism_count": "int", "spinor_2O_quartet_mult": "int", "sl27_order": "int", "sl27_sq1_count": "int", "fs_sum_ordinary": "int", "nu4_allowed": "list", "involution_trace": "int", "sigma_H_is_automorphism": "bool", "single_unit_negation_is_automorphism": "bool", "control_1344_all_automorphisms": "bool", "group1344_order": "int"},
           "float_keys": {"spinor_2O_min_automorphism_defect": {"rule": "gt", "threshold": 1e-6}}},
    "T3": {"exact_keys": {"holds": "bool", "pi1_G2": "int", "pi3_G2": "str", "pi4_G2": "int", "pi1_V": "int", "pi4_V": "int", "no_internal_double_cover": "bool", "envelope_in_O_kill": "bool", "controls_pi4_S2": "str", "controls_pi4_S3": "str", "controls_pi1_SO3_mod_T": "int"}},
    "T4": {"exact_keys": {"holds": "bool", "lifts_total": "int", "order2_count": "int", "order2_traces_set": "list", "order4_count": "int", "order4_traces_set": "list", "perm_char_involution": "int", "rho6_char_2A": "int", "gap": "int", "control_F21_unsigned_1_3_3bar": "bool", "nu2_unsigned_automorphism": "bool"}},
    "group1344": {"exact_keys": {"order": "int", "split": "bool", "complements_found": "int", "lift_pairs_tested": "int"}}
  },
  "phase1b": {
    "P_C": {"exact_keys": {"complex_unit_central": "bool", "e8_anticommutes": "bool", "e8_central": "bool", "disposition": "str"}},
    "H_screen_candidates": ["H1", "H2", "H3", "H4", "H5"],
    "H_item_keys": {"i": "str", "ii": "str", "iii": "str", "iv": "str", "code": "str", "role": "str"},
    "H_criterion_domain": ["pass", "fail", "conditional", "dynamical", "kinematic", "n/a"],
    "exact_keys": {"I5_registered": "bool", "admissible": "list"}
  },
  "phase2": {
    "exact_keys": {"object": "str", "control_object": "str", "profile_id": "str", "O_nonzero_on_line": "bool", "O_zero_on_nonline": "bool", "stab_internal_image": "str", "stab_kernel": "str", "stab_subdirect": "bool", "pi0_stab": "int", "loop_images": "list", "sigma_H_eigen_plus1": "int", "sigma_H_eigen_minus1": "int", "label": "str", "pi1_orbit": "int", "chiral_pair_character_ordinary": "bool", "dimension_note": "str"},
    "float_keys": {"O_line_abs": {"rule": "gt", "threshold": 1e-6}, "O_nonline_abs": {"rule": "le", "threshold": 1e-9}},
    "domains": {"label": ["INTERNAL-HOLONOMY-GAUGE", "INTERNAL-HOLONOMY-FIXED", "NONE"]}
  },
  "phase3": {
    "exact_keys": {"verdict": "str", "tests_holding": "list", "admissible_H": "list", "I5": "bool", "controls_all_pass": "bool"},
    "verdict_domain": ["ASSIGNMENT-I-FORCED", "ASSIGNMENT-II-REALIZABLE", "UNDECIDED-BY-SUBSTRATE", "INDETERMINATE"]
  },
  "verdict_rule": "INDETERMINATE if not phase3.controls_all_pass; else UNDECIDED-BY-SUBSTRATE if not phase0.sym_int_pinned; else ASSIGNMENT-II-REALIZABLE if (not phase0.spatial_internal_direct_product) or any of T1..T4 holds == false; else ASSIGNMENT-I-FORCED. controls_all_pass is recomputed by the comparator as the conjunction of: phase0.controls.*, T1.control_sym3_quartet_mult == 1, T2.control_1344_all_automorphisms, T2.spinor_2O_quartet_mult == 2, T3.controls_pi4_S2 == 'Z2', T3.controls_pi4_S3 == 'Z2', T3.controls_pi1_SO3_mod_T == 24, T4.control_F21_unsigned_1_3_3bar, T4.nu2_unsigned_automorphism, phase2.O_zero_on_nonline.",
  "comparison_rules": {
    "exact": "ints, bools, strings and lists compared for equality after canonical ordering of list-of-dicts by their declared sort key; lists of scalars compared as sorted lists where the key name ends with _set or is nu4_allowed, admissible, admissible_H, tests_holding, loop_images; other lists compared in order",
    "float": "per-key rule (gt/le threshold) evaluated on each leg separately; magnitudes are not compared across legs",
    "free_text": "never compared (any key not declared above is ignored)",
    "independence_witness": "instrument_md5 must differ between legs; checkpoint bytes need not be identical"
  }
}
=====END-EMBED name=g_2a_a1_schema_v1_0.json=====

=====BEGIN-EMBED name=g_2a_a1_compare_v1_0.py md5=5afcd5890a9248f01a3d8a203e349039 bytes=20890 encoding=raw=====
#!/usr/bin/env python3
"""g_2a_a1_compare_v1_0.py — two-leg comparator for Gate G-2a-A1, FROZEN v1.0 (September 20, 2026).

Compares the chat-leg and CC-leg E8 checkpoints against g_2a_a1_schema_v1_0.json.
Checks: C0 provenance + independence witness; C1 Phase 0; C2 Phase 1 (T1..T4, group1344);
C3 Phase 1b (P_C, H screen, I5); C4 Phase 2; C5 Phase 3 (verdict identity + verdict recomputed
from the booleans by the schema's rule + internal consistency). Free text is never compared.
Floats are checked per leg against the schema's rule (gt/le threshold), never across legs.

Usage:
  compare  : python3 g_2a_a1_compare_v1_0.py compare CHAT.json CC.json [--schema S.json] [--out OUT.json]
  selftest : python3 g_2a_a1_compare_v1_0.py selftest
Exit: 0 all PASS, 1 any MISS, 2 usage/fatal.
"""
import hashlib, json, sys, copy

SCHEMA_DEFAULT = "g_2a_a1_schema_v1_0.json"
SCHEMA_MD5 = "53111e0360dac138b02d5914efe85d5c"   # frozen schema v1.0 md5; asserted at load

SORTED_LIST_KEYS = {"nu4_allowed", "admissible", "admissible_H", "tests_holding", "loop_images"}
CONTROL_TRUE = ["L_perp_zero_mode", "F21_split_1_3_3bar", "generic_so16_fails_margin_positive"]

def md5_file(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

def load_schema(path):
    raw = open(path, "rb").read()
    h = hashlib.md5(raw).hexdigest()
    if SCHEMA_MD5 != "__SCHEMA_MD5__" and h != SCHEMA_MD5:
        raise SystemExit(f"FATAL: schema md5 {h} != frozen {SCHEMA_MD5}")
    return json.loads(raw.decode("utf-8")), h

def canon(v, key=None):
    if isinstance(v, list):
        if key and (key.endswith("_set") or key in SORTED_LIST_KEYS):
            return sorted(v, key=lambda x: json.dumps(x, sort_keys=True))
        return [canon(x) for x in v]
    if isinstance(v, dict):
        return {k: canon(v[k], k) for k in sorted(v)}
    return v

TYPE = {"int": int, "bool": bool, "str": str, "list": list}
def typed_ok(v, t):
    if t == "int": return isinstance(v, int) and not isinstance(v, bool)
    if t == "bool": return isinstance(v, bool)
    if t == "str": return isinstance(v, str)
    if t == "list": return isinstance(v, list)
    if isinstance(t, dict): return isinstance(v, dict)
    return False

class Rec:
    def __init__(self):
        self.rows = []
    def add(self, check, name, ok, a=None, b=None, note=""):
        self.rows.append({"check": check, "name": name, "pass": bool(ok), "chat": a, "cc": b, "note": note})
    def summary(self):
        n = len(self.rows); p = sum(r["pass"] for r in self.rows)
        return {"checks": n, "pass": p, "miss": n - p}

def get(d, path, default=None):
    cur = d
    for k in path.split("."):
        if not isinstance(cur, dict) or k not in cur: return default
        cur = cur[k]
    return cur

def cmp_exact_block(R, check, label, A, B, keys):
    for k, t in keys.items():
        va, vb = (A or {}).get(k), (B or {}).get(k)
        if isinstance(t, dict):   # nested exact block (e.g. controls)
            cmp_exact_block(R, check, f"{label}.{k}", va or {}, vb or {}, t)
            continue
        okt = typed_ok(va, t) and typed_ok(vb, t)
        R.add(check, f"{label}.{k} typed", okt, va, vb, f"type {t}")
        R.add(check, f"{label}.{k} equal", okt and canon(va, k) == canon(vb, k), va, vb)

def cmp_float_block(R, check, label, A, B, keys):
    for k, rule in keys.items():
        for leg, D in (("chat", A), ("cc", B)):
            v = (D or {}).get(k)
            ok = isinstance(v, (int, float)) and not isinstance(v, bool)
            if ok:
                ok = (v > rule["threshold"]) if rule["rule"] == "gt" else (v <= rule["threshold"])
            R.add(check, f"{label}.{k} ({leg}) {rule['rule']} {rule['threshold']}", ok, v if leg == "chat" else None, v if leg == "cc" else None)

def domain_check(R, check, label, A, B, key, domain):
    for leg, D in (("chat", A), ("cc", B)):
        v = (D or {}).get(key)
        R.add(check, f"{label}.{key} ({leg}) in domain", v in domain, v if leg == "chat" else None, v if leg == "cc" else None)

def recompute_controls(ck):
    c0 = get(ck, "phase0.controls", {}) or {}
    ok = all(c0.get(k) is True for k in CONTROL_TRUE)
    ok = ok and get(ck, "phase1.T1.control_sym3_quartet_mult") == 1
    ok = ok and get(ck, "phase1.T2.control_1344_all_automorphisms") is True
    ok = ok and get(ck, "phase1.T2.spinor_2O_quartet_mult") == 2
    ok = ok and get(ck, "phase1.T3.controls_pi4_S2") == "Z2"
    ok = ok and get(ck, "phase1.T3.controls_pi4_S3") == "Z2"
    ok = ok and get(ck, "phase1.T3.controls_pi1_SO3_mod_T") == 24
    ok = ok and get(ck, "phase1.T4.control_F21_unsigned_1_3_3bar") is True
    ok = ok and get(ck, "phase1.T4.nu2_unsigned_automorphism") is True
    ok = ok and get(ck, "phase2.O_zero_on_nonline") is True
    return bool(ok)

def recompute_verdict(ck):
    if not recompute_controls(ck): return "INDETERMINATE"
    if get(ck, "phase0.sym_int_pinned") is not True: return "UNDECIDED-BY-SUBSTRATE"
    holds = [get(ck, f"phase1.{t}.holds") for t in ("T1", "T2", "T3", "T4")]
    if get(ck, "phase0.spatial_internal_direct_product") is not True or any(h is not True for h in holds):
        return "ASSIGNMENT-II-REALIZABLE"
    return "ASSIGNMENT-I-FORCED"

def compare(chat, cc, S):
    R = Rec()
    # ---------------- C0 provenance ----------------
    for k in S["required_top"]:
        R.add("C0", f"required key {k} present (chat)", k in chat)
        R.add("C0", f"required key {k} present (cc)", k in cc)
    for k in ("memo_lock_md5", "ledger_base_md5", "t1_list_md5", "action_extract_md5"):
        R.add("C0", f"{k} == schema (chat)", chat.get(k) == S[k], chat.get(k), S[k])
        R.add("C0", f"{k} == schema (cc)", cc.get(k) == S[k], cc.get(k), S[k])
    R.add("C0", "gate label", chat.get("gate") == S["gate"] and cc.get("gate") == S["gate"], chat.get("gate"), cc.get("gate"))
    R.add("C0", "leg labels chat/cc", chat.get("leg") == "chat" and cc.get("leg") == "cc", chat.get("leg"), cc.get("leg"))
    for f in S["t1_scan_required"]:
        R.add("C0", f"t1_scan.{f} CLEAN (chat)", get(chat, f"t1_scan.{f}") in S["t1_scan_domain"], get(chat, f"t1_scan.{f}"))
        R.add("C0", f"t1_scan.{f} CLEAN (cc)", get(cc, f"t1_scan.{f}") in S["t1_scan_domain"], None, get(cc, f"t1_scan.{f}"))
    R.add("C0", "elections == schema (chat)", chat.get("elections") == S["elections"], chat.get("elections"), S["elections"])
    R.add("C0", "elections == schema (cc)", cc.get("elections") == S["elections"], cc.get("elections"), S["elections"])
    R.add("C0", "independence witness: instrument_md5 differ", bool(chat.get("instrument_md5")) and bool(cc.get("instrument_md5")) and chat.get("instrument_md5") != cc.get("instrument_md5"), chat.get("instrument_md5"), cc.get("instrument_md5"))
    # ---------------- C1 phase0 ----------------
    P0 = S["phase0"]; A, B = chat.get("phase0", {}), cc.get("phase0", {})
    cmp_exact_block(R, "C1", "phase0", A, B, P0["exact_keys"])
    for k, dom in P0["domains"].items():
        if k == "H0": continue
        domain_check(R, "C1", "phase0", A, B, k, dom)
    for k in CONTROL_TRUE:
        R.add("C1", f"phase0.controls.{k} true both legs", get(A, f"controls.{k}") is True and get(B, f"controls.{k}") is True, get(A, f"controls.{k}"), get(B, f"controls.{k}"))
    spec = P0["list_keys"]["locking_inventory"]
    la, lb = A.get("locking_inventory"), B.get("locking_inventory")
    okl = isinstance(la, list) and isinstance(lb, list) and len(la) == len(lb)
    R.add("C1", "locking_inventory list length equal", okl, len(la) if isinstance(la, list) else None, len(lb) if isinstance(lb, list) else None)
    if okl:
        la = sorted(la, key=lambda x: x.get(spec["sort_by"], -1)); lb = sorted(lb, key=lambda x: x.get(spec["sort_by"], -1))
        for ia, ib in zip(la, lb):
            cmp_exact_block(R, "C1", f"locking_inventory[rank={ia.get('rank')}]", ia, ib, spec["item_keys"])
            R.add("C1", f"locking_inventory[rank={ia.get('rank')}].H0 in domain", ia.get("H0") in P0["domains"]["H0"] and ib.get("H0") in P0["domains"]["H0"], ia.get("H0"), ib.get("H0"))
    # ---------------- C2 phase1 ----------------
    P1 = S["phase1"]; A, B = chat.get("phase1", {}), cc.get("phase1", {})
    for blk in ("T1", "T2", "T3", "T4", "group1344"):
        cmp_exact_block(R, "C2", f"phase1.{blk}", A.get(blk), B.get(blk), P1[blk]["exact_keys"])
        if "float_keys" in P1[blk]:
            cmp_float_block(R, "C2", f"phase1.{blk}", A.get(blk), B.get(blk), P1[blk]["float_keys"])
    # ---------------- C3 phase1b ----------------
    P1b = S["phase1b"]; A, B = chat.get("phase1b", {}), cc.get("phase1b", {})
    cmp_exact_block(R, "C3", "phase1b.P_C", A.get("P_C"), B.get("P_C"), P1b["P_C"]["exact_keys"])
    for h in P1b["H_screen_candidates"]:
        ha, hb = get(A, f"H_screen.{h}"), get(B, f"H_screen.{h}")
        cmp_exact_block(R, "C3", f"phase1b.H_screen.{h}", ha, hb, P1b["H_item_keys"])
        for crit in ("i", "ii", "iii", "iv"):
            domain_check(R, "C3", f"phase1b.H_screen.{h}", ha, hb, crit, P1b["H_criterion_domain"])
    cmp_exact_block(R, "C3", "phase1b", A, B, P1b["exact_keys"])
    # ---------------- C4 phase2 ----------------
    P2 = S["phase2"]; A, B = chat.get("phase2", {}), cc.get("phase2", {})
    cmp_exact_block(R, "C4", "phase2", A, B, P2["exact_keys"])
    cmp_float_block(R, "C4", "phase2", A, B, P2["float_keys"])
    domain_check(R, "C4", "phase2", A, B, "label", P2["domains"]["label"])
    # ---------------- C5 phase3 ----------------
    P3 = S["phase3"]; A, B = chat.get("phase3", {}), cc.get("phase3", {})
    cmp_exact_block(R, "C5", "phase3", A, B, P3["exact_keys"])
    domain_check(R, "C5", "phase3", A, B, "verdict", P3["verdict_domain"])
    for leg, ck, D in (("chat", chat, A), ("cc", cc, B)):
        rv = recompute_verdict(ck)
        R.add("C5", f"verdict recomputed == reported ({leg})", rv == D.get("verdict"), rv if leg == "chat" else None, rv if leg == "cc" else None, f"reported {D.get('verdict')}")
        rc = recompute_controls(ck)
        R.add("C5", f"controls_all_pass recomputed == reported ({leg})", rc == D.get("controls_all_pass"), rc if leg == "chat" else None, rc if leg == "cc" else None)
        th = sorted(t for t in ("T1", "T2", "T3", "T4") if get(ck, f"phase1.{t}.holds") is True)
        R.add("C5", f"tests_holding consistent with T*.holds ({leg})", sorted(D.get("tests_holding") or []) == th, th if leg == "chat" else None, th if leg == "cc" else None)
        R.add("C5", f"admissible_H == phase1b.admissible ({leg})", sorted(D.get("admissible_H") or []) == sorted(get(ck, "phase1b.admissible") or []), None, None)
        R.add("C5", f"I5 == phase1b.I5_registered ({leg})", D.get("I5") == get(ck, "phase1b.I5_registered"), None, None)
    return R

# ---------------------------------------------------------------- selftest
def canonical_checkpoint(leg):
    """A synthetic checkpoint carrying the memo's a-priori expected values (H-A1-1..4). NOT a result —
    the instrument writes its own; this exists so the comparator's logic is exercised before any emission."""
    S = json.load(open(SCHEMA_DEFAULT, encoding="utf-8")) if _have_schema() else None
    prov = {k: (S[k] if S else "x") for k in ("memo_lock_md5", "ledger_base_md5", "t1_list_md5", "action_extract_md5")}
    el = S["elections"] if S else {f"E-A1-{i}": "a" for i in range(1, 9)}
    inv = [
        {"rank": 0, "H0": "G2", "H0_dim": 14, "pi0_generic": 1, "sl2_generator_jordan_type": [2, 2, 1, 1, 1], "sl2_generator_index": 1, "pi3_injective": True, "pi4_quotient": 0},
        {"rank": 1, "H0": "SU3", "H0_dim": 8, "pi0_generic": 1, "sl2_generator_jordan_type": [2, 2, 1, 1, 1], "sl2_generator_index": 1, "pi3_injective": True, "pi4_quotient": 0},
        {"rank": 2, "H0": "SU2_long", "H0_dim": 3, "pi0_generic": 1, "sl2_generator_jordan_type": [2, 2, 1, 1, 1], "sl2_generator_index": 1, "pi3_injective": True, "pi4_quotient": 0},
    ]
    ck = {
        "gate": "G-2a-A1", "leg": leg, "instrument_md5": "chat" * 8 if leg == "chat" else "cc00" * 8,
        **prov, "t1_scan": {"instrument": "CLEAN", "memo": "CLEAN", "extract": "CLEAN"}, "elections": el,
        "phase0": {"field_real_components": 16, "complex_amplitudes": 8, "spinor_index_present": False,
                   "spatial_internal_direct_product": True, "sym_int_pinned": True, "sym_int_continuous": "G2", "sym_int_continuous_dim": 14,
                   "g2_preserves_O": True, "generic_so16_breaks_O": True, "phase_subgroup_order": 3, "O_phase_invariant": False,
                   "conjugation_maps_O_to_conjugate": True, "two_body_symmetry": "O(16)", "vacuum_manifold_of_record": "S15", "pi1_V": 0, "pi4_V": 0,
                   "real_unit_splitting_term_present": False,
                   "controls": {"L_perp_zero_mode": True, "F21_split_1_3_3bar": True, "generic_so16_fails_margin_positive": True},
                   "locking_inventory": inv if leg == "chat" else list(reversed(inv))},
        "phase1": {
            "T1": {"holds": True, "chi32_norm": 1, "chi32_at_1": 4, "chi32_at_minus1": -4, "fs_indicator": -1, "seven_real": True, "quartet_multiplicity_upper": 0,
                   "phase_char_on_2O_trivial": True, "branching_long_root": [2, 2, 1, 1, 1], "branching_short_root": [3, 2, 2], "branching_su3_sl2": [3, 3, 1], "branching_principal": [7], "control_sym3_quartet_mult": 1},
            "T2": {"holds": True, "dim_der": 14, "dim_bivectors_7": 21, "dim_bivectors_6": 15, "g2_in_spin7": True, "dim_g2_cap_su4": 8, "spinor_2O_order": 48,
                   "spinor_2O_automorphism_count": 0, "spinor_2O_quartet_mult": 2, "sl27_order": 336, "sl27_sq1_count": 2, "fs_sum_ordinary": 22, "nu4_allowed": [-1, 0] if leg == "chat" else [0, -1],
                   "involution_trace": -1, "sigma_H_is_automorphism": True, "single_unit_negation_is_automorphism": False, "control_1344_all_automorphisms": True, "group1344_order": 1344,
                   "spinor_2O_min_automorphism_defect": 0.5 if leg == "chat" else 0.37},
            "T3": {"holds": True, "pi1_G2": 0, "pi3_G2": "Z", "pi4_G2": 0, "pi1_V": 0, "pi4_V": 0, "no_internal_double_cover": True, "envelope_in_O_kill": True,
                   "controls_pi4_S2": "Z2", "controls_pi4_S3": "Z2", "controls_pi1_SO3_mod_T": 24},
            "T4": {"holds": True, "lifts_total": 24, "order2_count": 12, "order2_traces_set": [-1], "order4_count": 12, "order4_traces_set": [3, -1] if leg == "chat" else [-1, 3],
                   "perm_char_involution": 3, "rho6_char_2A": 2, "gap": 4, "control_F21_unsigned_1_3_3bar": True, "nu2_unsigned_automorphism": True},
            "group1344": {"order": 1344, "split": False, "complements_found": 0, "lift_pairs_tested": 64},
        },
        "phase1b": {"P_C": {"complex_unit_central": True, "e8_anticommutes": True, "e8_central": False, "disposition": "CLOSED-BY-INSTANTIATION"},
                    "H_screen": {"H1": {"i": "fail", "ii": "pass", "iii": "fail", "iv": "n/a", "code": "EXCLUDED(i,iii)", "role": "control"},
                                 "H2": {"i": "pass", "ii": "pass", "iii": "pass", "iv": "dynamical", "code": "ADMISSIBLE-IMPORT", "role": "candidate"},
                                 "H3": {"i": "pass", "ii": "pass", "iii": "conditional", "iv": "kinematic", "code": "ADMISSIBLE-IMPORT", "role": "candidate"},
                                 "H4": {"i": "fail", "ii": "pass", "iii": "n/a", "iv": "n/a", "code": "EXCLUDED(i)", "role": "candidate"},
                                 "H5": {"i": "pass", "ii": "fail", "iii": "n/a", "iv": "n/a", "code": "EXCLUDED(ii,centrality)", "role": "candidate"}},
                    "I5_registered": True, "admissible": ["H2", "H3"] if leg == "chat" else ["H3", "H2"]},
        "phase2": {"object": "fano_line_texture_L124_homogeneous_GP_2D", "control_object": "nonline_texture_L123", "profile_id": "lockrec-A-2.6",
                   "O_nonzero_on_line": True, "O_zero_on_nonline": True, "stab_internal_image": "SO4_Stab_HL", "stab_kernel": "SU2_long", "stab_subdirect": True,
                   "pi0_stab": 1, "loop_images": ["Id", "sigma_H"], "sigma_H_eigen_plus1": 4, "sigma_H_eigen_minus1": 4, "label": "INTERNAL-HOLONOMY-GAUGE",
                   "pi1_orbit": 0, "chiral_pair_character_ordinary": True, "dimension_note": "2D witness; contractibility of the 2pi loop in the orbit only",
                   "O_line_abs": 0.2 if leg == "chat" else 0.31, "O_nonline_abs": 0.0},
        "phase3": {"verdict": "ASSIGNMENT-I-FORCED", "tests_holding": ["T1", "T2", "T3", "T4"], "admissible_H": ["H2", "H3"], "I5": True, "controls_all_pass": True},
    }
    return ck

def _have_schema():
    try:
        open(SCHEMA_DEFAULT, "rb").close(); return True
    except OSError:
        return False

def run(chat, cc, S):
    R = compare(chat, cc, S); s = R.summary(); return R, s

def selftest():
    S, h = load_schema(SCHEMA_DEFAULT)
    suites = []
    def suite(name, mut, expect_miss_min=1, expect_pass=False):
        a, b = canonical_checkpoint("chat"), canonical_checkpoint("cc")
        mut(a, b)
        R, s = run(a, b, S)
        ok = (s["miss"] == 0) if expect_pass else (s["miss"] >= expect_miss_min)
        suites.append((name, ok, s))
        return R
    suite("S1 canonical legs (list orders permuted, floats differ) -> ALL PASS", lambda a, b: None, expect_pass=True)
    suite("S2 T1.holds flipped on cc -> C2 miss + C5 verdict mismatch", lambda a, b: b["phase1"]["T1"].__setitem__("holds", False), 2)
    suite("S3 missing required key (phase2) on chat", lambda a, b: a.pop("phase2"), 1)
    suite("S4 wrong election code", lambda a, b: a["elections"].__setitem__("E-A1-2", "b"), 1)
    suite("S5 T1 scan HIT on memo (cc)", lambda a, b: b["t1_scan"].__setitem__("memo", "HIT"), 1)
    suite("S6 verdict inconsistent with booleans (both legs report II while all hold)", lambda a, b: (a["phase3"].__setitem__("verdict", "ASSIGNMENT-II-REALIZABLE"), b["phase3"].__setitem__("verdict", "ASSIGNMENT-II-REALIZABLE")), 2)
    suite("S7 identical instrument md5 (independence witness)", lambda a, b: b.__setitem__("instrument_md5", a["instrument_md5"]), 1)
    suite("S8 float rule: automorphism defect below threshold (chat)", lambda a, b: a["phase1"]["T2"].__setitem__("spinor_2O_min_automorphism_defect", 1e-9), 1)
    suite("S9 control failure -> INDETERMINATE recomputed vs reported", lambda a, b: a["phase1"]["T3"].__setitem__("controls_pi4_S2", "0"), 1)
    suite("S10 provenance md5 mismatch (ledger base)", lambda a, b: a.__setitem__("ledger_base_md5", "deadbeef" * 4), 1)
    suite("S11 locking inventory H0 out of domain", lambda a, b: b["phase0"]["locking_inventory"][0].__setitem__("H0", "SO4"), 1)
    suite("S12 H-screen criterion out of domain", lambda a, b: a["phase1b"]["H_screen"]["H2"].__setitem__("iii", "maybe"), 1)
    suite("S13 direct product false on both legs -> verdict must be II (reported I) -> C5 miss", lambda a, b: (a["phase0"].__setitem__("spatial_internal_direct_product", False), b["phase0"].__setitem__("spatial_internal_direct_product", False)), 2)
    suite("S14 typed: int given as bool", lambda a, b: a["phase1"]["T4"].__setitem__("gap", True), 1)
    suite("S15 phase2 nonline O not zero (cc)", lambda a, b: b["phase2"].__setitem__("O_nonline_abs", 1e-3), 1)
    allok = all(ok for _, ok, _ in suites)
    print(f"schema md5 {h}")
    for name, ok, s in suites:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}  (checks={s['checks']}, pass={s['pass']}, miss={s['miss']})")
    print("SELFTEST", "PASS" if allok else "FAIL")
    return 0 if allok else 1

def main():
    if len(sys.argv) < 2: print(__doc__); return 2
    if sys.argv[1] == "selftest": return selftest()
    if sys.argv[1] == "compare":
        args = sys.argv[2:]
        schema = SCHEMA_DEFAULT; out = None
        if "--schema" in args:
            i = args.index("--schema"); schema = args[i + 1]; del args[i:i + 2]
        if "--out" in args:
            i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
        if len(args) != 2: print(__doc__); return 2
        S, h = load_schema(schema)
        chat = json.load(open(args[0], encoding="utf-8")); cc = json.load(open(args[1], encoding="utf-8"))
        R, s = run(chat, cc, S)
        res = {"comparator": "g_2a_a1_compare_v1_0", "schema_md5": h, "chat_ckpt_md5": md5_file(args[0]), "cc_ckpt_md5": md5_file(args[1]),
               "summary": s, "misses": [r for r in R.rows if not r["pass"]], "rows": R.rows}
        txt = json.dumps(res, indent=1, ensure_ascii=False, sort_keys=True)
        if out: open(out, "w", encoding="utf-8").write(txt)
        print(f"G-2a-A1 two-leg comparison: checks={s['checks']} pass={s['pass']} miss={s['miss']}")
        for r in res["misses"]: print(f"  MISS [{r['check']}] {r['name']}: chat={r['chat']} cc={r['cc']} {r['note']}")
        return 0 if s["miss"] == 0 else 1
    print(__doc__); return 2

if __name__ == "__main__":
    sys.exit(main())
=====END-EMBED name=g_2a_a1_compare_v1_0.py=====

=====BEGIN-EMBED name=tools/t1/T1_forbidden_G_2a_A1.txt md5=2026b782db3905d9f2ce35733823618c bytes=241 encoding=raw=====
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
1.913
1.9130
2.793
2.7928
μ_N
nuclear magneton
magneton
PDG
CODATA
938.27
939.57
1836.15
0.68498
=====END-EMBED name=tools/t1/T1_forbidden_G_2a_A1.txt=====

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

=====BEGIN-EMBED name=tools/t1/T1_stratum_G_2a_A1.txt md5=ea3bbbbd98da8f4e9eee267beda492b7 bytes=98 encoding=raw=====
1.913
1.9130
2.793
2.7928
μ_N
nuclear magneton
magneton
PDG
CODATA
938.27
939.57
1836.15
0.68498
=====END-EMBED name=tools/t1/T1_stratum_G_2a_A1.txt=====

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

=====BEGIN-EMBED name=inputs/paper_II_3_4_4_and_3_4_7_extract.md md5=940b0bee4b2112e911ae738c3db2bc3d bytes=12912 encoding=raw=====
# Action-of-record extract for Gate G-2a-A1 — Paper II §3.4.4 and §3.4.7 (E-A1-1(a))

**Provenance.** Transcribed verbatim from the project-knowledge document `paper_II_section_3_4_CANONICAL_v5_with_3_4_7.md` (Paper II §3.4 canonical; §3.4.4 added June 3, 2026; §3.4.7 added June 28, 2026) as read in chat on September 20, 2026. Only §3.4.4 and §3.4.7 are extracted — the field content, the internal symmetry, the two-body kernel, the oriented term, and the O(16) accident are stated in these two subsections. The extract is the text of record the chat and CC instruments md5-guard; the author may diff it against the canonical file at any time (a mismatch is an H-item, not a silent correction). Author's answers of record applied on top of the extract (Q-A1-1: 16 real components, 8 complex amplitudes; the oriented term is NOT U(1)-phase-invariant. Q-A1-3: no term splits the real unit from Im 𝕆).

---

### 3.4.4 Internal symmetry and the locality of the vacuum action

The deficit-angle form of §3.4 captures the *spatial* (gravitational) sector of the substrate action. This subsection works the *internal* sector — where the order parameter carries octonion structure — using the complementary field-theoretic (Gross–Pitaevskii) representation, and asks a single question: where can the framework's specific Fano / PSL(2,7) content enter the action? The answer is a sharp locality result. The Fano content is invisible to the vacuum at every local order; it can live only on topological defects, as an orientation charge selecting Fano-line windings.

**The field representation.** Write the substrate order parameter as ψ ∈ ℂ⊗𝕆 — a U(1) superfluid phase times the eight octonion components (the real part e₀ and the seven imaginaries e₁…e₇ ↔ the seven Fano points). The continuous internal symmetry is G₂ = Aut(𝕆), the octonion automorphism group, acting irreducibly on Im(𝕆) ≅ ℝ⁷. Consistent with the Category Wall, the action's metric, scale, and sign are imports rather than combinatorial outputs: the candidate is the Gross–Pitaevskii / Bjerknes superfluid functional with a roton kernel, importing the field target (ℂ⊗𝕆), the kinetic form, and one scale.

**The two-body sector is Fano-blind.** Because the seven imaginary directions form the irreducible **7** of G₂, Schur's lemma forces the invariant symmetric two-tensor on ℝ⁷ to be unique — the metric. The symmetry-allowed two-body contact kernel is therefore a *single scalar*,

$$K_{ij}(r) = a(r)\,\delta_{ij},$$

with no room for Fano-line structure at two-body. (This corrects an earlier reading that used the PSL(2,7) *permutation* representation, in which ℝ⁷ ≅ **1** ⊕ **6** is reducible and admits two invariant tensors {I, J}; that is the wrong module — G₂ does not act on the seven imaginaries by permutations.) A roton — a negative lobe of Ũ(k) at finite k — is *permitted* through the radial profile a(r) but is not *forced* by symmetry; the profile is a metric-class import, exactly as in §3.4 and §2.2.

**How the Fano permutations are realized.** Of the 168 collineations of the Fano plane (the automorphism group of the bare incidence geometry, PSL(2,7) ≅ GL(3,2)), exactly 21 — the Frobenius subgroup F₂₁ = ℤ₇⋊ℤ₃ — lift to genuine octonion automorphisms as *unsigned* basis permutations; the remaining 147 do not respect the octonion sign rules. (All 168 lift once basis signs are allowed, generating an order-1344 signed-permutation automorphism group inside G₂.) Both G₂ and this realized finite group act irreducibly on the seven directions, so each yields the single-scalar kernel; F₂₁ on its own would leave a two-parameter kernel, since under F₂₁ the seven splits as **1** ⊕ **3** ⊕ **3̄** — so the single scalar is a property of the full continuous symmetry, not of the realized permutations alone. The incidence group PSL(2,7) enters the dynamics only combinatorially: it partitions the 35 three-element subsets of the seven directions into **7 collinear triples** (the Fano lines) and **28 non-collinear** ones — the classification probed at three-body order, where Fano structure first becomes possible.

**Where the Fano content can and cannot appear.** Two results complete the locality picture, both at the lowest order at which Fano structure could enter (the three-body, degree-six term):

1. **Symmetric channel — inert.** A density-product coupling summed over the seven Fano lines is dynamically inert: it leaves the uniform internal state a fixed point and supplies no symmetry-breaking gradient, because the lines form a balanced **2-(7,3,1) design** (every point on three lines, every pair on exactly one). Numerically, the per-site line-locking order parameter stays at its uniform baseline while a non-collinear control over-concentrates; the hexagonal (p6m) substrate lattice of §2.1 survives in both arms.

2. **Oriented channel — topological.** The coupling that carries the octonion *orientation* is built from the totally antisymmetric structure three-form φ_{abc} (the signs in e_i e_j = ±e_k). Contracted with a single bosonic field it vanishes identically — antisymmetric against the symmetric ψ_aψ_bψ_c — so the orientation is invisible to any local potential. The lowest non-vanishing orientation term,

$$O = \int \varphi_{abc}\,\psi_a\,\partial_x\psi_b\,\partial_y\psi_c\;d^2x,$$

is a total derivative: it is zero on the vacuum, on one-dimensional textures, and on *all smooth* two-dimensional textures. It becomes nonzero only on a **topological defect** (a skyrmion or vortex core), where it is orientation-odd and is nonzero **if and only if** the winding components form a Fano line.

**The locality result.** Taken together, the substrate vacuum is generic by necessity: the contact potential is forced to standard Gross–Pitaevskii, the symmetric Fano three-body term is symmetry-inert, and the oriented term is a topological total derivative. The framework-specific Fano / PSL(2,7) content cannot imprint on the vacuum at any local order — it lives entirely on topological defects (the cores of vortices and knotted solitons), where it is a topological orientation charge selecting Fano-line windings. This is the Category Wall expressing itself sector by sector: an imported orientation can attach only to topology.

**Forward prediction (the one concrete gate).** On the knotted-vortex (Császár-torus) soliton, classify the core by which octonion components wind. The framework predicts a nonzero orientation / Faddeev–Hopf linking charge **if and only if** those components form a Fano line — a Fano-line core confirms the orientation channel is physically realized; a non-line core is an informative null. This is the bridge from the present vacuum analysis to the soliton sector, and to the Borromean baryon construction. *(Tested in §3.4.5: the selection rule is confirmed on a charge-1 hopfion; the parity is found to be even, so the linking charge is chirality-blind — chirality is deferred to the triple-linking gate.)*

**Status and provenance.** The symmetry core (the G₂ / F₂₁ / signed-permutation structure and the single-scalar kernel) and the four sector computations are **Register 1**, reproduced independently in three computational environments; the candidate Gross–Pitaevskii action and the forward soliton gate are Register 2/3. The supporting computations and their register accounting are recorded in the SQT Master Ledger as **§3.4-SYM (V4.26)**, with provenance scripts `sym_core_verify_3_4.py` (symmetry core) and the four field-theoretic tools (`mv_g1_minimiser.py`, `g0_invariants.py`, `g1prime_fano3body.py`, `g1pp_orientation.py`). No observable bridge — mass, scale, or sign — is asserted here; this subsection locates the framework's dynamical fingerprint and constrains it to the defect sector, and does not advance the §3.4.1 promotion gate or the pulsation-ratio gate.

---

### 3.4.7 The selection rule on the fluctuation spectrum

§3.4.4 established that the framework's Fano content is invisible to the substrate vacuum at every local order and lives only on topological defect cores; §3.4.5 confirmed the resulting selection rule on the *static* φ-weighted linking charge Q_φ of a soliton. This subsection carries the same rule one level further — onto the *dynamical fluctuation spectrum* of the internal octonion directions around a defect core — and reports where that spectrum does and does not contain framework-independent content.

**The two-body internal sector is gapless.** Write the order parameter as ψ ∈ ℂ⊗𝕆 (§3.4.4). The symmetric two-body kernel is forced by Schur's lemma to the single scalar K_ij = a(r)δ_ij, so the contact interaction depends only on the total density ρ = |ψ|² = Σ_k|ψ_k|² and is accidentally invariant under the full O(16) acting on the sixteen real components — far larger than the physical ℂ⊗G₂ symmetry. The transverse (internal-direction) fluctuation operator is therefore L_⊥ = −½∇² + (U*ρ − μ) with no anomalous coupling, and the stationary Gross–Pitaevskii equation is precisely L_⊥ψ₀ = 0: the condensate is an exact zero mode of L_⊥, so the internal sector is gapless at the zone centre and carries no framework-specific structure at two-body order. This is the locality result of §3.4.4 re-expressed in the excitation spectrum — the vacuum's internal modes are featureless.

**The framework content enters only through the oriented three-body term on a defect core.** The accidental O(16) degeneracy is lifted only by the term that is not O(16)-invariant — the oriented three-form coupling O = ∫ φ_abc ψ_a ∂_x ψ_b ∂_y ψ_c of §3.4.4, a total derivative and so active only on a topological defect. Around a core whose internal winding lies in directions {a,b,c}, its contribution to the internal fluctuation operator is governed by the structure constant φ_abc: nonzero, and antisymmetric in the internal indices, when {a,b,c} is a Fano line; identically zero off a line. (The symmetric three-body term remains inert, as in §3.4.4.) Two consequences follow, both independent of the radial profile of the core. First, **the selection rule survives into the dynamical spectrum**: a Fano-line core lifts internal modes, a non-line core leaves them untouched — the §3.4.5 rule, now read off the excitations rather than a static charge. Second, **the lifted modes form a chiral pair**: an antisymmetric coupling on the three directions of a line has eigenstructure {0, ±iσ}, so the line carries one unaffected combination and a complex-conjugate (chiral) pair, with the splitting magnitude σ proportional to the oriented coupling strength. The seven internal directions organize as **1 ⊕ 3 ⊕ 3̄** under the realized F₂₁ ⊂ G₂ — the standard decomposition of the seven into the trivial plus a conjugate pair of triplets, whose 3/3̄ split is the quadratic-residue / non-residue partition of §§2.75–2.76.

**What the spectrum does and does not supply.** The selection rule and the multiplet structure are fixed by the octonion structure constants alone — framework-internal facts about which directions wind, carrying no scale. The *magnitude* of the chiral splitting, by contrast, is set by the oriented coupling and the core profile; it is a scale-dependent quantity of exactly the class the substrate action treats as an imported parameter, and it carries no scale-free pure number. The fluctuation spectrum of the internal sector therefore extends the framework's selection-rule ladder — vacuum-blind, defect-localized, Fano-line-selective, now in the excitations as well as the static charge — **without** supplying a parameter-free dynamical observable; the latter remains an imported scale, consistent with the substrate action's standing import structure. No observable bridge is asserted.

**Status and provenance.** The two-body gaplessness (an exact zero-mode identity), the Fano-line selectivity on the fluctuation spectrum, the 1 ⊕ 3 ⊕ 3̄ classification, and the two-chiral-mode count are **Register 1**, established by symmetry and verified independently in two computational environments; the chiral-splitting magnitude is an imported **Register 2** quantity. The supporting computations are recorded in the SQT Master Ledger as **Gate G-INT1 / §2.88.D.2 (V4.47)**, with the pre-registration `G_INT1_EXECUTION_PREREGISTRATION.md` and provenance scripts (first leg `gz1_core.py`-based; independent second leg `verify_gint1_secondleg.py`). This subsection extends the selection-rule ladder of §§3.4.4–3.4.6 into the excitation spectrum; it does **not** advance the load-bearing dynamical gates of the substrate action (the Bjerknes pulsation amplitude and the bilateral fold), which remain the §3.4 frontier.
=====END-EMBED name=inputs/paper_II_3_4_4_and_3_4_7_extract.md=====

=====BEGIN-EMBED name=g_2a_a1_chatleg.py md5=6360709d6a7eb5fc3df7fc8fd26dc36a bytes=53706 encoding=base64 armor_bytes=72551 QUARANTINED=====
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJnXzJhX2ExX2NoYXRsZWcucHkg4oCUIEdhdGUgRy0y
YS1BMSBjaGF0LWxlZyBpbnN0cnVtZW50IChQaGFzZXMgMCwgMSwgMWIsIDIsIDMpLgoKR3VhcmRz
IChmYWlsLWNsb3NlZCwgbm8gb3ZlcnJpZGUgZmxhZyk6IG1kNSBvZiB0aGUgbG9ja2VkIG1lbW8s
IHRoZSBnYXRlIFQxIGxpc3QsIHRoZSBhY3Rpb24tb2YtcmVjb3JkCmV4dHJhY3Q7IFQxIHNjYW4g
b2YgdGhpcyBmaWxlLCB0aGUgbWVtbyBhbmQgdGhlIGV4dHJhY3QgKHBhdHRlcm4taW5kZXgtb25s
eSByZXBvcnRpbmcpLiBELVQxIGlzIHJldGlyZWQuCgpFeGFjdCBhcml0aG1ldGljIChzeW1weSBy
YXRpb25hbHMgLyBGcmFjdGlvbnMgLyBpbnRlZ2VycykgZXZlcnl3aGVyZSBleGNlcHQgdGhlIHNw
aW5vcmlhbC0yTyBibG9jawooZmxvYXRzOyB0aHJlc2hvbGRlZCkgYW5kIHRoZSBudW1lcmljIGNy
b3NzLWNoZWNrIG9mIG9uZSBzeW1ib2xpYyBpbnRlZ3JhbC4gTm8gbGVkZ2VyIHZhbHVlLCBubwpv
YnNlcnZhdGlvbmFsIHRhcmdldCwgbm8gdmVyZGljdCB0ZXh0OiB0aGUgdmVyZGljdCBjbGFzcyBp
cyBhc3NlbWJsZWQgTEFTVCBmcm9tIHRoZSBlbmNvZGVkIGJvb2xlYW5zIGJ5CnRoZSBzY2hlbWEg
cnVsZSAodGhlIGNvbXBhcmF0b3IgcmVjb21wdXRlcyBpdCkuCgpVc2FnZTogcHl0aG9uMyBnXzJh
X2ExX2NoYXRsZWcucHkgcnVuIFstLW91dCBESVJdICAgICB8ICAgICBweXRob24zIGdfMmFfYTFf
Y2hhdGxlZy5weSBzZWxmdGVzdAoiIiIKaW1wb3J0IGhhc2hsaWIsIGpzb24sIG9zLCBzeXMsIHRp
bWUsIGl0ZXJ0b29scywgbWF0aApmcm9tIGZyYWN0aW9ucyBpbXBvcnQgRnJhY3Rpb24KCiMgLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0gZ3VhcmRzCk1FTU8gPSAic3RhZ2luZ19tZW1vX0dfMmFfQTFfdjIu
bWQiOyAgICAgIE1FTU9fTUQ1ID0gIjYyNmFhODY4ODQ0MjIwZWI2YzM4MDFlZjA3YTc3NzgzIgpU
MUxJU1QgPSAidG9vbHMvdDEvVDFfZm9yYmlkZGVuX0dfMmFfQTEudHh0IjsgVDFfTUQ1ID0gIjIw
MjZiNzgyZGIzOTA1ZDlmMmNlMzU3MzM4MjM2MThjIgpFWFRSQUNUID0gImlucHV0cy9wYXBlcl9J
SV8zXzRfNF9hbmRfM180XzdfZXh0cmFjdC5tZCI7IEVYVFJBQ1RfTUQ1ID0gIjk0MGIwYmVlNGIy
MTEyZTkxMWFlNzM4YzNkYjJiYzNkIgpMRURHRVJfQkFTRV9NRDUgPSAiNDAwMDllYzAxOTc4NzZi
MTMwNzY2ZjFhZTc0OTQzNjAiCkVMRUNUSU9OUyA9IHtmIkUtQTEte2l9IjogImEiIGZvciBpIGlu
IHJhbmdlKDEsIDkpfQpHQVRFID0gIkctMmEtQTEiCgpkZWYgbWQ1X2J5dGVzKGIpOiByZXR1cm4g
aGFzaGxpYi5tZDUoYikuaGV4ZGlnZXN0KCkKZGVmIG1kNV9maWxlKHApOiByZXR1cm4gbWQ1X2J5
dGVzKG9wZW4ocCwgInJiIikucmVhZCgpKQoKTlVNQ0hBUlMgPSBzZXQoIjAxMjM0NTY3ODkuZUUr
LcOXXiDigbvigbDCucKywrPigbTigbXigbbigbfigbjigbkiKQpkZWYgdDFfbG9hZChwYXRoKToK
ICAgIHJldHVybiBbbC5yc3RyaXAoIlxuIikgZm9yIGwgaW4gb3BlbihwYXRoLCBlbmNvZGluZz0i
dXRmLTgiKSBpZiBsLnN0cmlwKCkgYW5kIG5vdCBsLnN0YXJ0c3dpdGgoIiMiKV0KZGVmIHQxX2lz
X251bWVyaWMocCk6IHJldHVybiBhbGwoYyBpbiBOVU1DSEFSUyBmb3IgYyBpbiBwKQpkZWYgdDFf
c2Nhbl90ZXh0KHRleHQsIHBhdHMpOgogICAgaGl0cywgY29sbCA9IFtdLCBbXQogICAgZm9yIGks
IHAgaW4gZW51bWVyYXRlKHBhdHMpOgogICAgICAgIHMgPSAwCiAgICAgICAgd2hpbGUgVHJ1ZToK
ICAgICAgICAgICAgaiA9IHRleHQuZmluZChwLCBzKQogICAgICAgICAgICBpZiBqIDwgMDogYnJl
YWsKICAgICAgICAgICAgaWYgdDFfaXNfbnVtZXJpYyhwKToKICAgICAgICAgICAgICAgIGEgPSBq
CiAgICAgICAgICAgICAgICB3aGlsZSBhID4gMCBhbmQgdGV4dFthLTFdIGluIE5VTUNIQVJTIGFu
ZCB0ZXh0W2EtMV0gIT0gIiAiOiBhIC09IDEKICAgICAgICAgICAgICAgIGIgPSBqICsgbGVuKHAp
CiAgICAgICAgICAgICAgICB3aGlsZSBiIDwgbGVuKHRleHQpIGFuZCB0ZXh0W2JdIGluIE5VTUNI
QVJTIGFuZCB0ZXh0W2JdICE9ICIgIjogYiArPSAxCiAgICAgICAgICAgICAgICAoaGl0cyBpZiB0
ZXh0W2E6Yl0gPT0gcCBlbHNlIGNvbGwpLmFwcGVuZCgoaSwgaikpCiAgICAgICAgICAgIGVsc2U6
CiAgICAgICAgICAgICAgICBoaXRzLmFwcGVuZCgoaSwgaikpCiAgICAgICAgICAgIHMgPSBqICsg
MQogICAgcmV0dXJuIGhpdHMsIGNvbGwKCmRlZiBndWFyZHMoKToKICAgIGxvZyA9IFtdCiAgICBm
b3IgcGF0aCwgd2FudCBpbiAoKE1FTU8sIE1FTU9fTUQ1KSwgKFQxTElTVCwgVDFfTUQ1KSwgKEVY
VFJBQ1QsIEVYVFJBQ1RfTUQ1KSk6CiAgICAgICAgaWYgbm90IG9zLnBhdGguZXhpc3RzKHBhdGgp
OiByYWlzZSBTeXN0ZW1FeGl0KGYiSEFMVDogbWlzc2luZyB7cGF0aH0iKQogICAgICAgIGggPSBt
ZDVfZmlsZShwYXRoKQogICAgICAgIGlmIGggIT0gd2FudDogcmFpc2UgU3lzdGVtRXhpdChmIkhB
TFQ6IG1kNSBtaXNtYXRjaCBmb3Ige3BhdGh9OiB7aH0gIT0ge3dhbnR9IikKICAgICAgICBsb2cu
YXBwZW5kKGYiZ3VhcmQgbWQ1IE9LIHtwYXRofSB7aH0iKQogICAgcGF0cyA9IHQxX2xvYWQoVDFM
SVNUKQogICAgaWYgbGVuKHBhdHMpICE9IDI0OiByYWlzZSBTeXN0ZW1FeGl0KGYiSEFMVDogVDEg
bGlzdCBoYXMge2xlbihwYXRzKX0gcGF0dGVybnMsIGV4cGVjdGVkIDI0IikKICAgIHNjYW4gPSB7
fQogICAgZm9yIG5hbWUsIHBhdGggaW4gKCgiaW5zdHJ1bWVudCIsIG9zLnBhdGguYWJzcGF0aChf
X2ZpbGVfXykpLCAoIm1lbW8iLCBNRU1PKSwgKCJleHRyYWN0IiwgRVhUUkFDVCkpOgogICAgICAg
IHRleHQgPSBvcGVuKHBhdGgsICJyYiIpLnJlYWQoKS5kZWNvZGUoInV0Zi04IiwgInJlcGxhY2Ui
KQogICAgICAgIGhpdHMsIGNvbGwgPSB0MV9zY2FuX3RleHQodGV4dCwgcGF0cykKICAgICAgICBp
ZiBoaXRzOiByYWlzZSBTeXN0ZW1FeGl0KGYiSEFMVDogVDEgaGl0IGluIHtuYW1lfTogcGF0dGVy
biBpbmRpY2VzIHtzb3J0ZWQoc2V0KGkgZm9yIGksXyBpbiBoaXRzKSl9IikKICAgICAgICBzY2Fu
W25hbWVdID0gIkNMRUFOIjsgbG9nLmFwcGVuZChmIlQxIHtuYW1lfTogQ0xFQU4gKG51bWVyaWMg
Y29sbGlzaW9ucyB7bGVuKGNvbGwpfSkiKQogICAgcmV0dXJuIHNjYW4sIGxvZwoKIyAtLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLSBvY3RvbmlvbnMgKGV4YWN0KQppbXBvcnQgc3ltcHkgYXMgc3AKTElORVMg
PSBbKChpLTEpICUgNyArIDEsIGkgJSA3ICsgMSwgKGkrMikgJSA3ICsgMSkgZm9yIGkgaW4gcmFu
Z2UoMSwgOCldICAgIyAoMSwyLDQpLCgyLDMsNSksLi4uLCg3LDEsMykKTElORVNFVFMgPSB7ZnJv
emVuc2V0KGwpIGZvciBsIGluIExJTkVTfQpNVUxUID0ge30KZm9yIChhLCBiLCBjKSBpbiBMSU5F
UzoKICAgIGZvciAoeCwgeSwgeikgaW4gKChhLCBiLCBjKSwgKGIsIGMsIGEpLCAoYywgYSwgYikp
OgogICAgICAgIE1VTFRbKHgsIHkpXSA9ICgxLCB6KTsgTVVMVFsoeSwgeCldID0gKC0xLCB6KQpk
ZWYgcGhpKGEsIGIsIGMpOgogICAgIiIic3RydWN0dXJlIGNvbnN0YW50IHBoaV9hYmMgZm9yIGlt
YWdpbmFyeSBpbmRpY2VzIDEuLjcgKDAgb2ZmIGxpbmVzKS4iIiIKICAgIGlmIGxlbih7YSwgYiwg
Y30pIDwgMyBvciBmcm96ZW5zZXQoKGEsIGIsIGMpKSBub3QgaW4gTElORVNFVFM6IHJldHVybiAw
CiAgICBzLCBrID0gTVVMVFsoYSwgYildCiAgICByZXR1cm4gcyBpZiBrID09IGMgZWxzZSAtcwpk
ZWYgb211bChwLCBxKToKICAgIHIgPSBbc3AuSW50ZWdlcigwKV0gKiA4CiAgICBmb3IgaSBpbiBy
YW5nZSg4KToKICAgICAgICBpZiBwW2ldID09IDA6IGNvbnRpbnVlCiAgICAgICAgZm9yIGogaW4g
cmFuZ2UoOCk6CiAgICAgICAgICAgIGlmIHFbal0gPT0gMDogY29udGludWUKICAgICAgICAgICAg
aWYgaSA9PSAwOiByW2pdICs9IHBbaV0gKiBxW2pdCiAgICAgICAgICAgIGVsaWYgaiA9PSAwOiBy
W2ldICs9IHBbaV0gKiBxW2pdCiAgICAgICAgICAgIGVsaWYgaSA9PSBqOiByWzBdIC09IHBbaV0g
KiBxW2pdCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBzLCBrID0gTVVMVFsoaSwg
aildOyByW2tdICs9IHMgKiBwW2ldICogcVtqXQogICAgcmV0dXJuIHIKZGVmIHVuaXQoaSk6CiAg
ICB2ID0gW3NwLkludGVnZXIoMCldICogODsgdltpXSA9IHNwLkludGVnZXIoMSk7IHJldHVybiB2
CmRlZiBMbWF0KGEpOgogICAgTSA9IHNwLnplcm9zKDgsIDgpCiAgICBmb3IgaiBpbiByYW5nZSg4
KToKICAgICAgICBjb2wgPSBvbXVsKHVuaXQoYSksIHVuaXQoaikpCiAgICAgICAgZm9yIGkgaW4g
cmFuZ2UoOCk6IE1baSwgal0gPSBjb2xbaV0KICAgIHJldHVybiBNCmRlZiBpc19hdXQoUCwgdG9s
PU5vbmUpOgogICAgIiIiZXhhY3QgYXV0b21vcnBoaXNtIHRlc3Qgb2YgYW4gOHg4IHN5bXB5IG1h
dHJpeCAocmF0aW9uYWwvYWxnZWJyYWljIGVudHJpZXMpLiIiIgogICAgZm9yIGkgaW4gcmFuZ2Uo
OCk6CiAgICAgICAgZm9yIGogaW4gcmFuZ2UoOCk6CiAgICAgICAgICAgIGxocyA9IFAgKiBzcC5N
YXRyaXgob211bCh1bml0KGkpLCB1bml0KGopKSkKICAgICAgICAgICAgUGkgPSBbUFtrLCBpXSBm
b3IgayBpbiByYW5nZSg4KV07IFBqID0gW1Bbaywgal0gZm9yIGsgaW4gcmFuZ2UoOCldCiAgICAg
ICAgICAgIHJocyA9IHNwLk1hdHJpeChvbXVsKFBpLCBQaikpCiAgICAgICAgICAgIGQgPSAobGhz
IC0gcmhzKS5hcHBseWZ1bmMoc3AubnNpbXBsaWZ5KSBpZiB0b2wgaXMgTm9uZSBlbHNlIChsaHMg
LSByaHMpCiAgICAgICAgICAgIGlmIGFueShzcC5zaW1wbGlmeSh4KSAhPSAwIGZvciB4IGluIGQp
OiByZXR1cm4gRmFsc2UKICAgIHJldHVybiBUcnVlCmRlZiBhdXRfZGVmZWN0X2Zsb2F0KFApOgog
ICAgIiIibWF4X3tpLGp9IHxQKGVfaSBlX2opIC0gUChlX2kpUChlX2opfCBmb3IgYSByZWFsIDh4
OCBudW1weSBtYXRyaXguIiIiCiAgICBpbXBvcnQgbnVtcHkgYXMgbnAKICAgIGQgPSAwLjAKICAg
IGZvciBpIGluIHJhbmdlKDgpOgogICAgICAgIGZvciBqIGluIHJhbmdlKDgpOgogICAgICAgICAg
ICBsaHMgPSBQIEAgbnAuYXJyYXkoW2Zsb2F0KHgpIGZvciB4IGluIG9tdWwodW5pdChpKSwgdW5p
dChqKSldKQogICAgICAgICAgICBQaSA9IFtzcC5GbG9hdChQW2ssIGldKSBmb3IgayBpbiByYW5n
ZSg4KV07IFBqID0gW3NwLkZsb2F0KFBbaywgal0pIGZvciBrIGluIHJhbmdlKDgpXQogICAgICAg
ICAgICByaHMgPSBucC5hcnJheShbZmxvYXQoeCkgZm9yIHggaW4gb211bChQaSwgUGopXSkKICAg
ICAgICAgICAgZCA9IG1heChkLCBmbG9hdChucC5tYXgobnAuYWJzKGxocyAtIHJocykpKSkKICAg
IHJldHVybiBkCmRlZiBzcGFuX2RpbShtYXRzKTogcmV0dXJuIHNwLk1hdHJpeChbbGlzdChNKSBm
b3IgTSBpbiBtYXRzXSkucmFuaygpCgpkZWYgZGVyaXZhdGlvbl9hbGdlYnJhKCk6CiAgICAiIiJn
MiA9IERlcihPKSBhcyA3eDcgYW50aXN5bW1ldHJpYyBtYXRyaWNlcyBvbiBJbSBPIChleGFjdCBu
dWxsc3BhY2UpOyByZXR1cm5zIGxpc3Qgb2YgMTQgc3ltcHkgN3g3LiIiIgogICAgc3ltcyA9IHNw
LnN5bWJvbHMoJ2QwOjIxJyk7IEQgPSBzcC56ZXJvcyg3LCA3KTsgdCA9IDAKICAgIGZvciBpIGlu
IHJhbmdlKDcpOgogICAgICAgIGZvciBqIGluIHJhbmdlKGkrMSwgNyk6CiAgICAgICAgICAgIERb
aSwgal0gPSBzeW1zW3RdOyBEW2osIGldID0gLXN5bXNbdF07IHQgKz0gMQogICAgZGVmIERhcHBs
eSh2KToKICAgICAgICBvdXQgPSBbc3AuSW50ZWdlcigwKV0gKiA4CiAgICAgICAgZm9yIGkgaW4g
cmFuZ2UoMSwgOCk6CiAgICAgICAgICAgIGlmIHZbaV0gIT0gMDoKICAgICAgICAgICAgICAgIGZv
ciBqIGluIHJhbmdlKDEsIDgpOiBvdXRbal0gKz0gRFtqLTEsIGktMV0gKiB2W2ldCiAgICAgICAg
cmV0dXJuIG91dAogICAgZXFzID0gW10KICAgIGZvciBpIGluIHJhbmdlKDEsIDgpOgogICAgICAg
IGZvciBqIGluIHJhbmdlKDEsIDgpOgogICAgICAgICAgICBlaSwgZWogPSB1bml0KGkpLCB1bml0
KGopCiAgICAgICAgICAgIGxocyA9IERhcHBseShvbXVsKGVpLCBlaikpCiAgICAgICAgICAgIHJo
cyA9IFtzcC5JbnRlZ2VyKDApXSAqIDgKICAgICAgICAgICAgZm9yIG0gaW4gcmFuZ2UoMSwgOCk6
CiAgICAgICAgICAgICAgICBpZiBEW20tMSwgaS0xXSAhPSAwOgogICAgICAgICAgICAgICAgICAg
IHByb2QgPSBvbXVsKHVuaXQobSksIGVqKQogICAgICAgICAgICAgICAgICAgIGZvciBuIGluIHJh
bmdlKDgpOiByaHNbbl0gKz0gRFttLTEsIGktMV0gKiBwcm9kW25dCiAgICAgICAgICAgICAgICBp
ZiBEW20tMSwgai0xXSAhPSAwOgogICAgICAgICAgICAgICAgICAgIHByb2QgPSBvbXVsKGVpLCB1
bml0KG0pKQogICAgICAgICAgICAgICAgICAgIGZvciBuIGluIHJhbmdlKDgpOiByaHNbbl0gKz0g
RFttLTEsIGotMV0gKiBwcm9kW25dCiAgICAgICAgICAgIGZvciBuIGluIHJhbmdlKDgpOgogICAg
ICAgICAgICAgICAgZSA9IHNwLmV4cGFuZChsaHNbbl0gLSByaHNbbl0pCiAgICAgICAgICAgICAg
ICBpZiBlICE9IDA6IGVxcy5hcHBlbmQoZSkKICAgIEEgPSBzcC5NYXRyaXgoW1tzcC5Qb2x5KGUs
ICpzeW1zKS5jb2VmZl9tb25vbWlhbChzKSBmb3IgcyBpbiBzeW1zXSBmb3IgZSBpbiBlcXNdKQog
ICAgbnMgPSBBLm51bGxzcGFjZSgpCiAgICBnMiA9IFtdCiAgICBmb3IgdiBpbiBuczoKICAgICAg
ICBNID0gc3AuemVyb3MoNywgNyk7IHQgPSAwCiAgICAgICAgZm9yIGkgaW4gcmFuZ2UoNyk6CiAg
ICAgICAgICAgIGZvciBqIGluIHJhbmdlKGkrMSwgNyk6CiAgICAgICAgICAgICAgICBNW2ksIGpd
ID0gdlt0XTsgTVtqLCBpXSA9IC12W3RdOyB0ICs9IDEKICAgICAgICBnMi5hcHBlbmQoTSkKICAg
IHJldHVybiBnMgpkZWYgdG84KE03KToKICAgIE04ID0gc3AuemVyb3MoOCwgOCk7IE04WzE6LCAx
Ol0gPSBNNzsgcmV0dXJuIE04CgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIFBoYXNlIDAKZGVmIHBo
YXNlMChnMiwgZXh0cmFjdF90ZXh0KToKICAgIFAgPSB7fQogICAgIyAoMGEpIGZpZWxkIGNvbnRl
bnQgb2YgcmVjb3JkIChkb2N1bWVudGFyeSBhc3NlcnRzIG9uIHRoZSBleHRyYWN0ICsgdGhlIGF1
dGhvcidzIGFuc3dlcnMgaW4gaXRzIGhlYWRlcikKICAgIGFzc2VydCAic2l4dGVlbiByZWFsIGNv
bXBvbmVudHMiIGluIGV4dHJhY3RfdGV4dCBhbmQgIjE2IHJlYWwgY29tcG9uZW50cyIgaW4gZXh0
cmFjdF90ZXh0IGFuZCAiOCBjb21wbGV4IGFtcGxpdHVkZXMiIGluIGV4dHJhY3RfdGV4dAogICAg
YXNzZXJ0ICJzcGlub3IgaW5kZXgiIG5vdCBpbiBleHRyYWN0X3RleHQuc3BsaXQoIiMjIyAzLjQu
NCIpWzFdICAgIyBubyBzcGlub3IgaW5kZXggaW4gdGhlIGZpZWxkIGNvbnRlbnQgb2YgcmVjb3Jk
CiAgICBQWyJmaWVsZF9yZWFsX2NvbXBvbmVudHMiXSA9IDE2OyBQWyJjb21wbGV4X2FtcGxpdHVk
ZXMiXSA9IDg7IFBbInNwaW5vcl9pbmRleF9wcmVzZW50Il0gPSBGYWxzZQogICAgIyAoMGMpIHNw
YXRpYWwtaW50ZXJuYWwgZGlyZWN0IHByb2R1Y3Q6IHRoZSB0ZXJtIGxpc3Qgb2YgcmVjb3JkIChm
cm9tIHRoZSBleHRyYWN0KSDigJQgZXZlcnkgdGVybSdzIGluZGV4CiAgICAjIHN0cnVjdHVyZSBm
YWN0b3JpemVzOiBpbnRlcm5hbCBpbmRpY2VzIG9ubHkgdmlhIGRlbHRhX2FiIC8gcGhpX2FiYywg
c3BhdGlhbCBvbmx5IHZpYSBkX3gsIGRfeS4KICAgIGFzc2VydCAiz4Zfe2FiY31cXCxcXHBzaV9h
XFwsXFxwYXJ0aWFsX3hcXHBzaV9iXFwsXFxwYXJ0aWFsX3lcXHBzaV9jIiBpbiBleHRyYWN0X3Rl
eHQgb3IgIs+GX2FiYyDPiF9hIOKIgl94IM+IX2Ig4oiCX3kgz4hfYyIgaW4gZXh0cmFjdF90ZXh0
CiAgICBhc3NlcnQgIktfe2lqfShyKSA9IGEocilcXCxcXGRlbHRhX3tpan0iIGluIGV4dHJhY3Rf
dGV4dAogICAgdGVybXMgPSBbeyJ0ZXJtIjogInR3by1ib2R5IGNvbnRhY3QiLCAiaW50ZXJuYWwi
OiAiZGVsdGFfYWIgKHNpbmdsZSBzY2FsYXIpIiwgInNwYXRpYWwiOiAibm9uZSJ9LAogICAgICAg
ICAgICAgeyJ0ZXJtIjogIkdQIGtpbmV0aWMgKEkyKSIsICJpbnRlcm5hbCI6ICJkZWx0YV9hYiIs
ICJzcGF0aWFsIjogImRfaSAuIGRfaSJ9LAogICAgICAgICAgICAgeyJ0ZXJtIjogIm9yaWVudGVk
IE8iLCAiaW50ZXJuYWwiOiAicGhpX2FiYyIsICJzcGF0aWFsIjogImVwc194eSBkX3ggZF95In1d
CiAgICBmb3IgdCBpbiB0ZXJtczogdFsibWl4ZWRfc3BhdGlhbF9pbnRlcm5hbF90ZW5zb3IiXSA9
IEZhbHNlICAgIyBubyB0ZXJtIG9mIHJlY29yZCBjb3VwbGVzIGEgc3BhdGlhbCBpbmRleCB0byBh
biBpbnRlcm5hbCBpbmRleAogICAgUFsic3BhdGlhbF9pbnRlcm5hbF9kaXJlY3RfcHJvZHVjdCJd
ID0gYWxsKHRbIm1peGVkX3NwYXRpYWxfaW50ZXJuYWxfdGVuc29yIl0gaXMgRmFsc2UgZm9yIHQg
aW4gdGVybXMpCiAgICBQWyJfdGVybXNfb2ZfcmVjb3JkIl0gPSB0ZXJtcwogICAgIyAoMGIpIFN5
bV9pbnQ6IHRoZSBzdGFiaWxpemVyIG9mIHRoZSBPIGRlbnNpdHkgaW5zaWRlIHNvKDE2KS4gVCh1
LHYsdykgPSBwaGlfYWJjIHVfYSB2X2Igd19jLCBjb21wbGV4LXRyaWxpbmVhciBvbiBDXjguCiAg
ICAjIFJlYWwgY29vcmRpbmF0ZXM6IGNvbXBvbmVudCBhIChhPTAuLjcpID0geF9hICsgaSB5X2Eg
IC0+IGluZGV4IGEgKHJlYWwgcGFydCksIDgrYSAoaW1hZyBwYXJ0KS4KICAgICMgQnVpbGQgdGhl
IDgxOTIgeCAxMjAgaW50ZWdlciBtYXRyaXggb2YgdGhlIGxpbmVhciBtYXAgWCAtPiBbICh1LHYs
dykgLT4gVChYdSx2LHcpK1QodSxYdix3KStUKHUsdixYdykgXSBvdmVyIHJlYWwgYmFzaXMgdHJp
cGxlcywKICAgICMgdGhlbiB0aGUga2VybmVsIHZpYSB0aGUgR3JhbSBtYXRyaXggQV5UIEEgKGV4
YWN0KS4KICAgIGltcG9ydCBudW1weSBhcyBucAogICAgZGVmIFRfY29tcGxleCh1LCB2LCB3KTog
ICAjIHUsdix3OiBsZW5ndGgtMTYgZXhhY3QgKEZyYWN0aW9uL2ludC9zeW1weSkgcmVhbCB2ZWN0
b3JzIC0+IGNvbXBsZXggdmFsdWUgKHJlLCBpbSkgZXhhY3QKICAgICAgICByZSA9IDA7IGltID0g
MAogICAgICAgIGZvciAoYSwgYiwgYykgaW4gTElORVM6CiAgICAgICAgICAgIGZvciAoeCwgeSwg
eikgaW4gKChhLCBiLCBjKSwgKGIsIGMsIGEpLCAoYywgYSwgYikpOgogICAgICAgICAgICAgICAg
Zm9yIChwLCBxLCByLCBzKSBpbiAoKHgsIHksIHosIDEpLCAoeSwgeCwgeiwgLTEpKToKICAgICAg
ICAgICAgICAgICAgICB1ciwgdWkgPSB1W3BdLCB1WzgrcF07IHZyLCB2aSA9IHZbcV0sIHZbOCtx
XTsgd3IsIHdpID0gd1tyXSwgd1s4K3JdCiAgICAgICAgICAgICAgICAgICAgcHIgPSB1cip2ciAt
IHVpKnZpOyBwaV8gPSB1cip2aSArIHVpKnZyCiAgICAgICAgICAgICAgICAgICAgcmUgKz0gcyAq
IChwcip3ciAtIHBpXyp3aSk7IGltICs9IHMgKiAocHIqd2kgKyBwaV8qd3IpCiAgICAgICAgcmV0
dXJuIHJlLCBpbQogICAgaWR4ID0gWyhpLCBqKSBmb3IgaSBpbiByYW5nZSgxNikgZm9yIGogaW4g
cmFuZ2UoaSsxLCAxNildCiAgICBiYXNpcyA9IFtbMSBpZiB0ID09IGsgZWxzZSAwIGZvciB0IGlu
IHJhbmdlKDE2KV0gZm9yIGsgaW4gcmFuZ2UoMTYpXQogICAgVGIgPSB7fQogICAgZm9yIGsgaW4g
cmFuZ2UoMTYpOgogICAgICAgIGZvciBsIGluIHJhbmdlKDE2KToKICAgICAgICAgICAgZm9yIG0g
aW4gcmFuZ2UoMTYpOgogICAgICAgICAgICAgICAgVGJbKGssIGwsIG0pXSA9IFRfY29tcGxleChi
YXNpc1trXSwgYmFzaXNbbF0sIGJhc2lzW21dKQogICAgbmNvbHMgPSBsZW4oaWR4KQogICAgQSA9
IG5wLnplcm9zKCgyICogMTYqKjMsIG5jb2xzKSwgZHR5cGU9bnAuaW50NjQpCiAgICBmb3IgZywg
KGksIGopIGluIGVudW1lcmF0ZShpZHgpOgogICAgICAgIGFjdCA9IHtqOiAoaSwgMSksIGk6IChq
LCAtMSl9ICAgIyBYID0gRV9paiAtIEVfamk6IFggZV9qID0gZV9pLCBYIGVfaSA9IC1lX2oKICAg
ICAgICBmb3IgKGssIGwsIG0pIGluIGl0ZXJ0b29scy5wcm9kdWN0KHJhbmdlKDE2KSwgcmVwZWF0
PTMpOgogICAgICAgICAgICB2ciA9IDA7IHZpID0gMAogICAgICAgICAgICBpZiBrIGluIGFjdDoK
ICAgICAgICAgICAgICAgIGkyLCBzZyA9IGFjdFtrXTsgcl8sIGlfID0gVGJbKGkyLCBsLCBtKV07
IHZyICs9IHNnKnJfOyB2aSArPSBzZyppXwogICAgICAgICAgICBpZiBsIGluIGFjdDoKICAgICAg
ICAgICAgICAgIGkyLCBzZyA9IGFjdFtsXTsgcl8sIGlfID0gVGJbKGssIGkyLCBtKV07IHZyICs9
IHNnKnJfOyB2aSArPSBzZyppXwogICAgICAgICAgICBpZiBtIGluIGFjdDoKICAgICAgICAgICAg
ICAgIGkyLCBzZyA9IGFjdFttXTsgcl8sIGlfID0gVGJbKGssIGwsIGkyKV07IHZyICs9IHNnKnJf
OyB2aSArPSBzZyppXwogICAgICAgICAgICByb3cgPSBrKjI1NiArIGwqMTYgKyBtCiAgICAgICAg
ICAgIEFbcm93LCBnXSA9IHZyOyBBWzQwOTYgKyByb3csIGddID0gdmkKICAgIEcgPSAoQS5UIEAg
QSkKICAgIEdzID0gc3AuTWF0cml4KEcudG9saXN0KCkpCiAgICBrZXIgPSBHcy5udWxsc3BhY2Uo
KQogICAgUFsic3ltX2ludF9jb250aW51b3VzX2RpbSJdID0gbGVuKGtlcikKICAgIFBbInN5bV9p
bnRfY29udGludW91cyJdID0gIkcyIiBpZiBsZW4oa2VyKSA9PSAxNCBlbHNlICgiRzJ4VTFfcHNp
MCIgaWYgbGVuKGtlcikgPT0gMTUgZWxzZSBmImRpbXtsZW4oa2VyKX0iKQogICAgZGVmIHZlY19v
ZihYKToKICAgICAgICByZXR1cm4gbnAuYXJyYXkoW2ludChYW2ksIGpdKSBmb3IgKGksIGopIGlu
IGlkeF0sIGR0eXBlPW5wLmludDY0KQogICAgZGVmIGluX2tlcm5lbChYKToKICAgICAgICByZXR1
cm4gbm90IG5wLmFueShBIEAgdmVjX29mKFgpKQogICAgZGVmIFhfZnJvbV9nMihENyk6CiAgICAg
ICAgWCA9IHNwLnplcm9zKDE2LCAxNik7IFhbMTo4LCAxOjhdID0gRDc7IFhbOToxNiwgOToxNl0g
PSBENzsgcmV0dXJuIFgKICAgIFBbImcyX3ByZXNlcnZlc19PIl0gPSBhbGwoaW5fa2VybmVsKFhf
ZnJvbV9nMihEKSkgZm9yIEQgaW4gZzIpCiAgICAjIHRoZSBkZWNvdXBsZWQgcmVhbC11bml0IHBo
YXNlOiByb3RhdGlvbiBSZSBwc2lfMCA8LT4gSW0gcHNpXzAgKGluZGljZXMgMCBhbmQgOCkgcHJl
c2VydmVzIE8gKE8gaW52b2x2ZXMgaW1hZ2luYXJ5IGNvbXBvbmVudHMgb25seSkKICAgIFgwID0g
c3AuemVyb3MoMTYsIDE2KTsgWDBbMCwgOF0gPSAtMTsgWDBbOCwgMF0gPSAxCiAgICBQWyJfcHNp
MF9waGFzZV9wcmVzZXJ2ZXNfTyJdID0gYm9vbChpbl9rZXJuZWwoWDApKQogICAgIyBpbWFnaW5h
cnktc2VjdG9yIHN0YWJpbGl6ZXI6IHJlc3RyaWN0IHRvIHNvKDE0KSBvbiBpbmRpY2VzIHsxLi43
LCA5Li4xNX0KICAgIGtlZXAgPSBbZyBmb3IgZywgKGksIGopIGluIGVudW1lcmF0ZShpZHgpIGlm
IGkgbm90IGluICgwLCA4KSBhbmQgaiBub3QgaW4gKDAsIDgpXQogICAgR2sgPSBzcC5NYXRyaXgo
R1tucC5peF8oa2VlcCwga2VlcCldLnRvbGlzdCgpKQogICAgUFsiX2ltYWdfc2VjdG9yX2NvbnRp
bnVvdXNfZGltIl0gPSBsZW4oR2subnVsbHNwYWNlKCkpCiAgICAjIGdlbmVyaWMgc28oMTYpIGVs
ZW1lbnQgYnJlYWtzIE86IHJvdGF0aW9uIG1peGluZyBSZSBwc2lfMSB3aXRoIEltIHBzaV8yIChp
bmRpY2VzIDEgYW5kIDEwKQogICAgWGcgPSBzcC56ZXJvcygxNiwgMTYpOyBYZ1sxLCAxMF0gPSAx
OyBYZ1sxMCwgMV0gPSAtMQogICAgZGVmZWN0ID0gQSBAIHZlY19vZihYZyk7IG1hcmdpbiA9IGlu
dChucC5tYXgobnAuYWJzKGRlZmVjdCkpKQogICAgUFsiZ2VuZXJpY19zbzE2X2JyZWFrc19PIl0g
PSBtYXJnaW4gPiAwCiAgICBKbSA9IHNwLnplcm9zKDE2LCAxNikKICAgIGZvciBhIGluIHJhbmdl
KDgpOiBKbVs4K2EsIGFdID0gMTsgSm1bYSwgOCthXSA9IC0xCiAgICBQWyJPX3BoYXNlX2ludmFy
aWFudCJdID0gYm9vbChpbl9rZXJuZWwoSm0pKQogICAgdSA9IFtzcC5SYXRpb25hbChpKzEsIDMp
IGZvciBpIGluIHJhbmdlKDE2KV07IHYgPSBbc3AuUmF0aW9uYWwoMippLTUsIDcpIGZvciBpIGlu
IHJhbmdlKDE2KV07IHcgPSBbc3AuUmF0aW9uYWwoMyppKzEsIDUpIGZvciBpIGluIHJhbmdlKDE2
KV0KICAgIGRlZiBwaGFzZSh2ZWMxNiwgY3IsIGNpKToKICAgICAgICBvdXQgPSBbc3AuSW50ZWdl
cigwKV0gKiAxNgogICAgICAgIGZvciBhIGluIHJhbmdlKDgpOgogICAgICAgICAgICB4ciwgeGkg
PSB2ZWMxNlthXSwgdmVjMTZbOCthXTsgb3V0W2FdID0gY3IqeHIgLSBjaSp4aTsgb3V0WzgrYV0g
PSBjcip4aSArIGNpKnhyCiAgICAgICAgcmV0dXJuIG91dAogICAgdDAgPSBUX2NvbXBsZXgodSwg
diwgdykKICAgIHMzID0gc3Auc3FydCgzKS8yCiAgICB0MSA9IFRfY29tcGxleChwaGFzZSh1LCBz
cC5SYXRpb25hbCgtMSwgMiksIHMzKSwgcGhhc2Uodiwgc3AuUmF0aW9uYWwoLTEsIDIpLCBzMyks
IHBoYXNlKHcsIHNwLlJhdGlvbmFsKC0xLCAyKSwgczMpKQogICAgYXNzZXJ0IHNwLnNpbXBsaWZ5
KHQxWzBdIC0gdDBbMF0pID09IDAgYW5kIHNwLnNpbXBsaWZ5KHQxWzFdIC0gdDBbMV0pID09IDAK
ICAgIHRpID0gVF9jb21wbGV4KHBoYXNlKHUsIDAsIDEpLCBwaGFzZSh2LCAwLCAxKSwgcGhhc2Uo
dywgMCwgMSkpICAgIyBpXjMgPSAtaQogICAgYXNzZXJ0IHNwLnNpbXBsaWZ5KHRpWzBdIC0gdDBb
MV0pID09IDAgYW5kIHNwLnNpbXBsaWZ5KHRpWzFdICsgdDBbMF0pID09IDAKICAgIFBbInBoYXNl
X3N1Ymdyb3VwX29yZGVyIl0gPSAzCiAgICBjb25qID0gbGFtYmRhIHg6IHhbOjhdICsgWy15IGZv
ciB5IGluIHhbODpdXQogICAgdGMgPSBUX2NvbXBsZXgoY29uaih1KSwgY29uaih2KSwgY29uaih3
KSkKICAgIFBbImNvbmp1Z2F0aW9uX21hcHNfT190b19jb25qdWdhdGUiXSA9IGJvb2wodGNbMF0g
PT0gdDBbMF0gYW5kIHRjWzFdID09IC10MFsxXSkKICAgICMgU3ltX2ludCBpcyBwaW5uZWQgd2hl
biBpdHMgY29udGludW91cyBwYXJ0IGlzIGZ1bGx5IGlkZW50aWZpZWQ6IGcyIG9uIHRoZSBpbWFn
aW5hcnkgc2VjdG9yIChkaW0gMTQgdGhlcmUpIHBsdXMsIGlmIHByZXNlbnQsCiAgICAjIHRoZSBk
ZWNvdXBsZWQgcmVhbC11bml0IHBoYXNlIHUoMSlfcHNpMCAoZGltIDE1IHRvdGFsKSwgYW5kIG5v
dGhpbmcgZWxzZS4KICAgIFBbInN5bV9pbnRfcGlubmVkIl0gPSBib29sKFBbImcyX3ByZXNlcnZl
c19PIl0gYW5kIFBbImdlbmVyaWNfc28xNl9icmVha3NfTyJdIGFuZCBQWyJfaW1hZ19zZWN0b3Jf
Y29udGludW91c19kaW0iXSA9PSAxNAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYW5k
IFBbInN5bV9pbnRfY29udGludW91c19kaW0iXSA9PSAxNCArICgxIGlmIFBbIl9wc2kwX3BoYXNl
X3ByZXNlcnZlc19PIl0gZWxzZSAwKSkKICAgICMgKDBkKSB2YWN1dW0gbWFuaWZvbGQgb2YgcmVj
b3JkOiB0d28tYm9keSB0ZXJtIGRlcGVuZHMgb24gcmhvID0gfHBzaXxeMiBvbmx5IChPKDE2KSk7
IE8gdmFuaXNoZXMgb24gY29uc3RhbnRzOgogICAgUFsidHdvX2JvZHlfc3ltbWV0cnkiXSA9ICJP
KDE2KSIKICAgIHogPSBbc3AuSW50ZWdlcigwKV0gKiAxNgogICAgYXNzZXJ0IFRfY29tcGxleCh1
LCB6LCB6KSA9PSAoMCwgMCkgICAjIE8gZGVuc2l0eSB2YW5pc2hlcyBvbiB1bmlmb3JtIHN0YXRl
cyAoZGVyaXZhdGl2ZXMgemVybykKICAgIFBbInJlYWxfdW5pdF9zcGxpdHRpbmdfdGVybV9wcmVz
ZW50Il0gPSBGYWxzZSAgICMgUS1BMS0zIChhdXRob3IncyBhbnN3ZXIgb2YgcmVjb3JkOyB0aGUg
ZXh0cmFjdCBoYXMgbm8gc3VjaCB0ZXJtKQogICAgUFsidmFjdXVtX21hbmlmb2xkX29mX3JlY29y
ZCJdID0gIlMxNSI7IFBbInBpMV9WIl0gPSAwOyBQWyJwaTRfViJdID0gMCAgICMgcGlfayhTXm4p
PTAgZm9yIGs8biAoYWRvcHRlZCkKICAgICMgbG9ja2luZyBpbnZlbnRvcnk6IHN0YWJpbGl6ZXJz
IGluIGcyIG9mIHJlcHJlc2VudGF0aXZlIHBzaV8wIGJ5IHJhbmsgb2Ygc3BhbihJbSBhLCBJbSBi
KQogICAgZGVmIHN0YWJfZGltKHZlY3RvcnMpOgogICAgICAgICMge0QgaW4gZzIgOiBEIHYgPSAw
IGZvciB2IGluIHZlY3RvcnN9OyB2ZWN0b3JzIGluIEltIE8gKDctdmVjdG9ycykKICAgICAgICBj
b2xzID0gW10KICAgICAgICBmb3IgRCBpbiBnMjoKICAgICAgICAgICAgY29sID0gW10KICAgICAg
ICAgICAgZm9yIHYgaW4gdmVjdG9yczogY29sICs9IGxpc3QoRCAqIHNwLk1hdHJpeCh2KSkKICAg
ICAgICAgICAgY29scy5hcHBlbmQoY29sKQogICAgICAgIE0gPSBzcC5NYXRyaXgoY29scykuVCAg
ICMgKDcqbGVuKSB4IDE0CiAgICAgICAgbnMgPSBNLm51bGxzcGFjZSgpCiAgICAgICAgcmV0dXJu
IGxlbihucyksIG5zCiAgICBlID0gbGFtYmRhIGs6IFsxIGlmIGkgPT0gay0xIGVsc2UgMCBmb3Ig
aSBpbiByYW5nZSg3KV0KICAgIGQwLCBfID0gc3RhYl9kaW0oW10pICAgICAgICAgICAgICAgICAg
ICAgIyByYW5rIDA6IHBzaV8wID0gZV8wIChyZWFsIHVuaXQpOiBhbGwgb2YgZzIKICAgIGQxLCBu
czEgPSBzdGFiX2RpbShbZSg3KV0pICAgICAgICAgICAgICAgIyByYW5rIDE6IHBzaV8wID0gZV83
CiAgICBkMiwgbnMyID0gc3RhYl9kaW0oW2UoMSksIGUoMildKSAgICAgICAgICMgcmFuayAyOiBw
c2lfMCA9IGVfMSArIGkgZV8yCiAgICBhc3NlcnQgKGQwLCBkMSwgZDIpID09ICgxNCwgOCwgMykK
ICAgICMgdGhlIHJhbmstMiBzdGFiaWxpemVyIGFsc28gZml4ZXMgZV80ID0gZV8xIGVfMiAocG9p
bnR3aXNlIHN0YWJpbGl6ZXIgb2YgdGhlIHF1YXRlcm5pb24gc3ViYWxnZWJyYSk6CiAgICBzdWIy
ID0gW3N1bSgoYyAqIEQgZm9yIGMsIEQgaW4gemlwKHYsIGcyKSksIHNwLnplcm9zKDcsIDcpKSBm
b3IgdiBpbiBuczJdCiAgICBhc3NlcnQgYWxsKEQgKiBzcC5NYXRyaXgoZSg0KSkgPT0gc3AuemVy
b3MoNywgMSkgZm9yIEQgaW4gc3ViMikKICAgIFBbIl9zdWJfbG9uZyJdID0gc3ViMgogICAgUFsi
X3N1Yl9zdTMiXSA9IFtzdW0oKGMgKiBEIGZvciBjLCBEIGluIHppcCh2LCBnMikpLCBzcC56ZXJv
cyg3LCA3KSkgZm9yIHYgaW4gbnMxXQogICAgaW52ID0gW10KICAgIGZvciByYW5rLCBIMCwgZGlt
IGluICgoMCwgIkcyIiwgMTQpLCAoMSwgIlNVMyIsIDgpLCAoMiwgIlNVMl9sb25nIiwgMykpOgog
ICAgICAgIGludi5hcHBlbmQoeyJyYW5rIjogcmFuaywgIkgwIjogSDAsICJIMF9kaW0iOiBkaW0s
ICJwaTBfZ2VuZXJpYyI6IDEsICJzbDJfZ2VuZXJhdG9yX2pvcmRhbl90eXBlIjogWzIsIDIsIDEs
IDEsIDFdLAogICAgICAgICAgICAgICAgICAgICJzbDJfZ2VuZXJhdG9yX2luZGV4IjogMSwgInBp
M19pbmplY3RpdmUiOiBUcnVlLCAicGk0X3F1b3RpZW50IjogMH0pCiAgICBQWyJsb2NraW5nX2lu
dmVudG9yeSJdID0gaW52CiAgICAjICgwZSkgY29udHJvbHMKICAgICMgTF9wZXJwIHBzaTAgPSAw
OiB3aXRoIG11ID0gVSpyaG8wIHRoZSBvcGVyYXRvciAtMS8yIGdyYWReMiArIChVIHJobyAtIG11
KSBhbm5paGlsYXRlcyB0aGUgdW5pZm9ybSBzdGF0ZSAoc3ltYm9saWMgaWRlbnRpdHkpCiAgICBV
LCByaG8wID0gc3Auc3ltYm9scygnVSByaG8wJywgcG9zaXRpdmU9VHJ1ZSk7IG11ID0gVSpyaG8w
CiAgICBQWyJjb250cm9scyJdID0geyJMX3BlcnBfemVyb19tb2RlIjogc3Auc2ltcGxpZnkoKFUq
cmhvMCAtIG11KSkgPT0gMCwKICAgICAgICAgICAgICAgICAgICAgIkYyMV9zcGxpdF8xXzNfM2Jh
ciI6IE5vbmUsICJnZW5lcmljX3NvMTZfZmFpbHNfbWFyZ2luX3Bvc2l0aXZlIjogYm9vbChtYXJn
aW4gPiAwKX0KICAgIFBbIl9tYXJnaW4iXSA9IHN0cihtYXJnaW4pCiAgICByZXR1cm4gUAoKIyAt
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLSBmaW5pdGUgZ3JvdXBzIG9uIHRoZSBGYW5vIHBsYW5lCmRlZiBm
YW5vX2NvbGxpbmVhdGlvbnMoKToKICAgIHB0cyA9IGxpc3QocmFuZ2UoMSwgOCkpOyBvdXQgPSBb
XQogICAgZm9yIHBlcm0gaW4gaXRlcnRvb2xzLnBlcm11dGF0aW9ucyhwdHMpOgogICAgICAgIG0g
PSBkaWN0KHppcChwdHMsIHBlcm0pKQogICAgICAgIGlmIGFsbChmcm96ZW5zZXQobVt4XSBmb3Ig
eCBpbiBsKSBpbiBMSU5FU0VUUyBmb3IgbCBpbiBMSU5FUyk6IG91dC5hcHBlbmQobSkKICAgIHJl
dHVybiBvdXQKZGVmIHBlcm1fbWF0cml4KHBlcm0sIHNpZ25zKToKICAgIFAgPSBzcC56ZXJvcyg4
LCA4KTsgUFswLCAwXSA9IDEKICAgIGZvciBpIGluIHJhbmdlKDEsIDgpOiBQW3Blcm1baV0sIGld
ID0gc2lnbnMuZ2V0KGksIDEpCiAgICByZXR1cm4gUApkZWYgaXNfYXV0X3NpZ25lZChwZXJtLCBz
aWducyk6CiAgICAiIiJleGFjdCBhdXRvbW9ycGhpc20gdGVzdCBmb3IgYSBzaWduZWQgcGVybXV0
YXRpb24gZV9pIC0+IHNpZ25zW2ldIGVfe3Blcm1baV19IChpbWFnaW5hcnkgdW5pdHMpLCBmaXhp
bmcgZV8wLiIiIgogICAgZm9yIGkgaW4gcmFuZ2UoMSwgOCk6CiAgICAgICAgZm9yIGogaW4gcmFu
Z2UoMSwgOCk6CiAgICAgICAgICAgIGlmIGkgPT0gajogY29udGludWUKICAgICAgICAgICAgZXBz
LCBrID0gTVVMVFsoaSwgaildCiAgICAgICAgICAgIGVwczIsIGsyID0gTVVMVFsocGVybVtpXSwg
cGVybVtqXSldCiAgICAgICAgICAgIGlmIHBlcm1ba10gIT0gazI6IHJldHVybiBGYWxzZQogICAg
ICAgICAgICBpZiBlcHMgKiBzaWducy5nZXQoaywgMSkgIT0gc2lnbnMuZ2V0KGksIDEpICogc2ln
bnMuZ2V0KGosIDEpICogZXBzMjogcmV0dXJuIEZhbHNlCiAgICByZXR1cm4gVHJ1ZQpkZWYgdW5z
aWduZWRfYXV0b21vcnBoaXNtcyhjb2xscyk6CiAgICByZXR1cm4gW20gZm9yIG0gaW4gY29sbHMg
aWYgaXNfYXV0X3NpZ25lZChtLCB7fSldCmRlZiBGMjFfY2hlY2soY29sbHMpOgogICAgRjIxID0g
WyB7eDogKGEqeCArIGIgLSAxKSAlIDcgKyAxIGZvciB4IGluIHJhbmdlKDEsIDgpfSBmb3IgYSBp
biAoMSwgMiwgNCkgZm9yIGIgaW4gcmFuZ2UoNykgXQogICAgb2sgPSBhbGwoaXNfYXV0X3NpZ25l
ZChtLCB7fSkgZm9yIG0gaW4gRjIxKSBhbmQgbGVuKHt0dXBsZShzb3J0ZWQobS5pdGVtcygpKSkg
Zm9yIG0gaW4gRjIxfSkgPT0gMjEKICAgIGNoaSA9IFtzdW0oMSBmb3IgeCBpbiByYW5nZSgxLCA4
KSBpZiBtW3hdID09IHgpIGZvciBtIGluIEYyMV0KICAgIG5vcm0gPSBzcC5SYXRpb25hbChzdW0o
YypjIGZvciBjIGluIGNoaSksIDIxKTsgdHJpdiA9IHNwLlJhdGlvbmFsKHN1bShjaGkpLCAyMSkK
ICAgIG51MiA9IHt4OiAoMip4IC0gMSkgJSA3ICsgMSBmb3IgeCBpbiByYW5nZSgxLCA4KX0KICAg
IHJldHVybiBvayBhbmQgbm9ybSA9PSAzIGFuZCB0cml2ID09IDEsIGlzX2F1dF9zaWduZWQobnUy
LCB7fSksIGludChub3JtKSwgaW50KHRyaXYpCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIFBoYXNl
IDEKZGVmIHBoYXNlMShnMiwgUDApOgogICAgUiA9IHt9CiAgICAjIC0tLS0tLS0tLS0tLS0tLS0g
VDEKICAgIGltcG9ydCBjbWF0aAogICAgczIgPSBzcC5zcXJ0KDIpCiAgICBRID0gc2V0KCkKICAg
IGZvciBzaWducyBpbiBpdGVydG9vbHMucHJvZHVjdChbMSwgLTFdLCByZXBlYXQ9NCk6CiAgICAg
ICAgZm9yIHBvcyBpbiByYW5nZSg0KToKICAgICAgICAgICAgdiA9IFswLCAwLCAwLCAwXTsgdltw
b3NdID0gc2lnbnNbcG9zXTsgUS5hZGQodHVwbGUoc3AuSW50ZWdlcih4KSBmb3IgeCBpbiB2KSkK
ICAgICAgICBRLmFkZCh0dXBsZShzcC5SYXRpb25hbChzLCAyKSBmb3IgcyBpbiBzaWducykpCiAg
ICBmb3IgaSwgaiBpbiBpdGVydG9vbHMuY29tYmluYXRpb25zKHJhbmdlKDQpLCAyKToKICAgICAg
ICBmb3Igc2kgaW4gKDEsIC0xKToKICAgICAgICAgICAgZm9yIHNqIGluICgxLCAtMSk6CiAgICAg
ICAgICAgICAgICB2ID0gW3NwLkludGVnZXIoMCldICogNDsgdltpXSA9IHNpL3MyOyB2W2pdID0g
c2ovczI7IFEuYWRkKHR1cGxlKHYpKQogICAgUSA9IGxpc3QoUSk7IGFzc2VydCBsZW4oUSkgPT0g
NDgKICAgIGRlZiBxbXVsKGEsIGIpOgogICAgICAgIGEwLCBhMSwgYTIsIGEzID0gYTsgYjAsIGIx
LCBiMiwgYjMgPSBiCiAgICAgICAgcmV0dXJuIChhMCpiMC1hMSpiMS1hMipiMi1hMypiMywgYTAq
YjErYTEqYjArYTIqYjMtYTMqYjIsIGEwKmIyLWExKmIzK2EyKmIwK2EzKmIxLCBhMCpiMythMSpi
Mi1hMipiMSthMypiMCkKICAgIGRlZiBjaGkzMihxKTogICAjIDJjb3MzcGhpICsgMmNvc3BoaSB3
aXRoIGMgPSBjb3MgcGhpID0gUmUgcTogOGNeMyAtIDRjCiAgICAgICAgYyA9IHFbMF07IHJldHVy
biBzcC5leHBhbmQoOCpjKiozIC0gNCpjKQogICAgbm9ybSA9IHNwLnNpbXBsaWZ5KHN1bShjaGkz
MihxKSoqMiBmb3IgcSBpbiBRKSAvIDQ4KQogICAgZnMgPSBzcC5zaW1wbGlmeShzdW0oY2hpMzIo
dHVwbGUoc3Auc2ltcGxpZnkoeCkgZm9yIHggaW4gcW11bChxLCBxKSkpIGZvciBxIGluIFEpIC8g
NDgpCiAgICBUMSA9IHsiY2hpMzJfbm9ybSI6IGludChub3JtKSwgImNoaTMyX2F0XzEiOiBpbnQo
Y2hpMzIoKDEsIDAsIDAsIDApKSksICJjaGkzMl9hdF9taW51czEiOiBpbnQoY2hpMzIoKC0xLCAw
LCAwLCAwKSkpLCAiZnNfaW5kaWNhdG9yIjogaW50KGZzKX0KICAgIFQxWyJzZXZlbl9yZWFsIl0g
PSBhbGwoYWxsKHguaXNfcmF0aW9uYWwgZm9yIHggaW4gRCkgZm9yIEQgaW4gZzIpICAgICAjIHRo
ZSA3IGlzIGRlZmluZWQgb3ZlciBRIChyZWFsIGZvcm0pCiAgICAjIGV2ZW4tbXVsdGlwbGljaXR5
IHRoZW9yZW0gZm9yIGEgcXVhdGVybmlvbmljIGlycmVwIGluIGEgcmVhbCByZXByZXNlbnRhdGlv
biArIGRpbWVuc2lvbiBib3VuZAogICAgdXBwZXIgPSA3IC8vIDQgICAgICAgICAgICAgICAgICAg
ICAjIDEKICAgIFQxWyJxdWFydGV0X211bHRpcGxpY2l0eV91cHBlciJdID0gdXBwZXIgaWYgdXBw
ZXIgJSAyID09IDAgZWxzZSB1cHBlciAtIDEgICAgICMgZXZlbiBhbmQgPD0gZmxvb3IoNy80KSAt
PiAwCiAgICBUMVsicGhhc2VfY2hhcl9vbl8yT190cml2aWFsIl0gPSBUcnVlICAgIyBIb20oMk8s
IFozKSA9IDE6IHwyT15hYnwgPSAyIGlzIGNvcHJpbWUgdG8gMyAoaW50ZWdlciBmYWN0LCBhc3Nl
cnRlZCBiZWxvdykKICAgIGFzc2VydCBtYXRoLmdjZCgyLCAzKSA9PSAxCiAgICAjIGJyYW5jaGlu
Z3MgdmlhIHRoZSBjb21wYWN0IENhc2ltaXIgQyA9IHN1bSAoR14tMSlfaWogRF9pIERfaiwgR19p
aiA9IC1LX3N1YihEX2ksRF9qKS8yIDsgZWlnZW52YWx1ZXMgLWooaisxKQogICAgZGVmIGNhc2lt
aXJfc3BlY3RydW0oc3ViKToKICAgICAgICBuID0gbGVuKHN1Yik7IGFzc2VydCBuID09IDMKICAg
ICAgICAjIGFkam9pbnQgd2l0aGluIHRoZSBzdWJhbGdlYnJhCiAgICAgICAgTXN1YiA9IHNwLk1h
dHJpeChbbGlzdChTKSBmb3IgUyBpbiBzdWJdKS5UCiAgICAgICAgTnN1YiA9IChNc3ViLlQgKiBN
c3ViKS5pbnYoKSAqIE1zdWIuVAogICAgICAgIGRlZiBhZF9jb29yZHMoWCk6CiAgICAgICAgICAg
IGNvbHMgPSBbXQogICAgICAgICAgICBmb3IgWSBpbiBzdWI6CiAgICAgICAgICAgICAgICBaID0g
WCpZIC0gWSpYCiAgICAgICAgICAgICAgICBzb2wgPSBOc3ViICogc3AuTWF0cml4KGxpc3QoWikp
CiAgICAgICAgICAgICAgICBhc3NlcnQgTXN1Yipzb2wgPT0gc3AuTWF0cml4KGxpc3QoWikpCiAg
ICAgICAgICAgICAgICBjb2xzLmFwcGVuZChsaXN0KHNvbCkpCiAgICAgICAgICAgIHJldHVybiBz
cC5NYXRyaXgoY29scykuVAogICAgICAgIGFkcyA9IFthZF9jb29yZHMoWCkgZm9yIFggaW4gc3Vi
XQogICAgICAgIEsgPSBzcC5NYXRyaXgoMywgMywgbGFtYmRhIGksIGo6IChhZHNbaV0qYWRzW2pd
KS50cmFjZSgpKQogICAgICAgIEcgPSAtSy8yOyBHaSA9IEcuaW52KCkKICAgICAgICBDID0gc3Au
emVyb3MoNywgNykKICAgICAgICBmb3IgaSBpbiByYW5nZSgzKToKICAgICAgICAgICAgZm9yIGog
aW4gcmFuZ2UoMyk6IEMgKz0gR2lbaSwgal0gKiBzdWJbaV0gKiBzdWJbal0KICAgICAgICBldiA9
ICgtQykuZWlnZW52YWxzKCkKICAgICAgICBzcGVjID0ge30KICAgICAgICBmb3IgdmFsLCBtdWx0
IGluIGV2Lml0ZW1zKCk6IHNwZWNbc3AubnNpbXBsaWZ5KHZhbCldID0gbXVsdAogICAgICAgICMg
LWooaisxKSAtPiBqIDsgaXJyZXBzIGRpbXMgMmorMSwgY291bnQgPSBtdWx0LygyaisxKQogICAg
ICAgIGRpbXMgPSBbXQogICAgICAgIGZvciBqajEsIG11bHQgaW4gc3BlYy5pdGVtcygpOgogICAg
ICAgICAgICBqID0gKC0xICsgc3Auc3FydCgxICsgNCpqajEpKSAvIDI7IGogPSBzcC5uc2ltcGxp
ZnkoaikKICAgICAgICAgICAgZCA9IGludCgyKmogKyAxKTsgYXNzZXJ0IG11bHQgJSBkID09IDAK
ICAgICAgICAgICAgZGltcyArPSBbZF0gKiAobXVsdCAvLyBkKQogICAgICAgIHJldHVybiBzb3J0
ZWQoZGltcywgcmV2ZXJzZT1UcnVlKQogICAgc3ViX2xvbmcgPSBQMFsiX3N1Yl9sb25nIl0KICAg
IFQxWyJicmFuY2hpbmdfbG9uZ19yb290Il0gPSBjYXNpbWlyX3NwZWN0cnVtKHN1Yl9sb25nKQog
ICAgIyBzaG9ydC1yb290OiB0aGUgaWRlYWwgb2Ygc28oNCkgPSBzdGFiKEhfTCkgY29tcGxlbWVu
dGFyeSB0byB0aGUgbG9uZy1yb290IGlkZWFsCiAgICBkZWYgc3RhYl9zZXR3aXNlX2RpbShzdWJz
cGFjZV92ZWN0b3JzKToKICAgICAgICAjIHtEIGluIGcyIDogRChzcGFuKSBzdWJzZXQgc3Bhbn0K
ICAgICAgICBWID0gc3AuTWF0cml4KHN1YnNwYWNlX3ZlY3RvcnMpLlQgICAjIDcgeCBrCiAgICAg
ICAgcHJvaiA9IHNwLmV5ZSg3KSAtIFYgKiAoVi5UICogVikuaW52KCkgKiBWLlQKICAgICAgICBj
b2xzID0gW10KICAgICAgICBmb3IgRCBpbiBnMjoKICAgICAgICAgICAgY29sID0gW10KICAgICAg
ICAgICAgZm9yIHYgaW4gc3Vic3BhY2VfdmVjdG9yczogY29sICs9IGxpc3QocHJvaiAqIEQgKiBz
cC5NYXRyaXgodikpCiAgICAgICAgICAgIGNvbHMuYXBwZW5kKGNvbCkKICAgICAgICBucyA9IHNw
Lk1hdHJpeChjb2xzKS5ULm51bGxzcGFjZSgpCiAgICAgICAgcmV0dXJuIFtzdW0oKGMgKiBEIGZv
ciBjLCBEIGluIHppcCh2LCBnMikpLCBzcC56ZXJvcyg3LCA3KSkgZm9yIHYgaW4gbnNdCiAgICBl
ID0gbGFtYmRhIGs6IFsxIGlmIGkgPT0gay0xIGVsc2UgMCBmb3IgaSBpbiByYW5nZSg3KV0KICAg
IHNvNCA9IHN0YWJfc2V0d2lzZV9kaW0oW2UoMSksIGUoMiksIGUoNCldKQogICAgYXNzZXJ0IGxl
bihzbzQpID09IDYKICAgICMgY2VudHJhbGl6ZXIgb2YgdGhlIGxvbmctcm9vdCBpZGVhbCBpbnNp
ZGUgc280CiAgICBkZWYgY2VudHJhbGl6ZXJfaW4oc3BhY2UsIHN1Yik6CiAgICAgICAgY29scyA9
IFtdCiAgICAgICAgZm9yIFggaW4gc3BhY2U6CiAgICAgICAgICAgIGNvbCA9IFtdCiAgICAgICAg
ICAgIGZvciBZIGluIHN1YjogY29sICs9IGxpc3QoWCpZIC0gWSpYKQogICAgICAgICAgICBjb2xz
LmFwcGVuZChjb2wpCiAgICAgICAgbnMgPSBzcC5NYXRyaXgoY29scykuVC5udWxsc3BhY2UoKQog
ICAgICAgIHJldHVybiBbc3VtKChjICogWCBmb3IgYywgWCBpbiB6aXAodiwgc3BhY2UpKSwgc3Au
emVyb3MoNywgNykpIGZvciB2IGluIG5zXQogICAgc3ViX3Nob3J0ID0gY2VudHJhbGl6ZXJfaW4o
c280LCBzdWJfbG9uZykKICAgIGFzc2VydCBsZW4oc3ViX3Nob3J0KSA9PSAzCiAgICBUMVsiYnJh
bmNoaW5nX3Nob3J0X3Jvb3QiXSA9IGNhc2ltaXJfc3BlY3RydW0oc3ViX3Nob3J0KQogICAgIyBz
dSgzKS1zbDI6IHNvKDMpIGJ1aWx0IGZyb20gdGhlIEotYmFzaXMgKGUxLGUzKSwoZTIsZTYpLChl
NCxlNSkgd2l0aCBKID0gTF97ZTd9OyBjaGVjayBtZW1iZXJzaGlwIGluIHN0YWIoZTcpCiAgICBk
ZWYgcm90KGksIGopOgogICAgICAgIE0gPSBzcC56ZXJvcyg3LCA3KTsgTVtpLTEsIGotMV0gPSAt
MTsgTVtqLTEsIGktMV0gPSAxOyByZXR1cm4gTQogICAgUjEyID0gcm90KDEsIDIpICsgcm90KDMs
IDYpOyBSMTMgPSByb3QoMSwgNCkgKyByb3QoMywgNSk7IFIyMyA9IHJvdCgyLCA0KSArIHJvdCg2
LCA1KQogICAgZGVmIGluX3NwYW4oWCwgc3BhY2UpOgogICAgICAgIE0gPSBzcC5NYXRyaXgoW2xp
c3QoUykgZm9yIFMgaW4gc3BhY2VdKS5UCiAgICAgICAgcmV0dXJuIHNwLk1hdHJpeC5oc3RhY2so
TSwgc3AuTWF0cml4KGxpc3QoWCkpKS5yYW5rKCkgPT0gTS5yYW5rKCkKICAgIHN1MyA9IFAwWyJf
c3ViX3N1MyJdCiAgICBhc3NlcnQgYWxsKGluX3NwYW4oWCwgc3UzKSBmb3IgWCBpbiAoUjEyLCBS
MTMsIFIyMykpLCAic28oMykgY29uc3RydWN0aW9uIG5vdCBpbnNpZGUgc3RhYihlNykiCiAgICBU
MVsiYnJhbmNoaW5nX3N1M19zbDIiXSA9IGNhc2ltaXJfc3BlY3RydW0oW1IxMiwgUjEzLCBSMjNd
KQogICAgIyBwcmluY2lwYWwgc2wyOiB3ZWlnaHRzIG9mIGhfcHJpbmMgPSAyIHJob152ZWUgb24g
dGhlIDcgdmlhIHRoZSByb290IHN5c3RlbSBvZiBnMiAoQ2FydGFuID0gc3UoMykgQ2FydGFuKQog
ICAgaDEgPSByb3QoMSwgMykgLSByb3QoMiwgNik7IGgyID0gcm90KDIsIDYpIC0gcm90KDQsIDUp
CiAgICBhc3NlcnQgaW5fc3BhbihoMSwgc3UzKSBhbmQgaW5fc3BhbihoMiwgc3UzKSBhbmQgKGgx
KmgyIC0gaDIqaDEpID09IHNwLnplcm9zKDcsIDcpCiAgICAjIGFkKGgpIG9uIGcyICgxNHgxNCks
IGVpZ2VudmFsdWVzIG9mIGkqYWQoaCkgYXJlIGludGVnZXJzCiAgICBNYiA9IHNwLk1hdHJpeChb
bGlzdChEKSBmb3IgRCBpbiBnMl0pLlQKICAgIE5iID0gKE1iLlQgKiBNYikuaW52KCkgKiBNYi5U
CiAgICBkZWYgYWRfb25fZzIoSCk6CiAgICAgICAgY29scyA9IFtdCiAgICAgICAgZm9yIEQgaW4g
ZzI6CiAgICAgICAgICAgIFogPSBIKkQgLSBEKkg7IHNvbCA9IE5iICogc3AuTWF0cml4KGxpc3Qo
WikpCiAgICAgICAgICAgIGFzc2VydCBNYipzb2wgPT0gc3AuTWF0cml4KGxpc3QoWikpCiAgICAg
ICAgICAgIGNvbHMuYXBwZW5kKGxpc3Qoc29sKSkKICAgICAgICByZXR1cm4gc3AuTWF0cml4KGNv
bHMpLlQKICAgIEExID0gYWRfb25fZzIoaDEpOyBBMiA9IGFkX29uX2cyKGgyKQogICAgIyBzaW11
bHRhbmVvdXMgZWlnZW52ZWN0b3JzOiBlaWdlbnZhbHVlcyBvZiBpKkExIChyZWFsIGludHMpIGFu
ZCB0aGUgbWF0Y2hpbmcgaSpBMiB2YWx1ZXMKICAgIEkgPSBzcC5JCiAgICBldjEgPSAoSSpBMSku
ZWlnZW52ZWN0cygpCiAgICByb290cyA9IFtdCiAgICBmb3IgdmFsMSwgbXVsdCwgdmVjcyBpbiBl
djE6CiAgICAgICAgZm9yIHYgaW4gdmVjczoKICAgICAgICAgICAgdyA9IEkqQTIqdgogICAgICAg
ICAgICAjIHYgaXMgYW4gZWlnZW52ZWN0b3Igb2YgQTIgcmVzdHJpY3RlZD8gbm90IG5lY2Vzc2Fy
aWx5OyBkaWFnb25hbGl6ZSBBMiBvbiB0aGUgZWlnZW5zcGFjZQogICAgICAgICMgcmVzdHJpY3Qg
aSpBMiB0byB0aGUgZWlnZW5zcGFjZSBvZiBpKkExIHdpdGggZWlnZW52YWx1ZSB2YWwxCiAgICAg
ICAgVnMgPSBzcC5NYXRyaXguaHN0YWNrKCp2ZWNzKQogICAgICAgIEIgPSAoVnMuSCAqIFZzKS5p
bnYoKSAqIFZzLkggKiAoSSpBMikgKiBWcwogICAgICAgIGZvciB2YWwyLCBtMiwgXyBpbiBCLmVp
Z2VudmVjdHMoKToKICAgICAgICAgICAgcm9vdHMgKz0gWyhzcC5uc2ltcGxpZnkodmFsMSksIHNw
Lm5zaW1wbGlmeSh2YWwyKSldICogbTIKICAgIHJvb3RzID0gW3IgZm9yIHIgaW4gcm9vdHMgaWYg
ciAhPSAoMCwgMCldCiAgICBhc3NlcnQgbGVuKHJvb3RzKSA9PSAxMiBhbmQgbGVuKHNldChyb290
cykpID09IDEyCiAgICAjIHdlaWdodHMgb2YgdGhlIDcgKGVpZ2VudmFsdWUgcGFpcnMgb2YgaSBo
MSwgaSBoMiBvbiBDXjcpCiAgICBldkEgPSAoSSpoMSkuZWlnZW52ZWN0cygpOyB3dHMgPSBbXQog
ICAgZm9yIHZhbDEsIG11bHQsIHZlY3MgaW4gZXZBOgogICAgICAgIFZzID0gc3AuTWF0cml4Lmhz
dGFjaygqdmVjcyk7IEIgPSAoVnMuSCAqIFZzKS5pbnYoKSAqIFZzLkggKiAoSSpoMikgKiBWcwog
ICAgICAgIGZvciB2YWwyLCBtMiwgXyBpbiBCLmVpZ2VudmVjdHMoKTogd3RzICs9IFsoc3AubnNp
bXBsaWZ5KHZhbDEpLCBzcC5uc2ltcGxpZnkodmFsMikpXSAqIG0yCiAgICBhc3NlcnQgbGVuKHd0
cykgPT0gNwogICAgIyBwb3NpdGl2ZSBzeXN0ZW0gdmlhIGEgZ2VuZXJpYyBmdW5jdGlvbmFsOyBz
aW1wbGUgcm9vdHMgPSBwb3NpdGl2ZSByb290cyBub3QgYSBzdW0gb2YgdHdvIHBvc2l0aXZlIHJv
b3RzCiAgICBmID0gbGFtYmRhIHI6IDcqclswXSArIDMqclsxXQogICAgcG9zID0gW3IgZm9yIHIg
aW4gcm9vdHMgaWYgZihyKSA+IDBdOyBhc3NlcnQgbGVuKHBvcykgPT0gNgogICAgc2ltcGxlID0g
W3IgZm9yIHIgaW4gcG9zIGlmIG5vdCBhbnkoKHJbMF0tcFswXSwgclsxXS1wWzFdKSBpbiBwb3Mg
Zm9yIHAgaW4gcG9zKV0KICAgIGFzc2VydCBsZW4oc2ltcGxlKSA9PSAyCiAgICAjIGhfcHJpbmMg
PSBjMSAoaSBoMSkgKyBjMiAoaSBoMikgd2l0aCBhbHBoYV9rKGhfcHJpbmMpID0gMiBmb3IgYm90
aCBzaW1wbGUgcm9vdHM6IGFscGhhKGgpID0gYzEqYWxwaGFfMSArIGMyKmFscGhhXzIgKHJvb3Qg
Y29vcmRzIGFyZSB0aGUgZWlnZW52YWx1ZXMpCiAgICBjMSwgYzIgPSBzcC5zeW1ib2xzKCdjMSBj
MicpCiAgICBzb2wgPSBzcC5zb2x2ZShbYzEqc2ltcGxlWzBdWzBdICsgYzIqc2ltcGxlWzBdWzFd
IC0gMiwgYzEqc2ltcGxlWzFdWzBdICsgYzIqc2ltcGxlWzFdWzFdIC0gMl0sIFtjMSwgYzJdKQog
ICAgaHBfd2VpZ2h0cyA9IHNvcnRlZChbc3AubnNpbXBsaWZ5KHNvbFtjMV0qd1swXSArIHNvbFtj
Ml0qd1sxXSkgZm9yIHcgaW4gd3RzXSkKICAgICMgZGVjb21wb3NlIHRoZSB3ZWlnaHQgbXVsdGlz
ZXQgaW50byBzbDIgc3RyaW5ncwogICAgZnJvbSBjb2xsZWN0aW9ucyBpbXBvcnQgQ291bnRlcgog
ICAgY250ID0gQ291bnRlcihocF93ZWlnaHRzKTsgZGltcyA9IFtdCiAgICB3aGlsZSBjbnQ6CiAg
ICAgICAgdG9wID0gbWF4KGsgZm9yIGssIHYgaW4gY250Lml0ZW1zKCkgaWYgdiA+IDApCiAgICAg
ICAgZCA9IGludCh0b3ApICsgMSAgICMgc3RyaW5nIHRvcCwgdG9wLTIsIC4uLiwgLXRvcAogICAg
ICAgIGZvciBrIGluIHJhbmdlKGludCh0b3ApLCAtaW50KHRvcCktMSwgLTIpOgogICAgICAgICAg
ICBjbnRba10gLT0gMQogICAgICAgICAgICBpZiBjbnRba10gPT0gMDogZGVsIGNudFtrXQogICAg
ICAgIGRpbXMuYXBwZW5kKGQpCiAgICBUMVsiYnJhbmNoaW5nX3ByaW5jaXBhbCJdID0gc29ydGVk
KGRpbXMsIHJldmVyc2U9VHJ1ZSkKICAgIFQxWyJfcHJpbmNpcGFsX3dlaWdodHMiXSA9IFtpbnQo
eCkgZm9yIHggaW4gaHBfd2VpZ2h0c10KICAgICMgY29udHJvbCBDLUExLTE6IChDXjIpXnt4M30g
dW5kZXIgZGlhZ29uYWwgc3UoMik6IENhc2ltaXIgc3BlY3RydW0KICAgIHN4ID0gc3AuTWF0cml4
KFtbMCwgMV0sIFsxLCAwXV0pIC8gMjsgc3kgPSBzcC5NYXRyaXgoW1swLCAtSV0sIFtJLCAwXV0p
IC8gMjsgc3ogPSBzcC5NYXRyaXgoW1sxLCAwXSwgWzAsIC0xXV0pIC8gMgogICAgZGVmIGtyb24z
KG0pOgogICAgICAgIEUyID0gc3AuZXllKDIpCiAgICAgICAgcmV0dXJuIHNwLmtyb25lY2tlcl9w
cm9kdWN0KG0sIEUyLCBFMikgKyBzcC5rcm9uZWNrZXJfcHJvZHVjdChFMiwgbSwgRTIpICsgc3Au
a3JvbmVja2VyX3Byb2R1Y3QoRTIsIEUyLCBtKQogICAgQyA9IGtyb24zKHN4KSoqMiArIGtyb24z
KHN5KSoqMiArIGtyb24zKHN6KSoqMgogICAgZXYgPSBDLmVpZ2VudmFscygpCiAgICBUMVsiY29u
dHJvbF9zeW0zX3F1YXJ0ZXRfbXVsdCJdID0gaW50KGV2LmdldChzcC5SYXRpb25hbCgxNSwgNCks
IDApIC8vIDQpCiAgICBUMVsiaG9sZHMiXSA9IGJvb2woVDFbImZzX2luZGljYXRvciJdID09IC0x
IGFuZCBUMVsiY2hpMzJfbm9ybSJdID09IDEgYW5kIFQxWyJjaGkzMl9hdF9taW51czEiXSA9PSAt
NCBhbmQgVDFbInNldmVuX3JlYWwiXQogICAgICAgICAgICAgICAgICAgICAgIGFuZCBUMVsicXVh
cnRldF9tdWx0aXBsaWNpdHlfdXBwZXIiXSA9PSAwIGFuZCBhbGwoNCBub3QgaW4gVDFba10gZm9y
IGsgaW4gKCJicmFuY2hpbmdfbG9uZ19yb290IiwgImJyYW5jaGluZ19zaG9ydF9yb290IiwgImJy
YW5jaGluZ19zdTNfc2wyIiwgImJyYW5jaGluZ19wcmluY2lwYWwiKSkpCiAgICBSWyJUMSJdID0g
VDEKCiAgICAjIC0tLS0tLS0tLS0tLS0tLS0gVDIKICAgIFQyID0ge30KICAgIEwgPSB7YTogTG1h
dChhKSBmb3IgYSBpbiByYW5nZSgxLCA4KX0KICAgIGZvciBhIGluIHJhbmdlKDEsIDgpOgogICAg
ICAgIGZvciBiIGluIHJhbmdlKDEsIDgpOgogICAgICAgICAgICBTID0gTFthXSpMW2JdICsgTFti
XSpMW2FdCiAgICAgICAgICAgIGFzc2VydCBTID09ICgtMipzcC5leWUoOCkgaWYgYSA9PSBiIGVs
c2Ugc3AuemVyb3MoOCwgOCkpCiAgICBUMlsiZGltX2RlciJdID0gbGVuKGcyKQogICAgYml2NyA9
IFtMW2FdKkxbYl0gZm9yIGEgaW4gcmFuZ2UoMSwgOCkgZm9yIGIgaW4gcmFuZ2UoYSsxLCA4KV0K
ICAgIGJpdjYgPSBbTFthXSpMW2JdIGZvciBhIGluIHJhbmdlKDEsIDcpIGZvciBiIGluIHJhbmdl
KGErMSwgNyldCiAgICBUMlsiZGltX2JpdmVjdG9yc183Il0gPSBzcGFuX2RpbShiaXY3KTsgVDJb
ImRpbV9iaXZlY3RvcnNfNiJdID0gc3Bhbl9kaW0oYml2NikKICAgIGcyXzggPSBbdG84KEQpIGZv
ciBEIGluIGcyXQogICAgVDJbImcyX2luX3NwaW43Il0gPSBzcGFuX2RpbShnMl84ICsgYml2Nykg
PT0gMjEKICAgIFQyWyJkaW1fZzJfY2FwX3N1NCJdID0gMTQgKyAxNSAtIHNwYW5fZGltKGcyXzgg
KyBiaXY2KQogICAgIyAoYikgdGhlIHNwaW5vcmlhbCAyTyBpbnNpZGUgc3UoNClfTCBvbiAoUl44
LCBKPUxfNyk6IEotYmFzaXMgdyA9IChlMCwgZTEsIGUyLCBlNCksIEogdyA9IChlNywgZTMsIGU2
LCBlNSkKICAgIGltcG9ydCBudW1weSBhcyBucAogICAgSiA9IExbN10KICAgIHdiID0gW3VuaXQo
MCksIHVuaXQoMSksIHVuaXQoMiksIHVuaXQoNCldCiAgICBKdyA9IFtsaXN0KEogKiBzcC5NYXRy
aXgodykpIGZvciB3IGluIHdiXQogICAgIyBiYXNpcyBjaGFuZ2U6IHJlYWwgY29vcmRzICh4X2ss
IHlfaykgLT4gdmVjdG9yIHN1bSB4X2sgd19rICsgeV9rIEp3X2sKICAgIEJtID0gc3AuTWF0cml4
LmhzdGFjaygqW3NwLk1hdHJpeCh3KSBmb3IgdyBpbiB3Yl0sICpbc3AuTWF0cml4KHYpIGZvciB2
IGluIEp3XSkgICAjIDh4OCwgY29sdW1ucwogICAgYXNzZXJ0IEJtLnJhbmsoKSA9PSA4CiAgICBC
aSA9IEJtLmludigpCiAgICBkZWYgcmVhbF90b19jb21wbGV4NChNOCk6ICAgIyBNOCBjb21tdXRp
bmcgd2l0aCBKIC0+IGNvbXBsZXggNHg0CiAgICAgICAgTWIgPSBCaSAqIE04ICogQm0gICAgIyBp
biAoeCx5KSBjb29yZGluYXRlczogW1tBLCAtQl0sW0IsIEFdXQogICAgICAgIEFfID0gTWJbOjQs
IDo0XTsgQl8gPSBNYls0OiwgOjRdCiAgICAgICAgYXNzZXJ0IE1iWzo0LCA0Ol0gPT0gLUJfIGFu
ZCBNYls0OiwgNDpdID09IEFfCiAgICAgICAgcmV0dXJuIEFfICsgSSpCXwogICAgZGVmIGNvbXBs
ZXg0X3RvX3JlYWwoQyk6CiAgICAgICAgQV8gPSBzcC5yZShDKTsgQl8gPSBzcC5pbShDKQogICAg
ICAgIE1iID0gc3AuemVyb3MoOCwgOCk7IE1iWzo0LCA6NF0gPSBBXzsgTWJbOjQsIDQ6XSA9IC1C
XzsgTWJbNDosIDo0XSA9IEJfOyBNYls0OiwgNDpdID0gQV8KICAgICAgICByZXR1cm4gQm0gKiBN
YiAqIEJpCiAgICBzdTQgPSBbcmVhbF90b19jb21wbGV4NChNKSBmb3IgTSBpbiBiaXY2XQogICAg
YXNzZXJ0IGFsbChzcC5zaW1wbGlmeShNLnRyYWNlKCkpID09IDAgYW5kIHNwLnNpbXBsaWZ5KE0g
KyBNLkgpID09IHNwLnplcm9zKDQsIDQpIGZvciBNIGluIHN1NCkKICAgICMgc3Bpbi0zLzIgZ2Vu
ZXJhdG9ycyBYX2sgPSAtaSBTX2sgKGFudGloZXJtaXRpYW4sIHRyYWNlbGVzcykKICAgIHMzID0g
c3Auc3FydCgzKQogICAgU3AgPSBzcC5NYXRyaXgoW1swLCBzMywgMCwgMF0sIFswLCAwLCAyLCAw
XSwgWzAsIDAsIDAsIHMzXSwgWzAsIDAsIDAsIDBdXSkgICAjIFMrIGluIHRoZSB8My8yPix8MS8y
Pix8LTEvMj4sfC0zLzI+IGJhc2lzCiAgICBTbSA9IFNwLlQKICAgIFN4ID0gKFNwICsgU20pIC8g
MjsgU3kgPSAoU3AgLSBTbSkgLyAoMipJKTsgU3ogPSBzcC5kaWFnKHNwLlJhdGlvbmFsKDMsIDIp
LCBzcC5SYXRpb25hbCgxLCAyKSwgc3AuUmF0aW9uYWwoLTEsIDIpLCBzcC5SYXRpb25hbCgtMywg
MikpCiAgICBYID0gWy1JKlN4LCAtSSpTeSwgLUkqU3pdCiAgICBhc3NlcnQgc3Auc2ltcGxpZnko
WFswXSpYWzFdIC0gWFsxXSpYWzBdIC0gWFsyXSkgPT0gc3AuemVyb3MoNCwgNCkKICAgIE1zdTQg
PSBzcC5NYXRyaXgoW2xpc3QoTSkgZm9yIE0gaW4gc3U0XSkuVAogICAgZm9yIFhrIGluIFg6CiAg
ICAgICAgYXNzZXJ0IHNwLk1hdHJpeC5oc3RhY2soTXN1NCwgc3AuTWF0cml4KGxpc3QoWGspKSku
cmFuayhzaW1wbGlmeT1UcnVlKSA9PSBNc3U0LnJhbmsoc2ltcGxpZnk9VHJ1ZSksICJzcGluLTMv
MiBnZW5lcmF0b3Igbm90IGluIHN1KDQpX0wiCiAgICAjIGdyb3VwIGVsZW1lbnRzIEQocSkgPSBl
eHAoMiB0aGV0YSBuLlgpIGZvciBxID0gY29zIHRoZXRhICsgc2luIHRoZXRhIChuLmkpOyBudW1l
cmljCiAgICBYbiA9IFtucC5hcnJheShzcC5OKFhrLCAzMCkudG9saXN0KCksIGR0eXBlPWNvbXBs
ZXgpIGZvciBYayBpbiBYXQogICAgZGVmIGV4cG0oTSk6CiAgICAgICAgdywgViA9IG5wLmxpbmFs
Zy5laWcoTSk7IHJldHVybiAoViBAIG5wLmRpYWcobnAuZXhwKHcpKSBAIG5wLmxpbmFsZy5pbnYo
VikpCiAgICBCbV9uID0gbnAuYXJyYXkoc3AuTihCbSkudG9saXN0KCksIGR0eXBlPWZsb2F0KTsg
QmlfbiA9IG5wLmxpbmFsZy5pbnYoQm1fbikKICAgIGRlZiBjNF90b19yOF9uKENtKToKICAgICAg
ICBBXyA9IENtLnJlYWw7IEJfID0gQ20uaW1hZwogICAgICAgIE1iID0gbnAuemVyb3MoKDgsIDgp
KTsgTWJbOjQsIDo0XSA9IEFfOyBNYls6NCwgNDpdID0gLUJfOyBNYls0OiwgOjRdID0gQl87IE1i
WzQ6LCA0Ol0gPSBBXwogICAgICAgIHJldHVybiBCbV9uIEAgTWIgQCBCaV9uCiAgICBkZWZlY3Rz
ID0gW107IHRyYWNlcyA9IFtdOyBhdXRvcyA9IDAKICAgIGZvciBxIGluIFE6CiAgICAgICAgcWYg
PSBbZmxvYXQoc3AuTih4LCAzMCkpIGZvciB4IGluIHFdCiAgICAgICAgYyA9IG1heCgtMS4wLCBt
aW4oMS4wLCBxZlswXSkpOyB0aGV0YSA9IG1hdGguYWNvcyhjKTsgcyA9IG1hdGguc3FydChtYXgo
MC4wLCAxIC0gYypjKSkKICAgICAgICBuID0gW3gvcyBmb3IgeCBpbiBxZlsxOl1dIGlmIHMgPiAx
ZS0xMiBlbHNlIFswLjAsIDAuMCwgMS4wXQogICAgICAgIEQgPSBleHBtKDIqdGhldGEqKG5bMF0q
WG5bMF0gKyBuWzFdKlhuWzFdICsgblsyXSpYblsyXSkpCiAgICAgICAgUDggPSBjNF90b19yOF9u
KEQpCiAgICAgICAgZCA9IGF1dF9kZWZlY3RfZmxvYXQoUDgpOyBkZWZlY3RzLmFwcGVuZCgocWYs
IGQpKTsgdHJhY2VzLmFwcGVuZChucC50cmFjZShQOCkucmVhbCkKICAgICAgICBpZiBkIDwgMWUt
OTogYXV0b3MgKz0gMQogICAgVDJbInNwaW5vcl8yT19vcmRlciJdID0gNDg7IFQyWyJzcGlub3Jf
Mk9fYXV0b21vcnBoaXNtX2NvdW50Il0gPSBhdXRvcwogICAgbm9udHJpdiA9IFtkIGZvciBxZiwg
ZCBpbiBkZWZlY3RzIGlmIG5vdCAoYWJzKHFmWzBdKSA+IDEgLSAxZS0xMiBhbmQgYWxsKGFicyh4
KSA8IDFlLTEyIGZvciB4IGluIHFmWzE6XSkpXQogICAgVDJbInNwaW5vcl8yT19taW5fYXV0b21v
cnBoaXNtX2RlZmVjdCJdID0gZmxvYXQobWluKG5vbnRyaXYpKQogICAgIyBxdWFydGV0IG11bHRp
cGxpY2l0eSBpbiB0aGUgMk8tY2hhcmFjdGVyIG9mIEPiipdPID0gUl44IOKKlyBDOiA8dHIgUDgs
IGNoaTMyPiBvdmVyIDJPCiAgICBjaGlzID0gW2Zsb2F0KHNwLk4oY2hpMzIocSksIDMwKSkgZm9y
IHEgaW4gUV0KICAgIG11bHQgPSBzdW0odCpjaCBmb3IgdCwgY2ggaW4gemlwKHRyYWNlcywgY2hp
cykpIC8gNDgKICAgIGFzc2VydCBhYnMobXVsdCAtIHJvdW5kKG11bHQpKSA8IDFlLTgKICAgIFQy
WyJzcGlub3JfMk9fcXVhcnRldF9tdWx0Il0gPSBpbnQocm91bmQobXVsdCkpCiAgICAjIChjKSBT
TCgyLDcpOiBnXjI9MSBjb3VudDsgb3JkaW5hcnkgRlMgc3VtIHdpdGggdGhlIDYgKEZhbm8gcGVy
bXV0YXRpb24gcmVwKSBhbmQgNyAoUF4xIHBlcm11dGF0aW9uIHJlcCkgbWFjaGluZS12ZXJpZmll
ZAogICAgcCA9IDcKICAgIFNMID0gWyhhLCBiLCBjLCBkKSBmb3IgYSwgYiwgYywgZCBpbiBpdGVy
dG9vbHMucHJvZHVjdChyYW5nZShwKSwgcmVwZWF0PTQpIGlmIChhKmQgLSBiKmMpICUgcCA9PSAx
XQogICAgZGVmIG0yKGcsIGgpOgogICAgICAgIGEsIGIsIGMsIGQgPSBnOyBlXywgZl8sIGdfLCBo
XyA9IGgKICAgICAgICByZXR1cm4gKChhKmVfICsgYipnXykgJSBwLCAoYSpmXyArIGIqaF8pICUg
cCwgKGMqZV8gKyBkKmdfKSAlIHAsIChjKmZfICsgZCpoXykgJSBwKQogICAgVDJbInNsMjdfb3Jk
ZXIiXSA9IGxlbihTTCk7IFQyWyJzbDI3X3NxMV9jb3VudCJdID0gc3VtKDEgZm9yIGcgaW4gU0wg
aWYgbTIoZywgZykgPT0gKDEsIDAsIDAsIDEpKQogICAgIyBQXjEoRjcpIHBlcm11dGF0aW9uIGNo
YXJhY3RlciBvZiBQU0woMiw3KTogOCBwb2ludHM7IFN0ZWluYmVyZyA3ID0gcGVybSAtIDEgOyBG
UyB2aWEgZ14yCiAgICBkZWYgYWN0KGcsIHB0KToKICAgICAgICBhLCBiLCBjLCBkID0gZzsgeCwg
eSA9IHB0ICAgIyBjb2x1bW4gdmVjdG9yICh4LCB5KSAtPiAoYSB4ICsgYiB5LCBjIHggKyBkIHkp
LCBub3JtYWxpemVkCiAgICAgICAgbngsIG55ID0gKGEqeCArIGIqeSkgJSBwLCAoYyp4ICsgZCp5
KSAlIHAKICAgICAgICBpZiBueSA9PSAwOiByZXR1cm4gKDEsIDApIGlmIG54IGVsc2UgTm9uZQog
ICAgICAgIGludiA9IHBvdyhueSwgcC0yLCBwKTsgcmV0dXJuIChueCppbnYgJSBwLCAxKQogICAg
UDEgPSBbKHgsIDEpIGZvciB4IGluIHJhbmdlKHApXSArIFsoMSwgMCldCiAgICBkZWYgZml4X2Nv
dW50KGcpOiByZXR1cm4gc3VtKDEgZm9yIHB0IGluIFAxIGlmIGFjdChnLCBwdCkgPT0gcHQpCiAg
ICAjIEZTIGluZGljYXRvciBvZiB0aGUgcGVybSByZXAgb24gUF4xICg4LWRpbSkgPSAoMS98R3wp
IHN1bSBmaXgoZ14yKTsgaW5kaWNhdG9yIG9mIFN0ID0gdGhhdCAtIDEgKHRyaXZpYWwgY29udHJp
YnV0ZXMgMSkKICAgIGZzX3Blcm04ID0gRnJhY3Rpb24oc3VtKGZpeF9jb3VudChtMihnLCBnKSkg
Zm9yIGcgaW4gU0wpLCBsZW4oU0wpKQogICAgZnNfU3QgPSBmc19wZXJtOCAtIDEKICAgIGNvbGxz
ID0gZmFub19jb2xsaW5lYXRpb25zKCk7IGFzc2VydCBsZW4oY29sbHMpID09IDE2OAogICAgZGVm
IGNmaXgobSk6IHJldHVybiBzdW0oMSBmb3IgeCBpbiByYW5nZSgxLCA4KSBpZiBtW3hdID09IHgp
CiAgICBkZWYgY29tcG9zZShtLCBuKTogcmV0dXJuIHt4OiBtW25beF1dIGZvciB4IGluIHJhbmdl
KDEsIDgpfQogICAgZnNfcGVybTcgPSBGcmFjdGlvbihzdW0oY2ZpeChjb21wb3NlKG0sIG0pKSBm
b3IgbSBpbiBjb2xscyksIDE2OCkKICAgIGZzXzYgPSBmc19wZXJtNyAtIDEKICAgIGFzc2VydCBm
c19TdCA9PSAxIGFuZCBmc182ID09IDEKICAgIFQyWyJmc19zdW1fb3JkaW5hcnkiXSA9IGludCgx
ICsgNipmc182ICsgNypmc19TdCArIDgqMSkgICAjIG51KDMpPW51KDNiYXIpPTAgYW5kIG51KDgp
PSsxIGFkb3B0ZWQgKGNpdGF0aW9ucykKICAgIHNvbHMgPSBbXQogICAgZm9yIG40IGluICgtMSwg
MCwgMSk6CiAgICAgICAgZm9yIG42IGluICgtMSwgMCwgMSk6CiAgICAgICAgICAgIGZvciBuOCBp
biAoLTEsIDAsIDEpOgogICAgICAgICAgICAgICAgaWYgOCpuNCArIDEyKm42ICsgOCpuOCA9PSAy
IC0gVDJbImZzX3N1bV9vcmRpbmFyeSJdOiBzb2xzLmFwcGVuZCgobjQsIG42LCBuOCkpCiAgICBU
MlsibnU0X2FsbG93ZWQiXSA9IHNvcnRlZCh7c1swXSBmb3IgcyBpbiBzb2xzfSk7IFQyWyJfZnNf
c29sdXRpb25zIl0gPSBzb2xzCiAgICAjIGludm9sdXRpb24gbGVtbWEgd2l0bmVzc2VzCiAgICBz
aWcgPSBzcC5kaWFnKCooWzFdICsgWzEgaWYgaSBpbiAoMSwgMiwgNCkgZWxzZSAtMSBmb3IgaSBp
biByYW5nZSgxLCA4KV0pKQogICAgVDJbInNpZ21hX0hfaXNfYXV0b21vcnBoaXNtIl0gPSBpc19h
dXQoc2lnKTsgVDJbImludm9sdXRpb25fdHJhY2UiXSA9IGludChzdW0oc2lnW2ksIGldIGZvciBp
IGluIHJhbmdlKDEsIDgpKSkKICAgIGJhZCA9IHNwLmRpYWcoKihbMV0gKyBbLTEgaWYgaSA9PSA3
IGVsc2UgMSBmb3IgaSBpbiByYW5nZSgxLCA4KV0pKQogICAgVDJbInNpbmdsZV91bml0X25lZ2F0
aW9uX2lzX2F1dG9tb3JwaGlzbSJdID0gaXNfYXV0KGJhZCkKICAgICMgdGhlIHJlYWxpemVkIHNp
Z25lZCBGYW5vIGdyb3VwOiBjbG9zdXJlIG9mIHRoZSBzaWduZWQgYXV0b21vcnBoaXNtIGxpZnRz
CiAgICBkZWYgbGlmdHNfb2YobSk6CiAgICAgICAgb3V0ID0gW10KICAgICAgICBmb3Igc2duIGlu
IGl0ZXJ0b29scy5wcm9kdWN0KFsxLCAtMV0sIHJlcGVhdD03KToKICAgICAgICAgICAgc2lnbnMg
PSB7aSsxOiBzZ25baV0gZm9yIGkgaW4gcmFuZ2UoNyl9CiAgICAgICAgICAgIGlmIGlzX2F1dF9z
aWduZWQobSwgc2lnbnMpOiBvdXQuYXBwZW5kKCh0dXBsZShtW2ldIGZvciBpIGluIHJhbmdlKDEs
IDgpKSwgdHVwbGUoc2duKSkpCiAgICAgICAgcmV0dXJuIG91dAogICAgZGVmIHNjb21wb3NlKHgs
IHkpOiAgICMgKHggbyB5KTogZmlyc3QgeSB0aGVuIHggOyBlbGVtZW50cyBlX2kgLT4gc19pIGVf
e3BfaX0KICAgICAgICBweCwgc3ggPSB4OyBweSwgc3kgPSB5CiAgICAgICAgcCA9IHR1cGxlKHB4
W3B5W2ldLTFdIGZvciBpIGluIHJhbmdlKDcpKTsgc2duID0gdHVwbGUoc3lbaV0gKiBzeFtweVtp
XS0xXSBmb3IgaSBpbiByYW5nZSg3KSkKICAgICAgICByZXR1cm4gKHAsIHNnbikKICAgIGRlZiBz
bWF0KHgpOgogICAgICAgIHJldHVybiBwZXJtX21hdHJpeCh7aSsxOiB4WzBdW2ldIGZvciBpIGlu
IHJhbmdlKDcpfSwge2krMTogeFsxXVtpXSBmb3IgaSBpbiByYW5nZSg3KX0pCiAgICBhX2ludiA9
IHsxOiAxLCAyOiAyLCA0OiA0LCAzOiA1LCA1OiAzLCA2OiA3LCA3OiA2fQogICAgb3JkZXI3ID0g
e3g6IHggJSA3ICsgMSBmb3IgeCBpbiByYW5nZSgxLCA4KX0KICAgIG9yZGVyMyA9IHt4OiAoMip4
IC0gMSkgJSA3ICsgMSBmb3IgeCBpbiByYW5nZSgxLCA4KX0KICAgIGdlbnMgPSBbXQogICAgZm9y
IG0gaW4gKGFfaW52LCBvcmRlcjcsIG9yZGVyMyk6IGdlbnMgKz0gbGlmdHNfb2YobSkKICAgIGlk
ZW50ID0gKHR1cGxlKHJhbmdlKDEsIDgpKSwgdHVwbGUoWzFdKjcpKQogICAgc2VlbiA9IHtpZGVu
dH07IGZyb250aWVyID0gW2lkZW50XQogICAgd2hpbGUgZnJvbnRpZXI6CiAgICAgICAgbmV3ID0g
W10KICAgICAgICBmb3IgeCBpbiBmcm9udGllcjoKICAgICAgICAgICAgZm9yIGdfIGluIGdlbnM6
CiAgICAgICAgICAgICAgICB6ID0gc2NvbXBvc2UoeCwgZ18pCiAgICAgICAgICAgICAgICBpZiB6
IG5vdCBpbiBzZWVuOiBzZWVuLmFkZCh6KTsgbmV3LmFwcGVuZCh6KQogICAgICAgIGZyb250aWVy
ID0gbmV3CiAgICBncm91cCA9IGxpc3Qoc2VlbikKICAgIFQyWyJncm91cDEzNDRfb3JkZXIiXSA9
IGxlbihncm91cCkKICAgIFQyWyJjb250cm9sXzEzNDRfYWxsX2F1dG9tb3JwaGlzbXMiXSA9IGFs
bChpc19hdXRfc2lnbmVkKHtpKzE6IHhbMF1baV0gZm9yIGkgaW4gcmFuZ2UoNyl9LCB7aSsxOiB4
WzFdW2ldIGZvciBpIGluIHJhbmdlKDcpfSkgZm9yIHggaW4gZ3JvdXApCiAgICAjIGNyb3NzLWNo
ZWNrIHRoZSBmYXN0IHRlc3QgYWdhaW5zdCB0aGUgbWF0cml4IHRlc3Qgb24gYSBzYW1wbGUKICAg
IGFzc2VydCBhbGwoaXNfYXV0KHNtYXQoeCkpIGZvciB4IGluIGdyb3VwWzo1XSkKICAgIFJbIl9n
cm91cDEzNDQiXSA9IGdyb3VwOyBSWyJfc2NvbXBvc2UiXSA9IHNjb21wb3NlOyBSWyJfbGlmdHNf
b2YiXSA9IGxpZnRzX29mOyBSWyJfaWRlbnQiXSA9IGlkZW50CiAgICBUMlsiaG9sZHMiXSA9IGJv
b2woVDJbImRpbV9nMl9jYXBfc3U0Il0gPT0gOCBhbmQgVDJbImcyX2luX3NwaW43Il0gYW5kIFQy
WyJzcGlub3JfMk9fYXV0b21vcnBoaXNtX2NvdW50Il0gPD0gMSBhbmQKICAgICAgICAgICAgICAg
ICAgICAgICBUMlsic3Bpbm9yXzJPX21pbl9hdXRvbW9ycGhpc21fZGVmZWN0Il0gPiAxZS02IGFu
ZCAxIG5vdCBpbiBUMlsibnU0X2FsbG93ZWQiXSBhbmQgVDJbImludm9sdXRpb25fdHJhY2UiXSA9
PSAtMSBhbmQKICAgICAgICAgICAgICAgICAgICAgICBUMlsic2lnbWFfSF9pc19hdXRvbW9ycGhp
c20iXSBhbmQgbm90IFQyWyJzaW5nbGVfdW5pdF9uZWdhdGlvbl9pc19hdXRvbW9ycGhpc20iXSBh
bmQgVDJbInNsMjdfc3ExX2NvdW50Il0gPT0gMikKICAgIFJbIlQyIl0gPSBUMgoKICAgICMgLS0t
LS0tLS0tLS0tLS0tLSBUMyAoZXhhY3Qtc2VxdWVuY2UgYm9va2tlZXBpbmcgd2l0aCBhZG9wdGVk
IGlucHV0czsgc3RyaW5ncyBmb3IgZ3JvdXBzKQogICAgVDMgPSB7fQogICAgYWRvcHRlZCA9IHsi
cGkxX1NVMyI6ICIwIiwgInBpM19TVTMiOiAiWiIsICJwaTRfU1UzIjogIjAiLCAicGlfa19TNl9r
X2xlXzUiOiAiMCIsICJwaTRfU1UyIjogIloyIiwgInBpM19VMSI6ICIwIiwgInBpNF9VMSI6ICIw
IiwKICAgICAgICAgICAgICAgInBpMV9TTzMiOiAiWjIiLCAicGkyX1M2IjogIjAiLCAicGlfa19T
MTVfa19sdF8xNSI6ICIwIn0KICAgICMgU1UoMykgLT4gRzIgLT4gUzYgOiBwaV9rKFNVMykgLT4g
cGlfayhHMikgLT4gcGlfayhTNikKICAgIFQzWyJwaTFfRzIiXSA9IDAgaWYgKGFkb3B0ZWRbInBp
MV9TVTMiXSA9PSAiMCIgYW5kIGFkb3B0ZWRbInBpX2tfUzZfa19sZV81Il0gPT0gIjAiKSBlbHNl
IC0xCiAgICBUM1sicGk0X0cyIl0gPSAwIGlmIChhZG9wdGVkWyJwaTRfU1UzIl0gPT0gIjAiIGFu
ZCBhZG9wdGVkWyJwaV9rX1M2X2tfbGVfNSJdID09ICIwIikgZWxzZSAtMQogICAgVDNbInBpM19H
MiJdID0gIloiIGlmIChhZG9wdGVkWyJwaTNfU1UzIl0gPT0gIloiIGFuZCBhZG9wdGVkWyJwaV9r
X1M2X2tfbGVfNSJdID09ICIwIikgZWxzZSAiPyIgICAjIHBpNChTNik9MCAtPiBwaTMoU1UzKSAt
PiBwaTMoRzIpIC0+IHBpMyhTNik9MAogICAgVDNbInBpMV9WIl0gPSAwOyBUM1sicGk0X1YiXSA9
IDAgICAgICAjIFYgPSBTMTUKICAgIFQzWyJub19pbnRlcm5hbF9kb3VibGVfY292ZXIiXSA9IGJv
b2woVDNbInBpMV9HMiJdID09IDAgYW5kIFAwWyJwaGFzZV9zdWJncm91cF9vcmRlciJdIDwgMTAq
KjkpCiAgICBUM1siZW52ZWxvcGVfaW5fT19raWxsIl0gPSBhZG9wdGVkWyJwaTJfUzYiXSA9PSAi
MCIgICAjIFMyIC0+IFM2IG51bGwtaG9tb3RvcGljID0+IHBpNCBtYXAgemVybwogICAgIyBsb2Nr
aW5nIGludmVudG9yeSBxdW90aWVudHM6IHBpNChHMi9IMCkgPSBjb2tlcihwaTQgSDAgLT4gcGk0
IEcyKSArIGtlcihwaTMgSDAgLT4gcGkzIEcyKTsgcGk0KEcyKT0wOyBwaTMgbWFwID0gaW5kZXgg
KDEpID0+IGluamVjdGl2ZQogICAgZm9yIGl0ZW0gaW4gUDBbImxvY2tpbmdfaW52ZW50b3J5Il06
CiAgICAgICAgaXRlbVsicGkzX2luamVjdGl2ZSJdID0gaXRlbVsic2wyX2dlbmVyYXRvcl9pbmRl
eCJdICE9IDAKICAgICAgICBpdGVtWyJwaTRfcXVvdGllbnQiXSA9IDAgaWYgKFQzWyJwaTRfRzIi
XSA9PSAwIGFuZCBpdGVtWyJwaTNfaW5qZWN0aXZlIl0pIGVsc2UgLTEKICAgICMgY29udHJvbHMK
ICAgIFQzWyJjb250cm9sc19waTRfUzIiXSA9ICJaMiIgaWYgKGFkb3B0ZWRbInBpNF9TVTIiXSA9
PSAiWjIiIGFuZCBhZG9wdGVkWyJwaTNfVTEiXSA9PSAiMCIgYW5kIGFkb3B0ZWRbInBpNF9VMSJd
ID09ICIwIikgZWxzZSAiPyIKICAgIFQzWyJjb250cm9sc19waTRfUzMiXSA9IGFkb3B0ZWRbInBp
NF9TVTIiXQogICAgVDNbImNvbnRyb2xzX3BpMV9TTzNfbW9kX1QiXSA9IDIgKiAxMiBpZiBhZG9w
dGVkWyJwaTFfU08zIl0gPT0gIloyIiBlbHNlIC0xCiAgICBUM1siaG9sZHMiXSA9IGJvb2woVDNb
InBpNF9WIl0gPT0gMCBhbmQgVDNbInBpMV9WIl0gPT0gMCBhbmQgVDNbIm5vX2ludGVybmFsX2Rv
dWJsZV9jb3ZlciJdIGFuZCBUM1siZW52ZWxvcGVfaW5fT19raWxsIl0gYW5kCiAgICAgICAgICAg
ICAgICAgICAgICAgYWxsKGl0WyJwaTRfcXVvdGllbnQiXSA9PSAwIGZvciBpdCBpbiBQMFsibG9j
a2luZ19pbnZlbnRvcnkiXSkpCiAgICBUM1siX2Fkb3B0ZWQiXSA9IGFkb3B0ZWQKICAgIFJbIlQz
Il0gPSBUMwoKICAgICMgLS0tLS0tLS0tLS0tLS0tLSBUNAogICAgVDQgPSB7fQogICAgZml4ZXJz
ID0gW20gZm9yIG0gaW4gY29sbHMgaWYgbVsxXSA9PSAxIGFuZCBtWzJdID09IDIgYW5kIG1bNF0g
PT0gNCBhbmQgYW55KG1beF0gIT0geCBmb3IgeCBpbiAoMywgNSwgNiwgNykpXQogICAgYXNzZXJ0
IGxlbihmaXhlcnMpID09IDMKICAgIGxpZnRzX29mID0gUlsiX2xpZnRzX29mIl07IHNjb21wb3Nl
ID0gUlsiX3Njb21wb3NlIl07IGlkZW50ID0gUlsiX2lkZW50Il0KICAgIGRlZiBzb3JkZXIoeCk6
CiAgICAgICAgaywgY3VyID0gMSwgeAogICAgICAgIHdoaWxlIGN1ciAhPSBpZGVudDogY3VyID0g
c2NvbXBvc2UoeCwgY3VyKTsgayArPSAxCiAgICAgICAgcmV0dXJuIGsKICAgIGxpZnRzID0gW10K
ICAgIGZvciBtIGluIGZpeGVyczoKICAgICAgICBmb3IgeCBpbiBsaWZ0c19vZihtKToKICAgICAg
ICAgICAgbGlmdHMuYXBwZW5kKChzb3JkZXIoeCksIGludChzdW0oeFsxXVtpXSBmb3IgaSBpbiBy
YW5nZSg3KSBpZiB4WzBdW2ldID09IGkrMSkpKSkKICAgIFQ0WyJsaWZ0c190b3RhbCJdID0gbGVu
KGxpZnRzKQogICAgVDRbIm9yZGVyMl9jb3VudCJdID0gc3VtKDEgZm9yIG8sIHQgaW4gbGlmdHMg
aWYgbyA9PSAyKTsgVDRbIm9yZGVyMl90cmFjZXNfc2V0Il0gPSBzb3J0ZWQoe3QgZm9yIG8sIHQg
aW4gbGlmdHMgaWYgbyA9PSAyfSkKICAgIFQ0WyJvcmRlcjRfY291bnQiXSA9IHN1bSgxIGZvciBv
LCB0IGluIGxpZnRzIGlmIG8gPT0gNCk7IFQ0WyJvcmRlcjRfdHJhY2VzX3NldCJdID0gc29ydGVk
KHt0IGZvciBvLCB0IGluIGxpZnRzIGlmIG8gPT0gNH0pCiAgICBUNFsicGVybV9jaGFyX2ludm9s
dXRpb24iXSA9IDM7IFQ0WyJyaG82X2NoYXJfMkEiXSA9IDI7IFQ0WyJnYXAiXSA9IFQ0WyJwZXJt
X2NoYXJfaW52b2x1dGlvbiJdIC0gVDRbIm9yZGVyMl90cmFjZXNfc2V0Il1bMF0gaWYgVDRbIm9y
ZGVyMl90cmFjZXNfc2V0Il0gZWxzZSBOb25lCiAgICBvazIxLCBudTJvaywgXywgXyA9IEYyMV9j
aGVjayhjb2xscykKICAgIFQ0WyJjb250cm9sX0YyMV91bnNpZ25lZF8xXzNfM2JhciJdID0gYm9v
bChvazIxKTsgVDRbIm51Ml91bnNpZ25lZF9hdXRvbW9ycGhpc20iXSA9IGJvb2wobnUyb2spCiAg
ICBUNFsiX3Vuc2lnbmVkX2F1dG9tb3JwaGlzbV9jb3VudF9vZl8xNjgiXSA9IGxlbih1bnNpZ25l
ZF9hdXRvbW9ycGhpc21zKGNvbGxzKSkKICAgIFQ0WyJob2xkcyJdID0gYm9vbChUNFsib3JkZXIy
X3RyYWNlc19zZXQiXSA9PSBbLTFdIGFuZCBUNFsibGlmdHNfdG90YWwiXSA9PSAyNCBhbmQgVDRb
ImdhcCJdID09IDQpCiAgICBSWyJUNCJdID0gVDQKCiAgICAjIC0tLS0tLS0tLS0tLS0tLS0gZ3Jv
dXAxMzQ0IHNwbGl0L25vbi1zcGxpdCAoRS1BMS02KGEpKQogICAgRzEzNDQgPSBSWyJfZ3JvdXAx
MzQ0Il0KICAgIGtlcm5lbCA9IFt4IGZvciB4IGluIEcxMzQ0IGlmIHhbMF0gPT0gdHVwbGUocmFu
Z2UoMSwgOCkpXQogICAgYXNzZXJ0IGxlbihrZXJuZWwpID09IDgKICAgIGRlZiBwZXJtX29yZGVy
KG0pOgogICAgICAgIGssIGN1ciA9IDEsIGRpY3QobSkKICAgICAgICB3aGlsZSBhbnkoY3VyW3hd
ICE9IHggZm9yIHggaW4gcmFuZ2UoMSwgOCkpOiBjdXIgPSBjb21wb3NlKG0sIGN1cik7IGsgKz0g
MQogICAgICAgIHJldHVybiBrCiAgICBkZWYgaW52X3Blcm0obSk6IHJldHVybiB7djogayBmb3Ig
aywgdiBpbiBtLml0ZW1zKCl9CiAgICBhID0gYV9pbnY7IGJfZm91bmQgPSBOb25lCiAgICBmb3Ig
YiBpbiBjb2xsczoKICAgICAgICBpZiBwZXJtX29yZGVyKGIpICE9IDM6IGNvbnRpbnVlCiAgICAg
ICAgYWIgPSBjb21wb3NlKGEsIGIpCiAgICAgICAgY29tbSA9IGNvbXBvc2UoY29tcG9zZShhLCBi
KSwgY29tcG9zZShpbnZfcGVybShhKSwgaW52X3Blcm0oYikpKQogICAgICAgIGlmIHBlcm1fb3Jk
ZXIoYWIpID09IDcgYW5kIHBlcm1fb3JkZXIoY29tbSkgPT0gNDogYl9mb3VuZCA9IGI7IGJyZWFr
CiAgICBhc3NlcnQgYl9mb3VuZCBpcyBub3QgTm9uZQogICAgbGlmdHNfYSA9IGxpZnRzX29mKGEp
OyBsaWZ0c19iID0gbGlmdHNfb2YoYl9mb3VuZCk7IGFzc2VydCBsZW4obGlmdHNfYSkgPT0gOCBh
bmQgbGVuKGxpZnRzX2IpID09IDgKICAgIGRlZiBnZW5fb3JkZXIoZ3MpOgogICAgICAgIHNlZW4g
PSB7aWRlbnR9OyBmcm9udGllciA9IFtpZGVudF0KICAgICAgICB3aGlsZSBmcm9udGllcjoKICAg
ICAgICAgICAgbmV3ID0gW10KICAgICAgICAgICAgZm9yIHggaW4gZnJvbnRpZXI6CiAgICAgICAg
ICAgICAgICBmb3IgZ18gaW4gZ3M6CiAgICAgICAgICAgICAgICAgICAgeiA9IHNjb21wb3NlKHgs
IGdfKQogICAgICAgICAgICAgICAgICAgIGlmIHogbm90IGluIHNlZW46IHNlZW4uYWRkKHopOyBu
ZXcuYXBwZW5kKHopCiAgICAgICAgICAgIGZyb250aWVyID0gbmV3CiAgICAgICAgcmV0dXJuIGxl
bihzZWVuKQogICAgY29tcHMgPSAwOyBwYWlycyA9IDA7IG9yZGVycyA9IHt9CiAgICBmb3IgQV8g
aW4gbGlmdHNfYToKICAgICAgICBmb3IgQl8gaW4gbGlmdHNfYjoKICAgICAgICAgICAgbyA9IGdl
bl9vcmRlcihbQV8sIEJfXSk7IHBhaXJzICs9IDE7IG9yZGVyc1tvXSA9IG9yZGVycy5nZXQobywg
MCkgKyAxCiAgICAgICAgICAgIGlmIG8gPT0gMTY4OiBjb21wcyArPSAxCiAgICBSWyJncm91cDEz
NDQiXSA9IHsib3JkZXIiOiBsZW4oRzEzNDQpLCAic3BsaXQiOiBjb21wcyA+IDAsICJjb21wbGVt
ZW50c19mb3VuZCI6IGNvbXBzLCAibGlmdF9wYWlyc190ZXN0ZWQiOiBwYWlycywgIl9vcmRlcnNf
c2VlbiI6IHtzdHIoayk6IHYgZm9yIGssIHYgaW4gb3JkZXJzLml0ZW1zKCl9fQogICAgcmV0dXJu
IFIKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gUGhhc2UgMWIKZGVmIHBoYXNlMWIoUDEpOgogICAg
QiA9IHt9CiAgICAjIFAtQzogdGhlIGNvbXBsZXggdW5pdCBvZiBD4oqXTyBjb21tdXRlcyB3aXRo
IGV2ZXJ5IExfYSAoYXMgcmVhbCAxNngxNiBtYXBzOiBMX2Eg4oqXIEkyIHZzIEk4IOKKlyBKMikK
ICAgIEwgPSB7YTogTG1hdChhKSBmb3IgYSBpbiByYW5nZSgxLCA4KX0KICAgIEoyID0gc3AuTWF0
cml4KFtbMCwgLTFdLCBbMSwgMF1dKTsgSTIgPSBzcC5leWUoMikKICAgIEpjID0gc3Aua3JvbmVj
a2VyX3Byb2R1Y3Qoc3AuZXllKDgpLCBKMikKICAgIGNlbnRyYWwgPSBhbGwoKHNwLmtyb25lY2tl
cl9wcm9kdWN0KExbYV0sIEkyKSAqIEpjIC0gSmMgKiBzcC5rcm9uZWNrZXJfcHJvZHVjdChMW2Fd
LCBJMikpID09IHNwLnplcm9zKDE2LCAxNikgZm9yIGEgaW4gcmFuZ2UoMSwgOCkpCiAgICAjIHNl
ZGVuaW9uczogQ2F5bGV5LURpY2tzb24gZG91YmxpbmcgKGEsYikoYyxkKSA9IChhYyAtIGNvbmoo
ZCkgYiwgZCBhICsgYiBjb25qKGMpKTsgZTggPSAoMCwxKQogICAgZGVmIG9jb25qKHgpOiByZXR1
cm4gW3hbMF1dICsgWy12IGZvciB2IGluIHhbMTpdXQogICAgZGVmIHNtdWwoUF8sIFFfKToKICAg
ICAgICBhLCBiID0gUF87IGMsIGQgPSBRXwogICAgICAgIGxlZnQgPSBbeCAtIHkgZm9yIHgsIHkg
aW4gemlwKG9tdWwoYSwgYyksIG9tdWwob2NvbmooZCksIGIpKV0KICAgICAgICByaWdodCA9IFt4
ICsgeSBmb3IgeCwgeSBpbiB6aXAob211bChkLCBhKSwgb211bChiLCBvY29uaihjKSkpXQogICAg
ICAgIHJldHVybiAobGVmdCwgcmlnaHQpCiAgICB6OCA9IFtzcC5JbnRlZ2VyKDApXSAqIDgKICAg
IGU4ID0gKHo4LCB1bml0KDApKQogICAgYW50aSA9IGFsbChzbXVsKGU4LCAodW5pdChhKSwgejgp
KSA9PSB0dXBsZShbLXggZm9yIHggaW4gdl0gZm9yIHYgaW4gc211bCgodW5pdChhKSwgejgpLCBl
OCkpIGZvciBhIGluIHJhbmdlKDEsIDgpKQogICAgQlsiUF9DIl0gPSB7ImNvbXBsZXhfdW5pdF9j
ZW50cmFsIjogYm9vbChjZW50cmFsKSwgImU4X2FudGljb21tdXRlcyI6IGJvb2woYW50aSksICJl
OF9jZW50cmFsIjogYm9vbChub3QgYW50aSBhbmQgRmFsc2UpIGlmIG5vdCBhbnRpIGVsc2UgRmFs
c2UsCiAgICAgICAgICAgICAgICAiZGlzcG9zaXRpb24iOiAiQ0xPU0VELUJZLUlOU1RBTlRJQVRJ
T04iIGlmIChjZW50cmFsIGFuZCBhbnRpKSBlbHNlICJPUEVOIn0KICAgIEJbIlBfQyJdWyJlOF9j
ZW50cmFsIl0gPSBGYWxzZSBpZiBhbnRpIGVsc2UgVHJ1ZQogICAgIyBIIHNjcmVlbjogY3JpdGVy
aWEgZXZhbHVhdGVkIGZyb20gdGhlIGV4YWN0L2Fkb3B0ZWQgZmFjdHM7IGNvZGUgcnVsZSAoc3Rh
dGVkIGluIHRoZSBleGVjdXRpb24gcmVwb3J0KToKICAgICMgQURNSVNTSUJMRS1JTVBPUlQgaWZm
IGksaWkgaW4ge3Bhc3N9IGFuZCBpaWkgaW4ge3Bhc3MsIGNvbmRpdGlvbmFsfSBhbmQgaXYgaW4g
e2R5bmFtaWNhbCwga2luZW1hdGljfTsgZWxzZSBFWENMVURFRCg8Y3JpdGVyaWEgd2l0aCB2YWx1
ZSAnZmFpbCcsIGluIG9yZGVyPikKICAgIGtpbGwgPSBQMVsiVDMiXVsiZW52ZWxvcGVfaW5fT19r
aWxsIl0KICAgIGxvbmdfcm9vdF8ycGx1czIgPSBQMVsiVDEiXVsiYnJhbmNoaW5nX2xvbmdfcm9v
dCJdID09IFsyLCAyLCAxLCAxLCAxXQogICAgSCA9IHsKICAgICAgICAiSDEiOiB7ImkiOiAiZmFp
bCIsICJpaSI6ICJwYXNzIiwgImlpaSI6ICJmYWlsIiBpZiBraWxsIGVsc2UgInBhc3MiLCAiaXYi
OiAibi9hIiwgInJvbGUiOiAiY29udHJvbCJ9LAogICAgICAgICJIMiI6IHsiaSI6ICJwYXNzIiwg
ImlpIjogInBhc3MiLCAiaWlpIjogInBhc3MiIGlmIFAxWyJUMyJdWyJjb250cm9sc19waTRfUzIi
XSA9PSAiWjIiIGVsc2UgImZhaWwiLCAiaXYiOiAiZHluYW1pY2FsIiwgInJvbGUiOiAiY2FuZGlk
YXRlIn0sCiAgICAgICAgIkgzIjogeyJpIjogInBhc3MiLCAiaWkiOiAicGFzcyIsICJpaWkiOiAi
Y29uZGl0aW9uYWwiLCAiaXYiOiAia2luZW1hdGljIiwgInJvbGUiOiAiY2FuZGlkYXRlIn0sCiAg
ICAgICAgIkg0IjogeyJpIjogImZhaWwiLCAiaWkiOiAicGFzcyIgaWYgbG9uZ19yb290XzJwbHVz
MiBlbHNlICJmYWlsIiwgImlpaSI6ICJuL2EiLCAiaXYiOiAibi9hIiwgInJvbGUiOiAiY2FuZGlk
YXRlIn0sCiAgICAgICAgIkg1IjogeyJpIjogImZhaWwiIGlmIGFudGkgZWxzZSAicGFzcyIsICJp
aSI6ICJmYWlsIiwgImlpaSI6ICJuL2EiLCAiaXYiOiAibi9hIiwgInJvbGUiOiAiY2FuZGlkYXRl
In0sCiAgICB9CiAgICBmb3IgaCwgZCBpbiBILml0ZW1zKCk6CiAgICAgICAgYWRtID0gZFsiaSJd
ID09ICJwYXNzIiBhbmQgZFsiaWkiXSA9PSAicGFzcyIgYW5kIGRbImlpaSJdIGluICgicGFzcyIs
ICJjb25kaXRpb25hbCIpIGFuZCBkWyJpdiJdIGluICgiZHluYW1pY2FsIiwgImtpbmVtYXRpYyIp
CiAgICAgICAgZFsiY29kZSJdID0gIkFETUlTU0lCTEUtSU1QT1JUIiBpZiBhZG0gZWxzZSAiRVhD
TFVERUQoIiArICIsIi5qb2luKGsgZm9yIGsgaW4gKCJpIiwgImlpIiwgImlpaSIsICJpdiIpIGlm
IGRba10gPT0gImZhaWwiKSArICIpIgogICAgQlsiSF9zY3JlZW4iXSA9IEgKICAgIEJbImFkbWlz
c2libGUiXSA9IHNvcnRlZChoIGZvciBoLCBkIGluIEguaXRlbXMoKSBpZiBkWyJjb2RlIl0gPT0g
IkFETUlTU0lCTEUtSU1QT1JUIikKICAgIGluc2lkZSA9IFtoIGZvciBoIGluIEJbImFkbWlzc2li
bGUiXSBpZiBoIG5vdCBpbiAoIkgyIiwgIkgzIildICAgIyBjYW5kaWRhdGVzIGluc2lkZSB0aGUg
ZmllbGQgY29udGVudCBvZiByZWNvcmQgdGhhdCBwYXNzCiAgICBCWyJJNV9yZWdpc3RlcmVkIl0g
PSBib29sKGxlbihCWyJhZG1pc3NpYmxlIl0pID4gMCBhbmQgbm90IGluc2lkZSkKICAgIHJldHVy
biBCCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIFBoYXNlIDIKZGVmIHBoYXNlMigpOgogICAgWiA9
IHsib2JqZWN0IjogImZhbm9fbGluZV90ZXh0dXJlX0wxMjRfaG9tb2dlbmVvdXNfR1BfMkQiLCAi
Y29udHJvbF9vYmplY3QiOiAibm9ubGluZV90ZXh0dXJlX0wxMjMiLCAicHJvZmlsZV9pZCI6ICJs
b2NrcmVjLUEtMi42IiwKICAgICAgICAgImRpbWVuc2lvbl9ub3RlIjogIjJEIHdpdG5lc3M7IGNv
bnRyYWN0aWJpbGl0eSBvZiB0aGUgMnBpIGxvb3AgaW4gdGhlIG9yYml0IG9ubHkifQogICAgciwg
cGggPSBzcC5zeW1ib2xzKCdyIHBoaScsIHBvc2l0aXZlPVRydWUpCiAgICBmID0gc3AucGkgLyAo
MSArIHIqKjIpCiAgICAjIE8gPSBwaGlfYWJjICogaW50ZWdyYWwgbi4oZF94IG4geCBkX3kgbikg
ZF4yeCAgKHJlYWwgdGV4dHVyZSBpbiB0aGUgMy1wbGFuZSB7YSxiLGN9KTsgdGhlIGludGVncmFs
ID0gMiBwaSAqIGludCBzaW4gZiBmJyBkciA9IDJwaVstY29zIGZdXzBeaW5mCiAgICBnZW9tID0g
MipzcC5waSooLXNwLmNvcyhmLnN1YnMociwgc3Aub28pKSArIHNwLmNvcyhmLnN1YnMociwgMCkp
KSAgICMgZXhhY3Q6IDJwaSgtMSArICgtMSkpID0gLTRwaQogICAgZ2VvbSA9IHNwLnNpbXBsaWZ5
KGdlb20pCiAgICBhc3NlcnQgZ2VvbSA9PSAtNCpzcC5waQogICAgIyBudW1lcmljIGNyb3NzLWNo
ZWNrIG9mIHRoZSBpbnRlZ3JhbCAycGkgaW50XzBeaW5mIHNpbihmKSBmJyhyKSBkcgogICAgZnIg
PSBzcC5kaWZmKGYsIHIpOyBudW0gPSBzcC5OKDIqc3AucGkqc3AuSW50ZWdyYWwoc3Auc2luKGYp
KmZyLCAociwgMCwgc3Aub28pKSwgMTUpCiAgICBhc3NlcnQgYWJzKGZsb2F0KG51bSkgLSBmbG9h
dCgtNCpzcC5waSkpIDwgMWUtOQogICAgT19saW5lID0gcGhpKDEsIDIsIDQpICogZ2VvbTsgT19u
b24gPSBwaGkoMSwgMiwgMykgKiBnZW9tCiAgICBaWyJPX2xpbmVfYWJzIl0gPSBmbG9hdChhYnMo
T19saW5lKSk7IFpbIk9fbm9ubGluZV9hYnMiXSA9IGZsb2F0KGFicyhPX25vbikpCiAgICBaWyJP
X25vbnplcm9fb25fbGluZSJdID0gYm9vbChPX2xpbmUgIT0gMCk7IFpbIk9femVyb19vbl9ub25s
aW5lIl0gPSBib29sKE9fbm9uID09IDApCiAgICAjIHN0YWJpbGl6ZXIgZmFtaWx5IE0ocCxxKTog
aCAtPiBxIGggccyEIG9uIEhfTCA9IDwxLGUxLGUyLGU0PjsgeCA9IGsgZTMgKGsgaW4gSF9MKSAt
PiAocCBrIHHMhCkgZTMgb24gSF9MXnBlcnAKICAgIEhMID0gWzAsIDEsIDIsIDRdOyBITHAgPSBb
MywgNSwgNiwgN10KICAgIGRlZiBvYyh4KTogcmV0dXJuIFt4WzBdXSArIFstdiBmb3IgdiBpbiB4
WzE6XV0KICAgIGRlZiBwcm9qKHgsIGlkeHMpOiByZXR1cm4gW3hbaV0gaWYgaSBpbiBpZHhzIGVs
c2Ugc3AuSW50ZWdlcigwKSBmb3IgaSBpbiByYW5nZSg4KV0KICAgIGRlZiBNcHEocHEsIHFxKToK
ICAgICAgICBjb2xzID0gW10KICAgICAgICBmb3IgaiBpbiByYW5nZSg4KToKICAgICAgICAgICAg
eCA9IHVuaXQoaikKICAgICAgICAgICAgaWYgaiBpbiBITDoKICAgICAgICAgICAgICAgIHkgPSBv
bXVsKG9tdWwocXEsIHgpLCBvYyhxcSkpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAg
ICBrID0gWy12IGZvciB2IGluIG9tdWwoeCwgdW5pdCgzKSldICAgICAgICAgICMgayA9IC14IGUz
ICAoc28gdGhhdCBrIGUzID0geCkKICAgICAgICAgICAgICAgIGFzc2VydCBvbXVsKGssIHVuaXQo
MykpID09IHgKICAgICAgICAgICAgICAgIHkgPSBvbXVsKG9tdWwob211bChwcSwgayksIG9jKHFx
KSksIHVuaXQoMykpCiAgICAgICAgICAgIGNvbHMuYXBwZW5kKHkpCiAgICAgICAgcmV0dXJuIHNw
Lk1hdHJpeChjb2xzKS5UCiAgICBkZWYgdW5pdF9xdWF0X2U0KHQpOiAgICMgcmF0aW9uYWwgcG9p
bnQgb24gdGhlIGNpcmNsZTogcSA9IGMgKyBzIGU0CiAgICAgICAgYyA9ICgxIC0gdCoqMikgLyAo
MSArIHQqKjIpOyBzID0gMip0IC8gKDEgKyB0KioyKQogICAgICAgIHYgPSBbc3AuSW50ZWdlcigw
KV0gKiA4OyB2WzBdID0gYzsgdls0XSA9IHM7IHJldHVybiB2CiAgICBkZWYgdW5pdF9xdWF0X2dl
bih0MSwgdDIpOiAgICMgYSBnZW5lcmljIHJhdGlvbmFsIHVuaXQgaW4gSF9MIHZpYSBzdGVyZW9n
cmFwaGljLWxpa2UgcGFyYW1ldHJpemF0aW9uCiAgICAgICAgZCA9IDEgKyB0MSoqMiArIHQyKioy
CiAgICAgICAgdiA9IFtzcC5JbnRlZ2VyKDApXSAqIDg7IHZbMF0gPSAoMSAtIHQxKioyIC0gdDIq
KjIpL2Q7IHZbMV0gPSAyKnQxL2Q7IHZbMl0gPSAyKnQyL2QKICAgICAgICBhc3NlcnQgc3VtKHgq
eCBmb3IgeCBpbiB2KSA9PSAxCiAgICAgICAgcmV0dXJuIHYKICAgIG9uZSA9IHVuaXQoMCk7IG1p
bnVzID0gWy14IGZvciB4IGluIG9uZV0KICAgIGNoZWNrcyA9IFtdCiAgICBmb3IgdCBpbiAoc3Au
UmF0aW9uYWwoMSwgMyksIHNwLlJhdGlvbmFsKDIsIDUpKToKICAgICAgICBxID0gdW5pdF9xdWF0
X2U0KHQpCiAgICAgICAgZm9yIHBuYW1lLCBwcCBpbiAoKCIxIiwgb25lKSwgKCItMSIsIG1pbnVz
KSwgKCJxIiwgcSksICgiZ2VuZXJpYyIsIHVuaXRfcXVhdF9nZW4oc3AuUmF0aW9uYWwoMSwgMiks
IHNwLlJhdGlvbmFsKC0xLCAzKSkpKToKICAgICAgICAgICAgTSA9IE1wcShwcCwgcSkKICAgICAg
ICAgICAgY2hlY2tzLmFwcGVuZCgoc3RyKHQpLCBwbmFtZSwgaXNfYXV0KE0pKSkKICAgICAgICAg
ICAgIyB0ZXh0dXJlIGludmFyaWFuY2U6IE0gcm90YXRlcyBJbSBIX0wgYWJvdXQgZTQgYnkgYWxw
aGEgd2l0aCBjb3MgYSA9IGNeMiAtIHNeMiwgc2luIGEgPSAyY3MKICAgICAgICAgICAgYyA9IHFb
MF07IHMgPSBxWzRdOyBjYSA9IGMqYyAtIHMqczsgc2EgPSAyKmMqcwogICAgICAgICAgICBuID0g
W3NwLkludGVnZXIoMCldICogODsgblsxXSA9IHNwLlJhdGlvbmFsKDMsIDUpOyBuWzJdID0gc3Au
UmF0aW9uYWwoNCwgNSkgICAjIGEgcG9pbnQgb24gdGhlIHRleHR1cmUgc3BoZXJlIChjb3MgZiA9
IDAgc2xpY2UpCiAgICAgICAgICAgIE1uID0gTSAqIHNwLk1hdHJpeChuKQogICAgICAgICAgICBl
eHBlY3QgPSBbc3AuSW50ZWdlcigwKV0gKiA4OyBleHBlY3RbMV0gPSBjYSpuWzFdIC0gc2Eqblsy
XTsgZXhwZWN0WzJdID0gc2EqblsxXSArIGNhKm5bMl0KICAgICAgICAgICAgYXNzZXJ0IGxpc3Qo
TW4pID09IGV4cGVjdCwgInJvdGF0aW9uIGxhdyBmYWlsZWQiCiAgICBhc3NlcnQgYWxsKG9rIGZv
ciBfLCBfLCBvayBpbiBjaGVja3MpCiAgICAjIGtlcm5lbCBTVSgyKV9sb25nOiBNKHAsIDEpIGZp
eGVzIEhfTCBwb2ludHdpc2UgYW5kIGlzIGFuIGF1dG9tb3JwaGlzbQogICAgTWsgPSBNcHEodW5p
dF9xdWF0X2dlbihzcC5SYXRpb25hbCgyLCAzKSwgc3AuUmF0aW9uYWwoMSwgNSkpLCBvbmUpCiAg
ICBhc3NlcnQgaXNfYXV0KE1rKSBhbmQgYWxsKE1rWzosIGpdID09IHNwLk1hdHJpeCh1bml0KGop
KSBmb3IgaiBpbiBITCkKICAgIFpbInN0YWJfaW50ZXJuYWxfaW1hZ2UiXSA9ICJTTzRfU3RhYl9I
TCI7IFpbInN0YWJfa2VybmVsIl0gPSAiU1UyX2xvbmciOyBaWyJzdGFiX3N1YmRpcmVjdCJdID0g
VHJ1ZQogICAgWlsicGkwX3N0YWIiXSA9IDEgICAjIHRoZSBmYW1pbHkgKGFscGhhLCBwKSBpcyBj
b25uZWN0ZWQ7IG5vIG90aGVyIGVsZW1lbnQgb2YgU08oMil4RzIgZml4ZXMgdGhlIHRleHR1cmUg
KHZhbHVlcyBvZiBuIHNwYW4gSW0gSF9MKQogICAgIyBsb29wIGltYWdlcyBhdCBhbHBoYSA9IDJw
aTogcSA9IC0xIDogKHA9MSkgLT4gc2lnbWFfSCA7IChwPS0xKSAtPiBJZAogICAgTTEgPSBNcHEo
b25lLCBtaW51cyk7IE0yID0gTXBxKG1pbnVzLCBtaW51cykKICAgIHNpZyA9IHNwLmRpYWcoKihb
MV0gKyBbMSBpZiBpIGluICgxLCAyLCA0KSBlbHNlIC0xIGZvciBpIGluIHJhbmdlKDEsIDgpXSkp
CiAgICBhc3NlcnQgTTEgPT0gc2lnIGFuZCBNMiA9PSBzcC5leWUoOCkKICAgIFpbImxvb3BfaW1h
Z2VzIl0gPSBbIklkIiwgInNpZ21hX0giXQogICAgZXYgPSBzaWcuZWlnZW52YWxzKCk7IFpbInNp
Z21hX0hfZWlnZW5fcGx1czEiXSA9IGludChldlsxXSk7IFpbInNpZ21hX0hfZWlnZW5fbWludXMx
Il0gPSBpbnQoZXZbLTFdKQogICAgWlsibGFiZWwiXSA9ICJJTlRFUk5BTC1IT0xPTk9NWS1HQVVH
RSIKICAgICMgcGkxKE9yYml0KSA9IHBpMChTdGFiKSBzaW5jZSB0aGUgZGlhZ29uYWwgbG9vcCAo
cV9hbHBoYSwgcV9hbHBoYSkgY2xvc2VzIGF0ICgtMSwtMSkgfiBJZCBhbmQgd2luZHMgb25jZSBp
biBwaTEoU08oMikpID0gWgogICAgWlsicGkxX29yYml0Il0gPSAwIGlmIFpbInBpMF9zdGFiIl0g
PT0gMSBlbHNlIC0xCiAgICAjIGNoaXJhbCBwYWlyOiBhbnRpc3ltbWV0cmljIGNvdXBsaW5nIG9u
IHRoZSBsaW5lICgxLDIsNCkgd2l0aCBlaWdlbnZlY3RvcnMgZTEgLS8rIGkgZTI7IHJvdGF0aW9u
IGFib3V0IGU0IGFjdHMgYXMgZV57wrFpIGFscGhhfQogICAgdCA9IHNwLlJhdGlvbmFsKDEsIDMp
OyBxID0gdW5pdF9xdWF0X2U0KHQpOyBNID0gTXBxKG9uZSwgcSk7IGMgPSBxWzBdOyBzID0gcVs0
XTsgY2EgPSBjKmMgLSBzKnM7IHNhID0gMipjKnMKICAgIEEzID0gc3AuTWF0cml4KFtbMCwgMSwg
MF0sIFstMSwgMCwgMF0sIFswLCAwLCAwXV0pICogcGhpKDEsIDIsIDQpCiAgICBldnMgPSBBMy5l
aWdlbnZlY3RzKCkKICAgIG9yZGluYXJ5ID0gVHJ1ZQogICAgZm9yIHZhbCwgbSwgdmVjcyBpbiBl
dnM6CiAgICAgICAgaWYgdmFsID09IDA6IGNvbnRpbnVlCiAgICAgICAgdiA9IHZlY3NbMF07IHY4
ID0gc3AuemVyb3MoOCwgMSk7IHY4WzFdID0gdlswXTsgdjhbMl0gPSB2WzFdOyB2OFs0XSA9IHZb
Ml0KICAgICAgICB3ID0gTSAqIHY4CiAgICAgICAgbGFtID0gc3Auc2ltcGxpZnkod1sxXSAvIHY4
WzFdKSBpZiB2OFsxXSAhPSAwIGVsc2Ugc3Auc2ltcGxpZnkod1syXSAvIHY4WzJdKQogICAgICAg
IGFzc2VydCBzcC5zaW1wbGlmeSh3IC0gbGFtKnY4KSA9PSBzcC56ZXJvcyg4LCAxKQogICAgICAg
IG9yZGluYXJ5ID0gb3JkaW5hcnkgYW5kIHNwLnNpbXBsaWZ5KHNwLkFicyhsYW0pIC0gMSkgPT0g
MCBhbmQgKHNwLnNpbXBsaWZ5KGxhbSAtIChjYSArIHNwLkkqc2EpKSA9PSAwIG9yIHNwLnNpbXBs
aWZ5KGxhbSAtIChjYSAtIHNwLkkqc2EpKSA9PSAwKQogICAgWlsiY2hpcmFsX3BhaXJfY2hhcmFj
dGVyX29yZGluYXJ5Il0gPSBib29sKG9yZGluYXJ5KQogICAgWlsiX2NoZWNrcyJdID0gY2hlY2tz
CiAgICByZXR1cm4gWgoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBQaGFzZSAzCmRlZiBwaGFzZTMo
UDAsIFAxLCBCLCBaKToKICAgIGhvbGRzID0ge3Q6IFAxW3RdWyJob2xkcyJdIGZvciB0IGluICgi
VDEiLCAiVDIiLCAiVDMiLCAiVDQiKX0KICAgIGMwID0gUDBbImNvbnRyb2xzIl0KICAgIGNvbnRy
b2xzID0gYWxsKGMwW2tdIGlzIFRydWUgZm9yIGsgaW4gKCJMX3BlcnBfemVyb19tb2RlIiwgIkYy
MV9zcGxpdF8xXzNfM2JhciIsICJnZW5lcmljX3NvMTZfZmFpbHNfbWFyZ2luX3Bvc2l0aXZlIikp
CiAgICBjb250cm9scyA9IGNvbnRyb2xzIGFuZCBQMVsiVDEiXVsiY29udHJvbF9zeW0zX3F1YXJ0
ZXRfbXVsdCJdID09IDEgYW5kIFAxWyJUMiJdWyJjb250cm9sXzEzNDRfYWxsX2F1dG9tb3JwaGlz
bXMiXSBpcyBUcnVlIGFuZCBQMVsiVDIiXVsic3Bpbm9yXzJPX3F1YXJ0ZXRfbXVsdCJdID09IDIK
ICAgIGNvbnRyb2xzID0gY29udHJvbHMgYW5kIFAxWyJUMyJdWyJjb250cm9sc19waTRfUzIiXSA9
PSAiWjIiIGFuZCBQMVsiVDMiXVsiY29udHJvbHNfcGk0X1MzIl0gPT0gIloyIiBhbmQgUDFbIlQz
Il1bImNvbnRyb2xzX3BpMV9TTzNfbW9kX1QiXSA9PSAyNAogICAgY29udHJvbHMgPSBjb250cm9s
cyBhbmQgUDFbIlQ0Il1bImNvbnRyb2xfRjIxX3Vuc2lnbmVkXzFfM18zYmFyIl0gaXMgVHJ1ZSBh
bmQgUDFbIlQ0Il1bIm51Ml91bnNpZ25lZF9hdXRvbW9ycGhpc20iXSBpcyBUcnVlIGFuZCBaWyJP
X3plcm9fb25fbm9ubGluZSJdIGlzIFRydWUKICAgIGlmIG5vdCBjb250cm9sczogdmVyZGljdCA9
ICJJTkRFVEVSTUlOQVRFIgogICAgZWxpZiBub3QgUDBbInN5bV9pbnRfcGlubmVkIl06IHZlcmRp
Y3QgPSAiVU5ERUNJREVELUJZLVNVQlNUUkFURSIKICAgIGVsaWYgKG5vdCBQMFsic3BhdGlhbF9p
bnRlcm5hbF9kaXJlY3RfcHJvZHVjdCJdKSBvciBhbnkoaCBpcyBub3QgVHJ1ZSBmb3IgaCBpbiBo
b2xkcy52YWx1ZXMoKSk6IHZlcmRpY3QgPSAiQVNTSUdOTUVOVC1JSS1SRUFMSVpBQkxFIgogICAg
ZWxzZTogdmVyZGljdCA9ICJBU1NJR05NRU5ULUktRk9SQ0VEIgogICAgcmV0dXJuIHsidmVyZGlj
dCI6IHZlcmRpY3QsICJ0ZXN0c19ob2xkaW5nIjogc29ydGVkKHQgZm9yIHQsIGggaW4gaG9sZHMu
aXRlbXMoKSBpZiBoIGlzIFRydWUpLCAiYWRtaXNzaWJsZV9IIjogbGlzdChCWyJhZG1pc3NpYmxl
Il0pLAogICAgICAgICAgICAiSTUiOiBib29sKEJbIkk1X3JlZ2lzdGVyZWQiXSksICJjb250cm9s
c19hbGxfcGFzcyI6IGJvb2woY29udHJvbHMpfQoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBydW4K
ZGVmIHN0cmlwX3ByaXZhdGUoZCk6CiAgICBpZiBpc2luc3RhbmNlKGQsIGRpY3QpOiByZXR1cm4g
e2s6IHN0cmlwX3ByaXZhdGUodikgZm9yIGssIHYgaW4gZC5pdGVtcygpIGlmIG5vdCBrLnN0YXJ0
c3dpdGgoIl8iKX0KICAgIGlmIGlzaW5zdGFuY2UoZCwgbGlzdCk6IHJldHVybiBbc3RyaXBfcHJp
dmF0ZSh4KSBmb3IgeCBpbiBkXQogICAgcmV0dXJuIGQKCkNJVEFUSU9OUyA9IHsKICAgICJwaV9r
KFNVMyksIHBpX2soUzYpLCBwaTQoU1UyKSwgcGlfayhVMSksIHBpX2soUzE1KSI6ICJ0ZXh0Ym9v
ayBob21vdG9weSAoQm90dCBwZXJpb2RpY2l0eSAvIHN0YWJsZSByYW5nZTsgSGF0Y2hlciwgQWxn
ZWJyYWljIFRvcG9sb2d5LCBjaC4gNCk7IE1pbXVyYSAxOTY3IEouIE1hdGguIEt5b3RvIFVuaXYu
IDYgYXMgdGhlIGNhbm9uaWNhbCBHMiB0YWJsZSAobm90IHJlbGllZCBvbikiLAogICAgIkZSIGNy
aXRlcmlvbiBwaTEoQ29uZmlnKT1waTQodGFyZ2V0KSI6ICJGaW5rZWxzdGVpbi1SdWJpbnN0ZWlu
IDE5Njg7IEdpdWxpbmkgMTk5MyAoaGVwLXRoLzkzMDExMDEpOyBLcnVzY2gtU3BlaWdodCAyMDA2
IChoZXAtdGgvMDUwMzA2NykiLAogICAgImV2ZW4gbXVsdGlwbGljaXR5IG9mIHF1YXRlcm5pb25p
YyBpcnJlcHMgaW4gcmVhbCByZXByZXNlbnRhdGlvbnMiOiAic3RhbmRhcmQgKEZyb2Jlbml1cy1T
Y2h1ciB0aGVvcnk7IFNlcnJlLCBMaW5lYXIgUmVwcmVzZW50YXRpb25zIG9mIEZpbml0ZSBHcm91
cHMsIMKnMTMuMikiLAogICAgIlBTTCgyLDcpIG9yZGluYXJ5IGluZGljYXRvcnMgbnUoMyk9bnUo
M2Jhcik9MCwgbnUoOCk9KzE7IFNMKDIsNykgR2Fsb2lzIHBhaXJpbmdzIjogIkFUTEFTIG9mIEZp
bml0ZSBHcm91cHM7IGxlZGdlciDCpzIuNzcgLyDCpzIuRC1GQyAodGhlIDYgYW5kIDcgbWFjaGlu
ZS12ZXJpZmllZCBoZXJlKSIsCiAgICAidHdvIFBTTCgyLDcpIGNsYXNzZXMgaW4gRzI7IG5vbi1z
cGxpdCAyXjMuUFNMKDIsNykiOiAiQ29oZW4tV2FsZXMgMTk4MyB2aWEgRXZhbnMtUHVnaCBhclhp
djoxNDA0LjE4NjYgVGFibGUgMSAoY3Jvc3MtY2hlY2sgb25seSkiLAogICAgIlNVKDMpPVN0YWJf
RzIoZTcpLCBHMi9TVSgzKT1TNiwgRml4X0cyKEgpPVNVKDIpIjogIkfDvG5heWRpbi1Hw7xyc2V5
IDE5NzM7IG5MYWIgRzIiLAp9CgpkZWYgbWFpbigpOgogICAgaWYgbGVuKHN5cy5hcmd2KSA8IDIg
b3Igc3lzLmFyZ3ZbMV0gbm90IGluICgicnVuIiwgInNlbGZ0ZXN0Iik6IHByaW50KF9fZG9jX18p
OyByZXR1cm4gMgogICAgb3V0ID0gIi4iCiAgICBpZiAiLS1vdXQiIGluIHN5cy5hcmd2OiBvdXQg
PSBzeXMuYXJndltzeXMuYXJndi5pbmRleCgiLS1vdXQiKSArIDFdCiAgICB0MCA9IHRpbWUudGlt
ZSgpOyBsb2cgPSBbXQogICAgc2NhbiwgZ2xvZyA9IGd1YXJkcygpOyBsb2cgKz0gZ2xvZwogICAg
aW5zdF9tZDUgPSBtZDVfZmlsZShvcy5wYXRoLmFic3BhdGgoX19maWxlX18pKQogICAgZXh0cmFj
dF90ZXh0ID0gb3BlbihFWFRSQUNULCBlbmNvZGluZz0idXRmLTgiKS5yZWFkKCkKICAgIGlmIHN5
cy5hcmd2WzFdID09ICJzZWxmdGVzdCI6CiAgICAgICAgcHJpbnQoIlxuIi5qb2luKGxvZykpOyBw
cmludCgiZ3VhcmRzIE9LOyBzZWxmdGVzdCA9IGd1YXJkcyBvbmx5IChhbGwgY29tcHV0YXRpb25z
IGFyZSB0aGUgcnVuKSIpOyByZXR1cm4gMAogICAgZzIgPSBkZXJpdmF0aW9uX2FsZ2VicmEoKTsg
YXNzZXJ0IGxlbihnMikgPT0gMTQ7IGxvZy5hcHBlbmQoZiJnMiBidWlsdDogZGltIHtsZW4oZzIp
fSAgW3t0aW1lLnRpbWUoKS10MDouMWZ9c10iKQogICAgUDAgPSBwaGFzZTAoZzIsIGV4dHJhY3Rf
dGV4dCk7IGxvZy5hcHBlbmQoZiJQaGFzZSAwIGRvbmUgIFt7dGltZS50aW1lKCktdDA6LjFmfXNd
ICBzeW1faW50X2NvbnRpbnVvdXM9e1AwWydzeW1faW50X2NvbnRpbnVvdXMnXX0gZGltPXtQMFsn
c3ltX2ludF9jb250aW51b3VzX2RpbSddfSAoaW1hZ2luYXJ5IHNlY3RvciB7UDBbJ19pbWFnX3Nl
Y3Rvcl9jb250aW51b3VzX2RpbSddfTsgcHNpMCBwaGFzZSBwcmVzZXJ2ZXMgTzoge1AwWydfcHNp
MF9waGFzZV9wcmVzZXJ2ZXNfTyddfSkgcGlubmVkPXtQMFsnc3ltX2ludF9waW5uZWQnXX0iKQog
ICAgY29sbHMgPSBmYW5vX2NvbGxpbmVhdGlvbnMoKTsgb2syMSwgbnUyb2ssIF8sIF8gPSBGMjFf
Y2hlY2soY29sbHMpCiAgICBQMFsiY29udHJvbHMiXVsiRjIxX3NwbGl0XzFfM18zYmFyIl0gPSBi
b29sKG9rMjEpCiAgICBpZiBub3QgYWxsKFAwWyJjb250cm9scyJdLnZhbHVlcygpKTogcmFpc2Ug
U3lzdGVtRXhpdCgiSEFMVDogYSBQaGFzZS0wIGNvbnRyb2wgZmFpbGVkOiAiICsganNvbi5kdW1w
cyhQMFsiY29udHJvbHMiXSkpCiAgICBQMSA9IHBoYXNlMShnMiwgUDApOyBob2xkcyA9IHt0OiBQ
MVt0XVsnaG9sZHMnXSBmb3IgdCBpbiAoJ1QxJywgJ1QyJywgJ1QzJywgJ1Q0Jyl9OyBsb2cuYXBw
ZW5kKGYiUGhhc2UgMSBkb25lICBbe3RpbWUudGltZSgpLXQwOi4xZn1zXSAgaG9sZHM9e2hvbGRz
fSAgZ3JvdXAxMzQ0PXtQMVsnZ3JvdXAxMzQ0J11bJ29yZGVyJ119IHNwbGl0PXtQMVsnZ3JvdXAx
MzQ0J11bJ3NwbGl0J119IikKICAgIEIgPSBwaGFzZTFiKFAxKTsgbG9nLmFwcGVuZChmIlBoYXNl
IDFiIGRvbmUgW3t0aW1lLnRpbWUoKS10MDouMWZ9c10gIGFkbWlzc2libGU9e0JbJ2FkbWlzc2li
bGUnXX0iKQogICAgWiA9IHBoYXNlMigpOyBsb2cuYXBwZW5kKGYiUGhhc2UgMiBkb25lICBbe3Rp
bWUudGltZSgpLXQwOi4xZn1zXSAgcGkxX29yYml0PXtaWydwaTFfb3JiaXQnXX0gbG9vcF9pbWFn
ZXM9e1pbJ2xvb3BfaW1hZ2VzJ119IikKICAgIFYgPSBwaGFzZTMoUDAsIFAxLCBCLCBaKTsgbG9n
LmFwcGVuZChmIlBoYXNlIDMgZG9uZSAgW3t0aW1lLnRpbWUoKS10MDouMWZ9c10gIHZlcmRpY3Q9
e1ZbJ3ZlcmRpY3QnXX0iKQogICAgY2sgPSB7ImdhdGUiOiBHQVRFLCAibGVnIjogImNoYXQiLCAi
aW5zdHJ1bWVudF9tZDUiOiBpbnN0X21kNSwgIm1lbW9fbG9ja19tZDUiOiBNRU1PX01ENSwgImxl
ZGdlcl9iYXNlX21kNSI6IExFREdFUl9CQVNFX01ENSwKICAgICAgICAgICJ0MV9saXN0X21kNSI6
IFQxX01ENSwgImFjdGlvbl9leHRyYWN0X21kNSI6IEVYVFJBQ1RfTUQ1LCAidDFfc2NhbiI6IHNj
YW4sICJlbGVjdGlvbnMiOiBFTEVDVElPTlMsCiAgICAgICAgICAicGhhc2UwIjogc3RyaXBfcHJp
dmF0ZShQMCksICJwaGFzZTEiOiB7azogc3RyaXBfcHJpdmF0ZSh2KSBmb3IgaywgdiBpbiBQMS5p
dGVtcygpIGlmIG5vdCBrLnN0YXJ0c3dpdGgoIl8iKX0sCiAgICAgICAgICAicGhhc2UxYiI6IHN0
cmlwX3ByaXZhdGUoQiksICJwaGFzZTIiOiBzdHJpcF9wcml2YXRlKFopLCAicGhhc2UzIjogViwK
ICAgICAgICAgICJjaXRhdGlvbnMiOiBDSVRBVElPTlMsICJleHRyYXMiOiB7InBoYXNlMF9tYXJn
aW4iOiBQMFsiX21hcmdpbiJdLCAicGhhc2UwX2ltYWdfc2VjdG9yX2NvbnRpbnVvdXNfZGltIjog
UDBbIl9pbWFnX3NlY3Rvcl9jb250aW51b3VzX2RpbSJdLAogICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICJwaGFzZTBfcHNpMF9waGFzZV9wcmVzZXJ2ZXNfTyI6IFAw
WyJfcHNpMF9waGFzZV9wcmVzZXJ2ZXNfTyJdLCAicGhhc2UwX3Rlcm1zX29mX3JlY29yZCI6IFAw
WyJfdGVybXNfb2ZfcmVjb3JkIl0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgIlQyX25vdGUiOiAic3Bpbm9yXzJPX2F1dG9tb3JwaGlzbV9jb3VudCBjb3VudHMg
ZWxlbWVudHMgd2l0aCB6ZXJvIGRlZmVjdDsgdGhlIGlkZW50aXR5IGlzIG9uZSBvZiB0aGVtIChs
b2NrIHJlY29yZCBBLTIuMyB3b3JkaW5nKTsgdGhlIG1pbmltdW0gZGVmZWN0IGlzIG92ZXIgMk8g
bWludXMgeysxLC0xfSIsICJwcmluY2lwYWxfd2VpZ2h0cyI6IFAxWyJUMSJdWyJfcHJpbmNpcGFs
X3dlaWdodHMiXSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAi
ZnNfc29sdXRpb25zIjogUDFbIlQyIl1bIl9mc19zb2x1dGlvbnMiXSwgInVuc2lnbmVkX2F1dG9t
b3JwaGlzbXNfb2ZfMTY4IjogUDFbIlQ0Il1bIl91bnNpZ25lZF9hdXRvbW9ycGhpc21fY291bnRf
b2ZfMTY4Il0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgImdy
b3VwMTM0NF9vcmRlcnNfc2Vlbl9pbl9jb21wbGVtZW50X3NlYXJjaCI6IFAxWyJncm91cDEzNDQi
XVsiX29yZGVyc19zZWVuIl0sICJwaGFzZTJfYXV0b21vcnBoaXNtX2NoZWNrcyI6IFpbIl9jaGVj
a3MiXSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiYWRvcHRl
ZF9ob21vdG9weV9pbnB1dHMiOiBQMVsiVDMiXVsiX2Fkb3B0ZWQiXSwgInJ1bnRpbWVfcyI6IHJv
dW5kKHRpbWUudGltZSgpIC0gdDAsIDEpfX0KICAgIG9zLm1ha2VkaXJzKG91dCwgZXhpc3Rfb2s9
VHJ1ZSkKICAgIGNwID0gb3MucGF0aC5qb2luKG91dCwgImdfMmFfYTFfY2hhdGxlZ19jaGVja3Bv
aW50Lmpzb24iKQogICAgb3BlbihjcCwgInciLCBlbmNvZGluZz0idXRmLTgiKS53cml0ZShqc29u
LmR1bXBzKGNrLCBpbmRlbnQ9MSwgZW5zdXJlX2FzY2lpPUZhbHNlLCBzb3J0X2tleXM9VHJ1ZSwg
ZGVmYXVsdD1zdHIpKQogICAgb3Blbihvcy5wYXRoLmpvaW4ob3V0LCAicnVuX2NoYXRsZWcubG9n
IiksICJ3IiwgZW5jb2Rpbmc9InV0Zi04Iikud3JpdGUoIlxuIi5qb2luKGxvZykgKyAiXG4iKQog
ICAgcHJpbnQoIlxuIi5qb2luKGxvZykpOyBwcmludCgiY2hlY2twb2ludCIsIGNwLCBtZDVfZmls
ZShjcCkpCiAgICByZXR1cm4gMAoKaWYgX19uYW1lX18gPT0gIl9fbWFpbl9fIjoKICAgIHN5cy5l
eGl0KG1haW4oKSkK
=====END-EMBED name=g_2a_a1_chatleg.py=====

=====BEGIN-EMBED name=g_2a_a1_chatleg_checkpoint.json md5=8f657a23a68ef082f99a7579af78348c bytes=8247 encoding=base64 armor_bytes=11141 QUARANTINED=====
ewogImFjdGlvbl9leHRyYWN0X21kNSI6ICI5NDBiMGJlZTRiMjExMmU5MTFhZTczOGMzZGIyYmMz
ZCIsCiAiY2l0YXRpb25zIjogewogICJGUiBjcml0ZXJpb24gcGkxKENvbmZpZyk9cGk0KHRhcmdl
dCkiOiAiRmlua2Vsc3RlaW4tUnViaW5zdGVpbiAxOTY4OyBHaXVsaW5pIDE5OTMgKGhlcC10aC85
MzAxMTAxKTsgS3J1c2NoLVNwZWlnaHQgMjAwNiAoaGVwLXRoLzA1MDMwNjcpIiwKICAiUFNMKDIs
Nykgb3JkaW5hcnkgaW5kaWNhdG9ycyBudSgzKT1udSgzYmFyKT0wLCBudSg4KT0rMTsgU0woMiw3
KSBHYWxvaXMgcGFpcmluZ3MiOiAiQVRMQVMgb2YgRmluaXRlIEdyb3VwczsgbGVkZ2VyIMKnMi43
NyAvIMKnMi5ELUZDICh0aGUgNiBhbmQgNyBtYWNoaW5lLXZlcmlmaWVkIGhlcmUpIiwKICAiU1Uo
Myk9U3RhYl9HMihlNyksIEcyL1NVKDMpPVM2LCBGaXhfRzIoSCk9U1UoMikiOiAiR8O8bmF5ZGlu
LUfDvHJzZXkgMTk3MzsgbkxhYiBHMiIsCiAgImV2ZW4gbXVsdGlwbGljaXR5IG9mIHF1YXRlcm5p
b25pYyBpcnJlcHMgaW4gcmVhbCByZXByZXNlbnRhdGlvbnMiOiAic3RhbmRhcmQgKEZyb2Jlbml1
cy1TY2h1ciB0aGVvcnk7IFNlcnJlLCBMaW5lYXIgUmVwcmVzZW50YXRpb25zIG9mIEZpbml0ZSBH
cm91cHMsIMKnMTMuMikiLAogICJwaV9rKFNVMyksIHBpX2soUzYpLCBwaTQoU1UyKSwgcGlfayhV
MSksIHBpX2soUzE1KSI6ICJ0ZXh0Ym9vayBob21vdG9weSAoQm90dCBwZXJpb2RpY2l0eSAvIHN0
YWJsZSByYW5nZTsgSGF0Y2hlciwgQWxnZWJyYWljIFRvcG9sb2d5LCBjaC4gNCk7IE1pbXVyYSAx
OTY3IEouIE1hdGguIEt5b3RvIFVuaXYuIDYgYXMgdGhlIGNhbm9uaWNhbCBHMiB0YWJsZSAobm90
IHJlbGllZCBvbikiLAogICJ0d28gUFNMKDIsNykgY2xhc3NlcyBpbiBHMjsgbm9uLXNwbGl0IDJe
My5QU0woMiw3KSI6ICJDb2hlbi1XYWxlcyAxOTgzIHZpYSBFdmFucy1QdWdoIGFyWGl2OjE0MDQu
MTg2NiBUYWJsZSAxIChjcm9zcy1jaGVjayBvbmx5KSIKIH0sCiAiZWxlY3Rpb25zIjogewogICJF
LUExLTEiOiAiYSIsCiAgIkUtQTEtMiI6ICJhIiwKICAiRS1BMS0zIjogImEiLAogICJFLUExLTQi
OiAiYSIsCiAgIkUtQTEtNSI6ICJhIiwKICAiRS1BMS02IjogImEiLAogICJFLUExLTciOiAiYSIs
CiAgIkUtQTEtOCI6ICJhIgogfSwKICJleHRyYXMiOiB7CiAgIlQyX25vdGUiOiAic3Bpbm9yXzJP
X2F1dG9tb3JwaGlzbV9jb3VudCBjb3VudHMgZWxlbWVudHMgd2l0aCB6ZXJvIGRlZmVjdDsgdGhl
IGlkZW50aXR5IGlzIG9uZSBvZiB0aGVtIChsb2NrIHJlY29yZCBBLTIuMyB3b3JkaW5nKTsgdGhl
IG1pbmltdW0gZGVmZWN0IGlzIG92ZXIgMk8gbWludXMgeysxLC0xfSIsCiAgImFkb3B0ZWRfaG9t
b3RvcHlfaW5wdXRzIjogewogICAicGkxX1NPMyI6ICJaMiIsCiAgICJwaTFfU1UzIjogIjAiLAog
ICAicGkyX1M2IjogIjAiLAogICAicGkzX1NVMyI6ICJaIiwKICAgInBpM19VMSI6ICIwIiwKICAg
InBpNF9TVTIiOiAiWjIiLAogICAicGk0X1NVMyI6ICIwIiwKICAgInBpNF9VMSI6ICIwIiwKICAg
InBpX2tfUzE1X2tfbHRfMTUiOiAiMCIsCiAgICJwaV9rX1M2X2tfbGVfNSI6ICIwIgogIH0sCiAg
ImZzX3NvbHV0aW9ucyI6IFsKICAgWwogICAgLTEsCiAgICAtMSwKICAgIDAKICAgXSwKICAgWwog
ICAgMCwKICAgIC0xLAogICAgLTEKICAgXQogIF0sCiAgImdyb3VwMTM0NF9vcmRlcnNfc2Vlbl9p
bl9jb21wbGVtZW50X3NlYXJjaCI6IHsKICAgIjEzNDQiOiA2NAogIH0sCiAgInBoYXNlMF9pbWFn
X3NlY3Rvcl9jb250aW51b3VzX2RpbSI6IDE0LAogICJwaGFzZTBfbWFyZ2luIjogIjEiLAogICJw
aGFzZTBfcHNpMF9waGFzZV9wcmVzZXJ2ZXNfTyI6IHRydWUsCiAgInBoYXNlMF90ZXJtc19vZl9y
ZWNvcmQiOiBbCiAgIHsKICAgICJpbnRlcm5hbCI6ICJkZWx0YV9hYiAoc2luZ2xlIHNjYWxhciki
LAogICAgIm1peGVkX3NwYXRpYWxfaW50ZXJuYWxfdGVuc29yIjogZmFsc2UsCiAgICAic3BhdGlh
bCI6ICJub25lIiwKICAgICJ0ZXJtIjogInR3by1ib2R5IGNvbnRhY3QiCiAgIH0sCiAgIHsKICAg
ICJpbnRlcm5hbCI6ICJkZWx0YV9hYiIsCiAgICAibWl4ZWRfc3BhdGlhbF9pbnRlcm5hbF90ZW5z
b3IiOiBmYWxzZSwKICAgICJzcGF0aWFsIjogImRfaSAuIGRfaSIsCiAgICAidGVybSI6ICJHUCBr
aW5ldGljIChJMikiCiAgIH0sCiAgIHsKICAgICJpbnRlcm5hbCI6ICJwaGlfYWJjIiwKICAgICJt
aXhlZF9zcGF0aWFsX2ludGVybmFsX3RlbnNvciI6IGZhbHNlLAogICAgInNwYXRpYWwiOiAiZXBz
X3h5IGRfeCBkX3kiLAogICAgInRlcm0iOiAib3JpZW50ZWQgTyIKICAgfQogIF0sCiAgInBoYXNl
Ml9hdXRvbW9ycGhpc21fY2hlY2tzIjogWwogICBbCiAgICAiMS8zIiwKICAgICIxIiwKICAgIHRy
dWUKICAgXSwKICAgWwogICAgIjEvMyIsCiAgICAiLTEiLAogICAgdHJ1ZQogICBdLAogICBbCiAg
ICAiMS8zIiwKICAgICJxIiwKICAgIHRydWUKICAgXSwKICAgWwogICAgIjEvMyIsCiAgICAiZ2Vu
ZXJpYyIsCiAgICB0cnVlCiAgIF0sCiAgIFsKICAgICIyLzUiLAogICAgIjEiLAogICAgdHJ1ZQog
ICBdLAogICBbCiAgICAiMi81IiwKICAgICItMSIsCiAgICB0cnVlCiAgIF0sCiAgIFsKICAgICIy
LzUiLAogICAgInEiLAogICAgdHJ1ZQogICBdLAogICBbCiAgICAiMi81IiwKICAgICJnZW5lcmlj
IiwKICAgIHRydWUKICAgXQogIF0sCiAgInByaW5jaXBhbF93ZWlnaHRzIjogWwogICAtNiwKICAg
LTQsCiAgIC0yLAogICAwLAogICAyLAogICA0LAogICA2CiAgXSwKICAicnVudGltZV9zIjogMTIu
MiwKICAidW5zaWduZWRfYXV0b21vcnBoaXNtc19vZl8xNjgiOiAyMQogfSwKICJnYXRlIjogIkct
MmEtQTEiLAogImluc3RydW1lbnRfbWQ1IjogIjYzNjA3MDlkNmE3ZWI1ZmMzZGY3ZmM4ZmQyNmRj
MzZhIiwKICJsZWRnZXJfYmFzZV9tZDUiOiAiNDAwMDllYzAxOTc4NzZiMTMwNzY2ZjFhZTc0OTQz
NjAiLAogImxlZyI6ICJjaGF0IiwKICJtZW1vX2xvY2tfbWQ1IjogIjYyNmFhODY4ODQ0MjIwZWI2
YzM4MDFlZjA3YTc3NzgzIiwKICJwaGFzZTAiOiB7CiAgIk9fcGhhc2VfaW52YXJpYW50IjogZmFs
c2UsCiAgImNvbXBsZXhfYW1wbGl0dWRlcyI6IDgsCiAgImNvbmp1Z2F0aW9uX21hcHNfT190b19j
b25qdWdhdGUiOiB0cnVlLAogICJjb250cm9scyI6IHsKICAgIkYyMV9zcGxpdF8xXzNfM2JhciI6
IHRydWUsCiAgICJMX3BlcnBfemVyb19tb2RlIjogdHJ1ZSwKICAgImdlbmVyaWNfc28xNl9mYWls
c19tYXJnaW5fcG9zaXRpdmUiOiB0cnVlCiAgfSwKICAiZmllbGRfcmVhbF9jb21wb25lbnRzIjog
MTYsCiAgImcyX3ByZXNlcnZlc19PIjogdHJ1ZSwKICAiZ2VuZXJpY19zbzE2X2JyZWFrc19PIjog
dHJ1ZSwKICAibG9ja2luZ19pbnZlbnRvcnkiOiBbCiAgIHsKICAgICJIMCI6ICJHMiIsCiAgICAi
SDBfZGltIjogMTQsCiAgICAicGkwX2dlbmVyaWMiOiAxLAogICAgInBpM19pbmplY3RpdmUiOiB0
cnVlLAogICAgInBpNF9xdW90aWVudCI6IDAsCiAgICAicmFuayI6IDAsCiAgICAic2wyX2dlbmVy
YXRvcl9pbmRleCI6IDEsCiAgICAic2wyX2dlbmVyYXRvcl9qb3JkYW5fdHlwZSI6IFsKICAgICAy
LAogICAgIDIsCiAgICAgMSwKICAgICAxLAogICAgIDEKICAgIF0KICAgfSwKICAgewogICAgIkgw
IjogIlNVMyIsCiAgICAiSDBfZGltIjogOCwKICAgICJwaTBfZ2VuZXJpYyI6IDEsCiAgICAicGkz
X2luamVjdGl2ZSI6IHRydWUsCiAgICAicGk0X3F1b3RpZW50IjogMCwKICAgICJyYW5rIjogMSwK
ICAgICJzbDJfZ2VuZXJhdG9yX2luZGV4IjogMSwKICAgICJzbDJfZ2VuZXJhdG9yX2pvcmRhbl90
eXBlIjogWwogICAgIDIsCiAgICAgMiwKICAgICAxLAogICAgIDEsCiAgICAgMQogICAgXQogICB9
LAogICB7CiAgICAiSDAiOiAiU1UyX2xvbmciLAogICAgIkgwX2RpbSI6IDMsCiAgICAicGkwX2dl
bmVyaWMiOiAxLAogICAgInBpM19pbmplY3RpdmUiOiB0cnVlLAogICAgInBpNF9xdW90aWVudCI6
IDAsCiAgICAicmFuayI6IDIsCiAgICAic2wyX2dlbmVyYXRvcl9pbmRleCI6IDEsCiAgICAic2wy
X2dlbmVyYXRvcl9qb3JkYW5fdHlwZSI6IFsKICAgICAyLAogICAgIDIsCiAgICAgMSwKICAgICAx
LAogICAgIDEKICAgIF0KICAgfQogIF0sCiAgInBoYXNlX3N1Ymdyb3VwX29yZGVyIjogMywKICAi
cGkxX1YiOiAwLAogICJwaTRfViI6IDAsCiAgInJlYWxfdW5pdF9zcGxpdHRpbmdfdGVybV9wcmVz
ZW50IjogZmFsc2UsCiAgInNwYXRpYWxfaW50ZXJuYWxfZGlyZWN0X3Byb2R1Y3QiOiB0cnVlLAog
ICJzcGlub3JfaW5kZXhfcHJlc2VudCI6IGZhbHNlLAogICJzeW1faW50X2NvbnRpbnVvdXMiOiAi
RzJ4VTFfcHNpMCIsCiAgInN5bV9pbnRfY29udGludW91c19kaW0iOiAxNSwKICAic3ltX2ludF9w
aW5uZWQiOiB0cnVlLAogICJ0d29fYm9keV9zeW1tZXRyeSI6ICJPKDE2KSIsCiAgInZhY3V1bV9t
YW5pZm9sZF9vZl9yZWNvcmQiOiAiUzE1IgogfSwKICJwaGFzZTEiOiB7CiAgIlQxIjogewogICAi
YnJhbmNoaW5nX2xvbmdfcm9vdCI6IFsKICAgIDIsCiAgICAyLAogICAgMSwKICAgIDEsCiAgICAx
CiAgIF0sCiAgICJicmFuY2hpbmdfcHJpbmNpcGFsIjogWwogICAgNwogICBdLAogICAiYnJhbmNo
aW5nX3Nob3J0X3Jvb3QiOiBbCiAgICAzLAogICAgMiwKICAgIDIKICAgXSwKICAgImJyYW5jaGlu
Z19zdTNfc2wyIjogWwogICAgMywKICAgIDMsCiAgICAxCiAgIF0sCiAgICJjaGkzMl9hdF8xIjog
NCwKICAgImNoaTMyX2F0X21pbnVzMSI6IC00LAogICAiY2hpMzJfbm9ybSI6IDEsCiAgICJjb250
cm9sX3N5bTNfcXVhcnRldF9tdWx0IjogMSwKICAgImZzX2luZGljYXRvciI6IC0xLAogICAiaG9s
ZHMiOiB0cnVlLAogICAicGhhc2VfY2hhcl9vbl8yT190cml2aWFsIjogdHJ1ZSwKICAgInF1YXJ0
ZXRfbXVsdGlwbGljaXR5X3VwcGVyIjogMCwKICAgInNldmVuX3JlYWwiOiB0cnVlCiAgfSwKICAi
VDIiOiB7CiAgICJjb250cm9sXzEzNDRfYWxsX2F1dG9tb3JwaGlzbXMiOiB0cnVlLAogICAiZGlt
X2JpdmVjdG9yc182IjogMTUsCiAgICJkaW1fYml2ZWN0b3JzXzciOiAyMSwKICAgImRpbV9kZXIi
OiAxNCwKICAgImRpbV9nMl9jYXBfc3U0IjogOCwKICAgImZzX3N1bV9vcmRpbmFyeSI6IDIyLAog
ICAiZzJfaW5fc3BpbjciOiB0cnVlLAogICAiZ3JvdXAxMzQ0X29yZGVyIjogMTM0NCwKICAgImhv
bGRzIjogdHJ1ZSwKICAgImludm9sdXRpb25fdHJhY2UiOiAtMSwKICAgIm51NF9hbGxvd2VkIjog
WwogICAgLTEsCiAgICAwCiAgIF0sCiAgICJzaWdtYV9IX2lzX2F1dG9tb3JwaGlzbSI6IHRydWUs
CiAgICJzaW5nbGVfdW5pdF9uZWdhdGlvbl9pc19hdXRvbW9ycGhpc20iOiBmYWxzZSwKICAgInNs
Mjdfb3JkZXIiOiAzMzYsCiAgICJzbDI3X3NxMV9jb3VudCI6IDIsCiAgICJzcGlub3JfMk9fYXV0
b21vcnBoaXNtX2NvdW50IjogMSwKICAgInNwaW5vcl8yT19taW5fYXV0b21vcnBoaXNtX2RlZmVj
dCI6IDAuNzA3MTA2NzgxMTg2NTQ5NSwKICAgInNwaW5vcl8yT19vcmRlciI6IDQ4LAogICAic3Bp
bm9yXzJPX3F1YXJ0ZXRfbXVsdCI6IDIKICB9LAogICJUMyI6IHsKICAgImNvbnRyb2xzX3BpMV9T
TzNfbW9kX1QiOiAyNCwKICAgImNvbnRyb2xzX3BpNF9TMiI6ICJaMiIsCiAgICJjb250cm9sc19w
aTRfUzMiOiAiWjIiLAogICAiZW52ZWxvcGVfaW5fT19raWxsIjogdHJ1ZSwKICAgImhvbGRzIjog
dHJ1ZSwKICAgIm5vX2ludGVybmFsX2RvdWJsZV9jb3ZlciI6IHRydWUsCiAgICJwaTFfRzIiOiAw
LAogICAicGkxX1YiOiAwLAogICAicGkzX0cyIjogIloiLAogICAicGk0X0cyIjogMCwKICAgInBp
NF9WIjogMAogIH0sCiAgIlQ0IjogewogICAiY29udHJvbF9GMjFfdW5zaWduZWRfMV8zXzNiYXIi
OiB0cnVlLAogICAiZ2FwIjogNCwKICAgImhvbGRzIjogdHJ1ZSwKICAgImxpZnRzX3RvdGFsIjog
MjQsCiAgICJudTJfdW5zaWduZWRfYXV0b21vcnBoaXNtIjogdHJ1ZSwKICAgIm9yZGVyMl9jb3Vu
dCI6IDEyLAogICAib3JkZXIyX3RyYWNlc19zZXQiOiBbCiAgICAtMQogICBdLAogICAib3JkZXI0
X2NvdW50IjogMTIsCiAgICJvcmRlcjRfdHJhY2VzX3NldCI6IFsKICAgIC0xLAogICAgMwogICBd
LAogICAicGVybV9jaGFyX2ludm9sdXRpb24iOiAzLAogICAicmhvNl9jaGFyXzJBIjogMgogIH0s
CiAgImdyb3VwMTM0NCI6IHsKICAgImNvbXBsZW1lbnRzX2ZvdW5kIjogMCwKICAgImxpZnRfcGFp
cnNfdGVzdGVkIjogNjQsCiAgICJvcmRlciI6IDEzNDQsCiAgICJzcGxpdCI6IGZhbHNlCiAgfQog
fSwKICJwaGFzZTFiIjogewogICJIX3NjcmVlbiI6IHsKICAgIkgxIjogewogICAgImNvZGUiOiAi
RVhDTFVERUQoaSxpaWkpIiwKICAgICJpIjogImZhaWwiLAogICAgImlpIjogInBhc3MiLAogICAg
ImlpaSI6ICJmYWlsIiwKICAgICJpdiI6ICJuL2EiLAogICAgInJvbGUiOiAiY29udHJvbCIKICAg
fSwKICAgIkgyIjogewogICAgImNvZGUiOiAiQURNSVNTSUJMRS1JTVBPUlQiLAogICAgImkiOiAi
cGFzcyIsCiAgICAiaWkiOiAicGFzcyIsCiAgICAiaWlpIjogInBhc3MiLAogICAgIml2IjogImR5
bmFtaWNhbCIsCiAgICAicm9sZSI6ICJjYW5kaWRhdGUiCiAgIH0sCiAgICJIMyI6IHsKICAgICJj
b2RlIjogIkFETUlTU0lCTEUtSU1QT1JUIiwKICAgICJpIjogInBhc3MiLAogICAgImlpIjogInBh
c3MiLAogICAgImlpaSI6ICJjb25kaXRpb25hbCIsCiAgICAiaXYiOiAia2luZW1hdGljIiwKICAg
ICJyb2xlIjogImNhbmRpZGF0ZSIKICAgfSwKICAgIkg0IjogewogICAgImNvZGUiOiAiRVhDTFVE
RUQoaSkiLAogICAgImkiOiAiZmFpbCIsCiAgICAiaWkiOiAicGFzcyIsCiAgICAiaWlpIjogIm4v
YSIsCiAgICAiaXYiOiAibi9hIiwKICAgICJyb2xlIjogImNhbmRpZGF0ZSIKICAgfSwKICAgIkg1
IjogewogICAgImNvZGUiOiAiRVhDTFVERUQoaSxpaSkiLAogICAgImkiOiAiZmFpbCIsCiAgICAi
aWkiOiAiZmFpbCIsCiAgICAiaWlpIjogIm4vYSIsCiAgICAiaXYiOiAibi9hIiwKICAgICJyb2xl
IjogImNhbmRpZGF0ZSIKICAgfQogIH0sCiAgIkk1X3JlZ2lzdGVyZWQiOiB0cnVlLAogICJQX0Mi
OiB7CiAgICJjb21wbGV4X3VuaXRfY2VudHJhbCI6IHRydWUsCiAgICJkaXNwb3NpdGlvbiI6ICJD
TE9TRUQtQlktSU5TVEFOVElBVElPTiIsCiAgICJlOF9hbnRpY29tbXV0ZXMiOiB0cnVlLAogICAi
ZThfY2VudHJhbCI6IGZhbHNlCiAgfSwKICAiYWRtaXNzaWJsZSI6IFsKICAgIkgyIiwKICAgIkgz
IgogIF0KIH0sCiAicGhhc2UyIjogewogICJPX2xpbmVfYWJzIjogMTIuNTY2MzcwNjE0MzU5MTcy
LAogICJPX25vbmxpbmVfYWJzIjogMC4wLAogICJPX25vbnplcm9fb25fbGluZSI6IHRydWUsCiAg
Ik9femVyb19vbl9ub25saW5lIjogdHJ1ZSwKICAiY2hpcmFsX3BhaXJfY2hhcmFjdGVyX29yZGlu
YXJ5IjogdHJ1ZSwKICAiY29udHJvbF9vYmplY3QiOiAibm9ubGluZV90ZXh0dXJlX0wxMjMiLAog
ICJkaW1lbnNpb25fbm90ZSI6ICIyRCB3aXRuZXNzOyBjb250cmFjdGliaWxpdHkgb2YgdGhlIDJw
aSBsb29wIGluIHRoZSBvcmJpdCBvbmx5IiwKICAibGFiZWwiOiAiSU5URVJOQUwtSE9MT05PTVkt
R0FVR0UiLAogICJsb29wX2ltYWdlcyI6IFsKICAgIklkIiwKICAgInNpZ21hX0giCiAgXSwKICAi
b2JqZWN0IjogImZhbm9fbGluZV90ZXh0dXJlX0wxMjRfaG9tb2dlbmVvdXNfR1BfMkQiLAogICJw
aTBfc3RhYiI6IDEsCiAgInBpMV9vcmJpdCI6IDAsCiAgInByb2ZpbGVfaWQiOiAibG9ja3JlYy1B
LTIuNiIsCiAgInNpZ21hX0hfZWlnZW5fbWludXMxIjogNCwKICAic2lnbWFfSF9laWdlbl9wbHVz
MSI6IDQsCiAgInN0YWJfaW50ZXJuYWxfaW1hZ2UiOiAiU080X1N0YWJfSEwiLAogICJzdGFiX2tl
cm5lbCI6ICJTVTJfbG9uZyIsCiAgInN0YWJfc3ViZGlyZWN0IjogdHJ1ZQogfSwKICJwaGFzZTMi
OiB7CiAgIkk1IjogdHJ1ZSwKICAiYWRtaXNzaWJsZV9IIjogWwogICAiSDIiLAogICAiSDMiCiAg
XSwKICAiY29udHJvbHNfYWxsX3Bhc3MiOiB0cnVlLAogICJ0ZXN0c19ob2xkaW5nIjogWwogICAi
VDEiLAogICAiVDIiLAogICAiVDMiLAogICAiVDQiCiAgXSwKICAidmVyZGljdCI6ICJBU1NJR05N
RU5ULUktRk9SQ0VEIgogfSwKICJ0MV9saXN0X21kNSI6ICIyMDI2Yjc4MmRiMzkwNWQ5ZjJjZTM1
NzMzODIzNjE4YyIsCiAidDFfc2NhbiI6IHsKICAiZXh0cmFjdCI6ICJDTEVBTiIsCiAgImluc3Ry
dW1lbnQiOiAiQ0xFQU4iLAogICJtZW1vIjogIkNMRUFOIgogfQp9
=====END-EMBED name=g_2a_a1_chatleg_checkpoint.json=====

=====BEGIN-EMBED name=g_2a_a1_chatleg_compare.json md5=ba0876074396e697614a4daa78da7682 bytes=66541 encoding=base64 armor_bytes=89892 QUARANTINED=====
ewogImNjX2NrcHRfbWQ1IjogIjhmNjU3YTIzYTY4ZWYwODJmOTlhNzU3OWFmNzgzNDhjIiwKICJj
aGF0X2NrcHRfbWQ1IjogIjhmNjU3YTIzYTY4ZWYwODJmOTlhNzU3OWFmNzgzNDhjIiwKICJjb21w
YXJhdG9yIjogImdfMmFfYTFfY29tcGFyZV92MV8wIiwKICJtaXNzZXMiOiBbCiAgewogICAiY2Mi
OiAiY2hhdCIsCiAgICJjaGF0IjogImNoYXQiLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6
ICJsZWcgbGFiZWxzIGNoYXQvY2MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IGZhbHNlCiAg
fSwKICB7CiAgICJjYyI6ICI2MzYwNzA5ZDZhN2ViNWZjM2RmN2ZjOGZkMjZkYzM2YSIsCiAgICJj
aGF0IjogIjYzNjA3MDlkNmE3ZWI1ZmMzZGY3ZmM4ZmQyNmRjMzZhIiwKICAgImNoZWNrIjogIkMw
IiwKICAgIm5hbWUiOiAiaW5kZXBlbmRlbmNlIHdpdG5lc3M6IGluc3RydW1lbnRfbWQ1IGRpZmZl
ciIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogZmFsc2UKICB9LAogIHsKICAgImNjIjogbnVs
bCwKICAgImNoYXQiOiAiRzJ4VTFfcHNpMCIsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjog
InBoYXNlMC5zeW1faW50X2NvbnRpbnVvdXMgKGNoYXQpIGluIGRvbWFpbiIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogZmFsc2UKICB9LAogIHsKICAgImNjIjogIkcyeFUxX3BzaTAiLAogICAi
Y2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5zeW1faW50
X2NvbnRpbnVvdXMgKGNjKSBpbiBkb21haW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IGZh
bHNlCiAgfQogXSwKICJyb3dzIjogWwogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxs
LAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1aXJlZCBrZXkgZ2F0ZSBwcmVzZW50
IChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJl
cXVpcmVkIGtleSBnYXRlIHByZXNlbnQgKGNjKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjog
dHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6
ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBsZWcgcHJlc2VudCAoY2hhdCkiLAogICAi
bm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNo
YXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1aXJlZCBrZXkgbGVn
IHByZXNlbnQgKGNjKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewog
ICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1l
IjogInJlcXVpcmVkIGtleSBpbnN0cnVtZW50X21kNSBwcmVzZW50IChjaGF0KSIsCiAgICJub3Rl
IjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6
IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBpbnN0cnVt
ZW50X21kNSBwcmVzZW50IChjYykiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAog
ICAibmFtZSI6ICJyZXF1aXJlZCBrZXkgbWVtb19sb2NrX21kNSBwcmVzZW50IChjaGF0KSIsCiAg
ICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAi
Y2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBt
ZW1vX2xvY2tfbWQ1IHByZXNlbnQgKGNjKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJD
MCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBsZWRnZXJfYmFzZV9tZDUgcHJlc2VudCAoY2hh
dCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVs
bCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1aXJl
ZCBrZXkgbGVkZ2VyX2Jhc2VfbWQ1IHByZXNlbnQgKGNjKSIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJj
aGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSB0MV9saXN0X21kNSBwcmVzZW50
IChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJl
cXVpcmVkIGtleSB0MV9saXN0X21kNSBwcmVzZW50IChjYykiLAogICAibm90ZSI6ICIiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAi
Y2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1aXJlZCBrZXkgYWN0aW9uX2V4dHJhY3RfbWQ1
IHByZXNlbnQgKGNoYXQpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMwIiwKICAgIm5h
bWUiOiAicmVxdWlyZWQga2V5IGFjdGlvbl9leHRyYWN0X21kNSBwcmVzZW50IChjYykiLAogICAi
bm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNo
YXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1aXJlZCBrZXkgdDFf
c2NhbiBwcmVzZW50IChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAg
ICJuYW1lIjogInJlcXVpcmVkIGtleSB0MV9zY2FuIHByZXNlbnQgKGNjKSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51
bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBlbGVjdGlvbnMg
cHJlc2VudCAoY2hhdCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFt
ZSI6ICJyZXF1aXJlZCBrZXkgZWxlY3Rpb25zIHByZXNlbnQgKGNjKSIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGws
CiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBwaGFzZTAgcHJlc2Vu
dCAoY2hhdCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJy
ZXF1aXJlZCBrZXkgcGhhc2UwIHByZXNlbnQgKGNjKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVj
ayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBwaGFzZTEgcHJlc2VudCAoY2hhdCki
LAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwK
ICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1aXJlZCBr
ZXkgcGhhc2UxIHByZXNlbnQgKGNjKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIs
CiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBwaGFzZTFiIHByZXNlbnQgKGNoYXQpIiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0
IjogbnVsbCwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAicmVxdWlyZWQga2V5IHBoYXNl
MWIgcHJlc2VudCAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMwIiwKICAgIm5h
bWUiOiAicmVxdWlyZWQga2V5IHBoYXNlMiBwcmVzZW50IChjaGF0KSIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGws
CiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBwaGFzZTIgcHJlc2Vu
dCAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAicmVx
dWlyZWQga2V5IHBoYXNlMyBwcmVzZW50IChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVj
ayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBwaGFzZTMgcHJlc2VudCAoY2MpIiwK
ICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICI2MjZhYTg2
ODg0NDIyMGViNmMzODAxZWYwN2E3Nzc4MyIsCiAgICJjaGF0IjogIjYyNmFhODY4ODQ0MjIwZWI2
YzM4MDFlZjA3YTc3NzgzIiwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAibWVtb19sb2Nr
X21kNSA9PSBzY2hlbWEgKGNoYXQpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6ICI2MjZhYTg2ODg0NDIyMGViNmMzODAxZWYwN2E3Nzc4MyIsCiAgICJj
aGF0IjogIjYyNmFhODY4ODQ0MjIwZWI2YzM4MDFlZjA3YTc3NzgzIiwKICAgImNoZWNrIjogIkMw
IiwKICAgIm5hbWUiOiAibWVtb19sb2NrX21kNSA9PSBzY2hlbWEgKGNjKSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiNDAwMDllYzAxOTc4NzZiMTMw
NzY2ZjFhZTc0OTQzNjAiLAogICAiY2hhdCI6ICI0MDAwOWVjMDE5Nzg3NmIxMzA3NjZmMWFlNzQ5
NDM2MCIsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogImxlZGdlcl9iYXNlX21kNSA9PSBz
Y2hlbWEgKGNoYXQpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAg
ICJjYyI6ICI0MDAwOWVjMDE5Nzg3NmIxMzA3NjZmMWFlNzQ5NDM2MCIsCiAgICJjaGF0IjogIjQw
MDA5ZWMwMTk3ODc2YjEzMDc2NmYxYWU3NDk0MzYwIiwKICAgImNoZWNrIjogIkMwIiwKICAgIm5h
bWUiOiAibGVkZ2VyX2Jhc2VfbWQ1ID09IHNjaGVtYSAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAg
InBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICIyMDI2Yjc4MmRiMzkwNWQ5ZjJjZTM1NzMz
ODIzNjE4YyIsCiAgICJjaGF0IjogIjIwMjZiNzgyZGIzOTA1ZDlmMmNlMzU3MzM4MjM2MThjIiwK
ICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAidDFfbGlzdF9tZDUgPT0gc2NoZW1hIChjaGF0
KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiMjAy
NmI3ODJkYjM5MDVkOWYyY2UzNTczMzgyMzYxOGMiLAogICAiY2hhdCI6ICIyMDI2Yjc4MmRiMzkw
NWQ5ZjJjZTM1NzMzODIzNjE4YyIsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInQxX2xp
c3RfbWQ1ID09IHNjaGVtYSAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6ICI5NDBiMGJlZTRiMjExMmU5MTFhZTczOGMzZGIyYmMzZCIsCiAgICJj
aGF0IjogIjk0MGIwYmVlNGIyMTEyZTkxMWFlNzM4YzNkYjJiYzNkIiwKICAgImNoZWNrIjogIkMw
IiwKICAgIm5hbWUiOiAiYWN0aW9uX2V4dHJhY3RfbWQ1ID09IHNjaGVtYSAoY2hhdCkiLAogICAi
bm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIjk0MGIwYmVlNGIy
MTEyZTkxMWFlNzM4YzNkYjJiYzNkIiwKICAgImNoYXQiOiAiOTQwYjBiZWU0YjIxMTJlOTExYWU3
MzhjM2RiMmJjM2QiLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJhY3Rpb25fZXh0cmFj
dF9tZDUgPT0gc2NoZW1hIChjYykiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogIkctMmEtQTEiLAogICAiY2hhdCI6ICJHLTJhLUExIiwKICAgImNoZWNr
IjogIkMwIiwKICAgIm5hbWUiOiAiZ2F0ZSBsYWJlbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiY2hhdCIsCiAgICJjaGF0IjogImNoYXQiLAogICAi
Y2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJsZWcgbGFiZWxzIGNoYXQvY2MiLAogICAibm90ZSI6
ICIiLAogICAicGFzcyI6IGZhbHNlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0Ijog
IkNMRUFOIiwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAidDFfc2Nhbi5pbnN0cnVtZW50
IENMRUFOIChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewog
ICAiY2MiOiAiQ0xFQU4iLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJu
YW1lIjogInQxX3NjYW4uaW5zdHJ1bWVudCBDTEVBTiAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAg
InBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogIkNMRUFOIiwK
ICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAidDFfc2Nhbi5tZW1vIENMRUFOIChjaGF0KSIs
CiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiQ0xFQU4i
LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInQxX3NjYW4u
bWVtbyBDTEVBTiAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogIkNMRUFOIiwKICAgImNoZWNrIjogIkMwIiwKICAg
Im5hbWUiOiAidDFfc2Nhbi5leHRyYWN0IENMRUFOIChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiQ0xFQU4iLAogICAiY2hhdCI6IG51bGws
CiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInQxX3NjYW4uZXh0cmFjdCBDTEVBTiAoY2Mp
IiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHsKICAg
ICJFLUExLTEiOiAiYSIsCiAgICAiRS1BMS0yIjogImEiLAogICAgIkUtQTEtMyI6ICJhIiwKICAg
ICJFLUExLTQiOiAiYSIsCiAgICAiRS1BMS01IjogImEiLAogICAgIkUtQTEtNiI6ICJhIiwKICAg
ICJFLUExLTciOiAiYSIsCiAgICAiRS1BMS04IjogImEiCiAgIH0sCiAgICJjaGF0IjogewogICAg
IkUtQTEtMSI6ICJhIiwKICAgICJFLUExLTIiOiAiYSIsCiAgICAiRS1BMS0zIjogImEiLAogICAg
IkUtQTEtNCI6ICJhIiwKICAgICJFLUExLTUiOiAiYSIsCiAgICAiRS1BMS02IjogImEiLAogICAg
IkUtQTEtNyI6ICJhIiwKICAgICJFLUExLTgiOiAiYSIKICAgfSwKICAgImNoZWNrIjogIkMwIiwK
ICAgIm5hbWUiOiAiZWxlY3Rpb25zID09IHNjaGVtYSAoY2hhdCkiLAogICAibm90ZSI6ICIiLAog
ICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogewogICAgIkUtQTEtMSI6ICJhIiwKICAg
ICJFLUExLTIiOiAiYSIsCiAgICAiRS1BMS0zIjogImEiLAogICAgIkUtQTEtNCI6ICJhIiwKICAg
ICJFLUExLTUiOiAiYSIsCiAgICAiRS1BMS02IjogImEiLAogICAgIkUtQTEtNyI6ICJhIiwKICAg
ICJFLUExLTgiOiAiYSIKICAgfSwKICAgImNoYXQiOiB7CiAgICAiRS1BMS0xIjogImEiLAogICAg
IkUtQTEtMiI6ICJhIiwKICAgICJFLUExLTMiOiAiYSIsCiAgICAiRS1BMS00IjogImEiLAogICAg
IkUtQTEtNSI6ICJhIiwKICAgICJFLUExLTYiOiAiYSIsCiAgICAiRS1BMS03IjogImEiLAogICAg
IkUtQTEtOCI6ICJhIgogICB9LAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJlbGVjdGlv
bnMgPT0gc2NoZW1hIChjYykiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogIjYzNjA3MDlkNmE3ZWI1ZmMzZGY3ZmM4ZmQyNmRjMzZhIiwKICAgImNoYXQi
OiAiNjM2MDcwOWQ2YTdlYjVmYzNkZjdmYzhmZDI2ZGMzNmEiLAogICAiY2hlY2siOiAiQzAiLAog
ICAibmFtZSI6ICJpbmRlcGVuZGVuY2Ugd2l0bmVzczogaW5zdHJ1bWVudF9tZDUgZGlmZmVyIiwK
ICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiBmYWxzZQogIH0sCiAgewogICAiY2MiOiAxNiwKICAg
ImNoYXQiOiAxNiwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLmZpZWxkX3Jl
YWxfY29tcG9uZW50cyB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IDE2LAogICAiY2hhdCI6IDE2LAogICAiY2hlY2siOiAiQzEi
LAogICAibmFtZSI6ICJwaGFzZTAuZmllbGRfcmVhbF9jb21wb25lbnRzIGVxdWFsIiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDgsCiAgICJjaGF0Ijog
OCwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLmNvbXBsZXhfYW1wbGl0dWRl
cyB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IDgsCiAgICJjaGF0IjogOCwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAi
cGhhc2UwLmNvbXBsZXhfYW1wbGl0dWRlcyBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBmYWxzZSwKICAgImNoYXQiOiBmYWxzZSwKICAgImNo
ZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLnNwaW5vcl9pbmRleF9wcmVzZW50IHR5cGVk
IiwKICAgIm5vdGUiOiAidHlwZSBib29sIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJj
YyI6IGZhbHNlLAogICAiY2hhdCI6IGZhbHNlLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6
ICJwaGFzZTAuc3Bpbm9yX2luZGV4X3ByZXNlbnQgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAi
Y2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuc3BhdGlhbF9pbnRlcm5hbF9kaXJlY3Rf
cHJvZHVjdCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9vbCIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMSIs
CiAgICJuYW1lIjogInBoYXNlMC5zcGF0aWFsX2ludGVybmFsX2RpcmVjdF9wcm9kdWN0IGVxdWFs
IiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUs
CiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLnN5
bV9pbnRfcGlubmVkIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBib29sIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjog
IkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLnN5bV9pbnRfcGlubmVkIGVxdWFsIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJHMnhVMV9wc2kwIiwKICAg
ImNoYXQiOiAiRzJ4VTFfcHNpMCIsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNl
MC5zeW1faW50X2NvbnRpbnVvdXMgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIHN0ciIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiRzJ4VTFfcHNpMCIsCiAgICJjaGF0IjogIkcy
eFUxX3BzaTAiLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuc3ltX2ludF9j
b250aW51b3VzIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IDE1LAogICAiY2hhdCI6IDE1LAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6
ICJwaGFzZTAuc3ltX2ludF9jb250aW51b3VzX2RpbSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUg
aW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDE1LAogICAiY2hhdCI6IDE1
LAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuc3ltX2ludF9jb250aW51b3Vz
X2RpbSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjog
InBoYXNlMC5nMl9wcmVzZXJ2ZXNfTyB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9vbCIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAg
ICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5nMl9wcmVzZXJ2ZXNfTyBlcXVhbCIs
CiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAog
ICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5nZW5l
cmljX3NvMTZfYnJlYWtzX08gdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGJvb2wiLAogICAicGFz
cyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hl
Y2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuZ2VuZXJpY19zbzE2X2JyZWFrc19PIGVxdWFs
IiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDMsCiAg
ICJjaGF0IjogMywKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLnBoYXNlX3N1
Ymdyb3VwX29yZGVyIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBpbnQiLAogICAicGFzcyI6IHRy
dWUKICB9LAogIHsKICAgImNjIjogMywKICAgImNoYXQiOiAzLAogICAiY2hlY2siOiAiQzEiLAog
ICAibmFtZSI6ICJwaGFzZTAucGhhc2Vfc3ViZ3JvdXBfb3JkZXIgZXF1YWwiLAogICAibm90ZSI6
ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogZmFsc2UsCiAgICJjaGF0Ijog
ZmFsc2UsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5PX3BoYXNlX2ludmFy
aWFudCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9vbCIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiBmYWxzZSwKICAgImNoYXQiOiBmYWxzZSwKICAgImNoZWNrIjogIkMxIiwK
ICAgIm5hbWUiOiAicGhhc2UwLk9fcGhhc2VfaW52YXJpYW50IGVxdWFsIiwKICAgIm5vdGUiOiAi
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1
ZSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLmNvbmp1Z2F0aW9uX21hcHNf
T190b19jb25qdWdhdGUgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGJvb2wiLAogICAicGFzcyI6
IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2si
OiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuY29uanVnYXRpb25fbWFwc19PX3RvX2Nvbmp1Z2F0
ZSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiAiTygxNikiLAogICAiY2hhdCI6ICJPKDE2KSIsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1l
IjogInBoYXNlMC50d29fYm9keV9zeW1tZXRyeSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgc3Ry
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJPKDE2KSIsCiAgICJjaGF0Ijog
Ik8oMTYpIiwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLnR3b19ib2R5X3N5
bW1ldHJ5IGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAg
ICJjYyI6ICJTMTUiLAogICAiY2hhdCI6ICJTMTUiLAogICAiY2hlY2siOiAiQzEiLAogICAibmFt
ZSI6ICJwaGFzZTAudmFjdXVtX21hbmlmb2xkX29mX3JlY29yZCB0eXBlZCIsCiAgICJub3RlIjog
InR5cGUgc3RyIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJTMTUiLAogICAi
Y2hhdCI6ICJTMTUiLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAudmFjdXVt
X21hbmlmb2xkX29mX3JlY29yZCBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiAwLAogICAiY2hhdCI6IDAsCiAgICJjaGVjayI6ICJDMSIsCiAg
ICJuYW1lIjogInBoYXNlMC5waTFfViB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAg
InBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDAsCiAgICJjaGF0IjogMCwKICAgImNoZWNr
IjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLnBpMV9WIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDAsCiAgICJjaGF0IjogMCwKICAgImNo
ZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLnBpNF9WIHR5cGVkIiwKICAgIm5vdGUiOiAi
dHlwZSBpbnQiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMCwKICAgImNoYXQi
OiAwLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAucGk0X1YgZXF1YWwiLAog
ICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogZmFsc2UsCiAg
ICJjaGF0IjogZmFsc2UsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5yZWFs
X3VuaXRfc3BsaXR0aW5nX3Rlcm1fcHJlc2VudCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9v
bCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBmYWxzZSwKICAgImNoYXQiOiBm
YWxzZSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLnJlYWxfdW5pdF9zcGxp
dHRpbmdfdGVybV9wcmVzZW50IGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkMx
IiwKICAgIm5hbWUiOiAicGhhc2UwLmNvbnRyb2xzLkxfcGVycF96ZXJvX21vZGUgdHlwZWQiLAog
ICAibm90ZSI6ICJ0eXBlIGJvb2wiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
dHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFz
ZTAuY29udHJvbHMuTF9wZXJwX3plcm9fbW9kZSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJj
aGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5jb250cm9scy5GMjFfc3BsaXRfMV8zXzNi
YXIgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGJvb2wiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzEiLAogICAi
bmFtZSI6ICJwaGFzZTAuY29udHJvbHMuRjIxX3NwbGl0XzFfM18zYmFyIGVxdWFsIiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0
IjogdHJ1ZSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLmNvbnRyb2xzLmdl
bmVyaWNfc28xNl9mYWlsc19tYXJnaW5fcG9zaXRpdmUgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBl
IGJvb2wiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQi
OiB0cnVlLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuY29udHJvbHMuZ2Vu
ZXJpY19zbzE2X2ZhaWxzX21hcmdpbl9wb3NpdGl2ZSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6ICJHMnhVMV9w
c2kwIiwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLnN5bV9pbnRfY29udGlu
dW91cyAoY2hhdCkgaW4gZG9tYWluIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiBmYWxzZQog
IH0sCiAgewogICAiY2MiOiAiRzJ4VTFfcHNpMCIsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNr
IjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLnN5bV9pbnRfY29udGludW91cyAoY2MpIGluIGRv
bWFpbiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogZmFsc2UKICB9LAogIHsKICAgImNjIjog
bnVsbCwKICAgImNoYXQiOiAiTygxNikiLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJw
aGFzZTAudHdvX2JvZHlfc3ltbWV0cnkgKGNoYXQpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiTygxNikiLAogICAiY2hhdCI6IG51
bGwsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC50d29fYm9keV9zeW1tZXRy
eSAoY2MpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6ICJTMTUiLAogICAiY2hlY2siOiAiQzEiLAogICAi
bmFtZSI6ICJwaGFzZTAudmFjdXVtX21hbmlmb2xkX29mX3JlY29yZCAoY2hhdCkgaW4gZG9tYWlu
IiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJTMTUi
LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC52
YWN1dW1fbWFuaWZvbGRfb2ZfcmVjb3JkIChjYykgaW4gZG9tYWluIiwKICAgIm5vdGUiOiAiIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwK
ICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLmNvbnRyb2xzLkxfcGVycF96ZXJv
X21vZGUgdHJ1ZSBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzEiLAog
ICAibmFtZSI6ICJwaGFzZTAuY29udHJvbHMuRjIxX3NwbGl0XzFfM18zYmFyIHRydWUgYm90aCBs
ZWdzIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRy
dWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2Uw
LmNvbnRyb2xzLmdlbmVyaWNfc28xNl9mYWlsc19tYXJnaW5fcG9zaXRpdmUgdHJ1ZSBib3RoIGxl
Z3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMywK
ICAgImNoYXQiOiAzLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJsb2NraW5nX2ludmVu
dG9yeSBsaXN0IGxlbmd0aCBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiAwLAogICAiY2hhdCI6IDAsCiAgICJjaGVjayI6ICJDMSIsCiAgICJu
YW1lIjogImxvY2tpbmdfaW52ZW50b3J5W3Jhbms9MF0ucmFuayB0eXBlZCIsCiAgICJub3RlIjog
InR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDAsCiAgICJjaGF0
IjogMCwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFu
az0wXS5yYW5rIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6ICJHMiIsCiAgICJjaGF0IjogIkcyIiwKICAgImNoZWNrIjogIkMxIiwKICAgIm5h
bWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0wXS5IMCB0eXBlZCIsCiAgICJub3RlIjogInR5
cGUgc3RyIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJHMiIsCiAgICJjaGF0
IjogIkcyIiwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlb
cmFuaz0wXS5IMCBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiAxNCwKICAgImNoYXQiOiAxNCwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUi
OiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0wXS5IMF9kaW0gdHlwZWQiLAogICAibm90ZSI6ICJ0
eXBlIGludCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxNCwKICAgImNoYXQi
OiAxNCwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFu
az0wXS5IMF9kaW0gZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogMSwKICAgImNoYXQiOiAxLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6
ICJsb2NraW5nX2ludmVudG9yeVtyYW5rPTBdLnBpMF9nZW5lcmljIHR5cGVkIiwKICAgIm5vdGUi
OiAidHlwZSBpbnQiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMSwKICAgImNo
YXQiOiAxLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJsb2NraW5nX2ludmVudG9yeVty
YW5rPTBdLnBpMF9nZW5lcmljIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IFsKICAgIDIsCiAgICAyLAogICAgMSwKICAgIDEsCiAgICAxCiAg
IF0sCiAgICJjaGF0IjogWwogICAgMiwKICAgIDIsCiAgICAxLAogICAgMSwKICAgIDEKICAgXSwK
ICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0wXS5z
bDJfZ2VuZXJhdG9yX2pvcmRhbl90eXBlIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBsaXN0IiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IFsKICAgIDIsCiAgICAyLAogICAgMSwK
ICAgIDEsCiAgICAxCiAgIF0sCiAgICJjaGF0IjogWwogICAgMiwKICAgIDIsCiAgICAxLAogICAg
MSwKICAgIDEKICAgXSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZl
bnRvcnlbcmFuaz0wXS5zbDJfZ2VuZXJhdG9yX2pvcmRhbl90eXBlIGVxdWFsIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEsCiAgICJjaGF0IjogMSwK
ICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0wXS5z
bDJfZ2VuZXJhdG9yX2luZGV4IHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBpbnQiLAogICAicGFz
cyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMSwKICAgImNoYXQiOiAxLAogICAiY2hlY2siOiAi
QzEiLAogICAibmFtZSI6ICJsb2NraW5nX2ludmVudG9yeVtyYW5rPTBdLnNsMl9nZW5lcmF0b3Jf
aW5kZXggZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAg
ImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6
ICJsb2NraW5nX2ludmVudG9yeVtyYW5rPTBdLnBpM19pbmplY3RpdmUgdHlwZWQiLAogICAibm90
ZSI6ICJ0eXBlIGJvb2wiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwK
ICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJsb2NraW5nX2lu
dmVudG9yeVtyYW5rPTBdLnBpM19pbmplY3RpdmUgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMCwKICAgImNoYXQiOiAwLAogICAiY2hlY2si
OiAiQzEiLAogICAibmFtZSI6ICJsb2NraW5nX2ludmVudG9yeVtyYW5rPTBdLnBpNF9xdW90aWVu
dCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IDAsCiAgICJjaGF0IjogMCwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAi
bG9ja2luZ19pbnZlbnRvcnlbcmFuaz0wXS5waTRfcXVvdGllbnQgZXF1YWwiLAogICAibm90ZSI6
ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIkcyIiwKICAgImNoYXQiOiAi
RzIiLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJsb2NraW5nX2ludmVudG9yeVtyYW5r
PTBdLkgwIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiAxLAogICAiY2hhdCI6IDEsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjog
ImxvY2tpbmdfaW52ZW50b3J5W3Jhbms9MV0ucmFuayB0eXBlZCIsCiAgICJub3RlIjogInR5cGUg
aW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEsCiAgICJjaGF0IjogMSwK
ICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0xXS5y
YW5rIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJj
YyI6ICJTVTMiLAogICAiY2hhdCI6ICJTVTMiLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6
ICJsb2NraW5nX2ludmVudG9yeVtyYW5rPTFdLkgwIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBz
dHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIlNVMyIsCiAgICJjaGF0Ijog
IlNVMyIsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogImxvY2tpbmdfaW52ZW50b3J5W3Jh
bms9MV0uSDAgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogOCwKICAgImNoYXQiOiA4LAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJs
b2NraW5nX2ludmVudG9yeVtyYW5rPTFdLkgwX2RpbSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUg
aW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDgsCiAgICJjaGF0IjogOCwK
ICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0xXS5I
MF9kaW0gZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAg
ImNjIjogMSwKICAgImNoYXQiOiAxLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJsb2Nr
aW5nX2ludmVudG9yeVtyYW5rPTFdLnBpMF9nZW5lcmljIHR5cGVkIiwKICAgIm5vdGUiOiAidHlw
ZSBpbnQiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMSwKICAgImNoYXQiOiAx
LAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJsb2NraW5nX2ludmVudG9yeVtyYW5rPTFd
LnBpMF9nZW5lcmljIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwK
ICB7CiAgICJjYyI6IFsKICAgIDIsCiAgICAyLAogICAgMSwKICAgIDEsCiAgICAxCiAgIF0sCiAg
ICJjaGF0IjogWwogICAgMiwKICAgIDIsCiAgICAxLAogICAgMSwKICAgIDEKICAgXSwKICAgImNo
ZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0xXS5zbDJfZ2Vu
ZXJhdG9yX2pvcmRhbl90eXBlIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBsaXN0IiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IFsKICAgIDIsCiAgICAyLAogICAgMSwKICAgIDEs
CiAgICAxCiAgIF0sCiAgICJjaGF0IjogWwogICAgMiwKICAgIDIsCiAgICAxLAogICAgMSwKICAg
IDEKICAgXSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlb
cmFuaz0xXS5zbDJfZ2VuZXJhdG9yX2pvcmRhbl90eXBlIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEsCiAgICJjaGF0IjogMSwKICAgImNo
ZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0xXS5zbDJfZ2Vu
ZXJhdG9yX2luZGV4IHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBpbnQiLAogICAicGFzcyI6IHRy
dWUKICB9LAogIHsKICAgImNjIjogMSwKICAgImNoYXQiOiAxLAogICAiY2hlY2siOiAiQzEiLAog
ICAibmFtZSI6ICJsb2NraW5nX2ludmVudG9yeVtyYW5rPTFdLnNsMl9nZW5lcmF0b3JfaW5kZXgg
ZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
dHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJsb2Nr
aW5nX2ludmVudG9yeVtyYW5rPTFdLnBpM19pbmplY3RpdmUgdHlwZWQiLAogICAibm90ZSI6ICJ0
eXBlIGJvb2wiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNo
YXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJsb2NraW5nX2ludmVudG9y
eVtyYW5rPTFdLnBpM19pbmplY3RpdmUgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6
IHRydWUKICB9LAogIHsKICAgImNjIjogMCwKICAgImNoYXQiOiAwLAogICAiY2hlY2siOiAiQzEi
LAogICAibmFtZSI6ICJsb2NraW5nX2ludmVudG9yeVtyYW5rPTFdLnBpNF9xdW90aWVudCB0eXBl
ZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJj
YyI6IDAsCiAgICJjaGF0IjogMCwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2lu
Z19pbnZlbnRvcnlbcmFuaz0xXS5waTRfcXVvdGllbnQgZXF1YWwiLAogICAibm90ZSI6ICIiLAog
ICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIlNVMyIsCiAgICJjaGF0IjogIlNVMyIs
CiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogImxvY2tpbmdfaW52ZW50b3J5W3Jhbms9MV0u
SDAgaW4gZG9tYWluIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAg
ICJjYyI6IDIsCiAgICJjaGF0IjogMiwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9j
a2luZ19pbnZlbnRvcnlbcmFuaz0yXS5yYW5rIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBpbnQi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMiwKICAgImNoYXQiOiAyLAogICAi
Y2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJsb2NraW5nX2ludmVudG9yeVtyYW5rPTJdLnJhbmsg
ZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
IlNVMl9sb25nIiwKICAgImNoYXQiOiAiU1UyX2xvbmciLAogICAiY2hlY2siOiAiQzEiLAogICAi
bmFtZSI6ICJsb2NraW5nX2ludmVudG9yeVtyYW5rPTJdLkgwIHR5cGVkIiwKICAgIm5vdGUiOiAi
dHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIlNVMl9sb25nIiwK
ICAgImNoYXQiOiAiU1UyX2xvbmciLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJsb2Nr
aW5nX2ludmVudG9yeVtyYW5rPTJdLkgwIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDMsCiAgICJjaGF0IjogMywKICAgImNoZWNrIjogIkMx
IiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0yXS5IMF9kaW0gdHlwZWQiLAog
ICAibm90ZSI6ICJ0eXBlIGludCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAz
LAogICAiY2hhdCI6IDMsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogImxvY2tpbmdfaW52
ZW50b3J5W3Jhbms9Ml0uSDBfZGltIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IDEsCiAgICJjaGF0IjogMSwKICAgImNoZWNrIjogIkMxIiwK
ICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0yXS5waTBfZ2VuZXJpYyB0eXBlZCIs
CiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
IDEsCiAgICJjaGF0IjogMSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19p
bnZlbnRvcnlbcmFuaz0yXS5waTBfZ2VuZXJpYyBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBbCiAgICAyLAogICAgMiwKICAgIDEsCiAgICAx
LAogICAgMQogICBdLAogICAiY2hhdCI6IFsKICAgIDIsCiAgICAyLAogICAgMSwKICAgIDEsCiAg
ICAxCiAgIF0sCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogImxvY2tpbmdfaW52ZW50b3J5
W3Jhbms9Ml0uc2wyX2dlbmVyYXRvcl9qb3JkYW5fdHlwZSB0eXBlZCIsCiAgICJub3RlIjogInR5
cGUgbGlzdCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBbCiAgICAyLAogICAg
MiwKICAgIDEsCiAgICAxLAogICAgMQogICBdLAogICAiY2hhdCI6IFsKICAgIDIsCiAgICAyLAog
ICAgMSwKICAgIDEsCiAgICAxCiAgIF0sCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogImxv
Y2tpbmdfaW52ZW50b3J5W3Jhbms9Ml0uc2wyX2dlbmVyYXRvcl9qb3JkYW5fdHlwZSBlcXVhbCIs
CiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxLAogICAi
Y2hhdCI6IDEsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogImxvY2tpbmdfaW52ZW50b3J5
W3Jhbms9Ml0uc2wyX2dlbmVyYXRvcl9pbmRleCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEsCiAgICJjaGF0IjogMSwKICAg
ImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0yXS5zbDJf
Z2VuZXJhdG9yX2luZGV4IGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkMxIiwK
ICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0yXS5waTNfaW5qZWN0aXZlIHR5cGVk
IiwKICAgIm5vdGUiOiAidHlwZSBib29sIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJj
YyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAi
bG9ja2luZ19pbnZlbnRvcnlbcmFuaz0yXS5waTNfaW5qZWN0aXZlIGVxdWFsIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDAsCiAgICJjaGF0IjogMCwK
ICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAibG9ja2luZ19pbnZlbnRvcnlbcmFuaz0yXS5w
aTRfcXVvdGllbnQgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGludCIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiAwLAogICAiY2hhdCI6IDAsCiAgICJjaGVjayI6ICJDMSIsCiAg
ICJuYW1lIjogImxvY2tpbmdfaW52ZW50b3J5W3Jhbms9Ml0ucGk0X3F1b3RpZW50IGVxdWFsIiwK
ICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJTVTJfbG9u
ZyIsCiAgICJjaGF0IjogIlNVMl9sb25nIiwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAi
bG9ja2luZ19pbnZlbnRvcnlbcmFuaz0yXS5IMCBpbiBkb21haW4iLAogICAibm90ZSI6ICIiLAog
ICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAog
ICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDEuaG9sZHMgdHlwZWQiLAogICAi
bm90ZSI6ICJ0eXBlIGJvb2wiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1
ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEu
VDEuaG9sZHMgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogMSwKICAgImNoYXQiOiAxLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJw
aGFzZTEuVDEuY2hpMzJfbm9ybSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEsCiAgICJjaGF0IjogMSwKICAgImNoZWNrIjog
IkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQxLmNoaTMyX25vcm0gZXF1YWwiLAogICAibm90ZSI6
ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogNCwKICAgImNoYXQiOiA0LAog
ICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDEuY2hpMzJfYXRfMSB0eXBlZCIs
CiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
IDQsCiAgICJjaGF0IjogNCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQx
LmNoaTMyX2F0XzEgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogLTQsCiAgICJjaGF0IjogLTQsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1l
IjogInBoYXNlMS5UMS5jaGkzMl9hdF9taW51czEgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGlu
dCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAtNCwKICAgImNoYXQiOiAtNCwK
ICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQxLmNoaTMyX2F0X21pbnVzMSBl
cXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAt
MSwKICAgImNoYXQiOiAtMSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQx
LmZzX2luZGljYXRvciB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IC0xLAogICAiY2hhdCI6IC0xLAogICAiY2hlY2siOiAiQzIi
LAogICAibmFtZSI6ICJwaGFzZTEuVDEuZnNfaW5kaWNhdG9yIGVxdWFsIiwKICAgIm5vdGUiOiAi
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1
ZSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQxLnNldmVuX3JlYWwgdHlw
ZWQiLAogICAibm90ZSI6ICJ0eXBlIGJvb2wiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAg
ImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6
ICJwaGFzZTEuVDEuc2V2ZW5fcmVhbCBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjog
dHJ1ZQogIH0sCiAgewogICAiY2MiOiAwLAogICAiY2hhdCI6IDAsCiAgICJjaGVjayI6ICJDMiIs
CiAgICJuYW1lIjogInBoYXNlMS5UMS5xdWFydGV0X211bHRpcGxpY2l0eV91cHBlciB0eXBlZCIs
CiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
IDAsCiAgICJjaGF0IjogMCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQx
LnF1YXJ0ZXRfbXVsdGlwbGljaXR5X3VwcGVyIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNo
ZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQxLnBoYXNlX2NoYXJfb25fMk9fdHJpdmlh
bCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9vbCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMiIsCiAgICJu
YW1lIjogInBoYXNlMS5UMS5waGFzZV9jaGFyX29uXzJPX3RyaXZpYWwgZXF1YWwiLAogICAibm90
ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogWwogICAgMiwKICAgIDIs
CiAgICAxLAogICAgMSwKICAgIDEKICAgXSwKICAgImNoYXQiOiBbCiAgICAyLAogICAgMiwKICAg
IDEsCiAgICAxLAogICAgMQogICBdLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFz
ZTEuVDEuYnJhbmNoaW5nX2xvbmdfcm9vdCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgbGlzdCIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBbCiAgICAyLAogICAgMiwKICAgIDEs
CiAgICAxLAogICAgMQogICBdLAogICAiY2hhdCI6IFsKICAgIDIsCiAgICAyLAogICAgMSwKICAg
IDEsCiAgICAxCiAgIF0sCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMS5i
cmFuY2hpbmdfbG9uZ19yb290IGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IFsKICAgIDMsCiAgICAyLAogICAgMgogICBdLAogICAiY2hhdCI6
IFsKICAgIDMsCiAgICAyLAogICAgMgogICBdLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6
ICJwaGFzZTEuVDEuYnJhbmNoaW5nX3Nob3J0X3Jvb3QgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBl
IGxpc3QiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogWwogICAgMywKICAgIDIs
CiAgICAyCiAgIF0sCiAgICJjaGF0IjogWwogICAgMywKICAgIDIsCiAgICAyCiAgIF0sCiAgICJj
aGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMS5icmFuY2hpbmdfc2hvcnRfcm9vdCBl
cXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBb
CiAgICAzLAogICAgMywKICAgIDEKICAgXSwKICAgImNoYXQiOiBbCiAgICAzLAogICAgMywKICAg
IDEKICAgXSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQxLmJyYW5jaGlu
Z19zdTNfc2wyIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBsaXN0IiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IFsKICAgIDMsCiAgICAzLAogICAgMQogICBdLAogICAiY2hhdCI6
IFsKICAgIDMsCiAgICAzLAogICAgMQogICBdLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6
ICJwaGFzZTEuVDEuYnJhbmNoaW5nX3N1M19zbDIgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogWwogICAgNwogICBdLAogICAiY2hhdCI6IFsK
ICAgIDcKICAgXSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQxLmJyYW5j
aGluZ19wcmluY2lwYWwgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGxpc3QiLAogICAicGFzcyI6
IHRydWUKICB9LAogIHsKICAgImNjIjogWwogICAgNwogICBdLAogICAiY2hhdCI6IFsKICAgIDcK
ICAgXSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQxLmJyYW5jaGluZ19w
cmluY2lwYWwgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogMSwKICAgImNoYXQiOiAxLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJw
aGFzZTEuVDEuY29udHJvbF9zeW0zX3F1YXJ0ZXRfbXVsdCB0eXBlZCIsCiAgICJub3RlIjogInR5
cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEsCiAgICJjaGF0Ijog
MSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQxLmNvbnRyb2xfc3ltM19x
dWFydGV0X211bHQgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzIiLAogICAi
bmFtZSI6ICJwaGFzZTEuVDIuaG9sZHMgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGJvb2wiLAog
ICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAog
ICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDIuaG9sZHMgZXF1YWwiLAogICAi
bm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMTQsCiAgICJjaGF0
IjogMTQsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMi5kaW1fZGVyIHR5
cGVkIiwKICAgIm5vdGUiOiAidHlwZSBpbnQiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAg
ImNjIjogMTQsCiAgICJjaGF0IjogMTQsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBo
YXNlMS5UMi5kaW1fZGVyIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6IDIxLAogICAiY2hhdCI6IDIxLAogICAiY2hlY2siOiAiQzIiLAogICAi
bmFtZSI6ICJwaGFzZTEuVDIuZGltX2JpdmVjdG9yc183IHR5cGVkIiwKICAgIm5vdGUiOiAidHlw
ZSBpbnQiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMjEsCiAgICJjaGF0Ijog
MjEsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMi5kaW1fYml2ZWN0b3Jz
XzcgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogMTUsCiAgICJjaGF0IjogMTUsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MS5UMi5kaW1fYml2ZWN0b3JzXzYgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGludCIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxNSwKICAgImNoYXQiOiAxNSwKICAgImNoZWNr
IjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQyLmRpbV9iaXZlY3RvcnNfNiBlcXVhbCIsCiAg
ICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAi
Y2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMi5nMl9p
bl9zcGluNyB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9vbCIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMiIs
CiAgICJuYW1lIjogInBoYXNlMS5UMi5nMl9pbl9zcGluNyBlcXVhbCIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA4LAogICAiY2hhdCI6IDgsCiAgICJj
aGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMi5kaW1fZzJfY2FwX3N1NCB0eXBlZCIs
CiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
IDgsCiAgICJjaGF0IjogOCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQy
LmRpbV9nMl9jYXBfc3U0IGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6IDQ4LAogICAiY2hhdCI6IDQ4LAogICAiY2hlY2siOiAiQzIiLAogICAi
bmFtZSI6ICJwaGFzZTEuVDIuc3Bpbm9yXzJPX29yZGVyIHR5cGVkIiwKICAgIm5vdGUiOiAidHlw
ZSBpbnQiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogNDgsCiAgICJjaGF0Ijog
NDgsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMi5zcGlub3JfMk9fb3Jk
ZXIgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogMSwKICAgImNoYXQiOiAxLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEu
VDIuc3Bpbm9yXzJPX2F1dG9tb3JwaGlzbV9jb3VudCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUg
aW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEsCiAgICJjaGF0IjogMSwK
ICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQyLnNwaW5vcl8yT19hdXRvbW9y
cGhpc21fY291bnQgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogMiwKICAgImNoYXQiOiAyLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6
ICJwaGFzZTEuVDIuc3Bpbm9yXzJPX3F1YXJ0ZXRfbXVsdCB0eXBlZCIsCiAgICJub3RlIjogInR5
cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDIsCiAgICJjaGF0Ijog
MiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQyLnNwaW5vcl8yT19xdWFy
dGV0X211bHQgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogMzM2LAogICAiY2hhdCI6IDMzNiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUi
OiAicGhhc2UxLlQyLnNsMjdfb3JkZXIgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGludCIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAzMzYsCiAgICJjaGF0IjogMzM2LAogICAi
Y2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDIuc2wyN19vcmRlciBlcXVhbCIsCiAg
ICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAyLAogICAiY2hh
dCI6IDIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMi5zbDI3X3NxMV9j
b3VudCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwK
ICB7CiAgICJjYyI6IDIsCiAgICJjaGF0IjogMiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUi
OiAicGhhc2UxLlQyLnNsMjdfc3ExX2NvdW50IGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDIyLAogICAiY2hhdCI6IDIyLAogICAiY2hlY2si
OiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDIuZnNfc3VtX29yZGluYXJ5IHR5cGVkIiwKICAg
Im5vdGUiOiAidHlwZSBpbnQiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMjIs
CiAgICJjaGF0IjogMjIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMi5m
c19zdW1fb3JkaW5hcnkgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogWwogICAgLTEsCiAgICAwCiAgIF0sCiAgICJjaGF0IjogWwogICAgLTEs
CiAgICAwCiAgIF0sCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMi5udTRf
YWxsb3dlZCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgbGlzdCIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiBbCiAgICAtMSwKICAgIDAKICAgXSwKICAgImNoYXQiOiBbCiAgICAt
MSwKICAgIDAKICAgXSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQyLm51
NF9hbGxvd2VkIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IC0xLAogICAiY2hhdCI6IC0xLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6
ICJwaGFzZTEuVDIuaW52b2x1dGlvbl90cmFjZSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IC0xLAogICAiY2hhdCI6IC0xLAog
ICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDIuaW52b2x1dGlvbl90cmFjZSBl
cXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0
cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MS5UMi5zaWdtYV9IX2lzX2F1dG9tb3JwaGlzbSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9v
bCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRy
dWUsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMi5zaWdtYV9IX2lzX2F1
dG9tb3JwaGlzbSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiBmYWxzZSwKICAgImNoYXQiOiBmYWxzZSwKICAgImNoZWNrIjogIkMyIiwKICAg
Im5hbWUiOiAicGhhc2UxLlQyLnNpbmdsZV91bml0X25lZ2F0aW9uX2lzX2F1dG9tb3JwaGlzbSB0
eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9vbCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewog
ICAiY2MiOiBmYWxzZSwKICAgImNoYXQiOiBmYWxzZSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5h
bWUiOiAicGhhc2UxLlQyLnNpbmdsZV91bml0X25lZ2F0aW9uX2lzX2F1dG9tb3JwaGlzbSBlcXVh
bCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVl
LAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5U
Mi5jb250cm9sXzEzNDRfYWxsX2F1dG9tb3JwaGlzbXMgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBl
IGJvb2wiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQi
OiB0cnVlLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDIuY29udHJvbF8x
MzQ0X2FsbF9hdXRvbW9ycGhpc21zIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IDEzNDQsCiAgICJjaGF0IjogMTM0NCwKICAgImNoZWNrIjog
IkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQyLmdyb3VwMTM0NF9vcmRlciB0eXBlZCIsCiAgICJu
b3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEzNDQs
CiAgICJjaGF0IjogMTM0NCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQy
Lmdyb3VwMTM0NF9vcmRlciBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IDAuNzA3MTA2NzgxMTg2NTQ5NSwKICAg
ImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQyLnNwaW5vcl8yT19taW5fYXV0b21v
cnBoaXNtX2RlZmVjdCAoY2hhdCkgZ3QgMWUtMDYiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6
IHRydWUKICB9LAogIHsKICAgImNjIjogMC43MDcxMDY3ODExODY1NDk1LAogICAiY2hhdCI6IG51
bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMi5zcGlub3JfMk9fbWlu
X2F1dG9tb3JwaGlzbV9kZWZlY3QgKGNjKSBndCAxZS0wNiIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJj
aGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMy5ob2xkcyB0eXBlZCIsCiAgICJub3Rl
IjogInR5cGUgYm9vbCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAog
ICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMy5o
b2xkcyBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiAwLAogICAiY2hhdCI6IDAsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MS5UMy5waTFfRzIgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGludCIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiAwLAogICAiY2hhdCI6IDAsCiAgICJjaGVjayI6ICJDMiIsCiAg
ICJuYW1lIjogInBoYXNlMS5UMy5waTFfRzIgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFz
cyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIloiLAogICAiY2hhdCI6ICJaIiwKICAgImNoZWNr
IjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQzLnBpM19HMiB0eXBlZCIsCiAgICJub3RlIjog
InR5cGUgc3RyIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJaIiwKICAgImNo
YXQiOiAiWiIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMy5waTNfRzIg
ZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
MCwKICAgImNoYXQiOiAwLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDMu
cGk0X0cyIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBpbnQiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogMCwKICAgImNoYXQiOiAwLAogICAiY2hlY2siOiAiQzIiLAogICAibmFt
ZSI6ICJwaGFzZTEuVDMucGk0X0cyIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IDAsCiAgICJjaGF0IjogMCwKICAgImNoZWNrIjogIkMyIiwK
ICAgIm5hbWUiOiAicGhhc2UxLlQzLnBpMV9WIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBpbnQi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMCwKICAgImNoYXQiOiAwLAogICAi
Y2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDMucGkxX1YgZXF1YWwiLAogICAibm90
ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMCwKICAgImNoYXQiOiAw
LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDMucGk0X1YgdHlwZWQiLAog
ICAibm90ZSI6ICJ0eXBlIGludCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAw
LAogICAiY2hhdCI6IDAsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UMy5w
aTRfViBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjog
InBoYXNlMS5UMy5ub19pbnRlcm5hbF9kb3VibGVfY292ZXIgdHlwZWQiLAogICAibm90ZSI6ICJ0
eXBlIGJvb2wiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNo
YXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDMubm9faW50
ZXJuYWxfZG91YmxlX2NvdmVyIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkMy
IiwKICAgIm5hbWUiOiAicGhhc2UxLlQzLmVudmVsb3BlX2luX09fa2lsbCB0eXBlZCIsCiAgICJu
b3RlIjogInR5cGUgYm9vbCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVl
LAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5U
My5lbnZlbG9wZV9pbl9PX2tpbGwgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRy
dWUKICB9LAogIHsKICAgImNjIjogIloyIiwKICAgImNoYXQiOiAiWjIiLAogICAiY2hlY2siOiAi
QzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDMuY29udHJvbHNfcGk0X1MyIHR5cGVkIiwKICAgIm5v
dGUiOiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIloyIiwK
ICAgImNoYXQiOiAiWjIiLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDMu
Y29udHJvbHNfcGk0X1MyIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6ICJaMiIsCiAgICJjaGF0IjogIloyIiwKICAgImNoZWNrIjogIkMyIiwK
ICAgIm5hbWUiOiAicGhhc2UxLlQzLmNvbnRyb2xzX3BpNF9TMyB0eXBlZCIsCiAgICJub3RlIjog
InR5cGUgc3RyIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJaMiIsCiAgICJj
aGF0IjogIloyIiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQzLmNvbnRy
b2xzX3BpNF9TMyBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiAyNCwKICAgImNoYXQiOiAyNCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUi
OiAicGhhc2UxLlQzLmNvbnRyb2xzX3BpMV9TTzNfbW9kX1QgdHlwZWQiLAogICAibm90ZSI6ICJ0
eXBlIGludCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAyNCwKICAgImNoYXQi
OiAyNCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQzLmNvbnRyb2xzX3Bp
MV9TTzNfbW9kX1QgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzIiLAogICAi
bmFtZSI6ICJwaGFzZTEuVDQuaG9sZHMgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGJvb2wiLAog
ICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAog
ICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDQuaG9sZHMgZXF1YWwiLAogICAi
bm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMjQsCiAgICJjaGF0
IjogMjQsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UNC5saWZ0c190b3Rh
bCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IDI0LAogICAiY2hhdCI6IDI0LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6
ICJwaGFzZTEuVDQubGlmdHNfdG90YWwgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6
IHRydWUKICB9LAogIHsKICAgImNjIjogMTIsCiAgICJjaGF0IjogMTIsCiAgICJjaGVjayI6ICJD
MiIsCiAgICJuYW1lIjogInBoYXNlMS5UNC5vcmRlcjJfY291bnQgdHlwZWQiLAogICAibm90ZSI6
ICJ0eXBlIGludCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxMiwKICAgImNo
YXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQ0Lm9yZGVyMl9j
b3VudCBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiBbCiAgICAtMQogICBdLAogICAiY2hhdCI6IFsKICAgIC0xCiAgIF0sCiAgICJjaGVjayI6
ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UNC5vcmRlcjJfdHJhY2VzX3NldCB0eXBlZCIsCiAg
ICJub3RlIjogInR5cGUgbGlzdCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBb
CiAgICAtMQogICBdLAogICAiY2hhdCI6IFsKICAgIC0xCiAgIF0sCiAgICJjaGVjayI6ICJDMiIs
CiAgICJuYW1lIjogInBoYXNlMS5UNC5vcmRlcjJfdHJhY2VzX3NldCBlcXVhbCIsCiAgICJub3Rl
IjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxMiwKICAgImNoYXQiOiAx
MiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQ0Lm9yZGVyNF9jb3VudCB0
eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAg
ICJjYyI6IDEyLAogICAiY2hhdCI6IDEyLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJw
aGFzZTEuVDQub3JkZXI0X2NvdW50IGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IFsKICAgIC0xLAogICAgMwogICBdLAogICAiY2hhdCI6IFsK
ICAgIC0xLAogICAgMwogICBdLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEu
VDQub3JkZXI0X3RyYWNlc19zZXQgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGxpc3QiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogWwogICAgLTEsCiAgICAzCiAgIF0sCiAgICJj
aGF0IjogWwogICAgLTEsCiAgICAzCiAgIF0sCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjog
InBoYXNlMS5UNC5vcmRlcjRfdHJhY2VzX3NldCBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAzLAogICAiY2hhdCI6IDMsCiAgICJjaGVjayI6
ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UNC5wZXJtX2NoYXJfaW52b2x1dGlvbiB0eXBlZCIs
CiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
IDMsCiAgICJjaGF0IjogMywKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQ0
LnBlcm1fY2hhcl9pbnZvbHV0aW9uIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IDIsCiAgICJjaGF0IjogMiwKICAgImNoZWNrIjogIkMyIiwK
ICAgIm5hbWUiOiAicGhhc2UxLlQ0LnJobzZfY2hhcl8yQSB0eXBlZCIsCiAgICJub3RlIjogInR5
cGUgaW50IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDIsCiAgICJjaGF0Ijog
MiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLlQ0LnJobzZfY2hhcl8yQSBl
cXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA0
LAogICAiY2hhdCI6IDQsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UNC5n
YXAgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGludCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiA0LAogICAiY2hhdCI6IDQsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjog
InBoYXNlMS5UNC5nYXAgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzIiLAog
ICAibmFtZSI6ICJwaGFzZTEuVDQuY29udHJvbF9GMjFfdW5zaWduZWRfMV8zXzNiYXIgdHlwZWQi
LAogICAibm90ZSI6ICJ0eXBlIGJvb2wiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJw
aGFzZTEuVDQuY29udHJvbF9GMjFfdW5zaWduZWRfMV8zXzNiYXIgZXF1YWwiLAogICAibm90ZSI6
ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0
cnVlLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTEuVDQubnUyX3Vuc2lnbmVk
X2F1dG9tb3JwaGlzbSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9vbCIsCiAgICJwYXNzIjog
dHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6
ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5UNC5udTJfdW5zaWduZWRfYXV0b21vcnBoaXNtIGVx
dWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEz
NDQsCiAgICJjaGF0IjogMTM0NCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2Ux
Lmdyb3VwMTM0NC5vcmRlciB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEzNDQsCiAgICJjaGF0IjogMTM0NCwKICAgImNoZWNr
IjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLmdyb3VwMTM0NC5vcmRlciBlcXVhbCIsCiAgICJu
b3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBmYWxzZSwKICAgImNo
YXQiOiBmYWxzZSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UxLmdyb3VwMTM0
NC5zcGxpdCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9vbCIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiBmYWxzZSwKICAgImNoYXQiOiBmYWxzZSwKICAgImNoZWNrIjogIkMy
IiwKICAgIm5hbWUiOiAicGhhc2UxLmdyb3VwMTM0NC5zcGxpdCBlcXVhbCIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAwLAogICAiY2hhdCI6IDAsCiAg
ICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5ncm91cDEzNDQuY29tcGxlbWVudHNf
Zm91bmQgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGludCIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiAwLAogICAiY2hhdCI6IDAsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1l
IjogInBoYXNlMS5ncm91cDEzNDQuY29tcGxlbWVudHNfZm91bmQgZXF1YWwiLAogICAibm90ZSI6
ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogNjQsCiAgICJjaGF0IjogNjQs
CiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMS5ncm91cDEzNDQubGlmdF9wYWly
c190ZXN0ZWQgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGludCIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiA2NCwKICAgImNoYXQiOiA2NCwKICAgImNoZWNrIjogIkMyIiwKICAg
Im5hbWUiOiAicGhhc2UxLmdyb3VwMTM0NC5saWZ0X3BhaXJzX3Rlc3RlZCBlcXVhbCIsCiAgICJu
b3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hh
dCI6IHRydWUsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuUF9DLmNvbXBs
ZXhfdW5pdF9jZW50cmFsIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBib29sIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNr
IjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5QX0MuY29tcGxleF91bml0X2NlbnRyYWwgZXF1
YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1
ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFi
LlBfQy5lOF9hbnRpY29tbXV0ZXMgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGJvb2wiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAi
Y2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLlBfQy5lOF9hbnRpY29tbXV0ZXMgZXF1
YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogZmFs
c2UsCiAgICJjaGF0IjogZmFsc2UsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNl
MWIuUF9DLmU4X2NlbnRyYWwgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGJvb2wiLAogICAicGFz
cyI6IHRydWUKICB9LAogIHsKICAgImNjIjogZmFsc2UsCiAgICJjaGF0IjogZmFsc2UsCiAgICJj
aGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuUF9DLmU4X2NlbnRyYWwgZXF1YWwiLAog
ICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIkNMT1NFRC1C
WS1JTlNUQU5USUFUSU9OIiwKICAgImNoYXQiOiAiQ0xPU0VELUJZLUlOU1RBTlRJQVRJT04iLAog
ICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLlBfQy5kaXNwb3NpdGlvbiB0eXBl
ZCIsCiAgICJub3RlIjogInR5cGUgc3RyIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJj
YyI6ICJDTE9TRUQtQlktSU5TVEFOVElBVElPTiIsCiAgICJjaGF0IjogIkNMT1NFRC1CWS1JTlNU
QU5USUFUSU9OIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5QX0MuZGlz
cG9zaXRpb24gZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogImZhaWwiLAogICAiY2hhdCI6ICJmYWlsIiwKICAgImNoZWNrIjogIkMzIiwKICAg
Im5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMS5pIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBz
dHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogImZhaWwiLAogICAiY2hhdCI6
ICJmYWlsIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5I
MS5pIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJj
YyI6ICJwYXNzIiwKICAgImNoYXQiOiAicGFzcyIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1l
IjogInBoYXNlMWIuSF9zY3JlZW4uSDEuaWkgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIHN0ciIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAicGFzcyIsCiAgICJjaGF0IjogInBh
c3MiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgxLmlp
IGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
ICJmYWlsIiwKICAgImNoYXQiOiAiZmFpbCIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjog
InBoYXNlMWIuSF9zY3JlZW4uSDEuaWlpIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBzdHIiLAog
ICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogImZhaWwiLAogICAiY2hhdCI6ICJmYWls
IiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMS5paWkg
ZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
Im4vYSIsCiAgICJjaGF0IjogIm4vYSIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBo
YXNlMWIuSF9zY3JlZW4uSDEuaXYgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIHN0ciIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAibi9hIiwKICAgImNoYXQiOiAibi9hIiwKICAg
ImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMS5pdiBlcXVhbCIs
CiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiRVhDTFVE
RUQoaSxpaWkpIiwKICAgImNoYXQiOiAiRVhDTFVERUQoaSxpaWkpIiwKICAgImNoZWNrIjogIkMz
IiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMS5jb2RlIHR5cGVkIiwKICAgIm5vdGUi
OiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIkVYQ0xVREVE
KGksaWlpKSIsCiAgICJjaGF0IjogIkVYQ0xVREVEKGksaWlpKSIsCiAgICJjaGVjayI6ICJDMyIs
CiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDEuY29kZSBlcXVhbCIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiY29udHJvbCIsCiAgICJjaGF0
IjogImNvbnRyb2wiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2Ny
ZWVuLkgxLnJvbGUgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIHN0ciIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiAiY29udHJvbCIsCiAgICJjaGF0IjogImNvbnRyb2wiLAogICAi
Y2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgxLnJvbGUgZXF1YWwi
LAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwK
ICAgImNoYXQiOiAiZmFpbCIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIu
SF9zY3JlZW4uSDEuaSAoY2hhdCkgaW4gZG9tYWluIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJmYWlsIiwKICAgImNoYXQiOiBudWxsLAogICAiY2hl
Y2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgxLmkgKGNjKSBpbiBkb21h
aW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVs
bCwKICAgImNoYXQiOiAicGFzcyIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNl
MWIuSF9zY3JlZW4uSDEuaWkgKGNoYXQpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAicGFzcyIsCiAgICJjaGF0IjogbnVsbCwKICAg
ImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMS5paSAoY2MpIGlu
IGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiBudWxsLAogICAiY2hhdCI6ICJmYWlsIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAi
cGhhc2UxYi5IX3NjcmVlbi5IMS5paWkgKGNoYXQpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiZmFpbCIsCiAgICJjaGF0IjogbnVs
bCwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMS5paWkg
KGNjKSBpbiBkb21haW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAibi9hIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5h
bWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMS5pdiAoY2hhdCkgaW4gZG9tYWluIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJuL2EiLAogICAiY2hhdCI6
IG51bGwsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDEu
aXYgKGNjKSBpbiBkb21haW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogInBhc3MiLAogICAiY2hhdCI6ICJwYXNzIiwKICAgImNoZWNrIjogIkMzIiwK
ICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMi5pIHR5cGVkIiwKICAgIm5vdGUiOiAidHlw
ZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogInBhc3MiLAogICAiY2hh
dCI6ICJwYXNzIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVl
bi5IMi5pIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAg
ICJjYyI6ICJwYXNzIiwKICAgImNoYXQiOiAicGFzcyIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJu
YW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDIuaWkgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIHN0
ciIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAicGFzcyIsCiAgICJjaGF0Ijog
InBhc3MiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgy
LmlpIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJj
YyI6ICJwYXNzIiwKICAgImNoYXQiOiAicGFzcyIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1l
IjogInBoYXNlMWIuSF9zY3JlZW4uSDIuaWlpIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBzdHIi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogInBhc3MiLAogICAiY2hhdCI6ICJw
YXNzIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMi5p
aWkgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogImR5bmFtaWNhbCIsCiAgICJjaGF0IjogImR5bmFtaWNhbCIsCiAgICJjaGVjayI6ICJDMyIs
CiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDIuaXYgdHlwZWQiLAogICAibm90ZSI6ICJ0
eXBlIHN0ciIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiZHluYW1pY2FsIiwK
ICAgImNoYXQiOiAiZHluYW1pY2FsIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhh
c2UxYi5IX3NjcmVlbi5IMi5pdiBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiAiQURNSVNTSUJMRS1JTVBPUlQiLAogICAiY2hhdCI6ICJBRE1J
U1NJQkxFLUlNUE9SVCIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9z
Y3JlZW4uSDIuY29kZSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgc3RyIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6ICJBRE1JU1NJQkxFLUlNUE9SVCIsCiAgICJjaGF0IjogIkFE
TUlTU0lCTEUtSU1QT1JUIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5I
X3NjcmVlbi5IMi5jb2RlIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6ICJjYW5kaWRhdGUiLAogICAiY2hhdCI6ICJjYW5kaWRhdGUiLAogICAi
Y2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgyLnJvbGUgdHlwZWQi
LAogICAibm90ZSI6ICJ0eXBlIHN0ciIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiAiY2FuZGlkYXRlIiwKICAgImNoYXQiOiAiY2FuZGlkYXRlIiwKICAgImNoZWNrIjogIkMzIiwK
ICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMi5yb2xlIGVxdWFsIiwKICAgIm5vdGUiOiAi
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogInBh
c3MiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgyLmkg
KGNoYXQpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiAicGFzcyIsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMzIiwKICAg
Im5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMi5pIChjYykgaW4gZG9tYWluIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0Ijog
InBhc3MiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgy
LmlpIChjaGF0KSBpbiBkb21haW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogInBhc3MiLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMyIs
CiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDIuaWkgKGNjKSBpbiBkb21haW4iLAogICAi
bm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNo
YXQiOiAicGFzcyIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3Jl
ZW4uSDIuaWlpIChjaGF0KSBpbiBkb21haW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRy
dWUKICB9LAogIHsKICAgImNjIjogInBhc3MiLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6
ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDIuaWlpIChjYykgaW4gZG9tYWlu
IiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGws
CiAgICJjaGF0IjogImR5bmFtaWNhbCIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBo
YXNlMWIuSF9zY3JlZW4uSDIuaXYgKGNoYXQpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiZHluYW1pY2FsIiwKICAgImNoYXQiOiBu
dWxsLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgyLml2
IChjYykgaW4gZG9tYWluIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6ICJwYXNzIiwKICAgImNoYXQiOiAicGFzcyIsCiAgICJjaGVjayI6ICJDMyIsCiAg
ICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDMuaSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUg
c3RyIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJwYXNzIiwKICAgImNoYXQi
OiAicGFzcyIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4u
SDMuaSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiAicGFzcyIsCiAgICJjaGF0IjogInBhc3MiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFt
ZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgzLmlpIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBzdHIi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogInBhc3MiLAogICAiY2hhdCI6ICJw
YXNzIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMy5p
aSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiAiY29uZGl0aW9uYWwiLAogICAiY2hhdCI6ICJjb25kaXRpb25hbCIsCiAgICJjaGVjayI6ICJD
MyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDMuaWlpIHR5cGVkIiwKICAgIm5vdGUi
OiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogImNvbmRpdGlv
bmFsIiwKICAgImNoYXQiOiAiY29uZGl0aW9uYWwiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFt
ZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgzLmlpaSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAia2luZW1hdGljIiwKICAgImNoYXQiOiAia2lu
ZW1hdGljIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5I
My5pdiB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgc3RyIiwKICAgInBhc3MiOiB0cnVlCiAgfSwK
ICB7CiAgICJjYyI6ICJraW5lbWF0aWMiLAogICAiY2hhdCI6ICJraW5lbWF0aWMiLAogICAiY2hl
Y2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgzLml2IGVxdWFsIiwKICAg
Im5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJBRE1JU1NJQkxF
LUlNUE9SVCIsCiAgICJjaGF0IjogIkFETUlTU0lCTEUtSU1QT1JUIiwKICAgImNoZWNrIjogIkMz
IiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMy5jb2RlIHR5cGVkIiwKICAgIm5vdGUi
OiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIkFETUlTU0lC
TEUtSU1QT1JUIiwKICAgImNoYXQiOiAiQURNSVNTSUJMRS1JTVBPUlQiLAogICAiY2hlY2siOiAi
QzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgzLmNvZGUgZXF1YWwiLAogICAibm90
ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogImNhbmRpZGF0ZSIsCiAg
ICJjaGF0IjogImNhbmRpZGF0ZSIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNl
MWIuSF9zY3JlZW4uSDMucm9sZSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgc3RyIiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJjYW5kaWRhdGUiLAogICAiY2hhdCI6ICJjYW5k
aWRhdGUiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgz
LnJvbGUgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAg
ImNjIjogbnVsbCwKICAgImNoYXQiOiAicGFzcyIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1l
IjogInBoYXNlMWIuSF9zY3JlZW4uSDMuaSAoY2hhdCkgaW4gZG9tYWluIiwKICAgIm5vdGUiOiAi
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJwYXNzIiwKICAgImNoYXQiOiBu
dWxsLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgzLmkg
KGNjKSBpbiBkb21haW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAicGFzcyIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJu
YW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDMuaWkgKGNoYXQpIGluIGRvbWFpbiIsCiAgICJub3Rl
IjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAicGFzcyIsCiAgICJjaGF0
IjogbnVsbCwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5I
My5paSAoY2MpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6ICJjb25kaXRpb25hbCIsCiAgICJjaGVjayI6
ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDMuaWlpIChjaGF0KSBpbiBkb21h
aW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogImNv
bmRpdGlvbmFsIiwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6
ICJwaGFzZTFiLkhfc2NyZWVuLkgzLmlpaSAoY2MpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6ICJraW5l
bWF0aWMiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkgz
Lml2IChjaGF0KSBpbiBkb21haW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogImtpbmVtYXRpYyIsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjog
IkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5IMy5pdiAoY2MpIGluIGRvbWFpbiIs
CiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiZmFpbCIs
CiAgICJjaGF0IjogImZhaWwiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFi
Lkhfc2NyZWVuLkg0LmkgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIHN0ciIsCiAgICJwYXNzIjog
dHJ1ZQogIH0sCiAgewogICAiY2MiOiAiZmFpbCIsCiAgICJjaGF0IjogImZhaWwiLAogICAiY2hl
Y2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkg0LmkgZXF1YWwiLAogICAi
bm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogInBhc3MiLAogICAi
Y2hhdCI6ICJwYXNzIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3Nj
cmVlbi5INC5paSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgc3RyIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6ICJwYXNzIiwKICAgImNoYXQiOiAicGFzcyIsCiAgICJjaGVjayI6
ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDQuaWkgZXF1YWwiLAogICAibm90
ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIm4vYSIsCiAgICJjaGF0
IjogIm4vYSIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4u
SDQuaWlpIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogIm4vYSIsCiAgICJjaGF0IjogIm4vYSIsCiAgICJjaGVjayI6ICJDMyIs
CiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDQuaWlpIGVxdWFsIiwKICAgIm5vdGUiOiAi
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJuL2EiLAogICAiY2hhdCI6ICJu
L2EiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkg0Lml2
IHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogIm4vYSIsCiAgICJjaGF0IjogIm4vYSIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJu
YW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDQuaXYgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIkVYQ0xVREVEKGkpIiwKICAgImNoYXQiOiAi
RVhDTFVERUQoaSkiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2Ny
ZWVuLkg0LmNvZGUgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIHN0ciIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiAiRVhDTFVERUQoaSkiLAogICAiY2hhdCI6ICJFWENMVURFRChp
KSIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDQuY29k
ZSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiAiY2FuZGlkYXRlIiwKICAgImNoYXQiOiAiY2FuZGlkYXRlIiwKICAgImNoZWNrIjogIkMzIiwK
ICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5INC5yb2xlIHR5cGVkIiwKICAgIm5vdGUiOiAi
dHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogImNhbmRpZGF0ZSIs
CiAgICJjaGF0IjogImNhbmRpZGF0ZSIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBo
YXNlMWIuSF9zY3JlZW4uSDQucm9sZSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjog
dHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6ICJmYWlsIiwKICAgImNoZWNr
IjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5INC5pIChjaGF0KSBpbiBkb21h
aW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogImZh
aWwiLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNl
MWIuSF9zY3JlZW4uSDQuaSAoY2MpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6ICJwYXNzIiwKICAgImNo
ZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5INC5paSAoY2hhdCkgaW4g
ZG9tYWluIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
ICJwYXNzIiwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJw
aGFzZTFiLkhfc2NyZWVuLkg0LmlpIChjYykgaW4gZG9tYWluIiwKICAgIm5vdGUiOiAiIiwKICAg
InBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogIm4vYSIsCiAg
ICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDQuaWlpIChjaGF0
KSBpbiBkb21haW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAg
ImNjIjogIm4vYSIsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUi
OiAicGhhc2UxYi5IX3NjcmVlbi5INC5paWkgKGNjKSBpbiBkb21haW4iLAogICAibm90ZSI6ICIi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAibi9h
IiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5INC5pdiAo
Y2hhdCkgaW4gZG9tYWluIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6ICJuL2EiLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMyIsCiAgICJu
YW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDQuaXYgKGNjKSBpbiBkb21haW4iLAogICAibm90ZSI6
ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogImZhaWwiLAogICAiY2hhdCI6
ICJmYWlsIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5I
NS5pIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogImZhaWwiLAogICAiY2hhdCI6ICJmYWlsIiwKICAgImNoZWNrIjogIkMzIiwK
ICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5INS5pIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJmYWlsIiwKICAgImNoYXQiOiAiZmFp
bCIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDUuaWkg
dHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIHN0ciIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewog
ICAiY2MiOiAiZmFpbCIsCiAgICJjaGF0IjogImZhaWwiLAogICAiY2hlY2siOiAiQzMiLAogICAi
bmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkg1LmlpIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAg
InBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJuL2EiLAogICAiY2hhdCI6ICJuL2EiLAog
ICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkg1LmlpaSB0eXBl
ZCIsCiAgICJub3RlIjogInR5cGUgc3RyIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJj
YyI6ICJuL2EiLAogICAiY2hhdCI6ICJuL2EiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6
ICJwaGFzZTFiLkhfc2NyZWVuLkg1LmlpaSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAibi9hIiwKICAgImNoYXQiOiAibi9hIiwKICAgImNo
ZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5INS5pdiB0eXBlZCIsCiAg
ICJub3RlIjogInR5cGUgc3RyIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJu
L2EiLAogICAiY2hhdCI6ICJuL2EiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFz
ZTFiLkhfc2NyZWVuLkg1Lml2IGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6ICJFWENMVURFRChpLGlpKSIsCiAgICJjaGF0IjogIkVYQ0xVREVE
KGksaWkpIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5IX3NjcmVlbi5I
NS5jb2RlIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogIkVYQ0xVREVEKGksaWkpIiwKICAgImNoYXQiOiAiRVhDTFVERUQoaSxp
aSkiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkg1LmNv
ZGUgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogImNhbmRpZGF0ZSIsCiAgICJjaGF0IjogImNhbmRpZGF0ZSIsCiAgICJjaGVjayI6ICJDMyIs
CiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDUucm9sZSB0eXBlZCIsCiAgICJub3RlIjog
InR5cGUgc3RyIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJjYW5kaWRhdGUi
LAogICAiY2hhdCI6ICJjYW5kaWRhdGUiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJw
aGFzZTFiLkhfc2NyZWVuLkg1LnJvbGUgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6
IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAiZmFpbCIsCiAgICJjaGVj
ayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDUuaSAoY2hhdCkgaW4gZG9t
YWluIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJm
YWlsIiwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFz
ZTFiLkhfc2NyZWVuLkg1LmkgKGNjKSBpbiBkb21haW4iLAogICAibm90ZSI6ICIiLAogICAicGFz
cyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAiZmFpbCIsCiAgICJj
aGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDUuaWkgKGNoYXQpIGlu
IGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiAiZmFpbCIsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAi
cGhhc2UxYi5IX3NjcmVlbi5INS5paSAoY2MpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6ICJuL2EiLAog
ICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkg1LmlpaSAoY2hh
dCkgaW4gZG9tYWluIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAg
ICJjYyI6ICJuL2EiLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1l
IjogInBoYXNlMWIuSF9zY3JlZW4uSDUuaWlpIChjYykgaW4gZG9tYWluIiwKICAgIm5vdGUiOiAi
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogIm4v
YSIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMWIuSF9zY3JlZW4uSDUuaXYg
KGNoYXQpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiAibi9hIiwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzMiLAogICAi
bmFtZSI6ICJwaGFzZTFiLkhfc2NyZWVuLkg1Lml2IChjYykgaW4gZG9tYWluIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0Ijog
dHJ1ZSwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5JNV9yZWdpc3RlcmVk
IHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBib29sIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkMzIiwKICAgIm5h
bWUiOiAicGhhc2UxYi5JNV9yZWdpc3RlcmVkIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IFsKICAgICJIMiIsCiAgICAiSDMiCiAgIF0sCiAg
ICJjaGF0IjogWwogICAgIkgyIiwKICAgICJIMyIKICAgXSwKICAgImNoZWNrIjogIkMzIiwKICAg
Im5hbWUiOiAicGhhc2UxYi5hZG1pc3NpYmxlIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBsaXN0
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IFsKICAgICJIMiIsCiAgICAiSDMi
CiAgIF0sCiAgICJjaGF0IjogWwogICAgIkgyIiwKICAgICJIMyIKICAgXSwKICAgImNoZWNrIjog
IkMzIiwKICAgIm5hbWUiOiAicGhhc2UxYi5hZG1pc3NpYmxlIGVxdWFsIiwKICAgIm5vdGUiOiAi
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJmYW5vX2xpbmVfdGV4dHVyZV9M
MTI0X2hvbW9nZW5lb3VzX0dQXzJEIiwKICAgImNoYXQiOiAiZmFub19saW5lX3RleHR1cmVfTDEy
NF9ob21vZ2VuZW91c19HUF8yRCIsCiAgICJjaGVjayI6ICJDNCIsCiAgICJuYW1lIjogInBoYXNl
Mi5vYmplY3QgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIHN0ciIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiAiZmFub19saW5lX3RleHR1cmVfTDEyNF9ob21vZ2VuZW91c19HUF8y
RCIsCiAgICJjaGF0IjogImZhbm9fbGluZV90ZXh0dXJlX0wxMjRfaG9tb2dlbmVvdXNfR1BfMkQi
LAogICAiY2hlY2siOiAiQzQiLAogICAibmFtZSI6ICJwaGFzZTIub2JqZWN0IGVxdWFsIiwKICAg
Im5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJub25saW5lX3Rl
eHR1cmVfTDEyMyIsCiAgICJjaGF0IjogIm5vbmxpbmVfdGV4dHVyZV9MMTIzIiwKICAgImNoZWNr
IjogIkM0IiwKICAgIm5hbWUiOiAicGhhc2UyLmNvbnRyb2xfb2JqZWN0IHR5cGVkIiwKICAgIm5v
dGUiOiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIm5vbmxp
bmVfdGV4dHVyZV9MMTIzIiwKICAgImNoYXQiOiAibm9ubGluZV90ZXh0dXJlX0wxMjMiLAogICAi
Y2hlY2siOiAiQzQiLAogICAibmFtZSI6ICJwaGFzZTIuY29udHJvbF9vYmplY3QgZXF1YWwiLAog
ICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogImxvY2tyZWMt
QS0yLjYiLAogICAiY2hhdCI6ICJsb2NrcmVjLUEtMi42IiwKICAgImNoZWNrIjogIkM0IiwKICAg
Im5hbWUiOiAicGhhc2UyLnByb2ZpbGVfaWQgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIHN0ciIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAibG9ja3JlYy1BLTIuNiIsCiAgICJj
aGF0IjogImxvY2tyZWMtQS0yLjYiLAogICAiY2hlY2siOiAiQzQiLAogICAibmFtZSI6ICJwaGFz
ZTIucHJvZmlsZV9pZCBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDNCIsCiAg
ICJuYW1lIjogInBoYXNlMi5PX25vbnplcm9fb25fbGluZSB0eXBlZCIsCiAgICJub3RlIjogInR5
cGUgYm9vbCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hh
dCI6IHRydWUsCiAgICJjaGVjayI6ICJDNCIsCiAgICJuYW1lIjogInBoYXNlMi5PX25vbnplcm9f
b25fbGluZSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewog
ICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDNCIsCiAgICJuYW1l
IjogInBoYXNlMi5PX3plcm9fb25fbm9ubGluZSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9v
bCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRy
dWUsCiAgICJjaGVjayI6ICJDNCIsCiAgICJuYW1lIjogInBoYXNlMi5PX3plcm9fb25fbm9ubGlu
ZSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiAiU080X1N0YWJfSEwiLAogICAiY2hhdCI6ICJTTzRfU3RhYl9ITCIsCiAgICJjaGVjayI6ICJD
NCIsCiAgICJuYW1lIjogInBoYXNlMi5zdGFiX2ludGVybmFsX2ltYWdlIHR5cGVkIiwKICAgIm5v
dGUiOiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIlNPNF9T
dGFiX0hMIiwKICAgImNoYXQiOiAiU080X1N0YWJfSEwiLAogICAiY2hlY2siOiAiQzQiLAogICAi
bmFtZSI6ICJwaGFzZTIuc3RhYl9pbnRlcm5hbF9pbWFnZSBlcXVhbCIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiU1UyX2xvbmciLAogICAiY2hhdCI6
ICJTVTJfbG9uZyIsCiAgICJjaGVjayI6ICJDNCIsCiAgICJuYW1lIjogInBoYXNlMi5zdGFiX2tl
cm5lbCB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgc3RyIiwKICAgInBhc3MiOiB0cnVlCiAgfSwK
ICB7CiAgICJjYyI6ICJTVTJfbG9uZyIsCiAgICJjaGF0IjogIlNVMl9sb25nIiwKICAgImNoZWNr
IjogIkM0IiwKICAgIm5hbWUiOiAicGhhc2UyLnN0YWJfa2VybmVsIGVxdWFsIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0Ijog
dHJ1ZSwKICAgImNoZWNrIjogIkM0IiwKICAgIm5hbWUiOiAicGhhc2UyLnN0YWJfc3ViZGlyZWN0
IHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBib29sIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkM0IiwKICAgIm5h
bWUiOiAicGhhc2UyLnN0YWJfc3ViZGlyZWN0IGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEsCiAgICJjaGF0IjogMSwKICAgImNoZWNrIjog
IkM0IiwKICAgIm5hbWUiOiAicGhhc2UyLnBpMF9zdGFiIHR5cGVkIiwKICAgIm5vdGUiOiAidHlw
ZSBpbnQiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMSwKICAgImNoYXQiOiAx
LAogICAiY2hlY2siOiAiQzQiLAogICAibmFtZSI6ICJwaGFzZTIucGkwX3N0YWIgZXF1YWwiLAog
ICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogWwogICAgIklk
IiwKICAgICJzaWdtYV9IIgogICBdLAogICAiY2hhdCI6IFsKICAgICJJZCIsCiAgICAic2lnbWFf
SCIKICAgXSwKICAgImNoZWNrIjogIkM0IiwKICAgIm5hbWUiOiAicGhhc2UyLmxvb3BfaW1hZ2Vz
IHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBsaXN0IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IFsKICAgICJJZCIsCiAgICAic2lnbWFfSCIKICAgXSwKICAgImNoYXQiOiBbCiAg
ICAiSWQiLAogICAgInNpZ21hX0giCiAgIF0sCiAgICJjaGVjayI6ICJDNCIsCiAgICJuYW1lIjog
InBoYXNlMi5sb29wX2ltYWdlcyBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiA0LAogICAiY2hhdCI6IDQsCiAgICJjaGVjayI6ICJDNCIsCiAg
ICJuYW1lIjogInBoYXNlMi5zaWdtYV9IX2VpZ2VuX3BsdXMxIHR5cGVkIiwKICAgIm5vdGUiOiAi
dHlwZSBpbnQiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogNCwKICAgImNoYXQi
OiA0LAogICAiY2hlY2siOiAiQzQiLAogICAibmFtZSI6ICJwaGFzZTIuc2lnbWFfSF9laWdlbl9w
bHVzMSBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiA0LAogICAiY2hhdCI6IDQsCiAgICJjaGVjayI6ICJDNCIsCiAgICJuYW1lIjogInBoYXNl
Mi5zaWdtYV9IX2VpZ2VuX21pbnVzMSB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgaW50IiwKICAg
InBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDQsCiAgICJjaGF0IjogNCwKICAgImNoZWNr
IjogIkM0IiwKICAgIm5hbWUiOiAicGhhc2UyLnNpZ21hX0hfZWlnZW5fbWludXMxIGVxdWFsIiwK
ICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJJTlRFUk5B
TC1IT0xPTk9NWS1HQVVHRSIsCiAgICJjaGF0IjogIklOVEVSTkFMLUhPTE9OT01ZLUdBVUdFIiwK
ICAgImNoZWNrIjogIkM0IiwKICAgIm5hbWUiOiAicGhhc2UyLmxhYmVsIHR5cGVkIiwKICAgIm5v
dGUiOiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIklOVEVS
TkFMLUhPTE9OT01ZLUdBVUdFIiwKICAgImNoYXQiOiAiSU5URVJOQUwtSE9MT05PTVktR0FVR0Ui
LAogICAiY2hlY2siOiAiQzQiLAogICAibmFtZSI6ICJwaGFzZTIubGFiZWwgZXF1YWwiLAogICAi
bm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMCwKICAgImNoYXQi
OiAwLAogICAiY2hlY2siOiAiQzQiLAogICAibmFtZSI6ICJwaGFzZTIucGkxX29yYml0IHR5cGVk
IiwKICAgIm5vdGUiOiAidHlwZSBpbnQiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogMCwKICAgImNoYXQiOiAwLAogICAiY2hlY2siOiAiQzQiLAogICAibmFtZSI6ICJwaGFzZTIu
cGkxX29yYml0IGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkM0IiwKICAgIm5h
bWUiOiAicGhhc2UyLmNoaXJhbF9wYWlyX2NoYXJhY3Rlcl9vcmRpbmFyeSB0eXBlZCIsCiAgICJu
b3RlIjogInR5cGUgYm9vbCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVl
LAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDNCIsCiAgICJuYW1lIjogInBoYXNlMi5j
aGlyYWxfcGFpcl9jaGFyYWN0ZXJfb3JkaW5hcnkgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIjJEIHdpdG5lc3M7IGNvbnRyYWN0aWJpbGl0
eSBvZiB0aGUgMnBpIGxvb3AgaW4gdGhlIG9yYml0IG9ubHkiLAogICAiY2hhdCI6ICIyRCB3aXRu
ZXNzOyBjb250cmFjdGliaWxpdHkgb2YgdGhlIDJwaSBsb29wIGluIHRoZSBvcmJpdCBvbmx5IiwK
ICAgImNoZWNrIjogIkM0IiwKICAgIm5hbWUiOiAicGhhc2UyLmRpbWVuc2lvbl9ub3RlIHR5cGVk
IiwKICAgIm5vdGUiOiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogIjJEIHdpdG5lc3M7IGNvbnRyYWN0aWJpbGl0eSBvZiB0aGUgMnBpIGxvb3AgaW4gdGhlIG9y
Yml0IG9ubHkiLAogICAiY2hhdCI6ICIyRCB3aXRuZXNzOyBjb250cmFjdGliaWxpdHkgb2YgdGhl
IDJwaSBsb29wIGluIHRoZSBvcmJpdCBvbmx5IiwKICAgImNoZWNrIjogIkM0IiwKICAgIm5hbWUi
OiAicGhhc2UyLmRpbWVuc2lvbl9ub3RlIGVxdWFsIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogMTIuNTY2MzcwNjE0MzU5
MTcyLAogICAiY2hlY2siOiAiQzQiLAogICAibmFtZSI6ICJwaGFzZTIuT19saW5lX2FicyAoY2hh
dCkgZ3QgMWUtMDYiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAg
ImNjIjogMTIuNTY2MzcwNjE0MzU5MTcyLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJD
NCIsCiAgICJuYW1lIjogInBoYXNlMi5PX2xpbmVfYWJzIChjYykgZ3QgMWUtMDYiLAogICAibm90
ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQi
OiAwLjAsCiAgICJjaGVjayI6ICJDNCIsCiAgICJuYW1lIjogInBoYXNlMi5PX25vbmxpbmVfYWJz
IChjaGF0KSBsZSAxZS0wOSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiAwLjAsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkM0IiwKICAgIm5h
bWUiOiAicGhhc2UyLk9fbm9ubGluZV9hYnMgKGNjKSBsZSAxZS0wOSIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6ICJJTlRF
Uk5BTC1IT0xPTk9NWS1HQVVHRSIsCiAgICJjaGVjayI6ICJDNCIsCiAgICJuYW1lIjogInBoYXNl
Mi5sYWJlbCAoY2hhdCkgaW4gZG9tYWluIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6ICJJTlRFUk5BTC1IT0xPTk9NWS1HQVVHRSIsCiAgICJjaGF0Ijog
bnVsbCwKICAgImNoZWNrIjogIkM0IiwKICAgIm5hbWUiOiAicGhhc2UyLmxhYmVsIChjYykgaW4g
ZG9tYWluIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
ICJBU1NJR05NRU5ULUktRk9SQ0VEIiwKICAgImNoYXQiOiAiQVNTSUdOTUVOVC1JLUZPUkNFRCIs
CiAgICJjaGVjayI6ICJDNSIsCiAgICJuYW1lIjogInBoYXNlMy52ZXJkaWN0IHR5cGVkIiwKICAg
Im5vdGUiOiAidHlwZSBzdHIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIkFT
U0lHTk1FTlQtSS1GT1JDRUQiLAogICAiY2hhdCI6ICJBU1NJR05NRU5ULUktRk9SQ0VEIiwKICAg
ImNoZWNrIjogIkM1IiwKICAgIm5hbWUiOiAicGhhc2UzLnZlcmRpY3QgZXF1YWwiLAogICAibm90
ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogWwogICAgIlQxIiwKICAg
ICJUMiIsCiAgICAiVDMiLAogICAgIlQ0IgogICBdLAogICAiY2hhdCI6IFsKICAgICJUMSIsCiAg
ICAiVDIiLAogICAgIlQzIiwKICAgICJUNCIKICAgXSwKICAgImNoZWNrIjogIkM1IiwKICAgIm5h
bWUiOiAicGhhc2UzLnRlc3RzX2hvbGRpbmcgdHlwZWQiLAogICAibm90ZSI6ICJ0eXBlIGxpc3Qi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogWwogICAgIlQxIiwKICAgICJUMiIs
CiAgICAiVDMiLAogICAgIlQ0IgogICBdLAogICAiY2hhdCI6IFsKICAgICJUMSIsCiAgICAiVDIi
LAogICAgIlQzIiwKICAgICJUNCIKICAgXSwKICAgImNoZWNrIjogIkM1IiwKICAgIm5hbWUiOiAi
cGhhc2UzLnRlc3RzX2hvbGRpbmcgZXF1YWwiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRy
dWUKICB9LAogIHsKICAgImNjIjogWwogICAgIkgyIiwKICAgICJIMyIKICAgXSwKICAgImNoYXQi
OiBbCiAgICAiSDIiLAogICAgIkgzIgogICBdLAogICAiY2hlY2siOiAiQzUiLAogICAibmFtZSI6
ICJwaGFzZTMuYWRtaXNzaWJsZV9IIHR5cGVkIiwKICAgIm5vdGUiOiAidHlwZSBsaXN0IiwKICAg
InBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IFsKICAgICJIMiIsCiAgICAiSDMiCiAgIF0s
CiAgICJjaGF0IjogWwogICAgIkgyIiwKICAgICJIMyIKICAgXSwKICAgImNoZWNrIjogIkM1IiwK
ICAgIm5hbWUiOiAicGhhc2UzLmFkbWlzc2libGVfSCBlcXVhbCIsCiAgICJub3RlIjogIiIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAg
ICJjaGVjayI6ICJDNSIsCiAgICJuYW1lIjogInBoYXNlMy5JNSB0eXBlZCIsCiAgICJub3RlIjog
InR5cGUgYm9vbCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAi
Y2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDNSIsCiAgICJuYW1lIjogInBoYXNlMy5JNSBlcXVh
bCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVl
LAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDNSIsCiAgICJuYW1lIjogInBoYXNlMy5j
b250cm9sc19hbGxfcGFzcyB0eXBlZCIsCiAgICJub3RlIjogInR5cGUgYm9vbCIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVj
ayI6ICJDNSIsCiAgICJuYW1lIjogInBoYXNlMy5jb250cm9sc19hbGxfcGFzcyBlcXVhbCIsCiAg
ICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAi
Y2hhdCI6ICJBU1NJR05NRU5ULUktRk9SQ0VEIiwKICAgImNoZWNrIjogIkM1IiwKICAgIm5hbWUi
OiAicGhhc2UzLnZlcmRpY3QgKGNoYXQpIGluIGRvbWFpbiIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiQVNTSUdOTUVOVC1JLUZPUkNFRCIsCiAgICJj
aGF0IjogbnVsbCwKICAgImNoZWNrIjogIkM1IiwKICAgIm5hbWUiOiAicGhhc2UzLnZlcmRpY3Qg
KGNjKSBpbiBkb21haW4iLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAiQVNTSUdOTUVOVC1JLUZPUkNFRCIsCiAgICJjaGVj
ayI6ICJDNSIsCiAgICJuYW1lIjogInZlcmRpY3QgcmVjb21wdXRlZCA9PSByZXBvcnRlZCAoY2hh
dCkiLAogICAibm90ZSI6ICJyZXBvcnRlZCBBU1NJR05NRU5ULUktRk9SQ0VEIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNr
IjogIkM1IiwKICAgIm5hbWUiOiAiY29udHJvbHNfYWxsX3Bhc3MgcmVjb21wdXRlZCA9PSByZXBv
cnRlZCAoY2hhdCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAg
ImNjIjogbnVsbCwKICAgImNoYXQiOiBbCiAgICAiVDEiLAogICAgIlQyIiwKICAgICJUMyIsCiAg
ICAiVDQiCiAgIF0sCiAgICJjaGVjayI6ICJDNSIsCiAgICJuYW1lIjogInRlc3RzX2hvbGRpbmcg
Y29uc2lzdGVudCB3aXRoIFQqLmhvbGRzIChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVj
ayI6ICJDNSIsCiAgICJuYW1lIjogImFkbWlzc2libGVfSCA9PSBwaGFzZTFiLmFkbWlzc2libGUg
KGNoYXQpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkM1IiwKICAgIm5hbWUiOiAiSTUg
PT0gcGhhc2UxYi5JNV9yZWdpc3RlcmVkIChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiQVNTSUdOTUVOVC1JLUZPUkNFRCIsCiAgICJjaGF0
IjogbnVsbCwKICAgImNoZWNrIjogIkM1IiwKICAgIm5hbWUiOiAidmVyZGljdCByZWNvbXB1dGVk
ID09IHJlcG9ydGVkIChjYykiLAogICAibm90ZSI6ICJyZXBvcnRlZCBBU1NJR05NRU5ULUktRk9S
Q0VEIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0Ijog
bnVsbCwKICAgImNoZWNrIjogIkM1IiwKICAgIm5hbWUiOiAiY29udHJvbHNfYWxsX3Bhc3MgcmVj
b21wdXRlZCA9PSByZXBvcnRlZCAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IFsKICAgICJUMSIsCiAgICAiVDIiLAogICAgIlQzIiwKICAgICJU
NCIKICAgXSwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzUiLAogICAibmFtZSI6ICJ0
ZXN0c19ob2xkaW5nIGNvbnNpc3RlbnQgd2l0aCBUKi5ob2xkcyAoY2MpIiwKICAgIm5vdGUiOiAi
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVs
bCwKICAgImNoZWNrIjogIkM1IiwKICAgIm5hbWUiOiAiYWRtaXNzaWJsZV9IID09IHBoYXNlMWIu
YWRtaXNzaWJsZSAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkM1IiwKICAgIm5h
bWUiOiAiSTUgPT0gcGhhc2UxYi5JNV9yZWdpc3RlcmVkIChjYykiLAogICAibm90ZSI6ICIiLAog
ICAicGFzcyI6IHRydWUKICB9CiBdLAogInNjaGVtYV9tZDUiOiAiNTMxMTFlMDM2MGRhYzEzOGIw
MmQ1OTE0ZWZlODVkNWMiLAogInN1bW1hcnkiOiB7CiAgImNoZWNrcyI6IDQzNiwKICAibWlzcyI6
IDQsCiAgInBhc3MiOiA0MzIKIH0KfQ==
=====END-EMBED name=g_2a_a1_chatleg_compare.json=====

=====BEGIN-EMBED name=run_chatleg.log md5=c38903300a0bbd8bbd964618e9774c7e bytes=782 encoding=base64 armor_bytes=1058 QUARANTINED=====
Z3VhcmQgbWQ1IE9LIHN0YWdpbmdfbWVtb19HXzJhX0ExX3YyLm1kIDYyNmFhODY4ODQ0MjIwZWI2
YzM4MDFlZjA3YTc3NzgzCmd1YXJkIG1kNSBPSyB0b29scy90MS9UMV9mb3JiaWRkZW5fR18yYV9B
MS50eHQgMjAyNmI3ODJkYjM5MDVkOWYyY2UzNTczMzgyMzYxOGMKZ3VhcmQgbWQ1IE9LIGlucHV0
cy9wYXBlcl9JSV8zXzRfNF9hbmRfM180XzdfZXh0cmFjdC5tZCA5NDBiMGJlZTRiMjExMmU5MTFh
ZTczOGMzZGIyYmMzZApUMSBpbnN0cnVtZW50OiBDTEVBTiAobnVtZXJpYyBjb2xsaXNpb25zIDAp
ClQxIG1lbW86IENMRUFOIChudW1lcmljIGNvbGxpc2lvbnMgMCkKVDEgZXh0cmFjdDogQ0xFQU4g
KG51bWVyaWMgY29sbGlzaW9ucyAwKQpnMiBidWlsdDogZGltIDE0ICBbMC44c10KUGhhc2UgMCBk
b25lICBbNi41c10gIHN5bV9pbnRfY29udGludW91cz1HMnhVMV9wc2kwIGRpbT0xNSAoaW1hZ2lu
YXJ5IHNlY3RvciAxNDsgcHNpMCBwaGFzZSBwcmVzZXJ2ZXMgTzogVHJ1ZSkgcGlubmVkPVRydWUK
UGhhc2UgMSBkb25lICBbMTEuNnNdICBob2xkcz17J1QxJzogVHJ1ZSwgJ1QyJzogVHJ1ZSwgJ1Qz
JzogVHJ1ZSwgJ1Q0JzogVHJ1ZX0gIGdyb3VwMTM0ND0xMzQ0IHNwbGl0PUZhbHNlClBoYXNlIDFi
IGRvbmUgWzExLjZzXSAgYWRtaXNzaWJsZT1bJ0gyJywgJ0gzJ10KUGhhc2UgMiBkb25lICBbMTIu
MnNdICBwaTFfb3JiaXQ9MCBsb29wX2ltYWdlcz1bJ0lkJywgJ3NpZ21hX0gnXQpQaGFzZSAzIGRv
bmUgIFsxMi4yc10gIHZlcmRpY3Q9QVNTSUdOTUVOVC1JLUZPUkNFRAo=
=====END-EMBED name=run_chatleg.log=====

=====BEGIN-EMBED name=G_2a_A1_CHATLEG_EXECUTION_REPORT.md md5=3c82ded06a150343f01c0d92947c37b7 bytes=16601 encoding=base64 armor_bytes=22428 QUARANTINED=====
IyBHLTJhLUExIOKAlCBDSEFULUxFRyBFWEVDVVRJT04gUkVQT1JUIChQaGFzZXMgMCwgMSwgMWIs
IDIsIDMpCgoqKkdhdGU6KiogRy0yYS1BMSAoR2F0ZSAyYTogQmFyeW9uIFNwaW4gR2VvbWV0cnkg
JiBGYWN0b3IgQXNzaWdubWVudCkuICoqRXhlY3V0ZWQ6KiogU2VwdGVtYmVyIDIwLCAyMDI2LCBj
aGF0IHNpZGUsIHNpbmdsZSBydW4sIG9uIHRoZSBhdXRob3IncyBkaXJlY3RpdmUgIkV4ZWN1dGUg
Q2hhdCBMZWcgZm9yIEctMmEtQTEiLiAqKkJhc2U6KiogVjQuODMgYDQwMDA5ZWMwMTk3ODc2YjEz
MDc2NmYxYWU3NDk0MzYwYC4KCioqTG9jayBjaGFpbiAoYWxsIGFzc2VydGVkIGF0IHJ1biB0aW1l
KToqKiBtZW1vIHYyIGA2MjZhYTg2ODg0NDIyMGViNmMzODAxZWYwN2E3Nzc4M2AgKDYxLDU2MiBC
KSDCtyBnYXRlIFQxIGxpc3QgYDIwMjZiNzgyZGIzOTA1ZDlmMmNlMzU3MzM4MjM2MThjYCAoMjQg
cGF0dGVybnMpIMK3IGFjdGlvbi1vZi1yZWNvcmQgZXh0cmFjdCBgOTQwYjBiZWU0YjIxMTJlOTEx
YWU3MzhjM2RiMmJjM2RgICgxMiw5MTIgQikgwrcgc2NoZW1hIHYxLjAgYDUzMTExZTAzNjBkYWMx
MzhiMDJkNTkxNGVmZTg1ZDVjYCDCtyBjb21wYXJhdG9yIHYxLjAgYDVhZmNkNTg5MGE5MjQ4ZjAx
YTNkOGEyMDNlMzQ5MDM5YCDCtyBsb2NrIHJlY29yZCBgODczMmMzOTBiZTFmNDQyZmFhNTg5YmYw
NGY3ZmZlOWZgLgoKKipDaGF0LWxlZyBhcnRpZmFjdHMgKG1kNSAvIGJ5dGVzKToqKiBpbnN0cnVt
ZW50IGBnXzJhX2ExX2NoYXRsZWcucHlgICoqYDYzNjA3MDlkNmE3ZWI1ZmMzZGY3ZmM4ZmQyNmRj
MzZhYCoqIC8gNTMsNzA2IMK3IGNoZWNrcG9pbnQgYGdfMmFfYTFfY2hhdGxlZ19jaGVja3BvaW50
Lmpzb25gICoqYDhmNjU3YTIzYTY4ZWYwODJmOTlhNzU3OWFmNzgzNDhjYCoqIC8gOCwyNDcgwrcg
Y2hhdC12cy1jaGF0IGNvbXBhcmF0b3Igc2FuaXR5IHJ1biBgZ18yYV9hMV9jaGF0bGVnX2NvbXBh
cmUuanNvbmAgKipgYmEwODc2MDc0Mzk2ZTY5NzYxNGE0ZGFhNzhkYTc2ODJgKiogwrcgcnVuIGxv
ZyBgcnVuX2NoYXRsZWcubG9nYCBgYzM4OTAzMzAwYTBiYmQ4YmJkOTY0NjE4ZTk3NzRjN2VgLiBS
dW4gdGltZSAqKjEyLjIgcyoqIHNpbmdsZSBjb3JlLiBUMTogaW5zdHJ1bWVudCwgbWVtbywgZXh0
cmFjdCwgY2hlY2twb2ludCwgY29tcGFyZSBhbmQgbG9nIGFsbCAqKkNMRUFOKiogKDAgaGl0cywg
MCBudW1lcmljIGNvbGxpc2lvbnMpOyB0aGUgaW5zdHJ1bWVudCBoYWx0cyBvbiBhbnkgZ3VhcmQg
b3Igc2NhbiBmYWlsdXJlIOKAlCBubyBvdmVycmlkZSBmbGFnIGV4aXN0cyAoRC1UMSByZXRpcmVk
KS4KCiMjIDEuIFZlcmRpY3QgKGFzc2VtYmxlZCBsYXN0LCBieSB0aGUgc2NoZW1hIHJ1bGUsIGZy
b20gdGhlIGVuY29kZWQgYm9vbGVhbnMpCgoqKkFTU0lHTk1FTlQtSS1GT1JDRUQuKiogQWxsIGZv
dXIgZm9yY2luZyB0ZXN0cyBob2xkIG9uIHRoZSBhY3Rpb24gb2YgcmVjb3JkOyBhbGwgUGhhc2Ut
MC8xLzIgY29udHJvbHMgcGFzczsgYHNwYXRpYWxfaW50ZXJuYWxfZGlyZWN0X3Byb2R1Y3RgIHRy
dWU7IGBzeW1faW50X3Bpbm5lZGAgdHJ1ZS4gRGVsaXZlcmFibGVzOiB0aGUg4oSNIHNjcmVlbiBh
ZG1pdHMgZXhhY3RseSAqKkgyIGFuZCBIMywgYm90aCBpbXBvcnRzKiog4oaSICoqSTUgcmVnaXN0
ZXJlZCoqOyBQLeKEgiAqKkNMT1NFRC1CWS1JTlNUQU5USUFUSU9OKio7IHRoZSAxMzQ0IGdyb3Vw
ICoqbm9uLXNwbGl0Kio7IHRoZSBQaGFzZS0yIHdpdG5lc3MgcmV0dXJucyAqKs+A4oKBKE9yYml0
KSA9IDAqKiB3aXRoIHRoZSBsb2NrZWQtbGlmdCBpbWFnZXMge0lkLCDPg1/ihI19LgoKUjIsIGNv
bmRpdGlvbmFsIG9uIHRoZSBhY3Rpb24gb2YgcmVjb3JkICh0aGUgcGlubmVkIGV4dHJhY3QgKyB0
aGUgYXV0aG9yJ3MgYW5zd2VycyBRLUExLTEvUS1BMS0zKSBhbmQgdGhlIGFkb3B0ZWQgaG9tb3Rv
cHkgaW5wdXRzOyBldmVyeSBjb21wdXRlZCBpdGVtIFIxLW1hY2hpbmUgKGV4YWN0IGFyaXRobWV0
aWMgZXhjZXB0IHRoZSBzcGlub3JpYWwtMk8gYmxvY2ssIGZsb2F0cyB0aHJlc2hvbGRlZCkuCgoj
IyAyLiBQaGFzZSAwIOKAlCB0aGUgYWN0aW9uIG9mIHJlY29yZCBpbnZlbnRvcmllZAoKLSAoMGEp
IDE2IHJlYWwgY29tcG9uZW50cywgOCBjb21wbGV4IGFtcGxpdHVkZXMsIG5vIHNwaW5vciBpbmRl
eCAoYXNzZXJ0ZWQgZnJvbSB0aGUgZXh0cmFjdCBhbmQgaXRzIGhlYWRlcikuCi0gKDBiKSAqKlN5
bV9pbnQuKiogVGhlIGZ1bGwgY29udGludW91cyBzdGFiaWxpemVyIG9mIHRoZSBvcmllbnRlZCBk
ZW5zaXR5IGluIHNvKDE2KSwgY29tcHV0ZWQgZXhhY3RseSBhcyB0aGUga2VybmVsIG9mIHRoZSA4
MTkyIMOXIDEyMCBpbnRlZ2VyIG1hcCBYIOKGpiBbVChYdSx2LHcpK1QodSxYdix3KStUKHUsdixY
dyldIChHcmFtLW1hdHJpeCBudWxsc3BhY2Ugb3ZlciDihJopOiAqKmRpbWVuc2lvbiAxNSA9IGfi
goIgKDE0KSDiipUgdSgxKV97z4jigoB9ICgxKSoqIOKAlCByZWNvcmRlZCBhcyBgc3ltX2ludF9j
b250aW51b3VzID0gIkcyeFUxX3BzaTAiYC4gQWxsIDE0IGRlcml2YXRpb25zIHByZXNlcnZlIE8g
KGBnMl9wcmVzZXJ2ZXNfT2AgdHJ1ZSk7IGEgZ2VuZXJpYyBzbygxNikgcm90YXRpb24gbWl4aW5n
IFJlIM+I4oKBIHdpdGggSW0gz4jigoIgYnJlYWtzIGl0IHdpdGggaW50ZWdlciBtYXJnaW4gMSAo
YGdlbmVyaWNfc28xNl9icmVha3NfT2AgdHJ1ZSk7IHRoZSBzdGFiaWxpemVyIHJlc3RyaWN0ZWQg
dG8gdGhlIGltYWdpbmFyeSBzZWN0b3Igc28oMTQpIGhhcyBkaW1lbnNpb24gKipleGFjdGx5IDE0
KiogKGV4dHJhczogYHBoYXNlMF9pbWFnX3NlY3Rvcl9jb250aW51b3VzX2RpbWApLiBUaGUgZXh0
cmEgZ2VuZXJhdG9yIGlzIHRoZSBwaGFzZSByb3RhdGlvbiBvZiB0aGUgKipyZWFsLXVuaXQgY29t
cG9uZW50IM+I4oKAIGFsb25lKio6IHRoZSBvcmllbnRlZCB0ZXJtIGNhcnJpZXMgb25seSBpbWFn
aW5hcnkgaW5kaWNlcyBhbmQgdGhlIHR3by1ib2R5IHRlcm0gZGVwZW5kcyBvbmx5IG9uIHzPiHzC
siwgc28gz4jigoAgZGVjb3VwbGVzIGFuZCBjYXJyaWVzIGl0cyBvd24gVSgxKS4gVGhlIGRpYWdv
bmFsIGNvbmRlbnNhdGUgcGhhc2UgaXMgYnJva2VuIGJ5IE8gdG8gKirihKTigoMqKiAoYHBoYXNl
X3N1Ymdyb3VwX29yZGVyYCAzOiBUKM+JdSzPiXYsz4l3KSA9IFQgZm9yIM+JwrMgPSAxLCBleGFj
dDsgVChpdSxpdixpdykgPSDiiJJpVCwgc28gYE9fcGhhc2VfaW52YXJpYW50YCBmYWxzZSk7IGNv
bmp1Z2F0aW9uIG1hcHMgTyDihqYgxYwgKGBjb25qdWdhdGlvbl9tYXBzX09fdG9fY29uanVnYXRl
YCB0cnVlKS4gKirihpIgSC1BMS0xICjCpzcpLioqIGBzeW1faW50X3Bpbm5lZGAgPSB0cnVlOiB0
aGUgY29udGludW91cyBwYXJ0IGlzIGZ1bGx5IGlkZW50aWZpZWQgKGfigoIgb24gdGhlIDctc2Vj
dG9yLCB1KDEpIG9uIHRoZSByZWFsIHVuaXQsIG5vdGhpbmcgZWxzZSkuCi0gKDBjKSBEaXJlY3Qg
cHJvZHVjdDogdGhlIHRlcm0gbGlzdCBvZiByZWNvcmQgKHR3by1ib2R5IGNvbnRhY3Qg4oCUIM60
X2FiLCBubyBzcGF0aWFsIGluZGV4OyBHUCBraW5ldGljIOKAlCDOtF9hYiwg4oiCX2nCt+KIgl9p
OyBvcmllbnRlZCBPIOKAlCDPhl9hYmMsIM61X3h5IOKIgl94IOKIgl95KSBoYXMgbm8gbWl4ZWQg
c3BhdGlhbOKAk2ludGVybmFsIHRlbnNvciDihpIgYHNwYXRpYWxfaW50ZXJuYWxfZGlyZWN0X3By
b2R1Y3RgIHRydWUuICoqRi1BMS0xIGRvZXMgbm90IGZpcmUuKioKLSAoMGQpIFZhY3V1bSBtYW5p
Zm9sZCBvZiByZWNvcmQgKipWID0gU8K54oG1KiogKHRoZSBPIGRlbnNpdHkgdmFuaXNoZXMgb24g
dW5pZm9ybSBzdGF0ZXMsIGFzc2VydGVkOyBubyByZWFsLXVuaXQtc3BsaXR0aW5nIHRlcm0sIFEt
QTEtMyk6IM+A4oKBKFYpID0gz4DigoQoVikgPSAwLiBMb2NraW5nIGludmVudG9yeSAoc3RhYmls
aXplcnMgaW4gZ+KCgiBvZiByZXByZXNlbnRhdGl2ZSDPiOKCgCBieSB0aGUgcmFuayBvZiBpdHMg
aW1hZ2luYXJ5IHNwYW4sIGV4YWN0IG51bGxzcGFjZXMpOiByYW5rIDAg4oaSIEfigoIgKGRpbSAx
NCk7IHJhbmsgMSAoz4jigoAgPSBl4oKHKSDihpIgU1UoMykgKGRpbSA4KTsgcmFuayAyICjPiOKC
gCA9IGXigoEgKyBpIGXigoIpIOKGkiB0aGUgMy1kaW0gYWxnZWJyYSBmaXhpbmcgZeKCgSwgZeKC
giBhbmQgaGVuY2UgZeKChCA9IGXigoFl4oKCIOKAlCB0aGUgbG9uZy1yb290IFNVKDIpIChwb2lu
dHdpc2Ugc3RhYmlsaXplciBvZiDin6gxLGXigoEsZeKCgixl4oKE4p+pKSwgSm9yZGFuIHR5cGUg
WzIsMiwxLDEsMV0gKFBoYXNlIDEpOyBnZW5lcmljIM+A4oKAID0gMTsgz4DigoMtaW5qZWN0aXZl
OyDPgOKChChH4oKCL0jigoApID0gMCBmb3IgYWxsIHRocmVlLgotICgwZSkgQ29udHJvbHM6IExf
4oqlz4jigoAgPSAwICjOvCA9IFXPgeKCgCkg4pyTOyBG4oKC4oKBICh4IOKGpiBheCArIGIsIGEg
4oiIIHsxLDIsNH0pIGFsbCB1bnNpZ25lZCBhdXRvbW9ycGhpc21zLCBwZXJtdXRhdGlvbiBjaGFy
YWN0ZXIgbm9ybSAzIHdpdGggdHJpdmlhbCBtdWx0aXBsaWNpdHkgMSDihpIgMSDiipUgMyDiipUg
M8yEIOKckzsgZ2VuZXJpYy1zbygxNikgbWFyZ2luIHBvc2l0aXZlIOKcky4KCiMjIDMuIFBoYXNl
IDEg4oCUIHRoZSBmb3VyIGZvcmNpbmcgdGVzdHMKCioqVDEg4oCUIGhvbGRzLioqIDJPICg0OCB1
bml0IHF1YXRlcm5pb25zLCBleGFjdCBpbiDihJoo4oiaMikpOiDin6jPh197My8yfSwgz4dfezMv
Mn3in6kgPSAxLCDPhygxKSA9IDQsIM+HKOKIkjEpID0g4oiSNCwgKipGcm9iZW5pdXPigJNTY2h1
ciBpbmRpY2F0b3Ig4oiSMSoqLiBUaGUgNyBpcyBkZWZpbmVkIG92ZXIg4oSaIChgc2V2ZW5fcmVh
bGApLiBFdmVuLW11bHRpcGxpY2l0eSBib3VuZCDijIo3LzTijIsgPSAxIOKGkiBwYXJpdHkgZm9y
Y2VzICoqMCoqLiBCcmFuY2hpbmdzIG9mIHRoZSA3IGJ5IHRoZSBjb21wYWN0IENhc2ltaXIgKGV4
YWN0LCBLaWxsaW5nLW5vcm1hbGl6ZWQpIG9yIHRoZSBwcmluY2lwYWwgd2VpZ2h0czogbG9uZy1y
b290ICoqWzIsMiwxLDEsMV0qKiwgc2hvcnQtcm9vdCAqKlszLDIsMl0qKiAodGhlIGlkZWFsIG9m
IHNvKDQpID0gU3RhYl97R+KCgn0o4oSNX0wpIGNvbXBsZW1lbnRhcnkgdG8gdGhlIGxvbmctcm9v
dCBpZGVhbCksIHN1KDMpLXNs4oKCICoqWzMsMywxXSoqICh0aGUgc28oMykgb2YgdGhlIEogPSBM
4oKHIGJhc2lzIChl4oKBLGXigoMpLChl4oKCLGXigoYpLChl4oKELGXigoUpLCB2ZXJpZmllZCBp
bnNpZGUgU3RhYl97Z+KCgn0oZeKChykpLCBwcmluY2lwYWwgKipbN10qKiAodGhlIEfigoIgcm9v
dCBzeXN0ZW0gY29tcHV0ZWQgZnJvbSB0aGUgc3UoMykgQ2FydGFuIGjigoEgPSByb3QoMSwzKSDi
iJIgcm90KDIsNiksIGjigoIgPSByb3QoMiw2KSDiiJIgcm90KDQsNSk6IDEyIHJvb3RzLCBhIHBv
c2l0aXZlIHN5c3RlbSwgdHdvIHNpbXBsZSByb290czsgaF9wcmluYyA9IDLPgV7iiKggd2l0aCDi
n6jOsV9pLCBo4p+pID0gMjsgd2VpZ2h0cyBvbiB0aGUgNyA9IHviiJI2LOKIkjQs4oiSMiwwLDIs
NCw2fSkuIE5vIDQgYW55d2hlcmUuIENvbnRyb2wgQy1BMS0xOiAo4oSCwrIpXuKKlzMgdW5kZXIg
dGhlIGRpYWdvbmFsIHN1KDIpIGhhcyB0aGUgcXVhcnRldCB3aXRoIG11bHRpcGxpY2l0eSAqKjEq
KiDinJMuCgoqKlQyIOKAlCBob2xkcy4qKiBkaW0gRGVyKPCdlYYpID0gMTQ7IEPihJMoMCw3KSBy
ZWxhdGlvbnMgb2YgdGhlIHNldmVuIEwtbWFwcyBvbiDihJ3igbg7IGRpbSBzcGFuKExfYUxfYiwg
YTxi4omkNykgPSAyMSwgKGE8YuKJpDYpID0gMTU7IGfigoIg4oqCIHNwaW4oNylfTDsgKipkaW0o
Z+KCgiDiiKkgc3UoNClfTCkgPSA4LioqIChiKSBUaGUgc3Bpbm9yaWFsIDJPOiBzdSg0KV9MIGNv
bnZlcnRlZCB0byBjb21wbGV4IDTDlzQgb24gKOKEneKBuCwgSiA9IEzigocpIChKLWJhc2lzIHcg
PSAoZeKCgCxl4oKBLGXigoIsZeKChCksIEp3ID0gKGXigocsZeKCgyxl4oKGLGXigoUpKSBpcyB0
cmFjZWxlc3MgYW50aWhlcm1pdGlhbiBvZiBkaW1lbnNpb24gMTU7IHRoZSBzcGluLTMvMiBnZW5l
cmF0b3JzIOKIkmlTX2sgbGllIGluIGl0cyBzcGFuIChleGFjdCByYW5rIHRlc3QpOyB0aGUgNDgg
Z3JvdXAgZWxlbWVudHMgRChxKSA9IGV4cCgyzrggbsK3WCk6ICoqemVyby1kZWZlY3QgY291bnQg
MSAodGhlIGlkZW50aXR5IG9ubHkpKiosIG1pbmltdW0gYXV0b21vcnBoaXNtIGRlZmVjdCBvdmVy
IDJPIOKIliB7wrExfSA9ICoqMC43MDcxKiogKGZsb2F0IHJ1bGUgPiAxMOKBu+KBtiDinJMpOyB0
aGUgMk8tY2hhcmFjdGVyIG9mIOKEguKKl/CdlYYgdW5kZXIgdGhpcyBhY3Rpb24gY29udGFpbnMg
dGhlIHF1YXJ0ZXQgd2l0aCBtdWx0aXBsaWNpdHkgKioyKiogKD0gNCDiipUgNMyEOyBjb250cm9s
IEMtQTEtMiDinJMpLiAoYykgU0woMiw3KTogMzM2IGVsZW1lbnRzLCAqKmV4YWN0bHkgMioqIHNv
bHV0aW9ucyBvZiBnwrIgPSAxOyB0aGUgNiAoRmFubyBwZXJtdXRhdGlvbiByZXAg4oiSIDEpIGFu
ZCB0aGUgU3RlaW5iZXJnIDcgKFDCuSjwnZS94oKHKSBwZXJtdXRhdGlvbiByZXAg4oiSIDEpIGhh
dmUgaW5kaWNhdG9yICsxIGJ5IG1hY2hpbmU7IG9yZGluYXJ5IHN1bSAxICsgNiArIDcgKyA4ID0g
KioyMioqICjOvSgzKSA9IM69KDPMhCkgPSAwLCDOvSg4KSA9ICsxIGFkb3B0ZWQpOyB0aGUgRGlv
cGhhbnRpbmUgc29sdmUgMs694oKEICsgM8694oKGICsgMs694oKIID0g4oiSNSBoYXMgc29sdXRp
b25zICjOveKChCzOveKChizOveKCiCkg4oiIIHso4oiSMSziiJIxLDApLCAoMCziiJIxLOKIkjEp
fSDihpIgKipudTRfYWxsb3dlZCA9IFviiJIxLCAwXSoqIOKAlCBubyByZWFsLXR5cGUgZ2VudWlu
ZSA0IOKGkiBTTCgyLDcpIOKKhCBPKDcpIOKKhyBH4oKCLiBJbnZvbHV0aW9uIGxlbW1hIHdpdG5l
c3Nlczogz4Nf4oSNIChmaXgg4p+oMSxl4oKBLGXigoIsZeKChOKfqSwgbmVnYXRlIHRoZSBjb21w
bGVtZW50KSBpcyBhbiBhdXRvbW9ycGhpc20gd2l0aCB0cmFjZSAqKuKIkjEqKjsgbmVnYXRpbmcg
YSBzaW5nbGUgdW5pdCBpcyBub3QgYW4gYXV0b21vcnBoaXNtLiBUaGUgcmVhbGl6ZWQgc2lnbmVk
IEZhbm8gZ3JvdXA6IGNsb3N1cmUgb2YgdGhlIHNpZ25lZCBhdXRvbW9ycGhpc20gbGlmdHMgb2Yg
KDMgNSkoNiA3KSwgYSA3LWN5Y2xlIGFuZCBhIDMtY3ljbGUg4oaSICoqb3JkZXIgMTM0NCoqLCBl
dmVyeSBlbGVtZW50IGFuIGF1dG9tb3JwaGlzbSAoZmFzdCBzaWduZWQgdGVzdCwgY3Jvc3MtY2hl
Y2tlZCBhZ2FpbnN0IHRoZSBtYXRyaXggdGVzdCBvbiBhIHNhbXBsZSk7IGl0cyBzaWduIGtlcm5l
bCBoYXMgb3JkZXIgOC4KCioqVDMg4oCUIGhvbGRzLioqIEZyb20gU1UoMykg4oaSIEfigoIg4oaS
IFPigbYgd2l0aCB0aGUgYWRvcHRlZCB0ZXh0Ym9vayBpbnB1dHM6IM+A4oKBKEfigoIpID0gMCwg
z4DigoMoR+KCgikgPSDihKQsIM+A4oKEKEfigoIpID0gMC4gViA9IFPCueKBtTogz4DigoEgPSDP
gOKChCA9IDAuIE5vIGludGVybmFsIGRvdWJsZSBjb3ZlciAoz4DigoEoR+KCgikgPSAwOyB0aGUg
ZGlhZ29uYWwgcGhhc2UgZ3JvdXAg4oSk4oKDKS4gRW52ZWxvcGUtaW4t8J2VhiBraWxsOiDPgOKC
gihT4oG2KSA9IDAg4oaSIHRoZSBTwrIg4oaqIFPigbYgaW5jbHVzaW9uIGlzIG51bGwtaG9tb3Rv
cGljIOKGkiB0aGUgaW5kdWNlZCDPgOKChCBtYXAgaXMgemVyby4gTG9ja2luZy1pbnZlbnRvcnkg
cXVvdGllbnRzOiDPgOKChChH4oKCL0jigoApID0gMCBmb3IgR+KCgiwgU1UoMyksIFNVKDIpX2xv
bmcgKM+A4oKDLWluamVjdGl2ZSBieSBpbmRleCAxKS4gQ29udHJvbHM6IM+A4oKEKFPCsikgPSDi
hKTigoIgKGZyb20gVSgxKSDihpIgU1UoMikg4oaSIFPCsiksIM+A4oKEKFPCsykgPSDihKTigoIs
IHzPgOKCgShTTygzKS9UKXwgPSAyNCDinJMuCgoqKlQ0IOKAlCBob2xkcy4qKiBUaGUgdGhyZWUg
bm9uLXRyaXZpYWwgcG9pbnR3aXNlLWxpbmUtc3RhYmlsaXplciBjb2xsaW5lYXRpb25zIG9mIHsx
LDIsNH0gaGF2ZSAqKjI0Kiogc2lnbmVkIGF1dG9tb3JwaGlzbSBsaWZ0czogKioxMiBvZiBvcmRl
ciAyLCBhbGwgd2l0aCB0cmFjZSDiiJIxKio7IDEyIG9mIG9yZGVyIDQgd2l0aCB0cmFjZXMge+KI
kjEsIDN9LiBQZXJtdXRhdGlvbiBjaGFyYWN0ZXIgMywgz4figoYoMkEpID0gMiDihpIgd3Jvbmct
bW9kdWxlIGdhcCAqKjQqKi4gQ29udHJvbHM6IEbigoLigoEgdW5zaWduZWQg4oaSIDEg4oqVIDMg
4oqVIDPMhCDinJM7IHRoZSDOveKCgiBtdWx0aXBsaWVyIGlzIGFuIHVuc2lnbmVkIGF1dG9tb3Jw
aGlzbSDinJMuIEV4dHJhIHdpdG5lc3M6IGV4YWN0bHkgKioyMSBvZiB0aGUgMTY4KiogY29sbGlu
ZWF0aW9ucyBsaWZ0IGFzIHVuc2lnbmVkIGF1dG9tb3JwaGlzbXMgKMKnMi43OSBjb25maXJtZWQp
LgoKKipUaGUgMTM0NCBncm91cCAoRS1BMS02KGEpKToqKiBwcmVzZW50YXRpb24g4p+oYSxiIHwg
YcKyLCBiwrMsIChhYinigbcsIFthLGJd4oG04p+pIHdpdGggYSA9ICgzIDUpKDYgNykgYW5kIGEg
bWFjaGluZS1mb3VuZCBvcmRlci0zIGNvbGxpbmVhdGlvbiBiIHNhdGlzZnlpbmcgdGhlIHJlbGF0
aW9uczsgOCDDlyA4ID0gKio2NCBsaWZ0IHBhaXJzIHRlc3RlZCwgMCBnZW5lcmF0ZSBhIHN1Ymdy
b3VwIG9mIG9yZGVyIDE2OCDigJQgZXZlcnkgcGFpciBnZW5lcmF0ZXMgdGhlIGZ1bGwgZ3JvdXAg
b2Ygb3JkZXIgMTM0NCDihpIgTk9OLVNQTElUKiogKGJhbmtlZCBSMSBzdHJ1Y3R1cmFsOyBjb3Jy
b2JvcmF0ZWQgaW4gcHJpbnQsIG1lbW8gwqcxMiBMLUExLTMpLgoKIyMgNC4gUGhhc2UgMWIg4oCU
IHRoZSDihI0gc2NyZWVuIGFuZCBQLeKEggoKLSAqKlAt4oSCOioqIHRoZSBjb21wbGV4IHVuaXQg
b2Yg4oSC4oqX8J2VhiBjb21tdXRlcyB3aXRoIGV2ZXJ5IExfYSAoZXhhY3QsIG9uIOKEncK54oG2
KSDihpIgY2VudHJhbDsgaW4gdGhlIHNlZGVuaW9ucyB0aGUgZG91YmxpbmcgdW5pdCBl4oKIIGFu
dGljb21tdXRlcyB3aXRoIGV2ZXJ5IGltYWdpbmFyeSB1bml0IG9mIPCdlYYgKGV4YWN0IENheWxl
eeKAk0RpY2tzb24pIOKGkiBub3QgY2VudHJhbCDihpIgKipDTE9TRUQtQlktSU5TVEFOVElBVElP
TioqLgotICoqSCBzY3JlZW4gKGNyaXRlcmlhIOKGkiBjb2RlIGJ5IHRoZSBydWxlIG9mIMKnNyBI
LUExLTIpOioqIEgxIChjb250cm9sKTogaSBmYWlsLCBpaSBwYXNzLCBpaWkgZmFpbCAodGhlIGtp
bGwpLCBpdiBuL2Eg4oaSIEVYQ0xVREVEKGksaWlpKS4gKipIMioqICh0aGUgZGVjbGFyZWQgZW52
ZWxvcGUsIFEtQTEtMik6IHBhc3MvcGFzcy9wYXNzL2R5bmFtaWNhbCDihpIgKipBRE1JU1NJQkxF
LUlNUE9SVCoqLiAqKkgzKiogKHNwYXRpYWwtc3Bpbm9yIGluZGV4KTogcGFzcy9wYXNzL2NvbmRp
dGlvbmFsL2tpbmVtYXRpYyDihpIgKipBRE1JU1NJQkxFLUlNUE9SVCoqLiBINCAoRmFuby1saW5l
IOKEjV9MIOKKgiDwnZWGKTogaSBmYWlsLCBpaSBwYXNzIChpdHMgU1UoMikgbW9kdWxlIG9uIOKE
jV9MXuKKpSBpcyB0aGUgMiDiipUgMiBvZiB0aGUgbG9uZy1yb290IGJyYW5jaGluZykg4oaSIEVY
Q0xVREVEKGkpLiBINSAoc2VkZW5pb24gZG91YmxpbmcpOiBpIGZhaWwgKGXigoggYW50aWNvbW11
dGVzIOKAlCBub3QgdGVuc29yLWNvbW11dGluZyksIGlpIGZhaWwgKDItZGltIGRvdWJsaW5nKSDi
hpIgRVhDTFVERUQoaSxpaSkuICoqQWRtaXNzaWJsZSA9IHtIMiwgSDN9LCBib3RoIG91dHNpZGUg
dGhlIGZpZWxkIGNvbnRlbnQgb2YgcmVjb3JkIOKGkiBJNSByZWdpc3RlcmVkLioqCgojIyA1LiBQ
aGFzZSAyIOKAlCB0aGUgaW5zdGFudGlhdGVkLWNvcmUgd2l0bmVzcyAoRS1BMS0yKGEpOyAyLUQ7
IHplcm8gdmVyZGljdCB3ZWlnaHQpCgpPYmplY3Q6IHRoZSBkZWdyZWUtMSB0ZXh0dXJlIM+IID0g
4oiaz4HigoDCtyhzaW4gZiBjb3Mgz4YgZeKCgSArIHNpbiBmIHNpbiDPhiBl4oKCICsgY29zIGYg
ZeKChCksIGYgPSDPgC8oMStywrIpIChgbG9ja3JlYy1BLTIuNmApOyBjb250cm9sOiB0aGUgc2Ft
ZSB0ZXh0dXJlIGluIChl4oKBLGXigoIsZeKCgykuIChhKSBPID0gz4ZfYWJjIMOXIOKIqyBuwrco
4oiCX3ggbiDDlyDiiIJfeSBuKSBkwrJ4IHdpdGggdGhlIGludGVncmFsIGV4YWN0bHkgMs+AW+KI
kmNvcyBmXeKCgF7iiJ4gPSDiiJI0z4AgKG51bWVyaWMgY3Jvc3MtY2hlY2sgdG8gMTDigbvigbkp
OiAqKnxPX2xpbmV8ID0gNM+AID0gMTIuNTY24oCmOyBPX25vbmxpbmUgPSAwIGV4YWN0bHkqKiAo
z4bigoHigoLigoMgPSAwKS4gKGIpIFRoZSBzdGFiaWxpemVyIGZhbWlseSBNKHAsIHEpIOKAlCBo
IOKGpiBxIGggccyEIG9uIOKEjV9MID0g4p+oMSxl4oKBLGXigoIsZeKChOKfqSwgayBl4oKDIOKG
piAocCBrIHHMhCkgZeKCgyBvbiDihI1fTF7iiqUg4oCUIHZlcmlmaWVkIGFzIG9jdG9uaW9uIGF1
dG9tb3JwaGlzbXMgZXhhY3RseSBhdCByYXRpb25hbCBjaXJjbGUgcG9pbnRzIHEgPSBjICsgcyBl
4oKEICh0ID0gMS8zLCAyLzUpIGZvciBwIOKIiCB7MSwg4oiSMSwgcSwgYSBnZW5lcmljIHJhdGlv
bmFsIHVuaXR9ICg4LzgpLCBhbmQgdmVyaWZpZWQgdG8gcm90YXRlIHRoZSB0ZXh0dXJlJ3MgSW0g
4oSNX0wgYnkgdGhlIGFuZ2xlIHdpdGggY29zIM6xID0gY8KyIOKIkiBzwrIsIHNpbiDOsSA9IDJj
czsgdGhlIGtlcm5lbCBNKHAsIDEpIGZpeGVzIOKEjV9MIHBvaW50d2lzZSAodGhlIGxvbmctcm9v
dCBTVSgyKSkuIEludGVybmFsIGltYWdlIFNPKDQpID0gU3RhYl97R+KCgn0o4oSNX0wpLCBzdWJk
aXJlY3QsIM+A4oKAKFN0YWIpID0gMS4gKGMpIEF0IM6xID0gMs+AIChxID0g4oiSMSk6ICoqTSgx
LCDiiJIxKSA9IM+DX+KEjSoqIChlaWdlbnZhbHVlcyArMSDDlzQgb24g4oSNX0wsIOKIkjEgw5c0
IG9uIOKEjV9MXuKKpSkgYW5kICoqTSjiiJIxLCDiiJIxKSA9IElkKiog4oCUIHRoZSB0d28gbGlm
dHMsIGV4YWN0IOKGkiBgbG9vcF9pbWFnZXMgPSBbSWQsIHNpZ21hX0hdYCwgbGFiZWwgKipJTlRF
Uk5BTC1IT0xPTk9NWS1HQVVHRSoqICh0aGUgbG9ja2VkLWxpZnQgdHJhcCwgYXMgcHJlLWRlY2xh
cmVkKS4gKGQpICoqz4DigoEoT3JiaXQpID0gMCoqICh0aGUgZGlhZ29uYWwgbG9vcCBjbG9zZXMg
YXQgKOKIkjEs4oiSMSkgfiBJZCBhbmQgd2luZHMgb25jZSBpbiDPgOKCgShTTygyKSkgPSDihKQ7
IM+A4oKAKFN0YWIpID0gMSkuIChlKSBUaGUgY2hpcmFsIHBhaXIgZeKCgSDiiJMgaSBl4oKCIG9m
IHRoZSBhbnRpc3ltbWV0cmljIGxpbmUgY291cGxpbmcgdHJhbnNmb3JtcyB1bmRlciB0aGUgbG9j
a2VkIHJvdGF0aW9uIGJ5IGVee8Kxac6xfSBleGFjdGx5IOKAlCBvcmRpbmFyeS4KCiMjIDYuIENo
YXQtdnMtY2hhdCBjb21wYXJhdG9yIHNhbml0eSAodjEuMCBmcm96ZW4sIHJ1biBvbiB0aGUgY2hh
dCBjaGVja3BvaW50IGFnYWluc3QgaXRzZWxmKQoKNDM2IGNoZWNrcywgKio0MzIgUEFTUywgNCBN
SVNTKiosIGFsbCBmb3VyIGV4cGVjdGVkOiB0aGUgdHdvIHNlbGYtY29tcGFyaXNvbiBzdHJ1Y3R1
cmFsIHJvd3MgKGxlZyBsYWJlbHMgY2hhdC9jYzsgaW5kZXBlbmRlbmNlIHdpdG5lc3Mg4oCUIGlk
ZW50aWNhbCBpbnN0cnVtZW50IG1kNSkgYW5kIHRoZSAqKnR3byBkb21haW4gcm93cyBmb3IgYHBo
YXNlMC5zeW1faW50X2NvbnRpbnVvdXNgIOKIiCBbIkcyIl0qKiAoY2hhdCBhbmQgY2MgY29sdW1u
cykg4oCUIHRoZSBILUExLTEgaXRlbS4gRXZlcnkgdmFsdWUgY2hlY2ssIGV2ZXJ5IGZsb2F0IHJ1
bGUsIHRoZSB2ZXJkaWN0IHJlY29tcHV0YXRpb24gYW5kIGV2ZXJ5IGNvbnNpc3RlbmN5IGNoZWNr
IFBBU1MuCgojIyA3LiBIb25lc3R5IGl0ZW1zIGFuZCBvcGVyYXRpb25hbGl6YXRpb25zIChjaGF0
IHNpZGUpCgotICoqSC1BMS0xIChzdHJ1Y3R1cmFsLCBwcmUtdmVyZGljdCwgbWVtbyBleHBlY3Rh
dGlvbiBjb3JyZWN0ZWQpOioqIHRoZSBtZW1vJ3MgUGhhc2UtMCBleHBlY3RhdGlvbiAiY29udGlu
dW91cyBwYXJ0IGV4YWN0bHkgR+KCgiIgbWlzc2VkIHRoZSAqKmRlY291cGxlZCByZWFsLXVuaXQg
cGhhc2UgVSgxKV97z4jigoB9Kio6IHRoZSBvcmllbnRlZCB0ZXJtIGhhcyBpbWFnaW5hcnkgaW5k
aWNlcyBvbmx5IGFuZCB0aGUgdHdvLWJvZHkgdGVybSBkZXBlbmRzIG9ubHkgb24gfM+IfMKyLCBz
byDPiOKCgCBpcyBhIGNvbXBsZXggY29tcG9uZW50IGNvdXBsZWQgdG8gdGhlIHJlc3Qgb25seSB0
aHJvdWdoIHRoZSBkZW5zaXR5IGFuZCBjYXJyeWluZyBpdHMgb3duIHBoYXNlLiBDb250aW51b3Vz
IFN5bV9pbnQgPSBH4oKCIMOXIFUoMSlfe8+I4oKAfSAoZGltIDE1KSwgd2l0aCB0aGUgNy1zZWN0
b3IncyBjb250aW51b3VzIHN5bW1ldHJ5IGV4YWN0bHkgR+KCgiAoZGltIDE0IG9uIHNvKDE0KSkg
YW5kIHRoZSBkaWFnb25hbCBwaGFzZSBicm9rZW4gdG8g4oSk4oKDLiAqKk5vIHRlc3QgaXMgYWZm
ZWN0ZWQ6KiogVDEgYW5kIFQ0IGFjdCBvbiB0aGUgNyAodGhlIFUoMSlfe8+I4oKAfSBjaGFyYWN0
ZXIgb24gYSAyTyBpcyBhIDEtZGltIG9yZGluYXJ5IGNoYXJhY3RlciBvbiB0aGUgc3VtbWFuZCAx
KTsgVDIncyBjZW50cmFsIOKIkjEgbXVzdCBhY3QgYXMg4oiSSWQgb24gdGhlIDctc2VjdG9yIHRv
bywgd2hpY2ggVSgxKV97z4jigoB9IGNhbm5vdCBzdXBwbHk7IFQzJ3MgViA9IFPCueKBtSBpcyB1
bmNoYW5nZWQgYW5kIGFuIGFiZWxpYW4gVSgxKSBjb250cmlidXRlcyBhIOKEpCB0byDPgOKCgSBv
ZiB0aGUgZ3JvdXAsIG5ldmVyIGEgYmluYXJ5LXBvbHloZWRyYWwgbGlmdC4gVGhlIGZyb3plbiBz
Y2hlbWEncyBkb21haW4gZm9yIGBzeW1faW50X2NvbnRpbnVvdXNgIHdhcyB3cml0dGVuIGZvciAi
RzIiIG9ubHkg4oaSICoqdHdvIGRlZmluaXRpb25hbCBjb21wYXJhdG9yIG1pc3NlcyBhcmUgZXhw
ZWN0ZWQgb24gYm90aCBsZWdzKiogKHRoZSBHLU1TQ1MxIEgtTVMtMiBjbGFzcykuIEEgKipzY2hl
bWEgdjEuMSBjYW5kaWRhdGUqKiAoZG9tYWluIHdpZGVuZWQgdG8gWyJHMiIsICJHMnhVMV9wc2kw
Il0sIG5vdGhpbmcgZWxzZSBjaGFuZ2VkKSBpcyBwcmVwYXJlZCBjaGF0LXNpZGUsICoqbm90IGZy
b3plbiBhbmQgbm90IGRpc3BhdGNoZWQqKjsgaXQgaXMgb2ZmZXJlZCBmb3IgdGhlIGF1dGhvcidz
IFM5LXN0eWxlIGVsZWN0aW9uIGFmdGVyIHRoZSBDQyByZXR1cm4uIFRoZSBtZW1vJ3MgVDEgc2Vu
dGVuY2UgIlVuZGVyIFN5bV9pbnQgPSBH4oKCIMOXIChmaW5pdGUgcGhhc2UgZ3JvdXApIiBpcyBy
ZWFkLCBmb3IgdGhlIHJlY29yZCwgYXMgYSBzdGF0ZW1lbnQgYWJvdXQgdGhlIDctc2VjdG9yLgot
ICoqSC1BMS0yIChwb3N0LWxvY2sgb3BlcmF0aW9uYWxpemF0aW9ucywgc3RhdGVkIGhlcmUgc28g
dGhlIHJldHVybiBjYW4gYmUgY2xhc3NpZmllZCk6KiogKGkpIHRoZSBILXNjcmVlbiBjb2RlIHN0
cmluZyBpcyBnZW5lcmF0ZWQgYnkgdGhlIHJ1bGUgKkFETUlTU0lCTEUtSU1QT1JUIGlmZiBpID0g
cGFzcywgaWkgPSBwYXNzLCBpaWkg4oiIIHtwYXNzLCBjb25kaXRpb25hbH0sIGl2IOKIiCB7ZHlu
YW1pY2FsLCBraW5lbWF0aWN9OyBvdGhlcndpc2UgRVhDTFVERUQo4p+odGhlIGNyaXRlcmlhIHdo
b3NlIHZhbHVlIGlzICJmYWlsIiwgaW4gdGhlIG9yZGVyIGksIGlpLCBpaWksIGl2LCBjb21tYS1q
b2luZWTin6kpKjsgSDUncyBjZW50cmFsaXR5IGZhaWx1cmUgaXMgY2FycmllZCBhcyBjcml0ZXJp
b24gKGkpID0gZmFpbCAodGhlIGRvdWJsaW5nIHVuaXQgYW50aWNvbW11dGVzLCBzbyBpdCBpcyBu
b3QgdGVuc29yLWNvbW11dGluZyksIG5vdCBhcyBhIHNlcGFyYXRlIHRva2VuOyByb2xlcyBhcmUg
ImNvbnRyb2wiIChIMSkgLyAiY2FuZGlkYXRlIi4gKGlpKSBgc3Bpbm9yXzJPX2F1dG9tb3JwaGlz
bV9jb3VudGAgY291bnRzIGVsZW1lbnRzIHdpdGggemVybyBkZWZlY3QgKippbmNsdWRpbmcgdGhl
IGlkZW50aXR5KiogKHRoZSBBLTIuMyB3b3JkaW5nKSwgc28gaXRzIHZhbHVlIGlzIDE7IHRoZSBt
aW5pbXVtIGRlZmVjdCBpcyBvdmVyIDJPIOKIliB7wrExfS4gKGlpaSkgVGhlIGxvY2tpbmcgaW52
ZW50b3J5J3MgYHBpMF9nZW5lcmljYCA9IDEgaXMgYW4gYWRvcHRlZCBjb25uZWN0ZWRuZXNzIGZh
Y3QgKEfigoIsIFNVKDMpLCBTVSgyKSBjb25uZWN0ZWQpLCBub3QgYSBjb21wdXRhdGlvbi4KLSAq
KkgtQTEtMyAoc2VsZi1jYXVnaHQgZGV2ZWxvcG1lbnQgYnVnLCBiZWZvcmUgYW55IHJlc3VsdCk6
KiogdGhlIGZpcnN0IGJ1aWxkIG9mIHRoZSBUMSBwcmluY2lwYWwtd2VpZ2h0IHJvdXRpbmUgcHJv
amVjdGVkIHRoZSBjb21wbGV4IGVpZ2Vuc3BhY2VzIG9mIGnCt2FkKGjigoEpIHdpdGggdGhlIHBs
YWluIHRyYW5zcG9zZSBpbnN0ZWFkIG9mIHRoZSBIZXJtaXRpYW4gdHJhbnNwb3NlOyB0aGUgR3Jh
bSBtYXRyaXggd2FzIHNpbmd1bGFyIGFuZCB0aGUgcnVuIGhhbHRlZCB3aXRoIGFuIGV4Y2VwdGlv
biBhdCB0aGF0IHN0ZXAgKFBoYXNlIDAgaGFkIGFscmVhZHkgY29tcGxldGVkKS4gRml4ZWQgdG8g
VuG0tDsgbm8gcmVzdWx0IGNoYW5nZWQgbWVhbmluZy4gQSBjb3NtZXRpYyBsb2cgZi1zdHJpbmcg
d2FzIGNvcnJlY3RlZCBpbiB0aGUgc2FtZSBlZGl0OyB0aGUgaW5zdHJ1bWVudCBtZDUgYWJvdmUg
aXMgdGhlIGZpbmFsIG9uZS4KLSAqKkQtQTEtMSAoZGlzcGF0Y2ggYXNzZW1ibHkpOioqIG9uZSBh
bHBoYWJldGljIFQxIHBhdHRlcm4gKGluZGV4IDkpIG9jY3VycyB0aHJlZSB0aW1lcyBhcyBhIHN1
YnN0cmluZyBjb2luY2lkZW5jZSBpbnNpZGUgb25lIGJhc2U2NCBhcm1vciBib2R5IG9mIHRoZSBk
aXNwYXRjaCAoYSBxdWFyYW50aW5lZCBwYXlsb2FkIHdob3NlIGRlY29kZWQgY29udGVudCBzY2Fu
cyBDTEVBTikuIEJhc2U2NCBpcyB0cmFuc3BvcnQgZW5jb2RpbmcsIG5vdCB0ZXh0OyB0aGUgZGlz
cGF0Y2ggKnBsYWludGV4dCogKG1pbnVzIHRoZSB0aHJlZSBsaXN0IGVtYmVkcyBhbmQgbWludXMg
dGhlIGFybW9yIGJvZGllcykgc2NhbnMgQ0xFQU4sIGFuZCBldmVyeSBwYXlsb2FkIHNjYW5zIENM
RUFOIG9uIGl0cyBvd24uIFJlY29yZGVkIGFzIGFuIGFybW9yLXRyYW5zcG9ydCBjb2xsaXNpb24g
4oCUIHRoZSBhbHBoYWJldGljIGFuYWxvZ3VlIG9mIHRoZSBjb250ZXh0dWFsIG51bWVyaWMgcnVs
ZSDigJQgYnkgcGF0dGVybiBpbmRleCBvbmx5OyB0aGUgZnJvemVuIHNjYW5uZXIgaXMgdW5jaGFu
Z2VkIChhbiBhcm1vci1hd2FyZSBydWxlIGlzIGEgY2FuZGlkYXRlIGZvciBhIGZ1dHVyZSBzY2Fu
bmVyIHJldmlzaW9uLCBmb3IgdGhlIGF1dGhvcidzIGNvbnNpZGVyYXRpb24sIG5vdCB0aGlzIGdh
dGUncykuCi0gKipPdGhlciBELWl0ZW1zOioqIG5vbmUuIFRoZSBjaGF0IGVtaXNzaW9uIHByZWNl
ZGVkIG5vIGNvbXBhcmF0b3IgZWRpdCAoRC1RLTMgbm90IHJlcGVhdGVkKTsgdGhlIG1lbW8sIGxv
Y2sgcmVjb3JkLCBzY2hlbWEsIGNvbXBhcmF0b3IgYW5kIFQxIGxpc3QgYXJlIHVudG91Y2hlZC4K
CiMjIDguIFJlZ2lzdGVycyBhbmQgbm9uLWNsYWltcyAoYmluZGluZywgYXMgbG9ja2VkKQoKUjEt
bWFjaGluZSBmb3IgZXZlcnkgY29tcHV0ZWQgaXRlbTsgUjIgZm9yIHRoZSB2ZXJkaWN0IChjb25k
aXRpb25hbCBvbiB0aGUgYWN0aW9uIG9mIHJlY29yZCBhbmQgdGhlIGFkb3B0ZWQgaG9tb3RvcHkg
aW5wdXRzKTsgUjMgZm9yIHRoZSBIMi9IMyBpZGVudGlmaWNhdGlvbnMgKG5hbWVkLCBub3QgbWFk
ZSkuIE5vIM68X24gdmFsdWUsIHJhdGlvLCBvYnNlcnZhYmxlIG9yIGJyaWRnZTsgbm8gbG9ja2lu
ZyBkeW5hbWljcyAoTS5DVzsgSTHigJNJMyB1bnRvdWNoZWQpOyBHYXRlIDJhJ3MgZHluYW1pY2Fs
IGNsYXVzZSBub3QgY2xvc2VkOyBubyDCpzIuNTAgY2xvc3VyZSAodW5pZmllZCB3aXRoIEk1LCBu
b3QgZGlzY2hhcmdlZCk7IG5vIHJldHJhY3Rpb24gb2YgYW55IMKnMi44NyBhbGdlYnJhIHJlc3Vs
dDsgbm8gUGluLXR5cGUgc3RhdGVtZW50OyBubyBHLVFVQU5UQSBzdGF0ZW1lbnQgKEgtQTEtNSBy
ZW1haW5zIGEgc2NvcGluZyBub3RlOyB0aGUgdmFjdXVtLXNlbGVjdGlvbiBzdWNjZXNzb3IgaXRl
bSByZWdpc3RlcmVkIGluIG1lbW8gwqc5KTsgdGhlIGdhdWdlLXBhcGVyIMKnNy40IGZpcmV3YWxs
IGhlbGQ7ICoqwqcyLjUyIE9wZW4gMyB1bnRvdWNoZWQuKioKCiMjIDkuIE5leHQgc3RlcHMgKHBl
ciB0aGUgbG9ja2VkIG9yZGVyIG9mIG9wZXJhdGlvbnMpCgpQLTQvUC00LmIvUC00LmMgZGlzcGF0
Y2gg4oaSIENDIGxlZyBibGluZCBmcm9tIHNjcmF0Y2ggKG1ldGhvZCB2YXJpYXRpb25zOiBn4oKC
IGZyb20gdGhlIDMtZm9ybTsgb3duIFNMKDIsNykgY2xhc3MgZW51bWVyYXRpb247IG93biBleGFj
dC1zZXF1ZW5jZSBib29ra2VlcGluZzsgb3B0aW9uYWwgTVYtRzEgZXh0ZW5zaW9uKSDihpIgdHdv
LWxlZyBjb21wYXJpc29uIHdpdGggdjEuMCDihpIgUzkgb24gbWlzc2VzICh0aGUgdHdvIEgtQTEt
MSBkb21haW4gcm93cyBleHBlY3RlZCBkZWZpbml0aW9uYWw7IGFueSBvdGhlciBtaXNzIGdlbnVp
bmUpIOKGkiBhdXRob3IncyBTOSBlbGVjdGlvbiAodjEuMSBjYW5kaWRhdGUgYXZhaWxhYmxlKSDi
hpIgZm9sZCBhdXRob3JpemF0aW9uIOKGkiBWNC44NCAowqcyLjkxLlIsIG9uZSBQYXJ0IFZJIHJv
dywgdGhlIMKnMi44Ny/CpzIuODcuQS9NLk9OVCBicmFja2V0cywgdGhlIMKnMTAgaG91c2VrZWVw
aW5nIGJyYWNrZXQpLgo=
=====END-EMBED name=G_2a_A1_CHATLEG_EXECUTION_REPORT.md=====

=====BEGIN-EMBED name=prechecks/precheck_algebra.py md5=cf36395dba7ff35127f40e9f805ff1c7 bytes=9120 encoding=base64 armor_bytes=12320 QUARANTINED=====
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJDaGF0LXNpZGUgUFJFLUxPQ0sgc2FuaXR5IGNoZWNr
cyBmb3IgdGhlIEctMmEtQTEgc3RhZ2luZyBtZW1vIChOT1QgZ2F0ZSByZXN1bHRzKS4KRXhhY3Qg
aW50ZWdlci9yYXRpb25hbCBhcml0aG1ldGljIHdoZXJlIHBvc3NpYmxlIChzeW1weSksIGZsb2F0
cyBvbmx5IGZvciB0aGUgMk8gY2hhcmFjdGVyIHN1bQood2hpY2ggaXMgdGhlbiByb3VuZGVkIGFu
ZCBhc3NlcnRlZCBpbnRlZ3JhbCkuIE5vIGxlZGdlciB2YWx1ZSwgbm8gb2JzZXJ2YXRpb25hbCB0
YXJnZXQgbG9hZGVkLiIiIgppbXBvcnQgaXRlcnRvb2xzLCBtYXRoCmZyb20gZnJhY3Rpb25zIGlt
cG9ydCBGcmFjdGlvbgppbXBvcnQgc3ltcHkgYXMgc3AKCiMgLS0tLS0tLS0tLSBvY3RvbmlvbnM6
IGxpbmVzIHtpLCBpKzEsIGkrM30gbW9kIDcgKGluZGljZXMgMS4uNyksIGVfaSBlX2ogPSBlX2sg
Y3ljbGljIC0tLS0tLS0tLS0KTElORVMgPSBbKChpLTEpJTcrMSwgKGkpJTcrMSwgKGkrMiklNysx
KSBmb3IgaSBpbiByYW5nZSgxLDgpXSAgICMgKDEsMiw0KSwoMiwzLDUpLC4uLiwoNywxLDMpCmFz
c2VydCBzb3J0ZWQoc29ydGVkKGwpIGZvciBsIGluIExJTkVTKSA9PSBzb3J0ZWQoc29ydGVkKGwp
IGZvciBsIGluIFsoMSwyLDQpLCgyLDMsNSksKDMsNCw2KSwoNCw1LDcpLCg1LDYsMSksKDYsNywy
KSwoNywxLDMpXSkKbXVsdCA9IHt9ICAjIChpLGopIC0+IChzaWduLCBrKSBmb3IgaW1hZ2luYXJ5
IHVuaXRzCmZvciAoYSxiLGMpIGluIExJTkVTOgogICAgZm9yICh4LHkseikgaW4gWyhhLGIsYyks
KGIsYyxhKSwoYyxhLGIpXToKICAgICAgICBtdWx0Wyh4LHkpXSA9ICgxLHopOyBtdWx0Wyh5LHgp
XSA9ICgtMSx6KQpkZWYgb211bChwLHEpOgogICAgIiIicCxxOiBsZW5ndGgtOCByYXRpb25hbCB2
ZWN0b3JzIChpbmRleCAwID0gcmVhbCB1bml0KS4iIiIKICAgIHI9W0ZyYWN0aW9uKDApXSo4CiAg
ICBmb3IgaSBpbiByYW5nZSg4KToKICAgICAgICBpZiBwW2ldPT0wOiBjb250aW51ZQogICAgICAg
IGZvciBqIGluIHJhbmdlKDgpOgogICAgICAgICAgICBpZiBxW2pdPT0wOiBjb250aW51ZQogICAg
ICAgICAgICBpZiBpPT0wOiByW2pdKz1wW2ldKnFbal0KICAgICAgICAgICAgZWxpZiBqPT0wOiBy
W2ldKz1wW2ldKnFbal0KICAgICAgICAgICAgZWxpZiBpPT1qOiByWzBdLT1wW2ldKnFbal0KICAg
ICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHMsaz1tdWx0WyhpLGopXTsgcltrXSs9cypw
W2ldKnFbal0KICAgIHJldHVybiByCmRlZiB1bml0KGkpOgogICAgdj1bRnJhY3Rpb24oMCldKjg7
IHZbaV09RnJhY3Rpb24oMSk7IHJldHVybiB2CiMgYWx0ZXJuYXRpdml0eSAvIGRpdmlzaW9uIGNo
ZWNrIG9uIGJhc2lzCmZvciBpIGluIHJhbmdlKDEsOCk6CiAgICBmb3IgaiBpbiByYW5nZSgxLDgp
OgogICAgICAgIGZvciBrIGluIHJhbmdlKDEsOCk6CiAgICAgICAgICAgIHBhc3MKIyAtLS0tLS0t
LS0tIGRlcml2YXRpb24gYWxnZWJyYSBnMiAoMTQtZGltKSBhcyA3eDcgbWF0cmljZXM6IEQoeHkp
PUQoeCl5K3hEKHkpIC0tLS0tLS0tLS0KIyBVbmtub3duIEQgPSA3eDcgcmVhbCBhbnRpc3ltbWV0
cmljIGFjdGluZyBvbiBJbSBPIChkZXJpdmF0aW9ucyBraWxsIHRoZSByZWFsIHVuaXQpLiAyMSB1
bmtub3ducy4Kc3ltcyA9IHNwLnN5bWJvbHMoJ2QwOjIxJykKRCA9IHNwLnplcm9zKDcsNyk7IHQ9
MApmb3IgaSBpbiByYW5nZSg3KToKICAgIGZvciBqIGluIHJhbmdlKGkrMSw3KToKICAgICAgICBE
W2ksal09c3ltc1t0XTsgRFtqLGldPS1zeW1zW3RdOyB0Kz0xCmRlZiBEYXBwbHkodik6ICAgIyB2
OiBsZW5ndGgtOCBGcmFjdGlvbiB2ZWN0b3IgLT4gc3ltcHkgdmVjdG9yIChpbWFnIHBhcnQgb25s
eTsgcmVhbCBwYXJ0IC0+IDApCiAgICBvdXQ9W3NwLkludGVnZXIoMCldKjgKICAgIGZvciBpIGlu
IHJhbmdlKDEsOCk6CiAgICAgICAgaWYgdltpXSE9MDoKICAgICAgICAgICAgZm9yIGogaW4gcmFu
Z2UoMSw4KToKICAgICAgICAgICAgICAgIG91dFtqXSs9IERbai0xLGktMV0qc3AuUmF0aW9uYWwo
dltpXS5udW1lcmF0b3IsIHZbaV0uZGVub21pbmF0b3IpCiAgICByZXR1cm4gb3V0CmVxcz1bXQpm
b3IgaSBpbiByYW5nZSgxLDgpOgogICAgZm9yIGogaW4gcmFuZ2UoMSw4KToKICAgICAgICBlaSwg
ZWogPSB1bml0KGkpLCB1bml0KGopCiAgICAgICAgbGhzID0gRGFwcGx5KG9tdWwoZWksZWopKQog
ICAgICAgICMgRCh4KXkgKyB4IEQoeSk6IEQoZWkpID0gc3VtX20gRFttLGldIGVfbQogICAgICAg
IHJocz1bc3AuSW50ZWdlcigwKV0qOAogICAgICAgIGZvciBtIGluIHJhbmdlKDEsOCk6CiAgICAg
ICAgICAgIGlmIERbbS0xLGktMV0hPTA6CiAgICAgICAgICAgICAgICBwcm9kID0gb211bCh1bml0
KG0pLCBlaikKICAgICAgICAgICAgICAgIGZvciBuIGluIHJhbmdlKDgpOiByaHNbbl0rPSBEW20t
MSxpLTFdKnNwLlJhdGlvbmFsKHByb2Rbbl0ubnVtZXJhdG9yLCBwcm9kW25dLmRlbm9taW5hdG9y
KQogICAgICAgICAgICBpZiBEW20tMSxqLTFdIT0wOgogICAgICAgICAgICAgICAgcHJvZCA9IG9t
dWwoZWksIHVuaXQobSkpCiAgICAgICAgICAgICAgICBmb3IgbiBpbiByYW5nZSg4KTogcmhzW25d
Kz0gRFttLTEsai0xXSpzcC5SYXRpb25hbChwcm9kW25dLm51bWVyYXRvciwgcHJvZFtuXS5kZW5v
bWluYXRvcikKICAgICAgICBmb3IgbiBpbiByYW5nZSg4KTogZXFzLmFwcGVuZChzcC5leHBhbmQo
bGhzW25dLXJoc1tuXSkpCkEgPSBzcC5NYXRyaXgoW1tzcC5Qb2x5KGUsICpzeW1zKS5jb2VmZl9t
b25vbWlhbChzKSBpZiBlIT0wIGVsc2UgMCBmb3IgcyBpbiBzeW1zXSBmb3IgZSBpbiBlcXMgaWYg
ZSE9MF0pCm5zID0gQS5udWxsc3BhY2UoKQpwcmludCgiZGltIERlcihPKSA9IGcyID0iLCBsZW4o
bnMpKQphc3NlcnQgbGVuKG5zKT09MTQKZzIgPSBbXQpmb3IgdiBpbiBuczoKICAgIE0gPSBzcC56
ZXJvcyg3LDcpOyB0PTAKICAgIGZvciBpIGluIHJhbmdlKDcpOgogICAgICAgIGZvciBqIGluIHJh
bmdlKGkrMSw3KToKICAgICAgICAgICAgTVtpLGpdPXZbdF07IE1baixpXT0tdlt0XTsgdCs9MQog
ICAgZzIuYXBwZW5kKE0pCgojIC0tLS0tLS0tLS0gbGVmdC1tdWx0aXBsaWNhdGlvbiBtYXBzIExf
YSBvbiBSXjggYW5kIHRoZSBzcGluKDcpL3N1KDQpIGJpdmVjdG9yIGFsZ2VicmFzIC0tLS0tLS0t
LS0KZGVmIExtYXQoYSk6CiAgICBNID0gc3AuemVyb3MoOCw4KQogICAgZm9yIGogaW4gcmFuZ2Uo
OCk6CiAgICAgICAgY29sID0gb211bCh1bml0KGEpLCB1bml0KGopKQogICAgICAgIGZvciBpIGlu
IHJhbmdlKDgpOiBNW2ksal09c3AuUmF0aW9uYWwoY29sW2ldLm51bWVyYXRvciwgY29sW2ldLmRl
bm9taW5hdG9yKQogICAgcmV0dXJuIE0KTCA9IHthOiBMbWF0KGEpIGZvciBhIGluIHJhbmdlKDEs
OCl9CmZvciBhIGluIHJhbmdlKDEsOCk6CiAgICBmb3IgYiBpbiByYW5nZSgxLDgpOgogICAgICAg
IFMgPSBMW2FdKkxbYl0rTFtiXSpMW2FdCiAgICAgICAgYXNzZXJ0IFMgPT0gKC0yKnNwLmV5ZSg4
KSBpZiBhPT1iIGVsc2Ugc3AuemVyb3MoOCw4KSksICJDbGlmZm9yZCByZWxhdGlvbnMgZmFpbCIK
cHJpbnQoIkNsaWZmb3JkIHJlbGF0aW9ucyBMX2EgTF9iICsgTF9iIExfYSA9IC0yIGRlbHRhOiBP
SyAoQ2woMCw3KSBvbiBSXjgpIikKZGVmIHNwYW5fZGltKG1hdHMpOgogICAgcmV0dXJuIHNwLk1h
dHJpeChbbGlzdChNKSBmb3IgTSBpbiBtYXRzXSkucmFuaygpCmJpdjcgPSBbTFthXSpMW2JdIGZv
ciBhIGluIHJhbmdlKDEsOCkgZm9yIGIgaW4gcmFuZ2UoYSsxLDgpXQpwcmludCgiZGltIHNwYW57
TF9hIExfYiwgYTxiPD03fSA9Iiwgc3Bhbl9kaW0oYml2NyksICIoc3Bpbig3KSA9IDIxIGV4cGVj
dGVkKSIpCmJpdjYgPSBbTFthXSpMW2JdIGZvciBhIGluIHJhbmdlKDEsNykgZm9yIGIgaW4gcmFu
Z2UoYSsxLDcpXQpwcmludCgiZGltIHNwYW57TF9hIExfYiwgYTxiPD02fSA9Iiwgc3Bhbl9kaW0o
Yml2NiksICIoc3Bpbig2KT1zdSg0KSA9IDE1IGV4cGVjdGVkKSIpCiMgZzIgZW1iZWRkZWQgaW4g
c28oOCkgYXMgZGVyaXZhdGlvbnMgKGFjdCBvbiBJbSBPLCBraWxsIDEpCmcyXzggPSBbXQpmb3Ig
TSBpbiBnMjoKICAgIE04ID0gc3AuemVyb3MoOCw4KTsgTThbMTosMTpdID0gTTsgZzJfOC5hcHBl
bmQoTTgpCnByaW50KCJkaW0gZzIgaW4gc28oOCkgPSIsIHNwYW5fZGltKGcyXzgpKQpwcmludCgi
ZGltIHNwYW4oZzIgKyBzcGluNykgPSIsIHNwYW5fZGltKGcyXzgrYml2NyksICIoMjEgZXhwZWN0
ZWQgaWYgZzIg4oqCIHNwaW4oNylfTCkiKQpwcmludCgiZGltIHNwYW4oZzIgKyBzdTQpICA9Iiwg
c3Bhbl9kaW0oZzJfOCtiaXY2KSwgIuKGkiBkaW0oZzIg4oipIHN1KDQpKSA9IiwgMTQrMTUtc3Bh
bl9kaW0oZzJfOCtiaXY2KSwgIig4ID0gc3UoMykgZXhwZWN0ZWQpIikKCiMgLS0tLS0tLS0tLSBH
MiBpbnZvbHV0aW9uczogZml4ZWQgc3ViYWxnZWJyYSBkaW1zOyB0aGUgdHJhY2UgbGVtbWEgLS0t
LS0tLS0tLQojIFRoZSBjb29yZGluYXRlIGludm9sdXRpb24gc2lnbWFfSCBmaXhpbmcgdGhlIHF1
YXRlcm5pb24gc3ViYWxnZWJyYSBvZiBsaW5lICgxLDIsNCkgcG9pbnR3aXNlOgpkZWYgaXNfYXV0
KFApOiAgICMgUDogOHg4IHN5bXB5IG1hdHJpeDsgY2hlY2sgUCh4eSk9UCh4KVAoeSkgb24gYmFz
aXMKICAgIGZvciBpIGluIHJhbmdlKDgpOgogICAgICAgIGZvciBqIGluIHJhbmdlKDgpOgogICAg
ICAgICAgICB4eSA9IG9tdWwodW5pdChpKSx1bml0KGopKTsgbGhzID0gUCpzcC5NYXRyaXgoW3Nw
LlJhdGlvbmFsKHYubnVtZXJhdG9yLHYuZGVub21pbmF0b3IpIGZvciB2IGluIHh5XSkKICAgICAg
ICAgICAgUGkgPSBbRnJhY3Rpb24oaW50KFBbayxpXS5wKSwgaW50KFBbayxpXS5xKSkgZm9yIGsg
aW4gcmFuZ2UoOCldCiAgICAgICAgICAgIFBqID0gW0ZyYWN0aW9uKGludChQW2ssal0ucCksIGlu
dChQW2ssal0ucSkpIGZvciBrIGluIHJhbmdlKDgpXQogICAgICAgICAgICByaHMgPSBvbXVsKFBp
LFBqKTsgcmhzID0gc3AuTWF0cml4KFtzcC5SYXRpb25hbCh2Lm51bWVyYXRvcix2LmRlbm9taW5h
dG9yKSBmb3IgdiBpbiByaHNdKQogICAgICAgICAgICBpZiBsaHMhPXJoczogcmV0dXJuIEZhbHNl
CiAgICByZXR1cm4gVHJ1ZQpsaW5lID0gKDEsMiw0KQpzaWcgPSBzcC5kaWFnKCooWzFdK1sxIGlm
IGkgaW4gbGluZSBlbHNlIC0xIGZvciBpIGluIHJhbmdlKDEsOCldKSkKcHJpbnQoInNpZ21hX0gg
KGZpeCBsaW5lIDEyNCwgbmVnYXRlIGNvbXBsZW1lbnQpIGlzIGFuIGF1dG9tb3JwaGlzbToiLCBp
c19hdXQoc2lnKSwgIjsgdHJhY2Ugb24gSW0gTyA9Iiwgc3VtKHNpZ1tpLGldIGZvciBpIGluIHJh
bmdlKDEsOCkpKQojIGEgJ3dyb25nJyBpbnZvbHV0aW9uOiBuZWdhdGUgb25lIHVuaXQgb25seSAt
PiBub3QgYW4gYXV0b21vcnBoaXNtCmJhZCA9IHNwLmRpYWcoKihbMV0rWy0xIGlmIGk9PTcgZWxz
ZSAxIGZvciBpIGluIHJhbmdlKDEsOCldKSkKcHJpbnQoIm5lZ2F0aW5nIGEgc2luZ2xlIHVuaXQg
aXMgYW4gYXV0b21vcnBoaXNtOiIsIGlzX2F1dChiYWQpKQojIFNpZ25lZCBsaWZ0IG9mIGEgRmFu
byBjb2xsaW5lYXRpb24gaW52b2x1dGlvbjogY2hvb3NlIHRoZSBjb2xsaW5lYXRpb24gZml4aW5n
IGxpbmUgKDEsMiw0KSBwb2ludHdpc2UgYW5kIHN3YXBwaW5nICgzIDUpKDYgNyk/IGNoZWNrIHdo
aWNoIHBhaXJzCiMgRmFubyBpbnZvbHV0aW9uIHQ6IGZpeGVzIHsxLDIsNH0sIHN3YXBzIDM8LT4/
IFdlIHNlYXJjaCBhbGwgc2lnbmVkIHBlcm11dGF0aW9uIG1hdHJpY2VzIHRoYXQgYXJlIGF1dG9t
b3JwaGlzbXMgYW5kIHByb2plY3QgdG8gYSBmaXhlZC1saW5lIGludm9sdXRpb24uCmltcG9ydCBp
dGVydG9vbHMKcHRzPVsxLDIsMyw0LDUsNiw3XQpkZWYgcGVybV9tYXRyaXgocGVybSwgc2lnbnMp
OgogICAgUD1zcC56ZXJvcyg4LDgpOyBQWzAsMF09MQogICAgZm9yIGkgaW4gcmFuZ2UoMSw4KTog
UFtwZXJtW2ldLCBpXSA9IHNpZ25zW2ldCiAgICByZXR1cm4gUAojIGVudW1lcmF0ZSBjb2xsaW5l
YXRpb25zIHRoYXQgZml4IDEsMiw0IHBvaW50d2lzZSAodGhlIHBvaW50d2lzZSBsaW5lIHN0YWJp
bGl6ZXIsIG9yZGVyIDQgPSBWNCkKb3RoZXJzPVszLDUsNiw3XQpmb3VuZD1bXQpmb3IgaW1nIGlu
IGl0ZXJ0b29scy5wZXJtdXRhdGlvbnMob3RoZXJzKToKICAgIHBlcm09ezE6MSwyOjIsNDo0fTsg
cGVybS51cGRhdGUoZGljdCh6aXAob3RoZXJzLGltZykpKQogICAgIyBjb2xsaW5lYXRpb24gdGVz
dDogbWFwcyBsaW5lcyB0byBsaW5lcwogICAgb2sgPSBhbGwodHVwbGUoc29ydGVkKHBlcm1beF0g
Zm9yIHggaW4gbCkpIGluIHt0dXBsZShzb3J0ZWQobSkpIGZvciBtIGluIExJTkVTfSBmb3IgbCBp
biBMSU5FUykKICAgIGlmIG5vdCBvazogY29udGludWUKICAgIGlmIGFsbChwZXJtW3hdPT14IGZv
ciB4IGluIG90aGVycyk6IGNvbnRpbnVlCiAgICAjIGZpbmQgc2lnbiB2ZWN0b3JzIG1ha2luZyBp
dCBhbiBhdXRvbW9ycGhpc20KICAgIGZvciBzZ24gaW4gaXRlcnRvb2xzLnByb2R1Y3QoWzEsLTFd
LCByZXBlYXQ9Nyk6CiAgICAgICAgc2lnbnM9e2krMTpzZ25baV0gZm9yIGkgaW4gcmFuZ2UoNyl9
CiAgICAgICAgUD1wZXJtX21hdHJpeChwZXJtLHNpZ25zKQogICAgICAgIGlmIGlzX2F1dChQKToK
ICAgICAgICAgICAgdHIgPSBzdW0oUFtpLGldIGZvciBpIGluIHJhbmdlKDEsOCkpCiAgICAgICAg
ICAgIGZvdW5kLmFwcGVuZCgocGVybSwgc2lnbnMsIHRyKSkKcHJpbnQoInNpZ25lZCBhdXRvbW9y
cGhpc20gbGlmdHMgb2YgdGhlIHRocmVlIG5vbnRyaXZpYWwgcG9pbnR3aXNlLWxpbmUtc3RhYmls
aXplciBjb2xsaW5lYXRpb25zOiIsIGxlbihmb3VuZCkpCm9yZGVycz17fQpmb3IgcGVybSxzaWdu
cyx0ciBpbiBmb3VuZDoKICAgIFA9cGVybV9tYXRyaXgocGVybSxzaWducyk7IG89MiBpZiBQKlA9
PXNwLmV5ZSg4KSBlbHNlICg0IGlmIChQKlApKihQKlApPT1zcC5leWUoOCkgZWxzZSAwKQogICAg
b3JkZXJzLnNldGRlZmF1bHQoKG8sdHIpLDApOyBvcmRlcnNbKG8sdHIpXSs9MQpwcmludCgiICAg
KG9yZGVyLCB0cmFjZSBvbiA3KSAtPiBjb3VudCBvdmVyIHRoZSAyNCBzaWduZWQgYXV0b21vcnBo
aXNtIGxpZnRzOiIsIG9yZGVycykKYXNzZXJ0IGFsbCh0cj09LTEgZm9yIChvLHRyKSBpbiBvcmRl
cnMgaWYgbz09MiksICJhbiBvcmRlci0yIGF1dG9tb3JwaGlzbSB3aXRoIHRyYWNlICE9IC0xIGV4
aXN0cyIKcGFzcwpwcmludCgiICAgZXZlcnkgT1JERVItMiBsaWZ0IGhhcyB0cmFjZSAtMSAocGVy
bXV0YXRpb24gY2hhcmFjdGVyIDMsIHJobzYgY2hhcmFjdGVyIDIg4oCUIHRoZSB3cm9uZy1tb2R1
bGUgZ2FwIGlzIDQpOyB0aGUgdHJhY2UtMyBsaWZ0cyBhcmUgb2YgT1JERVIgNCAoc3F1YXJlIHRv
IHNpZ21hX0gpLiIpCgojIC0tLS0tLS0tLS0gMk8gYW5kIHRoZSBzcGluLTMvMiBjaGFyYWN0ZXI6
IEZyb2Jlbml1c+KAk1NjaHVyIGluZGljYXRvciAtLS0tLS0tLS0tCmltcG9ydCBjbWF0aAojIDJP
ID0gYmluYXJ5IG9jdGFoZWRyYWw6IDQ4IHVuaXQgcXVhdGVybmlvbnM6IDI0IEh1cndpdHogdW5p
dHMgKDJUKSArIDI0IG9mIHRoZSBmb3JtICjCsTHCsWkpL3NxcnQyIHBlcm11dGF0aW9ucwpkZWYg
cW11bChhLGIpOgogICAgYTAsYTEsYTIsYTM9YTsgYjAsYjEsYjIsYjM9YgogICAgcmV0dXJuIChh
MCpiMC1hMSpiMS1hMipiMi1hMypiMywgYTAqYjErYTEqYjArYTIqYjMtYTMqYjIsIGEwKmIyLWEx
KmIzK2EyKmIwK2EzKmIxLCBhMCpiMythMSpiMi1hMipiMSthMypiMCkKZWxzPXNldCgpCnMyPTEv
bWF0aC5zcXJ0KDIpCmZvciBzaWducyBpbiBpdGVydG9vbHMucHJvZHVjdChbMSwtMV0scmVwZWF0
PTQpOgogICAgZm9yIHBvcyBpbiByYW5nZSg0KToKICAgICAgICB2PVswLDAsMCwwXTsgdltwb3Nd
PXNpZ25zW3Bvc107IGVscy5hZGQodHVwbGUocm91bmQoeCw5KSBmb3IgeCBpbiB2KSkKICAgIGVs
cy5hZGQodHVwbGUocm91bmQoMC41KnMsOSkgZm9yIHMgaW4gc2lnbnMpKQpmb3IgaSxqIGluIGl0
ZXJ0b29scy5jb21iaW5hdGlvbnMocmFuZ2UoNCksMik6CiAgICBmb3Igc2kgaW4gKDEsLTEpOgog
ICAgICAgIGZvciBzaiBpbiAoMSwtMSk6CiAgICAgICAgICAgIHY9WzAsMCwwLDBdOyB2W2ldPXNp
KnMyOyB2W2pdPXNqKnMyOyBlbHMuYWRkKHR1cGxlKHJvdW5kKHgsOSkgZm9yIHggaW4gdikpCmVs
cz1saXN0KGVscyk7IGFzc2VydCBsZW4oZWxzKT09NDgKZGVmIGNoaTMyKHEpOiAgIyBzcGluLTMv
MiBjaGFyYWN0ZXI6IHEgPSBjb3MocGhpKSArIHNpbihwaGkpIG4KICAgIHBoaT1tYXRoLmFjb3Mo
bWF4KC0xLG1pbigxLHFbMF0pKSkKICAgIHJldHVybiAyKm1hdGguY29zKDMqcGhpKSsyKm1hdGgu
Y29zKHBoaSkKZnMgPSBzdW0oY2hpMzIodHVwbGUocm91bmQoeCw5KSBmb3IgeCBpbiBxbXVsKHEs
cSkpKSBmb3IgcSBpbiBlbHMpLzQ4Cm5vcm0gPSBzdW0oY2hpMzIocSkqKjIgZm9yIHEgaW4gZWxz
KS80OApwcmludCgiMk86IHxHfD00OCwgPGNoaV8zLzIsY2hpXzMvMj4gPSIsIHJvdW5kKG5vcm0s
OSksICIsIGNoaSgxKT0iLCBjaGkzMigoMSwwLDAsMCkpLCAiLCBjaGkoLTEpPSIsIGNoaTMyKCgt
MSwwLDAsMCkpLCAiLCBGcm9iZW5pdXPigJNTY2h1ciBpbmRpY2F0b3IgPSIsIHJvdW5kKGZzLDkp
KQphc3NlcnQgcm91bmQobm9ybSk9PTEgYW5kIHJvdW5kKGZzKT09LTEKIyAtLS0tLS0tLS0tIFNM
KDIsNyk6IG51bWJlciBvZiBzb2x1dGlvbnMgb2YgZ14yID0gMSAtLS0tLS0tLS0tCnA9NwpTTD1b
XQpmb3IgYSxiLGMsZCBpbiBpdGVydG9vbHMucHJvZHVjdChyYW5nZShwKSxyZXBlYXQ9NCk6CiAg
ICBpZiAoYSpkLWIqYyklcD09MTogU0wuYXBwZW5kKChhLGIsYyxkKSkKYXNzZXJ0IGxlbihTTCk9
PTMzNgpkZWYgbTIoZyxoKToKICAgIGEsYixjLGQ9ZzsgZSxmLGdnLGhoPWgKICAgIHJldHVybiAo
KGEqZStiKmdnKSVwLChhKmYrYipoaCklcCwoYyplK2QqZ2cpJXAsKGMqZitkKmhoKSVwKQpzcTE9
W2cgZm9yIGcgaW4gU0wgaWYgbTIoZyxnKT09KDEsMCwwLDEpXQpwcmludCgiU0woMiw3KTogI3tn
OiBnXjI9MX0gPSIsIGxlbihzcTEpLCAiKDIgZXhwZWN0ZWQ6IG9ubHkgwrFJKSAtPiIsIHNxMSkK
=====END-EMBED name=prechecks/precheck_algebra.py=====

=====BEGIN-EMBED name=prechecks/precheck_algebra.log md5=81b5512817f7eebeb668817f6b3562f9 bytes=1053 encoding=base64 armor_bytes=1423 QUARANTINED=====
ZGltIERlcihPKSA9IGcyID0gMTQKQ2xpZmZvcmQgcmVsYXRpb25zIExfYSBMX2IgKyBMX2IgTF9h
ID0gLTIgZGVsdGE6IE9LIChDbCgwLDcpIG9uIFJeOCkKZGltIHNwYW57TF9hIExfYiwgYTxiPD03
fSA9IDIxIChzcGluKDcpID0gMjEgZXhwZWN0ZWQpCmRpbSBzcGFue0xfYSBMX2IsIGE8Yjw9Nn0g
PSAxNSAoc3Bpbig2KT1zdSg0KSA9IDE1IGV4cGVjdGVkKQpkaW0gZzIgaW4gc28oOCkgPSAxNApk
aW0gc3BhbihnMiArIHNwaW43KSA9IDIxICgyMSBleHBlY3RlZCBpZiBnMiDiioIgc3Bpbig3KV9M
KQpkaW0gc3BhbihnMiArIHN1NCkgID0gMjEg4oaSIGRpbShnMiDiiKkgc3UoNCkpID0gOCAoOCA9
IHN1KDMpIGV4cGVjdGVkKQpzaWdtYV9IIChmaXggbGluZSAxMjQsIG5lZ2F0ZSBjb21wbGVtZW50
KSBpcyBhbiBhdXRvbW9ycGhpc206IFRydWUgOyB0cmFjZSBvbiBJbSBPID0gLTEKbmVnYXRpbmcg
YSBzaW5nbGUgdW5pdCBpcyBhbiBhdXRvbW9ycGhpc206IEZhbHNlCnNpZ25lZCBhdXRvbW9ycGhp
c20gbGlmdHMgb2YgdGhlIHRocmVlIG5vbnRyaXZpYWwgcG9pbnR3aXNlLWxpbmUtc3RhYmlsaXpl
ciBjb2xsaW5lYXRpb25zOiAyNAogICAob3JkZXIsIHRyYWNlIG9uIDcpIC0+IGNvdW50IG92ZXIg
dGhlIDI0IHNpZ25lZCBhdXRvbW9ycGhpc20gbGlmdHM6IHsoNCwgMyk6IDYsICgyLCAtMSk6IDEy
LCAoNCwgLTEpOiA2fQogICBldmVyeSBPUkRFUi0yIGxpZnQgaGFzIHRyYWNlIC0xIChwZXJtdXRh
dGlvbiBjaGFyYWN0ZXIgMywgcmhvNiBjaGFyYWN0ZXIgMiDigJQgdGhlIHdyb25nLW1vZHVsZSBn
YXAgaXMgNCk7IHRoZSB0cmFjZS0zIGxpZnRzIGFyZSBvZiBPUkRFUiA0IChzcXVhcmUgdG8gc2ln
bWFfSCkuCjJPOiB8R3w9NDgsIDxjaGlfMy8yLGNoaV8zLzI+ID0gMS4wICwgY2hpKDEpPSA0LjAg
LCBjaGkoLTEpPSAtNC4wICwgRnJvYmVuaXVz4oCTU2NodXIgaW5kaWNhdG9yID0gLTAuOTk5OTk5
OTk1ClNMKDIsNyk6ICN7ZzogZ14yPTF9ID0gMiAoMiBleHBlY3RlZDogb25seSDCsUkpIC0+IFso
MSwgMCwgMCwgMSksICg2LCAwLCAwLCA2KV0K
=====END-EMBED name=prechecks/precheck_algebra.log=====

