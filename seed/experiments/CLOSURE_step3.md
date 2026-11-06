# Step 3 closure: the first-stable-closure line for fractional-flux strings ends

*November 4, 2026. Label: Exploration — closure note. Written under the stopping rule of `E11_medium_stiffness/PLAN.md` §4, which E11 triggered (`E11_medium_stiffness/REPORT.md`). Append-only: nothing below revises a recorded verdict.*

## 1. The question that is being closed

Step 3 of the Seed asked whether a **closed loop of a string carrying one third of a flux quantum** can be a stable, finite-size object, and whether the thirds play a part in holding it open. It was tested in two field theories and with four kinds of stabilizer, every test pre-registered.

## 2. The record

| route | model | stabilizer | verdict | where |
|---|---|---|---|---|
| A | three-component GL, one U(1) gauge field | Hopf twist + gauge field | **COLLAPSE**, all four (κ, η) cells, both starts | `E9_three_strand_closure/REPORT_N1*.md` |
| A | as above + core field σ | current and charge (vorton) | ring held open by σ alone; string costs energy; **string not required** | `E9_three_strand_closure/REPORT_phase1.md` |
| A | locked model | chiral term γψ*·(D×ψ) | **COLLAPSE**, all 12 runs; no handedness preference | `E9_three_strand_closure/REPORT_chiral_loop.md` |
| B | U(3) non-abelian vortices (λ only) | current and charge | ring **METASTABLE**; a vortex-free Q-ball of the same charge is cheaper; binding of lumps **TRACKS** the string's window | `E10_u3_vortices/REPORT_B4.md`, `REPORT_QB.md` |
| — | medium of S³/ℤ₃ units, tautness J + linking cost K | stiffness derived from the units | D1 pass, **D2 fail** as pre-registered (quartic form not positive definite), D3 pass, D4 pass for CP¹ only | `E11_medium_stiffness/REPORT.md` |

The combined account of E9 and E10 is `SYNTHESIS_E9_E10.md`; E11 is the one bounded attempt that synthesis §6 left open.

## 3. Conclusion

**Within standard gauge-and-scalar field theory, and within the one unit model the author fixed, no pre-registered test produced a stable closed loop of a fractional-flux string in which the string or its thirds do the stabilizing.**

- **Twist alone does not hold a loop.** A protected Hopf twist collapsed in every cell.
- **Charge can hold a loop, but it prefers to hold itself.** In both routes the charge binds more cheaply without the string; in Route B the two abilities share a cause.
- **A stiffness derived from the medium is a Faddeev term**, and it does not see the thirds. The ℤ₃ acts on the fibre phase, which the stiffness ignores.

Per `E11_medium_stiffness/PLAN.md` §4, **the closure line ends here.** No further stabilizer, unit model, or parameter scan is run under step 3.

## 4. What survives, independent of the closure question

1. **No-go for relative-phase vortons in Route A** (`SYNTHESIS_E9_E10.md` §3.1).
2. **The thin-ring identity** ℰ = 2T − 𝒯, so at equilibrium ℰ/q = T/(ωI), and a charged ring beats dispersal only if T/I < m². This is Carter's vorton condition in another form (`SYNTHESIS_E9_E10.md` §3.2).
3. **Route B: the string's charge window and the bulk Q-ball switch on together** at λ ∈ {0.8, 0.9, 1.0} (`SYNTHESIS_E9_E10.md` §3.3).
4. **A microscopic origin for the Seed's Model C.** E11 derived, and checked to under 1 % on the lattice, that a medium of S³ units with tautness J and a linking cost K has continuum energy

   ½J|∂n|² + (K/8) Σ_{μ<ν} F_μν²,  F_μν = n·(∂_μn × ∂_νn).

   This is the Faddeev–Skyrme model that `E8_hopfions` already solved (Model C), with the Faddeev length ℓ = √(K/4J) lattice spacings. So the Seed's knotted folds of E8 now have a stated origin in the author's picture of the medium: **linking of neighbouring units costs energy.**
   - **Caveat 1.** This uses the post-hoc "physical" reading of D2 that E11 did not adopt. The negative −(J/24)|∂²n|² piece is a nearest-neighbour lattice term. E8's own lattice also uses nearest-neighbour links and its hopfions relax normally, which supports that reading, but it is not a pre-registered result.
   - **Caveat 2.** These hopfions are two-component (CP¹) objects. They are not fractional-flux strings, and they carry no thirds.

## 5. Forecasts

The step-3 forecasts and outcomes are tabulated in `SYNTHESIS_E9_E10.md` §5. E11's prior (PLAN §6) was about 25 % for D1–D4 all holding. The risk named there was D3; the failure came instead at D2, from the nearest-neighbour term that PLAN §2 had flagged in advance.

## 6. Left open, not continued

None of these is a continuation of step 3. Each would be a new programme with its own pre-registration.

- **Route C: ℤ₃ strings.** In the unit model, the gluing L(3,1) = S³/ℤ₃ gives π₁ = ℤ₃, so strings of one-third winding exist and three can meet at a junction. This is where the thirds live in the author's picture. Untested.
- **ℤ₃ strings in a Faddeev-type medium**, combining Route C with item 4 above.
- **A three-component unit** (S⁵/ℤ₃, director in CP²), the unit that would match E9's three strands. Excluded here by the one-attempt rule.
- The untested items in `SYNTHESIS_E9_E10.md` §4: the semilocal Route A model, braided strings where reconnection is forbidden, the chiral helical regime, non-axisymmetric stability of the Route B ring, and quantum effects.

No particle identification is made or implied anywhere in step 3.
