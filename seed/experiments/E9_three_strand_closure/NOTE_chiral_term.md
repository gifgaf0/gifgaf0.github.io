# Derivation note: a chiral stiffness term for the three-strand medium

*October 31, 2026. Label: Exploration. Derivation note. No loop has been computed. Written after `STATUS_step3.md` (Route A twist and vorton routes both negative), at the author's request. Check script: `chiral_term_checks.py`; output: `chiral_term_checks_output.txt`. Citations are tagged [memory] until checked.*

## 0. The question

Route A's twisted loop collapses at every (κ, η) tested. A gradient-squared term scales like L under a size change, so shrinking always pays. Two options were considered:

- **A four-derivative term (Faddeev type).** Its natural source, the gauge field's own energy in the Babaev–Faddeev–Niemi rewriting, comes paired with a supercurrent that screens it at the very scale it would act.
- **The author's proposal.** The stiffness comes from the medium itself. If the medium is made of small units with a handedness (for example torus duals), the charge could favour one side, and the medium could have a natural twist in its taut state, like writhe.

This note works out what that proposal means for the E9 model: which term it adds, what that term needs, and what it would predict.

## 1. The term

Treat the three strands as one complex 3-vector ψ = (ψ₁, ψ₂, ψ₃). The chiral term is

  **E_c = γ ∫ ψ* · (D × ψ),  with D = ∇ − ieA.**

γ is a new coefficient. Its sign is the medium's handedness.

### 1.1 Properties

All five were checked numerically on a periodic 32³ grid with spectral derivatives (`chiral_term_checks.py`).

| Property | Statement | Check |
|---|---|---|
| Real | ∫ψ*·(∇×ψ) equals its own complex conjugate, by integrating the curl by parts. The gauge piece is real too: −ie A·(ψ×ψ*), and ψ×ψ* is purely imaginary. | Im/Re = 9×10⁻¹⁶ |
| Gauge invariant | D(e^{iα}ψ) = e^{iα}Dψ when A → A + ∇α/e. | relative difference 6×10⁻¹⁶ |
| Odd under parity | It is a pseudoscalar: under x → −x with ψ and A as vectors, E_c → −E_c. | ratio −1.0000000000000009 |
| Even under time reversal | ψ → ψ* leaves the integral unchanged (same integration by parts). | (analytic) |
| Director limit | For ψ = f e^{iθ} û with û a real unit vector, ψ*·(∇×ψ) = f² û·(∇×û). This is the cholesteric twist term of liquid crystals. | a helix of wavenumber q gives −q: −2.0000 for q = 2 |

So E_c is exactly the term that makes a liquid crystal cholesteric, and the analogue of the Dzyaloshinskii–Moriya term in chiral magnets [memory: Dzyaloshinskii 1958; Moriya 1960]. It is linear in the twist rate, so one sense of twist lowers the energy and the other raises it. That is "the charge favours a side", made precise.

## 2. What the term requires: strands locked to space

**In E9 as written, no such term is allowed.** The strand index is internal: spatial rotations act on x only. A rotation-invariant term linear in ∇ needs a second vector to contract ∂_j with, and the uniform vacuum supplies none. The ε_ijk in E_c contracts a strand index with a spatial index. It is rotation-invariant only if a spatial rotation also rotates the strand index.

**Adding E_c therefore forces a new assumption, A5: the three strands are locked to the three directions of space.** ψ becomes a vector order parameter, like a p-wave superfluid [memory: ³He-A; Volovik, *The Universe in a Helium Droplet*, 2003]. It needs exactly three strands in exactly three dimensions. With A5, the E9 model changes as follows. A5 is the price of the term, so these changes need to be faced directly.

### 2.1 The potential and Josephson terms become a crystal anisotropy

Σ_k ½(|ψ_k|² − 1)² and −η Σ_{i<j} Re(ψ_iψ_j*) are no longer internal symmetry terms. They depend on how ψ points relative to fixed spatial axes, so the medium is now a crystal, not an isotropic fluid.

The check script applies all 24 rotations of the cube to space and strands together:
- E_c and the potential are invariant under all 24.
- Potential plus Josephson is invariant under exactly **6**: the identity, the two 3-fold rotations about (1, 1, 1), and the three 2-fold rotations −(transposition). The three-strand vacuum picks out the body diagonal (1, 1, 1).

**So the locked E9 symmetry is the dihedral group D₃ about the (1, 1, 1) axis, plus U(1) gauge.**

### 2.2 What A1 becomes

A1 said "the strands are interchangeable". It becomes "the strands are interchangeable under D₃": cyclic permutations are 120° rotations about (1, 1, 1), and odd permutations are 180° flips, with the sign absorbed by the gauge.

The cyclic ℤ₃ still forces equal densities. **So the exact thirds of step 2 survive A5.** This connects to step 1's remark that a ℤ₃ cycling three lines would force equal densities.

### 2.3 New gradient terms become allowed

A vector order parameter admits separate stiffnesses for divergence, curl and cross terms, such as |∇·ψ|² and |∇×ψ|² (the analogue of the Frank constants K₁, K₂, K₃). The minimal model sets them to zero and keeps the isotropic Σ|Dψ_k|². This is a declared assumption, A6, not a derived one.

## 3. Ground state and the size of a twisted loop

### 3.1 Without pinning

