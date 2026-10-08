# C2 — The annotation batch: every item verified before folding

**Plain-language summary.** Every C2 item in the brief was checked before anything was folded. All of them hold, three of them after a correction to how the lead was worded.
- **ζ-tax gate 3 closes as failed.** The banked picture makes redshift a small loss of amplitude at each lattice corner. That is "tired light": it reddens light without stretching time. Supernova light curves are stretched by exactly the amount ordinary expansion predicts (DES: b = 1.003 ± 0.011, where tired light gives 0).
- **The electron's 2π closure is conditional.** It needs a vacuum in which a 2π phase winding cannot unwind. The vacuum of record has no such protection (π₁ = 0). A protected 2π winding exists only on vacua where the real-unit component ψ₀ carries weight, and choosing such a vacuum is an import (I6) that has been registered but not made. OP-2.14's closure and two G-QUANTA PASS verdicts rest on it, so they become conditional too.
- **"The factor of 4 is the spin-3/2 quartet" is downgraded.** In the quark model, the 4 in μ_p = (4μ_u − μ_d)/3 is a spin-½ weight (4/3). The spin-3/2 states are the Δ resonances, and the Δ⁰ has μ = 0, not the neutron's moment. Eighteen entries in the Gate 2a thread carry the old reading, and each gets a pointer.
- **The polycrystal window is only 5 to 20 lattice cells wide.** A floor requiring grains much larger than a cell would shrink it, and a 20-cell floor empties it. The ledger does not license ξ = ℓ_P on the transverse line: one gate elected it, and that gate's reading is conditional on the election.
- **§2.52 Open 3 gets the G-ζ1 result. The freeze stays.**
- **Fourteen math items are confirmed**, thirteen by exact computation and one (the de Marrais attribution) by reading the ledger. Three leads needed correcting first:
  - Moreno settles OP-2.81.2 but only part of OP-2.81.1.
  - The §2.84A coincidence works through a different map in that entry's own labels.
  - The OP-2.74.1c.i sign is +, not −.

No second leg disagreed. The fold (V4.94) adds 79 C2 brackets alongside C1's 34.

**Pre-registration:** `C2_PREREG.md` (md5 `e538b2e5…`, locked at `d6fee69` before any check). Every decision rule below is quoted from it.

## Legs

| Item | What decides it | Leg 1 | Leg 2 | Agreement |
|---|---|---|---|---|
| P1 | quotations (ledger, DES) | first reading (previous session) | `c2_quotes_check.py` re-reads the ledger verbatim; DES read from a second copy (ORNL portal) | yes |
| P3 | quotations (G-VS1, §2.92.B) | first reading (previous session) | `c2_quotes_check.py` | yes |
| P4 | quark-model moments, exact | `math_B/m_magnetic_moments.py` (states solved from constraints) | `c2_checks.py` (states built from Clebsch–Gordan weights) | yes |
| M-rev (a) §2.68.8.1 | an e₈-cancelling zero product | `math_A/item_a_moreno.py` | `c2_checks.py` (and `math_A/second_leg_checks.py`) | yes |
| M-rev (b) signed lifts | 8 sign vectors per collineation; annihilation graph | `math_A/item_b_signed_lifts.py` | `c2_checks_b.py` (and `math_A/second_leg_checks.py`) | yes |
| M-rev (c) §2.77 | conjugacy of u and u³; the generated algebra | `math_B/c_sl27.py` | `c2_checks.py`, `c2_checks_b.py` (Burnside), `math_B/c_sl27_crosscheck.py` | yes |
| M-rev (d) matchings | count of size-2 matchings | `math_A/item_d_matchings.py` | `c2_checks.py` (and `math_A/second_leg_checks.py`) | yes |
| M-rev (h) stabilizer | the flag stabilizer's isomorphism type | `math_A/item_h_stabilizer.py` | `c2_checks.py` (and `math_A/second_leg_checks.py`) | yes |
| P2, P5, other M items | arithmetic, quotations, literature | one leg | — | — |

The two math subagents worked blind to each other and to this session's checks. Their reports are saved verbatim as `math_A/REPORT.md` and `math_B/REPORT.md`, because the harness blocks subagents from writing report files.

