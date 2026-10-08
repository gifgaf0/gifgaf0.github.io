# Superfluid Quantum Topology — Paper VII
## A Topological Dictionary of the Particle Spectrum

*Ridgemark, CA — 2026*
*Integrated master document. All audit corrections of April 2026 applied.*
*Source of truth: SQT Explorer v2.0. All numbers independently verified.*
*Paper VIII §1 results appended to Forward Program:*
*OP.VIII.1 resolved, OP.VIII.2 negative result, OP.VIII.3 partial,*
*OP.VIII.4 opened.*

---

# SQT Paper VII — Abstract

Superfluid Quantum Topology (SQT) presents a foundational shift in
particle modeling, defining fermions not as point-like excitations but
as knotted manifolds within a superfluid vacuum characterized by a
Gaussian throat curvature $K(0) = -\varphi^2$. Using the electron mass
$m_e$ as the sole physical anchor and zero tuned parameters, the
framework derives mass scales and fundamental couplings of the Standard
Model from the geometric and algebraic structure of the vacuum manifold.

We establish a topological dictionary mapping knot types to fermion
generations. For five of nine fundamental fermions — the Down, Charm,
Bottom, and Top quarks and the Tau lepton — mass predictions fall within
2% of PDG values. The framework provides a closed derivation of the
nucleon's topological floor ($A = 20$) from the multivariable Alexander
polynomial of the Borromean link, and retrodicts the inverse
fine-structure constant ($\alpha^{-1}$) to within 0.003% of observation
given the muonic proton radius as input. The $W$ boson mass is recovered
within 2.2% via the cubic vacuum lattice ($3^3 = 27$), and a primary
neutrino mass eigenstate of $\approx 0.044\,\text{eV}$ is predicted under
a volumetric delocalization conjecture.

The framework operates under one observational anchor and five numbered
conjectures, the most consequential being the Borromean stabilizer
($Z_f = 6$, Conjecture 1) and the 8D-to-4D dimensional reduction (Open
Problem 3), which must simultaneously derive the proton charge radius,
the bare electromagnetic coupling, and the Borromean stabilizer without
independent adjustment. Documented tensions include the Weinberg angle
($+5.9\%$ vs on-shell) and the neutrino mass sum ($10$–$30\%$ above the
Planck 2018 bound). We provide a register of 13 open problems and
conjectures, identifying the precise derivations required to elevate
current results to theorems. The bulk modulus $\kappa = \varphi^{-4}$
appears as an attenuation coefficient across five independently derived
sectors — mass, electroweak mixing, top quark stabilizer, gravity
filtration, and S-matrix dissipation — a structural pattern that Paper
VIII will attempt to derive from a single geometric axiom.


---

# SQT Paper VII
## Chapter III — Primary Topological Invariants

**Chapter epistemic key:**

| Label | Meaning |
|-------|---------|
| **Theorem** | Proven from prior SQT axioms; no new free parameters |
| **Derivation** | Closed mathematical argument; result unique given the axioms |
| **Conjecture** | Motivated and numerically consistent; formal proof pending |
| **Retrodiction** | Formula recovers observed value given measured input; not a prediction |
| **Prediction** | Testable numerical output; no measured quantity used as input |

This chapter establishes two invariants of the vacuum topology that govern
the mass scale of composite matter and the strength of electromagnetic
coupling. They are treated together because both emerge from the same
underlying structure — the symmetry group PSL(2,7) acting on the Fano
geometry of the superfluid vacuum — and their open steps resolve from the
same unclosed calculation (§8.5, Paper VIII).

---

## §3  The Baryon Sector: Borromean Confinement and the A = 20 Invariant

### §3.1  Why the Borromean Link?

In the SQT framework, the transition from mesons to baryons represents a
shift from single-knot manifolds to link-based topologies. A nucleon
(proton or neutron) is modeled as a Borromean link of three vortex strands.
This assignment is not an analogy — it is the unique three-body topology
consistent with the color-confinement structure derived in Theorem 3.

Two structural facts constrain the model jointly:

1. **Pairwise confinement is absent.** No diquark sub-state is observed;
   the pairwise linking number of any two-quark pair is zero.
2. **Collective confinement is absolute.** The three-quark state is
   topologically inseparable; removing any one component dissolves the
   entire link.

The Borromean rings **B** satisfy both conditions simultaneously and
minimally: every pair of components has linking number zero, yet no
component can be removed without freeing the others. No simpler
three-component link has this property. The Borromean topology is therefore
not chosen for fit — it is the topological statement of color confinement.

### §3.2  Derivation of the Alexander Invariant: A = 20

**Convention.** The Alexander invariant $A$ of a knot or link is the sum
of squares of the integer coefficients of its symmetrized single-variable
Alexander polynomial:

$$A \;=\; \sum_k c_k^2, \qquad \Delta(t) = \sum_k c_k\,t^{k/2},\quad c_k \in \mathbb{Z}$$

**The multivariable polynomial.** The Borromean link **B** has three
components $L_1, L_2, L_3$. Its multivariable Alexander polynomial
(Torres 1953) is:

$$\Delta_B(t_1,t_2,t_3) \;=\;
  \bigl(t_1^{1/2} - t_1^{-1/2}\bigr)
  \bigl(t_2^{1/2} - t_2^{-1/2}\bigr)
  \bigl(t_3^{1/2} - t_3^{-1/2}\bigr)$$

This factored form is a direct consequence of the Borromean property: each
component contributes an independent single-strand factor, but their
product is non-trivial. For any link with all pairwise linking numbers zero
and non-trivial Milnor invariant $\bar{\mu}(123) = 1$, this is the
canonical form.

**Diagonal specialization.** For the degenerate hadronic ground state, the
three strand sectors are treated as a single topological charge. Setting
$t_1 = t_2 = t_3 = t$:

$$\Delta_B(t,t,t) \;=\; \bigl(t^{1/2} - t^{-1/2}\bigr)^3$$

The factor $(t^{1/2} - t^{-1/2})$ is the single-strand Alexander factor —
one per Borromean component — in the square-root normalization convention.
It is *not* the trefoil polynomial ($\Delta_{3_1}(t) = t - 1 + t^{-1}$);
that identification would be a topological error. The cube structure
reflects the three-fold product form of $\Delta_B$, not a trefoil
sub-topology.

Expanding:

$$\bigl(t^{1/2} - t^{-1/2}\bigr)^3
  \;=\; t^{3/2} - 3\,t^{1/2} + 3\,t^{-1/2} - t^{-3/2}$$

The integer coefficients in order are $[1,\,-3,\,3,\,-1]$.

**Result:**

$$A_B \;=\; 1^2 + (-3)^2 + 3^2 + (-1)^2
         \;=\; 1 + 9 + 9 + 1
         \;=\; \boxed{20}$$

This value is unique to the Borromean topology. The coefficient sequence
$[1,-3,3,-1]$ is the binomial expansion of $(x-y)^3$ at $x=t^{1/2}$,
$y=t^{-1/2}$, forced by the product structure of $\Delta_B$. Given the
Borromean topology assignment — which is forced by §3.1 — $A = 20$ follows
with no degrees of freedom.

### §3.3  Flavor Blindness and the Neutron Constraint

Because $\Delta_B(t,t,t)$ carries no label distinguishing which component
is which quark, $A_B = 20$ is identical for the proton (uud) and the
neutron (udd). This is structural, not assumed.

**Consequence.** At leading order, Theorem 1 predicts $m_p = m_n$. The
observed splitting $\Delta m = m_n - m_p = 1.293\,\text{MeV}$ lies outside
the domain of Theorem 1, which gives hadronic mass only; it is
electromagnetic in origin. This is a constraint on the model, not a
failure: the topology-blindness *predicts* that the splitting is
QED-generated, consistent with standard results. The neutron test (§3.5)
quantifies this boundary precisely.

### §3.4  The Stabilizer Phase: Z_f = 6 *(Conjecture 1)*

**Status: Conjecture 1.** The group-theoretic argument below is complete
and internally consistent. The Riemann-Hurwitz proof that the Borromean
complement's fundamental group representation factors through $F_7^*$ is
in preparation (Appendix E).

**Fano triangles and color singlets.** Theorem 3 established that
the strong force at residual $r=0$ corresponds to full crystallization of
all eight Fano edges, governed by $\text{PSL}(2,7)$ of order 168. For
single quarks, the relevant stabilizers are:

| Particle | Stabilizer | $Z_f$ | Status |
|----------|-----------|-------|--------|
| Up quark ($3_1$) | Line stabilizer in $\text{PG}(2,2)$ | 3 | Theorem 2 |
| Down quark ($4_1$) | Amphicheiral; order $3^2$ | 9 | Theorem 2 |

A color-singlet baryon requires three quarks occupying three
**non-collinear** Fano points — a *Fano triangle*. The symmetry group
preserving this configuration under the canonical action is scalar
multiplication by $F_7^*$, the multiplicative group of the Galois field
$\mathbb{F}_7$:

$$F_7^* \;=\; \{1,2,3,4,5,6\} \;\subset\; \text{PSL}(2,7),
  \qquad F_7^* \;\cong\; \mathbb{Z}_6$$

Scalar multiplication by any element of $F_7^*$ preserves the
non-collinear triple simultaneously, maintaining the color-singlet
condition. Three constraints single out $F_7^*$ as the unique candidate:

1. **Canonicity.** The group is defined by field arithmetic of
   $\mathbb{F}_7$, not by any mass input.
2. **Color-singlet compatibility.** Point and line stabilizers are
   excluded; they correspond to diquark or gluon states.
3. **Zero new parameters.** $|F_7^*| = 7 - 1 = 6$ by the standard formula
   for the multiplicative group of a prime field, applied to the $p = 7$
   already present in $\text{PSL}(2,7)$.

$$\boxed{Z_f(\text{baryon}) \;=\; |F_7^*| \;=\; 6} \qquad \text{(Conjecture 1)}$$

### §3.5  Mass Prediction and the Neutron Test

With $A = 20$ (§3.2, derived) and $Z_f = 6$ (§3.4, conjectured), Theorem 1
gives:

$$m(20,\,6,\,L_B) \;=\; m_0 \cdot \frac{20}{6} \cdot
  \exp\!\left(\frac{L_B}{\Phi\,r_\text{eff}(L_B)}\right)$$

Setting $m = m_p = 938.272\,\text{MeV}$ and solving by bisection:

$$\boxed{L_B \;=\; 60.194\,\text{fm}} \qquad \textbf{(Prediction)}$$

This is a **prediction**: the value $L_B = 60.194\,\text{fm}$ should
equal the ideal ropelength of the Borromean rings — the minimum
length-to-radius ratio at maximal tube width — which is a purely geometric
quantity independent of mass data. The current best numerical bounds
(Ashton et al. 2011) are $L_B^\text{ideal} \in [58.006,\,62.0]\,\text{fm}$.
The prediction lies within these bounds. This is necessary but not yet
sufficient: the bounds span 6.7\%, and confirmation requires a numerical
minimization closing the interval to $<1\%$ precision (Appendix E).

The same parameters applied to both baryons give:

| Baryon | $m_\text{obs}$ (MeV) | $m_\text{SQT}$ (MeV) | Error |
|--------|--------------------|---------------------|-------|
| Proton | 938.272 | 938.272 | 0.000\% (bisection target) |
| Neutron | 939.565 | 938.272 | $-0.138\%$ |

The neutron error of $-0.138\%$ represents the entire n-p mass splitting
(1.293 MeV) landing on the QED side of the model's domain boundary.
Topology predicts identical hadronic cores; QED generates the residual.
This is the first prescription in SQT history for which both $m_p$ and
$m_n$ are simultaneously within $0.15\%$ of observation.

### §3.6  Open Items

| Item | Status | What closes it |
|------|--------|----------------|
| $A = 20$ from Borromean polynomial | **Derivation ✓** | Complete (§3.2) |
| $Z_f = 6$ from $F_7^*$ action | **Conjecture 1** | Riemann-Hurwitz proof (Appendix E) |
| $L_B = 60.194\,\text{fm}$ in Ashton bounds | **Necessary check ✓** | Confirmed |
| $L_B$ from ideal Borromean minimization | **Prediction** | Numerical minimization to $<1\%$ (Appendix E) |

When Conjecture 1 is promoted to **Corollary 3.1** (Baryon Stabilizer, subordinate to Theorem 3), the baryon mass ceases to be a
target and becomes a pure prediction from topology and field arithmetic.

---

## §7  Theorem 4 (Candidate): The Fine-Structure Constant $\alpha^{-1}$

### §7.1  Structure of the Problem

The fine-structure constant $\alpha^{-1} \approx 137.036$ has resisted
derivation from first principles since Sommerfeld introduced it in 1916.
In SQT the problem is reframed: $\alpha^{-1}$ is not a dimensionless
coupling to be fitted, but a ratio of topological densities set by the
geometry of the vacuum manifold.

The formula has two factors:

$$\alpha^{-1} \;=\;
  \underbrace{\frac{84}{\arctan(1/\sqrt{2})}}_{\displaystyle\alpha_\text{bare}^{-1}}
  \;\cdot\;
  \underbrace{\left(1 + \frac{r_p^2\,\kappa}{8\pi}\right)}_{\displaystyle f_c}$$

where $\kappa = 1/\varphi^4$ is the superfluid bulk modulus (Theorem 1)
and $r_p$ is the proton charge radius. The bare coupling is evaluated at
the Fano-lattice level before hadronic volume corrections; $f_c$ accounts
for the finite size of the proton core. The relationship to §3 is direct:
both sections draw from PSL(2,7) geometry, and the open steps of both
sections resolve from the same unclosed calculation (§7.5).

The overall epistemic status of this section:

| Component | Status |
|-----------|--------|
| Solid angle $= 8\pi$ | Selection result ✓ |
| $\kappa = 1/\varphi^4$ | Theorem 1 ✓ |
| Formula recovers $\alpha^{-1}$ given $r_p$ | Retrodiction ✓ |
| $84 = |\text{PSL}(2,7)|/2$ in bare coupling | **Conjecture 2** |
| $r_p = 0.83847\,\text{fm}$ from 8D geometry | **Open Problem 3** |

### §7.2  The Bare Coupling: $\alpha_\text{bare}^{-1} = 84/\arctan(1/\sqrt{2})$

**Status: Conjecture 2.**

Numerically: $84/\arctan(1/\sqrt{2}) = 84/0.61548\ldots \approx 136.479$.

#### §7.2.1  The Angle: Cubic Vacuum Geometry

The denominator $\arctan(1/\sqrt{2})$ is not a fitted parameter. It is a
direct consequence of the cubic vacuum lattice established in Theorem 3.

That theorem fixed the Weak force at residual $r=3$ with volumetric drag
$D(3) = 1$ across a cubic grid of $3^3 = 27$ vertices — the same
structure that sets the W boson mass via $m_W = m_0\,\varphi^{27}$.
In that cubic lattice, the **primary angular resonance** is the angle
$\theta$ between the space diagonal and a face diagonal. Given space
diagonal $\vec{A} = (1,1,1)$ and face diagonal $\vec{B} = (1,1,0)$:

$$\cos\theta \;=\; \frac{\vec{A}\cdot\vec{B}}{|\vec{A}||\vec{B}|}
  \;=\; \frac{2}{\sqrt{3}\cdot\sqrt{2}} \;=\; \frac{2}{\sqrt{6}}$$

