# Isotone Steps of α-Decay Q-Values in the Deformed Actinide Region:  
## A Robust Break at Radium (Z = 88)

**Matthew Gifford** *(independent researcher, Hollister, CA)*  
Version 2 — October 2026. Corrects version 1 (Zenodo, May 29, 2026, doi:10.5281/zenodo.20448930); see the note at the end.

---

## Abstract

We report the behavior of the isotone step in alpha-decay Q-values,
ΔQ(Z,N) = Q_α(Z+2,N) − Q_α(Z,N), across the deformed actinide region
(N > 128). Using 51 isotone steps derived from 96 Q-values in the
AME2020 atomic mass evaluation, we find one robust break, at Z = 88 (Ra).
Grouped by proton number, the steps have means of 0.308 ± 0.059 MeV
(Z = 84–88), 0.599 ± 0.179 MeV (Z = 88–92) and 1.007 ± 0.302 MeV
(Z ≥ 92), and the pooled groups differ significantly (Welch t > 5.5).
Pooling, however, mixes neutron numbers. Compared at fixed neutron
number, the step across Z = 88 rises at every shared N, by 0.090 to
0.465 MeV, which coincides with the onset of permanent octupole
deformation near Ra. The apparent second break at Z = 92 does not survive
the same comparison: at fixed N it changes sign, and it is smaller than
the drift of a single boundary's step with N. It reflects the different
neutron coverage of the groups, and we do not claim it. N = 126
shell-closure effects are excluded by the N > 128 restriction.

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
Z = 84–100) using the AME2020 atomic mass evaluation [7]. Grouped by
proton number, the 51 available steps fall into three groups with
well-separated means. Compared at fixed neutron number, only the
boundary at Z = 88 holds, and it coincides with the documented onset of
octupole deformation near Ra. The apparent boundary at Z = 92 reflects
the different neutron coverage of the groups.

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
yields 51 isotone step measurements (74 over all N). The restriction is essential:
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
n. Regime separation is assessed by Welch's two-sample t-test. Because
the groups cover different ranges of N, each boundary is also tested by
comparing the steps on either side of it at the same N (Section 3.3).

---

## 3. Results

### 3.1 Grouping by Proton Number

Table 1 summarizes the regime statistics. Figure 1 shows all 51
individual N > 128 step measurements plotted against the U coordinate,
with regime mean lines and boundaries indicated. The grouping by Z is
visually clear; Section 3.3 tests which of its boundaries survive at
fixed N.

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

Both pooled differences are statistically significant, so the grouping
is not an artifact of small sample size. Pooling, however, mixes
neutron numbers; Section 3.3 separates the two.

### 3.3 Boundaries at Fixed Neutron Number

Within the full dataset (N = 130 to 156), the mean ΔQ per isotone step
increases with neutron number, with the steepest rise at N ≈ 138–140
(the Ra-226 / Th-230 region). The groups also cover different N ranges:
Regime I has N = 130–136, Regime II has N = 130–146, and Regime III has
N = 134–156. A difference between pooled group means can therefore
reflect N as well as Z. Table 2 compares the steps on either side of each
boundary at the same N.

**Table 2.** Isotone steps on either side of a boundary at equal N (MeV;
differences computed before rounding).

| N | Rn→Ra | Ra→Th | Across Z = 88 |
|---|-------|-------|---------------|
| 130 | 0.343 | 0.433 | +0.090 |
| 132 | 0.331 | 0.539 | +0.207 |
| 134 | 0.273 | 0.621 | +0.348 |
| 136 | 0.199 | 0.664 | +0.465 |

| N | Th→U | U→Pu | Across Z = 92 |
|---|------|------|---------------|
| 134 | 0.402 | 0.239 | −0.163 |
| 138 | 0.472 | 0.724 | +0.251 |
| 140 | 0.644 | 0.896 | +0.253 |
| 142 | 0.776 | 1.010 | +0.234 |
| 144 | 0.901 | 1.020 | +0.119 |
| 146 | 0.937 | 0.986 | +0.049 |

Across Z = 88 the step rises at every shared N. Across Z = 92 the
difference changes sign (negative at N = 134, positive at N = 138–146) and
falls toward zero at higher N. It is also smaller than the drift of the
Th→U step itself, which rises from 0.34 MeV at N = 136 to 0.93 MeV at
N = 146. We therefore claim one robust break, at Z = 88. A claim of a
break at Z = 92 would need a pre-registered test with controlled N
coverage.

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

### 4.2 Z = 92: Not Supported at Fixed N

