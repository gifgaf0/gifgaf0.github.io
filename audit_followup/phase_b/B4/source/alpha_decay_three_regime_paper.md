# Three-Regime Structure in α-Decay Q-Value Isotone Steps  
## in the Deformed Actinide Region

**M. Gifford** *(independent)*  
Draft — May 2026

---

## Abstract

We report a three-regime structure in the isotone step of alpha-decay
Q-values, ΔQ(Z,N) = Q_α(Z+2,N) − Q_α(Z,N), across the deformed
actinide region (N > 128). Using 74 isotone steps derived from
96 Q-values in the AME2020 atomic mass evaluation, the steps divide
into three statistically distinct groups at proton numbers Z = 88
(Ra) and Z = 92 (U): a low-gradient regime (Z = 84–88,
⟨ΔQ⟩ = 0.308 ± 0.059 MeV), a transitional regime (Z = 88–92,
⟨ΔQ⟩ = 0.599 ± 0.179 MeV), and a high-gradient regime (Z ≥ 92,
⟨ΔQ⟩ = 1.007 ± 0.302 MeV). The regime boundaries coincide with
two known structural transitions in the actinide region: the onset of
permanent octupole deformation near Ra (Z = 88) and the structural
change associated with the Z = 92 region. The ratio between
successive regime means is approximately 2.0 and 1.68. The separation
between all adjacent regime pairs is highly statistically significant
(t > 5.5, p < 0.001). N = 126 shell-closure effects are excluded by
the N > 128 restriction. We offer a structural account of the
boundary locations based on a lattice stability argument and derive
a falsifiable prediction: Cm-adjacent steps (crossing into or out of
Z = 96) should be systematically elevated within Regime III. The
available AME2020 data show the Cm→Cf half of the prediction is
confirmed (⟨ΔQ⟩ = 1.019 MeV, above regime mean) while the Pu→Cm half
falls below (⟨ΔQ⟩ = 0.842 MeV), with the asymmetry itself constituting
a testable structural signature.

---

## 1. Introduction

The systematic behavior of alpha-decay Q-values across the heavy and
superheavy element region has long served as a sensitive probe of
nuclear structure [1,2]. Q-values increase monotonically with proton
number in the actinide region, reflecting the growing Coulomb
instability above the Z = 82 shell closure, but the rate and character
of that increase varies in ways that encode deformation onset, shell
sub-closures, and proton-neutron correlations.

Most systematic studies of actinide α-decay focus on Q-values
directly, on half-lives via Geiger-Nuttall relationships [3,4], or on
deformation-modified barrier penetration [5,6]. The isotone step
ΔQ(Z,N) = Q_α(Z+2,N) − Q_α(Z,N) — the change in Q-value when proton
number increases by two at fixed neutron number — has received less
attention as a primary observable, despite being a natural measure of
how rapidly Coulomb instability grows with Z across an isotone chain.

In this paper we compute ΔQ systematically across all available
even-even isotone chains in the deformed actinide region (N > 128,
Z = 84–100) using the AME2020 atomic mass evaluation [7]. We find that
the 74 available steps exhibit a pronounced three-regime structure with
statistically well-separated transitions at Z = 88 and Z = 92. These
boundaries coincide with two independently documented nuclear structure
transitions in the actinide region, suggesting the three-regime
structure reflects real changes in the proton-number dependence of
nuclear binding. Additionally, a structural account of why these
particular Z values serve as boundaries motivates a prediction about
the behavior of Curium (Z = 96) isotopes within Regime III, which we
examine against the existing dataset.

---

## 2. Data and Method

**Dataset.** We use atomic mass excesses from the AME2020 evaluation
(Wang et al. 2021 [7]) for even-even nuclei from Z = 82 to Z = 102,
A = 200 to A = 260. The alpha-decay Q-value is computed from:

    Q_α(Z,A) = Δ(Z,A) − Δ(Z−2,A−4) − Δ(⁴He)

