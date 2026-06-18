# CC Verification — Pathion ZD / PG(n,2) recursion ledger

**Date:** 2026-06-17 · **Verifier:** CC (second environment) · **Subject:**
`ledger_entry_pathion_zd_pg32_recursion.md` (June 16 2026) + its five scripts.
**Result: every R1 claim reproduced exactly; two of the three outstanding caveats
now closed.**

## 1. Provenance (md5 — all match the ledger)
| file | md5 | ledger md5 | match |
|---|---|---|---|
| pathion_zd_structure.py | f8a7112327c5fef94c0fc1cfd4d60a02 | f8a711… | ✓ |
| pathion_boxkite_structure.py | e8a91f16c626466d008ce37df44287de | e8a91f… | ✓ |
| pathion_boxkite_pairing.py | c3666bdd09a064ee13ddfd8f4eb5ccb3 | c3666b… | ✓ |
| pathion_pg32_incidence.py | 31accbdceef102103ec0845c99f2a1c7 | 31accb… | ✓ |
| pathion64_pg42.py | 3045ade522914855d7e49972854cf65e | 3045ad… | ✓ |

## 2. Reproduced results (F_911, exactly as claimed)
| claim (ledger §) | claimed | reproduced |
|---|---|---|
| 16D sedenion ZD pairs (§R1.1) | 84 | **84** ✓ |
| 16D assessors / box-kites | 42 / 7×size-6, all deg-4 | **42 / 7×6, deg {4:42}** ✓ |
| 32D pairs = lower+upper+bridge (§R1.2) | 1260 = 84+84+1092 | **1260 = 84+84+1092** ✓ |
| every quadruple index-XOR=0 (§R1.3) | all, 0 exceptions | **{0:84},{0:1092},{0:84}** ✓ |
| bridge components (§R1.4) | 22 = 7×size-12 + 15×size-14 | **{12:7, 14:15}** ✓ |
| bridge assessor degrees | deg {4:168, 12:126} | **{4:168, 12:126}** ✓ |
| size-12 = box-kite self-pairings (§R1.5) | all 7, bijective | **CONFIRMED 7/7, box-kites 0..6 each once** ✓ |
| size-14 profile | (0,0,14)×15, 15 upper indices | **(0,0,14):15, 15 of 16** ✓ |
| PG(3,2) difference-lock (§R1.6 P1) | every d↦{d} | **True** ✓ |
| PG(3,2) line witnessing (§R1.6 P2) | 35/35, none spurious | **35/35, subset=True, missing=0** ✓ |
| 32D pruned == brute method-equiv | 1260==1260, identical sets | **identical sets: True** ✓ |
| 64D total (§64D Add.) | 13020 = 1260+1260+10500 | **13020 = 1260+1260+10500** ✓ |
| 64D all XOR=0 | yes | **True** ✓ |
| PG(4,2) witnessing | 155/155, e₃₂ excluded, 31 pts | **155/155, 31 reductions, missing=0** ✓ |

Run times (this environment): 32D enumeration ≈ 35 s each; 64D script ≈ 35 s
(pruned). Nothing diverged.

## 3. New independent check — field-class-independence (closes OP-PATH.1)
The ledger's #1 caveat: all results were at a single prime p=911 (p ≡ 1 mod 455);
the §2.81 standard requires a prime ≢ 1 mod 455. I re-derived the core counts from
an independently-typed driver (`field_class_check.py`) at **four primes spanning
both classes**:

| prime | p mod 455 | 16D | 32D = lo+up+cross | all XOR=0 | box-kite deg | PG(3,2) |
|---|---|---|---|---|---|---|
| 911 | 1 (published class) | 84 | 1260 = 84+84+1092 | True | {4:42} | 35/35 |
| 101 | 101 (**other class**) | 84 | 1260 = 84+84+1092 | True | {4:42} | 35/35 |
| 103 | 103 (**other class**) | 84 | 1260 = 84+84+1092 | True | {4:42} | 35/35 |
| 65537 | 17 (**other class**) | 84 | 1260 = 84+84+1092 | True | {4:42} | 35/35 |

