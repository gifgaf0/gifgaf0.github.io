#!/usr/bin/env python3
"""B3 DRAFT: sqt_v20_merged.jsx (SQT v1.9) -> v1.9.1 DRAFT (status corrections). Nothing is published.

Run on the project-store file:  python3 patch_sqt_v19_merged.py path/to/sqt_v20_merged.jsx [OUT_DIR]
Input of record: the store file's text as returned by the project read of October 7, 2026
(md5 b62b2a752871a2426066124be42cac8b, 122,906 bytes). The script checks that md5, asserts every anchor unique,
writes sqt_v19_1_DRAFT.jsx and verifies that the reverse splice reproduces the input byte-exact.
Scope (brief B3 and the A3 blast radius): "zero free parameters" wording; the retired electroweak formulas;
the Borromean panel (inverted length, falsified ropelength prediction, A = 20 vs 70, F7* not in PSL(2,7));
the top-quark Z_f status; PDG 2024 comparison values; the mixed L conventions.
"""
import hashlib, os, sys

SRC = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(OUT, "sqt_v19_1_DRAFT.jsx")
V19_MD5 = "b62b2a752871a2426066124be42cac8b"
text = open(SRC, encoding="utf-8").read()
md5_before = hashlib.md5(text.encode("utf-8")).hexdigest()
assert md5_before == V19_MD5, f"input is not the v1.9 file of record (md5 {md5_before})"
th = {"t": text}
HUNKS = []

def splice(hid, desc, old, new):
    t = th["t"]
    assert t.count(old) == 1, f"{hid}: anchor not unique (count={t.count(old)}) — {old[:70]!r}"
    th["t"] = t.replace(old, new)
    assert th["t"].count(new) == 1, f"{hid}: new text not unique"
    HUNKS.append((hid, desc, old, new))

def splice_span(hid, desc, start, end, new):
    """Replace the text from the unique marker `start` up to (not including) the unique marker `end`."""
    t = th["t"]
    assert t.count(start) == 1 and t.count(end) == 1, f"{hid}: span markers not unique"
    i, j = t.index(start), t.index(end)
    assert i < j, f"{hid}: span markers out of order"
    splice(hid, desc, t[i:j], new)

# ---------------------------------------------------------------- constants and header comment
splice("K1", "header comment: no 'zero free parameters'",
    "//  SQT v1.8 · DERIVED CONSTANTS (zero free parameters)",
    "//  SQT v1.9.1 DRAFT (October 2026) · CONSTANTS: one anchor (m_e), one selected scale (ξ_vac = 100φ)\n"
    "//  and per-particle selections (knot, A, Z_f, L). A leading-order fit, not a zero-parameter derivation (ledger §2.92).")
splice("K2", "ξ_vac labelled selected",
    "const XI_VAC = 100 * phi;\n",
    "const XI_VAC = 100 * phi;   // selected scale; no combinatorial address (ledger §2.64.A)\n")
splice("K3", "particle table: sources and L conventions",
    "const ZF_LEPTON = 1 / (2 * Math.PI);\nconst PARTICLES = [",
    "const ZF_LEPTON = 1 / (2 * Math.PI);\n"
    "// obs: PDG 2024 (Navas et al., PRD 110, 030001): u, d, s M̄S at 2 GeV; c, b M̄S at their own scale; top direct.\n"
    "// L: per-particle selected lengths, in mixed conventions. The quark values are ideal ropelengths per tube DIAMETER\n"
    "// (trefoil 16.372 = 32.743 per radius; no nontrivial knot is below 31.32 per radius); L_e = 2π and the Borromean\n"
    "// 58.006 are per RADIUS (audit B3, October 2026).\n"
    "const PARTICLES = [")
for hid, old, new in [
    ("K4a", 'obs:2.2,     gen:"I"',    'obs:2.16,    gen:"I"'),
    ("K4b", 'obs:4.67,    gen:"I"',    'obs:4.70,    gen:"I"'),
    ("K4c", 'obs:93,      gen:"II"',   'obs:93.5,    gen:"II"'),
    ("K4d", 'obs:1270,    gen:"II"',   'obs:1273.0,  gen:"II"'),
    ("K4e", 'obs:4180,    gen:"III"',  'obs:4183,    gen:"III"'),
    ("K4f", 'obs:172690,  gen:"III"',  'obs:172570,  gen:"III"'),
    ("K4g", 'obs:1776.86, gen:"III"',  'obs:1776.93, gen:"III"'),
]:
    splice(hid, "particle table: PDG 2024", old, new)
