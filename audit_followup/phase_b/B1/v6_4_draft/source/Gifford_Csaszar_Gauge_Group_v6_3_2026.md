**Gauge Group, Generation Structure, Hypercharge, and Quark Mixing**

**from the Császár Polyhedron**

Matthew Gifford

*Open Source Theoretical Research*

July 2026 — v6.3 (Revised)

*Revision note (v6.3): Attribution-completeness micro-revision; no equation, numeric value, claim, conjecture status, or open-problem content is changed. (i) The Section 11 differentiation paragraph now names the Cℓ(8) extension of the sedenion three-generation construction (Gourlay & Gresnigt 2024), completing the mechanism-family coverage of the July 2026 prior-art review, and the corresponding reference is added. (ii) A v6.2 reference-numbering defect is repaired: the final entry (Ringel & Youngs 1968) had retained its pre-v6.2 list number (13) outside the v6.2 renumbering, duplicating an existing label; it is renumbered to its alphabetical position (23). The reference list now runs 1–23. All technical content is unchanged from v6.2.*

*Revision note (v6.2): Attribution-only revision; no equation, numeric value, claim, conjecture status, or open-problem content is changed. Following a prior-art review against the Furey corpus (July 2026): (i) Section 5 now attributes the Fock-grading/number-operator hypercharge mechanism to Furey (2015; 2016; 2018a) and scopes this paper's contribution to the geometric identification of the three modes with the Hamiltonian 7-cycles of K₇ and, provisionally, the closed-form sign dressing; (ii) the canonical citation Günaydin & Gürsey (1973) is added for SU(3) as the G₂-stabilizer of an imaginary unit (Sections 1, 3, 7.3); (iii) Section 11 gains a differentiation paragraph naming the competing three-generation mechanisms and the principal algebraic alternatives on the rank-4 problem, with the novelty language of Sections 5 and 7 scoped accordingly; (iv) Section 8 gains a note differentiating Conjecture 1 from the algebraic parity-violation results of Furey (2018c) and Furey & Hughes (2022b); (v) Section 7.2 gains one attributed corroboration sentence from the triality identical-action theorem; (vi) nine references are added and the Furey 2018 entries are disambiguated as 2018a/b/c. All technical content is unchanged from v6.1.*

*Revision note (v6.1): Single-sentence correction to the abstract. The abstract previously stated "These act on independent tensor factors and commute by construction" — language inconsistent with the §7.2 body correction applied in v6. Replaced with a statement that (a) records the centralizer theorem from §7.3 as the proved negative result, and (b) names the tensor-product realization as Open Problem (i), consistent with the rest of the paper. No other content changed from v6.*

*Revision note (v6): v6 (i) corrects the Section 7.2 tensor-factorization argument — previously stated as automatic from the dimensional independence of the strata — to reflect that the cells of the Császár complex form a chain complex, not independent tensor factors, and that the edges carry a non-trivial color representation (Λ²(𝟕) = 𝟏 ⊕ 𝟖 ⊕ 𝟑 ⊕ 𝟑̄ ⊕ 𝟑 ⊕ 𝟑̄ as an su(3)-module); the factorization is now recorded as a requirement to be established. (ii) Adds to Section 7.3 the theorem that the centralizer of color SU(3) in G₂ is trivial (g₂ = 𝟖 ⊕ 𝟑 ⊕ 𝟑̄, no trivial summand; verified on Der(𝕆)), making rigorous the claim that no commuting weak factor exists inside G₂ and that the additional rank must be sourced externally. (iii) Restates Open Problem (i) as the establishment of a genuine tensor-product realization, shown to reduce to Open Problem (ii) or (xi)(b) according to how the weak SU(2) is realized, and removes the redundant bracket-computation framing; verifiable claim (4) is updated to match. The gauge-group construction, the three-generation and hypercharge derivations, and the Cabibbo-angle derivation are unchanged from v5.*

*Revision note: v5 adds an explicit quaternion algebra map for edge framings (Section 7.5), a conjecture paragraph on the left-handed coupling gap (Section 7.1), flags the 14 = 12 + 2 dimension count as a structural observation pending an explicit map (Section 7.3), condenses the V_cb material to a note (formerly Section 6.2), softens the Cabibbo physical interpretation to topological language (Section 6.1), and adds Open Problems (x) and (xi). The hypercharge derivation, gauge group construction, and Cabibbo angle derivation are substantively unchanged from v4.*

# **Abstract**

We show that the Császár polyhedron — the unique neighborly triangulation of the torus — encodes the Standard Model gauge group SU(3) × SU(2) × U(1), three fermion generations, correct hypercharge assignments, and the leading CKM quark mixing angle through its combinatorial topology. The construction proceeds in four stages: (i) G₂ = Aut(𝕆) acting on the K₇ vertex structure yields SU(3) via vertex stabilization; (ii) three generations arise from the three Fano lines through any vertex; (iii) hypercharge assignments follow from a Fock space grading of the three Hamiltonian cycles; (iv) the Cabibbo angle emerges as the ratio of the Fano valence to the rank of the boundary operator in the Császár triangulation.

