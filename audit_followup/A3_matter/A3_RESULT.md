# A3 — The matter sector: result

**Plain-language summary.**
- **The units match, so the proton check fails.**
  - Paper VII measures rope length per unit of tube radius. That is the same convention behind the published 58.006 for the tightest known Borromean rings.
  - Rebuilding the ledger's own four-arc Borromean rings gives 58.053 in those units.
  - So the tightest Borromean rings need at most 58.006, while the prediction's window was 59.894–60.494.
- **By the ledger's own rule, the proton entry (§2.15) goes back to Conjecture status.**
  - Paper VII's own outcome table calls this result "prediction falsified at leading order".
  - The rule's second clause ("the Borromean assignment is falsified") is not triggered as written. It was built on reading 58.006 as a lower bound, and it is an upper bound.
- **At the real length, the formula gives a 759 MeV proton, 19% light.**
- **Only one of the three proton lengths on record is a length.** About 58.05 is the length of a real configuration. The other two, 60.194 and 80.95, are the proton mass run backwards through the mass formula, using A/Z_f = 20/6 and 1/2.
- **The ledger's A = 20 uses a non-standard reduction of the Alexander polynomial.** The standard one-variable polynomial gives 70.
- **Nothing protects "Borromean linking = baryon number".**
  - The vacuum inventory has no non-commuting vortex charges.
  - The ledger computes no barrier.
  - Simulated vortex links come apart.
  - A protected Borromean baryon would need a suppression of about e⁻¹⁵⁰ to e⁻²⁰⁰.
- **The mass table is a fit with no spare degrees of freedom.** It has 8 rows and at least 9 selected inputs.
- **Against PDG 2024, four rows now miss by more than 2%:** down (−2.4%) and charm (−2.1%), joining W (+2.2%) and Z (+3.0%). The up quark also falls outside its band.

**Pre-registration.** `A3_PREREG.md` md5 `e2f1090cac3b097c0d2d205146c8b67c`, locked by commit 53667db before any A3 computation file existed.

**Two legs.**
- *First leg:* `a3_matter.py` (md5 `4f42a3a93fdabdfd33e7004be6a8534d`) produces `a3_output.txt` (`528dec212357ab6664f48fe59ecfe205`) and `a3_results.json` (`23d7d672a94a9b6420fd2aafea1b90ba`).
- *Second leg, blind:* `leg2/` (see `leg2/MANIFEST.md5`).
- *Comparison:* `a3_compare.py` (`4475387e339c320d624f26fbc8290c05`) produces `a3_compare_output.txt` (`6c7c8ff9541c3b83517cf7bc7e84394c`). **46/46 PASS.** Numbers agree to ≤ 10⁻¹³ relative, and every classification and verdict is identical.

## DR-A3-1. Units: UNITS MATCH

