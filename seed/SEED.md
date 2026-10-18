# Seed — a taut vacuum and its folds

*Started October 16, 2026, from the taut-medium thread. A clean start: no substrate, no ledger, no gates. Anything here can be renamed, dropped or replaced. T-numbers point to the thread in the October 16 exploration note.*

## In plain language

Space is taut. Its ground state has a tension equal to its energy density, and a vacuum like that looks the same to every observer: there is no rest frame to measure against. Light rides it on one cone, at one speed, at every energy. Matter is a fold: the field wrapped around its internal space in a way that can't come undone, because the number of wraps is conserved. Concentrate enough energy in one place and the field folds, always as a fold and an antifold together. The 60° wallpaper is real, but it is rolled up inside every point instead of laid out across space. Gravity is the cone itself, bent by the energy it carries, and everything rides the bent cone.

## 1. Five commitments

1. **One cone.** Everything (the field that makes matter, light, gravity) follows the same relativity. The vacuum is the ground state, so its stress-energy is T_μν ∝ g_μν: taut (p = −ρ) and the same in every frame. *(T-3)*
2. **The geometry is internal.** The field takes values in an internal space, and that is where the 60° lives. Spacetime stays smooth. *(T-7)*
3. **Matter is a fold.** A particle is a finite-energy configuration that wraps the internal space. The wrap number is an integer that smooth motion can't change, so the fold is locked. Folds are the sources. *(T-2, T-8)*
4. **Charge is dressed, not slowed.** A fold polarizes the vacuum around it, so its effective charge depends on how closely you look. None of that picks a frame or slows light. *(T-6)*
5. **Gravity is the cone.** All fields share one metric. Energy bends it; everything rides it. *(T-9)*

## 2. What comes free

Given 1–5, these hold with no tuning:

- **One speed.** Every massless signal shares the cone: light, gravitational waves, anything else massless.
- **No vacuum dispersion.** Light of every energy crosses empty space at the same speed.
- **Equivalence principle.** Everything falls the same way, because everything couples to the same metric.
- **Conserved matter.** The fold number is topological, so it can't drift.
- **Pairs.** A fold appears only with an antifold, so the threshold is twice the lightest fold's energy. Nature does this with light: two photons can become an electron and a positron (Breit–Wheeler, 1934). It was measured at RHIC in 2021, using the photons that surround passing gold nuclei.
- **Spin ½ from a spinless field.** A fold can be a fermion, but the internal space decides how, and whether. For SU(2), and for the S² of the knot models, turning a fold once around traces a loop that can't be shrunk away (π₄ = ℤ₂). Finkelstein and Rubinstein (1968) proposed this reading, with the spinor fields of textbooks as point-limit stand-ins for kinks of a nonlinear field. For SU(3) the loop does shrink (π₄ = 0); there the Wess–Zumino term supplies the sign instead, and the fold is a fermion when the number of colors N_c is odd (Witten 1983). For G₂ neither route exists: π₄ = π₅ = 0 (Mimura 1967), so there is no such loop and no Wess–Zumino term, and a G₂-valued field alone makes only bosonic folds.

## 3. The 60° lives inside

Moved from space to the internal space, the hexagon costs nothing (no frame, no dispersion), and the mathematics already has it. The torus and group computations below are checked by `hexagon_check.py`; the rest is cited.

- **SU(3)'s flat part is a hexagonal torus.** SU(3) is the color group and the group of the eightfold way. Its diagonal elements form a flat 2D surface that closes up like a doughnut, and that surface is the plane modulo the hexagonal lattice: a 60° wallpaper rolled into a torus. Its weights sit on a hexagonal lattice too, which is why the eightfold way's multiplets are hexagons (the octets) and a triangle (the decuplet).
- **The Császár torus is drawn on it.** Let ζ = e^{2πi/7} and D = diag(ζ, ζ², ζ⁴), an element of SU(3). Its seven powers are seven points on the torus, and the finer hexagonal lattice through them cuts the torus into the 7-vertex triangulation:
  - every point joined to every other (K₇);
  - 14 triangles in two families of 7;
  - each family a Fano plane, one of them exactly the octonion lines {i, i+1, i+3}. That match is guaranteed rather than lucky: only two Fano planes on the labels 0–6 survive x ↦ x+1, and the two families are exactly those, so labeling the points by powers of D always makes one family the octonion lines.
