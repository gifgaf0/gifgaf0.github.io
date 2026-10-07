# B4 — The alpha-decay paper: retraction check and ledger entry

**Plain-language summary.** The paper's Q-values are right. Its seven benchmark values match published values to within 0.2 keV, and its regime table reproduces exactly from its own data. The ledger had no entry for it; one is drafted below. Checked against the ledger's retractions, the text has three problems.
- **It claims two breaks; the ledger records one.** The paper reports two sharp changes, at radium (Z = 88) and uranium (Z = 92). The ledger's own record says an earlier audit reduced this to one real break, at Z = 88, which has a standard explanation (the onset of nuclear deformation). The paper's numbers agree with the ledger once steps with the same neutron number are compared:
  - The Z = 88 jump appears at every shared neutron number.
  - The Z = 92 "jump" changes sign. It is smaller than the drift with neutron number inside a single regime. Most of it comes from the third regime containing heavier-neutron steps.
- **Its theoretical section rests on retired or unpublished pieces.** The angle thresholds come from a lemma whose key steps the ledger retracted, and from a ferromagnetism bridge the ledger records as refuted. The citation for them points to the gauge paper, which does not contain them. The Curium prediction that section motivated failed; the paper says so.
- **Two factual slips.**
  - The paper says 74 steps where its table uses 51.
  - It calls ²⁰⁸Pb the end of "all" actinide decay chains; only the thorium series ends there.

The ledger has a related slip in §2.21, which says alpha decay becomes "thermodynamically inevitable" beyond ²⁰⁸Pb. In fact ²⁰⁸Pb itself already has a positive alpha-decay energy, +0.517 MeV.

Nothing is published. Whether to correct the deposit is the author's decision; a list of corrections is at the end.

**The text checked.** `alpha_decay_three_regime_paper.md` from the project store ("Draft — May 2026", dated May 28; md5 `770ac49755f559841e0e6d7c9b083f1b`). The brief calls it the deposited text, but neither the ledger nor the store records the deposit, and the record could not be read here. If the deposited version differs, these checks apply to the store text. **The ledger entry needs the deposit's DOI and date from the author.**

## Checks (`b4_checks.py`; reads only the literal AME2020 table in the store's `ame2020_qvalues.py`)

| Check | Result |
|---|---|
| Q-values | 96 even-even Q_α > 0. The seven benchmarks (²¹⁰Po … ²⁴⁴Cm) match to ≤ 0.2 keV, as the paper states (store script output) |
| Table 1 (N > 128) | Reproduced: I 0.308 ± 0.059 (n = 7), II 0.599 ± 0.179 (14), III 1.007 ± 0.302 (30). Welch t = 5.51 and 5.59 from those numbers |
| Step count | **51** steps for N > 128. The 74 of the abstract, §2 and §5 is the count for all N, and for all N regimes I and II do not separate (0.647 vs 0.641 MeV) |
| N composition | Regime I has N = 130–136, II has 130–146, III has 134–156 |
| Z = 88 at fixed N (Rn→Ra vs Ra→Th) | +0.09, +0.21, +0.35, +0.47 MeV at N = 130, 132, 134, 136: positive at every shared N |
| Z = 92 at fixed N (Th→U vs U→Pu) | −0.16, +0.25, +0.25, +0.23, +0.12, +0.05 MeV at N = 134 … 146: changes sign |
| N drift inside one boundary (Th→U) | 0.35 MeV at N = 136 rising to 0.94 MeV at N = 146 |
| Cm test (§4.6) | Pu→Cm 0.842 (n = 6), Cm→Cf 1.019 (n = 7), as the paper reports; the paper's σ there are population SDs, while Table 1 uses sample SDs |
| U↔θ map of §4.5 | θ = 0, π/8, π/4 at U = 2, 8, 12: steps of 6 and then 4 units of U per π/8, read off from the data |
| Q_α of lead (AME2020) | ²⁰⁸Pb **+516.7 keV**, ²⁰⁶Pb +1134.9 keV, ²⁰⁴Pb +1968.5 keV |

