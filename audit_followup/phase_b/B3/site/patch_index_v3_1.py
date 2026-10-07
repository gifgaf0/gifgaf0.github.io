#!/usr/bin/env python3
"""B3 DRAFT: public calculator index.html v3 -> v3.1 (status corrections). Nothing is deployed.

Writes index_v3_1_DRAFT.html next to this script. The live index.html on main is NOT modified.
Discipline: md5 precondition on the source; every anchor asserted unique; reverse splice must return v3 byte-exact.
Usage: python3 patch_index_v3_1.py [path/to/index.html]
"""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "..", "..", "index.html")
DST = os.path.join(HERE, "index_v3_1_DRAFT.html")
V3_MD5 = "a0a6dcd50e3bdf6a4b6a8105e78fef8c"

text = open(SRC, encoding="utf-8").read()
md5_before = hashlib.md5(text.encode("utf-8")).hexdigest()
assert md5_before == V3_MD5, f"source is not the v3 index.html of record (md5 {md5_before})"
th = {"t": text}
HUNKS = []

def splice(hid, desc, old, new):
    t = th["t"]
    assert t.count(old) == 1, f"{hid}: anchor not unique (count={t.count(old)})"
    th["t"] = t.replace(old, new)
    assert th["t"].count(new) == 1, f"{hid}: new text not unique"
    HUNKS.append((hid, desc, old, new))
    print(f"[hunk] {hid} — {desc}")

splice("S1", "title v3 -> v3.1",
    "<title>SQT Geometric Mass Calculator v3</title>",
    "<title>SQT Geometric Mass Calculator v3.1</title>")
splice("S2", "constants comment: no 'zero free parameters'",
    "    // ─────────────────────────── Derived constants (zero free parameters)",
    "    // ─────────────────────────── Constants: one anchor (m_e), one selected scale (ξ_vac = 100φ); per-particle selections in the table")

# ---- particle table: PDG 2024 observed values; anchor and inversion labels
rows = [
    ('src:"G", note:"L=2π from spinor closure; Zf=1 (calibration anchor)" },',
     'src:"A", note:"Calibration anchor: m₀ is set from m_e (A=1, Zf=1, L=2π). The formula at L=2π returns 0.4925 MeV (−3.6%), the r_eff(2π) slack." },'),
    ('obs:2.2,      src:"C", note:"A=crossing number; Zf=Fano base; L=Φφ². Prediction 2.039 MeV is the M̄S current quark mass at μ=2 GeV (PDG compiled quantity); lies inside PDG band 1.90–2.65 MeV." },',
     'obs:2.16,     src:"C", note:"A=crossing number; Zf=Fano base; L=Φφ². Output 2.037 MeV against the M̄S mass at μ=2 GeV, PDG 2024 2.16 ± 0.07 MeV: outside the band (−5.7%)." },'),
    ('L:21.04,  obs:4.67,     src:"C"', 'L:21.04,  obs:4.70,     src:"C"'),
    ('L:29.13,  obs:93,       src:"C"', 'L:29.13,  obs:93.5,     src:"C"'),
    ('L:23.60,  obs:1270,     src:"C"', 'L:23.60,  obs:1273.0,   src:"C"'),
    ('L:3*L_q,  obs:1776.86,  src:"C"', 'L:3*L_q,  obs:1776.93,  src:"C"'),
    ('L:37.31,  obs:4180,     src:"C"', 'L:37.31,  obs:4183,     src:"C"'),
    ('obs:172690,   src:"C", note:"Zf=κ/8 = 1/(8φ⁴) — the κ/8 stabilizer slot per §2.27/§2.36/§4.10 (top quark as torus-hole anchor). Prediction 171,185 MeV (−0.87%).',
     'obs:172570,   src:"C", note:"Zf=κ/8 = 1/(8φ⁴) — the κ/8 stabilizer slot per §2.27/§2.36/§4.10 (top quark as torus-hole anchor). Output 171,185 MeV (−0.80% against PDG 2024).'),
    ('L:L_B,    obs:938.272,  src:"G", note:"A=20 from Alexander poly; Zf=6=|F₇*| (Register 2 Complete)" },',
     'L:L_B,    obs:938.272,  src:"R", note:"INVERTED, NOT A PREDICTION: L_B is solved from m_p. A=20 uses Δ(t,t,t); the standard one-variable Alexander polynomial gives 70. Zf=6 is Conjecture 1. The ideal Borromean ropelength is at most 58.006, where the formula gives ≈759 MeV (−19%): the ropelength prediction is falsified at leading order (ledger §2.92)." },'),
]
for i, (old, new) in enumerate(rows, 1):
    splice(f"P{i}", "particle row", old, new)

