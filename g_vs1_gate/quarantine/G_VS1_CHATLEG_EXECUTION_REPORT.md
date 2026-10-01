# G-VS1 — CHAT-LEG FREEZE, PRE-READ AND EXECUTION REPORT — September 30, 2026

**Lock:** memo v2 `58fd02671ea77db63e22afdcc5ee93a0` (44,709 B) LOCKED; lock record `G_VS1_LOCK_RECORD.md` **`71711946d1c4abb06fa17402e8d5a6c9`** (23,071 B) with Addendum A-2 (readings Q-VS-1..5, elections E-VS-1..10(a), operationalizations A-2.3–A-2.9); T1 gate list `324f577d` (31) FROZEN; schema v1.0 **`4690e07d5a22cc7a1c5d08db39eda3fe`** (6,253 B) and comparator v1.0 **`69011375d28ec8f63f3ac76383e98321`** (9,236 B; selftest 7/7, 415 checks on a full pair) FROZEN; extract `940b0bee` pinned.

**Instrument frozen:** `g_vs1_chatleg.py` **`cb2e22308305cb6e2251531465984df5`** (55,958 B). Exact arithmetic (Fractions / sympy rationals); numpy integers mod p only for the GF(p) upper bounds (primes 1,048,573 and 999,983). Modes `preread` / `run`. Guards: md5 + byte counts of the memo, the lock record, the extract; md5 of the T1 list, the scanner, the schema, the comparator; T1 self-scan of the instrument, the memo, the lock record, the extract, the schema and the comparator under the gate list (31 patterns) at every invocation — all CLEAN, 0 collisions. Class codes only.

## 1. Pre-read suites (Phase 0) — GREEN

`g_vs1_chatleg_prereadcheckpoint.json` **`b208db869bbc0c8c80c482737d957d9d`** (5,941 B), 46.8 s. 0a PASS: dim g₂ = 14, all derivations, antisymmetric, closed, max |entry| 1; so(4)_ℍ dim 6; su(2)_long dim 3 index **1**; su(2)_short dim 3 index **3**. 0b PASS: commutant dims 1 (the 7) / 2 (1 ⊕ 7). 0c PASS: U(8) certified 1 / 1 (degrees 2 / 4); O(16) 1 / 1 by the sandwich; so(16)-orbit rank 15 at a unit vector (S¹⁵ transitive); V of record S¹⁵, π₁ = 0. 0d PASS: spin-1 polar → π₁ = ℤ with elementary winding π (m = 2, witness verified), π₂ = ℤ, π₃ = ℤ; spin-1 ferro → π₁ = ℤ₂ (d = 2), π₂ = 0, π₃ = ℤ — the textbook structure; Weyl counts spin-1 1/2/2; 2T order 24 closed; π₄(S²) chain recorded. 0e PASS: orbit ranks 0 (e₀), 6 (e₁), 11 (e₁,e₂), 11 (associative triple), **14 (generic triple < 15)**. 0f PASS: su(3) dim 8; three explicit degree-2 invariants, lower bound 3 > 2.

## 2. Execution (Phases 1–3, verdict) — chat leg of record

`g_vs1_chatleg_checkpoint.json` **`d3d1ed074259c8924d0c29a03d320918`** (32,101 B), 86.1 s; log `run_chatleg.log` `4b3847fdc0d2eb9069a2ce4dfcb36bb9`. T1 post-write: 0 hits, 0 collisions.

