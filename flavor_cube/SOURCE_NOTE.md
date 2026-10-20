> **Provenance.** This note was pasted into a Claude Code session on October 20, 2026, as the source for the Flavor Cube page (`flavor_cube/index.html`). It is copied here verbatim so the page's citations resolve. The script it cites, `claude/sqt_geometric_operators.py`, is not in this repository; `flavor_cube/check_geometry.py` recomputes the statements the page uses, and `flavor_cube/crosscheck/` holds an independent second computation.

# Exploration: geometric fermion operators at a vertex, and the Rubik's cube (October 19, 2026)

**Status.** Exploration, mathematics only. Nothing here reopens the closed substrate program or the gauge paper's physics. It answers one question from chat: can the seven-vertex torus supply fermion operators of its own, beyond the ones Furey's construction already gives?

**Plain-language summary.**
- At the fixed vertex v₀ the six neighbours can be paired symmetrically in exactly three ways: across the three up-triangles, across the three down-triangles, or straight through v₀ along the three Hamiltonian cycles. Each pairing gives a working set of three fermion modes, so anticommutation by itself costs nothing.
- Furey's modes are the up-triangle pairing: L_{e₀} pairs up-triangle partners, and her ladder operators pair the units on the three lines through e₇ (e₇ ≡ e₀ here). That is where her construction lives on the torus. The gauge paper's §4 put generations on these same lines and §5 put the modes on the cycles.
- The cycle modes are the torus's own preference: its 6-fold rotation about v₀ preserves only them. A 120° turn cycles the three modes; a 60° or 180° turn exchanges particles and holes.
- But cycle modes keep only an SU(2) of color (the part fixing the color direction r+g+b), and their vacuum is one quarter neutrino, three quarters up-quark states along r+g+b. The down-triangle modes fail the same way.
- The discrete color symmetry at v₀ (signed octonion automorphisms fixing e₀) is exactly Δ(96). The torus itself contributes only a ℤ₃ of it.
- Rubik's cube: the Fano plane's symmetries fixing v₀ act on its neighbours exactly as a cube's tetrahedral group (rotations plus mirrors) acts on its faces. Furey's three colors become the three pairs of opposite faces, and the corner view puts them at the SU(3) weights. The cycles land on adjacent faces.

## Conventions

- Labels ℤ₇. Up-triangles (i, i+1, i+3) are the oriented Fano⁺ lines, with octonion rule e_i e_{i+1} = e_{i+3}. This is Furey's convention with 7 ≡ 0. Down-triangles (i, i+2, i+3) are the Fano⁻ lines.
- v₀ = 0. QR = {1, 2, 4}, QNR = {3, 5, 6}.
- For c ∈ QNR, J_c sends e_r ↦ e_{cr} and e_{cr} ↦ −e_r (r ∈ QR).
- Annihilators a_J(v) = ½(γ(v) + iγ(Jv)) from Majoranas γ on ℝ⁶ = e₀^⊥.
- Furey's color basis is z_k = e_{r_k} + i e_{3r_k}, with r_k = 1, 2, 4.

## Results

All computed by `claude/sqt_geometric_operators.py` (self-contained, numpy only). Independent recomputation: see Verification.

**R1. Three pairings.** Of the 15 perfect matchings of v₀'s neighbours, exactly 3 are invariant under the 120° rotation x ↦ 2x:
- J₃: the up-triangles; this equals L_{e₀};
- J₅: the down-triangles;
- J₆: the straight lines through v₀, i.e. the Hamiltonian cycles.

In the hexagonal picture the partners are 60°, −60° and 180° apart.

**R2. Rotations about v₀** (x ↦ ax; all are torus automorphisms).
- The 120° and 240° turns are octonion automorphisms and preserve J₃, J₅ and J₆.
- The 60°, 180° and 300° turns are not octonion automorphisms; they send J₃ ↦ −J₅ and J₆ ↦ −J₆.
- So J₆ is the only pairing invariant, up to sign, under the full rotation group.

**R3. Homology.**
- With quadratic-residue orientation, c₁ + c₂ + c₄ = ∂(Σ up-triangles) = ∂(Σ down-triangles).
- Each c_r is non-bounding, and any two are independent in H₁.
- Their directions are three unit vectors at 120° summing to zero, the shape of the color weight triangle.
- Every triangle has one edge in each cycle.

**R4. Finite color group.**
- There are 1344 signed automorphisms of the octonions, 8 per collineation.
- The 96 that fix e₀ are, in Furey's color basis, exactly the monomial 3×3 matrices with entries ±1, ±i and determinant 1. That group is Δ(96) = (ℤ₄×ℤ₄)⋊S₃, with element orders 1:1, 2:15, 3:32, 4:24, 8:24.
- The other 96, which send e₀ ↦ −e₀, are antilinear: the charge-conjugation coset.
- The part visible on the torus is a ℤ₃, the cyclic color permutation.

