# A3 second leg (blind): report

This is the blind second leg for `A3_PREREG.md` (md5 e2f1090cac3b097c0d2d205146c8b67c, which matches `A3_LOCK.txt`). In `A3_matter/` I opened only those two files. I read no first-leg file, no ledger, no Paper VII and no web page. Every number comes from `leg2_a3.py` (about 50 s to run). The full console output is in `leg2_output.txt`, and all values to 20 or more digits are in `leg2_results.json`.

## Plain-language summary

- **The four-arc Borromean model is a genuine configuration, 58.0526 tube radii long.** I built it from the ledger's description. Every arc is centred on a point of another loop, exactly 2 away, so the radius-1 tubes touch along their whole length without overlapping. The length is 12π + 24·asin(3/4) = 58.0526017386. That matches CKS02's "about 58.05" to 0.005%, so the published 58.05 and 58.006 are lengths per tube *radius*. Per diameter the same configuration measures 29.03.
- **The three loops are the standard Borromean rings.**
  - No two loops are linked: all linking numbers are 0.
  - Each loop's flat disc is pierced twice, in opposite directions, by exactly one neighbour, and the pattern runs in a cycle.
  - The configuration deforms, without any loops crossing, into the textbook model of three perpendicular ellipses.
  - Its Alexander polynomial, read off the projection of the actual 3-D curves, equals that of the standard diagram.
- **60.194 and 80.95 are mass-formula outputs, not geometric lengths.** Inverting the mass formula at the proton mass gives L = 60.19346 with A/Z_f = 20/6, and L = 80.9473 with A/Z_f = 1/2. Both are longer than the known 58.006 configuration, so neither can be the minimal length. At L = 58.006 the formula gives 758.7 MeV, not 938.3.
- **The mass table reproduces from its inputs, but three rows fail the locked test.** Every printed value is reproduced to within 0.007%. Against PDG 2024, up, down and charm fail the locked 2% / ±1σ test. W (+2.19%) and Z (+3.04%) are also more than 2% off.
- **"A = 20" comes from the wrong polynomial.** The Borromean polynomial is (t1−1)(t2−1)(t3−1).
  - Its diagonal value (t−1)³ has squared-coefficient sum **20**.
  - The link's actual one-variable polynomial is (t−1)⁴ (Torres), with sum **70**. The Conway polynomial z⁴ and the Burau route both confirm (t−1)⁴.

## Results

### T1: four-arc configuration (DR-A3-1)
| item | value |
|---|---|
| arcs (radius 2) | convex lobes centred at (0, ±(√7−1)), sweep π+asin(3/4) = 228.590°; concave waists centred at (±(√7+1), 0), sweep asin(3/4) = 48.590° |
| placement | C1 lies in z = 0 with its lobes along y; C2 = σC1 and C3 = σ²C1, where σ(x,y,z) = (z,x,y). Each lobe centre is the waist midpoint of the next component, and each waist centre is the lobe tip of the previous one. All 12 centres lie on another component (distance 0). |
| length, closed form | **12π + 24 asin(3/4)** = 12π + 24 atan(3/√7) |
| length | **58.0526017386** (58.05260173863306305…); one component: 19.3508672462 |
| numerical check | Richardson-extrapolated inscribed polygons agree to 2.8e-10 |
| difference from 58.05 / 58.006 | +0.0045% / +0.0803% |
| curvature radius | 2 on every arc (numerical minimum 1.99999999) |
| minimum distance between components | 2.000000000000000 for every pair; every point of every component is exactly 2 from another component |
| thickness, inf ρ_pt (whole link / one component) | 1.000000000000000 / √7−1 = 1.6457513111 |
| non-local self-distance | doubly-critical minimum 2(√7−1) = 3.2915026221; arc separation ≥ π: 2.8305; arc separation ≥ 2π: 3.2915 |
| enclosing radii | core radius ranges from √7−1 to √7+1, so the tube lies inside a sphere of radius √7+2 = 4.6457513111 and clears a ball of radius √7−2 = 0.6457513111 |
| linking numbers (exact polygon solid angle) | +2.7e-11, +4.3e-11, −1.2e-11, all 0 |
| disc piercings | D1: C2 twice (−,+), C3 not at all; D2: C3 twice, C1 not at all; D3: C1 twice, C2 not at all. The pattern is cyclic. |
| standard Borromean rings? | **Yes.** A radial isotopy keeping the axis points fixed carries it to three perpendicular ellipses with semi-axes √7∓1 (smallest gap along the way 1.42 > 0). Fox calculus on 2 generic projections (12 crossings each) gives Δ = (t1−1)(t2−1)(t3−1), the same as the braid. Every 2-component sublink has Δ = 0. |
| length per tube radius / per tube diameter | **58.0526017386 / 29.0263008693** |

