# Step 3 pre-registration: the first stable closure

*Draft for the author, October 30, 2026. Label: Exploration. Written before any step 3 code is run. Follows the Oct 30 step 1 classification and step 2 results in `new-toe/`.*

## 0. What is being tested, in one sentence

Whether a closed loop of the three-strand composite vortex, held open by its own twist and gauge field, settles at a finite size instead of shrinking away.

## 1. The model (declared inputs)

Three complex fields ψ_k = f_k e^{iθ_k} (k = 1, 2, 3), equal charge e, one U(1) gauge field A, static energy in three dimensions:

E = Σ_k [ |(∇ − ieA)ψ_k|² + ½(|ψ_k|² − 1)² ] + ½ |∇×A|² − η Σ_{i<j} Re(ψ_i ψ_j*)

- **Units.** The coherence length ξ = 1 and the condensation energy set the length and energy units. Every output is a dimensionless ratio. No physical unit is chosen anywhere in step 3.
- **Penetration depth.** λ = 1/(e√3). Declared ratio κ = λ/ξ = 2 (primary); κ = 1 as a check.
- **Inter-strand coupling η.** Primary η = 0.1 (strands phase-locked, as in step 2). Secondary η = 0. Variant for later, not in this run: η < 0 on all three pairs, which locks the phases at 120° and gives a two-fold chiral ground state (Garaud, Carlström and Babaev, 2011 [memory]).
- **Assumption A1 (declared, not derived).** The three strands are interchangeable: equal charges, equal amplitudes, equal couplings. This is what makes the flux fractions exactly 1/3 and what allows a loop to close with its strands permuted.
- **Assumption A2 (declared).** The stabilizer is the twist of the relative phases plus the gauge field. No four-derivative term, no time dependence, no background.

## 2. Configuration

A closed loop (vortex ring) of radius R. Around the ring's core each ψ_k winds once (the composite (1,1,1) vortex of step 2). Along the ring, the **relative phases** θ_i − θ_j wind N times. N is the twist. It is topological because the relative-phase sector is neutral and its target space CP² has π₃ = ℤ.

Phases:
- **Phase A, axisymmetric.** Fields depend on (r, z); the twist enters as ψ_k ∝ e^{i n_k φ} with (n₁, n₂, n₃) = (N, 0, 0). No strand braiding. This reduces the problem to two dimensions.
- **Phase B, full 3D with braiding.** Only if Phase A returns STABLE or MARGINAL. The three fractional cores braid around the composite core by q/3 of a turn per circuit: q = 0 (parallel), q = 1 (closes as the (3,1) torus knot, an unknot), q = 2 (the (3,2) torus knot, a trefoil).

## 3. Method

- Finite differences on (r, z) ∈ [0, L] × [−L, L], L ≥ 6R, grid spacing h = 1/3, L-BFGS to gradient < 10⁻⁶, as in step 2.
- **E(R) curve (primary).** Pin the composite core at (R, 0) by Dirichlet zeros and minimize everything else. R ∈ {2, 3, 4, 6, 8, 12}.
- **Free relaxation (confirmation).** Start a ring at R = 8 with no pin and let it relax. Record whether R grows, shrinks or stops.
- Box-size check: repeat the key R values at L doubled.

## 4. Predictions and outcome map (written now)

| | Prediction | Outcome arm |
|---|---|---|
| P1 | N = 0: E(R) decreases monotonically as R → 0. An untwisted ring has only tension. | Control; must hold or the instrument is wrong. |
| P2 | N = 1, η = 0.1, κ = 2: E(R) has a minimum at R* with R* > 2ξ, and the minimum survives doubling the box. | **STABLE** |
| | E(R) decreases monotonically to core scale. | **COLLAPSE** |
| | Minimum at R* ≲ 1.5ξ, core-dominated. | **MARGINAL** (inconclusive; needs finer grid) |
| P3 | If STABLE: R*(N) grows with N. Record the exponent. The ungauged Faddeev model gives E ∝ N^{3/4}; this model has no reason to match it. | descriptive |
| P4 | If STABLE: the free relaxation from R = 8 stops at R* ± 10 %. | confirmation |

**My own prior, stated honestly:** the two-strand version of this model collapses (Jäykkä and Speight, 2011 [memory]: the supercurrent coupling that the Babaev–Faddeev–Niemi mapping drops destabilizes the knots). I give COLLAPSE about 60 %. A STABLE result would therefore be a real finding about the third strand and the η coupling, not a reproduction.

**Phase B prediction, if reached:** E(q = 2) > E(q = 1) > E(q = 0) at fixed N. No numerical value is predicted.

## 5. Eddington guard

- No particle mass, no m_p/m_e, no PDG number appears anywhere in step 3. The outputs are E(R)/E_core and R*/ξ.
- κ and η are fixed above, before any run. If COLLAPSE, no parameter is to be re-tuned in search of stability; a scan over (κ, η) would be a new pre-registration with its own label.
- "First stable closure" is a description of the configuration, not an identification with the electron. Any identification is a later step with its own tests.

## 6. Fallback

If COLLAPSE at both κ values and both η values: option 4 (a loop whose relative phase rotates in time at frequency ω, stabilized by the conserved charge, a vorton). That is a separate pre-registration.

## 7. Prior art to verify before interpreting (all [memory] until checked)

