# A3 — The matter sector: pre-registration

**Plain-language summary.** The ledger's proton is three vortex loops linked like the Borromean rings. Its mass formula is said to predict how much "rope" those loops need: 60.194 units. This file fixes, before any new calculation, how five questions will be decided:
1. Are the ledger's rope units the standard ones used by the mathematicians who computed the tightest Borromean rings (58.006)?
2. If they are, the ledger's 60.194 ± 0.3 check fails. What exactly does the ledger's own rule then require?
3. Which of the three proton lengths on record (60.194, about 58.05, and 80.95) is a real length?
4. What, if anything, stops the linked loops from cutting through each other and coming apart, given that protons live longer than 10³⁴ years?
5. How should the mass table be labelled once its fitted inputs are counted and it is compared with current data (PDG 2024)?

**Lock.** Locked by its md5 in `A3_LOCK.txt` and by the commit that adds it, before any A3 computation file exists. Corrections go in dated addenda.

**Base.** V4.91, md5 `ce9ca6873adb5686227f5d103b41e3cc`. Line numbers below are V4.91's; the brief's numbers (V4.88) are 6 lower in this region.

## Objects of record

- **§2.15** (L640–L668).
  - L649: "Theorem 1 inverts to predict the ideal Borromean ropelength: L_B = 60.194 fm (within Ashton bounds [58.006, 62.0])."
  - L655, open verification (1): "Numerical minimization of the ideal Borromean ropelength returns a value within 60.194 ± 0.3 fm."
  - L658, the rule: "If either fails, the entry retracts to Conjecture status. If (1) returns a value outside the Ashton interval, the Borromean topological assignment for the proton is falsified."
- **§2.14's mass function.** m = m₀ (A/Z_f) exp(L / (Φ r_eff(L))), with:
  - r_eff(L) = 1 + ln(1 + L/ξ_vac) and ξ_vac = 100φ;
  - Φ = 2π − φ²/(8π²);
  - m₀ = m_e / exp(2π/Φ), with m_e = 0.511 MeV in the calculator.
- **§2.82's four-arc model.** "Arcs of radius-2 circles centered at the vertices of a rhombus of side 4 whose major diagonal exceeds the minor by 4; half-diagonals √7 ± 1 … With unit-thickness tubes …"
- **V4.40 record.** "The proton ropelength 80.95 sits at half the vacuum coherence length 100φ", from "the existing HANDOFF_MASS_CALC_v3 formula".
- **V4.52 record (G-κ1).**
  - L is "strictly the geometric length".
  - The tangle's flow is cut off at an inter-strand distance of about 2–4ξ.
- **M.ONT declaration (L247) and VC-B annex (L253).**
  - "Borromean linking (= baryon number)".
  - "Filament-core mass = ideal ropelength … the tight (minimizer) configuration".
- **§2.1's mass table and disclaimer.** The per-row inputs come from the project-store calculator `SQTCalculator.jsx` (v2.0).
- **Paper VII, Appendix E.1** (project store, `sqt_paper_VII_verified_clean.md`).
  - E.1.1: "ℒ = L/R (arc-length divided by tube radius)".
  - E.1.3: the outcome table.

## External anchors (fetched October 7, 2026, unless noted)

- **Cantarella, Kusner & Sullivan**, Invent. Math. 150 (2002) (CKS02). Figure caption: "This configuration of the Borromean rings has ropelength about 58.05. It is built from three congruent piecewise-circular plane curves, in perpendicular planes."
- **Cantarella, Fu, Kusner, Sullivan & Wrinkle**, Geom. Topol. 10 (2006) 2055 (CFKSW).
  - "In Section 10 … we will explicitly describe a very similar configuration of the Borromean rings, which we prove is critical and believe is the minimizer."
  - Their configuration B₀ is "very slightly shorter than the piecewise-circular version in [CKS02]".
  - The value 58.006 itself was not in the fetched text, because the extraction stops before Section 10. It is the value the ledger quotes.
