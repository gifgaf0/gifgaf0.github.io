# A4 — The surviving gravity entries: pre-registration

**Plain-language summary.** Two ledger entries still describe gravity without waves.
- **§2.89** says an object feels a gravitational "bowl" only when the bowl is about its own size; a much larger bowl is "locally flat" and the object is "decoupled".
- **§2.90** says a knot pulls on the tensioned vacuum lattice, and that this static redistribution of tension *is* gravity, falling off as 1/r².

This file fixes, before any check, how three questions will be decided:
1. Does §2.89 claim that small objects feel no pull from large bowls? If so, what do falling neutrons and atoms say?
2. Can static tension in an elastic lattice produce a 1/r² attraction between two embedded defects? Classical elasticity (Eshelby) says isolated point defects do not attract at all.
3. What standing test must any gravity mechanism in the program pass? The weak equivalence principle requires that everything falls the same way. MICROSCOPE checked this to about one part in 10¹⁵.

**Lock.** Locked by its md5 in `A4_LOCK.txt` and by the commit that adds it, before any A4 computation file exists. Corrections go in dated addenda.

**Base.** V4.91, md5 `ce9ca6873adb5686227f5d103b41e3cc`. Objects of record:
- §2.89 (L1546–L1574);
- §2.90 (L1576–L1594);
- §2.88.E's import I4 (L1542);
- §2.91.D's kill set (L1606);
- the VC-B annex (L253), whose transfer annotations are "due on §2.90/Paper VII framing at their next touch";
- the M.CW note that §2.90's 1/r² is an "admissible incidence relation + the I4-imported exponent (§2.88.E)".

**External anchors.**
- **MICROSCOPE:** Touboul et al., Phys. Rev. Lett. 129, 121102 (2022), "η(Ti,Pt) = [−1.5 ± 2.3(stat) ± 1.5(syst)] × 10⁻¹⁵" (abstract fetched October 7, 2026).
- **Free fall of microscopic objects in Earth's field** (titles and bibliographic data confirmed by search, October 7, 2026):
  - Colella, Overhauser & Werner, Phys. Rev. Lett. 34, 1472 (1975), gravitationally induced neutron interference;
  - Jenke, Geltenbort, Lemmel & Abele, Nature Phys. 7, 468 (2011), gravity-resonance spectroscopy with ultracold neutrons (qBounce);
  - Peters, Chung & Chu, Nature 400, 849 (1999), g measured by dropping atoms;
  - ALPHA Collaboration, Nature 621, 716 (2023), gravity's effect on antihydrogen.
- **Elasticity:** Eshelby, "The continuum theory of lattice defects", Solid State Physics 3, 79 (1956).
- **Tensioned networks:** Bucher & Spergel, Phys. Rev. D 60, 043505 (1999), quoted in the October 4 Phase 2 report: a network of tensioned strings or walls has w = −1/3 or −2/3, never −1.

## Decision rules

**DR-A4-1 (§2.89: the pull versus the tides).**
- *Text test.* Does §2.89's load-bearing R2 claim assert that an object does not respond to (feels no pull from) a bowl whose radius greatly exceeds the object's scale, or only that it feels no tides from it?
- *Observational test.* Do microscopic objects feel Earth's full pull? Here the ratio R_bowl/d_obj is 10¹⁶ or more. The measurements are the neutron (COW; qBounce, whose quantized states exist only if the neutron feels mg), atom (Peters–Chung–Chu) and antihydrogen (ALPHA-g) results above.
- *Rule.*
  - If the text asserts decoupling of the pull and the measurements show the pull: **DOWNGRADE**. The scale-filtered-locality claim (R2) is withdrawn as stated, falsified for the pull. Record the tidal-only restatement: a bowl that is flat at the object's scale exerts a uniform pull and negligible tides, and in the object's freely falling frame only the tides remain. That is the standard Newtonian and equivalence-principle decomposition, so it is recorded as standard physics with no SQT register. The nesting paragraph survives only in that form.
  - If the text asserts only tidal response: annotate it "tidal-only; standard" and do not downgrade.

**DR-A4-2 (§2.90 against Eshelby).**
- *Computation* (standard results, re-derived symbolically as a check):
  - (a) Isotropic linear elasticity: the field of a centre of dilatation is u = C x/r³, and tr ε = 0 outside its core, so the interaction energy with a second centre of dilatation is W = −P tr ε = 0. For general force dipoles, W ∝ ∂²G with G ∝ 1/r, so W ∝ 1/r³.
  - (b) A 1/r interaction energy (1/r² force) needs both objects to exert a net force (a monopole) on the medium. A defect embedded in a closed lattice is self-equilibrated, so it exerts none.
  - (c) Linearising about a uniformly tensioned state gives an operator of the same order: its Green's function is ∝ 1/r in 3D and ∝ ln r in 2D. So the scalings in (a) and (b) are unchanged.
  - (d) §2.90's shell-counting step ("per-area perturbation ~1/r²") presupposes a conserved monopole flux.
- *Text search.* Does §2.90, or any entry it cites, supply a non-elastic or nonlinear source with a nonzero monopole?
- *Rule.* If (a)–(d) hold and the ledger supplies no such source: **DOWNGRADE** §2.90.
  - (i) Its "1/r² (R2; geometric)" claim is withdrawn, as contradicted by linear elasticity.
  - (ii) The mechanism "tension redistribution = gravity" goes from R2 to R3. Restoring it requires, stated as a derivation: a monopole source of a field that couples universally (KC-EP below), and a derived 1/r law. The exponent itself is the declared import I4.
  - (iii) Attach the owed I4 and VC-B transfer annotations.
  - (iv) Record the Λ conflict as standing. "Uniform tension ⇒ no gravity" is in tension with uniform vacuum stress gravitating in any metric theory; a tensioned network has w = −1/3 or −2/3.
- If the ledger does supply a monopole source, record it and do not downgrade.

**DR-A4-3 (KC-EP, the standing equivalence-principle kill condition).**
- *Declaration.* Any gravity mechanism kept or proposed in the program must derive that free-fall acceleration is independent of composition, at |η| of about 10⁻¹⁵ (MICROSCOPE). It must cover:
  - the electrons, which carry their own coupling ε_e in the ledger;
  - nuclear binding and electrostatic energy, which are not knots;
  - the neutron excess.
- *Sensitivities* for the Ti/Pt pair, to order of magnitude: computed in-script from Z/A and the semi-empirical mass formula.
- *Application now,* to each gravity mechanism on the record:
  - §2.88 (Bjerknes, CM-3);
  - §2.89;
  - §2.90;
  - the §2.91 longitudinal bridge (retired at V4.67).
- *Classes:*
  - **FIRES**, if the stated coupling is explicitly non-universal at O(1) (it depends on an object's size, topology or knot type rather than its total mass-energy);
  - **UNMET**, if there is no derivation either way;
  - **MET**, if universality is derived.
- *Rule.* FIRES withdraws the mechanism's gravity claim on this ground as well. UNMET is annotated "no promotion until derived". KC-EP is recorded as a Preamble standing rule and added to §2.91.D.

## Second leg

None. No new number or derivation decides an A4 verdict:
- DR-A4-1 rests on published measurements;
- DR-A4-2 rests on a standard theorem (Eshelby), which is only re-derived here as a check;
- DR-A4-3 is a declaration, and its sensitivities are order-of-magnitude illustrations.

This follows the brief's proportionality rule.

## Not in scope

- No new gravity mechanism.
- No value for G.
- No cosmology beyond recording that the Λ conflict stands.
- Paper IIA is not edited (Phase B).
- §2.52 Open 3 is untouched.
