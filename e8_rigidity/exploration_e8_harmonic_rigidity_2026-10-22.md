# E8 harmonic rigidity: Fano structure cannot move the octonion prime bias

*Exploration-mode entry of October 22, 2026, drafted for the author. **Status: REGISTERED at V4.102 (§2.102), on the author's word of October 22, 2026, 19:47 PDT ("Yes register").** Item 1 is R0; C1–C6 are R1, one leg, one environment; no two-leg run. The text below is revision 2 as registered; the ledger's §2.102 is the record of reference. (Original status line: DRAFT, unregistered; no lock, no two-leg run, no fold.) The theorem in §1 is R0 prior art. The corollaries in §2 are derived from it and machine-checked in §3. If the author registers them, the proposed register is R1. Check scripts: `claude/e8_harmonic_rigidity.py` (md5 `198f483e…`, 3,472 B) and `claude/fano_cP_check.py` (md5 `b9902b40…`, 5,365 B). Revision 2 (same day) folds in a Gemini review, as corrected in §6.*

## In plain language

The integral octonions of prime norm p form the E8 lattice shell of size 240(1 + p³). The October 22 prime experiments measured how those octonions lean toward the 240 units on S⁷, one harmonic degree at a time. This entry records why SQT's Fano and PSL(2,7) structure cannot change that picture.

At degree 8, *any* way of weighting the norm-n octonions gives Ramanujan's τ(n) times a single constant, and the 240 units alone fix that constant. Below degree 8 every weighting gives either zero or the plain count of the shell. The first degree where a weighting has any freedom is 20. Even there it only picks a mix of two fixed modular forms, and the shells of norm 1 and 2 already fix that mix.

The Fano structure does show up in one place, as a constant. Weighting by the 7 quaternion subalgebras gives a degree-8 constant of +6. The 28 non-line planes, rescaled to 7, give +3. That number is the whole of the Fano content at degree 8, and it is the same in all seven maximal orders.

So the Fano labelling can choose constants, but it cannot add arithmetic. This is the number-theory counterpart of two folded results:
- Paper II §3.4's locality result: an imported orientation attaches only to topology.
- G-VS1's transitivity lemma (§2.91.U, V4.88): G₂ cannot be told from SO(7) in a single-vector potential.

Here an imported orientation attaches only to constants the units already set. The one way out is to restrict the sum to a congruence class, which leaves level 1 (C6).

## 1. The theorem (R0)

**Weighted theta series.** Let Λ be an even unimodular lattice in ℝᵈ and P a harmonic polynomial of degree k > 0. Then

  Θ_{Λ,P}(q) = Σ_{x∈Λ} P(x) q^{|x|²/2}

is a cusp form of weight d/2 + k for SL₂(ℤ). This goes back to Hecke (*Analytische Arithmetik der positiven quadratischen Formen*, 1940) and Schoeneberg (1939). Ebeling, *Lattices and Codes*, ch. 3, has a textbook treatment. **[Hecke 1940 read: catalogue record; Schoeneberg memory; the statement and the Ebeling citation confirmed in Tasaka 2023, read]**

For E8 (d = 8) and with the octonion norm N(x) = |x|²/2:

| degree k | space | consequence for Σ_{N(x)=n} P(x) |
|---|---|---|
| odd | — | 0, since x ↦ −x |
| 2, 4, 6 | S₆ = S₈ = S₁₀ = 0 | 0 for every n: each shell is a spherical 7-design (Venkov) |
| 8 | S₁₂ = ℂΔ | **τ(n) · Σ_{units u} P(u)**, for every n |
| 10 | S₁₄ = 0 | 0 for every n |
| 12, 14, 16, 18, 22 | S₁₆, S₁₈, S₂₀, S₂₂, S₂₆, each of dimension 1 | a_f(n) for that single eigenform × a constant set by the units |
| 20 | dim S₂₄ = 2 | a mix of two eigenforms, fixed by the n = 1 and n = 2 shells |

The dimension-1 degrees (8, 12, 14, 16, 18, 22) are exactly the six panels of the October 22 E8 overlay.

**Polynomials that are not harmonic.** Any homogeneous polynomial Q of even degree 2m decomposes uniquely as

  Q(x) = c₀|x|^{2m} + Σ_{j=1}^{m} |x|^{2(m−j)} P_{2j}(x),

with each P_{2j} harmonic of degree 2j. Here c₀ is the average of Q over the unit sphere. Write the shell as N(x) = n with the units at |u| = 1, so |x|² = n. The pieces P₂, P₄ and P₆ sum to zero on every shell, so:

