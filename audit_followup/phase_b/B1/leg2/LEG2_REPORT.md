# B1, leg 2: independent blind report

## Plain-language summary

I rebuilt the paper's 8-state fermionic Fock space from scratch on the complex octonions, with Furey's ladder operators acting by left multiplication. No tensor or Jordan–Wigner product is used anywhere. Whichever way colour SU(3) acts on the three creation operators, the one-particle sector (N=1) and the two-particle sector (N=2) carry opposite colour representations (3 and 3̄, or 3̄ and 3). The paper labels both as 3̄, which cannot happen. Its hypercharge Y(N) = (−1)^(N+1)·N/3 is also not additive: a charge that is additive over modes and fits Y(0)=0 and Y(1)=1/3 must give Y(2)=+2/3, not −2/3. None of the eight "Furey options" (four charge rules × two colour actions) reproduces either the paper's Y values or its colour–charge table, and with the colours actually induced, the paper's (colour, Y) pairs break the Standard Model colour–charge correlation in one sector under either choice. Read as sin θ_C, 3/13 lies 7.6σ and 8.5σ from PDG 2024; read as tan θ_C, it lies within 0.8σ in all three comparisons. The Császár torus has exactly 42 automorphisms (the affine group x → ax+b on Z₇) and all of them preserve orientation.

## Scope, blindness, reproduction

- I worked only inside `audit_followup/phase_b/B1/leg2/`. I did not open, list or read any other file under `audit_followup/`, did not consult other material about B1, and used no git and no web access.
- To reproduce: `python3 leg2_b1.py > leg2_output.txt` (Python 3.13, sympy 1.14, mpmath 1.3; about 1.5 s). The script writes `leg2_results.json` itself. It runs 52 internal consistency checks and exits 0 only if all of them pass. All 52 pass.
- Exact arithmetic (sympy rationals, Gaussian rationals and √3) is used everywhere except C5. C5 uses IEEE doubles, re-checked with 50-digit mpmath.

## Method

### C1: the Fock space on C⊗O
1. **Octonion table.** I used e_i e_{i+1} = e_{i+3} with indices mod 7 in 1..7, which gives the triples (1,2,4) (2,3,5) (3,4,6) (4,5,7) (5,6,1) (6,7,2) (7,1,3). Checks:
   - Every pair of imaginary units lies in exactly one triple.
   - L_{e0} = 1, and each L_{ek} (k ≥ 1) is real antisymmetric.
   - The left and right Clifford relations {L_j, L_k} = {R_j, R_k} = −2δ_jk hold. So the algebra is alternative and a unital composition algebra, which by Hurwitz means it is the octonions.
   - (e1e2)e3 ≠ e1(e2e3), so the table is non-associative.
2. **Ladder operators.** I took Furey's α₁ = ½(−e₅+ie₄), α₂ = ½(−e₃+ie₁), α₃ = ½(−e₆+ie₂) as 8×8 left-multiplication matrices (printed in the output). Checks:
   - L(α_i†) equals the conjugate transpose of L(α_i).
   - {α_i, α_j†} = δ_ij·1₈ and {α_i, α_j} = 0.
   - **The table worked as given; no adjustment was needed.** These anticommutators use only the Clifford relations of L_{e1..e6}, so any valid octonion table would satisfy them. What the table fixes is where the vacuum sits.
3. **Vacuum and ideal.**
   - N = Σα_i†α_i has characteristic polynomial x(x−1)³(x−2)³(x−3).
   - With ω = α₁α₂α₃ (operator chain), ωω† is a hermitian rank-1 idempotent with trace 1. It is the projector onto v₀ = (ωω†)·1 = ½(1 + i e₇), and α_i v₀ = 0 for all i.
   - The 64 monomials in L_{e1..e6} are linearly independent, so they span M₈(ℂ) ≅ Cl₆(ℂ).
   - The left ideal M₈(ℂ)·ωω† has dimension 8. It is spanned by ωω†, α_i†ωω†, α_i†α_j†ωω† and α₃†α₂†α₁†ωω†, and the map Xωω† ↦ Xv₀ identifies it with C⊗O.
   - The Fock states as octonions:
     - N=1: ½(e₅+ie₄), ½(e₃+ie₁), ½(e₆+ie₂)
     - N=2 (α₁†α₂†v₀, α₁†α₃†v₀, α₂†α₃†v₀): −½(e₂+ie₆), ½(e₁+ie₃), −½(e₄+ie₅)
     - N=3: −(i/2)(1 − ie₇)
