# Exploration-Mode Ledger Entry: Recursive Projective Geometry in the Cayley-Dickson Zero-Divisor Tower (16D → 32D)

**Date:** June 16, 2026
**Mode:** EXPLORATION (declared). Not folded; not promoted. Awaiting author authorization and the two standard checks (two-leg / field-class-independence) before any register promotion.
**Cluster (proposed, on fold):** Cluster L (sedenion / Cayley-Dickson zero-divisor structure), downstream of §2.78/§2.79 (box-kites, F₂₁) and §2.81 (n-term ZD parity / odd-power rung selection).
**Provenance (deposited `/mnt/user-data/outputs/pathion_zd/`):**
- `pathion_zd_structure.py` (md5 f8a7112327c5fef94c0fc1cfd4d60a02) — 32D ZD enumeration + lower/upper/crossing decomposition + XOR probe
- `pathion_boxkite_structure.py` (md5 e8a91f16c626466d008ce37df44287de) — co-assessor graph, component decomposition, 7-box-kite baseline + 32D strata
- `pathion_boxkite_pairing.py` (md5 c3666bdd09a064ee13ddfd8f4eb5ccb3) — box-kite self-pairing test on the seven size-12 bridge components
- `pathion_pg32_incidence.py` (md5 31accbdceef102103ec0845c99f2a1c7) — PG(3,2) realization test (difference-lock + 35-line witnessing)
- `pathion64_pg42.py` (md5 3045ade522914855d7e49972854cf65e) — 64D PG(4,2) test with XOR-necessity lemma + pruned/brute method-equivalence cross-check (added June 16, 2026; see §64D Addendum)

All four reuse the project's Cayley-Dickson convention (the `build_cd_table` doubling and conjugation from `sedenion_Fp.py`), run over **F_911** (p ≡ 1 mod 455, the project's standard sedenion prime), and consult **no target value** — every count is reported as found (Eddington guard).

---

## Origin

This entry is the product of an exploration session that began from an author intuition ("a bridge between two octonion structures where math works on some levels"). The intuition was corrected on contact with the math (going *up* the tower degrades the algebra, it does not restore it) and then refined into a bounded, checkable question: **does the 32D ("pathion") zero-divisor structure build predictably from the 16D (sedenion) structure, and does the bridge between the two sedenion copies carry its own geometric organization?** The answer is yes, with a specific and exact form.

---

## R1 results (machine-verified, F_911, two-term ±1 canonical zero divisors)

### 1. Baseline reproduction (instrument soundness)
The 16D sedenion two-term canonical zero divisors reproduce the literature exactly: **84 unordered ZD pairs**, **42 assessors**, and a co-assessor graph with **7 connected components of size 6** — the seven Moreno/Cawagas box-kites, every assessor degree-4 (octahedral). (Moreno 1998, Cawagas 2004; cf. §2.78/§2.79.)

### 2. 32D decomposition: two copies + a bridge
The 32D pathion two-term canonical zero divisors number **1260 unordered pairs**, decomposing exactly as:

| Stratum | Count | Structure |
|---|---|---|
| Lower copy (indices 1..15) | **84** | the sedenion ZDs, embedded unchanged — 7 box-kites of 6 |
| Upper copy (indices 16..31) | **84** | a second sedenion copy — 7 box-kites of 6 |
| Bridge / crossing (mixed) | **1092** | new; organizes into 22 components (see §3) |
| **Total** | **1260** | 84 + 84 + 1092 |

This confirms the recursive picture at the algebra level: 𝕊 ⊕ 𝕊 (pathions = two sedenions glued), with each copy retaining its full box-kite structure and the gluing generating a far larger cross-term set (1092 ≫ 168). "It breaks harder as you climb" is the precise reading: the new (bridge) zero divisors vastly outnumber the inherited ones.