- For 2m ≤ 6: Σ_{N(x)=n} Q(x) = c₀ nᵐ · 240σ₃(n). A weighting of degree 6 or less can only rescale the plain count of the shell (the Eisenstein E₄ term).
- For 2m = 8: Σ_{N(x)=n} Q(x) = c₀ n⁴ · 240σ₃(n) + τ(n) · c_P, where c_P = Σ_{units u} P₈(u).

**Prior address for the degree-8 row.** Venkov's theorem, in Pache's Proposition B, says the 2m-shell of E8 is a spherical 8-design if and only if τ(m) = 0 (Lehmer's question). That is the degree-8 row read backwards. **[read via Tasaka 2023, which cites Pache 2005 and Venkov 1984/2001]** Nothing in §1 is new.

## 2. Corollaries for SQT (proposed R1)

All of C1–C5 are statements about **full-shell sums (level 1)**. C6 states the limit.

**C1. No Fano signal below degree 8.**
- The octonion orientation 3-form φ_{abc} has odd degree, so its sum over any shell vanishes. Evaluated on a single vector, φ(x, x, x) is identically zero anyway.
- Every Fano-line or PSL(2,7)-orbit weighting of degree ≤ 7 sums to zero on every shell if it is harmonic. If it is not harmonic, it sums to c₀nᵐ · 240σ₃(n) (§1).
- **G₂-invariant weightings are already the measured statistic.** G₂ acts transitively on the unit sphere S⁶ in Im 𝕆. So a G₂-invariant polynomial of one octonion depends only on Re x and |Im x|: it is zonal about 1. This is the single-vector case of G-VS1's transitivity lemma (§2.91.U, R1-machine), where G₂ and SO(7) have the same invariants on one vector of the 7.
- So a weighting that is genuinely Fano-specific has to break G₂ down to a finite line-preserving group. "The G₂-invariant degree-8 polynomial" is not a Fano probe. It is the zonal harmonic the October 22 experiment already measured.

**C2. Degree 8 is a single constant, and for the Fano lines it is nonzero.**
- For any degree-8 weighting P, Fano-built or not, the norm-n sum is τ(n)·c_P plus the plain count term of §1, with c_P = Σ_{240 units} P₈(u).
- The Fano weighting cannot change the n-dependence, the L-function (L(Δ, s)), the root number (+1) or the sign of the lean.
- Computed for the line weighting Q_lines(x) = Σ_{7 lines L} |proj_{span{1,e_a,e_b,e_c}} x|⁸: c_P = **+6**. The 7 imaginary 3-planes span{e_a,e_b,e_c} give +3.9375. The control, the 28 non-line 4-planes rescaled to 7 planes, gives **+3**. The Fano lines carry exactly twice the Δ-coefficient of the non-lines.
- Each shell is invariant under W(E8), and the W(E8)-invariant harmonics of degree 8 form a single dimension: the basic invariant degrees are 2, 8, 12, 14, 18, 20, 24, 30. So the shell sum sees only the averaged part of P, a multiple of c_P. This explains why there is one constant. It does not by itself give the τ(n) dependence; that needs §1's modularity. W(E8) does not contain G₂. The symmetry relevant to the Fano weighting is the finite group preserving each order (C3).

**C3. The seven maximal orders.**
- **Statistics measured from 1 are identical across all seven.** Every maximal order of integral octonions is a copy of E8 that contains 1 as a minimal vector. Any two copies of E8 are isometric, and W(E8) acts transitively on the 240 roots. So there is an isometry carrying one order to another and fixing 1. Every statistic depending only on N(x) and ⟨x, 1⟩, including the Re-direction distribution behind the October 22 bias measurement, is identical across the seven orders. Running the bias experiment in each order is a code check, not an experiment.
- **Line-built weightings are identical across all seven too.** Computed: of the 30 arrangements of 14 four-element blocks on {1, e₀, …, e₆} (each three points in exactly one block), exactly 7 give a unit set closed under multiplication. Those are the seven maximal orders. The 21 automorphisms of the form e_k ↦ ±e_{ak+b} (a ∈ {1, 2, 4}) preserve the Fano lines and permute the seven orders transitively. The 8 sign changes fix each order. So any weighting built from the lines, such as Q_lines, takes the same value in every order, as the computed c_P = +6 in all seven confirms.

**C4. The only freedom, at degree 20, is fixed by two shells.**
- S₂₄ has dimension 2. In the basis {ΔE₄³, Δ²} its normalised Hecke eigenforms are

    f_± = ΔE₄³ + (−156 ± 12√144169) Δ²,  with a(2) = 540 ± 12√144169,

  so their coefficients lie in ℚ(√144169) **[computed in `fano_cP_check.py`]**.
- A degree-20 weighting sets the ratio of f₊ to f₋.
- A cusp form of weight 24 is fixed by its q and q² coefficients (Sturm bound 2). So the n = 1 and n = 2 shells (240 and 2,160 vectors) fix that ratio. Measuring primes cannot reveal it. It is a finite computation.

**C5. Consequence for the octonionic-structure hypothesis.** On the E8 side, for full-shell sums, no PSL(2,7)- or Fano-derived weighting can produce a prime signal that the 240 units and two small shells do not already fix. This closes the full-shell octonion route for SQT. It does not close the number theory (§4).

**C6. The one opening: sums restricted to a congruence class.** §1 needs the sum over the *whole* norm-n shell.
- If an experiment sums only over x ≡ v (mod M), or over a sublattice, the theta series has level M > 1. Its modular group drops to Γ₀(M) or Γ(M), and new cusp forms appear: forms of level M, with their own L-functions and root numbers.
- C1–C5 then do not apply.
- Any future SQT experiment on octonion primes that splits a shell by a Fano-derived congruence (for instance by residues of the coordinates mod 2 or mod 7) is outside this entry. It would need its own pre-registration, with the level and the forms of that level computed before measuring.

## 3. Machine check (exploration mode)

`claude/e8_harmonic_rigidity.py` uses E8 in the even coordinate system and tests zonal harmonics about three directions: two random ones and (1,1,1,0,0,0,0,0). It enumerates the shells n = 1, 2, 3, 5, 7 and confirms sizes 240·σ₃(n) = 240, 2,160, 6,720, 30,240 and 82,560.

`claude/fano_cP_check.py` works in octonion coordinates with Fano lines (i, i+1, i+3) mod 7 (the §3.4-SIGNPHI convention, as in G-VS1). It builds the maximal orders and computes the Fano constants, the norm-2 shell check and the weight-24 eigenforms. It needs numpy and sympy.

| check | result |
|---|---|
| k = 2, 4, 6: normalised shell sums | ≤ 9 × 10⁻¹⁷ (zero to machine precision) |
| k = 8: shell sum / (τ(n) · root sum), n = 2, 3, 5, 7, all three directions | 1.0000000000 in every case |
| k = 20: shells n = 3, 5, 7 predicted from n = 1, 2 alone | relative error ≤ 2 × 10⁻¹³ |
| k = 20: mixing ratio y/x in the basis {ΔE₄³, Δ²} | +5.05 × 10³, −7.02 × 10³, −3.55 × 10³: different for each direction, as C4 says |
| 3-(8,4,1) block designs; how many give closed unit sets | 30; exactly 7 |
| permuting the 7 orders | 8 sign changes: each order fixed; 21 line-preserving automorphisms: transitive |
| c_P for Q_lines (7 associative 4-planes) | +6, in all 7 orders |
| c_P for 7 imaginary 3-planes / 28 non-line 4-planes (×7/28) | +3.9375 / +3, in all 7 orders |
| full degree-8 formula, Q_lines on the n = 2 shell (2,160 vectors) | direct sum 34,416; c₀·16·240·9 + τ(2)·c_P = 34,416 |
| S₂₄ eigenforms | a(2) = 540 ± 12√144169; f_± = ΔE₄³ + (−156 ± 12√144169)Δ² |

## 4. What this does not settle

- **The tower result stands.** This entry does not touch the October 22 finding that quaternion and octonion primes lean toward the units, degree by degree, with the sign set by the root number and by central vanishing. The degree-by-degree sign rule is itself known: Sarnak's 2007 letter to Mazur on Chebyshev's bias for τ(p), and Devin 2020. A write-up should present the geometric picture and its exact verification on S³ and S⁷ as an illustration of those results, not as a new theorem.
- **Summing over all degrees is open.** Rigidity holds degree by degree. Whether the lean converges as a whole cap-count bias near the identity, summed over all degrees, is not answered here. That is the part of the tower work that could be new.
- **Restricted sums are open** (C6).

## 5. Related exploratory observation (not a Phase B test)

The Phase B partitions spelled out in Entry 008 of the Phase B audit log are P5 = {1}|{2,…,6} and P4 = P7 = {3,5}|{1,2,4,6}, both on residues mod 7. They were applied to the October 22 consecutive-prime counts (pairs mod 455, primes to 10¹⁰ and 10¹¹), comparing the rate at which consecutive primes change block against the wheel–Cramér sieve model. They show the same 10⁻⁴-scale model residuals as the plain quadratic-residue split ({1,2,4}|{3,5,6}), with no Fano-specific excess.

This is outside Phase B's pre-registration (Entries 002, 006 and 007 concern 256-bit residue counts, not transitions). It is recorded as exploration only, with no test claimed. The sieve model is a correct null for consecutive-pair statistics. It does not resolve the Entry 007 null question for fixed-bit-length residue counts.

## 6. Review record

**Revision 2 (October 22, 2026, evening)** folds in five suggestions from a Gemini review. Each was checked before adoption:

1. **Citations.** Devin's journal record and Hecke 1940 were confirmed and adopted. Schoeneberg, *Math. Ann.* 116 (1939), 511–523, could not be confirmed and stays [memory]. Gemini's "Math. Ann. 114 (1937)" for Hecke was not adopted: those appear to be Hecke's operator papers, not the theta theorem. The review's weight-24 eigenform formula arrived blank, so it was computed here instead (C4).
2. **Polynomials that are not harmonic.** Adopted as stated, extended to degree 8 and checked on the norm-2 shell (§1, C1).
3. **A concrete Fano check.** Adopted with a correction. Both candidate weightings proposed fail: "Φ²(x)" is identically zero on one vector, and a G₂-invariant polynomial is zonal about 1, so it is the statistic already measured (C1). A line-projection weighting was used instead (C2). The review's W(E8) averaging remark was adopted, with the note that it explains the single constant but not τ(n), and that W(E8) does not contain G₂.
4. **The congruence caveat.** Adopted and strengthened from a qualifier into its own corollary (C6), because restricted sums are the one route the rigidity leaves open.
5. **The G-VS1 cross-reference.** Adopted; checked against the V4.88 fold authorization and the staging memo §2.4. Its useful consequence is the zonal reading in C1.

## 7. Registers and non-claims

Registered at V4.102 (§2.102). §1 is R0. §2's C1–C6 are R1 (derived from §1 and machine-checked in §3; one leg). §5 has no register. Nothing is deposited or sent. No claim is made about primes beyond §1's known results.

**Provenance.**
- Experiment bundle `prime_experiments.zip` (corrected version, October 22, md5 `7b5bf491…`): E8 bias overlay to p ≤ 2 × 10⁵ (`e8primes.py`, `e8_overlay.py`) and Legendre-flip counts (`pairs455_*`).
- The SQT-agent review of the same day caught two bundle errors, both since fixed by the other agent: the README's residual figure, now "about 10⁻⁴, model-limited", and the 10⁹ real-prime counts, which had been overwritten. The 10⁹ table was rerun from the corrected bundle and reproduces `flip_results.txt` exactly.
- The zero-divisor walk graph (`oq1_orbit_schedule_bfs.py`) was rebuilt and found irrelevant here. It has 42 ordered label pairs and is 20-regular, with spectrum 20¹, 6⁶, 0²¹, (−4)¹⁴. It is invariant under all of S₇ and uses no sedenion multiplication, so it carries no Fano or prime information.
- Cross-references: Paper II §3.4 (canonical v5); §2.91.U (G-VS1, folded at V4.88; `claude/FOLD_AUTHORIZATION_V4_88.md`; transitivity lemma at `claude/staging_memo_G_VS1_v2.md` §2.4).

## References

- Hecke, E., *Analytische Arithmetik der positiven quadratischen Formen*, Danske Vid. Selsk. Mat.-fys. Medd. 17, no. 12 (1940), 134 pp. [read: catalogue record].
- Schoeneberg, B., "Das Verhalten von mehrfachen Thetareihen bei Modulsubstitutionen", *Math. Ann.* 116 (1939), 511–523 [memory and review; not confirmed; check at lock].
- Ebeling, W., *Lattices and Codes*, Vieweg, 1994; 2nd edn. 2002, ch. 3 (weighted theta series) [memory; cited for this in Tasaka 2023].
- Venkov, B. B., "On even unimodular extremal lattices", *Trudy Mat. Inst. Steklov* 165 (1984), 43–48; *Proc. Steklov Inst. Math.* 165 (1985), 47–52 [via Tasaka 2023].
- Venkov, B. B., "Réseaux et designs sphériques", *Monogr. Enseign. Math.* 37 (2001), 10–86 [via Tasaka 2023].
- Pache, C., "Shells of selfdual lattices viewed as spherical designs", *Internat. J. Algebra Comput.* 15 (2005), 1085–1127, Prop. B [via Tasaka 2023].
- Tasaka, K., "The harmonic strength of shells of lattices and weighted theta series", arXiv:2308.14309 (2023) [read].
- Sarnak, P., "Letter to B. Mazur on Chebyshev bias for τ(p)" (2007), IAS publications page [read: record].
- Devin, L., "Chebyshev's bias for analytic L-functions", *Math. Proc. Cambridge Philos. Soc.* 169(1) (2020), 103–140, doi:10.1017/S0305004119000100 [read: journal record].
