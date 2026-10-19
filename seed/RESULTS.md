# Seed experiments: results

*October 19, 2026. Nine experiments testing SEED.md, run against the preregistration in `PLAN.md` (committed at `0dcd3fe`, before any of them was run). Every headline number was computed twice, by two agents with separate code; the second did not read the first one's code until its own numbers were in. Disagreements were settled in the open: each experiment folder has its `REPORT.md`, `crosscheck/CROSSCHECK.md` and, where needed, `RECONCILE.md`.*

## The short answer

No set of experiments can prove a theory of everything, and these don't. What they do show:

1. **The seed's mathematics is right.** Every computable claim in §3 holds in exact arithmetic, with no floating point anywhere (E0, 110 checks). One closing sentence gets a wording refinement, not a correction.
2. **The three starter models behave as published.** The tools reproduce the literature for φ⁴ kinks, Skyrme baryons, Faddeev–Hopf knots and gravitating skyrmions, usually to better than 1% (table below). Whatever the seed builds on these tools rests on working instruments.
3. **Most of the seed's specific claims hold.** The SU(3) fold is a fermion exactly when N_c is odd; a G₂ fold is always a boson; the lowest SU(3) fold states are the octet and the decuplet; folds appear only in pairs, never below twice the fold energy; pair production from colliding packets has a ragged boundary, not a threshold; the Q = 7 knot is a trefoil; knot energy grows like Q^{3/4}; fold charges come out as integers; one cone; the equivalence principle; a self-gravitating fold exists.
4. **Several need amending.** "Within roughly 30%" misses g_A by 52%. Packets fold by amplitude, not by energy, and a single tall packet folds on its own. Pulse trains make pairs in a velocity band, not "most easily at low speed". The order-21 group alone yields no masses and no viable mixing. "Energy bends the cone" should read "stress-energy bends the cone": a fold's gravitational binding is 1.29 times the energy-only estimate.
5. **The places a theory of everything has to reach are far away, and now measured.**
   - An electron-like fold misses the size condition by at least 3.5 × 10⁶, and the coupling it would need (Skyrme e ≈ 1.6 × 10⁴) is far past the point where a fold is a classical shape at all.
   - Electron pairs form readily in nature because QED is weakly coupled and perturbative (Breit–Wheeler peaks at 170 mb). A fold-like process at α = 1/137 would be suppressed by about 10⁻²²⁹. So §8's inference from easy pair production to a strongly coupled fold sector doesn't hold.
   - The graviton cannot be a composite of the fold field in a theory with a Lorentz-covariant conserved stress tensor (Weinberg–Witten), which commitment 1 assumes. The metric of commitment 5 has to be put in.
   - The vacuum's tension is (2.24 meV)⁴, between 10⁴² and 10¹²³ times smaller than any natural scale in the seed.
   - The order-21 family symmetry predicts nothing until vacuum alignments are chosen by hand.
   - Gravity changes a single fold by about one part in 10³⁹.

**Where that leaves the seed.** It is a consistent arrangement of known physics: topological baryons as in QCD's Skyrme limit, general relativity, Hopf knots, finite flavor groups. Its distinctive 60° structure is confirmed as mathematics and lives where the seed puts it, in the internal space. It does not yet contain a prediction that differs from established physics, and it has no route yet to the electron, the quark and lepton spectrum, or the size of the vacuum energy.

## Verdicts by seed claim

Verdict words as defined in PLAN.md §1. "By construction" means the result is built into the setup (for example, a Lorentz-invariant Lagrangian), so the check confirms consistency rather than testing nature.

