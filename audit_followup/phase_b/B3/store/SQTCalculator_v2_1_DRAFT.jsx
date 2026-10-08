import { useState } from "react";

// ═══════════════════════════════════════════════════════════════
//  SQT MASS CALCULATOR v2.0
//  Superfluid Quantum Topology — Geometric Mass Operator
//  Leading-order fit: one anchor (m_e), one selected scale (ξ_vac = 100φ) and
//  per-particle selections (knot, A, Z_f, L). Not a zero-parameter derivation.
//  v2.1 DRAFT (October 2026): status corrections per ledger §2.92; PDG 2024 values.
// ═══════════════════════════════════════════════════════════════

const phi     = (1 + Math.sqrt(5)) / 2;
const phi2    = phi * phi;
const phi4    = phi2 * phi2;
const TWO_PI  = 2 * Math.PI;
const PHI     = TWO_PI - phi2 / (8 * Math.PI * Math.PI);  // Φ ≈ 6.2500
const m0      = 0.511 / Math.exp(TWO_PI / PHI);            // m₀ ≈ 0.18699 MeV
const kappa   = 1 / phi4;                                   // κ = φ⁻⁴ ≈ 0.1459
const XI_VAC  = 100 * phi;                                  // ξ_vac = 100φ ≈ 161.8 (selected; no combinatorial address, §2.64.A)
const ZF_LEP  = 1 / (2 * Math.PI);
const L_q     = PHI * phi2;                                 // Φφ² ≈ 16.363

// Borromean baryon (proton)
const A_B  = 20;   // Σcoeff² of Δ(t,t,t) = 1+9+9+1 (the standard one-variable Δ gives 70)
const ZF_B = 6;    // |F₇*| — multiplicative group of F₇

function rEff(L) { return 1 + Math.log(1 + L / XI_VAC); }
function massFn(A, Zf, L) {
  if (L === 0) return m0 * (A / Zf);
  return m0 * (A / Zf) * Math.exp(L / (PHI * rEff(L)));
}
function pct(pred, obs) { return ((pred - obs) / obs * 100); }
function fmtMeV(v) {
  if (v >= 1e6)   return `${(v/1e6).toFixed(3)} TeV`;
  if (v >= 1e3)   return `${(v/1e3).toFixed(3)} GeV`;
  if (v < 0.001)  return `${(v*1e6).toFixed(2)} eV`;
  return `${v.toFixed(4)} MeV`;
}
function fmtPct(e) {
  const s = e >= 0 ? "+" : "";
  return `${s}${e.toFixed(2)}%`;
}

// Bisect for proton ropelength
function solveL(m_target) {
  let lo = 1, hi = 200;
  for (let i = 0; i < 80; i++) {
    const mid = (lo + hi) / 2;
    massFn(A_B, ZF_B, mid) < m_target ? lo = mid : hi = mid;
  }
  return (lo + hi) / 2;
}
const L_B = solveL(938.272);