- **The 120° turn gives the order-21 group.** SU(3)'s 120° Weyl rotation moves the seven points as x ↦ 4x. Together with D it generates ℤ₇⋊ℤ₃ (order 21) inside SU(3). In this labeling the group preserves both Fano families, so it is the collineation F₂₁, not the label-only one.
- **PSL(2,7) holds it, still inside SU(3).** Klein's group of order 168, the symmetry group of the Klein quartic, is PSL(2,7) acting on three complex dimensions. It is the only simple subgroup of SU(3) with a complex three-dimensional irreducible representation: the only other non-abelian simple one is A₅, whose triplets are real (Luhn, Nasri & Ramond 2007). The order-21 group is one of its maximal subgroups (ATLAS: Conway et al. 1985). One labeling detail: Klein's own matrices contain diag(ζ⁴, ζ², ζ), not D. The copy that holds this seed's ⟨D, 120° turn⟩ is Klein's group conjugated by swapping the first and third coordinates (with a sign, to stay in SU(3)), and it preserves the mirror quartic xy³ + yz³ + zx³. Flavor model-builders have used both groups as family symmetries for three generations.
- **G₂ sits above.** G₂, the symmetry group of the octonions, contains SU(3) as the subgroup fixing one imaginary octonion (Günaydin & Gürsey 1973). Its mirror pattern (the affine Weyl group) is exactly the wallpaper group p6m. SU(3)'s own Weyl group has only the 120° turns and three mirrors; G₂'s, of order 12, adds turns by 60°, 180° and 300°. Those turns keep the seven points (x ↦ 5x, 6x, 3x) but swap the two Fano families, and no mirror in either group keeps the seven points at all.

So p6m, the octonions, the Fano plane, F₂₁ and PSL(2,7) all live in the internal space, with no frame anywhere, but they don't stack into one clean tower: F₂₁, PSL(2,7) and the split into two Fano families belong to the SU(3) rung, and the turns that complete p6m arrive with G₂ and swap the families. The seed doesn't have to pick a rung yet. One reading to try: SU(3) or G₂ as the field's internal space, with PSL(2,7) ⊃ F₂₁ acting on three generations. G₂ comes with two costs: its extra turns swap the Fano families, and a G₂-valued field alone makes only bosonic folds (§2).

## 4. The fold

- **Counting wraps.** Finite energy forces the field to settle to one value far away, so space behaves like a closed 3-sphere. A fold maps that sphere into the internal space, and the number of wraps is an integer:
  - point-like folds: π₃ of the internal space, which is ℤ for SU(3), for G₂ and for every simple compact Lie group;
  - monopoles: π₂ of the vacuum space. The evening started here. Whether the seed has magnetic monopoles depends on how the internal symmetry breaks; a theory that unifies the forces in one simple group always has them;
  - knots: the Hopf number, π₃(S²) = ℤ.
- **The Gaussian envelope.** A small, spread-out packet is linear and passes through. Pile in enough energy and the nonlinear terms take over: the packet can fold into a fold–antifold pair. In one dimension this has been seen in simulations. In φ⁴, colliding trains of small pulses of the field itself make kink–antikink pairs over a wide range of settings, most easily at low speed (Dutta, Steer & Vachaspati 2008). A later setup collides Gaussian packets of a second field that reaches the kink field only through a quantum go-between; wide, energetic, slow packets work best, and without the go-between no kinks form (Albayrak & Vachaspati 2023). Its follow-up in two space dimensions, which makes vortices, finds no sharp threshold: production is fractured across packet height and speed, with gaps even at high energy (Albayrak & Vachaspati 2026).
- **Holding it together.** In three dimensions a static fold can't be held by gradient energy alone (Derrick 1964); it would shrink or spread. Something has to push back: a four-derivative stiffness term (Skyrme), a gauge field, or an internal rotation (Q-balls). That choice is the first real design decision.
- **Efficiency.** In knot models the energy has a floor that grows more slowly than the charge, E ≥ c|Q|^{3/4} (Vakulenko & Kapitanskii 1979). A floor alone doesn't make the energy grow slowly, but the 3/4 power is known to be the right one, and the computed minima agree (Sutcliffe 2007). Bigger folds store charge more cheaply, and the lowest-energy shape at each charge is a definite knot or link; at Q = 7 it is a trefoil (Battye & Sutcliffe 1998, confirmed by Sutcliffe 2007). That is your organizing idea in standard form: a structure lasts when it stores energy efficiently enough.

