# E11: stiffness from the medium's units — plan and stopping rule

*November 4, 2026. Label: Exploration. Written before any derivation. This is the single bounded attempt agreed after `../SYNTHESIS_E9_E10.md` §6. If it fails the stopping rule (§4), the closure line ends with a closure note.*

## 1. Why this, and only this

E9 and E10 showed two things:
- Twisted loops collapse when nothing stiffens them against shrinking.
- Charge-supported loops lose to bulk Q-balls.

The direction those results leave open is a stiffness that the gauge field cannot screen and that we do not choose. It has to be **derived** from a model of the medium's units, with its form and coefficient fixed by that model. A stiffness added by hand would be the Eddington move: the four-derivative option rejected in E9 for that reason.

## 2. The mechanism a derivation could produce (what to look for)

A lattice of units with only nearest-neighbour alignment has a gradient expansion whose four-derivative correction has the **wrong sign**. For example, −J cos(a∂θ) expands to Ja²(∂θ)²/2 − Ja⁴(∂θ)⁴/24 + …, so it does not stop shrinkage.

**Competing interactions** do something different. An example is nearest-neighbour alignment plus next-nearest-neighbour anti-alignment (frustration). This can make the four-derivative term **positive** while keeping the two-derivative term positive. Under Derrick scaling the four-derivative term grows as 1/L, so it stops collapse.

Frustrated magnets stabilize knotted solitons by exactly this route [memory: Sutcliffe, PRL 118, 247203 (2017); to verify].

**Honest scope.** The mechanism is known. What a successful derivation would add is two things:
- that the author's units imply such competing couplings, rather than having them chosen;
- how the resulting term acts on the three-strand fields (it must act on the neutral sector, which the gauge field does not screen; see `../E9_three_strand_closure/NOTE_chiral_term.md` §4 and Addendum A).

## 3. What must be fixed before the derivation (author's input)

1. **What a unit is:** its degrees of freedom and target space.
   - For example, an oriented 3-sphere element (a rotor), whose Hopf fibration gives a direction plus a phase.
   - Or a torus–dual-torus (Heegaard) pair.
   - Or something else.
2. **How neighbouring units couple:**
   - which geometric relation is favoured (alignment, linking of fibres, sharing of cycles);
   - the range of the coupling (nearest neighbour only, or also next-nearest);
   - the sign of each coupling.
3. **Handedness:** whether one chirality dominates, which feeds the chiral term of `NOTE_chiral_term.md`.
4. **Lattice:** which lattice the units sit on, or whether they form a disordered packing. If the author has no preference, the simple cubic lattice is the default, recorded as a choice.

These are fixed **from the picture**, in writing, before any expansion is computed. Changing them after seeing the derived coefficients would be a new attempt, and §4 allows only one.

## 4. Stopping rule (fixed now)

The attempt **SUCCEEDS** only if all four hold:

- **D1.** With the inputs of §3 fixed, the continuum expansion to fourth order in gradients is derived. It is checked symbolically and numerically against a lattice computation of the energy of slowly varying textures, with agreement to 1 % at small wavenumber.
- **D2.** In the derived continuum energy, the two-derivative stiffness is positive and the leading four-derivative stiffness is **positive definite** on an **open** set of the couplings that §3 allows. It must not be a single tuned point.
- **D3.** The sign pattern needed for D2 (for example, anti-aligning next-nearest neighbours) is **the one §3 already specified**, not one introduced afterwards.
- **D4.** When the units are identified with the three-strand order parameter of E9 or E10, the stabilizing term acts on the **neutral** sector, the one that does not couple to the supercurrent. It is therefore not screened by the gauge field, at least at leading order, by the A·S-type analysis of `NOTE_chiral_term.md` §4.

**Outcomes.**
- **If all four hold:** one loop pre-registration follows, with the derived coefficients and nothing re-tuned. It reuses E9's twisted-ring setup and controls (including the γ-type parity control if handedness enters).
- **If any fails:** a closure note is written. "First stable closure" then requires an ingredient outside standard gauge-and-scalar field theory and outside this unit model. **The closure line ends.** No second unit model is tried under this plan.

## 5. Cost

D1 and D2 are a symbolic gradient expansion plus a small numerical check: a day, mostly derivation. D4 is a short analytic argument. Nothing here needs CC until a loop pre-registration exists.

## 6. Prior

Given the author's units, the chance that D1–D4 all hold is **about 25 %**. The main risk is D3: frustration has to come from the picture, not from the need for stability.