The rank-4 problem — how the rank-4 gauge group SU(3) × SU(2) × U(1) arises from the rank-2 group G₂ — is addressed by showing that the three gauge actions operate on topological data of different dimension: SU(3) on vertex labels (0-cells), SU(2) on edge spin-framings (1-cells), and U(1) on the surface complex structure (2-cells). That no commuting weak factor exists inside G₂ itself is a theorem: the centralizer of color SU(3) in G₂ is trivial (g₂ = 𝟖 ⊕ 𝟑 ⊕ 𝟑̄ as an su(3)-module, containing no trivial summand), so the additional rank must be sourced externally. Whether the three geometric actions can be jointly realized on a common representation space as a genuine tensor product — which would ensure their commutativity identically — is a substantive open requirement recorded as Open Problem (i) in Section 10.

We further propose that the Császár polyhedron provides a geometric realization of the Dixon algebra ℂ ⊗ ℍ ⊗ 𝕆, with the 0-dimensional vertices carrying 𝕆, the 1-dimensional edge framings carrying ℍ, and the 2-dimensional surface complex structure carrying ℂ. A conjecture is offered relating the intrinsic chirality of the Császár embedding to parity violation in the weak sector. No free parameters are introduced. Open problems are explicitly identified.

# **1. Introduction**

The Standard Model gauge group SU(3) × SU(2) × U(1) is among the most precisely tested structures in physics, yet its origin remains unexplained. Several authors have noted connections between division algebras and particle physics. The octonion–quark connection originates with Günaydin & Gürsey (1973), who identified color SU(3) as the stabilizer of an imaginary unit inside G₂. Furey (2015; 2016; 2018a) showed that the algebra Cℓ(6), constructed from the octonions, reproduces a single generation of Standard Model fermions with correct hypercharges, with electric charge quantized because it is built from a number operator (Furey 2015). Dixon (1994) introduced the tensor product algebra ℂ ⊗ ℍ ⊗ 𝕆 as the algebraic foundation for the Standard Model. Gürsey & Tze (1996) explored related structures extensively.

This note proposes a specific geometric realization: the Császár polyhedron, whose vertex structure carries the octonion algebra naturally. The argument proceeds in stages: a uniqueness argument selects the polyhedron; vertex stabilization under G₂ yields SU(3); the Fano plane incidence geometry produces three generations and exact hypercharges; and the homological cycle structure of the triangulation produces the Cabibbo angle.

# **2. The Uniqueness Argument**

Among compact orientable surfaces, the torus is uniquely selected by the requirement χ = 0 (vanishing Euler characteristic). The Császár polyhedron (1949) is the geometric realization of the complete graph K₇ embedded on the torus. Its uniqueness as the only neighborly triangulation of the torus was proven by Bokowski & Eggert (1991). The combinatorial invariants are completely determined: V = 7 (Heawood bound), E = 21 = C(7,2) (neighborly), F = 14 (Euler: 7 − 21 + 14 = 0), genus g = 1, and χ = 0. Every integer is forced. All 14 faces are triangles (2E = 3F = 42).

# **3. Gauge Group from Vertex Stabilization**

The 7 vertices of K₇ are identified with the 7 imaginary octonion basis elements {e₁, ..., e₇}. The 14 triangular faces correspond to the 7 multiplication triples and their 7 anti-triples — the 7 lines of the Fano plane PG(2, 𝔽₂) and their complements.

The automorphism group of the octonions is the exceptional Lie group G₂, with dim(G₂) = 14 = F. Fix a vertex v₀ (equivalently, fix one imaginary octonion unit). The stabilizer of v₀ in G₂ is SU(3), acting on the 6 remaining vertices which decompose as 3 ⊕ 3̄ (outgoing/incoming via circuit directions). This identification — SU(3) as the G₂-stabilizer of a fixed imaginary unit, with the 3 ⊕ 3̄ branching on the remaining units — is classical (Günaydin & Gürsey 1973). The coset space G₂/SU(3) = S⁶ has dimension 6 = V − 1 = vertex degree of K₇. Three Fano⁺ lines through v₀ define three quaternionic subalgebras, each with Aut(ℍ) = SU(2), providing the weak gauge group. The Z₂ bipartition Fano⁺ ↔ Fano⁻ provides U(1) hypercharge. Dimension equation: 14 = 12 + 2, i.e., dim(G₂) = dim[SU(3)×SU(2)×U(1)] + dim H₁(T²).

# **4. Three Generations from Fano Lines**

Three of the 7 Fano lines pass through any given vertex. Each such line defines a quaternionic subalgebra of the octonions. The three lines through v₀ yield three geometrically distinct quaternionic embeddings ℍ₁, ℍ₂, ℍ₃ ⊂ 𝕆, each carrying its own Aut(ℍ) = SU(2). This gives exactly three generations of fermions.

The number three is the valence of the Fano plane at any point and cannot be adjusted.

# **5. Hypercharge from Fock Space Grading**

The mechanism of this section — a 2³ = 8-dimensional Fock space built from three octonionic fermionic modes, with hypercharge proportional to the occupation number divided by 3, so that charge quantization follows from the integrality of a number operator — is due to Furey (2015), who established it in Clifford-algebraic form with the neutrino playing the role of the vacuum state; the full SU(3) × SU(2) × U(1)(× U(1)) ladder-operator construction on ℂ ⊗ ℍ ⊗ 𝕆 is Furey (2016; 2018a). What this section contributes is a geometric realization of that mechanism on the Császár polyhedron, as follows.

