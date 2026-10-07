# B1 — Gauge paper v6.3: pre-registration

**Plain-language summary.** The published gauge-group paper (v6.3) makes two claims that a new calculation or a new data comparison could downgrade.
1. Its hypercharge formula puts an alternating sign, (−1)^(N+1), in front of Furey's number-operator charge N/3. The paper leaves open whether that sign is just a relabelling of choices Furey already makes. This file fixes how that question will be decided.
2. It states the Cabibbo result as sin θ_C = |V_us| = 3/13. This file fixes how that statement will be judged against the 2024 Particle Data Group values, and how the alternative reading tan θ_C = |V_us/V_ud| may be used.

It also records a text check that is already done (v6.3 never calls PSL(2,7) the polyhedron's automorphism group) and one structural check behind §8's chirality statement.

**Lock.** Locked by its md5 in `B1_LOCK.txt` and by the commit that adds it, before any B1 computation file exists. Corrections go in dated addenda.

## Objects of record

- **The paper.** `Gifford_Csaszar_Gauge_Group_v6_3_2026.md` (project store), the canonical text of Zenodo record 21316171 (Zenodo version v5, July 12, 2026); ledger anchor md5 `8c01f4c9d849bbab1eaff826fd353c3f`.
- **§5, verbatim:**
  > The hypercharge operator is: *Y = (−1)^(N+1) × N/3* where N is the total circuit occupation number and 3 = Z₃ is the color symmetry order. The sign alternation arises from the Z₂ complex structure J = L_{e₀}. This yields: N = 0 → Y = 0 (right-handed neutrino); N = 1 → Y = +1/3 (RH down antiquark, 3 colors); N = 2 → Y = −2/3 (RH up antiquark, 3 colors); N = 3 → Y = +1 (right-handed positron). All four match the Standard Model exactly, with no fitting.

  > […] provisionally, (b) the closed-form sign dressing (−1)^(N+1) obtained from the complex structure J = L_{e₀}. In Furey's construction the corresponding signs are distributed across ideal and conjugation choices; whether the closed-form dressing is a reparametrization of those choices is an open audit item and is claimed in neither direction here.
- **§3, verbatim:** "The stabilizer of v₀ in G₂ is SU(3), acting on the 6 remaining vertices which decompose as 3 ⊕ 3̄ (outgoing/incoming via circuit directions)."
- **§6.1 and §9 claim (5):** "|V_us| = 3/13 = 0.2308"; "The observed value is 0.2250 ± 0.0007 (PDG 2022). Error: 2.6%."; "(5) The Cabibbo angle sin(θ_C) = 3/13 = 0.2308, within 2.6% of the PDG value". Open Problem (ix): "Whether the 2.6% overshoot on sin(θ_C) = 3/13 is attributable to renormalization group running from the compactification scale."
- **§8:** "The Császár polyhedron has trivial symmetry group (C₁) […] It is therefore intrinsically chiral".

## External anchors (fetched October 7, 2026)

- **Furey 2015**, "Charge quantization from a number operator", PLB 742, 195–199 (arXiv:1603.04078, read on ar5iv):
  - ladder operators α₁ = ½(−e₅ + ie₄), α₂ = ½(−e₃ + ie₁), α₃ = ½(−e₆ + ie₂), with {α_i, α_j†} = δ_ij;
  - N = Σ α_i†α_i, eigenvalues {0, 1, 1, 1, 2, 2, 2, 3}; Q ≡ N/3;
  - minimal left ideal S^u: ν (ωω†), d̄^{r,g,b} (α_i†ωω†), u^{r,g,b} (α_i†α_j†ωω†), e⁺ (α₃†α₂†α₁†ωω†);
  - the complex-conjugate ideal S^d carries the antiparticles, with charge −Q*.
- **PDG 2024** (Navas et al., Phys. Rev. D 110, 030001 (2024)), review "CKM quark-mixing matrix", read on the KEK mirror (`rpp2024-rev-ckm-matrix.pdf`):
  - Eq. (12.7) |V_ud| = 0.97367 ± 0.00032;
  - Eq. (12.8) |V_us| = 0.22431 ± 0.00085 (average of K_ℓ3, 0.2233 ± 0.0005, and K_μ2/π_μ2, 0.2250 ± 0.0004, error scaled by 2.5);
  - Eq. (12.26) global fit λ = 0.22501 ± 0.00068; Eq. (12.27) fit |V_ud| = 0.97435 ± 0.00016, |V_us| = 0.22501 ± 0.00068.
- **CKM running.** Grossman, Ismail, Ruderman & Tsai, "CKM substructure from the weak to the Planck scale" (arXiv:2201.10561): "λ, ρ, and η only change by O(10⁻⁴) from the weak scale to the Planck scale, confirming known results."
- **Standard Model color–charge correlation (textbook).** In one generation, every color triplet has electric charge (and, for SU(2) singlets, hypercharge) ≡ 2/3 mod 1, every antitriplet ≡ 1/3 mod 1, every singlet ≡ 0 mod 1: u (3, +2/3), d (3, −1/3), ū (3̄, −2/3), d̄ (3̄, +1/3), ν (1, 0), e (1, ∓1).

## Questions and computations (two legs)

**Q1 — the Furey item.** On the Fock space Λ(ℂ³) of three fermionic modes (2³ = 8 states), with color SU(3) acting on the modes as ρ ∈ {3, 3̄} and on each N-sector by the induced action:
- **C1.** The color representation of each N-sector (from explicit weights).
- **C2.** Additivity: is there (a, b) with Y(N) = a + bN for N = 0…3, for the paper's Y? (A U(1) commuting with an irreducible color action on the modes gives every mode the same charge b, so a charge that is additive over modes has this form.)
- **C3.** Furey's options F: q(N) ∈ {N/3, −N/3, (3−N)/3, −(3−N)/3} (ideal S^u or S^d; number operator N or its conjugate 3 − N; overall sign), each with ρ ∈ {3, 3̄}. Does any option reproduce the paper's Y on every sector? Does any reproduce the paper's (color, Y) table with the paper's own labels (both quark sectors antiquarks, i.e. both 3̄)?
- **C4.** The paper's Y with the induced colors, for ρ = 3 and ρ = 3̄: list the (color, Y) pairs and test each against the color–charge correlation.

**Q2 — the Cabibbo observable.**
- **C5.** Pulls z = (3/13 − x)/σ_x for the sin reading, x ∈ {|V_us| (Eq. 12.8), λ (Eq. 12.26)}, and for the tan reading, x ∈ {|V_us|/|V_ud| from Eqs. 12.8 and 12.7 (errors added in quadrature), 0.2250/0.97367 from the K_μ2/π_μ2 value, λ/√(1 − λ²) from the fit}.

**Q3 — symmetry statements.**
- **T1 (done before this file).** v6.3 and the v5 manuscript (`Gifford_Csaszar_Gauge_Group_v5_2026.docx`) contain no statement that PSL(2,7) is the automorphism or symmetry group of the polyhedron; v6.3 never mentions PSL(2,7). Earlier manuscript versions are not in the store.
- **C6.** The Császár triangulation (faces {i, i+1, i+3} and {i, i+2, i+3}, i ∈ ℤ₇): order of its automorphism group (brute force over S₇), and for each automorphism whether it preserves the coherent orientation of the torus. Also |AGL(1,7)| = 42 is squarefree, so all its Sylow subgroups are cyclic and its Schur multiplier is trivial (standard theorem); record the factorisation.

## Decision rules

**DR-B1-1 (Q1).**
- **(R) Reparametrization:** some option in F reproduces the paper's Y on every sector with the paper's colors → claim (b) is withdrawn as not new.
- **(N-C) New and consistent:** no option in F reproduces it, Y is additive, and every (color, Y) pair passes the correlation under an induced action → claim (b) stands, still provisional.
- **(N-I) Not a reparametrization, and inconsistent:** no option in F reproduces it, and either Y is not additive or some pair fails the correlation under both induced actions → claim (b) is withdrawn as incorrect; §5's spectrum and §9 claim (3) are corrected to Furey's Q = N/3; the novelty of §5 is scoped to (a), the cycle identification.

**DR-B1-2 (Q2).**
- If |z| > 3 for the sin reading against both x values, the statement sin θ_C = |V_us| = 3/13 is excluded and leaves "Verified claims".
- The tan reading is reported with its pulls. Because v6.3 derives a number, not an observable, and the tan reading was found after comparison with data (audit of October 6, 2026), it may enter the paper only as a post-hoc observation (Eddington flag: a fit by choice of observable), never as a verified result or prediction.
- If |z| ≤ 3 for the sin reading against either x value, claim (5) stays, with the 2024 numbers.
- Open Problem (ix): if the cited running is below 0.5 % between the weak scale and high scales (against the 2.6 % gap), (ix) is closed negative.

**DR-B1-3 (Q3).**
- Any statement found that PSL(2,7) is the automorphism or symmetry group of the polyhedron or its face set is corrected. Ledger entries that attribute that statement to the gauge paper, or that call PSL(2,7) the symmetry group of K₇ or of the polyhedron, are annotated in the Phase B fold (blast radius).
- If every automorphism of the triangulation preserves orientation, §8's chirality may be stated combinatorially: no realization in ℝ³ has a mirror, inversion or rotoreflection symmetry. If some automorphism reverses orientation, §8's "intrinsically chiral" is scoped to the realization meant.

## Values worked out before computing (first leg, by hand)

Recorded here so that the first leg's values are filed before the second leg starts (the Phase A process note).
- **Q1:** N = 1 and N = 2 carry conjugate representations (Λ²ℂ³ ≅ 3̄ ⊗ det). The paper's Y (0, 1/3, −2/3, 1) is not of the form a + bN. No option in F reproduces it. With the induced colors, ρ = 3̄ gives (3̄, +1/3) and (3, −2/3), and ρ = 3 gives (3, +1/3) and (3̄, −2/3); one pair fails the correlation either way. Expected verdict **(N-I)**.
- **Q2:** sin reading +7.6σ (direct) and +8.5σ (fit), so excluded. Tan reading about +0.4σ (direct), −0.8σ (K_μ2/π_μ2) and −0.2σ (fit). Running O(10⁻⁴), so (ix) closes negative.
- **Q3:** the automorphism group has order 42 (AGL(1,7)), all of it orientation-preserving (the 7-vertex torus is the chiral regular map {3,6}₍₂,₁₎); 42 = 2·3·7.

## Second leg

A blind subagent receives the §5 and §3 quotes, Furey's definitions, the correlation rule, the PDG inputs and the face list, and computes C1–C6 independently in its own directory. It is not given this file, the values above or the first leg's outputs. A comparison script then checks that both legs agree on: the sector colors, additivity, the option match, the four induced (color, Y) pairs with pass/fail, the five pulls to 0.01σ, the automorphism-group order and its orientation count.
