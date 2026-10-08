# A4 — The surviving gravity entries: result

**Plain-language summary.**
- **§2.89 is downgraded.** It says a small object is "decoupled" from a gravitational bowl much larger than itself, because the bowl is locally flat at its scale.
  - "Flat" means no curvature. It does not mean no slope. A flat slope still pulls.
  - Neutrons, atoms and antihydrogen are all measured falling in Earth's field. Earth's bowl is at least 10¹⁶ times larger than any of them.
  - What survives is the tidal-only version: a bowl that is flat at the object's scale gives it no tides. That is ordinary physics, not an SQT result.
- **§2.90 is downgraded.** It says knots pull on the tensioned lattice, and that this static tension pattern is gravity, falling off as 1/r².
  - In an elastic medium, isolated point defects that only push or pull locally do not attract each other at all (Eshelby 1956). Non-spherical ones interact as 1/r³, and that interaction averages to zero over orientations.
  - A 1/r² force needs each body to exert a net force on the medium. A knot embedded in a closed lattice cannot.
  - Uniform tension does not change this.
  - The ledger offers no mechanism that escapes it. The 1/r² claim is withdrawn, and the mechanism drops from R2 to R3.
  - The conflict with the cosmological constant also still stands.
- **A standing kill condition, KC-EP, is now in force.** Every gravity mechanism must make everything fall the same way, to about one part in 10¹⁵ (MICROSCOPE).
  - §2.90 fails it as written. Its own rule says energy without topology produces no pull, so nuclear binding energy would not fall. That breaks the bound by 11 orders of magnitude.
  - §2.89 fails it too, because its response depends on the object's size.
  - The Bjerknes mechanism (§2.88) has not shown that it passes.

**Pre-registration.** `A4_PREREG.md` md5 `7b876a2720da53884933b0a512ca8df8`, locked by commit 08d6295 before any A4 computation file existed.

**Checks.** `a4_checks.py` (md5 in `MANIFEST.md5`) writes `a4_output.txt` and `a4_results.json`, using sympy for the symbolic checks.

**Second leg.** None, per the prereg: no new number or derivation decides an A4 verdict.

## DR-A4-1. §2.89: the pull versus the tides — DOWNGRADE

**Text test.** The claim covers the pull. §2.89 says the bowl's "gradient is negligible; the object is effectively decoupled from that bowl", and that "a subatomic particle near a proton does not respond to a planet-scale bowl because that bowl is locally flat at the particle's scale". That treats flatness (no curvature) as if it meant no gradient.

**Observational test.** In Earth's field, R_bowl/d_obj is at least 10¹⁶ for every one of these, and each feels Earth's pull:
- neutrons: Colella–Overhauser–Werner 1975, gravitationally induced interference;
- ultracold neutrons in quantized states above a mirror: qBounce, Jenke et al. 2011. Those states exist only because the neutron feels mg;
- atoms: Peters, Chung & Chu 1999, who measured g by dropping atoms;
- antihydrogen: ALPHA-g 2023.

**Verdict: DOWNGRADE.** The scale-filtered-locality claim (R2) is withdrawn as stated, because it is falsified for the pull.
- *Tidal-only restatement, recorded as standard physics with no SQT register.* A bowl that is flat at an object's scale exerts a uniform pull on it and negligible tides; in the object's freely falling frame only the tides remain. This is the Newtonian equivalence-principle decomposition.
- *The nesting paragraph* ("larger enclosing bowls contribute a nearly flat background offset") is true only in that form: relative to the inner body's free fall, not as an absence of pull.
- *The pressure-source question* stays §2.89's named M.BRIDGE gap. Note also that a fluid at rest with no body force or flow has ∇p = 0, so even the "bowl" itself has no stated mechanism.

## DR-A4-2. §2.90 against Eshelby — DOWNGRADE

**Symbolic checks** (standard results, re-derived; all as expected):