4. **su(3).** T^a = Σ_ij α_i† M^a_ij α_j, with M^a = λ^a/2 (ρ = 3) or M^a = −(λ^a)*/2 (ρ = 3̄). Verified:
   - [T^a, T^b] = i f_abc T^c
   - [T^a, α_k†] = Σ_i M^a_ik α_i†, so the creation operators transform as ρ
   - [T^a, N] = 0
5. **Classification criterion.** I restrict T^a exactly to each N-sector and form C₂ = Σ T^aT^a and C₃ = Σ d_abc T^aT^bT^c.
   - **1:** the sector is 1-dimensional and every T^a vanishes on it.
   - **3:** the sector is 3-dimensional with C₂ = 4/3 and C₃ = +10/9.
   - **3̄:** the sector is 3-dimensional with C₂ = 4/3 and C₃ = −10/9.

   As a cross-check, the (T³, T⁸) weights must equal the weights of the defining 3 or their negatives. The two criteria agree in all 8 cases (2 choices of ρ × 4 sectors).

### S1: supplementary cross-check (not one of C1–C6)
- I computed Der(O) by solving D(xy) = D(x)y + xD(y) exactly. It has dimension 14 (g₂), and its stabiliser of e₇ has dimension 8.
- span_ℝ{−iT^a} equals that stabiliser exactly (rank test).
- The N=1 sector is the +i eigenspace of L_{e₇} inside span_ℂ(e₁..e₆). The N=2 sector is the −i eigenspace, which is the **complex conjugate** of the N=1 sector. Conjugation also maps N=0 to N=3.
- So the paper's own Section-3 colour group (the stabiliser of an imaginary unit in G₂) is exactly this su(3). Its "3 ⊕ 3̄" on the six units is the N=1 ⊕ N=2 pair. Because the group acts by real automorphisms of O, these two sectors are always mutually conjugate, whatever labelling of generators is used.

### C2–C6
- **C2:** Exact fractions. I tested the a + bN form and also the general per-mode form c + y_a n_a + y_b n_b + y_g n_g over all 8 occupation patterns.
- **C3 and C4:** The colours come from C1. The correlation test is q mod 1 = 2/3 for 3, 1/3 for 3̄ and 0 for 1, computed with exact `Fraction % 1`.
- **C5:** z = (3/13 − x)/σ_x. For the ratios, relative errors are added in quadrature. For (e), σ = σ_λ(1−λ²)^(−3/2).
- **C6:** Brute force over all 5040 permutations of Z₇.
  - Orientation: each face carries its increasing-order reference orientation, and ∂₂[a,b,c] = [b,c] − [a,c] + [a,b] over ℤ.
  - ker ∂₂ has rank 1, and its integer generator s lies in {±1}¹⁴.
  - Each automorphism σ acts by σ_#(f) = sign(sort)·σ(f). I checked that σ_# is a chain map (∂₂σ_# = σ_#∂₂), then tested σ_# s = +s or −s.
  - Torus checks: K₇ edges, each in two faces; vertex links are 6-cycles; χ = 0; b₁ = 2.

## Results

### C1: induced sector colours
| N | dim | ρ = 3 | ρ = 3̄ |
|---|-----|-------|-------|
| 0 | 1 | 1 | 1 |
| 1 | 3 | 3 (C₃ = +10/9) | 3̄ (C₃ = −10/9) |
| 2 | 3 | 3̄ (C₃ = −10/9) | 3 (C₃ = +10/9) |
| 3 | 1 | 1 | 1 |

N=2 is always the conjugate of N=1, since Λ²ρ ≅ ρ̄ for SU(3). **No induced action makes N=1 and N=2 both 3̄** (`paper_labels_realizable = false`).

### C2: additivity
- Y = (0, 1/3, −2/3, 1).
- The unique affine fit through N=0 and N=1 (a = 0, b = 1/3) predicts Y(2) = 2/3, not −2/3.
- The second differences are −4/3 and 8/3, so Y is not affine in N.
- The per-mode linear system has no solution either.
- **`additive = false`.**