splice("K5", "Borromean constants: A, Z_f and the 58.006 / 62.0 numbers",
    "const A_BORROMEAN  = 20;   // Borromean Alexander polynomial: Σ coeff² = 1+9+9+1\n"
    "const ZF_BORROMEAN = 6;    // |F₇*| — scalar action of multiplicative group of F₇\n"
    "const L_B_BOUNDS   = { lo: 58.006, hi: 62.0 };  // Ashton et al. 2011",
    "const A_BORROMEAN  = 20;   // Σ coeff² of the diagonal Δ(t,t,t) = 1+9+9+1; the one-variable Alexander polynomial (t−1)⁴ gives 70\n"
    "const ZF_BORROMEAN = 6;    // Conjecture 1 (|F₇*| = 6; F₇* ≅ Z₆ is not a subgroup of PSL(2,7), whose Fano-triangle stabilizer is S₃)\n"
    "const L_B_BOUNDS   = { lo: 58.006, hi: 62.0 };  // lo: presumed-minimal tight Borromean rings (CFKSW 2006), an UPPER bound on the\n"
    "                                                 // ideal ropelength, not a lower one; hi: no source, kept only for the slider scale")
splice("K6", "L_B comment: an inversion",
    "const L_B_PREDICTED = borromeanL(938.272);  // 60.194 fm",
    "const L_B_PREDICTED = borromeanL(938.272);  // 60.194: m_p run backwards (an inversion, not a prediction; ledger §2.92)")

# ---------------------------------------------------------------- Tab 1, mass audit
splice("M1", "mass audit: title and status banner",
    "      <SectionHead col={CYA}>THEOREM 1 · LOCAL MASS OPERATOR — PRECISION AUDIT v1.8</SectionHead>\n",
    "      <SectionHead col={CYA}>THEOREM 1 · LOCAL MASS OPERATOR — LEADING-ORDER FIT AUDIT v1.9.1</SectionHead>\n"
    "      <div style={{ background:\"#0f0a00\", border:`1px solid ${AMB}55`, borderLeft:`3px solid ${AMB}`, borderRadius:4, padding:\"10px 14px\", marginBottom:16, fontSize:11, color:GRY, lineHeight:1.7 }}>\n"
    "        <span style={{ fontFamily:MONO, fontSize:9, color:AMB, letterSpacing:1 }}>STATUS · OCTOBER 2026 · </span>\n"
    "        This table is a leading-order fit, not a set of predictions: one anchor (m_e), one selected scale (ξ_vac = 100φ) and\n"
    "        per-particle selections (knot, A, Z_f, L). Observed values are PDG 2024; against them only b, t and τ fall within 2%.\n"
    "        The electron row is the anchor (the formula returns 0.4925 MeV at L = 2π, the r_eff(2π) slack). Ledger §2.92.\n"
    "      </div>\n")
splice("M2", "mass audit: L conventions under the formula",
    "          <br/><span style={{ color:GRY }}>reff = 1 + ln(1 + L/ξvac) &nbsp;|&nbsp; Lepton Zf = 1/2π (v1.8) &nbsp;|&nbsp; Top Zf = 1/(8φ⁴)</span>\n",
    "          <br/><span style={{ color:GRY }}>reff = 1 + ln(1 + L/ξvac) &nbsp;|&nbsp; Lepton Zf = 1/2π (v1.8) &nbsp;|&nbsp; Top Zf = 1/(8φ⁴)</span>\n"
    "          <br/><span style={{ color:GRY }}>L: the quark values are per tube diameter; L_e = 2π and the Borromean 58.006 are per radius</span>\n")

