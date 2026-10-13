# Gauge paper v6.4: the final pass (October 13, 2026)

**Plain-language summary.** A last careful read of the close-out draft found a set of small errors. All are fixed, and none changes a conclusion, a number or a reference entry.
- **What was fixed.**
  - Section 6 skipped a number.
  - Three places called 3/13 a *topological* invariant. It depends on the triangulation, so it is a *combinatorial* one.
  - The one theorem was stated for the groups. It is proved for the Lie algebras, and it is false for the groups.
  - A straight edge was given a Frenet–Serret frame, which it does not have.
  - The complex structure of a torus was said to be fixed by its topology. It is fixed by its geometry.
  - Two places said the rank-4 problem is "resolved", although the abstract and Section 9 leave it open.
  - The |V_cb| comparison value was not labelled as PDG 2022's.
  - One reference was listed but never cited.
  - Some formatting was broken.
- **What was left alone.** Ten points need the author's judgment, or a new derivation, so they are listed below and the text is unchanged.
  - The most serious is J1. The paper's color SU(3) mixes its three "generations", because the three Fano lines through a vertex are the three color directions. This bears on verified claim (2).
  - The next is J2. Section 6.2 labels generations differently from Sections 4 and 6.
- **The PDF.** It is built from the corrected text, and its text layer is checked against the Markdown.
- **Checks.** An independent check confirmed the fixes, the mathematics behind them and the PDF, and it found J1, J4, J6 and part of J8.
- **Status.** The v6.4 revision note records the fixes as item (ix). Nothing is deposited, committed or pushed.

| Item | Value |
|---|---|
| Source | `Gifford_Csaszar_Gauge_Group_v6_4_2026_CLOSEOUT_DRAFT.md`, md5 `87278ffcd8d19fccab3ff97971c4ddce` |
| Result | `Gifford_Csaszar_Gauge_Group_v6_4_2026_FINAL.md`, md5 `f24dcc37690a7d2083fba3eb590bba8a` (52,639 → 54,151 B) |
| Script | `edit_v6_4_final_pass.py`. It checks that every anchor is unique and lands exactly once. It also checks that undoing the 31 replacements gives the close-out draft byte for byte, and that the targeted statements are gone. It confirms that the reference list is unchanged (1–27) and that every reference is cited in the main text (`final_pass_output.txt`) |
| PDF | `Gifford_Csaszar_Gauge_Group_v6_4_2026.pdf`, md5 `d1b8507a5efe0c67edd4c6178c3c61d9`, 14 pages, US Letter |
| Build | `build_v6_4_pdf.py` with `pdf_filter.lua` (`build_pdf_output.txt`) |
| Version note | `ZENODO_VERSION_NOTE_v6_4.md` gains one sentence on the final pass |

## Fixes