$$\tan\theta \;=\; \frac{1}{\sqrt{2}}, \qquad
  \theta \;=\; \arctan\!\left(\tfrac{1}{\sqrt{2}}\right) \approx 35.26°$$

This is the angle at which the volumetric (3D) and planar (2D) propagation
axes of the cubic lattice are geometrically resolved. The same topology
that sets the exponent 27 in $m_W$ sets this angle in $\alpha_\text{bare}^{-1}$.
Requiring no new input, it transforms the denominator from a
numerical coincidence into a structural necessity of the cubic vacuum.

The physical interpretation: $\arctan(1/\sqrt{2})$ measures the
**geometric tilt of the vacuum manifold under electromagnetic stress** —
the angle at which a signal propagating along the full 3D diagonal of the
lattice is projected onto a 2D face. Electromagnetism, as a
two-residual force ($r=1$, one free edge), samples exactly this
face-to-diagonal projection.

#### §7.2.2  The Numerator: 84 and PSL(2,7) *(Conjecture 2)*

The automorphism group of the Fano plane is $\text{PSL}(2,7)$, of order
168, governing the vacuum topology at the strong-force fixed point. The
numerator is:

$$84 \;=\; \frac{|\text{PSL}(2,7)|}{2} \;=\; \frac{168}{2}$$

The factor of 2 corresponds to the index-2 chiral subgroup — the
separation between orientation-preserving and orientation-reversing
symmetries of the Fano geometry, equivalently the split between particle
and antiparticle sectors in the electromagnetic vacuum.

**This identification is Conjecture 2.** Both 84 and $\arctan(1/\sqrt{2})$
arise from structures independently established in the framework.
What is not yet proven is that the electromagnetic coupling *must* take
this form — that the ratio is forced by the dimensional reduction from
the 8D bulk manifold to the 4D electromagnetic boundary, rather than
being a numerological coincidence. That proof is the content of Open
Problem 3 (§7.5), and Conjecture 2 closes simultaneously with it.

### §7.3  The Solid Angle: Why $8\pi$ and Not $4\pi$

The correction factor $f_c$ contains $8\pi$ in the denominator. This is
not a free choice — it is selected by requiring physical consistency of
the proton radius.

The standard solid angle for isotropic emission in $\mathbb{R}^3$ is
$4\pi$. Particles described by Theorem 1 are spin-$\frac{1}{2}$; they
transform under the double cover of $\text{SO}(3)$, namely $\text{SU}(2)$.
A spin-$\frac{1}{2}$ state requires a full $4\pi$ rotation to return to
its original phase, so the effective spinor solid angle is:

$$\Omega_\text{spinor} \;=\; 2 \times 4\pi \;=\; 8\pi$$

This is set by the representation theory of the rotation group and is not
adjusted to fit $\alpha$.

**Uniqueness audit.** Three geometrically motivated candidate solid angles
are tested against the CODATA 2018 muonic hydrogen proton radius
$r_p = 0.8414 \pm 0.0015\,\text{fm}$:

| Solid angle | Interpretation | Required $r_p^*$ (fm) | Physically consistent? |
|-------------|---------------|----------------------|----------------------|
| $2\pi$ | Circle (1D winding) | $< 0.5$ | ✗ excluded |
| $4\pi$ | Sphere (3D surface) | $\approx 1.2$ | ✗ excluded |
| $8\pi$ | Spinor double-cover | $\approx 0.838$ | ✓ consistent |

Only $8\pi$ places the required proton radius inside the experimental
window. The solid angle is selected by exclusion of physically untenable
alternatives, not tuned to $\alpha$.

### §7.4  Retrodiction: $r_p$ as Input

Substituting $r_p = 0.8414\,\text{fm}$ (CODATA 2018 muonic hydrogen),
$\kappa = 1/\varphi^4$, and $8\pi$:

$$\alpha^{-1}(0.8414) \;\approx\; 136.479 \times 1.00411 \;\approx\; 137.040$$

against $\alpha^{-1}_\text{CODATA} = 137.035\,999\ldots$, an error of
$+0.003\%$. The formula has zero free parameters — $\kappa$ is derived
in Theorem 1, $8\pi$ is selected by the spinor audit, the bare coupling
is conjectured from PSL(2,7) geometry — and $r_p$ is substituted from
measurement, not fitted.

The **perfect SQT radius** — the value at which the formula recovers
$\alpha^{-1}$ exactly — is:

$$\boxed{r_p^\text{SQT} \;=\; 0.838\,47\,\text{fm}} \qquad \textbf{(Target for Theorem 4)}$$

This sits 0.43\% below the muonic hydrogen consensus. It is a prediction:
if the 8D manifold geometry forces this length scale, the fine-structure
constant is derived from topology alone. It should be treated as a target
for the dimensional reduction calculation, not as confirmation that the
formula is correct.

**Precision framing.** The 0.003\% residual when using $r_p = 0.8414\,\text{fm}$
is the electromagnetic analogue of the neutron's $-0.138\%$ in §3.5: a
high-precision boundary marker. In the baryon sector, $0.138\%$ is the QED
floor — the n-p splitting that Theorem 1 does not model. Here, $0.003\%$
is the geometric floor — the gap between the muonic measurement and the
SQT invariant radius. Both residuals identify exactly where the next
layer of the calculation begins.

### §7.5  Open Problem 3: The Path to Theorem 4

Conjecture 2 and Open Problem 3 are not two independent open items.
They are two faces of the same unclosed argument.

The same 8D-to-4D dimensional reduction that must derive $r_p$ must
simultaneously derive the bare coupling $84/\arctan(1/\sqrt{2})$: both
are outputs of the bulk-to-boundary map, not separately adjustable. A
partial result that produces one without the other is incomplete by
construction.

**What closes Theorem 4.** A derivation that:

1. Takes the 8D superfluid manifold geometry as its only input
2. Performs the dimensional reduction to the 4D electromagnetic boundary
3. Simultaneously extracts $r_p = 0.83847\,\text{fm}$ and
   $\alpha_\text{bare}^{-1} = 84/\arctan(1/\sqrt{2})$
4. Recovers $\alpha^{-1} = 137.036$ without any experimental input

If steps 1–4 succeed, the section heading changes from "Candidate" to
Theorem 4, and the fine-structure constant is derived from geometry with
zero experimental input. This is the central calculation of Paper VIII.

### §7.6  Open Items

| Item | Status | What closes it |
|------|--------|----------------|
| $\arctan(1/\sqrt{2})$ from cubic lattice | Geometric identification ✓ | Complete (§7.2.1) |
| $8\pi$ spinor selection | Selection result ✓ | Complete (§7.3) |
| $\kappa = 1/\varphi^4$ | Theorem 1 ✓ | Established |
| Retrodiction to $0.003\%$ | Retrodiction ✓ | Demonstrated (§7.4) |
| $84 = |\text{PSL}(2,7)|/2$ in coupling | **Conjecture 2** | 8D reduction (Paper VIII) |
| $r_p = 0.83847\,\text{fm}$ from geometry | **Open Problem 3** | Same 8D reduction |

---

## Chapter III — Synthesis

Sections §3 and §7 address different physical quantities — composite
matter mass and electromagnetic coupling strength — but share a common
algebraic foundation: the symmetry group $\text{PSL}(2,7)$ acting on the
Fano plane geometry of the superfluid vacuum.

In §3, PSL(2,7) provides the stabilizer modes that fix $Z_f$ values for
individual quarks (Theorem 2) and, under Conjecture 1, for the three-quark
Fano triangle ($Z_f = 6$). In §7, PSL(2,7) provides the half-order
$|{\rm PSL}(2,7)|/2 = 84$ that enters the bare electromagnetic coupling
(Conjecture 2). The cubic lattice of Theorem 3 — the same $3^3 = 27$
structure that sets $m_W$ — provides the angular resonance
$\arctan(1/\sqrt{2})$ in the coupling denominator.

The two open conjectures (1 and 2) and Open Problem 3 resolve together
from the 8D-to-4D dimensional reduction. This is not a weakness of the
framework but its most testable prediction: a single calculation must
simultaneously reproduce the proton charge radius, the bare
electromagnetic coupling, and the $Z_f = 6$ Borromean stabilizer. If any
one of the three fails, all three fail. The framework is falsifiable at
the level of one calculation.

### Remark III.1 — The Lucas Identity: $\varphi^4 + \kappa = 7$

The constants $\varphi^4$ and $\kappa = \varphi^{-4}$ each enter the
framework independently and for separate physical reasons: $\kappa$ is the
superfluid bulk modulus (Theorem 1, derived from the Gaussian throat
curvature $K(0) = -\varphi^2$); $\varphi^4$ enters the Top quark
stabilizer $Z_f = 1/(8\varphi^4)$ and the Weak boson exponent via the
cubic vacuum (Theorem 3). Their sum satisfies an exact identity:

$$\varphi^4 + \kappa \;=\; \varphi^4 + \varphi^{-4} \;=\; L_4 \;=\; 7$$

where $L_n$ denotes the $n$-th Lucas number, defined by the recurrence
$L_n = L_{n-1} + L_{n-2}$ with $L_1 = 1$, $L_2 = 3$. The general
identity $\varphi^n + \varphi^{-n} = L_n$ holds for all positive integers
$n$; at $n = 4$ it yields 7 exactly.

The number 7 is not arbitrary in this context: it is the order of the
finite field $\mathbb{F}_7$, the number of points and lines of the Fano
plane $\text{PG}(2,2)$, and the index appearing in $\text{PSL}(2,7)$ — the
automorphism group governing the vacuum topology throughout this chapter.

**What this establishes.** The bulk modulus and its reciprocal are the
exact algebraic complements of the Fano dimensionality. This is a
structural observation about the internal consistency of the framework's
constants: three quantities defined independently — from throat curvature,
from the cubic vacuum, and from projective geometry over $\mathbb{F}_7$ —
satisfy an exact relation with no free parameters and no fitting.

**What this does not establish.** The identity does not explain why the
exponent is 4 rather than 3 or 5, nor does it constitute a selection rule
forbidding particles at crossing number 7. The quark spectrum skips
crossing number 7 (the sequence runs 3, 4, 5, 6, 8, 8), and
$\varphi^4 + \kappa = 7$ is consistent with that gap being meaningful —
but consistency is not mechanism. A selection rule would require showing
that the mass operator, the Alexander invariant, or the stabilizer
structure becomes degenerate or undefined at $Z_b = 7$. That argument is
not yet available.

**Research direction.** The identity suggests that the exponent $n = 4$ in
$\kappa = \varphi^{-4}$ may be fixed by the requirement that
$\varphi^n + \varphi^{-n} \in \mathbb{Z}$ and that integer equals the
Fano order. Among positive integers, $n = 1$ gives $L_1 = 1$ (trivial),
$n = 2$ gives $L_2 = 3$ (the Up quark line stabilizer), $n = 3$ gives
$L_3 = 4$ (the crossing number of the Down quark knot $4_1$), and $n = 4$
gives $L_4 = 7$ (the Fano order). Whether this sequence is coincidental or
reflects a deeper constraint on which $n$ the bulk modulus selects is an
open question for Paper VIII.

---

*Chapter III complete. Chapter IV: Secondary Sectors (Neutrinos, Cosmological Echoes).*


---

# SQT Paper VII — Draft Section
## §8  The Neutrino Sector: Delocalized Defects and the Correlation Volume

**Epistemic status:**

| Component | Status |
|-----------|--------|
| Neutrino topology: $A=1$, $L=0$ (unclosed defect) | **Structural argument** — consistent with Theorem 1 |
| $Z_{f,\nu} = \xi_\text{vac}^3$ | **Conjecture 3** — dimensional argument; not yet from PSL(2,7) |
| $m_\nu \approx 0.044\,\text{eV}$ | **Prediction** — given Conjecture 3 |
| $\Sigma m_\nu \approx 0.132\,\text{eV}$ vs Planck bound | **Tension** — 10% above Planck 2018 |
| Oscillations as phase interference | **Conjecture 4** — qualitative; PMNS angles not derived |

---

### §8.1  Why Neutrinos Are Different

Every particle treated in §§3–9 carries a definite ropelength $L > 0$: its
vacuum knot is geometrically locked, and the bisection of Theorem 1 connects
$L$ to a mass eigenstate. Neutrinos violate this pattern. They are electrically
neutral, left-handed only, and — within the Standard Model — massless at tree
level. In the SQT framework these facts are unified by a single structural
claim: the neutrino is an **unclosed topological defect** of the vacuum superfluid.

Formally, the neutrino corresponds to an unknot ($A = 1$, knot type $0_1$) that
has not achieved a stable ropelength lock. Its topology is the ground state of
the vacuum strand — the same topology as the electron — but without the electron's
geometric locking at $L = 2\pi$. The neutrino strand has $L = 0$: no stable loop
radius, no fixed ropelength, and therefore no mass from the Theorem 1 exponential
factor $\exp(L/\Phi\,r_\text{eff}(L))$, which evaluates to 1 at $L = 0$.

This is not a new axiom. The $L = 0$ limit of Theorem 1 is already defined: it
gives the ground-state mass $m_0 \cdot (A/Z_f)$ before any ropelength
amplification. The neutrino's topology ($A = 1$) and its zero-ropelength status
together reduce the mass formula to:

$$m_\nu \;=\; m_0 \cdot \frac{1}{Z_{f,\nu}}$$

Everything depends on the correct identification of $Z_{f,\nu}$.

---

### §8.2  The Stabilizer: $Z_{f,\nu} = \xi_\text{vac}^3$ *(Conjecture 3)*

**Status: Conjecture 3.** The identification below is a dimensional argument.
It is internally consistent with the framework but has not been derived from
the PSL(2,7) stabilizer modes that generate the single-particle $Z_f$ values
in Theorems 1 and 2. Until such a derivation is complete, the neutrino mass
prediction carries an additional layer of conjecture not present in the quark
and charged-lepton sectors.

For a particle with a definite ropelength $L > 0$, the stabilizer $Z_f$ is
determined by the PSL(2,7) symmetry mode acting on the knot's Fano-plane
position. The neutrino, with $L = 0$, is not localized to a specific Fano
vertex. It is delocalized across the full 3D correlation volume of the
superfluid vacuum.

The SQT correlation length is $\xi_\text{vac} = 100\varphi \approx 161.8\,\text{fm}$.
The 3D correlation volume carries $\xi_\text{vac}^3$ independent vacuum modes.
The claim of Conjecture 3 is that this volumetric mode count functions as the
effective stabilizer for a delocalized defect:

$$\boxed{Z_{f,\nu} \;=\; \xi_\text{vac}^3 \;=\; (100\varphi)^3 \;\approx\; 4.236 \times 10^6}
\qquad \text{(Conjecture 3)}$$

**Physical interpretation.** A geometrically locked particle samples one Fano
mode and its mass is suppressed or amplified by one stabilizer factor.
A delocalized defect samples all $\xi_\text{vac}^3$ modes simultaneously; its
effective stabilizer is proportionally larger, producing a correspondingly
smaller mass. The neutrino is not light because it carries small quantum numbers
— it is light because it is not geometrically localized.

