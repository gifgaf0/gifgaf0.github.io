# B2 — PSL(2,7) Zenodo note: checks and v3 change set (DRAFT)

**Plain-language summary.** The PSL(2,7) note on Zenodo (v2, DOI 10.5281/zenodo.20532770) is mathematically right where it matters, but it needs a third version for four reasons.
- **It does not cite the classical literature** that already contains its main results. The results are textbook facts about a well-studied group action, a "Gelfand pair", and three papers from 1986–1990 classify exactly these actions.
- **One open problem miscounts.** It lists 104 group elements whose fixed set on the 7-sphere is a circle; the true number is 146. The 42 elements of order 4 were left out.
- **One proof checks the wrong list of subgroups.** It includes D₄, which is not a maximal subgroup, and it calls S₄ "unique" when there are two non-conjugate copies; one symmetry of the group swaps them.
- **The status line is out of date.**

Below are exact replacement texts for a v3. Nothing is published; the author approves any Zenodo version.

**What could not be done here.** The v2 text is not in the project store, and fetching the Zenodo record needs the author's permission (requested October 7). So the replacements below are written against the ledger's quotations of v2 (§1.1, L313–L349, and the §2.85 addendum, L1069). They must be matched to v2's exact sentences before a v3 is assembled. Given the v2 source, a full v3 with an anchored edit script, like B1's, takes one step.

## Verification (explicit computation, `b2_checks.py`; no character table consulted)

PSL(2,7) is built as 2×2 matrices over 𝔽₇ modulo ±I.
- **The action on S⁷.** ρ₈ is built explicitly as Ind_B^G(χ), with B the order-21 Borel subgroup and χ of order 3. It is irreducible (⟨χ,χ⟩ = 1), and its character is (8, 0, −1, 0, 1, 1) on 1A, 2A, 3A, 4A, 7A, 7B.
- **All 179 subgroups** are enumerated as two-generator closures.

| Check | Result |
|---|---|
| Fixed-subspace dimension of ρ₈ by class | 1A: 8, 2A: 4, 3A: 2, **4A: 2**, 7A: 2, 7B: 2 |
| Fixed set on S⁷ | 2A → S³ (21 elements); 3A, **4A**, 7A, 7B → S¹ (56 + **42** + 24 + 24 = **146** elements) |
| The v2 count | 104 = 146 − 42: the 4A class is omitted |
| Nesting | Fix(g) ⊂ Fix(g²) for g ∈ 4A, with g² ∈ 2A: each order-4 circle lies inside an involution's S³ |
| Maximal subgroups | **7:3** (one class of 8) and **S₄** (two classes of 7, exchanged by the outer automorphism, conjugation by diag(3,1) ∈ PGL(2,7)) |
| D₄ | 21 subgroups of order 8, all D₄, each inside an S₄, **none maximal** |
| n₁(H; ρ₆), with χ₆ = (permutation character on S₄-cosets) − 1 = (6, 2, 0, 0, −1, −1) | S₄: 1 (both classes); 7:3: 0; D₄ (not maximal): 2 |
| L²(G/D₄) | ρ₁ ⊕ 2ρ₆ ⊕ ρ₈ (dimension 21), as the ledger's §1.1 table says |

These agree with the audit reviewer's independent explicit ρ₈ build (fixed dimensions 4/2/2/2 for orders 2/3/4/7), and with the ledger's own character arithmetic in §1.1.
- **Why one leg suffices.** These items correct a count in an open problem and the scope of a proof; none downgrades a result. Under the brief's proportionality rule they are annotations, verified once here and once by the reviewer.

## v3 change set

Each item gives the replacement text. Bracketed notes are for the author and are not part of the text.