| SEED | Claim | Verdict | Evidence |
|---|---|---|---|
| §2 | One speed; no vacuum dispersion | CONFIRMED (by construction) | E5: photon ω = \|k\|, pion ω² = k² + m², no mixing; the Skyrme and Wess–Zumino terms have no quadratic part |
| §2 | Equivalence principle | CONFIRMED (by construction) | E6: M_ADM/E_flat = 1 − 4.6 × 10⁻¹² as α → 0 |
| §2 | Conserved matter (topological charge) | CONFIRMED in every computed fold | E3: B = 1.0000000000; E8: Hopf charges within 0.004 of integers at Δx = 0.1 |
| §2 | Pairs; threshold twice the lightest fold | CONFIRMED | E1: no production below 2M in 19,526 packet runs (three codes); every event is a pair. 2M is also the exact classical floor: time-reversed slow captures make pairs from kink-free data at 1.001 × 2M, but only when tuned beyond 10⁻⁸. In the scanned families production starts higher (1.86 × 2M for Gaussian packets, 7.8 × 2M for DSV trains) |
| §2 | Spin ½ from SU(3) exactly when N_c is odd | CONFIRMED (given the Wess–Zumino quantisation rule, which was imported) | E2: every allowed state has 2J ≡ N_c mod 2, N_c = 1…15 |
| §2 | G₂ folds are only bosons | CONFIRMED | E3: integer J in every allowed state up to dimension 500; exp(2πT₃^long) = exp(2πT₃^short) in G₂ |
| §2 | S² knot folds can be fermions (π₄ = ℤ₂) | AMENDED (literature) | Only for odd Hopf charge (Krusch & Speight 2006); PLAN §3 |
| §3 | Torus, K₇, two Fano families, octonion lines, F₂₁, PSL(2,7), quartics, maximality, Weyl groups, p6m | CONFIRMED (exact) | E0, 110/110 exact checks; independent cross-check 81/81 and 88/88 |
| §3 | "They don't stack into one clean tower" | CONFIRMED, wording refined | E0: the chain G₂ ⊃ SU(3)⋊ℤ₂ ⊃ PGL(2,7) ⊃ PSL(2,7) ⊃ F₂₁ exists; the family-swapping turns enter at PGL(2,7) |
| §4 | Derrick: something must push back | CONFIRMED | E2: E₂(μ) = E₂/μ without the Skyrme term; with it E₂ = E₄ to 4 × 10⁻¹³ |
| §4 | A small packet passes through | CONFIRMED | E1: no packet with amplitude A ≤ 0.3 produces, up to about 15 × 2M |
| §4 | Pile in enough energy and the packet folds | AMENDED | E1: amplitude decides, not energy (at fixed energy the producing fraction runs from 0 to about 0.8). A single packet with A ≳ 0.4 folds with no collision at all, as an over-barrier estimate predicts (A > √2 − 1 = 0.414) |
| §4 | Colliding pulse trains make pairs over a wide range, most easily at low speed (DSV 2008) | AMENDED | E1: the wide range holds and DSV's map is reproduced in outline; but at each pulse frequency production sits in a velocity band, and the band moves to lower speed as the pulses weaken. It is never easiest at low speed |
| §4, §7.1 | The pair boundary is ragged | CONFIRMED | E1: almost every line of fixed width or wavenumber switches production on and off repeatedly as amplitude rises (57 of 57, 48 of 53), in both codes; exact region counts depend on resolution, so they are illustrative |
| §4 | E ≥ c Q^{3/4}; computed minima follow it | CONFIRMED for Q ≤ 7; optimality is a theorem | E8: E/Q^{3/4} = 1.19–1.25; fitted exponent 0.764 over Q = 1–7 (Sutcliffe's table: 0.763). Optimality of 3/4 is Lin & Yang 2004 |
| §4, §6C | Lowest knots are rings; Q = 7 is a trefoil | CONFIRMED (one start per charge; global minimality rests on Sutcliffe's survey) | E8: types A₁,₁ … K₃,₂; Q = 7 position curve has Alexander polynomial t² − t + 1 |
| §4 | Bigger folds store charge more cheaply | CONFIRMED | E8: E/Q falls 1.22 → 0.76 from Q = 1 to 7; E₂/(2E₁) = 0.82 |
| §5 | Gravity is the cone; light bends around a mass | CONFIRMED (by construction) | E6: deflection → 4GM/b outside the fold |
| §5 | Energy bends the cone | CONFIRMED, wording refined | E6: the O(α) mass defect is −G∫(ρ + p_r) m/r dV, 1.29 × the energy-only Newtonian value: stresses gravitate |
| §5, commitment 1 | The vacuum is taut, p = −ρ, frame-free | CONFIRMED (by construction); its value is free | E5 |
| §6B | Quantised rotations give the octet and decuplet | CONFIRMED | E2: lowest allowed multiplets 8 (J = ½), 10 (J = 3/2); next the exotic 10̄ (J = ½) at 1757 MeV, which is not observed |
| §6B | Exact SU(3): one mass per multiplet | CONFIRMED | E2 |
| §6B | Nucleons within roughly 30% | AMENDED | E2, E5: g_A 52% low; μ_p, μ_n, g_πNN 31–33% low; 3 of 7 finite nucleon quantities strictly within 30%, 6 of 7 within 33%; charge radii diverge with massless pions |
| §7.2 | Swap in G₂ | New results | E3: 1 (J = 0), then 14 (J = 1) 709 MeV higher, then 27 (J = 0); the 7 is forbidden; minimality of the embedded fold is OPEN |
| §7.2 | Flag space: hexagonal moment image, π₂ = ℤ², π₃ = ℤ | CONFIRMED | E3 |
| §7.3 | The order-21 group does a job for three generations | AMENDED | E4: restricts couplings, gives no masses without breaking; no residual-symmetry pattern of F₂₁ fits data (best χ² = 2459); patterns that fit need PSL(2,7)'s order-2 elements; with complex couplings no alignment class both fits and predicts, with real couplings three classes survive with a weak δ_CP prediction |
| §7.4 | Gauge a U(1): fold charges | CONFIRMED | E5: every state of 8, 10, 10̄, 27 has integer charge; Q = I₃ + Y/2 |
| §7.4 | π⁰ → γγ from the fold's Wess–Zumino term | CONFIRMED | E5: 7.761 eV vs PrimEx-II 7.802 ± 0.117 eV; N_c = 1 excluded (with fixed quark charges). At the fold's own fitted f_π the width is 2.0–2.6 times too large |
| §7.5 | A self-gravitating fold | CONFIRMED | E6: solutions up to α_crit = 0.0403785253 (target 0.040378); two branches, the upper one radially unstable |
| §8 | Size: the electron is no classical fold | QUANTIFIED | E7: λ_C/R ≥ 3.5 × 10⁶ (LEP; model-dependent bound) |
| §8 | Coupling: points to a strongly coupled fold sector | AMENDED | E7: strong coupling is necessary but leaves no classical fold (corrections 10⁶–10¹³ × the classical mass); QED pairs are perturbative, not fold-like |
| §8 | Folding a few quanta into a pair is exponentially rare at weak coupling | CONFIRMED (from the literature, with the classical scaling computed) | E1: classical production needs of order m²/λ quanta (the fewest found: N = 1.24 m²/λ; energy alone requires ≥ ⅔ m²/λ). E7: the two-particle suppression is exp(−F/g²) with F = 3.84–4.48, read from Demidov & Levkov's figures |
| §8 | The vacuum's tension | QUANTIFIED | E7: ρ_Λ = (2.24 meV)⁴; f_π⁴/ρ_Λ = 2.9 × 10⁴², M_Pl⁴/ρ_Λ = 8.8 × 10¹²² |
| §8 | Can the cone be built from the field? | AMENDED | E7: a composite graviton is excluded (Weinberg–Witten); a neutral composite photon is not |

## Calibration: the instruments work

| Experiment | Quantity | Ours | Literature | Status |
|---|---|---|---|---|
| E1 | kink mass; shape mode | 2√2/3, √(3/2) to 10⁻⁸ | exact | CALIBRATED |
| E1 | kink–antikink critical velocity | 0.26006 (independent code 0.260066) | 0.2598 [summary] | CALIBRATED (offset is in the quoted target) |
| E1 | first two-bounce window | [0.19257, 0.20344] | [0.1926, 0.2034] | CALIBRATED |
| E1 | DSV breather trains: band trend, pass-through, hole at (0.91, 0.82), nothing above ω = 0.99 | all reproduced; 58 of 81 DSV producing points hit | Dutta, Steer & Vachaspati 2008, Fig. 2 | CALIBRATED |
| E1 | DSV example point (0.99, 0.43) | chaotic: the outcome is decided at t ≈ 850, after the finest runs diverge; (0.99, 0.41) is a converged producer | DSV 2008 | OPEN |
| E2 | hedgehog mass | 36.4616 F_π/e | 36.5 (ANW), 36.44 (Schechter–Weigel) | CALIBRATED |
| E2 | moment of inertia Λ | 50.979 | 50.9 | CALIBRATED |
| E2 | ANW fit | F_π = 129.26 MeV, e = 5.444 | 129, 5.45 | CALIBRATED |
| E2 | g_A | 0.6105 | 0.61 | CALIBRATED |
| E2 | strange inertia I₂ | 40.68/(e³F_π) | 40.5 (arctan ansatz) | CALIBRATED |
| E5 | isoscalar charge and magnetic radii | 0.594, 0.922 fm | 0.59, 0.92 fm | CALIBRATED |
| E5 | μ_p, μ_n | 1.878, −1.323 | 1.87, −1.31 | CALIBRATED |
| E5 | π⁰ → γγ | 7.761 eV | 7.802 ± 0.117 eV (PrimEx-II) | CALIBRATED |
| E6 | critical gravitational coupling | 0.0403785253 | 0.040378 | CALIBRATED |
| E8 | knot energies Q = 1–7 at Δx = 0.1 | 1.2226 … 5.3362 | 1.204 … 5.242 (Sutcliffe 2007) | CALIBRATED at the same grid spacing (+1.25% to +1.80%) |
| E8 | energy ratios E_Q/E₁ and configuration types | ratios within 0.3%; all seven types match | Sutcliffe 2007 | CALIBRATED |
| E8 | Q = 1, continuum and infinite volume | 1.2248 ± 0.0003; independent spectral code 1.22493 | "around 1.21" (Sutcliffe) | above the quoted range: Sutcliffe's table is 1.7–2.2% below the continuum (two independent codes agree) |
| E0, E3, E4 | group theory | exact | LNR, Mayanskiy, ATLAS | CALIBRATED |

## What missed, and what changed on the way

The method only works if misses are kept. These are the ones that matter:

1. **E6, my preregistered prediction was wrong.** I predicted the fold's gravitational binding would equal the Newtonian −½∫ρΦ to 1%. It is 1.29 times that, because the fold's internal stresses gravitate too; the full result, −G∫(ρ + p_r) m/r dV, was derived and reproduced in two gauges. It stays a MISS of the prediction, with the physics explained.
2. **E1, the DSV example point.** The first report called (ω, v) = (0.99, 0.43) reproduced from one run. The cross-check could not reproduce it, and the reconciliation showed why: the point is chaotic. A long-lived central oscillation decides whether to release a pair at t ≈ 850, after even the two finest discretisations have separated, and none of 11 neighbouring initial conditions produces. It is now OPEN; a converged producer sits nearby at (0.99, 0.41).
3. **E1, speed and energy.** The first report said slower packets produce more at matched energy. That was an amplitude effect: at equal energy, slow packets are taller. A 3,402-run test at fixed packet shape, with the decision rule fixed beforehand, finds no slow preference (faster packets produce as much or more), so the preregistered "favours low speed" is REFUTED. The first report also said 2M was not the onset of production; that holds only for the families scanned, since time-reversed captures reach 2M exactly.
4. **E4, "no class fits and predicts"** held only for complex couplings, a choice the first report did not state. With real couplings three classes survive, with one weak prediction (δ_CP on 16–22 discrete branches).
5. **E7, two numbers were misread.** The Demidov–Levkov exponent is 3.846, not 3.93 (re-read from the vector paths of the published figures), and a spline artifact inflated a hopfion radius (2.061, not 2.144). No conclusion changed.
6. **E8, the absolute knot energies** match Sutcliffe at his grid spacing, but two independent codes put the continuum about 2% above his table.
7. **Vocabulary and provenance.** Several reports first labelled seed predictions or internal checks as CALIBRATED; the reconciliations relabelled them. One target ("36.5 F_π/e = 1.2315 × 3π²", PLAN E2) mixed three slightly different literature values; all three are matched.

## Corrections to SEED.md

From the literature check (PLAN §3) and the experiments, for the next revision:

- **§2, pairs:** twice the fold energy is the exact floor, but reaching it takes finely tuned initial data; in ordinary packet collisions production starts at about 1.9 × 2M or higher.
- **§2, knots:** Hopf folds can be fermions only for odd Hopf charge (Krusch & Speight 2006).
- **§2, G₂:** the bosons-only result also follows from representation theory alone (E3), and the no-WZ argument needs H⁵(G₂; ℝ) = 0.
- **§3, last paragraph:** the groups do stack: G₂ ⊃ SU(3)⋊ℤ₂ ⊃ PGL(2,7) ⊃ PSL(2,7) ⊃ F₂₁; the family split survives up to PSL(2,7), and the family-swapping turns enter with PGL(2,7).
- **§4, packets:** a packet folds when its amplitude is large enough (A ≳ 0.4 in the units of E1), not when its energy is; a single tall packet folds on its own. DSV's trains make pairs in a velocity band that moves to lower speed as the pulses weaken, not "most easily at low speed".
- **§4, the 3/4 power:** optimality is Lin & Yang (2004); Sutcliffe 2007 is the numerical agreement.
- **§5:** Weinberg 1965 (Phys. Rev. 138, B988) for Einstein's equations; "energy bends the cone" → "stress-energy bends the cone".
- **§6B:** "within roughly 30%" → "most static properties within about 33%; g_A about 50% low; charge radii need a pion mass".
- **§7.3:** the order-21 group restricts couplings but gives no masses without breaking, and no residual-symmetry pattern of it fits the measured mixing.
- **§8:** the electron misses by ≥ 3.5 × 10⁶ (LEP); easy electron-pair production reflects weak, perturbative QED, not a strongly coupled fold sector; Weinberg–Witten excludes a composite graviton under commitment 1.
- **§9:** Albayrak & Vachaspati, Phys. Rev. D 109, 036001 is 2024; DESI DR2 II is Phys. Rev. D 112, 083515 (2025); Vakulenko & Kapitanskii's original is Dokl. Akad. Nauk SSSR 246, 840.

## Where to push next

Ranked by how much each would tell:

1. **The electron.** Nothing classical in the seed can make it (E7). The question is whether any quantum, strongly coupled fold sector yields a light, pointlike fermion, or whether fermions must enter as fundamental fields with folds as composites. This is the deciding problem.
2. **A falsifiable prediction from the 60° structure.** The three PSL(2,7) mixing patterns that fit current neutrino data tie δ_CP to the measured angles (best fits 235°–284°, E4). A dynamical reason for the vacuum alignment, plus DUNE and Hyper-Kamiokande's δ_CP, would test them. F₂₁ alone cannot do this.
3. **Quantise the knots.** Finkelstein–Rubinstein quantisation of Hopf folds (fermions at odd Q) and their excitation spectrum.
4. **The G₂ fold's global minimum.** Only local stability of the embedded fold was shown (E3); a full 3D minimisation in G₂ would settle it.
5. **Pair production in three dimensions.** E1's ragged boundary is one-dimensional; vortex and skyrmion production from colliding packets would show whether it persists.
6. **The vacuum energy.** No experiment in this series can touch it; it needs a mechanism, not a simulation.

## How this was done

- **Preregistration.** `PLAN.md` fixed the experiments, targets and pass rules before any computation (commit `0dcd3fe`). Deviations are listed in each report.
- **Literature.** Publisher sites were blocked by the sandbox's proxy. Targets were read from the public arXiv mirror on Google Cloud Storage and the PDG 2026 database, or, where marked [summary], from search extracts. `prior_address/` holds the raw literature check.
- **Two computations each.** A run agent implemented each experiment; an independent agent recomputed every headline number with different methods (different solvers, discretisations, representations, exact versus floating arithmetic) before reading the original code; a third reconciled any disagreement. All three outputs are kept.
- **Interruptions.** Two container restarts and three account usage-limit stops interrupted the run. Work resumed from checkpoints on disk; every report says what was resumed.
- **Compute.** Four shared cores. The knot relaxations (E8) took about 5 CPU-hours at Sutcliffe's grid (151³); everything else ran in minutes to an hour.

## Files

| Path | Contents |
|---|---|
| `SEED.md`, `hexagon_check.py` | the seed and its own §3 check |
| `PLAN.md` | the preregistration |
| `prior_address/` | the literature check, raw |
| `experiments/E0_hexagon_exact/` … `E8_hopfions/` | code, `results.json`, `REPORT.md`, figures, `crosscheck/`, `RECONCILE.md` |
| `RESULTS.md` | this summary |