| Hunk | Where | Change and reason |
|---|---|---|
| P1 | Section 6 | The subsections were 6.1, 6.3, 6.4, because the old 6.2 became a note in v5. They are renumbered 6.1–6.3. Nothing in the paper, the repository or the ledger cites the old numbers |
| P2 | Section 5 | "confined to (a) the identification…" had no "(b)", which was the sign dressing withdrawn in v6.4. The "(a)" is removed |
| P3 | Sections 6.1, 9 | The \|V_cb\| value 0.0408 ± 0.0014 is PDG 2022's. Next to the PDG 2024 numbers of Section 6.1, "the PDG value" read as PDG 2024's, so it is now labelled "PDG 2022" in both places. The PDG 2024 value is not quoted, because it was not confirmed here |
| P4 | Section 7.5, Open Problem (i) | The edges are straight segments (Section 7.1), so their curvature is zero and they have no Frenet–Serret frame: the principal normal is undefined. The frame is now "an adapted orthonormal frame: the unit tangent T, a chosen unit normal N, and the binormal B = T × N". T, N and B are vectors, so "four real quantities" becomes "four quantities", and "Frenet-framing fibre" becomes "edge-framing fibre" |
| P5 | Sections 7, 12 | "We resolve it" and "is resolved by" become "address" and "is addressed by". The abstract already says "addressed", and Section 9(4) says the commutativity of the three actions "is not claimed here as established" (Open Problem (i)). The heading "The Rank-4 Resolution" is left (see J10) |
| P6 | Sections 6.1, 9, 12 | 3/13 and its two integers are a "combinatorial", not a "topological", invariant. The rank of ∂₂ is F − 1, the face count minus one, so a different triangulation of the same torus gives a different number (a 9-vertex torus, with 18 faces, gives 17). "(determined by the homology of the torus)" becomes "(fixed by the face count and the homology of the torus)", which is the paper's own computation, 14 − 1 |
| P7 | Eleven run-in labels | "**Label. **Text" becomes "**Label.** Text". Markdown does not close a bold span after a space, so these would print with stray asterisks |
| P8 | Section 2 | "V = 7 (Heawood bound)" becomes "(the Heawood bound; Heawood 1890, Ringel & Youngs 1968)". Ringel & Youngs [27] was listed but cited nowhere, and Heawood [20] was cited by name only |
| P9 | Abstract, Sections 7.3, 9(4) | "The centralizer of color SU(3) in G₂ is trivial" becomes "the centralizer of color su(3) in g₂ is trivial". The group statement is false: the center of SU(3), {1, ω, ω²} with ω = e^{2πi/3}, lies in G₂ and commutes with SU(3). The Lie-algebra statement is what the paper proves (no trivial summand in 𝟖 ⊕ 𝟑 ⊕ 𝟑̄; the computed centralizer in g₂ has dimension zero), and it is all the conclusion needs, since a weak factor would be a connected group. The v6 revision note keeps its wording, as the record of that version |
| P10 | Section 7.1 (Stratum 2) | "determined by the surface topology" becomes "determined by the surface geometry". Tori of the same topology carry different complex structures: the square torus and the equilateral one are not conformally equivalent. Which geometry the paper means is J4 |
| P11 | Section 7.2 | "der(W) ⊂ tri(W)" used W without saying what it is. It now reads "for a normed division algebra W, der(W) ⊂ tri(W)…" |
| P12 | v6.4 revision note | Item (ix) lists P1–P6 and P8–P11 in plain terms |

## Not changed: for the author

Each of these would change an argument or need a derivation, or is a matter of wording that the author asked to leave. They are in order of weight.

- **J1. Color mixes the three generations (Sections 3, 4, 9(2)).**
  - Color SU(3) is the stabilizer of e₀, acting complex-linearly on the six other units with J = L_{e₀}.
  - Each generation algebra ℍᵢ = span{1, e₀, a, J(a)} is fixed by a complex line of that ℂ³. The three Fano lines through e₀ give the three coordinate lines {e₁, e₃}, {e₄, e₅}, {e₂, e₆}.
  - SU(3) moves these lines into one another. Only its maximal torus, of dimension 2, keeps all three (computed). So the three "generations" are the three color directions, and color mixes them.
  - This conflicts with verified claim (2) and with Section 4. Section 7.2's "Relabeling a vertex (SU(3)) permutes the octonion assignments" and Section 7.3's "The abstract K₇ graph has G₂ symmetry on its vertices" share the problem: G₂ and SU(3) act linearly on ℝ⁷ and do not permute the seven vertices.
- **J2. Section 6.2 (was 6.3): the generation labels.**
  - The section labels the up-type vertices e₁, e₂, e₃ as Generations 1–3.
  - Sections 4 and 6 instead make each generation a Fano⁺ line through v₀, so e₁ and e₃, on the line {e₀, e₁, e₃}, are one generation.
  - J = L_{e₀} maps each Fano⁺ doublet to itself: e₁ ↔ e₃, e₄ ↔ e₅, e₂ ↔ e₆. Under Section 6's labels it therefore couples no two generations.
  - It also takes e₂, an up-type vertex, to e₆, a down-type one, so it does not act within the up-type triple as "restricted to" suggests.
  - The hierarchy |V_us| > |V_cb| > |V_ub| is stated without a computation.