// ── Particle table ──────────────────────────────────────────────
// Source column: A = anchor, C = conjecture, F = fitted, R = inverted (not a prediction)
const PARTICLES = [
  { id:"e",   label:"Electron", sym:"e⁻",  type:"lepton", gen:1,
    knot:"0₁ (unknot)",         A:1,   Zf:1,       L:TWO_PI,
    obs:0.511,    src:"A", note:"Calibration anchor: m₀ is set from m_e (A=1, Zf=1, L=2π); the formula returns 0.4925 MeV (−3.6%), the r_eff(2π) slack" },
  { id:"u",   label:"Up",       sym:"u",   type:"quark",  gen:1,
    knot:"3₁ (trefoil)",        A:3,   Zf:3,       L:16.372,
    obs:2.16,     src:"C", note:"A=crossing number; Zf=Fano base; L≈Φφ². PDG 2024 2.16 ± 0.07 MeV: output outside the band (−5.6%)" },
  { id:"d",   label:"Down",     sym:"d",   type:"quark",  gen:1,
    knot:"4₁ (figure-8)",       A:11,  Zf:9,       L:21.04,
    obs:4.70,     src:"C", note:"A from Alexander poly; Zf=3² amphicheiral" },
  { id:"mu",  label:"Muon",     sym:"μ⁻",  type:"lepton", gen:2,
    knot:"(2,1)-cable 0₁",      A:1,   Zf:ZF_LEP,  L:2*L_q,
    obs:105.658,  src:"C", note:"Gen II lepton: double cable of unknot" },
  { id:"s",   label:"Strange",  sym:"s",   type:"quark",  gen:2,
    knot:"6₁",                  A:107, Zf:12,      L:29.13,
    obs:93.5,     src:"C", note:"Zf=12 chiral tetrahedral T⊂O" },
  { id:"c",   label:"Charm",    sym:"c",   type:"quark",  gen:2,
    knot:"5₁ (torus)",          A:5,   Zf:1/48,    L:23.60,
    obs:1273.0,   src:"C", note:"Zf=1/48 bilateral octahedral inversion" },
  { id:"tau", label:"Tau",      sym:"τ⁻",  type:"lepton", gen:3,
    knot:"(3,1)-cable 3₁",      A:3,   Zf:ZF_LEP,  L:3*L_q,
    obs:1776.93,  src:"C", note:"Gen III lepton: triple cable of trefoil" },
  { id:"b",   label:"Bottom",   sym:"b",   type:"quark",  gen:3,
    knot:"8₁",                  A:119, Zf:3/4,     L:37.31,
    obs:4183,     src:"C", note:"Zf=3/4 C₃/C₄ phase lock" },
  { id:"t",   label:"Top",      sym:"t",   type:"quark",  gen:3,
    knot:"8₁⁹",                 A:119, Zf:1/(8*phi4), L:37.31,
    obs:172570,   src:"F", note:"Zf=κ/8=1/(8φ⁴) is fitted (ledger §2.92 counts it among the six fitted Z_f); −0.80% against PDG 2024" },
  { id:"p",   label:"Proton",   sym:"p",   type:"baryon", gen:null,
    knot:"Borromean rings",      A:A_B, Zf:ZF_B,    L:L_B,
    obs:938.272,  src:"R", note:"INVERTED: L_B is solved from m_p, so the match is by construction. A=20 uses Δ(t,t,t) (standard Δ gives 70); Zf=6 is Conjecture 1. At the ideal ropelength (≤ 58.006) the formula gives ≈759 MeV" },
];

// ── Colors ──────────────────────────────────────────────────────
const C = {
  bg:    "#05050f",
  panel: "#0a0a1a",
  brd:   "#1c1c35",
  brd2:  "#252545",
  grn:   "#00e5a0",
  amb:   "#f5a623",
  org:   "#ff6b35",
  red:   "#ff3b5c",
  cya:   "#00d4ff",
  prp:   "#b07cff",
  blu:   "#4d9fff",
  gry:   "#5a5a7a",
  dim:   "#3a3a5a",
  txt:   "#d8d8f0",
  txt2:  "#8888aa",
  mono:  "'IBM Plex Mono', 'Courier New', monospace",
  sans:  "'IBM Plex Sans', system-ui, sans-serif",
};

function errColor(e) {
  const a = Math.abs(e);
  if (a < 2)  return C.grn;
  if (a < 8)  return C.amb;
  if (a < 25) return C.org;
  return C.red;
}
function srcColor(s) {
  if (s === "A" || s === "G") return C.grn;
  if (s === "C") return C.cya;
  if (s === "R") return C.red;
  return C.org;
}
function srcLabel(s) {
  if (s === "A") return "ANCHOR";
  if (s === "G") return "DERIVED";
  if (s === "C") return "CONJECTURE";
  if (s === "F") return "FIT";
  if (s === "R") return "INVERTED";
  return "OPEN";
}
function typeColor(t) {
  if (t === "lepton") return C.prp;
  if (t === "baryon") return C.amb;
  return C.cya;
}