splice("B1", "PDG bands: PDG 2024 ±1σ; proton band removed (inversion)",
    "      u: [1.90, 2.65],\n      d: [4.40, 4.90],\n      s: [91, 99],\n      c: [1240, 1300],\n      b: [4150, 4210],\n      t: [171000, 174300],\n"
    "      e: [0.510999, 0.511001],\n      mu: [105.6583, 105.6584],\n      tau: [1776.8, 1776.9],\n      p: [938.272, 938.273],\n    };",
    "      u: [2.09, 2.23],          // PDG 2024: 2.16 ± 0.07\n      d: [4.63, 4.77],          // 4.70 ± 0.07\n      s: [92.7, 94.3],          // 93.5 ± 0.8\n"
    "      c: [1268.4, 1277.6],      // 1273.0 ± 4.6\n      b: [4176, 4190],          // 4183 ± 7\n      t: [172280, 172860],      // 172570 ± 290 (direct)\n"
    "      e: [0.510999, 0.511001],\n      mu: [105.6583, 105.6584],\n      tau: [1776.84, 1777.02],  // 1776.93 ± 0.09\n"
    "      // no proton band: the proton row is an inversion (L_B solved from m_p)\n    };")
splice("L1", "source labels: ANCHOR and INVERTED",
    '    const srcColor = (s) => s==="G" ? C.grn : s==="C" ? C.cya : C.org;\n'
    '    const srcLabel = (s) => s==="G" ? "DERIVED" : s==="C" ? "CONJECTURE" : "OPEN";',
    '    const srcColor = (s) => s==="A" ? C.grn : s==="G" ? C.grn : s==="C" ? C.cya : s==="R" ? C.red : C.org;\n'
    '    const srcLabel = (s) => s==="A" ? "ANCHOR" : s==="G" ? "DERIVED" : s==="C" ? "CONJECTURE" : s==="R" ? "INVERTED" : "OPEN";')

splice("A1", "Mass Audit: status banner",
    '      return (\n        <div>\n          <div style={{ display:"flex", gap:8, marginBottom:12, flexWrap:"wrap" }}>\n            {["all","lepton","quark","baryon"]',
    '      return (\n        <div>\n'
    '          <div style={{ background:C.panel2, border:`1px solid ${C.amb}55`, borderLeft:`3px solid ${C.amb}`, borderRadius:4, padding:"10px 14px", marginBottom:12, fontFamily:C.mono, fontSize:10, color:C.txt2, lineHeight:1.7 }}>\n'
    '            <span style={{ color:C.amb, letterSpacing:1 }}>STATUS · OCTOBER 2026 · </span>\n'
    '            This table is a leading-order fit, not a set of predictions: one anchor (m_e), one selected scale (ξ_vac = 100φ,\n'
    '            no combinatorial address) and per-particle selections (knot, A, Z_f, L) — about nine selected inputs for eight\n'
    '            comparison rows. Observed values are PDG 2024; against them only b, t and τ fall within 2%. The proton row is the\n'
    '            proton mass run backwards; at the ideal Borromean ropelength (at most 58.006) the formula gives about 759 MeV.\n'
    '            Ledger §2.92.\n'
    '          </div>\n'
    '          <div style={{ display:"flex", gap:8, marginBottom:12, flexWrap:"wrap" }}>\n            {["all","lepton","quark","baryon"]')

splice("A2", "Mass Audit footnote: up-quark band and W/Z status",
    "Up quark prediction (2.039 MeV) is the M̄S current quark mass at μ=2 GeV and sits inside the PDG band 1.90–2.65 MeV (flagged IN PDG BAND).",
    "The up-quark output (2.037 MeV) is compared with the M̄S mass at μ=2 GeV; PDG 2024 gives 2.16 ± 0.07 MeV, so it lies outside the band (−5.7%).")