## 5. Gravity

- Put every field on one dynamical metric. A massless spin-2 field coupled consistently to all energy turns out to be general relativity (Weinberg 1964; Deser 1970). The cone bending under energy is GR.
- Read as optics, a mass makes the vacuum act like a medium with index n ≈ 1 + 2GM/(rc²). Light bends and is delayed, and every other signal rides the same bent cone. That is T-9, and it is already true.
- The taut vacuum's tension is a cosmological constant. The real vacuum is nearly taut: dark energy has p ≈ −ρ, though DESI's 2025 data prefer a slow drift: 3.1σ from BAO and the CMB, and 2.8–4.2σ once supernovae are added, depending on the sample. Not yet decisive. Why the tension is so small is open.

## 6. Three starter models

Each is a known theory with known answers, so the first runs calibrate the tools. Then you change things.

**A. A fold in one dimension** (laptop, minutes). φ⁴ theory in 1+1 dimensions:

    𝓛 = ½(∂ₜφ)² − ½(∂ₓφ)² − (λ/4)(φ² − v²)²

The potential has two vacua, φ = ±v; a kink is the field stepping from one to the other. Collide two Gaussian packets and map when a kink–antikink pair forms, and when it doesn't. The closest single-field result to calibrate against uses trains of small pulses rather than single packets (Dutta, Steer & Vachaspati 2008).

**B. The hexagon from a fold** (3D). The SU(3) Skyrme model, with U(x) ∈ SU(3):

    𝓛 = (F²/16) Tr(∂_μU ∂^μU†) + (1/32e²) Tr([U†∂_μU, U†∂_νU][U†∂^μU, U†∂^νU]) + Wess–Zumino term