**The fixed-N comparisons are descriptive.** They decide no verdict here. The ledger already records the reduction to one break (Preamble, M.CW instances: "§3.A.3 … the three-regime finding reduced on audit to one real break at Z=88 with a conventional octupole-deformation explanation"). That audit's own record is not in the ledger body or the project store. The comparisons show that the paper's data agree with it. If the author wants the ledger to rest on a formal N-controlled test, that test needs a pre-registered rule.

## Against the retractions

| Item | Finding |
|---|---|
| **Slot counting; the sin²(πU/4) envelope (§3.A.3); the Harmonic Saturation Theorem, 4-8-12 (§3.A.2)** | The text uses neither slot counting nor sin²(πU/4). Its regime edges, U = 4, 8 and 12, are the retracted 4-8-12 sequence, presented here as empirical boundaries. §4.6's "U = 16 = 2 × dim(𝕆), an algebra transition point" is a capacity reading of the retracted kind; the prediction it motivated failed (Pu→Cm below the regime mean, t ≈ −5.2), as the paper reports. The two-transition claim conflicts with the ledger's record of one real break (above). |
| **The structural account (§4.5)** | It rests on Lemma θ (§2.17, R2). The ledger retracted its π/8 sign flip (§3.01) and its Route 1 sketch (§3.02), and lists the ferromagnetism bridge as "refuted, R3". The form used, J(θ) = −sin 2θ·e₀ + cos 2θ·e₄, is not the ledger's current one, J₀ cos(Nθ). Ref. [11] (the gauge paper) contains neither J(θ) nor Lemma θ; both v5 (May 2026) and v6.3 were checked. "No parameter is adjusted" conflicts with the U↔θ steps (6, then 4) being read from the data, which the paper's own next paragraph concedes. |
| **§2.45-NGA** | The paper does not use it; it attributes the Z = 88 break to octupole deformation, as the ledger's M.CW record does. §2.45-NGA itself has three problems: it identifies the U = 8 boundary (Z = 88, Ra) with the noble-gas closure at Z = 86 (Rn, U = 6), one even-Z step away; it uses an electron-shell closure for a nuclear observable; and it sits in the "alpha-decay slot framework", the territory of the retracted §3.A.2/§3.A.3. As stated it is not a prior address. |
| **Cluster D, §2.21** | §2.21 says ²⁰⁸Pb is the boundary "beyond which alpha-decay becomes thermodynamically inevitable". Q_α(²⁰⁸Pb) = +516.7 keV, and lighter lead isotopes have larger Q_α. Alpha decay is exothermic at and below ²⁰⁸Pb, which is stable in practice because its decay is unobservably slow. The paper's §4.5 ("the terminus toward which all actinide chains converge") is wrong for a related reason. Of the four decay series only thorium's (4n) ends at ²⁰⁸Pb; uranium's ends at ²⁰⁶Pb, actinium's at ²⁰⁷Pb, and neptunium's at ²⁰⁹Bi/²⁰⁵Tl. |

**Incidental (ledger §2.17).** §2.17 states θ_c = π/(2N) and then "for the f-block (N = 8), θ_c = π/8". But π/(2·8) = π/16. Its π/8 corresponds to N = 4, or to |sin 2θ| = |cos 2θ| in the form the paper uses. This is an annotation for the fold.

## Ledger entry (proposed for the Phase B fold as §2.93.B4)