splice("A3", "Mass Audit footnote: W and Z retired",
    "W and Z bosons appear in §2.1 of the ledger but their structural assignments (A, Zf, L) are not yet wired into the calculator.",
    "W and Z are not in this table; their formulas (m_W = m₀φ²⁷, sin²θ_W = φ⁻³) are retired, being 2.2% and 3.0% off PDG 2024 at more than 100σ.")

splice("K1", "Constants: section title scoped",
    '<Section title="DERIVED CONSTANTS — STRUCTURAL FORM, ONE FITTED SCALE (m₀*)" accent={C.cya}>',
    '<Section title="CONSTANTS — ONE ANCHOR (m_e), ONE SELECTED SCALE (ξ_vac), STRUCTURAL FORMS AT REGISTER 2" accent={C.cya}>')
splice("K2", "Constants: ξ_vac labelled selected",
    '<Stat l="ξ_vac"             v={`${XI_VAC.toFixed(4)} fm`} s="100φ" />',
    '<Stat l="ξ_vac"             v={`${XI_VAC.toFixed(4)} fm`} s="100φ — selected; no combinatorial address (§2.64.A)" />')
splice("K3", "Constants: L_B labelled an inversion",
    '<Stat l="L_B (Borromean)"   v={`${L_B.toFixed(4)} fm`} s="solved for m_p=938.272 MeV" />',
    '<Stat l="L_B (Borromean)"   v={`${L_B.toFixed(4)} fm`} s="m_p run backwards — an inversion, not a prediction" />')

splice("Y1", "Baryon: ideal-length constant replaces the 'Ashton bounds'",
    "      const ashtonLo = 58.006, ashtonHi = 62.0;\n      const inAshton = L_B >= ashtonLo && L_B <= ashtonHi;",
    "      const idealMax = 58.006;                    // presumed-minimal tight Borromean rings (CFKSW 2006): ideal ropelength ≤ 58.006\n"
    "      const m_ideal = massFn(A_B, ZF_B, idealMax);")
splice("Y2", "Baryon: section title",
    '<Section title="OPEN PROBLEM 5 · BORROMEAN BARYON MASS" accent={C.amb}>',
    '<Section title="BORROMEAN BARYON MASS · ROPELENGTH PREDICTION FALSIFIED AT LEADING ORDER" accent={C.red}>')
splice("Y3", "Baryon: stats",
    '              <Stat l="A = Σ coeff² (Alexander poly)" v="20" />\n'
    '              <Stat l="Zf = |F₇*|"   v="6" />\n'
    '              <Stat l="L_B (solved)" v={`${L_B.toFixed(4)} fm`} />\n'
    '              <Stat l="Ashton bounds" v={`[${ashtonLo}, ${ashtonHi}] fm`} color={inAshton ? C.grn : C.red} />\n'
    '              <Stat l="Predicted m_p" v={fmtMeV(pred_p)} />\n'
    '              <Stat l="PDG m_p"       v="938.272 MeV" color={C.txt2} />\n'
    '              <Stat l="Δ"             v={fmtPct(pct(pred_p, 938.272))} color={errColor(pct(pred_p, 938.272))} />',
    '              <Stat l="A = Σ coeff² of Δ(t,t,t)" v="20" s="standard one-variable Δ gives 70" />\n'
    '              <Stat l="Zf = |F₇*|"   v="6" s="Conjecture 1" />\n'
    '              <Stat l="L_B (solved from m_p)" v={`${L_B.toFixed(4)} fm`} s="inversion" />\n'
    '              <Stat l="Ideal ropelength" v={`≤ ${idealMax} fm`} color={C.red} />\n'
    '              <Stat l="m_p at L_B" v={fmtMeV(pred_p)} s="by construction" />\n'
    '              <Stat l="m_p at 58.006" v={fmtMeV(m_ideal)} color={C.red} />\n'
    '              <Stat l="PDG m_p"       v="938.272 MeV" color={C.txt2} />\n'
    '              <Stat l="Δ at 58.006"   v={fmtPct(pct(m_ideal, 938.272))} color={C.red} />')