The first term is stretching energy; the second is the stiffness that stops the fold collapsing; the Wess–Zumino term gives the fold its fermion quantum numbers. The fold is the hedgehog, with wrap number 1. Quantize its rotations and the lowest states fill the octet (hexagon) and the decuplet (triangle) (Guadagnini 1984). F sets the units and e is the only pure number, so every prediction is a ratio. With exact SU(3), though, every member of the octet has one mass and every member of the decuplet another; the splittings inside them (Guadagnini's mass formulae) need a symmetry-breaking term for the heavier strange quark, which brings in more parameters. For nucleons the model lands within roughly 30% (Adkins, Nappi & Witten 1983).

**C. Knots** (3D). The Faddeev–Hopf model: a unit 3-vector field n(x) with a four-derivative term. Folds carry Hopf number; the lowest are rings, and Q = 7 is a trefoil. The natural output is the energy ladder E_Q/E₁.

## 7. First things to try

1. Run A. Watch a fold form, and map where pairs form against packet width, height and speed. The boundary may be ragged rather than one clean threshold (§4).
2. Reproduce B's octet and decuplet. Then swap the internal space and see what multiplets come out:
   - a G₂-valued field (its folds can only be bosons; see §2);
   - the flag space SU(3)/T², whose image under the moment map is a hexagon. It has two independent wrap numbers in the plane (π₂ = ℤ²) and one knot number in space (π₃ = ℤ).
3. Give the order-21 group a job. Let it act on three copies of a fold, three generations, and see which couplings it allows.
4. Add light. Gauge a U(1) inside the internal symmetry, read off the folds' electric charges, and confirm the photon's single cone.
5. Add gravity to one fold: a self-gravitating skyrmion.

## 8. Where it has to grow

These aren't tests. They are the places a theory of everything has to reach.

- Which folds are which particles: leptons, quarks, three generations?
- Size. The electron looks pointlike down to very short distances. How can a fold be that small yet that light? A fold is a classical shape only when it is larger than its own Compton wavelength, ħ/mc. The proton is (charge radius 0.84 fm against 0.21 fm). The electron misses by at least 10⁵: its Compton wavelength is 386 fm, and no size shows down to about 10⁻³ fm. So this item and the next point the same way, toward a strongly coupled fold sector.
- Coupling. In weakly coupled theories, folding a few quanta into a pair is exponentially rare; in nature, electron pairs form readily. That points to a strongly coupled fold sector, the way baryons are in QCD.
- Why is the vacuum's tension so small, and does it drift?
- Is the 60° chosen, or does it fall out of something deeper?
- Can light and the cone themselves be built from the field? Weinberg and Witten (1980) map where that's hard.

## 9. Neighbors

People who walked nearby. Borrow freely.

- Breit & Wheeler (1934). Collision of two light quanta. *Phys. Rev.* 46, 1087.
- Skyrme (1961). A nonlinear field theory. *Proc. R. Soc. A* 260, 127.
- Derrick (1964). Why static solitons need something extra. *J. Math. Phys.* 5, 1252.
- Weinberg (1964). Massless spin-2 couples universally. *Phys. Rev.* 135, B1049.
- Mimura (1967). The homotopy groups of Lie groups of low rank (π₄(G₂) = π₅(G₂) = 0). *J. Math. Kyoto Univ.* 6, 131.
- Finkelstein & Rubinstein (1968). Connection between spin, statistics, and kinks. *J. Math. Phys.* 9, 1762.
- Deser (1970). Self-interaction and gauge invariance. *Gen. Rel. Grav.* 1, 9.
- Günaydin & Gürsey (1973). Quark structure and octonions. *J. Math. Phys.* 14, 1651.
- Vakulenko & Kapitanskii (1979). The Hopf-charge energy bound. *Sov. Phys. Dokl.* 24, 433.
- Weinberg & Witten (1980). Limits on which massless particles can be composite. *Phys. Lett. B* 96, 59.
- Witten (1983). Skyrmions from QCD; the Wess–Zumino term. *Nucl. Phys. B* 223, 422 and 433.
- Adkins, Nappi & Witten (1983). Static properties of nucleons in the Skyrme model. *Nucl. Phys. B* 228, 552.
- Guadagnini (1984). Baryons as solitons and mass formulae. *Nucl. Phys. B* 236, 35.
- Conway, Curtis, Norton, Parker & Wilson (1985). *ATLAS of Finite Groups.* Oxford University Press. L₂(7) on p. 3: maximal subgroups S₄, S₄ and 7:3.
- Faddeev & Niemi (1997). Stable knot-like structures in classical field theory. *Nature* 387, 58.
- Battye & Sutcliffe (1998). Knots as stable soliton solutions. *Phys. Rev. Lett.* 81, 4798.
- Manton & Sutcliffe (2004). *Topological Solitons.* Cambridge University Press. The textbook.
- Luhn, Nasri & Ramond (2007). Simple finite non-Abelian flavor groups (PSL(2,7) inside SU(3)). *J. Math. Phys.* 48, 123519. Also ℤ₇⋊ℤ₃ as a family symmetry, *Phys. Lett. B* 652, 27.
- Sutcliffe (2007). Knots in the Skyrme–Faddeev model (the 3/4 power is optimal; Q = 7 is a trefoil). *Proc. R. Soc. A*, doi:10.1098/rspa.2007.0038.
- Dutta, Steer & Vachaspati (2008). Creating kinks from particles. *Phys. Rev. Lett.* 101, 121601.
- Gillard & Gresnigt (2019). Three fermion generations with two unbroken gauge symmetries from the complex sedenions. *Eur. Phys. J. C* 79, doi:10.1140/epjc/s10052-019-6967-1.
- STAR Collaboration (2021). Breit–Wheeler pairs from photon collisions. *Phys. Rev. Lett.* 127, 052302.
- Albayrak & Vachaspati (2023). Creating kinks with quantum mediation (Gaussian packets of a second field). *Phys. Rev. D* 109, 036001; arXiv:2308.01962.
- DESI Collaboration (2025). DR2 Results II: BAO measurements and cosmological constraints. arXiv:2503.14738.
- Albayrak & Vachaspati (2026). Production of global vortices with quantum mediation. arXiv:2603.10115.

## Words

- **taut vacuum** — the ground state: p = −ρ, the same in every frame.
- **cone** — the light cone, the one speed every massless signal shares.
- **fold, antifold** — a particle and its opposite: field configurations held by a conserved wrap number.
- **wrap number** — the topological charge, an integer.
- **internal space** — where the field takes its values; home of the 60°.