Identical in every column but the prime. **OP-PATH.1 → CLOSED-POSITIVE**: the
84 / 84+84+1092 / all-XOR=0 / box-kite / 35-line PG(3,2) structure is
field-class-independent. (Expected — over a field the canonical ±1 two-term ZD
condition is a set of sign equations in σ(i,j)∈{±1}, independent of p once p>2 — but
the ledger correctly required it be shown, and now it is.)

## 4. Caveat status after this verification
- **Caveat #1 (one prime):** CLOSED — see §3, four primes, two classes.
- **Caveat #3 (single environment / CC two-leg):** CLOSED — this is the CC re-run;
  all numbers reproduced in a second environment.
- **Caveat #2 (two-term ±1 canonical ZDs only):** UNCHANGED — higher-term ZDs
  (n=4 kernel family) are still out of scope; 1260/13020 remain the canonical-pair
  counts, not the full ZD variety. Not a defect, a scope boundary.

## 5. Scope / what is NOT claimed (unchanged from ledger)
Pure finite algebra. No observable, no physics, M.BRIDGE intact. The 128D→PG(5,2)
continuation remains R2 (not computed here — it would be the natural next test, a
third consecutive doubling). The result verified is: the Cayley-Dickson ZD bridge
realizes PG(n,2) exactly at two consecutive doublings (16→32 PG(3,2), 32→64 PG(4,2)),
with the GL(n,2) automorphism ladder advancing in lockstep — and that this is
prime-class-independent.

## 6. NEW RESULT — third consecutive doubling: 128D realizes PG(5,2) (R1)
The ledger left 128D→PG(5,2) as R2 (not computed). It is now computed and
**closes positive**. `pathion128_pg52.py`, pruned method (prime-free), 128D table:

| quantity | predicted by the pattern | computed |
|---|---|---|
| 128D total two-term canonical ZD pairs | — | **117180** |
| decomposition | two 64D copies + bridge | **13020 + 13020 + 91140** |
| every quadruple index-XOR=0 | yes | **True** |
| PG(5,2) ground truth | 63 pts, 651 lines, each pt on 31 | **63, 651, {31}** ✓ |
| bridge line witnessing | all 651, none spurious | **651/651, subset, missing=0** |
| generator e₆₄ | excluded | **excluded; 63 reductions used** |

**Implementation validated at two levels, not one.** `pathion64_brute_check.py`
ran the full 64D brute force (14 min) against the pruned method: **both 13020,
identical sets**. Combined with the in-script 32D equivalence (1260==1260) and the
dimension-general completeness lemma, the 128D pruned count rests on implementation
checks at 32D *and* 64D. The pruned search uses only σ(i,j)∈{±1} — no prime — so
this third level is field-class-independent by construction.

### Updated recursion (now R1 at THREE consecutive doublings)
| level | doubling | geometry | points | lines | Aut = GL(n,2) |
|---|---|---|---|---|---|
| octonion | — | PG(2,2) Fano | 7 | 7 | GL(3,2) ≅ PSL(2,7) |
| 16→32 | sedenion→pathion | PG(3,2) | 15 | 35 | GL(4,2) ≅ A₈ |
| 32→64 | pathion→64D | PG(4,2) | 31 | 155 | GL(5,2) |
| **64→128** | **64D→128D** | **PG(5,2)** | **63** | **651** | **GL(6,2)** |

The projective dimension advances by exactly one per algebra-doubling, confirmed
at three consecutive levels.

## 7. NEW RESULT — fourth consecutive doubling: 256D realizes PG(6,2) (R1)
`pathion256_pg62.py`, pruned method (prime-free), 256D table:

| quantity | computed |
|---|---|
| 256D total two-term canonical ZD pairs | **992124** |
| decomposition (two 128D copies + bridge) | **117180 + 117180 + 757764** |
| every quadruple index-XOR=0 | **True** |
| PG(6,2) ground truth | **127 pts, 2667 lines, each pt on 63** ✓ |
| bridge line witnessing | **2667/2667, none spurious, missing=0** |
| generator e₁₂₈ | **excluded; 127 reductions used** |

