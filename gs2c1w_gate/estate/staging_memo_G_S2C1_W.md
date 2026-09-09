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