**Phase 1 (certified inventory).** G₂ × U(1) on ℝ¹⁶: degree 2 **2** (lower 2 = upper 2 both primes), degree 4 **6** (lower 6 = upper 6, 1,296 monomials), **T-even 5**; on ℝ¹⁴: 1 / 2; degree 6 (Weyl) 10 on ℝ¹⁶, 2 on ℝ¹⁴ (explicit lower bound 2 on ℝ¹⁴). SO(7) × U(1): the same at every degree (certified 2/6 and 1/2; Weyl 2/6/10 and 1/2/2). **Methods agree (kernel certificate = Weyl) at degrees 2 and 4; G₂ = SO(7) at degrees 2, 4, 6 on both spaces → F-VS-2 SILENT.** Hand count met → F-VS-1 SILENT. T-parity: all +1 except Q (−1). RUS: every basis element is real-unit-splitting (none is a function of |ψ|² alone); RUS subspace dim 1 (degree 2), 5 (degree 4), T-even 4; singlet-blind: N, N², |S|². The point of record: |ψ|⁴ = ρ₀² + 2ρ₀N + N² → (A, B, c₄, c₅) = (0, 0, 0, 0): the origin.

**Phase 2 (stratum table, both the chat representatives of A-2.6).**

| Stratum | dim h / dim k | K | P = p(H) | m | π₀(H) | **π₁(V)** | elementary winding | π₂ | π₃ | dim V |
|---|---|---|---|---|---|---|---|---|---|---|
| R | 14 / 14 | G₂ | {1} | 1 | 1 | **ℤ** | 2π | 0 | 0 | 1 |
| P7 | 8 / 8 | SU(3) | {±1} (witness σ_(2,3,5)) | 2 | ℤ₂ | **ℤ** | **π** | 0 | 0 | 7 |
| F7 | 4 / 3 | SU(2)_long (index 1) | U(1) | — | 1 | **0** | none | 0 | 0 | 11 |
| I7 | 3 / 3 | SU(2)_long | {±1} (witness σ_(3,4,6)) | 2 | ℤ₂ | **ℤ** | **π** | 0 | 0 | 12 |
| MP+ / MP− / MP0 | 8 / 8 | SU(3) | {1} | 1 | 1 | **ℤ** | 2π | 0 | 0 | 7 |
| MF | 3 / 3 | SU(2)_long | {1} | 1 | 1 | **ℤ** | 2π | 0 | 0 | 12 |
| MI+ / MI− / MI0 | 3 / 3 | SU(2)_long | {1} | 1 | 1 | **ℤ** | 2π | 0 | 0 | 12 |

The criterion **π₁(V) = 0 ⟺ ρ₀ = 0 and S = 0** holds on all eleven strata. Reduction check (A-2.6 effective map) PASS. Sampling 2,401 points: strata realized as minimizers {R, P7, F7, MP±, MP0, MF, MI±} — **I7 is never a minimizer** (on the edge ρ₀ = 0 the potential is c₄s², minimized at an end); the criterion holds on every non-degenerate minimizer; the cone property holds; P0 only at the origin. Tally (top): R 708, P7 638, F7 356, MP+ 196, MP− 196, MI± 33 each, MF 18, two-stratum ties (F7+R 45, P7+R 48, …) and 128 degenerate outcomes (edges, interior segments, P0). Codimension: 5 RUS directions through 4 effective parameters; P0 the origin. **F-VS-3 SILENT.**

**Phase 3 (the F-a map; the algebra-native contact forms, exact expansions in the T-even basis (ρ₀², ρ₀N, N², |S|², Re)):**

| Form | coefficients | (A, B, c₄, c₅) | minimum set | π₁ there |
|---|---|---|---|---|
| F-a.1 \|⟨ψ,ψ⟩\|² | (1, 0, 0, 1, 2) | (1, 0, 1, 2) | **degenerate interior segment** ρ₀ = s from F7 (0,0) to MP− (½,½) through MI− | F7: 0; MI−, MP−: ℤ |
| F-a.2 ‖ψψ̄^†‖²_H | (1, 4, 2, −1, −2) | (−1, 0, −1, −2) | **degenerate polar edge** s = 1 − ρ₀: R, MP, P7 | all ℤ |
| F-a.3 ‖ψ̄^†ψ‖²_H | = F-a.2 | = F-a.2 | = F-a.2 | all ℤ |
| F-a.4 ‖ψ²‖²_H | (1, 4, 0, 1, −2) | (−3, 4, 1, −2) | **F7 alone** | **0** |
| F-a.5 N_𝕆(ψψ̄^†) | = F-a.1 (norm multiplicativity) | = F-a.1 | = F-a.1 | as F-a.1 |
| F-a.6 ‖Im_𝕆(ψψ̄^†)‖²_H | (0, 2, 1, −1, −2) | = F-a.2 | = F-a.2 | all ℤ |
| D-a.1, D-a.2 (degree 2) | ρ₀ + N | O(16) | — | — |