**R5. Color compatibility.**
- J₃ keeps all of su(3) (dimension 8) and all of Δ(96).
- J₅ and J₆ each keep a 3-dimensional su(2) and 3 elements of Δ(96).
- For J₆ that su(2) fixes the color vector (1,1,1) = e₁ + e₂ + e₄.

**R6. Fock spaces.**
- All three pairings give the canonical anticommutation relations with a unique vacuum, and all have Pfaffian +1, so they induce the same orientation.
- N_Furey and N_cycle do not commute.
- In Furey's basis the cycle vacuum is proportional to |000⟩ + |011⟩ − |101⟩ + |110⟩, and |⟨Ω_F|Ω_C⟩|² = 1/4. That is one quarter neutrino, three quarters up-quark states along r+g+b.
- The 120° turn preserves both number operators. The 60° and 180° turns send N_cycle ↦ 3 − N_cycle and N_Furey ↦ 3 − N_down.

**R7. Rubik's cube.**
- (a) Corner view.
  - Projected along a body diagonal, the face directions are exactly the SU(3) triplet and antitriplet weights.
  - The 6 symmetries fixing the corner (3 rotations, 3 mirrors) act as the Weyl group S₃.
  - Central inversion acts as charge conjugation.
- (b) Fano point-stabilizer.
  - The 24 Fano⁺ collineations fixing v₀ act on its neighbours as T_d acts on the cube's faces (48 bijections), not as O (none).
  - Under every such bijection, the up-triangle pairs go to opposite faces, the down-triangle and cycle pairs go to adjacent faces, and QR goes to three faces meeting at a corner.
- (c) Analogy only: a legal cube has total corner twist ≡ 0 mod 3, as color-neutral states have triality 0.

**R8. The same results on the Szilassi polyhedron (the dual).** The Szilassi polyhedron is the same torus with vertices and faces swapped: 7 hexagons, 14 corners, 21 edges.
- Each Császár edge separates one up- and one down-triangle. So the Szilassi skeleton is bipartite: it is the Heawood graph, the Fano incidence graph. Up-corners are the Fano⁺ lines and down-corners are the Fano⁻ lines.
- Consider the hexagon dual to v₀. Its six edges correspond to v₀'s neighbours, and its corners alternate up and down.
  - Furey's three colors are its three up-corners; each color's two real components are the two edges meeting there.
  - The down-triangle pairing is the other three corners.
  - The cycle pairing is opposite edges.
- Each Hamiltonian cycle becomes a straight belt of seven hexagons, entering and leaving each hexagon through opposite edges.
- Each up-corner touches three hexagons, so one Fano⁺ line is a color direction at each of its three points.
- The up- and down-pairings do not give six independent modes. Both use the same six Majoranas, and their number operators do not commute.

## What this means for the gauge paper's §5

The identification "three Fock modes = three Hamiltonian cycles" does not hold up:
- the operators it borrows from Furey sit on the up-triangles, the same Fano lines §4 uses for generations;
- a Fock space built on the cycles breaks color to SU(2).

## Novelty

- R1–R3, R5 and R6 are elementary statements I have not seen written down. None is a physics result.
- R4 was not found stated in a literature search, but it is elementary and plausibly known to people who study finite subgroups of G₂.
- R7(a) is classical. R7(b) identifies the specific action of a classical subgroup (the point stabilizer S₄ of PSL(2,7)).

## Next test for any new geometric operator

It must commute with Δ(96) (better, with color SU(3)) and reproduce Furey's charges. On the torus only the up-triangle pairing passes, and that one is Furey's.

## Verification

- **R1–R7: independently recomputed.** A separate leg rebuilt them from the stated claims alone, with its own code and exact integer or fraction arithmetic where possible, on October 19. All eight claim groups pass, 55 of 55 sub-checks.
  - The leg also found that the J₃–J₅ and J₅–J₆ vacuum overlaps are 1/4 as well.
  - In R7(b), which of the cube's two alternating corner sets QR lands on depends on the bijection (24 each way). Only "QR lands on a corner" is invariant.
- **R8: one computation.** The Szilassi picture was checked once and not recomputed independently.
- **Literature.** Furey's ladder operators (Charge quantization from a number operator, arXiv:1603.04078) pair the units on the lines through e₇, which matches J₃ in this labelling. A search did not find Δ(96) stated in connection with the octonions.
