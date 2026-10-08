#!/usr/bin/env python3
"""B3 DRAFT: SQTCalculator.jsx v2.0 -> v2.1 (status corrections). Nothing is published.

Run on the project-store file:  python3 patch_SQTCalculator_v2_1.py path/to/SQTCalculator.jsx [OUT_DIR]
No canonical md5 of v2.0 is on record, so the script prints the input md5 and relies on unique-anchor asserts:
if any anchor is missing or repeated, it stops without writing. Reverse splice must reproduce the input exactly.
The preview committed beside this script was built from the store file's text as returned by the project read of
October 7, 2026 (md5 503930f056fa0306095f91a80970a506, 18,676 bytes; see B3_RESULT.md).
"""
import hashlib, os, sys

SRC = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(OUT, "SQTCalculator_v2_1_DRAFT.jsx")
text = open(SRC, encoding="utf-8").read()
md5_before = hashlib.md5(text.encode("utf-8")).hexdigest()
print("input md5:", md5_before)
th = {"t": text}
HUNKS = []

def splice(hid, desc, old, new):
    t = th["t"]
    assert t.count(old) == 1, f"{hid}: anchor not unique (count={t.count(old)}) — {old[:60]!r}"
    th["t"] = t.replace(old, new)
    assert th["t"].count(new) == 1, f"{hid}: new text not unique"
    HUNKS.append((hid, desc, old, new))

splice("J1", "header comment scoped",
    "//  All constants derived from φ, π, and knot topology.\n//  No free parameters tuned to mass targets.",
    "//  Leading-order fit: one anchor (m_e), one selected scale (ξ_vac = 100φ) and\n"
    "//  per-particle selections (knot, A, Z_f, L). Not a zero-parameter derivation.\n"
    "//  v2.1 DRAFT (October 2026): status corrections per ledger §2.92; PDG 2024 values.")
splice("J2", "ξ_vac comment",
    "const XI_VAC  = 100 * phi;                                  // ξ_vac = 100φ ≈ 161.8",
    "const XI_VAC  = 100 * phi;                                  // ξ_vac = 100φ ≈ 161.8 (selected; no combinatorial address, §2.64.A)")
splice("J3", "A_B comment",
    "const A_B  = 20;   // Alexander polynomial: Σcoeff² = 1+9+9+1",
    "const A_B  = 20;   // Σcoeff² of Δ(t,t,t) = 1+9+9+1 (the standard one-variable Δ gives 70)")
splice("J4", "source-column legend",
    "// Source column: G = geometry-pinned, C = conjecture, F = fitted",
    "// Source column: A = anchor, C = conjecture, F = fitted, R = inverted (not a prediction)")
for hid, old, new in [
    ("J5a", 'obs:0.511,    src:"G", note:"L=2π from spinor closure; Zf=1 trivial" },',
            'obs:0.511,    src:"A", note:"Calibration anchor: m₀ is set from m_e (A=1, Zf=1, L=2π); the formula returns 0.4925 MeV (−3.6%), the r_eff(2π) slack" },'),
    ("J5b", 'obs:2.2,      src:"C", note:"A=crossing number; Zf=Fano base; L≈Φφ²" },',
            'obs:2.16,     src:"C", note:"A=crossing number; Zf=Fano base; L≈Φφ². PDG 2024 2.16 ± 0.07 MeV: output outside the band (−5.6%)" },'),
    ("J5c", "obs:4.67,     src:\"C\"", "obs:4.70,     src:\"C\""),
    ("J5d", "obs:93,       src:\"C\"", "obs:93.5,     src:\"C\""),
    ("J5e", "obs:1270,     src:\"C\"", "obs:1273.0,   src:\"C\""),
    ("J5f", "obs:1776.86,  src:\"C\"", "obs:1776.93,  src:\"C\""),
    ("J5g", "obs:4180,     src:\"C\"", "obs:4183,     src:\"C\""),
    ("J5h", 'obs:172690,   src:"F", note:"Top quark: known ~2.6× discrepancy; open problem" },',
            'obs:172570,   src:"F", note:"Zf=κ/8=1/(8φ⁴) is fitted (ledger §2.92 counts it among the six fitted Z_f); −0.80% against PDG 2024" },'),
    ("J5i", 'obs:938.272,  src:"G", note:"A=20 from Alexander poly; Zf=6=|F₇*|; L solved" },',
            'obs:938.272,  src:"R", note:"INVERTED: L_B is solved from m_p, so the match is by construction. A=20 uses Δ(t,t,t) (standard Δ gives 70); Zf=6 is Conjecture 1. At the ideal ropelength (≤ 58.006) the formula gives ≈759 MeV" },'),
]:
    splice(hid, "particle row (PDG 2024 / status)", old, new)