The 21 edges of K₇ decompose into three disjoint Hamiltonian 7-cycles (one for each quadratic residue class mod 7). At the fixed vertex v₀, these three circuits define three fermionic modes with occupation numbers nα, nβ, nγ ∈ {0,1}. The total occupation N = nα + nβ + nγ ranges from 0 to 3, generating a 2³ = 8 dimensional Fock space identified with the octonion basis.

The hypercharge operator is:

*Y = (−1)^(N+1) × N/3*

where N is the total circuit occupation number and 3 = Z₃ is the color symmetry order. The sign alternation arises from the Z₂ complex structure J = L_{e₀}. This yields: N = 0 → Y = 0 (right-handed neutrino); N = 1 → Y = +1/3 (RH down antiquark, 3 colors); N = 2 → Y = −2/3 (RH up antiquark, 3 colors); N = 3 → Y = +1 (right-handed positron). All four match the Standard Model exactly, with no fitting. The spectrum {0, +1/3, −2/3, +1} is the one anticipated by the number-operator construction (Furey 2015; 2018a); the match is a consistency check on the geometric identification rather than an independent derivation of the charges. Hypercharge is the product of the two discrete face symmetries: Y = (Z₂ sign) × N/Z₃.

The novel content of this section is therefore scoped to: (a) the identification of the three fermionic modes with the three disjoint Hamiltonian 7-cycles of K₇ (the quadratic-residue classes mod 7) — a geometric statement with no counterpart in the algebraic construction; and, provisionally, (b) the closed-form sign dressing (−1)^(N+1) obtained from the complex structure J = L_{e₀}. In Furey's construction the corresponding signs are distributed across ideal and conjugation choices; whether the closed-form dressing is a reparametrization of those choices is an open audit item and is claimed in neither direction here.

# **6. CKM Quark Mixing from Fano Generation Mismatch**

The left-handed (Fano⁺) and right-handed (Fano⁻) sectors assign different generation labels to the six neighbor vertices of v₀. The Fano⁺ doublets are {e₁, e₃}, {e₄, e₅}, {e₂, e₆}; the Fano⁻ doublets are {e₂, e₃}, {e₄, e₆}, {e₁, e₅}. Every left-handed generation shares exactly one vertex with two different right-handed generations and zero with the third. This structural mismatch is the geometric origin of quark mixing.

## **6.1 The Cabibbo Angle**

The leading mixing angle is the ratio of the Fano point-valence to the rank of the boundary operator in the Császár triangulation:

*|V_us| = 3/13 = 0.2308*

where 3 is the Fano valence (the number of lines through any vertex, equivalently the number of inter-generation transition channels) and 13 is the rank of the boundary operator ∂₂ in the Császár triangulation.

**Homological derivation of 13. **The Császár triangulation has F = 14 faces, E = 21 edges, V = 7 vertices. The boundary operator ∂₂: C₂ → C₁ sends each triangular face to the sum of its three boundary edges. The kernel of ∂₂ is ker(∂₂) = H₂(T²) ≅ ℤ, reflecting the single fundamental class of the closed torus. Therefore:

*rank(∂₂) = dim(C₂) − dim(ker ∂₂) = 14 − 1 = 13*

This counts the independent contractible 1-cycles on the Császár torus — cycles that bound a region of the surface. The total 1-cycle space has dimension E − V + 1 = 15 (the circuit rank of K₇). Of these, 13 are contractible (boundaries of face-chains) and the remaining 2 are the generators of H₁(T²) ≅ ℤ² — the two non-contractible loops around the torus.

**Physical interpretation. **The ratio 3/13 is a topological invariant of the Császár triangulation: the numerator is the Fano point-valence (three lines through every vertex, a combinatorial constant of PG(2,𝔽₂)) and the denominator is the rank of the boundary operator ∂₂ (determined by the homology of the torus). Both integers are forced by the triangulation; neither is fitted to the data. Why this ratio equals the Cabibbo mixing angle is the physical question the construction raises but does not yet answer from first principles.

The observed value is 0.2250 ± 0.0007 (PDG 2022). Error: 2.6%. Both integers arise from the combinatorial topology of the Császár triangulation: 3 from the Fano incidence structure, 13 from the homology of the torus. No free parameters.

**Note (unresolved conjecture). **The formula |V_cb| = 3/[13(φ + 4)] ≈ 0.04108 reproduces the PDG value 0.0408 ± 0.0014 to 0.7%, where the suppression factor satisfies the algebraic identity 6 − 1/φ² = φ + 4 (with 6 the vertex degree of K₇). This numerical agreement is documented for completeness. However, the golden ratio φ does not appear in the spectral data of K₇, the face adjacency graph eigenvalues, or the modular parameter of the Császár torus (ρ = e^{iπ/3}, involving √3 not √5). The suppression factor therefore lacks a prior address in the Császár geometry and the formula is not claimed as a derivation. See Open Problem (iii).

## **6.3 The Complex Structure Asymmetry**