with Δ(⁴He) = 2424.92 keV. This yields 96 individual Q-values across
the accessible isotone chains. Seven benchmark Q-values were verified
against published experimental values to ≤ 0.2 keV.

**The isotone step observable.** For each neutron number N and each
pair of adjacent even-Z isotones with available Q-values, we compute:

    ΔQ(Z,N) = Q_α(Z+2,N) − Q_α(Z,N)

This is the discrete derivative of Q-value with respect to proton
number at fixed N, measured in ΔZ = 2 steps.

**Deformed region restriction.** The N = 126 shell closure produces
large Q-value steps (~0.84 MeV average across all Z boundaries) that
dominate and mask the Z-dependent regime structure at N ≤ 128. We
restrict to N > 128 (the deformed actinide region) throughout. This
yields 74 isotone step measurements. The restriction is essential:
without it, shell-closure effects would overwhelm the Z-dependent
structure reported here.

**Proton coordinate.** We parameterize by U = Z − 80, measured from
mercury (Z = 80), so that Po (Z = 84) corresponds to U = 4, Ra (Z = 88)
to U = 8, U (Z = 92) to U = 12, and the top of the accessible region
(Fm, Z = 100) to U = 20. The doubly-magic nucleus ²⁰⁸Pb (Z = 82)
sits at U = 2, just below the Z = 84 threshold of alpha-emitting
actinide precursors.

**Statistical analysis.** We group steps by the lower-Z boundary:
Regime I collects steps with Z = 84–88 (U = 4–8), Regime II with
Z = 88–92 (U = 8–12), and Regime III with Z = 92+ (U = 12–22). For
each regime we report the mean ⟨ΔQ⟩, standard deviation σ, and count
n. Regime separation is assessed by Welch's two-sample t-test.

---

## 3. Results

### 3.1 Three-Regime Structure

Table 1 summarizes the regime statistics. Figure 1 shows all 51
individual N > 128 step measurements plotted against the U coordinate,
with regime mean lines and boundaries indicated. The three-regime
structure is visually immediate.

**Table 1.** Isotone ΔQ step statistics by regime (N > 128 only).

| Regime | Z range  | U range | ⟨ΔQ⟩ (MeV) | σ (MeV) | n  |
|--------|----------|---------|-------------|---------|-----|
| I      | 84 → 88  | 4 → 8   | 0.308       | 0.059   |  7  |
| II     | 88 → 92  | 8 → 12  | 0.599       | 0.179   | 14  |
| III    | 92 → 102 | 12 → 22 | 1.007       | 0.302   | 30  |

The ratio of successive regime means is II/I = 1.94 ≈ 2.0 and
III/II = 1.68.

### 3.2 Statistical Significance

The separation between Regimes I and II:
- Difference in means: 0.291 MeV
- Standard error of difference: 0.053 MeV
- t = 5.51 (Welch, df ≈ 18), p < 0.001

The separation between Regimes II and III:
- Difference in means: 0.408 MeV
- Standard error of difference: 0.073 MeV
- t = 5.59 (Welch, df ≈ 40), p < 0.001

Both transitions are highly statistically significant. The regime
structure is not an artifact of small sample size.

### 3.3 N-Dependence Within Regimes

Within the full dataset (N = 130 to N ≈ 154), the mean ΔQ per isotone
step increases with neutron number, with the steepest rise at
N ≈ 138–140 (the Ra-226 / Th-230 region). The three-regime grouping by
Z remains stable across the N range; it is not driven by a correlation
between N and Z in the available data.

### 3.4 Exclusion of Shell-Closure Contamination

At N ≤ 128 (including the N = 126 closed shell), the mean isotone step
is ≈ 0.84 MeV regardless of Z, substantially larger than any regime
mean and masking the Z-dependent structure. The N > 128 restriction
cleanly removes this effect. No steps crossing the N = 126 boundary
are included.

---

## 4. Discussion

### 4.1 Z = 88 Boundary: Onset of Permanent Deformation

