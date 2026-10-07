#!/usr/bin/env python3
# =============================================================================
# edit_v6_4_correction.py — Gauge paper v6.3 -> v6.4 DRAFT (correction).
# Items (B1 of the October 6, 2026 audit follow-up):
#   (i)  §5 sign dressing Y = (−1)^(N+1)·N/3 withdrawn; Furey's Q = N/3 restored;
#        the v6.2 audit item closed in the negative; §9 claim (3) withdrawn;
#        the §3 sentence tying hypercharge to the Fano± bipartition corrected.
#   (ii) Cabibbo: sin θ_C = 3/13 excluded by PDG 2024 (7.6σ, 8.5σ); tan θ_C
#        agreement recorded as a post-hoc observation (Conjecture 3); §9 claim (5)
#        withdrawn from the verified list; Open Problem (ix) restated.
#   (iii) §3 face description: two line-disjoint Fano planes, not lines and
#        complements; Aut(face set) = AGL(1,7), PSL(2,7) per Fano plane.
#   (iv) §8 chirality given its combinatorial basis (all 42 automorphisms
#        orientation-preserving).
# Authority: B1_PREREG.md (md5 5374289db16dcdd73f90875cc89b7ee3), two-leg checks
#   32/32 PASS (b1_compare_output.txt). DRAFT ONLY: not published; the author
#   approves any Zenodo version.
# Discipline: md5 precondition on v6.3; anchored unique replacements; reverse
#   splice must return v6.3 byte-exact; structural checks EOF-anchored.
# Usage: python3 edit_v6_4_correction.py [SRC_v6_3.md] [OUT_DIR]
# =============================================================================
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "source", "Gifford_Csaszar_Gauge_Group_v6_3_2026.md")
OUT = sys.argv[2] if len(sys.argv) > 2 else HERE
DST = os.path.join(OUT, "Gifford_Csaszar_Gauge_Group_v6_4_2026_DRAFT.md")
V63_MD5 = "8c01f4c9d849bbab1eaff826fd353c3f"

text = open(SRC, encoding="utf-8").read()
md5_before = hashlib.md5(text.encode("utf-8")).hexdigest()
assert md5_before == V63_MD5, f"source is not canonical v6.3 (md5 {md5_before})"
th = {"t": text}
HUNKS = []  # (id, tags, description, old, new)

def splice(hid, tags, desc, old, new):
    t = th["t"]
    assert t.count(old) == 1, f"{hid}: anchor not unique (count={t.count(old)})"
    th["t"] = t.replace(old, new)
    assert th["t"].count(new) == 1, f"{hid}: new text not unique"
    HUNKS.append((hid, tags, desc, old, new))
    print(f"[hunk] {hid} — {desc}")

def splice_span(hid, tags, desc, start, end, new):
    t = th["t"]
    assert t.count(start) == 1 and t.count(end) == 1, f"{hid}: span markers not unique"
    i, j = t.index(start), t.index(end) + len(end)
    assert i < j
    old = t[i:j]
    splice(hid, tags, desc, old, new)

# ---------------------------------------------------------------- G1 version
splice("G1", "T8", "version line v6.3 -> v6.4",
    "July 2026 — v6.3 (Revised)",
    "October 2026 — v6.4 (Revised)")