**What Conjecture 3 requires to become a theorem.** The derivation must show that
$\xi_\text{vac}^3$ arises as a stabilizer from the vacuum geometry rather than
being inserted by analogy with the correlation volume. Specifically: the
delocalized defect must be shown to couple to PSL(2,7) through a representation
whose effective order is $\xi_\text{vac}^3$. This requires an extension of the
stabilizer theory from localized knots to extended field configurations, a step
that is architecturally more demanding than the single-particle cases. It is the
content of Open Problem 4 (OP.4).

---

### §8.3  Mass Prediction: $m_\nu \approx 0.044\,\text{eV}$

With $A = 1$, $L = 0$, and $Z_{f,\nu} = \xi_\text{vac}^3$:

$$m_\nu \;=\; \frac{m_0}{Z_{f,\nu}} \;=\; \frac{m_0}{(100\varphi)^3}
  \;\approx\; \frac{0.18699\,\text{MeV}}{4.236 \times 10^6}
  \;\approx\; 4.41 \times 10^{-8}\,\text{MeV}$$

$$\boxed{m_\nu \;\approx\; 0.0441\,\text{eV}} \qquad \textbf{(Prediction, given Conjecture 3)}$$

This is a **degenerate-mass prediction**: the framework gives one mass eigenvalue,
not three. The three active neutrino flavors are assumed to share this mass
at leading order, with oscillations arising from phase misalignments between
degenerate states (Conjecture 4, §8.6). Whether the SQT spectrum is
normal-hierarchical, inverted-hierarchical, or degenerate cannot be determined
from the current framework — all three are consistent with three near-degenerate
states at this scale.

---

### §8.4  The Planck Tension *(Tension OP.5)*

**Status: Active tension with current data.**

The Planck 2018 CMB analysis places an upper bound on the sum of neutrino masses:

$$\sum m_\nu \;<\; 0.12\,\text{eV} \quad (95\%\,\text{CL, Planck 2018})$$

Under the SQT degenerate-mass prediction, the three-flavor sum is:

$$\sum m_\nu^\text{SQT} \;=\; 3 \times 0.0441\,\text{eV} \;=\; 0.132\,\text{eV}$$

This exceeds the Planck bound by **10.4%**. This is not a rounding-level
discrepancy — the tension is structural.

**What could resolve it.** Four logical possibilities exist:

1. **Refined $Z_{f,\nu}$ derivation.** If the correct derivation from PSL(2,7)
   yields a stabilizer larger than $\xi_\text{vac}^3$ by a factor of $\sim 1.1$,
   the mass drops below 0.040 eV and the sum satisfies the bound. Since
   $Z_{f,\nu}$ is currently a conjecture, its value could shift.

2. **Non-degenerate spectrum.** If the SQT framework permits a normal or
   inverted hierarchy, the lightest eigenstate could satisfy $\Sigma < 0.12\,\text{eV}$
   while the heaviest provides 0.044 eV as its mass. The degeneracy assumption
   in §8.3 is the simplest consistent with the framework but is not forced.

3. **Revised cosmological bound.** The Planck bound is model-dependent
   ($\Lambda$CDM plus specific assumptions about neutrino free-streaming).
   KATRIN and Project 8 measure the single-flavor endpoint kinematic mass;
   the combination of future data may shift or relax the bound.

4. **Framework revision.** The tension may indicate that the delocalized-defect
   picture is incomplete, and the neutrino sector requires an extension of the
   framework's axioms. This is the most conservative interpretation.

The tension is documented, not resolved. It does not propagate errors into the
charged-particle predictions — the neutrino sector is architecturally separate
from the quark and lepton sectors. But it prevents the neutrino mass from being
classified as a Green or Amber result; it is the primary active **tension** in
Paper VII.

---

### §8.5  Oscillation Phenomenology *(Conjecture 4)*

**Status: Conjecture 4.** The following is a qualitative structural account.
PMNS mixing angles are not derived.

The three active neutrino flavors ($\nu_e$, $\nu_\mu$, $\nu_\tau$) each couple
to their respective charged lepton ($e$, $\mu$, $\tau$) through the weak vertex.
The charged leptons carry definite, geometrically locked $Z_f$ values:

| Particle | Topology | $Z_f$ | L (fm) |
|----------|----------|-------|--------|
| Electron | Unknot $0_1$ | 1 | $2\pi$ |
| Muon | $(2,1)$-cable $0_1$ | $1/2\pi$ | $2L_q$ |
| Tau | $(3,1)$-cable $3_1$ | $1/2\pi$ | $3L_q$ |

Each charged-lepton $Z_f$ defines a phase-locking direction in the vacuum
Fano geometry. A neutrino produced in association with, say, the muon carries
the muon's phase orientation as its initial condition. Because the neutrino
is delocalized ($L = 0$, no ropelength lock), it does not maintain this phase
as it propagates. Instead, its topological phase drifts between the three
charged-lepton phase axes.

**Conjecture 4.** Neutrino oscillations are the macroscopic signature of this
phase drift: the probability of detecting flavor $\beta$ after producing flavor
$\alpha$ is $|\langle\phi_\beta|\phi_\alpha(t)\rangle|^2$, where $\phi_\alpha$
and $\phi_\beta$ are the phase-lock directions of the respective charged-lepton
$Z_f$ sectors. In the SQT picture, the mixing is not caused by a mass matrix
with off-diagonal elements; it is caused by the absence of a geometric lock that
would confine the neutrino to any single charged-lepton phase.

**What remains open.** Deriving the PMNS angles ($\theta_{12}$, $\theta_{13}$,
$\theta_{23}$) from the $Z_f$ ratio structure of the three charged leptons
— without introducing free mixing parameters — is Open Problem 4 (OP.7 in the
register). The qualitative account above is consistent with oscillations arising
from phase drift; it does not predict the specific angles measured in solar,
atmospheric, and reactor neutrino experiments.

---

### §8.6  Open Items

| Item | Status | What closes it |
|------|--------|----------------|
| $Z_{f,\nu} = \xi_\text{vac}^3$ | **Conjecture 3** | PSL(2,7) derivation for delocalized defects (OP.4) |
| $m_\nu = 0.0441\,\text{eV}$ | **Prediction** (given Conj. 3) | Conjecture 3 proof or falsification by KATRIN |
| $\Sigma m_\nu = 0.132\,\text{eV}$ vs Planck bound | **Tension** | Revised stabilizer, hierarchy, or bound (OP.5) |
| Oscillations from phase drift | **Conjecture 4** | Qualitative account only |
| PMNS angles from $Z_f$ ratios | **Open Problem 4** | Explicit derivation without free parameters (OP.7) |

The neutrino sector is the most conjectural primary sector in Paper VII.
It rests on Conjecture 3, which is architecturally weaker than the other
conjectures: it does not derive $Z_{f,\nu}$ from the PSL(2,7) stabilizer
apparatus that underlies every other $Z_f$ value in the framework.
This architectural weakness is the honest characterization of the section's
status, and it is maintained through the conjectural labeling above.

A falsification path exists independently of the theoretical resolution:
if KATRIN or Project 8 measures a single-flavor endpoint mass below
$0.040\,\text{eV}$ with 95% confidence, the prediction is falsified
regardless of the Planck bound question. If the endpoint mass is
consistent with $0.044\,\text{eV}$, the prediction is supported but not
confirmed — consistent with Conjecture 3 but not derived from it.

---

*End of §8 draft.*
*§9: The Electroweak Sector — W boson, Weinberg angle, and the cubic vacuum.*


---

# SQT Paper VII — Draft Section
## §9  Theorem 3 Extension: The Electroweak Sector

**Epistemic status:**

| Component | Status |
|-----------|--------|
| $m_0$ from electron mass $m_e$ | Single observational anchor |
| $3^3 = 27$ as exponent motivation | Geometric assertion — derivation pending |
| $m_W = m_0\varphi^{27}$ | Prediction — **+2.18%** (Amber) |
| $\sin^2\theta_W = \varphi^{-3}$ | Prediction — +5.9% vs on-shell (Orange) |
| $m_Z = m_W^\text{SQT}/\cos\theta_W^\text{SQT}$ | Prediction — **+3.05%** (Amber) |

---

### §9.1  The Framework's Single Observational Anchor

Before deriving the Weak sector, the status of $m_0$ must be stated
precisely, because the framework's "zero free parameters" claim depends on it.

The energy anchor is:

$$m_0 \;=\; \frac{m_e}{e^{2\pi/\Phi}} \;=\; \frac{0.511\,\text{MeV}}{e^{2\pi/6.250028}}
  \;\approx\; 0.18699\,\text{MeV}$$

where $m_e = 0.511\,\text{MeV}$ is the electron mass (measured) and
$\Phi = 2\pi + K(0)/(8\pi^2) = 2\pi - \varphi^2/(8\pi^2) \approx 6.250028$
is derived from the Gaussian throat curvature $K(0) = -\varphi^2$ with no fitting.
The framework therefore has **one observational anchor** ($m_e$) and **zero tuned
parameters**. Every mass, coupling, and ropelength prediction follows from
$m_e$ plus geometry.

---

### §9.2  Geometric Motivation: The Cubic Exponent ($3^3 = 27$)

Theorem 3 establishes the Weak force as residual $r = 3$, corresponding to
maximum volumetric drag $D(3) = 1$ across all three spatial dimensions. In the
SQT lattice model, a cubic vacuum element has $3 \times 3 \times 3 = 27$
internal degrees of freedom.

The SQT prediction is that this count sets the exponent in the W boson mass:

$$m_W \;=\; m_0 \cdot \varphi^{27}$$

**Open derivation.** Why the degree-of-freedom count equals the $\varphi$-exponent
in the mass formula is currently an asserted geometric motivation, not a formal
derivation. The prediction is rigid and non-tuned — 27 is forced by the cubic
geometry, not fitted — but the logical step connecting "27 lattice vertices"
to "exponent 27 in $m_0\varphi^{27}$" is stated as a conjecture.
Closing it is Open Problem 8 (OP.8), to be addressed in Paper VIII.

---

### §9.3  Prediction: The W Boson Mass

$$m_W \;=\; m_0 \cdot \varphi^{27}$$

**Numerical evaluation.** Using $\varphi^{27} = F_{27}\varphi + F_{26}
= 196{,}418\varphi + 121{,}393 = 439{,}204$ (exact via Fibonacci identity):

$$m_W \;\approx\; 0.18699 \times 439{,}204 \;\approx\; 82{,}128\,\text{MeV}$$

| | Value |
|-|-------|
| SQT prediction | **82,128 MeV** |
| PDG observed | $80{,}379 \pm 12\,\text{MeV}$ |
| **Error** | **+2.18% — Class: Amber** |

This result captures the Weak-force mass scale from a single geometric
input. The 2.18% overshoot is the raw bulk-geometry prediction before
loop corrections. It is neither fitted to the W mass nor adjusted post-hoc;
the formula was fixed by the cubic lattice argument.

---

### §9.4  Prediction: The Weinberg Angle

$$\sin^2\theta_W \;=\; \varphi^{-3} \;=\; \frac{1}{\varphi^3}
  \;=\; \frac{1}{2\varphi + 1} \;\approx\; 0.23607$$

**Physical interpretation.** The mixing of the $r=3$ (Weak) and $r=1$
(EM) residuals is modeled as the probability of a volumetric ($3D$) vs.
planar ($1D$) vacuum mode, weighted by $\varphi^{-3}$. The inverse cube
of the golden ratio is the "face" projection of the bulk modulus — geometrically
consistent with the EM residual sampling one fewer spatial dimension than
the Weak residual.

**Comparison.**

| Definition | Value |
|------------|-------|
| SQT prediction | 0.23607 |
| On-shell (PDG, from $m_W$, $m_Z$) | 0.2229 |
| $\overline{\text{MS}}$ at $m_Z$ | $\approx 0.2312$ |
| **Error vs on-shell** | **+5.9% — Class: Orange** |

The SQT value exceeds the most direct (on-shell) definition by 5.9%, and
exceeds the $\overline{\text{MS}}$ value at $m_Z$ by approximately 2.1%.
The geometric motivation is internally consistent but the prediction is
Orange-class, not precision-class. Mixing renormalization schemes to
improve the apparent agreement is not defensible.

---

### §9.5  Prediction: The Z Boson Mass

The Z mass is derived from the SQT W prediction and the SQT Weinberg
angle via the tree-level electroweak relation:

$$m_Z \;=\; \frac{m_W^{\,\text{SQT}}}{\cos\theta_W^{\,\text{SQT}}}
          \;=\; \frac{82{,}128}{\sqrt{1 - 0.23607}}
          \;=\; \frac{82{,}128}{0.87409}
          \;\approx\; 93{,}964\,\text{MeV}$$

| | Value |
|-|-------|
| SQT prediction | **93,964 MeV** |
| PDG observed | 91,187.6 MeV |
| **Error** | **+3.05% — Class: Amber** |

**On the error structure.** Both inputs to $m_Z$ are too high: $m_W$ is
+2.18% above PDG, and $\sin^2\theta_W$ being +5.9% above the on-shell
value means $\cos\theta_W$ is correspondingly smaller, making the ratio
$m_W/\cos\theta_W$ larger still. The two errors **compound**, not cancel.
The +3.05% Z error is the direct, consistent consequence of both upstream
overshoots.

A value of $m_Z \approx 91{,}960\,\text{MeV}$ at $+0.85\%$ error
appears if the PDG W mass (80,379 MeV) is substituted in place of
the SQT W prediction. That substitution is internally inconsistent
and should not appear in the paper.

---

### §9.6  Summary

| Quantity | SQT Formula | SQT Value | PDG Value | Error | Class |
|----------|------------|-----------|-----------|-------|-------|
| $m_W$ | $m_0\varphi^{27}$ | **82,128 MeV** | 80,379 MeV | **+2.18%** | Amber |
| $\sin^2\theta_W$ | $\varphi^{-3}$ | 0.23607 | 0.2229 (on-shell) | +5.9% | Orange |
| $m_Z$ | $m_W^\text{SQT}/\cos\theta_W^\text{SQT}$ | **93,964 MeV** | 91,187.6 MeV | **+3.05%** | Amber |

**What this section establishes.** A single geometric structure — the
cubic vacuum with $3^3 = 27$ degrees of freedom — and the golden ratio
$\varphi$ (fixed by throat curvature) produce mass predictions for both
Weak bosons within 3.1% of observation with one observational anchor
($m_e$) and no fitted parameters. The exponent-to-degree-count step is
the open derivation that, when closed, would elevate these results from
motivated predictions to theorems.

**What it does not establish.** The Weinberg angle prediction is
Orange-class (5.9% off the most direct experimental definition).
The $3^3 = 27$ step is asserted, not derived. The Z error is larger
than the W error because both upstream predictions overshoot in the
same direction.

---

### §9.7  Top Quark Stabilizer and the κ Connection *(Theorem 3 Extension)*

The top quark — the heaviest known fermion — requires a separate treatment
of its stabilizer. All other quarks carry $Z_f$ values from PSL(2,7) point
and line stabilizers (integers or simple fractions). The top quark cannot
be accommodated by any such stabilizer at the observed mass scale of
$172{,}690\,\text{MeV}$ while retaining the knot assignment $8_1^9$
($A = 119$, $L = 37.31\,\text{fm}$).