Trust basis: the dimension-general completeness lemma + implementation validated
pruned==brute at 32D (in-script) and 64D (full brute, §6). A 128D/256D brute force
is *not* run (256D brute ≈ hundreds of hours); this is the recorded tradeoff — the
proven lemma plus two-level validation, not a third brute leg. Prime-free pruned
search ⇒ field-class-independent by construction.

### Updated recursion (now R1 at FOUR consecutive doublings)
| level | doubling | geometry | points | lines | Aut = GL(n,2) | total ZD pairs | bridge |
|---|---|---|---|---|---|---|---|
| octonion | — | PG(2,2) Fano | 7 | 7 | GL(3,2)≅PSL(2,7) | — | — |
| 16→32 | sedenion→pathion | PG(3,2) | 15 | 35 | GL(4,2)≅A₈ | 1260 | 1092 |
| 32→64 | pathion→64D | PG(4,2) | 31 | 155 | GL(5,2) | 13020 | 10500 |
| 64→128 | 64D→128D | PG(5,2) | 63 | 651 | GL(6,2) | 117180 | 91140 |
| **128→256** | **128D→256D** | **PG(6,2)** | **127** | **2667** | **GL(7,2)** | **992124** | **757764** |

Projective dimension +1 per algebra-doubling, four consecutive levels. Each doubling
embeds two intact copies of the level below (totals: 84→1260→13020→117180→992124,
each = 2×prev + bridge) and the bridge realizes the next PG(n,2). The 512→PG(7,2)
continuation (255 points, 10795 lines) is the next R2.

## 8. NEW RESULT — fifth consecutive doubling: 512D realizes PG(7,2) (R1)
`pathion512_pg72.py`, pruned method (prime-free), 512D table (~2.5 min):

| quantity | computed |
|---|---|
| 512D total two-term canonical ZD pairs | **8161020** |
| decomposition (two 256D copies + bridge) | **992124 + 992124 + 6176772** |
| every quadruple index-XOR=0 | **True** |
| PG(7,2) ground truth | **255 pts, 10795 lines, each pt on 127** ✓ |
| bridge line witnessing | **10795/10795, none spurious, missing=0** |
| generator e₂₅₆ | **excluded; 255 reductions used** |

Trust basis unchanged (lemma + 32D/64D pruned==brute; no higher brute; prime-free
⇒ field-class-independent).

### Full recursion — R1 at FIVE consecutive doublings
| level | doubling | geometry | points | lines | Aut = GL(n,2) | total ZD pairs | bridge |
|---|---|---|---|---|---|---|---|
| octonion | — | PG(2,2) Fano | 7 | 7 | GL(3,2)≅PSL(2,7) | — | — |
| 16→32 | sedenion→pathion | PG(3,2) | 15 | 35 | GL(4,2)≅A₈ | 1260 | 1092 |
| 32→64 | pathion→64D | PG(4,2) | 31 | 155 | GL(5,2) | 13020 | 10500 |
| 64→128 | 64D→128D | PG(5,2) | 63 | 651 | GL(6,2) | 117180 | 91140 |
| 128→256 | 128D→256D | PG(6,2) | 127 | 2667 | GL(7,2) | 992124 | 757764 |
| **256→512** | **256D→512D** | **PG(7,2)** | **255** | **10795** | **GL(8,2)** | **8161020** | **6176772** |

Projective dimension +1 per algebra-doubling, five consecutive levels. Each total =
2×(previous) + bridge; bridge growth 1092 → 10500 → 91140 → 757764 → 6176772.
Points/lines match PG(n,2) at every level (points = 2ⁿ⁺¹−1, lines = the XOR-zero
triples). The 1024→PG(8,2) continuation (511 points, 43435 lines) is the next R2.

*Files added by this verification: `field_class_check.py` (independent driver),
`pathion128_pg52.py`, `pathion64_brute_check.py`, `pathion256_pg62.py`,
`pathion512_pg72.py`, this report. Author scripts unmodified.*
