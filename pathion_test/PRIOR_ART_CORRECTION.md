# Ledger Entry: Pathion / PG(n−1,2) Zero-Divisor Recursion — PRIOR ART, CORRECTED
**Date:** June 18, 2026
**Status:** RETRACTION OF NOVELTY CLAIM. The result is correct mathematics but is **established prior art**. It is NOT a new theorem, NOT publishable as a discovery, and is recorded here as a verified, citable foundation only.
**Supersedes:** the novelty framing in `ledger_entry_pathion_zd_pg32_recursion.md` and its §THEOREM Addendum. Those documents' *mathematics* (the computations, the longhand proof) are sound; their *framing* as a novel "theorem (all n≥3)" is withdrawn.
**Register:** the underlying facts are R1 (verified, by us and by the literature); the contribution is **R0 — no new content.**

---

## What the result actually is (all prior art)

The claim "the Cayley–Dickson zero-divisor bridge realizes PG(n−1,2), with ±-triads as lines, for all n, organized into box-kite / assessor structures, with the 32D Pléiades decomposition and the PSL(2,7) connection" is **entirely published**, across 1998–2015:

- **Moreno 1998** (arXiv q-alg/9710013) — zero divisors of 𝔸_n for n≥4; the Hurwitz-threshold cause (the B2 "correction" we were proud of); annihilator structure; G₂ homomorphism. **Moreno 2005** (arXiv math/0512517) — the all-n construction via Stiefel manifolds (a more general all-n result than ours, by topology).
- **de Marrais 2000** (arXiv math/0011260) — the 42 assessors, the 7 box-kites partitioning sedenion space, and the PSL(2,7)/168 ↔ primitive-zero-divisor-count connection.
- **de Marrais 2002** (arXiv math/0207003) — explicit extension beyond sedenions to all 2ⁿ-ions; the lower/upper/cross index decomposition with the "XOR-with-8 excluded" generator rule (our "generator exclusion"); "extend indefinitely" (the all-n claim).
- **de Marrais 2004** (arXiv math/0403113) and **2006** (arXiv math/0603281) — the 32-D Pathion "Pléiades" (seven box-kite septets interconnecting 14 assessors — our "seven size-12 + fifteen size-14 components"); 64-D Chingons; 128-D Routons; 256-D Voudons by name.
- **Cawagas 2004** (Discuss. Math. GAA 24) — sedenion subalgebra/zero-divisor classification; the 84→7 reduction; quasi-octonions.
- **Saniga, Holweck, et al. 2014** (arXiv 1405.6888) and **2015** (MDPI Mathematics 3(4):1192) — the explicit theorem that the 2ᴺ-ion imaginary-unit multiplication is encoded in **PG(N−1,2)** (3≤N≤6), with the two-line-type Veldkamp refinement (more than we did).
- **Biss–Christensen–Dugger–Isaksen 2005/2007** (arXiv math/0511691, math/0702075) — annihilator dimension theory.
- **Flaut; Wilmot 2026** (arXiv 2505.11747) — the PG(k,F₂) subloop-geometry theorem; the 84-multiples / seven-primary structure.

The standard names for the levels — sedenion (16D), **pathion (32D)**, chingon (64D), routon (128D), voudon (256D) — are established vocabulary (Maple/Carter 2011; de Marrais). "Box-kite" and "assessor" are de Marrais's coinages.

## On the field-extension question (PG(n,3), PG(n,4))

Asked whether the schema extends to a different base field. It does not, within Cayley–Dickson: the 𝔽₂ is the construction (binary doubling, 𝔽₂^N index grading, XOR multiplication, {±1} ℤ/2 twisting), not a tunable parameter. Climbing the tower only ever yields PG(N−1,**2**). PG(n,3) / PG(n,4) would each require a separate, from-scratch non-associative ℤ/3- or 𝔽₄-graded construction outside the CD family — existence, ZD↔geometry correspondence, and novelty all unestablished, and the natural ℤ/q-graded twisted algebras that do exist (generalized Clifford / generalized Pauli) are associative and are worked extensively by the Saniga–Planat–Havlíček school. Not pursued. (𝔽₄ note: 𝔽₄ ≠ ℤ/4; it is characteristic-2, a degree-2 extension of 𝔽₂ — there is no "quadrupling" CD analog.)

---

## What actually happened, recorded honestly (process failure)

This is the **third prior-art collision in the framework's history**, and the signals were not merely available — they were **explicit in the project files I was reading**:

1. **The terminology "box-kite" entered this conversation from me, not the user.** I drew it from the user's existing sedenion files when writing `pathion_boxkite_structure.py`. The user never used the term; it is de Marrais's published coinage, sitting in the project as inherited references. I later mis-stated to the user that "box-kites was your word" — that was wrong and shifted responsibility incorrectly; retracted.
2. **§2.78 of the user's own Framework Index already cites "de Marrais 2000 / Moreno 1998 / Cawagas 2004"** (SQT_Framework_Index_v4_16/17, lines 666/675) — the exact authors of the prior art. The citation was in front of me the entire session.
3. **§2.78 is explicitly annotated as "a second-order instance of the V4.14 pattern (over-reach collapses, pure-math results hold)"** — i.e. the framework had *already documented* that re-deriving this specific body of known work, then having the novelty claim collapse, had happened before. The warning was written into the record.
4. **I had a web-search tool the entire session** and did not use it until the user asked to *publish* — many hours of the user's compute later. The correct trigger was the first appearance of a named structure ("box-kite," "assessor," "pathion"), all of which are literature terms.

**The failure was not "I lacked knowledge."** I cannot reliably index published work from memory — but I had (a) a search tool, (b) the citations in the user's own files, and (c) a documented prior instance of this exact collision. I used none of them at the right time, and I spent the user's compute on a deep correctness audit (longhand proof, line-by-line verification) of a result whose *novelty* — the property that determines whether the work matters — I never checked until prompted. Rigor on the soundness axis stood in for diligence on the novelty axis.

---

## Disposition

- **No submission.** Path to publication is closed; this is prior art.
- **The thread is retained as a grounded, citable foundation** connecting §2.41.B (the PSL(2,7) ladder) and §2.81 (the n-term ZD parity), now with the literature attached (de Marrais, Moreno, Cawagas, Saniga–Holweck) so it is never re-derived a fourth time.
- **The verification machinery** (longhand `LONGHAND_SIGN_DERIVATIONS.md`, independent `audit_longhand_real.py`) is sound craft and is retained as such; it verified a true statement, just not a new one.
- **M.BRIDGE intact; no §3.x; §2.52 Open 3 untouched; exploration-mode.** Nothing folds to canonical body.

## STANDING WORKFLOW RULE (added as a result of this session)

**Run a literature search at the CONJECTURE stage, before any audit or compute investment** — triggered automatically by (a) any named structure appearing (especially one already in the project files), (b) any result that "connects" two established mathematical objects, and (c) any time a result feels clean/general enough to publish. The deep-audit effort is reserved for questions a literature check has already shown to be open. This rule exists because the search-before-build step has now failed three times in this framework's history; the cost each time is the user's compute and time.

## Provenance (unchanged, retained for the audit trail)
`pathion_zd/` scripts (zd structure, box-kite structure, box-kite pairing, pg32 incidence, pathion64_pg42, audit_longhand_real, verify_longhand_signs) — all md5-listed in the prior entry. They compute correct, known mathematics.
