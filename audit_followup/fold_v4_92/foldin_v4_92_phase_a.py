#!/usr/bin/env python3
"""foldin_v4_92_phase_a.py — FOLDS V4.92: the October 2026 audit follow-up, Phase A (kill surfaces).

Authorized by the author's brief of October 6, 2026 (audit_followup/inputs/BRIEF_2026-10-06_audit_followup.txt):
"Work out the blast radius every time. For each kill or downgrade, list every entry that depends on it and annotate those
entries in the same fold." / "One short fold per phase." Base: SQT_Master_Ledger_v4_91_CANONICAL.md (md5 ce9ca687…,
1,778,302 B; the project-store copy was read back at fold time and is byte-identical).

Edits (all additive):
  E1 title; E2 As-of prepend; E3 the V4.92 fold-in record (before the V4.91 record);
  E4 the Preamble KC-EP standing rule (before the M.ONT flag section);
  E5 §2.92 (after §2.91.V, before Cluster J);
  E6 in-line "[→ V4.92 …]" brackets at the end of each blast-radius line (inside the last cell for table rows);
  E7 three Part VI rows after the G-VS1 row; E8 one changelog line.
Anchors are read from the file and asserted unique; every fragment lands exactly once; the §2.52 Open 3 Part VI row is
asserted byte-identical; the reverse splice must reconstruct V4.91 byte-identically before the output is accepted.
"""
import hashlib, sys

SRC = "/home/claude/fold/SQT_Master_Ledger_v4_91_CANONICAL.md"
OUT = "/home/claude/fold/SQT_Master_Ledger_v4_92_CANONICAL.md"
V491, V491_BYTES = "ce9ca6873adb5686227f5d103b41e3cc", 1778302
LS_REMOTE = "2026-10-07 16:41:35 UTC"            # main = 3587eb3 (PR #37); estate branch claude/audit-followup-oct6 = 3297421
ESTATE = "`audit_followup/` on branch `claude/audit-followup-oct6`"

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V491, "base V4.91 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V491_BYTES
L = s.split("\n")
assert len(L) == 4643 and L[-1] == "", "line structure changed — re-anchor"

def one_line(prefix):
    hits = [x for x in L if x.startswith(prefix)]
    assert len(hits) == 1, f"anchor not unique: {prefix!r} ({len(hits)})"
    assert s.count("\n" + hits[0] + "\n") == 1
    return hits[0]

O3 = one_line("| **§2.52 Open 3**")

# ---------------------------------------------------------------- E1 title
T_OLD = "# SQT Master Ledger — V4.91 Canonical\n"
T_NEW = "# SQT Master Ledger — V4.92 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD

# ---------------------------------------------------------------- E2 As-of
A_OLD = "**As of:** October 4, 2026 (V4.91 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = ("**As of:** October 7, 2026 (V4.92 fold — **the October 2026 audit follow-up, Phase A (§2.92): A1 polarization "
         "gate FALSIFIED — the S2 channel's detector response is pure vector, the GW170817 structural pass is withdrawn and "
         "the transverse line keeps only the EM carrier; A2 — the internal sector is gapless and quadratic (m* = m/f_s, "
         "Landau speed 0), G-VS1's half-quantum protection is accidental and texture matter radiates at every speed; A3 — "
         "§2.15 RETRACTED to Conjecture (the ideal Borromean ropelength is ≤ 58.006 < 59.894; m_p = 758.7 MeV at the "
         "geometric length), 60.194 and 80.95 are m_p inverted, Borromean linking = baryon number is unprotected, §2.1 "
         "relabelled a fit (dof −1; under PDG 2024 d, c, W and Z miss by more than 2%); A4 — §2.89 and §2.90 DOWNGRADED, "
         "KC-EP made a standing kill condition.** V4.91 fold (October 4, 2026) — ")

