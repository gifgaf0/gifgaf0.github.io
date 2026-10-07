# B2 — PSL(2,7) Zenodo note: checks and v3 draft (DRAFT, not deposited)

**Plain-language summary.** The PSL(2,7) note is mathematically sound. A version 3 is drafted as tracked changes on the author's v2.1 file, and nothing has been deposited. It makes four substantive changes.
- **It now cites the classical literature.** Its main results are textbook facts about a well-understood group action, and the note now says so and cites the papers that classify such actions (Faradžev–Ivanov 1990, Praeger–Saxl–Yokoyama 1987, Inglis–Liebeck–Saxl 1986).
- **One open problem miscounted.** It listed 104 group elements whose fixed set on the 7-sphere is a circle. The true number is 146, because the 42 elements of order 4 were left out.
- **The same open problem misdescribed the theory it needs.** It said Kawasaki's index theorem covers only isolated singularities, which is false. The fix: for a finite group acting on a sphere, the problem reduces to standard equivariant index theory, and the η-invariant is a finite sum.
- **Small fixes.** A reference year is corrected (Kawasaki 1979, not 1978), an appendix label is corrected, a typo (Sₙ for Sⁿ) is fixed, and one open problem gains a sentence of context.

The audit's other item, the D₄ "maximal subgroup" error in Theorem 2.1, was **already corrected in v2.1**. v2.1 lists the two S₄ classes and 7:3 and calls D₄ the non-maximal Sylow 2-subgroup (Theorem 2.1 table, Remark 2.2, Theorem 2.3, Appendix A). The stale text is the ledger's §1.1 copy, which gets a bracket in the Phase B fold.

**For the author.** The draft is `v3_draft/PSL27_v3_DRAFT_tracked.docx`. Every change is a tracked insertion or deletion by "Claude (audit draft)", so each one can be accepted or rejected in Word. Clean copy: `PSL27_v3_DRAFT_clean.docx` (PDF beside it).

**Assumption to confirm.** The v2.1 file (attached October 7, "revised May 2026") is taken to be the text deposited as Zenodo v2 (DOI 10.5281/zenodo.20532770, 3 June 2026). The Zenodo record could not be fetched here. If the deposit differs, the edit set still applies to v2.1 as given.

*This file replaces the first version of B2_RESULT.md (commit 9b03eef). That version was written before the v2.1 source arrived, from the ledger's quotations of the note. Its replacement Theorem 2.1 text (old V3-4) is not needed, because v2.1 already has the correction.*

## Verification (explicit computation; no character table consulted)

PSL(2,7) is built as 2×2 matrices over 𝔽₇ modulo ±I (`b2_checks.py`). The note's own constructions are checked over 𝔽₂ in GL(3,2) (`b2_note_checks.py`).
- **ρ₈** is built explicitly as Ind_B^G(χ), with B the order-21 Borel subgroup and χ of order 3. It is irreducible (⟨χ,χ⟩ = 1), with character (8, 0, −1, 0, 1, 1) on 1A, 2A, 3A, 4A, 7A, 7B.
- **All 179 subgroups** are enumerated as two-generator closures.

| Check | Result |
|---|---|
| Fixed-subspace dimension of ρ₈ by class | 1A: 8, 2A: 4, 3A: 2, **4A: 2**, 7A: 2, 7B: 2 |
| Fixed set on S⁷ | 2A → S³ (21 elements); 3A, **4A**, 7A, 7B → S¹ (56 + **42** + 24 + 24 = **146** elements) |
| The v2.1 count | 104 = 146 − 42: the 4A class is omitted |
| Nesting | Fix(g) ⊂ Fix(g²) for g ∈ 4A, with g² ∈ 2A: each order-4 circle lies inside an involution's S³ |
| Maximal subgroups | **7:3** (one class of 8) and **S₄** (two classes of 7, exchanged by the outer automorphism) — as v2.1 states |
| D₄ | 21 subgroups of order 8, all D₄, each inside an S₄, none maximal — as v2.1 states |
| n₁(H; ρ₆) | S₄: 1 (both classes); 7:3: 0 — Theorem 2.3 of v2.1 holds |
| Lemma 2.5 (v2.1) | g₁, g₂ fix P₁; orders 2, 4, and g₁g₂ of order 3; \|⟨g₁, g₂⟩\| = 24 |
| Appendix A (v2.1) | h₁, h₂ fix P₁ and preserve L₁₂₄; h₁h₂ has order 4; ⟨h₁, h₂⟩ ≅ D₄ |
| Full group Laplacian, generating set 2A | ρ₁: 0, ρ₆: 2/3, ρ₈: 1, ρ₇: 8/7, ρ₃ and ρ₃′: 4/3; so δ = 10/21 is ρ₇ − ρ₆, while the next eigenvalue above 2/3 is ρ₈'s (gap 1/3) |