> **§2.93.B4 — The alpha-decay paper ("Three-Regime Structure in α-Decay Q-Value Isotone Steps in the Deformed Actinide Region", M. Gifford, May 2026; deposit ⟨DOI and date to be entered by the author⟩).**
>
> *What it reports (R1 for the data).* ΔQ(Z,N) = Q_α(Z+2,N) − Q_α(Z,N) from AME2020: 96 even-even Q-values, seven benchmarks to ≤ 0.2 keV. For N > 128 the regime table reproduces exactly: 0.308 / 0.599 / 1.007 MeV, n = 7 / 14 / 30. That is **51 steps, not the 74 the text states**; 74 is the all-N count.
>
> *Status of its claims.* The break at Z = 88 holds at fixed N at all four shared neutron numbers, with the conventional octupole-deformation account (R2 observation). The Z = 92 break is **not supported** as a Z effect: at fixed N it changes sign and is smaller than the N drift within one boundary, and the regimes differ in N coverage. This agrees with the ledger's record that the finding reduced on audit to one real break at Z = 88 (M.CW instances; §3.A.3). The structural account (§4.5) and the Curium prediction (§4.6, failed) rest on Lemma θ (§2.17, R2; §3.01 and §3.02 retracted, the ferromagnetism bridge refuted) and on a capacity reading of the retracted 4-8-12 kind (§3.A.2). The citation offered for them (the gauge paper) does not contain them. The text also misstates the decay-chain endpoints of ²⁰⁸Pb.
>
> *Disposition.* Data and the Z = 88 observation banked (R2). The two-transition claim and §4.5–§4.6 are not supported by the ledger. A correction of the deposit is the author's decision (Part VI). A formal N-controlled test, if wanted, needs a pre-registered rule.

**Brackets** (V4.92 line numbers):

| Line | Entry | Bracket |
|---|---|---|
| L527 | §2.21 Pb-208 sedenion boundary | Q_α(²⁰⁸Pb) = +516.7 keV (AME2020); alpha decay is exothermic at and below ²⁰⁸Pb, so the boundary is not "beyond which alpha-decay becomes thermodynamically inevitable". ²⁰⁸Pb is also not the end of all decay chains: only the 4n series ends there. |
| L1431 | §2.45-NGA | Off by one even-Z step (Rn is Z = 86, U = 6; the boundary is U = 8, Z = 88). It uses an atomic shell closure for a nuclear observable, and it rests on the slot framework of the retracted §3.A.2/§3.A.3. The alpha-decay paper and the ledger's M.CW record attribute the Z = 88 break to octupole deformation. Not a prior address as stated. |
| L500 | §2.17 Lemma θ | π/(2N) with N = 8 is π/16, not π/8. The alpha-decay paper's π/8 is \|sin 2θ\| = \|cos 2θ\| in a different form of J(θ). |
| Part VI | new row | Alpha-decay paper: correction of the deposit (51 steps; one robust break at Z = 88; §4.5–§4.6; ref. [11]; decay-chain endpoints). Open; author's decision. |

## Corrections the author may want in the deposit (not drafted as a new version)

1. Abstract, §2 and §5: 74 → 51 steps (N > 128).
2. Claim one robust break, at Z = 88, or run a pre-registered N-controlled test before claiming Z = 92. Remove §3.3's "it is not driven by a correlation between N and Z"; §4.7 and the fixed-N comparison contradict it.
3. §4.5: remove "the terminus toward which all actinide chains converge". Remove "No parameter is adjusted", or state that the U↔θ map is read from the data. Replace ref. [11], which does not contain J(θ), or drop §4.5–§4.6. They are the paper's only tie to the SQT framework, and the draft notes already suggest moving them to a footnote.
4. Ref. [9] is marked "[Citation pending]" in the text; complete it or remove the sentence.

## Files

| File | md5 |
|---|---|
| `b4_checks.py` | `fcec79eafd727c67820ef8fda0e72bc1` |
| `b4_checks_output.txt` / `b4_checks.json` | `22c0670766c968357f5eaee2e4fa111b` / `40e53f8e779771872d15e94fa759035b` |
| `source/alpha_decay_three_regime_paper.md` (store text) | `770ac49755f559841e0e6d7c9b083f1b` |
| `source/ame2020_qvalues.py` (store script) | `25ddfab78ff7348bffcbaef5c40fcdee` |