## P1. ζ-tax gate 3 — **CLOSED: FAILED as framed**

**Rule.** "CLOSED: FAILED if the banked entry makes the redshift a per-vertex amplitude penalty on the photon (Φ_out = Φ_in(1 − ζ)) with no change to emission and arrival intervals … If the entry admits a time-dilating reading, the verdict is not FAILED."

**The entry.** The banked row (V4.93 L4364) reads "Hypothesizes ζ = 1 − π/√12 is a discrete per-vertex amplitude penalty Φ_out = Φ_in(1−ζ) at every p6m corner, from which four objects are claimed to emerge: cosmological redshift …". The store file says the photon "pays the ζ-tax sequentially", giving "an exponential geometric attenuation mimicking Hubble's law". G-FOLD1's welding lemma (L4378, R1) puts every frame or metric redshift in the time-dilating class. It puts an amplitude penalty that preserves intervals in the tired-light class, which predicts no light-curve stretch. The same row says the lemma's bearing on the ζ-tax element was "flagged, not adjudicated".

**The data.** White et al. (DES), MNRAS 533, 3365 (2024), arXiv:2406.05050: "b = 1.003 ± 0.005 (stat) ± 0.010 (sys)", "ruling out any non-time-dilating cosmological models at very high significance." The combined uncertainty is 0.011, which puts the measurement about 90σ from b = 0.

**Does the entry admit a time-dilating reading?** The store file's Flag 1 leaves open whether the ζ-tax replaces metric expansion or adds to it.
- Either way, the ζ-tax part is an amplitude penalty with unchanged intervals, so the mechanism itself never dilates time.
- In the "adds to expansion" reading, the penalty supplies a share f of ln(1+z), and the light-curve stretch is (1+z)^(1−f). DES then gives f = 1 − b = −0.003 ± 0.011, consistent with zero. So the penalty cannot be the cosmological redshift.

**Verdict:** FAILED as framed. A frame or metric recast would dilate time by construction, but it abandons the amplitude mechanism. That would be a new entry, not this gate.