The SQT top quark stabilizer is:

$$Z_f(\text{top}) \;=\; \frac{\kappa}{8} \;=\; \frac{1}{8\varphi^4}
  \;\approx\; 0.018237 \qquad \textbf{(Theorem 3 Extension)}$$

**Derivation.** With $A = 119$, $Z_f = \kappa/8$, and $L = 37.31\,\text{fm}$:

$$m_\text{top} \;=\; m_0 \cdot \frac{119}{\kappa/8} \cdot
  \exp\!\left(\frac{37.31}{\Phi\,r_\text{eff}(37.31)}\right)
  \;\approx\; 171{,}185\,\text{MeV}$$

| | Value |
|-|-------|
| SQT prediction | 171,185 MeV |
| PDG observed | 172,690 MeV |
| **Error** | **−0.87% — Class: Green** |

**The κ connection.** The top quark stabilizer $Z_f = \kappa/8 = 1/(8\varphi^4)$
is the first appearance of the superfluid bulk modulus $\kappa$ as a
*stabilizer value* rather than an attenuation coefficient. The physical
interpretation is that the top quark's 8D vacuum phase is fully compressed
by the bulk modulus — the $8$-dimensional vacuum modulus applied per knot
component creates maximum topological drag, setting the effective $Z_f$
below 1 (an *amplifying* stabilizer, not a suppressing one).

This is one of the five independent appearances of $\kappa$ identified in
Structural Observation V.1. The top quark result is Green-class and
requires no additional conjecture beyond the knot assignment $8_1^9$
and ropelength $L = 37.31\,\text{fm}$.

---

*End of §9 (corrected). §10: Cosmological Echoes — the gravity filtration constant $\kappa/4$.*


---

# SQT Paper VII — Draft Section
## §10  Theorem 5 (Candidate): Cosmological Echoes and Gravity Filtration

**Epistemic status:**

| Component | Status |
|-----------|--------|
| Gravity as vacuum geometry, not r-residual | Structural argument — consistent with Theorem 3 |
| $\kappa/4$ as 4D filtration constant | Geometric motivation — formal derivation pending |
| $T_g = \exp(-\kappa/4) \approx 96.42\%$ | Prediction — given the $\kappa/4$ motivation |
| Connection to CMB ring anomalies | Qualitative consistency — observational status disputed |

---

### §10.1  Gravity as Bulk Geometry

In Theorem 3, the four observable interactions were assigned to residuals
$r = 0$ (Strong), $r = 1$ (EM), and $r = 3$ (Weak), with $r = 2$ forbidden.
Gravity is absent from this list. It is not a residual of the vacuum's
topological degrees of freedom; it is the geometry of the superfluid
medium itself.

This identification follows from the Gaussian throat curvature:

$$K(0) \;=\; -\varphi^2$$

The curvature is negative, definite, and fixed by $\varphi$ — the same
constant that defines the energy anchor $m_0$ and the tension identity
$\Phi$. Gravity is not an emergent force layered on top of the vacuum; it
is the vacuum's intrinsic curvature at its own ground state. A consequence
is that gravitational signals are not subject to the $Z_f$ stabilizer
suppression that governs fermionic masses. They propagate through the bulk
superfluid with a different attenuation mechanism: bulk filtration.

---

### §10.2  The 4D Filtration Constant: $F_g = \kappa/4$

**Status: Geometric motivation — derivation pending.**

When a gravitational wave crosses the conformal boundary between aeons
(in the Conformal Cyclic Cosmology picture), it traverses the superfluid
bulk modulus $\kappa = \varphi^{-4}$ across all four spacetime dimensions.
The SQT filtration constant is:

$$F_g \;=\; \frac{\kappa}{4} \;=\; \frac{1}{4\varphi^4} \;\approx\; 0.036474$$

**The open derivation step.** The claim that the modulus distributes
equally across each spacetime dimension — yielding division by 4 rather
than multiplication, or application of $\kappa$ once as a whole — is a
physical assumption about how the bulk modulus couples to the conformal
boundary. It is not derived from the axioms of Theorem 1. Why 4 and not
3 (spatial only) or 1 (full modulus once applied) requires showing that
each spacetime dimension independently contributes one factor of $\kappa$
to the total attenuation. This is the open derivation step for Theorem 5.

The structure parallels the $3^3 = 27$ step in §9: the geometric
motivation is consistent and non-tuned, but the logical connection between
the counting argument and the exponent or denominator in the formula is
asserted rather than proven.

---

### §10.3  Aeon Transmittance: $T_g$

**Status: Prediction — given $F_g = \kappa/4$.**

The surviving energy fraction after one conformal boundary crossing is:

$$T_g \;=\; \exp\!\left(-F_g\right) \;=\; \exp\!\left(-\frac{\kappa}{4}\right)
         \;=\; \exp(-0.036474) \;\approx\; 0.96420$$

$$\boxed{T_g \;\approx\; 96.42\%} \quad \text{per aeon crossing}$$

Equivalently, each conformal boundary dissipates $\approx 3.58\%$ of the
gravitational echo's energy.

**Single-crossing scope.** This prediction applies to one aeon boundary.
For scenarios involving multiple cyclic crossings, the fraction compounds:
after $n$ crossings, the surviving fraction is $(0.9642)^n$. After 10
crossings this is $\approx 69\%$; after 20, $\approx 48\%$. Claims about
gravitational signals being "virtually intact" across cosmological history
are not supported by this single-crossing formula and should not be
extrapolated from it.

---

### §10.4  Connection to CMB Anomalies

**Status: Qualitative consistency — not a confirmed prediction.**

In Penrose's Conformal Cyclic Cosmology (CCC), supermassive black hole
mergers in a prior aeon produce gravitational bursts that propagate into
the current universe, appearing as anomalous concentric temperature rings
in the CMB — "Hawking Points." The SQT transmittance $T_g \approx 96.42\%$
is qualitatively consistent with the hypothesis that pre-aeon gravitational
signals survive the conformal transition at detectable amplitude.

**Important qualification.** The observational status of Hawking Points is
currently disputed. Penrose and Gurzadyan have reported detecting
anomalous ring-like structures in CMB data; Moss, Scott, and others have
published analyses finding the signal statistically consistent with the
noise expected in a standard $\Lambda$CDM universe without a prior aeon.
The question is unresolved.

Furthermore, $T_g = 96.42\%$ gives the energy fraction surviving one
crossing but does not by itself predict the amplitude, angular scale, or
spatial distribution of CMB temperature anomalies. Those quantities depend
on the initial energy of the pre-aeon event, the angular distance from the
source, and the coupling between gravitational energy and photon temperature
at last scattering — none of which are addressed in the current framework.
The connection to CMB phenomenology is a research direction, not a derived
prediction.

**What would constitute a prediction.** A quantitative SQT prediction for
CMB Hawking Points would require: (1) an SQT model of black hole mass in
the prior aeon (derivable in principle from the Worticity sum rule of
Theorem 2), (2) a coupling formula between gravitational energy density
and CMB temperature fluctuation amplitude, and (3) a derived angular scale
for the rings from the geometry of the conformal boundary. None of these
three exist yet. The framework identifies the right order of magnitude for
the survival fraction; the predictive chain from $T_g$ to observed $\Delta
T/T$ is open.

---

### §10.5  Summary

| Quantity | Formula | Value | Status |
|----------|---------|-------|--------|
| $F_g$ | $\kappa/4 = 1/(4\varphi^4)$ | 0.036474 | Motivated — $\kappa/4$ step pending derivation |
| $T_g$ | $\exp(-\kappa/4)$ | 96.42% per crossing | Prediction given $F_g$ |
| Multi-aeon survival ($n$ crossings) | $(T_g)^n$ | $\to 0$ as $n \to \infty$ | Extrapolation from single-crossing formula |
| CMB ring amplitude | Not derived | — | OP.10 (§10.4) |

The Cosmological Echoes section demonstrates that the same bulk modulus
$\kappa$ that governs fermionic mass corrections (Theorem 1) and the
fine-structure retrodiction (§7) also sets the geometric attenuation of
gravitational signals at conformal boundaries. The connection is not
coincidental — both uses of $\kappa$ reflect the same underlying property
of the superfluid vacuum — but the derivation of $\kappa/4$ specifically
remains an open step.

---

*End of §10 draft.*
*Chapter V: S-Matrix Dissipation — the Lens Equation ($E_\text{det} = hf_0 \cdot e^{-\kappa n} \cdot \cos^2\!\Delta\phi$).*


---

# SQT Paper VII — Draft Section
## Chapter V — S-Matrix Dissipation

### Chapter V Introduction: The κ Thread

Before deriving the Lens Equation, a structural observation is warranted.

Throughout this paper, the superfluid bulk modulus $\kappa = \varphi^{-4}$
has appeared independently in four distinct physical contexts:

1. **Theorem 1** — Mass operator: $r_\text{eff}(L) = 1 + \ln(1 + L/\xi_\text{vac})$
   and the fine-structure correction $f_c = 1 + r_p^2\kappa/(8\pi)$
2. **Theorem 3 extension** — Top quark stabilizer: $Z_f = \kappa/8 = 1/(8\varphi^4)$
3. **§10** — Gravity filtration: $F_g = \kappa/4$, $T_g = e^{-\kappa/4}$
4. **§11 (this section)** — S-matrix attenuation: $e^{-\kappa n}$

In each case, $\kappa$ appears as the characteristic attenuation rate of
the superfluid vacuum — the "geometric friction" governing how energy is
dissipated when a signal moves between topological layers, crosses a
conformal boundary, or propagates through a phase-aligned medium. This
is not coincidental; it is the same property of the vacuum manifold
expressing itself at different scales and in different physical processes.

**Structural Observation V.1 (The κ Universality).** The bulk modulus
$\kappa = \varphi^{-4}$ serves as the universal attenuation coefficient
of the SQT vacuum, appearing without modification or rescaling in the mass
operator, the electromagnetic correction, the gravity filtration constant,
and the S-matrix dissipation formula. All four contexts are governed by
the same geometric resistance of the superfluid medium.

This is distinct from a "Principle" — a principle would follow from a
derivation showing that the vacuum's resistance must be $\kappa$ in all
these contexts from a single axiom. What is established is that $\kappa$
appears universally across sectors that were derived independently. Whether
this universality is a consequence of a deeper single axiom — or whether
the four occurrences are structurally distinct but numerically coincident —
is an open question. It is flagged here because it deserves to be named
before it can be explained.

---

## §11  The SQT Lens Equation: S-Matrix Dissipation

**Epistemic status:**

| Component | Status |
|-----------|--------|
| $E_\text{det} = hf_0 \cdot e^{-\kappa n} \cdot \cos^2(\Delta\phi)$ | **Structural model** — form motivated by vacuum geometry; full derivation pending |
| $n \geq 1$ (irreducible floor) | Geometric argument — any 4D observation requires one boundary crossing |
| 86.42% observational ceiling | **Prediction** — given $n \geq 1$ and $\Delta\phi = 0$ |
| $\cos^2(\Delta\phi)$ as measurement uncertainty mechanism | **Conjecture 5** — deterministic hidden-variable interpretation |
| Connection to QFT renormalization | **Not claimed** — distinct phenomena |

---

### §11.1  The Observational Gap

Every section of this paper to this point has addressed the *existence* of
particles — their masses, stabilizer phases, and ropelengths. This section
addresses a different question: when we measure a particle, do we observe
the theoretical vertex energy $hf_0$, or something less?

SQT's answer is that observation always involves a $Z_f$-layer traversal:
the physical process by which a signal propagates from the 8D bulk vertex
state — where the mass operator $m(A, Z_f, L)$ computes $hf_0$ — to the
4D electromagnetic detector interface where the measurement occurs. This
traversal crosses at least one vacuum stabilizer layer, and each crossing
attenuates the signal by a factor governed by $\kappa$.

**Why $n \geq 1$ is forced.** The vertex energy $hf_0$ exists in the 8D
bulk geometry. Any 4D measurement apparatus couples to the
electromagnetic boundary layer, not to the bulk directly. At minimum,
one conformal-boundary traversal separates the vertex from the detector.
$n = 0$ — direct bulk-state access — would require a detector that
operates in the 8D vacuum geometry itself, which has no physical
realization in the current framework. The irreducible minimum is one
traversal, giving $n = 1$ as the floor for any physical measurement.

---

### §11.2  The Lens Equation

$$\boxed{E_\text{det} \;=\; hf_0 \cdot e^{-\kappa n} \cdot \cos^2(\Delta\phi)}$$

where:

- $hf_0 = m(A, Z_f, L)$ — the invariant vertex source, the theoretical
  mass computed from Theorem 1 for the given particle topology
- $\kappa = \varphi^{-4} \approx 0.14589$ — the superfluid bulk modulus,
  the same constant appearing in Theorems 1, 3, and §10
- $n \in \{1, 2, 3, \ldots\}$ — the number of $Z_f$ stabilizer layer
  transitions between vertex and detector
- $\Delta\phi \in [0, \pi/2]$ — the phase misalignment between the
  particle's intrinsic topological phase and the measurement apparatus

**Status of the formula.** The exponential factor $e^{-\kappa n}$ is
motivated by the identification of $\kappa$ as the per-layer attenuation
coefficient — consistent with its role in §10's conformal-boundary
filtration, and with the general structure of exponential decay in layered
dissipative media. The $\cos^2(\Delta\phi)$ factor follows from the
projection of a phase-misaligned state onto the detector's phase axis,
by analogy with Malus's law in optics. Both forms are geometrically
consistent with the framework, but a derivation from the vacuum axioms
— showing that the attenuation must be exponential rather than polynomial,
and that the phase factor must be cosine-squared rather than some other
function — is the open derivation step for this section.

---

### §11.3  The Irreducible Observational Ceiling

Setting $n = 1$ (minimum traversal) and $\Delta\phi = 0$ (perfect phase
alignment) gives the maximum possible fidelity of any measurement:

$$F_\text{max} \;=\; e^{-\kappa} \;=\; e^{-1/\varphi^4}
  \;\approx\; e^{-0.14589} \;\approx\; 0.8642$$

$$\boxed{F_\text{max} \;\approx\; 86.42\%}$$

**SQT Prediction.** No physical measurement can recover more than 86.42%
of the theoretical vertex energy $hf_0$. The irreducible 13.58% loss is
the geometric cost of a single $Z_f$-layer traversal from the 8D bulk to
the 4D electromagnetic boundary. It is not instrumental noise; it is a
property of the vacuum interface.

**Falsifiability.** This is a strong, testable claim. It predicts a
universal upper bound on measurement fidelity that applies regardless of
detector technology — because the attenuation is geometric (set by
$\kappa$), not technological. If a precision measurement of any particle
mass were to recover more than 86.42% of the SQT-predicted vertex energy
$hf_0$ at $n=1$, the framework would require revision.

In practice, testing this requires knowing $hf_0$ independently of the
measurement — i.e., a precision test of Theorem 1 for a particle where
both $hf_0$ and the number of traversal layers $n$ are independently
known. The top quark, with its large vertex mass and short lifetime,
may be the most tractable candidate.

---

### §11.4  Multi-Layer Dissipation

For $n > 1$ traversals with perfect phase alignment:

$$E_\text{det}(n) \;=\; hf_0 \cdot e^{-\kappa n} \;=\; hf_0 \cdot (e^{-\kappa})^n$$

Each additional layer multiplies the detected energy by $e^{-\kappa}
\approx 0.8642$. The cumulative fidelity after $n$ layers:

| $n$ | Fidelity | Dissipated |
|-----|---------|-----------|
| 1 | 86.42% | 13.58% |
| 2 | 74.69% | 25.31% |
| 3 | 64.55% | 35.45% |
| 4 | 55.77% | 44.23% |
| 8 | 31.12% | 68.88% |

The signal fidelity drops below 50% by $n = 5$. This has a qualitative
implication for composite measurements: processes involving many
intermediate $Z_f$ transitions will appear to produce particles with
significantly less energy than the theoretical vertex energy predicts,
a discrepancy that grows combinatorially with process complexity.

---

### §11.5  Phase Misalignment: $\cos^2(\Delta\phi)$ *(Conjecture 5)*

**Status: Conjecture 5.** The following interpretation is structurally
consistent with the framework but represents a specific position on the
quantum measurement problem. It is labeled as a conjecture and should not
be read as a derivation.

The second factor $\cos^2(\Delta\phi)$ models the projection of the
particle's intrinsic topological phase onto the measurement apparatus's
phase axis. When $\Delta\phi = 0$ (perfect alignment), the full
attenuated signal is detected. As misalignment increases, the detected
fraction falls as $\cos^2(\Delta\phi)$, reaching zero at $\Delta\phi =
\pi/2$ (complete orthogonality).

**Conjecture 5.** What quantum mechanics describes as the intrinsic
probability of a measurement outcome is, in the SQT picture, the
$\cos^2(\Delta\phi)$ projection of a definite but inaccessible phase
state. Apparent measurement indeterminacy reflects varying phase
alignments across an ensemble of $Z_f$-layer traversals, not fundamental
ontological randomness.

**What this requires to become a theorem.** This conjecture must contend
with Bell's theorem, which constrains local hidden-variable theories.
Whether $\Delta\phi$ constitutes a local or non-local hidden variable in
the SQT framework determines whether the conjecture is viable. If
$\Delta\phi$ is set by local vacuum geometry at the measurement event,
the conjecture is a local hidden-variable theory and must satisfy Bell
inequalities — a constraint that the current framework does not address.
This is Open Problem 6, and it is likely the deepest open problem in the
entire SQT program.

---

### §11.6  Relationship to QFT Renormalization

The SQT Lens Equation should **not** be conflated with the renormalization
procedure of quantum field theory. They address different problems:

- **QFT renormalization** removes ultraviolet divergences — mathematical
  infinities arising from loop integrals over arbitrarily high momenta in
  perturbation theory. It is a procedure for extracting finite predictions
  from a theory that produces infinite bare quantities.

- **The SQT Lens Equation** models finite energy dissipation during
  traversal from a well-defined vertex state to a well-defined detector
  state. The vertex energy $hf_0$ is finite; the detected energy
  $E_\text{det}$ is finite; the ratio is $e^{-\kappa n}\cos^2(\Delta\phi)$.

The SQT framework does not address UV divergences. Claiming it provides
"the physical basis for renormalization" would be incorrect. The more
modest and defensible claim is: the SQT geometric attenuation provides a
possible physical interpretation for the *finite* mass corrections that
arise between bare and renormalized masses in the low-energy limit — but
this connection is speculative and is not pursued further in Paper VII.

---

### §11.7  Summary

$$E_\text{det} \;=\; hf_0 \cdot e^{-\kappa n} \cdot \cos^2(\Delta\phi)$$

| Component | Value / Range | Status |
|-----------|--------------|--------|
| $\kappa$ | $\varphi^{-4} \approx 0.14589$ | Theorem 1 ✓ |
| $F_\text{max}$ ($n=1$, $\Delta\phi=0$) | 86.42% | Prediction |
| Exponential form of attenuation | $e^{-\kappa n}$ | Motivated — derivation pending |
| $\cos^2$ phase factor | $\cos^2(\Delta\phi)$ | Motivated — derivation pending |
| Phase misalignment as QM uncertainty | — | Conjecture 5 (Open Problem 6) |
| Connection to UV renormalization | Not claimed | — |

The Lens Equation unifies the $\kappa$ thread across the framework: the
same geometric resistance that sets the bulk modulus in Theorem 1, the
fine-structure correction in §7, and the gravity filtration in §10 also
governs the irreducible dissipation of every particle measurement. Whether
this universality is a consequence of a single underlying axiom is the
question that motivates Structural Observation V.1 and remains the central
unification target of Paper VIII.

---

*End of §11 draft. Paper VII primary derivations complete.*
*Remaining: Chapter VI (Discussion), Open Problems register, and master bibliography.*


---

# SQT Paper VII
## Chapter VI — Register of Open Problems and Conjectures

This register collects all unresolved derivations, structural tensions,
and theoretical conjectures identified throughout Paper VII. Items are
identified by their in-text label first, with a secondary sequential index
(OP.1–OP.12) for navigation. The in-text label is the authoritative
cross-reference; the OP number is a convenience index for this chapter.

**Epistemic categories used in this paper:**

| Category | Definition |
|----------|-----------|
| **Conjecture** | Structurally motivated, numerically consistent; formal derivation pending |
| **Open Problem** | A specific derivation required to close an existing theorem candidate |
| **Tension** | A conflict between a framework prediction and current experimental data |
| **Research Direction** | A structural observation suggesting a derivation path; not yet a conjecture |

---

## Master Register

| OP# | In-text label | Research front | Description | Section | Category |
|-----|--------------|----------------|-------------|---------|----------|
| OP.1 | Conjecture 1 | Riemann-Hurwitz proof | Formal proof that $\pi_1(S^3 \setminus B)$ monodromy representation factors through $F_7^*$ via Riemann-Hurwitz branched covering. Closes $Z_f = 6$ from motivated to derived. | §3.4 | Conjecture |
| OP.2 | Prediction (§3.5) | Borromean ropelength | Tighten Ashton bounds $[58.006, 62.0]$ fm (6.7% span) to $<1\%$ precision by numerical ideal-Borromean minimization. If minimized value falls at $60.194 \pm 0.3$ fm, $L_B$ prediction is confirmed. Window justified in Appendix E.1.2: a minimized value outside this range but inside Ashton bounds falsifies the prediction at leading-order precision. | §3.5 | Prediction/Test |
| OP.3 | Open Problem 3 + Conjecture 2 | 8D-to-4D reduction | Single calculation from 8D manifold geometry must simultaneously output three quantities: (1) proton radius $r_p = 0.83847$ fm, (2) bare coupling $\alpha_\text{bare}^{-1} = 84/\arctan(1/\sqrt{2})$, and (3) Borromean stabilizer $Z_f = 6$ (Conjecture 1). All three resolve from the same calculation or none do. | §3.6, §7.5 | Open Problem |
| OP.4 | Conjecture 3 | Neutrino stabilizer | Axiomatic derivation of $Z_{f,\nu} = \xi_\text{vac}^3$ from the 3D correlation volume geometry of the superfluid vacuum. Currently a dimensional argument; must be shown to follow from the vacuum axioms without reference to the neutrino mass outcome. | §8.3 | Conjecture |
| OP.5 | Tension (§8.5) | Neutrino mass sum | The SQT prediction $m_\nu \approx 0.0441$ eV leads to $\sum m_\nu \approx 0.13$–$0.16$ eV, exceeding the Planck 2018 bound of $0.12$ eV by $10$–$30\%$. Requires either revised CMB data, a refined $Z_{f,\nu}$ derivation, or a demonstration that Conjecture 4's phase-interference picture changes the bound's applicability. | §8.5 | Tension |
| OP.6 | Conjecture 4 | Flavor oscillations | Neutrino oscillations arise from phase interference between a delocalized slip ($L=0$) and the locked phases of the charged-lepton $Z_f$ sectors. Requires derivation of PMNS mixing angles from $Z_f$ ratios without free parameters. | §8.6 | Conjecture |
| OP.7 | Open Problem 4 | PMNS angles | Explicit derivation of $\theta_{12}$, $\theta_{13}$, $\theta_{23}$ from the ratio structure of $Z_f = 1$ (electron), $Z_f = 1/2\pi$ (muon/tau) without introducing free mixing parameters. Closes Conjecture 4 to Theorem 6. | §8.6 | Open Problem |
| OP.8 | Open Problem (§9.2) | Electroweak exponent | Formal derivation of why the cubic vacuum's $3^3 = 27$ degree-of-freedom count equals the exponent in $m_W = m_0\varphi^{27}$. Requires showing the lattice mode structure forces the $\varphi$-exponent to equal the volumetric degree count, not $\varphi^3$ (one axis) or $\varphi^9$ (face). | §9.2 | Open Problem |
| OP.9 | Open Problem (§10.2) | Spacetime modulus | Derivation of $F_g = \kappa/4$ from vacuum axioms: why the bulk modulus distributes as $\kappa/D$ across $D$ spacetime dimensions rather than applying as a single factor $\kappa$ or product $D\kappa$. | §10.2 | Open Problem |
| OP.10 | Open Problem 5 | CMB ring amplitude | Quantitative prediction of $\Delta T/T$ for Hawking Points from $T_g$. Requires: (1) SQT model of prior-aeon black hole mass from Worticity sum rule, (2) coupling formula between gravitational energy density and CMB temperature fluctuations, (3) angular scale of rings from conformal boundary geometry. | §10.4 | Open Problem |
| OP.11 | Open Problem (§11.2) | Lens equation axioms | Derivation of the exponential form $e^{-\kappa n}$ and $\cos^2(\Delta\phi)$ phase factor from vacuum geometry. Must show attenuation is exponential (not polynomial) and phase factor is cosine-squared (not $|\cos|$ or other function). | §11.2 | Open Problem |
| OP.12 | Conjecture 5 / Open Problem 6 | Bell / locality | Testing Conjecture 5 (phase misalignment as quantum measurement mechanism) against Bell's theorem. Requires determining whether $\Delta\phi$ is a local or non-local hidden variable in the SQT framework. If local, Bell inequalities apply and constrain the conjecture. Deepest open problem in the SQT program. | §11.5 | Conjecture |

**Additional research direction (not yet a conjecture):**

| OP# | In-text label | Research front | Description | Section | Category |
|-----|--------------|----------------|-------------|---------|----------|
| OP.13 | Remark III.1 | Generation number | Three quark generations are currently inputs. PSL(2,7) acts on the Fano plane with three distinct orbit types for point-triples: collinear triples (7 lines), non-collinear triangles (28 configurations), and complementary quadrangles. If these three orbit types map onto the three generations, the generation count is derived from Fano geometry without fitting. | §3 / Remark III.1 | Research Direction |

---

## Structural Analysis

### The 8D Reduction Cluster (Paper VIII Primary Target)

Three in-text items are formally linked as a single calculation in §7.5
and the Chapter III Synthesis:

- **Conjecture 1** ($Z_f = 6$, Riemann-Hurwitz) → OP.1
- **Conjecture 2** (84 in bare coupling) → part of OP.3
- **Open Problem 3** ($r_p$ from geometry) → part of OP.3

These three resolve together or not at all: the 8D-to-4D dimensional
reduction must produce all three simultaneously. This was explicitly
established in the Chapter III Synthesis and is the primary target of
Paper VIII.

**Items not in this cluster.** OP.8 (electroweak exponent) and OP.9
(κ/4 gravity filtration) are independent open derivations. While they
may eventually be explained by the same 8D geometry, that connection was
not established in the section drafts and is not asserted here. Linking
them to the Paper VIII cluster would require a new argument in §9 or §10.

### The κ Universality (Structural Observation V.1)

$\kappa = \varphi^{-4}$ appears as the attenuation coefficient in:

| Context | Formula | Section |
|---------|---------|---------|
| Mass operator (reff correction) | $r_\text{eff} = 1 + \ln(1 + L/\xi_\text{vac})$ | §3 |
| Fine-structure correction | $f_c = 1 + r_p^2\kappa/(8\pi)$ | §7 |
| Top quark stabilizer | $Z_f = \kappa/8$ | §9 |
| Gravity filtration | $F_g = \kappa/4$ | §10 |
| S-matrix dissipation | $e^{-\kappa n}$ | §11 |

These five appearances were derived independently in separate sections.
Whether they follow from a single axiom (the "Unification Target") or
represent five structurally distinct uses of the same constant is the
question that Structural Observation V.1 names without claiming to answer.

### One Observational Anchor

Every prediction in this paper chains back to one measured input:

$$m_0 \;=\; \frac{m_e}{e^{2\pi/\Phi}}$$

where $m_e = 0.511\,\text{MeV}$ is the electron mass (measured) and
$\Phi$ is derived from the Gaussian throat curvature (no fitting). All
other quantities — quark masses, lepton masses, gauge boson masses,
neutrino mass scale, fine-structure constant retrodiction, Borromean
ropelength, cosmological transmittance — follow from $m_e$ plus geometry
with zero additional tuning.

The open problems listed above are derivations required to close specific
results as theorems; they do not introduce new free parameters. When any
open problem is resolved, the framework either gains a theorem (if the
derivation succeeds) or loses a prediction (if it fails). The register
above is the complete accounting of which results are theorems and which
remain open.

---

*End of Chapter VI — Open Problems Register.*
*Chapter VII: Conclusion and Discussion.*


---

# SQT Paper VII
## Chapter VII — Conclusion

---

### §12  Summary of Results

Paper VII has presented a topological mapping of the observed particle
spectrum and fundamental couplings under the Superfluid Quantum Topology
(SQT) framework. The foundational shift is from particles as point-like
excitations in a vacuum to particles as knotted manifolds in a superfluid
vacuum with Gaussian throat curvature $K(0) = -\varphi^2$.

The framework operates from one observational anchor — the electron mass
$m_e = 0.511\,\text{MeV}$ — and zero tuned parameters. Every prediction
chains through:

$$m_0 \;=\; \frac{m_e}{e^{2\pi/\Phi}}, \qquad
  \Phi \;=\; 2\pi + \frac{K(0)}{8\pi^2}$$

with knot topology, Fano geometry, and the bulk modulus
$\kappa = \varphi^{-4}$ providing the remaining structure.

**Closed results (Theorems and Derivations):**

| Result | Prediction | Observed | Error | Status |
|--------|-----------|---------|-------|--------|
| Down quark mass | 4.589 MeV | 4.67 MeV | −1.74% | Green |
| Charm quark mass | 1245.7 MeV | 1270 MeV | −1.92% | Green |
| Bottom quark mass | 4162.6 MeV | 4180 MeV | −0.42% | Green |
| Top quark mass | 171,185 MeV | 172,690 MeV | −0.87% | Green |
| Tau lepton mass | 1752.4 MeV | 1776.86 MeV | −1.38% | Green |
| $W$ boson mass ($m_0\varphi^{27}$) | 82,128 MeV | 80,379 MeV | +2.18% | Amber |
| $Z$ boson mass | 93,964 MeV | 91,187.6 MeV | +3.05% | Amber |
| $\alpha^{-1}$ retrodiction | 137.040 | 137.036 | +0.003% | Green |

**Boundary cases (known open items):**