The pooled means also change at Z = 92 (U). Empirical subdivision of the
actinide region at approximately Z = 89–92 has also been employed for
phenomenological Geiger-Nuttall fitting, where a single power-law
relationship for the actinides requires separate fitting parameters in
the Z < 92 and Z > 92 regions [9]. In the present data, however, the
Z = 92 boundary does not survive the fixed-N comparison of Section 3.3:
the difference across it changes sign and is smaller than the drift with
N within a single boundary. We therefore do not claim a structural
transition at Z = 92.

### 4.3 What the Grouping Reflects

The picture that emerges is physically coherent. Regime I (Z = 84–88)
is the region between the Z = 82 shell closure and the deformation
onset, where nuclei are still relatively close to spherical and the
Q-value gradient with Z is modest. Regime II (Z = 88–92) spans the
deformation onset region: Ra and Th are in the region of permanent
octupole deformation with rapidly evolving structure, producing a
more variable and larger mean gradient. Regime III (Z ≥ 92) covers
the well-deformed actinides, where the Q-value gradient with Z is largest
and most consistent with systematic Coulomb driving; its higher mean also
reflects its wider and higher range of N (Section 3.3).

### 4.4 The Approximate Doubling Ratio

The II/I ≈ 2.0 ratio is notably clean, while III/II ≈ 1.68. The III/II
ratio compares groups with different N coverage (Section 3.3). The exact ratio values
depend on the particular N range accessible in AME2020 for each Z range
and may shift as new mass measurements become available, particularly for
neutron-rich Ra and Rn isotopes (which contribute to Regime I) where
the dataset is thinnest (n = 7).

### 4.5 Limitations

**Dataset completeness.** Regime I has n = 7 measurements — the
smallest sample — because isotone chains with both Z = 84 (Po) and
Z = 86 (Rn) data at N > 128 are restricted by the short half-lives
and measurement challenges for neutron-rich Po and Rn isotopes. The
reported Regime I mean should be treated with appropriate caution;
new measurements in this region could shift it.

**N-correlation.** The available isotone chains are not uniformly
distributed in N across regimes (Section 3.3). The fixed-N comparison
shows that this accounts for the apparent Z = 92 boundary, while the
Z = 88 boundary holds at every shared N. A fully controlled comparison
would require equal N coverage across regimes, not yet available from
AME2020.

**Exclusion of odd-Z isotones.** We analyze only even-even nuclei.
Odd-Z isotones could in principle show similar structure, but pairing
effects and Nilsson-level blocking would complicate the comparison.
We make no claim about odd-Z behavior.

---

## 5. Conclusions

The isotone step ΔQ(Z,N) = Q_α(Z+2,N) − Q_α(Z,N) in the deformed
actinide region (N > 128) shows one robust break, at Z = 88, over 51
steps from AME2020. Grouped by Z, the steps form three groups whose pooled
means differ significantly (t > 5.5), but compared at fixed N only the
Z = 88 boundary holds: the step across it rises at every shared N. It
coincides with the documented onset of octupole deformation at Ra. The
apparent boundary at Z = 92 reflects the groups' different N coverage and
is not claimed.

This analysis is the first, to our knowledge, to characterize the
isotone Q-value step as a primary observable across the deformed
actinide series. The N > 128 restriction is essential: shell-closure
effects at N = 126 would mask the structure entirely.

Improved mass measurements for neutron-rich Po and Rn isotopes would
sharpen the Regime I statistics, and wider N coverage would allow a
controlled test at Z = 92.

**Note on version 2.** Version 1 was deposited on Zenodo on May 29, 2026 (doi:10.5281/zenodo.20448930).
This version corrects it:
(1) the N > 128 step count is 51, not 74 (74 counts all N);
(2) only the Z = 88 break is claimed, and the Z = 92 boundary is shown not
to survive a fixed-N comparison (Section 3.3, Table 2);
(3) the former Sections 4.5–4.6 are removed: a structural account drawn
from a separate framework, and the Curium prediction it motivated, which
the data did not confirm. The reference cited for that account did not
contain it;
(4) an incomplete citation, and the sentence that relied on it, are
removed;
(5) the abstract's statement that half of the Curium prediction was
confirmed is removed with it, since that step showed no significant
elevation (t = +0.4).
The data, the Q-values and Table 1 are unchanged.

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

[9] Akrawy, D.T. (2020). Z. Naturforsch. A 75, 1031.

---

*Figure caption:* **Figure 1.** Isotone Q-value steps ΔQ(Z,N) in the
deformed actinide region (N > 128), plotted against U = Z − 80 (the
lower-Z boundary of each step). Individual measurements are shown as
points; horizontal lines are regime means. Shaded regions and colors
identify the three groups. Dashed vertical lines mark the group
boundaries at Z = 88 (Ra) and Z = 92 (U); only the first survives the
fixed-N comparison of Section 3.3. Element labels at top
identify the lower-Z nucleus of each step column.

