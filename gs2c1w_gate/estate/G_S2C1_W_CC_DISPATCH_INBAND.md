# G_S2C1_W_CC_DISPATCH_INBAND.md — Gate G-S2C1-W, single-file in-band CC dispatch (P-4 / P-4.b / P-4.c)

**Date:** September 8, 2026. **Gate:** G-S2C1-W (the W_∪′ re-derivation mini-gate; §2.91.O PF-S2 successor). **Base:** V4.80 `a28e9b40616ee9b5798e9a5be027c1d9`. **Memo LOCKED** `1ebb6a82fcb24e207b164a654eb94dd1`; **lock record** `5f963ed8d7eff9f803da5c1eea2f841a`; **Addendum 1** `125809174278cc7738692fd783d4ecd7`.

## §0 ACTIVATION FLAGS (embedded; no side-channel message is load-bearing — P-4)
```
GATE=G-S2C1-W
LEG=cc
READ_AUTHORIZED=1        # author authorization of September 8, 2026: "Unseal the anchors, execute ... report the verdict"
ORDER=verify-then-build  # every embed hash-verified BEFORE any construction; machinery asserted in-repo by SHA + manifest
BLINDNESS=CC-BLIND-FIRST # E-W-5(a); armored embed #8 (chat instrument) is NOT decoded until the CC checkpoint is hashed
ELECTIONS=E-W-1(a) E-W-2(a) E-W-3(a) E-W-4(i) E-W-5(a) E-W-6(a) E-W-7(a); DEFAULTS D-W-1/4/5/6/7 ratified
RETURN=checkpoint g_s2c1w_phase3_cc.json (schema v1.0) + CC report + return manifest (md5,bytes) + commit sha + branch
```

## §1 Embed table (every artifact travels INSIDE this file; verify-then-build)
| # | embed | md5 | bytes | armor |
|---|---|---|---|---|
| 1 | `staging_memo_G_S2C1_W.md` | `1ebb6a82fcb24e207b164a654eb94dd1` | 32,219 | plain |
| 2 | `G_S2C1_W_LOCK_RECORD.md` | `5f963ed8d7eff9f803da5c1eea2f841a` | 10,875 | plain |
| 3 | `G_S2C1_W_LOCK_RECORD_ADDENDUM_1.md` | `125809174278cc7738692fd783d4ecd7` | 7,207 | plain |
| 4 | `t1_forbidden_G_S2C1_W.txt` | `20ba1e7eab5a3bbffe510b4840edbc57` | 1,560 | plain |
| 5 | `t1_forbidden_G_S2C1_W_A1.txt` | `735eae308aa7baec19f23da5602a2d82` | 39 | P-4.b quarantined |
| 6 | `pinned_inputs_G_S2C1_W.json` | `d1edc69b16dfd0b728a48cd8389b322b` | 5,769 | byte-exact (no trailing newline) |
| 7 | `anchors_G_S2C1_W_SEALED.md` | `8c7d59f64057e372d7b1ff760667a7c2` | 154 | P-4.b quarantined |
| 8 | `g_s2c1w_mapper_v6.py` | `e034d4281c4a2906377e1587672cc128` | 26,458 | P-4.b chat instrument (v6.1, read of record) |
| 9 | `g_s2c1w_compare_v1_0.py` | `007688e5d8ea45d6848fd8e99c57a7d8` | 4,665 | plain |
| 10 | `g_s2c1w_schema_v1_0.json` | `dd014b8cc4c48e5dbf356e96baded753` | 1,382 | plain |
| 11 | `MANIFEST_gpoly1_phase3.md5` | `3b178fb26068050c9f8c4866edce4078` | 792 | plain |
| 12 | `t1_scan.py` | `ccd47ac5779c6592bb3c49d6890049e9` | 2,138 | plain |
| 13 | `extract_embeds_G_S2C1_W.py` | `a5a006c69f720bac8ca2e461c623c4f2` | 2,775 | plain (extractor) |