# ---------------------------------------------------------------- G2 revision note
splice("G2", "T8", "v6.4 revision note (correction declaration)",
    "*Revision note (v6.3):",
    "*Revision note (v6.4): Correction following an audit of October 2026; no new claim is added. "
    "(i) Section 5: the alternating-sign operator Y = (−1)^(N+1) × N/3 is withdrawn. It is not affine in the "
    "occupation number N, so the three modes carry no definite charge under it, and its labels place the N = 1 and "
    "N = 2 sectors, which carry conjugate color representations, in the same one; with either color action one quark "
    "sector receives a charge the Standard Model forbids for its color. The charges of the three-mode Fock space are "
    "those of Furey's number operator, Q = N/3 (Furey 2015). The audit item left open in v6.2 is closed in the "
    "negative: the dressing is not a reparametrization of Furey's choices of ideal and conjugation, and it is not "
    "consistent. The novelty of Section 5 is confined to the identification of the three modes with the three "
    "Hamiltonian 7-cycles of K₇, verified claim (3) is withdrawn, and the sentence of Section 3 that tied hypercharge "
    "to the Fano⁺ ↔ Fano⁻ bipartition is corrected to match. (ii) Sections 6.1, 9, 10, 11 and 12: the Cabibbo "
    "result was stated as sin θ_C = |V_us| = 3/13. Against PDG 2024 this is excluded at 7.6σ (|V_us|) and 8.5σ "
    "(global fit). The ratio agrees with tan θ_C = |V_us/V_ud| to within 0.8σ, but that reading was identified after "
    "comparison with data and the construction does not select it, so it is recorded as a post-hoc observation "
    "(Conjecture 3), not a verified result. Verified claim (5) is withdrawn from the verified list, and Open Problem "
    "(ix) is restated, since Standard Model running of the Cabibbo angle is of order 10⁻⁴ (Grossman et al. 2022). "
    "(iii) Section 3: the 14 faces are the lines of two Fano planes on the seven vertices that share no line, not the "
    "lines of one Fano plane and their complements. The automorphism group of the face set is the affine group "
    "AGL(1,7), of order 42; PSL(2,7) ≅ GL(3,2), of order 168, is the automorphism group of each Fano plane "
    "separately, and only its 21 elements in F₂₁ preserve the faces. (iv) Section 8: the chirality statement is given "
    "a combinatorial basis; all 42 automorphisms preserve the orientation of the torus, so no realization has a "
    "mirror symmetry. Two references are added (Grossman et al. 2022; Particle Data Group 2024), and the reference "
    "list now runs 1–25.*\n\n"
    "*Revision note (v6.3):")

# ---------------------------------------------------------------- G3/G4 abstract
splice("G3", "COR", "Abstract, first sentence: hypercharge and Cabibbo claims scoped",
    "encodes the Standard Model gauge group SU(3) × SU(2) × U(1), three fermion generations, correct hypercharge "
    "assignments, and the leading CKM quark mixing angle through its combinatorial topology.",
    "encodes the Standard Model gauge group SU(3) × SU(2) × U(1) and three fermion generations through its "
    "combinatorial topology, carries the three fermionic modes of Furey's number-operator construction of charge, "
    "and contains a ratio, 3/13, that matches one reading of the leading CKM mixing parameter.")
splice("G4", "COR", "Abstract, stages (iii) and (iv)",
    "(iii) hypercharge assignments follow from a Fock space grading of the three Hamiltonian cycles; (iv) the "
    "Cabibbo angle emerges as the ratio of the Fano valence to the rank of the boundary operator in the Császár "
    "triangulation.",
    "(iii) the three modes of Furey's number-operator construction, whose charge spectrum Q = N/3 is Furey's (2015), "
    "are identified with the three Hamiltonian cycles of K₇; (iv) the ratio of the Fano valence to the rank of the "
    "boundary operator in the Császár triangulation is 3/13, which agrees with tan θ_C = |V_us/V_ud| but not with "
    "sin θ_C = |V_us|; because the construction does not select the observable, the agreement is recorded as a "
    "post-hoc observation.")

# ---------------------------------------------------------------- G5 introduction
splice("G5", "COR", "Section 1: outline sentence",
    "the Fano plane incidence geometry produces three generations and exact hypercharges; and the homological cycle "
    "structure of the triangulation produces the Cabibbo angle.",
    "the Fano plane incidence geometry produces three generations; the three Hamiltonian cycles carry the modes of "
    "Furey's number-operator charge; and the homological cycle structure of the triangulation produces the ratio "
    "3/13, which Section 6.1 compares with the Cabibbo angle.")

# ---------------------------------------------------------------- G6/G7 Section 3
splice("G6", "FACT", "Section 3: faces are two line-disjoint Fano planes; Aut(face set) = AGL(1,7); PSL(2,7) per plane",
    "The 14 triangular faces correspond to the 7 multiplication triples and their 7 anti-triples — the 7 lines of "
    "the Fano plane PG(2, 𝔽₂) and their complements.",
    "With the vertices labelled by i ∈ ℤ₇ (e₇ ≡ e₀, as in Section 6), the 14 triangular faces form two families of "
    "seven, {i, i+1, i+3} and {i, i+2, i+3}. Each family is the line set of a Fano plane PG(2, 𝔽₂) on the seven "
    "vertices: the first (Fano⁺) is the set of 7 octonion multiplication triples (e_i e_{i+1} = e_{i+3}), the "
    "second (Fano⁻) shares no line "
    "with it, and together they contain every edge exactly twice. (Earlier versions described the second family as "
    "the complements of the Fano lines; the complement of a line has four points, not three.) The automorphism group "
    "of the 14-face set is the affine group AGL(1,7) = {x ↦ ax + b}, of order 42; its index-2 subgroup F₂₁ "
    "(a ∈ {1, 2, 4}) preserves each Fano plane, and the other coset exchanges them. The group PSL(2,7) ≅ GL(3,2), "
    "of order 168, is the automorphism group of each Fano plane separately, not of the face set: only its 21 "
    "elements in F₂₁ preserve the faces.")