- **The four-arc configuration** (§2.82's description, tube radius 1, arcs of radius 2):
  - Each component has two convex lobes (sweep π + 2β) about the minor-diagonal vertices (0, ±(√7−1)) and two concave waists (sweep 2β) about the major-diagonal vertices (±(√7+1), 0), with β = arctan √7 − π/4.
  - Each arc is centred on a point of another component, at contact distance 2.
  - Component length 16 arctan √7. **Total 48 arctan √7 = 12π + 24 arcsin(3/4) = 58.052601738633** per tube radius (29.026 per diameter).
  - That is 0.0045% from CKS02's "about 58.05" and 0.080% above 58.006.
- **Embedding.**
  - Curvature radius is 2 everywhere.
  - The minimum distance between components is 2.000000000000, and every point is in contact with some other component.
  - The single-component self-distance is 2(√7−1) = 3.2915. So the link's thickness is exactly 1.
- **Topology.**
  - The pairwise linking numbers are all 0.
  - The piercing pattern is cyclic: each component's disc is pierced twice, in opposite directions, by one neighbour and missed by the other.
  - The second leg also computed the multivariable Alexander polynomial from two projections of the actual 3D curves and got (t₁−1)(t₂−1)(t₃−1), the Borromean value. Its two-component sublinks give 0.
- **Convention of record.** Paper VII E.1.1 defines ℒ = L/R, arc length per tube radius. So L_B is quoted in the same units as 58.006 and 58.05.
  - The project-store draft `sqt_baryon_section_draft.md` §4 instead says "arc-length-to-tube-diameter ratio". In diameter units the comparison values halve, to 29.003 and 29.026.
  - The verdict below holds in either convention.

## DR-A3-2. Verification (1): FAILS, and §2.15 RETRACTS to Conjecture

- **Clause 1.** U = min(58.006, 58.0526) = 58.006, which is below 59.894. Verification (1) **FAILS** in the convention of record, and a fortiori in diameters (U/2 = 29.003). By §2.15 L658, clause 1: **the entry retracts to Conjecture status.**
- **Clause 2** (the Borromean assignment falsified if the minimized value lies outside [58.006, 62.0]):
  - **Not triggered as written.** No Borromean configuration shorter than 58.006 is on record or computed here.
  - **Correction to the clause's premise.** 58.006 is the length of the best-known configuration, which CFKSW "believe is the minimizer". It is an upper bound on the minimum, not "a rigorous lower bound" (the wording of the source script `sqt_open_problem_5.py`). The clause can therefore fire only if someone finds a shorter configuration.
- **Paper VII's own outcome table** (E.1.3) reads: "Minimized L_B ∈ [58.006, 59.894) … Prediction falsified at leading order — framework requires revision". The best value on record, 58.006, falls in that row.
- **The mass at the geometric length** (A = 20, Z_f = 6):
  - m(58.006) = **758.69 MeV (−19.1%)**;
  - m(58.0526) = 762.15 MeV (−18.8%).

## DR-A3-3. Which proton length stands: 58.006 (58.05 for the four-arc version)

| Value | Class | Provenance |
|---|---|---|
| 60.194 | **(I)** | m_p inverted with A/Z_f = 20/6. The exact inversion is 60.19346; with m₀ rounded to 0.18699 (as in the source script) it is 60.19356, which prints as 60.194 |
| ≈ 58.05 | **(G)** | The four-arc configuration, 48 arctan √7 = 58.0526 |
| 80.95 | **(I)** | m_p inverted with A/Z_f = 1/2. The exact value needed is 0.49988; inverting with 1/2 gives 80.9473, −3.3×10⁻⁵ from 80.95. The V4.40 record attributes it to "the existing HANDOFF_MASS_CALC_v3 formula" |

- **The proton length of record is 58.006**, CFKSW's B₀ and the presumed minimum. The four-arc 58.0526 is its 0.08%-longer piecewise-circular approximation.
- **60.194 and 80.95 are retired as lengths.**
  - Both exceed U, so neither can be the ideal length, whatever its provenance.
  - V4.40's "L_p = ξ_vac/2 to 0.06%" and its "clean correction r_eff = 1 + ln(3/2)" are properties of an inversion, not of the proton's geometry.

## DR-A3-4. 60.194 is m_p inverted

The inversion lands within ±0.001 of 60.194, so the annotation applies:
- §2.15's proton "0.000% (by construction)" is a calibration.
- The neutron's −0.138% is m_n − m_p restated.
- "The first prescription … with both m_p and m_n within 0.15% … without per-baryon fitting" is not a prediction, because the per-baryon fit is the inversion for L.

## DR-A3-5. A = 20 versus 70: annotate

Both legs used Fox calculus, on different presentations:
- the first leg, the 3-generator closed-braid presentation of (σ₁σ₂⁻¹)³;
- the second leg, a 6-arc Wirtinger presentation.

They agree:
- Δ(t₁, t₂, t₃) = (t₁−1)(t₂−1)(t₃−1).
- Δ(t, t, t) = (t−1)³. Its coefficients are 1, −3, 3, −1, with **sum of squares 20**.
- The one-variable Alexander polynomial of the link is Δ_L(t) ≐ (t−1)Δ(t, t, t) = (t−1)⁴ (Torres). Its coefficients are 1, −4, 6, −4, 1, with **sum of squares 70**.
  - The first leg confirms it by reduced Burau; the second leg confirms it by Conway z⁴ and by Burau.

§2.15's A = 20 is therefore the diagonal specialisation of the multivariable polynomial. The source script calls it the "single-variable Alexander polynomial", which it is not. The knot rows have only one variable, so they cannot settle which convention applies to a link.
- With A = 70, the inversion gives L = 47.69.
- With A = 70 at L = 58.006, the formula gives m = 2655 MeV.

## DR-A3-6. Reconnection: UNPROTECTED

**(a) No non-Abelian π₁ on the vacuum inventory.** A2's recount under G₂ × U(1)_ψ₀ × ℤ₃ gives:
- π₁ = ℤ (ψ₀ windings) on R, MP, MF and MI;
- ℤ ⊕ ℤ on the mixed strata at degree ≤ 4, reducing to ℤ with Re S³;
- 0 on F7, and on P7 once Re S³ is present.

Every one of these groups is Abelian. The Poénaru–Toulouse commutator obstruction to two lines crossing is therefore trivial everywhere on the record. The only non-Abelian mention in the ledger is §2.70's candidate (b), "homomorphisms to non-abelian targets such as PSL(2,7)". That concerns strand labels, not a vortex π₁.

**(b) No barrier on record.** In V4.91, "reconnect", "untie", "Kleckner", "strand crossing", "proton decay" and "proton lifetime" each have 0 hits. "Proton stability" appears 3 times, all in the σ₄-unification context.

**(c) Literature.**
- Kleckner, Kauffman & Irvine (2016): 322 Gross–Pitaevskii knots and links "universally untie".
- Guan, Zuccher & Liu (2025): Borromean vortex rings reconnect into unlinked loops.
- Ruban (2018): quasi-stable windows extend lifetimes to "many dozens and even hundreds of typical times", not to 10⁶⁶–10⁸⁵.
- Annala et al. (2022): even non-Abelian protection can be undone by vortex splitting.
- G-κ1 places the ledger's strands 2–4ξ apart. That is within a few core sizes, the scale at which Gross–Pitaevskii lines approach and reconnect.

**Verdict.** "Borromean linking = baryon number" is **UNPROTECTED** on the vacuum of record.

**Required suppression**, with τ_p > 2.4 × 10³⁴ yr (Super-K) and exp(−S) < 1/(ν τ_p):
- **S ≳ 152** at the hadronic rate m_p c²/ħ = 1.43 × 10²⁴ s⁻¹;
- **S ≳ 197** at the core rate c/ξ_phys = 5.2 × 10⁴³ s⁻¹, using V4.40's ξ_phys = 0.358 l_P.

These are orders of magnitude only.

**Successor, registered.** Either:
- (i) a non-Abelian core sector not now on the record, followed by the PSL(2,7)-colouring and Annala-invariant computation from the Phase 2 report's Q1; or
- (ii) an energetic barrier, for example from a bound core filling. That filling is VC-B, which is itself conditional on the immiscibility import. The barrier would need a computed tunnelling action of S ≳ 150–200.

## DR-A3-7. The mass table: a fit with dof ≤ −1, and the 2% headline does not hold

**Reproduction.** All eight printed predictions reproduce from the calculator inputs to ≤ 7 × 10⁻⁵ relative.

**Against PDG 2024:**

| Row | Predicted (MeV) | PDG 2024 | Error | Pull (experimental σ only) | Rule |
|---|---|---|---|---|---|
| u | 2.0391 | 2.16 ± 0.07 | −5.60% | −1.7 | **NOT HOLDING** (outside the ±1σ interval [2.09, 2.23]; the "1.90–2.65 band" is PDG 2022's) |
| d | 4.5890 | 4.70 ± 0.07 | **−2.36%** | −1.6 | **NOT HOLDING** |
| c | 1245.67 | 1273.0 ± 4.6 | **−2.15%** | −5.9 | **NOT HOLDING** |
| b | 4162.59 | 4183 ± 7 | −0.49% | −2.9 | within 2% |
| t | 171,184.7 | 172,570 ± 290 | −0.80% | −4.8 | within 2% |
| τ | 1752.43 | 1776.93 ± 0.09 | −1.38% | −272 | within 2% |
| W | 82,127.5 | 80,369.2 ± 13.3 | **+2.19%** | +132 | reported |
| Z | 93,964.0 | 91,188.0 ± 2.0 | **+3.04%** | +1388 | reported |

**The headline.** "Within 2% … for 6 fundamental fermions (plus the up quark within the PDG band)" does not hold. Under PDG 2024 only b, t and τ are within 2%. Four rows (d, c, W, Z) exceed 2%, and u is outside its band.

**Degrees of freedom.**
- *Rows:* 8.
- *Per-row selected inputs (8):*
  - the six Z_f values, which the ledger's own disclaimer calls "fitted": 3, 9, 1/48, 3/4, κ/8 and 1/2π;
  - the W exponent 27;
  - the Z angle sin²θ_W = φ⁻³.
- *Shared continuous selection (1):* ξ_vac = 100φ.
- *Residual dof:* 8 − 9 = **−1**.
- *Discrete selections, not counted:*
  - the r_eff(2π) := 1 normalisation (the 3.81% slack, a common factor on every row);
  - the knot assignment per row;
  - the convention for A (crossing number for the up quark, Alexander sums of squares for the other knots, Δ(t, t, t) for the proton);
  - the convention for L (lead below).
- §2.1 is therefore **a fit with residual dof ≤ −1**, not a prediction table. Its m₀ is anchored to m_e, which lies outside the table.

**Lead for B3** (unverified in this session; no verdict depends on it). The calculator's quark L values (16.372, 21.04, 23.60, 37.31) look like ideal ropelengths measured in tube *diameters*: the standard trefoil value is 16.37 in diameters and 32.74 in radii. Meanwhile L_e = 2π is the unknot per tube *radius*, and L_B is compared with per-radius values. If so, the table mixes thickness conventions by a factor of 2 in L, which is a further hidden selection.
- Both legs flag this from memory.
- The Ashton et al. 2011 tables could not be re-quoted because two fetches were rate-limited (see H-A3-2).

## Honesty items

- **H-A3-1 (exposure).**
  - What happened: the blind second leg ran in the background and returned at 09:22, before the first-leg script existed. This is the same pattern as H-A1-1 and H-A2-1.
  - Mitigation, partial: the first leg's decisive values were derived in-session before the second leg launched: 48 arctan √7, m ≈ 759 MeV at 58.006, A/Z_f ≈ 1/2 for 80.95, 20 against 70, and the PDG 2024 errors. They were not filed until afterwards. Every comparison number is a closed form or a deterministic computation from stated inputs, so there is no free choice through which exposure could act.
  - Process fix (carried from H-A2-1): file the first-leg values before launching a second leg.
- **H-A3-2 (sources).**
  - Two pages could not be read, both because the fetch proxy rate-limited them: the arXiv HTML of Ashton, Cantarella, Piatek & Rawdon's "Self-contact sets …" (math.DG/0508248), and the arXiv abstract of "Knot tightening by constrained gradient descent" (1002.1723).
  - CFKSW's Section 10 lay beyond the text extraction, so the number 58.006 itself was taken as quoted. The four-arc length computed here, 58.0526, decides the verdict independently: it is below 59.894.
- **H-A3-3 (first-leg defect, fixed before filing).** The piercing count double-counted samples lying exactly on a plane. It now uses half-open sides, and the topology result was unchanged.

## Blast radius (annotated in the Phase A fold)

1. **§2.15:** RETRACTED to Conjecture (clause 1), with clause 2's premise corrected, the E.1.3 row, m_p = 758.7 MeV at 58.006, the inversion, the calibration status of the neutron figure, and A = 20 against 70.
2. **§§2.4–2.6:** "predictive scope … limited to the Borromean L_B = 60.194 fm prediction". That prediction failed.
3. **§2.82:** the four-arc length 48 arctan √7 = 58.0526 per tube radius (two-leg). It is "within 0.1%" (0.080%) of 58.006.
4. **§2.14:** V4.52's seal ground (3) cites the falsification clause whose verification has now failed. "L strictly geometric" stands, and is exactly why the proton row fails.
5. **§2.1:** relabelled a fit (dof ≤ −1), with the PDG 2024 table, the headline not holding for u, d and c, W and Z stated, and the L-convention lead.
6. **M.ONT declaration (L247):**
   - mass clause: at the "tight (minimizer) configuration" the formula gives 759 MeV;
   - "Borromean linking (= baryon number)": UNPROTECTED;
   - the "Paper VII Conj. 1 … TRANSFER" item: the transferred prediction failed.
7. **VC-B annex (L253):** "linking = baryon number" is UNPROTECTED.
8. **Part V, M.ONT row (V4.51, L4359):** "Filament core (linking = baryon number; ideal-ropelength mass)", annotated as in 6 and 7.
9. **Part V, G-Φ1 row (L4328):** "L_p = ξ_vac/2 R1" and the "mass factorization 1836 = 12.39 × 148" are inversion properties.
10. **Part V, G-κ1 row (L4360):** "Ashton falsification clause": verification failed (see 1).
11. **Not ledger entries:** STATUS.md (plain-language status); Paper VII §9.1, E.1 and the calculators (Phase B3 drafts).

## What stands

- The four-arc and CFKSW geometry, as mathematics.
- The mass formula's form, as a fitting function.
- The two-component declaration, as a declaration.

What does not stand: any claim that the proton's mass, or the ±0.3 window, is predicted, and any claim that baryon number is topologically protected in this substrate.