These agree with the audit reviewer's independent ρ₈ build (fixed dimensions 4/2/2/2 for orders 2/3/4/7).
- **Why one leg suffices.** The items correct a count in an open problem, a description of the literature and citations. None downgrades a result. Under the brief's proportionality rule they are annotations.

## The v3 draft: edits to v2.1

`v3_draft/make_v3_tracked.py` applies ten anchored edits to the run-merged `word/document.xml` of v2.1. Each anchor must match exactly once or the script stops. `build_v3.sh` reproduces the drafts from the source file (md5 checked) and validates the result against the original with the author check: "Paragraphs: 203 → 210 (+7) / All validations PASSED!". `v2_1_to_v3_text.diff` is the plain-text difference.

| Edit | Where | Change |
|---|---|---|
| E1 | Date line | "revised May 2026" → "revised May 2026 and October 2026" |
| E2 | Abstract, end | Adds one sentence. The statements of Theorem 2.3 and Lemmas 2.8–2.9 are classical: the action on seven cosets is 2-transitive, so (G, S₄) is a Gelfand pair, and the distance-transitive representations of PSL₂(q) ◁ G ≤ PΓL₂(q) are classified [15]. |
| E3 | New paragraph "Prior art", before "Conventions." | Explains each spectral statement as a classical fact. Lemma 2.8 is the 2-transitive permutation character; Lemma 2.9 is Schur's lemma; 2/3 is the central character of 2A on ρ₆. Cites [15, 16, 18]. Calls "spectral rigidity" and "spectral crystallization" descriptive names with no novelty claimed. |
| E4 | Open Problem 4.4 | Names the action (ρ₈ on S⁷ ⊂ ℝ⁸). Adds 4A and changes 104 → 146, with the nesting remark. Replaces the false sentence "Kawasaki … applies only to isolated singularities": the problem reduces to the G-equivariant index on S⁷ (Atiyah–Singer [13]); Kawasaki's V-manifold index theorem [17] and groupoid methods [9] treat it intrinsically; the η-invariant is the average over G of equivariant η-invariants [14], a finite sum not computed here. |
| E5 | Open Problem 4.1 | Adds the full-Laplacian eigenvalues and notes that δ = 10/21 skips ρ₈, so the h₂ = δ coincidence depends on choosing that difference. |
| E6 | AI declaration | Adds one sentence on the v3 revision. |
| E7 | Ref. [8] | Kawasaki (1978) → (1979); Osaka J. Math. 16 is the 1979 volume |
| E8 | Appendix A, first line | "We realize M₃ ≅ D₄" → "We realize D₄". In Theorem 2.1's table M₃ is S₄ = Stab(ℓ). |
| E10 | Proposition 4.2 statement | "any sphere Sₙ" → "any sphere Sⁿ" (the proof already has Sⁿ) |
| E9 | References | Adds [13] Atiyah–Singer III (1968); [14] Donnelly, Eta invariants for G-spaces (1978); [15] Faradžev–Ivanov (1990); [16] Inglis–Liebeck–Saxl (1986); [17] Kawasaki, V-manifolds (1981); [18] Praeger–Saxl–Yokoyama (1987) |

**Citation scope.** Faradžev–Ivanov and Praeger–Saxl–Yokoyama are described by what their titles and the standard literature say they do: a classification and a reduction theorem. Inglis–Liebeck–Saxl is described only as having *studied* multiplicity-free permutation representations of finite linear groups. A later seminar abstract by van Bon (TU/e) presents the determination of all primitive multiplicity-free permutation representations of the finite classical groups as a joint project with Saxl and Inglis, so "determined" would overclaim. The bibliographic data are the ledger's V4.45 record, verified there against five sources.