// ── Sub-components ───────────────────────────────────────────────
function Badge({ label, col }) {
  return (
    <span style={{
      fontFamily: C.mono, fontSize: 8, color: col,
      border: `1px solid ${col}`, borderRadius: 2,
      padding: "1px 5px", letterSpacing: 1,
      whiteSpace: "nowrap", opacity: 0.9,
    }}>{label}</span>
  );
}

function GenDot({ gen }) {
  const cols = [null, C.grn, C.amb, C.prp];
  if (!gen) return <span style={{ color: C.dim, fontFamily: C.mono, fontSize: 10 }}>—</span>;
  return (
    <span style={{ display: "flex", gap: 3, alignItems: "center" }}>
      {[1,2,3].map(g => (
        <span key={g} style={{
          width: 6, height: 6, borderRadius: "50%",
          background: g <= gen ? cols[g] : C.brd2,
          display: "inline-block",
        }} />
      ))}
    </span>
  );
}

function ParticleRow({ p, selected, onSelect }) {
  const pred = massFn(p.A, p.Zf, p.L);
  const err  = pct(pred, p.obs);
  const ec   = errColor(err);
  const isSelected = selected === p.id;

  return (
    <>
      <tr
        onClick={() => onSelect(isSelected ? null : p.id)}
        style={{
          cursor: "pointer",
          background: isSelected ? "#12122a" : "transparent",
          borderBottom: `1px solid ${C.brd}`,
          transition: "background 0.15s",
        }}
      >
        <td style={{ padding: "10px 12px", fontFamily: C.mono, fontSize: 13, color: typeColor(p.type) }}>
          {p.sym}
        </td>
        <td style={{ padding: "10px 8px" }}>
          <div style={{ color: C.txt, fontSize: 13, fontFamily: C.sans }}>{p.label}</div>
          <div style={{ color: C.gry, fontSize: 10, fontFamily: C.mono, marginTop: 2 }}>{p.knot}</div>
        </td>
        <td style={{ padding: "10px 8px", textAlign: "right" }}>
          <GenDot gen={p.gen} />
        </td>
        <td style={{ padding: "10px 12px", textAlign: "right", fontFamily: C.mono, fontSize: 12, color: C.txt2 }}>
          {fmtMeV(p.obs)}
        </td>
        <td style={{ padding: "10px 12px", textAlign: "right", fontFamily: C.mono, fontSize: 12, color: C.txt }}>
          {fmtMeV(pred)}
        </td>
        <td style={{ padding: "10px 12px", textAlign: "right", fontFamily: C.mono, fontSize: 13, color: ec, fontWeight: 600 }}>
          {fmtPct(err)}
        </td>
        <td style={{ padding: "10px 12px", textAlign: "center" }}>
          <Badge label={srcLabel(p.src)} col={srcColor(p.src)} />
        </td>
      </tr>
      {isSelected && (
        <tr style={{ background: "#0e0e22", borderBottom: `1px solid ${C.brd}` }}>
          <td colSpan={7} style={{ padding: "10px 16px 14px 16px" }}>
            <div style={{ display: "flex", gap: 32, flexWrap: "wrap" }}>
              <Detail label="A (winding)" val={p.A} />
              <Detail label="Zf (topology)" val={
                Math.abs(p.Zf - 1/(8*phi4)) < 1e-9 ? "1/(8φ⁴)" :
                Math.abs(p.Zf - 1/(2*Math.PI)) < 1e-10 ? "1/2π" :
                Math.abs(p.Zf - 0.75) < 1e-6 ? "3/4" :
                p.Zf < 1 ? `1/${Math.round(1/p.Zf)}` : String(p.Zf)
              } />
              <Detail label="L (ropelength)" val={`${p.L.toFixed(3)} fm`} />
              <Detail label="Predicted" val={fmtMeV(pred)} hi />
            </div>
            <div style={{ marginTop: 8, fontFamily: C.mono, fontSize: 10, color: C.gry }}>
              {p.note}
            </div>
          </td>
        </tr>
      )}
    </>
  );
}