splice("J6", "source labels",
    'function srcColor(s) {\n  if (s === "G") return C.grn;\n  if (s === "C") return C.cya;\n  return C.org;\n}\n'
    'function srcLabel(s) {\n  if (s === "G") return "DERIVED";\n  if (s === "C") return "CONJECTURE";\n  return "OPEN";\n}',
    'function srcColor(s) {\n  if (s === "A" || s === "G") return C.grn;\n  if (s === "C") return C.cya;\n  if (s === "R") return C.red;\n  return C.org;\n}\n'
    'function srcLabel(s) {\n  if (s === "A") return "ANCHOR";\n  if (s === "G") return "DERIVED";\n  if (s === "C") return "CONJECTURE";\n'
    '  if (s === "F") return "FIT";\n  if (s === "R") return "INVERTED";\n  return "OPEN";\n}')
splice("J7a", "proton panel: values at the ideal length",
    "  const pred = massFn(A_B, ZF_B, L_B);\n  const err  = pct(pred, 938.272);\n  return (",
    "  const pred = massFn(A_B, ZF_B, L_B);\n  const predIdeal = massFn(A_B, ZF_B, L_B_IDEAL_MAX);\n  const errIdeal  = pct(predIdeal, 938.272);\n  return (")
splice("J7b", "proton panel: title",
    "        OPEN PROBLEM 5 · BORROMEAN BARYON MASS\n",
    "        BORROMEAN BARYON MASS · ROPELENGTH PREDICTION FALSIFIED AT LEADING ORDER\n")
splice("J7c", "proton panel: details",
    '        <Detail label="A = Σcoeff² (Alexander poly)" val="20" />\n'
    '        <Detail label="Zf = |F₇*|" val="6" />\n'
    '        <Detail label="L_B (solved)" val={`${L_B.toFixed(3)} fm`} />\n'
    '        <Detail label="Ashton bounds" val="[58.006, 62.0] fm" />\n'
    '        <Detail label="Predicted m_p" val={fmtMeV(pred)} hi />\n'
    '        <Detail label="PDG m_p" val="938.272 MeV" />\n'
    '        <Detail label="Error" val={fmtPct(err)} />',
    '        <Detail label="A = Σcoeff² of Δ(t,t,t)" val="20 (standard Δ: 70)" />\n'
    '        <Detail label="Zf = |F₇*| (Conjecture 1)" val="6" />\n'
    '        <Detail label="L_B (solved from m_p)" val={`${L_B.toFixed(3)} fm`} />\n'
    '        <Detail label="Ideal ropelength" val={`≤ ${L_B_IDEAL_MAX} fm`} />\n'
    '        <Detail label="m_p at L_B (by construction)" val={fmtMeV(pred)} />\n'
    '        <Detail label="m_p at 58.006" val={fmtMeV(predIdeal)} hi />\n'
    '        <Detail label="PDG m_p" val="938.272 MeV" />\n'
    '        <Detail label="Error at 58.006" val={fmtPct(errIdeal)} />')
splice("J7d", "proton panel: text",
    "        L_B = {L_B.toFixed(3)} fm falls within Ashton ropelength bounds [{L_B_BOUNDS_LO}, {L_B_BOUNDS_HI}] fm.\n"
    "        A=20 derived from Borromean Alexander polynomial. Zf=6=|F₇*| is Conjecture 1 (Riemann-Hurwitz proof pending).",
    "        L_B = {L_B.toFixed(3)} fm is the proton mass run backwards, so matching m_p is not a test. 58.006 is the length of\n"
    "        the presumed-minimal tight Borromean rings (Cantarella–Fu–Kusner–Sullivan–Wrinkle 2006), so the ideal ropelength is at\n"
    "        most 58.006, where the formula gives about 759 MeV: the ropelength prediction is falsified at leading order (ledger\n"
    "        §2.15 retracted to Conjecture, §2.92). A=20 uses Δ(t,t,t); the standard one-variable Alexander polynomial gives 70.\n"
    "        Zf=6=|F₇*| is Conjecture 1 (Riemann-Hurwitz proof pending).")
splice("J7e", "ideal-length constant replaces the bounds",
    "const L_B_BOUNDS_LO = 58.006;\nconst L_B_BOUNDS_HI = 62.0;",
    "const L_B_IDEAL_MAX = 58.006;   // presumed-minimal tight Borromean rings (CFKSW 2006): ideal ropelength ≤ 58.006")
splice("J8a", "constants: sources",
    '    { label: "Φ (throat angle)",    val: PHI.toFixed(6),    src: "derived: 2π − φ²/8π²" },\n'
    '    { label: "m₀ (base mass)",      val: `${m0.toFixed(5)} MeV`, src: "derived: 0.511/exp(2π/Φ)" },\n'
    '    { label: "κ (bulk modulus)",     val: kappa.toFixed(6),  src: "derived: φ⁻⁴" },\n'
    '    { label: "ξ_vac (corr. length)",val: `${XI_VAC.toFixed(3)} fm`, src: "derived: 100φ" },',
    '    { label: "Φ (throat angle)",    val: PHI.toFixed(6),    src: "structural form 2π − φ²/8π² (Register 2)" },\n'
    '    { label: "m₀ (base mass)",      val: `${m0.toFixed(5)} MeV`, src: "anchor: m_e/exp(2π/Φ)" },\n'
    '    { label: "κ (bulk modulus)",     val: kappa.toFixed(6),  src: "φ⁻⁴" },\n'
    '    { label: "ξ_vac (corr. length)",val: `${XI_VAC.toFixed(3)} fm`, src: "selected: 100φ (no combinatorial address)" },')