# ---------------------------------------------------------------- E6 brackets (prefix, text, kind)
A, B, Cc, D = "§2.92.A", "§2.92.B", "§2.92.C", "§2.92.D"
BR = [
    # ---- A1 blast radius (A1_VERDICT.md §3)
    ("**M.ONT COUPLING-CLASS ANNEX — DECLARED (V4.65",
     f"[→ V4.92 ({A}): the A-SHEAR transverse-carrier consonance can concern the EM carrier only — the S2 (spin-2) reading "
     "is FALSIFIED by the GW170817 polarization test.]", "para"),
    ("**M.ONT VACUUM-COMPOSITION ANNEX — DECLARED (V4.66",
     f"[→ V4.92 (§2.92): ({A}) the A-SHEAR consonance ground now covers the EM carrier only; the other grounds stand. "
     f"({B}) The filament exists only with the immiscibility import — an unbound filling is a texture, which radiates at "
     "every speed on the vacuum of record; with the import, emission is threshold-only. "
     f"({Cc}) 'Linking = baryon number' is UNPROTECTED: every π₁ of the corrected vacuum inventory is Abelian and no "
     "crossing barrier is on record (successor G-RCX1).]", "para"),
    ("**DECLARED (reading (a); author word \"Lock\", July 22, 2026",
     f"[→ V4.92 ({A}): (iii)'s shared-channel claim is FALSIFIED for the spin-2 sector — the S2 response is pure vector and "
     "GW170817 prefers tensor at log₁₀ B ≈ 21; (iv)'s structural pass is WITHDRAWN; the units election (c := the EM "
     "carrier's speed) stands.]", "para"),
    ("**Import I4 declared (R2):**",
     f"[→ V4.92 ({A}): the GW170817 reframe is WITHDRAWN — the S2 channel is pure vector and fails the GW170817 "
     "polarization test; the substrate has no carrier for gravitational waves; c_T = c_EM survives only as the units "
     "election (ANNEX-CDEF-1).]", "para"),
    ("**A. The identification (R1 as algebra; R3 as physics).**",
     f"[→ V4.92 ({A}): the disclosed GW170817 transverse-sector structural pass is WITHDRAWN.]", "para"),
    ("**B. Scope, assumptions, the constitutive fork.**",
     f"[→ V4.92 ({A}): A-SHEAR's spin-2 clause is FALSIFIED (pure-vector S2 response; GW170817 polarization test); its EM "
     "clause remains an assumption.]", "para"),
    ("**D. The kill set as amended (Amendment 1",
     f"[→ V4.92 ({D}): **KC-EP added as a standing kill condition** — any gravity mechanism must derive "
     "composition-independent free fall at MICROSCOPE's |η| ≲ 10⁻¹⁵ (fractional coupling anomalies ≲ 2×10⁻¹⁰ for electrons, "
     "≲ 8×10⁻¹² for binding, ≲ 3×10⁻¹² for Coulomb energy); see the Preamble KC-EP rule.]", "para"),
    ("**H. Gate G-SCALE1 EXECUTED",
     f"[→ V4.92 ({A}): the GW170817 structural pass does not continue (WITHDRAWN); c_T ≡ c continues as the units "
     "election.]", "para"),
    ("**Consequence routing, registers, and the successor surface.**",
     f"[→ V4.92 ({A}): Q3 item (1)'s carrier-identity claim — its spin-2 half is FALSIFIED; item (1) is the EM-carrier "
     "declaration only.]", "para"),
    ("**M. Gate G-POLY1 REGISTERED",
     f"[→ V4.92 ({A}): the GW-side window ('GW170817-class transparency' of the S2 channel) is moot — S2 carries no tensor "
     "content; the EM-side window is unaffected.]", "para"),
    ("**N. Gate G-CI1 REGISTERED",
     f"[→ V4.92 ({A}): CI-V, foreclosed here with PF-3/A-POL, was adopted in substance by G-S2C1's E-P2-1(a) without A-POL; "
     "run now, A-POL FAILS (pure vector); S2-on-cone has no candidate carrier (K = ∅). Process finding H-POL-1.]", "para"),
    ("**O. Gate G-S2C1 REGISTERED",
     f"[→ V4.92 ({A}): E-P2-1(a) is CI-V; as a gravitational-wave carrier it FAILS the GW170817 polarization test; the "
     "dispersion numbers stand; W_∪′ is moot.]", "para"),
    ("**Q. Gate G-MSCS1 REGISTERED",
     f"[→ V4.92 ({A}): S2 carries no GW content; the EM/S2 identity and κ₂ stand as statements about two weightings of the "
     "EM carrier.]", "para"),
    ("**S. Gate G-MSCS2 REGISTERED",
     f"[→ V4.92 ({A}): as for §2.91.Q — the S2-E₂ descriptor carries no GW content.]", "para"),
    ("**T. Gate G-MSCS-A REGISTERED",
     f"[→ V4.92 ({A}): with no tensor carrier, the 'tensor-vs-EM speed difference' window constrains nothing observable: "
     "reading withdrawn, numbers stand.]", "para"),
    ("| **Polycrystalline-vacuum / domain-averaging (VRH) exploration**",
     f"[→ V4.92 ({A}): the GW-side window is moot; the EM-side window stays.]", "row"),
    ("| **Gate G-TSH1**", f"[→ V4.92 ({A}): A-SHEAR's spin-2 clause FALSIFIED; EM carrier only.]", "row"),
    ("| **Gate G-POLY1**", f"[→ V4.92 ({A}): GW-side window moot.]", "row"),
    ("| **Gate G-CI1**", f"[→ V4.92 ({A}): A-POL run — FAIL (pure vector); H-POL-1.]", "row"),
    ("| **Gate G-S2C1** (", f"[→ V4.92 ({A}): E-P2-1(a) = CI-V; it fails as a GW carrier.]", "row"),
    ("| **Gate G-S2C1-W**", f"[→ V4.92 ({A}): W_∪′ moot.]", "row"),
    ("| **Gate G-MSCS1**", f"[→ V4.92 ({A}): S2 carries no GW content.]", "row"),
    ("| **Gate G-MSCS2**", f"[→ V4.92 ({A}): S2 carries no GW content.]", "row"),
    ("| **Gate G-MSCS-A**", f"[→ V4.92 ({A}): tensor-vs-EM reading withdrawn; numbers stand.]", "row"),
    # ---- A2 blast radius (A2_RESULT.md)
    ("**U. Gate G-VS1 REGISTERED",
     f"[→ V4.92 ({B}): the inventory was computed under U(1)_global, which the action of record lacks (its phase is broken "
     "to ℤ₃). Under G₂ × U(1)_ψ₀ × ℤ₃ the counts (degrees 2/4/6, all/T-even; two-leg) are ℝ¹⁴ 1/1, 2/2, 4/3 and ℝ¹⁶ 2/2, "
     "4/4, 8/7; Re(ψ₀²S̄) is forbidden and Re S³ allowed, so the half-quantum protection on P7/I7 is ACCIDENTAL "
     "(DOWNGRADED: with Re S³, V_P7 → three copies of S⁶, π₁ = 0); robust protection = ψ₀ windings only. Successor "
     "G-OBD1.]", "para"),
    ("**Verdict (per the pre-registered arms): STRUCTURAL-ONLY**",
     f"[→ V4.92 ({B}): the gapless internal sector is quadratic (type B): ω ≈ q²/2m*, m* = m/f_s (10.5 in 2D, 314–321 in "
     "3D), Landau speed 0; texture-type defects radiate into it at every speed.]", "para"),
    ("**P. Gate G-QUANTA REGISTERED",
     f"[→ V4.92 ({B}): the K₇-vortex witness is texture-type — on the vacuum of record it feels internal-sector friction at "
     "every speed (a dynamical statement; C1/C2 not re-scored).]", "para"),
    ("| **Gate G-VS1**",
     f"[→ V4.92 ({B}): half-quantum protection DOWNGRADED to accidental (recount under the action's G₂ × U(1)_ψ₀ × ℤ₃); "
     "G-OBD1 registered.]", "row"),
    # ---- A3 blast radius (A3_RESULT.md)
    ("**Status: MIXED TIER 2 / CONJECTURE 1**",
     f"[→ V4.92 ({Cc}): **RETRACTED to Conjecture status by this entry's own rule (clause 1).** Verification (1) FAILS: in "
     "the convention of record (Paper VII E.1.1, length per tube radius) the ideal Borromean ropelength is ≤ 58.006 "
     "(CFKSW B₀; §2.82's four-arc configuration = 48 arctan √7 = 58.0526, two-leg), below the window 59.894–60.494; "
     "Paper VII E.1.3 reads 'prediction falsified at leading order'. Clause 2 not triggered as written: [58.006, 62.0] "
     "misread the best-known length (an upper bound on the minimum) as a lower bound. At L = 58.006 the §2.14 formula "
     "gives m_p = 758.7 MeV (−19.1%). L_B = 60.194 is m_p inverted (A/Z_f = 20/6), so the 0.000% and −0.138% are "
     "calibration outputs. A = 20 is Δ(t,t,t) = (t−1)³; the one-variable Alexander polynomial (t−1)⁴ gives 70. Borromean "
     "linking is unprotected (G-RCX1).]", "para"),
    ("Twist-knot ropelength formula L(K) = (13 + 5n)/12",
     f"[→ V4.92 ({Cc}): that prediction has failed — §2.15 retracted to Conjecture.]", "para"),
    ("- **Tight (CFKSW) conformation**",
     f"[→ V4.92 ({Cc}): this configuration's length is 48 arctan √7 = 12π + 24 arcsin(3/4) = 58.0526 per tube radius "
     "(embedded at thickness exactly 1; two-leg) — 0.080% above CFKSW's 58.006; it bounds the ideal ropelength below "
     "§2.15's window.]", "para"),
    ("*(V4.51 annotation — M.ONT RECONCILED",
     f"[→ V4.92 ({Cc}): ground (3) of the seal — the Ashton falsification clause — has executed: verification (1) FAILED and "
     "§2.15 is retracted to Conjecture. 'L strictly geometric' stands, which is why: at the geometric L = 58.006 the formula "
     "gives m_p = 758.7 MeV.]", "para"),
    ("The knot-to-particle mapping produces masses within 2%",
     f"[→ V4.92 ({Cc}): **RELABELLED — a fit, not a prediction table:** 8 rows against 8 per-row selected inputs (the six "
     "fitted Z_f, the W exponent 27, the Z angle φ⁻³) and the shared scale ξ_vac = 100φ — residual dof −1 (knot, A- and "
     "L-convention choices not counted). PDG 2024 (Navas et al., PRD 110, 030001): u −5.6% (outside 2.16 ± 0.07), "
     "d −2.36%, c −2.15%, b −0.49%, t −0.80%, τ −1.38%, W +2.19%, Z +3.04% — the 2% headline holds for b, t and τ "
     "only.]", "para"),
    ("**M.ONT DECLARATION (V4.51",
     f"[→ V4.92 ({Cc}): at the declared tight (minimizer) configuration, L = 58.006, the mass clause gives m_p = 758.7 MeV "
     "(−19%); the 'Paper VII Conj. 1 … TRANSFER' item transferred a prediction that has now failed (§2.15 → Conjecture); "
     "'Borromean linking (= baryon number)' is UNPROTECTED (G-RCX1).]", "para"),
    ("| **M.ONT gate**",
     f"[→ V4.92 ({Cc}): linking = baryon number UNPROTECTED; the ideal-ropelength mass gives m_p = 758.7 MeV.]", "row"),
    ("| **G-Φ1 gate**",
     f"[→ V4.92 ({Cc}): L_p = 80.95 is m_p inverted through §2.14 with A/Z_f = 1/2 (two-leg: 80.947); 'L_p = ξ_vac/2' and "
     "the 12.39 × 148 factorization are properties of that inversion, not of the proton's geometry (the ideal Borromean "
     "length is ≤ 58.006).]", "row"),
    ("| **Gate G-κ1**",
     f"[→ V4.92 ({Cc}): the Ashton clause cited by the seal has executed — verification (1) FAILED; §2.15 → Conjecture.]",
     "row"),
    # ---- A4 blast radius (A4_RESULT.md)
    ("- **R_bowl ≫ d_obj:**",
     f"[→ V4.92 ({D}): DOWNGRADED — flat means no curvature, not no slope; neutrons (COW; qBounce), atoms and antihydrogen "
     "fall in Earth's field at R_bowl/d_obj ≥ 10¹⁶. Withdrawn as stated; true only as the tidal-only statement (standard "
     "physics).]", "para"),
    ("- Scale-filtered locality + nesting: **R2**",
     f"[→ V4.92 ({D}): WITHDRAWN as stated (falsified for the pull); the nesting reading survives only relative to the inner "
     "body's free fall; KC-EP FIRES (scale-dependent response).]", "para"),
    ("**Ground state (R2 from R1 isotropy).**",
     f"[→ V4.92 ({D}): the Λ conflict stands — uniform stress gravitates in any metric theory; a tensioned thread/sheet "
     "network has w = −1/3 or −2/3 (Bucher–Spergel 1999), not dark energy's w ≈ −1, and a Planck-scale lattice's tension is "
     "~10¹²⁰ too large; 'no gravity' needs a mechanism, and none is on record.]", "para"),
    ("**What a defect does (R2).**",
     f"[→ V4.92 ({D}): mechanism DOWNGRADED R2 → R3 — a self-equilibrated defect in a (tensioned) elastic lattice exerts no "
     "net force, so it has no monopole field (Eshelby). VC-B transfer (owed since V4.66): knots are composite objects "
     "embedded in the envelope bath, not defects of the lattice's own field; 'not removable without cutting' meets "
     f"{Cc} — cutting (reconnection) is available and the linking is unprotected.]", "para"),
    ("**Propagation and 1/r² (R2; geometric, not formally proved).**",
     f"[→ V4.92 ({D}): **1/r² WITHDRAWN** — in linear elasticity, uniformly tensioned or not, isotropic dilatation centres do "
     "not interact (Eshelby 1956) and force dipoles interact as 1/r³ with zero orientation average; the shell count "
     "presupposes a conserved monopole flux. I4 (owed): the exponent was never import-free — it is the declared import I4 "
     "(§2.88.E).]", "para"),
    ("**Particle-type hierarchy (R2; the electron line R3 pending M.ONT).**",
     f"[→ V4.92 ({D}): **KC-EP FIRES** — 'no topology: zero' means binding and electrostatic energy carry no deficit and "
     "would not gravitate: η(Ti, Pt) ≈ 9×10⁻⁴, about 10¹¹ times MICROSCOPE's bound.]", "para"),
    ("**What §2.88 does NOT claim.**",
     f"[→ V4.92 ({D}): KC-EP UNMET — CM-2's 'knots contribute response amplitude only' carries no derivation that the "
     "response is ∝ total mass-energy; no promotion until derived.]", "para"),
]
EDITS = []
for prefix, text, kind in BR:
    old = one_line(prefix)
    assert "[→ V4.92" not in old
    if kind == "para":
        assert not old.endswith(" |")
        new = old + " " + text
    else:
        assert old.endswith(" |") and old.startswith("| ")
        new = old[:-2] + " " + text + " |"
    EDITS.append((old, new))