# ---------------------------------------------------------------- generation cards and leptons: PDG 2024
for hid, old, new in [
    ("G1", 'L:16.372, obs:2.2, col:GRN, tag:"MINIMAL RESONANCE"', 'L:16.372, obs:2.16, col:GRN, tag:"MINIMAL RESONANCE"'),
    ("G2", 'L:21.04, obs:4.67, col:CYA, tag:"AMPHICHEIRAL TORQUE"', 'L:21.04, obs:4.70, col:CYA, tag:"AMPHICHEIRAL TORQUE"'),
    ("G3", 'L:29.13, obs:93, col:"#f59e0b"', 'L:29.13, obs:93.5, col:"#f59e0b"'),
    ("G4", 'L:23.60, obs:1270, col:ORG', 'L:23.60, obs:1273.0, col:ORG'),
    ("G5", 'pred:botPred, obs:4180,', 'pred:botPred, obs:4183,'),
    ("G6", 'pred:topPred, obs:172690,', 'pred:topPred, obs:172570,'),
    ("G7", 'L:3*L0, obs:1776.86, pred:tauPred', 'L:3*L0, obs:1776.93, pred:tauPred'),
    ("G8", '({pct(tauPred,1776.86).toFixed(2)}%)', '({pct(tauPred,1776.93).toFixed(2)}%)'),
]:
    splice(hid, "cards: PDG 2024", old, new)

# ---------------------------------------------------------------- Tab 11, electroweak: retired
EW_NEW = r'''function ElectroweakSector() {
  // RETIRED AS PREDICTIONS (October 2026; ledger §2.92, audit B3). The formulas are kept as a record.
  const mW = m0 * Math.pow(phi, 27);
  const sin2 = Math.pow(phi, -3);
  const cosW = Math.sqrt(1 - sin2);
  const mZ = mW / cosW;
  const W_PDG = 80369.2, W_ERR = 13.3;   // PDG 2024 world average (MeV)
  const Z_PDG = 91188.0, Z_ERR = 2.0;    // PDG 2024 (MeV)
  const SIN2_PDG = [                     // PDG 2024 electroweak review, Table 10.2
    { l:"M̄S at M_Z",               v:0.23129, e:0.00004 },
    { l:"on-shell, 1 − M_W²/M_Z²", v:0.22348, e:0.00010 },
    { l:"effective leptonic",       v:0.23161, e:0.00004 },
    { l:"M̄S at Q → 0",             v:0.23873, e:0.00005 },
  ];
  const rows = [
    { q:"m_W", f:"m₀ · φ²⁷",                          pred:mW, obs:W_PDG, err:W_ERR },
    { q:"m_Z", f:"m_W / cos θ_W with sin²θ_W = φ⁻³", pred:mZ, obs:Z_PDG, err:Z_ERR },
  ];
  const th = { padding:"7px 10px", textAlign:"left", fontSize:9, color:GRY, whiteSpace:"nowrap" };
  const td = { padding:"7px 10px" };
  return (
    <div>
      <SectionHead col={GRY}>ELECTROWEAK FORMULAS · RETIRED AS PREDICTIONS (OCTOBER 2026)</SectionHead>
      <div style={{ background:"#1a0a0a", border:`1px solid ${RED}55`, borderLeft:`3px solid ${RED}`, borderRadius:4, padding:"10px 16px", marginBottom:20, fontSize:11, color:GRY, lineHeight:1.75 }}>
        <strong style={{ color:RED }}>RETIRED.</strong> m_W = m₀·φ²⁷ and sin²θ_W = φ⁻³ are no longer presented as predictions.
        The exponent 27 and the angle φ⁻³ are selected inputs (ledger §2.92 counts both among the mass table's selections);
        the step from 27 lattice degrees of freedom to the exponent was never derived (Paper VII OP.8), and φ⁻³ is stated
        at no energy scale or renormalization scheme. Against PDG 2024 the W mass is 2.19% high, more than 100 standard
        deviations. The numbers below are kept as a record.
      </div>
      <div style={{ overflowX:"auto", marginBottom:20 }}>
        <table style={{ width:"100%", borderCollapse:"collapse", fontFamily:MONO, fontSize:11 }}>
          <thead>
            <tr style={{ borderBottom:`1px solid ${BRD}` }}>
              {["Quantity","Formula (retired)","Value","PDG 2024","Δ","Pull"].map(h => <th key={h} style={th}>{h}</th>)}
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.q} style={{ borderBottom:`1px solid ${DIM}` }}>
                <td style={{ ...td, color:TXT }}>{r.q}</td>
                <td style={{ ...td, color:GRY }}>{r.f}</td>
                <td style={{ ...td, color:TXT }}>{fmtMeV(r.pred)}</td>
                <td style={{ ...td, color:GRY }}>{(r.obs/1000).toFixed(4)} ± {(r.err/1000).toFixed(4)} GeV</td>
                <td style={{ ...td, color:RED }}>{pct(r.pred, r.obs)>=0?"+":""}{pct(r.pred, r.obs).toFixed(2)}%</td>
                <td style={{ ...td, color:RED }}>{((r.pred - r.obs)/r.err).toFixed(0)}σ</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:8 }}>sin²θ_W = φ⁻³ = {sin2.toFixed(5)} AGAINST EACH STANDARD DEFINITION</div>
      <div style={{ overflowX:"auto" }}>
        <table style={{ width:"100%", borderCollapse:"collapse", fontFamily:MONO, fontSize:11 }}>
          <thead>
            <tr style={{ borderBottom:`1px solid ${BRD}` }}>
              {["Definition","PDG 2024","φ⁻³ − value"].map(h => <th key={h} style={th}>{h}</th>)}
            </tr>
          </thead>
          <tbody>
            {SIN2_PDG.map(s => (
              <tr key={s.l} style={{ borderBottom:`1px solid ${DIM}` }}>
                <td style={{ ...td, color:TXT }}>{s.l}</td>
                <td style={{ ...td, color:GRY }}>{s.v.toFixed(5)} ± {s.e.toFixed(5)}</td>
                <td style={{ ...td, color:AMB }}>{pct(sin2, s.v)>=0?"+":""}{pct(sin2, s.v).toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

'''
splice_span("E1", "electroweak tab: retired, with the record against PDG 2024",
    "function ElectroweakSector() {",
    "// ══════════════════════════════════════════════════════════════\n//  TAB 12 — LENS EQUATION",
    EW_NEW)