The mechanism producing the CKM hierarchy is the asymmetric action of the complex structure J = L_{e₀} on the up-type and down-type subspaces. Restricted to the up-type (outgoing) vertices {e₁, e₂, e₃}, J couples Generation 1 and Generation 3 (J(e₁) = e₃, J(e₃) = −e₁). Restricted to the down-type (incoming) vertices {e₆, e₅, e₄}, J couples Generation 2 and Generation 3 (J(e₄) = e₅, J(e₅) = −e₄). The up-sector rotation lives in the (1,3) plane; the down-sector rotation lives in the (2,3) plane. Their product produces mixing in all three planes with the natural hierarchy |V_us| > |V_cb| > |V_ub|.

## **6.4 Open CKM Elements**

The remaining matrix elements — |V_ub|, |V_td|, |V_ts|, and the CP-violating phase δ — have not been derived. The perturbation mechanism is identified: octonion non-associativity between the three quaternionic subalgebras creates inter-generation transition amplitudes. The associators are nonzero for half of the inter-generation triples (equal to ±2e₀) and zero for the other half. This asymmetry should encode the Jarlskog invariant, but the computation is incomplete.

# **7. The Rank-4 Resolution: Gauge Independence from Topological Dimension**

The gauge group SU(3) × SU(2) × U(1) has rank 4. The automorphism group G₂ = Aut(𝕆) has rank 2. This gap was identified by Krasnov (private communication) as the central obstruction to the present construction. We resolve it by showing that SU(2) and U(1) arise not from subgroups of G₂, but from the geometric and conformal structure of the Császár embedding, acting on topological data of different dimension than the vertex labels on which G₂ acts. Sourcing the additional rank outside Aut(𝕆) is itself standard in the division-algebra program — algebraically from the ℍ and ℂ factors of ℂ ⊗ ℍ ⊗ 𝕆 (Furey 2018a), or by triality enlargement of der(𝕆) to tri(𝕆) = so(8) (Furey & Hughes 2025) — and the claim of this section is confined to the topological realization of that move on embedding data (see Section 11).

## **7.1 Three Gauge Actions on Three Topological Strata**

The Császár polyhedron carries three geometrically independent types of data:

**Stratum 0 (vertices). **The seven vertices carry the imaginary octonion units e₁ through e₇. The automorphism group G₂ acts on these labels. Fixing one vertex reduces G₂ to its SU(3) stabilizer, acting on the six remaining vertices as 3 ⊕ 3̄. This is standard — the coset space G₂/SU(3) = S⁶ has dimension 6, matching the vertex degree of K₇.

**Stratum 1 (edges). **The 21 edges of the Császár polyhedron are embedded as line segments in ℝ³. Each edge carries a tangent vector and a normal plane. The orientation of the normal plane — the choice of normal and binormal directions — is the edge framing. Rotations of this frame form SO(3), and the spin structure induced by the ℝ³ embedding lifts this to SU(2). The embedding in ℝ³ has a unique spin structure — it is inherited from the ambient space, not selected from alternatives.

**Identification with the weak SU(2) (conjecture). **The existence of an SU(2) acting on edge framings establishes the gauge group factor but does not by itself identify it with the weak isospin SU(2) of the Standard Model. That identification requires two additional steps, both of which are conjectured here rather than derived. First, the coupling must be chiral: the SU(2) edge-framing action must couple to left-handed fermion modes only. The Császár embedding is intrinsically chiral (Section 8), and the conjecture is that this chirality selects the L-enantiomer as the one admitting a non-trivial SU(2) bundle extension, while the R-enantiomer encounters a topological obstruction. If this obstruction argument can be made precise — computing the relevant Stiefel-Whitney or framing class for each enantiomer — it would supply the V−A structure geometrically. Second, the SU(2) doublet structure must be connected to the generation structure of Section 4: each of the three quaternionic subalgebras ℍ₁, ℍ₂, ℍ₃ carries its own Aut(ℍ) = SU(2), and the weak SU(2) is identified with the diagonal or generation-averaged action on the edge framings. The precise quotient map has not been constructed. Both steps are recorded as open problems (see Open Problem (xi)).

**Stratum 2 (surface). **The 14 triangular faces form a toroidal surface of genus 1. As a Riemann surface, the torus carries a complex structure with U(1) phase rotations. This conformal data is determined by the surface topology and is independent of the vertex labeling and edge framing.

## **7.2 Independence and Commutativity**

The three gauge transformations are geometrically independent:

Relabeling a vertex (SU(3)) permutes the octonion assignments without moving any edge in space or altering the surface complex structure. Rotating an edge frame (SU(2)) reorients the normal plane of that edge without changing which octonion labels sit at its endpoints or altering the global conformal structure. Rotating the surface phase (U(1)) changes the complex structure without affecting vertex labels or edge framings.