### 3. Every ZD pair satisfies the Fano-coline XOR=0 rule
All 1260 pairs — lower, upper, and all 1092 crossing — have the four-index XOR equal to 0, with **zero exceptions** in any stratum. The Fano-derived index law (the algebraic trace of the Fano-plane line structure on the canonical sedenion ZDs) survives the doubling and governs the bridge cross-terms as well. The bridge is structured, not noise.

### 4. The bridge's coarse structure: 7 components of 12 + 15 components of 14
The co-assessor graph of the 1092-pair bridge stratum has **22 connected components**, in two sizes:
- **7 components of size 12** (assessor degree-4 within)
- **15 components of size 14** (the 126 degree-12 bridge assessors live here)

7×12 + 15×14 = 84 + 210 = 294 = every bridge assessor, accounted for exactly.

### 5. The seven size-12 components are box-kite self-pairings (falsifiable test PASSED)
Pre-registered falsifiable claim: each size-12 component splits 6 lower + 6 upper, the lower 6 are *exactly one* sedenion box-kite, and the upper 6 are the +16 index-shift image of that *same* box-kite. **Confirmed for all seven, no deviations, bijective** (box-kites 0..6 each appear once). The bridge stitches each sedenion box-kite to its own image across the seam — the recursive "two copies" made concrete at box-kite granularity.

### 6. The fifteen size-14 components realize PG(3,2) exactly (the headline)
The fifteen size-14 components are **pure cross-term objects**: every assessor in them is a crossing pair (one lower index, one upper index); profile (lower, upper, mixed) = (0, 0, 14) for all fifteen. Collectively they use **exactly the 15 nonzero upper indices** (the doubling generator e₁₆ excluded) — i.e. the 15 nonzero vectors of F₂⁴, the point set of PG(3,2).

Two independent probes establish that the bridge realizes the PG(3,2) incidence geometry:

- **Difference-lock (Probe 1):** for every crossing ZD pair, the lower-index XOR difference equals the upper-index XOR difference (every d ↦ {d}, no exceptions). The XOR=0 coline rule, applied across the seam, *forces* the upper structure to mirror the lower difference-for-difference. This is the mechanism: the gluing constraint locks the two copies' combinatorics.
- **Line witnessing (Probe 2):** the bridge zero divisors witness **all 35 PG(3,2) lines and nothing else** — exactly the 35 XOR-zero triples of the 15 nonzero F₂⁴ vectors, each a genuine projective line, none missing, none spurious. (Ground truth verified independently first: 15 points, 35 lines, each point on 7 lines, every line of size 3.)

**Conclusion (R1):** the sedenion→pathion bridge is organized by the projective 3-space PG(3,2).

---

## The recursive architecture (R1 at two computed doublings: 16→32 and 32→64)

Putting the levels together:

- **Octonion level:** octonion multiplication is encoded by the Fano plane **PG(2,2)** (7 points, 7 lines); Aut = **GL(3,2) ≅ PSL(2,7)**.
- **Sedenion→pathion bridge (16→32):** organized by **PG(3,2)** (15 points, 35 lines); Aut = **GL(4,2) ≅ A₈**.
- **Pathion→64D bridge (32→64):** organized by **PG(4,2)** (31 points, 155 lines); Aut = **GL(5,2)**. (See §64D Addendum — R1, method-equivalence-verified.)

The projective dimension increases by exactly one at each algebra-doubling, and the GL(n,2) automorphism ladder advances in lockstep. This is now confirmed at **two consecutive doublings**, not a single point: PG(2,2) → PG(3,2) → PG(4,2). The group ladder GL(3,2) ≅ PSL(2,7) → GL(4,2) ≅ A₈ → GL(5,2) — already traced abstractly in §2.41.B as the PGL(n,2) ladder — is here realized **concretely in the zero-divisor structure**, not merely as an isomorphism coincidence. This connects two previously separate framework threads (the §2.41.B group ladder and the §2.78/§2.79/§2.81 zero-divisor work) through a single mechanism.