- **J3. Sections 7.1 and 7.5: the size of the frame group.** Holding an edge fixed, its frame can only turn about the edge. Those rotations form SO(2), not SO(3), and the SU(2) attached to edge framings rests on SO(3).
- **J4. Which complex structure (Sections 6.1, 7.1, 7.3; Open Problem (iii)).**
  - The paper gives the Császár torus the modulus ρ = e^{iπ/3}. That is the modulus of the torus built from equilateral triangles.
  - The polyhedron in ℝ³ cannot have equilateral faces, since its seven vertices would be pairwise equidistant. The complex structure that the embedding induces, which Section 7.3 says the U(1) acts on, is a different one and depends on the coordinates.
  - The paper should say which structure it means.
- **J5. Section 7.2.** "Rotating the surface phase (U(1)) changes the complex structure." A U(1) phase rotation commutes with the complex structure and leaves it unchanged.
- **J6. Open Problem (i)(a).** It says that deciding whether the framed-edge bundle is trivial "is exactly Open Problem (ii)". But (ii) is the obstruction that distinguishes the two enantiomers, which is not evidently the same question. The reduction dates from v6.
- **J7. Section 8.** "No rotational axes". The combinatorial argument excludes mirror planes, centers and rotoreflections, not rotations. Whether some realization has a rotation axis is the item left open in Phase B.
- **J8. The abstract.**
  - It says the polyhedron encodes the gauge group "through its combinatorial topology". Section 7.3 says the SU(2) and U(1) act on data that "exists only because the Császár polyhedron is embedded in ℝ³".
  - "No free parameters are introduced" sits uneasily with two things: the observable for 3/13 (tan θ_C) was chosen after the data, and the φ in |V_cb| is unexplained.
- **J9. Sections 9 and 12.** Section 9 heads its list "Verified claims", and Section 12 calls the same three items "verifiable results".
- **J10. Headings.**
  - Section 5, "Hypercharge from Fock Space Grading", names Furey's mechanism, while the section's own content is now only the cycle identification.
  - Section 7 is still headed "The Rank-4 Resolution".

## The PDF

- **Toolchain.** pandoc 3.1.3 → XeLaTeX (TeX Live 2023), FreeSerif 11 pt. Fancy lists, superscripts, subscripts, TeX math and raw TeX are off, so "(i)", "(−1)^(N+1)", "e_i" and "e^{iπ/3}" print as written.
- **Typography.** pandoc sets straight quotes as curly ones and the "..." of {e₁, ..., e₇} as "…".
- **Layout.** The first five paragraphs become a centered title block. The three one-line italic formulas (Q = N/3, 3/13 = 0.23077, rank(∂₂) = …) are centered. A space after "Section", "Problem" or "Conjecture" before a number or "(" does not break.
- **Glyphs.**
  - FreeSerif's bold and italic faces lack ℂ ℍ ℝ ℤ 𝔽 𝕆 𝕊 𝟏 𝟑 𝟕 𝟖, so these are set from the upright face.
  - FreeSerif has no mark anchor for digits, so a combining macron after a digit sat inside it, and 3̄ printed as 3. The macron is now raised above the digit. It stays a real character, so 3̄ still copies as 3̄.
- **Checks.**
  - Two builds in separate directories are byte-identical (SOURCE_DATE_EPOCH = 2026-10-13T00:00:00Z).
  - There are no missing glyphs, overfull lines or undefined references.
  - One line in reference [23] is set loose.
  - The PDF's text layer equals the Markdown's once markup, page numbers, whitespace and hyphens are removed, the quotes and the ellipsis are put back in plain form, and both are in Unicode NFC.
  - Every page was inspected, and all 16 barred 3s show the bar.
