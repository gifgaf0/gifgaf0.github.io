# G-MSCS2 — CC LEG DISPATCH (P-4 single-file in-band; P-4.b armor; P-4.c lone delivery)

**Gate:** G-MSCS2 (Multi-Species Channel Speed, the l = 4 / cubic-effective texture family — the E-MS-5 registered successor of G-MSCS1). **Date:** September 26, 2026.
**Base ledger:** `SQT_Master_Ledger_v4_84_CANONICAL.md` md5 `f36bbdb04104008783f2763f70fb916f` (the canonical ledger is deliberately not in the repository and is not needed for this leg).
**Lock chain (all FROZEN):** memo v2 `efdcabdcd937cda4acb64f941dc4bb2b` (46,053 B) · lock record `49232d4c42061c4536867eba14aae501` (Addendum A-2.1–A-2.10, binding) · schema v1.0 `66f586d7b6c5e8228394222ddfda73f2` · comparator v1.0 `80d3b9078788fb17f57945da7d9c2c96` (asserts the schema md5; 18 selftest suites) · gate T1 list `be921b8c29f7578e85ed92f1450c1956` (36 patterns = base `05302210cc4ceb70553acbe8379e9fc3` + the G-MSCS1 stratum; scanner `6b86290090a8c84f1b1a0a99ec0bf697`) · X-1 `200e7a8b775577564369c6924d38a84c` (2,767 B) · X-6 chat `c04c0b8ea34cfe60f231aa06828e6ce4` / cc `249e11dd53c4cb82f302b15d3c94c337` (the G-MSCS1 checkpoints of record: continuity-pin sources).
**Elections (T3):** E-MS2-1 (a)+(b) · E-MS2-2 (a) · E-MS2-2b (a)+(b) · E-MS2-2c ⟨001⟩ primary / ⟨111⟩ reported · E-MS2-3 (a) no Born · E-MS2-4 (a) · E-MS2-5 (a) K̃₄ = (5/2)(Σx⁴ − 3/5) · E-MS2-6 (a) · E-MS2-7 base 05302210 + G-MSCS1 stratum · E-MS2-8 (a). Schema codes: `a+b`, `a`, `a+b`, `001+111`, `a`, `a`, `a`, `a`, `05302210+MSCS1stratum`, `a`.
**Chat-leg state at dispatch:** Phases 0, 2, 3 EXECUTED (checkpoint `1c5b6b59829d2a6b9ae2b1a7a016832d`; chat-vs-chat comparator sanity `0a10623660c8fbaed4c37ec388978593`); all 13 Phase-0 pins/controls PASS; the verdict class and every coefficient are in the quarantined checkpoint/report. **D-T1 RETIRED:** the T1 lists are embedded here; your instrument must halt without them and must scan itself and the memo at every invocation.

**T1-scan exemptions (the G-POLY1 justified-exemption class):** the two list embeds necessarily contain every pattern; the dispatch **plaintext** (minus those two embeds and minus the base64 armor *bodies*, which are transport encoding, not text) scans CLEAN against the gate list; every payload scans CLEAN on its own before embedding. **D-MS2-1 (recorded, the D-A1-1 class):** short patterns may occur as substring coincidences inside base64 armor bodies; they are logged here by pattern index; every decoded payload is CLEAN. Armor-body collisions by pattern index (D-MS2-1): `G_MSCS2_PHASE0_EXECUTION_REPORT.md`: [9].

**ACTIVATION FLAG — the author chooses exactly one line and it must be present verbatim:**
- `ACTIVATE: G-MSCS2-CC-LEG-1 WITH-A3` — proceed, applying **Addendum A-3** (§0b below) as part of the lock record's definitions.
- `ACTIVATE: G-MSCS2-CC-LEG-1 LITERAL-A29` — proceed under the lock record exactly as written (A-2.9 literal); A-3 is then not in force.
Without one of these lines, do not proceed.

## 0. Blindness clause (read first)

Twelve embeds are **QUARANTINED** (base64-armored): the chat instrument, its two checkpoints, its compare files, its run logs, its two execution reports and its post-run diagnostics. **Do not decode any of them until step 4.** Build your instrument from the memo (§0–§2, §4–§9), the lock record (Addendum A-2 — binding definitions; A-3 if the WITH-A3 flag is given) and the schema ONLY, from scratch, in your own structure. **Method variation requested (lock record §3):** the SO(3)/ODF averages by a different route than a (16, 10, 16) Euler product grid — e.g. a Lebedev or Gauss product of different orders exact to degree ≥ 12, or the analytic generalized-spherical-harmonic route (the l ≤ 4 harmonic decomposition of the rotated tensor contracted with the ODF's l = 2, 4 coefficients); your own HS reference optimizer (any procedure reproducing the X-6 `pins_vrh0[cfg].hs_ref` / `G_HS` to the PIN-HS0 tolerance); your own labelling and fits. The G-MSCS1 instruments on `main` (`gmscs1_gate/g_mscs1_chatleg.py`, `g_mscs1_ccleg.py`) may be read for the inherited descriptor definitions, as the memo says — not copied. Commit your checkpoint BEFORE any armor is opened and cite that commit as the pre-consultation checkpoint. If your read of this file is paged or truncated, locate embed boundaries by grepping sentinel lines only.

## 0b. Addendum A-3 to the lock record (definitional; author-selectable by the activation flag; no schema/comparator change)

The chat leg found, post-emission, that one control clause and one schema null tolerance were written against an ambiguity inherited from G-MSCS1's cubic l = 2 definition (recorded in the quarantined report as H-MS2-4/H-MS2-5; the details are quarantined so that your leg stays blind to the chat values). What you need to know to build is definitional and is stated here in full:

- **A-3.1 F-CTRL-L2NULL scope.** A-2.9's clause "…and r_agg unchanged to 10⁻¹²" applies to the **pure l = 2 term** (t₄ = 0; an identity — the aggregate is isotropic there). For the **mixed** (t₂, t₄) term under the inherited l = 2 weight (A-2.2: 1 + t₂·P₂ on the *elected descriptor axis*, which is not an O_h-invariant ODF), only the three **tensor** clauses (⟨C⟩_V, ⟨S⟩_R, C_HS unchanged ≤ 10⁻¹²) are the control; the mixed-term r_agg change is a **reported diagnostic** `mixed_r_agg_change_A29` per cubic key (the single-axis E₂ weight has l = 2 content and can couple to the l = 4 speed perturbation beyond second order), **not** a pass/fail criterion.
- **A-3.2 κ₂₄ by a basis-independent estimator.** Report per key `kappa24_richardson` = (4·D(h/2) − D(h))/3 with D(h) = [r(h,h) − r(h,−h) − r(−h,h) + r(−h,−h)]/(4h²), h = 0.02, computed on the same ODF reading as your quadratic form (an O(h⁴)-accurate estimate of the cross coefficient, independent of the 5 × 5 fit basis). The 7-term quadform of A-2.3 stays as specified and is compared as specified; **where the schema's cubic-null rows (κ₂₂, κ₂₄ ≤ 10⁻¹⁰ on cubic keys) miss on a 7-term fit, they are pre-classified definitional** (fit-basis resolution), for S9.
- **A-3.3 The cubic two-parameter reading.** State, as a CC-DD item, which reading you take for the cubic (t₂, t₄) form: (i) the inherited descriptor-axis P₂ (G-MSCS1's cubic l = 2, as A-2.2 defines the l = 2 family) or (ii) the O_h-symmetrized l = 2 term (identically zero on cubic, so the form reduces to κ₄₄t₄²). Both are admissible under A-2.3's wording; the comparison classifies accordingly.
- **A-3.4 Under LITERAL-A29** none of the above is in force: implement A-2.9 as written, report what happens (a failing control → INDETERMINATE per the schema rule), and the S9 process handles it.

## 1. Embed inventory

| Embed | md5 | Size | Handling |
|---|---|---|---|
| `staging_memo_G_MSCS2_v2.md` | `efdcabdcd937cda4acb64f941dc4bb2b` | 46,053 B | plain |
| `G_MSCS2_LOCK_RECORD.md` | `49232d4c42061c4536867eba14aae501` | 11,804 B | plain |
| `g_mscs2_schema_v1_0.json` | `66f586d7b6c5e8228394222ddfda73f2` | 5,800 B | plain |
| `g_mscs2_compare_v1_0.py` | `80d3b9078788fb17f57945da7d9c2c96` | 17,376 B | plain |
| `tools/t1/T1_forbidden_G_MSCS2.txt` | `be921b8c29f7578e85ed92f1450c1956` | 1,695 B | T1 list (scan-exempt) |
| `tools/t1/T1_base_author_20260919.txt` | `05302210cc4ceb70553acbe8379e9fc3` | 143 B | T1 list (scan-exempt) |
| `tools/t1/t1_scan.py` | `6b86290090a8c84f1b1a0a99ec0bf697` | 1,967 B | plain |
| `inputs/poly_vrh_results.json` | `200e7a8b775577564369c6924d38a84c` | 2,767 B | plain |
| `inputs/g_mscs1_chatleg_checkpoint.json` | `c04c0b8ea34cfe60f231aa06828e6ce4` | 33,289 B | plain |
| `inputs/g_mscs1_ccleg_checkpoint.json` | `249e11dd53c4cb82f302b15d3c94c337` | 24,415 B | plain |
| `g_mscs2_chatleg.py` | `f277580ddf0b4da9734d11edb009c54b` | 42,448 B | QUARANTINED (base64) |
| `g_mscs2_chatleg_checkpoint.json` | `1c5b6b59829d2a6b9ae2b1a7a016832d` | 31,575 B | QUARANTINED (base64) |
| `g_mscs2_chatleg_phase0_checkpoint.json` | `9e5a6e8ba0804bda778e4be52fbe2fde` | 7,747 B | QUARANTINED (base64) |
| `g_mscs2_chatleg_compare.json` | `7a9e170462cdbd92b8a4fa0b62307986` | 3,301 B | QUARANTINED (base64) |
| `g_mscs2_chatleg_selfcompare.json` | `0a10623660c8fbaed4c37ec388978593` | 65,952 B | QUARANTINED (base64) |
| `run_chatleg.log` | `e2940623b9e7035ffc29ac796280ecda` | 3,156 B | QUARANTINED (base64) |
| `run_phase0.log` | `72d64aebe9eb754e7e443bb36e63969e` | 1,681 B | QUARANTINED (base64) |
| `G_MSCS2_CHATLEG_EXECUTION_REPORT.md` | `ae032ab9d585b842cfd57410e7380d08` | 16,045 B | QUARANTINED (base64) |
| `G_MSCS2_PHASE0_EXECUTION_REPORT.md` | `b6a966920a34552e0f0e2dd91f2e969f` | 8,207 B | QUARANTINED (base64) |
| `diag_kappa24.py` | `9c53fa2f1715c499dec0bef143c503b0` | 2,323 B | QUARANTINED (base64) |
| `diag_kappa24.json` | `b7952dfcaddcd1d98e424aee8ce5231f` | 1,917 B | QUARANTINED (base64) |
| `diag_quadform_basis.json` | `d84aa1fdce7dea1b1a5d24dfb8f13c18` | 1,119 B | QUARANTINED (base64) |

## 2. Verify-then-build

Save this file as `dispatch.md` in a fresh `gmscs2_gate/` directory (branch from the current `main`), then run the extractor below **without** `--decode-quarantined` (it recreates `tools/t1/` and `inputs/`):

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

Expected: **ten `OK` lines and twelve `SKIP` lines.** Any assertion failure → HALT, report the md5 seen, do not build. Then: `python3 tools/t1/t1_scan.py tools/t1/T1_forbidden_G_MSCS2.txt staging_memo_G_MSCS2_v2.md G_MSCS2_LOCK_RECORD.md` → CLEAN; `python3 g_mscs2_compare_v1_0.py selftest` → SELFTEST PASS (18/18; this also proves the schema md5 you hold is the frozen one).

## 3. Build and run (blind)

1. Instrument `g_mscs2_ccleg.py`: md5-guards the memo (md5 + bytes), the T1 list, the scanner, X-1 (md5 + bytes) and both X-6 files; T1-scans itself and the memo at every invocation; halts on any hit; no override flag. Encode A-2.1–A-2.10 (and A-3 if flagged): the eight keys; the K̃₄ / P₄ / (t₂, t₄) families with the stated normalizations and positivity ranges; the 12-point t₄-grid and the 5 × 5 grid; Voigt/Reuss/Hill and Walpole-HS with references optimized at t = 0 and reused; the descriptors and the marginal weights (c_⟨001⟩ = 1, c_⟨111⟩ = −2/3); the exact closed forms (F-CTRL-C4); the fits with the 0.25 / 0.1 windows and the absolute-floor halving; `biref_b1_VRH` by the symmetric difference at ±0.05; the X-6 continuity pins read from the chat checkpoint at run time with the CC checkpoint as cross-check.
2. Phase 0 (13 items; halt-on-fail → INDETERMINATE) → Phase 2 → Phase 3 (verdict last, by the schema rule) → write `g_mscs2_ccleg_checkpoint.json` (schema v1.0 keys; floats at full precision; arrays in grid order; `extras` for anything beyond the schema — the A-3 diagnostics go there or under the keys named above).
3. **Commit** the instrument + checkpoint (+ run log) as the pre-consultation checkpoint, quoting the checkpoint md5 in the commit message. Only then:
4. Decode the quarantine (`--decode-quarantined`), run `python3 g_mscs2_compare_v1_0.py compare g_mscs2_chatleg_checkpoint.json g_mscs2_ccleg_checkpoint.json --out g_mscs2_twoleg_comparison.json`, then the chat-vs-chat re-run (must be byte-identical to the quarantined `g_mscs2_chatleg_selfcompare.json`) and a CC-vs-CC sanity. Classify every miss (definitional / representational / substantive) against the chat report §7 and your own H/CC-DD items; edit neither checkpoint.
5. Your hypothesis compare (the memo §6 HYP-MS2-1..5 against your checkpoint) as a separate artifact, last.

## 4. Return (single file, in-band, mirrored)

`G_MSCS2_CC_RETURN_INBAND.md`: branch + commits (pre-consultation first); the activation flag line you received, verbatim; instrument and execution summary (method variations executed; run time); Phase-0 table; Phase-2 coefficients per key; the verdict class; the two-leg comparison summary with every miss classified; CC-DD items (incl. A-3.3's reading); H-CC items (disagreements with memo / lock record / schema, self-caught bugs); deviations; T1 state; the A-3 diagnostics if in force. Embeds (sentinel format of this dispatch, byte-exact): your instrument, your checkpoint, the two-leg comparison, your chat-vs-chat re-run, your CC-vs-CC sanity, your hypothesis compare. Scan the return before committing. Per the gate convention the chat-side fold estate lands later in `gmscs2_gate/estate/` by a successor PR; do not commit any canonical ledger.

## 5. Repository note (recorded as observed by the chat leg at 15:50 UTC, September 26)

`main` = `d0a0e31` (the PR #13 merge); `gmscs1_gate/estate/` absent on every branch; `SQT_Master_Ledger_v4_79_CANONICAL.md` at the repository root; no PR #27 in `main`'s history (PR #26 is the g2aa1 fold-side estate). The HK-1 dispatch `36b8bd61` (September 23) remains the instrument for those two PRs; nothing in this leg depends on them. Branch this leg from whatever `main` is when you start and say which.

## 6. Embeds

=====BEGIN-EMBED name=staging_memo_G_MSCS2_v2.md md5=efdcabdcd937cda4acb64f941dc4bb2b bytes=46053 encoding=raw=====
# STAGING MEMO — Gate G-MSCS2 (Multi-Species Channel Speed, the l = 4 / cubic-effective texture family — the E-MS-5 registered successor of G-MSCS1) — v2

**Date:** September 26, 2026 (v2; draft v1 September 23, md5 055a0010ebf0ab4df595ea07684973b2, superseded — see §A). **Base:** `SQT_Master_Ledger_v4_84_CANONICAL.md` (md5 `f36bbdb04104008783f2763f70fb916f`, 1,637,662 B; active in project knowledge, byte-verified). **Status: LOCKED September 26, 2026 — author-authorized (directive of September 26, 2026: elections E-MS2-1..8 confirmed, lock explicitly authorized); this file is frozen at its md5 (recorded in the lock record); the T1 list is pinned; schema v1.0 + comparator v1.0 are frozen before any emission.** **Lineage:** §2.91.I Q3 item (1) → ANNEX-CDEF-1 → G-TSH4 (§2.91.L) → G-POLY1 (§2.91.M) → G-CI1 (§2.91.N) → G-S2C1 / G-S2C1-W (§2.91.O) → **G-MSCS1 (§2.91.Q, V4.83)** → its E-MS-5 registered successor arm, "the l = 4 (cubic-effective) texture family".

**Gate ID: G-MSCS2** (Q-MS2-1 — confirmed by the author's election set of September 26, which adopts the draft's identifiers). Everything G-MSCS1 settled is consumed here as banked; nothing is re-litigated; the descriptors, the configurations, the aggregate machinery and the tolerances are inherited unchanged (E-MS-1(a), E-MS-2, E-MS-2b, E-MS-2c, the A-2 operationalizations), so that the one new thing — the texture family — is the only thing the two legs can disagree about.

## A. v1 → v2 record (the author's elections applied; three chat-side sharpenings, all pre-lock and pre-instrument)

- **A-2.1 Elections applied (author, September 26, 2026).** E-MS2-1 (a)+(b); E-MS2-2 (a); E-MS2-2b (a)+(b); E-MS2-2c ⟨001⟩ primary / ⟨111⟩ reported; E-MS2-3 (a) leading order only, no Born; E-MS2-4 (a) Danielewski carried; E-MS2-5 (a) K̃₄ normalization as proposed; E-MS2-6 (a) no observational contact; E-MS2-7 base list `05302210` + the G-MSCS1 stratum; E-MS2-8 (a) X-6 continuity pins. Q-MS2-1..4 answered by the same set (gate ID G-MSCS2; the hex second arm included; the K̃₄ normalization; no Born). All T3-immutable from this lock.
- **A-2.2 The exact closed forms behind F-CTRL-C4 and F-CTRL-MARG (chat-side, sympy-exact, disclosed; §2.6).** Writing the cubic single-crystal tensor as C = λ δδ + μ(δδ + δδ) + H·Σ_a ê_a⊗ê_a⊗ê_a⊗ê_a with H = C₁₁ − C₁₂ − 2C₄₄ (the Zener combination), the Voigt average under the K̃₄ family is **⟨C⟩_V(t₄) = ⟨C⟩_V(0) + t₄·(H/3)·𝒯⁴(ẑ)**, where 𝒯⁴(ẑ) is the l = 4 (traceless, fully symmetric) part of ẑ⊗ẑ⊗ẑ⊗ẑ: in Voigt notation ΔC₁₁ = ΔC₂₂ = 3Ht₄/105, ΔC₃₃ = 8Ht₄/105, ΔC₁₂ = Ht₄/105, ΔC₁₃ = ΔC₂₃ = −4Ht₄/105, ΔC₄₄ = ΔC₅₅ = −4Ht₄/105, ΔC₆₆ = Ht₄/105 (transversely isotropic: ΔC₆₆ = (ΔC₁₁ − ΔC₁₂)/2 exactly). The prefactor is 2.5·|A₄|²/9 with |A₄|² = 3 − 9/5 = 6/5. The Reuss average obeys the same law on the compliance with H_S = S₁₁ − S₁₂ − S₄₄/2. The ODF average of the per-grain E₂ weight reduces exactly to an S² average of the weight over the descriptor axis n̂ with the **marginal fiber weight 1 + c·t₄·P₄(n̂·ẑ), c_⟨001⟩ = 1, c_⟨111⟩ = −2/3** (the rotation about the descriptor axis averaged analytically; the hex P₄ family has c = 1 by definition). Normalizations: ⟨K̃₄²⟩_S² = 4/21 (so the orthonormal cubic harmonic is K̃₄·√21/2) and ⟨P₄²⟩ = 1/9 (so P₄^orth = 3P₄) — the conversions to Roe's W₄₀₀ / Bunge's C₄¹¹ carry those authors' own normalizations and are read from the sources (§12 L-MS2-1), never load-bearing. These forms turn two controls from "rational coefficients pinned in the lock record" into explicit identities the instruments assert.
- **A-2.3 Verdict rule made explicit (§1).** L4-NULL is assigned iff, on both fcc configurations for the primary descriptor (⟨001⟩), |κ₄₄(S2-E₂)| ≤ the absolute floor 1×10⁻⁶ two-leg while F-CTRL-C4 passes (the aggregate tensor moves at O(t₄)); PROTECTION-BREACH takes precedence over L4-NULL; INDETERMINATE over both. The birefringence reporting quantity is defined (§4 Phase 2): for the textured cubic aggregate, b₁ = d/dt₄ [(v_qSH − v_qSV)/v_T] at t₄ = 0 for propagation perpendicular to the fiber axis, by symmetric difference at t₄ = ±0.05 on Hill (for the Voigt tensor it equals H/(42 μ_V) exactly — an in-instrument check, not a schema key).
- **A-2.4 Housekeeping discrepancy recorded (§10).** The author's directive of September 26 states the HK-1 PRs merged, with the PR numbers left as placeholders; the live remote at lock time shows neither merge. Recorded as observed; the fold carries the numbers.
- **A-2.5 T1 list composed and pinned (§11); LSF-δ executed (§12); the draft's one numeric-rendering collision (a machine-precision residual written in a forbidden digit form) reworded before v1 delivery — the v1 md5 above is the delivered, CLEAN file.**

## 0. What the ledger has already settled (this gate does not re-litigate any of it)

- **G-MSCS1 (§2.91.Q; two-leg, IDENTITY-DELIVERED; S9 (a); V4.83):** under CI-W/EM-IN and the E₂-content identification, EM and S2 are two *descriptors* of the one transverse phonon; their speed equality is an SO(3) identity on the untextured aggregate (the ODF-averaged E₂ weight is the mode-independent constant 2/5); **first-order protection** in an l = 2 fiber texture holds on every configuration (|S_t| ≤ 4.9×10⁻¹³, both legs); the split is second order — the delivered constraint curve r_agg(t) ≈ κ₂t² with **κ₂(S2-E₂) = −1.43946×10⁻³ (hex_step|a) / −1.43870×10⁻³ (|b) / −1.89565×10⁻³ (hex_gem8|a) / −1.89614×10⁻³ (|b) under Hill** (HS-mean within 0.8%); κ₂(S2-h) = −2.0 / −2.0 / −3.2 / −3.3 ×10⁻⁶.
- **The cubic l = 2 texture null (structural; both legs independently):** a cubic grain carries no l = 2 texture coefficient — the l = 2 harmonic summed over the octahedral orbit of the grain axis vanishes (Σ_i P₂(ê_i·ẑ) = 0 for an orthonormal triad), so ⟨C⟩_t = ⟨C⟩_0 to 10⁻¹² and every species quantity is zero on the fcc branch at every t in that family; the cubic clauses of H-MS-3 / H-MS-5 were refuted by symmetry; **"the first cubic texture effect is l = 4" — E-MS-5's registered successor arm. This gate is that arm.**
- **Single-crystal descriptor splits (banked, re-pinned here, not re-derived):** r_xtal(S2-E₂) = −2.7967×10⁻² (hex_step|a) / −2.7947×10⁻² (|b) / −3.9339×10⁻² (hex_gem8|a) / −3.9352×10⁻² (|b) / −1.7297×10⁻² (cubic_step|⟨001⟩) / +1.1531×10⁻² (|⟨111⟩) / −2.0842×10⁻² (cubic_gem8|⟨001⟩) / +1.3895×10⁻² (|⟨111⟩); r_xtal(S2-h) = −1.113 / −1.113 / −1.315 / −1.315 / −1.516 / −1.516 / −1.845 / −1.845 ×10⁻³; ⟨λ_L⟩ = 4.81 / 4.81 / 4.95 / 4.95 / 8.39 / 8.39 / 9.31 / 9.31 ×10⁻³, max λ_L = 3.35 / 3.35 / 3.51 / 3.51 / 3.87 / 3.87 / 4.33 / 4.33 ×10⁻² on qSV (hex) / qT2 (cubic); v_T(Hill, t = 0) = 8.41906 / 8.41928 / 10.04172 / 10.04155 / 7.79905 / 7.79905 / 9.30790 / 9.30790 (substrate units; the eight configuration/arm keys in the G-MSCS1 order). On a cubic lattice the descriptor axis is a genuine choice (recorded, not resolved): the E₂ split changes sign between ⟨001⟩ and ⟨111⟩.
- **The admixture structure (H-CC-1/H-CC-2, V4.83):** the S2-h split is admixture-sourced and dominated by the quasi-longitudinal EM-weight tail (0.5–0.9%), the covariance identity a 28–34% estimate; the Danielewski differentiation obligation discharged as far as a gate can. **Nothing in §3 of G-MSCS1 is reopened here** (E-MS2-4).
- **The kill surface for the single-species claim is outside any gate of this family** (G-MSCS1 §5): E-MS-1(b); the value of the texture import (the untextured ODF is an M.ONT import, G-POLY1 E3); a sealed-anchor comparison (E-MS-6(b), declined). This gate, like its predecessor, is a **delivery gate**.

**Consequence that frames this gate.** G-MSCS1 delivered the texture constraint curve for the hex stacking branch and found the fcc branch *blind* to l = 2 texture by symmetry. The constraint surface is therefore incomplete on exactly the branch where the substrate's own point group makes the first texture harmonic l = 4 — and l = 4 is also where the rank-4 elasticity of *any* grain stops seeing the ODF at all. Two exact facts organize the gate: **(i)** a rank-4 tensor averaged over an ODF depends on the ODF only through its l ≤ 4 coefficients (Man–Huang representation theorem; textbook Bunge/Roe), and the per-grain E₂ weight is a degree-4 polynomial in the grain axis, so **the (t₂, t₄) fiber family is the *general* axisymmetric weak texture for every observable of this gate** — an l ≥ 6 term changes nothing (an identity, encoded as control F-CTRL-L4EXHAUST); **(ii)** for cubic grains the l = 2 term is null, so the texture dependence of the fcc branch is the l = 4 term *alone* — "cubic-effective". The gate delivers the missing fcc constraint curve κ₄₄, the hex l = 4 curve, and (second arm) the hex cross-coefficient κ₂₄ that completes the quadratic form of the general weak fiber texture.

## 1. Object

**Question (one sentence):** in the instantiated substrate's SO(3) aggregate under the l = 4 fiber families — the cubic harmonic family 1 + t₄·K̃₄ on the two fcc configurations and the Legendre family 1 + t₄·P₄ on the two hex configurations, with the hex two-parameter family 1 + t₂·P₂ + t₄·P₄ as the second arm — does first-order protection of species universality hold as it did for l = 2, and what are the quadratic coefficients κ₄₄ (and κ₂₄) that complete the texture constraint surface, in particular the first non-zero curve on the fcc branch?

**Verdict classes (pre-registered; one is assigned by the machine, last):**
- **IDENTITY-DELIVERED-L4** — all Phase-0 controls and pins pass (the SO(3) identity at t = 0; the continuity pins to G-MSCS1; the exhaustion and cubic-null identities; first-order protection S_{t₄} = 0); κ₄₄ per configuration (both S2 arms), λ_L(t₄), and (second arm) the hex quadratic form (κ₂₂, κ₂₄, κ₄₄) are delivered two-leg. The texture constraint surface is COMPLETED to the general axisymmetric weak texture for all four configurations — R2, conditional on the imports in §7. Expected class.
- **PROTECTION-BREACH** — first-order protection fails in an l = 4 family (F-MS2-3 fires two-leg); an S9 item first, a structural finding second; the R2 reading is not delivered.
- **L4-NULL** — |κ₄₄(S2-E₂)| ≤ the absolute floor 1×10⁻⁶ on both fcc configurations for the primary descriptor (⟨001⟩), two-leg, while F-CTRL-C4 passes (the aggregate tensor moves at O(t₄)) (F-MS2-4): the descriptor pair is blind to the fcc branch's texture at second order — a structural finding (registered successor: the third-order term), not a kill. Precedence: INDETERMINATE > PROTECTION-BREACH > L4-NULL > IDENTITY-DELIVERED-L4.
- **INDETERMINATE** — a Phase-0 control or pin fails; no verdict.

## 2. Analytical frame (definitions the instrument encodes; nothing else is computed)

**2.1 Field, inputs, machinery — inherited.** Christoffel on the banked tensors of `poly_vrh_results.json` (X-1, md5 `200e7a8b`), sampled over the k̂-sphere with the pinned quadrature; textured Voigt / Reuss / Hill by exact SO(3) product quadrature of the ODF-weighted grain average; Walpole-form Hashin–Shtrikman with the isotropic references optimized at t = 0 and **reused at every t** (the G-MSCS1 A-2.3 operationalization — which is also what makes HS depend on the ODF only through l ≤ 4, §2.6). No second-order Born is computed in this gate (E-MS2-3; Q-MS2-4). Substrate units; every reported quantity a ratio.

**2.2–2.4 Descriptors and grain scale — inherited verbatim from G-MSCS1 §2.2–§2.4 (E-MS-1(a)):** w_EM = 1 − λ_L; S2-E₂ = the m = ±2 fraction of the transverse-projected strain about the grain's elected axis (hex: the c-axis; cubic: ⟨001⟩ primary, ⟨111⟩ reported), ODF-averaged at the grain scale; S2-h = (1 − λ_L)/(1 + λ_L/3). At t = 0 the ODF-averaged E₂ weight is 2/5 for every mode (the SO(3) identity; control, never a result). **One clarification, stated not re-elected:** on a cubic lattice the elected single-axis descriptor, averaged against an O_h-invariant ODF, is *identically* its octahedral-orbit average (∫ f(g) w(g) dg = ∫ f̄(g) w(g) dg when w(gh) = w(g) for h ∈ O_h) — so the ⟨001⟩ descriptor is the three-axis E₂ content and the ⟨111⟩ descriptor the four-diagonal E₂ content; the G-MSCS1 numbers already are that (the untextured ODF is O_h-invariant), and the l = 4 families below are O_h-invariant by construction.

**2.5 The l = 4 fiber families (the one new definition).** Let ẑ be the fiber axis (sample frame) and, for a grain of orientation g, let ẑ_c = g⁻¹ẑ be the fiber axis in the crystal frame with components (x, y, z).
- **Cubic (fcc branch):** the normalized l = 4 cubic harmonic **K̃₄(g) = (5/2)·(x⁴ + y⁴ + z⁴ − 3/5)**, O_h-invariant, sphere-mean zero, **K̃₄ = 1 when a cube axis is along the fiber and K̃₄ = −2/3 when a body diagonal is** (x⁴ + y⁴ + z⁴ ranges over [1/3, 1] on the sphere). ODF **w = 1 + t₄·K̃₄**, positivity **t₄ ∈ [−1, 3/2]**; t₄ > 0 is ⟨001⟩-aligned fiber, t₄ < 0 is ⟨111⟩-aligned. (Normalization election E-MS2-5; the conversion to the Bunge C₄¹¹ / Roe W₄₀₀ conventions is a fixed rational factor, stated in the lock record for the literature comparison of §3 — never load-bearing.)
- **Hex (hcp branch):** **w = 1 + t₄·P₄(cos θ)**, θ the angle between the grain's c-axis and the fiber; P₄ ∈ [−3/7, 1] (the minimum at cos²θ = 3/7), positivity **t₄ ∈ [−1, 7/3]**.
- **Hex second arm (E-MS2-1(b)):** **w = 1 + t₂·P₂ + t₄·P₄**, the general axisymmetric weak texture to the order elasticity sees; the instrument asserts positivity on its SO(3) grid at every (t₂, t₄) it uses (F-CTRL-POS) — the fit window |t₂|, |t₄| ≤ 0.25 lies inside the positivity region since |t₂P₂ + t₄P₄| ≤ ½ there.
- **Speeds and the fit — inherited form:** r_agg(t₄) = ⟨v⟩_S2(t₄)/⟨v⟩_EM(t₄) − 1 on the pinned 12-point t₄-grid, both S2 arms, VRH and HS at each t₄; the fit **r_agg(t₄) = S₄·t₄ + κ₄₄·t₄² + κ₄₄₄·t₄³ over |t₄| ≤ 0.25** with the A-2.4 step-halving convergence (relative tolerance carrying an absolute floor — the V4.83 process note). **First-order protection (algebraic, confirmed by the machine): S₄ = 0** — the same degenerate-perturbation argument as at l = 2: at t₄ = 0 the speeds are degenerate across polarization and the ODF-averaged weight is mode-independent; both perturb at O(t₄); their covariance, which r_agg measures, is O(t₄²). **κ₄₄ is the gate's quantitative product: the constraint curve r_agg(t₄) ≈ κ₄₄·t₄² on the l = 4 departure of the texture import — the first non-zero curve on the fcc branch.** Second arm: the quadratic form **r_agg(t₂, t₄) ≈ κ₂₂·t₂² + κ₂₄·t₂t₄ + κ₄₄·t₄²** fitted on a 5 × 5 grid |t₂|, |t₄| ≤ 0.25 with the cubic terms included in the fit and discarded; **κ₂₂ must reproduce G-MSCS1's κ₂** (PIN-K2, the continuity pin); on cubic **κ₂₂ = κ₂₄ = 0 identically** (the l = 2 null; control F-CTRL-L2NULL). λ_L(t₄) sphere-mean as in G-MSCS1 §2.6 (O(t₄²)).

**2.6 Two identities that define "cubic-effective" and "complete" (controls, never results).** **(i) Exhaustion:** the ODF average of a rotated rank-4 tensor depends on the ODF only through its l ≤ 4 coefficients — the rotated components are matrix elements of the l ≤ 4 representations; the per-grain E₂ weight is a degree-4 polynomial in the grain axis; the Walpole-HS average with references fixed at t = 0 is an ODF average of a rotated rank-4 tensor. Hence **every observable of this gate is invariant under any l ≥ 6 fiber term** — encoded as F-CTRL-L4EXHAUST: adding t₆·P₆ (hex) or the l = 6 cubic harmonic (cubic) at t₆ = 0.3 changes ⟨C⟩_Voigt, ⟨S⟩_Reuss, C_HS and r_agg by ≤ 10⁻¹². **(ii) Affinity and the Zener content:** ⟨C⟩(t₄) = ⟨C⟩₀ + t₄·C₄ *exactly* (the Voigt/Reuss averages are linear in the ODF), with **C₄ proportional to the Zener combination H = C₁₁ − C₁₂ − 2C₄₄ of the single-crystal tensor with rational coefficients** (an isotropic tensor, H = 0, has no l = 4 effect) — encoded as F-CTRL-C4: the lock record pins the rational coefficients; the textured cubic aggregate is a five-constant transversely isotropic medium at every t₄, its two transverse speeds split at O(t₄). *Chat-side pre-draft check (disclosed, not a gate result; §13): on a generic cubic tensor with a degree-12-exact SO(3) product quadrature — the l = 2 null 7×10⁻¹⁴, the l = 6 exhaustion 3×10⁻¹⁴, affinity in t₄ 7×10⁻¹⁴, the H = 0 tensor's l = 4 effect below 10⁻¹⁴; the E₂ weight's P₆ and P₈ moments 10⁻¹⁶ against non-zero P₂ and P₄ moments. The frame is not vacuous and its identities hold to machine precision.* **Exact closed forms (A-2.2; the instruments assert them):** ⟨C⟩_V(t₄) = ⟨C⟩_V(0) + t₄·(H/3)·𝒯⁴(ẑ), Voigt entries ΔC₁₁ = ΔC₂₂ = 3Ht₄/105, ΔC₃₃ = 8Ht₄/105, ΔC₁₂ = Ht₄/105, ΔC₁₃ = ΔC₂₃ = ΔC₄₄ = ΔC₅₅ = −4Ht₄/105, ΔC₆₆ = Ht₄/105, with H = C₁₁ − C₁₂ − 2C₄₄; the same law on the compliance for Reuss with H_S = S₁₁ − S₁₂ − S₄₄/2; the descriptor-weight ODF average = the S² average over the descriptor axis with the marginal weight 1 + c·t₄·P₄(n̂·ẑ), c_⟨001⟩ = 1, c_⟨111⟩ = −2/3; ⟨K̃₄²⟩ = 4/21, ⟨P₄²⟩ = 1/9.

## 3. LSF-δ obligations (executed at v2 — the sweep, sources and ceilings are §12)

Clusters and what each must establish or attribute; the §3.2-style table is not needed (the Danielewski obligation was discharged at G-MSCS1 and nothing here reopens it — E-MS2-4):
- **L-MS2-1 ODF harmonics and crystal symmetry.** Bunge, *Texture Analysis in Materials Science* (1982); Roe, J. Appl. Phys. 36, 2024 (1965): the symmetrized-harmonic expansion, the absence of l = 2 terms for cubic crystal symmetry, the l = 4 cubic harmonic, the axisymmetric (fiber) special case; positivity of truncated expansions. *Prior art for §2.5's families and the cubic null; attribution.*
- **L-MS2-2 Elasticity sees l ≤ 4; cubic aggregates see l = 4 only.** Man–Huang, J. Elasticity 105, 1 (2011) (the representation theorem; carried from G-MSCS1 cluster 2); Sayers, J. Phys. D 15, 2157 (1982) (ultrasonic velocities in textured cubic aggregates depend on the ODF through the l = 4 coefficients W₄₀₀, W₄₂₀, W₄₄₀ — the fiber case through W₄₀₀ alone); Morris (Int. J. Eng. Sci. 1969/1970, the Voigt–Reuss–Hill averages of textured cubic aggregates); Kocks–Tomé–Wenk, *Texture and Anisotropy* (1998). *Prior art for both identities of §2.6 — the gate's "cubic-effective" and "complete" are textbook facts about rank-4 averaging, claimed here only as applied to the descriptor pair.*
- **L-MS2-3 Bounds for textured polycrystals.** Walpole (J. Mech. Phys. Solids 1966; 1981); Willis; the HS-for-textured-aggregates literature (e.g. Man and co-workers on bounds for weakly textured cubic polycrystals). *Grounds the A-2.3 fixed-reference HS operationalization for t₄ ≠ 0 and its l ≤ 4 dependence.*
- **L-MS2-4 Ultrasonic texture measurement in fiber-textured cubic metals.** Thompson, Lee, Smith (J. Acoust. Soc. Am. 1986/1987), Hirao–Ogi (*EMATs for Science and Industry*, 2003): shear-wave birefringence and velocity anisotropy as a measurement of W₄₀₀ in cubic polycrystals. *The closest prior art to "a species split controlled by the l = 4 coefficient"; the differentiator is that G-MSCS2's observable is a descriptor split (two weightings of one phonon), not the birefringence of two polarizations — the birefringence is O(t₄), the descriptor split O(t₄²).*
- **L-MS2-5 The textured SOA (second-order) machinery.** Acoustics 2(1), 5 (2020) (carried): the anisotropic-reference Green function — the registered t ≠ 0 Born successor's machinery; not executed here (E-MS2-3).
- **L-MS2-6 The Danielewski / rotational-ether lane and the emergent-species literature.** Carried from G-MSCS1 §3 and §12 clusters 1 and 3 (Anber–Donoghue; Bednik–Pujolàs–Sibiryakov; Chadha–Nielsen; Collins et al.; Danielewski 2007/2020/2023; MacCullagh → Kelvin → Kleinert): nothing new is claimed against them; re-cited, not re-read, unless the sweep surfaces new texture-related content.
- **L-MS2-7 Collision check.** Expected verdict, to be verified at the sweep: no located prior claim computes an EM/spin-2 *descriptor* split as a function of l = 4 vacuum texture in an elastic-vacuum model; **novel-in-assembly; A0 not triggered.** Honest ceiling, pre-declared: every ingredient (l ≤ 4 exhaustion, the cubic l = 2 null, first-order degenerate-perturbation protection) is elementary or textbook; the novelty is the assembly and the delivered coefficients.

## 4. Execution leg

**Phase 0 — pins and controls (halt-on-fail).** X-1 byte-verified (`200e7a8b`). **Continuity pins to G-MSCS1 (the new machinery must reproduce the banked curve before it computes a new one):** **PIN-XTAL** — r_xtal (both arms, all eight keys), ⟨λ_L⟩ and max λ_L reproduce the G-MSCS1 checkpoint of record (X-6) to ≤ 1×10⁻⁸; **PIN-VRH0 / PIN-HS0** — v_T(t = 0) reproduces to ≤ 1×10⁻⁸; **PIN-K2** — with the l = 2 family switched on (t₄ = 0) the fitted κ₂(S2-E₂) reproduces the banked −1.43946 / −1.43870 / −1.89565 / −1.89614 ×10⁻³ (Hill) to ≤ 1×10⁻⁴ relative, and the cubic l = 2 null to ≤ 10⁻¹² — this pin is what makes G-MSCS2's κ₄₄ comparable to G-MSCS1's κ₂. **Controls:** **F-CTRL-ISO** — an isotropic tensor gives r_agg(t₄) = 0 ∀t₄, both families, machine precision; **F-CTRL-SO3** — the ODF-averaged S2-E₂ weight at t₄ = 0 is 2/5 for every mode; **F-CTRL-POS** — every ODF used is ≥ 0 on the SO(3) grid; **F-CTRL-L2NULL** — on both cubic configurations, t₂ ≠ 0 (alone and jointly with t₄) changes ⟨C⟩, the weights and r_agg by ≤ 10⁻¹² (κ₂₂ = κ₂₄ = 0); **F-CTRL-L4EXHAUST** — an l = 6 fiber term at t₆ = 0.3 changes ⟨C⟩_Voigt, ⟨S⟩_Reuss, C_HS and r_agg by ≤ 10⁻¹² on every configuration and family; **F-CTRL-C4** — ⟨C⟩_V(t₄) − ⟨C⟩_V(0) is affine in t₄ to 10⁻¹² and equals t₄·(H/3)·𝒯⁴(ẑ) (the A-2.2 Voigt entries) on both cubic configurations to 10⁻¹² relative to |C|; a synthetic H = 0 tensor gives zero; **F-CTRL-MARG** — the SO(3)-direct ODF average of the per-grain E₂ weight (the K̃₄ weight on the full orientation) equals its S²-marginal form (1 + c·t₄·P₄ over the descriptor axis; c = 1 for ⟨001⟩, −2/3 for ⟨111⟩) to 10⁻¹² on every mode; **F-CTRL-TEX4** — a synthetic strongly anisotropic cubic tensor at t₄ = 1 gives |r_agg| ≫ τ_agg (the instrument can see an l = 4 split); **F-CTRL-QUAD** — SO(3) product quadrature exact to degree ≥ 12 with doubling ≤ 1×10⁻¹⁰. Any control or pin failure → INDETERMINATE.

**Phase 1 — lattice scale.** Nothing new is derived; the Phase-1 quantities are recomputed only as PIN-XTAL inputs (they are G-MSCS1's).

**Phase 2 — aggregate sweeps (leading order; VRH and HS at each point).** (i) **Cubic l = 4 family:** r_agg(t₄) on the 12-point grid for S2-E₂ (⟨001⟩ primary, ⟨111⟩ reported) and S2-h; S₄, κ₄₄, κ₄₄₄ with halving; λ_L(t₄); the two transverse aggregate speeds v_qSH(t₄), v_qSV(t₄) along the pinned k̂ set and their O(t₄) split coefficient (the birefringence, reported for the L-MS2-4 differentiator — not a species quantity). (ii) **Hex l = 4 family:** the same, hex arms (a) and (b). (iii) **Hex two-parameter family (second arm):** the quadratic form (κ₂₂, κ₂₄, κ₄₄) on the 5 × 5 grid, with κ₂₂ checked against PIN-K2; on cubic the form reduces to κ₄₄ alone (F-CTRL-L2NULL).

**Phase 3 — comparison, last (Eddington quarantine).** Verdict class from the Phase-0/2 states; the pre-registered hypotheses (§6) compared in a separate artifact; no observational number anywhere.

**Instrument encoding.** k̂-sphere quadrature as G-MSCS1 (GL(cos θ) 64 × uniform φ 128, doubling ≤ 1×10⁻¹⁰); SO(3) product quadrature exact to degree ≥ 12 for every ODF average (the integrands are polynomials of degree ≤ 8 in the rotation entries; the exhaustion control is only meaningful if the l = 6 term is integrated exactly); the 12-point t₄-grid and the 5 × 5 (t₂, t₄) grid, all tolerances, the K̃₄ normalization and its conversion factors, the pinned k̂ set for the birefringence, and the rational C₄ coefficients in the lock record; every verdict-bearing quantity a float with a declared tolerance or a boolean/label; free text never compared; **comparator v1.0 + schema v1.0 FROZEN BEFORE the chat leg emits**; the T1 gate list in-band, the instruments halt without it (§11); both legs from scratch, CC blind, with the requested method variation (CC: the SO(3) average by a different quadrature — e.g. a Lebedev/Gauss product of different orders, or the generalized-spherical-harmonic route computing the l = 4 coefficients analytically and contracting with the harmonic decomposition of C — so that the exhaustion and affinity identities are witnessed by two constructions).

**Tolerances (pre-registered; the G-MSCS1 set plus the V4.83 process note).** τ_agg = 1×10⁻⁶ absolute on r; two-leg ≤ 1×10⁻⁸ on Phase-1 means, r_xtal and the t = 0 pins; ≤ 1×10⁻⁶ on r_agg(t₄) and S₄; ≤ 1×10⁻⁴ relative on κ₄₄, κ₂₂, κ₂₄ **with an absolute floor 1×10⁻⁶** (a null coefficient compares as a null, never as 0/0 — the G-MSCS1 v1.1 lesson built in from the start); identities ≤ 10⁻¹².

## 5. Falsifiers, controls, and where the kill surface actually is

- **F-MS2-3 (first-order protection, l = 4):** |S₄| > τ_agg on any configuration, either S2 arm, either family, reproduced two-leg after S9 → PROTECTION-BREACH.
- **F-MS2-4 (the cubic-effective null):** |κ₄₄| ≤ the absolute floor on both fcc configurations two-leg while F-CTRL-C4 shows the aggregate tensor moving at O(t₄) → L4-NULL. A live structural falsifier of the M-naive expectation (not of any framework claim): it would mean the descriptor pair is blind to the fcc branch's texture at second order, and the fcc constraint curve is third-order or higher (registered successor). Treated as a bug first (S9), a finding second.
- **F-MS2-2 (gyrotropy) — REGISTERED, NOT EXECUTED** (carried from G-MSCS1: first-order spatial dispersion, absent at this order).
- **Not falsifiers:** κ₄₄ ≠ 0 (the expected, delivered curve); κ₂₄ ≠ 0 on hex (expected; the cross term of the general weak texture); a sign difference between κ₄₄(⟨001⟩) and κ₄₄(⟨111⟩) on cubic (a structural question, §6).
- **Where the kill surface for the single-species claim lies (unchanged from G-MSCS1 §5):** E-MS-1(b); the value of the texture import; a sealed-anchor comparison of the constraint surface against the 2017 multi-messenger tensor-speed bound (E-MS-6(b), declined for this gate). None of these is inside G-MSCS2. **What this gate adds to that surface:** with κ₄₄ delivered, the fcc branch — blind at l = 2 — acquires its first texture sensitivity, so a future sealed-anchor mini-gate would have a curve to compare on *both* stacking branches.

## 6. Hypotheses (M-naive expectations, registered pre-data — NOT verdicts)

- **H-MS2-1:** κ₄₄(S2-E₂) ≠ 0 on both fcc configurations, |κ₄₄| of order 10⁻³–10⁻² (the cubic transverse splitting, ~41%, exceeds hex's ~34%, and l = 4 is the cubic anisotropy's own harmonic); κ₄₄(S2-h) smaller by roughly the admixture factor.
- **H-MS2-2:** on cubic, sign κ₄₄(⟨001⟩ descriptor) = sign r_xtal(⟨001⟩) < 0 and sign κ₄₄(⟨111⟩ descriptor) = sign r_xtal(⟨111⟩) > 0 — the descriptor-axis sign flip of G-MSCS1 persists into the texture coefficient (not forced; a structural question the machine answers).
- **H-MS2-3:** S₄ = 0 within τ_agg on all four configurations, both arms, both families (first-order protection is family-independent).
- **H-MS2-4:** on hex, |κ₄₄| < |κ₂₂| (the l = 2 term dominates the hex response) and κ₂₄ ≠ 0 with |κ₂₄| between them; κ₂₂ reproduces G-MSCS1's κ₂ (a pin, not a hypothesis).
- **H-MS2-5:** the fcc birefringence coefficient (the O(t₄) qSH/qSV split) is of order the cubic anisotropy times t₄, i.e. 10⁻¹ per unit t₄ — two orders above the descriptor split at t₄ ~ 0.25: the descriptor split is a strictly second-order shadow of the birefringence (the L-MS2-4 differentiator quantified).
- **Expected class: IDENTITY-DELIVERED-L4.**

## 7. Pinned inputs and imports (named; none exercised beyond what is stated)

- **X-1** `poly_vrh_results.json` `200e7a8b775577564369c6924d38a84c` (2,767 B) — the four tensors (repo: `gpoly1_gate/`, `gci1_gate/embeds/`, `gs2c1_gate/p2_ccleg/`, `gmscs1_gate/inputs/`).
- **X-6 (new pin source): the G-MSCS1 checkpoints of record** — chat `g_mscs1_chatleg_checkpoint.json` `c04c0b8ea34cfe60f231aa06828e6ce4` (33,289 B; the pin values are read from it at run time, md5-guarded) with CC's `249e11dd53c4cb82f302b15d3c94c337` as the cross-check (both in `gmscs1_gate/` on `main`); the values pinned: r_xtal (8 keys × 2 arms), ⟨λ_L⟩, max λ_L, v_T(Hill/VRH/HS, t = 0), κ₂(S2-E₂) Hill and HS-mean, the cubic l = 2 null.
- **Reference implementations (read for method, not copied):** the G-MSCS1 instruments — chat `g_mscs1_chatleg.py` `db5f51dd` and CC `g_mscs1_ccleg.py` `195a2b1b` (`gmscs1_gate/`); the texture machinery generalizes by replacing the ODF weight function.
- **Imports inherited, unexercised:** the transverse scale (T4; no SI); the M.ONT polycrystal ontology; the untextured orientation distribution (G-POLY1 E3) — *this gate's l = 4 families are a sensitivity sweep on that import, not a claim about its value*; E-P2-1(a) as a kinematic statement; K = ∅; the V4.70 KNOB caveat (kernel-labelled throughout); the tetragonal-form hex tensors (E-MS-2b arms (a)/(b)).

## 8. Elections (author, September 26, 2026 — T3-immutable on lock)

- **E-MS2-1 (texture families): (a)** the l = 4 fiber families of §2.5 (cubic K̃₄; hex P₄) **+ (b)** the hex two-parameter (t₂, t₄) quadratic form as the second arm. *Recommended: (a)+(b) — (b) costs one more grid and completes the general weak fiber texture; the pin PIN-K2 rides on it.*
- **E-MS2-2 (configurations): (a)** all four. **E-MS2-2b (hex form):** (a) tetragonal-form primary + (b) symmetrized second arm (as G-MSCS1). **E-MS2-2c (cubic descriptor axis):** ⟨001⟩ primary, ⟨111⟩ reported (as G-MSCS1; with the §2.4 clarification that both are octahedral-orbit averages under an O_h-invariant ODF).
- **E-MS2-3 (aggregate order): (a)** leading order only — no Born; the t ≠ 0 SOA second-order successor stays registered. *Recommended (Q-MS2-4).*
- **E-MS2-4 (Danielewski): (a)** carried, not reopened; no new table.
- **E-MS2-5 (K₄ normalization): (a)** K̃₄ = (5/2)(x⁴ + y⁴ + z⁴ − 3/5), max 1 on a cube axis, positivity t₄ ∈ [−1, 3/2]; conversion factors to C₄¹¹ (Bunge) / W₄₀₀ (Roe) stated in the lock record. *Recommended: (a) — dimensionless and positivity-transparent, like G-MSCS1's t.*
- **E-MS2-6 (observational contact): (a)** NONE (as G-MSCS1).
- **E-MS2-7 (T1): the author's base list `05302210` (election of September 23, 2026) + the G-MSCS1 observational stratum** (the 25 patterns of `fef28271` beyond the base) **composed as `T1_forbidden_G_MSCS2.txt` at lock**; the recovered G-2a-L1 list `04438b74` is NOT used (author's election); no new stratum foreseen.
- **E-MS2-8 (continuity pin source): (a)** X-6 as stated (chat checkpoint values, CC cross-check).

**Elected as written above, every item, by the author's directive of September 26, 2026** (E-MS2-1 (a)+(b); E-MS2-2 (a); E-MS2-2b (a)+(b); E-MS2-2c ⟨001⟩/⟨111⟩; E-MS2-3 (a); E-MS2-4 (a); E-MS2-5 (a); E-MS2-6 (a); E-MS2-7; E-MS2-8 (a)). Q-MS2-1..4 are thereby answered (G-MSCS2; the second arm included; the K̃₄ normalization; no Born). The "Recommended" annotations above are the draft's and are retained as record.

## 9. Registers and non-claims

- Every number R1-machine two-leg. The IDENTITY-DELIVERED-L4 reading R2, conditional on E-MS-1(a) (inherited), the untextured import, K = ∅, the kernel election and the A-2.3 HS operationalization; the polycrystal postulate remains R3. **The exhaustion, affinity, cubic-null and Zener statements of §2.6 are identities (R1 controls), not results.**
- No observable, no bridge, no SI value, no d, no f, no μ_n, no channel-speed number against any bound; no value of t₂ or t₄ asserted for the substrate; no claim that Maxwell's equations are derived; no helicity-±2 field; no reinstatement of W_∪; no kill of the single-species claim is possible inside this gate and none is claimed; §2.52 Open 3 untouched.

## 10. Housekeeping (V4.85 — carried by this gate's fold, not by this memo; the staged facts are in `claude/V4_85_HOUSEKEEPING_STAGING.md`, 7be337ff)

**Repository state at lock (September 26, 2026, ~14:10 UTC; `git ls-remote` + shallow fetch of every branch head):** `main` = `d0a0e31` (the PR #13 merge of September 22); **`gmscs1_gate/estate/` absent on every branch; `SQT_Master_Ledger_v4_79_CANONICAL.md` still at the repository root; no branch newer than September 21.** The author's lock directive states that the HK-1 housekeeping is complete — "`gmscs1_gate/estate/` landed via PR #[PR_ESTATE], and the V4.79 canonical was removed from the root via PR #[PR_V479]" — with the PR numbers left as placeholders. **Recorded as observed, not resolved (A-2.4):** the HK-1 dispatch `36b8bd61` (September 23) is the instrument for both PRs; the numbers and merge dates are to be filled at fold time from the merged PRs, or carried by the V4.85 housekeeping bracket if the merges post-date the fold. Nothing in this gate's science depends on them.

The V4.85 fold carries the additive housekeeping brackets: **(a)** on §2.91.R / the V4.84 fold-in record — PR #25 (`022fa3c`, September 21, 05:32 UTC; the G-2a-A1 CC leg), PR #26 (`e3df402`, September 22, 00:55 UTC; `g2aa1_gate/estate/`, 12/12 content files verified, CC's independent reverse-splice of V4.84 → V4.83 byte-identical without holding V4.83; D-A1-2 the manifest self-entry), the V4.84 slot "⟨to be entered by the author⟩" resolved; **(b)** on §2.91.Q / the V4.83 record — the gmscs1 fold-side estate → `gmscs1_gate/estate/` by **PR #⟨n₁⟩ (merged ⟨date⟩)** from the tarball `027afc74` (HK-1 Task A); **(c)** the PR #13 items — the G-2a-L1 estate on `main` (supersedes "no G-2a-L1 estate exists in the repo"); the cited G-2a-L1 T1 list `04438b74` RECOVERED (H-MS-0 sharpened: `05302210` shares no pattern with it; the author's election of September 23: `05302210` remains the operative base, `04438b74` not used as a base); the V4.79 canonical (`6cfeca22`) committed at the root by PR #13 and to be **REMOVED by PR #⟨n₂⟩ (merged ⟨date⟩)** per the author's election (HK-1 Task B; history retains the blob) — the FOLD_LEDGER_2026-06-18 practice ("Canonical V4.39 is not in this repository; this file is the in-repo record") restated as standing. Append-only; no re-fold; the §2.52 Open 3 guard.

## 11. T1 list (composed and pinned September 26, 2026; the instruments halt without it — D-T1 retired)

`tools/t1/T1_forbidden_G_MSCS2.txt` md5 **`be921b8c29f7578e85ed92f1450c1956`** (1,695 B, **36 pattern lines**) = the base stratum `tools/t1/T1_base_author_20260919.txt` (`05302210cc4ceb70553acbe8379e9fc3`, 11 patterns; the author's election of September 23) + the G-MSCS1 observational stratum verbatim (the 25 patterns of `fef2827100d3f85e0a6341b44f0c00bf` beyond the base: the SI speed of light in scientific form, the 2017 tensor-speed bound digit strings in five renderings, SI speed units, event/collaboration/instrument identifiers, observational-search identifiers, the anisotropic-dispersion coefficient names of the observational dialect); no G-MSCS2-specific stratum. Scanner `t1_scan.py` `6b86290090a8c84f1b1a0a99ec0bf697` (pattern lines only; case-sensitive substring; bare numeric patterns under the contextual numeric rule; hits by pattern index only). `tools/t1/MANIFEST.md5` pins the three files. The list travels in-band (P-4); the instruments md5-assert it, scan themselves and this memo at every invocation, and halt on any hit — no override path exists. Note for the record: the recovered G-2a-L1 list `04438b74` is a gate-specific vocabulary quarantine and is not a generic stratum; the author's election stands. This memo scans CLEAN under the composed list (and, as a courtesy, under `04438b74`).

## 12. LSF-δ (executed September 26, 2026; seven clusters; per-source transcription ceilings stated)

Ceilings: **FT** = full text or full-text excerpt read this session; **AB** = abstract or publisher description; **LS** = listing only (title/venue confirmed; text not retrieved this session); **SEC** = secondary exposition; **NF** = not fetched this session, standard reference cited. Access notes: the Springer article pages (Man–Huang 2011; the 2018 HS-representation paper) were refused by the fetch proxy (rate-limited) and are cited at LS; the ADS abstract pages are robots-disallowed; PubMed served a challenge page; those sources are cited at LS with the citation data taken from the search listings and from the full texts that cite them.

| Cluster | Sources (ceiling) | What was found | Verdict |
|---|---|---|---|
| **L-MS2-1** ODF harmonics and crystal symmetry | Roe, J. Appl. Phys. 36, 2024 (1965) (LS; cited in Thompson–Smith–Lee 1984); Bunge, Krist. Tech. 3, 431 (1968) (LS; same); Bunge, *Texture Analysis in Materials Science* (1982) (NF, standard); Man, *Effects of Texture on the Plastic Anisotropy of Orthorhombic Sheets of Cubic Metals: A Group-Theoretic Analysis*, Univ. Kentucky / DTIC ADA333226 (1997) (FT excerpt: for cubic crystal symmetry "Since all W_2mn are zero" — the l = 2 null in print; the texture coefficients W₄₀₀, W₄₂₀, W₄₄₀ named as the ones that "would specify, to good approximation, the plastic anisotropy"). | The symmetrized-harmonic expansion, the cubic l = 2 null and the l = 4 cubic coefficients are textbook; the fiber (axisymmetric) case reduces the l = 4 content to a single coefficient (W₄₀₀ / C₄¹¹ ↔ this gate's t₄ up to the authors' normalizations — read, never load-bearing). | prior art (families; the cubic null); attribution; no collision. |
| **L-MS2-2** elasticity sees l ≤ 4; cubic aggregates see l = 4 only | Thompson, Smith, Lee, *Inference of Stress and Texture from Angular Dependence of Ultrasonic Plate Mode Velocities*, NASA NTRS 19860013503 (1984) (FT: "only three independent coefficients enter in the calculation of elastic constants for cubic crystallites, W400, W420, and W440"; "the velocity anisotropies can be directly related to coefficients of the expansion of the crystallite orientation distribution function"; cites Sayers–Allen J. Phys. D 17, 1399); Sayers, *Ultrasonic velocities in anisotropic polycrystalline aggregates*, J. Phys. D 15, 2157 (1982) (LS: listing confirmed; abstract not served); Man–Huang, *A Representation Theorem for Material Tensors of Weakly-Textured Polycrystals and Its Applications in Elasticity*, J. Elasticity 105, 1 (2011) (LS: page refused by the proxy; the theorem's content — material tensors expressed in irreducible basis tensors with texture-coefficient components — carried from the G-MSCS1 sweep at AB); Du, Univ. Kentucky dissertation (2014) (AB: extends the Man–Huang theorem to ODFs on O(3); "restrictions on texture coefficients imposed by crystal symmetry for all the 21 improper point groups"); Morris, J. Appl. Phys. 40, 447 (1969) (LS; averaging fourth-rank tensors with weight functions); Kocks–Tomé–Wenk, *Texture and Anisotropy* (1998) (NF, standard). | **Both identities of §2.6 are in print for the elastic tensor** — a rank-4 average sees l ≤ 4; cubic crystallites contribute only l = 4. The E₂-descriptor half of the exhaustion statement (the per-grain weight is degree 4 in the grain axis) is this gate's own elementary extension. | prior art adopted with attribution; the descriptor half novel-in-assembly; no collision. |
| **L-MS2-3** bounds for textured polycrystals | Walpole, J. Mech. Phys. Solids 14, 151 and 289 (1966) (LS; listings confirmed); Huang–Man, *Explicit Bounds of Effective Stiffness Tensors for Textured Aggregates of Cubic Crystallites*, Math. Mech. Solids 13, 408 (2008) (AB: "derive explicit lower and upper bounds for the effective stiffness tensor, which are quadratic in texture coefficients"; "much tighter than those delivered by the Reuss lower bound and the Voigt upper bound"; spherical grains, uncorrelated orientations); Man–Du, *Representation of Hashin–Shtrikman Bounds in Terms of Texture Coefficients for Arbitrarily Anisotropic Polycrystalline Materials*, J. Elasticity (2018) (LS; proxy-refused). | HS-type bounds for textured cubic aggregates exist in closed form in the texture coefficients (quadratic); this gate's Walpole-form HS with references fixed at t = 0 (A-2.3 of G-MSCS1) is the operational choice, its l ≤ 4 dependence an identity (§2.6). | prior art; grounds the operationalization; no collision. |
| **L-MS2-4** ultrasonic texture measurement in fiber-textured cubic metals | Thompson–Smith–Lee 1984 (FT, above; plate-mode velocity anisotropies → W₄ₘ₀ by an overdetermined system); Sayers–Allen, J. Phys. D 17, 1399 (LS); Hirao–Ogi, *EMATs for Science and Industry* (2003) (NF); MRS *Ultrasonic Characterization of Texture* (1989) (LS). | The closest prior art to "a shear-wave observable controlled by the l = 4 coefficient": the birefringence and plate-mode anisotropies are **first order** in W₄₀₀. This gate's observable is the descriptor split — two weightings of one phonon — **second order** by first-order protection; the birefringence itself is reported as b₁ for the differentiator (H-MS2-5). | prior art; differentiator stated; no collision. |
| **L-MS2-5** the textured SOA machinery | Acoustics 2(1), 5 (2020) (FT at G-MSCS1; carried). | The anisotropic-reference Green function — the registered t ≠ 0 second-order successor's machinery; not executed here (E-MS2-3(a)). | carried; no collision. |
| **L-MS2-6** the Danielewski / rotational-ether lane; emergent multi-species limiting speeds | Danielewski 2007 / 2020 / 2023; MacCullagh → Kelvin → Kleinert; Anber–Donoghue; Bednik–Pujolàs–Sibiryakov; Chadha–Nielsen; Collins et al. (all carried from G-MSCS1 §3 and §12; re-cited, not re-read). | Nothing new claimed against them; the obligation was discharged at G-MSCS1 (E-MS2-4). | carried; no collision. |
| **L-MS2-7** collision check | Search listing (September 26): no located work computes a descriptor split of two weightings of one elastic-vacuum phonon as a function of an l = 4 vacuum texture; the hits are discussion threads on spacetime as an elastic medium (ResearchGate), a one-way light-speed anisotropy claim (gr-qc/0509066 — unrelated to texture), and the Acoustics 2020 SOA paper (cluster 5). | **Novel-in-assembly; A0 not triggered.** Honest ceiling: every ingredient (l ≤ 4 exhaustion, the cubic l = 2 null, the degenerate-perturbation protection) is elementary or textbook; the novelty is the assembly and the delivered coefficients κ₄₄ / κ₂₄. | novel-in-assembly at the stated ceilings. |

## 13. Pre-lock state and the disclosure (September 26, 2026)

1. **Chat-side pre-draft sanity checks (disclosed, NOT gate results):** the identities of §2.6 verified numerically on a generic cubic tensor with a degree-12-exact SO(3) product quadrature (values in §2.6) and the constants of A-2.2 derived exactly (sympy). No banked tensor, no ledger value, no target was used; nothing from these enters any checkpoint; re-derived from scratch by both legs under lock.
2. **Lock conditions:** the author's sequencing condition (HK-1 PRs merged, `main` clean) — asserted met by the author's directive of September 26; the repository state observed at lock recorded in §10 (A-2.4); the elections E-MS2-1..8 — elected; the LSF-δ sweep — executed (§12); the T1 list — composed and pinned (§11, `be921b8c`); the lock record with Addendum A-2 — generated at lock with this file's md5; schema v1.0 + comparator v1.0 — written, self-tested, FROZEN before any chat emission (their md5s in the lock record); **the author's word "Lock" — given (directive of September 26, item 6).**
3. **Order of operations (binding):** memo lock → T1 pinned → schema v1.0 + comparator v1.0 frozen → chat instrument (md5-guards this memo, the T1 list, X-1 and X-6) → **Phase 0 (pins and controls) — the author's directive stops here for the report** → Phase 2 → Phase 3 → execution report → P-4/P-4.c dispatch → CC leg blind from scratch → two-leg comparison → S9 on misses → fold authorization → V4.85.

*v2, September 26, 2026 — LOCKED (author-authorized). Base V4.84 (f36bbdb0). Supersedes draft v1 (055a0010).*
=====END-EMBED name=staging_memo_G_MSCS2_v2.md=====

=====BEGIN-EMBED name=G_MSCS2_LOCK_RECORD.md md5=49232d4c42061c4536867eba14aae501 bytes=11804 encoding=raw=====
# G-MSCS2 — LOCK RECORD (September 26, 2026)

**Gate:** G-MSCS2 (Multi-Species Channel Speed, the l = 4 / cubic-effective texture family — the E-MS-5 registered successor of G-MSCS1). **Base:** V4.84 `f36bbdb04104008783f2763f70fb916f` (1,637,662 B). **Authorization:** the author's directive of September 26, 2026 ("I explicitly AUTHORIZE the lock"; elections E-MS2-1..8 confirmed as listed in memo §8).

## 1. Locked artifacts (frozen at these hashes; never edited after this record)

| Artifact | md5 | Bytes | Role |
|---|---|---|---|
| `staging_memo_G_MSCS2_v2.md` | **`efdcabdcd937cda4acb64f941dc4bb2b`** | 46,053 | the locked memo (v2; draft v1 `055a0010` superseded) |
| `g_mscs2_schema_v1_0.json` | **`66f586d7b6c5e8228394222ddfda73f2`** | 5,800 | checkpoint schema v1.0 — FROZEN pre-emission |
| `g_mscs2_compare_v1_0.py` | **`80d3b9078788fb17f57945da7d9c2c96`** | 17,376 | comparator v1.0 — FROZEN pre-emission; asserts the schema md5; 18/18 adversarial suites |
| `tools/t1/T1_forbidden_G_MSCS2.txt` | **`be921b8c29f7578e85ed92f1450c1956`** | 1,695 | gate T1 list (36 patterns = base `05302210` (11) + the G-MSCS1 stratum (25)) |
| `tools/t1/T1_base_author_20260919.txt` | `05302210cc4ceb70553acbe8379e9fc3` | 143 | base stratum (the author's election of September 23) |
| `tools/t1/t1_scan.py` | `6b86290090a8c84f1b1a0a99ec0bf697` | 1,967 | scanner (contextual numeric rule) |
| `inputs/poly_vrh_results.json` (X-1) | `200e7a8b775577564369c6924d38a84c` | 2,767 | the four banked tensors |
| `inputs/g_mscs1_chatleg_checkpoint.json` (X-6 chat) | `c04c0b8ea34cfe60f231aa06828e6ce4` | 33,289 | continuity pin source (values read at run time) |
| `inputs/g_mscs1_ccleg_checkpoint.json` (X-6 cc) | `249e11dd53c4cb82f302b15d3c94c337` | 24,415 | continuity cross-check |

Elections (T3-immutable): E-MS2-1 (a)+(b) · E-MS2-2 (a) · E-MS2-2b (a)+(b) · E-MS2-2c ⟨001⟩ primary / ⟨111⟩ reported · E-MS2-3 (a) · E-MS2-4 (a) · E-MS2-5 (a) · E-MS2-6 (a) · E-MS2-7 base `05302210` + G-MSCS1 stratum · E-MS2-8 (a). Schema `elections` codes: `a+b`, `a`, `a+b`, `001+111`, `a`, `a`, `a`, `a`, `05302210+MSCS1stratum`, `a`.

**Repository state at lock (recorded as observed; memo §10 / A-2.4):** live `main` = `d0a0e31`; `gmscs1_gate/estate/` absent on every branch; `SQT_Master_Ledger_v4_79_CANONICAL.md` at the root; the author's directive states both HK-1 PRs merged with the numbers as placeholders. Not load-bearing for the gate.

## 2. Addendum A-2 — operationalizations (binding for both legs; CC re-derives from these words, not from chat code)

**A-2.1 Configurations, arms, keys.** The eight keys in this order: `hex_step|a`, `hex_step|b`, `hex_gem8|a`, `hex_gem8|b`, `cubic_step|001`, `cubic_step|111`, `cubic_gem8|001`, `cubic_gem8|111`. Hex arm (a) = the banked tetragonal-form tensor (C66 as banked); arm (b) = hexagonal-symmetrized C66 = (C11 − C12)/2. Cubic `|001` = descriptor axis a cube axis; `|111` = a body diagonal. X-1 tensors from `poly_vrh_results.json['vrh'][cfg]['C_over_rho']` with cfg ∈ {`hex:step`, `hex:gem8`, `cubic:step`, `cubic:gem8`}; the X-6 bank keys are `step_hex`, `gem8_hex`, `step_cubic`, `gem8_cubic` in `pins_vrh0`, and the eight keys above in `phase1` / `phase2`.

**A-2.2 The ODF families (fiber axis = lab ẑ; grain orientation g ∈ SO(3); crystal axes ê_i = g e_i).**
- Cubic K̃₄ family: w(g) = 1 + t₄·K̃₄(g), **K̃₄(g) = (5/2)·(Σ_{i=1}^{3} (ê_i·ẑ)⁴ − 3/5)**; range [−2/3, 1]; positivity t₄ ∈ [−1, 3/2]; ⟨K̃₄⟩_SO(3) = 0; ⟨K̃₄²⟩ = 4/21.
- Hex P₄ family: w = 1 + t₄·P₄(ĉ·ẑ), ĉ the c-axis; P₄(x) = (35x⁴ − 30x² + 3)/8; range [−3/7, 1]; positivity t₄ ∈ [−1, 7/3]; ⟨P₄²⟩ = 1/9.
- Hex two-parameter family: w = 1 + t₂·P₂(ĉ·ẑ) + t₄·P₄(ĉ·ẑ); positivity asserted on the SO(3) grid at every (t₂, t₄) used (F-CTRL-POS); the 5 × 5 grid t₂, t₄ ∈ {−0.25, −0.125, 0, 0.125, 0.25} lies inside the positivity region.
- l = 2 family for PIN-K2 and F-CTRL-L2NULL: exactly G-MSCS1's — w = 1 + t·P₂((g·axis_c)·ẑ) with axis_c the elected descriptor axis (ẑ for hex and cubic |001; (1,1,1)/√3 for cubic |111); G-MSCS1's 12-point t-grid.
- Exhaustion probe (F-CTRL-L4EXHAUST): hex — add t₆·P₆(ĉ·ẑ), P₆ = (231x⁶ − 315x⁴ + 105x² − 5)/16, t₆ = 0.3; cubic — add t₆·K₆(g) with K₆ the l = 6 cubic harmonic of the fiber axis in the crystal frame, K₆ ∝ (x⁶ + y⁶ + z⁶) − (15/11)(x⁴ + y⁴ + z⁴) + 30/77 (any non-zero multiple; sphere-mean zero is asserted), at an amplitude keeping w ≥ 0. The claim: ⟨C⟩_V, ⟨S⟩_R, C_HS (references fixed) and r_agg change by ≤ 10⁻¹² relative / absolute.

**A-2.3 The t₄-grid, the fits, halving.** t₄-grid (12 points, the G-MSCS1 grid): −0.5, −0.25, −0.1, −0.05, −0.02, 0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0 (all inside both positivity ranges). Fit r_agg(t₄) = S₄ t₄ + κ₄₄ t₄² + κ₄₄₄ t₄³ by least squares on the 7 grid points with |t₄| ≤ 0.25 (no constant term); the halving witness: refit on the 5 points with |t₄| ≤ 0.1 and report `halving_dev_kappa44` = |κ₄₄(0.25) − κ₄₄(0.1)| (absolute; the comparator accepts ≤ max(10⁻⁴·|κ₄₄|, 10⁻⁶) — the V4.83 process note). Quadratic form (hex second arm): fit r_agg(t₂, t₄) = κ₂₂ t₂² + κ₂₄ t₂t₄ + κ₄₄ t₄² + (cubic terms t₂³, t₂²t₄, t₂t₄², t₄³, included and discarded) on the 5 × 5 grid; on cubic keys the same fit is run and κ₂₂, κ₂₄ must be ≤ 10⁻¹⁰ (fit-amplified null). `kappa44` in `quadform` and `kappa44_E2` from the one-parameter fit are both reported (they need not coincide beyond the two-leg tolerance; the one-parameter value is the gate's κ₄₄ of record).

**A-2.4 The aggregate schemes and the HS operationalization (inherited from G-MSCS1 A-2.3).** Voigt = ODF average of the rotated stiffness; Reuss = inverse of the ODF average of the rotated compliance; Hill = arithmetic mean; Walpole-form HS with isotropic references (K₀, G₀) optimized at t = 0 (the tightest feasible majorant/minorant by the G-MSCS1 procedure or any procedure reproducing the X-6 `hs_ref` to PIN-HS0 tolerance) and **reused unchanged at every t₄ and (t₂, t₄)**; `HS` = the mean of the two bounds. Speeds: Christoffel on the aggregate tensor over the k̂-sphere quadrature GL(cos θ) 64 × uniform φ 128 (weights summing to 1); doubling check at 128 × 256 on r_agg at one non-zero t₄ per key (F-CTRL-QUAD ≤ 10⁻¹⁰).

**A-2.5 The descriptor weights (inherited verbatim from G-MSCS1 A-2/§2).** w_EM = 1 − (k̂·e)²; S2-E₂ per grain = |P^{(±2)}_{n̂} S_⊥|²/|S_⊥|² · w_EM with S_⊥ = sym(k̂ ⊗ e_⊥) and n̂ the descriptor axis, via frac_E2(n̂) = 1 − 2|S_⊥n̂|²/|S_⊥|² + ½(n̂·S_⊥·n̂)²/|S_⊥|²; S2-h = (1 − λ_L)/(1 + λ_L/3). **ODF average of the S2-E₂ weight (F-CTRL-MARG):** the S² average of frac_E2(n̂) over the descriptor axis with the marginal weight **1 + c·t₄·P₄(n̂·ẑ)** — c = 1 for hex (any family) and for cubic `|001`, c = −2/3 for cubic `|111`; for the hex two-parameter family the marginal is 1 + t₂P₂ + t₄P₄. The instrument also evaluates the SO(3)-direct average (the weight of the K̃₄ family on the full orientation, the descriptor axis carried along) on the cubic keys and asserts equality to 10⁻¹². n̂-sphere quadrature GL 12 × 24 (exact for degree ≤ 8 integrands in n̂).

**A-2.6 Exact closed forms asserted (F-CTRL-C4).** With H = C₁₁ − C₁₂ − 2C₄₄ of the single-crystal cubic tensor: ⟨C⟩_V(t₄) − ⟨C⟩_V(0) = t₄·(H/3)·𝒯⁴(ẑ), Voigt entries ΔC₁₁ = ΔC₂₂ = 3Ht₄/105, ΔC₃₃ = 8Ht₄/105, ΔC₁₂ = Ht₄/105, ΔC₁₃ = ΔC₂₃ = −4Ht₄/105, ΔC₄₄ = ΔC₅₅ = −4Ht₄/105, ΔC₆₆ = Ht₄/105, all other entries zero; asserted at t₄ = 0.3 and t₄ = 0.6 (affinity) on both cubic configurations to 10⁻¹² relative to max|C|; a synthetic H = 0 (isotropic) tensor must give |Δ⟨C⟩_V| ≤ 10⁻¹² relative. Reuss: the same law on the compliance with H_S = S₁₁ − S₁₂ − S₄₄/2 (asserted likewise). Voigt birefringence identity (in-instrument check, not a schema key): for propagation ⊥ ẑ, v_qSH² − v_qSV² = ΔC₆₆ − ΔC₄₄ = 5Ht₄/105 = Ht₄/21 on the Voigt tensor.

**A-2.7 Birefringence reporting quantity.** `biref_b1_VRH` = d/dt₄ [(v_qSH(k̂⊥) − v_qSV(k̂⊥))/v_T(0)] at t₄ = 0 on the Hill tensor, by the symmetric difference at t₄ = ±0.05, with k̂⊥ = x̂ (perpendicular to the fiber) and the two transverse branches labelled by polarization (qSH: e ∥ ŷ; qSV: e ∥ ẑ); for hex keys the same under the P₄ family. Reported; two-leg tolerance 10⁻⁶ absolute.

**A-2.8 Continuity pins (X-6 values read at run time from the chat checkpoint; the CC checkpoint as cross-check).** PIN-XTAL: `phase1[key]` {`r_xtal_E2`, `r_xtal_h`, `lambda_mean`, `lambda_max`} — worst relative deviation ≤ 10⁻⁸ over the 8 keys; PIN-VRH0: `phase2[key]` {`vT_VRH`, `vT_V`, `vT_R`} ≤ 10⁻⁸; PIN-HS0: `phase2[key]` {`vT_HS_lo`, `vT_HS_hi`} and `pins_vrh0[cfg].G_HS` ≤ 10⁻⁶ (a re-optimized reference may differ at the optimizer's tolerance); PIN-K2: `phase2[key].kappa2_E2` on the four hex keys ≤ 10⁻⁴ relative (the values of record: −1.43946×10⁻³, −1.43870×10⁻³, −1.89565×10⁻³, −1.89614×10⁻³), and |κ₂| ≤ 10⁻¹² on the four cubic keys — computed by this gate's machinery with the l = 2 family switched on (t₄ = 0) using G-MSCS1's fit window and grid.

**A-2.9 Controls' operational definitions.** F-CTRL-ISO: an isotropic cubic tensor (K = 134.609, G = 70.881, the G-MSCS1 values) → |r_agg(t₄)| ≤ 10⁻¹⁰ for every grid t₄, both families (K̃₄ on the cubic path; P₄ on the hex path) and |r_xtal| ≤ 10⁻¹⁰. F-CTRL-SO3: on `hex_step|a` at t = 0 the ODF-averaged E₂ fraction equals 2/5 for every mode with w_EM > 10⁻⁶ to 10⁻¹⁰ and |r_agg(0)| ≤ 10⁻⁶. F-CTRL-POS: min over the SO(3) grid of every ODF used ≥ 0. F-CTRL-L2NULL: on both cubic configurations, the l = 2 family at t = 1 and the mixed (t₂, t₄) = (0.25, 0.25) vs (0, 0.25) leave ⟨C⟩_V, ⟨S⟩_R, C_HS and r_agg unchanged to 10⁻¹². F-CTRL-L4EXHAUST as A-2.2 (≤ 10⁻¹² relative on tensors, absolute on r_agg). F-CTRL-C4, F-CTRL-MARG as A-2.5/A-2.6. F-CTRL-TEX4: the synthetic cubic tensor C11 = 300, C12 = 100, C44 = 40 (H = 120) at t₄ = 1 gives |r_agg(S2-E₂, `|001`, Hill)| > 10⁻⁶. F-CTRL-QUAD: doubling residual ≤ 10⁻¹⁰.

**A-2.10 Checkpoint discipline.** One checkpoint per leg, written once after Phase 3 (the Phase-0-only run of the author's directive writes `g_mscs2_chatleg_phase0_checkpoint.json` — a partial checkpoint, superseded by the full one when Phases 2–3 are authorized; the full checkpoint recomputes Phase 0 from scratch, never copies it); the instrument md5-guards this memo, the T1 list, X-1 and both X-6 files, scans itself and the memo at every invocation, and halts on any T1 hit (no override). Floats at full double precision in JSON; arrays in the schema's grid order; the verdict class assembled last by the schema rule.

## 3. Order of operations (binding)

Memo lock (this record) → T1 pinned → schema + comparator frozen → chat instrument → **Phase 0 (pins and controls) — report to the author** → Phase 2 → Phase 3 → execution report → dispatch (P-4/P-4.c; the T1 lists in-band) → CC leg blind from scratch (method variation requested: a different SO(3) quadrature or the analytic generalized-spherical-harmonic route for the ODF averages) → two-leg comparison → S9 on misses → fold authorization → V4.85.
=====END-EMBED name=G_MSCS2_LOCK_RECORD.md=====

=====BEGIN-EMBED name=g_mscs2_schema_v1_0.json md5=66f586d7b6c5e8228394222ddfda73f2 bytes=5800 encoding=raw=====
{
 "comparison_rules": {
  "exact": "strings/bools/ints compared for equality; elections and provenance md5s compared to this schema on each leg",
  "float": "phase0 float rules evaluated per leg (the comparator re-evaluates the pass condition from the reported float, independent of the leg's own 'passed' flag, and also requires passed == true on both legs); phase2 arrays compared elementwise across legs at array_tol_abs; abs_keys across legs at the stated absolute tolerance; rel_keys across legs at |a-b| <= max(rel*max(|a|,|b|), floor)",
  "free_text": "never compared",
  "independence_witness": "instrument_md5 must differ between legs"
 },
 "cubic_keys": [
  "cubic_step|001",
  "cubic_step|111",
  "cubic_gem8|001",
  "cubic_gem8|111"
 ],
 "elections": {
  "E-MS2-1": "a+b",
  "E-MS2-2": "a",
  "E-MS2-2b": "a+b",
  "E-MS2-2c": "001+111",
  "E-MS2-3": "a",
  "E-MS2-4": "a",
  "E-MS2-5": "a",
  "E-MS2-6": "a",
  "E-MS2-7": "05302210+MSCS1stratum",
  "E-MS2-8": "a"
 },
 "frozen": "2026-09-26",
 "gate": "G-MSCS2",
 "hex_keys": [
  "hex_step|a",
  "hex_step|b",
  "hex_gem8|a",
  "hex_gem8|b"
 ],
 "keys": [
  "hex_step|a",
  "hex_step|b",
  "hex_gem8|a",
  "hex_gem8|b",
  "cubic_step|001",
  "cubic_step|111",
  "cubic_gem8|001",
  "cubic_gem8|111"
 ],
 "ledger_base_md5": "f36bbdb04104008783f2763f70fb916f",
 "leg_domain": [
  "chat",
  "cc"
 ],
 "memo_lock_bytes": 46053,
 "memo_lock_md5": "efdcabdcd937cda4acb64f941dc4bb2b",
 "phase0": {
  "float_rules": {
   "F-CTRL-C4": {
    "h0_effect_rel": {
     "rule": "le",
     "threshold": 1e-12
    },
    "worst_rel_affine": {
     "rule": "le",
     "threshold": 1e-12
    },
    "worst_rel_closed_form": {
     "rule": "le",
     "threshold": 1e-12
    }
   },
   "F-CTRL-ISO": {
    "worst_abs": {
     "rule": "le",
     "threshold": 1e-10
    }
   },
   "F-CTRL-L2NULL": {
    "worst_abs": {
     "rule": "le",
     "threshold": 1e-12
    }
   },
   "F-CTRL-L4EXHAUST": {
    "worst_abs_r_agg": {
     "rule": "le",
     "threshold": 1e-12
    },
    "worst_rel_tensor": {
     "rule": "le",
     "threshold": 1e-12
    }
   },
   "F-CTRL-MARG": {
    "worst_abs": {
     "rule": "le",
     "threshold": 1e-12
    }
   },
   "F-CTRL-POS": {
    "min_odf_weight": {
     "rule": "ge",
     "threshold": 0.0
    }
   },
   "F-CTRL-QUAD": {
    "doubling_residual": {
     "rule": "le",
     "threshold": 1e-10
    }
   },
   "F-CTRL-SO3": {
    "dev_from_0p4": {
     "rule": "le",
     "threshold": 1e-10
    },
    "r_agg_0_abs": {
     "rule": "le",
     "threshold": 1e-06
    }
   },
   "F-CTRL-TEX4": {
    "r_agg_t1_abs": {
     "rule": "gt",
     "threshold": 1e-06
    }
   },
   "PIN-HS0": {
    "worst_rel": {
     "rule": "le",
     "threshold": 1e-06
    }
   },
   "PIN-K2": {
    "worst_abs_cubic_kappa2": {
     "rule": "le",
     "threshold": 1e-12
    },
    "worst_rel_hex_kappa2": {
     "rule": "le",
     "threshold": 0.0001
    }
   },
   "PIN-VRH0": {
    "worst_rel": {
     "rule": "le",
     "threshold": 1e-08
    }
   },
   "PIN-XTAL": {
    "worst_rel": {
     "rule": "le",
     "threshold": 1e-08
    }
   }
  },
  "items": [
   "PIN-XTAL",
   "PIN-VRH0",
   "PIN-HS0",
   "PIN-K2",
   "F-CTRL-ISO",
   "F-CTRL-SO3",
   "F-CTRL-POS",
   "F-CTRL-L2NULL",
   "F-CTRL-L4EXHAUST",
   "F-CTRL-C4",
   "F-CTRL-MARG",
   "F-CTRL-TEX4",
   "F-CTRL-QUAD"
  ]
 },
 "phase2": {
  "abs_keys": {
   "S4_E2": 1e-06,
   "S4_h": 1e-06,
   "biref_b1_VRH": 1e-06
  },
  "array_keys": {
   "lambda_mean_t4": 12,
   "r_agg_E2_HS": 12,
   "r_agg_E2_R": 12,
   "r_agg_E2_V": 12,
   "r_agg_E2_VRH": 12,
   "r_agg_h_VRH": 12
  },
  "array_tol_abs": 1e-06,
  "per_leg_rules": {
   "halving_dev_kappa44": {
    "floor": 1e-06,
    "rel": 0.0001,
    "rule": "le_rel_floor"
   }
  },
  "quadform_cubic_null_abs": 1e-10,
  "quadform_keys": {
   "kappa22": [
    0.0001,
    1e-06
   ],
   "kappa24": [
    0.0001,
    1e-06
   ],
   "kappa44": [
    0.0001,
    1e-06
   ]
  },
  "rel_keys": {
   "kappa444_E2": [
    0.0001,
    1e-06
   ],
   "kappa44_E2": [
    0.0001,
    1e-06
   ],
   "kappa44_E2_HS": [
    0.0001,
    1e-06
   ],
   "kappa44_h": [
    0.0001,
    1e-06
   ],
   "vT_HS_hi": [
    1e-06,
    0.0
   ],
   "vT_HS_lo": [
    1e-06,
    0.0
   ],
   "vT_VRH": [
    1e-08,
    0.0
   ]
  }
 },
 "phase3": {
  "exact_keys": {
   "F-MS2-2": "str",
   "F-MS2-3": "str",
   "F-MS2-4": "str",
   "verdict_class": "str"
  },
  "float_keys": {
   "worst_S4": {
    "rule": "le",
    "threshold": 1e-06
   }
  },
  "verdict_domain": [
   "IDENTITY-DELIVERED-L4",
   "PROTECTION-BREACH",
   "L4-NULL",
   "INDETERMINATE"
  ]
 },
 "primary_cubic_keys": [
  "cubic_step|001",
  "cubic_gem8|001"
 ],
 "required_top": [
  "gate",
  "leg",
  "instrument_md5",
  "memo_lock_md5",
  "ledger_base_md5",
  "t1_list_md5",
  "x1_md5",
  "x6_chat_md5",
  "x6_cc_md5",
  "elections",
  "t1_scan",
  "phase0",
  "phase2",
  "phase3"
 ],
 "schema": "G-MSCS2 checkpoint schema v1.0",
 "t1_list_md5": "be921b8c29f7578e85ed92f1450c1956",
 "t1_scan_domain": [
  "CLEAN"
 ],
 "t1_scan_required": [
  "instrument",
  "memo"
 ],
 "t2t4_grid": [
  -0.25,
  -0.125,
  0.0,
  0.125,
  0.25
 ],
 "t4_grid": [
  -0.5,
  -0.25,
  -0.1,
  -0.05,
  -0.02,
  0.0,
  0.02,
  0.05,
  0.1,
  0.25,
  0.5,
  1.0
 ],
 "tolerances": {
  "kappa_floor": 1e-06,
  "tau_agg": 1e-06
 },
 "verdict_rule": "INDETERMINATE if any phase0 item has passed == false; else PROTECTION-BREACH if max over keys of |S4_E2|,|S4_h| > tau_agg; else L4-NULL if |kappa44_E2| <= kappa_floor on both primary_cubic_keys; else IDENTITY-DELIVERED-L4. Precedence INDETERMINATE > PROTECTION-BREACH > L4-NULL > IDENTITY-DELIVERED-L4.",
 "x1_md5": "200e7a8b775577564369c6924d38a84c",
 "x6_cc_md5": "249e11dd53c4cb82f302b15d3c94c337",
 "x6_chat_md5": "c04c0b8ea34cfe60f231aa06828e6ce4"
}
=====END-EMBED name=g_mscs2_schema_v1_0.json=====

=====BEGIN-EMBED name=g_mscs2_compare_v1_0.py md5=80d3b9078788fb17f57945da7d9c2c96 bytes=17376 encoding=raw=====
#!/usr/bin/env python3
"""g_mscs2_compare_v1_0.py — two-leg comparator for Gate G-MSCS2, FROZEN v1.0 (September 26, 2026).

Compares the chat-leg and CC-leg checkpoints against g_mscs2_schema_v1_0.json.
Checks: C0 provenance + independence witness; C1 Phase 0 (13 pins/controls: passed on both legs AND the
float rule re-evaluated per leg from the reported float); C2 Phase 2 per configuration/arm key (12-point arrays
elementwise; S4/biref absolute; kappas relative with an absolute floor — a null compares as a null, never 0/0;
the hex quadratic form; the cubic quadform null); C3 Phase 3 (verdict identity, verdict recomputed from the
states by the schema rule, falsifier states). Free text is never compared.

Usage:
  compare  : python3 g_mscs2_compare_v1_0.py compare CHAT.json CC.json [--schema S.json] [--out OUT.json]
  selftest : python3 g_mscs2_compare_v1_0.py selftest
Exit: 0 all PASS, 1 any MISS, 2 usage/fatal.
"""
import hashlib, json, sys, copy, math

SCHEMA_DEFAULT = "g_mscs2_schema_v1_0.json"
SCHEMA_MD5 = "66f586d7b6c5e8228394222ddfda73f2"   # frozen schema v1.0 md5; asserted at load

def md5_file(p): return hashlib.md5(open(p, "rb").read()).hexdigest()

def load_schema(path):
    raw = open(path, "rb").read(); h = hashlib.md5(raw).hexdigest()
    if h != SCHEMA_MD5: raise SystemExit(f"FATAL: schema md5 {h} != frozen {SCHEMA_MD5}")
    return json.loads(raw.decode("utf-8")), h

def isnum(v): return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)

def get(d, path, default=None):
    cur = d
    for k in path.split("."):
        if not isinstance(cur, dict) or k not in cur: return default
        cur = cur[k]
    return cur

class Rec:
    def __init__(self): self.rows = []
    def add(self, check, name, ok, a=None, b=None, note=""):
        self.rows.append({"check": check, "name": name, "pass": bool(ok), "chat": a, "cc": b, "note": note})
    def summary(self):
        n = len(self.rows); p = sum(r["pass"] for r in self.rows); return {"checks": n, "pass": p, "miss": n - p}

def rule_ok(v, rule):
    if not isnum(v): return False
    r = rule["rule"]
    if r == "le": return v <= rule["threshold"]
    if r == "ge": return v >= rule["threshold"]
    if r == "gt": return v > rule["threshold"]
    if r == "le_rel_floor": return True   # handled with context
    return False

def rel_floor_ok(a, b, rel, floor):
    return isnum(a) and isnum(b) and abs(a - b) <= max(rel * max(abs(a), abs(b)), floor)

def recompute_verdict(ck, S):
    P0 = get(ck, "phase0", {}) or {}
    if any(get(P0, f"{it}.passed") is not True for it in S["phase0"]["items"]): return "INDETERMINATE"
    P2 = get(ck, "phase2", {}) or {}
    tau, floor = S["tolerances"]["tau_agg"], S["tolerances"]["kappa_floor"]
    worst = 0.0
    for k in S["keys"]:
        for f in ("S4_E2", "S4_h"):
            v = get(P2, f"{k}.{f}")
            if not isnum(v): return "INDETERMINATE"
            worst = max(worst, abs(v))
    if worst > tau: return "PROTECTION-BREACH"
    if all(isnum(get(P2, f"{k}.kappa44_E2")) and abs(get(P2, f"{k}.kappa44_E2")) <= floor for k in S["primary_cubic_keys"]): return "L4-NULL"
    return "IDENTITY-DELIVERED-L4"

def compare(chat, cc, S):
    R = Rec()
    # ---------------- C0 provenance ----------------
    for k in S["required_top"]:
        R.add("C0", f"required key {k} present (chat)", k in chat); R.add("C0", f"required key {k} present (cc)", k in cc)
    for k in ("memo_lock_md5", "ledger_base_md5", "t1_list_md5", "x1_md5", "x6_chat_md5", "x6_cc_md5"):
        R.add("C0", f"{k} == schema (chat)", chat.get(k) == S[k], chat.get(k), S[k]); R.add("C0", f"{k} == schema (cc)", cc.get(k) == S[k], cc.get(k), S[k])
    R.add("C0", "gate label", chat.get("gate") == S["gate"] and cc.get("gate") == S["gate"], chat.get("gate"), cc.get("gate"))
    R.add("C0", "leg labels chat/cc", chat.get("leg") == "chat" and cc.get("leg") == "cc", chat.get("leg"), cc.get("leg"))
    for f in S["t1_scan_required"]:
        R.add("C0", f"t1_scan.{f} CLEAN (chat)", get(chat, f"t1_scan.{f}") in S["t1_scan_domain"], get(chat, f"t1_scan.{f}"))
        R.add("C0", f"t1_scan.{f} CLEAN (cc)", get(cc, f"t1_scan.{f}") in S["t1_scan_domain"], None, get(cc, f"t1_scan.{f}"))
    R.add("C0", "elections == schema (chat)", chat.get("elections") == S["elections"], chat.get("elections"), S["elections"])
    R.add("C0", "elections == schema (cc)", cc.get("elections") == S["elections"], cc.get("elections"), S["elections"])
    R.add("C0", "independence witness: instrument_md5 differ", bool(chat.get("instrument_md5")) and bool(cc.get("instrument_md5")) and chat.get("instrument_md5") != cc.get("instrument_md5"), chat.get("instrument_md5"), cc.get("instrument_md5"))
    # ---------------- C1 phase0 ----------------
    A, B = chat.get("phase0", {}) or {}, cc.get("phase0", {}) or {}
    for it in S["phase0"]["items"]:
        pa, pb = get(A, f"{it}.passed"), get(B, f"{it}.passed")
        R.add("C1", f"phase0.{it}.passed true both legs", pa is True and pb is True, pa, pb)
        for fk, rule in S["phase0"]["float_rules"].get(it, {}).items():
            for leg, D in (("chat", A), ("cc", B)):
                v = get(D, f"{it}.{fk}")
                R.add("C1", f"phase0.{it}.{fk} ({leg}) {rule['rule']} {rule['threshold']}", rule_ok(v, rule), v if leg == "chat" else None, v if leg == "cc" else None)
    # ---------------- C2 phase2 ----------------
    P2 = S["phase2"]; A, B = chat.get("phase2", {}) or {}, cc.get("phase2", {}) or {}
    for k in S["keys"]:
        ka, kb = A.get(k) or {}, B.get(k) or {}
        R.add("C2", f"phase2[{k}] present both legs", bool(ka) and bool(kb))
        for ak, n in P2["array_keys"].items():
            va, vb = ka.get(ak), kb.get(ak)
            okl = isinstance(va, list) and isinstance(vb, list) and len(va) == n and len(vb) == n and all(isnum(x) for x in va + vb)
            R.add("C2", f"phase2[{k}].{ak} length {n} both legs", okl, len(va) if isinstance(va, list) else None, len(vb) if isinstance(vb, list) else None)
            worst = max((abs(x - y) for x, y in zip(va, vb)), default=float("inf")) if okl else float("inf")
            R.add("C2", f"phase2[{k}].{ak} elementwise <= {P2['array_tol_abs']}", okl and worst <= P2["array_tol_abs"], None, None, f"worst {worst:.3e}" if okl else "")
        for fk, tol in P2["abs_keys"].items():
            va, vb = ka.get(fk), kb.get(fk)
            R.add("C2", f"phase2[{k}].{fk} abs <= {tol}", isnum(va) and isnum(vb) and abs(va - vb) <= tol, va, vb)
        for fk, (rel, floor) in P2["rel_keys"].items():
            va, vb = ka.get(fk), kb.get(fk)
            R.add("C2", f"phase2[{k}].{fk} rel <= {rel} (floor {floor})", rel_floor_ok(va, vb, rel, floor), va, vb)
        for fk, rule in P2["per_leg_rules"].items():
            for leg, D in (("chat", ka), ("cc", kb)):
                v = D.get(fk); kv = D.get("kappa44_E2")
                ok = isnum(v) and isnum(kv) and v <= max(rule["rel"] * abs(kv), rule["floor"])
                R.add("C2", f"phase2[{k}].{fk} ({leg}) <= max(rel*|kappa44|, floor)", ok, v if leg == "chat" else None, v if leg == "cc" else None)
        qa, qb = ka.get("quadform") or {}, kb.get("quadform") or {}
        for fk, (rel, floor) in P2["quadform_keys"].items():
            va, vb = qa.get(fk), qb.get(fk)
            R.add("C2", f"phase2[{k}].quadform.{fk} rel <= {rel} (floor {floor})", rel_floor_ok(va, vb, rel, floor), va, vb)
        if k in S["cubic_keys"]:
            for fk in ("kappa22", "kappa24"):
                for leg, Q in (("chat", qa), ("cc", qb)):
                    v = Q.get(fk)
                    R.add("C2", f"phase2[{k}].quadform.{fk} ({leg}) cubic null abs <= {P2['quadform_cubic_null_abs']}", isnum(v) and abs(v) <= P2["quadform_cubic_null_abs"], v if leg == "chat" else None, v if leg == "cc" else None)
    # ---------------- C3 phase3 ----------------
    P3 = S["phase3"]; A, B = chat.get("phase3", {}) or {}, cc.get("phase3", {}) or {}
    for fk, t in P3["exact_keys"].items():
        va, vb = A.get(fk), B.get(fk)
        R.add("C3", f"phase3.{fk} typed str both legs", isinstance(va, str) and isinstance(vb, str), va, vb)
        R.add("C3", f"phase3.{fk} equal", isinstance(va, str) and va == vb, va, vb)
    for leg, D in (("chat", A), ("cc", B)):
        R.add("C3", f"phase3.verdict_class in domain ({leg})", D.get("verdict_class") in P3["verdict_domain"], D.get("verdict_class") if leg == "chat" else None, D.get("verdict_class") if leg == "cc" else None)
        for fk, rule in P3["float_keys"].items():
            v = D.get(fk); R.add("C3", f"phase3.{fk} ({leg}) {rule['rule']} {rule['threshold']}", rule_ok(v, rule), v if leg == "chat" else None, v if leg == "cc" else None)
    for leg, ck, D in (("chat", chat, A), ("cc", cc, B)):
        rv = recompute_verdict(ck, S)
        R.add("C3", f"verdict recomputed == reported ({leg})", rv == D.get("verdict_class"), rv if leg == "chat" else None, rv if leg == "cc" else None, f"reported {D.get('verdict_class')}")
        ws = max([abs(get(ck, f"phase2.{k}.{f}", float('nan'))) for k in S["keys"] for f in ("S4_E2", "S4_h")], default=float("nan"))
        R.add("C3", f"worst_S4 consistent with phase2 ({leg})", isnum(D.get("worst_S4")) and isnum(ws) and abs(D.get("worst_S4") - ws) <= 1e-15, None, None)
        fm3 = "FIRES" if isnum(ws) and ws > S["tolerances"]["tau_agg"] else "SILENT"
        R.add("C3", f"F-MS2-3 state consistent ({leg})", D.get("F-MS2-3") == fm3, D.get("F-MS2-3") if leg == "chat" else None, D.get("F-MS2-3") if leg == "cc" else None)
    return R

# ---------------------------------------------------------------- selftest
T4 = [-0.5, -0.25, -0.1, -0.05, -0.02, 0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0]
def canonical_checkpoint(leg, S):
    """Synthetic checkpoint carrying the memo's a-priori shape (HYP-MS2-1..5). NOT a result."""
    prov = {k: S[k] for k in ("memo_lock_md5", "ledger_base_md5", "t1_list_md5", "x1_md5", "x6_chat_md5", "x6_cc_md5")}
    p0 = {}
    vals = {"PIN-XTAL": {"worst_rel": 1e-12}, "PIN-VRH0": {"worst_rel": 3e-12}, "PIN-HS0": {"worst_rel": 2e-9}, "PIN-K2": {"worst_rel_hex_kappa2": 2e-6, "worst_abs_cubic_kappa2": 1e-15},
            "F-CTRL-ISO": {"worst_abs": 1e-14}, "F-CTRL-SO3": {"dev_from_0p4": 4e-15, "r_agg_0_abs": 1e-14}, "F-CTRL-POS": {"min_odf_weight": 0.5},
            "F-CTRL-L2NULL": {"worst_abs": 4e-14}, "F-CTRL-L4EXHAUST": {"worst_rel_tensor": 2e-15, "worst_abs_r_agg": 1e-15},
            "F-CTRL-C4": {"worst_rel_affine": 1e-14, "worst_rel_closed_form": 4e-15, "h0_effect_rel": 1e-15}, "F-CTRL-MARG": {"worst_abs": 2e-14},
            "F-CTRL-TEX4": {"r_agg_t1_abs": 2.3e-3}, "F-CTRL-QUAD": {"doubling_residual": 1e-13}}
    for it in S["phase0"]["items"]:
        p0[it] = dict(vals[it]); p0[it]["passed"] = True
    p2 = {}
    for i, k in enumerate(S["keys"]):
        cub = k.startswith("cubic"); kap = (-3.1e-3 if "001" in k else 2.2e-3) if cub else -0.9e-3
        eps = 1e-9 if leg == "cc" else 0.0
        r = [kap * t * t - 0.4e-3 * t**3 + eps for t in T4]
        p2[k] = {"r_agg_E2_VRH": r, "r_agg_h_VRH": [x * 1e-3 for x in r], "r_agg_E2_HS": [x * 0.99 for x in r], "r_agg_E2_V": [x * 1.02 for x in r], "r_agg_E2_R": [x * 0.98 for x in r],
                 "lambda_mean_t4": [1e-5 * t * t for t in T4], "S4_E2": 2e-13 + eps, "S4_h": 1e-13, "biref_b1_VRH": (0.12 if cub else 0.05) + eps,
                 "kappa44_E2": kap * (1 + eps), "kappa44_h": kap * 1e-3, "kappa444_E2": -0.4e-3, "kappa44_E2_HS": kap * 0.99, "halving_dev_kappa44": abs(kap) * 2e-5,
                 "vT_VRH": 8.4 + i * 0.1, "vT_HS_lo": 8.39 + i * 0.1, "vT_HS_hi": 8.41 + i * 0.1,
                 "quadform": {"kappa22": (0.0 if cub else -1.44e-3) + (1e-16 if cub else eps), "kappa24": (0.0 if cub else -0.5e-3) + (2e-16 if cub else eps), "kappa44": kap * (1 + eps), "residual": 1e-9}}
    ck = {"gate": "G-MSCS2", "leg": leg, "instrument_md5": ("chat" * 8) if leg == "chat" else ("cc00" * 8), **prov,
          "t1_scan": {"instrument": "CLEAN", "memo": "CLEAN"}, "elections": dict(S["elections"]), "phase0": p0, "phase2": p2,
          "phase3": {"verdict_class": "IDENTITY-DELIVERED-L4", "F-MS2-3": "SILENT", "F-MS2-4": "SILENT", "F-MS2-2": "REGISTERED_NOT_EXECUTED", "worst_S4": 2e-13 + eps}}
    return ck

def run(chat, cc, S):
    R = compare(chat, cc, S); return R, R.summary()

def selftest():
    S, h = load_schema(SCHEMA_DEFAULT); suites = []
    def suite(name, mut, expect_miss_min=1, expect_pass=False):
        a, b = canonical_checkpoint("chat", S), canonical_checkpoint("cc", S); mut(a, b); R, s = run(a, b, S)
        ok = (s["miss"] == 0) if expect_pass else (s["miss"] >= expect_miss_min); suites.append((name, ok, s)); return R
    suite("S1 canonical legs (1e-9 jitter on cc) -> ALL PASS", lambda a, b: None, expect_pass=True)
    suite("S2 a Phase-0 control fails on cc (passed false) -> C1 miss + verdict recompute INDETERMINATE", lambda a, b: b["phase0"]["F-CTRL-C4"].__setitem__("passed", False), 2)
    suite("S3 passed true but float violates its rule (PIN-K2 hex 2e-4) -> C1 miss", lambda a, b: a["phase0"]["PIN-K2"].__setitem__("worst_rel_hex_kappa2", 2e-4), 1)
    suite("S4 missing required key (phase2) on chat", lambda a, b: a.pop("phase2"), 1)
    suite("S5 wrong election code", lambda a, b: a["elections"].__setitem__("E-MS2-3", "b"), 1)
    suite("S6 T1 scan HIT on memo (cc)", lambda a, b: b["t1_scan"].__setitem__("memo", "HIT"), 1)
    suite("S7 identical instrument md5 (independence witness)", lambda a, b: b.__setitem__("instrument_md5", a["instrument_md5"]), 1)
    suite("S8 provenance md5 mismatch (x6 chat)", lambda a, b: a.__setitem__("x6_chat_md5", "deadbeef" * 4), 1)
    suite("S9 r_agg array disagrees at 1e-5 on one key", lambda a, b: b["phase2"]["hex_step|a"]["r_agg_E2_VRH"].__setitem__(9, b["phase2"]["hex_step|a"]["r_agg_E2_VRH"][9] + 1e-5), 1)
    suite("S10 kappa44 disagrees at 1e-3 relative", lambda a, b: b["phase2"]["cubic_step|001"].__setitem__("kappa44_E2", a["phase2"]["cubic_step|001"]["kappa44_E2"] * 1.001), 1)
    suite("S11 kappa null compares as null (both legs 1e-8 vs 3e-8: within the floor) -> PASS", lambda a, b: (a["phase2"]["hex_gem8|b"].__setitem__("kappa44_h", 1e-8), b["phase2"]["hex_gem8|b"].__setitem__("kappa44_h", 3e-8)), expect_pass=True)
    suite("S12 S4 breach on one leg (3e-6) -> C2 abs miss + C3 verdict/F-MS2-3 misses", lambda a, b: a["phase2"]["hex_step|a"].__setitem__("S4_E2", 3e-6), 2)
    suite("S13 verdict inconsistent with states (both report L4-NULL while cubic kappa44 is 3e-3)", lambda a, b: (a["phase3"].__setitem__("verdict_class", "L4-NULL"), b["phase3"].__setitem__("verdict_class", "L4-NULL")), 2)
    def l4null(a, b):
        for ck in (a, b):
            for k in ("cubic_step|001", "cubic_gem8|001"):
                ck["phase2"][k]["kappa44_E2"] = 1e-8; ck["phase2"][k]["quadform"]["kappa44"] = 1e-8; ck["phase2"][k]["halving_dev_kappa44"] = 1e-9
            ck["phase3"]["verdict_class"] = "L4-NULL"; ck["phase3"]["F-MS2-4"] = "FIRES"
    suite("S14 genuine L4-NULL on both legs, consistently reported -> ALL PASS", l4null, expect_pass=True)
    suite("S15 cubic quadform kappa22 not null (1e-6) on cc -> miss", lambda a, b: b["phase2"]["cubic_gem8|111"]["quadform"].__setitem__("kappa22", 1e-6), 1)
    suite("S16 halving deviation above floor and relative bound (cc)", lambda a, b: b["phase2"]["hex_step|b"].__setitem__("halving_dev_kappa44", 5e-6), 1)
    suite("S17 array wrong length (11) on chat", lambda a, b: a["phase2"]["hex_gem8|a"].__setitem__("lambda_mean_t4", a["phase2"]["hex_gem8|a"]["lambda_mean_t4"][:11]), 1)
    suite("S18 F-CTRL-TEX4 float below its gt threshold (instrument blind) -> C1 miss", lambda a, b: a["phase0"]["F-CTRL-TEX4"].__setitem__("r_agg_t1_abs", 1e-9), 1)
    allok = all(ok for _, ok, _ in suites)
    print(f"schema md5 {h}")
    for name, ok, s in suites: print(f"  [{'PASS' if ok else 'FAIL'}] {name}  (checks={s['checks']}, pass={s['pass']}, miss={s['miss']})")
    print("SELFTEST", "PASS" if allok else "FAIL"); return 0 if allok else 1

def main():
    if len(sys.argv) < 2: print(__doc__); return 2
    if sys.argv[1] == "selftest": return selftest()
    if sys.argv[1] == "compare":
        args = sys.argv[2:]; schema = SCHEMA_DEFAULT; out = None
        if "--schema" in args: i = args.index("--schema"); schema = args[i + 1]; del args[i:i + 2]
        if "--out" in args: i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
        if len(args) != 2: print(__doc__); return 2
        S, h = load_schema(schema); chat = json.load(open(args[0], encoding="utf-8")); cc = json.load(open(args[1], encoding="utf-8"))
        R, s = run(chat, cc, S)
        res = {"comparator": "g_mscs2_compare_v1_0", "schema_md5": h, "chat_ckpt_md5": md5_file(args[0]), "cc_ckpt_md5": md5_file(args[1]), "summary": s, "misses": [r for r in R.rows if not r["pass"]], "rows": R.rows}
        txt = json.dumps(res, indent=1, ensure_ascii=False, sort_keys=True)
        if out: open(out, "w", encoding="utf-8").write(txt)
        print(f"G-MSCS2 two-leg comparison: checks={s['checks']} pass={s['pass']} miss={s['miss']}")
        for r in res["misses"]: print(f"  MISS [{r['check']}] {r['name']}: chat={r['chat']} cc={r['cc']} {r['note']}")
        return 0 if s["miss"] == 0 else 1
    print(__doc__); return 2

if __name__ == "__main__":
    sys.exit(main())
=====END-EMBED name=g_mscs2_compare_v1_0.py=====

=====BEGIN-EMBED name=tools/t1/T1_forbidden_G_MSCS2.txt md5=be921b8c29f7578e85ed92f1450c1956 bytes=1695 encoding=raw=====
# T1 forbidden-string list — Gate G-MSCS2 (gate-specific), composed September 26, 2026
# Stratum 1: the author's base list (T1_base_author_20260919.txt, md5 05302210cc4ceb70553acbe8379e9fc3, 143 B, 11 pattern lines) — the operative base by the author's election of September 23, 2026 (E-MS2-7).
# Provenance note: the G-2a-L1 list 04438b74 (117 B, 13 patterns) was RECOVERED on main at PR #13 (g2a_l1_gate/t1_forbidden_G_2a_L1.txt); it shares no pattern with the base and is a gate-specific vocabulary quarantine — NOT used here (author's election). H-MS-0 (G-MSCS1) stands as sharpened in the V4.85 housekeeping note.
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
# Stratum 2: the G-MSCS1 observational stratum, verbatim (the 25 patterns of T1_forbidden_G_MSCS1.txt fef2827100d3f85e0a6341b44f0c00bf beyond the base): SI speed of light in scientific form, the 2017 multi-messenger tensor-speed bound digit strings, SI speed units, event/collaboration/instrument identifiers, observational-search identifiers, the anisotropic-dispersion coefficient names of the observational dialect. No G-MSCS2-specific stratum (none foreseen at staging).
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
=====END-EMBED name=tools/t1/T1_forbidden_G_MSCS2.txt=====

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

=====BEGIN-EMBED name=inputs/g_mscs1_chatleg_checkpoint.json md5=c04c0b8ea34cfe60f231aa06828e6ce4 bytes=33289 encoding=raw=====
{
 "gate": "G-MSCS1",
 "leg": "chat",
 "instrument": "g_mscs1_chatleg.py",
 "instrument_md5": "db5f51dd9ef7f54dd0826991d594681b",
 "memo_md5": "3f30262eaec461fb5fd3202835f7de37",
 "memo_bytes": 34837,
 "ledger_base_md5": "d095a7003bb0d4c177e7451e1d14c4c6",
 "utc": "2026-09-19T22:54:03.606899+00:00",
 "elections": {
  "E-MS-1": "(a) two descriptors of the one transverse field; S2-E2 primary, S2-h second arm",
  "E-MS-2": "(a) all four configurations",
  "E-MS-2b": "(a+b) banked tetragonal-form primary; symmetrized C66 second arm",
  "E-MS-2c": "(001+111) <001> primary, <111> reported",
  "E-MS-3": "(a) VRH/HS leading order; Born at t = 0 only; texture sweep",
  "E-MS-4": "(a) table + lambda_L",
  "E-MS-5": "(a) fiber ODF 1 + t P2, t in [-1, 2]",
  "E-MS-6": "(a) no observational contact"
 },
 "T1": {
  "list_md5": "fef2827100d3f85e0a6341b44f0c00bf",
  "state": "CLEAN",
  "numeric_collisions": 0,
  "files": [
   "g_mscs1_chatleg.py",
   "staging_memo_G_MSCS1_v2.md"
  ]
 },
 "inputs": {
  "X1_md5": "200e7a8b775577564369c6924d38a84c",
  "X1_bytes": 2767,
  "X3_md5": "aaae206733b0f0a378a5c6b600274d3f",
  "X4_md5": "ec87e42f0f617b00c4985ba2aceac339",
  "X5_md5": "df413a7cfa30e599b779af8fee5d07d1"
 },
 "quadrature": {
  "n_theta": 64,
  "n_phi": 128,
  "doubling_residual": 1.7763568394002505e-15,
  "so3_grid": [
   16,
   10,
   16
  ],
  "n_grid": [
   12,
   24
  ]
 },
 "t_grid": [
  -0.5,
  -0.25,
  -0.1,
  -0.05,
  -0.02,
  0.0,
  0.02,
  0.05,
  0.1,
  0.25,
  0.5,
  1.0
 ],
 "controls": {
  "F-CTRL-ISO": {
   "r_xtal_E2": 2.220446049250313e-16,
   "r_xtal_h": 0.0,
   "lambda_max": 5.8657280953489826e-31,
   "r_agg_max": 4.440892098500626e-16,
   "passed": true
  },
  "F-CTRL-SO3": {
   "w_S2_mean_t0": 0.39999999999999997,
   "dev_from_0p4": 4.996003610813204e-16,
   "r_agg_0_E2": 0.0,
   "passed": true
  },
  "F-CTRL-TEX": {
   "r_agg_t1": 0.0025019145217410887,
   "passed": true
  },
  "PIN-A2AGG": {
   "worst_rel_residual": 6.275451101635372e-14,
   "passed": true
  },
  "F-CTRL-POL": {
   "split_plus_minus": 0.0,
   "split_plus_avg": 4.799045625554363e-16,
   "passed": true
  },
  "F-CTRL-ADMIX": {
   "r_xtal_h_projected": 0.0,
   "passed": true
  },
  "PIN-VRH0": {
   "worst_rel_residual": 1.3982193552955251e-14,
   "passed": true
  },
  "PIN-HS0": {
   "worst_rel_residual": 1.601689060021389e-12,
   "passed": true
  }
 },
 "pins_vrh0": {
  "hex_step": {
   "GV": 73.06453333333313,
   "GR": 68.69659702931501,
   "KV": 134.60928888888833,
   "KR": 134.60823359538983,
   "worst_rel": 4.222845193672222e-15,
   "G_HS": [
    70.40652703753862,
    70.97358894132181
   ],
   "hs_ref": {
    "hi": [
     135.36659528369762,
     115.55987328919902
    ],
    "lo": [
     134.60708943712606,
     60.03080000143797
    ]
   }
  },
  "hex_gem8": {
   "GV": 105.041953333333,
   "GR": 96.63040078152201,
   "KV": 229.69615555555526,
   "KR": 229.69594530872757,
   "worst_rel": 1.3982193552955251e-14,
   "G_HS": [
    99.81834260496358,
    101.05874270190839
   ],
   "hs_ref": {
    "hi": [
     230.1360483907313,
     178.29434175576765
    ],
    "lo": [
     229.69575433586576,
     84.82450000231091
    ]
   }
  },
  "cubic_step": {
   "GV": 65.86612000000007,
   "GR": 55.78412874515959,
   "KV": 123.83246666666679,
   "KR": 123.83246666666577,
   "worst_rel": 7.688833886201092e-15,
   "G_HS": [
    60.196098807713454,
    61.904684503125985
   ],
   "hs_ref": {
    "hi": [
     123.83246666609068,
     85.29339999914612
    ],
    "lo": [
     123.83246666724266,
     36.72520000086347
    ]
   },
   "hs_band_rel": 8.404305891603147e-13
  },
  "cubic_gem8": {
   "GV": 97.46609999999977,
   "GR": 75.80787043785469,
   "KV": 210.27549999999948,
   "KR": 210.27549999999925,
   "worst_rel": 3.784596227574358e-15,
   "G_HS": [
    84.85580496777382,
    89.43210619954085
   ],
   "hs_ref": {
    "hi": [
     210.2754999990931,
     131.54359999864414
    ],
    "lo": [
     210.27550000090693,
     46.34985000135914
    ]
   },
   "hs_band_rel": 1.601689060021389e-12
  }
 },
 "born_t0": {
  "hex_step": {
   "D0_plus": -0.02052824459532726,
   "D0_minus": -0.02052824459532726,
   "D0_avg": -0.02052824459532726,
   "D2_avg": -0.018347663163946017,
   "D2_plus": -0.01834766316394601,
   "D2_minus": -0.01834766316394601,
   "a2agg_residual_rel": 9.076548452285695e-15,
   "I0_TT": 362.2844803374222,
   "I0_TL": 241.57169884554065,
   "I2_TT": 123.43047361632915,
   "I2_TL": 83.80274060401825,
   "V_T": 8.547779438739228,
   "V_L": 15.232487212095924
  },
  "hex_gem8": {
   "D0_plus": -0.02891780760307181,
   "D0_minus": -0.02891780760307181,
   "D0_avg": -0.028917807603071825,
   "D2_avg": -0.025933693584294384,
   "D2_plus": -0.025933693584294374,
   "D2_minus": -0.025933693584294374,
   "a2agg_residual_rel": 7.357979369086492e-15,
   "I0_TT": 1073.0614422363028,
   "I0_TL": 715.3892819892385,
   "I2_TT": 364.295965349171,
   "I2_TL": 247.56667439133207,
   "V_T": 10.248997674569596,
   "V_L": 19.228938954953616
  },
  "cubic_step": {
   "D0_plus": -0.03151342243433812,
   "D0_minus": -0.03151342243433812,
   "D0_avg": -0.03151342243433812,
   "D2_avg": -0.028537471107946306,
   "D2_plus": -0.028537471107946306,
   "D2_minus": -0.028537471107946306,
   "a2agg_residual_rel": 3.2825286917824895e-15,
   "I0_TT": 452.9030498380803,
   "I0_TL": 301.93536655872015,
   "I2_TT": 157.12962953566074,
   "I2_TL": 108.86105052797411,
   "V_T": 8.115794477437195,
   "V_L": 14.54833186313813
  },
  "cubic_gem8": {
   "D0_plus": -0.04367714392697779,
   "D0_minus": -0.04367714392697779,
   "D0_avg": -0.043677143926977795,
   "D2_avg": -0.039713976791286285,
   "D2_plus": -0.03971397679128628,
   "D2_minus": -0.03971397679128628,
   "a2agg_residual_rel": 4.542764439072047e-15,
   "I0_TT": 1393.5312074999997,
   "I0_TL": 929.0208049999997,
   "I2_TT": 483.47001076530677,
   "I2_TL": 334.95307935374194,
   "V_T": 9.87249208660102,
   "V_L": 18.445332743000304
  }
 },
 "phase1": {
  "hex_step|a": {
   "v_EM": 8.498926630589143,
   "v_S2E2": 8.261235391127114,
   "v_S2h": 8.489468358289109,
   "r_xtal_E2": -0.02796720689487253,
   "r_xtal_h": -0.001112878450555299,
   "lambda_mean": 0.004808575724022838,
   "lambda_max": 0.03353758299774612,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.036444417932560425,
   "share_EM": {
    "qSH": 0.49999999946246804,
    "qSV": 0.4951914248135092,
    "qL": 0.004808575724022834
   },
   "share_S2E2": {
    "qSH": 0.83333320610945,
    "qSV": 0.16464005343946514,
    "qL": 0.0020267404510848717
   },
   "doubling_r_xtal_E2": 7.771561172376096e-16
  },
  "hex_step|b": {
   "v_EM": 8.49913805976472,
   "v_S2E2": 8.261611551328288,
   "v_S2h": 8.489680210591468,
   "r_xtal_E2": -0.027947129081346778,
   "r_xtal_h": -0.0011128009813166084,
   "lambda_mean": 0.004808600428348514,
   "lambda_max": 0.033534547685208825,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.03644303566084012,
   "share_EM": {
    "qSH": 0.5,
    "qSV": 0.49519139957165154,
    "qL": 0.004808600428348502
   },
   "share_S2E2": {
    "qSH": 0.8333333333333336,
    "qSV": 0.16464001815350915,
    "qL": 0.002026648513157485
   },
   "doubling_r_xtal_E2": 6.661338147750939e-16
  },
  "hex_gem8|a": {
   "v_EM": 10.167571147427779,
   "v_S2E2": 9.767584615679638,
   "v_S2h": 10.154202161568202,
   "r_xtal_E2": -0.039339437703303504,
   "r_xtal_h": -0.0013148652382883874,
   "lambda_mean": 0.0049537696180639535,
   "lambda_max": 0.03513301845903744,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.05132899179683144,
   "share_EM": {
    "qSH": 0.49999999908685466,
    "qSV": 0.49504623129508146,
    "qL": 0.004953769618063935
   },
   "share_S2E2": {
    "qSH": 0.8333322334753969,
    "qSV": 0.16452961765676766,
    "qL": 0.002138148867835594
   },
   "doubling_r_xtal_E2": 6.661338147750939e-16
  },
  "hex_gem8|b": {
   "v_EM": 10.167412388965342,
   "v_S2E2": 9.767300819096656,
   "v_S2h": 10.154042977980577,
   "r_xtal_E2": -0.03935234989611769,
   "r_xtal_h": -0.0013149275816995987,
   "lambda_mean": 0.004953789932329422,
   "lambda_max": 0.035133018459037525,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.05133043709649301,
   "share_EM": {
    "qSH": 0.5,
    "qSV": 0.4950462100676707,
    "qL": 0.004953789932329417
   },
   "share_S2E2": {
    "qSH": 0.8333333333333337,
    "qSV": 0.16452845141380396,
    "qL": 0.002138215252862705
   },
   "doubling_r_xtal_E2": 4.440892098500626e-16
  },
  "cubic_step|001": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 7.889264216956222,
   "v_S2h": 8.015951162831872,
   "r_xtal_E2": -0.0172967677412158,
   "r_xtal_h": -0.001516377102324551,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173741,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.04901957894779367,
   "share_EM": {
    "qT1": 0.4992967361164542,
    "qT2": 0.49231094485466753,
    "qL": 0.008392319028878298
   },
   "share_S2E2": {
    "qT1": 0.4488023208911163,
    "qT2": 0.5426280022478344,
    "qL": 0.008569676861049398
   },
   "doubling_r_xtal_E2": 1.1102230246251565e-15
  },
  "cubic_step|111": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 8.120698567854001,
   "v_S2h": 8.015951162831872,
   "r_xtal_E2": 0.01153117849414409,
   "r_xtal_h": -0.001516377102324551,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173741,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.04901957894779367,
   "share_EM": {
    "qT1": 0.4992967361164542,
    "qT2": 0.49231094485466753,
    "qL": 0.008392319028878298
   },
   "share_S2E2": {
    "qT1": 0.5330407329981224,
    "qT2": 0.45868518652777995,
    "qL": 0.00827408047409754
   },
   "doubling_r_xtal_E2": 2.220446049250313e-16
  },
  "cubic_gem8|001": {
   "v_EM": 9.72117101507821,
   "v_S2E2": 9.5185580718033,
   "v_S2h": 9.703234472528251,
   "r_xtal_E2": -0.020842442022740326,
   "r_xtal_h": -0.0018451010194284745,
   "lambda_mean": 0.0093105038596528,
   "lambda_max": 0.043292701954120015,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.07221172083386433,
   "share_EM": {
    "qT1": 0.49922505755529545,
    "qT2": 0.49146443858505184,
    "qL": 0.009310503859652788
   },
   "share_S2E2": {
    "qT1": 0.44874904568984914,
    "qT2": 0.5417581722353867,
    "qL": 0.009492782074764219
   },
   "doubling_r_xtal_E2": 1.7763568394002505e-15
  },
  "cubic_gem8|111": {
   "v_EM": 9.72117101507821,
   "v_S2E2": 9.856246310594818,
   "v_S2h": 9.703234472528251,
   "r_xtal_E2": 0.01389496134849355,
   "r_xtal_h": -0.0018451010194284745,
   "lambda_mean": 0.0093105038596528,
   "lambda_max": 0.043292701954120015,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.07221172083386433,
   "share_EM": {
    "qT1": 0.49922505755529545,
    "qT2": 0.49146443858505184,
    "qL": 0.009310503859652788
   },
   "share_S2E2": {
    "qT1": 0.5329595958441811,
    "qT2": 0.4578514191062405,
    "qL": 0.009188985049578388
   },
   "doubling_r_xtal_E2": 2.220446049250313e-16
  }
 },
 "phase2": {
  "hex_step|a": {
   "vT_VRH": 8.419059637591603,
   "vT_V": 8.547779438739228,
   "vT_R": 8.288341029983927,
   "vT_HS_lo": 8.390859731728247,
   "vT_HS_hi": 8.424582419403457,
   "r_agg_E2_VRH": [
    -0.00035977898386985174,
    -8.995485659324398e-05,
    -1.4393819487867887e-05,
    -3.5985447373043655e-06,
    -5.757759000690754e-07,
    0.0,
    -5.757876907486192e-07,
    -3.5987289647154697e-06,
    -1.4395293312707835e-05,
    -8.997788565123788e-05,
    -0.0003599632319449819,
    -0.001440311666697669
   ],
   "r_agg_h_VRH": [
    -4.97443568558964e-07,
    -1.249121053259472e-07,
    -2.0039163883822653e-08,
    -5.014240023193395e-09,
    -8.027059017479132e-10,
    0.0,
    -8.03276667404873e-10,
    -5.023157112482579e-09,
    -2.0110500931203035e-08,
    -1.260267620262212e-07,
    -5.063613528477617e-07,
    -2.043685221497782e-06
   ],
   "r_agg_E2_HS": [
    -0.0003571461079143745,
    -8.927425424842816e-05,
    -1.4282679909993767e-05,
    -3.5705689754861325e-06,
    -5.71281304040383e-07,
    0.0,
    -5.712682860092855e-07,
    -3.570365567528988e-06,
    -1.4281052650555459e-05,
    -8.924882879379759e-05,
    -0.0003569427177455564,
    -0.001427336256063394
   ],
   "r_agg_E2_V": [
    -0.00044489345330223085,
    -0.00011129506285811885,
    -1.7814259669179933e-05,
    -4.4541593531288726e-06,
    -7.127228306424982e-07,
    0.0,
    -7.12799589352997e-07,
    -4.455358709520851e-06,
    -1.782385456405855e-05,
    -0.00011144498796067381,
    -0.0004460929933972624,
    -0.0017869833104871002
   ],
   "r_agg_E2_R": [
    -0.0002692160058006543,
    -6.725248904060344e-05,
    -1.0755531967165943e-05,
    -2.6884807549087952e-06,
    -4.301184323152185e-07,
    -2.220446049250313e-16,
    -4.300672613588574e-07,
    -2.687681208590753e-06,
    -1.0749135596066495e-05,
    -6.715254554567895e-05,
    -0.00026841645213737664,
    -0.0010721651905468699
   ],
   "S_t_E2": 1.6266231256261696e-13,
   "S_t_h": 4.563941055176853e-15,
   "kappa2_E2": -0.0014394617694966992,
   "kappa2_h": -2.0075101981637655e-06,
   "kappa3_E2": -7.369324458207498e-07,
   "kappa2_E2_HS": -0.0014281847168633966,
   "kappa2_E2_4term": -0.0014394544404300721,
   "S_t_E2_4term": 1.6265790021720394e-13,
   "kappa4_E2_4term": -1.1996041223777304e-07,
   "fit_residual": 3.04965357812358e-11,
   "fit_residual_4term": 3.3973616694016385e-15,
   "halving_dev_kappa2": 4.296077191089223e-06,
   "kappa2_E2_window0p1": -0.0014394555854578238,
   "lambda_mean_t": [
    2.5111906360924555e-06,
    6.283852379843875e-07,
    1.0059951851654784e-07,
    2.5154764402907355e-08,
    4.025233601588008e-09,
    1.8167378864124917e-30,
    4.025864750027318e-09,
    2.5164626100033596e-08,
    1.0067841215238367e-07,
    6.296179578773908e-07,
    2.521052590656771e-06,
    1.0105781771545095e-05
   ],
   "hs_ref": {
    "hi": [
     135.36659528369762,
     115.55987328919902
    ],
    "lo": [
     134.60708943712606,
     60.03080000143797
    ]
   }
  },
  "hex_step|b": {
   "vT_VRH": 8.419278648579612,
   "vT_V": 8.547982997955295,
   "vT_R": 8.288576029181627,
   "vT_HS_lo": 8.391084746837947,
   "vT_HS_hi": 8.424803257723832,
   "r_agg_E2_VRH": [
    -0.000359589205973343,
    -8.990741528092094e-05,
    -1.4386229051588373e-05,
    -3.5966471373383158e-06,
    -5.754722848250182e-07,
    0.0,
    -5.754840760596736e-07,
    -3.596831374630405e-06,
    -1.4387702956364379e-05,
    -8.993044558192054e-05,
    -0.00035977346397653154,
    -0.0014395524516434
   ],
   "r_agg_h_VRH": [
    -4.969233557972075e-07,
    -1.2478124211678931e-07,
    -2.0018147695033406e-08,
    -5.0089790093466036e-09,
    -8.018634645168277e-10,
    0.0,
    -8.024334530176702e-10,
    -5.017882886981795e-09,
    -2.0089378716114936e-08,
    -1.2589424946973793e-07,
    -5.058279419767331e-07,
    -2.041524180040888e-06
   ],
   "r_agg_E2_HS": [
    -0.0003569546896101672,
    -8.922641129294195e-05,
    -1.4275026188892426e-05,
    -3.5686556428826677e-06,
    -5.70975180358424e-07,
    0.0,
    -5.709621745397797e-07,
    -3.5684524321011324e-06,
    -1.4273400507525125e-05,
    -8.92010104921459e-05,
    -0.00035675149663971784,
    -0.0014265718105259673
   ],
   "r_agg_E2_V": [
    -0.0004447026316007907,
    -0.00011124729747324924,
    -1.7806611237514147e-05,
    -4.452246738839705e-06,
    -7.124167632488465e-07,
    0.0,
    -7.124934562341423e-07,
    -4.4534450686084526e-06,
    -1.7816197920628163e-05,
    -0.0001113970942586695,
    -0.00044590114491716015,
    -0.0017862135883479624
   ],
   "r_agg_E2_R": [
    -0.0002690281488036961,
    -6.720559786976832e-05,
    -1.0748036230245894e-05,
    -2.686607384894124e-06,
    -4.298187469276016e-07,
    -2.220446049250313e-16,
    -4.297676474696033e-07,
    -2.6858089564596455e-06,
    -1.0741648802214954e-05,
    -6.710579410051931e-05,
    -0.000268229712959811,
    -0.0010714202639685588
   ],
   "S_t_E2": 1.6125034658616313e-13,
   "S_t_h": 6.550087858874976e-15,
   "kappa2_E2": -0.001438702718749083,
   "kappa2_h": -2.0054031941127916e-06,
   "kappa3_E2": -7.369721996574744e-07,
   "kappa2_E2_HS": -0.0014274194267221226,
   "kappa2_E2_4term": -0.0014386954029739513,
   "S_t_E2_4term": 1.6124593656681758e-13,
   "kappa4_E2_4term": -1.1974286021456171e-07,
   "fit_residual": 3.04412293281627e-11,
   "fit_residual_4term": 3.330880835213012e-15,
   "halving_dev_kappa2": 4.290548556187453e-06,
   "kappa2_E2_window0p1": -0.0014386965459252104,
   "lambda_mean_t": [
    2.5086422130892723e-06,
    6.277474540246005e-07,
    1.0049740414358128e-07,
    2.512922990624887e-08,
    4.021147509275336e-09,
    2.8493087979525507e-30,
    4.0217778869806965e-09,
    2.5139079553542238e-08,
    1.005762013941085e-07,
    6.289786678735804e-07,
    2.5184921186771055e-06,
    1.0095510979328715e-05
   ],
   "hs_ref": {
    "hi": [
     135.36659528369762,
     115.55987328919902
    ],
    "lo": [
     134.60708943712606,
     60.03080000143797
    ]
   }
  },
  "hex_gem8|a": {
   "vT_VRH": 10.041721817369147,
   "vT_V": 10.248997674569596,
   "vT_R": 9.830076336505329,
   "vT_HS_lo": 9.990913001571156,
   "vT_HS_hi": 10.052797754949037,
   "r_agg_E2_VRH": [
    -0.00047377007967119855,
    -0.0001184586706243218,
    -1.8955103105455784e-05,
    -4.7389256596641616e-06,
    -7.582427594687857e-07,
    -2.220446049250313e-16,
    -7.582626075919308e-07,
    -4.7392357853670575e-06,
    -1.8957584126733096e-05,
    -0.00011849743822145431,
    -0.00047408026726247776,
    -0.0018971495594123367
   ],
   "r_agg_h_VRH": [
    -8.038770585860888e-07,
    -2.0201977346534505e-07,
    -3.242488200161375e-08,
    -8.11473377382299e-09,
    -1.299176211055908e-09,
    0.0,
    -1.3002692256236514e-09,
    -8.131815554257571e-09,
    -3.256153702224651e-08,
    -2.041550737352793e-07,
    -8.209613446830133e-07,
    -3.3191570847357355e-06
   ],
   "r_agg_E2_HS": [
    -0.00047147218794019174,
    -0.00011785019986731982,
    -1.885426634828935e-05,
    -4.71341728180974e-06,
    -7.541323487902929e-07,
    -2.220446049250313e-16,
    -7.54113030021486e-07,
    -4.713115426713266e-06,
    -1.8851851520729213e-05,
    -0.00011781246964737146,
    -0.0004711703880158069,
    -0.0018840138120467254
   ],
   "r_agg_E2_V": [
    -0.0005816603154129574,
    -0.00014553490980062644,
    -2.3297462136029345e-05,
    -5.8253708745681365e-06,
    -9.321564546915795e-07,
    0.0,
    -9.322866439953614e-07,
    -5.8274050896978125e-06,
    -2.331373598807307e-05,
    -0.00014578920292729336,
    -0.0005836950659862117,
    -0.002339328010586894
   ],
   "r_agg_E2_R": [
    -0.00035643481654545894,
    -8.901723504473047e-05,
    -1.4234158591031054e-05,
    -3.557830641987003e-06,
    -5.691851292510819e-07,
    2.220446049250313e-16,
    -5.690951039305503e-07,
    -3.5564239939667175e-06,
    -1.4222905402316854e-05,
    -8.88414034126983e-05,
    -0.0003550281474846706,
    -0.00141752637341086
   ],
   "S_t_E2": 4.894642365145396e-13,
   "S_t_h": 1.9849252759426836e-14,
   "kappa2_E2": -0.0018956484826701352,
   "kappa2_h": -3.2493966959289463e-06,
   "kappa3_E2": -1.24057090180438e-06,
   "kappa2_E2_HS": -0.0018853014774839155,
   "kappa2_E2_4term": -0.001895631597971673,
   "S_t_E2_4term": 4.894584258277063e-13,
   "kappa4_E2_4term": -2.763647120625483e-07,
   "fit_residual": 7.025789764898445e-11,
   "fit_residual_4term": 1.0214700603304965e-14,
   "halving_dev_kappa2": 7.51551994532953e-06,
   "kappa2_E2_window0p1": -0.0018956342358861544,
   "lambda_mean_t": [
    3.6006634946247986e-06,
    9.011863601809301e-07,
    1.4429157576509233e-07,
    3.608153193406747e-08,
    5.773880433588238e-09,
    2.8730624380705302e-30,
    5.775001291440091e-09,
    3.6099045346764643e-08,
    1.444316833663885e-07,
    9.033755744645923e-07,
    3.618178152703809e-06,
    1.4512512141033628e-05
   ],
   "hs_ref": {
    "hi": [
     230.1360483907313,
     178.29434175576765
    ],
    "lo": [
     229.69575433586576,
     84.82450000231091
    ]
   }
  },
  "hex_gem8|b": {
   "vT_VRH": 10.041554085160632,
   "vT_V": 10.248847414872234,
   "vT_R": 9.82989031256601,
   "vT_HS_lo": 9.99073982971986,
   "vT_HS_hi": 10.052629959294945,
   "r_agg_E2_VRH": [
    -0.0004738923403120321,
    -0.00011848923252755217,
    -1.895999284384775e-05,
    -4.740148086490592e-06,
    -7.584383474590339e-07,
    0.0,
    -7.584581946940006e-07,
    -4.740458205976239e-06,
    -1.8962473815165026e-05,
    -0.00011852799934297664,
    -0.0004742025216768475,
    -0.0018976387487924518
   ],
   "r_agg_h_VRH": [
    -8.04256157782568e-07,
    -2.021152383235858e-07,
    -3.2440223618479536e-08,
    -8.118574701398984e-09,
    -1.2997911635892478e-09,
    0.0,
    -1.3008849553131085e-09,
    -8.13566802815302e-09,
    -3.2576969677400314e-08,
    -2.0425195845774624e-07,
    -8.213518059019265e-07,
    -3.320743002910298e-06
   ],
   "r_agg_E2_HS": [
    -0.0004715958998675607,
    -0.0001178811207174224,
    -1.885921295863291e-05,
    -4.714653872306407e-06,
    -7.543301969725746e-07,
    -3.3306690738754696e-16,
    -7.543108705432289e-07,
    -4.714351890200419e-06,
    -1.8856797115107682e-05,
    -0.00011784337463216499,
    -0.00047129397306711063,
    -0.0018845078483341604
   ],
   "r_agg_E2_V": [
    -0.0005817817193016772,
    -0.00014556530971254755,
    -2.3302331052743597e-05,
    -5.826588524215914e-06,
    -9.323513193715272e-07,
    -2.220446049250313e-16,
    -9.324815636313488e-07,
    -5.828623595549587e-06,
    -2.3318611752976004e-05,
    -0.00014581970985627635,
    -0.0005838173263492674,
    -0.0023398190658678875
   ],
   "r_agg_E2_R": [
    -0.0003565570229338011,
    -8.904772300111219e-05,
    -1.423903074149191e-05,
    -3.5590481938241325e-06,
    -5.693798912353998e-07,
    -2.220446049250313e-16,
    -5.692898042974903e-07,
    -3.557640585682975e-06,
    -1.422776987347607e-05,
    -8.887177138017233e-05,
    -0.0003551493939385475,
    -0.0014180096723556135
   ],
   "S_t_E2": 4.895751529361098e-13,
   "S_t_h": 1.861754403597132e-14,
   "kappa2_E2": -0.0018961374665242264,
   "kappa2_h": -3.2509354903061167e-06,
   "kappa3_E2": -1.240545889104786e-06,
   "kappa2_E2_HS": -0.0018857960842583088,
   "kappa2_E2_4term": -0.001896120566862326,
   "S_t_E2_4term": 4.895693407496872e-13,
   "kappa4_E2_4term": -2.766096300511605e-07,
   "fit_residual": 7.032016110210891e-11,
   "fit_residual_4term": 1.0163106401516192e-14,
   "halving_dev_kappa2": 7.520240357827345e-06,
   "kappa2_E2_window0p1": -0.0018961232071147266,
   "lambda_mean_t": [
    3.6022883240770764e-06,
    9.015930248247842e-07,
    1.4435669065055046e-07,
    3.609781489575608e-08,
    5.7764861216668656e-09,
    1.2842490776280975e-31,
    5.777607540357807e-09,
    3.611533707604357e-08,
    1.4449686840147292e-07,
    9.037833352239438e-07,
    3.6198117522104935e-06,
    1.4519069924274029e-05
   ],
   "hs_ref": {
    "hi": [
     230.1360483907313,
     178.29434175576765
    ],
    "lo": [
     229.69575433586576,
     84.82450000231091
    ]
   }
  },
  "cubic_step|001": {
   "vT_VRH": 7.799046375844923,
   "vT_V": 8.115794477437195,
   "vT_R": 7.468877341686607,
   "vT_HS_lo": 7.758614490211087,
   "vT_HS_hi": 7.867953005904775,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    2.220446049250313e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    -1.1102230246251565e-16,
    2.220446049250313e-16,
    0.0,
    -1.1102230246251565e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "r_agg_E2_HS": [
    2.220446049250313e-16,
    0.0,
    2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    -1.1102230246251565e-16,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    -1.1102230246251565e-16,
    -2.220446049250313e-16,
    0.0
   ],
   "r_agg_E2_V": [
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    2.220446049250313e-16,
    0.0
   ],
   "r_agg_E2_R": [
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0
   ],
   "S_t_E2": 3.872699649800502e-16,
   "S_t_h": 2.7381760509747877e-16,
   "kappa2_E2": 3.141702123932416e-15,
   "kappa2_h": -3.458500796931401e-17,
   "kappa3_E2": -6.308626889222545e-15,
   "kappa2_E2_HS": -4.606723061512521e-16,
   "kappa2_E2_4term": -1.4860741481801268e-14,
   "S_t_E2_4term": 3.872699649800578e-16,
   "kappa4_E2_4term": 2.946596976449254e-13,
   "fit_residual": 8.549374687587548e-17,
   "fit_residual_4term": 4.1204862127242437e-17,
   "halving_dev_kappa2": 4.802491637841732,
   "kappa2_E2_window0p1": -1.194629605484262e-14,
   "lambda_mean_t": [
    2.8112615174278626e-30,
    1.9079063183926423e-31,
    2.534920485447341e-30,
    1.979885257559672e-30,
    2.173629477557336e-30,
    4.258392291069694e-32,
    7.083137335193975e-31,
    2.8979386817414475e-31,
    2.106564088504244e-31,
    4.975216689832133e-31,
    2.6091436397777845e-30,
    3.806067177046203e-30
   ],
   "hs_ref": {
    "hi": [
     123.83246666609068,
     85.29339999914612
    ],
    "lo": [
     123.83246666724266,
     36.72520000086347
    ]
   }
  },
  "cubic_step|111": {
   "vT_VRH": 7.799046375844923,
   "vT_V": 8.115794477437195,
   "vT_R": 7.468877341686607,
   "vT_HS_lo": 7.758614490211087,
   "vT_HS_hi": 7.867953005904775,
   "r_agg_E2_VRH": [
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    2.220446049250313e-16,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    -3.3306690738754696e-16,
    -2.220446049250313e-16
   ],
   "r_agg_h_VRH": [
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    2.220446049250313e-16,
    2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    2.220446049250313e-16,
    0.0,
    -1.1102230246251565e-16
   ],
   "r_agg_E2_HS": [
    -1.1102230246251565e-16,
    2.220446049250313e-16,
    2.220446049250313e-16,
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0
   ],
   "r_agg_E2_V": [
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    2.220446049250313e-16
   ],
   "r_agg_E2_R": [
    0.0,
    -1.1102230246251565e-16,
    2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    0.0,
    2.220446049250313e-16,
    -1.1102230246251565e-16,
    2.220446049250313e-16
   ],
   "S_t_E2": 4.1100077415202465e-16,
   "S_t_h": -2.925271284971396e-16,
   "kappa2_E2": -1.6739143857147652e-16,
   "kappa2_h": 1.7403176010158433e-15,
   "kappa3_E2": -6.477861259177068e-15,
   "kappa2_E2_HS": 3.6895286501663385e-15,
   "kappa2_E2_4term": -7.551062690715626e-15,
   "S_t_E2_4term": 4.1100077415202347e-16,
   "kappa4_E2_4term": 1.208541677071763e-13,
   "fit_residual": 9.58829698458047e-17,
   "fit_residual_4term": 9.082728246688532e-17,
   "halving_dev_kappa2": 36.70942580584538,
   "kappa2_E2_window0p1": -6.312235033344818e-15,
   "lambda_mean_t": [
    4.465944891615489e-31,
    5.476038365628235e-32,
    6.051257726818309e-32,
    1.948365321836496e-30,
    2.828315617598195e-30,
    4.258392291069694e-32,
    2.0671675410653463e-31,
    1.4414436418839758e-31,
    6.97654761692104e-31,
    8.05882784895705e-32,
    8.826351831704817e-31,
    5.277432358348646e-32
   ],
   "hs_ref": {
    "hi": [
     123.83246666609068,
     85.29339999914612
    ],
    "lo": [
     123.83246666724266,
     36.72520000086347
    ]
   }
  },
  "cubic_gem8|001": {
   "vT_VRH": 9.307899076533179,
   "vT_V": 9.87249208660102,
   "vT_R": 8.706771527831352,
   "vT_HS_lo": 9.211721064370861,
   "vT_HS_hi": 9.456854984588738,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    2.220446049250313e-16,
    2.220446049250313e-16
   ],
   "r_agg_E2_HS": [
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    -3.3306690738754696e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    -3.3306690738754696e-16
   ],
   "r_agg_E2_V": [
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16
   ],
   "r_agg_E2_R": [
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -4.440892098500626e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    -4.440892098500626e-16
   ],
   "S_t_E2": 2.2690471976516216e-16,
   "S_t_h": 1.0207029061365447e-15,
   "kappa2_E2": -1.4940723442743361e-16,
   "kappa2_h": 1.4525703347111552e-15,
   "kappa3_E2": -3.710299357793312e-15,
   "kappa2_E2_HS": -2.9328086757977686e-16,
   "kappa2_E2_4term": -7.548769884661831e-15,
   "S_t_E2_4term": 2.2690471976516093e-16,
   "kappa4_E2_4term": 1.2111100076374125e-13,
   "fit_residual": 1.2768503165890454e-16,
   "fit_residual_4term": 1.239173204933564e-16,
   "halving_dev_kappa2": 36.70942580584519,
   "kappa2_E2_window0p1": -5.634061021497827e-15,
   "lambda_mean_t": [
    1.3321601247899372e-30,
    3.2963158788329955e-31,
    5.115608018065614e-31,
    2.5296306525163064e-31,
    6.091189661068836e-32,
    1.490703376101465e-30,
    4.970531018467675e-31,
    1.6321728720822753e-31,
    2.0328800328242484e-30,
    9.252456281403098e-32,
    1.2157397395047422e-30,
    4.788242399022421e-30
   ],
   "hs_ref": {
    "hi": [
     210.2754999990931,
     131.54359999864414
    ],
    "lo": [
     210.27550000090693,
     46.34985000135914
    ]
   }
  },
  "cubic_gem8|111": {
   "vT_VRH": 9.307899076533179,
   "vT_V": 9.87249208660102,
   "vT_R": 8.706771527831352,
   "vT_HS_lo": 9.211721064370861,
   "vT_HS_hi": 9.456854984588738,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    0.0,
    2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    4.440892098500626e-16
   ],
   "r_agg_E2_HS": [
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    -3.3306690738754696e-16
   ],
   "r_agg_E2_V": [
    0.0,
    2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    2.220446049250313e-16,
    -2.220446049250313e-16,
    -3.3306690738754696e-16
   ],
   "r_agg_E2_R": [
    0.0,
    2.220446049250313e-16,
    0.0,
    -4.440892098500626e-16,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    2.220446049250313e-16,
    0.0,
    -4.440892098500626e-16,
    0.0
   ],
   "S_t_E2": -1.1819852171697386e-15,
   "S_t_h": 0.0,
   "kappa2_E2": 1.272728293270753e-16,
   "kappa2_h": 0.0,
   "kappa3_E2": 1.888996552887521e-14,
   "kappa2_E2_HS": -4.1502009563175863e-16,
   "kappa2_E2_4term": 4.644932862254055e-15,
   "S_t_E2_4term": -1.181985217169738e-15,
   "kappa4_E2_4term": -7.39439805238916e-14,
   "fit_residual": 1.3736358346507315e-16,
   "fit_residual_4term": 1.3607124301964625e-16,
   "halving_dev_kappa2": 36.70942580584462,
   "kappa2_E2_window0p1": 4.799385314609271e-15,
   "lambda_mean_t": [
    6.654563919555887e-32,
    1.284474620620143e-31,
    8.203146796165973e-32,
    2.191414433855259e-31,
    3.5992660205608407e-31,
    1.490703376101465e-30,
    3.737141516433966e-32,
    2.779423581315274e-32,
    4.91382581689863e-32,
    1.018907926091293e-30,
    1.3956842828973518e-31,
    4.844546844365318e-31
   ],
   "hs_ref": {
    "hi": [
     210.2754999990931,
     131.54359999864414
    ],
    "lo": [
     210.27550000090693,
     46.34985000135914
    ]
   }
  }
 },
 "falsifiers": {
  "F-MS-3": {
   "state": "SILENT",
   "worst_S_t": 4.895751529361098e-13
  },
  "F-MS-2": {
   "state": "REGISTERED_NOT_EXECUTED"
  },
  "F-MS-1": {
   "state": "RETIRED_TO_CONTROL"
  }
 },
 "verdict_class": "IDENTITY-DELIVERED",
 "T1_post_write": {
  "list_md5": "fef2827100d3f85e0a6341b44f0c00bf",
  "state": "CLEAN",
  "numeric_collisions": 4,
  "files": [
   "g_mscs1_chatleg_checkpoint.json"
  ]
 }
}
=====END-EMBED name=inputs/g_mscs1_chatleg_checkpoint.json=====

=====BEGIN-EMBED name=inputs/g_mscs1_ccleg_checkpoint.json md5=249e11dd53c4cb82f302b15d3c94c337 bytes=24415 encoding=raw=====
{
 "gate": "G-MSCS1",
 "leg": "cc",
 "instrument": "g_mscs1_ccleg.py",
 "instrument_md5": "195a2b1baf1589675d4bf18983673a23",
 "memo_md5": "3f30262eaec461fb5fd3202835f7de37",
 "memo_bytes": 34837,
 "ledger_base_md5": "d095a7003bb0d4c177e7451e1d14c4c6",
 "utc": "2026-09-20 02:00:35 UTC",
 "elections": {
  "E-MS-1": "(a) two descriptors of the one transverse field; S2-E2 primary, S2-h second arm",
  "E-MS-2": "(a) all four configurations",
  "E-MS-2b": "(a+b) banked tetragonal-form primary + hexagonal-symmetrized C66 second arm",
  "E-MS-2c": "(001+111) cubic axis 001 primary, 111 reported",
  "E-MS-3": "(a) VRH/HS leading order; polarization-resolved Born at t = 0 only",
  "E-MS-4": "(a) verbatim differentiation table + lambda_L computation",
  "E-MS-5": "(a) fiber ODF 1 + t P2(cos theta), t in [-1, 2]",
  "E-MS-6": "(a) no observational contact in this gate"
 },
 "T1": {
  "list_md5": "fef2827100d3f85e0a6341b44f0c00bf",
  "state": "CLEAN",
  "numeric_collisions": 5,
  "x_collisions_instrument_plus_memo": 0
 },
 "inputs": {
  "X1_md5": "200e7a8b775577564369c6924d38a84c",
  "X1_bytes": 2767,
  "X3_md5": "aaae206733b0f0a378a5c6b600274d3f",
  "X4_md5": "ec87e42f0f617b00c4985ba2aceac339",
  "X5_md5": "df413a7cfa30e599b779af8fee5d07d1"
 },
 "quadrature": {
  "n_theta": 64,
  "n_phi": 128,
  "doubling_residual": 1.1102230246251565e-15
 },
 "t_grid": [
  -0.5,
  -0.25,
  -0.1,
  -0.05,
  -0.02,
  0.0,
  0.02,
  0.05,
  0.1,
  0.25,
  0.5,
  1.0
 ],
 "controls": {
  "F-CTRL-ISO": {
   "passed": true,
   "r_xtal_E2": 2.220446049250313e-16,
   "r_xtal_h": 0.0,
   "lambda_max": 5.8657280953489826e-31,
   "r_agg_max": 2.220446049250313e-16
  },
  "F-CTRL-SO3": {
   "passed": true,
   "w_S2_mean_t0": 0.39999999999999997,
   "dev_from_0p4": 1.0547118733938987e-15,
   "r_agg_0_E2": 4.440892098500626e-16
  },
  "F-CTRL-TEX": {
   "passed": true,
   "r_agg_t1": 0.002501914521741977
  },
  "F-CTRL-POL": {
   "passed": true,
   "split_plus_minus": 0.0,
   "split_plus_avg": 2.0816681711721685e-17
  },
  "PIN-A2AGG": {
   "passed": true,
   "worst_rel_residual": 4.376704922376667e-15
  },
  "F-CTRL-ADMIX": {
   "passed": true,
   "r_xtal_h_projected": -0.001967367205683912,
   "x_r_by_key": {
    "hex_step|a": -0.0009717819955337159,
    "hex_step|b": -0.0009717429602675853,
    "hex_gem8|a": -0.0011309526900499245,
    "hex_gem8|b": -0.0011309883383803232,
    "cubic_step|001": -0.0016115554323222758,
    "cubic_step|111": -0.0016115554323222758,
    "cubic_gem8|001": -0.001967367205683912,
    "cubic_gem8|111": -0.001967367205683912
   },
   "x_r_complete_projection_worst": 0.0,
   "x_identity_check_2p6": {
    "hex_step|a": {
     "r_xtal_h": -0.001112878450555299,
     "identity_pred": -0.0014293733595875718,
     "rel_resid": 0.2843930609621828
    },
    "hex_step|b": {
     "r_xtal_h": -0.0011128009813170525,
     "identity_pred": -0.0014292835894878586,
     "rel_resid": 0.2844018054299647
    },
    "hex_gem8|a": {
     "r_xtal_h": -0.0013148652382883874,
     "identity_pred": -0.0016827680558306841,
     "rel_resid": 0.27980268002309533
    },
    "hex_gem8|b": {
     "r_xtal_h": -0.0013149275816995987,
     "identity_pred": -0.0016828417147120545,
     "rel_resid": 0.27979801939884136
    },
    "cubic_step|001": {
     "r_xtal_h": -0.001516377102324551,
     "identity_pred": -0.0020353270533740894,
     "rel_resid": 0.3422301419970053
    },
    "cubic_step|111": {
     "r_xtal_h": -0.001516377102324551,
     "identity_pred": -0.0020353270533740894,
     "rel_resid": 0.3422301419970053
    },
    "cubic_gem8|001": {
     "r_xtal_h": -0.0018451010194286965,
     "identity_pred": -0.0024760981546310635,
     "rel_resid": 0.3419851425792092
    },
    "cubic_gem8|111": {
     "r_xtal_h": -0.0018451010194286965,
     "identity_pred": -0.0024760981546310635,
     "rel_resid": 0.3419851425792092
    }
   },
   "x_note": "substantive implementation per dispatch step 3.3: r_xtal_h_projected is the literal memo-section-4 number (quasi-transverse eigenvectors projected, quasi-longitudinal branch untouched) and is NOT zero within tau_agg; the pass flag follows the complete zero-admixture reading, under which the split vanishes exactly; see H-CC items in the CC report"
  }
 },
 "phase1": {
  "hex_step|a": {
   "v_EM": 8.498926630589143,
   "v_S2E2": 8.261235391127112,
   "v_S2h": 8.489468358289109,
   "r_xtal_E2": -0.027967206894872754,
   "r_xtal_h": -0.001112878450555299,
   "lambda_mean": 0.004808575724022839,
   "lambda_max": 0.03353758299774612,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.03644441793256045,
   "share_EM": {
    "qL": 0.004808575724022839,
    "qSV": 0.4951914248135092,
    "qSH": 0.499999999462468
   },
   "share_S2E2": {
    "qL": 0.0020267404510848678,
    "qSV": 0.1646400534394651,
    "qSH": 0.8333332061094499
   }
  },
  "hex_step|b": {
   "v_EM": 8.499138059764721,
   "v_S2E2": 8.26161155132829,
   "v_S2h": 8.489680210591466,
   "r_xtal_E2": -0.027947129081346778,
   "r_xtal_h": -0.0011128009813170525,
   "lambda_mean": 0.0048086004283485135,
   "lambda_max": 0.033534547685208825,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.03644303566084019,
   "share_EM": {
    "qL": 0.0048086004283485135,
    "qSV": 0.49519139957165154,
    "qSH": 0.5
   },
   "share_S2E2": {
    "qL": 0.002026648513157482,
    "qSV": 0.16464001815350915,
    "qSH": 0.8333333333333335
   }
  },
  "hex_gem8|a": {
   "v_EM": 10.167571147427779,
   "v_S2E2": 9.767584615679638,
   "v_S2h": 10.154202161568202,
   "r_xtal_E2": -0.039339437703303504,
   "r_xtal_h": -0.0013148652382883874,
   "lambda_mean": 0.0049537696180639535,
   "lambda_max": 0.03513301845903746,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.051328991796831605,
   "share_EM": {
    "qL": 0.004953769618063954,
    "qSV": 0.49504623129508146,
    "qSH": 0.49999999908685466
   },
   "share_S2E2": {
    "qL": 0.0021381488678355936,
    "qSV": 0.16452961765676763,
    "qSH": 0.8333322334753966
   }
  },
  "hex_gem8|b": {
   "v_EM": 10.167412388965342,
   "v_S2E2": 9.767300819096654,
   "v_S2h": 10.154042977980577,
   "r_xtal_E2": -0.03935234989611791,
   "r_xtal_h": -0.0013149275816995987,
   "lambda_mean": 0.004953789932329422,
   "lambda_max": 0.035133018459037504,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.05133043709649307,
   "share_EM": {
    "qL": 0.004953789932329422,
    "qSV": 0.4950462100676707,
    "qSH": 0.5
   },
   "share_S2E2": {
    "qL": 0.0021382152528626997,
    "qSV": 0.1645284514138039,
    "qSH": 0.8333333333333336
   }
  },
  "cubic_step|001": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 7.889264216956221,
   "v_S2h": 8.015951162831872,
   "r_xtal_E2": -0.017296767741215913,
   "r_xtal_h": -0.001516377102324551,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173745,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.04901957894779363,
   "share_EM": {
    "qL": 0.0083923190288783,
    "qT1": 0.4992967361164543,
    "qT2": 0.49231094485466753
   },
   "share_S2E2": {
    "qL": 0.008569676861049402,
    "qT1": 0.44880232089111627,
    "qT2": 0.5426280022478344
   }
  },
  "cubic_step|111": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 8.120698567854001,
   "v_S2h": 8.015951162831872,
   "r_xtal_E2": 0.01153117849414409,
   "r_xtal_h": -0.001516377102324551,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173745,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.04901957894779363,
   "share_EM": {
    "qL": 0.0083923190288783,
    "qT1": 0.4992967361164543,
    "qT2": 0.49231094485466753
   },
   "share_S2E2": {
    "qL": 0.008274080474097544,
    "qT1": 0.5330407329981224,
    "qT2": 0.45868518652777995
   }
  },
  "cubic_gem8|001": {
   "v_EM": 9.721171015078212,
   "v_S2E2": 9.518558071803296,
   "v_S2h": 9.703234472528251,
   "r_xtal_E2": -0.02084244202274077,
   "r_xtal_h": -0.0018451010194286965,
   "lambda_mean": 0.009310503859652798,
   "lambda_max": 0.043292701954120015,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.07221172083386443,
   "share_EM": {
    "qL": 0.009310503859652798,
    "qT1": 0.49922505755529545,
    "qT2": 0.49146443858505184
   },
   "share_S2E2": {
    "qL": 0.009492782074764233,
    "qT1": 0.44874904568984897,
    "qT2": 0.5417581722353866
   }
  },
  "cubic_gem8|111": {
   "v_EM": 9.721171015078212,
   "v_S2E2": 9.856246310594821,
   "v_S2h": 9.703234472528251,
   "r_xtal_E2": 0.013894961348493773,
   "r_xtal_h": -0.0018451010194286965,
   "lambda_mean": 0.009310503859652798,
   "lambda_max": 0.043292701954120015,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.07221172083386443,
   "share_EM": {
    "qL": 0.009310503859652798,
    "qT1": 0.49922505755529545,
    "qT2": 0.49146443858505184
   },
   "share_S2E2": {
    "qL": 0.009188985049578397,
    "qT1": 0.5329595958441811,
    "qT2": 0.4578514191062405
   }
  }
 },
 "phase2": {
  "hex_step|a": {
   "vT_VRH": 8.419059637591616,
   "vT_HS_lo": 8.390859731729313,
   "vT_HS_hi": 8.424582419402883,
   "r_agg_E2_VRH": [
    -0.0003597789838700738,
    -8.995485659368807e-05,
    -1.4393819487867887e-05,
    -3.5985447373043655e-06,
    -5.7577590029112e-07,
    -2.220446049250313e-16,
    -5.757876907486192e-07,
    -3.5987289647154697e-06,
    -1.4395293313040902e-05,
    -8.997788565123788e-05,
    -0.00035996323194520397,
    -0.001440311666698113
   ],
   "r_agg_h_VRH": [
    -4.97443568558964e-07,
    -1.249121053259472e-07,
    -2.0039163883822653e-08,
    -5.01423980114879e-09,
    -8.027061237925182e-10,
    0.0,
    -8.03276667404873e-10,
    -5.023156890437974e-09,
    -2.011050115324764e-08,
    -1.260267622482658e-07,
    -5.063613532918509e-07,
    -2.043685221497782e-06
   ],
   "r_agg_E2_HS": [
    -0.0003571461079148186,
    -8.927425424842816e-05,
    -1.4282679909993767e-05,
    -3.5705689754861325e-06,
    -5.71281304040383e-07,
    2.220446049250313e-16,
    -5.712682857872409e-07,
    -3.570365567528988e-06,
    -1.4281052650777504e-05,
    -8.924882879401963e-05,
    -0.0003569427177455564,
    -0.0014273362560642822
   ],
   "S_t_E2": 1.6132521040103724e-13,
   "S_t_h": 3.901387545207024e-15,
   "kappa2_E2": -0.0014394617695005832,
   "kappa2_h": -2.0075102000424232e-06,
   "kappa3_E2": -7.369324104590622e-07,
   "fit_residual": 6.129824287082772e-11,
   "halving_dev_kappa2": 4.296068727221966e-06,
   "lambda_mean_t": [
    2.5111906360905225e-06,
    6.283852379770122e-07,
    1.0059951851451649e-07,
    2.51547644056437e-08,
    4.025233596548142e-09,
    0.0,
    4.025864754976195e-09,
    2.516462609932631e-08,
    1.0067841215180097e-07,
    6.296179578773481e-07,
    2.521052590653425e-06,
    1.0105781771537547e-05
   ],
   "x_kappa_4term_fit_E2": [
    1.613207980641205e-13,
    -0.0014394544404483034,
    -7.369324103762292e-07,
    -1.199601774147876e-07
   ]
  },
  "hex_step|b": {
   "vT_VRH": 8.4192786485796,
   "vT_HS_lo": 8.391084746839036,
   "vT_HS_hi": 8.42480325772318,
   "r_agg_E2_VRH": [
    -0.000359589205973343,
    -8.990741528092094e-05,
    -1.4386229051810417e-05,
    -3.5966471373383158e-06,
    -5.754722848250182e-07,
    0.0,
    -5.75484075837629e-07,
    -3.59683137440836e-06,
    -1.4387702956142334e-05,
    -8.993044558214258e-05,
    -0.00035977346397664256,
    -0.001439552451643511
   ],
   "r_agg_h_VRH": [
    -4.969233557972075e-07,
    -1.247812418947447e-07,
    -2.001814791707801e-08,
    -5.0089792313912085e-09,
    -8.018635755391301e-10,
    0.0,
    -8.024333419953678e-10,
    -5.017882998004097e-09,
    -2.0089378716114936e-08,
    -1.2589424969178253e-07,
    -5.058279419767331e-07,
    -2.04152418015191e-06
   ],
   "r_agg_E2_HS": [
    -0.0003569546896107223,
    -8.922641129327502e-05,
    -1.4275026188892426e-05,
    -3.5686556428826677e-06,
    -5.709751801363794e-07,
    -2.220446049250313e-16,
    -5.709621745397797e-07,
    -3.5684524321011324e-06,
    -1.4273400507525125e-05,
    -8.920101049236795e-05,
    -0.0003567514966401619,
    -0.0014265718105257452
   ],
   "S_t_E2": 1.6400082932192235e-13,
   "S_t_h": 8.137135505898113e-15,
   "kappa2_E2": -0.0014387027187507326,
   "kappa2_h": -2.0054031944932263e-06,
   "kappa3_E2": -7.369722507858468e-07,
   "fit_residual": 6.118721569792576e-11,
   "halving_dev_kappa2": 4.290551805693156e-06,
   "lambda_mean_t": [
    2.508642213075073e-06,
    6.277474540209645e-07,
    1.0049740414635627e-07,
    2.512922990500282e-08,
    4.021147506729069e-09,
    0.0,
    4.0217778891485955e-09,
    2.51390795521338e-08,
    1.0057620139494587e-07,
    6.289786678683045e-07,
    2.5184921186663207e-06,
    1.009551097933715e-05
   ],
   "x_kappa_4term_fit_E2": [
    1.6399641930257683e-13,
    -0.0014386954029695716,
    -7.369722507030138e-07,
    -1.197429589050166e-07
   ]
  },
  "hex_gem8|a": {
   "vT_VRH": 10.041721817369156,
   "vT_HS_lo": 9.990913001573082,
   "vT_HS_hi": 10.05279775494808,
   "r_agg_E2_VRH": [
    -0.0004737700796713096,
    -0.00011845867062443283,
    -1.8955103105566806e-05,
    -4.738925659331095e-06,
    -7.582427593577634e-07,
    -2.220446049250313e-16,
    -7.582626074809085e-07,
    -4.739235785145013e-06,
    -1.895758412695514e-05,
    -0.00011849743822178738,
    -0.00047408026726236674,
    -0.0018971495594128918
   ],
   "r_agg_h_VRH": [
    -8.038770585860888e-07,
    -2.0201977357636736e-07,
    -3.242488200161375e-08,
    -8.11473377382299e-09,
    -1.299175989011303e-09,
    0.0,
    -1.3002695586905588e-09,
    -8.131815554257571e-09,
    -3.2561537133268814e-08,
    -2.041550740683462e-07,
    -8.209613451271025e-07,
    -3.3191570850688024e-06
   ],
   "r_agg_E2_HS": [
    -0.00047147218794074686,
    -0.00011785019986754186,
    -1.8854266348178328e-05,
    -4.713417281476673e-06,
    -7.541323485682483e-07,
    -2.220446049250313e-16,
    -7.541130296884191e-07,
    -4.713115426491221e-06,
    -1.8851851520507168e-05,
    -0.00011781246964759351,
    -0.00047117038801591793,
    -0.0018840138120480576
   ],
   "S_t_E2": 4.88778727245365e-13,
   "S_t_h": 1.8870073354479004e-14,
   "kappa2_E2": -0.0018956484826738256,
   "kappa2_h": -3.249396699531321e-06,
   "kappa3_E2": -1.2405708979146963e-06,
   "fit_residual": 1.4122180315889916e-10,
   "halving_dev_kappa2": 7.515517296534205e-06,
   "lambda_mean_t": [
    3.6006634946301176e-06,
    9.011863601856414e-07,
    1.4429157576291246e-07,
    3.608153193548488e-08,
    5.7738804321405966e-09,
    0.0,
    5.775001286170658e-09,
    3.609904534358997e-08,
    1.4443168336644392e-07,
    9.033755744628227e-07,
    3.6181781526989147e-06,
    1.4512512141049044e-05
   ],
   "x_kappa_4term_fit_E2": [
    4.887729165585316e-13,
    -0.0018956315979800395,
    -1.2405708978056256e-06,
    -2.7636463552777845e-07
   ]
  },
  "hex_gem8|b": {
   "vT_VRH": 10.041554085160612,
   "vT_HS_lo": 9.990739829721814,
   "vT_HS_hi": 10.05262995929398,
   "r_agg_E2_VRH": [
    -0.0004738923403124762,
    -0.00011848923252755217,
    -1.8959992844180817e-05,
    -4.740148086490592e-06,
    -7.58438347125967e-07,
    4.440892098500626e-16,
    -7.584581950270675e-07,
    -4.740458205643172e-06,
    -1.896247381538707e-05,
    -0.00011852799934330971,
    -0.00047420252167706956,
    -0.0018976387487922297
   ],
   "r_agg_h_VRH": [
    -8.04256157782568e-07,
    -2.021152383235858e-07,
    -3.244022384052414e-08,
    -8.118574701398984e-09,
    -1.2997910525669454e-09,
    2.220446049250313e-16,
    -1.3008851773577135e-09,
    -8.13566802815302e-09,
    -3.2576969677400314e-08,
    -2.0425195845774624e-07,
    -8.213518062349934e-07,
    -3.3207430030213203e-06
   ],
   "r_agg_E2_HS": [
    -0.00047159589986833783,
    -0.00011788112071775547,
    -1.8859212958410865e-05,
    -4.714653872306407e-06,
    -7.543301973056415e-07,
    0.0,
    -7.543108700991397e-07,
    -4.714351890200419e-06,
    -1.8856797115107682e-05,
    -0.00011784337463249805,
    -0.00047129397306722165,
    -0.0018845078483346045
   ],
   "S_t_E2": 4.90291953941434e-13,
   "S_t_h": 1.9232267730539364e-14,
   "kappa2_E2": -0.0018961374665274083,
   "kappa2_h": -3.250935490588331e-06,
   "kappa3_E2": -1.240545911150953e-06,
   "fit_residual": 1.4134676897214994e-10,
   "halving_dev_kappa2": 7.520230342822992e-06,
   "lambda_mean_t": [
    3.6022883240769405e-06,
    9.015930248276157e-07,
    1.4435669065512994e-07,
    3.609781489279239e-08,
    5.776486127644972e-09,
    0.0,
    5.7776075427095745e-09,
    3.6115337074777367e-08,
    1.4449686839815845e-07,
    9.03783335221914e-07,
    3.6198117522199667e-06,
    1.4519069924266563e-05
   ],
   "x_kappa_4term_fit_E2": [
    4.902861417464788e-13,
    -0.001896120566887107,
    -1.2405459110416654e-06,
    -2.7660927652668255e-07
   ]
  },
  "cubic_step|001": {
   "vT_VRH": 7.7990463758448945,
   "vT_HS_lo": 7.758614490217017,
   "vT_HS_hi": 7.867953005902295,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    2.220446049250313e-16,
    2.220446049250313e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    2.220446049250313e-16
   ],
   "r_agg_E2_HS": [
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    0.0
   ],
   "S_t_E2": 7.009496149267015e-17,
   "S_t_h": 1.2375133173866637e-30,
   "kappa2_E2": -2.1857725036605986e-16,
   "kappa2_h": -3.5691728224331273e-16,
   "kappa3_E2": -1.317121335111205e-15,
   "fit_residual": 2.1815805389137155e-16,
   "halving_dev_kappa2": 36.70942580584521,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    7.009496149266831e-17,
    -1.0159890418394039e-14,
    -1.3171213351111684e-15,
    1.62717039777404e-13
   ]
  },
  "cubic_step|111": {
   "vT_VRH": 7.7990463758448945,
   "vT_HS_lo": 7.758614490217017,
   "vT_HS_hi": 7.867953005902295,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0,
    -2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    4.440892098500626e-16,
    6.661338147750939e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    2.220446049250313e-16
   ],
   "r_agg_E2_HS": [
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    0.0
   ],
   "S_t_E2": 7.00949614926752e-17,
   "S_t_h": 6.568330085717285e-30,
   "kappa2_E2": -1.9478276488317234e-15,
   "kappa2_h": -2.0861676807089763e-15,
   "kappa3_E2": -1.3171213351113003e-15,
   "fit_residual": 2.1383492789520715e-16,
   "halving_dev_kappa2": 3.2315974980991067,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    7.009496149266832e-17,
    -9.84213081218537e-15,
    -1.3171213351111702e-15,
    1.2921206888215457e-13
   ]
  },
  "cubic_gem8|001": {
   "vT_VRH": 9.307899076533193,
   "vT_HS_lo": 9.211721064384875,
   "vT_HS_hi": 9.456854984584107,
   "r_agg_E2_VRH": [
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    0.0,
    2.220446049250313e-16,
    0.0
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "r_agg_E2_HS": [
    2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -3.3306690738754696e-16,
    -5.551115123125783e-16
   ],
   "S_t_E2": -9.550804974045757e-16,
   "S_t_h": 0.0,
   "kappa2_E2": -2.9881446885486723e-16,
   "kappa2_h": 0.0,
   "kappa3_E2": 1.5179666171081885e-14,
   "fit_residual": 2.409052517562122e-16,
   "halving_dev_kappa2": 36.70942580584519,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    -9.550804974045788e-16,
    -1.3348319157336616e-14,
    1.517966617108195e-14,
    2.1359117629450065e-13
   ]
  },
  "cubic_gem8|111": {
   "vT_VRH": 9.307899076533193,
   "vT_HS_lo": 9.211721064384875,
   "vT_HS_hi": 9.456854984584107,
   "r_agg_E2_VRH": [
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "r_agg_E2_HS": [
    4.440892098500626e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -5.551115123125783e-16,
    -3.3306690738754696e-16
   ],
   "S_t_E2": 2.925271284971411e-16,
   "S_t_h": 0.0,
   "kappa2_E2": -2.2936777285248548e-15,
   "kappa2_h": 0.0,
   "kappa3_E2": -1.1860380658980084e-14,
   "fit_residual": 2.220446049250313e-16,
   "halving_dev_kappa2": 8.27952094619114,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    2.9252712849713164e-16,
    -2.4646954092833455e-14,
    -1.1860380658979912e-14,
    3.658730891834499e-13
   ]
  }
 },
 "born_t0": {
  "hex_step": {
   "D0_plus": -0.020528244595327125,
   "D0_minus": -0.020528244595327125,
   "D0_avg": -0.02052824459532713,
   "D2_avg": -0.018347663163945885,
   "a2agg_residual_rel": 1.8909475942262037e-15
  },
  "hex_gem8": {
   "D0_plus": -0.028917807603071596,
   "D0_minus": -0.028917807603071596,
   "D0_avg": -0.028917807603071617,
   "D2_avg": -0.025933693584294176,
   "a2agg_residual_rel": 6.689072153715041e-16
  },
  "cubic_step": {
   "D0_plus": -0.03151342243433817,
   "D0_minus": -0.03151342243433817,
   "D0_avg": -0.031513422434338176,
   "D2_avg": -0.028537471107946338,
   "a2agg_residual_rel": 4.376704922376667e-15
  },
  "cubic_gem8": {
   "D0_plus": -0.04367714392697755,
   "D0_minus": -0.04367714392697755,
   "D0_avg": -0.043677143926977566,
   "D2_avg": -0.03971397679128604,
   "a2agg_residual_rel": 1.5724953827557158e-15
  }
 },
 "falsifiers": {
  "F-MS-3": {
   "state": "SILENT",
   "worst_S_t": 4.90291953941434e-13
  },
  "F-MS-2": {
   "state": "REGISTERED_NOT_EXECUTED"
  },
  "F-MS-1": {
   "state": "RETIRED_TO_CONTROL"
  }
 },
 "x_pins": {
  "PIN-VRH0_worst_rel": 9.898898090587927e-16,
  "PIN-HS0_worst_rel": 4.644295379818518e-12,
  "hs_references": {
   "hex_step": {
    "lo_K0_G0": [
     134.60708943792756,
     60.030800002639964
    ],
    "hi_K0_G0": [
     135.3665929776937,
     115.55987377748554
    ]
   },
   "hex_step|b": {
    "lo_K0_G0": [
     134.60708943792758,
     60.03080000263914
    ],
    "hi_K0_G0": [
     135.36658842797797,
     115.55987474358491
    ]
   },
   "hex_gem8": {
    "lo_K0_G0": [
     229.69575433713962,
     84.82450000424566
    ],
    "hi_K0_G0": [
     230.1360532921952,
     178.29434080456548
    ]
   },
   "hex_gem8|b": {
    "lo_K0_G0": [
     229.69575433713962,
     84.82450000424924
    ],
    "hi_K0_G0": [
     230.13605425859672,
     178.29434061744877
    ]
   },
   "cubic_step": {
    "lo_K0_G0": [
     123.83246666828633,
     36.725200002429304
    ],
    "hi_K0_G0": [
     123.832466665047,
     85.29339999757266
    ]
   },
   "cubic_gem8": {
    "lo_K0_G0": [
     210.27550000263054,
     46.34985000394528
    ],
    "hi_K0_G0": [
     210.27549999736948,
     131.5435999960556
    ]
   }
  }
 },
 "x_so3_grid": [
  20,
  12,
  20
 ],
 "x_runtime_s": 33.46,
 "verdict_class": "IDENTITY-DELIVERED"
}
=====END-EMBED name=inputs/g_mscs1_ccleg_checkpoint.json=====

=====BEGIN-EMBED name=g_mscs2_chatleg.py md5=f277580ddf0b4da9734d11edb009c54b bytes=42448 encoding=base64 armor_bytes=57345 QUARANTINED=====
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJnX21zY3MyX2NoYXRsZWcucHkgLS0gR2F0ZSBHLU1T
Q1MyIGNoYXQtbGVnIGluc3RydW1lbnQsIHYxIChTZXB0ZW1iZXIgMjYsIDIwMjYpLgoKRW5jb2Rl
cyB0aGUgTE9DS0VEIHN0YWdpbmcgbWVtbyB2MiAoZWZkY2FiZGMpIGFuZCBsb2NrIHJlY29yZCBB
ZGRlbmR1bSBBLTIgKDQ5MjMyZDRjKS4gTm8gb2JzZXJ2YXRpb25hbCBudW1iZXIsCm5vIFNJIHVu
aXQsIG5vIHRhcmdldCBzdHJpbmcgYXBwZWFycyBoZXJlOyB0aGUgcGlubmVkIHNjYW5uZXIgKFQx
IGdhdGUgbGlzdCBiZTkyMWI4YykgcnVucyBvbiB0aGlzIGZpbGUgYW5kIHRoZSBtZW1vCmF0IGV2
ZXJ5IGludm9jYXRpb24gYW5kIHRoZSBpbnN0cnVtZW50IEhBTFRTIG9uIGFueSBoaXQgYW5kIHdp
dGhvdXQgdGhlIGxpc3QgKG5vIG92ZXJyaWRlIHBhdGgpLgoKTWFjaGluZXJ5IGluaGVyaXRlZCBm
cm9tIHRoZSBHLU1TQ1MxIGNoYXQgaW5zdHJ1bWVudCAoZGI1ZjUxZGQ7IHRoZSBjaGF0IGxlZyBt
YXkgcmV1c2UgaXRzIG93biBwcmlvciBjb2RlIOKAlCB0aGUgQ0MKbGVnIGlzIHRoZSBibGluZCBv
bmUpOiB0ZW5zb3JzLCBTTygzKSBwcm9kdWN0IHF1YWRyYXR1cmUsIFZvaWd0L1JldXNzL0hpbGwg
YW5kIFdhbHBvbGUtSFMgd2l0aCByZWZlcmVuY2VzIG9wdGltaXplZAphdCB0ID0gMCwgay1zcGhl
cmUgQ2hyaXN0b2ZmZWwsIHRoZSBkZXNjcmlwdG9ycywgdGhlIGZpdHMuIE5ldzogdGhlIGwgPSA0
IE9ERiBmYW1pbGllcyAoY3ViaWMgSzQtdGlsZGUsIGhleCBQNCwgdGhlIGhleAoodDIsIHQ0KSBm
b3JtKSwgdGhlIG1hcmdpbmFsIGRlc2NyaXB0b3Itd2VpZ2h0IGF2ZXJhZ2VzLCB0aGUgZXhoYXVz
dGlvbiAvIGFmZmluaXR5IC8gY2xvc2VkLWZvcm0gLyBtYXJnaW5hbCBjb250cm9scywKdGhlIGNv
bnRpbnVpdHkgcGlucyBhZ2FpbnN0IFgtNiwgdGhlIGJpcmVmcmluZ2VuY2UgY29lZmZpY2llbnQs
IHRoZSBxdWFkcmF0aWMgZm9ybS4KClN1YmNvbW1hbmRzCiAgc2VsZnRlc3QgICAgICAgICAgZXhh
Y3RuZXNzIGFuZCBpZGVudGl0eSBzdWl0ZXMgb24gc3ludGhldGljIGlucHV0cyAobm8gY2hlY2tw
b2ludCB3cml0dGVuKQogIHJ1biBbLS1waGFzZTAtb25seV0gIGd1YXJkcyAtPiBwaGFzZTAgcGlu
cytjb250cm9scyAoaGFsdCBvbiBmYWlsdXJlIC0+IElOREVURVJNSU5BVEUpIFstPiBwaGFzZTIg
LT4gcGhhc2UzXSAtPiBjaGVja3BvaW50CiAgY29tcGFyZSAgICAgICAgICAgTEFTVDogdGhlIG1l
bW8gc2VjdGlvbi02IGh5cG90aGVzZXMgYWdhaW5zdCB0aGUgZnVsbCBjaGVja3BvaW50LCB3cml0
dGVuIHRvIGEgc2VwYXJhdGUgYXJ0aWZhY3QKIiIiCmltcG9ydCBhcmdwYXJzZSwgZGF0ZXRpbWUs
IGhhc2hsaWIsIGltcG9ydGxpYi51dGlsLCBqc29uLCBtYXRoLCBvcywgc3lzCmltcG9ydCBudW1w
eSBhcyBucAoKSEVSRSA9IG9zLnBhdGguZGlybmFtZShvcy5wYXRoLmFic3BhdGgoX19maWxlX18p
KTsgTUUgPSBvcy5wYXRoLmFic3BhdGgoX19maWxlX18pCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0g
bG9jayBwaW5zIChsb2NrIHJlY29yZCDCpzEpCk1FTU8gPSBvcy5wYXRoLmpvaW4oSEVSRSwgJ3N0
YWdpbmdfbWVtb19HX01TQ1MyX3YyLm1kJyk7IE1FTU9fTUQ1ID0gJ2VmZGNhYmRjZDkzN2NkYTRh
Y2I2NGY5NDFkYzRiYjJiJzsgTUVNT19CWVRFUyA9IDQ2MDUzClQxTElTVCA9IG9zLnBhdGguam9p
bihIRVJFLCAndG9vbHMvdDEvVDFfZm9yYmlkZGVuX0dfTVNDUzIudHh0Jyk7IFQxX01ENSA9ICdi
ZTkyMWI4YzI5Zjc1NzhlODVlZDkyZjE0NTBjMTk1NicKU0NBTk5FUiA9IG9zLnBhdGguam9pbihI
RVJFLCAndG9vbHMvdDEvdDFfc2Nhbi5weScpOyBTQ0FOTkVSX01ENSA9ICc2Yjg2MjkwMDkwYThj
ODRmMWIxYTBhOTllYzBiZjY5NycKTEVER0VSX0JBU0VfTUQ1ID0gJ2YzNmJiZGIwNDEwNDAwODc4
M2YyNzYzZjcwZmI5MTZmJwpYMSA9IG9zLnBhdGguam9pbihIRVJFLCAnaW5wdXRzL3BvbHlfdnJo
X3Jlc3VsdHMuanNvbicpOyBYMV9NRDUgPSAnMjAwZTdhOGI3NzU1Nzc1NjQzNjljNjkyNGQzOGE4
NGMnOyBYMV9CWVRFUyA9IDI3NjcKWDZDID0gb3MucGF0aC5qb2luKEhFUkUsICdpbnB1dHMvZ19t
c2NzMV9jaGF0bGVnX2NoZWNrcG9pbnQuanNvbicpOyBYNkNfTUQ1ID0gJ2MwNGMwYjhlYTM0Y2Zl
NjBmMjMxYWEwNjgyOGU2Y2U0JwpYNkNDID0gb3MucGF0aC5qb2luKEhFUkUsICdpbnB1dHMvZ19t
c2NzMV9jY2xlZ19jaGVja3BvaW50Lmpzb24nKTsgWDZDQ19NRDUgPSAnMjQ5ZTExZGQ1M2M0Y2I4
MmYzMDJiMTVkM2M5NGMzMzcnCkVMRUNUSU9OUyA9IHsiRS1NUzItMSI6ICJhK2IiLCAiRS1NUzIt
MiI6ICJhIiwgIkUtTVMyLTJiIjogImErYiIsICJFLU1TMi0yYyI6ICIwMDErMTExIiwgIkUtTVMy
LTMiOiAiYSIsICJFLU1TMi00IjogImEiLCAiRS1NUzItNSI6ICJhIiwgIkUtTVMyLTYiOiAiYSIs
ICJFLU1TMi03IjogIjA1MzAyMjEwK01TQ1Mxc3RyYXR1bSIsICJFLU1TMi04IjogImEifQpUNF9H
UklEID0gWy0wLjUsIC0wLjI1LCAtMC4xLCAtMC4wNSwgLTAuMDIsIDAuMCwgMC4wMiwgMC4wNSwg
MC4xLCAwLjI1LCAwLjUsIDEuMF0KVDJUNCA9IFstMC4yNSwgLTAuMTI1LCAwLjAsIDAuMTI1LCAw
LjI1XQpOX1RIRVRBLCBOX1BISSA9IDY0LCAxMjgKVEFVLCBLRkxPT1IgPSAxZS02LCAxZS02CkNP
TkZJR1MgPSB7J2hleF9zdGVwJzogKCdoZXgnLCAnaGV4OnN0ZXAnKSwgJ2hleF9nZW04JzogKCdo
ZXgnLCAnaGV4OmdlbTgnKSwgJ2N1YmljX3N0ZXAnOiAoJ2N1YmljJywgJ2N1YmljOnN0ZXAnKSwg
J2N1YmljX2dlbTgnOiAoJ2N1YmljJywgJ2N1YmljOmdlbTgnKX0KQkFOS19LRVkgPSB7J2hleF9z
dGVwJzogJ3N0ZXBfaGV4JywgJ2hleF9nZW04JzogJ2dlbThfaGV4JywgJ2N1YmljX3N0ZXAnOiAn
c3RlcF9jdWJpYycsICdjdWJpY19nZW04JzogJ2dlbThfY3ViaWMnfQpLRVlTID0gWydoZXhfc3Rl
cHxhJywgJ2hleF9zdGVwfGInLCAnaGV4X2dlbTh8YScsICdoZXhfZ2VtOHxiJywgJ2N1YmljX3N0
ZXB8MDAxJywgJ2N1YmljX3N0ZXB8MTExJywgJ2N1YmljX2dlbTh8MDAxJywgJ2N1YmljX2dlbTh8
MTExJ10KWiA9IG5wLmFycmF5KFswLjAsIDAuMCwgMS4wXSk7IFggPSBucC5hcnJheShbMS4wLCAw
LjAsIDAuMF0pOyBZID0gbnAuYXJyYXkoWzAuMCwgMS4wLCAwLjBdKTsgQVgxMTEgPSBucC5hcnJh
eShbMS4wLCAxLjAsIDEuMF0pIC8gbWF0aC5zcXJ0KDMuMCkKQ0hFQ0tQT0lOVCA9IG9zLnBhdGgu
am9pbihIRVJFLCAnZ19tc2NzMl9jaGF0bGVnX2NoZWNrcG9pbnQuanNvbicpOyBDSEVDS1BPSU5U
X1AwID0gb3MucGF0aC5qb2luKEhFUkUsICdnX21zY3MyX2NoYXRsZWdfcGhhc2UwX2NoZWNrcG9p
bnQuanNvbicpOyBDT01QQVJFID0gb3MucGF0aC5qb2luKEhFUkUsICdnX21zY3MyX2NoYXRsZWdf
Y29tcGFyZS5qc29uJykKCmRlZiBtZDViKGIpOiByZXR1cm4gaGFzaGxpYi5tZDUoYikuaGV4ZGln
ZXN0KCkKZGVmIG1kNWYocCk6IHJldHVybiBtZDViKG9wZW4ocCwgJ3JiJykucmVhZCgpKQpkZWYg
cmVsKGEsIGIpOiByZXR1cm4gYWJzKGEgLSBiKSAvIG1heChhYnMoYSksIGFicyhiKSwgMWUtMzAw
KQoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBndWFyZHMgKyBUMQpkZWYgdDFfZ2F0ZShwYXRocyk6
CiAgICBpZiBub3Qgb3MucGF0aC5leGlzdHMoVDFMSVNUKTogc3lzLmV4aXQoJ0hBTFQ6IFQxIGdh
dGUgbGlzdCBhYnNlbnQgLS0gdGhpcyBnYXRlIGhhcyBubyBMSVNUX0FCU0VOVCBwYXRoJykKICAg
IGlmIG1kNWYoVDFMSVNUKSAhPSBUMV9NRDU6IHN5cy5leGl0KCdIQUxUOiBUMSBnYXRlIGxpc3Qg
bWQ1ICE9IGxvY2snKQogICAgaWYgbWQ1ZihTQ0FOTkVSKSAhPSBTQ0FOTkVSX01ENTogc3lzLmV4
aXQoJ0hBTFQ6IHNjYW5uZXIgbWQ1ICE9IGxvY2snKQogICAgc3BlYyA9IGltcG9ydGxpYi51dGls
LnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCd0MV9zY2FuJywgU0NBTk5FUik7IG1vZCA9IGltcG9y
dGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoc3BlYyk7IHNwZWMubG9hZGVyLmV4ZWNfbW9kdWxl
KG1vZCkKICAgIHBhdHMgPSBtb2QubG9hZChUMUxJU1QpOyBvdXQgPSB7J2xpc3RfbWQ1JzogVDFf
TUQ1LCAnc2Nhbm5lcl9tZDUnOiBTQ0FOTkVSX01ENX0KICAgIGZvciB0YWcsIHAgaW4gcGF0aHMu
aXRlbXMoKToKICAgICAgICBoaXRzLCBjb2xsID0gbW9kLnNjYW5fdGV4dChvcGVuKHAsICdyYicp
LnJlYWQoKS5kZWNvZGUoJ3V0Zi04JywgJ3JlcGxhY2UnKSwgcGF0cykKICAgICAgICBpZiBoaXRz
OiBzeXMuZXhpdChmJ0hBTFQ6IFQxIEhJVCBpbiB7dGFnfTogcGF0dGVybiBpbmRpY2VzIHtzb3J0
ZWQoc2V0KGkgZm9yIGksIF8gaW4gaGl0cykpfScpCiAgICAgICAgb3V0W3RhZ10gPSAnQ0xFQU4n
CiAgICByZXR1cm4gb3V0CmRlZiBndWFyZHMoKToKICAgIGZvciBwLCBtLCBuYiBpbiAoKE1FTU8s
IE1FTU9fTUQ1LCBNRU1PX0JZVEVTKSwgKFgxLCBYMV9NRDUsIFgxX0JZVEVTKSk6CiAgICAgICAg
cmF3ID0gb3BlbihwLCAncmInKS5yZWFkKCkKICAgICAgICBpZiBtZDViKHJhdykgIT0gbSBvciBs
ZW4ocmF3KSAhPSBuYjogc3lzLmV4aXQoZidIQUxUOiB7b3MucGF0aC5iYXNlbmFtZShwKX0gZG9l
cyBub3QgbWF0Y2ggdGhlIGxvY2sgKHttZDViKHJhdyl9LCB7bGVuKHJhdyl9IEIpJykKICAgIGZv
ciBwLCBtIGluICgoWDZDLCBYNkNfTUQ1KSwgKFg2Q0MsIFg2Q0NfTUQ1KSk6CiAgICAgICAgaWYg
bWQ1ZihwKSAhPSBtOiBzeXMuZXhpdChmJ0hBTFQ6IHBpbiBzb3VyY2Uge29zLnBhdGguYmFzZW5h
bWUocCl9IG1kNSAhPSBsb2NrJykKICAgIHJldHVybiB0MV9nYXRlKHsnaW5zdHJ1bWVudCc6IE1F
LCAnbWVtbyc6IE1FTU99KQoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSB0ZW5zb3JzIChpbmhlcml0
ZWQpClZPSUdUID0gWygwLCAwKSwgKDEsIDEpLCAoMiwgMiksICgxLCAyKSwgKDAsIDIpLCAoMCwg
MSldCmRlZiBjNF9mcm9tX2NvbnN0YW50cyhzeW0sIGMsIHN5bW1ldHJpemVfaGV4PUZhbHNlKToK
ICAgIE0gPSBucC56ZXJvcygoNiwgNikpCiAgICBpZiBzeW0gPT0gJ2hleCc6CiAgICAgICAgQzEx
LCBDMTIsIEMxMywgQzMzLCBDNDQgPSAoY1trXSBmb3IgayBpbiAoJ0MxMScsICdDMTInLCAnQzEz
JywgJ0MzMycsICdDNDQnKSkKICAgICAgICBDNjYgPSAwLjUgKiAoQzExIC0gQzEyKSBpZiBzeW1t
ZXRyaXplX2hleCBlbHNlIGNbJ0M2NiddCiAgICAgICAgTVs6MywgOjNdID0gW1tDMTEsIEMxMiwg
QzEzXSwgW0MxMiwgQzExLCBDMTNdLCBbQzEzLCBDMTMsIEMzM11dOyBNWzMsIDNdID0gTVs0LCA0
XSA9IEM0NDsgTVs1LCA1XSA9IEM2NgogICAgZWxzZToKICAgICAgICBDMTEsIEMxMiwgQzQ0ID0g
Y1snQzExJ10sIGNbJ0MxMiddLCBjWydDNDQnXQogICAgICAgIE1bOjMsIDozXSA9IFtbQzExLCBD
MTIsIEMxMl0sIFtDMTIsIEMxMSwgQzEyXSwgW0MxMiwgQzEyLCBDMTFdXTsgTVszLCAzXSA9IE1b
NCwgNF0gPSBNWzUsIDVdID0gQzQ0CiAgICByZXR1cm4gdm9pZ3Q2Nl90b19jNChNKQpkZWYgdm9p
Z3Q2Nl90b19jNChNKToKICAgIFQgPSBucC56ZXJvcygoMywgMywgMywgMykpCiAgICBmb3IgSSwg
KGksIGopIGluIGVudW1lcmF0ZShWT0lHVCk6CiAgICAgICAgZm9yIEosIChrLCBsKSBpbiBlbnVt
ZXJhdGUoVk9JR1QpOgogICAgICAgICAgICBmb3IgYSwgYiBpbiAoKGksIGopLCAoaiwgaSkpOgog
ICAgICAgICAgICAgICAgZm9yIGNjLCBkIGluICgoaywgbCksIChsLCBrKSk6CiAgICAgICAgICAg
ICAgICAgICAgVFthLCBiLCBjYywgZF0gPSBNW0ksIEpdCiAgICByZXR1cm4gVApkZWYgYzRfdG9f
dm9pZ3Q2NihUKToKICAgIHJldHVybiBucC5hcnJheShbW1RbaSwgaiwgaywgbF0gZm9yIChrLCBs
KSBpbiBWT0lHVF0gZm9yIChpLCBqKSBpbiBWT0lHVF0pCl9NRiA9IG5wLmFycmF5KFsxLCAxLCAx
LCBtYXRoLnNxcnQoMiksIG1hdGguc3FydCgyKSwgbWF0aC5zcXJ0KDIpXSkKZGVmIGM0X3RvX21h
bmRlbChUKToKICAgIHJldHVybiBucC5hcnJheShbW1RbaSwgaiwgaywgbF0gKiBfTUZbSV0gKiBf
TUZbSl0gZm9yIEosIChrLCBsKSBpbiBlbnVtZXJhdGUoVk9JR1QpXSBmb3IgSSwgKGksIGopIGlu
IGVudW1lcmF0ZShWT0lHVCldKQpkZWYgbWFuZGVsX3RvX2M0KE0pOiByZXR1cm4gdm9pZ3Q2Nl90
b19jNChNIC8gbnAub3V0ZXIoX01GLCBfTUYpKQpFNiA9IG5wLmFycmF5KFsxLjAsIDEsIDEsIDAs
IDAsIDBdKTsgSjYgPSBucC5vdXRlcihFNiwgRTYpIC8gMy4wOyBLNk0gPSBucC5leWUoNikgLSBK
NgpkZWYgaXNvX21hbmRlbChLLCBHKTogcmV0dXJuIDMgKiBLICogSjYgKyAyICogRyAqIEs2TQpk
ZWYgaXNvX0tHX29mX2M0KFQpOgogICAgSyA9IG5wLmVpbnN1bSgnaWlqai0+JywgVCkgLyA5LjA7
IEcgPSAobnAuZWluc3VtKCdpamlqLT4nLCBUKSAtIG5wLmVpbnN1bSgnaWlqai0+JywgVCkgLyAz
LjApIC8gMTAuMDsgcmV0dXJuIEssIEcKZGVmIHplbmVyX0goYyk6IHJldHVybiBjWydDMTEnXSAt
IGNbJ0MxMiddIC0gMi4wICogY1snQzQ0J10KCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gU08oMykg
cHJvZHVjdCBxdWFkcmF0dXJlICsgT0RGIGZhbWlsaWVzCmRlZiBzbzNfZ3JpZChuYSwgbmIsIG5n
KToKICAgIGFsID0gMiAqIG5wLnBpICogbnAuYXJhbmdlKG5hKSAvIG5hOyBnYSA9IDIgKiBucC5w
aSAqIG5wLmFyYW5nZShuZykgLyBuZwogICAgeGIsIHdiID0gbnAucG9seW5vbWlhbC5sZWdlbmRy
ZS5sZWdnYXVzcyhuYik7IHNiID0gbnAuc3FydCgxIC0geGIqKjIpCiAgICBScywgd3MgPSBbXSwg
W10KICAgIGZvciBhIGluIGFsOgogICAgICAgIFJhID0gbnAuYXJyYXkoW1ttYXRoLmNvcyhhKSwg
LW1hdGguc2luKGEpLCAwXSwgW21hdGguc2luKGEpLCBtYXRoLmNvcyhhKSwgMF0sIFswLCAwLCAx
XV0pCiAgICAgICAgZm9yIGliIGluIHJhbmdlKG5iKToKICAgICAgICAgICAgUmIgPSBucC5hcnJh
eShbW3hiW2liXSwgMCwgc2JbaWJdXSwgWzAsIDEsIDBdLCBbLXNiW2liXSwgMCwgeGJbaWJdXV0p
CiAgICAgICAgICAgIGZvciBnIGluIGdhOgogICAgICAgICAgICAgICAgUmcgPSBucC5hcnJheShb
W21hdGguY29zKGcpLCAtbWF0aC5zaW4oZyksIDBdLCBbbWF0aC5zaW4oZyksIG1hdGguY29zKGcp
LCAwXSwgWzAsIDAsIDFdXSkKICAgICAgICAgICAgICAgIFJzLmFwcGVuZChSYSBAIFJiIEAgUmcp
OyB3cy5hcHBlbmQod2JbaWJdIC8gKDIuMCAqIG5hICogbmcpKQogICAgcmV0dXJuIG5wLmFycmF5
KFJzKSwgbnAuYXJyYXkod3MpClNPMyA9IHNvM19ncmlkKDE2LCAxMCwgMTYpClNPM19ET1VCTEUg
PSBOb25lCmRlZiByb3RhdGVfYWxsKGM0LCBScyk6CiAgICB0ID0gbnAuZWluc3VtKCdnaWEsYWJj
ZC0+Z2liY2QnLCBScywgYzQsIG9wdGltaXplPVRydWUpOyB0ID0gbnAuZWluc3VtKCdnamIsZ2li
Y2QtPmdpamNkJywgUnMsIHQsIG9wdGltaXplPVRydWUpCiAgICB0ID0gbnAuZWluc3VtKCdna2Ms
Z2lqY2QtPmdpamtkJywgUnMsIHQsIG9wdGltaXplPVRydWUpOyByZXR1cm4gbnAuZWluc3VtKCdn
bGQsZ2lqa2QtPmdpamtsJywgUnMsIHQsIG9wdGltaXplPVRydWUpCmRlZiBQMih4KTogcmV0dXJu
IDAuNSAqICgzICogeCAqIHggLSAxKQpkZWYgUDQoeCk6IHJldHVybiAoMzUgKiB4Kio0IC0gMzAg
KiB4KioyICsgMykgLyA4LjAKZGVmIFA2KHgpOiByZXR1cm4gKDIzMSAqIHgqKjYgLSAzMTUgKiB4
Kio0ICsgMTA1ICogeCoqMiAtIDUpIC8gMTYuMApkZWYgSzR0aWxkZShScyk6CiAgICAiIiIoNS8y
KShzdW1faSAoZV9pIC4geileNCAtIDMvNSkgd2l0aCBlX2kgPSBSIGVfaSB0aGUgY3J5c3RhbCBh
eGVzIGluIHRoZSBsYWI6IChlX2kgLiB6KSA9IFJbMiwgaV0uIiIiCiAgICByZXR1cm4gMi41ICog
KG5wLnN1bShSc1s6LCAyLCA6XSoqNCwgYXhpcz0xKSAtIDAuNikKZGVmIEs2dGlsZGUoUnMpOgog
ICAgIiIiMjAgeCB0aGUgcHVyZSBsID0gNiBjdWJpYyBoYXJtb25pYyAoc3VtIHheNiAtICgxNS8x
MSkgc3VtIHheNCArIDMwLzc3KSBvZiB0aGUgZmliZXIgYXhpcyBpbiB0aGUgY3J5c3RhbCBmcmFt
ZTsgfEs2dHwgPCAxLiIiIgogICAgeiA9IFJzWzosIDIsIDpdOyByZXR1cm4gMjAuMCAqIChucC5z
dW0oeioqNiwgYXhpcz0xKSAtICgxNS4wIC8gMTEuMCkgKiBucC5zdW0oeioqNCwgYXhpcz0xKSAr
IDMwLjAgLyA3Ny4wKQpjbGFzcyBPREY6CiAgICAiIiJGaWJlci10ZXh0dXJlIHdlaWdodCBvbiBT
TygzKS4ga2luZDogJ2wyJyAoRy1NU0NTMTogMSArIHQgUDIoKGcgYXhpc19jKS56KSksICdLNCcg
KGN1YmljOiAxICsgdDQgSzR0KGcpIFsrIHQ2IEs2dF0pLAogICAgJ1A0JyAoaGV4OiAxICsgdDIg
UDIgKyB0NCBQNCArIHQ2IFA2IG9mIHRoZSBjLWF4aXMgYW5nbGUpLCAnaXNvJy4gQWxzbyBwcm92
aWRlcyB0aGUgZGVzY3JpcHRvci1heGlzIE1BUkdJTkFMIG9uIFNeMi4iIiIKICAgIGRlZiBfX2lu
aXRfXyhzZWxmLCBraW5kLCBheGlzX2M9WiwgdD0wLjAsIHQyPTAuMCwgdDQ9MC4wLCB0Nj0wLjAs
IGNtYXJnPTEuMCk6CiAgICAgICAgc2VsZi5raW5kLCBzZWxmLmF4aXNfYywgc2VsZi50LCBzZWxm
LnQyLCBzZWxmLnQ0LCBzZWxmLnQ2LCBzZWxmLmNtYXJnID0ga2luZCwgbnAuYXNhcnJheShheGlz
X2MsIGZsb2F0KSwgdCwgdDIsIHQ0LCB0NiwgY21hcmcKICAgIGRlZiB3X3NvMyhzZWxmLCBScyk6
CiAgICAgICAgaWYgc2VsZi5raW5kID09ICdpc28nOiByZXR1cm4gbnAub25lcyhsZW4oUnMpKQog
ICAgICAgIGlmIHNlbGYua2luZCA9PSAnbDInOiByZXR1cm4gMS4wICsgc2VsZi50ICogUDIoKFJz
IEAgc2VsZi5heGlzX2MpWzosIDJdKQogICAgICAgIGlmIHNlbGYua2luZCA9PSAnSzQnOiByZXR1
cm4gMS4wICsgc2VsZi50NCAqIEs0dGlsZGUoUnMpICsgc2VsZi50NiAqIEs2dGlsZGUoUnMpCiAg
ICAgICAgaWYgc2VsZi5raW5kID09ICdQNCc6CiAgICAgICAgICAgIHggPSAoUnMgQCBaKVs6LCAy
XTsgcmV0dXJuIDEuMCArIHNlbGYudDIgKiBQMih4KSArIHNlbGYudDQgKiBQNCh4KSArIHNlbGYu
dDYgKiBQNih4KQogICAgICAgIHJhaXNlIFZhbHVlRXJyb3Ioc2VsZi5raW5kKQogICAgZGVmIHdf
bWFyZyhzZWxmLCBuKToKICAgICAgICAiIiJNYXJnaW5hbCB3ZWlnaHQgb24gdGhlIGRlc2NyaXB0
b3IgYXhpcyBuIChTXjIpOiBsMiAtPiAxICsgdCBQMihuX3opOyBLNCAtPiAxICsgYyB0NCBQNChu
X3opICgrIHQ2IHRlcm0gaGFzIHplcm8gUDYtbW9tZW50CiAgICAgICAgYWdhaW5zdCBhIGRlZ3Jl
ZS00IHdlaWdodCwgc28gdGhlIGV4aGF1c3Rpb24gcHJvYmUgaXMgY2FycmllZCBhcyBjNiB0NiBQ
NiB3aXRoIGM2IGltbWF0ZXJpYWw6IGtlcHQgZm9yIHRoZSB0ZW5zb3IgcGF0aCBvbmx5KTsKICAg
ICAgICBQNCAtPiAxICsgdDIgUDIgKyB0NCBQNCArIHQ2IFA2LiIiIgogICAgICAgIHggPSBuWzos
IDJdCiAgICAgICAgaWYgc2VsZi5raW5kID09ICdpc28nOiByZXR1cm4gbnAub25lcyhsZW4obikp
CiAgICAgICAgaWYgc2VsZi5raW5kID09ICdsMic6IHJldHVybiAxLjAgKyBzZWxmLnQgKiBQMih4
KQogICAgICAgIGlmIHNlbGYua2luZCA9PSAnSzQnOiByZXR1cm4gMS4wICsgc2VsZi5jbWFyZyAq
IHNlbGYudDQgKiBQNCh4KSArIHNlbGYudDYgKiBQNih4KQogICAgICAgIGlmIHNlbGYua2luZCA9
PSAnUDQnOiByZXR1cm4gMS4wICsgc2VsZi50MiAqIFAyKHgpICsgc2VsZi50NCAqIFA0KHgpICsg
c2VsZi50NiAqIFA2KHgpCiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihzZWxmLmtpbmQpCmRlZiBv
ZGZfYXZnX2M0KGM0LCBvZGYsIGdyaWQ9Tm9uZSk6CiAgICBScywgd3MgPSBncmlkIGlmIGdyaWQg
aXMgbm90IE5vbmUgZWxzZSBTTzM7IHcgPSB3cyAqIG9kZi53X3NvMyhScykKICAgIHJldHVybiBu
cC5laW5zdW0oJ2csZ2lqa2wtPmlqa2wnLCB3LCByb3RhdGVfYWxsKGM0LCBScyksIG9wdGltaXpl
PVRydWUpCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIGFnZ3JlZ2F0ZSBzY2hlbWVzIChpbmhlcml0
ZWQpCmRlZiBjc3RhcihLMCwgRzApOgogICAgS3MgPSA0LjAgKiBHMCAvIDMuMDsgR3MgPSBHMCAq
ICg5ICogSzAgKyA4ICogRzApIC8gKDYuMCAqIChLMCArIDIgKiBHMCkpOyByZXR1cm4gaXNvX21h
bmRlbChLcywgR3MpCmRlZiBhZ2dyZWdhdGVfdGVuc29ycyhjNCwgb2RmLCBoc19yZWYsIGdyaWQ9
Tm9uZSk6CiAgICBDViA9IG9kZl9hdmdfYzQoYzQsIG9kZiwgZ3JpZCk7IFM0ID0gbWFuZGVsX3Rv
X2M0KG5wLmxpbmFsZy5pbnYoYzRfdG9fbWFuZGVsKGM0KSkpCiAgICBDUiA9IG1hbmRlbF90b19j
NChucC5saW5hbGcuaW52KGM0X3RvX21hbmRlbChvZGZfYXZnX2M0KFM0LCBvZGYsIGdyaWQpKSkp
OyBvdXQgPSB7J1YnOiBDViwgJ1InOiBDUiwgJ0gnOiAwLjUgKiAoQ1YgKyBDUil9CiAgICBpZiBo
c19yZWYgaXMgbm90IE5vbmU6CiAgICAgICAgaHMgPSB7fQogICAgICAgIGZvciB0YWcsIChLMCwg
RzApIGluIGhzX3JlZi5pdGVtcygpOgogICAgICAgICAgICBDcyA9IGNzdGFyKEswLCBHMCk7IGlu
diA9IG1hbmRlbF90b19jNChucC5saW5hbGcuaW52KGM0X3RvX21hbmRlbChjNCkgKyBDcykpCiAg
ICAgICAgICAgIGhzW3RhZ10gPSBtYW5kZWxfdG9fYzQobnAubGluYWxnLmludihjNF90b19tYW5k
ZWwob2RmX2F2Z19jNChpbnYsIG9kZiwgZ3JpZCkpKSAtIENzKQogICAgICAgIG91dFsnSFNsbydd
LCBvdXRbJ0hTaGknXSA9IGhzWydsbyddLCBoc1snaGknXTsgb3V0WydIUyddID0gMC41ICogKGhz
WydsbyddICsgaHNbJ2hpJ10pCiAgICByZXR1cm4gb3V0CmRlZiBoc19pc29fYm91bmQoYzQsIEsw
LCBHMCk6CiAgICBDcyA9IGNzdGFyKEswLCBHMCk7IGludiA9IG1hbmRlbF90b19jNChucC5saW5h
bGcuaW52KGM0X3RvX21hbmRlbChjNCkgKyBDcykpCiAgICBDID0gbWFuZGVsX3RvX2M0KG5wLmxp
bmFsZy5pbnYoYzRfdG9fbWFuZGVsKG9kZl9hdmdfYzQoaW52LCBPREYoJ2lzbycpKSkpIC0gQ3Mp
OyByZXR1cm4gaXNvX0tHX29mX2M0KEMpCmRlZiBmZWFzaWJsZShjNCwgSzAsIEcwLCB1cHBlcik6
CiAgICBEID0gaXNvX21hbmRlbChLMCwgRzApIC0gYzRfdG9fbWFuZGVsKGM0KTsgbGFtID0gbnAu
bGluYWxnLmVpZ3ZhbHNoKEQpOyBzY2FsZSA9IG5wLmFicyhjNF90b19tYW5kZWwoYzQpKS5tYXgo
KQogICAgcmV0dXJuIChsYW0ubWluKCkgPj0gLTFlLTExICogc2NhbGUpIGlmIHVwcGVyIGVsc2Ug
KGxhbS5tYXgoKSA8PSAxZS0xMSAqIHNjYWxlKQpkZWYgb3B0aW1pemVfaHNfcmVmZXJlbmNlKGM0
KToKICAgICIiIkctTVNDUzEgQS0yLjMgcHJvY2VkdXJlLCB2ZXJiYXRpbTogdGlnaHRlc3QgZmVh
c2libGUgV2FscG9sZSByZWZlcmVuY2VzIGF0IHQgPSAwIChncmlkICsgYmlzZWN0aW9uICsgZ29s
ZGVuIHNlY3Rpb24pLiIiIgogICAgS3YsIEd2ID0gaXNvX0tHX29mX2M0KGM0KTsgcmVmcyA9IHt9
CiAgICBmb3IgdXBwZXIgaW4gKFRydWUsIEZhbHNlKToKICAgICAgICBkZWYgS19hdChHMCk6CiAg
ICAgICAgICAgIGxvLCBoaSA9IDAuMCwgNTAuMCAqIEt2CiAgICAgICAgICAgIGlmIG5vdCAoZmVh
c2libGUoYzQsIGhpLCBHMCwgVHJ1ZSkgaWYgdXBwZXIgZWxzZSBmZWFzaWJsZShjNCwgbG8sIEcw
LCBGYWxzZSkpOiByZXR1cm4gTm9uZQogICAgICAgICAgICBmb3IgXyBpbiByYW5nZSg4MCk6CiAg
ICAgICAgICAgICAgICBtaWQgPSAwLjUgKiAobG8gKyBoaSk7IG9rID0gZmVhc2libGUoYzQsIG1p
ZCwgRzAsIHVwcGVyKQogICAgICAgICAgICAgICAgaWYgdXBwZXI6IGhpLCBsbyA9IChtaWQsIGxv
KSBpZiBvayBlbHNlIChoaSwgbWlkKQogICAgICAgICAgICAgICAgZWxzZTogICAgIGxvLCBoaSA9
IChtaWQsIGhpKSBpZiBvayBlbHNlIChsbywgbWlkKQogICAgICAgICAgICByZXR1cm4gaGkgaWYg
dXBwZXIgZWxzZSBsbwogICAgICAgIGV2YWxzID0ge30KICAgICAgICBkZWYgZihHMCk6CiAgICAg
ICAgICAgIGlmIEcwIGluIGV2YWxzOiByZXR1cm4gZXZhbHNbRzBdWzBdCiAgICAgICAgICAgIEsw
ID0gS19hdChHMCk7IHZhbCA9IDFlMzAwIGlmIEswIGlzIE5vbmUgZWxzZSAoaHNfaXNvX2JvdW5k
KGM0LCBLMCwgRzApWzFdICogKDEgaWYgdXBwZXIgZWxzZSAtMSkpOyBldmFsc1tHMF0gPSAodmFs
LCBLMCk7IHJldHVybiB2YWwKICAgICAgICBncmlkID0gbnAubGluc3BhY2UoMC4yICogR3YsIDQu
MCAqIEd2LCAxNjApCiAgICAgICAgZm9yIEcwIGluIGdyaWQ6IGYoZmxvYXQoRzApKQogICAgICAg
IGZlYXMgPSBbRzAgZm9yIEcwIGluIGV2YWxzIGlmIGV2YWxzW0cwXVsxXSBpcyBub3QgTm9uZV07
IGJlc3QgPSBtaW4oZmVhcywga2V5PWxhbWJkYSBHMDogZXZhbHNbRzBdWzBdKQogICAgICAgIGkg
PSBsaXN0KGdyaWQpLmluZGV4KG1pbihncmlkLCBrZXk9bGFtYmRhIHg6IGFicyh4IC0gYmVzdCkp
KQogICAgICAgIGEsIGIgPSBmbG9hdChncmlkW21heChpIC0gMSwgMCldKSwgZmxvYXQoZ3JpZFtt
aW4oaSArIDEsIGxlbihncmlkKSAtIDEpXSk7IHBoaSA9IChtYXRoLnNxcnQoNSkgLSAxKSAvIDIK
ICAgICAgICB4MSwgeDIgPSBiIC0gcGhpICogKGIgLSBhKSwgYSArIHBoaSAqIChiIC0gYSkKICAg
ICAgICBmb3IgXyBpbiByYW5nZSg3MCk6CiAgICAgICAgICAgIGlmIGYoeDEpIDwgZih4Mik6IGIs
IHgyID0geDIsIHgxOyB4MSA9IGIgLSBwaGkgKiAoYiAtIGEpCiAgICAgICAgICAgIGVsc2U6IGEs
IHgxID0geDEsIHgyOyB4MiA9IGEgKyBwaGkgKiAoYiAtIGEpCiAgICAgICAgZmVhcyA9IFtHMCBm
b3IgRzAgaW4gZXZhbHMgaWYgZXZhbHNbRzBdWzFdIGlzIG5vdCBOb25lXTsgYmVzdCA9IG1pbihm
ZWFzLCBrZXk9bGFtYmRhIEcwOiBldmFsc1tHMF1bMF0pCiAgICAgICAgcmVmc1snaGknIGlmIHVw
cGVyIGVsc2UgJ2xvJ10gPSAoZmxvYXQoZXZhbHNbYmVzdF1bMV0pLCBmbG9hdChiZXN0KSkKICAg
IHJldHVybiByZWZzCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIGstc3BoZXJlICsgQ2hyaXN0b2Zm
ZWwgKyBkZXNjcmlwdG9ycyAoaW5oZXJpdGVkKQpkZWYgc3BoZXJlX2dyaWQobnQsIG5waGkpOgog
ICAgeCwgdyA9IG5wLnBvbHlub21pYWwubGVnZW5kcmUubGVnZ2F1c3MobnQpOyBwaCA9IDIgKiBu
cC5waSAqIG5wLmFyYW5nZShucGhpKSAvIG5waGkKICAgIGN0LCBjcCA9IG5wLm1lc2hncmlkKHgs
IG5wLmNvcyhwaCksIGluZGV4aW5nPSdpaicpOyBzdCA9IG5wLnNxcnQoMSAtIGN0KioyKTsgc3Ag
PSBucC5zaW4obnAubWVzaGdyaWQoeCwgcGgsIGluZGV4aW5nPSdpaicpWzFdKQogICAgSyA9IG5w
LnN0YWNrKFtzdCAqIGNwLCBzdCAqIHNwLCBjdF0sIC0xKS5yZXNoYXBlKC0xLCAzKTsgVyA9IChu
cC5yZXBlYXQodywgbnBoaSkgLyAoMi4wICogbnBoaSkpOyByZXR1cm4gSywgVwpkZWYgbW9kZXMo
YzQsIEspOgogICAgRyA9IG5wLmVpbnN1bSgnaWprbCxuaixubC0+bmlrJywgYzQsIEssIEssIG9w
dGltaXplPVRydWUpOyB2YWwsIHZlYyA9IG5wLmxpbmFsZy5laWdoKEcpCiAgICByZXR1cm4gbnAu
c3FydChucC5tYXhpbXVtKHZhbCwgMC4wKSksIG5wLnRyYW5zcG9zZSh2ZWMsICgwLCAyLCAxKSkK
ZGVmIGRlc2NyaXB0b3JzKEssIGUpOgogICAga2UgPSBucC5laW5zdW0oJ25pLG5iaS0+bmInLCBL
LCBlKTsgbGFtID0ga2UqKjI7IHdfZW0gPSAxLjAgLSBsYW0KICAgIGVwZXJwID0gZSAtIGtlWy4u
LiwgTm9uZV0gKiBLWzosIE5vbmUsIDpdCiAgICBTcCA9IDAuNSAqIChucC5laW5zdW0oJ25pLG5i
ai0+bmJpaicsIEssIGVwZXJwKSArIG5wLmVpbnN1bSgnbmJpLG5qLT5uYmlqJywgZXBlcnAsIEsp
KQogICAgd19oID0gKDEuMCAtIGxhbSkgLyAoMS4wICsgbGFtIC8gMy4wKTsgcmV0dXJuIGxhbSwg
d19lbSwgU3AsIHdfaApkZWYgZnJhY19FMihTcCwgbik6CiAgICBTbiA9IG5wLmVpbnN1bSgnLi4u
aWosbWotPi4uLm1pJywgU3AsIG4pOyBuU24gPSBucC5laW5zdW0oJy4uLm1pLG1pLT4uLi5tJywg
U24sIG4pOyBTbjIgPSBucC5laW5zdW0oJy4uLm1pLC4uLm1pLT4uLi5tJywgU24sIFNuKQogICAg
bm9ybSA9IG5wLmVpbnN1bSgnLi4uaWosLi4uaWotPi4uLicsIFNwLCBTcClbLi4uLCBOb25lXQog
ICAgd2l0aCBucC5lcnJzdGF0ZShkaXZpZGU9J2lnbm9yZScsIGludmFsaWQ9J2lnbm9yZScpOgog
ICAgICAgIGYgPSAxLjAgLSAyLjAgKiBTbjIgLyBub3JtICsgMC41ICogblNuKioyIC8gbm9ybQog
ICAgcmV0dXJuIG5wLndoZXJlKG5vcm0gPiAxZS0zMDAsIGYsIDAuMCkKTkdSSUQgPSBzcGhlcmVf
Z3JpZCgxMiwgMjQpCmRlZiBvZGZfYXZnX2ZyYWNFMihTcCwgb2RmKToKICAgIG4sIHduID0gTkdS
SUQ7IGYgPSBmcmFjX0UyKFNwLCBuKTsgdyA9IHduICogb2RmLndfbWFyZyhuKTsgcmV0dXJuIG5w
LmVpbnN1bSgnLi4ubSxtLT4uLi4nLCBmLCB3KSAvIG5wLnN1bSh3KQpkZWYgc28zX2RpcmVjdF9m
cmFjRTIoU3AsIG9kZiwgYXhpc19jLCBjaHVuaz01MTIpOgogICAgIiIiU08oMyktZGlyZWN0IE9E
RiBhdmVyYWdlIG9mIHRoZSBwZXItZ3JhaW4gRTIgZnJhY3Rpb246IHRoZSBkZXNjcmlwdG9yIGF4
aXMgbiA9IGcgYXhpc19jIGNhcnJpZWQgYWxvbmcgdGhlIGZ1bGwgb3JpZW50YXRpb24uIiIiCiAg
ICBScywgd3MgPSBTTzM7IHcgPSB3cyAqIG9kZi53X3NvMyhScyk7IG5fYWxsID0gUnMgQCBheGlz
X2M7IG91dCA9IG5wLnplcm9zKFNwLnNoYXBlWzotMl0pOyB0b3QgPSAwLjAKICAgIGZvciBzIGlu
IHJhbmdlKDAsIGxlbihScyksIGNodW5rKToKICAgICAgICBvdXQgKz0gbnAuZWluc3VtKCcuLi5t
LG0tPi4uLicsIGZyYWNfRTIoU3AsIG5fYWxsW3M6cyArIGNodW5rXSksIHdbczpzICsgY2h1bmtd
KTsgdG90ICs9IGZsb2F0KG5wLnN1bSh3W3M6cyArIGNodW5rXSkpCiAgICByZXR1cm4gb3V0IC8g
dG90CmRlZiBsYWJlbF9icmFuY2hlcyhzeW0sIEssIGUsIGxhbSwgdik6CiAgICBuayA9IEsuc2hh
cGVbMF07IGxhYiA9IG5wLmZ1bGwoKG5rLCAzKSwgLTEsIGR0eXBlPWludCk7IGlMID0gbnAuYXJn
bWF4KGxhbSwgYXhpcz0xKQogICAgaWYgc3ltID09ICdoZXgnOgogICAgICAgIHprID0gbnAuY3Jv
c3MobnAuYnJvYWRjYXN0X3RvKFosIEsuc2hhcGUpLCBLKTsgbnJtID0gbnAubGluYWxnLm5vcm0o
emssIGF4aXM9MSk7IHprID0gemsgLyBucC53aGVyZShucm0gPiAwLCBucm0sIDEpWzosIE5vbmVd
CiAgICAgICAgb3YgPSBucC5hYnMobnAuZWluc3VtKCduYmksbmktPm5iJywgZSwgemspKTsgaVNI
ID0gbnAuYXJnbWF4KG92LCBheGlzPTEpCiAgICAgICAgZm9yIG4gaW4gcmFuZ2UobmspOgogICAg
ICAgICAgICByZXN0ID0gW2IgZm9yIGIgaW4gcmFuZ2UoMykgaWYgYiAhPSBpU0hbbl1dOyBsID0g
cmVzdFtpbnQobnAuYXJnbWF4KGxhbVtuLCByZXN0XSkpXTsgcyA9IFtiIGZvciBiIGluIHJlc3Qg
aWYgYiAhPSBsXVswXQogICAgICAgICAgICBsYWJbbiwgaVNIW25dXSA9IDA7IGxhYltuLCBzXSA9
IDE7IGxhYltuLCBsXSA9IDIKICAgIGVsc2U6CiAgICAgICAgZm9yIG4gaW4gcmFuZ2UobmspOgog
ICAgICAgICAgICByZXN0ID0gW2IgZm9yIGIgaW4gcmFuZ2UoMykgaWYgYiAhPSBpTFtuXV07IGYs
IHMgPSAocmVzdCBpZiB2W24sIHJlc3RbMF1dID49IHZbbiwgcmVzdFsxXV0gZWxzZSByZXN0Wzo6
LTFdKQogICAgICAgICAgICBsYWJbbiwgZl0gPSAwOyBsYWJbbiwgc10gPSAxOyBsYWJbbiwgaUxb
bl1dID0gMgogICAgcmV0dXJuIGxhYgpMQUJFTFMgPSB7J2hleCc6IFsncVNIJywgJ3FTVicsICdx
TCddLCAnY3ViaWMnOiBbJ3FUMScsICdxVDInLCAncUwnXX0KZGVmIHNwZWNpZXNfc3RhdHMoc3lt
LCBjNCwgSywgVywgb2RmPU5vbmUsIGF4aXNfbGFiPU5vbmUsIHdhbnRfbGFiZWxzPVRydWUpOgog
ICAgIiIiU2luZ2xlIGNyeXN0YWwgKG9kZiBOb25lKTogUzItRTIgYWJvdXQgdGhlIGZpeGVkIGxh
YiBheGlzIGF4aXNfbGFiOyBhZ2dyZWdhdGUgKG9kZiBnaXZlbik6IG1hcmdpbmFsLU9ERi1hdmVy
YWdlZCBFMiB3ZWlnaHQuIiIiCiAgICB2LCBlID0gbW9kZXMoYzQsIEspOyBsYW0sIHdfZW0sIFNw
LCB3X2ggPSBkZXNjcmlwdG9ycyhLLCBlKQogICAgZiA9IGZyYWNfRTIoU3AsIGF4aXNfbGFiW05v
bmUsIDpdKVsuLi4sIDBdIGlmIG9kZiBpcyBOb25lIGVsc2Ugb2RmX2F2Z19mcmFjRTIoU3AsIG9k
ZikKICAgIHdfZTIgPSB3X2VtICogZjsgV2IgPSBXWzosIE5vbmVdCiAgICBkZWYgbWVhbih3KTog
cmV0dXJuIGZsb2F0KG5wLnN1bShXYiAqIHcgKiB2KSAvIG5wLnN1bShXYiAqIHcpKQogICAgdkVN
LCB2RTIsIHZIID0gbWVhbih3X2VtKSwgbWVhbih3X2UyKSwgbWVhbih3X2gpCiAgICBvdXQgPSB7
J3ZfRU0nOiB2RU0sICd2X1MyRTInOiB2RTIsICd2X1MyaCc6IHZILCAncl94dGFsX0UyJzogdkUy
IC8gdkVNIC0gMS4wLCAncl94dGFsX2gnOiB2SCAvIHZFTSAtIDEuMH0KICAgIGlmIHdhbnRfbGFi
ZWxzOgogICAgICAgIGxhYiA9IGxhYmVsX2JyYW5jaGVzKHN5bSwgSywgZSwgbGFtLCB2KTsgcVQg
PSBsYWIgPCAyOyBsYW1UID0gbnAud2hlcmUocVQsIGxhbSwgbnAubmFuKQogICAgICAgIG91dFsn
bGFtYmRhX21lYW4nXSA9IGZsb2F0KG5wLm5hbnN1bShXYiAqIGxhbVQpIC8gbnAuc3VtKFdiICog
cVQpKQogICAgICAgIGltID0gbnAudW5yYXZlbF9pbmRleChucC5uYW5hcmdtYXgobnAud2hlcmUo
cVQsIGxhbSwgLTEuMCkpLCBsYW0uc2hhcGUpOyBvdXRbJ2xhbWJkYV9tYXgnXSA9IGZsb2F0KGxh
bVtpbV0pOyBvdXRbJ2xhbWJkYV9tYXhfYnJhbmNoJ10gPSBMQUJFTFNbc3ltXVtsYWJbaW1dXQog
ICAgcmV0dXJuIG91dAoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBmaXRzCmRlZiBmaXRfcih0LCBy
LCBiYXNpcz0oMSwgMiwgMykpOgogICAgQSA9IG5wLnN0YWNrKFtucC5hcnJheSh0KSoqayBmb3Ig
ayBpbiBiYXNpc10sIDEpOyBjb2VmLCAqXyA9IG5wLmxpbmFsZy5sc3RzcShBLCBucC5hcnJheShy
KSwgcmNvbmQ9Tm9uZSkKICAgIHJldHVybiBjb2VmLCBmbG9hdChucC5zcXJ0KG5wLm1lYW4oKEEg
QCBjb2VmIC0gbnAuYXJyYXkocikpKioyKSkpCmRlZiBmaXRfcXVhZGZvcm0odDJzLCB0NHMsIHIp
OgogICAgQSA9IG5wLnN0YWNrKFt0MnMqKjIsIHQycyAqIHQ0cywgdDRzKioyLCB0MnMqKjMsIHQy
cyoqMiAqIHQ0cywgdDJzICogdDRzKioyLCB0NHMqKjNdLCAxKTsgY29lZiwgKl8gPSBucC5saW5h
bGcubHN0c3EoQSwgciwgcmNvbmQ9Tm9uZSkKICAgIHJldHVybiB7J2thcHBhMjInOiBmbG9hdChj
b2VmWzBdKSwgJ2thcHBhMjQnOiBmbG9hdChjb2VmWzFdKSwgJ2thcHBhNDQnOiBmbG9hdChjb2Vm
WzJdKSwgJ3Jlc2lkdWFsJzogZmxvYXQobnAuc3FydChucC5tZWFuKChBIEAgY29lZiAtIHIpKioy
KSkpfQoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBjb25maWd1cmF0aW9uIGhlbHBlcnMKZGVmIGNv
bmZpZ19rZXlzKGNmZyk6CiAgICByZXR1cm4gWyhjZmcgKyAnfGEnLCBGYWxzZSwgWiwgMS4wKSwg
KGNmZyArICd8YicsIFRydWUsIFosIDEuMCldIGlmIGNmZy5zdGFydHN3aXRoKCdoZXgnKSBlbHNl
IFsoY2ZnICsgJ3wwMDEnLCBGYWxzZSwgWiwgMS4wKSwgKGNmZyArICd8MTExJywgRmFsc2UsIEFY
MTExLCAtMi4wIC8gMy4wKV0KZGVmIGZhbWlseShzeW0sIGF4aXNfYywgY21hcmcsICoqa3cpOgog
ICAgcmV0dXJuIE9ERignSzQnLCBheGlzX2M9YXhpc19jLCBjbWFyZz1jbWFyZywgKiprdykgaWYg
c3ltID09ICdjdWJpYycgZWxzZSBPREYoJ1A0JywgYXhpc19jPWF4aXNfYywgKiprdykKZGVmIHJf
YWdnX29mKHN5bSwgYzQsIG9kZiwgSywgVywgaHNfcmVmLCBzY2hlbWVzPSgnSCcsKSk6CiAgICBh
ZyA9IGFnZ3JlZ2F0ZV90ZW5zb3JzKGM0LCBvZGYsIGhzX3JlZik7IHJldHVybiB7czogc3BlY2ll
c19zdGF0cyhzeW0sIGFnW3NdLCBLLCBXLCBvZGYsIHdhbnRfbGFiZWxzPUZhbHNlKSBmb3IgcyBp
biBzY2hlbWVzfSwgYWcKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gUGhhc2UgMApkZWYgcGhhc2Uw
KHZyaCwgeDYsIEssIFcpOgogICAgQyA9IHt9OyBoc19yZWZzID0ge30KICAgIHg2cDEsIHg2cDIs
IHg2cGlucyA9IHg2WydwaGFzZTEnXSwgeDZbJ3BoYXNlMiddLCB4NlsncGluc192cmgwJ10KICAg
ICMgUElOLVhUQUwKICAgIHdvcnN0ID0gMC4wOyB4dGFsID0ge30KICAgIGZvciBjZmcsIChzeW0s
IHZrKSBpbiBDT05GSUdTLml0ZW1zKCk6CiAgICAgICAgZm9yIGtleSwgc3ltbSwgYXhpcywgY20g
aW4gY29uZmlnX2tleXMoY2ZnKToKICAgICAgICAgICAgYzQgPSBjNF9mcm9tX2NvbnN0YW50cyhz
eW0sIHZyaFt2a11bJ0Nfb3Zlcl9yaG8nXSwgc3ltbSk7IHN0ID0gc3BlY2llc19zdGF0cyhzeW0s
IGM0LCBLLCBXLCBOb25lLCBheGlzKTsgeHRhbFtrZXldID0gc3QKICAgICAgICAgICAgZm9yIGYg
aW4gKCdyX3h0YWxfRTInLCAncl94dGFsX2gnLCAnbGFtYmRhX21lYW4nLCAnbGFtYmRhX21heCcp
OiB3b3JzdCA9IG1heCh3b3JzdCwgcmVsKHN0W2ZdLCB4NnAxW2tleV1bZl0pKQogICAgQ1snUElO
LVhUQUwnXSA9IHsnd29yc3RfcmVsJzogd29yc3QsICdwYXNzZWQnOiBib29sKHdvcnN0IDw9IDFl
LTgpfQogICAgIyBQSU4tVlJIMCAvIFBJTi1IUzAKICAgIHd2ID0gd2hzID0gMC4wOyB2dDAgPSB7
fQogICAgZm9yIGNmZywgKHN5bSwgdmspIGluIENPTkZJR1MuaXRlbXMoKToKICAgICAgICBjNCA9
IGM0X2Zyb21fY29uc3RhbnRzKHN5bSwgdnJoW3ZrXVsnQ19vdmVyX3JobyddKTsgcmVmcyA9IG9w
dGltaXplX2hzX3JlZmVyZW5jZShjNCk7IGhzX3JlZnNbY2ZnXSA9IHJlZnMKICAgICAgICBmb3Ig
a2V5LCBzeW1tLCBheGlzLCBjbSBpbiBjb25maWdfa2V5cyhjZmcpOgogICAgICAgICAgICBjNGsg
PSBjNF9mcm9tX2NvbnN0YW50cyhzeW0sIHZyaFt2a11bJ0Nfb3Zlcl9yaG8nXSwgc3ltbSk7IGFn
ID0gYWdncmVnYXRlX3RlbnNvcnMoYzRrLCBPREYoJ2lzbycpLCByZWZzKQogICAgICAgICAgICB2
VCA9IHtrOiBtYXRoLnNxcnQoaXNvX0tHX29mX2M0KGFnW2tdKVsxXSkgZm9yIGsgaW4gKCdWJywg
J1InLCAnSCcsICdIU2xvJywgJ0hTaGknKX07IHZ0MFtrZXldID0gdlQKICAgICAgICAgICAgd3Yg
PSBtYXgod3YsIHJlbCh2VFsnSCddLCB4NnAyW2tleV1bJ3ZUX1ZSSCddKSwgcmVsKHZUWydWJ10s
IHg2cDJba2V5XVsndlRfViddKSwgcmVsKHZUWydSJ10sIHg2cDJba2V5XVsndlRfUiddKSkKICAg
ICAgICAgICAgd2hzID0gbWF4KHdocywgcmVsKHZUWydIU2xvJ10sIHg2cDJba2V5XVsndlRfSFNf
bG8nXSksIHJlbCh2VFsnSFNoaSddLCB4NnAyW2tleV1bJ3ZUX0hTX2hpJ10pKQogICAgICAgIEds
byA9IGhzX2lzb19ib3VuZChjNCwgKnJlZnNbJ2xvJ10pWzFdOyBHaGkgPSBoc19pc29fYm91bmQo
YzQsICpyZWZzWydoaSddKVsxXTsgYiA9IHg2cGluc1tjZmddWydHX0hTJ107IHdocyA9IG1heCh3
aHMsIHJlbChHbG8sIGJbMF0pLCByZWwoR2hpLCBiWzFdKSkKICAgIENbJ1BJTi1WUkgwJ10gPSB7
J3dvcnN0X3JlbCc6IHd2LCAncGFzc2VkJzogYm9vbCh3diA8PSAxZS04KX07IENbJ1BJTi1IUzAn
XSA9IHsnd29yc3RfcmVsJzogd2hzLCAncGFzc2VkJzogYm9vbCh3aHMgPD0gMWUtNil9CiAgICAj
IFBJTi1LMjogdGhlIGwgPSAyIGZhbWlseSB3aXRoIEctTVNDUzEncyBncmlkL3dpbmRvdy9maXQg
cmVwcm9kdWNlcyBrYXBwYTIgKGhleCByZWwgPD0gMWUtNDsgY3ViaWMgYWJzIDw9IDFlLTEyKQog
ICAgVF9HUklEMSA9IFstMC41LCAtMC4yNSwgLTAuMSwgLTAuMDUsIC0wLjAyLCAwLjAsIDAuMDIs
IDAuMDUsIDAuMSwgMC4yNSwgMC41LCAxLjBdOyB3aGV4ID0gMC4wOyB3Y3ViID0gMC4wOyBrMiA9
IHt9CiAgICBmb3IgY2ZnLCAoc3ltLCB2aykgaW4gQ09ORklHUy5pdGVtcygpOgogICAgICAgIGZv
ciBrZXksIHN5bW0sIGF4aXMsIGNtIGluIGNvbmZpZ19rZXlzKGNmZyk6CiAgICAgICAgICAgIGM0
ID0gYzRfZnJvbV9jb25zdGFudHMoc3ltLCB2cmhbdmtdWydDX292ZXJfcmhvJ10sIHN5bW0pOyBy
RTIgPSBbXQogICAgICAgICAgICBmb3IgdCBpbiBUX0dSSUQxOgogICAgICAgICAgICAgICAgcnMs
IF8gPSByX2FnZ19vZihzeW0sIGM0LCBPREYoJ2wyJywgYXhpc19jPWF4aXMsIHQ9dCksIEssIFcs
IE5vbmUsICgnSCcsKSk7IHJFMi5hcHBlbmQocnNbJ0gnXVsncl94dGFsX0UyJ10pCiAgICAgICAg
ICAgIGlkeCA9IFtpIGZvciBpLCB0IGluIGVudW1lcmF0ZShUX0dSSUQxKSBpZiBhYnModCkgPD0g
MC4yNSArIDFlLTEyXTsgY0UsIF8gPSBmaXRfcihbVF9HUklEMVtpXSBmb3IgaSBpbiBpZHhdLCBb
ckUyW2ldIGZvciBpIGluIGlkeF0pOyBrMltrZXldID0gZmxvYXQoY0VbMV0pCiAgICAgICAgICAg
IGlmIHN5bSA9PSAnaGV4Jzogd2hleCA9IG1heCh3aGV4LCByZWwoazJba2V5XSwgeDZwMltrZXld
WydrYXBwYTJfRTInXSkpCiAgICAgICAgICAgIGVsc2U6IHdjdWIgPSBtYXgod2N1YiwgYWJzKGsy
W2tleV0pKQogICAgICAgICAgICBwcmludChmJyAgUElOLUsyIHtrZXk6MTZ9IGthcHBhMj17azJb
a2V5XTorLjllfSAgWC02IHt4NnAyW2tleV1bImthcHBhMl9FMiJdOisuOWV9JywgZmx1c2g9VHJ1
ZSkKICAgIENbJ1BJTi1LMiddID0geyd3b3JzdF9yZWxfaGV4X2thcHBhMic6IHdoZXgsICd3b3Jz
dF9hYnNfY3ViaWNfa2FwcGEyJzogd2N1YiwgJ2thcHBhMl9FMl9yZWNvbXB1dGVkJzogazIsICdw
YXNzZWQnOiBib29sKHdoZXggPD0gMWUtNCBhbmQgd2N1YiA8PSAxZS0xMil9CiAgICAjIEYtQ1RS
TC1JU08KICAgIEtpc28sIEdpc28gPSAxMzQuNjA5LCA3MC44ODE7IGNfaXNvID0gYzRfZnJvbV9j
b25zdGFudHMoJ2N1YmljJywgeydDMTEnOiBLaXNvICsgNCAqIEdpc28gLyAzLCAnQzEyJzogS2lz
byAtIDIgKiBHaXNvIC8gMywgJ0M0NCc6IEdpc299KQogICAgc3QgPSBzcGVjaWVzX3N0YXRzKCdj
dWJpYycsIGNfaXNvLCBLLCBXLCBOb25lLCBaKTsgd29yc3QgPSBtYXgoYWJzKHN0WydyX3h0YWxf
RTInXSksIGFicyhzdFsncl94dGFsX2gnXSksIHN0WydsYW1iZGFfbWF4J10pCiAgICBmb3IgdDQg
aW4gVDRfR1JJRDoKICAgICAgICBmb3Igb2RmIGluIChPREYoJ0s0JywgdDQ9dDQpLCBPREYoJ1A0
JywgdDQ9dDQpKToKICAgICAgICAgICAgcnMsIF8gPSByX2FnZ19vZignY3ViaWMnLCBjX2lzbywg
b2RmLCBLLCBXLCBOb25lKTsgd29yc3QgPSBtYXgod29yc3QsIGFicyhyc1snSCddWydyX3h0YWxf
RTInXSksIGFicyhyc1snSCddWydyX3h0YWxfaCddKSkKICAgIENbJ0YtQ1RSTC1JU08nXSA9IHsn
d29yc3RfYWJzJzogZmxvYXQod29yc3QpLCAncGFzc2VkJzogYm9vbCh3b3JzdCA8PSAxZS0xMCl9
CiAgICAjIEYtQ1RSTC1TTzMKICAgIGM0ID0gYzRfZnJvbV9jb25zdGFudHMoJ2hleCcsIHZyaFsn
aGV4OnN0ZXAnXVsnQ19vdmVyX3JobyddKTsgYWcgPSBhZ2dyZWdhdGVfdGVuc29ycyhjNCwgT0RG
KCdpc28nKSwgTm9uZSk7IHYsIGUgPSBtb2RlcyhhZ1snSCddLCBLKTsgbGFtLCB3X2VtLCBTcCwg
XyA9IGRlc2NyaXB0b3JzKEssIGUpCiAgICBmID0gb2RmX2F2Z19mcmFjRTIoU3AsIE9ERignaXNv
JykpOyBkZXYgPSBmbG9hdChucC5tYXgobnAuYWJzKGZbd19lbSA+IDFlLTZdIC0gMC40KSkpOyBy
MCA9IHNwZWNpZXNfc3RhdHMoJ2hleCcsIGFnWydIJ10sIEssIFcsIE9ERignUDQnLCB0ND0wLjAp
LCB3YW50X2xhYmVscz1GYWxzZSlbJ3JfeHRhbF9FMiddCiAgICBDWydGLUNUUkwtU08zJ10gPSB7
J2Rldl9mcm9tXzBwNCc6IGRldiwgJ3JfYWdnXzBfYWJzJzogYWJzKHIwKSwgJ3Bhc3NlZCc6IGJv
b2woZGV2IDw9IDFlLTEwIGFuZCBhYnMocjApIDw9IFRBVSl9CiAgICAjIEYtQ1RSTC1QT1MKICAg
IFJzLCB3cyA9IFNPMzsgd21pbiA9IG1pbihbZmxvYXQobnAubWluKE9ERignSzQnLCB0ND10NCku
d19zbzMoUnMpKSkgZm9yIHQ0IGluIFQ0X0dSSURdICsgW2Zsb2F0KG5wLm1pbihPREYoJ1A0Jywg
dDQ9dDQpLndfc28zKFJzKSkpIGZvciB0NCBpbiBUNF9HUklEXQogICAgICAgICAgICAgICAgICAg
ICAgICAgKyBbZmxvYXQobnAubWluKE9ERignUDQnLCB0Mj1hLCB0ND1iKS53X3NvMyhScykpKSBm
b3IgYSBpbiBUMlQ0IGZvciBiIGluIFQyVDRdICsgW2Zsb2F0KG5wLm1pbihPREYoJ0s0JywgdDQ9
MC4zLCB0Nj0wLjMpLndfc28zKFJzKSkpLCBmbG9hdChucC5taW4oT0RGKCdQNCcsIHQ0PTAuMywg
dDY9MC4zKS53X3NvMyhScykpKV0pCiAgICBDWydGLUNUUkwtUE9TJ10gPSB7J21pbl9vZGZfd2Vp
Z2h0Jzogd21pbiwgJ3Bhc3NlZCc6IGJvb2wod21pbiA+PSAwLjApfQogICAgIyBGLUNUUkwtTDJO
VUxMIChjdWJpYyk6IGwyIGF0IHQgPSAxIGFuZCB0aGUgbWl4ZWQgKHQyLCB0NCkgbGVhdmUgdGVu
c29ycyBhbmQgcl9hZ2cgdW5jaGFuZ2VkCiAgICB3b3JzdCA9IDAuMAogICAgZm9yIGNmZyBpbiAo
J2N1YmljX3N0ZXAnLCAnY3ViaWNfZ2VtOCcpOgogICAgICAgIHN5bSwgdmsgPSBDT05GSUdTW2Nm
Z107IHJlZnMgPSBoc19yZWZzW2NmZ10KICAgICAgICBmb3Iga2V5LCBzeW1tLCBheGlzLCBjbSBp
biBjb25maWdfa2V5cyhjZmcpOgogICAgICAgICAgICBjNCA9IGM0X2Zyb21fY29uc3RhbnRzKHN5
bSwgdnJoW3ZrXVsnQ19vdmVyX3JobyddKTsgc2NhbGUgPSBucC5hYnMoYzQpLm1heCgpCiAgICAg
ICAgICAgIGEwID0gYWdncmVnYXRlX3RlbnNvcnMoYzQsIE9ERignaXNvJyksIHJlZnMpOyBhMSA9
IGFnZ3JlZ2F0ZV90ZW5zb3JzKGM0LCBPREYoJ2wyJywgYXhpc19jPWF4aXMsIHQ9MS4wKSwgcmVm
cykKICAgICAgICAgICAgZm9yIHMgaW4gKCdWJywgJ1InLCAnSFMnKTogd29yc3QgPSBtYXgod29y
c3QsIGZsb2F0KG5wLmFicyhhMVtzXSAtIGEwW3NdKS5tYXgoKSkgLyBzY2FsZSkKICAgICAgICAg
ICAgcjAgPSBzcGVjaWVzX3N0YXRzKHN5bSwgYTBbJ0gnXSwgSywgVywgT0RGKCdpc28nKSwgd2Fu
dF9sYWJlbHM9RmFsc2UpWydyX3h0YWxfRTInXTsgcjEgPSBzcGVjaWVzX3N0YXRzKHN5bSwgYTFb
J0gnXSwgSywgVywgT0RGKCdpc28nKSwgd2FudF9sYWJlbHM9RmFsc2UpWydyX3h0YWxfRTInXQog
ICAgICAgICAgICB3b3JzdCA9IG1heCh3b3JzdCwgYWJzKHIxIC0gcjApKQogICAgICAgICAgICAj
IG1peGVkOiBhIFAyIHRlcm0gb24gdGhlIGN1YmljIGRlc2NyaXB0b3IgYXhpcyBhZGRlZCB0byB0
aGUgSzQgZmFtaWx5IG11c3QgY2hhbmdlIG5vdGhpbmcgb24gdGhlIHRlbnNvciBzaWRlCiAgICAg
ICAgICAgIGIwID0gYWdncmVnYXRlX3RlbnNvcnMoYzQsIE9ERignSzQnLCBheGlzX2M9YXhpcywg
Y21hcmc9Y20sIHQ0PTAuMjUpLCByZWZzKQogICAgICAgICAgICBtaXhlZCA9IE9ERignSzQnLCBh
eGlzX2M9YXhpcywgY21hcmc9Y20sIHQ0PTAuMjUpOyB3bWl4ID0gbGFtYmRhIFJzLCBtPW1peGVk
OiBtLndfc28zKFJzKSArIDAuMjUgKiBQMigoUnMgQCBheGlzKVs6LCAyXSkKICAgICAgICAgICAg
Y2xhc3MgX00oT0RGKToKICAgICAgICAgICAgICAgIGRlZiB3X3NvMyhzZWxmLCBScyk6IHJldHVy
biBtaXhlZC53X3NvMyhScykgKyAwLjI1ICogUDIoKFJzIEAgYXhpcylbOiwgMl0pCiAgICAgICAg
ICAgIGIxID0gYWdncmVnYXRlX3RlbnNvcnMoYzQsIF9NKCdLNCcsIGF4aXNfYz1heGlzLCBjbWFy
Zz1jbSwgdDQ9MC4yNSksIHJlZnMpCiAgICAgICAgICAgIGZvciBzIGluICgnVicsICdSJywgJ0hT
Jyk6IHdvcnN0ID0gbWF4KHdvcnN0LCBmbG9hdChucC5hYnMoYjFbc10gLSBiMFtzXSkubWF4KCkp
IC8gc2NhbGUpCiAgICBDWydGLUNUUkwtTDJOVUxMJ10gPSB7J3dvcnN0X2Ficyc6IGZsb2F0KHdv
cnN0KSwgJ3Bhc3NlZCc6IGJvb2wod29yc3QgPD0gMWUtMTIpfQogICAgIyBGLUNUUkwtTDRFWEhB
VVNUOiBhbiBsID0gNiB0ZXJtIGNoYW5nZXMgbm90aGluZyAodGVuc29ycywgd2VpZ2h0cywgcl9h
Z2cpIOKAlCBoZXggUDYgYXQgdDYgPSAwLjMgb24gdG9wIG9mIHQ0ID0gMC4zOyBjdWJpYyBLNnQg
bGlrZXdpc2UKICAgIHd0ID0gd3IgPSAwLjAKICAgIGZvciBjZmcsIChzeW0sIHZrKSBpbiBDT05G
SUdTLml0ZW1zKCk6CiAgICAgICAgcmVmcyA9IGhzX3JlZnNbY2ZnXQogICAgICAgIGZvciBrZXks
IHN5bW0sIGF4aXMsIGNtIGluIGNvbmZpZ19rZXlzKGNmZyk6CiAgICAgICAgICAgIGM0ID0gYzRf
ZnJvbV9jb25zdGFudHMoc3ltLCB2cmhbdmtdWydDX292ZXJfcmhvJ10sIHN5bW0pOyBzY2FsZSA9
IG5wLmFicyhjNCkubWF4KCkKICAgICAgICAgICAgbzAgPSBmYW1pbHkoc3ltLCBheGlzLCBjbSwg
dDQ9MC4zKTsgbzYgPSBmYW1pbHkoc3ltLCBheGlzLCBjbSwgdDQ9MC4zLCB0Nj0wLjMpCiAgICAg
ICAgICAgIGEwID0gYWdncmVnYXRlX3RlbnNvcnMoYzQsIG8wLCByZWZzKTsgYTYgPSBhZ2dyZWdh
dGVfdGVuc29ycyhjNCwgbzYsIHJlZnMpCiAgICAgICAgICAgIGZvciBzIGluICgnVicsICdSJywg
J0hTJyk6IHd0ID0gbWF4KHd0LCBmbG9hdChucC5hYnMoYTZbc10gLSBhMFtzXSkubWF4KCkpIC8g
c2NhbGUpCiAgICAgICAgICAgIHIwID0gc3BlY2llc19zdGF0cyhzeW0sIGEwWydIJ10sIEssIFcs
IG8wLCB3YW50X2xhYmVscz1GYWxzZSlbJ3JfeHRhbF9FMiddOyByNiA9IHNwZWNpZXNfc3RhdHMo
c3ltLCBhNlsnSCddLCBLLCBXLCBvNiwgd2FudF9sYWJlbHM9RmFsc2UpWydyX3h0YWxfRTInXTsg
d3IgPSBtYXgod3IsIGFicyhyNiAtIHIwKSkKICAgIENbJ0YtQ1RSTC1MNEVYSEFVU1QnXSA9IHsn
d29yc3RfcmVsX3RlbnNvcic6IGZsb2F0KHd0KSwgJ3dvcnN0X2Fic19yX2FnZyc6IGZsb2F0KHdy
KSwgJ3Bhc3NlZCc6IGJvb2wod3QgPD0gMWUtMTIgYW5kIHdyIDw9IDFlLTEyKX0KICAgICMgRi1D
VFJMLUM0OiB0aGUgZXhhY3QgY2xvc2VkIGZvcm0gKFZvaWd0IGFuZCBSZXVzcyksIGFmZmluaXR5
LCBhbmQgdGhlIEggPSAwIHRlbnNvcgogICAgVDRWID0gbnAuemVyb3MoKDYsIDYpKTsgVDRWWzAs
IDBdID0gVDRWWzEsIDFdID0gMzsgVDRWWzIsIDJdID0gODsgVDRWWzAsIDFdID0gVDRWWzEsIDBd
ID0gMTsgVDRWWzAsIDJdID0gVDRWWzIsIDBdID0gVDRWWzEsIDJdID0gVDRWWzIsIDFdID0gLTQ7
IFQ0VlszLCAzXSA9IFQ0Vls0LCA0XSA9IC00OyBUNFZbNSwgNV0gPSAxCiAgICBUNFYgPSBUNFYg
LyAxMDUuMAogICAgd2NmID0gd2FmID0gMC4wCiAgICBmb3IgY2ZnIGluICgnY3ViaWNfc3RlcCcs
ICdjdWJpY19nZW04Jyk6CiAgICAgICAgc3ltLCB2ayA9IENPTkZJR1NbY2ZnXTsgYyA9IHZyaFt2
a11bJ0Nfb3Zlcl9yaG8nXTsgYzQgPSBjNF9mcm9tX2NvbnN0YW50cyhzeW0sIGMpOyBIID0gemVu
ZXJfSChjKTsgc2NhbGUgPSBucC5hYnMoYzQpLm1heCgpCiAgICAgICAgVjAgPSBjNF90b192b2ln
dDY2KG9kZl9hdmdfYzQoYzQsIE9ERignaXNvJykpKTsgVjMgPSBjNF90b192b2lndDY2KG9kZl9h
dmdfYzQoYzQsIE9ERignSzQnLCB0ND0wLjMpKSk7IFY2ID0gYzRfdG9fdm9pZ3Q2NihvZGZfYXZn
X2M0KGM0LCBPREYoJ0s0JywgdDQ9MC42KSkpCiAgICAgICAgd2NmID0gbWF4KHdjZiwgZmxvYXQo
bnAuYWJzKChWMyAtIFYwKSAtIDAuMyAqIEggKiBUNFYpLm1heCgpKSAvIHNjYWxlKTsgd2FmID0g
bWF4KHdhZiwgZmxvYXQobnAuYWJzKChWNiAtIFYwKSAtIDIgKiAoVjMgLSBWMCkpLm1heCgpKSAv
IHNjYWxlKQogICAgICAgIFM0ID0gbWFuZGVsX3RvX2M0KG5wLmxpbmFsZy5pbnYoYzRfdG9fbWFu
ZGVsKGM0KSkpOyBTdiA9IGM0X3RvX3ZvaWd0NjYoUzQpOyBIU18gPSBTdlswLCAwXSAtIFN2WzAs
IDFdIC0gMC41ICogKDQgKiBTdlszLCAzXSkgICAjIFZvaWd0LW5vdGF0aW9uIFM0NCA9IDQgU18y
MzIzIC0+IHRlbnNvciBIX1MgPSBTMTEgLSBTMTIgLSAyIFNfMjMyMwogICAgICAgIFIwID0gYzRf
dG9fdm9pZ3Q2NihvZGZfYXZnX2M0KFM0LCBPREYoJ2lzbycpKSk7IFIzID0gYzRfdG9fdm9pZ3Q2
NihvZGZfYXZnX2M0KFM0LCBPREYoJ0s0JywgdDQ9MC4zKSkpCiAgICAgICAgIyBWb2lndC1ub3Rh
dGlvbiBjb21wbGlhbmNlIGVudHJpZXM6IHRoZSB0ZW5zb3IgbGF3IGhvbGRzIG9uIHRoZSB0ZW5z
b3I7IGluIFZvaWd0IG5vdGF0aW9uIHRoZSBzaGVhciByb3dzIGNhcnJ5IGZhY3RvcnMgNCAoNDQp
IGFuZCB0aGUgbWl4ZWQgcm93cyAyIOKAlCBjb21wYXJlIG9uIHRlbnNvcnMgaW5zdGVhZAogICAg
ICAgIFMzdCA9IG9kZl9hdmdfYzQoUzQsIE9ERignSzQnLCB0ND0wLjMpKTsgUzB0ID0gb2RmX2F2
Z19jNChTNCwgT0RGKCdpc28nKSk7IEh0ID0gSFNfIC8gMS4wCiAgICAgICAgVHQgPSB2b2lndDY2
X3RvX2M0KFQ0Vik7IFR0X2Z1bGwgPSBUdC5jb3B5KCkgICAjIFQ0ViBpbiBWb2lndCBub3RhdGlv
biBlbmNvZGVzIHRoZSB0ZW5zb3Ig8J2Sr+KBtC8xMDUgZW50cmllcyBkaXJlY3RseSAoYWxsIGVu
dHJpZXMgc3ltbWV0cmljKQogICAgICAgIHdjZiA9IG1heCh3Y2YsIGZsb2F0KG5wLmFicygoUzN0
IC0gUzB0KSAtIDAuMyAqIEh0ICogVHRfZnVsbCkubWF4KCkpIC8gbnAuYWJzKFM0KS5tYXgoKSkK
ICAgIGNfaDAgPSBjNF9mcm9tX2NvbnN0YW50cygnY3ViaWMnLCB7J0MxMSc6IDIwMC4wLCAnQzEy
JzogMTAwLjAsICdDNDQnOiA1MC4wfSk7IFYwID0gb2RmX2F2Z19jNChjX2gwLCBPREYoJ2lzbycp
KTsgVjMgPSBvZGZfYXZnX2M0KGNfaDAsIE9ERignSzQnLCB0ND0wLjMpKQogICAgaDAgPSBmbG9h
dChucC5hYnMoVjMgLSBWMCkubWF4KCkpIC8gbnAuYWJzKGNfaDApLm1heCgpCiAgICBDWydGLUNU
UkwtQzQnXSA9IHsnd29yc3RfcmVsX2Nsb3NlZF9mb3JtJzogZmxvYXQod2NmKSwgJ3dvcnN0X3Jl
bF9hZmZpbmUnOiBmbG9hdCh3YWYpLCAnaDBfZWZmZWN0X3JlbCc6IGgwLCAncGFzc2VkJzogYm9v
bCh3Y2YgPD0gMWUtMTIgYW5kIHdhZiA8PSAxZS0xMiBhbmQgaDAgPD0gMWUtMTIpfQogICAgIyBG
LUNUUkwtTUFSRyAoY3ViaWMga2V5cyk6IFNPKDMpLWRpcmVjdCB3ZWlnaHQgYXZlcmFnZSA9PSBt
YXJnaW5hbCBmb3JtIGF0IHQ0ID0gMC4zCiAgICB3b3JzdCA9IDAuMAogICAgZm9yIGNmZyBpbiAo
J2N1YmljX3N0ZXAnLCAnY3ViaWNfZ2VtOCcpOgogICAgICAgIHN5bSwgdmsgPSBDT05GSUdTW2Nm
Z107IGM0ID0gYzRfZnJvbV9jb25zdGFudHMoc3ltLCB2cmhbdmtdWydDX292ZXJfcmhvJ10pCiAg
ICAgICAgZm9yIGtleSwgc3ltbSwgYXhpcywgY20gaW4gY29uZmlnX2tleXMoY2ZnKToKICAgICAg
ICAgICAgb2RmID0gT0RGKCdLNCcsIGF4aXNfYz1heGlzLCBjbWFyZz1jbSwgdDQ9MC4zKTsgYWcg
PSBhZ2dyZWdhdGVfdGVuc29ycyhjNCwgb2RmLCBOb25lKTsgdiwgZSA9IG1vZGVzKGFnWydIJ10s
IEspOyBsYW0sIHdfZW0sIFNwLCBfID0gZGVzY3JpcHRvcnMoSywgZSkKICAgICAgICAgICAgZm0g
PSBvZGZfYXZnX2ZyYWNFMihTcCwgb2RmKTsgZmQgPSBzbzNfZGlyZWN0X2ZyYWNFMihTcCwgb2Rm
LCBheGlzKTsgd29yc3QgPSBtYXgod29yc3QsIGZsb2F0KG5wLm1heChucC5hYnMoZm0gLSBmZClb
d19lbSA+IDFlLTZdKSkpCiAgICBDWydGLUNUUkwtTUFSRyddID0geyd3b3JzdF9hYnMnOiBmbG9h
dCh3b3JzdCksICdwYXNzZWQnOiBib29sKHdvcnN0IDw9IDFlLTEyKX0KICAgICMgRi1DVFJMLVRF
WDQKICAgIGNfdGV4ID0gYzRfZnJvbV9jb25zdGFudHMoJ2N1YmljJywgeydDMTEnOiAzMDAuMCwg
J0MxMic6IDEwMC4wLCAnQzQ0JzogNDAuMH0pOyBycywgXyA9IHJfYWdnX29mKCdjdWJpYycsIGNf
dGV4LCBPREYoJ0s0JywgdDQ9MS4wKSwgSywgVywgTm9uZSkKICAgIENbJ0YtQ1RSTC1URVg0J10g
PSB7J3JfYWdnX3QxX2Ficyc6IGFicyhyc1snSCddWydyX3h0YWxfRTInXSksICdwYXNzZWQnOiBi
b29sKGFicyhyc1snSCddWydyX3h0YWxfRTInXSkgPiBUQVUpfQogICAgIyBGLUNUUkwtUVVBRDog
ay1zcGhlcmUgZG91Ymxpbmcgb24gcl9hZ2cgYXQgdDQgPSAwLjI1IHBlciBrZXk7IFNPKDMpIGRv
dWJsaW5nIG9uIHRoZSBWb2lndCB0ZW5zb3IgYXQgdDQgPSAwLjMKICAgIGdsb2JhbCBTTzNfRE9V
QkxFCiAgICBLMiwgVzIgPSBzcGhlcmVfZ3JpZCgyICogTl9USEVUQSwgMiAqIE5fUEhJKTsgd2Qg
PSAwLjA7IHdzbzMgPSAwLjAKICAgIGlmIFNPM19ET1VCTEUgaXMgTm9uZTogU08zX0RPVUJMRSA9
IHNvM19ncmlkKDMyLCAyMCwgMzIpCiAgICBmb3IgY2ZnLCAoc3ltLCB2aykgaW4gQ09ORklHUy5p
dGVtcygpOgogICAgICAgIGZvciBrZXksIHN5bW0sIGF4aXMsIGNtIGluIGNvbmZpZ19rZXlzKGNm
Zyk6CiAgICAgICAgICAgIGM0ID0gYzRfZnJvbV9jb25zdGFudHMoc3ltLCB2cmhbdmtdWydDX292
ZXJfcmhvJ10sIHN5bW0pOyBvZGYgPSBmYW1pbHkoc3ltLCBheGlzLCBjbSwgdDQ9MC4yNSk7IGFn
ID0gYWdncmVnYXRlX3RlbnNvcnMoYzQsIG9kZiwgTm9uZSkKICAgICAgICAgICAgcjEgPSBzcGVj
aWVzX3N0YXRzKHN5bSwgYWdbJ0gnXSwgSywgVywgb2RmLCB3YW50X2xhYmVscz1GYWxzZSlbJ3Jf
eHRhbF9FMiddOyByMiA9IHNwZWNpZXNfc3RhdHMoc3ltLCBhZ1snSCddLCBLMiwgVzIsIG9kZiwg
d2FudF9sYWJlbHM9RmFsc2UpWydyX3h0YWxfRTInXTsgd2QgPSBtYXgod2QsIGFicyhyMSAtIHIy
KSkKICAgICAgICAgICAgVjEgPSBvZGZfYXZnX2M0KGM0LCBmYW1pbHkoc3ltLCBheGlzLCBjbSwg
dDQ9MC4zKSk7IFYyID0gb2RmX2F2Z19jNChjNCwgZmFtaWx5KHN5bSwgYXhpcywgY20sIHQ0PTAu
MyksIFNPM19ET1VCTEUpOyB3c28zID0gbWF4KHdzbzMsIGZsb2F0KG5wLmFicyhWMSAtIFYyKS5t
YXgoKSkgLyBucC5hYnMoYzQpLm1heCgpKQogICAgQ1snRi1DVFJMLVFVQUQnXSA9IHsnZG91Ymxp
bmdfcmVzaWR1YWwnOiBmbG9hdChtYXgod2QsIHdzbzMpKSwgJ2tfc3BoZXJlX2RvdWJsaW5nJzog
ZmxvYXQod2QpLCAnc28zX2RvdWJsaW5nJzogZmxvYXQod3NvMyksICdwYXNzZWQnOiBib29sKG1h
eCh3ZCwgd3NvMykgPD0gMWUtMTApfQogICAgcmV0dXJuIEMsIGhzX3JlZnMsIHh0YWwsIHZ0MAoK
IyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBQaGFzZSAyIC8gMwpkZWYgcGhhc2UyKHZyaCwgSywgVywg
aHNfcmVmcyk6CiAgICBvdXQgPSB7fQogICAgZm9yIGNmZywgKHN5bSwgdmspIGluIENPTkZJR1Mu
aXRlbXMoKToKICAgICAgICByZWZzID0gaHNfcmVmc1tjZmddCiAgICAgICAgZm9yIGtleSwgc3lt
bSwgYXhpcywgY20gaW4gY29uZmlnX2tleXMoY2ZnKToKICAgICAgICAgICAgYzQgPSBjNF9mcm9t
X2NvbnN0YW50cyhzeW0sIHZyaFt2a11bJ0Nfb3Zlcl9yaG8nXSwgc3ltbSk7IHJFMiwgcmgsIHJI
UywgclYsIHJSLCBsYW10ID0gW10sIFtdLCBbXSwgW10sIFtdLCBbXQogICAgICAgICAgICBmb3Ig
dDQgaW4gVDRfR1JJRDoKICAgICAgICAgICAgICAgIG9kZiA9IGZhbWlseShzeW0sIGF4aXMsIGNt
LCB0ND10NCk7IGFnID0gYWdncmVnYXRlX3RlbnNvcnMoYzQsIG9kZiwgcmVmcykKICAgICAgICAg
ICAgICAgIHNIID0gc3BlY2llc19zdGF0cyhzeW0sIGFnWydIJ10sIEssIFcsIG9kZik7IHJFMi5h
cHBlbmQoc0hbJ3JfeHRhbF9FMiddKTsgcmguYXBwZW5kKHNIWydyX3h0YWxfaCddKTsgbGFtdC5h
cHBlbmQoc0hbJ2xhbWJkYV9tZWFuJ10pCiAgICAgICAgICAgICAgICBmb3IgdGFnLCBsc3QgaW4g
KCgnSFMnLCBySFMpLCAoJ1YnLCByViksICgnUicsIHJSKSk6IGxzdC5hcHBlbmQoc3BlY2llc19z
dGF0cyhzeW0sIGFnW3RhZ10sIEssIFcsIG9kZiwgd2FudF9sYWJlbHM9RmFsc2UpWydyX3h0YWxf
RTInXSkKICAgICAgICAgICAgaWR4ID0gW2kgZm9yIGksIHQgaW4gZW51bWVyYXRlKFQ0X0dSSUQp
IGlmIGFicyh0KSA8PSAwLjI1ICsgMWUtMTJdOyBpZHgyID0gW2kgZm9yIGksIHQgaW4gZW51bWVy
YXRlKFQ0X0dSSUQpIGlmIGFicyh0KSA8PSAwLjEgKyAxZS0xMl0KICAgICAgICAgICAgdHQgPSBb
VDRfR1JJRFtpXSBmb3IgaSBpbiBpZHhdOyB0dDIgPSBbVDRfR1JJRFtpXSBmb3IgaSBpbiBpZHgy
XQogICAgICAgICAgICBjRSwgcmVzRSA9IGZpdF9yKHR0LCBbckUyW2ldIGZvciBpIGluIGlkeF0p
OyBjRTIsIF8gPSBmaXRfcih0dDIsIFtyRTJbaV0gZm9yIGkgaW4gaWR4Ml0pOyBjaCwgXyA9IGZp
dF9yKHR0LCBbcmhbaV0gZm9yIGkgaW4gaWR4XSk7IGNIUywgXyA9IGZpdF9yKHR0LCBbckhTW2ld
IGZvciBpIGluIGlkeF0pCiAgICAgICAgICAgICMgYmlyZWZyaW5nZW5jZSBiMSBvbiBIaWxsOiBw
cm9wYWdhdGlvbiBhbG9uZyB4IChwZXJwZW5kaWN1bGFyIHRvIHRoZSBmaWJlciksIHBvbGFyaXph
dGlvbnMgeSAocVNIKSBhbmQgeiAocVNWKQogICAgICAgICAgICBkZWYgYmlyZWYodDQpOgogICAg
ICAgICAgICAgICAgYWcgPSBhZ2dyZWdhdGVfdGVuc29ycyhjNCwgZmFtaWx5KHN5bSwgYXhpcywg
Y20sIHQ0PXQ0KSwgTm9uZSk7IE0gPSBjNF90b192b2lndDY2KGFnWydIJ10pCiAgICAgICAgICAg
ICAgICByZXR1cm4gKG1hdGguc3FydChNWzUsIDVdKSAtIG1hdGguc3FydChNWzMsIDNdKSkgICAj
IHZfU0heMiA9IEM2Niwgdl9TVl4yID0gQzQ0IGZvciBrIGFsb25nIHggaW4gYSBUSSBtZWRpdW0g
YWJvdXQgegogICAgICAgICAgICB2VDAgPSBtYXRoLnNxcnQoaXNvX0tHX29mX2M0KGFnZ3JlZ2F0
ZV90ZW5zb3JzKGM0LCBPREYoJ2lzbycpLCBOb25lKVsnSCddKVsxXSk7IGIxID0gKGJpcmVmKDAu
MDUpIC0gYmlyZWYoLTAuMDUpKSAvIDAuMSAvIHZUMAogICAgICAgICAgICAjIHF1YWRyYXRpYyBm
b3JtIG9uIHRoZSA1eDUgZ3JpZCAoaGV4OiBQMitQNDsgY3ViaWM6IFAyIG9uIHRoZSBkZXNjcmlw
dG9yIGF4aXMgKyBLNCAtPiBtdXN0IHJlZHVjZSB0byBrYXBwYTQ0IGFsb25lKQogICAgICAgICAg
ICB0MnMsIHQ0cywgcnEgPSBbXSwgW10sIFtdCiAgICAgICAgICAgIGZvciBhIGluIFQyVDQ6CiAg
ICAgICAgICAgICAgICBmb3IgYiBpbiBUMlQ0OgogICAgICAgICAgICAgICAgICAgIGlmIHN5bSA9
PSAnaGV4Jzogb2RmID0gT0RGKCdQNCcsIHQyPWEsIHQ0PWIpCiAgICAgICAgICAgICAgICAgICAg
ZWxzZToKICAgICAgICAgICAgICAgICAgICAgICAgYmFzZSA9IE9ERignSzQnLCBheGlzX2M9YXhp
cywgY21hcmc9Y20sIHQ0PWIpCiAgICAgICAgICAgICAgICAgICAgICAgIGNsYXNzIF9NKE9ERik6
CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBkZWYgd19zbzMoc2VsZiwgUnMpOiByZXR1cm4g
YmFzZS53X3NvMyhScykgKyBhICogUDIoKFJzIEAgYXhpcylbOiwgMl0pCiAgICAgICAgICAgICAg
ICAgICAgICAgICAgICBkZWYgd19tYXJnKHNlbGYsIG4pOiByZXR1cm4gYmFzZS53X21hcmcobikg
KyBhICogUDIobls6LCAyXSkKICAgICAgICAgICAgICAgICAgICAgICAgb2RmID0gX00oJ0s0Jywg
YXhpc19jPWF4aXMsIGNtYXJnPWNtLCB0ND1iKQogICAgICAgICAgICAgICAgICAgIGFnID0gYWdn
cmVnYXRlX3RlbnNvcnMoYzQsIG9kZiwgTm9uZSk7IHJxLmFwcGVuZChzcGVjaWVzX3N0YXRzKHN5
bSwgYWdbJ0gnXSwgSywgVywgb2RmLCB3YW50X2xhYmVscz1GYWxzZSlbJ3JfeHRhbF9FMiddKTsg
dDJzLmFwcGVuZChhKTsgdDRzLmFwcGVuZChiKQogICAgICAgICAgICBxZiA9IGZpdF9xdWFkZm9y
bShucC5hcnJheSh0MnMpLCBucC5hcnJheSh0NHMpLCBucC5hcnJheShycSkpCiAgICAgICAgICAg
IGFnMCA9IGFnZ3JlZ2F0ZV90ZW5zb3JzKGM0LCBPREYoJ2lzbycpLCByZWZzKTsgdlQgPSB7azog
bWF0aC5zcXJ0KGlzb19LR19vZl9jNChhZzBba10pWzFdKSBmb3IgayBpbiAoJ0gnLCAnSFNsbycs
ICdIU2hpJyl9CiAgICAgICAgICAgIG91dFtrZXldID0geydyX2FnZ19FMl9WUkgnOiByRTIsICdy
X2FnZ19oX1ZSSCc6IHJoLCAncl9hZ2dfRTJfSFMnOiBySFMsICdyX2FnZ19FMl9WJzogclYsICdy
X2FnZ19FMl9SJzogclIsICdsYW1iZGFfbWVhbl90NCc6IGxhbXQsCiAgICAgICAgICAgICAgICAg
ICAgICAgICdTNF9FMic6IGZsb2F0KGNFWzBdKSwgJ1M0X2gnOiBmbG9hdChjaFswXSksICdrYXBw
YTQ0X0UyJzogZmxvYXQoY0VbMV0pLCAna2FwcGE0NF9oJzogZmxvYXQoY2hbMV0pLCAna2FwcGE0
NDRfRTInOiBmbG9hdChjRVsyXSksICdrYXBwYTQ0X0UyX0hTJzogZmxvYXQoY0hTWzFdKSwKICAg
ICAgICAgICAgICAgICAgICAgICAgJ2hhbHZpbmdfZGV2X2thcHBhNDQnOiBmbG9hdChhYnMoY0Vb
MV0gLSBjRTJbMV0pKSwgJ2thcHBhNDRfRTJfd2luZG93MHAxJzogZmxvYXQoY0UyWzFdKSwgJ2Zp
dF9yZXNpZHVhbCc6IHJlc0UsICdiaXJlZl9iMV9WUkgnOiBmbG9hdChiMSksCiAgICAgICAgICAg
ICAgICAgICAgICAgICd2VF9WUkgnOiB2VFsnSCddLCAndlRfSFNfbG8nOiB2VFsnSFNsbyddLCAn
dlRfSFNfaGknOiB2VFsnSFNoaSddLCAncXVhZGZvcm0nOiBxZiwgJ2hzX3JlZic6IHJlZnN9CiAg
ICAgICAgICAgIHByaW50KGYnICBwaGFzZTIge2tleToxNn0gUzQ9e2NFWzBdOisuM2V9IGs0ND17
Y0VbMV06Ky42ZX0gKHdpbjAuMSB7Y0UyWzFdOisuNmV9KSBrNDRfSFM9e2NIU1sxXTorLjZlfSBr
NDRfaD17Y2hbMV06Ky4zZX0gYjE9e2IxOisuNGV9IHFmIGsyMj17cWZbImthcHBhMjIiXTorLjNl
fSBrMjQ9e3FmWyJrYXBwYTI0Il06Ky4zZX0gazQ0PXtxZlsia2FwcGE0NCJdOisuNmV9JywgZmx1
c2g9VHJ1ZSkKICAgIHJldHVybiBvdXQKZGVmIHBoYXNlMyhDLCBQMik6CiAgICBpZiBub3QgYWxs
KHZbJ3Bhc3NlZCddIGZvciB2IGluIEMudmFsdWVzKCkpOiByZXR1cm4geyd2ZXJkaWN0X2NsYXNz
JzogJ0lOREVURVJNSU5BVEUnLCAnRi1NUzItMyc6ICdOT1QtRVZBTFVBVEVEJywgJ0YtTVMyLTQn
OiAnTk9ULUVWQUxVQVRFRCcsICdGLU1TMi0yJzogJ1JFR0lTVEVSRURfTk9UX0VYRUNVVEVEJywg
J3dvcnN0X1M0JzogTm9uZX0KICAgIHdvcnN0ID0gbWF4KG1heChhYnMocFsnUzRfRTInXSksIGFi
cyhwWydTNF9oJ10pKSBmb3IgcCBpbiBQMi52YWx1ZXMoKSkKICAgIGZtMyA9ICdGSVJFUycgaWYg
d29yc3QgPiBUQVUgZWxzZSAnU0lMRU5UJwogICAgbnVsbCA9IGFsbChhYnMoUDJba11bJ2thcHBh
NDRfRTInXSkgPD0gS0ZMT09SIGZvciBrIGluICgnY3ViaWNfc3RlcHwwMDEnLCAnY3ViaWNfZ2Vt
OHwwMDEnKSk7IGZtNCA9ICdGSVJFUycgaWYgbnVsbCBlbHNlICdTSUxFTlQnCiAgICB2ZXJkaWN0
ID0gJ1BST1RFQ1RJT04tQlJFQUNIJyBpZiBmbTMgPT0gJ0ZJUkVTJyBlbHNlICgnTDQtTlVMTCcg
aWYgbnVsbCBlbHNlICdJREVOVElUWS1ERUxJVkVSRUQtTDQnKQogICAgcmV0dXJuIHsndmVyZGlj
dF9jbGFzcyc6IHZlcmRpY3QsICdGLU1TMi0zJzogZm0zLCAnRi1NUzItNCc6IGZtNCwgJ0YtTVMy
LTInOiAnUkVHSVNURVJFRF9OT1RfRVhFQ1VURUQnLCAnd29yc3RfUzQnOiBmbG9hdCh3b3JzdCl9
CgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIGNvbW1hbmRzCmRlZiBiYXNlX2NoZWNrcG9pbnQoVDEp
OgogICAgcmV0dXJuIHsnZ2F0ZSc6ICdHLU1TQ1MyJywgJ2xlZyc6ICdjaGF0JywgJ2luc3RydW1l
bnQnOiBvcy5wYXRoLmJhc2VuYW1lKF9fZmlsZV9fKSwgJ2luc3RydW1lbnRfbWQ1JzogbWQ1ZihN
RSksICdtZW1vX2xvY2tfbWQ1JzogTUVNT19NRDUsICdtZW1vX2xvY2tfYnl0ZXMnOiBNRU1PX0JZ
VEVTLAogICAgICAgICAgICAnbGVkZ2VyX2Jhc2VfbWQ1JzogTEVER0VSX0JBU0VfTUQ1LCAndDFf
bGlzdF9tZDUnOiBUMV9NRDUsICd4MV9tZDUnOiBYMV9NRDUsICd4Nl9jaGF0X21kNSc6IFg2Q19N
RDUsICd4Nl9jY19tZDUnOiBYNkNDX01ENSwKICAgICAgICAgICAgJ3V0Yyc6IGRhdGV0aW1lLmRh
dGV0aW1lLm5vdyhkYXRldGltZS50aW1lem9uZS51dGMpLmlzb2Zvcm1hdCgpLCAnZWxlY3Rpb25z
JzogRUxFQ1RJT05TLCAndDFfc2Nhbic6IHsnaW5zdHJ1bWVudCc6IFQxWydpbnN0cnVtZW50J10s
ICdtZW1vJzogVDFbJ21lbW8nXX0sCiAgICAgICAgICAgICdxdWFkcmF0dXJlJzogeyduX3RoZXRh
JzogTl9USEVUQSwgJ25fcGhpJzogTl9QSEksICdzbzNfZ3JpZCc6IFsxNiwgMTAsIDE2XSwgJ25f
Z3JpZCc6IFsxMiwgMjRdfSwgJ3Q0X2dyaWQnOiBUNF9HUklELCAndDJ0NF9ncmlkJzogVDJUNH0K
ZGVmIGNtZF9ydW4oYSk6CiAgICBUMSA9IGd1YXJkcygpOyB2cmggPSBqc29uLmxvYWQob3BlbihY
MSkpWyd2cmgnXTsgeDYgPSBqc29uLmxvYWQob3BlbihYNkMpKTsgSywgVyA9IHNwaGVyZV9ncmlk
KE5fVEhFVEEsIE5fUEhJKQogICAgcHJpbnQoJ3BoYXNlMCAuLi4nLCBmbHVzaD1UcnVlKTsgQywg
aHNfcmVmcywgeHRhbCwgdnQwID0gcGhhc2UwKHZyaCwgeDYsIEssIFcpCiAgICBmb3IgaywgdiBp
biBDLml0ZW1zKCk6IHByaW50KGYnICB7azoxNn0gcGFzc2VkPXt2WyJwYXNzZWQiXX0gICcgKyAn
ICcuam9pbihmJ3tra309e3Z2Oi4zZX0nIGZvciBraywgdnYgaW4gdi5pdGVtcygpIGlmIGlzaW5z
dGFuY2UodnYsIGZsb2F0KSksIGZsdXNoPVRydWUpCiAgICBjayA9IGJhc2VfY2hlY2twb2ludChU
MSk7IGNrWydwaGFzZTAnXSA9IEM7IGNrWydwaGFzZTBfd2l0bmVzcyddID0geydzaW5nbGVfY3J5
c3RhbCc6IHh0YWwsICd2VF90MCc6IHZ0MCwgJ2hzX3JlZic6IGhzX3JlZnN9CiAgICBvayA9IGFs
bCh2WydwYXNzZWQnXSBmb3IgdiBpbiBDLnZhbHVlcygpKQogICAgaWYgYS5waGFzZTBfb25seSBv
ciBub3Qgb2s6CiAgICAgICAgY2tbJ3BoYXNlMiddID0ge307IGNrWydwaGFzZTMnXSA9IHBoYXNl
MyhDLCB7fSkgaWYgbm90IG9rIGVsc2Ugeyd2ZXJkaWN0X2NsYXNzJzogJ05PVC1BU1NFTUJMRUQg
KHBoYXNlMC1vbmx5IHJ1biknLCAnbm90ZSc6ICdQaGFzZXMgMi0zIG5vdCBleGVjdXRlZCBvbiB0
aGlzIHJ1biBieSB0aGUgYXV0aG9yXCdzIGRpcmVjdGl2ZSd9CiAgICAgICAganNvbi5kdW1wKGNr
LCBvcGVuKENIRUNLUE9JTlRfUDAsICd3JyksIGluZGVudD0xKTsgcG9zdCA9IHQxX2dhdGUoeydj
aGVja3BvaW50JzogQ0hFQ0tQT0lOVF9QMH0pOyBja1snVDFfcG9zdF93cml0ZSddID0gcG9zdDsg
anNvbi5kdW1wKGNrLCBvcGVuKENIRUNLUE9JTlRfUDAsICd3JyksIGluZGVudD0xKQogICAgICAg
IHByaW50KGYneyJIQUxUOiBhIFBoYXNlLTAgcGluL2NvbnRyb2wgZmFpbGVkIC0+IElOREVURVJN
SU5BVEUiIGlmIG5vdCBvayBlbHNlICJwaGFzZTAgY29tcGxldGUgKHBoYXNlMC1vbmx5IHJ1biki
fTsgY2hlY2twb2ludCB7b3MucGF0aC5iYXNlbmFtZShDSEVDS1BPSU5UX1AwKX0ge21kNWYoQ0hF
Q0tQT0lOVF9QMCl9ICh7b3MucGF0aC5nZXRzaXplKENIRUNLUE9JTlRfUDApOix9IEIpICBUMSBw
b3N0IHtwb3N0WyJjaGVja3BvaW50Il19JykKICAgICAgICByZXR1cm4KICAgIHByaW50KCdwaGFz
ZTIgLi4uJywgZmx1c2g9VHJ1ZSk7IGNrWydwaGFzZTInXSA9IHBoYXNlMih2cmgsIEssIFcsIGhz
X3JlZnMpOyBja1sncGhhc2UzJ10gPSBwaGFzZTMoQywgY2tbJ3BoYXNlMiddKQogICAganNvbi5k
dW1wKGNrLCBvcGVuKENIRUNLUE9JTlQsICd3JyksIGluZGVudD0xKTsgcG9zdCA9IHQxX2dhdGUo
eydjaGVja3BvaW50JzogQ0hFQ0tQT0lOVH0pOyBja1snVDFfcG9zdF93cml0ZSddID0gcG9zdDsg
anNvbi5kdW1wKGNrLCBvcGVuKENIRUNLUE9JTlQsICd3JyksIGluZGVudD0xKQogICAgcHJpbnQo
Zid2ZXJkaWN0X2NsYXNzIHtja1sicGhhc2UzIl1bInZlcmRpY3RfY2xhc3MiXX0gIEYtTVMyLTMg
e2NrWyJwaGFzZTMiXVsiRi1NUzItMyJdfSAgRi1NUzItNCB7Y2tbInBoYXNlMyJdWyJGLU1TMi00
Il19ICBUMSBwb3N0IHtwb3N0WyJjaGVja3BvaW50Il19JykKICAgIHByaW50KGYnY2hlY2twb2lu
dCB7b3MucGF0aC5iYXNlbmFtZShDSEVDS1BPSU5UKX0ge21kNWYoQ0hFQ0tQT0lOVCl9ICh7b3Mu
cGF0aC5nZXRzaXplKENIRUNLUE9JTlQpOix9IEIpJykKZGVmIGNtZF9jb21wYXJlKGEpOgogICAg
Y2sgPSBqc29uLmxvYWQob3BlbihDSEVDS1BPSU5UKSk7IHAyID0gY2tbJ3BoYXNlMiddOyByb3dz
ID0gW107IGN1YiA9IFtrIGZvciBrIGluIEtFWVMgaWYgay5zdGFydHN3aXRoKCdjdWJpYycpXTsg
aGV4ayA9IFtrIGZvciBrIGluIEtFWVMgaWYgay5zdGFydHN3aXRoKCdoZXgnKV0KICAgIHIxID0g
YWxsKDFlLTMgPD0gYWJzKHAyW2tdWydrYXBwYTQ0X0UyJ10pIDw9IDFlLTIgZm9yIGsgaW4gY3Vi
KSBhbmQgYWxsKGFicyhwMltrXVsna2FwcGE0NF9oJ10pIDwgYWJzKHAyW2tdWydrYXBwYTQ0X0Uy
J10pIGZvciBrIGluIGN1YikKICAgIHJvd3MuYXBwZW5kKHsnaWQnOiAnSFlQLU1TMi0xJywgJ3By
ZWRpY3RlZCc6ICdjdWJpYyBrYXBwYTQ0X0UyICE9IDAsIHwufCBpbiBbMWUtMywgMWUtMl07IGth
cHBhNDRfaCBzbWFsbGVyJywgJ21hY2hpbmUnOiB7azogW3AyW2tdWydrYXBwYTQ0X0UyJ10sIHAy
W2tdWydrYXBwYTQ0X2gnXV0gZm9yIGsgaW4gY3VifSwgJ2NvbmNvcmRhbnQnOiBib29sKHIxKX0p
CiAgICByMiA9IGFsbChwMltrXVsna2FwcGE0NF9FMiddIDwgMCBmb3IgayBpbiBjdWIgaWYgJzAw
MScgaW4gaykgYW5kIGFsbChwMltrXVsna2FwcGE0NF9FMiddID4gMCBmb3IgayBpbiBjdWIgaWYg
JzExMScgaW4gaykKICAgIHJvd3MuYXBwZW5kKHsnaWQnOiAnSFlQLU1TMi0yJywgJ3ByZWRpY3Rl
ZCc6ICdzaWduIGthcHBhNDQoMDAxKSA8IDAsIHNpZ24ga2FwcGE0NCgxMTEpID4gMCcsICdtYWNo
aW5lJzoge2s6IHAyW2tdWydrYXBwYTQ0X0UyJ10gZm9yIGsgaW4gY3VifSwgJ2NvbmNvcmRhbnQn
OiBib29sKHIyKX0pCiAgICByMyA9IGFsbChhYnMocDJba11bJ1M0X0UyJ10pIDw9IFRBVSBhbmQg
YWJzKHAyW2tdWydTNF9oJ10pIDw9IFRBVSBmb3IgayBpbiBLRVlTKQogICAgcm93cy5hcHBlbmQo
eydpZCc6ICdIWVAtTVMyLTMnLCAncHJlZGljdGVkJzogJ1M0ID0gMCB3aXRoaW4gdGF1IG9uIGFs
bCBrZXlzLCBib3RoIGFybXMnLCAnbWFjaGluZSc6IHtrOiBbcDJba11bJ1M0X0UyJ10sIHAyW2td
WydTNF9oJ11dIGZvciBrIGluIEtFWVN9LCAnY29uY29yZGFudCc6IGJvb2wocjMpfSkKICAgIHI0
ID0gYWxsKGFicyhwMltrXVsncXVhZGZvcm0nXVsna2FwcGE0NCddKSA8IGFicyhwMltrXVsncXVh
ZGZvcm0nXVsna2FwcGEyMiddKSBhbmQgYWJzKHAyW2tdWydxdWFkZm9ybSddWydrYXBwYTI0J10p
ID4gMWUtNiBhbmQgYWJzKHAyW2tdWydxdWFkZm9ybSddWydrYXBwYTI0J10pIDwgYWJzKHAyW2td
WydxdWFkZm9ybSddWydrYXBwYTIyJ10pIGFuZCBhYnMocDJba11bJ3F1YWRmb3JtJ11bJ2thcHBh
MjQnXSkgPiBhYnMocDJba11bJ3F1YWRmb3JtJ11bJ2thcHBhNDQnXSkgZm9yIGsgaW4gaGV4aykK
ICAgIHJvd3MuYXBwZW5kKHsnaWQnOiAnSFlQLU1TMi00JywgJ3ByZWRpY3RlZCc6ICdoZXggfGth
cHBhNDR8IDwgfGthcHBhMjJ8OyBrYXBwYTI0ICE9IDAgd2l0aCB8a2FwcGE0NHwgPCB8a2FwcGEy
NHwgPCB8a2FwcGEyMnwnLCAnbWFjaGluZSc6IHtrOiBwMltrXVsncXVhZGZvcm0nXSBmb3IgayBp
biBoZXhrfSwgJ2NvbmNvcmRhbnQnOiBib29sKHI0KX0pCiAgICByNSA9IGFsbChhYnMocDJba11b
J2JpcmVmX2IxX1ZSSCddKSA+PSAwLjAzIGFuZCBhYnMocDJba11bJ2JpcmVmX2IxX1ZSSCddKSAq
IDAuMjUgPiAxMDAgKiBhYnMocDJba11bJ2thcHBhNDRfRTInXSkgKiAwLjI1KioyIGZvciBrIGlu
IGN1YikKICAgIHJvd3MuYXBwZW5kKHsnaWQnOiAnSFlQLU1TMi01JywgJ3ByZWRpY3RlZCc6ICdm
Y2MgYmlyZWZyaW5nZW5jZSBjb2VmZmljaWVudCBvZiBvcmRlciAxZS0xIHBlciB1bml0IHQ0OyB0
d28gb3JkZXJzIGFib3ZlIHRoZSBkZXNjcmlwdG9yIHNwbGl0IGF0IHQ0IH4gMC4yNScsICdtYWNo
aW5lJzoge2s6IFtwMltrXVsnYmlyZWZfYjFfVlJIJ10sIHAyW2tdWydrYXBwYTQ0X0UyJ11dIGZv
ciBrIGluIGN1Yn0sICdjb25jb3JkYW50JzogYm9vbChyNSl9KQogICAgb3V0ID0geydnYXRlJzog
J0ctTVNDUzInLCAnc3RlcCc6ICdjb21wYXJlIChsYXN0KScsICdjaGVja3BvaW50X21kNSc6IG1k
NWYoQ0hFQ0tQT0lOVCksICdyb3dzJzogcm93cywgJ3ZlcmRpY3RfY2xhc3MnOiBja1sncGhhc2Uz
J11bJ3ZlcmRpY3RfY2xhc3MnXSwgJ25fY29uY29yZGFudCc6IHN1bShyWydjb25jb3JkYW50J10g
Zm9yIHIgaW4gcm93cyl9CiAgICBqc29uLmR1bXAob3V0LCBvcGVuKENPTVBBUkUsICd3JyksIGlu
ZGVudD0xLCBkZWZhdWx0PWZsb2F0KQogICAgZm9yIHIgaW4gcm93czogcHJpbnQoKCdPSyAgJyBp
ZiByWydjb25jb3JkYW50J10gZWxzZSAnTUlTUycpLCByWydpZCddLCByWydwcmVkaWN0ZWQnXSkK
ICAgIHByaW50KGYnY29tcGFyZSB7b3MucGF0aC5iYXNlbmFtZShDT01QQVJFKX0ge21kNWYoQ09N
UEFSRSl9ICB2ZXJkaWN0X2NsYXNzIHtja1sicGhhc2UzIl1bInZlcmRpY3RfY2xhc3MiXX0nKQpk
ZWYgY21kX3NlbGZ0ZXN0KGEpOgogICAgbiA9IDAKICAgIGRlZiBncmVlbihuYW1lKTogbm9ubG9j
YWwgbjsgbiArPSAxOyBwcmludChmJyAgZ3JlZW4gIHtuYW1lfScpCiAgICBScywgd3MgPSBTTzMK
ICAgICMgUzEgT0RGIG5vcm1hbGl6YXRpb24gYW5kIHNwaGVyZS1tZWFuIHplcm8gb2YgSzR0LCBL
NnQsIFA0CiAgICBhc3NlcnQgYWJzKG5wLnN1bSh3cykgLSAxKSA8IDFlLTEzIGFuZCBhYnMobnAu
c3VtKHdzICogSzR0aWxkZShScykpKSA8IDFlLTEzIGFuZCBhYnMobnAuc3VtKHdzICogSzZ0aWxk
ZShScykpKSA8IDFlLTEzIGFuZCBhYnMobnAuc3VtKHdzICogUDQoKFJzIEAgWilbOiwgMl0pKSkg
PCAxZS0xMzsgZ3JlZW4oJ1MxIFNPKDMpIHdlaWdodHMgc3VtIHRvIDE7IEs0dCwgSzZ0LCBQNCBo
YXZlIHplcm8gbWVhbicpCiAgICAjIFMyIEs0dCByYW5nZSBhbmQgbWFyZ2luYWxzOiBtYXggMSBh
dCBhIGN1YmUgYXhpcyBhbG9uZyB6LCAtMi8zIGF0IGEgYm9keSBkaWFnb25hbAogICAgYXNzZXJ0
IGFicyhLNHRpbGRlKG5wLmV5ZSgzKVtOb25lXSkgWzBdIC0gMS4wKSA8IDFlLTE0CiAgICBSMTEx
ID0gbnAuYXJyYXkoW1sxL21hdGguc3FydCgyKSwgLTEvbWF0aC5zcXJ0KDYpLCAxL21hdGguc3Fy
dCgzKV0sIFstMS9tYXRoLnNxcnQoMiksIC0xL21hdGguc3FydCg2KSwgMS9tYXRoLnNxcnQoMyld
LCBbMCwgMi9tYXRoLnNxcnQoNiksIDEvbWF0aC5zcXJ0KDMpXV0pCiAgICBSMTExID0gUjExMS5U
ICAgIyB0aGlyZCBST1cgPSAoMSwxLDEpL3NxcnQzOiB0aGUgYm9keSBkaWFnb25hbCBpcyBjYXJy
aWVkIHRvIGxhYiB6CiAgICBhc3NlcnQgYWJzKEs0dGlsZGUoUjExMVtOb25lXSlbMF0gKyAyLjAg
LyAzLjApIDwgMWUtMTM7IGdyZWVuKCdTMiBLNHQgPSAxIG9uIGEgY3ViZSBheGlzLCAtMi8zIG9u
IGEgYm9keSBkaWFnb25hbCcpCiAgICAjIFMzIGV4YWN0IGNsb3NlZCBmb3JtIG9uIGEgZ2VuZXJp
YyBjdWJpYyB0ZW5zb3IgKFZvaWd0KSBhbmQgbDYgZXhoYXVzdGlvbgogICAgYyA9IHsnQzExJzog
Mi4wLCAnQzEyJzogMC45LCAnQzQ0JzogMC43fTsgYzQgPSBjNF9mcm9tX2NvbnN0YW50cygnY3Vi
aWMnLCBjKTsgSCA9IHplbmVyX0goYykKICAgIFQ0ViA9IG5wLnplcm9zKCg2LCA2KSk7IFQ0Vlsw
LCAwXSA9IFQ0VlsxLCAxXSA9IDM7IFQ0VlsyLCAyXSA9IDg7IFQ0VlswLCAxXSA9IFQ0VlsxLCAw
XSA9IDE7IFQ0VlswLCAyXSA9IFQ0VlsyLCAwXSA9IFQ0VlsxLCAyXSA9IFQ0VlsyLCAxXSA9IC00
OyBUNFZbMywgM10gPSBUNFZbNCwgNF0gPSAtNDsgVDRWWzUsIDVdID0gMTsgVDRWIC89IDEwNS4w
CiAgICBWMCA9IGM0X3RvX3ZvaWd0NjYob2RmX2F2Z19jNChjNCwgT0RGKCdpc28nKSkpOyBWMyA9
IGM0X3RvX3ZvaWd0NjYob2RmX2F2Z19jNChjNCwgT0RGKCdLNCcsIHQ0PTAuMykpKTsgVjYgPSBj
NF90b192b2lndDY2KG9kZl9hdmdfYzQoYzQsIE9ERignSzQnLCB0ND0wLjMsIHQ2PTAuMykpKQog
ICAgYXNzZXJ0IG5wLmFicygoVjMgLSBWMCkgLSAwLjMgKiBIICogVDRWKS5tYXgoKSA8IDFlLTEz
IGFuZCBucC5hYnMoVjYgLSBWMykubWF4KCkgPCAxZS0xMzsgZ3JlZW4oJ1MzIGNsb3NlZCBmb3Jt
IChILzMpIFQ0KHopIGFuZCBsID0gNiBleGhhdXN0aW9uIG9uIGEgc3ludGhldGljIGN1YmljIHRl
bnNvcicpCiAgICAjIFM0IG1hcmdpbmFsIGlkZW50aXR5OiBTTygzKS1kaXJlY3QgdnMgbWFyZ2lu
YWwgYXZlcmFnZSBvZiBmcmFjX0UyIGZvciBhIGZpeGVkIHRyYWNlbGVzcyBTLCBib3RoIGRlc2Ny
aXB0b3IgYXhlcwogICAgUyA9IG5wLmRpYWcoWzEuMCwgLTAuNCwgLTAuNl0pOyBTID0gUyArIDAu
MyAqIChucC5vdXRlcihYLCBZKSArIG5wLm91dGVyKFksIFgpKQogICAgZm9yIGF4aXMsIGNtIGlu
ICgoWiwgMS4wKSwgKEFYMTExLCAtMi4wIC8gMy4wKSk6CiAgICAgICAgb2RmID0gT0RGKCdLNCcs
IGF4aXNfYz1heGlzLCBjbWFyZz1jbSwgdDQ9MC40KTsgZm0gPSBvZGZfYXZnX2ZyYWNFMihTW05v
bmUsIE5vbmVdLCBvZGYpWzAsIDBdOyBmZCA9IHNvM19kaXJlY3RfZnJhY0UyKFNbTm9uZSwgTm9u
ZV0sIG9kZiwgYXhpcylbMCwgMF0KICAgICAgICBhc3NlcnQgYWJzKGZtIC0gZmQpIDwgMWUtMTMs
IChmbSwgZmQpCiAgICBncmVlbignUzQgbWFyZ2luYWwgd2VpZ2h0cyBjKDAwMSkgPSAxLCBjKDEx
MSkgPSAtMi8zIHJlcHJvZHVjZSB0aGUgU08oMyktZGlyZWN0IGF2ZXJhZ2UnKQogICAgIyBTNSBm
cmFjX0UyIGlkZW50aXRpZXMgYW5kIHRoZSAyLzUgYXZlcmFnZTsgUzItaCBpc290cm9waWMgY29u
dHJvbAogICAgVCA9IG5wLmRpYWcoWzEuMCwgLTEuMCwgMC4wXSk7IGFzc2VydCBhYnMoZnJhY19F
MihULCBaW05vbmUsIDpdKVswXSAtIDEuMCkgPCAxZS0xNCBhbmQgYWJzKG9kZl9hdmdfZnJhY0Uy
KFQsIE9ERignaXNvJykpIC0gMC40KSA8IDFlLTE0OyBncmVlbignUzUgbT0rLTIgZnJhY3Rpb24g
aWRlbnRpdGllczsgMi81IFNPKDMpIGF2ZXJhZ2UnKQogICAgIyBTNiBmaXRzCiAgICB0dCA9IFt0
IGZvciB0IGluIFQ0X0dSSUQgaWYgYWJzKHQpIDw9IDAuMjVdOyBjZiwgciA9IGZpdF9yKHR0LCBb
M2UtMyAqIHQgKiB0IC0gMmUtMyAqIHQqKjMgZm9yIHQgaW4gdHRdKTsgYXNzZXJ0IGFicyhjZlsw
XSkgPCAxZS0xNSBhbmQgcmVsKGNmWzFdLCAzZS0zKSA8IDFlLTEyCiAgICB0MnMgPSBucC5hcnJh
eShbYSBmb3IgYSBpbiBUMlQ0IGZvciBiIGluIFQyVDRdKTsgdDRzID0gbnAuYXJyYXkoW2IgZm9y
IGEgaW4gVDJUNCBmb3IgYiBpbiBUMlQ0XSk7IHFmID0gZml0X3F1YWRmb3JtKHQycywgdDRzLCAx
ZS0zICogdDJzKioyIC0gNWUtNCAqIHQycyAqIHQ0cyArIDJlLTMgKiB0NHMqKjIpCiAgICBhc3Nl
cnQgcmVsKHFmWydrYXBwYTIyJ10sIDFlLTMpIDwgMWUtMTAgYW5kIHJlbChxZlsna2FwcGEyNCdd
LCAtNWUtNCkgPCAxZS0xMCBhbmQgcmVsKHFmWydrYXBwYTQ0J10sIDJlLTMpIDwgMWUtMTA7IGdy
ZWVuKCdTNiBmaXRzIHJlY292ZXIgY29lZmZpY2llbnRzICgxLXBhcmFtZXRlciBhbmQgcXVhZHJh
dGljIGZvcm0pJykKICAgICMgUzcgVm9pZ3QgYmlyZWZyaW5nZW5jZSBpZGVudGl0eTogdl9TSF4y
IC0gdl9TVl4yID0gSCB0NCAvIDIxIGZvciBrIGFsb25nIHggb24gdGhlIFZvaWd0IHRlbnNvcgog
ICAgVjN0ID0gb2RmX2F2Z19jNChjNCwgT0RGKCdLNCcsIHQ0PTAuMykpOyBNID0gYzRfdG9fdm9p
Z3Q2NihWM3QpOyBhc3NlcnQgYWJzKChNWzUsIDVdIC0gTVszLCAzXSkgLSBIICogMC4zIC8gMjEu
MCkgPCAxZS0xMzsgZ3JlZW4oJ1M3IFZvaWd0IGJpcmVmcmluZ2VuY2UgaWRlbnRpdHkgSCB0NCAv
IDIxJykKICAgIHByaW50KGYnQUxMIHtufS83IFNVSVRFUyBHUkVFTiAgKGluc3RydW1lbnQge21k
NWYoTUUpfSknKQpkZWYgbWFpbigpOgogICAgcCA9IGFyZ3BhcnNlLkFyZ3VtZW50UGFyc2VyKGRl
c2NyaXB0aW9uPV9fZG9jX18sIGZvcm1hdHRlcl9jbGFzcz1hcmdwYXJzZS5SYXdEZXNjcmlwdGlv
bkhlbHBGb3JtYXR0ZXIpOyBwLmFkZF9hcmd1bWVudCgnY21kJywgY2hvaWNlcz1bJ3NlbGZ0ZXN0
JywgJ3J1bicsICdjb21wYXJlJ10pOyBwLmFkZF9hcmd1bWVudCgnLS1waGFzZTAtb25seScsIGFj
dGlvbj0nc3RvcmVfdHJ1ZScpCiAgICBhID0gcC5wYXJzZV9hcmdzKCk7IHsnc2VsZnRlc3QnOiBj
bWRfc2VsZnRlc3QsICdydW4nOiBjbWRfcnVuLCAnY29tcGFyZSc6IGNtZF9jb21wYXJlfVthLmNt
ZF0oYSkKaWYgX19uYW1lX18gPT0gJ19fbWFpbl9fJzogbWFpbigpCg==
=====END-EMBED name=g_mscs2_chatleg.py=====

=====BEGIN-EMBED name=g_mscs2_chatleg_checkpoint.json md5=1c5b6b59829d2a6b9ae2b1a7a016832d bytes=31575 encoding=base64 armor_bytes=42654 QUARANTINED=====
ewogImdhdGUiOiAiRy1NU0NTMiIsCiAibGVnIjogImNoYXQiLAogImluc3RydW1lbnQiOiAiZ19t
c2NzMl9jaGF0bGVnLnB5IiwKICJpbnN0cnVtZW50X21kNSI6ICJmMjc3NTgwZGRmMGI0ZGE5NzM0
ZDExZWRiMDA5YzU0YiIsCiAibWVtb19sb2NrX21kNSI6ICJlZmRjYWJkY2Q5MzdjZGE0YWNiNjRm
OTQxZGM0YmIyYiIsCiAibWVtb19sb2NrX2J5dGVzIjogNDYwNTMsCiAibGVkZ2VyX2Jhc2VfbWQ1
IjogImYzNmJiZGIwNDEwNDAwODc4M2YyNzYzZjcwZmI5MTZmIiwKICJ0MV9saXN0X21kNSI6ICJi
ZTkyMWI4YzI5Zjc1NzhlODVlZDkyZjE0NTBjMTk1NiIsCiAieDFfbWQ1IjogIjIwMGU3YThiNzc1
NTc3NTY0MzY5YzY5MjRkMzhhODRjIiwKICJ4Nl9jaGF0X21kNSI6ICJjMDRjMGI4ZWEzNGNmZTYw
ZjIzMWFhMDY4MjhlNmNlNCIsCiAieDZfY2NfbWQ1IjogIjI0OWUxMWRkNTNjNGNiODJmMzAyYjE1
ZDNjOTRjMzM3IiwKICJ1dGMiOiAiMjAyNi0wOS0yNlQxNjowMjoxMC4zNzI0MzgrMDA6MDAiLAog
ImVsZWN0aW9ucyI6IHsKICAiRS1NUzItMSI6ICJhK2IiLAogICJFLU1TMi0yIjogImEiLAogICJF
LU1TMi0yYiI6ICJhK2IiLAogICJFLU1TMi0yYyI6ICIwMDErMTExIiwKICAiRS1NUzItMyI6ICJh
IiwKICAiRS1NUzItNCI6ICJhIiwKICAiRS1NUzItNSI6ICJhIiwKICAiRS1NUzItNiI6ICJhIiwK
ICAiRS1NUzItNyI6ICIwNTMwMjIxMCtNU0NTMXN0cmF0dW0iLAogICJFLU1TMi04IjogImEiCiB9
LAogInQxX3NjYW4iOiB7CiAgImluc3RydW1lbnQiOiAiQ0xFQU4iLAogICJtZW1vIjogIkNMRUFO
IgogfSwKICJxdWFkcmF0dXJlIjogewogICJuX3RoZXRhIjogNjQsCiAgIm5fcGhpIjogMTI4LAog
ICJzbzNfZ3JpZCI6IFsKICAgMTYsCiAgIDEwLAogICAxNgogIF0sCiAgIm5fZ3JpZCI6IFsKICAg
MTIsCiAgIDI0CiAgXQogfSwKICJ0NF9ncmlkIjogWwogIC0wLjUsCiAgLTAuMjUsCiAgLTAuMSwK
ICAtMC4wNSwKICAtMC4wMiwKICAwLjAsCiAgMC4wMiwKICAwLjA1LAogIDAuMSwKICAwLjI1LAog
IDAuNSwKICAxLjAKIF0sCiAidDJ0NF9ncmlkIjogWwogIC0wLjI1LAogIC0wLjEyNSwKICAwLjAs
CiAgMC4xMjUsCiAgMC4yNQogXSwKICJwaGFzZTAiOiB7CiAgIlBJTi1YVEFMIjogewogICAid29y
c3RfcmVsIjogMC4wLAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIlBJTi1WUkgwIjogewogICAi
d29yc3RfcmVsIjogMC4wLAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIlBJTi1IUzAiOiB7CiAg
ICJ3b3JzdF9yZWwiOiAwLjAsCiAgICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiUElOLUsyIjogewog
ICAid29yc3RfcmVsX2hleF9rYXBwYTIiOiAxLjM5Mjk2NzUyNDU4NTkyOTVlLTEyLAogICAid29y
c3RfYWJzX2N1YmljX2thcHBhMiI6IDIuMTU1MzM3Njk2NjQ3NjAzNWUtMTUsCiAgICJrYXBwYTJf
RTJfcmVjb21wdXRlZCI6IHsKICAgICJoZXhfc3RlcHxhIjogLTAuMDAxNDM5NDYxNzY5NDk4NzA0
MywKICAgICJoZXhfc3RlcHxiIjogLTAuMDAxNDM4NzAyNzE4NzQ5OTQ3NiwKICAgICJoZXhfZ2Vt
OHxhIjogLTAuMDAxODk1NjQ4NDgyNjcwMTM1MiwKICAgICJoZXhfZ2VtOHxiIjogLTAuMDAxODk2
MTM3NDY2NTI0MzY0NSwKICAgICJjdWJpY19zdGVwfDAwMSI6IC00LjU1MTM4NzA0ODc2MTYyNmUt
MTYsCiAgICAiY3ViaWNfc3RlcHwxMTEiOiAtMS42NzM5MTQzODU3MTQ3NjUyZS0xNiwKICAgICJj
dWJpY19nZW04fDAwMSI6IC0yLjE1NTMzNzY5NjY0NzYwMzVlLTE1LAogICAgImN1YmljX2dlbTh8
MTExIjogLTEuNjAxOTc3NTY5MTM4NTg4OGUtMTUKICAgfSwKICAgInBhc3NlZCI6IHRydWUKICB9
LAogICJGLUNUUkwtSVNPIjogewogICAid29yc3RfYWJzIjogNC40NDA4OTIwOTg1MDA2MjZlLTE2
LAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIkYtQ1RSTC1TTzMiOiB7CiAgICJkZXZfZnJvbV8w
cDQiOiA0Ljk5NjAwMzYxMDgxMzIwNGUtMTYsCiAgICJyX2FnZ18wX2FicyI6IDAuMCwKICAgInBh
c3NlZCI6IHRydWUKICB9LAogICJGLUNUUkwtUE9TIjogewogICAibWluX29kZl93ZWlnaHQiOiAw
LjM5NTAyNzA2MTc4NTUxNDk0LAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIkYtQ1RSTC1MMk5V
TEwiOiB7CiAgICJ3b3JzdF9hYnMiOiA1Ljg0OTkwODkzMzY3NjE3MWUtMTQsCiAgICJwYXNzZWQi
OiB0cnVlCiAgfSwKICAiRi1DVFJMLUw0RVhIQVVTVCI6IHsKICAgIndvcnN0X3JlbF90ZW5zb3Ii
OiA0LjMyNTc3Mjg3ODk1NDU4OGUtMTQsCiAgICJ3b3JzdF9hYnNfcl9hZ2ciOiA0LjQ0MDg5MjA5
ODUwMDYyNmUtMTYsCiAgICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiRi1DVFJMLUM0IjogewogICAi
d29yc3RfcmVsX2Nsb3NlZF9mb3JtIjogMi41MTg2OTI2NTUwMDk5NjA1ZS0xNCwKICAgIndvcnN0
X3JlbF9hZmZpbmUiOiA0LjA3NDA0MzcyMTY2NzMzMzRlLTE0LAogICAiaDBfZWZmZWN0X3JlbCI6
IDIuMzAyMTU4NDYzODYyNzI0OGUtMTQsCiAgICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiRi1DVFJM
LU1BUkciOiB7CiAgICJ3b3JzdF9hYnMiOiA4LjMyNjY3MjY4NDY4ODY3NGUtMTYsCiAgICJwYXNz
ZWQiOiB0cnVlCiAgfSwKICAiRi1DVFJMLVRFWDQiOiB7CiAgICJyX2FnZ190MV9hYnMiOiAwLjAw
MDQxMTgzMjY1NTc3MzM4MDksCiAgICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiRi1DVFJMLVFVQUQi
OiB7CiAgICJkb3VibGluZ19yZXNpZHVhbCI6IDIuMjYwMzQyODg2MDcwNDMxNWUtMTQsCiAgICJr
X3NwaGVyZV9kb3VibGluZyI6IDIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgInNvM19kb3VibGlu
ZyI6IDIuMjYwMzQyODg2MDcwNDMxNWUtMTQsCiAgICJwYXNzZWQiOiB0cnVlCiAgfQogfSwKICJw
aGFzZTBfd2l0bmVzcyI6IHsKICAic2luZ2xlX2NyeXN0YWwiOiB7CiAgICJoZXhfc3RlcHxhIjog
ewogICAgInZfRU0iOiA4LjQ5ODkyNjYzMDU4OTE0MywKICAgICJ2X1MyRTIiOiA4LjI2MTIzNTM5
MTEyNzExNCwKICAgICJ2X1MyaCI6IDguNDg5NDY4MzU4Mjg5MTA5LAogICAgInJfeHRhbF9FMiI6
IC0wLjAyNzk2NzIwNjg5NDg3MjUzLAogICAgInJfeHRhbF9oIjogLTAuMDAxMTEyODc4NDUwNTU1
Mjk5LAogICAgImxhbWJkYV9tZWFuIjogMC4wMDQ4MDg1NzU3MjQwMjI4MzgsCiAgICAibGFtYmRh
X21heCI6IDAuMDMzNTM3NTgyOTk3NzQ2MTIsCiAgICAibGFtYmRhX21heF9icmFuY2giOiAicVNW
IgogICB9LAogICAiaGV4X3N0ZXB8YiI6IHsKICAgICJ2X0VNIjogOC40OTkxMzgwNTk3NjQ3MiwK
ICAgICJ2X1MyRTIiOiA4LjI2MTYxMTU1MTMyODI4OCwKICAgICJ2X1MyaCI6IDguNDg5NjgwMjEw
NTkxNDY4LAogICAgInJfeHRhbF9FMiI6IC0wLjAyNzk0NzEyOTA4MTM0Njc3OCwKICAgICJyX3h0
YWxfaCI6IC0wLjAwMTExMjgwMDk4MTMxNjYwODQsCiAgICAibGFtYmRhX21lYW4iOiAwLjAwNDgw
ODYwMDQyODM0ODUxNCwKICAgICJsYW1iZGFfbWF4IjogMC4wMzM1MzQ1NDc2ODUyMDg4MjUsCiAg
ICAibGFtYmRhX21heF9icmFuY2giOiAicVNWIgogICB9LAogICAiaGV4X2dlbTh8YSI6IHsKICAg
ICJ2X0VNIjogMTAuMTY3NTcxMTQ3NDI3Nzc5LAogICAgInZfUzJFMiI6IDkuNzY3NTg0NjE1Njc5
NjM4LAogICAgInZfUzJoIjogMTAuMTU0MjAyMTYxNTY4MjAyLAogICAgInJfeHRhbF9FMiI6IC0w
LjAzOTMzOTQzNzcwMzMwMzUwNCwKICAgICJyX3h0YWxfaCI6IC0wLjAwMTMxNDg2NTIzODI4ODM4
NzQsCiAgICAibGFtYmRhX21lYW4iOiAwLjAwNDk1Mzc2OTYxODA2Mzk1MzUsCiAgICAibGFtYmRh
X21heCI6IDAuMDM1MTMzMDE4NDU5MDM3NDQsCiAgICAibGFtYmRhX21heF9icmFuY2giOiAicVNW
IgogICB9LAogICAiaGV4X2dlbTh8YiI6IHsKICAgICJ2X0VNIjogMTAuMTY3NDEyMzg4OTY1MzQy
LAogICAgInZfUzJFMiI6IDkuNzY3MzAwODE5MDk2NjU2LAogICAgInZfUzJoIjogMTAuMTU0MDQy
OTc3OTgwNTc3LAogICAgInJfeHRhbF9FMiI6IC0wLjAzOTM1MjM0OTg5NjExNzY5LAogICAgInJf
eHRhbF9oIjogLTAuMDAxMzE0OTI3NTgxNjk5NTk4NywKICAgICJsYW1iZGFfbWVhbiI6IDAuMDA0
OTUzNzg5OTMyMzI5NDIyLAogICAgImxhbWJkYV9tYXgiOiAwLjAzNTEzMzAxODQ1OTAzNzUyNSwK
ICAgICJsYW1iZGFfbWF4X2JyYW5jaCI6ICJxU1YiCiAgIH0sCiAgICJjdWJpY19zdGVwfDAwMSI6
IHsKICAgICJ2X0VNIjogOC4wMjgxMjQ4Mjc0OTQ4ODksCiAgICAidl9TMkUyIjogNy44ODkyNjQy
MTY5NTYyMjIsCiAgICAidl9TMmgiOiA4LjAxNTk1MTE2MjgzMTg3MiwKICAgICJyX3h0YWxfRTIi
OiAtMC4wMTcyOTY3Njc3NDEyMTU4LAogICAgInJfeHRhbF9oIjogLTAuMDAxNTE2Mzc3MTAyMzI0
NTUxLAogICAgImxhbWJkYV9tZWFuIjogMC4wMDgzOTIzMTkwMjg4NzgzLAogICAgImxhbWJkYV9t
YXgiOiAwLjAzODcwMDY5MzM0MTczNzQxLAogICAgImxhbWJkYV9tYXhfYnJhbmNoIjogInFUMiIK
ICAgfSwKICAgImN1YmljX3N0ZXB8MTExIjogewogICAgInZfRU0iOiA4LjAyODEyNDgyNzQ5NDg4
OSwKICAgICJ2X1MyRTIiOiA4LjEyMDY5ODU2Nzg1NDAwMSwKICAgICJ2X1MyaCI6IDguMDE1OTUx
MTYyODMxODcyLAogICAgInJfeHRhbF9FMiI6IDAuMDExNTMxMTc4NDk0MTQ0MDksCiAgICAicl94
dGFsX2giOiAtMC4wMDE1MTYzNzcxMDIzMjQ1NTEsCiAgICAibGFtYmRhX21lYW4iOiAwLjAwODM5
MjMxOTAyODg3ODMsCiAgICAibGFtYmRhX21heCI6IDAuMDM4NzAwNjkzMzQxNzM3NDEsCiAgICAi
bGFtYmRhX21heF9icmFuY2giOiAicVQyIgogICB9LAogICAiY3ViaWNfZ2VtOHwwMDEiOiB7CiAg
ICAidl9FTSI6IDkuNzIxMTcxMDE1MDc4MjEsCiAgICAidl9TMkUyIjogOS41MTg1NTgwNzE4MDMz
LAogICAgInZfUzJoIjogOS43MDMyMzQ0NzI1MjgyNTEsCiAgICAicl94dGFsX0UyIjogLTAuMDIw
ODQyNDQyMDIyNzQwMzI2LAogICAgInJfeHRhbF9oIjogLTAuMDAxODQ1MTAxMDE5NDI4NDc0NSwK
ICAgICJsYW1iZGFfbWVhbiI6IDAuMDA5MzEwNTAzODU5NjUyOCwKICAgICJsYW1iZGFfbWF4Ijog
MC4wNDMyOTI3MDE5NTQxMjAwMTUsCiAgICAibGFtYmRhX21heF9icmFuY2giOiAicVQyIgogICB9
LAogICAiY3ViaWNfZ2VtOHwxMTEiOiB7CiAgICAidl9FTSI6IDkuNzIxMTcxMDE1MDc4MjEsCiAg
ICAidl9TMkUyIjogOS44NTYyNDYzMTA1OTQ4MTgsCiAgICAidl9TMmgiOiA5LjcwMzIzNDQ3MjUy
ODI1MSwKICAgICJyX3h0YWxfRTIiOiAwLjAxMzg5NDk2MTM0ODQ5MzU1LAogICAgInJfeHRhbF9o
IjogLTAuMDAxODQ1MTAxMDE5NDI4NDc0NSwKICAgICJsYW1iZGFfbWVhbiI6IDAuMDA5MzEwNTAz
ODU5NjUyOCwKICAgICJsYW1iZGFfbWF4IjogMC4wNDMyOTI3MDE5NTQxMjAwMTUsCiAgICAibGFt
YmRhX21heF9icmFuY2giOiAicVQyIgogICB9CiAgfSwKICAidlRfdDAiOiB7CiAgICJoZXhfc3Rl
cHxhIjogewogICAgIlYiOiA4LjU0Nzc3OTQzODczOTIyOCwKICAgICJSIjogOC4yODgzNDEwMjk5
ODM5MjcsCiAgICAiSCI6IDguNDE5MDU5NjM3NTkxNjAzLAogICAgIkhTbG8iOiA4LjM5MDg1OTcz
MTcyODI0NywKICAgICJIU2hpIjogOC40MjQ1ODI0MTk0MDM0NTcKICAgfSwKICAgImhleF9zdGVw
fGIiOiB7CiAgICAiViI6IDguNTQ3OTgyOTk3OTU1Mjk1LAogICAgIlIiOiA4LjI4ODU3NjAyOTE4
MTYyNywKICAgICJIIjogOC40MTkyNzg2NDg1Nzk2MTIsCiAgICAiSFNsbyI6IDguMzkxMDg0NzQ2
ODM3OTQ3LAogICAgIkhTaGkiOiA4LjQyNDgwMzI1NzcyMzgzMgogICB9LAogICAiaGV4X2dlbTh8
YSI6IHsKICAgICJWIjogMTAuMjQ4OTk3Njc0NTY5NTk2LAogICAgIlIiOiA5LjgzMDA3NjMzNjUw
NTMyOSwKICAgICJIIjogMTAuMDQxNzIxODE3MzY5MTQ3LAogICAgIkhTbG8iOiA5Ljk5MDkxMzAw
MTU3MTE1NiwKICAgICJIU2hpIjogMTAuMDUyNzk3NzU0OTQ5MDM3CiAgIH0sCiAgICJoZXhfZ2Vt
OHxiIjogewogICAgIlYiOiAxMC4yNDg4NDc0MTQ4NzIyMzQsCiAgICAiUiI6IDkuODI5ODkwMzEy
NTY2MDEsCiAgICAiSCI6IDEwLjA0MTU1NDA4NTE2MDYzMiwKICAgICJIU2xvIjogOS45OTA3Mzk4
Mjk3MTk4NiwKICAgICJIU2hpIjogMTAuMDUyNjI5OTU5Mjk0OTQ1CiAgIH0sCiAgICJjdWJpY19z
dGVwfDAwMSI6IHsKICAgICJWIjogOC4xMTU3OTQ0Nzc0MzcxOTUsCiAgICAiUiI6IDcuNDY4ODc3
MzQxNjg2NjA3LAogICAgIkgiOiA3Ljc5OTA0NjM3NTg0NDkyMywKICAgICJIU2xvIjogNy43NTg2
MTQ0OTAyMTEwODcsCiAgICAiSFNoaSI6IDcuODY3OTUzMDA1OTA0Nzc1CiAgIH0sCiAgICJjdWJp
Y19zdGVwfDExMSI6IHsKICAgICJWIjogOC4xMTU3OTQ0Nzc0MzcxOTUsCiAgICAiUiI6IDcuNDY4
ODc3MzQxNjg2NjA3LAogICAgIkgiOiA3Ljc5OTA0NjM3NTg0NDkyMywKICAgICJIU2xvIjogNy43
NTg2MTQ0OTAyMTEwODcsCiAgICAiSFNoaSI6IDcuODY3OTUzMDA1OTA0Nzc1CiAgIH0sCiAgICJj
dWJpY19nZW04fDAwMSI6IHsKICAgICJWIjogOS44NzI0OTIwODY2MDEwMiwKICAgICJSIjogOC43
MDY3NzE1Mjc4MzEzNTIsCiAgICAiSCI6IDkuMzA3ODk5MDc2NTMzMTc5LAogICAgIkhTbG8iOiA5
LjIxMTcyMTA2NDM3MDg2MSwKICAgICJIU2hpIjogOS40NTY4NTQ5ODQ1ODg3MzgKICAgfSwKICAg
ImN1YmljX2dlbTh8MTExIjogewogICAgIlYiOiA5Ljg3MjQ5MjA4NjYwMTAyLAogICAgIlIiOiA4
LjcwNjc3MTUyNzgzMTM1MiwKICAgICJIIjogOS4zMDc4OTkwNzY1MzMxNzksCiAgICAiSFNsbyI6
IDkuMjExNzIxMDY0MzcwODYxLAogICAgIkhTaGkiOiA5LjQ1Njg1NDk4NDU4ODczOAogICB9CiAg
fSwKICAiaHNfcmVmIjogewogICAiaGV4X3N0ZXAiOiB7CiAgICAiaGkiOiBbCiAgICAgMTM1LjM2
NjU5NTI4MzY5NzYyLAogICAgIDExNS41NTk4NzMyODkxOTkwMgogICAgXSwKICAgICJsbyI6IFsK
ICAgICAxMzQuNjA3MDg5NDM3MTI2MDYsCiAgICAgNjAuMDMwODAwMDAxNDM3OTcKICAgIF0KICAg
fSwKICAgImhleF9nZW04IjogewogICAgImhpIjogWwogICAgIDIzMC4xMzYwNDgzOTA3MzEzLAog
ICAgIDE3OC4yOTQzNDE3NTU3Njc2NQogICAgXSwKICAgICJsbyI6IFsKICAgICAyMjkuNjk1NzU0
MzM1ODY1NzYsCiAgICAgODQuODI0NTAwMDAyMzEwOTEKICAgIF0KICAgfSwKICAgImN1YmljX3N0
ZXAiOiB7CiAgICAiaGkiOiBbCiAgICAgMTIzLjgzMjQ2NjY2NjA5MDY4LAogICAgIDg1LjI5MzM5
OTk5OTE0NjEyCiAgICBdLAogICAgImxvIjogWwogICAgIDEyMy44MzI0NjY2NjcyNDI2NiwKICAg
ICAzNi43MjUyMDAwMDA4NjM0NwogICAgXQogICB9LAogICAiY3ViaWNfZ2VtOCI6IHsKICAgICJo
aSI6IFsKICAgICAyMTAuMjc1NDk5OTk5MDkzMSwKICAgICAxMzEuNTQzNTk5OTk4NjQ0MTQKICAg
IF0sCiAgICAibG8iOiBbCiAgICAgMjEwLjI3NTUwMDAwMDkwNjkzLAogICAgIDQ2LjM0OTg1MDAw
MTM1OTE0CiAgICBdCiAgIH0KICB9CiB9LAogInBoYXNlMiI6IHsKICAiaGV4X3N0ZXB8YSI6IHsK
ICAgInJfYWdnX0UyX1ZSSCI6IFsKICAgIDQuMDA3NTExMjE1NDUzNjE4NWUtMDUsCiAgICAxLjAw
MjE4NzYyNTU1MzkyOTdlLTA1LAogICAgMS42MDM4MTYwOTE5MzI5NDE0ZS0wNiwKICAgIDQuMDA5
ODExMjE0MTc4NDI3ZS0wNywKICAgIDYuNDE1OTYxMDczNTM1OTI1ZS0wOCwKICAgIDAuMCwKICAg
IDYuNDE2MzE1MzY3OTA3NTQ0ZS0wOCwKICAgIDQuMDEwMzY0ODQyNDMyNzc4N2UtMDcsCiAgICAx
LjYwNDI1OTAwMjk3NDExNzdlLTA2LAogICAgMS4wMDI4Nzk3NDc5NTc3NjM0ZS0wNSwKICAgIDQu
MDEzMDUwMzExMDgwMjM1ZS0wNSwKICAgIDAuMDAwMTYwNjU2NTA5MzU0ODE3MzUKICAgXSwKICAg
InJfYWdnX2hfVlJIIjogWwogICAgLTEuODY1OTcxMDU1NDQ4MDU2OWUtMDYsCiAgICAtNC42Nzgy
NjIzNDQxODIxMTZlLTA3LAogICAgLTcuNDk4Mzk5ODc4NzkxNDE3ZS0wOCwKICAgIC0xLjg3NTcx
NDI3Mjc5MjA5NWUtMDgsCiAgICAtMy4wMDIyMTg4MDY4OTEyMjE0ZS0wOSwKICAgIDAuMCwKICAg
IC0zLjAwMzY2MDU0MjUxMDk5OTdlLTA5LAogICAgLTEuODc3OTY2OTE1MzA5MDU5NWUtMDgsCiAg
ICAtNy41MTY0MjE0MDc1MDUxOTJlLTA4LAogICAgLTQuNzA2NDIzNTM2NDQ5MTIyNWUtMDcsCiAg
ICAtMS44ODg1MDcxNjQ0MjcwMTEzZS0wNiwKICAgIC03LjYwNDA1MTgwODQ0MDgxNWUtMDYKICAg
XSwKICAgInJfYWdnX0UyX0hTIjogWwogICAgMy45OTI5MjI4NTQ1Nzg3NTFlLTA1LAogICAgOS45
ODc3OTMxMzc4Nzc3ODdlLTA2LAogICAgMS41OTg1NzU0MjA3MDI2MzA0ZS0wNiwKICAgIDMuOTk2
ODc5NzY0OTMzNjgwN2UtMDcsCiAgICA2LjM5NTQzMTQ3MzI5MzkxMWUtMDgsCiAgICAwLjAsCiAg
ICA2LjM5NTk5Njk3NjQ5MzczNGUtMDgsCiAgICAzLjk5Nzc2MzM3ODExNjMwMzZlLTA3LAogICAg
MS41OTkyODIzMDk0NzIzNzE4ZS0wNiwKICAgIDkuOTk4ODM4Mzc2Mzc5MzgyZS0wNiwKICAgIDQu
MDAxNzU5MzIyNjI0OTIwNGUtMDUsCiAgICAwLjAwMDE2MDI0OTUxMzEzNzg2NjczCiAgIF0sCiAg
ICJyX2FnZ19FMl9WIjogWwogICAgNC41OTA2NjE1MzkzNDk4Mzg0ZS0wNSwKICAgIDEuMTQ3MTI2
Mjk2MjQxNDc0MWUtMDUsCiAgICAxLjgzNDkwMzkxMjM2NzczNThlLTA2LAogICAgNC41ODY4NTI2
ODY1NjExMTZlLTA3LAogICAgNy4zMzg1NzY1NDY0NDUwOTdlLTA4LAogICAgMC4wLAogICAgNy4z
MzgwNjMxNzkzMTg1MWUtMDgsCiAgICA0LjU4NjA1MDUzMDQ0MTgxZS0wNywKICAgIDEuODM0MjYy
MTgyMzY1MjY1ZS0wNiwKICAgIDEuMTQ2MTIzNTU0MTA3NzAzZS0wNSwKICAgIDQuNTgyNjM4NDc5
MjAwMjYzZS0wNSwKICAgIDAuMDAwMTgzMTY4OTU3NDIxNjUzMwogICBdLAogICAicl9hZ2dfRTJf
UiI6IFsKICAgIDMuMzg3NTI5NzM3NDA4NjM0NGUtMDUsCiAgICA4LjQ4MDU3ODEzNjg0OTEwNGUt
MDYsCiAgICAxLjM1ODA0ODI0NzYzNDk2ODdlLTA2LAogICAgMy4zOTYwOTUyMzgzNjE1OTZlLTA3
LAogICAgNS40MzQ2OTI0NTE2MjI0MjVlLTA4LAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwK
ICAgIDUuNDM1OTUxMDY3MDU2NTIxNGUtMDgsCiAgICAzLjM5ODA2MTgyMDgxNDAzNTZlLTA3LAog
ICAgMS4zNTk2MjE1MjQ5MjExOTUxZS0wNiwKICAgIDguNTA1MTYxOTUzNjA5MTc1ZS0wNiwKICAg
IDMuNDA3MjAwNjY0MzYyNjE5NmUtMDUsCiAgICAwLjAwMDEzNjcxNjgzNDQ4MTkwOTIKICAgXSwK
ICAgImxhbWJkYV9tZWFuX3Q0IjogWwogICAgOS4zODAzNzEzNTgyMzM4MDNlLTA2LAogICAgMi4z
NDg1NTc1MzgyNjU1NzI1ZS0wNiwKICAgIDMuNzYxMTgxNTM3MDA4NzZlLTA3LAogICAgOS40MDU5
MzA0MTY2ODA4MjZlLTA4LAogICAgMS41MDUyMzcyNjcyODc5NGUtMDgsCiAgICAxLjgxNjczNzg4
NjQxMjQ5MTdlLTMwLAogICAgMS41MDU2MjQ5MDAxNzg1OTZlLTA4LAogICAgOS40MTE5ODcyMTAz
NzMyODRlLTA4LAogICAgMy43NjYwMjcwNTc1MzI3ODllLTA3LAogICAgMi4zNTYxMjk1OTk5NzQy
NzFlLTA2LAogICAgOS40NDA5NzQ2MDE4MzA1MTFlLTA2LAogICAgMy43OTA2MzM1OTczNzgzNjJl
LTA1CiAgIF0sCiAgICJTNF9FMiI6IC0yLjIxMzYxNjc4MDA2MDY2MDJlLTEzLAogICAiUzRfaCI6
IDcuNjY1NDIzMDg0NTQ3ODQ0ZS0xNCwKICAgImthcHBhNDRfRTIiOiAwLjAwMDE2MDQwNTM0NjE0
MzY3OTg3LAogICAia2FwcGE0NF9oIjogLTcuNTA3NzM5NjYxOTcyMDA0ZS0wNiwKICAgImthcHBh
NDQ0X0UyIjogMi4yMTQ4MjY5NDE3MTQ2NDNlLTA3LAogICAia2FwcGE0NF9FMl9IUyI6IDAuMDAw
MTU5ODkzMDQ3Njg0Mzc3LAogICAiaGFsdmluZ19kZXZfa2FwcGE0NCI6IDEuNjA1NTY5NTM2NTA3
NTkxMmUtMDksCiAgICJrYXBwYTQ0X0UyX3dpbmRvdzBwMSI6IDAuMDAwMTYwNDAzNzQwNTc0MTQz
MzcsCiAgICJmaXRfcmVzaWR1YWwiOiA3LjkxNzg1NTkwNDkxNDQzNWUtMTIsCiAgICJiaXJlZl9i
MV9WUkgiOiAwLjAxNjI0MDg1NDEwNzIzNTExLAogICAidlRfVlJIIjogOC40MTkwNTk2Mzc1OTE2
MDMsCiAgICJ2VF9IU19sbyI6IDguMzkwODU5NzMxNzI4MjQ3LAogICAidlRfSFNfaGkiOiA4LjQy
NDU4MjQxOTQwMzQ1NywKICAgInF1YWRmb3JtIjogewogICAgImthcHBhMjIiOiAtMC4wMDE0Mzk0
NjkzMDIwMDMyOTAzLAogICAgImthcHBhMjQiOiAtMS4yNDg4NzkwNzMwNDkxODg3ZS0wOCwKICAg
ICJrYXBwYTQ0IjogMC4wMDAxNjAzOTkwMzc2Mzk0NTMxNywKICAgICJyZXNpZHVhbCI6IDMuMzUz
ODQyMjE2OTAxMTgyNGUtMTAKICAgfSwKICAgImhzX3JlZiI6IHsKICAgICJoaSI6IFsKICAgICAx
MzUuMzY2NTk1MjgzNjk3NjIsCiAgICAgMTE1LjU1OTg3MzI4OTE5OTAyCiAgICBdLAogICAgImxv
IjogWwogICAgIDEzNC42MDcwODk0MzcxMjYwNiwKICAgICA2MC4wMzA4MDAwMDE0Mzc5NwogICAg
XQogICB9CiAgfSwKICAiaGV4X3N0ZXB8YiI6IHsKICAgInJfYWdnX0UyX1ZSSCI6IFsKICAgIDQu
MDA3NzQyOTcyMjg5NTYzZS0wNSwKICAgIDEuMDAyMjQ1NzEwMjI0MzM2NWUtMDUsCiAgICAxLjYw
MzkwOTE3MzQ3NTQxNTJlLTA2LAogICAgNC4wMTAwNDQwNDEyNjkzNjdlLTA3LAogICAgNi40MTYz
MzM3MzA5OTYzNzFlLTA4LAogICAgMC4wLAogICAgNi40MTY2ODgyMDMwMDM2NzNlLTA4LAogICAg
NC4wMTA1OTc5MjcwOTU0NjA2ZS0wNywKICAgIDEuNjA0MzUyMjg3NDY1MzYwNGUtMDYsCiAgICAx
LjAwMjkzODE0OTYxOTA0ODFlLTA1LAogICAgNC4wMTMyODQ2MDUxOTc2NzU2ZS0wNSwKICAgIDAu
MDAwMTYwNjY1OTQwNTM3OTg1MQogICBdLAogICAicl9hZ2dfaF9WUkgiOiBbCiAgICAtMS44NjYy
ODcxMzE5NDYzNjQ4ZS0wNiwKICAgIC00LjY3OTA1Njc4NTM2MTYyNGUtMDcsCiAgICAtNy40OTk2
NzUyNDc0OTA5NTZlLTA4LAogICAgLTEuODc2MDMzNDYxOTExNjc0N2UtMDgsCiAgICAtMy4wMDI3
MjkzOTg0NjAyNDY2ZS0wOSwKICAgIDAuMCwKICAgIC0zLjAwNDE3MTkxMTIzNjE0MmUtMDksCiAg
ICAtMS44NzgyODY4NTkzODAyOTZlLTA4LAogICAgLTcuNTE3NzAyNzI3MDAwMTQyZS0wOCwKICAg
IC00LjcwNzIyNzIzNDY2ODIxZS0wNywKICAgIC0xLjg4ODgzMDY1MDEwOTY5NjNlLTA2LAogICAg
LTcuNjA1MzYzMDkwMDc5NjQyZS0wNgogICBdLAogICAicl9hZ2dfRTJfSFMiOiBbCiAgICAzLjk5
MzE2MDU1MDY4NTk5MjRlLTA1LAogICAgOS45ODgzODgyOTAwMjc1NzJlLTA2LAogICAgMS41OTg2
NzA3MzMzNDkyOTQ0ZS0wNiwKICAgIDMuOTk3MTE4MTE4NzE0ODM3NWUtMDcsCiAgICA2LjM5NTgx
Mjk0NTkyNTE3MmUtMDgsCiAgICAwLjAsCiAgICA2LjM5NjM3ODU2MDE0NzI5OGUtMDgsCiAgICAz
Ljk5ODAwMTg4MDY2NzM0NTZlLTA3LAogICAgMS41OTkzNzc3NDA2OTA4NTVlLTA2LAogICAgOS45
OTk0MzUzNzkyNzA5NDllLTA2LAogICAgNC4wMDE5OTg0OTk5MjUxMDhlLTA1LAogICAgMC4wMDAx
NjAyNTkxMTA3ODA5OTE0MgogICBdLAogICAicl9hZ2dfRTJfViI6IFsKICAgIDQuNTkwNjc2NDc4
Njg4NDkzNWUtMDUsCiAgICAxLjE0NzEzMDAyNDYzNjg0NDNlLTA1LAogICAgMS44MzQ5MDk4NzIw
NDQ5MzJlLTA2LAogICAgNC41ODY4Njc1ODEzMTMyMTRlLTA3LAogICAgNy4zMzg2MDAzOTQwMzU2
NjZlLTA4LAogICAgMC4wLAogICAgNy4zMzgwODcwMjY5MDkwNzllLTA4LAogICAgNC41ODYwNjU0
MTQwOTE2NzhlLTA3LAogICAgMS44MzQyNjgxMzQ3MTQ5ODkyZS0wNiwKICAgIDEuMTQ2MTI3Mjcw
Nzc5MTE4MWUtMDUsCiAgICA0LjU4MjY1MzMyNDQxNDIxZS0wNSwKICAgIDAuMDAwMTgzMTY5NTQ5
NjY4NTcxNDYKICAgXSwKICAgInJfYWdnX0UyX1IiOiBbCiAgICAzLjM4Nzk5NzU5NDgwNTkwM2Ut
MDUsCiAgICA4LjQ4MTc1MDk0NTE0NDAyOWUtMDYsCiAgICAxLjM1ODIzNjIxMjE2Nzc5NmUtMDYs
CiAgICAzLjM5NjU2NTQxNzgxMjUyNWUtMDcsCiAgICA1LjQzNTQ0NDk4Mjk5Mjk3NmUtMDgsCiAg
ICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgNS40MzY3MDM5MzE0OTM5OGUtMDgsCiAgICAz
LjM5ODUzMjUzOTgzMzM1NDNlLTA3LAogICAgMS4zNTk4MDk5MjI4ODUwOTEzZS0wNiwKICAgIDgu
NTA2MzQxNTM2OTI5MDg1ZS0wNiwKICAgIDMuNDA3NjczOTQ0MTc3OTU4ZS0wNSwKICAgIDAuMDAw
MTM2NzM1ODg4OTM4MzY2MwogICBdLAogICAibGFtYmRhX21lYW5fdDQiOiBbCiAgICA5LjM4MjI4
NTg3ODA2Nzc4NmUtMDYsCiAgICAyLjM0OTAzNzU2NzU4NTU2MjZlLTA2LAogICAgMy43NjE5NTEw
MTc0ODY0MThlLTA3LAogICAgOS40MDc4NTUzNTA0MzMyOTNlLTA4LAogICAgMS41MDU1NDUzNzY1
MjgwM2UtMDgsCiAgICAyLjg0OTMwODc5Nzk1MjU1MDdlLTMwLAogICAgMS41MDU5MzMxNzA4NTQ0
NTM1ZS0wOCwKICAgIDkuNDEzOTE0NjY2ODU4NDNlLTA4LAogICAgMy43NjY3OTg1NTYyMjQ1OTNl
LTA3LAogICAgMi4zNTY2MTI3ODM0MTI4NDNlLTA2LAogICAgOS40NDI5MTQzNzM1NTI2NzdlLTA2
LAogICAgMy43OTE0MTU3NDEyMDM2Mjc2ZS0wNQogICBdLAogICAiUzRfRTIiOiAtMi4xOTkwMjY4
Mzg4MDc1OTg3ZS0xMywKICAgIlM0X2giOiA3LjQ4NTg3MTY4MTIxNDcxNWUtMTQsCiAgICJrYXBw
YTQ0X0UyIjogMC4wMDAxNjA0MTQ2NjUwMzQwODU4OCwKICAgImthcHBhNDRfaCI6IC03LjUwOTAx
ODE2ODg5NDQxN2UtMDYsCiAgICJrYXBwYTQ0NF9FMiI6IDIuMjE1ODQxMDc2MjgwODk3NWUtMDcs
CiAgICJrYXBwYTQ0X0UyX0hTIjogMC4wMDAxNTk5MDI1ODQ5MjMzOTYwNiwKICAgImhhbHZpbmdf
ZGV2X2thcHBhNDQiOiAxLjYwNjE2MTYzNTA4OTEyNzJlLTA5LAogICAia2FwcGE0NF9FMl93aW5k
b3cwcDEiOiAwLjAwMDE2MDQxMzA1ODg3MjQ1MDgsCiAgICJmaXRfcmVzaWR1YWwiOiA3LjkyMDc3
NDUzMDA1ODYxMmUtMTIsCiAgICJiaXJlZl9iMV9WUkgiOiAwLjAxNjI0MTc5NzU3NzIyODA2MywK
ICAgInZUX1ZSSCI6IDguNDE5Mjc4NjQ4NTc5NjEyLAogICAidlRfSFNfbG8iOiA4LjM5MTA4NDc0
NjgzNzk0NywKICAgInZUX0hTX2hpIjogOC40MjQ4MDMyNTc3MjM4MzIsCiAgICJxdWFkZm9ybSI6
IHsKICAgICJrYXBwYTIyIjogLTAuMDAxNDM4NzEwMjQ3ODgzNjA2LAogICAgImthcHBhMjQiOiAt
MS4yNDg0NjE1MDgzOTAxMjM2ZS0wOCwKICAgICJrYXBwYTQ0IjogMC4wMDAxNjA0MDgzNTgyMzQ2
NTUyNSwKICAgICJyZXNpZHVhbCI6IDMuMzUyMDg5MTYxMzk3NTY3ZS0xMAogICB9LAogICAiaHNf
cmVmIjogewogICAgImhpIjogWwogICAgIDEzNS4zNjY1OTUyODM2OTc2MiwKICAgICAxMTUuNTU5
ODczMjg5MTk5MDIKICAgIF0sCiAgICAibG8iOiBbCiAgICAgMTM0LjYwNzA4OTQzNzEyNjA2LAog
ICAgIDYwLjAzMDgwMDAwMTQzNzk3CiAgICBdCiAgIH0KICB9LAogICJoZXhfZ2VtOHxhIjogewog
ICAicl9hZ2dfRTJfVlJIIjogWwogICAgNC40ODUxMjE1NDk3MzU0NmUtMDUsCiAgICAxLjEyMTU3
ODI3MTAxMjc3OTdlLTA1LAogICAgMS43OTQ4MzQwMTk0MDg0OTc3ZS0wNiwKICAgIDQuNDg3MzUx
OTMyMjU4NTc2NGUtMDcsCiAgICA3LjE4MDAyMjk5ODM3NjUwMWUtMDgsCiAgICAtMi4yMjA0NDYw
NDkyNTAzMTNlLTE2LAogICAgNy4xODAzNzM4Mjg4NTIyODJlLTA4LAogICAgNC40ODc5MDAxMTgx
OTk2NjE0ZS0wNywKICAgIDEuNzk1MjcyNTc0MTU2NTdlLTA2LAogICAgMS4xMjIyNjM2MDE4NzE1
MDkzZS0wNSwKICAgIDQuNDkwNjA2NzMzODY0NTg4ZS0wNSwKICAgIDAuMDAwMTc5NzYzMjYwODAz
Mzc4MzQKICAgXSwKICAgInJfYWdnX2hfVlJIIjogWwogICAgLTEuOTI3NDYxOTcxMzYyNzMxN2Ut
MDYsCiAgICAtNC44MzIxODUyNjYzNjc5NzJlLTA3LAogICAgLTcuNzQ0ODkxNTUwMzA5Nzc0ZS0w
OCwKICAgIC0xLjkzNzM1NjI2NDMwMzI0N2UtMDgsCiAgICAtMy4xMDA4NjQ3ODcxNjQ0MjU3ZS0w
OSwKICAgIDAuMCwKICAgIC0zLjEwMjMzMTk0Njg5MTQ2OGUtMDksCiAgICAtMS45Mzk2NDg4MDgy
MzU3MTY2ZS0wOCwKICAgIC03Ljc2MzIzMjI1NzA0MDg5N2UtMDgsCiAgICAtNC44NjA4NDU0MjA2
MTc4MjFlLTA3LAogICAgLTEuOTUwMzk4MDk0ODA3NjgxNmUtMDYsCiAgICAtNy44NTI3ODE0NDkx
MDI1MDhlLTA2CiAgIF0sCiAgICJyX2FnZ19FMl9IUyI6IFsKICAgIDQuNDY4MDI2ODgxNzQzMTky
ZS0wNSwKICAgIDEuMTE3NjU5NDg4MjI1NjE5N2UtMDUsCiAgICAxLjc4ODg4Mzg0NTI3NzMxMTVl
LTA2LAogICAgNC40NzI3MzQzNDUxMTc4NTdlLTA3LAogICAgNy4xNTY4NzkwMDA1NDcxNzhlLTA4
LAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIDcuMTU3NTUxNDYyNjMzMTk0ZS0wOCwK
ICAgIDQuNDczNzg1MDg2ODMzNzE1ZS0wNywKICAgIDEuNzg5NzI0NDM5MzE2MTMxNmUtMDYsCiAg
ICAxLjExODk3MjkyODgyNjM0NWUtMDUsCiAgICA0LjQ3ODUzNDc3NTU2NDkyNGUtMDUsCiAgICAw
LjAwMDE3OTM1NDE2ODE3NjcxNTIzCiAgIF0sCiAgICJyX2FnZ19FMl9WIjogWwogICAgNS4zMDM4
NzUxNzI3NDYzMzFlLTA1LAogICAgMS4zMjUyNTUwODI2OTU4NzUzZS0wNSwKICAgIDIuMTE5NzUy
NDM0NDcwNzEyZS0wNiwKICAgIDUuMjk4ODQ2OTAxMjU4MjU4ZS0wNywKICAgIDguNDc3NjQ2OTE3
ODAzODM4ZS0wOCwKICAgIDAuMCwKICAgIDguNDc2OTc0ODU1Mzk4MTEyZS0wOCwKICAgIDUuMjk3
Nzk2ODE2Nzk0NDMxZS0wNywKICAgIDIuMTE4OTEyMzYzMTI0ODkyZS0wNiwKICAgIDEuMzIzOTQy
NDAzNjg1OTQwNGUtMDUsCiAgICA1LjI5MzM3MTgwMzg2MDU4MDRlLTA1LAogICAgMC4wMDAyMTE1
NjEwNzY5NDkzMDcwNAogICBdLAogICAicl9hZ2dfRTJfUiI6IFsKICAgIDMuNTk1NTY1NTk2NzAz
NDg3ZS0wNSwKICAgIDkuMDAyMTkxOTU5NDI4NTNlLTA2LAogICAgMS40NDE2NTgwNzA2OTk5NTgy
ZS0wNiwKICAgIDMuNjA1MjQ4MzY2NTExNjU5N2UtMDcsCiAgICA1Ljc2OTQ2MTczMDU4NzAxMWUt
MDgsCiAgICAyLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICA1Ljc3MDg4NzA3OTMxNDk0NmUtMDgs
CiAgICAzLjYwNzQ3NTQ2Mjc5NjgyNzVlLTA3LAogICAgMS40NDM0Mzk3NjEyNzI4MTM0ZS0wNiwK
ICAgIDkuMDMwMDMyNTk4Nzc3OTkzZS0wNiwKICAgIDMuNjE3ODQzMDM2ODg0OTQ5ZS0wNSwKICAg
IDAuMDAwMTQ1MjAxNTkxMTE3MTk0NDQKICAgXSwKICAgImxhbWJkYV9tZWFuX3Q0IjogWwogICAg
OC41ODY1NDQ5NzEzMzY2NTllLTA2LAogICAgMi4xNDk3Njc3MTg1NjExOTVlLTA2LAogICAgMy40
NDI3OTAxODQ3NzQ0MjY2ZS0wNywKICAgIDguNjA5Njc1Nzc0MDU3ODY3ZS0wOCwKICAgIDEuMzc3
ODA5ODc5Mzc1MjQ5MWUtMDgsCiAgICAyLjg3MzA2MjQzODA3MDUzMDJlLTMwLAogICAgMS4zNzgx
NjE4NDA4NDMxMjY2ZS0wOCwKICAgIDguNjE1MTc1MjAyMDE2MDEyZS0wOCwKICAgIDMuNDQ3MTg5
ODEyODY0MTg5ZS0wNywKICAgIDIuMTU2NjQzMDc1MTA4MjQyZS0wNiwKICAgIDguNjQxNTc0NjI0
ODk5NDdlLTA2LAogICAgMy40Njk2NjIzMDE5MzczMDJlLTA1CiAgIF0sCiAgICJTNF9FMiI6IC0y
LjY1MjA0NjM3NDU1MTQ2NGUtMTMsCiAgICJTNF9oIjogOC4zOTQ0MDgxOTk4NDQxODNlLTE0LAog
ICAia2FwcGE0NF9FMiI6IDAuMDAwMTc5NTA3Mjk1Nzk0ODQxMTUsCiAgICJrYXBwYTQ0X2giOiAt
Ny43NTQ0MTQ4NDk0ODkyODhlLTA2LAogICAia2FwcGE0NDRfRTIiOiAyLjE5MzEwMDk3MzI4MjQ4
MjJlLTA3LAogICAia2FwcGE0NF9FMl9IUyI6IDAuMDAwMTc4OTMwNTg4NTcyNTc0NCwKICAgImhh
bHZpbmdfZGV2X2thcHBhNDQiOiAxLjk4MzYyNjkzMzIyOTM5NTNlLTA5LAogICAia2FwcGE0NF9F
Ml93aW5kb3cwcDEiOiAwLjAwMDE3OTUwNTMxMjE2NzkwNzkyLAogICAiZml0X3Jlc2lkdWFsIjog
OS43ODIyNDQ5MzA4MDUwNzhlLTEyLAogICAiYmlyZWZfYjFfVlJIIjogMC4wMTgxNzQ4ODI1MTEx
NzczOSwKICAgInZUX1ZSSCI6IDEwLjA0MTcyMTgxNzM2OTE0NywKICAgInZUX0hTX2xvIjogOS45
OTA5MTMwMDE1NzExNTYsCiAgICJ2VF9IU19oaSI6IDEwLjA1Mjc5Nzc1NDk0OTAzNywKICAgInF1
YWRmb3JtIjogewogICAgImthcHBhMjIiOiAtMC4wMDE4OTU2NTk5MDY5NDY4MjkzLAogICAgImth
cHBhMjQiOiAtMS44MzcyMTM0MTc4NTE5NDNlLTA4LAogICAgImthcHBhNDQiOiAwLjAwMDE3OTQ5
ODQyMjAyNTg2OTc2LAogICAgInJlc2lkdWFsIjogNS4yMzQ1MDE5NzM5OTQ5NzdlLTEwCiAgIH0s
CiAgICJoc19yZWYiOiB7CiAgICAiaGkiOiBbCiAgICAgMjMwLjEzNjA0ODM5MDczMTMsCiAgICAg
MTc4LjI5NDM0MTc1NTc2NzY1CiAgICBdLAogICAgImxvIjogWwogICAgIDIyOS42OTU3NTQzMzU4
NjU3NiwKICAgICA4NC44MjQ1MDAwMDIzMTA5MQogICAgXQogICB9CiAgfSwKICAiaGV4X2dlbTh8
YiI6IHsKICAgInJfYWdnX0UyX1ZSSCI6IFsKICAgIDQuNDg0OTc3ODg2NTQzMDA3ZS0wNSwKICAg
IDEuMTIxNTQyMjQ4MzM5MDQ3ZS0wNSwKICAgIDEuNzk0Nzc2Mjc2MDQyODUzMmUtMDYsCiAgICA0
LjQ4NzIwNzQ4NTU4MTczNDVlLTA3LAogICAgNy4xNzk3OTE3NjExMjQ5MzJlLTA4LAogICAgMC4w
LAogICAgNy4xODAxNDI0ODA1Nzg0MTFlLTA4LAogICAgNC40ODc3NTU0ODI3ODQ5MDUzZS0wNywK
ICAgIDEuNzk1MjE0NjgxNTc2OTUxZS0wNiwKICAgIDEuMTIyMjI3MzQ2MzE3Mzk0OGUtMDUsCiAg
ICA0LjQ5MDQ2MTIwNjM4NTYzMmUtMDUsCiAgICAwLjAwMDE3OTc1NzM5NTk5MDc0MjgKICAgXSwK
ICAgInJfYWdnX2hfVlJIIjogWwogICAgLTEuOTI3MjY5NDI1ODI3NjZlLTA2LAogICAgLTQuODMx
NzAxMjQxMzI1NzAzZS0wNywKICAgIC03Ljc0NDExNDQwNTI5NDc2NmUtMDgsCiAgICAtMS45Mzcx
NjE3NDIxMjcxMDI2ZS0wOCwKICAgIC0zLjEwMDU1MzE0NzU2MTQxMzRlLTA5LAogICAgMC4wLAog
ICAgLTMuMTAyMDIwMTk2MjY2MTUzZS0wOSwKICAgIC0xLjkzOTQ1MzgxOTc2NTkwMTdlLTA4LAog
ICAgLTcuNzYyNDUxNDAzODgwOTg4ZS0wOCwKICAgIC00Ljg2MDM1NTU1OTEzMzExMmUtMDcsCiAg
ICAtMS45NTAyMDA4Nzc4OTgyMTE2ZS0wNiwKICAgIC03Ljg1MTk4MTUyNzk3MzE3M2UtMDYKICAg
XSwKICAgInJfYWdnX0UyX0hTIjogWwogICAgNC40Njc4ODA5Mzk2ODQ3NTRlLTA1LAogICAgMS4x
MTc2MjI5MzkxMDYzMzNlLTA1LAogICAgMS43ODg4MjUzMDUyMTU2MjQ0ZS0wNiwKICAgIDQuNDcy
NTg3OTQ0NDQ4NDkxN2UtMDcsCiAgICA3LjE1NjY0NDcyMTI4NDUyMmUtMDgsCiAgICAtMy4zMzA2
NjkwNzM4NzU0Njk2ZS0xNiwKICAgIDcuMTU3MzE3MTM4OTYxNjE2ZS0wOCwKICAgIDQuNDczNjM4
NTc5NTgyOTM5ZS0wNywKICAgIDEuNzg5NjY1ODE2NDMxODA2OWUtMDYsCiAgICAxLjExODkzNjI1
MDU2NTkxNjJlLTA1LAogICAgNC40NzgzODc3OTk4MjIyMzY2ZS0wNSwKICAgIDAuMDAwMTc5MzQ4
MjY3ODA1MTkwNTMKICAgXSwKICAgInJfYWdnX0UyX1YiOiBbCiAgICA1LjMwMzg4Njg4NjI4NzU3
OWUtMDUsCiAgICAxLjMyNTI1ODAxMDE1NDE1MTFlLTA1LAogICAgMi4xMTk3NTcxMTc2MTM0NzQ0
ZS0wNiwKICAgIDUuMjk4ODU4NjA1MjI5Mzg0ZS0wNywKICAgIDguNDc3NjY1NjM2MTY0MDMzZS0w
OCwKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICA4LjQ3Njk5MzU3Mzc1ODMwN2UtMDgs
CiAgICA1LjI5NzgwODUyMjk4NjAwM2UtMDcsCiAgICAyLjExODkxNzA0NTM3OTQ3NmUtMDYsCiAg
ICAxLjMyMzk0NTMyOTc2NzUzOTZlLTA1LAogICAgNS4yOTMzODM1MDYyNTUxODllLTA1LAogICAg
MC4wMDAyMTE1NjE1NDQ5NzM1OTMwMwogICBdLAogICAicl9hZ2dfRTJfUiI6IFsKICAgIDMuNTk1
MjQ1NTcyMzg1MzMwNWUtMDUsCiAgICA5LjAwMTM4OTU5ODE0MDAwOGUtMDYsCiAgICAxLjQ0MTUy
OTQ2MzU3NTAwODdlLTA2LAogICAgMy42MDQ5MjY2NTcxODU4MTRlLTA3LAogICAgNS43Njg5NDY4
MzEzNTI2NTA0ZS0wOCwKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICA1Ljc3MDM3MTg5
MTQyMjU5OWUtMDgsCiAgICAzLjYwNzE1MzM1MTU3MDI0N2UtMDcsCiAgICAxLjQ0MzMxMDgzNzUx
MjI1NzJlLTA2LAogICAgOS4wMjkyMjUyOTM2NjYzNDNlLTA2LAogICAgMy42MTc1MTkwNTU3MzE5
MzI2ZS0wNSwKICAgIDAuMDAwMTQ1MTg4NTQxMzA5OTU5NjIKICAgXSwKICAgImxhbWJkYV9tZWFu
X3Q0IjogWwogICAgOC41ODU0OTQ5NTY5NjkyNDhlLTA2LAogICAgMi4xNDk1MDQ0MTIwOTYxNjc3
ZS0wNiwKICAgIDMuNDQyMzY4MDY4NzQyMjc3ZS0wNywKICAgIDguNjA4NjE5NzcyNjg3MTVlLTA4
LAogICAgMS4zNzc2NDA4NTAwMDgwOTk5ZS0wOCwKICAgIDEuMjg0MjQ5MDc3NjI4MDk3NWUtMzEs
CiAgICAxLjM3Nzk5MjcxODE4NzE2NDdlLTA4LAogICAgOC42MTQxMTc3NDMzMTE5NDZlLTA4LAog
ICAgMy40NDY3NjY1MzA4Mjc4NTRlLTA3LAogICAgMi4xNTYzNzc5NDYzMjIzNTM3ZS0wNiwKICAg
IDguNjQwNTEwMDE5Nzc2NTM2ZS0wNiwKICAgIDMuNDY5MjMyODE4MTA5MzU3NGUtMDUKICAgXSwK
ICAgIlM0X0UyIjogLTIuNjY0NTQ0MTEyNjU2ODUxZS0xMywKICAgIlM0X2giOiA4LjI1Njc4MTQ4
MzQ4NDI5NmUtMTQsCiAgICJrYXBwYTQ0X0UyIjogMC4wMDAxNzk1MDE1MTM1NDkwNTg3NiwKICAg
ImthcHBhNDRfaCI6IC03Ljc1MzYzNTc0MzE0NDIwMWUtMDYsCiAgICJrYXBwYTQ0NF9FMiI6IDIu
MTkyMzU1OTU2NTM2NDMyOWUtMDcsCiAgICJrYXBwYTQ0X0UyX0hTIjogMC4wMDAxNzg5MjQ3MzAz
ODMzNDY1MywKICAgImhhbHZpbmdfZGV2X2thcHBhNDQiOiAxLjk4MzE3MDA2OTMyNjEzMjhlLTA5
LAogICAia2FwcGE0NF9FMl93aW5kb3cwcDEiOiAwLjAwMDE3OTQ5OTUzMDM3ODk4OTQ0LAogICAi
Zml0X3Jlc2lkdWFsIjogOS43Nzk5ODkyNTUxNjE3NzRlLTEyLAogICAiYmlyZWZfYjFfVlJIIjog
MC4wMTgxNzQyOTcxMDkzNDA4MTMsCiAgICJ2VF9WUkgiOiAxMC4wNDE1NTQwODUxNjA2MzIsCiAg
ICJ2VF9IU19sbyI6IDkuOTkwNzM5ODI5NzE5ODYsCiAgICJ2VF9IU19oaSI6IDEwLjA1MjYyOTk1
OTI5NDk0NSwKICAgInF1YWRmb3JtIjogewogICAgImthcHBhMjIiOiAtMC4wMDE4OTYxNDg4OTI5
OTM2NDk4LAogICAgImthcHBhMjQiOiAtMS44Mzc2MDc0OTkwNDk3Mzg4ZS0wOCwKICAgICJrYXBw
YTQ0IjogMC4wMDAxNzk0OTI2Mzk1MDM1MzA2MiwKICAgICJyZXNpZHVhbCI6IDUuMjM1ODc4MDc2
OTI2MTcyZS0xMAogICB9LAogICAiaHNfcmVmIjogewogICAgImhpIjogWwogICAgIDIzMC4xMzYw
NDgzOTA3MzEzLAogICAgIDE3OC4yOTQzNDE3NTU3Njc2NQogICAgXSwKICAgICJsbyI6IFsKICAg
ICAyMjkuNjk1NzU0MzM1ODY1NzYsCiAgICAgODQuODI0NTAwMDAyMzEwOTEKICAgIF0KICAgfQog
IH0sCiAgImN1YmljX3N0ZXB8MDAxIjogewogICAicl9hZ2dfRTJfVlJIIjogWwogICAgLTkuMzk1
Mzg5MjIzMjY1NjZlLTA1LAogICAgLTIuMzQzODI2MzI3NDMzMzUxNWUtMDUsCiAgICAtMy43NDU3
NzU0NTc4MDg1MmUtMDYsCiAgICAtOS4zNjEwMDg3MDQ4NTU2NzhlLTA3LAogICAgLTEuNDk3NDM5
NDEwMjQ3MzgxZS0wNywKICAgIDAuMCwKICAgIC0xLjQ5NzAxODU1MDIzMzg3NWUtMDcsCiAgICAt
OS4zNTQ0MzI1NTk2NzE3MjFlLTA3LAogICAgLTMuNzQwNTEzOTQ0MjUwMzQ1NGUtMDYsCiAgICAt
Mi4zMzU1OTg2NjE5NjIyMDE2ZS0wNSwKICAgIC05LjMyOTM4MDMxMDEzMDE5OGUtMDUsCiAgICAt
MC4wMDAzNzIzOTM3MzM1ODgzMjc2CiAgIF0sCiAgICJyX2FnZ19oX1ZSSCI6IFsKICAgIC05LjY4
ODQ2MDUwNzc1MDc0ZS0wNiwKICAgIC0yLjM5NzUwNTQ4NzU4MzU1MWUtMDYsCiAgICAtMy44MTQ0
MzY2MzMyMjA0NTI3ZS0wNywKICAgIC05LjUxODkzOTU0NzcwMzU1M2UtMDgsCiAgICAtMS41MjE0
MTQ4NjA3NjExODMzZS0wOCwKICAgIDIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIC0xLjUxOTI5
NjgzMjc4NTk1NDZlLTA4LAogICAgLTkuNDg1ODQ0MzIxMTQ0Mjk5ZS0wOCwKICAgIC0zLjc4Nzk1
Njg3MjYxNDAxOGUtMDcsCiAgICAtMi4zNTYwOTE2NzU1MzcxODYzZS0wNiwKICAgIC05LjM1NjAy
NjY3ODM5NzYzM2UtMDYsCiAgICAtMy42OTg0Mzc5OTE0MDYyMzRlLTA1CiAgIF0sCiAgICJyX2Fn
Z19FMl9IUyI6IFsKICAgIC05Ljc2MzQyMzE0NDY5MzAyOWUtMDUsCiAgICAtMi40MzY4MjY3NTEw
NzMyNjIyZS0wNSwKICAgIC0zLjg5NTExMDk1Njc3NTMwNWUtMDYsCiAgICAtOS43MzQ2MjM3MjQ4
ODg1MzZlLTA3LAogICAgLTEuNTU3MjM3OTE1MjgzOTQ4OGUtMDcsCiAgICAtMS4xMTAyMjMwMjQ2
MjUxNTY1ZS0xNiwKICAgIC0xLjU1NjgzNjQxMzExOTEwMDRlLTA3LAogICAgLTkuNzI4MzUwMjQ0
MjY0NjZlLTA3LAogICAgLTMuODkwMDkyMTA5NDM3NTgyZS0wNiwKICAgIC0yLjQyODk4NDE0MzQz
MjE3OGUtMDUsCiAgICAtOS43MDA2NjM0NTAzMTgyODFlLTA1LAogICAgLTAuMDAwMzg2ODM1OTEy
NjUyNjQ5OTQKICAgXSwKICAgInJfYWdnX0UyX1YiOiBbCiAgICAtOC42NTY5NzI3NDc4MzM2MTNl
LTA1LAogICAgLTIuMTY1Nzc5MjYzODE4NTU3ZS0wNSwKICAgIC0zLjQ2Njg0OTczODE3NjIzNjRl
LTA2LAogICAgLTguNjY4NTEzODY4OTM2ODU2ZS0wNywKICAgIC0xLjM4NzA5NzY4NjcxMTQxMzhl
LTA3LAogICAgLTIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgIC0xLjM4NzI4MDcyNDc0MDU5MTZl
LTA3LAogICAgLTguNjcxMzczODg2NzE1MDE3ZS0wNywKICAgIC0zLjQ2OTEzNzc5NzE0MDc1MzNl
LTA2LAogICAgLTIuMTY5MzU0ODU1ODQxMDIxNGUtMDUsCiAgICAtOC42ODU1OTE3ODE2MzE5NzRl
LTA1LAogICAgLTAuMDAwMzQ4MTYwODI5MjA5OTY0NwogICBdLAogICAicl9hZ2dfRTJfUiI6IFsK
ICAgIC0wLjAwMDEwMjY2MDg5NTUxMDY5Nzc5LAogICAgLTIuNTUzOTY5ODU5NTY0NDY0NGUtMDUs
CiAgICAtNC4wNzUwODIzMTMzNzA2MTVlLTA2LAogICAgLTEuMDE3ODYzMTc3NjMyNTI3NWUtMDYs
CiAgICAtMS42Mjc3MjIwMDcxODAzMWUtMDcsCiAgICAwLjAsCiAgICAtMS42MjY1OTA1MTQ1MDI5
NzllLTA3LAogICAgLTEuMDE2MDk1MTgyNjU5ODgxOWUtMDYsCiAgICAtNC4wNjA5MzczNTg3MTg1
OTdlLTA2LAogICAgLTIuNTMxODU3NDYzNTk0NjMzNGUtMDUsCiAgICAtMC4wMDAxMDA4ODg3ODI4
NDcwODYxMywKICAgIC0wLjAwMDQwMDg5ODExNDU1NTY4MTE0CiAgIF0sCiAgICJsYW1iZGFfbWVh
bl90NCI6IFsKICAgIDQuNjA5MTQ5Mjg4OTIzNTY3ZS0wNSwKICAgIDEuMTQ0MTk3MzY5NDU3NTMy
NGUtMDUsCiAgICAxLjgyMzgzMzM5MDY0Mjc5NjJlLTA2LAogICAgNC41NTQyMDQ4ODE4MTcwMjg3
ZS0wNywKICAgIDcuMjgxNjk5MjQ5NDY0OTVlLTA4LAogICAgNC4yNTgzOTIyOTEwNjk2OTRlLTMy
LAogICAgNy4yNzUxNTA2NTE5MDk3MjNlLTA4LAogICAgNC41NDM5NzIyMzMyNzEyNDI2ZS0wNywK
ICAgIDEuODE1NjQ1OTQzODgxNzAwOWUtMDYsCiAgICAxLjEzMTM4OTk0Njg5NzEyN2UtMDUsCiAg
ICA0LjUwNjI3MzExMDUyMjI5OGUtMDUsCiAgICAwLjAwMDE3OTE4MjQxOTc4MjY3MjkzCiAgIF0s
CiAgICJTNF9FMiI6IC0xLjk1NDk2Nzg5NDYyNjA1OThlLTExLAogICAiUzRfaCI6IC0xLjE2OTQ4
OTg2MTAzNzc1MThlLTExLAogICAia2FwcGE0NF9FMiI6IC0wLjAwMDM3NDM1Mjk0MTgxNzU2NzQs
CiAgICJrYXBwYTQ0X2giOiAtMy44MDI4MzI3NjczNDYwNDg0ZS0wNSwKICAgImthcHBhNDQ0X0Uy
IjogMi42MzMxNjQyMzE2MDk5NjNlLTA2LAogICAia2FwcGE0NF9FMl9IUyI6IC0wLjAwMDM4OTI2
NDc0NTM1NTEzMjU1LAogICAiaGFsdmluZ19kZXZfa2FwcGE0NCI6IDMuODgxNDEyNjg0Mzg0OTk1
NmUtMDgsCiAgICJrYXBwYTQ0X0UyX3dpbmRvdzBwMSI6IC0wLjAwMDM3NDMxNDEyNzY5MDcyMzU1
LAogICAiZml0X3Jlc2lkdWFsIjogMS45MTQxMTkwNjc2Mzg0MDU0ZS0xMCwKICAgImJpcmVmX2Ix
X1ZSSCI6IC0wLjAzNzg5ODcwMzM5NTk4NjU0LAogICAidlRfVlJIIjogNy43OTkwNDYzNzU4NDQ5
MjMsCiAgICJ2VF9IU19sbyI6IDcuNzU4NjE0NDkwMjExMDg3LAogICAidlRfSFNfaGkiOiA3Ljg2
Nzk1MzAwNTkwNDc3NSwKICAgInF1YWRmb3JtIjogewogICAgImthcHBhMjIiOiA0LjQ4MTkxMTA3
NjM2MTA5ZS0wOSwKICAgICJrYXBwYTI0IjogMS45NzQwNDMzNzQ5ODYwNzZlLTA3LAogICAgImth
cHBhNDQiOiAtMC4wMDAzNzQzNTQ1NTkzOTEwNjE2NiwKICAgICJyZXNpZHVhbCI6IDIuMTk5MDQx
NTQyMzkwOTE5ZS0wOQogICB9LAogICAiaHNfcmVmIjogewogICAgImhpIjogWwogICAgIDEyMy44
MzI0NjY2NjYwOTA2OCwKICAgICA4NS4yOTMzOTk5OTkxNDYxMgogICAgXSwKICAgICJsbyI6IFsK
ICAgICAxMjMuODMyNDY2NjY3MjQyNjYsCiAgICAgMzYuNzI1MjAwMDAwODYzNDcKICAgIF0KICAg
fQogIH0sCiAgImN1YmljX3N0ZXB8MTExIjogewogICAicl9hZ2dfRTJfVlJIIjogWwogICAgNi4y
NjM1OTI4MTU1MjUyNDNlLTA1LAogICAgMS41NjI1NTA4ODQ5NDgxNjYyZS0wNSwKICAgIDIuNDk3
MTgzNjM4NTM5MDEzNGUtMDYsCiAgICA2LjI0MDY3MjQ2OTkwMzc4NWUtMDcsCiAgICA5Ljk4Mjky
OTM5NDI0NzcxOWUtMDgsCiAgICAwLjAsCiAgICA5Ljk4MDEyMzY2MDgyNDM0N2UtMDgsCiAgICA2
LjIzNjI4ODM3NDU5NDc3OGUtMDcsCiAgICAyLjQ5MzY3NTk2MzI3NzY1M2UtMDYsCiAgICAxLjU1
NzA2NTc3NDYyNjY2NDdlLTA1LAogICAgNi4yMTk1ODY4NzM0MTI3M2UtMDUsCiAgICAwLjAwMDI0
ODI2MjQ4OTA1ODk1OTEKICAgXSwKICAgInJfYWdnX2hfVlJIIjogWwogICAgLTkuNjg4NDYwNTA3
NzUwNzRlLTA2LAogICAgLTIuMzk3NTA1NDg3NTgzNTUxZS0wNiwKICAgIC0zLjgxNDQzNjYzMzIy
MDQ1MjdlLTA3LAogICAgLTkuNTE4OTM5NTQ3NzAzNTUzZS0wOCwKICAgIC0xLjUyMTQxNDg2MDc2
MTE4MzNlLTA4LAogICAgMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgLTEuNTE5Mjk2ODMyNzg1
OTU0NmUtMDgsCiAgICAtOS40ODU4NDQzMjExNDQyOTllLTA4LAogICAgLTMuNzg3OTU2ODcyNjE0
MDE4ZS0wNywKICAgIC0yLjM1NjA5MTY3NTUzNzE4NjNlLTA2LAogICAgLTkuMzU2MDI2Njc4Mzk3
NjMzZS0wNiwKICAgIC0zLjY5ODQzNzk5MTQwNjIzNGUtMDUKICAgXSwKICAgInJfYWdnX0UyX0hT
IjogWwogICAgNi41MDg5NDg3NjMxMjg2ODZlLTA1LAogICAgMS42MjQ1NTExNjc0MTE3ODA3ZS0w
NSwKICAgIDIuNTk2NzQwNjM3NjI4MTU4OGUtMDYsCiAgICA2LjQ4OTc0OTE0OTE4NTU0MmUtMDcs
CiAgICAxLjAzODE1ODYxMDE4OTI5OTJlLTA3LAogICAgLTEuMTEwMjIzMDI0NjI1MTU2NWUtMTYs
CiAgICAxLjAzNzg5MDkzOTg1ODk1NDJlLTA3LAogICAgNi40ODU1NjY4MjU4MDkwM2UtMDcsCiAg
ICAyLjU5MzM5NDczOTYyNTA1NDVlLTA2LAogICAgMS42MTkzMjI3NjIyODA3MTdlLTA1LAogICAg
Ni40NjcxMDg5NjY4Nzg4NTRlLTA1LAogICAgMC4wMDAyNTc4OTA2MDg0MzUxNzQKICAgXSwKICAg
InJfYWdnX0UyX1YiOiBbCiAgICA1Ljc3MTMxNTE2NTIxNTAwNzRlLTA1LAogICAgMS40NDM4NTI4
NDI1MzA5MDE2ZS0wNSwKICAgIDIuMzExMjMzMTU4ODU4MTcyNWUtMDYsCiAgICA1Ljc3OTAwOTI0
NDQ3NzYwNmUtMDcsCiAgICA5LjI0NzMxNzg4OTIwNDk2NWUtMDgsCiAgICAtMi4yMjA0NDYwNDky
NTAzMTNlLTE2LAogICAgOS4yNDg1MzgxNTc1MzU3OWUtMDgsCiAgICA1Ljc4MDkxNTkyMzczNjUy
OWUtMDcsCiAgICAyLjMxMjc1ODUzMTU3NTE5ODZlLTA2LAogICAgMS40NDYyMzY1NzA1NjgwODI0
ZS0wNSwKICAgIDUuNzkwMzk0NTIxMDY1Nzc4ZS0wNSwKICAgIDAuMDAwMjMyMTA3MjE5NDczMDg3
NzcKICAgXSwKICAgInJfYWdnX0UyX1IiOiBbCiAgICA2Ljg0NDA1OTcwMDcwNTc4NWUtMDUsCiAg
ICAxLjcwMjY0NjU3MzA0Mjk3NjNlLTA1LAogICAgMi43MTY3MjE1NDIzOTUxMDYzZS0wNiwKICAg
IDYuNzg1NzU0NTE2MDY5ODg2ZS0wNywKICAgIDEuMDg1MTQ4MDA0Nzg2ODczM2UtMDcsCiAgICAw
LjAsCiAgICAxLjA4NDM5MzY3NzA3NTQ2ODFlLTA3LAogICAgNi43NzM5Njc4ODQzOTkyMTJlLTA3
LAogICAgMi43MDcyOTE1NzI0NzkwNjQ3ZS0wNiwKICAgIDEuNjg3OTA0OTc1NzIyMzU0ZS0wNSwK
ICAgIDYuNzI1OTE4ODU2NDY1MDA3ZS0wNSwKICAgIDAuMDAwMjY3MjY1NDA5NzAzNzg3NAogICBd
LAogICAibGFtYmRhX21lYW5fdDQiOiBbCiAgICA0LjYwOTE0OTI4ODkyMzU2N2UtMDUsCiAgICAx
LjE0NDE5NzM2OTQ1NzUzMjRlLTA1LAogICAgMS44MjM4MzMzOTA2NDI3OTYyZS0wNiwKICAgIDQu
NTU0MjA0ODgxODE3MDI4N2UtMDcsCiAgICA3LjI4MTY5OTI0OTQ2NDk1ZS0wOCwKICAgIDQuMjU4
MzkyMjkxMDY5Njk0ZS0zMiwKICAgIDcuMjc1MTUwNjUxOTA5NzIzZS0wOCwKICAgIDQuNTQzOTcy
MjMzMjcxMjQyNmUtMDcsCiAgICAxLjgxNTY0NTk0Mzg4MTcwMDllLTA2LAogICAgMS4xMzEzODk5
NDY4OTcxMjdlLTA1LAogICAgNC41MDYyNzMxMTA1MjIyOThlLTA1LAogICAgMC4wMDAxNzkxODI0
MTk3ODI2NzI5MwogICBdLAogICAiUzRfRTIiOiAxLjMwMzU0MTY0MDU4MzMzNDRlLTExLAogICAi
UzRfaCI6IC0xLjE2OTQ4OTg2MTAzNzc1MThlLTExLAogICAia2FwcGE0NF9FMiI6IDAuMDAwMjQ5
NTY4NjI3ODc3MjQxMTcsCiAgICJrYXBwYTQ0X2giOiAtMy44MDI4MzI3NjczNDYwNDg0ZS0wNSwK
ICAgImthcHBhNDQ0X0UyIjogLTEuNzU1NDQyODYwMDg3MDc2OWUtMDYsCiAgICJrYXBwYTQ0X0Uy
X0hTIjogMC4wMDAyNTk1MDk4MzAyMzgwNTgyNiwKICAgImhhbHZpbmdfZGV2X2thcHBhNDQiOiAy
LjU4NzYwNjEwOTc5NzQxZS0wOCwKICAgImthcHBhNDRfRTJfd2luZG93MHAxIjogMC4wMDAyNDk1
NDI3NTE4MTYxNDMyLAogICAiZml0X3Jlc2lkdWFsIjogMS4yNzYwNzgyMjMwNjY1OThlLTEwLAog
ICAiYmlyZWZfYjFfVlJIIjogLTAuMDM3ODk4NzAzMzk1OTg2NTQsCiAgICJ2VF9WUkgiOiA3Ljc5
OTA0NjM3NTg0NDkyMywKICAgInZUX0hTX2xvIjogNy43NTg2MTQ0OTAyMTEwODcsCiAgICJ2VF9I
U19oaSI6IDcuODY3OTUzMDA1OTA0Nzc1LAogICAicXVhZGZvcm0iOiB7CiAgICAia2FwcGEyMiI6
IC0yLjk4NzkzODgzMDI3MTk4ZS0wOSwKICAgICJrYXBwYTI0IjogMS45NzQwNDMzODcwNjUxNzI0
ZS0wNywKICAgICJrYXBwYTQ0IjogMC4wMDAyNDk1Njk3MDYyNTc0NTIwNCwKICAgICJyZXNpZHVh
bCI6IDIuMTg3MzAxNDA0OTE1MzQ4NGUtMDkKICAgfSwKICAgImhzX3JlZiI6IHsKICAgICJoaSI6
IFsKICAgICAxMjMuODMyNDY2NjY2MDkwNjgsCiAgICAgODUuMjkzMzk5OTk5MTQ2MTIKICAgIF0s
CiAgICAibG8iOiBbCiAgICAgMTIzLjgzMjQ2NjY2NzI0MjY2LAogICAgIDM2LjcyNTIwMDAwMDg2
MzQ3CiAgICBdCiAgIH0KICB9LAogICJjdWJpY19nZW04fDAwMSI6IHsKICAgInJfYWdnX0UyX1ZS
SCI6IFsKICAgIC0wLjAwMDExMjg1OTA0NDk4MTgxNjc2LAogICAgLTIuODEzOTIzNTI0NjAyNzQ2
ZS0wNSwKICAgIC00LjQ5NTg3Nzk0NzgxODgwNWUtMDYsCiAgICAtMS4xMjM0NzA1MTE1MTA0MDQ5
ZS0wNiwKICAgIC0xLjc5NzA4Njc4MTYwNzUwNDJlLTA3LAogICAgMC4wLAogICAgLTEuNzk2NDgw
NDIxMDkwMTUyZS0wNywKICAgIC0xLjEyMjUyMzAyNjUzMTA0MTVlLTA2LAogICAgLTQuNDg4Mjk2
NzY0MTM3OTc4ZS0wNiwKICAgIC0yLjgwMjA2MzYyNzA2MDkyNDVlLTA1LAogICAgLTAuMDAwMTEx
OTA2MTU0NTQ2MDM3NTgsCiAgICAtMC4wMDA0NDY2NjczMDY5OTM0OTc5CiAgIF0sCiAgICJyX2Fn
Z19oX1ZSSCI6IFsKICAgIC0xLjE1OTA4MTU2MTU2MzYzNTJlLTA1LAogICAgLTIuODYyOTkxMTUy
ODE4ODVlLTA2LAogICAgLTQuNTUwOTcxOTI3MDg2NDIyNGUtMDcsCiAgICAtMS4xMzUzOTgzMDQy
NjM5MDE1ZS0wNywKICAgIC0xLjgxNDQzODg5OTEyODEzNDZlLTA4LAogICAgMC4wLAogICAgLTEu
ODExNTY4Mzg0MTkxMjc1NWUtMDgsCiAgICAtMS4xMzA5MTI4MjMzODgyODU5ZS0wNywKICAgIC00
LjUxNTA4MDgwOTIzMDkwOWUtMDcsCiAgICAtMi44MDY4MzEzNTYzMzg5NjhlLTA2LAogICAgLTEu
MTEzOTI0MjM0NDMwNDYzNGUtMDUsCiAgICAtNC40MDI4OTcxMTc5MTY2Mzc2ZS0wNQogICBdLAog
ICAicl9hZ2dfRTJfSFMiOiBbCiAgICAtMC4wMDAxMTk2NjA4MTYzMjgxOTMxNCwKICAgIC0yLjk4
NTM4OTA3Mzc2MTg5MDRlLTA1LAogICAgLTQuNzcwODQ4MTExMzQ2MjA0ZS0wNiwKICAgIC0xLjE5
MjIzNTM1OTQzNzM1NDdlLTA2LAogICAgLTEuOTA3MTIwNjkzNTg5NDQ4ZS0wNywKICAgIDAuMCwK
ICAgIC0xLjkwNjUxNDgzMjY3MjQ1NjhlLTA3LAogICAgLTEuMTkxMjg4NzAzMjM5NDc5MmUtMDYs
CiAgICAtNC43NjMyNzQ3MTE0MzkwMDNlLTA2LAogICAgLTIuOTczNTUzOTc0NjcyMjQ5NWUtMDUs
CiAgICAtMC4wMDAxMTg3MTM1MzMxOTg0Nzc4OCwKICAgIC0wLjAwMDQ3MzA4NTQ0NTQyNzkwMQog
ICBdLAogICAicl9hZ2dfRTJfViI6IFsKICAgIC0wLjAwMDEwMjU5NzQyMDk1MjUzMjY2LAogICAg
LTIuNTY2OTk1MDg2MjYxNjgwOGUtMDUsCiAgICAtNC4xMDkzODAyNDUwODc1NTdlLTA2LAogICAg
LTEuMDI3NTM2MjUwNDE5NzM2ZS0wNiwKICAgIC0xLjY0NDI0NDk1MzUyNDc3NmUtMDcsCiAgICAt
Mi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgLTEuNjQ0NDk4MjA2NDk4OTIzM2UtMDcsCiAgICAt
MS4wMjc5MzE5NjE3NzIzMTA0ZS0wNiwKICAgIC00LjExMjU0NjAyNTA1OTA2MWUtMDYsCiAgICAt
Mi41NzE5NDI1Nzg5NjYwOTFlLTA1LAogICAgLTAuMDAwMTAyOTkzNDk1NTA3OTA4MTUsCiAgICAt
MC4wMDA0MTMwMzgzNzc1MTgxNjAxCiAgIF0sCiAgICJyX2FnZ19FMl9SIjogWwogICAgLTAuMDAw
MTI2MDI2NDM2MDI3OTkyOCwKICAgIC0zLjEzMTIxODgzODA1OTQ0NjNlLTA1LAogICAgLTQuOTky
NzMzNjkxNTg4OTI0ZS0wNiwKICAgIC0xLjI0NjgwNzE2NTE3ODMzMmUtMDYsCiAgICAtMS45OTM1
OTIzNTM0MjIwMDI0ZS0wNywKICAgIC0yLjIyMDQ0NjA0OTI1MDMxM2UtMTYsCiAgICAtMS45OTE4
ODU3NzI5ODk0NzY4ZS0wNywKICAgIC0xLjI0NDE0MDU1ODEzMjA0NTNlLTA2LAogICAgLTQuOTcx
Mzk4NTkxNzkwOTY1ZS0wNiwKICAgIC0zLjA5Nzg1ODE1ODE5NjQwOWUtMDUsCiAgICAtMC4wMDAx
MjMzNTA1MzgzNDc4ODgzNCwKICAgIC0wLjAwMDQ4OTY2MDkxNTAzOTg4MDEKICAgXSwKICAgImxh
bWJkYV9tZWFuX3Q0IjogWwogICAgNC45MDQwMzI5MDc3NjM3MmUtMDUsCiAgICAxLjIxNTM2OTk5
NTkzNjI4NGUtMDUsCiAgICAxLjkzNTc0OTczNzQ1OTU1ZS0wNiwKICAgIDQuODMyNTU0NTUzMTkx
NzM5ZS0wNywKICAgIDcuNzI1NzQ3MDM5NzU5OTQ0ZS0wOCwKICAgIDEuNDkwNzAzMzc2MTAxNDY1
ZS0zMCwKICAgIDcuNzE3NTMyMzA1MTczNjI4ZS0wOCwKICAgIDQuODE5NzE4MTY0NDMyMzQxZS0w
NywKICAgIDEuOTI1NDc4MTUxNzI3NDc0M2UtMDYsCiAgICAxLjE5OTI5MzU0MDkwMDEyNzdlLTA1
LAogICAgNC43NzQ2NDI4ODgwMzI1Nzg1ZS0wNSwKICAgIDAuMDAwMTg5ODk3MDk1OTMzMTI5ODYK
ICAgXSwKICAgIlM0X0UyIjogLTQuMjY3MTY4MjI5MDIxODk2ZS0xMSwKICAgIlM0X2giOiAtMi4z
ODUyODE3MzQ3ODk4MDllLTExLAogICAia2FwcGE0NF9FMiI6IC0wLjAwMDQ0OTI3NzA5MzQyOTYx
NjksCiAgICJrYXBwYTQ0X2giOiAtNC41MzU3ODIyNjYyNDg5MTNlLTA1LAogICAia2FwcGE0NDRf
RTIiOiAzLjc5NTg0NjY1NTYyNjAyNzdlLTA2LAogICAia2FwcGE0NF9FMl9IUyI6IC0wLjAwMDQ3
NjcxNTE5NTA0MjMwNzQsCiAgICJoYWx2aW5nX2Rldl9rYXBwYTQ0IjogNi44OTY2MTI1ODg5MDc0
OTRlLTA4LAogICAia2FwcGE0NF9FMl93aW5kb3cwcDEiOiAtMC4wMDA0NDkyMDgxMjczMDM3Mjc4
LAogICAiZml0X3Jlc2lkdWFsIjogMy40MDEwNjgzOTM2Njg0MzM1ZS0xMCwKICAgImJpcmVmX2Ix
X1ZSSCI6IC0wLjA0NTQ4MTI1MjIyNzc0OTI0LAogICAidlRfVlJIIjogOS4zMDc4OTkwNzY1MzMx
NzksCiAgICJ2VF9IU19sbyI6IDkuMjExNzIxMDY0MzcwODYxLAogICAidlRfSFNfaGkiOiA5LjQ1
Njg1NDk4NDU4ODczOCwKICAgInF1YWRmb3JtIjogewogICAgImthcHBhMjIiOiA3Ljk2Mzc1Nzkz
MzM2Nzc5OWUtMDksCiAgICAia2FwcGEyNCI6IDMuNDc3ODU3MjQ2MjgxNDQxNGUtMDcsCiAgICAi
a2FwcGE0NCI6IC0wLjAwMDQ0OTI3OTk2NzYwNDIyNjg1LAogICAgInJlc2lkdWFsIjogMy44NzU0
NTE5NjEwOTk0NTk1ZS0wOQogICB9LAogICAiaHNfcmVmIjogewogICAgImhpIjogWwogICAgIDIx
MC4yNzU0OTk5OTkwOTMxLAogICAgIDEzMS41NDM1OTk5OTg2NDQxNAogICAgXSwKICAgICJsbyI6
IFsKICAgICAyMTAuMjc1NTAwMDAwOTA2OTMsCiAgICAgNDYuMzQ5ODUwMDAxMzU5MTQKICAgIF0K
ICAgfQogIH0sCiAgImN1YmljX2dlbTh8MTExIjogewogICAicl9hZ2dfRTJfVlJIIjogWwogICAg
Ny41MjM5MzYzMzIwOTg5MTNlLTA1LAogICAgMS44NzU5NDkwMTYzOTQ0MjkyZS0wNSwKICAgIDIu
OTk3MjUxOTY1MDY0NTA3ZS0wNiwKICAgIDcuNDg5ODAzNDA4NTg5MDY5ZS0wNywKICAgIDEuMTk4
MDU3ODU1MTQ1MTUxNWUtMDcsCiAgICAwLjAsCiAgICAxLjE5NzY1MzYxMTgzOTY1NTJlLTA3LAog
ICAgNy40ODM0ODY4NDM1NDAyNzdlLTA3LAogICAgMi45OTIxOTc4NDI2MTA2MjJlLTA2LAogICAg
MS44NjgwNDI0MTgwODUwMjUyZS0wNSwKICAgIDcuNDYwNDEwMzAzMDYxNzcxZS0wNSwKICAgIDAu
MDAwMjk3Nzc4MjA0NjYyMjU3OQogICBdLAogICAicl9hZ2dfaF9WUkgiOiBbCiAgICAtMS4xNTkw
ODE1NjE1NjM2MzUyZS0wNSwKICAgIC0yLjg2Mjk5MTE1MjgxODg1ZS0wNiwKICAgIC00LjU1MDk3
MTkyNzA4NjQyMjRlLTA3LAogICAgLTEuMTM1Mzk4MzA0MjYzOTAxNWUtMDcsCiAgICAtMS44MTQ0
Mzg4OTkxMjgxMzQ2ZS0wOCwKICAgIDAuMCwKICAgIC0xLjgxMTU2ODM4NDE5MTI3NTVlLTA4LAog
ICAgLTEuMTMwOTEyODIzMzg4Mjg1OWUtMDcsCiAgICAtNC41MTUwODA4MDkyMzA5MDllLTA3LAog
ICAgLTIuODA2ODMxMzU2MzM4OTY4ZS0wNiwKICAgIC0xLjExMzkyNDIzNDQzMDQ2MzRlLTA1LAog
ICAgLTQuNDAyODk3MTE3OTE2NjM3NmUtMDUKICAgXSwKICAgInJfYWdnX0UyX0hTIjogWwogICAg
Ny45NzczODc3NTUyMjAyNzhlLTA1LAogICAgMS45OTAyNTkzODI1MDA1MjU1ZS0wNSwKICAgIDMu
MTgwNTY1NDA3NzEyMTY2ZS0wNiwKICAgIDcuOTQ4MjM1NzI1MTQxNDczZS0wNywKICAgIDEuMjcx
NDEzNzg5ODA1MTA5MmUtMDcsCiAgICAwLjAsCiAgICAxLjI3MTAwOTg4ODQ0ODMwNDVlLTA3LAog
ICAgNy45NDE5MjQ2ODkwMDMzNDNlLTA3LAogICAgMy4xNzU1MTY0NzQ0NDA2OTgzZS0wNiwKICAg
IDEuOTgyMzY5MzE2NDExMTU5ZS0wNSwKICAgIDcuOTE0MjM1NTQ2NjAyMmUtMDUsCiAgICAwLjAw
MDMxNTM5MDI5Njk1MjE1NjA0CiAgIF0sCiAgICJyX2FnZ19FMl9WIjogWwogICAgNi44Mzk4Mjgw
NjM1MDk1NzllLTA1LAogICAgMS43MTEzMzAwNTc1NTIxOTZlLTA1LAogICAgMi43Mzk1ODY4MzAw
NTgzNzE0ZS0wNiwKICAgIDYuODUwMjQxNjY5NDY0OTA3ZS0wNywKICAgIDEuMDk2MTYzMzAwMTI5
NDA0N2UtMDcsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgMS4wOTYzMzIxMzM5NjUy
MDU1ZS0wNywKICAgIDYuODUyODc5NzQ1ODg4ODg1ZS0wNywKICAgIDIuNzQxNjk3MzUwMDM5Mzcz
OGUtMDYsCiAgICAxLjcxNDYyODM4NTk2MjU5MWUtMDUsCiAgICA2Ljg2NjIzMzAzMzgzMDkzN2Ut
MDUsCiAgICAwLjAwMDI3NTM1ODkxODM0NTI5MgogICBdLAogICAicl9hZ2dfRTJfUiI6IFsKICAg
IDguNDAxNzYyNDAxODY2MTg2ZS0wNSwKICAgIDIuMDg3NDc5MjI1Mzg3NzY3MmUtMDUsCiAgICAz
LjMyODQ4OTEyNzY1MTkzNDZlLTA2LAogICAgOC4zMTIwNDc3NjU2MzUxZS0wNywKICAgIDEuMzI5
MDYxNTY3NDY3NzA0MmUtMDcsCiAgICAtMi4yMjA0NDYwNDkyNTAzMTNlLTE2LAogICAgMS4zMjc5
MjM4NDY0MzkyMDUxZS0wNywKICAgIDguMjk0MjcwMzg4Mjg3MTE3ZS0wNywKICAgIDMuMzE0MjY1
NzI4MDgyNjg4ZS0wNiwKICAgIDIuMDY1MjM4NzcyMTUzMTQ0ZS0wNSwKICAgIDguMjIzMzY5MjIz
MTcwMzUxZS0wNSwKICAgIDAuMDAwMzI2NDQwNjEwMDI2NzM0NzUKICAgXSwKICAgImxhbWJkYV9t
ZWFuX3Q0IjogWwogICAgNC45MDQwMzI5MDc3NjM3MmUtMDUsCiAgICAxLjIxNTM2OTk5NTkzNjI4
NGUtMDUsCiAgICAxLjkzNTc0OTczNzQ1OTU1ZS0wNiwKICAgIDQuODMyNTU0NTUzMTkxNzM5ZS0w
NywKICAgIDcuNzI1NzQ3MDM5NzU5OTQ0ZS0wOCwKICAgIDEuNDkwNzAzMzc2MTAxNDY1ZS0zMCwK
ICAgIDcuNzE3NTMyMzA1MTczNjI4ZS0wOCwKICAgIDQuODE5NzE4MTY0NDMyMzQxZS0wNywKICAg
IDEuOTI1NDc4MTUxNzI3NDc0M2UtMDYsCiAgICAxLjE5OTI5MzU0MDkwMDEyNzdlLTA1LAogICAg
NC43NzQ2NDI4ODgwMzI1Nzg1ZS0wNSwKICAgIDAuMDAwMTg5ODk3MDk1OTMzMTI5ODYKICAgXSwK
ICAgIlM0X0UyIjogMi44NDQ3Njk3NjQwMTc5ODc2ZS0xMSwKICAgIlM0X2giOiAtMi4zODUyODE3
MzQ3ODk4MDllLTExLAogICAia2FwcGE0NF9FMiI6IDAuMDAwMjk5NTE4MDYyMjg4ODcwODcsCiAg
ICJrYXBwYTQ0X2giOiAtNC41MzU3ODIyNjYyNDg5MTNlLTA1LAogICAia2FwcGE0NDRfRTIiOiAt
Mi41MzA1NjQ0MTkwNTgzMjZlLTA2LAogICAia2FwcGE0NF9FMl9IUyI6IDAuMDAwMzE3ODEwMTMw
MDI0OTcwNjMsCiAgICJoYWx2aW5nX2Rldl9rYXBwYTQ0IjogNC41OTc3NDM1NjQ3Mjg5NTFlLTA4
LAogICAia2FwcGE0NF9FMl93aW5kb3cwcDEiOiAwLjAwMDI5OTQ3MjA4NDg1MzIyMzYsCiAgICJm
aXRfcmVzaWR1YWwiOiAyLjI2NzM3OTg0MjczMTUyMzJlLTEwLAogICAiYmlyZWZfYjFfVlJIIjog
LTAuMDQ1NDgxMjUyMjI3NzQ5MjQsCiAgICJ2VF9WUkgiOiA5LjMwNzg5OTA3NjUzMzE3OSwKICAg
InZUX0hTX2xvIjogOS4yMTE3MjEwNjQzNzA4NjEsCiAgICJ2VF9IU19oaSI6IDkuNDU2ODU0OTg0
NTg4NzM4LAogICAicXVhZGZvcm0iOiB7CiAgICAia2FwcGEyMiI6IC01LjMwOTE3MzgzNjQ1MzA3
MzRlLTA5LAogICAgImthcHBhMjQiOiAzLjQ3Nzg1NzIzODQ2NTQyOGUtMDcsCiAgICAia2FwcGE0
NCI6IDAuMDAwMjk5NTE5OTc4NDAzODEyOSwKICAgICJyZXNpZHVhbCI6IDMuODU0NDE3Nzg3MTQ1
NDc5NGUtMDkKICAgfSwKICAgImhzX3JlZiI6IHsKICAgICJoaSI6IFsKICAgICAyMTAuMjc1NDk5
OTk5MDkzMSwKICAgICAxMzEuNTQzNTk5OTk4NjQ0MTQKICAgIF0sCiAgICAibG8iOiBbCiAgICAg
MjEwLjI3NTUwMDAwMDkwNjkzLAogICAgIDQ2LjM0OTg1MDAwMTM1OTE0CiAgICBdCiAgIH0KICB9
CiB9LAogInBoYXNlMyI6IHsKICAidmVyZGljdF9jbGFzcyI6ICJJREVOVElUWS1ERUxJVkVSRUQt
TDQiLAogICJGLU1TMi0zIjogIlNJTEVOVCIsCiAgIkYtTVMyLTQiOiAiU0lMRU5UIiwKICAiRi1N
UzItMiI6ICJSRUdJU1RFUkVEX05PVF9FWEVDVVRFRCIsCiAgIndvcnN0X1M0IjogNC4yNjcxNjgy
MjkwMjE4OTZlLTExCiB9LAogIlQxX3Bvc3Rfd3JpdGUiOiB7CiAgImxpc3RfbWQ1IjogImJlOTIx
YjhjMjlmNzU3OGU4NWVkOTJmMTQ1MGMxOTU2IiwKICAic2Nhbm5lcl9tZDUiOiAiNmI4NjI5MDA5
MGE4Yzg0ZjFiMWEwYTk5ZWMwYmY2OTciLAogICJjaGVja3BvaW50IjogIkNMRUFOIgogfQp9
=====END-EMBED name=g_mscs2_chatleg_checkpoint.json=====

=====BEGIN-EMBED name=g_mscs2_chatleg_phase0_checkpoint.json md5=9e5a6e8ba0804bda778e4be52fbe2fde bytes=7747 encoding=base64 armor_bytes=10468 QUARANTINED=====
ewogImdhdGUiOiAiRy1NU0NTMiIsCiAibGVnIjogImNoYXQiLAogImluc3RydW1lbnQiOiAiZ19t
c2NzMl9jaGF0bGVnLnB5IiwKICJpbnN0cnVtZW50X21kNSI6ICJmMjc3NTgwZGRmMGI0ZGE5NzM0
ZDExZWRiMDA5YzU0YiIsCiAibWVtb19sb2NrX21kNSI6ICJlZmRjYWJkY2Q5MzdjZGE0YWNiNjRm
OTQxZGM0YmIyYiIsCiAibWVtb19sb2NrX2J5dGVzIjogNDYwNTMsCiAibGVkZ2VyX2Jhc2VfbWQ1
IjogImYzNmJiZGIwNDEwNDAwODc4M2YyNzYzZjcwZmI5MTZmIiwKICJ0MV9saXN0X21kNSI6ICJi
ZTkyMWI4YzI5Zjc1NzhlODVlZDkyZjE0NTBjMTk1NiIsCiAieDFfbWQ1IjogIjIwMGU3YThiNzc1
NTc3NTY0MzY5YzY5MjRkMzhhODRjIiwKICJ4Nl9jaGF0X21kNSI6ICJjMDRjMGI4ZWEzNGNmZTYw
ZjIzMWFhMDY4MjhlNmNlNCIsCiAieDZfY2NfbWQ1IjogIjI0OWUxMWRkNTNjNGNiODJmMzAyYjE1
ZDNjOTRjMzM3IiwKICJ1dGMiOiAiMjAyNi0wOS0yNlQxNDozMzozNi40MjUzOTArMDA6MDAiLAog
ImVsZWN0aW9ucyI6IHsKICAiRS1NUzItMSI6ICJhK2IiLAogICJFLU1TMi0yIjogImEiLAogICJF
LU1TMi0yYiI6ICJhK2IiLAogICJFLU1TMi0yYyI6ICIwMDErMTExIiwKICAiRS1NUzItMyI6ICJh
IiwKICAiRS1NUzItNCI6ICJhIiwKICAiRS1NUzItNSI6ICJhIiwKICAiRS1NUzItNiI6ICJhIiwK
ICAiRS1NUzItNyI6ICIwNTMwMjIxMCtNU0NTMXN0cmF0dW0iLAogICJFLU1TMi04IjogImEiCiB9
LAogInQxX3NjYW4iOiB7CiAgImluc3RydW1lbnQiOiAiQ0xFQU4iLAogICJtZW1vIjogIkNMRUFO
IgogfSwKICJxdWFkcmF0dXJlIjogewogICJuX3RoZXRhIjogNjQsCiAgIm5fcGhpIjogMTI4LAog
ICJzbzNfZ3JpZCI6IFsKICAgMTYsCiAgIDEwLAogICAxNgogIF0sCiAgIm5fZ3JpZCI6IFsKICAg
MTIsCiAgIDI0CiAgXQogfSwKICJ0NF9ncmlkIjogWwogIC0wLjUsCiAgLTAuMjUsCiAgLTAuMSwK
ICAtMC4wNSwKICAtMC4wMiwKICAwLjAsCiAgMC4wMiwKICAwLjA1LAogIDAuMSwKICAwLjI1LAog
IDAuNSwKICAxLjAKIF0sCiAidDJ0NF9ncmlkIjogWwogIC0wLjI1LAogIC0wLjEyNSwKICAwLjAs
CiAgMC4xMjUsCiAgMC4yNQogXSwKICJwaGFzZTAiOiB7CiAgIlBJTi1YVEFMIjogewogICAid29y
c3RfcmVsIjogMC4wLAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIlBJTi1WUkgwIjogewogICAi
d29yc3RfcmVsIjogMC4wLAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIlBJTi1IUzAiOiB7CiAg
ICJ3b3JzdF9yZWwiOiAwLjAsCiAgICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiUElOLUsyIjogewog
ICAid29yc3RfcmVsX2hleF9rYXBwYTIiOiAxLjM5Mjk2NzUyNDU4NTkyOTVlLTEyLAogICAid29y
c3RfYWJzX2N1YmljX2thcHBhMiI6IDIuMTU1MzM3Njk2NjQ3NjAzNWUtMTUsCiAgICJrYXBwYTJf
RTJfcmVjb21wdXRlZCI6IHsKICAgICJoZXhfc3RlcHxhIjogLTAuMDAxNDM5NDYxNzY5NDk4NzA0
MywKICAgICJoZXhfc3RlcHxiIjogLTAuMDAxNDM4NzAyNzE4NzQ5OTQ3NiwKICAgICJoZXhfZ2Vt
OHxhIjogLTAuMDAxODk1NjQ4NDgyNjcwMTM1MiwKICAgICJoZXhfZ2VtOHxiIjogLTAuMDAxODk2
MTM3NDY2NTI0MzY0NSwKICAgICJjdWJpY19zdGVwfDAwMSI6IC00LjU1MTM4NzA0ODc2MTYyNmUt
MTYsCiAgICAiY3ViaWNfc3RlcHwxMTEiOiAtMS42NzM5MTQzODU3MTQ3NjUyZS0xNiwKICAgICJj
dWJpY19nZW04fDAwMSI6IC0yLjE1NTMzNzY5NjY0NzYwMzVlLTE1LAogICAgImN1YmljX2dlbTh8
MTExIjogLTEuNjAxOTc3NTY5MTM4NTg4OGUtMTUKICAgfSwKICAgInBhc3NlZCI6IHRydWUKICB9
LAogICJGLUNUUkwtSVNPIjogewogICAid29yc3RfYWJzIjogNC40NDA4OTIwOTg1MDA2MjZlLTE2
LAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIkYtQ1RSTC1TTzMiOiB7CiAgICJkZXZfZnJvbV8w
cDQiOiA0Ljk5NjAwMzYxMDgxMzIwNGUtMTYsCiAgICJyX2FnZ18wX2FicyI6IDAuMCwKICAgInBh
c3NlZCI6IHRydWUKICB9LAogICJGLUNUUkwtUE9TIjogewogICAibWluX29kZl93ZWlnaHQiOiAw
LjM5NTAyNzA2MTc4NTUxNDk0LAogICAicGFzc2VkIjogdHJ1ZQogIH0sCiAgIkYtQ1RSTC1MMk5V
TEwiOiB7CiAgICJ3b3JzdF9hYnMiOiA1Ljg0OTkwODkzMzY3NjE3MWUtMTQsCiAgICJwYXNzZWQi
OiB0cnVlCiAgfSwKICAiRi1DVFJMLUw0RVhIQVVTVCI6IHsKICAgIndvcnN0X3JlbF90ZW5zb3Ii
OiA0LjMyNTc3Mjg3ODk1NDU4OGUtMTQsCiAgICJ3b3JzdF9hYnNfcl9hZ2ciOiA0LjQ0MDg5MjA5
ODUwMDYyNmUtMTYsCiAgICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiRi1DVFJMLUM0IjogewogICAi
d29yc3RfcmVsX2Nsb3NlZF9mb3JtIjogMi41MTg2OTI2NTUwMDk5NjA1ZS0xNCwKICAgIndvcnN0
X3JlbF9hZmZpbmUiOiA0LjA3NDA0MzcyMTY2NzMzMzRlLTE0LAogICAiaDBfZWZmZWN0X3JlbCI6
IDIuMzAyMTU4NDYzODYyNzI0OGUtMTQsCiAgICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiRi1DVFJM
LU1BUkciOiB7CiAgICJ3b3JzdF9hYnMiOiA4LjMyNjY3MjY4NDY4ODY3NGUtMTYsCiAgICJwYXNz
ZWQiOiB0cnVlCiAgfSwKICAiRi1DVFJMLVRFWDQiOiB7CiAgICJyX2FnZ190MV9hYnMiOiAwLjAw
MDQxMTgzMjY1NTc3MzM4MDksCiAgICJwYXNzZWQiOiB0cnVlCiAgfSwKICAiRi1DVFJMLVFVQUQi
OiB7CiAgICJkb3VibGluZ19yZXNpZHVhbCI6IDIuMjYwMzQyODg2MDcwNDMxNWUtMTQsCiAgICJr
X3NwaGVyZV9kb3VibGluZyI6IDIuMjIwNDQ2MDQ5MjUwMzEzZS0xNiwKICAgInNvM19kb3VibGlu
ZyI6IDIuMjYwMzQyODg2MDcwNDMxNWUtMTQsCiAgICJwYXNzZWQiOiB0cnVlCiAgfQogfSwKICJw
aGFzZTBfd2l0bmVzcyI6IHsKICAic2luZ2xlX2NyeXN0YWwiOiB7CiAgICJoZXhfc3RlcHxhIjog
ewogICAgInZfRU0iOiA4LjQ5ODkyNjYzMDU4OTE0MywKICAgICJ2X1MyRTIiOiA4LjI2MTIzNTM5
MTEyNzExNCwKICAgICJ2X1MyaCI6IDguNDg5NDY4MzU4Mjg5MTA5LAogICAgInJfeHRhbF9FMiI6
IC0wLjAyNzk2NzIwNjg5NDg3MjUzLAogICAgInJfeHRhbF9oIjogLTAuMDAxMTEyODc4NDUwNTU1
Mjk5LAogICAgImxhbWJkYV9tZWFuIjogMC4wMDQ4MDg1NzU3MjQwMjI4MzgsCiAgICAibGFtYmRh
X21heCI6IDAuMDMzNTM3NTgyOTk3NzQ2MTIsCiAgICAibGFtYmRhX21heF9icmFuY2giOiAicVNW
IgogICB9LAogICAiaGV4X3N0ZXB8YiI6IHsKICAgICJ2X0VNIjogOC40OTkxMzgwNTk3NjQ3MiwK
ICAgICJ2X1MyRTIiOiA4LjI2MTYxMTU1MTMyODI4OCwKICAgICJ2X1MyaCI6IDguNDg5NjgwMjEw
NTkxNDY4LAogICAgInJfeHRhbF9FMiI6IC0wLjAyNzk0NzEyOTA4MTM0Njc3OCwKICAgICJyX3h0
YWxfaCI6IC0wLjAwMTExMjgwMDk4MTMxNjYwODQsCiAgICAibGFtYmRhX21lYW4iOiAwLjAwNDgw
ODYwMDQyODM0ODUxNCwKICAgICJsYW1iZGFfbWF4IjogMC4wMzM1MzQ1NDc2ODUyMDg4MjUsCiAg
ICAibGFtYmRhX21heF9icmFuY2giOiAicVNWIgogICB9LAogICAiaGV4X2dlbTh8YSI6IHsKICAg
ICJ2X0VNIjogMTAuMTY3NTcxMTQ3NDI3Nzc5LAogICAgInZfUzJFMiI6IDkuNzY3NTg0NjE1Njc5
NjM4LAogICAgInZfUzJoIjogMTAuMTU0MjAyMTYxNTY4MjAyLAogICAgInJfeHRhbF9FMiI6IC0w
LjAzOTMzOTQzNzcwMzMwMzUwNCwKICAgICJyX3h0YWxfaCI6IC0wLjAwMTMxNDg2NTIzODI4ODM4
NzQsCiAgICAibGFtYmRhX21lYW4iOiAwLjAwNDk1Mzc2OTYxODA2Mzk1MzUsCiAgICAibGFtYmRh
X21heCI6IDAuMDM1MTMzMDE4NDU5MDM3NDQsCiAgICAibGFtYmRhX21heF9icmFuY2giOiAicVNW
IgogICB9LAogICAiaGV4X2dlbTh8YiI6IHsKICAgICJ2X0VNIjogMTAuMTY3NDEyMzg4OTY1MzQy
LAogICAgInZfUzJFMiI6IDkuNzY3MzAwODE5MDk2NjU2LAogICAgInZfUzJoIjogMTAuMTU0MDQy
OTc3OTgwNTc3LAogICAgInJfeHRhbF9FMiI6IC0wLjAzOTM1MjM0OTg5NjExNzY5LAogICAgInJf
eHRhbF9oIjogLTAuMDAxMzE0OTI3NTgxNjk5NTk4NywKICAgICJsYW1iZGFfbWVhbiI6IDAuMDA0
OTUzNzg5OTMyMzI5NDIyLAogICAgImxhbWJkYV9tYXgiOiAwLjAzNTEzMzAxODQ1OTAzNzUyNSwK
ICAgICJsYW1iZGFfbWF4X2JyYW5jaCI6ICJxU1YiCiAgIH0sCiAgICJjdWJpY19zdGVwfDAwMSI6
IHsKICAgICJ2X0VNIjogOC4wMjgxMjQ4Mjc0OTQ4ODksCiAgICAidl9TMkUyIjogNy44ODkyNjQy
MTY5NTYyMjIsCiAgICAidl9TMmgiOiA4LjAxNTk1MTE2MjgzMTg3MiwKICAgICJyX3h0YWxfRTIi
OiAtMC4wMTcyOTY3Njc3NDEyMTU4LAogICAgInJfeHRhbF9oIjogLTAuMDAxNTE2Mzc3MTAyMzI0
NTUxLAogICAgImxhbWJkYV9tZWFuIjogMC4wMDgzOTIzMTkwMjg4NzgzLAogICAgImxhbWJkYV9t
YXgiOiAwLjAzODcwMDY5MzM0MTczNzQxLAogICAgImxhbWJkYV9tYXhfYnJhbmNoIjogInFUMiIK
ICAgfSwKICAgImN1YmljX3N0ZXB8MTExIjogewogICAgInZfRU0iOiA4LjAyODEyNDgyNzQ5NDg4
OSwKICAgICJ2X1MyRTIiOiA4LjEyMDY5ODU2Nzg1NDAwMSwKICAgICJ2X1MyaCI6IDguMDE1OTUx
MTYyODMxODcyLAogICAgInJfeHRhbF9FMiI6IDAuMDExNTMxMTc4NDk0MTQ0MDksCiAgICAicl94
dGFsX2giOiAtMC4wMDE1MTYzNzcxMDIzMjQ1NTEsCiAgICAibGFtYmRhX21lYW4iOiAwLjAwODM5
MjMxOTAyODg3ODMsCiAgICAibGFtYmRhX21heCI6IDAuMDM4NzAwNjkzMzQxNzM3NDEsCiAgICAi
bGFtYmRhX21heF9icmFuY2giOiAicVQyIgogICB9LAogICAiY3ViaWNfZ2VtOHwwMDEiOiB7CiAg
ICAidl9FTSI6IDkuNzIxMTcxMDE1MDc4MjEsCiAgICAidl9TMkUyIjogOS41MTg1NTgwNzE4MDMz
LAogICAgInZfUzJoIjogOS43MDMyMzQ0NzI1MjgyNTEsCiAgICAicl94dGFsX0UyIjogLTAuMDIw
ODQyNDQyMDIyNzQwMzI2LAogICAgInJfeHRhbF9oIjogLTAuMDAxODQ1MTAxMDE5NDI4NDc0NSwK
ICAgICJsYW1iZGFfbWVhbiI6IDAuMDA5MzEwNTAzODU5NjUyOCwKICAgICJsYW1iZGFfbWF4Ijog
MC4wNDMyOTI3MDE5NTQxMjAwMTUsCiAgICAibGFtYmRhX21heF9icmFuY2giOiAicVQyIgogICB9
LAogICAiY3ViaWNfZ2VtOHwxMTEiOiB7CiAgICAidl9FTSI6IDkuNzIxMTcxMDE1MDc4MjEsCiAg
ICAidl9TMkUyIjogOS44NTYyNDYzMTA1OTQ4MTgsCiAgICAidl9TMmgiOiA5LjcwMzIzNDQ3MjUy
ODI1MSwKICAgICJyX3h0YWxfRTIiOiAwLjAxMzg5NDk2MTM0ODQ5MzU1LAogICAgInJfeHRhbF9o
IjogLTAuMDAxODQ1MTAxMDE5NDI4NDc0NSwKICAgICJsYW1iZGFfbWVhbiI6IDAuMDA5MzEwNTAz
ODU5NjUyOCwKICAgICJsYW1iZGFfbWF4IjogMC4wNDMyOTI3MDE5NTQxMjAwMTUsCiAgICAibGFt
YmRhX21heF9icmFuY2giOiAicVQyIgogICB9CiAgfSwKICAidlRfdDAiOiB7CiAgICJoZXhfc3Rl
cHxhIjogewogICAgIlYiOiA4LjU0Nzc3OTQzODczOTIyOCwKICAgICJSIjogOC4yODgzNDEwMjk5
ODM5MjcsCiAgICAiSCI6IDguNDE5MDU5NjM3NTkxNjAzLAogICAgIkhTbG8iOiA4LjM5MDg1OTcz
MTcyODI0NywKICAgICJIU2hpIjogOC40MjQ1ODI0MTk0MDM0NTcKICAgfSwKICAgImhleF9zdGVw
fGIiOiB7CiAgICAiViI6IDguNTQ3OTgyOTk3OTU1Mjk1LAogICAgIlIiOiA4LjI4ODU3NjAyOTE4
MTYyNywKICAgICJIIjogOC40MTkyNzg2NDg1Nzk2MTIsCiAgICAiSFNsbyI6IDguMzkxMDg0NzQ2
ODM3OTQ3LAogICAgIkhTaGkiOiA4LjQyNDgwMzI1NzcyMzgzMgogICB9LAogICAiaGV4X2dlbTh8
YSI6IHsKICAgICJWIjogMTAuMjQ4OTk3Njc0NTY5NTk2LAogICAgIlIiOiA5LjgzMDA3NjMzNjUw
NTMyOSwKICAgICJIIjogMTAuMDQxNzIxODE3MzY5MTQ3LAogICAgIkhTbG8iOiA5Ljk5MDkxMzAw
MTU3MTE1NiwKICAgICJIU2hpIjogMTAuMDUyNzk3NzU0OTQ5MDM3CiAgIH0sCiAgICJoZXhfZ2Vt
OHxiIjogewogICAgIlYiOiAxMC4yNDg4NDc0MTQ4NzIyMzQsCiAgICAiUiI6IDkuODI5ODkwMzEy
NTY2MDEsCiAgICAiSCI6IDEwLjA0MTU1NDA4NTE2MDYzMiwKICAgICJIU2xvIjogOS45OTA3Mzk4
Mjk3MTk4NiwKICAgICJIU2hpIjogMTAuMDUyNjI5OTU5Mjk0OTQ1CiAgIH0sCiAgICJjdWJpY19z
dGVwfDAwMSI6IHsKICAgICJWIjogOC4xMTU3OTQ0Nzc0MzcxOTUsCiAgICAiUiI6IDcuNDY4ODc3
MzQxNjg2NjA3LAogICAgIkgiOiA3Ljc5OTA0NjM3NTg0NDkyMywKICAgICJIU2xvIjogNy43NTg2
MTQ0OTAyMTEwODcsCiAgICAiSFNoaSI6IDcuODY3OTUzMDA1OTA0Nzc1CiAgIH0sCiAgICJjdWJp
Y19zdGVwfDExMSI6IHsKICAgICJWIjogOC4xMTU3OTQ0Nzc0MzcxOTUsCiAgICAiUiI6IDcuNDY4
ODc3MzQxNjg2NjA3LAogICAgIkgiOiA3Ljc5OTA0NjM3NTg0NDkyMywKICAgICJIU2xvIjogNy43
NTg2MTQ0OTAyMTEwODcsCiAgICAiSFNoaSI6IDcuODY3OTUzMDA1OTA0Nzc1CiAgIH0sCiAgICJj
dWJpY19nZW04fDAwMSI6IHsKICAgICJWIjogOS44NzI0OTIwODY2MDEwMiwKICAgICJSIjogOC43
MDY3NzE1Mjc4MzEzNTIsCiAgICAiSCI6IDkuMzA3ODk5MDc2NTMzMTc5LAogICAgIkhTbG8iOiA5
LjIxMTcyMTA2NDM3MDg2MSwKICAgICJIU2hpIjogOS40NTY4NTQ5ODQ1ODg3MzgKICAgfSwKICAg
ImN1YmljX2dlbTh8MTExIjogewogICAgIlYiOiA5Ljg3MjQ5MjA4NjYwMTAyLAogICAgIlIiOiA4
LjcwNjc3MTUyNzgzMTM1MiwKICAgICJIIjogOS4zMDc4OTkwNzY1MzMxNzksCiAgICAiSFNsbyI6
IDkuMjExNzIxMDY0MzcwODYxLAogICAgIkhTaGkiOiA5LjQ1Njg1NDk4NDU4ODczOAogICB9CiAg
fSwKICAiaHNfcmVmIjogewogICAiaGV4X3N0ZXAiOiB7CiAgICAiaGkiOiBbCiAgICAgMTM1LjM2
NjU5NTI4MzY5NzYyLAogICAgIDExNS41NTk4NzMyODkxOTkwMgogICAgXSwKICAgICJsbyI6IFsK
ICAgICAxMzQuNjA3MDg5NDM3MTI2MDYsCiAgICAgNjAuMDMwODAwMDAxNDM3OTcKICAgIF0KICAg
fSwKICAgImhleF9nZW04IjogewogICAgImhpIjogWwogICAgIDIzMC4xMzYwNDgzOTA3MzEzLAog
ICAgIDE3OC4yOTQzNDE3NTU3Njc2NQogICAgXSwKICAgICJsbyI6IFsKICAgICAyMjkuNjk1NzU0
MzM1ODY1NzYsCiAgICAgODQuODI0NTAwMDAyMzEwOTEKICAgIF0KICAgfSwKICAgImN1YmljX3N0
ZXAiOiB7CiAgICAiaGkiOiBbCiAgICAgMTIzLjgzMjQ2NjY2NjA5MDY4LAogICAgIDg1LjI5MzM5
OTk5OTE0NjEyCiAgICBdLAogICAgImxvIjogWwogICAgIDEyMy44MzI0NjY2NjcyNDI2NiwKICAg
ICAzNi43MjUyMDAwMDA4NjM0NwogICAgXQogICB9LAogICAiY3ViaWNfZ2VtOCI6IHsKICAgICJo
aSI6IFsKICAgICAyMTAuMjc1NDk5OTk5MDkzMSwKICAgICAxMzEuNTQzNTk5OTk4NjQ0MTQKICAg
IF0sCiAgICAibG8iOiBbCiAgICAgMjEwLjI3NTUwMDAwMDkwNjkzLAogICAgIDQ2LjM0OTg1MDAw
MTM1OTE0CiAgICBdCiAgIH0KICB9CiB9LAogInBoYXNlMiI6IHt9LAogInBoYXNlMyI6IHsKICAi
dmVyZGljdF9jbGFzcyI6ICJOT1QtQVNTRU1CTEVEIChwaGFzZTAtb25seSBydW4pIiwKICAibm90
ZSI6ICJQaGFzZXMgMi0zIG5vdCBleGVjdXRlZCBvbiB0aGlzIHJ1biBieSB0aGUgYXV0aG9yJ3Mg
ZGlyZWN0aXZlIgogfSwKICJUMV9wb3N0X3dyaXRlIjogewogICJsaXN0X21kNSI6ICJiZTkyMWI4
YzI5Zjc1NzhlODVlZDkyZjE0NTBjMTk1NiIsCiAgInNjYW5uZXJfbWQ1IjogIjZiODYyOTAwOTBh
OGM4NGYxYjFhMGE5OWVjMGJmNjk3IiwKICAiY2hlY2twb2ludCI6ICJDTEVBTiIKIH0KfQ==
=====END-EMBED name=g_mscs2_chatleg_phase0_checkpoint.json=====

=====BEGIN-EMBED name=g_mscs2_chatleg_compare.json md5=7a9e170462cdbd92b8a4fa0b62307986 bytes=3301 encoding=base64 armor_bytes=4462 QUARANTINED=====
ewogImdhdGUiOiAiRy1NU0NTMiIsCiAic3RlcCI6ICJjb21wYXJlIChsYXN0KSIsCiAiY2hlY2tw
b2ludF9tZDUiOiAiMWM1YjZiNTk4MjlkMmE2YjlhZTJiMWE3YTAxNjgzMmQiLAogInJvd3MiOiBb
CiAgewogICAiaWQiOiAiSFlQLU1TMi0xIiwKICAgInByZWRpY3RlZCI6ICJjdWJpYyBrYXBwYTQ0
X0UyICE9IDAsIHwufCBpbiBbMWUtMywgMWUtMl07IGthcHBhNDRfaCBzbWFsbGVyIiwKICAgIm1h
Y2hpbmUiOiB7CiAgICAiY3ViaWNfc3RlcHwwMDEiOiBbCiAgICAgLTAuMDAwMzc0MzUyOTQxODE3
NTY3NCwKICAgICAtMy44MDI4MzI3NjczNDYwNDg0ZS0wNQogICAgXSwKICAgICJjdWJpY19zdGVw
fDExMSI6IFsKICAgICAwLjAwMDI0OTU2ODYyNzg3NzI0MTE3LAogICAgIC0zLjgwMjgzMjc2NzM0
NjA0ODRlLTA1CiAgICBdLAogICAgImN1YmljX2dlbTh8MDAxIjogWwogICAgIC0wLjAwMDQ0OTI3
NzA5MzQyOTYxNjksCiAgICAgLTQuNTM1NzgyMjY2MjQ4OTEzZS0wNQogICAgXSwKICAgICJjdWJp
Y19nZW04fDExMSI6IFsKICAgICAwLjAwMDI5OTUxODA2MjI4ODg3MDg3LAogICAgIC00LjUzNTc4
MjI2NjI0ODkxM2UtMDUKICAgIF0KICAgfSwKICAgImNvbmNvcmRhbnQiOiBmYWxzZQogIH0sCiAg
ewogICAiaWQiOiAiSFlQLU1TMi0yIiwKICAgInByZWRpY3RlZCI6ICJzaWduIGthcHBhNDQoMDAx
KSA8IDAsIHNpZ24ga2FwcGE0NCgxMTEpID4gMCIsCiAgICJtYWNoaW5lIjogewogICAgImN1Ymlj
X3N0ZXB8MDAxIjogLTAuMDAwMzc0MzUyOTQxODE3NTY3NCwKICAgICJjdWJpY19zdGVwfDExMSI6
IDAuMDAwMjQ5NTY4NjI3ODc3MjQxMTcsCiAgICAiY3ViaWNfZ2VtOHwwMDEiOiAtMC4wMDA0NDky
NzcwOTM0Mjk2MTY5LAogICAgImN1YmljX2dlbTh8MTExIjogMC4wMDAyOTk1MTgwNjIyODg4NzA4
NwogICB9LAogICAiY29uY29yZGFudCI6IHRydWUKICB9LAogIHsKICAgImlkIjogIkhZUC1NUzIt
MyIsCiAgICJwcmVkaWN0ZWQiOiAiUzQgPSAwIHdpdGhpbiB0YXUgb24gYWxsIGtleXMsIGJvdGgg
YXJtcyIsCiAgICJtYWNoaW5lIjogewogICAgImhleF9zdGVwfGEiOiBbCiAgICAgLTIuMjEzNjE2
NzgwMDYwNjYwMmUtMTMsCiAgICAgNy42NjU0MjMwODQ1NDc4NDRlLTE0CiAgICBdLAogICAgImhl
eF9zdGVwfGIiOiBbCiAgICAgLTIuMTk5MDI2ODM4ODA3NTk4N2UtMTMsCiAgICAgNy40ODU4NzE2
ODEyMTQ3MTVlLTE0CiAgICBdLAogICAgImhleF9nZW04fGEiOiBbCiAgICAgLTIuNjUyMDQ2Mzc0
NTUxNDY0ZS0xMywKICAgICA4LjM5NDQwODE5OTg0NDE4M2UtMTQKICAgIF0sCiAgICAiaGV4X2dl
bTh8YiI6IFsKICAgICAtMi42NjQ1NDQxMTI2NTY4NTFlLTEzLAogICAgIDguMjU2NzgxNDgzNDg0
Mjk2ZS0xNAogICAgXSwKICAgICJjdWJpY19zdGVwfDAwMSI6IFsKICAgICAtMS45NTQ5Njc4OTQ2
MjYwNTk4ZS0xMSwKICAgICAtMS4xNjk0ODk4NjEwMzc3NTE4ZS0xMQogICAgXSwKICAgICJjdWJp
Y19zdGVwfDExMSI6IFsKICAgICAxLjMwMzU0MTY0MDU4MzMzNDRlLTExLAogICAgIC0xLjE2OTQ4
OTg2MTAzNzc1MThlLTExCiAgICBdLAogICAgImN1YmljX2dlbTh8MDAxIjogWwogICAgIC00LjI2
NzE2ODIyOTAyMTg5NmUtMTEsCiAgICAgLTIuMzg1MjgxNzM0Nzg5ODA5ZS0xMQogICAgXSwKICAg
ICJjdWJpY19nZW04fDExMSI6IFsKICAgICAyLjg0NDc2OTc2NDAxNzk4NzZlLTExLAogICAgIC0y
LjM4NTI4MTczNDc4OTgwOWUtMTEKICAgIF0KICAgfSwKICAgImNvbmNvcmRhbnQiOiB0cnVlCiAg
fSwKICB7CiAgICJpZCI6ICJIWVAtTVMyLTQiLAogICAicHJlZGljdGVkIjogImhleCB8a2FwcGE0
NHwgPCB8a2FwcGEyMnw7IGthcHBhMjQgIT0gMCB3aXRoIHxrYXBwYTQ0fCA8IHxrYXBwYTI0fCA8
IHxrYXBwYTIyfCIsCiAgICJtYWNoaW5lIjogewogICAgImhleF9zdGVwfGEiOiB7CiAgICAgImth
cHBhMjIiOiAtMC4wMDE0Mzk0NjkzMDIwMDMyOTAzLAogICAgICJrYXBwYTI0IjogLTEuMjQ4ODc5
MDczMDQ5MTg4N2UtMDgsCiAgICAgImthcHBhNDQiOiAwLjAwMDE2MDM5OTAzNzYzOTQ1MzE3LAog
ICAgICJyZXNpZHVhbCI6IDMuMzUzODQyMjE2OTAxMTgyNGUtMTAKICAgIH0sCiAgICAiaGV4X3N0
ZXB8YiI6IHsKICAgICAia2FwcGEyMiI6IC0wLjAwMTQzODcxMDI0Nzg4MzYwNiwKICAgICAia2Fw
cGEyNCI6IC0xLjI0ODQ2MTUwODM5MDEyMzZlLTA4LAogICAgICJrYXBwYTQ0IjogMC4wMDAxNjA0
MDgzNTgyMzQ2NTUyNSwKICAgICAicmVzaWR1YWwiOiAzLjM1MjA4OTE2MTM5NzU2N2UtMTAKICAg
IH0sCiAgICAiaGV4X2dlbTh8YSI6IHsKICAgICAia2FwcGEyMiI6IC0wLjAwMTg5NTY1OTkwNjk0
NjgyOTMsCiAgICAgImthcHBhMjQiOiAtMS44MzcyMTM0MTc4NTE5NDNlLTA4LAogICAgICJrYXBw
YTQ0IjogMC4wMDAxNzk0OTg0MjIwMjU4Njk3NiwKICAgICAicmVzaWR1YWwiOiA1LjIzNDUwMTk3
Mzk5NDk3N2UtMTAKICAgIH0sCiAgICAiaGV4X2dlbTh8YiI6IHsKICAgICAia2FwcGEyMiI6IC0w
LjAwMTg5NjE0ODg5Mjk5MzY0OTgsCiAgICAgImthcHBhMjQiOiAtMS44Mzc2MDc0OTkwNDk3Mzg4
ZS0wOCwKICAgICAia2FwcGE0NCI6IDAuMDAwMTc5NDkyNjM5NTAzNTMwNjIsCiAgICAgInJlc2lk
dWFsIjogNS4yMzU4NzgwNzY5MjYxNzJlLTEwCiAgICB9CiAgIH0sCiAgICJjb25jb3JkYW50Ijog
ZmFsc2UKICB9LAogIHsKICAgImlkIjogIkhZUC1NUzItNSIsCiAgICJwcmVkaWN0ZWQiOiAiZmNj
IGJpcmVmcmluZ2VuY2UgY29lZmZpY2llbnQgb2Ygb3JkZXIgMWUtMSBwZXIgdW5pdCB0NDsgdHdv
IG9yZGVycyBhYm92ZSB0aGUgZGVzY3JpcHRvciBzcGxpdCBhdCB0NCB+IDAuMjUiLAogICAibWFj
aGluZSI6IHsKICAgICJjdWJpY19zdGVwfDAwMSI6IFsKICAgICAtMC4wMzc4OTg3MDMzOTU5ODY1
NCwKICAgICAtMC4wMDAzNzQzNTI5NDE4MTc1Njc0CiAgICBdLAogICAgImN1YmljX3N0ZXB8MTEx
IjogWwogICAgIC0wLjAzNzg5ODcwMzM5NTk4NjU0LAogICAgIDAuMDAwMjQ5NTY4NjI3ODc3MjQx
MTcKICAgIF0sCiAgICAiY3ViaWNfZ2VtOHwwMDEiOiBbCiAgICAgLTAuMDQ1NDgxMjUyMjI3NzQ5
MjQsCiAgICAgLTAuMDAwNDQ5Mjc3MDkzNDI5NjE2OQogICAgXSwKICAgICJjdWJpY19nZW04fDEx
MSI6IFsKICAgICAtMC4wNDU0ODEyNTIyMjc3NDkyNCwKICAgICAwLjAwMDI5OTUxODA2MjI4ODg3
MDg3CiAgICBdCiAgIH0sCiAgICJjb25jb3JkYW50IjogdHJ1ZQogIH0KIF0sCiAidmVyZGljdF9j
bGFzcyI6ICJJREVOVElUWS1ERUxJVkVSRUQtTDQiLAogIm5fY29uY29yZGFudCI6IDMKfQ==
=====END-EMBED name=g_mscs2_chatleg_compare.json=====

=====BEGIN-EMBED name=g_mscs2_chatleg_selfcompare.json md5=0a10623660c8fbaed4c37ec388978593 bytes=65952 encoding=base64 armor_bytes=89094 QUARANTINED=====
ewogImNjX2NrcHRfbWQ1IjogIjFjNWI2YjU5ODI5ZDJhNmI5YWUyYjFhN2EwMTY4MzJkIiwKICJj
aGF0X2NrcHRfbWQ1IjogIjFjNWI2YjU5ODI5ZDJhNmI5YWUyYjFhN2EwMTY4MzJkIiwKICJjb21w
YXJhdG9yIjogImdfbXNjczJfY29tcGFyZV92MV8wIiwKICJtaXNzZXMiOiBbCiAgewogICAiY2Mi
OiAiY2hhdCIsCiAgICJjaGF0IjogImNoYXQiLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6
ICJsZWcgbGFiZWxzIGNoYXQvY2MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IGZhbHNlCiAg
fSwKICB7CiAgICJjYyI6ICJmMjc3NTgwZGRmMGI0ZGE5NzM0ZDExZWRiMDA5YzU0YiIsCiAgICJj
aGF0IjogImYyNzc1ODBkZGYwYjRkYTk3MzRkMTFlZGIwMDljNTRiIiwKICAgImNoZWNrIjogIkMw
IiwKICAgIm5hbWUiOiAiaW5kZXBlbmRlbmNlIHdpdG5lc3M6IGluc3RydW1lbnRfbWQ1IGRpZmZl
ciIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogZmFsc2UKICB9LAogIHsKICAgImNjIjogbnVs
bCwKICAgImNoYXQiOiA0LjQ4MTkxMTA3NjM2MTA5ZS0wOSwKICAgImNoZWNrIjogIkMyIiwKICAg
Im5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS5xdWFkZm9ybS5rYXBwYTIyIChjaGF0KSBj
dWJpYyBudWxsIGFicyA8PSAxZS0xMCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogZmFsc2UK
ICB9LAogIHsKICAgImNjIjogNC40ODE5MTEwNzYzNjEwOWUtMDksCiAgICJjaGF0IjogbnVsbCwK
ICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS5xdWFk
Zm9ybS5rYXBwYTIyIChjYykgY3ViaWMgbnVsbCBhYnMgPD0gMWUtMTAiLAogICAibm90ZSI6ICIi
LAogICAicGFzcyI6IGZhbHNlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogMS45
NzQwNDMzNzQ5ODYwNzZlLTA3LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJb
Y3ViaWNfc3RlcHwwMDFdLnF1YWRmb3JtLmthcHBhMjQgKGNoYXQpIGN1YmljIG51bGwgYWJzIDw9
IDFlLTEwIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiBmYWxzZQogIH0sCiAgewogICAiY2Mi
OiAxLjk3NDA0MzM3NDk4NjA3NmUtMDcsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMy
IiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS5xdWFkZm9ybS5rYXBwYTI0IChj
YykgY3ViaWMgbnVsbCBhYnMgPD0gMWUtMTAiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IGZh
bHNlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogLTIuOTg3OTM4ODMwMjcxOThl
LTA5LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfc3RlcHwxMTFd
LnF1YWRmb3JtLmthcHBhMjIgKGNoYXQpIGN1YmljIG51bGwgYWJzIDw9IDFlLTEwIiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiBmYWxzZQogIH0sCiAgewogICAiY2MiOiAtMi45ODc5Mzg4MzAy
NzE5OGUtMDksCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAi
cGhhc2UyW2N1YmljX3N0ZXB8MTExXS5xdWFkZm9ybS5rYXBwYTIyIChjYykgY3ViaWMgbnVsbCBh
YnMgPD0gMWUtMTAiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IGZhbHNlCiAgfSwKICB7CiAg
ICJjYyI6IG51bGwsCiAgICJjaGF0IjogMS45NzQwNDMzODcwNjUxNzI0ZS0wNywKICAgImNoZWNr
IjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MTExXS5xdWFkZm9ybS5rYXBw
YTI0IChjaGF0KSBjdWJpYyBudWxsIGFicyA8PSAxZS0xMCIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogZmFsc2UKICB9LAogIHsKICAgImNjIjogMS45NzQwNDMzODcwNjUxNzI0ZS0wNywKICAg
ImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNf
c3RlcHwxMTFdLnF1YWRmb3JtLmthcHBhMjQgKGNjKSBjdWJpYyBudWxsIGFicyA8PSAxZS0xMCIs
CiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogZmFsc2UKICB9LAogIHsKICAgImNjIjogbnVsbCwK
ICAgImNoYXQiOiA3Ljk2Mzc1NzkzMzM2Nzc5OWUtMDksCiAgICJjaGVjayI6ICJDMiIsCiAgICJu
YW1lIjogInBoYXNlMltjdWJpY19nZW04fDAwMV0ucXVhZGZvcm0ua2FwcGEyMiAoY2hhdCkgY3Vi
aWMgbnVsbCBhYnMgPD0gMWUtMTAiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IGZhbHNlCiAg
fSwKICB7CiAgICJjYyI6IDcuOTYzNzU3OTMzMzY3Nzk5ZS0wOSwKICAgImNoYXQiOiBudWxsLAog
ICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwwMDFdLnF1YWRm
b3JtLmthcHBhMjIgKGNjKSBjdWJpYyBudWxsIGFicyA8PSAxZS0xMCIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogZmFsc2UKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAzLjQ3
Nzg1NzI0NjI4MTQ0MTRlLTA3LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJb
Y3ViaWNfZ2VtOHwwMDFdLnF1YWRmb3JtLmthcHBhMjQgKGNoYXQpIGN1YmljIG51bGwgYWJzIDw9
IDFlLTEwIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiBmYWxzZQogIH0sCiAgewogICAiY2Mi
OiAzLjQ3Nzg1NzI0NjI4MTQ0MTRlLTA3LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJD
MiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19nZW04fDAwMV0ucXVhZGZvcm0ua2FwcGEyNCAo
Y2MpIGN1YmljIG51bGwgYWJzIDw9IDFlLTEwIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiBm
YWxzZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IC01LjMwOTE3MzgzNjQ1MzA3
MzRlLTA5LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwx
MTFdLnF1YWRmb3JtLmthcHBhMjIgKGNoYXQpIGN1YmljIG51bGwgYWJzIDw9IDFlLTEwIiwKICAg
Im5vdGUiOiAiIiwKICAgInBhc3MiOiBmYWxzZQogIH0sCiAgewogICAiY2MiOiAtNS4zMDkxNzM4
MzY0NTMwNzM0ZS0wOSwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFt
ZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFdLnF1YWRmb3JtLmthcHBhMjIgKGNjKSBjdWJpYyBu
dWxsIGFicyA8PSAxZS0xMCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogZmFsc2UKICB9LAog
IHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAzLjQ3Nzg1NzIzODQ2NTQyOGUtMDcsCiAgICJj
aGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19nZW04fDExMV0ucXVhZGZvcm0u
a2FwcGEyNCAoY2hhdCkgY3ViaWMgbnVsbCBhYnMgPD0gMWUtMTAiLAogICAibm90ZSI6ICIiLAog
ICAicGFzcyI6IGZhbHNlCiAgfSwKICB7CiAgICJjYyI6IDMuNDc3ODU3MjM4NDY1NDI4ZS0wNywK
ICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3Vi
aWNfZ2VtOHwxMTFdLnF1YWRmb3JtLmthcHBhMjQgKGNjKSBjdWJpYyBudWxsIGFicyA8PSAxZS0x
MCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogZmFsc2UKICB9CiBdLAogInJvd3MiOiBbCiAg
ewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJu
YW1lIjogInJlcXVpcmVkIGtleSBnYXRlIHByZXNlbnQgKGNoYXQpIiwKICAgIm5vdGUiOiAiIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwK
ICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAicmVxdWlyZWQga2V5IGdhdGUgcHJlc2VudCAo
Y2MpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51
bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAicmVxdWly
ZWQga2V5IGxlZyBwcmVzZW50IChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJD
MCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBsZWcgcHJlc2VudCAoY2MpIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0Ijog
bnVsbCwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAicmVxdWlyZWQga2V5IGluc3RydW1l
bnRfbWQ1IHByZXNlbnQgKGNoYXQpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMwIiwK
ICAgIm5hbWUiOiAicmVxdWlyZWQga2V5IGluc3RydW1lbnRfbWQ1IHByZXNlbnQgKGNjKSIsCiAg
ICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAi
Y2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBt
ZW1vX2xvY2tfbWQ1IHByZXNlbnQgKGNoYXQpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjog
IkMwIiwKICAgIm5hbWUiOiAicmVxdWlyZWQga2V5IG1lbW9fbG9ja19tZDUgcHJlc2VudCAoY2Mp
IiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGws
CiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAicmVxdWlyZWQg
a2V5IGxlZGdlcl9iYXNlX21kNSBwcmVzZW50IChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJj
aGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBsZWRnZXJfYmFzZV9tZDUgcHJl
c2VudCAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJj
YyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAi
cmVxdWlyZWQga2V5IHQxX2xpc3RfbWQ1IHByZXNlbnQgKGNoYXQpIiwKICAgIm5vdGUiOiAiIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwK
ICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAicmVxdWlyZWQga2V5IHQxX2xpc3RfbWQ1IHBy
ZXNlbnQgKGNjKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjog
InJlcXVpcmVkIGtleSB4MV9tZDUgcHJlc2VudCAoY2hhdCkiLAogICAibm90ZSI6ICIiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAi
Y2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1aXJlZCBrZXkgeDFfbWQ1IHByZXNlbnQgKGNj
KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxs
LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVk
IGtleSB4Nl9jaGF0X21kNSBwcmVzZW50IChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVj
ayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSB4Nl9jaGF0X21kNSBwcmVzZW50IChj
YykiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVs
bCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1aXJl
ZCBrZXkgeDZfY2NfbWQ1IHByZXNlbnQgKGNoYXQpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNr
IjogIkMwIiwKICAgIm5hbWUiOiAicmVxdWlyZWQga2V5IHg2X2NjX21kNSBwcmVzZW50IChjYyki
LAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwK
ICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1aXJlZCBr
ZXkgZWxlY3Rpb25zIHByZXNlbnQgKGNoYXQpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjog
IkMwIiwKICAgIm5hbWUiOiAicmVxdWlyZWQga2V5IGVsZWN0aW9ucyBwcmVzZW50IChjYykiLAog
ICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAg
ImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1aXJlZCBrZXkg
dDFfc2NhbiBwcmVzZW50IChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIs
CiAgICJuYW1lIjogInJlcXVpcmVkIGtleSB0MV9zY2FuIHByZXNlbnQgKGNjKSIsCiAgICJub3Rl
IjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6
IG51bGwsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBwaGFzZTAg
cHJlc2VudCAoY2hhdCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFt
ZSI6ICJyZXF1aXJlZCBrZXkgcGhhc2UwIHByZXNlbnQgKGNjKSIsCiAgICJub3RlIjogIiIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAg
ICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBwaGFzZTIgcHJlc2VudCAo
Y2hhdCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
bnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1
aXJlZCBrZXkgcGhhc2UyIHByZXNlbnQgKGNjKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjog
dHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6
ICJDMCIsCiAgICJuYW1lIjogInJlcXVpcmVkIGtleSBwaGFzZTMgcHJlc2VudCAoY2hhdCkiLAog
ICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAg
ImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJyZXF1aXJlZCBrZXkg
cGhhc2UzIHByZXNlbnQgKGNjKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiAiZWZkY2FiZGNkOTM3Y2RhNGFjYjY0Zjk0MWRjNGJiMmIiLAogICAiY2hh
dCI6ICJlZmRjYWJkY2Q5MzdjZGE0YWNiNjRmOTQxZGM0YmIyYiIsCiAgICJjaGVjayI6ICJDMCIs
CiAgICJuYW1lIjogIm1lbW9fbG9ja19tZDUgPT0gc2NoZW1hIChjaGF0KSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiZWZkY2FiZGNkOTM3Y2RhNGFj
YjY0Zjk0MWRjNGJiMmIiLAogICAiY2hhdCI6ICJlZmRjYWJkY2Q5MzdjZGE0YWNiNjRmOTQxZGM0
YmIyYiIsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogIm1lbW9fbG9ja19tZDUgPT0gc2No
ZW1hIChjYykiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogImYzNmJiZGIwNDEwNDAwODc4M2YyNzYzZjcwZmI5MTZmIiwKICAgImNoYXQiOiAiZjM2YmJk
YjA0MTA0MDA4NzgzZjI3NjNmNzBmYjkxNmYiLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6
ICJsZWRnZXJfYmFzZV9tZDUgPT0gc2NoZW1hIChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiZjM2YmJkYjA0MTA0MDA4NzgzZjI3NjNmNzBm
YjkxNmYiLAogICAiY2hhdCI6ICJmMzZiYmRiMDQxMDQwMDg3ODNmMjc2M2Y3MGZiOTE2ZiIsCiAg
ICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogImxlZGdlcl9iYXNlX21kNSA9PSBzY2hlbWEgKGNj
KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiYmU5
MjFiOGMyOWY3NTc4ZTg1ZWQ5MmYxNDUwYzE5NTYiLAogICAiY2hhdCI6ICJiZTkyMWI4YzI5Zjc1
NzhlODVlZDkyZjE0NTBjMTk1NiIsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInQxX2xp
c3RfbWQ1ID09IHNjaGVtYSAoY2hhdCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUK
ICB9LAogIHsKICAgImNjIjogImJlOTIxYjhjMjlmNzU3OGU4NWVkOTJmMTQ1MGMxOTU2IiwKICAg
ImNoYXQiOiAiYmU5MjFiOGMyOWY3NTc4ZTg1ZWQ5MmYxNDUwYzE5NTYiLAogICAiY2hlY2siOiAi
QzAiLAogICAibmFtZSI6ICJ0MV9saXN0X21kNSA9PSBzY2hlbWEgKGNjKSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiMjAwZTdhOGI3NzU1Nzc1NjQz
NjljNjkyNGQzOGE4NGMiLAogICAiY2hhdCI6ICIyMDBlN2E4Yjc3NTU3NzU2NDM2OWM2OTI0ZDM4
YTg0YyIsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogIngxX21kNSA9PSBzY2hlbWEgKGNo
YXQpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICIy
MDBlN2E4Yjc3NTU3NzU2NDM2OWM2OTI0ZDM4YTg0YyIsCiAgICJjaGF0IjogIjIwMGU3YThiNzc1
NTc3NTY0MzY5YzY5MjRkMzhhODRjIiwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAieDFf
bWQ1ID09IHNjaGVtYSAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwK
ICB7CiAgICJjYyI6ICJjMDRjMGI4ZWEzNGNmZTYwZjIzMWFhMDY4MjhlNmNlNCIsCiAgICJjaGF0
IjogImMwNGMwYjhlYTM0Y2ZlNjBmMjMxYWEwNjgyOGU2Y2U0IiwKICAgImNoZWNrIjogIkMwIiwK
ICAgIm5hbWUiOiAieDZfY2hhdF9tZDUgPT0gc2NoZW1hIChjaGF0KSIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiYzA0YzBiOGVhMzRjZmU2MGYyMzFh
YTA2ODI4ZTZjZTQiLAogICAiY2hhdCI6ICJjMDRjMGI4ZWEzNGNmZTYwZjIzMWFhMDY4MjhlNmNl
NCIsCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogIng2X2NoYXRfbWQ1ID09IHNjaGVtYSAo
Y2MpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICIy
NDllMTFkZDUzYzRjYjgyZjMwMmIxNWQzYzk0YzMzNyIsCiAgICJjaGF0IjogIjI0OWUxMWRkNTNj
NGNiODJmMzAyYjE1ZDNjOTRjMzM3IiwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAieDZf
Y2NfbWQ1ID09IHNjaGVtYSAoY2hhdCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUK
ICB9LAogIHsKICAgImNjIjogIjI0OWUxMWRkNTNjNGNiODJmMzAyYjE1ZDNjOTRjMzM3IiwKICAg
ImNoYXQiOiAiMjQ5ZTExZGQ1M2M0Y2I4MmYzMDJiMTVkM2M5NGMzMzciLAogICAiY2hlY2siOiAi
QzAiLAogICAibmFtZSI6ICJ4Nl9jY19tZDUgPT0gc2NoZW1hIChjYykiLAogICAibm90ZSI6ICIi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIkctTVNDUzIiLAogICAiY2hhdCI6
ICJHLU1TQ1MyIiwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAiZ2F0ZSBsYWJlbCIsCiAg
ICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiY2hhdCIsCiAg
ICJjaGF0IjogImNoYXQiLAogICAiY2hlY2siOiAiQzAiLAogICAibmFtZSI6ICJsZWcgbGFiZWxz
IGNoYXQvY2MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IGZhbHNlCiAgfSwKICB7CiAgICJj
YyI6IG51bGwsCiAgICJjaGF0IjogIkNMRUFOIiwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUi
OiAidDFfc2Nhbi5pbnN0cnVtZW50IENMRUFOIChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiQ0xFQU4iLAogICAiY2hhdCI6IG51bGwsCiAg
ICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogInQxX3NjYW4uaW5zdHJ1bWVudCBDTEVBTiAoY2Mp
IiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGws
CiAgICJjaGF0IjogIkNMRUFOIiwKICAgImNoZWNrIjogIkMwIiwKICAgIm5hbWUiOiAidDFfc2Nh
bi5tZW1vIENMRUFOIChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiAiQ0xFQU4iLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMCIs
CiAgICJuYW1lIjogInQxX3NjYW4ubWVtbyBDTEVBTiAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAg
InBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHsKICAgICJFLU1TMi0xIjogImErYiIsCiAg
ICAiRS1NUzItMiI6ICJhIiwKICAgICJFLU1TMi0yYiI6ICJhK2IiLAogICAgIkUtTVMyLTJjIjog
IjAwMSsxMTEiLAogICAgIkUtTVMyLTMiOiAiYSIsCiAgICAiRS1NUzItNCI6ICJhIiwKICAgICJF
LU1TMi01IjogImEiLAogICAgIkUtTVMyLTYiOiAiYSIsCiAgICAiRS1NUzItNyI6ICIwNTMwMjIx
MCtNU0NTMXN0cmF0dW0iLAogICAgIkUtTVMyLTgiOiAiYSIKICAgfSwKICAgImNoYXQiOiB7CiAg
ICAiRS1NUzItMSI6ICJhK2IiLAogICAgIkUtTVMyLTIiOiAiYSIsCiAgICAiRS1NUzItMmIiOiAi
YStiIiwKICAgICJFLU1TMi0yYyI6ICIwMDErMTExIiwKICAgICJFLU1TMi0zIjogImEiLAogICAg
IkUtTVMyLTQiOiAiYSIsCiAgICAiRS1NUzItNSI6ICJhIiwKICAgICJFLU1TMi02IjogImEiLAog
ICAgIkUtTVMyLTciOiAiMDUzMDIyMTArTVNDUzFzdHJhdHVtIiwKICAgICJFLU1TMi04IjogImEi
CiAgIH0sCiAgICJjaGVjayI6ICJDMCIsCiAgICJuYW1lIjogImVsZWN0aW9ucyA9PSBzY2hlbWEg
KGNoYXQpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
IHsKICAgICJFLU1TMi0xIjogImErYiIsCiAgICAiRS1NUzItMiI6ICJhIiwKICAgICJFLU1TMi0y
YiI6ICJhK2IiLAogICAgIkUtTVMyLTJjIjogIjAwMSsxMTEiLAogICAgIkUtTVMyLTMiOiAiYSIs
CiAgICAiRS1NUzItNCI6ICJhIiwKICAgICJFLU1TMi01IjogImEiLAogICAgIkUtTVMyLTYiOiAi
YSIsCiAgICAiRS1NUzItNyI6ICIwNTMwMjIxMCtNU0NTMXN0cmF0dW0iLAogICAgIkUtTVMyLTgi
OiAiYSIKICAgfSwKICAgImNoYXQiOiB7CiAgICAiRS1NUzItMSI6ICJhK2IiLAogICAgIkUtTVMy
LTIiOiAiYSIsCiAgICAiRS1NUzItMmIiOiAiYStiIiwKICAgICJFLU1TMi0yYyI6ICIwMDErMTEx
IiwKICAgICJFLU1TMi0zIjogImEiLAogICAgIkUtTVMyLTQiOiAiYSIsCiAgICAiRS1NUzItNSI6
ICJhIiwKICAgICJFLU1TMi02IjogImEiLAogICAgIkUtTVMyLTciOiAiMDUzMDIyMTArTVNDUzFz
dHJhdHVtIiwKICAgICJFLU1TMi04IjogImEiCiAgIH0sCiAgICJjaGVjayI6ICJDMCIsCiAgICJu
YW1lIjogImVsZWN0aW9ucyA9PSBzY2hlbWEgKGNjKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiZjI3NzU4MGRkZjBiNGRhOTczNGQxMWVkYjAwOWM1
NGIiLAogICAiY2hhdCI6ICJmMjc3NTgwZGRmMGI0ZGE5NzM0ZDExZWRiMDA5YzU0YiIsCiAgICJj
aGVjayI6ICJDMCIsCiAgICJuYW1lIjogImluZGVwZW5kZW5jZSB3aXRuZXNzOiBpbnN0cnVtZW50
X21kNSBkaWZmZXIiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IGZhbHNlCiAgfSwKICB7CiAg
ICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUi
OiAicGhhc2UwLlBJTi1YVEFMLnBhc3NlZCB0cnVlIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IDAuMCwK
ICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLlBJTi1YVEFMLndvcnN0X3JlbCAo
Y2hhdCkgbGUgMWUtMDgiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogMC4wLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1l
IjogInBoYXNlMC5QSU4tWFRBTC53b3JzdF9yZWwgKGNjKSBsZSAxZS0wOCIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRy
dWUsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5QSU4tVlJIMC5wYXNzZWQg
dHJ1ZSBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAwLjAsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1l
IjogInBoYXNlMC5QSU4tVlJIMC53b3JzdF9yZWwgKGNoYXQpIGxlIDFlLTA4IiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDAuMCwKICAgImNoYXQiOiBu
dWxsLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuUElOLVZSSDAud29yc3Rf
cmVsIChjYykgbGUgMWUtMDgiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzEiLAogICAi
bmFtZSI6ICJwaGFzZTAuUElOLUhTMC5wYXNzZWQgdHJ1ZSBib3RoIGxlZ3MiLAogICAibm90ZSI6
ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAw
LjAsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5QSU4tSFMwLndvcnN0X3Jl
bCAoY2hhdCkgbGUgMWUtMDYiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogMC4wLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMSIsCiAgICJu
YW1lIjogInBoYXNlMC5QSU4tSFMwLndvcnN0X3JlbCAoY2MpIGxlIDFlLTA2IiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0Ijog
dHJ1ZSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLlBJTi1LMi5wYXNzZWQg
dHJ1ZSBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAyLjE1NTMzNzY5NjY0NzYwMzVlLTE1LAogICAiY2hl
Y2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuUElOLUsyLndvcnN0X2Fic19jdWJpY19rYXBw
YTIgKGNoYXQpIGxlIDFlLTEyIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwK
ICB7CiAgICJjYyI6IDIuMTU1MzM3Njk2NjQ3NjAzNWUtMTUsCiAgICJjaGF0IjogbnVsbCwKICAg
ImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLlBJTi1LMi53b3JzdF9hYnNfY3ViaWNf
a2FwcGEyIChjYykgbGUgMWUtMTIiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAxLjM5Mjk2NzUyNDU4NTkyOTVlLTEyLAog
ICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuUElOLUsyLndvcnN0X3JlbF9oZXhf
a2FwcGEyIChjaGF0KSBsZSAwLjAwMDEiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUK
ICB9LAogIHsKICAgImNjIjogMS4zOTI5Njc1MjQ1ODU5Mjk1ZS0xMiwKICAgImNoYXQiOiBudWxs
LAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuUElOLUsyLndvcnN0X3JlbF9o
ZXhfa2FwcGEyIChjYykgbGUgMC4wMDAxIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkMx
IiwKICAgIm5hbWUiOiAicGhhc2UwLkYtQ1RSTC1JU08ucGFzc2VkIHRydWUgYm90aCBsZWdzIiwK
ICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAg
ICJjaGF0IjogNC40NDA4OTIwOTg1MDA2MjZlLTE2LAogICAiY2hlY2siOiAiQzEiLAogICAibmFt
ZSI6ICJwaGFzZTAuRi1DVFJMLUlTTy53b3JzdF9hYnMgKGNoYXQpIGxlIDFlLTEwIiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDQuNDQwODkyMDk4NTAw
NjI2ZS0xNiwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJw
aGFzZTAuRi1DVFJMLUlTTy53b3JzdF9hYnMgKGNjKSBsZSAxZS0xMCIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUs
CiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5GLUNUUkwtU08zLnBhc3NlZCB0
cnVlIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewog
ICAiY2MiOiBudWxsLAogICAiY2hhdCI6IDQuOTk2MDAzNjEwODEzMjA0ZS0xNiwKICAgImNoZWNr
IjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLkYtQ1RSTC1TTzMuZGV2X2Zyb21fMHA0IChjaGF0
KSBsZSAxZS0xMCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiA0Ljk5NjAwMzYxMDgxMzIwNGUtMTYsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjog
IkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLkYtQ1RSTC1TTzMuZGV2X2Zyb21fMHA0IChjYykgbGUg
MWUtMTAiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
bnVsbCwKICAgImNoYXQiOiAwLjAsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNl
MC5GLUNUUkwtU08zLnJfYWdnXzBfYWJzIChjaGF0KSBsZSAxZS0wNiIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAwLjAsCiAgICJjaGF0IjogbnVsbCwK
ICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLkYtQ1RSTC1TTzMucl9hZ2dfMF9h
YnMgKGNjKSBsZSAxZS0wNiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMSIsCiAgICJu
YW1lIjogInBoYXNlMC5GLUNUUkwtUE9TLnBhc3NlZCB0cnVlIGJvdGggbGVncyIsCiAgICJub3Rl
IjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6
IDAuMzk1MDI3MDYxNzg1NTE0OTQsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNl
MC5GLUNUUkwtUE9TLm1pbl9vZGZfd2VpZ2h0IChjaGF0KSBnZSAwLjAiLAogICAibm90ZSI6ICIi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMC4zOTUwMjcwNjE3ODU1MTQ5NCwK
ICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuRi1D
VFJMLVBPUy5taW5fb2RmX3dlaWdodCAoY2MpIGdlIDAuMCIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAogICAiY2hhdCI6IHRydWUsCiAgICJj
aGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5GLUNUUkwtTDJOVUxMLnBhc3NlZCB0cnVl
IGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiBudWxsLAogICAiY2hhdCI6IDUuODQ5OTA4OTMzNjc2MTcxZS0xNCwKICAgImNoZWNrIjog
IkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLkYtQ1RSTC1MMk5VTEwud29yc3RfYWJzIChjaGF0KSBs
ZSAxZS0xMiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiA1Ljg0OTkwODkzMzY3NjE3MWUtMTQsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMx
IiwKICAgIm5hbWUiOiAicGhhc2UwLkYtQ1RSTC1MMk5VTEwud29yc3RfYWJzIChjYykgbGUgMWUt
MTIiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogdHJ1
ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAu
Ri1DVFJMLUw0RVhIQVVTVC5wYXNzZWQgdHJ1ZSBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAog
ICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiA0LjQ0MDg5
MjA5ODUwMDYyNmUtMTYsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5GLUNU
UkwtTDRFWEhBVVNULndvcnN0X2Fic19yX2FnZyAoY2hhdCkgbGUgMWUtMTIiLAogICAibm90ZSI6
ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogNC40NDA4OTIwOTg1MDA2MjZl
LTE2LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNl
MC5GLUNUUkwtTDRFWEhBVVNULndvcnN0X2Fic19yX2FnZyAoY2MpIGxlIDFlLTEyIiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0
IjogNC4zMjU3NzI4Nzg5NTQ1ODhlLTE0LAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJw
aGFzZTAuRi1DVFJMLUw0RVhIQVVTVC53b3JzdF9yZWxfdGVuc29yIChjaGF0KSBsZSAxZS0xMiIs
CiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA0LjMyNTc3
Mjg3ODk1NDU4OGUtMTQsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMxIiwKICAgIm5h
bWUiOiAicGhhc2UwLkYtQ1RSTC1MNEVYSEFVU1Qud29yc3RfcmVsX3RlbnNvciAoY2MpIGxlIDFl
LTEyIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRy
dWUsCiAgICJjaGF0IjogdHJ1ZSwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2Uw
LkYtQ1RSTC1DNC5wYXNzZWQgdHJ1ZSBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFz
cyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAyLjMwMjE1ODQ2Mzg2
MjcyNDhlLTE0LAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuRi1DVFJMLUM0
LmgwX2VmZmVjdF9yZWwgKGNoYXQpIGxlIDFlLTEyIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDIuMzAyMTU4NDYzODYyNzI0OGUtMTQsCiAgICJjaGF0
IjogbnVsbCwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLkYtQ1RSTC1DNC5o
MF9lZmZlY3RfcmVsIChjYykgbGUgMWUtMTIiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRy
dWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiA0LjA3NDA0MzcyMTY2NzMzMzRl
LTE0LAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuRi1DVFJMLUM0LndvcnN0
X3JlbF9hZmZpbmUgKGNoYXQpIGxlIDFlLTEyIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IDQuMDc0MDQzNzIxNjY3MzMzNGUtMTQsCiAgICJjaGF0Ijog
bnVsbCwKICAgImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLkYtQ1RSTC1DNC53b3Jz
dF9yZWxfYWZmaW5lIChjYykgbGUgMWUtMTIiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRy
dWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAyLjUxODY5MjY1NTAwOTk2MDVl
LTE0LAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuRi1DVFJMLUM0LndvcnN0
X3JlbF9jbG9zZWRfZm9ybSAoY2hhdCkgbGUgMWUtMTIiLAogICAibm90ZSI6ICIiLAogICAicGFz
cyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMi41MTg2OTI2NTUwMDk5NjA1ZS0xNCwKICAgImNo
YXQiOiBudWxsLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuRi1DVFJMLUM0
LndvcnN0X3JlbF9jbG9zZWRfZm9ybSAoY2MpIGxlIDFlLTEyIiwKICAgIm5vdGUiOiAiIiwKICAg
InBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IHRydWUsCiAgICJjaGF0IjogdHJ1ZSwKICAg
ImNoZWNrIjogIkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLkYtQ1RSTC1NQVJHLnBhc3NlZCB0cnVl
IGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiBudWxsLAogICAiY2hhdCI6IDguMzI2NjcyNjg0Njg4Njc0ZS0xNiwKICAgImNoZWNrIjog
IkMxIiwKICAgIm5hbWUiOiAicGhhc2UwLkYtQ1RSTC1NQVJHLndvcnN0X2FicyAoY2hhdCkgbGUg
MWUtMTIiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
OC4zMjY2NzI2ODQ2ODg2NzRlLTE2LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMSIs
CiAgICJuYW1lIjogInBoYXNlMC5GLUNUUkwtTUFSRy53b3JzdF9hYnMgKGNjKSBsZSAxZS0xMiIs
CiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiB0cnVlLAog
ICAiY2hhdCI6IHRydWUsCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5GLUNU
UkwtVEVYNC5wYXNzZWQgdHJ1ZSBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6
IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAwLjAwMDQxMTgzMjY1NTc3
MzM4MDksCiAgICJjaGVjayI6ICJDMSIsCiAgICJuYW1lIjogInBoYXNlMC5GLUNUUkwtVEVYNC5y
X2FnZ190MV9hYnMgKGNoYXQpIGd0IDFlLTA2IiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IDAuMDAwNDExODMyNjU1NzczMzgwOSwKICAgImNoYXQiOiBu
dWxsLAogICAiY2hlY2siOiAiQzEiLAogICAibmFtZSI6ICJwaGFzZTAuRi1DVFJMLVRFWDQucl9h
Z2dfdDFfYWJzIChjYykgZ3QgMWUtMDYiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUK
ICB9LAogIHsKICAgImNjIjogdHJ1ZSwKICAgImNoYXQiOiB0cnVlLAogICAiY2hlY2siOiAiQzEi
LAogICAibmFtZSI6ICJwaGFzZTAuRi1DVFJMLVFVQUQucGFzc2VkIHRydWUgYm90aCBsZWdzIiwK
ICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAg
ICJjaGF0IjogMi4yNjAzNDI4ODYwNzA0MzE1ZS0xNCwKICAgImNoZWNrIjogIkMxIiwKICAgIm5h
bWUiOiAicGhhc2UwLkYtQ1RSTC1RVUFELmRvdWJsaW5nX3Jlc2lkdWFsIChjaGF0KSBsZSAxZS0x
MCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAyLjI2
MDM0Mjg4NjA3MDQzMTVlLTE0LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMSIsCiAg
ICJuYW1lIjogInBoYXNlMC5GLUNUUkwtUVVBRC5kb3VibGluZ19yZXNpZHVhbCAoY2MpIGxlIDFl
LTEwIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51
bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2Uy
W2hleF9zdGVwfGFdIHByZXNlbnQgYm90aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6IDEyLAogICAiY2hlY2siOiAi
QzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8YV0ubGFtYmRhX21lYW5fdDQgbGVuZ3Ro
IDEyIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewog
ICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1l
IjogInBoYXNlMltoZXhfc3RlcHxhXS5sYW1iZGFfbWVhbl90NCBlbGVtZW50d2lzZSA8PSAxZS0w
NiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUi
OiAicGhhc2UyW2hleF9zdGVwfGFdLnJfYWdnX0UyX0hTIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAog
ICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAg
ImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0
ZXB8YV0ucl9hZ2dfRTJfSFMgZWxlbWVudHdpc2UgPD0gMWUtMDYiLAogICAibm90ZSI6ICJ3b3Jz
dCAwLjAwMGUrMDAiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMTIsCiAgICJj
aGF0IjogMTIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfc3RlcHxh
XS5yX2FnZ19FMl9SIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFz
cyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hl
Y2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8YV0ucl9hZ2dfRTJfUiBlbGVt
ZW50d2lzZSA8PSAxZS0wNiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjog
IkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9zdGVwfGFdLnJfYWdnX0UyX1YgbGVuZ3RoIDEy
IGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjog
InBoYXNlMltoZXhfc3RlcHxhXS5yX2FnZ19FMl9WIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAg
Im5vdGUiOiAid29yc3QgMC4wMDBlKzAwIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJj
YyI6IDEyLAogICAiY2hhdCI6IDEyLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFz
ZTJbaGV4X3N0ZXB8YV0ucl9hZ2dfRTJfVlJIIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90
ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQi
OiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8YV0u
cl9hZ2dfRTJfVlJIIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAid29yc3QgMC4w
MDBlKzAwIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6
IDEyLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8YV0ucl9h
Z2dfaF9WUkggbGVuZ3RoIDEyIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjog
dHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6
ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfc3RlcHxhXS5yX2FnZ19oX1ZSSCBlbGVtZW50
d2lzZSA8PSAxZS0wNiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjog
dHJ1ZQogIH0sCiAgewogICAiY2MiOiAtMi4yMTM2MTY3ODAwNjA2NjAyZS0xMywKICAgImNoYXQi
OiAtMi4yMTM2MTY3ODAwNjA2NjAyZS0xMywKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAi
cGhhc2UyW2hleF9zdGVwfGFdLlM0X0UyIGFicyA8PSAxZS0wNiIsCiAgICJub3RlIjogIiIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA3LjY2NTQyMzA4NDU0Nzg0NGUtMTQsCiAg
ICJjaGF0IjogNy42NjU0MjMwODQ1NDc4NDRlLTE0LAogICAiY2hlY2siOiAiQzIiLAogICAibmFt
ZSI6ICJwaGFzZTJbaGV4X3N0ZXB8YV0uUzRfaCBhYnMgPD0gMWUtMDYiLAogICAibm90ZSI6ICIi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMC4wMTYyNDA4NTQxMDcyMzUxMSwK
ICAgImNoYXQiOiAwLjAxNjI0MDg1NDEwNzIzNTExLAogICAiY2hlY2siOiAiQzIiLAogICAibmFt
ZSI6ICJwaGFzZTJbaGV4X3N0ZXB8YV0uYmlyZWZfYjFfVlJIIGFicyA8PSAxZS0wNiIsCiAgICJu
b3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAyLjIxNDgyNjk0MTcx
NDY0M2UtMDcsCiAgICJjaGF0IjogMi4yMTQ4MjY5NDE3MTQ2NDNlLTA3LAogICAiY2hlY2siOiAi
QzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8YV0ua2FwcGE0NDRfRTIgcmVsIDw9IDAu
MDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwK
ICB7CiAgICJjYyI6IDAuMDAwMTYwNDA1MzQ2MTQzNjc5ODcsCiAgICJjaGF0IjogMC4wMDAxNjA0
MDUzNDYxNDM2Nzk4NywKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9z
dGVwfGFdLmthcHBhNDRfRTIgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDAuMDAwMTU5ODkzMDQ3Njg0
Mzc3LAogICAiY2hhdCI6IDAuMDAwMTU5ODkzMDQ3Njg0Mzc3LAogICAiY2hlY2siOiAiQzIiLAog
ICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8YV0ua2FwcGE0NF9FMl9IUyByZWwgPD0gMC4wMDAx
IChmbG9vciAxZS0wNikiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogLTcuNTA3NzM5NjYxOTcyMDA0ZS0wNiwKICAgImNoYXQiOiAtNy41MDc3Mzk2NjE5
NzIwMDRlLTA2LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8
YV0ua2FwcGE0NF9oIHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA4LjQyNDU4MjQxOTQwMzQ1NywKICAg
ImNoYXQiOiA4LjQyNDU4MjQxOTQwMzQ1NywKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAi
cGhhc2UyW2hleF9zdGVwfGFdLnZUX0hTX2hpIHJlbCA8PSAxZS0wNiAoZmxvb3IgMC4wKSIsCiAg
ICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA4LjM5MDg1OTcz
MTcyODI0NywKICAgImNoYXQiOiA4LjM5MDg1OTczMTcyODI0NywKICAgImNoZWNrIjogIkMyIiwK
ICAgIm5hbWUiOiAicGhhc2UyW2hleF9zdGVwfGFdLnZUX0hTX2xvIHJlbCA8PSAxZS0wNiAoZmxv
b3IgMC4wKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiA4LjQxOTA1OTYzNzU5MTYwMywKICAgImNoYXQiOiA4LjQxOTA1OTYzNzU5MTYwMywKICAgImNo
ZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9zdGVwfGFdLnZUX1ZSSCByZWwgPD0g
MWUtMDggKGZsb29yIDAuMCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAxLjYwNTU2OTUzNjUwNzU5MTJlLTA5LAogICAi
Y2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8YV0uaGFsdmluZ19kZXZf
a2FwcGE0NCAoY2hhdCkgPD0gbWF4KHJlbCp8a2FwcGE0NHwsIGZsb29yKSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxLjYwNTU2OTUzNjUwNzU5MTJl
LTA5LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MltoZXhfc3RlcHxhXS5oYWx2aW5nX2Rldl9rYXBwYTQ0IChjYykgPD0gbWF4KHJlbCp8a2FwcGE0
NHwsIGZsb29yKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiAtMC4wMDE0Mzk0NjkzMDIwMDMyOTAzLAogICAiY2hhdCI6IC0wLjAwMTQzOTQ2OTMwMjAw
MzI5MDMsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfc3RlcHxhXS5x
dWFkZm9ybS5rYXBwYTIyIHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAtMS4yNDg4NzkwNzMwNDkxODg3
ZS0wOCwKICAgImNoYXQiOiAtMS4yNDg4NzkwNzMwNDkxODg3ZS0wOCwKICAgImNoZWNrIjogIkMy
IiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9zdGVwfGFdLnF1YWRmb3JtLmthcHBhMjQgcmVsIDw9
IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6IDAuMDAwMTYwMzk5MDM3NjM5NDUzMTcsCiAgICJjaGF0IjogMC4wMDAx
NjAzOTkwMzc2Mzk0NTMxNywKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hl
eF9zdGVwfGFdLnF1YWRmb3JtLmthcHBhNDQgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwK
ICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAg
ICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9z
dGVwfGJdIHByZXNlbnQgYm90aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6IDEyLAogICAiY2hlY2siOiAiQzIiLAog
ICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8Yl0ubGFtYmRhX21lYW5fdDQgbGVuZ3RoIDEyIGJv
dGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBo
YXNlMltoZXhfc3RlcHxiXS5sYW1iZGFfbWVhbl90NCBlbGVtZW50d2lzZSA8PSAxZS0wNiIsCiAg
ICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhh
c2UyW2hleF9zdGVwfGJdLnJfYWdnX0UyX0hTIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90
ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQi
OiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8Yl0u
cl9hZ2dfRTJfSFMgZWxlbWVudHdpc2UgPD0gMWUtMDYiLAogICAibm90ZSI6ICJ3b3JzdCAwLjAw
MGUrMDAiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMTIsCiAgICJjaGF0Ijog
MTIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfc3RlcHxiXS5yX2Fn
Z19FMl9SIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRy
dWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAi
QzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8Yl0ucl9hZ2dfRTJfUiBlbGVtZW50d2lz
ZSA8PSAxZS0wNiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwK
ICAgIm5hbWUiOiAicGhhc2UyW2hleF9zdGVwfGJdLnJfYWdnX0UyX1YgbGVuZ3RoIDEyIGJvdGgg
bGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBu
dWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MltoZXhfc3RlcHxiXS5yX2FnZ19FMl9WIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUi
OiAid29yc3QgMC4wMDBlKzAwIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEy
LAogICAiY2hhdCI6IDEyLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4
X3N0ZXB8Yl0ucl9hZ2dfRTJfVlJIIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxs
LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8Yl0ucl9hZ2df
RTJfVlJIIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAid29yc3QgMC4wMDBlKzAw
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6IDEyLAog
ICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8Yl0ucl9hZ2dfaF9W
UkggbGVuZ3RoIDEyIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIs
CiAgICJuYW1lIjogInBoYXNlMltoZXhfc3RlcHxiXS5yX2FnZ19oX1ZSSCBlbGVtZW50d2lzZSA8
PSAxZS0wNiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiAtMi4xOTkwMjY4Mzg4MDc1OTg3ZS0xMywKICAgImNoYXQiOiAtMi4x
OTkwMjY4Mzg4MDc1OTg3ZS0xMywKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2Uy
W2hleF9zdGVwfGJdLlM0X0UyIGFicyA8PSAxZS0wNiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA3LjQ4NTg3MTY4MTIxNDcxNWUtMTQsCiAgICJjaGF0
IjogNy40ODU4NzE2ODEyMTQ3MTVlLTE0LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJw
aGFzZTJbaGV4X3N0ZXB8Yl0uUzRfaCBhYnMgPD0gMWUtMDYiLAogICAibm90ZSI6ICIiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMC4wMTYyNDE3OTc1NzcyMjgwNjMsCiAgICJj
aGF0IjogMC4wMTYyNDE3OTc1NzcyMjgwNjMsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjog
InBoYXNlMltoZXhfc3RlcHxiXS5iaXJlZl9iMV9WUkggYWJzIDw9IDFlLTA2IiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDIuMjE1ODQxMDc2MjgwODk3
NWUtMDcsCiAgICJjaGF0IjogMi4yMTU4NDEwNzYyODA4OTc1ZS0wNywKICAgImNoZWNrIjogIkMy
IiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9zdGVwfGJdLmthcHBhNDQ0X0UyIHJlbCA8PSAwLjAw
MDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiAwLjAwMDE2MDQxNDY2NTAzNDA4NTg4LAogICAiY2hhdCI6IDAuMDAwMTYwNDE0
NjY1MDM0MDg1ODgsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfc3Rl
cHxiXS5rYXBwYTQ0X0UyIHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAwLjAwMDE1OTkwMjU4NDkyMzM5
NjA2LAogICAiY2hhdCI6IDAuMDAwMTU5OTAyNTg0OTIzMzk2MDYsCiAgICJjaGVjayI6ICJDMiIs
CiAgICJuYW1lIjogInBoYXNlMltoZXhfc3RlcHxiXS5rYXBwYTQ0X0UyX0hTIHJlbCA8PSAwLjAw
MDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiAtNy41MDkwMTgxNjg4OTQ0MTdlLTA2LAogICAiY2hhdCI6IC03LjUwOTAxODE2
ODg5NDQxN2UtMDYsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfc3Rl
cHxiXS5rYXBwYTQ0X2ggcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAi
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDguNDI0ODAzMjU3NzIzODMyLAog
ICAiY2hhdCI6IDguNDI0ODAzMjU3NzIzODMyLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6
ICJwaGFzZTJbaGV4X3N0ZXB8Yl0udlRfSFNfaGkgcmVsIDw9IDFlLTA2IChmbG9vciAwLjApIiwK
ICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDguMzkxMDg0
NzQ2ODM3OTQ3LAogICAiY2hhdCI6IDguMzkxMDg0NzQ2ODM3OTQ3LAogICAiY2hlY2siOiAiQzIi
LAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8Yl0udlRfSFNfbG8gcmVsIDw9IDFlLTA2IChm
bG9vciAwLjApIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJj
YyI6IDguNDE5Mjc4NjQ4NTc5NjEyLAogICAiY2hhdCI6IDguNDE5Mjc4NjQ4NTc5NjEyLAogICAi
Y2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X3N0ZXB8Yl0udlRfVlJIIHJlbCA8
PSAxZS0wOCAoZmxvb3IgMC4wKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IDEuNjA2MTYxNjM1MDg5MTI3MmUtMDksCiAg
ICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfc3RlcHxiXS5oYWx2aW5nX2Rl
dl9rYXBwYTQ0IChjaGF0KSA8PSBtYXgocmVsKnxrYXBwYTQ0fCwgZmxvb3IpIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEuNjA2MTYxNjM1MDg5MTI3
MmUtMDksCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhh
c2UyW2hleF9zdGVwfGJdLmhhbHZpbmdfZGV2X2thcHBhNDQgKGNjKSA8PSBtYXgocmVsKnxrYXBw
YTQ0fCwgZmxvb3IpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAg
ICJjYyI6IC0wLjAwMTQzODcxMDI0Nzg4MzYwNiwKICAgImNoYXQiOiAtMC4wMDE0Mzg3MTAyNDc4
ODM2MDYsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfc3RlcHxiXS5x
dWFkZm9ybS5rYXBwYTIyIHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAtMS4yNDg0NjE1MDgzOTAxMjM2
ZS0wOCwKICAgImNoYXQiOiAtMS4yNDg0NjE1MDgzOTAxMjM2ZS0wOCwKICAgImNoZWNrIjogIkMy
IiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9zdGVwfGJdLnF1YWRmb3JtLmthcHBhMjQgcmVsIDw9
IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6IDAuMDAwMTYwNDA4MzU4MjM0NjU1MjUsCiAgICJjaGF0IjogMC4wMDAx
NjA0MDgzNTgyMzQ2NTUyNSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hl
eF9zdGVwfGJdLnF1YWRmb3JtLmthcHBhNDQgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwK
ICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAg
ICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9n
ZW04fGFdIHByZXNlbnQgYm90aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6IDEyLAogICAiY2hlY2siOiAiQzIiLAog
ICAibmFtZSI6ICJwaGFzZTJbaGV4X2dlbTh8YV0ubGFtYmRhX21lYW5fdDQgbGVuZ3RoIDEyIGJv
dGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBo
YXNlMltoZXhfZ2VtOHxhXS5sYW1iZGFfbWVhbl90NCBlbGVtZW50d2lzZSA8PSAxZS0wNiIsCiAg
ICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhh
c2UyW2hleF9nZW04fGFdLnJfYWdnX0UyX0hTIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90
ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQi
OiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X2dlbTh8YV0u
cl9hZ2dfRTJfSFMgZWxlbWVudHdpc2UgPD0gMWUtMDYiLAogICAibm90ZSI6ICJ3b3JzdCAwLjAw
MGUrMDAiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMTIsCiAgICJjaGF0Ijog
MTIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfZ2VtOHxhXS5yX2Fn
Z19FMl9SIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRy
dWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAi
QzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X2dlbTh8YV0ucl9hZ2dfRTJfUiBlbGVtZW50d2lz
ZSA8PSAxZS0wNiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwK
ICAgIm5hbWUiOiAicGhhc2UyW2hleF9nZW04fGFdLnJfYWdnX0UyX1YgbGVuZ3RoIDEyIGJvdGgg
bGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBu
dWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MltoZXhfZ2VtOHxhXS5yX2FnZ19FMl9WIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUi
OiAid29yc3QgMC4wMDBlKzAwIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEy
LAogICAiY2hhdCI6IDEyLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4
X2dlbTh8YV0ucl9hZ2dfRTJfVlJIIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxs
LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X2dlbTh8YV0ucl9hZ2df
RTJfVlJIIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAid29yc3QgMC4wMDBlKzAw
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6IDEyLAog
ICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X2dlbTh8YV0ucl9hZ2dfaF9W
UkggbGVuZ3RoIDEyIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIs
CiAgICJuYW1lIjogInBoYXNlMltoZXhfZ2VtOHxhXS5yX2FnZ19oX1ZSSCBlbGVtZW50d2lzZSA8
PSAxZS0wNiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiAtMi42NTIwNDYzNzQ1NTE0NjRlLTEzLAogICAiY2hhdCI6IC0yLjY1
MjA0NjM3NDU1MTQ2NGUtMTMsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMlto
ZXhfZ2VtOHxhXS5TNF9FMiBhYnMgPD0gMWUtMDYiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6
IHRydWUKICB9LAogIHsKICAgImNjIjogOC4zOTQ0MDgxOTk4NDQxODNlLTE0LAogICAiY2hhdCI6
IDguMzk0NDA4MTk5ODQ0MTgzZS0xNCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhh
c2UyW2hleF9nZW04fGFdLlM0X2ggYWJzIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAiIiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDAuMDE4MTc0ODgyNTExMTc3MzksCiAgICJjaGF0
IjogMC4wMTgxNzQ4ODI1MTExNzczOSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhh
c2UyW2hleF9nZW04fGFdLmJpcmVmX2IxX1ZSSCBhYnMgPD0gMWUtMDYiLAogICAibm90ZSI6ICIi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMi4xOTMxMDA5NzMyODI0ODIyZS0w
NywKICAgImNoYXQiOiAyLjE5MzEwMDk3MzI4MjQ4MjJlLTA3LAogICAiY2hlY2siOiAiQzIiLAog
ICAibmFtZSI6ICJwaGFzZTJbaGV4X2dlbTh8YV0ua2FwcGE0NDRfRTIgcmVsIDw9IDAuMDAwMSAo
Zmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAg
ICJjYyI6IDAuMDAwMTc5NTA3Mjk1Nzk0ODQxMTUsCiAgICJjaGF0IjogMC4wMDAxNzk1MDcyOTU3
OTQ4NDExNSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9nZW04fGFd
LmthcHBhNDRfRTIgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDAuMDAwMTc4OTMwNTg4NTcyNTc0NCwK
ICAgImNoYXQiOiAwLjAwMDE3ODkzMDU4ODU3MjU3NDQsCiAgICJjaGVjayI6ICJDMiIsCiAgICJu
YW1lIjogInBoYXNlMltoZXhfZ2VtOHxhXS5rYXBwYTQ0X0UyX0hTIHJlbCA8PSAwLjAwMDEgKGZs
b29yIDFlLTA2KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiAtNy43NTQ0MTQ4NDk0ODkyODhlLTA2LAogICAiY2hhdCI6IC03Ljc1NDQxNDg0OTQ4OTI4
OGUtMDYsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfZ2VtOHxhXS5r
YXBwYTQ0X2ggcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAg
InBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEwLjA1Mjc5Nzc1NDk0OTAzNywKICAgImNo
YXQiOiAxMC4wNTI3OTc3NTQ5NDkwMzcsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBo
YXNlMltoZXhfZ2VtOHxhXS52VF9IU19oaSByZWwgPD0gMWUtMDYgKGZsb29yIDAuMCkiLAogICAi
bm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogOS45OTA5MTMwMDE1
NzExNTYsCiAgICJjaGF0IjogOS45OTA5MTMwMDE1NzExNTYsCiAgICJjaGVjayI6ICJDMiIsCiAg
ICJuYW1lIjogInBoYXNlMltoZXhfZ2VtOHxhXS52VF9IU19sbyByZWwgPD0gMWUtMDYgKGZsb29y
IDAuMCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
MTAuMDQxNzIxODE3MzY5MTQ3LAogICAiY2hhdCI6IDEwLjA0MTcyMTgxNzM2OTE0NywKICAgImNo
ZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9nZW04fGFdLnZUX1ZSSCByZWwgPD0g
MWUtMDggKGZsb29yIDAuMCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAxLjk4MzYyNjkzMzIyOTM5NTNlLTA5LAogICAi
Y2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X2dlbTh8YV0uaGFsdmluZ19kZXZf
a2FwcGE0NCAoY2hhdCkgPD0gbWF4KHJlbCp8a2FwcGE0NHwsIGZsb29yKSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxLjk4MzYyNjkzMzIyOTM5NTNl
LTA5LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MltoZXhfZ2VtOHxhXS5oYWx2aW5nX2Rldl9rYXBwYTQ0IChjYykgPD0gbWF4KHJlbCp8a2FwcGE0
NHwsIGZsb29yKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiAtMC4wMDE4OTU2NTk5MDY5NDY4MjkzLAogICAiY2hhdCI6IC0wLjAwMTg5NTY1OTkwNjk0
NjgyOTMsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfZ2VtOHxhXS5x
dWFkZm9ybS5rYXBwYTIyIHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAtMS44MzcyMTM0MTc4NTE5NDNl
LTA4LAogICAiY2hhdCI6IC0xLjgzNzIxMzQxNzg1MTk0M2UtMDgsCiAgICJjaGVjayI6ICJDMiIs
CiAgICJuYW1lIjogInBoYXNlMltoZXhfZ2VtOHxhXS5xdWFkZm9ybS5rYXBwYTI0IHJlbCA8PSAw
LjAwMDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiAwLjAwMDE3OTQ5ODQyMjAyNTg2OTc2LAogICAiY2hhdCI6IDAuMDAwMTc5
NDk4NDIyMDI1ODY5NzYsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhf
Z2VtOHxhXS5xdWFkZm9ybS5rYXBwYTQ0IHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIsCiAg
ICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAi
Y2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfZ2Vt
OHxiXSBwcmVzZW50IGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwKICAg
Im5hbWUiOiAicGhhc2UyW2hleF9nZW04fGJdLmxhbWJkYV9tZWFuX3Q0IGxlbmd0aCAxMiBib3Ro
IGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
bnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFz
ZTJbaGV4X2dlbTh8Yl0ubGFtYmRhX21lYW5fdDQgZWxlbWVudHdpc2UgPD0gMWUtMDYiLAogICAi
bm90ZSI6ICJ3b3JzdCAwLjAwMGUrMDAiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogMTIsCiAgICJjaGF0IjogMTIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MltoZXhfZ2VtOHxiXS5yX2FnZ19FMl9IUyBsZW5ndGggMTIgYm90aCBsZWdzIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0Ijog
bnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9nZW04fGJdLnJf
YWdnX0UyX0hTIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAid29yc3QgMC4wMDBl
KzAwIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6IDEy
LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X2dlbTh8Yl0ucl9hZ2df
RTJfUiBsZW5ndGggMTIgYm90aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMy
IiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9nZW04fGJdLnJfYWdnX0UyX1IgZWxlbWVudHdpc2Ug
PD0gMWUtMDYiLAogICAibm90ZSI6ICJ3b3JzdCAwLjAwMGUrMDAiLAogICAicGFzcyI6IHRydWUK
ICB9LAogIHsKICAgImNjIjogMTIsCiAgICJjaGF0IjogMTIsCiAgICJjaGVjayI6ICJDMiIsCiAg
ICJuYW1lIjogInBoYXNlMltoZXhfZ2VtOHxiXS5yX2FnZ19FMl9WIGxlbmd0aCAxMiBib3RoIGxl
Z3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVs
bCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJb
aGV4X2dlbTh8Yl0ucl9hZ2dfRTJfViBlbGVtZW50d2lzZSA8PSAxZS0wNiIsCiAgICJub3RlIjog
IndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxMiwK
ICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9n
ZW04fGJdLnJfYWdnX0UyX1ZSSCBsZW5ndGggMTIgYm90aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwK
ICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9nZW04fGJdLnJfYWdnX0Uy
X1ZSSCBlbGVtZW50d2lzZSA8PSAxZS0wNiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAg
ImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9nZW04fGJdLnJfYWdnX2hfVlJI
IGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAog
ICAibmFtZSI6ICJwaGFzZTJbaGV4X2dlbTh8Yl0ucl9hZ2dfaF9WUkggZWxlbWVudHdpc2UgPD0g
MWUtMDYiLAogICAibm90ZSI6ICJ3b3JzdCAwLjAwMGUrMDAiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogLTIuNjY0NTQ0MTEyNjU2ODUxZS0xMywKICAgImNoYXQiOiAtMi42NjQ1
NDQxMTI2NTY4NTFlLTEzLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4
X2dlbTh8Yl0uUzRfRTIgYWJzIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0
cnVlCiAgfSwKICB7CiAgICJjYyI6IDguMjU2NzgxNDgzNDg0Mjk2ZS0xNCwKICAgImNoYXQiOiA4
LjI1Njc4MTQ4MzQ4NDI5NmUtMTQsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MltoZXhfZ2VtOHxiXS5TNF9oIGFicyA8PSAxZS0wNiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAwLjAxODE3NDI5NzEwOTM0MDgxMywKICAgImNoYXQi
OiAwLjAxODE3NDI5NzEwOTM0MDgxMywKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhh
c2UyW2hleF9nZW04fGJdLmJpcmVmX2IxX1ZSSCBhYnMgPD0gMWUtMDYiLAogICAibm90ZSI6ICIi
LAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMi4xOTIzNTU5NTY1MzY0MzI5ZS0w
NywKICAgImNoYXQiOiAyLjE5MjM1NTk1NjUzNjQzMjllLTA3LAogICAiY2hlY2siOiAiQzIiLAog
ICAibmFtZSI6ICJwaGFzZTJbaGV4X2dlbTh8Yl0ua2FwcGE0NDRfRTIgcmVsIDw9IDAuMDAwMSAo
Zmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAg
ICJjYyI6IDAuMDAwMTc5NTAxNTEzNTQ5MDU4NzYsCiAgICJjaGF0IjogMC4wMDAxNzk1MDE1MTM1
NDkwNTg3NiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9nZW04fGJd
LmthcHBhNDRfRTIgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDAuMDAwMTc4OTI0NzMwMzgzMzQ2NTMs
CiAgICJjaGF0IjogMC4wMDAxNzg5MjQ3MzAzODMzNDY1MywKICAgImNoZWNrIjogIkMyIiwKICAg
Im5hbWUiOiAicGhhc2UyW2hleF9nZW04fGJdLmthcHBhNDRfRTJfSFMgcmVsIDw9IDAuMDAwMSAo
Zmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAg
ICJjYyI6IC03Ljc1MzYzNTc0MzE0NDIwMWUtMDYsCiAgICJjaGF0IjogLTcuNzUzNjM1NzQzMTQ0
MjAxZS0wNiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9nZW04fGJd
LmthcHBhNDRfaCByZWwgPD0gMC4wMDAxIChmbG9vciAxZS0wNikiLAogICAibm90ZSI6ICIiLAog
ICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMTAuMDUyNjI5OTU5Mjk0OTQ1LAogICAi
Y2hhdCI6IDEwLjA1MjYyOTk1OTI5NDk0NSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAi
cGhhc2UyW2hleF9nZW04fGJdLnZUX0hTX2hpIHJlbCA8PSAxZS0wNiAoZmxvb3IgMC4wKSIsCiAg
ICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA5Ljk5MDczOTgy
OTcxOTg2LAogICAiY2hhdCI6IDkuOTkwNzM5ODI5NzE5ODYsCiAgICJjaGVjayI6ICJDMiIsCiAg
ICJuYW1lIjogInBoYXNlMltoZXhfZ2VtOHxiXS52VF9IU19sbyByZWwgPD0gMWUtMDYgKGZsb29y
IDAuMCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
MTAuMDQxNTU0MDg1MTYwNjMyLAogICAiY2hhdCI6IDEwLjA0MTU1NDA4NTE2MDYzMiwKICAgImNo
ZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9nZW04fGJdLnZUX1ZSSCByZWwgPD0g
MWUtMDggKGZsb29yIDAuMCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAxLjk4MzE3MDA2OTMyNjEzMjhlLTA5LAogICAi
Y2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbaGV4X2dlbTh8Yl0uaGFsdmluZ19kZXZf
a2FwcGE0NCAoY2hhdCkgPD0gbWF4KHJlbCp8a2FwcGE0NHwsIGZsb29yKSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxLjk4MzE3MDA2OTMyNjEzMjhl
LTA5LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MltoZXhfZ2VtOHxiXS5oYWx2aW5nX2Rldl9rYXBwYTQ0IChjYykgPD0gbWF4KHJlbCp8a2FwcGE0
NHwsIGZsb29yKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiAtMC4wMDE4OTYxNDg4OTI5OTM2NDk4LAogICAiY2hhdCI6IC0wLjAwMTg5NjE0ODg5Mjk5
MzY0OTgsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltoZXhfZ2VtOHxiXS5x
dWFkZm9ybS5rYXBwYTIyIHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAtMS44Mzc2MDc0OTkwNDk3Mzg4
ZS0wOCwKICAgImNoYXQiOiAtMS44Mzc2MDc0OTkwNDk3Mzg4ZS0wOCwKICAgImNoZWNrIjogIkMy
IiwKICAgIm5hbWUiOiAicGhhc2UyW2hleF9nZW04fGJdLnF1YWRmb3JtLmthcHBhMjQgcmVsIDw9
IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6IDAuMDAwMTc5NDkyNjM5NTAzNTMwNjIsCiAgICJjaGF0IjogMC4wMDAx
Nzk0OTI2Mzk1MDM1MzA2MiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2hl
eF9nZW04fGJdLnF1YWRmb3JtLmthcHBhNDQgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwK
ICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAg
ICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1Ymlj
X3N0ZXB8MDAxXSBwcmVzZW50IGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjog
dHJ1ZQogIH0sCiAgewogICAiY2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMy
IiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS5sYW1iZGFfbWVhbl90NCBsZW5n
dGggMTIgYm90aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5h
bWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS5sYW1iZGFfbWVhbl90NCBlbGVtZW50d2lzZSA8
PSAxZS0wNiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwKICAg
Im5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS5yX2FnZ19FMl9IUyBsZW5ndGggMTIgYm90
aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhh
c2UyW2N1YmljX3N0ZXB8MDAxXS5yX2FnZ19FMl9IUyBlbGVtZW50d2lzZSA8PSAxZS0wNiIsCiAg
ICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhh
c2UyW2N1YmljX3N0ZXB8MDAxXS5yX2FnZ19FMl9SIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAi
bm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNo
YXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfc3Rl
cHwwMDFdLnJfYWdnX0UyX1IgZWxlbWVudHdpc2UgPD0gMWUtMDYiLAogICAibm90ZSI6ICJ3b3Jz
dCAwLjAwMGUrMDAiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMTIsCiAgICJj
aGF0IjogMTIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVw
fDAwMV0ucl9hZ2dfRTJfViBsZW5ndGggMTIgYm90aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwKICAg
InBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAg
ImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS5yX2FnZ19F
Ml9WIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAid29yc3QgMC4wMDBlKzAwIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6IDEyLAogICAi
Y2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfc3RlcHwwMDFdLnJfYWdnX0Uy
X1ZSSCBsZW5ndGggMTIgYm90aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMy
IiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS5yX2FnZ19FMl9WUkggZWxlbWVu
dHdpc2UgPD0gMWUtMDYiLAogICAibm90ZSI6ICJ3b3JzdCAwLjAwMGUrMDAiLAogICAicGFzcyI6
IHRydWUKICB9LAogIHsKICAgImNjIjogMTIsCiAgICJjaGF0IjogMTIsCiAgICJjaGVjayI6ICJD
MiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDAwMV0ucl9hZ2dfaF9WUkggbGVuZ3Ro
IDEyIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewog
ICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1l
IjogInBoYXNlMltjdWJpY19zdGVwfDAwMV0ucl9hZ2dfaF9WUkggZWxlbWVudHdpc2UgPD0gMWUt
MDYiLAogICAibm90ZSI6ICJ3b3JzdCAwLjAwMGUrMDAiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogLTEuOTU0OTY3ODk0NjI2MDU5OGUtMTEsCiAgICJjaGF0IjogLTEuOTU0OTY3
ODk0NjI2MDU5OGUtMTEsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJp
Y19zdGVwfDAwMV0uUzRfRTIgYWJzIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IC0xLjE2OTQ4OTg2MTAzNzc1MThlLTExLAogICAiY2hh
dCI6IC0xLjE2OTQ4OTg2MTAzNzc1MThlLTExLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6
ICJwaGFzZTJbY3ViaWNfc3RlcHwwMDFdLlM0X2ggYWJzIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAi
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IC0wLjAzNzg5ODcwMzM5NTk4NjU0
LAogICAiY2hhdCI6IC0wLjAzNzg5ODcwMzM5NTk4NjU0LAogICAiY2hlY2siOiAiQzIiLAogICAi
bmFtZSI6ICJwaGFzZTJbY3ViaWNfc3RlcHwwMDFdLmJpcmVmX2IxX1ZSSCBhYnMgPD0gMWUtMDYi
LAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMi42MzMx
NjQyMzE2MDk5NjNlLTA2LAogICAiY2hhdCI6IDIuNjMzMTY0MjMxNjA5OTYzZS0wNiwKICAgImNo
ZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS5rYXBwYTQ0NF9F
MiByZWwgPD0gMC4wMDAxIChmbG9vciAxZS0wNikiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6
IHRydWUKICB9LAogIHsKICAgImNjIjogLTAuMDAwMzc0MzUyOTQxODE3NTY3NCwKICAgImNoYXQi
OiAtMC4wMDAzNzQzNTI5NDE4MTc1Njc0LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJw
aGFzZTJbY3ViaWNfc3RlcHwwMDFdLmthcHBhNDRfRTIgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUt
MDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IC0w
LjAwMDM4OTI2NDc0NTM1NTEzMjU1LAogICAiY2hhdCI6IC0wLjAwMDM4OTI2NDc0NTM1NTEzMjU1
LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfc3RlcHwwMDFdLmth
cHBhNDRfRTJfSFMgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IC0zLjgwMjgzMjc2NzM0NjA0ODRlLTA1
LAogICAiY2hhdCI6IC0zLjgwMjgzMjc2NzM0NjA0ODRlLTA1LAogICAiY2hlY2siOiAiQzIiLAog
ICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfc3RlcHwwMDFdLmthcHBhNDRfaCByZWwgPD0gMC4wMDAx
IChmbG9vciAxZS0wNikiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogNy44Njc5NTMwMDU5MDQ3NzUsCiAgICJjaGF0IjogNy44Njc5NTMwMDU5MDQ3NzUs
CiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDAwMV0udlRf
SFNfaGkgcmVsIDw9IDFlLTA2IChmbG9vciAwLjApIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDcuNzU4NjE0NDkwMjExMDg3LAogICAiY2hhdCI6IDcu
NzU4NjE0NDkwMjExMDg3LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3Vi
aWNfc3RlcHwwMDFdLnZUX0hTX2xvIHJlbCA8PSAxZS0wNiAoZmxvb3IgMC4wKSIsCiAgICJub3Rl
IjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA3Ljc5OTA0NjM3NTg0NDky
MywKICAgImNoYXQiOiA3Ljc5OTA0NjM3NTg0NDkyMywKICAgImNoZWNrIjogIkMyIiwKICAgIm5h
bWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS52VF9WUkggcmVsIDw9IDFlLTA4IChmbG9vciAw
LjApIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51
bGwsCiAgICJjaGF0IjogMy44ODE0MTI2ODQzODQ5OTU2ZS0wOCwKICAgImNoZWNrIjogIkMyIiwK
ICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS5oYWx2aW5nX2Rldl9rYXBwYTQ0IChj
aGF0KSA8PSBtYXgocmVsKnxrYXBwYTQ0fCwgZmxvb3IpIiwKICAgIm5vdGUiOiAiIiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDMuODgxNDEyNjg0Mzg0OTk1NmUtMDgsCiAgICJj
aGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0
ZXB8MDAxXS5oYWx2aW5nX2Rldl9rYXBwYTQ0IChjYykgPD0gbWF4KHJlbCp8a2FwcGE0NHwsIGZs
b29yKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA0
LjQ4MTkxMTA3NjM2MTA5ZS0wOSwKICAgImNoYXQiOiA0LjQ4MTkxMTA3NjM2MTA5ZS0wOSwKICAg
ImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MDAxXS5xdWFkZm9y
bS5rYXBwYTIyIHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjogIiIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxLjk3NDA0MzM3NDk4NjA3NmUtMDcsCiAg
ICJjaGF0IjogMS45NzQwNDMzNzQ5ODYwNzZlLTA3LAogICAiY2hlY2siOiAiQzIiLAogICAibmFt
ZSI6ICJwaGFzZTJbY3ViaWNfc3RlcHwwMDFdLnF1YWRmb3JtLmthcHBhMjQgcmVsIDw9IDAuMDAw
MSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IC0wLjAwMDM3NDM1NDU1OTM5MTA2MTY2LAogICAiY2hhdCI6IC0wLjAwMDM3NDM1
NDU1OTM5MTA2MTY2LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNf
c3RlcHwwMDFdLnF1YWRmb3JtLmthcHBhNDQgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwK
ICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAg
ICJjaGF0IjogNC40ODE5MTEwNzYzNjEwOWUtMDksCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1l
IjogInBoYXNlMltjdWJpY19zdGVwfDAwMV0ucXVhZGZvcm0ua2FwcGEyMiAoY2hhdCkgY3ViaWMg
bnVsbCBhYnMgPD0gMWUtMTAiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IGZhbHNlCiAgfSwK
ICB7CiAgICJjYyI6IDQuNDgxOTExMDc2MzYxMDllLTA5LAogICAiY2hhdCI6IG51bGwsCiAgICJj
aGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDAwMV0ucXVhZGZvcm0u
a2FwcGEyMiAoY2MpIGN1YmljIG51bGwgYWJzIDw9IDFlLTEwIiwKICAgIm5vdGUiOiAiIiwKICAg
InBhc3MiOiBmYWxzZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IDEuOTc0MDQz
Mzc0OTg2MDc2ZS0wNywKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1Ymlj
X3N0ZXB8MDAxXS5xdWFkZm9ybS5rYXBwYTI0IChjaGF0KSBjdWJpYyBudWxsIGFicyA8PSAxZS0x
MCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogZmFsc2UKICB9LAogIHsKICAgImNjIjogMS45
NzQwNDMzNzQ5ODYwNzZlLTA3LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAg
ICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDAwMV0ucXVhZGZvcm0ua2FwcGEyNCAoY2MpIGN1
YmljIG51bGwgYWJzIDw9IDFlLTEwIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiBmYWxzZQog
IH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIs
CiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDExMV0gcHJlc2VudCBib3RoIGxlZ3MiLAog
ICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMTIsCiAgICJj
aGF0IjogMTIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVw
fDExMV0ubGFtYmRhX21lYW5fdDQgbGVuZ3RoIDEyIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGws
CiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDExMV0ubGFt
YmRhX21lYW5fdDQgZWxlbWVudHdpc2UgPD0gMWUtMDYiLAogICAibm90ZSI6ICJ3b3JzdCAwLjAw
MGUrMDAiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMTIsCiAgICJjaGF0Ijog
MTIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDExMV0u
cl9hZ2dfRTJfSFMgbGVuZ3RoIDEyIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVj
ayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDExMV0ucl9hZ2dfRTJfSFMg
ZWxlbWVudHdpc2UgPD0gMWUtMDYiLAogICAibm90ZSI6ICJ3b3JzdCAwLjAwMGUrMDAiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMTIsCiAgICJjaGF0IjogMTIsCiAgICJjaGVj
ayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDExMV0ucl9hZ2dfRTJfUiBs
ZW5ndGggMTIgYm90aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwK
ICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAg
Im5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MTExXS5yX2FnZ19FMl9SIGVsZW1lbnR3aXNlIDw9
IDFlLTA2IiwKICAgIm5vdGUiOiAid29yc3QgMC4wMDBlKzAwIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6IDEyLAogICAiY2hlY2siOiAiQzIiLAogICAi
bmFtZSI6ICJwaGFzZTJbY3ViaWNfc3RlcHwxMTFdLnJfYWdnX0UyX1YgbGVuZ3RoIDEyIGJvdGgg
bGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBu
dWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MltjdWJpY19zdGVwfDExMV0ucl9hZ2dfRTJfViBlbGVtZW50d2lzZSA8PSAxZS0wNiIsCiAgICJu
b3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2Uy
W2N1YmljX3N0ZXB8MTExXS5yX2FnZ19FMl9WUkggbGVuZ3RoIDEyIGJvdGggbGVncyIsCiAgICJu
b3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hh
dCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVw
fDExMV0ucl9hZ2dfRTJfVlJIIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAid29y
c3QgMC4wMDBlKzAwIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAi
Y2hhdCI6IDEyLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfc3Rl
cHwxMTFdLnJfYWdnX2hfVlJIIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAog
ICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAog
ICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfc3RlcHwxMTFdLnJfYWdn
X2hfVlJIIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAid29yc3QgMC4wMDBlKzAw
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEuMzAzNTQxNjQwNTgzMzM0NGUt
MTEsCiAgICJjaGF0IjogMS4zMDM1NDE2NDA1ODMzMzQ0ZS0xMSwKICAgImNoZWNrIjogIkMyIiwK
ICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MTExXS5TNF9FMiBhYnMgPD0gMWUtMDYiLAog
ICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogLTEuMTY5NDg5
ODYxMDM3NzUxOGUtMTEsCiAgICJjaGF0IjogLTEuMTY5NDg5ODYxMDM3NzUxOGUtMTEsCiAgICJj
aGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDExMV0uUzRfaCBhYnMg
PD0gMWUtMDYiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogLTAuMDM3ODk4NzAzMzk1OTg2NTQsCiAgICJjaGF0IjogLTAuMDM3ODk4NzAzMzk1OTg2NTQs
CiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDExMV0uYmly
ZWZfYjFfVlJIIGFicyA8PSAxZS0wNiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiAtMS43NTU0NDI4NjAwODcwNzY5ZS0wNiwKICAgImNoYXQiOiAtMS43
NTU0NDI4NjAwODcwNzY5ZS0wNiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2Uy
W2N1YmljX3N0ZXB8MTExXS5rYXBwYTQ0NF9FMiByZWwgPD0gMC4wMDAxIChmbG9vciAxZS0wNiki
LAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMC4wMDAy
NDk1Njg2Mjc4NzcyNDExNywKICAgImNoYXQiOiAwLjAwMDI0OTU2ODYyNzg3NzI0MTE3LAogICAi
Y2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfc3RlcHwxMTFdLmthcHBhNDRf
RTIgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDAuMDAwMjU5NTA5ODMwMjM4MDU4MjYsCiAgICJjaGF0
IjogMC4wMDAyNTk1MDk4MzAyMzgwNTgyNiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAi
cGhhc2UyW2N1YmljX3N0ZXB8MTExXS5rYXBwYTQ0X0UyX0hTIHJlbCA8PSAwLjAwMDEgKGZsb29y
IDFlLTA2KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2Mi
OiAtMy44MDI4MzI3NjczNDYwNDg0ZS0wNSwKICAgImNoYXQiOiAtMy44MDI4MzI3NjczNDYwNDg0
ZS0wNSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MTEx
XS5rYXBwYTQ0X2ggcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwK
ICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDcuODY3OTUzMDA1OTA0Nzc1LAogICAi
Y2hhdCI6IDcuODY3OTUzMDA1OTA0Nzc1LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJw
aGFzZTJbY3ViaWNfc3RlcHwxMTFdLnZUX0hTX2hpIHJlbCA8PSAxZS0wNiAoZmxvb3IgMC4wKSIs
CiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA3Ljc1ODYx
NDQ5MDIxMTA4NywKICAgImNoYXQiOiA3Ljc1ODYxNDQ5MDIxMTA4NywKICAgImNoZWNrIjogIkMy
IiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MTExXS52VF9IU19sbyByZWwgPD0gMWUt
MDYgKGZsb29yIDAuMCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsK
ICAgImNjIjogNy43OTkwNDYzNzU4NDQ5MjMsCiAgICJjaGF0IjogNy43OTkwNDYzNzU4NDQ5MjMs
CiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDExMV0udlRf
VlJIIHJlbCA8PSAxZS0wOCAoZmxvb3IgMC4wKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjog
dHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IDIuNTg3NjA2MTA5Nzk3NDFl
LTA4LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfc3RlcHwxMTFd
LmhhbHZpbmdfZGV2X2thcHBhNDQgKGNoYXQpIDw9IG1heChyZWwqfGthcHBhNDR8LCBmbG9vciki
LAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMi41ODc2
MDYxMDk3OTc0MWUtMDgsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5h
bWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MTExXS5oYWx2aW5nX2Rldl9rYXBwYTQ0IChjYykgPD0g
bWF4KHJlbCp8a2FwcGE0NHwsIGZsb29yKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1
ZQogIH0sCiAgewogICAiY2MiOiAtMi45ODc5Mzg4MzAyNzE5OGUtMDksCiAgICJjaGF0IjogLTIu
OTg3OTM4ODMwMjcxOThlLTA5LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJb
Y3ViaWNfc3RlcHwxMTFdLnF1YWRmb3JtLmthcHBhMjIgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUt
MDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEu
OTc0MDQzMzg3MDY1MTcyNGUtMDcsCiAgICJjaGF0IjogMS45NzQwNDMzODcwNjUxNzI0ZS0wNywK
ICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX3N0ZXB8MTExXS5xdWFk
Zm9ybS5rYXBwYTI0IHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjogIiIs
CiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAwLjAwMDI0OTU2OTcwNjI1NzQ1MjA0
LAogICAiY2hhdCI6IDAuMDAwMjQ5NTY5NzA2MjU3NDUyMDQsCiAgICJjaGVjayI6ICJDMiIsCiAg
ICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDExMV0ucXVhZGZvcm0ua2FwcGE0NCByZWwgPD0g
MC4wMDAxIChmbG9vciAxZS0wNikiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiAtMi45ODc5Mzg4MzAyNzE5OGUtMDksCiAg
ICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDExMV0ucXVhZGZv
cm0ua2FwcGEyMiAoY2hhdCkgY3ViaWMgbnVsbCBhYnMgPD0gMWUtMTAiLAogICAibm90ZSI6ICIi
LAogICAicGFzcyI6IGZhbHNlCiAgfSwKICB7CiAgICJjYyI6IC0yLjk4NzkzODgzMDI3MTk4ZS0w
OSwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJb
Y3ViaWNfc3RlcHwxMTFdLnF1YWRmb3JtLmthcHBhMjIgKGNjKSBjdWJpYyBudWxsIGFicyA8PSAx
ZS0xMCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogZmFsc2UKICB9LAogIHsKICAgImNjIjog
bnVsbCwKICAgImNoYXQiOiAxLjk3NDA0MzM4NzA2NTE3MjRlLTA3LAogICAiY2hlY2siOiAiQzIi
LAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfc3RlcHwxMTFdLnF1YWRmb3JtLmthcHBhMjQgKGNo
YXQpIGN1YmljIG51bGwgYWJzIDw9IDFlLTEwIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiBm
YWxzZQogIH0sCiAgewogICAiY2MiOiAxLjk3NDA0MzM4NzA2NTE3MjRlLTA3LAogICAiY2hhdCI6
IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19zdGVwfDEx
MV0ucXVhZGZvcm0ua2FwcGEyNCAoY2MpIGN1YmljIG51bGwgYWJzIDw9IDFlLTEwIiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiBmYWxzZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hh
dCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19nZW04
fDAwMV0gcHJlc2VudCBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUK
ICB9LAogIHsKICAgImNjIjogMTIsCiAgICJjaGF0IjogMTIsCiAgICJjaGVjayI6ICJDMiIsCiAg
ICJuYW1lIjogInBoYXNlMltjdWJpY19nZW04fDAwMV0ubGFtYmRhX21lYW5fdDQgbGVuZ3RoIDEy
IGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAi
Y2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjog
InBoYXNlMltjdWJpY19nZW04fDAwMV0ubGFtYmRhX21lYW5fdDQgZWxlbWVudHdpc2UgPD0gMWUt
MDYiLAogICAibm90ZSI6ICJ3b3JzdCAwLjAwMGUrMDAiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogMTIsCiAgICJjaGF0IjogMTIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1l
IjogInBoYXNlMltjdWJpY19nZW04fDAwMV0ucl9hZ2dfRTJfSFMgbGVuZ3RoIDEyIGJvdGggbGVn
cyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxs
LAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltj
dWJpY19nZW04fDAwMV0ucl9hZ2dfRTJfSFMgZWxlbWVudHdpc2UgPD0gMWUtMDYiLAogICAibm90
ZSI6ICJ3b3JzdCAwLjAwMGUrMDAiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjog
MTIsCiAgICJjaGF0IjogMTIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltj
dWJpY19nZW04fDAwMV0ucl9hZ2dfRTJfUiBsZW5ndGggMTIgYm90aCBsZWdzIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0Ijog
bnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8MDAx
XS5yX2FnZ19FMl9SIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAid29yc3QgMC4w
MDBlKzAwIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6
IDEyLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwwMDFd
LnJfYWdnX0UyX1YgbGVuZ3RoIDEyIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNz
IjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVj
ayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19nZW04fDAwMV0ucl9hZ2dfRTJfViBl
bGVtZW50d2lzZSA8PSAxZS0wNiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJw
YXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNr
IjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8MDAxXS5yX2FnZ19FMl9WUkgg
bGVuZ3RoIDEyIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAg
ICJuYW1lIjogInBoYXNlMltjdWJpY19nZW04fDAwMV0ucl9hZ2dfRTJfVlJIIGVsZW1lbnR3aXNl
IDw9IDFlLTA2IiwKICAgIm5vdGUiOiAid29yc3QgMC4wMDBlKzAwIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6IDEyLAogICAiY2hlY2siOiAiQzIiLAog
ICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwwMDFdLnJfYWdnX2hfVlJIIGxlbmd0aCAxMiBi
b3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJw
aGFzZTJbY3ViaWNfZ2VtOHwwMDFdLnJfYWdnX2hfVlJIIGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwK
ICAgIm5vdGUiOiAid29yc3QgMC4wMDBlKzAwIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAg
ICJjYyI6IC00LjI2NzE2ODIyOTAyMTg5NmUtMTEsCiAgICJjaGF0IjogLTQuMjY3MTY4MjI5MDIx
ODk2ZS0xMSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8
MDAxXS5TNF9FMiBhYnMgPD0gMWUtMDYiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUK
ICB9LAogIHsKICAgImNjIjogLTIuMzg1MjgxNzM0Nzg5ODA5ZS0xMSwKICAgImNoYXQiOiAtMi4z
ODUyODE3MzQ3ODk4MDllLTExLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJb
Y3ViaWNfZ2VtOHwwMDFdLlM0X2ggYWJzIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAiIiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IC0wLjA0NTQ4MTI1MjIyNzc0OTI0LAogICAiY2hh
dCI6IC0wLjA0NTQ4MTI1MjIyNzc0OTI0LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJw
aGFzZTJbY3ViaWNfZ2VtOHwwMDFdLmJpcmVmX2IxX1ZSSCBhYnMgPD0gMWUtMDYiLAogICAibm90
ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMy43OTU4NDY2NTU2MjYw
Mjc3ZS0wNiwKICAgImNoYXQiOiAzLjc5NTg0NjY1NTYyNjAyNzdlLTA2LAogICAiY2hlY2siOiAi
QzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwwMDFdLmthcHBhNDQ0X0UyIHJlbCA8
PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQog
IH0sCiAgewogICAiY2MiOiAtMC4wMDA0NDkyNzcwOTM0Mjk2MTY5LAogICAiY2hhdCI6IC0wLjAw
MDQ0OTI3NzA5MzQyOTYxNjksCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltj
dWJpY19nZW04fDAwMV0ua2FwcGE0NF9FMiByZWwgPD0gMC4wMDAxIChmbG9vciAxZS0wNikiLAog
ICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogLTAuMDAwNDc2
NzE1MTk1MDQyMzA3NCwKICAgImNoYXQiOiAtMC4wMDA0NzY3MTUxOTUwNDIzMDc0LAogICAiY2hl
Y2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwwMDFdLmthcHBhNDRfRTJf
SFMgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IC00LjUzNTc4MjI2NjI0ODkxM2UtMDUsCiAgICJjaGF0
IjogLTQuNTM1NzgyMjY2MjQ4OTEzZS0wNSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAi
cGhhc2UyW2N1YmljX2dlbTh8MDAxXS5rYXBwYTQ0X2ggcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUt
MDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDku
NDU2ODU0OTg0NTg4NzM4LAogICAiY2hhdCI6IDkuNDU2ODU0OTg0NTg4NzM4LAogICAiY2hlY2si
OiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwwMDFdLnZUX0hTX2hpIHJlbCA8
PSAxZS0wNiAoZmxvb3IgMC4wKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiA5LjIxMTcyMTA2NDM3MDg2MSwKICAgImNoYXQiOiA5LjIxMTcyMTA2NDM3
MDg2MSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8MDAx
XS52VF9IU19sbyByZWwgPD0gMWUtMDYgKGZsb29yIDAuMCkiLAogICAibm90ZSI6ICIiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogOS4zMDc4OTkwNzY1MzMxNzksCiAgICJjaGF0
IjogOS4zMDc4OTkwNzY1MzMxNzksCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNl
MltjdWJpY19nZW04fDAwMV0udlRfVlJIIHJlbCA8PSAxZS0wOCAoZmxvb3IgMC4wKSIsCiAgICJu
b3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hh
dCI6IDYuODk2NjEyNTg4OTA3NDk0ZS0wOCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAi
cGhhc2UyW2N1YmljX2dlbTh8MDAxXS5oYWx2aW5nX2Rldl9rYXBwYTQ0IChjaGF0KSA8PSBtYXgo
cmVsKnxrYXBwYTQ0fCwgZmxvb3IpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6IDYuODk2NjEyNTg4OTA3NDk0ZS0wOCwKICAgImNoYXQiOiBudWxsLAog
ICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwwMDFdLmhhbHZp
bmdfZGV2X2thcHBhNDQgKGNjKSA8PSBtYXgocmVsKnxrYXBwYTQ0fCwgZmxvb3IpIiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDcuOTYzNzU3OTMzMzY3
Nzk5ZS0wOSwKICAgImNoYXQiOiA3Ljk2Mzc1NzkzMzM2Nzc5OWUtMDksCiAgICJjaGVjayI6ICJD
MiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19nZW04fDAwMV0ucXVhZGZvcm0ua2FwcGEyMiBy
ZWwgPD0gMC4wMDAxIChmbG9vciAxZS0wNikiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRy
dWUKICB9LAogIHsKICAgImNjIjogMy40Nzc4NTcyNDYyODE0NDE0ZS0wNywKICAgImNoYXQiOiAz
LjQ3Nzg1NzI0NjI4MTQ0MTRlLTA3LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFz
ZTJbY3ViaWNfZ2VtOHwwMDFdLnF1YWRmb3JtLmthcHBhMjQgcmVsIDw9IDAuMDAwMSAoZmxvb3Ig
MWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
IC0wLjAwMDQ0OTI3OTk2NzYwNDIyNjg1LAogICAiY2hhdCI6IC0wLjAwMDQ0OTI3OTk2NzYwNDIy
Njg1LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwwMDFd
LnF1YWRmb3JtLmthcHBhNDQgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0Ijog
Ny45NjM3NTc5MzMzNjc3OTllLTA5LAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFz
ZTJbY3ViaWNfZ2VtOHwwMDFdLnF1YWRmb3JtLmthcHBhMjIgKGNoYXQpIGN1YmljIG51bGwgYWJz
IDw9IDFlLTEwIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiBmYWxzZQogIH0sCiAgewogICAi
Y2MiOiA3Ljk2Mzc1NzkzMzM2Nzc5OWUtMDksCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjog
IkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8MDAxXS5xdWFkZm9ybS5rYXBwYTIy
IChjYykgY3ViaWMgbnVsbCBhYnMgPD0gMWUtMTAiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6
IGZhbHNlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogMy40Nzc4NTcyNDYyODE0
NDE0ZS0wNywKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8
MDAxXS5xdWFkZm9ybS5rYXBwYTI0IChjaGF0KSBjdWJpYyBudWxsIGFicyA8PSAxZS0xMCIsCiAg
ICJub3RlIjogIiIsCiAgICJwYXNzIjogZmFsc2UKICB9LAogIHsKICAgImNjIjogMy40Nzc4NTcy
NDYyODE0NDE0ZS0wNywKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFt
ZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwwMDFdLnF1YWRmb3JtLmthcHBhMjQgKGNjKSBjdWJpYyBu
dWxsIGFicyA8PSAxZS0xMCIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogZmFsc2UKICB9LAog
IHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAi
bmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFdIHByZXNlbnQgYm90aCBsZWdzIiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6
IDEyLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFd
LmxhbWJkYV9tZWFuX3Q0IGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAi
cGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAi
Y2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFdLmxhbWJkYV9t
ZWFuX3Q0IGVsZW1lbnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAid29yc3QgMC4wMDBlKzAw
IiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6IDEyLAog
ICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFdLnJfYWdn
X0UyX0hTIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRy
dWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAi
QzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFdLnJfYWdnX0UyX0hTIGVsZW1l
bnR3aXNlIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAid29yc3QgMC4wMDBlKzAwIiwKICAgInBhc3Mi
OiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDEyLAogICAiY2hhdCI6IDEyLAogICAiY2hlY2siOiAi
QzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFdLnJfYWdnX0UyX1IgbGVuZ3Ro
IDEyIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewog
ICAiY2MiOiBudWxsLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1l
IjogInBoYXNlMltjdWJpY19nZW04fDExMV0ucl9hZ2dfRTJfUiBlbGVtZW50d2lzZSA8PSAxZS0w
NiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiAxMiwKICAgImNoYXQiOiAxMiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUi
OiAicGhhc2UyW2N1YmljX2dlbTh8MTExXS5yX2FnZ19FMl9WIGxlbmd0aCAxMiBib3RoIGxlZ3Mi
LAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwK
ICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3Vi
aWNfZ2VtOHwxMTFdLnJfYWdnX0UyX1YgZWxlbWVudHdpc2UgPD0gMWUtMDYiLAogICAibm90ZSI6
ICJ3b3JzdCAwLjAwMGUrMDAiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMTIs
CiAgICJjaGF0IjogMTIsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJp
Y19nZW04fDExMV0ucl9hZ2dfRTJfVlJIIGxlbmd0aCAxMiBib3RoIGxlZ3MiLAogICAibm90ZSI6
ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiBu
dWxsLAogICAiY2hlY2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFd
LnJfYWdnX0UyX1ZSSCBlbGVtZW50d2lzZSA8PSAxZS0wNiIsCiAgICJub3RlIjogIndvcnN0IDAu
MDAwZSswMCIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAxMiwKICAgImNoYXQi
OiAxMiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8MTEx
XS5yX2FnZ19oX1ZSSCBsZW5ndGggMTIgYm90aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNo
ZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8MTExXS5yX2FnZ19oX1ZS
SCBlbGVtZW50d2lzZSA8PSAxZS0wNiIsCiAgICJub3RlIjogIndvcnN0IDAuMDAwZSswMCIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAyLjg0NDc2OTc2NDAxNzk4NzZlLTExLAog
ICAiY2hhdCI6IDIuODQ0NzY5NzY0MDE3OTg3NmUtMTEsCiAgICJjaGVjayI6ICJDMiIsCiAgICJu
YW1lIjogInBoYXNlMltjdWJpY19nZW04fDExMV0uUzRfRTIgYWJzIDw9IDFlLTA2IiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IC0yLjM4NTI4MTczNDc4
OTgwOWUtMTEsCiAgICJjaGF0IjogLTIuMzg1MjgxNzM0Nzg5ODA5ZS0xMSwKICAgImNoZWNrIjog
IkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8MTExXS5TNF9oIGFicyA8PSAxZS0w
NiIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAtMC4w
NDU0ODEyNTIyMjc3NDkyNCwKICAgImNoYXQiOiAtMC4wNDU0ODEyNTIyMjc3NDkyNCwKICAgImNo
ZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8MTExXS5iaXJlZl9iMV9W
UkggYWJzIDw9IDFlLTA2IiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7
CiAgICJjYyI6IC0yLjUzMDU2NDQxOTA1ODMyNmUtMDYsCiAgICJjaGF0IjogLTIuNTMwNTY0NDE5
MDU4MzI2ZS0wNiwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dl
bTh8MTExXS5rYXBwYTQ0NF9FMiByZWwgPD0gMC4wMDAxIChmbG9vciAxZS0wNikiLAogICAibm90
ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogMC4wMDAyOTk1MTgwNjIy
ODg4NzA4NywKICAgImNoYXQiOiAwLjAwMDI5OTUxODA2MjI4ODg3MDg3LAogICAiY2hlY2siOiAi
QzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFdLmthcHBhNDRfRTIgcmVsIDw9
IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAg
fSwKICB7CiAgICJjYyI6IDAuMDAwMzE3ODEwMTMwMDI0OTcwNjMsCiAgICJjaGF0IjogMC4wMDAz
MTc4MTAxMzAwMjQ5NzA2MywKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1
YmljX2dlbTh8MTExXS5rYXBwYTQ0X0UyX0hTIHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIs
CiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAtNC41MzU3
ODIyNjYyNDg5MTNlLTA1LAogICAiY2hhdCI6IC00LjUzNTc4MjI2NjI0ODkxM2UtMDUsCiAgICJj
aGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19nZW04fDExMV0ua2FwcGE0NF9o
IHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjog
dHJ1ZQogIH0sCiAgewogICAiY2MiOiA5LjQ1Njg1NDk4NDU4ODczOCwKICAgImNoYXQiOiA5LjQ1
Njg1NDk4NDU4ODczOCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1Ymlj
X2dlbTh8MTExXS52VF9IU19oaSByZWwgPD0gMWUtMDYgKGZsb29yIDAuMCkiLAogICAibm90ZSI6
ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogOS4yMTE3MjEwNjQzNzA4NjEs
CiAgICJjaGF0IjogOS4yMTE3MjEwNjQzNzA4NjEsCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1l
IjogInBoYXNlMltjdWJpY19nZW04fDExMV0udlRfSFNfbG8gcmVsIDw9IDFlLTA2IChmbG9vciAw
LjApIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDku
MzA3ODk5MDc2NTMzMTc5LAogICAiY2hhdCI6IDkuMzA3ODk5MDc2NTMzMTc5LAogICAiY2hlY2si
OiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFdLnZUX1ZSSCByZWwgPD0g
MWUtMDggKGZsb29yIDAuMCkiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAog
IHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiA0LjU5Nzc0MzU2NDcyODk1MWUtMDgsCiAgICJj
aGVjayI6ICJDMiIsCiAgICJuYW1lIjogInBoYXNlMltjdWJpY19nZW04fDExMV0uaGFsdmluZ19k
ZXZfa2FwcGE0NCAoY2hhdCkgPD0gbWF4KHJlbCp8a2FwcGE0NHwsIGZsb29yKSIsCiAgICJub3Rl
IjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiA0LjU5Nzc0MzU2NDcyODk1
MWUtMDgsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhh
c2UyW2N1YmljX2dlbTh8MTExXS5oYWx2aW5nX2Rldl9rYXBwYTQ0IChjYykgPD0gbWF4KHJlbCp8
a2FwcGE0NHwsIGZsb29yKSIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAg
ewogICAiY2MiOiAtNS4zMDkxNzM4MzY0NTMwNzM0ZS0wOSwKICAgImNoYXQiOiAtNS4zMDkxNzM4
MzY0NTMwNzM0ZS0wOSwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1Ymlj
X2dlbTh8MTExXS5xdWFkZm9ybS5rYXBwYTIyIHJlbCA8PSAwLjAwMDEgKGZsb29yIDFlLTA2KSIs
CiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAzLjQ3Nzg1
NzIzODQ2NTQyOGUtMDcsCiAgICJjaGF0IjogMy40Nzc4NTcyMzg0NjU0MjhlLTA3LAogICAiY2hl
Y2siOiAiQzIiLAogICAibmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFdLnF1YWRmb3JtLmth
cHBhMjQgcmVsIDw9IDAuMDAwMSAoZmxvb3IgMWUtMDYpIiwKICAgIm5vdGUiOiAiIiwKICAgInBh
c3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IDAuMDAwMjk5NTE5OTc4NDAzODEyOSwKICAgImNo
YXQiOiAwLjAwMDI5OTUxOTk3ODQwMzgxMjksCiAgICJjaGVjayI6ICJDMiIsCiAgICJuYW1lIjog
InBoYXNlMltjdWJpY19nZW04fDExMV0ucXVhZGZvcm0ua2FwcGE0NCByZWwgPD0gMC4wMDAxIChm
bG9vciAxZS0wNikiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAg
ImNjIjogbnVsbCwKICAgImNoYXQiOiAtNS4zMDkxNzM4MzY0NTMwNzM0ZS0wOSwKICAgImNoZWNr
IjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8MTExXS5xdWFkZm9ybS5rYXBw
YTIyIChjaGF0KSBjdWJpYyBudWxsIGFicyA8PSAxZS0xMCIsCiAgICJub3RlIjogIiIsCiAgICJw
YXNzIjogZmFsc2UKICB9LAogIHsKICAgImNjIjogLTUuMzA5MTczODM2NDUzMDczNGUtMDksCiAg
ICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1Ymlj
X2dlbTh8MTExXS5xdWFkZm9ybS5rYXBwYTIyIChjYykgY3ViaWMgbnVsbCBhYnMgPD0gMWUtMTAi
LAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IGZhbHNlCiAgfSwKICB7CiAgICJjYyI6IG51bGws
CiAgICJjaGF0IjogMy40Nzc4NTcyMzg0NjU0MjhlLTA3LAogICAiY2hlY2siOiAiQzIiLAogICAi
bmFtZSI6ICJwaGFzZTJbY3ViaWNfZ2VtOHwxMTFdLnF1YWRmb3JtLmthcHBhMjQgKGNoYXQpIGN1
YmljIG51bGwgYWJzIDw9IDFlLTEwIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiBmYWxzZQog
IH0sCiAgewogICAiY2MiOiAzLjQ3Nzg1NzIzODQ2NTQyOGUtMDcsCiAgICJjaGF0IjogbnVsbCwK
ICAgImNoZWNrIjogIkMyIiwKICAgIm5hbWUiOiAicGhhc2UyW2N1YmljX2dlbTh8MTExXS5xdWFk
Zm9ybS5rYXBwYTI0IChjYykgY3ViaWMgbnVsbCBhYnMgPD0gMWUtMTAiLAogICAibm90ZSI6ICIi
LAogICAicGFzcyI6IGZhbHNlCiAgfSwKICB7CiAgICJjYyI6ICJSRUdJU1RFUkVEX05PVF9FWEVD
VVRFRCIsCiAgICJjaGF0IjogIlJFR0lTVEVSRURfTk9UX0VYRUNVVEVEIiwKICAgImNoZWNrIjog
IkMzIiwKICAgIm5hbWUiOiAicGhhc2UzLkYtTVMyLTIgdHlwZWQgc3RyIGJvdGggbGVncyIsCiAg
ICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiUkVHSVNURVJF
RF9OT1RfRVhFQ1VURUQiLAogICAiY2hhdCI6ICJSRUdJU1RFUkVEX05PVF9FWEVDVVRFRCIsCiAg
ICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMy5GLU1TMi0yIGVxdWFsIiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJTSUxFTlQiLAogICAi
Y2hhdCI6ICJTSUxFTlQiLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTMuRi1N
UzItMyB0eXBlZCBzdHIgYm90aCBsZWdzIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6ICJTSUxFTlQiLAogICAiY2hhdCI6ICJTSUxFTlQiLAogICAiY2hl
Y2siOiAiQzMiLAogICAibmFtZSI6ICJwaGFzZTMuRi1NUzItMyBlcXVhbCIsCiAgICJub3RlIjog
IiIsCiAgICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiAiU0lMRU5UIiwKICAgImNoYXQi
OiAiU0lMRU5UIiwKICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UzLkYtTVMyLTQg
dHlwZWQgc3RyIGJvdGggbGVncyIsCiAgICJub3RlIjogIiIsCiAgICJwYXNzIjogdHJ1ZQogIH0s
CiAgewogICAiY2MiOiAiU0lMRU5UIiwKICAgImNoYXQiOiAiU0lMRU5UIiwKICAgImNoZWNrIjog
IkMzIiwKICAgIm5hbWUiOiAicGhhc2UzLkYtTVMyLTQgZXF1YWwiLAogICAibm90ZSI6ICIiLAog
ICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIklERU5USVRZLURFTElWRVJFRC1MNCIs
CiAgICJjaGF0IjogIklERU5USVRZLURFTElWRVJFRC1MNCIsCiAgICJjaGVjayI6ICJDMyIsCiAg
ICJuYW1lIjogInBoYXNlMy52ZXJkaWN0X2NsYXNzIHR5cGVkIHN0ciBib3RoIGxlZ3MiLAogICAi
bm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogIklERU5USVRZLURF
TElWRVJFRC1MNCIsCiAgICJjaGF0IjogIklERU5USVRZLURFTElWRVJFRC1MNCIsCiAgICJjaGVj
ayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMy52ZXJkaWN0X2NsYXNzIGVxdWFsIiwKICAgIm5v
dGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0
IjogIklERU5USVRZLURFTElWRVJFRC1MNCIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjog
InBoYXNlMy52ZXJkaWN0X2NsYXNzIGluIGRvbWFpbiAoY2hhdCkiLAogICAibm90ZSI6ICIiLAog
ICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNjIjogbnVsbCwKICAgImNoYXQiOiA0LjI2NzE2
ODIyOTAyMTg5NmUtMTEsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInBoYXNlMy53b3Jz
dF9TNCAoY2hhdCkgbGUgMWUtMDYiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9
LAogIHsKICAgImNjIjogIklERU5USVRZLURFTElWRVJFRC1MNCIsCiAgICJjaGF0IjogbnVsbCwK
ICAgImNoZWNrIjogIkMzIiwKICAgIm5hbWUiOiAicGhhc2UzLnZlcmRpY3RfY2xhc3MgaW4gZG9t
YWluIChjYykiLAogICAibm90ZSI6ICIiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogNC4yNjcxNjgyMjkwMjE4OTZlLTExLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJD
MyIsCiAgICJuYW1lIjogInBoYXNlMy53b3JzdF9TNCAoY2MpIGxlIDFlLTA2IiwKICAgIm5vdGUi
OiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0Ijog
IklERU5USVRZLURFTElWRVJFRC1MNCIsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogInZl
cmRpY3QgcmVjb21wdXRlZCA9PSByZXBvcnRlZCAoY2hhdCkiLAogICAibm90ZSI6ICJyZXBvcnRl
ZCBJREVOVElUWS1ERUxJVkVSRUQtTDQiLAogICAicGFzcyI6IHRydWUKICB9LAogIHsKICAgImNj
IjogbnVsbCwKICAgImNoYXQiOiBudWxsLAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJ3
b3JzdF9TNCBjb25zaXN0ZW50IHdpdGggcGhhc2UyIChjaGF0KSIsCiAgICJub3RlIjogIiIsCiAg
ICJwYXNzIjogdHJ1ZQogIH0sCiAgewogICAiY2MiOiBudWxsLAogICAiY2hhdCI6ICJTSUxFTlQi
LAogICAiY2hlY2siOiAiQzMiLAogICAibmFtZSI6ICJGLU1TMi0zIHN0YXRlIGNvbnNpc3RlbnQg
KGNoYXQpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6
ICJJREVOVElUWS1ERUxJVkVSRUQtTDQiLAogICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJD
MyIsCiAgICJuYW1lIjogInZlcmRpY3QgcmVjb21wdXRlZCA9PSByZXBvcnRlZCAoY2MpIiwKICAg
Im5vdGUiOiAicmVwb3J0ZWQgSURFTlRJVFktREVMSVZFUkVELUw0IiwKICAgInBhc3MiOiB0cnVl
CiAgfSwKICB7CiAgICJjYyI6IG51bGwsCiAgICJjaGF0IjogbnVsbCwKICAgImNoZWNrIjogIkMz
IiwKICAgIm5hbWUiOiAid29yc3RfUzQgY29uc2lzdGVudCB3aXRoIHBoYXNlMiAoY2MpIiwKICAg
Im5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfSwKICB7CiAgICJjYyI6ICJTSUxFTlQiLAog
ICAiY2hhdCI6IG51bGwsCiAgICJjaGVjayI6ICJDMyIsCiAgICJuYW1lIjogIkYtTVMyLTMgc3Rh
dGUgY29uc2lzdGVudCAoY2MpIiwKICAgIm5vdGUiOiAiIiwKICAgInBhc3MiOiB0cnVlCiAgfQog
XSwKICJzY2hlbWFfbWQ1IjogIjY2ZjU4NmQ3YjZjNWU4MjI4Mzk0MjIyZGRmZGE3M2YyIiwKICJz
dW1tYXJ5IjogewogICJjaGVja3MiOiAzNTYsCiAgIm1pc3MiOiAxOCwKICAicGFzcyI6IDMzOAog
fQp9
=====END-EMBED name=g_mscs2_chatleg_selfcompare.json=====

=====BEGIN-EMBED name=run_chatleg.log md5=e2940623b9e7035ffc29ac796280ecda bytes=3156 encoding=base64 armor_bytes=4264 QUARANTINED=====
cGhhc2UwIC4uLgogIFBJTi1LMiBoZXhfc3RlcHxhICAgICAgIGthcHBhMj0tMS40Mzk0NjE3Njll
LTAzICBYLTYgLTEuNDM5NDYxNzY5ZS0wMwogIFBJTi1LMiBoZXhfc3RlcHxiICAgICAgIGthcHBh
Mj0tMS40Mzg3MDI3MTllLTAzICBYLTYgLTEuNDM4NzAyNzE5ZS0wMwogIFBJTi1LMiBoZXhfZ2Vt
OHxhICAgICAgIGthcHBhMj0tMS44OTU2NDg0ODNlLTAzICBYLTYgLTEuODk1NjQ4NDgzZS0wMwog
IFBJTi1LMiBoZXhfZ2VtOHxiICAgICAgIGthcHBhMj0tMS44OTYxMzc0NjdlLTAzICBYLTYgLTEu
ODk2MTM3NDY3ZS0wMwogIFBJTi1LMiBjdWJpY19zdGVwfDAwMSAgIGthcHBhMj0tNC41NTEzODcw
NDllLTE2ICBYLTYgKzMuMTQxNzAyMTI0ZS0xNQogIFBJTi1LMiBjdWJpY19zdGVwfDExMSAgIGth
cHBhMj0tMS42NzM5MTQzODZlLTE2ICBYLTYgLTEuNjczOTE0Mzg2ZS0xNgogIFBJTi1LMiBjdWJp
Y19nZW04fDAwMSAgIGthcHBhMj0tMi4xNTUzMzc2OTdlLTE1ICBYLTYgLTEuNDk0MDcyMzQ0ZS0x
NgogIFBJTi1LMiBjdWJpY19nZW04fDExMSAgIGthcHBhMj0tMS42MDE5Nzc1NjllLTE1ICBYLTYg
KzEuMjcyNzI4MjkzZS0xNgogIFBJTi1YVEFMICAgICAgICAgcGFzc2VkPVRydWUgIHdvcnN0X3Jl
bD0wLjAwMGUrMDAKICBQSU4tVlJIMCAgICAgICAgIHBhc3NlZD1UcnVlICB3b3JzdF9yZWw9MC4w
MDBlKzAwCiAgUElOLUhTMCAgICAgICAgICBwYXNzZWQ9VHJ1ZSAgd29yc3RfcmVsPTAuMDAwZSsw
MAogIFBJTi1LMiAgICAgICAgICAgcGFzc2VkPVRydWUgIHdvcnN0X3JlbF9oZXhfa2FwcGEyPTEu
MzkzZS0xMiB3b3JzdF9hYnNfY3ViaWNfa2FwcGEyPTIuMTU1ZS0xNQogIEYtQ1RSTC1JU08gICAg
ICAgcGFzc2VkPVRydWUgIHdvcnN0X2Ficz00LjQ0MWUtMTYKICBGLUNUUkwtU08zICAgICAgIHBh
c3NlZD1UcnVlICBkZXZfZnJvbV8wcDQ9NC45OTZlLTE2IHJfYWdnXzBfYWJzPTAuMDAwZSswMAog
IEYtQ1RSTC1QT1MgICAgICAgcGFzc2VkPVRydWUgIG1pbl9vZGZfd2VpZ2h0PTMuOTUwZS0wMQog
IEYtQ1RSTC1MMk5VTEwgICAgcGFzc2VkPVRydWUgIHdvcnN0X2Ficz01Ljg1MGUtMTQKICBGLUNU
UkwtTDRFWEhBVVNUIHBhc3NlZD1UcnVlICB3b3JzdF9yZWxfdGVuc29yPTQuMzI2ZS0xNCB3b3Jz
dF9hYnNfcl9hZ2c9NC40NDFlLTE2CiAgRi1DVFJMLUM0ICAgICAgICBwYXNzZWQ9VHJ1ZSAgd29y
c3RfcmVsX2Nsb3NlZF9mb3JtPTIuNTE5ZS0xNCB3b3JzdF9yZWxfYWZmaW5lPTQuMDc0ZS0xNCBo
MF9lZmZlY3RfcmVsPTIuMzAyZS0xNAogIEYtQ1RSTC1NQVJHICAgICAgcGFzc2VkPVRydWUgIHdv
cnN0X2Ficz04LjMyN2UtMTYKICBGLUNUUkwtVEVYNCAgICAgIHBhc3NlZD1UcnVlICByX2FnZ190
MV9hYnM9NC4xMThlLTA0CiAgRi1DVFJMLVFVQUQgICAgICBwYXNzZWQ9VHJ1ZSAgZG91Ymxpbmdf
cmVzaWR1YWw9Mi4yNjBlLTE0IGtfc3BoZXJlX2RvdWJsaW5nPTIuMjIwZS0xNiBzbzNfZG91Ymxp
bmc9Mi4yNjBlLTE0CnBoYXNlMiAuLi4KICBwaGFzZTIgaGV4X3N0ZXB8YSAgICAgICBTND0tMi4y
MTRlLTEzIGs0ND0rMS42MDQwNTNlLTA0ICh3aW4wLjEgKzEuNjA0MDM3ZS0wNCkgazQ0X0hTPSsx
LjU5ODkzMGUtMDQgazQ0X2g9LTcuNTA4ZS0wNiBiMT0rMS42MjQxZS0wMiBxZiBrMjI9LTEuNDM5
ZS0wMyBrMjQ9LTEuMjQ5ZS0wOCBrNDQ9KzEuNjAzOTkwZS0wNAogIHBoYXNlMiBoZXhfc3RlcHxi
ICAgICAgIFM0PS0yLjE5OWUtMTMgazQ0PSsxLjYwNDE0N2UtMDQgKHdpbjAuMSArMS42MDQxMzFl
LTA0KSBrNDRfSFM9KzEuNTk5MDI2ZS0wNCBrNDRfaD0tNy41MDllLTA2IGIxPSsxLjYyNDJlLTAy
IHFmIGsyMj0tMS40MzllLTAzIGsyND0tMS4yNDhlLTA4IGs0ND0rMS42MDQwODRlLTA0CiAgcGhh
c2UyIGhleF9nZW04fGEgICAgICAgUzQ9LTIuNjUyZS0xMyBrNDQ9KzEuNzk1MDczZS0wNCAod2lu
MC4xICsxLjc5NTA1M2UtMDQpIGs0NF9IUz0rMS43ODkzMDZlLTA0IGs0NF9oPS03Ljc1NGUtMDYg
YjE9KzEuODE3NWUtMDIgcWYgazIyPS0xLjg5NmUtMDMgazI0PS0xLjgzN2UtMDggazQ0PSsxLjc5
NDk4NGUtMDQKICBwaGFzZTIgaGV4X2dlbTh8YiAgICAgICBTND0tMi42NjVlLTEzIGs0ND0rMS43
OTUwMTVlLTA0ICh3aW4wLjEgKzEuNzk0OTk1ZS0wNCkgazQ0X0hTPSsxLjc4OTI0N2UtMDQgazQ0
X2g9LTcuNzU0ZS0wNiBiMT0rMS44MTc0ZS0wMiBxZiBrMjI9LTEuODk2ZS0wMyBrMjQ9LTEuODM4
ZS0wOCBrNDQ9KzEuNzk0OTI2ZS0wNAogIHBoYXNlMiBjdWJpY19zdGVwfDAwMSAgIFM0PS0xLjk1
NWUtMTEgazQ0PS0zLjc0MzUyOWUtMDQgKHdpbjAuMSAtMy43NDMxNDFlLTA0KSBrNDRfSFM9LTMu
ODkyNjQ3ZS0wNCBrNDRfaD0tMy44MDNlLTA1IGIxPS0zLjc4OTllLTAyIHFmIGsyMj0rNC40ODJl
LTA5IGsyND0rMS45NzRlLTA3IGs0ND0tMy43NDM1NDZlLTA0CiAgcGhhc2UyIGN1YmljX3N0ZXB8
MTExICAgUzQ9KzEuMzA0ZS0xMSBrNDQ9KzIuNDk1Njg2ZS0wNCAod2luMC4xICsyLjQ5NTQyOGUt
MDQpIGs0NF9IUz0rMi41OTUwOThlLTA0IGs0NF9oPS0zLjgwM2UtMDUgYjE9LTMuNzg5OWUtMDIg
cWYgazIyPS0yLjk4OGUtMDkgazI0PSsxLjk3NGUtMDcgazQ0PSsyLjQ5NTY5N2UtMDQKICBwaGFz
ZTIgY3ViaWNfZ2VtOHwwMDEgICBTND0tNC4yNjdlLTExIGs0ND0tNC40OTI3NzFlLTA0ICh3aW4w
LjEgLTQuNDkyMDgxZS0wNCkgazQ0X0hTPS00Ljc2NzE1MmUtMDQgazQ0X2g9LTQuNTM2ZS0wNSBi
MT0tNC41NDgxZS0wMiBxZiBrMjI9KzcuOTY0ZS0wOSBrMjQ9KzMuNDc4ZS0wNyBrNDQ9LTQuNDky
ODAwZS0wNAogIHBoYXNlMiBjdWJpY19nZW04fDExMSAgIFM0PSsyLjg0NWUtMTEgazQ0PSsyLjk5
NTE4MWUtMDQgKHdpbjAuMSArMi45OTQ3MjFlLTA0KSBrNDRfSFM9KzMuMTc4MTAxZS0wNCBrNDRf
aD0tNC41MzZlLTA1IGIxPS00LjU0ODFlLTAyIHFmIGsyMj0tNS4zMDllLTA5IGsyND0rMy40Nzhl
LTA3IGs0ND0rMi45OTUyMDBlLTA0CnZlcmRpY3RfY2xhc3MgSURFTlRJVFktREVMSVZFUkVELUw0
ICBGLU1TMi0zIFNJTEVOVCAgRi1NUzItNCBTSUxFTlQgIFQxIHBvc3QgQ0xFQU4KY2hlY2twb2lu
dCBnX21zY3MyX2NoYXRsZWdfY2hlY2twb2ludC5qc29uIDFjNWI2YjU5ODI5ZDJhNmI5YWUyYjFh
N2EwMTY4MzJkICgzMSw1NzUgQikK
=====END-EMBED name=run_chatleg.log=====

=====BEGIN-EMBED name=run_phase0.log md5=72d64aebe9eb754e7e443bb36e63969e bytes=1681 encoding=base64 armor_bytes=2274 QUARANTINED=====
cGhhc2UwIC4uLgogIFBJTi1LMiBoZXhfc3RlcHxhICAgICAgIGthcHBhMj0tMS40Mzk0NjE3Njll
LTAzICBYLTYgLTEuNDM5NDYxNzY5ZS0wMwogIFBJTi1LMiBoZXhfc3RlcHxiICAgICAgIGthcHBh
Mj0tMS40Mzg3MDI3MTllLTAzICBYLTYgLTEuNDM4NzAyNzE5ZS0wMwogIFBJTi1LMiBoZXhfZ2Vt
OHxhICAgICAgIGthcHBhMj0tMS44OTU2NDg0ODNlLTAzICBYLTYgLTEuODk1NjQ4NDgzZS0wMwog
IFBJTi1LMiBoZXhfZ2VtOHxiICAgICAgIGthcHBhMj0tMS44OTYxMzc0NjdlLTAzICBYLTYgLTEu
ODk2MTM3NDY3ZS0wMwogIFBJTi1LMiBjdWJpY19zdGVwfDAwMSAgIGthcHBhMj0tNC41NTEzODcw
NDllLTE2ICBYLTYgKzMuMTQxNzAyMTI0ZS0xNQogIFBJTi1LMiBjdWJpY19zdGVwfDExMSAgIGth
cHBhMj0tMS42NzM5MTQzODZlLTE2ICBYLTYgLTEuNjczOTE0Mzg2ZS0xNgogIFBJTi1LMiBjdWJp
Y19nZW04fDAwMSAgIGthcHBhMj0tMi4xNTUzMzc2OTdlLTE1ICBYLTYgLTEuNDk0MDcyMzQ0ZS0x
NgogIFBJTi1LMiBjdWJpY19nZW04fDExMSAgIGthcHBhMj0tMS42MDE5Nzc1NjllLTE1ICBYLTYg
KzEuMjcyNzI4MjkzZS0xNgogIFBJTi1YVEFMICAgICAgICAgcGFzc2VkPVRydWUgIHdvcnN0X3Jl
bD0wLjAwMGUrMDAKICBQSU4tVlJIMCAgICAgICAgIHBhc3NlZD1UcnVlICB3b3JzdF9yZWw9MC4w
MDBlKzAwCiAgUElOLUhTMCAgICAgICAgICBwYXNzZWQ9VHJ1ZSAgd29yc3RfcmVsPTAuMDAwZSsw
MAogIFBJTi1LMiAgICAgICAgICAgcGFzc2VkPVRydWUgIHdvcnN0X3JlbF9oZXhfa2FwcGEyPTEu
MzkzZS0xMiB3b3JzdF9hYnNfY3ViaWNfa2FwcGEyPTIuMTU1ZS0xNQogIEYtQ1RSTC1JU08gICAg
ICAgcGFzc2VkPVRydWUgIHdvcnN0X2Ficz00LjQ0MWUtMTYKICBGLUNUUkwtU08zICAgICAgIHBh
c3NlZD1UcnVlICBkZXZfZnJvbV8wcDQ9NC45OTZlLTE2IHJfYWdnXzBfYWJzPTAuMDAwZSswMAog
IEYtQ1RSTC1QT1MgICAgICAgcGFzc2VkPVRydWUgIG1pbl9vZGZfd2VpZ2h0PTMuOTUwZS0wMQog
IEYtQ1RSTC1MMk5VTEwgICAgcGFzc2VkPVRydWUgIHdvcnN0X2Ficz01Ljg1MGUtMTQKICBGLUNU
UkwtTDRFWEhBVVNUIHBhc3NlZD1UcnVlICB3b3JzdF9yZWxfdGVuc29yPTQuMzI2ZS0xNCB3b3Jz
dF9hYnNfcl9hZ2c9NC40NDFlLTE2CiAgRi1DVFJMLUM0ICAgICAgICBwYXNzZWQ9VHJ1ZSAgd29y
c3RfcmVsX2Nsb3NlZF9mb3JtPTIuNTE5ZS0xNCB3b3JzdF9yZWxfYWZmaW5lPTQuMDc0ZS0xNCBo
MF9lZmZlY3RfcmVsPTIuMzAyZS0xNAogIEYtQ1RSTC1NQVJHICAgICAgcGFzc2VkPVRydWUgIHdv
cnN0X2Ficz04LjMyN2UtMTYKICBGLUNUUkwtVEVYNCAgICAgIHBhc3NlZD1UcnVlICByX2FnZ190
MV9hYnM9NC4xMThlLTA0CiAgRi1DVFJMLVFVQUQgICAgICBwYXNzZWQ9VHJ1ZSAgZG91Ymxpbmdf
cmVzaWR1YWw9Mi4yNjBlLTE0IGtfc3BoZXJlX2RvdWJsaW5nPTIuMjIwZS0xNiBzbzNfZG91Ymxp
bmc9Mi4yNjBlLTE0CnBoYXNlMCBjb21wbGV0ZSAocGhhc2UwLW9ubHkgcnVuKTsgY2hlY2twb2lu
dCBnX21zY3MyX2NoYXRsZWdfcGhhc2UwX2NoZWNrcG9pbnQuanNvbiA5ZTVhNmU4YmEwODA0YmRh
Nzc4ZTRiZTUyZmJlMmZkZSAoNyw3NDcgQikgIFQxIHBvc3QgQ0xFQU4KCnJlYWwJNG0wLjQ3NXMK
dXNlcgkzbTAuNTQ4cwpzeXMJMG01OS4wMDdzCg==
=====END-EMBED name=run_phase0.log=====

=====BEGIN-EMBED name=G_MSCS2_CHATLEG_EXECUTION_REPORT.md md5=ae032ab9d585b842cfd57410e7380d08 bytes=16045 encoding=base64 armor_bytes=21678 QUARANTINED=====
IyBHLU1TQ1MyIOKAlCBDSEFULUxFRyBFWEVDVVRJT04gUkVQT1JUIChQaGFzZXMgMCwgMiwgMykK
CioqRGF0ZToqKiBTZXB0ZW1iZXIgMjYsIDIwMjYgKGZ1bGwgcnVuIDE1OjV44oCTMTY6MDIgVVRD
OyB0aGUgUGhhc2UtMC1vbmx5IHJ1biBvZiAxNDozMyBVVEMsIGNoZWNrcG9pbnQgYDllNWE2ZThi
YCwgaXMgc3VwZXJzZWRlZCBieSB0aGlzIG9uZSwgd2hpY2ggcmVjb21wdXRlZCBQaGFzZSAwIGZy
b20gc2NyYXRjaCBwZXIgQS0yLjEwKS4gKipCYXNlOioqIFY0Ljg0IGBmMzZiYmRiMGAuICoqTWVt
byBsb2NrOioqIHYyIGBlZmRjYWJkY2Q5MzdjZGE0YWNiNjRmOTQxZGM0YmIyYmAuICoqTG9jayBy
ZWNvcmQ6KiogYDQ5MjMyZDRjYC4gKipTY2hlbWEgdjEuMCoqIGA2NmY1ODZkN2AgKyAqKmNvbXBh
cmF0b3IgdjEuMCoqIGA4MGQzYjkwN2Ag4oCUIEZST1pFTiBiZWZvcmUgZW1pc3Npb24uICoqVDEg
bGlzdCoqIGBiZTkyMWI4Y2AgKDM2IHBhdHRlcm5zKS4gKipJbnN0cnVtZW50OioqIGBnX21zY3My
X2NoYXRsZWcucHlgIGBmMjc3NTgwZGRmMGI0ZGE5NzM0ZDExZWRiMDA5YzU0YmAgKHVuY2hhbmdl
ZCBzaW5jZSB0aGUgUGhhc2UtMCBydW47IDcvNyBzdWl0ZXMpLiAqKkNoZWNrcG9pbnQgb2YgcmVj
b3JkOioqIGBnX21zY3MyX2NoYXRsZWdfY2hlY2twb2ludC5qc29uYCAqKmAxYzViNmI1OTgyOWQy
YTZiOWFlMmIxYTdhMDE2ODMyZGAqKiAoMzEsNTc1IEIpLiAqKkh5cG90aGVzaXMgY29tcGFyZSAo
bGFzdCk6KiogYGdfbXNjczJfY2hhdGxlZ19jb21wYXJlLmpzb25gIGA3YTllMTcwNGAuICoqQ2hh
dC12cy1jaGF0IGNvbXBhcmF0b3Igc2FuaXR5OioqIGBnX21zY3MyX2NoYXRsZWdfc2VsZmNvbXBh
cmUuanNvbmAgYDBhMTA2MjM2YCAoMzU2IC8gMzM4IC8gMTgg4oCUIHNlZSDCpzYpLiBSdW4gbG9n
IGBlMjk0MDYyM2AuIFQxOiBpbnN0cnVtZW50LCBtZW1vLCBjaGVja3BvaW50LCBjb21wYXJlIGZp
bGVzLCBkaWFnbm9zdGljcyBhbGwgQ0xFQU4uCgojIyAxLiBWZXJkaWN0IChhc3NlbWJsZWQgbGFz
dCwgYnkgdGhlIHNjaGVtYSBydWxlKTogKipJREVOVElUWS1ERUxJVkVSRUQtTDQqKgoKQWxsIDEz
IFBoYXNlLTAgcGlucyBhbmQgY29udHJvbHMgUEFTUyAoUGhhc2UgMCByZWNvbXB1dGVkOyB2YWx1
ZXMgaWRlbnRpY2FsIHRvIHRoZSBQaGFzZS0wIHJlcG9ydCkuICoqRi1NUzItMyBTSUxFTlQqKiDi
gJQgd29yc3QgfFPigoR8ID0gNC4zw5cxMOKBu8K5wrkgb3ZlciB0aGUgZWlnaHQga2V5cyBhbmQg
Ym90aCBTMiBhcm1zIChmaXJzdC1vcmRlciBwcm90ZWN0aW9uIGhvbGRzIGluIHRoZSBsID0gNCBm
YW1pbGllcyBhcyBpdCBkaWQgYXQgbCA9IDIpLiAqKkYtTVMyLTQgU0lMRU5UKiog4oCUIM664oKE
4oKEKFMyLUXigoIpIG9uIHRoZSBwcmltYXJ5IGN1YmljIGtleXMgaXMg4oiSMy43NMOXMTDigbvi
gbQgYW5kIOKIkjQuNDnDlzEw4oG74oG0LCBmYXIgYWJvdmUgdGhlIDEw4oG74oG2IGZsb29yOiB0
aGUgZmNjIGJyYW5jaCwgYmxpbmQgYXQgbCA9IDIsIGhhcyBhIG5vbi16ZXJvIHNlY29uZC1vcmRl
ciB0ZXh0dXJlIHNwbGl0IGF0IGwgPSA0LiBGLU1TMi0yIFJFR0lTVEVSRURfTk9UX0VYRUNVVEVE
LgoKIyMgMi4gUGhhc2UgMiDigJQgdGhlIGRlbGl2ZXJlZCBjb2VmZmljaWVudHMgKEhpbGwgdW5s
ZXNzIHN0YXRlZDsgYWxsIGVpZ2h0IGtleXM7IHN1YnN0cmF0ZSByYXRpb3MpCgp8IEtleSB8IM66
4oKE4oKEKFMyLUXigoIpIHwgSFMtbWVhbiB8IM664oKE4oKEKFMyLWgpIHwgzrrigoTigoTigoQg
fCBoYWx2aW5nIGRldiB8IGLigoEgKGJpcmVmcmluZ2VuY2UgLyB1bml0IHTigoQpIHwgzrvMhF9M
KHTigoQgPSAxKSB8CnwtLS18LS0tfC0tLXwtLS18LS0tfC0tLXwtLS18LS0tfAp8IGhleF9zdGVw
XHxhIHwgKiorMS42MDQwNcOXMTDigbvigbQqKiB8ICsxLjU5ODkzw5cxMOKBu+KBtCB8IOKIkjcu
NTHDlzEw4oG74oG2IHwgKzIuMsOXMTDigbvigbcgfCAxLjbDlzEw4oG74oG5IHwgKzEuNjI0McOX
MTDigbvCsiB8IDMuOMOXMTDigbvigbUgfAp8IGhleF9zdGVwXHxiIHwgKzEuNjA0MTXDlzEw4oG7
4oG0IHwgKzEuNTk5MDPDlzEw4oG74oG0IHwg4oiSNy41McOXMTDigbvigbYgfCArMi4yw5cxMOKB
u+KBtyB8IDEuNsOXMTDigbvigbkgfCArMS42MjQyw5cxMOKBu8KyIHwgMy44w5cxMOKBu+KBtSB8
CnwgaGV4X2dlbThcfGEgfCAqKisxLjc5NTA3w5cxMOKBu+KBtCoqIHwgKzEuNzg5MzHDlzEw4oG7
4oG0IHwg4oiSNy43NcOXMTDigbvigbYgfCArMi4yw5cxMOKBu+KBtyB8IDIuMMOXMTDigbvigbkg
fCArMS44MTc1w5cxMOKBu8KyIHwgMy41w5cxMOKBu+KBtSB8CnwgaGV4X2dlbThcfGIgfCArMS43
OTUwMsOXMTDigbvigbQgfCArMS43ODkyNcOXMTDigbvigbQgfCDiiJI3Ljc1w5cxMOKBu+KBtiB8
ICsyLjLDlzEw4oG74oG3IHwgMi4ww5cxMOKBu+KBuSB8ICsxLjgxNzTDlzEw4oG7wrIgfCAzLjXD
lzEw4oG74oG1IHwKfCBjdWJpY19zdGVwXHwwMDEgfCAqKuKIkjMuNzQzNTPDlzEw4oG74oG0Kiog
fCDiiJIzLjg5MjY1w5cxMOKBu+KBtCB8IOKIkjMuODDDlzEw4oG74oG1IHwgKzIuNsOXMTDigbvi
gbYgfCAzLjnDlzEw4oG74oG4IHwg4oiSMy43ODk5w5cxMOKBu8KyIHwgMS44w5cxMOKBu+KBtCB8
CnwgY3ViaWNfc3RlcFx8MTExIHwgKiorMi40OTU2OcOXMTDigbvigbQqKiB8ICsyLjU5NTEww5cx
MOKBu+KBtCB8IOKIkjMuODDDlzEw4oG74oG1IHwg4oiSMS44w5cxMOKBu+KBtiB8IDIuNsOXMTDi
gbvigbggfCDiiJIzLjc4OTnDlzEw4oG7wrIgfCAxLjjDlzEw4oG74oG0IHwKfCBjdWJpY19nZW04
XHwwMDEgfCAqKuKIkjQuNDkyNzfDlzEw4oG74oG0KiogfCDiiJI0Ljc2NzE1w5cxMOKBu+KBtCB8
IOKIkjQuNTTDlzEw4oG74oG1IHwgKzMuOMOXMTDigbvigbYgfCA2LjnDlzEw4oG74oG4IHwg4oiS
NC41NDgxw5cxMOKBu8KyIHwgMS45w5cxMOKBu+KBtCB8CnwgY3ViaWNfZ2VtOFx8MTExIHwgKior
Mi45OTUxOMOXMTDigbvigbQqKiB8ICszLjE3ODEww5cxMOKBu+KBtCB8IOKIkjQuNTTDlzEw4oG7
4oG1IHwg4oiSMi41w5cxMOKBu+KBtiB8IDQuNsOXMTDigbvigbggfCDiiJI0LjU0ODHDlzEw4oG7
wrIgfCAxLjnDlzEw4oG74oG0IHwKCkZpdCByZXNpZHVhbHMgOMOXMTDigbvCucKyIChoZXgpIHRv
IDPDlzEw4oG7wrnigbAgKGN1YmljKTsgZXZlcnkgaGFsdmluZyBkZXZpYXRpb24gd2l0aGluIG1h
eCgxMOKBu+KBtMK3fM664oKE4oKEfCwgMTDigbvigbYpLiBUaGUgcl9hZ2codOKChCkgYXJyYXlz
IChWUkgsIEhTLCBWLCBSOyBib3RoIGFybXMpLCDOu8yEX0wodOKChCkgYW5kIHRoZSBxdWFkcmF0
aWMgZm9ybXMgYXJlIGluIHRoZSBjaGVja3BvaW50LgoKKipIZXggdHdvLXBhcmFtZXRlciBmYW1p
bHkgKHNlY29uZCBhcm0pLCA1IMOXIDUgZ3JpZCwgNy10ZXJtIGZpdDoqKiDOuuKCguKCgiA9IOKI
kjEuNDM5w5cxMOKBu8KzIC8g4oiSMS40MznDlzEw4oG7wrMgLyDiiJIxLjg5NsOXMTDigbvCsyAv
IOKIkjEuODk2w5cxMOKBu8KzICgqKj0gdGhlIGJhbmtlZCBHLU1TQ1MxIM664oKCIHRvIDQgZGln
aXRzIOKAlCBQSU4tSzIgaW4gdGhlIHNlY29uZCBhcm0gYXMgd2VsbCoqKTsgzrrigoTigoQgPSAr
MS42MDQww5cxMOKBu+KBtCAvICsxLjYwNDHDlzEw4oG74oG0IC8gKzEuNzk1MMOXMTDigbvigbQg
LyArMS43OTQ5w5cxMOKBu+KBtCAobWF0Y2hpbmcgdGhlIG9uZS1wYXJhbWV0ZXIgZml0IHRvIDTD
lzEw4oG74oG1IHJlbGF0aXZlKTsgKirOuuKCguKChCA9IOKIkjEuMjXDlzEw4oG74oG4IC8g4oiS
MS4yNcOXMTDigbvigbggLyDiiJIxLjg0w5cxMOKBu+KBuCAvIOKIkjEuODTDlzEw4oG74oG4IOKA
lCB6ZXJvIGF0IHRoZSBmaXQncyByZXNvbHV0aW9uLioqIEN1YmljIGtleXMsIHNhbWUgZml0IHVu
ZGVyIHRoZSBpbmhlcml0ZWQgKG5vbi1PX2gtc3ltbWV0cml6ZWQsIGRlc2NyaXB0b3ItYXhpcykg
bCA9IDIgd2VpZ2h0OiDOuuKCguKCgiA9ICs0LjXDlzEw4oG74oG5IC8g4oiSMy4ww5cxMOKBu+KB
uSAvICs4LjDDlzEw4oG74oG5IC8g4oiSNS4zw5cxMOKBu+KBuTsgzrrigoLigoQgPSArMS45N8OX
MTDigbvigbcgLyArMS45N8OXMTDigbvigbcgLyArMy40OMOXMTDigbvigbcgLyArMy40OMOXMTDi
gbvigbcgKMKnNywgSC1NUzItNCkuCgojIyAzLiBGaW5kaW5ncyAoUjEtbWFjaGluZSBjaGF0IGxl
ZzsgdHdvLWxlZyBjb25maXJtYXRpb24gcGVuZGluZykKCjEuICoqVGhlIGZjYyBjb25zdHJhaW50
IGN1cnZlIGV4aXN0cyBhbmQgaXMgZGVsaXZlcmVkOiByX2FnZyh04oKEKSDiiYggzrrigoTigoQg
dOKChMKyIHdpdGggzrrigoTigoQo4p+oMDAx4p+pIGRlc2NyaXB0b3IpID0g4oiSMy43NMOXMTDi
gbvigbQgKGN1YmljOnN0ZXApIC8g4oiSNC40OcOXMTDigbvigbQgKGN1YmljOmdlbTgpKiog4oCU
IHRoZSBmY2MgYnJhbmNoLCBpZGVudGljYWxseSBibGluZCB0byBsID0gMiB0ZXh0dXJlIChHLU1T
Q1MxKSwgcmVzcG9uZHMgYXQgc2Vjb25kIG9yZGVyIHRvIHRoZSBmaXJzdCBoYXJtb25pYyBpdHMg
cG9pbnQgZ3JvdXAgYWRtaXRzLiBIUy1tZWFuIHdpdGhpbiA0JSBvZiBIaWxsLgoyLiAqKlRoZSBk
ZXNjcmlwdG9yLWF4aXMgImdlbnVpbmUgY2hvaWNlIiBvZiBHLU1TQ1MxIGlzIG5vdyBhIG51bWJl
cjogzrrigoTigoQo4p+oMTEx4p+pKSA9IOKIkigyLzMpwrfOuuKChOKChCjin6gwMDHin6kpIGV4
YWN0bHkqKiAo4oiSMC42NjY2NyBvbiBib3RoIGZjYyBjb25maWd1cmF0aW9ucykg4oCUIHRoZSBt
YXJnaW5hbCBjb2VmZmljaWVudHMgY1/in6gwMDHin6kgPSAxLCBjX+KfqDExMeKfqSA9IOKIkjIv
MyAoQS0yLjUsIEYtQ1RSTC1NQVJHKSBjYXJyeSBzdHJhaWdodCB0aHJvdWdoIHRvIHRoZSBzZWNv
bmQtb3JkZXIgY29lZmZpY2llbnQgYmVjYXVzZSB0aGUgbCA9IDQgc3BlZWQgcGVydHVyYmF0aW9u
IGlzIGRlc2NyaXB0b3ItaW5kZXBlbmRlbnQgYW5kIHRoZSB3ZWlnaHQgcGVydHVyYmF0aW9uIGlz
IGxpbmVhciBpbiBjLiBIWVAtTVMyLTIgKHRoZSBzaWduIGZsaXApIGNvbmZpcm1lZCwgYW5kIHNo
YXJwZW5lZCB0byB0aGUgcmF0aW8uIFRoZSBTMi1oIGFybSwgZGVzY3JpcHRvci1pbmRlcGVuZGVu
dCwgZ2l2ZXMgzrrigoTigoQoUzItaCkgPSDiiJIzLjjDlzEw4oG74oG1IC8g4oiSNC41w5cxMOKB
u+KBtSAoYWRtaXh0dXJlLXNvdXJjZWQsIGFzIGF0IGwgPSAyKS4KMy4gKipPbiB0aGUgaGV4IGJy
YW5jaCB0aGUgbCA9IDQgcmVzcG9uc2UgaGFzIHRoZSBvcHBvc2l0ZSBzaWduIHRvIHRoZSBsID0g
MiByZXNwb25zZToqKiDOuuKChOKChCA9ICsxLjYww5cxMOKBu+KBtCAvICsxLjgww5cxMOKBu+KB
tCBhZ2FpbnN0IM664oKC4oKCID0g4oiSMS40NMOXMTDigbvCsyAvIOKIkjEuOTDDlzEw4oG7wrMg
4oCUIGFuIGwgPSA0IGZpYmVyIHRleHR1cmUgKnJhaXNlcyogdGhlIEXigoItZGVzY3JpcHRvciBz
cGVlZCByZWxhdGl2ZSB0byBFTSB3aGVyZSBhbiBsID0gMiB0ZXh0dXJlIGxvd2VycyBpdDsgfM66
4oKE4oKEfC98zrrigoLigoJ8ID0gMC4xMSAvIDAuMDk1LiBIWVAtTVMyLTQncyBtYWduaXR1ZGUg
Y2xhdXNlIGNvbmZpcm1lZCAodGhlIGwgPSAyIHRlcm0gZG9taW5hdGVzIHRoZSBoZXggcmVzcG9u
c2UpLCBpdHMgY3Jvc3MtdGVybSBjbGF1c2UgcmVmdXRlZCAoYmVsb3cpLgo0LiAqKlRoZSBxdWFk
cmF0aWMgZm9ybSBpcyBkaWFnb25hbCBpbiBsOiDOuuKCguKChCA9IDAgZXhhY3RseSwgb24gZXZl
cnkga2V5LCBoZXggYW5kIGN1YmljLioqIFRoZSA3LXRlcm0gZml0cyBnaXZlIM664oKC4oKEIGF0
IDEw4oG74oG4IChoZXgpIC8gMTDigbvigbcgKGN1YmljKTsgdGhlIHBvc3QtcnVuIGRpYWdub3N0
aWMgKGBkaWFnX2thcHBhMjQucHlgLCBub3QgYSBjaGVja3BvaW50IHF1YW50aXR5KSBlc3RpbWF0
ZXMgzrrigoLigoQgYnkgUmljaGFyZHNvbi1leHRyYXBvbGF0ZWQgbWl4ZWQgc2Vjb25kIGRpZmZl
cmVuY2VzIChoID0gMC4wMiwgMC4wMTsgZXJyb3IgTyho4oG0KSkgYXQgKioxMOKBu8K5wrPigJMx
MOKBu8K5wrIqKiBvbiBhbGwgZWlnaHQga2V5cywgYW5kIGEgcXVhcnRpYy1pbmNsdXNpdmUgMTIt
dGVybSByZWZpdCBvZiB0aGUgc2FtZSA1IMOXIDUgZ3JpZCByZXR1cm5zIM664oKC4oKEID0gKzEu
N8OXMTDigbvCucKyIChoZXhfc3RlcHxhKSBhbmQg4oiSMy41w5cxMOKBu8K5wrkgKGN1YmljX3N0
ZXB8MDAxKSB3aXRoIM664oKC4oKCID0g4oiSOcOXMTDigbvCueKBtSBvbiBjdWJpYy4gKipSZWFk
aW5nIChSMik6IGF0IHNlY29uZCBvcmRlciByX2FnZyBpcyBhIHN1bSBvZiBjb3ZhcmlhbmNlcyDi
n6hhX2zCt860dl97bCd94p+pIG9mIHRoZSBsLWhhcm1vbmljIHdlaWdodCBwZXJ0dXJiYXRpb24g
YW5kIHRoZSBsJy1oYXJtb25pYyBzcGVlZCBwZXJ0dXJiYXRpb24gb3ZlciB0aGUgbW9kZSBlbnNl
bWJsZSwgYW5kIHRoZSBhdmVyYWdlIG92ZXIgdGhlIGZpYmVyIGRpcmVjdGlvbiBraWxscyBsIOKJ
oCBsJyBieSBoYXJtb25pYyBvcnRob2dvbmFsaXR5OyB0aGUgZ2VuZXJhbCB3ZWFrIGZpYmVyIHRl
eHR1cmUncyBjb25zdHJhaW50IHN1cmZhY2UgaXMgdGhlcmVmb3JlIHJfYWdnKHTigoIsIHTigoQp
ID0gzrrigoLigoJ04oKCwrIgKyDOuuKChOKChHTigoTCsiArIE8odMKzKSwgd2l0aCBjcm9zcy1j
b3VwbGluZyBiZWdpbm5pbmcgYXQgdGhpcmQgb3JkZXIqKiAoaGV4OiB04oKCwrJ04oKEID0g4oiS
Ny4zw5cxMOKBu+KBtiwgdOKCgnTigoTCsiA9IOKIkjMuOcOXMTDigbvigbY7IGN1YmljIHVuZGVy
IHRoZSBpbmhlcml0ZWQgd2VpZ2h0OiB04oKCdOKChMKyID0g4oiSNS45w5cxMOKBu+KBtSwgbm8g
dOKCgsKyIHRlcm0gb2YgYW55IGtpbmQpLiBUaGUgbm9uLXplcm8gZml0dGVkIM664oKC4oKEIHZh
bHVlcyBpbiB0aGUgY2hlY2twb2ludCBhcmUgYWxpYXNpbmcgb2YgdGhlc2UgY3ViaWMvcXVhcnRp
YyB0ZXJtcyBpbnRvIHRoZSA3LXRlcm0gYmFzaXMg4oCUIHRoZSBzY2hlbWEncyBjdWJpYy1udWxs
IHJvd3MgZmlyZSBvbiBpdCAowqc2LCDCpzcpLgo1LiAqKkZpcnN0LW9yZGVyIHByb3RlY3Rpb24g
aXMgZmFtaWx5LWluZGVwZW5kZW50KiogKEhZUC1NUzItMyk6IHxT4oKEfCDiiaQgNC4zw5cxMOKB
u8K5wrkgZXZlcnl3aGVyZS4KNi4gKipUaGUgYmlyZWZyaW5nZW5jZSBkaWZmZXJlbnRpYXRvciAo
SFlQLU1TMi01KToqKiB0aGUgTyh04oKEKSBxU0gvcVNWIHNwbGl0IG9mIHRoZSB0ZXh0dXJlZCBm
Y2MgYWdncmVnYXRlIGZvciBwcm9wYWdhdGlvbiBwZXJwZW5kaWN1bGFyIHRvIHRoZSBmaWJlciBp
cyBi4oKBID0g4oiSMy43OcOXMTDigbvCsiAvIOKIkjQuNTXDlzEw4oG7wrIgcGVyIHVuaXQgdOKC
hCAobmVnYXRpdmU6IEggPSBD4oKB4oKBIOKIkiBD4oKB4oKCIOKIkiAyQ+KChOKChCA8IDAgb24g
dGhlIGJhbmtlZCBjdWJpYyB0ZW5zb3JzOyBkZXNjcmlwdG9yLWluZGVwZW5kZW50IGFzIGl0IG11
c3QgYmUpOyBhdCB04oKEID0gMC4yNSB0aGUgYmlyZWZyaW5nZW5jZSBpcyB+McOXMTDigbvCsiBh
Z2FpbnN0IGEgZGVzY3JpcHRvciBzcGxpdCBvZiB+Mi4zw5cxMOKBu+KBtSDigJQgdGhlIGRlc2Ny
aXB0b3Igc3BsaXQgaXMgYSBzZWNvbmQtb3JkZXIgc2hhZG93LCB0d28gdG8gdGhyZWUgb3JkZXJz
IGJlbG93IHRoZSBmaXJzdC1vcmRlciBiaXJlZnJpbmdlbmNlIHRoYXQgdWx0cmFzb25pYyB0ZXh0
dXJlIG1lYXN1cmVtZW50IHJlYWRzIChMLU1TMi00KS4gT24gaGV4LCBi4oKBID0gKzEuNjLDlzEw
4oG7wrIgLyArMS44MsOXMTDigbvCsi4KNy4gKipNYWduaXR1ZGUgKEhZUC1NUzItMSByZWZ1dGVk
IGluIGl0cyBtYWduaXR1ZGUgY2xhdXNlKToqKiB8zrrigoTigoR8IG9uIHRoZSBmY2MgYnJhbmNo
IGlzIDIuNeKAkzQuNcOXMTDigbvigbQsIGJlbG93IHRoZSBNLW5haXZlIDEw4oG7wrPigJMxMOKB
u8KyIGFuZCBiZWxvdyB0aGUgaGV4IGwgPSAyIGNvZWZmaWNpZW50IOKAlCB0aGUgbCA9IDQgaGFy
bW9uaWMgY291cGxlcyB0aGUgZGVzY3JpcHRvciBwYWlyIG1vcmUgd2Vha2x5IHRoYW4gbCA9IDIg
ZGlkIG9uIGhleCwgZGVzcGl0ZSB0aGUgbGFyZ2VyIGN1YmljIHRyYW5zdmVyc2UgYW5pc290cm9w
eS4gUmVjb3JkZWQgYXMgYSByZWZ1dGVkIGV4cGVjdGF0aW9uICgzLzUgaHlwb3RoZXNlcyBjb25j
b3JkYW50OiBIWVAtTVMyLTIsIC0zLCAtNSkuCgojIyA0LiBXaGF0IHRoZSBnYXRlIGFkZHMgdG8g
dGhlIGNvbnN0cmFpbnQgc3VyZmFjZSAoUjIsIGNvbmRpdGlvbmFsIGFzIGluIG1lbW8gwqc5KQoK
V2l0aCBHLU1TQ1MxJ3MgzrrigoIgKGhleCkgYW5kIHRoaXMgZ2F0ZSdzIM664oKE4oKEIChoZXgg
YW5kIGZjYykgYW5kIHRoZSBkaWFnb25hbGl0eSByZXN1bHQsIHRoZSBzcGVjaWVzLXVuaXZlcnNh
bGl0eSBjb25zdHJhaW50IHN1cmZhY2UgZm9yIHRoZSBnZW5lcmFsIHdlYWsgYXhpc3ltbWV0cmlj
IHRleHR1cmUgb2YgdGhlIHZhY3V1bSBwb2x5Y3J5c3RhbCBpcywgb24gZXZlcnkgY29uZmlndXJh
dGlvbiwgKipyX2FnZyA9IM664oKC4oKCdOKCgsKyICsgzrrigoTigoR04oKEwrIqKiB3aXRoIGFs
bCBmb3VyIGNvZWZmaWNpZW50cyBkZWxpdmVyZWQgKM664oKC4oKCIOKJoSAwIG9uIGZjYyksIHBs
dXMgdGhlIFMyLWggYWRtaXh0dXJlIGFybS4gTm90aGluZyBoZXJlIGV2YWx1YXRlcyB04oKCIG9y
IHTigoQ7IG5vdGhpbmcgdG91Y2hlcyBhbnkgYm91bmQ7IHRoZSBraWxsIHN1cmZhY2UgcmVtYWlu
cyB3aGVyZSBHLU1TQ1MxIMKnNSBwdXQgaXQuIFRoZSBmY2MgYnJhbmNoIG5vdyBoYXMgYSBjdXJ2
ZSBhIGZ1dHVyZSBzZWFsZWQtYW5jaG9yIG1pbmktZ2F0ZSBjb3VsZCBjb21wYXJlIG9uLgoKIyMg
NS4gUGhhc2UgMCAocmVjb21wdXRlZCBpbiB0aGlzIHJ1bjsgaWRlbnRpY2FsIHRvIHRoZSBQaGFz
ZS0wIHJlcG9ydCBgYjZhOTY2OTJgKQoKUElOLVhUQUwgLyBQSU4tVlJIMCAvIFBJTi1IUzAgPSAw
IChiaXQtaWRlbnRpY2FsIHRvIEctTVNDUzEpOyBQSU4tSzIgMS40w5cxMOKBu8K5wrIgKGhleCkg
LyAyLjLDlzEw4oG7wrnigbUgKGN1YmljKTsgRi1DVFJMLUlTTyA0w5cxMOKBu8K54oG2OyBGLUNU
UkwtU08zIDXDlzEw4oG7wrnigbYgLyAwOyBGLUNUUkwtUE9TIDAuMzk1OyBGLUNUUkwtTDJOVUxM
IDUuOMOXMTDigbvCueKBtDsgRi1DVFJMLUw0RVhIQVVTVCA0LjPDlzEw4oG7wrnigbQgLyA0LjTD
lzEw4oG7wrnigbY7IEYtQ1RSTC1DNCAyLjXDlzEw4oG7wrnigbQgLyA0LjHDlzEw4oG7wrnigbQg
LyAyLjPDlzEw4oG7wrnigbQ7IEYtQ1RSTC1NQVJHIDguM8OXMTDigbvCueKBtjsgRi1DVFJMLVRF
WDQgNC4xw5cxMOKBu+KBtDsgRi1DVFJMLVFVQUQgMi4zw5cxMOKBu8K54oG0LgoKIyMgNi4gQ2hh
dC12cy1jaGF0IGNvbXBhcmF0b3Igc2FuaXR5ICh2MS4wIGZyb3plbiwgb24gdGhlIGNoZWNrcG9p
bnQgYWdhaW5zdCBpdHNlbGYpCgozNTYgY2hlY2tzLCAqKjMzOCBQQVNTLCAxOCBNSVNTKio6IHRo
ZSB0d28gc3RydWN0dXJhbCBzZWxmLWNvbXBhcmlzb24gcm93cyAobGVnIGxhYmVsczsgaWRlbnRp
Y2FsIGluc3RydW1lbnQgbWQ1KSBhbmQgKipzaXh0ZWVuIGBxdWFkZm9ybWAgY3ViaWMtbnVsbCBy
b3dzKiogKM664oKC4oKCIGFuZCDOuuKCguKChCBvbiB0aGUgZm91ciBjdWJpYyBrZXlzLCBib3Ro
IGNvbHVtbnMpIOKAlCB0aGUgc2NoZW1hJ3MgMTDigbvCueKBsCBudWxsIHRvbGVyYW5jZSBhZ2Fp
bnN0IHRoZSA3LXRlcm0gZml0J3MgMTDigbvigbkvMTDigbvigbcgYWxpYXNpbmcgdmFsdWVzLiBF
eHBlY3RlZCBpbiB0aGUgdHdvLWxlZyBydW46IHRoZSBlaWdodCBjaGF0LWNvbHVtbiByb3dzIG1p
c3MgZm9yIHRoZSBzYW1lIHJlYXNvbiAocHJlLWNsYXNzaWZpZWQgZGVmaW5pdGlvbmFsLCDCpzcp
OyB0aGUgQ0MtY29sdW1uIHJvd3MgZGVwZW5kIG9uIENDJ3Mgb3BlcmF0aW9uYWxpemF0aW9uLiBF
dmVyeXRoaW5nIHZlcmRpY3QtYmVhcmluZyBwYXNzZXMuCgojIyA3LiBIb25lc3R5IGl0ZW1zIGFu
ZCBvcGVyYXRpb25hbGl6YXRpb25zIChjaGF0IHNpZGUpCgotICoqSC1NUzItNCAoc2NoZW1hIGV4
cGVjdGF0aW9uIHZzIHRoZSBpbmhlcml0ZWQgY3ViaWMgbCA9IDIgZGVmaW5pdGlvbjsgcHJlLXZl
cmRpY3QsIG5vbi12ZXJkaWN0LWJlYXJpbmcpLioqIE1lbW8gwqcyLjUgLyBBLTIuMyAvIHRoZSBz
Y2hlbWEgYXNzZXJ0IM664oKC4oKCID0gzrrigoLigoQgPSAwIG9uIGN1YmljIGF0IDEw4oG7wrni
gbAgYXMgInRoZSBsID0gMiBudWxsIi4gVGhhdCBpcyBleGFjdCBmb3IgdGhlICp0ZW5zb3IqIChG
LUNUUkwtTDJOVUxMLCA1LjjDlzEw4oG7wrnigbQpIGFuZCBleGFjdCBmb3IgzrrigoLigoQgKHRo
ZSBkaWFnb25hbGl0eSBmaW5kaW5nLCDCpzMuNCkg4oCUIGJ1dCB0aGUgY3ViaWMgKHTigoIsIHTi
goQpIGZvcm0gYXMgb3BlcmF0aW9uYWxpemVkIGluaGVyaXRzIEctTVNDUzEncyBjdWJpYyBsID0g
MiB3ZWlnaHQsIDEgKyB04oKCUOKCgiBvbiB0aGUgKmVsZWN0ZWQgZGVzY3JpcHRvciBheGlzKiwg
d2hpY2ggaXMgbm90IGFuIE9faC1pbnZhcmlhbnQgT0RGOyB0aGUgdGVuc29yIGlzIGJsaW5kIHRv
IGl0LCB0aGUgc2luZ2xlLWF4aXMgReKCgiB3ZWlnaHQgaXMgbm90IChpdCBoYXMgbCA9IDIgY29u
dGVudCksIHNvIHVuZGVyIGl0IHJfYWdnIGFjcXVpcmVzIG9kZC1pbi104oKCIGNyb3NzIHRlcm1z
IGF0ICoqdGhpcmQgb3JkZXIqKiAodOKCgnTigoTCsiA9IOKIkjUuOcOXMTDigbvigbUgb24gY3Vi
aWNfc3RlcHwwMDEpIHdoaWNoIHRoZSA3LXRlcm0gZml0IGFsaWFzZXMgaW50byDOuuKCguKChCBh
dCAxMOKBu+KBtyBhbmQgzrrigoLigoIgYXQgMTDigbvigbkuIFVuZGVyIHRoZSBvbmx5IGxlZ2l0
aW1hdGUgY3ViaWMgT0RGIChPX2gtc3ltbWV0cml6ZWQpIHRoZSBsID0gMiB0ZXJtIGlzIGlkZW50
aWNhbGx5IGFic2VudCBhbmQgdGhlIG51bGwgaXMgdHJpdmlhbC4gKipUd28gZGVmZWN0cywgYm90
aCBtaW5lLCByZWNvcmRlZDoqKiAoaSkgdGhlIG1lbW8vbG9jayByZWNvcmQgZGlkIG5vdCBzYXkg
d2hpY2ggcmVhZGluZyB0aGUgY3ViaWMgdHdvLXBhcmFtZXRlciBmb3JtIHRha2VzIChhIEctTVND
UzEtaW5oZXJpdGVkIGFtYmlndWl0eSB0aGF0IGRpZCBub3QgbWF0dGVyIHRoZXJlIGJlY2F1c2Ug
dGhlIHNwZWVkcyB3ZXJlIGlzb3Ryb3BpYyk7IChpaSkgdGhlIHNjaGVtYSdzIGN1YmljLW51bGwg
dG9sZXJhbmNlIGFzc3VtZWQgYSBmaXQgYmFzaXMgdGhhdCBjYW5ub3QgcmVzb2x2ZSBhIG51bGwg
YmVsb3cgdGhlIGFsaWFzaW5nIGxldmVsLiBUaGUgY2hlY2twb2ludCBzdGFuZHMgYXMgY29tcHV0
ZWQ7IG5vdGhpbmcgdmVyZGljdC1iZWFyaW5nIGlzIGFmZmVjdGVkLgotICoqSC1NUzItNSAoY29u
dHJvbCB3b3JkaW5nIHZzIGltcGxlbWVudGF0aW9uOyBkaXNjbG9zZWQpLioqIExvY2sgcmVjb3Jk
IEEtMi45IHN0YXRlcyBGLUNUUkwtTDJOVUxMJ3MgbWl4ZWQgY2xhdXNlIGFzICIodOKCgiwgdOKC
hCkgPSAoMC4yNSwgMC4yNSkgdnMgKDAsIDAuMjUpIGxlYXZlIOKfqEPin6lfViwg4p+oU+KfqV9S
LCBDX0hTICoqYW5kIHJfYWdnKiogdW5jaGFuZ2VkIHRvIDEw4oG7wrnCsiIuIFRoZSBjaGF0IGlu
c3RydW1lbnQgdGVzdGVkIHRoZSB0aHJlZSB0ZW5zb3IgY2xhdXNlcyBmb3IgdGhlIG1peGVkIHRl
cm0gKGFsbCBleGFjdCkgYW5kIHRoZSByX2FnZyBjbGF1c2Ugb25seSBmb3IgdGhlIHB1cmUgbCA9
IDIgdGVybSAoZXhhY3QsIGlzb3Ryb3BpYyBzcGVlZHMpIOKAlCBpdCBkaWQgKipub3QqKiB0ZXN0
IHRoZSByX2FnZyBjbGF1c2UgZm9yIHRoZSBtaXhlZCB0ZXJtLiBNZWFzdXJlZCBwb3N0IGhvYyAo
ZGlhZ25vc3RpYywgbm90IHRoZSBjaGVja3BvaW50KTogdGhlIG1peGVkLXRlcm0gcl9hZ2cgY2hh
bmdlIGlzICoqOS4xw5cxMOKBu+KBtyAoY3ViaWM6c3RlcCkgLyAxLjPDlzEw4oG74oG2IChjdWJp
YzpnZW04KSoqIOKAlCB0aGUgdGhpcmQtb3JkZXIgdOKCgnTigoTCsiBjcm9zcyB0ZXJtIG9mIEgt
TVMyLTQuIFNvIHRoZSBjb250cm9sIGFzICp3b3JkZWQqIHdvdWxkIGhhdmUgRkFJTEVEIG9uIGEg
bGl0ZXJhbCBpbXBsZW1lbnRhdGlvbiwgc2VuZGluZyB0aGUgbGVnIHRvIElOREVURVJNSU5BVEUg
b24gYSB3cm9uZyBhLXByaW9yaSBleHBlY3RhdGlvbiwgbm90IG9uIHBoeXNpY3M7IHRoZSBjb250
cm9sIGFzICppbXBsZW1lbnRlZCogcGFzc2VkIG9uIHRoZSBpZGVudGl0aWVzIHRoYXQgYXJlIHRy
dWUuICoqQSBDQyBsZWcgaW1wbGVtZW50aW5nIEEtMi45IGxpdGVyYWxseSB3aWxsIGhhbHQuKiog
VGhlIHJlbWVkeSBpcyBkZWZpbml0aW9uYWwsIG5vdCBudW1lcmljYWw6ICoqQWRkZW5kdW0gQS0z
IChwcm9wb3NlZCBiZWxvdzsgZm9yIHRoZSBhdXRob3IncyBhdXRob3JpemF0aW9uLCBzZWxlY3Rh
YmxlIGF0IGRpc3BhdGNoIGJ5IHRoZSBhY3RpdmF0aW9uIGZsYWcpKiogc2NvcGVzIHRoZSByX2Fn
ZyBjbGF1c2UgdG8gdGhlIHB1cmUgbCA9IDIgdGVybSwgcmVjbGFzc2lmaWVzIHRoZSBtaXhlZC10
ZXJtIHJfYWdnIGNoYW5nZSBhcyBhIHJlcG9ydGVkIGRpYWdub3N0aWMsIGFuZCBhZGRzIHRoZSBi
YXNpcy1pbmRlcGVuZGVudCDOuuKCguKChCBlc3RpbWF0ZSBhcyBhIHJlcG9ydGVkIHF1YW50aXR5
LiBUaGUgdmVyZGljdCBjbGFzcyBkb2VzIG5vdCBkZXBlbmQgb24gYW55IG9mIHRoaXMuCi0gKipI
LU1TMi02IChob3VzZWtlZXBpbmcsIHJlY29yZGVkIG5vdCByZXNvbHZlZCkuKiogVGhlIGF1dGhv
cidzIGRpcmVjdGl2ZSBvZiBTZXB0ZW1iZXIgMjYgKDA4OjQ4IFBEVCkgc3RhdGVzIHRoZSBISy0x
IHdvcmsgbWVyZ2VkIGFzICJQUiAjMjYgKGdtc2NzMSBlc3RhdGUpIGFuZCBQUiAjMjcgKFY0Ljc5
IHJlbW92YWwpIi4gQXQgMTU6NTAgVVRDIHRoZSBsaXZlIHJlbW90ZSBpcyB1bmNoYW5nZWQ6IGBt
YWluYCA9IGBkMGEwZTMxYDsgbm8gYGdtc2NzMV9nYXRlL2VzdGF0ZS9gIG9uIGFueSBicmFuY2g7
IHRoZSBWNC43OSBjYW5vbmljYWwgYXQgdGhlIHJvb3Q7ICoqUFIgIzI2IGluIHRoZSByZXBvc2l0
b3J5IGlzIHRoZSBnMmFhMSBmb2xkLXNpZGUgZXN0YXRlIChlM2RmNDAyLCBTZXB0ZW1iZXIgMjIp
IGFuZCBubyBQUiAjMjcgZXhpc3RzIGluIGBtYWluYCdzIGhpc3RvcnkuKiogUmVjb3JkZWQgYXMg
b2JzZXJ2ZWQ7IHRoZSBWNC44NSBicmFja2V0IHdpbGwgY2Fycnkgd2hhdGV2ZXIgdGhlIHJlcG9z
aXRvcnkgc2hvd3MgYXQgZm9sZCB0aW1lLgotICoqUHJvY2VzcyBub3RlIGZvciB0aGUgbmV4dCBn
YXRlOioqIGEgY29udHJvbCB0aGF0IG5hbWVzICJyX2FnZyB1bmNoYW5nZWQiIG11c3Qgc2F5IHVu
ZGVyIHdoaWNoIE9ERiAqcmVhZGluZyo7IGEgc2NoZW1hIG51bGwgdG9sZXJhbmNlIG11c3QgYmUg
c2V0IGF0IHRoZSBmaXQncyByZXNvbHV0aW9uIG9yIHRoZSBmaXQgYmFzaXMgbXVzdCBiZSBjaG9z
ZW4gdG8gcmVzb2x2ZSBpdDsgZXZlcnkgaW5oZXJpdGVkIGRlZmluaXRpb24gKGhlcmUgRy1NU0NT
MSdzIGN1YmljIGwgPSAyIHdlaWdodCkgbmVlZHMgYSBvbmUtbGluZSByZS1kZXJpdmF0aW9uIG9m
IHdoYXQgaXQgbWVhbnMgaW4gdGhlIG5ldyBjb250ZXh0IGJlZm9yZSBsb2NrLgoKIyMgOC4gUHJv
cG9zZWQgQWRkZW5kdW0gQS0zIHRvIHRoZSBsb2NrIHJlY29yZCAoZGVmaW5pdGlvbmFsOyBubyBu
dW1iZXIgY2hhbmdlczsgYXV0aG9yJ3MgYXV0aG9yaXphdGlvbiByZXF1aXJlZDsgc2NoZW1hL2Nv
bXBhcmF0b3IgdjEuMCBzdGF5IGZyb3plbikKCi0gKipBLTMuMSBGLUNUUkwtTDJOVUxMIHNjb3Bl
LioqIFRoZSByX2FnZyBjbGF1c2UgYXBwbGllcyB0byB0aGUgcHVyZSBsID0gMiB0ZXJtICh04oKE
ID0gMCksIHdoZXJlIGl0IGlzIGFuIGlkZW50aXR5OyBmb3IgdGhlIG1peGVkICh04oKCLCB04oKE
KSB0ZXJtIG9ubHkgdGhlIHRlbnNvciBjbGF1c2VzICjin6hD4p+pX1YsIOKfqFPin6lfUiwgQ19I
UyB1bmNoYW5nZWQg4omkIDEw4oG7wrnCsikgYXJlIHRoZSBjb250cm9sLiBUaGUgbWl4ZWQtdGVy
bSByX2FnZyBjaGFuZ2UgdW5kZXIgdGhlIGluaGVyaXRlZCBkZXNjcmlwdG9yLWF4aXMgbCA9IDIg
d2VpZ2h0IGlzIGEgKipyZXBvcnRlZCBkaWFnbm9zdGljKiogYG1peGVkX3JfYWdnX2NoYW5nZV9B
MjlgIChwZXIgY3ViaWMga2V5OyBub3QgdmVyZGljdC1iZWFyaW5nKS4KLSAqKkEtMy4yIM664oKC
4oKEIGJ5IGEgYmFzaXMtaW5kZXBlbmRlbnQgZXN0aW1hdG9yLioqIEV2ZXJ5IGxlZyByZXBvcnRz
LCBwZXIga2V5LCBga2FwcGEyNF9yaWNoYXJkc29uYCA9ICg0RChoLzIpIOKIkiBEKGgpKS8zIHdp
dGggRChoKSA9IFtyKGgsaCkg4oiSIHIoaCziiJJoKSDiiJIgcijiiJJoLGgpICsgcijiiJJoLOKI
kmgpXS8oNGjCsiksIGggPSAwLjAyLCBvbiB0aGUgc2FtZSBPREYgcmVhZGluZyBhcyBpdHMgcXVh
ZHJhdGljIGZvcm07IHRoZSA3LXRlcm0gcXVhZGZvcm0gc3RheXMgYXMgc3BlY2lmaWVkIGFuZCBp
cyBjb21wYXJlZCBhcyBzcGVjaWZpZWQ7IHRoZSBzY2hlbWEncyBjdWJpYy1udWxsIHJvd3MgYXJl
IHByZS1jbGFzc2lmaWVkIGRlZmluaXRpb25hbCB3aGVyZSB0aGV5IG1pc3Mgb24gdGhlIDctdGVy
bSBiYXNpcy4KLSAqKkEtMy4zIFRoZSBjdWJpYyB0d28tcGFyYW1ldGVyIHJlYWRpbmcuKiogTGVn
cyBzdGF0ZSB3aGljaCByZWFkaW5nIHRoZXkgdG9vayBmb3IgdGhlIGN1YmljICh04oKCLCB04oKE
KSBmb3JtIOKAlCAoaSkgdGhlIGluaGVyaXRlZCBkZXNjcmlwdG9yLWF4aXMgUOKCgiAoRy1NU0NT
MSdzIGN1YmljIGwgPSAyKSBvciAoaWkpIHRoZSBPX2gtc3ltbWV0cml6ZWQgbCA9IDIgdGVybSAo
aWRlbnRpY2FsbHkgemVybywgc28gdGhlIGZvcm0gcmVkdWNlcyB0byDOuuKChOKChHTigoTCsikg
4oCUIGFzIGEgQ0MtREQvSCBpdGVtOyBib3RoIGFyZSBhZG1pc3NpYmxlIHVuZGVyIEEtMi4zJ3Mg
d29yZGluZzsgdGhlIHR3by1sZWcgY29tcGFyaXNvbiBvZiDOuuKCguKCgi/OuuKCguKChCB0aGVu
IGNsYXNzaWZpZXMgYWNjb3JkaW5nbHkuCgojIyA5LiBSZWdpc3RlcnMgYW5kIG5vbi1jbGFpbXMg
KGFzIGxvY2tlZCkKCkV2ZXJ5IGNoZWNrIGFuZCBjb2VmZmljaWVudCBSMS1tYWNoaW5lIChjaGF0
IGxlZyk7IHRoZSB2ZXJkaWN0IGNsYXNzIGFuZCB0aGUgY29uc3RyYWludC1zdXJmYWNlIHJlYWRp
bmcgUjIsIGNvbmRpdGlvbmFsIG9uIEUtTVMtMShhKSwgdGhlIHVudGV4dHVyZWQgaW1wb3J0LCBL
ID0g4oiFLCB0aGUga2VybmVsIGVsZWN0aW9uIGFuZCBBLTIuNDsgdGhlIGRpYWdvbmFsaXR5IHJl
YWRpbmcgKGhhcm1vbmljIG9ydGhvZ29uYWxpdHkpIFIyIHBlbmRpbmcgdHdvLWxlZyBjb25maXJt
YXRpb24gb2YgdGhlIFJpY2hhcmRzb24gZXN0aW1hdGVzOyB0aGUgcG9seWNyeXN0YWwgcG9zdHVs
YXRlIFIzLiBObyBvYnNlcnZhYmxlLCBubyBicmlkZ2UsIG5vIFNJIHZhbHVlLCBubyB2YWx1ZSBv
ZiB04oKCIG9yIHTigoQsIG5vIGV2YWx1YXRpb24gYWdhaW5zdCBhbnkgYm91bmQ7IG5vIGtpbGwg
Y2xhaW1lZCBvciBwb3NzaWJsZSBoZXJlOyDCpzIuNTIgT3BlbiAzIHVudG91Y2hlZC4KCiMjIDEw
LiBOZXh0IHN0ZXBzIChwZXIgdGhlIGxvY2tlZCBvcmRlciBvZiBvcGVyYXRpb25zKQoKUC00L1At
NC5jIGRpc3BhdGNoICh0aGlzIHJlcG9ydCwgdGhlIGNoZWNrcG9pbnQgYW5kIHRoZSBkaWFnbm9z
dGljcyBhcm1vcmVkOyB0aGUgbWVtbywgbG9jayByZWNvcmQsIHNjaGVtYSwgY29tcGFyYXRvciwg
VDEgbGlzdHMsIFgtMSwgWC02IGluIHRoZSBjbGVhcjsgdGhlIEEtMyBwcm9wb3NhbCBpbiB0aGUg
Y2xlYXIgd2l0aCB0d28gYWN0aXZhdGlvbiBmbGFncyBmb3IgdGhlIGF1dGhvcidzIGNob2ljZSkg
4oaSIENDIGxlZyBibGluZCBmcm9tIHNjcmF0Y2gg4oaSIHR3by1sZWcgY29tcGFyaXNvbiAodjEu
MCkg4oaSIFM5IG9uIG1pc3NlcyAodGhlIDggY2hhdC1jb2x1bW4gY3ViaWMtbnVsbCByb3dzIHBy
ZS1jbGFzc2lmaWVkKSDihpIgYXV0aG9yJ3MgZWxlY3Rpb24gKHYxLjEgY2FuZGlkYXRlczogdGhl
IHF1YXJ0aWMtaW5jbHVzaXZlIGJhc2lzIG9yIHRoZSBudWxsIHRvbGVyYW5jZSBhdCB0aGUgYWxp
YXNpbmcgbGV2ZWw7IGBrYXBwYTI0X3JpY2hhcmRzb25gIGFzIGEgc2NoZW1hIGtleSkg4oaSIGZv
bGQgYXV0aG9yaXphdGlvbiDihpIgVjQuODUuCg==
=====END-EMBED name=G_MSCS2_CHATLEG_EXECUTION_REPORT.md=====

=====BEGIN-EMBED name=G_MSCS2_PHASE0_EXECUTION_REPORT.md md5=b6a966920a34552e0f0e2dd91f2e969f bytes=8207 encoding=base64 armor_bytes=11088 QUARANTINED=====
IyBHLU1TQ1MyIOKAlCBDSEFULUxFRyBQSEFTRSAwIEVYRUNVVElPTiBSRVBPUlQgKHBpbnMgYW5k
IGNvbnRyb2xzKQoKKipEYXRlOioqIFNlcHRlbWJlciAyNiwgMjAyNiAocnVuIGF0IDE0OjMzIFVU
QzsgNCBtIDAwIHMpLiAqKkJhc2U6KiogVjQuODQgYGYzNmJiZGIwYC4gKipNZW1vIGxvY2s6Kiog
djIgYGVmZGNhYmRjZDkzN2NkYTRhY2I2NGY5NDFkYzRiYjJiYCAoNDYsMDUzIEIpLiAqKkxvY2sg
cmVjb3JkOioqIGA0OTIzMmQ0Y2AgKEFkZGVuZHVtIEEtMi4x4oCTQS0yLjEwKS4gKipTY2hlbWEg
djEuMCoqIGA2NmY1ODZkN2AgKyAqKmNvbXBhcmF0b3IgdjEuMCoqIGA4MGQzYjkwN2AgKDE4LzE4
IHN1aXRlcykg4oCUIEZST1pFTiBiZWZvcmUgdGhpcyBlbWlzc2lvbi4gKipUMSBnYXRlIGxpc3Qq
KiBgYmU5MjFiOGNgICgzNiBwYXR0ZXJuczsgc2Nhbm5lciBgNmI4NjI5MDBgKS4gKipJbnN0cnVt
ZW50OioqIGBnX21zY3MyX2NoYXRsZWcucHlgIGBmMjc3NTgwZGRmMGI0ZGE5NzM0ZDExZWRiMDA5
YzU0YmAgKDcvNyBzZWxmdGVzdCBzdWl0ZXMpLiAqKkNoZWNrcG9pbnQgKFBoYXNlIDAsIHBhcnRp
YWwgYnkgZGlyZWN0aXZlKToqKiBgZ19tc2NzMl9jaGF0bGVnX3BoYXNlMF9jaGVja3BvaW50Lmpz
b25gIGA5ZTVhNmU4YmEwODA0YmRhNzc4ZTRiZTUyZmJlMmZkZWAgKDcsNzQ3IEIpOyBydW4gbG9n
IGA3MmQ2NGFlYmAuIFQxOiBpbnN0cnVtZW50LCBtZW1vIGFuZCBjaGVja3BvaW50IENMRUFOICho
YWx0LW9uLWhpdDsgbm8gb3ZlcnJpZGUgcGF0aCk7IG9uZSBudW1lcmljIGZvcm1hdHRpbmcgY29s
bGlzaW9uIGxvZ2dlZCBpbiB0aGUgbG9nIGZpbGUgdW5kZXIgdGhlIGNvbnRleHR1YWwgcnVsZSAo
MCBoaXRzKS4KCioqU2NvcGUgb2YgdGhpcyBydW4gKHRoZSBhdXRob3IncyBkaXJlY3RpdmUgb2Yg
U2VwdGVtYmVyIDI2LCAyMDI2KToqKiBQaGFzZSAwIG9ubHkuIFBoYXNlcyAy4oCTMyBhcmUgaW1w
bGVtZW50ZWQgaW4gdGhlIGluc3RydW1lbnQgYW5kIHdlcmUgKipub3QgZXhlY3V0ZWQqKjsgdGhl
IHZlcmRpY3QgY2xhc3MgaXMgTk9UIEFTU0VNQkxFRC4gR3VhcmRzIGhlbGQ6IG1lbW8gbWQ1K2J5
dGVzLCBUMSBsaXN0IG1kNSwgc2Nhbm5lciBtZDUsIFgtMSBgMjAwZTdhOGJgIChtZDUrYnl0ZXMp
LCBYLTYgY2hhdCBgYzA0YzBiOGVgIGFuZCBjYyBgMjQ5ZTExZGRgLgoKIyMgMS4gUmVzdWx0OiBh
bGwgMTMgcGlucyBhbmQgY29udHJvbHMgUEFTUwoKfCBJdGVtIHwgVGhyZXNob2xkIHwgVmFsdWUg
fCBSZWFkaW5nIHwKfC0tLXwtLS18LS0tfC0tLXwKfCAqKlBJTi1YVEFMKiog4oCUIHJfeHRhbCAo
Ym90aCBhcm1zKSwg4p+ozrtfTOKfqSwgbWF4IM67X0wgb24gdGhlIDgga2V5cyB2cyBYLTYgfCB3
b3JzdCByZWwg4omkIDEw4oG74oG4IHwgKiowKiogKGJpdC1pZGVudGljYWwpIHwgdGhlIGluaGVy
aXRlZCBzaW5nbGUtY3J5c3RhbCBtYWNoaW5lcnkgcmVwcm9kdWNlcyBHLU1TQ1MxIGV4YWN0bHkg
fAp8ICoqUElOLVZSSDAqKiDigJQgdl9UKHQgPSAwKSBWb2lndCAvIFJldXNzIC8gSGlsbCBvbiB0
aGUgOCBrZXlzIHZzIFgtNiB8IOKJpCAxMOKBu+KBuCB8ICoqMCoqIHwgaWRlbSB8CnwgKipQSU4t
SFMwKiog4oCUIHZfVChIUyBsby9oaSksIEdfSFMgYm91bmRzIGFuZCB0aGUgb3B0aW1pemVkIHJl
ZmVyZW5jZXMgdnMgWC02IHwg4omkIDEw4oG74oG2IHwgKiowKiogfCB0aGUgQS0yLjMgcmVmZXJl
bmNlIG9wdGltaXphdGlvbiByZXByb2R1Y2VkIChyZWZlcmVuY2VzIGxpc3RlZCBpbiB0aGUgY2hl
Y2twb2ludCB3aXRuZXNzKSB8CnwgKipQSU4tSzIqKiDigJQgdGhlIGwgPSAyIGZhbWlseSByZS1y
dW4gd2l0aCB0aGlzIGdhdGUncyBPREYgbWFjaGluZXJ5OiDOuuKCgihTMi1F4oKCLCBIaWxsKSBv
biB0aGUgNCBoZXgga2V5cyB2cyBYLTY7IGN1YmljIG51bGwgfCBoZXggcmVsIOKJpCAxMOKBu+KB
tDsgY3ViaWMgYWJzIOKJpCAxMOKBu8K5wrIgfCAqKjEuMznDlzEw4oG7wrnCsioqIC8gKioyLjE2
w5cxMOKBu8K54oG1KiogfCDiiJIxLjQzOTQ2MTc2OSAvIOKIkjEuNDM4NzAyNzE5IC8g4oiSMS44
OTU2NDg0ODMgLyDiiJIxLjg5NjEzNzQ2NyDDlzEw4oG7wrMgcmVwcm9kdWNlZCB0byAxMiBkaWdp
dHM7IHRoZSBjdWJpYyBsID0gMiBudWxsIHJlcHJvZHVjZWQgKHzOuuKCgnwg4omkIDIuMsOXMTDi
gbvCueKBtSkg4oCUICoqdGhlIGNvbnRpbnVpdHkgcGluIHRoYXQgbWFrZXMgzrrigoTigoQgY29t
cGFyYWJsZSB0byBHLU1TQ1MxJ3MgzrrigoIqKiB8CnwgKipGLUNUUkwtSVNPKiog4oCUIGlzb3Ry
b3BpYyB0ZW5zb3I6IHJfeHRhbCwgzrtfbWF4LCByX2FnZyh04oKEKSBib3RoIGZhbWlsaWVzIHwg
4omkIDEw4oG7wrnigbAgfCA0LjTDlzEw4oG7wrnigbYgfCB0ZXh0dXJlIG9uIGFuIGlzb3Ryb3Bp
YyBncmFpbiBkb2VzIG5vdGhpbmcgfAp8ICoqRi1DVFJMLVNPMyoqIOKAlCBPREYtYXZlcmFnZWQg
ReKCgiBmcmFjdGlvbiA9IDIvNSBmb3IgZXZlcnkgbW9kZSBhdCB0ID0gMDsgcl9hZ2coMCkgfCDi
iaQgMTDigbvCueKBsDsg4omkIDEw4oG74oG2IHwgNS4ww5cxMOKBu8K54oG2OyAwIHwgdGhlIFNP
KDMpIGlkZW50aXR5IHwKfCAqKkYtQ1RSTC1QT1MqKiDigJQgbWluIE9ERiB3ZWlnaHQgb3ZlciB0
aGUgU08oMykgZ3JpZCwgZXZlcnkgZmFtaWx5L2dyaWQgdXNlZCAoaW5jbC4gdGhlIGV4aGF1c3Rp
b24gcHJvYmVzKSB8IOKJpSAwIHwgMC4zOTUgfCBhbGwgT0RGcyBwb3NpdGl2ZSB8CnwgKipGLUNU
UkwtTDJOVUxMKiog4oCUIGN1YmljOiBsID0gMiBhdCB0ID0gMSwgYW5kIFDigoIgYWRkZWQgdG8g
dGhlIEvMg+KChCBmYW1pbHksIGxlYXZlIOKfqEPin6lfViwg4p+oU+KfqV9SLCBDX0hTIGFuZCBy
X2FnZyB1bmNoYW5nZWQgfCDiiaQgMTDigbvCucKyIHwgNS44w5cxMOKBu8K54oG0IHwgdGhlIGN1
YmljIGwgPSAyIG51bGwgaG9sZHMgam9pbnRseSB3aXRoIGwgPSA0ICjOuuKCguKCgiA9IM664oKC
4oKEID0gMCBvbiBjdWJpYyBpcyBhbiBpZGVudGl0eSkgfAp8ICoqRi1DVFJMLUw0RVhIQVVTVCoq
IOKAlCBhbiBsID0gNiB0ZXJtICh04oKGID0gMC4zOyBoZXggUOKChiAvIGN1YmljIEvMg+KChikg
b24gdG9wIG9mIHTigoQgPSAwLjMgY2hhbmdlcyB0ZW5zb3JzIGFuZCByX2FnZyB8IOKJpCAxMOKB
u8K5wrIgfCB0ZW5zb3JzIDQuM8OXMTDigbvCueKBtDsgcl9hZ2cgNC40w5cxMOKBu8K54oG2IHwg
KiplbGFzdGljaXR5IGFuZCB0aGUgZGVzY3JpcHRvciBwYWlyIHNlZSB0aGUgT0RGIG9ubHkgdGhy
b3VnaCBsIOKJpCA0IOKAlCB0aGUgKHTigoIsIHTigoQpIGZhbWlseSBpcyB0aGUgZ2VuZXJhbCBh
eGlzeW1tZXRyaWMgd2VhayB0ZXh0dXJlIGZvciB0aGlzIGdhdGUqKiB8CnwgKipGLUNUUkwtQzQq
KiDigJQg4p+oQ+KfqV9WKHTigoQpIOKIkiDin6hD4p+pX1YoMCkgPSB04oKEwrcoSC8zKcK38J2S
r+KBtCjhupEpIChWb2lndCBlbnRyaWVzIDMsIDMsIDggLyAxIC8g4oiSNCwg4oiSNCAvIOKIkjQs
IOKIkjQgLyAxIG92ZXIgMTA1LCBIID0gQ+KCgeKCgSDiiJIgQ+KCgeKCgiDiiJIgMkPigoTigoQp
OyBSZXVzcyBsaWtld2lzZSB3aXRoIEhfUzsgYWZmaW5pdHkgYXQgMC42IHZzIDLDlzAuMzsgSCA9
IDAgdGVuc29yIHwg4omkIDEw4oG7wrnCsiB8IGNsb3NlZCBmb3JtIDIuNcOXMTDigbvCueKBtDsg
YWZmaW5lIDQuMcOXMTDigbvCueKBtDsgSCA9IDA6IDIuM8OXMTDigbvCueKBtCB8ICoqdGhlIHRl
eHR1cmVkIGN1YmljIGFnZ3JlZ2F0ZSBpcyBleGFjdGx5IHRoZSBpc290cm9waWMgYWdncmVnYXRl
IHBsdXMgdOKChMK3KEgvMynCt/Cdkq/igbQg4oCUIGEgZml2ZS1jb25zdGFudCB0cmFuc3ZlcnNl
bHkgaXNvdHJvcGljIG1lZGl1bSB3aG9zZSBlbnRpcmUgbCA9IDQgcmVzcG9uc2UgaXMgdGhlIFpl
bmVyIGNvbWJpbmF0aW9uKiogfAp8ICoqRi1DVFJMLU1BUkcqKiDigJQgU08oMyktZGlyZWN0IE9E
RiBhdmVyYWdlIG9mIHRoZSBwZXItZ3JhaW4gReKCgiB3ZWlnaHQgdnMgdGhlIFPCsi1tYXJnaW5h
bCBmb3JtIDEgKyBjwrd04oKEwrdQ4oKEIChjX+KfqDAwMeKfqSA9IDEsIGNf4p+oMTEx4p+pID0g
4oiSMi8zKSwgYm90aCBjdWJpYyBjb25maWd1cmF0aW9ucywgYm90aCBkZXNjcmlwdG9yIGF4ZXMs
IGV2ZXJ5IG1vZGUgfCDiiaQgMTDigbvCucKyIHwgOC4zw5cxMOKBu8K54oG2IHwgdGhlIG1hcmdp
bmFsIGNvZWZmaWNpZW50cyBvZiBBLTIuNSBhcmUgZXhhY3QgfAp8ICoqRi1DVFJMLVRFWDQqKiDi
gJQgc3ludGhldGljIGN1YmljIHRlbnNvciAoSCA9IDEyMCkgYXQgdOKChCA9IDEsIOKfqDAwMeKf
qSwgSGlsbCB8IFx8cl9hZ2dcfCA+IDEw4oG74oG2IHwgNC4xMsOXMTDigbvigbQgfCB0aGUgaW5z
dHJ1bWVudCBjYW4gc2VlIGFuIGwgPSA0IGRlc2NyaXB0b3Igc3BsaXQgfAp8ICoqRi1DVFJMLVFV
QUQqKiDigJQga8yCLXNwaGVyZSBkb3VibGluZyAoMTI4IMOXIDI1Nikgb24gcl9hZ2cgYXQgdOKC
hCA9IDAuMjU7IFNPKDMpIGRvdWJsaW5nICgzMiwgMjAsIDMyKSBvbiDin6hD4p+pX1YgYXQgdOKC
hCA9IDAuMyB8IOKJpCAxMOKBu8K54oGwIHwgMi4yw5cxMOKBu8K54oG2OyAyLjPDlzEw4oG7wrni
gbQgfCBib3RoIHF1YWRyYXR1cmVzIGV4YWN0IGF0IHRoZSB3b3JraW5nIGRlZ3JlZXMgfAoKIyMg
Mi4gV2hhdCBQaGFzZSAwIGVzdGFibGlzaGVzIChSMS1tYWNoaW5lLCBjaGF0IGxlZzsgdGhlIEND
IGxlZyByZS1kZXJpdmVzIGFsbCBvZiBpdCBibGluZCkKCjEuICoqQ29udGludWl0eS4qKiBUaGlz
IGdhdGUncyB0ZXh0dXJlIG1hY2hpbmVyeSAqaXMqIEctTVNDUzEncyBvbiB0aGUgbCA9IDIgZmFt
aWx5IOKAlCB0aGUgYmFua2VkIM664oKCIGN1cnZlLCB0aGUgc2luZ2xlLWNyeXN0YWwgc3BsaXRz
LCB0aGUgdCA9IDAgc3BlZWRzIGFuZCB0aGUgSFMgcmVmZXJlbmNlcyByZXByb2R1Y2UgdG8gMTIg
ZGlnaXRzIG9yIGV4YWN0bHkuIFdoYXRldmVyIM664oKE4oKEIFBoYXNlIDIgcmV0dXJucyBpcyBv
biB0aGUgc2FtZSBmb290aW5nIGFzIHRoZSBiYW5rZWQgzrrigoIuCjIuICoqVGhlIHR3byBpZGVu
dGl0aWVzIHRoYXQgZGVmaW5lIHRoZSBnYXRlIGhvbGQgdG8gbWFjaGluZSBwcmVjaXNpb24gb24g
dGhlIGJhbmtlZCB0ZW5zb3JzOioqIGwg4omlIDYgdGV4dHVyZSBpcyBpbnZpc2libGUgdG8gZXZl
cnkgb2JzZXJ2YWJsZSAoZXhoYXVzdGlvbiksIGFuZCBvbiB0aGUgZmNjIGJyYW5jaCB0aGUgbCA9
IDIgdGVybSBpcyBudWxsIGpvaW50bHkgd2l0aCBsID0gNCwgc28gdGhlIGZjYyB0ZXh0dXJlIHJl
c3BvbnNlIGlzIHRoZSBsID0gNCB0ZXJtIGFsb25lIChjdWJpYy1lZmZlY3RpdmUpLiBCb3RoIGFy
ZSBjb250cm9scywgbmV2ZXIgcmVzdWx0czsgYm90aCBhcmUgbm93IHdpdG5lc3NlZCBvbiB0aGUg
c3Vic3RyYXRlJ3Mgb3duIHRlbnNvcnMsIG5vdCBvbmx5IG9uIHRoZSBzeW50aGV0aWMgcHJlLWRy
YWZ0IGNoZWNrLgozLiAqKlRoZSBleGFjdCBjbG9zZWQgZm9ybSBvZiB0aGUgY3ViaWMgbCA9IDQg
cmVzcG9uc2UgaXMgY29uZmlybWVkIG9uIGJvdGggZmNjIGNvbmZpZ3VyYXRpb25zOioqIHRoZSB3
aG9sZSB0ZXh0dXJlIGRlcGVuZGVuY2Ugb2YgdGhlIFZvaWd0L1JldXNzIGFnZ3JlZ2F0ZSBpcyB0
4oKEwrcoSC8zKcK38J2Sr+KBtCjhupEpIHdpdGggSCB0aGUgWmVuZXIgY29tYmluYXRpb24g4oCU
IHNvIHRoZSBmY2MgYnJhbmNoJ3MgdGV4dHVyZSByZXNwb25zZSBpcyBvbmUgbnVtYmVyIHBlciBj
b25maWd1cmF0aW9uIHRpbWVzIGEgZml4ZWQgcmF0aW9uYWwgdGVuc29yLiAoUGhhc2UgMidzIM66
4oKE4oKEIGlzIHRoZW4gdGhlIGRlc2NyaXB0b3IgcGFpcidzIHNlY29uZC1vcmRlciByZWFkaW5n
IG9mIHRoaXMgb25lLXBhcmFtZXRlciBkZWZvcm1hdGlvbjsgdGhlIE8odOKChCkgcVNIL3FTViBi
aXJlZnJpbmdlbmNlIGFsb25nIGvMgiDiiqUg4bqRIGlzIGV4YWN0bHkgSHTigoQvMjEgb24gdGhl
IFZvaWd0IHRlbnNvciwgQS0yLjYuKQo0LiAqKlRoZSBtYXJnaW5hbCByZWR1Y3Rpb24gb2YgdGhl
IGRlc2NyaXB0b3IgYXZlcmFnZSBpcyBleGFjdCoqIOKAlCBjX+KfqDAwMeKfqSA9IDEsIGNf4p+o
MTEx4p+pID0g4oiSMi8zIOKAlCB3aGljaCBpcyB3aGF0IG1ha2VzIHRoZSDin6gxMTHin6kgZGVz
Y3JpcHRvcidzIGwgPSA0IHJlc3BvbnNlIHRoZSBuZWdhdGl2ZSB0d28tdGhpcmRzIG9mIHRoZSDi
n6gwMDHin6kgZGVzY3JpcHRvcidzIGF0IHRoZSB3ZWlnaHQgbGV2ZWw7IHdoZXRoZXIgdGhlIHNp
Z24gZmxpcCBvZiByX3h0YWwgY2FycmllcyBpbnRvIM664oKE4oKEIChIWVAtTVMyLTIpIGlzIGEg
UGhhc2UtMiBxdWVzdGlvbi4KCiMjIDMuIEhvbmVzdHkgaXRlbXMgKGNoYXQgc2lkZSwgdGhpcyBy
dW4pCgotICoqSC1NUzItMSAocHJlLWxvY2ssIGRpc2Nsb3NlZCk6KiogdGhlIGNsb3NlZCBmb3Jt
cyBvZiBBLTIuMi9BLTIuNiBhbmQgdGhlIG1hcmdpbmFsIGNvZWZmaWNpZW50cyB3ZXJlIGRlcml2
ZWQgY2hhdC1zaWRlIChzeW1weSkgYmVmb3JlIHRoZSBsb2NrIGFuZCB2ZXJpZmllZCBudW1lcmlj
YWxseSBvbiBhIGdlbmVyaWMgc3ludGhldGljIHRlbnNvciBiZWZvcmUgdGhlIG1lbW8gdjIgd2Fz
IHdyaXR0ZW47IHRoZXkgZW50ZXJlZCB0aGUgbG9jayByZWNvcmQgYXMgb3BlcmF0aW9uYWxpemF0
aW9ucyB0byBiZSBhc3NlcnRlZCwgbm90IGFzIHJlc3VsdHM7IHRoZSBQaGFzZS0wIHJ1biBhc3Nl
cnRzIHRoZW0gb24gdGhlIGJhbmtlZCB0ZW5zb3JzLgotICoqSC1NUzItMiAoYnVpbGQpOioqIHRo
ZSBpbnN0cnVtZW50J3Mgc2VsZnRlc3QgUzIgaW5pdGlhbGx5IGZhaWxlZCBvbiB0aGUgdGVzdCdz
IG93biByb3RhdGlvbiBtYXRyaXggKHRoZSBib2R5LWRpYWdvbmFsIHRlc3QgdXNlZCB0aGUgdHJh
bnNwb3NlIG9mIHRoZSBpbnRlbmRlZCByb3RhdGlvbik7IHRoZSB0ZXN0IHdhcyBjb3JyZWN0ZWQg
KG5vIGluc3RydW1lbnQgY29kZSBwYXRoIGNoYW5nZWQpIGJlZm9yZSBhbnkgcnVuOyB0aGUgaW5z
dHJ1bWVudCBtZDUgYWJvdmUgaXMgdGhlIGZpbmFsIG9uZS4KLSAqKkgtTVMyLTMgKGhvdXNla2Vl
cGluZywgcmVjb3JkZWQgbm90IHJlc29sdmVkKToqKiB0aGUgYXV0aG9yJ3MgbG9jayBkaXJlY3Rp
dmUgc3RhdGVzIHRoZSBISy0xIFBScyBtZXJnZWQgd2l0aCBwbGFjZWhvbGRlciBudW1iZXJzOyB0
aGUgbGl2ZSByZW1vdGUgYXQgbG9jayAoMTQ6MTAgVVRDKSBzaG93cyBgbWFpbmAgPSBgZDBhMGUz
MWAsIG5vIGBnbXNjczFfZ2F0ZS9lc3RhdGUvYCBvbiBhbnkgYnJhbmNoLCB0aGUgVjQuNzkgY2Fu
b25pY2FsIGF0IHRoZSByb290IChtZW1vIMKnMTAsIEEtMi40KS4KLSAqKkQtTVMyLTEgKG5vbmUp
OioqIG5vIGRldmlhdGlvbiBmcm9tIHRoZSBsb2NrZWQgb3JkZXIgb2Ygb3BlcmF0aW9uczsgUGhh
c2VzIDLigJMzIG5vdCBydW4gYnkgZGlyZWN0aXZlLgotICoqU2NhbiBoeWdpZW5lIChyZWNvcmRl
ZCBmb3IgdGhlIG5leHQgbG9jayk6KiogdHdvIGZvcmJpZGRlbiBudW1lcmljIHJlbmRlcmluZ3Mg
d2VyZSBjYXVnaHQgYnkgdGhlIFQxIHNjYW5uZXIgaW4gZHJhZnRpbmcg4oCUIGEgbWFjaGluZS1w
cmVjaXNpb24gcmVzaWR1YWwgaW4gdGhlIGRyYWZ0IG1lbW8gYW5kIGEgc3ludGhldGljIHNlbGZ0
ZXN0IHZhbHVlIGluIHRoZSBjb21wYXJhdG9yIOKAlCBib3RoIHJld29yZGVkIGJlZm9yZSBmcmVl
emluZzsgdGhleSB3ZXJlIGNvaW5jaWRlbmNlcyB3aXRoIGRpZ2l0IHN0cmluZ3Mgb24gdGhlIHN0
cmF0dW0sIG5vdCByZWZlcmVuY2VzLgoKIyMgNC4gTmV4dCBzdGVwcyAocGVyIHRoZSBsb2NrZWQg
b3JkZXIgb2Ygb3BlcmF0aW9uczsgb24gdGhlIGF1dGhvcidzIHdvcmQpCgpQaGFzZSAyICh0aGUg
S8yD4oKEIC8gUOKChCBzd2VlcHMsIHRoZSBmaXRzLCB0aGUgYmlyZWZyaW5nZW5jZSBjb2VmZmlj
aWVudCwgdGhlIGhleCBxdWFkcmF0aWMgZm9ybSkg4oaSIFBoYXNlIDMgKHZlcmRpY3QsIGxhc3Qp
IOKGkiBleGVjdXRpb24gcmVwb3J0IOKGkiBQLTQvUC00LmMgZGlzcGF0Y2ggd2l0aCB0aGUgVDEg
bGlzdHMgaW4tYmFuZCDihpIgQ0MgbGVnIGJsaW5kIGZyb20gc2NyYXRjaCAobWV0aG9kIHZhcmlh
dGlvbjogYSBkaWZmZXJlbnQgU08oMykgcXVhZHJhdHVyZSBvciB0aGUgYW5hbHl0aWMgZ2VuZXJh
bGl6ZWQtc3BoZXJpY2FsLWhhcm1vbmljIHJvdXRlKSDihpIgdHdvLWxlZyBjb21wYXJpc29uICh2
MS4wKSDihpIgUzkgb24gbWlzc2VzIOKGkiBmb2xkIGF1dGhvcml6YXRpb24g4oaSIFY0Ljg1Lgo=
=====END-EMBED name=G_MSCS2_PHASE0_EXECUTION_REPORT.md=====

=====BEGIN-EMBED name=diag_kappa24.py md5=9c53fa2f1715c499dec0bef143c503b0 bytes=2323 encoding=base64 armor_bytes=3141 QUARANTINED=====
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJkaWFnX2thcHBhMjQucHkgLS0gcG9zdC1ydW4gRElB
R05PU1RJQyAobm90IGEgY2hlY2twb2ludDsgbm90IHZlcmRpY3QtYmVhcmluZyk6ICgxKSBSaWNo
YXJkc29uIGVzdGltYXRlcyBvZiB0aGUKY3Jvc3MgY29lZmZpY2llbnQga2FwcGEyNCBmcm9tIG1p
eGVkIHNlY29uZCBkaWZmZXJlbmNlcyBhdCBoIGFuZCBoLzIgKGVycm9yIE8oaF40KSksIGhleCBQ
MitQNCBmYW1pbHkgYW5kIHRoZSBjdWJpYwppbmhlcml0ZWQgKG5vbi1zeW1tZXRyaXplZCwgZGVz
Y3JpcHRvci1heGlzKSBQMiB0ZXJtICsgSzQtdGlsZGU7ICgyKSB0aGUgbWl4ZWQtdGVybSByX2Fn
ZyBjaGFuZ2UgdGhhdCBBLTIuOSdzCkYtQ1RSTC1MMk5VTEwgcl9hZ2cgY2xhdXNlIHdvdWxkIGhh
dmUgbWVhc3VyZWQgb24gY3ViaWM7ICgzKSB0aGUgcHVyZSBsID0gMiByX2FnZyBjaGFuZ2Ugb24g
Y3ViaWMgKGV4YWN0IG51bGwpLiIiIgppbXBvcnQganNvbiwgbWF0aCwgc3lzLCBpbXBvcnRsaWIu
dXRpbAppbXBvcnQgbnVtcHkgYXMgbnAKc3BlYyA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9m
aWxlX2xvY2F0aW9uKCdpbnN0JywgJy9ob21lL2NsYXVkZS9nbXNjczIvZ19tc2NzMl9jaGF0bGVn
LnB5Jyk7IEkgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKHNwZWMpOyBzcGVjLmxv
YWRlci5leGVjX21vZHVsZShJKQp2cmggPSBqc29uLmxvYWQob3BlbihJLlgxKSlbJ3ZyaCddOyBL
LCBXID0gSS5zcGhlcmVfZ3JpZChJLk5fVEhFVEEsIEkuTl9QSEkpCmRlZiBtaXhlZF9vZGYoc3lt
LCBheGlzLCBjbSwgdDIsIHQ0KToKICAgIGlmIHN5bSA9PSAnaGV4JzogcmV0dXJuIEkuT0RGKCdQ
NCcsIHQyPXQyLCB0ND10NCkKICAgIGJhc2UgPSBJLk9ERignSzQnLCBheGlzX2M9YXhpcywgY21h
cmc9Y20sIHQ0PXQ0KQogICAgY2xhc3MgX00oSS5PREYpOgogICAgICAgIGRlZiB3X3NvMyhzZWxm
LCBScyk6IHJldHVybiBiYXNlLndfc28zKFJzKSArIHQyICogSS5QMigoUnMgQCBheGlzKVs6LCAy
XSkKICAgICAgICBkZWYgd19tYXJnKHNlbGYsIG4pOiByZXR1cm4gYmFzZS53X21hcmcobikgKyB0
MiAqIEkuUDIobls6LCAyXSkKICAgIHJldHVybiBfTSgnSzQnLCBheGlzX2M9YXhpcywgY21hcmc9
Y20sIHQ0PXQ0KQpkZWYgcihzeW0sIGM0LCBvZGYpOgogICAgYWcgPSBJLmFnZ3JlZ2F0ZV90ZW5z
b3JzKGM0LCBvZGYsIE5vbmUpOyByZXR1cm4gSS5zcGVjaWVzX3N0YXRzKHN5bSwgYWdbJ0gnXSwg
SywgVywgb2RmLCB3YW50X2xhYmVscz1GYWxzZSlbJ3JfeHRhbF9FMiddCm91dCA9IHt9CmZvciBj
ZmcsIChzeW0sIHZrKSBpbiBJLkNPTkZJR1MuaXRlbXMoKToKICAgIGZvciBrZXksIHN5bW0sIGF4
aXMsIGNtIGluIEkuY29uZmlnX2tleXMoY2ZnKToKICAgICAgICBjNCA9IEkuYzRfZnJvbV9jb25z
dGFudHMoc3ltLCB2cmhbdmtdWydDX292ZXJfcmhvJ10sIHN5bW0pCiAgICAgICAgZGVmIEQoaCk6
CiAgICAgICAgICAgIGYgPSBsYW1iZGEgYSwgYjogcihzeW0sIGM0LCBtaXhlZF9vZGYoc3ltLCBh
eGlzLCBjbSwgYSwgYikpCiAgICAgICAgICAgIHJldHVybiAoZihoLCBoKSAtIGYoaCwgLWgpIC0g
ZigtaCwgaCkgKyBmKC1oLCAtaCkpIC8gKDQgKiBoICogaCkKICAgICAgICBkMSwgZDIgPSBEKDAu
MDIpLCBEKDAuMDEpOyBrMjQgPSAoNCAqIGQyIC0gZDEpIC8gMy4wCiAgICAgICAgcmVjID0geydr
YXBwYTI0X3JpY2hhcmRzb24nOiBrMjQsICdEX2gwcDAyJzogZDEsICdEX2gwcDAxJzogZDJ9CiAg
ICAgICAgaWYgc3ltID09ICdjdWJpYyc6CiAgICAgICAgICAgIHIwMCA9IHIoc3ltLCBjNCwgSS5P
REYoJ2lzbycpKTsgcjIwID0gcihzeW0sIGM0LCBJLk9ERignbDInLCBheGlzX2M9YXhpcywgdD0x
LjApKQogICAgICAgICAgICByQSA9IHIoc3ltLCBjNCwgbWl4ZWRfb2RmKHN5bSwgYXhpcywgY20s
IDAuMCwgMC4yNSkpOyByQiA9IHIoc3ltLCBjNCwgbWl4ZWRfb2RmKHN5bSwgYXhpcywgY20sIDAu
MjUsIDAuMjUpKQogICAgICAgICAgICByZWMudXBkYXRlKHsncHVyZV9sMl9yX2FnZ19jaGFuZ2Vf
dDEnOiBhYnMocjIwIC0gcjAwKSwgJ21peGVkX3JfYWdnX2NoYW5nZV9BMjknOiBhYnMockIgLSBy
QSksICdyX2FnZ18wXzBwMjUnOiByQSwgJ3JfYWdnXzBwMjVfMHAyNSc6IHJCfSkKICAgICAgICBv
dXRba2V5XSA9IHJlYzsgcHJpbnQoa2V5LCB7azogZid7djorLjNlfScgZm9yIGssIHYgaW4gcmVj
Lml0ZW1zKCl9LCBmbHVzaD1UcnVlKQpqc29uLmR1bXAob3V0LCBvcGVuKCcvaG9tZS9jbGF1ZGUv
Z21zY3MyL2RpYWdfa2FwcGEyNC5qc29uJywgJ3cnKSwgaW5kZW50PTEpCg==
=====END-EMBED name=diag_kappa24.py=====

=====BEGIN-EMBED name=diag_kappa24.json md5=b7952dfcaddcd1d98e424aee8ce5231f bytes=1917 encoding=base64 armor_bytes=2590 QUARANTINED=====
ewogImhleF9zdGVwfGEiOiB7CiAgImthcHBhMjRfcmljaGFyZHNvbiI6IDkuNDgzMTU1MDAyMDA2
NTQ1ZS0xMywKICAiRF9oMHAwMiI6IC05LjM4ODMyMzQ1MTk4NjQ4ZS0xMSwKICAiRF9oMHAwMSI6
IC0yLjI3NTk1NzIwMDQ4MTU3MWUtMTEKIH0sCiAiaGV4X3N0ZXB8YiI6IHsKICAia2FwcGEyNF9y
aWNoYXJkc29uIjogMi41NDQyNjEwOTgwOTkzMTdlLTEzLAogICJEX2gwcDAyIjogLTkuNDAyMjAx
MjM5Nzk0Mjk0ZS0xMSwKICAiRF9oMHAwMSI6IC0yLjMzMTQ2ODM1MTcxMjgyODdlLTExCiB9LAog
ImhleF9nZW04fGEiOiB7CiAgImthcHBhMjRfcmljaGFyZHNvbiI6IC01LjMxOTgxODY1OTY2MjIw
OWUtMTMsCiAgIkRfaDBwMDIiOiAtMS4zODI5MjE1NTUwNDg3MTA2ZS0xMCwKICAiRF9oMHAwMSI6
IC0zLjQ5NzIwMjUyNzU2OTI0M2UtMTEKIH0sCiAiaGV4X2dlbTh8YiI6IHsKICAia2FwcGEyNF9y
aWNoYXJkc29uIjogNi45Mzg4OTM5MDM5MDcyMjhlLTEzLAogICJEX2gwcDAyIjogLTEuMzg2Mzkx
MDAyMDAwNjY0MmUtMTAsCiAgIkRfaDBwMDEiOiAtMy40MTM5MzU4MDA3MjIzNTY0ZS0xMQogfSwK
ICJjdWJpY19zdGVwfDAwMSI6IHsKICAia2FwcGEyNF9yaWNoYXJkc29uIjogLTYuNzA3NTk3NDQw
NDQzNjU0ZS0xMywKICAiRF9oMHAwMiI6IDEuNDg1MjcwMjQwMTMxMzQyMmUtMDksCiAgIkRfaDBw
MDEiOiAzLjcwODE0NDkwMjI0ODAyM2UtMTAsCiAgInB1cmVfbDJfcl9hZ2dfY2hhbmdlX3QxIjog
MS4xMTAyMjMwMjQ2MjUxNTY1ZS0xNiwKICAibWl4ZWRfcl9hZ2dfY2hhbmdlX0EyOSI6IDkuMDc2
MTc3NzExNjE5OTQ4ZS0wNywKICAicl9hZ2dfMF8wcDI1IjogLTIuMzM1NTk4NjYxOTYyMjAxNmUt
MDUsCiAgInJfYWdnXzBwMjVfMHAyNSI6IC0yLjQyNjM2MDQzOTA3ODQwMWUtMDUKIH0sCiAiY3Vi
aWNfc3RlcHwxMTEiOiB7CiAgImthcHBhMjRfcmljaGFyZHNvbiI6IDcuNDAxNDg2ODMwODM0Mzc3
ZS0xMywKICAiRF9oMHAwMiI6IDEuNDg1NDc4NDA2OTQ4NDU5NWUtMDksCiAgIkRfaDBwMDEiOiAz
LjcxOTI0NzEzMjQ5NDI3NDRlLTEwLAogICJwdXJlX2wyX3JfYWdnX2NoYW5nZV90MSI6IDMuMzMw
NjY5MDczODc1NDY5NmUtMTYsCiAgIm1peGVkX3JfYWdnX2NoYW5nZV9BMjkiOiA5LjA3NjE3Nzcx
MTYxOTk0OGUtMDcsCiAgInJfYWdnXzBfMHAyNSI6IDEuNTU3MDY1Nzc0NjI2NjY0N2UtMDUsCiAg
InJfYWdnXzBwMjVfMHAyNSI6IDEuNDY2MzAzOTk3NTEwNDY1M2UtMDUKIH0sCiAiY3ViaWNfZ2Vt
OHwwMDEiOiB7CiAgImthcHBhMjRfcmljaGFyZHNvbiI6IC01Ljc4MjQxMTU4NjU4OTM1N2UtMTMs
CiAgIkRfaDBwMDIiOiAyLjYxNjMwOTk0NjQ2ODIyMDVlLTA5LAogICJEX2gwcDAxIjogNi41MzY0
MzgwNTc0ODA2MDllLTEwLAogICJwdXJlX2wyX3JfYWdnX2NoYW5nZV90MSI6IDIuMjIwNDQ2MDQ5
MjUwMzEzZS0xNiwKICAibWl4ZWRfcl9hZ2dfY2hhbmdlX0EyOSI6IDEuMzA0MTU3Nzg4MjA2Njk0
NmUtMDYsCiAgInJfYWdnXzBfMHAyNSI6IC0yLjgwMjA2MzYyNzA2MDkyNDVlLTA1LAogICJyX2Fn
Z18wcDI1XzBwMjUiOiAtMi45MzI0Nzk0MDU4ODE1OTRlLTA1CiB9LAogImN1YmljX2dlbTh8MTEx
IjogewogICJrYXBwYTI0X3JpY2hhcmRzb24iOiAtMS44NTAzNzE3MDc3MDg1OTQzZS0xMywKICAi
RF9oMHAwMiI6IDIuNjE2MjQwNTU3NTI5MTgxNGUtMDksCiAgIkRfaDBwMDEiOiA2LjUzOTIxMzYx
NTA0MjE3MmUtMTAsCiAgInB1cmVfbDJfcl9hZ2dfY2hhbmdlX3QxIjogMi4yMjA0NDYwNDkyNTAz
MTNlLTE2LAogICJtaXhlZF9yX2FnZ19jaGFuZ2VfQTI5IjogMS4zMDQxNTc3ODg0Mjg3MzkyZS0w
NiwKICAicl9hZ2dfMF8wcDI1IjogMS44NjgwNDI0MTgwODUwMjUyZS0wNSwKICAicl9hZ2dfMHAy
NV8wcDI1IjogMS43Mzc2MjY2MzkyNDIxNTEzZS0wNQogfQp9
=====END-EMBED name=diag_kappa24.json=====

=====BEGIN-EMBED name=diag_quadform_basis.json md5=d84aa1fdce7dea1b1a5d24dfb8f13c18 bytes=1119 encoding=base64 armor_bytes=1512 QUARANTINED=====
ewogImN1YmljX3N0ZXB8MDAxIjogewogICJrNyI6IFsKICAgNC40ODE5MTEwNzYzNjEwOWUtMDks
CiAgIDEuOTc0MDQzMzc0OTg2MDc2ZS0wNywKICAgLTAuMDAwMzc0MzU0NTU5MzkxMDYxNjYsCiAg
IDMuNjQxMDYwMjcwNTE0Mjg2M2UtMDksCiAgIC0xLjcwNDg4OTA3NTk4MDk2NDVlLTEwLAogICAt
NS45MDE4NzgxNjg2MDcxOWUtMDUsCiAgIDIuNjMyOTEzMzM0NjgzNzY3ZS0wNgogIF0sCiAgImsx
MiI6IFsKICAgLTkuMDUzOTc0ODIwMTUwMjgyZS0xNSwKICAgLTMuNTI5NTQ0MDYxNTM0MDUxZS0x
MSwKICAgLTAuMDAwMzc0MzA2OTM5MDkxMjU2OCwKICAgMy42NDEwNjAyNzA1MzcwNDZlLTA5LAog
ICAtMS43MDQ4ODkwNzYzMzYwMDJlLTEwLAogICAtNS45MDE4NzgxNjg2MDcxOTJlLTA1LAogICAy
LjYzMjkxMzMzNDY4MzgxMjhlLTA2LAogICAxLjU0MDMzNzIxNTIwODQxNGUtMTMsCiAgIDEuODk0
ODMwOTk2NTU3NzExZS0xNCwKICAgLTQuNDEyNDc5MDg2NTg5OTY3ZS0xNSwKICAgMy43MTY1MTA3
MTg3MzIwNzFlLTA2LAogICAtNy41Mjk2MDk1OTg2OTExMTRlLTA3CiAgXQogfSwKICJoZXhfc3Rl
cHxhIjogewogICJrNyI6IFsKICAgLTAuMDAxNDM5NDY5MzAyMDAzMjkwMywKICAgLTEuMjQ4ODc5
MDczMDQ5MTg4N2UtMDgsCiAgIDAuMDAwMTYwMzk5MDM3NjM5NDUzMTcsCiAgIC03LjM2OTUxNTY4
OTM2MzE3NWUtMDcsCiAgIC03LjI3NjM4Njk2NzAxMTg1NGUtMDYsCiAgIC0zLjkzNjkyODkzNTc3
NDAwNGUtMDYsCiAgIDIuMjE0Mzc5NjkzOTE4MzA5ZS0wNwogIF0sCiAgImsxMiI6IFsKICAgLTAu
MDAxNDM5NDU0NDQwMDQ3Nzc2LAogICAxLjY2NjgwMjk4MDM2MDE0OTJlLTEyLAogICAwLjAwMDE2
MDQwMzQ0Mzg3OTQ3NzIsCiAgIC03LjM2OTUxNTY4OTM2MzIzZS0wNywKICAgLTcuMjc2Mzg2OTY3
MDExODU4ZS0wNiwKICAgLTMuOTM2OTI4OTM1Nzc0MDAyZS0wNiwKICAgMi4yMTQzNzk2OTM5MTgy
OTRlLTA3LAogICAtMS4xOTk2NDQ2Mjc3NTcxNzFlLTA3LAogICAtMS4yNjgxNTkzMTg2MDAyNDFl
LTA3LAogICAtMy42MDMxNzIyOTM1NjM2NzU2ZS0wNywKICAgLTEuMDgyOTg1NjI4ODg2Mzc5N2Ut
MDcsCiAgIDMuMTEzNzQ5MDA5OTQzNzFlLTA4CiAgXQogfQp9
=====END-EMBED name=diag_quadform_basis.json=====