splice("G7", "COR", "Section 3: the Fano± bipartition no longer said to provide hypercharge",
    "The Z₂ bipartition Fano⁺ ↔ Fano⁻ provides U(1) hypercharge.",
    "The Z₂ bipartition Fano⁺ ↔ Fano⁻ exchanges the two face families. (Versions through v6.3 also said it "
    "provides U(1) hypercharge, through the sign dressing of Section 5; that dressing is withdrawn in v6.4, and the "
    "U(1) factor is the surface phase of Section 7.)")

# ---------------------------------------------------------------- G8/G9 Section 5
splice("G8", "COR", "Section 5, first paragraph: Furey 2015's operator is a charge",
    "with hypercharge proportional to the occupation number divided by 3,",
    "with charge proportional to the occupation number divided by 3,")
splice_span("G9", "WD/COR", "Section 5: sign dressing withdrawn, Furey's Q = N/3 restored, audit item closed negative, novelty confined to (a)",
    "The hypercharge operator is:", "is claimed in neither direction here.",
    "The charge operator is Furey's number operator divided by three (Furey 2015):\n\n"
    "*Q = N/3*\n\n"
    "where N is the total circuit occupation number. In Furey's minimal left ideal its eigenvalues are N = 0 → Q = 0 "
    "(neutrino); N = 1 → Q = +1/3 (anti-down quark, 3 colors); N = 2 → Q = +2/3 (up quark, 3 colors); N = 3 → "
    "Q = +1 (positron); the complex-conjugate ideal carries the antiparticles, with charge −N/3. For SU(2)-singlet "
    "states the charge equals the hypercharge. These assignments are Furey's; they are carried here by the cycle "
    "modes, not derived. Two structural facts fix their form. First, color acts irreducibly on the three modes, so a "
    "U(1) charge commuting with color gives every mode the same charge, and the charge of an N-mode state is then "
    "affine in N. Second, the N = 2 states are antisymmetric pairs of N = 1 modes, so the N = 1 and N = 2 sectors "
    "carry conjugate color representations, 3̄ and 3 or 3 and 3̄ — the 3 ⊕ 3̄ of Section 3.\n\n"
    "**Correction (v6.4).** Versions through v6.3 used the operator Y = (−1)^(N+1) × N/3, assigned its spectrum "
    "{0, +1/3, −2/3, +1} to the right-handed neutrino, three down antiquarks, three up antiquarks and the positron, "
    "attributed the alternating sign to the complex structure J = L_{e₀}, and described the spectrum as the one "
    "anticipated by Furey's construction. That operator is withdrawn. It is not affine in N, so the modes carry no "
    "definite charge under it; and its labels place the N = 1 and N = 2 sectors in the same color representation "
    "(3̄), which the conjugate pairing excludes. With either color action on the modes, one quark sector receives a "
    "charge that the Standard Model forbids for its color: (3, +1/3) or (3, −2/3). The open audit item recorded in "
    "v6.2 — whether the dressing is a reparametrization of Furey's choices of ideal and conjugation — is closed in "
    "the negative: each of those choices gives a charge affine in N, and none reproduces the dressing.\n\n"
    "The novel content of this section is therefore confined to (a) the identification of the three fermionic modes "
    "with the three disjoint Hamiltonian 7-cycles of K₇ (the quadratic-residue classes mod 7) — a geometric "
    "statement with no counterpart in the algebraic construction.")

# ---------------------------------------------------------------- G10-G12 Section 6.1
splice("G10", "COR", "Section 6.1: the displayed equation states the number, not |V_us|",
    "The leading mixing angle is the ratio of the Fano point-valence to the rank of the boundary operator in the "
    "Császár triangulation:\n\n*|V_us| = 3/13 = 0.2308*",
    "The construction's candidate for the leading mixing parameter is the ratio of the Fano point-valence to the "
    "rank of the boundary operator in the Császár triangulation:\n\n*3/13 = 0.23077*")