Extraction: `python3 extract_embeds_G_S2C1_W.py` (embed #13 — extract it first by hand from its markers, or with any conforming extractor; the payload convention is in its docstring). Halt on any md5/size mismatch. The extractor is the ONLY reader of embedded artifacts (P-4.c).

## §2 Standing rules honored by this dispatch
- **P-4:** one self-contained file; activation flags embedded (§0); no side-channel instruction is load-bearing.
- **P-4.b:** quarantined embeds travel base64-armored — #5 (T1-A1: anchor-specific identifiers and digit strings), #7 (the sealed anchor file), #8 (the chat instrument) — so no viewer/pager renders them in the clear (the G-2a-L1 D-CC-1 lesson). #6 is armored for byte-exactness only (no trailing newline), as the G-S2C1 aggregate dispatch did with its pinned inputs.
- **P-4.c:** this dispatch is delivered ALONE. No loose file accompanies it. Any loose file present at delivery is a logged deviation at the receiving leg (H-CC-P2-1 lineage). Everything the CC leg needs is in §1; the G-POLY1 Phase-3 machinery is NOT re-shipped — it is referenced by commit and asserted in-repo (§3 step 2).
- **Blindness clause:** decode #8 only AFTER the CC checkpoint is hashed and committed; decode #7 only inside the mapper at read time (md5 + census asserted at open); decode #5 at T1 setup. Cross-leg disclosure of defect CLASSES is admissible (H-7/H-18 precedent); cross-leg CODE is not.
- **Order-of-record disclosure (D-W-9):** the CC leg's first execution preceded this dispatch (author-directed; CC checkpoint declared `97f26c04f982b1cc1694f4a47bdce882` in Addendum 1 §4). This dispatch is the canonical package of record: if the declared CC checkpoint conforms to schema v1.0 (#10) the frozen comparator (#9) applies to it as-is; any representational miss is an S9 item resolved by re-emission UNDER THIS DISPATCH (the path-(a) mini-dispatch pattern), never by editing the frozen comparator after the fact.

## §3 CC tasks (in order; each halts the chain on failure)
1. Verify all 13 embeds byte-exact against §1 (extract, md5, size). Record the dispatch file's own md5 and size in the CC report.
2. Assert the G-POLY1 Phase-3 machinery in-repo: branch `claude/new-session-e1u91p`, commit `dd813646ed112f630816ee260ae0bdd096e2b417`, dir `gpoly1_gate/phase3/`, `MANIFEST.md5` (#11) 13/13 OK. Reuse of `att_edge`/`bir_edge` is NOT required (the G-POLY1 kinds are pinned, not re-read); the machinery is the lineage reference for the envelope, dressing, masking, and single-read patterns.
3. T1: base (#4, `20ba1e7eab5a3bbffe510b4840edbc57`) ∪ A1 (#5, `735eae308aa7baec19f23da5602a2d82`), pattern-lines-only, D-W-7 rule (numeric patterns hit only when glued to a letter/underscore token; digit/sign/dot glue and exponent suffixes LOGGED, not fatal). Independent scanner implementation (rule disclosed at #12; no code transfer required). Self-grep every instrument at every invocation; scan every artifact.
4. F-W-PIN: load #6 (`d1edc69b16dfd0b728a48cd8389b322b`, AUTHOR-VERIFIED); assert every memo §2 value to 1e-12 rel; pin the four G-POLY1 edges from `2064bd7b` (in-repo).
5. Build the CC mapper FROM SCRATCH (own lexer with NAMED-KEY binding for `B =` and `k = … /m`; own Born edge; own fixed-point dressing; own union; own comparison-last gate). Implement memo §3.2–3.7, §4 (E-W-1(a) a_phys interval; E-W-2(a) Γ–K window / Γ–M robustness; E-W-3(a) CC's OWN a₂ column), §7 falsifiers. Pre-read suites with synthetic values disjoint from the sealed file: Born edge vs hand value; envelope VOID; FAIL-L election-robust (base AND ×10) vs fragile; Δ₄ both sides + dressed fixed point (residual ≤ 1e-12) + no-root-beyond-turnover; phase/group c_q = √3 edge ratio; malformed-row masked aborts (field count, separator inside a field, unnamed key, negativity, missing unit, bad q, non-disp kind); census mismatch; comparison-last guard; F-W-MONO trap; masking self-scan.
6. Read: decode #7 inside the mapper only; assert md5 `8c7d59f64057e372d7b1ff760667a7c2`, 154 B, census 1 row / {disp: 1} / 8 fields; single read; masked X-1 abort on any defect; serialize per-arm records, union, intersection, pre-comparison md5; THEN the comparison (INERT / TIGHTENED / FAIL-L; OOM ×10 / ×0.1; reinstatement NONE by E-W-7(a)).
7. Checkpoint per schema v1.0 (#10); T1-scan it (masked texts; numeric collisions logged); hash; commit; return per §0 RETURN. Do not consult the chat instrument (#8) or any chat value before the CC checkpoint is hashed and committed.
8. CC report: design register (CC-DD-n), honesty items (H-CC-n), deviations, return manifest.

## §4 What is NOT authorized by this dispatch
No fold; no register change; no reinstatement of W_∪; no reading of the four G-POLY1 sealed anchors (pinned only); no re-fit of any pinned coefficient; no per-arm tuning.

## §5 Embeds
<<<BEGIN staging_memo_G_S2C1_W.md>>>
# STAGING MEMO — Gate G-S2C1-W (the W_∪′ re-derivation mini-gate)

**Date:** September 8, 2026. **Base:** `SQT_Master_Ledger_v4_80_CANONICAL.md` md5 `a28e9b40616ee9b5798e9a5be027c1d9` (1,514,144 B). **Successor named at:** V4.80 PF-S2 (§2.91.O; the Part VI G-POLY1 window-row annotation). **Status: DRAFT — NOT LOCKED. No sealed file exists. No T1 list is frozen. No computation, no read, no window. Nothing reinstated.** Author authorization required for: lock (this memo), T1 freeze, sealed-anchor assembly, and any execution — each separately.

---

## 0. Object, scope, and what is NOT claimed

**Object.** Re-derive the spin-2-radiative-side admissible window on the domain scale d (the M.CW import of G-POLY1, §2.91.M) with the S2 channel's *measured* O(k²) dispersion included as constraint curves at both scales — the lattice scale (a₂ at a\*, §2.91.O P1) and the grain scale (a₂^agg at a_g = d, §2.91.O P2). The result is W_∪′.

**Standing state carried in.** W_∪ = (0, 2.1213132100130068 m] REMAINS SUSPENDED (PF-1 at V4.77; PF-S2 at V4.80). The S2-on-cone rescue condition FAILED (A3 / A3-agg). This memo does not reinstate W_∪, does not re-read the G-POLY1 sealed anchors, and does not decide whether W_∪′ replaces W_∪ in any downstream use — that is a separate fold-level election (§10, E-W-7).

**Not claimed by this gate under any outcome:** no observable; no bridge (M.BRIDGE intact); no channel-speed-equality statement (the multi-species problem is its own successor); no μ_n; no d derived (constraint curve only, the KC3/G-SCALE1 pattern); no statement about the EM-side window W^EM_∪ (§2.91.N, untouched); the §2.52 Open 3 row untouched.

**Register ceiling.** Every number R1-machine two-leg; the window reading R2, conditional on the enumerated imports (§4, §9); the polycrystal postulate remains R3 whatever W_∪′ turns out to be. A non-empty W_∪′ is a non-kill with a quantitative ceiling, not a confirmation.

---

## 1. Recovery record — G-POLY1 Phase-3 window machinery (H-W-0)

Recovered September 8, 2026, chat side, from `github.com/gifgaf0/gifgaf0.github.io`, branch `claude/new-session-e1u91p`, directory `gpoly1_gate/phase3/`, **pinned to commit `dd813646ed112f630816ee260ae0bdd096e2b417`** (= the ledger's `dd81364`; the branch head at recovery; commit message "G-POLY1 Phase 3: re-lock 4 record set committed; CC review of chat v5 (pre-read-#4)", 2026-08-12). Fetched by raw content at that SHA, not by branch name.

**Census:** 14 files (13 payload + `MANIFEST.md5`). **`MANIFEST.md5` check: 13/13 OK.** Every ledger-cited Phase-3 hash matched byte-exact:

| file | bytes | md5 (matches ledger / manifest) |
|---|---|---|
| `g_poly1_phase3_mapper_v5.py` (chat instrument of record) | 28,027 | `2c5ca7a47042cc9929b891450f855c7e` |
| `g_poly1_phase3_mapper_cc.py` (CC independent mapper) | 36,218 | `f1cd9de544b1378da2cfea211db6eb52` |
| `poly1_phase3_cc.json` (CC read #1 — blind verdict read of record) | 11,808 | `2064bd7b4ed4f7b2b4e09bafdc0cf85a` |
| `poly1_phase3_chat_read3_X1_breach.json` (H-16 masked breach record) | 1,311 | `b99fa804d0bef0dc46615f2adedf86d6` |
| `poly1_hexghs_cc.json` (hex G_HS CC confirmation) | 3,785 | `96951e65df37700e30a8783aeb5dedfb` |
| `poly1_hexghs_chat.json` | 4,107 | `d74916a22984deab514e11164ef88725` |
| `g_poly1_hexghs_ccleg.py` / `g_poly1_hexghs_chatleg_v3.py` | 15,172 / 13,024 | `511e46b08a5cd8bddbdeb97702a4a36f` / `fba6439a3a14d8cbab19939f4ff33f39` |
| `staging_memo_G_POLY1_phase3_ADDENDUM_4.md` (P3-A4, FROZEN) | 5,481 | `659454eda11c969ce7d6736c6f1e1063` |
| `G_POLY1_PHASE3_RELOCK_RECORD_4.md` (re-lock 4, E3-6(a)) | 1,706 | `98be3e3c0071bebad816aeca4ea96755` |
| `G_POLY1_PHASE3_CC_REPORT.md` | 17,704 | `0feed9bd4c78e3a54658fbf25ad1d5da` |
| `extract_embeds.py` (P-4 extractor, declared 15-embed table) | 3,193 | `10cdf1a9bec460534d1e92f014f31b1f` |
| `compare_ghs.py` | 3,153 | `201c18adc9e3ccbf58273ded5814ca21` |
| `MANIFEST.md5` | 792 | (verbatim in §1.2) |

**1.1 Absent BY DESIGN (correct under P-4 / P-4.c):** the in-band dispatch `G_POLY1_PHASE3_CC_DISPATCH_INBAND.md` `e24d047b` (90,387 B) and the sealed anchor file `anchors_G_POLY1_SEALED.md` `a1d19dd98151cd7299af41fb14584c6f` (2,470 B) are not committed as loose files; the extractor was their only reader. The extractor's declared table (recovered byte-exact) pins the full frozen chain by md5 and size: `staging_memo_G_POLY1_phase3.md` `e16a78906560d2bb076d0699966981ac` (7,965 B); P3-A1 `ba75b113e8ad094cd752026df4e73977` (5,066 B); P3-A2 `ac87bc92890c7bf6a08b3d67d493ec9c` (3,567 B); P3-A3 `257b81bf3924cb92ca9d1232fb94325c` (4,247 B); lock record `abb463d75a96fc9913123562ff1fecbf` (2,167 B); re-locks `7f4b53ad43af3aff55938726d8f26738` (1,368 B) / `b1150c946f6986a9bc19ae2b073db83e` (963 B) / `6a7069b07c2184eea41dfc38b4446c9d` (1,531 B); mapper v4 `413996ae82cdb16545e5568622ee89ca` (24,906 B); pin addenda `57dfd40e5f0dbb311a64b30a67a47df6` (5,441 B) / `3d419b8f7196efd895fc5079df8760b4` (3,449 B); `poly_vrh_results.json` `200e7a8b775577564369c6924d38a84c` (2,767 B).

**1.2 `MANIFEST.md5` verbatim (non-quarantined; carried so the future dispatch can assert in-repo byte-identity by SHA + manifest instead of re-embedding the machinery):**
```
201c18adc9e3ccbf58273ded5814ca21  compare_ghs.py
10cdf1a9bec460534d1e92f014f31b1f  extract_embeds.py
511e46b08a5cd8bddbdeb97702a4a36f  g_poly1_hexghs_ccleg.py
fba6439a3a14d8cbab19939f4ff33f39  g_poly1_hexghs_chatleg_v3.py
f1cd9de544b1378da2cfea211db6eb52  g_poly1_phase3_mapper_cc.py
2c5ca7a47042cc9929b891450f855c7e  g_poly1_phase3_mapper_v5.py
96951e65df37700e30a8783aeb5dedfb  poly1_hexghs_cc.json
d74916a22984deab514e11164ef88725  poly1_hexghs_chat.json
2064bd7b4ed4f7b2b4e09bafdc0cf85a  poly1_phase3_cc.json
b99fa804d0bef0dc46615f2adedf86d6  poly1_phase3_chat_read3_X1_breach.json
0feed9bd4c78e3a54658fbf25ad1d5da  G_POLY1_PHASE3_CC_REPORT.md
98be3e3c0071bebad816aeca4ea96755  G_POLY1_PHASE3_RELOCK_RECORD_4.md
659454eda11c969ce7d6736c6f1e1063  staging_memo_G_POLY1_phase3_ADDENDUM_4.md
```

**1.3 Absent chat-side (lost with session storage; hashes ledger-recorded; D-W-1):** chat-4 checkpoint `bc30a6d3` (6,509 B), expectation pins `b9d08e6c`, Phase-3 closure memo `43dca454` (6,243 B), and the G-S2C1 chat P2 estate (checkpoints `0328b570` / `6da62fca` / `0e8cc05e`, Phase-3 `48927b9a`, P2-A evaluation `56b17d93`, fold packet `f0c81745`). None is load-bearing for this memo: the G-POLY1 edges are pinned from the *blind leg of record* `2064bd7b` (§2.3), and the G-S2C1 inputs are pinned from the V4.80 canonical text (§2.1–2.2) with the CC returns (`gsmiya` `cd51a00`; `3xgb2b` `debce15`) as the byte-level backstop.

**1.4 Machinery components confirmed intact and reusable as-is:** `att_edge` (Born closed form + fixed-point (1+q²)² dressing, contraction-basin fallback), `bir_edge` (δ_RMS(L) = s₁·√(d/L) inverted), the envelope clip `KD_CLIP = 0.3` (kd ≤ 0.3, edges beyond it VOIDED), the regime rule `N_MIN = 10` (birefringence channels VOIDED below N = (s₁/B)²), the four-arm map `['hex:step','hex:gem8','cubic:step','cubic:gem8']` with the banked Q_T^a and s₁ quartets as constants, the sealed-file single-read with md5 assertion, the T1 self-grep (split-string form), the R-B masking (`rb_mask`), the masked X-1 abort (catch-all), the P3-A4 lexer guards (frozen-token conformance `{ceiling, bound, margin, criterion}`; identifier/sign glue class `[A-Za-z0-9_.-]`; strict positivity), the nine pre-read suites, per-arm `eval_arm` with OOM ×10 relaxation, `gate_class`, `W_union`. **Nothing modified. Nothing executed.** The successor instrument (§8) extends this lineage by ONE anchor kind; it does not rewrite it.

---

## 2. Pinned inputs (frozen upstream by two-leg hash; NO re-fitting permitted at any stage of this gate)

**2.1 Lattice-scale dispersion, a₂ ≡ a₂^L (§2.91.O P1; gem8 U = 20e^{−r⁸}, a\* = 1.46059, μ = 53.225 fixed, ⟨ρ⟩ = 0.999988; c_T = 5.04820 chat / 5.04824 CC; o₂ = 0.99999999; F-ISO 1.3×10⁻⁵).** Joint fit ω_T/k = c_T(1 + a₂(ka\*)² + a₄(ka\*)⁴) over the A-2 common floor-clean rung set {0.3, 0.15, 0.075, 0.0375}:

| direction | chat leg (`5ee152fc` ladder; A-2 eval `77fea65f`) | CC leg (`gsmiya` @ `cd51a00`) |
|---|---|---|
| Γ–K | −1.2794×10⁻² | −1.324×10⁻² |
| Γ–M | −1.9933×10⁻² | −2.063×10⁻² |

CI of record = the inter-leg spread (3.5%). **a₄ (lattice) is UNRESOLVED and EXCLUDED** (not verdict-bearing at G-S2C1; not consumed here). Both a₂ values are negative in both directions on both legs (sub-cone-going at O(k²)).

**2.2 Grain-scale dispersion, a₂^agg (§2.91.O P2; E-P2-1 (a) — the polarization-averaged shear cone under full SO(3) IS the aggregate S2 channel; P2-A: a₂^agg of record = the analytic second-order Born real part D2 = Σ_M N_M[(1−2r_M²)I₀/8 − 3I₂/8], identical on both legs' kernels to 2×10⁻¹⁶):**

| arm (mapper label ↔ G-S2C1 label) | a₂^agg (two-leg ≤ 3.4×10⁻¹³) | a₄^agg (two-leg ≤ 0.5%; diagnostic only) | D(0) static Born shift |
|---|---|---|---|
| `hex:step` ↔ step_hex | −1.834766×10⁻² | +0.0695 | −2.05×10⁻² |
| `hex:gem8` ↔ gem8_hex | −2.593369×10⁻² | +0.0990 | −2.89×10⁻² |
| `cubic:step` ↔ step_cubic | −2.853747×10⁻² | +0.1068 | −3.15×10⁻² |
| `cubic:gem8` ↔ gem8_cubic | −3.971398×10⁻² | +0.1493 | −4.37×10⁻² |

R(k) = Δ − D2·k² analytic in k² (pure even basis both legs; the pre-registered k³ term REFUTED, H-S2C-10). Chat checkpoints `48927b9a` (Phase-3) / `56b17d93` (P2-A); CC return `3xgb2b` @ `debce15`; comparator `aa887e6c` 69/69 both sides. **Label-order pin (the H-S2C-7 swap class):** the mapper arm order and the G-S2C1 quartet order coincide position-for-position as tabulated; the instrument MUST assert the pairing by name, not by index.

**2.3 G-POLY1 per-arm edges of record (blind leg of record `2064bd7b`, recovered byte-exact; class P-2 every arm; OOM ×10 robust both directions; governing anchor A-1 on every arm):** `hex:step` 2.1213132100130068 m; `hex:gem8` 1.8866794048346085 m; `cubic:step` 1.838266105289967 m; `cubic:gem8` 1.6447865351995365 m; W_union = (0, 2.1213132100130068]. **These enter G-S2C1-W as PINNED NUMBERS — the G-POLY1 sealed file is NOT re-opened (§5, EG-3).**

**2.4 Also pinned (unchanged, from mapper v5 constants):** Q_T^a = {3.519074e-2, 5.002055e-2, 5.407763e-2, 7.549430e-2}, Q_T^d = Q_T^a/8; s₁ = {1.51508022e-1, 1.81569447e-1, 2.33348904e-1, 2.84231508e-1}. Report-only tie-in carried from §2.91.O: a₂^agg/Q_T^a = −0.52 ± 0.9% across the quartet — a consistency check between the dispersion and attenuation arms (F-W-PIN), not a verdict quantity.

**F-W-PIN (pre-read gate):** the instrument re-reads every §2 value from a pinned-inputs JSON whose md5 is declared in the lock record; any deviation from the values tabulated here > 10⁻¹² relative → masked halt before any sealed open.

---

## 3. Operational definition of W_∪′

**3.1 Channel identification (inherited imports, not re-adjudicated):** at the grain scale the S2 channel is the polarization-averaged shear cone (E-P2-1 (a)); at the lattice scale it is the E₂/quadrupole doublet (θ_id = 0.90). The G-POLY1 attenuation and birefringence constraint curves therefore remain the correct leading-order curves for the S2 carrier — G-S2C1 did not remove the cone, it dressed it with O(k²) dispersion. W_∪′ is that dressing made into constraints.

**3.2 Dispersion law of record (per arm A, wavenumber k, domain scale d, physical lattice constant a_phys):**

  δ_φ,A(k; d, a_phys) ≡ v_φ/c_T − 1 = a₂^agg[A]·(k d)² + a₂^L·(k a_phys)²   (+ a₄^agg[A]·(k d)⁴, diagnostic)

  δ_g,A(k; d, a_phys) ≡ v_g/c_T − 1 = 3·a₂^agg[A]·(k d)² + 3·a₂^L·(k a_phys)²   (from ω = c_T k(1 + a₂x²) ⇒ dω/dk = c_T(1 + 3a₂x²))

Assumption **S-W-1 (declared, load-bearing):** leading-order additivity of the two scales under the scale separation d ≫ a_phys — the intra-grain lattice term rides inside every grain independently of grain size; cross terms are O((ka)²(kd)²) and dropped. Both terms are negative; the lattice term is a **floor** the grain term cannot cancel.

**3.3 Anchor kinds.** The four G-POLY1 kinds — `att` (attenuation, `att_edge`), `ceil` (attenuation + birefringence), `dlm` (birefringence, `bir_edge`), `vld` (validity cap) — are carried **as pinned edges only** (§2.3; their BIR channels were VOIDED by N ≥ 10 at G-POLY1 and stay so). ONE new kind is introduced:

  `disp` — fields: budget B (dimensionless |δ| bound), binding quantity q ∈ {phase, group}, wavenumber field (a single k_ref or a band [k₁, k₂]), reading class (bound / ceiling / margin / criterion — the frozen P3-A1 §2(b) token list, unchanged), OOM class. Anchors of the *speed-offset* class (an arrival-time or common-limiting-speed statement at a stated wavenumber/band) and of the *modified-dispersion-relation* class (a bound on a k-dependent term of the stated order) both instantiate `disp`; the sealed text's own statement decides q (D-W-4 gives the default when the text is silent).

**3.4 The dispersion edge (new; Born, then dressing, mirroring `att_edge`):** for a `disp` anchor with budget B at wavenumber k and quantity q (c_q = 1 for phase, 3 for group):

  (i) lattice floor F_L(k) = c_q·|a₂^L|·(k a_phys)²  (a_phys per E-W-1; a₂^L per E-W-2);
  (ii) residual budget B′ = B − F_L(k);
  (iii) **if B′ ≤ 0 → FAIL-L** for that anchor (channel-level; independent of d; NOT a window edge — §7);
  (iv) Born edge d_disp = √(B′/(c_q·|a₂^agg[A]|)) / k;
  (v) envelope: if k·d_disp > KD_CLIP = 0.3 the edge is **VOIDED** (outside the Born/long-wavelength regime the law of record was measured in; a VOID can only widen a window — E-11 lineage) and reported with its envelope ceiling 0.3/k;
  (vi) dressing diagnostic Δ₄ = |a₄^agg[A]|·(k d_disp)² / |a₂^agg[A]| at the edge; if Δ₄ > 0.10 the edge is flagged **DRESSING-SENSITIVE** and the dressed fixed-point edge (the root of c_q(|a₂^agg|x² − a₄^agg x⁴) = B′ in x = kd, seeded at the Born value, contraction-basin fallback as in `att_edge`) is REPORTED alongside; the edge OF RECORD is the Born (a₂-only) value per default D-W-5 (author veto standing);
  (vii) band anchors: evaluated at the wavenumber in [k₁, k₂] that minimizes d_disp (D-W-6: the upper band edge k₂, with the full band sweep serialized).

**3.5 Per-arm window.** W′_A = (0, min{ all NON-VOIDED upper edges: the pinned G-POLY1 edge of A (§2.3), every `disp` edge of A, every `vld` cap }]. Per-arm class:
  - **P-2′ (PASS-UNBOUNDED-BELOW)** — finite positive edge, no FAIL-L;
  - **FAIL-L** — any `disp` anchor's floor consumes its whole budget (§7);
  - **VOID-DISP** — every `disp` edge VOIDED (the window then equals the pinned G-POLY1 edge; class INERT below).
  OOM robustness: every `disp` budget relaxed ×10 and tightened ×0.1; the class is OOM-ROBUST iff unchanged under both.

**3.6 The union.** W_∪′ = ∪_A W′_A = (0, max_A edge_A] — **CONSERVATIVE** by the E3-6(a) lineage (the widest reading; any corrected reading only tightens, never empties). The strict intersection ∩_A is serialized alongside, non-verdict. Per-arm windows, the union, the intersection, the voided-edge table, and the OOM bands are all serialized in the checkpoint before any comparison (§5).

**3.7 Comparison of record (LAST; quarantined):** W_∪′ against the pinned W_∪ upper edge 2.1213132100130068 m:
  - **TIGHTENED** — W_∪′ ⊊ W_∪ (at least one `disp` edge governs on the governing arm);
  - **INERT** — W_∪′ = W_∪ on the governing arm (no `disp` edge governs; the dispersion arms are non-binding at the sealed budgets);
  - **FAIL-L** — as above, on the governing arm or on all arms (reported per arm);
  - **F-W-MONO** — W_∪′ ⊋ W_∪ is impossible by construction; if it occurs the run halts as an S9-class instrument defect (a pinned-edge or arm-map fault), never a finding.
  **INERT ≠ reinstatement.** Whether an INERT or TIGHTENED W_∪′ re-enters any Phase-3-style intersection is E-W-7, decided by the author at fold, not by the instrument.

**3.8 M-naive expectation, REGISTERED PRE-DATA (the §2.91.O practice; not a target, not consulted by any instrument):** under every a_phys chain currently on the ledger the lattice floor is expected to be many orders below any conceivable sealed budget — expected VOID-TRIVIAL for F_L, so W_∪′ is expected to be governed by the grain-scale `disp` arms. Whether those arms land TIGHTENED or INERT is **NOT predicted** — it depends on the sealed budgets and wavenumbers this memo has deliberately not seen. FAIL-L is expected NOT to fire; if it does, the finding is channel-level and the routing is §7.

---

## 4. The lattice-scale physical pin (a_phys) — the one new import this gate touches

a₂^L is dimensionless in (k a\*) with a\* = 1.46059 in substrate units (kernel-range units of the gem8 GP soft-core state). A physical a_phys requires the transverse-scale chain, which the framework has DECLARED but never exercised in a dispersion arm. This memo does not pick; it enumerates the election **E-W-1** with named consequences:

  (a) **Declared chain:** ξ = ℓ_P (G-SCALE1, §2.91.F/ANNEX-SC-1 reading (a)) and the G-C1 class-(b) ratio C = ξ/a ∈ [0.0213, 0.0851] (the measured sweep range; a knob, not a pure number) ⇒ a_phys ∈ [ℓ_P/0.0851, ℓ_P/0.0213] as an **interval**. F_L evaluated at BOTH ends; the window uses the smaller a_phys (conservative, widest); **FAIL-L is declared only if it fires at the smaller a_phys too** (a kill must be election-robust — the G-SCALE1 pattern); the larger-a_phys result serialized as the robustness arm. (Default D-W-1.)
  (b) **Unexercised:** a_phys undeclared; F_L omitted (F_L ≡ 0); the lattice term reported as a named, unexercised import (T4 discipline); W_∪′ then depends on a₂^agg alone. Honest, but leaves the directive's "two dispersion scales" half-executed — recorded as such if elected.
  (c) **Author-supplied a_phys** (a single value or interval), T3 on lock.

**E-W-2 (direction rule for a₂^L in the aggregate floor):** the single-crystal a₂ is direction-dependent (Γ–K vs Γ–M); inside a randomly oriented grain the floor is an orientation average. Options: (a) the smaller magnitude (Γ–K; conservative for the window); (b) the arithmetic mean of Γ–K and Γ–M; (c) the larger magnitude (Γ–M). Default: (a) for the window edge, (c) for the FAIL-L robustness arm — both serialized.

**E-W-3 (leg values):** each leg uses its OWN a₂ values (chat: §2.1 chat column; CC: §2.1 CC column); the comparator tolerance on every F_L-dependent quantity includes the 3.5% CI; a₂^agg is shared to 3.4×10⁻¹³ and needs no such allowance.

Under (a) the import delta of this gate is **zero** — every input was already declared (ξ = ℓ_P; the C-range; the two dispersion coefficients). Under (c) the import is the author's a_phys.

---

## 5. Eddington guard register (explicit log, per the directive)

| # | guard | mechanism |
|---|---|---|
| EG-1 | **Inputs frozen before any anchor exists.** | a₂, a₂^agg, a₄^agg, Q_T, s₁ and the four G-POLY1 edges are pinned by upstream two-leg hash (§2) and re-read from a pinned-inputs JSON whose md5 is in the lock record (F-W-PIN). No coefficient is re-fitted, re-selected, or re-averaged after the sealed file exists. |
| EG-2 | **Sealed anchors, single read, md5 + census asserted at every open.** | New file `anchors_G_S2C1_W_SEALED.md`, assembled AFTER this memo is locked and the T1 list frozen; opened only by the mapper phase; md5 and census (row count + per-class census) asserted at every open; masked X-1 abort on any parse defect; field separator drawn from a character class asserted absent from every anchor text (the H-16 pipe-collision guard); binder binds constants by NAMED KEY, never by magnitude window (the G-CI1 S9 root cause (A)). |
| EG-3 | **The G-POLY1 sealed file is NOT re-opened.** | Its four edges enter as pinned numbers from the blind leg of record `2064bd7b`. Disclosure **D-W-0**: those anchor values are disclosed in the V4.76/V4.77 ledger records, so no leg (and no ledger reader) is blind to them; the guard on that set is procedural — pinned inputs + pinned edges leave nothing to tune. |
| EG-4 | **Comparison LAST.** | The W_∪′-vs-W_∪ comparison (§3.7) and any OOM classification run only after every per-arm edge, VOID, and FAIL-L result is serialized and hashed; the pinned W_∪ edge is read by the comparison step alone. |
| EG-5 | **No per-arm tuning; no per-anchor tuning.** | KD_CLIP, N_MIN, the Δ₄ threshold, the fixed-point tolerance, the Born-vs-dressed rule and the band-evaluation rule are fixed in this memo (defaults D-W-5/6, ratified at lock), not chosen per arm or per anchor. |
| EG-6 | **M-naive expectation registered pre-data (§3.8); no numeric target.** | The memo states expected classes, not expected numbers; no anchor budget or wavenumber has been consulted in drafting; the chat leg has not seen any candidate `disp` anchor. |
| EG-7 | **T1 self-grep at every invocation and on every artifact, both legs, independently cross-scanned** (§6). | Pattern-lines-only scanning (G-BKZ32 H-2); split-string form inside instruments so the list cannot self-hit. |
| EG-8 | **Blindness order: CC-BLIND-FIRST** (E3-5(a) lineage; election E-W-5). | The CC read is the verdict read of record for the CLASS; the chat read follows. The chat leg's Phase-3 blindness on the G-POLY1 set was burned (H-16) and is burned for everyone by the ledger (D-W-0); on the NEW `disp` set the chat leg is blind until its read. |
| EG-9 | **OOM ×10 both directions on every `disp` budget; a kill must be election-robust.** | FAIL-L requires firing at the smaller a_phys AND under the ×10 relaxation of the budget; otherwise it is reported as OOM-FRAGILE, not declared. |
| EG-10 | **Vocabulary-substitution watch.** | "The S2 channel is dispersive" is a measured statement in substrate units; no physical-c, no physical-frequency, and no catalog identifier may appear in any instrument outside the sealed file's own text (the G-TSH1 grep discipline extended to this gate). |

---

## 6. T1 forbidden-string list — assembly plan (contents deliberately NOT reproduced here)

**6.1 Base set (RECOVERED byte-exact):** the seven FORBIDDEN patterns and two DECOY patterns embedded at lines 10–11 of `g_poly1_phase3_mapper_v5.py` (`2c5ca7a4`), plus the two mask-only tokens of its `rb_mask` T1SUB list. The list file `t1_forbidden_G_S2C1_W.txt` carries them in pattern-line form; instruments carry them in split-string form.

**6.2 Additions at assembly (by the party assembling the sealed file, §5 EG-2):** every identifier of every `disp` anchor — collaboration / catalog / event designations, the parameter-symbol family of the modified-dispersion parametrization, any bound digit string of ≥ 4 significant digits, the reference-wavenumber and reference-frequency strings, the distance and unit strings of any speed-offset anchor — each in the same split/pattern discipline.

**6.3 Merge on recovery (D-W-2):** the G-S2C1 list `8cd89b9a` (16 pattern lines) and the G-CI1 list `653a0b74` (1,127 B) are NOT recoverable chat-side this session (not in project knowledge; the CC branches `gsmiya` / `3xgb2b` / `xvqfm7` could not be listed — unauthenticated API quota exhausted; raw-path probes missed). They merge into `t1_forbidden_G_S2C1_W.txt` when recovered; the freeze waits on them unless the author elects to freeze without (E-W-4(ii)).

**6.4 Numeric-collision rule (default D-W-7, author ratification):** the G-S2C1 contextual-pattern amendment is ADOPTED for this gate — bare numeric patterns count as hits only when adjacent (within the glue class) to a unit or identifier token; machine-epsilon and exponent-formatting collisions (H-S2C-3/12, H-CC-P2-2 lineage) are logged, not fatal.

**6.5 This memo's own scan:** self-grepped against the base set (§6.1) before delivery — result reported in the chat return with the draft hash. The memo names no anchor, no catalog, no physical frequency, no physical distance, and no target digit string.

---

## 7. Falsifiers, arms, and the FAIL-L blast radius

| falsifier | fires when | consequence |
|---|---|---|
| F-W-PIN | any pinned input deviates > 10⁻¹² rel from §2, or the four G-POLY1 edges ≠ `2064bd7b` byte-values | masked halt pre-open; no read spent |
| F-W-ENV | k·d_disp > 0.3 for a `disp` edge | that edge VOIDED (reported with 0.3/k); never consumed |
| F-W-L | B′ ≤ 0 at the smaller a_phys AND under ×10 budget relaxation | **FAIL-L** on that arm/anchor (see below) |
| F-W-DRESS | Δ₄ > 0.10 at an edge of record | DRESSING-SENSITIVE flag; dressed edge reported; record edge stands |
| F-W-MONO | W_∪′ ⊋ W_∪ | S9-class instrument halt; never a finding |
| F-W-T1 | any T1 hit on any instrument or artifact | halt; artifact quarantined; H-item |
| F-W-CENSUS | sealed md5 or census mismatch at any open | masked abort; read NOT spent if pre-parse |

**FAIL-L blast radius (pre-declared, the §2.2/G-SCALE1 pattern):** FAIL-L is not a statement about d. It says the S2 carrier, under the declared scale chain and the measured single-crystal dispersion, is inconsistent with a sealed dispersion budget at the lattice scale alone. Routing: (i) the declared-chain reading E-W-1(a) is the thing tested — a FAIL-L is a constraint ON the a_phys chain (a second constraint curve on the same import G-C1 located), not a kill of the polycrystal postulate; (ii) the grain-scale `disp` edges are still computed and serialized under E-W-1(b) (F_L ≡ 0) as the fallback arm, labelled conditional; (iii) nothing in §2.91.O, §2.91.M, §2.91.N, Paper IIA, or the gauge-paper firewall is touched; (iv) a successor is named, not executed. Any verdict-aware re-pin of a_phys is Eddington-foreclosed by this clause.

---

## 8. Two-leg plan, instruments, and P-4 / P-4.b / P-4.c compliance

**8.1 Chat leg:** mapper v6 = the v5 lineage (§1.4, unmodified core) + the `disp` kind (§3.3–3.4) + the pinned-edge carry (§2.3) + the pinned-inputs gate (F-W-PIN) + the comparison-last step (§3.7). Pre-read suites: the nine v5 suites unchanged PLUS `disp` synthetics (C-SYN-D: Born edge on a hand-computed synthetic; envelope VOID; FAIL-L at a synthetic floor; Δ₄ threshold both sides; band-min rule; group-vs-phase c_q; masked abort on a malformed `disp` row) — all green before any sealed open (D-W-4). T1 self-grep at every invocation.

**8.2 CC leg:** an independent mapper from the frozen chain (own lexer, own edge formulas, own fixed-point, own union) — no code transfer; disclosure of defect CLASSES admissible (the H-7/H-18 precedent), code and synthetics not. The recovered Phase-3 machinery is referenced by commit SHA + `MANIFEST.md5` (§1.2); CC asserts in-repo byte-identity (verify-then-build) instead of receiving the machinery as embeds.

**8.3 Dispatch — ONE file, delivered ALONE.** `G_S2C1_W_CC_DISPATCH_INBAND.md`, P-4 (activation flags embedded; no side-channel message load-bearing), P-4.b (the sealed anchor file and any quarantined embed travel base64-armored), **P-4.c (the dispatch is delivered with NO loose file; the extractor is the only reader of embedded artifacts; any loose file at delivery is a logged deviation at the receiving leg).** Declared embed table (all `<<<BEGIN name>>> … <<<END name>>>` per the recovered extractor convention): this memo (frozen), the lock record, `t1_forbidden_G_S2C1_W.txt`, `anchors_G_S2C1_W_SEALED.md` (armored), `pinned_inputs_G_S2C1_W.json`, the frozen comparator + schema, and `MANIFEST.md5` + SHA for the machinery reference. Hashes and byte sizes for every embed in the dispatch §1 table; re-extraction-verified byte-exact before send.

**8.4 Comparator (frozen BEFORE either emission; the G-CI1/G-2a-L1 precedent):** C-W-1 per-arm edges of record (rel 10⁻⁶; F_L-dependent quantities at 10⁻⁶ + the 3.5% CI allowance); C-W-2 per-arm class + OOM class + gate class identity; C-W-3 sealed md5 + census identity; C-W-4 lexer readings identical except pre-registered divergences (each leg pins expected divergences before the chat read, the b9d08e6c/CC-§9 pattern); C-W-5 pinned-inputs identity; C-W-6 T1 zero hits both legs. S9 on any C-W miss; resolution by the path-(a) mini-dispatch pattern if representational.

**8.5 Delivery of THIS memo:** one file, no companions — the recovered machinery stays in the repo at the pinned SHA and is not re-shipped loose (the lone-delivery discipline applied to the staging artifact itself).

---

## 9. Deviations, disclosures, and honesty items opened at staging

- **H-W-0** (recovery): 14 files, manifest 13/13, every ledger-cited hash matched; commit pinned; nothing modified; nothing executed.
- **D-W-0** (blindness): the four G-POLY1 anchor values are ledger-disclosed (V4.76/V4.77); no party is blind to them; guard procedural (EG-3).
- **D-W-1** (lost chat estate): §1.3 items absent from project knowledge; values pinned from V4.80 canonical text + `2064bd7b`; byte re-verification of the G-S2C1 chat P2 checkpoints pending recovery (CC `3xgb2b` return or author upload).
- **D-W-2** (T1 merge): `8cd89b9a` and `653a0b74` unrecovered this session (§6.3).
- **D-W-3** (lattice CI): a₂^L carries the 3.5% inter-leg spread; the lattice a₄ term is unresolved and excluded; F_L therefore carries a stated ±3.5% (and an unquantified O(k⁴a⁴) truncation, expected negligible under E-W-1(a)).
- **D-W-4** (new kind): `disp` has no precedent in the v5 suites; the C-SYN-D suite is a pre-read obligation on both legs.
- **D-W-5** (scope): the aggregate reading inherits, as imports, E-P2-1 (a), the Born/second-order (SOA) order of P2, G-POLY1's E3 elections, and S-W-1 additivity; none is re-adjudicated here.
- **D-W-6** (environment): GitHub directory listing was rate-limited mid-recovery; the Phase-3 directory was fetched before the limit and verified by manifest; the G-S2C1 CC branches were not listed (§6.3).

---

## 10. Elections requested (T3-immutable on lock; NONE decided by this memo)

| election | question | options (default in bold) |
|---|---|---|
| E-W-1 | a_phys chain for the lattice floor | **(a) declared chain ξ = ℓ_P + G-C1 C-interval** / (b) unexercised, F_L ≡ 0 / (c) author-supplied |
| E-W-2 | a₂^L direction rule in the aggregate floor | **(a) Γ–K for the window, Γ–M for the FAIL-L robustness arm** / (b) mean / (c) Γ–M throughout |
| E-W-3 | leg values | **each leg its own a₂; CI in comparator** / shared chat values |
| E-W-4 | sealed `disp` census and assembler | (i) author-supplied sealed file / (ii) chat-assembled under masking with the C-P3-4 criterion; **freeze T1 after D-W-2 merge** / freeze without |
| E-W-5 | leg order | **(a) CC-BLIND-FIRST** / (b) chat-first |
| E-W-6 | edge of record | **(a) Born a₂-only; dressed reported** / (b) dressed fixed-point of record |
| E-W-7 | downstream semantics of W_∪′ | decided at fold only: **(a) W_∪′ banked alongside the suspended W_∪, no reinstatement** / (b) W_∪′ replaces W_∪ in the Phase-3 intersection (a PF-S2 reversal — requires its own authorization) |

Defaults D-W-1 (interval ends), D-W-4 (silent text ⇒ q = group for arrival-time-class rows, phase for coherence-class rows), D-W-5 (Δ₄ threshold 0.10), D-W-6 (band evaluated at k₂), D-W-7 (contextual numeric rule) — ratified by the lock word unless vetoed.

---

## 11. What this memo does NOT do

No lock. No sealed file. No T1 freeze. No instrument written. No computation. No read. No window. No reinstatement. No §2.x / §3.x text. No register change. No fold. No memory write. The recovered machinery is unchanged and unexecuted.

**Lock protocol when authorized:** the author's lock word freezes THIS FILE byte-identical (md5 reported in the chat return; a lock record then cites it); any change before lock is a new draft with a new hash, never an edit under the old one.
<<<END staging_memo_G_S2C1_W.md>>>

<<<BEGIN G_S2C1_W_LOCK_RECORD.md>>>
# G-S2C1-W — LOCK RECORD (staging memo lock; elections E-W-1..E-W-7; T1 freeze; pinned inputs)

**Date:** September 8, 2026. **Base:** `SQT_Master_Ledger_v4_80_CANONICAL.md` md5 `a28e9b40616ee9b5798e9a5be027c1d9` (1,514,144 B). **Gate:** G-S2C1-W, the W_∪′ re-derivation mini-gate (successor named at V4.80 PF-S2, §2.91.O). **Chat leg:** this instance. **Order of record:** register (memo) → lock (this record) → leg. No leg has run.

## 1. Author authorization (verbatim)

> **Directive: Lock G-S2C1-W Staging Memo and Proceed**
> The recovery of the Phase-3 machinery is confirmed. The staging memo (md5: 1ebb6a82fcb24e207b164a654eb94dd1) is approved.
> I explicitly AUTHORIZE the lock of the staging memo with the following elections:
> * E-W-1: (a) declared chain ξ = ℓ_P + G-C1 C-interval.
> * E-W-2: (a) Γ–K for the window, Γ–M for the FAIL-L robustness arm.
> * E-W-3: (a) each leg uses its own a₂; CI in comparator.
> * E-W-4: (i) author-supplied sealed file. Freeze T1 without D-W-2 merge.
> * E-W-5: (a) CC-BLIND-FIRST.
> * E-W-6: (a) Born a₂-only; dressed reported.
> * E-W-7: (a) W_∪′ banked alongside the suspended W_∪, no reinstatement.
> The defaults (D-W-1, D-W-4, D-W-5, D-W-6, D-W-7) are ratified.
> 1. Generate the lock record. 2. Freeze the T1 list and provide its hash. 3. Provide the `pinned_inputs_G_S2C1_W.json` so I can verify its contents before I provide the sealed anchor file.
> Do not write or execute the chat-side instrument until I provide the sealed anchors.

## 2. LOCKED — the staging memo

`staging_memo_G_S2C1_W.md` — md5 **`1ebb6a82fcb24e207b164a654eb94dd1`**, sha256 `b29db538886d21e6694c84d7f3a0272fae01294f992515f23656816f2bca9eff`, **32,219 B**, verified byte-identical at lock (September 8, 2026) to the approved draft delivered the same day. The file is never edited: its own header line ("Status: DRAFT — NOT LOCKED") stays as drafted and is superseded by this record — byte-identity is the ledger. Any change is a new draft with a new hash, staged under an addendum, never an edit under the old hash.

## 3. Elections — T3-immutable

| election | locked reading |
|---|---|
| E-W-1 | **(a)** declared chain: ξ = ℓ_P (G-SCALE1 reading (a)) + the G-C1 class-(b) interval C = ξ/a ∈ [0.0213, 0.0851] ⇒ a_phys = ℓ_P/C as an interval; window edge at a_phys.lo; FAIL-L only if it fires at a_phys.lo AND under the ×10 budget relaxation (EG-9); a_phys.hi serialized as the robustness arm |
| E-W-2 | **(a)** a₂^L = Γ–K for the window edge; Γ–M for the FAIL-L robustness arm — both serialized |
| E-W-3 | **(a)** each leg uses its own a₂ column; the comparator carries the 3.5% CI on every F_L-dependent quantity |
| E-W-4 | **(i)** the sealed anchor file `anchors_G_S2C1_W_SEALED.md` is AUTHOR-SUPPLIED; **T1 frozen WITHOUT the D-W-2 merge** (the G-S2C1 `8cd89b9a` and G-CI1 `653a0b74` lists are not part of this gate's T1 — D-W-2 disposed by election, disclosed permanently) |
| E-W-5 | **(a)** CC-BLIND-FIRST: the CC read is the verdict read of record for the CLASS; the chat read follows |
| E-W-6 | **(a)** edge of record = Born a₂-only; the a₄-dressed fixed-point edge REPORTED alongside; Δ₄ > 0.10 → DRESSING-SENSITIVE flag |
| E-W-7 | **(a)** W_∪′ is BANKED ALONGSIDE the suspended W_∪; NO reinstatement; INERT ≠ reinstatement; any PF-S2 reversal requires its own authorization |

**Defaults RATIFIED:** D-W-1 (a_phys interval ends), D-W-4 (silent sealed text ⇒ q = group for arrival-time-class rows, phase for coherence-class rows), D-W-5 (Δ₄ threshold 0.10), D-W-6 (band anchors evaluated at the upper band edge k₂; full sweep serialized), D-W-7 (contextual bare-numeric rule; formatting collisions logged, not fatal). Import delta under E-W-1(a): **zero** (every input previously declared).

## 4. FROZEN — the T1 forbidden-string list

`t1_forbidden_G_S2C1_W.txt` — md5 **`20ba1e7eab5a3bbffe510b4840edbc57`**, **1,560 B, 34 pattern lines** (pattern-lines-only convention, G-BKZ32 H-2; `#` lines are documentation, not patterns). Composition: **11** base patterns recovered byte-exact from `g_poly1_phase3_mapper_v5.py` `2c5ca7a4` (the seven FORBIDDEN, the two DECOYS retained as forbidden, the two `rb_mask` T1SUB tokens promoted to patterns); **21** identifier-class patterns for the S2-side dispersion / speed-offset anchor literature (names, symbols, units — **no numeric bounds**; the chat leg consulted no candidate anchor value in cutting them); **2** G-POLY1 sealed-reference strings (ledger-disclosed at V4.76; the G-POLY1 sealed file is not re-opened, so they may never appear in an instrument of this gate).

**T1 Addendum 1 (T1-A1) protocol:** at sealed delivery the author appends the anchor-specific identifiers and the bound / wavenumber / distance digit strings of the sealed file as `t1_forbidden_G_S2C1_W_A1.txt`, frozen with its own md5 declared in a lock-record addendum; every instrument scans base ∪ T1-A1. Justified scan exemptions (as at G-POLY1): the sealed file itself, the two list files.

**Scanner of record for this gate:** `t1_scan.py` md5 `ccd47ac5779c6592bb3c49d6890049e9` — implements the memo §6.4 D-W-7 rule (non-numeric patterns unconditional; a bare-numeric pattern is a HIT only when glued to a letter/underscore token; digit/sign/dot glue and exponent suffixes are LOGGED, not fatal); reports pattern indices, never echoes patterns. Independent CC re-implementation expected (disclosure-level rule only; no code transfer).

**Scan results at lock:** staging memo — 34 patterns, **0 hits, 0 logged**; `pinned_inputs_G_S2C1_W.json` — **0 hits, 1 logged** (H-W-1 below); this lock record — result appended at §9.

## 5. PINNED — the inputs file (author verification = pre-Phase-0 gate)

`pinned_inputs_G_S2C1_W.json` — md5 **`d1edc69b16dfd0b728a48cd8389b322b`**, **5,769 B**. Carries: provenance (ledger base, memo, T1, machinery commit `dd813646ed…`, the G-POLY1 blind-leg checkpoint `2064bd7b`); the arm map (by name, H-S2C-7 rule); a₂^L both legs both directions with the 3.5% CI and the a₄^L exclusion; the a₂^agg quartet (two-leg ≤ 3.4×10⁻¹³) and the a₄^agg diagnostic quartet; D(0); Q_T^a, the Q_T^d rule, s₁; the report-only tie-in; **the four G-POLY1 per-arm edges read programmatically from `2064bd7b`** (2.1213132100130068 / 1.8866794048346085 / 1.838266105289967 / 1.6447865351995365 m, all P-2, union upper 2.1213132100130068 m); the E-W-1(a) chain — ℓ_P = 1.616255×10⁻³⁵ m (CODATA 2018), C ∈ [0.0213, 0.0851], **a_phys ∈ [1.8992420681551118×10⁻³⁴, 7.588051643192489×10⁻³⁴] m**; the constants (KD_CLIP 0.3, N_MIN 10, Δ₄ threshold 0.10, fixed-point tol 10⁻¹⁵ / 200 iterations, c_q phase 1 / group 3, band rule k₂, OOM ×10 / ×0.1, comparator 10⁻⁶, pin 10⁻¹²); the locked elections; the ratified defaults; the exclusions. **It contains no anchor, no budget, no wavenumber, no comparison.**

**Verification gate:** the author's word on this file's contents is required before Phase 0. Any correction is a `v2` with a new md5 recorded in a lock-record addendum; the memo is untouched. The instrument's F-W-PIN gate asserts this file's md5 (or the v2 md5) before any sealed open.

## 6. Honesty ledger opened at lock

**H-W-0** (recovery, from the memo §1): 14 files, manifest 13/13, every ledger-cited hash matched; commit pinned; nothing modified or executed.

**H-W-1 (chat, self-caught at lock, pre-verdict, no artifact consumed):** on its first run the chat scanner counted digit-glue as identifier-glue for numeric patterns — stricter than the locked memo's D-W-7 text — and flagged the pinned-inputs file: the decimal rendering of the pinned chat a₂(Γ–M) = −1.9933×10⁻² (`-0.019933`) contains the digit run of one of the two mapper-v5 DECOY patterns retained in the frozen list. Disposition: (i) the T1 list is NOT re-cut (re-cutting a frozen list to dodge a collision is the reflex the discipline forbids); (ii) the scanner was corrected to the memo's rule — digit/sign/dot glue and exponent suffixes are formatting collisions, logged not fatal; (iii) the pinned value is a legitimate two-leg input, not a forbidden reference — the H-S2C-12 / H-CC-P2-2 numeric-collision class; (iv) the collision stands LOGGED on the JSON scan (1 logged, 0 hits). Both scanner versions' hashes are on the record (defective first cut superseded pre-use; `be054b9f` → `ccd47ac5`).

## 7. Pre-Phase-0 gates (all must be green before any read; each item halts the chain if missing)

1. Sealed anchor file `anchors_G_S2C1_W_SEALED.md` **author-supplied** (E-W-4(i)); md5 and census (row count + per-class census incl. the `disp` count) declared by lock-record addendum; field separator asserted absent from every anchor text (H-16 guard); constants bound by NAMED KEY only (G-CI1 S9 root cause (A)).
2. **T1-A1** appended by the author and frozen (md5 in the same addendum).
3. **Author verification word** on `pinned_inputs_G_S2C1_W.json` (or its v2).
4. Chat instrument (mapper v6 = v5 lineage + the `disp` kind + pinned-edge carry + F-W-PIN + comparison-last) written **only after items 1–3** per the directive; the nine v5 suites + C-SYN-D suite all green pre-read; T1 self-grep at every invocation.
5. Comparator + schema (C-W-1..6) FROZEN before either emission.
6. In-band CC dispatch `G_S2C1_W_CC_DISPATCH_INBAND.md` built: P-4 (activation flags embedded), P-4.b (sealed file and any quarantined embed base64-armored), **P-4.c (delivered ALONE; no loose file; the extractor is the only reader; any loose file at delivery is a logged deviation at the receiving leg)**; machinery referenced by commit SHA + `MANIFEST.md5` (verify-then-build), not re-embedded; every embed re-extraction-verified byte-exact before send.
7. **CC-BLIND-FIRST** read (E-W-5(a)); CC checkpoint hashed and returned to the chat workspace before the chat read (the re-lock-4 gate pattern).
8. Chat read; two-leg comparison C-W-1..6; S9 on any miss; fold only on separate authorization.

## 8. NOT authorized by this record

No instrument written; no execution; no read; no window; no comparison; no fold; no reinstatement; no §2.x / §3.x; no register change. The directive's standing instruction — **do not write or execute the chat-side instrument until the sealed anchors are provided** — is in force.

## 9. Delivery note and self-scan

Three lock artifacts (this record, the frozen T1 list, the pinned-inputs JSON) are delivered to the AUTHOR as separate hashed files alongside the already-delivered locked memo; this is a lock delivery to the author, not a leg dispatch — they will travel to the CC leg only inside the single in-band dispatch of gate 6 (P-4.c). Self-scan of this record against the frozen list: reported in the chat return with this record's md5 (the record cannot carry its own hash).
<<<END G_S2C1_W_LOCK_RECORD.md>>>

<<<BEGIN G_S2C1_W_LOCK_RECORD_ADDENDUM_1.md>>>
# G-S2C1-W — LOCK RECORD ADDENDUM 1 (sealed anchors; T1-A1; declared CC checkpoint; delivery deviations)

**Date:** September 8, 2026. **Amends:** `G_S2C1_W_LOCK_RECORD.md` `5f963ed8d7eff9f803da5c1eea2f841a` (10,875 B) under its §7 gate sequence. **Memo:** `1ebb6a82fcb24e207b164a654eb94dd1` LOCKED (untouched). **Pinned inputs:** `pinned_inputs_G_S2C1_W.json` `d1edc69b16dfd0b728a48cd8389b322b` — **AUTHOR-VERIFIED** (directive of this date; §7 gate 3 GREEN).

## 1. Author directive (verbatim, operative clauses)

> The lock record, frozen T1 list, and the pinned inputs JSON are confirmed. I explicitly VERIFY the contents of `pinned_inputs_G_S2C1_W.json` (d1edc69b16dfd0b728a48cd8389b322b). I provide the sealed anchor file and the T1-A1 addition below.
> 1. Generate the Lock Record Addendum stating the MD5 of the sealed anchor file and the MD5 of T1-A1. 2. The sealed file contains 1 row (`disp` class). Confirm this census. 3. Build the chat instrument (mapper v6). Run the pre-read suites (C-SYN-D). 4. Build the frozen comparator and schema. 5. Construct the P-4/P-4.b/P-4.c single-file in-band CC dispatch (`G_S2C1_W_CC_DISPATCH_INBAND.md`). Ensure ALL constraints of P-4.c are met: the dispatch must be completely self-contained with no loose files. 6. The CC leg has been executed externally. The CC checkpoint md5 is: `97f26c04f982b1cc1694f4a47bdce882`. (Use this hash in the closure log). 7. Unseal the anchors, execute the Chat leg read, run the comparator against the CC checkpoint hash, and report the verdict.

## 2. SEALED — the anchor file (E-W-4(i), author-supplied)

`anchors_G_S2C1_W_SEALED.md` — md5 **`8c7d59f64057e372d7b1ff760667a7c2`**, **154 B**. Canonical serialization of record: the one row exactly as supplied between the author's BEGIN/END markers, followed by a single trailing newline (LF), UTF-8, no leading pipe. **Census (confirmed by machine): 1 row; per-class {`disp`: 1}; 8 pipe-delimited fields per row (7 content fields + the trailing empty field from the closing bar); separator guard PASS (no bar inside any field).** Field map bound by NAMED KEY (never by magnitude window — the G-CI1 S9 root cause (A) rule): f0 class, f1 anchor id, f2 source designation (masked in every artifact), f3 binding quantity q ∈ {phase, group}, f4 `B = <budget>`, f5 `k = <wavenumber> /m`, f6 Caveat/Binding clause (carried verbatim inside the sealed file only; masked elsewhere). The file is a justified T1-scan exemption (as at G-POLY1). Opened ONLY by the mapper phase, single read per leg, md5 + census asserted at open.

**C-W-3 pin for the CC leg:** the CC checkpoint must carry `sealed_md5 = 8c7d59f64057e372d7b1ff760667a7c2` and the same census; a differing sealed md5 on the CC side means a differing serialization (whitespace/newline), to be resolved by byte comparison of the two files, not by re-reading.

## 3. FROZEN — T1 Addendum 1

`t1_forbidden_G_S2C1_W_A1.txt` — md5 **`735eae308aa7baec19f23da5602a2d82`**, **39 B, 4 pattern lines** (author-supplied, byte-exact as delivered, LF-terminated). One line duplicates a base-list pattern (harmless; the scan is a set union). **Effective T1 of this gate = base `20ba1e7e` ∪ A1 `735eae30` = 37 distinct patterns**, scanned on every instrument invocation and on every artifact under the D-W-7 rule (numeric patterns: hit only when glued to a letter/underscore token; digit/sign/dot glue and exponent suffixes logged, not fatal). Two of the four A1 lines are numeric (the sealed budget and wavenumber): they will appear as parsed NUMBERS in both legs' checkpoints — expected LOGGED collisions, not hits; their appearance in any instrument SOURCE is a hit and a halt.

## 4. DECLARED — the CC checkpoint

CC leg executed EXTERNALLY by the author's direction before this addendum existed. Declared CC checkpoint md5: **`97f26c04f982b1cc1694f4a47bdce882`** (file name, byte size, branch, and commit NOT declared). This hash is the C-W identity anchor for the CC side. **The file itself is not in the chat workspace at the time of this addendum** — see D-W-10 and the re-lock-4 gate pattern (§7 gate 7: the CC checkpoint must be PRESENT AND HASHED in the chat workspace before comparison). Recovery attempt from the repository is logged in the closure log.

## 5. Deviations and honesty items logged AT DELIVERY (pre-instrument, pre-read)

- **H-W-2 (chat blindness burned at delivery).** The sealed row was delivered IN THE CLEAR inside the directive body (not as an armored file), so the chat leg read the anchor values before the chat instrument was written. Consequence (the G-POLY1 H-16 → E3-5(a) precedent): **the CC read is the verdict read of record for the CLASS (E-W-5(a) already elected); the chat read is a POST-EXPOSURE re-run** — its value is reproduction on an independent implementation plus the lexer/edge cross-check, not blind concurrence. The chat instrument is nevertheless written values-blind by construction (reads only the sealed file; contains no anchor string; T1 self-grep base ∪ A1 at every invocation) and its synthetic suites use values disjoint from the sealed ones.
- **D-W-8 (P-4.b not performed on the author→chat delivery).** Quarantined content travelled unarmored to the chat leg. P-4.b/P-4.c bind leg dispatches; the author→chat channel is not a leg dispatch, but the effect (exposure) is the same and is recorded as H-W-2.
- **D-W-9 (order deviation).** The CC leg executed before the in-band dispatch and the frozen comparator existed. The dispatch is built after the fact as the canonical package (for the record, for any S9 re-run, and for the return manifest); the comparator is frozen BEFORE the chat emission only — the "frozen before either emission" property holds on the chat side, not the CC side. Not fold-blocking; disclosed.
- **D-W-10 (CC checkpoint absent).** Hash declared, file absent; comparison C-W-1..6 cannot execute on a hash — a comparator compares VALUES. Status at addendum: OUTSTANDING pending the file (or its recovery from the repository), the D-S2C1-1 pattern.
- **Q-W-1 (query, recorded not acted on; R-B class, post-parse):** the sealed row binds a wavenumber field to a named source; the instrument reads the sealed text as dispositive (the G-CI1 rule) and does not re-derive k from the source's own emission. Any consistency question between the stated k and the named source's radiation wavenumber is the author's to answer in a sealed-file revision (which would be a new sealed md5 + a new addendum), never the instrument's to correct.

## 6. Gate status after this addendum (lock record §7)

1 sealed file — **GREEN** (`8c7d59f6`, census 1/disp). 2 T1-A1 — **GREEN** (`735eae30`). 3 JSON verified — **GREEN**. 4 chat instrument + suites — proceeds now (post-exposure, H-W-2). 5 comparator frozen pre-chat-emission — proceeds now (D-W-9). 6 dispatch — built now, after the fact (D-W-9); P-4/P-4.b/P-4.c honored in construction. 7 CC-blind-first read — **executed externally**, hash `97f26c04…` declared, file absent (D-W-10). 8 chat read + comparison — chat read proceeds; comparison contingent on the CC file.

Elections E-W-1..7 and defaults unchanged. No fold authorized by this addendum.
<<<END G_S2C1_W_LOCK_RECORD_ADDENDUM_1.md>>>

<<<BEGIN t1_forbidden_G_S2C1_W.txt>>>
# t1_forbidden_G_S2C1_W.txt — T1 forbidden-string list, Gate G-S2C1-W
# FROZEN September 8, 2026 under election E-W-4 (freeze WITHOUT the D-W-2 merge; 8cd89b9a / 653a0b74 unrecovered).
# Convention (G-BKZ32 H-2): lines beginning with '#' are documentation, NOT patterns. Every other non-empty line is
# one literal, case-sensitive substring pattern. Scanner: pattern-lines only; instruments carry patterns split-string.
# Numeric rule D-W-7 (contextual): a bare-numeric pattern counts as a hit only when glued to a unit/identifier token;
# machine-epsilon / exponent-formatting collisions are logged, not fatal. Non-numeric patterns are unconditional.
# Exemptions (justified, as at G-POLY1): the sealed anchor file itself; this list file; T1 Addendum 1.
# T1 ADDENDUM 1 (T1-A1): the author appends the anchor-specific identifiers and bound digit strings of the sealed
# file at sealed delivery (E-W-4(i)); frozen with its own md5; the instrument scans base ∪ T1-A1.
#
# --- base set (recovered byte-exact from g_poly1_phase3_mapper_v5.py 2c5ca7a4, lines 10-11 + rb_mask T1SUB) ---
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
# --- identifier-class additions (S2-side dispersion / speed-offset anchor literature; no numeric bounds) ---
GWTC
Virgo
KAGRA
LVK
LVC
graviton
Graviton
lambda_g
λ_g
A_alpha
A_α
Mirshekari
Yunes
Kostelecky
Kostelecký
Mewes
GRB
gamma-ray
eV/c
Abbott
Tests of GR
# --- G-POLY1 sealed reference strings (ledger-disclosed at V4.76; the G-POLY1 sealed file is NOT re-opened) ---
1.234271032596547e24
2.095845021951682e-6
<<<END t1_forbidden_G_S2C1_W.txt>>>

<<<BEGIN t1_forbidden_G_S2C1_W_A1.txt>>>
UFNSIEIxOTEzKzE2ClRlc3RzIG9mIEdSCjguNTdlLTcKMC4wMDIK
<<<END t1_forbidden_G_S2C1_W_A1.txt>>>

<<<BEGIN pinned_inputs_G_S2C1_W.json>>>
ewogImdhdGUiOiAiRy1TMkMxLVciLAogImFydGlmYWN0IjogInBpbm5lZF9pbnB1dHNfR19TMkMxX1cuanNvbiIsCiAiZGF0ZSI6ICIyMDI2LTA5LTA4IiwKICJzdGF0dXMiOiAiUElOTkVEIGZvciBhdXRob3IgdmVyaWZpY2F0aW9uIChwcmUtUGhhc2UtMCBnYXRlKTsgYW55IGNvcnJlY3Rpb24gLT4gdjIgKyBsb2NrLXJlY29yZCBhZGRlbmR1bTsgbWVtbyB1bnRvdWNoZWQiLAogInByb3ZlbmFuY2UiOiB7CiAgImxlZGdlcl9iYXNlIjogewogICAiZmlsZSI6ICJTUVRfTWFzdGVyX0xlZGdlcl92NF84MF9DQU5PTklDQUwubWQiLAogICAibWQ1IjogImEyOGU5YjQwNjE2ZWU5YjU3OThlOWE1YmUwMjdjMWQ5IiwKICAgImJ5dGVzIjogMTUxNDE0NAogIH0sCiAgInN0YWdpbmdfbWVtbyI6IHsKICAgImZpbGUiOiAic3RhZ2luZ19tZW1vX0dfUzJDMV9XLm1kIiwKICAgIm1kNSI6ICIxZWJiNmE4MmZjYjI0ZTIwN2IxNjRhNjU0ZWI5NGRkMSIsCiAgICJieXRlcyI6IDMyMjE5LAogICAic3RhdHVzIjogIkxPQ0tFRCIKICB9LAogICJ0MV9saXN0IjogewogICAiZmlsZSI6ICJ0MV9mb3JiaWRkZW5fR19TMkMxX1cudHh0IiwKICAgIm1kNSI6ICIyMGJhMWU3ZWFiNWEzYmJmZmU1MTBiNDg0MGVkYmM1NyIsCiAgICJieXRlcyI6IDE1NjAsCiAgICJwYXR0ZXJuX2xpbmVzIjogMzQsCiAgICJzdGF0dXMiOiAiRlJPWkVOICh3aXRob3V0IEQtVy0yIG1lcmdlKSIKICB9LAogICJwaGFzZTNfbWFjaGluZXJ5IjogewogICAicmVwbyI6ICJnaXRodWIuY29tL2dpZmdhZjAvZ2lmZ2FmMC5naXRodWIuaW8iLAogICAiYnJhbmNoIjogImNsYXVkZS9uZXctc2Vzc2lvbi1lMXU5MXAiLAogICAiY29tbWl0IjogImRkODEzNjQ2ZWQxMTJmNjMwODE2ZWUyNjBhZTBiZGQwOTZlMmI0MTciLAogICAiZGlyIjogImdwb2x5MV9nYXRlL3BoYXNlMy8iLAogICAibWFuaWZlc3RfY2hlY2siOiAiMTMvMTMgT0siCiAgfSwKICAiZ3BvbHkxX2JsaW5kX2xlZ19jaGVja3BvaW50IjogewogICAiZmlsZSI6ICJwb2x5MV9waGFzZTNfY2MuanNvbiIsCiAgICJtZDUiOiAiMjA2NGJkN2I0ZWQ0ZjdiMmI0ZTA5YmFmZGMwY2Y4NWEiLAogICAiYnl0ZXMiOiAxMTgwOCwKICAgIm1hcHBlcl9zb3VyY2VfbWQ1IjogImYxY2Q5ZGU1NDRiMTM3OGRhMmNmZWEyMTFkYjZlYjUyIiwKICAgImdhdGVfY2xhc3MiOiAiUC0yIgogIH0sCiAgImdzMmMxX3NvdXJjZXMiOiB7CiAgICJzZWN0aW9uIjogIsKnMi45MS5PIChWNC44MCkiLAogICAiY2hhdF9QMV9sYWRkZXIiOiAiNWVlMTUyZmMiLAogICAiY2hhdF9BMl9ldmFsIjogIjc3ZmVhNjVmIiwKICAgImNoYXRfUDJfcGhhc2UzIjogIjQ4OTI3YjlhIiwKICAgImNoYXRfUDJBX2V2YWwiOiAiNTZiMTdkOTMiLAogICAiY2Nfc2luZ2xlX2NyeXN0YWwiOiAiZ3NtaXlhQGNkNTFhMDAiLAogICAiY2NfYWdncmVnYXRlIjogIjN4Z2IyYkBkZWJjZTE1IiwKICAgImNvbXBhcmF0b3JfUDIiOiAiYWE4ODdlNmMgKDY5LzY5IGJvdGggc2lkZXMpIiwKICAgIm5vdGUiOiAiY2hhdCBQMiBjaGVja3BvaW50IGJ5dGVzIG5vdCBpbiBwcm9qZWN0IGtub3dsZWRnZSAoRC1XLTEpOyB2YWx1ZXMgcGlubmVkIGZyb20gdGhlIFY0LjgwIGNhbm9uaWNhbCB0ZXh0IgogIH0KIH0sCiAiYXJtX21hcCI6IFsKICB7CiAgICJtYXBwZXJfbGFiZWwiOiAiaGV4OnN0ZXAiLAogICAiZ3MyYzFfbGFiZWwiOiAic3RlcF9oZXgiCiAgfSwKICB7CiAgICJtYXBwZXJfbGFiZWwiOiAiaGV4OmdlbTgiLAogICAiZ3MyYzFfbGFiZWwiOiAiZ2VtOF9oZXgiCiAgfSwKICB7CiAgICJtYXBwZXJfbGFiZWwiOiAiY3ViaWM6c3RlcCIsCiAgICJnczJjMV9sYWJlbCI6ICJzdGVwX2N1YmljIgogIH0sCiAgewogICAibWFwcGVyX2xhYmVsIjogImN1YmljOmdlbTgiLAogICAiZ3MyYzFfbGFiZWwiOiAiZ2VtOF9jdWJpYyIKICB9CiBdLAogImFybV9tYXBfcnVsZSI6ICJpbnN0cnVtZW50IGFzc2VydHMgcGFpcmluZyBCWSBOQU1FLCBuZXZlciBieSBpbmRleCAoSC1TMkMtNyBzd2FwIGNsYXNzKSIsCiAiYTJfTF9sYXR0aWNlIjogewogICJzdGF0ZSI6IHsKICAgImtlcm5lbCI6ICJnZW04IFU9MjAqZXhwKC1yXjgpIiwKICAgImFfc3Rhcl9zdWJzdHJhdGUiOiAxLjQ2MDU5LAogICAibXUiOiA1My4yMjUsCiAgICJyaG9fbWVhbiI6IDAuOTk5OTg4CiAgfSwKICAiY19UX3N1YnN0cmF0ZSI6IHsKICAgImNoYXQiOiA1LjA0ODIsCiAgICJjYyI6IDUuMDQ4MjQKICB9LAogICJjaGF0IjogewogICAiR0siOiAtMC4wMTI3OTQsCiAgICJHTSI6IC0wLjAxOTkzMwogIH0sCiAgImNjIjogewogICAiR0siOiAtMC4wMTMyNCwKICAgIkdNIjogLTAuMDIwNjMKICB9LAogICJjaV9yZWwiOiAwLjAzNSwKICAiYTRfTCI6ICJVTlJFU09MVkVEIOKAlCBFWENMVURFRCAoRC1XLTMpIiwKICAiZWxlY3Rpb25fRV9XXzIiOiAiR0sgZm9yIHRoZSB3aW5kb3cgZWRnZTsgR00gZm9yIHRoZSBGQUlMLUwgcm9idXN0bmVzcyBhcm0iLAogICJlbGVjdGlvbl9FX1dfMyI6ICJlYWNoIGxlZyB1c2VzIGl0cyBvd24gY29sdW1uOyBjb21wYXJhdG9yIGNhcnJpZXMgY2lfcmVsIG9uIGV2ZXJ5IEZfTC1kZXBlbmRlbnQgcXVhbnRpdHkiCiB9LAogImEyX2FnZ19ncmFpbiI6IHsKICAiaGV4OnN0ZXAiOiAtMC4wMTgzNDc2NiwKICAiaGV4OmdlbTgiOiAtMC4wMjU5MzM2OSwKICAiY3ViaWM6c3RlcCI6IC0wLjAyODUzNzQ3LAogICJjdWJpYzpnZW04IjogLTAuMDM5NzEzOTgsCiAgInR3b19sZWdfYWdyZWVtZW50IjogMy40ZS0xMywKICAiZGVmaW5pdGlvbiI6ICJQMi1BIGFuYWx5dGljIHNlY29uZC1vcmRlciBCb3JuIHJlYWwgcGFydCBEMiAowqcyLjkxLk8pIgogfSwKICJhNF9hZ2dfZ3JhaW5fZGlhZ25vc3RpYyI6IHsKICAiaGV4OnN0ZXAiOiAwLjA2OTUsCiAgImhleDpnZW04IjogMC4wOTksCiAgImN1YmljOnN0ZXAiOiAwLjEwNjgsCiAgImN1YmljOmdlbTgiOiAwLjE0OTMsCiAgInR3b19sZWdfYWdyZWVtZW50X3JlbCI6IDAuMDA1LAogICJyb2xlIjogImRyZXNzaW5nIGRpYWdub3N0aWMgb25seSAoRS1XLTYoYSkpIgogfSwKICJEMF9zdGF0aWNfYm9ybl9zaGlmdCI6IHsKICAiaGV4OnN0ZXAiOiAtMC4wMjA1LAogICJoZXg6Z2VtOCI6IC0wLjAyODksCiAgImN1YmljOnN0ZXAiOiAtMC4wMzE1LAogICJjdWJpYzpnZW04IjogLTAuMDQzNywKICAicm9sZSI6ICJyZXBvcnQtb25seSIKIH0sCiAiUV9UX2EiOiB7CiAgImhleDpzdGVwIjogMC4wMzUxOTA3NCwKICAiaGV4OmdlbTgiOiAwLjA1MDAyMDU1LAogICJjdWJpYzpzdGVwIjogMC4wNTQwNzc2MywKICAiY3ViaWM6Z2VtOCI6IDAuMDc1NDk0MwogfSwKICJRX1RfZF9ydWxlIjogIlFfVF9hIC8gOCAobWFwcGVyIHY1IGNvbnN0YW50KSIsCiAiczEiOiB7CiAgImhleDpzdGVwIjogMC4xNTE1MDgwMjIsCiAgImhleDpnZW04IjogMC4xODE1Njk0NDcsCiAgImN1YmljOnN0ZXAiOiAwLjIzMzM0ODkwNCwKICAiY3ViaWM6Z2VtOCI6IDAuMjg0MjMxNTA4CiB9LAogInRpZV9pbl9yZXBvcnRfb25seSI6IHsKICAiYTJfYWdnX292ZXJfUV9UX2EiOiAtMC41MiwKICAic3ByZWFkX3JlbCI6IDAuMDA5LAogICJyb2xlIjogIkYtVy1QSU4gY29uc2lzdGVuY3ksIG5vbi12ZXJkaWN0IgogfSwKICJncG9seTFfcGlubmVkX2VkZ2VzX20iOiB7CiAgImhleDpzdGVwIjogMi4xMjEzMTMyMTAwMTMwMDY4LAogICJoZXg6Z2VtOCI6IDEuODg2Njc5NDA0ODM0NjA4NSwKICAiY3ViaWM6c3RlcCI6IDEuODM4MjY2MTA1Mjg5OTY3LAogICJjdWJpYzpnZW04IjogMS42NDQ3ODY1MzUxOTk1MzY1CiB9LAogImdwb2x5MV9waW5uZWRfY2xhc3MiOiB7CiAgImhleDpzdGVwIjogIlAtMiIsCiAgImhleDpnZW04IjogIlAtMiIsCiAgImN1YmljOnN0ZXAiOiAiUC0yIiwKICAiY3ViaWM6Z2VtOCI6ICJQLTIiCiB9LAogImdwb2x5MV9XX3VuaW9uX3VwcGVyX20iOiAyLjEyMTMxMzIxMDAxMzAwNjgsCiAiZ3BvbHkxX3J1bGUiOiAiZWRnZXMgZW50ZXIgYXMgUElOTkVEIE5VTUJFUlM7IHRoZSBHLVBPTFkxIHNlYWxlZCBmaWxlIGlzIE5PVCByZS1vcGVuZWQgKEVHLTMsIEQtVy0wKSIsCiAiYV9waHlzX2NoYWluX0VfV18xYSI6IHsKICAieGlfZGVjbGFyZWQiOiAibF9QIChHLVNDQUxFMSByZWFkaW5nIChhKSkiLAogICJsX1BfbSI6IDEuNjE2MjU1ZS0zNSwKICAibF9QX3NvdXJjZSI6ICJDT0RBVEEgMjAxOCIsCiAgIkNfcmF0aW9feGlfb3Zlcl9hIjogewogICAibG8iOiAwLjAyMTMsCiAgICJoaSI6IDAuMDg1MSwKICAgInNvdXJjZSI6ICJHLUMxIGNsYXNzLShiKSBzd2VlcCByYW5nZSAoYSBrZXJuZWwtY2xhc3Mga25vYiwgY2F2ZWF0IGluaGVyaXRlZCkiCiAgfSwKICAiYV9waHlzX20iOiB7CiAgICJsbyI6IDEuODk5MjQyMDY4MTU1MTExOGUtMzQsCiAgICJoaSI6IDcuNTg4MDUxNjQzMTkyNDg5ZS0zNCwKICAgImZvcm11bGEiOiAiYV9waHlzID0gbF9QIC8gQyIKICB9LAogICJydWxlIjogIndpbmRvdyBlZGdlIHVzZXMgYV9waHlzLmxvIChjb25zZXJ2YXRpdmUpOyBGQUlMLUwgZGVjbGFyZWQgb25seSBpZiBpdCBmaXJlcyBhdCBhX3BoeXMubG8gQU5EIHVuZGVyIHgxMCBidWRnZXQgcmVsYXhhdGlvbiAoRUctOSk7IGFfcGh5cy5oaSBzZXJpYWxpemVkIGFzIHJvYnVzdG5lc3MgYXJtIgogfSwKICJjb25zdGFudHMiOiB7CiAgIktEX0NMSVAiOiAwLjMsCiAgIk5fTUlOIjogMTAuMCwKICAiREVMVEE0X1RIUkVTSE9MRCI6IDAuMSwKICAiRlBfVE9MX1JFTCI6IDFlLTE1LAogICJGUF9NQVhfSVRFUiI6IDIwMCwKICAiY19xIjogewogICAicGhhc2UiOiAxLAogICAiZ3JvdXAiOiAzCiAgfSwKICAiYmFuZF9ydWxlIjogImV2YWx1YXRlIGF0IHVwcGVyIGJhbmQgZWRnZSBrMjsgZnVsbCBzd2VlcCBzZXJpYWxpemVkIChELVctNikiLAogICJzaWxlbnRfdGV4dF9xX2RlZmF1bHQiOiB7CiAgICJhcnJpdmFsX3RpbWVfY2xhc3MiOiAiZ3JvdXAiLAogICAiY29oZXJlbmNlX2NsYXNzIjogInBoYXNlIgogIH0sCiAgIm9vbV9mYWN0b3JzIjogWwogICAxMC4wLAogICAwLjEKICBdLAogICJjb21wYXJhdG9yX3JlbF90b2wiOiAxZS0wNiwKICAicGluX3JlbF90b2wiOiAxZS0xMgogfSwKICJlbGVjdGlvbnNfVDMiOiB7CiAgIkUtVy0xIjogIihhKSIsCiAgIkUtVy0yIjogIihhKSIsCiAgIkUtVy0zIjogIihhKSIsCiAgIkUtVy00IjogIihpKSBhdXRob3Itc3VwcGxpZWQgc2VhbGVkIGZpbGU7IFQxIGZyb3plbiB3aXRob3V0IEQtVy0yIG1lcmdlIiwKICAiRS1XLTUiOiAiKGEpIENDLUJMSU5ELUZJUlNUIiwKICAiRS1XLTYiOiAiKGEpIEJvcm4gYTItb25seSBvZiByZWNvcmQ7IGRyZXNzZWQgcmVwb3J0ZWQiLAogICJFLVctNyI6ICIoYSkgYmFua2VkIGFsb25nc2lkZSBzdXNwZW5kZWQgV191bmlvbjsgbm8gcmVpbnN0YXRlbWVudCIKIH0sCiAiZGVmYXVsdHNfcmF0aWZpZWQiOiBbCiAgIkQtVy0xIiwKICAiRC1XLTQiLAogICJELVctNSIsCiAgIkQtVy02IiwKICAiRC1XLTciCiBdLAogImV4Y2x1ZGVkIjogWwogICJhNF9MICh1bnJlc29sdmVkKSIsCiAgImEyX0wgbG9uZ2l0dWRpbmFsIHF1YXJ0ZXQgKG5vdCB0aGUgUzIgY2hhbm5lbCkiLAogICJnZW00L2dlbTMga2VybmVsIHN1Yi1hbm5vdGF0aW9ucyAobm90IHJ1biBhdCBHLVMyQzEpIgogXSwKICJub3RfaW5fdGhpc19maWxlIjogIm5vIGFuY2hvciwgbm8gYnVkZ2V0LCBubyB3YXZlbnVtYmVyLCBubyBjb21wYXJpc29uIOKAlCB0aGUgc2VhbGVkIGZpbGUgaXMgYXV0aG9yLXN1cHBsaWVkIGFuZCBvcGVuZWQgb25seSBieSB0aGUgbWFwcGVyIHBoYXNlIgp9
<<<END pinned_inputs_G_S2C1_W.json>>>

<<<BEGIN anchors_G_S2C1_W_SEALED.md>>>
YGRpc3BgIHwgQS1ESVNQLTEgfCBQU1IgQjE5MTMrMTYgfCBncm91cCB8IEIgPSAwLjAwMiB8IGsgPSA4LjU3ZS03IC9tIHwgQ2F2ZWF0OiBUZXN0cyBvZiBHUiBvcmJpdGFsIGRlY2F5IGFncmVlbWVudDsgYmluZGluZyBvbiBTMiBjYXJyaWVyIHNwZWVkLW9mZnNldCB8Cg==
<<<END anchors_G_S2C1_W_SEALED.md>>>

<<<BEGIN g_s2c1w_mapper_v6.py>>>
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJnX3MyYzF3X21hcHBlcl92Ni5weSDigJQgR2F0ZSBHLVMyQzEtVyBjaGF0IGluc3RydW1lbnQgKHY2LjEgPSBHLVBPTFkxIG1hcHBlciB2NSBsaW5lYWdlICsgdGhlIGBkaXNwYCBhbmNob3Iga2luZDsgSC1XLTQgdHdvLXBhc3MgbWFza2VyKS4KCkxpbmVhZ2U6IGdfcG9seTFfcGhhc2UzX21hcHBlcl92NS5weSAyYzVjYTdhNDcwNDJjYzk5MjliODkxNDUwZjg1NWM3ZSAocmVjb3ZlcmVkIGNsYXVkZS9uZXctc2Vzc2lvbi1lMXU5MXAgQCBkZDgxMzY0NikuCk1lbW86ICAgIHN0YWdpbmdfbWVtb19HX1MyQzFfVy5tZCAxZWJiNmE4MmZjYjI0ZTIwN2IxNjRhNjU0ZWI5NGRkMSAoTE9DS0VEKSDigJQgdGhpcyBmaWxlIGltcGxlbWVudHMgbWVtbyDCpzMuMy0zLjcsIMKnNCwgwqc1LCDCpzcuCkxvY2s6ICAgIEdfUzJDMV9XX0xPQ0tfUkVDT1JELm1kIDVmOTYzZWQ4ZDdlZmY5ZjgwM2RhNWMxZWVhMmY4NDFhOyBBZGRlbmR1bSAxIGRlY2xhcmVzIHRoZSBzZWFsZWQgbWQ1IGFuZCBUMS1BMSBtZDUgYmVsb3cuCgpPcmRlciBvZiBvcGVyYXRpb25zIChldmVyeSBpbnZvY2F0aW9uKTogVDEgc2VsZi1ncmVwIG9mIHRoaXMgc291cmNlIChiYXNlIOKIqiBBMSkgLT4gcGlubmVkLWlucHV0cyBnYXRlIChGLVctUElOKSAtPgpwcmUtcmVhZCBzdWl0ZXMgKHN5bnRoZXRpYyB2YWx1ZXMsIGRpc2pvaW50IGZyb20gdGhlIHNlYWxlZCBmaWxlKSAtPiBbUkVBRCBvbmx5XSBzZWFsZWQgc2luZ2xlIG9wZW4gKG1kNSArIGNlbnN1cyArIHNlcGFyYXRvcgpndWFyZCkgLT4gcGVyLWFybSBlZGdlcyAtPiB1bmlvbiAtPiBwcmUtY29tcGFyaXNvbiBoYXNoIC0+IGNvbXBhcmlzb24gTEFTVCAtPiBtYXNrZWQgY2hlY2twb2ludCAtPiBjaGVja3BvaW50IFQxIHNjYW4uClRoZSBpbnN0cnVtZW50IGhvbGRzIE5PIGFuY2hvciB2YWx1ZS4gSXQgYmluZHMgc2VhbGVkIGZpZWxkcyBieSBOQU1FRCBLRVkgb25seS4gQ29tcGFyaXNvbiB2YWx1ZXMgKHRoZSBwaW5uZWQgV191bmlvbiBlZGdlKQphcmUgcmVhZCBieSB0aGUgY29tcGFyaXNvbiBzdGVwIGFsb25lLgoiIiIKaW1wb3J0IG9zLCBzeXMsIHJlLCBqc29uLCBoYXNobGliLCBtYXRoCgpIRVJFID0gb3MucGF0aC5kaXJuYW1lKG9zLnBhdGguYWJzcGF0aChfX2ZpbGVfXykpCkxFRyA9IG9zLmVudmlyb24uZ2V0KCdHUzJDMVdfTEVHJywgJ2NoYXQnKQpSRUFEID0gb3MuZW52aXJvbi5nZXQoJ0dTMkMxV19SRUFEJywgJzAnKSA9PSAnMScKT1VURElSID0gb3MuZW52aXJvbi5nZXQoJ0dTMkMxV19PVVQnLCBIRVJFKQpDS1BBVEggPSBvcy5wYXRoLmpvaW4oT1VURElSLCBmJ2dfczJjMXdfcGhhc2UzX3tMRUd9Lmpzb24nKQoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIGRlY2xhcmVkIGhhc2hlcyAobG9jayByZWNvcmQgKyBhZGRlbmR1bSAxKQpUMV9CQVNFID0gKCd0MV9mb3JiaWRkZW5fR19TMkMxX1cudHh0JywgJzIwYmExZTdlYWI1YTNiYmZmZTUxMGI0ODQwZWRiYzU3JykKVDFfQTEgPSAoJ3QxX2ZvcmJpZGRlbl9HX1MyQzFfV19BMS50eHQnLCAnNzM1ZWFlMzA4YWE3YmFlYzE5ZjIzZGE1NjAyYTJkODInKQpQSU5ORUQgPSAoJ3Bpbm5lZF9pbnB1dHNfR19TMkMxX1cuanNvbicsICdkMWVkYzY5YjE2ZGZkMGI3MjhhNDhjZDgzODliMzIyYicpClNFQUxFRCA9ICgnYW5jaG9yc19HX1MyQzFfV19TRUFMRUQubWQnLCAnOGM3ZDU5ZjY0MDU3ZTM3MmQ3YjFmZjc2MDY2N2E3YzInKQpTRUFMRURfQ0VOU1VTID0geydyb3dzJzogMSwgJ3Blcl9jbGFzcyc6IHsnZGlzcCc6IDF9LCAnZmllbGRzJzogOH0KR1BPTFkxX0NDX0NLUFQgPSAoJ3BvbHkxX3BoYXNlM19jYy5qc29uJywgJzIwNjRiZDdiNGVkNGY3YjJiNGUwOWJhZmRjMGNmODVhJykgICAjIG9wdGlvbmFsIHBpbiBjcm9zcy1jaGVjayBpZiBwcmVzZW50CgpkZWYgbWQ1ZihwYXRoKToKICAgIHJldHVybiBoYXNobGliLm1kNShvcGVuKHBhdGgsICdyYicpLnJlYWQoKSkuaGV4ZGlnZXN0KCkKCmRlZiBmaW5kKG5hbWUpOgogICAgZm9yIGQgaW4gKEhFUkUsIE9VVERJUiwgb3MucGF0aC5qb2luKEhFUkUsICcuLicsICdyZWNvdmVyJywgJ3BoYXNlMycpLCBvcy5wYXRoLmpvaW4oSEVSRSwgJ2VtYmVkcycpKToKICAgICAgICBwID0gb3MucGF0aC5qb2luKGQsIG5hbWUpCiAgICAgICAgaWYgb3MucGF0aC5leGlzdHMocCk6CiAgICAgICAgICAgIHJldHVybiBwCiAgICByZXR1cm4gTm9uZQoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIFQxIG1hY2hpbmVyeSAobWVtbyDCpzYuNCwgRC1XLTcpCmRlZiB0MV9sb2FkKCk6CiAgICBwYXRzID0gW10KICAgIGZvciBuYW1lLCB3YW50IGluIChUMV9CQVNFLCBUMV9BMSk6CiAgICAgICAgcCA9IGZpbmQobmFtZSkKICAgICAgICBhc3NlcnQgcCBpcyBub3QgTm9uZSwgZidUMSBsaXN0IG1pc3Npbmc6IHtuYW1lfScKICAgICAgICBnb3QgPSBtZDVmKHApCiAgICAgICAgYXNzZXJ0IGdvdCA9PSB3YW50LCBmJ1QxIExJU1QgTUQ1IE1JU01BVENIIHtuYW1lfToge2dvdH0nCiAgICAgICAgcGF0cyArPSBbbC5yc3RyaXAoJ1xuJykgZm9yIGwgaW4gb3BlbihwLCBlbmNvZGluZz0ndXRmLTgnKSBpZiBsLnN0cmlwKCkgYW5kIG5vdCBsLnN0YXJ0c3dpdGgoJyMnKV0KICAgIHNlZW4sIG91dCA9IHNldCgpLCBbXQogICAgZm9yIHggaW4gcGF0czoKICAgICAgICBpZiB4IG5vdCBpbiBzZWVuOgogICAgICAgICAgICBzZWVuLmFkZCh4KTsgb3V0LmFwcGVuZCh4KQogICAgcmV0dXJuIG91dAoKZGVmIHQxX3NjYW4ocGF0cywgdGV4dCk6CiAgICAiIiJSZXR1cm5zIChoaXRzLCBsb2dnZWQpLiBOb24tbnVtZXJpYyBwYXR0ZXJucyB1bmNvbmRpdGlvbmFsOyBudW1lcmljIHBhdHRlcm5zIGhpdCBvbmx5IHdoZW4gZ2x1ZWQgdG8gW0EtWmEtel9dLiIiIgogICAgaGl0cywgbG9nZ2VkID0gW10sIFtdCiAgICBmb3IgaSwgcCBpbiBlbnVtZXJhdGUocGF0cyk6CiAgICAgICAgbnVtZXJpYyA9IHJlLmZ1bGxtYXRjaChyJ1swLTldWzAtOS5lRStcLV0qJywgcCkgaXMgbm90IE5vbmUKICAgICAgICBmb3IgbSBpbiByZS5maW5kaXRlcihyZS5lc2NhcGUocCksIHRleHQpOgogICAgICAgICAgICBiID0gdGV4dFttLnN0YXJ0KCkgLSAxXSBpZiBtLnN0YXJ0KCkgPiAwIGVsc2UgJycKICAgICAgICAgICAgYSA9IHRleHRbbS5lbmQoKV0gaWYgbS5lbmQoKSA8IGxlbih0ZXh0KSBlbHNlICcnCiAgICAgICAgICAgIGEyID0gdGV4dFttLmVuZCgpICsgMV0gaWYgbS5lbmQoKSArIDEgPCBsZW4odGV4dCkgZWxzZSAnJwogICAgICAgICAgICBpZiBudW1lcmljOgogICAgICAgICAgICAgICAgZ2IgPSBib29sKHJlLmZ1bGxtYXRjaChyJ1tBLVphLXpfXScsIGIgb3IgJyAnKSkKICAgICAgICAgICAgICAgIGV4cG8gPSBhIGluICgnZScsICdFJykgYW5kIGJvb2wocmUuZnVsbG1hdGNoKHInWzAtOStcLV0nLCBhMiBvciAnICcpKQogICAgICAgICAgICAgICAgZ2EgPSBib29sKHJlLmZ1bGxtYXRjaChyJ1tBLVphLXpfXScsIGEgb3IgJyAnKSkgYW5kIG5vdCBleHBvCiAgICAgICAgICAgICAgICAoaGl0cyBpZiAoZ2Igb3IgZ2EpIGVsc2UgbG9nZ2VkKS5hcHBlbmQoaSkKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIGhpdHMuYXBwZW5kKGkpCiAgICByZXR1cm4gaGl0cywgbG9nZ2VkCgpQQVRTID0gdDFfbG9hZCgpCl9zcmMgPSBvcGVuKG9zLnBhdGguYWJzcGF0aChfX2ZpbGVfXyksIGVuY29kaW5nPSd1dGYtOCcpLnJlYWQoKQpfaCwgX2wgPSB0MV9zY2FuKFBBVFMsIF9zcmMpCmFzc2VydCBub3QgX2gsIGYnVDEgSElUIChtYXBwZXIgdjYgc291cmNlKTogcGF0dGVybiBpZHgge3NvcnRlZChzZXQoX2gpKX0nCnByaW50KGYnVDEgc2VsZi1ncmVwIChtYXBwZXIgdjYgc291cmNlLCB7bGVuKFBBVFMpfSBwYXR0ZXJucyBiYXNlIOKIqiBBMSk6IFBBU1MgKGhpdHMgMCwgbG9nZ2VkIHtsZW4oX2wpfSknKQoKZGVmIHJiX21hc2socyk6CiAgICAiIiJUd28tcGFzcyBtYXNrICh2Ni4xLCBILVctNCk6ICgxKSBldmVyeSBmdWxsIFQxIHBhdHRlcm4gb2NjdXJyZW5jZSwgbG9uZ2VzdCBmaXJzdCwgY2FzZS1pbnNlbnNpdGl2ZSAtPiAnPFU+JwogICAgKG11bHRpLXRva2VuIHBhdHRlcm5zIGNhbm5vdCBzdXJ2aXZlIGEgdG9rZW4tbGV2ZWwgbWFzayk7ICgyKSBldmVyeSByZW1haW5pbmcgd2hpdGVzcGFjZSB0b2tlbiBjb250YWluaW5nIGFueSBwYXR0ZXJuIC0+ICc8VT4nLgogICAgVGhlIG1hc2tlZCB0ZXh0IGlzIHRoZW4gc2VsZi1zY2FubmVkOyBhbnkgc3Vydml2aW5nIGhpdCBpcyBhIG1hc2tlZCBhYm9ydCAoZmFpbC1jbG9zZWQpLiIiIgogICAgZm9yIHAgaW4gc29ydGVkKFBBVFMsIGtleT1sZW4sIHJldmVyc2U9VHJ1ZSk6CiAgICAgICAgcyA9IHJlLnN1YihyZS5lc2NhcGUocCksICc8VT4nLCBzLCBmbGFncz1yZS5JKQogICAgb3V0ID0gW10KICAgIGZvciB3IGluIHMuc3BsaXQoKToKICAgICAgICB3bCA9IHcubG93ZXIoKQogICAgICAgIG91dC5hcHBlbmQoJzxVPicgaWYgYW55KHAubG93ZXIoKSBpbiB3bCBmb3IgcCBpbiBQQVRTKSBlbHNlIHcpCiAgICBtID0gJyAnLmpvaW4ob3V0KQogICAgaCwgXyA9IHQxX3NjYW4oUEFUUywgbSkKICAgIGFzc2VydCBub3QgaCwgJ01BU0tJTkcgU0VMRi1TQ0FOIEZBSUxFRCcKICAgIHJldHVybiBtCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gcGlubmVkIGlucHV0cyAobWVtbyDCpzI7IEYtVy1QSU4pCkFSTVMgPSBbJ2hleDpzdGVwJywgJ2hleDpnZW04JywgJ2N1YmljOnN0ZXAnLCAnY3ViaWM6Z2VtOCddCk1FTU9fVEFCTEUgPSB7ICAgIyB0aGUgbWVtbyDCpzIgdmFsdWVzLCBoZWxkIGludGVybmFsbHk7IHRoZSBKU09OIG11c3QgYWdyZWUgdG8gMWUtMTIgcmVsIChGLVctUElOKQogICAgJ2EyX2FnZyc6IHsnaGV4OnN0ZXAnOiAtMS44MzQ3NjZlLTIsICdoZXg6Z2VtOCc6IC0yLjU5MzM2OWUtMiwgJ2N1YmljOnN0ZXAnOiAtMi44NTM3NDdlLTIsICdjdWJpYzpnZW04JzogLTMuOTcxMzk4ZS0yfSwKICAgICdhNF9hZ2cnOiB7J2hleDpzdGVwJzogMC4wNjk1LCAnaGV4OmdlbTgnOiAwLjA5OTAsICdjdWJpYzpzdGVwJzogMC4xMDY4LCAnY3ViaWM6Z2VtOCc6IDAuMTQ5M30sCiAgICAnYTJfTF9jaGF0JzogeydHSyc6IC0xLjI3OTRlLTIsICdHTSc6IC0xLjk5MzNlLTJ9LAogICAgJ2EyX0xfY2MnOiB7J0dLJzogLTEuMzI0ZS0yLCAnR00nOiAtMi4wNjNlLTJ9LAogICAgJ2dwb2x5MV9lZGdlcyc6IHsnaGV4OnN0ZXAnOiAyLjEyMTMxMzIxMDAxMzAwNjgsICdoZXg6Z2VtOCc6IDEuODg2Njc5NDA0ODM0NjA4NSwKICAgICAgICAgICAgICAgICAgICAgJ2N1YmljOnN0ZXAnOiAxLjgzODI2NjEwNTI4OTk2NywgJ2N1YmljOmdlbTgnOiAxLjY0NDc4NjUzNTE5OTUzNjV9LAogICAgJ2dwb2x5MV9XX3VuaW9uX3VwcGVyJzogMi4xMjEzMTMyMTAwMTMwMDY4LAogICAgJ2xfUF9tJzogMS42MTYyNTVlLTM1LCAnQ19sbyc6IDAuMDIxMywgJ0NfaGknOiAwLjA4NTEsCiAgICAnS0RfQ0xJUCc6IDAuMywgJ05fTUlOJzogMTAuMCwgJ0RFTFRBNF9USFJFU0hPTEQnOiAwLjEwLCAnRlBfVE9MX1JFTCc6IDFlLTE1LCAnRlBfTUFYX0lURVInOiAyMDAsCiAgICAnY19xJzogeydwaGFzZSc6IDEsICdncm91cCc6IDN9LCAnb29tX2ZhY3RvcnMnOiBbMTAuMCwgMC4xXSwgJ2NpX3JlbCc6IDAuMDM1LAp9CgpkZWYgcmVsKGEsIGIpOgogICAgcmV0dXJuIGFicyhhIC0gYikgLyBtYXgoYWJzKGIpLCAxZS0zMDApCgpkZWYgbG9hZF9waW5uZWQoKToKICAgIHAgPSBmaW5kKFBJTk5FRFswXSk7IGFzc2VydCBwIGlzIG5vdCBOb25lLCAncGlubmVkIGlucHV0cyBtaXNzaW5nJwogICAgZ290ID0gbWQ1ZihwKTsgYXNzZXJ0IGdvdCA9PSBQSU5ORURbMV0sIGYnUElOTkVEIE1ENSBNSVNNQVRDSCB7Z290fScKICAgIEogPSBqc29uLmxvYWQob3BlbihwLCBlbmNvZGluZz0ndXRmLTgnKSkKICAgIHdvcnN0ID0gMC4wCiAgICBkZWYgY2hrKHgsIHksIGxhYmVsKToKICAgICAgICBub25sb2NhbCB3b3JzdAogICAgICAgIHdvcnN0ID0gbWF4KHdvcnN0LCByZWwoeCwgeSkpOyBhc3NlcnQgcmVsKHgsIHkpIDw9IDFlLTEyLCBmJ0YtVy1QSU46IHtsYWJlbH0ge3h9IHZzIHt5fScKICAgIGZvciBhIGluIEFSTVM6CiAgICAgICAgY2hrKEpbJ2EyX2FnZ19ncmFpbiddW2FdLCBNRU1PX1RBQkxFWydhMl9hZ2cnXVthXSwgZidhMl9hZ2cge2F9JykKICAgICAgICBjaGsoSlsnYTRfYWdnX2dyYWluX2RpYWdub3N0aWMnXVthXSwgTUVNT19UQUJMRVsnYTRfYWdnJ11bYV0sIGYnYTRfYWdnIHthfScpCiAgICAgICAgY2hrKEpbJ2dwb2x5MV9waW5uZWRfZWRnZXNfbSddW2FdLCBNRU1PX1RBQkxFWydncG9seTFfZWRnZXMnXVthXSwgZidncG9seTEgZWRnZSB7YX0nKQogICAgZm9yIGQgaW4gKCdHSycsICdHTScpOgogICAgICAgIGNoayhKWydhMl9MX2xhdHRpY2UnXVsnY2hhdCddW2RdLCBNRU1PX1RBQkxFWydhMl9MX2NoYXQnXVtkXSwgZidhMl9MIGNoYXQge2R9JykKICAgICAgICBjaGsoSlsnYTJfTF9sYXR0aWNlJ11bJ2NjJ11bZF0sIE1FTU9fVEFCTEVbJ2EyX0xfY2MnXVtkXSwgZidhMl9MIGNjIHtkfScpCiAgICBjaGsoSlsnZ3BvbHkxX1dfdW5pb25fdXBwZXJfbSddLCBNRU1PX1RBQkxFWydncG9seTFfV191bmlvbl91cHBlciddLCAnV191bmlvbiB1cHBlcicpCiAgICBjaCA9IEpbJ2FfcGh5c19jaGFpbl9FX1dfMWEnXQogICAgY2hrKGNoWydsX1BfbSddLCBNRU1PX1RBQkxFWydsX1BfbSddLCAnbF9QJyk7IGNoayhjaFsnQ19yYXRpb194aV9vdmVyX2EnXVsnbG8nXSwgTUVNT19UQUJMRVsnQ19sbyddLCAnQ19sbycpCiAgICBjaGsoY2hbJ0NfcmF0aW9feGlfb3Zlcl9hJ11bJ2hpJ10sIE1FTU9fVEFCTEVbJ0NfaGknXSwgJ0NfaGknKQogICAgY2hrKGNoWydhX3BoeXNfbSddWydsbyddLCBNRU1PX1RBQkxFWydsX1BfbSddIC8gTUVNT19UQUJMRVsnQ19oaSddLCAnYV9waHlzIGxvJykKICAgIGNoayhjaFsnYV9waHlzX20nXVsnaGknXSwgTUVNT19UQUJMRVsnbF9QX20nXSAvIE1FTU9fVEFCTEVbJ0NfbG8nXSwgJ2FfcGh5cyBoaScpCiAgICBLID0gSlsnY29uc3RhbnRzJ10KICAgIGZvciBrIGluICgnS0RfQ0xJUCcsICdOX01JTicsICdERUxUQTRfVEhSRVNIT0xEJywgJ0ZQX1RPTF9SRUwnKToKICAgICAgICBjaGsoS1trXSwgTUVNT19UQUJMRVtrXSwgaykKICAgIGFzc2VydCBLWydGUF9NQVhfSVRFUiddID09IE1FTU9fVEFCTEVbJ0ZQX01BWF9JVEVSJ10gYW5kIEtbJ2NfcSddID09IE1FTU9fVEFCTEVbJ2NfcSddCiAgICBhc3NlcnQgW2Zsb2F0KHgpIGZvciB4IGluIEtbJ29vbV9mYWN0b3JzJ11dID09IE1FTU9fVEFCTEVbJ29vbV9mYWN0b3JzJ10KICAgICMgb3B0aW9uYWwgYnl0ZS1sZXZlbCBwaW4gb2YgdGhlIEctUE9MWTEgZWRnZXMgYWdhaW5zdCB0aGUgcmVjb3ZlcmVkIGJsaW5kLWxlZyBjaGVja3BvaW50CiAgICBncCA9IGZpbmQoR1BPTFkxX0NDX0NLUFRbMF0pOyBwaW5fc3JjID0gJ21lbW8tdGFibGUgb25seSAoMjA2NGJkN2IgZmlsZSBub3QgcHJlc2VudCknCiAgICBpZiBncCBpcyBub3QgTm9uZSBhbmQgbWQ1ZihncCkgPT0gR1BPTFkxX0NDX0NLUFRbMV06CiAgICAgICAgY2MgPSBqc29uLmxvYWQob3BlbihncCwgZW5jb2Rpbmc9J3V0Zi04JykpCiAgICAgICAgZm9yIGEgaW4gQVJNUzoKICAgICAgICAgICAgYXNzZXJ0IGNjWydwZXJfYXJtJ11bYV1bJ1cnXVsxXSA9PSBNRU1PX1RBQkxFWydncG9seTFfZWRnZXMnXVthXSwgZidHLVBPTFkxIGVkZ2UgcGluIHthfScKICAgICAgICBhc3NlcnQgY2NbJ1dfdW5pb24nXVswXVsxXSA9PSBNRU1PX1RBQkxFWydncG9seTFfV191bmlvbl91cHBlciddCiAgICAgICAgcGluX3NyYyA9ICcyMDY0YmQ3YiBieXRlLWV4YWN0IChwZXJfYXJtIFdbMV0gaWRlbnRpY2FsKScKICAgIHJldHVybiBKLCB3b3JzdCwgcGluX3NyYwoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIHBoeXNpY3MgY29yZSAobWVtbyDCpzMuMi0zLjYpCmRlZiBhX3BoeXNfcGFpcihKKToKICAgIGNoID0gSlsnYV9waHlzX2NoYWluX0VfV18xYSddWydhX3BoeXNfbSddCiAgICByZXR1cm4gZmxvYXQoY2hbJ2xvJ10pLCBmbG9hdChjaFsnaGknXSkKCmRlZiBsYXR0aWNlX2Zsb29yKGNxLCBhMkwsIGssIGEpOgogICAgcmV0dXJuIGNxICogYWJzKGEyTCkgKiAoayAqIGEpICoqIDIKCmRlZiBib3JuX2VkZ2UoY3EsIGEyYWdnLCBCcCwgayk6CiAgICByZXR1cm4gbWF0aC5zcXJ0KEJwIC8gKGNxICogYWJzKGEyYWdnKSkpIC8gawoKZGVmIGRyZXNzZWRfZWRnZShjcSwgYTJhZ2csIGE0YWdnLCBCcCwgaywgdG9sPTFlLTE1LCBpdG1heD0yMDApOgogICAgIiIiUm9vdCBvZiBjcSoofGEyfCB4XjIgLSBhNCB4XjQpID0gQnAgaW4geCA9IGsgZCwgc2VlZGVkIGF0IHRoZSBCb3JuIHZhbHVlOyBmaXhlZC1wb2ludCB4ID0gc3FydCgoQnAvY3EgKyBhNCB4XjQpL3xhMnwpLiIiIgogICAgYTIgPSBhYnMoYTJhZ2cpOyBhNCA9IGZsb2F0KGE0YWdnKQogICAgaWYgYTQgPiAwIGFuZCBCcCAvIGNxID4gYTIgKiBhMiAvICg0LjAgKiBhNCk6CiAgICAgICAgcmV0dXJuIE5vbmUsICdOTy1ST09ULUJFWU9ORC1UVVJOT1ZFUicKICAgIHggPSBtYXRoLnNxcnQoQnAgLyAoY3EgKiBhMikpCiAgICBmb3IgXyBpbiByYW5nZShpdG1heCk6CiAgICAgICAgeG4gPSBtYXRoLnNxcnQoKEJwIC8gY3EgKyBhNCAqIHggKiogNCkgLyBhMikKICAgICAgICBpZiBhYnMoeG4gLSB4KSA8PSB0b2wgKiBtYXgoeCwgMWUtMzAwKToKICAgICAgICAgICAgcmV0dXJuIHhuIC8gaywgJ0NPTlZFUkdFRCcKICAgICAgICB4ID0geG4KICAgIHJldHVybiB4IC8gaywgJ01BWC1JVEVSJwoKZGVmIGV2YWxfZGlzcF9hcm0oSiwgYXJtLCBhbmNob3IsIEJfc2NhbGU9MS4wLCBhMkxfa2V5PSdHSycsIGFfZW5kPSdsbycsIGxlZz1MRUcpOgogICAgIiIiT25lIGFybSwgb25lIGRpc3AgYW5jaG9yLCBvbmUgYnVkZ2V0IHNjYWxlLCBvbmUgbGF0dGljZSBjb25maWd1cmF0aW9uIC0+IGVkZ2UgcmVjb3JkIChtZW1vIMKnMy40KS4iIiIKICAgIEsgPSBKWydjb25zdGFudHMnXTsgY3EgPSBLWydjX3EnXVthbmNob3JbJ3EnXV07IGtkX2NsaXAgPSBLWydLRF9DTElQJ10KICAgIGEyYWdnID0gSlsnYTJfYWdnX2dyYWluJ11bYXJtXTsgYTRhZ2cgPSBKWydhNF9hZ2dfZ3JhaW5fZGlhZ25vc3RpYyddW2FybV0KICAgIGEyTCA9IEpbJ2EyX0xfbGF0dGljZSddWydjaGF0JyBpZiBsZWcgPT0gJ2NoYXQnIGVsc2UgJ2NjJ11bYTJMX2tleV0KICAgIGFsbywgYWhpID0gYV9waHlzX3BhaXIoSik7IGEgPSBhbG8gaWYgYV9lbmQgPT0gJ2xvJyBlbHNlIGFoaQogICAgQiA9IGFuY2hvclsnQiddICogQl9zY2FsZTsgayA9IGFuY2hvclsnayddCiAgICBGTCA9IGxhdHRpY2VfZmxvb3IoY3EsIGEyTCwgaywgYSk7IEJwID0gQiAtIEZMCiAgICByZWMgPSB7J2FybSc6IGFybSwgJ2FuY2hvcic6IGFuY2hvclsnaWR4J10sICdxJzogYW5jaG9yWydxJ10sICdjX3EnOiBjcSwgJ0Jfc2NhbGUnOiBCX3NjYWxlLCAnYTJMX2tleSc6IGEyTF9rZXksCiAgICAgICAgICAgJ2FfZW5kJzogYV9lbmQsICdGX0wnOiBGTCwgJ0JfcHJpbWUnOiBCcCwgJ2ZhaWxfTCc6IEJwIDw9IDAuMH0KICAgIGlmIEJwIDw9IDAuMDoKICAgICAgICByZWMudXBkYXRlKHsnZWRnZV9ib3JuX20nOiBOb25lLCAndm9pZGVkJzogVHJ1ZSwgJ3ZvaWRfcmVhc29uJzogJ0ZBSUwtTCAoYnVkZ2V0IGNvbnN1bWVkIGJ5IGxhdHRpY2UgZmxvb3IpJ30pCiAgICAgICAgcmV0dXJuIHJlYwogICAgZCA9IGJvcm5fZWRnZShjcSwgYTJhZ2csIEJwLCBrKTsga2QgPSBrICogZAogICAgcmVjLnVwZGF0ZSh7J2VkZ2VfYm9ybl9tJzogZCwgJ2tkJzoga2QsICdlbnZlbG9wZV9jZWlsaW5nX20nOiBrZF9jbGlwIC8gaywgJ3ZvaWRlZCc6IGtkID4ga2RfY2xpcCwKICAgICAgICAgICAgICAgICd2b2lkX3JlYXNvbic6ICgnRi1XLUVOViBrZCA+IEtEX0NMSVAnIGlmIGtkID4ga2RfY2xpcCBlbHNlIE5vbmUpfSkKICAgIGRlbHRhNCA9IGFicyhhNGFnZykgKiBrZCAqIGtkIC8gYWJzKGEyYWdnKQogICAgZGQsIHN0YXR1cyA9IGRyZXNzZWRfZWRnZShjcSwgYTJhZ2csIGE0YWdnLCBCcCwgaywgS1snRlBfVE9MX1JFTCddLCBLWydGUF9NQVhfSVRFUiddKQogICAgcmVjLnVwZGF0ZSh7J2RlbHRhNCc6IGRlbHRhNCwgJ2RyZXNzaW5nX3NlbnNpdGl2ZSc6IGRlbHRhNCA+IEtbJ0RFTFRBNF9USFJFU0hPTEQnXSwKICAgICAgICAgICAgICAgICdlZGdlX2RyZXNzZWRfbSc6IGRkLCAnZHJlc3NlZF9zdGF0dXMnOiBzdGF0dXN9KQogICAgcmV0dXJuIHJlYwoKZGVmIGV2YWxfYXJtKEosIGFybSwgYW5jaG9ycywgbGVnPUxFRyk6CiAgICAiIiJQZXItYXJtIHdpbmRvdyAobWVtbyDCpzMuNSk6IG1pbiBvdmVyIE5PTi1WT0lERUQgZWRnZXMgb2Yge3Bpbm5lZCBHLVBPTFkxIGVkZ2UsIGRpc3AgQm9ybiBlZGdlc307IGNsYXNzOyBPT00uIiIiCiAgICBLID0gSlsnY29uc3RhbnRzJ10KICAgIG91dCA9IHsnYXJtJzogYXJtLCAncGlubmVkX2dwb2x5MV9lZGdlX20nOiBKWydncG9seTFfcGlubmVkX2VkZ2VzX20nXVthcm1dLCAnZGlzcCc6IFtdLCAncm9idXN0bmVzcyc6IFtdLCAnb29tJzoge319CiAgICBmYWlsX0xfZGVjbGFyZWQgPSBGYWxzZQogICAgZm9yIGFuIGluIGFuY2hvcnM6CiAgICAgICAgYmFzZSA9IGV2YWxfZGlzcF9hcm0oSiwgYXJtLCBhbiwgMS4wLCAnR0snLCAnbG8nLCBsZWcpICAgICAgICAgICAgICAgICAgIyB3aW5kb3cgY29uZmlndXJhdGlvbiAoRS1XLTEoYSksIEUtVy0yKGEpKQogICAgICAgIHJlbGF4ZWQgPSBldmFsX2Rpc3BfYXJtKEosIGFybSwgYW4sIEtbJ29vbV9mYWN0b3JzJ11bMF0sICdHSycsICdsbycsIGxlZykKICAgICAgICB0aWdodCA9IGV2YWxfZGlzcF9hcm0oSiwgYXJtLCBhbiwgS1snb29tX2ZhY3RvcnMnXVsxXSwgJ0dLJywgJ2xvJywgbGVnKQogICAgICAgIG91dFsnZGlzcCddLmFwcGVuZChiYXNlKTsgb3V0Wydvb20nXVthblsnaWR4J11dID0geydyZWxheGVkJzogcmVsYXhlZCwgJ3RpZ2h0ZW5lZCc6IHRpZ2h0fQogICAgICAgIGZvciBrZXksIGVuZCBpbiAoKCdHSycsICdoaScpLCAoJ0dNJywgJ2xvJyksICgnR00nLCAnaGknKSk6ICAgICAgICAgICAgICMgcm9idXN0bmVzcyBhcm1zIChyZXBvcnRlZCwgbm9uLXZlcmRpY3QpCiAgICAgICAgICAgIG91dFsncm9idXN0bmVzcyddLmFwcGVuZChldmFsX2Rpc3BfYXJtKEosIGFybSwgYW4sIDEuMCwga2V5LCBlbmQsIGxlZykpCiAgICAgICAgaWYgYmFzZVsnZmFpbF9MJ10gYW5kIHJlbGF4ZWRbJ2ZhaWxfTCddOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIyBFRy05OiBGQUlMLUwgbXVzdCBiZSBlbGVjdGlvbi1yb2J1c3QKICAgICAgICAgICAgZmFpbF9MX2RlY2xhcmVkID0gVHJ1ZQogICAgICAgIGVsaWYgYmFzZVsnZmFpbF9MJ106CiAgICAgICAgICAgIGJhc2VbJ2ZhaWxfTF9mcmFnaWxlJ10gPSBUcnVlCiAgICBlZGdlcyA9IFsob3V0WydwaW5uZWRfZ3BvbHkxX2VkZ2VfbSddLCAnR1BPTFkxLXBpbm5lZCcpXQogICAgZWRnZXMgKz0gWyhyWydlZGdlX2Jvcm5fbSddLCBmIkF7clsnYW5jaG9yJ119LWRpc3AiKSBmb3IgciBpbiBvdXRbJ2Rpc3AnXSBpZiBub3Qgclsndm9pZGVkJ11dCiAgICB1cCwgbGFiID0gbWluKGVkZ2VzLCBrZXk9bGFtYmRhIHQ6IHRbMF0pCiAgICBvdXQudXBkYXRlKHsnV191cHBlcl9tJzogdXAsICdnb3Zlcm5pbmcnOiBsYWIsICdlZGdlc19jb25zaWRlcmVkJzogZWRnZXMsCiAgICAgICAgICAgICAgICAndm9pZGVkJzogWyhmIkF7clsnYW5jaG9yJ119LWRpc3AiLCByLmdldCgndm9pZF9yZWFzb24nKSkgZm9yIHIgaW4gb3V0WydkaXNwJ10gaWYgclsndm9pZGVkJ11dfSkKICAgIGlmIGZhaWxfTF9kZWNsYXJlZDoKICAgICAgICBvdXRbJ2FybV9jbGFzcyddID0gJ0ZBSUwtTCcKICAgIGVsaWYgYWxsKHJbJ3ZvaWRlZCddIGZvciByIGluIG91dFsnZGlzcCddKSBhbmQgb3V0WydkaXNwJ106CiAgICAgICAgb3V0Wydhcm1fY2xhc3MnXSA9ICdWT0lELURJU1AnCiAgICBlbHNlOgogICAgICAgIG91dFsnYXJtX2NsYXNzJ10gPSAiUC0yJyIKICAgICMgT09NIGNsYXNzIHJvYnVzdG5lc3Mgb2YgdGhlIHdpbmRvdzogcmVjb21wdXRlIHRoZSBnb3Zlcm5pbmcgZWRnZSB1bmRlciByZWxheGVkIC8gdGlnaHRlbmVkIGJ1ZGdldHMKICAgIGRlZiB1cF91bmRlcih3aGljaCk6CiAgICAgICAgZSA9IFsob3V0WydwaW5uZWRfZ3BvbHkxX2VkZ2VfbSddLCAnR1BPTFkxLXBpbm5lZCcpXQogICAgICAgIGZvciBhbiBpbiBhbmNob3JzOgogICAgICAgICAgICByID0gb3V0Wydvb20nXVthblsnaWR4J11dW3doaWNoXQogICAgICAgICAgICBpZiBub3Qgclsndm9pZGVkJ10gYW5kIHJbJ2VkZ2VfYm9ybl9tJ10gaXMgbm90IE5vbmU6CiAgICAgICAgICAgICAgICBlLmFwcGVuZCgoclsnZWRnZV9ib3JuX20nXSwgZiJBe2FuWydpZHgnXX0tZGlzcCIpKQogICAgICAgIHJldHVybiBtaW4oZSwga2V5PWxhbWJkYSB0OiB0WzBdKQogICAgb3V0Wydvb21fcmVsYXhlZF91cHBlciddLCBvdXRbJ29vbV90aWdodGVuZWRfdXBwZXInXSA9IHVwX3VuZGVyKCdyZWxheGVkJyksIHVwX3VuZGVyKCd0aWdodGVuZWQnKQogICAgb3V0Wydvb21fcm9idXN0J10gPSAob3V0Wydvb21fcmVsYXhlZF91cHBlciddWzFdID09IGxhYikgYW5kIChvdXRbJ29vbV90aWdodGVuZWRfdXBwZXInXVsxXSA9PSBsYWIpCiAgICByZXR1cm4gb3V0CgpkZWYgdW5pb25fYW5kX2ludGVyc2VjdGlvbihwZXJfYXJtKToKICAgIHVwcyA9IHthOiBwZXJfYXJtW2FdWydXX3VwcGVyX20nXSBmb3IgYSBpbiBBUk1TfQogICAgdW1heCA9IG1heCh1cHMsIGtleT11cHMuZ2V0KTsgdW1pbiA9IG1pbih1cHMsIGtleT11cHMuZ2V0KQogICAgcmV0dXJuIHsnV191bmlvbl9wcmltZSc6IFswLjAsIHVwc1t1bWF4XV0sICd1bmlvbl9nb3Zlcm5pbmdfYXJtJzogdW1heCwgJ1dfaW50ZXJzZWN0aW9uJzogWzAuMCwgdXBzW3VtaW5dXSwKICAgICAgICAgICAgJ2ludGVyc2VjdGlvbl9nb3Zlcm5pbmdfYXJtJzogdW1pbiwgJ3Blcl9hcm1fdXBwZXInOiB1cHN9CgpkZWYgY29tcGFyaXNvbl9sYXN0KEosIHBlcl9hcm0sIHVuaSwgcHJlX2hhc2gpOgogICAgIiIiUnVucyBPTkxZIGFmdGVyIHRoZSBwcmUtY29tcGFyaXNvbiByZWNvcmQgaXMgaGFzaGVkIChtZW1vIMKnMy43LCBFRy00KS4gUmVhZHMgdGhlIHBpbm5lZCBXX3VuaW9uIGVkZ2UgaGVyZSBhbmQgbm93aGVyZSBlbHNlLiIiIgogICAgYXNzZXJ0IHByZV9oYXNoIGFuZCBsZW4ocHJlX2hhc2gpID09IDMyLCAnY29tcGFyaXNvbiBhdHRlbXB0ZWQgYmVmb3JlIHByZS1jb21wYXJpc29uIGhhc2gnCiAgICBXdXAgPSBKWydncG9seTFfV191bmlvbl91cHBlcl9tJ107IHVwID0gdW5pWydXX3VuaW9uX3ByaW1lJ11bMV07IGdhcm0gPSB1bmlbJ3VuaW9uX2dvdmVybmluZ19hcm0nXQogICAgaWYgdXAgPiBXdXAgKiAoMS4wICsgMWUtMTIpOgogICAgICAgIHJhaXNlIFJ1bnRpbWVFcnJvcignRi1XLU1PTk86IFdfdW5pb25fcHJpbWUgZXhjZWVkcyBXX3VuaW9uIOKAlCBpbnN0cnVtZW50IGRlZmVjdCwgaGFsdGluZycpCiAgICBpZiBhbnkocGVyX2FybVthXVsnYXJtX2NsYXNzJ10gPT0gJ0ZBSUwtTCcgZm9yIGEgaW4gQVJNUyk6CiAgICAgICAgY2xzID0gJ0ZBSUwtTCcKICAgIGVsaWYgcGVyX2FybVtnYXJtXVsnZ292ZXJuaW5nJ10gPT0gJ0dQT0xZMS1waW5uZWQnIGFuZCBhYnModXAgLSBXdXApIDw9IDFlLTEyICogV3VwOgogICAgICAgIGNscyA9ICdJTkVSVCcKICAgIGVsc2U6CiAgICAgICAgY2xzID0gJ1RJR0hURU5FRCcKICAgIHJvYnVzdCA9IGFsbChwZXJfYXJtW2FdWydvb21fcm9idXN0J10gZm9yIGEgaW4gQVJNUykKICAgIHJldHVybiB7J3ByZV9jb21wYXJpc29uX21kNSc6IHByZV9oYXNoLCAnV191bmlvbl9waW5uZWRfdXBwZXJfbSc6IFd1cCwgJ1dfdW5pb25fcHJpbWVfdXBwZXJfbSc6IHVwLAogICAgICAgICAgICAncmF0aW9fcHJpbWVfb3Zlcl9waW5uZWQnOiB1cCAvIFd1cCwgJ2NsYXNzJzogY2xzLCAnb29tX3JvYnVzdCc6IHJvYnVzdCwKICAgICAgICAgICAgJ3Blcl9hcm1fY2xhc3Nlcyc6IHthOiBwZXJfYXJtW2FdWydhcm1fY2xhc3MnXSBmb3IgYSBpbiBBUk1TfSwKICAgICAgICAgICAgJ3Blcl9hcm1fZ292ZXJuaW5nJzoge2E6IHBlcl9hcm1bYV1bJ2dvdmVybmluZyddIGZvciBhIGluIEFSTVN9LAogICAgICAgICAgICAncmVpbnN0YXRlbWVudCc6ICdOT05FIChFLVctNyhhKTogYmFua2VkIGFsb25nc2lkZSB0aGUgc3VzcGVuZGVkIFdfdW5pb24pJ30KCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBzZWFsZWQgZmlsZSAobWVtbyDCpzMuMywgwqc1IEVHLTIpCmNsYXNzIFJvd0RlZmVjdChFeGNlcHRpb24pOgogICAgcGFzcwoKTlVNID0gcicoWy0rXT9cZCsoPzpcLlxkKyk/KD86W2VFXVstK10/XGQrKT8pJwoKZGVmIHBhcnNlX3NlYWxlZCh0ZXh0KToKICAgIHJvd3MgPSBbbCBmb3IgbCBpbiB0ZXh0LnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICBwYXJzZWQsIGNlbnN1cyA9IFtdLCB7fQogICAgZm9yIGksIGxpbmUgaW4gZW51bWVyYXRlKHJvd3MsIDEpOgogICAgICAgIGYgPSBbeC5zdHJpcCgpIGZvciB4IGluIGxpbmUuc3BsaXQoJ3wnKV0KICAgICAgICBpZiBsZW4oZikgIT0gU0VBTEVEX0NFTlNVU1snZmllbGRzJ10gb3IgZlstMV0gIT0gJyc6CiAgICAgICAgICAgIHJhaXNlIFJvd0RlZmVjdChmJ3JvdyB7aX06IGZpZWxkIGNvdW50IHtsZW4oZil9IChzZXBhcmF0b3IgZ3VhcmQpJykKICAgICAgICBjbHMgPSBmWzBdLnN0cmlwKCdgJykubG93ZXIoKQogICAgICAgIGNlbnN1c1tjbHNdID0gY2Vuc3VzLmdldChjbHMsIDApICsgMQogICAgICAgIGlmIGNscyAhPSAnZGlzcCc6CiAgICAgICAgICAgIHJhaXNlIFJvd0RlZmVjdChmJ3JvdyB7aX06IGtpbmQge2NscyFyfSBub3QgcmVhZCBieSB2NiAoRy1QT0xZMSBraW5kcyBhcmUgcGlubmVkLCBub3QgcmUtcmVhZCknKQogICAgICAgIHEgPSBmWzNdLmxvd2VyKCkKICAgICAgICBpZiBxIG5vdCBpbiAoJ3BoYXNlJywgJ2dyb3VwJyk6CiAgICAgICAgICAgIHJhaXNlIFJvd0RlZmVjdChmJ3JvdyB7aX06IHEgZmllbGQge3Ehcn0gbm90IGluIHt7cGhhc2UsIGdyb3VwfX0nKQogICAgICAgIG1CID0gcmUuZnVsbG1hdGNoKHInQlxzKj1ccyonICsgTlVNLCBmWzRdKTsgbWsgPSByZS5mdWxsbWF0Y2gocidrXHMqPVxzKicgKyBOVU0gKyByJ1xzKi9tJywgZls1XSkKICAgICAgICBpZiBub3QgbUIgb3Igbm90IG1rOgogICAgICAgICAgICByYWlzZSBSb3dEZWZlY3QoZidyb3cge2l9OiBuYW1lZC1rZXkgYmluZGluZyBmYWlsZWQgKEI9LCBrPSAvbSknKQogICAgICAgIEIsIGsgPSBmbG9hdChtQi5ncm91cCgxKSksIGZsb2F0KG1rLmdyb3VwKDEpKQogICAgICAgIGlmIG5vdCAoQiA+IDAgYW5kIGsgPiAwKToKICAgICAgICAgICAgcmFpc2UgUm93RGVmZWN0KGYncm93IHtpfTogcG9zaXRpdml0eSAoQj17Qn0sIGs9e2t9KScpCiAgICAgICAgcGFyc2VkLmFwcGVuZCh7J2lkeCc6IGksICdjbHMnOiBjbHMsICdpZF9tYXNrZWQnOiByYl9tYXNrKGZbMV0pLCAnc291cmNlX21hc2tlZCc6IHJiX21hc2soZlsyXSksICdxJzogcSwKICAgICAgICAgICAgICAgICAgICAgICAnQic6IEIsICdrJzogaywgJ2NhdmVhdF9tYXNrZWQnOiByYl9tYXNrKGZbNl0pLCAncm93X21kNSc6IGhhc2hsaWIubWQ1KGxpbmUuZW5jb2RlKCkpLmhleGRpZ2VzdCgpfSkKICAgIGlmIGxlbihyb3dzKSAhPSBTRUFMRURfQ0VOU1VTWydyb3dzJ10gb3IgY2Vuc3VzICE9IFNFQUxFRF9DRU5TVVNbJ3Blcl9jbGFzcyddOgogICAgICAgIHJhaXNlIFJvd0RlZmVjdChmJ2NlbnN1cyB7bGVuKHJvd3MpfSByb3dzIC8ge2NlbnN1c30gdnMgZGVjbGFyZWQge1NFQUxFRF9DRU5TVVN9JykKICAgIHJldHVybiBwYXJzZWQsIGNlbnN1cwoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIHByZS1yZWFkIHN1aXRlcyAobWVtbyDCpzguMSwgRC1XLTQpIOKAlCBzeW50aGV0aWMgdmFsdWVzIG9ubHkKZGVmIHNlbGZfdGVzdHMoSik6CiAgICBSID0ge30KICAgIEsgPSBKWydjb25zdGFudHMnXQogICAgc3luID0geydpZHgnOiAwLCAncSc6ICdncm91cCcsICdCJzogMC4wNSwgJ2snOiAyLjVlLTZ9ICAgICAgICAgICAgICAgICAgIyBzeW50aGV0aWMgZGlzcCBhbmNob3IgKGRpc2pvaW50IGZyb20gYW55IHNlYWxlZCB2YWx1ZSkKICAgICMgUzEgVDEgc2VsZi1ncmVwIGFscmVhZHkgYXNzZXJ0ZWQgYXQgaW1wb3J0OyBTMiBwaW5uZWQgaWRlbnRpdHkgYXNzZXJ0ZWQgaW4gbG9hZF9waW5uZWQKICAgIHIgPSBldmFsX2Rpc3BfYXJtKEosICdoZXg6c3RlcCcsIHN5biwgMS4wLCAnR0snLCAnbG8nKQogICAgaGFuZCA9IG1hdGguc3FydCgoMC4wNSAtIHJbJ0ZfTCddKSAvICgzICogYWJzKEpbJ2EyX2FnZ19ncmFpbiddWydoZXg6c3RlcCddKSkpIC8gMi41ZS02CiAgICBSWydTNF9ib3JuX2VkZ2VfdnNfaGFuZCddID0gcmVsKHJbJ2VkZ2VfYm9ybl9tJ10sIGhhbmQpOyBhc3NlcnQgUlsnUzRfYm9ybl9lZGdlX3ZzX2hhbmQnXSA8IDFlLTE0CiAgICBSWydTNV9lbnZlbG9wZV92b2lkJ10gPSBldmFsX2Rpc3BfYXJtKEosICdoZXg6c3RlcCcsIHsnaWR4JzogMCwgJ3EnOiAncGhhc2UnLCAnQic6IDAuNSwgJ2snOiAyLjVlLTZ9LCAxLjAsICdHSycsICdsbycpWyd2b2lkZWQnXQogICAgYXNzZXJ0IFJbJ1M1X2VudmVsb3BlX3ZvaWQnXSBpcyBUcnVlCiAgICAjIFM2IEZBSUwtTCBhdCBhIHN5bnRoZXRpYyBmbG9vcjogcHVzaCBhX3BoeXMgdG8gYSBtYWNyb3Njb3BpYyBzeW50aGV0aWMgdmFsdWUgdGhyb3VnaCBhIGNvcHkgb2YgSgogICAgSjIgPSBqc29uLmxvYWRzKGpzb24uZHVtcHMoSikpOyBKMlsnYV9waHlzX2NoYWluX0VfV18xYSddWydhX3BoeXNfbSddID0geydsbyc6IDIuMGU2LCAnaGknOiAyLjBlN30gICAjIHN5bnRoZXRpYzogayphID0gNSAtPiBmbG9vciB+MC45NiA+IDEwKkIKICAgIGYxID0gZXZhbF9kaXNwX2FybShKMiwgJ2hleDpzdGVwJywgc3luLCAxLjAsICdHSycsICdsbycpOyBmMTAgPSBldmFsX2Rpc3BfYXJtKEoyLCAnaGV4OnN0ZXAnLCBzeW4sIDEwLjAsICdHSycsICdsbycpCiAgICBSWydTNl9mYWlsTF9iYXNlX2FuZF9yZWxheGVkJ10gPSAoZjFbJ2ZhaWxfTCddLCBmMTBbJ2ZhaWxfTCddKTsgYXNzZXJ0IGYxWydmYWlsX0wnXSBhbmQgZjEwWydmYWlsX0wnXQogICAgYXJtNiA9IGV2YWxfYXJtKEoyLCAnaGV4OnN0ZXAnLCBbc3luXSk7IFJbJ1M2X2FybV9jbGFzcyddID0gYXJtNlsnYXJtX2NsYXNzJ107IGFzc2VydCBhcm02Wydhcm1fY2xhc3MnXSA9PSAnRkFJTC1MJwogICAgSjMgPSBqc29uLmxvYWRzKGpzb24uZHVtcHMoSikpOyBKM1snYV9waHlzX2NoYWluX0VfV18xYSddWydhX3BoeXNfbSddID0geydsbyc6IDguMGU1LCAnaGknOiAyLjBlN30gICAjIHN5bnRoZXRpYzogayphID0gMiAtPiBmbG9vciB+MC4xNTogZmFpbHMgYXQgQiwgcGFzc2VzIGF0IDEwQiAoZnJhZ2lsZSkKICAgIGYxYiA9IGV2YWxfZGlzcF9hcm0oSjMsICdoZXg6c3RlcCcsIHN5biwgMS4wLCAnR0snLCAnbG8nKTsgZjEwYiA9IGV2YWxfZGlzcF9hcm0oSjMsICdoZXg6c3RlcCcsIHN5biwgMTAuMCwgJ0dLJywgJ2xvJykKICAgIFJbJ1M2Yl9mcmFnaWxlX25vdF9kZWNsYXJlZCddID0gKGYxYlsnZmFpbF9MJ10sIGYxMGJbJ2ZhaWxfTCddLCBldmFsX2FybShKMywgJ2hleDpzdGVwJywgW3N5bl0pWydhcm1fY2xhc3MnXSkKICAgIGFzc2VydCBmMWJbJ2ZhaWxfTCddIGFuZCBub3QgZjEwYlsnZmFpbF9MJ10gYW5kIFJbJ1M2Yl9mcmFnaWxlX25vdF9kZWNsYXJlZCddWzJdICE9ICdGQUlMLUwnCiAgICAjIFM3IGRlbHRhNCBib3RoIHNpZGVzICsgZHJlc3NlZCBmaXhlZCBwb2ludAogICAgbG8gPSBldmFsX2Rpc3BfYXJtKEosICdoZXg6c3RlcCcsIHsnaWR4JzogMCwgJ3EnOiAnZ3JvdXAnLCAnQic6IDFlLTQsICdrJzogMi41ZS02fSwgMS4wLCAnR0snLCAnbG8nKQogICAgaGkgPSBldmFsX2Rpc3BfYXJtKEosICdoZXg6c3RlcCcsIHsnaWR4JzogMCwgJ3EnOiAnZ3JvdXAnLCAnQic6IDIuNWUtMywgJ2snOiAyLjVlLTZ9LCAxLjAsICdHSycsICdsbycpICAgIyBzeW50aGV0aWM6IGRlbHRhNCB+MC4xNywgaW5zaWRlIHRoZSBhNCB0dXJub3ZlcgogICAgUlsnUzdfZGVsdGE0X2xvX2hpJ10gPSAobG9bJ2RlbHRhNCddLCBsb1snZHJlc3Npbmdfc2Vuc2l0aXZlJ10sIGhpWydkZWx0YTQnXSwgaGlbJ2RyZXNzaW5nX3NlbnNpdGl2ZSddKQogICAgYXNzZXJ0IChub3QgbG9bJ2RyZXNzaW5nX3NlbnNpdGl2ZSddKSBhbmQgaGlbJ2RyZXNzaW5nX3NlbnNpdGl2ZSddCiAgICBhc3NlcnQgaGlbJ2RyZXNzZWRfc3RhdHVzJ10gPT0gJ0NPTlZFUkdFRCcgYW5kIGhpWydlZGdlX2RyZXNzZWRfbSddID4gaGlbJ2VkZ2VfYm9ybl9tJ10gICAjIGE0ID4gMCB3aWRlbnMKICAgIHggPSBoaVsnayddICogaGlbJ2VkZ2VfZHJlc3NlZF9tJ10gaWYgJ2snIGluIGhpIGVsc2UgMi41ZS02ICogaGlbJ2VkZ2VfZHJlc3NlZF9tJ10KICAgIHJlc2lkID0gMyAqIChhYnMoSlsnYTJfYWdnX2dyYWluJ11bJ2hleDpzdGVwJ10pICogeCAqKiAyIC0gSlsnYTRfYWdnX2dyYWluX2RpYWdub3N0aWMnXVsnaGV4OnN0ZXAnXSAqIHggKiogNCkgLSBoaVsnQl9wcmltZSddCiAgICBSWydTN19kcmVzc2VkX3Jlc2lkdWFsJ10gPSBhYnMocmVzaWQpOyBhc3NlcnQgYWJzKHJlc2lkKSA8IDFlLTEyCiAgICBiaWcgPSBldmFsX2Rpc3BfYXJtKEosICdoZXg6c3RlcCcsIHsnaWR4JzogMCwgJ3EnOiAnZ3JvdXAnLCAnQic6IDAuMDUsICdrJzogMi41ZS02fSwgMS4wLCAnR0snLCAnbG8nKQogICAgUlsnUzdfbm9fcm9vdF9iZXlvbmRfdHVybm92ZXInXSA9IGJpZ1snZHJlc3NlZF9zdGF0dXMnXTsgYXNzZXJ0IGJpZ1snZHJlc3NlZF9zdGF0dXMnXSA9PSAnTk8tUk9PVC1CRVlPTkQtVFVSTk9WRVInCiAgICAjIFM4IGdyb3VwIHZzIHBoYXNlIGNfcQogICAgZyA9IGV2YWxfZGlzcF9hcm0oSiwgJ2N1YmljOmdlbTgnLCB7J2lkeCc6IDAsICdxJzogJ2dyb3VwJywgJ0InOiAxZS0zLCAnayc6IDIuNWUtNn0sIDEuMCwgJ0dLJywgJ2xvJykKICAgIHAgPSBldmFsX2Rpc3BfYXJtKEosICdjdWJpYzpnZW04JywgeydpZHgnOiAwLCAncSc6ICdwaGFzZScsICdCJzogMWUtMywgJ2snOiAyLjVlLTZ9LCAxLjAsICdHSycsICdsbycpCiAgICBSWydTOF9waGFzZV9vdmVyX2dyb3VwX2VkZ2UnXSA9IHBbJ2VkZ2VfYm9ybl9tJ10gLyBnWydlZGdlX2Jvcm5fbSddOyBhc3NlcnQgYWJzKFJbJ1M4X3BoYXNlX292ZXJfZ3JvdXBfZWRnZSddIC0gbWF0aC5zcXJ0KDMpKSA8IDFlLTEyCiAgICAjIFM5IG1hc2tlZCBhYm9ydCBvbiBtYWxmb3JtZWQgcm93cyAoZWFjaCBtdXN0IHJhaXNlIFJvd0RlZmVjdCkKICAgIGJhZCA9IFsnYGRpc3BgIHwgQSB8IHNyYyB8IGdyb3VwIHwgQiA9IDFlLTMgfCBrID0gMi41ZS02IC9tIHwnLCAgICAgICAgICAgICAgICAgICAgICAgIyA3IGZpZWxkcwogICAgICAgICAgICdgZGlzcGAgfCBBIHwgc3xyYyB8IGdyb3VwIHwgQiA9IDFlLTMgfCBrID0gMi41ZS02IC9tIHwgYyB8JywgICAgICAgICAgICAgICAgICAjIGJhciBpbnNpZGUgYSBmaWVsZAogICAgICAgICAgICdgZGlzcGAgfCBBIHwgc3JjIHwgZ3JvdXAgfCAxZS0zIHwgayA9IDIuNWUtNiAvbSB8IGMgfCcsICAgICAgICAgICAgICAgICAgICAgICAjIHVubmFtZWQga2V5CiAgICAgICAgICAgJ2BkaXNwYCB8IEEgfCBzcmMgfCBncm91cCB8IEIgPSAxZS0zIHwgayA9IC0yLjVlLTYgL20gfCBjIHwnLCAgICAgICAgICAgICAgICAgICMgbmVnYXRpdml0eQogICAgICAgICAgICdgZGlzcGAgfCBBIHwgc3JjIHwgZ3JvdXAgfCBCID0gMWUtMyB8IGsgPSAyLjVlLTYgfCBjIHwnLCAgICAgICAgICAgICAgICAgICAgICAjIHVuaXQgbWlzc2luZwogICAgICAgICAgICdgZGlzcGAgfCBBIHwgc3JjIHwgYm90aCB8IEIgPSAxZS0zIHwgayA9IDIuNWUtNiAvbSB8IGMgfCcsICAgICAgICAgICAgICAgICAgICAjIHEgaW52YWxpZAogICAgICAgICAgICdgYXR0YCB8IEEgfCBzcmMgfCBncm91cCB8IEIgPSAxZS0zIHwgayA9IDIuNWUtNiAvbSB8IGMgfCddICAgICAgICAgICAgICAgICAgICAjIGtpbmQgbm90IHJlYWQgYnkgdjYKICAgIGNhdWdodCA9IDAKICAgIGZvciBiIGluIGJhZDoKICAgICAgICB0cnk6CiAgICAgICAgICAgIHBhcnNlX3NlYWxlZChiICsgJ1xuJyk7IAogICAgICAgIGV4Y2VwdCBSb3dEZWZlY3Q6CiAgICAgICAgICAgIGNhdWdodCArPSAxCiAgICBSWydTOV9tYWxmb3JtZWRfcm93c19jYXVnaHQnXSA9IChjYXVnaHQsIGxlbihiYWQpKTsgYXNzZXJ0IGNhdWdodCA9PSBsZW4oYmFkKQogICAgIyBTMTAgY2Vuc3VzIG1pc21hdGNoICh0d28gZ29vZCByb3dzIHZzIGRlY2xhcmVkIDEpCiAgICBnb29kID0gJ2BkaXNwYCB8IEEgfCBzcmMgfCBncm91cCB8IEIgPSAxZS0zIHwgayA9IDIuNWUtNiAvbSB8IGMgfCcKICAgIHRyeToKICAgICAgICBwYXJzZV9zZWFsZWQoZ29vZCArICdcbicgKyBnb29kICsgJ1xuJyk7IFJbJ1MxMF9jZW5zdXNfYWJvcnQnXSA9IEZhbHNlCiAgICBleGNlcHQgUm93RGVmZWN0OgogICAgICAgIFJbJ1MxMF9jZW5zdXNfYWJvcnQnXSA9IFRydWUKICAgIGFzc2VydCBSWydTMTBfY2Vuc3VzX2Fib3J0J10KICAgIHByLCBjcyA9IHBhcnNlX3NlYWxlZChnb29kICsgJ1xuJyk7IGFzc2VydCBwclswXVsnQiddID09IDFlLTMgYW5kIHByWzBdWydrJ10gPT0gMi41ZS02IGFuZCBjcyA9PSB7J2Rpc3AnOiAxfQogICAgIyBTMTEgY29tcGFyaXNvbi1sYXN0OiByZWZ1c2VzIHdpdGhvdXQgYSBwcmUtY29tcGFyaXNvbiBoYXNoCiAgICB0cnk6CiAgICAgICAgY29tcGFyaXNvbl9sYXN0KEosIHt9LCB7fSwgJycpOyBSWydTMTFfY29tcGFyaXNvbl9sYXN0X2d1YXJkJ10gPSBGYWxzZQogICAgZXhjZXB0IEFzc2VydGlvbkVycm9yOgogICAgICAgIFJbJ1MxMV9jb21wYXJpc29uX2xhc3RfZ3VhcmQnXSA9IFRydWUKICAgIGFzc2VydCBSWydTMTFfY29tcGFyaXNvbl9sYXN0X2d1YXJkJ10KICAgICMgUzEyIEYtVy1NT05PIHRyYXA6IGEgc3ludGhldGljIHVuaW9uIGFib3ZlIHRoZSBwaW5uZWQgZWRnZSBtdXN0IGhhbHQKICAgIGZha2UgPSB7YTogeydhcm1fY2xhc3MnOiAiUC0yJyIsICdnb3Zlcm5pbmcnOiAnR1BPTFkxLXBpbm5lZCcsICdvb21fcm9idXN0JzogVHJ1ZX0gZm9yIGEgaW4gQVJNU30KICAgIHRyeToKICAgICAgICBjb21wYXJpc29uX2xhc3QoSiwgZmFrZSwgeydXX3VuaW9uX3ByaW1lJzogWzAuMCwgMTAuMF0sICd1bmlvbl9nb3Zlcm5pbmdfYXJtJzogJ2hleDpzdGVwJ30sICcwJyAqIDMyKQogICAgICAgIFJbJ1MxMl9tb25vX3RyYXAnXSA9IEZhbHNlCiAgICBleGNlcHQgUnVudGltZUVycm9yOgogICAgICAgIFJbJ1MxMl9tb25vX3RyYXAnXSA9IFRydWUKICAgIGFzc2VydCBSWydTMTJfbW9ub190cmFwJ10KICAgICMgUzEzIG1hc2tpbmc6IGEgdG9rZW4gY29udGFpbmluZyBhIFQxIHBhdHRlcm4gaXMgbWFza2VkIGFuZCB0aGUgbWFza2VkIHRleHQgcmUtc2NhbnMgY2xlYW4KICAgIFJbJ1MxM19tYXNrJ10gPSByYl9tYXNrKCd4ICcgKyBQQVRTWzBdICsgJ3kgeicpIDsgYXNzZXJ0ICc8VT4nIGluIFJbJ1MxM19tYXNrJ10KICAgIG11bHRpID0gW3AgZm9yIHAgaW4gUEFUUyBpZiAnICcgaW4gcF0gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIyBTMTNiICh2Ni4xKTogbXVsdGktdG9rZW4gcGF0dGVybnMgbXVzdCBiZSBtYXNrZWQgd2hvbGUKICAgIGZvciBwIGluIG11bHRpOgogICAgICAgIG1tID0gcmJfbWFzaygncHJlICcgKyBwICsgJyBwb3N0Jyk7IGFzc2VydCAnPFU+JyBpbiBtbSBhbmQgcC5sb3dlcigpIG5vdCBpbiBtbS5sb3dlcigpCiAgICBSWydTMTNiX211bHRpdG9rZW5fbWFza2VkJ10gPSBsZW4obXVsdGkpCiAgICByZXR1cm4gUgoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIG1haW4KZGVmIG1haW4oKToKICAgIGNrID0geydnYXRlJzogJ0ctUzJDMS1XJywgJ3BoYXNlJzogJ21hcHBlcicsICdsZWcnOiBMRUcsICdyZWFkJzogUkVBRCwgJ2luc3RydW1lbnQnOiAnZ19zMmMxd19tYXBwZXJfdjYucHknLAogICAgICAgICAgJ2luc3RydW1lbnRfbWQ1JzogaGFzaGxpYi5tZDUoX3NyYy5lbmNvZGUoJ3V0Zi04JykpLmhleGRpZ2VzdCgpLAogICAgICAgICAgJ2xvY2snOiB7J21lbW8nOiAnMWViYjZhODJmY2IyNGUyMDdiMTY0YTY1NGViOTRkZDEnLCAnbG9ja19yZWNvcmQnOiAnNWY5NjNlZDhkN2VmZjlmODAzZGE1YzFlZWEyZjg0MWEnLAogICAgICAgICAgICAgICAgICAgJ3QxX2Jhc2UnOiBUMV9CQVNFWzFdLCAndDFfYTEnOiBUMV9BMVsxXSwgJ3Bpbm5lZF9pbnB1dHMnOiBQSU5ORURbMV0sICdzZWFsZWRfZGVjbGFyZWQnOiBTRUFMRURbMV19LAogICAgICAgICAgJ3QxX3BhdHRlcm5zJzogbGVuKFBBVFMpLCAndDFfc291cmNlX3NjYW4nOiB7J2hpdHMnOiAwLCAnbG9nZ2VkJzogbGVuKF9sKX19CiAgICBKLCB3b3JzdCwgcGluX3NyYyA9IGxvYWRfcGlubmVkKCkKICAgIGNrWydwaW5uZWRfZ2F0ZSddID0geyd3b3JzdF9yZWxfZGV2Jzogd29yc3QsICdncG9seTFfZWRnZV9waW5fc291cmNlJzogcGluX3NyYywgJ3N0YXR1cyc6ICdQQVNTJ30KICAgIHByaW50KGYnRi1XLVBJTjogUEFTUyAod29yc3QgcmVsIGRldiB7d29yc3Q6LjFlfTsgRy1QT0xZMSBlZGdlcyBwaW5uZWQgZnJvbSB7cGluX3NyY30pJykKICAgIGNrWydzZWxmX3Rlc3RzJ10gPSBzZWxmX3Rlc3RzKEopCiAgICBwcmludCgnUFJFLVJFQUQgU1VJVEVTIChTNC4uUzEzLCBzeW50aGV0aWMgdmFsdWVzKTogQUxMIFBBU1MnKQogICAgaWYgbm90IFJFQUQ6CiAgICAgICAgY2tbJ25vdGUnXSA9ICdkcnkgcnVuIOKAlCBzZWFsZWQgZmlsZSBOT1Qgb3BlbmVkJwogICAgICAgIGpzb24uZHVtcChjaywgb3BlbihDS1BBVEgsICd3JywgZW5jb2Rpbmc9J3V0Zi04JyksIGluZGVudD0xKQogICAgICAgIHByaW50KGYnY2hlY2twb2ludCAoZHJ5KSB7Q0tQQVRIfSBtZDUge21kNWYoQ0tQQVRIKX0nKTsgcmV0dXJuCiAgICAjIC0tLS0gc2VhbGVkIHNpbmdsZSBvcGVuCiAgICBzcCA9IGZpbmQoU0VBTEVEWzBdKTsgYXNzZXJ0IHNwIGlzIG5vdCBOb25lLCAnc2VhbGVkIGZpbGUgbWlzc2luZycKICAgIHJhdyA9IG9wZW4oc3AsICdyYicpLnJlYWQoKTsgc21kNSA9IGhhc2hsaWIubWQ1KHJhdykuaGV4ZGlnZXN0KCkKICAgIGFzc2VydCBzbWQ1ID09IFNFQUxFRFsxXSwgZidTRUFMRUQgTUQ1IE1JU01BVENIOiB7c21kNX0nCiAgICBja1snc2VhbGVkJ10gPSB7J21kNSc6IHNtZDUsICdieXRlcyc6IGxlbihyYXcpLCAnZGVjbGFyZWRfY2Vuc3VzJzogU0VBTEVEX0NFTlNVU30KICAgIHByaW50KGYnU0VBTEVEIEZJTEUgU0lOR0xFIFJFQUQgKHtMRUd9KTogbWQ1IHtzbWQ1fSAoe2xlbihyYXcpfSBCKScpCiAgICB0cnk6CiAgICAgICAgYW5jaG9ycywgY2Vuc3VzID0gcGFyc2Vfc2VhbGVkKHJhdy5kZWNvZGUoJ3V0Zi04JykpCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6ICAgICAgICAgICAgICAgICAgICAgICAjIGNhdGNoLWFsbCBtYXNrZWQgYWJvcnQgKFAzLUE0IMKnMihpaWkpIGxpbmVhZ2UpCiAgICAgICAgY2tbJ1gxJ10gPSB7J2RlZmVjdCc6IHJiX21hc2soc3RyKGUpKSwgJ3N0YXR1cyc6ICdNQVNLRUQtQUJPUlQnfQogICAgICAgIGpzb24uZHVtcChjaywgb3BlbihDS1BBVEgsICd3JywgZW5jb2Rpbmc9J3V0Zi04JyksIGluZGVudD0xKQogICAgICAgIHByaW50KCdYLTEgTUFTS0VEIEFCT1JUIOKAlCBzZWUgY2hlY2twb2ludCcpOyBzeXMuZXhpdCgyKQogICAgY2tbJ3NlYWxlZCddWydjZW5zdXMnXSA9IGNlbnN1cwogICAgY2tbJ2FuY2hvcnMnXSA9IGFuY2hvcnMKICAgIHByaW50KGYiQU5DSE9SIENFTlNVUzoge2xlbihhbmNob3JzKX0gcm93cyAtPiAiICsgJywgJy5qb2luKGYie2FbJ2lkeCddfTp7YVsnY2xzJ119L3thWydxJ119IiBmb3IgYSBpbiBhbmNob3JzKSkKICAgIGZvciBhIGluIGFuY2hvcnM6CiAgICAgICAgcHJpbnQoZiIgIFt7YVsnaWR4J119XSBCID0ge2FbJ0InXTouNmV9ICBrID0ge2FbJ2snXTouNmV9IC9tICBxID0ge2FbJ3EnXX0gIHJvd19tZDUge2FbJ3Jvd19tZDUnXVs6OF19IikKICAgICMgLS0tLSBwZXItYXJtIGV2YWx1YXRpb24gKG5vIGNvbXBhcmlzb24gdmFsdWUgY29uc3VsdGVkIGhlcmUpCiAgICBwZXJfYXJtID0ge2FybTogZXZhbF9hcm0oSiwgYXJtLCBhbmNob3JzKSBmb3IgYXJtIGluIEFSTVN9CiAgICB1bmkgPSB1bmlvbl9hbmRfaW50ZXJzZWN0aW9uKHBlcl9hcm0pCiAgICBja1sncGVyX2FybSddID0gcGVyX2FybTsgY2tbJ3VuaW9uJ10gPSB1bmkKICAgIHByZSA9IGpzb24uZHVtcHMoeydwZXJfYXJtJzogcGVyX2FybSwgJ3VuaW9uJzogdW5pfSwgc29ydF9rZXlzPVRydWUpLmVuY29kZSgndXRmLTgnKQogICAgcHJlX2hhc2ggPSBoYXNobGliLm1kNShwcmUpLmhleGRpZ2VzdCgpOyBja1sncHJlX2NvbXBhcmlzb25fbWQ1J10gPSBwcmVfaGFzaAogICAgZm9yIGFybSBpbiBBUk1TOgogICAgICAgIHIgPSBwZXJfYXJtW2FybV07IGQwID0gclsnZGlzcCddWzBdCiAgICAgICAgcHJpbnQoZiIgIHthcm06MTFzfSBGX0wge2QwWydGX0wnXTouM2V9ICBCJyB7ZDBbJ0JfcHJpbWUnXTouNmV9ICBkX2Rpc3AoQm9ybikge2QwWydlZGdlX2Jvcm5fbSddOi42ZX0gbSAga2Qge2QwWydrZCddOi40Zn0iCiAgICAgICAgICAgICAgZiIgIHZvaWRlZCB7ZDBbJ3ZvaWRlZCddfSAgzpQ0IHtkMFsnZGVsdGE0J106LjRmfXsnIERSRVNTLVNFTlMnIGlmIGQwWydkcmVzc2luZ19zZW5zaXRpdmUnXSBlbHNlICcnfSIKICAgICAgICAgICAgICBmIiAgZHJlc3NlZCB7ZDBbJ2VkZ2VfZHJlc3NlZF9tJ10gaWYgZDBbJ2VkZ2VfZHJlc3NlZF9tJ10gaXMgTm9uZSBlbHNlIGZvcm1hdChkMFsnZWRnZV9kcmVzc2VkX20nXSwgJy42ZScpfSBbe2QwWydkcmVzc2VkX3N0YXR1cyddfV0iCiAgICAgICAgICAgICAgZiIgIC0+IFcnX3VwcGVyIHtyWydXX3VwcGVyX20nXTouMTZnfSBtICh7clsnZ292ZXJuaW5nJ119KSBjbGFzcyB7clsnYXJtX2NsYXNzJ119IG9vbV9yb2J1c3Qge3JbJ29vbV9yb2J1c3QnXX0iKQogICAgcHJpbnQoZiIgIFdfdW5pb24nID0gKDAsIHt1bmlbJ1dfdW5pb25fcHJpbWUnXVsxXTouMTZnfV0gbSAoYXJtIHt1bmlbJ3VuaW9uX2dvdmVybmluZ19hcm0nXX0pOyBpbnRlcnNlY3Rpb24gdXBwZXIge3VuaVsnV19pbnRlcnNlY3Rpb24nXVsxXTouMTZnfSBtIikKICAgIHByaW50KGYnICBwcmUtY29tcGFyaXNvbiByZWNvcmQgbWQ1IHtwcmVfaGFzaH0nKQogICAgIyAtLS0tIGNvbXBhcmlzb24gTEFTVAogICAgY2tbJ2NvbXBhcmlzb24nXSA9IGNvbXBhcmlzb25fbGFzdChKLCBwZXJfYXJtLCB1bmksIHByZV9oYXNoKQogICAgYyA9IGNrWydjb21wYXJpc29uJ10KICAgIHByaW50KGYiQ09NUEFSSVNPTiAobGFzdCk6IGNsYXNzIHtjWydjbGFzcyddfSAgVydfdXAvV191cCA9IHtjWydyYXRpb19wcmltZV9vdmVyX3Bpbm5lZCddOi4xNmd9ICBPT00teydST0JVU1QnIGlmIGNbJ29vbV9yb2J1c3QnXSBlbHNlICdGUkFHSUxFJ30gIHJlaW5zdGF0ZW1lbnQ6IHtjWydyZWluc3RhdGVtZW50J119IikKICAgICMgLS0tLSBjaGVja3BvaW50ICsgVDEgc2NhbiBvZiB0aGUgY2hlY2twb2ludCAobWFza2VkIHRleHRzIG9ubHk7IG51bWVyaWMgY29sbGlzaW9ucyBsb2dnZWQpCiAgICB0eHQgPSBqc29uLmR1bXBzKGNrLCBpbmRlbnQ9MSwgZW5zdXJlX2FzY2lpPUZhbHNlKQogICAgaCwgbCA9IHQxX3NjYW4oUEFUUywgdHh0KQogICAgY2tbJ3QxX2NoZWNrcG9pbnRfc2NhbiddID0geydoaXRzJzogbGVuKGgpLCAnbG9nZ2VkJzogbGVuKGwpfQogICAgYXNzZXJ0IG5vdCBoLCBmJ1QxIEhJVCBpbiBjaGVja3BvaW50OiBwYXR0ZXJuIGlkeCB7c29ydGVkKHNldChoKSl9JwogICAganNvbi5kdW1wKGNrLCBvcGVuKENLUEFUSCwgJ3cnLCBlbmNvZGluZz0ndXRmLTgnKSwgaW5kZW50PTEsIGVuc3VyZV9hc2NpaT1GYWxzZSkKICAgIHByaW50KGYnY2hlY2twb2ludCB7Q0tQQVRIfSBtZDUge21kNWYoQ0tQQVRIKX0gIChUMSBjaGVja3BvaW50IHNjYW46IGhpdHMgMCwgbG9nZ2VkIHtsZW4obCl9KScpCgppZiBfX25hbWVfXyA9PSAnX19tYWluX18nOgogICAgbWFpbigpCg==
<<<END g_s2c1w_mapper_v6.py>>>

<<<BEGIN g_s2c1w_compare_v1_0.py>>>
#!/usr/bin/env python3
"""g_s2c1w_compare_v1_0.py — frozen two-leg comparator for G-S2C1-W (C-W-1..C-W-6; memo §8.4). Frozen pre-chat-emission (D-W-9).
Usage: g_s2c1w_compare_v1_0.py <chat_ckpt.json> <cc_ckpt.json>
Exit 0 ALL PASS; 1 MISS (S9); 3 CC checkpoint ABSENT or md5 != declared (comparison OUTSTANDING, nothing compared)."""
import sys, os, json, hashlib
CC_DECLARED_MD5 = '97f26c04f982b1cc1694f4a47bdce882'      # lock record addendum 1 §4
SCHEMA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'g_s2c1w_schema_v1_0.json')))
def md5f(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
def rel(a, b): return abs(a - b) / max(abs(b), SCHEMA['tolerances']['abs_floor'])
def get(d, path):
    for k in path:
        if isinstance(d, list): d = d[int(k)]
        elif isinstance(d, dict) and k in d: d = d[k]
        else: return None
    return d
def main():
    chat_p, cc_p = sys.argv[1], sys.argv[2]
    rec = {'comparator': 'g_s2c1w_compare_v1_0.py', 'cc_declared_md5': CC_DECLARED_MD5}
    if not os.path.exists(cc_p):
        rec.update({'status': 'OUTSTANDING', 'reason': 'CC checkpoint file ABSENT — a hash cannot be compared to values; C-W-1..6 not executed'})
        print(json.dumps(rec, indent=1)); sys.exit(3)
    got = md5f(cc_p); rec['cc_file_md5'] = got
    if got != CC_DECLARED_MD5:
        rec.update({'status': 'OUTSTANDING', 'reason': 'CC checkpoint md5 != declared; not the checkpoint of record'})
        print(json.dumps(rec, indent=1)); sys.exit(3)
    A, B = json.load(open(chat_p)), json.load(open(cc_p))
    miss, items = [], 0
    def cmp(path, tol=None, exact=False, label=None):
        nonlocal items
        items += 1; a, b = get(A, path), get(B, path); lab = label or '/'.join(map(str, path))
        if a is None or b is None:
            miss.append((lab, 'REPRESENTATIONAL: key absent on ' + ('both' if a is None and b is None else 'chat' if a is None else 'cc'))); return
        if exact or isinstance(a, (str, bool)) or a is None:
            if a != b: miss.append((lab, f'{a!r} != {b!r}'))
        else:
            if a is None and b is None: return
            if (a is None) != (b is None): miss.append((lab, f'{a!r} vs {b!r}')); return
            r = rel(float(a), float(b))
            if r > tol: miss.append((lab, f'rel dev {r:.3e} > {tol}'))
    T = SCHEMA['tolerances']
    # C-W-3 sealed identity
    cmp(['sealed', 'md5'], exact=True); cmp(['sealed', 'census'], exact=True); cmp(['sealed', 'bytes'], exact=True)
    # C-W-5 pinned inputs identity
    for k in SCHEMA['lock_keys']: cmp(['lock', k], exact=True)
    # C-W-4 lexer readings
    na, nb = len(A.get('anchors', [])), len(B.get('anchors', []))
    if na != nb: miss.append(('anchors/count', f'{na} vs {nb}'))
    for i in range(min(na, nb)):
        for k in ('idx', 'cls', 'q', 'row_md5'): cmp(['anchors', i, k], exact=True)
        for k in ('B', 'k'): cmp(['anchors', i, k], tol=1e-12)
    # C-W-1 edges of record + C-W-2 classes
    for arm in SCHEMA['arms']:
        cmp(['per_arm', arm, 'W_upper_m'], tol=T['rel_exact']); cmp(['per_arm', arm, 'pinned_gpoly1_edge_m'], tol=1e-12)
        cmp(['per_arm', arm, 'governing'], exact=True); cmp(['per_arm', arm, 'arm_class'], exact=True); cmp(['per_arm', arm, 'oom_robust'], exact=True)
        for i in range(min(na, nb)):
            for k in SCHEMA['disp_keys']:
                if k in ('fail_L', 'voided', 'dressing_sensitive', 'dressed_status', 'q', 'anchor', 'c_q'): cmp(['per_arm', arm, 'disp', i, k], exact=True)
                else: cmp(['per_arm', arm, 'disp', i, k], tol=T['rel_F_L_dependent'] if k in SCHEMA['F_L_dependent_fields'] else T['rel_exact'])
    cmp(['union', 'W_union_prime', 1], tol=T['rel_exact']); cmp(['union', 'union_governing_arm'], exact=True); cmp(['union', 'W_intersection', 1], tol=T['rel_exact'])
    for k in ('class', 'oom_robust', 'reinstatement'): cmp(['comparison', k], exact=True)
    cmp(['comparison', 'W_union_prime_upper_m'], tol=T['rel_exact']); cmp(['comparison', 'W_union_pinned_upper_m'], tol=1e-12)
    cmp(['comparison', 'per_arm_classes'], exact=True); cmp(['comparison', 'per_arm_governing'], exact=True)
    # C-W-6 T1 zero hits
    cmp(['t1_checkpoint_scan', 'hits'], exact=True); cmp(['t1_source_scan', 'hits'], exact=True)
    if get(A, ['t1_checkpoint_scan', 'hits']) not in (0, None) or get(B, ['t1_checkpoint_scan', 'hits']) not in (0, None): miss.append(('t1', 'nonzero hits'))
    rec.update({'items': items, 'miss': miss, 'status': 'ALL PASS' if not miss else f'MISS x{len(miss)} (S9)'})
    print(json.dumps(rec, indent=1)); sys.exit(0 if not miss else 1)
if __name__ == '__main__': main()
<<<END g_s2c1w_compare_v1_0.py>>>

<<<BEGIN g_s2c1w_schema_v1_0.json>>>
{
 "schema": "G-S2C1-W checkpoint schema v1.0 (frozen pre-chat-emission; memo §8.4)",
 "required_top": ["gate", "leg", "read", "instrument_md5", "lock", "t1_patterns", "pinned_gate", "sealed", "anchors",
                  "per_arm", "union", "pre_comparison_md5", "comparison", "t1_checkpoint_scan"],
 "lock_keys": ["memo", "lock_record", "t1_base", "t1_a1", "pinned_inputs", "sealed_declared"],
 "sealed_keys": ["md5", "bytes", "census"],
 "anchor_keys": ["idx", "cls", "q", "B", "k", "row_md5"],
 "arms": ["hex:step", "hex:gem8", "cubic:step", "cubic:gem8"],
 "per_arm_keys": ["pinned_gpoly1_edge_m", "disp", "W_upper_m", "governing", "arm_class", "oom_robust", "oom_relaxed_upper", "oom_tightened_upper"],
 "disp_keys": ["anchor", "q", "c_q", "F_L", "B_prime", "fail_L", "edge_born_m", "kd", "voided", "delta4", "dressing_sensitive", "edge_dressed_m", "dressed_status"],
 "union_keys": ["W_union_prime", "union_governing_arm", "W_intersection"],
 "comparison_keys": ["class", "oom_robust", "W_union_prime_upper_m", "W_union_pinned_upper_m", "per_arm_classes", "per_arm_governing", "reinstatement"],
 "tolerances": {"rel_exact": 1e-6, "rel_F_L_dependent": 0.035001, "abs_floor": 1e-300},
 "F_L_dependent_fields": ["F_L", "B_prime", "edge_born_m", "kd", "delta4", "edge_dressed_m"],
 "classes": {"arm": ["P-2'", "FAIL-L", "VOID-DISP"], "gate": ["TIGHTENED", "INERT", "FAIL-L"]}
}
<<<END g_s2c1w_schema_v1_0.json>>>

<<<BEGIN MANIFEST_gpoly1_phase3.md5>>>
201c18adc9e3ccbf58273ded5814ca21  compare_ghs.py
10cdf1a9bec460534d1e92f014f31b1f  extract_embeds.py
511e46b08a5cd8bddbdeb97702a4a36f  g_poly1_hexghs_ccleg.py
fba6439a3a14d8cbab19939f4ff33f39  g_poly1_hexghs_chatleg_v3.py
f1cd9de544b1378da2cfea211db6eb52  g_poly1_phase3_mapper_cc.py
2c5ca7a47042cc9929b891450f855c7e  g_poly1_phase3_mapper_v5.py
96951e65df37700e30a8783aeb5dedfb  poly1_hexghs_cc.json
d74916a22984deab514e11164ef88725  poly1_hexghs_chat.json
2064bd7b4ed4f7b2b4e09bafdc0cf85a  poly1_phase3_cc.json
b99fa804d0bef0dc46615f2adedf86d6  poly1_phase3_chat_read3_X1_breach.json
0feed9bd4c78e3a54658fbf25ad1d5da  G_POLY1_PHASE3_CC_REPORT.md
98be3e3c0071bebad816aeca4ea96755  G_POLY1_PHASE3_RELOCK_RECORD_4.md
659454eda11c969ce7d6736c6f1e1063  staging_memo_G_POLY1_phase3_ADDENDUM_4.md
<<<END MANIFEST_gpoly1_phase3.md5>>>

<<<BEGIN t1_scan.py>>>
#!/usr/bin/env python3
"""t1_scan.py — T1 forbidden-string scanner for Gate G-S2C1-W (pattern-lines-only; D-W-7 contextual numeric rule).
Usage: t1_scan.py <t1_list> <artifact>... ; exit 1 on any unconditional hit. Reports patterns by index only (never echoes them)."""
import sys, re
GLUE = r'[A-Za-z0-9_.\-]'
def load(path):
    return [l.rstrip('\n') for l in open(path, encoding='utf-8') if l.strip() and not l.startswith('#')]
def scan(pats, text):
    hits, logged = [], []
    for i, p in enumerate(pats):
        numeric = re.fullmatch(r'[0-9][0-9.eE+\-]*', p) is not None
        for m in re.finditer(re.escape(p), text):
            ctx = text[max(0, m.start()-1):m.start()] + '|' + text[m.end():m.end()+1]
            before = text[m.start()-1] if m.start() > 0 else ''
            after  = text[m.end()] if m.end() < len(text) else ''
            after2 = text[m.end()+1] if m.end()+1 < len(text) else ''
            if numeric:
                # D-W-7 (memo §6.4): a bare-numeric pattern is a HIT only when glued to a unit/identifier token
                # (letter or underscore). Digit/sign/dot glue and an exponent suffix are formatting collisions:
                # LOGGED, not fatal (H-S2C-3/12, H-CC-P2-2 lineage).
                ident = r'[A-Za-z_]'
                glued_before = bool(re.fullmatch(ident, before or ' '))
                exponent = after in 'eE' and after != '' and bool(re.fullmatch(r'[0-9+\-]', after2 or ' '))
                glued_after = bool(re.fullmatch(ident, after or ' ')) and not exponent
                (hits if (glued_before or glued_after) else logged).append((i, m.start()))
            else:
                hits.append((i, m.start()))            # non-numeric patterns are unconditional
    return hits, logged
if __name__ == '__main__':
    pats = load(sys.argv[1]); rc = 0
    for a in sys.argv[2:]:
        t = open(a, encoding='utf-8').read()
        h, l = scan(pats, t)
        print(f'{a}: patterns={len(pats)} HITS={len(h)} logged_numeric={len(l)}' + (f' hit_pattern_idx={sorted(set(i for i,_ in h))}' if h else ' — PASS'))
        rc |= 1 if h else 0
    sys.exit(rc)
<<<END t1_scan.py>>>

<<<BEGIN extract_embeds_G_S2C1_W.py>>>
#!/usr/bin/env python3
"""extract_embeds_G_S2C1_W.py — P-4 extractor for G_S2C1_W_CC_DISPATCH_INBAND.md (the ONLY reader of embedded artifacts, P-4.c).
Convention (recovered G-POLY1 extractor): payload = span between the BEGIN marker line's trailing newline and the newline
before the END marker line, plus one trailing newline. ARMORED embeds are base64 text; decoded bytes are written
(P-4.b for quarantined content; also used for byte-exactness of any artifact lacking a trailing newline).
Every extracted artifact is verified against the DECLARED (md5, bytes) table; any mismatch halts (verify-then-build)."""
import os, re, sys, base64, hashlib
DISPATCH = os.environ.get('GS2C1W_DISPATCH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'G_S2C1_W_CC_DISPATCH_INBAND.md'))
OUT = os.path.join(os.path.dirname(os.path.abspath(DISPATCH)), 'embeds'); os.makedirs(OUT, exist_ok=True)
DECLARED = [  # (name, md5, bytes, armored)
    ('staging_memo_G_S2C1_W.md', '1ebb6a82fcb24e207b164a654eb94dd1', 32219, False),
    ('G_S2C1_W_LOCK_RECORD.md', '5f963ed8d7eff9f803da5c1eea2f841a', 10875, False),
    ('G_S2C1_W_LOCK_RECORD_ADDENDUM_1.md', '125809174278cc7738692fd783d4ecd7', 7207, False),
    ('t1_forbidden_G_S2C1_W.txt', '20ba1e7eab5a3bbffe510b4840edbc57', 1560, False),
    ('t1_forbidden_G_S2C1_W_A1.txt', '735eae308aa7baec19f23da5602a2d82', 39, True),
    ('pinned_inputs_G_S2C1_W.json', 'd1edc69b16dfd0b728a48cd8389b322b', 5769, True),
    ('anchors_G_S2C1_W_SEALED.md', '8c7d59f64057e372d7b1ff760667a7c2', 154, True),
    ('g_s2c1w_mapper_v6.py', 'e034d4281c4a2906377e1587672cc128', 26458, True),
    ('g_s2c1w_compare_v1_0.py', '007688e5d8ea45d6848fd8e99c57a7d8', 4665, False),
    ('g_s2c1w_schema_v1_0.json', 'dd014b8cc4c48e5dbf356e96baded753', 1382, False),
    ('MANIFEST_gpoly1_phase3.md5', '3b178fb26068050c9f8c4866edce4078', 792, False),
    ('t1_scan.py', 'ccd47ac5779c6592bb3c49d6890049e9', 2138, False),
    ('extract_embeds_G_S2C1_W.py', 'SELF', 0, False),
]
src = open(DISPATCH, 'rb').read().decode('utf-8'); fail = 0
for name, want, size, armored in DECLARED:
    m = re.search(r'<<<BEGIN ' + re.escape(name) + r'>>>\n(.*?)\n<<<END ' + re.escape(name) + r'>>>', src, re.S)
    if not m: print(f'MISSING {name}'); fail += 1; continue
    payload = m.group(1) + '\n'
    data = base64.b64decode(payload.encode('ascii')) if armored else payload.encode('utf-8')
    got = hashlib.md5(data).hexdigest()
    ok = (want == 'SELF') or (got == want and len(data) == size)
    print(f"{'OK  ' if ok else 'FAIL'} {name:42s} {got} {len(data):>7} B{'  [armored]' if armored else ''}")
    fail += 0 if ok else 1
    open(os.path.join(OUT, name), 'wb').write(data)
print('EXTRACTION', 'ALL OK' if not fail else f'FAILED x{fail}'); sys.exit(1 if fail else 0)
<<<END extract_embeds_G_S2C1_W.py>>>