assert len({o for o, _ in EDITS}) == len(EDITS), "two brackets on one line"
NBR = len(EDITS)

# ---------------------------------------------------------------- E4 Preamble KC-EP
P_ANCH = "### The Particle-Ontology Declaration Flag (M.ONT)\n"
assert s.count(P_ANCH) == 1 and s.count("\n\n" + P_ANCH) == 1
KCEP = ("### KC-EP — The Equivalence-Principle Kill Condition (standing; V4.92)\n\n"
        "*(Standing rule, October 7, 2026, from the audit follow-up brief of October 6: \"Make this a standing kill "
        "condition.\" Derivation of the thresholds and first application: §2.92.D.)*\n\n"
        "**Statement.** Any gravity mechanism kept or proposed in the program must *derive*, not declare, that free-fall "
        "acceleration is independent of composition at the level of MICROSCOPE's test of the weak equivalence principle, "
        "η(Ti, Pt) = [−1.5 ± 2.3 (stat) ± 1.5 (syst)] × 10⁻¹⁵ (Touboul et al., PRL 129, 121102 (2022)). The derivation must "
        "cover every form of mass-energy: the electrons (the ledger's separate ε_e), nuclear binding and electrostatic "
        "energy (which are not knots), and the neutron excess. For the Ti/Pt pair the fractional coupling anomalies allowed "
        "are, to order of magnitude, ≲ 2×10⁻¹⁰ (electrons), ≲ 8×10⁻¹² (binding), ≲ 3×10⁻¹² (Coulomb) and ≲ 6×10⁻¹⁴ (neutron "
        "excess). A mechanism whose coupling is set by an object's size, topology or knot type rather than its total "
        "mass-energy FIRES this condition unless it derives the proportionality. **Status at V4.92:** FIRES for §2.89 and "
        "§2.90; UNMET for §2.88 (Bjerknes/CM-3); the §2.91 longitudinal bridge was already retired (V4.67).\n\n")