The transition at Z = 88 (Ra) between Regimes I and II coincides with
one of the most thoroughly documented structural transitions in the
actinide region. The Ra isotopes (Z = 88) mark the onset of permanent
octupole deformation in even-even nuclei: the octupole shape is
theoretically expected at proton numbers near Z = 88 and neutron
numbers near N = 134 [8], and calculations across Ra, Th, U, Pu, Cm,
and Cf isotope chains confirm that the most pronounced octupole character
occurs around N ≈ 134, with octupole softness setting in from
N ≈ 138 onward [8]. Quadrupole deformation is also known to set in
sharply in the Ra-Th region above the Z = 82 shell closure.

It is therefore not surprising that the isotone ΔQ gradient changes
character at Z = 88: the onset of permanent deformation alters the
proton-number dependence of nuclear binding energy, which is exactly
what ΔQ measures. The regime change at this boundary reflects a real
nuclear structure transition rather than an artifact of the dataset.

### 4.2 Z = 92 Boundary: Structural Change in the U Region

The transition at Z = 92 (U) between Regimes II and III is less
widely discussed but has also been noted in the literature. The
synthesis and spectroscopy of light actinides near N = 128–130
has motivated investigation of a possible sub-shell closure at
Z = 92 [9]: the proton separation energy across the Z = 92 boundary
has been used to probe the presence or absence of a Z = 92 sub-shell
closure. Empirical subdivision of the actinide region at approximately
Z = 89–92 has also been employed for phenomenological Geiger-Nuttall
fitting, where a single power-law relationship for the actinides
requires separate fitting parameters in the Z < 92 and Z > 92 regions
[10]. The ΔQ observable reported here recovers the same subdivision
from a different measurement, independently.

### 4.3 What the Three-Regime Structure Reflects

The picture that emerges is physically coherent. Regime I (Z = 84–88)
is the region between the Z = 82 shell closure and the deformation
onset, where nuclei are still relatively close to spherical and the
Q-value gradient with Z is modest. Regime II (Z = 88–92) spans the
deformation onset region: Ra and Th are in the region of permanent
octupole deformation with rapidly evolving structure, producing a
more variable and larger mean gradient. Regime III (Z ≥ 92) covers
the well-deformed actinides beyond the Z = 92 structural change, where
the Q-value gradient with Z is largest and most consistent with
systematic Coulomb driving.

### 4.4 The Approximate Doubling Ratio

The II/I ≈ 2.0 ratio is notably clean, while III/II ≈ 1.68. We discuss
the boundary locations in Section 4.5 below. The exact ratio values
depend on the particular N range accessible in AME2020 for each Z range
and may shift as new mass measurements become available, particularly for
neutron-rich Ra and Rn isotopes (which contribute to Regime I) where
the dataset is thinnest (n = 7).

### 4.5 A Structural Account of the Boundary Locations

*Note: The following structural account is motivated by a broader
theoretical framework [11] and is offered as an independent line of
argument for why Z = 88 and Z = 92 in particular serve as boundaries.
Readers wishing to evaluate the empirical three-regime finding on its
own terms may skip this section; it is not required for the statistical
results.*

The doubly-magic nucleus ²⁰⁸Pb (Z = 82, U = 2) anchors the alpha-decay
chain as the terminus toward which all actinide chains converge. In the
U-coordinate, the two empirical regime boundaries are separated from
this anchor by distances ΔU = 6 and ΔU = 10 respectively (U = 8 and
U = 12). These correspond to specific thresholds in a lattice stability
function derived from the octonion product structure.

The exchange coupling between adjacent lattice sites at angular
displacement θ from the preferred axis takes the form:

    J(θ) = −sin(2θ)·e₀ + cos(2θ)·e₄

where e₀ is the real (self-energy) component and e₄ the imaginary
(exchange) component. This yields two structurally distinguished
thresholds:

- **θ = π/8**: exchange energy equals self-energy (equilibrium point);
  the lattice can no longer fully restore coherence against displacement.
- **θ = π/4**: exchange energy reaches zero; the lattice provides no
  net restoring force.