# ---------------------------------------------------------------- Tab 15, top-quark Z_f
splice("T1", "top: PDG 2024 mass",
    "const TOP_A = 119; const TOP_L = 37.31; const TOP_OBS = 172690;",
    "const TOP_A = 119; const TOP_L = 37.31; const TOP_OBS = 172570;   // PDG 2024 direct measurement")
splice("T2", "top: κ/8 candidate status and the 8 = 3³ arithmetic",
    '  { id:"phi8",   label:"1/(8φ⁴)", Zf:1/(8*phi4),   col:PRP,       verdict:"PREFERRED", verdictCol:PRP,\n'
    '    short:"Mod-8 vacuum × bulk modulus κ",\n'
    '    long:"Zf = κ/8 = (1/φ⁴)/8 = 1/(8φ⁴). Recycles κ = 1/φ⁴ (superfluid bulk modulus, Theorem 1) and b = 8 = 3³ (cubic vacuum base, Theorem 3). No new constants — both pre-derived independently with separate physical meanings." },',
    '  { id:"phi8",   label:"1/(8φ⁴)", Zf:1/(8*phi4),   col:PRP,       verdict:"SELECTED (FIT)", verdictCol:AMB,\n'
    '    short:"Mod-8 vacuum × bulk modulus κ",\n'
    '    long:"Zf = κ/8 = (1/φ⁴)/8 = 1/(8φ⁴). Combines κ = 1/φ⁴ (superfluid bulk modulus, Theorem 1) with b = 8 (the mod-8 base of Theorem 3; 8 = 2³, not 3³). Status (October 2026): a selected value — ledger §2.92 counts it among the six fitted Z_f." },')
splice("T3", "top: section title and status line",
    "      <SectionHead col={PRP}>TOP QUARK Zf RESOLUTION · REPLACING 1/144</SectionHead>\n",
    "      <SectionHead col={PRP}>TOP QUARK Zf RESOLUTION · REPLACING 1/144</SectionHead>\n"
    "      <div style={{ fontSize:11, color:GRY, lineHeight:1.7, marginBottom:14 }}>\n"
    "        <span style={{ fontFamily:MONO, fontSize:9, color:AMB, letterSpacing:1 }}>STATUS · OCTOBER 2026 · </span>\n"
    "        The candidates below are compared with the observed mass; whichever is kept is a fitted Z_f (ledger §2.92).\n"
    "        Observed: PDG 2024, 172.57 ± 0.29 GeV.\n"
    "      </div>\n")