| Check | Result |
|---|---|
| (a) Centre of dilatation, 3D, u = C x/r³ | tr ε = 0 off the core; it solves the Navier equation. So the interaction energy with a second centre of dilatation is W = −P tr ε = **0** (Eshelby) |
| (a) Centre of dilatation, 2D, u = C x/ρ² | tr ε = 0, so again no interaction |
| (a′) Two tetragonal force dipoles (Kelvin Green's function, verified to solve Navier) | W(λx)/W(x) = **λ⁻³**. The isotropic limit is 0, and the orientation average is **0** |
| (b) Monopole–monopole | W ∝ **1/r**, the only 1/r term. It needs net forces F₁ and F₂ ≠ 0 on the medium. Monopole–dipole goes as 1/r² |
| (c) Uniform tension T (geometric stiffness: μ → μ + T) | The dilatation field still solves the prestressed Navier equation, and the Green's function stays homogeneous of degree −1. So (a)–(b) are unchanged |

**Text search for an escape.**
- §2.90's source is a knot that "forces some lattice threads shorter/tighter". Such a source is self-equilibrated: the lattice is closed, so there is no net force on it and no monopole.
- Its shell-counting step ("shells … ~4πr² ⇒ per-area perturbation ~1/r²") assumes a conserved monopole flux. The total force flux through any shell around a self-equilibrated defect is zero.
- The knots' declared coupling, the density deficit ε of the Branch-C annex, is a dilatation-type source. That is case (a).
- The only monopole-type source in the ledger is the pulsating (Bjerknes) volume source of §2.88. It is dynamic and needs a propagating channel, which §2.90 explicitly disowns ("needs no propagating channel").
- No escape is on record.

**Verdict: DOWNGRADE.**
- (i) "1/r² (R2; geometric)" is **withdrawn**. In linear elasticity, uniformly tensioned or not, self-equilibrated defects have zero interaction (isotropic dilatation) or one falling as 1/r³ with zero orientation average.
- (ii) The mechanism "tension redistribution = gravity" goes from **R2 to R3**. Restoring it requires a derivation of two things:
  - a monopole source of a field that couples universally (KC-EP);
  - the 1/r law itself.
- (iii) **I4 annotation, owed since M.CW-c.** The 1/r² was never import-free. Its exponent is the declared import I4 (§2.88.E: three propagating dimensions; in 2D the law is 1/r). So §2.90's "no new assumption beyond the existing axioms" is corrected.
- (iv) **VC-B annotation, owed since V4.66.**
  - Under VC-B, knots are composite objects embedded in the envelope bath, not defects of the lattice's own condensed field.
  - "Permanent topological constraint (not removable without cutting)" also meets A3: the linking is unprotected, and cutting (reconnection) is available.
- (v) **The Λ conflict stands, recorded and not resolved.** "Uniform tension ⇒ no gravity" has two horns:
  - If the tensioned lattice's uniform stress gravitates, as uniform stress-energy does in any metric theory, it acts as vacuum energy. A network of tensioned threads or sheets has w = −1/3 or −2/3 (Bucher & Spergel 1999), not the w ≈ −1 of the observed dark energy, and at a Planck-scale lattice its energy density is about 10¹²⁰ times too large.
  - If it does not gravitate, that needs a mechanism (for example, self-tuning à la Klinkhamer–Volovik), and none is on record.

## DR-A4-3. KC-EP — declared; it FIRES for §2.89 and §2.90, and is UNMET for §2.88

**Declaration** (standing, folded into the Preamble and §2.91.D).
- Any gravity mechanism kept or proposed must *derive* that free-fall acceleration does not depend on composition, at the MICROSCOPE level: η(Ti, Pt) = [−1.5 ± 2.3 (stat) ± 1.5 (syst)] × 10⁻¹⁵, so |η| < 7 × 10⁻¹⁵ at about 2σ.
- If a fraction f_X of each body's mass couples with strength (1 + δ_X), then η ≈ δ_X Δf_X. For Ti against Pt (Z/A and the semi-empirical mass formula, to order of magnitude):

| Component | f(Ti) | f(Pt) | Δf | Bound on δ_X |
|---|---|---|---|---|
| electrons (the ledger's own ε_e) | 2.5×10⁻⁴ | 2.2×10⁻⁴ | 3.3×10⁻⁵ | **< 2×10⁻¹⁰** |
| nuclear binding energy | 9.5×10⁻³ | 8.5×10⁻³ | 9.1×10⁻⁴ | **< 8×10⁻¹²** |
| electrostatic (Coulomb) energy | 2.0×10⁻³ | 4.1×10⁻³ | 2.0×10⁻³ | **< 3×10⁻¹²** |
| neutron excess (A − 2Z)/A | 0.081 | 0.200 | 0.12 | **< 6×10⁻¹⁴** |

**Application to the mechanisms on record:**

| Mechanism | Coupling as stated | KC-EP |
|---|---|---|
| §2.89 static bowl | "volume displacement … not a force acting on mass"; the response depends on the object's scale | **FIRES**: the response differs at O(1) between a neutron, an atom and a test mass in the same field |
| §2.90 static tension | "Transient oscillation, no topology: zero"; the deficit scales "with knot complexity"; aggregates are "additive at large r" | **FIRES**: non-topological field energy carries no deficit, so binding energy would not gravitate. η(Ti, Pt) ≈ Δf_binding ≈ 9×10⁻⁴, which is 10¹¹ times the bound |
| §2.88 Bjerknes / CM-3 | "knots contribute response amplitude only" (CM-2); CM-3 staged | **UNMET**: universality is not derived. KC1(b) already covers composition-dependent dipole radiation |
| §2.91 longitudinal bridge | retired at V4.67 (KC3) | not applicable |

## Blast radius (annotated in the Phase A fold)

1. **§2.89:** DOWNGRADED, with the tidal-only restatement, KC-EP fires, and the bowl-mechanism note.
2. **§2.90:** DOWNGRADED (1/r² withdrawn; R2 → R3), with the I4 annotation, the VC-B annotation, the Λ conflict standing, and KC-EP fires.
3. **§2.88 (§2.88.C CM-3 / What-not-claimed):** KC-EP unmet.
4. **§2.91.D:** KC-EP added as a standing kill condition.
5. **Preamble:** KC-EP recorded as a standing rule, after M.BRIDGE.
6. **Not ledger entries:** Paper IIA / II-B text (Phase B or later) and STATUS.md.

## Honesty items

- **H-A4-1 (sources).** The four free-fall measurements were confirmed by bibliographic search only; their full texts were not fetched. The verdict uses only their qualitative content: each object falls with Earth's g. MICROSCOPE's η was quoted from its fetched abstract.
- **H-A4-2 (scope).** The KC-EP sensitivities are order-of-magnitude illustrations (semi-empirical mass formula; standard atomic weights). No verdict depends on their second digit.