# ---------------------------------------------------------------- E5 §2.92
J_ANCH = "## J. Multi-Lens Reference and Phase Incommensurability\n"
assert s.count(J_ANCH) == 1 and s.count("\n\n" + J_ANCH) == 1
V_LINE = one_line("**V. Longitudinal branch coupling on the instantiated supersolid")
assert s.count(V_LINE + "\n\n" + J_ANCH) == 1
S292 = [
    "### §2.92 — The October 2026 Audit Follow-Up, Phase A: Kill Surfaces (V4.92)",
    f"*(Folded V4.92, October 7, 2026, under the author's brief of October 6 — \"One short fold per phase\"; estate {ESTATE}. "
    "Each part was pre-registered and md5-locked before any computation, with a blind second leg wherever a new number or "
    "derivation decided a verdict. The affected entries carry short [→ V4.92 (§2.92.x)] pointers. No §3.x: each verdict is a "
    "pre-registered rule executing its registered consequence (the V4.67/V4.77 precedent).)*",
    "**A. Polarization gate (A1) — FALSIFIED (R1, two-leg).** Pre-registration `A1_PREREG.md` d5f6aa3b (+ Addendum 1). The "
    "S2 channel presents no tensor part to a detector: every coupling of a detector made of the medium to the transverse "
    "wave has spin weight ±1 (pure vector), and the longitudinal wave has m = 0 with no breathing mode. Motion-induced "
    "transverse-traceless leakage is ≤ 2.6 (v/c)² in power, texture ≈ 10⁻¹², second order ≈ 10⁻⁴². Both legs agree to "
    "3.3×10⁻¹⁶ on a common 1,680-value grid. GW170817, with its sky position fixed, prefers pure tensor over pure vector at "
    "log₁₀ B = 20.81 (PRL 123, 011102 (2019)), and no helicity-0 substrate branch is on the light cone to supply a mixed "
    "escape. **Verdict (locked rule, clause 1): the reading that the spin-2 radiative sector shares the transverse channel is "
    "FALSIFIED; the GW170817 structural pass is WITHDRAWN wherever it appears; the transverse line keeps only the EM carrier "
    "(c_T ≡ c survives as the units election); the gravitational-wave sector has no carrier in the substrate.** Secondary "
    "arms (no decision weight): the double pulsar cannot confirm a vector channel, and a vector channel's pulsar-timing "
    "correlation is not Hellings–Downs. Process finding H-POL-1: G-CI1's PF-3 tripwire did not fire when G-S2C1's E-P2-1(a) "
    "adopted CI-V in substance; proposed pin — any election that re-identifies a radiative species is screened against the "
    "PF list of the gate that defined it.",
    "**B. Internal modes (A2) — two DOWNGRADES (R1 mechanism, two-leg).** Pre-registration `A2_PREREG.md` fd2e9597. "
    "(1) The internal sector of the vacuum of record is gapless and quadratic, ω ≈ q²/2m* with m* = m/f_s (10.506 in 2D; "
    "314–321 in 3D), so its Landau critical velocity is 0; P0 has seven type-B branches, and only stratum R is fully gapped. "
    "(2) G-VS1 counted invariants under U(1)_global, which the action lacks. Under G₂ × U(1)_ψ₀ × ℤ₃ the degree-6 term Re S³ "
    "is allowed and pins the 7-sector phase, so the half-quantum protection on P7 and I7 is accidental; robust protection is "
    "ψ₀ windings only, and Re(ψ₀²S̄) is forbidden. (3) The declared coupling class (total density; −ρ_n u̇·v_s) does not "
    "couple linearly to the internal branches, but texture-type matter (Fano-line cores, the K₇ vortex) radiates into them at "
    "every speed (drag ∝ m*²v in 2D, m*³v² in 3D): the vacuum of record cannot host moving texture matter without an import "
    "that gaps those directions, and on stratum R the gap must reach Δ ≥ ½m*c_T² ≈ 3.2μ. The VC-B filament with its "
    "immiscibility import has threshold emission only. Successor registered: **G-OBD1** (order-by-disorder stratum "
    "selection, which would turn I6 from an import into a computation).",
    "**C. Matter sector (A3) — §2.15 RETRACTED to Conjecture (two-leg, 46/46).** Pre-registration `A3_PREREG.md` e2f1090c. "
    "(1) Units match: Paper VII E.1.1 defines ℒ = L/R, length per tube radius, the CKS/CFKSW convention. §2.82's four-arc "
    "configuration has length 48 arctan √7 = 12π + 24 arcsin(3/4) = **58.0526** per tube radius (CKS 2002: \"about 58.05\"); "
    "it is embedded at thickness exactly 1 and is Borromean by its linking numbers, piercing pattern and the multivariable "
    "Alexander polynomial of its projections. CFKSW's critical configuration B₀ is 58.006. (2) The ideal ropelength is "
    "≤ 58.006 < 59.894, so verification (1) FAILS and, by §2.15's own rule (clause 1), the entry retracts to Conjecture status. "
    "Paper VII's outcome table (E.1.3) reads \"prediction falsified at leading order\". Clause 2 is not triggered as written: "
    "its interval misread 58.006, the best-known configuration and so an upper bound on the minimum, as a lower bound. At "
    "L = 58.006 the §2.14 formula gives **m_p = 758.7 MeV (−19.1%)**. (3) Of the three proton lengths on record only ≈ 58.05 "
    "is a length: **60.194 and 80.95 are m_p inverted** (A/Z_f = 20/6 and 1/2), so the proton's 0.000% and the neutron's "
    "−0.138% are calibration outputs and V4.40's \"L_p = ξ_vac/2\" has no geometric standing. (4) A = 20 is the sum of squares "
    "of Δ(t,t,t) = (t−1)³; the one-variable Alexander polynomial (t−1)⁴ (Torres) gives **70**. (5) **Borromean linking = "
    "baryon number is UNPROTECTED:** every π₁ of the corrected vacuum inventory is Abelian, so there is no Poénaru–Toulouse "
    "crossing obstruction; no barrier is on record; and Gross–Pitaevskii vortex links untie (Kleckner, Kauffman & Irvine, Nat. "
    "Phys. 12, 650 (2016); Borromean rings: Guan, Zuccher & Liu, Phys. Fluids 37, 024126 (2025)). Protection would need "
    "exp(−S) with S ≳ 152 (hadronic attempt rate) to 197 (core rate) against τ_p > 2.4×10³⁴ yr (Super-Kamiokande). Successor "
    "registered: **G-RCX1** (a non-Abelian core sector, or a computed crossing barrier). (6) **§2.1 is a fit:** 8 rows against "
    "8 per-row selected inputs (six fitted Z_f, the W exponent 27, the Z angle φ⁻³) plus the shared scale ξ_vac = 100φ, so "
    "the residual dof is −1. Against PDG 2024: u −5.6% (outside 2.16 ± 0.07), d −2.36%, c −2.15%, b −0.49%, t −0.80%, "
    "τ −1.38%, **W +2.19%, Z +3.04%**; the 2% headline holds for b, t and τ only. Lead for Phase B (unverified in-session): "
    "the calculator's quark L values look like ropelengths per tube diameter, while L_e and L_B are per radius.",
    "**D. Gravity entries (A4) and KC-EP.** Pre-registration `A4_PREREG.md` 7b876a27; no second leg, since standard theorems "
    "and published measurements decide. (1) **§2.89 DOWNGRADED:** its decoupling claim concerns the pull (\"its gradient is "
    "negligible … decoupled\"), but flat means no curvature, not no slope. Neutrons (Colella–Overhauser–Werner 1975; qBounce "
    "2011), atoms (Peters–Chung–Chu 1999) and antihydrogen (ALPHA-g 2023) fall in Earth's field at R_bowl/d_obj ≥ 10¹⁶. "
    "Scale-filtered locality is withdrawn as stated; the tidal-only restatement is standard physics. (2) **§2.90 DOWNGRADED "
    "(R2 → R3; 1/r² withdrawn):** in linear elasticity, uniformly tensioned or not, self-equilibrated defects do not interact "
    "as 1/r — isotropic dilatation centres not at all (Eshelby 1956), force dipoles as 1/r³ with zero orientation average — "
    "and a 1/r energy needs net forces on the medium, which a knot in a closed lattice cannot exert (sympy re-derivation, "
    "`a4_checks.py`). The owed I4 and VC-B annotations are attached, and the Λ conflict stands. (3) **KC-EP declared** "
    "(Preamble; §2.91.D). It FIRES for §2.89 (scale-dependent response) and for §2.90 (non-topological field energy carries "
    "no deficit, so binding energy would not gravitate: η ≈ 9×10⁻⁴), and is UNMET for §2.88 (Bjerknes/CM-3).",
    "**E. What the substrate program still stands on.** As mathematics: the PSL(2,7) and lattice results, the instantiated "
    "crystals with their two-leg numbers, and the four-arc/CFKSW geometry. As declarations, not derivations: one transverse "
    "light carrier (the units election), knots as embedded objects with a ropelength-organized fitting function, and a "
    "vacuum whose stability, vortex protection and matter-hosting each rest on named imports (I4, I6, the immiscibility "
    "import). Gone or downgraded: any carrier for gravitational waves, every static gravity mechanism on record, the "
    "proton-mass prediction, topological protection of baryon number, and the 2% mass-table headline. Standing tests: "
    "KC1–KC3 and KC-EP.",
    "**Registers and non-claims.** A1–A3 numerics R1 (two-leg). Honesty items H-A1-1, H-A2-1 and H-A3-1: each blind leg "
    "returned before the first-leg code existed; the decisive first-leg values had been derived first and are deterministic. "
    "A4: R1 for the re-derived standard results, R2 for the dispositions. No observable bridge (M.BRIDGE intact); no "
    "magnitude for any import; §2.52 Open 3 untouched.",
]
S292_TXT = "\n\n".join(S292) + "\n\n"