splice("G11", "COR", "Section 6.1: physical-interpretation sentence scoped",
    "Why this ratio equals the Cabibbo mixing angle is the physical question the construction raises but does not "
    "yet answer from first principles.",
    "Whether this ratio is related to Cabibbo mixing at all, and if so through which observable, is the physical "
    "question the construction raises but does not yet answer from first principles.")
splice("G12", "COR/DATA", "Section 6.1: comparison updated to PDG 2024; sin reading excluded; tan reading post hoc",
    "The observed value is 0.2250 ± 0.0007 (PDG 2022). Error: 2.6%. Both integers arise from the combinatorial "
    "topology of the Császár triangulation: 3 from the Fano incidence structure, 13 from the homology of the torus. "
    "No free parameters.",
    "**Comparison with data (corrected in v6.4).** Earlier versions compared 3/13 with sin θ_C = |V_us| and reported "
    "a 2.6% overshoot against 0.2250 ± 0.0007 (PDG 2022). Against PDG 2024 that reading is excluded: 3/13 lies "
    "7.6σ above |V_us| = 0.22431 ± 0.00085 and 8.5σ above the global-fit value λ = 0.22501 ± 0.00068. The ratio "
    "does agree with tan θ_C = |V_us/V_ud|: with |V_ud| = 0.97367 ± 0.00032, the ratio is 0.2304 ± 0.0009 from the "
    "averaged |V_us| (3/13 lies 0.4σ above it) and 0.2311 ± 0.0004 from the K_μ2/π_μ2 determination of |V_us| "
    "(0.8σ below), and the global fit gives 0.2309 ± 0.0007 (0.2σ below). Both integers arise from the "
    "combinatorial topology of the Császár triangulation, but the construction derives a number, not the observable "
    "it should be compared with, and the tan θ_C reading was found only after the comparison with data. It is "
    "therefore recorded as a post-hoc observation (Section 9, Conjecture 3), not as a derivation or a prediction.")

# ---------------------------------------------------------------- G13 Section 8
splice("G13", "FACT", "Section 8: chirality given its combinatorial basis",
    "It is therefore intrinsically chiral, existing as two non-superimposable enantiomers ℳ_L and ℳ_R.",
    "The absence of improper symmetries does not depend on the coordinates chosen: all 42 automorphisms of the "
    "triangulated torus (the "
    "group AGL(1,7) of Section 3) preserve the orientation of the surface, while a mirror plane, a center of "
    "symmetry or a rotoreflection axis would each induce an orientation-reversing automorphism, so no realization "
    "in ℝ³ has any of them. It is therefore intrinsically chiral, existing as two non-superimposable enantiomers "
    "ℳ_L and ℳ_R.")

# ---------------------------------------------------------------- G14-G16 Section 9
splice("G14", "WD", "Section 9: verified claim (3) withdrawn",
    "(3) Hypercharges (0, +1/3, −2/3, +1) follow from Y = (−1)^(N+1) × N/3. Any deviation in hypercharge "
    "quantization would falsify the construction.",
    "(3) *Withdrawn in v6.4.* Earlier versions listed the hypercharges (0, +1/3, −2/3, +1) from "
    "Y = (−1)^(N+1) × N/3; that operator is withdrawn (Section 5). The charge spectrum of the three-mode Fock space "
    "is Furey's Q = N/3 (Furey 2015), and this paper's contribution there, the identification of the three modes "
    "with the three Hamiltonian 7-cycles of K₇, is a construction rather than a verifiable claim.")
splice("G15", "WD", "Section 9: verified claim (5) withdrawn from the verified list",
    "(5) The Cabibbo angle sin(θ_C) = 3/13 = 0.2308, within 2.6% of the PDG value, where both 3 and 13 are "
    "topological invariants of the Császár triangulation.",
    "(5) *Withdrawn from this list in v6.4.* Earlier versions listed the Cabibbo angle sin(θ_C) = 3/13 = 0.2308, "
    "within 2.6% of the PDG value. Against PDG 2024 that statement is excluded at 7.6σ–8.5σ (Section 6.1). The "
    "agreement of 3/13 with tan θ_C is listed below as Conjecture 3.")