splice("T4", "top: constant-reuse audit lines",
    '<div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="8" col={GRN}/><span style={{ fontSize:10, color:GRY }}>b = 3³ cubic vacuum — Theorem 3 ✓</span></div>\n'
    '                    <div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="κ/8" col={PRP}/><span style={{ fontSize:10, color:GRY }}>Zero new constants — both pre-derived ✓✓</span></div>',
    '<div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="8" col={GRN}/><span style={{ fontSize:10, color:GRY }}>b = 8, the mod-8 base of Theorem 3 (8 = 2³)</span></div>\n'
    '                    <div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="κ/8" col={AMB}/><span style={{ fontSize:10, color:GRY }}>A selected combination: counted as a fitted Z_f (ledger §2.92)</span></div>')
splice("T5", "top: target panel uses PDG 2024",
    "<div style={{ fontFamily:MONO, fontSize:13, color:TXT }}>172,690 MeV / {fmtMeV(mBase)}</div>",
    "<div style={{ fontFamily:MONO, fontSize:13, color:TXT }}>172,570 MeV / {fmtMeV(mBase)}</div>")
splice("T6", "top: observed line uses PDG 2024",
    "Observed: 172,690 MeV (172.69 GeV)</div>",
    "Observed: 172,570 MeV (PDG 2024)</div>")

# ---------------------------------------------------------------- Tab 17, baryon
splice("B1", "baryon: start the slider at the geometric length",
    "  const [lSlider, setLSlider] = useState(L_B_PREDICTED);",
    "  const [lSlider, setLSlider] = useState(L_B_BOUNDS.lo);   // start at the geometric length 58.006, not at the inversion")
splice("B2", "baryon: lengths on record",
    '    { L: L_B_BOUNDS.lo, src: "Ashton lower bound"       },\n'
    '    { L: L_B_PREDICTED, src: "SQT prediction (Z_f = 6)" },\n'
    '    { L: 60.0,          src: "Central estimate"          },\n'
    '    { L: L_B_BOUNDS.hi, src: "Upper estimate"            },',
    '    { L: L_B_BOUNDS.lo, src: "Ideal ropelength ≤ this (CFKSW 2006)" },\n'
    '    { L: 58.0526,       src: "Four-arc configuration (CKS 2002)"    },\n'
    '    { L: L_B_PREDICTED, src: "m_p inverted — not a prediction"      },')
splice("B3", "baryon: section title",
    "<SectionHead col={RED}>BARYON SECTOR · OPEN PROBLEM 5 · BORROMEAN TOPOLOGY</SectionHead>",
    "<SectionHead col={RED}>BARYON SECTOR · BORROMEAN TOPOLOGY · ROPELENGTH PREDICTION FALSIFIED AT LEADING ORDER</SectionHead>")
splice("B4", "baryon: status banner",
    "          <strong style={{ color:RED }}>LEADING-ORDER CONJECTURE</strong> — Paper VII pending.\n"
    "          A = 20 and Z_f = 6 are derived from topology and group theory. One verification remains:\n"
    "          numerical minimization of the ideal Borromean ropelength to &lt;1% precision.\n"
    "          Z_f = 6 is motivated by F₇* ⊂ PSL(2,7) but not yet proven with the rigour of single-particle Z_f values.",
    "          <strong style={{ color:RED }}>FALSIFIED AT LEADING ORDER (October 2026)</strong> — ledger §2.15 retracted to Conjecture (§2.92).\n"
    "          The ideal Borromean ropelength is at most 58.006, the length of the presumed-minimal tight configuration\n"
    "          (Cantarella, Fu, Kusner, Sullivan &amp; Wrinkle 2006), below the pre-stated window 60.194 ± 0.3; at 58.006 the formula\n"
    "          gives about 759 MeV (−19%). L_B = 60.194 is the proton mass run backwards, so the proton and neutron matches are\n"
    "          calibration outputs. A = 20 uses the diagonal Δ(t,t,t); the one-variable Alexander polynomial gives 70.\n"
    "          Z_f = 6 remains Conjecture 1.")