# ---------------------------------------------------------------- E7 Part VI rows (after the G-VS1 row)
C1_ANCH = one_line("| **G-C1 gate** (angle-3")
ROWS = ("| **Audit follow-up, Phase A** (§2.92 — A1 polarization gate, A2 internal modes, A3 matter sector, A4 gravity "
        "entries; brief of October 6, 2026; pre-registrations d5f6aa3b / fd2e9597 / e2f1090c / 7b876a27) | **CLOSED (V4.92, "
        "October 7, 2026)** — A1 FALSIFIED (S2 pure vector; the GW170817 pass withdrawn); A2 two DOWNGRADES (half-quantum "
        "protection accidental; texture matter radiates at every speed); A3 §2.15 → Conjecture, linking unprotected, §2.1 "
        "relabelled a fit; A4 §2.89 and §2.90 DOWNGRADED; KC-EP standing. §2.52 Open 3 untouched. |\n"
        "| **Gate G-OBD1** (registered by §2.92.B: the zero-point (BdG) energy of each G-VS1 stratum — does order-by-disorder "
        "select a stratum, turning import I6 into a computation?) | **REGISTERED, unopened** |\n"
        "| **Gate G-RCX1** (registered by §2.92.C: what protects Borromean linking — a non-Abelian core sector (PSL(2,7) "
        "colourings of the link group plus the Annala et al. invariant) or a computed crossing barrier with S ≳ 150–200?) | "
        "**REGISTERED, unopened** |\n")