**Left for the author.**
- **Title.** V4.45 called "spectral rigidity" a name for Schur's lemma and "crystallization" a name backed by no theorem. E3 says so in the text. Retitling is the author's call.
- **Optional extra citation.** van Bon–Cohen, *Linear groups and distance-transitive graphs*, Eur. J. Combin. 10 (1989), for PSL(n,q). The end page is 412 in the ledger and 411 in one bibliography; check it before use.
- **Deposit.** v3 would go to Zenodo as a new version of the same record. That is the author's action, after approval.

## Ledger annotations for the Phase B fold (V4.92 line numbers)

| Line | Text | Bracket |
|---|---|---|
| L313 (§1.1 heading) | "SUBMISSION READY" | Stale; see L349. |
| L315 (§1.1 Theorem 2.1 and its n₁ list) | "S₄ is the unique maximal subgroup H …", with an n₁(D₄) line | Superseded in the note: v2.1 (revised May 2026) lists the maximal subgroups as two S₄ classes (n₁ = 1 each, exchanged by the outer automorphism) and 7:3 (n₁ = 0), and calls D₄ the non-maximal Sylow 2-subgroup (Remark 2.2). This ledger copy predates v2.1. Checked by explicit computation (B2). |
| L349 (§1.1 Paper status) | "Submitted to Journal of Algebra (JALGEBRA-D-26-00651) …" | Stale. Per the V4.45 record the submission route ended at *Finite Fields Appl.* (FFA-26-260), declined without referee reports after transfer from *J. Algebra*. The note rests as the Zenodo deposit (v2, DOI 10.5281/zenodo.20532770). A v3 is drafted (B2), not deposited. |
| L1069 (§2.85 addendum, step (i)) | "3A, 7A, 7B → S¹ codim 6, 104 elements" | 146 elements, not 104: the 42 elements of 4A also fix circles (ρ₈ fixed dimensions 4/2/2/2 for orders 2/3/4/7), nested inside the S³ of their squares. The identification of the action as ρ₈ is unchanged. Corrected in the v3 draft of the note. |

The As-of lines L3 and L32 repeat "104 elts". They are historical logs and are not touched. The project description's "submitted to JCT-A" and the Framework Index's "Submitted to Journal of Algebra" are stale too. Both live outside the ledger, in the project settings and the store.

**Blast radius.** No entry depends on the 104 count or on D₄'s maximality. §2.85's identification of the action as ρ₈ (and the bosonic, w₂ = 0 conclusion drawn from it) uses the character of ρ₈, which is unchanged. The corrections are annotations.

## Files

| File | md5 |
|---|---|
| `b2_checks.py` | `1328e291b2be8a4de8acb8ba4010b295` |
| `b2_output.txt` | `e9cee8674675f1f40cf5605f4ad59e0d` |
| `b2_results.json` | `6962cf8d8b46128c149077448153e569` |
| `b2_note_checks.py` | `c78beea7d12b038d16f801ed1b569f63` |
| `b2_note_checks_output.txt` | `5a030ff7782c7fcc6f0a75c1ab3d1432` |
| `v3_draft/source/PSL27_Spectral_Rigidity_corrected_v2_1.docx` (the author's file, byte-exact) | `9e80932408379a1c44813c56afa0327b` |
| `v3_draft/make_v3_tracked.py` | `417bc80d1e6594453e3f4d9dd30ccd50` |
| `v3_draft/build_v3.sh` | `a59c3015e5a0e09ee1fd7280d00b2429` |
| `v3_draft/build_log.txt` | `cfc22c8ce6a20e3c7a09eb318ca31dd9` |
| `v3_draft/PSL27_v3_DRAFT_tracked.docx` (its `word/document.xml`: `f667eaf71e53c1e42be1566e5e574271`) | `d56ac33c70669cfadff97b0b3c23b2d6` |
| `v3_draft/PSL27_v3_DRAFT_clean.docx` | `3cd28e9d55e4bc6440c9c3f22b1fff5a` |
| `v3_draft/PSL27_v3_DRAFT_tracked.pdf` | `4c60c5fc365ba51a0fee162a55c94458` |
| `v3_draft/PSL27_v3_DRAFT_clean.pdf` | `0de99189ef1691e123c9978131ea494b` |
| `v3_draft/v2_1_to_v3_text.diff` | `fecd2847c19293d6cc27bd6d0352a2b7` |

The .docx files are zip archives, so a rebuild gives a different archive md5 but the same `word/document.xml` md5. That was checked with two independent rebuilds.
