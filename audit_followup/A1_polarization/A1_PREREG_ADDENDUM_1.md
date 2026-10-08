# A1 pre-registration — Addendum 1 (filed after the second leg returned, before the verdict record)

**Plain-language summary.** The independent second check raised five points about how the locked rules define a "tensor part". None changes the rule. This addendum records them and fixes, before the verdict is written down, how each is handled. The main one: the locked file gives two definitions of "tensor part" that agree in the case of record but can disagree when something small breaks the symmetry (texture of the grains, or the detector moving through the medium). The verdict is therefore evaluated under both definitions and both results are reported.

**Status.** The locked file `A1_PREREG.md` (md5 `d5f6aa3bd50743c5d69e54338494bb27`) is not edited. This addendum adds operational detail only. It was written after the second leg's return and after the first leg's derivation, so it is not blind to the outcome; that is why it may only add an evaluation, never remove one.

## The second leg's points and their handling

1. **The two definitions in §3 (spin weight in ψ; the TT projection Λ(k̂)) are equivalent only when the response map is covariant under rotations about k̂.** They differ when texture, a single-crystal response map or the detector's motion through the substrate breaks that symmetry: then Λ(k̂) of the effective response tensor can be nonzero while R(ψ) stays first-harmonic.
   - *Handling:* the verdict is evaluated under both readings. Reading S (spin weight, §3 first bullet) and reading Λ (TT projection, §3 second bullet). Under reading Λ, any nonzero projection is reported as a fraction f_T with its bound, and the rule's second clause (report the fraction and run the comparison) is applied to it.
2. **The direction k̂ is ambiguous at order v/c** (phase normal, ray direction, or apparent source direction) when the detector moves through the substrate.
   - *Handling:* under reading Λ the motion-induced fraction is reported for all three axes, and the largest is used.
3. **Normalization of e_l.** The dispatch fixed e_l = √2 k̂k̂, which differs from Isi & Weinstein's ŵ_z⊗ŵ_z.
   - *Handling:* both legs used the dispatch's convention, so the comparison is unaffected. Where patterns are quoted against the literature, F_l is stated with its normalization.
4. **F_l = −√2 F_b for an L-shaped detector**, so breathing and longitudinal patterns cannot be told apart by an interferometer.
   - *Handling:* the antenna classification reports "scalar" as one class; the six-tensor decomposition still separates b and l.
5. **The f_T normalization ("unit strain-equivalent") is undefined for a vector wave.**
   - *Handling:* f_T is defined as the power fraction of the TT projection, f_T = ⟨|Λ(k̂)T|²⟩ / ⟨|T|²⟩, averaged uniformly over sky position and polarization angle, where T is the effective response tensor (the tensor the detector contracts with D). This is the quantity both legs computed.

## The comparison under reading Λ (fixed now, before the verdict record)

If reading Λ yields a nonzero but bounded f_T, the comparison is: GW170817's network signal-to-noise ratio was 32.4 (LVC, PRL 119, 161101 (2017)). A tensor component with power fraction f_T contributes signal-to-noise ≈ 32.4·√f_T. If that is below 1, the tensor part is invisible in the data, the signal is effectively pure vector, and the pure-vector comparisons of the locked §4 apply unchanged.

## Honesty items opened by this addendum

- **H-A1-1 (exposure).** The second leg's summary reached the first leg before the first leg's code existed. The first leg's classification had been reasoned before the dispatch, but it was not written to a file before the return. The comparison is numerical on a common grid of 1,680 values and the two legs use different constructions, so the exposure could not have produced agreement by copying. It is recorded so that the independence claim is not overstated.
- **H-A1-2 (tooling).** The first leg's first run used `sympy.simplify` on trigonometric identities. It failed to reduce a true identity (the basis Gram matrix) to zero and took 7.5 minutes. The script was rewritten with the half-angle rational parametrization, where every identity is decided exactly by `cancel`. No physics changed. The second leg met the same tooling failure independently and fixed it the same way, by an exact reduction.