function Detail({ label, val, hi }) {
  return (
    <div>
      <div style={{ fontFamily: C.mono, fontSize: 9, color: C.gry, letterSpacing: 1, marginBottom: 2 }}>{label}</div>
      <div style={{ fontFamily: C.mono, fontSize: 13, color: hi ? C.cya : C.txt }}>{val}</div>
    </div>
  );
}

function ProtonPanel() {
  const pred = massFn(A_B, ZF_B, L_B);
  const predIdeal = massFn(A_B, ZF_B, L_B_IDEAL_MAX);
  const errIdeal  = pct(predIdeal, 938.272);
  return (
    <div style={{
      background: C.panel, border: `1px solid ${C.amb}22`,
      borderRadius: 8, padding: "18px 20px", marginTop: 16,
    }}>
      <div style={{ fontFamily: C.mono, fontSize: 9, color: C.amb, letterSpacing: 3, marginBottom: 14 }}>
        BORROMEAN BARYON MASS · ROPELENGTH PREDICTION FALSIFIED AT LEADING ORDER
      </div>
      <div style={{ display: "flex", gap: 32, flexWrap: "wrap", marginBottom: 12 }}>
        <Detail label="A = Σcoeff² of Δ(t,t,t)" val="20 (standard Δ: 70)" />
        <Detail label="Zf = |F₇*| (Conjecture 1)" val="6" />
        <Detail label="L_B (solved from m_p)" val={`${L_B.toFixed(3)} fm`} />
        <Detail label="Ideal ropelength" val={`≤ ${L_B_IDEAL_MAX} fm`} />
        <Detail label="m_p at L_B (by construction)" val={fmtMeV(pred)} />
        <Detail label="m_p at 58.006" val={fmtMeV(predIdeal)} hi />
        <Detail label="PDG m_p" val="938.272 MeV" />
        <Detail label="Error at 58.006" val={fmtPct(errIdeal)} />
      </div>
      <div style={{ fontFamily: C.mono, fontSize: 10, color: C.gry, lineHeight: 1.6 }}>
        L_B = {L_B.toFixed(3)} fm is the proton mass run backwards, so matching m_p is not a test. 58.006 is the length of
        the presumed-minimal tight Borromean rings (Cantarella–Fu–Kusner–Sullivan–Wrinkle 2006), so the ideal ropelength is at
        most 58.006, where the formula gives about 759 MeV: the ropelength prediction is falsified at leading order (ledger
        §2.15 retracted to Conjecture, §2.92). A=20 uses Δ(t,t,t); the standard one-variable Alexander polynomial gives 70.
        Zf=6=|F₇*| is Conjecture 1 (Riemann-Hurwitz proof pending).
      </div>
    </div>
  );
}

const L_B_IDEAL_MAX = 58.006;   // presumed-minimal tight Borromean rings (CFKSW 2006): ideal ropelength ≤ 58.006