Each doubling: (i) inherits two copies of the level below with their full structure intact (16→32: 84+84; 32→64: 1260+1260); (ii) [16→32, R1] stitches corresponding box-kites to their seam-images (the size-12 components); (iii) generates new bridge units governed by the next projective geometry PG(n,2).

---

## R2 (structural, strongly indicated, NOT computed)

- **Continuation beyond 64D.** The PG(n,2)-per-doubling recursion is now R1 at two doublings (16→32 PG(3,2); 32→64 PG(4,2)). That it continues — 128D bridge realizing PG(5,2) (63 points, 651 lines, Aut = GL(6,2)), etc. — is the natural extrapolation but is not computed past 64D. The §2.81 / V4.30 odd-power result says the {2n²}-touching *floors* are ℂ, 𝕆, 32D (2⁵), 128D (2⁷); the PG(n,2) bridge pattern, by contrast, appears at *every* doubling (it is a property of the bridge, not of the floor-selection). Whether the two selection rules interact at 128D (the next floor) is open.
- **The PG(n,2) automorphism group acting on the bridge.** The point-and-line incidence is R1 at both levels; that GL(4,2) ≅ A₈ (resp. GL(5,2)) acts on the bridge components as their automorphism group — the analog of PSL(2,7) acting on the sedenion box-kites via F₂₁ — is the natural R2 reading, not yet verified by an explicit action computation.

---

## Caveats (bound the R1 claims)

1. **One prime.** All results are over F_911 (p ≡ 1 mod 455). The §2.81 standard for field-class-independence requires re-running at a prime ≢ 1 mod 455 (e.g. 101, 103, 65537, the §2.81-V4 primes). Until then the R1 results are "R1 at the mod-455≡1 class," not field-class-independent.
2. **Two-term ±1 canonical zero divisors only.** Higher-term ZDs (the n=4 kernel family, OP-2.81.1) are not in these counts. 1260 is the canonical-pair analog of the sedenion 84, not the full zero-divisor variety.
3. **Single environment.** Computed chat-side in the canonical sandbox; not yet reproduced by CC or a second implementation. Two-leg verification is outstanding.

---

## Relation to existing canon

- **§2.78 / §2.79** (box-kites, F₂₁, assessor structure): this entry's sedenion baseline reproduces that structure and extends the box-kite organization up one Cayley-Dickson level.
- **§2.81 / V4.30** (n-term ZD parity, odd-power rung selection, "𝕊 = the bridge, not a floor"): this entry computes the *structure* of that bridge. The 32D level here is the even-k bridge (2⁴ = 16 → not a {2n²} floor); the entry shows what the bridge between the 𝕆 floor (2³) and the next floor (32D = 2⁵) actually contains.
- **§2.41.B** (PSL(2,p) vs PGL(n,2) ladders; the GL(3,2)≅PSL(2,7) → GL(4,2)≅A₈ rungs): this entry realizes that ladder concretely in the zero-divisor architecture.

## Does NOT touch

No observable bridge (M.BRIDGE intact — this is pure finite algebra, no physics). No §3.x. No mass/gravity claim. §2.52 Open 3 untouched. The author's original "bridge / 5 / self-similar tower" framing is **corrected** by this entry (the tower degrades upward; the "5" that is real here is the exponent — 32D = 2⁵, the next floor — not a new "5 does X" reading; the five-seam/32D-interface R3 thread's Eddington flag stands and is not advanced by count-matching).

## Open follow-ups (bounded)