# ---------------------------------------------------------------- E3 fold-in record
R_ANCH = "**V4.91 fold-in record (October 4, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = ("**V4.92 fold-in record (October 7, 2026):** AUDIT FOLLOW-UP, PHASE A — four pre-registered parts recorded as "
          "§2.92, under the author's brief of October 6, 2026 (\"Work out the blast radius every time … annotate those entries "
          "in the same fold\"; \"One short fold per phase\"; `FOLD_AUTHORIZATION_V4_92.md`). A1 polarization gate (two-leg): "
          "FALSIFIED. A2 internal modes (two-leg): two DOWNGRADES. A3 matter sector (two-leg, 46/46): §2.15 RETRACTED to "
          "Conjecture, linking unprotected, §2.1 relabelled a fit. A4 gravity entries: §2.89 and §2.90 DOWNGRADED; KC-EP "
          f"declared as a Preamble standing rule. The blast radius is annotated in place: {NBR} in-line [→ V4.92] brackets, "
          "plus three Part VI rows (the Phase A closure, G-OBD1, G-RCX1). Estate: " + ESTATE + " (head at fold `3297421`); "
          "`git ls-remote` " + LS_REMOTE + ": main = `3587eb3` (PR #37). No §3.x; no observable bridge; §2.52 Open 3 "
          "untouched.\n\n")