splice("J8b", "constants: title",
    "        DERIVED CONSTANTS · ZERO FREE PARAMETERS",
    "        CONSTANTS · ONE ANCHOR (m_e) · ONE SELECTED SCALE (ξ_vac)")
splice("J9", "header paragraph",
    "            Particle masses derived from knot topology, division algebra structure,\n"
    "            and Fano plane combinatorics. Constants flow from φ and π — no mass targets\n"
    "            were consulted in constructing the geometric parameters.",
    "            A leading-order fit of particle masses to knot topology, division algebra structure\n"
    "            and Fano plane combinatorics: one anchor (m_e), one selected scale (ξ_vac = 100φ) and\n"
    "            per-particle selections (knot, A, Z_f, L). Not a zero-parameter derivation; PDG 2024 values.")
splice("J10", "header badges",
    '            <Badge label="DERIVED" col={C.grn} />\n            <Badge label="CONJECTURE" col={C.cya} />',
    '            <Badge label="ANCHOR" col={C.grn} />\n            <Badge label="FIT" col={C.org} />\n'
    '            <Badge label="CONJECTURE" col={C.cya} />\n            <Badge label="INVERTED" col={C.red} />')
splice("J11", "constants toggle label",
    '{showConst ? "▼" : "▶"} DERIVED CONSTANTS',
    '{showConst ? "▼" : "▶"} CONSTANTS')
splice("J12", "table footnote",
    "Click any row to expand geometric parameters. Top quark is a known open problem (~2.6× discrepancy).",
    "Click any row to expand geometric parameters. This table is a leading-order fit (about nine selected inputs for eight\n"
    "          rows; ledger §2.92). Against PDG 2024 only b, t and τ fall within 2%.")
splice("J13", "footer",
    "          Gauge group paper: <span style={{ color: C.cya }}>arXiv (Császár polyhedron)</span> &nbsp;·&nbsp;\n"
    "          Ropelength paper: <span style={{ color: C.cya }}>arXiv (Paper 1A)</span><br/>\n"
    "          Parameters labeled CONJECTURE or OPEN PROBLEM are structural but not yet formally derived.\n"
    "          Top quark discrepancy is documented and under investigation.",
    "          Gauge group paper: <span style={{ color: C.cya }}>Zenodo record 21316171 (Császár polyhedron)</span> &nbsp;·&nbsp;\n"
    "          Ropelength paper: <span style={{ color: C.cya }}>Paper 1A</span><br/>\n"
    "          Parameters labeled CONJECTURE or OPEN PROBLEM are structural but not yet formally derived.\n"
    "          v2.1 DRAFT (October 2026): status corrections per ledger §2.92.")

splice("J14", "pass badge: anchor and inverted rows are not tests; the top is counted",
    '  const passing = PARTICLES.filter(p => {\n    const e = Math.abs(pct(massFn(p.A, p.Zf, p.L), p.obs));\n'
    '    return e < 8 && p.id !== "t";\n  }).length;',
    '  const outputs = PARTICLES.filter(p => p.src !== "A" && p.src !== "R");   // the anchor and the inverted row are not tests\n'
    '  const within  = lim => outputs.filter(p => Math.abs(pct(massFn(p.A, p.Zf, p.L), p.obs)) < lim).length;')
splice("J14b", "pass badges",
    '            <Badge label={`${passing}/9 WITHIN 8%`} col={C.grn} />',
    '            <Badge label={`${within(2)}/${outputs.length} WITHIN 2%`} col={C.grn} />\n'
    '            <Badge label={`${within(8)}/${outputs.length} WITHIN 8%`} col={C.grn} />')
splice("J15", "mass-operator legend: L conventions named",
    "            A = knot winding index &nbsp;·&nbsp; Zf = topological partition factor &nbsp;·&nbsp; L = ropelength (fm)",
    "            A = knot winding index &nbsp;·&nbsp; Zf = topological partition factor &nbsp;·&nbsp; L = ropelength (fm)<br/>\n"
    "            L conventions are mixed: the quark values are ideal ropelengths per tube diameter (trefoil 16.372 = 32.743 per\n"
    "            radius; no nontrivial knot is below 31.32 per radius), while L_e = 2π and the Borromean 58.006 are per radius.")

final = th["t"]
os.makedirs(OUT, exist_ok=True)
open(DST, "w", encoding="utf-8").write(final)
recon = final
for hid, desc, old, new in reversed(HUNKS):
    assert recon.count(new) == 1, f"reverse: {hid}"
    recon = recon.replace(new, old)
assert recon == text, "reverse-splice FAILED"
left = [s for s in ("ZERO FREE PARAMETERS", "No free parameters", "Ashton", "L_B_BOUNDS", "no mass targets") if s in final]
assert not left, left
print(f"{len(HUNKS)} hunks; output md5 {hashlib.md5(final.encode()).hexdigest()}; reverse splice OK; wrote {DST}")