All eight forms are G₂ × U(1)-invariant and T-even (residual 0 in the T-even basis). **HYP-VS-5 (left blank at lock) is answered:** the algebra-native quartics do not agree among themselves — the Hermitian-norm forms select the polar edge (protected, degenerate), the bilinear-norm form a degenerate ferro–polar segment, and the octonionic-square form the ferro-7 stratum (unprotected); none is the O(16) point; the degree-2 algebra forms are O(16). Forcing table: F-a MAP (not forcing: I2 is the import); F-b SCREENED_OUT (A-2.1; successor S-VS-1); F-c NOT_FORCING (A-2.2); F-d EXCLUDED; live sources 0 → **F-VS-4 SILENT.**

**Verdict (machine, last): class code VC-3** ("extra (real-unit-splitting) invariants certified; every forcing source screened not forcing / out / excluded"); precedence VC-4 > VC-2 > VC-1 > VC-3.

## 3. Comparator sanity

`g_vs1_compare_v1_0.py compare` on the chat checkpoint against itself: 415 checks, 414 PASS, 1 MISS — the by-design C-VS-0 "instrument_md5 differ" check (a self-pair must fail it). The two-leg run of record follows CC's checkpoint.

## 4. Items

- **D-VS-1 (order of legs):** the chat leg executed before the dispatch (E-VS-7(a): chat first; the lock directive's "ensure all pre-read suites are green" taken as Phase 0, and the full run as the leg's execution on the frozen instrument). The instrument was frozen (`cb2e2230`) before the run and before the dispatch; the chat instrument, both chat checkpoints, this report and the run log travel quarantined (P-4.b) and are decoded by CC only after its pre-consultation commit.
- **D-VS-2 (build-run disclosure):** the instrument's components were exercised end-to-end during the build (lock record §5); one design gap (interior-segment degeneracy) fixed before freeze; nothing from the build runs is banked.
- **H-VS-1 (chat-self-caught, pre-freeze, no verdict effect):** the memo §2.3 states that the minima of the orbit-space problem "lie at its vertices and edges"; the potential is quadratic in s (through |S|²), so interior critical points and interior segments of minimizers occur (MI± strata are realized at 33 + 33 grid points; F-a.1 has an interior segment). A-2.6 of the lock record states the correct enumeration (vertices, edge critical points, the interior critical point, degenerate faces and segments); the memo is locked and not edited.
- No H-item fired in the run; no D-item beyond D-VS-1/2.

## 5. Hashes of record

| File | md5 | Bytes |
|---|---|---|
| `g_vs1_chatleg.py` | `cb2e22308305cb6e2251531465984df5` | 55,958 |
| `g_vs1_chatleg_prereadcheckpoint.json` | `b208db869bbc0c8c80c482737d957d9d` | 5,941 |
| `g_vs1_chatleg_checkpoint.json` | `d3d1ed074259c8924d0c29a03d320918` | 32,101 |
| `run_chatleg.log` | `4b3847fdc0d2eb9069a2ce4dfcb36bb9` | — |
| `G_VS1_LOCK_RECORD.md` | `71711946d1c4abb06fa17402e8d5a6c9` | 23,071 |
| `g_vs1_schema_v1_0.json` | `4690e07d5a22cc7a1c5d08db39eda3fe` | 6,253 |
| `g_vs1_compare_v1_0.py` | `69011375d28ec8f63f3ac76383e98321` | 9,236 |

T1: this report scans CLEAN under the gate list `324f577d` and the base `05302210`.