### T2: mass-formula inversions (DR-A3-2/3/4)
Constants: Φ = 6.250027519360085, ξ = 100φ = 161.8033988749895, m₀ = 0.1869917255560066 MeV.

| quantity | value |
|---|---|
| (a) L(m_p = 938.272; A/Z_f = 20/6) | **60.1934596388**; Lambert W₋₁ and bisection agree to 1e-49; L − 60.194 = −5.40e-4 (relative −8.98e-6) |
| (b) m(20, 6, L = 58.006) | **758.688512012 MeV** (−19.14% from m_p) |
| (b) m(20, 6, L = 58.0526017386) | **762.151463091 MeV** (−18.77%) |
| (c) A/Z_f that makes L = 80.95 give m_p | 0.499884232289. Nearest p/q with p, q ≤ 20 is **1/2**; the next, 9/19, is 0.026 away. |
| (c) L(m_p; A/Z_f = 1/2) | **80.9473329260**, relative difference from 80.95 = −3.29e-5 (−0.0033%) |
| (d) L(m_p; A/Z_f = 70/6) | **47.6901564515** |
| (d) m(70, 6, L = 58.006) | **2655.40979204 MeV** |

### T3: mass table (MeV; DR-A3-7)
| row | recomputed | printed | rec/prt − 1 | err % (rec) | pull (rec) | err % (prt) | pull (prt) | locked rule |
|---|---|---|---|---|---|---|---|---|
| Up | 2.03914201 | 2.039 | +7.0e-5 | −5.595 | −1.73 | −5.602 | −1.73 | **NOT HOLDING** (outside [2.09, 2.23]) |
| Down | 4.58899004 | 4.589 | −2.2e-6 | −2.362 | −1.59 | −2.362 | −1.59 | **NOT HOLDING** |
| Charm | 1245.67449 | 1245.7 | −2.0e-5 | −2.147 | −5.94 | −2.145 | −5.93 | **NOT HOLDING** |
| Bottom | 4162.58573 | 4162.6 | −3.4e-6 | −0.488 | −2.92 | −0.488 | −2.91 | holds |
| Top | 171184.722 | 171185 | −1.6e-6 | −0.803 | −4.78 | −0.803 | −4.78 | holds |
| Tau (L = 3Φφ² = 49.0883534289) | 1752.42612 | 1752.4 | +1.5e-5 | −1.379 | −272.3 | −1.380 | −272.6 | holds |
| W = m₀φ²⁷ | 82127.5138 | 82128 | −5.9e-6 | +2.188 | +132.2 | +2.188 | +132.2 | reported |
| Z = m_W/√(1−φ⁻³) | 93963.9615 | 93964 | −4.1e-7 | +3.044 | +1388.0 | +3.044 | +1388.0 | reported |

No row differs from its printed value by more than 0.1%; the largest gap is 7.0e-5 (Up, a rounding effect). The verdicts are the same whether the recomputed or the printed values are used.

### T4: Alexander polynomials (DR-A3-5)
I derived a Wirtinger presentation from the closed braid (σ1σ2⁻¹)³: 6 arcs and 6 crossings. Arcs x1 and x4 belong to C1, x2 and x6 to C2, and x3 and x5 to C3. The relations are:
x4 = x2 x1 x2⁻¹, x5 = x4⁻¹ x3 x4, x6 = x5 x2 x5⁻¹, x1 = x6⁻¹ x4 x6, x3 = x1 x5 x1⁻¹, x2 = x3⁻¹ x6 x3.

| quantity | result | Σ coeff² |
|---|---|---|
| (a) Δ(t1,t2,t3), up to units | **(t1−1)(t2−1)(t3−1)**. All 36 row/column deletions agree, it is symmetric, and Δ(t1,t2,1) = 0. | n/a |
| (b) Δ(t,t,t) | (t−1)³ = t³ − 3t² + 3t − 1 | **20** |
| (c) Δ_L(t) = gcd of all 36 5×5 minors with tᵢ = t | (t−1)⁴ = t⁴ − 4t³ + 6t² − 4t + 1. The Torres relation Δ_L ≐ (t−1)Δ(t,t,t) holds. | **70** |
| Conway polynomial, by skein recursion over descending diagrams | ∇ = z⁴, so ∇(t^½ − t^−½) ≐ (t−1)⁴ | 70 |
| reduced Burau | (1−t)/(1−t³) · det(I − ψ(β)) ≐ (t−1)⁴ | 70 |