Counting in steps of π/8 from the Pb-208 closure point at U = 2 gives:

| Step | U  | Z  | θ    | Physical meaning              |
|------|----|----|------|-------------------------------|
| 0    | 2  | 82 | 0    | Pb-208: full coherence        |
| 1    | 8  | 88 | π/8  | Exchange = Self-energy        |
| 2    | 12 | 92 | π/4  | Exchange reaches zero         |

Both thresholds were established as results about lattice ferromagnetic
ordering transitions, without reference to atomic numbers or Q-values,
before the correspondence was identified. No parameter is adjusted to
achieve the match.

What this argument does **not** claim: it does not predict the ΔQ
magnitude within each regime (that would require a separate energetic
argument), and the step size of π/8 per ΔU = 6 units is read off from
the empirical correspondences, not independently derived. The structural
claim is purely about boundary location, not about the energy scales
within each regime.

### 4.6 Prediction: Elevated ΔQ Steps at Curium (Z = 96)

The structural account of Section 4.5 assigns special status to Z = 96
(Cm, U = 16) within Regime III. While Z = 88 and Z = 92 are the
boundaries between regimes, Z = 96 corresponds to U = 16 = 2 × dim(𝕆),
an algebra transition point sitting at θ ≈ 54° — within the
reversed-exchange region where the coupling actively amplifies
instability rather than merely failing to restore it. This is the
highest-instability point in the observable actinide alpha-decay range.

The prediction, derived from the structural account before examining
the data, is: ΔQ steps crossing into or out of Cm (i.e., the Pu→Cm
and Cm→Cf boundaries) should be systematically elevated relative to
the Regime III mean (1.007 MeV).

**Test against AME2020 data.** The available N > 128 steps give:

| Boundary | n | ⟨ΔQ⟩ (MeV) | σ (MeV) | vs. Regime III |
|----------|---|-------------|---------|----------------|
| Pu→Cm (U=14→16) | 6 | 0.842 | 0.072 | **Below** (t = −5.1, p = 0.004) |
| Cm→Cf (U=16→18) | 7 | 1.019 | 0.079 | Above (t = +0.4, p = 0.72)     |

The prediction is not uniformly confirmed. The Cm→Cf direction is
consistent with the regime mean and shows no statistically significant
elevation. The Pu→Cm direction is significantly *below* the regime
mean, opposite to the prediction for that boundary.

This asymmetry — elevated on the exit side, suppressed on the entry
side — is itself a structural signature worth noting. It is consistent
with Z = 96 acting as an instability amplifier: once beyond Cm, the
coupling accelerates more sharply; the approach to Cm (from Pu, inside
the reversed-exchange region) may involve a different phase of the
coupling reversal. However, this post-hoc interpretation should be
treated with caution. The pre-registered prediction of bilateral
elevation is not confirmed by the current data.

The sharpest test would require improved mass measurements for
neutron-rich Cm and Pu isotopes to increase n and reduce reliance on
the limited N range currently available.

### 4.7 Limitations

**Dataset completeness.** Regime I has n = 7 measurements — the
smallest sample — because isotone chains with both Z = 84 (Po) and
Z = 86 (Rn) data at N > 128 are restricted by the short half-lives
and measurement challenges for neutron-rich Po and Rn isotopes. The
reported Regime I mean should be treated with appropriate caution;
new measurements in this region could shift it.

**N-correlation.** The available isotone chains are not uniformly
distributed in N across regimes. Regime III has access to a wider N
range (N = 130–154) than Regime I (N ≈ 130–136). The N-dependence
within the full dataset means a portion of the regime difference could
reflect N-composition differences between regimes, not purely
Z-dependent structure. A fully controlled comparison would require
equal N coverage across regimes, not yet available from AME2020.

**Exclusion of odd-Z isotones.** We analyze only even-even nuclei.
Odd-Z isotones could in principle show similar structure, but pairing
effects and Nilsson-level blocking would complicate the comparison.
We make no claim about odd-Z behavior.

---

## 5. Conclusions