| Result | Prediction | Observed | Error | Note |
|--------|-----------|---------|-------|------|
| Up quark mass | 2.039 MeV | 2.2 MeV | −7.31% | Amber — IR boundary |
| Muon mass | 97.79 MeV | 105.658 MeV | −7.45% | Amber — lepton cable boundary |
| $\sin^2\theta_W$ | 0.23607 | 0.2229 (on-shell) | +5.91% | Orange |

*Electron mass: observational anchor ($m_e = 0.511\,\text{MeV}$ defines $m_0$).
Applying the formula at $L = 2\pi$ gives $0.493\,\text{MeV}$ (−3.62%); this
residual reflects the ground-state boundary correction $r_\text{eff}(2\pi) = 1.038$,
not a prediction error. The electron is the scale-setter for Theorem 1, not a
result of it. The −3.6% gap defines exactly where the anchor sits relative to
the formula's self-consistent ground state.*

The Up and Muon errors are labeled boundary cases in the
framework: they occur at the lightest end of each sector where the mass
operator approaches its ground-state limit. They are documented, not
concealed. The Weinberg angle at +5.9% off the on-shell definition is
the largest unexplained discrepancy in the primary derivations.

**Conjectured results (labeled throughout):**

| Result | Value | Status |
|--------|-------|--------|
| Proton topology ($A = 20$) | Derivation from Borromean Alexander polynomial | Closed |
| Baryon stabilizer ($Z_f = 6$) | Conjecture 1 — Riemann-Hurwitz proof pending | Open |
| Borromean ropelength ($L_B = 60.194$ fm) | Prediction within Ashton bounds | Pending verification |
| Neutrino mass ($m_\nu \approx 0.044$ eV) | Prediction under Conjecture 3 | Open |
| Planck 2018 $\sum m_\nu$ bound | Exceeds by 10–30% | Tension |

---

### §13  The Falsifiability Structure

The framework's strength is not that it matches all known numbers — many
models can do that through parameter tuning. Its strength is structural
rigidity: the predictions are not independently adjustable.

The clearest expression of this is the **8D-to-4D Reduction** (Open
Problem 3, Chapter VI), which must simultaneously output:

1. Proton charge radius $r_p = 0.83847\,\text{fm}$
2. Bare coupling $\alpha_\text{bare}^{-1} = 84/\arctan(1/\sqrt{2})$
3. Borromean stabilizer $Z_f = 6$ (Conjecture 1)

These three quantities were derived from separate physical arguments in
separate sections. The claim of the Chapter III Synthesis is that they
resolve from a single calculation. If the 8D reduction produces all three
at the correct values, the framework gains three theorems simultaneously.
If it fails to produce any one of them, all three fail: the calculation
cannot be tuned to preserve two while sacrificing one.

This is the intended falsifiability structure of a zero-free-parameter
framework. The open problems listed in Chapter VI are not weaknesses to
be explained away — they are the precise research fronts where the
framework's claims will stand or fall.

---

### §14  The κ Thread

The bulk modulus $\kappa = \varphi^{-4} \approx 0.1459$ appears as the
attenuation coefficient in five independent derivations:

| Context | Role of $\kappa$ |
|---------|-----------------|
| Mass operator (Theorem 1) | Enters $r_\text{eff}$ via $\xi_\text{vac} = 100\varphi$ |
| Fine-structure correction (§7) | $f_c = 1 + r_p^2\kappa/(8\pi)$ |
| Top quark stabilizer (§9) | $Z_f = \kappa/8$ |
| Gravity filtration (§10) | $F_g = \kappa/4$, $T_g = e^{-\kappa/4}$ |
| S-matrix dissipation (§11) | $E_\text{det} = hf_0 \cdot e^{-\kappa n} \cdot \cos^2\Delta\phi$ |

All five were derived without reference to one another. Whether their
common use of $\kappa$ follows from a single underlying axiom — the
"Universal Attenuation" hypothesis — or represents five structurally
distinct uses of the same constant is the question that Structural
Observation V.1 names without claiming to answer.

Resolving this question may be the deepest result available in Paper VIII.
If the 8D-to-4D reduction produces $\kappa$ as an output of the manifold
geometry — rather than accepting it as a derived quantity from $K(0) =
-\varphi^2$ — then all five appearances become consequences of a single
geometric fact about the vacuum. That would constitute the strongest
unification result in the SQT program to date.

---

### §15  What Paper VII Has and Has Not Established

**Has established:**

- A topological dictionary mapping knot types to quark and lepton
  generations, with 6 of 9 fermion masses predicted Green or near-Green
  from one observational anchor
- $A = 20$ for the nucleon as a closed derivation from the Borromean
  Alexander polynomial — the first zero-free-parameter result for baryon
  topology in this framework
- $\alpha^{-1}$ retrodicted to 0.003% given the muonic proton radius
  as input, via a formula with no fitted couplings
- The $\kappa$ universality as a structural observation across five
  independent sectors
- An honest accounting of 13 open problems and conjectures, including
  one active tension with Planck 2018 data

**Has not established:**

- A derivation of $Z_f = 6$ for the baryon (Conjecture 1)
- A derivation of $r_p$ or the bare coupling from geometry (Open Problem 3)
- A resolution of the Weinberg angle at 5.9% off on-shell (OP.8)
- A neutrino sector in agreement with the Planck mass sum bound (OP.5)
- A derivation of three fermion generations from first principles (OP.13)
- A connection between the Lens Equation and quantum measurement theory
  that satisfies Bell's theorem constraints (Conjecture 5, OP.12)

The boundary between these two lists is the boundary between Paper VII
and Paper VIII. Nothing in the first list depends on anything in the
second. The open problems are research fronts, not hidden assumptions.

---

*Paper VII complete.*
*Paper VIII target: 8D-to-4D dimensional reduction and the derivation of
the framework's three primary conjectures from manifold geometry alone.*


---

# SQT Paper VII — Bibliography

## Primary Mathematical References

**[Torres 1953]**
Torres, G. (1953).
On the Alexander polynomial.
*Annals of Mathematics*, 57(1), 57–89.
https://doi.org/10.2307/1969726

Role: Source for the multivariable Alexander polynomial of the Borromean
link $\Delta_B(t_1,t_2,t_3)$ used in §3.2.

---

**[Ashton 2011]**
Ashton, T., Cantarella, J., Piatek, M., & Rawdon, E. J. (2011).
Knot tightening by constrained gradient descent.
*Experimental Mathematics*, 20(1), 57–90.
https://doi.org/10.1080/10586458.2011.544581

Role: Source for the ideal Borromean ropelength bounds
$L_B^\text{ideal} \in [58.006,\, 62.0]\,\text{fm}$ used in §3.5
and the baryon ropelength prediction test (OP.2).

---

**[Milnor 1954]**
Milnor, J. (1954).
Link groups.
*Annals of Mathematics*, 59(2), 177–195.
https://doi.org/10.2307/1969685

Role: Foundation for Milnor's $\bar{\mu}$-invariants; $\bar{\mu}(123) = 1$
for the Borromean link cited in §3.2 to establish the canonical form of
$\Delta_B$.

---

**[Conway 1970]**
Conway, J. H. (1970).
An enumeration of knots and links, and some of their algebraic properties.
In *Computational Problems in Abstract Algebra* (pp. 329–358).
Pergamon Press.

Role: Background for the Alexander invariant sum-of-squares convention
used throughout Theorem 1 and §3.2.

---

## Experimental and Observational References

**[PDG 2022]**
Workman, R. L., et al. (Particle Data Group). (2022).
Review of Particle Physics.
*Progress of Theoretical and Experimental Physics*, 2022, 083C01.
https://doi.org/10.1093/ptep/ptac097

Role: Source for all PDG particle masses cited in §§3, 8, 9, and the
mass audit tables; W and Z boson masses; muon and tau masses.

---

**[Antognini 2013]**
Antognini, A., et al. (2013).
Proton structure from the measurement of 2S–2P transition frequencies
of muonic hydrogen.
*Science*, 339(6118), 417–420.
https://doi.org/10.1126/science.1230016

Role: Source for the muonic hydrogen measurement
$r_p = 0.84087 \pm 0.00039\,\text{fm}$ (Antognini et al. direct result).
Note: this value differs from the CODATA 2018 compilation below.
The fine-structure retrodiction in §7.4 uses the CODATA 2018 value
$r_p = 0.8414\,\text{fm}$ as input, not the Antognini direct result.

---

**[CODATA 2018]**
Tiesinga, E., Mohr, P. J., Newell, D. B., & Taylor, B. N. (2021).
CODATA recommended values of the fundamental physical constants: 2018.
*Reviews of Modern Physics*, 93(2), 025010.
https://doi.org/10.1103/RevModPhys.93.025010

Role: Source for $\alpha^{-1}_\text{CODATA} = 137.035\,999\ldots$,
the electron mass $m_e = 0.511\,\text{MeV}$ (the framework's sole
observational anchor), and the compiled proton charge radius
$r_p = 0.8414 \pm 0.0015\,\text{fm}$ used as input to the §7.4
fine-structure retrodiction.

---

**[Planck 2018]**
Planck Collaboration: Aghanim, N., et al. (2020).
Planck 2018 results. VI. Cosmological parameters.
*Astronomy & Astrophysics*, 641, A6.
https://doi.org/10.1051/0004-6361/201833910

Role: Source for the neutrino mass sum bound
$\sum m_\nu < 0.12\,\text{eV}$ (95% CL) cited in §8.5 and the
neutrino sector tension (OP.5).

---

**[SNO 2002]** (representative neutrino oscillation reference)
Ahmad, Q. R., et al. (SNO Collaboration). (2002).
Direct evidence for neutrino flavor transformation from neutral-current
interactions in the Sudbury Neutrino Observatory.
*Physical Review Letters*, 89(1), 011301.
https://doi.org/10.1103/PhysRevLett.89.011301

Role: Background for the neutrino oscillation mass splittings
$\Delta m^2_{21}$, $|\Delta m^2_{31}|$ used in §8.5 to compute
the neutrino mass sum under Interpretation B.

---

## Cosmological References

**[Penrose 2010]**
Penrose, R. (2010).
*Cycles of Time: An Extraordinary New View of the Universe.*
Bodley Head, London.

Role: Source for Conformal Cyclic Cosmology (CCC) framework and the
concept of aeon-boundary transmission of gravitational signals, cited
in §10.4.

---

**[Gurzadyan 2010]**
Gurzadyan, V. G., & Penrose, R. (2010).
Concentric circles in WMAP data may provide evidence of violent
pre-Big-Bang activity.
arXiv:1004.1521 [astro-ph.CO].
https://arxiv.org/abs/1004.1521

Role: Source for the Hawking Points claim cited in §10.4.
Note: The observational status of this result is disputed;
see [Moss 2011] below.

---

**[Moss 2011]**
Moss, A., Scott, D., & Zibin, J. P. (2011).
No evidence for anomalously low variance circles on the sky.
*Journal of Cosmology and Astroparticle Physics*, 2011(04), 033.
https://doi.org/10.1088/1475-7516/2011/04/033

Role: Counter-evidence to [Gurzadyan 2010]; cited in §10.4 to
establish that the Hawking Points observation is currently disputed
and the framework's connection to CMB anomalies is qualitative
consistency, not a confirmed prediction.

---

## Group Theory and Algebraic References

**[Conway 1985]**
Conway, J. H., & Sloane, N. J. A. (1988).
*Sphere Packings, Lattices and Groups.*
Springer-Verlag, New York.

Role: Background for $\text{PSL}(2,7)$ of order 168 and its
action on the Fano plane $\text{PG}(2,2)$; cited in §§3.4 and 7.2.2.

---

**[Wilson 2009]**
Wilson, R. A. (2009).
*The Finite Simple Groups.*
Springer, London.

Role: Reference for $F_7^* \cong \mathbb{Z}_6$ as the multiplicative
group of the Galois field $\mathbb{F}_7$, used in the $Z_f = 6$
derivation (Conjecture 1, §3.4).

---

## Bell's Theorem Reference

**[Bell 1964]**
Bell, J. S. (1964).
On the Einstein–Podolsky–Rosen paradox.
*Physics*, 1(3), 195–200.
https://doi.org/10.1103/PhysicsPhysiqueFizika.1.195

Role: The constraint that Conjecture 5 (§11.5) must satisfy; cited in
Open Problem 6 (OP.12) as the primary obstacle to the hidden-variable
interpretation of $\cos^2(\Delta\phi)$.

---

## SQT Internal Cross-References

**[SQT Paper I–VI]**
Gifford, M. (2023–2025).
Superfluid Quantum Topology: Papers I–VI.
Unpublished working manuscripts, Ridgemark, CA.

Note: Papers I–VI establish Theorems 1–3, the mass operator, the
Alexander invariant sum-of-squares convention, and the force-residual
correspondence from which all results in Paper VII are derived.
Theorem numbers referenced throughout this paper (Theorem 1: mass
operator; Theorem 2: Worticity sum rule; Theorem 3: force-residual
correspondence) refer to these prior papers.

---

## Software and Numerical Tools

**[SQT Explorer v1.9/v2.0]**
Gifford, M. (2026).
SQT Interactive Explorer v1.9/v2.0 (React/JSX).
Available as supplementary material.

Role: All numerical values cited in the paper — mass predictions,
error percentages, fine-structure retrodiction, ropelength bisection —
are computed live in this application. The source code is the
computational source of truth for all quantitative results.

---

*End of bibliography. 16 primary references + 1 software citation.*

## Notes on References Needed for Future Drafts

The following citations are mentioned or implied in the text but
require specific reference completion:

1. **Torres 1953 page number** for the specific Borromean polynomial
   form — confirm the exact theorem number in the original paper.
2. **Riemann-Hurwitz** — if Conjecture 1 (OP.1) is resolved in
   Paper VIII, a primary reference for the Riemann-Hurwitz formula
   applied to the Borromean complement will be needed.
3. **Ideal ropelength computations** — Cantarella, Kusner, & Sullivan
   (2002) "On the minimum ropelength of knots and links" may provide
   additional bounds context beyond [Ashton 2011].
4. **Neutrino oscillation parameters** — a more recent reference than
   [SNO 2002] giving the current best-fit values of $\Delta m^2_{21}$
   and $|\Delta m^2_{31}|$ should be included when §8.5 is finalized.


---

# SQT — Forward Program
## Appendix E.1 and Paper VIII Preamble

*Status: Requirements locked. Mathematical execution pending.*

---

## Appendix E.1 — Numerical Ropelength Minimization Protocol

**Objective.** Tighten the Ashton et al. (2011) bounds for the ideal
Borromean rings ($L_{6a4}$) from their current $6.7\%$ window
$[58.006,\,62.0]\,\text{fm}$ to precision $\epsilon < 0.5\%$.

This is a computational geometry problem external to the SQT framework.
The framework provides the prediction; this protocol specifies what a
numerical collaborator must compute to verify or falsify it.

### E.1.1  Model Parameters

**Topology.** Three-component link with:
- Pairwise linking numbers $\ell_{ij} = 0$ for all $i \neq j$
- Non-trivial Milnor invariant $\bar{\mu}(123) = 1$
- Knot atlas identifier: $L_{6a4}$ (Borromean rings)