If the fermion representation space factorizes as a genuine tensor product V_color ⊗ V_weak ⊗ V_hypercharge — with SU(3) acting on the first factor, SU(2) on the second, and U(1) on the third — then gauge transformations acting on distinct factors commute automatically, and the total rank is rank(SU(3)) + rank(SU(2)) + rank(U(1)) = 2 + 1 + 1 = 4. This tensor factorization is not, however, automatic from the geometric independence of the strata. The vertices, edges, and faces of the Császár complex are not independent objects but the cells of a chain complex linked by the boundary maps ∂₂ : C₂ → C₁ and ∂₁ : C₁ → C₀ — an edge is a pair of vertices, a face a triple of edges — and cells of different degree are direct summands of this complex, not tensor factors. Under the color SU(3) the 21 edges accordingly carry a non-trivial representation: explicit computation on the octonion derivation algebra gives the su(3)-module decomposition Λ²(𝟕) = 𝟏 ⊕ 𝟖 ⊕ 𝟑 ⊕ 𝟑̄ ⊕ 𝟑 ⊕ 𝟑̄, in which the adjoint 𝟖 appears and exactly one of the 21 dimensions is color-inert. The edge data is therefore not a color-singlet factor. The same conclusion follows independently from the algebraic side: der(W) ⊂ tri(W) acts identically on the spinor, conjugate-spinor, and vector representations (Furey & Hughes 2025), so color, sitting inside der(𝕆), acts alike on every triality representation — predicting from that direction too that the edge stratum cannot be color-inert. Whether the three geometric actions can nonetheless be realized on a common space as a genuine tensor product — on which they then commute identically — is a substantive requirement, not a structural triviality; it is recorded as Open Problem (i).

## **7.3 Why the Additional Rank Does Not Violate the G₂ Constraint**

The rank-2 limitation of G₂ applies to transformations acting on the same representation space — the octonion vertex labels. The SU(2) edge framing and U(1) surface phase do not act on vertex labels. They act on geometric data that exists only because the Császár polyhedron is embedded in ℝ³ as a Riemann surface, not merely defined as an abstract combinatorial object. The abstract K₇ graph has G₂ symmetry on its vertices and nothing else. The Császár embedding enriches K₇ with edge framings and a conformal structure that carry the additional rank.

This necessity can be made precise. Within G₂ = Aut(𝕆) itself there is no room for a commuting weak factor: the centralizer of the color SU(3) in G₂ is trivial. As an su(3)-module the Lie algebra g₂ decomposes as g₂ = 𝟖 ⊕ 𝟑 ⊕ 𝟑̄ (the classical branching; Günaydin & Gürsey 1973) — the adjoint of su(3) together with the 𝟑 ⊕ 𝟑̄ tangent space of the coset G₂/SU(3) = S⁶ — and this decomposition contains no copy of the trivial representation, so no non-zero element of g₂ commutes with all of su(3). The statement is verified by direct computation: solving the derivation condition for g₂ = Der(𝕆), restricting to the 8-dimensional stabilizer of a fixed imaginary unit, and computing its centralizer in g₂ returns dimension zero. Consequently a second gauge factor commuting with color cannot be found inside G₂ under any choice of embedding, and the additional rank must be carried by structure external to Aut(𝕆) — precisely what the edge framings and surface conformal structure supply. The rank-4 obstruction identified by Krasnov is in this sense intrinsic to G₂, not an artifact of the construction, and the stratification of §7.1 is the minimal response to it.

The dimension count dim(G₂) = dim(SU(3) × SU(2) × U(1)) + dim(H₁(T²)) gives 14 = 12 + 2, where the two extra dimensions of G₂ beyond the Standard Model gauge group match the two generators of H₁(T²) — the topological data that supports the edge framings. This is a structural observation, not a derived identity: no map has been constructed sending the two extra G₂ generators to the two torus 1-cycles. The coincidence is noted as a consistency check on the stratification, and is recorded as an open derivation target (see Open Problem (x)).

## **7.4 The Spin Structure**

An abstract genus-1 surface admits 2²ᵍ = 4 spin structures. However, a surface embedded in ℝ³ does not freely choose among them. The ambient space ℝ³ has a unique spin structure, and the embedding pulls it back to the surface canonically. The Császár polyhedron, as a physical object in three-dimensional space, inherits a specific spin structure from ℝ³. The three abstract alternatives would require the edge framings to acquire sign flips around non-contractible cycles (antiperiodic boundary conditions), which the physical embedding does not produce.

Consequently, the SU(2) gauge action on edge framings is uniquely determined by the embedding. This is stronger than a selection among alternatives: the embedding forces a single spin structure with no free choice.

## **7.5 The Tensor Product Decomposition and the Dixon Algebra**

The three topological strata provide a geometric realization of the Dixon algebra ℂ ⊗ ℍ ⊗ 𝕆 (Dixon 1994) — the factor-to-force assignment 𝕆 → SU(3), ℍ → SU(2), ℂ → U(1) that runs through the modern division-algebra corpus (nearest statement: one Standard Model generation from a single copy of ℝ ⊗ ℂ ⊗ ℍ ⊗ 𝕆, Furey & Hughes 2022a; see also Furey & Hughes 2022b):

**Vertices (0-dimensional) → 𝕆 → SU(3). **The 7 vertices carry the imaginary octonion units. Fixing one vertex gives SU(3) as the stabilizer in G₂.