# ---------------------------------------------------------------- E8 changelog
LINE_CH91 = one_line("*V4.91 (October 4, 2026): additions only")
assert L[4641] == LINE_CH91
CH_NEW = (f"*V4.92 (October 7, 2026): additions only — title/As-of header bump; the V4.92 fold-in record; the Preamble KC-EP "
          f"standing rule (before the M.ONT flag); §2.92 (audit follow-up, Phase A) after §2.91.V; {NBR} in-line [→ V4.92] "
          "brackets on the blast-radius entries; three Part VI rows after the G-VS1 row; reverse-splice byte-identical to "
          "V4.91 (`ce9ca687`); the §2.52 Open 3 row untouched.*")


def build():
    frags = [T_NEW, A_NEW, RECORD, KCEP, S292_TXT, ROWS, CH_NEW] + [n for _, n in EDITS]
    for fr in [A_NEW, RECORD, KCEP, S292_TXT, ROWS, CH_NEW]:
        assert s.count(fr) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    out = out.replace("\n\n" + P_ANCH, "\n\n" + KCEP + P_ANCH, 1)
    for old, new in EDITS:
        assert out.count("\n" + old + "\n") == 1
        out = out.replace("\n" + old + "\n", "\n" + new + "\n", 1)
    V_NEW = V_LINE                                     # §2.91.V itself carries no bracket
    out = out.replace(V_NEW + "\n\n" + J_ANCH, V_NEW + "\n\n" + S292_TXT + J_ANCH, 1)
    out = out.replace("\n" + C1_ANCH + "\n", "\n" + ROWS + C1_ANCH + "\n", 1)
    out = out.replace("\n" + LINE_CH91 + "\n", "\n" + LINE_CH91 + "\n" + CH_NEW + "\n", 1)
    O3_POST = [x for x in out.split("\n") if x.startswith("| **§2.52 Open 3**")]
    assert O3_POST == [O3] and out.count(O3) == 1, "§2.52 Open 3 row changed — halt"
    for fr in frags:
        assert out.count(fr) == 1, f"fragment count != 1: {fr[:60]!r}"
    # reverse splice
    rev = out.replace("\n" + LINE_CH91 + "\n" + CH_NEW + "\n", "\n" + LINE_CH91 + "\n", 1)
    rev = rev.replace("\n" + ROWS + C1_ANCH + "\n", "\n" + C1_ANCH + "\n", 1)
    rev = rev.replace(V_NEW + "\n\n" + S292_TXT + J_ANCH, V_NEW + "\n\n" + J_ANCH, 1)
    for old, new in EDITS:
        rev = rev.replace("\n" + new + "\n", "\n" + old + "\n", 1)
    rev = rev.replace("\n\n" + KCEP + P_ANCH, "\n\n" + P_ANCH, 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V491 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    print("V4.92 FOLDED:", OUT)
    print("bytes:", len(b), "(V4.91 %d B; delta +%d B); chars delta +%d" % (V491_BYTES, len(b) - V491_BYTES, len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("brackets:", NBR, "| §2.92 chars:", len(S292_TXT), "| KC-EP chars:", len(KCEP), "| record chars:", len(RECORD))
    print("reverse-splice: BYTE-IDENTICAL to V4.91 (%s) — PASS" % V491)
    print("§2.52 Open 3: Part VI row byte-identical and unique — PASS; all fragments landed exactly once — PASS")