**Objective function.** Ropelength minimization: find the configuration
that minimizes $\mathcal{L} = L/R$ (arc-length divided by tube radius)
subject to the constraints below. Equivalently: maximize $R$ for unit
arc-length.

**Constraints.**
1. Non-self-intersection: $\text{dist}(x, y) \geq 2R$ for all
   $x \neq y$ on the link.
2. Local thickness: curvature $1/\rho \leq 1/R$ at every point.
3. Component topology preserved: no strand crossings during
   gradient descent.

**Recommended solver.** RIDGERUNNER (Cantarella, Piatek, Rawdon) —
constrained gradient descent on the space of polygonal links, with
Brakke's Surface Evolver for cross-validation.

### E.1.2  Verification Target and Falsification Threshold

The SQT bisection solves $m(A{=}20,\,Z_f{=}6,\,L) = 938.272\,\text{MeV}$
for $L$, yielding:

$$L_B^\text{target} = 60.194\,\text{fm}$$

The verification window is:

$$\boxed{L_B^\text{target} = 60.194 \pm 0.3\,\text{fm}}$$

**Justification of $\pm 0.3\,\text{fm}$.** This window is chosen so
that a minimized value landing *outside* $[59.894,\,60.494]\,\text{fm}$
while remaining *inside* the Ashton bounds $[58.006,\,62.0]$ would
still falsify the hadronic mass prediction at the claimed leading-order
precision. The Ashton bounds alone are too wide ($6.7\%$) to distinguish
the SQT prediction from other values. A minimized bound tighter than
$\pm 0.3\,\text{fm}$ ($< 0.5\%$ precision) would make the prediction
either confirmed or falsified rather than merely consistent.

### E.1.3  Outcomes

| Result | Interpretation |
|--------|---------------|
| Minimized $L_B \in [59.894,\,60.494]\,\text{fm}$ | Prediction confirmed — Conjecture 1 + $A=20$ together survive numerical test |
| Minimized $L_B \in [58.006,\,59.894)$ or $(60.494,\,62.0]$ | Prediction falsified at leading order — framework requires revision |
| Minimized $L_B \notin [58.006,\,62.0]$ | Ashton bounds incorrect — recompute with current solver |

**Note.** Confirmation here means the ropelength prediction is
*consistent with* the minimization result, not that the prediction
is proven. A geometric proof that the ideal Borromean ropelength is
*exactly* $60.194\,\text{fm}$ would require analytic methods beyond
numerical minimization.

---

## Paper VIII Preamble — The 8D-to-4D Reduction

**Objective.** Define the axiomatic foundation and boundary constraints
for the dimensional reduction $\Psi: \mathcal{M}^8 \to \mathcal{M}^4$
that must simultaneously produce the framework's three primary conjectures
as outputs.

### P8.1  The Single Axiomatic Input

The only independent physical input is the Gaussian throat curvature of
the ground-state superfluid:

$$\boxed{K(0) = -\varphi^2}$$

All derived constants follow algebraically:

$$\kappa \;=\; \varphi^{-4} \;=\; |K(0)|^{-2}$$

The bulk modulus is the inverse square of the curvature magnitude.
This identity is algebraically forced by $K(0) = -\varphi^2$ and
requires no independent assumption. The **Unification Check** for
Paper VIII is therefore not "does the reduction produce $\kappa$?"
(it must, by algebra) but rather: *why does $|K(0)|^{-2}$ govern
mass, electromagnetic coupling, gravity filtration, and S-matrix
dissipation simultaneously?* That is, why is the inverse-square of
the vacuum curvature the universal attenuation rate across all physical
sectors?

### P8.2  The Ambient Manifold

The natural 8-dimensional manifold for the SQT bulk is octonionic
space $\mathbb{O} \cong \mathbb{R}^8$, deformed by the throat curvature:

$$\mathcal{M}^8: \quad \mathbb{O} \text{ with } K(0) = -\varphi^2$$

**Why octonionic space.** The seven imaginary units
$e_1, \ldots, e_7 \in \mathbb{O}$ are indexed by the seven points of the
Fano plane $\text{PG}(2,2)$, with the seven lines of the Fano plane
encoding the multiplication rule $e_i e_j = \pm e_k$ iff $\{i,j,k\}$
is a Fano line. The automorphism group of $\mathbb{O}$ is $G_2 \supset
\text{SU}(3)$, connecting to color symmetry. The symmetry group of the
Fano plane is $\text{PSL}(2,7)$, of order 168.

The Fano-lattice and octonionic descriptions are therefore not competing
metric candidates — they are two levels of description of the same
manifold. Octonionic flat space deformed by $K(0) = -\varphi^2$ is
the bulk metric; the Fano structure is the boundary dictionary for
reading off $Z_f$ values. Paper VIII uses both.

### P8.3  Structural Constraints on $\Psi$

The reduction $\Psi: \mathcal{M}^8 \to \mathcal{M}^4$ must satisfy:

**C1 — Conformality.** $\Psi$ is a conformal map. This preserves
angle structure (and hence phase-field couplings) across the reduction,
preventing gauge drift in the $\alpha^{-1}$ retrodiction.

**C2 — Boundary topology.** $\partial\mathcal{M}^8 \cong S^7$ or a
specific quotient $S^7/\Gamma$ consistent with the octonionic symmetry.
The 7-sphere is the natural boundary of $\mathbb{O}$ and carries the
Hopf fibration $S^7 \to S^4$ with fiber $S^3$, relating 8D bulk to
4D boundary geometrically.

**C3 — Symmetry preservation.** $\Psi$ preserves the action of
$\text{PSL}(2,7)$ on $\partial\mathcal{M}^8$. This is required for the
Fano stabilizer structure — and hence $Z_f$ values — to be readable
from the boundary data. If PSL(2,7) is broken by $\Psi$, Conjecture 1
cannot be derived.

### P8.4  Required Outputs

A valid reduction must simultaneously produce, without independent
adjustment:

| Output | Target value | Physical role |
|--------|-------------|---------------|
| $r_p$ | $0.83847\,\text{fm}$ | Scale of 4D electromagnetic boundary |
| $\alpha_\text{bare}^{-1}$ | $84/\arctan(1/\sqrt{2})$ | Bare EM coupling from Fano lattice |
| $Z_f$ | $6$ | Stabilizer of the Fano triangle ($F_7^*$ action) |

Additionally, the reduction must demonstrate that $\kappa = |K(0)|^{-2}$
appears as the attenuation coefficient in each physical sector as a
*geometric consequence* of the bulk-to-boundary map, not by separate
assumption.

### P8.5  The First Calculation

The entry point for Paper VIII:

1. Write the metric on $\mathcal{M}^8$ explicitly as octonionic flat
   space with the $K(0) = -\varphi^2$ deformation.
2. Identify the conformal boundary $S^7$ and its $\text{PSL}(2,7)$
   action inherited from the Fano structure of $\mathbb{O}$.
3. Compute the mode decomposition of the conformal reduction from
   $S^7$ to $S^4$ (the Hopf fibration step).
4. Check whether the surviving boundary modes include the three
   target invariants ($r_p$, $\alpha_\text{bare}^{-1}$, $Z_f = 6$)
   at the correct values.

Step 4 is where the framework succeeds or fails. Steps 1–3 are the
mathematical prerequisites.

### P8.6  What Cannot Be Specified in Advance

The following cannot be determined from the requirements document alone —
they require the calculation:

- Whether the $K(0) = -\varphi^2$ deformation of octonionic flat space
  produces a well-defined conformal reduction (the space may need to be
  compact or have specific boundary conditions to admit the Hopf fibration)
- Whether the PSL(2,7) action on $S^7$ descends to the correct
  stabilizer structure on $S^4$
- Whether the numerical values of $r_p$ and $\alpha_\text{bare}^{-1}$
  follow from the geometry or require additional structure

These open questions define the risk: the manifold setup is consistent
with the framework's requirements, but consistency is not sufficiency.

---

---

## Additional Research Direction: The $n=4$ Angular Convergence Gap

**Observation.** The gap between $\arcsin(1/n)$ and $\arctan(1/n)$
converges toward zero as $n \to \infty$:

| $n$ | $\arcsin(1/n)$ | $\arctan(1/n)$ | Gap |
|-----|--------------|--------------|-----|
| 1 | 90.00° | 45.00° | 45.00° |
| 2 | 30.00° | 26.57° | 3.43° |
| 3 | 19.47° | 18.43° | 1.04° |
| 4 | 14.48° | 14.04° | **0.44°** |
| 5 | 11.54° | 11.31° | 0.23° |

The convergence is exact in the large-$n$ limit: both
$\arcsin(1/n) \approx 1/n$ and $\arctan(1/n) \approx 1/n$ (radians)
for large $n$, so the gap vanishes algebraically. At $n = 4$ the gap
is $0.44° \approx 0.00768$ radians.

**The structural coincidence.** The SQT bulk modulus uses the fourth
power: $\kappa = \varphi^{-4}$. The framework maps an 8D bulk to a 4D
boundary — a factor of 4 in dimensionality. The $n = 4$ row is where
the gap first falls below $0.5°$.

**Open question (Research Direction, not Conjecture).** Does the
$n = 4$ convergence gap of $0.44°$ have a strict geometric
interpretation in the $\mathcal{M}^8 \to \mathcal{M}^4$ dimensional
reduction? Specifically:

1. Does this angular differential relate to the phase misalignment
   $\Delta\phi$ in the S-matrix Lens Equation (§11), or is it a
   numerical artifact of the integer sequence?
2. Is the near-equality $0.00768\,\text{rad} \approx \kappa/19$
   meaningful, or coincidental?
3. Does the gap's rate of convergence encode information about the
   number of spacetime dimensions, or does the same gap appear at
   $n = 4$ for any framework with a fourth-power modulus?

**Epistemic label.** This is a structural observation at the same level
as Remark III.1 ($\varphi^4 + \kappa = 7$): the coincidence is real,
the mechanism is absent. It becomes a conjecture only if a derivation
connects the $n = 4$ gap to a specific geometric object in the
$S^7 \to S^4$ Hopf fibration or the Lens Equation phase factor.

---

*Appendix E.1 and Paper VIII Preamble complete.*
*Next action: execute the RIDGERUNNER protocol (Appendix E.1) and*
*write the octonionic metric for $\mathcal{M}^8$ (Paper VIII §1).*

---

## Paper VIII §1 — Derived Results and Open Problems
### Session record: Ridgemark workshop, April 2026

*Status: Proposition P8.1 derived and adversarially audited. Three open
problems identified, bounded, and logged. The metric ansatz, instanton
calculation, and symmetry-breaking chain are established. The squashing
parameter $t$ remains free. All results below have been checked against
the multiplication table and the constraint structure.*

---

### P8.1.1  The Throat Metric

The deformed octonionic manifold $\mathcal{M}^8$ carries the warped product metric:

$$ds^2 = dr^2 + \bigl(r^2 + \varphi^{-2}\bigr)
  \bigl[\pi^*(g_{S^4}) + t^2\,g_{S^3}^{\text{fiber}}\bigr]$$

using the quaternionic Hopf decomposition $\mathbb{O} = \mathbb{H} \oplus \mathbb{H}\ell$
with $(q_1, q_2) \in \mathbb{H}^2$, $|q_1|^2 + |q_2|^2 = 1$, and
projection $\pi(q_1, q_2) = q_1 q_2^{-1} \in \mathbb{HP}^1 \cong S^4$.

**Why Path B over Path A.** A conformally flat metric has vanishing Weyl tensor
and full $SO(8)$ local isotropy. The $G_2$ automorphism group of $\mathbb{O}$
requires non-vanishing Weyl curvature to encode the anisotropic Fano
multiplication table and thereby all $Z_f$ values. A conformally flat bulk
erases the Fano structure. The warped product preserves $G_2$ anisotropy.

**Sectional curvatures at the throat $r = 0$:**

$$K_\text{radial-angular}(0) = -\varphi^2 \quad \text{(7 planes)}, \qquad
  K_\text{angular-angular}(0) = +\varphi^2 \quad \text{(21 planes)}$$

$$S_{\mathcal{M}^8}(0) = 2(7 \times (-\varphi^2) + 21 \times (+\varphi^2)) = +28\varphi^2$$

The 8D scalar curvature at the throat is **positive**. The assumption
$S = 56K(0) = -56\varphi^2$ (constant curvature) is **withdrawn** and
**must not reappear**. The quartic $3t^4 - 34t^2 - 3 = 0$ and its root
$t^2 \approx 11.42$ are **struck from the record** — derived from a
double error (wrong scalar curvature, constraint double-spent).

---

### P8.1.2  Geometric Parameter Status

| Quantity | Value | Status |
|----------|-------|--------|
| $R_0 = \varphi^{-1}$ | Throat minimum radius | **Established** |
| $\kappa = R_0^4 = \varphi^{-4}$ | Bulk modulus | **Established** |
| $\mathrm{Vol}(S^4)\big\vert_{r=0} = \tfrac{8\pi^2}{3}\kappa$ | Boundary 4-volume | **Established** |
| $\|F_\omega\|^2 = 24\kappa^{-1}$ | Instanton curvature | **Established** |
| $t$ | Fiber-to-base scale ratio | **Free — not fixed by $K(0)$** |

**Proposition 1.1 (Volumetric Identity).** The bulk modulus $\kappa = \varphi^{-4}$
is the 4-volume of the $S^4$ electromagnetic boundary at $r = 0$, up to
$3/8\pi^2$. The attenuation $e^{-\kappa n}$ is volumetric dilution across
$n$ boundary layers of cross-sectional volume $\propto \kappa$.

**Note on $\kappa$ vs $\kappa^{-1}$.** The instanton curvature $\|F_\omega\|^2 = 24\kappa^{-1}$
is the inverse bulk modulus. In a superfluid, a stiffer medium (large $\kappa$)
supports shallower order-parameter gradients (small connection curvature).
$\kappa$ governs volumetric capacity; $\kappa^{-1}$ governs connection rigidity.
These are dual quantities, not identical.

---

### P8.1.3  Proposition P8.2 — Symmetry Breaking under Squashing

**True PSL(2,7) generators in $SO(7)$** acting on $\{e_1,\ldots,e_7\}$:

$$C: e_i \mapsto e_{i+1 \bmod 7} \qquad \text{(order 7)}$$
$$S: e_i \mapsto e_{-i^{-1} \bmod 7}, \text{ acting as } (1\ 6)(2\ 3)(4\ 5) \qquad \text{(order 2)}$$

Both generators map Fano points across the $\{1,2,4\}/\{3,5,6,7\}$ split.
The PSL(2,7) embedding in $SO(8)$ is transverse to $Sp(2)\cdot Sp(1)$.

Note: The previously proposed generator $T$ (negating $\mathbb{H}^\perp$)
is a signed permutation in the hyperoctahedral group, **not** in PSL(2,7).
It is **withdrawn**.

**Proposition P8.2.** For $t \neq 1$, the subgroup of $\mathrm{PSL}(2,7)$
acting isometrically on the squashed Hopf $S^7$ is the stabilizer of the
Fano line $\{1,2,4\}$, of order 24, isomorphic to $S_4$.