**Edge framings (1-dimensional) → ℍ → SU(2). **The 21 edges, viewed as framed curves in ℝ³, carry quaternionic structure via the following explicit map. Each edge e possesses a Frenet-Serret frame: a unit tangent T, principal normal N, and binormal B = T × N, together with a scalar density (the edge length or a local metric coefficient). These four real quantities (T, N, B, scalar) are assigned to the quaternion basis as (i, j, k, 1) respectively. Under this identification the frame-rotation group SO(3) acting on (T, N, B) is the image of SU(2) under the standard 2:1 covering SU(2) → SO(3), with the scalar component carrying the U(1) norm. The action of SU(2) on the edge framing is therefore the spinor double cover of the SO(3) frame rotation, not merely an analogy. This identification is well-defined on each edge independently; commutativity with the vertex and surface actions holds once the tensor-product structure of §7.2 is established, which — as noted there — is itself an open requirement rather than an automatic consequence of the dimensional separation of the strata.

**Surface complex structure (2-dimensional) → ℂ → U(1). **The Császár torus as a Riemann surface carries a complex structure with U(1) phase rotations.

Granting that tensor-product structure, the gauge actions commute and the total rank is 2 + 1 + 1 = 4. The additional rank beyond G₂ arises from the geometric and conformal structure of the Császár embedding, not from subgroups of G₂; and, as established in §7.3, no weak factor commuting with color exists inside G₂, so an external source for the additional rank is mandatory rather than merely convenient.

# **8. Conjecture: Geometric Origin of Parity Violation**

The Császár polyhedron has trivial symmetry group (C₁): it possesses no planes of symmetry, no rotational axes, and no center of symmetry. It is therefore intrinsically chiral, existing as two non-superimposable enantiomers ℳ_L and ℳ_R.

**Conjecture 1 (Chiral Coupling). ***The SU(2) weak interaction, acting on the quaternionic edge-framing factor, is permitted only for one enantiomer of the Császár embedding. The L-enantiomer admits a vanishing obstruction class for the relevant bundle transition, while the R-enantiomer encounters a non-trivial topological obstruction enforcing its status as an SU(2) singlet.*

If correct, this provides a geometric origin for the V−A structure of the weak interaction. The relevant obstruction theory — involving ribbon framing, total torsion, and writhe of the K₇ edge graph — has not been carried out.

**Adjacent prior art, differentiated.** Parity violation has been obtained from the algebraic side of the division-algebra program: Furey (2018c) demonstrates that electroweak theory can violate parity automatically in the leptonic case, from ideal and conjugation structure, and Furey & Hughes (2022b) obtain left–right symmetric Higgs representations from quaternionic triality within a symmetry-breaking cascade. Conjecture 1 targets the same phenomenon by a distinct mechanism — a topological obstruction distinguishing the two enantiomers of a chiral embedding — and is neither derived from nor reducible to those algebraic mechanisms; no priority is claimed in either direction, and the obstruction computation remains open as stated.

# **9. Structural Predictions and Falsifiability**

**Verified claims:**

(1) SU(3) arises as Stab_{G₂}(e_i), acting on the octonionic vertex structure.

(2) Three fermion generations correspond to the three Fano lines through any vertex. A fourth generation would falsify this.

(3) Hypercharges (0, +1/3, −2/3, +1) follow from Y = (−1)^(N+1) × N/3. Any deviation in hypercharge quantization would falsify the construction.

(4) The rank-4 gauge group arises from three independent topological strata of the Császár embedding, not from subgroups of G₂. That no weak factor commuting with color can instead be found inside G₂ is a theorem: the centralizer of the color SU(3) in G₂ is trivial, since g₂ = 𝟖 ⊕ 𝟑 ⊕ 𝟑̄ as an su(3)-module contains no trivial summand (verified by direct computation on Der(𝕆)). The commutativity of the three actions, by contrast, is contingent on establishing a genuine tensor-product realization of the representation space (Open Problem (i)) and is not claimed here as established.

(5) The Cabibbo angle sin(θ_C) = 3/13 = 0.2308, within 2.6% of the PDG value, where both 3 and 13 are topological invariants of the Császár triangulation.

**Conjectures (untested):**

(1) The intrinsic chirality of the Császár polyhedron provides a geometric origin for parity violation.

(2) |V_cb| = 3/[13(φ+4)] = 0.04108, within 0.7% of PDG. The golden ratio suppression factor lacks a prior address in the Császár geometry.

# **10. Open Problems**

The following are explicitly unsolved and are not claimed as results:

(i) Establishment of a genuine tensor-product realization V_color ⊗ V_weak ⊗ V_hypercharge of the three gauge actions. The commutativity asserted in Section 7.2 is automatic once such a factorization is in hand — operators on distinct tensor factors commute identically, so no separate bracket computation is required — but the factorization itself is not automatic: the strata are the cells of a chain complex rather than independent factors, and the 21 edges carry a non-trivial color representation (Section 7.2). The required content splits according to how the weak SU(2) is realized. (a) If SU(2) acts on the Frenet-framing fibre (the four real quantities (T, N, B, scalar) per edge) while color acts on the edge labels, the two commute precisely when the framed-edge bundle is trivial — i.e. when the color action lifts to the bundle without frame holonomy. Because the bundle is associated to a non-trivial color representation, this is not automatic, and deciding it is exactly Open Problem (ii). (b) If SU(2) is the weak isospin acting on the octonionic fermion doublets, commutativity with color is the Furey–Dixon centralizer statement, which holds in Cℓ(6) because there SU(2) lives on the ℍ factor of ℂ ⊗ ℍ ⊗ 𝕆, genuinely separate from the 𝕆 carrying color; the Császár-specific burden is then to show the edge-framing data faithfully reconstructs that ℍ factor, which is Open Problem (xi)(b). In either reading the problem reduces to one already on this list, and is not an independent computation.