- **PDG 2024.** S. Navas et al., Phys. Rev. D 110, 030001 (2024), summary tables.
  - Light quarks (MS-bar at 2 GeV): m_u = 2.16 ± 0.07 MeV; m_d = 4.70 ± 0.07 MeV.
  - Heavy quarks: m_c(m_c) = 1.2730 ± 0.0046 GeV; m_b(m_b) = 4.183 ± 0.007 GeV; m_t = 172.57 ± 0.29 GeV (direct measurements).
  - Bosons: m_W = 80.3692 ± 0.0133 GeV; m_Z = 91.1880 ± 0.0020 GeV.
  - Tau: m_τ = 1776.93 ± 0.09 MeV (2024 edition with its 2025 update).
- **Super-Kamiokande**, Phys. Rev. D 102, 112011 (2020): τ/B(p → e⁺π⁰) > 2.4 × 10³⁴ yr (90% CL).
- **Kleckner, Kauffman & Irvine**, Nat. Phys. 12, 650 (2016): 322 knots and links in the Gross–Pitaevskii model "universally untie" by reconnection.
- **Ruban**, "Long-lived quantum vortex knots", arXiv:1801.04822: quasi-stable windows with lifetimes of "many dozens and even hundreds of typical times".
- **From the October 4 Phase 2 report** (`lbc_bank/phase2/PHASE2_REPORT.md`, fetched then):
  - Guan, Zuccher & Liu, Phys. Fluids 37, 024126 (2025): Borromean vortex rings in a Gross–Pitaevskii superfluid reconnect into unlinked loops.
  - Poénaru & Toulouse, J. Physique 38, 887 (1977): the commutator obstruction to defect crossing.
  - Annala, Zamora-Zamora & Möttönen, Commun. Phys. 5, 309 (2022): protection needs non-commuting charges and can still be undone by vortex splitting.

## Decision rules

**DR-A3-1 (units).**
- *Computation.*
  - (a) The length of §2.82's four-arc configuration in closed form, with tube radius 1. The arcs then have radius 2, the contact distance.
  - (b) A numerical check that tubes of radius 1 are embedded: curvature radius ≥ 1; distance between distinct components ≥ 2; non-local self-distance ≥ 2.
  - (c) A check that the three curves sit in the standard Borromean piercing pattern, with pairwise linking numbers 0.
- *Rule.*
  - If (a) is within 0.2% of CKS02's "about 58.05", then 58.05 and 58.006 are lengths per unit tube radius.
  - If Paper VII E.1.1's L is also length per tube radius, record **UNITS MATCH**.
  - If the ledger's L is per tube diameter, record **UNITS DIFFER** and evaluate DR-A3-2 in both conventions. In diameters, the comparison values halve.