The same code reproduces known links: unknot 1; trefoil t²−t+1 (∇ = 1+z²); figure-eight t²−3t+1 (∇ = 1−z²); Hopf link 1 (∇ = z); T(2,4) 1+t1t2 (∇ = z³+2z); Whitehead link (t1−1)(t2−1) (∇ = z³).

## What the locked rules give with these numbers
- **DR-A3-1.** 58.0526 is within 0.2% of 58.05, so 58.05 and 58.006 are lengths per tube radius. The prereg quotes Paper VII E.1.1 as L/R, so the result is **UNITS MATCH**.
- **DR-A3-2.**
  - U = min(58.006, 58.0526) = 58.006, which is below 59.894. Verification (1) therefore **FAILS** and the entry **RETRACTS to Conjecture status**. The same holds in diameters (U = 29.003).
  - Clause 2 is **not triggered as written**, because no configuration shorter than 58.005 was computed here.
- **DR-A3-3.** All three values lie above U. The shortest (G) value of the three is 58.05.
  - 60.194 is **(I)**: A/Z_f = 20/6, relative difference −9.0e-6.
  - ≈58.05 is **(G)**: the four-arc configuration, 58.0526.
  - 80.95 is **(I)**: A/Z_f = 1/2, relative difference −3.3e-5.
- **DR-A3-4.** |L − 60.194| = 5.4e-4, inside the ±0.001 window, so the calibration-output annotation applies.
- **DR-A3-5.** 20 ≠ 70, so "A = 20" should be annotated with both values. 20 is the coefficient-square sum of the diagonal Δ(t,t,t), which leaves out the Torres factor (t−1).
- **DR-A3-7.** Up, down and charm are **NOT HOLDING**, using either the recomputed or the printed values. W and Z are reported at +2.19% and +3.04%.

## Methods (where there was a choice)
- **Length:** closed form from the junction geometry, checked against Richardson-extrapolated polygons.
- **Embedding:** the thickness functional inf ρ_pt (Gonzalez–Maddocks–Schuricht–von der Mosel), exact point-to-arc distances, and an exact enumeration of doubly-critical chords.
- **Linking:** the exact polygon solid-angle formula, plus a disc-piercing count.
- **Link type:** an explicit isotopy plus Fox calculus on projections of the 3-D curves.
- **Inversion:** closed form L = ξ(−c W₋₁(−e^{−1−1/c}/c) − 1), with c = Φ ln(m/(m₀ A/Z_f))/ξ, at 50 digits; bisection as a cross-check. m(L) is monotone, so the root is unique.
- **Fox calculus:** the Wirtinger presentation is generated arc by arc in code. The Conway polynomial is computed by skein recursion and the Burau route is a third check.

## Honesty notes
1. The provenance condition in DR-A3-3 ("the ledger derives it from the mass formula") and the unit convention of Paper VII E.1.1 are taken from the prereg's own quotations. I did not read the ledger or Paper VII. I used 58.006 as quoted and did not compute it.
2. Choices I made:
   - **Lobe/waist assignment.** It is forced: with the opposite assignment the two waists cross at v = ∓0.354, and the far point sits at √7+3 instead of √7+1.
   - **Chirality.** Lobes along y for C1, with σ = (z,x,y). The other choice gives the mirror image, and every number reported here is unchanged under mirroring.
   - **"Non-local self-distance".** It depends on the cutoff, so I report three versions in T1.
   - **"Nearby rational".** I took the p/q (p, q ≤ 20) nearest to the exact value, which is 1/2.
   - **Up-quark test.** I applied the ±1σ interval [2.09, 2.23]; the up quark's error is also −5.60%.
3. Small disagreement with a quoted value: the inversion gives 60.19346, which rounds to 60.193, not 60.194. The ledger's 60.194 looks like double rounding through 60.1935. It is still inside DR-A3-4's ±0.001 window. 80.95 is the correct rounding of 80.9473. Separately, V4.40's "half the vacuum coherence length", 50φ = 80.9017, differs from 80.95 by 0.06%.
4. Outside scope: with the formula exactly as given, m(A/Z_f = 1, L = 2π) = 0.49249 MeV, not 0.511, because r_eff(2π) = 1.038. In effect, m₀ is normalised as if r_eff = 1 at the electron anchor.
5. Outside scope, from memory and not checked this session: the calculator's quark lengths 16.372, 21.04 and 23.60 are almost exactly half the published per-radius ideal ropelengths of the knots 3₁, 4₁ and 5₁ (about 32.74, 42.09 and 47.20). That points to a per-diameter convention, which bears on the DR-A3-7 lead for B3.