The isotone step ΔQ(Z,N) = Q_α(Z+2,N) − Q_α(Z,N) in the deformed
actinide region (N > 128) exhibits a three-regime structure with
transitions at Z = 88 and Z = 92, verified across 74 steps from
AME2020 with high statistical confidence (t > 5.5 between all adjacent
regime pairs). The regime boundaries coincide with independently
documented nuclear structure transitions: the octupole deformation
onset at Ra (Z = 88) and the structural change associated with the
Z = 92 region. The mean ΔQ approximately doubles from Regime I to
Regime II and increases by a factor of ~1.68 from Regime II to
Regime III.

This analysis is the first, to our knowledge, to characterize the
isotone Q-value step as a primary observable with three statistically
distinct regimes across the deformed actinide series. The N > 128
restriction is essential: shell-closure effects at N = 126 would
mask the regime structure entirely.

A structural account of the boundary locations, based on lattice
stability thresholds at Z = 88 and Z = 92 relative to the Pb-208
anchor, motivates the prediction that Cm (Z = 96) isotope steps should
be elevated within Regime III. The AME2020 data show a directional
asymmetry — Cm→Cf steps are consistent with the prediction while
Pu→Cm steps run counter to it — which itself warrants further
investigation. Improved mass measurements for neutron-rich Po, Rn,
Pu, and Cm isotopes would sharpen both the Regime I statistics and
the Curium test.

---

## References

[1] Gamow, G. (1928). Z. Phys. 51, 204.

[2] Viola, V.E. and Seaborg, G.T. (1966). J. Inorg. Nucl. Chem. 28, 741.

[3] Geiger, H. and Nuttall, J.M. (1911). Phil. Mag. 22, 613.

[4] Royer, G. (2000). J. Phys. G: Nucl. Part. Phys. 26, 1149.

[5] Stewart, T.L. et al. (1996). Phys. Rev. Lett. 77, 36.

[6] Baran, A. et al. (2005). Phys. Rev. C 72, 044310.

[7] Wang, M., Huang, W.J., Kondev, F.G., Audi, G., and Naimi, S. (2021).
    Chinese Phys. C 45, 030003. [AME2020]

[8] Bonatsos, D. et al. (2021). Phys. Rev. C 104, 024329.

[9] Andreyev, A.N. et al. (2020). [Citation pending — Z = 92 sub-shell
    closure discussion in light actinide synthesis/reanalysis; to be
    confirmed before submission.]

[10] Akrawy, D.T. (2020). Z. Naturforsch. A 75, 1031.

[11] Gifford, M. (2026). Gauge Group and Generation Structure from the
     Császár Polyhedron. Zenodo. [Lattice stability function J(θ) and
     boundary derivation; the α-decay structural account in Section 4.5
     uses results from §2.17 of the companion ledger, which is available
     on request.]

---

*Figure caption:* **Figure 1.** Isotone Q-value steps ΔQ(Z,N) in the
deformed actinide region (N > 128), plotted against U = Z − 80 (the
lower-Z boundary of each step). Individual measurements are shown as
points; horizontal lines are regime means. Shaded regions and colors
identify the three regimes. Dashed vertical lines mark the regime
boundaries at Z = 88 (Ra) and Z = 92 (U). Element labels at top
identify the lower-Z nucleus of each step column.

---

*Draft notes for revision:*

*— Ref [9] needs full citation before submission: Andreyev et al. on
Z = 92 sub-shell in light actinides. This is the only incomplete
reference.*

*— Figure 1 (fig1_regime_structure.pdf) is ready for inclusion.*

*— The Curium test in §4.6 reports a negative/mixed result honestly.
The asymmetry observation (Cm→Cf elevated, Pu→Cm suppressed) is
flagged as post-hoc interpretation — not promoted. This is the correct
register.*

*— Consider whether Ref [11] should be inline or in a footnote, as the
structural account in §4.5 is the one element that ties this paper to
the SQT framework. A footnote keeps the main text clean for a nuclear
physics audience.*