**DR-A3-2 (verification (1) and §2.15's rule).**
- *Upper bound.* The ideal (minimum) ropelength is at most the length of any explicit embedded configuration. So take U = min(58.006, the DR-A3-1(a) length). 58.006 is CFKSW's B₀ as quoted.
- *Clause 1.* If U < 59.894 (= 60.194 − 0.3) in the convention of record, verification (1) **FAILS**. By §2.15's rule, the entry **RETRACTS to Conjecture status**.
- *Clause 2.* Evaluated as written.
  - It fires only if a Borromean configuration shorter than 58.006 − 0.001 is on record or is computed here.
  - Otherwise record "clause 2 not triggered as written", with the correction that 58.006 is the best-known configuration, an upper bound on the minimum, not a lower bound.
- *Paper VII.* Report what its own pre-stated E.1.3 outcome table says for the best value on record.
- *Mass at the geometric length.* Report m_p from §2.14 at L = 58.006 and at the DR-A3-1(a) length, with A = 20 and Z_f = 6. No further verdict depends on it.

**DR-A3-3 (which proton length stands).**
- *Classify* each of 60.194, ≈ 58.05 and 80.95 as one of:
  - **(G)**, the length of an explicit embedded Borromean configuration;
  - **(I)**, an inversion of m_p through §2.14 under a stated A/Z_f;
  - **(U)**, unidentified.
- *Test for (I).* A value is (I) if the ledger text derives it from the mass formula and an inversion with A/Z_f = p/q (p, q ≤ 20) reproduces it within 0.1%.
- *Rule.*
  - (I) and (U) values are retired as lengths.
  - The proton length of record is the shortest (G) value, and the ideal minimum is at most that value.
  - Any value above U cannot be the ideal length, whatever its provenance.

**DR-A3-4 (60.194 as m_p inverted).** If L(m_p = 938.272 MeV; A = 20, Z_f = 6) = 60.194 ± 0.001, record that the proton row's 0.000% and the neutron's −0.138% are calibration outputs, not predictions. Annotation only; no kill.

**DR-A3-5 (convention for A).**
- *Computation.*
  - Fox calculus on a Wirtinger presentation of the Borromean rings gives the multivariable Alexander polynomial Δ(t₁, t₂, t₃).
  - From it, the one-variable polynomial Δ(t) ≐ (t − 1) Δ(t, t, t) (Torres).
- *Report* the sums of squared coefficients of Δ(t, t, t) and of Δ(t).
- *Rule.* If they differ, annotate §2.15's "A = 20 from the Borromean Alexander polynomial" with both values, and name the convention it uses. Annotation only; no kill.

**DR-A3-6 (reconnection).**
- *Determine:*
  - (a) whether any stratum of the corrected vacuum inventory (A2, under G₂ × U(1)_ψ₀ × ℤ₃) has a non-Abelian π₁, which a Poénaru–Toulouse crossing obstruction needs;
  - (b) whether the ledger contains a computed energy or action barrier against core crossing for strands 2–4ξ apart (searched terms: reconnect, crossing, barrier, untie, Kleckner);
  - (c) what the literature listed above says.
- *Rule.* If (a) and (b) both find nothing:
  - record that "Borromean linking = baryon number" is **UNPROTECTED** on the vacuum of record;
  - annotate every entry that asserts it;
  - state the protection required, to order of magnitude: exp(−S) < 1/(ν τ_p) with τ_p > 2.4 × 10³⁴ yr, for two stated attempt rates ν (the core rate c/ξ_phys with V4.40's ξ_phys = 0.358 l_P, and the hadronic rate m_p c²/ħ);
  - register the successor.
- If (a) finds a non-Abelian stratum, record protection as conditional on that stratum and on the absence of vortex splitting (Annala et al. 2022), and register the successor computation.

**DR-A3-7 (mass table).**
- *Reproduce* §2.1's predicted column from the calculator inputs: A, Z_f and L per row; m_W = m₀ φ²⁷; m_Z = m_W / √(1 − φ⁻³). A row that does not reproduce to 0.1% is an honesty item.
- *Compute* the errors against the PDG 2024 central values above.
- *Rule.* §2.1's headline reads "within 2% of PDG central values for 6 fundamental fermions (plus the up quark within the PDG MS-bar band)". Annotate it as **NOT HOLDING**:
  - for each row whose |error| exceeds 2.00% against PDG 2024;
  - for the up quark, if its prediction lies outside PDG 2024's ±1σ interval.
- *W and Z* are reported with their errors.
- *Degrees of freedom* (no verdict).
  - Count the data rows.
  - Count the selected inputs named by the ledger itself (§2.1's disclaimer and §2.14's 3.81% slack) and by the calculator.
  - Report residual dof = rows − selected continuous inputs. List discrete selections (knot assignment, convention for A, convention for L) separately.
  - Relabel §2.1 a fit with that dof.
- *Lead* (no verdict): whether the calculator's quark L values use a different thickness convention from L_e = 2π and L_B. If the literature tables cannot be re-quoted in-session, record this as an unverified lead for B3.

## Second leg

A blind agent repeats the following without the first leg's files:
- the four-arc length and the embedding and piercing checks (DR-A3-1);
- the inversion L(m_p) for A/Z_f = 20/6, the A/Z_f that reproduces 80.95, and m_p at L = 58.006 (DR-A3-2, 3 and 4);
- §2.1's predicted column and its PDG 2024 errors, from the inputs listed here (DR-A3-7);
- the Fox-calculus Alexander polynomials (DR-A3-5).

*Agreement:* numbers to 10⁻⁶ relative (closed forms exactly), with identical classifications and verdicts. A disagreement halts the affected verdict until a third derivation settles it. DR-A3-6 is a reading of the record and the literature, so it has no second leg.

## Not in scope

- No new ropelength minimization, no new mass formula, and no re-fit.
- No edit of Paper VII or the calculators; Phase B3 drafts those.
- Nothing on Z_f = 6 (Conjecture 1) beyond its role in DR-A3-2.
- §2.52 Open 3 is untouched.