splice("G16", "COR", "Section 9: Conjecture 3 (post-hoc observation) added",
    "(2) |V_cb| = 3/[13(φ+4)] = 0.04108, within 0.7% of PDG. The golden ratio suppression factor lacks a prior "
    "address in the Császár geometry.",
    "(2) |V_cb| = 3/[13(φ+4)] = 0.04108, within 0.7% of PDG. The golden ratio suppression factor lacks a prior "
    "address in the Császár geometry.\n\n"
    "(3) *Post-hoc observation.* 3/13 = tan θ_C = |V_us/V_ud|, within 0.8σ of every PDG 2024 determination (Section "
    "6.1). Both integers are topological invariants of the Császár triangulation, but the construction does not "
    "select tan θ_C over sin θ_C, and this reading was identified after comparison with data. It becomes a result "
    "only if a derivation fixes the observable before the comparison.")

# ---------------------------------------------------------------- G17 Section 10
splice("G17", "COR", "Open Problem (ix) restated; RG running closed negative",
    "(ix) Whether the 2.6% overshoot on sin(θ_C) = 3/13 is attributable to renormalization group running from the "
    "compactification scale.",
    "(ix) Which observable, if any, the ratio 3/13 determines. Read as sin θ_C it is excluded (Section 6.1); read as "
    "tan θ_C it agrees, but that reading is post hoc (Conjecture 3). Renormalization-group running cannot rescue the "
    "sin θ_C reading: in the Standard Model the Wolfenstein parameter λ changes only by O(10⁻⁴) between the weak and "
    "Planck scales (Grossman et al. 2022), far below the 2.6% gap. (Versions through v6.3 asked instead whether such "
    "running could account for the overshoot.)")

# ---------------------------------------------------------------- G18/G19 Section 11
splice("G18", "COR", "Section 11: mixing-angle wording scoped",
    "been used to derive gauge group structure or quark mixing angles.",
    "been used to derive gauge group structure or to propose values for quark mixing parameters.")
splice("G19", "COR", "Section 11: 'Cabibbo 3/13 result' -> 'the 3/13 ratio'",
    "so the Cabibbo 3/13 result and the Fano⁺/Fano⁻ doublet-mismatch mechanism of Section 6 remain",
    "so the 3/13 ratio of Section 6.1 and the Fano⁺/Fano⁻ doublet-mismatch mechanism of Section 6 remain")

# ---------------------------------------------------------------- G20-G22 Section 12
splice("G20", "COR", "Section 12: hypercharge sentence corrected",
    "three generations via Fano line valence, and exact hypercharges via Fock space grading.",
    "three generations via Fano line valence, and a geometric carrier, the three Hamiltonian cycles, for the modes "
    "of Furey's number-operator charge.")
splice("G21", "COR", "Section 12: Cabibbo sentence corrected",
    "The Cabibbo angle sin(θ_C) = 3/13 is derived from the ratio of the Fano valence to the rank of the boundary "
    "operator in the Császár triangulation, both topological invariants of the polyhedron, within 2.6% of the PDG "
    "value.",
    "The ratio of the Fano valence to the rank of the boundary operator in the Császár triangulation, 3/13, built "
    "from two topological invariants of the polyhedron, is excluded as sin θ_C by PDG 2024 and agrees with tan θ_C; "
    "because that reading was identified after the comparison with data, it is recorded as a post-hoc observation "
    "(Conjecture 3).")
splice("G22", "COR", "Section 12: claim and conjecture counts",
    "Five claims are presented as verifiable results; two conjectures and eleven open problems are explicitly "
    "identified as unsolved.",
    "Three claims are presented as verifiable results, two others having been withdrawn in v6.4 (Section 9); three "
    "conjectures, one of them a post-hoc observation, and eleven open problems are explicitly identified as "
    "unsolved.")