splice("Y4", "Baryon: explanatory text",
    "              A=20 from the Borromean Alexander polynomial. L_B sits inside the Ashton bounds [58.006, 62.0] fm.",
    "              A=20 uses the diagonal specialization Δ(t,t,t) = (t^½ − t^−½)³; the standard one-variable Alexander polynomial,\n"
    "              (t − 1)⁴, gives 70. L_B = 60.194 is the proton mass run backwards, so matching m_p is not a test. 58.006 is the\n"
    "              length of the presumed-minimal tight Borromean rings (Cantarella, Fu, Kusner, Sullivan &amp; Wrinkle, 2006), so the\n"
    "              ideal ropelength is at most 58.006, where the formula gives about 759 MeV (−19%). By its own pre-stated window\n"
    "              (60.194 ± 0.3) the prediction is falsified at leading order, and ledger §2.15 is retracted to Conjecture (§2.92).")

splice("Y5", "Conjecture 1 sketch, step 8: F₇* is not a subgroup of PSL(2,7)",
    '["8","ℤ/6ℤ ≅ F₇* canonical in PSL(2,7) context","R1"],',
    '["8","ℤ/6ℤ ≅ F₇* — corrected Oct. 2026: F₇* is not a subgroup of PSL(2,7) (no element of order 6); the Fano-triangle stabilizer there is S₃","corr."],')

splice("M1", "mass-formula legend: L conventions named",
    "A — knot winding index &nbsp;·&nbsp; Zf — topological partition factor &nbsp;·&nbsp; L — ropelength (fm)",
    "A — knot winding index &nbsp;·&nbsp; Zf — topological partition factor &nbsp;·&nbsp; L — ropelength (fm)<br/>\n"
    "              L conventions are mixed: the quark values are ideal ropelengths per tube diameter (trefoil 16.372 = 32.743 per\n"
    "              radius; no nontrivial knot is below 31.32 per radius), while L_e = 2π and the Borromean 58.006 are per radius.")

splice("H1", "header version line",
    "                SUPERFLUID QUANTUM TOPOLOGY · v3 · MAY 2026",
    "                SUPERFLUID QUANTUM TOPOLOGY · v3.1 · OCTOBER 2026 · STATUS CORRECTIONS")
splice("H2", "header paragraph scoped",
    "                Particle masses from knot topology, division-algebra structure, and Fano-plane combinatorics.\n"
    "                Constants flow from φ and π; the calibration form m_e = m₀·exp(2π/Φ) is structurally derived\n"
    "                (§2.14), with m₀'s scalar value absorbing the §2.50.A continuum/discrete slack.",
    "                A leading-order fit of particle masses to knot topology, division-algebra structure and Fano-plane\n"
    "                combinatorics: one anchor (m_e), one selected scale (ξ_vac = 100φ) and per-particle selections (knot, A,\n"
    "                Z_f, L). It is not a zero-parameter derivation. Comparisons use PDG 2024. The proton-ropelength prediction is\n"
    "                falsified at leading order (October 2026).")
splice("H3", "header badges",
    '                <Badge label="DERIVED" col={C.grn} />\n                <Badge label="CONJECTURE" col={C.cya} />',
    '                <Badge label="ANCHOR" col={C.grn} />\n                <Badge label="FIT" col={C.amb} />\n'
    '                <Badge label="CONJECTURE" col={C.cya} />\n                <Badge label="INVERTED" col={C.red} />')
splice("F1", "footer status line",
    "              §4.7 top-knot tension (7₁ vs 8₁) remains Priority 1 blocking.",
    "              §4.7 top-knot tension (7₁ vs 8₁) remains Priority 1 blocking.<br/>\n"
    "              v3.1 (October 2026): status corrections per ledger §2.92 — proton-ropelength prediction falsified at leading\n"
    "              order (§2.15 retracted to Conjecture); mass table relabelled a leading-order fit; PDG 2024 comparison values.")

final = th["t"]
open(DST, "w", encoding="utf-8").write(final)
md5_after = hashlib.md5(final.encode("utf-8")).hexdigest()
recon = final
for hid, desc, old, new in reversed(HUNKS):
    assert recon.count(new) == 1, f"reverse: {hid}"
    recon = recon.replace(new, old)
assert hashlib.md5(recon.encode("utf-8")).hexdigest() == md5_before, "reverse-splice FAILED"
print(f"[v3] md5 {md5_before} -> [v3.1 DRAFT] md5 {md5_after}; {len(HUNKS)} hunks; reverse-splice OK")
leftover = [s for s in ("zero free parameters", "Ashton bounds", "ashtonLo", "inAshton", "(Register 2 Complete)") if s in final]
print("strings that must be gone:", leftover if leftover else "none")
assert not leftover
