# Gauge paper, close-out fixes to the v6.4 draft (Step 2a)

**Plain-language summary.** The Phase B draft v6.4 of the gauge paper gains three corrections and a shorter title. It is still v6.4, because v6.4 was never released. The changes:
- the quaternions' automorphism group is SO(3), not SU(2);
- the spin-structure paragraph (Section 7.4) is turned the right way round;
- the uniqueness of the seven-vertex torus is credited to its classical source.

Every other line is unchanged, and removing the new hunks gives back the Phase B draft byte for byte. Nothing is published or deposited. There is no editor letter, because the paper is not under review (the author's F1).

| Item | Value |
|---|---|
| Source | `phase_b/B1/v6_4_draft/Gifford_Csaszar_Gauge_Group_v6_4_2026_DRAFT.md`, md5 `afbbf56dc1f0b5573d8beb1431555567` |
| Result | `Gifford_Csaszar_Gauge_Group_v6_4_2026_CLOSEOUT_DRAFT.md`, md5 `87278ffcd8d19fccab3ff97971c4ddce` (50,350 → 52,639 B) |
| Script | `edit_v6_4_closeout.py`. It checks that every hunk lands exactly once, that the reverse splice is exact, that the references run 1–27 in order, and that the old statements are gone (`edit_output.txt`) |
| Version note | `ZENODO_VERSION_NOTE_v6_4.md`: one paragraph for Zenodo, in plain terms |

## Hunks

| Hunk | Where | Change |
|---|---|---|
| K1 | Title | "Gauge Group, Generation Structure, Hypercharge, and Quark Mixing from the Császár Polyhedron" → **"Gauge Group and Generation Structure from the Császár Polyhedron"** (the F6 default) |
| K2 | v6.4 revision note | Items (v)–(viii) added; the reference count is now 1–27 |
| K3 | Section 2 | The 7-vertex torus is unique up to isomorphism, which is classical: Möbius (1886), with the enumeration in Lutz (2008). A neighborly torus triangulation has exactly 7 vertices, so it is also the only neighborly one. Bokowski & Eggert (1991) are now cited for what their title says, all realizations in ℝ³ |
| K4 | Section 3 | Aut(ℍ) ≅ SO(3). The unit quaternions, Sp(1) ≅ SU(2), act by conjugation with kernel {±1}. The weak-group claim is now attached to this double cover, not to Aut(ℍ) |
| K5 | Section 4 | Same correction ("each carrying its own unit-quaternion group Sp(1) ≅ SU(2)") |
| K6 | Section 7.1 | Same correction, in the conjecture paragraph on the weak SU(2). This is outside the brief's list (§3, §4, (xi)), but it is the same sentence, so it is fixed for consistency |
| K7 | Section 7.4 | The induced spin structure is even (Arf 0): antiperiodic around two of the three nonzero classes of H₁(T²; ℤ₂) and periodic around one. The all-periodic structure is the odd one (Arf 1), and no embedding induces it. The section's conclusion, that the embedding fixes a single spin structure, stands. Which class carries the periodic condition for the Császár embedding is not stated, because that would be a new computation |
| K8 | Open Problem (xi) | The diagonal action is that of Sp(1)₁ × Sp(1)₂ × Sp(1)₃, not Aut(ℍ₁) × Aut(ℍ₂) × Aut(ℍ₃) |
| K9 | References | Lutz (2008) [23] and Möbius (1886) [24] inserted alphabetically; [23]–[25] become [25]–[27] |

## Sources for the fixes

- **SO(3) and SU(2).** This is standard: the conjugation map Sp(1) → Aut(ℍ) is onto SO(3), and its kernel is {±1}. The paper's own Section 7.5 already uses the 2:1 cover SU(2) → SO(3).
- **The spin structure.** The brief states the correct version. The induced quadratic form on H₁(T²; ℤ₂) takes the value 1 on exactly one nonzero class. A closed surface in ℝ³ bounds a region of ℝ³ over which the spin structure extends, so its Arf invariant is 0.
- **Uniqueness.** Lutz (2008, Table 2) lists exactly one triangulated torus with 7 vertices. It credits the 7-vertex torus to Möbius (1886) as a minimal and combinatorially unique triangulation that was "already known in the 19th century". The full citation is checked against the arXiv text (math/0506316) and the book's table of contents (Discrete Differential Geometry, Oberwolfach Seminars 38, Birkhäuser 2008, from p. 235).