(ii) Computation of the obstruction invariant distinguishing the two Császár enantiomers under quaternionic framing extension.

(iii) Prior address for the golden ratio φ in the V_cb suppression factor. The spectral data of K₇ and its face adjacency graph do not contain φ. The modular parameter of the Császár torus is ρ = e^{iπ/3}, involving √3 not √5. The prior address, if it exists, must come from the algebraic structure (octonion multiplication, associators) rather than the combinatorial geometry.

(iv) The remaining CKM elements: |V_ub|, |V_td|, |V_ts|, and the CP-violating phase δ.

(v) The PMNS neutrino mixing matrix.

(vi) Mass hierarchies and coupling constant values from the lattice invariants.

(vii) Quantization of the classical vertex structure — connecting the combinatorial lattice to quantum field theory.

(viii) Whether the K₈ embedding on genus 2 carries F₄ or E₆ structure relevant to grand unification.

(ix) Whether the 2.6% overshoot on sin(θ_C) = 3/13 is attributable to renormalization group running from the compactification scale.

(x) Construction of an explicit map from the two extra generators of G₂ (beyond SU(3)) to the two generators of H₁(T²). The dimension count 14 = 12 + 2 is a structural consistency observation; it becomes a theorem only when this map is made explicit and shown to be equivariant under the full gauge action.

(xi) The left-handed coupling of the SU(2) edge-framing action. Two steps are required: (a) computation of the topological obstruction class distinguishing the L- and R-enantiomers of the Császár embedding under quaternionic framing extension, to establish that the SU(2) bundle couples exclusively to the L-enantiomer; and (b) construction of the quotient map identifying the weak isospin SU(2) with the diagonal action of Aut(ℍ₁) × Aut(ℍ₂) × Aut(ℍ₃) on the generation structure, rather than with each generation’s SU(2) separately. Until both steps are completed, the identification of the edge-framing SU(2) with the Standard Model weak isospin SU(2) is a conjecture.

# **11. Relationship to Prior Work**

The algebraic core of this construction is closely related to work by Furey (2014; 2015; 2016; 2018a,b; 2025), who showed that division algebraic ladder operators reproduce Standard Model fermion representations with correct gauge charges. Dixon (1994) introduced ℂ ⊗ ℍ ⊗ 𝕆 as the algebraic design of physics; the present work proposes the Császár polyhedron as its geometric realization. Gürsey & Tze (1996) studied octonions in particle physics extensively. Krasnov (2018, 2024) approached the Standard Model gauge group from Spin(10) geometry. Boyle & Farnsworth (2020) explored non-associative geometry and the Pati-Salam model via Jordan algebras. The Császár polyhedron is well-studied in combinatorial topology; its connection to octonion multiplication via the Fano plane has not previously, to our knowledge, been used to derive gauge group structure or quark mixing angles.

**Three-generation mechanisms, differentiated.** Several distinct threefold mechanisms exist in the division-algebra program, and none coincides with the Fano point-valence mechanism of Section 4. Furey & Hughes (2025) identify the Standard Model symmetries inside tri(ℂ) ⊕ tri(ℍ) ⊕ tri(𝕆) and realize three generations as the triality triple (Ψ₊, Ψ₋, V) — spinor, conjugate-spinor, and vector representations of ℂ ⊗ ℍ ⊗ 𝕆 — with the third generation extracted from the vector copy via a Cartan factorization; the three there is S₃ triality, not incidence valence. Furey (2014; 2018b) realizes three generations as three generation "prints" within the Cℓ(6) decomposition, with unbroken symmetry SU(3) × U(1) only. Gillard & Gresnigt (2019) obtain three generations from the complex sedenions, splitting ℂ ⊗ 𝕊 into three ℂ ⊗ 𝕆 subalgebras that share a common quaternionic subalgebra — structurally the nearest relative of the present mechanism, and still distinct: three octonion subalgebras through a common ℍ there, versus three quaternionic subalgebras ℍ₁, ℍ₂, ℍ₃ ⊂ 𝕆 through a common unit here. The sedenion construction has since been extended to Cℓ(8), with the three generations carrying an explicit S₃ family symmetry (Gourlay & Gresnigt 2024) — again an automorphism three, not incidence valence. One further near-miss deserves explicit note: the decomposition e₇ ≅ (tri(ℍ) ⊕ tri(𝕆)) + 3(ℍ ⊗ 𝕆) also contains three copies of ℍ ⊗ 𝕆, but those are triality-related copies of the *same* algebra — different objects, different threes. On the rank-4 problem, the principal algebraic alternatives to the topological-strata sourcing of Section 7 are rank from the ℍ and ℂ factors (Furey 2018a) and triality enlargement of der(𝕆) (rank 2) to tri(𝕆) = so(8) (rank 4), with the weak su(2)_L realized inside tri(ℍ) (Furey & Hughes 2025); as noted in Section 7, the external-sourcing move is standard in this program, and the present contribution is confined to its topological realization on embedding data. By contrast, no derivation of quark mixing angles appears in this corpus — Yukawa couplings there remain free parameters — so the Cabibbo 3/13 result and the Fano⁺/Fano⁻ doublet-mismatch mechanism of Section 6 remain, to our knowledge, without counterpart.