splice("B5", "baryon: A = 20 panel, the one-variable value",
    "            Flavor-blind: A(proton) = A(neutron) = 20.\n"
    "            Required for m_p ≈ m_n at leading order. ✓\n",
    "            Flavor-blind: A(proton) = A(neutron) = 20.\n"
    "            Required for m_p ≈ m_n at leading order. ✓<br/>\n"
    "            20 comes from the diagonal Δ(t,t,t); the one-variable Alexander polynomial, (t − 1)⁴, gives 70.\n")
splice("B6", "baryon: Z_f = 6 panel, the group statement",
    "            The symmetry preserving this configuration is the scalar multiplication action of F₇*,\n"
    "            the multiplicative group of the Galois field F₇.\n"
    "          </div>\n"
    "          <div style={{ background:DIM, borderRadius:4, padding:\"12px 14px\", fontFamily:MONO, fontSize:10, color:PRP, lineHeight:2 }}>\n"
    "            F₇* = &#123;1, 2, 3, 4, 5, 6&#125; ⊂ PSL(2,7)<br/>\n"
    "            <span style={{ color:GRY }}>Order = 6 (cyclic group Z₆)</span><br/>\n"
    "            <span style={{ color:PRP }}>Z_f(baryon) = |F₇*| = <strong>6</strong></span>",
    "            Its stabilizer in PSL(2,7) ≅ GL(3,2) is S₃, of order 6, permuting the three points. Conjecture 1\n"
    "            sets Z_f = |F₇*| = 6, the order of the multiplicative group of the Galois field F₇.\n"
    "          </div>\n"
    "          <div style={{ background:DIM, borderRadius:4, padding:\"12px 14px\", fontFamily:MONO, fontSize:10, color:PRP, lineHeight:2 }}>\n"
    "            Stab(Fano triangle) ≅ S₃ ⊂ PSL(2,7), order 6<br/>\n"
    "            <span style={{ color:GRY }}>F₇* ≅ Z₆ is not a subgroup of PSL(2,7): no element has order 6</span><br/>\n"
    "            <span style={{ color:PRP }}>Z_f(baryon) = <strong>6</strong> (Conjecture 1)</span>")
splice("B7", "baryon: Z_f grid note",
    '{ p:"Baryon", zf:"6",  note:"F₇* scalar action", hi:true },',
    '{ p:"Baryon", zf:"6",  note:"Conjecture 1", hi:true },')
splice("B8", "baryon: explorer title",
    "          ROPELENGTH PREDICTION · INTERACTIVE BOUNDS EXPLORER",
    "          ROPELENGTH · INTERACTIVE EXPLORER · IDEAL LENGTH ≤ 58.006")
splice("B9", "baryon: bar shows the allowed region and the inversion",
    "              {/* Ashton bounds region */}\n"
    "              <div style={{ position:\"absolute\",\n"
    "                left:`${barFrac(L_B_BOUNDS.lo)*100}%`,\n"
    "                width:`${(barFrac(L_B_BOUNDS.hi)-barFrac(L_B_BOUNDS.lo))*100}%`,\n"
    "                top:12, height:8, background:`${GRN}33`, borderRadius:2 }}/>\n"
    "              {/* Predicted marker */}\n"
    "              <div style={{ position:\"absolute\", left:`${barFrac(L_B_PREDICTED)*100}%`,\n"
    "                top:6, width:2, height:20, background:GRN, transform:\"translateX(-1px)\" }}/>",
    "              {/* region allowed for the ideal ropelength: at most 58.006 */}\n"
    "              <div style={{ position:\"absolute\",\n"
    "                left:\"0%\",\n"
    "                width:`${barFrac(L_B_BOUNDS.lo)*100}%`,\n"
    "                top:12, height:8, background:`${GRN}33`, borderRadius:2 }}/>\n"
    "              {/* the m_p-inverted length (60.194), outside the allowed region */}\n"
    "              <div style={{ position:\"absolute\", left:`${barFrac(L_B_PREDICTED)*100}%`,\n"
    "                top:6, width:2, height:20, background:RED, transform:\"translateX(-1px)\" }}/>")
splice("B10", "baryon: bar label 62.0 replaced by the inversion label",
    "              <div style={{ position:\"absolute\", left:`${barFrac(L_B_BOUNDS.hi)*100}%`,\n"
    "                bottom:0, fontSize:8, color:GRN, fontFamily:MONO, transform:\"translateX(-24px)\" }}>62.0</div>",
    "              <div style={{ position:\"absolute\", left:`${barFrac(L_B_PREDICTED)*100}%`,\n"
    "                bottom:0, fontSize:8, color:RED, fontFamily:MONO, transform:\"translateX(-12px)\" }}>60.194 (inverted)</div>")