The one-constant energy of a helix û = (cos qz, sin qz, 0) per unit volume is f²(q² − γq). This is minimal at **q₀ = γ/2**, with a gain of −f²γ²/4. A chiral medium with nothing pinning the director is twisted in its ground state, with pitch 2π/q₀. That is the author's "natural curvature in the taut state".

### 3.2 With pinning, which locked E9 has

The anisotropy of §2.1 pins û to the body diagonal. A uniform vacuum then survives for γ below a critical value γ_c set by the pinning strength (the potential and η). Above γ_c the vacuum becomes helical. **γ_c has not been computed.** It is a 1D calculation and should be done first.

### 3.3 Why the regime below γ_c is the interesting one

Below γ_c the vacuum is uniform, and the chiral term acts only on textures. This is exactly how chiral magnets host isolated skyrmions [memory: Bogdanov and Yablonskii 1989]. Under a size change L, the energy of a texture has three pieces:

| Piece | Scales as |
|---|---|
| Gradient and magnetic energy | L |
| Chiral energy (favourable handedness) | −L² |
| Anisotropy (potential + Josephson) | L³ |

E(L) = aL − bL² + cL³ has a minimum at finite L when b² > 3ac. **The locked anisotropy supplies the term that stops growth.** That closes the gap noted in the chat (the chiral term alone pushes loops to grow) at the level of scaling. Whether it holds for an actual twisted loop is what a run would test.

## 4. Screening

This was the obstacle for the four-derivative term. It splits cleanly here.

ψ*·(D×ψ) = ψ*·(∇×ψ) − e A·S, where **S = iψ×ψ*** is real. S vanishes when ψ points along a real direction (times an overall phase), and is non-zero for "complex" textures such as p + ip.

- **Director (real) textures: S = 0.** The term is f² û·(∇×û). It acts on the neutral director, which the supercurrent does not couple to, since the current couples to the overall phase. **Not screened at leading order.**
- **Complex textures: S ≠ 0.** A couples linearly to S, which adds a source γeS to Ampère's law. Its effect, screening, enhancement or neither, is **not known.** Noncentrosymmetric superconductors have related Lifshitz terms that produce helical phases [memory: Kaur, Agterberg and Sigrist, PRL 94, 137002 (2005)], so this needs checking against that literature.
- **Consequence for the twist.** E9's twist N lives in relative phases, a complex texture, so S ≠ 0 there. But the director field alone carries a Hopf charge too (π₃ of the director space is ℤ). Hopfions made purely of a twisted director exist in chiral liquid crystals [memory: Ackerman and Smalyukh, PRX 7, 011006 (2017)]. **A twisted loop realized in the director (S = 0) sector would sidestep the screening question entirely.** That is a reason to prefer it as the first configuration.

## 5. The built-in control: parity

Because E_c is odd under parity, the twisted loop with charge +N and its mirror image −N must have different energies. With γ in the favourable window, one handedness can be stable while the other collapses. **That is a prediction, not an input.** If a run finds equal behaviour for ±N, the chiral term is not doing the work. It plays the role the no-vortex passenger control played for the vorton.

## 6. What a torus-dual unit model would have to supply

The term is legitimate, not tuned, only if a model of the medium's units fixes the following. Each item says what the unit model must produce.

1. **The locking (A5).** The units need an orientation that ties the three strand directions to the three axes of space. Without that, E_c is not allowed at all (§2).
2. **A net handedness: the sign of γ.** In the 3-sphere picture, the Heegaard splitting into two solid tori, and the Hopf fibres threading them, comes in left- and right-handed versions. A medium of such units has a chirality only if one version dominates. A racemic mix gives γ = 0.
3. **The magnitude of γ relative to the stiffness and the pinning.** This sets the pitch q₀ξ and the ratio γ/γ_c. If the unit model fixes γ/γ_c, the run becomes a single prediction (stable or not at that value) instead of a scan.

**If no unit model fixes these, γ is a free parameter and A5 is a declared assumption.** Any run is then an exploration of the chiral-medium class, not a derivation.

## 7. What is and is not established

**Established:**
- The form of the term and its five properties (checked numerically).
- That it requires locking (A5).
- That under locking the E9 symmetry is D₃ × U(1), and the thirds survive.
- The helix pitch q₀ = γ/2 in the unpinned one-constant case.

**Not established:**
- γ_c.
- The screening effect for complex textures.
- Whether any twisted loop is stable.
- Any unit model that fixes γ.
- All literature claims, which are [memory].

**Assumptions introduced:**
- A5 (locking).
- A6 (one-constant stiffness).
- γ as a coefficient.

The original A1 is reinterpreted, and A2 (no extra stabilizer) is superseded if this route is taken.

## 8. Proposed order of work

1. **γ_c.** A 1D calculation: the uniform locked vacuum against a helix, with the E9 potential and Josephson term at η = 0.1 and η = 0. Cheap.
2. **Screening check.** A 1D or straight-string calculation of the A·S coupling for a complex texture. Also cheap.
3. **Only then, a pre-registration** for a twisted loop in the director sector, with γ ∈ (0, γ_c). It would include:
   - a scan rule fixed in advance,
   - the ±N parity control,
   - the Derrick balance check: at a true minimum, the quadratic, chiral and anisotropy energies must satisfy the scaling identity, the way the virial cross-check worked in Phase 0.
4. **In parallel, the unit model:** whether torus-dual units can supply A5, a net handedness and a definite γ. This is the step that would turn the term from a choice into a consequence.

No particle identification is made or implied.
