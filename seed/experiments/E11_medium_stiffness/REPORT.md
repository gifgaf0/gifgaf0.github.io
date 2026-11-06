# E11 report: stiffness from the medium's units — verdict under the stopping rule

*November 4, 2026. Label: Exploration. Applies PLAN.md §4 to the unit model fixed in PLAN.md §7 (commit bdbbe70) before any derivation. Script: `e11_gradient.py`; output: `e11_D1_N48.json`.*

## 1. Verdict

| criterion | result |
|---|---|
| **D1** (gradient expansion derived and checked against the lattice to 1 %) | **PASS** |
| **D2** (positive four-derivative stiffness, positive definite, on an open set) | **FAIL as written.** The derived quartic form is not positive definite for any J, K > 0. A physically motivated reading passes; see §3. |
| **D3** (the needed sign was specified beforehand) | **PASS.** The author fixed "linking costs the medium energy" before any coefficient was computed. |
| **D4** (acts on the neutral, unscreened sector) | **PASS in the two-component (CP¹) sense only.** The term depends only on the director n, which carries no supercurrent. The chosen unit (S³) gives a CP¹ director, not E9's three-strand CP² (§4). |

**Under PLAN §4 read literally, the attempt FAILS (D2).**

## 2. Derivation (D1)

**Lattice energy (PLAN §7):**

E = J Σ_links (1 − n·n′) + K Σ_plaquettes (1 − cos(Ω_p/2)).

**Alignment term.** Use 1 − n·n′ = ½|n′ − n|², which is exact for unit vectors. Expand n′ − n = a∂n + a²∂²n/2 + a³∂³n/6 + …, and integrate by parts (∂n·∂²n is a total derivative, and ∂n·∂³n → −|∂²n|²). This gives

  J Σ_links (1 − n·n′) = J ∫ [ ½ Σ_μ |∂_μ n|² − (1/24) Σ_μ |∂_μ² n|² ] + O(a⁶).

**Linking term.** The plaquette solid angle is Ω_p = a² F_μν + O(a⁴), with F_μν = n·(∂_μn × ∂_νn), the curvature of the Hopf connection. So

  K Σ_plaq (1 − cos(Ω_p/2)) = K ∫ (1/8) Σ_{μ<ν} F_μν² + higher order.

This is the **Faddeev term**, with coefficient K/8.

**Numerical check.** A localized Hopf-charge-1 texture of size L on a 48³ lattice, with the continuum integrals evaluated on the same box (4th-order differences on a grid 4× finer):

| L | alignment, 2nd order only | alignment, + 4th-order term | linking vs F²/8 |
|---|---|---|---|
| 2 | −29.1 % | +7.2 % | −9.3 % |
| 3 | −12.7 % | +1.4 % | −1.7 % |
| 4 | −7.1 % | **+0.43 %** | **−0.78 %** |
| 5 | −4.5 % | +0.18 % | −0.44 % |
| 6 | −3.1 % | +0.084 % | −0.28 % |

- With the 4th-order term included, the alignment error falls as L⁻⁴ (16.5 × from L = 3 to 6, against 2⁴ = 16).
- The linking error falls as L⁻² (the next order).
- Agreement is under 1 % for L ≥ 4. **D1 passes.**

## 3. D2

**As written: FAIL.** The quartic form is

  Q₄ = (K/8) Σ F_μν² − (J/24) Σ_μ |∂_μ² n|².

Take any planar texture (n confined to a great circle, e.g. n₃ = 0). Then F ≡ 0, because ∂_μn × ∂_νn is parallel to e₃ and so orthogonal to n. Meanwhile |∂²n|² > 0, so Q₄ < 0 for every J, K > 0.

Nearest-neighbour alignment always contributes the negative term (PLAN §2 says so). The linking term cannot cancel it in directions where F vanishes. Only an |∂²n|²-type positive term, such as one from frustration, could do that, and the author's coupling does not supply one.

**Physical reading (post-hoc; not the rule).**
- The negative term is a lattice-scale effect. The true lattice energy is bounded below (1 − n·n′ ≥ 0), so it causes no instability by itself.
- What matters for a closure is the Derrick balance of **Hopf-charged** textures. From the table, with coefficients identical at L = 5 and 6 to 4 digits:

  E(L) ≈ J·100.7·L + (69.3 K − 113.1 J)/L.

- So a size minimum exists when **K/J > 1.63**, at L*² = (69.3K − 113.1J)/(100.7J).
- L* ≥ 3 lattice spacings needs **K/J ≳ 14.7**. This is an open set of couplings.
- **Caveat:** this uses an ansatz, not a relaxed solution. It is a Derrick estimate, not a stability proof.

**What that reading amounts to.** The continuum model it gives, ½J|∂n|² + (K/8)F², is the **Faddeev–Niemi (Faddeev–Skyrme) model**. Its stable knotted solitons (hopfions) are already known [memory: Faddeev and Niemi, Nature 387, 58 (1997); Battye and Sutcliffe, PRL 81, 4798 (1998); to verify]. So the generous reading leads to known physics: the author's medium, with linking that costs energy, *is* a Faddeev-type medium.

## 4. D4

- **What passes.** The linking term depends only on the director n. In the two-component (Babaev–Faddeev–Niemi) picture, n is gauge-neutral and carries no supercurrent. Unlike the Faddeev piece hidden in the gauge field's own energy, this term cannot be screened by the current, because the current never enters it.
- **The mismatch.** The unit fixed in §7 is an S³ rotor, so its director lives in S² = CP¹: the natural partner of a **two**-component condensate. E9's three-strand neutral sector is CP². The matching unit would be S⁵/ℤ₃ (three complex components, with a director in CP² and the Faddeev term built from CP²'s Kähler form). That is a different unit model, a second attempt, which PLAN §4 does not allow.
- **ℤ₃ does not enter the stiffness.** The energy depends only on n, which is invariant under the fibre phase. The ℤ₃ (the "third") would enter through the defects (ℤ₃ strings, π₁(L(3,1)) = ℤ₃), not through what holds a loop open.

## 5. What this establishes

- **The author's medium has a precise continuum form.** Units are S³ orientations with ℤ₃ along the fibre. Tautness is an alignment cost, and fibre linking costs energy. The continuum is a σ-model plus the Faddeev term, with the stiffness ratio K/J set by the linking cost against the tautness. Derived and checked (D1).
- **Under the pre-registered rule the attempt fails (D2):** the derived quartic form is not positive definite.
- **Under a post-hoc physical reading it succeeds, but onto known ground.** The medium is the Faddeev–Niemi model, in which stable knotted closed loops are already known to exist.
- **Either way, the thirds do not come from the stiffness.** ℤ₃ acts on the fibre phase, which the stiffness ignores. In this picture the thirds belong to the defects (Route C), not to what stabilizes a closure.

## 6. Consequence

**By PLAN §4 the closure line ends here.**

What it leaves, for the author's picture:
1. **A taut medium of Hopf units whose linking costs energy is a Faddeev-type medium.** Stable closed knotted loops are known to exist in such media. So "first stable closure" has a consistent home in the picture: Faddeev–Niemi hopfions. It is not a new object, and it does not carry thirds.
2. **The thirds, if they come from the ℤ₃ gluing, live in the defects:** ℤ₃ strings, which can meet three at a junction (Route C, untested).
   - A future direction that combines both would be ℤ₃ strings in a Faddeev-type medium.
   - That would be a new programme with its own pre-registration. It is not a continuation of this one.