function ConstantsPanel() {
  const consts = [
    { label: "φ (golden ratio)",    val: phi.toFixed(6),    src: "axiom" },
    { label: "Φ (throat angle)",    val: PHI.toFixed(6),    src: "structural form 2π − φ²/8π² (Register 2)" },
    { label: "m₀ (base mass)",      val: `${m0.toFixed(5)} MeV`, src: "anchor: m_e/exp(2π/Φ)" },
    { label: "κ (bulk modulus)",     val: kappa.toFixed(6),  src: "φ⁻⁴" },
    { label: "ξ_vac (corr. length)",val: `${XI_VAC.toFixed(3)} fm`, src: "selected: 100φ (no combinatorial address)" },
  ];
  return (
    <div style={{
      background: C.panel, border: `1px solid ${C.brd}`,
      borderRadius: 8, padding: "18px 20px", marginTop: 16,
    }}>
      <div style={{ fontFamily: C.mono, fontSize: 9, color: C.gry, letterSpacing: 3, marginBottom: 14 }}>
        CONSTANTS · ONE ANCHOR (m_e) · ONE SELECTED SCALE (ξ_vac)
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "10px 32px" }}>
        {consts.map(c => (
          <div key={c.label} style={{ minWidth: 180 }}>
            <div style={{ fontFamily: C.mono, fontSize: 9, color: C.gry, marginBottom: 2 }}>{c.label}</div>
            <div style={{ fontFamily: C.mono, fontSize: 13, color: C.cya }}>{c.val}</div>
            <div style={{ fontFamily: C.mono, fontSize: 9, color: C.dim, marginTop: 1 }}>{c.src}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Main app ─────────────────────────────────────────────────────
export default function SQTCalculator() {
  const [selected, setSelected]   = useState(null);
  const [filter, setFilter]       = useState("all");
  const [showConst, setShowConst] = useState(false);
  const [showProton, setShowProton] = useState(true);

  const filtered = PARTICLES.filter(p =>
    filter === "all" || p.type === filter
  );

  const outputs = PARTICLES.filter(p => p.src !== "A" && p.src !== "R");   // the anchor and the inverted row are not tests
  const within  = lim => outputs.filter(p => Math.abs(pct(massFn(p.A, p.Zf, p.L), p.obs)) < lim).length;

  return (
    <div style={{
      background: C.bg, minHeight: "100vh", padding: "24px 16px",
      fontFamily: C.sans, color: C.txt,
    }}>
      <div style={{ maxWidth: 860, margin: "0 auto" }}>

        {/* Header */}
        <div style={{ marginBottom: 24 }}>
          <div style={{ fontFamily: C.mono, fontSize: 10, color: C.cya, letterSpacing: 4, marginBottom: 8 }}>
            SUPERFLUID QUANTUM TOPOLOGY
          </div>
          <h1 style={{
            fontSize: 26, fontWeight: 700, margin: 0, letterSpacing: -0.5,
            color: C.txt, lineHeight: 1.2,
          }}>
            Geometric Mass Calculator
          </h1>
          <p style={{ color: C.txt2, fontSize: 13, marginTop: 8, lineHeight: 1.5, maxWidth: 580 }}>
            A leading-order fit of particle masses to knot topology, division algebra structure
            and Fano plane combinatorics: one anchor (m_e), one selected scale (ξ_vac = 100φ) and
            per-particle selections (knot, A, Z_f, L). Not a zero-parameter derivation; PDG 2024 values.
          </p>
          <div style={{ display: "flex", gap: 12, marginTop: 12, flexWrap: "wrap" }}>
            <Badge label={`${within(2)}/${outputs.length} WITHIN 2%`} col={C.grn} />
            <Badge label={`${within(8)}/${outputs.length} WITHIN 8%`} col={C.grn} />
            <Badge label="ANCHOR" col={C.grn} />
            <Badge label="FIT" col={C.org} />
            <Badge label="CONJECTURE" col={C.cya} />
            <Badge label="INVERTED" col={C.red} />
            <Badge label="OPEN PROBLEM" col={C.org} />
          </div>
        </div>

        {/* Filter tabs */}
        <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          {["all","lepton","quark","baryon"].map(f => (
            <button key={f} onClick={() => setFilter(f)} style={{
              fontFamily: C.mono, fontSize: 10, letterSpacing: 1,
              padding: "5px 14px", borderRadius: 3, cursor: "pointer",
              border: `1px solid ${filter === f ? C.cya : C.brd}`,
              background: filter === f ? `${C.cya}18` : "transparent",
              color: filter === f ? C.cya : C.gry,
              textTransform: "uppercase",
            }}>{f}</button>
          ))}
        </div>

        {/* Mass table */}
        <div style={{
          background: C.panel, border: `1px solid ${C.brd}`,
          borderRadius: 8, overflow: "hidden",
        }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: `1px solid ${C.brd2}` }}>
                {["","Particle / Knot","Gen","PDG Mass","SQT Prediction","Error","Status"].map((h,i) => (
                  <th key={i} style={{
                    padding: "10px 12px", textAlign: i >= 3 ? "right" : i === 2 ? "center" : "left",
                    fontFamily: C.mono, fontSize: 9, color: C.gry,
                    letterSpacing: 1.5, fontWeight: 400,
                    ...(i === 6 ? { textAlign: "center" } : {}),
                  }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map(p => (
                <ParticleRow key={p.id} p={p} selected={selected} onSelect={setSelected} />
              ))}
            </tbody>
          </table>
        </div>

        <div style={{ fontFamily: C.mono, fontSize: 9, color: C.gry, marginTop: 8, marginLeft: 4 }}>
          Click any row to expand geometric parameters. This table is a leading-order fit (about nine selected inputs for eight
          rows; ledger §2.92). Against PDG 2024 only b, t and τ fall within 2%.
        </div>

        {/* Proton toggle */}
        <div style={{ marginTop: 20 }}>
          <button onClick={() => setShowProton(v => !v)} style={{
            fontFamily: C.mono, fontSize: 9, letterSpacing: 2,
            padding: "6px 14px", borderRadius: 3, cursor: "pointer",
            border: `1px solid ${C.amb}`, background: "transparent",
            color: C.amb,
          }}>
            {showProton ? "▼" : "▶"} PROTON / BORROMEAN BARYON
          </button>
          {showProton && <ProtonPanel />}
        </div>

        {/* Constants toggle */}
        <div style={{ marginTop: 12 }}>
          <button onClick={() => setShowConst(v => !v)} style={{
            fontFamily: C.mono, fontSize: 9, letterSpacing: 2,
            padding: "6px 14px", borderRadius: 3, cursor: "pointer",
            border: `1px solid ${C.brd2}`, background: "transparent",
            color: C.gry,
          }}>
            {showConst ? "▼" : "▶"} CONSTANTS
          </button>
          {showConst && <ConstantsPanel />}
        </div>

        {/* Mass formula */}
        <div style={{
          marginTop: 20, padding: "14px 18px",
          background: C.panel, border: `1px solid ${C.brd}`,
          borderRadius: 8,
        }}>
          <div style={{ fontFamily: C.mono, fontSize: 9, color: C.gry, letterSpacing: 2, marginBottom: 10 }}>
            MASS OPERATOR
          </div>
          <div style={{ fontFamily: C.mono, fontSize: 13, color: C.cya, lineHeight: 2 }}>
            m(A, Zf, L) = m₀ · (A/Zf) · exp(L / (Φ · r_eff(L)))
          </div>
          <div style={{ fontFamily: C.mono, fontSize: 11, color: C.txt2, lineHeight: 2, marginTop: 4 }}>
            r_eff(L) = 1 + ln(1 + L/ξ_vac) &nbsp;·&nbsp; ξ_vac = 100φ<br/>
            A = knot winding index &nbsp;·&nbsp; Zf = topological partition factor &nbsp;·&nbsp; L = ropelength (fm)<br/>
            L conventions are mixed: the quark values are ideal ropelengths per tube diameter (trefoil 16.372 = 32.743 per
            radius; no nontrivial knot is below 31.32 per radius), while L_e = 2π and the Borromean 58.006 are per radius.
          </div>
        </div>

        {/* Footer */}
        <div style={{
          marginTop: 24, paddingTop: 16,
          borderTop: `1px solid ${C.brd}`,
          fontFamily: C.mono, fontSize: 9, color: C.gry,
          lineHeight: 1.8,
        }}>
          SQT Framework · M. Gifford · 2026 &nbsp;·&nbsp;
          Gauge group paper: <span style={{ color: C.cya }}>Zenodo record 21316171 (Császár polyhedron)</span> &nbsp;·&nbsp;
          Ropelength paper: <span style={{ color: C.cya }}>Paper 1A</span><br/>
          Parameters labeled CONJECTURE or OPEN PROBLEM are structural but not yet formally derived.
          v2.1 DRAFT (October 2026): status corrections per ledger §2.92.
        </div>

      </div>
    </div>
  );
}