splice("B11", "baryon: stat cells",
    '                { l:"Predicted L_B",    v:`${L_B_PREDICTED.toFixed(3)} fm`, c:GRN },\n'
    '                { l:"In Ashton bounds", v:L_B_BOUNDS.lo<=lSlider&&lSlider<=L_B_BOUNDS.hi?"YES ✓":"NO ✗",\n'
    '                  c:L_B_BOUNDS.lo<=lSlider&&lSlider<=L_B_BOUNDS.hi?GRN:RED },',
    '                { l:"L_B solved from m_p", v:`${L_B_PREDICTED.toFixed(3)} fm`, c:RED },\n'
    '                { l:"Slider ≤ 58.006 (ideal bound)?", v:lSlider<=L_B_BOUNDS.lo?"YES":"NO",\n'
    '                  c:lSlider<=L_B_BOUNDS.lo?GRN:RED },')
splice("B12", "baryon: table title",
    ">SENSITIVITY ACROSS BOUNDS</div>",
    ">MASS AT THE LENGTHS ON RECORD</div>")
splice("B13", "baryon: highlight the geometric length, not the inversion",
    "                  const isMain = Math.abs(r.L - L_B_PREDICTED) < 0.001;",
    "                  const isMain = Math.abs(r.L - L_B_BOUNDS.lo) < 0.001;   // the geometric length, not the inversion")
splice("B14", "baryon: neutron button",
    '{showNeutron ? "▼" : "▶"} NEUTRON TEST (LEADING ORDER)',
    '{showNeutron ? "▼" : "▶"} NEUTRON CHECK (CALIBRATION OUTPUT, NOT A TEST)')
splice("B15", "baryon: neutron panel title",
    "              NEUTRON TEST PASSES AT LEADING ORDER — FIRST TIME IN SQT HISTORY",
    "              NOT A TEST: L_B IS SOLVED FROM m_p, SO BOTH ROWS ARE CALIBRATION OUTPUTS")
splice("B16", "baryon: topology-blind line",
    "                        <strong style={{ color:GRN }}>Topology-blind Borromean ✓</strong>",
    "                        <strong style={{ color:GRY }}>Topology-blind Borromean: p and n identical by construction</strong>")
splice("B17", "baryon: closing paragraph",
    "              All previous prescriptions (A=99, A=363, A=20 with Z_f=φ/6) gave either wrong absolute masses\n"
    "              or wrong n-p ratios. Z_f = 6 with A = 20 gives the first self-consistent result.",
    "              Earlier prescriptions (A=99, A=363, A=20 with Z_f=φ/6) are on record. With A = 20 and Z_f = 6 the length\n"
    "              is solved from m_p, so the match is by construction; at the geometric length 58.006 the formula gives about 759 MeV.")
splice("B18", "baryon: Paper VII items",
    "          OPEN — PAPER VII\n"
    "        </div>\n"
    "        <div style={{ display:\"grid\", gridTemplateColumns:\"1fr 1fr\", gap:16, fontSize:11, color:GRY, lineHeight:1.75 }}>\n"
    "          <div>\n"
    "            <strong style={{ color:TXT }}>Appendix E (new).</strong> Numerical minimization of the ideal\n"
    "            Borromean ropelength to &lt;1% precision. If the minimized value equals 60.19 ± 0.6, the\n"
    "            derivation is closed. Analogous to the Φ precision computation in Appendix D.",
    "          PAPER VII ITEMS\n"
    "        </div>\n"
    "        <div style={{ display:\"grid\", gridTemplateColumns:\"1fr 1fr\", gap:16, fontSize:11, color:GRY, lineHeight:1.75 }}>\n"
    "          <div>\n"
    "            <strong style={{ color:TXT }}>Appendix E.1 — resolved negative (October 2026).</strong> The ideal Borromean\n"
    "            ropelength is at most 58.006 (CFKSW 2006), outside the window 60.194 ± 0.3: the ropelength prediction is\n"
    "            falsified at leading order (ledger §2.15 retracted to Conjecture, §2.92).")