- Babaev, Faddeev, Niemi, Phys. Rev. B 65, 100512 (2002): two-component condensate ↔ Faddeev model; knotted vortex loops proposed.
- Jäykkä, Speight, Phys. Rev. D 84, 125035 (2011): those knots collapse in the full Ginzburg–Landau model.
- Jäykkä, Hietarinta, Salo (2008): numerical knots in the two-component GL model.
- Garaud, Carlström, Babaev, PRL 107, 197001 (2011): CP² skyrmions in three-band superconductors with 120° frustrated phases.
- Witten, Nucl. Phys. B 249, 557 (1985): superconducting strings. Davis, Shellard (1988–89): vortons.
- Krusch, Speight (2006): odd Hopf charge gives Finkelstein–Rubinstein fermions (already in the Seed survey).

## 8. Cost

Phase A: roughly 10–20 minimizations of ~10⁵ unknowns each; a few hours. Phase B: full 3D, days of compute, and likely a separate session.

## 9. Amendment A (October 30, 2026, before any step 3 run)

**What changed.** Phase A's axisymmetric ansatz ψ_k ∝ e^{i n_k φ} with (n₁, n₂, n₃) = (N, 0, 0) is withdrawn. Regularity on the symmetry axis forces ψ₁ = 0 along the entire axis, which is an infinite fractional vortex line through the ring. At η > 0 that line is linearly confined (step 2), so the configuration has energy growing with the box and is not a localized object. The E(R) test under that ansatz would be meaningless.

**Replacement.** The twisted ring is a localized configuration in which strand 1's own vortex loop links the (2, 3) composite ring N times; the Hopf charge is that linking number. At η > 0 the string of step 2 should pull strand 1's loop onto a helix wrapped N times per circuit around the composite core. No 2D reduction is available, because the Josephson term breaks the relative-phase symmetry the reduction would need. **Phase A is therefore a full 3D computation at modest resolution** (grid spacing h = 0.5 ξ-units, box 24, 48³ points), and Phase B is the same at higher resolution with the strand-permuting closures q = 1, 2.

**Initial conditions, fixed now.**
- N = 0 (control): all three strands wind once around a circle of radius R in the z = 0 plane.
- N = 1: strands 2 and 3 as above; strand 1 winds once around a circle of the same radius in the x–z plane centered at (R, 0, 0), so that the two loops form a Hopf link. A second start, strand 1 on a (1,1) helix of minor radius 2 around the ring core, is run as a check that both starts reach the same state.

**Model units, stated exactly.** E = Σ_k [ |Dψ_k|² + ½(|ψ_k|² − 1)² ] + ½(∇×A)² − η Σ_{i<j} Re(ψ_i ψ_j*), D = ∇ − ieA. With this normalization the coherence length is ξ = 1/√2 and the penetration depth is λ = 1/(e√6). κ = λ/ξ = 2 gives e = 1/√12. Lengths below are quoted in units of ξ.

**Predictions, re-stated for the 3D run.** P1 (N = 0): the free ring shrinks monotonically; the pinned E(R) decreases monotonically as R falls. P2 (N = 1): STABLE if the free relaxation from R = 6 stops at a finite radius R* > 2ξ, with strand 1's loop still linked, and the result survives a box of 64³; COLLAPSE if the ring shrinks to core scale or strand 1's loop unlinks by reconnection; MARGINAL otherwise. The pre-run prior (about 60 % COLLAPSE) stands.

**Run plan.** The N = 0 control runs now, in this session, as a calibration. The N = 1 runs are long and go to a Claude Code session against this branch.

## 10. Amendment B (October 30, 2026, after the first N = 1 run, before any rerun)

**Why.** The first N = 1 session (`REPORT_N1.md`, commit 470e78d) found two errors in the authoring session's scripts. Neither is a change of model, parameters or verdict rules.

1. **Start A touched the box.** Strand 1's loop (radius 6, centred at x = 6) reached x = 12, the face of the 49³ box, and stuck to it for iterations 2–16. The start A collapse at 49³ is therefore recorded as *inconclusive*, not as a verdict.
2. **Start B did not match §9.** The script placed a radius-2 circle in the y–z plane, which touches the composite ring instead of linking it (Lk = 0). §9 specifies a (1,1) helix of minor radius 2.

**Corrections, fixed now.**
- **Grid.** 65³ points (box half-width 16) for both starts. This was §9's box check size; it becomes the primary size. The 81³ box is the check, if a start does not collapse.
- **Starts** are built in `starts.py` from closed curves by the solid-angle phase (Ω/2), so each strand's vortex line is exactly the stated curve. Start A: the §9 Hopf-linked circle. Start B: the §9 helix. Verified before any run: both give |Lk(strand 1, composite)| = 1, and strand 1's line clears every box face by 3.75 (A) and 7.75 (B).
- **Diagnostics.** `trace_N1.py` (added in the first N = 1 session) is the run instrument, recording every 2 iterations, so the trajectory and the moment of unlinking are visible.
- **Recorded deviations from the first session:** 49³ rather than 48³ (now superseded by 65³); `linking.py` and `trace_N1.py` added; scipy installed by pip.

**Unchanged:** the model, κ = 2, η = 0.1, h = 0.5, R0 = 6, the verdict rules of §9, and the prior.

**Added interpretation rule, stated before the rerun.** If strand 1's line merges onto the composite core (closest approach below one grid spacing) and the configuration then shrinks, the run is COLLAPSE by the mechanism "the twist has no protected place to live where all three amplitudes vanish". The report must say whether that mechanism, or a different one, is what happened.