### C3: Furey's options
Paper's table: (1, 0), (3̄, +1/3), (3̄, −2/3), (1, +1).

| q(N) | ρ | N=0 | N=1 | N=2 | N=3 | (i) q = Y | (ii) = paper table | (iii) correlation |
|---|---|---|---|---|---|---|---|---|
| N/3 | 3 | (1,0) | (3,1/3) | (3̄,2/3) | (1,1) | no | no | **fails** |
| N/3 | 3̄ | (1,0) | (3̄,1/3) | (3,2/3) | (1,1) | no | no | holds (Furey S^u: ν, d̄, u, e⁺) |
| −N/3 | 3 | (1,0) | (3,−1/3) | (3̄,−2/3) | (1,−1) | no | no | holds (S^d) |
| −N/3 | 3̄ | (1,0) | (3̄,−1/3) | (3,−2/3) | (1,−1) | no | no | **fails** |
| (3−N)/3 | 3 | (1,1) | (3,2/3) | (3̄,1/3) | (1,0) | no | no | holds |
| (3−N)/3 | 3̄ | (1,1) | (3̄,2/3) | (3,1/3) | (1,0) | no | no | **fails** |
| −(3−N)/3 | 3 | (1,−1) | (3,−2/3) | (3̄,−1/3) | (1,0) | no | no | **fails** |
| −(3−N)/3 | 3̄ | (1,−1) | (3̄,−2/3) | (3,−1/3) | (1,0) | no | no | holds |

- `any_option_reproduces_paper_Y = false`
- `any_option_reproduces_paper_table = false`
- 4 of the 8 options satisfy the correlation.

### C4: the paper's Y under the induced colours
| ρ | N=0 | N=1 | N=2 | N=3 |
|---|---|---|---|---|
| 3 | (1, 0) pass | (3, 1/3) **FAIL** | (3̄, −2/3) pass | (1, 1) pass |
| 3̄ | (1, 0) pass | (3̄, 1/3) pass | (3, −2/3) **FAIL** | (1, 1) pass |

### C5: pulls (3/13 = 0.230769230769…)
| reading | comparison x ± σ | z (unrounded) | z (3 dp) |
|---|---|---|---|
| sin | \|V_us\| = 0.22431 ± 0.00085 | +7.599095 | **+7.599** |
| sin | λ = 0.22501 ± 0.00068 | +8.469457 | **+8.469** |
| tan | 0.22431/0.97367 = 0.23037579 ± 0.00087626 | +0.448993 | **+0.449** |
| tan | 0.2250/0.97367 = 0.23108445 ± 0.00041778 | −0.754523 | **−0.755** |
| tan | λ/√(1−λ²) = 0.23093191 ± 0.00073512 | −0.221302 | **−0.221** |

Note for the leg comparison: pull (d) is −0.75452, only 2.3×10⁻⁵ from the −0.7545 rounding boundary. Doubles and 50-digit arithmetic agree, but rounding intermediate values (x or σ) changes the third decimal. Compare unrounded values.

### C6: Császár torus
- |Aut(face set)| = **42**, and it **equals AGL(1,7)** = {x → ax + b}.
- **21** automorphisms keep each 7-face family: multipliers a ∈ {1, 2, 4}, the quadratic residues. The other 21 (a ∈ {3, 5, 6}) swap the two families.
- Orientation class: s = +1 on every {i,i+1,i+3} face and −1 on every {i,i+2,i+3} face (increasing-order reference orientation).
- σ_# s = +s for all 42 automorphisms: **42 preserve orientation and 0 reverse it.** The 7-vertex torus map is chiral; x → −x is a half-turn.
- |Stab_{S₇}(family {i,i+1,i+3})| = **168**: this family is a Fano plane, and the stabiliser is its collineation group. Its intersection with Aut has **21** elements, the family-preserving automorphisms.

## Notes for comparison with leg 1
- The 3 versus 3̄ label of a sector is fixed by the choice of ρ. What does not depend on any labelling convention: N=0 and N=3 are singlets, N=1 and N=2 are mutually conjugate, and the two can never both be 3̄.
- The JSON pulls are rounded to 3 decimals. Full values are in `leg2_output.txt`.
- `MANIFEST.md5` lists md5 sums of the script, output, JSON and this report.