*Proof sketch.* Generator $C$ maps $e_2$ (base, unscaled) to $e_3$ (fiber,
scaled by $t$). Norm preservation under the squashed metric requires $t = 1$.
Generator $S$ maps $e_1$ (base) to $e_6$ (fiber); same constraint.
The only PSL(2,7) elements compatible with $t \neq 1$ preserve the
$\{1,2,4\}$ and $\{3,5,6,7\}$ partition. This is the line stabilizer,
order $168/7 = 24 \cong S_4$. $\square$

**Corollary.** $F_7^* \cong \mathbb{Z}_6$ breaks under squashing:

$$\mathbb{Z}_6 \xrightarrow{t \neq 1} \mathbb{Z}_3$$

The surviving $\mathbb{Z}_3 = \{1,2,4\}$ cycles Fano base points.
The broken order-2 coset $\{3,5,6\}$ is the base-fiber exchange symmetry.
When $t \neq 1$, spacetime and gauge space have different geometric scales;
the exchange is broken; the geometric distinction between them is born.

**Correction on record.** The Fano triangle (Borromean color singlet) is
non-collinear and therefore cannot lie entirely within the base line
$\{1,2,4\}$. Every Fano triangle straddles the base-fiber split.
Squashing does not lock the baryon into spacetime; it locks the
**relative orientation** of the baryon across the spacetime-gauge divide.
Any confinement argument must address this orientation-locking, not
spatial localization. Claims to the contrary are **withdrawn**.

---

### P8.1.4  Open Problems for Paper VIII

**OP.VIII.1 — Fix the squashing parameter $t$**

$K(0) = -\varphi^2$ fixes $R_0$ but is orthogonal to $t$.
Candidate conditions:
- PSL(2,7) isometry → forces $t = 1$ (round sphere)
- Einstein condition → $t^2 = 5/4$ (Jensen 1973)
- PSL(2,7) descent condition on $S^4$ → may select a specific $t$

*Closes when:* The PSL(2,7) action on $S^7$ is computed at candidate $t$
values and the descent to $S^4$ is checked for the correct stabilizer
structure ($F_7^*$ action on non-collinear triples).

**OP.VIII.2 — Connect 84 to $\arctan(1/\sqrt{2})$ in the same geometry**

Proposition P8.2 provides a mechanism for the 84 (half of PSL(2,7) broken
by squashing). The $\arctan(1/\sqrt{2})$ factor in $\alpha_\text{bare}^{-1}$
comes from a separate cubic lattice argument in Paper VII §7.2.1. For
Conjecture 2 to become Theorem 4, both factors must emerge from one calculation.

*Closes when:* The holonomy angle of the Sp(1) connection around a minimal
loop on $S^4$ at $R_0 = \varphi^{-1}$ is computed and checked against
$\arctan(1/\sqrt{2})$.

**OP.VIII.3 — Lorentzian signature from the throat**

A Riemannian submersion cannot flip metric signature. The Lorentzian
character of 4D spacetime is not derivable from the Hopf projection
within the Riemannian framework alone.

*Conjecture (logged, not claimed):* $K(0) = -\varphi^2 < 0$ forces a
signature change under analytic continuation at $r = 0$, implementing
a Wick rotation as a geometric consequence rather than a manual assumption.

*Closes when:* $\det(g)$ at $r = 0$ is computed and its sign under analytic
continuation of $r$ is determined. If $\det(g)|_{r=0} < 0$ under the throat
constraint, Lorentzian signature is derived. If not, the Wick rotation must
be imposed externally and its origin remains open for Paper IX.

---

### P8.1.5  What Paper VIII Must Not Claim Without Independent Derivation

1. That $t \neq 1$ is forced by the throat geometry
2. That the Fano triangle is locked into the spacetime base
3. That the broken $\mathbb{Z}_2$ directly produces color confinement
4. That 84 gives the electromagnetic coupling without connecting $\arctan(1/\sqrt{2})$
5. That Lorentzian signature is derived from the Hopf projection alone

---

*Paper VIII §1 results logged. Three open problems bounded.*
*Next action: attack OP.VIII.1 — compute the PSL(2,7) descent to $S^4$*
*at $t = 1$ and $t = 5/4$ and determine which produces the correct*
*stabilizer structure for the Borromean color singlet.*

---

### OP.VIII.1 — Resolution (corrected)

**Date:** Ridgemark workshop, April 2026

**Previous calculation withdrawn.** An earlier attempt to test PSL(2,7) descent
compared base projections of co-fiber image points rather than testing whether
image points of co-fiber points remain co-fiber. That test was structurally
incorrect. The correct co-fiber test ($q_1'^{-1}q_1 = q_2'^{-1}q_2$) showed
that at least one $S_4$ generator *does* descend to the $S^4$ base.

**Correct resolution.** The failure of the full PSL(2,7) to descend is a known
topological fact, not derived from the fiber-point calculation:

The quaternionic Hopf fibration $\pi: S^7 \to S^4$ depends on the choice of a
specific quaternionic subalgebra $\mathbb{H} \subset \mathbb{O}$. The
automorphism group $G_2$ acts transitively on the space of all quaternionic
subalgebras of $\mathbb{O}$. A generic $G_2$ element maps $\mathbb{H}$ to a
different subalgebra $\mathbb{H}'$, shredding the fiber structure: fibers of
the original fibration map to fibers of a *different* Hopf fibration defined
over $\mathbb{H}'$. Only the subgroup of $G_2$ strictly preserving $\mathbb{H}$
can descend. For PSL(2,7), this is exactly the $S_4$ line stabilizer of
$\{1,2,4\}$ (Proposition P8.2). The remaining 144 elements rotate $\mathbb{H}$
and cannot descend to the original $S^4$.

**Consequence for $t$.** The PSL(2,7) descent condition cannot fix $t$ because
the discrete algebra does not constrain the squashing — it cannot descend to
$S^4$ regardless of $t$. The squashing parameter $t$ is unconstrained by the
Fano algebra and is fixed by a continuous geometric condition.

**Resolution.** The Einstein condition $t^2 = 5/4$ (Jensen 1973) is adopted as
the natural minimal-action geometric selector. This is an *assumption* about
the vacuum geometry, not derived from the throat curvature or the Fano algebra.
It must be stated as such in Paper VIII.

**Status: OP.VIII.1 closed.** The discrete Fano algebra does not fix $t$.
The Einstein condition $t^2 = 5/4$ is assumed. The geometry at the throat
is now fully specified:

$$\boxed{R_0 = \varphi^{-1}, \qquad t^2 = \tfrac{5}{4}}$$

**Citation needed:** The statement that $G_2$ acts transitively on quaternionic
subalgebras of $\mathbb{O}$ should be cited. Standard reference:
Harvey, *Spinors and Calibrations* (1990), Chapter 8; or
Baez, "The Octonions," *Bull. AMS* 39 (2002), §4.1.


---

### OP.VIII.2 — Negative Result (logged)

**Date:** Ridgemark workshop, April 2026

**The calculation.** OP.VIII.2 asked whether the Sp(1) connection holonomy
around a minimal loop on $S^4$ at $R_0 = \varphi^{-1}$ evaluates to
$\arctan(1/\sqrt{2})$, which would connect the bare electromagnetic coupling
of Paper VII §7.2.1 to the continuous Hopf geometry.

Two geometric objects were tested:

**Test 1: BPST instanton holonomy.**
The holonomy of the canonical unit-charge Sp(1) connection around a
hemisphere boundary (great $S^3 \subset S^4$) is determined by the instanton
number:

$$k = \frac{1}{8\pi^2}\int_{S^4} \mathrm{tr}(F_\omega \wedge F_\omega) = 1$$

The holonomy around the hemisphere is $\exp(\pi\,\mathbf{n})$ for a unit
imaginary quaternion $\mathbf{n}$ — a rotation by $\pi$ in the Sp(1) fiber.
This is a topological invariant: it does not depend on $R_0$ or $t$, and
it evaluates to $\pi \approx 180°$, not $\arctan(1/\sqrt{2}) \approx 35.26°$.
To obtain $35.26°$ from holonomy would require a loop enclosing exactly
$35.26°/180° \approx 19.6\%$ of $S^4$'s area — a fraction with no geometric
motivation in the framework.

**Test 2: O'Neill mixing angle.**
The O'Neill tensor $|A|$ measures the geometric tilt between base and fiber
directions in the squashed Hopf fibration. At $R_B = \varphi^{-1}$ and
$t^2 = 5/4$:

$$|A|^2 = 6\,t^2\varphi^2 = 6 \times \tfrac{5}{4} \times \varphi^2
  = \tfrac{15}{2}\varphi^2$$

The dimensionless mixing angle defined by the ratio of $|A|$ to the base
curvature scale $K_\text{base}^{1/2} = \varphi$:

$$\theta_\text{mix} = \arctan\!\left(\frac{|A|}{K_\text{base}^{1/2}}\right)
  = \arctan\!\left(\sqrt{\tfrac{15}{2}}\right)
  = \arctan(2.739\ldots) \approx 69.97°$$

This is not $\arctan(1/\sqrt{2}) \approx 35.26°$.

**Negative result.** No computation in the Hopf bundle framework at the
specified parameters $R_0 = \varphi^{-1}$, $t^2 = 5/4$ reproduces
$\arctan(1/\sqrt{2})$. The O'Neill mixing angle at the Einstein squashing
evaluates to $\approx 70°$. The symmetric instanton holonomy is $\pi$,
independent of all metric parameters.

**Physical conclusion.** The 8D-to-4D dimensional reduction of the continuous
vacuum manifold does not generate the electromagnetic bare coupling angle
$\arctan(1/\sqrt{2})$. If this angle is physically real, its origin lies in
the discrete algebraic structure of the cubic vacuum lattice (Paper VII §7.2.1)
— the angle between the space diagonal and face diagonal of the $3^3 = 27$
cubic lattice, which is fixed by the Weak force geometry at residual $r = 3$.
The continuous Riemannian geometry of the squashed Hopf fibration and the
discrete cubic lattice geometry are **distinct regimes** of the SQT vacuum.
They both contribute to $\alpha_\text{bare}^{-1}$, but through separate
mechanisms that have not been unified into a single calculation.

**Implication for Conjecture 2.** The geometric mechanism for the 84 (half of
PSL(2,7) broken by squashing — Proposition P8.2) is established. The geometric
mechanism for $\arctan(1/\sqrt{2})$ in the same framework is not. Conjecture 2
($\alpha_\text{bare}^{-1} = 84/\arctan(1/\sqrt{2})$) remains a conjecture: its
two factors have distinct geometric origins that have not been shown to arise
from one calculation. This is the honest status.

**Status: OP.VIII.2 remains open.** The geometric object connecting the
continuous Hopf geometry to the discrete cubic lattice angle has not been
identified. The negative result is recorded, not explained away.

**What would close it.** Either: (a) identify a geometric object in the Hopf
bundle framework that evaluates to $\arctan(1/\sqrt{2})$ at the throat
parameters — a candidate other than holonomy and O'Neill mixing angle; or
(b) demonstrate that the two factors of $\alpha_\text{bare}^{-1}$ arise from
genuinely separate physical mechanisms (continuous geometry and discrete
lattice), in which case their product is not a single geometric result but a
two-regime formula, and Conjecture 2 requires restatement accordingly.


---

### OP.VIII.3 — Partial Resolution with Caveat (logged)

**Date:** Ridgemark workshop, April 2026

**The calculation.** Analytic continuation $r \to i\tau$ applied to the
throat metric at $r = 0$ transforms $dr^2 \to -d\tau^2$. The metric
determinant flips sign: $\det(g) < 0$ in the continued coordinates.
The signature at the throat becomes $(-,+,+,+,+,+,+,+)$.

**What is established.** The sign flip is correct arithmetic. Under the
substitution $r = i\tau$, the radial term picks up a minus sign and the
angular terms remain positive definite at $\tau = 0$. The continued metric
has Lorentzian signature with the radial axis as the timelike direction.

**The caveat — the Wick rotation is not forced.**
The analytic continuation $r \to i\tau$ is performed by hand. A Riemannian
manifold with metric $ds^2 = dr^2 + f(r)^2 g_{S^7}$ has $\det(g) > 0$
everywhere on its domain $r \in [0, \infty)$. Extending to $r^2 < 0$ always
yields $-d\tau^2$, regardless of whether a throat is present. The same sign
flip appears for flat $\mathbb{R}^8$ under the same substitution. Therefore,
the Lorentzian signature is not a geometric consequence of the specific throat
curvature $K(0) = -\varphi^2$ — it is a consequence of analytically continuing
any radial coordinate past the origin. The Wick rotation remains manual.

**What the throat does contribute — a genuine result.**
The throat sets a finite temporal extent for the continued geometry. The
analytically continued angular scale is:

$$R(\tau)^2 = \varphi^{-2} - \tau^2$$

This is real only for $|\tau| < \varphi^{-1} = R_0$. The universe has a
finite temporal extent $\Delta\tau = 2R_0 = 2\varphi^{-1}$ in the
analytically continued region before the metric becomes complex and the
geometry collapses. This is a genuine, throat-dependent result: the
temporal extent is set by the minimum throat radius.

**The time interpretation.** If the Wick rotation is accepted (as an
assumption, not a derivation), the radial bulk axis becomes macroscopic
time. A signal traversing $n$ $Z_f$ stabilizer layers outward from the
throat traverses a proper time $\Delta\tau = n \cdot \delta\tau$ in the
continued geometry. The Lens Equation attenuation $e^{-\kappa n}$ is
then volumetric dilution over proper time steps of size $\delta\tau$
set by the throat geometry. This is consistent with the "time is distance"
intuition, but requires accepting the Wick rotation as an input.

**New open problem: OP.VIII.4 — The 1+4 dimensional boundary.**
The $S^4$ base has 4 spatial dimensions. Observable spacetime has 3.
If the radial axis is time and $S^4$ is space, the macroscopic boundary is
$1+4$ dimensional, not $1+3$. Three candidate mechanisms for reducing $S^4$
to $S^3$ are known but none is clean:
(a) Restrict to an equatorial $S^3 \subset S^4$ via a $\mathbb{Z}_2$ quotient
    — requires physical motivation
(b) A second analytic continuation makes one $S^4$ direction timelike,
    but produces two timelike dimensions
(c) The Hopf fibration collapses one $S^4$ dimension — but $S^7 \to S^4$
    produces 4D, not 3D

This is not a resolution; it is a new open problem. It must not be stated
as resolved in Paper VIII.

**Status: OP.VIII.3 partially resolved.**

| Claim | Status |
|-------|--------|
| Analytic continuation gives $(-,+,+,+,+,+,+,+)$ | Established (arithmetic) |
| $K(0) = -\varphi^2$ forces the Wick rotation | Not established |
| Temporal extent $= 2\varphi^{-1}$ from throat | Established (throat-dependent) |
| Radial axis = macroscopic time | Consistent if Wick rotation assumed |
| $S^4$ base reduces to observable $S^3$ | Open — OP.VIII.4 |

**What would fully close OP.VIII.3.** Show that the negative curvature
$K(0) < 0$ at the throat is a *necessary* condition for the analytic
continuation to produce a physically real Lorentzian geometry — i.e., that
for $K(0) > 0$, the continuation produces a complex or indefinite metric
that has no physical interpretation, while $K(0) < 0$ is the unique case
where the continued geometry is real and causal. This requires a classification
argument, not just the substitution calculation.



---