**V3-0. Title vocabulary (author's decision).** V4.45 flagged it: "'spectral rigidity' = Schur's lemma, 'crystallization' = a name backed by no theorem in the paper." Either retitle, or add to the abstract: "The terms *spectral rigidity* and *crystallization* name Schur's lemma on a multiplicity-free (Gelfand-pair) action; no further theorem is attached to them."

**V3-1. Revision note (new, at the top).**
> *Version 3 (October 2026).* Adds the classical literature that already contains the results of Sections 2 and 3 (new paragraph "Prior art"; Inglis–Liebeck–Saxl 1986, Praeger–Saxl–Yokoyama 1987, Faradžev–Ivanov 1990). Corrects Open Problem 4.4: the elements whose fixed set on S⁷ is a circle are the classes 3A, 4A, 7A and 7B, 146 elements; version 2 listed 3A, 7A and 7B (104 elements) and omitted the 42 elements of order 4, whose fixed circles lie inside the 3-spheres fixed by their squares. Corrects the proof of Theorem 2.1: the maximal subgroups of PSL(2,7) are two conjugacy classes of S₄, exchanged by the outer automorphism, and one class of 7:3; D₄, which version 2 also checked, is a Sylow 2-subgroup contained in S₄ and is not maximal. Updates the status line.

**V3-2. Prior art (new paragraph, end of the introduction).**
> **Prior art.** The results of Sections 2 and 3 are instances of classical facts. PSL(2,7) acts 2-transitively on the seven cosets of S₄ (the points, or the lines, of the Fano plane), so the permutation character is 1 + χ₆ and (PSL(2,7), S₄) is a Gelfand pair; the isotypic rigidity of Lemma 3.5, and the eigenvalue 2/3 of the involution graph, are Schur's lemma for this rank-2 action (the class sum of the 21 involutions acts on ρ₆ as the scalar 21·χ₆(2A)/χ₆(1) = 7). The multiplicity-free permutation representations of the finite linear groups were determined by Inglis, Liebeck and Saxl [ILS86]. Praeger, Saxl and Yokoyama [PSY87] reduced the classification of primitive distance-transitive graphs to the almost simple and affine cases, and Faradžev and Ivanov [FI90] classified the distance-transitive representations of the groups G with PSL₂(q) ◁ G ≤ PΓL₂(q). This note records the case q = 7 in spectral language and claims no novelty for those statements.

**V3-3. References to add.**
> [FI90] I. A. Faradžev and A. A. Ivanov, Distance-transitive representations of groups G with PSL₂(q) ◁ G ≤ PΓL₂(q), *European J. Combin.* 11 (1990) 347–356.
> [ILS86] N. F. J. Inglis, M. W. Liebeck and J. Saxl, Multiplicity-free permutation representations of finite linear groups, *Math. Z.* 192 (1986) 329–337.
> [PSY87] C. E. Praeger, J. Saxl and K. Yokoyama, Distance transitive graphs and finite simple groups, *Proc. London Math. Soc.* (3) 55 (1987) 1–21.

[Optional, also in the V4.45 record: J. van Bon and A. M. Cohen, Linear groups and distance-transitive graphs, *European J. Combin.* 10 (1989) 399–41x. The end page is 412 in the ledger and 411 in one bibliography; check it before use.]

[Sources: the ledger's V4.45 record, verified there against five sources, plus the bibliography of arXiv:2110.13794 for PSY87's title and pages.]

**V3-4. Theorem 2.1, statement and proof** (replaces v2's; the ledger's quote of v2: "S₄ is the unique maximal subgroup H of PSL(2,7) satisfying n₁(H; ρ₆) = 1 and containing a 3-dimensional cubic irrep", with proof lines for S₄, Z₇ ⋊ Z₃ and D₄).
> **Theorem 2.1 (S₄ uniqueness).** Up to automorphisms of PSL(2,7), S₄ is the unique maximal subgroup H of PSL(2,7) satisfying n₁(H; ρ₆) = 1 and containing a 3-dimensional cubic irrep.
>
> *Proof.* The maximal subgroups of PSL(2,7) form three conjugacy classes: two classes of S₄, the stabilizers of the points and of the lines of the Fano plane, exchanged by the outer automorphism; and one class of 7:3 = Z₇ ⋊ Z₃. For either class of S₄, n₁(S₄; ρ₆) = (6 + 9·2 + 8·0 + 6·0)/24 = 1. For 7:3, n₁ = (6 + 14·0 + 6·(−1))/21 = 0. ∎
>
> *Remark (v3).* Version 2 also evaluated n₁(D₄; ρ₆) = (6 + 5·2 + 2·0)/8 = 2. D₄ is a Sylow 2-subgroup, contained in S₄, and is not maximal, so that case is not part of the proof. The second condition in the statement is implied by the first among maximal subgroups.

**V3-5. Open Problem 4.4, strata sentence** (replaces v2's; the ledger's quote: "2A → S³ (codim 4); 3A, 7A, 7B → S¹ (codim 6, 104 elements); 4A nested").
> Under the 8-dimensional irreducible representation ρ₈, every non-identity element has a fixed set on S⁷. Each of the 21 involutions (class 2A) fixes a 3-sphere (codimension 4). Each of the 56 elements of order 3, the 42 of order 4 and the 48 of order 7 (classes 3A, 4A, 7A, 7B; 146 elements) fixes a circle (codimension 6), and the circle fixed by an element of order 4 lies inside the 3-sphere fixed by its square. *(Corrected in v3: version 2 listed 3A, 7A and 7B, 104 elements.)*

[The rest of Open Problem 4.4, the question itself, stays as in v2.]

**V3-6. Status line.** If v2 carries a submission status, replace it with:
> *Status (October 2026): Zenodo deposit, version 3. Not under journal review.*

[The submission history (JCTA → *J. Algebra* JALGEBRA-D-26-00651 → *FFA* FFA-26-260, declined without referee reports) belongs in the ledger, not the note.]

## Ledger annotations for the Phase B fold (V4.92 lines)

| Line | Text | Bracket |
|---|---|---|
| L315 (§1.1 Theorem 2.1) | "S₄ is the unique maximal subgroup H …" | D₄ is not maximal: it is a Sylow 2-subgroup inside S₄. The maximal subgroups are two S₄ classes (n₁ = 1 each, exchanged by the outer automorphism) and 7:3 (n₁ = 0), so "unique" holds up to automorphism. The n₁(D₄) line is not part of the proof. v3 is drafted. |
| L349 (§1.1 Paper status) | "Submitted to Journal of Algebra (JALGEBRA-D-26-00651) after desk rejection from Discrete Mathematics" | Stale. The paper went JCTA → *J. Algebra* → FFA (FFA-26-260) and was declined at all three (V4.45). Its resting place is the Zenodo note (v2, DOI 10.5281/zenodo.20532770). The heading's "SUBMISSION READY" is stale with it. v3 is drafted. |
| L1069 (§2.85 addendum, step (i)) | "3A, 7A, 7B → S¹ codim 6, 104 elements" | 146 elements, not 104: the 42 elements of 4A also fix circles (ρ₈ fixed dimensions 4/2/2/2 for orders 2/3/4/7), nested inside the S³ of their squares. The identification of the action as ρ₈ is unchanged (4A's S¹ is consistent with ρ₈). |

The As-of lines L3 and L32 repeat "104 elts"; they are historical logs and are not touched. The project description's "submitted to JCT-A" and the Framework Index's "Submitted to Journal of Algebra" are stale too; they live outside the ledger (store and project settings).

## Files

| File | md5 |
|---|---|
| `b2_checks.py` | `1328e291b2be8a4de8acb8ba4010b295` |
| `b2_output.txt` | `e9cee8674675f1f40cf5605f4ad59e0d` |
| `b2_results.json` | `6962cf8d8b46128c149077448153e569` |