# **12. Conclusion**

The Császár polyhedron is selected by uniqueness: it is the only neighborly triangulation of the only χ = 0 compact orientable surface. Its combinatorial structure produces SU(3) via vertex stabilization, three generations via Fano line valence, and exact hypercharges via Fock space grading. The rank-4 problem is resolved by the observation that the three gauge groups act on topological data of different dimension — vertex labels, edge framings, and surface complex structure — inheriting additional rank from the embedding geometry rather than from G₂ subgroups.

The Cabibbo angle sin(θ_C) = 3/13 is derived from the ratio of the Fano valence to the rank of the boundary operator in the Császár triangulation, both topological invariants of the polyhedron, within 2.6% of the PDG value. The |V_cb| element is reproduced to 0.7% but with an algebraically unmotivated golden-ratio factor; it is documented as a conjecture pending a prior address.

Five claims are presented as verifiable results; two conjectures and eleven open problems are explicitly identified as unsolved. The identification of the edge-framing SU(2) with the weak isospin SU(2) is explicitly labeled as a conjecture pending the obstruction computation of Open Problem (xi). The construction is offered for independent mathematical verification.

# **Acknowledgments**

The author thanks Kirill Krasnov for identifying the rank-4 obstruction, which led to the topological stratification argument in Section 7.

# **References**

[1] Bokowski, J. & Eggert, A. (1991). All realizations of Möbius’ torus with 7 vertices. Topologie Structurale 17, 59–78.

[2] Boyle, L. & Farnsworth, S. (2020). The standard model, the Pati-Salam model, and Jordan geometry. New J. Phys. 22, 073023.

[3] Császár, Á. (1949). A polyhedron without diagonals. Acta Sci. Math. (Szeged) 13, 140–142.

[4] Dixon, G. M. (1994). Division Algebras: Octonions, Quaternions, Complex Numbers and the Algebraic Design of Physics. Kluwer.

[5] Furey, C. (2014). Generations: three prints, in colour. J. High Energy Phys. 10, 046.

[6] Furey, C. (2015). Charge quantization from a number operator. Phys. Lett. B 742, 195–199.

[7] Furey, C. (2016). Standard Model physics from an algebra? arXiv:1611.09182.

[8] Furey, C. (2018a). SU(3)×SU(2)×U(1)(×U(1)) as a symmetry of division algebraic ladder operators. Eur. Phys. J. C 78, 375.

[9] Furey, C. (2018b). Three generations, two unbroken gauge symmetries, and one eight-dimensional algebra. Phys. Lett. B 785, 84–89.

[10] Furey, C. (2018c). A demonstration that electroweak theory can violate parity automatically (leptonic case). Int. J. Mod. Phys. A 33 (4), 1830005.

[11] Furey, C. (2025). A superalgebra within. Annalen der Physik 537 (arXiv:2505.07923).

[12] Furey, N. & Hughes, M. J. (2022a). One generation of Standard Model Weyl representations as a single copy of ℝ ⊗ ℂ ⊗ ℍ ⊗ 𝕆. Phys. Lett. B 827, 136959.

[13] Furey, N. & Hughes, M. J. (2022b). Division algebraic symmetry breaking. Phys. Lett. B 831, 137186.

[14] Furey, N. & Hughes, M. J. (2025). Three Generations and a Trio of Trialities. Phys. Lett. B 865, 139473 (arXiv:2409.17948).

[15] Gillard, A. B. & Gresnigt, N. G. (2019). Three fermion generations with two unbroken gauge symmetries from the complex sedenions. Eur. Phys. J. C 79, 446.

[16] Gourlay, L. & Gresnigt, N. G. (2024). Algebraic realisation of three fermion generations with S₃ family and unbroken gauge symmetry from Cℓ(8). Eur. Phys. J. C 84, 1129.

[17] Günaydin, M. & Gürsey, F. (1973). Quark structure and the octonions. J. Math. Phys. 14 (11), 1651–1667.

[18] Gürsey, F. & Tze, C.-H. (1996). On the Role of Division, Jordan and Related Algebras in Particle Physics. World Scientific.

[19] Heawood, P. J. (1890). Map-colour theorem. Quart. J. Math. 24, 332–338.

[20] Krasnov, K. (2018). Fermions, differential forms and doubled geometry. Nucl. Phys. B 936, 36–75.

[21] Krasnov, K. (2024). Geometry of Spin(10) symmetry breaking. J. Math. Phys. 65, 082302.

[22] Particle Data Group (2022). Review of Particle Physics. PTEP 2022, 083C01.

[23] Ringel, G. & Youngs, J. W. T. (1968). Solution of the Heawood map-coloring problem. PNAS 60(2), 438–445.