**Brackets (V4.93 lines):** 4599 (gate 3 row: the closure), 4364 (the banked row), 4378 (G-FOLD1's "flagged, not adjudicated").

## P2. Polycrystal — validity floor and the ξ = ℓ_P license (annotation, no verdict)

**Cells per grain** (`c2_checks.py`). W^EM_∪ of record is (0, 3.7641664288×10⁻³³ m] (§2.91.N). The declared chain (ξ = ℓ_P, C = ξ/a ∈ [0.0213, 0.0851]) gives a_phys ∈ [1.899, 7.588]×10⁻³⁴ m. So the window edge is **4.96–19.82 cells**.

**Effect of a floor.** A floor of N cells leaves (N·a_phys, 3.764×10⁻³³ m]:
- at N = 10, a window remains only for a_phys ≤ 3.76×10⁻³⁴ m;
- at N = 20, no window remains anywhere in the band (20 × 1.899×10⁻³⁴ = 3.80×10⁻³³ > 3.764×10⁻³³).

The value of N is the author's to elect, so a Part VI row is registered for it.

**What licenses ξ = ℓ_P on the transverse line (from the ledger's own record).**
- G-SCALE1 (§2.91.H, V4.67) declared ξ := ℓ_P as a "scale placement ONLY" for the longitudinal KC3 comparison. That comparison retired the longitudinal bridge.
- ANNEX-CDEF-1 (V4.71, L293) then records the transverse scale import as "named and unexercised (… ξ = ℓ_P not licensed …; the G-SCALE1 corollary stays channel-specific to the longitudinal KC3 constraint)".
- The only later transverse use is G-S2C1-W (V4.81), through its own lock-record election "E-W-1 (a) declared chain ξ = ℓ_P + G-C1 C-interval". That gate's row reads "R2 reading conditional on E-W-1..3".

**Resolution.** ξ = ℓ_P is not licensed on the transverse line. It is used there once, as a gate election, and the a_phys band and lattice floor inherit that conditionality.

**Brackets:** 1658 (§2.91.N: the floor), 4420 (G-CI1 row), 1632 (§2.91.H: scope of the declaration), 293 (ANNEX-CDEF-1: "not licensed" stands), 4424 (G-S2C1-W row: E-W-1 is an election).

**Noted, not bracketed.** G-MSCS-A (§2.91.T, Part VI row L4429) reads its regime "at the W^EM_∪ edge (vacuous)". It would be affected if a floor were adopted. A floor is an election, not a verdict, so no dependents are bracketed.

## P3. §2.50.A, OP-2.14, G-QUANTA — **CONDITIONAL**

**Rule.** If π₁ = 0 at the vacuum of record, the elementary winding is π on the polar strata, and it is 2π only where ψ₀ carries weight, annotate CONDITIONAL. That covers §2.50.A's 2π trap, OP-2.14's closure, and G-QUANTA's electron-2π and K₇-vortex PASS rows: each holds only on a ψ₀-weighted vacuum (import I6, not forced).

**The facts (second reading, verbatim, `c2_quotes_check.py`).**
- **π₁.** G-VS1 (§2.91.U, L1672): "π₁(V) = ℤ on every stratum except F7 (ψ₀ = 0, S = 0: P = U(1), π₁ = 0) and the accidental point P0 (the O(16) sphere of record, HYP-A1-5)".
- **Elementary winding.** Same entry: "elementary winding π on the polar strata P7, I7 (half-quantum vortices), 2π wherever e₀ carries weight".
- **Protection.** Same entry: "protection is a selection — by the import I6 (registered, not made) or by the dynamical clause (M.CW)".
- **§2.92.B (L1682).** "the half-quantum protection on P7 and I7 is accidental; robust protection is ψ₀ windings only".
- **Not yet re-read.** G-VS1 itself recorded "§2.50.A's closure not re-read (the half-quantum fact registered only)".

All three conditions hold. **Verdict:** CONDITIONAL. No number changes, because m₀ is fitted from m_e. What changes is the claim that the 2π, and with it the exponent 2π/Φ, is forced.

**Blast radius** (every entry leaning on the 2π closure as protected):

| Line | Entry |
|---|---|
| 1379 | §2.50.A statement |
| 1373 | §2.50 result ("minimum stable") |
| 424 | §2.14 result |
| 4610 | OP-2.14, closed list |
| 1662 | §2.91.P G-QUANTA |
| 4425 | G-QUANTA row |
| 4382 | stability / composite-quanta memo row |
| 1672 | G-VS1's "not re-read" |
| 279 | M.REL worked example (π₁(S¹) = ℤ as import-free) |
| 283 | M.REL rationale citing §2.50.A as a clean Step 2 |
| 4376 | the electron Cl(2) R3 row, which restates §2.50.A |
| 4255 | §4.10's "Electron at the tip (2π first stable closure)" |

Checked and not bracketed:
- §2.1, the mass table: its numbers are fits and do not change.
- §2.64.x (L3866 ff.): it uses the definitional anchor, not the trap.

## P4. μ_n — **DOWNGRADED: "factor of 4 = the spin-3/2 quartet"**

**Rule.** Downgrade if both hold: (i) μ_p = (4μ_u − μ_d)/3 comes from the spin-½ coupling weights, ⟨σ_z(u₁) + σ_z(u₂)⟩ = 4/3; (ii) μ(Δ⁰) = μ_u + 2μ_d = 0 at μ_u = −2μ_d.

**Two legs, exact (sympy).**

| Quantity | math_B (states solved from symmetry, spin and charge constraints) | this session (states built from Clebsch–Gordan weights, then symmetrized) |
|---|---|---|
| μ_p | (4μ_u − μ_d)/3 | −μ_d/3 + 4μ_u/3 |
| μ_n | (4μ_d − μ_u)/3 | 4μ_d/3 − μ_u/3 |
| ⟨σ_z(u₁) + σ_z(u₂)⟩_p, ⟨σ_z(d)⟩_p | 4/3, −1/3 | 4/3, −1/3 |
| μ(Δ⁺⁺, Δ⁺, Δ⁰, Δ⁻) | 3μ_u, 2μ_u + μ_d, μ_u + 2μ_d, 3μ_d | same |
| μ(Δ⁰) at μ_u = −2μ_d | 0 | 0 |
| μ_p/μ_n at μ_u = −2μ_d | −3/2 | −3/2 |

Both conditions hold. **Verdict:** DOWNGRADED. The −3/2 ratio is a spin-½ result, so a quartet programme targets the Δ. Supplying −1 ↦ −Id to make the 4-dimensional channel spin-3/2 would give Δ-type moments, not μ_n's. The representation theory stays R1 throughout: σ₄|₂O = spin-3/2, the 2O irreps, Cℓ(6) = Spin(6) = SU(4), and the assignment theorems.

**Blast radius (18):**
- §2.85: Part B 1045, Part D 1053, Part E 1057.
- §2.87: 1067 (the reduction), 1080 (the unification sentence), 1084 (net for μ_n).
- §2.87.A: 1096, 1100, 1118.
- §2.87.B: 1134. §2.87.C: 1154. §2.91.R: 1666.
- Part VI: 4438, 4563 (the μ_n gate), 4565, 4574, 4578, 4579.

Mentions of μ_n that only say "no μ_n" are not dependents.

## P5. §2.52 Open 3 — the G-ζ1 result added; freeze kept

G-ζ1 (§2.88.D.1, V4.36) returned DEGENERATE as primary: the registered density channel is gapless and transparent (t → 1, 10.7× ζ). The alternative reading was INFORMATIVE-FAIL: no probe entered the PASS window [0.0881, 0.0981], and the closest, t = 0.36 ± 0.02, sat 3.87× above ζ. H′ was retired (§3.A.9).

One bracket goes on the row (L4393). The row stays Open and frozen, as the brief says: "Add the G-ζ1 result, and leave the freeze in place." This is the first fold authorized to touch the row, and it touches it only by appending.

## Math items

| Item | Lead | Check | Verdict | Brackets (V4.93 lines) |
|---|---|---|---|---|
| (a) OP-2.81.2 | closes by Moreno's criterion | Moreno, arXiv:q-alg/9710013: x = (a, b) is a zero divisor iff Re a = Re b = 0, \|a\| = \|b\| ≠ 0 and a ⊥ b. So a clean zero divisor has no e₈ and equal term counts in each copy, making n even. Census of all 7,174,453 clean elements (math_A); n = 2, 4, 6 reproduced (this session). | **CLOSED** | 2772, 4469 |
| (a) OP-2.81.1 | closes by Moreno | Moreno gives the count (1764 = 21 × 84) and the rank (12), not the kernel split. Computed split: 84 / 336 / 1344, the last a class the ledger never mentions. | **partly answered** (lead corrected) | 2771, 4468 |
| (a) §2.68.8.1 | the argument is flawed; OP-2.67.1b(ii)'s "CLOSED" rests on it | e_a·e_{a+8} is never a term of x·y. (e₁+e₂+e₁₁+e₁₂)(e₃−e₄+e₁₃−e₁₄) = 0 has two cancelling e₈ terms (two legs). ⟨e₀, e₈⟩ is not the only ZD-free plane. The exclusion itself stands on §2.68.7 and Moreno. | **argument invalid; fact stands** | 2149, 2194, 4478, 496 |
| (b) signed lifts | all 168 lift with signs | 8 sign vectors for every collineation (1344); 21 unsigned. Unsigned, the other 147 reverse exactly 4 of 7 line orientations. All 2688 signed Cayley–Dickson lifts preserve the annihilation graph; 21 unsigned do (two legs). The 1344-group is the non-split 2³·PSL(2,7) (math_A). | **confirmed** | 2353, 3215, 3219, 1760, 4587 |
| (c) §2.77 | χ is outer; the order-4 images span M₄(ℂ); no order-24 element | No g ∈ SL(2,7) conjugates u to u³ (0 of 336), and s = diag(3,5) = −t gives s u s⁻¹ = u². χ is induced by conjugation by diag(3,1) ∈ GL(2,7), which carries σ₄ to σ₄′. The 42 order-4 elements generate SL(2,7), so their images generate M₄(ℂ) (Burnside). Their linear span is the 15-dimensional traceless space (math_B, exact and mod 11). Element orders are 1, 2, 3, 4, 6, 7, 8, 14. | **confirmed** (span vs algebra stated precisely) | 2461, 2371, 2494, 4543, 2853, 2857, 2869, 2531 |
| (d) matchings | K₇,₇ − M has 651 size-2 matchings | 861 − 210 = 651 (three computations). The 42 quadruples are the matchings whose four labels form a Fano-line complement and whose all-plus diagonals annihilate. The other 42 such matchings are exactly 𝒴. | **confirmed** | 2003, 2060, 2068, 496 |
| (e) K₈ | six 1-factorizations | 6240 labelled factorizations in six classes, \|Aut\| = 1344, 96, 64, 42, 24, 16 | **confirmed** | 1782 |
| (f) | arctan(1/√2) = 35.26° | 35.2644°; 54.7356° is its complement | **confirmed** | 1950 |
| (g) | log(4π)/log 7 = 1.3007 | 1.300689 | **confirmed** | 1792 |
| (h) §2.62.C | the stabilizer is D₄ | flag stabilizer of order 8, non-abelian, five involutions (three computations). Unsigned, V₄ fixes a code space whose orbit has 42 members. §2.62.B's "Sign Duality" is false: the negated orientation gives 21 different spaces. | **confirmed** | 3412, 3402, 484, 1740 |
| (i) §2.84A | a labeling coincidence via 7⊕a ≡ −a | In §2.84A's cyclic labels, L_{e₇} acts as a ↦ 3a on QR. The 7⊕a ≡ −a map holds in Cayley–Dickson labels. 12 of 30 labelled planes give the swap, and J has 8 transversal splits. | **coincidence confirmed; mechanism corrected** | 3189 |
| (j) OP-2.74.1c.i/iii | TS_O1 = {e_a·e_b = −e_{a⊕b}} | The sign is reversed: TS_O1 = {+}, TS_O2 = {−} on all 42 (a ≤ 7 < b), and it is F₂₁-invariant. For .iii, the asymmetry is a sign-convention artifact. | **answered (sign corrected)** | 2440, 2442, 4531, 4533 |
| (k) de Marrais | unattributed in §2.55, §2.68.4, §2.41.B | Keyword scan: no attribution in those sections; the structures are the box-kites (math_A, k). The ledger attributes de Marrais 2000 at §2.78. | **confirmed** | 1972, 2036, 1760 |
| (l) α⁻¹ | 136.48 below 137.036; one match from two starting values | 84/arctan(1/√2) = 136.4789 (−0.407%). 240/√3 = 138.5641 (+1.115% of CODATA 2022, not 1.099%). §2.2 and §2.25.3–6 credit one 0.003% match to the two values, with different named corrections. | **confirmed** | 408, 1353 |

Lines 1760 and 496 each carry one combined bracket: (b) with (k), and (a) with (d). Line 1782 carries the K₈ correction plus a pointer to (h).

## Found, not annotated

These are outside the brief's C2 list, recorded for the author.
- **L2427.** "a + b = 15 picks out twosets of signed-skew χ = −1 (QNR) exclusively" is false for the sum-15 set: (3,12), (5,10) and (6,9) have χ = +1 (math_A, j).
- **§2.53's imaginaries column.** The findings say it should read 3, 7, 15. Not in the brief's list.
- **Other findings in the Part II §M–O review.** G-C1 against §2.64.A; the verify-then-widen couplings; C.COSM.4's Plateau argument; the §2.69 canary; the §4.7 blocker; the cosmogony entries. None is in Phase C's brief.

## Files

| File | md5 |
|---|---|
| `C2_PREREG.md` | `e538b2e57bbcd3a52d17df7181b21923` |
| `c2_checks.py` / `_output.txt` / `.json` | `c90a6790…` / `ab3bc77a…` / `589ef266…` |
| `c2_checks_b.py` / `_output.txt` / `.json` | `ab0ac39d…` / `89069a6a…` / `ab5221d1…` |
| `c2_quotes_check.py` / `_output.txt` / `.json` | `ff6afd09…` / `b17f1e29…` / `a2bae771…` |
| `math_A/REPORT.md` (verbatim) + 29 scripts and outputs | `dacffce1…`; per-file md5s in the report |
| `math_B/REPORT.md` (verbatim) + 12 scripts and outputs | `f691a026…`; per-file md5s in the report |