# ---------------------------------------------------------------- main app: header strip, title, footer
splice("H1", "header strip: PDG 2024; W retired; L_B inverted",
    '    { l:"Top",    v:pct(mass(119,1/(8*phi4),37.31),172690), fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },\n'
    '    { l:"Bottom", v:pct(mass(119,0.75,37.31),4180),         fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },\n'
    '    { l:"Tau",    v:pct(mass(3,ZF_LEPTON,3*L_q),1776.86),fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },',
    '    { l:"Top",    v:pct(mass(119,1/(8*phi4),37.31),172570), fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },\n'
    '    { l:"Bottom", v:pct(mass(119,0.75,37.31),4183),         fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },\n'
    '    { l:"Tau",    v:pct(mass(3,ZF_LEPTON,3*L_q),1776.93),fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },')
splice("H2", "header strip: W retired",
    '    { l:"W",      v:pct(m0*Math.pow(phi,27),80379),          fmt:v=>`${v>=0?"+":""}${v.toFixed(3)}%` },',
    '    { l:"W (retired)", v:pct(m0*Math.pow(phi,27),80369.2),   fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },')
splice("H3", "header strip: L_B inverted",
    '    { l:"L_B",    v:null, fmt:()=>`${L_B_PREDICTED.toFixed(3)} fm` },',
    '    { l:"L_B (inverted)", v:null, fmt:()=>`${L_B_PREDICTED.toFixed(3)} fm` },')
splice("H4", "version line",
    "          SQT · v1.9 · Matthew Gifford · Ridgemark CA · April 2026",
    "          SQT · v1.9.1 DRAFT · Matthew Gifford · Ridgemark CA · April 2026 · status corrections October 2026")
splice("H5", "title: no 'Zero Free Parameters'",
    "          Superfluid Quantum Topology — Zero Free Parameters",
    "          Superfluid Quantum Topology — Leading-Order Mass Fit")
splice("H6", "constants line: imports named",
    "· Lepton Zf=1/2π · Top Zf=1/(8φ⁴)\n        </div>",
    "· Lepton Zf=1/2π · Top Zf=1/(8φ⁴) · one anchor (m_e), one selected scale (ξvac), Z_f and L selected per particle\n        </div>")
splice("H7", "footer",
    "        <span>SQT v1.9 · Matthew Gifford · Ridgemark CA · Collaborative synthesis with Gemini (Google AI) and Claude (Anthropic)</span>\n"
    "        <span>m=m₀·(A/Zf)·exp(L/Φreff) · Lepton Zf=1/2π · ν:Zf=ξvac³ · W:m₀·φ²⁷ · α⁻¹:bare·(1+r_p²κ/8π) · L_B={L_B_PREDICTED.toFixed(3)}</span>",
    "        <span>SQT v1.9.1 DRAFT (October 2026 status corrections) · Matthew Gifford · Ridgemark CA · Collaborative synthesis with Gemini (Google AI) and Claude (Anthropic)</span>\n"
    "        <span>m=m₀·(A/Zf)·exp(L/Φreff) · Lepton Zf=1/2π · ν:Zf=ξvac³ · W:m₀·φ²⁷ (retired) · α⁻¹:bare·(1+r_p²κ/8π) · L_B={L_B_PREDICTED.toFixed(3)} (m_p inverted)</span>")

# ---------------------------------------------------------------- write, verify
final = th["t"]
os.makedirs(OUT, exist_ok=True)
open(DST, "w", encoding="utf-8").write(final)
recon = final
for hid, desc, old, new in reversed(HUNKS):
    assert recon.count(new) == 1, f"reverse: {hid}"
    recon = recon.replace(new, old)
assert recon == text, "reverse-splice FAILED"
gone = [s for s in ("Zero Free Parameters", "zero free parameters", "Ashton", "PREFERRED", "⊂ PSL(2,7)<br/>",
                    "FIRST TIME IN SQT HISTORY", "172690", "80379") if s in final]
assert not gone, gone
print(f"input md5 {md5_before}; {len(HUNKS)} hunks; output md5 {hashlib.md5(final.encode()).hexdigest()}; "
      f"reverse splice OK; wrote {DST}")
for hid, desc, old, new in HUNKS:
    print(f"  {hid:4s} {desc}")