- **OP-PATH.1** (R1 target): field-class-independence — re-run all four scripts at a prime ≢ 1 mod 455; confirm 84/84/1092, all-XOR=0, 7 box-kite self-pairings, and the 35-line PG(3,2) realization are prime-class-independent.
- **OP-PATH.2** (R2→R1): verify GL(4,2) ≅ A₈ acts on the fifteen size-14 components as their automorphism group (the F₂₁-analog), realizing the line incidence as a group action.
- **OP-PATH.3** (R2 test, heavier): **CLOSED-POSITIVE (June 16, 2026; §64D Addendum).** The 64D bridge realizes PG(4,2) exactly (31 points, all 155 lines witnessed, nothing spurious; generator e₃₂ excluded; lower/upper copies = 1260 each, intact). The PG(n,2)-per-doubling recursion is confirmed at a second consecutive level. Method-equivalence cross-check (pruned vs brute force) passed at 32D before the 64D run.
- **OP-PATH.4**: relate the box-kite-self-pairing (size-12) and PG(3,2) (size-14) split to the §2.81 even/odd ZD parity — is the size-12/size-14 dichotomy the bridge-level shadow of the n-term parity result?

---

## §64D Addendum (June 16, 2026) — PG(4,2) confirmed at the next doubling

**Provenance:** `pathion64_pg42.py` (md5 3045ade522914855d7e49972854cf65e), F_911, no target consulted.

**Reproducibility safeguard (the point of this addendum's method).** The 64D brute force is ~17× the 32D cost, so a faster search was needed; to keep it trustworthy the script makes the speedup *provably equivalent* to the validated brute force rather than an unverified shortcut:

1. **Lemma (necessary condition), proved in the script header.** In the standard CD basis e_i·e_j = σ(i,j)·e_{i⊕j} for i,j ≥ 1. For a two-term canonical pair, the product is four terms ±e_{a⊕c}, ±e_{a⊕d}, ±e_{b⊕c}, ±e_{b⊕d}; it can vanish only if (i) the index sets are **disjoint** (else e_a·e_a = −e₀ appears uncancellable) and (ii) **a⊕b⊕c⊕d = 0** (else the four product-indices are pairwise distinct and cannot cancel). Pruning to {disjoint, XOR=0} candidates is therefore **complete** — it discards only provable non-ZDs. (This also explains *why* every ZD has index-XOR=0: it is forced, not incidental.)
2. **XOR-property check.** e_i·e_j = ±e_{i⊕j} verified to hold in the project's `build_cd_table` convention at both 32 and 64 dimensions.
3. **Method-equivalence cross-check.** The pruned/σ search and the original brute force produce **identical ZD sets at 32D (1260 = 1260)**. The 64D result therefore rests on a method validated against the trusted one at the largest level where both run. Any re-runner (CC, another instance) gets this equivalence check automatically before the 64D number.

**Results (R1 at p=911):**
- 64D = two-copies-of-32D glued. Two-term canonical ZD pairs total **13020 = 1260 (lower, idx 1..31) + 1260 (upper, idx 32..63) + 10500 (bridge)**. Both copies are the full 32D pathion structure, embedded unchanged.
- All 13020 satisfy index-XOR = 0 (no exceptions).
- **The bridge witnesses all 155 PG(4,2) lines and nothing else** — exactly the 155 XOR-zero triples of the 31 nonzero F₂⁵ vectors; ground truth (31 points, 155 lines) verified independently first.
- **31 of 32 upper indices participate**; the doubling generator e₃₂ is excluded (exactly as e₁₆ was at 32D). The 31 participating reductions are the points of PG(4,2).

**Consequence.** The PG(n,2)-per-doubling recursion is now R1 at **two consecutive doublings**: PG(2,2) (Fano, octonions) → PG(3,2) (16→32) → PG(4,2) (32→64), with the GL(n,2) automorphism ladder advancing GL(3,2)≅PSL(2,7) → GL(4,2)≅A₈ → GL(5,2) in lockstep. This is no longer a single-level coincidence; it is a confirmed two-level pattern, which materially strengthens both the result and its transmissibility. OP-PATH.3 closed-positive.

**Caveats unchanged.** Single prime (F_911, mod-455≡1 class — field-class-independence at a prime ≢1 mod 455 is OP-PATH.1, still outstanding); two-term ±1 canonical ZDs only; single environment (the 64D run is a second *level*, not a second *environment* — a CC re-run remains the true two-leg check). The 128→ continuation (PG(5,2)) is R2, not computed.