# ---------------------------------------------------------------- G23 references (EOF-anchored)
t = th["t"]
start = t.index("[17] Günaydin")
old_tail = t[start:]
assert old_tail.endswith("PNAS 60(2), 438–445.")
new_tail = """[17] Grossman, Y., Ismail, A., Ruderman, J. T. & Tsai, T.-H. (2022). CKM substructure from the weak to the Planck scale. J. High Energy Phys. 06, 065.

[18] Günaydin, M. & Gürsey, F. (1973). Quark structure and the octonions. J. Math. Phys. 14 (11), 1651–1667.

[19] Gürsey, F. & Tze, C.-H. (1996). On the Role of Division, Jordan and Related Algebras in Particle Physics. World Scientific.

[20] Heawood, P. J. (1890). Map-colour theorem. Quart. J. Math. 24, 332–338.

[21] Krasnov, K. (2018). Fermions, differential forms and doubled geometry. Nucl. Phys. B 936, 36–75.

[22] Krasnov, K. (2024). Geometry of Spin(10) symmetry breaking. J. Math. Phys. 65, 082302.

[23] Particle Data Group (2022). Review of Particle Physics. PTEP 2022, 083C01.

[24] Particle Data Group (2024). Review of Particle Physics. Phys. Rev. D 110, 030001.

[25] Ringel, G. & Youngs, J. W. T. (1968). Solution of the Heawood map-coloring problem. PNAS 60(2), 438–445."""
splice("G23", "REF", "References: Grossman et al. (2022) at 17 and PDG (2024) at 24 inserted alphabetically; tail renumbered to 25",
    old_tail, new_tail)

# ---------------------------------------------------------------- write + verify
final = th["t"]
os.makedirs(OUT, exist_ok=True)
open(DST, "w", encoding="utf-8").write(final)
md5_after = hashlib.md5(final.encode("utf-8")).hexdigest()
print(f"[v6.3] md5 = {md5_before}")
print(f"[v6.4 DRAFT] md5 = {md5_after}; bytes {len(text.encode())} -> {len(final.encode())}; "
      f"lines {len(text.splitlines())} -> {len(final.splitlines())}")

recon = final
for hid, tags, desc, old, new in reversed(HUNKS):
    assert recon.count(new) == 1, f"reverse: {hid} new not unique"
    recon = recon.replace(new, old)
assert hashlib.md5(recon.encode("utf-8")).hexdigest() == md5_before, "reverse-splice FAILED"
print("reverse-splice reconstruction: OK (v6.4 draft minus hunks == v6.3 byte-exact)")

# structural checks
issues = []
body = final[:final.index("[1] Bokowski")]
refs = final[final.index("[1] Bokowski"):]          # to EOF
nums = [int(m.group(1)) for m in re.finditer(r"^\[(\d+)\]", refs, re.M)]
if nums != list(range(1, 26)):
    issues.append(f"reference numbering not 1..25: {nums}")
if re.findall(r"\[\d+\]", body):
    issues.append("bracket-number citation in body")
if body.count("(Grossman et al. 2022)") != 2 or refs.count("Grossman, Y., Ismail") != 1:
    issues.append("Grossman et al. citation/reference count")
if "PDG 2024" not in body or refs.count("Particle Data Group (2024)") != 1:
    issues.append("PDG 2024 citation/reference")
paras = body.split("\n\n")
for p in paras:
    if "(−1)^(N+1)" in p and "withdrawn" not in p.lower():
        issues.append("dressing formula outside a withdrawal context: " + p[:80])
    if "sin(θ_C) = 3/13" in p and not ("Withdrawn" in p or "excluded" in p):
        issues.append("sin(θ_C) = 3/13 outside a withdrawal context: " + p[:80])
for lab in ["2018a", "2018b", "2018c", "2022a", "2022b", "Gourlay & Gresnigt 2024"]:
    if lab not in body:
        issues.append(f"label {lab} lost from body")
for k in ("(1) SU(3) arises", "(2) Three fermion generations", "(3) *Withdrawn in v6.4.*", "(4) The rank-4",
          "(5) *Withdrawn from this list in v6.4.*", "(3) *Post-hoc observation.*"):
    if body.count(k) != 1:
        issues.append(f"Section 9 item missing or duplicated: {k}")
print("structural issues:", issues if issues else "none")
assert not issues

# ---------------------------------------------------------------- change-log table rows (for V64_CHANGE_LOG.md)
rows = "\n".join(f"| {hid} | {tags} | {desc.replace('|', chr(92) + '|')} |" for hid, tags, desc, _, _ in HUNKS)
open(os.path.join(OUT, "v64_hunk_table.md"), "w", encoding="utf-8").write(
    "| Hunk | Tags | Description |\n|---|---|---|\n" + rows + "\n")
print(f"hunks: {len(HUNKS)}; table written to v64_hunk_table.md")
with open(__file__, "rb") as fh:
    print("edit script md5:", hashlib.md5(fh.read()).hexdigest())
